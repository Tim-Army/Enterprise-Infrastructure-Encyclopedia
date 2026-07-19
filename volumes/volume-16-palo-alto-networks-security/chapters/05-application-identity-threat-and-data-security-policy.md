# Chapter 05: Application, Identity, Threat, and Data Security Policy

## Learning Objectives

- Write App-ID- and User-ID-based security policy rules that enforce
  least-privilege access instead of port-based rules.
- Configure User-ID identity mapping using an integrated User-ID agent and
  group mapping against a directory service.
- Build and attach security profiles (Antivirus, Anti-Spyware, Vulnerability
  Protection, URL Filtering, File Blocking, WildFire Analysis, and Data
  Filtering) as a security profile group.
- Explain why SSL/TLS decryption is required for Content-ID to inspect
  encrypted traffic, and configure an SSL Forward Proxy decryption policy.
- Validate policy behavior with `test security-policy-match` and diagnose
  common App-ID and decryption failures.

## Theory and Architecture

[Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md) built the network plumbing — zones, routing, and NAT. This
chapter builds the policy that actually decides what happens to traffic
once it arrives, which is where App-ID, User-ID, and Content-ID (introduced
conceptually in [Chapter 01](01-cybersecurity-apprentice-foundations.md)) become concrete rule configuration.

### Anatomy of a PAN-OS security policy rule

A PAN-OS security rule is evaluated using a superset of match criteria far
richer than a traditional five-tuple firewall rule:

| Match field | Purpose |
| --- | --- |
| Source/destination zone | Coarse network-topology scoping ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)) |
| Source/destination address | IP, FQDN, or address group objects |
| Source user | User-ID identity or group, not just source IP |
| Application | App-ID-classified application, not port |
| Service | TCP/UDP port, typically left as `application-default` |
| URL category | PAN-DB category, for combined app+category rules |
| Action | allow, deny, drop, reset |
| Profile / profile group | Content-ID security profiles applied on match |
| Log settings | Log at session start and/or end, forwarding profile |

Rules are evaluated top-down, first match wins — identical in principle to
NAT policy evaluation from [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md). The single most important shift
from legacy firewall design is that **Application replaces Service as the
primary match dimension**: a rule permitting `application: ssl` restricted
to `service: application-default` still only permits SSL/TLS traffic that
App-ID actually classifies as SSL on its standard port, closing the classic
port-hopping evasion that a port-only rule cannot.

### App-ID mechanics and dependencies

App-ID classifies traffic using signatures, protocol decoding, and
heuristics, updated continuously through the Applications and Threats
content updates ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)). Two behaviors are essential to understand:

- **Application dependencies.** Many applications are built on other
  applications — for example, `facebook-posting` depends on `facebook-base`,
  which depends on `ssl` and `web-browsing`. PAN-OS's App-ID engine
  identifies the base protocol first, then progressively refines the
  classification as more packets arrive; a rule permitting only the
  specific sub-application without also permitting its dependency chain
  (either explicitly or by relying on an existing broader permit rule
  earlier in the rulebase) will break that application. The Web UI's
  application dependency viewer (and `show application <name>` in the CLI)
  displays this chain.
- **`unknown-tcp` / `unknown-udp`.** Traffic App-ID cannot classify —
  because it does not match any known signature — is labeled
  `unknown-tcp` or `unknown-udp`. A well-tuned rulebase treats a
  significant volume of unknown traffic as worth investigating, since it
  can indicate either a legitimate custom internal application that merits
  its own App-ID request/custom signature, or genuinely evasive/malicious
  traffic.
- **Application override.** In rare cases (typically a custom or legacy
  protocol that App-ID misclassifies), an administrator can force a
  session to a specific application/port pairing via an Application
  Override policy, which bypasses further App-ID inspection for that
  session. Because this also bypasses Content-ID threat inspection for the
  overridden session, it is used sparingly and only when App-ID
  misclassification is confirmed, not as a general troubleshooting
  shortcut.

### User-ID: identity as a policy dimension

User-ID maps IP addresses (or, in multi-user contexts, more granular
identifiers) to directory identities so policy can be written against
"Finance" rather than a subnet. Common identity-mapping sources:

