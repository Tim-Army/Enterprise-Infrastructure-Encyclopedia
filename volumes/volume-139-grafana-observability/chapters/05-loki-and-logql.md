# Chapter 05: Loki and LogQL

## Learning Objectives

- Explain Loki's index-the-labels, not-the-content design.
- Write LogQL queries: stream selectors, line filters, parsers, and label filters.
- Build metric queries from logs with `rate` and `sum by`.
- Avoid the label mistakes that make Loki slow and expensive.

## Loki's central design choice

Most log systems index the full text of every line, which makes arbitrary search fast and makes ingestion expensive — the index frequently rivals the data in size.

**Loki indexes only labels.** Log content is stored compressed and unindexed, and queries work by first selecting streams via labels, then **brute-force scanning** the matching content. The trade is deliberate:

| | Full-text indexed | **Loki (labels only)** |
|:---|:---|:---|
| Ingestion cost | High | **Low** |
| Storage cost | High (index + data) | **Low** (object storage) |
| Arbitrary text search | Fast anywhere | Fast **only within a well-selected stream** |
| Operational model | Index tuning | **Label design** |

Everything about using Loki well follows from this: **the stream selector determines how much data you scan**, and therefore how fast and how cheap your query is.

## LogQL structure

A LogQL query has up to four stages, applied left to right:

```logql
{app="api", env="prod"}          # 1. stream selector  (REQUIRED — indexed labels)
  |= "error" != "healthcheck"    # 2. line filters     (fast substring match)
  | json | status >= 500         # 3. parser + label filter (structured extraction)
  | line_format "{{.msg}}"       # 4. formatting
```

| Stage | Operators |
|:---|:---|
| **Stream selector** | `=`, `!=`, `=~`, `!~` on labels — the only indexed part |
| **Line filter** | `\|=` contains, `!=` not contains, `\|~` regex, `!~` not regex |
| **Parser** | `json`, `logfmt`, `pattern`, `regexp` — extract fields into labels |
| **Label filter** | Compare extracted values: `\| status >= 500`, `\| duration > 1s` |

**Order matters for performance.** Line filters are cheap and should come before parsers, which are expensive: filtering a million lines down to a thousand and then parsing those thousand is far faster than parsing a million and filtering afterward.

## Metrics from logs

LogQL can turn logs into time series, which is how you alert on log content:

```logql
sum(rate({app="api"} |= "error" [5m])) by (route)
```

This is genuinely useful when an application emits no metrics for something you need to watch. It is also more expensive than a metric would be — if you find yourself doing it constantly for the same thing, that is a signal the application should expose a counter instead (or that a recording rule should materialize it, Chapter 08).

## Labels in Loki: fewer than you think

The instinct carried over from other systems — add labels for everything — is actively harmful here, for the same cardinality reason as Chapter 04 but with a sharper edge: **each unique label combination is a separate stream**, and Loki keeps a chunk open per stream.

| Good labels (bounded) | Bad labels (unbounded) |
|:---|:---|
| `app`, `env`, `cluster`, `namespace`, `container`, `level` | `request_id`, `user_id`, `trace_id`, `path`, `ip`, the message itself |

The unbounded values still need to be searchable — and they are, through **line filters and parsers at query time**. That is precisely the design: put the low-cardinality dimensions in labels for selection, and reach everything else by scanning the selected streams.

## Hands-On Lab

Python models LogQL. **Cost:** none.

### Lab 5.1 — The four stages, and why order matters

**Objective:** Build a query pipeline and measure the cost of stage order.

```bash
python3 - <<'EOF'
import json, re
LOGS = []
for i in range(1000):
    LOGS.append({"labels":{"app":"api","env":"prod"},
                 "line": json.dumps({"msg":"request done","route":"/checkout" if i%3 else "/health",
                                     "status":500 if i%50==0 else 200,"dur_ms":i%400})})
for i in range(500):
    LOGS.append({"labels":{"app":"worker","env":"prod"},"line": json.dumps({"msg":"job ok","status":200})})

def run(selector, line_filter, parse, label_filter, order="filter-first"):
    scanned = parsed = 0
    out = []
    streams = [l for l in LOGS if all(l["labels"].get(k)==v for k,v in selector.items())]
    for l in streams:
        scanned += 1
        if order == "filter-first":
            if line_filter and line_filter not in l["line"]: continue
            parsed += 1
            rec = json.loads(l["line"]) if parse else {}
        else:                                    # parse everything, filter later
            parsed += 1
            rec = json.loads(l["line"]) if parse else {}
            if line_filter and line_filter not in l["line"]: continue
        if label_filter and not label_filter(rec): continue
        out.append(rec)
    return scanned, parsed, len(out)

sel = {"app":"api","env":"prod"}
for order in ("filter-first","parse-first"):
    s,p,m = run(sel, '"status":500', True, lambda r: r.get("status",0)>=500, order)
    print(f"{order:12} selector matched {s:>4} lines | JSON-parsed {p:>4} | result {m}")
print("\nSame answer, but parse-first parsed 1000 lines to keep 20 — 50x the work.")
print("Line filters are cheap substring matches; parsers are expensive. FILTER, THEN PARSE.")

s,_,_ = run({"env":"prod"}, None, False, None)
print(f"\nAnd the selector dominates everything: {{env=\"prod\"}} scans {s} lines,")
print(f"while {{app=\"api\",env=\"prod\"}} scans 1000. A vague selector is the #1 cause of slow LogQL.")
EOF
```

