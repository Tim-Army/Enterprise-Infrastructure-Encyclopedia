# Chapter 03: INA — NIOS DDI Administrator

## Learning Objectives

- Explain what the INA certifies and its target role.
- Summarize the administrator topic areas.
- Manage Grid members and advanced DHCP/DNS.
- Configure Discovery, access control, and remote authentication.
- Complete a walkthrough for each administrator topic.

## Theory and Architecture

The **NIOS DDI Administrator (INA)** builds on the operator, validating administration of
the Grid. Its topic areas: **Grid member management** (adding/joining members, service
assignment), **advanced DHCP/DNS** (options, DDNS, DNSSEC, failover), **IPAM** (network
containers, discovery data), **Discovery** (network discovery jobs), **access control**
(admin groups, permissions), and **remote authentication** (RADIUS/AD/LDAP/TACACS+).

## Design Considerations

The administrator assigns **DNS/DHCP services** to members, configures **DHCP failover**
and **DDNS**, runs **Discovery** to populate IPAM, builds **admin groups** with scoped
permissions, and integrates **remote authentication** so admins log in against the
directory. Least-privilege admin groups are central.

## Implementation and Automation

The labs use the WAPI for each administrator topic — member services, DHCP/DNS, IPAM
containers, Discovery, permissions, and remote auth.

## Validation and Troubleshooting

Confirm the topic areas:

```text
INA topics: Grid member management; advanced DHCP/DNS; IPAM; Discovery;
access control (admin groups/permissions); remote authentication.
```

Common pitfalls: single DHCP server (no **failover**); and over-broad admin groups.

## Security and Best Practices

Configure **DHCP failover** for resilience, enable **DDNS/DNSSEC** where required, run
**Discovery** to keep IPAM accurate, build **least-privilege admin groups**, and
integrate **remote authentication** with the corporate directory.

## Hands-On Lab

Per-topic walkthroughs — INA. **Shared prerequisites** — a NIOS Grid; WAPI access.
**Cost:** none beyond a lab Grid.

### Lab 3.1 — Grid member management

**Objective:** Review member service assignments.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/member:dns?_return_fields=host_name,enable_dns" \
  | python3 -c "import sys,json;print([(m['host_name'],m.get('enable_dns')) for m in json.load(sys.stdin)])"
```

**Expected result:** which members run **DNS** — the member/service management topic.

**Negative test:** assume every member serves DNS; **check service assignment** — roles
vary per member.

**Rollback:** none (read-only).

### Lab 3.2 — Advanced DHCP: failover

**Objective:** Describe a DHCP failover association.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/dhcpfailover" \
  | python3 -c "import sys,json;print('failover associations:',len(json.load(sys.stdin)))"
```

**Expected result:** the DHCP **failover** associations — the advanced DHCP topic
(resilient leasing).

**Negative test:** run a single DHCP server; **failover** keeps leasing alive if one
member fails — configure it.

**Rollback:** none (read-only).

### Lab 3.3 — Advanced DNS: DDNS/DNSSEC

**Objective:** Check a zone's DNSSEC/DDNS settings.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/zone_auth?fqdn=lab.example&_return_fields=fqdn,dnssec_enabled,allow_update" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)[0])"
```

**Expected result:** the zone's **DNSSEC/DDNS** configuration — the advanced DNS topic.

**Negative test:** allow open dynamic updates; scope **`allow_update`** (TSIG/ACL) — don't
accept updates from anywhere.

**Rollback:** none (read-only).

### Lab 3.4 — Discovery

**Objective:** Review network discovery data.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/discovery:device?_return_fields=address,os" \
  | python3 -c "import sys,json;print('discovered devices:',len(json.load(sys.stdin)))"
```

**Expected result:** devices found by **Discovery** — the Discovery topic (populating
IPAM).

**Negative test:** enter IPAM data by hand; **Discovery** reconciles actual network state
— run it.

**Rollback:** none (read-only).

### Lab 3.5 — Access control (admin groups)

**Objective:** Review admin groups and permissions.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/admingroup?_return_fields=name,roles" \
  | python3 -c "import sys,json;print([g['name'] for g in json.load(sys.stdin)])"
```

**Expected result:** the **admin groups** and their roles — the access-control topic.

**Negative test:** give all admins superuser; build **scoped admin groups** per duty.

**Rollback:** none (read-only).

### Lab 3.6 — Remote authentication

**Objective:** Confirm a remote auth service.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/ad_auth_service" \
  | python3 -c "import sys,json;print('AD auth services:',len(json.load(sys.stdin)))"
```

**Expected result:** the configured **remote authentication** (AD/LDAP/RADIUS) service —
the remote-auth topic.

**Negative test:** manage local admin accounts only; **integrate the directory** so
access follows corporate identity.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The INA certifies administering the Grid across member management, advanced DHCP/DNS
(failover, DDNS/DNSSEC), IPAM, Discovery, access control (admin groups), and remote
authentication — via the Grid Manager and WAPI.

- [ ] I can review member service assignments.
- [ ] I can describe DHCP failover and advanced DNS.
- [ ] I can review Discovery data and admin groups.
- [ ] I can confirm remote authentication integration.
- [ ] I completed Labs 3.1–3.6 including each negative test.
