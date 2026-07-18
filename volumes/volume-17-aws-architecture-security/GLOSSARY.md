# Volume XVII Glossary

Definitions for terms introduced in **Volume XVII — AWS Architecture and
Security**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Account Factory** — AWS Control Tower's self-service capability for
provisioning new, policy-compliant AWS accounts into a landing zone.
Introduced in Chapter 02.

**AWS Backup** — A centralized service for defining backup plans, vaults,
and lifecycle/retention policy across multiple AWS storage and database
services from a single control point. Introduced in Chapter 05.

**AWS Config** — A service that continuously records resource
configuration and evaluates it against Config rules, providing the
detective counterpart to preventive service control policies. Introduced
in Chapter 07.

**AWS Control Tower** — AWS's managed landing zone service, deploying and
maintaining a multi-account baseline including guardrails and Account
Factory. Introduced in Chapter 02.

**AWS Direct Connect** — A dedicated, private network connection from a
customer location into an AWS Direct Connect location, bypassing the
public internet for hybrid connectivity. Introduced in Chapter 03.

**AWS Global Accelerator** — A service that anycasts static IP addresses
across the AWS global network edge, routing to the closest healthy
endpoint for non-HTTP or mixed-protocol workloads. Introduced in Chapter
03.

**AWS Key Management Service (KMS)** — The managed service for creating
and controlling the cryptographic keys used to encrypt data at rest
across AWS storage and database services. Introduced in Chapter 05.

**AWS Organizations** — The service that groups multiple AWS accounts
under a single management account for consolidated billing and
centralized policy enforcement. Introduced in Chapter 02.

**AWS PrivateLink** — A mechanism for exposing a specific service to many
consumer VPCs or accounts through a private interface endpoint, without
network peering or route table exposure. Introduced in Chapter 03.

**AWS Resilience Hub** — A service that assesses a defined application
against a resiliency policy expressing target RTO/RPO and produces scored,
prioritized recommendations. Introduced in Chapter 06.

**AWS Resource Access Manager (RAM)** — The service used to share AWS
resources, such as a Transit Gateway, across accounts within an
Organization without duplicating the resource. Introduced in Chapter 03.

**AWS Schema Conversion Tool (SCT)** — A tool that translates database
schema and code from a source engine to a target engine during a
heterogeneous database migration. Introduced in Chapter 06.

**AWS Security Finding Format (ASFF)** — The normalized JSON format AWS
Security Hub uses to represent findings ingested from GuardDuty,
Inspector, Macie, Config, and third-party tools. Introduced in Chapter 08.

**AWS Shield** — AWS's managed DDoS protection service; Standard is
automatic and free for every customer, and Advanced adds enhanced
detection, cost protection, and DDoS Response Team access. Introduced in
Chapter 03.

**AWS Well-Architected Framework** — A structured set of six pillars —
Operational Excellence, Security, Reliability, Performance Efficiency,
Cost Optimization, and Sustainability — used to evaluate architectural
trade-offs. Introduced in Chapter 01.

**AWS Well-Architected Tool** — A free console and CLI tool that walks an
architect through a structured pillar-by-pillar review of a defined
workload, recording improvement items. Introduced in Chapter 01.

**AWS X-Ray** — A distributed tracing service that assembles a service
map and per-request trace across service boundaries to identify
latency contributors. Introduced in Chapter 07.

**Aurora Global Database** — Amazon Aurora's purpose-built, low-lag
cross-Region replication mechanism supporting up to five secondary read
Regions from one write Region. Introduced in Chapter 06.

**Availability Zone (AZ)** — One or more discrete data centers within an
AWS Region, with independent power, cooling, and networking, connected to
other AZs by low-latency private fiber. Introduced in Chapter 01.

**Change data capture (CDC)** — Ongoing replication of source database
changes to a target during a database migration, enabling low-downtime
cutover. Introduced in Chapter 06.

**Composite alarm** — A CloudWatch alarm that combines multiple
underlying alarms with Boolean logic to reduce alert noise from
correlated failures. Introduced in Chapter 07.

**Conformance pack** — A bundled, deployable set of AWS Config rules and
remediation actions, commonly deployed organization-wide. Introduced in
Chapter 07.

**Customer managed key (CMK)** — A KMS key whose key policy, rotation
schedule, and access are fully controlled by the customer, as opposed to
an AWS managed key. Introduced in Chapter 05.

**Delegated administrator** — An AWS Organizations member account granted
administrative rights over a specific service (such as GuardDuty or
Security Hub) across the entire Organization, without being the
management account. Introduced in Chapter 08.

**Direct Connect gateway** — A construct that lets a single Direct
Connect connection reach multiple VPCs across Regions and accounts.
Introduced in Chapter 03.

**DynamoDB Global Tables** — A DynamoDB feature replicating a table
across Regions with multi-Region, multi-active writes and eventual
consistency. Introduced in Chapter 05 and used as a DR mechanism in
Chapter 06.

**Execution role (Lambda)** — The IAM role an AWS Lambda function assumes
at runtime, scoping exactly what the function's code is permitted to do.
Introduced in Chapter 04.

**Failover routing policy** — A Route 53 routing policy that returns a
primary record while its health check passes and automatically shifts to
a secondary record when it fails. Introduced in Chapter 06.

**Gateway Load Balancer (GWLB)** — A Layer 3/4 load balancer that
transparently inserts third-party or custom traffic-inspection appliances
into a network path. Introduced in Chapter 04.

