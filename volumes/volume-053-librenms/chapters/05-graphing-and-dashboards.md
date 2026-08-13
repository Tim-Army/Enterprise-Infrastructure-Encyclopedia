# Chapter 05: Graphing and Dashboards

## Learning Objectives

- Retrieve device and port graphs from the API.
- Understand RRDtool graphing and time ranges.
- Build a custom dashboard with widgets.
- Share and scope dashboards.
- Complete a walkthrough for each visualization feature.

## Theory and Architecture

LibreNMS renders **graphs** from RRD data — per device, port, sensor, or application —
over selectable **time ranges** (day/week/month/year). The API exposes graphs as PNG or
data. **Dashboards** compose **widgets** (graphs, device availability, alerts, maps,
top-N) into a single operational view, which can be set as default or shared. For richer
visualization many operators pair LibreNMS with Grafana (Chapter 07).

## Design Considerations

Build **role-focused dashboards** (NOC overview, capacity, a customer view) rather than
one giant page. Use **top-N** and **availability** widgets for at-a-glance health, and
graph the **time range** that matches the question (day for incidents, year for
capacity).

## Implementation and Automation

The labs use the API to fetch a graph, build a dashboard, and add widgets.

## Validation and Troubleshooting

Confirm the model:

```text
Graphs: RRD-rendered per device/port/sensor/app, selectable time range, PNG or data via API.
Dashboards: composed of widgets (graph, availability, alerts, top-N, map).
```

Common pitfalls: one overloaded dashboard; and reading a **day** graph for a capacity
question (use a longer range).

## Security and Best Practices

Compose **focused** dashboards, use the right **time range** per question, scope shared
dashboards to the right audience, and offload heavy visualization to **Grafana** where
needed. Keep the default dashboard lightweight.

## Hands-On Lab

Visualization walkthroughs. **Shared prerequisites** — a running LibreNMS with a polled
device; `$LNMS`/`$TOKEN`. **Cost:** none.

### Lab 5.1 — Fetch a device graph

**Objective:** Retrieve a graph via the API.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" \
  "$LNMS/api/v0/devices/127.0.0.1/graphs" \
  | python3 -c "import sys,json;print('graph types:',[g['name'] for g in json.load(sys.stdin)['graphs']][:6])"
```

**Expected result:** the list of available **graph types** for the device — the graphing
surface.

**Negative test:** expect graphs before the first poll; graphs need **RRD data** — poll
first.

**Rollback:** none (read-only).

### Lab 5.2 — Fetch a port graph as PNG

**Objective:** Render a port traffic graph.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" \
  "$LNMS/api/v0/devices/127.0.0.1/ports/eth0?columns=ifName,ifInOctets_rate,ifOutOctets_rate" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['port'][0])"
```

**Expected result:** the port's **in/out rate** columns — the data behind a traffic
graph.

**Negative test:** eyeball raw counters; use **rates** (`_rate`) — counters wrap and are
not directly meaningful.

**Rollback:** none (read-only).

### Lab 5.3 — Create a dashboard

**Objective:** Create a named dashboard.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -X POST "$LNMS/api/v0/dashboards" -d '{"dashboard_name":"NOC Overview"}' \
  | python3 -c "import sys,json;print('dashboard id:',json.load(sys.stdin).get('dashboard_id'))"
```

**Expected result:** a new **"NOC Overview"** dashboard — a container for widgets.

**Negative test:** pile everything on the default dashboard; build a **focused** one
per role.

**Rollback:** delete the dashboard.

### Lab 5.4 — Add a widget

**Objective:** Describe adding a widget to the dashboard.

```text
# Dashboard > Edit > Add Widget: choose 'Alerts' or 'Availability map' or 'Graph'.
# Widgets bind to a device/group/graph and refresh on an interval.
"widget 'Availability map' added to NOC Overview"
```

**Expected result:** a widget bound to data on the dashboard — the composed operational
view.

**Negative test:** screenshot graphs into a doc; a **live widget** stays current — use
the dashboard.

**Rollback:** remove the widget.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Visualization is RRD-rendered graphs over selectable time ranges and dashboards composed
of focused widgets. This chapter fetched device/port graphs and built a dashboard.

- [ ] I can list a device's available graphs.
- [ ] I can read port traffic as rates.
- [ ] I can create a focused dashboard.
- [ ] I can add widgets bound to data.
- [ ] I completed Labs 5.1–5.4 including each negative test.
