# Chapter 08: Operating Clusters and Confluent Cloud

## Learning Objectives

- Size clusters from retention, throughput, and replication.
- Monitor the metrics that predict trouble, not just the ones that report it.
- Secure a cluster with authentication, ACLs, and encryption.
- Explain Confluent Cloud features examined on CCAC: Cluster Linking, multi-cloud, and managed operations.

## The administrator's job

This chapter carries the **CCAAK** (administrator) and **CCAC** (cloud operator) material. Where the earlier chapters built applications, this one keeps the platform alive: capacity, monitoring, security, and — for the cloud exam — the features that span regions and providers.

## Sizing

Storage is arithmetic, and the replication multiplier is the part people forget:

**Storage = ingest rate × retention period × replication factor**

A topic taking 100 MB/s with 7-day retention and RF 3 needs roughly 100 × 86,400 × 7 × 3 ≈ **181 TB**. The replication factor multiplies everything, so a decision made for durability directly triples the storage bill.

Other sizing levers: partition count (Chapter 02), broker count (must exceed replication factor), and network throughput — replication traffic is roughly (RF − 1) × ingest, so a 3× replicated cluster pushes twice the ingest volume between brokers before any consumer reads it.

## Monitoring

| Metric | Why it matters |
|:---|:---|
| **Under-replicated partitions** | The canonical health signal — replicas falling behind; **should be 0** |
| **Offline partitions** | Partitions with no leader — data unavailable *now* |
| **ISR shrink/expand rate** | Churn indicates broker or network instability |
| **Consumer lag** | Consumers falling behind (Chapter 04) |
| **Request latency (p99)** | Producer/consumer experience |
| **Disk usage and growth** | Retention exhausting storage |
| **Active controller count** | Must be exactly **1** across the cluster |

Under-replicated partitions is the single metric to alert on first: it is often the earliest visible symptom of a broker, disk, or network problem, and it directly threatens the durability guarantee of Chapter 03.

## Security

| Layer | Mechanism |
|:---|:---|
| **Encryption in transit** | TLS between clients and brokers, and between brokers |
| **Authentication** | SASL (SCRAM, GSSAPI/Kerberos, OAUTHBEARER), or mTLS |
| **Authorization** | **ACLs** on resources (topic, group, cluster, transactional ID) |
| **Encryption at rest** | Disk/volume encryption or cloud-provider keys |

ACLs are `principal → operation → resource`, and they are deny-by-default once an authorizer is configured. The frequent operational surprise: a consumer needs `READ` on the **topic** *and* `READ` on its **consumer group** — granting only the topic produces a puzzling authorization failure.

## Confluent Cloud (CCAC)

The cloud exam concentrates on capabilities that are hard to build yourself:

- **Cluster Linking** — replicate topics between clusters (across regions or cloud providers) with offsets preserved, so consumers can fail over without losing position.
- **Multi-cloud and global architectures** — clusters across AWS, Azure, and Google Cloud under one control plane.
- **Stream Governance** — registry, catalog, lineage (Chapter 05).
- **Fully managed connectors** — Connect (Chapter 06) without operating workers.
- **Managed stream processing** — including Flink (Chapter 07).

The trade is the familiar managed-service one: you stop tuning brokers and JVMs, and you gain scaling, patching, and cross-region replication as configuration rather than projects.

## Hands-On Lab

Python models cluster operations. **Cost:** none.

### Lab 8.1 — Size a cluster and see the replication multiplier

**Objective:** Compute storage and network from first principles.

```bash
python3 - <<'EOF'
def size(name, ingest_mb_s, retention_days, rf, broker_disk_tb):
    raw_tb  = ingest_mb_s * 86400 * retention_days / 1_000_000
    tot_tb  = raw_tb * rf
    brokers = max(rf, -(-int(tot_tb) // int(broker_disk_tb)))
    repl_mb = ingest_mb_s * (rf - 1)
    print(f"\n{name}: {ingest_mb_s} MB/s, {retention_days}d retention, RF={rf}")
    print(f"   raw data            {raw_tb:8.1f} TB")
    print(f"   with replication    {tot_tb:8.1f} TB   (x{rf})")
    print(f"   brokers @ {broker_disk_tb} TB disk  {brokers:5d}")
    print(f"   inter-broker replication traffic: {repl_mb:.0f} MB/s ({rf-1}x ingest) before any consumer reads")

size("events",   100, 7,  3, 10)
size("audit",     20, 90, 3, 10)
size("metrics",  500, 1,  2, 10)
print("\nRetention and replication factor dominate cost. Cutting 'events' retention from 7d to 3d")
print("saves ~104 TB; dropping RF from 3 to 2 saves ~60 TB but weakens durability (ch02).")
EOF
```

**Expected result:** The events topic needs ~181 TB replicated and pushes 200 MB/s of inter-broker traffic; the 90-day audit topic needs ~466 TB despite modest ingest. The closing lines quantify the two levers — retention and replication factor — and make explicit that the second one trades storage against the durability guarantee, so it is not a free saving.

**Negative test:** Sizing on raw ingest without the replication multiplier — you provision a third of the storage you need, and the cluster fills silently until retention starts deleting data early.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Alert on the metrics that predict trouble

