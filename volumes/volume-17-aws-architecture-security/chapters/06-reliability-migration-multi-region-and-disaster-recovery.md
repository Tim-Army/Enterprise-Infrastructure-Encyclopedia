# Chapter 06: Reliability, Migration, Multi-Region, and Disaster Recovery

## Learning Objectives

- Define Recovery Time Objective (RTO) and Recovery Point Objective (RPO)
  and use them to select among the four standard AWS disaster recovery
  strategies.
- Configure Amazon Route 53 health checks and failover routing to
  automate DR activation for a workload.
- Compare S3 Cross-Region Replication, Aurora Global Database, and
  DynamoDB Global Tables as multi-Region data replication mechanisms.
- Apply the AWS Cloud Adoption Framework's "7 Rs" to classify a migration
  approach for a given legacy workload.
- Use AWS Application Migration Service (MGN) and AWS Database Migration
  Service (DMS) to plan a lift-and-shift and a database migration,
  respectively.
- Use AWS Resilience Hub to assess a workload's resiliency posture against
  a stated RTO/RPO target.

## Theory and Architecture

The Well-Architected Framework's **Reliability** pillar centers on two
metrics that must be defined before any DR architecture is chosen:

- **Recovery Time Objective (RTO)** — the maximum acceptable time between
  a disaster and the workload being restored to service.
- **Recovery Point Objective (RPO)** — the maximum acceptable amount of
  data loss, measured as time since the last recoverable state.

These are business decisions, not technical ones — an architect's job is
to translate a stated RTO/RPO into an architecture that meets it at the
lowest justifiable cost, not to maximize resilience regardless of cost.

### The four DR strategies

| Strategy | RTO | RPO | Standing cost | Description |
| --- | --- | --- | --- | --- |
| Backup and restore | Hours | Hours | Lowest — storage only | Regular backups to a second Region; infrastructure provisioned only during a declared disaster |
| Pilot light | Tens of minutes | Minutes | Low — core data services running, compute idle | Minimal core infrastructure (typically a replicated database) always running in the DR Region; compute scaled up on failover |
| Warm standby | Minutes | Seconds to minutes | Moderate — a scaled-down full stack running | A fully functional but minimally scaled copy of the environment runs continuously in the DR Region, scaled up on failover |
| Multi-site active/active | Near zero | Near zero | Highest — full duplicate capacity | Both Regions actively serve production traffic simultaneously; failover is a traffic-routing change, not an infrastructure change |

Each strategy up this list reduces RTO/RPO at increasing standing cost.
**Backup and restore** is appropriate for workloads that can tolerate
extended downtime (internal tools, batch-processing systems). **Pilot
light** keeps the hardest-to-quickly-recreate component — usually a
database — continuously replicated while compute is provisioned only when
needed. **Warm standby** runs a right-sized (not full-scale) version of
the entire stack continuously, cutting failover time to the time needed to
scale it up and redirect traffic. **Multi-site active/active** eliminates
failover time entirely by having both Regions already serving live
traffic, at the cost of running (and keeping in sync) two full production
environments continuously.

### Multi-Region data replication mechanisms

| Service | Mechanism | Consistency model |
| --- | --- | --- |
| Amazon S3 Cross-Region Replication (CRR) | Asynchronous, per-object, rule-based | Eventually consistent; replication time typically under 15 minutes, monitorable via S3 Replication Time Control |
| Amazon Aurora Global Database | Dedicated, purpose-built replication infrastructure separate from storage replication | Asynchronous, typically sub-second lag; one primary Region for writes, up to five secondary read Regions |
| Amazon DynamoDB Global Tables | Multi-Region, multi-active | Eventually consistent, last-writer-wins conflict resolution; every participating Region accepts writes |
| Amazon RDS cross-Region read replica | Asynchronous, engine-native replication | Eventually consistent; promotable to a standalone primary during DR |

