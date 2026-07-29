# Chapter 02: Core Certified User and Power User

## Learning Objectives

- Explain the Core User and Power User credentials and their place in the track.
- List the Power User blueprint topic areas and weights.
- Apply foundational and intermediate SPL: search, fields, transforms, and knowledge objects.
- Build the SPL fluency every other Splunk track depends on.
- Complete a per-topic walkthrough for each Core User and Power User area.

## Theory and Architecture

The **Core Certified User** proves foundational Splunk skills — searching, using
fields and time, basic reports, alerts, and dashboards — while the **Core
Certified Power User** adds intermediate **SPL** and **knowledge objects**: field
extractions, aliases and calculated fields, tags and event types, macros,
workflow actions, data models, and the **Common Information Model (CIM)**. The
Power User exam blueprint weights ten topic areas:

| Topic | Weight |
|-------|--------|
| Using Transforming Commands for Visualizations | 5% |
| Filtering and Formatting Results | 10% |
| Correlating Events | 15% |
| Creating and Managing Fields | 10% |
| Creating Field Aliases and Calculated Fields | 10% |
| Creating Tags and Event Types | 10% |
| Creating and Using Macros | 10% |
| Creating and Using Workflow Actions | 10% |
| Creating Data Models | 10% |
| Using the Common Information Model (CIM) Add-On | 10% |

**Correlating Events (15%)** is the heaviest — transactions and `stats`-based
grouping are core Power User skills.

## Design Considerations

These two credentials are the **SPL foundation** of the whole program. Master the
search pipeline (`search | transform | format`), the difference between
**transactions** and **stats** for correlation, and the **knowledge objects**
(fields, aliases, tags, event types, macros, data models) that make data reusable
and normalized. **CIM** matters because the security track depends on
CIM-compliant, normalized data.

## Implementation and Automation

The labs below use **illustrative SPL** you can run on any Splunk instance,
covering the Core User basics and each Power User topic area — transforms,
filtering, correlation, fields, knowledge objects, data models, and CIM.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
splunk.com > Core Certified User / Power User > test blueprint:
  - Power User: ten topic areas (Correlating Events 15% is heaviest)
  - Power User is the prerequisite for Advanced Power User and Admin
```

Common pitfalls: using **transactions** where **stats** is faster (stats scales
better for grouping); forgetting `index=` and a time range; and confusing a
**field alias** (rename) with a **calculated field** (eval-derived).

## Security and Best Practices

Write **efficient SPL**: filter early (`index=`, time, terms), transform late, and
prefer `stats` over `transaction` unless you truly need event grouping. Normalize
data to the **CIM** so it works across apps and the security track. Save reusable
logic as **knowledge objects** (macros, event types) rather than repeating it.

## References and Knowledge Checks

- splunk.com: *Core Certified User* and *Power User* blueprints; SPL Search Reference; the CIM documentation.

**Knowledge checks**

1. Which Power User topic is heaviest, and what does it cover?
2. When should you use `stats` instead of `transaction`?
3. Why does the security track depend on the CIM?

## Hands-On Lab

Per-topic walkthroughs — Core User basics plus **one lab per Power User topic
area**. Run the SPL on a Splunk trial/Cloud instance.

**Shared prerequisites** — a Splunk instance with sample data (or `index=_internal`).
**Cost:** none (trial).

### Lab 2.1 — Core User: search, fields, and time

**Objective:** Run a scoped search and read fields (the User foundation).

```text
index=_internal sourcetype=splunkd | head 20 | table _time, component, log_level
```

**Expected result:** 20 recent `splunkd` events with time, component, and log
level — the scoped search + `table` that Core User certifies.

**Negative test:** search with no `index=` or time range; unscoped searches are
slow and may time out — always scope.

**Cleanup:** none.

### Lab 2.2 — Power User: Transforming Commands for Visualizations (5%)

**Objective:** Use `timechart` to produce a visualization-ready result.

```text
index=_internal | timechart span=1h count by log_level
```

**Expected result:** a time series of event counts per log level — the
transforming command that feeds a chart.

**Negative test:** use `stats count by _time`; `timechart` handles time bucketing
correctly for visualizations — use it for time series.

**Cleanup:** none.

### Lab 2.3 — Power User: Filtering and Formatting Results (10%)

**Objective:** Filter with `where`/`eval` and format output.

```text
index=_internal | eval level=upper(log_level)
  | where level IN ("ERROR","WARN") | stats count by level
