# Chapter 08: Capstone — A Public Sector Data Governance Program Blueprint

## Learning Objectives

- Assemble the four content areas into one coherent program blueprint.
- Run a maturity assessment and set a roadmap.
- Trace a single dataset end-to-end through drivers, deliverables, roles, and law.
- Produce an executive one-page program summary.
- Complete a capstone walkthrough integrating the whole volume.

## Theory and Architecture

A PSDGP program is only real when the four content areas **connect**. This capstone assembles
them: the **mission drivers** (Chapter 02) justify the **deliverables** (Chapter 03), which are
operated by **roles** (Chapter 04), constrained by the **legal environment** (Chapter 05), and
built on the **core body of knowledge** (Chapter 06). The tools of the blueprint are a
**maturity assessment** (where are we?), a **roadmap** (where next?), an **end-to-end trace**
(does a real dataset flow correctly?), and an **executive summary** (can leadership see it?).
This is the artifact a certified professional is expected to be able to produce.

## Design Considerations

Anchor the blueprint to a **baseline maturity** and a **short roadmap** — governance matures in
increments, not big bangs. Prove the design with **one dataset traced end-to-end** before
scaling. Keep the executive summary to a page: drivers, deliverables, roles, obligations, and
next steps.

## Implementation and Automation

The capstone labs run a maturity scorecard, build a roadmap, trace a dataset end-to-end, and
generate an executive summary.

## Validation and Troubleshooting

Confirm the blueprint assembles:

```text
Drivers (why) -> Deliverables (what) -> Roles (who) -> Legal (bounds) -> Core (how).
Prove with: maturity baseline + roadmap + one end-to-end dataset trace + exec summary.
```

Common pitfalls: a blueprint with **deliverables but no roadmap**; and never validating the
design against a **real dataset**.

## Hands-On Lab

Capstone walkthroughs. **Shared prerequisites for Labs 8.1–8.4** — a shell with `python3`.
**Cost:** none.

### Lab 8.1 — Maturity assessment

**Objective:** Baseline the program across the four areas.

```python
python3 - <<'PY'
levels={"Mission Drivers":3,"Deliverables":2,"Roles":2,"Legal & Regulatory":3}  # 1..5
avg=sum(levels.values())/len(levels)
for a,l in levels.items(): print(f"{a:20} L{l}")
print(f"overall maturity: {avg:.1f}/5")
PY
```

**Expected result:** a per-area maturity baseline and overall score (**2.5/5**) — the starting
point for a roadmap.

**Negative test:** declare the program "mature" with no assessment; maturity must be
**measured** per area — score it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Roadmap from the baseline

**Objective:** Turn the weakest areas into next steps.

```python
python3 - <<'PY'
levels={"Mission Drivers":3,"Deliverables":2,"Roles":2,"Legal & Regulatory":3}
roadmap={a:("raise to L3: complete core deliverables/roles" if l<3 else "sustain")
         for a,l in levels.items()}
for a,step in roadmap.items(): print(f"{a:20} -> {step}")
PY
```

**Expected result:** targeted next steps for the **weakest areas** (Deliverables, Roles) — an
incremental roadmap.

**Negative test:** plan to fix everything at once; governance matures **incrementally** —
sequence the weakest first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — End-to-end dataset trace

**Objective:** Validate the design on one real dataset.

```python
python3 - <<'PY'
trace={
 "dataset":"benefits_enrollment",
 "driver":"Service delivery + Transparency",
 "deliverables":["Catalog entry","Classification=PII","DQ scorecard"],
 "roles":{"owner":"Benefits Division","steward":"J. Rivera","custodian":"IT/BENSYS"},
 "legal":["Privacy Act (PII)","NARA 7-yr retention","FOIA (redact PII)"],
}
for k,v in trace.items(): print(f"{k:12}: {v}")
print("trace complete: driver->deliverable->role->law all present")
PY
```

**Expected result:** one dataset shown flowing through **driver → deliverable → role → law** —
the design proven on a real record.

**Negative test:** scale the program before tracing any dataset; validate the design on **one**
first — trace before you scale.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Executive one-pager

**Objective:** Summarize the program for leadership.

```python
python3 - <<'PY'
summary={
 "Program":"Agency Data Governance","Maturity":"2.5/5 -> target 3.5 in 12 months",
 "Drivers":"Service, Open data, Transparency, Compliance",
 "Deliverables":"Charter, Policies, Catalog, DQ scorecard, RACI",
 "Roles":"Council, CDO, Owners, Stewards, Custodians",
 "Obligations":"FOIA, Privacy Act, NARA, FISMA/FedRAMP, OPEN Data Act",
 "Next":"Complete deliverables & roles to L3",
}
for k,v in summary.items(): print(f"{k:12}: {v}")
PY
```

**Expected result:** a one-page program summary leadership can read — drivers, deliverables,
roles, obligations, and next steps.

**Negative test:** brief executives with a 40-page document; leadership needs a **one-pager** —
summarize.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The capstone assembles the four content areas into one program: drivers justify deliverables,
operated by roles, bounded by law, built on the core. Baseline maturity, set an incremental
roadmap, prove the design by tracing one dataset end-to-end, and summarize it on a page for
leadership.

- [ ] I can run a maturity assessment across the four areas.
- [ ] I can build an incremental roadmap from the baseline.
- [ ] I can trace a dataset end-to-end through the model.
- [ ] I can produce an executive one-page summary.
- [ ] I completed Labs 8.1–8.4 including each negative test.
