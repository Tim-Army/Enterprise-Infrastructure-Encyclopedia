# Chapter 06: Cloud Storage, Databases, and Data Services

## Learning Objectives

- Differentiate object, block, and file storage and choose correctly among
  them for a given access pattern.
- Design a storage lifecycle and tiering policy that balances access
  latency against cost across a data set's useful life.
- Compare managed relational, NoSQL, and caching database services and
  select correctly based on consistency, access pattern, and scale
  requirements.
- Explain the CAP theorem's practical implications for distributed managed
  database selection.
- Design a backup, replication, and recovery strategy using Recovery Point
  Objective (RPO) and Recovery Time Objective (RTO) as the driving
  requirements.
- Implement storage lifecycle policy and a managed database with
  encryption and automated backup as code, and validate a restore.

## Theory and Architecture

### Object, block, and file storage

- **Object storage** — stores immutable objects (arbitrary binary data
  plus metadata) in a flat namespace, accessed over an HTTP(S) API rather
  than a filesystem mount. Effectively unlimited scale, strong durability
  (typically eleven nines or better via automatic multi-device, often
  multi-zone, replication), and the default choice for unstructured data:
  backups, media, logs, data lake storage, and static web content. Object
  storage is not a general-purpose filesystem — there is no in-place
  partial-file modification; updating an object means replacing it
  entirely.
- **Block storage** — presents a raw block device attached to a single
  compute instance (or, for some provider offerings, a small number of
  instances with coordination), formatted with a conventional filesystem
  by the guest OS. Required for anything needing POSIX filesystem
  semantics, low-latency random I/O, or to serve as the underlying volume
  for a database engine's own storage layer. Performance is normally
  specified directly (provisioned IOPS and throughput), independent of
  volume size on higher-tier offerings.
- **File storage** — a managed, network-attached filesystem (NFS or SMB)
  mountable concurrently by many compute instances, providing shared
  POSIX or SMB semantics without the customer operating a file server.
  The correct choice when multiple instances need concurrent read/write
  access to the same file namespace, which neither object storage
  (no true concurrent in-place writes) nor block storage (single-instance
  attachment in the common case) provides natively.

| Attribute | Object | Block | File |
| --- | --- | --- | --- |
| Access method | HTTP(S) API | Raw device via OS | Network filesystem protocol (NFS/SMB) |
| Concurrent multi-client access | Yes, read-heavy patterns | No (typically single-attach) | Yes, native |
| Typical latency | Higher (network + API overhead) | Lowest | Low-to-moderate |
| Typical use | Backups, media, logs, data lake | Database volumes, boot volumes | Shared application state, home directories, content repositories |
| Scaling model | Effectively unlimited, automatic | Provisioned per volume | Provisioned per filesystem, often auto-scaling in modern offerings |

### Storage lifecycle and tiering

Object storage services typically offer multiple storage classes trading
retrieval latency and per-GB storage cost against each other: a frequent-
access tier at the highest per-GB cost and lowest retrieval latency, one
or more infrequent-access tiers at lower storage cost with either a
retrieval fee or slightly higher latency, and one or more archive tiers at
the lowest storage cost with retrieval times measured in minutes to hours
rather than milliseconds. A lifecycle policy automatically transitions
objects between tiers (and eventually to deletion or archive) based on
object age or last-access time, without requiring an application change.

Design lifecycle policy from the data's actual access pattern, not from
its age alone where the two diverge: a compliance archive accessed at
most once a year belongs in an archive tier from day one regardless of how
recently it was created, while an actively queried analytics data set
should stay in a frequent-access tier even after it ages past an
arbitrary threshold, if it is still being read regularly. Where the access
pattern is genuinely age-correlated (the common case for logs and backups
— recent data accessed frequently, older data rarely), an age-based
lifecycle policy is the simpler and sufficient choice.

### Managed database categories

- **Managed relational (SQL)** — a provider-operated relational database
  engine (handling patching, backup, and often failover) exposed through
  a standard SQL dialect. The default for workloads needing strong
  consistency, multi-row transactions, and a well-understood relational
  data model.
