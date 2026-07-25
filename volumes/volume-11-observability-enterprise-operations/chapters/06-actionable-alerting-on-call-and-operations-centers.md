# Chapter 06: Actionable Alerting, On-Call, and Operations Centers

![Lab flow for this chapter: three PodUnavailable alerts for different pods on the same node are fired together, and the webhook sink receives a single grouped notification containing all three. As a negative test, a NodeDown alert for that node is fired, then a new PodUnavailable alert for the same node; the count of PodUnavailable notifications after NodeDown fired is zero, inhibited because the matching NodeDown alert shares the node label. Repeating with PodUnavailable on a different node with no active NodeDown confirms that notification is delivered, showing the inhibition correctly scopes to the matching node rather than suppressing globally.](../../../diagrams/volume-11-observability-enterprise-operations/chapter-06-alertmanager-grouping-inhibition-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: Alertmanager grouping three related alerts into one notification, then a node-scoped inhibition rule tested against two different nodes.*

## Learning Objectives

- Apply the actionability test to distinguish a page-worthy alert from
  noise, and explain why symptom-based alerting is generally preferred
  over cause-based alerting.
- Configure Prometheus Alertmanager routing, grouping, inhibition, and
  silencing to control alert volume and correlate related failures.
- Design an on-call rotation and escalation policy that matches paging
  urgency to the service tiering defined in [Chapter 01](01-observability-operating-model-and-service-ownership.md).
- Measure and reduce alert fatigue using quantitative signals (page
  volume, acknowledgment time, false-positive rate).
- Write a runbook that reduces mean time to resolution for a specific,
  recurring alert condition.
- Describe the operating models for centralized operations centers (NOC,
  SOC) and how they interact with service-team on-call.

## Theory and Architecture

### What makes an alert actionable

An alert exists to interrupt a human. Every page has a real cost —
context-switching cost during the day, sleep-disruption cost at night,
and a cumulative trust cost: an on-call engineer who has been paged for
non-actionable noise repeatedly will, predictably and rationally, start
responding to pages more slowly and skeptically, which is the mechanism
by which alert fatigue turns into missed real incidents. An alert
justifies a page only if it passes three tests, adapted from the Google
SRE Workbook's alerting philosophy:

- **Actionable.** There is a specific action a human can take right now
  that changes the outcome. An alert with no available response beyond
  "wait and watch" belongs on a dashboard, not in a page.
- **Urgent.** The action must happen soon, not at the next convenient
  working moment. If the correct response is "file a ticket for next
  sprint," it is not a page.
- **Real.** The underlying condition genuinely reflects degraded user
  experience or imminent risk, not a transient blip that resolves itself
  before a human could act (the multi-window burn-rate design in
  [Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md) exists specifically to filter this case).

### Symptom-based versus cause-based alerting

**Cause-based alerting** fires on an internal signal presumed to
precede a problem: high CPU, a queue depth threshold, a specific error
log pattern. **Symptom-based alerting** fires on user-visible impact
directly: the SLO burn-rate alerts from [Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md) are the canonical
symptom-based alert, because they measure exactly what a user
experiences (successful, timely requests) rather than a proxy for it.

Cause-based alerts are tempting because internal signals are easy to
threshold, but they carry two structural risks: a cause-based threshold
(CPU above 80%) may not actually correlate with user impact for a given
service (a CPU-bound batch job legitimately runs hot with zero user
impact), producing noise; and a genuine user-impacting problem can occur
without tripping any single pre-declared cause-based threshold (a
correctness bug returning fast, wrong `200` responses trips no latency
or CPU alert at all). The enterprise paved-road default should be:
symptom-based, SLO-burn alerts are the primary page-worthy signal for
Tier 0/1 services; cause-based alerts are retained as supporting,
lower-urgency signals (tickets, not pages) that help diagnose *why* once
a symptom-based alert has already fired, and as early-warning signals
for known failure precursors specific to a given system (disk
approaching full, a certificate approaching expiry) where waiting for
user-visible symptom is genuinely too late to act.

### Alertmanager: routing, grouping, inhibition, silencing

Prometheus Alertmanager receives fired alerts from Prometheus rule
evaluation (the burn-rate rules from [Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md), for example) and applies
four distinct mechanisms before any notification is sent:

- **Routing** — a tree of matchers that directs an alert to the correct
  receiver (a specific team's paging integration, a Slack channel, an
  email list) based on its labels, typically `service`, `severity`, and
  `team`.
- **Grouping** — batches multiple alerts that share specified labels
  into a single notification, so a cluster-wide outage that trips the
  same alert across fifty pods produces one page describing fifty
  instances, not fifty separate pages.
- **Inhibition** — suppresses a lower-severity alert when a related
  higher-severity alert is already firing, encoding a known causal or
  hierarchical relationship (a node-down alert inhibits every
  pod-on-that-node alert, since paging separately for each is redundant
  once the root cause is already paged).
- **Silencing** — a time-bounded, manually applied suppression, used
  during planned maintenance or an already-acknowledged, in-progress
  incident, so continued firing of the same alert does not keep
  re-paging.

```yaml
# alertmanager.yaml
route:
  receiver: default-slack
  group_by: [alertname, service]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers:
        - severity="page"
        - service.tier="tier-0"
      receiver: pagerduty-tier0
      group_wait: 10s
      continue: false
    - matchers:
        - severity="page"
      receiver: pagerduty-standard
    - matchers:
        - severity="ticket"
      receiver: ticketing-queue

inhibit_rules:
  - source_matchers: [alertname="NodeDown"]
    target_matchers: [alertname=~"PodUnavailable|PodCrashLooping"]
    equal: [node]

receivers:
  - name: pagerduty-tier0
    pagerduty_configs:
      - routing_key: "<TIER0_INTEGRATION_KEY>"
        severity: critical
  - name: pagerduty-standard
    pagerduty_configs:
      - routing_key: "<STANDARD_INTEGRATION_KEY>"
        severity: warning
  - name: ticketing-queue
    webhook_configs:
      - url: "https://ticketing.internal/api/alertmanager-webhook"
  - name: default-slack
    slack_configs:
      - channel: "#observability-alerts"
```

`group_wait` (how long to wait for additional alerts to join the first
group before sending the initial notification) and `group_interval` (how
long to wait before sending an update to an already-notified group) are
tuning knobs that trade page latency against grouping effectiveness — a
`group_wait` too long delays the first page for a fast-moving incident;
too short, and a rapidly firing multi-instance failure sends several
separate pages before Alertmanager has collected them into one group.

### On-call rotation and escalation design

An on-call rotation assigns accountability for a defined time window
(commonly one week, sometimes split into a primary and secondary
rotation) to a specific person. An escalation policy defines what
happens if the primary does not acknowledge within a target window:
escalate to a secondary, then to a manager, then potentially to a
broader incident-response bridge. Escalation timing should map directly
to the service-tiering acknowledgment targets established in [Chapter 01](01-observability-operating-model-and-service-ownership.md):

| Tier | Ack target | Escalation if unacknowledged |
| --- | --- | --- |
| Tier 0 | 5 minutes | Escalate to secondary at 5 min, to manager at 10 min |
| Tier 1 | 15 minutes | Escalate to secondary at 15 min, to manager at 30 min |
| Tier 2 | Business hours | Escalate to team lead next business day if unactioned |
| Tier 3 | N/A (ticket-based) | No paging escalation |

A rotation schedule should never have a single point of failure: at
minimum a primary and secondary, ideally spanning more than one time zone
for a Tier 0 service with a global user base ("follow-the-sun"
coverage), and with an explicit, tested handoff process rather than an
implicit assumption that the outgoing on-call will informally brief the
incoming one.

### Alert fatigue as a measured, not felt, problem

Alert fatigue is often discussed anecdotally ("on-call feels
exhausting") but should be tracked with quantitative signals so the
platform team can act on trend, not sentiment:

- **Pages per on-call shift**, tracked over time per team; a rising
  trend without a corresponding rise in real incidents is a leading
  indicator of noise creeping into alert rules.
- **Acknowledgment time distribution**; a widening or slowing
  distribution over time, especially for the same alert type
  repeatedly, indicates responders have learned that alert is usually
  safe to deprioritize — a direct, measurable symptom of eroded trust.
- **False-positive rate per alert rule** — the fraction of firings that
  were closed with no action taken or explicitly marked non-actionable.
  A rule with a sustained high false-positive rate should be tuned or
  removed, not tolerated indefinitely because it once caught something
  real.
- **Time-of-day distribution of pages**, since a rule that fires
  disproportionately overnight without corresponding overnight-specific
  real incidents often indicates a threshold miscalibrated against
  legitimate nightly traffic or batch-job patterns rather than a genuine
  overnight risk pattern.

### Operations centers: NOC and SOC

A **Network Operations Center (NOC)** and a **Security Operations Center
(SOC)** are centralized teams staffed to provide continuous (often
24/7) monitoring and first-line response, distinct in scope from the
service-team on-call model described above. A NOC typically owns
infrastructure-layer monitoring (network, data center, and
platform-level health) and first-line triage before escalating to the
owning service team; a SOC (covered in depth in [Volume X](../../volume-10-enterprise-cybersecurity/README.md)) owns security
event monitoring and incident response. The relationship between a NOC
and per-service on-call should be explicit: the NOC is commonly the
first responder for a Tier 0 alert during off-hours, performing initial
triage and confirming genuine impact before paging the owning team's
on-call, reducing false escalations reaching engineers for conditions
resolvable at the NOC's own runbook level (a known-flaky health check, a
scheduled maintenance window not yet silenced). Where no NOC exists, the
service team's own on-call is the first responder directly, and the
Alertmanager routing tree (above) sends pages straight to the owning
team.

## Design Considerations

- **Page-versus-ticket threshold, encoded not assumed.** Every alert
  rule should declare its severity (`page` or `ticket`) explicitly at
  creation, reviewed against the actionable/urgent/real test before
  merge, rather than defaulting new rules to `page` "to be safe" — that
  default is exactly how alert fatigue accumulates over a platform's
  lifetime.
- **Grouping key design.** Group by dimensions that share a likely root
  cause (`service`, `region`, `alertname`) rather than over-grouping
  (grouping only by `alertname` across all services) or under-grouping
  (grouping by every available label, which defeats grouping's purpose
  by producing near-singleton groups again).
- **Follow-the-sun versus single-region on-call.** Follow-the-sun
  coverage avoids overnight paging entirely for a distributed team but
  requires genuinely equivalent operational context and authority in
  every region's rotation, not just warm bodies awake at the right
  hour — a follow-the-sun handoff that loses context between regions
  recreates the single-rotation night-page problem in a different form.
- **Runbook versus tribal knowledge.** A page with no linked runbook
  forces every responder to rediscover the diagnostic and remediation
  steps from scratch, extending time to resolution and increasing the
  chance of an inconsistent or unsafe response under pressure. Treat
  "no runbook" as a blocking gap for any Tier 0/1 alert, not an
  acceptable long-term state.
- **NOC/SOC scope boundary.** Define precisely what a centralized
  operations center is authorized to do unilaterally (acknowledge,
  triage, run a pre-approved runbook step) versus what requires
  escalating to the owning team (any remediation with a meaningful
  blast radius or rollback complexity) before the first real incident
  forces an ad hoc answer under pressure.
- **Cost of the paging platform itself.** Commercial incident-
  management/paging platforms (PagerDuty, Opsgenie) typically price per
  user seat and per integration; align the rotation design and receiver
  routing to avoid unnecessary seats for roles that only need
  read/dashboard access, not full paging-eligible seats.

## Implementation and Automation

Encode escalation policy as a versioned, reviewable configuration rather
than only inside a paging platform's UI, where changes are harder to
audit and diff:

```yaml
# escalation-policies/checkout-api.yaml
service: checkout-api
tier: tier-0
escalation_policy:
  - level: 1
    target: schedule:checkout-api-primary
    acknowledge_within_minutes: 5
  - level: 2
    target: schedule:checkout-api-secondary
    acknowledge_within_minutes: 5
  - level: 3
    target: user:payments-eng-manager
    acknowledge_within_minutes: 10
  - level: 4
    target: process:major-incident-bridge
schedules:
  checkout-api-primary:
    rotation_type: weekly
    handoff_day: monday
    handoff_time: "09:00"
    timezone: America/New_York
    participants:
      - alice@example.com
      - bao@example.com
      - carmen@example.com
```

Apply the same nightly audit discipline from [Chapter 01](01-observability-operating-model-and-service-ownership.md)'s catalog check
to escalation policy completeness, extending that script's pattern to
confirm every Tier 0/1 service in the catalog has a linked, non-empty
escalation policy and schedule:

```bash
#!/usr/bin/env bash
# audit-escalation-coverage.sh — fail CI if a tiered service lacks paging coverage
set -euo pipefail

CATALOG_DIR="${1:-./catalog}"
POLICY_DIR="${2:-./escalation-policies}"
missing=0

for f in "$CATALOG_DIR"/**/catalog-info.yaml; do
  name=$(yq '.metadata.name' "$f")
  tier=$(yq '.metadata.tags[] | select(test("^tier-[01]$"))' "$f")
  [[ -z "$tier" ]] && continue  # only Tier 0/1 require paging coverage

  policy_file="$POLICY_DIR/${name}.yaml"
  if [[ ! -f "$policy_file" ]]; then
    echo "MISSING ESCALATION POLICY: $name ($tier)"
    missing=$((missing + 1))
    continue
  fi
  participant_count=$(yq '.schedules.*.participants | length' "$policy_file")
  if [[ "$participant_count" -lt 2 ]]; then
    echo "SINGLE-POINT-OF-FAILURE ROTATION: $name has fewer than 2 participants"
    missing=$((missing + 1))
  fi
done

echo "Escalation coverage audit complete: $missing issue(s) found"
exit "$missing"
```

A minimal runbook, linked directly from the alert's `annotations.runbook`
field ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)'s generated alert already includes this field) so a
responder reaches it in one click from the page itself:

