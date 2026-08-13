# Chapter 07: CWDP — Design Professional

## Learning Objectives

- Explain the CWDP scope: WLAN design and validation.
- Gather requirements and plan for coverage vs capacity.
- Conduct site surveys (predictive, passive, active).
- Produce a channel plan and validate the design.
- Complete a design walkthrough for each CWDP topic.

## Theory and Architecture

**CWDP** (Certified Wireless Design Professional) covers designing WLANs that meet requirements.
Design starts with **requirements gathering** — applications (voice, video, data, location),
device types, density, and coverage areas — because a **coverage** design (fewer APs for signal
everywhere) differs from a **capacity** design (more APs for many high-throughput clients).
**Site surveys** validate the RF environment: **predictive** (modeling in software from floor
plans), **passive** (walking with a receiver to measure existing signal/noise), and **active**
(associating and measuring throughput/roaming). The output includes **AP placement**, a
**channel/power plan** (reuse 1/6/11 in 2.4 GHz; plan 5/6 GHz channels and widths; manage DFS),
and **capacity math** (clients × application bandwidth ÷ per-AP capacity → AP count). Finally the
design is **validated** with a post-deployment survey. CWDP turns requirements into a working,
verified WLAN.

## Design Considerations

Decide **coverage vs capacity** from the requirements. Survey **predictively then validate on
site**. Plan **channels and power** to minimize co-channel interference and size **channel width**
to density. Compute **capacity** from real application demand. Always **validate** post-deployment —
a design isn't done until measured.

## Implementation and Automation

The design exercises size capacity, plan channels, choose a survey type, and define validation.

## Validation and Troubleshooting

Confirm the design method:

```text
Requirements -> coverage vs capacity -> survey (predictive/passive/active) -> AP placement +
channel/power plan (1/6/11 in 2.4; 5/6 GHz widths; DFS) -> capacity math -> VALIDATE post-deploy.
CWDP.
```

Common pitfalls: a **coverage** design for a **high-density** space (too few APs); and skipping
**post-deployment validation**.

## Security and Best Practices

Design to **requirements**, validate **predictions on site**, plan **channels/power** for minimal
interference, and **validate** the finished WLAN. Build in redundancy for critical areas. Document
the design and survey results. A measured design is a defensible design.

## Hands-On Lab

Design exercises. **Shared prerequisites for Labs 7.1–7.4** — a shell with `python3` and a
requirements sheet. **Cost:** none.

### Lab 7.1 — Coverage vs capacity

**Objective:** Classify the design goal.

```python
python3 - <<'PY'
def goal(clients_per_area, app):
    return "capacity" if clients_per_area>25 or app in ("voice","video") else "coverage"
print("warehouse (few devices, data):", goal(8,"data"))
print("lecture hall (many devices, video):", goal(120,"video"))
PY
```

**Expected result:** **coverage** for sparse data areas, **capacity** for dense/real-time — the
design driver.

**Negative test:** design a 300-seat auditorium for coverage; high density needs a **capacity**
design — more APs, tighter cells.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Capacity AP count

**Objective:** Size APs from application demand.

```python
python3 - <<'PY'
import math
clients=200; per_client_mbps=2; ap_capacity_mbps=300
aps=math.ceil((clients*per_client_mbps)/ap_capacity_mbps)
print(f"{clients} clients x {per_client_mbps} Mbps / {ap_capacity_mbps} per AP -> {aps} APs (capacity)")
PY
```

**Expected result:** the **AP count** from capacity math — sized to real demand, not guesswork.

**Negative test:** place APs by "one per room" with no capacity math; **compute** from client count
and demand.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Choose a survey type

**Objective:** Match the survey to the phase.

```python
python3 - <<'PY'
surveys={"Design phase (no gear installed)":"predictive (model from floor plan)",
         "Existing WLAN assessment":"passive (measure signal/noise)",
         "Validate performance/roaming":"active (associate, measure throughput)"}
for phase,s in surveys.items(): print(f"{phase:34}: {s}")
PY
```

**Expected result:** the right **survey type per phase** — predictive to plan, passive/active to
validate.

**Negative test:** rely only on a **predictive** model and never validate on site; **passive/active
surveys** confirm reality — do them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Validation plan

**Objective:** Define post-deployment checks.

```python
python3 - <<'PY'
checks=["min signal (e.g., -67 dBm in coverage areas)","SNR >= 25 dB","channel plan (no co-channel overlap)",
        "roaming across cells","throughput per application","secondary coverage for critical areas"]
for c in checks: print("-",c)
PY
```

**Expected result:** a **validation checklist** (signal, SNR, channels, roaming, throughput) — proof
the design works.

**Negative test:** declare the WLAN done at install with no validation; **measure** against the
checklist first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CWDP covers WLAN design: requirements-driven coverage-vs-capacity decisions, predictive/passive/
active site surveys, AP placement and channel/power planning, capacity math, and post-deployment
validation. Design to requirements, survey and validate on site, and never skip validation.

- [ ] I can classify a coverage vs capacity design.
- [ ] I can size APs from capacity demand.
- [ ] I can choose the right survey type.
- [ ] I can define a validation plan.
- [ ] I completed Labs 7.1–7.4 including each negative test.
