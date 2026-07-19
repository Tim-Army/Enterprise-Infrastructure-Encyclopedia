# Chapter 05: Storage, Databases, Analytics, and Data Protection

## Learning Objectives

- Select among Amazon S3, Amazon EBS, and Amazon EFS for a given
  workload's access pattern, durability, and sharing requirements.
- Configure Amazon S3 bucket security controls, including Block Public
  Access, bucket policies, versioning, and lifecycle transitions across
  storage classes.
- Distinguish Amazon RDS, Amazon Aurora, and Amazon DynamoDB, and choose
  correctly among relational Multi-AZ, relational read-replica, and
  NoSQL designs.
- Encrypt data at rest with AWS KMS and explain the difference between
  AWS-managed and customer-managed keys.
- Describe how Amazon Redshift, AWS Glue, Amazon Athena, and AWS Lake
  Formation compose into an analytics pipeline.
- Configure AWS Backup as a centralized backup policy across multiple
  storage and database services.

## Theory and Architecture

AWS storage and database services divide along two axes that determine the
correct choice for a given workload: **access pattern** (object, block, or
file) for storage, and **data model** (relational or non-relational) for
databases.

### Object, block, and file storage

| Service | Access pattern | Durability | Typical use |
| --- | --- | --- | --- |
| Amazon S3 | Object (HTTP API, whole-object read/write) | 11 nines, Regional by default | Static assets, data lakes, backups, application file storage |
| Amazon EBS | Block (attached to one EC2 instance at a time, per-AZ) | 99.8–99.9% annual failure rate depending on volume type | Instance boot volumes, databases running on EC2 |
| Amazon EFS | File (POSIX, NFS, concurrently shared across instances/AZs) | 11 nines, Regional | Shared configuration, content repositories, workloads needing concurrent multi-instance access |

**Amazon S3** stores objects in **buckets**, each object addressed by a
key, with no inherent directory structure (prefixes simulate folders for
tooling and listing purposes). S3 **storage classes** trade retrieval
latency and per-request cost against per-GB storage cost:

| Storage class | Retrieval | Typical use |
| --- | --- | --- |
| S3 Standard | Milliseconds | Frequently accessed data |
| S3 Standard-IA / One Zone-IA | Milliseconds, lower storage cost, retrieval fee | Infrequently accessed data; One Zone trades AZ redundancy for lower cost |
| S3 Intelligent-Tiering | Milliseconds | Unknown/changing access patterns; AWS moves objects between tiers automatically |
| S3 Glacier Instant Retrieval | Milliseconds | Archive data needing occasional immediate access |
| S3 Glacier Flexible Retrieval | Minutes to hours | Archive data with rare, tolerant-of-delay access |
| S3 Glacier Deep Archive | Hours | Long-term compliance retention, lowest storage cost |

An **S3 Lifecycle configuration** automates the transition of objects
between storage classes (and eventual expiration) by age or prefix,
without any application code change. **S3 Versioning** retains every
version of an object when enabled, protecting against accidental overwrite
or deletion — combined with **S3 Object Lock** (WORM — Write Once, Read
Many), it satisfies regulatory retention requirements that must resist
even administrative deletion within a locked retention period.

**Amazon EBS** provides durable block storage attached to a single EC2
instance within one AZ at a time; volume types (`gp3` general purpose,
`io2 Block Express` for the highest IOPS/throughput databases, `st1`/`sc1`
for throughput-oriented workloads) trade cost against IOPS and throughput
ceilings. **EBS snapshots** are incremental, point-in-time copies stored
in S3 (though not directly accessible as S3 objects), forming the basis
for both backup and cross-Region/cross-account disaster recovery copies.

**Amazon EFS** is a fully managed NFS file system, elastically scaling
storage and supporting concurrent mounts from many EC2 instances, ECS
tasks, and Lambda functions across multiple AZs simultaneously — the
correct choice whenever multiple compute resources must read and write
the same file-based data set concurrently, which neither S3 (object
semantics, no POSIX locking) nor EBS (single-instance attachment) support
natively. **Amazon FSx** provides purpose-built managed file systems for
specific ecosystems (FSx for Windows File Server for SMB/Active Directory
environments, FSx for Lustre for high-performance computing workloads,
FSx for NetApp ONTAP and FSx for OpenZFS for feature parity with those
platforms).

### Relational databases: RDS and Aurora

