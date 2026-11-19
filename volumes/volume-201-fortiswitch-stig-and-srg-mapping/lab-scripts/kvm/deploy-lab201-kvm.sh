#!/usr/bin/env bash
# Create the Volume CCI lab virtual machines on a Linux host with KVM and libvirt.
#
# Run as root (or as a member of the libvirt group) on a host with libvirt,
# virt-install 4.0 or later, qemu-img, and Python 3. It reads
# ../common/lab201-vms.json, downloads and checks the cloud image for each Linux
# flavor in use, makes a copy-on-write disk for each machine, renders a cloud-init
# seed with ../common/make-seed.py, and creates and starts the machines with
# virt-install.
#
# VLAN tags are created inside the guests (the seeds use --tagging guest), so the
# bridges can be plain Linux bridges. Create them before you run the script:
#   --bridge-t1     the NIC that cables to sw-648f-1 is a port of this bridge
#   --bridge-t2     the NIC that cables to sw-2048f-1 is a port of this bridge
#   --bridge-oob    the NIC that cables to the switch management ports
#   --bridge-lan220 no ports (internal)
#   --bridge-wan    reaches the internet (default virbr0, the libvirt NAT network)
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
manifest="$here/../common/lab201-vms.json"
seedtool="$here/../common/make-seed.py"
resolver="$here/../common/resolve-image.py"

action=deploy
bridge_wan=virbr0 bridge_oob=br-oob bridge_t1=br-t1 bridge_t2=br-t2 bridge_lan220=br-lan220
disk_dir=/var/lib/libvirt/images/lab201
workdir=/var/tmp/lab201
dry_run=0
ssh_keys=()
license_file=""
python="python3"
rhel_image=""
snapshot_name=baseline-201
wait_for=0
wait_minutes=30

usage() {
  cat <<EOF
Usage: $0 [options]
  --action ACTION        deploy (default), check, status, remove-build-nics, snapshot, restore, or remove
                           check     tests what a deploy needs on this host and changes nothing
                           status    shows each machine and whether its first boot has finished
                           snapshot  takes the baseline snapshot of every machine (Lab 999.6)
                           restore   returns every machine to the baseline snapshot, running
  --ssh-key FILE         public key for the admin user (repeatable; needed for deploy)
  --bridge-wan|oob|t1|t2|lan220 NAME   bridge for each lab network
  --disk-dir DIR         where the machine disks go (default $disk_dir)
  --workdir DIR          download and render directory (default $workdir)
  --rhel-image FILE      the Red Hat Enterprise Linux 10 qcow2 image you downloaded (for rhel-10 flavors)
  --license-file FILE    JSON file with keys to apply (Red Hat, Ubuntu Pro)
  --python CMD           Python 3 command to use (default python3), for example python3.15
  --snapshot-name NAME   the snapshot that snapshot and restore use (default $snapshot_name)
  --wait                 with status: keep checking until every machine has finished its first boot
  --wait-minutes N       with --wait: give up after N minutes (default $wait_minutes)
  --dry-run              print what would run
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --action) action="$2"; shift 2 ;;
    --ssh-key) ssh_keys+=("$2"); shift 2 ;;
    --bridge-wan) bridge_wan="$2"; shift 2 ;;
    --bridge-oob) bridge_oob="$2"; shift 2 ;;
    --bridge-t1) bridge_t1="$2"; shift 2 ;;
    --bridge-t2) bridge_t2="$2"; shift 2 ;;
    --bridge-lan220) bridge_lan220="$2"; shift 2 ;;
    --disk-dir) disk_dir="$2"; shift 2 ;;
    --workdir) workdir="$2"; shift 2 ;;
    --rhel-image) rhel_image="$2"; shift 2 ;;
    --license-file) license_file="$2"; shift 2 ;;
    --python) python="$2"; shift 2 ;;
    --snapshot-name) snapshot_name="$2"; shift 2 ;;
    --wait) wait_for=1; shift ;;
    --wait-minutes) wait_minutes="$2"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ "$wait_minutes" =~ ^[0-9]+$ ]] || { echo "--wait-minutes must be a number." >&2; exit 2; }
