# Chapter 07: Wiz Defend — Detection and Response

## Learning Objectives

- Explain cloud detection and response (CDR) and what Wiz Defend does.
- Understand runtime threat detection with graph context.
- Trace an incident code-to-cloud-to-runtime for faster response.
- Recognize how posture and detection reinforce each other.

*Cert relevance: Wiz Defend is the subject of the **Defend Fundamentals** exam (60 questions / 150 minutes / 2-year validity). This chapter is defensive — detecting and responding to cloud threats.*

> **Defensive framing.** This chapter is about *defending* cloud environments — detecting malicious activity at runtime and responding to it. The mechanisms (detections, investigation, containment) are the tools a SOC and incident-response team use to stop attackers in the cloud. Nothing here is about conducting attacks.

## From posture to detection

Chapters 2–6 were about **posture** — reducing the attack surface *before* anything happens (fixing misconfigurations, vulnerabilities, over-privilege, exposed data). But posture is not perfect: some risk always remains, and attackers act. **Wiz Defend** is the **CDR** (Cloud Detection and Response) pillar — it detects threats *at runtime* and helps you investigate and respond.

Defend adds real-time signals that posture scanning alone does not have: it watches **runtime activity** (process execution, network connections, cloud control-plane API calls, identity behavior) for the signs of an attack in progress — a workload suddenly mining cryptocurrency, an identity enumerating every bucket, an unusual `AssumeRole` from an unexpected geography. This typically uses an **optional lightweight sensor** for real-time workload signals plus the cloud provider's audit logs (like CloudTrail) for control-plane activity.

## Detection with graph context

The difference between Wiz Defend and a standalone cloud-detection tool is, again, **the graph**. A raw detection — "process `xmrig` started on host web-42" — is an alert. The *same* detection with graph context is an **investigation, already half-done**: web-42 is internet-exposed, runs the payment service, its role can reach the customer database, and the same host had a known critical RCE flagged by posture last week. The responder does not start from a hostname; they start from **the blast radius and the likely entry point**, because the graph already holds them.

This is the payoff of the [attack-path work (Chapter 3)](03-attack-paths-and-toxic-combinations.md) turned real: the paths you prioritized in posture are the paths an attacker travels, so when a detection fires, you already know **what it can reach next** and **where to cut**. The lab models enriching a detection with graph context.

## Code-to-cloud-to-runtime

The full Wiz story closes here. When Defend detects a runtime threat, the shared graph lets you trace it **all the way back**:

```text
runtime detection (Defend) → the workload and its cloud posture (Cloud) → the IaC line / PR that introduced the weakness (Code)
```

So an incident does not end at "we contained the crypto-miner." It ends at "we contained it, *and* we found the exposed-vulnerable path it entered through, *and* we fixed the Terraform line so it cannot recur." Detection feeds remediation feeds posture — one loop on one graph. The lab models the full trace.

## Hands-On Lab

Python models defensive detection and response. **Cost:** none.

### Lab 7.1 — Enrich a detection with graph context

**Objective:** Turn a bare alert into a prioritized, half-solved investigation.

```bash
python3 - <<'EOF'
# two runtime detections, identical signal, different graph context
GRAPH = {
  "web-42":    {"exposed": True,  "service": "payments", "reaches": "customer-db (PII)", "prior_posture": "critical RCE (unpatched)"},
  "sandbox-9": {"exposed": False, "service": "dev sandbox", "reaches": "nothing sensitive", "prior_posture": "none"},
}
DETECTIONS = [
  ("crypto-miner (xmrig) started", "web-42"),
  ("crypto-miner (xmrig) started", "sandbox-9"),
]
def triage(host):
    g = GRAPH[host]; score = 0; notes = []
    if g["exposed"]:                       score += 4; notes.append("internet-EXPOSED (entry point)")
    if "PII" in g["reaches"] or "sensitive" in g["reaches"] and "nothing" not in g["reaches"]:
        pass
    if "db" in g["reaches"] or "PII" in g["reaches"]: score += 4; notes.append(f"reaches {g['reaches']}")
    if g["prior_posture"] != "none":       score += 3; notes.append(f"prior finding: {g['prior_posture']} (likely entry)")
    if not notes: notes = ["isolated, no sensitive reach"]
    return score, notes
print("Same detection ('crypto-miner started'), two hosts — context sets the response:\n")
for det, host in DETECTIONS:
    score, notes = triage(host)
    sev = "P1 — INVESTIGATE NOW" if score >= 7 else "P4 — low, contain routinely"
    print(f"   [{host}] {det}")
    print(f"      graph context: {'; '.join(notes)}")
    print(f"      -> risk {score} -> {sev}\n")
print("web-42: exposed + reaches PII + had an unpatched critical RCE last week. The")
print("miner isn't the story — it's a SYMPTOM of a compromise on a path to customer")
print("data, and the RCE is the likely entry. You start the investigation already")
print("knowing the blast radius (customer-db) and the entry (the RCE). CONTAIN web-42,")
print("check the DB for access, patch/rotate.")
print("\nsandbox-9: same miner, but isolated dev box, no sensitive reach, no prior risk.")
print("Annoying, not an emergency. Same alert, opposite response — because the GRAPH")
print("turns a bare detection into an investigation that's already half-done.")
EOF
```

