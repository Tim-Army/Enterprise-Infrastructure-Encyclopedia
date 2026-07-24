# Volume XVII — AWS Architecture and Security

> Designing, securing, automating, and operating enterprise workloads on
> Amazon Web Services, from account foundations through detection and
> incident response, mapped to the AWS Certified Solutions Architect and
> AWS Certified Security certification paths.

## Overview

Volume XVII applies the Well-Architected Framework introduced in its own
first chapter across a complete AWS enterprise stack: account and
organization design, identity and governance, networking and hybrid
connectivity, compute and application architecture, storage and databases,
reliability and disaster recovery, observability and cost governance, and
security detection and incident response. Each chapter builds on the
account, identity, and network foundations established in Chapters 01–03,
and Chapter 09 closes the volume with a capstone that integrates every
preceding chapter into one reference architecture and one hands-on build.

The volume is organized in four parts:

- **Chapters 01–02** establish the account as the unit of isolation, the
  Well-Architected Framework as the volume's design vocabulary, and the
  multi-account, identity, and governance model (AWS Organizations, IAM,
  IAM Identity Center, and AWS Control Tower) every later chapter assumes.
- **Chapters 03–07** cover the technical domains an AWS architecture is
  built from: secure networking and hybrid/edge connectivity, compute and
  application architecture (EC2, containers, and serverless), storage and
  databases with data protection, reliability and disaster recovery, and
  observability, automation, and cost governance.
- **Chapters 08–09** complete the technical arc with security
  architecture, detection, and incident response, and a capstone chapter
  that synthesizes every prior chapter into one reference architecture and
  maps the volume to both certification paths.
- **Chapters 10–13** map the whole AWS certification program onto that
  technical content: the four-level program structure and foundational
  tier, the five associate certifications, the three professional
  certifications, and the shrinking specialty tier — closing with a
  recurring, primary-source currency check that keeps the map accurate.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and explicit cost implications with cleanup instructions to avoid
ongoing billing.

## Chapters

1. [Cloud Foundations, Accounts, and Well-Architected Design](chapters/01-cloud-foundations-accounts-and-well-architected-design.md) — the shared responsibility model, AWS global infrastructure, the six Well-Architected pillars, and root-account hardening.
2. [Multi-Account Identity, Governance, and Landing Zones](chapters/02-multi-account-identity-governance-and-landing-zones.md) — AWS Organizations, service control policies, IAM, IAM Identity Center, and AWS Control Tower landing zones.
3. [Secure Networking, Hybrid Connectivity, and Edge](chapters/03-secure-networking-hybrid-connectivity-and-edge.md) — VPC design, security groups and NACLs, Transit Gateway and PrivateLink, Direct Connect and Site-to-Site VPN, and Route 53/CloudFront/WAF at the edge.
4. [Compute, Containers, Serverless, and Application Architecture](chapters/04-compute-containers-serverless-and-application-architecture.md) — EC2 Auto Scaling, Amazon ECS and EKS, AWS Lambda, load balancer selection, and event-driven orchestration with Step Functions and EventBridge.
5. [Storage, Databases, Analytics, and Data Protection](chapters/05-storage-databases-analytics-and-data-protection.md) — S3, EBS, and EFS; RDS, Aurora, and DynamoDB; the Redshift/Glue/Athena/Lake Formation analytics stack; KMS encryption; and AWS Backup.
6. [Reliability, Migration, Multi-Region, and Disaster Recovery](chapters/06-reliability-migration-multi-region-and-disaster-recovery.md) — RTO/RPO-driven DR strategy selection, Route 53 failover, multi-Region replication, and migration with the 7 Rs, MGN, and DMS.
7. [Observability, Automation, Performance, and Cost Governance](chapters/07-observability-automation-performance-and-cost-governance.md) — CloudWatch, X-Ray, AWS Config, Systems Manager, infrastructure as code, and cost governance with Cost Explorer, Budgets, and Compute Optimizer.
8. [Security Architecture, Detection, and Incident Response](chapters/08-security-architecture-detection-and-incident-response.md) — GuardDuty, Inspector, Macie, and Security Hub; automated detection-to-response pipelines; and AWS-specific incident response phases.
9. [Solutions Architect and Security Training Capstone](chapters/09-solutions-architect-and-security-training-capstone.md) — a synthesized reference architecture, a certification blueprint domain map, and a capstone hands-on build spanning the full volume.
10. [The AWS Certification Program — Structure, Foundational Tier, and Recertification](chapters/10-the-aws-certification-program-structure-foundational-tier-and-recertification.md) — the four levels, all twelve current exams and codes, the `-C0x` suffix, Cloud Practitioner (CLF-C02) and AI Practitioner (AIF-C01), and three-year validity and recertification.
11. [The Associate Tier — Developer, CloudOps Engineer, Data Engineer, and Machine Learning Engineer](chapters/11-the-associate-tier-developer-cloudops-data-engineer-and-machine-learning-engineer.md) — DVA-C02, SOA-C03 (the renamed SysOps Administrator), DEA-C01, and MLA-C01 with its MLA-C02 transition, each mapped to this volume's chapters.
12. [The Professional Tier — Solutions Architect, DevOps Engineer, and Generative AI Developer](chapters/12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md) — SAP-C02, DOP-C02, and the new AIP-C01, with what actually changes at this tier: reading load, trade-off judgment, breadth, and organizational scale.
13. [Specialty Certifications, and Keeping the AWS Certification Program Current](chapters/13-specialty-certifications-and-keeping-the-aws-certification-program-current.md) — ANS-C01 (retiring 25 August 2026) and SCS-C03, where the four retired specialties went, and a four-step primary-source currency check.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all thirteen
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the current GA AWS service surface as
recorded in [SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md), dated
2026-07. AWS service behavior and console paths evolve continuously;
treat the CLI and Terraform (AWS provider, Terraform 1.9.x) examples in
this volume as correct against that baseline and verify current syntax
against official AWS documentation before applying them in production.