**Amazon RDS** manages patching, backups, and Multi-AZ failover for
standard relational engines (PostgreSQL, MySQL, MariaDB, SQL Server,
Oracle). **RDS Multi-AZ** synchronously replicates to a standby in a
second AZ, failing over automatically on primary failure — this is a
high-availability mechanism, not a read-scaling mechanism, since the
standby is not readable in the classic Multi-AZ instance deployment.
**RDS read replicas** provide asynchronous, eventually consistent copies
that can serve read traffic and, for some engines, be promoted to a
standalone primary — a read-scaling and cross-Region DR mechanism distinct
from Multi-AZ's failover role. **Amazon Aurora** is AWS's own
MySQL/PostgreSQL-compatible engine with a storage layer replicated six
ways across three AZs automatically, decoupling compute (which can scale
independently, including to zero with **Aurora Serverless v2**) from a
shared, self-healing storage volume, and supporting up to fifteen
low-latency read replicas sharing the same underlying storage.

### Non-relational: Amazon DynamoDB

**Amazon DynamoDB** is a fully managed, serverless key-value and document
database delivering single-digit-millisecond latency at any scale, using a
**partition key** (and optional **sort key**) rather than a fixed
relational schema. Capacity is provisioned or, more commonly for variable
workloads, set to **on-demand**, billing per request with no capacity
planning. **Global Secondary Indexes (GSIs)** and **Local Secondary
Indexes (LSIs)** enable query patterns beyond the base key schema, but —
unlike a relational database — access patterns must be designed into the
table's key structure up front; DynamoDB does not support ad hoc joins or
arbitrary `WHERE` clauses at scale. **DynamoDB Global Tables** replicate a
table across Regions with multi-Region active-active writes, covered
further as a DR mechanism in [Chapter 06](06-reliability-migration-multi-region-and-disaster-recovery.md).

### Analytics: Redshift, Glue, Athena, and Lake Formation

- **Amazon Redshift** is a managed, columnar data warehouse for large-scale
  SQL analytics, with **Redshift Serverless** removing cluster sizing for
  variable analytical workloads.
- **AWS Glue** is a serverless ETL (extract, transform, load) service with
  a **Data Catalog** that stores table metadata (schema, location,
  partitioning) usable by Athena, Redshift Spectrum, and EMR alike.
- **Amazon Athena** runs serverless, interactive SQL queries directly
  against data in S3 using the Glue Data Catalog's schema, without
  provisioning any cluster — the standard tool for ad hoc querying of a
  data lake.
- **AWS Lake Formation** centralizes fine-grained (table-, column-, and
  row-level) access control over a data lake built on S3 and the Glue
  Data Catalog, layering governed permissions on top of what would
  otherwise be bucket-level IAM/S3 policy control alone.

### Encryption and key management

**AWS Key Management Service (KMS)** manages the cryptographic keys used
to encrypt data at rest across nearly every AWS storage and database
service. An **AWS managed key** (`aws/s3`, `aws/rds`, and so on) requires
no customer configuration but offers no customer control over rotation
schedule or key policy beyond default AWS behavior. A **customer managed
key (CMK)** gives full control over the key policy (who can use and
administer the key), rotation schedule, and the ability to revoke access
by disabling the key — the correct choice whenever compliance requires
demonstrable control over encryption keys, cross-account key sharing, or
detailed CloudTrail key-usage auditing.

## Design Considerations

- **Storage class transitions must match real, not assumed, access
  patterns.** Aggressive lifecycle transitions to Glacier tiers on data
  that is actually accessed periodically produce retrieval fees that
  exceed the storage savings; use S3 Storage Lens or S3 Intelligent-
  Tiering when the access pattern is genuinely unknown rather than
  guessing at a fixed lifecycle schedule.
- **RDS Multi-AZ and read replicas solve different problems and are often
  both needed.** Multi-AZ alone does not help a read-heavy workload scale,
  and a read replica alone does not provide automatic failover for
  writes; a production relational workload commonly needs both.
- **DynamoDB access patterns must be designed before the table, not
  after.** Because DynamoDB has no ad hoc query flexibility at scale,
  retrofitting a new access pattern onto an existing table typically
  requires a new GSI (with its own cost and eventual-consistency
  characteristics) or a data migration — model every required query
  pattern during design, not as an afterthought.
- **Aurora vs. RDS is a cost/control trade-off, not strictly a
  performance one.** Aurora's storage auto-scaling and read-replica
  latency advantages come with a different pricing model (I/O-optimized
  or I/O-included configurations) that needs modeling against actual
  workload I/O patterns rather than assumed to always be cheaper.
