# Chapter 06: Identity Services Engine: Deployment, Policy, and Services

## Learning Objectives

- Describe ISE's architecture and the distributed persona/node model.
- Build the ISE policy set that drives 802.1X authentication and
  authorization.
- Explain ISE's services: profiler, guest and web authentication, BYOD,
  and posture.
- Configure ISE for TACACS+ device administration alongside RADIUS network
  access.
- Prepare for the SISE (300-715) concentration, whose weights this chapter
  is organized around.

## Theory and Architecture

### The SISE concentration, and this chapter's shape

This chapter is both the SCOR access domain's implementation and the whole
of the **SISE (300-715)** concentration. It is organized around SISE's
published weights, whose largest domain by far is **Policy Enforcement at
25%** — so that is where the depth goes. SISE v1.1 and v1.2 share identical
weights; the August 2026 transition changes the edition label, not the
study.

The SISE domains and where each is covered:

| SISE domain | Weight | Section |
| --- | --- | --- |
| Policy Enforcement | 25% | *Policy sets* below |
| Web Auth and Guest Services | 15% | *Guest and web authentication* |
| Profiler | 15% | *Profiling* |
| BYOD | 15% | *BYOD* |
| Architecture and Deployment | 10% | *Architecture* below |
| Endpoint Compliance | 10% | *Posture* |
| Network Access Device Administration | 10% | *TACACS+ device admin* |

### Architecture: personas and nodes

ISE is a distributed system, and its **persona** model is the
architectural core SISE tests. A single ISE deployment runs several
personas, which can be co-located on one node in a lab or spread across
many for scale and resilience:

- **Policy Administration Node (PAN)** — the management and configuration
  plane; where policy is authored. One primary, one secondary.
- **Monitoring node (MnT)** — collects logs and provides the reporting and
  live-log views used for troubleshooting.
- **Policy Service Node (PSN)** — the workhorse that actually processes
  authentication requests. In a large deployment there are many PSNs
  behind a load balancer; they are the RADIUS servers the switches from
  [Chapter 05](05-secure-network-access-visibility-and-enforcement.md)
  talk to.
- **pxGrid** — the publish/subscribe fabric that shares ISE's context
  (who is on the network, with what tags) with other Cisco security
  products, tying the portfolio together.

Understanding which persona does what is the key to both deployment design
and troubleshooting: an authentication problem is a PSN question, a policy
problem is a PAN question, and the evidence for both lives on the MnT.

### Policy sets: the 25% that matters most

ISE evaluates access through **policy sets**, and this is where SISE
concentrates its weight. A policy set has two stages, and keeping them
distinct is the single most important ISE concept:

1. **Authentication policy** — *who or what is this?* It validates the
   credential (a certificate, a username and password, a MAC address) and
   establishes identity, choosing an identity source (internal, Active
   Directory, LDAP, certificate).
2. **Authorization policy** — *what may they do?* Given the established
   identity and its context (device type from the profiler, posture
   status, location, time), it returns the result: a permit, a VLAN, a
   downloadable ACL, or a security group tag.

The recurring lesson from Chapter 05 lands here: authentication succeeding
and authorization granting access are different events. Most "it does not
work" tickets are authorization policy returning a result other than the
one expected, not authentication failing. Reading the policy set
top-down — because rules match in order, like a firewall policy — is the
core troubleshooting skill.

### Profiling

**Profiling** identifies *what a device is* without asking it. ISE gathers
attributes — DHCP fingerprints, HTTP user agents, SNMP data, active
scans — and matches them against profiles to conclude "this is an IP
phone" or "this is a Windows workstation." This is what makes MAB from
Chapter 05 tolerable: a device authenticating only by MAC is corroborated
by behaving like the device type it claims, so a spoofed printer MAC on a
laptop is caught by the laptop not matching the printer profile.

### Guest and web authentication

**Guest services** handle users who are not part of the corporate
identity store: a captive portal for visitors, sponsored guest accounts,
self-registration, and hotspot access. **Web authentication** redirects an
unauthenticated session to a portal for credential entry. These carry 15%
of SISE and are the most visible ISE feature to non-technical users, since
the guest portal is what a visitor actually sees.

### BYOD

**BYOD (bring your own device)** onboards personal devices securely:
provisioning a certificate to the device so it can do certificate-based
802.1X, registering it to a user, and applying policy appropriate to a
personal rather than corporate asset. It leans directly on the PKI
foundation from
[Chapter 01](01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md),
because the onboarding issues a certificate the device then authenticates
with.

### Posture