| Method | Mechanism |
| --- | --- |
| PAN-OS integrated User-ID agent | Reads domain controller security event logs directly |
| Windows-based User-ID agent | Same log-reading approach, run on a dedicated Windows host |
| Terminal Server / Citrix agent | Maps individual users sharing one host IP via session tracking |
| Syslog listener | Parses identity events from a firewall/VPN/NAC syslog source |
| Captive portal | Interactive authentication when no other mapping exists |
| XFF (X-Forwarded-For) header | Extracts client identity from a load balancer or proxy header |
| GlobalProtect | Identity established at VPN/agent login |

**Group mapping** is a related but distinct configuration: it retrieves
group membership from a directory (via LDAP) so policy can reference
"Finance-Group" as a group object rather than enumerating individual
usernames, and so group membership changes in the directory are reflected
in policy automatically on the next mapping refresh.

### Content-ID security profiles

Once a session is permitted by App-ID/User-ID/zone match, **Content-ID**
security profiles perform the deep inspection:

| Profile | Function |
| --- | --- |
| Antivirus | Signature-based malware detection in file transfers |
| Anti-Spyware | Detects command-and-control traffic and spyware phone-home behavior |
| Vulnerability Protection | IPS — blocks exploit attempts against known CVEs |
| URL Filtering | Category-based web access control, integrated with Advanced URL Filtering ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)) |
| File Blocking | Controls file types allowed to transfer, by direction and application |
| WildFire Analysis | Forwards unknown files for cloud/appliance sandbox detonation |
| Data Filtering | Pattern-based data loss prevention (predates and complements Enterprise DLP) |
| DoS Protection | Per-zone or per-rule flood protection, distinct from zone protection profiles ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)) |

Profiles are typically bundled into a **security profile group** and
attached to a rule as a set, rather than attaching each profile
individually to every rule — this keeps a consistent inspection baseline
across the rulebase and makes a fleet-wide profile update a single change
rather than dozens.

### Why decryption matters

Content-ID's security profiles inspect the actual payload stream. An
encrypted TLS session is opaque to every profile above except metadata-only
signals (SNI, certificate details) — Content-ID cannot detect malware
inside a file downloaded over HTTPS it cannot decrypt. **SSL Forward
Proxy** decryption terminates outbound client TLS sessions at the firewall,
re-establishes a new TLS session to the actual destination, and inspects
the plaintext in between, presenting a firewall-signed certificate to the
internal client (which must trust the firewall's decryption CA).
**SSL Inbound Inspection** does the reverse for traffic to an
organization's own published TLS services, using the server's actual
private key so the firewall can decrypt and inspect inbound sessions
without any client-trust requirement. Given that most enterprise and
malicious traffic alike is now TLS-encrypted by default, an
undecrypted rulebase is Content-ID-blind for the majority of sessions
crossing it, regardless of how well-tuned the App-ID and User-ID rules are.

## Design Considerations

- **App-ID-based rules over port-based rules, as a hard default.** Every
  new rule should specify a real application (or application filter/group)
  rather than `application: any`. An `any/any/any-permit` rule is a
  port-based rule wearing an App-ID interface and defeats the platform's
  core value proposition.
- **Security profile group as the mandatory default,** not an optional
  add-on per rule. Establish one or a small number of standard profile
  groups (for example, a strict group for Internet-facing traffic and a
  slightly relaxed group for trusted East-West traffic) and require every
  allow rule to carry one, rather than leaving profile attachment to
  individual rule authors' discretion.
- **Decryption scope and exceptions.** Decrypting 100% of outbound traffic
  is rarely feasible immediately — legal, compliance, and technical
  categories (personal banking, healthcare, some SaaS with certificate
  pinning that breaks under interception) commonly require decryption
  exclusions. Plan a phased decryption rollout by URL category and
  business risk rather than attempting a single cutover, and maintain a
  documented, reviewed decrypt-exclusion list rather than an ad hoc,
  undocumented one.
- **User-ID source selection.** The integrated agentless User-ID agent
  (reading domain controller logs directly from PAN-OS) is the lowest-
  operational-overhead option for a standard Active Directory environment
  and is a reasonable default; a dedicated Windows-based agent or
  Terminal Server agent is needed when the environment includes shared-host
  scenarios (RDS/Citrix) where IP-to-user mapping is one-to-many.
  Multi-source User-ID (agent plus syslog plus GlobalProtect) is common in
  mature environments to cover on-premises, remote, and multi-user hosts
  simultaneously.
- **Data Filtering vs. Enterprise DLP.** Built-in Data Filtering profiles
  use administrator-defined patterns (regex, file properties) and are
  adequate for straightforward, well-known data patterns (national ID
  formats, keyword lists). Organizations with cross-platform data
  protection requirements (the same policy enforced consistently across
  NGFW, Prisma Access, and SaaS Security) should evaluate the Enterprise
  DLP subscription ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)) instead of maintaining parallel,
  platform-specific pattern sets.

