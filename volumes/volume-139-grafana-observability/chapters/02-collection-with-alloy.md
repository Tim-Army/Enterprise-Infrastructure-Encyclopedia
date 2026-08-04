# Chapter 02: Collection with Alloy

## Learning Objectives

- Explain what a telemetry collector does and where Grafana Alloy sits in the pipeline.
- Deploy collection to Kubernetes using the Kubernetes Monitoring Helm chart.
- Route each signal to the right backend.
- Validate that telemetry actually arrived, rather than assuming a running agent means data is flowing.

## Collection is not instrumentation

The GROT Academy curriculum is explicit about its scope here, and the distinction is worth adopting: this material covers **practical telemetry collection, assuming applications are already instrumented**. Two different jobs:

| Job | Who does it | Covered here |
|:---|:---|:---|
| **Instrumentation** — making an application emit telemetry | Developers, or automatically (OpenTelemetry SDKs, eBPF) | No — see [Volume LIV](../../volume-054-opentelemetry/README.md) |
| **Collection** — gathering that telemetry and delivering it to a backend | Platform and observability engineers | **Yes** |

## Grafana Alloy

**Alloy** is Grafana's telemetry collector: it scrapes, receives, processes, and forwards metrics, logs, traces, and profiles. It is OpenTelemetry-Collector-compatible while also speaking Prometheus scraping and Loki push natively, which is why it can replace several single-purpose agents.

A pipeline has the same four stages regardless of signal:

| Stage | What happens |
|:---|:---|
| **Discover** | Find the targets — Kubernetes pods, services, nodes |
| **Collect** | Scrape metrics, tail logs, receive traces |
| **Process** | Relabel, filter, drop, enrich, batch |
| **Forward** | Write to the backend with authentication |

The **process** stage is where most of the operational value sits: it is where you drop the labels that would otherwise explode your cardinality (Chapter 04) and where you filter the noise you would otherwise pay to store.

## Deploying to Kubernetes

Grafana publishes a **Kubernetes Monitoring Helm chart** that deploys Alloy preconfigured to collect **metrics, logs, and traces in one deployment**. The value of a preconfigured chart over assembling collection yourself is exactly what you would expect: it simplifies configuration, encodes sensible defaults, and avoids the common misconfigurations that otherwise take a day to find.

Typical topology on a cluster:

| Deployment shape | Collects |
|:---|:---|
| **DaemonSet** (one per node) | Node metrics, pod logs from the node's filesystem |
| **Deployment / StatefulSet** | Cluster-wide scraping, trace reception, remote-write forwarding |

## Routing signals to backends

Each signal has a destination built for its shape, and matching them is the first thing to get right:

| Data | Backend | Why |
|:---|:---|:---|
| Pod CPU and memory over time | **Metrics** (Mimir / Grafana Cloud Metrics) | Numeric time series, aggregated and queried with PromQL |
| Container error messages and stack traces | **Logs** (Loki / Grafana Cloud Logs) | Timestamped text, queried with LogQL |
| A request flowing through frontend → API → database with timings | **Traces** (Tempo / Grafana Cloud Traces) | Causally linked spans across services |
| CPU/memory attribution inside a process | **Profiles** (Pyroscope) | Sampled stack traces |

Putting a signal in the wrong store is not merely untidy: logs in a metrics store explode cardinality, and metrics scraped as log lines cannot be aggregated.

## Validate, do not assume

The curriculum emphasizes **validating and troubleshooting data ingestion**, and it deserves the emphasis. A deployed collector that reports healthy is not evidence that data is arriving — credentials can be wrong, a remote-write endpoint can reject silently, relabeling can drop everything, and a network policy can block egress. The only proof is querying the backend and finding your data.

## Hands-On Lab

Python models the collection pipeline. **Cost:** none.

### Lab 2.1 — Model the pipeline and the process stage

**Objective:** Show where relabeling and filtering earn their place.

```bash
python3 - <<'EOF'
raw_targets = [
  {"pod":"api-7f9c","namespace":"prod","container":"api","port":8080,"scrape":True,
   "labels":{"pod":"api-7f9c","instance":"10.1.2.3:8080","namespace":"prod","app":"api","commit_sha":"a3f8c1e"}},
  {"pod":"api-2b1d","namespace":"prod","container":"api","port":8080,"scrape":True,
   "labels":{"pod":"api-2b1d","instance":"10.1.2.9:8080","namespace":"prod","app":"api","commit_sha":"a3f8c1e"}},
  {"pod":"debug-x","namespace":"sandbox","container":"debug","port":9090,"scrape":False,
   "labels":{"pod":"debug-x","namespace":"sandbox","app":"debug"}},
]
DROP_LABELS = {"commit_sha", "pod", "instance"}      # high-cardinality; keep app/namespace
def process(t):
    if not t["scrape"]:
        return None, "dropped at DISCOVER — not marked for scraping"
    kept = {k: v for k, v in t["labels"].items() if k not in DROP_LABELS}
    dropped = sorted(set(t["labels"]) - set(kept))
    return kept, f"kept {sorted(kept)}, dropped {dropped}"

for t in raw_targets:
    kept, why = process(t)
    print(f"{t['pod']:9} ns={t['namespace']:8} -> {'FORWARD' if kept else 'DROP   '}  {why}")

print("\nWhy drop pod/instance/commit_sha? Every distinct value creates a NEW time series.")
print("A 200-pod deployment that redeploys 20x a day with commit_sha as a label produces")
print("thousands of short-lived series — the classic cardinality explosion (see ch04).")
print("The PROCESS stage is where you prevent that, before it reaches the backend and the bill.")
EOF
```

