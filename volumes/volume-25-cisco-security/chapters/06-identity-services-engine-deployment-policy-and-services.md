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

This chapter carries a topic-level walkthrough lab for **every objective in
the SISE (300-715) exam guide** — all seven domains, from ISE architecture
through device administration — mapped in the volume README's coverage
tables. Labs use the ISE CLI, the ISE ERS/Open API, and switch-side RADIUS
verification. Each ends **`**Lab verified by:** *pending*`** until a human
runs it.

**Shared prerequisites for Labs 6.1–6.29** — an ISE deployment reachable at
`$ISE` with ERS enabled and an API credential in `$IA` (an `Authorization`
header), a Catalyst switch as the NAD, an AD/LDAP identity store, and test
endpoints. **Cost:** none beyond lab resources.

### Lab 6.1 — Configure ISE personas (Objective 1.1)

**Objective:** Read the persona roles a node runs.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/node" | jq -r '.SearchResult.resources[].name'
# on the node
show application status ise | include Running
```

**Expected result:** the node's personas (PAN, MnT, PSN, pxGrid) — the
functional roles ISE splits management, monitoring, and policy service into.

**Negative test:** a single-node lab running all personas cannot scale to
production PSN load; personas distribute across nodes for HA/scale.

**Cleanup:** none (read-only).

### Lab 6.2 — Describe ISE deployment options (Objective 1.2)

**Objective:** Read the deployment topology (standalone vs distributed).

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/node" | jq '.SearchResult.total'
```

**Expected result:** the node count — standalone (1), or distributed (2
admin + N PSNs) for HA and scale.

**Negative test:** a two-node deployment with both PANs primary is invalid;
one primary + one secondary admin is the supported model.

**Cleanup:** none (read-only).

### Lab 6.3 — Describe hardware and VM performance specs (Objective 1.3)

**Objective:** Read the node's resource profile against the sizing guide.

```bash
show tech-support | include CPU|Memory|Disk
show application status ise
```

**Expected result:** the CPU/RAM/disk profile — ISE VM sizing (small/medium/
large) caps concurrent sessions/endpoints per node.

**Negative test:** an undersized VM hits its session ceiling and drops
authentications under load; size to the endpoint count.

**Cleanup:** none (read-only).

### Lab 6.4 — Describe zero-touch provisioning (Objective 1.4)

**Objective:** Confirm the automated node-onboarding/registration path.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/node/<id>" | jq -r '.Node.otherAttributes // "registered"'
```

**Expected result:** nodes registered to the deployment via automated
provisioning — hands-off scale-out of PSNs.

**Negative test:** a node with a mismatched certificate/time cannot join the
deployment; ZTP still requires PKI/NTP alignment.

**Cleanup:** none (read-only).

### Lab 6.5 — Configure native AD and LDAP (Objective 2.1)

**Objective:** Confirm the external identity source join.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/activedirectory" | jq -r '.SearchResult.resources[].name'
```

**Expected result:** the AD join point (and any LDAP source) ISE
authenticates users against — enterprise identity, not local accounts.

**Negative test:** an AD join with clock skew beyond Kerberos tolerance fails;
ISE and the DC must be time-synced.

**Cleanup:** none (read-only).

### Lab 6.6 — Describe identity store options (Objective 2.2)