- **Customer-managed KMS keys add both control and operational overhead.**
  A CMK enables custom key policies and revocation, but the key's policy
  must explicitly grant the services and principals that need it —
  including AWS service-linked roles in some integrations — and an overly
  restrictive key policy can silently break a dependent service (a
  Lambda function that can no longer decrypt an environment variable, for
  example).
- **Lake Formation is worth adopting before a data lake sprawls, not
  after.** Retrofitting column- and row-level governance onto an existing
  S3-based data lake with established bucket-policy-only access control
  is significantly more disruptive than establishing Lake Formation
  permissions as the data lake is built.
- **EFS is not a substitute for object storage at S3's scale/cost
  profile**, and S3 is not a substitute for EFS's POSIX file semantics;
  choosing based on "it's file-shaped so it must be EFS" or "it's data so
  it must be S3" without considering concurrent-access and API
  requirements leads to expensive rearchitecting later.

## Implementation and Automation

### 1. S3 bucket with versioning, encryption, Block Public Access, and lifecycle policy

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "example-corp-app-data-2026"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    id     = "tier-and-expire"
    status = "Enabled"
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    expiration { days = 730 }
    noncurrent_version_expiration { noncurrent_days = 90 }
  }
}
```

### 2. Customer-managed KMS key

```hcl
resource "aws_kms_key" "data" {
  description             = "CMK for app-data bucket and RDS"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnableRootAccountAdmin"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::111122223333:root" }
        Action    = "kms:*"
        Resource  = "*"
      },
      {
        Sid       = "AllowAppRoleUse"
        Effect    = "Allow"
        Principal = { AWS = aws_iam_role.app.arn }
        Action    = ["kms:Decrypt", "kms:GenerateDataKey"]
        Resource  = "*"
      }
    ]
  })
}
```

### 3. Aurora PostgreSQL cluster with a reader endpoint

```hcl
resource "aws_rds_cluster" "app" {
  cluster_identifier      = "app-aurora"
  engine                  = "aurora-postgresql"
  engine_version          = "16.4"
  master_username         = "appadmin"
  manage_master_user_password = true
  database_name           = "appdb"
  db_subnet_group_name    = aws_db_subnet_group.app.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  storage_encrypted       = true
  kms_key_id              = aws_kms_key.data.arn
  backup_retention_period = 14
  preferred_backup_window = "03:00-04:00"
}

resource "aws_rds_cluster_instance" "writer" {
  cluster_identifier = aws_rds_cluster.app.id
  instance_class     = "db.r6g.large"
  engine             = aws_rds_cluster.app.engine
}

resource "aws_rds_cluster_instance" "reader" {
  count               = 2
  cluster_identifier  = aws_rds_cluster.app.id
  instance_class      = "db.r6g.large"
  engine              = aws_rds_cluster.app.engine
}
```

### 4. DynamoDB table with a Global Secondary Index and point-in-time recovery

```hcl
resource "aws_dynamodb_table" "orders" {
  name         = "orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
  attribute {
    name = "customer_id"
    type = "S"
  }

  global_secondary_index {
    name            = "customer-index"
    hash_key        = "customer_id"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.data.arn
  }
}
```

### 5. AWS Backup plan covering S3, RDS, and DynamoDB

```bash
aws backup create-backup-vault \
  --backup-vault-name central-backup-vault \
  --encryption-key-arn "$KMS_KEY_ARN"

aws backup create-backup-plan --backup-plan '{
  "BackupPlanName": "daily-14-day-retention",
  "Rules": [{
    "RuleName": "daily",
    "TargetBackupVaultName": "central-backup-vault",
    "ScheduleExpression": "cron(0 5 * * ? *)",
    "Lifecycle": {"DeleteAfterDays": 14}
  }]
}'

aws backup create-backup-selection \
  --backup-plan-id "$PLAN_ID" \
  --backup-selection '{
    "SelectionName": "tag-based-selection",
    "IamRoleArn": "arn:aws:iam::111122223333:role/AWSBackupDefaultServiceRole",
    "ListOfTags": [{"ConditionType": "STRINGEQUALS", "ConditionKey": "backup", "ConditionValue": "daily"}]
  }'
