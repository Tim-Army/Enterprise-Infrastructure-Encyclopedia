# Chapter 03: Cloud Security and the Secure Service Edge

## Learning Objectives

- Explain the shared-responsibility model and what it means for securing
  cloud workloads.
- Describe cloud-delivered security and the DNS-layer control Cisco
  Umbrella provides.
- Define the secure service edge (SSE) and SASE, and place Cisco's
  offering within them.
- Distinguish the SCOR Cloud Security and Secure Service Edge domains, and
  connect them to the SCAZT concentration.
- Apply cloud and edge controls to the threat classes from Chapter 01.

## Theory and Architecture

### Two domains, one subject

SCOR v2.0 carries **Cloud Security at 15%** and a new **Secure Service
Edge domain at 10%**. They are closely related, which is why this chapter
covers both, and the SSE domain is the clearest signal of Cisco's
strategic direction — the same subject the
[SCAZT concentration](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)
develops in full. The v1.1-to-v2.0 change that added the SSE domain is the
one most worth understanding, because it reflects where enterprise
security is actually moving: away from a fixed perimeter and toward a
cloud-delivered enforcement layer users reach wherever they are.

### The shared-responsibility model

Cloud security begins with knowing which security is yours. In every cloud
service model the provider secures some layers and the customer secures
others, and the boundary moves with the model:

- **Infrastructure as a service** — the provider secures the physical and
  virtualization layers; you secure the OS, applications, data, and
  network configuration.
- **Platform as a service** — the provider secures up to the runtime; you
  secure your code and data.
- **Software as a service** — the provider secures the application; you
  secure identity, access, and how data is used.

The recurring failure is assuming the provider covers more than it does —
an exposed storage bucket or an over-permissive identity is the customer's
responsibility in every model. SCOR expects you to place the boundary
correctly for a given service.

### Cloud-delivered security and the DNS layer

Cisco's cloud-delivered security centers on **Umbrella**, and its most
distinctive control is at the **DNS layer**. Because nearly every
connection begins with a DNS lookup, resolving names through a security
service lets you block malicious destinations before a connection is even
attempted — earlier and cheaper than inspecting the traffic after it
starts.

DNS-layer security answers several Chapter 01 threats at once:
command-and-control callbacks, phishing domains, and malware distribution
sites are blocked at resolution. It is not a complete control — it does
not inspect payloads — but it is a high-value, low-cost first line, and
SCOR expects you to know why the DNS layer is a security enforcement point
and not merely a name service.

Beyond DNS, cloud-delivered security adds a **secure web gateway**
(full web traffic inspection), **cloud-access security broker (CASB)**
functions (visibility and control over SaaS use), and **cloud firewall**
capabilities — the components that assemble into the service edge.

### Secure service edge and SASE

**SASE (secure access service edge)** is the convergence of networking
(SD-WAN) and security (SSE) into a single cloud-delivered service.
**SSE (secure service edge)** is the security half: secure web gateway,
CASB, zero-trust network access (ZTNA), and cloud firewall, delivered from
the cloud rather than from an appliance in a data center.

The architectural shift SSE represents: instead of backhauling a remote
user's traffic to a central firewall and out, the user connects to the
nearest cloud enforcement point, which applies policy and forwards the
traffic. This is faster for the user and enforces policy identically
regardless of location — which is the point of the zero-trust model
[Chapter 08](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)
builds on.

Cisco's SSE offering assembles Umbrella's gateway and DNS security, ZTNA,
and related controls. SCOR expects the model and the component names, not
a specific console; SCAZT goes deep on the implementation.

### Securing cloud workloads

Distinct from securing *access* to the cloud is securing the *workloads*
running in it: cloud-native firewalls, workload segmentation, posture
management (finding misconfigurations like the exposed bucket above), and
visibility into east-west traffic between cloud instances. This is where
the SCOR Cloud Security domain overlaps with the design thinking in
[Chapter 09](09-designing-security-infrastructure-automation-and-capstone.md)
and the application-and-data focus of SCAZT.

