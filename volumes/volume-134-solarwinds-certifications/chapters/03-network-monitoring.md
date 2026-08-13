# Chapter 03: Network Monitoring

## Learning Objectives

- Calculate availability and interpret what an SLA percentage actually permits.
- Monitor interface utilization, errors, and discards — and know which matters when.
- Use topology and path awareness to find the failure rather than every symptom.
- Apply flow data to answer "who is consuming the bandwidth?"

## What network monitoring measures

This is the material behind the **Observability Self-Hosted Network Monitoring** exam and the historical NPM product. Four question types:

| Question | Measured by |
|:---|:---|
| Is it up? | ICMP/SNMP polling — **availability** |
| Is it fast enough? | Latency, packet loss, response time |
| Is the link full? | **Interface utilization** (bps against link speed) |
| Is the link healthy? | **Errors and discards** — distinct from utilization |

The distinction between the last two is a favorite of both exams and real incidents: a link at 30% utilization with rising CRC errors is failing, and a utilization-only dashboard shows it as healthy.

## Availability arithmetic

Availability is uptime divided by total time, and the percentages have consequences people rarely internalize until they write them down:

| Availability | Downtime per year | Downtime per month |
|:---|:---|:---|
| 99% ("two nines") | 3.65 days | 7.3 hours |
| 99.9% ("three nines") | 8.77 hours | 43.8 minutes |
| 99.99% ("four nines") | 52.6 minutes | 4.4 minutes |
| 99.999% ("five nines") | 5.26 minutes | 26 seconds |

Two consequences worth stating. First, **your polling interval bounds what you can measure**: five-minute polling cannot detect a 26-second outage, so a five-nines claim measured by five-minute polls is unprovable. Second, at four nines and above, the **time to detect and respond** consumes the entire budget — you cannot meet it with humans reading dashboards.

## Errors, discards, and utilization

| Counter | Means | Usual cause |
|:---|:---|:---|
| **Utilization** | Fraction of link capacity in use | Demand |
| **Errors (CRC/FCS)** | Corrupted frames | Physical layer: cable, optic, connector, duplex mismatch |
| **Discards** | Frames dropped despite arriving intact | Congestion, buffer exhaustion, policy |

Errors point at the **physical layer**; discards point at **congestion or policy**. They call for different responses, and treating both as "packet loss" sends you to the wrong place.

## Topology and root cause

When a distribution switch fails, everything behind it stops responding. A monitoring platform without topology awareness alerts on all of it — the switch plus fifty downstream devices — and buries the one alert that matters. **Dependency/parent-child awareness** suppresses the downstream noise and reports the actual failure. Chapter 07 builds this.

Path-aware monitoring (the NetPath idea) extends the same principle across networks you do not own: when a SaaS application is slow, hop-by-hop path data shows whether the problem is your LAN, your ISP, or the provider — which is the difference between fixing it and waiting for someone else to.

## Hands-On Lab

Python models network monitoring. **Cost:** none.

### Lab 3.1 — Availability against an SLA

**Objective:** Convert outage minutes into an availability figure and a verdict.

```bash
python3 - <<'EOF'
PERIOD_MIN = 30*24*60          # one 30-day month
outages = {                    # device -> outage minutes this month
  "core-router-1": 4,
  "dist-switch-7": 55,
  "wan-link-eu":   260,
}
SLA = {"core-router-1":99.99, "dist-switch-7":99.9, "wan-link-eu":99.0}

for dev, mins in outages.items():
    avail = (PERIOD_MIN - mins) / PERIOD_MIN * 100
    target = SLA[dev]
    budget = PERIOD_MIN * (1 - target/100)
    status = "MET" if avail >= target else "BREACHED"
    print(f"{dev:15} down {mins:>4} min  availability {avail:7.4f}%  target {target}%  "
          f"budget {budget:5.1f} min -> {status}")
print("\nPolling interval bounds measurement: 5-minute polls cannot see a 26-second outage,")
print("so a five-nines claim measured that way is unprovable.")
EOF
```

**Expected result:** The core router meets four nines with 4 minutes against a 4.3-minute budget — barely; the distribution switch breaches three nines (55 minutes against 43.2); the WAN link meets 99% with room to spare. Writing the **error budget** in minutes next to the percentage is what makes an SLA operationally meaningful: "99.99%" is abstract, "you have 4.3 minutes this month" is not.

