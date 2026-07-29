# Chapter 04: Content Security and Endpoint Protection

## Learning Objectives

- Describe email and web content security and the threats each answers.
- Explain endpoint protection and detection: the shift from signature
  antivirus to behavior-based EDR.
- Describe Cisco Secure Endpoint's architecture — cloud analysis,
  retrospection, and trajectory.
- Understand why Content Security lost its standalone SCOR domain in v2.0
  and where the material now lives.
- Connect endpoint and content controls to the malware and phishing
  threats from Chapter 01.

## Theory and Architecture

### A domain that moved

This chapter covers two things SCOR treats differently across editions,
and the difference is worth stating plainly because older study material
is everywhere.

**In SCOR v1.1, Content Security was a standalone 15% domain.** In
**v2.0 it is gone as a separate domain** — the email- and web-security
material is folded into network and cloud security, and the freed weight
went to Endpoint Protection, which rose from 10% to **15%**. This chapter
keeps both subjects together because they remain examinable and are core
to the role, but a v2.0 candidate should understand that content security
now appears *within* other domains rather than carrying its own line,
while endpoint protection got more important.

### Content security: email and web

Content security inspects the two channels most malware and phishing
arrive through: email and web.

**Email security** (Cisco Secure Email) answers the phishing and
malware-delivery threats from Chapter 01 at the mail boundary:

- **Anti-spam and anti-phishing** — filtering unsolicited and deceptive
  mail before it reaches a user.
- **Malware inspection** — scanning attachments, integrating with the
  same file-analysis backend as the endpoint and firewall.
- **URL and content filtering** — rewriting or blocking malicious links,
  since the payload is often a link rather than an attachment.
- **Outbound controls** — data-loss prevention and encryption for mail
  leaving the organization.

**Web security** (Cisco Secure Web Appliance, and the cloud secure web
gateway from [Chapter 03](03-cloud-security-and-the-secure-service-edge.md))
inspects HTTP and HTTPS:

- **URL filtering** by category and reputation.
- **Malware scanning** of downloaded content.
- **TLS decryption** for inspecting encrypted traffic — which depends
  directly on the PKI foundation from Chapter 01, because the gateway must
  present a trusted certificate to intercept the session.

The through-line: email and web are the delivery channels, and content
security is inspection at those channels. It overlaps the cloud-delivered
gateway of Chapter 03 and the firewall's file inspection of Chapter 02 —
which is precisely why v2.0 could redistribute it rather than keep it
separate.

### Endpoint protection and detection

The endpoint is the last enforcement point and, increasingly, the most
important — which is why v2.0 weighted it up. The evolution SCOR expects
you to understand:

- **Traditional antivirus** matched files against signatures of known
  malware. Necessary but insufficient: it cannot catch what it has no
  signature for.
- **Endpoint detection and response (EDR)** watches *behavior* — a
  process spawning unexpected children, encrypting files rapidly, reaching
  out to a command-and-control host — and can detect novel threats by what
  they do rather than what they are.

**Cisco Secure Endpoint** (formerly AMP for Endpoints) is the platform.
Its distinctive capabilities:

- **Cloud-based analysis** — files and behaviors are evaluated against
  cloud intelligence shared across the whole install base, so a threat
  seen anywhere protects everywhere.
- **Retrospection** — if a file initially judged clean is later found
  malicious, Secure Endpoint can identify every endpoint that received it,
  after the fact. Signature antivirus cannot look backward.
- **Trajectory** — a visual record of a file's and a process's movement
  across endpoints and time, which is the raw material of the incident
  response in
  [Chapter 09](09-designing-security-infrastructure-automation-and-capstone.md).

### The endpoint as a policy enforcement point

The endpoint is not only a detection sensor; it is where several other
controls terminate. The **Cisco Secure Client** (formerly AnyConnect)
carries the VPN of
[Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md),
the DNS-layer security of Chapter 03 when off-network, and the posture
assessment of [Chapter 06](06-identity-services-engine-deployment-policy-and-services.md).
The endpoint is where the distributed enforcement model actually reaches
the user, which is why it recurs across the volume.

## Design Considerations

- **Layer email, web, and endpoint rather than choosing among them.**
  Each covers a channel the others do not; malware blocked at email never
  reaches the endpoint, and malware that arrives another way is caught
  there. Defense in depth is the design, not redundancy to trim.
- **Plan TLS decryption deliberately.** Inspecting encrypted web traffic
  requires the gateway to intercept TLS, which has privacy, performance,
  and certificate-trust implications. Decide what to decrypt and what to
  bypass (banking, health) as a policy, and provision the certificate
  trust the interception needs.
- **Value retrospection in the platform choice.** The ability to answer
  "who else got this file" after a verdict changes is what separates EDR
  from antivirus operationally. Design assuming initial verdicts are
  sometimes wrong.
- **Consolidate the endpoint agent.** Secure Client unifies VPN, DNS
  security, and posture; multiple overlapping agents create conflict and
  management burden. One agent carrying several controls is the intended
  design.
- **Treat email as the primary attack channel it is.** Most breaches
  begin with a phishing email; weighting email security accordingly
  matches the threat, whatever the exam's domain structure.

## Implementation and Automation

Endpoint and content security are console- and API-driven; the operational
skill is reading verdicts and trajectories, and automating response.

### 1. Reading an endpoint verdict and trajectory

The investigative workflow, expressed against Secure Endpoint's API:

