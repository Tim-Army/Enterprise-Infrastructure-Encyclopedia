# Chapter 07: Observability, Automation, Performance, and Cost Governance

![Lab flow for this chapter: an alarm on a custom metric transitions to ALARM after two consecutive above-threshold data points are published, and an SNS email notification arrives. As a negative test, two data points back under the threshold are published; the alarm returns to OK and a second SNS notification confirms the recovery — proving the alarm evaluates the metric bidirectionally rather than latching in the ALARM state once triggered.](../../../diagrams/volume-17-aws-architecture-security/chapter-07-cloudwatch-alarm-bidirectional-flow.svg)

*Figure 7-1. Flow used throughout this chapter's Hands-On Lab: a CloudWatch alarm on a custom metric firing and clearing through SNS, tested for bidirectional (non-latching) behavior.*

## Learning Objectives

- Configure Amazon CloudWatch metrics, alarms, dashboards, and log
  aggregation for a multi-service application.
- Trace a distributed request across services using AWS X-Ray.
- Use AWS Config and Config conformance packs to detect and remediate
  configuration drift against a defined baseline.
- Operate AWS Systems Manager Automation, Patch Manager, and Session
  Manager as the standard patching and access pattern for EC2 fleets.
- Apply AWS Cost Explorer, AWS Budgets, and AWS Compute Optimizer to
  govern and reduce cloud spend without degrading reliability.
- Design a tagging strategy that supports cost allocation, automation
  targeting, and access control simultaneously.

## Theory and Architecture

Observability and automation are the operational layer that makes every
architecture from the preceding chapters sustainable at scale — a workload
that is correctly designed but unobserved and unpatched degrades into an
incident regardless of its initial architecture quality.

### Amazon CloudWatch: metrics, logs, alarms, dashboards

**Amazon CloudWatch** is AWS's native observability service, built around
four primitives:

- **Metrics** — numeric time-series data, either published automatically
  by AWS services (EC2 CPU utilization, ALB request count) or as **custom
  metrics** published by application code via `PutMetricData`. Metrics
  are stored per namespace/dimension combination at configurable
  resolution (standard, one-minute; or high-resolution, down to one
  second).
- **Logs** — CloudWatch Logs ingests log data from EC2 (via the
  CloudWatch agent), Lambda, ECS, and most managed services into **log
  groups**, each with a configurable retention period. **CloudWatch Logs
  Insights** provides a purpose-built query language for ad hoc log
  analysis without exporting data to a separate system.
- **Alarms** — evaluate a metric against a threshold over a defined
  number of periods and change state (`OK`, `ALARM`, `INSUFFICIENT_DATA`),
  triggering an action such as an SNS notification, an Auto Scaling
  policy, or a Systems Manager Automation runbook. A **composite alarm**
  combines multiple underlying alarms with Boolean logic, reducing alert
  noise from correlated failures.
- **Dashboards** — customizable visual layouts combining metrics, logs
  widgets, and alarm status into a single operational view, definable as
  code (JSON) for version control alongside infrastructure.

### AWS X-Ray and distributed tracing

**AWS X-Ray** traces a request as it moves across service boundaries —
API Gateway, Lambda, ECS, downstream HTTP calls — assembling a **service
map** and per-request **trace** showing latency contribution at each hop.
This is the tool that answers "which specific downstream call made this
request slow," a question aggregate metrics alone cannot answer once an
architecture spans more than a couple of services, which is the norm for
the compute patterns in [Chapter 04](04-compute-containers-serverless-and-application-architecture.md).

### AWS Config and conformance packs

**AWS Config** continuously records configuration changes to supported
resource types and evaluates them against **Config rules** — AWS managed
rules (for example, `s3-bucket-public-read-prohibited`), or custom rules
backed by a Lambda function. A **conformance pack** bundles a set of Config
rules and remediation actions as a single deployable, version-controlled
unit, commonly deployed organization-wide via Config's multi-account,
multi-Region aggregation and Organizations integration — the detective
counterpart to the preventive SCP guardrails from [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md). Where a Config
rule identifies a `NON_COMPLIANT` resource, an associated **remediation
action** (a Systems Manager Automation document) can correct it
automatically or require manual approval, depending on the guardrail's
risk tolerance.

### AWS Systems Manager

**AWS Systems Manager** is AWS's operational management hub for managed
instances (EC2 and, via the hybrid activation model, on-premises servers):

