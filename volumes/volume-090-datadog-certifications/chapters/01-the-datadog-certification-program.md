# Chapter 01: The Datadog Certification Program

## Learning Objectives

- Describe the Datadog certifications and what each validates.
- Explain the exam format, cost, and retake policy.
- Explain the free Datadog Learning Center.
- Place the certifications against the observability platform.
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

**Datadog** certifications validate skills on the Datadog **observability** platform. Datadog
**relaunched** its certification program on a new learning platform, and the current lineup is:

- **Datadog Fundamentals** — the foundational certification: basic computer fundamentals, infrastructure
  deployment with Datadog, networking and **Datadog Agent** configuration, data collection,
  troubleshooting the Agent, and data visualization.
- **APM & Distributed Tracing Fundamentals** — application performance monitoring: APM fundamentals,
  application instrumentation, insight discovery, visualization, and troubleshooting with APM.
- **Log Management Fundamentals** — logging and log management with Datadog.
- **Database Monitoring Fundamentals** and **Cloud SIEM for AWS Fundamentals** — newer/pilot
  certifications for database observability and security analytics.

Each exam costs **US$100** and has **90 multiple-choice questions**; you may retake, limited to **three
attempts within a 180-day** window from your first attempt. Preparation is **free** through the **Datadog
Learning Center**. This chapter orients you on a free Datadog trial with the **Agent** and API so the
certifications map to real configuration.

## Design Considerations

Start with **Datadog Fundamentals** — it grounds the Agent, metrics, tags, and visualization that every
other exam builds on — then add **APM**, **Log Management**, **Database Monitoring**, or **Cloud SIEM** by
role. Use the free **Learning Center** courses and a **14-day trial** to practice. Plan your **three
attempts** within the 180-day window.

## Implementation and Automation

The labs confirm the Agent status and API access, and map the certification ladder — the orientation
every Datadog candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Datadog Fundamentals: Agent + metrics + tags + visualization (foundation)
APM & Distributed Tracing Fundamentals: instrumentation + traces/spans + troubleshooting
Log Management Fundamentals: logging + log management
Database Monitoring + Cloud SIEM for AWS: newer certifications
Exams: $100; 90 multiple-choice; 3 attempts / 180 days; free Datadog Learning Center prep
```

Common pitfalls: skipping **Datadog Fundamentals** and its Agent/metrics/tags grounding; and burning
attempts — you get **three per 180 days**.

## Security and Best Practices

Datadog certifications validate observing and defending **your own** systems. Protect API and application
keys and scope them least-privilege. The Cloud SIEM path is defensive security operations. All work is
authorized.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a free Datadog trial with the **Agent**
installed, an **API key**, and `python3`. **Cost:** none (14-day trial + free Agent).

### Lab 1.1 — Confirm the Agent is reporting

**Objective:** Verify a working Datadog Agent.

```bash
datadog-agent status | grep -A2 "Agent (v"
```

```text
Agent (v7.55.0)
  Status date: 2026-07-29 12:00:00
  Agent start: 2026-07-29 11:30:00
```

**Expected result:** the Agent version and a recent status — the data source the certifications assume.

**Negative test:** study without a running Agent; the Fundamentals exam is about **Agent** configuration
— install and run it.

**Rollback:** none (read-only).

### Lab 1.2 — Confirm API access

**Objective:** Validate your API key.

```bash
curl -s "https://api.datadoghq.com/api/v1/validate" \
  -H "DD-API-KEY: ${DD_API_KEY}" | python3 -m json.tool
```

```json
{ "valid": true }
```

**Expected result:** `valid: true` — the API key works for programmatic access.

**Negative test:** commit the API key into a repo or script; keep it in an environment variable/secret.

**Rollback:** none (read-only).

### Lab 1.3 — Map the certification ladder

**Objective:** Reason about the certifications.

```python
python3 - <<'PY'
certs = {
  "Datadog Fundamentals":      "Agent + metrics + tags + visualization (start here)",
  "APM & Distributed Tracing": "instrumentation + traces/spans + troubleshooting",
  "Log Management":            "log collection + pipelines + indexes",
  "Database Monitoring":       "query metrics + explain plans",
  "Cloud SIEM for AWS":        "log-based detection + signals (defensive)",
}
for cert, focus in certs.items():
    print(f"{cert:26}: {focus}")
print("Each: $100, 90 MC questions, 3 attempts / 180 days; free Learning Center prep")
PY
```

**Expected result:** the certifications mapped to their focus and the shared exam format.

**Negative test:** treat all Datadog exams as one; each is role-specific — pick the one for your work.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog's relaunched certification program offers Datadog Fundamentals, APM & Distributed Tracing, and Log
Management Fundamentals, plus Database Monitoring and Cloud SIEM — each a $100, 90-question exam with three
attempts per 180 days, free preparation through the Datadog Learning Center, and Fundamentals grounding
the Agent, metrics, tags, and visualization the others build on.

- [ ] I can describe the Datadog certifications.
- [ ] I can explain the exam format, cost, and retake policy.
- [ ] I can explain the free Datadog Learning Center.
- [ ] I completed Labs 1.1–1.3 including each negative test.
