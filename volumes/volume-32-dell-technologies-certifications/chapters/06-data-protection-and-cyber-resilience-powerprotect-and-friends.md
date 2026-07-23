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

With DDVE (Data Domain Virtual Edition) on the Volume XXVI lab where
entitled: build an MTree, Boost unit, and replication pair; lock a
copy; protect two lab VMs with a Data Manager policy; run one
restore and one vault-style rehearsal narrative (isolated copy,
verified recovery). Otherwise: the full runbook with exact commands
and expected outputs against the guides.

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
