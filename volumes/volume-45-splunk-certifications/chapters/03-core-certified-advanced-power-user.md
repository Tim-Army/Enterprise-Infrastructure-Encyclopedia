# Chapter 03: Core Certified Advanced Power User

## Learning Objectives

- Explain what the Advanced Power User certifies and its prerequisite.
- Summarize the blueprint's topic clusters (advanced SPL, acceleration, dashboards).
- Apply advanced SPL: multivalue, subsearches, acceleration, and tuning.
- Build dashboards with forms, tokens, and drilldowns.
- Complete a per-topic walkthrough for each Advanced Power User cluster.

## Theory and Architecture

The **Core Certified Advanced Power User** builds on the Power User with **advanced
SPL** and **dashboarding**. Its blueprint spans 22 fine topics that group into
clusters: advanced `stats`/`eval`, advanced **lookups** (KV Store), advanced
**alerts**, advanced **field creation**, **self-describing data** (`spath`),
advanced **macros**, **acceleration** (report/summary indexing and data-model
acceleration/`tsidx`), **search efficiency and tuning**, **multivalue** fields,
advanced **transactions**, **subsearches**, and **dashboards** (Simple XML,
forms, tokens, drilldowns, performance, and custom visualizations). It requires
the **Power User** first.

## Design Considerations

This exam rewards **efficient, advanced SPL** and **interactive dashboards**.
Learn when acceleration (`tstats`, summary indexing, accelerated data models) is
worth it, how to tune searches (filter early, lispy/`TERM`, streaming vs
transforming commands), and how to build **form-driven dashboards** with tokens
and drilldowns. Multivalue handling and subsearch caveats are common exam themes.

## Implementation and Automation

The labs below cluster the blueprint into runnable SPL and dashboard patterns:
advanced eval/stats, lookups, acceleration/`tstats`, tuning, multivalue,
subsearches, and dashboard tokens/drilldowns.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
splunk.com > Advanced Power User > test blueprint:
  - clusters: advanced SPL, acceleration, search tuning, dashboards (Simple XML)
  - prerequisite: Core Certified Power User
```

Common pitfalls: overusing **subsearches** (they have result/time limits);
forgetting to **accelerate** heavy reporting searches; and building static
dashboards where **tokens/drilldowns** would make them interactive.

## Security and Best Practices

Accelerate heavy reporting with **data models + `tstats`** or summary indexing;
tune searches to filter early and use `TERM`/lispy; keep subsearches small; and
build **form-driven** dashboards so one dashboard serves many questions. These are
both performance best practices and exam content.

## References and Knowledge Checks

- splunk.com: *Advanced Power User* blueprint; SPL Search Reference; Dashboards and Simple XML docs.

**Knowledge checks**

1. When is acceleration (`tstats`/summary indexing) worth using?
2. What are the caveats of subsearches?
3. How do tokens and drilldowns make a dashboard interactive?

## Hands-On Lab

Per-topic walkthroughs — **one lab per Advanced Power User cluster**. Run the SPL
on a Splunk instance.

**Shared prerequisites** — a Splunk instance; the Power User skills from Chapter
02. **Cost:** none (trial).

### Lab 3.1 — Advanced eval and stats

**Objective:** Combine conditional `eval` with multi-function `stats`.

```text
index=_internal | eval sev=if(log_level="ERROR",2,if(log_level="WARN",1,0))
  | stats sum(sev) as sev_score, count by component | sort -sev_score
```

**Expected result:** a severity-weighted score per component — conditional eval
feeding aggregate stats.

**Negative test:** compute severity outside Splunk after export; do it **in SPL**
with `eval` so it scales and stays live.

**Cleanup:** none.

### Lab 3.2 — Advanced lookups (KV Store)

**Objective:** Enrich events with a lookup.

```text
index=_internal | lookup component_owners component OUTPUT owner
  | stats count by owner
