# Chapter 08: Maintenance (IC37) — Operations and Maintenance

## Learning Objectives

- Cover the IC37 Maintenance Specialist: operating and maintaining IACS security over the lifecycle.
- Understand OT patch management, monitoring, incident response, and audit.
- Model keeping SL-Achieved intact as the plant changes.

## The exam in brief

**Certificate 4 — Cybersecurity Maintenance Specialist** (course **IC37**) maps to the **Operate/Maintain** phase and to **IEC 62443-2-1** (the asset owner's security program) and **2-3** (patch management). Design produces a secure system *once*; maintenance keeps it secure for the 15–30 years it runs, as assets, threats, and staff change. The theme: **SL-Achieved decays without active maintenance**, and IC37 is how you keep it at target.

## The operations discipline

| Activity | OT-specific practice |
|:---|:---|
| **Patch management (2-3)** | Test in a lab; apply in change windows; virtual-patch what you can't touch; track vendor advisories |
| **Monitoring** | Passive network monitoring, anomaly detection on OT protocols, log aggregation from Levels 1–3 |
| **Incident response** | OT-aware IR: containment that preserves safety/availability; coordinate with operations |
| **Backup & recovery** | Tested restores of PLC logic, HMI configs, and historian data; offline/immutable copies |
| **Audit & assessment** | Periodic re-assessment; verify SL-A still meets SL-T after changes |
| **Change management** | Every change re-evaluated against the CRS — the top cause of SL decay |

## Hands-On Lab

Python and free primitives model OT operations. **Cost:** none.

### Lab 8.1 — OT patch decision workflow

**Objective:** Decide how to handle a vulnerability the OT way.

```bash
python3 - <<'EOF'
# The OT patch decision: patch, virtual-patch, or accept — driven by criticality + patchability
def decide(asset, patchable, criticality, exploit_reachable):
    if not exploit_reachable: return "MONITOR (not reachable through conduits) — schedule at next window"
    if patchable and criticality != "safety": return "PATCH in next change window (lab-test first)"
    return "VIRTUAL PATCH at conduit + monitor (asset unpatchable or safety-critical)"
print("HMI, patchable, ops:      ", decide("HMI", True,  "ops",    True))
print("safety PLC, patchable:    ", decide("safety-PLC", True, "safety", True))
print("EOL RTU, unpatchable:     ", decide("EOL-RTU", False, "ops", True))
print("legacy switch, not reachable:", decide("switch", False, "ops", False))
EOF
```

**Expected result:** Differentiated decisions — patch the HMI in a window, virtual-patch the safety PLC and the EOL RTU, monitor the unreachable switch. OT patching is **never** "auto-update"; it is a risk-and-availability decision per asset, with virtual patching and monitoring as first-class options. This is IC37's core judgment.

**Negative test:** Applying an IT patch-Tuesday auto-update policy to the control network — an untested patch can halt production or a safety function; OT patching is deliberate, tested, and windowed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Passive OT monitoring

**Objective:** Detect anomalies on the control network without touching traffic (FR6).

```bash
python3 - <<'EOF'
# Passive monitor: baseline normal OT behavior, flag deviations (no active interference)
baseline = {"masters":{"10.2.0.10"}, "function_codes":{3,4,6,16}, "cycle_ms":100}
observed = [
  ("10.2.0.10", 3,  100),   # normal read
  ("10.9.9.9",  3,  100),   # NEW master (not in baseline) -> alert
  ("10.2.0.10", 5,  100),   # NEW function code (force single coil / write) -> alert
  ("10.2.0.10", 3,   10),   # abnormal cycle time (10x faster) -> alert
]
for src, fc, cyc in observed:
    flags = []
    if src not in baseline["masters"]: flags.append("unknown master")
    if fc not in baseline["function_codes"]: flags.append(f"unexpected function code {fc}")
    if cyc < baseline["cycle_ms"] // 2: flags.append("abnormal timing")
    print(f"{src} fc={fc} cyc={cyc}ms -> {'ALERT: '+', '.join(flags) if flags else 'normal'}")
EOF
```

**Expected result:** The known master doing known reads is normal; a new master, an unexpected write function code, and abnormal timing all alert. Passive monitoring **baselines normal OT behavior** (masters, function codes, cadence) and flags deviation — detection (FR6) without the availability risk of inline blocking. This is what the OT-monitoring products (Claroty, Nozomi, TXOne) automate, and IC37 expects you to operate.

**Negative test:** Deploying an inline IPS that blocks "anomalies" on the control network — a false positive drops legitimate control traffic and can trip the process; OT detection is passive-first, with response coordinated through operations.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Verify SL hasn't decayed after a change

**Objective:** Re-check SL-Achieved after a plant change — the top cause of drift.

```bash
python3 - <<'EOF'
# A change (added a vendor remote-access conduit) — did it break the design's SL-A?
FRS = ["IAC","UC","SI","DC","RDF","TRE","RA"]
sl_t = {"IAC":3,"UC":3,"SI":3,"DC":1,"RDF":3,"TRE":2,"RA":3}
sl_a_after_change = {"IAC":3,"UC":3,"SI":3,"DC":1,"RDF":1,"TRE":2,"RA":3}  # RDF dropped: new open conduit
print("Post-change SL verification:")
regressions = []
for fr in FRS:
    if sl_a_after_change[fr] < sl_t[fr]:
        regressions.append(fr); print(f"  FR {fr}: SL-A {sl_a_after_change[fr]} < SL-T {sl_t[fr]}  <-- REGRESSION")
    else:
        print(f"  FR {fr}: OK")
print(f"\n{'CHANGE REJECTED — ' + ', '.join(regressions) + ' regressed' if regressions else 'change preserves SL'}")
EOF
```

**Expected result:** The added remote-access conduit dropped FR5 (restricted data flow) below target — a regression the post-change verification catches. **Change management is where SL decays**: every change must be re-evaluated against the CRS, or the secure design erodes one convenient exception at a time. IC37 makes this verification routine.

**Negative test:** Approving the vendor conduit without re-verifying SL — the plant now has an unmonitored path into control that no risk assessment sanctioned; the maintenance discipline exists to prevent exactly this drift.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] OT patch decision workflow (patch/virtual-patch/monitor) drilled.
- [ ] Passive OT monitoring (baseline + anomaly) modeled.
- [ ] Post-change SL verification (catching decay) understood — the maintenance core.