## Design Considerations

- **Place the responsibility boundary before designing controls.** The
  IaaS/PaaS/SaaS distinction determines what you must secure; designing
  controls without fixing the boundary produces gaps and duplication both.
- **Use DNS-layer security as the first line, not the only line.** It is
  cheap, early, and broad, but it does not inspect payloads. Layer a
  secure web gateway behind it for the traffic that matters.
- **Prefer the service edge to backhaul for a distributed workforce.**
  Hauling remote users' traffic to a central firewall adds latency and
  scales poorly; the SSE model enforces policy closer to the user. Where
  the workforce is centralized, the appliance model may still be simpler.
- **Treat SaaS visibility as a real requirement.** Unmanaged SaaS use
  ("shadow IT") is a data-exfiltration path; CASB functions exist to see
  and control it, and a design that ignores it has an open flank.
- **Do not confuse SASE the concept with any one product.** SASE is an
  architecture; vendors assemble it from different components. SCOR tests
  the model; buy against the requirements, not the acronym.

## Implementation and Automation

This domain is largely cloud-console and API driven; the CLI role is
smaller than in Chapter 02.

### 1. Confirming DNS-layer enforcement

DNS security is only working if clients actually resolve through it.
Confirm the resolution path:

```bash
# Which resolver is answering, and is it the security service?
dig +short whoami.umbrella.com any
# Umbrella returns diagnostic records confirming the request egressed
# through its service; a plain answer means clients are bypassing it.

# Test that a known-malicious category is actually blocked. Umbrella
# publishes test domains that resolve to a block page when protection is
# in the path — examplemalwaredomain.com and examplephishingdomain.com.
dig +short examplemalwaredomain.com
```

The common failure is clients configured with a public resolver that
bypasses the security service entirely — the control is deployed but not
in the path.

### 2. Auditing cloud posture programmatically

Posture management — finding the exposed bucket before an attacker does —
is API work:

```bash
# Illustrative: enumerate storage exposed to the public, the canonical
# shared-responsibility failure. Provider CLI shown generically.
cloud storage list --query "buckets[?public==\`true\`].name"
```

Automating the search for misconfiguration is higher-value than reacting
to alerts about it, and it is the cloud application of the read-only-first
automation principle the volume repeats.

## Validation and Troubleshooting

### Is the control actually in the path?

The defining cloud-security validation question is whether traffic
actually traverses the control:

| Control | "Is it in the path?" check |
| --- | --- |
| DNS-layer security | `dig whoami.umbrella.com` returns service diagnostics, not a plain answer |
| Secure web gateway | Traffic to a test URL shows the gateway's headers or block page |
| ZTNA | Application is unreachable without the client; reachable with it |
| CASB | Sanctioned SaaS appears in the console; unsanctioned use is visible |

A control that is configured but bypassed is worse than one known to be
absent, because it produces false confidence — the same lesson the
VxRail and iDRAC volumes draw about call-home and alerting.

### Latency and the backhaul question

When remote users complain of slowness, the frequent cause is backhaul:
traffic hauled to a central firewall and back. The service-edge model
exists to fix this. Diagnosing it means confirming where enforcement
happens relative to where the user is — a design question surfacing as a
performance symptom.

## Security and Best Practices

- **Enforce DNS security everywhere, including off-network.** A roaming
  client that reverts to a public resolver when it leaves the office has
  lost the control exactly when it is most exposed. The endpoint client in
  [Chapter 04](04-content-security-and-endpoint-protection.md) is how DNS
  security follows the user.
- **Assume SaaS data leaves your control unless CASB says otherwise.**
  Visibility precedes control; you cannot govern what you cannot see.
- **Right-size cloud identity and permissions.** Over-permissive cloud
  identities are the most common breach root cause; least privilege
  (Chapter 01) applies to cloud IAM as strictly as to firewall rules.
- **Encrypt in transit and at rest, and manage the keys deliberately.**
  The PKI foundation from Chapter 01 governs cloud data protection as much
  as VPNs.
