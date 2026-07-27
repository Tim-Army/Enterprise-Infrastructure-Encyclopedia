# Chapter 05: Enterprise Architect and Core Consultant

## Learning Objectives

- Explain the Architect and Consultant credentials and their scope.
- Describe distributed Splunk architecture: indexer and search-head clustering.
- Apply sizing, capacity planning, and deployment design.
- Troubleshoot distributed deployments.
- Complete a per-topic walkthrough for each Architect topic area.

## Theory and Architecture

The **Enterprise Certified Architect** validates the ability to **design and
manage distributed Splunk deployments** — planning, sizing, indexer and
search-head **clustering**, and troubleshooting at scale. The **Core Certified
Consultant** goes further into **large-scale, multi-tier** implementations and is
the expert-level design credential. Both build on the Admin foundation.

Key architectural components:

- **Indexer cluster** — replicated indexers (replication and search factors) for
  data availability and search.
- **Search head cluster** — coordinated search heads (a captain) sharing knowledge
  objects and search load.
- **Deployment server / management** components for forwarders and apps.
- **Monitoring Console** for health, and **capacity/sizing** models for scale.

## Design Considerations

Architecture is about **scale, availability, and performance**. Size indexers by
ingest volume and search concurrency; set **replication factor (RF)** and **search
factor (SF)** for the availability you need; cluster search heads for HA and shared
knowledge objects; and design data tiering (hot/warm/cold, SmartStore) for cost.
The **Consultant** applies this to complex, multi-site, multi-tier environments.

## Implementation and Automation

The labs below model the architect's decisions — sizing, RF/SF, clustering, and
troubleshooting — as calculations and configuration you can reason about without a
full cluster.

## Validation and Troubleshooting

Confirm the credentials before studying:

```text
splunk.com > Enterprise Certified Architect / Core Certified Consultant:
  - Architect: distributed design, sizing, indexer/SH clustering, troubleshooting
  - Consultant: large-scale, multi-tier implementations (expert)
  - prerequisite: Admin foundation
```

Common pitfalls: setting **RF/SF** without capacity for the extra copies;
under-sizing indexers for search concurrency; and treating a single search head as
HA (use a **cluster**).

## Security and Best Practices

Design for the **required availability** (RF/SF sized to failure tolerance and
capacity), separate roles (indexers, search heads, cluster manager), use the
**Monitoring Console** for health, and plan **data tiering/SmartStore** for cost
at scale. Document the architecture and capacity model.

## References and Knowledge Checks

- splunk.com: *Architect* and *Consultant* tracks; Distributed Deployment and Indexer/Search Head Clustering manuals; Capacity Planning Manual.

**Knowledge checks**

1. What do replication factor and search factor control?
2. Why cluster search heads rather than run a single one?
3. How does indexer sizing depend on ingest and search concurrency?

## Hands-On Lab

Per-topic walkthroughs — **one lab per Architect topic area**. Calculations and
config you can reason about.

**Shared prerequisites** — a shell with `python3`; optionally a Splunk instance.
**Cost:** none.

### Lab 5.1 — Deployment planning and sizing

**Objective:** Size indexers from ingest volume.

```bash
python3 - <<'PY'
daily_gb = 500                     # daily ingest
per_indexer_gb = 100               # rule-of-thumb indexing capacity/indexer/day
indexers = -(-daily_gb // per_indexer_gb)   # ceil
print(f"Ingest {daily_gb} GB/day at ~{per_indexer_gb} GB/indexer -> >= {indexers} indexers (before search load).")
PY
```

**Expected result:** a minimum indexer count from ingest — the sizing calculation
the Architect performs (add for search concurrency and replication).

**Negative test:** size by storage alone; **search concurrency** and replication
also drive indexer count — account for both.

**Cleanup:** none.

### Lab 5.2 — Indexer clustering (RF/SF)

**Objective:** Reason about replication and search factors.

```bash
python3 - <<'PY'
RF, SF, nodes = 3, 2, 5
print(f"RF={RF}: {RF} copies of each bucket -> tolerate {RF-1} indexer failures for data.")
print(f"SF={SF}: {SF} searchable copies -> tolerate {SF-1} failures for search.")
print(f"Requires >= RF nodes ({nodes} nodes OK) and ~{RF}x raw storage.")
PY
```

**Expected result:** how RF/SF map to failure tolerance and storage cost — the
clustering design of the Architect exam.

**Negative test:** set RF=3 on 2 nodes; RF requires at least RF peer nodes — size
the cluster to the factor.

**Cleanup:** none.

### Lab 5.3 — Search head clustering

**Objective:** Describe the search-head cluster model.

```bash
python3 - <<'PY'
print("SH cluster: 3+ members elect a CAPTAIN; replicate knowledge objects; share scheduling.")
print("Benefits: HA of the search tier + consistent knowledge objects across members.")
PY
```

**Expected result:** the SH-cluster model (captain, KO replication, HA) — a core
Architect topic.

**Negative test:** run one search head and call it HA; a **cluster** provides
resilience and shared knowledge — cluster for production.

**Cleanup:** none.

### Lab 5.4 — Data tiering and SmartStore

**Objective:** Plan cost-effective data tiers.

```bash
python3 - <<'PY'
tiers = {"hot/warm":"fast local storage, recent data",
         "cold":"cheaper storage, older data",
         "SmartStore":"object storage (S3) backing with local cache -> decouple compute/storage"}
for t,d in tiers.items(): print(f"{t:11}: {d}")
PY
```

**Expected result:** the storage-tier model including SmartStore — capacity/cost
design for scale.

**Negative test:** keep all data on hot storage; **tiering/SmartStore** controls
cost at scale — design tiers to retention and access patterns.

**Cleanup:** none.

### Lab 5.5 — Monitoring and troubleshooting

**Objective:** Use the Monitoring Console signals to troubleshoot.

```bash
python3 - <<'PY'
signals = ["Indexing latency / queue fill -> ingest bottleneck",
           "Search concurrency at limit -> add SH capacity or tune searches",
           "Skipped searches -> scheduler contention",
           "Cluster fixup tasks -> bucket replication catching up"]
for s in signals: print("-", s)
PY
```

**Expected result:** health signals mapped to causes — the distributed
troubleshooting an Architect performs (via the Monitoring Console).

**Negative test:** troubleshoot from one node's logs; use the **Monitoring
Console** for the whole-deployment view.

**Cleanup:** none.

### Lab 5.6 — Consultant: multi-tier / multi-site design

**Objective:** Reason about a multi-site cluster.

```bash
python3 - <<'PY'
print("Multi-site indexer cluster: site-aware RF/SF (e.g., origin:2,total:3) for DR across sites.")
print("Consultant scope: multi-tier (forwarding tiers, intermediate forwarders), capacity per site.")
PY
```

**Expected result:** multi-site RF/SF and multi-tier forwarding — the large-scale
design the Consultant certifies.

**Negative test:** use single-site RF for a DR requirement; **site-aware** RF/SF
ensures copies survive a site loss.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Enterprise Architect certifies distributed Splunk design — sizing, indexer and
search-head clustering, data tiering, and troubleshooting — and the Core Consultant
extends this to large-scale, multi-tier, multi-site implementations. Both build on
the Admin foundation and center on scale, availability, and performance.

- [ ] I can size indexers and set RF/SF for availability.
- [ ] I can describe search-head clustering and data tiering.
- [ ] I can troubleshoot with Monitoring Console signals.
- [ ] I can reason about multi-site/multi-tier design.
- [ ] I completed Labs 5.1–5.6 including each negative test.