**Posture** assessment checks an endpoint's compliance before granting
full access — is the antivirus running, the OS patched, the disk
encrypted? A non-compliant device can be quarantined to a remediation
segment until it complies. Posture is assessed through the Cisco Secure
Client from
[Chapter 04](04-content-security-and-endpoint-protection.md), which is the
same agent carrying VPN and DNS security — the consolidated-endpoint design
paying off again.

### TACACS+ device administration

RADIUS controls *network access* (who gets on); **TACACS+** controls
*device administration* (who may log in to the switch itself, and what
commands they may run). ISE provides both. TACACS+ separates
authentication from per-command authorization, so an operator can be
allowed `show` commands but not `configure` — the administrative
least-privilege that protects the network devices themselves.

## Design Considerations

- **Size personas to the deployment.** A lab runs all personas on one
  node; production separates PAN, MnT, and multiple PSNs for scale and
  survivability. Design the PSN count and placement against authentication
  load and failure domains.
- **Author authorization policy from most-specific to least.** Like a
  firewall, ISE matches top-down; a broad early authorization rule shadows
  the specific ones beneath it. This is the most common ISE policy defect.
- **Design profiling before enforcing MAB.** Enforcement without reliable
  profiles turns every un-authenticatable device into a denial. Get
  profiling accurate in monitor mode first.
- **Plan PSN reachability and fallback.** The switches depend on reaching
  a PSN; if none is reachable, the switch's fallback policy (Chapter 05)
  governs. Design PSN redundancy so that fallback is rare.
- **Separate guest infrastructure from corporate.** Guest access is
  untrusted by definition; its portal, its segment, and its policy should
  assume the guest is hostile.

## Implementation and Automation

### 1. Building a policy set

Conceptually, in the ISE administration console, a policy set for wired
802.1X:

```text
Policy Set: Wired-Dot1X   (condition: Wired_802.1X)
  Authentication Policy:
    Rule "Dot1X"  -> use identity source: AD + Internal Certs
  Authorization Policy (top-down, specific first):
    Rule "Non-compliant"  if Posture=NonCompliant -> Quarantine dACL
    Rule "Employees"      if AD:group=Employees + Compliant -> Permit + SGT:Employee
    Rule "IP-Phones"      if EndPointPolicy=Cisco-IP-Phone -> Permit + Voice VLAN
    Default               -> Deny
```

The ordering is deliberate: the non-compliant check sits above the
employee permit, so a compliant employee's laptop that later falls out of
compliance is caught rather than retaining access.

### 2. Reading the live logs — the primary troubleshooting tool

```text
# In ISE: Operations > RADIUS > Live Logs
# Each entry shows: identity, the authentication result, the authorization
# policy rule matched, and the result (VLAN/dACL/SGT) returned.
```

The live log is where the authentication-versus-authorization distinction
becomes concrete: it shows whether the credential validated *and* which
authorization rule fired. Nearly every ISE problem is diagnosed here.

### 3. Automating with the ISE API (ERS and open APIs)

```bash
# Retrieve endpoint identities via the External RESTful Services API.
curl -sk "https://ise.example.com:9060/ers/config/endpoint" \
  -u "$ERS_USER:$ERS_PASS" -H "Accept: application/json" \
  | jq '.SearchResult.total'
```

As throughout the volume, read-only automation — inventory, audit, live
context via pxGrid — is the safe, high-value place to start.

## Validation and Troubleshooting

### The live-log method

ISE troubleshooting is overwhelmingly a live-log discipline:

| Symptom | Live log shows | Cause |
| --- | --- | --- |
| No access at all | No entry | Request never reached the PSN — network/RADIUS path |
| Authenticated, wrong access | Auth success, unexpected authz rule | Authorization policy ordering |
| Auth fails for valid user | Auth failure, identity-source error | AD/LDAP/cert trust problem |
| Device denied unexpectedly | Profiled as wrong type | Profiler misclassification |
| Access lost after being fine | Posture went non-compliant | Endpoint fell out of compliance |

The method is always the same: find the session in the live log, read
whether authentication succeeded, then read which authorization rule
matched and what it returned.

### The "authenticated but denied" pattern

This is the SISE troubleshooting archetype and worth internalizing: the
user's credential is perfectly valid, the live log shows authentication
success, and yet the device has no useful access — because the
authorization policy matched a restrictive rule. The fix is in the policy
ordering, not the credential. A candidate who instinctively checks the
password when the live log already shows auth success has not understood
the two-stage model.

## Security and Best Practices

