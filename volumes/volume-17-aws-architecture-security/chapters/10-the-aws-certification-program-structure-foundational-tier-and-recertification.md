# Chapter 10: The AWS Certification Program — Structure, Foundational Tier, and Recertification

![The complete AWS certification program as four stacked levels. Foundational (90 minutes / 65 questions, no prior experience needed): Cloud Practitioner CLF-C02 and AI Practitioner AIF-C01. Associate (130 minutes / 65 questions): Solutions Architect SAA-C03, Developer DVA-C02, CloudOps Engineer SOA-C03 (renamed from SysOps Administrator), Data Engineer DEA-C01, and Machine Learning Engineer MLA-C01 with MLA-C02 registration opening 1 September 2026. Professional (180 minutes / 75 questions, 2+ years AWS experience): Solutions Architect Professional SAP-C02, DevOps Engineer Professional DOP-C02, and Generative AI Developer Professional AIP-C01. Specialty (170 minutes / 65 questions): Advanced Networking ANS-C01, retiring 25 August 2026, and Security SCS-C03. No level is a formal prerequisite for another.](../../../diagrams/volume-17-aws-architecture-security/chapter-10-aws-certification-program-map.svg)

*Figure 10-1. The whole program on one page: four levels, twelve exams. Levels describe assumed depth, not a required sequence.*

## Learning Objectives

- Describe the four levels of the AWS certification program — foundational,
  associate, professional, and specialty — and explain why none of them is
  a formal prerequisite for another.
- Identify all twelve current AWS certifications and their exam codes, and
  read what the `-C0x` version suffix signals about a blueprint's age.
- Explain what the two foundational certifications, Cloud Practitioner
  (CLF-C02) and AI Practitioner (AIF-C01), assess and who should — and
  should not — spend time on them.
- Describe the three-year validity period and the recertification paths
  that reset it, including how a higher-level certification affects lower
  ones.
- Locate the authoritative source for any exam's current code, format, and
  status, and recognize why third-party summaries of this program go stale
  unusually fast.

## Theory and Architecture

[Chapters 1 through 9](01-cloud-foundations-accounts-and-well-architected-design.md)
built an AWS architecture and security practice and mapped it to two
certifications — Solutions Architect – Associate (SAA-C03) and Security –
Specialty (SCS-C03). Those two are a small part of a twelve-exam program.
This chapter and the three that follow map the rest of it, so the volume's
technical content can be aimed at whichever certification a reader actually
needs.

As with every certification chapter in this encyclopedia, this is study and
review material organized against publicly published structure. It does not
reproduce exam questions, does not reveal scoring weightings, and is not a
substitute for AWS's own exam guides. Every code below was verified against
AWS's certification pages on 23 July 2026; confirm currency before
scheduling, because this program changes faster than most.

### Four levels, and what "level" actually means

AWS organizes certifications into four levels. The critical structural
fact — and the one most often gotten wrong — is that **no AWS
certification is a formal prerequisite for any other**. AWS removed the
old "associate before professional" requirement years ago. The levels
describe the depth of knowledge and the amount of hands-on experience each
exam assumes, not a gate you must pass through:

- **Foundational** — broad conceptual understanding, no prior experience
  required. 90 minutes, 65 questions.
- **Associate** — working technical competence in one role. Cloud or IT
  experience recommended. 130 minutes, 65 questions.
- **Professional** — advanced, organization-scale competence. AWS states
  roughly two or more years of hands-on AWS experience. 180 minutes,
  75 questions.
- **Specialty** — deep expertise in one technical domain. 170 minutes,
  65 questions.

You may sit a professional exam first. Whether you *should* is a different
question, addressed in [Chapter 12](12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md).

### The twelve current certifications

| Level | Certification | Exam code |
| --- | --- | --- |
| Foundational | Cloud Practitioner | CLF-C02 |
| Foundational | AI Practitioner | AIF-C01 |
| Associate | Solutions Architect – Associate | SAA-C03 |
| Associate | Developer – Associate | DVA-C02 |
| Associate | CloudOps Engineer – Associate | SOA-C03 |
| Associate | Data Engineer – Associate | DEA-C01 |
| Associate | Machine Learning Engineer – Associate | MLA-C01 |
| Professional | Solutions Architect – Professional | SAP-C02 |
| Professional | DevOps Engineer – Professional | DOP-C02 |
| Professional | Generative AI Developer – Professional | AIP-C01 |
| Specialty | Advanced Networking – Specialty | ANS-C01 |
| Specialty | Security – Specialty | SCS-C03 |

Three of these rows carry news that a reader working from older material
will not have:

- **CloudOps Engineer – Associate (SOA-C03)** is the certification
  previously called **SysOps Administrator – Associate**. The role name
  changed; the `SOA` code prefix did not.
- **Generative AI Developer – Professional (AIP-C01)** is a new
  professional certification covering production generative-AI solutions on
  services such as Amazon Bedrock. It did not exist in earlier program maps.