- **Managed NoSQL — key-value and document** — schema-flexible stores
  optimized for high-throughput, low-latency access by a primary key,
  typically trading multi-row transactional guarantees and complex join
  support for horizontal scalability that a single relational instance
  cannot match. Appropriate for workloads with a well-defined access
  pattern by key (session state, user profiles, product catalogs) that
  need to scale writes horizontally beyond what vertical scaling of a
  relational engine supports.
- **Managed wide-column / distributed database** — designed for very
  high write throughput and horizontal scale across regions, typically
  with tunable consistency. Appropriate for time-series, telemetry, and
  other workloads with extreme write volume and predictable access
  patterns.
- **Managed in-memory cache** — a managed key-value store held in memory
  (commonly a managed Redis- or Memcached-compatible service), used to
  offload read pressure from a primary database or to hold ephemeral
  session/state data with sub-millisecond access latency. Not a system of
  record: design the application to tolerate cache data loss and
  repopulate from the primary store.

### CAP theorem and practical database selection

The CAP theorem states that a distributed data store can provide at most
two of three guarantees simultaneously during a network partition:
**consistency** (every read receives the most recent write or an error),
**availability** (every request receives a non-error response), and
**partition tolerance** (the system continues operating despite network
partitions between nodes). Because network partitions are a fact of
distributed systems life, partition tolerance is effectively mandatory in
practice, which reduces the real-world decision to a spectrum between
consistency and availability under partition:

- **CP-leaning systems** reject or delay requests during a partition
  rather than risk returning stale or conflicting data — appropriate for
  financial transactions, inventory counts, and anything where an
  incorrect read is worse than a temporarily unavailable one.
- **AP-leaning systems** continue serving requests during a partition,
  accepting that some reads may return stale data until the partition
  heals and the system reconciles (commonly via eventual consistency) —
  appropriate for content that tolerates brief staleness (a product
  description, a social media feed) in exchange for uninterrupted
  availability.

Most managed NoSQL services expose a tunable consistency setting (per-
request or per-table) rather than forcing a single global choice, which
lets a single database serve both a strongly consistent read path (a
current account balance) and an eventually consistent one (a historical
activity feed) from the same underlying service. Treat the CAP trade-off
as a per-access-pattern decision, not a single database-wide setting
chosen once at provisioning time.

### Backup, replication, and recovery objectives

Every data service's resilience design should be driven by two explicitly
stated, workload-specific requirements, not a default "back it up
nightly" habit:

