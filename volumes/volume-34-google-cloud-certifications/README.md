# Volume XXXIV — Google Cloud Certification Tracks

> The complete Google Cloud certification program in one volume:
> foundational, associate, and professional — with the exam format, fees,
> validity periods, and the platform knowledge each credential assesses.

## Overview

Volume XXXIV maps Google Cloud's certification program end to end and
teaches the platform knowledge behind it. It completes this
encyclopedia's coverage of the three major public clouds, alongside
[Volume XVII (AWS)](../volume-17-aws-architecture-security/README.md) and
[Volume XXXIII (Microsoft Azure)](../volume-33-microsoft-azure-certifications/README.md).

Every certification, fee, format, and validity period in this volume was
verified against Google Cloud's own certification pages on
**23 July 2026**.

Two structural facts shape the whole volume. **Google Cloud certifications
have no exam codes** — they are named credentials, so there is no version
suffix to signal that an exam has been re-scoped. And **professional
certifications expire in two years while foundational and associate ones
last three**, which inverts the usual intuition that the harder credential
lasts longer.

The volume is organized in four parts:

- **Chapter 01** maps the program: three levels, fourteen certifications,
  the absence of exam codes, and the fee and validity structure.
- **Chapters 02–04** cover the foundational and associate tiers — the
  entry credentials and the three associate certifications, which span
  three genuinely different product surfaces.
- **Chapters 05–08** cover the professional tier: the flagship architect
  certification, the infrastructure trio, the two security
  certifications, and the data and ML track.
- **Chapter 09** closes with certification operations — portfolio
  economics and the recurring currency check this program needs more than
  most.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab states its cost implications and ends in cleanup,
because every lab runs against a billable Google Cloud project.

## Chapters

1. [The Google Cloud Certification Program — Levels and Validity](chapters/01-the-google-cloud-certification-program-levels-and-validity.md) — three levels, fourteen certifications, the absence of exam codes, fees and validity by level, and the Google Cloud Next '26 exam refresh.
2. [Foundational — Cloud Digital Leader and Generative AI Leader](chapters/02-foundational-cloud-digital-leader-and-generative-ai-leader.md) — the two entry credentials, and the projects, resource hierarchy, billing, and additive-IAM scaffolding they assume.
3. [Associate Cloud Engineer](chapters/03-associate-cloud-engineer.md) — the working anchor: compute, networking, storage, and IAM, with basic versus predefined versus custom roles and service accounts.
4. [Associate Google Workspace Administrator and Data Practitioner](chapters/04-associate-workspace-administrator-and-data-practitioner.md) — the other two associate certifications, covering a different product surface and the data on-ramp.
5. [Professional Cloud Architect](chapters/05-professional-cloud-architect.md) — the flagship: published case studies, the landing zone, Shared VPC, and organization policy as a guardrail IAM cannot express.
6. [Infrastructure Professionals — Network Engineer, DevOps Engineer, and Developer](chapters/06-infrastructure-professionals-network-engineer-devops-engineer-and-developer.md) — global VPCs, hybrid connectivity, the SRE vocabulary of SLIs/SLOs/error budgets, and the application compute choices.
7. [Security Professionals — Cloud Security Engineer and Security Operations Engineer](chapters/07-security-professionals-cloud-security-engineer-and-security-operations-engineer.md) — building controls versus working alerts, CMEK, and VPC Service Controls as the exfiltration control IAM cannot provide.
8. [Data and ML Professionals — Data Engineer, Database Engineer, and Machine Learning Engineer](chapters/08-data-and-ml-professionals-data-engineer-database-engineer-and-machine-learning-engineer.md) — BigQuery's cost model, choosing a database, Spanner's distinctive combination, and MLOps over modeling.
9. [Certification Operations and Keeping the Program Current](chapters/09-certification-operations-and-keeping-the-program-current.md) — portfolio economics, why drift is harder to detect without exam codes, and the four-step currency check.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume maps the whole Google Cloud certification program, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The
table below is the state verified on 23 July 2026; confirm any
certification on its Google Cloud page before registering.