**Expected result:** Two production targets forward with trimmed labels; the sandbox debug pod is dropped at discovery. The reasoning in the closing lines is the point of the process stage — high-cardinality labels like `commit_sha` and `pod` multiply time series, and the cheapest place to remove them is before they are ever written.

**Negative test:** Forwarding every discovered label because "more context is better" — you get context and a cardinality problem that degrades query performance and inflates cost, and removing labels later does not retract the series already created.

**Cleanup:** None.

### Lab 2.2 — Route each signal to the right backend

**Objective:** Match data shape to store.

```bash
python3 - <<'EOF'
data = [
  {"desc":"Pod CPU usage and memory over time",                      "shape":"numeric time series"},
  {"desc":"Error messages and stack traces from containers",         "shape":"timestamped text"},
  {"desc":"A request through frontend -> API -> database with timings","shape":"causally linked spans"},
  {"desc":"Which functions consume CPU inside a process",            "shape":"sampled stack traces"},
]
ROUTE = {
  "numeric time series":   ("METRICS  (Mimir / Cloud Metrics)", "aggregate and query with PromQL"),
  "timestamped text":      ("LOGS     (Loki / Cloud Logs)",     "filter and query with LogQL"),
  "causally linked spans": ("TRACES   (Tempo / Cloud Traces)",  "follow one request across services"),
  "sampled stack traces":  ("PROFILES (Pyroscope)",             "attribute resource use within a process"),
}
for d in data:
    dest, why = ROUTE[d["shape"]]
    print(f"{d['desc']:52} -> {dest}")
    print(f"{'':52}    ({why})")
print("\nWrong store, real consequences:")
print("  logs pushed as metrics   -> every distinct message becomes a series; cardinality explosion")
print("  metrics scraped as logs  -> no aggregation, no rate(), no alerting on trends")
print("  traces without spans     -> you have timestamps but cannot follow one request end to end")
EOF
```

**Expected result:** Each data shape routes to the store built for it, with the failure modes for mismatches named. The three failures are worth internalizing because each is silent at ingest time — nothing rejects logs pushed into a metrics store; the damage shows up later as query latency, cost, or an aggregation you cannot perform.

**Negative test:** Sending everything to one store "for simplicity" — you inherit the worst properties of each mismatch, and unpicking it later means re-instrumenting collection.

**Cleanup:** None.

### Lab 2.3 — Validate ingestion instead of trusting the agent

**Objective:** Prove data arrived.

```bash
python3 - <<'EOF'
def diagnose(agent_running, auth_ok, egress_allowed, relabel_keeps_series, backend_has_recent_data):
    if backend_has_recent_data:
        return "HEALTHY — data queried back from the backend within the expected window"
    if not agent_running:      return "agent not running — check the DaemonSet/Deployment and pod events"
    if not auth_ok:            return "AUTH FAILURE — remote-write rejected; check the token/stack URL"
    if not egress_allowed:     return "EGRESS BLOCKED — network policy or firewall; agent looks fine locally"
    if not relabel_keeps_series: return ("RELABELING DROPPED EVERYTHING — the pipeline is 'working' and "
                                         "discarding all series; the agent reports healthy")
    return "data not yet visible — check the backend's ingest lag before assuming failure"

cases = [
  ("all good",              True, True, True, True, True),
  ("bad token",             True, False,True, True, False),
  ("network policy blocks", True, True, False,True, False),
  ("over-aggressive relabel",True,True, True, False,False),
  ("agent restart loop",    False,True, True, True, False),
]
for label, *state in cases:
    print(f"{label:24} -> {diagnose(*state)}")
print("\nEvery failing case except the restart loop leaves an agent that LOOKS healthy.")
print("The only proof of ingestion is QUERYING THE BACKEND for your data.")
print("Validate after every collection change, and alert on 'no data received' per source —")
print("silence from a telemetry pipeline is indistinguishable from a quiet system.")
EOF
```

**Expected result:** Four of five failure modes leave a healthy-looking agent, and only querying the backend distinguishes them. The final line generalizes a theme that recurs across this encyclopedia's observability volumes: **absence of data looks exactly like absence of problems**, so a pipeline needs an explicit "no data received" alert per source.

**Negative test:** Treating a green agent status as confirmation — the collector is reporting on itself, not on whether the backend accepted anything.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Collection distinguished from instrumentation, and Alloy's role in the pipeline described.
- [ ] The Kubernetes Monitoring Helm chart understood as preconfigured collection for all three signals.
- [ ] The process stage used to control cardinality before data reaches the backend.
- [ ] Each signal routed to its matching store, with mismatch consequences known.
- [ ] Ingestion validated by querying the backend, with per-source no-data alerting.