```bash
# Find recent malware detections across the fleet.
curl -s "https://api.amp.cisco.com/v1/events?event_type[]=1090519054" \
  -u "$CLIENT_ID:$API_KEY" | jq '.data[] | {computer: .computer.hostname, file: .file.file_name, disposition: .file.disposition}'

# For a suspect file hash, find every endpoint that has seen it —
# retrospection expressed as an API query.
curl -s "https://api.amp.cisco.com/v1/computers/activity?q=$SHA256" \
  -u "$CLIENT_ID:$API_KEY" | jq '.data[].hostname'
```

The second query is the one antivirus cannot answer: *given a file now
known bad, where is it?*

### 2. Automating containment

When an endpoint is confirmed compromised, isolating it from the network
while preserving it for forensics is a response action worth automating —
carefully, because it disconnects a user's machine:

```bash
# Move an endpoint into isolation (illustrative). Guard this heavily;
# it is a disruptive action and belongs behind confirmation and logging.
curl -s -X PUT "https://api.amp.cisco.com/v1/computers/$CONNECTOR_GUID/isolation" \
  -u "$CLIENT_ID:$API_KEY"
```

As with firewall automation in Chapter 02, build the read-only
investigative tooling first and gate any containment action behind
deliberate confirmation.

## Validation and Troubleshooting

### Confirming coverage, not just deployment

The endpoint-security validation question mirrors Chapter 03's: is the
control actually protecting the endpoint, or merely installed?

| Check | What it confirms |
| --- | --- |
| Connector reporting to the console | The endpoint is managed, not orphaned |
| Recent policy sync | It has the current rules, not stale ones |
| A test detection (EICAR) fires | Detection is actually functioning |
| Off-network DNS/VPN still enforced | Controls follow the user, not just on-LAN |

An endpoint with an installed-but-not-reporting connector is unprotected
in the way that matters — it looks covered on the deployment count and is
invisible in an incident.

### The TLS-decryption failure class

When web inspection breaks, the cause is frequently certificate trust: the
gateway intercepts TLS by presenting its own certificate, and if the
client does not trust the gateway's CA, the session fails or warns. This
is a PKI problem (Chapter 01) surfacing as a web-access problem, and the
fix is distributing the gateway's CA to the client trust store — the same
mechanics as any certificate deployment in the volume.

## Security and Best Practices

- **Keep the endpoint agent and its intelligence current.** EDR depends
  on cloud intelligence and engine updates; a stale connector is closer to
  antivirus than EDR.
- **Do not exempt endpoints from inspection for convenience.** The
  executive laptop excluded from policy is the one an attacker most wants;
  exceptions are attack surface.
- **Protect the endpoint-management console as tier-0.** It can isolate,
  and in some configurations remediate, every managed endpoint;
  controlling it is controlling the fleet.
- **Encrypt and control outbound mail.** Data-loss prevention and mail
  encryption protect the data leaving through the channel most breaches
  also enter through.
- **Preserve trajectory and event data.** It is the evidence base for
  incident response; retention policy on it is a security decision, not a
  storage one.

## References and Knowledge Checks

**References**

