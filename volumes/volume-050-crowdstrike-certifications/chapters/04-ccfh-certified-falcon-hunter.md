# Chapter 04: CCFH — Certified Falcon Hunter

## Learning Objectives

- Explain what the CCFH certifies and its target role.
- Summarize the seven exam-guide domains.
- Write hunting queries with the CrowdStrike Query Language (CQL).
- Apply hunting analytics and a repeatable methodology.
- Complete a per-domain walkthrough for each CCFH domain.

## Theory and Architecture

The **CrowdStrike Certified Falcon Hunter (CCFH)** validates proactive threat hunting
— the investigative analyst credential. Its exam guide (90 minutes, 60 questions)
covers **seven domains**: **ATT&CK Frameworks**, **Detection Analysis**, **Search and
Investigation Tools**, **Event Search**, **Reports and References**, **Hunting
Analytics**, and **Hunting Methodology**. Hunting centers on the **CrowdStrike Query
Language (CQL)**.

## Design Considerations

The hunter forms **hypotheses** from ATT&CK, queries telemetry with **CQL**
(filtering, aggregation, joins), builds **analytics** (baselines, outliers, stacking/
frequency analysis), uses **investigation tools** and **references** (event
dictionaries), and follows a repeatable **methodology** (hypothesis → hunt →
validate → document → operationalize into detections).

## Implementation and Automation

The labs use CQL and FalconPy for each domain — ATT&CK-driven hunts, detection
analysis, search/investigation tools, event search, references, analytics, and
methodology.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CCFH exam guide:
  1 ATT&CK Frameworks  2 Detection Analysis  3 Search and Investigation Tools
  4 Event Search  5 Reports and References  6 Hunting Analytics  7 Hunting Methodology
```

Common pitfalls: hunting without a **hypothesis**; and one-off hunts that are never
**operationalized** into custom detections.

## Security and Best Practices

Start every hunt from an **ATT&CK-based hypothesis**, use **CQL** aggregation for
outlier/stack analysis, corroborate with **investigation tools**, consult the
**event reference** for field meanings, and **operationalize** confirmed patterns as
custom IOAs/scheduled searches. Document so hunts are repeatable.

## References and Knowledge Checks

- crowdstrike.com: CCFH exam guide; CrowdStrike Query Language (CQL) and event reference docs.

**Knowledge checks**

1. What is a hunting hypothesis, and why start there?
2. How does frequency/stack analysis surface anomalies?
3. How do you operationalize a successful hunt?

## Hands-On Lab

Per-domain walkthroughs — CCFH. **Shared prerequisites** — a Falcon tenant with
Next-Gen SIEM / Advanced event search and the CrowdStrike Query Language. CQL is
shown as runnable query text. **Cost:** none beyond the tenant.

### Lab 4.1 — ATT&CK Frameworks (hypothesis)

**Objective:** Frame a hunt around an ATT&CK technique.

```text
# Hypothesis: adversary uses T1059.001 (PowerShell) for execution.
#event_simpleName=ProcessRollup2 FileName=/powershell\.exe/i
| groupBy([ComputerName], function=count())
```

**Expected result:** hosts running PowerShell, grouped by count — an **ATT&CK-driven**
starting set (the ATT&CK Frameworks domain).

**Negative test:** hunt with no framework anchor; **ATT&CK** gives the hunt a
testable technique — anchor on it.

**Rollback:** none (read-only query).

### Lab 4.2 — Detection Analysis

**Objective:** Correlate a hunt hit with existing detections.

```text
#event_simpleName=/DetectionSummaryEvent/ 
| groupBy([Tactic, Technique], function=count())
| sort(_count, order=desc)
```

**Expected result:** detections grouped by **tactic/technique** — the Detection
Analysis domain (where hunts and detections overlap).

**Negative test:** treat hunts and detections as separate; **correlate** — a hunt hit
that matches a detection confirms the lead.

**Rollback:** none (read-only).

### Lab 4.3 — Search and Investigation Tools

**Objective:** Pivot from a process to its network connections.

```text
#event_simpleName=NetworkConnectIP4 aid=?aid
| table([timestamp, LocalAddressIP4, RemoteAddressIP4, RemotePort])
```

**Expected result:** the host's outbound connections for investigation — the Search
and Investigation Tools domain (pivoting across event types).

**Negative test:** stop at the process; **pivot** to network/file events to see the
full behavior.

**Rollback:** none (read-only).

### Lab 4.4 — Event Search (CQL aggregation)

**Objective:** Aggregate rare parent→child process pairs.

```text
#event_simpleName=ProcessRollup2
| concat([ParentBaseFileName, "->", FileName]) as chain
| groupBy([chain], function=count())
| sort(_count, order=asc)
```

**Expected result:** parent→child chains sorted by rarity (rarest first) — the Event
Search domain (CQL aggregation for outliers).

**Negative test:** scroll raw events; **aggregation** turns millions of rows into a
ranked shortlist.

**Rollback:** none (read-only).

### Lab 4.5 — Reports and References

**Objective:** Use the event reference to interpret a field.

```text
# Reference: event_simpleName=ProcessRollup2 documents fields
#   FileName, CommandLine, ParentBaseFileName, SHA256HashData, ...
#event_simpleName=ProcessRollup2 | select([FileName, SHA256HashData]) | head(5)
```

**Expected result:** correctly interpreted fields (e.g., `SHA256HashData`) from the
**event reference** — the Reports and References domain.

**Negative test:** guess a field's meaning; the **event dictionary/reference** is
authoritative — consult it.

**Rollback:** none (read-only).

### Lab 4.6 — Hunting Analytics (stacking)

**Objective:** Stack service-creation events to find outliers.

```text
#event_simpleName=ServiceStarted
| groupBy([ServiceDisplayName], function=count())
| sort(_count, order=asc)
| head(20)
```

**Expected result:** the 20 rarest services (long-tail outliers) — the Hunting
Analytics domain (frequency/stack analysis).

**Negative test:** look for "known bad" only; **stacking** surfaces the rare-and-
unknown that signatures miss.

**Rollback:** none (read-only).

### Lab 4.7 — Hunting Methodology (operationalize)

**Objective:** Turn a confirmed hunt into a repeatable artifact.

```text
# Methodology: hypothesis -> hunt (CQL) -> validate -> document -> operationalize.
# Save the validated CQL as a scheduled search / custom IOA so it runs continuously.
"operationalized: scheduled search created from validated hunt query"
```

**Expected result:** the validated query saved as a **scheduled search / custom
detection** — the Hunting Methodology domain (closing the loop).

**Negative test:** run the hunt once and move on; **operationalize** it so the
coverage persists.

**Rollback:** remove the scheduled search if it was only for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCFH certifies proactive threat hunting across seven domains: ATT&CK-driven
hypotheses, detection analysis, search/investigation tools, event search (CQL),
reports/references, hunting analytics (stacking), and a repeatable methodology that
operationalizes findings.

- [ ] I can frame a hunt from an ATT&CK technique.
- [ ] I can write CQL aggregation and stacking queries.
- [ ] I can pivot across event types and use the event reference.
- [ ] I can operationalize a confirmed hunt.
- [ ] I completed Labs 4.1–4.7 including each negative test.
