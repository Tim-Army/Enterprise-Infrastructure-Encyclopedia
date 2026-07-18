# Volume IX Glossary

Definitions for terms introduced in **Volume IX — Infrastructure
Automation**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Agentless architecture** — An automation model, used by Ansible, in
which the control node connects to managed hosts over SSH or WinRM at run
time rather than relying on a persistent installed agent daemon.
Introduced in Chapter 03.

**`ansible-vault`** — Ansible's built-in tool for symmetrically encrypting
files or in-line values so encrypted content can be safely committed to
version control. Introduced in Chapter 06.

**AppRole** — A Vault authentication method designed for machine and
application clients, using a `role_id`/`secret_id` pair to authenticate
and receive a scoped, time-limited token. Introduced in Chapter 06.

**Backoff with jitter** — A retry strategy that increases the wait time
between attempts exponentially and randomizes it within a range, avoiding
synchronized retry storms from many callers failing at once. Introduced in
Chapter 04.

**Break-glass access** — A deliberately narrow, heavily audited exception
to normal just-in-time credential issuance, used only when the standard
issuance path is provably unavailable, and rotated immediately after use.
Introduced in Chapter 06.

**`check` block** — A Terraform 1.9.x language construct that asserts a
condition about infrastructure without failing the overall plan or apply,
surfacing a warning instead. Introduced in Chapter 02.

**CloudEvents** — A CNCF specification standardizing the envelope fields
(`id`, `source`, `type`, `time`) of an event, leaving the payload
provider-specific, used to give event-driven integrations a common
structure. Introduced in Chapter 04.

**Compensating action** — In the saga pattern, an explicit step that
undoes a prior workflow step's side effect, run when a later step in the
same workflow fails. Introduced in Chapter 07.

**Conftest** — A CLI tool that evaluates structured data (commonly
Terraform plan JSON) against Open Policy Agent Rego policies, used as an
automated, blocking pipeline gate. Introduced in Chapter 05.

**`cosign`** — A Sigstore tool for signing and verifying software
artifacts, supporting keyless signing that uses a CI platform's OIDC
identity instead of a stored private key. Introduced in Chapter 08.

**Dynamic secret** — A credential a secrets engine (such as Vault's
database secrets engine) generates on demand for a specific request and
automatically revokes at expiry, rather than handing out a shared static
value. Introduced in Chapter 06.

**Drift frequency** — A reliability indicator measuring how often a
scheduled `terraform plan` detects unmanaged changes to infrastructure,
used as a signal of governance gaps outside the pipeline. Introduced in
Chapter 09.

**Event-Driven Ansible (EDA)** — An Ansible ecosystem framework
(`ansible-rulebook`) that reacts to events from a configured source with
declarative rules, running a playbook or module when a rule's condition
matches. Introduced in Chapter 07.

**Execution environment** — A container image packaging `ansible-core`,
required collections, and their Python dependencies into a reproducible,
versioned runtime, built with `ansible-builder`. Introduced in Chapter 03.

**Idempotency key** — A unique identifier attached to a request or event
that a receiver records and checks before acting, so a duplicate delivery
becomes a no-op instead of a duplicate action. Introduced in Chapter 04.

**`import` block** — A Terraform 1.5+ declarative construct that brings an
existing, unmanaged resource under Terraform management as part of a
reviewed plan/apply cycle, replacing the older imperative `terraform
import` CLI command. Introduced in Chapter 02.

**Keyless signing** — A Sigstore signing model in which a CI job's own
OIDC identity, rather than a stored private key, is used to sign an
artifact, with the signature recorded in a public transparency log.
Introduced in Chapter 08.

**Mean time to recovery (MTTR), automation-specific** — The elapsed time
from an automation pipeline or control-plane failure to a passing re-run,
used as a reliability indicator for the automation system itself rather
than for the infrastructure it manages. Introduced in Chapter 09.

**`moved` block** — A Terraform 1.9.x language construct that records a
resource address change declaratively, so Terraform applies a rename or
refactor in place instead of destroying and recreating the resource.
Introduced in Chapter 02.

**Molecule** — A testing framework that drives an Ansible role through
create, converge, idempotence, verify, and destroy stages inside a
disposable container, automating the "runs cleanly twice" idempotency
check. Introduced in Chapter 03.

**OIDC federation** — OpenID Connect used by a CI pipeline to exchange a
signed, short-lived, workflow-scoped identity token for temporary cloud or
Vault credentials, eliminating the need for a stored long-lived secret.
Introduced in Chapter 06 (first referenced in Chapter 02).

