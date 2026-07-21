# Chapter 02: Network Security with Cisco Secure Firewall and IPS

## Learning Objectives

- Distinguish the Cisco Secure Firewall platforms — ASA and FTD — and
  explain when each applies.
- Describe firewall policy construction: access control, NAT, and the
  order in which a packet is evaluated.
- Explain next-generation firewall inspection: application visibility,
  URL filtering, and intrusion prevention with Snort.
- Configure and read the core of a firewall policy, and diagnose why a
  flow is permitted or dropped.
- Apply network segmentation as a security control rather than only a
  routing decision.

## Theory and Architecture

### Why this is the heaviest SCOR domain

Network Security is **25% of SCOR v2.0**, the single largest domain and up
from 20% in v1.1. That reflects where enterprise security still
concentrates: the firewall is the most-deployed enforcement point, and
Cisco's Secure Firewall line is the product SCOR most expects you to
reason about. This chapter is where a candidate should spend the most
SCOR study time, which is why the volume's plan gives it two weeks.

### Two firewall platforms: ASA and FTD

Cisco Secure Firewall runs two operating systems, and knowing which is
which is foundational:

- **ASA (Adaptive Security Appliance)** — the long-established stateful
  firewall OS. Configured through a CLI that a routing-and-switching
  engineer finds familiar, plus ASDM for a GUI. Strong at stateful
  filtering, NAT, and VPN termination; limited in application-layer
  visibility on its own.
- **FTD (Firepower Threat Defense)** — the next-generation platform,
  unifying ASA-style firewalling with Snort-based intrusion prevention,
  application visibility, and URL filtering. Managed centrally through
  **FMC (Secure Firewall Management Center)** or, for smaller
  deployments, **FDM (device manager)** on the box.

The same hardware often runs either image. SCOR expects you to know that
FTD is the strategic direction and where its capabilities exceed ASA's,
while still understanding ASA because it remains widely deployed and its
CLI concepts carry into VPN configuration in
[Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md).

### The stateful model, and why order matters

A stateful firewall tracks connections, not just packets: it permits
return traffic for a connection it already allowed outbound, without a
separate rule. Understanding the **order of operations** on a flow is the
skill that separates configuring a firewall from troubleshooting one.

On FTD, a packet is evaluated roughly in this order:

1. **Prefilter / fastpath** — early, coarse decisions before deep
   inspection.
2. **Access control policy** — the main rule set: match on zone, network,
   port, application, URL, and user, then allow, block, or inspect.
3. **NAT** — address translation, which interacts with access rules in
   ways that surprise people (rules match the real address, not the
   translated one, on modern releases).
4. **Intrusion and file policies** — for traffic the access policy sent to
   inspection, Snort evaluates it against signatures.

The recurring troubleshooting question — *why was this flow permitted or
dropped?* — is almost always answered by walking this order and finding
the stage that decided.

### Next-generation inspection

FTD's value over a stateful ASA is what it sees above layer 4:

- **Application visibility and control (AVC)** — identifying the actual
  application (not just the port), so a policy can permit a business app
  and block a tunneling tool sharing port 443.
- **URL filtering** — category- and reputation-based web control,
  overlapping with the cloud-delivered security in
  [Chapter 03](03-cloud-security-and-the-secure-service-edge.md).
- **Intrusion prevention (IPS)** — the **Snort** engine matching traffic
  against signatures for known exploits, with tunable rule sets balancing
  security against false positives.
- **File and malware inspection** — extracting files from flows and
  checking them, integrating with the endpoint story in
  [Chapter 04](04-content-security-and-endpoint-protection.md).

### Segmentation as a security control

Segmentation appears in this domain and again in
[Chapter 05](05-secure-network-access-visibility-and-enforcement.md), and
SCOR treats it as security, not merely design. The principle: limit
lateral movement by ensuring a compromised host cannot reach everything.
Firewalls enforce segmentation at boundaries; TrustSec and ISE
(Chapters 05–06) enforce it dynamically by identity. This chapter's share
is the enforced-at-a-boundary case — inter-zone access control that treats
internal traffic as worth filtering, not only the perimeter.

## Design Considerations

- **Choose FTD for new deployments unless a specific reason argues
  otherwise.** It is the strategic platform and the one SCOR weights
  toward. ASA remains correct where an existing investment, a specific VPN
  feature, or raw throughput simplicity dictates.
