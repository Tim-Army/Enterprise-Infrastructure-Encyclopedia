# Chapter 03: Grail, DQL, and DPL

## Learning Objectives

- Explain Grail's data model — buckets, tables, and views — and why it needs no up-front schema.
- Write DQL pipelines and order the stages for cost as well as correctness.
- Use DPL to extract structure from unstructured records.
- Recognize how schema-on-read changes what "expensive query" means.

*Exam relevance: **DQL/DPL** and **Grail** appear in the Advanced Observability, Advanced Security, and DEM Specialist skill lists — DQL is the single most cross-cutting skill in the Dynatrace catalog.*

## Grail

Dynatrace describes Grail as **"the Dynatrace data lakehouse designed explicitly for observability data,"** holding "logs, metrics, traces, events, and more" in one store, with "a real-time model that reflects the topology and dependencies within a monitored environment."

Its data model is **buckets, tables, and views**, and its defining property is that it requires **"no up-front description of the input data's schema."**

That last point deserves unpacking, because it inverts a trade-off the other volumes in this reading path make explicitly:

| Approach | Cost paid at | Consequence |
|:---|:---|:---|
| **Index-on-write** (Elasticsearch, Splunk) | Ingestion | Fast arbitrary search, expensive to ingest, schema decided early |
| **Labels-only index** (Loki) | Query, if the selector is poor | Cheap ingest, needs a good stream selector |
| **Schema-on-read** (Grail) | Query | Ingest anything without deciding its shape; the query does the structuring |

The practical effect: you can send Grail a log format nobody planned for and query it later. The bill for that flexibility arrives at query time, which is why the ordering discipline below matters as much here as `sum(rate())` ordering does in PromQL.

## DQL

DQL is a **pipeline language**: a query starts by fetching a data source and then passes records through stages, each narrowing or reshaping.

| Command | Does |
|:---|:---|
| `fetch` | Starts the pipeline against a table (`logs`, `spans`, `events`, `metrics`, `dt.entity.*`) |
| `filter` | Keeps matching records |
| `parse` | Extracts fields using **DPL** |
| `fields` / `fieldsAdd` | Selects or computes columns |
| `summarize` | Aggregates — counts, averages, percentiles, grouped |
| `sort` | Orders |
| `limit` | Caps rows |

A representative query:

```dql
fetch logs
| filter dt.entity.host == "HOST-1234" and loglevel == "ERROR"
| parse content, "LD 'user=' WORD:user"
| summarize count(), by:{user}
| sort `count()` desc
| limit 10
```

**Ordering rule, and it is the whole game:** `filter` before `parse`, and both before `summarize`. Parsing is per-record work. Filtering a billion records down to a thousand and parsing those thousand is dramatically cheaper than parsing a billion and filtering afterward — and DQL will happily let you write it the expensive way.

The parallel to [LogQL](../../volume-139-grafana-observability/chapters/05-loki-and-logql.md) is exact, and it is worth carrying between the two: **cheap stages first.**

## DPL

**Dynatrace Pattern Language** describes patterns with matchers rather than raw regular expressions. Matchers are named for what they match — `INT`, `WORD`, `IPADDR`, `TIMESTAMP`, `LD` (line data), `SPACE` — and you bind them to field names with `:`.

```text
LD 'status=' INT:status ' duration=' INT:duration_ms
```

The argument for DPL over regex is legibility and intent: `IPADDR:client` states what it is looking for, where the equivalent regex states only a shape and leaves the reader to infer the meaning. On a query someone else has to maintain at 3 a.m., that difference is not cosmetic.

## Hands-On Lab

Python models Grail and DQL. **Cost:** none.

### Lab 3.1 — Stage ordering and query cost

**Objective:** Quantify why `filter` precedes `parse`.

```bash
python3 - <<'EOF'
RECORDS      = 1_000_000_000       # records in the scanned time range
MATCH_RATE   = 0.000_002           # filter keeps 2 per million
COST_SCAN    = 1                   # arbitrary units per record scanned
COST_PARSE   = 40                  # parsing is ~40x scanning per record

kept = int(RECORDS * MATCH_RATE)

good = RECORDS*COST_SCAN + kept*COST_PARSE          # filter, then parse
bad  = RECORDS*COST_SCAN + RECORDS*COST_PARSE       # parse, then filter

print("fetch logs | filter ... | parse ... | summarize ...")
print(f"  records in range : {RECORDS:,}")
print(f"  survive filter   : {kept:,}\n")
print(f"{'ordering':34}{'cost units':>18}")
print(f"{'filter -> parse  (correct)':34}{good:>18,}")
print(f"{'parse  -> filter (expensive)':34}{bad:>18,}")
print(f"\nratio: {bad/good:.1f}x more expensive to parse first")
print(f"parsing {RECORDS:,} records to keep {kept:,} of them wastes")
print(f"{(RECORDS-kept)*COST_PARSE:,} cost units on records that are discarded.")
print("\nSchema-on-read means Grail accepted this data with no up-front modeling.")
print("That flexibility is real, and the bill for it arrives at QUERY time —")
print("so stage ordering is not a micro-optimization here, it is the cost model.")
EOF
```

**Expected result:** Parsing first is about 41 times more expensive, wasting roughly 40 billion cost units on records that are immediately thrown away. The closing point ties it back to the architecture: schema-on-read moves the cost from ingest to query, so the query author — not the platform team — controls whether the system is affordable.

**Negative test:** Writing `fetch | parse | filter` because it reads more naturally left-to-right. It returns identical results at many times the cost, and nothing in the output signals the waste.

**Cleanup:** None.

### Lab 3.2 — Build a DQL pipeline

**Objective:** Assemble and reason about a real query.

