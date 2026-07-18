# Chapter 07: Cybersecurity Incident Response and Digital Evidence

## Learning Objectives

- Apply the NIST SP 800-61 incident response lifecycle to structure
  preparation, detection and analysis, containment, eradication and
  recovery, and post-incident activity.
- Design an incident severity classification model and a communication
  plan that meets regulatory notification obligations.
- Apply digital forensics fundamentals — order of volatility, chain of
  custody, and forensically sound evidence collection — to preserve
  evidence integrity during response.
- Build incident response playbooks as structured, testable artifacts
  rather than static prose documents.
- Design and run a tabletop exercise that validates an incident response
  plan before a real incident tests it instead.
- Build and test a working evidence chain-of-custody and integrity
  verification workflow, including a negative test for tampered
  evidence.

## Theory and Architecture

### The incident response lifecycle

**NIST SP 800-61** (the *Computer Security Incident Handling Guide*, most
recently restructured to align with NIST CSF 2.0's functions) organizes
incident response into four phases:

1. **Preparation** — the work done before any incident: an approved IR
   plan, defined roles and authority, tooling, playbooks, and trained
   staff. Preparation quality is the single largest determinant of how
   well an organization performs during an actual incident — improvising
   process during a live incident is materially slower and more
   error-prone than executing a rehearsed plan.
2. **Detection and Analysis** — identifying that an incident is
   occurring, scoping its extent, and classifying its severity. This
   phase consumes the telemetry and detection capability built in
   Chapter 6; incident response does not have a separate detection
   pipeline, it consumes the same one.
3. **Containment, Eradication, and Recovery** — limiting further damage
   (containment), removing the adversary's presence and access
   (eradication), and restoring affected systems to normal, verified-clean
   operation (recovery). These are treated as one combined phase because
   they are often iterative — a contained incident can re-flare if
   eradication was incomplete, requiring a return to containment before
   recovery proceeds.
4. **Post-Incident Activity** — the lessons-learned review, evidence
   retention decisions, and process improvements that feed back into
   Preparation for the next incident. An incident that is closed without
   this phase wastes the organization's most expensive source of process
   improvement data.

This lifecycle is cyclical, not linear: Post-Incident Activity findings
should measurably change Preparation (updated playbooks, closed detection
gaps fed back to Chapter 6, corrected authority gaps), and Detection and
Analysis frequently loops back on itself as scope expands during
investigation.

### Incident classification and severity

A useful severity model combines **scope** (how many systems/users
affected), **data sensitivity** (what data is at risk, informed by the
classification scheme in Chapter 8), and **business impact** (is a
revenue-generating or safety-critical system affected) into a small
number of severity tiers, each with a defined response posture:

| Severity | Example criteria | Response posture |
| --- | --- | --- |
| SEV-1 (Critical) | Confirmed ransomware detonation, confirmed exfiltration of regulated data, safety-critical system compromise | Full IR team activation, executive notification within the hour, external forensics/legal engagement considered immediately |
| SEV-2 (High) | Confirmed compromise of a single production system with lateral-movement potential, privileged credential confirmed compromised | IR team activation, containment within a defined SLA, executive notification within the day |
| SEV-3 (Moderate) | Isolated malware detection with EDR-confirmed containment, contained phishing click with no follow-on activity | Standard IR workflow, no executive escalation required unless scope grows |
| SEV-4 (Low) | Policy violation with no confirmed compromise, blocked and logged attack attempt | Logged and tracked, no dedicated IR activation |

Severity should be assigned at first triage and re-assessed as scope
information changes — a SEV-3 classification that later reveals lateral
movement must be re-escalated immediately, not left at its initial rating
out of process inertia.

### Digital forensics fundamentals

Digital forensics applies scientific rigor to evidence collection so
findings are both technically sound and, where necessary, legally
defensible.

- **Order of volatility** — collect evidence in order from most to least
  volatile, since later collection steps can destroy earlier volatile
  evidence: CPU registers and cache, RAM contents, network state (active
  connections, ARP cache), running process list, disk contents, and
  finally archival/backup media. A forensic image of disk should follow,
  not precede, memory acquisition when both are needed and the system
  remains powered on.
- **Chain of custody** — a documented, unbroken record of who collected
  a piece of evidence, when, how, and who has held or accessed it since,
  with a cryptographic hash recorded at each handoff to prove integrity.
  A gap in chain of custody does not necessarily invalidate evidence for
  internal investigative purposes, but can materially weaken it for legal
  or regulatory proceedings.
- **Forensically sound collection** — using write-blockers for physical
  media, cryptographically hashing acquired images immediately after
  collection (and verifying the hash matches after every subsequent
  transfer), and working from a copy, never the original evidence,
  wherever possible.
- **Live forensics vs. dead-box forensics.** Modern incidents
  increasingly require live, running-system analysis (memory acquisition,
  live process inspection) because significant adversary activity leaves
  little or no disk artifact — full-disk imaging alone, the traditional
  "dead-box" approach, can miss memory-resident and cloud-native evidence
  entirely.

### Communication and legal coordination

An incident response plan must define, in advance, who is notified, in
what order, and under what triggering condition — decided calmly during
Preparation, not improvised under pressure during an active incident:

- **Internal stakeholders** — executive leadership, legal, HR (for
  insider-involved incidents), communications/PR, and affected business
  unit owners.
- **External notification** — regulatory bodies (GDPR's 72-hour breach
  notification requirement, state breach notification laws, sector
  regulators referenced in Chapter 1's regulatory landscape), affected
  customers or individuals, cyber insurance carriers (often with their
  own mandatory notification and vendor-selection requirements), and law
  enforcement where appropriate.
- **Outside counsel and forensics engagement** — engaging outside counsel
  early, and having that counsel direct external forensics engagement
  under attorney-client privilege, is a common pattern intended to
  protect the resulting investigative work product — this decision
  should be pre-negotiated (retainer in place) during Preparation, not
  sourced for the first time mid-incident.

### Tabletop exercises

A **tabletop exercise** walks the IR team through a realistic, scripted
scenario in a discussion-based format (no live systems touched) to
validate the plan, playbooks, and team's decision-making before a real
incident does. Effective tabletop exercises:

- Use a scenario relevant to the organization's actual threat profile and
  architecture (informed by the ATT&CK-based coverage review in
  Chapter 6), not a generic template.
- Include a decision point requiring genuine judgment (should we take a
  production system offline, do we have legal authority to isolate a
  third-party-managed system) rather than a purely technical walkthrough.
- Produce documented findings that feed directly into Preparation
  improvements — an exercise that surfaces the same gap repeatedly
  without a tracked remediation has failed at its actual purpose.

## Design Considerations

- **Decision authority for containment actions must be pre-delegated.**
  Isolating a production host, disabling a privileged account, or taking
  a customer-facing system offline all carry business impact. An IR plan
  that requires executive sign-off for every containment action during
  an active incident introduces dangerous delay; pre-delegate authority
  for defined, bounded containment actions to the IR incident commander,
  reserving executive approval for decisions with major business impact
  (public system-wide outage, law enforcement engagement).
- **Internal vs. retained external IR capability.** A fully internal IR
  team retains institutional knowledge and can respond fastest, but is
  rarely staffed for a sustained, complex incident (ransomware recovery
  routinely runs for weeks). A retainer with an external incident
  response firm, negotiated and tested before it is needed, provides
  surge capacity and specialized forensics expertise without full-time
  headcount — most mature programs use both.
- **Evidence retention vs. privacy and storage cost.** Retaining full
  forensic images indefinitely is expensive and can itself create
  privacy and data-minimization exposure (Chapter 8). Define a retention
  period aligned to realistic legal, regulatory, and insurance
  requirements, and dispose of evidence according to a documented
  schedule rather than either deleting prematurely or retaining
  indefinitely by default.
- **Out-of-band communication planning.** If primary communication and
  ticketing systems are hosted on infrastructure that may itself be
  compromised (email, chat, ticketing on the same domain under
  investigation), the IR team needs a pre-established out-of-band channel
  — this is a Preparation-phase decision, since standing up an
  alternative channel mid-incident, while the primary channel's integrity
  is in question, is far riskier.
- **Balancing speed and evidence integrity during containment.** Rapid
  eradication (wiping and rebuilding a compromised host) can destroy
  evidence needed for scoping and legal purposes. Define, in the IR plan,
  which incident severities require forensic preservation before
  remediation and which permit immediate rebuild — this should be a
  pre-agreed policy decision, not resolved ad hoc under pressure for
  every incident.

## Implementation and Automation

### Incident response playbook as structured configuration

```yaml
# playbooks/ransomware-detonation.yaml
playbook_id: ir-pb-004
title: "Confirmed Ransomware Detonation"
severity_floor: SEV-1
trigger_conditions:
  - "EDR alert: mass file modification/encryption behavior confirmed"
  - "Multiple hosts reporting ransom note artifact"
immediate_actions:
  - action: "Isolate affected hosts at the network layer (Chapter 4 segmentation controls)"
    owner: soc-tier2-oncall
    time_target_minutes: 15
  - action: "Preserve volatile evidence (memory) on at least one representative affected host before isolation completes rebuild"
    owner: forensics-lead
    time_target_minutes: 30
  - action: "Activate out-of-band communication channel"
    owner: incident-commander
    time_target_minutes: 10
  - action: "Notify legal and determine attorney-client privilege posture for external forensics engagement"
    owner: incident-commander
    time_target_minutes: 60
notification_requirements:
  - stakeholder: executive-leadership
    trigger: immediate
  - stakeholder: cyber-insurance-carrier
    trigger: within_24_hours
  - stakeholder: regulatory-bodies
    trigger: per-jurisdiction-requirement   # see Chapter 1 regulatory table
decision_gates:
  - question: "Is backup integrity confirmed unaffected before recovery begins?"
    owner: backup-recovery-lead
  - question: "Has eradication been validated (not just containment) before any host is reconnected?"
    owner: forensics-lead
```

### Chain-of-custody and evidence integrity logging

```python
#!/usr/bin/env python3
"""evidence_custody.py — record and verify a chain-of-custody log with
cryptographic integrity checks for collected evidence artifacts.
"""
import csv
import hashlib
import sys
from datetime import datetime, timezone


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def log_custody_event(log_path: str, evidence_id: str, artifact_path: str,
                       handler: str, action: str) -> None:
    digest = sha256_file(artifact_path)
    row = {
        "evidence_id": evidence_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "handler": handler,
        "action": action,
        "artifact_path": artifact_path,
        "sha256": digest,
    }
    file_exists = False
    try:
        with open(log_path, newline="", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        pass
    with open(log_path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    print(f"Logged: {evidence_id} {action} by {handler} sha256={digest}")


def verify_integrity(log_path: str, evidence_id: str, artifact_path: str) -> bool:
    expected = None
    with open(log_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["evidence_id"] == evidence_id:
                expected = row["sha256"]
    if expected is None:
        raise SystemExit(f"No custody record found for {evidence_id}")
    current = sha256_file(artifact_path)
    if current != expected:
        raise SystemExit(
            f"INTEGRITY FAILURE: {evidence_id} hash mismatch — "
            f"expected {expected}, got {current}"
        )
    print(f"Integrity verified: {evidence_id} matches original chain-of-custody hash")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("log", "verify"):
        raise SystemExit(
            "Usage: evidence_custody.py log <evidence_id> <artifact_path> <handler>\n"
            "       evidence_custody.py verify <evidence_id> <artifact_path>"
        )
    mode = sys.argv[1]
    if mode == "log":
        if len(sys.argv) != 5:
            raise SystemExit("Usage: evidence_custody.py log <evidence_id> <artifact_path> <handler>")
        log_custody_event("custody_log.csv", sys.argv[2], sys.argv[3], sys.argv[4], "collected")
    elif mode == "verify":
        if len(sys.argv) != 4:
            raise SystemExit("Usage: evidence_custody.py verify <evidence_id> <artifact_path>")
        verify_integrity("custody_log.csv", sys.argv[2], sys.argv[3])
```

### Severity-triggered notification timer

```bash
# Illustrative cron-driven check for a regulatory notification SLA clock
# (GDPR: 72 hours from confirmed personal-data breach)
0 * * * * /usr/local/bin/check_notification_sla.sh --incident-log /var/ir/active_incidents.csv --sla-hours 72
```

## Validation and Troubleshooting

- **Validate the IR plan with tabletop exercises, not just document
  review.** A plan that reads correctly on paper frequently reveals
  gaps (unclear authority, a missing stakeholder, an untested
  notification contact) only when actually walked through against a
  realistic scenario.
- **Common failure: unclear containment authority causes delay.** If a
  tabletop or real incident reveals that a Tier 2 analyst was uncertain
  whether they had authority to isolate a production host, that is a
  Preparation-phase failure, not an individual performance failure —
  fix the delegated-authority documentation, not just the specific
  analyst's judgment.
- **Common failure: evidence collected out of volatility order.** If disk
  imaging occurs before memory acquisition on a system that will
  subsequently be powered off, volatile evidence is permanently lost.
  Build the order-of-volatility sequence into the playbook itself
  (as in the ransomware playbook example above) rather than relying on
  the responder's memory during a high-stress incident.
- **Common failure: notification SLA missed due to untracked clock
  start.** Regulatory notification windows (GDPR's 72 hours, for
  example) start from confirmed awareness, not from final root-cause
  determination; a program that waits for full investigation completion
  before starting the notification clock risks missing the actual legal
  deadline. Track the clock from initial confirmed-breach determination
  and treat notification as parallel to, not sequential after,
  investigation.
- **Diagnosing chain-of-custody gaps**: any handoff without a logged
  hash-verified entry is a gap; review the custody log for continuous,
  unbroken hash matches across every transfer, and treat a detected gap
  as reducing (not necessarily eliminating) the evidentiary value of
  the artifact, documented explicitly rather than silently.
- **Post-incident review process failure**: if the same root cause or
  gap appears across multiple post-incident reviews without a completed
  remediation, that is itself a governance failure — feed unresolved
  post-incident findings into the risk register from Chapter 1 with an
  assigned owner, the same discipline applied to any other risk.

## Security and Best Practices

- Pre-delegate containment authority for defined, bounded actions to the
  incident commander role, and document escalation thresholds for
  decisions requiring executive involvement.
- Maintain a tested, pre-negotiated retainer with external incident
  response, forensics, and outside counsel — negotiating these
  relationships for the first time during an active incident costs
  critical response time.
- Build and maintain an out-of-band communication channel, independent
  of primary corporate infrastructure, specifically for use when primary
  systems' integrity is in question.
- Encode playbooks as structured, version-controlled artifacts with
  explicit time targets and owners, consistent with the detection
  engineering discipline in Chapter 6 and the automation practices in
  Chapter 9.
- Hash and log every evidence artifact at collection and every
  subsequent handoff; treat the custody log itself as evidence requiring
  integrity protection.
- Run tabletop exercises at least annually, and after any significant
  architecture change, using scenarios grounded in the organization's
  actual ATT&CK coverage gaps from Chapter 6.
- Feed every post-incident review finding into the risk register from
  Chapter 1 with a named owner, and track remediation to closure rather
  than treating the review document itself as the deliverable.

## References and Knowledge Checks

**References**

- NIST SP 800-61, *Incident Handling Guide*
- NIST SP 800-86, *Guide to Integrating Forensic Techniques into
  Incident Response*
- ISO/IEC 27035, *Information Security Incident Management*
- SANS Institute, *Incident Handler's Handbook*
- CISA, *Federal Government Cybersecurity Incident and Vulnerability
  Response Playbooks*
- Article 33, GDPR — breach notification requirements

**Knowledge Checks**

1. Why are containment, eradication, and recovery treated as one
   combined, iterative phase rather than three strictly sequential
   phases?
2. What is the order-of-volatility principle, and what happens to
   evidence quality when it is violated?
3. Why should decision authority for containment actions be
   pre-delegated rather than requested in real time during an incident?
4. What does chain of custody protect against, and what specifically
   breaks it?
5. From what point does a regulatory breach-notification clock (such as
   GDPR's 72-hour requirement) typically start, and why does that matter
   operationally?
6. What makes a tabletop exercise effective versus a superficial
   walkthrough?

## Hands-On Lab

**Objective:** Build and run a chain-of-custody evidence logging and
integrity-verification workflow, confirming that an unmodified artifact
verifies successfully and a tampered artifact is detected and rejected.

**Prerequisites**

- A workstation with Python 3.11 or later.
- No production evidence-handling systems are involved — this lab uses a
  local sample file to represent a collected artifact.

**Steps**

1. Create a lab directory and a sample "evidence" artifact (representing
   a collected log export or memory image reference file):

   ```bash
   mkdir -p ~/labs/vol10-ch07 && cd ~/labs/vol10-ch07
   echo "sample host memory summary — process list snapshot 2026-07-18T10:00Z" > host-snapshot.txt
   ```

2. Save the `evidence_custody.py` script from the Implementation and
   Automation section into the same directory.

3. Log the initial collection event, establishing the chain-of-custody
   baseline hash:

   ```bash
   python3 evidence_custody.py log EV-2026-0031 host-snapshot.txt "analyst.chen"
   ```

4. **Expected result:** A confirmation line prints showing the evidence
   ID, handler, and a SHA-256 digest, and a `custody_log.csv` file is
   created:

   ```bash
   cat custody_log.csv
   ```

   Output shows one row with `evidence_id=EV-2026-0031`,
   `action=collected`, and the recorded hash.

5. Verify integrity against the unmodified artifact:

   ```bash
   python3 evidence_custody.py verify EV-2026-0031 host-snapshot.txt
   ```

   **Expected result:**
   `Integrity verified: EV-2026-0031 matches original chain-of-custody hash`.

6. **Negative test:** Simulate evidence tampering by modifying the
   artifact after collection, then attempt to verify it again:

   ```bash
   echo "tampered line appended after collection" >> host-snapshot.txt
   python3 evidence_custody.py verify EV-2026-0031 host-snapshot.txt ; echo "exit=$?"
   ```

   **Expected result:** The script exits with an
   `INTEGRITY FAILURE: EV-2026-0031 hash mismatch` message showing the
   expected and actual hashes differ, and a nonzero exit code —
   demonstrating that the custody log detects post-collection tampering
   rather than silently accepting a modified artifact.

7. Restore the artifact to its original state and confirm verification
   succeeds again, illustrating that integrity checking is deterministic
   and reproducible, not a one-time check:

   ```bash
   sed -i.bak '$ d' host-snapshot.txt 2>/dev/null || sed -i '' '$ d' host-snapshot.txt
   python3 evidence_custody.py verify EV-2026-0031 host-snapshot.txt
   ```

   **Expected result:** Integrity verification succeeds again, confirming
   the hash comparison is exact and repeatable.

**Cleanup**

```bash
cd ~ && rm -rf ~/labs/vol10-ch07
```

## Summary and Completion Checklist

This chapter built the incident response and digital evidence discipline
that activates when Chapter 6's detection pipeline confirms a genuine
incident: the four-phase NIST SP 800-61 lifecycle, severity
classification driving response posture, digital forensics fundamentals
(order of volatility, chain of custody, forensically sound collection),
structured playbooks with pre-delegated containment authority, and
tabletop exercises as the mechanism that validates a plan before a real
incident does. The hands-on lab built a working chain-of-custody logging
and integrity-verification tool and proved, with a negative test, that
post-collection tampering is detected rather than silently accepted.

- [ ] I can describe the four phases of the NIST SP 800-61 incident
      response lifecycle and how they relate iteratively.
- [ ] I can design a severity classification model that drives a
      defined response posture.
- [ ] I can explain the order-of-volatility principle and why violating
      it destroys evidence.
- [ ] I can explain why containment authority should be pre-delegated
      rather than requested during an active incident.
- [ ] I can describe what a chain-of-custody log protects against and
      how a gap in it weakens evidentiary value.
- [ ] I built and tested a chain-of-custody integrity verification
      workflow in the hands-on lab, including a negative test for
      tampered evidence.
