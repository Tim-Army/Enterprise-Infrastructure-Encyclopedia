# Chapter 02: OneAgent, ActiveGate, and Deployment

## Learning Objectives

- Explain what OneAgent instruments automatically and what it does not.
- Place ActiveGate correctly: routing, remote monitoring, and secure connectivity.
- Choose a deployment model and size the ActiveGate tier.
- Recognize the deployment mistakes that produce blind spots rather than errors.

*Exam relevance: **Components And Architecture** and **Installation And Configuration**, two of the six Associate domains, and a large share of the Advanced Observability Specialist skill list (OneAgent, ActiveGate, permissions and policies).*

## OneAgent

The platform's central claim is that you install **one agent per host** and it discovers the rest. OneAgent detects processes as they start, injects instrumentation into supported technologies, and reports host, process, service, and application telemetry along with the dependencies between them.

That is a genuinely different operating model from the collector-and-exporter approach in [Volume CXXXIX](../../volume-139-grafana-observability/README.md) and [Volume LV](../../volume-055-prometheus/README.md), and it earns its keep in environments where nobody can enumerate what is running. It also creates a specific failure mode: **when auto-instrumentation does not cover something, the gap is silent.** Nothing errors. A service simply does not appear, and an absent service looks identical to a healthy one nobody is calling.

| What OneAgent handles well | Where you must act deliberately |
|:---|:---|
| Mainstream runtimes (Java, .NET, Node.js, PHP, Go, Python) | Unsupported or exotic runtimes |
| Host, process, container metrics | Custom business metrics |
| Service-to-service dependencies | Third-party SaaS you do not run |
| Automatic service detection | Naming that matches how *you* think about services |
| Log collection from detected processes | Logs written somewhere unusual |

The discipline that follows: **after deploying, verify what was detected against what you believe you run.** The lab below models exactly this reconciliation, because the failure is a difference between two lists, not an error message.

## ActiveGate

ActiveGate is the platform's gateway component. It sits between OneAgents and the Dynatrace environment, and it carries roles that OneAgent cannot:

| Role | Purpose |
|:---|:---|
| **Routing** | Concentrates OneAgent traffic, so hosts need no direct outbound path |
| **Remote monitoring** | Monitors things with no OneAgent — network devices, cloud APIs, databases via extensions |
| **Synthetic execution** | Runs private synthetic monitors from inside your network |
| **Secure connectivity** | A controlled egress point in segmented or air-gapped environments |

The two variants are worth keeping straight: an **Environment ActiveGate** serves a specific environment and is the usual choice, while a **Cluster ActiveGate** serves a Dynatrace Managed cluster. In segmented networks the ActiveGate is often the *only* component permitted to talk outbound, which makes its placement a security-architecture decision rather than a monitoring one.

## Deployment models

| Model | What you run | What Dynatrace runs |
|:---|:---|:---|
| **SaaS** | OneAgents, ActiveGates | The environment, Grail, everything else |
| **Managed** | The whole cluster, on your hardware | Nothing — you operate it |

The Managed variant is why **Dynatrace Associate for Managed** exists as a separate credential with the same six domains: the concepts are shared, the operational reality is not.

## Hands-On Lab

Python models deployment planning. **Cost:** none.

### Lab 2.1 — Reconcile detected services against reality

**Objective:** Find the silent blind spot.

```bash
python3 - <<'EOF'
# What you believe you run
inventory = {
  "checkout-api":     {"runtime":"Java",    "hosts":4},
  "payments-api":     {"runtime":".NET",    "hosts":3},
  "search":           {"runtime":"Go",      "hosts":2},
  "legacy-billing":   {"runtime":"COBOL",   "hosts":1},
  "image-processing":    {"runtime":"Rust",    "hosts":2},
  "recommendations":  {"runtime":"Python",  "hosts":3},
  "vendor-gateway":   {"runtime":"SaaS",    "hosts":0},
}
# What OneAgent auto-instruments
AUTO = {"Java", ".NET", "Go", "Python", "Node.js", "PHP"}

detected, missing = [], []
for name, meta in inventory.items():
    if meta["hosts"] == 0:
        missing.append((name, meta, "no host to install on (external SaaS)"))
    elif meta["runtime"] in AUTO:
        detected.append((name, meta))
    else:
        missing.append((name, meta, f"{meta['runtime']} not auto-instrumented"))

print(f"{'service':20}{'runtime':10}{'hosts':>6}   status")
for n, m in detected:
    print(f"{n:20}{m['runtime']:10}{m['hosts']:>6}   detected automatically")
for n, m, why in missing:
    print(f"{n:20}{m['runtime']:10}{m['hosts']:>6}   *** NOT DETECTED — {why}")

cov = len(detected) / len(inventory) * 100
print(f"\ncoverage: {len(detected)}/{len(inventory)} services ({cov:.0f}%)")
print("\nThe critical property: the three missing services produce NO ERROR.")
print("They are simply absent. An absent service and a healthy idle service look")
print("identical on a dashboard — which is why you reconcile against an inventory")
print("instead of trusting the service list to be complete.")
print("\nFixes, per case:")
print("  unsupported runtime -> OpenTelemetry ingest, or a Dynatrace extension")
print("  external SaaS       -> synthetic monitors from an ActiveGate, or API polling")
EOF
```

