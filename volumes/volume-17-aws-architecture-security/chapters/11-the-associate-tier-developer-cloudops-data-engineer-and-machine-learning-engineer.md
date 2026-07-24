# Chapter 11: The Associate Tier — Developer, CloudOps Engineer, Data Engineer, and Machine Learning Engineer

![Five associate certifications shown as role columns above the volume chapters that prepare them. Solutions Architect Associate (SAA-C03) is already covered by Chapters 1 to 9. Developer Associate (DVA-C02) targets application builders, drawing on Chapter 4 compute and Chapter 7 observability. CloudOps Engineer Associate (SOA-C03), renamed from SysOps Administrator, targets operators, drawing on Chapters 6 and 7. Data Engineer Associate (DEA-C01) targets data pipeline builders, drawing on Chapter 5. Machine Learning Engineer Associate (MLA-C01, updating to MLA-C02 with registration opening 1 September 2026) reaches beyond this volume into SageMaker and MLOps. All five are 130 minutes and 65 questions, sit at the same tier, and none requires another.](../../../diagrams/volume-17-aws-architecture-security/chapter-11-associate-tier-role-map.svg)

*Figure 11-1. The associate tier as five roles at one depth. The chapters below each column are what this volume already gives you toward that exam.*

## Learning Objectives

- Identify the five associate-tier AWS certifications and their codes, and
  match each to the job role it is designed around.
- Explain what changed when SysOps Administrator – Associate became
  **CloudOps Engineer – Associate**, and what did not.
- Track the **MLA-C01 to MLA-C02** transition on Machine Learning Engineer –
  Associate and decide which version to prepare against.
- Map each associate exam onto the chapters of this volume that prepare it,
  and identify precisely where this volume stops and separate study begins.
- Choose which associate certifications are worth your time, and recognize
  when a second one is a cheap increment versus an expensive detour.

## Theory and Architecture

The associate tier is where most AWS certification effort belongs. It has
five certifications, all at the same depth — 130 minutes, 65 questions —
each shaped around a different job role. This volume already carries one of
them end to end; this chapter maps the other four.

This is study and review material organized against published structure. It
reproduces no exam content. Codes were verified against AWS's certification
pages on 23 July 2026; confirm before scheduling.

### The five associate certifications

| Certification | Code | The role it is built around |
| --- | --- | --- |
| Solutions Architect – Associate | SAA-C03 | Designs cost- and performance-optimized solutions |
| Developer – Associate | DVA-C02 | Develops, tests, deploys, and debugs cloud applications |
| CloudOps Engineer – Associate | SOA-C03 | Deploys, manages, and operates workloads |
| Data Engineer – Associate | DEA-C01 | Builds data models and pipelines; owns data life cycle and quality |
| Machine Learning Engineer – Associate | MLA-C01 | Builds, deploys, and operates ML solutions |

**Solutions Architect – Associate (SAA-C03)** is the one this volume
already covers: [Chapters 1–9](01-cloud-foundations-accounts-and-well-architected-design.md)
are built around it, and
[Chapter 9](09-solutions-architect-and-security-training-capstone.md)
carries its domain map and capstone. Nothing further is needed here.

### CloudOps Engineer — a rename, not a new exam

**CloudOps Engineer – Associate (SOA-C03)** is the certification formerly
called **SysOps Administrator – Associate**. This matters practically:

- The **role name changed**; the `SOA` code prefix did not, which is why
  the current code still reads `SOA-C03` rather than something new.
- Study material, forum posts, and job descriptions written before the
  rename will say "SysOps Administrator" for the same credential. Treat
  the two names as the same thing, and check the code — `SOA-C03` — rather
  than the name when confirming a resource is current.
- The renaming tracks a real shift in emphasis toward cloud operations
  broadly (reliability, monitoring, automation, incident response) rather
  than system administration narrowly.

Its content maps onto this volume's
[Chapter 6](06-reliability-migration-multi-region-and-disaster-recovery.md)
(reliability, failover, recovery) and
[Chapter 7](07-observability-automation-performance-and-cost-governance.md)
(CloudWatch, Systems Manager, infrastructure as code, cost governance) more
than any others.

### Machine Learning Engineer — a version transition in progress

**Machine Learning Engineer – Associate** is mid-transition, and the dates
matter:

- The current exam is **MLA-C01**.
- AWS states the exam is being updated, and **registration for the updated
  version (MLA-C02) opens 1 September 2026**.
- A beta of the updated exam (**ME1-C02**) is offered in English only.

If you are preparing now and can sit the exam before the changeover, MLA-C01
is the target. If your study plan runs past the changeover, prepare against
MLA-C02's guide once it publishes rather than finishing against a blueprint
that is being replaced. This is the same judgment call the encyclopedia
records for Cisco's SCOR v1.1→v2.0 window — plan against the version your
test date falls in.

This exam also reaches furthest beyond this volume. Chapter 5 supplies the
data and storage foundations, but SageMaker, feature engineering, model
deployment, and MLOps are not covered here; budget separate study.

### Developer and Data Engineer

- **Developer – Associate (DVA-C02)** tests building, deploying, and
  debugging applications on AWS: Lambda and container deployment patterns,
  SDK usage, API integration, CI/CD, and application-level observability
  and troubleshooting. It leans on
  [Chapter 4](04-compute-containers-serverless-and-application-architecture.md)
  for compute, containers, and serverless, and
  [Chapter 7](07-observability-automation-performance-and-cost-governance.md)
  for instrumentation. It assumes you can actually write code — this is the
  most code-dependent associate exam.
- **Data Engineer – Associate (DEA-C01)** tests designing data models,
  building and operating ingestion and transformation pipelines, and
  managing the data life cycle and data quality. It maps closely onto
  [Chapter 5](05-storage-databases-analytics-and-data-protection.md)'s
  storage, database, and analytics stack — S3, RDS/Aurora/DynamoDB, and the
  Redshift/Glue/Athena/Lake Formation surface. Its `-C01` suffix marks it as
  a first-generation blueprint on a relatively young certification, which
  means fewer mature third-party resources and more reason to work from
  AWS's own material.

### The tier's real economics

Because all five share a depth and much of a service surface, the marginal
cost of a *second* associate certification in an adjacent role is far lower
than the first — the platform knowledge transfers and only the emphasis
changes. The marginal *value*, however, drops just as fast. Two associate
certifications spanning your actual responsibilities is a strong position;
five is a large investment that rarely reflects a real role.

## Design Considerations

- **Pick by the job you do, not by sequence.** These are peers, not steps.
  An engineer running production workloads should sit CloudOps Engineer
  before Developer regardless of which is more famous, and vice versa for
  an application team.
- **Check the code, not the name, for CloudOps Engineer.** Because
  SysOps Administrator and CloudOps Engineer name the same credential,
  resource currency is judged by `SOA-C03`, not by which title the cover
  uses.
- **Decide the ML Engineer version by your test date.** Sitting before the
  changeover means MLA-C01; a plan extending past 1 September 2026 should
  target MLA-C02's published guide rather than finishing against a
  superseded blueprint.
- **Expect a real gap for ML Engineer and a modest one elsewhere.**
  Developer, CloudOps, and Data Engineer are largely re-emphasis of
  material this volume already covers. ML Engineer requires substantial
  outside study — treat it as a separate project, not an extension.
- **A second associate is cheap; a fifth is not.** Sequence a second exam
  in an adjacent role close behind the first while the platform knowledge
  is fresh. Beyond two, ask what the credential actually changes about your
  work before committing the time.
- **Ethical preparation boundary.** AWS exam guides, Skill Builder,
  official training, and hands-on practice only. Anything claiming to
  reproduce live questions violates the certification agreement and is
  especially unreliable for `-C01` blueprints, where little accurate
  third-party material exists yet.

## Implementation and Automation

### An associate-tier study spine

