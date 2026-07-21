# Chapter 08: Infrastructure Lifecycle Management

![Lab flow for this chapter: a CMDB asset record moves through its legal lifecycle states from planned through decommissioned, with every transition checked against a table of legal state pairs before the record is modified; an attempt to bring a decommissioned asset back into service is rejected without corrupting the record.](../../../diagrams/volume-01-enterprise-engineering-foundations/chapter-08-cmdb-lifecycle-state-machine-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: the CMDB lifecycle state machine driving an asset from planned to decommissioned, including the illegal-transition negative test.*

## Learning Objectives

- Describe the infrastructure lifecycle stages from planning through
  decommissioning and map them to the ITIL 4 service value chain.
- Distinguish configuration management (CMDB) from IT asset management
  (ITAM) and explain why an enterprise needs both.
- Design a change management process with risk-based change categories and
  a defined Change Advisory Board (CAB) role.
- Plan patch and capacity management as recurring lifecycle disciplines
  rather than one-time projects.
- Execute a secure decommissioning process aligned with NIST SP 800-88
  media sanitization guidance.

## Theory and Architecture

Infrastructure lifecycle management is the discipline of treating every
asset — physical or virtual, on-premises or cloud — as having a defined,
tracked path from initial planning through eventual retirement, rather
than as something that simply exists once deployed. [Chapter 06](06-understanding-enterprise-infrastructure.md) introduced
the domain taxonomy this encyclopedia organizes itself around, and Chapter
07 introduced the governance mechanisms that decide what gets built.
Lifecycle management is what happens after that decision: the ongoing
discipline of keeping every deployed asset accounted for, current,
changed under control, and eventually removed deliberately rather than
abandoned in place.

### Lifecycle stages

Every infrastructure asset — a server, a network device, a cloud resource,
a software license — moves through a common sequence of stages:

1. **Plan and design.** Requirements, sizing, and architecture (Chapter
   07's domain) determine what will be built before any procurement or
   provisioning begins.
2. **Procure or provision.** Physical assets are purchased, received, and
   racked; cloud or virtual assets are provisioned through infrastructure
   as code ([Chapter 03](03-automation-architecture.md), formalized further in [Volume IX](../../volume-09-infrastructure-automation/README.md)).
3. **Deploy.** The asset is configured to its intended running state and
   brought into service.
4. **Operate and maintain.** The asset runs in production, subject to
   monitoring ([Volume XI](../../volume-11-observability-enterprise-operations/README.md)), patching, and change management (this
   chapter).
5. **Optimize.** Capacity and cost are reviewed against actual utilization,
   often triggering resizing, consolidation, or migration between
   consumption models discussed in [Chapter 06](06-understanding-enterprise-infrastructure.md).
6. **Decommission and retire.** The asset is removed from service, its
   data sanitized or destroyed, and its records closed out — the stage
   organizations most consistently under-invest in, and the source of
   disproportionate security and compliance risk relative to its cost.

### Mapping to the ITIL 4 service value chain

ITIL 4 reframes the older, more linear ITIL service lifecycle as a service
value chain of six activities that can be combined in different orders
depending on the situation, rather than a fixed sequence:

| ITIL 4 value chain activity | What it covers | Relationship to the stages above |
| --- | --- | --- |
| Plan | Strategic direction and portfolio management | Feeds Plan and design |
| Improve | Continual improvement across all activities | Feeds Optimize |
| Engage | Understanding stakeholder needs and maintaining relationships | Spans all stages |
| Design and transition | Designing and moving services into production | Feeds Plan and design, Deploy |
| Obtain/build | Acquiring or building service components | Feeds Procure or provision |
| Deliver and support | Day-to-day operation and support | Feeds Operate and maintain |

The practical takeaway for infrastructure teams is not to memorize ITIL
terminology, but to recognize that lifecycle management is not a purely
linear pipeline — an asset in the Operate stage regularly triggers new
Plan activity (capacity growth, a discovered vulnerability), and a mature
practice's tooling should support that feedback loop rather than assuming
every asset moves through the stages exactly once.

### Configuration and asset management

Two related but distinct practices are frequently conflated:

- **IT Asset Management (ITAM)** tracks the financial and contractual
  lifecycle of an asset: purchase cost, warranty, license entitlement,
  depreciation schedule, and disposal value. ITAM answers "what do we own
  and what is it worth."
- **Configuration Management (CMDB — Configuration Management Database)**
  tracks the technical state and relationships of Configuration Items
  (CIs): what an asset is, what it depends on, and what depends on it.
  A CMDB answers "what exists, how is it configured, and what breaks if it
  changes."

An enterprise needs both because they answer different questions to
different audiences: finance and procurement consume ITAM data; change
management, incident response, and dependency analysis consume CMDB data.
[Chapter 06](06-understanding-enterprise-infrastructure.md)'s domain inventory operates one level above both — it tracks
domains, not individual assets — and a mature organization's CMDB is the
domain inventory's natural drill-down target.

### Change management

Change management governs how modifications to production infrastructure
are proposed, assessed, approved, and recorded. Enterprises typically
classify changes into three risk-based categories:

| Change type | Risk profile | Typical approval path |
| --- | --- | --- |
| Standard change | Pre-approved, low-risk, repeatable (for example, a routine certificate rotation using a tested runbook) | Pre-authorized; no case-by-case approval required |
| Normal change | Requires individual risk assessment | Reviewed by a Change Advisory Board (CAB) or delegated approver before a scheduled window |
| Emergency change | Addresses an active incident or imminent risk | Expedited approval, often a smaller emergency CAB, with mandatory retrospective review |

A **Request for Change (RFC)** is the record that carries a proposed
change through this process: what will change, why, the rollback plan, and
the change window. The RFC pattern parallels the pull request pattern from
[Chapter 04](04-github-project-and-workflow-management.md) closely enough that many organizations implement RFCs as
structured issues in the same system used for code review — the review
and approval mechanics differ in formality, but the underlying principle
(propose, assess, approve, execute, record) is identical.

### Patch and capacity management

Patch management and capacity management are both recurring, not
one-time, lifecycle disciplines:

- **Patch management** tracks the gap between an asset's current software
  version and the vendor's latest security-relevant release, prioritizing
  remediation by severity and exposure. Every asset's expected patch
  cadence should be documented against the dated baseline this
  encyclopedia maintains in
  [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md); a baseline with
  no revisit date is not a baseline, it is a snapshot slowly becoming
  wrong.
- **Capacity management** forecasts demand against current provisioned
  capacity and triggers the Optimize stage before a shortfall becomes an
  incident. Capacity planning differs meaningfully between fixed-capacity
  environments (on-premises hardware with lead-time-bound procurement) and
  elastic environments (public cloud, where capacity can, in principle, be
  added on demand but where cost discipline requires the same forecasting
  effort in reverse).

Both disciplines depend on End-of-Life (EOL) and End-of-Support (EOS)
tracking: knowing not just an asset's current version but the date beyond
which the vendor stops shipping security fixes, so a refresh or upgrade
project can be planned with lead time rather than triggered reactively
after support has already lapsed.

### Decommissioning

Decommissioning is the lifecycle stage most often treated as an
afterthought, and it carries disproportionate risk when it is: a
decommissioned asset's data, credentials, and network access must be
retired as deliberately as they were provisioned. NIST Special
Publication 800-88, *Guidelines for Media Sanitization*, defines three
sanitization categories that map directly to enterprise decommissioning
decisions:

| Method | What it does | When it applies |
| --- | --- | --- |
| Clear | Logical techniques (for example, a full overwrite) applied to all addressable storage locations | Media being reused within the organization's control |
| Purge | Physical or logical techniques rendering data recovery infeasible even with advanced laboratory techniques | Media being reused outside the organization's direct physical control |
| Destroy | Physical destruction rendering the media unusable | Media that will never be reused, or where Purge is not technically supported by the media type |

Decommissioning also includes closing out the ITAM and CMDB records for
the asset, revoking any credentials or network access scoped to it, and
reclaiming any software licenses — a checklist, not a single action, and
one this chapter's lab enforces as an explicit lifecycle state rather
than an implicit "we deleted the VM" assumption.

## Design Considerations

- **CMDB automation vs. manual maintenance.** A manually maintained CMDB
  drifts from reality within weeks in any environment with meaningful
  change velocity. Prefer discovery-based or infrastructure-as-code-driven
  CMDB population (where the same Terraform or Ansible run that provisions
  an asset also registers it) over relying on engineers to remember a
  separate documentation step.
- **Change risk tiering calibration.** Classifying too many changes as
  "Normal" overloads the CAB and slows delivery without a proportional
  safety benefit; classifying too many as "Standard" erodes the review
  step's value. Calibrate categories against actual change-failure-rate
  data, and revisit the classification periodically rather than treating
  it as fixed at first definition.
- **Change windows and freeze periods.** Restricting changes to defined
  windows reduces the population of concurrent changes an incident
  responder must reason about, but a freeze that is too broad or too
  frequent pushes legitimate work into the freeze's edges, increasing
  batch size and risk exactly where it was meant to reduce it. Scope
  freezes to genuinely high-risk periods (major sales events, financial
  close) rather than applying them by default.
- **Hardware refresh cadence vs. cloud elasticity.** On-premises hardware
  typically follows a 3-5 year refresh cycle driven by vendor support
  lifecycles and warranty terms; cloud resources have no equivalent fixed
  cadence but require continuous right-sizing discipline instead. An
  organization operating both models needs two different lifecycle
  cadences tracked explicitly, not one assumed cadence applied uniformly.
- **Who owns closing out a decommissioned asset's records.** Decommission
  is frequently split across teams — infrastructure removes the running
  asset, security revokes access, finance closes the ITAM record — and
  without a single accountable owner for the full checklist, individual
  steps get silently skipped. Assign end-to-end decommission ownership
  explicitly, the same way [Chapter 06](06-understanding-enterprise-infrastructure.md) required explicit domain ownership.
- **Data sanitization method selection has cost and time trade-offs.**
  Destroy is the most certain method but forecloses any asset resale or
  reuse value; Purge preserves reuse value at greater verification cost;
  Clear is cheapest but only appropriate when the media never leaves
  organizational control. Choose the method against the data
  classification of what the asset held, not against convenience.

## Implementation and Automation

### 1. A minimal CMDB record with an explicit lifecycle state

```json
{
  "asset_id": "srv-app-0export-042",
  "domain": "compute",
  "lifecycle_state": "operating",
  "owner": "platform-eng@example.com",
  "environment": "production",
  "eol_date": "2029-06-30",
  "last_reviewed": "2026-07-01"
}
```

### 2. Encoding legal lifecycle transitions as a state machine

Modeling the lifecycle as an explicit state machine — rather than a free-
text status field — is what makes an illegal transition (for example,
`decommissioned` back to `operating`) a validation failure instead of a
silent data-integrity problem:

```bash
#!/usr/bin/env bash
# validate-lifecycle-transition.sh — enforce legal CMDB state transitions
set -euo pipefail

from="$1"
to="$2"

# A case statement (rather than an associative array) keeps this portable
# to bash 3.2, which is still the default /bin/bash on macOS.
case "$from" in
  planned)         allowed="procured" ;;
  procured)        allowed="deployed" ;;
  deployed)        allowed="operating" ;;
  operating)       allowed="maintenance decommissioned" ;;
  maintenance)     allowed="operating decommissioned" ;;
  decommissioned)  allowed="" ;;
  *)
    echo "UNKNOWN STATE: '$from' is not a valid lifecycle state" >&2
    exit 1
    ;;
esac

if [[ ! " ${allowed} " =~ " ${to} " ]]; then
  echo "ILLEGAL TRANSITION: '$from' -> '$to' is not permitted" >&2
  echo "Allowed from '$from': ${allowed:-none (terminal state)}" >&2
  exit 1
fi

echo "OK: '$from' -> '$to' is a legal transition"
```

### 3. Applying a transition to the CMDB record

```bash
#!/usr/bin/env bash
# apply-transition.sh — validate, then apply, a CMDB lifecycle transition
set -euo pipefail
FILE="$1"
NEW_STATE="$2"

CURRENT_STATE=$(jq -r '.lifecycle_state' "$FILE")

./validate-lifecycle-transition.sh "$CURRENT_STATE" "$NEW_STATE"

jq --arg state "$NEW_STATE" --arg date "$(date -u +%Y-%m-%d)" \
  '.lifecycle_state = $state | .last_reviewed = $date' \
  "$FILE" > "${FILE}.tmp"
mv "${FILE}.tmp" "$FILE"
echo "Applied: $FILE is now '$NEW_STATE'"
```

### 4. A change request template as a structured issue form

```yaml
# .github/ISSUE_TEMPLATE/change_request.yml
name: Request for Change (RFC)
description: Propose a change to production infrastructure
labels: ["type:change"]
body:
  - type: dropdown
    id: risk_category
    attributes:
      label: Change category
      options:
        - "Standard (pre-approved runbook)"
        - "Normal (requires CAB review)"
        - "Emergency (active incident)"
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: What will change, and why?
    validations:
      required: true
  - type: textarea
    id: rollback
    attributes:
      label: Rollback plan
    validations:
      required: true
  - type: input
    id: window
    attributes:
      label: Proposed change window
      placeholder: "2026-07-25 02:00-04:00 UTC"
    validations:
      required: true
```

### 5. Checking EOL/EOS exposure against the CMDB

```bash
# report-eol-exposure.sh — list assets whose EOL date is within 180 days
jq -r --arg cutoff "$(date -u -v+180d +%Y-%m-%d 2>/dev/null || date -u -d '+180 days' +%Y-%m-%d)" \
  '.[] | select(.eol_date <= $cutoff) | "\(.asset_id): EOL \(.eol_date)"' \
  cmdb-assets.json
```

## Validation and Troubleshooting

- **CMDB records that exist but were never updated.** A `last_reviewed`
  date far in the past is a stronger signal of an unreliable CMDB record
  than the absence of a record entirely, because a missing record is at
  least an obvious gap — a stale one looks authoritative while being
  wrong. Alert on records past a defined staleness threshold, not only on
  missing records.
- **Illegal transitions attempted through a manual edit, bypassing the
  validator.** A CMDB stored as version-controlled data (as in this
  chapter's examples) is only as reliable as the enforcement path; a
  direct edit to the JSON file that skips `apply-transition.sh` bypasses
  the state machine entirely. Enforce transitions in CI (reject a pull
  request that changes `lifecycle_state` without a passing validator run)
  the same way [Chapter 02](02-repository-architecture.md) enforced structural validation.
- **Change category misclassification discovered only after an incident.**
  If a change classified as "Standard" causes an outage, that is a signal
  the pre-approval criteria for that runbook were too broad, not simply a
  one-off failure; feed change-failure data back into the risk-tiering
  calibration described in Design Considerations.
- **EOL exposure discovered with no lead time.** An asset that reaches its
  EOS date with no refresh project already underway indicates the EOL
  report (Implementation step 5) was not being reviewed on a recurring
  cadence. Schedule the exposure report as a recurring job, not an ad hoc
  query run only when a vendor announcement prompts concern.
- **Decommissioning "completed" but the asset still appears in monitoring
  or billing.** A partial decommission — the running instance removed, but
  its monitoring agent, DNS record, or billing line item left behind — is
  extremely common. Treat decommission as complete only when every system
  that referenced the asset (CMDB, ITAM, monitoring, DNS, billing) has
  been checked explicitly, not when the asset itself stops responding.

## Security and Best Practices

- Enforce data sanitization method selection (Clear, Purge, Destroy)
  against the data classification of what the asset held, and record which
  method was used and by whom as part of the decommission record — this is
  frequently an audit requirement, not merely good practice, under
  frameworks such as PCI DSS and HIPAA.
- Revoke credentials, API keys, and network access scoped to an asset
  before or during decommissioning, not after; a decommissioned asset with
  still-valid credentials is a dangling attack surface with no
  corresponding monitoring, because nothing expects it to be active
  anymore.
- Require CAB (or delegated) approval to be recorded against the RFC
  itself, not communicated informally (a verbal approval or a chat
  message), so the change record remains a complete audit trail on its
  own.
- Restrict who can apply a lifecycle-state transition in the CMDB to a
  narrowly scoped automation identity or role, mirroring the least-
  privilege principle [Chapter 03](03-automation-architecture.md) applied to CI-to-cloud credentials — CMDB
  write access is effectively write access to the organization's
  understanding of its own infrastructure.
- Treat an emergency change's mandatory retrospective review as
  non-optional; an emergency change that bypassed normal review is exactly
  the change most likely to need a follow-up correction, and skipping the
  retrospective because the incident is resolved discards that signal.
- Track EOL/EOS dates as a security control, not only a cost or
  reliability concern — unsupported software with no vendor security
  patches is one of the most common root causes found in post-incident
  reviews across the industry.

## References and Knowledge Checks

**References**

- [AXELOS/PeopleCert, *ITIL 4 Foundation*](https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil-4-foundation-2565) — the service value chain model
  referenced in this chapter.
- [NIST Special Publication 800-88 Rev. 1, *Guidelines for Media
  Sanitization*](https://csrc.nist.gov/pubs/sp/800/88/r1/final) — the Clear/Purge/Destroy model used in the
  Decommissioning section.
- [ITIL 4 Practice Guide](https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil-4-foundation-2565) — *Change Enablement* — the standard/normal/
  emergency change categorization used in this chapter.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline, the direct analog of the EOL/EOS tracking
  this chapter recommends for every managed asset.
- [Chapter 06](06-understanding-enterprise-infrastructure.md) (Understanding Enterprise Infrastructure) — the domain
  inventory that this chapter's CMDB records drill down from.

**Knowledge checks**

1. Explain the difference between ITAM and a CMDB, and why an enterprise
   needs both rather than treating them as interchangeable.
2. Why does modeling lifecycle state as an explicit state machine catch
   errors that a free-text status field would not?
3. Give an example of a change that should be pre-approved as a "Standard"
   change, and explain what would make it graduate to requiring "Normal"
   change review instead.
4. Under NIST SP 800-88, when is Purge an appropriate sanitization method
   instead of Destroy, and what does choosing it depend on?

## Hands-On Lab

**Objective:** Build a minimal, git-tracked CMDB record with an enforced
lifecycle state machine, drive an asset through several legal transitions
to decommissioning, and prove the validator rejects an illegal transition
attempted after decommissioning.

**Prerequisites**

- `bash` and `jq` installed.
- A local Git repository (a new scratch repository is sufficient).

**Steps**

1. Create the working directory and an initial CMDB record:

   ```bash
   mkdir -p ~/lifecycle-lab/scripts ~/lifecycle-lab/cmdb
   cd ~/lifecycle-lab
   git init -q
   cat > cmdb/srv-app-lab-001.json <<'EOF'
   {
     "asset_id": "srv-app-lab-001",
     "domain": "compute",
     "lifecycle_state": "planned",
     "owner": "platform-eng@example.com",
     "environment": "lab",
     "eol_date": "2030-01-01",
     "last_reviewed": "2026-07-18"
   }
   EOF
   ```

2. Add the transition validator:

   ```bash
   cat > scripts/validate-lifecycle-transition.sh <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   from="$1"
   to="$2"
   case "$from" in
     planned)         allowed="procured" ;;
     procured)        allowed="deployed" ;;
     deployed)        allowed="operating" ;;
     operating)       allowed="maintenance decommissioned" ;;
     maintenance)     allowed="operating decommissioned" ;;
     decommissioned)  allowed="" ;;
     *)
       echo "UNKNOWN STATE: '$from' is not a valid lifecycle state" >&2
       exit 1
       ;;
   esac
   if [[ ! " ${allowed} " =~ " ${to} " ]]; then
     echo "ILLEGAL TRANSITION: '$from' -> '$to' is not permitted" >&2
     echo "Allowed from '$from': ${allowed:-none (terminal state)}" >&2
     exit 1
   fi
   echo "OK: '$from' -> '$to' is a legal transition"
   EOF
   chmod +x scripts/validate-lifecycle-transition.sh
   ```

3. Add the apply script:

   ```bash
   cat > scripts/apply-transition.sh <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   FILE="$1"
   NEW_STATE="$2"
   CURRENT_STATE=$(jq -r '.lifecycle_state' "$FILE")
   "$(dirname "$0")/validate-lifecycle-transition.sh" "$CURRENT_STATE" "$NEW_STATE"
   jq --arg state "$NEW_STATE" --arg date "$(date -u +%Y-%m-%d)" \
     '.lifecycle_state = $state | .last_reviewed = $date' \
     "$FILE" > "${FILE}.tmp"
   mv "${FILE}.tmp" "$FILE"
   echo "Applied: $FILE is now '$NEW_STATE'"
   EOF
   chmod +x scripts/apply-transition.sh
   ```

4. Drive the asset through its normal lifecycle:

   ```bash
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json procured
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json deployed
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json operating
   ```

   **Expected result:** Each command prints `OK: ... is a legal
   transition` followed by `Applied: ... is now '<state>'`, and
   `jq -r '.lifecycle_state' cmdb/srv-app-lab-001.json` reports
   `operating`.

5. Commit the baseline:

   ```bash
   git add -A
   git commit -q -m "feat: track srv-app-lab-001 through deployment to operating"
   ```

6. Transition the asset to maintenance and back to operating, then
   decommission it:

   ```bash
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json maintenance
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json operating
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json decommissioned
   jq -r '.lifecycle_state' cmdb/srv-app-lab-001.json
   ```

   **Expected result:** Final output is `decommissioned`.

7. **Negative test:** Attempt to bring the decommissioned asset back into
   service:

   ```bash
   ./scripts/apply-transition.sh cmdb/srv-app-lab-001.json operating
   echo "Exit code: $?"
   ```

   **Expected result:** The script prints `ILLEGAL TRANSITION:
   'decommissioned' -> 'operating' is not permitted` and `Allowed from
   'decommissioned': none (terminal state)`, exits non-zero, and — because
   the validator runs before the record is modified — `jq -r
   '.lifecycle_state' cmdb/srv-app-lab-001.json` still reports
   `decommissioned`, confirming the record was never corrupted by the
   rejected transition.

8. **Cleanup:**

   ```bash
   cd ~ && rm -rf ~/lifecycle-lab
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Infrastructure lifecycle management treats every asset as moving through
a defined sequence — plan, procure, deploy, operate, optimize, decommission
— that maps onto the ITIL 4 service value chain's six activities. ITAM and
a CMDB answer different questions (financial/contractual ownership versus
technical configuration and dependency) and both are necessary. Change
management classifies changes by risk to route them through proportionate
approval, and patch and capacity management are recurring disciplines
tracked against a dated baseline, not one-time projects. Decommissioning
is the stage most often under-invested in and carries the most
disproportionate risk when skipped; NIST SP 800-88's Clear/Purge/Destroy
model, paired with an enforced lifecycle state machine, turns
decommissioning into a verifiable, terminal state rather than an implicit
assumption.

- [ ] Can map the six infrastructure lifecycle stages to the ITIL 4
      service value chain's six activities.
- [ ] Can explain the difference between ITAM and a CMDB and why both are
      needed.
- [ ] Can design a risk-tiered change management process with a defined
      CAB role.
- [ ] Can select an appropriate NIST SP 800-88 sanitization method for a
      given data classification and reuse scenario.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
