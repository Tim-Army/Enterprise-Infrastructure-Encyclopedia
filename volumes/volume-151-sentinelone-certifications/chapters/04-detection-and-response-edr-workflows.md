# Chapter 04: Detection and Response — EDR Workflows

## Learning Objectives

- Walk the incident-response workflow: triage, scope, contain, remediate.
- Understand proactive threat hunting versus reactive detection.
- Apply one-click response actions (kill, quarantine, isolate).
- Recognize the human's role alongside autonomous response.

*Cert relevance: the IR workflow and threat hunting are the core of **SIREN** and **THP** — the practical skills the simulations test.*

## The incident-response workflow

Even with autonomous response ([Chapter 2](02-autonomous-endpoint-protection.md)) handling machine-speed containment, the **human incident responder** runs a workflow — validating, scoping, and closing out incidents. The standard sequence, and what [SIREN](01-the-sentinelone-university-program.md) validates:

| Step | Question | Action |
|:---|:---|:---|
| **Triage** | Is this real and how bad? | Assess the Storyline, confirm malicious, set priority |
| **Scope** | How far did it spread? | Find every affected endpoint, account, and asset |
| **Contain** | Stop the bleeding | Isolate devices, kill processes, disable accounts |
| **Remediate** | Undo the damage | Quarantine, remove persistence, [roll back (Chapter 5)](05-rollback-and-remediation.md) |
| **Recover & learn** | Return to normal, prevent recurrence | Restore, tune policy, document |

The [Storyline (Chapter 3)](03-storyline-autonomous-correlation.md) accelerates every step: triage reads one narrative, scope follows the correlated spread, and containment can act on the whole story at once. The lab walks the workflow.

## Threat hunting

**Detection** is reactive — you respond to what the system flags. **Threat hunting** is *proactive* — you *go looking* for threats that have not triggered an alert, on the hypothesis that a sophisticated attacker may be present but quiet. A hunter queries the endpoint telemetry ("show me every process that made an outbound connection to a newly-registered domain," "find PowerShell spawned by Office apps") to surface suspicious activity that automated detection did not flag.

Threat hunting is the **THP** certification's focus and the mark of a mature SOC: you do not wait to be attacked, you assume compromise and hunt for it. SentinelOne's rich endpoint telemetry (every process, file, network event) and query capability are the hunter's tools. The lab models a hunt.

## One-click response

When a responder acts, SentinelOne provides **one-click response actions** on an endpoint or a whole Storyline:

- **Kill** — terminate the malicious process (and its tree).
- **Quarantine** — isolate the malicious file so it cannot execute.
- **Isolate** (network containment) — cut the device off from the network (except the management channel) to stop lateral movement while you investigate.
- **Remediate / Rollback** — undo the changes ([Chapter 5](05-rollback-and-remediation.md)).

These are *deliberate human actions* complementing the autonomous ones — for cases needing judgment, or to contain a broader incident. The skill the certifications test is knowing *which* action, *when*, and *at what scope*. The lab is covered within the workflow exercise.

## Hands-On Lab

Python models IR workflows. **Cost:** none.

### Lab 4.1 — Walk the incident-response workflow

**Objective:** Take an incident from triage to remediation.

```bash
python3 - <<'EOF'
# an incident arrives as a Storyline; walk the IR steps
STORYLINE = {
  "id": "S-4471",
  "narrative": "invoice.doc -> powershell -> payload.exe -> injected explorer -> C2 + encrypting",
  "endpoints_affected": ["ws-014", "ws-022", "srv-03"],   # scope: spread
  "malicious_process": "payload.exe",
  "persistence": "scheduled task 'Updater'",
}
print(f"INCIDENT {STORYLINE['id']}\n")
print("1. TRIAGE — is it real, how bad?")
print(f"   Storyline: {STORYLINE['narrative']}")
print("   -> confirmed malicious (C2 + encryption). Priority: CRITICAL.\n")
print("2. SCOPE — how far did it spread?")
print(f"   affected endpoints: {STORYLINE['endpoints_affected']} (3 hosts, incl. a SERVER)")
print("   -> not one machine; lateral movement in progress.\n")
print("3. CONTAIN — stop the bleeding")
for ep in STORYLINE['endpoints_affected']:
    print(f"   ISOLATE {ep} (network containment — cut off except mgmt channel)")
print(f"   KILL {STORYLINE['malicious_process']} process tree on all 3\n")
print("4. REMEDIATE — undo the damage")
print(f"   quarantine payload.exe; remove persistence ('{STORYLINE['persistence']}')")
print("   ROLLBACK encrypted files (Chapter 5)\n")
print("5. RECOVER & LEARN")
print("   de-isolate once clean; tune policy to block the initial doc->powershell;")
print("   document the Storyline as an IOC set.\n")
print("The workflow SIREN validates: TRIAGE (read the story) -> SCOPE (follow the")
print("correlated spread — note it hit a SERVER and 2 workstations, not just one) ->")
print("CONTAIN (isolate + kill, at the RIGHT scope: all 3 hosts) -> REMEDIATE (quarantine,")
print("kill persistence, roll back) -> RECOVER. Storyline accelerates every step — you")
print("scope by following the correlation, and contain the whole attack at once. The")
print("autonomous agent already bought you time; the human closes it out with judgment.")
EOF
```

