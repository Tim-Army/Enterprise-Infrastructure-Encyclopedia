# Chapter 06: Platform, Virtual Appliances, and Connectivity

## Learning Objectives

- Describe the Identity Security Cloud platform and tenant model.
- Explain the virtual appliance (VA) architecture and why it exists.
- Choose and configure connectors for on-premises and SaaS sources.
- Size VA clusters for resilience and troubleshoot connectivity.

## The platform and the tenant

**Platform** and **Virtual Appliances** are named domains on the Identity Security Administrator exam (and carried into the Engineer exam), because operating ISC means understanding how a SaaS control plane reaches systems that live inside your network.

Identity Security Cloud is multi-tenant SaaS: your **tenant** holds your identities, access model, policies, and configuration, reached through the admin UI and APIs. Nothing about your internal network is exposed to it directly — which raises the obvious question of how the cloud service reads your on-premises Active Directory.

## The virtual appliance

The answer is the **virtual appliance (VA)**: a hardened virtual machine you deploy *inside* your network that acts as the secure bridge between your on-premises systems and the ISC tenant.

The critical architectural property: the VA makes an **outbound** connection to the tenant and polls for work. You do **not** open inbound firewall ports to your identity infrastructure. That single design choice is why the VA exists and is a reliable exam point.

| Property | Detail |
|:---|:---|
| Direction | **Outbound only** — VA initiates to the tenant |
| Placement | Inside the network, with line of sight to the sources it serves |
| Grouping | Deployed in a **cluster**; connectors are assigned to a cluster |
| Resilience | **Multiple VAs per cluster** — one VA is a single point of failure |
| Maintenance | Auto-updating; keep them running and reachable |

Sizing rule of thumb worth internalizing: a cluster with a single VA has no redundancy, and every source assigned to it stops aggregating when that VA is down or updating. Production clusters run at least two.

## Connectors and sources

A **connector** is the driver that speaks a specific system's protocol; a **source** is one configured instance of a connector pointed at one system. Connectivity concerns differ by source type:

| Source type | Reached via | Typical concerns |
|:---|:---|:---|
| **On-premises** (AD, LDAP, database, mainframe) | **VA cluster** | Service account rights, network path, ports, credentials |
| **SaaS** (Salesforce, Workday, ServiceNow) | Direct cloud-to-cloud or VA | API credentials, OAuth, rate limits |
| **Flat file / delimited** | Upload or VA | Schedule, format stability |
| **Custom** | Connector rules / API | Development and maintenance burden |

Each source needs an **account schema** (which fields become account attributes), a **correlation rule** (Chapter 02), and a **service account** with exactly the rights it needs — read for aggregation, write for provisioning. Over-privileging that service account is a common and serious finding: it is a credential that can modify access everywhere.

## Hands-On Lab

Python models the connectivity architecture. **Cost:** none.

### Lab 6.1 — Model VA cluster resilience

**Objective:** Show why a cluster needs more than one VA.

```bash
python3 - <<'EOF'
clusters = {
  "cluster-prod-dc1": {"vas":["va-01","va-02"], "sources":["AD-corp","Oracle-HR","LDAP-legacy"]},
  "cluster-prod-dc2": {"vas":["va-03"],         "sources":["AD-subsidiary","SQL-finance"]},
}
def health(cluster, down):
    up = [v for v in cluster["vas"] if v not in down]
    if not up:
        return "OUTAGE", f"all VAs down -> {len(cluster['sources'])} source(s) stop aggregating"
    if len(up) == 1 and len(cluster["vas"]) == 1:
        return "AT RISK", "single VA: no redundancy — an update or reboot halts aggregation"
    return "HEALTHY", f"{len(up)}/{len(cluster['vas'])} VAs up"

for name, c in clusters.items():
    for down in ([], ["va-01"], ["va-03"]):
        relevant = [d for d in down if d in c["vas"]]
        state, note = health(c, relevant)
        print(f"{name:20} down={relevant or '[]':12} -> {state:8} {note}")
    print()
EOF
```

