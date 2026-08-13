# Chapter 02: The Elastic Stack Architecture

## Learning Objectives

- Describe Elasticsearch node roles and cluster topology.
- Explain shards, replicas, and data tiers.
- Explain the roles of Kibana, Elastic Agent/Fleet, Beats, and Logstash.
- Read node and shard state.
- Complete a walkthrough for each architecture topic.

## Theory and Architecture

The **Elastic Stack** is a distributed system. **Elasticsearch** is the search and analytics engine: a
**cluster** of **nodes**, each with one or more **roles** (master, data, ingest, coordinating, machine
learning, transform). Data lives in **indices** split into **shards** (primary and **replica**) spread
across data nodes for scale and resilience; hot/warm/cold/frozen **data tiers** place shards on storage
matched to access frequency (with ILM moving them, Chapter 03). **Kibana** is the UI — Discover, Lens,
dashboards, Dev Tools, and the observability and security apps. Data reaches Elasticsearch through
**Elastic Agent** (a single agent managed centrally by **Fleet**, running **integrations**), the older
**Beats** shippers (Filebeat, Metricbeat, Heartbeat), and **Logstash** (a flexible ingest/transform
pipeline). Understanding which component does what — and how nodes, shards, and tiers fit together — is
the foundation every Elastic certification builds on. This chapter teaches the architecture with hands-on
Elasticsearch API walkthroughs.

## Design Considerations

Assign **node roles** deliberately (dedicated masters for stability at scale; data nodes sized for
shards). Keep **shards** reasonably sized (avoid tiny or giant shards) and use **replicas** for
resilience and read throughput. Use **data tiers** with ILM to cut cost. Prefer **Elastic Agent + Fleet**
for new deployments (central management) over standalone Beats. Use **Logstash** when you need heavy
transformation or buffering.

## Implementation and Automation

The labs read node roles, inspect shard allocation, and reason about the ingest components — the topology
the Engineer and Observability exams assume.

## Validation and Troubleshooting

Confirm the architecture:

```text
Elasticsearch: cluster -> nodes (roles: master/data/ingest/ml/coordinating) -> indices -> shards (primary/replica)
Data tiers: hot -> warm -> cold -> frozen (ILM moves shards by age/access)
Kibana: Discover / Lens / dashboards / Dev Tools / Observability / Security apps
Ingest: Elastic Agent + Fleet (integrations) | Beats (Filebeat/Metricbeat/Heartbeat) | Logstash
```

Common pitfalls: too many tiny **shards** (overhead) or a few huge ones (slow recovery); and mixing
standalone Beats with Fleet-managed Agents without a plan.

## Security and Best Practices

Enable cluster security and TLS, give nodes least-privilege roles, and manage agents centrally with
Fleet. A well-architected, secured cluster is the basis for everything else. All work is authorized.

## Hands-On Lab

Architecture walkthroughs. **Shared prerequisites** — an Elastic Stack cluster at
`https://localhost:9200`, `curl`, and `python3`. **Cost:** none.

### Lab 2.1 — Read node roles

**Objective:** See the cluster topology.

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/_cat/nodes?v&h=name,node.role,master"
```

```text
name node.role   master
es01 himrst       *
es02 himrst       -
es03 dilm         -
```

**Expected result:** nodes with their roles (`m`=master, `d`=data, `i`=ingest, `l`=ml, and so on) — the
cluster topology.

**Negative test:** run a single node with every role in production and wonder why it is unstable; use
**dedicated masters** and sized data nodes at scale.

**Rollback:** none (read-only).

### Lab 2.2 — Inspect shards and replicas

**Objective:** See how data is distributed.

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/_cat/shards/my-index?v&h=index,shard,prirep,state,node"
```

```text
index    shard prirep state   node
my-index 0     p      STARTED es01
my-index 0     r      STARTED es02
my-index 1     p      STARTED es02
my-index 1     r      STARTED es01
```

**Expected result:** primary (`p`) and replica (`r`) shards distributed across nodes — scale and
resilience.

**Negative test:** set `number_of_replicas: 0` on critical data; a node loss loses shards — keep at
least one replica.

**Rollback:** none (read-only).

### Lab 2.3 — Reason about the ingest components

**Objective:** Choose the right data path.

```python
python3 - <<'PY'
ingest = {
  "Elastic Agent + Fleet": "single agent, central mgmt, integrations — preferred for new deployments",
  "Beats (Filebeat/Metricbeat/Heartbeat)": "lightweight single-purpose shippers",
  "Logstash": "heavy transformation, buffering, many inputs/outputs",
}
for tool, use in ingest.items():
    print(f"{tool:40}: {use}")
print("Rule: new deployments -> Elastic Agent + Fleet; Logstash for heavy transform")
PY
```

**Expected result:** each ingest component matched to its use — a deliberate data path.

**Negative test:** deploy a dozen standalone Beats when Fleet-managed Agents would centralize
management; prefer **Elastic Agent + Fleet** for new work.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Read data-tier assignment

**Objective:** See tiering in action.

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/_cat/indices/my-index?v&h=index,pri,rep,docs.count,store.size"
curl -s -k -u elastic:$PW "https://localhost:9200/my-index/_settings/index.routing.allocation.include._tier_preference?pretty"
```

```json
{ "my-index": { "settings": { "index": { "routing": { "allocation": { "include": { "_tier_preference": "data_hot" } } } } } } }
```

**Expected result:** the index preferring the `data_hot` tier — the first stop before ILM moves it.

**Negative test:** keep all data on hot (SSD) tier forever; cost balloons — use **ILM** to move aging
data to warm/cold/frozen (Chapter 03).

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Elastic Stack is Elasticsearch (a cluster of role-assigned nodes holding indices split into
primary/replica shards across hot/warm/cold/frozen tiers), Kibana (the UI), and the ingest layer —
Elastic Agent with Fleet, Beats, and Logstash — the architecture every Elastic certification builds on.

- [ ] I can describe node roles and cluster topology.
- [ ] I can explain shards, replicas, and data tiers.
- [ ] I can explain Kibana, Elastic Agent/Fleet, Beats, and Logstash.
- [ ] I completed Labs 2.1–2.4 including each negative test.