- **Design the access policy top-down and specific-first.** Rules are
  evaluated in order; a broad early rule shadows narrower later ones. The
  most common policy defect is an allow rule that matches more than
  intended because it sits above the block that should have caught it.
- **Decide where deep inspection is worth its cost.** IPS and file
  inspection consume resources and add latency. Applying them everywhere
  is neither necessary nor free; apply them where the risk is, and
  fastpath what does not need them.
- **Plan NAT and access rules together.** On modern FTD, access rules
  match real addresses while NAT translates them; reasoning about them
  separately produces rules that do not match the traffic you expected.
- **Segment internally, not only at the edge.** A flat internal network
  behind a strong perimeter is the topology ransomware spreads across.
  Inter-zone filtering is a control, and SCOR expects you to treat it as
  one.

## Implementation and Automation

FTD is configured through FMC's GUI in practice; the concepts, though, are
inspectable from the device CLI, which is where troubleshooting happens.

### 1. Reading the access policy decision from the CLI

On FTD, the packet-tracer utility answers the "permitted or dropped"
question definitively by simulating a flow through the full order of
operations:

```text
> packet-tracer input INSIDE tcp 10.1.1.10 40000 203.0.113.5 443

Phase: 1  Type: ACCESS-LIST   ... Result: ALLOW
Phase: 2  Type: NAT           ... translate 10.1.1.10 -> 198.51.100.10
Phase: 3  Type: SNORT         ... 
Result: input-interface: INSIDE
        Action: allow
```

Each phase names the stage that made a decision. A `DROP` result names the
phase responsible — which is the answer to almost every "why is this
blocked" ticket.

### 2. Confirming connection state and NAT

```text
# Is the firewall actually tracking this connection?
> show conn address 10.1.1.10 protocol tcp

# What NAT rule is this flow hitting, and is it the one you intended?
> show nat detail

# IPS: is Snort seeing and acting on traffic?
> show snort statistics
```

### 3. Automating policy against FMC

FMC exposes a REST API, which is the SCOR automation story applied to the
firewall and developed further in
[Chapter 09](09-designing-security-infrastructure-automation-and-capstone.md):

```bash
# Authenticate to FMC and retrieve the access control policies.
# Token handling omitted; store credentials in a vault, never inline.
curl -sk -X POST "https://fmc.example.com/api/fmc_platform/v1/auth/generatetoken" \
  -u "$FMC_USER:$FMC_PASS" -D - | grep -i x-auth-access-token

curl -sk "https://fmc.example.com/api/fmc_config/v1/domain/$DOMAIN/policy/accesspolicies" \
  -H "X-auth-access-token: $TOKEN" | jq '.items[] | {name, id}'
```

Automating policy retrieval and audit is lower-risk and higher-value than
automating policy change; build read-only tooling first, exactly as the
VxRail and iDRAC volumes argue for their platforms.

## Validation and Troubleshooting

### The order-of-operations method

Every firewall troubleshooting problem is answered by locating the stage
that decided the flow's fate:

| Symptom | First check | Likely stage |
| --- | --- | --- |
| Flow blocked, expected allowed | `packet-tracer` | Access policy — a shadowing rule above the intended allow |
| Flow allowed, expected blocked | `packet-tracer` | Access policy — a broad rule matching too much |
| Connects then breaks under load | `show conn`, IPS logs | Snort dropping on a signature |
| Works one direction only | `show nat detail` | NAT translating unexpectedly |
| Intermittent, app-specific | AVC/application logs | Application misidentified or reclassified |

The discipline is to run `packet-tracer` *first* and let it name the
stage, rather than guessing and reconfiguring.

### The false-positive problem

IPS tuning is a validation skill SCOR expects. A signature set that blocks
a legitimate application is as much a failure as one that misses an
attack. The method: identify the triggering rule from the intrusion
events, judge whether the traffic is genuinely malicious, and either tune
the rule's action or fix the traffic — never blanket-disable a category to
make a symptom disappear, which is the reflex that leaves real gaps.

## Security and Best Practices

- **Protect FMC as tier-0.** It controls every managed firewall;
  compromising it compromises the entire enforced boundary. Restrict its
  management network, use strong authentication, and log administrative
  access.
- **Default-deny, then permit deliberately.** The access policy should end
  in a deny and permit only what is understood. An implicit or trailing
  broad allow is the defect that makes a firewall decorative.
- **Keep IPS signatures current.** Snort's value is only as good as its
  rule set; stale signatures miss current exploits. Signature currency is
  the IPS equivalent of patching.