**Aurora Global Database** is purpose-built for low-lag cross-Region
replication of relational data, using dedicated replication infrastructure
rather than the general-purpose asynchronous replica mechanism RDS uses
for cross-Region read replicas — this typically yields sub-second
replication lag versus RDS cross-Region replicas' more variable lag.
**DynamoDB Global Tables** is the only mechanism in this table supporting
simultaneous multi-Region *writes*; the other three are single-writer
(with the write Region promotable during DR), which matters directly for
whether an active/active strategy is even achievable for a given data
layer.

### Route 53 health checks and failover routing

**Route 53 health checks** poll an endpoint (an HTTP(S) path, a TCP port,
or a CloudWatch alarm state) on a defined interval and mark it
healthy/unhealthy based on a threshold of consecutive check results.
**Failover routing policy** pairs a primary and secondary record; Route 53
returns the primary's answer while its health check passes and
automatically shifts to the secondary when the primary's health check
fails, without any manual DNS change. Because DNS resolvers and clients
cache responses according to the record's **TTL**, a lower TTL reduces
failover propagation delay at the cost of higher query volume against
Route 53 — an explicit trade-off to set deliberately for DR-critical
records, not left at a default value.

### Migration: the 7 Rs and migration tooling

The AWS Cloud Adoption Framework classifies migration approaches into
seven strategies, commonly called the "7 Rs":

1. **Retire** — decommission a workload with no ongoing value.
2. **Retain** — keep a workload on-premises for now (regulatory,
   dependency, or timing reasons).
3. **Relocate** — move a VMware-based workload to AWS with no
   modification, using VMware Cloud on AWS.
4. **Rehost** ("lift and shift") — move a workload to AWS with minimal
   change, typically using **AWS Application Migration Service (MGN)**,
   which performs continuous block-level replication from source servers
   and allows a low-downtime cutover.
5. **Replatform** ("lift, tinker, and shift") — make targeted
   optimizations during migration (for example, moving a self-managed
   database to Amazon RDS) without changing the core application
   architecture.
6. **Repurchase** — replace the workload with a SaaS or different
   commercial product.
7. **Refactor/re-architect** — rebuild the application to take advantage
   of cloud-native patterns (the compute and data services covered in
   Chapters 04 and 05), usually reserved for workloads where the business
   case justifies the higher effort.

**AWS Database Migration Service (DMS)** migrates databases with minimal
downtime, supporting both homogeneous migrations (same engine) and
heterogeneous migrations (engine change, such as Oracle to Aurora
PostgreSQL) when paired with the **AWS Schema Conversion Tool (SCT)** for
schema and code translation. DMS supports both a one-time full load and
ongoing **change data capture (CDC)** replication, which is what enables a
low-downtime cutover: the target stays continuously synchronized until the
final cutover moment.

### AWS Resilience Hub

**AWS Resilience Hub** assesses a defined application (a CloudFormation
stack, Terraform state, or resource group) against a selected **resiliency
policy** expressing target RTO/RPO for defined disruption types
(infrastructure, application, AZ, and Region-level disruptions), producing
a scored assessment and specific, prioritized recommendations to close any
gap between the current architecture and the stated target.

## Design Considerations

- **Choose the DR strategy the business is willing to pay for, not the
  most resilient one available.** A multi-site active/active architecture
  for a workload with a genuinely acceptable four-hour RTO is a wasted
  standing cost; conversely, a backup-and-restore strategy for a
  workload the business claims needs minutes-level RTO is a
  latent incident waiting to happen. Reconcile the stated RTO/RPO with
  actual budget before committing to an architecture.
- **RPO is bounded by the replication mechanism's lag, not by policy.** A
  stated RPO of thirty seconds is not achievable with S3 CRR's
  typical-under-fifteen-minutes replication window; match the mechanism
  to the requirement, not the other way around.
- **DNS failover has a floor set by TTL and client caching behavior**,
  not just the health check interval; some clients and intermediate
  resolvers ignore or extend TTLs, so DNS-based failover should be
  treated as "usually fast" rather than "guaranteed within N seconds" for
  the most time-critical failover requirements, where Global Accelerator
  ([Chapter 03](03-secure-networking-hybrid-connectivity-and-edge.md)) or a load-balancer-level mechanism may be more
  appropriate.
