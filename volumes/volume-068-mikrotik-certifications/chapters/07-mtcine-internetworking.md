# Chapter 07: MTCINE — Inter-networking

## Learning Objectives

- Explain the MTCINE scope: BGP, MPLS, VPLS, and traffic engineering.
- Configure BGP on RouterOS v7.
- Enable MPLS with LDP for label switching.
- Describe VPLS for Layer-2 VPN over MPLS.
- Complete a walkthrough for each inter-networking topic.

## Theory and Architecture

**MTCINE** (Inter-networking Engineer, requires MTCRE) is the ISP/carrier certificate: **BGP**,
**MPLS**, **VPLS**, and **traffic engineering**. **BGP** connects autonomous systems (EBGP for
peering/transit, IBGP within the AS) and carries full internet routing; on **RouterOS v7** the
syntax changed to `/routing bgp connection` (from v6's `/routing bgp peer`). **MPLS** label-switches
traffic across the core: **LDP** distributes labels along the IGP path so the core forwards by
label, not IP lookup — the basis for scalable transport and VPNs. **VPLS** builds a **Layer-2 VPN**
(multipoint bridged service) over the MPLS core, connecting customer sites at L2 across the ISP.
Traffic engineering steers traffic for capacity and resilience. MTCINE is where MikroTik meets
service-provider networking.

## Design Considerations

Use **EBGP** for external peering and **IBGP** (full mesh or reflectors) internally; filter with
**routing filters**. Keep the **IGP** solid — MPLS/LDP rides on it. Use **MPLS/LDP** for scalable
transport and **VPLS** for L2 VPNs. On v7, use the **new BGP syntax**. Control advertisement with
policy, never leak.

## Implementation and Automation

The labs configure BGP (v7), enable MPLS/LDP, and describe VPLS.

## Validation and Troubleshooting

Confirm the inter-networking model:

```text
BGP (v7): /routing bgp connection (EBGP/IBGP), routing filters. IGP underpins MPLS.
MPLS: /mpls ldp distributes labels along IGP -> label switching. VPLS: L2 VPN over MPLS.
MTCINE requires MTCRE.
```

Common pitfalls: **v6 BGP syntax** on v7; and MPLS/LDP with a **broken IGP** (labels follow the
IGP).

## Security and Best Practices

Filter BGP with **import/export policy**, authenticate sessions, and keep the **IGP** solid for
MPLS. Use **VPLS** for isolated L2 VPNs. Verify label bindings and BGP best paths before trusting
the network. Controlled advertisement throughout.

## Hands-On Lab

MTCINE walkthroughs. **Shared prerequisites** — RouterOS core nodes (CHR) with an IGP up, in a lab.
**Cost:** none.

### Lab 7.1 — Configure BGP (RouterOS v7)

**Objective:** Peer with another AS (v7 syntax).

```text
/routing bgp connection add name=peer-isp remote.address=192.0.2.2 remote.as=65100 \
    local.role=ebgp local.address=192.0.2.1 
/routing bgp connection print
/routing bgp session print
```

**Expected result:** an **EBGP** session (RouterOS **v7** `bgp connection`) established — inter-AS
routing.

**Negative test:** configure `/routing bgp peer` (v6 syntax) on v7; use the **v7 `bgp connection`**
model.

**Rollback:** `/routing bgp connection remove [find name=peer-isp]`.

### Lab 7.2 — Filter BGP routes

**Objective:** Control advertised/received prefixes.

```text
/routing filter rule add chain=bgp-out rule="if (dst==203.0.113.0/24) {accept}"
/routing filter rule add chain=bgp-out rule="reject"
/routing bgp connection set [find name=peer-isp] output.filter-chain=bgp-out
/routing filter rule print
```

**Expected result:** only the intended prefix advertised via a **routing filter chain** —
policy-controlled BGP.

**Negative test:** advertise with **no filter**; you may leak routes — filter output.

**Rollback:** reset the connection filter and remove the rules.

### Lab 7.3 — Enable MPLS with LDP

**Objective:** Label-switch across the core.

```text
/mpls ldp add transport-address=10.0.0.1 lsr-id=10.0.0.1 enabled=yes
/mpls ldp interface add interface=ether1
/mpls ldp neighbor print
/mpls forwarding-table print
```

**Expected result:** an **LDP** neighbor and label bindings — MPLS label switching along the IGP.

**Negative test:** enable LDP with a **down IGP**; labels follow the IGP — fix routing first.

**Rollback:** `/mpls ldp remove [find]`.

### Lab 7.4 — VPLS concept

**Objective:** Describe an L2 VPN over MPLS.

```text
# VPLS builds a multipoint Layer-2 bridge across the MPLS core: customer sites appear on one LAN
#   over the ISP. Pseudowires carry L2 frames label-switched between PE routers.
"VPLS: L2 VPN over MPLS -> customer sites bridged across the provider core"
```

**Expected result:** the **VPLS** model — Layer-2 VPN transport over MPLS.

**Negative test:** stretch a customer L2 across the internet with no encapsulation; **VPLS over
MPLS** provides the isolated L2 VPN — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCINE covers ISP inter-networking: BGP (the RouterOS v7 `bgp connection` model) with routing
filters, MPLS/LDP label switching over a solid IGP, and VPLS Layer-2 VPNs. Use the v7 BGP syntax,
filter advertisements, keep the IGP solid for MPLS, and use VPLS for L2 VPNs.

- [ ] I can configure BGP with the v7 syntax.
- [ ] I can filter BGP routes.
- [ ] I can enable MPLS/LDP.
- [ ] I can explain VPLS.
- [ ] I completed Labs 7.1–7.4 including each negative test.
