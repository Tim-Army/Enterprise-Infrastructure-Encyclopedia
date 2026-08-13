# Chapter 02: Insight Platform Architecture

## Learning Objectives

- Describe the Insight platform's components: agents, collectors, scan engines, and the cloud console.
- Explain how data flows from your environment to the platform.
- Choose between agent-based and scan-based coverage for a given asset.
- Place components correctly for network reachability and scale.

## The components

The Insight platform is a **cloud console fed by lightweight components you deploy**. The pieces are shared across products, which is why understanding them once serves all four certifications.

| Component | Role |
|:---|:---|
| **Insight Platform (cloud)** | The console, data store, analytics, and reporting |
| **Insight Agent** | A lightweight agent on endpoints and servers; collects continuously and reports to the platform |
| **Scan Engine** | Performs network vulnerability scans against targets (InsightVM) |
| **Collector** | Receives and forwards log data from event sources (InsightIDR) |
| **Security Console** | The InsightVM management component that coordinates scan engines |
| **Orchestrator** | Executes InsightConnect automation inside your network |

The direction of travel matters: these components make **outbound** connections to the Insight platform. You do not open inbound ports to your security infrastructure — the same architectural pattern as SailPoint's virtual appliance in [Volume CXXXII](../../volume-132-sailpoint-certifications/README.md), and for the same reason.

## Agent versus scan

This is the central coverage decision in InsightVM, and it appears in exam scenarios constantly.

| | **Insight Agent** | **Scan Engine** |
|:---|:---|:---|
| Data | Continuous, from the host's own view | Point-in-time, from the network's view |
| Coverage | Follows the asset anywhere — laptops, remote workers, cloud instances | Only what the engine can reach on the network |
| Depth | Deep local visibility without credentials-on-the-wire | Depth depends on credentials |
| Cannot cover | Devices you cannot install software on | Assets that are off the network when scanning runs |

The right answer is usually **both**, and the reason is complementary blind spots:

- A **laptop that is rarely on the corporate network** is invisible to scheduled scanning and fully visible to an agent.
- A **printer, switch, or appliance** cannot run an agent and is only visible to scanning.

An estate covered by scanning alone systematically under-reports the roaming population — which, post-remote-work, is often the majority of endpoints.

## Placement and reachability

Scan engines must **reach their targets**, and a scan engine sitting the wrong side of a firewall reports assets as "down" rather than reporting an error you would notice. Distributed sites generally want a local engine, both for reachability and to avoid dragging scan traffic across a WAN.

Collectors follow the same logic for log sources: place them where the sources can send to them, and remember that a collector is a **funnel** — sizing it below the event rate means dropped or delayed data, which silently degrades detection.

## Hands-On Lab

Python models the architecture. **Cost:** none.

### Lab 2.1 — Agent and scan coverage, and the gap between them

**Objective:** Show what each method misses.

```bash
python3 - <<'EOF'
assets = [
  {"name":"laptop-hr-07",  "type":"laptop",  "agent":True,  "on_network_at_scan":False},
  {"name":"laptop-eng-12", "type":"laptop",  "agent":False, "on_network_at_scan":False},
  {"name":"srv-app-01",    "type":"server",  "agent":True,  "on_network_at_scan":True},
  {"name":"printer-3f",    "type":"printer", "agent":False, "on_network_at_scan":True},
  {"name":"switch-core-1", "type":"switch",  "agent":False, "on_network_at_scan":True},
  {"name":"vm-cloud-09",   "type":"cloud vm","agent":True,  "on_network_at_scan":False},
]
covered, blind = [], []
for a in assets:
    by_agent = a["agent"]
    by_scan  = a["on_network_at_scan"]
    how = [m for m, ok in (("agent", by_agent), ("scan", by_scan)) if ok]
    (covered if how else blind).append((a["name"], how))
    print(f"{a['name']:15} [{a['type']:8}] covered by: {how or 'NOTHING — BLIND SPOT'}")

print(f"\ncovered {len(covered)}/{len(assets)}, blind {len(blind)}")
for name, _ in blind:
    print(f"   BLIND: {name} — no agent installed and off-network when scanning ran")
print("\nAgents follow roaming assets; scanning reaches devices that cannot run software.")
print("Scanning ALONE systematically under-reports laptops and cloud instances —")
print("which is most of the estate once remote work is normal.")
EOF
```

