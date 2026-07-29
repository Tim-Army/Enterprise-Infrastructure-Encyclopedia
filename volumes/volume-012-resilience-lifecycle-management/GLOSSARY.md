# Volume XII Glossary

Definitions for terms introduced in **Volume XII — Resilience and
Lifecycle Management**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter section each
term is drawn from, and the [master glossary](../../GLOSSARY.md) for
cross-volume terminology.

**3-2-1-1-0 Rule** — A backup design rule requiring 3 copies of data on
2 different media types, with 1 copy off-site, 1 copy offline or
immutable, and 0 verification errors on restore testing. Introduced in
Chapter 04.

**6 Rs of Modernization** — Six strategies (retain, retire, rehost,
replatform, refactor/rearchitect, repurchase) for responding to a
system's technical debt or end-of-life status. Introduced in Chapter 07.

**Active-active topology** — An HA topology in which two or more
instances serve traffic simultaneously, so the failure of any one
instance is absorbed by remaining capacity with no promotion step.
Introduced in Chapter 03.

**Active-passive topology** — An HA topology in which one instance
serves traffic while a standby remains ready to take over on failure,
introducing a nonzero failover time. Introduced in Chapter 03.

**Bake time** — The observation period a staged rollout stage must
complete, healthy, before promotion to the next stage is permitted.
Introduced in Chapter 06.

**BCP (Business Continuity Plan)** — An organization-wide plan covering
people, facilities, suppliers, and processes needed to keep the business
operating through a disruption, broader in scope than IT-specific
disaster recovery. Introduced in Chapter 02.

**Blast radius** — The set of users, transactions, or downstream
services affected when a failure domain fails completely. Introduced in
Chapter 01.

**Blue-green deployment** — A staged rollout strategy in which a
complete parallel environment is provisioned with the new version and
traffic is cut over only after validation, with the prior environment
retained briefly for instant rollback. Introduced in Chapter 06.

**Bulkhead** — A fault-tolerance primitive that isolates resource pools
(threads, connections, queue capacity) per dependency so a saturated
dependency cannot exhaust resources needed to serve calls to healthy
dependencies. Introduced in Chapter 03.

**Canary rollout** — A staged rollout strategy in which a change is
applied to a small subset of a fleet first and promoted to the full
fleet only if it remains healthy against defined success metrics.
Introduced in Chapter 06.

**Carbon payback period** — The time required for a replacement asset's
operational carbon savings to offset the embodied carbon discarded by
retiring the asset it replaces. Introduced in Chapter 08.

**Chaos engineering** — The discipline of running controlled experiments
against a system, guided by a steady-state hypothesis and a bounded
blast radius, to build confidence in its resilience to real-world
turbulent conditions. Introduced in Chapter 05.

**Circuit breaker** — A fault-tolerance primitive that stops sending
requests to a failing dependency after a failure-rate threshold is
crossed, failing fast instead of waiting for calls to time out.
Introduced in Chapter 03.

**Circular hardware lifecycle** — A hardware lifecycle model (reduce,
reuse, refurbish, recycle) that extends useful asset life in stages
before final disposal, in contrast to a linear buy-use-discard model.
Introduced in Chapter 08.

**Clear** — The lowest-assurance NIST SP 800-88 media sanitization
category, using logical overwrite techniques, appropriate for media
being reused within the same security domain. Introduced in Chapter 09.

**COOP (Continuity of Operations Plan)** — A continuity plan type, most
common in government and public-sector contexts, focused on maintaining
essential functions and lines of succession during a significant
disruption. Introduced in Chapter 02.

**Criticality tier** — A deliberately assigned rating (commonly Tier
0–4) of a service's importance to the business, used to calibrate
resilience, testing, and maintenance investment. Introduced in Chapter
01.

**Decommissioning** — The governed process of retiring a system:
verifying it is safe to remove, sanitizing or destroying its data, and
closing every record that referenced it. Introduced in Chapter 09.

**Dependency graph** — A directed graph of service-to-service
dependencies used to identify single points of failure and, later in the
lifecycle, to verify a system has no remaining dependents before
decommissioning. Introduced in Chapter 01; extended in Chapter 09.

**Destroy** — The highest-assurance NIST SP 800-88 media sanitization
category, using physical destruction to render media itself unusable.
Introduced in Chapter 09.

**DRP (Disaster Recovery Plan)** — The IT-specific continuity plan
subset that restores technology infrastructure and data, most directly
implemented by the backup and DR patterns in Chapter 04. Introduced in
Chapter 02.

**Embodied carbon** — The emissions associated with manufacturing,
transporting, and eventually disposing of equipment, incurred largely
independent of how the equipment is subsequently used. Introduced in
Chapter 08.

**Exercise maturity ladder** — The progression of continuity and DR
exercise types (tabletop, walkthrough, simulation, parallel test, full
interruption test) increasing in realism, cost, and risk. Introduced in
Chapter 05.

