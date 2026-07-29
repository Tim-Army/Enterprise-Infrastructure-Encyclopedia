# Chapter 06: Data Protection and Cyber Resilience — PowerProtect and Friends

## Learning Objectives

- Operate and deploy PowerProtect Data Domain (dedupe architecture,
  DD Boost, replication) and Data Manager (policy-driven protection)
- Design PowerProtect solutions and position the appliance line
  (DP series, Data Manager Appliance)
- Deploy Cyber Recovery vaults and articulate the ransomware-era
  recovery doctrine this encyclopedia's Volume XII demands
- Map the fifteen-exam family: Foundations D-DP-FN-01; Data Domain
  D-PDD-OE-01/DY-01; Data Manager D-PDM-DY-01 (+ appliance
  D-PDM-A-01, DP series D-PDPS-A-01); Cyber Recovery D-PCR-DY-01;
  Avamar D-AV-OE-23/DY-23; NetWorker D-NWR-DY-01; RecoverPoint
  D-RP-OE-A-24/DY-A-24 and RP4VM D-RPVM-A-01; Solutions Design
  D-DP-DS-01; suite D-DPS-A-01

## Theory and Architecture

### The stack in one sentence

Dell's data protection is a **target** (Data Domain: variable-length
dedupe, DD Boost client-side distribution, MTree replication), a
**brain** (Data Manager: SLA-policy protection of VMs, databases,
K8s, file), **legacy movers** still certified at scale (Avamar,
NetWorker), **continuous replication** (RecoverPoint and RP4VM
journal-based any-point-in-time), and the **vault** (Cyber Recovery:
an air-gapped Data Domain replica with CyberSense analytics) — the
architecture Chapter 01's function grammar slices into fifteen exams.

### Data Domain is the center of gravity

Everything lands on DD: Boost changes backup topology (source-side
dedupe, managed file replication), MTrees partition tenants and
retention, and **Retention Lock** (governance/compliance modes)
turns the target into the immutability layer ransomware doctrine
requires. The OE exam is filesystem/replication administration; DY
adds deployment, capacity, and integration into the movers above.

### Cyber Recovery is doctrine, not product trivia

The vault exam certifies the pattern Volume XII teaches: replicate
to an isolated enclave over a controlled link, lock copies, analyze
with CyberSense, and rehearse recovery from the vault — the
operational answer to "backups were encrypted too."

## Design Considerations

- Design from restore requirements backward (Volume XII's RTO/RPO
  discipline); dedupe ratios are workload facts, not marketing
- One policy engine: consolidate movers toward Data Manager unless an
  installed base (Avamar/NetWorker estates) pays to stay
- The vault link is the design: schedule, direction, and lock policy
  drawn explicitly; a vault reachable at will is not a vault
- RecoverPoint where seconds of RPO matter; backup policies where
  hours do — write both numbers before choosing

## Implementation and Automation

```text
# Data Domain essentials (the OE exam's daily verbs)
filesys show space; mtree list
ddboost storage-unit create su-app1 user boost-app
mtree create /data/col1/app1
replication add source mtree://dd-a/data/col1/app1 \
  destination mtree://dd-b/data/col1/app1
mtree retention-lock enable mode compliance mtree /data/col1/app1

# Data Manager: policy-as-API (Volume IX pipelines apply)
POST /api/v2/protection-policies   # SLA: targets, schedule, retention
POST /api/v2/asset-assignments     # bind VMs/DBs to the policy
```

## Validation and Troubleshooting

- Restore tests are the only truth (Volume XII): schedule them; a
  green backup job proves nothing about recovery
- DD: `filesys show space` cleaning behavior, replication lag per
  MTree, Boost client stats before network guesses
- Data Manager: policy compliance dashboard, then per-asset job
  logs; agent/proxy health before policy edits
- Vault: rehearsal cadence with timed recovery evidence; CyberSense
  verdicts reviewed, not archived

## Security and Best Practices

- Retention Lock Compliance plus separated vault credentials — the
  admin who runs backups must not be able to unlock or reach the
  vault
- DD Boost users least-privileged per mover; management on the
  management VLAN; MFA on every console
- Runbooks for vault recovery stored offline with the Volume XII
  drill calendar

## References and Knowledge Checks

- Exam descriptions for all fifteen codes above (Dell Learning
  catalog); DD OS and Data Manager admin guides; Cyber Recovery
  solution guide

Knowledge checks:

1. Why does DD Boost move dedupe to the client, and what does that do
   to backup-window math?
2. Governance versus Compliance Retention Lock: who can undo what?
3. Which failures does RP4VM answer that a 4-hour backup policy
   cannot, and what does its journal cost?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab spanning the **data protection and
