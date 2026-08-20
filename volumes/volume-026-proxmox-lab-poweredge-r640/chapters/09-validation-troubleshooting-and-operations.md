# Chapter 09: Validation, Troubleshooting, and Operations

## Learning Objectives

- Validate the whole build end to end, from hardware to running VMs.
- Apply a layered troubleshooting method that localizes a fault to the
  right tier.
- Establish day-2 operational practice: backups, updates, and monitoring.
- Recognize the failure modes this specific build most commonly produces.
- Confirm the environment matches its specification exactly.

## Theory and Architecture

### Validating the build as a whole

The previous chapters each validated their own phase. This chapter validates
the *composition* — that the layers built up from bare hardware to running
VMs actually work together. The build is a stack, and each layer depends on
the ones beneath it:

```text
Virtual machines (Ch 08)   — ten VMs, tagged VLANs, fixed addresses
  Network (Ch 05)          — management NIC + VLAN trunk + VLAN-aware bridge
  Storage in Proxmox (Ch 06) — river datastore + ISO repository
  Proxmox VE (Ch 03-04)    — installed, updated, DNS/NTP via gateway
  Hardware storage (Ch 02) — BOSS boot mirror + river RAID 5
  iDRAC (Ch 01)            — out-of-band access
```

A fault in a running VM might originate at any layer beneath it — the VLAN
tag, the trunk, the bridge, the datastore, or the array. Validation confirms
each layer, and troubleshooting works *down* the stack to find where a
symptom originates.

### The specification as the acceptance test

This build has an exact specification — the environment table in the
[volume README](../README.md). That table is the acceptance test: the build
is done when every value in it is true of the running system. Validation is
therefore not open-ended; it is checking reality against a known list.

## Design Considerations

- **Validate against the specification, not against "it seems to work."**
  Every address, VLAN, hostname, and array in the spec is either true of the
  system or not. Check them explicitly.
- **Keep the layered mental model for troubleshooting.** When a VM has a
  problem, resist jumping to the guest OS; the cause is often a layer below —
  a tag, the trunk, the bridge. Localize before investigating.
- **Establish day-2 practice before you need it.** Backups, an update
  cadence, and basic monitoring are cheaper to set up now, with the build
  fresh, than to bolt on after an incident.
- **Document the as-built state.** The running system's actual configuration
  is the reference every future change is measured against; capture it while
  it matches the spec.

## Implementation and Automation

### 1. End-to-end validation against the specification

```bash
# --- Hardware layer (via iDRAC) ---
racadm -r 10.30.161.25 -u root -p <password> storage get vdisks -o \
  -p Name,Status,Layout          # BOSS RAID1 Online, river RAID5 Optimal

# --- Proxmox layer ---
ssh root@10.30.161.10 pveversion         # current version
ssh root@10.30.161.10 pvesm status       # river + ISO storage active
ssh root@10.30.161.10 'chronyc sources | grep 10.30.161.1'   # time via gateway

# --- Network layer ---
ssh root@10.30.161.10 'bridge vlan show | grep -E " 3| 6"'   # VLANs present

# --- VM layer: every VM up, on its VLAN, at its address ---
ssh root@10.30.161.10 'qm list'          # all ten running
```

### 2. Confirming each VM against the table

For every VM, confirm the three facts the spec fixes — VLAN, address,
gateway reachability:

```bash
# From each guest (or via the Proxmox console):
hostname                      # matches the table
ip -br addr                   # the fixed address on the right interface
ping -c2 <gateway>            # 10.30.10.1 for VLAN 3, 10.30.12.1 for VLAN 6
```

A simple as-built check script run from the host confirms no address is
duplicated and each VM's tag matches its subnet.

### 3. Establishing day-2 operations

