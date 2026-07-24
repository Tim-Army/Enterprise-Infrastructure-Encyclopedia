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

This chapter carries a topic-level walkthrough lab for **every objective in
the SCAZT (300-740 Designing and Implementing Secure Cloud Access for Users
and Endpoints) exam guide** — the Security Reference Architecture and SAFE,
identity/MFA/posture, zero-trust policy, threat frameworks, XDR/visibility,
and response automation — mapped in the volume README's coverage tables.
"Describe/Determine" topics use a read-only inspection or a design-decision
walkthrough; "Implement/Configure" topics build and verify. Labs use Cisco
Secure Access (SSE), Duo, and Cisco XDR APIs. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.30** — a Cisco Secure Access
organization (`$SSE` + token `$ST`), a Duo admin API (`$DUO`), a Cisco XDR
tenant (`$XDR` + token `$XT`), and Secure Client on a test endpoint.
**Cost:** none beyond lab resources.

### Lab 8.1 — Describe the Cisco Security Reference Architecture (Objective 1.1)

**Objective:** Map the deployed products to the reference-architecture
domains.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/deployments/v2/networktunnelgroups" | jq -r '.[].name' 2>/dev/null | head
```

**Expected result:** the SSE/SASE, firewall, identity, and endpoint products
in place — the reference architecture's domains realized as products.

**Negative test:** point products with no architecture leave gaps between
them; the reference architecture ensures coverage across domains.

**Cleanup:** none (read-only).

### Lab 8.2 — Describe recommended capabilities per use case (Objective 1.2)

**Objective:** Read the Secure Access capabilities enabled for a use case.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" | jq -r '.[].name' 2>/dev/null | head
```

**Expected result:** the capabilities (SWG, CASB, ZTNA, DNS security, FWaaS)
matched to the use case (remote user, branch, cloud app) — capability-to-need
mapping.

**Negative test:** enabling every capability without a use case adds latency
and cost; match capabilities to the requirement.

**Cleanup:** none (read-only).

### Lab 8.3 — Describe industry security frameworks (Objective 1.3)

**Objective:** Map controls to NIST/CISA ZT maturity.

```bash
echo "NIST 800-207 ZTA pillars: identity, device, network, app/workload, data"
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" >/dev/null 2>&1 || true
```

**Expected result:** the deployed controls mapped to a framework's pillars
(NIST 800-207, CISA ZT Maturity Model) — a common language for maturity.

**Negative test:** claiming "zero trust" from one pillar (identity only)
overstates maturity; ZT spans all pillars.

**Cleanup:** none (read-only).

### Lab 8.4 — Describe the SAFE architectural framework (Objective 1.4)

**Objective:** Place controls in a SAFE Place-in-the-Network (PIN).

```text
Cisco SAFE PINs: Branch, Campus, Data Center, Edge, Cloud, WAN
```

**Expected result:** each security control located in its SAFE PIN — SAFE
organizes controls by where they sit in the network.

**Negative test:** a control designed with no PIN context can be misplaced
(e.g. DLP only at the edge, missing east-west); SAFE ensures placement.

**Cleanup:** none (read-only).

### Lab 8.5 — Describe the SAFE Key structure (Objective 1.5)

**Objective:** Map a threat to a SAFE secure-domain capability.

```text
SAFE secure domains: Management, Security Intelligence, Compliance,
Segmentation, Threat Defense, Secure Services
```

**Expected result:** the SAFE Key linking business flows → threats →
capabilities → the architecture — the model's traceability from risk to
control.

**Negative test:** buying a capability with no mapped threat is unjustified;
the SAFE Key traces each control to a risk.

**Cleanup:** none (read-only).

### Lab 8.6 — Implement user/device certificate authentication (Objective 2.1)

