# Chapter 03: Midrange Storage — PowerStore, Unity, and PowerVault

## Learning Objectives

- Administer PowerStore at Operate depth: appliances, volumes and
  vVols, snapshots and thin clones, replication, and file services
- Position Unity XT and PowerVault ME5 in the midrange lineup and
  know their exams' scope
- Deploy PowerStore: cabling and cluster creation through host
  connectivity (FC/iSCSI/NVMe-oF) and migration
- Map the ladders: PowerStore OE/DY/DS/MN (D-PST-OE-23, D-PST-DY-23,
  D-PST-DS-00, D-PST-MN-A-01), Unity OE/DY (D-UN-OE-23, D-UN-DY-23),
  PowerVault ME5 (D-PV-DY-A-00)

## Theory and Architecture

### The midrange in one sentence

PowerStore is Dell's lead midrange array — container-based PowerStoreOS
on active-active NVMe appliances, always-on inline dedupe/compression,
vVols-first VMware integration — with Unity XT as the still-certified
prior generation and PowerVault ME5 as the entry SAN behind servers
and small clusters. The certification ladders follow Chapter 01's
function grammar exactly.

### PowerStore's objects, the exam's objects

Appliance → volumes / volume groups (crash-consistent groups for
apps), vVol storage containers for VMware, file: NAS servers with
SMB/NFS on the same cluster. Data reduction is not optional (sizing
honesty), snapshots are redirect-on-write with policies, replication
is asynchronous per volume group with Metro options on current
releases — the Operate exam lives in exactly these nouns, PowerStore
Manager and CLI both.

### Deploy and Design change the questions

Deploy adds discovery/initialization, PowerStore-to-host pathing
(NVMe-oF included), importing external storage natively, and
integration touchpoints (vCenter, CloudIQ). Design turns the same
facts into sizing: workload profiles against data-reduction
assumptions, appliance and drive counts, and replication topology —
the D-PST-DS-00 mindset this encyclopedia's Volume VI generalizes.

## Design Considerations

- vVols-first for VMware estates; VMFS remains for edge cases —
  decide per cluster, not per datastore
- File and block on one appliance is a consolidation win and a
  failure-domain decision; draw it before enabling NAS
- Unity XT choose only to extend an installed base; ME5 where cost
  per usable TB beats every software feature argument
- CloudIQ from day one: fleet health/forecasting is free telemetry

## Implementation and Automation

```text
# PowerStore CLI (pstcli) essentials the Operate exam mirrors
pstcli -d ps-lab volume create -name vol-app1 -size 2T
pstcli -d ps-lab volume_group create -name vg-app1 -members vol-app1
pstcli -d ps-lab snapshot_rule create -name hourly -interval One_Hour -keep 24
pstcli -d ps-lab protection_policy create -name pp-app1 -snapshot_rules hourly
pstcli -d ps-lab volume modify -name vol-app1 -protection_policy pp-app1

# REST is first-class; everything above is POST-able for Volume IX pipelines
```

## Validation and Troubleshooting

- Appliance health and alerts in PowerStore Manager, then hardware
  views — controller/drive state before any performance theory
- Host connectivity: initiator sessions and multipath state on both
  ends; NVMe-oF namespaces verified from the host's view
- Performance triage order: workload profile change, data-reduction
  ratio shift, path imbalance, then drive/controller saturation
- Replication: session state and RPO compliance, not just "enabled"

## Security and Best Practices

- Array management on the management VLAN only; RBAC with directory
  auth; no shared admin accounts
- Data at Rest Encryption verified, not assumed; external key
  management where policy demands
- Snapshot policies are not backup: Chapter 06's data-protection
  ladder owns recoverability

## References and Knowledge Checks

- Exam descriptions: D-PST-OE-23/DY-23/DS-00/MN-A-01, D-UN-OE-23,
  D-UN-DY-23, D-PV-DY-A-00 (Dell Learning catalog)
- PowerStore admin and CLI guides; Volume VI of this encyclopedia

Knowledge checks:

1. Why does a volume group, not a volume, own the application's
   snapshot policy?
2. A host sees one path to each PowerStore node. Name the two ends
   you verify and the exam function (OE or DY) that owns each.
3. Give the one-sentence positioning that separates PowerStore,
   Unity XT, and ME5 in 2026.

## Hands-On Lab

Where hardware or simulator access exists: create the block objects
end to end (volume, group, policy), present to a Volume XXVI lab VM
over iSCSI, take and restore a snapshot; document the same flow via
REST calls. Without array access: build the full object model and
REST call sequence as a runbook against the official CLI/REST guides,
with expected outputs.

## Lab Verification

Verification means the object chain (volume→group→policy) exists with
evidence, the host mounted and survived a controlled path-down, the
snapshot restore was proven with data, and the REST runbook replays
the CLI story call for call.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] PowerStore object model and policies operated
- [ ] Host connectivity verified both ends, one failure induced
- [ ] Deploy/Design scopes distinguished per the D-codes
- [ ] Unity/ME5 positioning recorded