```bash
# Backups: schedule VM backups to a target that is NOT river (availability
# is not backup). A separate NAS/share or external storage.
# In the UI: Datacenter > Backup > Add a scheduled job.

# Updates: keep the node current on the no-subscription repo (Chapter 04).
ssh root@10.30.161.10 'apt update && apt list --upgradable'

# Monitoring: the node's metrics, VM health, and the iDRAC's hardware alerts
# together cover the stack from array to guest.
ssh root@10.30.161.10 'pvesh get /nodes/$(hostname)/status --output-format json | head'
```

## Validation and Troubleshooting

### The layered troubleshooting method

When something in the environment does not work, localize before
investigating, working down the stack:

| Symptom | Check, in order | Likely layer |
| --- | --- | --- |
| A VM cannot reach its gateway | Its VLAN tag, then the bridge VLANs, then the trunk | Network (Ch 05) |
| A VM will not start | Its storage on `river`, then `river`'s health | Storage (Ch 06 / Ch 02) |
| Web UI unreachable | Management address on port 0, then the NIC | Network (Ch 05) — use iDRAC console |
| Updates fail | The enterprise repo still enabled | Repos (Ch 04) |
| Certificate/log oddities | Node time via the gateway | Services (Ch 04) |
| The node will not boot | The BOSS mirror health | Hardware (Ch 02) — use iDRAC |

The discipline is the same as the firewall and VPN chapters elsewhere in the
encyclopedia: find the layer that owns the symptom before changing anything,
and the iDRAC from Chapter 01 is the recovery path whenever the network or
boot is the problem.

### This build's characteristic failures

Three failures are specific to this build and worth recognizing on sight:

- **A server VM with the right IP but no connectivity** — almost always a
  VLAN tag of 6 where it should be 3, or (before the Chapter 05 correction)
  VLAN 3 missing from the trunk. The corrected trunk carries VLAN 3; confirm
  the VM's tag is 3.
- **A duplicate-address symptom on 10.30.10.88** — Red Hat Server and Windows
  Server both at .88 if the correction was not applied. Windows Server is
  .89.
- **Updates failing after install** — the enterprise repository still
  enabled without a key (Chapter 04); disable it.

### The as-built-versus-spec diff

The cleanest validation is a direct comparison of the running system against
the specification table. Any divergence — an address that differs, a VLAN
mistagged, a storage on the wrong array — is a defect to fix, not a variation
to accept. The spec is the definition of done.

## Security and Best Practices

- **Back up to somewhere other than `river`.** The VM datastore's RAID 5
  tolerates a drive, not a disaster; real backups live off the array, and a
  restore should be tested, not assumed.
- **Keep the whole stack patched.** Proxmox, the guests, and the iDRAC/BIOS
  firmware all need updating on a cadence; a lab is not exempt from the
  vulnerabilities in unpatched components.
- **Maintain the management-plane isolation.** The iDRAC and the host
  management interface stay on the isolated management network; the VM VLANs
  stay segmented. The security boundaries built in Chapters 01 and 05 are
  ongoing, not one-time.
- **Monitor the array and the guests.** A predictive drive failure on `river`
  or a resource-starved emulator VM is easier to catch early than to
  diagnose after it causes an outage.

## References and Knowledge Checks

**References**

- [The volume README](../README.md)
  — the environment specification that serves as the acceptance test.
- All prior chapters of this volume — the layers this chapter validates as a
  whole.
- [Volume XXIII, Chapter 06](../../volume-023-dell-idrac-9-10-administration/chapters/06-hardware-health-power-thermal-logs-and-support.md)
  — hardware health and alerting for the array and the server.
- [Volume XI](../../volume-011-observability-enterprise-operations/README.md)
  — observability and operations practice for the day-2 discipline.

**Knowledge checks**

1. Why does troubleshooting a VM problem work *down* the stack rather than
   starting at the guest OS?
2. What is the acceptance test for this build, and why is it not open-ended?
3. Give the three characteristic failures of this build and the layer each
   belongs to.
4. Why must backups target something other than `river`?
5. When the network or boot is broken, what is the recovery path, and which
   chapter established it?

## Hands-On Lab