**Objective:** Read the identity source sequence.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/idstoresequence" | jq -r '.SearchResult.resources[].name'
```

**Expected result:** an identity-source sequence (internal → AD → LDAP) —
the ordered stores ISE checks for a credential.

**Negative test:** a sequence that stops on first store miss can block a
valid user in a later store; order and "continue" behavior matter.

**Cleanup:** none (read-only).

### Lab 6.7 — Configure wireless 802.1X (Objective 2.3)

**Objective:** Verify a wireless 802.1X authentication reached ISE.

```bash
# on the WLC/switch, then confirm in ISE
show authentication sessions | include dot1x
curl -sk -H "$IA" "$ISE:9060/ers/config/... " >/dev/null  # RADIUS live-log via MnT API
```

**Expected result:** a wireless client authenticated via 802.1X/EAP against
ISE, with an authorization result (VLAN/dACL) returned.

**Negative test:** an EAP method mismatch (client PEAP, policy EAP-TLS) fails
auth; the allowed protocols must include the client's method.

**Cleanup:** none (read-only).

### Lab 6.8 — Configure wired 802.1X and IBNS 2.0 (Objective 2.4)

**Objective:** Read an IBNS 2.0 policy-map-driven wired auth session.

```text
SW# show authentication sessions interface gig1/0/5 details
SW# show access-session interface gig1/0/5 policy
```

**Expected result:** the port's concurrent 802.1X/MAB session under an IBNS
2.0 (Cisco Common Classification Policy Language) policy map.

**Negative test:** legacy IBNS 1.0 `authentication` commands cannot express
concurrent/priority auth; IBNS 2.0 `policy-map type control subscriber` can.

**Cleanup:** none (read-only).

### Lab 6.9 — Implement MAB (Objective 2.5)

**Objective:** Authenticate a non-802.1X device by MAC.

```text
SW# show authentication sessions interface gig1/0/6 | include MAB|Mac
```

**Expected result:** a printer/IoT device authenticated via MAB against ISE's
endpoint store — a policy-driven path for supplicant-less devices.

**Negative test:** MAB with no matching endpoint/identity in ISE is rejected
or lands in a limited VLAN; MAB is only as strong as the MAC allowlist.

**Cleanup:** none (read-only).

### Lab 6.10 — Configure Cisco TrustSec (Objective 2.6)

**Objective:** Read the SGT assigned by ISE authorization.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/sgt" | jq -r '.SearchResult.resources[].name'
```

**Expected result:** the Security Group Tags ISE can assign — identity-based
micro-segmentation carried in the fabric.

**Negative test:** an SGACL matrix with no default-deny leaks traffic between
groups; the matrix must be explicit.

**Cleanup:** none (read-only).

### Lab 6.11 — Configure authentication and authorization policies (Objective 2.7)

**Objective:** Read a policy set's rules.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/... " 2>/dev/null; \
echo "policy sets via ISE UI/OpenAPI: authN + authZ conditions -> result"
```

**Expected result:** a policy set with authentication (identity store) and
authorization (VLAN/dACL/SGT) rules — the decision logic per access request.

**Negative test:** an authorization rule above a more specific one shadows it
(first-match); order the rules specific-to-general.

**Cleanup:** none (read-only).

### Lab 6.12 — Configure web authentication (Objective 3.1)

**Objective:** Confirm a central web-auth (CWA) redirect.

```text
SW# show authentication sessions interface gig1/0/7 details | include URL|ACL
```

**Expected result:** an unauthenticated client redirected to ISE's web portal
by a redirect ACL — browser-based auth for devices without a supplicant.

**Negative test:** a redirect ACL that permits the portal but not DNS leaves
the client unable to resolve the portal URL; permit DNS in the redirect ACL.

**Cleanup:** none (read-only).

### Lab 6.13 — Configure guest access services (Objective 3.2)

**Objective:** Read the guest access type in use.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/guestuser" | jq '.SearchResult.total'
```

**Expected result:** guest accounts (hotspot, self-registered, sponsored) —
the guest-onboarding model.

**Negative test:** hotspot access with no AUP acceptance grants network access
with no accountability; require the acceptable-use policy.

**Cleanup:** none (read-only).

### Lab 6.14 — Configure sponsor and guest portals (Objective 3.3)

**Objective:** Read the portal configuration.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/sponsorportal" | jq -r '.SearchResult.resources[].name'
```

**Expected result:** the sponsor and guest portals — sponsors create guest
accounts; guests self-register or use them.

**Negative test:** a sponsor group with no portal mapping cannot create
accounts; the portal-to-group binding is required.

**Cleanup:** none (read-only).

### Lab 6.15 — Implement profiler services (Objective 4.1)

**Objective:** Read a profiled endpoint's device type.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/endpoint" | jq -r '.SearchResult.resources[0].name'
```

