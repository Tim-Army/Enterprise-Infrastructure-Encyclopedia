# Chapter 09: Solutions Architect and Security Training Capstone

![Lab flow for this chapter: the capstone Terraform stack applies cleanly, and posting to the deployed API endpoint writes a database item end to end; a posture-check script reports account guardrail status, storage exposure, detection-service enrollment, and active alarms, flagging any gap honestly, and the workload registers in the Well-Architected Tool with at least one real cost-optimization finding recorded. As a negative test, the Lambda function is invoked with an unsupported action; it is rejected in application logic or denied at the IAM layer, confirming the scoped policy from the individual chapter's lab still blocks anything beyond its granted actions in this fully composed stack.](../../../diagrams/volume-17-aws-architecture-security/chapter-09-capstone-posture-check-iam-boundary-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: the volume's minimal secure serverless capstone stack exercised end to end, audited by a posture-check script, and tested against an out-of-scope Lambda action.*

## Learning Objectives

- Synthesize the account, identity, network, compute, data, reliability,
  observability, and security controls from Chapters 01–08 into a single
  reference architecture.
- Map this volume's chapters to the domain areas of the AWS Certified
  Solutions Architect and AWS Certified Security certification blueprints
  without relying on any single chapter in isolation.
- Build and validate a minimal, secure, end-to-end serverless workload
  that exercises least-privilege IAM, encryption at rest, monitoring, and
  cost guardrails together.
- Run a structured self-assessment against the AWS Well-Architected
  Framework's six pillars for a complete workload.
- Identify the primary study resources and hands-on practice patterns
  appropriate for AWS certification preparation beyond this volume.

## Theory and Architecture

This chapter does not introduce new AWS services. It integrates the
services and controls from Chapters 01 through 08 into one coherent
reference architecture, and maps that architecture back to the
certification blueprints named in
[CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md): the
**AWS Certified Solutions Architect** and **AWS Certified Security**
paths. Consult the official AWS exam guide for the current, authoritative
domain weighting — this chapter describes where each domain area is
covered in this volume, not the proprietary exam content itself.

### A synthesized reference architecture

The following text diagram represents a workload that uses one control
or pattern from every chapter in this volume:

```text
Organization (Ch. 02)
└── Workloads OU → Production account
    ├── Identity: IAM Identity Center permission sets (Ch. 02)
    ├── Network (Ch. 03)
    │   ├── VPC: public/private subnet tiers across 2 AZs
    │   ├── Security groups referencing each other (ALB → app)
    │   ├── Route 53 public hosted zone + failover routing (Ch. 06)
    │   └── CloudFront + AWS WAF in front of the public API
    ├── Compute (Ch. 04)
    │   ├── API Gateway → Lambda (least-privilege execution role)
    │   └── ECS Fargate service behind an ALB (stateful tier)
    ├── Data (Ch. 05)
    │   ├── DynamoDB table (encrypted, point-in-time recovery)
    │   ├── Aurora PostgreSQL cluster (Multi-AZ, encrypted)
    │   └── S3 bucket (versioned, encrypted, Block Public Access)
    ├── Reliability (Ch. 06)
    │   ├── S3 Cross-Region Replication to a DR Region
    │   └── AWS Backup plan covering RDS/DynamoDB/S3
    ├── Observability and cost (Ch. 07)
    │   ├── CloudWatch alarms + composite alarm → SNS
    │   ├── AWS Config conformance pack
    │   └── AWS Budgets guardrail with forecasted-spend alert
    └── Security (Ch. 08)
        ├── GuardDuty + Security Hub (delegated from Security OU)
        ├── EventBridge → Lambda automated containment
        └── Secrets Manager for all database credentials
```

Every arrow and every service in this diagram was built in an earlier
chapter; the capstone lab in this chapter builds a deliberately smaller
slice of it end to end, while this diagram represents the target state a
production implementation of this volume's guidance converges on.

### Mapping this volume to certification domain areas

| Blueprint domain area (both paths, generally stated) | Primary chapters | Supporting chapters |
| --- | --- | --- |
| Secure account and organization design | 02 | 01 |
| Identity and access management | 02 | 04, 08 |
| Resilient, well-architected design | 01, 06 | 03, 05 |
| Networking and connectivity | 03 | 04, 06 |
| Compute and application architecture selection | 04 | 05, 07 |
| Data storage, database selection, and protection | 05 | 06, 08 |
| High availability, DR, and migration | 06 | 03, 05 |
| Monitoring, automation, and cost optimization | 07 | 04, 06 |
| Threat detection, incident response, and data security | 08 | 02, 05 |

**AWS Certified Solutions Architect** weights design and trade-off
judgment across nearly every domain in this table, with particular depth
in compute/storage/database selection (Chapters 04–05), resilient
architecture ([Chapter 06](06-reliability-migration-multi-region-and-disaster-recovery.md)), and cost-aware design ([Chapter 07](07-observability-automation-performance-and-cost-governance.md)).
**AWS Certified Security** weights identity, detection, incident response,
and data protection more heavily, with particular depth in Chapters 02,
05, and 08. Both paths draw on the Well-Architected Framework introduced
in [Chapter 01](01-cloud-foundations-accounts-and-well-architected-design.md) as their underlying design vocabulary — trade-off questions
on either exam are, at their core, Well-Architected pillar trade-off
questions applied to a specific scenario.

### Using the Well-Architected Tool as a capstone self-assessment

[Chapter 01](01-cloud-foundations-accounts-and-well-architected-design.md) introduced the **AWS Well-Architected Tool** for a single
workload review. As a capstone practice, running a full six-pillar review
against a defined workload — ideally the workload built in this chapter's
hands-on lab, or a workload from the reader's own environment — is the
single most representative exercise for both certification paths, because
it forces explicit trade-off reasoning (the same reasoning style tested by
scenario-based certification questions) rather than recall of individual
service facts.

## Design Considerations

- **Treat the certification blueprint as a study map, not a checklist to
  memorize.** Both AWS certification paths test applied judgment in
  scenario form — given a set of constraints, which service or
  configuration best satisfies them — rather than service trivia; the
  deepest preparation is building and breaking the patterns in Chapters
  02 through 08 hands-on, not memorizing service limits.
- **Security and Solutions Architect preparation overlap more than they
  diverge.** A candidate preparing for AWS Certified Security without
  solid Solutions Architect-level networking and compute fundamentals
  (Chapters 03–04) will struggle with scenario questions that embed a
  security decision inside a broader architecture; prepare the
  foundational chapters regardless of which certification is the
  immediate target.
- **A capstone workload should be small enough to fully understand end
  to end.** A minimal serverless workload that the reader personally
  built, broke, and repaired teaches more than a larger workload copied
  from a template without every decision being deliberately made and
  understood.
- **Cost discipline is itself a tested competency, not just a lab
  courtesy.** Both certification paths include cost-optimization
  judgment as a first-class design consideration, not an afterthought;
  practicing deliberate cleanup and budget guardrails (as every lab in
  this volume has required) directly reinforces that competency.
- **Recertification and blueprint drift are expected, not exceptional.**
  AWS certification blueprints and the underlying service surface both
  change over time; treat the dated baseline in
  [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) as a snapshot,
  and always confirm current blueprint domains and weights against the
  official AWS exam guide before using any material — including this
  volume — as final exam preparation.

### A six-to-eight week SAA-C03 study plan

The schedule below sequences this volume against the **AWS Certified
Solutions Architect – Associate (SAA-C03)** blueprint for a reader with
production infrastructure experience who is new to AWS specifically. It
assumes **8–10 hours per week**; at 15 hours it compresses to roughly
four weeks, and a reader without hands-on infrastructure background
should plan closer to twelve.

The exam's scored content divides into four domains:

| Domain | Weight | Where this volume covers it |
| --- | --- | --- |
| 1 — Design Secure Architectures | 30% | [Ch. 02](02-multi-account-identity-governance-and-landing-zones.md), [Ch. 08](08-security-architecture-detection-and-incident-response.md), [Ch. 03](03-secure-networking-hybrid-connectivity-and-edge.md) |
| 2 — Design Resilient Architectures | 26% | [Ch. 06](06-reliability-migration-multi-region-and-disaster-recovery.md), [Ch. 01](01-cloud-foundations-accounts-and-well-architected-design.md) |
| 3 — Design High-Performing Architectures | 24% | [Ch. 04](04-compute-containers-serverless-and-application-architecture.md), [Ch. 05](05-storage-databases-analytics-and-data-protection.md) |
| 4 — Design Cost-Optimized Architectures | 20% | [Ch. 07](07-observability-automation-performance-and-cost-governance.md) |

Weighting is a guide to *exam* emphasis, not to study effort. Effort
should go where the reader's existing knowledge is weakest, which for an
infrastructure engineer is rarely Domain 1's networking content and
frequently Domain 3's managed-service selection.

| Week | Focus | Chapters | Practical work |
| --- | --- | --- | --- |
| 1 | Account structure, IAM, Well-Architected vocabulary | 01, 02 | Build an organization with an SCP guardrail; write one IAM policy from scratch rather than copying |
| 2 | Networking, hybrid connectivity, edge | 03 | VPC with public and private subnets across two AZs; reach it over a VPN or Direct Connect equivalent |
| 3 | Compute and application architecture | 04 | EC2 behind an ALB across two AZs; the same workload again as Lambda plus API Gateway |
| 4 | Storage and database selection | 05 | Exercise S3 classes and lifecycle rules; compare EBS, EFS, and FSx on one workload; contrast RDS with DynamoDB |
| 5 | Resilience, DR, and migration | 06 | Fail an AZ deliberately and observe recovery; write an RTO/RPO statement for the capstone workload |
| 6 | Observability, automation, cost | 07 | Budgets and alarms; price the same workload On-Demand, Reserved, Spot, and Savings Plan |
| 7 | Security architecture and detection | 08 | Enable detection services; run the incident-response walkthrough |
| 8 | Capstone and consolidation | 09 | This chapter's lab and Well-Architected review; re-read weak domains only |

Weeks 7 and 8 are where a six-week schedule compresses: a reader already
strong in security operations can fold Week 7 into Week 6, and Week 8's
consolidation into whatever time remains.

Two habits matter more than the schedule itself. **Build in a sandbox
account rather than reading**, because the exam rewards knowing which
managed service fits a scenario, and that judgment does not survive
passive study. And **track readiness against scenario-style practice
rather than recall**, since the questions are multiple-choice and
multiple-response scenarios, not definitions — consistent scores in the
low-to-mid eighties on realistic practice material is a more reliable
signal than finishing a syllabus.

**Study materials.** This volume is written to stand on its own, but most
candidates pair a video course with a practice-exam bank, and that
combination has a better track record than either alone:

| Role | Resource | Why |
| --- | --- | --- |
| Course spine | Stephane Maarek's SAA-C03 course (Udemy) | Broad service coverage in blueprint order; useful for the services this volume treats only as design inputs |
| Readiness measurement | Tutorials Dojo practice exams (Jon Bonso) | Scenario-style questions with explanations that argue why the distractors are wrong, which is the reasoning the exam tests |
| Hands-on | An AWS free-tier account | Non-negotiable; see the weekly practical work above |
| Official | [AWS Skill Builder](https://skillbuilder.aws/) and the exam guide | Authority on domains, weights, and version — outranks any third-party material where they disagree |

Treat the third-party material as a supplement to building, not a
substitute. A candidate who has watched a full course and scored well on
practice exams without provisioning anything tends to fail on the
scenario questions that hinge on operational detail.

**Exam mechanics, as published in the official guide:** 50 scored
questions plus 15 unscored, a scaled score of 100–1,000 with 720 to pass,
and a compensatory model — a weak domain does not fail the exam provided
the overall score clears the bar. AWS states a target candidate has at
least one year of hands-on AWS design experience. Question count, scoring,
and domain weights come from the SAA-C03 exam guide; **seat time, price,
and exam version are not reproduced here because they change** and are
region-dependent. Confirm all of them, and that SAA-C03 is still the
current version, on the official certification page at registration.

## Implementation and Automation

### 1. A minimal, secure serverless capstone stack (Terraform)

This composes patterns from Chapters 02, 04, 05, 07, and 08 into one
small, low-cost stack: a least-privilege Lambda function behind API
Gateway, an encrypted DynamoDB table, an encrypted and versioned S3 export
bucket, a CloudWatch alarm, and a budget guardrail.

```hcl
resource "aws_dynamodb_table" "notes" {
  name         = "capstone-notes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "note_id"
  attribute {
    name = "note_id"
    type = "S"
  }
  point_in_time_recovery { enabled = true }
  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.capstone.arn
  }
}

resource "aws_s3_bucket" "exports" {
  bucket = "capstone-notes-exports-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_public_access_block" "exports" {
  bucket                  = aws_s3_bucket.exports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "exports" {
  bucket = aws_s3_bucket.exports.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_iam_role" "notes_lambda" {
  name = "capstone-notes-lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "notes_lambda_scoped" {
  name = "scoped-access"
  role = aws_iam_role.notes_lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Scan"]
        Resource = aws_dynamodb_table.notes.arn
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.exports.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_cloudwatch_metric_alarm" "notes_errors" {
  alarm_name          = "capstone-notes-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods   = 1
  metric_name          = "Errors"
  namespace            = "AWS/Lambda"
  period               = 60
  statistic            = "Sum"
  threshold            = 0
  alarm_actions        = [aws_sns_topic.capstone_alerts.arn]
  dimensions = {
    FunctionName = aws_lambda_function.notes.function_name
  }
}
```

### 2. A cross-chapter posture-check script

A capstone-appropriate automation confirms several chapters' controls are
simultaneously in place — a lightweight version of what a real platform
team scripts as a recurring compliance check:

```bash
#!/usr/bin/env bash
# posture-check.sh — cross-chapter guardrail verification (read-only)
set -euo pipefail

echo "== Chapter 02: Organizations feature set =="
aws organizations describe-organization --query "Organization.FeatureSet" --output text

echo "== Chapter 05: S3 buckets with Block Public Access NOT fully enabled =="
for bucket in $(aws s3api list-buckets --query "Buckets[].Name" --output text); do
  status=$(aws s3api get-public-access-block --bucket "$bucket" \
    --query "PublicAccessBlockConfiguration.[BlockPublicAcls,BlockPublicPolicy,IgnorePublicAcls,RestrictPublicBuckets]" \
    --output text 2>/dev/null || echo "NOT_SET")
  if [[ "$status" != $'True\tTrue\tTrue\tTrue' ]]; then
    echo "  GAP: $bucket -> $status"
  fi
done

echo "== Chapter 08: GuardDuty enabled in this Region? =="
aws guardduty list-detectors --query "DetectorIds" --output text

echo "== Chapter 08: Security Hub enabled in this Region? =="
aws securityhub describe-hub --query "HubArn" --output text 2>/dev/null || echo "  GAP: Security Hub not enabled"

echo "== Chapter 07: Active CloudWatch alarms currently in ALARM state =="
aws cloudwatch describe-alarms --state-value ALARM --query "MetricAlarms[].AlarmName" --output text
```

## Validation and Troubleshooting

- **Reconciling conflicting design guidance across chapters.** A scenario
  that seems to call for both a centralized egress VPC ([Chapter 03](03-secure-networking-hybrid-connectivity-and-edge.md), for
  cost and inspection) and per-account NAT gateways (for account
  isolation) is a Well-Architected trade-off, not a contradiction —
  resolve it by asking which pillar the specific requirement optimizes
  for (cost/operational simplicity vs. blast-radius isolation) and state
  the trade-off explicitly, the same reasoning pattern certification
  scenario questions expect.
- **Posture-check script reports a false gap.** Confirm the script is
  running with credentials that have read access across every relevant
  service in the account/Region being checked; a permissions gap in the
  checking role, not an actual control gap, is a common cause of
  unexpected script output — validate with `aws sts get-caller-identity`
  and a targeted `iam simulate-principal-policy` call before trusting a
  reported finding.
- **Well-Architected Tool review answers do not match the built
  architecture.** If a pillar question's answer seems to require a
  service not present in the reviewed workload, that mismatch is itself
  the finding — record it as an improvement item rather than answering
  inaccurately to make the review look complete.
- **Capstone Lambda function times out on cold start under a VPC
  configuration.** If the capstone stack is extended into a VPC for
  private RDS/Aurora access, confirm ENI provisioning latency
  ([Chapter 04](04-compute-containers-serverless-and-application-architecture.md)) is accounted for in the function's configured timeout, or
  use RDS Proxy to reduce connection-establishment overhead.

## Security and Best Practices

- Apply every guardrail from Chapters 02–08 to a capstone or practice
  workload exactly as it would be applied in production — practicing
  shortcuts (broad IAM policies, disabled encryption, public buckets)
  "just for the lab" builds the wrong muscle memory for both
  certification scenarios and real operational work.
- Treat the cross-chapter posture-check pattern as a template for a real
  recurring compliance job (a scheduled Lambda function or Config
  conformance pack, per [Chapter 07](07-observability-automation-performance-and-cost-governance.md)), not a one-time manual script.
- Use a dedicated sandbox account ([Chapter 02](02-multi-account-identity-governance-and-landing-zones.md)'s Sandbox OU) for
  certification practice and capstone experimentation, never a shared
  production account, and apply the same Region-restriction and
  cost-guardrail SCPs used elsewhere in the Organization.
- When in doubt on a design trade-off, default to the more restrictive/
  secure option and document why a less restrictive option was
  ultimately chosen if it was — this is both sound security practice and
  the reasoning style rewarded on the AWS Certified Security exam.

## References and Knowledge Checks

**References**

- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  the authoritative pointer to AWS Training and Certification for current
  blueprint domains and weighting for both paths.
- [AWS Well-Architected Framework whitepaper and Well-Architected Tool](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) —
  the design vocabulary underlying both certification paths.
- [AWS Training and Certification official exam guides for AWS Certified
  Solutions Architect and AWS Certified Security](https://docs.aws.amazon.com/aws-certification/latest/examguides/aws-certification-exam-guides.html) — confirm current domain
  weighting directly from AWS before using any third-party material,
  including this volume, as final exam preparation.
- [AWS Skill Builder](https://skillbuilder.aws/) — official AWS digital training, including free
  digital courses and exam-readiness content for both certification
  paths.
- Chapters 01–08 of this volume — the primary reference material this
  capstone synthesizes.

**Knowledge checks**

1. Explain, in Well-Architected pillar terms, the trade-off between a
   centralized egress VPC and per-account NAT gateways introduced in
   [Chapter 03](03-secure-networking-hybrid-connectivity-and-edge.md).
2. Which chapters in this volume most directly support AWS Certified
   Security preparation, and why do they still depend on the networking
   and compute chapters?
3. Why is a scenario-based exam question better prepared for by building
   and breaking a pattern hands-on than by memorizing a service feature
   list?
4. What should a candidate do if a Well-Architected Tool review question
   seems to require a control the reviewed workload does not have?

## Hands-On Lab

**Objective:** Build the minimal secure serverless capstone stack (Lambda,
DynamoDB, S3, CloudWatch alarm), exercise it end to end, run the
cross-chapter posture-check script against the account, and register the
workload in the Well-Architected Tool for a lightweight pillar review.

**Cost implications:** This lab uses Lambda, API Gateway (HTTP API),
DynamoDB (on-demand), S3, CloudWatch, SNS, KMS (one customer-managed key,
approximately $1/month if not cleaned up), and the free Well-Architected
Tool. Total cost for the lab's duration is a few cents at most. Complete
cleanup, particularly the KMS key deletion, to avoid the recurring
per-month key charge.

**Prerequisites**

- An AWS account (sandbox recommended) with AWS CLI v2 and Terraform
  1.9.x configured, and permissions across Lambda, API Gateway, DynamoDB,
  S3, KMS, CloudWatch, SNS, GuardDuty, Security Hub, and
  Well-Architected Tool actions.
- Completion of, or familiarity with, the hands-on labs in Chapters 04,
  05, 07, and 08, whose patterns this lab composes.

**Steps**

1. Apply the capstone Terraform from the Implementation section above
   (adapting the Lambda function code from [Chapter 04](04-compute-containers-serverless-and-application-architecture.md)'s lab), and confirm
   all resources were created:

   ```bash
   terraform init
   terraform apply
   terraform output
   ```

   **Expected result:** Terraform reports `Apply complete` with no
   errors, and outputs include the API endpoint URL.

2. Exercise the deployed API to confirm the end-to-end path works:

   ```bash
   curl -s -X POST "$(terraform output -raw api_endpoint)/notes" \
     -d '{"text": "capstone lab test note"}'
   aws dynamodb scan --table-name capstone-notes --select COUNT
   ```

   **Expected result:** A successful response, and a DynamoDB item count
   of at least 1.

3. Save the posture-check script from the Implementation section as
   `posture-check.sh`, make it executable, and run it:

   ```bash
   chmod +x posture-check.sh
   ./posture-check.sh
   ```

   **Expected result:** Output covering Organizations feature set, S3
   Block Public Access status for every bucket (the capstone bucket
   should show no gap), GuardDuty/Security Hub enrollment status, and any
   active CloudWatch alarms. Any `GAP:` line identifies a control this
   volume covers that is not yet applied in the account being checked.

4. Register the capstone workload in the Well-Architected Tool and
   answer at least the Security and Cost Optimization pillar questions:

   ```bash
   aws wellarchitected create-workload \
     --workload-name "capstone-notes-api" \
     --description "Volume XVII capstone lab workload" \
     --environment PREPRODUCTION \
     --aws-regions "$(aws configure get region)" \
     --lenses "wellarchitected" \
     --review-owner "YOUR_EMAIL@example.com"
   ```

   **Expected result:** A `WorkloadId` is returned; use it to answer
   pillar questions via the console or `aws wellarchitected
   update-answer` and confirm at least one improvement item is recorded
   for the Cost Optimization pillar (a real, honest finding — for
   example, "no Savings Plan analysis has been performed for this
   workload" — is expected and correct for a small lab workload).

5. **Negative test:** Attempt an action the Lambda execution role does
   not permit, confirming the least-privilege boundary from [Chapter 04](04-compute-containers-serverless-and-application-architecture.md)
   still holds in this composed stack:

   ```bash
   aws lambda invoke --function-name "$(terraform output -raw lambda_function_name)" \
     --payload '{"action": "delete_table"}' response.json
   cat response.json
   ```

   **Expected result:** The function either rejects the unsupported
   action in application logic or, if the code path attempted a
   `dynamodb:DeleteTable` call, an `AccessDeniedException` in the
   function's CloudWatch Logs — confirming the scoped IAM policy from
   step 1 blocks an action beyond `PutItem`/`GetItem`/`Scan` regardless
   of what the application code attempts.

6. **Cleanup:**

   ```bash
   aws wellarchitected delete-workload --workload-id <WORKLOAD_ID>
   terraform destroy
   rm -f response.json posture-check.sh
   ```

   Confirm removal:

   ```bash
   aws dynamodb describe-table --table-name capstone-notes
   ```

   The command must return a `ResourceNotFoundException`. Confirm the
   customer-managed KMS key shows `PendingDeletion` state rather than
   remaining `Enabled`:

   ```bash
   aws kms describe-key --key-id "$(terraform output -raw kms_key_id)" \
     --query "KeyMetadata.KeyState"
   ```

## Summary and Completion Checklist

This chapter did not add a new AWS service to the volume; it integrated
the account, identity, network, compute, data, reliability, observability,
and security controls from Chapters 01 through 08 into one reference
architecture and one hands-on capstone stack, and mapped that material to
the AWS Certified Solutions Architect and AWS Certified Security
certification paths. Both certifications reward the same underlying
skill this volume has built chapter by chapter: applying Well-Architected
trade-off reasoning to a concrete scenario, not recalling isolated service
facts. The capstone lab's least-privilege IAM, encryption at rest,
monitoring, and cost guardrails are not lab conveniences — they are the
same controls a production implementation of this volume requires, built
at a scale a reader can fully understand end to end.

- [ ] Can describe the end-to-end reference architecture synthesizing
      Chapters 01–08.
- [ ] Can map this volume's chapters to the general domain areas of both
      certification paths and knows where to find the authoritative,
      current blueprint.
- [ ] Built and validated the minimal secure serverless capstone stack.
- [ ] Ran a Well-Architected Tool review against the capstone workload
      and recorded at least one honest improvement item.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