This chapter closes the build with **validation, troubleshooting, and day-2 operations** — plus a
capstone that confirms the whole R640→Proxmox→10-VM stack. Commands are runnable `qm`/`pvesm`/
`vzdump`/journal. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.5** — the completed Proxmox node with the VM fleet deployed
(Chapter 08), and root SSH. **Cost:** none.

### Lab 9.1 — Validate the fleet and node (Topic: Validation)

**Objective:** Confirm the VMs and node are healthy.

```bash
qm list                                       # all VMs running
pvesh get /nodes/pve01/status --output-format json | python3 -c "import json,sys; d=json.load(sys.stdin); print('cpu:', round(d['cpu']*100,1),'% mem used:', round(d['memory']['used']/d['memory']['total']*100,1),'%')"
pvesm status                                  # datastores online, capacity healthy
for id in $(seq 101 110); do qm guest cmd $id ping 2>/dev/null || true; done
```

**Expected result:** all ten VMs `running`, the node's CPU/memory within healthy headroom, and
`river` with capacity to spare — validation confirms the build's goal (a node hosting ten VMs) is met
and the datastore is not over-committed.

**Negative test:** declare success from "VMs are running" without checking node memory/`river`
capacity; ten VMs may over-commit RAM (ballooning/swap) or fill the thin pool — validate node and
storage headroom, not just VM power state.

**Rollback:** none (read-only).

### Lab 9.2 — Backups with vzdump (Topic: Backups)

**Objective:** Protect the VMs with scheduled backups.

```bash
vzdump 101 --storage riverfiles --mode snapshot --compress zstd
ls -lh /river/dump/ | head
# Schedule via Datacenter > Backup (or /etc/pve/jobs.cfg) for the whole fleet, nightly.
```

**Expected result:** a compressed backup archive of VM 101 in the backup storage, and a schedulable
job for the fleet — `vzdump` (snapshot mode for running VMs) is Proxmox's built-in backup; scheduled
backups to the `river` directory storage (or a Proxmox Backup Server) make the lab recoverable.

**Negative test:** run the lab with no backups; a bad change or disk failure loses VMs with no
recovery — even a lab benefits from scheduled `vzdump`, and production requires it.

**Rollback:** remove the lab backup archive if space is tight.

### Lab 9.3 — Troubleshooting (Topic: Troubleshooting)

**Objective:** Diagnose a VM/node issue from the logs.

```bash
qm status 101 --verbose 2>/dev/null | head
journalctl -u pveproxy -u pvedaemon --since "-1 hour" --no-pager | tail
tail -5 /var/log/pve/tasks/index 2>/dev/null           # the task log: every action + result
qm showcmd 101                                          # the exact QEMU command line for a VM
```

**Expected result:** VM status, control-plane service logs, the Proxmox **task log** (every UI/CLI
action and its outcome), and the QEMU command line for a VM — Proxmox troubleshooting works from the
task log (what was done and whether it failed), service journals, and per-VM QEMU details, rather
than guessing.

**Negative test:** retry a failing VM start repeatedly without reading the task log/`qm showcmd`;
the task log names the cause (e.g. a missing ISO volid, or the thin pool full) that a retry will not
fix.

**Rollback:** none (read-only).

### Lab 9.4 — Capstone: verify the whole build (Topic: Synthesis)

**Objective:** Confirm the end-to-end R640→Proxmox→fleet stack against the build's goal.

```bash
# 1. Hardware/OOB (Ch01-02): arrays optimal, node on the BOSS mirror
racadm storage get vdisks -o | grep -iE "river|State"      # (from a mgmt host with racadm)
# 2. Platform (Ch03-04): current, services healthy
pveversion | head -1 ; systemctl is-active pve-cluster pveproxy pvedaemon
# 3. Network (Ch05): VLAN-aware bridge + reachability
bridge vlan show | head
# 4. Storage (Ch06-07): river datastore + ISO library online
pvesm status
# 5. Fleet (Ch08): ten VMs up, cloud-init-configured, backed up (Ch09)
qm list ; ls /river/dump/ 2>/dev/null | head
```

