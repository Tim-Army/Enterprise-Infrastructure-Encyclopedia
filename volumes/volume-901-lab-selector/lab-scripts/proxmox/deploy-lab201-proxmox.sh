#!/usr/bin/env bash
# Create the Volume CCI lab virtual machines on a Proxmox VE node.
#
# Run as root on the node (Proxmox VE 8.1 or later, because the script imports
# disks with "qm set ... import-from"). It reads ../common/lab201-vms.json,
# downloads and checks the cloud image for each Linux flavor the machines use
# (../common/resolve-image.py), renders a cloud-init seed for each machine with
# ../common/make-seed.py, and creates and starts the machines.
#
# Before you run it, create these Linux bridges in the node's network
# configuration (the script does not change the host network):
#   --bridge-t1   VLAN-aware, with the NIC that cables to sw-648f-1 as its port
#   --bridge-t2   VLAN-aware, with the NIC that cables to sw-2048f-1 as its port
#   --bridge-oob  with the NIC that cables to the switch management ports
#   --bridge-wan  the bridge that reaches the internet (often vmbr0)
#   --bridge-mcast  no ports (internal)
#
# A machine is known by its VM ID and its name together. When a VM ID holds a
# machine with another name, every action leaves it alone and says so.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
manifest="$here/../common/lab201-vms.json"
seedtool="$here/../common/make-seed.py"

action=deploy
storage=local-lvm
snip_storage=local
bridge_wan=vmbr0 bridge_oob=vmbr1 bridge_t1=vmbr2 bridge_t2=vmbr3 bridge_mcast=vmbr4
vmid_base=20100
workdir=/var/tmp/lab201
dry_run=0
ssh_keys=()
license_file=""
python="python3"
rhel_image=""
iso_storage=local
snapshot_name=baseline-201
wait_for=0
wait_minutes=30
declare -A iso_vol
declare -A iso_sum

usage() {
  cat <<EOF
Usage: $0 [options]
  --action ACTION        deploy (default), check, status, remove-build-nics, snapshot, restore, or remove
                           check     tests what a deploy needs on this node and changes nothing
                           status    shows each machine and whether its first boot has finished
                           snapshot  takes the baseline snapshot of every machine (Lab 999.6)
                           restore   returns every machine to the baseline snapshot and starts it
  --ssh-key FILE         public key for the admin user (repeatable; needed for deploy)
  --storage NAME         storage for disks and cloud-init drives (default $storage)
  --snippets-storage NAME  storage with the "snippets" content type (default $snip_storage)
  --bridge-wan|oob|t1|t2|mcast NAME   bridge for each lab network
  --vmid-base N          first VM ID; the first machine (the gateway in the default manifest) gets N+1 (default $vmid_base)
  --workdir DIR          download and render directory (default $workdir)
  --rhel-image FILE      the Red Hat Enterprise Linux 10 qcow2 image you downloaded (needed for rhel-10 flavors)
  --license-file FILE    JSON file with keys to apply (Red Hat, Ubuntu Pro, Proxmox subscription)
  --python CMD           Python 3 command to use (default python3), for example python3.15
  --iso FLAVOR=VOLUME    the install ISO for a Windows, Linux Mint, or Tiny Core flavor, as a Proxmox volume
                         (repeatable), for example win-2025=local:iso/Server2025.iso
  --iso-sum FLAVOR=HEX   the publisher's checksum of that ISO (repeatable). check and deploy stop when the
                         file does not match. SHA-256, SHA-512, SHA-1, or MD5, told apart by the length
  --iso-storage NAME     storage with the "iso" content type for the answer-file CDs (default $iso_storage)
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
    --storage) storage="$2"; shift 2 ;;
    --snippets-storage) snip_storage="$2"; shift 2 ;;
    --bridge-wan) bridge_wan="$2"; shift 2 ;;
    --bridge-oob) bridge_oob="$2"; shift 2 ;;
    --bridge-t1) bridge_t1="$2"; shift 2 ;;
    --bridge-t2) bridge_t2="$2"; shift 2 ;;
    --bridge-mcast) bridge_mcast="$2"; shift 2 ;;
    --vmid-base) vmid_base="$2"; shift 2 ;;
    --workdir) workdir="$2"; shift 2 ;;
    --rhel-image) rhel_image="$2"; shift 2 ;;
    --license-file) license_file="$2"; shift 2 ;;
    --python) python="$2"; shift 2 ;;
    --iso) iso_vol["${2%%=*}"]="${2#*=}"; shift 2 ;;
    --iso-sum) iso_sum["${2%%=*}"]="${2#*=}"; shift 2 ;;
    --iso-storage) iso_storage="$2"; shift 2 ;;
    --snapshot-name) snapshot_name="$2"; shift 2 ;;
    --wait) wait_for=1; shift ;;
    --wait-minutes) wait_minutes="$2"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ "$vmid_base" =~ ^[0-9]+$ ]] || { echo "--vmid-base must be a number." >&2; exit 2; }
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
    lab201-mcast) echo "$bridge_mcast" ;;
    *) echo "No bridge for network $1" >&2; return 1 ;;
  esac
}

