# Chapter 09: CMMC Roles, Certificates, and Keeping Current

## Learning Objectives

- Describe the ISACA-administered CMMC ecosystem roles.
- Explain ISACA's certificate programs and how they differ from certifications.
- Explain the CPE maintenance model, annual fees, and experience verification.
- Track program change — the AI family, CCOA, and outline refreshes.
- Plan an ISACA career path and verify program currency.

## Theory and Architecture

Beyond its certifications, ISACA administers two further kinds of credential:

- **CMMC ecosystem roles** — ISACA is an authorized body for the U.S. **Cybersecurity
  Maturity Model Certification (CMMC)** program, offering the assessor and trainer
  roles: **CCP** (CMMC Certified Professional), **CCA** (CMMC Certified Assessor),
  **LCCA** (Lead CMMC Certified Assessor), and **CCI** (CMMC Certified Instructor).
  These certify people to assess defense-contractor compliance with CMMC.
- **Certificate programs** — shorter, exam-based **certificates** (not
  certifications): **COBIT Foundation** and **Design & Implementation**, and
  **Fundamentals** certificates in IT Audit, IT Risk, Cybersecurity Audit, AI,
  Cloud, Data Science, Blockchain, IoT, and more. Certificates prove focused
  knowledge and do not require CPE maintenance the way certifications do.

**Certifications** (CISA, CISM, CRISC, CGEIT, CDPSE, CCOA, the AI family) require
**experience verification** and ongoing **CPE**; **certificates** are standalone.

## Design Considerations

Use **certificates** to build or demonstrate focused knowledge quickly (COBIT for
governance, the Fundamentals series to explore a domain), and **certifications**
for career-defining, experience-backed credentials. The **CMMC roles** are for
professionals working in the U.S. defense industrial base. Sequence a path by
role, and treat **CPE** as continuous from the day a certification is earned.

## Implementation and Automation

Maintain certifications by recording CPE and paying the annual maintenance fee.
Verify currency from isaca.org — outlines and the catalog change (the Advanced in
AI family and CCOA are recent, CDPSE and CRISC were refreshed in 2025).

```bash
# Effective/updated signals for a credential's current outline
curl -sSL -A "Mozilla/5.0" \
  "https://www.isaca.org/credentialing/cdpse/cdpse-exam-content-outline" \
  | grep -oiE 'Domain [0-9][^<]{0,50}[0-9]{1,2}%' | head
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
isaca.org:
  - Credentialing: certifications, CCOA, the Advanced in AI family, CMMC roles, certificates
  - each certification's Exam Content Outline + effective/update date
  - CPE policy and annual maintenance fee
```

Common pitfalls: confusing a **certificate** (no CPE) with a **certification**
(CPE + experience); missing the new **AI family** and **CCOA**; and letting a
certification lapse by neglecting **CPE**.

## Security and Best Practices

Record CPE as you earn it; pay the annual maintenance fee on time; keep evidence
for audit. Choose credentials by the role you want — audit (CISA), security
management (CISM), risk (CRISC), governance (CGEIT), privacy (CDPSE), operations
(CCOA), AI (AAIA/AAISM/AAIR), or CMMC assessment — rather than collecting them.
ISACA credentials pair naturally with ISC2's for a complete governance-and-
management portfolio.

## References and Knowledge Checks

- isaca.org: *Credentialing* catalog; *CPE policy*; *CMMC* program; *COBIT*.

**Knowledge checks**

1. How do ISACA certificates differ from certifications?
2. What are the ISACA-administered CMMC roles?
3. Which credentials and outlines changed most recently?

## Hands-On Lab

Exam-preparation walkthroughs for tracking change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a Linux shell with `curl` and
`python3`. **Cost:** none.

### Lab 9.1 — Detect an outline refresh (Topic: Verify currency)

**Objective:** Confirm the current domain structure across credentials.

```bash
for c in cisa cism crisc cgeit cdpse; do
  n=$(curl -sSL -A "Mozilla/5.0" \
     "https://www.isaca.org/credentialing/$c/${c}-exam-content-outline" \
     | grep -oiE 'Domain [0-9]' | sort -u | wc -l | tr -d ' ')
  printf '%-6s domains: %s\n' "$c" "$n"
done
```

**Expected result:** a domain count per credential — flagging CDPSE's move to
**four** domains (2025) so you never study a superseded outline.

**Negative test:** trust an old study guide's domain list; CDPSE and CRISC changed
in 2025 — confirm against isaca.org.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a CPE-compliant renewal (Topic: Maintain the credential)

**Objective:** Check a CPE plan against ISACA's requirement.

```bash
python3 - <<'PY'
required_3yr = 120     # ISACA certification 3-year requirement
annual_min   = 20
plan = [40, 40, 45]
print("Annual >= 20 each year?", all(x>=annual_min for x in plan))
print("3-year total:", sum(plan), ">= 120 ->", sum(plan)>=required_3yr)
PY
```

**Expected result:** both checks `True` — a compliant renewal (annual minimum 20
and 120 over three years), the CPE model ISACA uses.

**Negative test:** back-load all CPE into year three; ISACA requires an **annual
minimum** as well as the total — pace the credits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Beyond its certifications, ISACA administers the CMMC assessor/trainer roles (CCP,
CCA, LCCA, CCI) and a broad catalog of certificates (COBIT and the Fundamentals
series). Certifications require experience verification and CPE; certificates are
standalone. The program changes — the Advanced in AI family and CCOA are recent,
and CDPSE/CRISC were refreshed in 2025 — so verify outlines before studying and
maintain CPE to keep credentials active.

- [ ] I can distinguish ISACA certificates from certifications.
- [ ] I can name the ISACA-administered CMMC roles.
- [ ] I can list the recent additions and refreshes.
- [ ] I can verify a current outline and plan a compliant CPE renewal.
- [ ] I completed Labs 9.1–9.2 including each negative test.