**Expected result:** An identical crypto-miner detection triaged as a P1 on an exposed, PII-reaching host with a prior unpatched RCE, but a low-priority cleanup on an isolated sandbox. The graph-context lesson is that Wiz Defend starts the responder from the blast radius and likely entry point — the same detection is an emergency or an annoyance depending on what the graph says the host can reach.

**Negative test:** Triaging detections by signal alone. Both hosts show "crypto-miner started," so a context-free SOC treats them equally and may burn the first hour on the sandbox while the payments host — on a path to customer PII — spreads.

**Cleanup:** None.

### Lab 7.2 — Code-to-cloud-to-runtime: close the loop

**Objective:** Trace an incident from runtime back to the source, and prevent recurrence.

```bash
python3 - <<'EOF'
# an incident, traced across the three pillars on one graph
incident = {
  "runtime (Defend)": "suspicious AssumeRole + data egress from web-42",
  "cloud (Cloud)":    "web-42 is internet-exposed, unpatched RCE, role reaches customer-db",
  "code (Code)":      "modules/web/main.tf:88 opens 0.0.0.0/0 ingress; app pins vulnerable lib v1.2",
}
print("ONE incident, traced across the three pillars (one Security Graph):\n")
for pillar, detail in incident.items():
    print(f"   {pillar:20} {detail}")
print("\nResponse WITHOUT the loop (detection only):")
print("   - kill the process, isolate web-42. Done?  ...the exposed, vulnerable path")
print("     is still there. Next week a different attacker walks the same route.\n")
print("Response WITH code-to-cloud-to-runtime (Wiz):")
steps = [
  "CONTAIN: isolate web-42, revoke the abused role's session (stop the bleeding)",
  "SCOPE:   graph shows what the role could reach -> audit customer-db for access",
  "ENTRY:   posture shows the unpatched RCE + open ingress -> that's how they got in",
  "ROOT:    trace to modules/web/main.tf:88 (0.0.0.0/0) + vulnerable lib v1.2",
  "PREVENT: fix the IaC line + bump the lib -> every env from this module is corrected",
]
for i, s in enumerate(steps, 1):
    print(f"   {i}. {s}")
print("\nThe incident doesn't end at containment — it ends at the FIXED TERRAFORM LINE,")
print("so it cannot recur. Detection (Defend) -> blast radius + entry (Cloud) -> root")
print("cause (Code) -> a permanent fix. That full loop, on ONE graph, is Wiz's thesis:")
print("posture and detection reinforce each other. The paths you hardened are the paths")
print("attackers travel, and every incident makes your posture stronger.")
EOF
```

**Expected result:** An incident traced from a runtime detection through the cloud posture that explains the blast radius and entry point to the exact IaC line that introduced the weakness, closing with a source fix that prevents recurrence. The code-to-cloud-to-runtime lesson is that one graph turns response from "contain and hope" into "contain, scope, find root cause, and permanently fix" — posture and detection reinforcing each other.

**Negative test:** Ending the response at containment. Killing the process and isolating the host stops this instance, but the exposed, vulnerable path remains for the next attacker — only tracing to the source and fixing it closes the loop.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Wiz Defend understood as the CDR pillar — runtime detection and response, the subject of Defend Fundamentals.
- [ ] Detections enriched with graph context so responders start from blast radius and likely entry, not a bare hostname.
- [ ] Incidents traced code-to-cloud-to-runtime on one graph, ending at a source fix that prevents recurrence.
- [ ] Posture and detection recognized as reinforcing — the hardened paths are the traveled paths, and incidents strengthen posture.
