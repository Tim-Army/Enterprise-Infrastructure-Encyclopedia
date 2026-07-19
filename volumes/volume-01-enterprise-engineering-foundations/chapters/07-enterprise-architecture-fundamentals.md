# Chapter 07: Enterprise Architecture Fundamentals

## Learning Objectives

- Explain what enterprise architecture is for, and distinguish it from
  solution architecture and infrastructure engineering.
- Compare the TOGAF Architecture Development Method and the Zachman
  Framework as complementary, not competing, tools.
- Describe the Business, Data, Application, and Technology (BDAT) domains
  and produce a capability map that spans them.
- Write and govern Architecture Decision Records (ADRs) as the lightweight,
  durable output of architectural reasoning.
- Design an architecture governance process — review board, technology
  radar, and ADR log — sized appropriately to an organization's maturity.

## Theory and Architecture

Enterprise architecture (EA) is the discipline of deliberately aligning an
organization's business strategy, information, applications, and
technology so that infrastructure investment serves business outcomes
rather than accumulating as an unplanned byproduct of individual project
decisions. [Chapter 06](06-understanding-enterprise-infrastructure.md) established what enterprise infrastructure is; this
chapter establishes the discipline that decides which infrastructure gets
built, in what order, and why — the layer above individual technology
choices where those choices are supposed to add up to something coherent.

EA sits at a specific altitude between two neighboring disciplines, and
confusing the three is the most common cause of a failed architecture
practice:

- **Enterprise architecture** reasons across the whole organization, over a
  multi-year horizon, about capability, standardization, and technical
  direction.
- **Solution architecture** reasons about a single system or project,
  applying the enterprise architecture's standards and constraints to a
  concrete design.
- **Infrastructure engineering** — the subject of most of this
  encyclopedia — implements the solution architecture's design as running,
  operated systems.

An enterprise architecture practice that produces diagrams no solution
architect ever consults, or that has no visibility into what infrastructure
engineering actually deploys, has failed regardless of how thorough its
documentation is. The remainder of this chapter treats governance
mechanisms — the review board, the ADR log, the technology radar — as the
connective tissue that keeps these three altitudes synchronized.

### Framework landscape

No single framework is mandatory, and most mature EA practices combine
elements of more than one. Three frameworks recur across the industry:

| Framework | Core idea | Primary output |
| --- | --- | --- |
| TOGAF (The Open Group Architecture Framework) | A repeatable process — the Architecture Development Method (ADM) — for producing and governing architecture | A cycle of phases producing vision, business, information systems, and technology architectures |
| Zachman Framework | A classification schema, not a process: six interrogatives (What, How, Where, Who, When, Why) crossed with perspectives from planner through operating enterprise | A matrix ensuring no perspective on a system is silently omitted |
| COBIT | An IT governance and management framework focused on control objectives and risk | Governance structures and control mappings, often used alongside TOGAF rather than instead of it |

TOGAF and Zachman answer different questions and are frequently used
together: Zachman asks "have we considered this system from every relevant
perspective," while TOGAF asks "what is the repeatable process by which we
produce and evolve architecture." COBIT overlays governance and control
concerns — who is accountable, what must be audited — on top of either.
Security architecture has its own dedicated framework lineage (SABSA is
the most cited), which [Volume X](../../volume-10-enterprise-cybersecurity/README.md) treats in the context of security
architecture specifically; this chapter treats security as one of several
concerns that must be integrated into every architecture domain below, not
as a separate framework to adopt in parallel.

### The TOGAF Architecture Development Method

The ADM is a cyclical, iterative sequence of phases. Each phase produces a
defined artifact set and feeds the next:

1. **Preliminary Phase.** Establish the architecture capability itself —
   governance, principles, tooling — before any specific architecture work
   begins.
2. **Phase A — Architecture Vision.** Define scope, stakeholders, and the
   high-level vision for the work.
3. **Phase B — Business Architecture.** Model business capabilities,
   processes, and organizational structure.
4. **Phase C — Information Systems Architectures.** Split into Data
   Architecture (what information exists and how it flows) and Application
   Architecture (what systems exist and how they interact).
5. **Phase D — Technology Architecture.** Define the infrastructure
   platforms, standards, and patterns that will support the application
   and data architectures — the phase most directly relevant to this
   encyclopedia's remaining volumes.
6. **Phase E — Opportunities and Solutions.** Identify implementation
   projects and evaluate build-vs-buy options.
7. **Phase F — Migration Planning.** Sequence the work, accounting for
   dependency and risk.
8. **Phase G — Implementation Governance.** Ensure delivered projects
   actually conform to the architecture that was approved.