```markdown
# Runbook: CheckoutAPIAvailabilitySLOPageBurn

## Summary
checkout-api's 30-day availability error budget is burning at a rate
that will exhaust it in under 2 days if sustained.

## Immediate diagnostic steps
1. Open the checkout-api service dashboard and confirm current error
   rate and affected endpoint(s).
2. Check the service dependency map (Chapter 05) for the
   checkout-api -> payment-gateway-adapter edge error rate; this is the
   most common root cause for this specific alert historically.
3. Check recent deploys: `kubectl rollout history deployment/checkout-api -n prod`.

## Common root causes and response
- **Recent deploy correlates with onset** — roll back:
  `kubectl rollout undo deployment/checkout-api -n prod`.
- **Payment gateway edge error rate elevated** — this is an upstream
  dependency issue; open payment-gateway-adapter's own dashboard and
  escalate to that service's on-call per the dependency map.
- **No clear cause after 10 minutes** — declare a major incident per
  Chapter 07's process and engage the incident commander rotation.

## Escalation
If unresolved after 15 minutes, escalate to payments-eng-manager per
the service's escalation policy.
```

## Validation and Troubleshooting

- **Escalation path testing.** Fire a synthetic test alert through the
  full routing tree (a deliberately labeled test alert matched by the
  same route as production Tier 0 alerts, sent to a designated test
  receiver, not a real page) on a scheduled cadence and confirm it
  reaches the expected receiver within the expected `group_wait` window
  — this validates the same routing configuration production alerts
  depend on without paging a real human unnecessarily.
