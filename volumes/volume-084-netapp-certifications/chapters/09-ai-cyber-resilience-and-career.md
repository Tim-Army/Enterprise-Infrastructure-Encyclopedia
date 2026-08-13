# Chapter 09: AI, Cyber Resilience, and Career

## Learning Objectives

- Place the AI Expert and AI Data Infrastructure Expert credentials and ONTAP AI in the portfolio.
- Enable Autonomous Ransomware Protection (ARP) on a volume.
- Apply immutable, tamper-proof retention with SnapLock.
- Plan certification prep, currency, and career progression.
- Complete a walkthrough for each AI/cyber-resilience topic.

## Theory and Architecture

The **Certified Expert** tier includes two AI credentials — **AI Expert** and **AI Data Infrastructure**
— and the **Cyber Resiliency** expert. **ONTAP AI** is NetApp's validated architecture for machine
learning and analytics: NVIDIA **DGX** GPU compute with NetApp **AFF** all-flash storage (the **AIPod**
reference design), feeding data pipelines at scale; the AI credentials validate designing and running
that data infrastructure. **Cyber Resiliency** is defensive: protecting and recovering **your own** data
from ransomware and tampering. Its core ONTAP controls are **Autonomous Ransomware Protection (ARP)** —
on-box machine learning that watches a volume's I/O for ransomware-like behavior (abnormal entropy and
file activity), raises alerts, and takes an automatic protective Snapshot — and **SnapLock**, which
writes data in **WORM** (write-once, read-many) form for compliance or enterprise retention so even an
administrator cannot alter or early-delete it. Together with immutable **Snapshots**, off-box
**SnapMirror** copies (Chapters 05–06), and **multi-admin verification**, they give a tamper-resistant
recovery position. This chapter closes with prep, currency, and career.

## Design Considerations

Design **ONTAP AI** so storage throughput keeps the GPUs fed (all-flash, high-bandwidth networking).
Enable **ARP** on volumes holding valuable, user-changeable data and review its learning period. Use
**SnapLock Compliance** for regulatory WORM and **SnapLock Enterprise** where a trusted admin may still
manage retention. Combine immutable Snapshots, off-box copies, and **multi-admin verification** so no
single compromised account can destroy recovery data. Plan certification **currency** against the
April 2026 exam refresh and the ~two-year validity.

## Implementation and Automation

The labs enable ARP and confirm its state, apply a SnapLock retention model, and reason about ONTAP AI
and a certification/career path — the resilience and progression these Expert credentials validate.

## Validation and Troubleshooting

Confirm resilience and progression:

```text
AI: ONTAP AI = NVIDIA DGX + NetApp AFF (AIPod); AI Expert + AI Data Infrastructure validate the design
ARP: on-box ML watches volume I/O -> alert + automatic protective Snapshot on ransomware-like activity
SnapLock: WORM retention (Compliance = even admin can't delete; Enterprise = trusted admin manages)
Recovery: immutable Snapshots + off-box SnapMirror + multi-admin verification
Career: NCDA -> Specialist (NCIE) -> Expert (Architect / AI / Cyber Resiliency); recert ~2 yrs
```

Common pitfalls: assuming **ARP** blocks an attack outright (it detects, alerts, and snapshots — recovery
still relies on protected copies); and choosing **SnapLock Compliance** when business change control is
needed (it cannot be shortened) — match the mode to the requirement.

## Security and Best Practices

ARP, SnapLock WORM, immutable Snapshots, off-box copies, and multi-admin verification are **defensive**
controls that protect and recover **your own** data — there is no offensive content here. Keep the
recovery copies off the production cluster and require multiple admins for destructive operations.

## Hands-On Lab

AI-and-cyber-resilience walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster
(`admin@cluster1`), SVM `svm_app`, volume `vol_finance`, and `python3`. **Cost:** none.

### Lab 9.1 — Enable Autonomous Ransomware Protection