9. **Phase H — Architecture Change Management.** Monitor for changes in
   technology or business context that require the cycle to run again.

**Requirements Management** sits at the center of the cycle, feeding and
being fed by every phase — a requirement discovered during Phase D
(Technology Architecture) may force a revisit of Phase B (Business
Architecture), and the ADM is explicitly designed to accommodate that,
rather than treating each phase as a one-way gate.

### The Zachman Framework

Where the ADM is a process, Zachman is a classification matrix: six
interrogatives (What/data, How/function, Where/network, Who/people,
When/time, Why/motivation) crossed against six perspectives, from the
broad scope a planner sees down to the functioning enterprise itself. Its
value is not in filling every cell for every system — that is rarely
practical — but in using the matrix as a checklist to catch a perspective
an architecture effort silently skipped. A technology architecture that
thoroughly documents "How" (integration patterns) but has nothing recorded
for "Who" (which teams own operation) has a real gap the matrix makes
visible before it becomes an operational incident.

### The BDAT domains

Most EA practices, TOGAF-aligned or not, organize their artifacts around
four domains, commonly abbreviated BDAT:

| Domain | Question it answers | Example artifact |
| --- | --- | --- |
| Business | What capabilities does the organization need? | Capability map, value stream map |
| Data | What information exists, and who is authoritative for it? | Conceptual data model, data ownership matrix |
| Application | What systems implement which capabilities? | Application portfolio, integration diagram |
| Technology | What infrastructure and platforms support the applications? | Reference architecture, technology standards catalog |

A capability map — a hierarchical list of what the business does,
independent of which system or team currently does it — is the anchor
artifact that ties the other three domains together: applications exist to
implement capabilities, data exists because capabilities produce and
consume it, and technology exists to run the applications. Building a
capability map before a technology standards catalog is what prevents
technology standardization from becoming an exercise in its own right,
disconnected from business need.

### Architecture governance mechanisms

Three lightweight, durable mechanisms carry most of an EA practice's
day-to-day value, independent of how much of the full ADM an organization
adopts:

- **Architecture Decision Records (ADRs).** A short, immutable document
  capturing a single architectural decision, its context, and its
  consequences, written at the moment the decision is made rather than
  reconstructed later. The Michael Nygard format — Title, Status, Context,
  Decision, Consequences — is the de facto standard because it is short
  enough that engineers actually write it.
- **Architecture Review Board (ARB).** A recurring, cross-functional
  review of proposed significant changes against architecture principles
  and standards, before implementation begins rather than after. An ARB's
  authority should be scoped explicitly (which changes require review) so
  it does not become a bottleneck for routine work.
- **Technology radar.** A living catalog of technologies grouped into
  adoption rings — commonly Adopt, Trial, Assess, and Hold — that makes
  the organization's current technology stance explicit and revisable,
  instead of leaving "what are we allowed to use" as tribal knowledge.

These three mechanisms are deliberately lightweight compared to the full
ADM cycle, and an organization can adopt them productively without ever
running a formal TOGAF engagement — this is the on-ramp most enterprise
engineering teams actually use, and the one this chapter's lab builds.

## Design Considerations

- **Framework depth vs. bureaucracy.** A small platform engineering team
  adopting the full nine-phase ADM for every change will produce more
  process than architecture. Start with ADRs and a lightweight ARB;
  adopt more of TOGAF's formal artifact set only when the organization's
  scale and audit requirements demand the additional rigor.
- **Who has authority to make a decision an ADR merely records.** An ADR
  documents a decision; it does not itself grant decision-making authority.
  Define explicitly which roles can author an ADR that binds a team's
  technology direction versus which ADRs are informational records of a
  smaller-scoped choice.
- **Centralized vs. federated architecture ownership.** A single central
  EA team preserves consistency but can become a bottleneck and lose
  context on domain-specific nuance; a federated model (domain architects
  embedded in each platform team, coordinated by a smaller central
  function) scales better but requires strong shared principles and a
  genuinely used ADR log to stay coherent. Most enterprises converge on
  the federated model as they grow past a single architecture team's
  attention span.
- **Technology radar governance cadence.** A radar reviewed too rarely
  becomes stale and loses credibility (teams route around it); reviewed
  too often, it churns and undermines the stability it exists to provide.
  A quarterly review cadence, with an explicit lightweight process for
  urgent additions, is a common balance point.
