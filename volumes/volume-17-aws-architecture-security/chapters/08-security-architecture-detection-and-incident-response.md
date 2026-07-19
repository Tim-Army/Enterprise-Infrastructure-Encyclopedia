# Chapter 08: Security Architecture, Detection, and Incident Response

## Learning Objectives

- Enable and interpret Amazon GuardDuty findings across account,
  workload, and data-plane threat categories.
- Aggregate findings from GuardDuty, Amazon Inspector, and Amazon Macie
  in AWS Security Hub against a defined security standard.
- Build an automated detection-to-response pipeline using Amazon
  EventBridge, AWS Step Functions, and AWS Lambda.
- Apply AWS Secrets Manager and AWS KMS as the credential- and
  encryption-key-management foundation for incident containment.
- Describe the phases of an AWS-specific incident response process and
  the forensic evidence-preservation steps unique to a cloud environment.
- Query CloudTrail Lake for investigative evidence during an incident.

## Theory and Architecture

[Chapter 02](02-multi-account-identity-governance-and-landing-zones.md) established preventive controls (SCPs, IAM boundaries) and
[Chapter 03](03-secure-networking-hybrid-connectivity-and-edge.md) established network-layer controls (security groups, WAF,
Shield). This chapter completes the security architecture with
**detective controls** — services that identify when a preventive control
was bypassed or did not exist — and the **incident response** processes
that act on what they find.

### Amazon GuardDuty

**Amazon GuardDuty** is a managed threat-detection service that
continuously analyzes VPC Flow Logs, DNS query logs, CloudTrail management
and data events, and (with optional protection plans enabled) EKS audit
logs, S3 data-plane events, RDS login activity, and Lambda network
activity — without the customer deploying or managing any agent or sensor.
GuardDuty findings are categorized by threat type and resource, each
carrying a severity score:

| Finding category (examples) | Signal |
| --- | --- |
| `UnauthorizedAccess:EC2/SSHBruteForce` | Network-layer brute-force pattern against an instance |
| `CryptoCurrency:EC2/BitcoinTool.B!DNS` | DNS query to a known cryptocurrency-mining domain |
| `Recon:IAMUser/MaliciousIPCaller` | API reconnaissance activity from a known-malicious IP |
| `Exfiltration:S3/ObjectRead.Unusual` | Anomalous S3 data access pattern (S3 Protection) |
| `Persistence:IAMUser/AnomalousBehavior` | Unusual IAM persistence-oriented API activity |

