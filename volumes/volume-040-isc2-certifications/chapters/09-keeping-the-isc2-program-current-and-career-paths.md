# Chapter 09: Keeping the ISC2 Program Current and Career Paths

## Learning Objectives

- Explain the ISC2 maintenance model: CPE credits, the Annual Maintenance Fee, and the three-year cycle.
- Describe endorsement, the Code of Ethics, and how a credential can be revoked.
- Track program change: exam-outline refreshes, betas, retirements, and the new AI Security certification.
- Plan an ISC2 career path across the ladder and map it to DoD 8140/8570 baselines.
- Verify program currency from the authoritative source.

## Theory and Architecture

An ISC2 credential is a **continuing membership**, not a one-time exam. Three
mechanics keep it active:

- **Continuing Professional Education (CPE)** — earn credits over a **three-year
  cycle** by training, teaching, publishing, volunteering, or earning other
  credentials. Each certification has an annual minimum and a three-year total
  (higher-level credentials require more); concentrations and multiple credentials
  can share some Group A CPEs.
- **Annual Maintenance Fee (AMF)** — a yearly fee that maintains membership; a
  single **combined AMF** covers a member who holds several ISC2 credentials.
- **Endorsement** — after passing, a candidate is **endorsed** by an existing
  ISC2 professional attesting to their experience before the credential is
  conferred; ISC2 can endorse directly if no endorser is available.

Every member agrees to the **ISC2 Code of Ethics** (four canons: protect
society and the infrastructure; act honorably and legally; provide diligent,
competent service; advance the profession). Violations — including using or
sharing **brain dumps** — can lead to **revocation**.

## Design Considerations

Read the program as a **living catalog**. ISC2 refreshes exam outlines on a Job
Task Analysis cycle, and the recent cadence has been brisk:

- **CISSP** refreshed **15 April 2024** (Domain 1 → 16%, Domain 8 → 10%).
- **SSCP** new outline **September 2024**, moved to **CAT** with a new item
  format in 2025.
- **CGRC** refreshed **15 June 2024** (privacy added throughout).
- **ISSAP, ISSEP, ISSMP** all **re-issued 1 August 2025** with new domain counts
  and weights — a major concentration overhaul.
- **CCSP** new outline **effective 1 August 2026**.
- **CC** new outline **effective 1 September 2026**.
- A brand-new **AI Security certification is in development** (details pending) —
  ISC2's response to securing and governing AI systems, worth watching for
  candidates on the architecture and governance tracks.

The naming has changed too: **CAP → CGRC**, and the organization's own styling
moved from **(ISC)²** to **ISC2**; **HCISPP** was retired. Do not trust
older material on names, domains, or weights without checking the live outline.

## Implementation and Automation

Verify currency from **isc2.org** — the exam-outline hub carries each
credential's current effective date:

```bash
# Effective date for a given credential's current outline
for c in cissp ccsp sscp cgrc csslp; do
  d=$(curl -sSL -A "Mozilla/5.0" \
    "https://www.isc2.org/certifications/$c/${c}-certification-exam-outline" \
    | grep -oiE 'Effective[^<]{0,40}20[0-9]{2}' | head -1)
  printf '%-6s %s\n' "$c" "${d:-check-page}"
done
```

## Validation and Troubleshooting

Confirm program facts before committing study time or a renewal decision:

```text
isc2.org:
  - Certifications > Exam Outlines: current outline + effective date per credential
  - Member resources: CPE Handbook (annual + 3-year requirements), AMF amount
  - Code of Ethics: the four canons and the complaint/revocation process
  - News/Insights: betas, refreshes, and the AI Security certification
```

Common pitfalls: letting a credential **suspend** by missing CPE or the AMF
deadline (a grace period exists, then the credential lapses and may require
re-exam); studying a **superseded outline**; and assuming a **beta** exam's
content or price matches the eventual GA.

## Security and Best Practices

Record CPEs **as you earn them**, not at renewal; keep evidence for audit. Pay a
**combined AMF** if you hold multiple credentials. Never touch **brain dumps** —
they violate the Code of Ethics and can revoke every credential you hold. Plan
the ladder deliberately: **CC → SSCP → CISSP**, then branch to **CCSP** (cloud),
**CSSLP** (software), **CGRC** (authorization), or the **ISSAP/ISSEP/ISSMP**
concentrations (architecture/engineering/management). Many ISC2 credentials
satisfy **DoD 8140/8570** baselines — SSCP (IAT II), CISSP (IAT/IAM III, IASAE),
CCSP (cloud), CGRC (RMF roles) — useful for defense and regulated careers.

## References and Knowledge Checks

- isc2.org: *CPE Handbook*; *Annual Maintenance Fees*; *Code of Ethics*; *Exam Outlines*; *Insights* (program news).

**Knowledge checks**

1. What are the three mechanics that keep an ISC2 credential active?
2. Which ISC2 credentials had outline changes in 2024–2026, and what is coming?
3. How can a credential be revoked, and what common practice triggers it?

## Hands-On Lab

Exam-preparation walkthroughs for tracking program change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a Linux shell with `curl` and
`python3`. **Cost:** none.

### Lab 9.1 — Detect an outline refresh (Topic: Verify currency)

**Objective:** Read the current effective date across credentials in one pass.

```bash
for c in cissp ccsp sscp cgrc csslp issap issep issmp; do
  d=$(curl -sSL -A "Mozilla/5.0" \
    "https://www.isc2.org/certifications/$c/${c}-certification-exam-outline" \
    | grep -oiE 'Effective[^<]{0,40}20[0-9]{2}' | head -1)
  printf '%-6s %s\n' "$c" "${d:-check-page}"
done
```

**Expected result:** an effective date per credential — flagging the 2025
concentration refresh and the 2026 CCSP/CC changes so you never study a
superseded outline.

**Negative test:** trust a course's "updated 2022" label; outlines changed since
— confirm against isc2.org.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a CPE-compliant renewal (Topic: Maintain the credential)

**Objective:** Check whether a CPE plan meets a three-year requirement.

```bash
python3 - <<'PY'
required_3yr = 120        # e.g., CISSP total over the cycle
annual_min   = 40
plan = [45, 40, 45]       # CPEs earned each year
print("Yearly >= min?", all(x>=annual_min for x in plan))
print("3-year total:", sum(plan), ">= required", required_3yr, "->", sum(plan)>=required_3yr)
PY
```

**Expected result:** both checks `True` — a compliant CISSP-style renewal (annual
minimum met each year and the three-year total satisfied).

**Negative test:** back-load all CPEs into year three; ISC2 requires an **annual
minimum** as well as the total — pace the credits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

An ISC2 credential is a multi-year professional commitment maintained by CPE
credits, the Annual Maintenance Fee, and adherence to the Code of Ethics, with
endorsement required to certify. The program changes continually — CISSP (2024),
SSCP (2024–25), CGRC (2024), the ISSAP/ISSEP/ISSMP concentrations (2025), and
CCSP and CC refreshes in 2026, plus a new AI Security certification in
development. Plan the ladder deliberately and map it to DoD 8140 where relevant.

- [ ] I can explain CPE, the AMF, and endorsement.
- [ ] I can name the four canons of the Code of Ethics and how a credential is revoked.
- [ ] I can list the recent and upcoming outline changes and the AI Security cert.
- [ ] I can verify a current effective date and plan a compliant renewal.
- [ ] I completed Labs 9.1–9.2 including each negative test.