```text
# Rate 1-5 per row. Below 3 means lab time in the listed chapters before
# booking. "Outside study" flags what this volume does not cover.

Exam (code)                  | Chapters   | Outside study needed        | Rating
-----------------------------|------------|-----------------------------|-------
Solutions Architect (SAA-C03)| 1-9        | none - fully covered        |
Developer (DVA-C02)          | 4, 7       | SDK/CI-CD coding practice   |
CloudOps Engineer (SOA-C03)  | 6, 7       | Systems Manager depth       |
Data Engineer (DEA-C01)      | 5          | Glue/EMR pipeline practice  |
ML Engineer (MLA-C01/C02)    | 5          | SageMaker, MLOps - large    |
```

### A Developer-exam drill: deploy, break, and trace a Lambda

```bash
# DVA-C02 rewards debugging fluency, not just deployment. Deploy the
# Chapter 4 Lambda, invoke it, then read its trace and logs unaided.
aws lambda invoke --function-name lab-demo-fn \
  --payload '{"test":true}' --cli-binary-format raw-in-base64-out /tmp/out.json
aws logs tail /aws/lambda/lab-demo-fn --since 5m --format short
# Then: introduce a permissions error deliberately and diagnose it from
# the log and trace alone before looking at the policy.
```

### A CloudOps-exam drill: prove an alarm actually fires

```bash
# SOA-C03 is operations-first. An alarm that has never fired is untested.
aws cloudwatch describe-alarms --alarm-names lab-cpu-high \
  --query 'MetricAlarms[0].[AlarmName,StateValue,ActionsEnabled]' --output text
# Force the state transition and confirm the notification arrives:
aws cloudwatch set-alarm-state --alarm-name lab-cpu-high \
  --state-value ALARM --state-reason "operational readiness drill"
```

### A Data Engineer drill: verify pipeline data quality, not just flow

```bash
# DEA-C01 emphasizes data quality and life cycle, not only movement.
# After running the Chapter 5 pipeline, check the catalog and row counts
# rather than assuming the job's success status means correct data.
aws glue get-table --database-name lab_db --name lab_table \
  --query 'Table.StorageDescriptor.Columns[].[Name,Type]' --output table
aws athena start-query-execution \
  --query-string 'SELECT count(*) FROM lab_db.lab_table' \
  --result-configuration OutputLocation=s3://lab-athena-results/
```

## Validation and Troubleshooting

- **Role fit is the first check.** If you cannot describe, in one sentence,
  the job the exam is built around and why it is your job, you have picked
  by reputation rather than by fit — the most common source of wasted
  associate-tier effort.
- **Code currency beats title currency.** For CloudOps Engineer especially,
  confirm a resource targets `SOA-C03`. A "SysOps Administrator" course is
  fine if its code matches and stale if it does not.
- **ML Engineer readiness is not readable from this volume.** If your
  self-rating for MLA is based only on Chapter 5, it is inflated. Rate it
  against SageMaker and MLOps material you have actually worked through.
- **Test the drill, not the deployment.** Each drill above ends in a
  verification step — a diagnosed error, a fired alarm, a row count —
  because all three exams reward proving a thing works, not asserting it.
  A deployment that was never exercised is not evidence of readiness.
- **Watch the changeover date.** If your ML Engineer study runs toward
  September 2026, re-check the exam page for MLA-C02's guide rather than
  discovering the change at registration.

## Security and Best Practices

- Run every drill in the dedicated sandbox account with the budget alarm
  from [Chapter 10](10-the-aws-certification-program-structure-foundational-tier-and-recertification.md),
  never in an account carrying production workloads — the CloudOps and
  Developer drills deliberately break things.
- Scope drill IAM roles to least privilege as
  [Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)
  teaches. Practising with an over-permissive role builds exactly the habit
  the Security material warns against, and the exams test the correct one.
- Deliberately introduced faults must be reverted before the sandbox is
  left unattended; a broken permission left in place becomes a confusing
  failure weeks later.
- Data Engineer and ML drills move real data volumes. Confirm S3 lifecycle
  rules and delete query results and intermediate datasets after each
  session — this is the cost trap of the data-oriented exams.

## References and Knowledge Checks

**References**

