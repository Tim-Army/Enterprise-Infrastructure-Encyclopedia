# Chapter 03: XDR — Cross-Layer Detection and Response

## Learning Objectives

- Explain XDR and how it extends beyond EDR.
- Describe cross-layer telemetry correlation.
- Understand the attack story and root-cause analysis.
- Recognize automated and analyst-driven response.

*Cert relevance: XDR is the core of Trend Vision One and central to the certifications.*

## What XDR is

**XDR (Extended Detection and Response)** is the core of [Trend Vision One (Ch 2)](02-trend-vision-one.md) — extending detection and response **beyond the endpoint** to correlate signals across **all** security layers: endpoint, **email**, **network**, **cloud**, and **identity**. Where **EDR** watches one domain (the endpoint), XDR **collects and correlates telemetry from every domain** into one view. This matters because sophisticated attacks are **multi-stage and cross-layer** — no single-domain tool sees the whole thing, but XDR does. Trend Micro was an early XDR proponent, and it is what the certifications increasingly emphasize. The lab models cross-layer correlation.

## Cross-layer telemetry correlation

XDR's mechanism is **correlation**. Each layer produces telemetry — the endpoint sees process execution, email sees messages, network sees connections, cloud sees API calls, identity sees logins. Individually, many of these events look **minor**. XDR **correlates** them — by user, host, time, and causal relationship — to reveal that a set of individually-low-severity events is actually **one coordinated attack**. A phishing email (email), an executed macro (endpoint), an anomalous login (identity), and data exfiltration (cloud) become a **single, high-confidence detection** that no siloed tool would raise. Correlation across layers is XDR's defining capability. The lab models it.

## The attack story and root cause

A key XDR output is the **attack story** (or execution graph) — a **visual, connected narrative** of an attack from its **root cause** through every step. Instead of a pile of disconnected alerts, the analyst sees: *this* phishing email led to *this* process which made *this* connection which accessed *this* cloud resource. This **root-cause analysis** lets responders understand the **full scope** of an incident — every affected asset, the entry point, and the attacker's path — so they can respond **completely** rather than cleaning one symptom while the attack persists elsewhere. Seeing the whole story is what makes response effective. The lab models the attack story.

## Automated and analyst-driven response

XDR closes the loop with **response** — both **automated** (playbooks that contain a threat the moment it's confirmed: isolate a host, block an account, quarantine a file) and **analyst-driven** (investigation and manual actions from the console). Automated response acts at **machine speed** for clear threats; analysts handle the nuanced cases. Combined with the attack story, response can address the **entire** incident across all layers — isolating the endpoint, disabling the identity, and revoking the cloud access together. Detection plus coordinated response across layers is the value XDR delivers. The lab synthesizes.

## Hands-On Lab

Python models XDR correlation and response. **Cost:** none.

### Lab 3.1 — Correlate cross-layer telemetry into one attack story

**Objective:** See XDR turn scattered signals into a response-ready attack story.

```bash
python3 - <<'EOF'
# telemetry from multiple layers, same user 'jsmith' — individually minor, together an attack
telemetry = [
  {"t": "09:00", "layer": "email",    "event": "attachment opened (invoice.xlsm)", "sev": "low"},
  {"t": "09:01", "layer": "endpoint", "event": "excel spawned powershell",          "sev": "medium"},
  {"t": "09:03", "layer": "identity", "event": "jsmith login from new ASN",          "sev": "low"},
  {"t": "09:05", "layer": "cloud",    "event": "bulk download from file store",       "sev": "medium"},
]
print("Cross-layer telemetry (same user jsmith) — each event ALONE looks minor:")
for e in telemetry:
    print(f"   {e['t']} [{e['layer']:8}] {e['event']}  (sev: {e['sev']})")
# XDR correlation -> one attack story
print("\nXDR CORRELATION (by user/time/causality) -> ONE ATTACK STORY (root cause -> steps):")
story = " -> ".join(f"{e['layer']}:{e['event'].split('(')[0].strip()}" for e in telemetry)
print(f"   {story}")
print("   severity: HIGH (correlated multi-stage attack) — no single-layer tool would raise this\n")
# response across ALL layers, complete
print("RESPONSE (automated + analyst-driven), across ALL affected layers:")
for action in ["isolate jsmith's endpoint", "disable jsmith identity (revoke sessions)",
               "revoke cloud file-store access", "quarantine invoice.xlsm fleet-wide"]:
    print(f"   - {action}")
print("   -> the ENTIRE incident addressed (entry point + every affected asset), not one symptom\n")
print("XDR extends beyond EDR (one domain) to CORRELATE telemetry across endpoint+email+network+")
print("cloud+identity into one ATTACK STORY with ROOT CAUSE + full scope. Then RESPOND across ALL")
print("layers (automated at machine speed + analyst-driven) — completely, not symptom-by-symptom.")
print("Multi-stage attacks are invisible to siloed tools; XDR is the core of Trend Vision One.")
EOF
```

**Expected result:** Four individually-minor cross-layer events (email attachment, endpoint PowerShell, anomalous login, cloud bulk download) for the same user correlated by XDR into one high-severity attack story with root cause, then a coordinated response across all affected layers (isolate endpoint, disable identity, revoke cloud access, quarantine the file). The XDR lesson is that it extends beyond single-domain EDR to correlate telemetry across all layers into a root-cause attack story and respond completely across every affected layer — catching multi-stage attacks siloed tools miss.

**Negative test:** Investigating each layer's alerts separately. The individually-minor events never connect, so the multi-stage attack is missed and response addresses one symptom while the attack persists; XDR correlates them into one story and enables complete cross-layer response.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] XDR understood — extending detection and response beyond EDR to all security layers.
- [ ] Cross-layer telemetry correlation understood — connecting individually-minor events into one attack.
- [ ] The attack story and root-cause analysis understood — seeing the full scope of an incident.
- [ ] Automated and analyst-driven response understood — addressing the entire incident across layers.