cyber-resilience exams — Foundations and Design (D-DP-FN-01, D-DP-DS-01), PowerProtect
Data Domain (D-PDD-*), Data Manager (D-PDM-*), DP/DPS appliances (D-PDPS-A-01,
D-DPS-A-01), Cyber Recovery (D-PCR-DY-01), Avamar (D-AV-*), NetWorker (D-NWR-DY-01),
and RecoverPoint (D-RP-*, D-RPVM-A-01)** — mapped in the volume README's coverage
tables. Labs use the Data Domain, PowerProtect, Cyber Recovery, and Avamar CLIs. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.10** — a PowerProtect Data Domain, a
PowerProtect Data Manager, a Cyber Recovery vault, and Avamar/NetWorker/RecoverPoint
management access. **Cost:** none beyond lab resources.

### Lab 6.1 — Data protection foundations (Data Protection Foundations)

**Objective:** Identify the protection methods and their RPO/RTO.

```text
show filesys space
show replication status
```

**Expected result:** the protected capacity and replication posture — data protection
combines **backup/archive** (point-in-time copies with retention), **replication**
(remote copies for DR), **snapshots** (fast local recovery), and **cyber recovery**
(isolated immutable copies), each with a different RPO/RTO and threat model.

**Negative test:** rely on backups alone against ransomware that also encrypts the
backup catalog/repository; an **isolated, immutable** copy (Cyber Recovery) is what
survives — RPO/RTO planning must include the cyber threat.

**Cleanup:** none (read-only).

### Lab 6.2 — Data Domain MTree and filesystem (PowerProtect Data Domain Deploy)

**Objective:** Create an MTree and read dedup on Data Domain.

```text
mtree create /data/col1/lab-mtree
mtree list
filesys show compression /data/col1/lab-mtree
```

**Expected result:** the MTree and its dedup/compression ratio — **PowerProtect Data
Domain** is the protection-storage target: **MTrees** are managed namespaces (per
app/tenant), and inline variable-length **deduplication** stores only unique segments,
yielding large effective:used ratios and efficient replication.

**Negative test:** target a Data Domain with backups of pre-encrypted data; the dedup
ratio collapses — client-side encryption before the DD defeats dedup (use DD-side
encryption instead).

**Cleanup:** `mtree delete /data/col1/lab-mtree`.

### Lab 6.3 — DD Boost (PowerProtect Data Domain Operate)

**Objective:** Verify DD Boost storage units and distributed dedup.

```text
ddboost enable
ddboost storage-unit create LAB-SU
ddboost storage-unit show
ddboost show stats
```

**Expected result:** the Boost storage unit and stats — **DD Boost** moves part of the
dedup to the backup client/server so only unique segments cross the network, cutting
backup bandwidth and time; storage units are the Boost-accessed containers.

**Negative test:** send backups over generic CIFS/NFS instead of Boost; the full data
crosses the network (no distributed dedup) — Boost is what reduces the transfer.

**Cleanup:** `ddboost storage-unit delete LAB-SU`.

### Lab 6.4 — Data Domain replication (PowerProtect Data Domain Operate)

**Objective:** Configure and read MTree replication to a remote DD.

```text
replication add source mtree://ddsrc/data/col1/lab-mtree destination mtree://dddst/data/col1/lab-mtree
replication status
replication show performance
```

**Expected result:** the replication context and lag — Data Domain replicates
**deduplicated** data (MTree, collection, or managed-file), so only unique segments
traverse the WAN, making offsite DR copies bandwidth-efficient with a small RPO.

**Negative test:** expect full-bandwidth transfer sizing for DD replication; because it
sends only unique post-dedup segments, sizing on logical data over-provisions the link
— size on the daily unique change rate.

**Cleanup:** `replication break destination mtree://dddst/data/col1/lab-mtree`.

### Lab 6.5 — PowerProtect Data Manager protection policy (Data Manager Deploy)

**Objective:** Read a PPDM protection policy and its assets.

```bash
curl -sk -H "Authorization: Bearer $PPDM" "https://$PPDM_HOST/api/v2/protection-policies" | jq -r '.content[]? | "\(.name) \(.assetType)"'
curl -sk -H "Authorization: Bearer $PPDM" "https://$PPDM_HOST/api/v2/protection-jobs?filter=result.status eq \"FAILED\"" 2>/dev/null | jq '.page.totalElements'
```

**Expected result:** the protection policies and any failed jobs — **PowerProtect Data
Manager** is the software-defined data-protection control plane: it discovers assets
(VMs, DBs, K8s, file systems), applies **protection policies** (backup to Data Domain,
replication, cloud tiering), and reports compliance centrally.