## Certification alignment

Chapters 01–09 are built around the **AWS Certified Solutions Architect –
Associate (SAA-C03)** and **AWS Certified Security – Specialty (SCS-C03)**
paths, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Chapter
09 provides a chapter-to-domain mapping and capstone exercise; always
confirm current blueprint domains and weighting against the official AWS
Training and Certification exam guide, since blueprints change
independently of this repository's release cycle.

**Chapters 10–13 map the rest of the program.** Every code below was
verified against AWS's own certification pages on 23 July 2026 — read from
the AWS Skill Builder exam-prep link each page carries, since AWS no longer
prints exam codes in page body text.

| Level | Certification | Code | Notes |
| --- | --- | --- | --- |
| Foundational | Cloud Practitioner | CLF-C02 | 90 min / 65 q |
| Foundational | AI Practitioner | AIF-C01 | 90 min / 65 q |
| Associate | Solutions Architect | SAA-C03 | covered by Chapters 01–09 |
| Associate | Developer | DVA-C02 | most code-dependent associate |
| Associate | CloudOps Engineer | SOA-C03 | renamed from SysOps Administrator |
| Associate | Data Engineer | DEA-C01 | first-generation blueprint |
| Associate | Machine Learning Engineer | MLA-C01 | MLA-C02 registration opens 1 Sep 2026 |
| Professional | Solutions Architect | SAP-C02 | 180 min / 75 q |
| Professional | DevOps Engineer | DOP-C02 | 180 min / 75 q |
| Professional | Generative AI Developer | AIP-C01 | newest professional exam |
| Specialty | Advanced Networking | ANS-C01 | **retires 25 August 2026** |
| Specialty | Security | SCS-C03 | covered by Chapter 08 |

Three structural facts worth carrying into any study plan. **No AWS
certification is a prerequisite for another** — the levels describe assumed
depth, not a required sequence. **The `-C0x` suffix is the blueprint
version**, and it is the fastest way to spot stale study material.
**The specialty tier is shrinking**: four specialties (Machine Learning,
Data Analytics, Database, SAP on AWS) already left the catalog with their
subject matter folded into role-based exams, and one of the two survivors
retires in August 2026. Chapter 13 defines the recurring currency check
that keeps this table, the
[course-catalog appendix](../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md),
and the repository blueprint in step.