**Objective:** Turn on on-box ransomware detection.

```text
cluster1::> security anti-ransomware volume enable -vserver svm_app -volume vol_finance
cluster1::> security anti-ransomware volume show -vserver svm_app -volume vol_finance \
  -fields state,attack-probability
vserver  volume       state    attack-probability
-------- ------------ -------- ------------------
svm_app  vol_finance  enabled  none
```

**Expected result:** ARP `enabled` on the volume, learning normal I/O — it will alert and snapshot on
ransomware-like activity.

**Negative test:** treat ARP as a preventive firewall and skip backups; ARP **detects and snapshots**
but recovery needs protected copies — keep SnapMirror/SnapVault copies too.

**Rollback:** none (ARP is left enabled — the protected state).

### Lab 9.2 — Apply immutable SnapLock retention

**Objective:** Make data tamper-proof (WORM).

```text
cluster1::> volume create -vserver svm_app -volume vol_archive -aggregate aggr1_data -size 20GB \
  -snaplock-type enterprise
cluster1::> volume snaplock modify -vserver svm_app -volume vol_archive \
  -default-retention-period 7years -minimum-retention-period 1years

cluster1::> volume snaplock show -vserver svm_app -volume vol_archive \
  -fields snaplock-type,default-retention-period
vserver  volume       snaplock-type default-retention-period
-------- ------------ ------------- ------------------------
svm_app  vol_archive  enterprise    7years
```

**Expected result:** a SnapLock Enterprise volume with a 7-year default retention — committed files
become WORM and cannot be altered or early-deleted.

**Negative test:** store immutable regulatory records on a normal volume; an admin or attacker can
delete them — use a **SnapLock** WORM volume.

**Rollback:**

```text
cluster1::> volume offline -vserver svm_app -volume vol_archive
cluster1::> volume delete -vserver svm_app -volume vol_archive
```

*(In production, committed SnapLock Compliance data cannot be deleted before its retention expires; the
simulator lab uses an uncommitted Enterprise volume so cleanup succeeds.)*

### Lab 9.3 — Plan certification currency and career

**Objective:** Map the path forward and keep credentials current.

```python
python3 - <<'PY'
ladder = [
  ("Associate",   "Cloud Native / Hybrid Cloud Associate accreditations"),
  ("Professional","Technology Solutions + Data Administrator ONTAP (NCDA, NS0-163)"),
  ("Specialist",  "NCIE SAN (NS0-521) / Data Protection (NS0-528) / MetroCluster / FlexPod"),
  ("Expert",      "Hybrid Cloud Architect (NS0-604) / AI Expert / AI Data Infra / Cyber Resiliency"),
]
for tier, certs in ladder:
    print(f"{tier:12}: {certs}")
print("Currency: exams refreshed Apr 2026; ~2-yr validity; recert by current or higher exam")
print("Prep: free NetApp exam-prep videos + Learning Center courses + Simulate ONTAP")
PY
```

**Expected result:** the four-tier ladder with a currency plan — a career map from NCDA to Expert.

**Negative test:** let an NCDA lapse past its validity while chasing an Expert exam; the foundation
expires — recertify on cadence with the current exam.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Expert tier adds AI (ONTAP AI on NVIDIA DGX + NetApp AFF, validated by AI Expert and AI Data
Infrastructure) and Cyber Resiliency — defensive protection of your own data with Autonomous Ransomware
Protection, immutable SnapLock WORM retention, immutable Snapshots, and off-box copies. The career
ladder runs Associate → NCDA → Specialist (NCIE) → Expert, kept current against the April 2026 refresh.

- [ ] I can place the AI credentials and ONTAP AI in the portfolio.
- [ ] I can enable Autonomous Ransomware Protection.
- [ ] I can apply SnapLock WORM retention.
- [ ] I can plan certification currency and career progression.
- [ ] I completed Labs 9.1–9.3 including each negative test.