# One line per VM and per NIC, in the order of the manifest.
plan() {
  "$python" - "$manifest" "$here/../common/flavors.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
fl = dict((f["id"], f) for f in json.load(open(sys.argv[2], encoding="utf-8"))["flavors"])
for i, vm in enumerate(m["vms"]):
    flavor = vm.get("flavor") or m.get("default_flavor") or "ubuntu-24.04"
    f = fl[flavor]
    print("VM|%s|%d|%d|%d|%d|%s|%s|%d|%s|%s|%s" % (vm["name"], i + 1, vm["vcpu"], vm["memory_mb"], vm["disk_gb"], vm.get("role", ""), flavor,
                                           1 if f.get("iso") else 0, f["family"], f.get("proxmox_ostype", "l26"), f.get("proxmox_cpu", "x86-64-v2-AES")))
    for n, nic in enumerate(vm["nics"]):
        mac = "%s:%02x:%02x" % (m["mac_prefix"], i + 1, n)
        print("NIC|%s|%d|%s|%s|%s|%s" % (vm["name"], n, nic["net"], nic.get("vlan", ""),
                                         "1" if nic.get("trunk") else "0", mac))
PY
}

# The machine whose first NIC stays as the uplink to the external firewall. The Lab Selector writes "uplink" into the
# manifest when the build keeps one. remove-build-nics and snapshot then leave that NIC alone.
uplink_vm() {
  "$python" -c 'import json, sys; print((json.load(open(sys.argv[1], encoding="utf-8")).get("uplink") or {}).get("vm", ""))' "$manifest"
}

vmid_of() { echo $(( vmid_base + $1 )); }

# The name of the machine that has a VM ID, or nothing when the ID is free.
vm_name_of() { { qm config "$1" 2>/dev/null || true; } | sed -n 's/^name: //p' | head -n 1; }

# 0 when the VM ID holds this lab machine, 1 when the ID is free, 2 (with a message) when another machine has it.
lab_vm() {
  local id="$1" name="$2" have
  qm status "$id" >/dev/null 2>&1 || return 1
  have="$(vm_name_of "$id")"
  [[ "$have" == "$name" ]] && return 0
  echo "VM ID $id is '$have', not the lab machine '$name'. It is left alone. Pass --vmid-base with a range the lab can use." >&2
  return 2
}

# The folder where a storage keeps its ISO images, or nothing when it holds none.
# Proxmox VE accepts an ISO volume name only when it ends in .iso or .img, so the probe has one.
iso_dir_of() {
  { pvesm path "$1:iso/lab201-probe.iso" 2>/dev/null || true; } | sed 's#/lab201-probe\.iso$##'
}

has_snapshot() {
  qm listsnapshot "$1" 2>/dev/null | awk -v s="$2" '{ for (i = 1; i <= NF; i++) if ($i == s) found = 1 } END { exit !found }'
}

# Check an install ISO against the checksum from its publisher. The length of the value names the algorithm.
check_iso_sum() {
  local flv="$1" vol="$2" want="${3,,}" path tool got
  path="$(pvesm path "$vol" 2>/dev/null)" || true
  [[ -n "$path" && -f "$path" ]] || { echo "The ISO for $flv was not found: $vol" >&2; return 1; }
  [[ "$want" =~ ^[0-9a-f]+$ ]] || { echo "--iso-sum $flv: the value has characters that are not hexadecimal." >&2; return 1; }
  case "${#want}" in
    32) tool=md5sum ;;
    40) tool=sha1sum ;;
    64) tool=sha256sum ;;
    128) tool=sha512sum ;;
    *) echo "--iso-sum $flv: ${#want} characters is not the length of an MD5, SHA-1, SHA-256, or SHA-512 checksum." >&2; return 1 ;;
  esac
  got="$("$tool" "$path" | awk '{ print $1 }')"
  [[ "$got" == "$want" ]] || { echo "Checksum mismatch for $vol: expected $want, got $got. Download the ISO again." >&2; return 1; }
  echo "The ${tool%sum} checksum of $vol matches."
  [[ "$tool" != md5sum ]] || echo "  MD5 shows a damaged download. It does not show a file that someone changed on purpose."
}

