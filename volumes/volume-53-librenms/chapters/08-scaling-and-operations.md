# Chapter 08: Scaling and Operations

## Learning Objectives

- Explain distributed polling and when it is needed.
- Use rrdcached and a shared cache to scale I/O.
- Measure and tune poller performance.
- Operate the dispatcher service.
- Complete a walkthrough for each scaling mechanism.

## Theory and Architecture

A single LibreNMS node polls thousands of devices, but at larger scale you use
**distributed polling**: multiple **poller nodes** share the workload, coordinated
through **Redis** (locking/queues) against one database. **rrdcached** batches RRD
writes to cut disk I/O; **Redis/Memcached** caches shared state across pollers. The
**dispatcher** (Python service) schedules discovery and polling. The key metric is that
each device polls **within its interval** — when it doesn't, add poller capacity.

## Design Considerations

Scale out when **poll duration approaches the interval** or the node is CPU/I/O bound.
Add **poller nodes** behind Redis, front RRD with **rrdcached**, and shard by device
group if needed. Monitor the pollers themselves.

## Implementation and Automation

The labs inspect poller performance, rrdcached, and the dispatcher, and describe adding
a poller.

## Validation and Troubleshooting

Confirm the mechanics:

```text
Distributed polling: N poller nodes + Redis coordination + one DB.
rrdcached: batch RRD writes. Redis/Memcached: shared cache/locks.
Dispatcher: schedules discovery + polling. Goal: poll each device < interval.
```

Common pitfalls: poll time exceeding the interval (gaps); and no **rrdcached** (I/O
bottleneck).

## Security and Best Practices

Watch **poll performance** and add poller nodes before gaps appear, run **rrdcached**
and a shared cache, secure the **Redis** coordination channel, and monitor the
pollers/dispatcher as first-class services.

## Hands-On Lab

Scaling walkthroughs. **Shared prerequisites** — a running LibreNMS with devices.
**Cost:** none.

### Lab 8.1 — Measure poller performance

**Objective:** Read per-device poll durations.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" "$LNMS/api/v0/devices" \
  | python3 -c "import sys,json;[print(d['hostname'],'last_polled_timetaken:',d.get('last_polled_timetaken')) for d in json.load(sys.stdin)['devices'][:5]]"
```

**Expected result:** each device's **poll time** — the metric that governs scaling.

**Negative test:** ignore poll time until gaps appear; **watch `last_polled_timetaken`**
against the interval proactively.

**Cleanup:** none (read-only).

### Lab 8.2 — Confirm rrdcached

**Objective:** Verify RRD writes are batched.

```bash
docker compose exec librenms sh -c 'grep -i rrdcached config.php 2>/dev/null; pgrep -a rrdcached || echo "rrdcached not running"'
```

**Expected result:** **rrdcached** configured/running — batched RRD I/O.

**Negative test:** run at scale without rrdcached; direct RRD writes become an **I/O
bottleneck** — enable it.

**Cleanup:** none (read-only).

### Lab 8.3 — Inspect the dispatcher

**Objective:** Confirm the dispatcher is scheduling work.

```bash
docker compose exec librenms sh -c 'pgrep -a -f dispatcher || pgrep -a -f librenms-service'
```

**Expected result:** the **dispatcher/service** process running — discovery and polling
are scheduled.

**Negative test:** assume cron alone suffices at scale; the **dispatcher** distributes
work across pollers — run it.

**Cleanup:** none (read-only).

### Lab 8.4 — Add a poller node (describe)

**Objective:** Describe adding distributed polling.

```text
# On a new node: install LibreNMS, point at the SAME database + Redis,
#   set distributed_poller = true and a unique poller name; join the pool.
$config['distributed_poller'] = true;
$config['distributed_poller_name'] = 'poller2';
```

**Expected result:** a second **poller node** sharing the load via Redis — horizontal
scale.

**Negative test:** vertically scale one node forever; **distributed polling** scales
past a single host's limits.

**Cleanup:** none (describe-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

LibreNMS scales with distributed polling (poller nodes coordinated by Redis against one
DB), rrdcached for batched I/O, and a shared cache — keeping every device polling within
its interval. This chapter measured poll performance and reviewed the scaling
components.

- [ ] I can read per-device poll durations.
- [ ] I can confirm rrdcached is batching I/O.
- [ ] I can verify the dispatcher is scheduling.
- [ ] I can describe adding a distributed poller.
- [ ] I completed Labs 8.1–8.4 including each negative test.