**Objective:** Confirm certificate-based user/device identity.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/... " 2>/dev/null; \
echo "device cert enrollment via Secure Client + internal/managed CA"
```

**Expected result:** users/devices authenticating with certificates (not
passwords) — strong, phishing-resistant identity for ZT access.

**Negative test:** password-only access is phishable; certificate/device
identity raises the bar.

**Cleanup:** none (read-only).

### Lab 8.7 — Implement multifactor authentication (Objective 2.2)

**Objective:** Confirm Duo MFA enrollment and policy.

```bash
curl -sk -H "$DUO" "https://api-<host>.duosecurity.com/admin/v1/users" | jq -r '.response[0].username' 2>/dev/null
```

**Expected result:** users enrolled in Duo MFA with a policy requiring a
second factor — MFA on every access request.

**Negative test:** MFA bypass for "trusted" networks is an attack path;
require MFA regardless of location in ZT.

**Cleanup:** none (read-only).

### Lab 8.8 — Implement endpoint posture for access (Objective 2.3)

**Objective:** Read the device posture gating access.

```bash
curl -sk -H "$DUO" "https://api-<host>.duosecurity.com/admin/v1/endpoints" | jq -r '.response[0].trusted_endpoint' 2>/dev/null
```

**Expected result:** endpoint health/trust (managed, encrypted, patched)
evaluated before access — posture as an access condition.

**Negative test:** granting access without a posture check lets a compromised
device in; ZT gates on device health.

**Cleanup:** none (read-only).

### Lab 8.9 — Configure SAML/SSO and OIDC (Objective 2.4)

**Objective:** Confirm the IdP (SAML/OIDC) integration.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/admin/v2/identityproviders" | jq -r '.[].name' 2>/dev/null
```

**Expected result:** the SAML/OIDC identity provider federating authentication
— one identity across cloud apps and Secure Access.

**Negative test:** a broken SAML assertion (clock skew, wrong audience) fails
SSO; the IdP and SP must agree on claims/time.

**Cleanup:** none (read-only).

### Lab 8.10 — Configure user/device trust with SAML (Objective 2.5)

**Objective:** Read the trust conditions in the access policy.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" | jq -r '.[0].conditions' 2>/dev/null | head
```

**Expected result:** access rules conditioned on verified user + device trust
via SAML — continuous, per-request trust evaluation.

**Negative test:** trusting a session indefinitely after one auth violates ZT;
re-evaluate trust continuously.

**Cleanup:** none (read-only).

### Lab 8.11 — Determine endpoint→private-app policy (Objective 3.1)

**Objective:** Design a ZTNA policy for a private application.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" | jq -r '.[] | select(.ruleType=="private") | .name' 2>/dev/null | head
```

**Decision to record:** the least-privilege ZTNA rule (which users/devices →
which private app, no network-level access). **Negative test:** VPN-style
network access exposes the whole subnet; ZTNA exposes only the app.

**Cleanup:** none (read-only).

### Lab 8.12 — Determine endpoint→internet/SaaS policy (Objective 3.2)

**Objective:** Design the SWG/CASB policy for internet/SaaS.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" | jq -r '.[] | select(.ruleType=="internet") | .name' 2>/dev/null | head
```

**Decision to record:** the SWG (URL/category, malware) and CASB (sanctioned
vs shadow SaaS) rules. **Negative test:** unrestricted SaaS access enables
data exfiltration; CASB controls it.

**Cleanup:** none (read-only).

### Lab 8.13 — Determine remote-user VPN/ZTNA policy (Objective 3.3)

**Objective:** Choose per-app ZTNA vs VPN for remote users.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/deployments/v2/roamingcomputers" | jq '. | length' 2>/dev/null
```

**Decision to record:** ZTNA for app-specific access, VPN only where a full
tunnel is genuinely needed. **Negative test:** default full-VPN for everyone
over-exposes; prefer ZTNA per app.

**Cleanup:** none (read-only).

### Lab 8.14 — Determine network-security-edge policy (Objective 3.4)

**Objective:** Design the branch/edge FWaaS policy.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" | jq -r '.[] | select(.ruleType=="firewall") | .name' 2>/dev/null | head
```

**Decision to record:** the cloud-firewall (FWaaS) rules for branch egress —
inspection at the edge without backhaul. **Negative test:** backhauling
branch traffic to a DC firewall adds latency; the cloud edge inspects locally.

**Cleanup:** none (read-only).

### Lab 8.15 — Describe MITRE ATT&CK and defense mapping (Objective 4.1)

**Objective:** Map an XDR detection to an ATT&CK technique.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/incidents" | jq -r '.data[0].mitre_tactics // "TA00xx"' 2>/dev/null
```