# The build state of one machine, as "STATE|detail". STATE is ok, running, failed, starting, stopped, manual, or unknown.
# A cloud-init machine answers through the QEMU guest agent, which runs /usr/local/sbin/lab201-status in it.
build_state() {
  local id="$1" isflag="$2" out line state
  if ! qm status "$id" 2>/dev/null | grep -q running; then echo "stopped|"; return; fi
  if [[ "$isflag" == 1 ]]; then echo "manual|installs from an ISO, so look at its console"; return; fi
  out="$(qm guest exec "$id" --timeout 20 -- /usr/local/sbin/lab201-status 2>&1)" || true
  line="$(printf '%s' "$out" | "$python" -c '
import json, sys
text = sys.stdin.read()
try:
    data = json.loads(text[text.index("{"):])
except ValueError:
    data = {}
lines = (data.get("out-data") or "").strip().splitlines()
print(lines[0] if lines else "")')" || line=""
  if [[ "$line" == lab201\ * ]]; then
    state="$(awk '{ print $2 }' <<<"$line")"
    echo "$state|$(cut -d' ' -f4- <<<"$line")"
    return
  fi
  case "$out" in
    *"No such file"*) echo "unknown|this machine was built before the status script existed" ;;
    *"has been disabled"*|*"not allowed"*|*"denied"*) echo "unknown|the guest agent of this flavor runs no commands. Log in and run: lab201-status" ;;
    *) echo "starting|the guest agent does not answer yet" ;;
  esac
}

