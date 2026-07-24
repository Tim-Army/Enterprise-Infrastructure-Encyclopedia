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

This chapter carries a topic-level walkthrough lab spanning the **midrange and entry
storage exams — PowerStore Operate/Deploy/Design/Maintenance (D-PST-*), Unity
Operate/Deploy (D-UN-*), and PowerVault ME5 (D-PV-DY-A-00)** — mapped in the volume
README's coverage tables. Labs use the PowerStore CLI/REST, the Unity `uemcli`, and
the ME5 CLI. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.9** — a PowerStore appliance reachable at
`$PS` with a REST token in `$T`, a Unity system with `uemcli`, a PowerVault ME5, and
CloudIQ access. **Cost:** none beyond lab resources.

### Lab 3.1 — PowerStore provisioning (PowerStore Deploy)

**Objective:** Create a block volume via the PowerStore REST API.

```bash
curl -sk -X POST -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/volume" \
  -H 'Content-Type: application/json' -d '{"name":"LAB-VOL","size":107374182400}'
curl -sk -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/volume?select=name,size,state" | jq '.[] | select(.name=="LAB-VOL")'
```

**Expected result:** the 100 GB volume created and `Ready` — PowerStore provisions
block volumes (and volume groups) from a single pool with always-on data reduction;
the REST API (and PSTCLI/UI) drives provisioning, and host mappings expose it over
FC/iSCSI/NVMe.

**Negative test:** create a volume without mapping it to a host; the host sees no
LUN — provisioning plus a **host mapping** is required for access.

**Cleanup:** DELETE the volume by its id.

### Lab 3.2 — PowerStore snapshots and thin clones (PowerStore Operate)

**Objective:** Snapshot a volume and create a thin clone.

```bash
curl -sk -X POST -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/volume/$VID/snapshot" -d '{"name":"LAB-SNAP"}'
curl -sk -X POST -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/volume/$VID/clone" -d '{"name":"LAB-CLONE"}'
```

**Expected result:** the snapshot and a space-efficient thin clone — PowerStore
snapshots are redirect-on-write (instant, space-efficient); **thin clones** are
writable, sharing blocks with the source until changed, ideal for test/dev.

**Negative test:** delete the source volume with dependent snapshots/clones; PowerStore
blocks or requires handling the dependents — the data relationships are enforced.

**Cleanup:** delete the clone and snapshot.

### Lab 3.3 — PowerStore replication (PowerStore Operate)

**Objective:** Read an asynchronous replication session and its RPO.

```bash
curl -sk -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/replication_session?select=state,role,estimated_completion_timestamp" | jq '.' | head
```

**Expected result:** the replication session, role (source/destination), and RPO —
PowerStore replicates asynchronously to a remote system (and offers **metro** active/
active for zero-RPO between two systems), protecting against site loss with a
policy-driven RPO.

**Negative test:** set an RPO shorter than the change rate can meet over the link; the
session falls behind and misses the RPO — the RPO must fit the data-change rate and
bandwidth.

**Cleanup:** none (read-only).

### Lab 3.4 — PowerStore file / NAS (PowerStore Deploy)

**Objective:** Create a NAS server and a file system.

```bash
curl -sk -X POST -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/nas_server" -d '{"name":"LAB-NAS"}'
curl -sk -X POST -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/file_system" -d '{"name":"LAB-FS","size_total":10737418240,"nas_server_id":"'$NAS'"}'
```

**Expected result:** the NAS server and file system created — PowerStore is unified:
the same appliance serves file (SMB/NFS via a **NAS server**) alongside block, with
snapshots, quotas, and replication on file systems too.

**Negative test:** create a file system with no NAS server; the API requires a
`nas_server_id` — the NAS server (the file protocol endpoint) must exist first.

**Cleanup:** delete the file system then the NAS server.

### Lab 3.5 — PowerStore sizing and design (PowerStore Design)

**Objective:** Read the metrics that drive a PowerStore sizing/design decision.

