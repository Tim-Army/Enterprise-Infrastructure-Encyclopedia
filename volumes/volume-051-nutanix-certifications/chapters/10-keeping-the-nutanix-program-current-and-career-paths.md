# Chapter 10: Keeping the Nutanix Program Current and Career Paths

## Learning Objectives

- Explain Nutanix certification validity and recertification.
- Track program change — version refreshes and the 3-year validity.
- Plan a Nutanix certification path by role.
- Relate Nutanix credentials to the encyclopedia's virtualization and cloud volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Nutanix certifications are valid for **three years** (since **1 August 2025**, up from
two) and renewed by **passing the current version** of the exam. The program tracks the
platform through **version refreshes** — **7.5** launched for NCA and NCP-MCI in 2026 —
and expands with tracks for automation (NCP-MCA), databases (NCP-DB), unified storage
(NCP-US), and cloud clusters (NCP-CI-AWS/Azure).

## Design Considerations

Plan by **role**: everyone starts at **NCA**; infrastructure admins take **NCP-MCI**
then **NCM-MCI** and ultimately **NCX-MCI**; specialists add **NCP-MCA/DB/US** or the
**NCP-CI** cloud tracks. There are no enforced prerequisites, but higher tiers assume
the lower skill set.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.nutanix.com/support-services/training-certification/certifications" \
  | grep -oiE 'NCA|NCP-[A-Z-]+|NCM-MCI|NCX-MCI|7\.5|6\.10' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
nutanix.com > Training & Certification:
  - valid 3 years (since 1 Aug 2025); recertify by passing the current exam
  - check the current version (NCA/NCP-MCI 7.5) before scheduling
  - download the current blueprint guide
```

Common pitfalls: studying a superseded version; and assuming a two-year validity.

## Security and Best Practices

Recertify by exam within the three-year window, study the **current version**
blueprint, practice on **Community Edition**, and combine credentials for your role
(e.g., NCA → NCP-MCI → NCM-MCI → NCX-MCI). Track version refreshes so content changes
don't surprise you.

## References and Knowledge Checks

- nutanix.com/support-services/training-certification: the program, blueprints, and courses.

**Knowledge checks**

1. How are Nutanix certifications renewed, and for how long are they valid?
2. Which exams refreshed to version 7.5?
3. What path suits an infrastructure administrator?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 10.1–10.2** — a
shell with `curl` and `python3`. **Cost:** none.

### Lab 10.1 — Verify the current versions

**Objective:** Read current certifications and versions from the source.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.nutanix.com/support-services/training-certification/certifications" \
  | grep -oiE '7\.5|6\.10|NCA|NCP-MCI' | sort -u
```

**Expected result:** current versions (**7.5** for NCA/NCP-MCI) — confirming what to
study.

**Negative test:** study a 6.5 blueprint; **7.5** is current for NCA/NCP-MCI — verify.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 10.2 — Plan a path

**Objective:** Map a role to a Nutanix certification sequence.

```bash
python3 - <<'PY'
paths={"Infrastructure Admin":"NCA -> NCP-MCI -> NCM-MCI -> NCX-MCI",
       "Automation":"NCA -> NCP-MCA",
       "Database (DBA)":"NCA -> NCP-DB",
       "Storage":"NCA -> NCP-US",
       "Cloud (NC2)":"NCA -> NCP-CI-AWS / NCP-CI-Azure"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** attempt NCM/NCX first; build up from **NCA → NCP** — the higher
tiers assume the lower skills.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Nutanix certifications are valid three years (since August 2025) and renewed by passing
the current exam version. The program refreshes with the platform (7.5 for NCA/
NCP-MCI) and spans infrastructure, automation, database, storage, and cloud tracks.
Plan a path by role from NCA upward and verify the current version before you study.

- [ ] I can explain validity and recertification.
- [ ] I can identify the current exam versions.
- [ ] I can plan a role-based path from NCA upward.
- [ ] I can verify the current program on nutanix.com.
- [ ] I completed Labs 10.1–10.2 including each negative test.