**Expected result:** endpoints classified by profile (Apple-Device,
IP-Phone) — profiling drives differentiated authorization.

**Negative test:** an not-yet-profiled endpoint falls to a generic policy; more
probes/CoA refine the profile.

**Cleanup:** none (read-only).

### Lab 6.16 — Implement probes (Objective 4.2)

**Objective:** Read the profiling probes enabled on a PSN.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/profilerprobeconfig" 2>/dev/null | jq -r '.' | head
```

**Expected result:** enabled probes (RADIUS, DHCP, HTTP, SNMP, NMAP, DNS) —
the data sources that classify a device.

**Negative test:** relying on one probe (MAC OUI) misclassifies spoofed
devices; multiple probes raise confidence.

**Cleanup:** none (read-only).

### Lab 6.17 — Implement Change of Authorization (Objective 4.3)

**Objective:** Trigger and confirm a CoA.

```bash
curl -sk -X PUT -H "$IA" "$ISE:9060/ers/config/endpoint/<id>" >/dev/null
# switch shows re-authentication
```

**Expected result:** a re-profiled endpoint triggers a CoA, re-authorizing
the live session without the user reconnecting — dynamic policy change.

**Negative test:** a NAD not configured for CoA (dynamic-author) ignores the
request; the switch must accept CoA on UDP 1700.

**Cleanup:** none (read-only).

### Lab 6.18 — Configure endpoint identity management (Objective 4.4)

**Objective:** Read the endpoint identity groups.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/endpointgroup" | jq -r '.SearchResult.resources[].name'
```

**Expected result:** endpoint identity groups (static and profiled) used in
authorization conditions — managing devices as identities.

**Negative test:** a statically grouped endpoint overrides its profile;
static assignment wins, which can mis-authorize a re-purposed device.

**Cleanup:** none (read-only).

### Lab 6.19 — Describe Cisco BYOD functionality (Objective 5.1)

**Objective:** Read the BYOD onboarding flow components.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/portal" | jq -r '.SearchResult.resources[] | .name' | grep -i byod
```

**Expected result:** the BYOD portal — dual-SSID/single-SSID onboarding that
provisions a certificate and moves the device to secured access.

**Negative test:** BYOD without a supplicant-provisioning wizard leaves users
manually configuring 802.1X; the flow automates it.

**Cleanup:** none (read-only).

### Lab 6.20 — Configure BYOD onboarding with the internal CA (Objective 5.2)

**Objective:** Confirm the ISE internal CA is issuing endpoint certs.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/internalcaserver" 2>/dev/null | jq -r '.' | head
show application status ise | include CA
```

**Expected result:** the internal CA service running and issuing BYOD
certificates — device identity via PKI, no shared PSK.

**Negative test:** the internal CA disabled forces an external CA or blocks
cert-based BYOD; the CA service must be enabled.

**Cleanup:** none (read-only).

### Lab 6.21 — Configure certificates for BYOD (Objective 5.3)

**Objective:** Read the certificate template used for BYOD.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/certificatetemplate" 2>/dev/null | jq -r '.' | head
```

**Expected result:** the cert template (key size, SAN, validity) issued to
onboarded devices — the identity the device authenticates with thereafter.

**Negative test:** a template with too-long a validity outlives device
ownership; scope validity to the device lifecycle.

**Cleanup:** none (read-only).

### Lab 6.22 — Configure block list / allow list (Objective 5.4)

**Objective:** Read the blocklist endpoint group.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/endpointgroup" | jq -r '.SearchResult.resources[] | select(.name|test("Blocklist|Blacklist";"i")) | .name'
```

**Expected result:** the Blocklist group — a lost/stolen device dropped into
it is denied network access by policy.

