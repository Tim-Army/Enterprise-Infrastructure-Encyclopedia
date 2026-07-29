# Chapter 04: Logs and Correlation

## Learning Objectives

- Explain the OTel logs data model and the log bridge.
- Emit logs correlated with traces.
- Attach resource and log attributes.
- Route logs through the Collector.
- Complete a walkthrough for each logging concept.

## Theory and Architecture

OTel **logs** capture timestamped events. Unlike traces/metrics, OTel largely
**bridges** existing logging libraries rather than replacing them: a **log appender /
bridge** feeds records from your logging framework into the OTel **LogRecord** model,
which carries a body, severity, attributes, and — critically — the **trace context**
(trace ID + span ID) of the active span. That trace correlation lets you jump from a log
line to the trace it belongs to. Logs are exported via OTLP (often through the
Collector, which can also receive host/file logs via receivers).

## Design Considerations

Correlate logs with traces by emitting them **within an active span** so the bridge
stamps `trace_id`/`span_id`. Use **structured** attributes over string interpolation,
set proper **severity**, and route logs through the **Collector** for consistent
processing with traces and metrics.

## Implementation and Automation

The labs use the Python logging bridge and the Collector's filelog receiver.

## Validation and Troubleshooting

Confirm the model:

```text
LogRecord: timestamp, severity, body, attributes, + trace_id/span_id (correlation).
Bridge/appender: feeds a logging library (logging, log4j, ...) into OTel.
Collector: OTLP logs receiver + filelog receiver for host/file logs.
```

Common pitfalls: logs emitted outside a span (no correlation); and unstructured string
logs (hard to query).

## Security and Best Practices

Emit logs **within spans** for correlation, use **structured** attributes, set
**severity** correctly, route through the **Collector** for redaction/processing, and
avoid logging secrets. Standardize attribute names via semantic conventions.

## Hands-On Lab

Logging walkthroughs. **Shared prerequisites** — Python with
`opentelemetry-sdk`; a running Collector. **Cost:** none.

### Lab 4.1 — Bridge the logging library

**Objective:** Send Python `logging` through OTel.

```python
import logging
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
lp = LoggerProvider(); lp.add_log_record_processor(BatchLogRecordProcessor(ConsoleLogExporter()))
logging.getLogger().addHandler(LoggingHandler(logger_provider=lp))
logging.getLogger("app").warning("cache miss", extra={"cache.key": "user:42"})
```

**Expected result:** the log record exported through OTel with its **attributes** — the
log bridge.

**Negative test:** print to stdout only; the **bridge** turns logs into structured OTel
records — use it.

**Cleanup:** none.

### Lab 4.2 — Correlate a log with a trace

**Objective:** Emit a log inside a span.

```python
from opentelemetry import trace
tracer = trace.get_tracer("demo")
with tracer.start_as_current_span("checkout"):
    logging.getLogger("app").error("payment declined")
    # the exported LogRecord carries the span's trace_id + span_id
```

**Expected result:** a log record stamped with the active span's **trace_id/span_id** —
log-to-trace correlation.

**Negative test:** log after the span ends; the record has **no trace context** — log
within the span.

**Cleanup:** none.

### Lab 4.3 — Receive host logs in the Collector

**Objective:** Configure the filelog receiver.

```yaml
receivers:
  filelog:
    include: [ /var/log/app/*.log ]
    operators: [ { type: json_parser } ]
exporters: { debug: {} }
service: { pipelines: { logs: { receivers: [filelog], exporters: [debug] } } }
```

**Expected result:** the Collector tailing and parsing app log files into OTel logs —
agentless log collection.

**Negative test:** ship raw files to a backend unparsed; the **filelog receiver +
operators** structure them — parse at collection.

**Cleanup:** remove the receiver config.

### Lab 4.4 — Attach resource attributes

**Objective:** Identify the source with resource attributes.

```python
from opentelemetry.sdk.resources import Resource
res = Resource.create({"service.name": "checkout", "deployment.environment": "prod"})
# pass resource=res to LoggerProvider(...) / TracerProvider(...) / MeterProvider(...)
```

**Expected result:** telemetry carrying **`service.name`/`deployment.environment`** —
consistent source identity across signals.

**Negative test:** emit signals with no `service.name`; backends can't attribute them —
set the **resource**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OTel logs bridge existing logging libraries into a structured LogRecord model that
carries trace context for correlation, exported via OTLP or collected by the Collector's
filelog receiver, all tagged with resource attributes. This chapter bridged, correlated,
and collected logs.

- [ ] I can bridge a logging library into OTel.
- [ ] I can correlate logs with traces.
- [ ] I can receive host logs via the filelog receiver.
- [ ] I can set resource attributes for source identity.
- [ ] I completed Labs 4.1–4.4 including each negative test.
