# Chapter 06: VDOMs for Hard Separation

## Learning Objectives

- Understand VDOMs as independent virtual firewalls inside one FortiGate.
- Move the OT tier into its own VDOM so IT↔OT traffic must cross an explicit inter-VDOM link.
- Confirm that, without an inter-VDOM link and policy, IT and OT cannot reach each other at all.
- Model the hard separation in Track 2 with separate tables.

## Zones separate; VDOMs isolate

Zone-to-zone policies (Chapter 05) segment traffic that shares one routing and policy table. **VDOMs** go further: each VDOM has its own interfaces, routing table, and policy set, and there is **no path between VDOMs** unless you create an **inter-VDOM link** and write policy across it. This is the strongest separation a single FortiGate offers — appropriate for keeping an OT network isolated from IT with only a tightly controlled crossing.

## Hands-On Lab

### Exercise 6.1 — Enable VDOMs and split IT and OT

**Objective.** Create an `OT` VDOM holding the OT tier, leaving the rest in `IT`.

**Track 1 — Walkthrough.** Enable multi-VDOM mode and assign interfaces:

```text
FGT # config system global
FGT (global) # set vdom-mode multi-vdom
FGT (global) # end
FGT # config vdom
FGT (vdom) # edit IT
FGT (IT) # next
FGT (vdom) # edit OT
FGT (OT) # end
# move port5 (plc) into the OT vdom
FGT # config global
FGT (global) # config system interface
FGT (interface) # edit port5
FGT (port5) # set vdom OT
FGT (port5) # set ip 10.30.4.1/24
FGT (port5) # end
```

**Expected result.**

```text
FGT # diagnose sys vdom list | grep name
name=IT
name=OT
```

Two VDOMs exist; `port5` (the plc) now lives in `OT`, `port2–port4` (web/db/hmi) remain in `IT`.

**Negative test.** With OT split off and no inter-VDOM link yet, `hmi (IT) → plc (OT)` — previously permitted in Chapter 05 — now fails completely, because there is no route or policy path between the VDOMs at all. VDOM separation is total by default.

**Track 2 — Walkthrough.** Model each VDOM as a separate nftables table with no path between them except an explicit rule set:

```bash
sudo nft add table inet fgt_it
sudo nft add table inet fgt_ot
sudo nft add chain inet fgt_it forward '{ type filter hook forward priority 0 ; policy drop ; }'
# without a cross-table (inter-vdom) rule, IT<->OT is dropped
sudo nft list tables | grep fgt
```

**Expected result.** Two independent tables; the default-drop IT chain blocks any IT↔OT flow until an explicit crossing is added.

**Cleanup.** Keep the VDOMs.

### Exercise 6.2 — Add a controlled inter-VDOM link

**Objective.** Permit only the legitimate MGMT→OT flow across an inter-VDOM link.

**Track 1 — Walkthrough.** Create an inter-VDOM link pair, address both ends, route the OT subnet across it, and permit only MODBUS:

```text
FGT # config global
FGT (global) # config system vdom-link
FGT (vdom-link) # edit itot
FGT (itot) # end
# addresses on each end (itot0 in IT, itot1 in OT), routes, then policy:
FGT # config vdom
FGT (vdom) # edit IT
FGT (IT) # config firewall policy
FGT (policy) # edit 4
FGT (4) # set name it-to-ot-modbus
FGT (4) # set srcintf port4
FGT (4) # set dstintf itot0
FGT (4) # set srcaddr hmi
FGT (4) # set dstaddr plc
FGT (4) # set service MODBUS
FGT (4) # set action accept
FGT (4) # set schedule always
FGT (4) # end
```

The OT VDOM needs a matching policy on `itot1 → port5` permitting MODBUS to plc.

**Expected result.** `hmi → plc:502` works again, but *only* MODBUS, and *only* over the inter-VDOM link — every other IT↔OT flow remains impossible because no other policy crosses the link.

**Negative test.** Attempt `hmi → plc:22` (ssh) across the link — denied, because the only crossing policy permits MODBUS. The inter-VDOM link is a single, tightly scoped door between otherwise-isolated networks.

**Track 2 — Walkthrough.** Add the one permitted crossing between the tables' logical domains (modeled on the enforcer host as an explicit accepted flow):

```bash
sudo nft add rule inet fgt_it forward ip saddr 10.30.3.10 ip daddr 10.30.4.10 tcp dport 502 accept
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.4.10 502 && echo hmi->plc OPEN (via inter-vdom)'
```

**Expected result.** `hmi->plc OPEN (via inter-vdom)` — the single scoped crossing works; nothing else crosses.

**Cleanup.** Keep the VDOMs and link for Chapter 07.

## Summary and Completion Checklist

- [ ] Multi-VDOM enabled; OT tier isolated in its own VDOM.
- [ ] IT↔OT confirmed impossible without an inter-VDOM link.
- [ ] A single MODBUS-only crossing added over the inter-VDOM link.
- [ ] The strength of VDOM isolation understood versus zone policy.
