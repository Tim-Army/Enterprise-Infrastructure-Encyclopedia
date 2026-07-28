# Chapter 07: Industrial Control Systems Security

## Learning Objectives

- Describe the ICS/OT security challenge and the GIAC ICS credentials.
- Apply the Purdue model and safe OT segmentation (GICSP).
- Respond to ICS incidents (GRID).
- Protect critical infrastructure to standards (GCIP).
- Complete a walkthrough for each ICS domain.

## Theory and Architecture

The **Industrial Control Systems (ICS) Security** focus area validates protecting operational
technology (OT) — the systems that run power, water, manufacturing, and other physical processes,
where **safety and availability** outrank confidentiality. **GICSP (Global Industrial Cyber Security
Professional)** is the flagship, bridging IT, OT, and engineering: field devices (PLCs/RTUs),
protocols (Modbus, DNP3), the **Purdue reference model** of network levels, and safe segmentation.
**GRID (Response and Industrial Defense)** covers **ICS incident response and active defense** —
detecting and responding to threats in OT without disrupting the process. **GCIP (Critical
Infrastructure Protection)** covers the regulatory and standards side — notably **NERC CIP** for the
electric sector — mapping controls to compliance requirements. Because OT devices are fragile and
uptime is safety-critical, ICS security emphasizes **passive monitoring**, careful change control,
and network **segmentation** over intrusive scanning. This chapter teaches each with a hands-on
defensive walkthrough (Purdue-model reasoning, passive OT monitoring, CIP mapping).

## Design Considerations

Segment OT from IT using the **Purdue model** levels and a DMZ (GICSP). Prefer **passive** monitoring
in OT — active scans can crash fragile PLCs. Plan IR that **preserves the process** (safety first)
(GRID). Map controls to **NERC CIP / IEC 62443** where they apply (GCIP). Coordinate with
**engineering** — OT security is a joint discipline.

## Implementation and Automation

The labs reason about the Purdue model, plan passive monitoring, and map a CIP control.

## Validation and Troubleshooting

Confirm the ICS map:

```text
GICSP = IT/OT/engineering bridge (PLC/RTU, Modbus/DNP3, Purdue model, segmentation). GRID = ICS IR + active defense (safety-first).
GCIP = critical-infrastructure compliance (NERC CIP / IEC 62443). OT priority: Safety > Availability > Integrity > Confidentiality.
```

Common pitfalls: **active-scanning** an OT network (can halt a plant); and applying IT patch cadence
to OT (change windows are safety-gated).

## Security and Best Practices

Segment by **Purdue** level, monitor OT **passively**, put **safety first** in IR, and map to the
applicable **standards** (NERC CIP / IEC 62443). Work with engineering. All practice is defensive
and non-disruptive.

## Hands-On Lab

ICS walkthroughs. **Shared prerequisites** — Linux with `python3`, in a lab (no real OT devices).
**Cost:** none.

### Lab 7.1 — GICSP: place assets in the Purdue model

**Objective:** Segment IT from OT.

```python
python3 - <<'PY'
purdue={0:"field devices (sensors/actuators)",1:"controllers (PLC/RTU)",2:"supervisory (HMI/SCADA)",
        3:"site operations (historian)","3.5":"IT/OT DMZ",4:"enterprise IT",5:"internet"}
for lvl,desc in purdue.items(): print(f"Level {lvl}: {desc}")
print("GICSP: no direct Level 5<->Level 0/1; traffic passes the Level 3.5 DMZ")
PY
```

**Expected result:** assets mapped to **Purdue levels** with the IT/OT DMZ between — safe OT
segmentation (GICSP).

**Negative test:** allow enterprise IT (Level 4) to reach a PLC (Level 1) directly; that bridges IT
threats into OT — enforce the **DMZ** boundary.

**Cleanup:** none.

### Lab 7.2 — GRID: plan safety-first ICS incident response

**Objective:** Respond without disrupting the process.

```python
python3 - <<'PY'
priorities=["Safety (people/plant)","Availability (keep process running)","Integrity","Confidentiality"]
for i,p in enumerate(priorities,1): print(f"{i}. {p}")
print("GRID: containment must not trip the process; coordinate with engineering before isolating OT")
PY
```

**Expected result:** the **inverted CIA priority** (safety/availability first) guiding IR — the GRID
approach.

**Negative test:** yank an infected HMI offline mid-process like an IT box; that could cause an
unsafe state — **coordinate** and prioritize safety.

**Cleanup:** none.

### Lab 7.3 — GCIP: map a control to a standard

**Objective:** Tie a control to compliance.

```python
python3 - <<'PY'
mapping={"NERC CIP-005 (Electronic Security Perimeter)":"OT firewall + DMZ at Level 3.5",
         "NERC CIP-007 (System Security Mgmt)":"patch/AV/logging on cyber assets",
         "NERC CIP-010 (Config Change Mgmt)":"baseline + monitored changes",
         "IEC 62443 zones & conduits":"segment OT into zones with controlled conduits"}
for req,ctrl in mapping.items(): print(f"{req}\n   -> {ctrl}")
PY
```

**Expected result:** controls mapped to **NERC CIP / IEC 62443** requirements — the GCIP compliance
view.

**Negative test:** claim compliance without mapping controls to specific requirements; auditors need
the **traceability** — map each control.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ICS Security spans the IT/OT bridge and Purdue segmentation (GICSP), safety-first ICS incident
response (GRID), and critical-infrastructure compliance (GCIP) — protecting fragile, safety-critical
OT with passive monitoring and careful segmentation.

- [ ] I can place assets in the Purdue model (GICSP).
- [ ] I can plan safety-first ICS IR (GRID).
- [ ] I can map a control to NERC CIP / IEC 62443 (GCIP).
- [ ] I understand why OT prioritizes safety and availability.
- [ ] I completed Labs 7.1–7.3 including each negative test.
