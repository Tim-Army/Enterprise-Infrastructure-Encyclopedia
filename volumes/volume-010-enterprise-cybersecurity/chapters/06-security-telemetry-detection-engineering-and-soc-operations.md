# Chapter 06: Security Telemetry, Detection Engineering, and SOC Operations

![Lab flow for this chapter: detect_credential_stuffing.py flags a user with 8 or more authentication failures followed by a success within a 15-minute window; a user with 8 tightly clustered failures then a success triggers an ALERT, while a user's single clean sign-in does not. As a negative test, a benign dataset with the same user's failures spread across hours produces no alert, and trimming the malicious dataset to exactly 7 failures (one below the threshold) also produces no alert — confirming the rule's tuning correctly distinguishes automated credential stuffing from benign retry behavior without over-firing at the threshold boundary.](../../../diagrams/volume-010-enterprise-cybersecurity/chapter-06-credential-stuffing-detection-flow.svg)

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

This chapter is the **highest-value chapter for CyberOps** — Security Monitoring is the
CCNA Cybersecurity exam's heaviest domain at 25%. It carries a lab for each SOC skill: log
collection and normalization, detection engineering, correlation with MITRE ATT&CK mapping,
and alert triage. Every step is runnable. Each ends **`**Lab verified by:** *pending*`** until
a human runs it.

**Shared prerequisites for Labs 6.1–6.4** — a Linux host with `journalctl`/`jq`/`python3`, and
sample auth logs (`/var/log` or a copied sample). Work in `mkdir -p ~/soc && cd ~/soc`.
**Cost:** none.

### Lab 6.1 — Collect and normalize logs (Topic: Telemetry sources)

**Objective:** Turn raw logs into structured, queryable events.

```bash
cd ~/soc
journalctl -u ssh --since "-1 day" -o json 2>/dev/null | \
  jq -r 'select(.MESSAGE|test("Failed password")) | "\(.__REALTIME_TIMESTAMP) \(.MESSAGE)"' | head || \
  grep "Failed password" /var/log/auth.log 2>/dev/null | head
# Normalize to a common schema (time, source_ip, user, outcome):
grep "Failed password" /var/log/auth.log 2>/dev/null | \
  sed -E 's/.*from ([0-9.]+) .*for (invalid user )?([a-z]+).*/ip=\1 user=\3 outcome=fail/' | head
```

**Expected result:** raw log lines normalized into `ip=… user=… outcome=fail` fields — SOC work
starts with telemetry: collecting logs (auth, network, endpoint) and normalizing them to a common
schema so events from many sources can be searched and correlated together.

**Negative test:** search raw, unnormalized logs from ten different products; each has a different
format and correlation is impossible — normalization to a common schema is what makes cross-source
detection work.

**Rollback:** none (read-only).

### Lab 6.2 — Detection engineering with Sigma (Topic: Detection engineering)

**Objective:** Write a portable detection rule and apply its logic.

```bash
cd ~/soc
cat > brute-force.yml <<'EOF'
title: SSH Brute Force
logsource: {product: linux, service: sshd}
detection:
  selection: {message: "Failed password"}
  timeframe: 5m
  condition: selection | count() by source_ip > 10
level: high
EOF
# Apply the logic against normalized events:
grep "Failed password" /var/log/auth.log 2>/dev/null | \
  grep -oE 'from [0-9.]+' | awk '{print $2}' | sort | uniq -c | awk '$1>10{print "ALERT brute-force from "$2" ("$1" fails)"}'
```

**Expected result:** the Sigma rule expresses "more than 10 SSH failures from one IP in 5
minutes," and the shell applies that logic to flag offending IPs — detection engineering writes
portable, reviewable detections (Sigma → any SIEM) as code, versioned and tested like software
rather than clicked into a console.

**Negative test:** hand-tune one-off searches in a SIEM UI with no saved, version-controlled
rule; the detection is not reviewable, portable, or testable — detection-as-code (Sigma) is what
makes coverage durable and auditable.

**Rollback:** `rm -f ~/soc/brute-force.yml`.

### Lab 6.3 — Correlation and MITRE ATT&CK mapping (Topic: SOC workflow)

**Objective:** Correlate multi-source events and map to attacker techniques.

```bash
cd ~/soc
python3 - <<'EOF'
# Correlate: failed logins THEN a success from the same IP = possible successful brute force
events=[("10.0.0.9","fail"),("10.0.0.9","fail"),("10.0.0.9","fail"),("10.0.0.9","success")]
from collections import defaultdict
seq=defaultdict(list)
for ip,o in events: seq[ip].append(o)
for ip,os in seq.items():
    if os.count("fail")>=3 and "success" in os:
        print(f'CORRELATED: {ip} brute force -> success | ATT&CK T1110 (Brute Force), TA0006 (Credential Access)')
EOF
```

**Expected result:** the correlation flags failures followed by a success from one IP and maps it
to **ATT&CK T1110** — correlation combines events into a story (recon → access → action) that no
single alert tells, and mapping to MITRE ATT&CK gives a shared language for technique coverage and
gaps.

**Negative test:** treat each failed login as an isolated low-severity event; the fail-then-
success pattern (a likely compromise) is missed — correlation across events is what elevates
noise into a real detection.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Alert triage and tuning (Topic: SOC operations)

**Objective:** Enrich an alert and reduce false positives.

```bash
cd ~/soc
python3 - <<'EOF'
alert={"src":"10.0.0.9","rule":"SSH brute force","count":42}
# Enrich: is the source a known scanner/allowlisted admin jump host?
allowlist={"10.0.0.5"}   # admin bastion
verdict = "FALSE POSITIVE (allowlisted bastion)" if alert["src"] in allowlist else "TRUE POSITIVE - escalate/contain"
print(f'{alert["rule"]} from {alert["src"]} ({alert["count"]}x) -> {verdict}')
EOF
```

**Expected result:** the alert is triaged to true/false positive using enrichment (allowlist,
asset context) — SOC operations is a workflow: triage each alert with context, tune out benign
sources to cut false positives, and escalate real ones, so analysts spend time on genuine threats.

**Negative test:** ship noisy detections with no tuning or enrichment; analysts drown in false
positives and miss the real alert (alert fatigue) — enrichment and tuning are what keep the signal
above the noise.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

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