## Implementation and Automation

### Building a security policy rule with App-ID and User-ID

```text
admin@pa-fw01# set rulebase security rules Finance-to-SaaS from trust to untrust source any destination any source-user Finance-Group application [ web-browsing ssl salesforce ] service application-default action allow
admin@pa-fw01# set rulebase security rules Finance-to-SaaS profile-setting group Standard-Inspection
admin@pa-fw01# set rulebase security rules Finance-to-SaaS log-end yes
admin@pa-fw01# commit
```

`service application-default` restricts the rule to each application's
standard, expected ports — an important complement to App-ID that prevents
an application from being permitted on an arbitrary port simply because it
was classified correctly.

### Configuring the integrated User-ID agent

```text
admin@pa-fw01# set zone trust network enable-user-identification yes
admin@pa-fw01# set deviceconfig setting server-profile ldap-profile ADProfile server ad01.acme.local port 389
admin@pa-fw01# set user-id-collector setting server-monitor domain-controller ad01 host 10.10.10.20
admin@pa-fw01# set user-id-collector setting server-monitor domain-controller ad01 domain-name ACME
admin@pa-fw01# commit
```

Group mapping is configured under `Device > User Identification > Group
Mapping Settings` (or the equivalent `set` path under
`deviceconfig setting ldap`) pointing at the same or a dedicated LDAP
service account with read access to directory group membership.

### Building a security profile group

```text
admin@pa-fw01# set profiles virus Strict-AV decoder [ smtp imap pop3 http ftp ]
admin@pa-fw01# set profiles vulnerability Strict-Vuln rules default
admin@pa-fw01# set profiles spyware Strict-Spyware rules default
admin@pa-fw01# set profiles url-filtering Strict-URL block [ malware phishing command-and-control ]
admin@pa-fw01# set profile-group Standard-Inspection virus Strict-AV
admin@pa-fw01# set profile-group Standard-Inspection vulnerability Strict-Vuln
admin@pa-fw01# set profile-group Standard-Inspection spyware Strict-Spyware
admin@pa-fw01# set profile-group Standard-Inspection url-filtering Strict-URL
admin@pa-fw01# set profile-group Standard-Inspection wildfire-analysis default
admin@pa-fw01# commit
```

### Configuring SSL Forward Proxy decryption

```text
admin@pa-fw01# set shared ssl-decrypt trusted-root-CA Firewall-Decrypt-CA
admin@pa-fw01# set rulebase decryption rules Decrypt-Outbound-Web from trust to untrust source any destination any service any category any action decrypt type ssl-forward-proxy
admin@pa-fw01# set rulebase decryption rules Decrypt-Exclude-Finance from trust to untrust source any destination any category [ financial-services health-and-medicine ] action no-decrypt
admin@pa-fw01# commit
```

Decryption rules, like security and NAT rules, are evaluated top-down;
place `no-decrypt` exclusion rules above the broader decrypt rule they are
meant to carve an exception out of. The firewall's decryption CA
certificate must be distributed to and trusted by managed endpoints
(typically via Group Policy or an MDM-pushed trust store) before SSL
Forward Proxy decryption is enabled broadly, or clients will present
certificate-trust errors for every decrypted site.

### Testing a policy match without live traffic

```text
admin@pa-fw01> test security-policy-match from trust to untrust source 10.10.20.15 destination 8.8.8.8 destination-port 443 protocol 6 application ssl source-user acme\\jsmith
```

## Validation and Troubleshooting

- **Traffic permitted by an unintended, broader rule.** `test
  security-policy-match` reports the exact rule name that would match a
  given flow — use it before assuming a rule change is required, since the
  actual match is frequently an earlier, broader rule rather than the rule
  the administrator just edited.
- **User-ID not mapping a source IP.** `show user ip-user-mapping all`
  lists current mappings; if a host is missing, confirm the User-ID agent
  or agentless collector has connectivity to the domain controller's
  security event log, that the domain controller is actually logging
  logon events (Windows auditing must be enabled for the relevant event
  IDs), and that the zone has `enable-user-identification` set — User-ID
  only maps within zones explicitly enabled for it.
