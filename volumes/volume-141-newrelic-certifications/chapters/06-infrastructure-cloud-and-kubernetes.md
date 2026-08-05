# Chapter 06: Infrastructure, Cloud, and Kubernetes

## Learning Objectives

- Deploy and tune the infrastructure agent, and know what tuning trades away.
- Monitor VM, container, Kubernetes, and serverless workloads appropriately for each.
- Use on-host and cloud integrations without double-collecting.
- Correlate network and application signals to cut mean time to resolve.

*Exam relevance: REP Section 3 in full — "VM and containerized (Docker and K8s) workloads, serverless workloads, on-host integrations and common cloud integrations, advanced tuning of infrastructure agent, with network monitoring correlate and analyze application to reduce MTTR" — plus PEP Section 4 (Infrastructure and Cloud Performance: "cloud service integrations, container metrics, and database infrastructure").*

## The infrastructure agent

The infrastructure agent reports host metrics, process telemetry, and events, and hosts the **on-host integrations** — modular collectors for databases, queues, and web servers running beside it.

REP names **"advanced tuning of infrastructure agent"** explicitly, and tuning here means one thing: choosing what not to collect, and how often. Every knob trades visibility for cost:

| Knob | Turned down | You save | You lose |
|:---|:---|:---|:---|
| Sample rates | Less frequent metric samples | Ingest volume | Resolution during fast incidents |
| Process telemetry | Fewer/no per-process samples | The single biggest volume item on busy hosts | "What was eating CPU at 10:04?" |
| Event filtering | Drop matching events at source | Noise and volume | Whatever matched — permanently |

The discipline is the one this shelf keeps arriving at: **tune deliberately, record what you turned off, and revisit after the next incident.** Data dropped at the agent is not recoverable at query time — this is the collection-side mirror of Grail's schema-on-read bargain.

## Four workload shapes

| Workload | What matters | What changes |
|:---|:---|:---|
| **VM** | Host metrics, processes | The stable baseline case |
| **Containers (Docker)** | Container-level limits and restarts | The *host* being fine no longer implies the *workload* is |
| **Kubernetes** | Pods, deployments, nodes, restarts, pending pods, limits vs requests | Entities churn constantly; identity must follow the deployment, not the pod |
| **Serverless** | Invocations, duration, cold starts, errors | There is no host — the agent model inverts to platform integrations |

The Kubernetes row deserves the emphasis the exam gives it: a pod is an ephemeral entity, so alerting or dashboarding on pod identity produces panels full of dead names within a day. Aggregate at the deployment/workload level and let pods churn beneath it.

## Cloud integrations, and double-collection

Cloud integrations poll provider APIs (CloudWatch and equivalents) for managed-service telemetry. The design question is overlap: an RDS database can be monitored by the cloud integration (provider metrics), an on-host integration is impossible (no host access), but the *application's* view of that database comes from APM (Chapter 04). Those views answer different questions — provider-side health versus application-experienced latency — and you generally want both. What you do not want is the same signal ingested twice through two paths, paying twice to disagree with itself.

## Network correlation and MTTR

REP's phrasing — "with network monitoring correlate and analyze application to reduce MTTR" — names a specific failure of siloed tooling: application dashboards and network dashboards each look "sort of degraded" and neither names the other. The lab models the payoff: when application errors and a network path problem share a timeline and a topology, the diagnosis that used to take a bridge call falls out of a correlation.

## Hands-On Lab

Python models infrastructure monitoring. **Cost:** none.

### Lab 6.1 — Agent tuning is a trade, not a free lunch

**Objective:** Tune ingest down and see exactly what disappears.

```bash
python3 - <<'EOF'
HOSTS = 800
BYTES = {
  # source:            (bytes/host/day at default, at tuned)
  "host metrics 15s -> 60s":        (48_000_000, 12_000_000),
  "process samples 20s -> off":     (95_000_000,          0),
  "storage samples 20s -> 120s":    (22_000_000,  3_700_000),
  "network samples 10s -> 60s":     (31_000_000,  5_200_000),
}
print(f"{'source':34}{'default GB/day':>15}{'tuned GB/day':>14}")
tot_d = tot_t = 0
for src, (d, t) in BYTES.items():
    gd, gt = d*HOSTS/1e9, t*HOSTS/1e9
    tot_d += gd; tot_t += gt
    print(f"{src:34}{gd:>15.1f}{gt:>14.1f}")
print(f"{'TOTAL':34}{tot_d:>15.1f}{tot_t:>14.1f}   ({(1-tot_t/tot_d)*100:.0f}% reduction)\n")

print("Now the incident: a runaway process ate a host's CPU for 4 minutes at 10:04.")
print("  default config : 12 process samples of the spike — named process, owned, fixed")
print("  tuned config   : process telemetry is OFF. Host CPU shows a plateau; WHICH")
print("                   process is unknowable retroactively. The data was never kept.")
print("\nThis is not an argument against tuning — 89% is real money at 800 hosts.")
print("It is an argument for tuning with a ledger:")
print("  1. record every knob you turned and why")
print("  2. keep process telemetry ON for tier-1 hosts, off for the fleet")
print("  3. after each incident, ask: did a tuning choice cost us the diagnosis?")
EOF
```