- **Active/active introduces data-conflict design obligations.**
  DynamoDB Global Tables' last-writer-wins conflict resolution is
  invisible to the application unless deliberately designed around
  (idempotent writes, conflict-free data types, or partitioning writes by
  Region); an active/active architecture is a data-modeling commitment,
  not only an infrastructure one.
- **Migration wave planning should sequence by dependency and risk, not
  size.** Migrate low-risk, well-understood workloads first to build
  operational confidence and refine the runbook before tackling
  business-critical or tightly coupled systems; a common failure pattern
  is sequencing purely by team availability rather than technical
  dependency order.
- **DMS CDC cutover windows still require a coordination plan.** Even
  with continuous replication minimizing downtime, the final cutover
  (stopping writes to the source, confirming the target is caught up,
  redirecting the application) is a coordinated, rehearsed event, not an
  unattended automatic switch.
- **Resilience Hub assessments are only as good as the defined resource
  scope.** An assessment that omits a critical dependency (a shared
  DNS zone, an external SaaS integration) will report a resiliency score
  that does not reflect the workload's actual end-to-end failure modes.

## Implementation and Automation

### 1. Route 53 health check and failover records

```bash
HEALTH_CHECK_ID=$(aws route53 create-health-check \
  --caller-reference "primary-$(date +%s)" \
  --health-check-config '{
    "IPAddress": "203.0.113.10",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/healthz",
    "RequestInterval": 30,
    "FailureThreshold": 3
  }' --query "HealthCheck.Id" --output text)

aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" \
  --change-batch '{
    "Changes": [
      {
        "Action": "UPSERT",
        "ResourceRecordSet": {
          "Name": "app.example.com", "Type": "A", "SetIdentifier": "primary",
          "Failover": "PRIMARY", "TTL": 30,
          "ResourceRecords": [{"Value": "203.0.113.10"}],
          "HealthCheckId": "'"$HEALTH_CHECK_ID"'"
        }
      },
      {
        "Action": "UPSERT",
        "ResourceRecordSet": {
          "Name": "app.example.com", "Type": "A", "SetIdentifier": "secondary",
          "Failover": "SECONDARY", "TTL": 30,
          "ResourceRecords": [{"Value": "198.51.100.10"}]
        }
      }
    ]
  }'
```

### 2. S3 Cross-Region Replication (Terraform)

```hcl
resource "aws_s3_bucket_replication_configuration" "crr" {
  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "replicate-to-dr-region"
    status = "Enabled"
    filter {}
    destination {
      bucket        = aws_s3_bucket.data_dr.arn
      storage_class = "STANDARD_IA"
      replication_time {
        status = "Enabled"
        time { minutes = 15 }
      }
      metrics {
        status = "Enabled"
        event_threshold { minutes = 15 }
      }
    }
  }
}
```

### 3. Aurora Global Database

```hcl
resource "aws_rds_global_cluster" "app" {
  global_cluster_identifier = "app-global"
  engine                    = "aurora-postgresql"
  engine_version            = "16.4"
  database_name              = "appdb"
  storage_encrypted          = true
}

resource "aws_rds_cluster" "primary" {
  cluster_identifier        = "app-primary-useast1"
  engine                    = "aurora-postgresql"
  engine_version            = "16.4"
  global_cluster_identifier = aws_rds_global_cluster.app.id
  master_username           = "appadmin"
  manage_master_user_password = true
  db_subnet_group_name      = aws_db_subnet_group.primary.name
}

resource "aws_rds_cluster" "secondary" {
  provider                  = aws.us-west-2
  cluster_identifier        = "app-secondary-uswest2"
  engine                    = "aurora-postgresql"
  engine_version            = "16.4"
  global_cluster_identifier = aws_rds_global_cluster.app.id
  db_subnet_group_name      = aws_db_subnet_group.secondary.name
}
```

