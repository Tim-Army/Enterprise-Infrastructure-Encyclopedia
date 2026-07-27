# Chapter 02: INO — NIOS DDI Operator

## Learning Objectives

- Explain what the INO certifies and its target role.
- Summarize the operator topic areas.
- Perform day-to-day DNS, DHCP, and IPAM tasks on the NIOS Grid.
- Manage objects via the Grid Manager and WAPI.
- Complete a walkthrough for each operator topic.

## Theory and Architecture

The **NIOS DDI Operator (INO)** validates the fundamentals of operating an Infoblox
**NIOS Grid** — the entry credential. Its topic areas: **Grid fundamentals** (the Grid
Master and members, roles), **DHCP** services (ranges, leases, fixed addresses), **DNS**
services (zones, records), **IPAM** (networks, IP allocation), and **day-to-day object
management**. Operators handle routine changes through the **Grid Manager** UI and the
**WAPI**.

## Design Considerations

The operator works within an established Grid: allocate IPs from **networks**, create
**A/PTR/CNAME** records, manage **DHCP ranges/fixed addresses**, and use IPAM to keep
address space accurate. Let NIOS own allocation (next-available IP) rather than tracking
manually.

## Implementation and Automation

The labs use the WAPI for each operator topic — Grid view, DHCP, DNS, IPAM, and object
management.

## Validation and Troubleshooting

Confirm the topic areas:

```text
INO topics: Grid fundamentals; DHCP; DNS; IPAM; day-to-day object management.
Management: Grid Manager UI + WAPI (/wapi/v2.x/).
```

Common pitfalls: creating an A record without the matching **PTR** (broken reverse DNS);
and manual IP allocation causing conflicts.

## Security and Best Practices

Allocate from **IPAM** (next-available), keep **forward and reverse** DNS in sync, manage
DHCP with **fixed addresses/reservations** where needed, and make changes through
audited surfaces (Grid Manager/WAPI).

## Hands-On Lab

Per-topic walkthroughs — INO. **Shared prerequisites** — a NIOS Grid; WAPI access
(`https://<grid>/wapi/v2.13/`, admin creds). **Cost:** none beyond a lab Grid.

### Lab 2.1 — Grid fundamentals

**Objective:** View the Grid and its members.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/member?_return_fields=host_name,service_status" \
  | python3 -c "import sys,json;print('members:',[m['host_name'] for m in json.load(sys.stdin)])"
```

**Expected result:** the Grid **member list** — the Grid fundamentals topic.

**Negative test:** assume a single appliance; a **Grid** has a Master and members —
enumerate them.

**Cleanup:** none (read-only).

### Lab 2.2 — DNS: create an A record

**Objective:** Add a host/A record.

```bash
curl -sS -k -u admin:infoblox -X POST "https://<grid>/wapi/v2.13/record:a" \
  -H "Content-Type: application/json" \
  -d '{"name":"web1.lab.example","ipv4addr":"10.10.0.20"}'
```

**Expected result:** the object reference of a new **A record** for web1 — the DNS topic.

**Negative test:** create the A record but skip the **PTR**; reverse lookups fail —
create the matching PTR.

**Cleanup:** `DELETE` the record by its `_ref`.

### Lab 2.3 — DHCP: create a range

**Objective:** Add a DHCP range to a network.

```bash
curl -sS -k -u admin:infoblox -X POST "https://<grid>/wapi/v2.13/range" \
  -H "Content-Type: application/json" \
  -d '{"start_addr":"10.10.0.100","end_addr":"10.10.0.200","network":"10.10.0.0/24"}'
```

**Expected result:** a new **DHCP range** on 10.10.0.0/24 — the DHCP topic.

**Negative test:** overlap the range with fixed addresses; NIOS flags the conflict —
keep ranges and reservations distinct.

**Cleanup:** `DELETE` the range by its `_ref`.

### Lab 2.4 — IPAM: allocate the next IP

**Objective:** Let NIOS pick the next free address.

```bash
curl -sS -k -u admin:infoblox -X POST "https://<grid>/wapi/v2.13/record:host" \
  -H "Content-Type: application/json" \
  -d '{"name":"app1.lab.example","ipv4addrs":[{"ipv4addr":"func:nextavailableip:10.10.0.0/24"}]}'
```

**Expected result:** a host record with the **next available IP** from the network —
IPAM-driven allocation.

**Negative test:** pick an IP by hand from a spreadsheet; **next-available** guarantees no
conflict — let IPAM allocate.

**Cleanup:** `DELETE` the host record by its `_ref`.

### Lab 2.5 — Day-to-day object management

**Objective:** Search and modify an object.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/record:a?name=web1.lab.example" \
  | python3 -c "import sys,json;print('ref:',json.load(sys.stdin)[0]['_ref'])"
# PUT to that _ref to change the address; DELETE to remove it.
```

**Expected result:** the object **`_ref`** to modify/delete — routine object management.

**Negative test:** edit records only in the UI at scale; the **WAPI** enables consistent,
scriptable changes — use it.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The INO certifies day-to-day NIOS operation across Grid fundamentals, DHCP, DNS, IPAM,
and object management — through the Grid Manager and WAPI. This chapter created DNS/DHCP
objects and allocated IPs via IPAM.

- [ ] I can view the Grid and its members.
- [ ] I can create DNS records with matching PTRs.
- [ ] I can create DHCP ranges without overlap.
- [ ] I can allocate the next-available IP via IPAM.
- [ ] I completed Labs 2.1–2.5 including each negative test.
