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

This chapter carries a topic-level walkthrough lab for **every objective in
the SVPN (300-730 Implementing Secure Solutions with VPNs) exam guide** —
site-to-site (GETVPN/DMVPN/FlexVPN), remote access (AnyConnect/Clientless),
troubleshooting, and architecture/design — plus the SCOR VPN topics, mapped
in the volume README's coverage tables. Labs use IOS and ASA CLI. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.20** — IOS routers and an ASA (or CML
equivalents), a CA for certificate labs, an AnyConnect/Secure Client image on
the ASA. **Cost:** none beyond lab resources; each lab removes its config.

### Lab 7.1 — Describe GETVPN (Objective 1.1)

**Objective:** Read a GETVPN group member's registration and SA.

```text
GM1# show crypto gdoi
GM1# show crypto gdoi gm
```

**Expected result:** the group member registered to the Key Server with a
shared group SA — tunnel-less encryption preserving the original IP header,
ideal for a fully-meshed private WAN.

**Negative test:** GETVPN over the public internet breaks (no NAT traversal,
original header preserved); it is for private (MPLS) transport.

**Cleanup:** none (read-only).

### Lab 7.2 — Implement DMVPN (Objective 1.2)

**Objective:** Build a Phase 3 DMVPN spoke and confirm NHRP.

```text
SPOKE1(config)# interface tunnel0
SPOKE1(config-if)# ip nhrp shortcut
SPOKE1(config-if)# tunnel protection ipsec profile DMVPN
SPOKE1# show dmvpn detail
```

**Expected result:** the spoke registered to the hub and a dynamic
spoke-to-spoke tunnel forming on demand — Phase 3 direct spoke traffic.

**Negative test:** without `ip nhrp shortcut`/`redirect`, spoke-to-spoke
hairpins through the hub (Phase 1); Phase 3 needs both.

**Cleanup:** `no interface tunnel0`.

### Lab 7.3 — Implement FlexVPN with local AAA (Objective 1.3)

**Objective:** Build a FlexVPN hub using IKEv2 and local AAA.

```text
HUB(config)# aaa authorization network FLEX local
HUB(config)# crypto ikev2 profile FLEX-PROF
HUB(config-ikev2-profile)# aaa authorization group psk list FLEX FLEX-POLICY
HUB# show crypto ikev2 sa
```

**Expected result:** IKEv2 SAs established with per-peer authorization from
local AAA — FlexVPN's unified IKEv2 framework for site-to-site and RA.

**Negative test:** a FlexVPN peer with no matching authorization policy gets
no attributes (IP/routes) and the tunnel is useless; authorization is
required.

**Cleanup:** remove the IKEv2 profile and AAA list.

### Lab 7.4 — Implement AnyConnect IKEv2 on ASA/routers (Objective 2.1)

**Objective:** Confirm an AnyConnect IKEv2 remote-access session.

```text
ASA# show vpn-sessiondb detail anyconnect
```

**Expected result:** a remote user connected via AnyConnect IKEv2 with an
assigned pool address and group policy — RA VPN over IKEv2/IPsec.

**Negative test:** an IKEv2 RA connection with no client profile pushing the
IKEv2 protocol falls back or fails; the profile selects the protocol.

**Cleanup:** none (read-only).

### Lab 7.5 — Implement AnyConnect SSL VPN on ASA (Objective 2.2)

**Objective:** Read the AnyConnect SSL (TLS/DTLS) session.

```text
ASA# show vpn-sessiondb detail anyconnect | include Tunnel|Encryption
```

**Expected result:** an SSL/TLS (with DTLS for data) AnyConnect tunnel — the
default RA VPN where firewalls block IKEv2/IPsec.

**Negative test:** DTLS blocked by a firewall forces TLS-only, degrading
real-time performance; permit DTLS/UDP 443 for best experience.

**Cleanup:** none (read-only).

### Lab 7.6 — Implement Clientless SSL VPN on ASA (Objective 2.3)

**Objective:** Read the clientless (browser) VPN configuration.

```text
ASA# show running-config webvpn
ASA# show vpn-sessiondb webvpn
```