- **Advanced Networking – Specialty (ANS-C01) retires 25 August 2026** —
  covered in [Chapter 13](13-specialty-certifications-and-keeping-the-aws-certification-program-current.md).

Reading the code is useful: the three-letter prefix identifies the
certification and the **`-C0x` suffix is the blueprint version**. `SAA-C03`
is the third-generation Solutions Architect – Associate blueprint;
`DEA-C01` is a first-generation blueprint on a young certification. A
suffix bump means the blueprint was rebuilt, so study material written
against the previous suffix is stale in a way that matters.

### The foundational tier

Two certifications sit at the foundational level, and they serve different
purposes:

- **Cloud Practitioner (CLF-C02)** validates broad understanding of AWS
  services, the shared responsibility model, pricing and support models,
  and core security concepts — the ground
  [Chapter 1](01-cloud-foundations-accounts-and-well-architected-design.md)
  covers. It is aimed at people who work *around* the cloud (sales,
  finance, project management, leadership) as much as at engineers.
- **AI Practitioner (AIF-C01)** validates conceptual understanding of AI,
  machine learning, and generative AI on AWS — terminology, use cases,
  responsible-AI considerations, and the relevant service surface — without
  requiring the ability to build or train models.

Neither is required for anything else, and for a working engineer neither
is usually the right place to spend exam money. Their value is for people
who need credible fluency without a build role, and for teams that want a
shared vocabulary before a migration.

### Validity and recertification

Every AWS certification is valid for **three years**. AWS's recertification
model has one property worth planning around: **earning a
higher-level certification generally extends the validity of lower-level
ones you hold**. A reader holding Solutions Architect – Associate who then
passes Solutions Architect – Professional does not separately need to renew
the associate credential during that window. Confirm the current rules on
AWS's recertification page before relying on this for a specific pair —
the policy has been revised before, and it is the kind of detail that
quietly changes.

## Design Considerations

- **Do not treat the levels as a ladder you must climb.** Because nothing
  is a prerequisite, the right first exam is the one matching the work you
  do. An experienced AWS engineer should usually start at associate level
  or above and skip the foundational tier entirely.
- **Skip Cloud Practitioner if you can already pass an associate exam.**
  Its value is credible fluency for non-builders and shared vocabulary for
  teams. For someone already administering AWS, it consumes an exam fee and
  several weeks to certify knowledge their associate exam will test anyway.
- **AI Practitioner is a fluency credential, not an engineering one.** If
  the goal is to *build* generative-AI systems on AWS, the relevant target
  is Generative AI Developer – Professional (Chapter 12), not AIF-C01. If
  the goal is to converse credibly about AI strategy, AIF-C01 is well
  aimed.
- **Sequence recertification deliberately.** Because a higher certification
  extends lower ones, a reader planning both an associate and a
  professional exam should sit them close enough together that the
  professional pass carries the associate's clock forward, rather than
  renewing the associate separately.
- **Budget for reading speed, not just knowledge.** The format differences
  across levels (65 questions in 130 minutes at associate versus 75 in 180
  at professional) change the pacing more than the raw difficulty does;
  this is developed further in Chapter 12.
- **Ethical preparation boundary.** Prepare only from AWS's own exam
  guides, AWS Skill Builder, official training, and hands-on practice.
  Material claiming to reproduce live exam questions violates the AWS
  Certification agreement and is frequently wrong against the current
  blueprint — treat any such resource as disqualifying rather than helpful.

## Implementation and Automation

### A program-wide readiness tracker

```text
# Rate each certification 1-5 for current readiness. Below 3 means the
# volume chapters listed need lab time before the exam is worth booking.
# Only fill rows you actually intend to sit — most readers need two or
# three, not twelve.

Level        | Certification (code)             | Chapters      | Rating
-------------|----------------------------------|---------------|-------
Foundational | Cloud Practitioner (CLF-C02)     | 1             |
Foundational | AI Practitioner (AIF-C01)        | 1 (concepts)  |
Associate    | Solutions Architect (SAA-C03)    | 1-9           |
Associate    | Developer (DVA-C02)              | 4, 7          |
Associate    | CloudOps Engineer (SOA-C03)      | 6, 7          |
Associate    | Data Engineer (DEA-C01)          | 5             |
Associate    | ML Engineer (MLA-C01)            | 5 + SageMaker |
Professional | Solutions Architect (SAP-C02)    | 2, 3, 6, 7    |
Professional | DevOps Engineer (DOP-C02)        | 6, 7          |
Professional | Generative AI Developer (AIP-C01)| beyond volume |
Specialty    | Advanced Networking (ANS-C01)    | 3  [retiring] |
Specialty    | Security (SCS-C03)               | 8             |
```

### Confirming a certification's current code from the authoritative source

