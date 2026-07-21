# Chapter 06: Security Telemetry, Detection Engineering, and SOC Operations

![Lab flow for this chapter: detect_credential_stuffing.py flags a user with 8 or more authentication failures followed by a success within a 15-minute window; a user with 8 tightly clustered failures then a success triggers an ALERT, while a user's single clean sign-in does not. As a negative test, a benign dataset with the same user's failures spread across hours produces no alert, and trimming the malicious dataset to exactly 7 failures (one below the threshold) also produces no alert — confirming the rule's tuning correctly distinguishes automated credential stuffing from benign retry behavior without over-firing at the threshold boundary.](../../../diagrams/volume-10-enterprise-cybersecurity/chapter-06-credential-stuffing-detection-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: a credential-stuffing detection rule tuned against benign and threshold-boundary datasets to avoid false positives.*

## Learning Objectives

- Explain the SIEM data pipeline from log collection through
  normalization, correlation, and retention, and how it aggregates the
  telemetry sources introduced in Chapters 2 through 5.
- Apply the detection engineering lifecycle to build, test, tune, and
  retire detection rules as version-controlled artifacts.
- Use the MITRE ATT&CK framework as a shared taxonomy for detection
  coverage mapping, independent of any specific vendor's rule language.
- Design a SOC operating model, including tiered analyst workflow, alert
  triage, and the role of SOAR in automating repetitive response actions.
- Integrate threat intelligence and behavioral analytics (UEBA) as
  enrichment layers rather than standalone detection sources.
- Build and test a working, defensive log-correlation detection rule
  against sample authentication telemetry.

## Theory and Architecture

### Telemetry sources and the SIEM pipeline

Every preceding chapter in this volume produces telemetry that detection
depends on: identity provider sign-in logs and conditional access
decisions ([Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)), EDR process and file-system telemetry ([Chapter 3](03-platform-hardening-configuration-and-endpoint-defense.md)),
NetFlow/IPFIX and IDS/IPS alerts ([Chapter 4](04-network-security-architecture-and-infrastructure-defense.md)), and vulnerability and
exposure state ([Chapter 5](05-vulnerability-exposure-and-patch-risk-management.md)). A **Security Information and Event Management
(SIEM)** platform — or, increasingly, a security data lake with a SIEM
query layer on top — exists to collect, normalize, correlate, and retain
that telemetry so it can be searched and alerted on as a unified body of
evidence rather than as isolated per-tool logs.

The pipeline has four stages:

1. **Collection** — log forwarders, agents, and API-based pull
   integrations gather raw events from every telemetry source.
2. **Normalization** — raw, vendor-specific log formats are mapped to a
   common schema (fields like source IP, destination IP, user, process,
   event outcome share a consistent name across sources), so a single
   detection rule can query across products without per-vendor rewrites.
3. **Correlation** — detection logic evaluates normalized events,
   individually or across multiple events and sources, to identify
   patterns worth an analyst's attention.
4. **Storage and retention** — events are retained for both active
   detection (typically a shorter hot-tier window) and historical
   investigation and compliance (a longer, often cheaper cold-tier
   window), with retention periods aligned to the incident-investigation
   and regulatory timelines in [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md) and [Chapter 8](08-data-security-cryptography-privacy-and-ransomware-resilience.md).

A SIEM that collects everything but normalizes and correlates nothing is
an expensive log archive, not a detection capability — the value is in
stages two through four, not stage one alone.

### Detection engineering as an engineering discipline

**Detection engineering** treats detection logic as software: version-
controlled, tested, peer-reviewed, and measured, rather than accumulated
ad hoc vendor-default rules nobody has reviewed in years. The lifecycle:

1. **Hypothesis** — start from a specific, testable idea ("an adversary
   using a stolen credential would authenticate from a geographically
   improbable location shortly after a legitimate sign-in").
2. **Data source mapping** — confirm the telemetry required to test the
   hypothesis is actually being collected (identity provider sign-in
   logs with geolocation, in this example) — many detection gaps are data
   source gaps, not logic gaps.
3. **Rule authoring** — write the detection logic, ideally in a
   vendor-neutral format that can be translated to the target platform.
4. **Testing** — validate the rule fires on known-true-positive telemetry
   (from a controlled, authorized test — see [Chapter 9](09-security-automation-assurance-threat-hunting-and-lifecycle-operations.md)'s coverage of
   continuous control validation) and does not fire excessively on normal
   baseline traffic.
5. **Tuning** — adjust thresholds and exclusions based on real
   production alert volume and analyst feedback.
6. **Deployment and retirement** — deploy with an owner and a review
   date; retire rules that no longer map to a current threat or that have
   been superseded, rather than letting the rule set grow indefinitely
   with no pruning.

**Sigma** is a widely used, vendor-neutral detection rule format
specifically designed to make this lifecycle portable: a Sigma rule
describes detection logic in a structured, human-readable form that
converts to a specific SIEM's native query language, so detection content
is not locked to a single vendor's syntax.

### MITRE ATT&CK as a shared taxonomy

The **MITRE ATT&CK** Enterprise matrix catalogs adversary tactics
(the "why" — initial access, persistence, privilege escalation) and
techniques (the "how" — specific methods within each tactic), built from
observed real-world intrusions. Its value to a defending organization is
as a **coverage-mapping and gap-analysis tool**: mapping each detection
rule to the ATT&CK technique(s) it covers produces a heatmap showing
which techniques have detection coverage, which have none, and which
techniques are most relevant to the organization's actual threat profile
(informed by industry-specific threat intelligence) but remain uncovered.
This chapter uses ATT&CK strictly as that defensive planning and coverage
tool — the same purpose the security architecture review board in
[Chapter 1](01-cybersecurity-governance-risk-and-architecture.md) uses it for during design review — not as a how-to reference for
performing techniques.

### SOC operating model

A **Security Operations Center (SOC)** is commonly organized in tiers:

| Tier | Role | Typical activity |
| --- | --- | --- |
| Tier 1 | Triage | Initial alert review, enrichment, and disposition (escalate, close as benign, close as false positive) |
| Tier 2 | Investigation | Deeper analysis of escalated alerts, scoping, and initial containment coordination with the incident response process ([Chapter 7](07-cybersecurity-incident-response-and-digital-evidence.md)) |
| Tier 3 | Engineering and hunting | Detection engineering (the lifecycle above), proactive threat hunting ([Chapter 9](09-security-automation-assurance-threat-hunting-and-lifecycle-operations.md)), and complex investigation support |

Organizations vary this model — some flatten Tier 1/2, some fully
outsource Tier 1 to a managed detection and response (MDR) provider while
retaining Tier 2/3 internally, and 24/7 coverage is achieved either with
an internal follow-the-sun model across regions or a hybrid with an
MSSP/MDR covering off-hours. The right model depends on alert volume,
budget, and how much institutional context (internal architecture,
business-criticality of specific systems) is required for accurate
triage — context an external provider structurally has less of.

### Alert triage, SOAR, and alert fatigue

Every alert an analyst reviews consumes finite attention; a detection
rule with a high false-positive rate does not just waste analyst time, it
measurably increases the chance a genuine positive is missed among the
noise — the well-documented alert fatigue problem. Two structural
mitigations:

- **Rigorous tuning** (part of the detection engineering lifecycle above)
  keeps false-positive rates low enough that each alert retains analyst
  attention value.
- **Security Orchestration, Automation, and Response (SOAR)** automates
  the repetitive, well-defined portions of triage — enrichment (looking
  up an IP's reputation, a user's role, an asset's criticality),
  standard containment actions for high-confidence detections, and case
  creation — so Tier 1 analyst time concentrates on judgment calls rather
  than mechanical lookups. SOAR playbooks should include human approval
  gates for any action with meaningful business impact ([Chapter 9](09-security-automation-assurance-threat-hunting-and-lifecycle-operations.md)
  covers this automation-guardrail design consideration further).

### Threat intelligence and UEBA as enrichment

**Threat intelligence** — indicators of compromise (IOCs), adversary
tactics profiles, and sector-specific reporting — is most valuable as an
**enrichment layer** applied to existing telemetry (does this outbound
connection match a known-malicious indicator) rather than as a standalone
detection source; raw IOC feeds without context produce high false-
positive volume if ingested uncritically. **User and Entity Behavior
Analytics (UEBA)** builds a statistical baseline of normal behavior per
user or entity and flags deviations (unusual data-access volume, unusual
login timing) — a complementary detection method to rule-based detection,
particularly effective against insider threats and slow, low-and-slow
compromise activity that never trips a single high-confidence rule.

## Design Considerations

- **Build vs. buy for the SIEM/data platform.** A managed SIEM reduces
  operational burden but constrains query flexibility and can carry
  significant per-gigabyte ingestion cost at enterprise log volumes; a
  self-managed security data lake offers more control and often better
  cost scaling at high volume, but requires dedicated platform
  engineering investment. Total cost of ownership calculations should
  include the detection-engineering and platform-maintenance labor, not
  ingestion licensing cost alone.
- **Retention economics.** Hot-tier (actively queryable, used for
  real-time detection) retention is materially more expensive than
  cold-tier archival retention. Calibrate hot-tier retention to the
  realistic detection and initial-investigation window (often 30–90
  days) and cold-tier retention to the incident-investigation and
  regulatory timelines from [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md) and [Chapter 8](08-data-security-cryptography-privacy-and-ransomware-resilience.md), rather than
  applying one retention period uniformly regardless of cost.
- **Coverage prioritization using ATT&CK.** Building comprehensive
  coverage across all ATT&CK techniques is not a realistic goal for most
  programs. Prioritize coverage for techniques most relevant to the
  organization's actual threat profile and highest-value assets, and
  treat the resulting heatmap as a living planning artifact reviewed
  alongside the risk register in [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md).
- **Alert-to-analyst ratio and staffing.** A SOC with more detection
  rules than analyst capacity to review inevitably develops a growing
  backlog or unreviewed-alert blind spot. Detection engineering
  investment (new rules) and SOC staffing/automation investment
  (capacity to handle the resulting alert volume) must scale together;
  adding detection coverage without adding triage capacity degrades
  overall detection effectiveness even as raw coverage improves.
- **In-house SOC vs. MDR/MSSP trade-off.** External providers bring
  24/7 coverage and cross-customer threat visibility without the
  staffing burden, but have less organizational context and a
  communication-latency cost during a live incident. Many mature
  programs retain internal Tier 2/3 (investigation, engineering, and
  hunting, which most benefit from institutional context) while
  outsourcing Tier 1 or off-hours coverage.
- **UEBA baseline period and false-positive risk during change.**
  Behavioral baselines take time to mature and can generate elevated
  false positives during organizational change (reorganizations, new
  application rollouts, mergers). Plan for a defined baseline-tuning
  period after any significant environmental change rather than expecting
  immediate accuracy.

## Implementation and Automation

### Sigma detection rule (vendor-neutral)

```yaml
# sigma/impossible-travel-sign-in.yml
title: Impossible Travel Following Successful Sign-In
id: 8f3e2b10-2c44-4e9a-9c1e-example000001
status: stable
description: >
  Detects a successful authentication from a geographic location that is
  implausible given a prior successful authentication for the same
  principal within a short time window.
logsource:
  category: authentication
  product: identity_provider
detection:
  prior_signin:
    EventType: SignInSuccess
  current_signin:
    EventType: SignInSuccess
  timeframe: 60m
  condition: prior_signin and current_signin | distance_km > 1000 and travel_time_hours < feasible_travel_hours
level: high
tags:
  - attack.initial_access
  - attack.t1078          # Valid Accounts
falsepositives:
  - Legitimate VPN exit-node change
  - Corporate travel without prior notice to IT
```

### SIEM correlation query (vendor-neutral pseudo-query)

```text
// Detect repeated authentication failures followed by a success,
// a common credential-stuffing / brute-force success pattern
source=identity_provider_signin_logs
| where EventType in ("SignInFailure", "SignInSuccess")
| stats count(SignInFailure) as fail_count,
        max(EventTime) as last_event by UserPrincipal, bin(EventTime, 15m)
| where fail_count >= 8
| join UserPrincipal
    [ source=identity_provider_signin_logs
      | where EventType="SignInSuccess" ]
| eval alert_severity="high"
```

### SOAR playbook for high-confidence containment (human-approval gated)

```yaml
# soar/impossible-travel-response.yaml
trigger: sigma_rule.impossible-travel-sign-in
steps:
  - action: enrich
    lookups:
      - user_risk_score
      - asset_criticality
      - ip_reputation
  - action: notify_analyst
    channel: soc-tier1-queue
    include_enrichment: true
  - action: require_human_approval
    approvers: [soc-tier2-oncall]
    proposed_action: "suspend_session_and_require_reauthentication"
  - action: execute_if_approved
    step: suspend_session_and_require_reauthentication
    target: "{{ trigger.UserPrincipal }}"
  - action: create_case
    system: case-management
    priority: high
```

### Log source onboarding checklist as code

```yaml
# detection-engineering/log-source-onboarding.yaml
log_source: identity_provider_signin
required_fields: [UserPrincipal, EventTime, EventType, SourceIP, GeoLocation]
normalization_mapping_owner: detection-engineering
validated: true
first_seen: "2026-06-01"
review_cadence_days: 180
mapped_detections:
  - impossible-travel-sign-in
  - credential-stuffing-success-pattern
```

## Validation and Troubleshooting

- **Validate detection rules against known-true-positive telemetry
  before trusting them in production.** A rule that has never fired
  against a controlled test event is unproven; use authorized, scoped
  test events ([Chapter 9](09-security-automation-assurance-threat-hunting-and-lifecycle-operations.md) covers continuous control validation and purple
  teaming) to confirm a rule actually detects the pattern it claims to.
- **Common failure: silent log source outage.** A telemetry source that
  stops forwarding events produces no alerts at all — which looks
  identical to "nothing bad is happening." Monitor log source health
  (event volume against an expected baseline) as its own detection
  category, and treat an unexpected drop to zero from a previously
  healthy source as a high-priority finding in itself, following the
  same principle as the EDR agent-silence detection in [Chapter 3](03-platform-hardening-configuration-and-endpoint-defense.md).
- **Common failure: normalization schema drift.** A vendor log format
  change (a field renamed or restructured in a product update) silently
  breaks every detection rule depending on that field, without any error
  — the rule simply stops matching. Version-control the normalization
  mapping alongside the detection rules that depend on it, and validate
  mappings after any source-product upgrade.
- **Common failure: rule review debt.** Detection rules accumulate the
  same way policy exceptions do ([Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)); a rule set that has only
  grown for years without retiring stale rules degrades both performance
  and analyst trust. Require a review date on every deployed rule,
  mirroring the review-cadence pattern used for the control crosswalk in
  [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md).
- **Diagnosing high false-positive rates**: pull the specific alert
  population the rule generated over a representative period and
  characterize the false positives by common attribute (a specific
  business process, a specific asset class) before tuning — an
  undifferentiated threshold increase often just trades false positives
  for false negatives rather than fixing the underlying logic gap.
- **Diagnosing SOAR playbook execution failures**: playbook failures
  frequently trace to a downstream API credential expiring or a target
  system's API contract changing; validate each playbook's integration
  health independently on a schedule, not only when a failure is
  reported by an analyst.

## Security and Best Practices

- Treat the SIEM and detection-engineering repository as Tier 0
  infrastructure ([Chapter 2](02-enterprise-identity-zero-trust-and-privileged-access.md)) — an attacker who can suppress or delete
  detection content operates with reduced risk of discovery for the
  remainder of an intrusion.
- Version-control detection rules and SOAR playbooks with the same
  peer-review discipline as production infrastructure code, and require
  an owner and review date on every deployed rule.
- Require human approval for any automated response action with
  meaningful business impact (session suspension, host isolation,
  account disablement); reserve fully automatic response for narrow,
  extremely high-confidence detections with well-understood blast
  radius.
- Map detection coverage to MITRE ATT&CK and review the resulting
  heatmap against the organization's actual threat profile at least
  annually, prioritizing coverage investment toward the highest-relevance
  gaps rather than pursuing uniform coverage.
- Monitor telemetry source health as a first-class detection category;
  a silent log source is a blind spot indistinguishable from "no
  activity" until it is monitored explicitly.
- Calibrate hot- and cold-tier retention to actual investigative and
  regulatory need ([Chapter 1](01-cybersecurity-governance-risk-and-architecture.md), [Chapter 8](08-data-security-cryptography-privacy-and-ransomware-resilience.md)) rather than either
  over-retaining at high cost or under-retaining and losing
  investigative value.
- Feed confirmed incident findings from [Chapter 7](07-cybersecurity-incident-response-and-digital-evidence.md) back into detection
  engineering as new hypotheses and rules — the detection lifecycle
  should close the loop with the incident response process, not operate
  as a one-way pipeline.

## References and Knowledge Checks

**References**

- [MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)
- [SigmaHQ, *Sigma Detection Rule Specification*](https://github.com/SigmaHQ/sigma-specification)
- [NIST SP 800-92, *Guide to Computer Security Log Management*](https://csrc.nist.gov/pubs/sp/800/92/final)
- [NIST SP 800-137, *Information Security Continuous Monitoring (ISCM)*](https://csrc.nist.gov/pubs/sp/800/137/final)
- [CISA, *Recommended Practices for Security Operations Centers*](https://www.cisa.gov/resources-tools/services/security-operations-center-soc-optimization-advisory-service)
- [FIRST.org, *Traffic Light Protocol (TLP)* for threat intelligence
  handling](https://www.first.org/tlp/)

**Knowledge Checks**

1. What is the difference between log collection and log normalization,
   and why does correlation depend on the latter?
2. Describe the six stages of the detection engineering lifecycle and
   explain why "data source mapping" is a distinct step from "rule
   authoring."
3. How is MITRE ATT&CK used defensively as a coverage-mapping tool
   rather than as attack guidance?
4. Why is a silent log source outage a detection-worthy event in its
   own right?
5. What is the purpose of a human-approval gate in a SOAR playbook, and
   when should one be required?
6. Why is threat intelligence most valuable as an enrichment layer
   rather than a standalone detection source?

## Hands-On Lab

**Objective:** Build and run a defensive log-correlation script that
detects a credential-stuffing / brute-force success pattern (repeated
authentication failures followed by a success) from sample authentication
telemetry, and validate it against both a true-positive and a
benign (negative-test) dataset.

**Prerequisites**

- A workstation with Python 3.11 or later.
- No production SIEM or identity provider access is required — this lab
  uses local sample telemetry files.

**Steps**

1. Create a lab directory:

   ```bash
   mkdir -p ~/labs/vol10-ch06 && cd ~/labs/vol10-ch06
   ```

2. Create sample authentication telemetry representing a credential-
   stuffing success pattern (eight failures followed by a success, for
   the same user, within 15 minutes):

   ```bash
   cat > signin_events.csv << 'EOF'
   user,event_time,event_type,source_ip
   bob@corp.example,2026-07-18T09:00:00Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:05Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:11Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:16Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:22Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:29Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:35Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:41Z,failure,203.0.113.44
   bob@corp.example,2026-07-18T09:00:47Z,success,203.0.113.44
   alice@corp.example,2026-07-18T09:05:00Z,success,198.51.100.20
   EOF
   ```

3. Save the detection script:

   ```bash
   cat > detect_credential_stuffing.py << 'EOF'
   #!/usr/bin/env python3
   """detect_credential_stuffing.py — flag repeated authentication
   failures followed by a success within a 15-minute window, per user.
   """
   import csv
   import sys
   from collections import defaultdict
   from datetime import datetime, timedelta

   FAILURE_THRESHOLD = 8
   WINDOW = timedelta(minutes=15)


   def load_events(path):
       events = defaultdict(list)
       with open(path, newline="", encoding="utf-8") as fh:
           for row in csv.DictReader(fh):
               row["event_time"] = datetime.fromisoformat(
                   row["event_time"].replace("Z", "+00:00"))
               events[row["user"]].append(row)
       return events


   def detect(events):
       findings = []
       for user, rows in events.items():
           rows.sort(key=lambda r: r["event_time"])
           for i, row in enumerate(rows):
               if row["event_type"] != "success":
                   continue
               window_start = row["event_time"] - WINDOW
               failures = [
                   r for r in rows[:i]
                   if r["event_type"] == "failure" and r["event_time"] >= window_start
               ]
               if len(failures) >= FAILURE_THRESHOLD:
                   findings.append({
                       "user": user,
                       "success_time": row["event_time"].isoformat(),
                       "prior_failures": len(failures),
                       "source_ip": row["source_ip"],
                   })
       return findings


   def main(path):
       events = load_events(path)
       findings = detect(events)
       if not findings:
           print("No credential-stuffing success pattern detected.")
           return
       for f in findings:
           print(f"ALERT: {f['user']} succeeded at {f['success_time']} "
                 f"after {f['prior_failures']} failures from {f['source_ip']}")


   if __name__ == "__main__":
       main(sys.argv[1] if len(sys.argv) > 1 else "signin_events.csv")
   EOF
   ```

4. Run the detection script:

   ```bash
   python3 detect_credential_stuffing.py signin_events.csv
   ```

5. **Expected result:** An `ALERT` line prints for `bob@corp.example`
   showing 8 prior failures before the success, and no alert is raised
   for `alice@corp.example`, whose single successful sign-in has no
   preceding failures.

6. **Negative test:** Create a benign dataset with failures spread far
   apart in time (outside the 15-minute window) that should not trigger
   the detection:

   ```bash
   cat > signin_events_benign.csv << 'EOF'
   user,event_time,event_type,source_ip
   carol@corp.example,2026-07-18T08:00:00Z,failure,198.51.100.55
   carol@corp.example,2026-07-18T08:20:00Z,failure,198.51.100.55
   carol@corp.example,2026-07-18T09:10:00Z,success,198.51.100.55
   EOF
   python3 detect_credential_stuffing.py signin_events_benign.csv
   ```

   **Expected result:**
   `No credential-stuffing success pattern detected.` — confirming the
   rule correctly distinguishes a benign, widely spaced retry pattern
   (a plausible forgotten-password scenario) from the tightly clustered
   pattern indicative of automated credential stuffing, avoiding a false
   positive.

7. Confirm the detection threshold is enforced correctly by removing one
   failure event from the malicious dataset (leaving 7) and re-running —
   this represents tuning validation, confirming the rule's boundary
   condition behaves as documented:

   ```bash
   head -8 signin_events.csv > signin_events_below_threshold.csv
   tail -n +10 signin_events.csv >> signin_events_below_threshold.csv
   python3 detect_credential_stuffing.py signin_events_below_threshold.csv
   ```

   **Expected result:** No alert, since only 7 failures precede the
   success — one below `FAILURE_THRESHOLD`.

**Cleanup**

```bash
cd ~ && rm -rf ~/labs/vol10-ch06
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter connected the telemetry produced throughout the volume so
far — identity, endpoint, and network signals — into a SIEM pipeline, and
established detection engineering as a version-controlled, tested
engineering discipline rather than an accumulation of untuned vendor
defaults. MITRE ATT&CK was applied as a defensive coverage-mapping tool,
the tiered SOC operating model and SOAR were introduced as the workflow
and automation layer that turns detections into managed response, and
threat intelligence and UEBA were framed as enrichment rather than
standalone detection. The hands-on lab built and validated a real
log-correlation detection rule, including a negative test proving the
rule distinguishes malicious clustering from benign, widely spaced
authentication failures.

- [ ] I can describe the four stages of the SIEM pipeline: collection,
      normalization, correlation, and retention.
- [ ] I can walk through the detection engineering lifecycle from
      hypothesis to retirement.
- [ ] I can explain how MITRE ATT&CK supports defensive coverage
      mapping.
- [ ] I can describe the tiered SOC model and where SOAR reduces
      analyst toil.
- [ ] I can explain why a silent telemetry source is itself a
      detection-worthy failure mode.
- [ ] I built and validated a log-correlation detection script in the
      hands-on lab, including a negative test against benign telemetry.
