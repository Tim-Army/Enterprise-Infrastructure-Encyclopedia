# Volume I Glossary

Definitions for terms introduced in **Volume I — Enterprise Engineering
Foundations**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Architecture Decision Record (ADR)** — A short, immutable document
recording a single architectural decision, its context, and its
consequences, written using the Nygard format (Status, Context, Decision,
Consequences). Introduced in Chapter 07.

**Architecture Development Method (ADM)** — TOGAF's cyclical, iterative
process for producing and governing architecture, running from a
Preliminary Phase through Phases A–H with Requirements Management at its
center. Introduced in Chapter 07.

**Architecture Review Board (ARB)** — A recurring, cross-functional review
body that evaluates proposed significant technical changes against
architecture principles and standards before implementation begins.
Introduced in Chapter 07.

**BDAT domains** — The four domains most enterprise architecture practices
organize artifacts around: Business, Data, Application, and Technology.
Introduced in Chapter 07.

**Bootstrap script** — An idempotent script that provisions a workstation
or environment from a clean state, doubling as its own drift check when
re-run. Introduced in Chapter 01.

**Branch protection** — Git hosting platform rules that enforce required
status checks, required reviews, and linear history before a change can
reach a protected branch. Introduced in Chapter 02.

**Capability map** — A hierarchical list of what a business does,
independent of which system or team currently performs it, used to anchor
the BDAT domains to actual business need. Introduced in Chapter 07.

**CAB (Change Advisory Board)** — The group responsible for reviewing and
approving "Normal" risk-category changes before they proceed to a
scheduled change window. Introduced in Chapter 08.

**Change management** — The discipline governing how modifications to
production infrastructure are proposed, assessed, approved, and recorded,
typically classified into standard, normal, and emergency risk categories.
Introduced in Chapter 08.

**CMDB (Configuration Management Database)** — A system tracking
Configuration Items (CIs) — what an asset is, how it is configured, and
what depends on it — distinct from IT Asset Management's financial and
contractual focus. Introduced in Chapter 08.

**CODEOWNERS** — A repository file mapping paths to required reviewers,
declaring review responsibility in-repository rather than relying on
tribal knowledge. Introduced in Chapter 02.

**COBIT** — An IT governance and management framework focused on control
objectives and risk, commonly layered alongside TOGAF rather than used as
a replacement for it. Introduced in Chapter 07.

**Consumption model** — The categorization of infrastructure by who owns
and operates the underlying stack: on-premises, colocation, private cloud,
public cloud, hybrid, or edge. Introduced in Chapter 06.

**Conventional Commits** — A commit message convention that turns commit
history into machine-parseable metadata, enabling automated changelog
generation and semantic versioning. Introduced in Chapter 02.

**Criticality tier** — A deliberately assigned rating of an infrastructure
domain's or asset's importance to the business, used to calibrate
oversight and availability investment. Introduced in Chapter 06.

**Declarative automation** — Automation that describes a desired end
state, reconciled by a tool (Terraform, Ansible, Kubernetes manifests),
making changes reviewable as a diff before they are applied. Introduced in
Chapter 03.

**Decommissioning** — The lifecycle stage in which an asset is removed
from service, its data sanitized or destroyed, and its records closed out
across every system that referenced it. Introduced in Chapter 08.

**Docs-as-code** — The practice of treating written content the way
software teams treat code: plain-text source under version control,
validated by automated checks, and transformed by a repeatable build.
Introduced in Chapter 05.

**Domain inventory** — A version-controlled, validated record naming every
infrastructure domain in use, its owner, consumption model, and
criticality tier. Introduced in Chapter 06.

**Emergency change** — A change addressing an active incident or imminent
risk, approved through an expedited path with mandatory retrospective
review. Introduced in Chapter 08.

**Enterprise architecture (EA)** — The discipline of aligning business
strategy, information, applications, and technology across an entire
organization, distinct from solution architecture's single-project scope.
Introduced in Chapter 07.

**Enterprise infrastructure** — The shared compute, network, storage,
platform, identity, and security capabilities an organization operates as
a managed foundation for dependent applications, distinguished from
smaller-scale IT by scale, shared risk, regulatory obligation, and formal
accountability. Introduced in Chapter 06.

