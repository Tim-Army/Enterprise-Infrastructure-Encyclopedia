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
#   --bridge-lan220  no ports (internal)
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
manifest="$here/../common/lab201-vms.json"
seedtool="$here/../common/make-seed.py"

action=deploy
storage=local-lvm
snip_storage=local
bridge_wan=vmbr0 bridge_oob=vmbr1 bridge_t1=vmbr2 bridge_t2=vmbr3 bridge_lan220=vmbr4
vmid_base=20100
workdir=/var/tmp/lab201
dry_run=0
ssh_keys=()
license_file=""
rhel_image=""
iso_storage=local
declare -A iso_vol

usage() {
  cat <<EOF
Usage: $0 [options]
  --action ACTION        deploy (default), status, remove-build-nics, or remove
  --ssh-key FILE         public key for the admin user (repeatable; needed for deploy)
  --storage NAME         storage for disks and cloud-init drives (default $storage)
  --snippets-storage NAME  storage with the "snippets" content type (default $snip_storage)
  --bridge-wan|oob|t1|t2|lan220 NAME   bridge for each lab network
  --vmid-base N          first VM ID; the first machine (the gateway in the default manifest) gets N+1 (default $vmid_base)
  --workdir DIR          download and render directory (default $workdir)
  --rhel-image FILE      the Red Hat Enterprise Linux 10 qcow2 image you downloaded (needed for rhel-10 flavors)
  --license-file FILE    JSON file with keys to apply (Red Hat, Ubuntu Pro, Proxmox subscription)
  --iso FLAVOR=VOLUME    the install ISO for a Windows, Linux Mint, or Tiny Core flavor, as a Proxmox volume
                         (repeatable), for example win-2025=local:iso/Server2025.iso
  --iso-storage NAME     storage with the "iso" content type for the answer-file CDs (default $iso_storage)
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
    --bridge-lan220) bridge_lan220="$2"; shift 2 ;;
    --vmid-base) vmid_base="$2"; shift 2 ;;
    --workdir) workdir="$2"; shift 2 ;;
    --rhel-image) rhel_image="$2"; shift 2 ;;
    --license-file) license_file="$2"; shift 2 ;;
    --iso) iso_vol["${2%%=*}"]="${2#*=}"; shift 2 ;;
    --iso-storage) iso_storage="$2"; shift 2 ;;
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

# One line per VM and per NIC, in the order of the manifest.
plan() {
  python3 - "$manifest" "$here/../common/flavors.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
fl = dict((f["id"], f) for f in json.load(open(sys.argv[2], encoding="utf-8"))["flavors"])
for i, vm in enumerate(m["vms"]):
    flavor = vm.get("flavor") or m.get("default_flavor") or "ubuntu-24.04"
    f = fl[flavor]
    print("VM|%s|%d|%d|%d|%d|%s|%s|%d|%s|%s" % (vm["name"], i + 1, vm["vcpu"], vm["memory_mb"], vm["disk_gb"], vm.get("role", ""), flavor,
                                           1 if f.get("iso") else 0, f["family"], f.get("proxmox_ostype", "l26")))
    for n, nic in enumerate(vm["nics"]):
        mac = "%s:%02x:%02x" % (m["mac_prefix"], i + 1, n)
        print("NIC|%s|%d|%s|%s|%s|%s" % (vm["name"], n, nic["net"], nic.get("vlan", ""),
                                         "1" if nic.get("trunk") else "0", mac))
PY
}

vmid_of() { echo $(( vmid_base + $1 )); }

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
need qm; need pvesm; need python3

case "$action" in
  status)
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      printf '%-16s %s  ' "$name" "$id"
      qm status "$id" 2>/dev/null || echo "missing"
    done < <(plan)
    exit 0 ;;
  remove-build-nics)
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      qm status "$id" >/dev/null 2>&1 || continue
      echo "Removing the build NIC of $name"
      run qm set "$id" --delete net0
    done < <(plan)
    exit 0 ;;
  remove)
    while IFS='|' read -r kind name idx _; do
      [[ "$kind" == VM ]] || continue
      id="$(vmid_of "$idx")"
      qm status "$id" >/dev/null 2>&1 || continue
      echo "Destroying $name ($id)"
      run qm stop "$id" --skiplock 1 || true
      run qm destroy "$id" --purge 1
    done < <(plan)
    exit 0 ;;
  deploy) ;;
  *) echo "Unknown action: $action" >&2; exit 2 ;;
esac