[[ "$snapshot_name" =~ ^[A-Za-z][A-Za-z0-9_-]{1,39}$ ]] ||
  { echo "--snapshot-name must start with a letter and use letters, digits, hyphens, and underscores (2 to 40 characters)." >&2; exit 2; }

run() {
  if [[ "$dry_run" == 1 ]]; then printf 'DRY-RUN:'; printf ' %q' "$@"; printf '\n'; else "$@"; fi
}

bridge_of() {
  case "$1" in
    lab201-wan) echo "$bridge_wan" ;;
    lab201-oob) echo "$bridge_oob" ;;
    lab201-t1) echo "$bridge_t1" ;;
    lab201-t2) echo "$bridge_t2" ;;
    lab201-lan220) echo "$bridge_lan220" ;;
    *) echo "No bridge for network $1" >&2; return 1 ;;
  esac
}

# One line for each machine: name|vcpu|memory_mb|disk_gb|role|flavor|net,mac;net,mac;...
plan() {
  "$python" - "$manifest" "$here/../common/flavors.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
for i, vm in enumerate(m["vms"]):
    flavor = vm.get("flavor") or m.get("default_flavor") or "ubuntu-24.04"
    fl = dict((f["id"], f) for f in json.load(open(sys.argv[2], encoding="utf-8"))["flavors"])
    if fl[flavor].get("iso"):
        sys.exit("%s uses %s, which installs from an ISO. The KVM script guest-tags VLANs, which these guests cannot do. Use the Proxmox script for them." % (vm["name"], flavor))
    nics = ";".join("%s,%s:%02x:%02x" % (n["net"], m["mac_prefix"], i + 1, k) for k, n in enumerate(vm["nics"]))
    print("|".join([vm["name"], str(vm["vcpu"]), str(vm["memory_mb"]), str(vm["disk_gb"]), vm.get("role", ""), flavor, nics]))
PY
}

has_snapshot() { virsh snapshot-list "$1" --name 2>/dev/null | grep -Fxq "$2"; }

# The build state of one machine, as "STATE|detail". STATE is ok, running, failed, starting, stopped, or unknown.
# The QEMU guest agent runs /usr/local/sbin/lab201-status in the machine.
build_state() {
  local name="$1" line
  [[ "$(virsh domstate "$name" 2>/dev/null)" == running ]] || { echo "stopped|"; return; }
  line="$("$python" - "$name" <<'PY' 2>/dev/null
import base64, json, subprocess, sys, time
name = sys.argv[1]


def agent(command):
    r = subprocess.run(["virsh", "qemu-agent-command", name, json.dumps(command), "--timeout", "10"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return json.loads(r.stdout)["return"]


try:
    pid = agent({"execute": "guest-exec", "arguments": {"path": "/usr/local/sbin/lab201-status", "capture-output": True}})["pid"]
    for _ in range(30):
        state = agent({"execute": "guest-exec-status", "arguments": {"pid": pid}})
        if state.get("exited"):
            out = base64.b64decode(state.get("out-data", "")).decode("utf-8", "replace").strip().splitlines()
            print(out[0] if out else "")
            break
        time.sleep(0.5)
except Exception as err:
    print("ERR " + str(err).replace("\n", " "))
PY
)" || line=""
  if [[ "$line" == lab201\ * ]]; then
    echo "$(awk '{ print $2 }' <<<"$line")|$(cut -d' ' -f4- <<<"$line")"
    return
  fi
  case "$line" in
    *"No such file"*) echo "unknown|this machine was built before the status script existed" ;;
    *"has been disabled"*|*"not allowed"*|*"denied"*) echo "unknown|the guest agent of this flavor runs no commands. Log in and run: lab201-status" ;;
    *) echo "starting|the guest agent does not answer yet" ;;
  esac
}

