# Chapter 07: Secure VPNs: Site-to-Site, Remote Access, and Troubleshooting

## Learning Objectives

- Explain IPsec and the IKEv2 negotiation that establishes a tunnel.
- Configure site-to-site VPNs on routers and firewalls, including
  route-based (VTI) designs.
- Describe remote-access VPN with Cisco Secure Client, including SSL and
  IPsec, and split tunneling.
- Explain the scalable VPN architectures — FlexVPN and DMVPN — and when
  each applies.
- Troubleshoot a VPN methodically, which is where the SVPN concentration
  puts most of its weight.

## Theory and Architecture

### The SVPN concentration, and where its weight actually is

This chapter is the **SVPN (300-730)** concentration, and its weight
distribution is the single most important thing to understand before
studying it:

| SVPN domain | Weight |
| --- | --- |
| Troubleshooting Using ASDM and CLI | **35%** |
| Secure Communications Architectures | **30%** |
| Remote Access VPNs | 20% |
| Site-to-Site VPNs on Routers and Firewalls | 15% |

**Building tunnels is 15% of this exam. Troubleshooting and architecture
are 65%.** A candidate who can configure a site-to-site VPN but cannot
diagnose why one is down, or design which VPN model fits a topology, has
prepared for the smallest domain. The chapter is weighted the same way:
configuration is the foundation, but the depth is in reading a failed
negotiation and choosing an architecture.

### IPsec and IKEv2

IPsec is the protocol suite securing IP traffic, and **IKEv2 (Internet Key
Exchange version 2)** is how two peers negotiate and maintain the security
association. The exchange, which you must be able to read to troubleshoot:

- **IKE SA (phase 1 equivalent)** — the peers authenticate each other
  (pre-shared key or certificate, the PKI from Chapter 01) and establish a
  secure channel for negotiation.
- **Child SA (phase 2 equivalent)** — within that channel, they negotiate
  the parameters that actually protect data traffic: encryption, integrity,
  and which traffic the tunnel carries.

IKEv2 replaced the older IKEv1 with a simpler, more resilient exchange, and
SVPN is written to it. The parameters both sides propose — encryption
algorithm, integrity, Diffie-Hellman group, lifetime — must match, and a
mismatch is the most common tunnel failure. Reading which parameter failed
to agree is the core troubleshooting skill.

### Site-to-site VPNs: policy-based and route-based

Two models connect sites, and choosing correctly is architecture, not
configuration:

- **Policy-based** — an access list defines "interesting traffic," and
  matching traffic is encrypted into the tunnel. Simple for a single,
  static pair of subnets; awkward as topologies grow because every subnet
  pair needs an entry.
- **Route-based (VTI, Virtual Tunnel Interface)** — the tunnel is a
  routable interface, and normal routing decides what goes through it.
  This scales, supports dynamic routing across the tunnel, and is the
  modern default. VTI is what SVPN expects you to reach for.

### Remote access: Cisco Secure Client

Remote-access VPN connects individual users, through the **Cisco Secure
Client** (formerly AnyConnect) — the same consolidated agent carrying DNS
security (Chapter 03), endpoint protection (Chapter 04), and ISE posture
(Chapter 06). Two transport options:

- **SSL/TLS VPN** — runs over TLS (443), traversing firewalls and proxies
  easily because it looks like web traffic. The common choice.
- **IPsec/IKEv2 remote access** — IPsec for the remote user, where its
  characteristics are preferred.

**Split tunneling** is the key design decision: does *all* the user's
traffic go through the VPN (full tunnel — everything inspected, higher
latency, more load) or only corporate-bound traffic (split tunnel — direct
internet access, less protected)? The answer interacts with the
secure-service-edge model from Chapter 03: split tunneling plus SSE can
give both direct paths and enforced policy, which is part of why SSE is
strategically ascendant.

### Scalable architectures: DMVPN and FlexVPN

For many sites, configuring individual tunnels does not scale. Two
architectures solve it, and Secure Communications Architectures (30% of
SVPN) is largely about them:

- **DMVPN (Dynamic Multipoint VPN)** — a hub-and-spoke design where spokes
  build dynamic, on-demand tunnels directly to each other when they have
  traffic to exchange, using NHRP to discover peers and mGRE for the
  multipoint tunnel. It scales a mesh without configuring one.
- **FlexVPN** — a unified, IKEv2-based framework that covers site-to-site,
  hub-and-spoke, and remote access under one configuration model. Cisco's
  strategic direction for VPN, and where SVPN weights architecture.

Choosing between them — and knowing DMVPN's phases and FlexVPN's building
blocks — is architecture-domain material, and it is worth more of the exam
than configuring any single tunnel.

## Design Considerations

- **Default to route-based (VTI) for site-to-site.** It scales, supports
  dynamic routing, and avoids the access-list sprawl of policy-based. Use
  policy-based only for a simple, static pair or when interoperating with
  a peer that requires it.
