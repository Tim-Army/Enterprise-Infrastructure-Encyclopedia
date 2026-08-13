# Chapter 02: CCFA — Certified Falcon Administrator

## Learning Objectives

- Explain what the CCFA certifies and its target role.
- Summarize the eight exam-guide domains.
- Administer Falcon: RBAC, sensor deployment, host and group management, policy.
- Configure rules, dashboards/reports, and workflows.
- Complete a per-domain walkthrough for each CCFA domain.

## Theory and Architecture

The **CrowdStrike Certified Falcon Administrator (CCFA)** validates administering the
Falcon platform — the foundation credential for anyone with console admin access.
Its exam guide (90 minutes, 60 questions) covers **eight domains**: **User
Management**, **Sensor Deployment**, **Host Management and Setup**, **Group
Creation**, **Policy Application**, **Rules Configuration**, **Dashboards and
Reports**, and **Workflows**. CrowdStrike does not publish domain weights, so prepare
evenly.

## Design Considerations

The administrator builds a clean **RBAC** model, deploys **sensors** across supported
OSes, organizes hosts into **groups** that drive **policy**, tunes **prevention/
sensor-update/containment** policies, authors **detection/exclusion rules**, monitors
via **dashboards/reports**, and automates with **Falcon Fusion workflows**. Group
design is central — groups determine which policies apply.

## Implementation and Automation

The labs use `falconctl` and **FalconPy** for each domain — RBAC, deployment,
host/group management, policy, rules, reporting, and workflows.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CrowdStrike University > CCFA exam guide:
  1 User Management  2 Sensor Deployment  3 Host Management and Setup
  4 Group Creation  5 Policy Application  6 Rules Configuration
  7 Dashboards and Reports  8 Workflows
```

Common pitfalls: over-broad admin roles; hosts in **Reduced Functionality Mode
(RFM)**; and static host groups that miss new endpoints.

## Security and Best Practices

Apply **least-privilege roles**, prefer **dynamic host groups**, stage **sensor
update policies** (N-1/N-2 rings), enable **prevention** appropriate to risk, scope
**exclusions** narrowly, watch **RFM** and inactive sensors, and codify response with
**Fusion workflows**.

## References and Knowledge Checks

- crowdstrike.com: CCFA exam guide; Falcon console administration and FalconPy docs.

**Knowledge checks**

1. How do host groups affect policy application?
2. What is Reduced Functionality Mode (RFM), and how do you find hosts in it?
3. Why stage sensor update policies into rings?

## Hands-On Lab

Per-domain walkthroughs — CCFA. **Shared prerequisites** — a Falcon tenant, an API
client (scopes for Hosts/Host Groups/Prevention Policies/Sensor Download),
`pip install crowdstrike-falconpy`, and `FALCON_CLIENT_ID`/`FALCON_CLIENT_SECRET`
exported. **Cost:** none beyond a licensed/trial tenant.

### Lab 2.1 — User Management (RBAC)

**Objective:** List roles and grants via the API.

```python
from falconpy import UserManagement
um = UserManagement(client_id=CID, client_secret=SEC)
roles = um.get_roles_mssp() if hasattr(um,"get_roles_mssp") else um.get_available_role_ids()
print("role ids:", roles["body"]["resources"][:5])
```

**Expected result:** a list of **role IDs** available in the tenant — the User
Management domain (roles gate console features).

**Negative test:** grant everyone `falcon_administrator`; assign **least-privilege**
roles per job function instead.

**Rollback:** none (read-only).

### Lab 2.2 — Sensor Deployment

**Objective:** Confirm sensor identity and health on a host.

```bash
sudo /opt/CrowdStrike/falconctl -g --cid --aid --version
# CID = customer ID the sensor reports to; AID = this host's agent ID
```

**Expected result:** the **CID**, **AID**, and sensor **version** — proof the sensor
is installed and registered (the Sensor Deployment domain).

**Negative test:** install without setting the CID (`falconctl -s --cid=<CID>`); the
sensor cannot register — set the CID at/after install.

**Rollback:** leave the sensor installed; `falconctl` reads are non-destructive.

### Lab 2.3 — Host Management and Setup (find RFM)

**Objective:** Find hosts in Reduced Functionality Mode.

```python
from falconpy import Hosts
h = Hosts(client_id=CID, client_secret=SEC)
rfm = h.query_devices_by_filter(filter="reduced_functionality_mode:'yes'")
print("RFM host count:", len(rfm["body"]["resources"]))
```

**Expected result:** the **count of RFM hosts** — the Host Management domain (RFM
degrades protection and must be remediated).

**Negative test:** assume all sensors are healthy; **query RFM** — a kernel/OS
mismatch silently drops a host into RFM.

**Rollback:** none (read-only).

### Lab 2.4 — Group Creation

**Objective:** Create a dynamic host group.

```python
from falconpy import HostGroup
hg = HostGroup(client_id=CID, client_secret=SEC)
r = hg.create_host_groups(body={"resources":[{
  "name":"lab-servers","group_type":"dynamic",
  "assignment_rule":"platform_name:'Linux'"}]})
