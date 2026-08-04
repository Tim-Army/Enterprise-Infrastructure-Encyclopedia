# Chapter 03: Data Sources, Queries, and Transformations

## Learning Objectives

- Configure data sources and understand Grafana's query-where-it-lives model.
- Combine multiple data sources in one dashboard and one panel.
- Apply transformations to reshape query results without changing the source.
- Use variables and templating to build dashboards that adapt.

## Query where the data lives

Grafana's founding architectural choice is that it **does not own your data**. It connects to backends and queries them in place, which has three consequences worth stating:

1. **No migration required.** Grafana sits on top of what you already run.
2. **Query capability is the backend's.** Grafana cannot make a data source do something it cannot do; PromQL features come from Prometheus, not from Grafana.
3. **One pane, many sources.** A dashboard can mix Prometheus, Loki, Tempo, PostgreSQL, and a cloud provider's monitoring API.

Common data sources include the Grafana stack (Prometheus/Mimir, Loki, Tempo, Pyroscope), SQL databases, cloud monitoring services, Elasticsearch, and a **TestData** source that generates synthetic data — genuinely useful for building and demonstrating panels before real data exists.

## Transformations

A **transformation** reshapes query results **inside Grafana**, after the query returns and before the panel renders. This is the tool for the very common case where the data you have is not shaped like the visualization you want.

| Transformation | Use |
|:---|:---|
| **Filter fields / by value** | Drop columns or rows you do not want shown |
| **Organize fields** | Rename, reorder, hide |
| **Join by field** | Combine results from **different queries or data sources** on a shared key |
| **Group by** | Aggregate rows |
| **Add field from calculation** | Derive a column — ratios, differences, percentages |
| **Reduce** | Collapse a series to a single value (last, max, mean) |
| **Rows to fields / labels to fields** | Pivot between long and wide shapes |

**Join by field** is the one that unlocks genuinely cross-source analysis: query business data from PostgreSQL and infrastructure metrics from Prometheus, join on a service name, and compute cost per request in a panel.

The discipline: transform in the **query** when the backend can do it efficiently (aggregation over millions of series belongs in PromQL), and transform in **Grafana** when you are reshaping a modest result set or combining sources the backend cannot see.

## Variables and templating

**Variables** turn one dashboard into many. Declared once, referenced as `$name` in queries and titles, they let a viewer switch environment, cluster, service, or instance without editing anything.

| Variable type | Source of values |
|:---|:---|
| **Query** | Values fetched from a data source (for example, all namespaces) |
| **Custom** | A fixed list you type |
| **Constant** | A value hidden from the viewer |
| **Interval** | Time windows for rate calculations (`$__interval` and friends) |
| **Data source** | Switch the whole dashboard between sources |
| **Text box** | Free-form viewer input |

Two properties matter in practice. **Chaining**: a `pod` variable whose query filters on `$namespace` narrows as the viewer chooses, so the lists stay usable. **Multi-value and All**: a variable that returns several values must be interpolated correctly in the query — usually as a regex alternation — or the panel silently returns only one series.

## Hands-On Lab

Python models querying and transformation. **Cost:** none.

### Lab 3.1 — Join across data sources

**Objective:** Combine results the backends cannot join themselves.

```bash
python3 - <<'EOF'
# Query A: infrastructure metrics (Prometheus)
prom = [
  {"service":"checkout","requests_per_sec":420.0,"cpu_cores":6.2},
  {"service":"search",  "requests_per_sec":1310.0,"cpu_cores":4.1},
  {"service":"profile", "requests_per_sec":95.0, "cpu_cores":3.8},
]
# Query B: business/cost data (PostgreSQL) — a DIFFERENT data source
sql = [
  {"service":"checkout","monthly_cost_usd":4100},
  {"service":"search",  "monthly_cost_usd":2600},
  {"service":"profile", "monthly_cost_usd":2900},
]
by_service = {r["service"]: dict(r) for r in prom}
for r in sql:                                    # JOIN BY FIELD on 'service'
    by_service[r["service"]].update(r)

print(f"{'service':10}{'req/s':>9}{'cores':>7}{'$/mo':>8}{'$ per req/s':>13}{'cores/req':>11}")
for s, r in by_service.items():
    cost_per_rps = r["monthly_cost_usd"] / r["requests_per_sec"]      # ADD FIELD FROM CALCULATION
    cores_per_rps = r["cpu_cores"] / r["requests_per_sec"] * 1000
    print(f"{s:10}{r['requests_per_sec']:>9.0f}{r['cpu_cores']:>7.1f}"
          f"{r['monthly_cost_usd']:>8}{cost_per_rps:>13.2f}{cores_per_rps:>11.2f}")

print("\nNeither backend could compute this: Prometheus has no cost data, Postgres has no metrics.")
print("The join happens in GRAFANA, after both queries return.")
print("\nWhat it reveals: 'profile' costs $30.53 per req/s while 'search' costs $1.98 —")
print("a 15x efficiency gap invisible in either data source alone.")
EOF
```

