# Chapter 05: CCSA — Certified SIEM Analyst

## Learning Objectives

- Explain what the CCSA certifies and its target role.
- Summarize the four exam-guide domains.
- Query and analyze data in Falcon Next-Gen SIEM with CQL.
- Analyze detection logic, investigate incidents, and report findings.
- Complete a per-domain walkthrough for each CCSA domain.

## Theory and Architecture

The **CrowdStrike Certified SIEM Analyst (CCSA)** validates analyzing data in
**Falcon Next-Gen SIEM** — the SOC/detection-analyst credential. Its exam guide (90
minutes, 60 questions) covers **four domains**: **Querying and Analytics**,
**Detection Logic and Alert Analysis**, **Incident Investigation**, and **Reporting
and Communication**. Analysis uses the **CrowdStrike Query Language (CQL)** over
ingested data.

## Design Considerations

The analyst writes **CQL** to filter, aggregate, and visualize across many data
sources, reads and reasons about **detection logic** (correlation rules) and the
**alerts** they raise, correlates events into **incidents**, and **communicates**
findings clearly (dashboards, summaries). Foundational SIEM experience is assumed.

## Implementation and Automation

The labs use CQL in Next-Gen SIEM for each domain — querying/analytics, detection
logic/alert analysis, incident investigation, and reporting.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CCSA exam guide:
  1 Querying and Analytics  2 Detection Logic and Alert Analysis
  3 Incident Investigation  4 Reporting and Communication
```

Common pitfalls: unfiltered wide queries (slow/costly); and closing alerts without
correlating them into an **incident**.

## Security and Best Practices

Filter **early** in CQL (narrow time/source first), aggregate for signal, understand
the **detection logic** behind each alert, correlate related alerts into a single
**incident**, and **communicate** with clear dashboards/summaries for stakeholders.

## References and Knowledge Checks

- crowdstrike.com: CCSA exam guide; Falcon Next-Gen SIEM and CQL docs.

**Knowledge checks**

1. Why filter early in a CQL pipeline?
2. What is detection logic, and how does it raise alerts?
3. How do you correlate alerts into an incident?

## Hands-On Lab

Per-domain walkthroughs — CCSA. **Shared prerequisites** — a Falcon Next-Gen SIEM
tenant with ingested data. CQL is shown as runnable query text. **Cost:** none beyond
the tenant.

### Lab 5.1 — Querying and Analytics

**Objective:** Aggregate events by source with CQL.

```text
#repo=* 
| groupBy([#type], function=count())
| sort(_count, order=desc)
```

**Expected result:** event counts per data **type/source**, highest first — the
Querying and Analytics domain.

**Negative test:** query `*` with no grouping over all time; **filter and aggregate**
— raw scans are slow and unreadable.

**Rollback:** none (read-only).

### Lab 5.2 — Detection Logic and Alert Analysis

**Objective:** Review recent alerts and their rule logic.

```text
#type=alert
| groupBy([rule_name, severity], function=count())
| sort(_count, order=desc)
```

**Expected result:** alerts grouped by **rule and severity** — the Detection Logic
and Alert Analysis domain (which rules fire and why).

**Negative test:** treat all alerts equally; group by **rule/severity** to prioritize
the meaningful ones.

**Rollback:** none (read-only).

### Lab 5.3 — Incident Investigation

**Objective:** Correlate a user's activity across sources.

```text
#repo=* user_name=?user
| sort(@timestamp)
| table([@timestamp, #type, action, src_ip])
```

**Expected result:** a chronological, cross-source view of one **user's** activity —
the Incident Investigation domain (correlation).

**Negative test:** investigate one log source; **correlate across sources** — the
incident spans endpoint, identity, and network.

**Rollback:** none (read-only).

### Lab 5.4 — Reporting and Communication

**Objective:** Produce a summary suitable for a report.

```text
#type=alert
| timeChart(span=1d, function=count(), series=severity)
```

**Expected result:** a daily alert **trend by severity** for a report/dashboard — the
Reporting and Communication domain.

**Negative test:** paste raw rows into a report; a **timechart/summary** communicates
trend to stakeholders.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCSA certifies analyzing data in Falcon Next-Gen SIEM across four domains:
querying and analytics (CQL), detection logic and alert analysis, incident
investigation (cross-source correlation), and reporting and communication.

- [ ] I can write filtered, aggregated CQL.
- [ ] I can analyze detection logic and alerts.
- [ ] I can correlate activity into an incident.
- [ ] I can produce a report-ready summary.
- [ ] I completed Labs 5.1–5.4 including each negative test.