- **Symptom: pages arriving in bursts of near-duplicates.** Check the
  `group_by` labels against the alert's actual label set — a grouping
  key that includes a high-cardinality label (a pod name that differs
  per replica) defeats grouping because each firing instance forms its
  own singleton group. Group by stable, shared labels only.
  Look at `alertmanager_notifications_total` and
  `alertmanager_alerts_received_total` to quantify the burst.
- **Symptom: an inhibition rule is not suppressing the expected
  target.** Confirm the `equal` label list in the inhibition rule
  actually matches between the source and target alerts' label sets —
  inhibition requires an exact match on every label listed in `equal`,
  and a source alert missing one of those labels (for example, `node`
  present on `NodeDown` but absent on a differently-labeled pod alert)
  silently fails to inhibit with no error surfaced.
- **Rising false-positive rate on a specific rule.** Pull the alert's
  firing history alongside its linked incident/ticket resolution
  disposition ([Chapter 07](07-service-management-incident-problem-and-change-operations.md)) for the last quarter; a rule with a
  false-positive rate trending upward is either measuring a signal that
  no longer correlates with real impact (a system changed underneath
  it) or was never symptom-based to begin with and should be converted
  or retired.
- **Runbook drift.** Periodically confirm the runbook linked from a live
  alert still matches the current system (dashboard URLs, deploy
  commands, escalation contacts); a stale runbook followed under
  incident pressure can actively slow resolution, and this should be
  checked on the same review cadence as the alert rule itself, not left
  to be discovered mid-incident.