```bash
# AWS certification pages no longer print the exam code in body text, but
# the Skill Builder exam-prep link on each page embeds it. This is the
# most reliable way to confirm a code without trusting a third-party page.
curl -s https://aws.amazon.com/certification/certified-solutions-architect-associate/ \
  | grep -oE 'skillbuilder\.aws/[^"]*exam-prep[^"]*' | head -1
# -> .../category/exam-prep/solutions-architect-associate-SAA-C03
```

### Checking your own certification validity window

```bash
# Certifications are valid three years. Record the expiry for each
# credential you hold so recertification is planned, not discovered.
# (Values come from your AWS Certification Account; this is a local
# tracker, not an API call.)
cat > ~/aws-cert-expiry.txt <<'TRACKER'
certification,code,earned,expires,recert_plan
Solutions Architect - Associate,SAA-C03,,,
Security - Specialty,SCS-C03,,,
TRACKER
```

## Validation and Troubleshooting

- **Code check before study.** Before buying a course or book, confirm its
  target code matches the current one from the certification's own AWS
  page. A course built for `SAA-C02` or `SCS-C02` is a blueprint behind,
  and the gap is real content, not cosmetics.
- **Distinguish a language retirement from an exam retirement.** AWS
  publishes end-of-support notices for individual *language versions* of an
  exam alongside notices for the exam itself. The Cloud Practitioner page,
  for instance, carries a retirement notice that applies to its Indonesian
  language version, not to CLF-C02. Read which noun the notice attaches to
  before concluding a certification is closing.
- **Verify the level's format, not just its name.** If you have prepared
  for a 65-question associate exam and are sitting a 75-question
  professional one, the pacing plan is wrong even if the knowledge is
  right. Confirm duration and question count from the exam page.
- **Recertification assumptions age badly.** Before relying on a higher
  certification to carry a lower one's expiry, re-read AWS's current
  recertification policy; this is a rule that has changed and will likely
  change again.

## Security and Best Practices

- Register only through your AWS Certification Account and AWS's
  authorized testing partners; confirm identification and
  online-proctoring requirements from the official portal before exam day.
- Do not use, buy, or share unauthorized exam dumps. Beyond the
  certification-agreement violation, the fast `-C0x` turnover in this
  program makes circulating material unusually likely to be both illicit
  and wrong.
- Protect the AWS account you practice in with the same discipline
  [Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)
  teaches — a dedicated sandbox account under an organization, with a
  budget alarm — rather than practicing in an account that carries real
  workloads.
- Every hands-on exercise in this volume can incur charges. Keep the
  cost-control habits from
  [Chapter 7](07-observability-automation-performance-and-cost-governance.md)
  active during exam preparation, when the temptation to leave lab
  resources running between study sessions is highest.

## References and Knowledge Checks

**References**