- **Application misclassified as `unknown-tcp`/`unknown-udp`.** Confirm
  Applications and Threats content ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)) is current, since new
  application signatures ship in every content release; if the traffic is
  a legitimate internal/custom protocol with no existing signature,
  evaluate a custom application definition or an App-ID enhancement
  request rather than defaulting to a broad port-based permit rule.
- **Decryption breaks a specific application.** Some applications use
  certificate pinning or mutual TLS and will fail, not silently degrade,
  under interception. Add a `no-decrypt` exception for the specific
  category/destination rather than disabling decryption broadly; `show
  session id <id>` and the decryption logs (`Monitor > Logs > Decryption`)
  identify the specific failure reason (unsupported cipher, pinned
  certificate, expired certificate on the origin server).
- **Security profile action not triggering as expected.** Confirm the
  profile (or profile group) is actually attached to the matching rule —
  `show rulebase security rules <name>` displays the currently attached
  profile settings — and that the relevant content update (Antivirus,
  WildFire signatures) is current, since a profile with stale content
  enforces stale detections.

## Security and Best Practices

- Default every new security rule to a specific application list and a
  source-user or source-address scope; treat any rule proposal using
  `application: any` as requiring explicit written justification and a
  compensating profile group at minimum.
- Log at session end (not session start only) for every allow rule so
  byte counts, duration, and final App-ID classification are captured —
  session-start-only logging captures the initial classification but
  misses data that changes as App-ID refines its verdict mid-session.
- Treat Application Override as an exception mechanism, not a
  troubleshooting shortcut; document every override rule's justification,
  since it removes Content-ID inspection for the overridden session.
- Roll out decryption in phases by risk and by user population, starting
  with the highest-risk categories (general web browsing, newly registered
  domains) and expanding coverage as certificate-trust distribution and
  exception handling mature; do not attempt a single big-bang cutover for
  the entire user population.
- Restrict who can create or modify `no-decrypt` exclusion rules — an
  overly broad decrypt exclusion is a common way security teams
  unknowingly reintroduce the exact blind spot decryption was deployed to
  close.
- Review Data Filtering and WildFire Analysis profile logs on a recurring
  cadence, not only on alert; unknown-file submission volume and pattern
  matches over time reveal policy tuning opportunities that individual
  alerts do not.

## References and Knowledge Checks

**References**

