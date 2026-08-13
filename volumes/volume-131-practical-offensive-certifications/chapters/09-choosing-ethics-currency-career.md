# Chapter 09: Choosing a Path, Ethics and Authorization, and Career

## Learning Objectives

- Choose and sequence practical certifications across HTB, TCM, and INE for your role.
- Reinforce the ethical and legal core: authorization governs everything.
- Keep skills current, and place these certs among the encyclopedia's other security programs.

## Choosing a path

All three providers offer practical, hands-on paths; choose by role and budget:

| If your goal is… | Practical entry | Then |
|:---|:---|:---|
| Break into security (foundation) | INE **eJPT** or HTB **CJCA** or TCM **PJPT** | CPTS / PNPT / eCPPT |
| Penetration tester | HTB **CPTS** / TCM **PNPT** / INE **eCPPT** | AD (**CAPE**), web (**CWES/CWEE/eWPTX**) |
| Web/app security | HTB **CWES** → **CWEE**; INE **eWPT** → **eWPTX**; TCM **PWPA→PWPP→PWPE** | secure coding review |
| SOC analyst / blue team | HTB **CDSA** / TCM **PSAA→PSAP** / INE **eSOC** | IR (**eCIR**), hunting (**eCTHP**), forensics (**eCDFP**) |
| AI security | HTB **COAE** / TCM **PAPA** / INE **eAIS** | — |
| OSINT / specialist | TCM **PORP** (OSINT), **PIPA** (IoT), **PMPA** (mobile) / INE **eMAPT** | — |

The providers differ in flavor: **TCM** is affordable and scenario-realistic (non-proctored, free retake, learning-path bundles); **HTB** is module-rich and job-role-mapped; **INE** (eLearnSecurity heritage) pairs subscription training with hand-graded exams. Many practitioners mix them. A common, cost-effective ladder: **eJPT/CJCA (foundation) → CPTS/PNPT (core) → a specialty (CAPE / CWEE / CDSA)**.

## Ethics and authorization — the career's foundation

This bears repeating as the volume closes: **the single most important thing these certifications teach is that authorization governs everything.** The technical skills are valuable only within a lawful, authorized, in-scope context — your lab, a sanctioned exam range, or a signed engagement. The same skill set is a respected profession *or* a crime, and the only difference is authorization. Every reputable program (these three, plus [OffSec XLIII](../../volume-043-offensive-security-certifications/README.md), [GIAC LXXIV](../../volume-074-giac-certifications/README.md), [EC-Council LXXV](../../volume-075-ec-council-certifications/README.md)) makes this explicit, and so does this volume.

## The context in the encyclopedia

These practical certs complement the encyclopedia's other security programs:

- **Offensive/authorized-testing peers:** [OffSec XLIII](../../volume-043-offensive-security-certifications/README.md) (OSCP+ and the practical-exam pioneer), [EC-Council LXXV](../../volume-075-ec-council-certifications/README.md) (CEH), [GIAC LXXIV](../../volume-074-giac-certifications/README.md) (SANS).
- **Governance/knowledge peers:** [ISC2 XL](../../volume-040-isc2-certifications/README.md) (CISSP), [CompTIA XXXIX](../../volume-039-comptia-certification-tracks/README.md) (Security+/PenTest+).
- **The broader program:** [Enterprise Cybersecurity X](../../volume-010-enterprise-cybersecurity/README.md).

Their distinctive contribution is the **practical, prove-it-by-doing** assessment model — and, uniquely in this batch, spanning red *and* blue with the same hands-on rigor.

## Currency

- **These programs move fast.** New certs appear frequently (the AI ones — COAE/PAPA/eAIS — are recent); exam labs and modules update. Verify the current catalog on each provider's site before planning.
- **Practical validity.** Some (e.g. HTB) tie certs to versioned material; check whether/when re-validation applies. TCM/INE include free retakes.
- **The law is jurisdictional and evolving.** Authorization requirements and computer-misuse law vary by country; know your local law, and never rely on "it was for learning" as a defense for unauthorized testing. Verified 4 August 2026.

## Hands-On Lab

### Lab 9.1 — Build your practical-cert plan

**Objective:** Commit a role-aligned, ethical plan.

```bash
cat > my-practical-cert-plan.md <<'EOF'
Goal: entry / pentester / web / blue-team / AI-security / specialist
Foundation: eJPT  /  HTB CJCA  /  TCM PJPT           target: ___
Core:       HTB CPTS  /  TCM PNPT  /  INE eCPPT       target: ___
Specialty:  CAPE(AD) / CWEE(web) / CDSA(blue) / COAE(AI) / eCTHP(hunt) ...
Practice ONLY in: the provider's sanctioned exam range / my own isolated lab VMs
Authorization rule: signed, in-scope permission before ANY test of a system I don't own
Currency: verify each provider's current catalog before scheduling
EOF
cat my-practical-cert-plan.md
```

**Expected result:** A plan pairing a role-aligned cert ladder with the **authorization rule stated explicitly** — the ethical frame that must accompany the technical plan. The "practice only in sanctioned ranges" line is not boilerplate; it's the boundary that makes the whole endeavor lawful.

**Negative test:** A skills plan with no authorization discipline — the skills are only professionally usable within legal, authorized bounds; the plan is incomplete without it.

**Rollback:** Keep the plan.

### Lab 9.2 — The authorization self-check

**Objective:** Internalize the pre-action question that governs a security career.

```bash
python3 - <<'EOF'
def may_i_test(i_own_it, signed_scope, in_scope, within_window):
    if i_own_it: return "YES — your own isolated lab"
    if signed_scope and in_scope and within_window: return "YES — authorized, in-scope, in-window engagement"
    return "NO — do not proceed (unauthorized or out-of-scope = illegal)"
print("my home lab VM:        ", may_i_test(True, False, False, False))
print("client, signed+in-scope:", may_i_test(False, True, True, True))
print("interesting site online:", may_i_test(False, False, False, False))
EOF
```

**Expected result:** Your own lab and a signed, in-scope, in-window engagement are YES; an "interesting site online" is **NO**. This self-check is the reflex every practitioner these certs produce must have: **before any action, confirm authorization.** It's the difference between the profession and a crime, and the most important thing this volume — and these certifications — convey.

**Negative test:** Rationalizing an unauthorized test ("just looking," "for research") — the authorization self-check returns NO, and so does the law; there is no exception.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A role-aligned path across HTB/TCM/INE chosen (foundation → core → specialty).
- [ ] The authorization-governs-everything ethic internalized as the career's foundation.
- [ ] These practical certs placed among the encyclopedia's other security programs.
- [ ] Currency habits installed (fast-moving catalogs, jurisdictional law).
