# Chapter 02: Monitoring Fundamentals and the Observability Platform

## Learning Objectives

- Describe the platform architecture: polling engines, database, web front end, and agents.
- Compare agentless collection (SNMP, WMI, API) with agent-based collection.
- Contrast Self-Hosted and SaaS deployment models.
- Scale collection with additional polling engines and plan for high availability.

## Platform architecture

The **Self-Hosted** platform (the Orion lineage) has a shape worth knowing before any exam:

| Component | Role |
|:---|:---|
| **Polling engine** | Collects data from monitored nodes on a schedule. The unit of collection capacity. |
| **Database** | Stores collected metrics, events, and configuration (SQL Server in the self-hosted product). |
| **Web front end** | The console — dashboards, alerts, reports. |
| **Additional polling engine (APE)** | An extra collector added to scale out or reach a remote network. |
| **Agent** | Optional software on the monitored host, for cases where agentless collection cannot reach or cannot see enough. |
| **High Availability** | A standby that takes over a failed primary or polling engine. |

The **database is the usual bottleneck and the usual single point of failure** — a fact that surprises people who assume the polling engines are the constrained resource. Metric ingestion is write-heavy and retention-hungry, so database sizing and storage performance dominate the scaling conversation.

## How data gets collected

| Method | Typical use | Notes |
|:---|:---|:---|
| **ICMP** | Up/down, latency, packet loss | Cheapest check; proves reachability only |
| **SNMP** | Network devices: interfaces, CPU, memory | v2c is unauthenticated in practice; **v3 adds authentication and encryption** |
| **WMI / PowerShell** | Windows servers | Credential-heavy; firewall-sensitive |
| **SSH / CLI** | Linux/network devices, config retrieval | Used by configuration management (Chapter 04) |
| **API / streaming** | Cloud services, modern platforms | The SaaS platform's center of gravity |
| **Agent** | Hosts across NAT/firewalls, deeper OS visibility | Survives network segmentation; more to deploy and maintain |
| **Flow (NetFlow/sFlow/IPFIX)** | Who is using the bandwidth | Traffic composition, not just utilization |
| **Syslog / traps** | Event-driven signals | Push, not poll — arrives when the device decides |

The distinction that matters operationally: **polling** asks on a schedule (so you see a sampled view), while **syslog and traps** are pushed asynchronously (so you see events but cannot infer health from silence). Both are needed; neither substitutes for the other.

**SNMPv3** deserves an explicit note. v1/v2c authenticate with a community string sent in clear text — effectively a shared password on the wire. v3 provides authentication and encryption, and is the correct choice on any network where monitoring traffic could be observed.

## Self-Hosted versus SaaS

| | **Self-Hosted** | **SaaS** |
|:---|:---|:---|
| You operate | Polling engines, database, web tier, upgrades | Nothing — SolarWinds runs the platform |
| Data lives | In your data center | In SolarWinds' cloud |
| Reaches | Anything on your network | Cloud/API sources directly; on-prem via collectors |
| Fits | Data-sovereignty needs, air-gapped and federal environments, large existing deployments | Cloud-native estates, teams without infrastructure to spare |

The certification catalog mirrors this split, with a **Fundamentals** exam on each side, so choose based on what you actually run.

## Hands-On Lab

Python models collection. **Cost:** none.

### Lab 2.1 — Model polling capacity and scale out

**Objective:** Size polling engines against the element count.

```bash
python3 - <<'EOF'
# Each polled element costs capacity; an engine has a finite budget per interval
ENGINE_CAPACITY = 10000     # elements one polling engine handles comfortably
nodes = [
  {"site":"HQ",       "elements":6500,  "reachable_from_primary":True},
  {"site":"DR",       "elements":3200,  "reachable_from_primary":True},
  {"site":"Branch-EU","elements":2800,  "reachable_from_primary":False},  # separate network
]
total = sum(n["elements"] for n in nodes)
primary_load = sum(n["elements"] for n in nodes if n["reachable_from_primary"])
print(f"total elements={total}, reachable from primary={primary_load}, engine capacity={ENGINE_CAPACITY}\n")

engines_needed = -(-primary_load // ENGINE_CAPACITY)      # ceiling division
print(f"primary side: {engines_needed} polling engine(s) for {primary_load} elements")
for n in nodes:
    if not n["reachable_from_primary"]:
        print(f"{n['site']}: needs its OWN additional polling engine ({n['elements']} elements) —")
        print(f"{'':11} not a capacity decision but a REACHABILITY one")
print(f"\nAlso size the DATABASE: {total} elements of metrics is the real scaling constraint.")
EOF
```