- [Palo Alto Networks, *PAN-OS Administrator's Guide*](https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-admin) — Security Policy,
  App-ID, User-ID, Content-ID, and Decryption chapters (version 11.1).
- [Palo Alto Networks, *Decryption Best Practices* documentation.](https://docs.paloaltonetworks.com/best-practices/10-2/decryption-best-practices)
- [Palo Alto Networks, *App-ID Technology Brief*.](https://www.paloaltonetworks.com/resources/techbriefs/app-id-tech-brief)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — PAN-OS 11.x
  baseline used throughout this volume.

**Knowledge checks**

1. Why does `service application-default` matter on an App-ID-based
   security rule, even though the application has already been correctly
   classified?
2. What is the practical difference between the built-in Data Filtering
   profile and the Enterprise DLP subscription introduced in [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)?
3. Why can Content-ID security profiles not inspect the payload of an
   undecrypted TLS session, and which PAN-OS feature addresses that gap
   for outbound traffic initiated by internal clients?
4. Which CLI command reports current User-ID IP-to-username mappings, and
   which zone-level setting must be enabled before mappings apply within
   that zone?

## Hands-On Lab

**Objective:** Build an App-ID-based security policy rule with an attached
security profile group, validate its match behavior, and configure a
scoped SSL Forward Proxy decryption rule with a category-based exclusion —
including a negative test confirming an unauthorized application is
blocked.

**Prerequisites**

- A lab PAN-OS firewall with the Layer 3 interfaces, zones, routing, and
  NAT configured in [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)'s lab.
- Current Applications and Threats content ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)).
- A test client in the trust zone able to generate outbound HTTPS traffic.
- Administrative access to distribute a certificate to the test client's
  trust store (or a test client where trust warnings can be manually
  accepted for lab purposes).

**Steps**

1. Create a security profile group:

   ```text
   admin@pa-fw01# set profiles vulnerability Strict-Vuln rules default
   admin@pa-fw01# set profiles spyware Strict-Spyware rules default
   admin@pa-fw01# set profile-group Lab-Inspection vulnerability Strict-Vuln
   admin@pa-fw01# set profile-group Lab-Inspection spyware Strict-Spyware
   admin@pa-fw01# set profile-group Lab-Inspection wildfire-analysis default
   admin@pa-fw01# commit
   ```

2. Replace the [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md) lab's broad outbound rule with an application-
   scoped rule:

   ```text
   admin@pa-fw01# delete rulebase security rules Allow-Outbound-Web
   admin@pa-fw01# set rulebase security rules Allow-Outbound-Web-Scoped from trust to untrust source any destination any application [ web-browsing ssl dns ] service application-default action allow
   admin@pa-fw01# set rulebase security rules Allow-Outbound-Web-Scoped profile-setting group Lab-Inspection
   admin@pa-fw01# set rulebase security rules Allow-Outbound-Web-Scoped log-end yes
   admin@pa-fw01# commit
   ```

3. Validate the match with a simulated lookup:

   ```text
   admin@pa-fw01> test security-policy-match from trust to untrust source 10.10.20.15 destination 93.184.216.34 destination-port 443 protocol 6 application ssl
   ```

   **Expected result:** `Allow-Outbound-Web-Scoped` is reported as the
   matching rule.

4. **Negative test:** Simulate a match for an application not included in
   the rule, such as a peer-to-peer or unsanctioned file-sharing
   application:

   ```text
   admin@pa-fw01> test security-policy-match from trust to untrust source 10.10.20.15 destination 93.184.216.34 destination-port 443 protocol 6 application bittorrent
   ```

   **Expected result:** No rule matches other than the default interzone
   or intrazone deny, confirming the scoped rule does not implicitly
   permit unrelated applications.

5. Generate real outbound HTTPS traffic from the test client and confirm
   the session in the traffic log:

   ```text
   admin@pa-fw01> show session all filter application ssl
   ```

6. Configure a decryption CA and a scoped decrypt rule:

   ```text
   admin@pa-fw01# set rulebase decryption rules Decrypt-Outbound-Lab from trust to untrust source any destination any category any action decrypt type ssl-forward-proxy
   admin@pa-fw01# set rulebase decryption rules Decrypt-Exclude-Financial from trust to untrust source any destination any category financial-services action no-decrypt
   admin@pa-fw01# commit
   ```

   Order matters: confirm `Decrypt-Exclude-Financial` is listed above
   `Decrypt-Outbound-Lab` in the rulebase (`show rulebase decryption
   rules`); if not, use `move` to reorder it.

7. Distribute or manually trust the firewall's decryption CA certificate on
   the test client, then browse to a non-excluded HTTPS site and confirm
   decrypted inspection in `Monitor > Logs > Decryption` (or `show session
   id <id>` for the active session, noting the decryption flag).

8. Browse to a site categorized as `financial-services` and confirm it is
   **not** decrypted (no certificate warning, and the decryption log shows
   `no-decrypt` as the reason).

9. **Cleanup:** If this lab environment will be reused in later chapters,
   leave the scoped rule, profile group, and decryption configuration in
   place; otherwise remove the lab-only decryption rules and CA trust from
   the test client:

   ```text
   admin@pa-fw01# delete rulebase decryption rules Decrypt-Outbound-Lab
   admin@pa-fw01# delete rulebase decryption rules Decrypt-Exclude-Financial
   admin@pa-fw01# commit
   ```

## Summary and Completion Checklist

Security policy on PAN-OS is where App-ID, User-ID, and Content-ID come
together into enforceable rules: applications and identities replace ports
and subnets as the primary match criteria, security profile groups apply
consistent deep inspection, and decryption is the prerequisite that makes
that inspection meaningful against the TLS-encrypted majority of modern
traffic. [Chapter 06](06-panorama-installation-central-management-and-logging.md) extends this same rule model to Panorama-managed device
groups so it can be applied consistently across a fleet rather than one
firewall at a time.

- [ ] Can write an App-ID- and User-ID-based security rule and explain why
      it is preferable to a port-based rule.
- [ ] Can configure User-ID identity mapping and group mapping against a
      directory service.
- [ ] Can build and attach a security profile group covering Antivirus,
      Vulnerability Protection, Anti-Spyware, URL Filtering, and WildFire
      Analysis.
- [ ] Can configure a scoped SSL Forward Proxy decryption rule with a
      category-based exclusion.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
