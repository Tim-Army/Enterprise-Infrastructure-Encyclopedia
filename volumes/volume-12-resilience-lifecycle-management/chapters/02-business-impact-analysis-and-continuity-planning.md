# Chapter 2: Business Impact Analysis and Continuity Planning

![Lab flow for this chapter: derive_mtd.py walks a sample BIA's impact-escalation curve and finds the operational impact category first crosses the severity threshold at the 24-hour checkpoint, producing a derived MTD deliberately in conflict with the questionnaire's owner-stated 48 hours; the evidence-based figure takes precedence, escalated to the process owner for reconciliation. As a negative test, every checkpoint's impact scores are set identical (no escalation over time); the script still returns a 1-hour-checkpoint-based MTD, but this flat-impact scenario should itself be flagged as suspect during BIA quality review.](../../../diagrams/volume-12-resilience-lifecycle-management/chapter-02-bia-mtd-derivation-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: deriving a maximum tolerable downtime from a BIA impact-escalation curve, checked against a flat-impact negative test.*

## Learning Objectives

- Explain the purpose and output of a business impact analysis (BIA) and how it differs from a risk assessment.
- Derive recovery time objective (RTO), recovery point objective (RPO), and maximum tolerable downtime (MTD) from business impact data rather than technical convenience.
- Score business processes for financial, operational, regulatory, and reputational impact using a repeatable methodology.
- Distinguish business continuity planning (BCP), continuity of operations planning (COOP), and IT disaster recovery planning (DRP), and describe how they relate.
- Select an appropriate alternate-site or recovery strategy (hot, warm, cold, pilot light) based on BIA output and cost constraints.
- Produce a reviewable BIA document and a continuity plan skeleton for a business process.

## Theory and Architecture

### What a BIA Is (and Is Not)

A business impact analysis is the structured process of identifying business processes, determining the impact of their disruption over time, and deriving recovery requirements from that impact. It answers "if this process stops, what happens, and how quickly does it get worse?" A BIA is frequently confused with a risk assessment, but the two ask different questions: a risk assessment asks "what could go wrong and how likely is it?"; a BIA asks "regardless of cause, what is the consequence of this process being unavailable, and for how long can we tolerate it?" The BIA is cause-agnostic by design — a payment processing outage has the same business consequence whether it was caused by a failed disk, a ransomware event, a regional power outage, or human error. This is why the BIA, not the risk register, is the correct starting point for setting RTO and RPO: recovery targets should reflect what the business can survive, not what a particular failure scenario happens to allow.

The BIA sits upstream of the criticality register introduced in [Chapter 1](01-resilience-engineering-and-critical-service-design.md). Where [Chapter 1](01-resilience-engineering-and-critical-service-design.md) treated tiering as a given input to architecture, this chapter defines the methodology that produces defensible tier and RTO/RPO values in the first place.

### Recovery Time Objective, Recovery Point Objective, and Maximum Tolerable Downtime

Three metrics anchor every continuity and disaster-recovery conversation:

- **RTO (Recovery Time Objective)** — the maximum acceptable time between an outage starting and the process being restored to an operating state. RTO is a target the technical recovery design must meet.
- **RPO (Recovery Point Objective)** — the maximum acceptable amount of data loss, measured as time (for example, "15 minutes of transactions"). RPO drives replication and backup frequency decisions.
- **MTD (Maximum Tolerable Downtime)** — the absolute ceiling beyond which the organization suffers unacceptable or unrecoverable harm (a failed regulatory filing, a contractual breach, a life-safety issue). MTD is a business-defined hard boundary, not a target to aim for.

The relationship between these three is frequently misunderstood: RTO must always be less than MTD, with margin, because RTO is measured from outage detection while MTD is measured from outage onset, and detection itself consumes time. A related figure, **WRT (Work Recovery Time)**, accounts for the time needed after systems are technically restored before the business process is fully caught up (reprocessing a backlog, reconciling data, re-notifying customers). A common modeling error is setting RTO equal to MTD with no margin for detection time or WRT, which produces a plan that is compliant on paper and fails in practice.

```text
Timeline:
  Outage begins ----[detection lag]----> Outage detected
  Outage detected --[RTO]--> System restored --[WRT]--> Process fully recovered
  Outage begins ---------------------[MTD]---------------------> Unacceptable harm threshold

  Constraint: detection lag + RTO + WRT < MTD, with margin
```

### Impact Categories and Scoring

A rigorous BIA scores impact across multiple dimensions rather than a single "dollars lost" figure, because not every consequential impact is immediately financial:

| Impact Category | Example Questions | Typical Data Source |
| --- | --- | --- |
| Financial | Lost revenue per hour, contractual penalties, cost of manual workaround | Finance, process owner |
| Operational | Backlog growth rate, dependent process cascading failure, staff idle time | Process owner, operations |
| Regulatory/Compliance | Reporting deadlines missed, license or certification jeopardized | Legal, compliance |
| Reputational | Customer-visible outage, media exposure, SLA breach with key accounts | Customer success, communications |
| Safety | Any life-safety or environmental consequence | EHS, legal |

Each category is typically scored on a 1–5 scale at defined elapsed-time checkpoints (1 hour, 4 hours, 24 hours, 3 days, 1 week), because impact is rarely linear — a process may be a minor inconvenience at 1 hour and catastrophic at 24 hours. Plotting impact score against elapsed time produces an **impact escalation curve**, and the point where the curve crosses an "unacceptable" threshold is a defensible source for MTD, rather than an arbitrary round number.

### From BIA to Recovery Strategy

Once RTO, RPO, and MTD are established per process, they map to a recovery strategy and, transitively, an infrastructure investment:

| RTO Range | Typical Strategy | Infrastructure Pattern |
| --- | --- | --- |
| Seconds–minutes | Hot site / active-active | Real-time replication, automated failover ([Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md)) |
| Under 4 hours | Warm site / pilot light | Standing infrastructure, data replicated, manual or semi-automated activation |
| 4–24 hours | Cold site / backup-and-restore | Infrastructure provisioned on demand, restore from backup ([Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md)) |
| Days | Reciprocal or contracted recovery | Third-party or alternate-facility arrangement |
| Not required | Accept the risk | Documented and formally accepted by process owner |

This mapping is the bridge between Chapter 2's business analysis and [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md)'s DR engineering: the BIA determines which strategy row applies; [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md) details how to build and test the corresponding infrastructure pattern.

## Design Considerations

### Process-Centric, Not System-Centric, Analysis

A BIA is conducted at the business-process level (for example, "process customer refunds," "run payroll," "clear trades") and only then mapped down to the supporting applications and infrastructure. Starting from the system inventory instead of the process inventory produces two failure modes: infrastructure gets protected that no active business process actually depends on, and a business-critical process turns out to depend on a system nobody flagged as important because its name did not sound critical. The dependency-mapping technique from [Chapter 1](01-resilience-engineering-and-critical-service-design.md) is the tool that performs this process-to-system translation; the BIA questionnaire feeds the process side, and the dependency graph feeds the system side.

### Interviewing Process Owners Effectively

Process owners routinely overstate criticality (self-preservation bias) or cannot articulate downstream cascading effects (they see their own process, not what depends on it). Mitigate both by:

- Anchoring impact questions to concrete elapsed-time checkpoints rather than open-ended "how bad would it be?"
- Cross-referencing the process owner's answers against the dependency graph to catch cascading effects the owner may not see.
- Requiring impact claims above a materiality threshold to cite a source (a contract clause, an SLA, a regulatory deadline) rather than accepting an unsupported assertion.

### Aggregation and Prioritization

A large enterprise BIA can cover hundreds of processes. Aggregate and prioritize using a simple weighted score, but keep the underlying category scores visible — a single blended number hides the difference between "expensive but survivable" and "small dollar impact but a regulatory trigger." Present findings as a ranked list with the full category breakdown available, not a single collapsed ranking.

### Continuity Planning Scope: BCP, COOP, and DRP

Three related but distinct plan types are frequently conflated:

- **BCP (Business Continuity Plan)** — organization-wide, covers people, facilities, suppliers, and processes, not just IT. Addresses "how does the business keep operating," including manual workarounds that do not involve technology at all.
- **COOP (Continuity of Operations Plan)** — a term most common in government and public-sector contexts, focused on maintaining essential functions and lines of succession during and after a significant disruption, often facilities- and personnel-centric.
- **DRP (Disaster Recovery Plan)** — the IT-specific subset that restores technology infrastructure and data. DRP is the plan most directly implemented by the patterns in [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md).

A BIA informs all three; the recovery strategy table above is primarily a DRP input, but the underlying impact analysis (loss of a facility, loss of key staff, loss of a supplier) belongs to BCP/COOP and should not be discarded just because this volume's later chapters focus on infrastructure.

## Implementation and Automation

### A Structured BIA Questionnaire

Standardize data collection so responses are comparable across processes:

```yaml
# bia-questionnaire-template.yaml
process_id: customer-refunds
process_owner: finance-ops
supporting_systems:
  - checkout-api
  - payment-gateway-external
  - erp-finance-module
impact_by_checkpoint:
  1h:  { financial: 1, operational: 2, regulatory: 1, reputational: 1, safety: 0 }
  4h:  { financial: 2, operational: 3, regulatory: 1, reputational: 2, safety: 0 }
  24h: { financial: 4, operational: 4, regulatory: 2, reputational: 3, safety: 0 }
  72h: { financial: 5, operational: 5, regulatory: 4, reputational: 4, safety: 0 }
manual_workaround_available: true
manual_workaround_capacity_pct: 20
derived_mtd_hours: 48
derived_rto_hours: 8
derived_rpo_minutes: 60
last_reviewed: "2026-05-20"
reviewed_by: "finance-ops-director"
```

Storing responses in structured form (rather than a shared document) allows the same tooling built in [Chapter 1](01-resilience-engineering-and-critical-service-design.md) to validate that every Tier 0/1 service in the criticality register has a corresponding, current BIA record, and to flag processes whose derived RTO does not match their assigned tier's target.

### Deriving MTD From the Impact Escalation Curve

```python
def derive_mtd(impact_by_checkpoint: dict, threshold: int = 4) -> int:
    """Return the earliest checkpoint (in hours) at which any impact
    category reaches or exceeds the unacceptable threshold."""
    checkpoint_hours = {"1h": 1, "4h": 4, "24h": 24, "72h": 72}
    crossings = []
    for checkpoint, scores in impact_by_checkpoint.items():
        if max(scores.values()) >= threshold:
            crossings.append(checkpoint_hours[checkpoint])
    return min(crossings) if crossings else None
```

Running this function against the questionnaire example above returns 24 (the 24-hour checkpoint, where operational impact first reaches 4), giving a data-derived MTD rather than a guessed one. Compare this systematically against the `derived_mtd_hours` value supplied by the process owner and flag divergence for review — self-reported and calculated MTD disagreeing is a signal that the checkpoint scoring or the owner's stated figure needs reconciliation.

### Continuity Plan Skeleton

A minimal, automatable continuity plan document structure keeps plans consistent and testable:

```markdown
# Continuity Plan: <process-id>

## Activation Criteria
- Conditions under which this plan is invoked, and who has authority to invoke it.

## Recovery Team
- Role, name/rotation, contact method (primary and backup).

## Recovery Steps
1. Numbered, specific, testable steps.

## Manual Workaround
- Description, capacity limits, and the point at which it must hand off to full recovery.

## Communication Plan
- Who is notified, by what channel, at what elapsed-time intervals.

## Dependencies
- Cross-reference to the Chapter 1 dependency map entries relevant to this process.

## Plan Test History
| Date | Test Type | Result | Follow-up Actions |
```

Keep continuity plans in the same version-controlled repository as the criticality register and BIA data so that a change to RTO/RPO in the BIA can be linked, in the same review, to the plan and infrastructure that must change to support it.

## Validation and Troubleshooting

### Validating BIA Quality

- Check for **checkpoint monotonicity**: impact scores should not decrease at a later checkpoint (a process rarely gets less painful to have down the longer it stays down). A decrease is a data-entry or methodology error, not a real finding, in the large majority of cases.
- Check for **RTO/tier consistency**: cross-reference every BIA record's derived RTO against the criticality tier assigned in the [Chapter 1](01-resilience-engineering-and-critical-service-design.md) register; a Tier 0 service with a BIA-derived RTO of 12 hours indicates either the tier or the BIA is wrong.
- Check for **stale reviews**: flag any BIA record with `last_reviewed` older than the organization's review cadence (annually at minimum; more frequently for Tier 0/1).

### Common Troubleshooting Scenarios

| Symptom | Likely Cause | Corrective Action |
| --- | --- | --- |
| Every process claims Tier 0 | No calibration exercise across process owners; self-preservation bias | Run a relative-ranking calibration session across all owners together |
| Derived RTO shorter than any feasible recovery strategy can deliver | Business need genuinely exceeds current infrastructure investment | Escalate as a funding/risk-acceptance decision, not an engineering problem to silently absorb |
| Continuity plan untested for multiple years | No test cadence enforced | Establish mandatory test cadence tied to tier (see [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md)) |
| BIA and dependency map disagree on supporting systems | BIA questionnaire completed without dependency-graph cross-check | Require dependency-graph reconciliation as a mandatory BIA completion step |

## Security and Best Practices

- Treat completed BIA documents and continuity plans as sensitive: they describe exactly which processes, if disrupted, cause maximum harm, and are a target list for an adversary conducting reconnaissance for an extortion or sabotage scenario. Apply access controls consistent with the sensitivity of the underlying business data.
- Do not let continuity plans reference credentials, break-glass account details, or specific access procedures in plaintext; reference a secrets-management system instead (see [Volume X](../../volume-10-enterprise-cybersecurity/README.md) for enterprise secrets and identity practices).
- Require dual authorization for continuity-plan activation criteria on Tier 0 processes, mirroring change-management controls, so activation cannot be triggered unilaterally.
- Ensure recovery team contact information includes verified backups for every role; a continuity plan whose only escalation path is a single named individual has recreated the organizational SPOF discussed in [Chapter 1](01-resilience-engineering-and-critical-service-design.md).
- Align regulatory-impact scoring with actual current legal/compliance obligations, not assumptions; obligations change and a stale BIA can understate regulatory risk materially.

## References and Knowledge Checks

### References

- ISO 22301:2019, *Business continuity management systems — Requirements*.
- NIST SP 800-34 Rev. 1, *Contingency Planning Guide for Federal Information Systems*.
- ASIS International / DRI International BIA methodology guidance (Disaster Recovery Institute, driscotland.org / drii.org professional practices).
- [Chapter 1](01-resilience-engineering-and-critical-service-design.md) for the criticality register and dependency map this chapter's BIA output feeds.

### Knowledge Checks

1. Explain why a BIA is cause-agnostic and why that property matters when deriving RTO.
2. Given detection lag, RTO, and WRT, write the inequality that must hold relative to MTD, and explain what happens operationally when it does not.
3. Describe the difference between BCP, COOP, and DRP, and give an example of a continuity control that belongs to BCP but not DRP.
4. Why should impact be scored across multiple checkpoints in time rather than as a single number?
5. A process owner reports their process as Tier 0 with an MTD of 72 hours, but the dependency graph shows three other Tier 0 processes depend on it within a 2-hour window. How should this discrepancy be resolved?

## Hands-On Lab

### Lab: Conducting a BIA and Deriving Recovery Objectives

**Objective:** Complete a structured BIA for a sample business process, programmatically derive MTD from the impact escalation curve, and produce a continuity plan skeleton consistent with the result.

**Prerequisites:**

- `python3` (3.11+) and `pyyaml` (`pip install pyyaml`).
- The `criticality-register.yaml` and `dependencies.yaml` artifacts from the [Chapter 1](01-resilience-engineering-and-critical-service-design.md) lab (or freshly recreated equivalents).

**Procedure:**

1. Create a working directory:

   ```bash
   mkdir -p ~/labs/resilience-ch2 && cd ~/labs/resilience-ch2
   ```

2. Create `bia-customer-refunds.yaml` using the questionnaire template shown in this chapter, either reusing the example values or adjusting them to reflect a process of your choosing.

3. Save the `derive_mtd` function from this chapter as `derive_mtd.py`, and add a small driver that loads the YAML file and prints the derived MTD:

   ```python
   import yaml
   from pathlib import Path

   def derive_mtd(impact_by_checkpoint: dict, threshold: int = 4) -> int:
       checkpoint_hours = {"1h": 1, "4h": 4, "24h": 24, "72h": 72}
       crossings = [checkpoint_hours[c] for c, s in impact_by_checkpoint.items()
                    if max(s.values()) >= threshold]
       return min(crossings) if crossings else None

   data = yaml.safe_load(Path("bia-customer-refunds.yaml").read_text())
   mtd = derive_mtd(data["impact_by_checkpoint"])
   print(f"Derived MTD: {mtd} hours (owner-stated: {data['derived_mtd_hours']} hours)")
   ```

4. Run the script:

   ```bash
   python3 derive_mtd.py
   ```

**Expected Result:** The script prints a derived MTD of 24 hours against the example data, while the owner-stated value in the template is 48 hours — a deliberate discrepancy for this lab.

5. Investigate the discrepancy as you would in practice: examine which impact category crossed the threshold first (operational, at the 24-hour checkpoint) and document, in a `RESOLUTION.md` file, which figure should be used and why (in this example, the data-derived, evidence-based figure should generally take precedence, with the disagreement escalated to the process owner for reconciliation).

6. Using the continuity plan skeleton from this chapter, produce `continuity-plan-customer-refunds.md` with at least the Activation Criteria, Recovery Team, and Recovery Steps sections completed.

**Negative Test:** Edit `bia-customer-refunds.yaml` so every checkpoint's impact scores are identical (no escalation over time — an unrealistic but useful test case) and rerun `derive_mtd.py`. Confirm the script still returns a value based on the 1-hour checkpoint, and manually verify that this flat-impact scenario should itself be flagged as suspect during BIA quality review, per the checkpoint-monotonicity guidance in this chapter's Validation section.

**Cleanup:**

```bash
cd ~ && rm -rf ~/labs/resilience-ch2
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The business impact analysis converts business consequence into the technical vocabulary — RTO, RPO, MTD — that drives every recovery investment decision in this volume. It is process-centric, cause-agnostic, and multi-dimensional, and its output must be traceable and defensible, not asserted. BCP, COOP, and DRP are related but distinct plan types drawing on the same BIA data at different scopes. The next chapter ([Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md)) picks up where the BIA's fast-RTO strategies leave off, detailing the HA and fault-tolerance architecture needed to actually hit sub-minute and sub-hour recovery targets.

**Completion checklist:**

- [ ] Can define RTO, RPO, MTD, and WRT and state the inequality relating them.
- [ ] Can score business impact across financial, operational, regulatory, reputational, and safety dimensions at multiple time checkpoints.
- [ ] Can distinguish BCP, COOP, and DRP and identify which this volume's infrastructure chapters primarily support.
- [ ] Completed a structured BIA questionnaire for a sample process.
- [ ] Programmatically derived MTD from an impact escalation curve and reconciled it against a stated value.
- [ ] Produced a continuity plan skeleton consistent with the derived recovery objectives.