```

**Expected result:** event counts by the enriched `owner` field — lookup-based
enrichment (KV Store lookups do this at scale).

**Negative test:** hard-code owner mappings in a giant `case()`; a **lookup** is
maintainable and updatable — externalize the mapping.

**Cleanup:** none.

### Lab 3.3 — Acceleration and `tstats`

**Objective:** Use `tstats` against indexed/accelerated data for speed.

```text
| tstats count where index=_internal by sourcetype
```

**Expected result:** fast counts by sourcetype from the tsidx/accelerated data —
the acceleration technique central to Advanced Power User.

**Negative test:** run a raw `stats` over billions of events for a dashboard
panel; **`tstats`/acceleration** is orders of magnitude faster — use it for
reporting.

**Cleanup:** none.

### Lab 3.4 — Search efficiency and tuning

**Objective:** Filter early and prefer streaming commands.

```text
index=_internal log_level=ERROR component=Metrics | stats count
```

**Expected result:** a fast count because filtering happens **at search time**
before transforms — the tuning principle (filter early, transform late).

**Negative test:** `index=_internal | search log_level=ERROR` (filter after
retrieval); push filters into the base search for speed.

**Cleanup:** none.

### Lab 3.5 — Multivalue fields

**Objective:** Expand and aggregate a multivalue field.

```text
index=_internal | stats values(component) as comps by log_level
  | mvexpand comps | stats count by comps
```

**Expected result:** per-component counts after `mvexpand` — multivalue handling,
a weighted Advanced Power User topic.

**Negative test:** treat a multivalue field as a single string; use `mvexpand`/
`mvindex`/`mvcount` to handle multiple values correctly.

**Cleanup:** none.

### Lab 3.6 — Subsearches (with caveats)

**Objective:** Use a subsearch to filter by another search's results.

```text
index=_internal [ search index=_internal log_level=ERROR | top limit=3 component | fields component ]
  | stats count by component
```

**Expected result:** counts limited to the top-3 error components (from the
subsearch) — subsearch filtering, respecting its result limits.

**Negative test:** return 100k rows from a subsearch; subsearches have **result
and time limits** — keep them small and fast.

**Cleanup:** none.

### Lab 3.7 — Self-describing data with `spath`

**Objective:** Parse JSON/structured data with `spath`.

```text
index=_internal | head 100 | spath | fields data.* | stats count
```

**Expected result:** extracted structured fields from self-describing data —
`spath` parsing (a blueprint topic).

**Negative test:** regex-extract deeply nested JSON by hand; `spath` parses
structured data natively — use it.

**Cleanup:** none.

### Lab 3.8 — Dashboards: tokens and drilldowns

**Objective:** Make a dashboard interactive with a form token.

```xml
<form>
  <fieldset><input type="dropdown" token="lvl"><label>Level</label>
    <choice value="ERROR">ERROR</choice><choice value="WARN">WARN</choice></input></fieldset>
  <row><panel><table>
    <search><query>index=_internal log_level=$lvl$ | stats count by component</query></search>
  </table></panel></row>
</form>
```

**Expected result:** a dropdown that drives the panel's search via the `$lvl$`
token — form-driven, interactive dashboards (a heavily weighted cluster).

**Negative test:** build one static dashboard per level; **tokens** let one
form serve them all — parameterize.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Advanced Power User builds on the Power User with advanced SPL (eval/stats,
lookups, multivalue, subsearches, `spath`), acceleration and search tuning
(`tstats`, summary indexing), and interactive Simple XML dashboards (forms,
tokens, drilldowns). It certifies efficient, advanced search and dashboarding.

- [ ] I can summarize the Advanced Power User blueprint clusters.
- [ ] I can write advanced eval/stats, lookups, and multivalue SPL.
- [ ] I can accelerate with `tstats` and tune searches.
- [ ] I can build a token-driven, drilldown dashboard.
- [ ] I completed Labs 3.1–3.8 including each negative test.