### 4. DynamoDB Global Table

```hcl
resource "aws_dynamodb_table" "orders_global" {
  name             = "orders"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "order_id"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "order_id"
    type = "S"
  }

  replica {
    region_name = "us-west-2"
  }
  replica {
    region_name = "eu-west-1"
  }
}
```

### 5. Application Migration Service and DMS

```bash
# Register a source server for continuous replication (agent installed on source first)
aws mgn describe-source-servers --filters '{"isArchived": false}'

# Launch a test instance from the latest replicated snapshot without cutover
aws mgn start-test \
  --source-server-id s-1234567890abcdef0

# Create a DMS replication instance and a CDC-enabled migration task
aws dms create-replication-instance \
  --replication-instance-identifier app-db-migration \
  --replication-instance-class dms.r6i.large \
  --vpc-security-group-ids sg-0123456789abcdef0

aws dms create-replication-task \
  --replication-task-identifier oracle-to-aurora-cdc \
  --source-endpoint-arn "$SOURCE_ENDPOINT_ARN" \
  --target-endpoint-arn "$TARGET_ENDPOINT_ARN" \
  --replication-instance-arn "$REPL_INSTANCE_ARN" \
  --migration-type full-load-and-cdc \
  --table-mappings file://table-mappings.json
```

### 6. Resilience Hub assessment

```bash
aws resiliencehub create-app --name "payments-api" \
  --description "Customer-facing payments API"

aws resiliencehub create-resiliency-policy \
  --policy-name "tier1-30min-rto" \
  --tier "MissionCritical" \
  --policy '{
    "Software": {"rtoInSecs": 1800, "rpoInSecs": 300},
    "Hardware": {"rtoInSecs": 1800, "rpoInSecs": 300},
    "AZ": {"rtoInSecs": 1800, "rpoInSecs": 300},
    "Region": {"rtoInSecs": 14400, "rpoInSecs": 3600}
  }'

aws resiliencehub start-app-assessment \
  --app-arn "$APP_ARN" --assessment-name "quarterly-review"
```

## Validation and Troubleshooting

- **Confirm Route 53 failover actually shifts traffic.** `aws route53
  get-health-check-status --health-check-id "$HEALTH_CHECK_ID"` shows
  each checking Region's current verdict; a health check that never
  fails during a planned test likely has a path/port misconfiguration
  that always returns success regardless of the actual application
  state — verify the check targets the real application health endpoint,
  not a static page.
- **S3 CRR replication lag exceeding the configured RTC window.** `aws
  s3api get-bucket-replication` confirms configuration; per-object
  replication status is visible via `x-amz-replication-status` in object
  metadata (`PENDING`, `COMPLETED`, `FAILED`) — a sustained `FAILED`
  status usually indicates a destination bucket policy or KMS key policy
  gap for the replication role.
- **Aurora Global Database secondary Region lag spikes.** Check the
  `AuroraGlobalDBReplicationLag` CloudWatch metric; sustained high lag
  under normal write volume often indicates the secondary Region's
  instance class is undersized relative to the primary's write
  throughput.
- **DMS task stuck or erroring.** `aws dms describe-replication-tasks
  --query "ReplicationTasks[].ReplicationTaskStats"` reports load
  progress; validation failures are visible per-table in the task's
  table statistics, most commonly caused by unsupported data types
  requiring a transformation rule in the table mapping.
- **Common failure: DR Region drift.** A DR Region's infrastructure
  (security groups, IAM roles, AMIs) provisioned once and never updated
  alongside the primary Region silently diverges over time; DR
  infrastructure must be defined in the same IaC pipeline as production,
  not maintained as a one-time manual copy.
