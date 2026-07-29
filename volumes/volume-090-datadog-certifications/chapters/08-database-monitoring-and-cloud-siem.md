# Chapter 08: Database Monitoring and Cloud SIEM

## Learning Objectives

- Explain Database Monitoring (query metrics, explain plans, samples).
- Reason about normalized queries and top consumers.
- Explain Cloud SIEM detection rules and signals.
- Triage a security signal (defensively).
- Complete a walkthrough for each DBM-and-SIEM topic.

## Theory and Architecture

Two newer certifications extend Datadog into databases and security. **Database Monitoring (DBM)** gives
query-level visibility into Postgres, MySQL, SQL Server, and Oracle: it collects **normalized query
metrics** (the same query shape aggregated regardless of literal values), **explain plans** (how the
database executes a query), and **query samples**, so you can find the **top consumers** by latency or
executions and see exactly which query and plan are slow — without adding application code. **Cloud SIEM**
is Datadog's **security analytics**: it applies **detection rules** to your ingested logs (cloud,
identity, network, application) to generate **security signals** (mapped to **MITRE ATT&CK**), which
analysts **triage** in the Security Signals explorer, pivoting into the underlying logs. Cloud SIEM is
entirely **defensive** — detecting and investigating threats in **your own** telemetry. This chapter
teaches DBM and Cloud SIEM with hands-on walkthroughs.

## Design Considerations

Enable **DBM** on your databases to find slow queries by their **normalized** shape and read their
**explain plans** before optimizing (index, rewrite). For **Cloud SIEM**, enable the relevant **detection
rules** for your cloud/identity logs, tune them to cut false positives, and map coverage to **MITRE
ATT&CK**. Treat security **signals** as work to triage, and keep the whole workflow defensive on systems
you own.

## Implementation and Automation

The labs reason about DBM query metrics and explain plans, and model a Cloud SIEM detection and signal
triage — the database and security observability these certifications validate.

## Validation and Troubleshooting

Confirm DBM and Cloud SIEM:

```text
DBM: normalized query metrics + explain plans + query samples (Postgres/MySQL/SQL Server/Oracle)
     -> top consumers by latency/executions; optimize the slow query/plan (no app code)
Cloud SIEM: detection rules on ingested logs -> security signals (MITRE ATT&CK) -> triage in explorer
Cloud SIEM is DEFENSIVE: detect + investigate threats in your own telemetry
```

Common pitfalls: optimizing a query from a single sample instead of the **normalized** aggregate; and
enabling SIEM rules without **triaging** the signals they produce.

## Security and Best Practices

DBM observes your own databases; Cloud SIEM **defends** your own environment — detection and
investigation only, no offensive content. Scope database and security access least-privilege. All work is
authorized.

## Hands-On Lab

DBM-and-SIEM walkthroughs. **Shared prerequisites** — DBM enabled on a database (or the concepts,
modeled), Cloud SIEM with ingested logs (or modeled), and `python3`. **Cost:** none.

### Lab 8.1 — Reason about normalized query metrics

**Objective:** Aggregate a query shape.

```python
python3 - <<'PY'
# raw queries differ only by literal; DBM normalizes them to one shape
raw = [
  "SELECT * FROM orders WHERE id = 42",
  "SELECT * FROM orders WHERE id = 99",
  "SELECT * FROM orders WHERE id = 7",
]
normalized = "SELECT * FROM orders WHERE id = ?"
print("normalized:", normalized, "->", len(raw), "executions aggregated")
print("Top consumer view ranks normalized queries by total time/executions")
PY
```

**Expected result:** three literal queries collapsed into one **normalized** shape aggregated for
ranking — the DBM view.

**Negative test:** analyze each literal query separately; DBM **normalizes** so you see the real top
consumer.

**Cleanup:** none.

### Lab 8.2 — Read an explain plan

**Objective:** See why a query is slow.

```python
python3 - <<'PY'
plan = [
  "Seq Scan on orders  (cost=0..18000 rows=1)  <- full table scan",
  "  Filter: (customer_id = ?)",
]
for line in plan: print(line)
print("Diagnosis: Seq Scan on a filtered column -> add an index on customer_id")
PY
```

**Expected result:** an explain plan showing a sequential scan — the fix is an index on the filtered
column.

**Negative test:** guess at the slowness; read the **explain plan** DBM captures to see the scan.

**Cleanup:** none.

### Lab 8.3 — Model a Cloud SIEM detection rule

**Objective:** Detect a threat pattern (defensively).

```python
python3 - <<'PY'
# detection rule: many failed logins then a success from one IP (brute force) -> signal
events = [("failed", 12), ("success", 1)]
failed = dict(events).get("failed", 0)
if failed >= 10 and dict(events).get("success", 0) >= 1:
    print("SIGNAL: possible brute-force success (MITRE T1110) -> severity HIGH")
    print("Triage: scope the source IP + account, investigate session, respond")
PY
```

```text
SIGNAL: possible brute-force success (MITRE T1110) -> severity HIGH
Triage: scope the source IP + account, investigate session, respond
```

**Expected result:** a detection rule that raises a MITRE-mapped signal on a brute-force pattern —
defensive detection.

**Negative test:** alert on a single failed login (noise); a **threshold** rule distinguishes an attack.

**Cleanup:** none.

### Lab 8.4 — Triage a security signal

**Objective:** Investigate defensively.

```python
python3 - <<'PY'
signal = {
  "rule": "brute-force success", "severity": "high", "mitre": "T1110",
  "source_ip": "203.0.113.9", "account": "svc_deploy",
  "pivot": "open underlying logs: auth events + subsequent API calls from this IP/account",
}
for k, v in signal.items(): print(f"{k:10}: {v}")
print("Action: confirm, contain (disable/rotate), and document -- defensive response")
PY
```

**Expected result:** a signal triaged by pivoting to the underlying logs and taking defensive action.

**Negative test:** close signals without investigating the underlying **logs**; pivot into the evidence
and respond.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Database Monitoring gives code-free, query-level visibility — normalized query metrics, explain plans, and
samples to find and fix the slowest queries — while Cloud SIEM applies detection rules to your logs to
raise MITRE-mapped security signals that analysts triage by pivoting into the evidence, a defensive
security-analytics workflow on your own telemetry.

- [ ] I can explain normalized query metrics and top consumers.
- [ ] I can read an explain plan.
- [ ] I can model a Cloud SIEM detection rule.
- [ ] I can triage a security signal defensively.
- [ ] I completed Labs 8.1–8.4 including each negative test.