```

## Validation and Troubleshooting

- **Confirm Block Public Access is active before uploading sensitive
  data.** `aws s3api get-public-access-block --bucket <BUCKET>` must show
  all four settings `true`; a bucket policy alone does not protect
  against a future misconfigured ACL if Block Public Access is disabled.
- **Verify lifecycle transitions are actually running.** `aws s3api
  get-bucket-lifecycle-configuration` confirms the rule exists, but
  transition execution should be confirmed with S3 Storage Lens or by
  sampling object storage class with `aws s3api head-object` after the
  transition window — a syntactically valid but incorrectly scoped
  filter/prefix silently transitions zero objects.
- **RDS/Aurora failover taking longer than expected.** `aws rds
  describe-events --source-type db-cluster` shows the actual failover
  timeline; a failover meaningfully slower than the documented 30–60
  second Aurora typical range often indicates a long-running transaction
  or connection draining issue on the application side, not an AWS fault.
- **DynamoDB throttling (`ProvisionedThroughputExceededException`) on
  on-demand tables.** On-demand tables still enforce a per-partition
  throughput ceiling; a hot partition key (for example, a single
  high-traffic customer ID) can throttle even though aggregate table
  capacity is far from any limit — check CloudWatch's
  `ThrottledRequests` metric dimensioned by table, and redesign the
  partition key if a single key concentrates traffic.
- **Common failure: KMS key policy blocks a service that needs it.** An
  `AccessDeniedException` referencing KMS on an otherwise correctly
  IAM-permitted action means the **key policy**, not the caller's IAM
  policy, is the blocker — KMS key policies are evaluated independently
  and a caller needs both an IAM grant and a compatible key policy
  statement.
- **Common failure: Glue Data Catalog schema drift breaks Athena
  queries.** A query that ran previously and now fails with a column
  type mismatch usually indicates the underlying S3 data changed shape
  without a corresponding Glue crawler run; re-run the crawler or update
  the catalog table schema explicitly.

## Security and Best Practices

- Enable S3 Block Public Access at the account level (via Organizations
  SCP or account-level default) in addition to per-bucket settings, so a
  future bucket cannot be created public by mistake.
- Enable S3 Versioning and Object Lock (compliance mode) on any bucket
  holding data subject to retention regulation, and restrict
  `s3:PutBucketPolicy` and `s3:PutLifecycleConfiguration` to a small,
  audited set of principals.
- Encrypt every database and storage resource at rest using a
  customer-managed KMS key where compliance requires demonstrable key
  control, and enable KMS key rotation.
- Enforce TLS-in-transit for RDS/Aurora connections (`rds.force_ssl`
  parameter or engine-equivalent) and for S3 access (a bucket policy
  condition denying `aws:SecureTransport: false`).
- Use IAM database authentication or Secrets Manager-integrated
  credential rotation for RDS/Aurora rather than long-lived, manually
  rotated database passwords.
- Apply least-privilege, table/column-level access through Lake
  Formation permissions for any shared data lake, rather than granting
  broad `s3:GetObject` on the entire underlying bucket to every
  analytics consumer.
- Centralize backup policy through AWS Backup with a dedicated,
  access-restricted backup vault, and test restore procedures on a
  schedule — an untested backup is a liability disguised as a control.

## References and Knowledge Checks

**References**

- [Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) — storage classes, lifecycle, versioning, and
  Object Lock.
- [Amazon RDS, Amazon Aurora, and Amazon DynamoDB documentation.](https://docs.aws.amazon.com/rds/)
- [AWS KMS documentation](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) — key policies, managed vs. customer-managed
  keys, and key rotation.
- [Amazon Redshift, AWS Glue, Amazon Athena, and AWS Lake Formation
  documentation.](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
- [AWS Backup documentation](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html) — backup plans, vaults, and cross-account/
  cross-Region copy.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the data storage, database, and data-protection
  domains of the AWS Certified Solutions Architect and AWS Certified
  Security blueprints.

**Knowledge checks**

1. Why does RDS Multi-AZ not, by itself, solve a read-scaling problem?
2. What must be true of a DynamoDB table's key design before the table is
   created, and why is this different from relational database design?
3. Why can a caller with a fully permissive IAM policy still receive an
   `AccessDeniedException` on a KMS-encrypted resource?
4. What problem does AWS Lake Formation solve that bucket-level S3
   policies alone do not?

## Hands-On Lab

**Objective:** Create an encrypted, versioned S3 bucket with Block Public
Access enforced, apply a lifecycle rule, and confirm that an attempt to
make the bucket public is blocked.

**Cost implications:** S3 storage, KMS customer-managed keys ($1/month
plus per-request charges), and the API calls in this lab are minimal
(pennies at most for a short-lived lab bucket with a handful of small test
objects). Complete cleanup to avoid the ongoing per-month KMS key charge
and any accumulated storage.

**Prerequisites**

- An AWS account with AWS CLI v2 configured and permissions for S3, KMS,
  and IAM.

**Steps**

1. Create a customer-managed KMS key and a bucket:

   ```bash
   KEY_ID=$(aws kms create-key --description "lab-bucket-cmk" \
     --query "KeyMetadata.KeyId" --output text)
   aws kms enable-key-rotation --key-id "$KEY_ID"

   aws s3api create-bucket --bucket lab-data-bucket-$RANDOM --region us-east-1
   ```

   Record the bucket name as `BUCKET`.

2. Enable Block Public Access, versioning, and default encryption:

   ```bash
   aws s3api put-public-access-block --bucket "$BUCKET" \
     --public-access-block-configuration \
     BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

   aws s3api put-bucket-versioning --bucket "$BUCKET" \
     --versioning-configuration Status=Enabled

   aws s3api put-bucket-encryption --bucket "$BUCKET" \
     --server-side-encryption-configuration '{
       "Rules": [{
         "ApplyServerSideEncryptionByDefault": {
           "SSEAlgorithm": "aws:kms",
           "KMSMasterKeyID": "'"$KEY_ID"'"
         }
       }]
     }'
   ```

   **Expected result:** No errors from any of the three calls.

3. Upload a test object and confirm it is encrypted with the CMK:

   ```bash
   echo "lab test object" > test.txt
   aws s3 cp test.txt "s3://$BUCKET/test.txt"
   aws s3api head-object --bucket "$BUCKET" --key test.txt \
     --query "[ServerSideEncryption,SSEKMSKeyId]"
   ```

   **Expected result:** `["aws:kms", "<the KEY_ID's full ARN>"]`.

4. Apply a lifecycle rule transitioning objects to Standard-IA after 30
   days:

   ```bash
   aws s3api put-bucket-lifecycle-configuration --bucket "$BUCKET" \
     --lifecycle-configuration '{
       "Rules": [{
         "ID": "tier-ia",
         "Status": "Enabled",
         "Filter": {},
         "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}]
       }]
     }'

   aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET"
   ```

   **Expected result:** The lifecycle configuration is returned unchanged
   from what was submitted.

5. **Negative test:** Attempt to attach a public-read bucket policy and
   confirm Block Public Access rejects it:

   ```bash
   aws s3api put-bucket-policy --bucket "$BUCKET" --policy '{
     "Version": "2012-10-17",
     "Statement": [{
       "Sid": "PublicRead",
       "Effect": "Allow",
       "Principal": "*",
       "Action": "s3:GetObject",
       "Resource": "arn:aws:s3:::'"$BUCKET"'/*"
     }]
   }'
   ```

   **Expected result:** An `AccessDenied` error stating the action is
   blocked by the bucket's Block Public Access configuration, confirming
   the control prevents accidental public exposure even when a policy
   document explicitly grants it.

6. **Cleanup:**

   ```bash
   aws s3api delete-objects --bucket "$BUCKET" \
     --delete "$(aws s3api list-object-versions --bucket "$BUCKET" \
       --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}')"
   aws s3api delete-bucket --bucket "$BUCKET"
   aws kms schedule-key-deletion --key-id "$KEY_ID" --pending-window-in-days 7
   rm -f test.txt
   ```

   Confirm removal:

   ```bash
   aws s3api head-bucket --bucket "$BUCKET"
   ```

   The command must return a `404 Not Found` error.

## Summary and Completion Checklist

Object, block, and file storage each fit a distinct access pattern — S3
for whole-object HTTP access and archival tiering, EBS for single-instance
block volumes, EFS for POSIX-shared concurrent access — and choosing among
them by access pattern rather than habit avoids expensive rearchitecting.
RDS Multi-AZ, RDS read replicas, and Aurora each solve a different
availability or scaling problem in the relational model, while DynamoDB
trades relational flexibility for predictable, massively scalable
key-based access once access patterns are correctly modeled up front.
Redshift, Glue, Athena, and Lake Formation compose into a governed
analytics pipeline over data at rest in S3. Every layer of this chapter
converges on one control: encryption at rest via KMS, with key policy
evaluated independently of IAM, and centralized backup policy through AWS
Backup to make recovery a tested capability rather than an assumption.

- [ ] Can select the correct storage service (S3, EBS, EFS) for a stated
      access pattern.
- [ ] Can configure S3 Block Public Access, versioning, encryption, and
      lifecycle transitions.
- [ ] Can distinguish RDS Multi-AZ, RDS read replicas, Aurora, and
      DynamoDB use cases.
- [ ] Can explain why KMS key policy is evaluated independently of IAM
      policy.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
