# Chapter 09: Keeping the Cribl Program Current and Career Paths

## Learning Objectives

- Explain Cribl certification validity and renewal.
- Track program change across the product portfolio.
- Plan a Cribl certification path by role.
- Relate Cribl credentials to the encyclopedia's observability volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Cribl certifications are **free**, delivered as **online self-study** through Cribl
University, and **valid three years**. The program tracks a fast-growing portfolio — Stream,
Edge, Search, and Lake — so new courses and certifications appear as the products evolve.
The ladder (**CC User → CC Admin (Stream/Edge) → CC Engineer → CCSC**) reflects increasing
depth from using to administering to designing to consulting.

## Design Considerations

Plan by **role**: everyone starts at **CC User**; pipeline admins take **CC Admin - Stream**,
collection admins take **CC Admin - Edge**, architects take **CC Engineer** (after the Admin
certs), and partners pursue **CCSC**. Recertify within the three-year window and watch for
new product certs.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://cribl.io/university/" \
  | grep -oiE 'CC User|CC Admin[^<]*|CC Engineer|CCSC|Cribl Certified[^<]*' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
cribl.io/university:
  - ladder: CC User -> CC Admin (Stream/Edge) -> CC Engineer -> CCSC (partner)
  - free; online self-study; valid 3 years; Admin requires CC User; Engineer requires Admin
```

Common pitfalls: skipping **CC User** (it gates the Admin certs); and letting a credential
lapse past three years.

## Security and Best Practices

Recertify by exam within the three-year window, follow the matching **Cribl University**
course, practice on the **free tier**, and combine credentials for your role (e.g., User →
Admin-Stream → Engineer). Track new product certifications as the portfolio grows.

## References and Knowledge Checks

- cribl.io/university and university.cribl.io: the certification catalog and courses.

**Knowledge checks**

1. How are Cribl certifications delivered and how long are they valid?
2. Which certifications require CC User first?
3. What path suits a Stream pipeline administrator?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell with
`curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify the current ladder

**Objective:** Read the current certifications.

```bash
curl -sSL -A "Mozilla/5.0" "https://cribl.io/university/" \
  | grep -oiE 'CC User|CC Admin[^<]{0,12}|CC Engineer|CCSC' | sort -u
```

**Expected result:** the current ladder (**CC User, CC Admin …, CC Engineer, CCSC**) —
confirming scope.

**Negative test:** trust a cached list; Cribl adds product certs — confirm on
cribl.io/university.

**Cleanup:** none.

### Lab 9.2 — Plan a path

**Objective:** Map a role to a Cribl certification sequence.

```bash
python3 - <<'PY'
paths={"Stream Admin":"CC User -> CC Admin - Stream -> CC Engineer",
       "Edge Admin":"CC User -> CC Admin - Edge",
       "Architect":"CC User -> both Admin -> CC Engineer",
       "Partner Consultant":"... -> CCSC"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** attempt CC Engineer first; it **requires the Admin certs** — build up the
ladder.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cribl certifications are free, self-study, and valid three years, following a ladder from CC
User through CC Admin (Stream/Edge) and CC Engineer to the partner CCSC. Plan a path by
role, practice on the free tier, and verify the current ladder before you study.

- [ ] I can explain delivery, validity, and renewal.
- [ ] I can identify which certs require CC User/Admin first.
- [ ] I can plan a role-based certification path.
- [ ] I can verify the current program on cribl.io.
- [ ] I completed Labs 9.1–9.2 including each negative test.