if [[ "$action" == check ]]; then
  # Tests what a deploy needs on this node and changes nothing.
  failed=0
  ok() { printf '[OK]   %s\n' "$1"; }
  warn() { printf '[WARN] %s\n' "$1"; [[ -z "${2:-}" ]] || printf '       %s\n' "$2"; }
  bad() { printf '[FAIL] %s\n' "$1"; [[ -z "${2:-}" ]] || printf '       %s\n' "$2"; failed=$((failed + 1)); }
  echo "Checking this node for the lab build. Nothing is changed."
  tools=1
  for c in qm pvesm; do
    if command -v "$c" >/dev/null 2>&1; then ok "$c is installed"; else bad "$c was not found" "Run this script on a Proxmox VE node, as root"; tools=0; fi
  done
  if command -v pveversion >/dev/null 2>&1; then
    pve="$({ pveversion 2>/dev/null || true; } | sed -n 's#^pve-manager/\([0-9]*\.[0-9]*\).*#\1#p' | head -n 1)"
    if [[ -z "$pve" ]]; then warn "The Proxmox VE version could not be read"
    elif (( ${pve%%.*} > 8 || (${pve%%.*} == 8 && ${pve##*.} >= 1) )); then ok "Proxmox VE $pve"
    else bad "Proxmox VE $pve is older than 8.1" "The script imports disks with 'qm set ... import-from', which needs 8.1 or later"; fi
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
      if [[ ! -e "$key" && "$key" == *.pub ]]; then ok "SSH public key $key does not exist yet. The deploy makes it with ssh-keygen"
      elif [[ ! -r "$key" ]]; then bad "SSH public key not found: $key" "Pass a file name that ends in .pub, and the deploy makes the key"
      elif head -n 1 "$key" | grep -Eq '^(ssh-|ecdsa-|sk-)'; then ok "SSH public key: $key"
      elif head -n 1 "$key" | grep -q 'PRIVATE KEY'; then bad "$key is a private key" "Pass the public key, the file that ends in .pub"
      else bad "$key does not look like an SSH public key" "Pass the file that ends in .pub"; fi
    done
  fi
  plan_text=""
  if [[ "$have_python" == 1 ]]; then
    if plan_text="$(plan 2>&1)"; then ok "Manifest: $(grep -c '^VM|' <<<"$plan_text") machines"
    else bad "The manifest could not be read: $manifest" "$(tail -n 1 <<<"$plan_text")"; plan_text=""; fi
  fi
  if [[ "$tools" == 1 ]]; then
    stline="$({ pvesm status 2>/dev/null || true; } | awk -v s="$storage" '$1 == s')"
    if [[ -z "$stline" ]]; then bad "Storage $storage was not found" "Pass --storage with a storage that holds disk images (pvesm status lists them)"
    elif [[ "$(awk '{ print $3 }' <<<"$stline")" != active ]]; then bad "Storage $storage is not active"
    else
      free_gb=$(( $(awk '{ print $6 }' <<<"$stline") / 1024 / 1024 ))
      need_gb=0
      [[ -z "$plan_text" ]] || need_gb="$(awk -F'|' '$1 == "VM" { s += $6 } END { print s + 0 }' <<<"$plan_text")"
      if (( free_gb >= need_gb )); then ok "Storage $storage: $free_gb GB free. The thin disks can grow to $need_gb GB"
      else warn "Storage $storage: $free_gb GB free, and the thin disks can grow to $need_gb GB" "Free some space, or pass --storage with a larger storage"; fi
    fi
    if [[ -n "$(pvesm path "$snip_storage:snippets/probe" 2>/dev/null)" ]]; then ok "Storage $snip_storage holds snippets"
    else bad "Storage $snip_storage has no snippets content type" "Enable Snippets on it under Datacenter > Storage, or pass --snippets-storage"; fi
  fi
  for br in "$bridge_t1" "$bridge_t2"; do
    if [[ ! -d "/sys/class/net/$br" ]]; then bad "Bridge $br does not exist" "Create it in the node's network configuration"
    elif [[ "$(cat "/sys/class/net/$br/bridge/vlan_filtering" 2>/dev/null || echo 0)" != 1 ]]; then bad "Bridge $br is not VLAN-aware" "Add 'bridge-vlan-aware yes' to it in /etc/network/interfaces"
    else ok "Bridge $br (trunk, VLAN-aware)"; fi
  done
  for br in "$bridge_wan" "$bridge_oob" "$bridge_mcast"; do
    if [[ -d "/sys/class/net/$br" ]]; then ok "Bridge $br"; else bad "Bridge $br does not exist" "Create it in the node's network configuration"; fi
  done
  if [[ -n "$plan_text" ]]; then
    need_mb="$(awk -F'|' '$1 == "VM" { s += $5 } END { print s + 0 }' <<<"$plan_text")"
    avail_mb=$(( $(awk '/^MemAvailable:/ { print $2 }' /proc/meminfo) / 1024 ))
    if (( avail_mb >= need_mb )); then ok "Memory: the machines use $need_mb MB, and $avail_mb MB is available"
    else warn "Memory: the machines use $need_mb MB, and $avail_mb MB is available" "Leave machines out in the Lab Selector, or make them smaller"; fi
    exists=0 iso_used=0
    declare -A seen_flavor=()
    # One listing of the node's machines, to see which VM IDs are taken and by which name.
    declare -A id_name=()
    if [[ "$tools" == 1 ]]; then
      while read -r vid vname _; do
        if [[ "$vid" =~ ^[0-9]+$ ]]; then id_name[$vid]="$vname"; fi
      done < <(qm list 2>/dev/null || true)
    fi
    while IFS='|' read -r kind name idx _ _ _ _ flv isflag _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      have="${id_name[$id]:-}"
      if [[ -n "$have" ]]; then
        if [[ "$have" == "$name" ]]; then exists=$((exists + 1))
        else bad "VM ID $id is used by '$have', and the lab wants it for $name" "Pass --vmid-base with a range of free IDs"; fi
      fi
      [[ -z "${seen_flavor[$flv]:-}" ]] || continue
      seen_flavor[$flv]=1
      case "$flv" in
        rhel-10|rhel-10-stig)
          if [[ -z "$rhel_image" ]]; then bad "$flv needs --rhel-image" "Download the qcow2 file from the Red Hat Customer Portal"
          elif [[ -r "$rhel_image" ]]; then ok "Red Hat image: $rhel_image"
          else bad "The Red Hat image was not found: $rhel_image"; fi ;;
      esac
      if [[ "$isflag" == 1 ]]; then
        iso_used=1
        if [[ -z "${iso_vol[$flv]:-}" ]]; then bad "$flv installs from an ISO, and no --iso $flv=VOLUME was given" "For example: --iso $flv=local:iso/file.iso"
        elif [[ "$tools" != 1 ]]; then :
        elif [[ -n "${iso_sum[$flv]:-}" ]]; then
          if msg="$(check_iso_sum "$flv" "${iso_vol[$flv]}" "${iso_sum[$flv]}" 2>&1)"; then ok "$(head -n 1 <<<"$msg")"; else bad "$msg"; fi
        elif [[ -f "$(pvesm path "${iso_vol[$flv]}" 2>/dev/null)" ]]; then
          warn "The ISO for $flv is there, but it was not compared with a checksum: ${iso_vol[$flv]}" "Pass --iso-sum $flv=<the publisher's checksum>"
        else bad "The ISO for $flv was not found: ${iso_vol[$flv]}"; fi
      fi
    done <<<"$plan_text"
    [[ "$exists" == 0 ]] || ok "$exists machine(s) of the lab already exist. A deploy skips them"
    if [[ "$iso_used" == 1 ]]; then
      if "$python" -c 'import pycdlib' 2>/dev/null || command -v xorriso >/dev/null 2>&1 || command -v genisoimage >/dev/null 2>&1 || command -v mkisofs >/dev/null 2>&1; then
        ok "A tool that writes the answer-file CDs (pycdlib, xorriso, genisoimage, or mkisofs)"
      else bad "No tool writes the answer-file CDs" "Run: apt install xorriso"; fi
      if [[ "$tools" == 1 && -z "$(iso_dir_of "$iso_storage")" ]]; then bad "Storage $iso_storage has no iso content type" "Pass --iso-storage with a storage that holds ISO images"; fi
    fi
  fi
  if [[ "$failed" -gt 0 ]]; then echo "$failed problem(s) to fix before the build."; exit 1; fi
  echo "Ready. Run the preview next (--dry-run)."
  exit 0
fi

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
need qm; need pvesm; need "$python"

case "$action" in
  status)
    deadline=$(( $(date +%s) + wait_minutes * 60 ))
    answers="$(mktemp -d)"
    trap 'rm -rf "$answers"' EXIT
    while :; do
      # Every machine is asked at the same time, because each answer takes a few seconds.
      count=0
      while IFS='|' read -r kind name idx _ _ _ _ _ isflag _; do
        [[ "$kind" == VM ]] || continue
        id="$(vmid_of "$idx")"; count=$((count + 1))
        (
          if ! qm status "$id" >/dev/null 2>&1; then printf '%-16s %-6s %-9s\n' "$name" "$id" missing
          elif [[ "$(vm_name_of "$id")" != "$name" ]]; then printf '%-16s %-6s %-9s %s\n' "$name" "$id" other "this VM ID holds another machine"
          else
            st="$(build_state "$id" "$isflag")" || st="unknown|the state could not be read"
            printf '%-16s %-6s %-9s %s\n' "$name" "$id" "${st%%|*}" "${st#*|}"
          fi
        ) > "$answers/$count" 2>/dev/null &
      done < <(plan)
      wait
      lines=() pending=0 failed=0
      for (( n = 1; n <= count; n++ )); do
        line="$(cat "$answers/$n" 2>/dev/null)"
        [[ -n "$line" ]] || line="(machine $n)        -      unknown   the state could not be read"
        case "$(awk '{ print $3 }' <<<"$line")" in running|starting) pending=1 ;; failed) failed=1 ;; esac
        lines+=("$line")
      done
      if [[ "$wait_for" == 0 || "$pending" == 0 || $(date +%s) -ge $deadline ]]; then break; fi
      echo "$(date +%T) Still building: $(printf '%s\n' "${lines[@]}" | awk '$3 == "running" || $3 == "starting" { printf "%s ", $1 }')"
      sleep 15
    done
    printf '%-16s %-6s %-9s %s\n' MACHINE ID BUILD DETAIL
    printf '%s\n' "${lines[@]}"
    if [[ "$failed" == 1 ]]; then echo "A machine reports a problem: its first boot failed, or a lab service is not running. Log in to it and run: lab201-status" >&2; exit 1; fi
    if [[ "$wait_for" == 1 && "$pending" == 1 ]]; then echo "Not every machine finished within $wait_minutes minutes." >&2; exit 1; fi
    if [[ "$wait_for" == 1 ]]; then
      # Say what the table shows and no more: a machine that cannot report, installs by hand, or is off was not checked.
      n_ok=0 n_unknown=0 n_manual=0 n_off=0
      read -r n_ok n_unknown n_manual n_off < <(printf '%s\n' "${lines[@]}" | awk '$3 == "ok" { o++ } $3 == "unknown" { u++ } $3 == "manual" { m++ } $3 == "stopped" || $3 == "missing" || $3 == "other" { f++ } END { print o + 0, u + 0, m + 0, f + 0 }') || true
      if (( count > 0 && n_ok == count )); then echo "Every machine has finished its first boot."
      elif (( n_ok > 0 )); then echo "Every machine that reports has finished its first boot ($n_ok of $count)."; fi
      if (( n_unknown > 0 )); then echo "$n_unknown machine(s) cannot report their state to this script (see the DETAIL column). Log in to each and run: lab201-status"; fi
      if (( n_manual > 0 )); then echo "$n_manual machine(s) install from an ISO, so this script cannot follow them. Look at the console of each."; fi
      if (( n_off > 0 )); then echo "$n_off machine(s) were not checked, because they are stopped or missing, or their VM ID holds another machine (see the BUILD column)."; fi
      if (( n_ok + n_unknown + n_manual == 0 )); then echo "No lab machine is running at these VM IDs. Is --vmid-base the one the lab was built with?"; fi
    fi
    exit 0 ;;
  remove-build-nics)
    keep="$(uplink_vm)"
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      if [[ -n "$keep" && "$name" == "$keep" ]]; then echo "$name keeps its first NIC: it is the uplink to the external firewall."; continue; fi
      id="$(vmid_of "$idx")"
      lab_vm "$id" "$name" || continue
      echo "Removing the build NIC of $name"
      run qm set "$id" --delete net0
    done < <(plan)
    exit 0 ;;
  snapshot)
    # A snapshot keeps the machine's NICs. With the build NIC (net0) still there, a restore would bring it back,
    # and with it the machine's path to the internet. So the build NICs have to go first.
    with_build_nic=()
    keep="$(uplink_vm)"
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      # The first NIC of the uplink machine is its uplink to the external firewall, and it stays.
      if [[ -n "$keep" && "$name" == "$keep" ]]; then continue; fi
      id="$(vmid_of "$idx")"
      lab_vm "$id" "$name" 2>/dev/null || continue
      if { qm config "$id" 2>/dev/null || true; } | grep -q '^net0:'; then with_build_nic+=("$name"); fi
    done < <(plan)
    if [[ ${#with_build_nic[@]} -gt 0 ]]; then
      echo "These machines still have their build NIC: ${with_build_nic[*]}" >&2
      echo "A snapshot keeps that NIC, and a restore would bring it back with its path to the internet. Run --action remove-build-nics first. No snapshot was taken." >&2
      exit 1
    fi
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      lab_vm "$id" "$name" || continue
      if has_snapshot "$id" "$snapshot_name"; then echo "$name has the snapshot $snapshot_name. Skipped."; continue; fi
      echo "Taking the snapshot $snapshot_name of $name"
      run qm snapshot "$id" "$snapshot_name" --description "Lab 201 baseline (Lab 999.6)"
    done < <(plan)
    exit 0 ;;
  restore)
    # Roll every machine back, then start the gateway first and the rest after it.
    gateway_id="" ids=() skipped=0
    while IFS='|' read -r kind name idx _ _ _ role _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      lab_vm "$id" "$name" || continue
      if ! has_snapshot "$id" "$snapshot_name"; then echo "$name has no snapshot $snapshot_name. It is left as it is." >&2; skipped=1; continue; fi
      echo "Returning $name to the snapshot $snapshot_name"
      run qm rollback "$id" "$snapshot_name"
      if [[ "$role" == gateway ]]; then gateway_id="$id"; else ids+=("$id"); fi
    done < <(plan)
    for id in $gateway_id ${ids[@]+"${ids[@]}"}; do
      if qm status "$id" 2>/dev/null | grep -q running; then continue; fi
      run qm start "$id"
    done
    [[ "$skipped" == 0 ]] || { echo "Take the snapshot first: --action snapshot" >&2; exit 1; }
    exit 0 ;;
  remove)
    snip_dir="$(pvesm path "$snip_storage:snippets/probe" 2>/dev/null | sed 's#/probe$##')" || true
    iso_dir="$(iso_dir_of "$iso_storage")"
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      rc=0; lab_vm "$id" "$name" || rc=$?
      [[ "$rc" != 2 ]] || continue
      if [[ "$rc" == 0 ]]; then
        echo "Destroying $name ($id)"
        run qm stop "$id" --skiplock 1 || true
        run qm destroy "$id" --purge 1
      fi
      # The files the deploy left behind: the cloud-init snippets and the ISO flavors' answer CD.
      if [[ -n "${snip_dir:-}" ]]; then
        for f in user network meta; do run rm -f "$snip_dir/lab201-$name-$f.yml"; done
      fi
      if [[ -n "${iso_dir:-}" ]]; then run rm -f "$iso_dir/lab201-$name-seed.iso"; fi
    done < <(plan)
    exit 0 ;;
  deploy) ;;
  *) echo "Unknown action: $action" >&2; exit 2 ;;
