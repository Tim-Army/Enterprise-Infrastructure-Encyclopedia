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
- [Volume XXIII, Chapter 06](../../volume-23-dell-idrac-9-10-administration/chapters/06-hardware-health-power-thermal-logs-and-support.md)
  — hardware health and alerting for the array and the server.
- [Volume XI](../../volume-11-observability-enterprise-operations/README.md)
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

**Objective:** Validate the entire build against its specification, exercise
the layered troubleshooting method, and establish day-2 operations.

**Prerequisites:** The complete build from Chapters 01–08 — hardware,
Proxmox, network, storage, and the ten VMs.

**The validation is fully reproducible on the built environment;** the
capstone composes every prior chapter.

**Procedure — validation**

1. Walk the stack top to bottom with the commands above: confirm the arrays
   are healthy, Proxmox is current with time via the gateway, the bridge
   carries VLANs 3 and 6, and all ten VMs are running.
2. For each VM, confirm its hostname, address, VLAN tag, and gateway
   reachability against the specification table.
3. Confirm no address is duplicated — specifically that Red Hat Server (.88)
   and Windows Server (.89) are distinct.
4. Produce an as-built record and diff it against the README's specification
   table; every value must match.

**Procedure — day-2 operations**

5. Configure a scheduled VM backup job targeting storage *other than*
   `river`.
6. Confirm the update path is clean (`apt update`), and note the monitoring
   available from Proxmox and the iDRAC.

**Negative test**

7. Pick one server VM and re-tag its NIC from VLAN 3 to VLAN 6. Using only
   the layered method — VM tag, bridge, trunk — diagnose why it lost gateway
   connectivity, without checking the guest OS first. Confirm the method
   localizes the fault to the network layer and the tag specifically, then
   restore VLAN 3.

**Expected results**

- Every value in the specification table confirmed true of the running
  system.
- No duplicate addresses; the .88/.89 split verified.
- A scheduled backup targeting off-array storage.
- The layered method demonstrated to localize a fault without guesswork.

**Cleanup**

8. Restore any change made in the negative test, confirm all ten VMs are
   healthy on their correct VLANs, and retain the as-built record as the
   reference for future changes.

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
