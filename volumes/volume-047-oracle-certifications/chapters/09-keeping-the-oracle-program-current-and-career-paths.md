# Chapter 09: Keeping the Oracle Program Current and Career Paths

## Learning Objectives

- Explain Oracle's year-versioned exam codes and recertification.
- Track program change — OCI Generative AI, Multicloud, Database 23ai, Java SE 21.
- Plan an Oracle career path across the four families.
- Relate Oracle credentials to the encyclopedia's cloud and data volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Oracle refreshes many exams **annually**, encoded in the **year suffix** of the
exam number (for example, OCI Architect Associate **1Z0-1072-26**, OCI Generative
AI Professional **1Z0-1127-26**). OCI certifications generally follow this
year-versioned model; some Database, MySQL, and Java exams are versioned by
**product release** (Database 23ai, Java SE 21) instead. Credentials are managed in
**Oracle CertView**, and free training is available through **Oracle Learning
Explorer** and the OCI free tier.

Recent program changes worth verifying against any older map: the **OCI Generative
AI Professional** and **Multicloud Architect** credentials, **Oracle Database
23ai** (AI Vector Search), and **Java SE 21** as the current Java target.

## Design Considerations

Plan a path by **family and role**:

- **Cloud:** OCI Foundations → Architect Associate → Professional, then a specialty
  (Developer, Operations/DevOps, Networking, Security, Data Science, **Generative
  AI**, Multicloud).
- **Database:** SQL Associate → DBA Associate → Professional (on **23ai**), plus
  Autonomous Database.
- **MySQL:** DBA and/or Developer.
- **Java:** Java SE 21 Developer.

Always confirm the **current year suffix / release** so you study the live exam.

## Implementation and Automation

Verify currency from **education.oracle.com** — the certification pages carry the
current exam code (with year suffix) and topics:

```bash
curl -sSL -A "Mozilla/5.0" "https://education.oracle.com/certification" \
  | grep -oiE '1Z0-[0-9]{3,4}(-[0-9]{2})?' | sort -u | head
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
education.oracle.com:
  - the current exam code (year suffix / product release) and topics
  - recommended courses and hands-on practice (free tiers)
  - recertification requirements per credential
Watch for OCI Generative AI, Multicloud, Database 23ai, and Java SE 21.
```

Common pitfalls: studying a **prior-year** OCI exam (check the suffix); targeting
**older Database/Java** versions; and letting an OCI credential lapse (they carry
recertification timelines).

## Security and Best Practices

Track the **year-versioned** code and recertify on schedule (Oracle provides
shorter delta/recert exams for some tracks). Practice on **free tiers** (OCI Always
Free, Oracle Database Free/Autonomous, MySQL, JDK 21) so preparation costs nothing.
Combine credentials to match a role (e.g., OCI Architect + Database DBA for a cloud
DBA).

## References and Knowledge Checks

- education.oracle.com: the certification catalog, exam topics, CertView, and recertification policy; Oracle Learning Explorer (free).

**Knowledge checks**

1. What does the year suffix in an OCI exam code mean for currency?
2. Which recent credentials/releases must you verify against an old map?
3. What is a sensible OCI cloud path from Foundations upward?

## Hands-On Lab

Exam-preparation walkthroughs for tracking change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a shell with `curl` and `python3`.
**Cost:** none.

### Lab 9.1 — Verify current exam codes (Topic: Verify currency)

**Objective:** Read current, year-versioned exam codes from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://education.oracle.com/certification" \
  | grep -oiE '1Z0-[0-9]{3,4}(-[0-9]{2})?' | sort -u | head
```

**Expected result:** current `1Z0-####(-YY)` codes — confirming the year suffixes
(e.g., `-25`/`-26`) so you study the live exam, not a superseded one.

**Negative test:** trust a course citing `1Z0-1072-23`; the suffix has rolled —
confirm the current year on education.oracle.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a path across families (Topic: Career)

**Objective:** Map roles to Oracle credential sequences.

```bash
python3 - <<'PY'
paths = {"Cloud Architect":"OCI Foundations -> Architect Associate -> Professional (+ specialty)",
         "Cloud DBA":"OCI Foundations + SQL Associate -> DBA Professional (23ai) + Autonomous",
         "AI Engineer":"OCI AI Foundations -> Data Science Pro -> Generative AI Professional",
         "Java Developer":"Java SE 21 Developer (1Z0-830)"}
for role,path in paths.items(): print(f"{role:16}: {path}")
PY
```

**Expected result:** role-to-path sequences across OCI, Database, and Java — the
career mapping this volume supports.

**Negative test:** collect certs with no role in mind; plan the **sequence** for a
target role instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Oracle refreshes exams on a yearly (OCI) or product-release (Database 23ai, Java SE
21) cadence, encoded in the exam code, and manages credentials in CertView. The
program has added OCI Generative AI and Multicloud credentials, Database 23ai, and
Java SE 21. Plan a path by family and role, practice on free tiers, and confirm the
current exam code before studying.

- [ ] I can explain Oracle's year-versioned exam codes and recertification.
- [ ] I can name the recent OCI/Database/Java additions.
- [ ] I can map a role to an Oracle credential sequence.
- [ ] I can verify current exam codes on education.oracle.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
