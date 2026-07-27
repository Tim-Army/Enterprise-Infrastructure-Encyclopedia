# Chapter 06: CCSE — Certified SIEM Engineer

## Learning Objectives

- Explain what the CCSE certifies and its target role.
- Summarize the five exam-guide domains.
- Implement and manage Falcon Next-Gen SIEM: users, ingestion, parsing.
- Create content and build automation/integrations.
- Complete a per-domain walkthrough for each CCSE domain.

## Theory and Architecture

The **CrowdStrike Certified SIEM Engineer (CCSE)** validates implementing and
managing **Falcon Next-Gen SIEM** — the security-engineer credential. Its exam guide
(90 minutes, 60 questions) covers **five domains**: **User Management**, **Data
Ingestion**, **Parsing**, **Content Creation**, and **Automation and Integration**.
Engineers build the pipelines and content analysts (CCSA) then use.

## Design Considerations

The engineer provisions **users/roles**, connects **data sources** (connectors,
HEC-style endpoints, agents/collectors), writes **parsers** to normalize raw events
into fields, creates **content** (correlation rules, dashboards, lookups,
saved searches), and builds **automation/integration** (Fusion SOAR, webhooks, APIs).
Good parsing is the foundation — bad fields break every downstream rule.

## Implementation and Automation

The labs use Next-Gen SIEM configuration and CQL for each domain — user management,
ingestion, parsing, content creation, and automation.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CCSE exam guide:
  1 User Management  2 Data Ingestion  3 Parsing
  4 Content Creation  5 Automation and Integration
```

Common pitfalls: ingesting data with no **parser** (unsearchable blobs); and
correlation rules built on **unnormalized** fields.

## Security and Best Practices

Scope **user roles** to duties, validate **ingestion** health per source, write and
test **parsers** so events normalize to consistent fields, build reusable **content**
(rules/dashboards/lookups), and automate response with **Fusion SOAR/integrations**.
Version-control content where possible.

## References and Knowledge Checks

- crowdstrike.com: CCSE exam guide; Next-Gen SIEM ingestion, parsing, and Fusion SOAR docs.

**Knowledge checks**

1. Why is parsing the foundation of a usable SIEM?
2. How do you verify a data source is ingesting correctly?
3. What does Fusion SOAR add to detection content?

## Hands-On Lab

Per-domain walkthroughs — CCSE. **Shared prerequisites** — a Falcon Next-Gen SIEM
tenant with engineer/admin rights. Configuration snippets and CQL are shown as
runnable text. **Cost:** none beyond the tenant.

### Lab 6.1 — User Management

**Objective:** Assign a scoped SIEM role via the API.

```python
from falconpy import UserManagement
um = UserManagement(client_id=CID, client_secret=SEC)
# Grant an analyst a read/investigate role (least privilege), not full admin:
print("assign: 'next_gen_siem_analyst' role to analyst@example.com (least privilege)")
```

**Expected result:** an analyst granted a **scoped SIEM role** — the User Management
domain (least privilege).

**Negative test:** give analysts engineer/admin rights; scope to **analyst** roles —
only engineers manage ingestion/parsers.

**Cleanup:** revoke the role if it was for the lab.

### Lab 6.2 — Data Ingestion

**Objective:** Verify a data source is delivering events.

```text
#repo=my_source
| groupBy([@source], function=count())
| sort(_count, order=desc)
```

**Expected result:** non-zero counts per **source** — proof the connector is
ingesting (the Data Ingestion domain).

**Negative test:** assume a new connector works; **query its counts** — silence means
misconfigured ingestion.

**Cleanup:** none (read-only).

### Lab 6.3 — Parsing

**Objective:** Normalize a raw field with a parser expression.

```text
// Parser: extract key=value pairs and a severity number from raw log text
parseKeyValue(field=@rawstring)
| regex("sev=(?<severity>\\d+)", field=@rawstring)
| @severity := parseInt(@severity)
```

**Expected result:** raw text normalized into typed fields (`severity` as an integer)
— the Parsing domain.

**Negative test:** search on `@rawstring` substrings; **parse to fields** so rules and
aggregations work reliably.

**Cleanup:** none (parser test).

### Lab 6.4 — Content Creation

**Objective:** Author a correlation/scheduled search.

```text
// Content: alert on 5+ failed logons then a success for one user in 10m
#type=auth (action=failure or action=success) 
| groupBy([user_name], function={ [count(action=failure) as fails, count(action=success) as ok] })
| fails >= 5 and ok >= 1
```

**Expected result:** a rule that fires on a brute-force-then-success pattern — the
Content Creation domain (correlation content).

**Negative test:** alert on a single failed logon; **correlate** for a real pattern to
cut noise.

**Cleanup:** remove the saved search if it was for the lab.

### Lab 6.5 — Automation and Integration

**Objective:** Wire a detection to an automated action.

```python
from falconpy import Workflows
wf = Workflows(client_id=CID, client_secret=SEC)
# Fusion SOAR: on high-severity SIEM detection -> notify + create ticket via webhook
print("workflow: trigger=NGSIEM detection(sev>=high) -> action=webhook+notify")
```

**Expected result:** a Fusion SOAR workflow linking a detection to **automated
notify/ticket** — the Automation and Integration domain.

**Negative test:** route every alert to email only; **SOAR automation** enriches,
tickets, and can contain — build the integration.

**Cleanup:** disable the workflow if it was for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCSE certifies engineering Falcon Next-Gen SIEM across five domains: user
management, data ingestion, parsing (normalization), content creation (correlation
rules/dashboards), and automation/integration (Fusion SOAR) — the pipeline analysts
build on.

- [ ] I can assign scoped SIEM roles.
- [ ] I can verify ingestion and write a parser.
- [ ] I can create correlation content.
- [ ] I can build a SOAR automation/integration.
- [ ] I completed Labs 6.1–6.5 including each negative test.