| Level | Certification | Length | Fee | Validity |
| --- | --- | --- | --- | --- |
| Foundational | Cloud Digital Leader | 90 min | $99 | 3 years |
| Foundational | Generative AI Leader | 90 min | $99 | 3 years |
| Associate | Cloud Engineer | 2 hours | $125 | 3 years |
| Associate | Google Workspace Administrator | 2 hours | $125 | 3 years |
| Associate | Data Practitioner | 2 hours | $125 | 3 years |
| Professional | Cloud Architect | 2 hours | $200 | 2 years |
| Professional | Cloud Database Engineer | 2 hours | $200 | 2 years |
| Professional | Cloud Developer | 2 hours | $200 | 2 years |
| Professional | Data Engineer | 2 hours | $200 | 2 years |
| Professional | Cloud DevOps Engineer | 2 hours | $200 | 2 years |
| Professional | Cloud Security Engineer | 2 hours | $200 | 2 years |
| Professional | Cloud Network Engineer | 2 hours | $200 | 2 years |
| Professional | Machine Learning Engineer | 2 hours | $200 | 2 years |
| Professional | Security Operations Engineer | 2 hours | $200 | 2 years |

Fees exclude tax. All exams are 50–60 multiple choice and multiple select
questions (foundational is multiple choice), delivered online-proctored or
onsite.

### Four facts to carry into any study plan

**No certification is a prerequisite for another.** Google states no
prerequisites even at professional level, offering recommended experience
instead — typically three or more years of industry experience including
one or more on Google Cloud.

**There are no exam codes.** Unlike AWS's `SAA-C03` or Azure's `AZ-104`, a
Google Cloud certification is identified only by name. Currency is checked
by presence on the certification page, by the exam guide's section list,
and by program notices — never by a version suffix, because there is none.

**Professional certifications expire soonest.** Two years against three
for everything else, and recertification is a full paid retake — there is
no free renewal assessment. That makes a professional credential roughly
$100 a year to hold, against $42 for an associate.

**The program is mid-refresh.** Google's certification page states exams
are being updated for **Google Cloud Next '26**, naming the **Gemini
Enterprise Agent Platform** and **Google Cloud's data and analytics
stack**, and directs candidates to each exam guide for the products
actually covered. The data and AI certifications are the most affected.

### Lab coverage — Associate Cloud Engineer

Labs are mapped to the certification's published **exam guide topics**,
which this repository treats as the blueprint. Every topic in the guide
has a walkthrough lab in
[Chapter 03](chapters/03-associate-cloud-engineer.md); section weights are
Google's own.

| Exam guide section | Topic | Lab |
| --- | --- | --- |
| 1 — Setting up a cloud solution environment (~20%) | 1.1 Cloud projects and accounts | 3.1 |
| | 1.2 Billing configuration | 3.2 |
| 2 — Planning and configuring (~17.5%) | 2.1 Compute resources | 3.3 |
| | 2.2 Data storage options | 3.4 |
| | 2.3 Network resources | 3.5 |
| 3 — Deploying and implementing (~25%) | 3.1 Compute Engine | 3.6 |
| | 3.2 Google Kubernetes Engine | 3.7 |
| | 3.3 Cloud Run and Cloud Functions | 3.8 |
| | 3.4 Data solutions | 3.9 |
| | 3.5 Networking resources | 3.10 |
| | 3.6 Infrastructure as code | 3.11 |
| 4 — Ensuring successful operation (~20%) | 4.1 Managing Compute Engine | 3.12 |
| | 4.2 Managing GKE | 3.13 |
| | 4.3 Managing Cloud Run | 3.14 |
| | 4.4 Managing storage and databases | 3.15 |
| | 4.5 Managing networking | 3.16 |
| | 4.6 Monitoring and logging | 3.17 |
| 5 — Configuring access and security (~17.5%) | 5.1 Managing IAM | 3.18 |
| | 5.2 Managing service accounts | 3.19, 3.20 |

Lab 3.20 is the negative test (proving a predefined role is genuinely
scoped) and 3.21 is cleanup. Every lab is a **walkthrough**: the runnable
command plus the expected result to check against.

**All fourteen certifications in this volume now carry topic-level lab
coverage**, mapped to each certification's published exam guide (Chapters
02–08). Chapter 01 (program planning) and Chapter 09 (currency check)
carry process labs rather than blueprint-topic labs, since their subject is
the program itself rather than a product surface.

### Lab coverage — Professional Cloud Architect