**Expected result:** every layer checks out — optimal RAID arrays, a current node with healthy
services on the BOSS mirror, a VLAN-aware network, the `river` datastore and ISO library online, and
ten backed-up VMs — the complete, working Proxmox lab this volume set out to build, verified end to
end.

**Negative test:** call the build "done" when the VMs run but backups were never configured, the
array is degraded, or the node is unpatched; the stack is fragile — the capstone verifies *every*
layer (hardware, platform, network, storage, fleet, backup), which is what "done" actually means.

**Rollback:** none — this is the finished lab; tear-down commands appear in the earlier chapters'
cleanups.

### Lab 9.5 — Reach a VM over the serial console (Topic: Out-of-band access)

**Objective:** Get a console on a guest that has **no network path** — a freshly built VM before it
has an IP, or one whose networking is broken — straight from the node, with no dependency on the
guest's addressing.

```bash
# The VM must have a serial device (serial0: socket). The qm create recipes in
# Chapter 08 set this; confirm it, then attach from the node's shell:
qm config 124 | grep -E "serial0|vga"          # expect: serial0: socket
qm terminal 124
# -> starting serial terminal on interface serial0 (press Ctrl+O to exit)
# Press Enter to wake the guest's login prompt, log in, and work as normal.
# Leave the console with Ctrl+O — this DETACHES; it does NOT stop the VM.

# If a VM was built without a serial port, add one live; it appears on next boot:
qm set 124 --serial0 socket
```

**Expected result:** `qm terminal <vmid>` prints `starting serial terminal on interface serial0
(press Ctrl+O to exit)`, and after Enter the guest's `login:` prompt appears — a working console with
no dependency on the guest's network. The same serial line is in the web UI at *VM → Console →*
dropdown *→ Serial terminal 0*. This is the path used to bootstrap every FortiGate-VM and Alpine cell
in this lab *before* it had an address ([Chapter 08](08-deploying-the-virtual-machines.md)), and the
recovery path whenever a guest's networking is misconfigured — the software analogue of
[Chapter 01](01-idrac-out-of-band-access-and-first-configuration.md)'s iDRAC out-of-band console for
the node itself.

**Negative test:** open the serial terminal in the web UI *and* run `qm terminal` on the same VM at
once — the serial socket takes a single reader, so the second attaches to a garbled, unresponsive
line. Use one serial client per VM. (The web-UI *noVNC/VGA* console is a separate channel and does not
conflict with `qm terminal`.) Likewise, do not press `Ctrl+C` to leave — it is delivered to the guest,
not the terminal; only `Ctrl+O` detaches.

**Rollback:** none — `Ctrl+O` detaches and leaves the VM running; do not confuse it with `qm stop`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The build is a stack — iDRAC, hardware storage, Proxmox, network, Proxmox
storage, and the ten VMs — and this chapter validates the composition rather
than any single layer, checking the running system against the exact
specification that serves as its acceptance test. Troubleshooting works down
the stack: a VM symptom is localized to the layer that owns it before
anything is changed, and the iDRAC out-of-band console is the recovery path
whenever the network or boot is the fault. Three failures are characteristic
of this build — a correct-IP-wrong-VLAN server VM, the .88 duplicate address,
and updates failing on the still-enabled enterprise repository — and each
maps to a specific earlier chapter and its correction. Day-2 operations —
backups off `river`, a patch cadence across the whole stack, and monitoring
from Proxmox and the iDRAC — keep the environment healthy past the build.

- [ ] Every value in the specification table confirmed true of the system.
- [ ] All ten VMs running on their correct VLANs at their fixed addresses.
- [ ] No duplicate addresses — Red Hat Server .88, Windows Server .89.
- [ ] A scheduled backup targeting storage other than `river`.
- [ ] The layered troubleshooting method exercised and understood.