**Expected result:** 4 of 7 services detected — 57% coverage — with three silent gaps. The point the lab exists to make is in the last block: **auto-instrumentation failures do not raise errors.** Every other monitoring problem announces itself; this one hides, and the only detection method is comparing the discovered list against a list you maintain by hand.

**Negative test:** Treating the auto-detected service list as the inventory. It is a subset by construction, and the gap is exactly where your unusual, oldest, and riskiest systems live.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Size the ActiveGate tier

**Objective:** Plan gateways for routing, synthetics, and segmentation.

```bash
python3 - <<'EOF'
ENVIRONMENTS = [
  # name, hosts, network zone, needs private synthetics, cloud APIs to poll
  ("prod-dc-east",   420, "restricted", True,  3),
  ("prod-dc-west",   380, "restricted", True,  3),
  ("prod-cloud",     640, "egress-ok",  False, 5),
  ("staging",        120, "egress-ok",  False, 1),
  ("pci-zone",        45, "isolated",   True,  0),
]
HOSTS_PER_AG   = 250      # planning ratio for routing capacity
AG_REDUNDANCY  = 2        # never one gateway in front of production

print(f"{'environment':16}{'hosts':>7}{'zone':>12}{'routing AG':>12}{'total AG':>10}   drivers")
total = 0
for name, hosts, zone, synth, apis in ENVIRONMENTS:
    routing = max(1, -(-hosts // HOSTS_PER_AG))
    ags = routing
    drivers = [f"routing({routing})"]
    if zone in ("restricted", "isolated"):
        ags = max(ags, AG_REDUNDANCY); drivers.append("segmented egress")
    if synth:
        drivers.append("private synthetics")
    if apis:
        drivers.append(f"{apis} cloud API sources")
    if "prod" in name or zone == "isolated":
        ags = max(ags, AG_REDUNDANCY); drivers.append("HA pair")
    total += ags
    print(f"{name:16}{hosts:>7}{zone:>12}{routing:>12}{ags:>10}   {', '.join(drivers)}")

print(f"\ntotal ActiveGates: {total}")
print("\nNote what drives the count: routing capacity sets a FLOOR, but network")
print("segmentation and HA set the actual number. pci-zone has 45 hosts and still")
print("needs a redundant pair — because it is the only permitted egress path, and a")
print("single gateway there is a single point of failure for ALL monitoring in the zone.")
print("\nIn isolated zones the ActiveGate is a security-architecture decision:")
print("it is the one component allowed to talk outbound, so its placement, hardening,")
print("and change control belong to the security review, not just the monitoring plan.")
EOF
```

**Expected result:** 10 ActiveGates across five environments, where the PCI zone needs two despite having the fewest hosts. That inversion is the lesson — capacity is the floor, not the driver, and treating gateway count as a pure hosts-divided-by-ratio calculation under-provisions exactly the environments where an outage is least acceptable.

**Negative test:** Sizing gateways on host count alone and putting one ActiveGate in the isolated zone. When it restarts, every host in that zone goes dark at once.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — SaaS versus Managed

**Objective:** Choose a deployment model on the criteria that actually decide it.

```bash
python3 - <<'EOF'
CRITERIA = [
  # criterion,                          weight, saas, managed
  ("Data residency / sovereignty",         5,     2,     5),
  ("Air-gapped or restricted network",     4,     1,     5),
  ("Operational staff available",          5,     5,     2),
  ("Upgrade and patch burden",             4,     5,     1),
  ("Time to first value",                  3,     5,     2),
  ("Grail and newest platform features",   5,     5,     2),
  ("Predictable infrastructure cost",      2,     3,     4),
]
s = sum(w*a for _,w,a,_ in CRITERIA); m = sum(w*b for _,w,_,b in CRITERIA)
print(f"{'criterion':38}{'wt':>4}{'SaaS':>7}{'Managed':>9}")
for c,w,a,b in CRITERIA:
    mark = "  <--" if abs(a-b) >= 3 else ""
    print(f"{c:38}{w:>4}{a:>7}{b:>9}{mark}")
print(f"\n{'WEIGHTED TOTAL':38}{'':>4}{s:>7}{m:>9}")
print(f"\nSaaS wins on this profile ({s} vs {m}), and the arrows show why the choice is")
print("rarely close: the criteria that separate them are near-absolute rather than")
print("marginal. Sovereignty and air-gap requirements do not trade off against")
print("convenience — if you have them, they decide the question by themselves.")
print("\nIf you run Managed, note the SEPARATE credential: 'Dynatrace Associate for")
print("Managed' covers the same six domains against a platform you operate yourself.")
EOF
```

**Expected result:** SaaS scores 105 against Managed's 83 on this profile, but the arrows mark six criteria where the gap is three points or more. The framing matters more than the total: regulatory and network constraints are gates, not weights, and no amount of operational convenience outvotes a data-residency requirement.

**Negative test:** Running a weighted score and picking the winner when one criterion is a hard legal constraint — the model is decision support, not the decision.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] OneAgent's auto-instrumentation scope understood, including its silent gaps.
- [ ] Detected services reconciled against a maintained inventory.
- [ ] ActiveGate roles distinguished, and gateway count driven by segmentation and HA.
- [ ] SaaS and Managed compared, with hard constraints treated as gates.
