# Chapter 05: VMDR — Response: Patch Management and TruRisk Eliminate

## Learning Objectives

- Close the VMDR loop with integrated response.
- Deploy patches with Qualys Patch Management.
- Apply non-patch mitigations with TruRisk Eliminate.
- Verify remediation and measure reduction.
- Complete a walkthrough for each response topic.

## Theory and Architecture

The **Response** stage completes VMDR — turning findings into fixes **within the same platform**,
using the **Cloud Agent** already deployed for detection. **Qualys Patch Management** correlates each
vulnerability to the **patch that fixes it** and deploys patches directly (no separate patch tool),
scoped by dynamic tags and orchestrated with maintenance windows. But not every risk is fixed by a
patch: **TruRisk Eliminate** adds **non-patch mitigations** — configuration changes, disabling a
vulnerable feature, isolating an asset, or applying a compensating control — for cases where a patch
is unavailable, can't be applied yet (EOL software, change freeze), or is riskier than a mitigation.
The loop is: **detect → prioritize (TruRisk) → respond (patch or mitigate) → verify** by re-assessing.
Closing this loop **within one platform**, driven by the same agent and inventory, is Qualys's key
differentiator — remediation is measured by **risk reduction** (falling TruRisk), not just tickets
opened. This chapter teaches each with a hands-on defensive walkthrough (patch correlation,
mitigation, and verification).

## Design Considerations

Correlate vulnerabilities to **patches** and deploy in **maintenance windows**, scoped by tags. Use
**TruRisk Eliminate** mitigations when patching isn't possible or timely. Prioritize response by
**TruRisk**. **Verify** by re-assessing (the agent confirms the fix). Measure **risk reduction**, not
activity.

## Implementation and Automation

The labs correlate a patch, apply a mitigation, and verify remediation.

## Validation and Troubleshooting

Confirm the response model:

```text
VMDR Response (same platform + Cloud Agent): Patch Management correlates vuln -> patch and deploys (no separate tool), scoped + scheduled. TruRisk Eliminate = non-patch mitigations (config/disable/isolate/compensating control) when patching isn't possible/timely.
Loop: detect -> prioritize -> respond -> verify (re-assess). Measure by risk reduction (falling TruRisk).
```

Common pitfalls: opening tickets in a separate tool and losing the loop; and treating **unpatchable**
risk as unfixable (use **mitigations**).

## Security and Best Practices

Deploy **patches** from the same platform, use **TruRisk Eliminate** mitigations when needed,
prioritize by **TruRisk**, **verify** by re-assessment, and measure **risk reduction**. All work is
defensive.

## Hands-On Lab

Response walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 5.1 — Correlate a vulnerability to a patch

**Objective:** Deploy the right fix.

```python
python3 - <<'PY'
vuln={"qid":91234,"title":"Missing OS security update","fixed_by_patch":"KB5099999"}
deploy={"patch":vuln["fixed_by_patch"],"scope":"tag:Servers","window":"Sat 02:00-04:00","reboot":"if required"}
print("vuln:", vuln)
print("patch job:", deploy)
print("Patch Management: correlate vuln -> patch and deploy from the same platform")
PY
```

**Expected result:** the vulnerability **correlated to a patch** and a scoped, scheduled deploy —
integrated response.

**Negative test:** export the vuln list to a separate patch tool and lose tracking; the **integrated**
loop closes it — patch in-platform.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Apply a non-patch mitigation (TruRisk Eliminate)

**Objective:** Reduce risk without a patch.

```python
python3 - <<'PY'
case={"qid":40001,"title":"Vulnerable legacy service","patch_available":False,
      "mitigation":"disable the service + firewall the port + isolate host"}
print(case)
print("TruRisk Eliminate: when no patch exists, mitigate (disable/config/isolate) to cut risk now")
PY
```

**Expected result:** a **non-patch mitigation** for an unpatchable vulnerability — TruRisk Eliminate.

**Negative test:** leave an unpatchable vuln open because "there's no patch"; a **mitigation** still
reduces risk — apply one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Verify remediation

**Objective:** Confirm the fix took.

```python
python3 - <<'PY'
before={"qid":91234,"status":"active"}
after ={"qid":91234,"status":"fixed"}   # re-assessment by the Cloud Agent
print("before:", before, "-> after:", after)
print("VMDR: the agent re-assesses and confirms 'fixed' -> verified remediation (not just a closed ticket)")
PY
```

**Expected result:** the vulnerability status changed to **fixed** by re-assessment — verified
remediation.

**Negative test:** close the ticket without re-assessing; the vuln may still be present — **verify**
via the agent.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Measure risk reduction

**Objective:** Report outcomes, not activity.

```python
python3 - <<'PY'
metrics={"TruRisk score":"720 -> 540 (down 25%)","exploitable open":"85 -> 30",
         "mean time to remediate (critical)":"9 days","patches deployed":642}
for m,v in metrics.items(): print(f"{m:36}: {v}")
print("VMDR: measure falling risk (TruRisk), not just patch counts")
PY
```

**Expected result:** **risk-reduction metrics** (falling TruRisk) — outcome-based measurement.

**Negative test:** report only "patches deployed"; that's activity, not **risk reduction** — track
TruRisk trend.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VMDR closes the loop within one platform: Patch Management deploys correlated patches and TruRisk
Eliminate applies non-patch mitigations, verified by agent re-assessment and measured by falling
TruRisk — detect, prioritize, respond, verify.

- [ ] I can correlate a vulnerability to a patch.
- [ ] I can apply a non-patch mitigation (TruRisk Eliminate).
- [ ] I can verify remediation.
- [ ] I can measure risk reduction.
- [ ] I completed Labs 5.1–5.4 including each negative test.