- **Common failure: untested runbook fails during an actual event.** A
  DR plan that has never been executed as a game day exercise
  frequently has an undocumented manual step (a DNS delegation change, a
  credential that only exists in the primary Region's Secrets Manager)
  that blocks the real failover; schedule regular DR game days, not just
  architecture reviews.

## Security and Best Practices

- Replicate CloudTrail, GuardDuty, and Security Hub findings to the DR
  Region (or maintain them Region-agnostic via organization-wide trails)
  so security visibility does not disappear during a failover event.
- Ensure IAM roles, KMS keys, and Secrets Manager secrets needed by the
  DR Region exist and are kept in sync continuously, not created
  reactively during a declared disaster — a DR failover is the worst
  possible time to discover a missing IAM role.
- Test restores from AWS Backup on a defined schedule, not only backup
  creation; an unrestorable backup provides false confidence.
- Encrypt cross-Region replication traffic and replicated data at rest
  using Region-appropriate KMS keys (KMS keys are Regional; a
  multi-Region key or an equivalent key per Region must be provisioned
  deliberately).
- Apply the same guardrail SCPs and security baseline from [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md) to
  the DR Region's accounts/OUs — DR infrastructure is not exempt from
  the organization's security posture.
- Run DR failover exercises ("game days") on a recurring cadence and
  record actual measured RTO/RPO against the target, feeding gaps back
  into the Resilience Hub assessment.

## References and Knowledge Checks

**References**

- [AWS Well-Architected Reliability Pillar whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) — the four DR
  strategies and design principles.
- [Amazon Route 53 documentation](https://docs.aws.amazon.com/Route53/) — health checks and routing policies.
- [Amazon Aurora Global Database and Amazon DynamoDB Global Tables
  documentation.](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
- [AWS Application Migration Service (MGN) and AWS Database Migration
  Service (DMS) documentation.](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)
- [AWS Resilience Hub documentation.](https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html)
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the reliability, migration, and business-
  continuity domains of the AWS Certified Solutions Architect blueprint.

**Knowledge checks**

1. Why is a stated RPO of thirty seconds incompatible with S3 Cross-
   Region Replication as the sole replication mechanism?
2. What distinguishes "pilot light" from "warm standby" in standing cost
   and RTO?
3. Why does an active/active multi-Region architecture impose a data-
   modeling obligation that a single-writer replication mechanism does
   not?
4. Which "R" in the 7 Rs framework corresponds to moving a self-managed
   on-premises database to Amazon RDS during a lift-and-shift migration,
   and why is it not classified as a pure "rehost"?

## Hands-On Lab

**Objective:** Configure Route 53 failover routing between two endpoints
with a health check, and confirm that failing the primary's health check
shifts resolution to the secondary.

**Cost implications:** Route 53 hosted zones ($0.50/month), health checks
(a small per-check monthly charge), and DNS queries are low-cost but not
free. This lab does not require EC2 or any compute resource — it uses two
low-cost static endpoints. Complete cleanup to stop the hosted zone and
health check charges.

**Prerequisites**

- An AWS account with a Route 53 public hosted zone (or willingness to
  create a temporary one for this lab) and AWS CLI v2 configured.
- Two reachable HTTP(S) endpoints to use as primary/secondary targets
  (two small S3 static website endpoints or two EC2 test instances are
  sufficient; the lab below uses two S3 static websites for minimal
  cost).

**Steps**

1. Create a hosted zone for the lab and record its ID:

   ```bash
   ZONE_ID=$(aws route53 create-hosted-zone \
     --name lab-dr-test.example.com \
     --caller-reference "lab-$(date +%s)" \
     --query "HostedZone.Id" --output text)
   ```

2. Create a health check against the primary endpoint:

   ```bash
   HC_ID=$(aws route53 create-health-check \
     --caller-reference "lab-hc-$(date +%s)" \
     --health-check-config '{
       "FullyQualifiedDomainName": "primary-endpoint.example.com",
       "Port": 80, "Type": "HTTP", "ResourcePath": "/",
       "RequestInterval": 30, "FailureThreshold": 2
     }' --query "HealthCheck.Id" --output text)
   ```

3. Create primary and secondary failover records:

   ```bash
   aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" \
     --change-batch '{
       "Changes": [
         {"Action": "CREATE", "ResourceRecordSet": {
           "Name": "app.lab-dr-test.example.com", "Type": "CNAME",
           "SetIdentifier": "primary", "Failover": "PRIMARY", "TTL": 30,
           "ResourceRecords": [{"Value": "primary-endpoint.example.com"}],
           "HealthCheckId": "'"$HC_ID"'"}},
         {"Action": "CREATE", "ResourceRecordSet": {
           "Name": "app.lab-dr-test.example.com", "Type": "CNAME",
           "SetIdentifier": "secondary", "Failover": "SECONDARY", "TTL": 30,
           "ResourceRecords": [{"Value": "secondary-endpoint.example.com"}]}}
       ]
     }'
   ```

4. Confirm the health check is currently healthy and DNS resolves to the
   primary:

   ```bash
   aws route53 get-health-check-status --health-check-id "$HC_ID"
   dig +short app.lab-dr-test.example.com CNAME
   ```

   **Expected result:** The health check reports healthy from a majority
   of checking Regions, and `dig` returns `primary-endpoint.example.com`.

5. **Negative test:** Point the primary endpoint's DNS at an address that
   will fail the health check (or stop the primary endpoint's service),
   wait for the failure threshold (roughly two minutes at a 30-second
   interval with a threshold of 2), then re-check:

   ```bash
   aws route53 get-health-check-status --health-check-id "$HC_ID"
   dig +short app.lab-dr-test.example.com CNAME
   ```

   **Expected result:** The health check reports unhealthy, and `dig`
   now returns `secondary-endpoint.example.com`, confirming automatic
   failover occurred without any manual DNS change.

6. **Cleanup:**

   ```bash
   aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" \
     --change-batch '{
       "Changes": [
         {"Action": "DELETE", "ResourceRecordSet": {
           "Name": "app.lab-dr-test.example.com", "Type": "CNAME",
           "SetIdentifier": "primary", "Failover": "PRIMARY", "TTL": 30,
           "ResourceRecords": [{"Value": "primary-endpoint.example.com"}],
           "HealthCheckId": "'"$HC_ID"'"}},
         {"Action": "DELETE", "ResourceRecordSet": {
           "Name": "app.lab-dr-test.example.com", "Type": "CNAME",
           "SetIdentifier": "secondary", "Failover": "SECONDARY", "TTL": 30,
           "ResourceRecords": [{"Value": "secondary-endpoint.example.com"}]}}
       ]
     }'
   aws route53 delete-health-check --health-check-id "$HC_ID"
   aws route53 delete-hosted-zone --id "$ZONE_ID"
   ```

   Confirm removal:

   ```bash
   aws route53 get-hosted-zone --id "$ZONE_ID"
   ```

   The command must return a `NoSuchHostedZone` error.

## Summary and Completion Checklist

Recovery Time Objective and Recovery Point Objective are business
decisions that determine which of the four DR strategies — backup and
restore, pilot light, warm standby, or multi-site active/active — is
appropriate, and the correct choice balances standing cost against the
stated recovery targets rather than maximizing resilience unconditionally.
S3 Cross-Region Replication, Aurora Global Database, and DynamoDB Global
Tables offer materially different replication lag and write-topology
characteristics that must match the chosen RPO. The 7 Rs framework
classifies migration approaches, with AWS Application Migration Service
and AWS Database Migration Service providing the low-downtime cutover
tooling for rehost and replatform migrations. AWS Resilience Hub turns
resiliency posture from an assumption into a scored, continuously
assessable metric against a defined policy.

- [ ] Can select a DR strategy given a stated RTO/RPO and cost
      constraint.
- [ ] Can configure Route 53 health checks and failover routing.
- [ ] Can compare S3 CRR, Aurora Global Database, and DynamoDB Global
      Tables by replication model and write topology.
- [ ] Can classify a migration scenario using the 7 Rs framework.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
