# Chapter 06: NRS II — Services

## Learning Objectives

- Explain the SR OS service model (VLL, VPLS, VPRN, EVPN).
- Configure a point-to-point Epipe (VLL) service.
- Configure a VPLS multipoint Layer-2 service.
- Configure a VPRN Layer-3 VPN service.
- Complete a walkthrough for each service topic.

## Theory and Architecture

Services are what a Nokia SR OS network **sells** — the customer-facing constructs carried over the
MPLS/SR transport. SR OS models them uniformly with **SAPs** (Service Access Points — the
customer-facing ports/VLANs) and **SDPs** (Service Distribution Points — the transport tunnels
between PEs). The core services are: **Epipe (VLL)** — a point-to-point Layer-2 pseudowire
connecting two customer sites as if by a wire; **VPLS** — a multipoint Layer-2 service emulating a
LAN/switch across sites; **VPRN** — a multipoint **Layer-3 VPN** (per-customer VRF, routes carried
in MP-BGP VPN-IPv4); and **EVPN** — the modern BGP control plane for Layer-2 (and L3) services,
replacing flood-and-learn with control-plane MAC/IP distribution. Each service binds SAPs to SDPs
over the transport tunnels. Services are the payoff of the whole NRS II stack.

## Design Considerations

Pick the service to the need: **Epipe** for point-to-point L2, **VPLS/EVPN** for multipoint L2,
**VPRN** for L3VPN. Prefer **EVPN** over legacy VPLS flood-and-learn for scale and efficiency. Use
consistent **service IDs** and bind SAPs to the right **SDPs/tunnels**. Keep the transport (Chapter
5) healthy — services ride on it.

## Implementation and Automation

The labs configure Epipe, VPLS, and VPRN services, and verify them.

## Validation and Troubleshooting

Confirm the service model:

```text
SAP (customer-facing) + SDP (transport tunnel between PEs). Services:
  Epipe/VLL (p2p L2), VPLS (multipoint L2), VPRN (L3VPN, MP-BGP VPN-IPv4), EVPN (BGP L2/L3 control plane).
Services bind over MPLS/SR tunnels. Prefer EVPN over legacy VPLS flood-and-learn.
```

Common pitfalls: a service with a SAP but **no SDP/tunnel** to the far PE; and legacy VPLS
flood-and-learn where **EVPN** scales better.

## Security and Best Practices

Bind services to **verified transport**, isolate customers with per-service constructs (VPRN VRFs),
and prefer **EVPN** control-plane learning. Keep service and transport configuration reviewed and
consistent. Verify each service is **up** end to end.

## Hands-On Lab

Service walkthroughs. **Shared prerequisites** — two SR OS PEs with MPLS/SR transport up between
them (Chapter 5), in a lab. **Cost:** none.

### Lab 6.1 — Configure an Epipe (VLL)

**Objective:** Build a point-to-point L2 pseudowire.

```text
A:PE1>config# service sdp 1 mpls create far-end 10.0.0.2 ldp no shutdown
A:PE1>config# service epipe 100 customer 1 create
A:PE1>config# service epipe 100 sap 1/1/2:100 create
A:PE1>config# service epipe 100 spoke-sdp 1:100 create
A:PE1# show service id 100 base
```

**Expected result:** an **Epipe** binding a customer SAP to the far PE over an SDP — a
point-to-point L2 service.

**Negative test:** create the Epipe with a SAP but **no spoke-SDP**; it can't reach the far site —
bind the SDP.

**Cleanup:** delete the epipe and SDP.

### Lab 6.2 — Configure a VPLS

**Objective:** Build a multipoint L2 service.

```text
A:PE1>config# service vpls 200 customer 1 create
A:PE1>config# service vpls 200 sap 1/1/2:200 create
A:PE1>config# service vpls 200 mesh-sdp 1:200 create
A:PE1# show service id 200 base
```

**Expected result:** a **VPLS** emulating a LAN across sites via mesh-SDPs — multipoint L2.

**Negative test:** use a VPLS where a simple **Epipe** suffices (two sites only); match the service
to the topology.

**Cleanup:** delete the vpls.

### Lab 6.3 — Configure a VPRN (L3VPN)

**Objective:** Build a per-customer Layer-3 VPN.

```text
A:PE1>config# service vprn 300 customer 1 create
A:PE1>config# service vprn 300 route-distinguisher 65000:300
A:PE1>config# service vprn 300 vrf-target target:65000:300
A:PE1>config# service vprn 300 interface "cust" address 10.20.0.1/30 sap 1/1/2:300 create
A:PE1# show service id 300 base
```

**Expected result:** a **VPRN** with an RD/RT and a customer interface — an L3VPN carried in
MP-BGP VPN-IPv4.

**Negative test:** omit the **route-target**; VPN routes won't import/export between PEs — set the
RT.

**Cleanup:** delete the vprn.

### Lab 6.4 — Verify services end to end

**Objective:** Confirm service and transport state.

```text
A:PE1# show service service-using
A:PE1# show service id 300 sdp
```

**Expected result:** the services **up** with their SDP/transport bindings — customer connectivity
delivered.

**Negative test:** declare a service working without checking **SDP/transport**; verify it is up
end to end.

**Cleanup:** none (read-only).

### Lab 6.5 — EVPN concept

**Objective:** Describe control-plane L2/L3 services.

```text
# EVPN uses MP-BGP to distribute MAC/IP reachability (and L3 routes) for services -> replaces
#   VPLS flood-and-learn with a control plane; scales multipoint L2/L3, supports active-active.
"EVPN: BGP control plane for L2/L3 services -> scalable, no flood-and-learn"
```

**Expected result:** the **EVPN** control-plane model — the modern basis for scalable services.

**Negative test:** rely on flood-and-learn at scale; **EVPN** distributes reachability via BGP —
prefer it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SR OS services — Epipe/VLL (p2p L2), VPLS (multipoint L2), VPRN (L3VPN), and EVPN (BGP control
plane) — bind customer SAPs to transport SDPs over MPLS/SR. Match the service to the topology,
prefer EVPN for scale, set RDs/RTs for L3VPN, and verify end to end.

- [ ] I can configure an Epipe (VLL).
- [ ] I can configure a VPLS.
- [ ] I can configure a VPRN with RD/RT.
- [ ] I can verify services and explain EVPN.
- [ ] I completed Labs 6.1–6.5 including each negative test.
