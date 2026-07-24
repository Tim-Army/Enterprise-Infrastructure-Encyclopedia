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
