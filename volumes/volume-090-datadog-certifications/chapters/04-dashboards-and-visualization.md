# Chapter 04: Dashboards and Data Visualization

## Learning Objectives

- Distinguish timeboards from screenboards.
- Build a dashboard with widgets.
- Use template variables to make a dashboard dynamic.
- Choose the right visualization for the data.
- Complete a walkthrough for each dashboard topic.

## Theory and Architecture

**Data visualization** is a core **Fundamentals** domain. Datadog **dashboards** come in two styles: the
**timeboard** (a time-synchronized grid — all graphs share one time range, ideal for correlating metrics
during an incident) and the **screenboard** (free-form layout mixing widgets, images, and text, ideal
for status/NOC displays). Dashboards are built from **widgets** — **timeseries** (line/bar/area),
**query value** (a single number), **top list**, **heat map**, **distribution**, **table**, and more —
each backed by a metric query. **Template variables** turn a dashboard into a reusable tool: a variable
like `$env` or `$host` (bound to a tag) adds dropdowns that re-scope every widget at once. Choosing the
right widget — timeseries for trends, top list for ranking, heat map for distributions across hosts — is
part of the skill. This chapter teaches dashboards with hands-on walkthroughs (dashboard JSON via the
API).

## Design Considerations

Use a **timeboard** for troubleshooting (shared time range) and a **screenboard** for a status display.
Pick the **widget** that fits — timeseries for trends, query value for SLIs, top list for "which host is
worst," heat map for distributions. Add **template variables** (`$env`, `$service`) so one dashboard
serves many scopes. Keep dashboards focused; link to detail rather than cramming.

## Implementation and Automation

The labs create a dashboard with a widget via the API, add a template variable, and reason about widget
choice — the visualization the Fundamentals exam validates.

## Validation and Troubleshooting

Confirm dashboards:

```text
Timeboard: shared time range across all graphs (troubleshooting/correlation)
Screenboard: free-form layout (status/NOC display)
Widgets: timeseries | query value | top list | heat map | distribution | table
Template variables ($env/$service/$host, bound to tags) re-scope every widget at once
```

Common pitfalls: a **screenboard** where widgets should share a time range (use a **timeboard**); and a
static dashboard duplicated per environment instead of using **template variables**.

## Security and Best Practices

Share dashboards (read-only) rather than raw API keys, and scope app keys least-privilege. Visualization
is authorized use of your own telemetry. All work is authorized.

## Hands-On Lab

Dashboard walkthroughs. **Shared prerequisites** — a Datadog account with an API/app key and `curl`;
`python3`. **Cost:** none.

### Lab 4.1 — Create a timeboard with a timeseries widget

**Objective:** Graph a metric on a dashboard.

```bash
curl -s -X POST "https://api.datadoghq.com/api/v1/dashboard" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -H "Content-Type: application/json" -d '{
    "title": "Web CPU", "layout_type": "ordered",
    "widgets": [ { "definition": {
      "type": "timeseries", "title": "CPU by host",
      "requests": [ { "q": "avg:system.cpu.user{env:prod} by {host}" } ] } } ] }' \
  | python3 -c 'import sys,json;print("dashboard id:",json.load(sys.stdin)["id"])'
```

```text
dashboard id: abc-def-ghi
```

**Expected result:** a timeboard created with a timeseries widget graphing CPU by host.

**Negative test:** build a screenboard for incident correlation; a **timeboard** shares the time range —
use it for troubleshooting.

**Cleanup:**

```bash
curl -s -X DELETE "https://api.datadoghq.com/api/v1/dashboard/abc-def-ghi" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}"
```

### Lab 4.2 — Add a template variable

**Objective:** Make the dashboard dynamic.

```json
{ "template_variables": [
    { "name": "env", "prefix": "env", "default": "prod" },
    { "name": "service", "prefix": "service", "default": "*" } ],
  "widgets": [ { "definition": {
    "type": "timeseries",
    "requests": [ { "q": "avg:system.cpu.user{$env,$service} by {host}" } ] } } ] }
```

**Expected result:** dropdowns for `env` and `service` that re-scope every widget — one dashboard, many
scopes.

**Negative test:** clone the dashboard for prod and staging; use a **`$env` template variable** instead.

**Cleanup:** none.

### Lab 4.3 — Choose the right widget

**Objective:** Match visualization to intent.

```python
python3 - <<'PY'
intents = {
  "trend over time":        "timeseries",
  "single current value / SLI": "query value",
  "which hosts are worst":  "top list",
  "latency distribution across hosts": "heat map / distribution",
  "tabular breakdown":      "table",
}
for intent, widget in intents.items(): print(f"{intent:34}: {widget}")
PY
```

**Expected result:** each analytical intent matched to the right widget.

**Negative test:** show a ranking as a timeseries with 50 lines; use a **top list** for "which is worst."

**Cleanup:** none.

### Lab 4.4 — Reason about screenboard vs timeboard

**Objective:** Pick the dashboard style.

```python
python3 - <<'PY'
cases = {
  "incident troubleshooting": "timeboard (shared time range correlates metrics)",
  "NOC status wall":          "screenboard (free-form, mixed widgets/images/text)",
}
for case, choice in cases.items(): print(f"{case:26}: {choice}")
PY
```

**Expected result:** timeboard for troubleshooting, screenboard for status — the right style per use.

**Negative test:** use a free-form screenboard to correlate a spike across metrics; a **timeboard**
synchronizes time.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog dashboards are timeboards (shared time range, for troubleshooting) and screenboards (free-form,
for status), built from widgets (timeseries, query value, top list, heat map, table) chosen to fit the
data, and made reusable with template variables that re-scope every widget by tag.

- [ ] I can distinguish timeboards from screenboards.
- [ ] I can build a dashboard with a widget.
- [ ] I can add a template variable.
- [ ] I can choose the right visualization.
- [ ] I completed Labs 4.1–4.4 including each negative test.
