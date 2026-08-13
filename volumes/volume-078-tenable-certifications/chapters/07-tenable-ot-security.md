# Chapter 07: Tenable OT Security

## Learning Objectives

- Describe the OT/ICS security challenge and Tenable OT Security.
- Build asset inventory with passive detection.
- Detect vulnerabilities and anomalies safely in OT.
- Segment IT and OT for exposure management.
- Complete a walkthrough for each OT Security topic.

## Theory and Architecture

**Tenable OT Security** (the basis of the **Tenable One OT Exposure Certification**) protects
**operational technology (OT)** — the industrial control systems (PLCs, RTUs, HMIs, SCADA) that run
physical processes, where **safety and availability** outrank confidentiality and where active
scanning can crash fragile devices. Tenable OT therefore relies primarily on **passive monitoring** —
watching network traffic to build a complete **asset inventory** (device, firmware, protocol) without
touching the devices — supplemented by careful, device-safe **active queries** where supported. It
identifies **vulnerabilities** in OT devices, detects **anomalies and unauthorized changes** (a new
PLC program, an unexpected controller command), and maps OT into the **exposure-management** picture.
Because OT and IT increasingly converge, Tenable OT provides visibility across the boundary while
respecting OT's safety-first constraints. This chapter teaches each with a hands-on defensive
walkthrough (passive inventory, OT-safe detection, and IT/OT segmentation).

## Design Considerations

Prefer **passive** monitoring in OT; use active queries only where **device-safe**. Build a complete
**asset inventory** (the foundation of OT security). Detect **anomalies and unauthorized changes** to
controllers. **Segment** IT from OT (Purdue model). Prioritize by **process safety and criticality**,
not just CVSS.

## Implementation and Automation

The labs build passive inventory, detect an OT anomaly, and reason about segmentation.

## Validation and Troubleshooting

Confirm the OT model:

```text
Tenable OT Security: OT/ICS (PLC/RTU/HMI/SCADA); safety & availability first. Passive monitoring builds asset inventory (device/firmware/protocol) without touching devices; device-safe active queries where supported.
Detects OT vulnerabilities + anomalies/unauthorized changes. Segment IT/OT (Purdue). Prioritize by process safety.
```

Common pitfalls: **active-scanning** fragile PLCs (can halt a process); and no **asset inventory**
(you can't secure unknown OT devices).

## Security and Best Practices

Monitor OT **passively**, build a complete **inventory**, detect **unauthorized changes**, **segment**
IT/OT, and prioritize by **process safety**. Coordinate with engineering. All practice is defensive
and non-disruptive.

## Hands-On Lab

OT Security walkthroughs. **Shared prerequisites** — `python3`, in a lab (no real OT devices). **Cost:**
none.

### Lab 7.1 — Build passive OT asset inventory

**Objective:** Inventory without touching devices.

```python
python3 - <<'PY'
# Passive observation of OT traffic -> asset inventory (no active probing)
observed=[{"ip":"192.168.1.10","type":"PLC","vendor":"Siemens","proto":"S7","firmware":"4.2"},
          {"ip":"192.168.1.20","type":"HMI","vendor":"Rockwell","proto":"EtherNet/IP"}]
for a in observed: print(a)
print("Tenable OT: passive monitoring identifies devices/firmware/protocols safely")
PY
```

**Expected result:** an OT **asset inventory** built passively — the OT security foundation.

**Negative test:** actively scan the PLCs to inventory them; that can crash the process — use
**passive** monitoring.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Detect an unauthorized OT change

**Objective:** Catch controller tampering.

```python
python3 - <<'PY'
baseline={"plc-10":{"program_hash":"abc123","mode":"RUN"}}
observed={"plc-10":{"program_hash":"def456","mode":"PROGRAM"}}   # changed!
for plc in baseline:
    if observed[plc]["program_hash"]!=baseline[plc]["program_hash"] or observed[plc]["mode"]!=baseline[plc]["mode"]:
        print(f"ALERT {plc}: program/mode changed ({baseline[plc]} -> {observed[plc]})")
print("Tenable OT: unauthorized PLC program/mode change = high-priority OT anomaly")
PY
```

**Expected result:** the **unauthorized PLC change** detected — OT anomaly detection.

**Negative test:** monitor only for IT-style malware in OT; **controller changes** are the real OT
threat — watch for them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Prioritize OT vulnerabilities by process safety

**Objective:** Weight by impact on the process.

```python
python3 - <<'PY'
vulns=[{"device":"safety-plc","cvss":7.0,"process_role":"safety instrumented system","priority":"CRITICAL"},
       {"device":"lobby-hmi","cvss":9.0,"process_role":"display only","priority":"low"}]
for v in vulns: print(f"{v['device']:12} CVSS {v['cvss']} role={v['process_role']:26} -> {v['priority']}")
print("OT: a lower-CVSS vuln on a SAFETY system outranks a higher-CVSS one on a display")
PY
```

**Expected result:** the safety-system vuln prioritized over a higher-CVSS display issue — OT
process-safety prioritization.

**Negative test:** prioritize OT purely by **CVSS**; you may fix a lobby display before a safety
controller — weight by **process safety**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Reason about IT/OT segmentation

**Objective:** Contain the boundary.

```python
python3 - <<'PY'
def allowed(src,dst):
    return not (src=="IT" and dst=="OT-Level1")   # no direct IT -> controllers
for pair in [("IT","OT-DMZ"),("OT-DMZ","OT-Level2"),("IT","OT-Level1")]:
    print(pair, "ALLOW" if allowed(*pair) else "DENY (must pass OT DMZ)")
print("Tenable OT + Purdue: no direct IT-to-controller path; enforce the OT DMZ")
PY
```

**Expected result:** IT→controller **denied**, boundary traffic via the **OT DMZ** — safe IT/OT
segmentation.

**Negative test:** allow IT to reach controllers directly; IT threats cross into OT — enforce the
**DMZ**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Tenable OT Security protects fragile OT with passive asset inventory, unauthorized-change detection,
process-safety-weighted prioritization, and IT/OT segmentation — extending exposure management into
operational technology without disrupting it.

- [ ] I can build passive OT asset inventory.
- [ ] I can detect an unauthorized OT change.
- [ ] I can prioritize OT vulns by process safety.
- [ ] I can reason about IT/OT segmentation.
- [ ] I completed Labs 7.1–7.4 including each negative test.
