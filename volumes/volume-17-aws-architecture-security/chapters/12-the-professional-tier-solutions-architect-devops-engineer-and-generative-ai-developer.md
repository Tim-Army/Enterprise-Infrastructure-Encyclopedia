# Chapter 12: The Professional Tier — Solutions Architect, DevOps Engineer, and Generative AI Developer

![The professional tier above the associate tier. Three professional certifications: Solutions Architect Professional (SAP-C02), testing multi-account and multi-Region architecture and migration, drawing on Chapters 2, 3, 6, and 7; DevOps Engineer Professional (DOP-C02), testing continuous delivery, automation, and resilience, drawing on Chapters 6 and 7; and Generative AI Developer Professional (AIP-C01), the newest professional exam, testing production generative-AI solutions on services such as Amazon Bedrock, reaching beyond this volume. Below sits the associate tier as the practical starting point, with a note that no formal prerequisite exists but roughly two years of hands-on AWS experience is assumed. All three professional exams run 180 minutes with 75 questions and are dominated by long scenario items — the step up is reading load, trade-off judgment, service breadth, and organizational scale.](../../../diagrams/volume-17-aws-architecture-security/chapter-12-professional-tier-map.svg)

*Figure 12-1. What actually changes at the professional tier: scope and reading load, not obscurity. The associate tier below is a practical starting point, not a gate.*

## Learning Objectives

- Identify the three professional-tier AWS certifications and their codes,
  including the newly added Generative AI Developer – Professional
  (AIP-C01).
- Explain what genuinely changes at the professional tier — reading load,
  trade-off judgment, service breadth, and organizational scale — rather
  than assuming the questions are simply harder.
- Map Solutions Architect – Professional and DevOps Engineer – Professional
  onto this volume's multi-account, networking, reliability, and operations
  chapters.
- Decide whether to sit an associate exam first, given that AWS imposes no
  prerequisite but assumes roughly two years of hands-on experience.
- Build a pacing plan for a 180-minute, 75-question scenario exam, since
  time pressure at this tier comes from reading speed as much as recall.

## Theory and Architecture

The professional tier holds three certifications. Two have existed for
years and map well onto this volume; the third is new and points outside
it. All three run **180 minutes with 75 questions**.

This is study and review material organized against published structure; it
reproduces no exam content. Codes were verified against AWS's certification
pages on 23 July 2026.

### The three professional certifications

| Certification | Code | What it tests | This volume |
| --- | --- | --- | --- |
| Solutions Architect – Professional | SAP-C02 | Multi-account, multi-Region architecture, migration, and cost optimization at organizational scale | [2](02-multi-account-identity-governance-and-landing-zones.md), [3](03-secure-networking-hybrid-connectivity-and-edge.md), [6](06-reliability-migration-multi-region-and-disaster-recovery.md), [7](07-observability-automation-performance-and-cost-governance.md) |
| DevOps Engineer – Professional | DOP-C02 | Continuous delivery, automation, monitoring, and operational resilience | [6](06-reliability-migration-multi-region-and-disaster-recovery.md), [7](07-observability-automation-performance-and-cost-governance.md) |
| Generative AI Developer – Professional | AIP-C01 | Building and deploying production generative-AI solutions on AWS services such as Amazon Bedrock | beyond this volume |

**Generative AI Developer – Professional (AIP-C01)** is the newest addition
to the program and will not appear in older certification maps. It sits at
full professional level — 180 minutes, 75 questions — and targets engineers
building production generative-AI systems, not the conceptual fluency that
AI Practitioner (AIF-C01,
[Chapter 10](10-the-aws-certification-program-structure-foundational-tier-and-recertification.md))
covers. This volume does not teach Bedrock or generative-AI application
architecture; treat AIP-C01 as a separate project with its own study plan.

### What actually changes at this tier

The professional exams are not associate exams with more obscure facts.
Four things change, and preparing for the wrong one is the common failure:

- **Reading load.** Question stems run several paragraphs, describing an
  organization, its constraints, and its goals before asking anything. At
  75 questions in 180 minutes you have roughly 2 minutes 24 seconds per
  question *including* reading. Time pressure here is a reading-speed
  problem more than a recall-speed problem.
- **Trade-offs over facts.** Several answer options usually work. The
  question is which one best satisfies the stated constraints — cost
  ceiling, RTO/RPO, compliance boundary, operational overhead. Knowing that
  a service *can* do something is not enough; you need to know when it is
  the wrong choice.
- **Service breadth per question.** A single scenario can span identity,
  networking, storage, and cost governance simultaneously. Siloed knowledge
  fails here even when each silo is strong.
- **Organizational scale.** The unit of design is the organization and its
  accounts, not one workload. This is why
  [Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)'s
  Organizations, SCP, and Control Tower material carries disproportionate
  weight for SAP-C02.

### Associate first?

AWS imposes **no prerequisite** — you may sit SAP-C02 without holding
SAA-C03. AWS does state an expectation of roughly **two or more years of
hands-on AWS experience** for this tier, and that expectation, not a rule,
is what should drive the decision:

- With two-plus years of real AWS work, going straight to professional is
  defensible and saves an exam fee and several weeks.
- Without it, the associate exam is a cheaper, faster way to find the gaps
  — and a failed professional attempt costs more than an associate pass.
- The recertification interaction from Chapter 10 also matters: a
  professional pass generally carries a held associate certification's
  clock forward, so taking both close together is efficient if you want
  both.

### SAP-C02 and DOP-C02 overlap more than their names suggest

Both professional exams test operational resilience, automation, and
monitoring at scale — Chapters 6 and 7 serve both. They diverge in where
the weight sits: SAP-C02 pushes into multi-account governance, network
architecture, and migration strategy; DOP-C02 pushes into deployment
pipelines, release safety, and incident response automation. A reader who
holds one finds the second substantially cheaper than starting cold.

## Design Considerations

- **Train reading pace deliberately.** Practice with full-length,
  multi-paragraph scenarios against a clock, not with short recall
  questions. If you cannot sustain roughly 2 minutes 24 seconds per
  question including reading, the constraint is pacing, and pacing is
  trainable separately from content.
- **Study by constraint, not by service.** For each service you know,
  practice naming the condition under which it is the *wrong* answer —
  too expensive, too slow to recover, too much operational overhead. That
  inversion is what the trade-off questions test.
- **Give Chapter 2 extra weight for SAP-C02.** Multi-account design,
  service control policies, and landing zones carry weight at this tier
  well beyond their share of this volume's page count.
- **Do not prepare AIP-C01 from this volume.** Chapters 1–9 give you the
  AWS platform grounding it assumes, and nothing about Bedrock, prompt and
  retrieval architecture, evaluation, or generative-AI operations. Plan
  separate study and separate lab time.
- **Sequence the two established professionals together if you want both.**
  Their shared Chapter 6/7 foundation makes the second exam far cheaper
  soon after the first than years later.
- **Ethical preparation boundary.** AWS exam guides, Skill Builder,
  official training, and hands-on practice only. The professional tier is
  heavily targeted by dump sites; their material is both a
  certification-agreement violation and unusually poor preparation, because
  memorized answers do not transfer to scenario questions whose constraints
  vary.

