# Chapter 06: Traces and Correlating the Three Signals

## Learning Objectives

- Explain distributed tracing: traces, spans, parent-child relationships, and context propagation.
- Read a trace to find where latency actually goes.
- Correlate metrics, logs, and traces to move from symptom to cause.
- Use exemplars to jump from a metric spike to a representative trace.

## What each signal is good at

The GROT Academy curriculum devotes a whole module to using the three signals *together*, and the reason is that each answers a different question:

| Signal | Answers | Weak at |
|:---|:---|:---|
| **Metrics** | *Is something wrong, and since when?* Cheap, aggregate, easy to alert on | Explaining **why** — no per-request detail |
| **Logs** | *What happened in this component?* Rich detail | Following one request **across** services |
| **Traces** | *Where did this request spend its time, across every service?* | Aggregate trends; expensive to keep in full |
| **Profiles** | *Which code inside a process consumed the resource?* | Anything above the process boundary |

Nobody debugs with one. The workflow that actually works is **metric → trace → log**: a metric tells you something is wrong, a trace tells you which service and which operation, and logs tell you what that service was thinking.

## Traces and spans

A **trace** is one request's journey. It is a tree of **spans**, each with a name, a service, a start time, a duration, a parent, and attributes.

Two properties do the work:

- **Parent-child structure** shows what called what.
- **Context propagation** — passing the trace ID and span ID across service boundaries in headers — is what makes the tree possible. **If propagation breaks, you get disconnected fragments instead of one trace**, which is the single most common tracing defect.

### Reading a trace

The instinct is to look for the longest span, which is usually the root — and the root is long *by definition*, because it contains everything else. What you actually want is **self time**: a span's duration minus the time its children accounted for. High self time is where the work happened.

The other pattern worth recognizing is **serial versus parallel children**. Five 100 ms calls made sequentially cost 500 ms; made concurrently they cost about 100 ms. A trace shows you which you have.

## Sampling

Keeping every trace is expensive at volume, so systems sample:

| Strategy | How it decides | Trade |
|:---|:---|:---|
| **Head sampling** | At the start, before the outcome is known | Cheap and simple; **will discard the slow and failed requests you most want** |
| **Tail sampling** | After the trace completes, using its outcome | Keeps errors and slow traces; needs buffering and more resources |

If you can only afford one insight here: **head sampling at 1% means 99% of your incidents have no trace.** Tail sampling that always keeps errors and outliers is dramatically more useful for the same storage.

## Correlation

Grafana's value across these signals is the **linking**:

- **Exemplars** attach a trace ID to a metric sample, so a spike in a latency histogram links directly to a representative slow trace.
- **Trace to logs** uses the trace ID (and time range) to find the log lines emitted during that request.
- **Logs to trace** works in reverse when a log line carries a trace ID.

The trace ID is the join key across all three — which is exactly why Chapter 05 insisted it should *not* be a Loki label. You find it by filtering within a selected stream, not by indexing millions of values.

## Hands-On Lab

Python models tracing. **Cost:** none.

### Lab 6.1 — Read a trace by self time

**Objective:** Find the real bottleneck rather than the longest span.

```bash
python3 - <<'EOF'
spans = [
  {"id":"1","parent":None,"service":"frontend","op":"GET /checkout","start":0,"dur":840},
  {"id":"2","parent":"1","service":"api",     "op":"POST /orders",  "start":15,"dur":800},
  {"id":"3","parent":"2","service":"api",     "op":"validate",      "start":20,"dur":30},
  {"id":"4","parent":"2","service":"postgres","op":"SELECT items",  "start":55,"dur":40},
  {"id":"5","parent":"2","service":"inventory","op":"GET /stock",   "start":100,"dur":690},
  {"id":"6","parent":"5","service":"redis",   "op":"GET cache",     "start":105,"dur":5},
  {"id":"7","parent":"5","service":"vendor-api","op":"POST /reserve","start":115,"dur":665},
]
kids = {}
for s in spans: kids.setdefault(s["parent"], []).append(s)
def self_time(s): return s["dur"] - sum(c["dur"] for c in kids.get(s["id"], []))

def show(s, depth=0):
    st = self_time(s)
    bar = "#" * max(1, int(st/25))
    print(f"{'  '*depth}{s['service']:12} {s['op']:16} total {s['dur']:>4}ms  self {st:>4}ms {bar}")
    for c in sorted(kids.get(s["id"], []), key=lambda x: x["start"]): show(c, depth+1)
show(spans[0])

worst = max(spans, key=self_time)
print(f"\nLongest TOTAL span: frontend GET /checkout at 840ms — but it CONTAINS everything.")
print(f"Highest SELF time:  {worst['service']} {worst['op']} at {self_time(worst)}ms  <-- the actual bottleneck")
print("\n665 of 840ms is one call to a third-party vendor API. No amount of optimizing your own")
print("code fixes this: the answer is caching, an async flow, or a conversation with the vendor.")
EOF
```

**Expected result:** The root span is longest at 840 ms, but the third-party `vendor-api` call has the highest self time at 665 ms. The conclusion is the kind traces exist to produce — the fix is not in your code at all, which is something no amount of metric-staring would have told you.