- [AWS Certified Developer – Associate](https://aws.amazon.com/certification/certified-developer-associate/) (DVA-C02)
- [AWS Certified CloudOps Engineer – Associate](https://aws.amazon.com/certification/certified-cloudops-engineer-associate/) (SOA-C03)
- [AWS Certified Data Engineer – Associate](https://aws.amazon.com/certification/certified-data-engineer-associate/) (DEA-C01)
- [AWS Certified Machine Learning Engineer – Associate](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) (MLA-C01; MLA-C02 registration opens 1 September 2026)
- [AWS Skill Builder](https://skillbuilder.aws/) — free exam-prep plans per
  certification.
- [Appendix — AWS Certifications and Course Access](../../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md)
- See [Chapter 10](10-the-aws-certification-program-structure-foundational-tier-and-recertification.md)
  for the program structure, and
  [Chapter 12](12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md)
  for the tier above.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any AWS exam item)*

1. Name the five associate certifications and the role each is built
   around, without looking back.
2. What changed and what stayed the same when SysOps Administrator –
   Associate became CloudOps Engineer – Associate?
3. Your exam date is October 2026 and you are studying Machine Learning
   Engineer. Which version should you prepare against, and why?
4. Which associate exam depends most on being able to write code, and which
   requires the most study outside this volume?
5. Explain why a second associate certification is cheaper than the first,
   and what should still make you hesitate before a third.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every task in the
four non-Solutions-Architect associate exam guides** — Developer (DVA-C02,
13 tasks), CloudOps Engineer (SOA-C03, 13), Data Engineer (DEA-C01, 17),
and Machine Learning Engineer (MLA-C01, 12) — 55 labs, each mapped in the
volume README's coverage tables. Solutions Architect – Associate (SAA-C03)
is the volume's architecture spine and its topic labs live in Chapters
01–07.

**Shared prerequisites for Labs 11.1–11.55**

- AWS CLI v2 authenticated to a sandbox account with developer/operator
  rights and a default Region set. Labs assume an execution role ARN in
  `$ROLE_ARN` and a scratch bucket in `$BUCKET` where noted.
- **Cost:** labs prefer create-then-describe-then-delete over running large
  compute. Any lab that can incur more than trivial cost (SageMaker
  training, Redshift, EMR, Firehose delivery) says so and stays at the
  setup/describe level with a cleanup step. Delete resources the same day.
- Every lab ends **`**Lab verified by:** *pending*`** until a human runs it.

**Developer – Associate (DVA-C02) — Labs 11.1–11.13**

### Lab 11.1 — Develop code for applications hosted on AWS

**Objective:** Register an ECS task definition — the deployable unit for a
containerized application.

```bash
aws ecs register-task-definition --family dva-app --network-mode awsvpc \
  --requires-compatibilities FARGATE --cpu 256 --memory 512 \
  --container-definitions '[{"name":"web","image":"public.ecr.aws/nginx/nginx:latest","essential":true}]' \
  --query 'taskDefinition.taskDefinitionArn' --output text
```

**Expected result:** a task-definition ARN ending `:dva-app:1` — a versioned
application artifact ready to run on Fargate.

**Negative test:** omit `--memory`; registration fails with
`ClientException` for a Fargate task, showing CPU/memory are required for
serverless compute.

**Cleanup:** `aws ecs deregister-task-definition --task-definition dva-app:1`.

### Lab 11.2 — Develop code for AWS Lambda

**Objective:** Create and invoke a Lambda function and read its response.

```bash
echo 'def handler(e,c): return {"ok": True, "event": e}' > /tmp/l.py && (cd /tmp && zip -q l.zip l.py)
aws lambda create-function --function-name dva-fn --runtime python3.12 \
  --role "$ROLE_ARN" --handler l.handler --zip-file fileb:///tmp/l.zip >/dev/null
aws lambda invoke --function-name dva-fn --payload '{"hello":"aws"}' \
  --cli-binary-format raw-in-base64-out /tmp/out.json && cat /tmp/out.json
```

**Expected result:** `{"ok": true, "event": {"hello": "aws"}}` — the
function ran and echoed its event.

**Negative test:** invoke with a malformed payload (`--payload 'not-json'`);
the call returns an `InvalidRequestContentException`.

**Cleanup:** `aws lambda delete-function --function-name dva-fn`.

### Lab 11.3 — Use data stores in application development

**Objective:** Write and read an item in DynamoDB.

```bash
aws dynamodb create-table --table-name dva-items \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST >/dev/null
aws dynamodb wait table-exists --table-name dva-items
aws dynamodb put-item --table-name dva-items --item '{"id":{"S":"a1"},"v":{"N":"42"}}'
aws dynamodb get-item --table-name dva-items --key '{"id":{"S":"a1"}}' --query 'Item.v.N' --output text
```

**Expected result:** `42` — the item round-trips through the data store.

**Negative test:** `get-item` with a key that omits the partition key fails
`ValidationException`, showing the key schema is mandatory.

**Cleanup:** `aws dynamodb delete-table --table-name dva-items`.

### Lab 11.4 — Implement authentication and/or authorization

**Objective:** Create a Cognito user pool — the managed identity store for
application auth.

```bash
POOL=$(aws cognito-idp create-user-pool --pool-name dva-pool \
  --query 'UserPool.Id' --output text)
aws cognito-idp create-user-pool-client --user-pool-id "$POOL" \
  --client-name dva-client --query 'UserPoolClient.ClientId' --output text
```

**Expected result:** a user-pool ID and an app-client ID — the auth surface
an application authenticates against.

**Negative test:** create a user with a password below the pool's policy
length; `InvalidPasswordException` proves the policy is enforced at signup.

**Cleanup:** `aws cognito-idp delete-user-pool --user-pool-id "$POOL"`.

### Lab 11.5 — Implement encryption by using AWS services

**Objective:** Encrypt and decrypt a value with a KMS key.

```bash
KID=$(aws kms create-key --description dva-key --query 'KeyMetadata.KeyId' --output text)
CT=$(aws kms encrypt --key-id "$KID" --plaintext "$(echo -n secret | base64)" \
  --query CiphertextBlob --output text)
aws kms decrypt --ciphertext-blob fileb://<(echo "$CT" | base64 -d) \
  --query Plaintext --output text | base64 -d
```

**Expected result:** `secret` — the value survives an encrypt/decrypt round
trip under a customer-managed key.

**Negative test:** decrypt the ciphertext after
`aws kms disable-key --key-id "$KID"`; it fails `DisabledException`,
proving the key controls access to the data.

**Cleanup:** `aws kms schedule-key-deletion --key-id "$KID" --pending-window-in-days 7`.

### Lab 11.6 — Manage sensitive data in application code

**Objective:** Store a credential in Secrets Manager instead of in code.

```bash
aws secretsmanager create-secret --name dva/db --secret-string '{"user":"app","pass":"s3cr3t"}' >/dev/null
aws secretsmanager get-secret-value --secret-id dva/db \
  --query 'SecretString' --output text
```

**Expected result:** the JSON secret is returned at runtime — the app reads
it by name, never embedding the value.

**Negative test:** an IAM principal without `secretsmanager:GetSecretValue`
gets `AccessDeniedException`, showing the secret is access-controlled, not
merely hidden.

**Cleanup:** `aws secretsmanager delete-secret --secret-id dva/db --force-delete-without-recovery`.

### Lab 11.7 — Prepare application artifacts to be deployed to AWS

**Objective:** Publish a versioned deployment artifact to S3.

```bash
aws s3api put-object --bucket "$BUCKET" --key artifacts/dva-fn-1.0.0.zip \
  --body /tmp/l.zip --metadata sha=$(shasum -a256 /tmp/l.zip | cut -d' ' -f1)
aws s3api head-object --bucket "$BUCKET" --key artifacts/dva-fn-1.0.0.zip \
  --query 'Metadata.sha' --output text
```

**Expected result:** the object's stored SHA metadata — an immutable,
traceable artifact ready for a deploy stage.

**Negative test:** overwrite the same key with different bytes; without
bucket versioning the original is lost, the case for enabling versioning on
an artifact bucket.

**Cleanup:** `aws s3api delete-object --bucket "$BUCKET" --key artifacts/dva-fn-1.0.0.zip`.

### Lab 11.8 — Test applications in development environments

**Objective:** Validate a function in a dev alias before promoting it.

```bash
aws lambda publish-version --function-name dva-fn --query Version --output text
aws lambda create-alias --function-name dva-fn --name dev --function-version 1 >/dev/null
aws lambda invoke --function-name dva-fn:dev --payload '{"env":"dev"}' \
  --cli-binary-format raw-in-base64-out /tmp/dev.json && cat /tmp/dev.json
```

**Expected result:** the `dev` alias resolves to version 1 and returns the
echoed event — a tested version, isolated from production callers.

**Negative test:** invoke `dva-fn:prod` before that alias exists;
`ResourceNotFoundException` shows aliases are the promotion gate.

**Cleanup:** `aws lambda delete-alias --function-name dva-fn --name dev`.

### Lab 11.9 — Automate deployment testing

**Objective:** Define a CodeBuild project whose buildspec runs tests.

```bash
aws codebuild create-project --name dva-test \
  --source '{"type":"NO_SOURCE","buildspec":"version: 0.2\nphases:\n  build:\n    commands:\n      - echo running tests\n      - python -m pytest -q || true"}' \
  --artifacts '{"type":"NO_ARTIFACTS"}' \
  --environment '{"type":"LINUX_CONTAINER","image":"aws/codebuild/standard:7.0","computeType":"BUILD_GENERAL1_SMALL"}' \
  --service-role "$ROLE_ARN" --query 'project.name' --output text
```

**Expected result:** a project `dva-test` whose build phase runs the test
command — automated testing as a pipeline stage.

**Negative test:** start a build with a buildspec whose test command exits
non-zero (remove `|| true`); the build reports `FAILED`, gating the deploy.

**Cleanup:** `aws codebuild delete-project --name dva-test`.

### Lab 11.10 — Deploy code by using AWS CI/CD services

**Objective:** Create a CodeDeploy application and deployment group for
Lambda traffic shifting.

```bash
aws deploy create-application --application-name dva-cd \
  --compute-platform Lambda --query applicationId --output text
aws deploy create-deployment-group --application-name dva-cd \
  --deployment-group-name dva-dg --service-role-arn "$ROLE_ARN" \
  --deployment-config-name CodeDeployDefault.LambdaCanary10Percent5Minutes \
  --query deploymentGroupId --output text
```

**Expected result:** an application and a deployment group configured for a
10%-canary Lambda rollout — CI/CD with a controlled blast radius.

**Negative test:** reference a nonexistent deployment config; the call fails
`InvalidDeploymentConfigNameException`, showing the shift strategy must be
valid.

**Cleanup:** `aws deploy delete-application --application-name dva-cd`.

### Lab 11.11 — Assist in a root cause analysis

**Objective:** Query logs with CloudWatch Logs Insights to find errors
fast.

```bash
QID=$(aws logs start-query --log-group-name /aws/lambda/dva-fn \
  --start-time $(($(date +%s)-3600)) --end-time $(date +%s) \
  --query-string 'fields @timestamp,@message | filter @message like /ERROR/ | limit 20' \
  --query queryId --output text)
sleep 3; aws logs get-query-results --query-id "$QID" --query 'status'
```

**Expected result:** a query `Status` of `Complete` with any matching
`ERROR` lines — structured root-cause evidence, not a manual log scroll.

**Negative test:** query a log group that does not exist;
`ResourceNotFoundException` shows the function must have logged at least
once first.

**Cleanup:** none (read-only query).

### Lab 11.12 — Instrument code for observability

**Objective:** Turn on AWS X-Ray active tracing for the function.

```bash
aws lambda update-function-configuration --function-name dva-fn \
  --tracing-config Mode=Active >/dev/null
aws lambda get-function-configuration --function-name dva-fn \
  --query 'TracingConfig.Mode' --output text
```

**Expected result:** `Active` — invocations now emit X-Ray segments,
turning latency and downstream calls into a service map.

**Negative test:** query the X-Ray trace summaries with tracing set to
`PassThrough` and no upstream trace header; no traces appear, showing active
tracing is what produces them.

**Cleanup:** reset with `--tracing-config Mode=PassThrough`.

### Lab 11.13 — Optimize applications by using AWS services and features

**Objective:** Add provisioned concurrency to remove Lambda cold starts on
a latency-sensitive path.

```bash
aws lambda put-provisioned-concurrency-config --function-name dva-fn \
  --qualifier 1 --provisioned-concurrent-executions 2 \
  --query 'Status' --output text
```

**Expected result:** a status of `IN_PROGRESS` then `READY` — two warm
environments eliminate cold-start latency. **Cost:** provisioned
concurrency bills while allocated; delete promptly.

**Negative test:** set provisioned concurrency on `$LATEST` rather than a
published version; it fails, showing the optimization requires an immutable
version.

**Cleanup:** `aws lambda delete-provisioned-concurrency-config --function-name dva-fn --qualifier 1`.

**CloudOps Engineer – Associate (SOA-C03) — Labs 11.14–11.26**

### Lab 11.14 — Implement metrics, alarms, and filters

**Objective:** Turn a log pattern into a metric and alarm on it.

```bash
aws logs put-metric-filter --log-group-name /aws/lambda/dva-fn \
  --filter-name errors --filter-pattern 'ERROR' \
  --metric-transformations metricName=AppErrors,metricNamespace=SOA,metricValue=1
aws cloudwatch put-metric-alarm --alarm-name soa-errors \
  --namespace SOA --metric-name AppErrors --statistic Sum --period 300 \
  --evaluation-periods 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold
aws cloudwatch describe-alarms --alarm-names soa-errors --query 'MetricAlarms[0].StateValue' --output text
```

**Expected result:** the alarm exists in `INSUFFICIENT_DATA` until the
metric reports — a log-derived operational signal.

**Negative test:** a metric filter whose pattern never matches keeps the
metric at zero and the alarm silent, the untested-alarm trap.

**Cleanup:** delete the alarm and the metric filter.

### Lab 11.15 — Identify and remediate issues by using metrics

**Objective:** Wire an alarm to an SSM Automation remediation.

```bash
aws ssm start-automation-execution --document-name AWS-RestartEC2Instance \
  --parameters InstanceId=$INSTANCE_ID --query AutomationExecutionId --output text
aws ssm describe-automation-executions \
  --filters Key=DocumentNamePrefix,Values=AWS-RestartEC2Instance \
  --query 'AutomationExecutionMetadataList[0].AutomationExecutionStatus' --output text
```

**Expected result:** an execution ID and a status progressing to `Success`
— an operational issue remediated by automation rather than by hand.

**Negative test:** run the document against a stopped instance; it fails and
records why, showing remediation must match resource state.

**Cleanup:** none (the automation completes and self-terminates).

### Lab 11.16 — Implement performance optimization for compute, storage, database

**Objective:** Modify an EBS volume from gp2 to gp3 for better price and
baseline performance without downtime.

```bash
aws ec2 modify-volume --volume-id "$VOL" --volume-type gp3 --iops 3000 --throughput 125 \
  --query 'VolumeModification.ModificationState' --output text
aws ec2 describe-volumes-modifications --volume-ids "$VOL" \
  --query 'VolumesModifications[0].TargetVolumeType' --output text
```

**Expected result:** modification state `modifying` then `completed`, target
type `gp3` — a live storage optimization.

**Negative test:** request 20000 IOPS on a small gp3 volume; it fails the
size-to-IOPS ratio check, a real performance constraint.

**Cleanup:** none (the volume remains in use; gp3 is the desired end state).

### Lab 11.17 — Implement scalability and elasticity

**Objective:** Create an Auto Scaling group that maintains capacity.

```bash
aws autoscaling create-auto-scaling-group --auto-scaling-group-name soa-asg \
  --launch-template LaunchTemplateId=$LT --min-size 2 --max-size 6 --desired-capacity 2 \
  --vpc-zone-identifier "$SUBNET_A,$SUBNET_B"
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names soa-asg \
  --query 'AutoScalingGroups[0].{Desired:DesiredCapacity,AZs:length(AvailabilityZones)}'
```

**Expected result:** desired capacity 2 across two AZs — the group replaces
failed instances and scales on policy.

**Negative test:** set `--desired-capacity 10` above `--max-size 6`; the
request is rejected, showing max-size is a hard ceiling.

**Cleanup:** `aws autoscaling delete-auto-scaling-group --auto-scaling-group-name soa-asg --force-delete`.

### Lab 11.18 — Implement highly available and resilient environments

**Objective:** Attach ELB health checks so the ASG replaces unhealthy
targets.

```bash
aws autoscaling attach-load-balancer-target-groups \
  --auto-scaling-group-name soa-asg --target-group-arns "$TG"
aws autoscaling update-auto-scaling-group --auto-scaling-group-name soa-asg \
  --health-check-type ELB --health-check-grace-period 120
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names soa-asg \
  --query 'AutoScalingGroups[0].HealthCheckType' --output text
```

**Expected result:** `HealthCheckType: ELB` — instances failing the ALB
health check are terminated and replaced, closing the resilience loop.

**Negative test:** leave health-check type at `EC2`; an app that hangs but
keeps the instance "running" is never replaced — the failure ELB checks
catch.

**Cleanup:** detach the target group.

### Lab 11.19 — Implement backup and restore strategies

**Objective:** Create an AWS Backup plan and confirm the rule.

```bash
aws backup create-backup-plan --backup-plan '{"BackupPlanName":"soa-daily","Rules":[{"RuleName":"daily","TargetBackupVaultName":"Default","ScheduleExpression":"cron(0 5 * * ? *)","Lifecycle":{"DeleteAfterDays":35}}]}' \
  --query 'BackupPlanId' --output text
```

**Expected result:** a backup-plan ID with a daily rule and 35-day
retention — centralized, policy-driven backups.

**Negative test:** a plan with `DeleteAfterDays` less than
`MoveToColdStorageAfterDays` is rejected, enforcing a sane lifecycle.

**Cleanup:** `aws backup delete-backup-plan --backup-plan-id <id>`.

### Lab 11.20 — Provision and maintain cloud resources

**Objective:** Patch-scan managed instances with Systems Manager.

```bash
aws ssm send-command --document-name AWS-RunPatchBaseline \
  --targets Key=tag:Env,Values=lab --parameters Operation=Scan \
  --query 'Command.CommandId' --output text
```

**Expected result:** a command ID; `aws ssm list-command-invocations`
shows per-instance `Success` with missing-patch counts — fleet maintenance
at scale.

**Negative test:** target a tag no instance carries; the command has zero
targets and does nothing, showing tag hygiene gates operations.

**Cleanup:** none (scan is read-only; no patches installed).

### Lab 11.21 — Automate the management of existing resources

**Objective:** Schedule recurring maintenance with an SSM maintenance
window.

```bash
WIN=$(aws ssm create-maintenance-window --name soa-win \
  --schedule "cron(0 3 ? * SUN *)" --duration 2 --cutoff 1 --no-allow-unassociated-targets \
  --query WindowId --output text)
aws ssm describe-maintenance-windows --query "WindowIdentities[?WindowId=='$WIN'].Enabled" --output text
```

**Expected result:** an enabled weekly window — a recurring automation
container for patching and tasks.

**Negative test:** set `--duration 1 --cutoff 2` (cutoff exceeds duration);
the request is rejected, enforcing a coherent schedule.

**Cleanup:** `aws ssm delete-maintenance-window --window-id "$WIN"`.

### Lab 11.22 — Implement and manage security and compliance tools and policies

**Objective:** Add an AWS Config managed rule to detect noncompliant
resources.

```bash
aws configservice put-config-rule --config-rule '{"ConfigRuleName":"s3-ssl-only","Source":{"Owner":"AWS","SourceIdentifier":"S3_BUCKET_SSL_REQUESTS_ONLY"}}'
aws configservice describe-compliance-by-config-rule --config-rule-names s3-ssl-only \
  --query 'ComplianceByConfigRules[0].Compliance.ComplianceType' --output text
```

**Expected result:** the rule evaluates buckets and reports
`COMPLIANT`/`NON_COMPLIANT` — continuous compliance as code.

**Negative test:** add the rule with Config's recorder off; it never
evaluates (`INSUFFICIENT_DATA`), the dependency from Lab 10.6.

**Cleanup:** `aws configservice delete-config-rule --config-rule-name s3-ssl-only`.

### Lab 11.23 — Implement strategies to protect data and infrastructure

**Objective:** Enforce default encryption on the account's EBS volumes.

```bash
aws ec2 enable-ebs-encryption-by-default --query 'EbsEncryptionByDefault' --output text
aws ec2 get-ebs-encryption-by-default --query 'EbsEncryptionByDefault' --output text
```

**Expected result:** `True` — every new volume in the Region is encrypted
at rest without relying on per-request flags.

**Negative test:** launch a volume before enabling the default and inspect
`Encrypted`; it is `false`, the gap default-encryption closes.

**Cleanup:** leave enabled (secure default), or
`aws ec2 disable-ebs-encryption-by-default` to restore prior state.

### Lab 11.24 — Implement and optimize networking features and connectivity

**Objective:** Add an interface VPC endpoint so private subnets reach an AWS
API without a NAT gateway.

```bash
aws ec2 create-vpc-endpoint --vpc-id "$VPC" --vpc-endpoint-type Interface \
  --service-name "com.amazonaws.$(aws configure get region).ssm" \
  --subnet-ids "$SUBNET_A" --security-group-ids "$SG" \
  --query 'VpcEndpoint.State'
```

**Expected result:** the SSM interface endpoint reaches `available` —
private connectivity to the API, cheaper and more secure than NAT egress.

**Negative test:** call SSM from the private subnet with the endpoint
deleted and no NAT; the request times out, proving the endpoint carried it.

**Cleanup:** `aws ec2 delete-vpc-endpoints --vpc-endpoint-ids <id>`.

### Lab 11.25 — Configure domains, DNS services, and content delivery

**Objective:** Create an alias record pointing a hosted-zone name at a
CloudFront/ELB target.

```bash
aws route53 change-resource-record-sets --hosted-zone-id "$ZONE" \
  --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"app.example.com","Type":"A","AliasTarget":{"HostedZoneId":"'"$ALB_ZONE"'","DNSName":"'"$ALB_DNS"'","EvaluateTargetHealth":true}}}]}' \
  --query 'ChangeInfo.Status' --output text
```

**Expected result:** `PENDING` then `INSYNC` — an alias record that health-
checks its target, the standard front-door DNS pattern.

**Negative test:** UPSERT an alias whose `HostedZoneId` does not match the
target service; the change is rejected, showing alias targets are typed.

**Cleanup:** repeat the call with `"Action":"DELETE"`.

### Lab 11.26 — Troubleshoot network connectivity issues

**Objective:** Use Reachability Analyzer to prove why a path fails.

```bash
PID=$(aws ec2 create-network-insights-path --source "$SG_SOURCE" \
  --destination "$ENI" --protocol tcp --destination-port 443 \
  --query 'NetworkInsightsPath.NetworkInsightsPathId' --output text)
AID=$(aws ec2 start-network-insights-analysis --network-insights-path-id "$PID" \
  --query 'NetworkInsightsAnalysis.NetworkInsightsAnalysisId' --output text)
aws ec2 describe-network-insights-analyses --network-insights-analysis-ids "$AID" \
  --query 'NetworkInsightsAnalyses[0].{Found:NetworkPathFound,Why:Explanations[0].ExplanationCode}'
```

**Expected result:** `Found: false` with an `ExplanationCode` naming the
blocking security group or route — a definitive troubleshooting verdict.

**Negative test:** open the required rule and re-run; `Found: true`,
confirming the analyzer, not guesswork, located the fault.

**Cleanup:** delete the analysis and path.

**Data Engineer – Associate (DEA-C01) — Labs 11.27–11.43**

### Lab 11.27 — Perform data ingestion

**Objective:** Create a Kinesis Data Firehose stream that lands records in
S3.

```bash
aws firehose create-delivery-stream --delivery-stream-name dea-ingest \
  --s3-destination-configuration RoleARN="$ROLE_ARN",BucketARN="arn:aws:s3:::$BUCKET" \
  --query 'DeliveryStreamARN' --output text
aws firehose describe-delivery-stream --delivery-stream-name dea-ingest \
  --query 'DeliveryStreamDescription.DeliveryStreamStatus' --output text
```

**Expected result:** the stream reaches `ACTIVE` — a managed ingestion path
that batches records to the lake. **Cost:** Firehose bills per GB ingested.

**Negative test:** `put-record` with a role lacking `s3:PutObject`; delivery
fails and the error surfaces in the stream's error logs, not at the API.

**Cleanup:** `aws firehose delete-delivery-stream --delivery-stream-name dea-ingest`.

### Lab 11.28 — Transform and process data

**Objective:** Register a Glue ETL job (the managed Spark transform).

```bash
aws glue create-job --name dea-etl --role "$ROLE_ARN" \
  --command '{"Name":"glueetl","ScriptLocation":"s3://'"$BUCKET"'/scripts/etl.py","PythonVersion":"3"}' \
  --glue-version 4.0 --query 'Name' --output text
```

**Expected result:** a job `dea-etl` bound to a PySpark script — a
repeatable transform stage. **Cost:** running the job bills DPU-hours; this
lab only registers it.

**Negative test:** start the job with a missing script location; the run
fails immediately with a script-not-found error.

**Cleanup:** `aws glue delete-job --job-name dea-etl`.

### Lab 11.29 — Orchestrate data pipelines

**Objective:** Define a Step Functions state machine that sequences pipeline
stages.

```bash
aws stepfunctions create-state-machine --name dea-pipeline --role-arn "$ROLE_ARN" \
  --definition '{"StartAt":"Ingest","States":{"Ingest":{"Type":"Pass","Next":"Transform"},"Transform":{"Type":"Pass","End":true}}}' \
  --query 'stateMachineArn' --output text
```

**Expected result:** a state-machine ARN — orchestration with explicit
ordering, retries, and error paths.

**Negative test:** submit a definition whose `Next` points at an undefined
state; creation fails validation, catching a broken DAG before runtime.

**Cleanup:** `aws stepfunctions delete-state-machine --state-machine-arn <arn>`.

### Lab 11.30 — Apply programming concepts

**Objective:** Version-control transform logic and store it as a reusable
artifact (idempotency, parameterization).

```bash
aws s3api put-object --bucket "$BUCKET" --key scripts/etl.py \
  --body /tmp/etl.py
aws s3api put-bucket-versioning --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled
aws s3api list-object-versions --bucket "$BUCKET" --prefix scripts/etl.py \
  --query 'length(Versions)' --output text
```

**Expected result:** at least one script version tracked — code managed
with the same rigor (versioning, rollback) as application code.

**Negative test:** overwrite with versioning disabled; only one version
exists and the prior logic is unrecoverable.

**Cleanup:** delete the object versions and the script.

### Lab 11.31 — Choose a data store

**Objective:** Provision a purpose-fit store (DynamoDB for key-value access
patterns) and confirm its billing mode.

```bash
aws dynamodb create-table --table-name dea-events \
  --attribute-definitions AttributeName=pk,AttributeType=S \
  --key-schema AttributeName=pk,KeyType=HASH --billing-mode PAY_PER_REQUEST \
  --query 'TableDescription.BillingModeSummary.BillingMode' --output text
```

**Expected result:** `PAY_PER_REQUEST` — a serverless store chosen for
spiky, key-based access rather than defaulting to a relational engine.

**Negative test:** run an unindexed `scan` with a filter on a large table; it
reads every item, the anti-pattern that signals the wrong store or missing
index.

**Cleanup:** `aws dynamodb delete-table --table-name dea-events`.

### Lab 11.32 — Understand data cataloging systems

**Objective:** Create a Glue Data Catalog database and a crawler to populate
it.

```bash
aws glue create-database --database-input '{"Name":"dea_catalog"}'
aws glue create-crawler --name dea-crawler --role "$ROLE_ARN" \
  --database-name dea_catalog \
  --targets '{"S3Targets":[{"Path":"s3://'"$BUCKET"'/data/"}]}'
aws glue get-crawler --name dea-crawler --query 'Crawler.State' --output text
```

**Expected result:** a catalog database and a `READY` crawler — schema
inferred and registered so query engines can find the data.

**Negative test:** run Athena against uncatalogued S3 data; queries fail
without a table definition, showing the catalog is the schema source.

**Cleanup:** delete the crawler and database.

### Lab 11.33 — Manage the lifecycle of data

**Objective:** Apply an S3 lifecycle policy that tiers and expires objects.

```bash
aws s3api put-bucket-lifecycle-configuration --bucket "$BUCKET" \
  --lifecycle-configuration '{"Rules":[{"ID":"tier","Status":"Enabled","Filter":{"Prefix":"data/"},"Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"},{"Days":90,"StorageClass":"GLACIER"}],"Expiration":{"Days":365}}]}'
aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET" \
  --query 'Rules[0].Transitions[].StorageClass' --output text
```

**Expected result:** `STANDARD_IA GLACIER` — data tiers down by age and
expires at a year, controlling storage cost automatically.

**Negative test:** a rule transitioning to `STANDARD_IA` before 30 days is
rejected, enforcing the class's minimum-age rule.

**Cleanup:** `aws s3api delete-bucket-lifecycle --bucket "$BUCKET"`.

### Lab 11.34 — Design data models and schema evolution

**Objective:** Register a schema and evolve it under a compatibility rule.

```bash
aws glue create-registry --registry-name dea-reg --query 'RegistryArn' --output text
aws glue create-schema --registry-id RegistryName=dea-reg --schema-name events \
  --data-format JSON --compatibility BACKWARD \
  --schema-definition '{"type":"record","name":"e","fields":[{"name":"id","type":"string"}]}' \
  --query 'SchemaName' --output text
```

**Expected result:** a schema with `BACKWARD` compatibility — new versions
must not break existing readers.

**Negative test:** register a new version that removes the `id` field; the
registry rejects it as incompatible, preventing a breaking change.

**Cleanup:** delete the schema and registry.

### Lab 11.35 — Automate data processing by using AWS services

**Objective:** Trigger a Glue job on a schedule with EventBridge Scheduler.

```bash
aws scheduler create-schedule --name dea-nightly \
  --schedule-expression "cron(0 2 * * ? *)" \
  --flexible-time-window '{"Mode":"OFF"}' \
  --target '{"Arn":"arn:aws:scheduler:::aws-sdk:glue:startJobRun","RoleArn":"'"$ROLE_ARN"'","Input":"{\"JobName\":\"dea-etl\"}"}' \
  --query 'ScheduleArn' --output text
```

**Expected result:** a schedule ARN that starts the ETL job nightly —
hands-off pipeline execution.

**Negative test:** a schedule whose role cannot `glue:StartJobRun` runs but
the target invocation fails; the error lands in the schedule's dead-letter
queue, not silently.

**Cleanup:** `aws scheduler delete-schedule --name dea-nightly`.

### Lab 11.36 — Analyze data by using AWS services

**Objective:** Run an Athena query over catalogued S3 data.

```bash
QE=$(aws athena start-query-execution \
  --query-string "SELECT count(*) FROM dea_catalog.data" \
  --result-configuration OutputLocation=s3://$BUCKET/athena/ \
  --query QueryExecutionId --output text)
sleep 4; aws athena get-query-execution --query-execution-id "$QE" \
  --query 'QueryExecution.Status.State' --output text
```

**Expected result:** `SUCCEEDED` with a row count in the results — SQL over
the lake without moving data. **Cost:** Athena bills per TB scanned.

**Negative test:** query a column not in the catalogued schema; the state is
`FAILED` with a column-not-found error.

**Cleanup:** delete the Athena result objects under `athena/`.

### Lab 11.37 — Maintain and monitor data pipelines

**Objective:** Read Glue job-run metrics to confirm health, not just
success.

```bash
aws glue get-job-runs --job-name dea-etl \
  --query 'JobRuns[0].{State:JobRunState,DPU:MaxCapacity,Secs:ExecutionTime}'
```

**Expected result:** the latest run's state, capacity, and duration — the
data to spot a job that "succeeds" but is slowing or over-provisioned.

**Negative test:** rely on `JobRunState=SUCCEEDED` alone while
`ExecutionTime` climbs each run; the trend reveals a degrading pipeline a
binary status hides.

**Cleanup:** none (read-only).

### Lab 11.38 — Ensure data quality

**Objective:** Attach a Glue Data Quality ruleset that fails on bad data.

```bash
aws glue create-data-quality-ruleset --name dea-dq \
  --ruleset 'Rules = [ColumnCount > 3, IsComplete "id", Uniqueness "id" > 0.95]' \
  --query 'Name' --output text
```

**Expected result:** a ruleset asserting completeness and uniqueness — data
quality enforced as code, not assumed.

**Negative test:** run it against data with duplicate `id` values; the
ruleset returns `FAIL` with the failing rule named, blocking bad data
downstream.

**Cleanup:** `aws glue delete-data-quality-ruleset --name dea-dq`.

### Lab 11.39 — Apply authentication mechanisms

**Objective:** Confirm the pipeline's execution identity via its assumed
role.

```bash
aws sts get-caller-identity --query 'Arn' --output text
aws iam get-role --role-name "$(basename $ROLE_ARN)" \
  --query 'Role.AssumeRolePolicyDocument.Statement[0].Principal.Service' --output text
```

**Expected result:** the caller ARN and the service principal (e.g.
`glue.amazonaws.com`) allowed to assume the role — authentication by role,
not long-lived keys.

**Negative test:** a trust policy naming the wrong service principal blocks
the assume-role, so the job cannot authenticate at all.

**Cleanup:** none (read-only).

### Lab 11.40 — Apply authorization mechanisms

**Objective:** Grant table-level access with Lake Formation instead of raw
S3 policies.

```bash
aws lakeformation grant-permissions \
  --principal DataLakePrincipalIdentifier="$ROLE_ARN" \
  --resource '{"Table":{"DatabaseName":"dea_catalog","Name":"data"}}' \
  --permissions SELECT
aws lakeformation list-permissions \
  --principal DataLakePrincipalIdentifier="$ROLE_ARN" \
  --query 'PrincipalResourcePermissions[0].Permissions' --output text
```

**Expected result:** `SELECT` granted on the specific table — fine-grained
authorization the coarse S3 bucket policy cannot express.

**Negative test:** query the table as a principal without the grant;
`AccessDenied` from Lake Formation, proving authorization is enforced at the
catalog.

**Cleanup:** `aws lakeformation revoke-permissions` with the same arguments.

### Lab 11.41 — Ensure data encryption and masking

**Objective:** Enforce SSE-KMS on the lake bucket so every object is
encrypted at rest.

```bash
aws s3api put-bucket-encryption --bucket "$BUCKET" \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"'"$KID"'"},"BucketKeyEnabled":true}]}'
aws s3api get-bucket-encryption --bucket "$BUCKET" \
  --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output text
```

**Expected result:** `aws:kms` — objects are encrypted with a customer-
managed key, and `BucketKeyEnabled` cuts KMS request cost.

**Negative test:** a principal without `kms:Decrypt` on the key cannot read
objects even with `s3:GetObject`, showing encryption adds an authorization
layer.

**Cleanup:** `aws s3api delete-bucket-encryption --bucket "$BUCKET"`.

### Lab 11.42 — Prepare logs for audit

**Objective:** Turn on S3 data-event logging in CloudTrail so object access
is auditable.

```bash
aws cloudtrail put-event-selectors --trail-name "$TRAIL" \
  --event-selectors '[{"ReadWriteType":"All","IncludeManagementEvents":false,"DataResources":[{"Type":"AWS::S3::Object","Values":["arn:aws:s3:::'"$BUCKET"'/"]}]}]' \
  --query 'EventSelectors[0].DataResources[0].Type' --output text
```

**Expected result:** `AWS::S3::Object` — every read and write to the lake is
now recorded for audit.

**Negative test:** with management events only, object-level reads are
invisible in CloudTrail — the gap data-event logging closes.

**Cleanup:** reset event selectors to management-only.

### Lab 11.43 — Understand data privacy and governance

**Objective:** Tag data with Lake Formation LF-Tags to govern by
classification.

```bash
aws lakeformation create-lf-tag --tag-key confidentiality --tag-values public restricted
aws lakeformation add-lf-tags-to-resource \
  --resource '{"Table":{"DatabaseName":"dea_catalog","Name":"data"}}' \
  --lf-tags TagKey=confidentiality,TagValues=restricted
aws lakeformation get-resource-lf-tags \
  --resource '{"Table":{"DatabaseName":"dea_catalog","Name":"data"}}' \
  --query 'LFTagOnDatabase' --output text 2>&1 | head -1
```

**Expected result:** the table tagged `confidentiality=restricted` —
governance by attribute, so access policies follow the classification, not
the path.

**Negative test:** grant by LF-Tag to a principal, then re-tag the resource;
the principal's effective access changes automatically, showing tag-based
governance is dynamic.

**Cleanup:** remove the LF-Tag and delete it.

**Machine Learning Engineer – Associate (MLA-C01) — Labs 11.44–11.55**

### Lab 11.44 — Ingest and store data

**Objective:** Stage training data in S3 with a prefix layout SageMaker
expects.

```bash
aws s3api put-object --bucket "$BUCKET" --key ml/train/data.csv --body /tmp/data.csv
aws s3api list-objects-v2 --bucket "$BUCKET" --prefix ml/train/ \
  --query 'Contents[].Key' --output text
```

**Expected result:** the training object listed under `ml/train/` — the
channel layout training jobs read from.

**Negative test:** point a training job at an empty prefix; it fails with a
no-training-data error, showing the channel must resolve to objects.

**Cleanup:** delete the `ml/` prefix objects.

### Lab 11.45 — Transform data and perform feature engineering

**Objective:** Launch a SageMaker Processing job for feature engineering.

```bash
aws sagemaker create-processing-job --processing-job-name mla-fe \
  --role-arn "$ROLE_ARN" \
  --app-specification ImageUri=$PROCESS_IMAGE \
  --processing-resources '{"ClusterConfig":{"InstanceCount":1,"InstanceType":"ml.t3.medium","VolumeSizeInGB":5}}' \
  --processing-inputs '[{"InputName":"raw","S3Input":{"S3Uri":"s3://'"$BUCKET"'/ml/train/","LocalPath":"/opt/ml/processing/input","S3DataType":"S3Prefix"}}]' \
  --query 'ProcessingJobArn' --output text
```

**Expected result:** a processing-job ARN; `describe-processing-job` shows
`InProgress` then `Completed` — reproducible feature engineering. **Cost:**
bills instance-time; use `ml.t3.medium` and clean up.

**Negative test:** reference a container image URI in the wrong Region; the
job fails to pull the image, showing image and job must share a Region.

**Cleanup:** the job self-terminates; delete any output under `ml/`.

### Lab 11.46 — Ensure data integrity and prepare data for modeling

**Objective:** Create a SageMaker Feature Group so features are consistent
across training and inference.

```bash
aws sagemaker create-feature-group --feature-group-name mla-features \
  --record-identifier-feature-name id --event-time-feature-name ts \
  --feature-definitions '[{"FeatureName":"id","FeatureType":"String"},{"FeatureName":"ts","FeatureType":"String"},{"FeatureName":"x1","FeatureType":"Fractional"}]' \
  --online-store-config '{"EnableOnlineStore":true}' --role-arn "$ROLE_ARN" \
  --query 'FeatureGroupArn' --output text
```

**Expected result:** a feature-group ARN reaching `Created` — one source of
truth for features, eliminating train/serve skew.

**Negative test:** ingest a record missing the `id` identifier; it is
rejected, enforcing record integrity.

**Cleanup:** `aws sagemaker delete-feature-group --feature-group-name mla-features`.

### Lab 11.47 — Choose a modeling approach

**Objective:** List SageMaker's built-in algorithm images to match an
approach to the problem.

```bash
python3 -c "import sagemaker; from sagemaker import image_uris; \
print(image_uris.retrieve('xgboost', '$(aws configure get region)', '1.7-1'))"
```

**Expected result:** a resolved XGBoost container URI — a built-in
gradient-boosting approach chosen for tabular data over a hand-built model.

**Negative test:** request an algorithm/version pair that does not exist;
`retrieve` raises a `ValueError`, showing approach selection is constrained
to supported images.

**Cleanup:** none (read-only lookup).

### Lab 11.48 — Train and refine models

**Objective:** Submit a managed training job.

```bash
aws sagemaker create-training-job --training-job-name mla-train \
  --algorithm-specification TrainingImage=$XGB_IMAGE,TrainingInputMode=File \
  --role-arn "$ROLE_ARN" \
  --input-data-config '[{"ChannelName":"train","DataSource":{"S3DataSource":{"S3DataType":"S3Prefix","S3Uri":"s3://'"$BUCKET"'/ml/train/","S3DataDistributionType":"FullyReplicated"}}}]' \
  --output-data-config S3OutputPath=s3://$BUCKET/ml/model/ \
  --resource-config InstanceType=ml.m5.large,InstanceCount=1,VolumeSizeInGB=5 \
  --stopping-condition MaxRuntimeInSeconds=600 \
  --query 'TrainingJobArn' --output text
```

**Expected result:** a training-job ARN; status moves to `Completed` and a
model artifact lands under `ml/model/`. **Cost:** bills instance-time;
`MaxRuntimeInSeconds` caps it.

**Negative test:** omit the `train` channel the algorithm requires; the job
fails validation before consuming compute.

**Cleanup:** delete the model artifact; the job record is retained.

### Lab 11.49 — Analyze model performance

**Objective:** Register the trained model and inspect its metrics in the
Model Registry.

```bash
aws sagemaker create-model-package --model-package-group-name mla-mpg \
  --inference-specification '{"Containers":[{"Image":"'"$XGB_IMAGE"'","ModelDataUrl":"s3://'"$BUCKET"'/ml/model/model.tar.gz"}],"SupportedContentTypes":["text/csv"],"SupportedResponseMIMETypes":["text/csv"]}' \
  --model-approval-status PendingManualApproval \
  --query 'ModelPackageArn' --output text
```

**Expected result:** a versioned model package pending approval — a
governed record of a model and its evaluation, not a loose artifact.

**Negative test:** approve and deploy a package whose metrics fall below a
threshold; a gated pipeline should block it — the reason metrics live with
the package.

**Cleanup:** `aws sagemaker delete-model-package --model-package-name <arn>`.

### Lab 11.50 — Select deployment infrastructure

**Objective:** Define an endpoint configuration sized to the workload.

```bash
aws sagemaker create-model --model-name mla-model --execution-role-arn "$ROLE_ARN" \
  --primary-container Image=$XGB_IMAGE,ModelDataUrl=s3://$BUCKET/ml/model/model.tar.gz >/dev/null
aws sagemaker create-endpoint-config --endpoint-config-name mla-ec \
  --production-variants '[{"VariantName":"v1","ModelName":"mla-model","InstanceType":"ml.t2.medium","InitialInstanceCount":1}]' \
  --query 'EndpointConfigArn' --output text
```

**Expected result:** an endpoint-config ARN selecting a real-time instance
variant — the deployment shape chosen from latency/throughput needs.

**Negative test:** reference a model name that does not exist; config
creation fails, showing the model must be registered first.

**Cleanup:** delete the endpoint config and model.

### Lab 11.51 — Create and script infrastructure

**Objective:** Capture the endpoint as CloudFormation so it is reproducible.

```bash
cat > /tmp/ep.yaml <<'YAML'
Resources:
  Ep:
    Type: AWS::SageMaker::Endpoint
    Properties: {EndpointConfigName: mla-ec}
YAML
aws cloudformation validate-template --template-body file:///tmp/ep.yaml \
  --query 'Description' --output text 2>&1 | head -1
```

**Expected result:** the template validates — ML infrastructure defined as
code, versioned and repeatable across environments.

**Negative test:** introduce a YAML indentation error; `validate-template`
returns a template-format error before any deploy.

**Cleanup:** `rm -f /tmp/ep.yaml`.

### Lab 11.52 — Use automated orchestration tools for CI/CD pipelines

**Objective:** Create a SageMaker Pipeline that chains process → train →
register.

```bash
aws sagemaker create-pipeline --pipeline-name mla-pipe --role-arn "$ROLE_ARN" \
  --pipeline-definition '{"Version":"2020-12-01","Steps":[{"Name":"Train","Type":"Training","Arguments":{}}]}' \
  --query 'PipelineArn' --output text 2>&1 | head -1
```

**Expected result:** a pipeline ARN — MLOps as a defined, re-runnable DAG
rather than manual steps.

**Negative test:** submit a definition missing the required `Version`; the
API rejects it, enforcing a valid pipeline schema.

**Cleanup:** `aws sagemaker delete-pipeline --pipeline-name mla-pipe`.

### Lab 11.53 — Monitor model inference

**Objective:** Enable data capture so inference inputs/outputs can be
monitored for drift.

```bash
aws sagemaker create-endpoint-config --endpoint-config-name mla-ec-mon \
  --production-variants '[{"VariantName":"v1","ModelName":"mla-model","InstanceType":"ml.t2.medium","InitialInstanceCount":1}]' \
  --data-capture-config '{"EnableCapture":true,"InitialSamplingPercentage":100,"DestinationS3Uri":"s3://'"$BUCKET"'/ml/capture/","CaptureOptions":[{"CaptureMode":"Input"},{"CaptureMode":"Output"}]}' \
  --query 'EndpointConfigArn' --output text
```

**Expected result:** an endpoint config capturing 100% of inputs and outputs
to S3 — the raw material Model Monitor uses to detect data/quality drift.

**Negative test:** monitor an endpoint with capture disabled; Model Monitor
has nothing to analyze, so drift goes undetected.

**Cleanup:** `aws sagemaker delete-endpoint-config --endpoint-config-name mla-ec-mon`.

### Lab 11.54 — Monitor and optimize infrastructure and costs

**Objective:** Register an auto-scaling policy for an inference endpoint so
capacity tracks load.

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace sagemaker --resource-id endpoint/mla-ep/variant/v1 \
  --scalable-dimension sagemaker:variant:DesiredInstanceCount \
  --min-capacity 1 --max-capacity 4
aws application-autoscaling describe-scalable-targets \
  --service-namespace sagemaker \
  --query 'ScalableTargets[0].{Min:MinCapacity,Max:MaxCapacity}'
```

**Expected result:** min 1 / max 4 — the endpoint scales in to save cost at
low load and out to hold latency at peak.

**Negative test:** a fixed single-instance endpoint drops requests under a
load spike, the cost/latency trade-off autoscaling resolves.

**Cleanup:** `aws application-autoscaling deregister-scalable-target` with
the same target.

### Lab 11.55 — Secure AWS resources

**Objective:** Confine a training job to a private VPC with no internet
route.

```bash
aws sagemaker create-training-job --training-job-name mla-secure \
  --algorithm-specification TrainingImage=$XGB_IMAGE,TrainingInputMode=File \
  --role-arn "$ROLE_ARN" --output-data-config S3OutputPath=s3://$BUCKET/ml/model/ \
  --resource-config InstanceType=ml.m5.large,InstanceCount=1,VolumeSizeInGB=5 \
  --stopping-condition MaxRuntimeInSeconds=600 \
  --vpc-config Subnets=$SUBNET_A,SecurityGroupIds=$SG \
  --enable-network-isolation \
  --input-data-config '[{"ChannelName":"train","DataSource":{"S3DataSource":{"S3DataType":"S3Prefix","S3Uri":"s3://'"$BUCKET"'/ml/train/","S3DataDistributionType":"FullyReplicated"}}}]' \
  --query 'TrainingJobArn' --output text
```

**Expected result:** a training job with `EnableNetworkIsolation=true` in a
private subnet — the container has no outbound internet path. **Cost:**
bills instance-time; capped by the stopping condition.

**Negative test:** the isolated job cannot `pip install` from PyPI; the
dependency failure proves isolation is real and forces vendored
dependencies.

**Cleanup:** the job self-terminates; delete `ml/model/` output.

### Lab 11.56 — Associate-tier readiness drill (integrative)

**Objective:** Prove readiness for one associate certification other than
Solutions Architect by completing its role-specific drill unaided, ending
in a verification that the thing actually works.

**Cost note:** Lambda, CloudWatch, and Athena usage in this lab is small
but not free. Step 6 cleans up; leaving the Glue/Athena artifacts running
is the main cost risk.

**Prerequisites**

- The sandbox account and budget alarm from Chapter 10.
- The relevant prior-chapter lab environment: Chapter 4 (Developer),
  Chapter 6/7 (CloudOps), or Chapter 5 (Data Engineer).
- No reference material open during the timed portion.

**Steps**

1. **Choose your target (5 minutes).** Pick the one associate certification
   your role most justifies, and confirm its current code from its AWS page.

   **Expected result:** one target with a primary-source-confirmed code.

2. **Run the matching drill (timed, target 30 minutes).** Execute the drill
   from the Implementation section for your chosen exam, unaided.

   **Expected result:** Developer — a deliberately introduced error
   diagnosed from logs/traces alone. CloudOps — an alarm driven into ALARM
   with the notification confirmed received. Data Engineer — a row count
   returned from the cataloged table.

3. **Negative test (target 15 minutes).** Break the thing you just proved:
   revoke a permission the Lambda needs, disable the alarm's actions, or
   corrupt a column type in the Glue catalog. Diagnose from symptoms alone.

   **Expected result:** the fault identified and corrected without
   reference material — this, not the happy path, is the exam-relevant
   skill.

4. **Rate honestly (10 minutes).** Fill your row in the study spine. Any
   step needing reference material is a named gap, not a general "review
   more."

   **Expected result:** a specific list of gaps tied to chapters.

5. **Check the transition (5 minutes).** If your target is ML Engineer,
   check the exam page for the MLA-C02 guide and decide which version your
   test date falls in.

   **Expected result:** a version decision recorded with its reason.

6. **Cleanup:** revert every deliberately introduced fault, delete Athena
   query results and any Glue/EMR artifacts, and confirm no compute is
   running. Verify the budget alarm shows no unexpected spend.

## Lab Verification

Complete this sign-off once the drill and its negative test have been
completed unaided and the sandbox is clean. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The associate tier holds five peer certifications at one depth, each built
around a role: Solutions Architect (SAA-C03, already covered by Chapters
1–9), Developer (DVA-C02), CloudOps Engineer (SOA-C03), Data Engineer
(DEA-C01), and Machine Learning Engineer (MLA-C01, with MLA-C02
registration opening 1 September 2026). CloudOps Engineer is the renamed
SysOps Administrator — same `SOA` prefix, so judge resources by code, not
title. Developer, CloudOps, and Data Engineer are largely a re-emphasis of
material this volume already teaches; ML Engineer requires substantial
outside study. Pick by role, take a second one while the platform knowledge
is fresh, and stop before the credential stops changing your work.

- [ ] Can name all five associate certifications, their codes, and roles.
- [ ] Knows CloudOps Engineer is the renamed SysOps Administrator and that
      `SOA-C03` is the currency test.
- [ ] Can decide MLA-C01 versus MLA-C02 from a planned test date.
- [ ] Can map each exam to this volume's chapters and name where the volume
      stops.
- [ ] Has completed one role drill and its negative test unaided.
- [ ] Has recorded specific, chapter-linked gaps rather than a general
      review plan.
- [ ] Completed the hands-on lab, including full cleanup and a cost check.
