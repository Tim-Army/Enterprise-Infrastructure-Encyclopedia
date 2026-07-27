# Chapter 03: Polling and Data Collection

## Learning Objectives

- Explain the poller and its schedule.
- Understand RRD time-series storage and rrdcached.
- Run and debug a poll for a device.
- Collect availability with ping and application metrics.
- Complete a walkthrough for each collection mechanism.

## Theory and Architecture

The **poller** collects metrics from each device on a schedule (default every 5
minutes) via SNMP, storing time-series in **RRDtool** files (fixed-size, self-rolling
databases) fronted by **rrdcached** to batch writes. Availability comes from **ICMP
ping**; deeper metrics come from **applications** (agent scripts for services like
Apache, MySQL) and SNMP modules. The **dispatcher** service schedules discovery and
polling across workers.

## Design Considerations

Keep the poll cycle **under the interval** — if polling a device takes longer than 5
minutes, you get gaps; scale pollers (Chapter 08). Use **rrdcached** to reduce disk I/O.
Enable only the **modules** you need to keep polls fast.

## Implementation and Automation

The labs use `lnms device:poll`, RRD inspection, and ping to observe collection.

## Validation and Troubleshooting

Confirm the mechanics:

```text
Poller: SNMP collect every ~5 min -> RRD (via rrdcached).
Ping: ICMP availability + latency. Applications: agent/script metrics.
Dispatcher schedules discovery + polling across workers.
```

Common pitfalls: a poll that **overruns** the interval (data gaps); and rrdcached not
running (write storms).

## Security and Best Practices

Watch **poll duration** (keep under interval), run **rrdcached**, disable unused
**modules**, and monitor the poller itself. Investigate gaps promptly — they mean the
collection pipeline is behind.

## Hands-On Lab

Collection walkthroughs. **Shared prerequisites** — a running LibreNMS with a device
added. **Cost:** none.

### Lab 3.1 — Poll a device with debug

**Objective:** Run a single poll and read timing.

```bash
docker compose exec librenms lnms device:poll 127.0.0.1 -vv 2>&1 | tail -20
```

**Expected result:** module-by-module poll output ending with a **runtime** — the poll
cycle and its duration.

**Negative test:** ignore poll runtime; if it **exceeds the interval** you get gaps —
watch the timing.

**Cleanup:** none.

### Lab 3.2 — Inspect an RRD file

**Objective:** Confirm time-series are being written.

```bash
docker compose exec librenms sh -c \
  'ls -1 rrd/*/ 2>/dev/null | head; rrdtool info rrd/*/port-id*.rrd 2>/dev/null | grep -m1 last_update'
```

**Expected result:** RRD files with a recent **last_update** — proof metrics are
persisting.

**Negative test:** assume data is stored; **check `last_update`** — a stale timestamp
means polling stopped.

**Cleanup:** none (read-only).

### Lab 3.3 — Check availability (ping)

**Objective:** Read the device's reachability/latency.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" "$LNMS/api/v0/devices/127.0.0.1" \
  | python3 -c "import sys,json;d=json.load(sys.stdin)['devices'][0];print('status:',d['status'],'last_ping:',d.get('last_ping'))"
```

**Expected result:** the device **status** (up/down) and last ping — ICMP availability.

**Negative test:** rely only on SNMP polls for up/down; **ping** detects reachability
even when SNMP is degraded.

**Cleanup:** none (read-only).

### Lab 3.4 — Enable an application metric

**Objective:** Describe collecting an application metric.

```text
# Applications extend polling with agent scripts (e.g., 'os', 'mysql', 'nginx').
# Deploy the agent/snmp-extend script on the device, then enable the app in LibreNMS.
"application 'mysql' enabled -> LibreNMS graphs query/connection metrics"
```

**Expected result:** an application feeding service-level metrics beyond base SNMP — the
applications mechanism.

**Negative test:** expect app metrics with no agent/extend script; **deploy the script**
on the device first.

**Cleanup:** disable the application if it was for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Collection is the poller pulling SNMP into RRD (via rrdcached) on a schedule,
availability from ICMP ping, and deeper metrics from applications — all scheduled by the
dispatcher. This chapter polled a device, inspected RRD, and checked availability.

- [ ] I can run and time a device poll.
- [ ] I can confirm RRD writes via last_update.
- [ ] I can read ping-based availability.
- [ ] I can describe application metric collection.
- [ ] I completed Labs 3.1–3.4 including each negative test.