**EOL / EOS (End-of-Life / End-of-Support)** — The dates beyond which a
vendor stops shipping updates or security fixes for a product, tracked to
trigger refresh or upgrade projects with adequate lead time. Introduced in
Chapter 08.

**Error budget** — The amount of unreliability a Service Level Objective
permits over a period, treated as a resource a team can deliberately spend
on risk rather than minimize to zero. Introduced in Chapter 06.

**Idempotency** — The property that running an operation multiple times
produces the same end state as running it once, which is what allows
automation to be re-run safely after a partial failure. Introduced in
Chapter 01 and formalized in Chapter 03.

**ITAM (IT Asset Management)** — The practice of tracking the financial
and contractual lifecycle of an asset: purchase cost, warranty, license
entitlement, depreciation, and disposal value. Introduced in Chapter 08.

**ITIL 4 service value chain** — Six activities (Plan, Improve, Engage,
Design and transition, Obtain/build, Deliver and support) that can combine
in different orders to describe how a service organization creates value,
replacing the older linear ITIL service lifecycle model. Introduced in
Chapter 08.

**Merge queue** — A mechanism that serializes pull requests and
re-validates each against the current default branch immediately before
merging, catching integration failures that direct required review alone
cannot. Introduced in Chapter 04.

**Monorepo** — A repository topology holding all or most related code or
content in a single repository, trading larger blast radius for atomic
cross-cutting changes. Introduced in Chapter 02.

**NIST SP 800-88** — The NIST Special Publication defining Clear, Purge,
and Destroy media sanitization categories used to guide secure
decommissioning decisions. Introduced in Chapter 08.

**OIDC federation** — OpenID Connect used by a CI pipeline to exchange a
short-lived, workflow-scoped identity token for cloud credentials that
expire in minutes, eliminating the need for a stored long-lived secret.
Introduced in Chapter 03.

**Plan/apply separation** — The practice of using a distinct, more
privileged identity for the "apply" stage of an infrastructure pipeline
than for the read-only "plan" stage, gating write access behind human
approval. Introduced in Chapter 03.

**Polyrepo** — A repository topology using one repository per service,
library, or content domain, trading coordination cost for clear ownership
boundaries and independent access control. Introduced in Chapter 02.

**Reference architecture** — A reusable architectural pattern documenting
how a class of systems should be built, produced primarily during TOGAF's
Technology Architecture phase. Introduced in Chapter 07.

**Request for Change (RFC)** — The record that carries a proposed
infrastructure change through the change management process: what will
change, why, the rollback plan, and the change window. Introduced in
Chapter 08.

**SABSA** — A dedicated security architecture framework, distinct from
general enterprise architecture frameworks, treated in depth in Volume X.
Introduced in Chapter 07.

**Service Level Agreement (SLA)** — An externally facing, often
contractual, availability or performance commitment with defined
consequences for non-compliance. Introduced in Chapter 06.

**Service Level Indicator (SLI)** — The actual measured metric (for
example, successful request ratio or latency percentile) used to evaluate
a Service Level Objective. Introduced in Chapter 06.

**Service Level Objective (SLO)** — An internal reliability target,
usually stricter than the SLA, that a team designs and operates toward.
Introduced in Chapter 06.

**Standard change** — A pre-approved, low-risk, repeatable change executed
against a tested runbook without case-by-case approval. Introduced in
Chapter 08.

**Structural validation** — Automated checks confirming required files,
sequential numbering, and cross-references between a manifest and files on
disk, run before more expensive validation and build steps. Introduced in
Chapter 02.

**Technology radar** — A living catalog of technologies grouped into
adoption rings (commonly Adopt, Trial, Assess, Hold) that makes an
organization's current technology stance explicit and revisable.
Introduced in Chapter 07.

**TOGAF (The Open Group Architecture Framework)** — An enterprise
architecture framework centered on the Architecture Development Method, a
repeatable process for producing and governing architecture. Introduced in
Chapter 07.

**Version manager** — A tool (such as `mise`) that reads a version file
committed to a repository and activates the correct language or tool
runtime automatically, removing an entire class of "wrong version"
defects. Introduced in Chapter 01.

**Zachman Framework** — A classification matrix crossing six
interrogatives (What, How, Where, Who, When, Why) against perspectives
from planner to functioning enterprise, used as a completeness checklist
rather than a process. Introduced in Chapter 07.