**Pipeline success rate** — A reliability indicator measuring the
percentage of pipeline runs that complete without failure over a rolling
window, used to detect systemic automation problems rather than isolated
bad changes. Introduced in Chapter 09.

**Plan/apply credential separation** — The practice of using distinct,
differently scoped identities for a pipeline's read-only plan stage and
its write-capable apply stage, so a compromised or buggy plan stage cannot
itself make changes. Introduced in Chapter 05 and detailed in Chapter 06.

**Policy as code** — Expressing organizational rules (security baselines,
tagging standards, risk classification) as version-controlled,
automatically evaluated code rather than a checklist a human reviewer must
remember to apply. Introduced in Chapter 05.

**Provider (Terraform)** — A plugin, versioned independently of Terraform
core, that translates HCL resource blocks into calls against a specific
API. Introduced in Chapter 02.

**Provider mirror** — A network- or filesystem-based redirection of
Terraform provider resolution away from the public registry, used to
enforce a private, organization-controlled dependency trust boundary.
Introduced in Chapter 08.

**Rego** — The policy language used by Open Policy Agent and Conftest to
express `deny` and `allow` rules evaluated against structured input such
as a Terraform plan's JSON representation. Introduced in Chapter 05.

**Renovate** — An automated dependency-update tool that opens a reviewable
pull request for each eligible version bump (Terraform providers, Ansible
collections) instead of silently resolving a floating version constraint.
Introduced in Chapter 08.

**Replay protection** — A webhook receiver control that rejects or
deduplicates events outside an acceptable time window or already seen by
identifier, preventing a captured request from being resubmitted to
re-trigger automation. Introduced in Chapter 04.

**SBOM (software bill of materials)** — A structured, machine-readable
inventory of every dependency a piece of software or an automation
repository pulls in, used to match a newly disclosed vulnerability against
actual exposure quickly. Introduced in Chapter 08.

**Saga pattern** — A workflow design pattern that pairs every step with a
side effect to an explicit compensating action, run in reverse order from
the point of failure, to recover cleanly from a partially completed
multi-step operation. Introduced in Chapter 07.

**Secret zero** — The initial credential that bootstraps trust in any
secrets-issuance chain, which cannot itself be dynamically issued;
minimizing what secret zero actually is (a cryptographic trust
relationship instead of a stored value) is the goal of OIDC federation.
Introduced in Chapter 06.

**SLSA (Supply-chain Levels for Software Artifacts)** — An OpenSSF
framework defining increasing levels of build and provenance integrity,
applied in this volume as a maturity model for infrastructure pipelines.
Introduced in Chapter 08.

**State locking** — A Terraform backend feature that prevents concurrent
`apply` operations from corrupting each other's writes by blocking or
failing a second run until the first releases its lock. Introduced in
Chapter 02.

**Static service identity** — A dedicated non-human account with
credentials that do not expire on their own, contrasted with federated,
short-lived workload identity. Introduced in Chapter 06.

**Structured logging** — Emitting log output as machine-parseable records
(commonly JSON Lines) with consistent fields, rather than free-text
console output, so automation run history is queryable rather than only
readable. Introduced in Chapter 09.

**Terraform lock file (`.terraform.lock.hcl`)** — A generated file
recording the exact resolved provider versions and their cryptographic
hashes for a configuration, committed to version control as a supply-chain
control. Introduced in Chapter 02 and extended in Chapter 08.

**Test pyramid (infrastructure)** — A layered testing model — static
analysis, unit, integration, end-to-end — applied to infrastructure code,
weighted toward fast, cheap lower layers over slow, expensive end-to-end
validation. Introduced in Chapter 05.

**Time-to-apply** — A reliability indicator measuring elapsed time from a
merged change to a completed, approved apply, used as a proxy for pipeline
friction. Introduced in Chapter 09.

**Variable precedence (Ansible)** — The defined order in which Ansible
resolves a variable name from multiple possible sources (role defaults,
inventory, play vars, extra vars), from lowest to highest priority.
Introduced in Chapter 03.

**Vault (HashiCorp)** — A secrets management platform providing
centralized storage, access policy, dynamic secret issuance, and audit
logging for credentials automation systems need at run time. Introduced in
Chapter 06.

**Webhook** — An HTTP callback a remote system invokes to notify a
receiver of an event in near real time, the push counterpart to polling.
Introduced in Chapter 04.

**Workflow orchestration** — Sequencing multiple, often heterogeneous
automation steps — playbooks, API calls, pipeline triggers, human
approvals — into a single coherent, auditable operation, distinct from a
single configuration-management run or a single pipeline. Introduced in
Chapter 07.
