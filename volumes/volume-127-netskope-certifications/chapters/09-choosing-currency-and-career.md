# Chapter 09: Choosing a Path, Currency, and Career

## Learning Objectives

- Choose and sequence the Netskope credentials (SASE Accreditation → NCCSA → NCCSI) for your role.
- Build a study plan grounded in the platform's SSE pillars.
- Keep certifications current through exam-code churn and platform evolution.

## Choosing a path

| If your role is… | Start with | Then |
|:---|:---|:---|
| Anyone learning SASE (vendor-neutral) | **SASE Accreditation** (free) | — |
| Security/cloud admin operating Netskope | SASE Accreditation | **NCCSA** (NSK101) |
| Integration engineer / architect | NCCSA | **NCCSI** |
| SOC / detection engineer | NCCSA | NCCSI (API/analytics focus) |

The spine: the **free, vendor-agnostic SASE Accreditation** grounds you in the framework; **NCCSA** proves you can administer the platform; **NCCSI** proves you can integrate it into the enterprise (identity, API, posture, analytics). The SASE Accreditation is worth taking even if you never touch Netskope — it teaches SASE as an architecture.

## Study approach

| Credential | Volume chapters | Prep |
|:---|:---|:---|
| SASE Accreditation | [02](02-sase-accreditation-architecture.md) | free on-demand course; 45-min exam, 80% |
| NCCSA (NSK101) | [03](03-nccsa-platform-and-steering.md)–[07](07-nccsa-ztna-private-access.md) | Netskope One Administrator course; Pearson VUE, 70 Q / ~2 hr / 70% |
| NCCSI | [08](08-nccsi-integration-and-operations.md) | Netskope One Professional course; Pearson VUE |

The NCCSA spans the SSE pillars — steering, CASB, SWG, DLP, ZTNA — so budget lab time across all five; this volume's free-primitive labs make each concrete before the vendor course. NCCSI adds the integration surfaces (SAML, API, IaaS/SSPM, analytics).

## The SASE/SSE context

Netskope sits in a crowded, fast-moving SASE/SSE market. This volume pairs with the other cloud-security-edge coverage in the encyclopedia:

- [Volume XXXV — Zscaler Zero Trust Exchange](../../volume-035-zscaler-zero-trust-exchange/README.md) — the neighboring SSE/SASE platform and its certifications.
- [Volume XVI — Palo Alto Networks Security](../../volume-016-palo-alto-networks-security/README.md) and [Volume LXV — Palo Alto Certification Tracks](../../volume-065-palo-alto-networks-certifications/README.md) — Prisma Access SASE.
- [Volume XIX — Fortinet Network Security](../../volume-019-fortinet-network-security/README.md) — FortiSASE.
- [Volume X — Enterprise Cybersecurity](../../volume-010-enterprise-cybersecurity/README.md) — the broader defensive program.

Knowing where Netskope's model (rich CASB granularity, NewEdge, single policy engine) differs from Zscaler's or Palo Alto's is exactly the comparative judgment these certifications build.

## Currency

- **Exam codes churn.** NSK100 → NSK101 already happened; the NCCSI exam code and the SASE Accreditation's free window can change. **Re-verify on netskope.com before booking.**
- **"Netskope One" branding.** The platform consolidated under **Netskope One**; older material says "Netskope Security Cloud." Course names (Netskope One Administrator/Professional) track the current branding.
- **Two-year validity.** NCCSA is valid **2 years** — plan recertification; confirm NCCSI's validity on netskope.com.
- **The market moves.** SASE/SSE features (AI/ML data classification, GenAI app controls, SSPM scope) expand quickly; the exams follow. Track the current Netskope One capabilities, not a cached feature list.

## Hands-On Lab

### Lab 9.1 — Build your Netskope certification plan

**Objective:** Commit a role-aligned plan.

```bash
cat > my-netskope-plan.md <<'EOF'
Role: admin / integrator / architect / SOC
Step 1: SASE Accreditation (free, vendor-agnostic)          target: ___
Step 2: NCCSA — NSK101 (Pearson VUE, 70Q/~2hr/70%/2yr)      course: Netskope One Administrator
        weak pillars: steering / CASB / SWG / DLP / ZTNA -> ___
Step 3: NCCSI (integration: SAML/API/IaaS-SSPM/analytics)   course: Netskope One Professional
Re-verify exam codes on netskope.com before booking (NSK100->NSK101 churn).
Recert: NCCSA every 2 years.
EOF
cat my-netskope-plan.md
```

**Expected result:** A plan naming the current exam code, the five NCCSA pillars to shore up, and the re-verify/recert steps — the discipline exam-code churn and 2-year validity demand.

**Negative test:** A plan pinned to "NSK100" or an assumed free window — both have moved; the plan must re-verify against netskope.com.

**Cleanup:** Keep the plan.

### Lab 9.2 — Currency check

**Objective:** Make re-verification routine.

```bash
cat <<'EOF'
Before booking, on netskope.com:
  [ ] current NCCSA exam code (NSK101? successor?) and NCCSI code
  [ ] SASE Accreditation still free / on-demand availability
  [ ] Netskope One course names + any new certification tier
  [ ] validity periods (NCCSA = 2 yr)
EOF
echo "verified 3 Aug 2026 — re-verify before scheduling"
```

**Expected result:** A short pre-booking checklist covering the code churn, free-window, and branding changes — the currency habit for a fast-moving SASE vendor.

**Negative test:** Trusting a third-party site's exam code or "free forever" claim — both drift; netskope.com is authoritative.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Path chosen and sequenced (SASE Accreditation → NCCSA → NCCSI).
- [ ] Study plan committed across the five NCCSA pillars plus NCCSI integration.
- [ ] Currency habits installed: re-verify exam codes/free-window on netskope.com; recert NCCSA at 2 years.
- [ ] Netskope placed within the SASE/SSE market (Zscaler, Palo Alto, Fortinet).