print("group id:", r["body"]["resources"][0]["id"])
```

**Expected result:** a new **dynamic group** auto-including Linux hosts — the Group
Creation domain (groups drive policy).

**Negative test:** use a static group and add hosts by hand; new endpoints are
missed — a **dynamic assignment rule** self-populates.

**Rollback:** `hg.delete_host_groups(ids=[group_id])`.

### Lab 2.5 — Policy Application

**Objective:** Inspect a prevention policy's settings.

```python
from falconpy import PreventionPolicies
pp = PreventionPolicies(client_id=CID, client_secret=SEC)
pol = pp.query_combined_policies(filter="platform_name:'Linux'")
print("policy:", pol["body"]["resources"][0]["name"], "enabled:", pol["body"]["resources"][0]["enabled"])
```

**Expected result:** a prevention policy with its **enabled** state and settings —
the Policy Application domain.

**Negative test:** leave prevention in **Detect-only** in production; set
appropriate **prevention** actions for real protection.

**Rollback:** none (read-only).

### Lab 2.6 — Rules Configuration (exclusions)

**Objective:** List sensor visibility exclusions.

```python
from falconpy import SensorVisibilityExclusions as SVE
sve = SVE(client_id=CID, client_secret=SEC)
ex = sve.query_exclusions()
print("exclusion count:", len(ex["body"]["resources"]))
```

**Expected result:** the count of configured **exclusions** — the Rules
Configuration domain (exclusions and custom IOA/detection rules).

**Negative test:** add a broad `C:\*` exclusion for convenience; scope exclusions
**narrowly** or you blind the sensor.

**Rollback:** none (read-only).

### Lab 2.7 — Dashboards and Reports

**Objective:** Pull a scheduled-report definition.

```python
from falconpy import ReportExecutions
re_api = ReportExecutions(client_id=CID, client_secret=SEC)
rr = re_api.query_reports()
print("report executions:", len(rr["body"]["resources"]))
```

**Expected result:** the list of **report executions** — the Dashboards and Reports
domain (host-management and detection reporting).

**Negative test:** eyeball the console daily; **scheduled reports** deliver metrics
without manual effort.

**Rollback:** none (read-only).

### Lab 2.8 — Workflows (Falcon Fusion)

**Objective:** List automation workflows.

```python
from falconpy import Workflows
wf = Workflows(client_id=CID, client_secret=SEC)
defs = wf.workflow_definitions_search(filter="")
print("workflow defs:", len(defs["body"]["resources"]))
```

**Expected result:** the count of **Fusion workflow definitions** — the Workflows
domain (event-driven automation).

**Negative test:** handle every detection manually; a **Fusion workflow** can
notify/contain automatically on defined triggers.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCFA certifies administering Falcon across eight domains: user management (RBAC),
sensor deployment, host management (including RFM), group creation, policy
application, rules/exclusions, dashboards/reports, and Fusion workflows — using the
console and FalconPy/`falconctl`.

- [ ] I can manage roles with least privilege.
- [ ] I can verify sensor identity and find RFM hosts.
- [ ] I can build dynamic groups that drive policy.
- [ ] I can inspect policies, exclusions, reports, and workflows.
- [ ] I completed Labs 2.1–2.8 including each negative test.