**Expected result:** A joined table exposing that `profile` costs about 15 times more per unit of traffic than `search`. The insight exists in **neither** source — Prometheus has no billing data, the database has no metrics — which is precisely the case transformations exist for.

**Negative test:** Exporting both datasets to a spreadsheet each month to do this by hand — the analysis goes stale immediately and nobody repeats it, whereas a transformed panel updates itself.

**Cleanup:** None.

### Lab 3.2 — Variable chaining and multi-value interpolation

**Objective:** Build variables that stay usable at scale, and interpolate them correctly.

```bash
python3 - <<'EOF'
INVENTORY = {
  ("prod","eu-west"):  ["api-1","api-2","api-3"],
  ("prod","us-east"):  ["api-4","api-5"],
  ("staging","eu-west"):["api-s1"],
}
def options(var_name, selections):
    if var_name == "env":     return sorted({e for e, _ in INVENTORY})
    if var_name == "region":  return sorted({r for e, r in INVENTORY if e == selections.get("env")})
    if var_name == "pod":     return INVENTORY.get((selections.get("env"), selections.get("region")), [])
    return []

sel = {}
for var in ("env","region","pod"):
    opts = options(var, sel)
    sel[var] = opts[0] if opts else None
    print(f"${var:7} options={opts}  -> selected '{sel[var]}'")
print("\nChaining keeps each list SHORT and RELEVANT: region only shows regions that exist in the")
print("chosen env, pod only shows pods in that env+region. Without it, $pod lists every pod you own.")

print("\n--- multi-value interpolation ---")
chosen = ["api-1","api-2","api-3"]
print(f'WRONG: pod="{",".join(chosen)}"            -> matches nothing; no pod is literally named that')
print(f'RIGHT: pod=~"{"|".join(chosen)}"           -> regex alternation, matches all three')
print("\nA multi-value variable interpolated as an exact match silently returns ONE series or none.")
print("The panel renders, shows less data than expected, and nothing errors.")
EOF
```

**Expected result:** Chained variables narrow from environment to region to pod, and the interpolation comparison shows exact-match failing where regex alternation succeeds. The silent nature of the interpolation bug is the important part — the panel does not error, it simply under-reports, which is the hardest class of dashboard defect to notice.

**Negative test:** Building unchained variables on a large estate — the `pod` dropdown lists thousands of entries across every environment, and viewers pick the wrong one.

**Cleanup:** None.

### Lab 3.3 — Transform in the query or in Grafana?

**Objective:** Put the work in the right place.

```bash
python3 - <<'EOF'
def decide(op, series_count, cross_source, backend_can_do_it):
    if cross_source:
        return "GRAFANA", "spans data sources — the backend cannot see the other one"
    if not backend_can_do_it:
        return "GRAFANA", "the backend has no equivalent operation"
    if series_count > 10000:
        return "QUERY (backend)", f"{series_count:,} series — aggregate at the source, do not ship them all"
    return "either", "small result set; put it wherever it reads more clearly"

cases = [
  ("sum CPU across 50,000 pods",        50000, False, True),
  ("join metrics with billing rows",       12, True,  False),
  ("rename two columns",                    8, False, False),
  ("rate() over a counter",             25000, False, True),
  ("compute a ratio of two queries",       40, False, False),
]
for op, n, cross, backend in cases:
    where, why = decide(op, n, cross, backend)
    print(f"{op:34} -> {where:16} ({why})")
print("\nRule of thumb: AGGREGATE at the source, RESHAPE in Grafana.")
print("Shipping 50,000 series to the browser so Grafana can sum them is slow, expensive,")
print("and will eventually hit a query limit — the backend was built to do exactly that sum.")
EOF
```

**Expected result:** Large aggregations route to the backend, cross-source and cosmetic work to Grafana, small operations either way. The closing rule — aggregate at the source, reshape in Grafana — is the one that keeps dashboards fast as an estate grows, and the failure it prevents is a panel that works fine in staging and times out in production.

**Negative test:** Pulling raw series into Grafana and using Reduce to aggregate — it works at small scale and fails exactly when the system gets big enough to need the dashboard.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The query-where-it-lives model understood, including its limits.
- [ ] Cross-source joins used to derive insight neither backend holds.
- [ ] Variables chained, and multi-value interpolation handled with regex alternation.
- [ ] Aggregation placed at the source and reshaping in Grafana.