if [[ "$action" == check ]]; then
  # Tests what a deploy needs on this host and changes nothing.
  failed=0
  ok() { printf '[OK]   %s\n' "$1"; }
  warn() { printf '[WARN] %s\n' "$1"; [[ -z "${2:-}" ]] || printf '       %s\n' "$2"; }
  bad() { printf '[FAIL] %s\n' "$1"; [[ -z "${2:-}" ]] || printf '       %s\n' "$2"; failed=$((failed + 1)); }
  echo "Checking this host for the lab build. Nothing is changed."
  for c in virsh qemu-img; do
    if command -v "$c" >/dev/null 2>&1; then ok "$c is installed"; else bad "$c was not found" "Install libvirt and QEMU (for example: apt install libvirt-daemon-system qemu-utils)"; fi
  done
  if command -v virt-install >/dev/null 2>&1; then
    vi="$({ virt-install --version 2>/dev/null || true; } | head -n 1)"
    if [[ "${vi%%.*}" =~ ^[0-9]+$ ]] && (( ${vi%%.*} >= 4 )); then ok "virt-install $vi"
    else bad "virt-install ${vi:-(unknown version)} is older than 4.0" "The script uses --cloud-init, which needs virt-install 4.0 or later"; fi
  else
    bad "virt-install was not found" "Install it (for example: apt install virtinst)"
  fi
  if command -v virsh >/dev/null 2>&1; then
    if virsh list --all >/dev/null 2>&1; then ok "libvirt answers (virsh list)"; else bad "virsh cannot reach libvirt" "Run as root, or add your account to the libvirt group"; fi
  fi
  have_python=0
  if command -v "$python" >/dev/null 2>&1 && "$python" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' 2>/dev/null; then
    ok "Python: $("$python" --version 2>&1)"; have_python=1
  else
    bad "$python is not Python 3.8 or later" "Install python3, or pass --python with the command to use"
  fi
  if [[ ${#ssh_keys[@]} -eq 0 ]]; then
    bad "No SSH public key was given (--ssh-key)" "Make one with: ssh-keygen -t ed25519   Then pass: --ssh-key ~/.ssh/id_ed25519.pub"
  else
    for key in "${ssh_keys[@]}"; do
      if [[ ! -r "$key" ]]; then bad "SSH public key not found: $key" "Make one with: ssh-keygen -t ed25519"
      elif head -n 1 "$key" | grep -Eq '^(ssh-|ecdsa-|sk-)'; then ok "SSH public key: $key"
      elif head -n 1 "$key" | grep -q 'PRIVATE KEY'; then bad "$key is a private key" "Pass the public key, the file that ends in .pub"
      else bad "$key does not look like an SSH public key" "Pass the file that ends in .pub"; fi
    done
  fi
  plan_text=""
  if [[ "$have_python" == 1 ]]; then
    if plan_text="$(plan 2>&1)"; then ok "Manifest: $(grep -c . <<<"$plan_text") machines"
    else bad "The manifest cannot be built on KVM: $manifest" "$(tail -n 1 <<<"$plan_text")"; plan_text=""; fi
  fi
  for br in "$bridge_wan" "$bridge_oob" "$bridge_t1" "$bridge_t2" "$bridge_lan220"; do
    if [[ -d "/sys/class/net/$br" ]]; then ok "Bridge $br"; else bad "Bridge $br does not exist" "Create it before the build (Chapter 14)"; fi
  done
  if [[ -n "$plan_text" ]]; then
    need_mb="$(awk -F'|' '{ s += $3 } END { print s + 0 }' <<<"$plan_text")"
    need_gb="$(awk -F'|' '{ s += $4 } END { print s + 0 }' <<<"$plan_text")"
    avail_mb=$(( $(awk '/^MemAvailable:/ { print $2 }' /proc/meminfo) / 1024 ))
    if (( avail_mb >= need_mb )); then ok "Memory: the machines use $need_mb MB, and $avail_mb MB is available"
    else warn "Memory: the machines use $need_mb MB, and $avail_mb MB is available" "Leave machines out in the Lab Builder, or make them smaller"; fi
    probe="$disk_dir"; while [[ ! -d "$probe" && "$probe" != / ]]; do probe="$(dirname "$probe")"; done
    free_gb=$(( $(df -Pk "$probe" | awk 'NR == 2 { print $4 }') / 1024 / 1024 ))
    if (( free_gb >= need_gb )); then ok "Disk: $free_gb GB free under $probe. The thin disks can grow to $need_gb GB"
    else warn "Disk: $free_gb GB free under $probe, and the thin disks can grow to $need_gb GB" "Free some space, or pass --disk-dir with a folder on a larger disk"; fi
    exists=0
    while IFS='|' read -r name _ _ _ _ flv _; do
      if virsh dominfo "$name" >/dev/null 2>&1; then exists=$((exists + 1)); fi
      case "$flv" in
        rhel-10|rhel-10-stig)
          if [[ -z "$rhel_image" ]]; then bad "$flv needs --rhel-image" "Download the qcow2 file from the Red Hat Customer Portal"
          elif [[ ! -r "$rhel_image" ]]; then bad "The Red Hat image was not found: $rhel_image"; fi ;;
      esac
    done <<<"$plan_text"
    [[ "$exists" == 0 ]] || ok "$exists machine(s) of the lab already exist. A deploy skips them"
  fi
  if [[ "$failed" -gt 0 ]]; then echo "$failed problem(s) to fix before the build."; exit 1; fi
  echo "Ready. Run the preview next (--dry-run)."
  exit 0
fi

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
need virsh; need "$python"

case "$action" in
  status)
    deadline=$(( $(date +%s) + wait_minutes * 60 ))
    answers="$(mktemp -d)"
    trap 'rm -rf "$answers"' EXIT
    while :; do
      # Every machine is asked at the same time, because each answer takes a few seconds.
      count=0
      while IFS='|' read -r name _; do
        count=$((count + 1))
        (
          if ! virsh dominfo "$name" >/dev/null 2>&1; then printf '%-16s %-9s\n' "$name" missing
          else
            st="$(build_state "$name")" || st="unknown|the state could not be read"
            printf '%-16s %-9s %s\n' "$name" "${st%%|*}" "${st#*|}"
          fi
        ) > "$answers/$count" 2>/dev/null &
      done < <(plan)
      wait
      lines=() pending=0 failed=0
      for (( n = 1; n <= count; n++ )); do
        line="$(cat "$answers/$n" 2>/dev/null)"
        [[ -n "$line" ]] || line="(machine $n)        unknown   the state could not be read"
        case "$(awk '{ print $2 }' <<<"$line")" in running|starting) pending=1 ;; failed) failed=1 ;; esac
        lines+=("$line")
      done
      if [[ "$wait_for" == 0 || "$pending" == 0 || $(date +%s) -ge $deadline ]]; then break; fi
      echo "$(date +%T) Still building: $(printf '%s\n' "${lines[@]}" | awk '$2 == "running" || $2 == "starting" { printf "%s ", $1 }')"
      sleep 15
    done
    printf '%-16s %-9s %s\n' MACHINE BUILD DETAIL
    printf '%s\n' "${lines[@]}"
    if [[ "$failed" == 1 ]]; then echo "A machine reports a problem: its first boot failed, or a lab service is not running. Log in to it and run: lab201-status" >&2; exit 1; fi
    if [[ "$wait_for" == 1 && "$pending" == 1 ]]; then echo "Not every machine finished within $wait_minutes minutes." >&2; exit 1; fi
    if [[ "$wait_for" == 1 ]]; then
      # Say what the table shows and no more: a machine that cannot report or is off was not checked.
      n_ok=0 n_unknown=0 n_off=0
      read -r n_ok n_unknown n_off < <(printf '%s\n' "${lines[@]}" | awk '$2 == "ok" { o++ } $2 == "unknown" { u++ } $2 == "stopped" || $2 == "missing" { f++ } END { print o + 0, u + 0, f + 0 }') || true
      if (( count > 0 && n_ok == count )); then echo "Every machine has finished its first boot."
      elif (( n_ok > 0 )); then echo "Every machine that reports has finished its first boot ($n_ok of $count)."; fi
      if (( n_unknown > 0 )); then echo "$n_unknown machine(s) cannot report their state to this script (see the DETAIL column). Log in to each and run: lab201-status"; fi
      if (( n_off > 0 )); then echo "$n_off machine(s) were not checked, because they are stopped or missing (see the BUILD column)."; fi
      if (( n_ok + n_unknown == 0 )); then echo "No lab machine is running."; fi
    fi
    exit 0 ;;
  remove-build-nics)
    while IFS='|' read -r name _ _ _ _ _ nics; do
      virsh dominfo "$name" >/dev/null 2>&1 || continue
      mac="${nics%%;*}"; mac="${mac#*,}"
      echo "Removing the build NIC of $name"
      run virsh detach-interface "$name" bridge --mac "$mac" --live --config
    done < <(plan)
    exit 0 ;;
  snapshot)
    # A snapshot keeps the machine's NICs. With the build NIC (the first one) still there, a restore would bring
    # it back, and with it the machine's path to the internet. So the build NICs have to go first.
    with_build_nic=()
    while IFS='|' read -r name _ _ _ _ _ nics; do
      virsh dominfo "$name" >/dev/null 2>&1 || continue
      mac="${nics%%;*}"; mac="${mac#*,}"
      if { virsh domiflist "$name" 2>/dev/null || true; } | grep -qi -- "$mac"; then with_build_nic+=("$name"); fi
    done < <(plan)
    if [[ ${#with_build_nic[@]} -gt 0 ]]; then
      echo "These machines still have their build NIC: ${with_build_nic[*]}" >&2
      echo "A snapshot keeps that NIC, and a restore would bring it back with its path to the internet. Run --action remove-build-nics first. No snapshot was taken." >&2
      exit 1
    fi
    while IFS='|' read -r name _; do
      virsh dominfo "$name" >/dev/null 2>&1 || continue
      if has_snapshot "$name" "$snapshot_name"; then echo "$name has the snapshot $snapshot_name. Skipped."; continue; fi
      echo "Taking the snapshot $snapshot_name of $name"
      run virsh snapshot-create-as "$name" "$snapshot_name" --description "Lab 201 baseline (Lab 999.6)"
    done < <(plan)
    exit 0 ;;
  restore)
    # The gateway first, then the rest.
    skipped=0
    for pass in gateway others; do
      while IFS='|' read -r name _ _ _ role _; do
        if [[ "$pass" == gateway && "$role" != gateway ]]; then continue; fi
        if [[ "$pass" == others && "$role" == gateway ]]; then continue; fi
        virsh dominfo "$name" >/dev/null 2>&1 || continue
        if ! has_snapshot "$name" "$snapshot_name"; then echo "$name has no snapshot $snapshot_name. It is left as it is." >&2; skipped=1; continue; fi
        echo "Returning $name to the snapshot $snapshot_name"
        run virsh snapshot-revert "$name" "$snapshot_name" --running
      done < <(plan)
    done
    [[ "$skipped" == 0 ]] || { echo "Take the snapshot first: --action snapshot" >&2; exit 1; }
    exit 0 ;;
  remove)
    while IFS='|' read -r name _; do
      virsh dominfo "$name" >/dev/null 2>&1 || continue
      echo "Removing $name"
      run virsh destroy "$name" || true
      run virsh undefine "$name" --remove-all-storage --nvram --snapshots-metadata
    done < <(plan)
    exit 0 ;;
  deploy) ;;
  *) echo "Unknown action: $action" >&2; exit 2 ;;