**Expected result:** Five assets covered, `laptop-eng-12` a **blind spot** — no agent and off-network at scan time. The closing observation is the practically important one: a vulnerability report built from scanning alone looks complete while omitting the roaming population entirely, and nothing in the report indicates the omission.

**Negative test:** Reporting "98% of assets scanned" without stating the denominator — assets that were off the network are usually not in the denominator at all, so the percentage measures the wrong thing.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Scan engine placement and reachability

**Objective:** Diagnose why a site reports as down.

```bash
python3 - <<'EOF'
sites = [
  {"site":"HQ",        "engine_local":True,  "firewall_blocks":False, "assets":800},
  {"site":"Branch-EU", "engine_local":False, "firewall_blocks":True,  "assets":150},
  {"site":"DC-2",      "engine_local":True,  "firewall_blocks":False, "assets":400},
  {"site":"Cloud-AWS", "engine_local":False, "firewall_blocks":False, "assets":250},
]
for s in sites:
    if s["engine_local"]:
        verdict = "OK — local engine reaches targets directly"
    elif s["firewall_blocks"]:
        verdict = ("BROKEN — remote engine blocked by firewall. Assets report as DOWN, which reads "
                   "like 'nothing to fix' rather than 'we cannot see them'")
    else:
        verdict = "WORKS but scan traffic crosses the WAN — slow, and noisy for the link"
    print(f"{s['site']:11} {s['assets']:>4} assets  local_engine={str(s['engine_local']):5} -> {verdict}")
print("\nThe dangerous failure is the silent one: a blocked engine makes an unreachable site")
print("indistinguishable from a clean one. Reconcile scanned counts against your asset inventory.")
EOF
```

**Expected result:** Branch-EU is **broken in the worst way** — its assets report as down, which on a dashboard is visually identical to a site with nothing wrong. The remedy named in the closing lines is reconciliation: compare what the scanner found against an independent inventory, because a vulnerability tool cannot tell you about assets it never reached.

**Negative test:** Trusting a clean scan report for a remote site — "no vulnerabilities found" and "no assets reachable" produce the same reassuring green, and only one of them is good news.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Size a collector against event rate

**Objective:** Show what happens when ingestion is undersized.

```bash
python3 - <<'EOF'
def assess(name, eps_peak, collector_capacity_eps):
    headroom = (collector_capacity_eps - eps_peak) / collector_capacity_eps * 100
    if eps_peak > collector_capacity_eps:
        over = eps_peak - collector_capacity_eps
        verdict = (f"OVERSUBSCRIBED by {over} EPS — events queue then DROP. "
                   "Detection degrades silently: the alerts you never see look like quiet")
    elif headroom < 20:
        verdict = f"TIGHT — only {headroom:.0f}% headroom; an incident burst will overrun it"
    else:
        verdict = f"healthy — {headroom:.0f}% headroom for bursts"
    print(f"{name:14} peak {eps_peak:>6} EPS vs capacity {collector_capacity_eps:>6} -> {verdict}")

assess("collector-hq",  4500, 10000)
assess("collector-dc",  9200, 10000)
assess("collector-eu", 12500, 10000)
print("\nEvent bursts happen during INCIDENTS — exactly when you need the data most.")
print("Size collectors for peak-plus-burst, not average, and alert on ingestion lag.")
EOF
```

**Expected result:** One healthy collector, one with dangerously thin headroom, and one oversubscribed and dropping events. The timing argument in the closing lines is the one that matters: log volume spikes during an attack, so a collector sized to average throughput fails precisely when the data is most valuable — and the resulting gap presents as *silence*, not as an error.

**Negative test:** Sizing ingestion on a monthly average — a normal business-hours peak is several times the average, and an incident is several times that again.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Insight platform components identified, with outbound-only connectivity understood.
- [ ] Agent and scan coverage compared, and their complementary blind spots quantified.
- [ ] Scan engine placement diagnosed, including the silent unreachable-site failure.
- [ ] Collectors sized for peak-plus-burst, with ingestion lag identified as an alerting requirement.
