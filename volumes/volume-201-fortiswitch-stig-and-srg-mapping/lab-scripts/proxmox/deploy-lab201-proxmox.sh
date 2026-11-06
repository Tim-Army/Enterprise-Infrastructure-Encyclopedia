#!/usr/bin/env bash
# Create the Volume CCI lab virtual machines on a Proxmox VE node.
#
# Run as root on the node (Proxmox VE 8.1 or later, because the script imports
# disks with "qm set ... import-from"). It reads ../common/lab201-vms.json,
# downloads and checks the Ubuntu cloud image, renders a cloud-init seed for each
# machine with ../common/make-seed.py, and creates and starts the machines.
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
  python3 - "$manifest" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
for i, vm in enumerate(m["vms"]):
    print("VM|%s|%d|%d|%d|%d|%s" % (vm["name"], i + 1, vm["vcpu"], vm["memory_mb"], vm["disk_gb"], vm.get("role", "")))
    for n, nic in enumerate(vm["nics"]):
        mac = "%s:%02x:%02x" % (m["mac_prefix"], i + 1, n)
        print("NIC|%s|%d|%s|%s|%s|%s" % (vm["name"], n, nic["net"], nic.get("vlan", ""),
                                         "1" if nic.get("trunk") else "0", mac))
PY
}

vmid_of() { echo $(( vmid_base + $1 )); }

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
need qm; need pvesm; need python3; need curl; need sha256sum

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

# Image: download and check the SHA-256 sum.
img_name="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['image']['img'])" "$manifest")"
base_url="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['image']['base_url'])" "$manifest")"
img="$workdir/$img_name"
if [[ ! -f "$img" ]]; then
  run curl -fL -o "$img" "$base_url$img_name"
  if [[ "$dry_run" == 0 ]]; then
    want="$(curl -fsSL "${base_url}SHA256SUMS" | awk -v f="*$img_name" '$2 == f {print $1}')"
    got="$(sha256sum "$img" | awk '{print $1}')"
    [[ -n "$want" && "$want" == "$got" ]] || { rm -f "$img"; echo "SHA-256 mismatch for $img_name." >&2; exit 1; }
  fi
fi

# Seeds.
key_args=(); for key in "${ssh_keys[@]}"; do key_args+=(--ssh-key "$key"); done
run python3 "$seedtool" --manifest "$manifest" --out "$workdir/seeds" --tagging hypervisor --guest-agent qemu "${key_args[@]}"

# Machines.
declare -A vm_cpu vm_mem vm_disk vm_idx
nic_args=()
current=""
create_vm() {
  local name="$1" id
  id="$(vmid_of "${vm_idx[$name]}")"
  if qm status "$id" >/dev/null 2>&1; then echo "$name ($id) exists. Skipped."; return; fi
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
  run qm set "$id" --scsi0 "$storage:0,import-from=$img,discard=on"
  run qm resize "$id" scsi0 "${vm_disk[$name]}G"
  run qm set "$id" --ide2 "$storage:cloudinit" --boot order=scsi0 \
    --cicustom "user=$snip_storage:snippets/lab201-$name-user.yml,network=$snip_storage:snippets/lab201-$name-network.yml,meta=$snip_storage:snippets/lab201-$name-meta.yml"
}

gateway_name=""
while IFS='|' read -r kind a b c d e f; do
  if [[ "$kind" == VM ]]; then
    [[ -z "$current" ]] || create_vm "$current"
    current="$a"; vm_idx[$a]="$b"; vm_cpu[$a]="$c"; vm_mem[$a]="$d"; vm_disk[$a]="$e"; nic_args=()
    [[ "$f" != gateway ]] || gateway_name="$a"
  else
    # NIC|name|index|net|vlan|trunk|mac
    br="$(bridge_of "$c")"
    opt="virtio=$f,bridge=$br,firewall=0"
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