**Negative test:** Optimizing the slowest *service* by total time — that is your own API at 800 ms, of which it spent only 35 ms doing work; you would tune the wrong thing entirely.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Head versus tail sampling

**Objective:** Show what each strategy keeps.

```bash
python3 - <<'EOF'
import random
random.seed(7)
traces = []
for i in range(10000):
    err = random.random() < 0.01                      # 1% errors
    slow = random.random() < 0.02                     # 2% slow
    traces.append({"id":i,"error":err,"slow":slow})

def head_sample(traces, rate=0.01):                   # decide BEFORE outcome known
    return [t for t in traces if random.random() < rate]
def tail_sample(traces, base_rate=0.01):              # decide AFTER completion
    return [t for t in traces if t["error"] or t["slow"] or random.random() < base_rate]

errors = sum(t["error"] for t in traces); slows = sum(t["slow"] for t in traces)
h, t = head_sample(traces), tail_sample(traces)
print(f"population: {len(traces)} traces, {errors} errors, {slows} slow\n")
for name, kept in (("head (1%)", h), ("tail (errors+slow+1%)", t)):
    ke, ks = sum(x["error"] for x in kept), sum(x["slow"] for x in kept)
    print(f"{name:24} kept {len(kept):>4} traces | errors {ke:>3}/{errors} ({ke/errors*100:5.1f}%) "
          f"| slow {ks:>3}/{slows} ({ks/slows*100:5.1f}%)")
print("\nHead sampling keeps ~1% of errors — so ~99% of incidents have NO TRACE when you go looking.")
print("Tail sampling keeps ALL of them for a modest increase in stored traces.")
print("It costs more to run (traces must be buffered until complete) and is almost always worth it.")
EOF
```

**Expected result:** Head sampling retains **none** of the 107 error traces in this run — 1% of 107 rounds to about one, and the draw came up empty — while tail sampling retains all 107 and all 200 slow traces for roughly 290 extra stored traces. The framing that matters: sampling strategy determines **whether tracing helps during an incident**, and head sampling optimizes storage at the direct expense of the cases you built tracing for.

**Negative test:** Choosing head sampling for simplicity and discovering during an outage that no trace of the failing requests was kept — the data was discarded before anyone knew it mattered.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Metric → trace → log

**Objective:** Walk the correlation path from symptom to cause.

```bash
python3 - <<'EOF'
metric_samples = [
  {"t":"10:00","p99_ms":180,"exemplar_trace":None},
  {"t":"10:05","p99_ms":190,"exemplar_trace":None},
  {"t":"10:10","p99_ms":2400,"exemplar_trace":"trace-9f2c"},   # exemplar attached to the spike
]
traces = {"trace-9f2c":[
  {"service":"api","op":"POST /orders","dur":2380,"self":25},
  {"service":"vendor-api","op":"POST /reserve","dur":2310,"self":2310,"status":"error"},
]}
logs = {"trace-9f2c":[
  {"service":"api","line":'{"level":"warn","msg":"vendor call slow","trace_id":"trace-9f2c"}'},
  {"service":"api","line":'{"level":"error","msg":"vendor timeout after 2300ms","trace_id":"trace-9f2c"}'},
]}

print("STEP 1 — METRIC: something is wrong, and when")
for m in metric_samples:
    flag = "  <-- SPIKE (exemplar: " + m["exemplar_trace"] + ")" if m["p99_ms"] > 1000 else ""
    print(f"   {m['t']}  p99 = {m['p99_ms']:>4} ms{flag}")

tid = metric_samples[-1]["exemplar_trace"]
print(f"\nSTEP 2 — TRACE: click the exemplar -> {tid}; where did the time go?")
for s in traces[tid]:
    mark = "  <-- highest self time" if s["self"] > 1000 else ""
    print(f"   {s['service']:12} {s['op']:16} {s['dur']:>5}ms (self {s['self']}ms){mark}")

print(f"\nSTEP 3 — LOGS: filter the stream by trace_id = {tid}")
for l in logs[tid]:
    print(f"   {l['service']:12} {l['line']}")

print("\nSymptom to cause in three moves, each answering what the previous could not:")
print("   metric = WHEN  ->  trace = WHERE  ->  logs = WHAT")
print("\nNote step 3 filters by trace_id at QUERY time — trace_id is NOT a Loki label (ch05).")
EOF
```

**Expected result:** A p99 spike carries an exemplar to a specific trace, the trace localizes the time to a vendor call, and logs filtered by trace ID give the timeout message. The three-move summary — **metric = when, trace = where, logs = what** — is the workflow the correlation module exists to teach, and each step answers a question the previous signal structurally cannot.

**Negative test:** Trying to debug the spike from metrics alone — you can see p99 rose at 10:10 and nothing about which dependency caused it, so the next step is guesswork.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Traces, spans, parent-child structure, and context propagation explained.
- [ ] Traces read by self time rather than total duration.
- [ ] Head and tail sampling compared by what they retain during incidents.
- [ ] The metric → trace → log workflow walked, with exemplars and trace-ID filtering.