**IAM Identity Center** — AWS's workforce identity federation service,
mapping users and groups from a directory or external IdP to permission
sets provisioned as roles across accounts. Introduced in Chapter 02.

**IAM permission boundary** — A policy attached to an IAM user or role
that caps the maximum permissions identity-based policies can grant to
that principal. Introduced in Chapter 02.

**Interface endpoint** — A VPC endpoint implemented as an ENI in a
customer subnet, providing private connectivity to most AWS services and
PrivateLink-published SaaS services. Introduced in Chapter 03.

**Landing zone** — The automated multi-account baseline — Organizations
structure, log-archive account, baseline SCPs, and account vending — that
a new enterprise AWS environment is built from. Introduced in Chapter 02.

**Launch template** — A versioned, reusable EC2 configuration object
capturing AMI, instance type, security groups, and other launch
parameters. Introduced in Chapter 04.

**Migration wave** — A planned, sequenced group of workloads migrated
together during a cloud migration, ordered by dependency and risk.
Introduced in Chapter 06.

**Multi-site active/active** — A disaster recovery strategy in which two
or more Regions actively serve production traffic simultaneously,
minimizing RTO/RPO at the highest standing cost. Introduced in Chapter 06.

**Network ACL (NACL)** — A stateless, subnet-level traffic filter
evaluated in numbered rule order, supporting explicit allow and deny
rules. Introduced in Chapter 03.

**Organizational unit (OU)** — A hierarchical grouping construct within
AWS Organizations used to attach policy once and have it inherit to every
account beneath it. Introduced in Chapter 02.

**Permission set** — An IAM Identity Center template provisioned as an
IAM role in each assigned AWS account, granting federated, short-lived
access. Introduced in Chapter 02.

**Pilot light** — A disaster recovery strategy keeping minimal core
infrastructure (typically a replicated database) continuously running in
a DR Region, with compute scaled up only on failover. Introduced in
Chapter 06.

**Point-in-time recovery (PITR)** — A DynamoDB and RDS/Aurora capability
allowing restoration to any second within a defined retention window.
Introduced in Chapter 05.

**Posture-check script** — A read-only script verifying that multiple
chapters' guardrails (Organizations settings, S3 public access
configuration, GuardDuty/Security Hub enrollment, active alarms) are
simultaneously in place across an account. Introduced in Chapter 09.

**Recovery Point Objective (RPO)** — The maximum acceptable amount of
data loss, measured as time since the last recoverable state, used to
select a disaster recovery strategy. Introduced in Chapter 06.

**Recovery Time Objective (RTO)** — The maximum acceptable time between a
disaster and a workload being restored to service, used to select a
disaster recovery strategy. Introduced in Chapter 06.

**Reserved concurrency** — A Lambda setting that caps the maximum
concurrent executions of a function, protecting a limited-capacity
downstream dependency from being overwhelmed. Introduced in Chapter 04.

**Resource-based policy** — An IAM policy attached directly to a resource
(an S3 bucket policy, a KMS key policy) granting a principal, including a
cross-account principal, permission on that specific resource. Introduced
in Chapter 02.

**Security group** — A stateful, ENI-level traffic filter supporting
allow rules only, commonly referencing other security groups by ID rather
than hardcoded CIDR ranges. Introduced in Chapter 03.

**Service control policy (SCP)** — A JSON policy attached to an
Organizations root, OU, or account that defines the maximum permission
boundary IAM policies inside an account can grant, and cannot be
overridden by any in-account policy. Introduced in Chapter 02.

**Session policy** — A policy passed during an `AssumeRole` call that
further restricts a temporary session below the role's own permissions,
scoped to that session only. Introduced in Chapter 02.

**Storage class (Amazon S3)** — A per-object cost/retrieval-latency tier
(Standard, Standard-IA, Intelligent-Tiering, Glacier tiers) that S3
lifecycle rules can transition objects between automatically. Introduced
in Chapter 05.

**Target-tracking scaling policy** — An Auto Scaling policy type that
holds a chosen metric at a set target value by adding or removing
capacity automatically. Introduced in Chapter 04.

**Task execution role (ECS)** — The IAM role ECS itself uses to pull a
container image and write logs, kept deliberately separate from the task
role an application uses at runtime. Introduced in Chapter 04.

**Transit Gateway (TGW)** — A Regional routing hub enabling transitive
connectivity among many VPCs, VPN connections, and Direct Connect
gateways through centrally managed route tables. Introduced in Chapter 03.

**VPC endpoint** — A construct allowing private-subnet resources to reach
an AWS service without a NAT gateway or the public internet, implemented
as either a gateway endpoint (S3, DynamoDB) or an interface endpoint
(PrivateLink). Introduced in Chapter 03.

**VPC peering** — A point-to-point, non-transitive network connection
between exactly two VPCs. Introduced in Chapter 03.

**VPC Reachability Analyzer** — A tool that traces the actual hop-by-hop
path between a source and destination ENI, identifying which specific
route table entry or security group blocks a path. Introduced in Chapter
03.

**Warm standby** — A disaster recovery strategy running a fully
functional but minimally scaled copy of an environment continuously in a
DR Region, scaled up on failover. Introduced in Chapter 06.

**7 Rs (migration framework)** — The AWS Cloud Adoption Framework's seven
migration strategy classifications: Retire, Retain, Relocate, Rehost,
Replatform, Repurchase, and Refactor/re-architect. Introduced in Chapter
06.