- **Session Manager** provides interactive shell access to an instance
  without an open inbound SSH/RDP port, a bastion host, or a stored SSH
  key — access is instead governed entirely by IAM policy and logged to
  CloudWatch Logs/S3, directly reducing the network attack surface
  established in [Chapter 03](03-secure-networking-hybrid-connectivity-and-edge.md).
- **Patch Manager** automates OS and application patch compliance
  against a defined **patch baseline** (approved patch classifications and
  an auto-approval delay), scanning and installing patches during defined
  **maintenance windows**.
- **Automation** runs multi-step operational runbooks (AWS-provided or
  custom SSM documents) — for example, an automated remediation triggered
  by a Config rule violation, or a scheduled AMI-refresh pipeline.
- **Parameter Store** holds configuration values and (in its advanced
  tier or paired with Secrets Manager) secrets, referenced by
  applications and IaC without hardcoding values into source.

### Infrastructure as code: CloudFormation and Terraform

**AWS CloudFormation** is AWS's native IaC service, applying a declarative
template to create/update/delete a **stack** of resources as a unit, with
built-in rollback on failure and drift detection against the last known
template state. **Terraform**, used throughout this volume, achieves the
same declarative, plan-then-apply model through the AWS provider, with the
advantage of a single multi-cloud-capable tool and state-file-based drift
tracking, at the cost of managing state storage and locking (typically an
S3 backend with DynamoDB state locking) as an explicit operational
concern that CloudFormation does not require.

### Cost governance

- **AWS Cost Explorer** visualizes historical and forecasted spend,
  filterable and groupable by service, linked account, and cost
  allocation tag.
- **AWS Budgets** (introduced in [Chapter 01](01-cloud-foundations-accounts-and-well-architected-design.md) for account-level guardrails)
  scales to org-wide budgets with configurable alert thresholds and,
  through **budget actions**, can automatically apply a restrictive IAM
  policy or stop specific resources when a threshold is breached.
- **AWS Compute Optimizer** analyzes historical utilization (CPU, memory
  where the CloudWatch agent is installed, network) and recommends
  right-sized EC2 instance types, EBS volume configurations, and Lambda
  memory settings — a data-driven alternative to guessing at instance
  sizing.
- **AWS Trusted Advisor** checks across cost optimization, performance,
  security, fault tolerance, and service limits, with the depth of checks
  available scaling with the AWS Support plan tier.
- **Savings Plans and Reserved Instances** commit to a consistent amount
  of compute usage (Savings Plans, flexible across instance family/
  Region) or a specific instance configuration (Reserved Instances) in
  exchange for a significant discount over On-Demand pricing, appropriate
  once a workload's baseline steady-state usage is well understood.

## Design Considerations

- **Alarm on symptoms customers feel, not just resource metrics.** CPU
  utilization crossing 80% is not itself a customer-facing problem;
  pairing resource-level alarms with request-level SLO alarms (error
  rate, p99 latency) keeps the team focused on what actually matters to
  the business, and composite alarms reduce noise from a single root
  cause triggering many correlated resource alarms simultaneously.
- **Log retention is a cost and compliance trade-off, set deliberately
  per log group.** Indefinite retention on high-volume log groups
  (VPC Flow Logs, ALB access logs) accumulates significant CloudWatch
  Logs storage cost; export older logs to S3 (with lifecycle transitions
  from [Chapter 05](05-storage-databases-analytics-and-data-protection.md)) for cheaper long-term retention where compliance
  requires it, rather than leaving every log group at the default
  "never expire" setting.
- **Config rules should map to actual guardrails, not just available
  managed rules.** Enabling every AWS managed Config rule produces a
  compliance dashboard full of findings nobody is accountable for
  remediating; select and prioritize rules that map to real
  organizational policy, and pair each with an owned remediation path.
- **Session Manager changes the security perimeter, not just the access
  method.** Removing inbound SSH/RDP access entirely is only a net
  security improvement if the IAM policies governing Session Manager
  access are themselves tightly scoped — a broad `ssm:StartSession` grant
  recreates the same exposure in a different form.
- **CloudFormation vs. Terraform is a team/ecosystem decision.**
  CloudFormation avoids external state management and integrates
  natively with StackSets for multi-account deployment; Terraform offers
  a single tool across cloud and non-cloud resources and a larger
  third-party module ecosystem. Standardize on one per team/organization
  rather than mixing both for the same resource, which produces drift and
  ownership ambiguity.
