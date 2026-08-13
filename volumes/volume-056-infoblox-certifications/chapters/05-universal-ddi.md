# Chapter 05: Universal DDI

## Learning Objectives

- Explain Universal DDI and how it differs from NIOS.
- Navigate the Infoblox Portal and deploy NIOS-X.
- Configure DNS, DHCP, records, views, and zones.
- Design protocol redundancy.
- Complete a walkthrough for each Universal DDI topic.

## Theory and Architecture

**Universal DDI** is Infoblox's cloud-native DDI: a single **Infoblox Portal** (the Cloud
Services Portal) managing on-prem **NIOS-X** hosts and cloud-delivered services, unifying
DNS, DHCP, and IPAM across environments. The microcredential's topic areas: **Portal
navigation**, **deploying NIOS-X**, **DNS and DHCP** services, **resource records, views,
and zones**, and **protocol redundancy**. Universal DDI is managed through the Portal and
its **REST API**, not the NIOS Grid Manager.

## Design Considerations

Universal DDI centralizes management in the **Portal** while running services on
distributed **NIOS-X** hosts. Model **views** and **zones** for split-horizon DNS, and
design **redundancy** (multiple NIOS-X hosts, anycast) so DNS/DHCP survive host loss.

## Implementation and Automation

The labs use the Infoblox Portal API for each Universal DDI topic — hosts, DNS/DHCP,
records/views/zones, and redundancy.

## Validation and Troubleshooting

Confirm the topic areas:

```text
Universal DDI: Portal navigation; deploy NIOS-X; DNS/DHCP; resource records/views/zones;
protocol redundancy. Managed via the Infoblox Portal + its REST API (CSP).
```

Common pitfalls: expecting the **NIOS Grid Manager** (Universal DDI uses the Portal); and
single NIOS-X host (no redundancy).

## Security and Best Practices

Manage from the **Portal**, deploy multiple **NIOS-X** hosts for **redundancy**, use
**views** for split-horizon DNS, secure the Portal **API key**, and apply Portal RBAC.
Keep on-prem and cloud services consistent.

## Hands-On Lab

Per-topic walkthroughs — Universal DDI. **Shared prerequisites** — an Infoblox Portal
tenant and API key (`Authorization: Token <key>`). Commands shown as Portal REST
patterns. **Cost:** none beyond a trial tenant.

### Lab 5.1 — Portal navigation (API auth)

**Objective:** Authenticate to the Infoblox Portal API.

```bash
curl -sS "https://csp.infoblox.com/api/ddi/v1/ipam/address_block" \
  -H "Authorization: Token $CSP_API_KEY" \
  | python3 -c "import sys,json;print('address blocks:',len(json.load(sys.stdin).get('results',[])))"
```

**Expected result:** an authenticated response listing **address blocks** — Portal API
access (the navigation topic, programmatically).

**Negative test:** call the Portal API with a NIOS Grid credential; Universal DDI uses a
**Portal API token** — use the right auth.

**Rollback:** none (read-only).

### Lab 5.2 — Deploy NIOS-X (hosts)

**Objective:** List NIOS-X hosts serving DNS/DHCP.

```bash
curl -sS "https://csp.infoblox.com/api/infra/v1/hosts" -H "Authorization: Token $CSP_API_KEY" \
  | python3 -c "import sys,json;print('NIOS-X hosts:',len(json.load(sys.stdin).get('results',[])))"
```

**Expected result:** the deployed **NIOS-X hosts** — the deployment topic.

**Negative test:** expect services with no host deployed; **deploy NIOS-X** to serve
DNS/DHCP on-prem.

**Rollback:** none (read-only).

### Lab 5.3 — DNS: create a zone

**Objective:** Create an authoritative DNS zone.

```bash
curl -sS -X POST "https://csp.infoblox.com/api/ddi/v1/dns/auth_zone" \
  -H "Authorization: Token $CSP_API_KEY" -H "Content-Type: application/json" \
  -d '{"fqdn":"lab.example.","primary_type":"cloud"}'
```

**Expected result:** a new authoritative **zone `lab.example`** — the DNS/records/zones
topic.

**Negative test:** create records with no parent **zone**; the zone must exist first —
create it.

**Rollback:** `DELETE` the zone by its id.

### Lab 5.4 — DHCP: create a subnet

**Objective:** Create a DHCP-enabled subnet.

```bash
curl -sS -X POST "https://csp.infoblox.com/api/ddi/v1/ipam/subnet" \
  -H "Authorization: Token $CSP_API_KEY" -H "Content-Type: application/json" \
  -d '{"address":"10.20.0.0","cidr":24,"name":"lab-subnet"}'
```

**Expected result:** a new **subnet** for DHCP/IPAM — the DHCP topic.

**Negative test:** overlap the subnet with an existing block; Universal DDI flags the
overlap — keep address space non-overlapping.

**Rollback:** `DELETE` the subnet by its id.

### Lab 5.5 — Protocol redundancy

**Objective:** Describe DNS/DHCP redundancy.

```text
# Redundancy: assign the DNS/DHCP service to MULTIPLE NIOS-X hosts (+ anycast for DNS)
#   so loss of one host does not stop resolution/leasing.
"redundancy: service on >=2 NIOS-X hosts; anycast VIP for DNS"
```

**Expected result:** the multi-host (and anycast) **redundancy** model — the redundancy
topic.

**Negative test:** serve DNS from one host; **redundant hosts** keep resolution alive on
failure — design for it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Universal DDI is Infoblox's cloud-native DDI managed from the Infoblox Portal over NIOS-X
hosts, covering Portal navigation, NIOS-X deployment, DNS/DHCP, records/views/zones, and
protocol redundancy — via the Portal REST API.

- [ ] I can authenticate to and navigate the Portal API.
- [ ] I can list/deploy NIOS-X hosts.
- [ ] I can create zones and subnets.
- [ ] I can design protocol redundancy.
- [ ] I completed Labs 5.1–5.5 including each negative test.