- **Recovery Point Objective (RPO)** — the maximum acceptable amount of
  data loss, measured as time (for example, "no more than 15 minutes of
  data loss is acceptable"). RPO drives backup/replication frequency:
  achieving a 15-minute RPO requires continuous or near-continuous
  replication or transaction-log shipping, not a nightly snapshot.
- **Recovery Time Objective (RTO)** — the maximum acceptable time to
  restore service after a failure. RTO drives the recovery mechanism
  choice: a multi-hour RTO can be satisfied by restoring from a backup, a
  minutes-scale RTO typically requires a warm or hot standby replica
  ready to be promoted, not a restore-from-backup process.

Cross-region replication additionally protects against a full-region
failure, which same-region multi-zone replication does not — design the
replication topology (same-zone, cross-zone, cross-region) against the
specific failure scope the RPO/RTO requirement is meant to survive.

## Design Considerations

### Matching storage type to access pattern

Choose storage type from the actual access pattern the workload needs,
not from what is most familiar to the team. A common anti-pattern is
running a shared network filesystem workload on block storage attached to
a single "file server" instance the team manually built — recreating an
on-premises single-point-of-failure pattern inside the cloud instead of
using the provider's managed file storage service built for exactly that
concurrent-access requirement.

### Choosing a database category

Start from the access pattern and consistency requirement, not from
familiarity with SQL. A workload with a well-defined, high-volume
key-based access pattern and no need for multi-row transactions or
complex joins (a session store, a shopping cart) is frequently a better
fit for managed NoSQL than for forcing horizontal scale onto a relational
engine through manual sharding — which reintroduces significant
operational complexity the managed NoSQL service would otherwise absorb.
Conversely, do not adopt NoSQL for a workload with genuine multi-row
transactional and relational-integrity requirements just because it is
perceived as more "cloud-native"; the operational and consistency cost of
working around the missing transactional guarantees usually exceeds the
scalability benefit for that workload shape.

### RPO/RTO-driven resilience design, not resilience-driven RPO/RTO

Determine RPO and RTO from the business impact of data loss and downtime
for a specific workload first, then design the backup/replication
mechanism to meet them — not the reverse. Designing the mechanism first
("we do nightly backups") and then describing whatever RPO that happens
to deliver as "the RPO" skips the actual business-requirements
conversation and routinely under-protects a workload that needed a
tighter RPO than the default mechanism happens to provide.

### Encryption and key management alignment

Apply the key management model decision from Chapter 03 consistently
across storage and database services: a data classification requiring
customer-managed keys for compliance should use them uniformly across
every storage and database service holding that data, including backups
and replicas — a backup encrypted with a different (or provider-managed)
key than its source is a common audit finding and a real data-governance
gap.

### Storage cost as a first-class design input

Object storage lifecycle policy, block storage over-provisioning, and
database instance sizing are all significant, continuously accruing cost
drivers, not one-time decisions. Fold storage and database sizing into
the same right-sizing review cadence established for compute in Chapter
05, and treat an unmanaged, growing volume of data sitting in the
highest-cost storage tier indefinitely as a finding requiring lifecycle
policy, not an acceptable steady state.

## Implementation and Automation

### Object storage with lifecycle policy

```hcl
# storage.tf — illustrative object storage bucket with tiering lifecycle.
resource "cloud_object_storage_bucket" "app_data" {
  name = "example-app-data-${var.environment}"

  versioning_enabled = true
  encryption {
    kms_key_id = var.customer_managed_key_id # aligns with Chapter 03 key model
  }

  lifecycle_rule {
    id      = "age-based-tiering"
    enabled  = true

    transition {
      days          = 30
      storage_class   = "infrequent-access"
    }
    transition {
      days          = 90
      storage_class   = "archive"
    }
    expiration {
      days = 2555 # 7-year retention, then delete
    }
  }
}
```

### Managed relational database with automated backup

```hcl
# database.tf — illustrative managed relational database instance.
resource "cloud_managed_database" "primary" {
  engine          = "postgresql"
  engine_version    = "16"
  instance_class    = "db.r6.large" # memory-optimized, matches OLTP working-set ratio

  storage_encrypted   = true
  kms_key_id       = var.customer_managed_key_id

  backup_retention_days = 14
  backup_window      = "03:00-04:00"
  multi_az         = true # synchronous standby within the region

  deletion_protection = true
}

resource "cloud_managed_database_replica" "cross_region_dr" {
  source_database_id = cloud_managed_database.primary.id
  region        = var.dr_region
  instance_class    = "db.r6.large"
  # Asynchronous cross-region replica: protects against full-region
  # failure; RPO bounded by replication lag, not zero.
}
```

### Managed NoSQL table with tunable consistency

```hcl
# nosql.tf — illustrative managed NoSQL table.
resource "cloud_nosql_table" "sessions" {
  name         = "user-sessions-${var.environment}"
  partition_key   = "session_id"
  billing_mode   = "on-demand" # scales with traffic, no pre-provisioned capacity

  ttl_attribute   = "expires_at" # automatic expiration; sessions are not a system of record

  point_in_time_recovery = true
}
```

### Restore automation and validation script

```bash
#!/usr/bin/env bash
# restore-and-validate.sh — illustrative restore drill automation.
set -euo pipefail

SNAPSHOT_ID="${1:?snapshot id required}"
TARGET_INSTANCE="restore-drill-$(date +%s)"

cloud-cli database restore-from-snapshot \
  --snapshot-id "$SNAPSHOT_ID" \
  --target-instance-id "$TARGET_INSTANCE"

cloud-cli database wait --instance-id "$TARGET_INSTANCE" --status available

# Run an application-level validation query against the restored instance
# rather than only checking that the instance reports "available."
psql "host=$TARGET_INSTANCE.example dbname=app" -c "SELECT count(*) FROM orders;"

cloud-cli database delete --instance-id "$TARGET_INSTANCE" --skip-final-snapshot
```

## Validation and Troubleshooting

- **Validate a restore by testing it, on a schedule, not by trusting that
  backups are completing successfully.** A backup job reporting success
  confirms the backup process ran; it does not confirm the resulting
  backup is actually restorable to a working state. Run a full restore
  drill (like the script above) periodically and record the actual time
  taken against the workload's stated RTO.
- **Diagnose unexpectedly high storage cost by first checking lifecycle
  policy application**, not by immediately assuming a data volume
  problem — a lifecycle rule that silently stopped applying (commonly
  after a bucket configuration change) is a common, easily overlooked
  cause of data accumulating in the highest-cost tier indefinitely.
- **Diagnose replication lag issues on an asynchronous replica by
  checking the lag metric directly**, not by assuming the replica is
  current — an application inadvertently reading from a lagging replica
  after a recent write is a common source of "the data isn't there yet"
  reports that are not actually a bug.
- **Test failover to a standby explicitly and measure actual RTO**,
  including DNS/connection-string cutover time, not only the database
  engine's own failover time — the end-to-end RTO experienced by the
  application is frequently longer than the database engine's reported
  failover duration.
- **Confirm cross-region replica encryption uses the correct
  region-appropriate key reference**, since a customer-managed key is
  typically a regional resource and a cross-region replica needs its own
  key or a deliberately configured multi-region key strategy — this is a
  common oversight surfaced only during a DR drill or an audit.

## Security and Best Practices

- Default to private, non-public access for every storage bucket, file
  share, and database endpoint; require an explicit, reviewed exception
  for any public-read object storage use case (static website assets,
  for example), never a default-open bucket.
- Encrypt data at rest for every storage and database service using the
  key management model established in Chapter 03, applied consistently
  across primary data, replicas, and backups.
- Enable versioning or point-in-time recovery on data stores holding
  data that cannot be regenerated, as protection against accidental
  overwrite or deletion in addition to infrastructure failure.
- Restrict database network access to the specific application security
  groups from Chapter 04 that require it; never expose a database
  endpoint directly to the public internet.
- Test restores on a defined schedule and record the result as an
  auditable artifact — an untested backup should be treated as an
  unverified control, not a satisfied one.
- Apply the same least-privilege identity model from Chapter 03 to data
  access: a workload identity should hold read or write access to only
  the specific tables, buckets, or prefixes it requires, not broad
  account-wide storage or database permissions.

## References and Knowledge Checks

### References

- Brewer, E., *Towards Robust Distributed Systems* (the original CAP
  conjecture presentation).
- Each major provider's object storage, block storage, file storage, and
  managed database service documentation — consult the current vendor
  source for exact storage class names, consistency tuning options, and
  backup retention limits.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. A team needs a shared filesystem mounted concurrently by twelve
   application instances. Why is a single block-storage-backed "file
   server" instance not the correct managed-service equivalent?
2. Explain why partition tolerance is treated as effectively mandatory in
   practice, reducing the CAP trade-off to a consistency/availability
   spectrum.
3. A workload states an RPO of 5 minutes and an RTO of 10 minutes. What
   does this rule out as a viable backup/recovery mechanism, and why?
4. Why is a successfully completing nightly backup job insufficient
   evidence that the workload's stated RTO can actually be met?
5. A cross-region database replica uses the primary region's
   customer-managed key reference and fails to provision. What is the
   likely cause?

## Hands-On Lab

### Lab 6.1 — Storage lifecycle policy validation and RPO/RTO calculation

This lab uses local Terraform `check` blocks to validate that a proposed
storage lifecycle policy's tier transition ordering is internally
consistent (each transition must occur later than the previous one) and
that a proposed backup mechanism can plausibly satisfy a stated RPO. No
cloud account or credentials are required.

**Prerequisites**

- Terraform 1.9.x or later, or a compatible OpenTofu release.
- A POSIX shell.

**Steps**

1. Create the working directory:

   ```bash
   mkdir -p ~/labs/vol07-ch06 && cd ~/labs/vol07-ch06
   ```

2. Create `variables.tf`:

   ```hcl
   variable "infrequent_access_after_days" {
     type    = number
     default = 30
   }

   variable "archive_after_days" {
     type    = number
     default = 90
   }

   variable "backup_interval_minutes" {
     type    = number
     default = 60
   }

   variable "required_rpo_minutes" {
     type    = number
     default = 15
   }
   ```

3. Create `main.tf`:

   ```hcl
   check "lifecycle_transitions_ordered" {
     assert {
       condition     = var.archive_after_days > var.infrequent_access_after_days
       error_message = "archive_after_days must be greater than infrequent_access_after_days; tiers must transition in increasing order."
     }
   }

   check "backup_interval_meets_rpo" {
     assert {
       condition     = var.backup_interval_minutes <= var.required_rpo_minutes
       error_message = "backup_interval_minutes exceeds required_rpo_minutes; this backup mechanism cannot satisfy the stated RPO."
     }
   }

   output "lifecycle_summary" {
     value = {
       infrequent_access_after_days = var.infrequent_access_after_days
       archive_after_days       = var.archive_after_days
       backup_interval_minutes    = var.backup_interval_minutes
       required_rpo_minutes      = var.required_rpo_minutes
     }
   }
   ```

4. Initialize and plan with the default values:

   ```bash
   terraform init
   terraform plan
   ```

   **Expected result:** The `lifecycle_transitions_ordered` check passes
   (90 > 30), but `backup_interval_meets_rpo` **fails** — a 60-minute
   backup interval cannot satisfy a 15-minute RPO. Terraform reports:
   `backup_interval_minutes exceeds required_rpo_minutes; this backup
   mechanism cannot satisfy the stated RPO.` This is the expected, correct
   outcome of this step: it demonstrates the check catching a real,
   common mismatch between a default hourly backup job and a
   tighter-than-hourly business requirement.

5. Correct the mismatch by supplying a backup interval that meets the
   RPO:

   ```bash
   terraform plan -var="backup_interval_minutes=10"
   ```

   **Expected result:** Both checks pass with no failures reported.

**Negative test**

6. Confirm the lifecycle ordering check independently by supplying an
   invalid tier order:

   ```bash
   terraform plan -var="backup_interval_minutes=10" -var="archive_after_days=20"
   ```

   **Expected result:** `lifecycle_transitions_ordered` fails with
   `archive_after_days must be greater than infrequent_access_after_days;
   tiers must transition in increasing order.`, confirming the check
   independently catches a misconfigured lifecycle policy regardless of
   the backup interval value.

**Cleanup**

7. Remove the lab directory:

   ```bash
   cd ~ && rm -rf ~/labs/vol07-ch06
   ```

   **Expected result:** The directory no longer exists. No cloud storage
   or database resources were created at any point in this lab.

## Summary and Completion Checklist

Cloud data services span object, block, and file storage, each suited to
a distinct access pattern, and managed relational, NoSQL, wide-column, and
caching databases, each suited to a distinct consistency and scale
requirement. The CAP theorem frames the practical consistency/availability
trade-off distributed databases make under partition, and RPO/RTO —
determined from business impact, not from a default backup habit — should
drive every backup, replication, and recovery design. Chapter 07 extends
these data services into hybrid and multicloud replication patterns, and
Chapter 09 covers ongoing observability and resilience operations for the
data layer.

- [ ] Can choose correctly among object, block, and file storage for a
      stated access pattern.
- [ ] Can select an appropriate managed database category from a stated
      consistency and access-pattern requirement.
- [ ] Can explain the CAP theorem's practical effect on managed database
      selection.
- [ ] Can derive a backup/replication mechanism from a stated RPO and RTO,
      rather than describing a default mechanism's RPO after the fact.
- [ ] Completed Lab 6.1, including the negative test and cleanup.