**Expected result:** detections tagged with ATT&CK tactics/techniques — a
common taxonomy for defense coverage and gaps.

**Negative test:** measuring coverage by product count instead of ATT&CK
technique coverage hides blind spots.

**Cleanup:** none (read-only).

### Lab 8.16 — Describe cloud attack tactics and mitigation (Objective 4.2)

**Objective:** Read a cloud-focused detection.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/incidents?source=cloud" | jq -r '.data[0].title' 2>/dev/null
```

**Expected result:** cloud attack detections (credential theft, misconfiguration
exploitation, lateral movement) with mitigations — cloud-specific defense.

**Negative test:** on-prem-only detection misses cloud-native attacks; cloud
telemetry is required.

**Cleanup:** none (read-only).

### Lab 8.17 — Describe WAF and DDoS protection (Objective 4.3)

**Objective:** Read the WAF/DDoS policy protecting an app.

```bash
echo "WAF: OWASP Top 10 rules; DDoS: rate limiting / scrubbing at the edge"
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" >/dev/null 2>&1 || true
```

**Expected result:** WAF signatures (injection, XSS) and DDoS rate limiting in
front of the app — L7 application protection.

**Negative test:** a network firewall alone does not stop an L7 injection; the
WAF inspects the application layer.

**Cleanup:** none (read-only).

### Lab 8.18 — Determine application-enforcement policy (Objective 4.4)

**Objective:** Design app-level access enforcement.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/policies/v2/rules" | jq -r '.[] | select(.applications!=null) | .name' 2>/dev/null | head
```

**Decision to record:** per-application access rules (who, from what device
posture, to which app). **Negative test:** IP/port rules cannot express
per-user app access; application-aware policy can.

**Cleanup:** none (read-only).

### Lab 8.19 — Determine hybrid/multicloud platform security (Objective 4.5)

**Objective:** Design consistent policy across clouds.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/deployments/v2/networktunnelgroups" | jq -r '.[].name' 2>/dev/null | head
```

**Decision to record:** one policy model applied across AWS/Azure/GCP via the
SSE fabric, not per-cloud silos. **Negative test:** per-cloud policy silos
drift and leave gaps; a unified fabric keeps them consistent.

**Cleanup:** none (read-only).

### Lab 8.20 — Describe the Cisco XDR solution (Objective 5.1)

**Objective:** Read XDR's correlated incident view.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/incidents" | jq -r '.data[0] | "\(.id)\t\(.severity)"' 2>/dev/null
```

**Expected result:** XDR correlating detections across email, endpoint,
network, and cloud into one incident — the cross-domain SOC view.

**Negative test:** per-tool alerts without XDR correlation multiply analyst
effort; XDR unifies them.

**Cleanup:** none (read-only).

### Lab 8.21 — Describe visibility/assurance automation use cases (Objective 5.2)

**Objective:** Read an automation workflow in XDR.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/workflows" | jq -r '.data[].name' 2>/dev/null | head
```

**Expected result:** automation workflows (enrich, notify, contain) — the
assurance/response automation XDR orchestrates.

**Negative test:** manual enrichment for every alert does not scale; the
workflow automates it.

**Cleanup:** none (read-only).

### Lab 8.22 — Describe visibility and logging benefits (Objective 5.3)

**Objective:** Read the telemetry sources feeding visibility.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/integrations" | jq -r '.data[].name' 2>/dev/null | head
```

**Expected result:** the integrated telemetry sources (SSE, firewall,
endpoint, cloud) — breadth of visibility is the value.

**Negative test:** a blind spot (an unmonitored segment) hides attacker activity;
comprehensive logging closes it.

**Cleanup:** none (read-only).

### Lab 8.23 — Validate traffic flow and telemetry baseline (Objective 5.4)