**Expected result:** `cluster-prod-dc1` survives losing `va-01` (its partner carries the load), while `cluster-prod-dc2` is **AT RISK** even when healthy and goes to full **OUTAGE** when its single VA drops — taking two sources with it. Because VAs auto-update, a single-VA cluster has scheduled outages built in. Redundancy here is not gold-plating; it is the difference between aggregation continuing and identity data going stale.

**Negative test:** Assigning every source to one cluster to "keep it simple" — the blast radius of a single VA cluster failure becomes the entire identity program, and geographically distant sources aggregate over a long network path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Choose the connectivity path per source

**Objective:** Decide VA-mediated vs direct connectivity, and the rights required.

```bash
python3 - <<'EOF'
sources = [
  {"name":"AD-corp",     "location":"on-prem", "provisioning":True,  "protocol":"LDAPS"},
  {"name":"Workday",     "location":"saas",    "provisioning":False, "protocol":"REST/OAuth"},
  {"name":"Salesforce",  "location":"saas",    "provisioning":True,  "protocol":"REST/OAuth"},
  {"name":"Oracle-HR",   "location":"on-prem", "provisioning":False, "protocol":"JDBC"},
]
for s in sources:
    path = "VA cluster (outbound from your network)" if s["location"]=="on-prem" else "direct cloud-to-cloud"
    rights = "read + write (aggregate AND provision)" if s["provisioning"] else "read-only (aggregate only)"
    print(f"{s['name']:12} [{s['location']:7} {s['protocol']:11}] via {path}")
    print(f"{'':12} service account rights: {rights}")
print("\nLeast privilege: a read-only source must NOT have a write-capable service account.")
EOF
```

**Expected result:** On-premises sources route through the VA cluster; SaaS sources connect directly; and each service account gets only the rights its role requires — Workday and Oracle-HR are authoritative *read* sources and never need write access. That last distinction is the security point: the aggregation account for your HR system should be incapable of modifying it.

**Negative test:** Granting Domain Admin to the AD connector service account "so provisioning always works" — you have created a highly privileged credential stored in a connector configuration, which is exactly the credential an attacker targets to grant themselves access everywhere.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Troubleshoot a failing source

**Objective:** Work the connectivity fault tree in order.

```bash
python3 - <<'EOF'
def diagnose(va_reachable, creds_valid, schema_ok, perms_ok):
    if not va_reachable: return "VA offline/unreachable — check the VA VM, its outbound path to the tenant, and cluster health"
    if not creds_valid:  return "Authentication failure — service account password expired or locked"
    if not perms_ok:     return "Permission denied — service account lacks read rights on the target OU/table"
    if not schema_ok:    return "Schema mismatch — an attribute was renamed/removed at the source"
    return "Healthy — aggregation completing"

cases = [
  ("AD-corp",    False, True,  True,  True),
  ("Oracle-HR",  True,  False, True,  True),
  ("LDAP-legacy",True,  True,  True,  False),
  ("SQL-finance",True,  True,  False, True),
]
for name, *state in cases:
    print(f"{name:12} -> {diagnose(*state)}")
print("\nOrder matters: connectivity, then authentication, then authorization, then data.")
EOF
```

**Expected result:** Each fault resolves to one cause, and the closing line states the discipline: work the layers in order — **connectivity → authentication → authorization → data** — instead of guessing. An expired service-account password and an unreachable VA present identically in the UI ("aggregation failed"), so the ordered fault tree is what separates a five-minute fix from an afternoon.

**Negative test:** Starting with the schema because the error mentions attributes — if the VA is down, every source reports errors and none of them are about schema.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Tenant and platform model described.
- [ ] VA architecture explained, including the outbound-only property and cluster redundancy.
- [ ] Connectivity path and least-privilege service-account rights chosen per source type.
- [ ] Connectivity faults diagnosed in layer order.