esac

[[ ${#ssh_keys[@]} -gt 0 ]] || { echo "--ssh-key is required for deploy." >&2; exit 2; }
# A missing key that ends in .pub is made by make-seed.py --make-keys, with its folder.
for key in "${ssh_keys[@]}"; do [[ -r "$key" || ( ! -e "$key" && "$key" == *.pub ) ]] || { echo "Cannot read $key" >&2; exit 2; }; done

# The VLAN-aware bridges must exist, or the VLAN tags are ignored.
for br in "$bridge_t1" "$bridge_t2"; do
  [[ -d "/sys/class/net/$br" ]] || { echo "Bridge $br does not exist." >&2; exit 1; }
  [[ "$(cat "/sys/class/net/$br/bridge/vlan_filtering" 2>/dev/null || echo 0)" == 1 ]] ||
    { echo "Bridge $br is not VLAN-aware. Add 'bridge-vlan-aware yes' to it in /etc/network/interfaces." >&2; exit 1; }
done
for br in "$bridge_wan" "$bridge_oob" "$bridge_mcast"; do
  [[ -d "/sys/class/net/$br" ]] || { echo "Bridge $br does not exist." >&2; exit 1; }
done
snip_dir="$(pvesm path "$snip_storage:snippets/probe" 2>/dev/null | sed 's#/probe$##')" || true
[[ -n "${snip_dir:-}" ]] || { echo "Storage $snip_storage has no snippets content type. Enable it under Datacenter > Storage." >&2; exit 1; }

# A VM ID that another machine holds stops the deploy before anything is made.
while IFS='|' read -r kind name idx _; do
  [[ "$kind" == VM ]] || continue
  rc=0; lab_vm "$(vmid_of "$idx")" "$name" || rc=$?
  [[ "$rc" != 2 ]] || exit 1
done < <(plan)
run mkdir -p "$snip_dir" "$workdir"

# Images: one for each flavor in use. resolve-image.py finds the newest file, downloads it,
# and checks it against the publisher's checksum. Hardened flavors use their base flavor's image.
# An install ISO you supply is checked against --iso-sum when you give one.
resolver="$here/../common/resolve-image.py"
declare -A flavor_img
declare -A iso_checked
any_iso=0
while IFS='|' read -r kind _ _ _ _ _ _ flv isflag _; do
  [[ "$kind" == VM ]] || continue
  if [[ "$isflag" == 1 ]]; then
    any_iso=1
    [[ -n "${iso_vol[$flv]:-}" ]] || { echo "$flv installs from an ISO. Pass --iso $flv=<volume>, for example $flv=local:iso/file.iso." >&2; exit 2; }
    if [[ -n "${iso_sum[$flv]:-}" && -z "${iso_checked[$flv]:-}" ]]; then
      check_iso_sum "$flv" "${iso_vol[$flv]}" "${iso_sum[$flv]}" || exit 1
      iso_checked[$flv]=1
    fi
    continue
  fi
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

# A Proxmox subscription key, if the license file has one. It is not printed.
if [[ -n "$license_file" && "$dry_run" == 0 ]]; then
  pve_key="$("$python" -c "import json,sys;print((json.load(open(sys.argv[1])).get('proxmox') or {}).get('subscription_key',''))" "$license_file")"
  if [[ -n "$pve_key" ]]; then pvesubscription set "$pve_key" >/dev/null || echo "Could not set the Proxmox subscription key." >&2; fi
fi

# Seeds.
key_args=(--make-keys); for key in "${ssh_keys[@]}"; do key_args+=(--ssh-key "$key"); done
seed_args=(--manifest "$manifest" --out "$workdir/seeds" --tagging hypervisor --guest-agent qemu)
iso_dir=""
if [[ "$any_iso" == 1 ]]; then
  seed_args+=(--iso)
  iso_dir="$(iso_dir_of "$iso_storage")"
  [[ -n "$iso_dir" ]] || { echo "Storage $iso_storage has no iso content type." >&2; exit 1; }
fi
[[ -z "$license_file" ]] || seed_args+=(--license-file "$license_file")
run "$python" "$seedtool" "${seed_args[@]}" "${key_args[@]}"

# Machines.
declare -A vm_cpu vm_mem vm_disk vm_idx vm_flavor vm_iso vm_family vm_ostype vm_cputype
nic_args=()
current=""
create_iso_vm() {
  # A machine that installs from an ISO: an empty disk, the install ISO, and a CD with the answer file or first-login script.
  local name="$1" id="$2" flv disk_opt boot
  flv="${vm_flavor[$name]}"
  echo "Creating $name ($id) from an ISO"
  if [[ "${vm_family[$name]}" == windows ]]; then disk_opt=(--sata0 "$storage:${vm_disk[$name]}"); boot="order=sata0;ide2"
  else disk_opt=(--scsi0 "$storage:${vm_disk[$name]}"); boot="order=scsi0;ide2"; fi
  run cp "$workdir/seeds/$name-seed.iso" "$iso_dir/lab201-$name-seed.iso"
  run qm create "$id" --name "$name" --memory "${vm_mem[$name]}" --cores "${vm_cpu[$name]}" --cpu "${vm_cputype[$name]}" \
    --ostype "${vm_ostype[$name]}" --scsihw virtio-scsi-single "${nic_args[@]}" "${disk_opt[@]}"
  run qm set "$id" --ide2 "${iso_vol[$flv]},media=cdrom" --ide3 "$iso_storage:iso/lab201-$name-seed.iso,media=cdrom" --boot "$boot"
  case "${vm_family[$name]}" in
    mint) echo "  $name: run the Linux Mint installer on its console, then run lab201-firstlogin.sh from the second CD as root." ;;
    tce) echo "  $name: boot Tiny Core, mount the second CD, and run: sh lab201-tc.sh" ;;
    windows) echo "  $name: Windows installs unattended and reboots. Remove both CDs when it has finished." ;;
  esac
}

