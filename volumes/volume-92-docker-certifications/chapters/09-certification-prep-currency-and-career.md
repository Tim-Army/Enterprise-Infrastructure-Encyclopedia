# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Plan preparation with Mirantis training and hands-on practice.
- Handle the DOMC question format.
- Plan for the two-year validity and renewal.
- Map a Docker/containers career.
- Complete a walkthrough for each prep-and-career topic.

## Theory and Architecture

Earning the **Docker Certified Associate** follows a clear path. Preparation combines **hands-on
practice** on a free Docker Engine (the CLI is what the exam tests) with **Mirantis training** — courses
and a **bootcamp** tailored to the DCA — plus the official documentation. Register through **Mirantis
training**; the exam is **$199** for one attempt (cancel/reschedule up to 48 hours before). A distinctive
challenge is the **DOMC (discrete-option multiple-choice)** format: 42 of the 55 questions present
statements one at a time and you answer **Yes/No**, with **no going back** — so you need precise, decisive
knowledge rather than elimination strategies. The credential is **valid for two years**, after which you
re-certify against the current exam. A Docker/containers career ladders from container developer into
DevOps, platform engineering, and cloud-native/Kubernetes roles (complemented by the CNCF/Kubernetes
volume, XLI). This chapter closes the volume — and the DevOps & observability cluster — with prep,
currency, and career walkthroughs.

## Design Considerations

Practice on a **free Docker Engine** across all six domains, weighting by exam weight (orchestration and
images first). Rehearse the **DOMC** style — decide each statement Yes/No confidently. Use **Mirantis
training/bootcamp** to fill gaps. Plan the **$199 single attempt** and the **two-year** renewal. Keep
skills current as Docker and the orchestrators evolve.

## Implementation and Automation

The labs plan a preparation path, model the DOMC format, and map the certification to a career — the
progression the program supports.

## Validation and Troubleshooting

Confirm prep, currency, and career:

```text
Prep: free Docker Engine hands-on (all 6 domains) + Mirantis training/bootcamp + docs
DOMC: 42 of 55 questions are Yes/No statements, one at a time, NO going back -> precise knowledge
Register: Mirantis training; $199 (one attempt); reschedule 48h before; valid 2 years
Career: container developer -> DevOps / platform engineer / cloud-native (K8s, Volume XLI)
```

Common pitfalls: preparing only with theory and no **hands-on** CLI; and being unready for **DOMC** (no
elimination, no revisiting).

## Security and Best Practices

Prepare on your own engine, apply the security practices from Chapter 08, and keep skills current. Docker
skills underpin secure, portable delivery. All work is authorized administration.

## Hands-On Lab

Prep-and-career walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Plan a preparation path

**Objective:** Sequence practice and training to the exam.

```python
python3 - <<'PY'
plan = [
  "1. Install a free Docker Engine; practice all 6 domains via this volume's labs",
  "2. Weight study by exam weight: Orchestration 25%, Images 20%, then Install/Net/Sec/Storage",
  "3. Mirantis training / bootcamp to fill gaps; read the docs",
  "4. Rehearse the DOMC (Yes/No, no going back) style",
  "5. Register via Mirantis; sit the exam ($199; 13 MC + 42 DOMC / 90 min)",
]
for step in plan: print(step)
PY
```

**Expected result:** a hands-on, weighted preparation path ending at the DCA exam.

**Negative test:** study only reading material; the exam rewards **hands-on** CLI fluency — practice.

**Cleanup:** none.

### Lab 9.2 — Model the DOMC format

**Objective:** Practice decisive Yes/No answering.

```python
python3 - <<'PY'
# DOMC: each statement judged Yes/No independently; no elimination, no revisit
statements = {
  "A named volume persists after the container is removed": "YES",
  "A bind mount is managed under /var/lib/docker/volumes": "NO (that's a named volume)",
  "The default bridge provides DNS resolution by name":    "NO (user-defined does)",
}
for s, ans in statements.items(): print(f"[{ans:>3}] {s}")
print("DOMC needs precise recall -> answer each statement decisively")
PY
```

**Expected result:** independent Yes/No judgments on precise statements — the DOMC skill.

**Negative test:** rely on eliminating wrong options like standard multiple-choice; **DOMC** judges each
statement on its own.

**Cleanup:** none.

### Lab 9.3 — Map a Docker career and renewal

**Objective:** Plan progression and currency.

```python
python3 - <<'PY'
ladder = {
  "DCA (Docker Certified Associate)": "container developer / operator baseline",
  "-> DevOps engineer":               "CI/CD + containers in pipelines",
  "-> Platform engineer":             "orchestration at scale (Swarm/Kubernetes)",
  "-> Cloud-native / K8s":            "CNCF certifications (Volume XLI)",
}
for role, arc in ladder.items(): print(f"{role:34}: {arc}")
print("Currency: DCA valid 2 years -> re-certify against the current exam")
PY
```

**Expected result:** the DCA as a baseline laddering into DevOps, platform, and cloud-native roles, with a
two-year renewal.

**Negative test:** let the credential lapse past two years as tooling changes; **re-certify** on the
current exam.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Docker Certified Associate prep combines free hands-on Docker Engine practice across all six weighted
domains with Mirantis training and bootcamp, rehearsing the DOMC Yes/No format (no going back) before the
$199 single-attempt exam — a two-year credential that ladders a container career from developer into
DevOps, platform engineering, and cloud-native/Kubernetes roles.

- [ ] I can plan a preparation path across all domains.
- [ ] I can handle the DOMC question format.
- [ ] I can plan for the two-year validity and renewal.
- [ ] I can map a Docker/containers career.
- [ ] I completed Labs 9.1–9.3 including each negative test.