```bash
curl -sk -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/metrics/generate" -X POST \
  -d '{"entity":"performance_metrics_by_appliance","entity_id":"'$APP'"}' | jq '.[0] | {avg_latency, iops, bandwidth}' 2>/dev/null
curl -sk -H "DELL-EMC-TOKEN: $T" "https://$PS/api/rest/appliance?select=name,model" | jq '.'
```

**Expected result:** latency/IOPS/bandwidth and the appliance model — PowerStore
**design** sizes the appliance model and count from workload IOPS/throughput/latency
and capacity (post data-reduction), scaling out (clustering appliances) or up (adding
drives) as needed.

**Negative test:** size on raw capacity ignoring the data-reduction ratio; the design
over-provisions drives — effective capacity (after dedup/compression) is the sizing
basis.

**Cleanup:** none (read-only).

### Lab 3.6 — Unity provisioning with uemcli (Unity Deploy)

**Objective:** Create a Unity LUN via `uemcli`.

```text
uemcli -d $UNITY -u admin -p $PW /stor/prov/luns/lun create -name LAB-LUN -size 100G -pool pool_1
uemcli -d $UNITY -u admin -p $PW /stor/prov/luns/lun show
```

**Expected result:** the LUN created in the pool — Dell **Unity** (uemcli) provisions
block LUNs and file systems from storage pools; uemcli is the scriptable interface for
provisioning, hosts, snapshots, and replication.

**Negative test:** create a LUN in a pool with insufficient free capacity; uemcli
returns an error — the pool must have capacity (thin allows over-subscription with
monitoring).

**Cleanup:** `uemcli ... /stor/prov/luns/lun -name LAB-LUN delete`.

### Lab 3.7 — Unity snapshots and replication (Unity Operate)

**Objective:** Snapshot a LUN and read replication sessions.

```text
uemcli -d $UNITY -u admin -p $PW /prot/snap create -source LAB-LUN -name LAB-SNAP
uemcli -d $UNITY -u admin -p $PW /prot/rep/session show
```

**Expected result:** the snapshot and any replication session — Unity offers unified
snapshots (block/file) and native async/synchronous replication to a remote Unity for
DR, managed through uemcli or Unisphere.

**Negative test:** configure synchronous replication between systems without the
required low-latency link; sessions fail or throttle writes — synchronous needs a
metro-distance link.

**Cleanup:** `uemcli ... /prot/snap -name LAB-SNAP delete`.

### Lab 3.8 — PowerVault ME5 provisioning (PowerVault ME5)

**Objective:** Create a disk group and volume on ME5.

```text
create disk-group type virtual disks 0.0-0.5 level r6 pool A name dg01
create volume size 100GB pool A name LAB-VOL
map volume LAB-VOL access rw
show volumes
```

**Expected result:** the RAID-6 disk group, volume, and host mapping — **PowerVault
ME5** is the entry block array (SAS/iSCSI/FC): create disk groups (RAID), carve
volumes from pools, and map them to hosts, for cost-effective direct/SAN block
storage.

**Negative test:** map a volume without defining the host/initiator; the host cannot
access it — mapping requires a known initiator.

**Cleanup:** `delete volumes LAB-VOL` then `delete disk-groups dg01`.

### Lab 3.9 — CloudIQ monitoring (PowerStore/Unity Operate)

**Objective:** Read proactive health/capacity from CloudIQ.

```bash
curl -s -H "Authorization: Bearer $CIQ" "https://cloudiq.dell.com/api/v1/systems" 2>/dev/null | jq -r '.results[]? | "\(.name) \(.health_score)"' | head
```

**Expected result:** the systems with health scores — **CloudIQ** is Dell's cloud-
based AIOps: it aggregates telemetry from PowerStore/Unity/PowerMax/PowerScale/
PowerEdge for health scores, capacity/performance forecasting, anomaly detection, and
cybersecurity assessment.

**Negative test:** expect CloudIQ data from a system with SupportAssist/connectivity
disabled; it does not report — the system must send telemetry to CloudIQ.

**Cleanup:** none (read-only).

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