# Grow a machine's first disk to the size the manifest asks for. A disk cannot shrink, so when the cloud image
# is already larger (the Rocky Linux and AlmaLinux images are 10 GB), the disk keeps the size of the image.
grow_disk() {
  local id="$1" want_gb="$2" name="$3" have="" unit="" have_mb
  if [[ "$dry_run" == 1 ]]; then run qm resize "$id" scsi0 "${want_gb}G"; return; fi
  read -r have unit < <({ qm config "$id" 2>/dev/null || true; } | sed -n 's/^scsi0:.*size=\([0-9.]*\)\([KMGT]\).*/\1 \2/p') || true
  if [[ -z "$have" ]]; then qm resize "$id" scsi0 "${want_gb}G"; return; fi
  have_mb="$(awk -v n="$have" -v u="$unit" 'BEGIN { m = (u == "K") ? n / 1024 : (u == "M") ? n : (u == "G") ? n * 1024 : n * 1048576; printf "%d", m }')"
  if (( want_gb * 1024 > have_mb )); then qm resize "$id" scsi0 "${want_gb}G"
  elif (( want_gb * 1024 < have_mb )); then
    echo "  $name: its image is $have$unit, larger than the $want_gb GB the manifest asks for. A disk cannot shrink, so it stays $have$unit."
  fi
}