## Topic-level lab coverage

Every task in all **twelve** current AWS exam guides is covered by a
hands-on **walkthrough** lab in this volume — **193 topic-level labs** in
all, plus one integrative lab per chapter. The task lists were harvested
from the authoritative exam guides at
`docs.aws.amazon.com/aws-certification` on 24 July 2026. Solutions
Architect – Associate (SAA-C03) and Security – Specialty (SCS-C03) are
distributed across the Chapter 01–09 architecture spine; the other ten
certifications map to the certification chapters 10–13. Each lab is a full
walkthrough — runnable command, expected result, a negative test, and
cleanup — and carries `**Lab verified by:** *pending*` until a human runs
it, per the root README Disclaimer.

### Cloud Practitioner (CLF-C02) — 19 topic-tasks

Labs in [Chapter 10](chapters/10-the-aws-certification-program-structure-foundational-tier-and-recertification.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Define the benefits of the AWS Cloud | Lab 10.1 |
| 1 | 1.2 Identify design principles of the AWS Cloud | Lab 10.2 |
| 1 | 1.3 Understand the benefits of and strategies for migration to the AWS Cloud | Lab 10.3 |
| 1 | 1.4 Understand concepts of cloud economics | Lab 10.4 |
| 2 | 2.1 Understand the AWS shared responsibility model | Lab 10.5 |
| 2 | 2.2 Understand AWS Cloud security, governance, and compliance concepts | Lab 10.6 |
| 2 | 2.3 Identify AWS access management capabilities | Lab 10.7 |
| 2 | 2.4 Identify components and resources for security | Lab 10.8 |
| 3 | 3.1 Define methods of deploying and operating in the AWS Cloud | Lab 10.9 |
| 3 | 3.2 Define the AWS global infrastructure | Lab 10.10 |
| 3 | 3.3 Identify AWS compute services | Lab 10.11 |
| 3 | 3.4 Identify AWS database services | Lab 10.12 |
| 3 | 3.5 Identify AWS network services | Lab 10.13 |
| 3 | 3.6 Identify AWS storage services | Lab 10.14 |
| 3 | 3.7 Identify AWS artificial intelligence and machine learning (AI/ML) services and analytics services | Lab 10.15 |
| 3 | 3.8 Identify services from other in-scope AWS service categories | Lab 10.16 |
| 4 | 4.1 Compare AWS pricing models | Lab 10.17 |
| 4 | 4.2 Understand resources for billing, budget, and cost management | Lab 10.18 |
| 4 | 4.3 Identify AWS technical resources and AWS Support options | Lab 10.19 |

### AI Practitioner (AIF-C01) — 14 topic-tasks

Labs in [Chapter 10](chapters/10-the-aws-certification-program-structure-foundational-tier-and-recertification.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Explain basic AI concepts and terminologies | Lab 10.20 |
| 1 | 1.2 Identify practical use cases for AI | Lab 10.21 |
| 1 | 1.3 Describe the AI/ML development lifecycle | Lab 10.22 |
| 2 | 2.1 Explain the basic concepts of generative AI (GenAI) | Lab 10.23 |
| 2 | 2.2 Understand the capabilities and limitations of GenAI for solving business problems | Lab 10.24 |
| 2 | 2.3 Describe AWS infrastructure and technologies for building GenAI applications | Lab 10.25 |
| 3 | 3.1 Describe design considerations for applications that use foundation models (FMs) | Lab 10.26 |
| 3 | 3.2 Choose effective prompt engineering techniques | Lab 10.27 |
| 3 | 3.3 Describe the training and fine-tuning process for FMs | Lab 10.28 |
| 3 | 3.4 Describe methods to evaluate FM performance | Lab 10.29 |
| 4 | 4.1 Explain the development of AI systems that are responsible | Lab 10.30 |
| 4 | 4.2 Recognize the importance of transparent and explainable models | Lab 10.31 |
| 5 | 5.1 Explain methods to secure AI systems | Lab 10.32 |
| 5 | 5.2 Recognize governance and compliance regulations for AI systems | Lab 10.33 |

### Developer – Associate (DVA-C02) — 13 topic-tasks

Labs in [Chapter 11](chapters/11-the-associate-tier-developer-cloudops-data-engineer-and-machine-learning-engineer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1 Develop code for applications hosted on AWS | Lab 11.1 |
| 1 | 2 Develop code for AWS Lambda | Lab 11.2 |
| 1 | 3 Use data stores in application development | Lab 11.3 |
| 2 | 1 Implement authentication and/or authorization for applications and AWS services | Lab 11.4 |
| 2 | 2 Implement encryption by using AWS services | Lab 11.5 |
| 2 | 3 Manage sensitive data in application code | Lab 11.6 |
| 3 | 1 Prepare application artifacts to be deployed to AWS | Lab 11.7 |
| 3 | 2 Test applications in development environments | Lab 11.8 |
| 3 | 3 Automate deployment testing | Lab 11.9 |
| 3 | 4 Deploy code by using AWS Continuous Integration and Continuous Delivery (CI/CD) services | Lab 11.10 |
| 4 | 1 Assist in a root cause analysis | Lab 11.11 |
| 4 | 2 Instrument code for observability | Lab 11.12 |
| 4 | 3 Optimize applications by using AWS services and features | Lab 11.13 |

### CloudOps Engineer – Associate (SOA-C03) — 13 topic-tasks

Labs in [Chapter 11](chapters/11-the-associate-tier-developer-cloudops-data-engineer-and-machine-learning-engineer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Implement metrics, alarms, and filters by using AWS monitoring and logging services | Lab 11.14 |
| 1 | 1.2 Identify and remediate issues by using monitoring and availability metrics | Lab 11.15 |
| 1 | 1.3 Implement performance optimization strategies for compute, storage, and database resources | Lab 11.16 |
| 2 | 2.1 Implement scalability and elasticity | Lab 11.17 |
| 2 | 2.2 Implement highly available and resilient environments | Lab 11.18 |
| 2 | 2.3 Implement backup and restore strategies | Lab 11.19 |
| 3 | 3.1 Provision and maintain cloud resources | Lab 11.20 |
| 3 | 3.2 Automate the management of existing resources | Lab 11.21 |
| 4 | 4.1 Implement and manage security and compliance tools and policies | Lab 11.22 |
| 4 | 4.2 Implement strategies to protect data and infrastructure | Lab 11.23 |
| 5 | 5.1 Implement and optimize networking features and connectivity | Lab 11.24 |
| 5 | 5.2 Configure domains, DNS services, and content delivery | Lab 11.25 |
| 5 | 5.3 Troubleshoot network connectivity issues | Lab 11.26 |

### Data Engineer – Associate (DEA-C01) — 17 topic-tasks

Labs in [Chapter 11](chapters/11-the-associate-tier-developer-cloudops-data-engineer-and-machine-learning-engineer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Perform data ingestion | Lab 11.27 |
| 1 | 1.2 Transform and process data | Lab 11.28 |
| 1 | 1.3 Orchestrate data pipelines | Lab 11.29 |
| 1 | 1.4 Apply programming concepts | Lab 11.30 |
| 2 | 2.1 Choose a data store | Lab 11.31 |
| 2 | 2.2 Understand data cataloging systems | Lab 11.32 |
| 2 | 2.3 Manage the lifecycle of data | Lab 11.33 |
| 2 | 2.4 Design data models and schema evolution | Lab 11.34 |
| 3 | 3.1 Automate data processing by using AWS services | Lab 11.35 |
| 3 | 3.2 Analyze data by using AWS services | Lab 11.36 |
| 3 | 3.3 Maintain and monitor data pipelines | Lab 11.37 |
| 3 | 3.4 Ensure data quality | Lab 11.38 |
| 4 | 4.1 Apply authentication mechanisms | Lab 11.39 |
| 4 | 4.2 Apply authorization mechanisms | Lab 11.40 |
| 4 | 4.3 Ensure data encryption and masking | Lab 11.41 |
| 4 | 4.4 Prepare logs for audit | Lab 11.42 |
| 4 | 4.5 Understand data privacy and governance | Lab 11.43 |

### Machine Learning Engineer – Associate (MLA-C01) — 12 topic-tasks

Labs in [Chapter 11](chapters/11-the-associate-tier-developer-cloudops-data-engineer-and-machine-learning-engineer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Ingest and store data | Lab 11.44 |
| 1 | 1.2 Transform data and perform feature engineering | Lab 11.45 |
| 1 | 1.3 Ensure data integrity and prepare data for modeling | Lab 11.46 |
| 2 | 2.1 Choose a modeling approach | Lab 11.47 |
| 2 | 2.2 Train and refine models | Lab 11.48 |
| 2 | 2.3 Analyze model performance | Lab 11.49 |
| 3 | 3.1 Select deployment infrastructure based on existing architecture and requirements | Lab 11.50 |
| 3 | 3.2 Create and script infrastructure based on existing architecture and requirements | Lab 11.51 |
| 3 | 3.3 Use automated orchestration tools to set up continuous integration and continuous delivery (CI/CD) pipelines | Lab 11.52 |
| 4 | 4.1 Monitor model inference | Lab 11.53 |
| 4 | 4.2 Monitor and optimize infrastructure and costs | Lab 11.54 |
| 4 | 4.3 Secure AWS resources | Lab 11.55 |

### Solutions Architect – Professional (SAP-C02) — 20 topic-tasks

Labs in [Chapter 12](chapters/12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Architect network connectivity strategies | Lab 12.1 |
| 1 | 1.2 Prescribe security controls | Lab 12.2 |
| 1 | 1.3 Design reliable and resilient architectures | Lab 12.3 |
| 1 | 1.4 Design a multi-account AWS environment | Lab 12.4 |
| 1 | 1.5 Determine cost optimization and visibility strategies | Lab 12.5 |
| 2 | 2.1 Design a deployment strategy to meet business requirements | Lab 12.6 |
| 2 | 2.2 Design a solution to ensure business continuity | Lab 12.7 |
| 2 | 2.3 Determine security controls based on requirements | Lab 12.8 |
| 2 | 2.4 Design a strategy to meet reliability requirements | Lab 12.9 |
| 2 | 2.5 Design a solution to meet performance objectives | Lab 12.10 |
| 2 | 2.6 Determine a cost optimization strategy to meet solution goals and objectives | Lab 12.11 |
| 3 | 3.1 Determine a strategy to improve overall operational excellence | Lab 12.12 |
| 3 | 3.2 Determine a strategy to improve security | Lab 12.13 |
| 3 | 3.3 Determine a strategy to improve performance | Lab 12.14 |
| 3 | 3.4 Determine a strategy to improve reliability | Lab 12.15 |
| 3 | 3.5 Identify opportunities for cost optimizations | Lab 12.16 |
| 4 | 4.1 Select existing workloads and processes for potential migration | Lab 12.17 |
| 4 | 4.2 Determine the optimal migration approach for existing workloads | Lab 12.18 |
| 4 | 4.3 Determine a new architecture for existing workloads | Lab 12.19 |
| 4 | 4.4 Determine opportunities for modernization and enhancements | Lab 12.20 |

### DevOps Engineer – Professional (DOP-C02) — 19 topic-tasks

Labs in [Chapter 12](chapters/12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Implement CI/CD pipelines | Lab 12.21 |
| 1 | 1.2 Integrate automated testing into CI/CD pipelines | Lab 12.22 |
| 1 | 1.3 Build and manage artifacts | Lab 12.23 |
| 1 | 1.4 Implement deployment strategies for instance, container, and serverless environments | Lab 12.24 |
| 2 | 2.1 Define cloud infrastructure and reusable components to provision and manage systems throughout their lifecycle | Lab 12.25 |
| 2 | 2.2 Deploy automation to create, onboard, and secure AWS accounts in a multi-account or multi-Region environment | Lab 12.26 |
| 2 | 2.3 Design and build automated solutions for complex tasks and large-scale environments | Lab 12.27 |
| 3 | 3.1 Implement highly available solutions to meet resilience and business requirements | Lab 12.28 |
| 3 | 3.2 Implement solutions that are scalable to meet business requirements | Lab 12.29 |
| 3 | 3.3 Implement automated recovery processes to meet RTO and RPO requirements | Lab 12.30 |
| 4 | 4.1 Configure the collection, aggregation, and storage of logs and metrics | Lab 12.31 |
| 4 | 4.2 Audit, monitor, and analyze logs and metrics to detect issues | Lab 12.32 |
| 4 | 4.3 Automate monitoring and event management of complex environments | Lab 12.33 |
| 5 | 5.1 Manage event sources to process, notify, and take action in response to events | Lab 12.34 |
| 5 | 5.2 Implement configuration changes in response to events | Lab 12.35 |
| 5 | 5.3 Troubleshoot system and application failures | Lab 12.36 |
| 6 | 6.1 Implement techniques for identity and access management at scale | Lab 12.37 |
| 6 | 6.2 Apply automation for security controls and data protection | Lab 12.38 |
| 6 | 6.3 Implement security monitoring and auditing solutions | Lab 12.39 |

### Generative AI Developer – Professional (AIP-C01) — 20 topic-tasks

Labs in [Chapter 12](chapters/12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Analyze requirements and design GenAI solutions | Lab 12.40 |
| 1 | 1.2 Select and configure FMs | Lab 12.41 |
| 1 | 1.3 Implement data validation and processing pipelines for FM consumption | Lab 12.42 |
| 1 | 1.4 Design and implement vector store solutions | Lab 12.43 |
| 1 | 1.5 Design retrieval mechanisms for FM augmentation | Lab 12.44 |
| 1 | 1.6 Implement prompt engineering strategies and governance for FM interactions | Lab 12.45 |
| 2 | 2.1 Implement agentic AI solutions and tool integrations | Lab 12.46 |
| 2 | 2.2 Implement model deployment strategies | Lab 12.47 |
| 2 | 2.3 Design and implement enterprise integration architectures | Lab 12.48 |
| 2 | 2.4 Implement FM API integrations | Lab 12.49 |
| 2 | 2.5 Implement application integration patterns and development tools | Lab 12.50 |
| 3 | 3.1 Implement input and output safety controls | Lab 12.51 |
| 3 | 3.2 Implement data security and privacy controls | Lab 12.52 |
| 3 | 3.3 Implement AI governance and compliance mechanisms | Lab 12.53 |
| 3 | 3.4 Implement responsible AI principles | Lab 12.54 |
| 4 | 4.1 Implement cost optimization and resource efficiency strategies | Lab 12.55 |
| 4 | 4.2 Optimize application performance | Lab 12.56 |
| 4 | 4.3 Implement monitoring systems for GenAI applications | Lab 12.57 |
| 5 | 5.1 Implement evaluation systems for GenAI | Lab 12.58 |
| 5 | 5.2 Troubleshoot GenAI applications | Lab 12.59 |

### Advanced Networking – Specialty (ANS-C01) — 16 topic-tasks

Labs in [Chapter 13](chapters/13-specialty-certifications-and-keeping-the-aws-certification-program-current.md#hands-on-lab).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Design a solution that incorporates edge network services to optimize user performance and traffic management for global architectures | Lab 13.1 |
| 1 | 1.2 Design DNS solutions that meet public, private, and hybrid requirements | Lab 13.2 |
| 1 | 1.3 Design solutions that integrate load balancing to meet high availability, scalability, and security requirements | Lab 13.3 |
| 1 | 1.4 Define logging and monitoring requirements across AWS and hybrid networks | Lab 13.4 |
| 1 | 1.5 Design a routing strategy and connectivity architecture between on-premises networks and the AWS Cloud | Lab 13.5 |
| 1 | 1.6 Design a routing strategy and connectivity architecture that include multiple AWS accounts, AWS Regions, and VPCs to support different connectivity patterns | Lab 13.6 |
| 2 | 2.1 Implement routing and connectivity between on-premises networks and the AWS Cloud | Lab 13.7 |
| 2 | 2.2 Implement routing and connectivity across multiple AWS accounts, Regions, and VPCs to support different connectivity patterns | Lab 13.8 |
| 2 | 2.3 Implement complex hybrid and multi-account DNS architectures | Lab 13.9 |
| 2 | 2.4 Automate and configure network infrastructure | Lab 13.10 |
| 3 | 3.1 Maintain routing and connectivity on AWS and hybrid networks | Lab 13.11 |
| 3 | 3.2 Monitor and analyze network traffic to troubleshoot and optimize connectivity patterns | Lab 13.12 |
| 3 | 3.3 Optimize AWS networks for performance, reliability, and cost-effectiveness | Lab 13.13 |
| 4 | 4.1 Implement and maintain network features to meet security and compliance needs and requirements | Lab 13.14 |
| 4 | 4.2 Validate and audit security by using network monitoring and logging services | Lab 13.15 |
| 4 | 4.3 Implement and maintain confidentiality of data and communications of the network | Lab 13.16 |

### Solutions Architect – Associate (SAA-C03) — 14 topic-tasks

Distributed across the Chapter 01–09 architecture spine.

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Design secure access to AWS resources | Lab 2.1 |
| 1 | 1.2 Design secure workloads and applications | Lab 3.1 |
| 1 | 1.3 Determine appropriate data security controls | Lab 5.1 |
| 2 | 2.1 Design scalable and loosely coupled architectures | Lab 4.1 |
| 2 | 2.2 Design highly available and/or fault-tolerant architectures | Lab 6.1 |
| 3 | 3.1 Determine high-performing and/or scalable storage solutions | Lab 5.2 |
| 3 | 3.2 Design high-performing and elastic compute solutions | Lab 4.2 |
| 3 | 3.3 Determine high-performing database solutions | Lab 5.3 |
| 3 | 3.4 Determine high-performing and/or scalable network architectures | Lab 3.2 |
| 3 | 3.5 Determine high-performing data ingestion and transformation solutions | Lab 5.4 |
| 4 | 4.1 Design cost-optimized storage solutions | Lab 7.1 |
| 4 | 4.2 Design cost-optimized compute solutions | Lab 7.2 |
| 4 | 4.3 Design cost-optimized database solutions | Lab 7.3 |
| 4 | 4.4 Design cost-optimized network architectures | Lab 7.4 |

### Security – Specialty (SCS-C03) — 16 topic-tasks

Distributed across the security spine (Chapters 02–08).

| Domain | Exam-guide task | Lab |
| --- | --- | --- |
| 1 | 1.1 Design and implement monitoring and alerting solutions for an AWS account or organization | Lab 8.1 |
| 1 | 1.2 Design and implement logging solutions | Lab 8.2 |
| 1 | 1.3 Troubleshoot security monitoring, logging, and alerting solutions | Lab 8.3 |
| 2 | 2.1 Design and test an incident response plan | Lab 8.4 |
| 2 | 2.2 Respond to security events | Lab 8.5 |
| 3 | 3.1 Design, implement, and troubleshoot security controls for network edge services | Lab 3.3 |
| 3 | 3.2 Design, implement, and troubleshoot security controls for compute workloads | Lab 8.6 |
| 3 | 3.3 Design and troubleshoot network security controls | Lab 3.4 |
| 4 | 4.1 Design, implement, and troubleshoot authentication strategies | Lab 2.2 |
| 4 | 4.2 Design, implement, and troubleshoot authorization strategies | Lab 2.3 |
| 5 | 5.1 Design and implement controls for data in transit | Lab 8.7 |
| 5 | 5.2 Design and implement controls for data at rest | Lab 5.5 |
| 5 | 5.3 Design and implement controls to protect confidential data, credentials, secrets, and cryptographic key materials | Lab 8.8 |
| 6 | 6.1 Develop a strategy to centrally deploy and manage AWS accounts | Lab 2.4 |
| 6 | 6.2 Implement a secure and consistent deployment strategy for cloud resources | Lab 2.5 |
| 6 | 6.3 Evaluate the compliance of AWS resources | Lab 8.9 |

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-17-aws-architecture-security

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-17-aws-architecture-security/chapters/01-cloud-foundations-accounts-and-well-architected-design.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