- [AWS Certification](https://aws.amazon.com/certification/) — the
  authoritative list of current certifications, levels, and retirement
  notices; the source verified for this chapter on 23 July 2026.
- [AWS Certified Cloud Practitioner](https://aws.amazon.com/certification/certified-cloud-practitioner/)
  and [AWS Certified AI Practitioner](https://aws.amazon.com/certification/certified-ai-practitioner/) —
  the two foundational certifications, with current exam guides.
- [AWS Skill Builder](https://skillbuilder.aws/) — official digital
  training, including free exam-prep plans per certification.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — AWS Certifications and Course Access](../../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md) —
  every certification with its code, exam end date, and training access.
- See [Chapter 1](01-cloud-foundations-accounts-and-well-architected-design.md)
  for the shared responsibility model and Well-Architected content the
  foundational tier assesses.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any AWS exam item)*

1. Explain why "associate before professional" is a planning heuristic
   rather than a rule, and give a case where skipping the associate is
   defensible.
2. What does the `-C0x` suffix tell you, and why does it matter when
   choosing a study resource?
3. Which certification was previously named SysOps Administrator –
   Associate, and did its exam code prefix change?
4. Distinguish the audiences for Cloud Practitioner and AI Practitioner,
   and name one reader who should sit neither.
5. How does earning a professional certification affect the validity of an
   associate one you already hold, and where would you confirm that?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every task in the
two foundational exam guides** — AWS Certified Cloud Practitioner (CLF-C02,
four domains, nineteen tasks) and AWS Certified AI Practitioner (AIF-C01,
five domains, fourteen tasks) — each mapped in the volume README's coverage
tables. The foundational exams are conceptual, so each lab *demonstrates*
its concept with a real, mostly read-only command rather than building
infrastructure.

**Shared prerequisites for Labs 10.1–10.33**

- AWS CLI v2 authenticated to a sandbox account with read access, a default
  Region set, and (for the AIF labs) Amazon Bedrock model access enabled in
  a Bedrock-supported Region such as `us-east-1`.
- **Cost:** every lab here is free except the two that invoke a Bedrock
  model (Labs 10.24 and 10.27), which cost a fraction of a cent in tokens
  and are marked. No lab leaves a billable resource running.
- Every lab ends **`**Lab verified by:** *pending*`** until a human runs it.

### Lab 10.1 — Define the benefits of the AWS Cloud

**Objective:** Show the global reach and elasticity that underpin the
"benefits" answers by listing every Region on demand.

```bash
aws ec2 describe-regions --all-regions \
  --query 'length(Regions)' --output text
```

**Expected result:** a count in the low-to-mid thirties — the on-demand
global footprint no single data center can match.

**Negative test:** `aws ec2 describe-regions --region-names no-such-1`
returns `InvalidParameterValue`, proving the list is authoritative, not
free text.

**Cleanup:** none (read-only).

### Lab 10.2 — Identify design principles of the AWS Cloud

**Objective:** Read the Well-Architected Framework's own pillars from the
service that encodes them.

```bash
aws wellarchitected list-lenses \
  --query "LensSummaries[?LensAlias=='wellarchitected'].LensName" --output text
```

**Expected result:** the AWS Well-Architected Framework lens is listed —
the canonical source of the six design-principle pillars.

**Negative test:** query a nonexistent lens alias; the filter returns
empty, confirming the alias must be exact.

**Cleanup:** none (read-only).

### Lab 10.3 — Understand benefits of and strategies for migration

**Objective:** Surface the migration tooling that operationalizes the
"7 Rs" strategies.

```bash
aws discovery describe-configurations --configuration-ids none 2>&1 | head -1
aws mgn describe-source-servers --query 'items[].sourceServerID' --output text
```

**Expected result:** the Application Migration Service responds (an empty
server list in a fresh account) — the rehost path is available and
API-driven.

**Negative test:** calling `aws mgn` in a Region where the service is not
initialized returns `UninitializedAccountException`, the prompt to
initialize before a migration.

**Cleanup:** none (read-only).

### Lab 10.4 — Understand concepts of cloud economics

**Objective:** Pull a real on-demand price from the Pricing API to ground
the capex-to-opex argument.

```bash
aws pricing get-products --service-code AmazonEC2 --region us-east-1 \
  --filters 'Type=TERM_MATCH,Field=instanceType,Value=t3.micro' \
            'Type=TERM_MATCH,Field=location,Value=US East (N. Virginia)' \
  --max-results 1 --query 'PriceList[0]' --output text | head -c 120
```

**Expected result:** a JSON price document for `t3.micro` — a concrete
per-hour figure, the unit cloud economics reasons about.

**Negative test:** omit the `location` filter and the query returns many
conflicting prices, showing why economics comparisons must fix the Region.

**Cleanup:** none (read-only).

### Lab 10.5 — Understand the AWS shared responsibility model

**Objective:** Enumerate the customer's half of the model — the security
surface AWS does *not* manage for you.

```bash
aws iam get-account-summary \
  --query 'SummaryMap.{MFADevices:MFADevices,AccessKeys:AccountAccessKeysPresent,Users:Users}'
```

**Expected result:** counts of IAM users, access keys, and MFA devices —
all "in the cloud" responsibilities that belong to the customer, not AWS.

**Negative test:** there is no API that returns AWS's side (hypervisor
patching, physical security); its absence *is* the lesson — that half is
not yours to query or manage.

**Cleanup:** none (read-only).

### Lab 10.6 — Understand security, governance, and compliance concepts

**Objective:** Show the governance service that continuously evaluates
configuration against rules.

```bash
aws configservice describe-configuration-recorders \
  --query 'ConfigurationRecorders[].name'
```

**Expected result:** either a recorder name or an empty list; either way
the governance control plane (AWS Config) answers — the mechanism behind
"continuous compliance."

**Negative test:** query compliance results with no recorder enabled;
`describe-compliance-by-config-rule` returns nothing, showing governance
requires the recorder to be on first.

**Cleanup:** none (read-only).

### Lab 10.7 — Identify AWS access management capabilities

**Objective:** Read the account password policy — one concrete access-
management control.

```bash
aws iam get-account-password-policy --query 'PasswordPolicy' 2>&1 | head -8
```

**Expected result:** the policy (minimum length, complexity, rotation) or
`NoSuchEntity` if none is set — both are valid findings about the account's
access posture.

**Negative test:** `NoSuchEntity` on a production account is itself a
finding: no enforced password policy is a governance gap.

**Cleanup:** none (read-only).

### Lab 10.8 — Identify components and resources for security

**Objective:** List the MFA devices protecting privileged identities.

```bash
aws iam list-virtual-mfa-devices \
  --query 'VirtualMFADevices[].{User:User.UserName,Serial:SerialNumber}' --output table
```

**Expected result:** a table of MFA devices and their assigned users — the
building blocks of identity security.

**Negative test:** a root entry with no MFA device is the highest-priority
security finding an account can surface.

**Cleanup:** none (read-only).

### Lab 10.9 — Define methods of deploying and operating in the AWS Cloud

**Objective:** Confirm the two primary operate-and-deploy control planes
(IaC and systems management) respond.

```bash
aws cloudformation list-stacks --query 'length(StackSummaries)' --output text
aws ssm describe-instance-information --query 'length(InstanceInformationList)' --output text
```

**Expected result:** two numeric counts — CloudFormation (deploy) and
Systems Manager (operate) are both reachable.

**Negative test:** `aws ssm send-command` against an instance with no SSM
agent fails with `InvalidInstanceId`, showing managed operations require the
agent.

**Cleanup:** none (read-only).

### Lab 10.10 — Define the AWS global infrastructure

**Objective:** Distinguish Regions from Availability Zones with data.

```bash
aws ec2 describe-availability-zones \
  --query 'AvailabilityZones[].{AZ:ZoneName,Type:ZoneType}' --output table
```

**Expected result:** at least three Availability Zones in the current
Region, each an isolated failure domain — the basis of every HA design.

**Negative test:** launch two "HA" instances into the *same* AZ; a single
AZ failure takes both down, the anti-pattern this topic exists to correct.

**Cleanup:** none (read-only).

### Lab 10.11 — Identify AWS compute services

**Objective:** Enumerate compute options by family.

```bash
aws ec2 describe-instance-types \
  --filters Name=instance-type,Values='t3.*' \
  --query 'InstanceTypes[].InstanceType' --output text | tr '\t' '\n' | head
```

**Expected result:** a list of `t3` general-purpose types — one of several
families (compute-, memory-, storage-optimized) the exam expects you to
distinguish.

**Negative test:** filter for `t9.*`; the empty result shows the family
names are fixed, not arbitrary.

**Cleanup:** none (read-only).

### Lab 10.12 — Identify AWS database services

**Objective:** Show the managed relational engines behind Amazon RDS.

```bash
aws rds describe-db-engine-versions \
  --query 'DBEngineVersions[].Engine' --output text | tr '\t' '\n' | sort -u
```

**Expected result:** engines such as `aurora-mysql`, `postgres`, `mysql`,
`mariadb`, `oracle-ee`, `sqlserver-*` — the managed relational catalog.

**Negative test:** there is no `mongodb` engine here; document databases
live in a different service (Amazon DocumentDB), a common distractor.

**Cleanup:** none (read-only).

### Lab 10.13 — Identify AWS network services

**Objective:** Confirm the account's default VPC — the base networking
primitive.

```bash
aws ec2 describe-vpcs --filters Name=isDefault,Values=true \
  --query 'Vpcs[0].{VpcId:VpcId,Cidr:CidrBlock}'
```

**Expected result:** the default VPC's ID and CIDR — the network every new
account starts with.

**Negative test:** in an account whose default VPC was deleted, the query
returns null, showing networking is a resource that can be absent.

**Cleanup:** none (read-only).

### Lab 10.14 — Identify AWS storage services

**Objective:** List S3 buckets and reason about storage classes.

```bash
aws s3api list-buckets --query 'length(Buckets)' --output text
aws s3api list-objects-v2 --bucket "$BUCKET_NAME" \
  --query 'Contents[].StorageClass' --output text 2>/dev/null | tr '\t' '\n' | sort -u
```

**Expected result:** a bucket count and the storage classes in use
(`STANDARD`, `STANDARD_IA`, `GLACIER`, …) — object storage plus its cost
tiers.

**Negative test:** request a byte-range read from an object archived in
Glacier without restoring it first; it fails with `InvalidObjectState`,
demonstrating class-dependent access.

**Cleanup:** none (read-only).

### Lab 10.15 — Identify AI/ML and analytics services

**Objective:** List the managed foundation models and confirm a query
engine is reachable.

```bash
aws bedrock list-foundation-models --region us-east-1 \
  --query 'length(modelSummaries)' --output text
aws athena list-work-groups --query 'WorkGroups[].Name' --output text
```

**Expected result:** a nonzero model count (Bedrock) and at least the
`primary` Athena workgroup — the AI/ML and analytics surfaces the exam
groups together.

**Negative test:** call `aws bedrock` in an unsupported Region; it returns
an endpoint error, showing these services are Region-scoped.

**Cleanup:** none (read-only).

### Lab 10.16 — Identify services from other in-scope categories

**Objective:** Touch the application-integration category (messaging).

```bash
aws sns list-topics --query 'length(Topics)' --output text
aws sqs list-queues --query 'length(QueueUrls)' --output text
```

**Expected result:** two counts — SNS (pub/sub) and SQS (queues), the
decoupling primitives that appear across many in-scope categories.

**Negative test:** publish to a non-existent topic ARN; `NotFound` proves
the topic must exist before it can decouple anything.

**Cleanup:** none (read-only).

### Lab 10.17 — Compare AWS pricing models

**Objective:** Contrast On-Demand with Spot using live Spot prices.

```bash
aws ec2 describe-spot-price-history --instance-types t3.micro \
  --product-descriptions "Linux/UNIX" --max-items 1 \
  --query 'SpotPriceHistory[0].SpotPrice' --output text
```

**Expected result:** a Spot price well below the On-Demand rate from Lab
10.4 — the concrete trade-off (lower cost, interruptible) the exam tests.

**Negative test:** treat Spot as guaranteed capacity; a Spot interruption
notice (2-minute warning) proves the discount buys interruptible capacity, not
reliability.

**Cleanup:** none (read-only).

### Lab 10.18 — Understand billing, budget, and cost-management resources

**Objective:** Read month-to-date spend from Cost Explorer.

```bash
aws ce get-cost-and-usage --time-period Start=$(date -u +%Y-%m-01),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY --metrics UnblendedCost \
  --query 'ResultsByTime[0].Total.UnblendedCost.Amount' --output text
```

**Expected result:** a dollar figure for the current month — the data
Budgets and Cost Explorer visualize.

**Negative test:** query a future month; the empty result shows cost data
is historical, so budgets are the forward-looking control.

**Cleanup:** none (read-only).

### Lab 10.19 — Identify AWS technical resources and Support options

**Objective:** List the Support plan surface and available services.

```bash
aws support describe-services --query 'services[0].name' --output text 2>&1 | head -1
```

**Expected result:** a service name if the account has Business/Enterprise
Support, or `SubscriptionRequiredException` on Basic Support — either
outcome identifies the account's support tier.

**Negative test:** `SubscriptionRequiredException` confirms the Support API
itself requires a paid plan, a fact the exam tests directly.

**Cleanup:** none (read-only).

### Lab 10.20 — Explain basic AI concepts and terminologies

**Objective:** Distinguish model modalities from the Bedrock catalog.

```bash
aws bedrock list-foundation-models --region us-east-1 \
  --query 'modelSummaries[].{Model:modelId,In:inputModalities,Out:outputModalities}' \
  --output table | head -20
```

**Expected result:** models tagged with input/output modalities (TEXT,
IMAGE, EMBEDDING) — the concrete meaning of terms like "multimodal."

**Negative test:** filter for an `AUDIO` output modality that no listed
model supports; the empty result shows modality is a real model property,
not a label you can assume.

**Cleanup:** none (read-only).

### Lab 10.21 — Identify practical use cases for AI

**Objective:** Run a managed AI service on real input — sentiment
detection.

```bash
aws comprehend detect-sentiment --language-code en \
  --text "The migration finished ahead of schedule and under budget." \
  --query 'Sentiment'
```

**Expected result:** `POSITIVE` — a use case (text analytics) solved
without training a model, illustrating "AI as a managed service."

**Negative test:** pass `--language-code zz`; `UnsupportedLanguageException`
shows even managed AI has defined input constraints.

**Cleanup:** none (read-only).

### Lab 10.22 — Describe the AI/ML development lifecycle

**Objective:** Show the lifecycle stages SageMaker makes explicit.

```bash
aws sagemaker list-endpoints --query 'length(Endpoints)' --output text
aws sagemaker list-training-jobs --query 'length(TrainingJobSummaries)' --output text
```

**Expected result:** counts of training jobs (build/train stage) and
endpoints (deploy/monitor stage) — the two ends of the ML lifecycle in one
service.

**Negative test:** invoke an endpoint that is not `InService`; the call
fails, showing "deployed" is a distinct lifecycle state from "trained."

**Cleanup:** none (read-only).

### Lab 10.23 — Explain the basic concepts of generative AI

**Objective:** Isolate the text-generation foundation models.

```bash
aws bedrock list-foundation-models --region us-east-1 \
  --by-output-modality TEXT \
  --query 'modelSummaries[].modelId' --output text | tr '\t' '\n' | head
```

**Expected result:** a set of text-output FMs — the generative core, as
distinct from embedding or image models.

**Negative test:** filter `--by-output-modality VIDEO`; an empty or short
list shows the generative catalog is modality-specific.

**Cleanup:** none (read-only).

### Lab 10.24 — Understand capabilities and limitations of GenAI

**Objective:** Invoke a model and observe both a useful answer and a
limitation (no live data).

```bash
aws bedrock-runtime invoke-model --region us-east-1 \
  --model-id amazon.titan-text-express-v1 \
  --body '{"inputText":"In one sentence, what is Amazon S3?","textGenerationConfig":{"maxTokenCount":60}}' \
  --cli-binary-format raw-in-base64-out /tmp/titan-out.json >/dev/null && \
  python3 -c "import json;print(json.load(open('/tmp/titan-out.json'))['results'][0]['outputText'][:120])"
```

**Expected result:** a fluent one-sentence definition of S3.
**Cost:** a few hundred tokens, well under one cent.

**Negative test:** ask "what is today's date?"; the model cannot answer
correctly from training data alone — the limitation (no real-time
knowledge) that motivates retrieval augmentation.

**Cleanup:** `rm -f /tmp/titan-out.json`.

### Lab 10.25 — Describe AWS infrastructure and technologies for GenAI

**Objective:** Show the managed retrieval-augmentation surface (Bedrock
Knowledge Bases).

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1 \
  --query 'length(knowledgeBaseSummaries)' --output text 2>&1 | head -1
```

**Expected result:** a count (often zero in a fresh account) — the managed
RAG building block exists and is API-addressable.

**Negative test:** query knowledge bases in a Region without Bedrock Agents;
the endpoint error shows the GenAI infrastructure is Region-bound.

**Cleanup:** none (read-only).

### Lab 10.26 — Describe design considerations for FM applications

**Objective:** List the guardrail policies that shape safe FM application
design.

```bash
aws bedrock list-guardrails --region us-east-1 \
  --query 'guardrails[].{Name:name,Status:status}' --output table 2>&1 | head
```

**Expected result:** any configured guardrails, or an empty list — the
control that enforces content and topic boundaries at design time.

**Negative test:** invoke a model with a guardrail that denies a topic and
send that topic; the response is blocked, proving the design control acts
at runtime.

**Cleanup:** none (read-only).

### Lab 10.27 — Choose effective prompt-engineering techniques

**Objective:** Compare a vague prompt with a structured one and see the
difference.

```bash
aws bedrock-runtime invoke-model --region us-east-1 \
  --model-id amazon.titan-text-express-v1 \
  --body '{"inputText":"List exactly three AWS storage services as a numbered list, names only.","textGenerationConfig":{"maxTokenCount":60}}' \
  --cli-binary-format raw-in-base64-out /tmp/prompt.json >/dev/null && \
  python3 -c "import json;print(json.load(open('/tmp/prompt.json'))['results'][0]['outputText'])"
```

**Expected result:** a clean numbered list of three services — structure
and constraints in the prompt produce structure in the output.
**Cost:** under one cent.

**Negative test:** re-run with just "storage?"; the vaguer prompt yields a
rambling, unstructured answer — the case for prompt engineering.

**Cleanup:** `rm -f /tmp/prompt.json`.

### Lab 10.28 — Describe the training and fine-tuning process for FMs

**Objective:** Show where customized models are tracked.

```bash
aws bedrock list-model-customization-jobs --region us-east-1 \
  --query 'length(modelCustomizationJobSummaries)' --output text 2>&1 | head -1
aws bedrock list-custom-models --region us-east-1 \
  --query 'length(modelSummaries)' --output text 2>&1 | head -1
```

**Expected result:** counts (usually zero) for customization jobs and
custom models — the fine-tuning lifecycle surface.

**Negative test:** starting a customization job without a training-data S3
URI fails validation, showing fine-tuning is data-driven, not a toggle.

**Cleanup:** none (read-only).

### Lab 10.29 — Describe methods to evaluate FM performance

**Objective:** Show the model-evaluation surface Bedrock provides.

```bash
aws bedrock list-evaluation-jobs --region us-east-1 \
  --query 'length(jobSummaries)' --output text 2>&1 | head -1
```

**Expected result:** a count of evaluation jobs — the managed way to score
models on accuracy, toxicity, and robustness rather than by intuition.

**Negative test:** compare two models by a single hand-picked prompt; the
inconsistency across prompts shows why systematic evaluation exists.

**Cleanup:** none (read-only).

### Lab 10.30 — Explain the development of responsible AI systems

**Objective:** Create a guardrail that enforces a responsible-AI policy.

```bash
aws bedrock create-guardrail --region us-east-1 --name responsible-ai-lab \
  --blocked-input-messaging "Blocked." --blocked-outputs-messaging "Blocked." \
  --content-policy-config '{"filtersConfig":[{"type":"HATE","inputStrength":"HIGH","outputStrength":"HIGH"}]}' \
  --query 'guardrailId' --output text
```

**Expected result:** a `guardrailId` — a codified responsible-AI control
that filters hateful content at high strength.

**Negative test:** send hateful input through the guardrail; it is blocked
with your configured message, proving the policy is enforced, not advisory.

**Cleanup:** `aws bedrock delete-guardrail --guardrail-identifier <id>`.

### Lab 10.31 — Recognize the importance of transparent and explainable models

**Objective:** Locate the bias/explainability tooling (SageMaker Clarify
runs as a processing job).

```bash
aws sagemaker list-processing-jobs \
  --query 'length(ProcessingJobSummaries)' --output text
```

**Expected result:** a count of processing jobs — the job type Clarify uses
to produce bias metrics and feature-attribution (SHAP) reports.

**Negative test:** a model deployed with no Clarify report offers no
feature attributions, the opacity that transparency requirements exist to
prevent.

**Cleanup:** none (read-only).

### Lab 10.32 — Explain methods to secure AI systems

**Objective:** Confirm whether model-invocation logging (the AI audit
trail) is enabled.

```bash
aws bedrock get-model-invocation-logging-configuration --region us-east-1 \
  --query 'loggingConfig.cloudWatchConfig.logGroupName' --output text 2>&1 | head -1
```

**Expected result:** a log-group name if invocation logging is on, or
`None` — a direct read of one AI security control.

**Negative test:** `None` means prompts and completions are not audited; on
a production AI system that is a security finding.

**Cleanup:** none (read-only).

### Lab 10.33 — Recognize governance and compliance regulations for AI systems

**Objective:** Turn on the governance control from Lab 10.32 — invocation
logging to CloudWatch.

```bash
aws logs create-log-group --log-group-name /ai/bedrock-audit 2>/dev/null
aws bedrock put-model-invocation-logging-configuration --region us-east-1 \
  --logging-config '{"cloudWatchConfig":{"logGroupName":"/ai/bedrock-audit","roleArn":"'"$BEDROCK_LOG_ROLE"'"},"textDataDeliveryEnabled":true}'
aws bedrock get-model-invocation-logging-configuration --region us-east-1 \
  --query 'loggingConfig.textDataDeliveryEnabled' --output text
```

**Expected result:** `True` — invocation logging is now delivering the
audit record that compliance regimes for AI require.

**Negative test:** supply a role ARN Bedrock cannot assume;
`ValidationException` shows the audit sink must be genuinely writable, not
merely declared.

**Cleanup:** delete the logging configuration and the `/ai/bedrock-audit`
log group.

### Lab 10.34 — Build a verified certification plan and cost-safe sandbox (integrative)

**Objective:** Build a verified, personal certification plan from
authoritative sources — confirming current codes yourself rather than
trusting this chapter — and stand up the cost-safe sandbox account you will
practice in.

**Cost note:** Steps 1–3 are free. Step 4 creates a budget alarm, which is
free; any resources you later create in the sandbox are not. Step 6 cleans
up.

**Prerequisites**

- An AWS account you may use as a sandbox, ideally a dedicated member
  account under an organization
  ([Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)).
- The readiness tracker from the Implementation section.

**Steps**

1. **Confirm the lineup (target 10 minutes).** From
   [aws.amazon.com/certification](https://aws.amazon.com/certification/),
   list the current certifications and note any retirement text appearing
   in a certification's name.

   **Expected result:** a list matching this chapter's table — or a
   documented difference, which means this chapter has aged and the
   currency check in Chapter 13 is due.

2. **Confirm three codes (target 10 minutes).** For three certifications
   you might sit, open each certification's own page and extract the code
   from its Skill Builder exam-prep link.

   **Expected result:** three codes confirmed from primary sources, not
   from this chapter.

3. **Choose and justify (target 15 minutes).** Fill the readiness tracker
   for only the certifications your role justifies, and write one sentence
   per row explaining why it is on your list.

   **Expected result:** a short, defensible plan — for most readers two or
   three certifications, not twelve.

4. **Create the cost guardrail (target 10 minutes).** In the sandbox
   account, create an AWS Budget with an alert threshold, as in
   [Chapter 7](07-observability-automation-performance-and-cost-governance.md).

   **Expected result:** a budget alarm that will email you before study
   labs become an expensive surprise.

5. **Negative test (target 5 minutes).** Deliberately look up one
   certification on a third-party "AWS certification list" site and compare
   its code and lineup against what you confirmed in steps 1–2.

   **Expected result:** you find at least one discrepancy — a stale code, a
   retired certification still listed, or a missing new one. This is the
   point of the exercise: it demonstrates why step 2 uses primary sources.

6. **Cleanup:** the budget alarm is free and worth keeping. Remove any
   other resources created while exploring, and confirm the sandbox has no
   running compute before you stop.

## Lab Verification

Complete this sign-off once the plan has been built from confirmed codes
and the budget guardrail is active. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The AWS certification program has four levels — foundational, associate,
professional, and specialty — and twelve current certifications, none of
which is a formal prerequisite for another. Levels describe assumed depth
and experience, so the right first exam is the one matching your role.
The `-C0x` suffix is the blueprint version and is the fastest way to spot
stale study material. The foundational tier (Cloud Practitioner CLF-C02,
AI Practitioner AIF-C01) exists mainly for people who need credible cloud
or AI fluency without a build role; working engineers should usually start
higher. Certifications last three years, and a higher-level pass generally
carries lower-level ones forward. Because the program churns, confirm every
code from AWS's own pages rather than from any summary, including this one.

- [ ] Can name the four levels and explain that none gates another.
- [ ] Can list the twelve current certifications and read the `-C0x`
      suffix.
- [ ] Knows CloudOps Engineer – Associate is the renamed SysOps
      Administrator.
- [ ] Can say who should and should not sit the foundational exams.
- [ ] Understands the three-year validity and how higher certifications
      extend lower ones.
- [ ] Has confirmed at least three exam codes from primary AWS sources.
- [ ] Completed the hands-on lab, including the budget guardrail and the
      third-party-discrepancy negative test.
