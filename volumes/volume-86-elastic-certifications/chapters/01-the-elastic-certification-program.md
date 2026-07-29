# Chapter 01: The Elastic Certification Program

## Learning Objectives

- Describe the four Elastic certifications and what each validates.
- Distinguish performance-based from cognitive exam formats.
- Explain the 8.15→9.3 version transition and its timing.
- Explain proctoring, cost, and free training.
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

**Elastic** certifications validate skills on the **Elastic Stack** (Elasticsearch, Kibana, Elastic
Agent/Fleet, Beats, Logstash) for search, analytics, observability, and security. The program has four
credentials:

- **Elastic Certified Engineer** — Elasticsearch experts who install and manage clusters and develop
  search solutions. A **hands-on, performance-based, proctored** exam: timed real-world tasks on live
  Elasticsearch clusters, with only the Elastic documentation for reference. **$500 USD**, on-demand.
- **Elastic Certified Analyst** — Kibana experts in data visualization and advanced analysis.
  Performance-based and proctored.
- **Elastic Certified Observability Engineer** — experts who ingest metrics, logs, APM, and uptime data
  and analyze and react to events with Kibana, machine learning, and alerting. Performance-based and
  proctored. **$500 USD**.
- **Elastic Certified SIEM Analyst** — Elastic Security analysts with strong SIEM knowledge. Unlike the
  other three, this is a **cognitive** exam (multiple-choice, select-all, fill-in-the-blank, and
  true/false).

The Engineer exam is currently based on **Elastic 8.15** and updates to **9.3 on 1 September 2026** —
candidates testing in August 2026 take 8.15, and those scheduled near the transition are offered a
reschedule. Elastic offers **free on-demand training** and instructor-led courses; the exams are
delivered online with a remote proctor watching the candidate and screen. This chapter orients you on a
free Elastic Stack (self-managed, Docker, or an Elastic Cloud trial) using the Elasticsearch REST API
and Kibana Dev Tools so the certifications map to real operations.

## Design Considerations

Pick the certification that matches your role — **Engineer** for Elasticsearch/search, **Analyst** for
Kibana analytics, **Observability Engineer** for the observability stack, **SIEM Analyst** for Elastic
Security. Because three of the four are **performance-based**, prepare by **doing** on a live cluster,
not memorizing. Track the **8.15→9.3** transition (new topics: ES|QL, semantic search, RBAC) and study
the current blueprint.

## Implementation and Automation

The labs connect to an Elasticsearch cluster, read its version, and map the certification ladder — the
orientation every Elastic candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Engineer     : Elasticsearch cluster + search dev; performance-based; $500; 8.15 -> 9.3 (1 Sep 2026)
Analyst      : Kibana data viz + analysis; performance-based
Observability: metrics/logs/APM/uptime + ML + alerting; performance-based; $500
SIEM Analyst : Elastic Security; COGNITIVE (MCQ/select-all/fill-blank/true-false)
Delivery: online proctored; Elastic docs allowed on performance exams; free training available
```

Common pitfalls: preparing for a **performance-based** exam by memorizing instead of practicing on a
cluster; and studying the retiring **8.15** topics when you will test on **9.3** after 1 September 2026.

## Security and Best Practices

Elastic certifications validate building on and defending **your own** clusters and data. Secure your lab
cluster (enable security, TLS, RBAC — Chapter 09) even for practice. The SIEM Analyst path is defensive
security operations. All work in this volume is authorized.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a free Elastic Stack (self-managed, Docker,
or an Elastic Cloud trial) reachable at `https://localhost:9200`, `curl`, and `python3`. **Cost:** none
(free tier / trial).

### Lab 1.1 — Read the cluster version

**Objective:** Confirm the Elastic Stack version the exam assumes.

```bash
curl -s -k -u elastic:$PW https://localhost:9200 | python3 -m json.tool
```

```json
{
  "name": "es01",
  "cluster_name": "docker-cluster",
  "version": { "number": "8.15.3", "build_flavor": "default" },
  "tagline": "You Know, for Search"
}
```

**Expected result:** the cluster version (8.15) — the Engineer exam baseline until 9.3 lands 1 September
2026.

**Negative test:** prepare on a very old 7.x cluster; APIs and topics differ — practice on the exam's
current major version.

**Cleanup:** none (read-only).

### Lab 1.2 — Map the certification ladder

**Objective:** Reason about the four credentials and their formats.

```python
python3 - <<'PY'
certs = {
  "Certified Engineer":        "Elasticsearch + search dev — performance-based ($500)",
  "Certified Analyst":         "Kibana data viz + analysis — performance-based",
  "Certified Observability Eng":"metrics/logs/APM/uptime + ML — performance-based ($500)",
  "Certified SIEM Analyst":    "Elastic Security — COGNITIVE (multiple choice)",
}
for cert, detail in certs.items():
    print(f"{cert:28}: {detail}")
print("Three are hands-on; SIEM Analyst is a cognitive exam")
PY
```

**Expected result:** the four certifications mapped to their focus and format.

**Negative test:** expect the **SIEM Analyst** to be hands-on like the others; it is a **cognitive** MCQ
exam — prepare accordingly.

**Cleanup:** none.

### Lab 1.3 — Check cluster health before you begin

**Objective:** Confirm a healthy practice cluster.

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/_cluster/health?pretty"
```

```json
{
  "cluster_name": "docker-cluster",
  "status": "green",
  "number_of_nodes": 1,
  "active_shards_percent_as_number": 100.0
}
```

**Expected result:** a `green` cluster ready for practice — the platform the certifications validate.

**Negative test:** practice on a `red` cluster with unassigned shards; fix health first
(`_cluster/allocation/explain`) — a broken cluster blocks the labs.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Elastic offers four certifications on the Elastic Stack: the performance-based Certified Engineer
(Elasticsearch/search), Certified Analyst (Kibana), and Observability Engineer (metrics/logs/APM/uptime),
plus the cognitive SIEM Analyst (Elastic Security). The Engineer exam moves from 8.15 to 9.3 on
1 September 2026; exams are online-proctored with free training available.

- [ ] I can describe the four certifications and what each validates.
- [ ] I can distinguish performance-based from cognitive formats.
- [ ] I can explain the 8.15→9.3 transition.
- [ ] I completed Labs 1.1–1.3 including each negative test.
