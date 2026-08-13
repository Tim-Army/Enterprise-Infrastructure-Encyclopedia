# Chapter 09: Choosing and Rolling Out Microsegmentation

## Learning Objectives

- Score the options against the weighted rubric to a decision.
- Plan a proof of concept (PoC) with clear exit criteria.
- Plan a phased, monitor-first rollout.
- Avoid the common failure modes.
- Complete a walkthrough for each decision-and-rollout topic.

## Theory and Architecture

Choosing a microsegmentation approach is a **fit** decision, not a "best product" decision. Bring the
options through the same **weighted rubric** from Chapter 02 (coverage, visibility, automation,
granularity, scale, failure mode, compliance, TCO), scored for **your** estate, and let the numbers plus
judgment pick a shortlist — often a **primary** platform plus a **complement** for assets it does not
cover (for example, an agent platform for servers plus an appliance for OT). Validate the shortlist with
a **PoC** that has explicit exit criteria (coverage %, mapping accuracy, policy-automation quality,
performance, operability). Then roll out in **phases**: **discover and map**, **ring-fence** the flat
high-risk zones, apply policy in **monitor/observe** mode, review, and only then **enforce** default-deny
— starting with crown jewels and expanding. This chapter turns the comparison into a plan.

## Design Considerations

Expect to combine **more than one** model for full coverage. Sequence the rollout by **risk** (crown
jewels, flat zones, admin paths first) and always **monitor before enforce**. Set **PoC exit criteria**
up front so the decision is evidence-based. Plan **day-2 operations**: policy change control, drift
detection, new-workload onboarding, and break-glass. Decide **failure mode** per asset class. Keep the
segmentation controller itself hardened and highly available.

## Implementation and Automation

The labs score the options into a decision, define PoC exit criteria, and model a phased rollout — turning
the volume's comparison into an actionable plan.

## Validation and Troubleshooting

Confirm the decision-and-rollout process:

```text
Decide: score every option on the SAME weighted rubric for YOUR estate -> primary + complement
PoC: explicit exit criteria (coverage %, mapping accuracy, automation, performance, operability)
Rollout: discover/map -> ring-fence flat zones -> MONITOR mode -> review -> ENFORCE default-deny (crown jewels first)
Day-2: change control, drift detection, onboarding, break-glass; per-asset failure mode
```

Common pitfalls: **enforcing before monitoring** (outages); picking one tool that **misses** an asset
class; and no **day-2** process so policy rots as the estate changes.

## Security and Best Practices

Monitor-first, risk-sequenced rollout with default-deny at the end is the safe path to real containment.
Harden and make the controller highly available. Keep humans in the loop for enforcement changes. All
work is authorized administration of your own environment.

## Hands-On Lab

Decision-and-rollout walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Score the options to a decision

**Objective:** Turn the comparison into a shortlist.

```python
python3 - <<'PY'
weights = {"coverage":0.25,"visibility":0.15,"automation":0.15,"granularity":0.10,
           "scale":0.10,"failure_mode":0.05,"compliance":0.10,"tco":0.10}
# illustrative scores for one hybrid IT/OT estate (score to YOUR environment)
options = {
  "NSX DFW":        {"coverage":3,"visibility":4,"automation":4,"granularity":4,"scale":4,"failure_mode":4,"compliance":3,"tco":3},
  "Illumio":        {"coverage":4,"visibility":5,"automation":4,"granularity":5,"scale":4,"failure_mode":3,"compliance":4,"tco":3},
  "Zero Networks":  {"coverage":4,"visibility":4,"automation":5,"granularity":3,"scale":4,"failure_mode":3,"compliance":4,"tco":5},
  "TrueFort":       {"coverage":3,"visibility":5,"automation":4,"granularity":5,"scale":4,"failure_mode":3,"compliance":4,"tco":4},
  "ColorTokens":    {"coverage":5,"visibility":4,"automation":4,"granularity":4,"scale":4,"failure_mode":4,"compliance":5,"tco":3},
}
ranked = sorted(options.items(), key=lambda kv: -sum(weights[k]*kv[1][k] for k in weights))
for name, s in ranked:
    print(f"{name:14}: {sum(weights[k]*s[k] for k in weights):.2f}")
print("Read as fit-for-THIS-estate, not absolute; top 1-2 go to PoC (+ complement for gaps)")
PY
```

**Expected result:** a ranked shortlist for the modeled estate — evidence for the PoC choice (re-score
for your own environment).

**Negative test:** pick the "market leader" without scoring your **own** coverage needs; score every
option on the same rubric for your estate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Define PoC exit criteria

**Objective:** Make the PoC pass/fail objective.

```python
python3 - <<'PY'
criteria = {
  "asset coverage":       ">= 95% of in-scope assets enforceable",
  "dependency mapping":   ">= 90% of flows auto-identified correctly",
  "policy automation":    "default-deny policy generated with < X manual edits",
  "performance impact":   "< 2% host CPU; no app latency regression",
  "operability":          "policy change + onboard new workload in < 1 day",
  "failure mode":         "verified behavior on controller/agent failure",
}
for k, v in criteria.items(): print(f"[ ] {k:20}: {v}")
print("PoC passes only if ALL criteria met on representative assets (incl. OT/legacy)")
PY
```

**Expected result:** a checklist of measurable exit criteria — an evidence-based go/no-go.

**Negative test:** run a PoC with no exit criteria and decide on vibes; define **measurable** criteria up
front.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Model a phased, monitor-first rollout

**Objective:** Sequence enforcement safely.

```python
python3 - <<'PY'
phases = [
  ("1 Discover",   "deploy sensors/agents; map east-west flows"),
  ("2 Ring-fence", "isolate flat high-risk zones (DCs, jump hosts, OT) at the boundary"),
  ("3 Monitor",    "author allowlist; run in OBSERVE mode; review would-be denies"),
  ("4 Enforce",    "flip crown jewels to default-deny; expand ring by ring"),
  ("5 Operate",    "change control, drift detection, onboarding, break-glass"),
]
for name, action in phases: print(f"Phase {name:12}: {action}")
print("Never skip Phase 3 (monitor) before Phase 4 (enforce)")
PY
```

**Expected result:** the discover→ring-fence→monitor→enforce→operate sequence — a safe path to
default-deny.

**Negative test:** jump straight to enforce on the whole estate; unmapped flows break — monitor first,
enforce by risk.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Choosing microsegmentation is a fit decision: score every option on one weighted rubric for your estate
(usually landing on a primary platform plus a complement for uncovered assets), validate with a PoC that
has measurable exit criteria, and roll out in phases — discover and map, ring-fence, monitor, then enforce
default-deny from the crown jewels outward — with a real day-2 operations process.

- [ ] I can score the options into a decision for my estate.
- [ ] I can define measurable PoC exit criteria.
- [ ] I can plan a phased, monitor-first rollout.
- [ ] I can name the common failure modes and avoid them.
- [ ] I completed Labs 9.1–9.3 including each negative test.