- **Tagging strategy must be enforced, not just documented.** A tagging
  standard that exists only as a wiki page decays quickly; enforce
  required tags at resource creation via SCPs (`aws:RequestTag`
  conditions), Config rules (`required-tags`), or Service Catalog, so
  cost allocation and automation targeting remain reliable.
- **Savings Plans/Reserved Instance commitments should follow measured
  usage, not forecasted usage.** Committing based on an optimistic growth
  forecast before the baseline is established risks paying for unused
  committed capacity; layer commitments in as steady-state usage is
  actually observed via Cost Explorer.

## Implementation and Automation

### 1. CloudWatch alarm with SNS notification (Terraform)

```hcl
resource "aws_sns_topic" "alerts" {
  name = "app-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "secops@example.com"
}

resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "app-5xx-error-rate-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods   = 3
  metric_name          = "HTTPCode_Target_5XX_Count"
  namespace            = "AWS/ApplicationELB"
  period               = 60
  statistic            = "Sum"
  threshold            = 10
  alarm_actions        = [aws_sns_topic.alerts.arn]
  ok_actions           = [aws_sns_topic.alerts.arn]
  dimensions = {
    LoadBalancer = aws_lb.app.arn_suffix
  }
}

resource "aws_cloudwatch_composite_alarm" "app_health" {
  alarm_name = "app-overall-health"
  alarm_rule = "ALARM(${aws_cloudwatch_metric_alarm.high_error_rate.alarm_name}) OR ALARM(${aws_cloudwatch_metric_alarm.high_latency.alarm_name})"
  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

### 2. AWS Config rule and remediation

```hcl
resource "aws_config_config_rule" "s3_public_read" {
  name = "s3-bucket-public-read-prohibited"
  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }
}

resource "aws_config_remediation_configuration" "s3_public_read_fix" {
  config_rule_name = aws_config_config_rule.s3_public_read.name
  target_type      = "SSM_DOCUMENT"
  target_id        = "AWSConfigRemediation-RemoveS3BucketPublicReadAccess"
  parameter {
    name           = "AutomationAssumeRole"
    static_value   = aws_iam_role.config_remediation.arn
  }
  parameter {
    name                = "S3BucketName"
    resource_value      = "RESOURCE_ID"
  }
  automatic             = true
  maximum_automatic_attempts = 3
}
```

### 3. Systems Manager Patch Manager baseline and maintenance window

```bash
aws ssm create-patch-baseline \
  --name "prod-linux-baseline" \
  --operating-system AMAZON_LINUX_2023 \
  --approval-rules '{
    "PatchRules": [{
      "PatchFilterGroup": {"PatchFilters": [{"Key": "CLASSIFICATION", "Values": ["Security"]}]},
      "ApproveAfterDays": 3,
      "ComplianceLevel": "CRITICAL"
    }]
  }'

aws ssm create-maintenance-window \
  --name "weekly-patch-window" \
  --schedule "cron(0 3 ? * SUN *)" \
  --duration 4 --cutoff 1 --allow-unassociated-targets
```

### 4. X-Ray tracing enabled on a Lambda function

```hcl
resource "aws_lambda_function" "orders" {
  # ...prior configuration from Chapter 04...
  tracing_config {
    mode = "Active"
  }
}