- **Choose the VPN architecture from the topology.** A few sites: static
  VTI tunnels. A large hub-and-spoke with spoke-to-spoke traffic: DMVPN. A
  need to unify site-to-site and remote access: FlexVPN. This choice is
  worth 30% of the exam; make it deliberately.
- **Decide split versus full tunnel against the security model.** Full
  tunnel inspects everything at the cost of latency and load; split tunnel
  is lighter but less protected. SSE (Chapter 03) changes the trade by
  enforcing policy on the direct path.
- **Plan the crypto parameters to match, and to be current.** Both peers
  must agree, and both should use current algorithms. A mismatch fails the
  tunnel; a weak-but-matching set is a vulnerability.
- **Design for troubleshooting.** Since 35% of the exam is diagnosis,
  design VPNs to be diagnosable: consistent naming, logging enabled, and
  known-good baselines to compare against.

## Implementation and Automation

### 1. A route-based site-to-site tunnel (IKEv2, VTI)

On IOS XE, the essential building blocks:

```text
! IKEv2 proposal and policy — the phase-1 parameters that must match
crypto ikev2 proposal PROP
 encryption aes-cbc-256
 integrity sha256
 group 14
crypto ikev2 policy POL
 proposal PROP

! Keyring (pre-shared key) and profile identifying the peer
crypto ikev2 keyring KR
 peer SITE-B
  address 198.51.100.2
  pre-shared-key <secret>
crypto ikev2 profile IKE-PROF
 match identity remote address 198.51.100.2 255.255.255.255
 authentication local pre-share
 authentication remote pre-share
 keyring local KR

! IPsec transform and the tunnel interface (VTI)
crypto ipsec transform-set TS esp-aes 256 esp-sha256-hmac
 mode tunnel
crypto ipsec profile IPSEC-PROF
 set transform-set TS
 set ikev2-profile IKE-PROF

interface Tunnel0
 ip address 10.255.255.1 255.255.255.252
 tunnel source GigabitEthernet1
 tunnel mode ipsec ipv4
 tunnel destination 198.51.100.2
 tunnel protection ipsec profile IPSEC-PROF
```

Routing then directs traffic through `Tunnel0` like any interface — the
route-based advantage.

### 2. The troubleshooting commands — the 35%

Reading a tunnel's state is the highest-weighted SVPN skill:

```text
! Is the IKEv2 SA up? If not, phase 1 (authentication/parameters) failed.
show crypto ikev2 sa

! Is the IPsec (child) SA up and passing packets? Watch encaps/decaps.
show crypto ipsec sa

! The negotiation itself — where a mismatch actually shows
debug crypto ikev2
```

The diagnostic logic:

| Symptom | Command | Meaning |
| --- | --- | --- |
| No IKEv2 SA | `show crypto ikev2 sa` | Phase 1 failed — auth or parameter mismatch |
| IKEv2 up, no IPsec SA | `show crypto ipsec sa` | Phase 2 failed — transform or proxy-ID mismatch |
| SAs up, no traffic | `show crypto ipsec sa` (encaps/decaps counters) | Routing or interesting-traffic problem |
| Tunnel flaps | logs, lifetimes | Mismatched lifetimes or path instability |

The single most common cause across all of these is a **parameter
mismatch** — the two ends proposing sets that do not intersect. The debug
shows exactly which parameter failed to agree, which is why reading it is
worth a third of the exam.

## Validation and Troubleshooting

### The up-the-stack method

VPN troubleshooting has a natural order that mirrors the negotiation:

1. **Is IKEv2 (phase 1) up?** No — authentication (PSK/certificate) or
   IKE-proposal mismatch. This is where most failures live.
2. **Is the IPsec child SA up?** IKE up but no child — transform-set
   mismatch, or the proxy identities (what traffic each side expects to
   protect) do not agree.
3. **Are packets encrypting and decrypting?** SAs up but counters flat —
   routing is not sending traffic to the tunnel, or interesting-traffic
   definitions differ.
4. **Is it stable?** Flapping — lifetime mismatches or an unstable
   underlay.

Working this order, rather than guessing, is the method SVPN's 35%
troubleshooting domain rewards. The discipline is identical in spirit to
Chapter 02's firewall order-of-operations: find the stage that failed,
then fix that stage.

### The proxy-ID trap

A classic phase-2 failure: IKE comes up cleanly, but the child SA never
forms because the two ends disagree about *which traffic* the tunnel
protects. On policy-based VPNs the access lists must mirror each other
exactly; a subnet on one side not matched on the other fails the
negotiation with a proxy-identity mismatch. Route-based VTI avoids this by
protecting all traffic on the tunnel interface — one of the concrete
reasons to prefer it.

## Security and Best Practices