**Expected result:** Both orders return 20 matching lines, but parse-first does fifty times the parsing work, and a loose stream selector scans 1,500 lines instead of 1,000. The hierarchy to remember: **selector first (indexed), then line filters (cheap), then parsers (expensive)** — and the selector matters most because it is the only stage that avoids reading data at all.

**Negative test:** Writing `{env="prod"} | json | app="api"` — it returns the right answer by scanning and parsing every production log line, when `{app="api", env="prod"}` would have selected the streams directly from the index.

**Cleanup:** None.

### Lab 5.2 — Label design and stream explosion

**Objective:** Count streams and see which labels are safe.

```bash
python3 - <<'EOF'
def streams(dims):
    n = 1
    for _, v in dims: n *= v
    return n

good = [("app",12),("env",3),("cluster",4),("namespace",20),("level",5)]
print("Bounded labels:")
for k,v in good: print(f"   {k:11} {v:>8,} values")
print(f"   -> {streams(good):,} streams  (fine)\n")

for label, n in [("request_id", 5_000_000), ("user_id", 200_000), ("path", 50_000), ("trace_id", 8_000_000)]:
    print(f"add {label:11} ({n:,} values) -> {streams(good + [(label,n)]):,} streams")
print("\nEach stream is a separately-tracked, separately-chunked entity. Millions of them will")
print("degrade ingestion and query performance long before you run out of storage.")

print("\nBut you still need to FIND a request by its ID — and you can:")
print('   {app="api",env="prod"} |= "req-abc123"                     <- line filter')
print('   {app="api",env="prod"} | json | request_id="req-abc123"    <- parse + label filter')
print("\nThat IS the design: bounded dimensions in labels for SELECTION;")
print("everything else reachable by SCANNING the selected streams at query time.")
EOF
```

**Expected result:** Bounded labels yield 14,400 streams; adding `trace_id` yields over 115 billion. The second half is the constructive part — the high-cardinality values remain fully searchable through line filters and parsers, so nothing is lost by keeping them out of labels. That is the point people miss when they reach for a label.

**Negative test:** Adding `trace_id` as a label to make trace-to-log correlation easy — Chapter 06 shows correlation works by *querying* the trace ID within a selected stream, no label required.

**Cleanup:** None.

### Lab 5.3 — Metrics from logs

**Objective:** Derive a time series from log lines, and know when not to.

```bash
python3 - <<'EOF'
import json
logs = []
for minute in range(5):
    for i in range(100):
        status = 500 if (i % (10 if minute >= 3 else 50)) == 0 else 200   # error spike from minute 3
        logs.append({"t":minute,"route":"/checkout" if i%2 else "/search",
                     "line":json.dumps({"status":status})})

print("sum(rate({app=\"api\"} |= \"500\" [1m])) by (route)\n")
print(f"{'minute':>7}{'/checkout':>12}{'/search':>10}")
for m in range(5):
    per = {}
    for l in logs:
        if l["t"] != m: continue
        if '"status":500' not in l["line"]: continue
        per[l["route"]] = per.get(l["route"], 0) + 1
    print(f"{m:>7}{per.get('/checkout',0):>12}{per.get('/search',0):>10}")

print("\nThe error spike from minute 3 is now a TIME SERIES you can alert on and graph —")
print("without the application ever exposing an error counter.")
print("\nWhen NOT to do this: if you run the same log-derived metric constantly, it is cheaper")
print("and faster to have the app expose a real counter, or to materialize it as a RECORDING")
print("RULE (ch08). Log-to-metric queries rescan raw log data every single evaluation.")
EOF
```

**Expected result:** The error spike from minute 3 appears as a per-route time series derived purely from logs. The caveat is the operationally important half: this re-scans raw logs on every evaluation, so a query you run continuously — especially one backing an alert — belongs in a recording rule or, better, as a real application counter.

**Negative test:** Building an alert on a log-derived metric over a wide time range and a loose selector — it re-scans an enormous volume every evaluation interval, which is expensive and eventually times out.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Loki's labels-only indexing understood, and its consequences for query cost.
- [ ] LogQL's four stages written in the efficient order: select, filter, parse, format.
- [ ] Stream cardinality controlled, with high-cardinality values reached at query time instead.
- [ ] Metrics derived from logs, with the recording-rule and real-counter alternatives noted.