**Expected result:** a clientless portal proxying specific web apps in the
browser — no client install, for limited app access.

**Negative test:** expecting full network access from clientless; it proxies
specific apps only, not an IP tunnel.

**Cleanup:** none (read-only).

### Lab 7.7 — Implement FlexVPN on routers (Objective 2.4)

**Objective:** Build a FlexVPN remote-access hub for Secure Client.

```text
HUB(config)# crypto ikev2 authorization policy FLEX-RA
HUB(config-ikev2-author-policy)# pool RA-POOL
HUB# show crypto ikev2 client flexvpn
```

**Expected result:** a FlexVPN RA hub assigning pool addresses to clients —
the router-based unified RA VPN.

**Negative test:** a FlexVPN RA client with no authorization pool gets no
address; the authorization policy must define one.

**Cleanup:** remove the authorization policy.

### Lab 7.8 — Troubleshoot IPsec (Objective 3.1)

**Objective:** Diagnose an IPsec SA failure.

```text
R1# show crypto ipsec sa
R1# show crypto isakmp sa
R1# debug crypto ipsec
```

**Expected result:** Phase 1 (ISAKMP/IKE) and Phase 2 (IPsec) SA state; the
debug names the mismatch (transform set, proxy ACL, PSK).

**Negative test:** a mismatched Phase 2 proxy ACL (interesting traffic) leaves
Phase 1 up but no data flows; check both phases.

**Cleanup:** `undebug all`.

### Lab 7.9 — Troubleshoot DMVPN (Objective 3.2)

**Objective:** Diagnose a DMVPN registration failure.

```text
HUB# show dmvpn detail
HUB# show ip nhrp
HUB# debug nhrp packet
```

**Expected result:** NHRP registration state; the debug reveals the fault
(NHRP auth mismatch, wrong NHS, tunnel-key mismatch).

**Negative test:** a tunnel-key mismatch drops NHRP silently; both ends must
share the key.

**Cleanup:** `undebug all`.

### Lab 7.10 — Troubleshoot FlexVPN (Objective 3.3)

**Objective:** Diagnose a FlexVPN IKEv2 negotiation.

```text
HUB# show crypto ikev2 sa detail
HUB# debug crypto ikev2
```

**Expected result:** the IKEv2 SA exchange; the debug names the failure
(auth method, proposal, cert validation).

**Negative test:** a certificate-authenticated FlexVPN peer with an expired
cert fails IKEv2 AUTH; check PKI validity/time.

**Cleanup:** `undebug all`.

### Lab 7.11 — Troubleshoot AnyConnect IKEv2/SSL (Objective 3.4)

**Objective:** Diagnose a remote-access connection failure on the ASA.

```text
ASA# show vpn-sessiondb fail
ASA# debug webvpn anyconnect 255
```

**Expected result:** the failed-session log and debug naming the cause (group
policy, certificate, license limit).

**Negative test:** hitting the AnyConnect license limit rejects new sessions
though config is correct; check the license count.

**Cleanup:** `undebug all`.

### Lab 7.12 — Troubleshoot Clientless SSL VPN (Objective 3.5)

**Objective:** Diagnose a clientless portal/bookmark failure.

```text
ASA# debug webvpn 255
ASA# show webvpn ... 
```

**Expected result:** the debug showing why a bookmark/app fails (rewrite
engine, DNS, plugin) — clientless rewriting is fragile per-app.

**Negative test:** a complex web app that the rewrite engine cannot proxy
breaks clientless; use AnyConnect for full access instead.

**Cleanup:** `undebug all`.

### Lab 7.13 — Identify GETVPN/FlexVPN/DMVPN/IPsec components (Objective 4.1)

**Objective:** Match components to the technology.

```text
R1# show crypto session
```

**Expected result:** the session shows the technology's components (GETVPN =
KS/GM/GDOI; DMVPN = mGRE/NHRP; FlexVPN = IKEv2/tunnel) — identify by
component.

**Negative test:** confusing DMVPN's NHRP with FlexVPN's IKEv2 config leads to
the wrong troubleshooting path; the components identify the technology.