- **Architecture debt is real debt.** A decision that was correct when the
  ADR was written can become wrong as the business or technology landscape
  shifts. Track superseded ADRs explicitly (a `Superseded` status pointing
  to the replacing ADR) rather than deleting or silently ignoring outdated
  decisions — the historical record of *why* a now-wrong decision was
  right at the time is exactly what prevents repeating the same mistake
  under new pressure.
- **Integrating security architecture from the start, not as a gate at the
  end.** A reference architecture reviewed for security only at
  implementation time forces expensive rework. Require a stated trust
  boundary and data-classification consideration in every ADR and
  reference architecture from Phase D onward, foreshadowing the
  security-architecture depth in [Volume X](../../volume-10-enterprise-cybersecurity/README.md).

## Implementation and Automation

### 1. An ADR template

```markdown
<!-- docs/adr/adr-template.md -->
# ADR-NNNN: {Short, imperative decision title}

## Status

Proposed | Accepted | Superseded by ADR-NNNN | Deprecated

## Context

What problem or forcing function led to this decision? What constraints
(technical, organizational, regulatory) applied?

## Decision

The decision, stated as a single clear sentence if possible.

## Consequences

What becomes easier, what becomes harder, and what follow-on work does
this decision create?
```

### 2. A worked example

```markdown
<!-- docs/adr/0007-adopt-oidc-federation-for-ci-cloud-access.md -->
# ADR-0007: Adopt OIDC federation for CI-to-cloud credential access

## Status

Accepted

## Context

CI pipelines currently authenticate to the cloud provider using static,
long-lived access keys stored as repository secrets, as described in
Chapter 03. A recent internal audit flagged these as a standing credential
exposure risk.

## Decision

All new CI-to-cloud integrations must use OpenID Connect (OIDC) federation
to assume a short-lived, workflow-scoped role instead of a static secret.
Existing pipelines using static keys are migrated on a defined schedule,
tracked as follow-on issues linked from this record.

## Consequences

CI credential exposure risk drops significantly because no long-lived
secret is stored. Pipelines require an initial one-time IAM role and trust
policy setup per repository, which is a new operational step platform
engineering must document and support.
```

### 3. Validating the ADR log

```bash
#!/usr/bin/env bash
# validate-adr-log.sh — enforce required sections and valid status values
set -euo pipefail
DIR="${1:-docs/adr}"
VALID_STATUSES='^(Proposed|Accepted|Deprecated|Superseded by ADR-[0-9]{4})$'
fail=0

for file in "$DIR"/[0-9]*.md; do
  [[ -e "$file" ]] || continue
  for section in "## Status" "## Context" "## Decision" "## Consequences"; do
    if ! grep -qF "$section" "$file"; then
      echo "MISSING SECTION '$section' in $file" >&2
      fail=1
    fi
  done

  status=$(awk '/^## Status/{getline; while ($0 ~ /^$/) getline; print; exit}' "$file")
  if ! [[ "$status" =~ $VALID_STATUSES ]]; then
    echo "INVALID STATUS '$status' in $file" >&2
    fail=1
  fi
done

exit "$fail"
```

### 4. A minimal technology radar as data

```json
{
  "updated": "2026-07",
  "entries": [
    { "name": "OIDC federation for CI cloud access", "ring": "adopt", "domain": "automation" },
    { "name": "Rootless container runtimes", "ring": "trial", "domain": "platform" },
    { "name": "Static long-lived cloud access keys", "ring": "hold", "domain": "automation" }
  ]
}
```

```bash
# List everything currently on Hold, so a proposed design can be checked against it
jq -r '.entries[] | select(.ring == "hold") | .name' technology-radar.json
```

### 5. Requiring an ADR reference in the pull request template

Extending [Chapter 04](04-github-project-and-workflow-management.md)'s pull request template with an architecture-linkage
field keeps significant technical decisions traceable from the change that
implements them back to the record of why:

```markdown
## Architecture

- [ ] This change implements an existing ADR: <!-- ADR-NNNN -->
- [ ] This change requires a new ADR (attach before requesting review)
- [ ] Not applicable — no architecturally significant decision involved
```

## Validation and Troubleshooting

- **ADR log exists but nobody reads it before deciding.** An ADR log that
  is written to but never consulted before a new decision produces
  contradictory decisions over time. Require a "prior art" check — a
  search of the ADR log — as an explicit step before opening a new ADR,
  and reference any related prior decision by number even when the new
  decision changes course.
- **Status field drifts from reality.** A decision that has been silently
  abandoned in practice but still shows `Accepted` in its ADR misleads
  anyone who reads it later. Treat updating an ADR's status as part of the
  same change that supersedes or deprecates the decision, enforced by the
  validator's status-pattern check above.
