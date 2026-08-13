# Chapter 07: Cybersecurity Defense Engineer and Architect

## Learning Objectives

- Explain the Engineer and Architect credentials and how they extend the Analyst.
- Describe building detections, threat intelligence, and automation/orchestration.
- Design scalable, data-driven security architectures and governance.
- Apply SPL and configuration to engineer and architect a Splunk security practice.
- Complete a per-topic walkthrough for each Engineer and Architect area.

## Theory and Architecture

Two credentials extend the Cybersecurity Defense track beyond analysis:

- **Certified Cybersecurity Defense Engineer** — **builds** the detections: writing
  and tuning **correlation searches**, incorporating **threat intelligence**, and
  developing **automation and orchestration** (SOAR playbooks). It turns analyst
  needs into engineered, repeatable detection and response.
- **Certified Cybersecurity Defense Architect** — **designs** the security
  practice: scalable **security controls**, **data-driven architectures** (data
  onboarding, CIM, ES/data-model design), and **governance** frameworks.

Together with the Analyst (Chapter 06), they cover detect → engineer → architect.

## Design Considerations

The **Engineer** focuses on **detection engineering**: build correlation searches
mapped to ATT&CK, enrich with threat intel, tune for signal, and automate response
with **SOAR**. The **Architect** focuses on the **data and control architecture**:
what to onboard, how to normalize (CIM), how to scale ES, and how governance
(detection lifecycle, content management) keeps the practice healthy. Both build on
the Analyst's detection fluency.

## Implementation and Automation

The labs below cover the Engineer's build tasks (correlation search, threat intel,
SOAR playbook) and the Architect's design tasks (data onboarding/normalization,
ES/data-model architecture, governance).

## Validation and Troubleshooting

Confirm the credentials before studying:

```text
splunk.com > Cybersecurity Defense Engineer / Architect:
  - Engineer: build detections, threat intel, automation/orchestration (SOAR)
  - Architect: scalable controls, data-driven architecture, governance
  - build on the Analyst track
```

Common pitfalls: writing noisy correlation searches (tune for fidelity);
automating response before detections are trustworthy; and architecting ES without
a **data onboarding/CIM** plan.

## Security and Best Practices

Engineer detections mapped to **ATT&CK**, tuned for **fidelity**, and enriched with
**threat intel**; automate only **trustworthy** responses with SOAR (with human
approval for high-impact actions); and architect for **normalized (CIM) data**,
**scalable ES**, and a **detection lifecycle** (develop → test → deploy → tune →
retire) governed as content.

## References and Knowledge Checks

- splunk.com: *Cybersecurity Defense Engineer* and *Architect* blueprints; Enterprise Security and SOAR docs; the CIM.

**Knowledge checks**

1. What does a detection engineer do that an analyst does not?
2. When should a SOAR playbook require human approval?
3. Why is CIM/data onboarding central to security architecture?

## Hands-On Lab

Per-topic walkthroughs — Engineer build tasks and Architect design tasks.

**Shared prerequisites** — a Splunk instance (ES/SOAR optional); SPL from earlier
chapters. **Cost:** none (trial).

### Lab 7.1 — Engineer: build a correlation search

**Objective:** Write a detection suitable for a scheduled correlation search.

```text
| tstats count from datamodel=Authentication where Authentication.action=failure
  by Authentication.src, Authentication.user, _time span=5m
  | where count > 20
  ``` schedule as a correlation search -> creates a notable + risk when triggered ```
```

**Expected result:** a tunable brute-force correlation search — the engineered
detection (schedule it in ES to generate notables/risk).

**Negative test:** ship an untuned detection that fires constantly; **tune**
thresholds and suppression for fidelity before enabling.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Engineer: incorporate threat intelligence

**Objective:** Match events against a threat-intel indicator list.

```text
index=web | lookup threat_intel_ip ip AS src OUTPUT threat_category
  | where isnotnull(threat_category) | stats count by src, threat_category
```

**Expected result:** events matching known-bad IPs enriched with a category —
threat-intel enrichment the Engineer builds into detections.

**Negative test:** hand-maintain IOC lists in searches; use **threat-intel
frameworks/lookups** that update automatically.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Engineer: automation and orchestration (SOAR)

**Objective:** Outline a SOAR playbook for a phishing notable.

```text
Playbook: Phishing Triage
  1. Ingest notable -> extract URL/sender/attachment
  2. Enrich: reputation lookups (URL/IP/hash)
  3. Decision: malicious? -> (auto) quarantine email; (approval) block sender
  4. Respond: create ticket, notify analyst, close or escalate
```

**Expected result:** a playbook with enrichment, a decision gate, and a
human-approval step — the automation/orchestration the Engineer develops.

**Negative test:** auto-remediate every alert without approval; gate **high-impact**
actions behind human review to avoid harmful automation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Architect: data onboarding and normalization

**Objective:** Plan onboarding of a new source to the CIM.

```text
New source: firewall logs
  1. Onboard: input (HEC/forwarder), sourcetype, index
  2. Parse: field extractions (src, dest, action, bytes)
  3. Normalize: map to CIM Network Traffic data model
  4. Validate: `| datamodel Network_Traffic search` returns the new data
```

**Expected result:** a data-onboarding-to-CIM plan — the architecture step that
makes new data usable by ES detections.

**Negative test:** onboard data without CIM mapping; ES detections rely on **CIM**
— normalize on onboarding.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.5 — Architect: scalable ES / data-model design

**Objective:** Design for accelerated data models at scale.

```text
| tstats summariesonly=t count from datamodel=Network_Traffic by All_Traffic.action
  ``` summariesonly leverages acceleration -> fast dashboards/detections at scale ```
```

**Expected result:** an accelerated data-model query pattern — the scalable ES
architecture (accelerated CIM models) the Architect designs.

**Negative test:** run detections against raw data at scale; **accelerated data
models** are what make ES perform — design for them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.6 — Architect: detection governance

**Objective:** Define the detection lifecycle as governed content.

```text
Detection lifecycle: develop -> test (against known data) -> deploy ->
  measure (true/false positive rate) -> tune -> retire when obsolete.
Governance: version control content, map coverage to ATT&CK, review regularly.
```

**Expected result:** a governed detection lifecycle with ATT&CK coverage mapping —
the governance an Architect establishes.

**Negative test:** deploy detections and never review them; govern the **lifecycle**
(measure, tune, retire) so coverage stays effective.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Cybersecurity Defense Engineer builds the detections (correlation searches,
threat intelligence, SOAR automation) and the Architect designs the practice
(scalable data-driven architecture, CIM onboarding, accelerated ES, and detection
governance). Together with the Analyst they span detect → engineer → architect.

- [ ] I can distinguish the Engineer and Architect roles from the Analyst.
- [ ] I can build a tuned correlation search and threat-intel enrichment.
- [ ] I can outline a SOAR playbook with a human-approval gate.
- [ ] I can plan CIM onboarding and govern the detection lifecycle.
- [ ] I completed Labs 7.1–7.6 including each negative test.
