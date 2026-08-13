# Chapter 02: MTCNA — RouterOS Fundamentals

## Learning Objectives

- Navigate RouterOS via the CLI and WinBox.
- Configure interfaces, IP addressing, and DHCP.
- Configure source NAT (masquerade) for internet access.
- Apply a basic firewall and back up the configuration.
- Complete a walkthrough for each MTCNA topic.

## Theory and Architecture

**MTCNA** is the foundation certificate and the prerequisite for all others. It covers operating
**RouterOS**: the management interfaces (**CLI**, the **WinBox** GUI, WebFig, and the API); the menu
hierarchy (`/interface`, `/ip address`, `/ip dhcp-server`, `/ip firewall`); **IP addressing** and
**DHCP** (server and client); **NAT** — especially **masquerade** (source NAT) so a private LAN
reaches the internet through one public address; a **basic firewall** (filter rules on the
input/forward chains to protect the router and the network); **bridging** (combining ports into one
L2 domain); basic **wireless**; and **management** (users, backup/export, upgrades). RouterOS
applies a consistent command grammar (`add`, `set`, `print`, `remove`) across every menu, so the
skills transfer across features. MTCNA proves you can bring a MikroTik router online, connect a LAN
to the internet, and protect it.

## Design Considerations

Plan addressing and let **DHCP** serve clients. Use **masquerade** for LAN internet access. Protect
the router with an **input** firewall (accept established/related, drop the rest) and the network
with a **forward** policy. **Back up/export** before changes. Prefer WinBox for learning, CLI for
speed and automation.

## Implementation and Automation

The labs configure addressing/DHCP, masquerade NAT, a basic firewall, and a backup, using RouterOS
CLI.

## Validation and Troubleshooting

Confirm the MTCNA model:

```text
RouterOS: CLI + WinBox/WebFig + API; menus /interface /ip address /ip dhcp-server /ip firewall.
Grammar: add/set/print/remove. NAT: masquerade (srcnat) for LAN internet.
Firewall: input (protect router) + forward (protect network); accept established/related, drop rest.
Backup: /system backup + /export. RouterOS v6/v7.
```

Common pitfalls: no **masquerade**, so the LAN can't reach the internet; and an **input** chain
left open, exposing the router.

## Security and Best Practices

Firewall the **router itself** (input chain), masquerade the LAN, use strong credentials, and
**disable/limit** unused services (restrict WinBox/API access). **Back up** before every change.
These are the security basics MTCNA instills.

## Hands-On Lab

MTCNA walkthroughs. **Shared prerequisites** — a RouterOS instance (CHR in GNS3/EVE-NG or a
RouterBOARD), in a lab. **Cost:** none with CHR.

### Lab 2.1 — Address an interface and serve DHCP

**Objective:** Bring up a LAN with DHCP.

```text
/ip address add address=192.168.88.1/24 interface=ether2
/ip pool add name=lan-pool ranges=192.168.88.10-192.168.88.254
/ip dhcp-server add name=lan interface=ether2 address-pool=lan-pool disabled=no
/ip dhcp-server network add address=192.168.88.0/24 gateway=192.168.88.1 dns-server=1.1.1.1
/ip address print
```

**Expected result:** the LAN interface addressed and a **DHCP server** handing out leases — clients
get addresses.

**Negative test:** enable the DHCP server with **no address pool/network**; it can't lease — define
the pool and network.

**Rollback:** `/ip dhcp-server remove [find name=lan]; /ip address remove [find interface=ether2]`.

### Lab 2.2 — Masquerade for internet access

**Objective:** Source-NAT the LAN out the WAN.

```text
/ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade
/ip firewall nat print
```

**Expected result:** a **masquerade** rule so LAN hosts reach the internet via the WAN address —
source NAT.

**Negative test:** expect LAN internet with **no NAT**; private addresses aren't routable — add
masquerade.

**Rollback:** `/ip firewall nat remove [find action=masquerade]`.

### Lab 2.3 — Basic router firewall

**Objective:** Protect the router's input chain.

```text
/ip firewall filter add chain=input connection-state=established,related action=accept
/ip firewall filter add chain=input connection-state=invalid action=drop
/ip firewall filter add chain=input in-interface=ether1 action=drop comment="drop WAN to router"
/ip firewall filter print
```

**Expected result:** an **input** firewall accepting established/related and dropping WAN-to-router
— the router protected.

**Negative test:** leave the input chain default-accept from the WAN; the router is **exposed** —
add input filtering.

**Rollback:** remove the added filter rules.

### Lab 2.4 — Back up and export

**Objective:** Create restore points.

```text
/system backup save name=pre-change
/export file=pre-change
/file print
```

**Expected result:** a binary **backup** and a readable **export** — restore points before changes.

**Negative test:** change config with no backup; a bad change is hard to undo — **back up/export**
first.

**Rollback:** none (keep the backups).

### Lab 2.5 — Bridge ports

**Objective:** Combine ports into one L2 segment.

```text
/interface bridge add name=bridge-lan
/interface bridge port add bridge=bridge-lan interface=ether2
/interface bridge port add bridge=bridge-lan interface=ether3
/interface bridge port print
```

**Expected result:** ether2/ether3 in **bridge-lan** — a single Layer-2 domain across ports.

**Negative test:** expect two separate ports to switch traffic with no bridge; **bridge** them for
L2 connectivity.

**Rollback:** `/interface bridge remove bridge-lan`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCNA covers RouterOS fundamentals: interfaces and addressing, DHCP, masquerade NAT, a basic
input/forward firewall, bridging, and backups — with RouterOS's consistent add/set/print grammar.
Serve DHCP, masquerade the LAN, firewall the router, and back up before changes.

- [ ] I can address an interface and serve DHCP.
- [ ] I can configure masquerade NAT.
- [ ] I can protect the router's input chain.
- [ ] I can back up/export and bridge ports.
- [ ] I completed Labs 2.1–2.5 including each negative test.
