# Chapter 09: Keeping the Snowflake Program Current and Career Paths

## Learning Objectives

- Explain Snowflake certification validity and recertification.
- Track program change — the COF-C03 Core refresh, the Associate tier, and Cortex AI.
- Plan a SnowPro career path from Core to Advanced.
- Relate Snowflake credentials to the encyclopedia's data and cloud volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Snowflake certifications are valid for **two years** and renewed by **passing a
recertification exam** (or a higher/newer exam), since the platform evolves quickly.
The program changes with the platform: **SnowPro Core moved from COF-C02 to
COF-C03** (16 February 2026), a **SnowPro Associate: Platform** entry tier was
added, and **Cortex** AI content now features across exams under the **AI Data
Cloud** branding.

## Design Considerations

Plan a path by **role**: **Core** first (the required foundation), then a **SnowPro
Advanced** exam for your role — Architect, Data Engineer, Data Analyst, Data
Scientist, or Administrator. The **Associate** is an optional on-ramp. Confirm the
current **exam code** (Core is COF-C03) so you study the live version.

## Implementation and Automation

Verify currency from **learn.snowflake.com/certifications** — the pages carry the
current codes and guides:

```bash
curl -sSL -A "Mozilla/5.0" "https://learn.snowflake.com/en/certifications/" \
  | grep -oiE 'SnowPro (Associate|Core|Advanced)[^<]{0,30}|COF-C0[0-9]|[A-Z]{3}-C0[0-9]' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
learn.snowflake.com/certifications:
  - current exam codes and guides (verify Core = COF-C03)
  - Advanced exams require Core; two-year validity
Watch for AI Data Cloud / Cortex additions and new tiers.
```

Common pitfalls: studying **COF-C02**; attempting Advanced without **Core**; and
letting a credential lapse (recertify by exam).

## Security and Best Practices

Recertify by exam within the two-year window. Practice on the **free trial** with
current features (Cortex, Snowpark, governance). Combine Core + an Advanced role
exam for your target job. Track platform changes so guide revisions don't surprise
you.

## References and Knowledge Checks

- learn.snowflake.com/certifications: the catalog, per-exam guides, and recertification policy.

**Knowledge checks**

1. How are Snowflake certifications renewed?
2. What changed with the COF-C03 Core refresh?
3. What is the required foundation for the Advanced exams?

## Hands-On Lab

Exam-preparation walkthroughs for tracking change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a shell with `curl` and `python3`.
**Cost:** none.

### Lab 9.1 — Verify current exam codes (Topic: Verify currency)

**Objective:** Read the current SnowPro exams from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://learn.snowflake.com/en/certifications/" \
  | grep -oiE 'COF-C0[0-9]' | sort -u
```

**Expected result:** the current Core code (**COF-C03**) — confirming COF-C02 is
retired.

**Negative test:** trust a course citing COF-C02; the current Core is **COF-C03** —
confirm on learn.snowflake.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a path (Topic: Career)

**Objective:** Map a role to a SnowPro sequence.

```bash
python3 - <<'PY'
paths = {"Data Engineer":"Core -> Advanced Data Engineer",
         "Architect":"Core -> Advanced Architect",
         "Administrator":"Core -> Advanced Administrator",
         "Analyst/Scientist":"Core -> Advanced Data Analyst / Data Scientist"}
for role,path in paths.items(): print(f"{role:18}: {path}")
PY
```

**Expected result:** role-to-path sequences (Core → Advanced) — the career mapping
this volume supports.

**Negative test:** attempt an Advanced exam first; **Core is required** — earn it
before Advanced.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Snowflake certifications are valid two years and renewed by exam, tracking a
fast-evolving AI Data Cloud. Core moved to COF-C03, an Associate tier was added,
and Cortex AI features across the exams. Plan a path from Core to a role-based
Advanced exam, practice on the free trial, and verify the current code.

- [ ] I can explain Snowflake certification validity and renewal.
- [ ] I can confirm the current Core code (COF-C03) and the Associate tier.
- [ ] I can plan a Core → Advanced path by role.
- [ ] I can verify the current catalog on learn.snowflake.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
