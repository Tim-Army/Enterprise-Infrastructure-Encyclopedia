# Chapter 08: Certified SIEM Analyst — Elastic Security

## Learning Objectives

- Explain Elastic Security (SIEM) and the detection engine.
- Reason about detection rules and generated alerts.
- Investigate with Timelines and the alerts workflow.
- Hunt threats across security data.
- Complete a walkthrough for each SIEM topic.

## Theory and Architecture

The **Elastic Certified SIEM Analyst** — the one **cognitive** (multiple-choice) exam in the program —
validates **defensive** security operations with **Elastic Security**. Security data (endpoint, network,
cloud, authentication) is normalized to the **Elastic Common Schema (ECS)** and ingested via Elastic
Agent integrations. The **detection engine** runs **detection rules** — prebuilt or custom (query,
threshold, indicator-match/threat-intel, ML, and event-correlation **EQL** rules) — on a schedule and
generates **alerts** with a severity and risk score, mapped to **MITRE ATT&CK**. Analysts triage alerts
in the **Alerts** workflow, pivot into **Timelines** to reconstruct an incident event-by-event, and run
**threat hunts** with KQL/EQL/ES|QL across the data. Everything here is defensive — detecting,
investigating, and responding to threats against **your own** environment. This chapter teaches Elastic
Security with hands-on walkthroughs (detection-rule and hunt queries via the API; triage workflow
modeled).

## Design Considerations

Normalize data to **ECS** so rules and hunts work across sources. Enable the **prebuilt rules** relevant
to your stack and add **custom rules** for your gaps; tune to cut false positives. Map coverage to
**MITRE ATT&CK** to find blind spots. Use **Timelines** for investigation and **exceptions** to suppress
known-good. Keep the whole workflow **defensive** — detection and response on systems you own.

## Implementation and Automation

The labs reason about the detection engine, model a detection rule and its alert, run a hunt query, and
model a Timeline investigation — the defensive SOC work the SIEM Analyst exam validates.

## Validation and Troubleshooting

Confirm the SIEM workflow:

```text
Ingest -> ECS-normalized security data (endpoint/network/cloud/auth)
Detection engine: rules (query/threshold/indicator-match/ML/EQL) -> alerts (severity + MITRE ATT&CK)
Triage: Alerts workflow -> Timeline (reconstruct incident) -> respond
Hunt: KQL / EQL / ES|QL across the data; exceptions suppress known-good
```

Common pitfalls: data not normalized to **ECS** (rules miss it); and alert fatigue from **untuned**
rules — tune and use exceptions.

## Security and Best Practices

This chapter is entirely **defensive**: detecting, investigating, and responding to threats against your
own environment. There is no offensive tradecraft. Scope analyst access with RBAC, protect the SIEM data,
and act only on systems you are authorized to defend. All work is authorized.

## Hands-On Lab

SIEM walkthroughs (defensive). **Shared prerequisites** — an Elastic Stack with Elastic Security and
sample security data (or the concepts, modeled in `python3`), `curl`. **Cost:** none.

### Lab 8.1 — Reason about the detection engine

**Objective:** Map rule types to detections.

```python
python3 - <<'PY'
rules = {
  "Query":            "match a KQL/Lucene condition (e.g., failed logons)",
  "Threshold":        "N events in a window (e.g., 10 failures/5m = brute force)",
  "Indicator match":  "join events to threat-intel indicators (known-bad IPs/hashes)",
  "EQL (correlation)":"ordered event sequences (process spawns network conn)",
  "ML":               "anomaly jobs flag unusual behavior",
}
for kind, use in rules.items():
    print(f"{kind:18}: {use}")
print("Alerts carry severity + risk score, mapped to MITRE ATT&CK (defensive detection)")
PY
```

**Expected result:** the detection-rule types mapped to what each catches — the detection engine.

**Negative test:** rely on a single query rule for everything; combine **threshold, indicator-match, EQL,
and ML** rules for coverage.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Model a threshold detection rule

**Objective:** Detect a brute-force pattern (defensively).

```bash
curl -s -k -u elastic:$PW -X GET "https://localhost:9200/logs-*/_search" -H 'Content-Type: application/json' -d'
{ "size": 0,
  "query": { "match": { "event.outcome": "failure" } },
  "aggs": { "by_user": { "terms": { "field": "user.name", "min_doc_count": 10 },
      "aggs": { "per_15m": { "date_histogram": { "field": "@timestamp", "fixed_interval": "15m" } } } } } }'
```

```json
{ "aggregations": { "by_user": { "buckets": [ { "key": "svc_backup", "doc_count": 47 } ] } } }
```

**Expected result:** a user with many authentication failures — the signal a threshold rule alerts on.

**Negative test:** alert on a single failed login (noise); a **threshold** (e.g., 10 in 15m) distinguishes
a brute-force attempt from a typo.

**Rollback:** none (read-only).

### Lab 8.3 — Run a threat hunt

**Objective:** Search proactively across security data.

```bash
curl -s -k -u elastic:$PW -X POST "https://localhost:9200/_query?format=txt" -H 'Content-Type: application/json' -d'
{ "query": "FROM logs-* | WHERE event.category == \"process\" AND process.name == \"powershell.exe\" AND process.args LIKE \"*-enc*\" | STATS c = COUNT(*) BY host.name | SORT c DESC" }'
```

```text
  c | host.name
----+----------
  4 | WIN-DB01
```

**Expected result:** hosts running encoded-command PowerShell — a hunt lead to investigate (defensively).

**Negative test:** wait only for prebuilt alerts; proactive **hunting** with EQL/ES|QL finds what no rule
fired on yet.

**Rollback:** none (read-only).

### Lab 8.4 — Model a Timeline investigation

**Objective:** Reconstruct an incident.

```python
python3 - <<'PY'
timeline = [
  ("10:01", "auth: failed logons x47 for svc_backup on WIN-DB01"),
  ("10:04", "auth: successful logon svc_backup (credential guessed?)"),
  ("10:06", "process: powershell.exe -enc <base64> spawned"),
  ("10:07", "network: outbound to 203.0.113.9 (unknown)"),
]
for t, e in timeline:
    print(f"{t}: {e}")
print("Timeline reconstructs the chain -> scope, contain, and respond (defensive)")
PY
```

**Expected result:** an event-by-event Timeline linking the brute force to suspicious execution and
egress — the basis for response.

**Negative test:** treat each alert in isolation; a **Timeline** connects them into one incident you can
scope and contain.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Certified SIEM Analyst runs defensive security operations in Elastic Security: ECS-normalized data
feeding a detection engine of query, threshold, indicator-match, EQL, and ML rules that generate
MITRE-mapped alerts, triaged in the Alerts workflow and Timelines and extended with proactive threat
hunting — all on your own environment.

- [ ] I can explain the detection engine and rule types.
- [ ] I can model a threshold detection rule.
- [ ] I can run a threat hunt.
- [ ] I can reconstruct an incident in a Timeline.
- [ ] I completed Labs 8.1–8.4 including each negative test.
