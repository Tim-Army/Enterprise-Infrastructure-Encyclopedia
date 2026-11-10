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
rhel_image=""

usage() {
  cat <<EOF
Usage: $0 [options]
  --action ACTION        deploy (default), status, remove-build-nics, or remove
  --ssh-key FILE         public key for the admin user (repeatable; needed for deploy)
  --bridge-wan|oob|t1|t2|lan220 NAME   bridge for each lab network
  --disk-dir DIR         where the machine disks go (default $disk_dir)
  --workdir DIR          download and render directory (default $workdir)
  --rhel-image FILE      the Red Hat Enterprise Linux 10 qcow2 image you downloaded (for rhel-10 flavors)
  --license-file FILE    JSON file with keys to apply (Red Hat, Ubuntu Pro)
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
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

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
  python3 - "$manifest" "$here/../common/flavors.json" <<'PY'
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

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
need virsh; need python3

case "$action" in
  status)
    while IFS='|' read -r name _; do
      printf '%-16s ' "$name"
      virsh domstate "$name" 2>/dev/null || echo "missing"
    done < <(plan)
    exit 0 ;;
  remove-build-nics)
    while IFS='|' read -r name _ _ _ _ _ nics; do
      virsh dominfo "$name" >/dev/null 2>&1 || continue
      mac="${nics%%;*}"; mac="${mac#*,}"
      echo "Removing the build NIC of $name"
      run virsh detach-interface "$name" bridge --mac "$mac" --live --config
    done < <(plan)
    exit 0 ;;
  remove)
    while IFS='|' read -r name _; do
      virsh dominfo "$name" >/dev/null 2>&1 || continue
      echo "Removing $name"
      run virsh destroy "$name" || true
      run virsh undefine "$name" --remove-all-storage --nvram
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
    run python3 "$resolver" "${img_args[@]}"
    flavor_img[$flv]="$workdir/images/<image-for-$flv>"
  else
    flavor_img[$flv]="$(python3 "$resolver" "${img_args[@]}" | tail -n 1)"
  fi
done < <(plan)

# Seeds. VLAN tags are made inside the guests.
key_args=(); for key in "${ssh_keys[@]}"; do key_args+=(--ssh-key "$key"); done
seed_args=(--manifest "$manifest" --out "$workdir/seeds" --tagging guest --guest-agent qemu)
[[ -z "$license_file" ]] || seed_args+=(--license-file "$license_file")
run python3 "$seedtool" "${seed_args[@]}" "${key_args[@]}"

create_vm() {
  local name="$1" cpu="$2" mem="$3" disk="$4" flv="$5" nics="$6" disk_path seed net_args=() pair net mac
  if virsh dominfo "$name" >/dev/null 2>&1; then echo "$name exists. Skipped."; return; fi
  echo "Creating $name"
  disk_path="$disk_dir/$name.qcow2"
  seed="$workdir/seeds/$name"
  run qemu-img create -f qcow2 -F qcow2 -b "${flavor_img[$flv]}" "$disk_path" "${disk}G"
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