create_vm() {
  local name="$1" id
  id="$(vmid_of "${vm_idx[$name]}")"
  if qm status "$id" >/dev/null 2>&1; then echo "$name ($id) exists. Skipped."; return; fi
  if [[ "${vm_iso[$name]}" == 1 ]]; then create_iso_vm "$name" "$id"; return; fi
  echo "Creating $name ($id)"
  local f src
  for f in user network meta; do
    case "$f" in
      user) src="$workdir/seeds/$name/user-data" ;;
      network) src="$workdir/seeds/$name/network-config" ;;
      meta) src="$workdir/seeds/$name/meta-data" ;;
    esac
    run cp "$src" "$snip_dir/lab201-$name-$f.yml"
  done
  run qm create "$id" --name "$name" --memory "${vm_mem[$name]}" --cores "${vm_cpu[$name]}" --cpu "${vm_cputype[$name]}" \
    --ostype l26 --scsihw virtio-scsi-single --agent enabled=1 --serial0 socket --vga serial0 "${nic_args[@]}"
  run qm set "$id" --scsi0 "$storage:0,import-from=${flavor_img[${vm_flavor[$name]}]},discard=on"
  grow_disk "$id" "${vm_disk[$name]}" "$name"
  run qm set "$id" --ide2 "$storage:cloudinit" --boot order=scsi0 \
    --cicustom "user=$snip_storage:snippets/lab201-$name-user.yml,network=$snip_storage:snippets/lab201-$name-network.yml,meta=$snip_storage:snippets/lab201-$name-meta.yml"
}

