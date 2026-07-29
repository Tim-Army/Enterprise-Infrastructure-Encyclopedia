# Volume VII Glossary

Definitions for terms introduced in **Volume VII — Cloud Infrastructure**,
alphabetized. See also the [volume index](INDEX.md) for pointers back to
the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Attribute-based access control (ABAC)** — An authorization model that
evaluates identity, resource, and request-context attributes at request
time (for example, a matching team tag) rather than relying solely on
named role membership, scaling better than RBAC when role/resource
combinations grow combinatorially. Introduced in Chapter 03.

**Autoscaling** — The automated addition or removal of compute capacity in
response to a reactive metric, a fixed schedule, or a demand forecast,
tuned to avoid thrashing between scale-out and scale-in states.
Introduced in Chapter 05.

**Availability zone (AZ)** — One or more discrete data centers within a
region engineered with independent power, cooling, and networking, so
that a single-zone failure does not take down the region. Introduced in
Chapter 01.

**Break-glass access** — An emergency access path that bypasses normal
approval flow but is fully logged, automatically time-boxed, and reviewed
after use. Introduced in Chapter 02.

**CAP theorem** — The principle that a distributed data store can provide
at most two of consistency, availability, and partition tolerance
simultaneously during a network partition; since partition tolerance is
effectively mandatory, the practical trade-off is between consistency and
availability. Introduced in Chapter 06.

**Chaos engineering** — The deliberate, controlled practice of injecting
failure into a system to validate that its resilience design behaves as
intended, run against a stated hypothesis with defined success criteria.
Introduced in Chapter 09.

**Chargeback** — Cost attribution that is actually debited against an
owning team's budget, as distinct from showback's visibility-only
attribution. Introduced in Chapter 08.

**CIDR allocation registry** — A central, version-controlled record of
which CIDR blocks are assigned to which virtual network, used to prevent
overlapping address space between networks that might later need to peer
or connect over VPN. Introduced in Chapter 04.

**Cloud security posture management (CSPM)** — The continuous practice of
evaluating deployed cloud configuration against a defined security
benchmark and surfacing drift, distinct from a point-in-time audit.
Introduced in Chapter 08.

**Commitment coverage** — The percentage of actual eligible cloud usage
covered by an active reserved or committed-use discount instrument, as
distinct from utilization. Introduced in Chapter 08.

**Commitment utilization** — The percentage of a purchased commitment's
capacity that is actually being consumed; low utilization means paying
for committed capacity that goes unused. Introduced in Chapter 08.

**Composite availability** — The actual end-to-end availability of a
multi-tier system, computed by multiplying component availabilities in
series or combining redundant components in parallel, which differs from
and is often lower than any single component's published SLA.
Introduced in Chapter 01.

**Control plane** — The APIs and services used to create, modify, and
delete cloud resources, as distinct from the data plane that carries
application traffic once a resource exists. Introduced in Chapter 01.

**Customer-managed key (CMK)** — An encryption key generated through a
provider's key management service under customer control of policy,
rotation, and deletion, chosen for regulatory requirements around key
ownership and audit. Introduced in Chapter 03.

**Data plane** — The component of a cloud service that carries
application traffic or serves application data once a resource exists, as
distinct from the control plane that manages the resource's lifecycle.
Introduced in Chapter 01.

**Detective guardrail** — A control that evaluates resources after
creation and reports or remediates noncompliance, trading a window of
noncompliance for broader, lower-friction rollout than a preventive
control. Introduced in Chapter 02.

**Drift** — Any divergence between the infrastructure-as-code-defined
desired state and the actual deployed state, caused by a manual change, an
out-of-band API call, or a provider-side default change. Introduced in
Chapter 09.

**Edge computing** — Compute and storage placed close to the data source
or end user to reduce latency or satisfy local data-processing
requirements, typically managed through the same control plane as
regional infrastructure but designed for autonomous operation during
connectivity loss. Introduced in Chapter 07.

**FaaS (Function as a Service)** — A service model in which the provider
operates everything except the function code and its trigger wiring.
Introduced in Chapter 01.

**FinOps** — The cross-functional operating discipline (Inform, Optimize,
Operate) that brings financial accountability to consumption-based cloud
spending. Introduced in Chapter 08.

**Golden image** — A validated, version-controlled machine image used to
launch or replace compute instances, central to the immutable-
infrastructure pattern of replacing rather than patching running
instances. Introduced in Chapter 05.

**Hub-and-spoke topology** — A network topology in which a central hub
virtual network holds shared services and each spoke peers directly to
the hub only, scaling linearly with spoke count instead of the
quadratic growth of a full peering mesh. Introduced in Chapter 04.

**IaaS (Infrastructure as a Service)** — A service model in which the
provider operates physical hosts, the hypervisor, and network/storage
fabric, while the customer operates the OS, runtime, and application.
Introduced in Chapter 01.

**Immutable infrastructure** — A pattern that treats running compute
instances as disposable, replacing them via a new golden image rather
than patching or reconfiguring them in place, eliminating configuration
drift. Introduced in Chapter 05.