**Expected result:** An incident walked from triage (confirm the Storyline is malicious) through scope (three affected hosts including a server), containment (isolate and kill at the right scope), remediation (quarantine, remove persistence, rollback), to recovery. The workflow lesson is the SIREN discipline — Storyline accelerates each step, scoping follows the correlated spread, and the human closes out with judgment after the autonomous agent has bought time.

**Negative test:** Containing only the first endpoint that alerted. Scoping shows the attack spread to three hosts including a server — responding to one leaves the lateral movement active; the workflow requires scoping the full spread before containing.

**Cleanup:** None.

### Lab 4.2 — Proactive threat hunting

**Objective:** Hunt for a quiet threat that did not trigger an alert.

```bash
python3 - <<'EOF'
# endpoint telemetry a hunter queries; nothing here fired an automated alert
TELEMETRY = [
  # process,            parent,        network,                    signed
  ("chrome.exe",        "explorer.exe","cdn.example.com",          True),
  ("powershell.exe",    "winword.exe", "185.220.new-domain.xyz",   True),   # Office->PS + new domain
  ("svchost.exe",       "services.exe","microsoft.com",            True),
  ("updater.exe",       "explorer.exe","45.9.division.ru",         False),   # unsigned + odd geo
  ("teams.exe",         "explorer.exe","teams.microsoft.com",      True),
]
print("HUNT hypothesis: 'a quiet attacker may be living off the land — look for Office")
print("apps spawning shells, and unsigned processes calling new/odd domains.'\n")
findings = []
for proc, parent, net, signed in TELEMETRY:
    flags = []
    if proc == "powershell.exe" and parent in ("winword.exe","excel.exe","outlook.exe"):
        flags.append("Office spawned PowerShell (living-off-the-land)")
    if not signed:
        flags.append("UNSIGNED binary")
    if any(x in net for x in ["new-domain", ".ru", ".xyz"]) and "microsoft" not in net:
        flags.append(f"suspicious network: {net}")
    if flags:
        findings.append((proc, flags))
print(f"{'process':16}findings")
for proc, flags in findings:
    print(f"   {proc:16}{'; '.join(flags)}")
print("\nThe hunt surfaced 2 suspicious processes that NO automated alert fired on:")
print("  powershell spawned by WINWORD + calling a newly-registered domain — classic")
print("     phishing-macro living-off-the-land. Individually 'signed powershell' and")
print("     'a network connection' look benign; the COMBINATION + context is the tell.")
print("  updater.exe — UNSIGNED, calling an odd geography. Worth investigating.")
print("\nThis is THREAT HUNTING (the THP cert): you don't wait for an alert — you form a")
print("HYPOTHESIS about attacker behavior and query the telemetry to test it, surfacing")
print("quiet threats automated detection missed. SentinelOne's rich per-process/")
print("network telemetry is the hunter's data. Assume compromise; go look.")
EOF
```

**Expected result:** A hypothesis-driven query over endpoint telemetry surfacing an Office-spawned PowerShell calling a new domain and an unsigned process with odd network activity — neither of which fired an automated alert. The threat-hunting lesson is the THP discipline: form a hypothesis about attacker behavior, query the rich telemetry to test it, and surface quiet threats proactively rather than waiting to be alerted.

**Negative test:** Waiting for automated detection to flag everything. A patient attacker living off the land (signed PowerShell, normal-looking connections) may never trigger an alert — only proactive hunting on a behavioral hypothesis surfaces them.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The IR workflow (triage, scope, contain, remediate, recover) walked, accelerated by Storyline at each step.
- [ ] Threat hunting understood as proactive, hypothesis-driven searching versus reactive detection.
- [ ] One-click response actions (kill, quarantine, isolate) understood, chosen by which/when/what-scope.
- [ ] The human's role recognized as judgment and closure alongside the agent's autonomous containment.