**Failure domain** — The boundary within which a single fault can
propagate without crossing into another domain. Introduced in Chapter
01.

**Game day** — A scheduled, facilitated exercise combining fault
injection with active human response, run against a single, clearly
stated hypothesis about a specific failure mode. Introduced in Chapter
05.

**Graceful degradation** — Designing a service to deliver reduced
functionality under stress rather than failing entirely, through
techniques such as load shedding and feature-flag-driven fallback.
Introduced in Chapter 03.

**Grandfather-Father-Son (GFS)** — A tiered backup retention rotation
scheme (daily, weekly, monthly) balancing recovery flexibility against
storage cost. Introduced in Chapter 04.

**Hot site** — A DR site strategy in which the DR location runs at full
production capacity continuously, delivering an RTO approaching zero.
Introduced in Chapter 04.

**Impact escalation curve** — A plot of business impact score against
elapsed outage time, used to derive a defensible Maximum Tolerable
Downtime rather than an arbitrary figure. Introduced in Chapter 02.

**MTBF (Mean Time Between Failures)** — The average operating time
between failures of a repairable component, used with MTTR to calculate
component and system availability. Introduced in Chapter 01.

**MTD (Maximum Tolerable Downtime)** — The absolute, business-defined
ceiling beyond which an organization suffers unacceptable or
unrecoverable harm from an outage. Introduced in Chapter 02.

**MTTR (Mean Time To Repair/Recover)** — The average time to restore a
failed component to service. Introduced in Chapter 01.

**N+1 redundancy** — A redundancy notation describing N units required
to carry full load plus 1 spare unit, tolerating the loss of one unit
without capacity loss. Introduced in Chapter 01.

**Operational carbon** — The emissions associated with the electricity
consumed while equipment runs, varying with the carbon intensity of the
electricity source. Introduced in Chapter 08.

**Patch severity classification** — A scheme (critical, high, moderate,
low) mapping a patch's risk to a remediation SLA. Introduced in Chapter
06.

**Pilot light** — A DR site strategy in which a minimal core, typically
the data tier, is kept continuously replicated at the DR location while
compute is provisioned only during a declared disaster. Introduced in
Chapter 04.

**Purge** — A NIST SP 800-88 media sanitization category using physical
or logical techniques (such as cryptographic erase) that render data
infeasible to recover even with advanced laboratory techniques.
Introduced in Chapter 09.

**PUE (Power Usage Effectiveness)** — The ratio of total facility energy
to IT equipment energy, a widely used but incomplete data center
efficiency metric. Introduced in Chapter 08.

**Quorum** — A requirement that a strict majority of cluster members
agree before accepting a write or promoting a new leader, the standard
defense against split-brain. Introduced in Chapter 03.

**Reversibility window** — A deliberate, bounded period during which a
system being decommissioned is disabled but recoverable before
sanitization becomes irreversible. Introduced in Chapter 09.

**Right-sizing** — Matching provisioned infrastructure capacity to
observed demand, reducing both cost and energy consumption while
excluding deliberate HA/DR redundancy headroom from being treated as
waste. Introduced in Chapter 08.

**Rolling deployment** — A staged rollout strategy in which instances
are updated in sequential, validated batches, keeping a bounded fraction
of capacity offline at any time. Introduced in Chapter 06.

**RPO (Recovery Point Objective)** — The maximum acceptable amount of
data loss, measured as time, driving replication and backup frequency
decisions. Introduced in Chapter 02.

**RTO (Recovery Time Objective)** — The maximum acceptable time between
an outage starting and a process being restored to an operating state.
Introduced in Chapter 02.

**Split-brain** — A condition where a network partition causes two
sides of a cluster to independently believe they are the primary and
both accept writes, producing divergent, unreconcilable state.
Introduced in Chapter 03.

**SPOF (Single Point of Failure)** — Any component whose failure removes
service capability with no automatic compensating path. Introduced in
Chapter 01.

**Steady-state hypothesis** — A measurable definition of normal system
behavior established before a chaos experiment, against which a
deviation can be objectively detected. Introduced in Chapter 05.

**Strangler fig pattern** — An incremental migration pattern in which a
routing layer progressively redirects functionality from a legacy
system to a new implementation until the legacy system can be retired.
Introduced in Chapter 07.

**Technical debt** — The implied future cost of choosing an expedient
solution now over a more thorough one, classified by whether it was
taken on deliberately or inadvertently, and recklessly or prudently.
Introduced in Chapter 07.

**Warm standby** — A DR site strategy in which a scaled-down but fully
functional copy of production runs continuously at the DR location,
ready to scale up on failover. Introduced in Chapter 04.

**WRT (Work Recovery Time)** — The time needed after systems are
technically restored before a business process is fully caught up, such
as reprocessing a backlog or reconciling data. Introduced in Chapter 02.

**Zombie system** — A system that should have been retired but continues
running indefinitely, accumulating unpatchable version debt and unused
redundancy and monitoring investment while delivering no business value.
Introduced in Chapter 09.
