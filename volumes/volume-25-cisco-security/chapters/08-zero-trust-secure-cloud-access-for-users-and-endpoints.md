# Chapter 08: Zero-Trust Secure Cloud Access for Users and Endpoints

## Learning Objectives

- Explain zero trust as an architecture and how it differs from
  perimeter security.
- Describe zero-trust network access (ZTNA) and how it replaces
  traditional VPN for application access.
- Apply user, device, application, and data security in a secure cloud
  access design.
- Explain the visibility, assurance, and threat-response requirements of
  the SCAZT concentration.
- Situate SCAZT within Cisco's secure-service-edge direction from
  Chapter 03.

## Theory and Architecture

### The SCAZT concentration and its weight

This chapter is the **SCAZT (300-740)** concentration —
*Designing and Implementing Secure Cloud Access for Users and Endpoints* —
the newest of the four covered here and the one most aligned with where
Cisco security is heading. Its weights:

| SCAZT domain | Weight |
| --- | --- |
| Application and Data Security | **25%** |
| User and Device Security | 20% |
| Network and Cloud Security | 20% |
| Visibility and Assurance | 15% |
| Cloud Security Architecture | 10% |
| Threat Response | 10% |

The largest domain is application and data security, and the whole exam is
weighted toward *protecting what users reach* rather than *building
network plumbing* — which is the zero-trust shift made examinable.

### Zero trust: the model that assumes breach

Traditional security trusts the network: inside the perimeter is
trusted, outside is not. **Zero trust discards that assumption.** Its
premise is "never trust, always verify" — every access request is
authenticated, authorized, and encrypted regardless of where it comes
from, because the network location tells you nothing about whether a
request is legitimate.

The Chapter 01 threats this answers: a compromised insider, a stolen
credential, or lateral movement all defeat perimeter trust, because they
originate *inside*. Zero trust removes the free pass that being "inside"
grants, so a compromised host must still authenticate and be authorized
for every resource it reaches.

Zero trust rests on a few principles SCAZT expects you to apply:

- **Verify explicitly** — authenticate and authorize on identity, device
  health, and context for every request.