- **Zachman-style gaps surface late.** A reference architecture that never
  documented "Who" (operational ownership) typically surfaces the gap
  during an incident, when responders discover no team is clearly
  accountable. Use the Zachman interrogatives as a review checklist during
  the ARB process specifically to catch this before implementation, not
  after an outage.
- **Technology radar entries with no owner or review date.** A radar entry
  that never gets revisited becomes stale documentation rather than a
  living governance tool; require every entry to carry a last-reviewed
  date and treat entries past a defined staleness threshold as due for
  re-evaluation, not as permanently settled.
- **Central EA team becomes a bottleneck.** If proposals queue for weeks
  awaiting ARB review, the governance mechanism is working against
  delivery rather than for it. Scope ARB review explicitly to
  architecturally significant changes (new external dependencies, new
  data flows crossing a trust boundary, new infrastructure domains) and
  let routine work proceed without a review gate.

## Security and Best Practices

- Require every ADR and reference architecture to state its trust
  boundaries and data classification explicitly, even briefly — this is
  the cheapest point in the lifecycle to catch a design that would
  otherwise require expensive rework once [Volume X](../../volume-10-enterprise-cybersecurity/README.md)'s security review
  processes are applied downstream.
- Treat the technology radar's Hold ring as an enforceable control, not a
  suggestion: pair it with the same CI-based checks this volume has used
  elsewhere (Chapters 02 and 03) so a Hold-ringed dependency or pattern
  can be flagged automatically in a pull request, not caught only if a
  human remembers to check.
- Restrict who can mark an ADR `Accepted` to the roles with actual
  decision authority defined for that scope; anyone should be able to
  propose an ADR, but acceptance is a governance action and belongs behind
  the same review rigor as a production infrastructure change.
- Keep the ADR log itself under the same version control, review, and
  branch protection controls established in [Chapter 02](02-repository-architecture.md) — the integrity of
  the decision record matters as much as the integrity of the
  infrastructure it describes.
- Do not let architecture documentation become the only place a decision
  is enforced. An ADR stating "all CI-to-cloud access uses OIDC
  federation" has no teeth until it is backed by an actual technical
  control (for example, an organization policy blocking static
  credential creation); pair every significant ADR with a corresponding
  enforcement mechanism where one is feasible.

## References and Knowledge Checks

**References**

- The Open Group, *TOGAF Standard* — the Architecture Development Method
  in full detail.
- John Zachman, *The Zachman Framework for Enterprise Architecture* —
  origin of the classification matrix referenced in this chapter.
- Michael Nygard, *Documenting Architecture Decisions* — the ADR format
  this chapter's template follows.
- ISACA, *COBIT* — governance and control-objective framework referenced
  above.
- [templates/technical-review-checklist.md](../../../templates/technical-review-checklist.md)
  — this encyclopedia's own governance gate, a worked example of a
  lightweight review mechanism applied at document-publication scale.

**Knowledge checks**

1. What distinguishes enterprise architecture from solution architecture
   and from infrastructure engineering, and why does confusing the three
   commonly cause an architecture practice to fail?
2. Why are TOGAF's ADM and the Zachman Framework described as
   complementary rather than competing?
3. Name the four sections of the Nygard ADR format and explain why
   `Consequences` matters as much as `Decision`.
4. Give an example of when a federated architecture-ownership model scales
   better than a centralized one, and what it requires to stay coherent.

## Hands-On Lab

**Objective:** Stand up an ADR log with a validated template, record two
linked decisions (one superseding the other), and prove the validator
correctly rejects a malformed ADR before it would reach review.

**Prerequisites**

- `bash`, `awk`, and `jq` installed.
- A local Git repository (a new scratch repository is sufficient).

**Steps**

1. Create the ADR directory and template:

   ```bash
   mkdir -p ~/ea-lab/docs/adr ~/ea-lab/scripts
   cd ~/ea-lab
   git init -q
   cat > docs/adr/adr-template.md <<'EOF'
   # ADR-NNNN: {Short, imperative decision title}

   ## Status

   Proposed

   ## Context

   ## Decision

   ## Consequences
   EOF
   ```

2. Add the validator:

   ```bash
   cat > scripts/validate-adr-log.sh <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   DIR="${1:-docs/adr}"
   VALID_STATUSES='^(Proposed|Accepted|Deprecated|Superseded by ADR-[0-9]{4})$'
   fail=0
   for file in "$DIR"/[0-9]*.md; do
     [[ -e "$file" ]] || continue
     for section in "## Status" "## Context" "## Decision" "## Consequences"; do
       if ! grep -qF "$section" "$file"; then
         echo "MISSING SECTION '$section' in $file" >&2
         fail=1
       fi
     done
     status=$(awk '/^## Status/{getline; while ($0 ~ /^$/) getline; print; exit}' "$file")
     if ! [[ "$status" =~ $VALID_STATUSES ]]; then
       echo "INVALID STATUS '$status' in $file" >&2
       fail=1
     fi
   done
   exit "$fail"
   EOF
   chmod +x scripts/validate-adr-log.sh
   ```