GuardDuty is enabled per Region and centrally administered across an
Organization through a **delegated administrator** account (typically the
security-tooling account from [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md)'s Security OU), which
automatically enrolls new member accounts and provides a single
organization-wide findings view.

### Amazon Inspector and Amazon Macie

**Amazon Inspector** continuously scans EC2 instances (via SSM Agent, no
separate deployment needed), container images in ECR, and Lambda
functions for known software vulnerabilities (CVEs) and network
reachability issues, replacing point-in-time vulnerability scans with
continuous, automatically triggered reassessment on code or dependency
change. **Amazon Macie** uses machine learning and pattern matching to
discover and classify sensitive data (PII, credentials, financial data) in
S3, flagging both the presence of sensitive data and any bucket
configuration that leaves it overexposed — the S3-focused counterpart to
Inspector's compute-focused scanning.

### AWS Security Hub

**AWS Security Hub** aggregates findings from GuardDuty, Inspector, Macie,
AWS Config, IAM Access Analyzer, and integrated third-party tools into a
single normalized format (AWS Security Finding Format, ASFF), then scores
the account/organization against selectable **security standards** — most
commonly the **AWS Foundational Security Best Practices** standard and the
**CIS AWS Foundations Benchmark**. Like GuardDuty, Security Hub supports
organization-wide delegated administration, giving the security-tooling
account a consolidated, cross-account compliance and findings view rather
than requiring a security analyst to check each account individually.

### Automated detection-to-response

Detection has limited value without a fast, consistent response. The
standard AWS pattern chains three services:

1. **Amazon EventBridge** rule matches a GuardDuty finding (or a Security
   Hub finding, Config rule change, or CloudTrail event) by pattern.
2. The rule triggers an **AWS Step Functions** state machine ([Chapter 04](04-compute-containers-serverless-and-application-architecture.md))
   or directly a **Lambda function** that performs the response — for
   example, isolating a compromised EC2 instance by replacing its
   security group with a "quarantine" group that permits no traffic, or
   disabling an IAM access key associated with anomalous activity.
3. The response action is logged and, for higher-severity or
   less-certain findings, routed to a human via SNS/ticketing
   integration rather than fully automated — the balance between
   automation speed and false-positive blast radius is a deliberate
   design choice per finding severity, not a blanket "automate
   everything" policy.

### Secrets and key management for containment

**AWS Secrets Manager** stores credentials with automatic rotation
(native rotation Lambda functions for RDS, Redshift, and DocumentDB; a
custom rotation Lambda for any other credential type) and fine-grained
resource policies. During an incident, the ability to force-rotate a
credential immediately — rather than manually resetting it through a
third-party console — is often the fastest containment action available.
**AWS KMS** ([Chapter 05](05-storage-databases-analytics-and-data-protection.md)) provides a second containment lever: disabling a
KMS key immediately blocks all decryption/encryption operations depending
on it, which can contain an in-progress data exfiltration attempt faster
than revoking individual IAM permissions across multiple principals.

### Incident response phases on AWS

AWS-specific incident response follows the same general phases as
traditional IR (preparation, detection and analysis, containment,
eradication and recovery, post-incident activity), with cloud-specific
detail at each phase:

1. **Preparation** — pre-provisioned IAM roles for incident responders
   (least-privilege, time-bound via Identity Center permission sets),
   pre-built forensic tooling (an isolated forensics VPC and account),
   and documented runbooks stored where they remain accessible if the
   primary account is compromised.
2. **Detection and analysis** — GuardDuty/Security Hub findings, CloudTrail
   Lake queries, and VPC Flow Log analysis ([Chapter 03](03-secure-networking-hybrid-connectivity-and-edge.md)) establish scope:
   which principal, which resources, and what time window.
3. **Containment** — network isolation (security group replacement, NACL
   deny), IAM credential revocation/rotation, and KMS key disabling,
   chosen to stop the specific observed activity without unnecessarily
   destroying forensic evidence.
4. **Eradication and recovery** — rebuild affected resources from known-
   good IaC definitions and AMIs/images rather than attempting to "clean"
   a potentially compromised instance in place; rotate every credential
   the compromised principal could have accessed, not only the one
   confirmed misused.
5. **Post-incident activity** — a blameless retrospective, updated
   detection rules/SCPs closing the gap that allowed the incident, and
   evidence retention per legal/compliance requirements.

A critical cloud-specific practice at the containment phase is **preserving
forensic evidence before terminating a compromised resource**: snapshot
the affected EBS volume, capture the instance's memory if feasible, and
export relevant CloudTrail/VPC Flow Log data to an isolated, access-
restricted location before the resource is terminated or its IAM
credentials are rotated out from under an active forensic capture.

### CloudTrail Lake

**CloudTrail Lake** is a managed, SQL-queryable data lake for CloudTrail
events (management, data, and network activity events), retained for up to
seven years, that answers investigative questions ("which principal called
`CreateAccessKey` for this user in the last 90 days") directly via SQL
without exporting logs to a separate analytics stack — a materially faster
investigative path than searching raw CloudTrail S3 objects.

## Design Considerations

- **Enable protection plans deliberately, not all-or-nothing.**
  GuardDuty's S3, EKS, RDS, and Lambda protection plans each carry
  their own cost and require the relevant workload to actually be in
  use; enabling S3 Protection with no S3-based workloads produces no
  value, while skipping EKS Protection on an EKS-heavy environment
  leaves a real detection gap.
- **Automate response proportional to finding confidence and severity,
  not uniformly.** A `CRITICAL` severity finding with high confidence
  (a known-malicious IP performing credential exfiltration) is a strong
  candidate for automatic containment; a `LOW` severity, low-confidence
  finding is better routed to human triage — indiscriminate full
  automation on every finding risks disrupting legitimate activity on a
  false positive.
- **Security Hub standard selection should map to actual compliance
  obligations.** Enabling every available standard produces overlapping,
  sometimes contradictory findings and dilutes attention; select the
  standard(s) that map to the organization's actual regulatory or
  contractual requirements and treat others as reference material.
- **Pre-provision the forensics capability before it is needed.** A
  forensics account/VPC, an incident-responder IAM role, and evidence-
  handling runbooks built during an active incident are built under time
  pressure and are far more likely to have gaps than ones built and
  tested in advance.
- **Containment actions can destroy evidence if sequenced incorrectly.**
  Terminating an instance before snapshotting its volume, or rotating a
  credential before capturing the CloudTrail history of its use, forecloses
  investigative options; define and rehearse the evidence-preservation
  sequence as part of the containment runbook, not as an improvised step.
- **CloudTrail Lake retention and query cost should be sized to actual
  investigative need**, balancing the value of longer retention for
  after-the-fact investigations against ingestion and storage cost —
  align retention with the organization's compliance-mandated evidence
  retention period where one exists.

## Implementation and Automation

### 1. Enable GuardDuty with protection plans (Terraform)

```hcl
resource "aws_guardduty_detector" "main" {
  enable = true
  datasources {
    s3_logs { enable = true }
    kubernetes { audit_logs { enable = true } }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes { enable = true }
      }
    }
  }
}

resource "aws_guardduty_organization_admin_account" "delegated" {
  admin_account_id = "222233334444" # security-tooling account
}
```

### 2. Security Hub with a foundational standard

```hcl
resource "aws_securityhub_account" "main" {}

resource "aws_securityhub_standards_subscription" "fsbp" {
  standards_arn = "arn:aws:securityhub:us-east-1::standards/aws-foundational-security-best-practices/v/1.0.0"
  depends_on    = [aws_securityhub_account.main]
}
```

### 3. Automated response: quarantine an instance on a GuardDuty finding

```hcl
resource "aws_cloudwatch_event_rule" "guardduty_high_severity" {
  name = "guardduty-high-severity-ec2"
  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    "detail-type" = ["GuardDuty Finding"]
    detail = {
      severity = [{ numeric = [">=", 7] }]
      resource = { resourceType = ["Instance"] }
    }
  })
}

resource "aws_cloudwatch_event_target" "quarantine_lambda" {
  rule = aws_cloudwatch_event_rule.guardduty_high_severity.name
  arn  = aws_lambda_function.quarantine_instance.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.quarantine_instance.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.guardduty_high_severity.arn
}
```

```python
# quarantine_instance/index.py — replaces an instance's security groups
# with a no-egress quarantine group and snapshots its volumes before
# any further containment step.
import boto3

ec2 = boto3.client("ec2")
QUARANTINE_SG = "sg-quarantine0000000"

def handler(event, context):
    instance_id = event["detail"]["resource"]["instanceDetails"]["instanceId"]

    volumes = ec2.describe_instances(InstanceIds=[instance_id])
    for reservation in volumes["Reservations"]:
        for instance in reservation["Instances"]:
            for mapping in instance.get("BlockDeviceMappings", []):
                vol_id = mapping["Ebs"]["VolumeId"]
                ec2.create_snapshot(
                    VolumeId=vol_id,
                    Description=f"forensic-snapshot-{instance_id}",
                )

    ec2.modify_instance_attribute(
        InstanceId=instance_id, Groups=[QUARANTINE_SG]
    )
    return {"instanceId": instance_id, "action": "quarantined"}
```

### 4. Secrets Manager rotation and emergency KMS key disable

```bash
# Force an immediate rotation of a compromised database credential
aws secretsmanager rotate-secret \
  --secret-id prod/app/db-credentials \
  --rotate-immediately

# Emergency containment: disable a KMS key blocking all dependent
# encrypt/decrypt operations immediately
aws kms disable-key --key-id "$SUSPECT_KMS_KEY_ID"
```

### 5. CloudTrail Lake investigative query

```bash
aws cloudtrail start-query \
  --query-statement "
    SELECT eventTime, eventName, userIdentity.arn, sourceIPAddress
    FROM $EVENT_DATA_STORE_ID
    WHERE eventName = 'CreateAccessKey'
      AND eventTime > '2026-07-01 00:00:00'
    ORDER BY eventTime DESC
  "

aws cloudtrail get-query-results --query-id "$QUERY_ID"
```

## Validation and Troubleshooting

- **Confirm GuardDuty is actually enrolled organization-wide.** `aws
  guardduty list-organization-admin-accounts` and, from the delegated
  administrator, `aws guardduty list-detectors` per member account
  confirm enrollment; a member account showing no detector was likely
  added to the Organization after the last auto-enrollment sync and
  needs explicit enrollment.
- **Security Hub findings not appearing from a known-active GuardDuty
  finding.** Confirm the GuardDuty-to-Security-Hub integration is
  enabled (`aws securityhub list-enabled-products-for-import`); findings
  generated before the integration was enabled do not backfill
  automatically.
- **EventBridge rule not triggering the response Lambda.** Check the
  rule's event pattern against the actual finding JSON structure using
  `aws events test-event-pattern`; a common failure is a pattern
  referencing an incorrect nested path (for example, missing the
  `detail.severity` numeric matcher syntax), which silently matches zero
  events rather than erroring.
- **Lambda quarantine function fails with `AccessDenied`.** The
  function's execution role needs the specific EC2 actions used
  (`ec2:ModifyInstanceAttribute`, `ec2:CreateSnapshot`,
  `ec2:DescribeInstances`) scoped as tightly as the environment allows;
  verify with CloudWatch Logs for the exact denied action rather than
  broadening the role speculatively.
- **CloudTrail Lake query returns no results for a known event.**
  Confirm the event data store's event selectors actually include the
  relevant event category (management vs. data events) and that the
  query's time range and event data store ID are correct — CloudTrail
  Lake event data stores are created with a specific event source scope
  that does not retroactively include event types added later.
- **Common failure: automated containment disrupts a legitimate
  workload.** A quarantine action triggered by a false-positive finding
  (for example, a legitimate but unusual administrative script) causes
  an outage; maintain a documented, fast manual override/rollback path
  (removing the quarantine security group) alongside every automated
  containment action.

## Security and Best Practices

- Enable GuardDuty and Security Hub in every account from account
  creation (via Control Tower or an Account Factory customization),
  administered centrally from the security-tooling account, so no
  workload account is ever running without baseline detection.
- Route high-confidence, high-severity findings to automated containment
  and lower-confidence findings to human triage, and review the
  threshold split periodically as false-positive/false-negative rates
  become known.
- Preserve forensic evidence (EBS snapshots, exported CloudTrail/VPC
  Flow Log data) before terminating a compromised resource or rotating
  its credentials, following a pre-defined evidence-preservation runbook.
- Store incident-response runbooks and forensic tooling access outside
  the blast radius of the accounts they respond to — a break-glass
  responder role should not depend on the compromised account remaining
  accessible.
- Rotate every credential the compromised principal could have accessed,
  not only the credential confirmed misused, since lateral movement
  before detection is a reasonable default assumption during
  eradication.
- Run a blameless post-incident review after every significant finding
  response, and feed identified gaps back into SCPs ([Chapter 02](02-multi-account-identity-governance-and-landing-zones.md)), Config
  rules ([Chapter 07](07-observability-automation-performance-and-cost-governance.md)), and detection rule tuning — an incident that does
  not produce a control improvement is a missed opportunity, not a
  closed ticket.

## References and Knowledge Checks

**References**

- Amazon GuardDuty, Amazon Inspector, and Amazon Macie documentation.
- AWS Security Hub documentation — security standards and finding
  aggregation (ASFF).
- AWS Secrets Manager and AWS KMS documentation — credential rotation
  and key management.
- AWS CloudTrail Lake documentation — event data stores and SQL-based
  querying.
- AWS Security Incident Response guidance (AWS Well-Architected Security
  Pillar and the AWS incident response whitepaper).
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the detection, incident response, and data
  protection domains of the AWS Certified Security blueprint.

**Knowledge checks**

1. Why is GuardDuty's S3 Protection plan not automatically valuable for
   every account, and what determines whether it should be enabled?
2. Why should automated containment response be tied to finding
   confidence and severity rather than applied uniformly to every
   finding?
3. What forensic evidence can be lost if a compromised EC2 instance is
   terminated before containment steps are taken, and how is that
   avoided?
4. What advantage does CloudTrail Lake offer over querying raw CloudTrail
   log files in S3 during an active investigation?

## Hands-On Lab

**Objective:** Enable GuardDuty, generate a sample finding using
GuardDuty's built-in finding generator, and confirm an EventBridge rule
correctly routes the finding to an SNS notification.

**Cost implications:** GuardDuty bills based on analyzed data volume
(CloudTrail events, VPC Flow Logs, DNS logs); a short-lived lab in a
low-traffic sandbox account typically costs well under one dollar for the
lab's duration, and GuardDuty includes a 30-day free trial for new
detectors. Disable GuardDuty during cleanup to stop ongoing analysis
charges, since it otherwise continues running (and billing) indefinitely.

**Prerequisites**

- An AWS account (sandbox recommended, not a shared production account)
  with AWS CLI v2 configured and permissions for GuardDuty, EventBridge,
  and SNS.

**Steps**

1. Enable GuardDuty:

   ```bash
   DETECTOR_ID=$(aws guardduty create-detector --enable \
     --query "DetectorId" --output text)
   ```

   **Expected result:** A detector ID is returned.

2. Create an SNS topic and an EventBridge rule matching GuardDuty
   findings:

   ```bash
   TOPIC_ARN=$(aws sns create-topic --name lab-guardduty-alerts \
     --query "TopicArn" --output text)
   aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email \
     --notification-endpoint YOUR_EMAIL@example.com

   aws events put-rule --name lab-guardduty-findings \
     --event-pattern '{"source": ["aws.guardduty"], "detail-type": ["GuardDuty Finding"]}'

   aws sns set-topic-attributes --topic-arn "$TOPIC_ARN" \
     --attribute-name Policy --attribute-value '{
       "Version": "2012-10-17",
       "Statement": [{
         "Effect": "Allow", "Principal": {"Service": "events.amazonaws.com"},
         "Action": "SNS:Publish", "Resource": "'"$TOPIC_ARN"'"
       }]
     }'

   aws events put-targets --rule lab-guardduty-findings \
     --targets "Id"="1","Arn"="$TOPIC_ARN"
   ```

   Confirm the email subscription before continuing.

3. Generate GuardDuty sample findings covering every finding type:

   ```bash
   aws guardduty create-sample-findings --detector-id "$DETECTOR_ID"
   ```

4. Confirm the findings were created and the notification arrived:

   ```bash
   aws guardduty list-findings --detector-id "$DETECTOR_ID" \
     --query "length(FindingIds)"
   ```

   **Expected result:** A non-zero count, and an SNS email notification
   for the sample findings routed through EventBridge.

5. **Negative test:** Update the EventBridge rule's pattern to match only
   `CRITICAL` severity (numeric value 9 or above) and re-generate sample
   findings, most of which are below that severity:

   ```bash
   aws events put-rule --name lab-guardduty-findings \
     --event-pattern '{"source": ["aws.guardduty"], "detail-type": ["GuardDuty Finding"], "detail": {"severity": [{"numeric": [">=", 9]}]}}'
   aws guardduty create-sample-findings --detector-id "$DETECTOR_ID"
   ```

   **Expected result:** No new SNS notification for the lower-severity
   sample findings, confirming the tightened pattern correctly filters
   out findings below the new threshold.

6. **Cleanup:**

   ```bash
   aws events remove-targets --rule lab-guardduty-findings --ids "1"
   aws events delete-rule --name lab-guardduty-findings
   aws sns delete-topic --topic-arn "$TOPIC_ARN"
   aws guardduty delete-detector --detector-id "$DETECTOR_ID"
   ```

   Confirm removal:

   ```bash
   aws guardduty list-detectors --query "DetectorIds"
   ```

   The query must return an empty list, confirming GuardDuty analysis
   (and its associated charges) has stopped.

## Summary and Completion Checklist

Amazon GuardDuty, Amazon Inspector, and Amazon Macie provide continuous,
agentless detective coverage across network, compute, and data layers, and
AWS Security Hub aggregates their output into a single, standards-scored
view. EventBridge, Step Functions, and Lambda compose into an automated
detection-to-response pipeline whose automation level should track finding
confidence and severity, not apply uniformly. Secrets Manager and KMS
provide the fastest available containment levers — credential rotation and
key disabling — and CloudTrail Lake turns investigative queries into SQL
rather than manual log archaeology. Every containment action must be
sequenced to preserve forensic evidence, and every incident should produce
a concrete control improvement rather than ending at remediation alone.

- [ ] Can explain what each GuardDuty protection plan detects and when
      to enable it.
- [ ] Can describe how Security Hub aggregates and scores findings
      against a standard.
- [ ] Can build an EventBridge-to-Lambda automated response pipeline for
      a detection finding.
- [ ] Can describe the evidence-preservation sequence required before
      terminating a compromised resource.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
