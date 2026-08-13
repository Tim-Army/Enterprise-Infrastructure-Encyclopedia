# Chapter 04: IPAM — Prefixes, Addresses, VLANs, and VRFs

## Learning Objectives

- Model IP space with aggregates, prefixes, and IP addresses.
- Use hierarchy and utilization to find available space.
- Model VLANs and VLAN groups.
- Separate overlapping address space with VRFs.
- Complete a walkthrough for each IPAM building block.

## Theory and Architecture

**IPAM** models the logical network. **Aggregates** are top-level blocks (from an RIR),
subdivided into **Prefixes** (which nest hierarchically by containment), down to
individual **IP Addresses**. **VLANs** (optionally grouped into **VLAN Groups**) model
layer-2 segments, and **VRFs** provide separate routing tables so **overlapping** IP
space can coexist. NetBox computes prefix **utilization** and can return the next
available prefix/IP.

## Design Considerations

Let NetBox own **allocation**: ask it for the **next available** prefix/IP instead of
tracking in a spreadsheet. Nest prefixes to reflect real hierarchy, scope VLANs with
groups, and use **VRFs** where address space overlaps (e.g., multi-tenant).

## Implementation and Automation

The labs use `pynetbox`/`curl` to create aggregates, prefixes, IPs, VLANs, and VRFs,
and to request available space.

## Validation and Troubleshooting

Confirm the model:

```text
Aggregate (RIR block) > Prefix (nests by containment) > IP Address.
VLAN (+ VLAN Group) = L2 segment; VRF = separate routing table (allows overlap).
available-prefixes / available-ips endpoints return free space.
```

Common pitfalls: manual IP allocation causing conflicts; and overlapping prefixes
without a **VRF**.

## Security and Best Practices

Use the **available-prefixes/available-ips** endpoints for allocation, reflect real
**hierarchy**, isolate overlapping space with **VRFs**, and mark statuses
(active/reserved/deprecated). NetBox becomes the authoritative allocator.

## Hands-On Lab

IPAM walkthroughs. **Shared prerequisites** — a running NetBox; `$NB`/`$TOKEN`;
`pynetbox`. **Cost:** none.

### Lab 4.1 — Create an aggregate and prefix

**Objective:** Model a block and a child prefix.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
rir = nb.ipam.rirs.create(name="RFC1918", slug="rfc1918")
agg = nb.ipam.aggregates.create(prefix="10.0.0.0/8", rir=rir.id)
pfx = nb.ipam.prefixes.create(prefix="10.1.0.0/16", status="active")
print("aggregate:", agg.prefix, "prefix:", pfx.prefix)
```

**Expected result:** a **10.0.0.0/8** aggregate and a **10.1.0.0/16** prefix nested
within it — the IP hierarchy.

**Negative test:** create a prefix outside any aggregate for tracked space; model the
**aggregate** so utilization rolls up.

**Rollback:** `pfx.delete(); agg.delete(); rir.delete()`.

### Lab 4.2 — Allocate the next available prefix

**Objective:** Let NetBox carve a child prefix.

```python
child = pfx.available_prefixes.create({"prefix_length": 24})
print("allocated child prefix:", child["prefix"])   # e.g. 10.1.0.0/24
```

**Expected result:** the **next free /24** inside 10.1.0.0/16 — NetBox as allocator.

**Negative test:** pick a /24 by hand and hope it's free; the **available-prefixes**
endpoint guarantees no overlap.

**Rollback:** delete the allocated child prefix.

### Lab 4.3 — Model a VLAN

**Objective:** Create a VLAN in a group.

```python
grp = nb.ipam.vlan_groups.create(name="Campus", slug="campus")
vlan = nb.ipam.vlans.create(vid=100, name="users", group=grp.id, status="active")
print("vlan:", vlan.vid, vlan.name)
```

**Expected result:** **VLAN 100 "users"** in the Campus group — an L2 segment.

**Negative test:** reuse VID 100 in the same group; VIDs are unique per group — NetBox
rejects it.

**Rollback:** `vlan.delete(); grp.delete()`.

### Lab 4.4 — Separate overlapping space with a VRF

**Objective:** Create a VRF and an overlapping prefix within it.

```python
vrf = nb.ipam.vrfs.create(name="tenant-A", rd="65000:1")
overlap = nb.ipam.prefixes.create(prefix="10.1.0.0/16", vrf=vrf.id, status="active")
print("VRF prefix:", overlap.prefix, "in", vrf.name)
```

**Expected result:** a **second 10.1.0.0/16** coexisting inside VRF tenant-A — overlap
allowed by the VRF boundary.

**Negative test:** put overlapping prefixes in the **global** table; without a **VRF**
NetBox flags the duplicate — scope with a VRF.

**Rollback:** `overlap.delete(); vrf.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

IPAM models logical addressing: aggregates → prefixes → IPs with hierarchy and
utilization, VLANs/VLAN groups for L2, and VRFs to separate overlapping space. This
chapter let NetBox allocate space and isolate tenants with a VRF.

- [ ] I can model aggregates, prefixes, and IPs.
- [ ] I can request the next available prefix/IP.
- [ ] I can model VLANs and VLAN groups.
- [ ] I can separate overlapping space with a VRF.
- [ ] I completed Labs 4.1–4.4 including each negative test.
