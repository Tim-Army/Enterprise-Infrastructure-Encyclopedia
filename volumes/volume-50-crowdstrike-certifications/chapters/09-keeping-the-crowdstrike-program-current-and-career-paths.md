# Chapter 09: Keeping the CrowdStrike Program Current and Career Paths

## Learning Objectives

- Explain CrowdStrike certification validity and recertification.
- Track program change — new specialist exams and guide revisions.
- Plan a Falcon certification path by role.
- Relate Falcon credentials to the encyclopedia's security volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

CrowdStrike certifications are valid for **three years** and renewed by **passing the
current version of the exam** on expiry. The program tracks the platform: the
**Next-Gen SIEM** pair (CCSA/CCSE) and the **specialist** exams (CCIS, CCCS) reflect
Falcon's expansion beyond endpoint into SIEM, identity, and cloud. Exam guides are
revised regularly (the current set dates from January–July 2026).

## Design Considerations

Plan by **role**: administrators start at **CCFA**; SOC analysts add **CCFR** then
**CCFH**; SIEM teams take **CCSA**/**CCSE**; identity and cloud specialists take
**CCIS**/**CCCS**. There are no enforced prerequisites, but the guides recommend the
matching CrowdStrike University learning path and hands-on experience.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.crowdstrike.com/en-us/crowdstrike-university/crowdstrike-falcon-certification-program/" \
  | grep -oiE 'CCF[ARH]|CCS[AE]|CCIS|CCCS' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
crowdstrike.com/crowdstrike-university:
  - 7 certifications; 90-min / 60-Q; Pearson VUE
  - valid 3 years; recertify by passing the current exam
  - download the current exam guide (check the revision date)
```

Common pitfalls: studying a stale guide; and letting a credential lapse past three
years (recertify by exam).

## Security and Best Practices

Recertify by exam within the three-year window. Follow the matching **CSU learning
path**, practice in a Falcon tenant, and combine credentials for your role (e.g.,
CCFA + CCFR + CCFH for a full endpoint analyst path). Track guide revisions so
content changes don't surprise you.

## References and Knowledge Checks

- crowdstrike.com/crowdstrike-university: the program, exam guides, and CSU training.

**Knowledge checks**

1. How are CrowdStrike certifications renewed?
2. Which exams reflect Falcon's move into SIEM, identity, and cloud?
3. What path suits an endpoint SOC analyst?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell
with `curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify the current lineup

**Objective:** Read the current certifications from the source.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.crowdstrike.com/en-us/crowdstrike-university/crowdstrike-falcon-certification-program/" \
  | grep -oiE 'CCF[ARH]|CCS[AE]|CCIS|CCCS' | sort -u | wc -l
```

**Expected result:** **7** — the seven current certifications (confirming the program
scope before you study).

**Negative test:** trust a cached list; the vendor adds specialist exams — confirm on
crowdstrike.com.

**Cleanup:** none.

### Lab 9.2 — Plan a path

**Objective:** Map a role to a Falcon certification sequence.

```bash
python3 - <<'PY'
paths={"Falcon Admin":"CCFA",
       "SOC Analyst":"CCFA -> CCFR -> CCFH",
       "SIEM Team":"CCSA (analyst) / CCSE (engineer)",
       "Identity Specialist":"CCIS",
       "Cloud Specialist":"CCCS"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** collect exams at random; **sequence by role** for a coherent skill
path.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CrowdStrike certifications are valid three years and renewed by passing the current
exam. The program spans endpoint (CCFA/CCFR/CCFH), Next-Gen SIEM (CCSA/CCSE), and
specialists (CCIS/CCCS). Plan a path by role, follow the CSU learning path, and
verify the current lineup before you study.

- [ ] I can explain validity and recertification.
- [ ] I can name which exams cover SIEM, identity, and cloud.
- [ ] I can plan a role-based certification path.
- [ ] I can verify the current lineup on crowdstrike.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
