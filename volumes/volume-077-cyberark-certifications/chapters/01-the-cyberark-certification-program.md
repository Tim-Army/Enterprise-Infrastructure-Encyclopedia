# Chapter 01: The CyberArk Certification Program

## Learning Objectives

- Explain CyberArk's role in Privileged Access Management (PAM) and Identity Security.
- Describe the Trustee → Defender → Sentry → Guardian certification progression.
- Understand the Pearson VUE exam model and prerequisites.
- Map credentials to roles and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**CyberArk** is the leading **Privileged Access Management (PAM)** and **Identity Security** vendor —
its platform protects the most dangerous credentials in an organization: the **privileged accounts**
(administrators, service accounts, secrets) that, if abused, grant attackers control. CyberArk's
certification program validates the people who deploy and operate this platform, in a progression:
**Trustee** (foundational concepts and platform basics), **Defender** (daily maintenance and
operation), **Sentry** (deployment, installation, and configuration — prerequisite Defender), and
**Guardian** (the highest credential — advanced skills across solutions plus Identity Security
architecture and strategy). A **Certified Delivery Engineer (CDE)** track serves implementation
partners. Exams are delivered through **Pearson VUE** (proctored). The credentials span CyberArk's
products — **PAM Self-Hosted**, **Privilege Cloud**, **Endpoint Privilege Manager (EPM)**, **Secrets
Manager**, **Identity**, and **Secure Cloud Access**. Because PAM exists to **defend** privileged
access, this entire volume is defensive administration.

> **Currency note.** As of 2026, CyberArk operates as **part of Palo Alto Networks**, and the
> platform is progressively rebranding toward **"Idira."** The component architecture (Vault, CPM,
> PVWA, PSM) and the **Defender/Sentry/Guardian** credential names are **unchanged**. Verify current
> exam names, delivery, and prerequisites on cyberark.com.

The scope of this volume is strictly defensive:

> **Scope.** Privileged Access Management is a defensive discipline. Every lab is **authorized
> administration** — securing, rotating, isolating, monitoring, and governing privileged access —
> never an attack on a credential store.

## Design Considerations

Climb **Trustee → Defender → Sentry** for operational and deployment depth, then **Guardian** for
architecture. Add **product-specific** Defenders (EPM, Privilege Cloud) as your environment needs.
Respect **prerequisites** (Sentry requires Defender). Verify current exam names on cyberark.com — the
platform is evolving under Palo Alto Networks.

## Implementation and Automation

Confirm your practice toolset (used throughout the volume):

```bash
command -v python3 >/dev/null && echo "python3: ok" || echo "python3: install for labs"
echo "Practice on an authorized CyberArk lab/trial; never a production Vault"
```

## Validation and Troubleshooting

The verified program facts (cyberark.com + Pearson VUE, 28 July 2026):

```text
Progression: Trustee -> Defender (operate) -> Sentry (deploy/configure; prereq Defender) -> Guardian (architect/expert). Also CDE (partners).
Platform: PAM Self-Hosted (Vault/CPM/PVWA/PSM/PTA), Privilege Cloud, EPM, Secrets Manager, Identity, Secure Cloud Access. Delivery: Pearson VUE.
2026: CyberArk is part of Palo Alto Networks; rebranding toward "Idira"; architecture + credential names unchanged.
```

Common pitfalls: attempting **Sentry** before **Defender** (prerequisite); and assuming the Palo Alto
acquisition changed the exams (credential names/architecture are unchanged — verify on cyberark.com).

## Security and Best Practices

Learn the **current** progression on cyberark.com, respect **prerequisites**, and practice on an
**authorized lab**, never production. Treat privileged credentials as the crown jewels. All work is
defensive.

## References and Knowledge Checks

- cyberark.com/services-support/training-certification: the levels, products, and exam model.
- Pearson VUE: exam scheduling and delivery.

**Knowledge checks**

1. What does CyberArk's platform protect?
2. Name the certification progression in order.
3. What is Sentry's prerequisite?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a workstation with `python3`,
in a lab. **Cost:** none.

### Lab 1.1 — Map the PAM platform

**Objective:** Learn the products.

```python
python3 - <<'PY'
platform={"PAM Self-Hosted":"Vault + CPM + PVWA + PSM + PTA (on-prem privileged access)",
          "Privilege Cloud":"SaaS PAM","EPM":"endpoint least privilege / elevation",
          "Secrets Manager":"app & CI/CD secrets (Conjur, Credential Providers)",
          "Identity":"workforce/customer identity","Secure Cloud Access":"cloud entitlements (JIT/ZSP)"}
for prod,scope in platform.items(): print(f"{prod:18}: {scope}")
PY
```

**Expected result:** the CyberArk **product map** — the platform this volume covers.

**Negative test:** think CyberArk is only the Vault; it spans **endpoints, secrets, identity, and
cloud** — use the full map.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map credentials to the progression

**Objective:** Record the ladder.

```python
python3 - <<'PY'
prog=[("Trustee","foundational concepts + platform basics"),
      ("Defender","daily maintenance & operation (e.g., PAM-DEF)"),
      ("Sentry","deploy/install/configure — prereq Defender (e.g., PAM-SEN)"),
      ("Guardian","advanced + architecture + Identity Security strategy")]
for name,note in prog: print(f"{name:10}: {note}")
print("Also: CDE (Certified Delivery Engineer) for implementation partners")
PY
```

**Expected result:** the **Trustee→Defender→Sentry→Guardian** progression — your scheduling
reference.

**Negative test:** target **Guardian** first; it assumes deep Defender/Sentry experience — climb the
progression.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"PAM operator":"Trustee -> Defender (PAM)","PAM engineer":"Defender -> Sentry (PAM)",
       "Endpoint least privilege":"Defender - EPM","Secrets/DevOps":"Defender + Secrets Manager focus",
       "PAM architect":"Sentry -> Guardian"}
for role,path in paths.items(): print(f"{role:26}: {path}")
PY
```

**Expected result:** role-to-path sequences — the progression this volume follows.

**Negative test:** skip **Trustee/Defender** foundations and jump to deployment; Sentry assumes
operational fluency — build up.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CyberArk certifies PAM and Identity Security practitioners in a Trustee → Defender → Sentry → Guardian
progression across the Vault, Privilege Cloud, EPM, Secrets Manager, Identity, and Secure Cloud
Access — delivered by Pearson VUE, now under Palo Alto Networks — taught here as defensive privileged-
access administration.

- [ ] I can explain what CyberArk protects.
- [ ] I can name the certification progression.
- [ ] I can state Sentry's prerequisite.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