## Security and Best Practices

- Restrict who can create silences and modify routing/inhibition rules
  in production Alertmanager configuration; an unauthorized silence is a
  realistic way to suppress paging ahead of a planned malicious action,
  echoing the same concern raised for catalog tier downgrades in
  [Chapter 01](01-observability-operating-model-and-service-ownership.md).
- Set an expiration on every silence and alert on any silence approaching
  or exceeding a reasonable maximum duration (for example, a week) —
  an indefinite silence is functionally equivalent to permanently
  disabling an alert and should require the same review as removing the
  alert rule outright.
- Keep paging-platform API keys and webhook secrets in a secrets
  manager, scoped per integration, and rotated on the same schedule as
  other operational credentials ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)); a leaked paging
  integration key can be used to inject fabricated pages or, more
  seriously, to silence real ones.
- Log every acknowledgment, escalation, and silence action with actor
  identity, and review this log periodically — the same audit posture
  applied to the service catalog in [Chapter 01](01-observability-operating-model-and-service-ownership.md) applies directly to the
  paging system, since it is operationally equivalent infrastructure.
- Require a named, individually accountable on-call participant, not a
  shared or generic credential, in every rotation; shared paging
  logins make post-incident review of who actually responded and when
  impossible to reconstruct accurately.

## References and Knowledge Checks