**Cleanup:** none (read-only).

### Lab 7.14 — Identify FlexVPN/IPsec/Clientless components (Objective 4.2)

**Objective:** Read the component set of a remote-access solution.

```text
ASA# show running-config crypto ikev2
ASA# show running-config group-policy
```

**Expected result:** the IKEv2 policy, group policy, and connection profile —
the components an RA VPN is assembled from.

**Negative test:** a connection profile referencing a missing group policy
fails; the components must all be present and linked.

**Cleanup:** none (read-only).

### Lab 7.15 — Identify VPN technology from config output I (Objective 4.3)

**Objective:** Read a config and name the VPN type.

```text
R1# show running-config | section crypto
```

**Expected result:** `crypto gdoi` = GETVPN, `tunnel mode gre multipoint` =
DMVPN, `crypto ikev2 profile` + `interface tunnel` = FlexVPN — identify from
the configuration.

**Negative test:** a static crypto map is legacy site-to-site, not DMVPN/
FlexVPN; the config keywords distinguish them.

**Cleanup:** none (read-only).

### Lab 7.16 — Identify VPN technology from config output II (Objective 4.4)

**Objective:** Read a remote-access config and name the type.

```text
ASA# show running-config | include tunnel-group|webvpn|ikev2
```

**Expected result:** `webvpn` + `anyconnect enable` = AnyConnect SSL;
`webvpn` without client = clientless; `crypto ikev2` = IKEv2 RA — identified
from config.

**Negative test:** assuming any `webvpn` line means clientless; AnyConnect SSL
also uses `webvpn` — check for the client-enable line.

**Cleanup:** none (read-only).

### Lab 7.17 — Identify split-tunneling requirements (Objective 4.5)

**Objective:** Read the split-tunnel policy on an RA group policy.

```text
ASA# show running-config group-policy | include split-tunnel
```

**Expected result:** the split-tunnel ACL (tunnel only corporate subnets) vs
tunnel-all — the policy deciding what traffic uses the VPN.

**Negative test:** tunnel-all backhauls all internet traffic through the VPN,
adding latency; split-tunnel sends only corporate traffic over it (with the
security trade-off).

**Cleanup:** none (read-only).

### Lab 7.18 — Design a site-to-site VPN solution (Objective 4.6)

**Objective:** Choose the site-to-site technology from requirements.

```text
R1# show crypto session brief
```

**Decision to record:** for a fully-meshed private WAN → GETVPN; for
dynamic spoke-to-spoke over the internet → DMVPN Phase 3; for a
standards-based IKEv2 framework → FlexVPN. Record the driver and the rejected
option.

**Negative test:** GETVPN over the internet, or a full mesh of static tunnels
at 100 sites — the anti-patterns each design avoids.

**Cleanup:** none (read-only).

### Lab 7.19 — Design a remote-access VPN solution (Objective 4.7)

**Objective:** Choose the RA technology and posture from requirements.

```text
ASA# show vpn-sessiondb summary
```

**Decision to record:** AnyConnect SSL (broadest firewall traversal),
AnyConnect IKEv2 (best performance where permitted), or clientless (limited
app access, no install); plus split-tunnel and posture. Record the driver.

**Negative test:** clientless for users needing full network access
under-serves them; match the technology to the access requirement.

**Cleanup:** none (read-only).

### Lab 7.20 — Identify ECC algorithms (Objective 4.8)

**Objective:** Read the elliptic-curve crypto in a proposal.

```text
R1# show crypto ikev2 proposal
ASA# show crypto ikev2 sa detail | include Encr|PRF|DH
```

**Expected result:** ECC in use (ECDSA authentication, ECDH groups 19/20/21) —
stronger security at smaller key sizes than RSA/DH group 14.

**Negative test:** pairing an ECDSA certificate with an RSA-only IKEv2 policy
fails auth; the algorithms must match end to end.

**Cleanup:** none (read-only).

### Lab 7.21 — Build and troubleshoot a route-based IKEv2 site-to-site VPN (integrative)

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