## Implementation and Automation

### A pacing rehearsal

```text
# Professional pacing: 75 questions / 180 minutes = 2m24s per question,
# reading included. Rehearse in blocks rather than one sitting.

Block   | Questions | Target time | Actual | Notes
--------|-----------|-------------|--------|---------------------------
1       | 25        | 60 min      |        | flag-and-move discipline
2       | 25        | 60 min      |        | watch for slowdown
3       | 25        | 60 min      |        | fatigue is the real test
Review  | flagged   | remainder   |        |

# Rule to rehearse: if a question is unresolved at 3 minutes, flag it,
# choose the best current answer, and move. Time lost early is not
# recoverable late.
```

### A trade-off drill against your own architecture

```bash
# SAP-C02 rewards knowing when a service is the wrong choice. Take the
# Chapter 6 DR setup and re-cost it under a different constraint.
aws ce get-cost-and-usage \
  --time-period Start=2026-06-01,End=2026-07-01 \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[?Metrics.UnblendedCost.Amount>`1`]' \
  --output table
# Then answer, in writing: if the RTO relaxed from minutes to 8 hours,
# which of these services would you remove, and what would you lose?
```

### A DevOps-tier drill: prove a rollback, not just a deploy

```bash
# DOP-C02 is about release safety. A pipeline that has never rolled back
# is unproven. Trigger a deployment, then force the rollback path.
aws deploy list-deployments --application-name lab-app \
  --query 'deployments[0]' --output text
aws deploy stop-deployment --deployment-id <DEPLOYMENT_ID> --auto-rollback-enabled
# Confirm the previous revision is serving traffic and the alarm that
# should have caught the bad release actually fired.
```

## Validation and Troubleshooting

- **Pacing is the first thing to measure.** Run one 25-question timed block
  before any content study. If you finish comfortably, content is your
  constraint; if you run out of time, pacing is, and no amount of extra
  reading fixes it.
- **Test trade-off reasoning by inversion.** For any service you would
  propose, state aloud the constraint that would make it wrong. If you
  cannot, your knowledge is descriptive rather than comparative, which is
  the gap this tier exposes.
- **Check breadth with cross-domain questions.** Give yourself a scenario
  touching identity, network, storage, and cost at once and answer it end
  to end. Strong single-domain knowledge with weak integration is the
  characteristic professional-tier failure.
- **Do not read AIP-C01 readiness from AWS platform strength.** Being
  strong on this volume says nothing about Bedrock application
  architecture. Rate it only against generative-AI material you have
  actually built with.
- **Confirm the format before booking.** 75 questions and 180 minutes is
  the current professional format; verify on the exam page, since format
  changes are exactly the kind of detail that shifts without fanfare.

## Security and Best Practices

- Run the cost and deployment drills in the sandbox account with the budget
  alarm from Chapter 10. The SAP-C02 cost drill queries real billing data —
  use your own account's data, and never share exported cost reports, which
  can reveal architecture and scale.
- The DevOps rollback drill deliberately fails a deployment. Never rehearse
  it against a pipeline that can reach production; use a dedicated lab
  application.
- Multi-account drills touch AWS Organizations. Follow
  [Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)'s
  guidance on management-account hygiene — practice SCP changes on a
  sandbox organizational unit, never at the root, where a mistake locks out
  every account.
- Keep least-privilege discipline in drill roles even under time pressure;
  the professional exams test the correct pattern, and preparation is where
  the habit forms.

## References and Knowledge Checks

**References**