- **Log cloud control-plane actions.** The audit trail of who changed what
  in the cloud console is tier-0 evidence for the incident response in
  Chapter 09.

## References and Knowledge Checks

**References**

- [Cisco Umbrella documentation](https://docs.umbrella.com/)
  — DNS-layer security, secure web gateway, and CASB functions.
- [Cisco 350-701 SCOR exam topics](https://learningnetwork.cisco.com/s/scor-exam-topics)
  — the Cloud Security and Secure Service Edge domain subtopics.
- [Chapter 08](08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)
  — the SCAZT concentration, which develops SSE and zero trust in full.
- [Volume VII — Cloud Infrastructure](../../volume-07-cloud-infrastructure/README.md)
  — the cloud fundamentals the shared-responsibility model assumes.

**Knowledge checks**

1. Place the security responsibility boundary for IaaS, PaaS, and SaaS.
2. Why is the DNS layer a valuable security enforcement point, and what
   can it not do?
3. Define SSE and SASE and state the relationship between them.
4. Explain how the service-edge model changes a remote user's traffic
   path versus backhaul.
5. A DNS-layer control is deployed but not blocking anything. What is the
   most likely cause?

## Hands-On Lab

**Objective:** Prove that a cloud-delivered security control is in the
traffic path, and observe the difference DNS-layer enforcement makes.

**Prerequisites:** A Cisco Umbrella evaluation or dCloud environment, and
a client you can point at its resolvers. No production cloud tenancy.

**This lab is reproducible with an evaluation account.** Umbrella offers
one, and its test domains make enforcement observable without exposing
real systems to real threats.

**Procedure**

1. Point a lab client's DNS at the Umbrella resolvers and confirm the path
   with `dig whoami.umbrella.com any` — verify you get service diagnostics,
   not a plain answer.
2. Attempt to resolve Umbrella's malware/phishing test domains and confirm
   they return a block response rather than the real address.
3. In the Umbrella console, review the activity log and find your test
   lookups — confirming visibility as well as enforcement.
4. Configure a category or destination block, then demonstrate it from the
   client.
5. Review the SSE component list in the console and map each (DNS
   security, secure web gateway, CASB) to a Chapter 01 threat it answers.

**Negative test**

6. Reconfigure the client to use a public resolver instead of Umbrella,
   then re-run the test-domain lookups. Confirm the malicious domains now
   resolve normally — demonstrating that a bypassed control provides no
   protection, and that verifying the *path* matters as much as the
   configuration. Restore the Umbrella resolvers afterwards.

**Expected results**

- Confirmed DNS-layer enforcement, proven by service diagnostics and
  blocked test domains.
- Visibility of your own lookups in the activity log.
- Direct demonstration that a bypassed resolver defeats the control.

**Cleanup**

7. Restore the client's original DNS settings and end the evaluation
   session; retain the SSE-to-threat mapping for Chapter 08.

## Summary and Completion Checklist

Cloud security starts with the shared-responsibility boundary, which moves
with the service model and whose misjudgment causes the exposed-bucket
class of breach. Cisco's cloud-delivered security centers on Umbrella,
whose DNS-layer control blocks malicious destinations before a connection
is attempted — an early, broad, cheap first line that does not replace
payload inspection. The secure service edge converges secure web gateway,
CASB, ZTNA, and cloud firewall into a cloud-delivered enforcement layer
users reach wherever they are, which SCOR v2.0 recognized by adding an SSE
domain and which the SCAZT concentration develops fully. Across all of it,
the defining validation question is whether the control is actually in the
traffic path — a configured-but-bypassed control is false confidence.

- [ ] Can place the responsibility boundary across IaaS, PaaS, and SaaS.
- [ ] Can explain DNS-layer security's value and its limit.
- [ ] Can define SSE and SASE and relate them.
- [ ] Can verify a cloud control is in the traffic path.
- [ ] Can connect each SSE component to the threat it answers.