- **Least-privilege access** — grant only what the request needs, for as
  long as it needs it (Chapter 01's organizing principle).
- **Assume breach** — design as though an attacker is already inside;
  segment, monitor, and minimize blast radius.

### ZTNA: replacing the VPN for application access

**Zero-trust network access (ZTNA)** is zero trust applied to reaching
applications, and it is the practical successor to the remote-access VPN
from [Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md).
The difference is fundamental:

- **A traditional VPN** places the user *on the network*, then relies on
  other controls to limit what they can reach. Access is broad by default.
- **ZTNA** connects the user *to a specific application*, and to nothing
  else, after verifying identity and device posture. The application is
  invisible until authorization succeeds — there is no network to be "on."

This is the secure-service-edge model from
[Chapter 03](03-cloud-security-and-the-secure-service-edge.md) delivering
access: policy enforced in the cloud, the user connected to exactly what
they are entitled to and nothing more. It shrinks the attack surface from
"the network" to "one authorized application at a time."

### The four security layers SCAZT weights

SCAZT organizes secure cloud access into layers, and the exam's weight
tracks them:

- **Application and data security (25%)** — the largest domain: protecting
  the applications users reach and the data within them, including
  data-loss prevention, classification, and controlling how data moves to
  and from cloud services (the CASB functions from Chapter 03).
- **User and device security (20%)** — verifying the user (strong,
  ideally phishing-resistant multi-factor authentication) and the device
  (posture and health, the assessment from Chapter 06) before granting
  access.
- **Network and cloud security (20%)** — the secure web gateway, cloud
  firewall, and DNS-layer controls from Chapter 03 that sit in the access
  path.
- **Visibility and assurance (15%)** — knowing what access is happening
  and confirming controls are working, the always-in-the-path validation
  theme from Chapter 03.

Plus cloud security architecture (10%) — the design frame — and threat
response (10%) — acting when visibility flags something.

### Multi-factor authentication and Duo

Strong user verification is central, and Cisco's platform is **Duo**:
multi-factor authentication, device-trust checks, and adaptive policy that
raises or lowers assurance requirements by risk. Duo is how the "verify
explicitly" and "user and device security" pieces are implemented — MFA
that resists the phishing and credential-theft threats from Chapter 01,
plus a device-trust gate that a healthy, known device passes and an
unknown or non-compliant one does not.

## Design Considerations

- **Design from the resource inward, not the network outward.** Zero trust
  asks "who and what should reach this application," not "who should be on
  this network." Start from the resource and its data, and grant the
  minimum path to it.
- **Prefer ZTNA to VPN for application access.** New remote-access designs
  should default to ZTNA's per-application model; the broad-network VPN is
  the legacy pattern zero trust exists to replace. Chapter 07's VPN
  remains right for site-to-site and for legacy applications ZTNA cannot
  yet front.
- **Make device posture a gate, not a report.** User verification without
  device verification trusts a valid credential on a compromised machine.
  Both must pass, and posture must actually restrict — the same
  enforce-don't-flag point as Chapter 06.
- **Classify data before protecting it.** Application and data security is
  the largest domain, and you cannot apply data-loss controls to data you
  have not classified. Classification precedes protection.
- **Design visibility in from the start.** Assurance is 15% of the exam
  and the difference between a zero-trust design that works and one that
  merely claims to; you cannot respond to what you cannot see.

## Implementation and Automation

SCAZT is design- and cloud-console weighted; the implementation is policy
and verification rather than device CLI.

### 1. Verifying a ZTNA access decision

The defining check is that an application is reachable *only* through the
zero-trust path, after verification:

```bash
# Without the ZTNA client / policy, the application should be unreachable —
# not merely blocked, but invisible (no route to it at all).
curl -m 5 -sS https://internal-app.example.com/health ; echo "exit: $?"
# Expected without access: timeout/connection failure (exit != 0).

# Through the ZTNA path with a verified user and healthy device, the same
# request succeeds. The contrast is the control working.
```

The zero-trust property to confirm is that the application is *dark*
without authorization — reachability itself is gated, not just the
response.

### 2. Confirming device posture gates access

```text
# In Duo / the access policy: an access attempt from a device failing
# posture (out-of-date OS, no disk encryption, unknown device) should be
# denied or stepped up, and appear in the access log with the reason.
# Verify by attempting access from a deliberately non-compliant device.
```

The validation mirrors Chapter 06's posture check: a policy that reports
non-compliance without blocking is telemetry, not zero trust.

## Validation and Troubleshooting

### Is access actually zero trust, or VPN with extra steps?

The diagnostic question for a SCAZT design is whether it delivers
zero-trust properties or merely rebrands perimeter access:

| Property | Confirms zero trust | Fails if |
| --- | --- | --- |
| Application invisibility | App unreachable without authorization | App is pingable/reachable pre-auth |
| Per-application access | User reaches only authorized apps | User lands "on the network" |
| Device gating | Non-compliant device denied/stepped-up | Valid credential alone suffices |
| Continuous verification | Access re-evaluated on context change | Verified once, trusted thereafter |

A design that authenticates strongly but then places the user on a broad
network has MFA, not zero trust.

### The visibility gap

The common SCAZT-domain failure is a design that enforces well but cannot
show what it enforced. When an incident occurs, "who accessed what, from
which device, with what posture" must be answerable. A zero-trust
architecture without assurance is one you cannot audit or respond from —
which is why visibility carries its own domain.

## Security and Best Practices

- **Make MFA phishing-resistant where the risk warrants.** Not all
  second factors are equal; push-fatigue and SMS interception are real.
  The strongest factors resist the credential-theft threats zero trust
  exists to contain.
- **Re-verify on context change, not just at login.** Continuous
  verification is what separates zero trust from a strong front door;
  access should be re-evaluated when device health or risk changes.
- **Minimize the blast radius by design.** Per-application access means a
  compromised session reaches one application, not the network — the
  assume-breach principle made concrete.
- **Protect the access-control plane as tier-0.** The ZTNA broker and the
  identity provider are the systems that decide every access; their
  compromise is total, exactly as with ISE and FMC elsewhere in the
  volume.
- **Govern data movement to and from SaaS.** The largest domain is
  application and data security; DLP and CASB controls on where data goes
  are the substance of it.

## References and Knowledge Checks

**References**

- [Cisco 300-740 SCAZT exam topics](https://learningnetwork.cisco.com/s/scazt-exam-topics)
  — the concentration's domains and subtopics.
- [Cisco Duo documentation](https://duo.com/docs)
  — multi-factor authentication and device trust.
- [Chapter 03](03-cloud-security-and-the-secure-service-edge.md)
  — the secure service edge SCAZT delivers access through.
- [Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md)
  — the remote-access VPN model ZTNA succeeds for application access.

**Knowledge checks**

1. State the three zero-trust principles and the perimeter assumption each
   rejects.
2. How does ZTNA differ from a traditional remote-access VPN, and what
   does "the application is dark" mean?
3. Why must device posture gate access rather than merely report it?
4. Which SCAZT domain is largest, and what does protecting it involve?
5. Give the test that distinguishes a genuine zero-trust design from
   strong MFA layered on perimeter access.

## Hands-On Lab

**Objective:** Demonstrate the defining zero-trust property — an
application invisible without authorization, reachable only after user and
device verification — and confirm posture gates access.

**Prerequisites:** A Duo evaluation and a ZTNA/secure-access environment
(Cisco dCloud offers secure-access labs; Duo offers a free evaluation
tier). A lab application to protect. No production access broker.

**This lab leans on evaluation and dCloud environments**, since the
integrated secure-access stack has no free self-hosted equivalent; the
zero-trust *properties*, though, are observable in those environments.

**Procedure**

1. Place a lab application behind the zero-trust access path and configure
   an access policy requiring a verified user and a healthy device.
2. From an unauthorized position, confirm the application is unreachable —
   not merely blocked but with no route to it (the `curl` timeout above).
3. Authenticate through the ZTNA path with a compliant device and confirm
   access to that application — and only that application.
4. Configure Duo MFA and device trust; attempt access and complete the
   second factor.
5. Review the access logs and confirm you can answer "who reached what,
   from which device, with what posture" — the assurance requirement.

**Negative test**

6. Attempt access from a device that fails posture (an unknown device, or
   one with a disabled control) and confirm it is denied or stepped up,
   with the reason visible in the log — demonstrating that device gating
   is real and not merely a valid credential passing. Then confirm the
   protected application remained invisible throughout the failed attempt.

**Expected results**

- An application that is dark without authorization and reachable only
  through verified zero-trust access.
- Per-application access, not network placement.
- A device-posture denial with a logged reason.
- Access logs that answer the who/what/where/posture question.

**Cleanup**

7. Remove the lab access policy and end the evaluation or dCloud session.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SCAZT is the zero-trust concentration, and zero trust is the model that
discards perimeter trust in favor of verifying every request explicitly,
granting least privilege, and assuming breach. Its practical expression
for reaching applications is ZTNA, which connects a verified user to a
single authorized application rather than placing them on a network —
shrinking the attack surface from "the network" to "one application at a
time" and succeeding the remote-access VPN for that purpose. The exam
weights application and data security highest, with user and device
verification (Duo's MFA and device trust), network and cloud controls
(the secure service edge), and the visibility that makes any of it
auditable. The test of a real zero-trust design is whether the application
is dark without authorization and whether device posture actually gates
access — not whether strong authentication has been layered onto the old
perimeter.

- [ ] Can state the zero-trust principles and what they reject.
- [ ] Can explain ZTNA versus VPN and application invisibility.
- [ ] Can explain why device posture must gate, not report.
- [ ] Can name SCAZT's largest domain and what protecting it involves.
- [ ] Can test whether a design is genuinely zero trust.