**Negative test:** Reporting availability without stating the polling interval — the number's precision implies a measurement resolution you may not have.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Utilization versus errors

**Objective:** Distinguish a busy link from a failing one.

```bash
python3 - <<'EOF'
interfaces = [
  {"name":"Gi0/1","speed_mbps":1000,"in_mbps":920,"errors":0,   "discards":0},
  {"name":"Gi0/2","speed_mbps":1000,"in_mbps":300,"errors":4200,"discards":0},
  {"name":"Gi0/3","speed_mbps":1000,"in_mbps":990,"errors":0,   "discards":8500},
  {"name":"Gi0/4","speed_mbps":1000,"in_mbps":120,"errors":0,   "discards":0},
]
for i in interfaces:
    util = i["in_mbps"]/i["speed_mbps"]*100
    findings = []
    if util > 90:      findings.append(f"SATURATED ({util:.0f}%) — capacity problem")
    elif util > 70:    findings.append(f"busy ({util:.0f}%) — trend for capacity planning")
    if i["errors"] > 100:
        findings.append("ERRORS — PHYSICAL layer: cable/optic/connector/duplex. Utilization is only "
                        f"{util:.0f}%, so this is NOT congestion")
    if i["discards"] > 100:
        findings.append("DISCARDS — congestion/buffer exhaustion; pairs with the high utilization")
    print(f"{i['name']}: util={util:5.1f}%  errors={i['errors']:>5}  discards={i['discards']:>5}")
    for f in findings or ["healthy"]:
        print(f"      -> {f}")
EOF
```

**Expected result:** Gi0/1 is saturated but clean; **Gi0/2 is the interesting one** — only 30% utilized yet throwing 4,200 errors, a physical-layer fault a utilization dashboard would call healthy; Gi0/3 shows discards alongside saturation, the signature of congestion; Gi0/4 is idle. Monitoring errors and discards **separately from utilization** is what catches the failing optic before it becomes an outage.

**Negative test:** Alerting only on utilization thresholds — Gi0/2's degrading cable stays invisible until it fails completely, at which point the outage is unexplained.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Topology-aware root cause

**Objective:** Report the failure, not the fifty symptoms.

```bash
python3 - <<'EOF'
topology = {                       # child -> parent
  "core-1": None,
  "dist-a": "core-1", "dist-b": "core-1",
  "acc-1":"dist-a","acc-2":"dist-a","acc-3":"dist-a",
  "acc-4":"dist-b","acc-5":"dist-b",
  "srv-1":"acc-1","srv-2":"acc-1","srv-3":"acc-2",
}
unreachable = {"dist-a","acc-1","acc-2","acc-3","srv-1","srv-2","srv-3"}

def root_cause(node):
    p = topology.get(node)
    while p:
        if p in unreachable: return root_cause(p)
        break
    return node

roots = {root_cause(n) for n in unreachable}
print(f"unreachable devices: {len(unreachable)}")
print(f"ROOT CAUSE: {sorted(roots)}  <- alert on this")
print(f"suppressed as downstream: {sorted(unreachable - roots)}")
print(f"\nAlerts sent: {len(roots)} instead of {len(unreachable)} — a {len(unreachable)}x noise reduction,")
print("and the on-call engineer is told WHICH device to fix.")
EOF
```

**Expected result:** Seven unreachable devices collapse to **one root cause (`dist-a`)**, with the other six suppressed as downstream. The seven-fold noise reduction is the visible benefit; the real one is diagnostic — the engineer is handed the device to fix rather than a wall of alerts to triage under pressure. This dependency logic is what Chapter 07 generalizes into alert design.

**Negative test:** Flat alerting with no topology — a single distribution-switch failure pages on every device behind it, and the responder spends the first ten minutes working out which alert is the cause rather than fixing it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Availability calculated against SLA targets with error budgets in minutes.
- [ ] Polling interval understood as the bound on measurable availability.
- [ ] Utilization, errors, and discards distinguished and mapped to different causes.
- [ ] Topology-aware root cause used to report the failure rather than the symptoms.