**Objective:** Read a baseline traffic/telemetry report.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/reports/v2/activity?limit=10" | jq -r '.data[0]' 2>/dev/null
```

**Expected result:** a baseline of normal user→app flows — the reference that
makes an anomaly detectable.

**Negative test:** alerting with no baseline fires on normal variation;
baseline first.

**Cleanup:** none (read-only).

### Lab 8.24 — Diagnose user application/workload access issues (Objective 5.5)

**Objective:** Trace a failed ZTNA access.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/reports/v2/activity?verdict=blocked" | jq -r '.data[0] | "\(.identity)\t\(.rule)"' 2>/dev/null
```

**Expected result:** the blocked access with the rule/reason (posture failed,
policy denied) — the diagnosis of a ZT access denial.

**Negative test:** blaming the app for a posture-driven denial; the activity
log names the real cause.

**Cleanup:** none (read-only).

### Lab 8.25 — Verify user access with tools (Objective 5.6)

**Objective:** Confirm a user can reach an authorized app.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/reports/v2/activity?verdict=allowed&identity=<user>" | jq -r '.data[0].destination' 2>/dev/null
```

**Expected result:** the allowed session to the authorized app — verifying the
positive path, not just denials.

**Negative test:** confirming only that bad traffic is blocked, without
verifying good traffic passes, risks a policy that blocks everything.

**Cleanup:** none (read-only).

### Lab 8.26 — Analyze application dependencies (Objective 5.7)

**Objective:** Read app dependencies from flow/firewall data.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/reports/v2/activity?application=<app>" | jq -r '[.data[].destination] | unique' 2>/dev/null | head
```

**Expected result:** the destinations an app actually talks to — the
dependency map a least-privilege policy must permit.

**Negative test:** a ZTNA rule that omits a dependency breaks the app; map
dependencies before tightening.

**Cleanup:** none (read-only).

### Lab 8.27 — Describe response automation use cases (Objective 6.1)

**Objective:** Read an automated response playbook.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/workflows?type=response" | jq -r '.data[].name' 2>/dev/null | head
```

**Expected result:** response playbooks (isolate endpoint, block indicator,
revoke session) — automation that shortens time-to-contain.

**Negative test:** manual response to a fast-moving attack loses the race;
automation contains at machine speed.

**Cleanup:** none (read-only).

### Lab 8.28 — Determine actions from telemetry (Objective 6.2)

**Objective:** Choose a response from a telemetry signal.

```bash
curl -sk -H "Authorization: Bearer $XT" "$XDR/incidents?severity=high" | jq -r '.data[0].recommended_actions' 2>/dev/null
```

**Decision to record:** the action a high-severity telemetry signal warrants
(quarantine, revoke, investigate). **Negative test:** ignoring a high-severity
signal or over-reacting to a low one; match the action to the signal.

**Cleanup:** none (read-only).

### Lab 8.29 — Determine policy from audit reports (Objective 6.3)

**Objective:** Derive a policy change from an audit finding.

```bash
curl -sk -H "Authorization: Bearer $ST" "$SSE/reports/v2/... " 2>/dev/null; \
echo "audit finding: over-permissive rule -> tighten to least privilege"
```

**Decision to record:** the policy tightening an audit finding drives (remove
an over-broad rule, add posture). **Negative test:** noting a finding without
a policy change leaves the gap open.

**Cleanup:** none (read-only).

### Lab 8.30 — Determine action on user/app compromise (Objective 6.4)

**Objective:** Choose containment for a compromised identity.

```bash
curl -sk -X POST -H "Authorization: Bearer $XT" "$XDR/response/actions" \
  -d '{"action":"revoke-session","target":"<user>"}' 2>/dev/null | jq -r '.status' 2>/dev/null || echo "revoke session + isolate device"
```

**Decision to record:** revoke the user's sessions, isolate the device, and
force re-authentication — the containment for a confirmed compromise.
**Negative test:** resetting the password alone leaves active sessions live;
revoke sessions too.

**Cleanup:** none (read-only).

### Lab 8.31 — Zero-trust application access (integrative)

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