- **Protect the PAN as tier-0.** It authors the policy that governs every
  network connection; its compromise is total. Restrict and log
  administrative access, and use TACACS+ to constrain even ISE's own
  administrators.
- **Default-deny authorization.** The policy set should end in a deny;
  every permit should be deliberate and specific, exactly as with a
  firewall.
- **Use certificate-based authentication where possible.** It is stronger
  than passwords and is what BYOD onboarding provisions; MAB is a fallback,
  not a target state.
- **Quarantine, do not merely flag, non-compliance.** Posture is only a
  control if a non-compliant device is actually restricted; a posture
  policy that reports without enforcing is telemetry, not enforcement.
- **Keep guest and corporate trust strictly separated.** Treat the guest
  path as hostile by design.

## References and Knowledge Checks

**References**

- [Cisco Identity Services Engine documentation](https://www.cisco.com/c/en/us/support/security/identity-services-engine/series.html)
  — the authoritative source for ISE deployment, policy, and services.
- [Cisco 300-715 SISE exam topics](https://learningnetwork.cisco.com/s/sise-exam-topics)
  — the concentration's full domain and subtopic list.
- [Chapter 05](05-secure-network-access-visibility-and-enforcement.md)
  — the switch-side 802.1X configuration ISE is the server for.
- [Chapter 01](01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md)
  — the PKI foundation BYOD certificate onboarding depends on.

**Knowledge checks**

1. Name the ISE personas and state which handles authentication requests,
   which holds policy, and which holds the logs.
2. Distinguish the authentication and authorization stages of a policy
   set, and explain why the distinction dominates troubleshooting.
3. Why does profiling make MAB acceptable, and what does it catch?
4. What does TACACS+ control that RADIUS does not?
5. A user authenticates successfully but has no useful access. Where do
   you look, and what is the likely cause?

## Hands-On Lab

**Objective:** Build an ISE policy set, drive 802.1X authorization with
it, and diagnose an "authenticated but denied" condition using the live
logs.

**Prerequisites:** An ISE deployment — Cisco dCloud offers an integrated
ISE lab with switches and endpoints; a self-hosted route is an ISE
evaluation OVA in a hypervisor with the Chapter 05 switch. No production
ISE.

**Procedure**

1. Confirm your ISE node's personas and that it is reachable as a RADIUS
   server from the Chapter 05 switch.
2. Build a policy set for wired 802.1X with an authentication rule against
   your identity source and an authorization policy with at least three
   ordered rules (a specific permit, a device-type rule, a default deny).
3. Authenticate a test endpoint and find the session in the RADIUS live
   logs. Read the authentication result and the authorization rule matched.
4. Confirm the endpoint received the access the matched rule specifies
   (VLAN, dACL, or SGT).
5. Configure profiling and connect a MAB device; confirm ISE profiles it
   and that authorization uses the profile.

**Negative test**

6. Reorder the authorization policy so a restrictive rule sits above the
   employee permit. Re-authenticate the test endpoint and observe it now
   authenticates successfully but receives restricted access. Use the live
log to confirm auth succeeded while the wrong authz rule matched — the
   "authenticated but denied" archetype — then fix the ordering and
   re-verify.

**Expected results**

- A working policy set authorizing an 802.1X endpoint by identity.
- A profiled MAB device authorized by device type.
- A deliberately induced "authenticated but denied" condition, diagnosed
  from the live log to the authorization ordering rather than the
  credential.

**Cleanup**

7. Restore the correct policy ordering, and end the dCloud or evaluation
   session.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Identity Services Engine implements most of the enforcement Chapter 05
introduces, and it is the whole of the SISE concentration. Its
distributed persona model — PAN for policy, PSN for processing
authentication, MnT for logs, pxGrid for context sharing — is the
architectural core, and its policy sets are where SISE concentrates its
weight. The two-stage policy model, authentication establishing *who* and
authorization deciding *what*, is the concept that dominates both
configuration and troubleshooting: the archetypal ISE problem is a valid
credential receiving unexpected access because authorization matched the
wrong rule, diagnosed from the live logs rather than the password. Around
that core sit profiler, guest and web authentication, BYOD, posture, and
TACACS+ device administration — each a SISE domain, each an application of
identity to a different access problem.

- [ ] Can describe the ISE persona model and what each persona does.
- [ ] Can build a two-stage policy set and explain the stages.
- [ ] Can explain profiling's role alongside MAB.
- [ ] Can distinguish RADIUS network access from TACACS+ device admin.
- [ ] Can diagnose "authenticated but denied" from the live logs.
