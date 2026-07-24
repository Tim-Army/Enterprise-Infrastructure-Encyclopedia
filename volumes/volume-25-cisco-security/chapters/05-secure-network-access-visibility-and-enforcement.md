# Chapter 05: Secure Network Access, Visibility, and Enforcement

## Learning Objectives

- Explain 802.1X and the supplicant/authenticator/authentication-server
  model.
- Describe network segmentation by identity with Cisco TrustSec and
  security group tags.
- Explain network telemetry and visibility: NetFlow, and encrypted-traffic
  analytics.
- Connect this SCOR domain to the SISE concentration, which implements
  most of its enforcement.
- Apply access control and visibility to the lateral-movement threat from
  Chapter 01.

## Theory and Architecture

### The bridge domain

Secure Network Access, Visibility, and Enforcement is **15% of SCOR
v2.0**, and it is the bridge between the core exam and the SISE
concentration. This chapter covers the concepts SCOR tests; the platform
that implements most of them — the Identity Services Engine — is the whole
of [Chapter 06](06-identity-services-engine-deployment-policy-and-services.md).
Read this chapter for the *why* and the vocabulary; read Chapter 06 for
the *how* on the product.

The domain answers a specific Chapter 01 threat directly: **lateral
movement**. A perimeter firewall does nothing against an attacker already
inside; controlling who and what may connect to the network, and
segmenting by identity once connected, is how you contain a breach rather
than merely repel one.

### 802.1X: authenticating the connection itself

**802.1X** authenticates a device or user *before* granting network
access, at the point of connection. Its three roles are the model SCOR
expects you to know cold:

- **Supplicant** — the endpoint requesting access, running software (often
  the Cisco Secure Client from
  [Chapter 04](04-content-security-and-endpoint-protection.md)) that
  presents credentials.
- **Authenticator** — the switch or wireless controller the endpoint
  connects to, which relays credentials and enforces the result by opening
  or holding the port.
- **Authentication server** — typically ISE, which evaluates the
  credentials against policy and tells the authenticator what access to
  grant.

The exchange uses **EAP (Extensible Authentication Protocol)** over the
LAN, with **RADIUS** between the authenticator and the server. The
outcome is not merely allow/deny: the server can return a VLAN, an access
list, or a security group — access shaped to identity, not a binary gate.

**What about devices that cannot do 802.1X?** Printers, cameras, and IoT
often have no supplicant. **MAB (MAC Authentication Bypass)** authenticates
them by MAC address — weaker, because a MAC is spoofable, which is exactly
why **profiling** (Chapter 06) exists to corroborate that a device
claiming to be a printer behaves like one.

### TrustSec: segmentation by identity

