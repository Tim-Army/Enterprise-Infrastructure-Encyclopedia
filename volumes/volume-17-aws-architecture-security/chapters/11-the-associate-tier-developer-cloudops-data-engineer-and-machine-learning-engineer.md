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
