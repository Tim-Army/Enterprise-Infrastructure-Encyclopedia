# Chapter 05: Tenable Security Center

## Learning Objectives

- Describe the Security Center (on-prem) architecture.
- Organize scan data with repositories and scan zones.
- Apply role-based access control and organizations.
- Build Assurance Report Cards and dashboards.
- Complete a walkthrough for each Security Center topic.

## Theory and Architecture

**Tenable Security Center** (formerly Tenable.sc) is the **on-premises** console for organizations
that must keep vulnerability data in their own data center (air-gapped, regulated, or sovereignty
requirements). It manages one or more **Nessus scanners**, stores results in **repositories** (data
stores that can be scoped by network or purpose), and uses **scan zones** to route scans to the right
scanner for a given network segment. Access is governed by **organizations** (tenant boundaries) and
**role-based access control (RBAC)** — users, roles, and groups that limit who sees and does what.
Reporting is rich: **dashboards**, **reports**, and **Assurance Report Cards (ARCs)** that measure
posture against defined policies (e.g., "95% of critical hosts scanned in the last 7 days"). Security
Center delivers the same scanning and prioritization as the cloud VM, but **self-hosted and
self-managed**. This chapter teaches each with a hands-on defensive walkthrough (repository/zone
design, RBAC, and reporting).

## Design Considerations

Design **repositories** by network/purpose and **scan zones** so scans use the nearest scanner.
Enforce **RBAC** and **organizations** for least-privilege, multi-team access. Build **ARCs** to
measure posture against policy. Plan **capacity** (scanner count, data retention). Keep the appliance
**patched and hardened**.

## Implementation and Automation

The labs design repositories/zones, apply RBAC, and build an ARC.

## Validation and Troubleshooting

Confirm the Security Center model:

```text
Security Center = on-prem console (self-hosted). Manages Nessus scanners; repositories (scoped data stores); scan zones (route scans to right scanner).
Access: organizations + RBAC (users/roles/groups). Reporting: dashboards, reports, Assurance Report Cards (ARCs measure posture vs policy).
```

Common pitfalls: one giant **repository** with no scoping (hard to manage/permission); and **flat**
access (everyone sees everything).

## Security and Best Practices

Scope **repositories/zones**, enforce **RBAC/organizations**, measure posture with **ARCs**, plan
capacity, and **harden** the appliance. Retain data per policy. All work is defensive.

## Hands-On Lab

Security Center walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 5.1 — Design repositories and scan zones

**Objective:** Organize scan data and routing.

```python
python3 - <<'PY'
design={"repositories":{"DC-East":"10.10.0.0/16","DC-West":"10.20.0.0/16","DMZ":"203.0.113.0/24"},
        "scan_zones":{"DC-East":"scanner-east","DC-West":"scanner-west","DMZ":"scanner-dmz"}}
for k,v in design.items():
    print(k+":"); [print(f"   {a}: {b}") for a,b in v.items()]
print("Security Center: repositories scope data; zones route scans to the nearest scanner")
PY
```

**Expected result:** repositories and **scan zones** mapped to networks/scanners — organized
Security Center data.

**Negative test:** route all scans through one central scanner across WAN links; slow and fragile —
use **scan zones**.

**Cleanup:** none.

### Lab 5.2 — Apply role-based access control

**Objective:** Least-privilege multi-team access.

```python
python3 - <<'PY'
roles={"Security Manager":["view all","manage scans","reports"],
       "Server Team":["view DC-East repo only","request re-scan"],
       "Auditor":["view dashboards + ARCs (read-only)"]}
for role,perms in roles.items(): print(f"{role:16}: {perms}")
print("Security Center: RBAC + organizations limit visibility to each team's scope")
PY
```

**Expected result:** roles with **scoped, least-privilege** permissions — Security Center RBAC.

**Negative test:** give every user full admin; teams see other teams' data and can change scans —
enforce **RBAC**.

**Cleanup:** none.

### Lab 5.3 — Build an Assurance Report Card

**Objective:** Measure posture against policy.

```python
python3 - <<'PY'
arc=[{"policy":"Critical hosts scanned within 7 days","target":"95%","actual":"92%","status":"FAIL"},
     {"policy":"No unpatched critical > 30 days","target":"100%","actual":"100%","status":"PASS"}]
for a in arc: print(f"[{a['status']}] {a['policy']}: {a['actual']} (target {a['target']})")
print("ARC: red/green posture vs policy for leadership")
PY
```

**Expected result:** an **ARC** showing pass/fail against posture policies — Security Center
reporting.

**Negative test:** report raw scan counts to executives; an **ARC** shows posture against policy —
use it.

**Cleanup:** none.

### Lab 5.4 — Plan on-prem capacity and retention

**Objective:** Size the deployment.

```python
python3 - <<'PY'
plan={"scanners":"one per site + DMZ","data retention":"90 days active + 1yr archive",
      "appliance":"hardened, patched, backed up","HA":"consider redundant console for critical use"}
for k,v in plan.items(): print(f"{k:16}: {v}")
print("Security Center: self-hosted means you own capacity, retention, HA, and hardening")
PY
```

**Expected result:** an on-prem **capacity/retention** plan — self-hosted operational design.

**Negative test:** deploy one scanner for thousands of hosts with no retention plan; scans queue and
data overflows — **size** it properly.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Tenable Security Center is the self-hosted console: repositories and scan zones organize data and
routing, RBAC and organizations scope access, and Assurance Report Cards measure posture against
policy — cloud-VM capability, on-premises.

- [ ] I can design repositories and scan zones.
- [ ] I can apply RBAC.
- [ ] I can build an Assurance Report Card.
- [ ] I can plan capacity and retention.
- [ ] I completed Labs 5.1–5.4 including each negative test.