3. Write the first ADR:

   ```bash
   cat > docs/adr/0001-standardize-on-monorepo-for-platform-tooling.md <<'EOF'
   # ADR-0001: Standardize on a monorepo for platform tooling

   ## Status

   Accepted

   ## Context

   Platform tooling is currently spread across twelve small repositories
   with duplicated CI configuration.

   ## Decision

   Consolidate platform tooling into a single monorepo with path-scoped CI.

   ## Consequences

   Cross-cutting changes become atomic. The migration requires updating
   twelve sets of CI credentials and access controls.
   EOF
   ```

4. Run the validator:

   ```bash
   ./scripts/validate-adr-log.sh docs/adr
   echo "Exit code: $?"
   ```

   **Expected result:** Exit code `0`, no error output.

5. Write a second ADR that supersedes the first, and update the first
   record's status:

   ```bash
   cat > docs/adr/0002-revert-to-polyrepo-for-platform-tooling.md <<'EOF'
   # ADR-0002: Revert to polyrepo for platform tooling

   ## Status

   Accepted

   ## Context

   The monorepo from ADR-0001 created a single point of CI failure that
   blocked unrelated teams during a recent incident.

   ## Decision

   Split platform tooling back into per-domain repositories with a shared,
   versioned CI workflow template instead of shared source.

   ## Consequences

   Restores team-level CI isolation. Reintroduces the coordination cost
   for genuinely cross-cutting changes that ADR-0001 was written to solve.
   EOF
   sed -i.bak 's/^Accepted$/Superseded by ADR-0002/' docs/adr/0001-standardize-on-monorepo-for-platform-tooling.md
   rm docs/adr/0001-standardize-on-monorepo-for-platform-tooling.md.bak
   ```

6. Re-run the validator:

   ```bash
   ./scripts/validate-adr-log.sh docs/adr
   echo "Exit code: $?"
   ```

   **Expected result:** Exit code `0` — both the `Superseded by ADR-0002`
   and `Accepted` status values match the validator's pattern.

7. **Negative test:** Add a malformed ADR missing a required section and
   using an invalid status value:

   ```bash
   cat > docs/adr/0003-broken-record.md <<'EOF'
   # ADR-0003: Broken record

   ## Status

   In Review

   ## Decision

   Something was decided.
   EOF
   ./scripts/validate-adr-log.sh docs/adr
   echo "Exit code: $?"
   ```

   **Expected result:** The validator reports `MISSING SECTION '##
   Context' in docs/adr/0003-broken-record.md`, `MISSING SECTION '##
   Consequences' in docs/adr/0003-broken-record.md`, and `INVALID STATUS
   'In Review' in docs/adr/0003-broken-record.md`, exiting non-zero —
   confirming both the section and status checks fire independently.

8. Remove the broken record and confirm recovery:

   ```bash
   rm docs/adr/0003-broken-record.md
   ./scripts/validate-adr-log.sh docs/adr
   echo "Exit code: $?"
   ```

   **Expected result:** Exit code `0` again.

9. **Cleanup:**

   ```bash
   cd ~ && rm -rf ~/ea-lab
   ```

## Summary and Completion Checklist

Enterprise architecture aligns business strategy with technology direction
across the whole organization, distinct from solution architecture's
single-project scope and infrastructure engineering's implementation
scope. TOGAF's Architecture Development Method and the Zachman Framework
are complementary: one is a repeatable process, the other a completeness
checklist. The BDAT domains organize architecture artifacts around
business capability first, so technology standardization stays anchored to
business need. Architecture Decision Records, a scoped Architecture Review
Board, and a living technology radar are the lightweight governance
mechanisms that make architecture decisions durable, traceable, and
enforceable without requiring a full formal framework adoption.

- [ ] Can distinguish enterprise architecture, solution architecture, and
      infrastructure engineering by scope and time horizon.
- [ ] Can explain how TOGAF's ADM and the Zachman Framework complement
      each other.
- [ ] Can write a complete ADR using the Nygard format, including a status
      that reflects reality.
- [ ] Can design a right-sized architecture governance process for a given
      organization's maturity.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