**Negative test:** block-listing by IP (which changes) instead of MAC/identity
fails to follow the device; blocklist by endpoint identity.

**Cleanup:** none (read-only).

### Lab 6.23 — Describe posture services and client provisioning (Objective 6.1)

**Objective:** Read the posture status of an endpoint.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/... " 2>/dev/null; \
echo "posture: Compliant/NonCompliant/Unknown drives authZ"
```

**Expected result:** endpoints with a posture status (Compliant/NonCompliant/
Unknown) that authorization keys on — health-gated access.

**Negative test:** granting full access before posture completes (no
"pending" state handling) lets a non-compliant device on; gate on Compliant.

**Cleanup:** none (read-only).

### Lab 6.24 — Configure posture conditions and provisioning (Objective 6.2)

**Objective:** Read a posture policy's requirement.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/... " 2>/dev/null; \
echo "posture requirement: e.g. AV running, disk encrypted, patch level"
```

**Expected result:** a posture requirement (AV/AS running, firewall on, patch
level) with a remediation action — the compliance bar and how to meet it.

**Negative test:** a requirement with no remediation leaves non-compliant
users stuck; provide a remediation path.

**Cleanup:** none (read-only).

### Lab 6.25 — Configure the compliance module (Objective 6.3)

**Objective:** Confirm the AnyConnect/Secure Client compliance module
version.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/... " 2>/dev/null; \
echo "compliance module version deployed to clients"
```

**Expected result:** the compliance module version ISE pushes to clients —
it evaluates the posture conditions on the endpoint.

**Negative test:** an outdated compliance module cannot evaluate newer OS/AV
checks; keep it current.

**Cleanup:** none (read-only).

### Lab 6.26 — Configure posture agents and modes (Objective 6.4)

**Objective:** Distinguish agent vs agentless posture.

```bash
echo "agent (Secure Client ISE Posture) vs temporal agent vs agentless (API)"
curl -sk -H "$IA" "$ISE:9060/ers/config/... " >/dev/null 2>&1 || true
```

**Expected result:** the posture agent type in use — persistent agent,
temporal (dissolvable) agent, or agentless posture over an API.

**Negative test:** agentless posture on an unmanaged device it cannot reach
returns Unknown; match the mode to device manageability.

**Cleanup:** none (read-only).

### Lab 6.27 — Describe supplicant and authenticator (Objective 6.5)

**Objective:** Read the 802.1X roles on a live session.

```text
SW# show authentication sessions interface gig1/0/5 details | include Method|Server
```

**Expected result:** the supplicant (endpoint), authenticator (switch), and
authentication server (ISE) roles and the EAP method — the 802.1X triangle.

**Negative test:** a device with no supplicant cannot do 802.1X and needs MAB;
the role must exist for the method.

**Cleanup:** none (read-only).

### Lab 6.28 — Compare AAA protocols (Objective 7.1)

**Objective:** Contrast RADIUS and TACACS+ usage in ISE.

```bash
curl -sk -H "$IA" -H 'Accept: application/json' "$ISE:9060/ers/config/networkdevice" | jq -r '.SearchResult.resources[0].name'
```

**Expected result:** NADs configured for RADIUS (network access) and/or
TACACS+ (device admin) — the two AAA protocols and their jobs.

**Negative test:** using RADIUS for per-command device-admin authorization is
weak; TACACS+ separates and authorizes commands.

**Cleanup:** none (read-only).

### Lab 6.29 — Configure TACACS+ device administration (Objective 7.2)

**Objective:** Verify TACACS+ command authorization from a NAD.

```text
SW# test aaa group tacacs+ admin <pw> legacy
SW# show tacacs
```

**Expected result:** admin logins and per-command authorization enforced by
ISE's device-admin service — granular CLI control.

**Negative test:** a command set that permits `configure terminal` but no
sub-commands blocks all config; scope command sets to the role's needs.

**Cleanup:** none (read-only).

### Lab 6.30 — Build an ISE policy set and diagnose an authorization failure (integrative)

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