esac

need virt-install; need qemu-img
[[ ${#ssh_keys[@]} -gt 0 ]] || { echo "--ssh-key is required for deploy." >&2; exit 2; }
for key in "${ssh_keys[@]}"; do [[ -r "$key" ]] || { echo "Cannot read $key" >&2; exit 2; }; done
if [[ "$dry_run" == 0 ]]; then
  for br in "$bridge_wan" "$bridge_oob" "$bridge_t1" "$bridge_t2" "$bridge_lan220"; do
    [[ -d "/sys/class/net/$br" ]] || { echo "Bridge $br does not exist." >&2; exit 1; }
  done
fi
run mkdir -p "$disk_dir" "$workdir"

# Images: one for each flavor in use, found, downloaded, and checked by resolve-image.py.
declare -A flavor_img
while IFS='|' read -r _ _ _ _ _ flv _; do
  [[ -z "${flavor_img[$flv]:-}" ]] || continue
  img_args=(--flavor "$flv" --out "$workdir/images")
  case "$flv" in
    rhel-10|rhel-10-stig)
      [[ -n "$rhel_image" ]] || { echo "$flv needs --rhel-image, the qcow2 file from the Red Hat Customer Portal." >&2; exit 2; }
      img_args+=(--image-path "$rhel_image") ;;
  esac
  if [[ "$dry_run" == 1 ]]; then
    run "$python" "$resolver" "${img_args[@]}"
    flavor_img[$flv]="$workdir/images/<image-for-$flv>"
  else
    flavor_img[$flv]="$("$python" "$resolver" "${img_args[@]}" | tail -n 1)"
  fi
done < <(plan)

# Seeds. VLAN tags are made inside the guests.
key_args=(); for key in "${ssh_keys[@]}"; do key_args+=(--ssh-key "$key"); done
seed_args=(--manifest "$manifest" --out "$workdir/seeds" --tagging guest --guest-agent qemu)
[[ -z "$license_file" ]] || seed_args+=(--license-file "$license_file")
run "$python" "$seedtool" "${seed_args[@]}" "${key_args[@]}"

create_vm() {
  local name="$1" cpu="$2" mem="$3" disk="$4" flv="$5" nics="$6" disk_path seed net_args=() pair net mac
  if virsh dominfo "$name" >/dev/null 2>&1; then echo "$name exists. Skipped."; return; fi
  echo "Creating $name"
  disk_path="$disk_dir/$name.qcow2"
  seed="$workdir/seeds/$name"
  # A disk cannot be smaller than the image under it, or the guest sees the image cut off. When the cloud image is
  # larger than the manifest's size (the Rocky Linux and AlmaLinux images are 10 GB), the disk keeps the size of the image.
  local image="${flavor_img[$flv]}" image_bytes size_arg=("${disk}G")
  image_bytes="$({ qemu-img info "$image" 2>/dev/null || true; } | sed -n 's/^virtual size:.*(\([0-9]*\) bytes).*/\1/p' | head -n 1)"
  if [[ -n "$image_bytes" ]] && (( image_bytes > disk * 1024 * 1024 * 1024 )); then
    echo "  $name: its image is larger than the $disk GB the manifest asks for. A disk cannot shrink, so it keeps the size of the image."
    size_arg=()
  fi
  run qemu-img create -f qcow2 -F qcow2 -b "$image" "$disk_path" ${size_arg[@]+"${size_arg[@]}"}
  IFS=';' read -ra pairs <<<"$nics"
  for pair in "${pairs[@]}"; do
    net="${pair%%,*}"; mac="${pair#*,}"
    net_args+=(--network "bridge=$(bridge_of "$net"),model=virtio,mac=$mac")
  done
  run virt-install --name "$name" --memory "$mem" --vcpus "$cpu" --cpu host-model --import \
    --disk "path=$disk_path,format=qcow2,bus=virtio" --os-variant generic \
    "${net_args[@]}" \
    --cloud-init "user-data=$seed/user-data,meta-data=$seed/meta-data,network-config=$seed/network-config" \
    --graphics none --noautoconsole
}

# The gateway first, then the rest. virt-install starts each machine as it creates it.
for pass in gateway others; do
  while IFS='|' read -r name cpu mem disk role flv nics; do
    if [[ "$pass" == gateway && "$role" != gateway ]]; then continue; fi
    if [[ "$pass" == others && "$role" == gateway ]]; then continue; fi
    create_vm "$name" "$cpu" "$mem" "$disk" "$flv" "$nics"
  done < <(plan)
done
echo "Started. To see when every machine has finished its first boot, run: $0 --action status --wait"