**References**

- [Google, *The Site Reliability Workbook*, Chapter 5 ("Alerting on
  SLOs") and Chapter 6 ("Eliminating Toil"), free online edition.](https://sre.google/workbook/table-of-contents/)
- [Prometheus Alertmanager documentation,
  `prometheus.io/docs/alerting/latest/alertmanager/`, for routing,
  grouping, and inhibition configuration reference.](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [PagerDuty, *Incident Response Documentation*, for escalation policy
  and on-call scheduling patterns referenced in this chapter.](https://response.pagerduty.com/)
- Allspaw, J., "Blameless PostMortems and a Just Culture" (Etsy
  engineering blog), for the cultural foundation [Chapter 07](07-service-management-incident-problem-and-change-operations.md) builds on.

**Knowledge Checks**

1. State the three-part actionability test for a page-worthy alert and
   give an example of an alert that fails each part individually.
2. Explain the structural risk of relying primarily on cause-based
   alerting (CPU, queue depth) rather than symptom-based (SLO burn-rate)
   alerting for a Tier 0 service.
3. Describe the difference between Alertmanager grouping and inhibition,
   and give a scenario where each is the correct mechanism.
4. Why should a new alert rule declare `page` or `ticket` severity
   explicitly at creation rather than defaulting to `page`?
5. What quantitative signals would you track to detect alert fatigue
   before it causes a missed real incident?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each alerting and on-call skill** — alert
rules, Alertmanager routing, actionable-alert design, and on-call/escalation. Labs use Prometheus
Alertmanager. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.4** — Prometheus + Alertmanager, a notification target (a lab
webhook/Slack/email sink), and `curl`. **Cost:** none.

### Lab 6.1 — Alerting rules (Topic: Alert rules)

**Objective:** Define an alert on a symptom.

```yaml
groups:
- name: service-alerts
  rules:
  - alert: CheckoutHighErrorRate
    expr: sum(rate(http_requests_total{service="checkout",status=~"5.."}[5m])) / sum(rate(http_requests_total{service="checkout"}[5m])) > 0.02
    for: 5m
    labels: { severity: page, service: checkout }
    annotations:
      summary: "Checkout error rate > 2% for 5m"
      runbook: "https://runbooks.example.com/checkout-errors"
```

**Expected result:** the alert fires when the *user-facing* error ratio exceeds 2% for 5 minutes,
carrying a severity, service label, and a runbook link — good alerts fire on symptoms users feel
(error ratio, latency), include the context to act, and use `for:` to avoid flapping on brief blips.

**Negative test:** alert on a cause metric (CPU > 80%) instead of a symptom; high CPU may not affect
users while a real user-facing failure at low CPU raises no alert — alert on symptoms, diagnose with
causes.

**Cleanup:** remove the lab rule.

### Lab 6.2 — Alertmanager routing, grouping, and inhibition (Topic: Alert routing)

**Objective:** Route alerts to the right team and suppress noise.

```yaml
route:
  receiver: default
  group_by: [service, severity]
  group_wait: 30s
  group_interval: 5m
  routes:
    - matchers: [ severity="page" ]
      receiver: pagerduty
    - matchers: [ team="payments" ]
      receiver: payments-slack
inhibit_rules:
  - source_matchers: [ severity="page", alertname="ClusterDown" ]
    target_matchers: [ severity=~"page|warning" ]
    equal: [ cluster ]
receivers:
  - { name: default }
  - { name: pagerduty, pagerduty_configs: [{ routing_key: "<key>" }] }
  - { name: payments-slack, slack_configs: [{ channel: "#payments-alerts" }] }
```

**Expected result:** pages go to PagerDuty, team alerts to the team's Slack, related alerts are
grouped into one notification, and a cluster-down alert **inhibits** the flood of downstream alerts
it causes — routing/grouping/inhibition turn a storm of raw alerts into a few actionable
notifications to the right owners.

**Negative test:** send every alert individually to one shared channel with no grouping/inhibition;
a single outage generates hundreds of notifications and the real signal is buried — grouping and
inhibition are what keep alerts actionable during an incident.

**Cleanup:** revert to the lab default config.

### Lab 6.3 — Actionable alerts (Topic: Alert quality)

**Objective:** Make every alert answer "what do I do?"

```text
# Audit each alert against the actionability checklist:
#   - Is it a symptom (user impact), not just a cause? 
#   - Does it require human action now (page) vs. later (ticket) vs. FYI (dashboard only)?
#   - Does it link a runbook and name the owning service/team?
#   - Would a responder know the first step from the alert alone?
# Delete or downgrade any alert that fails these (especially non-actionable "FYI" pages).
```

**Expected result:** every page is a symptom that needs action now and carries a runbook and owner;
non-actionable alerts are downgraded to tickets/dashboards — alert quality (not quantity) is what
prevents alert fatigue; a page that no one can act on is training responders to ignore pages.

**Negative test:** keep alerting on everything "just in case"; responders normalize ignoring alerts
and miss the real one — pruning to actionable, symptom-based alerts is what keeps paging trustworthy.

**Cleanup:** none.

### Lab 6.4 — On-call and escalation design (Topic: On-call)

**Objective:** Design a humane, effective on-call.

```text
# Define the on-call model for the service:
#   - rotation (follow-the-sun or weekly), primary + secondary, and escalation timeouts
#   - what pages a human (SLO-burn/symptom pages only) vs. auto-remediates (Chapter 09)
#   - handoff process, and a page-load budget (e.g. < 2 actionable pages per on-call shift)
#   - blameless expectations and comp/time-off-in-lieu for out-of-hours pages
```

**Expected result:** an on-call design with clear rotation, escalation, a bounded page load, and
blameless, humane practices — on-call is a people system: it must be sustainable (low, actionable
page volume; fair rotation) or responders burn out and reliability suffers.

**Negative test:** run on-call with one person, no secondary/escalation, and dozens of noisy pages a
night; burnout and missed pages follow — a bounded, fairly-rotated, escalation-backed on-call is
what makes it sustainable.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

An alert earns a page only by being actionable, urgent, and real;
symptom-based, SLO-burn alerting ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)) should be the primary
page-worthy signal, with cause-based alerts supporting diagnosis rather
than driving pages directly. Alertmanager's routing, grouping,
inhibition, and silencing mechanisms exist to deliver the right alert to
the right person once, not repeatedly and not to the wrong team.
On-call rotations and escalation policy should map directly to service
tier, and alert fatigue should be tracked quantitatively, not left to
anecdote. [Chapter 07](07-service-management-incident-problem-and-change-operations.md) continues directly from a fired, acknowledged page
into the formal incident, problem, and change management processes that
follow it.

**Completion checklist**

- [ ] Can apply the actionable/urgent/real test to evaluate whether an
      alert should page.
- [ ] Can explain why symptom-based alerting is preferred over
      cause-based alerting for primary paging.
- [ ] Can configure Alertmanager grouping and inhibition and explain the
      difference between them.
- [ ] Can design an escalation policy mapped to service tier with no
      single point of failure in the rotation.
- [ ] Deployed a local Alertmanager pipeline and validated both grouping
      and label-scoped inhibition behavior with a negative test.