resource "aws_iam_role_policy_attachment" "xray_write" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}
```

### 5. Tagging enforcement via SCP and Config

```hcl
data "aws_iam_policy_document" "require_tags_scp" {
  statement {
    sid    = "DenyEC2CreateWithoutOwnerTag"
    effect = "Deny"
    actions = ["ec2:RunInstances"]
    resources = ["arn:aws:ec2:*:*:instance/*"]
    condition {
      test     = "Null"
      variable = "aws:RequestTag/owner"
      values   = ["true"]
    }
  }
}
```

```bash
aws budgets create-budget --account-id 111122223333 --budget '{
  "BudgetName": "org-monthly-guardrail",
  "BudgetLimit": {"Amount": "50000", "Unit": "USD"},
  "TimeUnit": "MONTHLY", "BudgetType": "COST",
  "CostFilters": {"TagKeyValue": ["user:environment$production"]}
}' --notifications-with-subscribers '[{
  "Notification": {"NotificationType": "FORECASTED", "ComparisonOperator": "GREATER_THAN", "Threshold": 90},
  "Subscribers": [{"SubscriptionType": "SNS", "Address": "arn:aws:sns:us-east-1:111122223333:budget-alerts"}]
}]'
```

## Validation and Troubleshooting

- **Alarm not firing despite the underlying condition being true.**
  Confirm the alarm's `evaluation_periods`/`period` combination actually
  matches the metric's publish interval — a five-minute-period alarm
  cannot react faster than five minutes, and a metric published only
  under load (no data point when idle) can leave an alarm in
  `INSUFFICIENT_DATA` rather than `OK`, which some notification
  configurations do not treat the same as a resolved alarm.
- **CloudWatch Logs Insights query returns no results.** Confirm the
  query's time range aligns with actual log ingestion timestamps (not
  the log event's embedded application timestamp, unless the log group
  uses a custom timestamp parser) and that the log group name is exact —
  a common failure is querying the wrong Region's log group when a
  multi-Region deployment shares a naming convention.
- **Config rule stuck in `INSUFFICIENT_DATA`.** This means Config has not
  yet received a configuration item for an in-scope resource type; verify
  the Config recorder's resource type scope actually includes the
  resource type the rule evaluates, using `aws configservice
  describe-configuration-recorder-status`.
- **Session Manager session fails to start.** `aws ssm
  describe-instance-information` confirms the instance is
  `PingStatus: Online`; a missing SSM Agent, an instance profile lacking
  the `AmazonSSMManagedInstanceCore` policy, or no route to the
  `ssm`/`ssmmessages`/`ec2messages` VPC endpoints (or NAT gateway) from a
  private subnet are the three most common root causes.
- **Patch Manager compliance shows `NON_COMPLIANT` after a successful
  patch run.** Compliance is evaluated against the patch baseline's
  approval rules at scan time; a patch released after the last scan, or
  a patch excluded by the approval delay window, produces a
  `NON_COMPLIANT` state that is expected and will clear on the next
  scheduled scan/patch cycle rather than indicating a failure.
- **Common failure: Terraform state drift after a manual console
  change.** `terraform plan` showing unexpected changes on unmodified
  code almost always indicates someone changed a resource directly in
  the console; import or revert the manual change, and restrict console
  write access to IaC-managed resources via SCP or permission boundary
  where feasible.

## Security and Best Practices

- Restrict Session Manager access with IAM policies scoped to specific
  instance tags or resource ARNs, and enable session logging to a
  centralized, access-restricted CloudWatch Logs group or S3 bucket for
  audit purposes.
- Treat AWS Config's recorder and rules the same as CloudTrail from
  [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md) — deploy organization-wide via Config's Organizations
  aggregator, and protect the delivery channel/S3 bucket from
  workload-account tampering.
- Apply patch baselines with security classification auto-approval on a
  short, deliberate delay (days, not months) to balance patch
  regression risk against exposure window, and track patch compliance
  as a reportable operational metric.
- Store Terraform state in an encrypted S3 backend with DynamoDB state
  locking and versioning enabled, and restrict write access to the CI/CD
  pipeline's federated role rather than individual engineer credentials —
  consistent with the plan/apply separation principle from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md).
- Alert on budget thresholds using forecasted, not only actual, spend so
  a runaway cost trend triggers investigation before the money is
  actually spent, not after.
- Require the tagging standard's mandatory tags (`owner`, `environment`,
  `cost-center` at minimum) at resource creation via SCP condition keys
  rather than relying on after-the-fact tag compliance reporting alone.

## References and Knowledge Checks

**References**

- [Amazon CloudWatch documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) — metrics, alarms, Logs Insights, and
  composite alarms.
- [AWS X-Ray documentation](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html) — distributed tracing and service maps.
- [AWS Config documentation](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html) — rules, conformance packs, and remediation.
- [AWS Systems Manager documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html) — Session Manager, Patch Manager, and
  Automation.
- [AWS Cost Management documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html) — Cost Explorer, Budgets, Compute
  Optimizer, and Savings Plans.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the operational excellence, monitoring, and cost-
  optimization domains of the AWS Certified Solutions Architect
  blueprint.

**Knowledge checks**

1. Why should alarms be defined on customer-facing SLO metrics in
   addition to resource-utilization metrics?
2. What is the relationship between an AWS Config rule and a remediation
   action, and why should automatic remediation be applied selectively?
3. Why does removing inbound SSH/RDP access in favor of Session Manager
   only improve security if the corresponding IAM policy is also tightly
   scoped?
4. Name two mechanisms that can enforce a mandatory tagging standard at
   resource-creation time rather than relying on after-the-fact
   reporting.

## Hands-On Lab

**Objective:** Create a CloudWatch alarm on a custom metric, trigger it
with a manually published data point, confirm the SNS notification
fires, and confirm the alarm returns to `OK` when the condition clears.

**Cost implications:** CloudWatch custom metrics, alarms, and SNS
notifications are low-cost (a fraction of a cent for this lab's volume),
well within typical free-tier allowances. No compute resources are
required. Complete cleanup to avoid the small recurring alarm/metric
charge beyond the free tier.

**Prerequisites**

- An AWS account with AWS CLI v2 configured and permissions for
  CloudWatch and SNS.
- An email address able to receive an SNS subscription confirmation.

**Steps**

1. Create an SNS topic and subscribe an email address:

   ```bash
   TOPIC_ARN=$(aws sns create-topic --name lab-alerts --query "TopicArn" --output text)
   aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email \
     --notification-endpoint YOUR_EMAIL@example.com
   ```

   Confirm the subscription from the email AWS sends before continuing.

2. Create an alarm on a custom metric namespace:

   ```bash
   aws cloudwatch put-metric-alarm \
     --alarm-name lab-queue-depth-high \
     --namespace "Lab/App" --metric-name QueueDepth \
     --statistic Average --period 60 --evaluation-periods 2 \
     --threshold 100 --comparison-operator GreaterThanThreshold \
     --alarm-actions "$TOPIC_ARN" --ok-actions "$TOPIC_ARN" \
     --treat-missing-data notBreaching
   ```

3. Confirm the alarm starts in `OK` or `INSUFFICIENT_DATA` state:

   ```bash
   aws cloudwatch describe-alarms --alarm-names lab-queue-depth-high \
     --query "MetricAlarms[0].StateValue"
   ```

4. Publish data points above the threshold for two consecutive periods:

   ```bash
   aws cloudwatch put-metric-data --namespace "Lab/App" \
     --metric-name QueueDepth --value 150
   sleep 70
   aws cloudwatch put-metric-data --namespace "Lab/App" \
     --metric-name QueueDepth --value 175
   sleep 70
   aws cloudwatch describe-alarms --alarm-names lab-queue-depth-high \
     --query "MetricAlarms[0].StateValue"
   ```

   **Expected result:** `"ALARM"`, and an email notification arrives from
   the SNS subscription.

5. **Negative test:** Publish a data point back under the threshold and
   confirm the alarm clears rather than staying latched:

   ```bash
   aws cloudwatch put-metric-data --namespace "Lab/App" \
     --metric-name QueueDepth --value 10
   sleep 70
   aws cloudwatch put-metric-data --namespace "Lab/App" \
     --metric-name QueueDepth --value 5
   sleep 70
   aws cloudwatch describe-alarms --alarm-names lab-queue-depth-high \
     --query "MetricAlarms[0].StateValue"
   ```

   **Expected result:** `"OK"`, and a second SNS notification confirming
   the alarm recovered, proving the alarm is not one-directional.

6. **Cleanup:**

   ```bash
   aws cloudwatch delete-alarms --alarm-names lab-queue-depth-high
   aws sns delete-topic --topic-arn "$TOPIC_ARN"
   ```

   Confirm removal:

   ```bash
   aws cloudwatch describe-alarms --alarm-names lab-queue-depth-high \
     --query "MetricAlarms"
   ```

   The query must return an empty list. Custom metric data points expire
   automatically per CloudWatch's retention schedule and require no
   separate deletion.

## Summary and Completion Checklist

CloudWatch metrics, logs, alarms, and dashboards form the core
observability layer, with X-Ray extending visibility across service
boundaries for distributed architectures. AWS Config and conformance
packs provide the detective counterpart to the preventive SCP guardrails
from [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md), and Systems Manager standardizes patching and access
without exposing inbound management ports. CloudFormation and Terraform
both express infrastructure declaratively, and the choice between them is
an organizational standardization decision rather than a technical
correctness one. Cost governance — Cost Explorer, Budgets, Compute
Optimizer, and a consistently enforced tagging standard — turns spend from
a monthly surprise into a continuously visible and actionable signal.

- [ ] Can configure a CloudWatch alarm with SNS notification and explain
      composite alarms' purpose.
- [ ] Can explain how an AWS Config rule and remediation action work
      together.
- [ ] Can configure Session Manager access without inbound management
      ports.
- [ ] Can name at least three cost governance tools and their distinct
      purposes.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