Mapped to the exam guide's own sections and weights (harvested from
Google's published guide PDF). Labs are in
[Chapter 05](chapters/05-professional-cloud-architect.md).

| Exam guide section | Topic | Lab |
| --- | --- | --- |
| 1 — Designing and planning (~25%) | 1.1 Business requirements | 5.1 |
| | 1.2 Technical requirements | 5.2 |
| | 1.3 Network, storage, compute | 5.3 |
| | 1.4 Migration plan | 5.4 |
| | 1.5 Future improvements | 5.5 |
| 2 — Managing and provisioning (~17.5%) | 2.1 Network topologies | 5.6 |
| | 2.2 Storage systems | 5.7 |
| | 2.3 Compute systems | 5.8 |
| | 2.4 Gemini Enterprise Agent Platform | 5.9 |
| | 2.5 Prebuilt solutions and APIs | 5.10 |
| 3 — Security and compliance (~17.5%) | 3.1 Designing for security | 5.11 |
| | 3.2 Designing for compliance | 5.12 |
| 4 — Technical and business processes (~15%) | 4.1 Technical processes | 5.13 |
| | 4.2 Business processes | 5.14 |
| 5 — Managing implementation (~12.5%) | 5.1 Advising teams | 5.15 |
| | 5.2 Interacting programmatically | 5.16 |
| 6 — Solution and operations excellence (~12.5%) | 6.2 Observability | 5.17 |
| | 6.3 / 6.5 Release and quality control | 5.18 |

Lab 5.19 is the negative test and cleanup. **Topics 2.4 and 2.5 name the
Gemini Enterprise Agent Platform** — content that entered the guide with
the Google Cloud Next '26 refresh, and the newest material on the exam.

### Lab coverage — Foundational

Cloud Digital Leader is a knowledge credential (no build); its labs read
the platform facts the exam asks about. Generative AI Leader is mapped to
its exam-guide sections. Labs are in
[Chapter 02](chapters/02-foundational-cloud-digital-leader-and-generative-ai-leader.md).

| Certification / section | Lab |
| --- | --- |
| Cloud Digital Leader — digital transformation | 2.1 |
| Cloud Digital Leader — modernization | 2.2 |
| Cloud Digital Leader — data and AI | 2.3 |
| Cloud Digital Leader — trust, security, operations | 2.4 |
| Generative AI Leader §1 — fundamentals of gen AI | 2.5 |
| Generative AI Leader §2 — Google Cloud's gen AI offerings | 2.6 |
| Generative AI Leader §3 — techniques to improve output | 2.7 |
| Generative AI Leader §4 — business strategy, responsible AI | 2.8 |

Labs 2.9–2.10 verify the shared scaffolding and the negative test.

### Lab coverage — Associate Workspace Administrator and Data Practitioner

Data Practitioner is mapped topic by topic to its exam guide; Workspace
Administrator is covered per guide section (administered in the Admin
console / Admin SDK, not `gcloud`). Labs are in
[Chapter 04](chapters/04-associate-workspace-administrator-and-data-practitioner.md).

| Exam guide topic | Lab |
| --- | --- |
| Data Practitioner 1.1 Prepare and process data | 4.1 |
| Data Practitioner 1.2 Extract and load | 4.2 |
| Data Practitioner 2.x Analysis and presentation | 4.3 |
| Data Practitioner 3.1 Design pipelines | 4.4 |
| Data Practitioner 3.2 Schedule and monitor | 4.5 |
| Data Practitioner 4.1 Access control and governance | 4.6 |
| Data Practitioner 4.2 Lifecycle management | 4.7 |
| Workspace 1 User accounts, domains, Directory | 4.8, 4.10 |
| Workspace 1.2 Organizational units | 4.9 |
| Workspace 2 Core Workspace services | 4.11 |
| Workspace 3 Data governance and compliance | 4.12 |
| Workspace 4 Security policies and access | 4.13 |
| Workspace 5 Browsers and endpoints | 4.14 |
| Workspace 6 Monitoring and troubleshooting | 4.15 |

Lab 4.16 is the negative test and cleanup.

### Lab coverage — Infrastructure Professionals

Network Engineer and DevOps Engineer are mapped topic by topic to their
exam guides; Developer shares the Cloud Run / GKE / integration surface
those labs exercise. Labs are in
[Chapter 06](chapters/06-infrastructure-professionals-network-engineer-devops-engineer-and-developer.md).

