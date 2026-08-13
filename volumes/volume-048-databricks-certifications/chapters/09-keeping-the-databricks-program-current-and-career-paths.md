# Chapter 09: Keeping the Databricks Program Current and Career Paths

## Learning Objectives

- Explain Databricks certification validity and recertification.
- Track program change — the new GenAI/Context Engineer certs and platform evolution.
- Plan a Databricks career path across the role-based certifications.
- Relate Databricks credentials to the encyclopedia's data and AI volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Databricks certifications are valid for a defined period (commonly **two years**)
and renewed by **retaking the current exam**, since the platform and exam guides
evolve quickly. Free **accreditations** (Fundamentals, Platform
Architect/Administrator) refresh on their own cadence. The program is expanding
toward **AI and agents** — the **Generative AI Engineer** and **Context Engineer**
certifications and the **AI Agent Fundamentals** accreditation are recent — while
the **Hadoop Migration Architect** certification was retired (1 August 2024).

## Design Considerations

Plan a path by **role**, starting from the free **Fundamentals**:

- **Analytics:** Data Analyst Associate.
- **Data engineering:** Data Engineer Associate → Professional.
- **Machine learning:** Machine Learning Associate → Professional.
- **AI/agents:** Generative AI Engineer Associate and Context Engineer Associate.
- **Foundation:** Apache Spark Developer Associate underpins all of them.

Confirm the current **exam guide** before studying, since Databricks revises guides
as the platform changes (e.g., DLT → Lakeflow, Feature Store → Feature Engineering
in Unity Catalog).

## Implementation and Automation

Verify currency from **databricks.com/learn/certification** — the catalog and
per-exam guides carry the current lineup and sections:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.databricks.com/learn/certification" \
  | grep -oiE '(Data Analyst|Data Engineer|Machine Learning|Generative AI Engineer|Context Engineer|Apache Spark Developer)' \
  | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
databricks.com/learn/certification:
  - current certifications and per-exam guides (sections)
  - accreditations (free) vs certifications (proctored)
  - validity and recertification terms
Watch for AI-focused additions (GenAI Engineer, Context Engineer).
```

Common pitfalls: studying a **retired guide**; letting a credential lapse (renew by
exam); and skipping the free **Fundamentals**/accreditations that scaffold the
certs.

## Security and Best Practices

Renew by re-exam within the validity window. Keep practicing on **Free/Community
Edition** with current platform features (Unity Catalog, Lakeflow, Mosaic AI).
Combine credentials for a role (e.g., Data Engineer Professional + ML Associate for
an ML platform engineer). Track platform renames so guide changes don't surprise
you.

## References and Knowledge Checks

- databricks.com/learn/certification: the catalog, per-exam guides, and recertification policy; Databricks Academy.

**Knowledge checks**

1. How are Databricks certifications renewed?
2. Which certifications are recent AI-focused additions?
3. What is a sensible path from Fundamentals to a data-engineering role?

## Hands-On Lab

Exam-preparation walkthroughs for tracking change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a shell with `curl` and `python3`.
**Cost:** none.

### Lab 9.1 — Verify the current catalog (Topic: Verify currency)

**Objective:** Read the current certifications from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.databricks.com/learn/certification" \
  | grep -oiE '(Data Analyst|Data Engineer|Machine Learning|Generative AI Engineer|Context Engineer|Apache Spark Developer)[^<]{0,15}(Associate|Professional)?' \
  | sort -u
```

**Expected result:** the current role-based certifications, including the new
**Generative AI Engineer** and **Context Engineer** — confirming what an old map
misses.

**Negative test:** trust a 2024 Databricks cert chart; it predates the GenAI/
Context Engineer certs and the Hadoop Migration Architect retirement — confirm on
databricks.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a path (Topic: Career)

**Objective:** Map a role to a Databricks credential sequence.

```bash
python3 - <<'PY'
paths = {"Data Engineer":"Fundamentals -> DE Associate -> DE Professional",
         "ML Engineer":"Fundamentals -> ML Associate -> ML Professional",
         "GenAI Engineer":"GenAI Fundamentals -> Generative AI Engineer -> Context Engineer",
         "Analyst":"Fundamentals -> Data Analyst Associate"}
for role,path in paths.items(): print(f"{role:15}: {path}")
PY
```

**Expected result:** role-to-path sequences from the free Fundamentals to the
role-based certs — the career mapping this volume supports.

**Negative test:** expect CE credits to renew certifications; Databricks renews **by
exam** — plan to re-test.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Databricks certifications are valid ~two years and renewed by exam, reflecting a
fast-evolving platform. The program is expanding toward AI and agents (Generative
AI Engineer, Context Engineer) and retired the Hadoop Migration Architect. Plan a
path by role from the free Fundamentals, practice on Free/Community Edition, and
verify the current exam guide before studying.

- [ ] I can explain Databricks certification validity and renewal.
- [ ] I can name the recent AI-focused additions.
- [ ] I can plan a role-based path from Fundamentals upward.
- [ ] I can verify the current catalog on databricks.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