```bash
python3 - <<'EOF'
import re, collections
LOGS = [
  '2026-08-04T10:00:01Z host=web-1 level=ERROR status=500 duration=1420 user=alice path=/checkout',
  '2026-08-04T10:00:02Z host=web-1 level=INFO  status=200 duration=95   user=bob   path=/browse',
  '2026-08-04T10:00:03Z host=web-2 level=ERROR status=503 duration=2310 user=alice path=/checkout',
  '2026-08-04T10:00:04Z host=web-1 level=WARN  status=200 duration=880  user=carol path=/search',
  '2026-08-04T10:00:05Z host=web-2 level=ERROR status=500 duration=1990 user=dave  path=/checkout',
  '2026-08-04T10:00:06Z host=web-3 level=INFO  status=200 duration=110  user=alice path=/browse',
  '2026-08-04T10:00:07Z host=web-2 level=ERROR status=500 duration=1750 user=alice path=/pay',
]
print("DQL:")
print("  fetch logs")
print("  | filter level == \"ERROR\"")
print("  | parse content, \"LD 'duration=' INT:duration LD 'user=' WORD:user\"")
print("  | summarize cnt = count(), avg_ms = avg(duration), by:{user}")
print("  | sort cnt desc\n")

stage = LOGS
print(f"fetch logs                -> {len(stage)} records")
stage = [l for l in stage if 'level=ERROR' in l]
print(f"| filter level == ERROR   -> {len(stage)} records   (cheap: substring)")
parsed = []
for l in stage:
    d = int(re.search(r'duration=(\d+)', l).group(1))
    u = re.search(r'user=(\w+)', l).group(1)
    parsed.append({"user": u, "duration": d})
print(f"| parse (DPL)             -> {len(parsed)} records parsed, NOT {len(LOGS)}")

agg = collections.defaultdict(list)
for r in parsed: agg[r["user"]].append(r["duration"])
rows = sorted(((u, len(v), sum(v)/len(v)) for u, v in agg.items()), key=lambda r: -r[1])
print(f"| summarize by user\n")
print(f"  {'user':8}{'cnt':>5}{'avg_ms':>10}")
for u, c, a in rows: print(f"  {u:8}{c:>5}{a:>10.0f}")
print(f"\nParse ran on {len(stage)} of {len(LOGS)} records because filter came first.")
print("\nDPL matchers name their intent: INT:duration and WORD:user say WHAT is")
print("being extracted. The regex equivalent, \\d+ and \\w+, says only what SHAPE to")
print("expect — the meaning lives in the author's head instead of the query.")
EOF
```

**Expected result:** Four ERROR records survive the filter, only those get parsed, and Alice appears three times with the highest average duration. The mechanical takeaway is that the parse stage processed 4 records rather than 7; at production scale that ratio is the difference between a query that returns and one that times out.

**Negative test:** Omitting the filter entirely and parsing everything to "see what's there." Exploration is legitimate, but do it on a narrow time range, not a wide one.

**Cleanup:** None.

### Lab 3.3 — Schema-on-read against three log formats

**Objective:** Show what accepting arbitrary shapes buys you.

```bash
python3 - <<'EOF'
# Three services, three formats, none coordinated with the platform team
SOURCES = {
  "checkout (JSON)":  '{"ts":"...","lvl":"error","msg":"declined","order_id":"A-9931","ms":1420}',
  "legacy (syslog)":  '<134>Aug  4 10:00:01 billing[4412]: TXN FAILED id=A-9931 rc=51 elapsed=1420ms',
  "gateway (CSV)":    '2026-08-04T10:00:01Z,A-9931,DECLINE,51,1420',
}
print("Three services emit the SAME event in three formats:\n")
for name, line in SOURCES.items():
    print(f"  {name:18} {line}")

print("\n--- index-on-write platform (schema decided at ingest) ---")
print("  requires: a parser/mapping per format, agreed BEFORE data arrives")
print("  a new format = a pipeline change + reindex; until then, data is unusable")
print("  the legacy service usually just... never gets onboarded")

print("\n--- Grail (schema-on-read) ---")
print("  requires: nothing at ingest. All three land as records.")
print("  the query supplies the structure, per format, at read time:")
print()
print('  fetch logs | filter matchesValue(dt.entity.service, "checkout")')
print('    | parse content, "JSON:j" | fieldsAdd order = j[order_id], ms = j[ms]')
print()
print('  fetch logs | filter matchesValue(dt.entity.service, "billing")')
print('    | parse content, "LD \'id=\' WORD:order LD \'elapsed=\' INT:ms"')
print()
print("  ...then both can be summarized on the SAME field names and joined.")

print("\nThe trade is explicit, not free:")
print("  gained  — the legacy service is queryable on day one, with no pipeline work")
print("  paid    — every query carries the parsing cost, forever, for every reader")
print("  implied — a heavily-read source is worth normalizing anyway; schema-on-read")
print("            removes the BLOCKER to onboarding, not the VALUE of good structure")
EOF
```

**Expected result:** All three formats are queryable without ingest-time modeling, at the cost of per-query parsing. The final block is the honest reading: schema-on-read is not an argument against structured logging — it removes the barrier that leaves awkward legacy sources permanently unmonitored, while a frequently-queried source still repays being normalized.

**Negative test:** Concluding that log formats no longer matter. Deferring the cost is not eliminating it, and a popular badly-shaped source pays that cost on every query by every user.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Grail described as a schema-on-read lakehouse with buckets, tables, and views.
- [ ] DQL pipelines written with cheap stages first — filter before parse before summarize.
- [ ] DPL matchers used for legible, intent-revealing extraction.
- [ ] The schema-on-read trade-off stated honestly in both directions.
