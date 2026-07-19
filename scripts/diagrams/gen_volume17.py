import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-17-aws-architecture-security"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Hands-On Lab: A Cost Guardrail Whose API Rejects Malformed Input Outright",
        subtitle="A valid monthly budget and a Well-Architected workload register cleanly; an invalid time unit is rejected, not partially applied",
        svg_title="Chapter 1 lab flow: an AWS account baseline hardened with a cost guardrail and a registered Well-Architected workload, tested against malformed budget input",
        svg_desc="Caller identity and Region defaults are confirmed, root is verified to have no access keys, and "
                  "a monthly cost guardrail budget ($10, 80% threshold) is created and confirmed with a near-zero "
                  "actual spend. A sample workload registers in the Well-Architected Tool, returning a "
                  "WorkloadId. As a negative test, a second budget is submitted with an invalid time unit "
                  "(FORTNIGHTLY instead of a supported value); the Budgets API returns a ValidationException "
                  "rather than creating a partially configured guardrail, confirming malformed input is rejected "
                  "outright.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Account baseline", 12.5, 700, "#111827"),
        Line("caller identity confirmed", 10.5, 400, "#374151"),
        Line("root: no access keys", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("lab-guardrail budget", 12.5, 700, "#111827"),
        Line("$10/month, 80% threshold", 10.5, 400, "#374151"),
        Line("+ Well-Architected workload", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("TimeUnit: FORTNIGHTLY", 10.5, 700, "#7f1d1d"),
        Line("(invalid)", 10.5, 700, "#7f1d1d"),
        Line("→ ValidationException", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the Budgets API rejects the malformed request outright rather than creating a broken or partially", 11.5, 400, "#374151"),
        Line("configured guardrail — validation happens before any resource state changes.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Baseline checks"), ("alt", "Valid guardrails"), ("warn", "Rejected malformed input")])
    c.save(f"{OUT}/chapter-01-account-baseline-budget-guardrail-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A Region-Restriction SCP That Overrides the Account's Own IAM Policy",
        subtitle="Calls inside the approved Region succeed normally; the same call outside it is denied regardless of what the account's IAM allows",
        svg_title="Chapter 2 lab topology: an AWS Organizations Region-restriction SCP attached to a sandbox OU, tested against an out-of-Region API call",
        svg_desc="A Sandbox-Test OU receives a Service Control Policy denying all actions outside us-east-1 "
                  "(with narrow exceptions for IAM, Organizations, STS, and Support). A sandbox account moved "
                  "into that OU can describe VPCs normally in us-east-1. As a negative test, the identical call "
                  "is repeated against eu-west-1; it returns an AccessDenied/UnauthorizedOperation error, "
                  "confirming the SCP guardrail blocks the out-of-Region call regardless of what the account's "
                  "own IAM policy would otherwise permit — Organizations-level policy is the ceiling, not merely "
                  "advisory.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Sandbox-Test OU", 12.5, 700, "#111827"),
        Line("SCP: deny outside us-east-1", 10.5, 700, "#1d4ed8"),
        Line("(narrow IAM/STS exceptions)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 110, "alt", [
        Line("describe-vpcs, us-east-1", 12.5, 700, "#111827"),
        Line("normal JSON output", 10.5, 700, "#14532d"),
        Line("(inside approved Region)", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 400, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("describe-vpcs, eu-west-1", 10.5, 700, "#7f1d1d"),
        Line("→ AccessDenied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("the SCP denial applies regardless of the sandbox account's own IAM policy — Organizations-level", 11.5, 400, "#374151"),
        Line("guardrails are a hard ceiling on what any identity in the account can do, not an additional suggestion.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Organizational guardrail"), ("alt", "Permitted Region"), ("warn", "Denied out-of-Region call")])
    c.save(f"{OUT}/chapter-02-scp-region-restriction-topology.svg")


def ch03():
    c = Canvas(960, 620,
        title="Chapter 3 Hands-On Lab: Reachability Analyzer Proves the Security Group Boundary, Not Just Assumes It",
        subtitle="The permitted port finds a valid path; a port the security group doesn't allow reports no path found, with the SG named as the blocker",
        svg_title="Chapter 3 lab topology: a two-AZ VPC with security groups validated by VPC Reachability Analyzer, tested against a blocked port",
        svg_desc="A two-AZ VPC with public and private subnets hosts a test instance in the private subnet behind "
                  "the sg-app security group. A Reachability Analyzer path from the ALB's security group to the "
                  "app instance's ENI on port 8443 succeeds with NetworkPathFound true, confirming the security "
                  "group permits that path. As a negative test, the identical analysis is re-run against port "
                  "3389, which the app security group does not permit; the analysis succeeds but reports "
                  "NetworkPathFound false, with the ExplanationCode identifying the security group as the "
                  "specific blocking component — proving the boundary is enforced, not merely assumed from the "
                  "rule definitions.")
    c.node_box(60, 150, 220, 110, "mgmt", [
        Line("ALB security group", 12.5, 700, "#111827"),
        Line("(notional source)", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 150, 240, 110, "alt", [
        Line("App instance (private subnet)", 12, 700, "#111827"),
        Line("sg-app: allows 8443", 10.5, 700, "#14532d"),
        Line("blocks 3389", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(280, 205, 360, 205, "alt", label="port 8443: path found")
    c.node_box(700, 150, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("Reachability path :3389", 10.5, 700, "#7f1d1d"),
        Line("→ NetworkPathFound: false", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(600, 205, 700, 205, "warn", label="blocked by sg-app")
    c.node_box(60, 340, 860, 90, "neutral", [
        Line("the analysis succeeds either way (the tool itself works); ExplanationCode identifies the security group", 11.5, 400, "#374151"),
        Line("as the specific component blocking port 3389 — the enforcement boundary is proven, not assumed.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 470, [("mgmt", "Traffic source"), ("alt", "Security-group-governed destination"), ("warn", "Confirmed-blocked path")])
    c.save(f"{OUT}/chapter-03-vpc-reachability-analyzer-topology.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: A Least-Privilege Lambda Role Proven by Removing It Mid-Lab",
        subtitle="The API writes to DynamoDB successfully with the scoped role in place, and fails specifically at the DynamoDB layer the moment PutItem is revoked",
        svg_title="Chapter 4 lab flow: a Lambda function behind an HTTP API Gateway with a least-privilege execution role, tested against a revoked IAM permission",
        svg_desc="A Lambda function scoped to only dynamodb:PutItem and basic logging permissions sits behind an "
                  "HTTP API Gateway route; invoking the endpoint returns 'order recorded' and the DynamoDB table's "
                  "item count increases. As a negative test, the PutItem permission is deleted from the "
                  "function's execution role and the endpoint invoked again; the API now returns HTTP 502, and "
                  "the function's CloudWatch Logs show an AccessDeniedException from DynamoDB specifically — "
                  "confirming the least-privilege grant, not an implicit broader permission, was what allowed the "
                  "write to succeed in the first place.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("API Gateway → Lambda", 12.5, 700, "#111827"),
        Line("execution role: PutItem only", 10.5, 700, "#1d4ed8"),
        Line("+ basic log permissions", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("DynamoDB write succeeds", 12.5, 700, "#111827"),
        Line("curl → \"order recorded\"", 10.5, 700, "#14532d"),
        Line("table item count increases", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("PutItem permission deleted", 10.5, 700, "#7f1d1d"),
        Line("→ HTTP 502, AccessDeniedException", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("CloudWatch Logs name DynamoDB specifically as the denial source — the scoped role was what made", 11.5, 400, "#374151"),
        Line("the earlier write work, not a broader grant the application happened not to exercise.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Scoped execution role"), ("alt", "Permitted write"), ("warn", "Revoked permission (denied)")])
    c.save(f"{OUT}/chapter-04-lambda-least-privilege-flow.svg")


def ch05():
    c = Canvas(960, 580,
        title="Chapter 5 Hands-On Lab: Block Public Access Rejects a Public-Read Policy Even When the Policy Explicitly Grants It",
        subtitle="An encrypted, versioned bucket with a lifecycle rule stays private — an attached public-read statement is blocked at the account/bucket control layer",
        svg_title="Chapter 5 lab flow: an encrypted, versioned S3 bucket with Block Public Access enforced, tested against an explicit public-read policy attempt",
        svg_desc="A customer-managed KMS key backs a new bucket with Block Public Access, versioning, and default "
                  "KMS encryption all enabled; a test object uploads and is confirmed encrypted with the CMK, and "
                  "a lifecycle rule transitions objects to Standard-IA after 30 days. As a negative test, a "
                  "bucket policy explicitly granting public s3:GetObject to any principal is submitted; the call "
                  "fails with AccessDenied, stating the action is blocked by the bucket's Block Public Access "
                  "configuration — confirming the control prevents accidental public exposure even when a policy "
                  "document explicitly tries to grant it.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("lab-data-bucket (CMK-encrypted)", 12, 700, "#111827"),
        Line("versioning + default KMS encryption", 10.5, 400, "#374151"),
        Line("Block Public Access: enabled", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Lifecycle rule", 12.5, 700, "#111827"),
        Line("→ Standard-IA after 30 days", 10.5, 700, "#14532d"),
        Line("confirmed as submitted", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("public-read bucket policy", 10.5, 700, "#7f1d1d"),
        Line("submitted explicitly", 10.5, 700, "#7f1d1d"),
        Line("→ AccessDenied (BPA blocks it)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("Block Public Access rejects the policy attachment itself — the exposure never becomes live even", 11.5, 400, "#374151"),
        Line("though the submitted policy document explicitly grants public read access.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Protected bucket state"), ("alt", "Data lifecycle"), ("warn", "Blocked exposure attempt")])
    c.save(f"{OUT}/chapter-05-s3-block-public-access-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: Route 53 Failover That Shifts DNS Automatically, With No Manual Change",
        subtitle="A healthy primary resolves normally; once its health check fails the threshold, resolution shifts to the secondary on its own",
        svg_title="Chapter 6 lab topology: Route 53 failover routing between a primary and secondary endpoint, tested against a failed health check",
        svg_desc="A health check against the primary endpoint reports healthy, and app.lab-dr-test.example.com "
                  "resolves via CNAME to the primary endpoint, confirmed with dig. As a negative test, the "
                  "primary endpoint is made to fail its health check; after the configured failure threshold "
                  "(roughly two minutes at a 30-second interval with a threshold of 2), the health check reports "
                  "unhealthy and the same dig query now resolves to the secondary endpoint instead — confirming "
                  "automatic failover occurred with no manual DNS record change.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Health check: primary", 12.5, 700, "#111827"),
        Line("30s interval, threshold 2", 10.5, 400, "#374151"),
        Line("status: healthy", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("app.lab-dr-test... CNAME", 12, 700, "#111827"),
        Line("resolves to primary-endpoint", 10.5, 700, "#14532d"),
        Line("(PRIMARY failover record)", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("primary fails health check", 10.5, 700, "#7f1d1d"),
        Line("→ resolves to secondary", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("the SECONDARY failover record has no health check of its own — it becomes authoritative purely", 11.5, 400, "#374151"),
        Line("because the PRIMARY record's health check failed, with no administrator touching a DNS record.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Health check state"), ("alt", "Primary DNS resolution"), ("warn", "Automatic failover")])
    c.save(f"{OUT}/chapter-06-route53-failover-topology.svg")


def ch07():
    c = Canvas(960, 580,
        title="Chapter 7 Hands-On Lab: A CloudWatch Alarm Confirmed Bidirectional, Not Latched",
        subtitle="Two above-threshold data points trip the alarm and notify; two below-threshold points clear it and notify again",
        svg_title="Chapter 7 lab flow: a CloudWatch alarm on a custom metric firing and clearing through SNS, tested for bidirectional (non-latching) behavior",
        svg_desc="An alarm on the Lab/App QueueDepth custom metric, evaluated over two periods above a threshold "
                  "of 100, transitions to ALARM after two consecutive above-threshold data points are published, "
                  "and an SNS email notification arrives. As a negative test, two data points back under the "
                  "threshold are published; the alarm returns to OK and a second SNS notification confirms the "
                  "recovery — proving the alarm evaluates the metric bidirectionally rather than latching in "
                  "ALARM state once triggered.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("QueueDepth: 150, then 175", 12.5, 700, "#111827"),
        Line("(2 periods above threshold 100)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "warn", [
        Line("Alarm: ALARM", 12.5, 700, "#111827"),
        Line("SNS notification #1 fires", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("QueueDepth: 10, then 5", 10.5, 700, "#14532d"),
        Line("→ Alarm: OK, SNS notification #2", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("the second notification on recovery is what confirms the alarm is genuinely bidirectional — a", 11.5, 400, "#374151"),
        Line("one-directional or latched alarm would never send a clearing notification once triggered.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Above-threshold data"), ("warn", "Alarm fires"), ("alt", "Alarm clears (recovery confirmed)")])
    c.save(f"{OUT}/chapter-07-cloudwatch-alarm-bidirectional-flow.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: An EventBridge Severity Filter That Correctly Suppresses Low-Severity Findings",
        subtitle="Sample GuardDuty findings notify at first, then a tightened CRITICAL-only pattern correctly produces no notification for the same lower-severity findings",
        svg_title="Chapter 8 lab flow: GuardDuty sample findings routed through EventBridge to SNS, tested against a severity-tightened event pattern",
        svg_desc="GuardDuty is enabled and generates sample findings covering every finding type; an EventBridge "
                  "rule matching all GuardDuty Finding events routes them to an SNS topic, and the subscribed "
                  "email receives a notification. As a negative test, the EventBridge rule's pattern is tightened "
                  "to match only severity 9 or above (CRITICAL), and sample findings are regenerated — most of "
                  "which fall below that severity; no new SNS notification arrives, confirming the tightened "
                  "pattern correctly filters out findings below the new threshold rather than notifying on "
                  "everything regardless of the pattern.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("GuardDuty detector", 12.5, 700, "#111827"),
        Line("create-sample-findings", 10.5, 400, "#374151"),
        Line("(all finding types, all severities)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("EventBridge: all findings", 12, 700, "#111827"),
        Line("→ SNS notification arrives", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("pattern tightened: severity ≥ 9", 10.5, 700, "#7f1d1d"),
        Line("→ no new notification", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("most regenerated sample findings fall below CRITICAL severity, and the tightened pattern correctly", 11.5, 400, "#374151"),
        Line("suppresses notification for them — the filter is doing real work, not passing everything through.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Detection source"), ("alt", "Unfiltered routing"), ("warn", "Severity-filtered (correctly suppressed)")])
    c.save(f"{OUT}/chapter-08-guardduty-eventbridge-severity-flow.svg")


def ch09():
    c = Canvas(960, 640,
        title="Chapter 9 Hands-On Lab: The Capstone — a Posture-Check Script and an IAM Boundary That Holds Under Composition",
        subtitle="The full serverless stack works end to end and self-reports its own gaps; the scoped Lambda role still blocks an unsupported action",
        svg_title="Chapter 9 lab flow: the volume's minimal secure serverless capstone stack exercised end to end, audited by a posture-check script, and tested against an out-of-scope Lambda action",
        svg_desc="The capstone Terraform stack (Lambda, DynamoDB, S3, CloudWatch, KMS) applies cleanly; posting "
                  "to the deployed API endpoint writes a DynamoDB item, confirmed by a nonzero scan count. A "
                  "posture-check script reports Organizations feature set, S3 Block Public Access status, "
                  "GuardDuty/Security Hub enrollment, and active alarms, flagging any GAP: line honestly. The "
                  "workload registers in the Well-Architected Tool with at least one real Cost Optimization "
                  "finding recorded. As a negative test, the Lambda function is invoked with an unsupported "
                  "delete_table action; the function either rejects it in application logic or, if it attempted "
                  "the call, CloudWatch Logs show an AccessDeniedException — confirming the scoped IAM policy "
                  "from the individual-chapter lab still blocks anything beyond PutItem/GetItem/Scan in this "
                  "composed stack.")
    c.node_box(60, 130, 260, 120, "mgmt", [
        Line("Capstone stack (Terraform)", 12.5, 700, "#111827"),
        Line("Lambda + DynamoDB + S3 + CW + KMS", 10.5, 400, "#374151"),
        Line("POST /notes → item written", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 130, 240, 120, "alt", [
        Line("posture-check.sh", 12.5, 700, "#111827"),
        Line("Org/S3-BPA/GuardDuty/alarms", 10.5, 400, "#374151"),
        Line("GAP: lines reported honestly", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 190, 400, 190, "mgmt")
    c.node_box(700, 130, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("invoke: delete_table action", 10.5, 700, "#7f1d1d"),
        Line("(unsupported / out of scope)", 10.5, 400, "#7f1d1d"),
        Line("→ rejected or AccessDenied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 190, 700, 190, "warn")
    c.node_box(60, 320, 860, 100, "neutral", [
        Line("the scoped IAM policy from Chapter 4's individual lab still blocks anything beyond PutItem/GetItem/Scan", 11.5, 400, "#374151"),
        Line("in this fully composed stack — least privilege composes correctly, it doesn't erode when the stack grows.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Deployed capstone stack"), ("alt", "Honest self-audit"), ("warn", "IAM boundary under composition")])
    c.save(f"{OUT}/chapter-09-capstone-posture-check-iam-boundary-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
