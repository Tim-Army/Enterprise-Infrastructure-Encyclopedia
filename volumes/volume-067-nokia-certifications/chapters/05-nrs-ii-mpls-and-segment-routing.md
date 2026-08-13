# Chapter 05: NRS II — MPLS and Segment Routing

## Learning Objectives

- Explain MPLS in the SR OS core (LDP and RSVP-TE).
- Configure LDP for label distribution.
- Configure RSVP-TE LSPs for traffic engineering.
- Describe Segment Routing (SR-MPLS) as the modern transport.
- Complete a walkthrough for each MPLS topic.

## Theory and Architecture

**MPLS** provides the transport tunnels that carry services across a Nokia SR OS core. Labels are
distributed two ways: **LDP** (Label Distribution Protocol) builds label-switched paths that follow
the IGP shortest path automatically — simple and ubiquitous; and **RSVP-TE** signals explicit,
**traffic-engineered LSPs** with bandwidth reservation and constraints, used for guaranteed paths
and fast reroute. The modern alternative is **Segment Routing (SR-MPLS)**, which encodes the path
as a stack of **segment IDs** advertised by the IGP (IS-IS/OSPF) — no LDP/RSVP state in the core,
simpler and highly scalable, and the foundation for SR-TE and SRv6. Services (Chapter 6) bind to
these transport tunnels. NRS II expects fluency in LDP, RSVP-TE, and SR concepts on SR OS.

## Design Considerations

Use **LDP** for simple any-to-any transport, **RSVP-TE** where you need traffic engineering or
bandwidth guarantees, and **Segment Routing** to remove per-LSP state and scale the core. Enable
MPLS on core interfaces, keep the IGP solid (transport rides on it), and prefer **SR** for new
designs.

## Implementation and Automation

The labs enable LDP, signal an RSVP-TE LSP, enable Segment Routing, and verify the tunnels.

## Validation and Troubleshooting

Confirm the MPLS model:

```text
LDP: labels follow IGP shortest path (simple, any-to-any). RSVP-TE: explicit TE LSPs + bandwidth + FRR.
Segment Routing (SR-MPLS): path as segment-ID stack advertised by IGP; no LDP/RSVP core state; SR-TE/SRv6.
Services bind to transport tunnels. Enable MPLS on core interfaces.
```

Common pitfalls: expecting label transport with **MPLS not enabled** on the interface; and running
LDP **and** RSVP without a clear tunnel-selection policy.

## Security and Best Practices

Keep the **IGP** solid (MPLS transport depends on it), enable MPLS only on **core** interfaces, and
prefer **Segment Routing** to reduce state. Verify LSPs are **up** before binding services. Secure
control-plane protocols.

## Hands-On Lab

MPLS walkthroughs. **Shared prerequisites** — SR OS core nodes with an IGP up, in a lab. **Cost:**
none.

### Lab 5.1 — Enable LDP

**Objective:** Distribute labels along the IGP path.

```text
A:router>config# router ldp interface-parameters interface "to-core" no shutdown
A:router# show router ldp session
A:router# show router ldp bindings active
```

**Expected result:** an **LDP** session up and active label bindings — LSPs following the IGP.

**Negative test:** enable LDP but leave **MPLS off** on the interface; transport needs MPLS enabled
— enable it.

**Rollback:** `configure router ldp shutdown`.

### Lab 5.2 — Signal an RSVP-TE LSP

**Objective:** Build a traffic-engineered path.

```text
A:router>config# router rsvp no shutdown
A:router>config# router mpls interface "to-core" no shutdown
A:router>config# router mpls lsp "to-PE2" to 10.0.0.2 primary "loose" no shutdown
A:router# show router mpls lsp
```

**Expected result:** an **RSVP-TE LSP** to PE2 in **Up** state — a signaled, TE-capable tunnel.

**Negative test:** create an LSP with **RSVP disabled**; RSVP-TE must be enabled to signal — turn
it on.

**Rollback:** shut and delete the LSP.

### Lab 5.3 — Enable Segment Routing

**Objective:** Use IGP-advertised segments for transport.

```text
A:router>config# router isis segment-routing prefix-sid-range global no shutdown
A:router>config# router isis interface "system" 
A:router# show router isis segment-routing sid-database
```

**Expected result:** **Segment Routing** enabled with a prefix-SID database — stateless MPLS
transport via the IGP.

**Negative test:** expect SR transport with **no SID range/enablement**; SR must be enabled under
the IGP — configure it.

**Rollback:** `configure router isis segment-routing shutdown`.

### Lab 5.4 — Verify tunnel table

**Objective:** Confirm transport tunnels are available to services.

```text
A:router# show router tunnel-table
```

**Expected result:** LDP/RSVP/SR **tunnels** in the tunnel table — transport ready for service
binding.

**Negative test:** bind a service before a tunnel exists; check the **tunnel-table** first.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MPLS transport in NRS II spans LDP (IGP-following), RSVP-TE (traffic-engineered), and Segment
Routing (stateless, IGP-advertised segments). Enable MPLS on core interfaces, choose the transport
per need, prefer SR for scale, and verify the tunnel table before binding services.

- [ ] I can enable LDP and see label bindings.
- [ ] I can signal an RSVP-TE LSP.
- [ ] I can enable Segment Routing.
- [ ] I can verify the tunnel table.
- [ ] I completed Labs 5.1–5.4 including each negative test.
