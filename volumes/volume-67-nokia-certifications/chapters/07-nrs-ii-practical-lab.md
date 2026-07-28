# Chapter 07: NRS II — The Practical Lab

## Learning Objectives

- Explain the NRS II practical lab (4A0-N01) format and expectations.
- Build an integrated network: IGP + BGP + MPLS + a service, end to end.
- Troubleshoot layer by layer when a service is down.
- Manage time and verification under lab conditions.
- Complete an integrated walkthrough for the practical lab.

## Theory and Architecture

Beyond the composite written, NRS II requires a **3.5-hour hands-on practical lab (4A0-N01)** on
real SR OS equipment. It tests **integration**: building a working network where the IGP
(Chapter 3) provides reachability, BGP (Chapter 4) distributes routes and VPN address families,
MPLS/SR (Chapter 5) provides transport, and a **service** (Chapter 6) is delivered end to end — and
then **troubleshooting** when something is broken. Success is methodical: build **bottom-up**
(interfaces → IGP → MPLS → BGP → services), verify each layer before the next, and when a service
fails, diagnose **top-down** (service → transport → BGP → IGP → interface) to find where the chain
breaks. The lab rewards disciplined verification and time management, not just configuration
knowledge.

## Design Considerations

Build **bottom-up** and verify at each layer so failures are localized. Keep a mental (or written)
**dependency chain**: a service needs transport, transport needs the IGP, BGP needs IGP next-hops.
Budget **time** across tasks and leave margin to verify. Save/commit known-good states as you go.

## Implementation and Automation

The labs assemble an integrated network, then troubleshoot a broken service layer by layer.

## Validation and Troubleshooting

Confirm the integration method:

```text
Build bottom-up: interfaces -> IGP -> MPLS/SR -> BGP -> services (verify each layer).
Troubleshoot top-down: service -> SDP/tunnel -> BGP -> IGP -> interface (find the break).
Lab: 4A0-N01, 3.5 hours, real SR OS. Verify + manage time.
```

Common pitfalls: configuring **top-down** and losing where a failure originates; and skipping
**per-layer verification** so errors compound.

## Security and Best Practices

Verify **each layer** before building on it, keep configuration **saved/committed** at good states,
and troubleshoot **systematically** (top-down for a down service). Manage time so verification is
never skipped. These habits pass the lab and run real networks.

## Hands-On Lab

Integrated walkthroughs. **Shared prerequisites** — a multi-node SR OS topology (VSR in
containerlab/EVE-NG), in a lab. **Cost:** none.

### Lab 7.1 — Build an integrated PE-to-PE service

**Objective:** Deliver a VPRN end to end across the core.

```text
# Bottom-up on both PEs and the core:
#  1) interfaces + system  2) IS-IS (or OSPF)  3) LDP/SR transport  4) IBGP (VPN-IPv4)  5) VPRN
A:PE1# show router isis adjacency        ;# layer 2 up?
A:PE1# show router tunnel-table          ;# transport up?
A:PE1# show router bgp summary           ;# VPN-IPv4 established?
A:PE1# show service id 300 base          ;# service up?
```

**Expected result:** each layer verified in order, ending in a **VPRN up** end to end — integrated
delivery.

**Negative test:** configure the VPRN before the IGP/transport/BGP are up; build **bottom-up** and
verify each layer.

**Cleanup:** none (keep for Lab 7.2).

### Lab 7.2 — Troubleshoot a down service (top-down)

**Objective:** Localize a break methodically.

```text
# Service down. Diagnose top-down:
A:PE1# show service id 300 base          ;# service oper state / SDP status
A:PE1# show router tunnel-table          ;# is the transport tunnel to the far PE present?
A:PE1# show router bgp summary           ;# is VPN-IPv4 established? routes received?
A:PE1# show router isis adjacency        ;# is the IGP up (next-hop reachable)?
```

**Expected result:** the **layer where the chain breaks** identified (e.g., missing tunnel because
LDP is down) — a targeted fix.

**Negative test:** randomly reconfigure the service; diagnose **top-down** to find the actual
broken layer first.

**Cleanup:** none.

### Lab 7.3 — Verify and manage time

**Objective:** Confirm the whole network and budget verification.

```text
A:PE1# show router route-table
A:PE1# show service service-using
# Budget: build ~60%, verify ~25%, buffer ~15% of the 3.5-hour window.
echo "verify every layer; reserve time to check the full end-to-end path"
```

**Expected result:** a fully verified network with **time reserved** for checking — lab discipline.

**Negative test:** spend all time configuring and none verifying; **reserve verification time** —
an unverified network may be silently broken.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NRS II practical lab (4A0-N01, 3.5 hours) tests integration and troubleshooting on real SR OS:
build bottom-up (interfaces → IGP → MPLS/SR → BGP → services), verify each layer, and diagnose a
down service top-down. Build methodically, verify continuously, and manage time.

- [ ] I can build an integrated PE-to-PE service bottom-up.
- [ ] I can troubleshoot a down service top-down.
- [ ] I can verify the full network and manage lab time.
- [ ] I understand the 4A0-N01 format.
- [ ] I completed Labs 7.1–7.3 including each negative test.
