# Chapter 04: Risk Assessment (IC33) — High-Level Assessment

## Learning Objectives

- Cover the IC33 Risk Assessment Specialist's first half: the high-level (initial) risk assessment.
- Understand the System under Consideration, initial risk, and the risk matrix.
- Build a repeatable high-level risk-scoring worksheet.

## The exam in brief

**Certificate 2 — Cybersecurity Risk Assessment Specialist** (course **IC33**) maps to the **Assess** phase and to **IEC 62443-3-2** (risk assessment for system design). It has two stages: a **high-level (initial) risk assessment** to identify and prioritize (this chapter), and a **detailed risk assessment** per zone/conduit that sets target security levels ([Chapter 05](05-risk-assessment-detailed.md)).

## The high-level assessment

The high-level assessment answers: *what are we protecting, and where is the unacceptable risk?* Its steps:

1. **Identify the System under Consideration (SuC)** — the boundary of what's being assessed.
2. **High-level risk assessment** — for the SuC as a whole, estimate worst-case consequence and likelihood.
3. **Partition into zones and conduits** — group assets by common security requirements.
4. **Prioritize** — which zones carry unacceptable initial risk and need detailed assessment first.

**Risk = likelihood × consequence**, but in IACS the **consequence** axis includes **safety, environmental, and operational** impact — not just financial/data loss. A consequence that could injure a person or breach a permit dominates the score.

## Hands-On Lab

Python models the risk matrix and SuC scoring. **Cost:** none.

### Lab 4.1 — Define the System under Consideration

**Objective:** Draw the assessment boundary — the first IC33 step.

```bash
python3 - <<'EOF'
# The SuC: the assets, their function, and the boundary of assessment
suc = {
  "name": "Water treatment control system",
  "assets": ["PLC-chlorine", "PLC-flow", "HMI-operator", "historian", "engineering-ws"],
  "boundary": "Level 1-3 (control through site ops); excludes corporate IT (separate SuC)",
  "worst_consequence": "unsafe chlorine dosing -> public health event (SAFETY, not just data)",
}
for k, v in suc.items(): print(f"{k:20}: {v}")
EOF
```

**Expected result:** A defined SuC with an explicit boundary and a **safety-framed worst consequence** — the assessment scope. Getting the boundary right matters: too wide and the assessment never finishes; too narrow and a critical conduit falls outside it. The worst consequence being a *safety* event (not data loss) is the OT hallmark.

**Negative test:** An SuC boundary that excludes the IT/OT conduit "because it's IT's job" — the boundary must include the interfaces you depend on; orphaning the conduit hides the highest-risk path.

**Cleanup:** None.

### Lab 4.2 — The IACS risk matrix

**Objective:** Score initial risk with a consequence axis that includes safety.

```bash
python3 - <<'EOF'
# 5x5 risk matrix; consequence includes safety/environmental/operational, not just $$
def risk(likelihood, consequence):   # each 1..5
    score = likelihood * consequence
    band = "LOW" if score <= 6 else "MEDIUM" if score <= 12 else "HIGH" if score <= 19 else "UNACCEPTABLE"
    return score, band
scenarios = [
  ("Malware from USB on engineering WS -> PLC logic change", 3, 5),   # safety consequence = 5
  ("Recon scan of historian",                                4, 1),
  ("Ransomware on HMI halts operator visibility",            3, 4),
]
for s, l, c in scenarios:
    score, band = risk(l, c)
    print(f"[{band:12}] L{l} x C{c} = {score:2}  {s}")
EOF
```

**Expected result:**

```text
[HIGH        ] L3 x C5 = 15  Malware from USB ... -> PLC logic change
[LOW         ] L4 x C1 =  4  Recon scan of historian
[MEDIUM      ] L3 x C4 = 12  Ransomware on HMI ...
```

The USB→PLC-logic scenario scores HIGH despite moderate likelihood, because its **safety consequence** is maximal — the matrix surfaces exactly the OT-specific risks IT scoring would under-rate. High/unacceptable scenarios feed the detailed assessment.

**Negative test:** A consequence axis that only counts data breach — the PLC-logic-change scenario would score LOW (no data lost), hiding the real danger; the IACS consequence axis must include safety/operational impact.

**Cleanup:** None.

### Lab 4.3 — Partition and prioritize

**Objective:** Group assets into zones and rank them for detailed assessment.

```bash
python3 - <<'EOF'
# Partition the SuC into zones; prioritize by initial (high-level) risk
zones = {
  "Control zone (PLCs)":        {"initial_risk": "HIGH", "assets": ["PLC-chlorine","PLC-flow"]},
  "Supervisory zone (HMI)":     {"initial_risk": "MEDIUM", "assets": ["HMI-operator"]},
  "Site zone (historian, WS)":  {"initial_risk": "MEDIUM", "assets": ["historian","engineering-ws"]},
  "IT/OT DMZ conduit":          {"initial_risk": "HIGH", "assets": ["dmz-broker"]},
}
order = sorted(zones.items(), key=lambda z: 0 if z[1]["initial_risk"]=="HIGH" else 1)
print("Detailed-assessment priority order:")
for name, z in order:
    print(f"  [{z['initial_risk']:6}] {name}")
EOF
```

**Expected result:** The control zone and IT/OT DMZ conduit rank first for detailed assessment (HIGH initial risk) — partitioning turns one big SuC into scoped, prioritized units of work. The high-level assessment's product is this **prioritized list of zones/conduits**, handed to the detailed assessment.

**Negative test:** Skipping the high-level pass and jumping to a detailed assessment of everything at once — you drown in scope and may spend effort on a LOW-risk zone before the HIGH one; prioritization is the point of the high-level stage.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The System under Consideration and its boundary defined.
- [ ] The IACS risk matrix (consequence includes safety/operational) applied.
- [ ] The SuC partitioned into zones/conduits and prioritized for detailed assessment.