**Objective:** Triage cluster health signals by urgency.

```bash
python3 - <<'EOF'
def assess(m):
    findings = []
    if m["offline_partitions"] > 0:
        findings.append(("CRITICAL", f"{m['offline_partitions']} OFFLINE partition(s) — no leader, data unavailable NOW"))
    if m["under_replicated"] > 0:
        findings.append(("CRITICAL", f"{m['under_replicated']} under-replicated — durability guarantee is degraded"))
    if m["active_controllers"] != 1:
        findings.append(("CRITICAL", f"active controller count = {m['active_controllers']} (must be exactly 1)"))
    if m["isr_shrinks_per_min"] > 5:
        findings.append(("WARNING", f"ISR churn {m['isr_shrinks_per_min']}/min — broker or network instability"))
    if m["disk_pct"] > 80:
        findings.append(("WARNING", f"disk {m['disk_pct']}% — reduce retention or add brokers before it fills"))
    if m["p99_ms"] > 500:
        findings.append(("WARNING", f"p99 request latency {m['p99_ms']} ms — clients feel this"))
    return findings or [("OK", "healthy")]

clusters = {
 "prod-a": {"offline_partitions":0,"under_replicated":0,"active_controllers":1,"isr_shrinks_per_min":0,"disk_pct":55,"p99_ms":40},
 "prod-b": {"offline_partitions":0,"under_replicated":12,"active_controllers":1,"isr_shrinks_per_min":9,"disk_pct":88,"p99_ms":650},
 "prod-c": {"offline_partitions":3,"under_replicated":30,"active_controllers":2,"isr_shrinks_per_min":20,"disk_pct":92,"p99_ms":2000},
}
for name, m in clusters.items():
    print(f"\n{name}:")
    for sev, msg in assess(m):
        print(f"   [{sev:8}] {msg}")
print("\nUnder-replicated partitions is the metric to alert on FIRST: it is usually the earliest")
print("visible symptom of a broker/disk/network fault and directly threatens durability.")
EOF
```

**Expected result:** `prod-a` is healthy, `prod-b` shows a degrading cluster (under-replicated partitions, ISR churn, disk pressure, high latency), and `prod-c` is in outage with offline partitions and **two active controllers** — a split-brain condition. Ordering by urgency matters: offline partitions mean unavailability *now*, while under-replication means the safety margin is gone and the next failure causes loss.

**Negative test:** Monitoring only disk and CPU — under-replicated partitions can sit above zero for days on a cluster that looks resource-comfortable, silently running without the redundancy you believe you have.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — ACLs and the consumer-group permission trap

**Objective:** Evaluate authorization the way the broker does.

```bash
python3 - <<'EOF'
acls = [
  {"principal":"User:app-producer","operation":"WRITE","resource_type":"topic","resource":"orders"},
  {"principal":"User:app-consumer","operation":"READ", "resource_type":"topic","resource":"orders"},
  {"principal":"User:app-consumer","operation":"READ", "resource_type":"group","resource":"order-processors"},
  {"principal":"User:audit","operation":"READ","resource_type":"topic","resource":"orders"},
]
def allowed(principal, op, rtype, resource):
    return any(a["principal"]==principal and a["operation"]==op and
               a["resource_type"]==rtype and a["resource"]==resource for a in acls)

def can_consume(principal, topic, group):
    t = allowed(principal,"READ","topic",topic)
    g = allowed(principal,"READ","group",group)
    if t and g: return f"ALLOWED — READ on topic '{topic}' and group '{group}'"
    missing = []
    if not t: missing.append(f"READ on topic '{topic}'")
    if not g: missing.append(f"READ on GROUP '{group}'  <-- the commonly missed one")
    return "DENIED — missing " + " and ".join(missing)

print("produce:", "ALLOWED" if allowed("User:app-producer","WRITE","topic","orders") else "DENIED")
print("consume (app-consumer):", can_consume("User:app-consumer","orders","order-processors"))
print("consume (audit):       ", can_consume("User:audit","orders","audit-readers"))
print("\nConsuming needs BOTH topic READ and consumer-group READ. Granting only the topic")
print("produces a GroupAuthorizationException that looks like a topic problem but is not.")
EOF
```

**Expected result:** The producer and the fully-provisioned consumer are allowed, while `audit` is **denied for the group** despite holding topic access — the single most common Kafka ACL mistake. The error it produces names the group, but people debug the topic permission because that is what they were thinking about. Modeling the two-part check makes the failure obvious.

**Negative test:** Granting wildcard ACLs to resolve the confusion quickly — the immediate problem disappears and every principal gains cluster-wide access, which is exactly what the authorizer exists to prevent.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Clusters sized with the replication multiplier for both storage and inter-broker traffic.
- [ ] Health metrics triaged, with under-replicated partitions as the first alert.
- [ ] Security layered: TLS, SASL/mTLS authentication, ACL authorization, encryption at rest.
- [ ] The consumer-group ACL requirement understood alongside topic permissions.
- [ ] Confluent Cloud capabilities placed: Cluster Linking, multi-cloud, governance, managed connectors and Flink.
