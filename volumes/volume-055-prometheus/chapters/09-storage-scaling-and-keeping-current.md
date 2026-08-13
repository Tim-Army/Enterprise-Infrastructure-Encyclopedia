# Chapter 09: Storage, Scaling, and Keeping Current

## Learning Objectives

- Explain the local TSDB and retention.
- Scale with remote write, federation, and the ecosystem.
- Back up TSDB data with snapshots.
- Track releases and the ecosystem.
- Complete a walkthrough for each operational concern.

## Theory and Architecture

Prometheus stores samples in a **local TSDB** organized into 2-hour **blocks** compacted
over time, with a **retention** window (default 15 days). For **long-term** and **global**
views, Prometheus **remote-writes** to systems like **Thanos**, **Mimir**, or **Cortex**,
which provide durable storage, downsampling, and cross-cluster querying; **federation**
lets one Prometheus scrape aggregates from others. The **admin API** can take a **TSDB
snapshot** for backup. Prometheus ships on a fast release cadence — the current series is
**3.x (v3.13.x)** — and is queried directly or via **Grafana**.

## Design Considerations

Set **retention** to your local needs and offload long-term storage via **remote write**
to Thanos/Mimir. Use **federation** for aggregation, not for pulling raw series at scale.
**Snapshot** before risky operations. Visualize with **Grafana**.

## Implementation and Automation

The labs inspect TSDB/retention, snapshot, and check the release.

## Validation and Troubleshooting

Confirm the model:

```text
Local TSDB: 2h blocks + retention (default 15d). Remote write -> Thanos/Mimir/Cortex.
Federation: scrape aggregates from other Prometheis. Admin API: TSDB snapshot for backup.
Releases: github.com/prometheus/prometheus (3.x, v3.13.x).
```

Common pitfalls: relying on local TSDB for long-term retention; and federating raw
high-cardinality series (overload).

## Security and Best Practices

Right-size **retention**, offload long-term to **remote-write** backends, **federate
aggregates** only, **snapshot** before upgrades/migrations, secure the admin API, and
track releases. Keep Grafana datasources least-privilege.

## Hands-On Lab

Operations walkthroughs. **Shared prerequisites** — a running Prometheus (with
`--web.enable-admin-api` for snapshots); `curl`, `python3`. **Cost:** none.

### Lab 9.1 — Inspect TSDB stats

**Objective:** Read TSDB head stats.

```bash
curl -sS "http://localhost:9090/api/v1/status/tsdb" \
  | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print('series:',d['headStats']['numSeries'])"
```

**Expected result:** the head **series count** — the TSDB's current working set.

**Negative test:** ignore series growth; a climbing **series count** signals cardinality
issues — watch it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Take a TSDB snapshot

**Objective:** Create a backup snapshot.

```bash
curl -sS -X POST "http://localhost:9090/api/v1/admin/tsdb/snapshot" \
  | python3 -c "import sys,json;print('snapshot:',json.load(sys.stdin)['data']['name'])"
```

**Expected result:** a **snapshot name** under `data/snapshots/` — a consistent backup.

**Negative test:** copy the live `data/` dir while running; take an **atomic snapshot**
via the admin API instead.

**Rollback:** remove the snapshot directory when done.

### Lab 9.3 — Describe remote write

**Objective:** Configure long-term storage offload.

```yaml
remote_write:
  - url: "http://mimir:9009/api/v1/push"
# Prometheus stays the scraper/ruler; durable + global storage lives in Mimir/Thanos.
```

**Expected result:** samples **remote-written** to a long-term backend — durable, global
storage beyond local retention.

**Negative test:** raise local retention to years; the **local TSDB isn't built for
that** — remote-write to a purpose-built backend.

**Rollback:** remove the remote_write block.

### Lab 9.4 — Check the current release

**Objective:** Read the latest Prometheus release.

```bash
curl -sS "https://api.github.com/repos/prometheus/prometheus/releases/latest" \
  | python3 -c "import sys,json;print('latest:',json.load(sys.stdin)['tag_name'])"
```

**Expected result:** the latest tag (a **v3.13.x** release) — what to track for upgrades.

**Negative test:** run a long-unsupported release; track **releases** and stay current.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Prometheus stores samples in a local TSDB with a retention window, offloads long-term/
global storage via remote write to Thanos/Mimir, federates aggregates, snapshots for
backup, and ships on a fast 3.x cadence visualized in Grafana. This chapter inspected the
TSDB, snapshotted, and checked the release.

- [ ] I can explain the local TSDB and retention.
- [ ] I can take a TSDB snapshot for backup.
- [ ] I can describe remote write for long-term storage.
- [ ] I can find the current release to plan upgrades.
- [ ] I completed Labs 9.1–9.4 including each negative test.
