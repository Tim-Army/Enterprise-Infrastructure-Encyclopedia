# Chapter 08: Integration, Performance Analytics, and Now Assist

## Learning Objectives

- Integrate systems with IntegrationHub and REST/SOAP.
- Measure trends with Performance Analytics.
- Apply Now Assist (GenAI) capabilities responsibly.
- Understand IntegrationHub spokes and the data flow.
- Complete a walkthrough for each integration/analytics/AI topic.

## Theory and Architecture

Three capabilities extend the platform's reach. **IntegrationHub** provides **low-code integration** —
pre-built **spokes** (connectors for Microsoft, Slack, AWS, and hundreds more) and custom REST/SOAP
actions usable directly in **Flow Designer**, so integrations become flow steps rather than scripts.
**Performance Analytics (PA)** turns operational data into **trends over time** — it snapshots
**indicators** (KPIs like average resolution time, open P1 count) on a schedule and visualizes them on
dashboards, answering "are we improving?" (distinct from Reporting, which is point-in-time). **Now
Assist** is ServiceNow's **generative-AI** layer — summarizing incidents, drafting responses,
generating code and flows, and powering the Virtual Agent — governed by **guardrails** (scoped data
access, human review). The theme is turning the platform into a **connected, measured, AI-assisted**
system. Because Now Assist acts on enterprise data, it must be applied **responsibly** (data
governance, human oversight). This chapter teaches each with a hands-on walkthrough (spoke integration,
PA indicators, and responsible Now Assist).

## Design Considerations

Integrate low-code with **IntegrationHub spokes** in Flow Designer; script only when needed. Define
**PA indicators** and snapshot them for **trend** analysis (not just point-in-time reports). Apply
**Now Assist** where it saves time (summaries, drafting) with **human review** and **data governance**.
Protect credentials and scope AI data access.

## Implementation and Automation

The labs use a spoke, define a PA indicator, and apply Now Assist responsibly.

## Validation and Troubleshooting

Confirm the integration/analytics/AI model:

```text
IntegrationHub: low-code spokes (pre-built connectors) + custom REST/SOAP actions in Flow Designer. Performance Analytics: indicators (KPIs) snapshotted over time -> trend dashboards (vs point-in-time Reporting).
Now Assist (GenAI): summarize/draft/generate + Virtual Agent, with guardrails (scoped data + human review).
```

Common pitfalls: **scripting** integrations that a **spoke** already provides; and confusing
point-in-time **Reporting** with trend-based **PA**.

## Security and Best Practices

Integrate with **spokes** (low-code), measure **trends** with PA indicators, and apply **Now Assist**
responsibly (human review, data governance, scoped access). Protect integration credentials. All work
is authorized administration.

## Hands-On Lab

Integration/analytics/AI walkthroughs. **Shared prerequisites** — `python3`, a free PDI. **Cost:**
none.

### Lab 8.1 — Use an IntegrationHub spoke

**Objective:** Low-code integration.

```python
python3 - <<'PY'
flow_step={"action":"Microsoft Teams spoke: Post Message","inputs":{"channel":"#incidents","text":"P1 opened: {{incident.number}}"},
           "used_in":"Flow Designer (no custom REST script)"}
for k,v in flow_step.items(): print(f"{k:9}: {v}")
print("IntegrationHub: drop a pre-built spoke action into a flow (low-code)")
PY
```

**Expected result:** a **spoke** action posting to Teams inside a flow — low-code integration.

**Negative test:** hand-code the Teams REST call when a **spoke** exists; that's more work and less
maintainable — use the spoke.

**Cleanup:** none.

### Lab 8.2 — Define a Performance Analytics indicator

**Objective:** Measure a trend.

```python
python3 - <<'PY'
indicator={"name":"Open P1 incidents","source":"incident (priority=1, active=true)","frequency":"daily snapshot",
           "visualization":"time series on a dashboard","goal":"downward trend"}
for k,v in indicator.items(): print(f"{k:13}: {v}")
print("PA: snapshot an indicator over time -> trend (Reporting is point-in-time)")
PY
```

**Expected result:** a **PA indicator** snapshotted daily for trend analysis — trend measurement.

**Negative test:** use a point-in-time **report** to show improvement over months; you need **PA
snapshots** for trend — use PA.

**Cleanup:** none.

### Lab 8.3 — Apply Now Assist responsibly

**Objective:** Use GenAI with guardrails.

```python
python3 - <<'PY'
use_cases={"summarize a long incident":"Now Assist summary + agent reviews before use",
           "draft a customer reply":"Now Assist draft -> agent edits/approves (human in loop)",
           "generate a flow":"Now Assist scaffolds -> developer reviews/tests"}
guardrails=["scoped data access","human review before action","governance/logging"]
for uc,how in use_cases.items(): print(f"- {uc}: {how}")
print("guardrails:", guardrails)
PY
```

**Expected result:** Now Assist applied with **human review** and **guardrails** — responsible GenAI.

**Negative test:** auto-send AI-drafted customer replies with no review; errors reach customers — keep
a **human in the loop**.

**Cleanup:** none.

### Lab 8.4 — Choose Reporting vs Performance Analytics

**Objective:** Match the tool to the question.

```python
python3 - <<'PY'
questions={"How many P1 are open right now?":"Reporting (point-in-time)",
           "Is average resolution time improving this quarter?":"Performance Analytics (trend)",
           "List today's changes":"Reporting","Are SLA breaches trending down?":"Performance Analytics"}
for q,tool in questions.items(): print(f"- {q}\n    -> {tool}")
PY
```

**Expected result:** each question mapped to **Reporting (now)** or **PA (trend)** — correct tool
choice.

**Negative test:** answer a **trend** question with a point-in-time report; it can't show the trend —
use PA.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

IntegrationHub connects systems low-code with spokes, Performance Analytics measures trends via
snapshotted indicators, and Now Assist adds responsible generative AI with guardrails — a connected,
measured, AI-assisted platform.

- [ ] I can use an IntegrationHub spoke.
- [ ] I can define a Performance Analytics indicator.
- [ ] I can apply Now Assist responsibly.
- [ ] I can choose Reporting vs Performance Analytics.
- [ ] I completed Labs 8.1–8.4 including each negative test.