**Negative test:** a policy with no schedule/SLA protects nothing; assets stay
unprotected until a policy with a schedule covers them — discovery plus an active
policy is required.

**Cleanup:** none (read-only).

### Lab 6.6 — PowerProtect appliances: DP/DPS series (PowerProtect DP Series Appliances)

**Objective:** Read an integrated PowerProtect appliance's components.

```bash
curl -sk -H "Authorization: Bearer $PPDM" "https://$PPDM_HOST/api/v2/appliances" 2>/dev/null | jq -r '.content[]? | "\(.name) \(.model) \(.status)"'
```

**Expected result:** the integrated appliance (protection software + Data Domain) —
the **PowerProtect DP series** (formerly IDPA) are integrated appliances bundling the
protection software, search, and Data Domain storage in one system for turnkey backup,
while **DPS** (Data Protection Suite) is the software portfolio.

**Negative test:** expect to scale the appliance's protection software separately from
its storage; the integrated appliance scales as a unit — that integration is its
value versus build-your-own.

**Cleanup:** none (read-only).

### Lab 6.7 — PowerProtect Cyber Recovery vault (Cyber Recovery Deploy)

**Objective:** Read the Cyber Recovery vault and its air-gap sync.

```bash
curl -sk -H "Authorization: Bearer $CR" "https://$CR_HOST/irapi/policies" 2>/dev/null | jq -r '.[]? | "\(.name) \(.action)"'
curl -sk -H "Authorization: Bearer $CR" "https://$CR_HOST/irapi/copies" 2>/dev/null | jq '. | length'
```

**Expected result:** the CR policies and immutable copies — **PowerProtect Cyber
Recovery** maintains an isolated vault: an **operational air gap** opens only to
replicate, then closes; copies are made **immutable (Retention Lock)** and analyzed by
**CyberSense** for tampering, so a clean recovery point survives ransomware.

**Negative test:** leave the air-gap link permanently open (always-on replication);
malware can reach the vault — the scheduled, normally-closed air gap is the protection.

**Cleanup:** none (read-only).

### Lab 6.8 — Avamar backup (Avamar Deploy)

**Objective:** Read Avamar clients, datasets, and backup status.

```text
mccli client show
mccli backup show --recursive=true | head
avmaint config --ava | grep -i capacity
```

**Expected result:** the Avamar clients and recent backups — **Avamar** does
client-side (source) deduplication: only unique segments leave the client, making it
efficient for remote offices, VMs, and file systems, storing to its own grid or to
Data Domain.

**Negative test:** back up dense change-rate databases with Avamar source dedup and CPU
on the client spikes; for high-change DBs, DD Boost/PPDM (server-side) may fit better —
match the dedup model to the workload.

**Cleanup:** none (read-only).

### Lab 6.9 — NetWorker (NetWorker Deploy)

**Objective:** Read NetWorker clients, pools, and a backup group.

```text
nsradmin -p nsrd -i /dev/null <<'EOF'
show name; type
print type: NSR client
EOF
nsrpolicy list
```

**Expected result:** the NetWorker clients and policies — **NetWorker** is the
enterprise backup application: it protects heterogeneous clients (OS, DB, VM, NAS via
NDMP) to Data Domain or tape, organized by data-protection policies/workflows and
media pools, at large scale.

**Negative test:** a client not in any protection group/policy is never backed up —
NetWorker protects only what a policy/workflow includes.

**Cleanup:** none (read-only).

### Lab 6.10 — RecoverPoint continuous data protection (RecoverPoint Deploy)

**Objective:** Read a RecoverPoint consistency group and journal.

```text
get_group_state
get_consistency_group_settings
get_system_status
```

**Expected result:** the consistency group replicating with a journal — **RecoverPoint**
(and **RecoverPoint for VMs**) provides **continuous data protection**: every write is
journaled, so you can recover to any point in time (not just scheduled snapshots),
with local and remote (sync/async) replication for granular, near-zero-RPO recovery.

**Negative test:** size the journal too small for the retention/change rate; the
protection window shrinks and old points age out — the journal must fit the desired
rewind window.

**Cleanup:** none (read-only).

## Lab Verification

Verification means one restore completed with data proof, the locked
copy resisted deletion with the error captured, replication lag was
observed and explained, and the rehearsal narrative names times,
gates, and evidence.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] DD architecture (Boost/MTree/locks) operated or runbooked
- [ ] Data Manager policy model exercised
- [ ] Vault doctrine articulated with rehearsal evidence
- [ ] All fifteen family codes recorded from the verified table