Traditional segmentation uses VLANs and access lists tied to network
location. **Cisco TrustSec** segments by *identity* instead, using
**Security Group Tags (SGTs)**: when a device authenticates, it is
assigned an SGT, and policy is written between groups ("employees may
reach the finance app; guests may not") rather than between subnets.

The advantage is that policy follows the identity regardless of where the
device connects or what IP it holds — which is the network-enforcement
expression of the zero-trust model
[Chapter 08](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)
builds on. SGTs are assigned at authentication (by ISE) and enforced in
the network fabric, decoupling policy from topology.

### Visibility: you cannot secure what you cannot see

Enforcement depends on visibility, and SCOR treats telemetry as a security
control:

- **NetFlow** records conversations — who talked to whom, how much, over
  what — without capturing payloads. It is the flow-level record that
  reveals reconnaissance, exfiltration, and lateral movement as patterns.
- **Encrypted Traffic Analytics (ETA)** infers malicious intent from
  metadata of encrypted flows *without decrypting them* — using the
  characteristics of the flow rather than its contents. This matters
  because a growing majority of traffic is encrypted, and decrypting all
  of it is neither practical nor always permitted.
- **Cisco Secure Network Analytics** (formerly Stealthwatch) consumes this
  telemetry to detect anomalies — the behavioral analytics counterpart to
  the endpoint's EDR.

The lateral-movement threat is caught here: an attacker moving between
internal hosts generates flow patterns that visibility tooling can flag,
even when each individual connection looks ordinary.

## Design Considerations

- **Deploy 802.1X in monitor mode first.** Enforcing authentication before
  you know what is on the network locks out legitimate devices. Monitor
  mode reveals what would fail, so you can fix it before enforcing — the
  single most important 802.1X rollout practice.
- **Plan for the un-authenticatable device.** Printers, cameras, badge
  readers, and IoT will not do 802.1X; decide how MAB and profiling handle
  them before enforcement, or they become the outage.
- **Segment by identity where topology cannot express policy.** TrustSec
  earns its complexity when policy needs to follow users across a fabric;
  for a small, stable network, VLANs and ACLs may suffice. Match the tool
  to the need.
- **Treat telemetry as always-on, not incident-triggered.** NetFlow and
  ETA are valuable because they are already recording when an incident is
  discovered; turning them on afterward loses the history that explains
  what happened.
- **Design the RADIUS path for availability.** If ISE is the
  authentication server and it is unreachable, every new connection
  depends on your fallback policy. Decide whether unreachable means
  fail-open (available, insecure) or fail-closed (secure, disruptive)
  before you find out the hard way.

## Implementation and Automation

The switch-side configuration is the SCOR-level view; the ISE-side is
Chapter 06.

### 1. Configuring an 802.1X access port

On an IOS XE switch (the authenticator), the essentials:

```text
! RADIUS server (ISE) for authentication and authorization
radius server ISE
 address ipv4 10.1.100.10 auth-port 1812 acct-port 1813
 key <shared-secret>

aaa new-model
aaa authentication dot1x default group radius
aaa authorization network default group radius

! Access port doing 802.1X with MAB fallback, in monitor mode first
interface GigabitEthernet1/0/10
 switchport mode access
 authentication host-mode multi-auth
 authentication open              ! monitor mode: log, do not enforce yet
 dot1x pae authenticator
 mab
 authentication port-control auto
```

`authentication open` is monitor mode — the port authenticates and logs
but does not block. Removing it is the step from monitoring to enforcement,
taken only once the logs show legitimate devices succeeding.

### 2. Verifying authentication sessions

```text
! Who is authenticated on this switch, by what method, with what result?
show authentication sessions
show authentication sessions interface GigabitEthernet1/0/10 details

! Is the RADIUS server reachable and answering?
show aaa servers | include RADIUS|SUCCESS|FAIL
```

### 3. Reading flow telemetry

```text
! Flexible NetFlow: confirm the flow record is capturing conversations
show flow monitor NETFLOW-MON cache format table
```

Flow data is the input to the analytics platform; confirming the switch
is exporting it is the equivalent of confirming a log source is live.

## Validation and Troubleshooting

### The 802.1X decision walk

When a device cannot get on the network, walk the model in order:

| Stage | Check | Failure means |
| --- | --- | --- |
| Supplicant | Is the endpoint configured for 802.1X? | No credentials sent; falls to MAB or fails |
| Authenticator | `show authentication sessions` | Switch not relaying, or port misconfigured |
| RADIUS path | `show aaa servers` | Server unreachable — fallback policy decides |
| Server policy | ISE live logs (Chapter 06) | Authenticated but authorization denied |

The frequent real-world cause is not authentication failing but
*authorization* returning less access than expected — the credentials are
valid, but policy assigned a restricted result. That distinction is a
SCOR-level troubleshooting skill.

### Monitor mode as a diagnostic

The reason monitor mode matters is that it turns "authentication is broken"
into data before it becomes an outage. Deployed in monitor mode, the
`show authentication sessions` output reveals exactly which devices would
be denied and why, letting you fix profiling and policy before enforcement
turns denials into disconnections.

## Security and Best Practices

- **Do not rely on MAB alone for security.** A MAC address is spoofable;
  MAB is a bypass for devices that cannot authenticate, corroborated by
  profiling, not a security control on its own.
- **Enforce, eventually.** Monitor mode is a rollout stage, not a
  destination. A network permanently in monitor mode has the configuration
  of access control and none of the enforcement.
- **Segment to contain, not only to organize.** The security value of
  segmentation is limiting lateral movement; design it against the
  breach-containment goal, not only for administrative tidiness.
- **Keep telemetry flowing to a collector that survives the endpoint.**
  Flow records held only on a compromised device are evidence an attacker
  can erase; export them.
- **Protect the RADIUS shared secret and the ISE path.** The
  authentication server and its trust are tier-0; the whole access-control
  model rests on them.

## References and Knowledge Checks

**References**

- [Cisco 350-701 SCOR exam topics](https://learningnetwork.cisco.com/s/scor-exam-topics)
  — the Secure Network Access, Visibility, and Enforcement domain.
- [Chapter 06](06-identity-services-engine-deployment-policy-and-services.md)
  — ISE, which implements the authentication server and policy this
  chapter configures the switch side of.
- [Volume III, Chapter 07](../../volume-03-cisco-enterprise-networking/chapters/07-cisco-identity-access-control-and-segmentation.md)
  — access control and segmentation in the enterprise networking track.
- [Volume II, Chapter 03](../../volume-02-network-engineering-foundations/chapters/03-ethernet-switching-vlans-and-layer-2-resilience.md)
  — the switching and VLAN foundation 802.1X and TrustSec sit on.

**Knowledge checks**

1. Name the three 802.1X roles and what each does, and the protocols
   between them.
2. Why does MAB exist, and why is profiling necessary alongside it?
3. What does TrustSec segment by that VLAN-and-ACL segmentation does not,
   and why does that matter?
4. How can Encrypted Traffic Analytics flag malicious traffic without
   decrypting it, and why is that valuable?
5. A device authenticates successfully but gets less access than expected.
   Is this an authentication or authorization problem, and where do you
   look?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **SCOR (350-701)
Domain 6 (Secure Network Access, Visibility, and Enforcement)** — identity
and access, 802.1X/MAB, CoA, exfiltration detection, telemetry/NAT
visibility, Duo, and security automation — mapped in the volume README's
coverage tables. The deep ISE treatment is Chapter 06 (SISE); this is the
SCOR-level coverage. Each ends **`**Lab verified by:** *pending*`** until a
human runs it.

**Shared prerequisites for Labs 5.1–5.8** — a Catalyst switch as the NAD, ISE
as the RADIUS server, NetFlow/Stealthwatch (Secure Network Analytics) and
Duo where noted. **Cost:** none beyond lab resources.

### Lab 5.1 — Describe identity and secure network access (Objective 6.1)

**Objective:** Read the identity-driven access on a live session.

```text
SW# show authentication sessions interface gig1/0/5 details
```

**Expected result:** the session's user/endpoint identity, method, and
authorization result — access decided by identity, not port.

**Negative test:** open ports with no identity grant anyone access; 802.1X/MAB
ties access to identity.

**Cleanup:** none (read-only).

### Lab 5.2 — Describe device compliance and application control (Objective 6.2)

**Objective:** Read the compliance/posture result gating access.

```text
SW# show authentication sessions interface gig1/0/5 details | include Compliance|SGT|ACS ACL
```

**Expected result:** the posture/compliance status and the resulting policy
(quarantine dACL if non-compliant) — health-gated access.

**Negative test:** granting full access before compliance is confirmed lets an
unpatched device on; gate on Compliant.

**Cleanup:** none (read-only).

### Lab 5.3 — Configure 802.1X and MAB (Objective 6.3)

**Objective:** Configure concurrent 802.1X + MAB on an access port.

```text
SW(config)# interface gig1/0/5
SW(config-if)# access-session port-control auto
SW(config-if)# dot1x pae authenticator
SW(config-if)# mab
SW(config-if)# service-policy type control subscriber DOT1X-MAB
SW# show access-session interface gig1/0/5
```

**Expected result:** the port trying 802.1X first, then MAB — a supplicant-
capable device does 802.1X; a printer falls back to MAB.

**Negative test:** MAB before 802.1X (wrong priority) authenticates a
spoofable MAC when a supplicant was available; 802.1X should be preferred.

**Cleanup:** reset the interface to default.

### Lab 5.4 — Configure Change of Authorization (Objective 6.4)

**Objective:** Enable the switch to accept CoA from ISE.

```text
SW(config)# aaa server radius dynamic-author
SW(config-locsvr-da-radius)# client 10.0.0.50 server-key <key>
SW# show authentication sessions | include Reauth
```

**Expected result:** the switch accepting CoA on UDP 1700 — ISE can re-
authorize or bounce a live session (e.g. after profiling or a threat signal).

**Negative test:** without `dynamic-author`, ISE's CoA is ignored and policy
changes do not apply to live sessions until reconnect.

**Cleanup:** `no aaa server radius dynamic-author`.

### Lab 5.5 — Explain exfiltration techniques (Objective 6.5)

**Objective:** Detect a DNS-tunneling pattern in flow data.

```text
SW# show flow monitor MON cache | include 53
# or on Stealthwatch: long-duration/high-volume DNS to one host
```

**Expected result:** anomalous DNS (many/large TXT queries to one domain) —
the signature of DNS tunneling exfiltration.

**Negative test:** allowing all DNS outbound enables tunneling; DNS-layer
security (Umbrella/Secure Access) and flow analytics catch it.

**Cleanup:** none (read-only).

### Lab 5.6 — Describe network visibility and enforcement (Objective 6.6)

**Objective:** Read NetFlow/telemetry feeding Secure Network Analytics.

```text
SW# show flow exporter statistics
SW# show flow monitor MON cache format table
```

**Expected result:** flow records exported to Stealthwatch/SNA for
behavioral detection — visibility that turns into enforcement (via ISE ANC).

**Negative test:** enforcement without visibility is blind; the telemetry is
what detects the anomaly to enforce against.

**Cleanup:** none (read-only).

### Lab 5.7 — Describe Cisco Duo in zero trust (Objective 6.7)

**Objective:** Read Duo's trust-monitor / device-trust posture.

```bash
curl -sk -H "$DUO" "https://api-<host>.duosecurity.com/admin/v1/endpoints" | jq -r '.response[0].trust_level' 2>/dev/null || echo "Duo: MFA + device trust in the ZT access decision"
```

**Expected result:** Duo evaluating user MFA and device trust as part of the
access decision — the identity pillar of zero trust (Chapter 08).

**Negative test:** MFA without device trust admits a valid credential on a
compromised device; both are checked.

**Cleanup:** none (read-only).

### Lab 5.8 — Describe security orchestration and automation (Objective 6.8)

**Objective:** Read an automated security response (SOAR/XDR).

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/workflows?type=response" | jq -r '.data[].name' 2>/dev/null | head || echo "SOAR: correlation -> ISE ANC quarantine, automatically"
```

**Expected result:** an orchestration workflow that, on detection,
automatically contains the endpoint (ISE ANC via pxGrid) — machine-speed
response.

**Negative test:** manual containment lags the attack; automation closes the
detect-to-contain loop.

**Cleanup:** none (read-only).

### Lab 5.9 — 802.1X with MAB fallback in monitor mode (integrative)

**Objective:** Configure and validate 802.1X with MAB fallback in monitor
mode, and read the authentication sessions and flow telemetry that make
the network visible.

**Prerequisites:** A switched lab with an IOS XE switch and ISE (Cisco
dCloud provides an integrated ISE lab; CML plus an ISE evaluation is the
self-hosted route). A test endpoint. No production access network.

**Procedure**

1. Configure a switch access port for 802.1X with MAB fallback in monitor
   mode (`authentication open`), pointing at ISE as the RADIUS server.
2. Connect a test endpoint configured as an 802.1X supplicant and read
   `show authentication sessions` — confirm it authenticated and note the
   method and result.
3. Connect a device with no supplicant (or disable it) and confirm it
   falls back to MAB, visible in the same output.
4. In ISE (Chapter 06 covers the detail), find the corresponding live
   authentication log entry and read the policy result.
5. Confirm NetFlow is exporting with `show flow monitor ... cache` and
   locate your test traffic in the flow record.

**Negative test**

6. Make the RADIUS server unreachable (block its address or stop the
   service) and connect a new endpoint. Observe how the port behaves under
   your fallback configuration — confirming whether your design fails open
   or closed, and demonstrating why that decision must be made
   deliberately rather than discovered. Restore reachability afterwards.

**Expected results**

- An access port authenticating both an 802.1X supplicant and a MAB
  device, visible in `show authentication sessions`.
- The matching authorization result read from ISE.
- Flow telemetry confirmed exporting.
- A demonstrated, understood fail-open-or-closed behavior when the
  authentication server is unreachable.

**Cleanup**

7. Return the switch port to its original configuration and end the lab
   session; the ISE policy detail carries into Chapter 06.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Secure network access is how an enterprise controls who and what may
connect and contains lateral movement once they do — the threat a
perimeter firewall cannot touch. 802.1X authenticates the connection
itself through the supplicant/authenticator/server model, returning not
just allow-or-deny but access shaped to identity, with MAB and profiling
handling devices that cannot authenticate themselves. TrustSec segments by
identity using security group tags so policy follows the user rather than
the topology, and NetFlow and Encrypted Traffic Analytics provide the
always-on visibility that turns lateral movement into a detectable
pattern. This SCOR domain is the vocabulary; the Identity Services Engine
in Chapter 06 is where most of it is implemented — and monitor-mode-first
is the rollout discipline that keeps enforcement from becoming an outage.

- [ ] Can explain the 802.1X role model and the EAP/RADIUS protocols.
- [ ] Can explain why MAB needs profiling alongside it.
- [ ] Can describe identity-based segmentation with SGTs.
- [ ] Can explain ETA's value for encrypted traffic.
- [ ] Can distinguish an authentication failure from an authorization one.