```

**Expected result:** counts of ERROR and WARN events — `eval` deriving a field and
`where` filtering on it.

**Negative test:** filter with `search level=ERROR` after `eval`; use `where` for
eval-derived fields — `search` filters raw/indexed fields.

**Cleanup:** none.

### Lab 2.4 — Power User: Correlating Events (15%)

**Objective:** Group related events with `stats` (the preferred correlation).

```text
index=_internal | stats count, values(component) as components by log_level
```

**Expected result:** per-level counts with the components involved — `stats`-based
correlation, Power User's heaviest topic.

**Negative test:** reach for `transaction` first; `stats` is faster and scales —
use `transaction` only when event boundaries/ordering matter.

**Cleanup:** none.

### Lab 2.5 — Power User: Creating and Managing Fields (10%)

**Objective:** Extract a field at search time with `rex`.

```text
index=_internal | rex field=_raw "group=(?<grp>\w+)" | stats count by grp
```

**Expected result:** counts by the extracted `grp` field — search-time field
extraction with `rex` (the Field Extractor does this in the UI).

**Negative test:** assume all fields are pre-extracted; many need **search-time
extraction** — use `rex` or the Field Extractor.

**Cleanup:** none.

### Lab 2.6 — Power User: Field Aliases and Calculated Fields (10%)

**Objective:** Derive a calculated field and alias a field name.

```text
index=_internal | eval size_kb=round(len(_raw)/1024, 2)
  | stats avg(size_kb) as avg_kb by sourcetype
```

**Expected result:** average event size per sourcetype — a calculated field
(`size_kb`); in config, aliases/calculated fields make this permanent and reusable.

**Negative test:** hard-code the calculation in every search; a **calculated
field** (props.conf) computes it automatically — define it once.

**Cleanup:** none.

### Lab 2.7 — Power User: Knowledge Objects — Tags, Event Types, Macros, Workflow Actions (40%)

**Objective:** Reuse logic with an event type and a macro (the reusable knowledge
objects).

```text
| `security_errors`      ``` a macro expanding to: index=_internal log_level=ERROR ```
eventtype=splunkd_error  ``` an event type: a saved search classification ```
```

**Expected result:** a macro and event type standing in for a search — the
reuse mechanisms (tags, event types, macros, workflow actions) that make up 40% of
the Power User exam combined.

**Negative test:** copy-paste the same search everywhere; **macros/event types**
centralize it — change once, apply everywhere.

**Cleanup:** none.

### Lab 2.8 — Power User: Data Models and CIM (20%)

**Objective:** Query a CIM data model with `datamodel`/`tstats`.

```text
| tstats count from datamodel=Authentication where nodename=Authentication by Authentication.action
```

**Expected result:** authentication counts by action from the CIM
**Authentication** data model — accelerated data-model search and CIM
normalization (20% of the exam combined).

**Negative test:** run raw searches across every sourcetype for security data; the
**CIM** normalizes fields so one search works across sources — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Core User and Power User credentials build the SPL foundation of the whole
program: searching and fields (User), then the ten Power User topic areas —
transforms, filtering, correlation, fields, knowledge objects, data models, and
CIM — led by Correlating Events (15%). SPL fluency here underpins every other
Splunk track.

- [ ] I can list the Power User topic areas and their weights.
- [ ] I can search, filter with `where`/`eval`, and transform with `timechart`.
- [ ] I can correlate with `stats` and extract fields with `rex`.
- [ ] I can use knowledge objects and query CIM data models with `tstats`.
- [ ] I completed Labs 2.1–2.8 including each negative test.