**Expected result:** An 89% ingest reduction, followed by an incident the tuned config can no longer diagnose because process samples were never collected. The tiering suggestion is the practical resolution — the fleet gets the cheap config, the hosts whose incidents matter keep the expensive one, and the ledger makes the trade auditable.

**Negative test:** Tuning everything to minimum after a billing surprise, with no record. Three weeks later the undiagnosable incident arrives, and nobody remembers that process telemetry was the price.

**Cleanup:** None.

### Lab 6.2 — Kubernetes: aggregate at the workload, not the pod

**Objective:** Show why pod-identity monitoring rots in hours.

```bash
python3 - <<'EOF'
import random
random.seed(6)
# A deployment over one day: pods churn via rollouts and rescheduling
pods, events = [], []
counter = 0
def new_pod():
    global counter
    counter += 1
    return f"checkout-7d9f{counter:04x}"
live = [new_pod() for _ in range(6)]
for hour in range(24):
    if hour in (3, 11, 19):                 # rollouts
        for i in range(len(live)):
            events.append((hour, "replaced", live[i]))
            live[i] = new_pod()
    if random.random() < 0.3:               # a rescheduling
        i = random.randrange(len(live))
        events.append((hour, "rescheduled", live[i]))
        live[i] = new_pod()

all_pods = {p for _, _, p in events} | set(live)
print(f"deployment 'checkout': 6 replicas, 24 hours")
print(f"distinct pod names over the day : {len(all_pods)}")
print(f"pods alive right now            : {len(live)}\n")

print("A dashboard FACETed by pod name after one day:")
print(f"   {len(all_pods)} series, {len(all_pods)-len(live)} of them DEAD names showing flat lines")
print("An alert on a specific pod name from this morning:")
print(f"   its target was replaced at the 11:00 rollout — the alert now watches nothing\n")
print("Aggregated at the DEPLOYMENT (workload) level instead:")
print("   1 series: checkout replica health, restarts/hr, pending pods")
print("   rollouts appear as EVENTS on the timeline, not as series churn")
print("\nThe entity that persists is the deployment; pods are its disposable")
print("instances. Point dashboards, alerts, and SLOs at what persists. (Same")
print("principle as user-action naming in Vols CXXXIX/CXL — identifiers churn,")
print("categories persist; put identity in attributes, not in the aggregation key.)")
EOF
```

**Expected result:** Roughly 30 distinct pod names in a day for a 6-replica deployment, leaving a pod-faceted dashboard dominated by dead series and a pod-named alert watching nothing after the first rollout. The closing parallel is deliberate — this is the third appearance of "aggregate on what persists" on this shelf, now wearing Kubernetes clothes.

**Negative test:** Alerting on pod restarts by pod name to "catch the flapping one." The flapping pod is replaced mid-flap; the alert history fragments across names and the pattern becomes invisible.

**Cleanup:** None.

### Lab 6.3 — Correlate network and application to cut MTTR

**Objective:** Model the REP correlation scenario end to end.

```bash
python3 - <<'EOF'
TIMELINE = [
  # minute, source,        signal
  (0,  "app (APM)",       "checkout error rate 0.4% (normal)"),
  (4,  "network",         "packet loss on path web-tier -> payments-vlan rises 0% -> 2%"),
  (5,  "app (APM)",       "checkout timeouts to payment-svc begin"),
  (7,  "network",         "packet loss 6%, retransmits climbing"),
  (8,  "app (APM)",       "checkout error rate 3.1%, alert fires"),
  (11, "network",         "loss localized: switch uplink eth1/48, CRC errors"),
]
print("SILOED VIEW — two teams, two dashboards:")
print("  app team sees   : timeouts to payment-svc -> suspects payment-svc, starts a rollback")
print("  network team sees: some loss on a VLAN     -> low priority, no app context")
print("  the connection is made on a bridge call at ~minute 45. MTTR ~70 min.\n")

print("CORRELATED VIEW — one timeline, entities linked by topology:")
for m, src, sig in TIMELINE:
    print(f"   t+{m:>2}m  {src:12} {sig}")
print("\n   the network degradation PRECEDES the app symptom by ~1 minute and sits on")
print("   the exact path the failing calls traverse. The rollback never starts;")
print("   the uplink is drained at ~minute 15. MTTR ~20 min.\n")
print("Two conditions made the correlation possible, and both are configuration:")
print("   1. network telemetry INGESTED beside app telemetry (not in a separate tool)")
print("   2. topology linking the app's calls to the path they ride")
print("\nNote also what was AVOIDED: a rollback of a healthy service — action taken")
print("at machine speed on the wrong target, the same failure mode as Vol CXL's")
print("automation chapter, caused here by a missing data source instead of a")
print("missing topology edge.")
EOF
```

**Expected result:** The siloed reading produces a wrong rollback and ~70-minute MTTR; the correlated timeline shows network loss preceding app symptoms on the exact path, resolving in ~20. The two enabling conditions are the exam-relevant content — correlation is not a feature you click but a consequence of ingesting both signals and linking them topologically.

**Negative test:** Keeping network monitoring in a separate tool "because the network team prefers it." Both tools are individually fine, and every cross-domain incident pays the bridge-call tax.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Infrastructure agent tuned with a ledger, tiered by host criticality.
- [ ] Kubernetes monitored at the deployment level, with pods treated as disposable.
- [ ] Cloud integrations combined with APM views without double-collection.
- [ ] Network and application telemetry correlated on one timeline to cut MTTR.
