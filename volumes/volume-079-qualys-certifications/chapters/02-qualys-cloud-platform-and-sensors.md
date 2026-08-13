# Chapter 02: Qualys Cloud Platform and Sensors

## Learning Objectives

- Describe the Qualys Cloud Platform architecture.
- Deploy the right sensors for full coverage.
- Use Cloud Agents for continuous assessment.
- Search the platform with Qualys Query Language (QQL).
- Complete a walkthrough for each platform/sensor topic.

## Theory and Architecture

The **Qualys Cloud Platform** is a single SaaS backend into which all Qualys applications and data
flow — VMDR, compliance, cloud, EDR, and more share one asset inventory and one query language. Data
is collected by **sensors**: **Cloud Agents** (a lightweight agent installed on hosts that
continuously reports inventory, vulnerabilities, and configuration — no scan window, works off the
corporate network, ideal for laptops and cloud instances); **scanner appliances** (virtual or
physical network scanners for reachable targets, including credentialed scans); **passive network
sensors** (that discover unmanaged assets by watching traffic); **cloud connectors** (that sync
cloud assets and configuration from AWS/Azure/GCP); and the **API**. Across all of it,
**QQL (Qualys Query Language)** is the unified search — one syntax to find assets, vulnerabilities,
or compliance results anywhere in the platform. Understanding the platform and choosing the right
mix of **agents and scanners** for **complete coverage** is the foundation for every Qualys
application. This chapter teaches each with a hands-on defensive walkthrough (sensor selection, agent
reasoning, and QQL).

## Design Considerations

Combine **Cloud Agents** (continuous, off-network) with **scanners** (network-reachable, credentialed)
and **passive sensors** (find unmanaged assets) for **complete coverage**. Use **cloud connectors**
for cloud posture. Learn **QQL** — it's how you find and report on anything. Watch for **coverage
gaps** and duplicate assets.

## Implementation and Automation

The labs select sensors, reason about agents, and write QQL queries.

## Validation and Troubleshooting

Confirm the platform model:

```text
Qualys Cloud Platform (SaaS): one inventory, one query language across all apps. Sensors: Cloud Agents (continuous host), scanner appliances (network/credentialed), passive sensors (discover unmanaged), cloud connectors (cloud posture), API.
QQL = unified search across assets/vulns/compliance. Goal: complete coverage.
```

Common pitfalls: **scan-only** coverage (misses roaming/cloud assets — use agents); and not learning
**QQL** (you can't find or report efficiently).

## Security and Best Practices

Build **complete coverage** with agents + scanners + passive sensors + connectors, learn **QQL**, and
watch for gaps and duplicates. Scan only **authorized** targets. All work is defensive.

## Hands-On Lab

Platform/sensor walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 2.1 — Select sensors for coverage

**Objective:** Match sensor to asset.

```python
python3 - <<'PY'
assets={"data-center server":"scanner appliance (credentialed)","roaming laptop":"Cloud Agent",
        "cloud VM":"Cloud Agent or cloud connector","unmanaged device on the wire":"passive sensor",
        "AWS account posture":"cloud connector"}
for asset,sensor in assets.items(): print(f"{asset:26}: {sensor}")
PY
```

**Expected result:** each asset matched to the right **Qualys sensor** — full-coverage strategy.

**Negative test:** cover laptops with network scans only; they're often off-network — use **Cloud
Agents**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Reason about the Cloud Agent advantage

**Objective:** Continuous vs point-in-time.

```python
python3 - <<'PY'
scan={"data":"point-in-time (at scan window)","network":"must be reachable + credentialed"}
agent={"data":"continuous (reports on change)","network":"works anywhere (checks in to platform)"}
print("scanner:", scan)
print("agent  :", agent)
print("Cloud Agent: always-on, off-network coverage -> fresher data, no missed windows")
PY
```

**Expected result:** the **continuous, anywhere** agent model vs point-in-time scanning — the agent
advantage.

**Negative test:** wait for the next scan window to learn about a new critical vuln; an **agent**
reports it continuously — prefer agents for endpoints.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Search with QQL

**Objective:** Find assets and vulns.

```python
python3 - <<'PY'
queries={"critical vulns on servers":'vulnerabilities.vulnerability.severity:5 and asset.tags.name:"Servers"',
         "internet-facing assets":'asset.tags.name:"Internet-Facing"',
         "missing a patch":'vulnerabilities.vulnerability.qid:91234'}
for intent,qql in queries.items(): print(f"{intent:28}: {qql}")
print("QQL: one syntax to search assets, vulnerabilities, and compliance across the platform")
PY
```

**Expected result:** **QQL** queries expressing common searches — the platform's unified search.

**Negative test:** export everything and filter in a spreadsheet; **QQL** filters at the source —
query the platform.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Tag assets for scope

**Objective:** Organize with dynamic tags.

```python
python3 - <<'PY'
def tag(asset):
    tags=[]
    if asset["os"].startswith("Windows Server"): tags.append("Servers")
    if asset["public_ip"]: tags.append("Internet-Facing")
    if "prod" in asset["name"]: tags.append("Production")
    return tags
print(tag({"name":"prod-web01","os":"Windows Server 2025","public_ip":True}))
print("Qualys: dynamic tags scope scans, reports, and QQL by business context")
PY
```

**Expected result:** an asset **dynamically tagged** (Servers/Internet-Facing/Production) — scoping by
context.

**Negative test:** manage scope by static IP lists; they drift — use **dynamic tags**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Qualys Cloud Platform unifies all applications on one inventory and query language, fed by Cloud
Agents, scanners, passive sensors, and cloud connectors, searched with QQL and scoped with dynamic
tags — the foundation for complete coverage.

- [ ] I can select sensors for coverage.
- [ ] I can explain the Cloud Agent advantage.
- [ ] I can search with QQL.
- [ ] I can tag assets for scope.
- [ ] I completed Labs 2.1–2.4 including each negative test.