gateway_name=""
nic_model=virtio
while IFS='|' read -r kind a b c d e f g h i j k; do
  if [[ "$kind" == VM ]]; then
    [[ -z "$current" ]] || create_vm "$current"
    current="$a"; vm_idx[$a]="$b"; vm_cpu[$a]="$c"; vm_mem[$a]="$d"; vm_disk[$a]="$e"; vm_flavor[$a]="$g"; vm_iso[$a]="$h"; vm_family[$a]="$i"; vm_ostype[$a]="$j"; vm_cputype[$a]="$k"; nic_args=()
    nic_model=virtio; [[ "$i" != windows ]] || nic_model=e1000e
    [[ "$f" != gateway ]] || gateway_name="$a"
  else
    # NIC|name|index|net|vlan|trunk|mac
    br="$(bridge_of "$c")"
    opt="$nic_model=$f,bridge=$br,firewall=0"
    [[ -z "$d" ]] || opt="$opt,tag=$d"
    [[ "$e" != 1 ]] || opt="$opt,trunks=2-4094"
    nic_args+=("--net$b" "$opt")
  fi
done < <(plan)
[[ -z "$current" ]] || create_vm "$current"

# Start the gateway first, then the rest.
order=()
[[ -z "$gateway_name" ]] || order+=("$gateway_name")
for name in "${!vm_idx[@]}"; do [[ "$name" == "$gateway_name" ]] || order+=("$name"); done
for name in "${order[@]}"; do
  id="$(vmid_of "${vm_idx[$name]}")"
  if qm status "$id" 2>/dev/null | grep -q running; then continue; fi
  run qm start "$id"
done
echo "Started. To see when every machine has finished its first boot, run: $0 --action status --wait --vmid-base $vmid_base"