- [Cisco Secure Endpoint documentation](https://docs.amp.cisco.com/)
  — connector architecture, retrospection, and the API.
- [Cisco Secure Email and Web documentation](https://www.cisco.com/c/en/us/support/security/email-security-appliance/series.html)
  — content-security configuration.
- [Chapter 01](01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md)
  — the malware and phishing threats these controls answer, and the PKI
  that TLS decryption depends on.
- [Cisco 350-701 SCOR exam topics](https://learningnetwork.cisco.com/s/scor-exam-topics)
  — the Endpoint Protection domain, and where content security now lives.

**Knowledge checks**

1. What changed for Content Security between SCOR v1.1 and v2.0, and where
   did its material and weight go?
2. Distinguish signature antivirus from behavior-based EDR, and give a
   threat only the latter catches.
3. Explain retrospection and why signature antivirus cannot provide it.
4. Why does TLS decryption for web inspection depend on PKI, and what
   breaks if the client does not trust the gateway?
5. Name three controls the Cisco Secure Client carries beyond antivirus.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in
two content-security concentration exam guides** — SESA (300-720 Secure
Email) and SWSA (300-725 Secure Web) — plus the SCOR endpoint topics, mapped
in the volume README's coverage tables. Labs use the Secure Email Gateway
(ESA) and Secure Web Appliance (WSA) CLIs and their APIs. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.69** — an ESA and a WSA (physical,
virtual, or dCloud), CLI access, an LDAP/AD source, and test mail/web
clients. **Cost:** none beyond lab resources.

**Cisco Secure Email (SESA 300-720) — Labs 4.1–4.31**

### Lab 4.1 — Configure Secure Email Gateway features (Objective 1.1)

**Objective:** Read the ESA listener/interface configuration.

```text
esa> listenerconfig
esa> interfaceconfig
```

**Expected result:** the public (inbound) and private (outbound) listeners on
their interfaces — the ESA's mail-flow entry/exit points.

**Negative test:** a public listener with no HAT/RAT restricts nothing and
becomes an open relay; the mail-flow policy must gate it.

**Cleanup:** none (read-only).

### Lab 4.2 — Describe centralized services (Objective 1.2)

**Objective:** Read the Security Management Appliance (SMA) integration.

```text
esa> smaconfig
```

**Expected result:** the ESA reporting to a centralized SMA for
quarantine/reporting/tracking — one console across multiple ESAs.

**Negative test:** per-ESA quarantines fragment admin; centralized services
consolidate them.

**Cleanup:** none (read-only).

### Lab 4.3 — Configure mail policies (Objective 1.3)

**Objective:** Read the incoming/outgoing mail policies.

```text
esa> policyconfig
```

**Expected result:** per-recipient/sender mail policies applying antispam,
antivirus, and content filters — the policy layer per user group.

**Negative test:** a single default policy cannot differentiate executives
from general users; per-group policies do.

**Cleanup:** none (read-only).

### Lab 4.4 — Integrate ESA with SecureX (Objective 1.4)

**Objective:** Confirm the SecureX/XDR integration.

```text
esa> securexconfig
```

**Expected result:** the ESA registered to SecureX/XDR — email threats
correlated into cross-product investigations.

**Negative test:** email events analyzed in isolation miss the broader
campaign; the integration correlates them.

**Cleanup:** none (read-only).

### Lab 4.5 — Configure Secure Email Threat Defense (Objective 1.5)

**Objective:** Read the cloud Threat Defense (ETD) posture.

```text
esa> threatfeedconfig
```

**Expected result:** the cloud-based Email Threat Defense analyzing messages
for BEC/phishing beyond the gateway — layered email defense.

**Negative test:** gateway filters alone miss sophisticated BEC with no
malicious payload; ETD's behavioral analysis catches it.

**Cleanup:** none (read-only).

### Lab 4.6 — Control spam with SenderBase and Antispam (Objective 2.1)

**Objective:** Read the reputation/antispam verdicts.

```text
esa> grep -i "SenderBase\|reputation" mail_logs
```

**Expected result:** SenderBase (Talos) reputation scores gating connections
and IPAS/CASE antispam scanning content — the two spam-control layers.

**Negative test:** disabling reputation filtering forces every message through
content scanning, raising load; reputation drops known-bad senders early.

**Cleanup:** none (read-only).

### Lab 4.7 — Describe graymail management (Objective 2.2)

**Objective:** Read the graymail/unsubscribe handling.

```text
esa> grep -i graymail mail_logs
```

**Expected result:** graymail (marketing/bulk) detected and safe-unsubscribe
offered — separating unwanted-but-not-malicious mail from spam.

**Negative test:** treating graymail as spam blocks legitimate bulk mail;
graymail handling classifies it distinctly.

**Cleanup:** none (read-only).

### Lab 4.8 — Configure file reputation and analysis (Objective 2.3)

**Objective:** Confirm AMP file reputation/sandboxing on attachments.

```text
esa> ampconfig
```

**Expected result:** attachments checked against file reputation and sent to
file analysis (sandbox) when unknown — malware defense on email files.

**Negative test:** reputation-only (no analysis) misses zero-day attachments;
sandboxing evaluates the unknown.

**Cleanup:** none (read-only).

### Lab 4.9 — Implement malicious URL protection (Objective 2.4)

**Objective:** Read URL filtering/rewriting in messages.

```text
esa> outbreakconfig
esa> grep -i "URL" mail_logs
```

**Expected result:** malicious URLs blocked and suspicious ones rewritten to a
proxy for click-time protection — defense against phishing links.

**Negative test:** scanning URLs only at delivery misses a link weaponized
after delivery; click-time rewriting re-checks at click.

**Cleanup:** none (read-only).

### Lab 4.10 — Describe bounce verification (Objective 2.5)

**Objective:** Read the bounce-verification tagging.

```text
esa> bounceconfig
```

**Expected result:** outbound messages tagged so forged bounces (backscatter)
are rejected — anti-backscatter protection.

**Negative test:** without bounce verification, forged bounces flood the
postmaster; tagging validates legitimate bounces.

**Cleanup:** none (read-only).

### Lab 4.11 — Describe content filter capabilities (Objective 3.1)

**Objective:** Read the content filters applied.

```text
esa> filters
```

**Expected result:** content filters acting on message conditions (subject,
body, attachment) with actions (quarantine, strip, notify) — flexible policy.

**Negative test:** an overly broad content filter quarantines legitimate mail;
scope the conditions.

**Cleanup:** none (read-only).

### Lab 4.12 — Create text resources (Objective 3.2)

**Objective:** Read content dictionaries and disclaimers.

```text
esa> dictionaryconfig
esa> textconfig
```

**Expected result:** content dictionaries (keyword lists for DLP/filters) and
disclaimer text resources — reusable content-matching and stamping.

**Negative test:** a dictionary with common words false-positives constantly;
tune the term list.

**Cleanup:** none (read-only).

### Lab 4.13 — Configure message filters (Objective 3.3)

**Objective:** Read CLI-defined message filters (pre-policy).

```text
esa> filters
esa> filters detail
```

**Expected result:** message filters (evaluated before mail policies, system-
wide) — the earliest, most powerful filtering stage.

**Negative test:** a message filter dropping mail runs before per-policy
exceptions can save it; order message vs content filters deliberately.

**Cleanup:** none (read-only).

### Lab 4.14 — Configure scan behavior (Objective 3.4)

**Objective:** Read the body/attachment scan limits.

```text
esa> scanconfig
```

**Expected result:** scan depth/size limits for attachments and archives — the
bound on how deep the ESA inspects.

**Negative test:** a scan-size limit below a malicious archive lets it pass
unscanned; size limits are a bypass if too low.

**Cleanup:** none (read-only).

### Lab 4.15 — Configure antivirus scanning (Objective 3.5)

**Objective:** Confirm the antivirus engine (Sophos/McAfee) is scanning.

```text
esa> antivirusconfig
esa> grep -i "virus" mail_logs
```

**Expected result:** the AV engine scanning and acting (clean/quarantine/drop)
on infected mail.

**Negative test:** AV set to scan-only logs infections but delivers them;
set the action to drop/quarantine.

**Cleanup:** none (read-only).

### Lab 4.16 — Configure outbreak filters (Objective 3.6)

**Objective:** Read the outbreak-filter (Talos) protection.

```text
esa> outbreakconfig
```

**Expected result:** outbreak filters holding suspicious mail during a
zero-day window based on Talos intelligence — early defense before signatures.

**Negative test:** disabling outbreak filters removes the zero-day quarantine;
they bridge the gap until AV/AS updates.

**Cleanup:** none (read-only).

### Lab 4.17 — Configure Data Loss Prevention (Objective 3.7)

**Objective:** Read the outbound DLP policy.

```text
esa> policyconfig
esa> grep -i "DLP" mail_logs
```

**Expected result:** DLP scanning outbound mail for regulated data (PCI/PII)
with actions (encrypt, quarantine, block) — preventing data exfiltration.

**Negative test:** DLP on inbound only misses data leaving; DLP belongs on the
outgoing policy.

**Cleanup:** none (read-only).

### Lab 4.18 — Configure LDAP servers and queries (Objective 4.1)

**Objective:** Verify the LDAP accept/routing query.

```text
esa> ldapconfig
esa> ldapconfig test
```

**Expected result:** LDAP recipient-acceptance and routing queries validating
recipients against the directory — rejecting mail to non-existent users early.

**Negative test:** no LDAP accept query accepts mail for every address then
bounces it later (backscatter); validate at acceptance.

**Cleanup:** none (read-only).

### Lab 4.19 — Understand spam quarantine (Objective 4.2)

**Objective:** Read the spam quarantine configuration.

```text
esa> quarantineconfig
```

**Expected result:** the spam quarantine holding flagged mail with end-user
access — false positives recoverable without admin.

**Negative test:** dropping spam outright loses recoverable false positives;
the quarantine holds them for review.

**Cleanup:** none (read-only).

### Lab 4.20 — Understand SMTP functionality (Objective 4.3)

**Objective:** Read the SMTP conversation/routes.

```text
esa> smtproutes
esa> tophosts
```

**Expected result:** SMTP routes and delivery destinations — how the ESA
relays accepted mail onward.

**Negative test:** a missing SMTP route to the internal mail store queues mail
undelivered; the route must exist.

**Cleanup:** none (read-only).

### Lab 4.21 — Configure DomainKeys and DKIM signing (Objective 5.1)

**Objective:** Confirm outbound DKIM signing.

```text
esa> domainkeysconfig
```

**Expected result:** outbound mail DKIM-signed with the domain key — receivers
can verify the message was not altered and came from the domain.

**Negative test:** a DKIM key not published in DNS makes verification fail at
the receiver; publish the public key.

**Cleanup:** none (read-only).

### Lab 4.22 — Configure SPF and SIDF (Objective 5.2)

**Objective:** Read inbound SPF verification.

```text
esa> grep -i "SPF" mail_logs
```

**Expected result:** inbound mail SPF-checked against the sender domain's
authorized senders — anti-spoofing at the envelope level.

**Negative test:** accepting mail that fails SPF from a spoofed domain enables
phishing; enforce the SPF verdict.

**Cleanup:** none (read-only).

### Lab 4.23 — Configure DMARC verification (Objective 5.3)

**Objective:** Read inbound DMARC policy enforcement.

```text
esa> dmarcconfig
```

**Expected result:** DMARC combining SPF/DKIM with the domain's published
policy (none/quarantine/reject) — the authoritative anti-spoofing decision.

**Negative test:** honoring `p=none` (monitor) as enforcement lets spoofed
mail through; act on `quarantine`/`reject`.

**Cleanup:** none (read-only).

### Lab 4.24 — Configure forged email detection (Objective 5.4)

**Objective:** Read the forged-email-detection (display-name) rules.

```text
esa> dictionaryconfig
esa> grep -i "forged" mail_logs
```

**Expected result:** display-name spoofing of executives detected (FED
dictionary) — catching BEC that passes SPF/DKIM but forges the display name.

**Negative test:** SPF/DKIM/DMARC do not stop a look-alike display name from a
new domain; FED catches the impersonation.

**Cleanup:** none (read-only).

### Lab 4.25 — Configure email encryption (Objective 5.5)

**Objective:** Read the outbound encryption profile.

```text
esa> encryptionconfig
```

**Expected result:** sensitive outbound mail encrypted (CRES/envelope) by
policy — confidentiality for regulated content.

**Negative test:** relying on opportunistic TLS alone does not guarantee
encryption if the peer refuses it; policy-driven message encryption does.

**Cleanup:** none (read-only).

### Lab 4.26 — Describe S/MIME services (Objective 5.6)

**Objective:** Read the S/MIME signing/encryption config.

```text
esa> smimeconfig
```

**Expected result:** S/MIME certificate-based signing/encryption between
gateways — end-to-end message integrity and confidentiality.

**Negative test:** S/MIME without valid peer certificates cannot encrypt to
that peer; certificate exchange is required.

**Cleanup:** none (read-only).

### Lab 4.27 — Configure Cisco Secure Email settings (Objective 5.7)

**Objective:** Read the overall mail-flow security posture.

```text
esa> mailconfig
```

**Expected result:** the consolidated inbound/outbound security settings — the
gateway's end-to-end mail-security configuration.

**Negative test:** a strong inbound posture with a weak outbound one leaks data
and reputation; secure both directions.

**Cleanup:** none (read-only).

### Lab 4.28 — Configure quarantines (Objective 6.1)

**Objective:** Read the policy/virus/outbreak quarantines.

```text
esa> quarantineconfig
```

**Expected result:** separate quarantines (spam, policy, virus, outbreak) with
retention and actions — categorized message holding.

**Negative test:** one quarantine for everything mixes recoverable spam with
confirmed malware; separate them.

**Cleanup:** none (read-only).

### Lab 4.29 — Use safelists and blocklists (Objective 6.2)

**Objective:** Read the end-user safelist/blocklist.

```text
esa> slblconfig
```

**Expected result:** per-user safelists (always deliver) and blocklists
(always quarantine) — user-level delivery control.

**Negative test:** a safelisted spoofed sender bypasses filtering; safelists
must be used cautiously.

**Cleanup:** none (read-only).

### Lab 4.30 — Manage messages in quarantines (Objective 6.3)

**Objective:** Read and release quarantined messages.

```text
esa> quarantineconfig
esa> findevent <recipient>
```

**Expected result:** quarantined messages searchable and releasable —
recovering a false positive.

**Negative test:** releasing a message without re-scanning can deliver a later-
confirmed threat; re-scan on release where possible.

**Cleanup:** none (read-only).

### Lab 4.31 — Configure virtual gateways (Objective 6.4)

**Objective:** Read the virtual-gateway (multi-IP) configuration.

```text
esa> altsrchost
```

**Expected result:** virtual gateways sending different mail streams from
different IPs/reputations — isolating bulk from transactional mail.

**Negative test:** sending all streams from one IP lets a bulk-mail reputation
hit hurt transactional delivery; virtual gateways separate them.

**Cleanup:** none (read-only).

**Cisco Secure Web (SWSA 300-725) — Labs 4.32–4.68**

### Lab 4.32 — Describe Secure Web Appliance features (Objective 1.1)

**Objective:** Read the WSA's enabled services.

```text
wsa> version
wsa> status detail
```

**Expected result:** the WSA proxy services (HTTP/HTTPS/FTP, AVC, AMP, URL
filtering) — the web-security functions on the appliance.

**Negative test:** a WSA with the proxy disabled inspects nothing; the proxy
must be on to enforce policy.

**Cleanup:** none (read-only).

### Lab 4.33 — Describe Secure Web Appliance solutions (Objective 1.2)

**Objective:** Read the deployment solution (explicit vs transparent).

```text
wsa> proxyconfig
```

**Expected result:** explicit-forward (client points at proxy) or transparent
(WCCP/PBR redirect) proxying — the two ways traffic reaches the WSA.

**Negative test:** transparent mode without WCCP/redirect never sees the
traffic; the redirection must be configured.

**Cleanup:** none (read-only).

### Lab 4.34 — Integrate WSA with Advanced Web Security Reporting (Objective 1.3)

**Objective:** Confirm the AWSR/log export.

```text
wsa> logconfig
```

**Expected result:** access logs exported to AWSR/Splunk for long-term
reporting — analytics beyond the on-box reports.

**Negative test:** on-box logs roll over; without export, long-term reporting
is lost.

**Cleanup:** none (read-only).

### Lab 4.35 — Integrate WSA with Cisco ISE (Objective 1.4)

**Objective:** Confirm the WSA↔ISE (pxGrid) integration.

```text
wsa> isesettings
```

**Expected result:** the WSA consuming ISE identity/SGT via pxGrid —
identity-based web policy without a separate auth prompt.

**Negative test:** without ISE integration the WSA re-authenticates users;
pxGrid supplies the identity transparently.

**Cleanup:** none (read-only).

### Lab 4.36 — Troubleshoot data security / external DLP (Objective 1.5)

**Objective:** Read the external DLP (ICAP) integration.

```text
wsa> externaldlpconfig
```

**Expected result:** the WSA sending uploads to an external DLP server over
ICAP — outbound data-loss control on web traffic.

**Negative test:** an unreachable ICAP server either fails-open (leak) or
fails-closed (block all); set the fail behavior deliberately.

**Cleanup:** none (read-only).

### Lab 4.37 — Perform initial WSA configuration (Objective 2.1)

**Objective:** Read the network/interface baseline.

```text
wsa> ifconfig
wsa> routeconfig
```

**Expected result:** the management/data interfaces and routes — the WSA's
network placement in the traffic path.

**Negative test:** a WSA with no route to the internet cannot fetch
categories/updates; connectivity is a prerequisite.

**Cleanup:** none (read-only).

### Lab 4.38 — Configure an access policy (Objective 2.2)

**Objective:** Read the web access policy and its actions.

```text
wsa> policyconfig
```

**Expected result:** access policies (by identity/URL category) with actions
(allow/block/monitor/warn) — the core web-filtering policy.

**Negative test:** a global-allow policy above a specific block never reaches
the block; order matters (policy trace proves it).

**Cleanup:** none (read-only).

### Lab 4.39 — Configure and verify web proxy features (Objective 2.3)

**Objective:** Read the proxy caching/settings.

```text
wsa> advancedproxyconfig
```

**Expected result:** proxy features (caching, upstream proxy, X-Forwarded-For)
— performance and integration behavior of the proxy.

**Negative test:** aggressive caching of dynamic content serves stale pages;
tune cacheability.

**Cleanup:** none (read-only).

### Lab 4.40 — Configure a referrer header filter (Objective 2.4)

**Objective:** Read a referrer-based category exception.

```text
wsa> policyconfig
```

**Expected result:** a policy using the HTTP referrer to allow embedded
content from a blocked category (e.g. video on an allowed site) — granular
exceptions.

**Negative test:** referrer headers are spoofable; do not rely on them for
security-critical decisions.

**Cleanup:** none (read-only).

### Lab 4.41 — Describe deployment options (Objective 3.1)

**Objective:** Read the redirection method in use.

```text
wsa> wccp
```

**Expected result:** WCCP (from a switch/router), PBR, or explicit — the
mechanism steering client traffic to the WSA.

**Negative test:** WCCP without the router side configured redirects nothing;
both ends must agree.

**Cleanup:** none (read-only).

### Lab 4.42 — Describe WSA features (Objective 3.2)

**Objective:** Read the scanning/AVC feature set.

```text
wsa> status detail
```

**Expected result:** AVC (application visibility), AMP, DVS (Dynamic Vectoring
and Streaming) engines — the inspection features on allowed traffic.

**Negative test:** allowing without AVC/AMP passes web malware and shadow apps;
enable the inspection engines.

**Cleanup:** none (read-only).

### Lab 4.43 — Describe PAC files (Objective 3.3)

**Objective:** Read the Proxy Auto-Config delivery.

```text
wsa> pacfile
```

**Expected result:** a PAC file telling browsers which proxy to use per URL —
automatic client proxy configuration.

**Negative test:** a PAC file unreachable by clients leaves them direct
(bypassing the WSA); host it reliably.

**Cleanup:** none (read-only).

### Lab 4.44 — Describe SOCKS proxy services (Objective 3.4)

**Objective:** Read the SOCKS proxy configuration.

```text
wsa> socksconfig
```

**Expected result:** the SOCKS proxy handling non-HTTP TCP traffic (e.g. some
apps) — extending proxy control beyond web.

**Negative test:** expecting URL-category filtering on SOCKS; it operates at
TCP, not the HTTP layer.

**Cleanup:** none (read-only).

### Lab 4.45 — Describe authentication features (Objective 4.1)

**Objective:** Read the authentication realms.

```text
wsa> authcache
wsa> userconfig
```

**Expected result:** the auth realms (AD/LDAP, ISE) and scheme (Kerberos/NTLM/
Basic) — how the WSA identifies users for policy.

**Negative test:** Basic auth over HTTP sends credentials in the clear;
Kerberos is transparent and secure.

**Cleanup:** none (read-only).

### Lab 4.46 — Configure traffic redirection to the WSA (Objective 4.2)

**Objective:** Confirm WCCP redirection is active.

```text
wsa> wccp
# on the switch: show ip wccp
```

**Expected result:** WCCP service groups with the WSA registered — client
traffic transparently redirected for inspection.

**Negative test:** an ACL on the router excluding a subnet from WCCP leaves it
uninspected; the redirect ACL scope matters.

**Cleanup:** none (read-only).

### Lab 4.47 — Describe FTP proxy authentication (Objective 4.3)

**Objective:** Read the FTP proxy auth configuration.

```text
wsa> ftpproxyconfig
```

**Expected result:** the FTP proxy authenticating and scanning FTP transfers —
extending control to FTP.

**Negative test:** native FTP that bypasses the proxy is uninspected; redirect
FTP to the proxy.

**Cleanup:** none (read-only).

### Lab 4.48 — Troubleshoot authentication issues (Objective 4.4)

**Objective:** Diagnose an auth failure from the logs.

```text
wsa> grep -i "auth" accesslogs
wsa> authcache flushall
```

**Expected result:** the auth failure reason (realm unreachable, clock skew,
wrong scheme) in the logs; flushing the cache re-tests cleanly.

**Negative test:** a stale auth cache masks a fixed problem; flush to re-test.

**Cleanup:** none (diagnostic).

### Lab 4.49 — Describe SSL/TLS inspection (Objective 5.1)

**Objective:** Read the HTTPS decryption policy.

```text
wsa> httpsconfig
```

**Expected result:** the decryption policy (by category/reputation) enabling
inspection of HTTPS — most web traffic is encrypted, so this is essential.

**Negative test:** no HTTPS decryption leaves the majority of traffic
uninspected; decrypt (with privacy exceptions) to see it.

**Cleanup:** none (read-only).

### Lab 4.50 — Configure HTTPS capabilities (Objective 5.2)

**Objective:** Read the decryption exceptions (privacy categories).

```text
wsa> policyconfig
```

**Expected result:** decryption-policy exceptions for finance/health
categories — inspecting most HTTPS while respecting privacy/legal limits.

**Negative test:** decrypting banking traffic risks compliance issues; exempt
sensitive categories.

**Cleanup:** none (read-only).

### Lab 4.51 — Configure certificates for decryption (Objective 5.3)

**Objective:** Confirm the decryption CA certificate.

```text
wsa> certconfig
```

**Expected result:** the WSA's root/intermediate CA that clients trust,
enabling MITM decryption without browser errors.

**Negative test:** clients that do not trust the WSA CA get certificate errors
on every HTTPS site; deploy the CA to clients.

**Cleanup:** none (read-only).

### Lab 4.52 — Describe access policies (Objective 6.1)

**Objective:** Read the access-policy structure.

```text
wsa> policyconfig
```

**Expected result:** access policies grouping identity + URL/AVC/malware
settings — the decision layer for allowed users.

**Negative test:** a policy with no identity match applies the global policy;
identity binds the right policy.

**Cleanup:** none (read-only).

### Lab 4.53 — Describe identification profiles and authentication (Objective 6.2)

**Objective:** Read the identification profiles.

```text
wsa> identityconfig
```

**Expected result:** identification profiles (how a transaction is
identified — by IP, auth, ISE) that select which access policy applies.

**Negative test:** an ID profile requiring auth on a device that cannot
authenticate (IoT) blocks it; use IP-based ID for those.

**Cleanup:** none (read-only).

### Lab 4.54 — Troubleshoot using access logs (Objective 6.3)

**Objective:** Read an access-log entry to explain a decision.

```text
wsa> grep "<client-ip>" accesslogs
wsa> tail accesslogs
```

**Expected result:** the ACL decision tag (ALLOW/BLOCK/DECRYPT) and the policy/
category that decided — the authoritative per-transaction record.

**Negative test:** guessing the policy instead of reading the ACL tag misleads;
the log names the deciding policy.

**Cleanup:** none (diagnostic).

### Lab 4.55 — Configure URL filtering (Objective 7.1)

**Objective:** Read the URL-category filtering policy.

```text
wsa> policyconfig
wsa> urlcatconfig
```

**Expected result:** URL categories (Talos) blocked/allowed/warned per policy —
category-based web control.

**Negative test:** an uncategorized/new site falls to the default action; set
the default deliberately.

**Cleanup:** none (read-only).

### Lab 4.56 — Configure acceptable-use policies (Objective 7.2)

**Objective:** Read time-based / volume-based quotas.

```text
wsa> quotasconfig
```

**Expected result:** time-of-day and bandwidth-volume quotas (e.g. streaming
capped during work hours) — usage-based acceptable-use control.

**Negative test:** a category blocked outright when a quota was intended
over-restricts; quotas allow bounded use.

**Cleanup:** none (read-only).

### Lab 4.57 — Configure application visibility and control (Objective 7.3)

**Objective:** Read the AVC application controls.

```text
wsa> avcconfig
```

**Expected result:** AVC controlling app behaviors (e.g. block file upload to
a webmail app while allowing read) — granular in-app control.

**Negative test:** URL filtering alone cannot allow an app while blocking one
of its actions; AVC provides the in-app granularity.

**Cleanup:** none (read-only).

### Lab 4.58 — Create a corporate global acceptable-use policy (Objective 7.4)

**Objective:** Read the global/default access policy.

```text
wsa> policyconfig
```

**Expected result:** the global policy that applies when no specific policy
matches — the organization's baseline acceptable use.

**Negative test:** a permissive global policy undermines specific blocks for
unmatched traffic; set a safe default.

**Cleanup:** none (read-only).

### Lab 4.59 — Implement the policy trace tool (Objective 7.5)

**Objective:** Trace how a URL is handled for a user.

```text
wsa> policytrace <user> http://example.com
```

**Expected result:** the exact identity, policy, and action a request would
hit — the WSA's `packet-tracer` equivalent for verifying policy.

**Negative test:** guessing policy behavior instead of tracing misdiagnoses a
block; the trace shows the real decision.

**Cleanup:** none (diagnostic).

### Lab 4.60 — Inspect archive file types (Objective 7.6)

**Objective:** Read the archive-inspection settings.

```text
wsa> policyconfig
```

**Expected result:** the WSA extracting and scanning archive contents (zip,
rar) — malware hidden in archives is inspected.

**Negative test:** a nested/encrypted archive beyond the extraction depth
passes; set depth and block unscannable archives.

**Cleanup:** none (read-only).

### Lab 4.61 — Describe scanning engines (Objective 8.1)

**Objective:** Read the anti-malware scanning engines.

```text
wsa> status detail | grep -i "Webroot\|Sophos\|McAfee\|AMP"
```

**Expected result:** the DVS engines (Webroot/Sophos/McAfee) plus AMP scanning
web objects — layered malware detection.

**Negative test:** one engine misses what another catches; the multi-engine
DVS raises detection.

**Cleanup:** none (read-only).

### Lab 4.62 — Configure file reputation and analysis (Objective 8.2)

**Objective:** Confirm AMP file reputation/sandboxing on downloads.

```text
wsa> ampconfig
```

**Expected result:** downloads checked against file reputation and sent to
analysis when unknown — web malware defense, with retrospection.

**Negative test:** reputation-only misses zero-day downloads; file analysis
evaluates the unknown.

**Cleanup:** none (read-only).

### Lab 4.63 — Describe Cisco Secure Endpoint (Objective 8.3)

**Objective:** Read the Secure Endpoint integration/retrospection.

```text
wsa> ampconfig
```

**Expected result:** AMP retrospective alerts when a previously-clean file is
later found malicious — retrospection across the web and endpoint.

**Negative test:** point-in-time scanning cannot catch a file whose verdict
changes later; retrospection re-alerts.

**Cleanup:** none (read-only).

### Lab 4.64 — Describe Cognitive Intelligence integration (Objective 8.4)

**Objective:** Read the behavioral (Cognitive/Talos) analytics feed.

```text
wsa> logconfig
```

**Expected result:** access logs fed to Cognitive Intelligence/SNA for
behavioral detection of C2/exfiltration in web traffic — analytics beyond
signatures.

**Negative test:** signature detection misses novel C2 over HTTPS; behavioral
analytics on the logs catches the pattern.

**Cleanup:** none (read-only).

### Lab 4.65 — Configure and analyze web tracking reports (Objective 9.1)

**Objective:** Read a web-tracking query.

```text
wsa> reportingconfig
```

**Expected result:** web-tracking data (top users, categories, malware) — the
report set for usage and threat analysis.

**Negative test:** reporting over a window with logging off is incomplete;
ensure logging covered the period.

**Cleanup:** none (read-only).

### Lab 4.66 — Configure Advanced Web Security Reporting (Objective 9.2)

**Objective:** Confirm the AWSR (Splunk-based) export.

```text
wsa> logconfig
```

**Expected result:** access logs streaming to AWSR for scaled reporting across
many WSAs — enterprise-wide web analytics.

**Negative test:** on-box reports cannot aggregate multiple WSAs; AWSR
centralizes them.

**Cleanup:** none (read-only).

### Lab 4.67 — Troubleshoot connectivity issues (Objective 9.3)

**Objective:** Diagnose a proxy/upstream connectivity fault.

```text
wsa> nslookup example.com
wsa> telnet example.com 443
wsa> grep -i "DNS\|upstream" system_logs
```

**Expected result:** DNS resolution and upstream reachability tests — the
first checks for "the internet is down through the proxy."

**Negative test:** blaming policy for a failure that is really DNS/upstream;
test connectivity first.

**Cleanup:** none (diagnostic).

### Lab 4.68 — Interpret the System Health Dashboard and REST API (Objectives 9.4, 9.5)

**Objective:** Read WSA health via the dashboard and the AsyncOS REST API.

```bash
curl -sk -u admin:pw "https://$WSA:6443/wsa/api/v3.0/health" | jq -r '.'
```

**Expected result:** CPU/proxy/RAM health and the REST API returning it — the
programmatic and dashboard views of appliance health.

**Negative test:** a WSA at its connection ceiling drops sessions though config
is correct; the health metrics reveal the resource limit.

**Cleanup:** none (read-only).

### Lab 4.69 — Endpoint retrospection and content-security enforcement (integrative)

**Objective:** Exercise endpoint detection and the retrospection workflow,
and observe a content-security control acting on a test threat.

**Prerequisites:** A Cisco Secure Endpoint evaluation or dCloud
environment with the connector on a lab machine, and the EICAR test file
(a harmless standard antivirus test string). No production endpoints.

**This lab uses the EICAR test file**, an industry-standard harmless
string that every endpoint product detects as a test — so detection is
observable without any real malware.

**Procedure**

1. Confirm the Secure Endpoint connector on your lab machine is reporting
   to the console and has synced policy.
2. Create the EICAR test file on the endpoint and observe the detection
   fire in the console. Note the disposition and the event.
3. In the console, open the file's trajectory and read how it represents
   the file's appearance and the process that created it.
4. Using the API queries above, find the detection event and then query
   for every endpoint that has seen the test file's hash — exercising
   retrospection.
5. If email or web security is available in your environment, send a test
   message or request a test URL and observe the content control act.

**Negative test**

6. Stop the connector service (simulating an orphaned endpoint), recreate
   the EICAR file, and confirm the console shows no new detection —
   demonstrating that an installed-but-not-reporting connector is
   unprotected despite appearing deployed. Restart the connector and
   confirm reporting resumes.

**Expected results**

- A confirmed, reporting connector and a fired test detection.
- A read of the file's trajectory and a successful retrospection query.
- Direct demonstration that a non-reporting connector provides no
  protection.

**Cleanup**

7. Delete the EICAR test file, confirm the connector is running and
   reporting, and end the evaluation session.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Content security inspects the email and web channels most malware and
phishing arrive through, and endpoint protection catches what reaches the
device. SCOR v2.0 dissolved Content Security as a standalone domain,
folding its material into network and cloud security and moving the weight
to Endpoint Protection, which reflects where the threat and the industry
have gone. Endpoint security's evolution from signature antivirus to
behavior-based EDR — with cloud analysis, retrospection, and trajectory —
is the conceptual core, and the endpoint doubles as the enforcement point
where VPN, DNS security, and posture reach the user through a single
consolidated agent. Throughout, the validation question is whether the
control actually covers the endpoint and sits in the traffic path, not
merely whether it is installed.

- [ ] Can explain the v1.1-to-v2.0 content/endpoint reweighting.
- [ ] Can distinguish antivirus from EDR and name a threat only EDR
      catches.
- [ ] Can explain retrospection and trajectory.
- [ ] Can connect TLS decryption to PKI and diagnose a trust failure.
- [ ] Can verify an endpoint is genuinely protected, not just installed.