[[ ${#ssh_keys[@]} -gt 0 ]] || { echo "--ssh-key is required for deploy." >&2; exit 2; }
for key in "${ssh_keys[@]}"; do [[ -r "$key" ]] || { echo "Cannot read $key" >&2; exit 2; }; done

# The VLAN-aware bridges must exist, or the VLAN tags are ignored.
for br in "$bridge_t1" "$bridge_t2"; do
  [[ -d "/sys/class/net/$br" ]] || { echo "Bridge $br does not exist." >&2; exit 1; }
  [[ "$(cat "/sys/class/net/$br/bridge/vlan_filtering" 2>/dev/null || echo 0)" == 1 ]] ||
    { echo "Bridge $br is not VLAN-aware. Add 'bridge-vlan-aware yes' to it in /etc/network/interfaces." >&2; exit 1; }
done
for br in "$bridge_wan" "$bridge_oob" "$bridge_lan220"; do
  [[ -d "/sys/class/net/$br" ]] || { echo "Bridge $br does not exist." >&2; exit 1; }
done
snip_dir="$(pvesm path "$snip_storage:snippets/probe" 2>/dev/null | sed 's#/probe$##')" || true
[[ -n "${snip_dir:-}" ]] || { echo "Storage $snip_storage has no snippets content type. Enable it under Datacenter > Storage." >&2; exit 1; }
run mkdir -p "$snip_dir" "$workdir"

# Images: one for each flavor in use. resolve-image.py finds the newest file, downloads it,
# and checks it against the publisher's checksum. Hardened flavors use their base flavor's image.
resolver="$here/../common/resolve-image.py"
declare -A flavor_img
any_iso=0
while IFS='|' read -r kind _ _ _ _ _ _ flv isflag _; do
  [[ "$kind" == VM ]] || continue
  if [[ "$isflag" == 1 ]]; then
    any_iso=1
    [[ -n "${iso_vol[$flv]:-}" ]] || { echo "$flv installs from an ISO. Pass --iso $flv=<volume>, for example $flv=local:iso/file.iso." >&2; exit 2; }
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
    run python3 "$resolver" "${img_args[@]}"
    flavor_img[$flv]="$workdir/images/<image-for-$flv>"
  else
    flavor_img[$flv]="$(python3 "$resolver" "${img_args[@]}" | tail -n 1)"
  fi
done < <(plan)

# A Proxmox subscription key, if the license file has one. It is not printed.
if [[ -n "$license_file" && "$dry_run" == 0 ]]; then
  pve_key="$(python3 -c "import json,sys;print((json.load(open(sys.argv[1])).get('proxmox') or {}).get('subscription_key',''))" "$license_file")"
  if [[ -n "$pve_key" ]]; then pvesubscription set "$pve_key" >/dev/null || echo "Could not set the Proxmox subscription key." >&2; fi
fi

# Seeds.
key_args=(); for key in "${ssh_keys[@]}"; do key_args+=(--ssh-key "$key"); done
seed_args=(--manifest "$manifest" --out "$workdir/seeds" --tagging hypervisor --guest-agent qemu)
iso_dir=""
if [[ "$any_iso" == 1 ]]; then
  seed_args+=(--iso)
  iso_dir="$(pvesm path "$iso_storage:iso/probe" 2>/dev/null | sed 's#/probe$##')" || true
  [[ -n "$iso_dir" ]] || { echo "Storage $iso_storage has no iso content type." >&2; exit 1; }
fi
[[ -z "$license_file" ]] || seed_args+=(--license-file "$license_file")
run python3 "$seedtool" "${seed_args[@]}" "${key_args[@]}"

# Machines.
declare -A vm_cpu vm_mem vm_disk vm_idx vm_flavor vm_iso vm_family vm_ostype
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
  run qm create "$id" --name "$name" --memory "${vm_mem[$name]}" --cores "${vm_cpu[$name]}" --cpu x86-64-v2-AES \
    --ostype "${vm_ostype[$name]}" --scsihw virtio-scsi-single "${nic_args[@]}" "${disk_opt[@]}"
  run qm set "$id" --ide2 "${iso_vol[$flv]},media=cdrom" --ide3 "$iso_storage:iso/lab201-$name-seed.iso,media=cdrom" --boot "$boot"
  case "${vm_family[$name]}" in
    mint) echo "  $name: run the Linux Mint installer on its console, then run lab201-firstlogin.sh from the second CD as root." ;;
    tce) echo "  $name: boot Tiny Core, mount the second CD, and run: sh lab201-tc.sh" ;;
    windows) echo "  $name: Windows installs unattended and reboots. Remove both CDs when it has finished." ;;
  esac
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
  run qm create "$id" --name "$name" --memory "${vm_mem[$name]}" --cores "${vm_cpu[$name]}" --cpu x86-64-v2-AES \
    --ostype l26 --scsihw virtio-scsi-single --agent enabled=1 --serial0 socket --vga serial0 "${nic_args[@]}"
  run qm set "$id" --scsi0 "$storage:0,import-from=${flavor_img[${vm_flavor[$name]}]},discard=on"
  run qm resize "$id" scsi0 "${vm_disk[$name]}G"
  run qm set "$id" --ide2 "$storage:cloudinit" --boot order=scsi0 \
    --cicustom "user=$snip_storage:snippets/lab201-$name-user.yml,network=$snip_storage:snippets/lab201-$name-network.yml,meta=$snip_storage:snippets/lab201-$name-meta.yml"
}

gateway_name=""
nic_model=virtio
while IFS='|' read -r kind a b c d e f g h i j; do
  if [[ "$kind" == VM ]]; then
    [[ -z "$current" ]] || create_vm "$current"
    current="$a"; vm_idx[$a]="$b"; vm_cpu[$a]="$c"; vm_mem[$a]="$d"; vm_disk[$a]="$e"; vm_flavor[$a]="$g"; vm_iso[$a]="$h"; vm_family[$a]="$i"; vm_ostype[$a]="$j"; nic_args=()
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