- **Use certificate authentication over pre-shared keys where you can.**
  PSKs are simpler but weaker and harder to rotate at scale; certificates
  (Chapter 01's PKI) are the stronger, more manageable choice.
- **Use current cryptographic parameters.** Deprecated DH groups and
  ciphers are both exam material and real weakness; strong-by-default is
  the posture.
- **Prefer route-based VPNs for manageability and security.** Fewer
  proxy-ID failures, cleaner routing, and easier troubleshooting.
- **Protect the VPN headend as tier-0.** It terminates trusted tunnels
  into the network; compromising it is compromising the perimeter it
  defines.
- **Log and baseline tunnels.** A known-good `show crypto` baseline is
  what makes a later failure diagnosable by comparison — designing for the
  35% troubleshooting reality.

## References and Knowledge Checks

**References**

- [Cisco 300-730 SVPN exam topics](https://learningnetwork.cisco.com/s/svpn-exam-topics)
  — the concentration's domains and subtopics.
- [Cisco Secure Client documentation](https://www.cisco.com/c/en/us/support/security/anyconnect-secure-mobility-client/series.html)
  — remote-access VPN and the consolidated agent.
- [Chapter 01](01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md)
  — the PKI foundation certificate-based VPN authentication depends on.
- [Volume III, Chapter 03](../../volume-03-cisco-enterprise-networking/chapters/03-cisco-enterprise-routing-and-path-control.md)
  — the routing that route-based VPNs direct across the tunnel.

**Knowledge checks**

1. What do the IKE SA and the child SA each establish, and which failure
   maps to which?
2. Distinguish policy-based from route-based site-to-site VPN and state
   which to prefer and why.
3. When would you choose DMVPN, and when FlexVPN?
4. Explain the split-versus-full-tunnel decision and how SSE changes it.
5. A tunnel's IKEv2 SA is up but no IPsec child SA forms. What class of
   problem is this, and what is the classic cause?

## Hands-On Lab

**Objective:** Build a route-based site-to-site IKEv2 VPN, then deliberately
break and diagnose it — spending the lab time where the exam puts its
weight.

**Prerequisites:** Two routers or firewalls that can build an IPsec tunnel
— Cisco Modeling Labs is the practical route; dCloud offers VPN labs. No
production VPN headend.

**This lab is the most reproducible concentration** without buying
licensed appliances: CML routers carry site-to-site IKEv2 fully.

**Procedure**

1. Build a route-based (VTI) IKEv2 tunnel between two routers using the
   configuration above, with matching proposals and a pre-shared key.
2. Confirm the tunnel with `show crypto ikev2 sa` and `show crypto ipsec
   sa`, and verify traffic crosses it by watching the encaps/decaps
   counters.
3. Route a lab subnet across the tunnel and confirm end-to-end
   connectivity.
4. Convert the authentication from pre-shared key to certificate-based
   (using a lab CA), exercising the PKI dependency from Chapter 01.

**Negative test**

5. Introduce a mismatch on one end — change the IKEv2 integrity algorithm
   or the DH group on one router only — and observe the tunnel fail. Use
   `show crypto ikev2 sa` to confirm phase 1 is down, then `debug crypto
   ikev2` to read *which* parameter failed to agree. Fix it and confirm
   recovery. This is the exact skill the 35% troubleshooting domain tests.
6. Then induce a phase-2 failure: on a policy-based configuration, make the
   interesting-traffic access lists asymmetric and observe the child SA
   fail with a proxy-identity mismatch while IKE stays up.

**Expected results**

- A working certificate-authenticated route-based tunnel passing traffic.
- A diagnosed phase-1 parameter mismatch, identified from the debug to the
  specific parameter.
- A diagnosed phase-2 proxy-ID mismatch, distinguished from a phase-1
  failure.

**Cleanup**

7. Remove the lab tunnel configuration or revert to saved baselines, and
   end the CML or dCloud session.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SVPN is a troubleshooting-and-architecture exam wearing a configuration
exam's name: building tunnels is 15% of it, while diagnosing them is 35%
and designing the right VPN model is 30%. IPsec with IKEv2 establishes
tunnels in two stages — an authenticated IKE SA, then a child SA
protecting data — and reading which stage and which parameter failed is
the dominant skill. Route-based VTI is the modern default for site-to-site
because it scales and sidesteps the proxy-ID failures that plague
policy-based designs; DMVPN and FlexVPN are the architectures that scale a
mesh and unify VPN types, and choosing among them is worth more than
configuring any single tunnel. Remote access runs through the same
consolidated Secure Client that carries the volume's other endpoint
controls, and the split-versus-full-tunnel decision ties directly back to
the secure service edge.

- [ ] Can explain the IKE SA and child SA and map failures to each.
- [ ] Can build and prefer a route-based VTI tunnel.
- [ ] Can choose among static VTI, DMVPN, and FlexVPN from a topology.
- [ ] Can diagnose a phase-1 parameter mismatch from the debug.
- [ ] Can distinguish a phase-2 proxy-ID failure from a phase-1 failure.
