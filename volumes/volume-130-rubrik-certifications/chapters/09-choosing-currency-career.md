# Chapter 09: Choosing a Path, Currency, and Career

## Learning Objectives

- Choose between the free and paid RCSA study routes for your situation.
- Build a study plan across the Rubrik Security Cloud domains.
- Keep knowledge current as the platform and program evolve.

## Choosing your route to RCSA

There is one active certification, **RCSA**, and two ways to prepare:

| Route | Best for |
|:---|:---|
| **Free learning path** | Self-motivated learners; already have hands-on access; budget-conscious. eLearning → unlimited practice exams → final exam |
| **Paid bootcamp** | Those who want instructor-led, hands-on labs (4-day RSC Administration bootcamp, ~60% labs); exam questions drawn from bootcamp content |

Either way, the practice exams (unlimited attempts, immediate feedback) are the readiness signal: **once you consistently pass the practice exams, you're ready for the final.** Rubrik Support credentials are required to access Rubrik University. Beyond RCSA, the topic **workshops** (Threat Detection & Incident Recovery, Cloud-Native Workloads, Database Workloads) deepen specific areas.

## Study approach

| Domain | Volume chapters | Study emphasis |
|:---|:---|:---|
| RSC architecture / data protection | [02](02-rsc-architecture-data-protection.md) | SLA Domains, compliance, control/data planes |
| Immutability & air-gap | [03](03-immutability-and-air-gap.md) | Why backups survive ransomware |
| Ransomware / cyber recovery | [04](04-ransomware-cyber-recovery.md) | Anomaly detection, last-clean-snapshot |
| DSPM | [05](05-dspm.md) | Discovery, classification, data risk |
| Recovery orchestration | [06](06-recovery-orchestration.md) | RTO/RPO, mass recovery, validation |
| Workloads | [07](07-workloads.md) | VM/DB/cloud/SaaS protection choices |
| Security & identity | [08](08-security-rbac-identity-resilience.md) | RBAC, MFA, identity resilience |

RCSA centers on **operating** the platform — SLA Domains, compliance, and recovery — so weight your hands-on time on Chapters 02, 06, and 07. The security/resilience chapters (03–05, 08) explain *why* the platform is built as it is, which the exam expects you to understand.

## The Rubrik context in the encyclopedia

Rubrik sits at the intersection of **data protection** and **cyber security** — the cyber-resilience layer:

- Data-protection neighbors: [Veeam LXXXV](../../volume-085-veeam-certifications/README.md), [NetApp LXXXIV](../../volume-084-netapp-certifications/README.md) — backup/storage programs to contrast.
- Security neighbors: [CrowdStrike L](../../volume-050-crowdstrike-certifications/README.md) (endpoint detection), [Enterprise Cybersecurity X](../../volume-010-enterprise-cybersecurity/README.md) (the broader program).
- Identity: [Microsoft Certifications Beyond Azure XXXVIII](../../volume-038-microsoft-certifications-beyond-azure/README.md) — the AD/Entra identity resilience protects.

Rubrik's distinctive angle among backup vendors is the **security** framing: immutability, data threat analytics, DSPM, and identity resilience — treating backup as a security control, not just IT insurance.

## Currency

- **One active cert today; verify before assuming more.** RCSA is current; RCE is retired. Rubrik may add certifications — check training.rubrik.com before planning.
- **The platform evolves fast.** DSPM and identity resilience are recent additions; RSC capabilities advance, and the RCSA exam follows. Track current features, not a cached list.
- **Access requires Rubrik Support credentials.** Rubrik University is customer/partner-gated; confirm your access route. Verified 4 August 2026.

## Hands-On Lab

### Lab 9.1 — Build your Rubrik certification plan

**Objective:** Commit a route and study plan.

```bash
cat > my-rubrik-plan.md <<'EOF'
Cert: RCSA (Rubrik Certified System Administrator) — the active certification
Route: FREE learning path  /  PAID 4-day RSC Administration bootcamp
Access: obtain Rubrik University access (Rubrik Support credentials)
Study weight (hands-on): SLA Domains + compliance (Ch02), recovery/RTO-RPO (Ch06), workloads (Ch07)
Understand (why): immutability (Ch03), ransomware recovery (Ch04), DSPM (Ch05), identity (Ch08)
Readiness signal: consistently passing the unlimited practice exams -> take the final
Currency: RCE retired; verify current cert list + new platform features on training.rubrik.com
EOF
cat my-rubrik-plan.md
```

**Expected result:** A plan naming the route, the access requirement, and where to weight hands-on time, with the practice-exam readiness signal — the structure this volume follows. The "understand why" line captures the security concepts the exam tests conceptually.

**Negative test:** A plan targeting "RCE" or assuming open access — RCE is retired and Rubrik University needs support credentials; verify both before starting.

**Cleanup:** Keep the plan.

### Lab 9.2 — Currency check

**Objective:** Make re-verification routine.

```bash
cat <<'EOF'
Before relying on this volume, re-check on training.rubrik.com:
  [ ] current certification list (RCSA active? any new certs? RCE still retired?)
  [ ] free vs paid learning path details
  [ ] new RSC platform capabilities (DSPM, identity resilience, threat analytics evolve)
  [ ] Rubrik University access requirements
EOF
echo "verified 4 Aug 2026 — re-verify before scheduling"
```

**Expected result:** A short checklist covering the cert list, study routes, and fast-moving platform features — the currency habits a focused-but-evolving program needs.

**Negative test:** Studying an old feature list — Rubrik ships new security capabilities frequently; training.rubrik.com is authoritative.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A route to RCSA (free vs paid) chosen and access route identified.
- [ ] Study weighted toward operating the platform (SLA/compliance/recovery/workloads).
- [ ] Currency habits installed (RCE retired, fast-evolving platform, gated access).
- [ ] Rubrik placed as the cyber-resilience (data + identity) layer.
