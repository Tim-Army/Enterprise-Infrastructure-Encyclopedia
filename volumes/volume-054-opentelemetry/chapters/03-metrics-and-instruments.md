# Chapter 03: Metrics and Instruments

## Learning Objectives

- Explain the OTel metrics data model and instruments.
- Choose the right instrument: counter, up-down counter, gauge, histogram.
- Record measurements with attributes (dimensions).
- Configure views and aggregation.
- Complete a walkthrough for each metrics concept.

## Theory and Architecture

OTel **metrics** are aggregated numeric measurements. You record through
**instruments**: a **Counter** (monotonic sum, e.g., requests), an **UpDownCounter**
(non-monotonic, e.g., queue length), a **Gauge** (last value, e.g., temperature), and a
**Histogram** (distribution, e.g., latency), each either synchronous (recorded inline)
or asynchronous (observed via callback). Measurements carry **attributes** (dimensions)
and are aggregated by the SDK into metric points exported via OTLP. **Views** customize
which instruments are exported, their aggregation, and attribute filtering.

## Design Considerations

Pick the instrument by **semantics** (monotonic? distribution?). Keep attribute
**cardinality** bounded — every unique attribute combination is a separate time series.
Use **histograms** for latency (percentiles) and **views** to drop or rename dimensions.

## Implementation and Automation

The labs use the Python SDK to record with each instrument type and configure a view.

## Validation and Troubleshooting

Confirm the model:

```text
Instruments: Counter (monotonic), UpDownCounter (non-monotonic), Gauge (last value),
Histogram (distribution). Sync (record) or Async (observe callback).
Attributes = dimensions -> each combo is a time series. Views customize export/aggregation.
```

Common pitfalls: unbounded attribute cardinality (time-series explosion); and a Counter
where an UpDownCounter is needed.

## Security and Best Practices

Match the **instrument** to the semantics, bound **attribute cardinality**, prefer
**histograms** for latency, and use **views** to control what's exported. Avoid
high-cardinality identifiers (user IDs) as attributes.

## Hands-On Lab

Metrics walkthroughs. **Shared prerequisites** — Python with `opentelemetry-sdk`; a
running Collector. **Cost:** none.

### Lab 3.1 — Counter

**Objective:** Record a monotonic counter.

```python
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=2000)
set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = get_meter_provider().get_meter("demo")
reqs = meter.create_counter("http.server.requests")
reqs.add(1, {"http.route": "/checkout", "http.status_code": 200})
```

**Expected result:** a **counter** point for `/checkout` exported to the console — a
monotonic sum.

**Negative test:** use a counter for a value that decreases (queue depth); use an
**UpDownCounter** instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Histogram

**Objective:** Record a latency distribution.

```python
latency = meter.create_histogram("http.server.duration", unit="ms")
for ms in (12, 45, 130, 22): latency.record(ms, {"http.route": "/checkout"})
```

**Expected result:** a **histogram** capturing the latency distribution (buckets/counts)
— percentile-ready data.

**Negative test:** track latency with a gauge (last value only); a **histogram** gives
distribution/percentiles — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Async gauge (observation)

**Objective:** Observe a value via callback.

```python
def cpu_cb(observer):
    observer.observe(0.37, {"host": "web01"})
meter.create_observable_gauge("system.cpu.utilization", callbacks=[cpu_cb])
```

**Expected result:** an **observable gauge** reporting CPU each collection — the async
pattern for sampled values.

**Negative test:** synchronously record a value you can only sample; an **async gauge**
observes it on the collection cycle.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — A view to bound cardinality

**Objective:** Drop a high-cardinality attribute via a view.

```python
from opentelemetry.sdk.metrics.view import View
# View: for http.server.requests, keep only http.route (drop user id, etc.)
view = View(instrument_name="http.server.requests", attribute_keys={"http.route"})
# pass views=[view] to MeterProvider(...)
```

**Expected result:** the metric exported with **only `http.route`** — bounded
cardinality via a view.

**Negative test:** export every attribute including user id; cardinality **explodes** —
filter with a view.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OTel metrics record through instruments (counter, up-down counter, gauge, histogram),
synchronous or asynchronous, with bounded-cardinality attributes and views to control
export. This chapter recorded each instrument type and applied a view.

- [ ] I can choose the right instrument by semantics.
- [ ] I can record counters and histograms.
- [ ] I can observe async gauges via callbacks.
- [ ] I can bound cardinality with a view.
- [ ] I completed Labs 3.1–3.4 including each negative test.