**Landing zone** — The pre-provisioned, governed environment a workload
lands into, comprising resource hierarchy, identity and network
foundations, guardrails, logging, and a repeatable vending process.
Introduced in Chapter 02.

**Least privilege** — The principle that an identity holds exactly the
permissions its current task requires, for exactly as long as the task
requires them, applied as a continuous discipline rather than a one-time
grant decision. Introduced in Chapter 03.

**Multicloud** — The deliberate or incidental operation of production
workloads across more than one public cloud provider, distinct from mere
portability. Introduced in Chapter 01 and expanded in Chapter 07.

**Network access control list (NACL)** — A stateless, subnet-level
traffic filter evaluated in addition to any security group, used as a
coarse defense-in-depth backstop rather than the primary segmentation
control. Introduced in Chapter 04.

**Observability** — The property of being able to answer questions not
anticipated in advance by examining a system's emitted telemetry
(structured logs, traces, high-cardinality metrics), as distinct from
monitoring's pre-defined dashboards and alerts. Introduced in Chapter 09.

**Peering connection** — A direct, non-transitive routing relationship
between two virtual networks; connectivity does not extend to a third
network peered with either party. Introduced in Chapter 04.

**PaaS (Platform as a Service)** — A service model in which the provider
operates the OS, runtime, and often scaling, while the customer operates
application code, configuration, and data. Introduced in Chapter 01.

**Plan/apply separation** — The practice of using a read-only identity for
computing an infrastructure-as-code diff (plan) and a distinct, more
privileged identity for executing an approved change (apply), making
infrastructure changes reviewable before they take effect. Introduced in
Chapter 09.

**Point-in-time recovery** — A database or storage feature enabling
restoration to any specific timestamp within a retention window, rather
than only to the moment of a discrete snapshot. Introduced in Chapter 06.

**Policy as code** — The practice of expressing guardrails as versioned,
tested, pipeline-deployed code rather than manually configured console
settings, commonly implemented with the Open Policy Agent and `conftest`.
Introduced in Chapter 02.

**Preventive guardrail** — A control that blocks a noncompliant action
before it takes effect, providing the strongest guarantee but requiring
careful scoping to avoid blocking legitimate work. Introduced in
Chapter 02.

**Recovery Point Objective (RPO)** — The maximum acceptable amount of data
loss, measured as time, which drives the required backup or replication
frequency for a workload. Introduced in Chapter 06.

**Recovery Time Objective (RTO)** — The maximum acceptable time to restore
service after a failure, which drives the choice of recovery mechanism
(backup restore versus a warm or hot standby). Introduced in Chapter 06.

**Region** — A geographic area containing multiple isolated data centers,
chosen for data residency, latency, and disaster-recovery separation from
other regions. Introduced in Chapter 01.

**Reserved / committed-use capacity** — A purchasing option that commits to
a usage volume or specific configuration over a term in exchange for a
substantial discount relative to on-demand pricing, best matched to a
workload's well-understood steady-state baseline. Introduced in
Chapter 05.

**Responsive guardrail** — A control that triggers an automated action in
reaction to a detected event, closing the exposure window detective
controls leave open, provided the remediation action is safe and
well-tested. Introduced in Chapter 02.

**Right-sizing** — The continuous practice of matching compute instance
family and size to observed resource utilization, rather than a one-time
launch-time decision. Introduced in Chapter 05.

**Role-based access control (RBAC)** — An authorization model that bundles
permissions into named roles and grants identities membership in a role,
the standard default for most human and workload access. Introduced in
Chapter 03.

**SaaS (Software as a Service)** — A service model in which the provider
operates the entire application, and the customer operates configuration,
data, and user access. Introduced in Chapter 01.

**Shared responsibility model** — The division between what a cloud
provider secures (security of the cloud) and what the customer secures
(security in the cloud), with the exact boundary shifting by service
model. Introduced in Chapter 01.

**Showback** — Cost attribution made visible to the owning team without a
direct budget consequence, typically the appropriate starting point before
introducing chargeback. Introduced in Chapter 08.

**Spot / preemptible capacity** — A purchasing option consuming a
provider's spare capacity at a steep discount, reclaimable by the provider
on short notice, appropriate for fault-tolerant and interruptible
workloads. Introduced in Chapter 05.

**Transit gateway** — A managed, transitive routing hub that many virtual
networks and on-premises connections attach to once, gaining routed
connectivity to every other attachment, including spoke-to-spoke, without
a full peering mesh. Introduced in Chapter 04.

**Well-Architected pillar framework** — A provider-neutral set of design
review dimensions (operational excellence, security, reliability,
performance efficiency, cost optimization, sustainability) modeled on
providers' published Well-Architected frameworks. Introduced in
Chapter 01.

**Workload identity federation** — The pattern by which a CI/CD platform's
own OIDC issuer asserts identity directly to a cloud provider in exchange
for a short-lived, scoped credential, eliminating long-lived static cloud
access keys stored in pipeline secrets. Introduced in Chapter 03.