| Exam guide topic | Lab |
| --- | --- |
| Network 1.1–1.4 Designing/planning the VPC | 6.1–6.4 |
| Network 2.1 Configuring VPCs | 6.5 |
| Network 2.2 VPC routing | 6.6 |
| Network 2.3 / 4.4 Network Connectivity Center | 6.7 |
| Network 2.4 GKE clusters | 6.8 |
| Network 3.1 Load balancing | 6.9 |
| Network 3.2 Cloud CDN | 6.10 |
| Network 3.3 Cloud DNS | 6.11 |
| Network 4.1–4.3 Interconnect, VPN, Router | 6.12 |
| Network 5.1 Logging and monitoring | 6.13 |
| Network 5.2 Troubleshooting connectivity | 6.14 |
| Network 6.1–6.2 Cloud Armor, firewall policies | 6.15 |
| Network 6.4 Packet Mirroring, appliances | 6.16 |
| DevOps 1.1–1.5 Bootstrapping the org | 6.17 |
| DevOps 2.1–2.4 CI/CD pipelines and secrets | 6.18 |
| DevOps 3.1–3.3 SRE practices, error budgets | 6.19 |
| DevOps 4.1–4.5 Observability | 6.20 |
| DevOps 5.1–5.2 Performance and FinOps | 6.21 |

Lab 6.22 is the negative test (default-deny firewall) and cleanup.

### Lab coverage — Security Professionals

Cloud Security Engineer mapped topic by topic; Security Operations
Engineer touched where detection/response adjoins (Labs 7.13, 7.15). Labs
are in [Chapter 07](chapters/07-security-professionals-cloud-security-engineer-and-security-operations-engineer.md).

| Exam guide topic | Lab |
| --- | --- |
| 1.1 Cloud Identity | 7.1 |
| 1.2 Service accounts | 7.2 |
| 1.3 Authentication | 7.3 |
| 1.4 Authorization controls | 7.4 |
| 1.5 Resource hierarchy | 7.5 |
| 2.1 Perimeter security | 7.6 |
| 2.2 Boundary segmentation | 7.7 |
| 2.3 Private connectivity | 7.8 |
| 3.1 Preventing data loss | 7.9 |
| 3.2 Encryption (CMEK) | 7.10 |
| 3.3 Securing AI workloads | 7.11 |
| 4.1 Automating security | 7.12 |
| 4.2 Logging, monitoring, detection | 7.13 |
| 5.1 Compliance | 7.14 |

Lab 7.15 covers Data Access audit logs; 7.16 is the CMEK negative test and cleanup.

### Lab coverage — Data and ML Professionals

Data Engineer mapped topic by topic; Database Engineer and Machine
Learning Engineer covered at section level (Lab 8.19) with their published
weights. Labs are in
[Chapter 08](chapters/08-data-and-ml-professionals-data-engineer-database-engineer-and-machine-learning-engineer.md).

| Exam guide topic | Lab |
| --- | --- |
| Data Eng 1.1–1.4 Designing processing systems | 8.1–8.4 |
| Data Eng 2.1–2.3 Ingesting and processing | 8.5–8.7 |
| Data Eng 3.1–3.4 Storing the data | 8.8–8.11 |
| Data Eng 4.1–4.3 Preparing for analysis | 8.12–8.14 |
| Data Eng 5.1–5.5 Maintaining and automating | 8.15–8.18 |
| Database Eng §1–4; ML Eng §1–6 | 8.19 |

Lab 8.20 is the partitioning negative test and cleanup.

### Training access

**[Google Skills](https://cloud.google.com/learn)** provides a free
learning path for every certification in this volume, with on-demand
courses and hands-on labs. Professional Cloud Architect additionally
publishes **case studies in advance** — reading them before exam day is
free preparation. Exams themselves are paid. The
[course-catalog appendix](../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
records the training path and access model per certification.

## Software and platform baseline

Chapters reference the current GA Google Cloud service surface, the
`gcloud` CLI, and `bq`. Google Cloud service behavior and console paths
evolve continuously; treat the CLI examples as correct against the
baseline in [SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) and verify
current syntax against Google's documentation before production use.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-34-google-cloud-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
