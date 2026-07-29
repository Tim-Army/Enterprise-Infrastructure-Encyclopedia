# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Prepare for Alibaba Cloud Academy exams.
- Practice hands-on with a free-tier account.
- Keep credentials current as services evolve.
- Plan a career across the ACA/ACP/ACE levels.
- Complete a walkthrough for exam prep and currency.

## Theory and Architecture

Alibaba Cloud certifications are delivered by **Alibaba Cloud Academy** (edu.alibabacloud.com) with
**online proctored** exams, so preparation combines **conceptual knowledge** and **hands-on practice**.
Effective prep combines the **Academy courses and learning paths** for the target certification, the
**product documentation**, and hands-on time in a **free-tier/trial** account (many services offer a
free tier or trial credits) — building, not just reading. On **currency**: cloud services evolve
continuously and certifications are typically valid **two years**, so a credential should be renewed as
services and best practices change — tracking alibabacloud.com is ongoing. An Alibaba Cloud career
climbs **ACA → ACP → ACE**, branching by **domain**: cloud computing, security, big data, cloud native,
database, networking, DevOps, or machine learning. This closing chapter turns the volume into a durable
exam-prep, currency, and career plan.

## Design Considerations

Prepare with **Academy courses + docs + hands-on** (free tier). Match study to the exam's **domain and
level**. Renew on the **two-year** cycle as services evolve. Choose a **domain** for your career and
climb ACA → ACP → ACE. Learn the **native service names** (not AWS/Azure equivalents).

## Implementation and Automation

The labs plan prep, verify a free practice setup, and plan currency/career.

## Validation and Troubleshooting

Confirm the prep/currency model:

```text
Exams: Alibaba Cloud Academy (online proctored). Prepare: Academy courses + docs + hands-on (free-tier/trial). Currency: ~2-year validity; services evolve -> renew. Track alibabacloud.com.
Career: ACA -> ACP -> ACE, by domain (cloud computing/security/big data/cloud native/database/networking/DevOps/ML-AI).
```

Common pitfalls: concepts-only prep with no **hands-on**; and letting a cert lapse past **two years**.

## Security and Best Practices

Prepare with Academy training, docs, and **hands-on** on a free tier; match the **level/domain**; and
renew on the **two-year** cycle. Learn native service names. All practice is authorized.

## Hands-On Lab

Prep and currency walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Plan exam preparation

**Objective:** Cover concepts and practice.

```python
python3 - <<'PY'
prep={"Courses":"Alibaba Cloud Academy learning path for the target cert (level + domain)",
      "Docs":"product documentation (ECS/VPC/OSS/RDS/ACK/PAI)","Hands-on":"free-tier/trial account: build a VPC + ECS + OSS + RDS",
      "Blueprint":"map study to the exam's domain outline"}
for k,v in prep.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** a prep plan covering **concepts + hands-on** — balanced preparation.

**Negative test:** memorize service names with no **hands-on** building; the exam tests applied
knowledge — practice.

**Cleanup:** none.

### Lab 9.2 — Verify a free practice setup

**Objective:** Practice at low cost.

```python
python3 - <<'PY'
free_prep={"account":"free-tier / trial credits","build":"VPC + vSwitch + ECS + security group + OSS bucket + small RDS",
          "cli":"aliyun CLI for repeatable, scriptable practice","teardown":"delete resources after each session (avoid charges)"}
for k,v in free_prep.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** a **free-tier** practice setup with teardown — accessible hands-on prep.

**Negative test:** leave practice resources running after sessions; trial credits/charges accrue —
**tear down** after each lab.

**Cleanup:** none.

### Lab 9.3 — Plan currency and career

**Objective:** Stay current and plan a path.

```python
python3 - <<'PY'
routine={"Validity":"~2 years — renew as services/best practices evolve",
         "Track":"new services + exam updates on alibabacloud.com","Practice":"keep a free-tier account for hands-on",
         "Career":"ACA -> ACP -> ACE, specialized by domain (cloud/security/big data/cloud native/ML)"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — renewal, service tracking, practice, and a path.

**Negative test:** hold an old cert without renewing; services and exams change — renew on the
**two-year** cycle.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alibaba Cloud exams are Academy-delivered and test concepts plus hands-on skill, prepared with courses,
docs, and a free-tier account; certifications are ~two-year valid, so hands-on prep, service tracking,
and renewal across ACA → ACP → ACE by domain keep you current.

- [ ] I can plan exam preparation.
- [ ] I can verify a free practice setup.
- [ ] I can plan two-year currency.
- [ ] I can plan a career across the levels.
- [ ] I completed Labs 9.1–9.3 including each negative test.