- **Log at the boundary and send it somewhere.** Firewall logs are the
  raw material for the visibility in
  [Chapter 05](05-secure-network-access-visibility-and-enforcement.md) and
  the incident response in
  [Chapter 09](09-designing-security-infrastructure-automation-and-capstone.md).
  A firewall that drops silently is a firewall you cannot investigate.
- **Separate management, data, and failover paths.** The same discipline
  the iDRAC and VxRail volumes apply to platform management applies here.

## References and Knowledge Checks

**References**

- [Cisco Secure Firewall documentation](https://www.cisco.com/c/en/us/support/security/firepower-ngfw/series.html)
  — the authoritative source for FTD, FMC, and ASA configuration.
- [Cisco 350-701 SCOR exam topics](https://learningnetwork.cisco.com/s/scor-exam-topics)
  — the Network Security domain's full subtopic list.
- [Volume III, Chapter 07](../../volume-03-cisco-enterprise-networking/chapters/07-cisco-identity-access-control-and-segmentation.md)
  — access control and segmentation in the enterprise networking context.
- [Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md)
  — VPN termination on the same Secure Firewall platforms.

**Knowledge checks**

1. Distinguish ASA from FTD and state when each is the right choice.
2. Give the FTD order of operations and explain why it determines
   troubleshooting method.
3. What does application visibility let a policy do that a port-based rule
   cannot?
4. A flow is blocked that should be allowed. What is your first action,
   and what does it tell you?
5. Why is blanket-disabling an IPS category the wrong response to a false
   positive?

## Hands-On Lab

**Objective:** Build, exercise, and troubleshoot a Secure Firewall access
policy, using `packet-tracer` to prove why flows are permitted or dropped.

**Prerequisites:** An FTD/FMC environment — Cisco dCloud provides one
without purchase, or a Secure Firewall evaluation in a hypervisor per the
volume's *Practicing* section. No production firewall.

**Procedure**

1. In dCloud or your eval FMC, build an access control policy with three
   zones (inside, outside, DMZ) and rules that permit specific
   applications inside-to-outside while blocking the rest.
2. Add an intrusion policy to one allow rule and confirm Snort is
   inspecting that traffic with `show snort statistics`.
3. From the CLI, run `packet-tracer` for a flow you expect to be allowed.
   Read each phase and confirm the access, NAT, and Snort stages behave as
   designed.
4. Run `packet-tracer` for a flow you expect to be blocked. Confirm the
   result names the access-policy phase as the one that dropped it.
5. Deliberately create a shadowing rule: place a broad allow above a
   specific block, then use `packet-tracer` to show the traffic hitting
   the wrong rule. Reorder to fix it and re-verify.

**Negative test**

6. Configure NAT so that access rules reference the translated address
   rather than the real one (the common mistake). Observe the flow fail
   to match, then correct the rules to reference the real address and
   confirm with `packet-tracer` that the flow now matches — demonstrating
   why NAT and access rules must be reasoned about together.

**Expected results**

- A working three-zone policy that permits by application, not port.
- `packet-tracer` output that names the deciding stage for both an
  allowed and a blocked flow.
- Direct experience of a shadowing rule and a NAT-address mismatch, the
  two most common policy defects.

**Cleanup**

7. In dCloud, simply end the session. In an eval environment, remove the
   test policy or revert to a saved baseline so the next chapter starts
   clean.

## Summary and Completion Checklist

Network Security is SCOR's largest domain because the firewall is still
the enterprise's most-deployed enforcement point. Cisco Secure Firewall
runs two operating systems — ASA, the established stateful platform, and
FTD, the next-generation one with Snort IPS, application visibility, and
URL filtering — and FTD is the strategic direction. The skill that matters
most is not building a policy but reasoning about the order of operations:
access control, NAT, then intrusion inspection, in that order, is what
answers every "why was this flow permitted or dropped" question, and
`packet-tracer` names the deciding stage directly. Segmentation and IPS
tuning turn a firewall from a perimeter box into an internal security
control.

- [ ] Can distinguish ASA and FTD and choose correctly between them.
- [ ] Can state the FTD order of operations and use it to troubleshoot.
- [ ] Can build an application-aware access policy and read its decisions.
- [ ] Can diagnose a shadowing rule and a NAT mismatch with
      `packet-tracer`.
- [ ] Can tune IPS without disabling security wholesale.