**Expected result:** The primary side needs one polling engine for 9,700 elements, and Branch-EU needs its own **regardless of capacity** because it sits on an unreachable network. That distinction is the point: additional polling engines are deployed for **two different reasons** — capacity and reachability — and conflating them leads to either an overloaded collector or a remote site nobody can poll. The closing line flags the database as the constraint people forget.

**Negative test:** Adding polling engines to fix slow dashboards — if the bottleneck is database I/O, more collectors write more data to the same overloaded database and make it worse.

**Cleanup:** None.

### Lab 2.2 — Choose a collection method per target

**Objective:** Match method to target, and prefer SNMPv3.

```bash
python3 - <<'EOF'
targets = [
  {"name":"core-switch",   "type":"network", "cross_firewall":False, "needs":"interfaces+CPU"},
  {"name":"win-app-01",    "type":"windows", "cross_firewall":False, "needs":"services+disk"},
  {"name":"linux-db-02",   "type":"linux",   "cross_firewall":True,  "needs":"processes+disk"},
  {"name":"aws-lambda",    "type":"cloud",   "cross_firewall":True,  "needs":"invocations+errors"},
]
for t in targets:
    if t["type"] == "network":
        method, note = "SNMPv3", "use v3 — v2c community strings cross the wire in clear text"
    elif t["type"] == "cloud":
        method, note = "API/cloud integration", "no polling of hosts; query the provider's API"
    elif t["cross_firewall"]:
        method, note = "agent", "agent initiates outbound — survives firewalls/NAT where WMI/SSH cannot"
    else:
        method, note = ("WMI" if t["type"] == "windows" else "SSH"), "agentless where the network path is open"
    print(f"{t['name']:14} [{t['type']:8}] -> {method:22} ({note})")
EOF
```

**Expected result:** The switch uses SNMPv3, the local Windows box WMI, the firewalled Linux host an **agent**, and the cloud function the provider API. The rule to internalize: an **agent is the answer to a network-path problem**, not automatically the better method — agentless is simpler to operate where the path is open, and agents earn their maintenance cost when they cross segmentation.

**Negative test:** Standardizing on SNMPv2c because "v3 is fiddly to configure" — you have put a plaintext credential on every device and made monitoring traffic readable by anyone on the path.

**Cleanup:** None.

### Lab 2.3 — Poll versus push, and the silence problem

**Objective:** Show why polling and event streams are complementary.

```bash
python3 - <<'EOF'
def interpret(signal_type, received_recently, device_state):
    if signal_type == "poll":
        return ("device is UP (poll answered)" if received_recently
                else "device is DOWN or unreachable — SILENCE IS THE SIGNAL")
    # push (syslog/trap)
    return ("event received — something happened" if received_recently
            else "no events — could mean healthy, or could mean the device is dead and silent")

for st in ("poll", "push"):
    for recent in (True, False):
        print(f"{st:5} received_recently={str(recent):5} -> {interpret(st, recent, None)}")
print("\nPolling turns silence into information (a missed poll is a down device).")
print("Push tells you WHAT happened but cannot distinguish 'healthy' from 'dead'.")
print("You need both: polling for health, events for cause.")
EOF
```

**Expected result:** For polling, silence means "down"; for push signals, silence is ambiguous — a healthy quiet device and a dead one look identical. That asymmetry is the reason monitoring platforms poll for availability even in event-rich environments: **you cannot build an availability guarantee out of messages that only arrive when things go wrong.**

**Negative test:** Relying on syslog alone for availability — a device that loses power stops sending logs, which is indistinguishable from a device having a quiet afternoon.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Platform components described, with the database identified as the usual bottleneck.
- [ ] Collection methods matched to targets; SNMPv3 preferred over v2c.
- [ ] Polling engines scaled for capacity *and* reachability as separate reasons.
- [ ] Poll-versus-push asymmetry understood: silence is only meaningful when you poll.