- [AWS Certified Solutions Architect – Professional](https://aws.amazon.com/certification/certified-solutions-architect-professional/) (SAP-C02)
- [AWS Certified DevOps Engineer – Professional](https://aws.amazon.com/certification/certified-devops-engineer-professional/) (DOP-C02)
- [AWS Certified Generative AI Developer – Professional](https://aws.amazon.com/certification/certified-generative-ai-developer-professional/) (AIP-C01)
- [AWS Skill Builder](https://skillbuilder.aws/) — official exam-prep plans,
  including full-length practice at professional pacing.
- [Appendix — AWS Certifications and Course Access](../../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md)
- See [Chapter 11](11-the-associate-tier-developer-cloudops-data-engineer-and-machine-learning-engineer.md)
  for the tier below and
  [Chapter 13](13-specialty-certifications-and-keeping-the-aws-certification-program-current.md)
  for the specialty tier.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any AWS exam item)*

1. Name the three professional certifications and their codes, and say
   which one is newest.
2. Give the four things that change at the professional tier, and explain
   why "the questions are harder" is an inadequate summary.
3. Compute the per-question time budget for a professional exam and
   describe the flag-and-move rule you would rehearse.
4. AWS requires no prerequisite for SAP-C02. Give one case for sitting it
   directly and one for taking an associate exam first.
5. Why is being strong on this volume a poor predictor of AIP-C01
   readiness?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every task in the
three professional exam guides** — Solutions Architect – Professional
(SAP-C02, 20 tasks), DevOps Engineer – Professional (DOP-C02, 19), and
Generative AI Developer – Professional (AIP-C01, 20) — 59 labs, each mapped
in the volume README's coverage tables. The professional exams reward design
judgment, so each SAP lab is a **command-driven design walkthrough**: it
reads the real evidence a decision rests on, then records the decision and
the alternative rejected.

**Shared prerequisites for Labs 12.1–12.59**

- AWS CLI v2 authenticated to a sandbox with the relevant admin rights, a
  default Region, and (for the AIP labs) Amazon Bedrock model access. An
  execution role ARN is in `$ROLE_ARN`.
- **Cost:** labs prefer read/describe and create-then-delete over long-
  running compute; any non-trivial spend (multi-account, Transit Gateway,
  OpenSearch, Bedrock invocation) is marked and cleaned up the same day.
- Every lab ends **`**Lab verified by:** *pending*`** until a human runs it.

**Solutions Architect – Professional (SAP-C02) — Labs 12.1–12.20**

### Lab 12.1 — Architect network connectivity strategies

**Objective:** Read the account's inter-VPC topology to choose between
peering and a Transit Gateway hub.

```bash
aws ec2 describe-vpc-peering-connections --query 'length(VpcPeeringConnections)' --output text
aws ec2 describe-transit-gateways --query 'length(TransitGateways)' --output text
```

**Expected result:** counts that reveal the current model. **Decision to
record:** at >3 VPCs needing any-to-any reach, a Transit Gateway hub
replaces the O(n²) peering mesh; below that, peering is cheaper. Note the
rejected option and why.

**Negative test:** assume full-mesh peering scales; at 6 VPCs it needs 15
connections and 15 route-table edits — the failure a hub design avoids.

**Cleanup:** none (read-only assessment).

### Lab 12.2 — Prescribe security controls

**Objective:** Inventory guardrails already in force to prescribe the gaps.

```bash
aws organizations list-policies --filter SERVICE_CONTROL_POLICY \
  --query 'Policies[].Name' --output text 2>&1 | head -1
aws securityhub get-enabled-standards --query 'StandardsSubscriptions[].StandardsArn' --output text 2>&1 | head -1
```

**Expected result:** the SCPs and Security Hub standards in place. **Decision
to record:** prescribe the missing preventive control (SCP) versus detective
control (Security Hub standard) for the identified gap.

**Negative test:** rely on detective controls alone; a misconfiguration is
found *after* it happens — the case for a preventive SCP.

**Cleanup:** none (read-only).

### Lab 12.3 — Design reliable and resilient architectures

**Objective:** Read a workload's current AZ spread to design for AZ
independence.

```bash
aws ec2 describe-instances --filters Name=tag:Env,Values=prod \
  --query 'Reservations[].Instances[].Placement.AvailabilityZone' --output text | tr '\t' '\n' | sort | uniq -c
```

**Expected result:** instance counts per AZ. **Decision to record:** if any
AZ holds a majority, redistribute so the loss of one AZ removes at most
1/N of capacity; record the target spread.

**Negative test:** a "resilient" tier with all instances in one AZ fails
completely on a single-AZ event.

**Cleanup:** none (read-only).

### Lab 12.4 — Design a multi-account AWS environment

**Objective:** Read the organization structure to place workloads by OU.

```bash
aws organizations list-roots --query 'Roots[0].Id' --output text
aws organizations list-organizational-units-for-parent --parent-id "$(aws organizations list-roots --query 'Roots[0].Id' --output text)" \
  --query 'OrganizationalUnits[].Name' --output text
```

**Expected result:** the OU layout (e.g. Security, Infrastructure, Workloads,
Sandbox). **Decision to record:** which OU a new workload joins and which
SCPs it inherits.

**Negative test:** a flat single-account design cannot apply
environment-specific SCPs, the isolation multi-account provides.

**Cleanup:** none (read-only).

### Lab 12.5 — Determine cost optimization and visibility strategies

**Objective:** Read cost by service to target the largest optimization.

```bash
aws ce get-cost-and-usage --time-period Start=$(date -u +%Y-%m-01),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[:5].[Keys[0],Metrics.UnblendedCost.Amount]' --output text
```

**Expected result:** the top spend by service. **Decision to record:**
target the largest line (e.g. Savings Plans for steady EC2, S3 lifecycle for
storage) and the expected saving.

**Negative test:** optimize a trivial line while the top service dominates
spend — effort spent where it cannot matter.

**Cleanup:** none (read-only).

### Lab 12.6 — Design a deployment strategy to meet business requirements

**Objective:** Choose a rollout strategy by reading the available CodeDeploy
configs.

```bash
aws deploy list-deployment-configs --query 'deploymentConfigsList' --output text | tr '\t' '\n' | grep -i canary
```

**Expected result:** the canary configs available. **Decision to record:**
for a low-risk-tolerance service, a linear/canary shift over all-at-once;
record the RTO impact of each.

**Negative test:** an all-at-once deploy of a bad build takes 100% of
traffic down before any alarm fires.

**Cleanup:** none (read-only).

### Lab 12.7 — Design a solution to ensure business continuity

**Objective:** Inspect backup coverage to design a continuity plan.

```bash
aws backup list-protected-resources --query 'Results[].ResourceType' --output text | tr '\t' '\n' | sort -u
```

**Expected result:** the resource types under backup. **Decision to record:**
the DR pattern (backup-restore, pilot-light, warm-standby, multi-site) that
meets the stated RTO/RPO, and the cost of each.

**Negative test:** a backup plan that omits a critical data store leaves an
un-recoverable gap in the continuity design.

**Cleanup:** none (read-only).

### Lab 12.8 — Determine security controls based on requirements

**Objective:** Map a data-classification requirement to a concrete control
by reading current encryption posture.

```bash
aws s3api get-bucket-encryption --bucket "$BUCKET" \
  --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault' 2>&1 | head -3
```

**Expected result:** the bucket's default encryption (or none). **Decision
to record:** for "confidential" data, SSE-KMS with a CMK and a key policy
versus SSE-S3 — and why the requirement forces the stronger control.

**Negative test:** SSE-S3 cannot satisfy a requirement for per-team key
access separation; only a CMK key policy can.

**Cleanup:** none (read-only).

### Lab 12.9 — Design a strategy to meet reliability requirements

**Objective:** Read service quotas that cap reliability before designing
around them.

```bash
aws service-quotas list-service-quotas --service-code ec2 \
  --query "Quotas[?contains(QuotaName,'On-Demand')].[QuotaName,Value]" --output text | head
```

**Expected result:** the On-Demand vCPU quotas. **Decision to record:**
whether a multi-AZ scale-out fits within quota or needs a quota-increase
request as part of the reliability design.

**Negative test:** a design that assumes unlimited capacity fails at the
quota ceiling during the exact surge it was meant to survive.

**Cleanup:** none (read-only).

### Lab 12.10 — Design a solution to meet performance objectives

**Objective:** Read Compute Optimizer findings to size for performance.

```bash
aws compute-optimizer get-ec2-instance-recommendations \
  --query 'instanceRecommendations[0].{Current:currentInstanceType,Finding:finding,Rec:recommendationOptions[0].instanceType}' 2>&1 | head -6
```

**Expected result:** a finding (`Underprovisioned`/`Optimized`) and a
recommended type. **Decision to record:** the instance family that meets the
latency/throughput objective, and the evidence behind it.

**Negative test:** guessing an instance type without the recommendation
either overspends or under-serves the objective.

**Cleanup:** none (read-only).

### Lab 12.11 — Determine a cost optimization strategy for solution goals

**Objective:** Read Savings Plans utilization to decide on a commitment.

```bash
aws ce get-savings-plans-utilization --time-period Start=$(date -u -v-30d +%Y-%m-%d 2>/dev/null || date -u -d '30 days ago' +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
  --query 'Total.Utilization.UtilizationPercentage' --output text 2>&1 | head -1
```

**Expected result:** current utilization (or none if no plan). **Decision to
record:** commit to a Compute Savings Plan sized to steady-state usage;
record the break-even and the on-demand fallback for spiky load.

**Negative test:** over-committing a Savings Plan to peak usage wastes the
commitment during troughs.

**Cleanup:** none (read-only).

### Lab 12.12 — Determine a strategy to improve operational excellence

**Objective:** Read Systems Manager OpsCenter/compliance to target ops
improvements.

```bash
aws ssm list-compliance-summaries \
  --query 'ComplianceSummaryItems[].{Type:ComplianceType,NonCompliant:NonCompliantSummary.NonCompliantCount}' --output table 2>&1 | head
```

**Expected result:** compliance counts by type (patch, association).
**Decision to record:** automate the largest non-compliant category (e.g.
patch) via a maintenance window rather than manual remediation.

**Negative test:** tracking ops health by ticket volume alone hides
systemic drift that compliance summaries make measurable.

**Cleanup:** none (read-only).

### Lab 12.13 — Determine a strategy to improve security

**Objective:** Read Security Hub findings severity to prioritize the
improvement.

```bash
aws securityhub get-findings --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}],"RecordState":[{"Value":"ACTIVE","Comparison":"EQUALS"}]}' \
  --query 'length(Findings)' --output text 2>&1 | head -1
```

**Expected result:** a count of active critical findings. **Decision to
record:** remediate critical findings first and encode the fix as a Config rule so
it cannot recur.

**Negative test:** closing findings by hand without a preventive control
lets the same misconfiguration return next week.

**Cleanup:** none (read-only).

### Lab 12.14 — Determine a strategy to improve performance

**Objective:** Read CloudWatch latency percentiles to find the real
bottleneck.

```bash
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB \
  --metric-name TargetResponseTime --dimensions Name=LoadBalancer,Value=$ALB_NAME \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 300 --extended-statistics p95 p99 \
  --query 'Datapoints[0].ExtendedStatistics'
```

**Expected result:** p95/p99 response times. **Decision to record:** whether
the fix is caching (CloudFront/ElastiCache), a larger instance, or a read
replica — chosen from the tail latency, not the average.

**Negative test:** optimizing on the mean hides a p99 that violates the SLA.

**Cleanup:** none (read-only).

### Lab 12.15 — Determine a strategy to improve reliability

**Objective:** Read Trusted Advisor fault-tolerance checks.

```bash
aws support describe-trusted-advisor-checks --language en \
  --query "checks[?category=='fault_tolerance'].name" --output text 2>&1 | head -3
```

**Expected result:** the fault-tolerance check names (requires Business
Support). **Decision to record:** address the flagged single points of
failure (single-AZ RDS, no ASG) in priority order.

**Negative test:** `SubscriptionRequiredException` on Basic Support shows
this reliability signal needs a paid plan — itself a design input.

**Cleanup:** none (read-only).

### Lab 12.16 — Identify opportunities for cost optimizations

**Objective:** Find idle resources with Compute Optimizer's rightsizing.

```bash
aws compute-optimizer get-ec2-instance-recommendations \
  --filters name=Finding,values=Overprovisioned \
  --query 'instanceRecommendations[].{Id:instanceArn,Save:recommendationOptions[0].savingsOpportunity.estimatedMonthlySavings.value}' \
  --output text 2>&1 | head
```

**Expected result:** over-provisioned instances and their monthly savings.
**Decision to record:** rightsize the largest-saving instances first;
record the total addressable saving.

**Negative test:** cost cuts driven by intuition miss idle capacity the data
names precisely.

**Cleanup:** none (read-only).

### Lab 12.17 — Select existing workloads and processes for migration

**Objective:** Read Application Discovery data to prioritize migration
candidates.

```bash
aws discovery describe-configurations --configuration-ids none 2>&1 | head -1
aws migrationhubstrategy get-portfolio-summary 2>&1 | head -3
```

**Expected result:** discovery/portfolio summary availability. **Decision to
record:** select low-dependency, high-value workloads first (the migration
"waves"); record why a tightly-coupled workload is deferred.

**Negative test:** migrating a highly-connected workload first drags its
entire dependency web along unplanned.

**Cleanup:** none (read-only).

### Lab 12.18 — Determine the optimal migration approach

**Objective:** Map a workload to one of the 7 Rs by reading its
characteristics.

```bash
aws mgn describe-source-servers \
  --query 'items[0].{Server:sourceServerID,State:dataReplicationInfo.dataReplicationState}' 2>&1 | head -4
```

**Expected result:** the Application Migration Service (rehost) state, or an
empty list. **Decision to record:** rehost via MGN for lift-and-shift versus
replatform/refactor for a workload that would benefit from managed services;
justify the choice.

**Negative test:** refactoring everything up front stalls a migration that
a rehost-then-optimize approach would have completed on time.

**Cleanup:** none (read-only).

### Lab 12.19 — Determine a new architecture for existing workloads

**Objective:** Read a monolith's traffic to design a decomposition.

```bash
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB \
  --metric-name RequestCount --dimensions Name=LoadBalancer,Value=$ALB_NAME \
  --start-time $(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 3600 --statistics Sum \
  --query 'Datapoints | length(@)' --output text
```

**Expected result:** hourly request datapoints. **Decision to record:** the
target architecture (containers on ECS/EKS, or serverless) chosen from the
traffic shape — bursty favors serverless, steady favors containers.

**Negative test:** re-hosting a monolith unchanged carries its scaling
limits into the cloud.

**Cleanup:** none (read-only).

### Lab 12.20 — Determine opportunities for modernization and enhancements

**Objective:** Identify self-managed components a managed service could
replace.

```bash
aws rds describe-db-instances \
  --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,MultiAZ:MultiAZ}' --output table 2>&1 | head
```

**Expected result:** the RDS estate and its Multi-AZ status. **Decision to
record:** modernize a single-AZ, self-tuned database to Aurora (managed
failover, autoscaling storage); record the operational burden removed.

**Negative test:** keeping a self-managed database forgoes the managed
resilience the exam expects you to recommend.

**Cleanup:** none (read-only).

**DevOps Engineer – Professional (DOP-C02) — Labs 12.21–12.39**

### Lab 12.21 — Implement CI/CD pipelines

**Objective:** Create a CodePipeline skeleton with source and build stages.

```bash
aws codepipeline create-pipeline --cli-input-json '{"pipeline":{"name":"dop-pipe","roleArn":"'"$ROLE_ARN"'","artifactStore":{"type":"S3","location":"'"$BUCKET"'"},"stages":[{"name":"Source","actions":[{"name":"S3","actionTypeId":{"category":"Source","owner":"AWS","provider":"S3","version":"1"},"configuration":{"S3Bucket":"'"$BUCKET"'","S3ObjectKey":"src.zip"},"outputArtifacts":[{"name":"src"}]}]},{"name":"Build","actions":[{"name":"Build","actionTypeId":{"category":"Build","owner":"AWS","provider":"CodeBuild","version":"1"},"configuration":{"ProjectName":"dva-test"},"inputArtifacts":[{"name":"src"}]}]}]}}' \
  --query 'pipeline.name' --output text
```

**Expected result:** pipeline `dop-pipe` created with source→build — an
automated path from commit to build.

**Negative test:** a stage referencing a nonexistent CodeBuild project fails
at execution, surfacing the broken link.

**Cleanup:** `aws codepipeline delete-pipeline --name dop-pipe`.

### Lab 12.22 — Integrate automated testing into CI/CD pipelines

**Objective:** Add a test phase to a buildspec so failing tests block the
pipeline.

```bash
aws codebuild update-project --name dva-test \
  --source '{"type":"NO_SOURCE","buildspec":"version: 0.2\nphases:\n  build:\n    commands:\n      - python -m pytest -q"}' \
  --query 'project.name' --output text
```

**Expected result:** the project now runs `pytest` with no `|| true` — a
non-zero test result fails the build and stops promotion.

**Negative test:** with `|| true` restored, failing tests are masked and bad
code promotes — the anti-pattern.

**Cleanup:** none (project reused; delete in Lab 11.9 cleanup).

### Lab 12.23 — Build and manage artifacts

**Objective:** Publish a versioned artifact to CodeArtifact.

```bash
aws codeartifact create-domain --domain dop-dom --query 'domain.name' --output text
aws codeartifact create-repository --domain dop-dom --repository dop-repo \
  --query 'repository.name' --output text
```

**Expected result:** a domain and repository — a governed, versioned store
for build outputs and dependencies.

**Negative test:** resolving a package version that was never published
returns `404`, proving artifacts must be published before consumption.

**Cleanup:** delete the repository and domain.

### Lab 12.24 — Implement deployment strategies for instances, containers, serverless

**Objective:** Configure a blue/green deployment group for ECS.

```bash
aws deploy create-deployment-group --application-name dva-cd \
  --deployment-group-name dop-bg --service-role-arn "$ROLE_ARN" \
  --deployment-style deploymentType=BLUE_GREEN,deploymentOption=WITH_TRAFFIC_CONTROL \
  --query 'deploymentGroupId' --output text 2>&1 | head -1
```

**Expected result:** a blue/green deployment group — new tasks come up
alongside old, then traffic shifts, enabling instant rollback.

**Negative test:** an in-place deploy has no parallel environment, so
rollback means redeploying the previous version under an outage.

**Cleanup:** `aws deploy delete-deployment-group --application-name dva-cd --deployment-group-name dop-bg`.

### Lab 12.25 — Define reusable IaC components

**Objective:** Register a reusable module in the CloudFormation registry.

```bash
aws cloudformation list-types --type MODULE --visibility PRIVATE \
  --query 'TypeSummaries[].TypeName' --output text 2>&1 | head -1
aws cloudformation validate-template --template-body file:///tmp/vpc.yaml \
  --query 'Description' --output text 2>&1 | head -1
```

**Expected result:** existing private modules (if any) and a valid template
— reusable infrastructure defined once and consumed many times.

**Negative test:** copy-pasting the same VPC block across stacks drifts over
time; a module keeps one definition authoritative.

**Cleanup:** none (read-only / validate only).

### Lab 12.26 — Deploy automation to create and secure accounts at scale

**Objective:** Deploy a guardrail to every account in an OU with a
StackSet.

```bash
aws cloudformation create-stack-set --stack-set-name dop-guardrail \
  --template-body file:///tmp/vpc.yaml --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --query 'StackSetId' --output text 2>&1 | head -1
```

**Expected result:** a service-managed StackSet that auto-deploys to new
accounts in the target OUs — account baselines at scale.

**Negative test:** a self-managed StackSet requires manual role setup per
account; forgetting one leaves an ungoverned account.

**Cleanup:** `aws cloudformation delete-stack-set --stack-set-name dop-guardrail`.

### Lab 12.27 — Design automated solutions for complex, large-scale tasks

**Objective:** Fan out a large task with Step Functions Map state.

```bash
aws stepfunctions create-state-machine --name dop-fan-out --role-arn "$ROLE_ARN" \
  --definition '{"StartAt":"Map","States":{"Map":{"Type":"Map","ItemsPath":"$.items","MaxConcurrency":40,"Iterator":{"StartAt":"Work","States":{"Work":{"Type":"Pass","End":true}}},"End":true}}}' \
  --query 'stateMachineArn' --output text
```

**Expected result:** a state machine that processes items with bounded
concurrency (40) — large-scale work without hand-rolled queue plumbing.

**Negative test:** unbounded concurrency (`MaxConcurrency:0`) can overwhelm a
downstream service; the bound is the back-pressure control.

**Cleanup:** delete the state machine.

### Lab 12.28 — Implement highly available solutions

**Objective:** Confirm a data tier is Multi-AZ for automatic failover.

```bash
aws rds modify-db-instance --db-instance-identifier "$DB" --multi-az --apply-immediately \
  --query 'DBInstance.MultiAZ' --output text 2>&1 | head -1
```

**Expected result:** `true` (pending) — a standby in a second AZ takes over
automatically on primary failure.

**Negative test:** a single-AZ instance failing takes an outage until a
manual restore; Multi-AZ removes that manual step.

**Cleanup:** revert with `--no-multi-az` if this was a test instance.

### Lab 12.29 — Implement scalable solutions

**Objective:** Attach a target-tracking scaling policy to an ASG.

```bash
aws autoscaling put-scaling-policy --auto-scaling-group-name soa-asg \
  --policy-name cpu-target --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50.0}' \
  --query 'PolicyARN' --output text 2>&1 | head -1
```

**Expected result:** a policy holding average CPU at 50% — capacity tracks
demand automatically.

**Negative test:** a step policy with a too-wide cooldown reacts too slowly
to a spike; target-tracking self-tunes.

**Cleanup:** `aws autoscaling delete-policy --auto-scaling-group-name soa-asg --policy-name cpu-target`.

### Lab 12.30 — Implement automated recovery to meet RTO and RPO

**Objective:** Read backup recovery-point timestamps to verify RPO.

```bash
aws backup list-recovery-points-by-backup-vault --backup-vault-name Default \
  --query 'RecoveryPoints[0].{Created:CreationDate,Status:Status}' 2>&1 | head -4
```

**Expected result:** the newest recovery point's age. **Decision to
record:** whether the backup frequency meets the RPO; if the gap exceeds
RPO, increase frequency or add continuous backup.

**Negative test:** a daily backup cannot meet a 1-hour RPO — the mismatch
this check catches before an incident.

**Cleanup:** none (read-only).

### Lab 12.31 — Configure collection, aggregation, and storage of logs and metrics

**Objective:** Centralize logs by creating a CloudWatch Logs destination /
subscription.

```bash
aws logs put-subscription-filter --log-group-name /aws/lambda/dva-fn \
  --filter-name central --filter-pattern "" \
  --destination-arn "$FIREHOSE_ARN" --role-arn "$ROLE_ARN"
aws logs describe-subscription-filters --log-group-name /aws/lambda/dva-fn \
  --query 'subscriptionFilters[0].destinationArn' --output text
```

**Expected result:** a subscription streaming all log events to a central
sink — aggregation across accounts/services.

**Negative test:** logs left in per-service groups cannot be correlated in
one query; centralization is what enables cross-service analysis.

**Cleanup:** `aws logs delete-subscription-filter --log-group-name /aws/lambda/dva-fn --filter-name central`.

### Lab 12.32 — Audit, monitor, and analyze logs and metrics to detect issues

**Objective:** Build a metric filter that turns an error signature into an
alarmed metric.

```bash
aws logs put-metric-filter --log-group-name /aws/lambda/dva-fn \
  --filter-name 5xx --filter-pattern '{ $.statusCode = 5* }' \
  --metric-transformations metricName=Http5xx,metricNamespace=DOP,metricValue=1
aws logs describe-metric-filters --log-group-name /aws/lambda/dva-fn \
  --query 'metricFilters[?filterName==`5xx`].metricTransformations[0].metricName' --output text
```

**Expected result:** `Http5xx` — a JSON-aware filter that detects 5xx
responses and feeds an alarm.

**Negative test:** a plain-text pattern misses structured JSON fields; the
JSON selector is what makes the detection reliable.

**Cleanup:** delete the metric filter.

### Lab 12.33 — Automate monitoring and event management of complex environments

**Objective:** Route findings automatically with an EventBridge rule.

```bash
aws events put-rule --name dop-guardduty --event-pattern \
  '{"source":["aws.guardduty"],"detail-type":["GuardDuty Finding"]}' \
  --query 'RuleArn' --output text
```

**Expected result:** a rule matching GuardDuty findings — monitoring events
are routed to automation (SNS, Lambda, ticketing) without polling.

**Negative test:** an event pattern with a typo in `source` matches nothing,
so findings are silently missed — validate patterns against sample events.

**Cleanup:** `aws events delete-rule --name dop-guardduty`.

### Lab 12.34 — Manage event sources to process, notify, and act on events

**Objective:** Add an SNS target to the rule so events notify responders.

```bash
TOPIC=$(aws sns create-topic --name dop-alerts --query TopicArn --output text)
aws events put-targets --rule dop-guardduty \
  --targets "Id=1,Arn=$TOPIC"
aws events list-targets-by-rule --rule dop-guardduty --query 'Targets[0].Arn' --output text
```

**Expected result:** the SNS topic wired as the rule target — events now
fan out to subscribers and downstream actions.

**Negative test:** a target whose resource policy denies EventBridge silently
drops deliveries; the topic policy must allow `events.amazonaws.com`.

**Cleanup:** remove the target and delete the topic.

### Lab 12.35 — Implement configuration changes in response to events

**Objective:** Auto-remediate a Config rule violation with an SSM document.

```bash
aws configservice put-remediation-configurations --remediation-configurations \
  '[{"ConfigRuleName":"s3-ssl-only","TargetType":"SSM_DOCUMENT","TargetId":"AWSConfigRemediation-SetS3BucketEncryption","Automatic":true,"MaximumAutomaticAttempts":3,"RetryAttemptSeconds":60,"Parameters":{"AutomationAssumeRole":{"StaticValue":{"Values":["'"$ROLE_ARN"'"]}},"BucketName":{"ResourceValue":{"Value":"RESOURCE_ID"}}}}]' \
  2>&1 | head -1
```

**Expected result:** an automatic remediation bound to the rule — a
noncompliant bucket is fixed without human action.

**Negative test:** remediation with a role lacking the target permission
fails on execution; the config change never applies.

**Cleanup:** `aws configservice delete-remediation-configuration --config-rule-name s3-ssl-only`.

### Lab 12.36 — Troubleshoot system and application failures

**Objective:** Correlate a failure across services with a CloudWatch Logs
Insights cross-group query.

```bash
aws logs start-query --log-group-names /aws/lambda/dva-fn /ans/flow-logs \
  --start-time $(($(date +%s)-3600)) --end-time $(date +%s) \
  --query-string 'fields @timestamp,@log,@message | sort @timestamp desc | limit 20' \
  --query 'queryId' --output text
```

**Expected result:** a query ID spanning application and network logs — one
timeline to locate where the failure originated.

**Negative test:** querying a single log group hides a fault that lives at
the boundary between services.

**Cleanup:** none (read-only query).

### Lab 12.37 — Implement identity and access management at scale

**Objective:** Enforce a permission boundary so delegated admins cannot
escalate.

```bash
aws iam create-policy --policy-name dop-boundary \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:*","logs:*"],"Resource":"*"},{"Effect":"Deny","Action":["iam:*","organizations:*"],"Resource":"*"}]}' \
  --query 'Policy.Arn' --output text
```

**Expected result:** a boundary policy ARN — attaching it caps any role's
effective permissions regardless of its own policy, enabling safe
delegation at scale.

**Negative test:** a delegated role without a boundary can grant itself
`iam:*` and escalate; the boundary is what prevents it.

**Cleanup:** delete the policy.

### Lab 12.38 — Apply automation for security controls and data protection

**Objective:** Auto-enable default EBS encryption org-wide via an SCP-style
control (account-level here).

```bash
aws ec2 enable-ebs-encryption-by-default --query 'EbsEncryptionByDefault' --output text
aws ec2 get-ebs-encryption-by-default --query 'EbsEncryptionByDefault' --output text
```

**Expected result:** `True` — data-at-rest protection enforced by default,
the pattern an SCP would replicate across every account.

**Negative test:** relying on developers to tick "encrypt" per volume leaves
gaps; the default closes them automatically.

**Cleanup:** leave enabled (secure default).

### Lab 12.39 — Implement security monitoring and auditing solutions

**Objective:** Confirm an organization-wide CloudTrail is logging.

```bash
aws cloudtrail describe-trails \
  --query 'trailList[].{Name:Name,Org:IsOrganizationTrail,Multi:IsMultiRegionTrail}' --output table
```

**Expected result:** a trail with `IsOrganizationTrail=true` and
`IsMultiRegionTrail=true` — a tamper-evident audit record across every
account and Region.

**Negative test:** a single-Region trail misses activity in other Regions —
a blind spot an org, multi-Region trail eliminates.

**Cleanup:** none (read-only).

**Generative AI Developer – Professional (AIP-C01) — Labs 12.40–12.59**

### Lab 12.40 — Analyze requirements and design GenAI solutions

**Objective:** Read the available FMs and their modalities to match a
requirement to a model.

```bash
aws bedrock list-foundation-models --region us-east-1 \
  --query "modelSummaries[?contains(outputModalities,'TEXT')].[modelId,providerName]" --output table | head
```

**Expected result:** text-capable models by provider. **Decision to record:**
the model chosen for the requirement (latency vs quality vs cost) and the
rejected alternative.

**Negative test:** choosing a model by name without checking modality/Region
availability produces a design that cannot deploy.

**Cleanup:** none (read-only).

### Lab 12.41 — Select and configure FMs

**Objective:** Read a model's inference parameters and request throughput.

```bash
aws bedrock get-foundation-model --region us-east-1 \
  --model-identifier amazon.titan-text-express-v1 \
  --query 'modelDetails.{In:inputModalities,Out:outputModalities,Streaming:responseStreamingSupported}'
```

**Expected result:** the model's modalities and streaming support.
**Decision to record:** the inference config (temperature, max tokens) and
whether provisioned throughput is needed for the workload's rate.

**Negative test:** on-demand throughput throttles under high concurrency;
the exam expects provisioned throughput for guaranteed rates.

**Cleanup:** none (read-only).

### Lab 12.42 — Implement data validation and processing pipelines for FM consumption

**Objective:** Validate and chunk source documents before indexing.

```bash
aws s3api put-object --bucket "$BUCKET" --key rag/docs/policy.txt --body /tmp/policy.txt
aws s3api head-object --bucket "$BUCKET" --key rag/docs/policy.txt \
  --query 'ContentLength' --output text
```

**Expected result:** the document's byte length — the input a chunking
pipeline validates (encoding, size limits) before embedding.

**Negative test:** feeding an oversized document that is not chunked exceeds the
embedding model's token limit and the ingestion fails.

**Cleanup:** delete the `rag/docs/` objects.

### Lab 12.43 — Design and implement vector store solutions

**Objective:** Create an OpenSearch Serverless collection to hold
embeddings.

```bash
aws opensearchserverless create-collection --name aip-vectors --type VECTORSEARCH \
  --query 'createCollectionDetail.status' --output text 2>&1 | head -1
```

**Expected result:** a `CREATING` vector-search collection — the store for
semantic retrieval. **Cost:** OpenSearch Serverless bills OCU-hours; delete
promptly.

**Negative test:** creating the collection without a matching
encryption/network security policy leaves it unreachable — the policies are
prerequisites, not options.

**Cleanup:** `aws opensearchserverless delete-collection --id <id>`.

### Lab 12.44 — Design retrieval mechanisms for FM augmentation

**Objective:** Create a Bedrock Knowledge Base binding the store to a model
for RAG.

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1 \
  --query 'knowledgeBaseSummaries[].{Name:name,Status:status}' --output table 2>&1 | head
```

**Expected result:** existing knowledge bases, or an empty list — the
managed retrieval layer that grounds model answers in your data.

**Negative test:** answering from the model alone (no retrieval) hallucinates
on private facts; retrieval augmentation is the fix.

**Cleanup:** none (read-only); delete any KB created for the lab.

### Lab 12.45 — Implement prompt engineering strategies and governance

**Objective:** Store a governed prompt template in Bedrock Prompt
Management.

```bash
aws bedrock-agent list-prompts --region us-east-1 \
  --query 'promptSummaries[].name' --output text 2>&1 | head -1
```

**Expected result:** managed prompts (if any) — versioned, reviewable
templates rather than prompts scattered in code.

**Negative test:** inline prompts edited ad hoc drift and cannot be audited;
a managed template is versioned and governed.

**Cleanup:** none (read-only); delete any prompt created.

### Lab 12.46 — Implement agentic AI solutions and tool integrations

**Objective:** List Bedrock Agents and their action groups (tools).

```bash
aws bedrock-agent list-agents --region us-east-1 \
  --query 'agentSummaries[].{Name:agentName,Status:agentStatus}' --output table 2>&1 | head
```

**Expected result:** any agents defined — an agent orchestrates tools (Lambda
action groups) to complete multi-step tasks.

**Negative test:** an agent with no action group can only chat; without tools
it cannot take action in your systems.

**Cleanup:** none (read-only); delete any agent created.

### Lab 12.47 — Implement model deployment strategies

**Objective:** Reserve provisioned throughput for predictable latency.

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1 \
  --query 'provisionedModelSummaries[].{Model:modelArn,Units:modelUnits,Status:status}' \
  --output table 2>&1 | head
```

**Expected result:** provisioned throughput reservations (if any).
**Decision to record:** on-demand for spiky/dev, provisioned for
steady/production SLA — with the cost of each. **Cost:** provisioned
throughput bills hourly; do not create one casually.

**Negative test:** a production endpoint on on-demand throttles under load,
violating the latency SLA.

**Cleanup:** none (read-only).

### Lab 12.48 — Design and implement enterprise integration architectures

**Objective:** Front the model with an API Gateway + Lambda so enterprise
apps consume it over a governed API.

```bash
API=$(aws apigatewayv2 create-api --name aip-api --protocol-type HTTP \
  --query 'ApiId' --output text)
aws apigatewayv2 get-api --api-id "$API" --query 'ApiEndpoint' --output text
```

**Expected result:** an HTTP API endpoint — the integration seam where auth,
throttling, and logging are applied before requests reach the model.

**Negative test:** exposing Bedrock credentials directly to client apps
removes the governance layer the API provides.

**Cleanup:** `aws apigatewayv2 delete-api --api-id "$API"`.

### Lab 12.49 — Implement FM API integrations

**Objective:** Invoke a model via the Converse API (the unified integration
surface).

```bash
aws bedrock-runtime converse --region us-east-1 \
  --model-id amazon.titan-text-express-v1 \
  --messages '[{"role":"user","content":[{"text":"Reply with the single word: ready"}]}]' \
  --query 'output.message.content[0].text' --output text
```

**Expected result:** `ready` — a normalized request/response that works
across providers, simplifying integration. **Cost:** a few tokens.

**Negative test:** a per-provider bespoke payload breaks when the model is
swapped; Converse abstracts that difference.

**Cleanup:** none.

### Lab 12.50 — Implement application integration patterns and development tools

**Objective:** Add asynchronous processing with an SQS queue between the app
and the model worker.

```bash
QUEUE_URL=$(aws sqs create-queue --queue-name aip-jobs --query QueueUrl --output text)
aws sqs send-message --queue-url "$QUEUE_URL" --message-body '{"prompt":"summarize doc 1"}' \
  --query 'MessageId' --output text
```

**Expected result:** a queued job ID — a decoupled pattern that smooths
bursty GenAI workloads and enables retries.

**Negative test:** synchronous invocation under a burst hits rate limits and
drops requests; the queue absorbs the spike.

**Cleanup:** `aws sqs delete-queue --queue-url "$QUEUE_URL"`.

### Lab 12.51 — Implement input and output safety controls

**Objective:** Apply a Bedrock Guardrail to a model call and confirm it
filters.

```bash
aws bedrock list-guardrails --region us-east-1 \
  --query 'guardrails[].{Name:name,Id:id,Status:status}' --output table 2>&1 | head
```

**Expected result:** available guardrails — the input/output filter that
blocks unsafe content and denied topics.

**Negative test:** send a denied-topic prompt through a call with no
guardrail; it is answered, the risk guardrails remove.

**Cleanup:** none (read-only); reuse the guardrail from Lab 10.30.

### Lab 12.52 — Implement data security and privacy controls

**Objective:** Add PII filtering via a guardrail sensitive-information
policy.

```bash
aws bedrock get-guardrail --region us-east-1 --guardrail-identifier "$GUARDRAIL_ID" \
  --query 'sensitiveInformationPolicy.piiEntitiesConfig[].{Type:type,Action:action}' \
  --output table 2>&1 | head
```

**Expected result:** the PII entity rules (e.g. `EMAIL: ANONYMIZE`) — private
data is masked before it reaches or leaves the model.

**Negative test:** without a sensitive-information policy, PII in prompts is
sent to and logged by the model, a privacy violation.

**Cleanup:** none (read-only).

### Lab 12.53 — Implement AI governance and compliance mechanisms

**Objective:** Confirm model-invocation logging feeds the compliance audit
trail.

```bash
aws bedrock get-model-invocation-logging-configuration --region us-east-1 \
  --query 'loggingConfig.{CW:cloudWatchConfig.logGroupName,S3:s3Config.bucketName}' 2>&1 | head -4
```

**Expected result:** the CloudWatch and/or S3 sinks capturing every
invocation — the record auditors and AI regulations require.

**Negative test:** logging disabled means no evidence of what the model was
asked or answered — a compliance gap.

**Cleanup:** none (read-only).

### Lab 12.54 — Implement responsible AI principles

**Objective:** Create a guardrail denied-topics policy that encodes a
responsible-use boundary.

```bash
aws bedrock create-guardrail --region us-east-1 --name aip-responsible \
  --blocked-input-messaging "Blocked." --blocked-outputs-messaging "Blocked." \
  --topic-policy-config '{"topicsConfig":[{"name":"medical-advice","definition":"Diagnosis or treatment guidance","type":"DENY"}]}' \
  --query 'guardrailId' --output text
```

**Expected result:** a guardrail that refuses medical-advice requests — a
codified responsible-AI limit, not a documentation promise.

**Negative test:** ask for medical advice through the guardrail; it is
blocked with your message, proving the principle is enforced.

**Cleanup:** `aws bedrock delete-guardrail --guardrail-identifier <id>`.

### Lab 12.55 — Implement cost optimization and resource efficiency strategies

**Objective:** Read invocation logs to choose a cheaper model for simple
calls.

```bash
aws logs filter-log-events --log-group-name /ai/bedrock-audit \
  --filter-pattern '{ $.modelId = "*" }' --limit 5 \
  --query 'events[].message' 2>&1 | head -3
```

**Expected result:** sampled invocations with their model IDs. **Decision to
record:** route short/simple prompts to a smaller model (e.g. Titan Lite)
and reserve a large model for complex tasks; record the projected saving.

**Negative test:** using the largest model for every call overspends on
prompts a small model answers just as well.

**Cleanup:** none (read-only).

### Lab 12.56 — Optimize application performance

**Objective:** Enable response streaming to cut time-to-first-token.

```bash
aws bedrock get-foundation-model --region us-east-1 \
  --model-identifier amazon.titan-text-express-v1 \
  --query 'modelDetails.responseStreamingSupported' --output text
```

**Expected result:** `true` — streaming lets the app render tokens as they
arrive instead of waiting for the full completion, improving perceived
latency.

**Negative test:** a non-streaming call makes the user wait for the entire
response; streaming is the perceived-performance win.

**Cleanup:** none (read-only).

### Lab 12.57 — Implement monitoring systems for GenAI applications

**Objective:** Alarm on Bedrock invocation errors via CloudWatch.

```bash
aws cloudwatch put-metric-alarm --alarm-name aip-invocation-errors \
  --namespace AWS/Bedrock --metric-name InvocationClientErrors \
  --statistic Sum --period 300 --evaluation-periods 1 --threshold 5 \
  --comparison-operator GreaterThanThreshold
aws cloudwatch describe-alarms --alarm-names aip-invocation-errors \
  --query 'MetricAlarms[0].Namespace' --output text
```

**Expected result:** `AWS/Bedrock` — an alarm watching client-side
invocation errors (throttling, validation), the health signal for a GenAI
app.

**Negative test:** monitoring only the app tier misses Bedrock-side
throttling that degrades responses.

**Cleanup:** `aws cloudwatch delete-alarms --alarm-names aip-invocation-errors`.

### Lab 12.58 — Implement evaluation systems for GenAI

**Objective:** List Bedrock model-evaluation jobs to score quality
systematically.

```bash
aws bedrock list-evaluation-jobs --region us-east-1 \
  --query 'jobSummaries[].{Name:jobName,Status:status,Type:evaluationTaskTypes}' \
  --output table 2>&1 | head
```

**Expected result:** evaluation jobs (if any) — automated scoring on
accuracy, toxicity, and robustness across a dataset.

**Negative test:** judging a model by a handful of manual prompts gives an
unrepresentative verdict; systematic evaluation is the fix.

**Cleanup:** none (read-only).

### Lab 12.59 — Troubleshoot GenAI applications

**Objective:** Diagnose a failed invocation from its logged error.

```bash
aws logs filter-log-events --log-group-name /ai/bedrock-audit \
  --filter-pattern '{ $.errorCode = "*" }' --limit 5 \
  --query 'events[].message' 2>&1 | head -3
```

**Expected result:** invocations that carried an error code (throttling,
access denied, validation) — the specific fault, not a generic "it broke."

**Negative test:** troubleshooting without invocation logging leaves only
the client-side symptom; the logged `errorCode` names the real cause.

**Cleanup:** none (read-only).

### Lab 12.60 — Professional-tier pacing and trade-off drill (integrative)

**Objective:** Measure your professional-tier pacing and trade-off
reasoning — the two things that actually gate this tier — before committing
to a study plan.

**Cost note:** The Cost Explorer query is free. The deployment drill uses
CodeDeploy and compute in the sandbox; step 6 cleans up.

**Prerequisites**

- The sandbox account and budget alarm from Chapter 10.
- The Chapter 6 DR architecture (for the trade-off drill) or the Chapter 7
  pipeline material (for the rollback drill).
- A timer, and a source of full-length scenario questions (AWS Skill
  Builder's official practice material).

**Steps**

1. **Pacing baseline (timed, 60 minutes).** Complete one 25-question block
   of full-length scenario questions against the clock, using
   flag-and-move.

   **Expected result:** a completion time and a flagged-question count. At
   or under 60 minutes with fewer than 5 flags is a healthy baseline.

2. **Trade-off drill (target 30 minutes).** Run the Cost Explorer query
   against your sandbox, then write the answer to the RTO-relaxation
   question in the Implementation section — which services you would
   remove, and what you would lose.

   **Expected result:** a written trade-off argument naming the constraint
   driving each removal, not just a cheaper architecture.

3. **Rollback drill (target 30 minutes).** For DOP-C02 candidates, force
   the rollback path and confirm the previous revision serves traffic and
   the guarding alarm fired.

   **Expected result:** a proven rollback, with evidence the alarm — not
   you — would have caught the bad release.

4. **Cross-domain test (target 20 minutes).** Answer one scenario spanning
   identity, networking, storage, and cost end to end, unaided.

   **Expected result:** a coherent answer, or an identified integration gap
   between domains you each know individually.

5. **Decide the plan.** If pacing was the constraint, schedule pacing
   rehearsals before further content study. If content, target the weakest
   domain from step 4.

   **Expected result:** a plan whose first action is aimed at your actual
   constraint.

6. **Cleanup:** stop and delete the lab deployment and any compute it
   created, revert SCP or organizational changes, and confirm the budget
   alarm shows no unexpected spend.

## Lab Verification

Complete this sign-off once the pacing baseline and at least one drill have
been completed and the sandbox is clean. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The professional tier holds three certifications — Solutions Architect
(SAP-C02), DevOps Engineer (DOP-C02), and the new Generative AI Developer
(AIP-C01) — each 180 minutes and 75 questions. What changes from associate
is scope, not obscurity: multi-paragraph scenarios that reward reading
pace, trade-off judgment against stated constraints, breadth across
services within a single question, and design at organizational rather than
workload scale. SAP-C02 and DOP-C02 rest on this volume's Chapters 2, 3, 6,
and 7 and overlap enough that the second is much cheaper than the first.
AIP-C01 is a separate project this volume does not prepare. AWS requires no
associate first, but assumes roughly two years of hands-on experience —
treat that expectation, not the absent rule, as the real gate.

- [ ] Can name the three professional certifications and their codes.
- [ ] Can state the four things that change at this tier.
- [ ] Has computed the per-question time budget and rehearsed flag-and-move.
- [ ] Can argue a service is the *wrong* choice under a stated constraint.
- [ ] Knows why AIP-C01 needs study outside this volume.
- [ ] Has measured a pacing baseline before planning content study.
- [ ] Completed the hands-on lab, including cleanup and a cost check.
