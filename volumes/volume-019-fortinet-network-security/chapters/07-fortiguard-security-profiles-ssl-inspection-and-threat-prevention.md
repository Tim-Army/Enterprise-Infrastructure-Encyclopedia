# Chapter 07: FortiGuard Security Profiles, SSL Inspection, and Threat Prevention

![Lab flow for this chapter: antivirus, IPS, web-filter, and application-control profiles attach to the outbound policy with SSL certificate inspection; downloading a standard antivirus test file is blocked and logged, and browsing a filtered category is blocked and logged. Switching to full deep inspection without installing the firewall's CA certificate produces a browser trust warning; installing the certificate removes the warning and gives antivirus and IPS visibility into HTTPS content they couldn't inspect before. As a negative test, an explicit allow override is added for the previously blocked category; the site becomes reachable, confirming the override mechanism works, before it is reverted.](../../../diagrams/volume-019-fortinet-network-security/chapter-07-security-profiles-ssl-inspection-flow.svg)

*Figure 7-1. Flow used throughout this chapter's Hands-On Lab: AV/IPS/web-filter/app-control profiles and SSL inspection validated against real test traffic, tested against a category-allow override.*

## Learning Objectives

- Describe the FortiGuard security services and how flow-based and
  proxy-based inspection differ.
- Configure antivirus, IPS, web filtering, and application control
  profiles and attach them to a firewall policy.
- Configure certificate-inspection and full SSL deep-inspection profiles
  and explain the trust and privacy trade-offs of each.
- Integrate FortiSandbox verdicts into the inspection path.
- Diagnose security-profile blocking behavior and SSL inspection
  certificate errors.

## Theory and Architecture

### FortiGuard security services

FortiGuard is Fortinet's cloud-delivered threat intelligence and content
service, supplying the signature, category, and reputation data that
FortiGate's security profiles enforce:

| Service | Function |
| --- | --- |
| Antivirus (AV) | Signature and heuristic-based malware detection in file transfers |
| Intrusion Prevention System (IPS) | Signature- and behavior-based blocking of known exploit patterns against vulnerable protocols/services |
| Web Filtering | URL category-based access control using FortiGuard's continuously updated category database |
| Application Control | Identifies and controls traffic by application signature, independent of port, distinguishing (for example) sanctioned from unsanctioned use of the same underlying protocol |
| DNS Filter | Category and reputation-based filtering at the DNS resolution stage, blocking a lookup before a connection is even attempted |
| Anti-Spam | Signature and reputation-based filtering for FortiMail and FortiGate-inspected mail flows |
| Botnet/C2 Detection | Identifies traffic matching known command-and-control infrastructure |
| FortiSandbox integration | Cloud or on-premises detonation of unknown files, with verdicts fed back into AV signature updates fleet-wide |

### Flow-based vs. proxy-based inspection

FortiOS security profiles operate in one of two inspection modes:

- **Flow-based inspection** examines traffic as it passes through the
  firewall without fully buffering the payload, offering lower latency and
  higher throughput at the cost of some detection depth compared to full
  proxy reconstruction. Flow-based is the default and recommended mode for
  most profile types on current FortiOS releases and benefits most
  directly from NP/CP hardware acceleration ([Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)) where available.
- **Proxy-based inspection** fully reconstructs the session (buffering
  and reassembling content) before applying inspection, enabling deeper
  content analysis for certain profile types at a higher CPU and latency
  cost, and without the same degree of NP-level offload.

Profile type availability and default mode vary by FortiOS release and
profile; this volume's examples use flow-based mode, the current default
for antivirus, IPS, application control, and web filtering on the
FortiOS 7.6.x baseline.

### SSL/TLS inspection

The majority of enterprise traffic is TLS-encrypted, which means security
profiles that inspect content (AV, IPS payload matching, application
control depth, web filtering by page content rather than just SNI) cannot
see anything meaningful without the FortiGate participating in the TLS
session itself. FortiOS offers two SSL inspection profile types:

- **Certificate inspection** only reads the TLS handshake's certificate
  and SNI (server name indication) field — enough to enforce web filtering
  and application control by domain/category — without decrypting the
  session payload. This preserves end-to-end encryption and requires no
  certificate trust changes on clients, at the cost of no visibility into
  the encrypted payload itself (so AV and deep IPS payload inspection
  cannot act on it).
  Because SNI is legible before the FortiGate needs to open the session,
  certificate inspection performance overhead is low even on
  non-accelerated deployments.
- **Full SSL inspection ("deep inspection")** terminates the client's TLS
  session at the FortiGate and re-establishes a new outbound TLS session
  to the actual destination, acting as an authorized on-path party — the
  firewall presents a FortiGate-signed certificate to the internal client
  (which must trust the FortiGate's CA certificate) and validates/inspects
  the real payload before re-encrypting it toward the destination. This
  restores payload-level AV, IPS, and DLP visibility over TLS traffic, at
  the cost of requiring CA certificate trust distribution to every client,
  materially higher CPU cost, and a genuine privacy/legal consideration
  since the organization is technically intercepting encrypted
  communication its own traffic policy governs.

### Security profile groups and policy attachment

Individual profiles (`config antivirus profile`, `config ips sensor`,
`config webfilter profile`, `config application list`, and others) are
created independently and then referenced by name on a firewall policy's
inspection fields — a policy is not required to reference every profile
type, and different policies commonly apply different profile
combinations depending on the traffic they govern (for example, a DMZ
inbound policy may apply IPS and AV without web filtering, since inbound
server traffic is not a browsing session).

## Design Considerations

- **Full inspection privacy and legal review.** Full SSL inspection is a
  deliberate interception of otherwise-encrypted traffic; involve legal
  and HR stakeholders before enabling it broadly, publish the practice in
  the organization's acceptable use policy, and exempt categories with
  specific legal sensitivity (banking, healthcare portals, and
  jurisdiction-specific categories) from deep inspection rather than
  inspecting everything indiscriminately.
- **Certificate distribution at scale.** Full inspection requires every
  client to trust the FortiGate's CA certificate; distribute it via Group
  Policy, MDM, or a configuration management baseline ([Volume IX](../../volume-009-infrastructure-automation/README.md)) rather
  than manual per-device installation, and plan for certificate rotation
  before the CA certificate's validity expires.
- **Performance impact of deep inspection.** Proxy-mode deep inspection is
  CPU-intensive and benefits less from NP-level hardware offload than
  flow-based, certificate-only inspection; size the platform (or the
  FortiGate-VM's vCPU allocation) against expected concurrent
  deep-inspected sessions, not just total throughput, and validate actual
  CPU headroom (`get system performance status`) after enabling deep
  inspection rather than assuming rated throughput figures still apply
  unchanged.
- **False-positive tuning process.** Web filtering category
  misclassification and IPS false positives on legitimate internal
  applications are inevitable at scale; define a change-controlled
  exception process (a specific override rule tied to a specific
  business justification and review date) rather than ad hoc, undocumented
  bypasses that erode the profile's overall effectiveness over time.

## Implementation and Automation

### Antivirus and IPS profiles

```text
FGT-LAB-01 # config antivirus profile
FGT-LAB-01 (profile) # edit "AV-Standard"
FGT-LAB-01 (AV-Standard) # set feature-set flow
FGT-LAB-01 (AV-Standard) # config http
FGT-LAB-01 (http) # set av-scan block
FGT-LAB-01 (http) # end
FGT-LAB-01 (AV-Standard) # config ftp
FGT-LAB-01 (ftp) # set av-scan block
FGT-LAB-01 (ftp) # end
FGT-LAB-01 (AV-Standard) # set scan-mode full
FGT-LAB-01 (AV-Standard) # next
FGT-LAB-01 (profile) # end
FGT-LAB-01 # config ips sensor
FGT-LAB-01 (sensor) # edit "IPS-Standard"
FGT-LAB-01 (IPS-Standard) # config entries
FGT-LAB-01 (entries) # edit 1
FGT-LAB-01 (1) # set severity high critical
FGT-LAB-01 (1) # set action block
FGT-LAB-01 (1) # next
FGT-LAB-01 (entries) # end
FGT-LAB-01 (IPS-Standard) # next
FGT-LAB-01 (sensor) # end
```

### Web filter and application control profiles

```text
FGT-LAB-01 # config webfilter profile
FGT-LAB-01 (profile) # edit "WebFilter-Standard"
FGT-LAB-01 (WebFilter-Standard) # config ftgd-wf
FGT-LAB-01 (ftgd-wf) # config filters
FGT-LAB-01 (filters) # edit 1
FGT-LAB-01 (1) # set category 26
FGT-LAB-01 (1) # set action block
FGT-LAB-01 (1) # next
FGT-LAB-01 (filters) # edit 2
FGT-LAB-01 (2) # set category 61
FGT-LAB-01 (2) # set action block
FGT-LAB-01 (2) # next
FGT-LAB-01 (filters) # end
FGT-LAB-01 (ftgd-wf) # end
FGT-LAB-01 (WebFilter-Standard) # next
FGT-LAB-01 (profile) # end
FGT-LAB-01 # config application list
FGT-LAB-01 (list) # edit "AppCtrl-Standard"
FGT-LAB-01 (AppCtrl-Standard) # config entries
FGT-LAB-01 (entries) # edit 1
FGT-LAB-01 (1) # set category 6
FGT-LAB-01 (1) # set action block
FGT-LAB-01 (1) # next
FGT-LAB-01 (entries) # end
FGT-LAB-01 (AppCtrl-Standard) # next
FGT-LAB-01 (list) # end
```

Category IDs (such as `26` for Malicious Websites or `61` for Phishing in
a representative FortiGuard category taxonomy) are FortiGuard-maintained
and should be confirmed against the current category list
(`diagnose webfilter fortiguard categories` or the GUI's category
picker) rather than assumed static across every release, since Fortinet
periodically revises category numbering and grouping.

### SSL inspection profiles

```text
FGT-LAB-01 # config firewall ssl-ssh-profile
FGT-LAB-01 (ssl-ssh-profile) # edit "Certificate-Inspection"
FGT-LAB-01 (Certificate-Inspection) # config https
FGT-LAB-01 (https) # set ports 443
FGT-LAB-01 (https) # set status certificate-inspection
FGT-LAB-01 (https) # end
FGT-LAB-01 (Certificate-Inspection) # next
FGT-LAB-01 (ssl-ssh-profile) # edit "Full-Deep-Inspection"
FGT-LAB-01 (Full-Deep-Inspection) # config https
FGT-LAB-01 (https) # set ports 443
FGT-LAB-01 (https) # set status deep-inspection
FGT-LAB-01 (https) # end
FGT-LAB-01 (Full-Deep-Inspection) # set caname "Fortinet_CA_SSL"
FGT-LAB-01 (Full-Deep-Inspection) # next
FGT-LAB-01 (ssl-ssh-profile) # end
```

For a production deployment, `caname` should reference an
enterprise-issued CA certificate imported specifically for this purpose
(`execute vpn certificate ca import`, or generated via an internal PKI)
rather than the default `Fortinet_CA_SSL` factory certificate, so client
trust distribution matches the organization's existing PKI rather than a
Fortinet-shared default.

### Attaching profiles to a firewall policy

```text
FGT-LAB-01 # config firewall policy
FGT-LAB-01 (policy) # edit 1
FGT-LAB-01 (1) # set av-profile "AV-Standard"
FGT-LAB-01 (1) # set ips-sensor "IPS-Standard"
FGT-LAB-01 (1) # set webfilter-profile "WebFilter-Standard"
FGT-LAB-01 (1) # set application-list "AppCtrl-Standard"
FGT-LAB-01 (1) # set ssl-ssh-profile "Certificate-Inspection"
FGT-LAB-01 (1) # set logtraffic all
FGT-LAB-01 (1) # next
FGT-LAB-01 (policy) # end
```

This attaches the full security-profile stack to policy 1
(`LAN-to-WAN-Outbound` from [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)), turning the previously simple
permit/NAT decision into a fully inspected outbound path.

### FortiSandbox integration

```text
FGT-LAB-01 # config system fortisandbox
FGT-LAB-01 (fortisandbox) # set status enable
FGT-LAB-01 (fortisandbox) # set forticloud enable
FGT-LAB-01 (fortisandbox) # end
FGT-LAB-01 # config antivirus profile
FGT-LAB-01 (profile) # edit "AV-Standard"
FGT-LAB-01 (AV-Standard) # set analytics-bl-filetype all
FGT-LAB-01 (AV-Standard) # next
FGT-LAB-01 (profile) # end
```

`forticloud enable` uses Fortinet's cloud-hosted FortiSandbox service; an
on-premises FortiSandbox appliance is referenced instead with `set
fortisandbox <ip>` when the organization operates its own sandbox
infrastructure.

## Validation and Troubleshooting

- **Confirming a block is happening for the expected reason.** The
  FortiGuard block page (or the connection reset behavior for
  non-web protocols) identifies which profile matched; cross-reference
  with `diagnose debug flow` output showing which profile field
  (`av-profile`, `ips-sensor`, `webfilter-profile`) triggered the block,
  rather than assuming which control fired.
- **Deep inspection performance impact.** After enabling deep inspection
  broadly, check `get system performance status` and `diagnose sys top`
  under representative load; a CPU utilization jump disproportionate to
  traffic volume increase indicates the platform (or VM vCPU allocation)
  is undersized for proxy-mode inspection at the intended scale.
- **Client certificate trust errors.** A browser TLS warning after
  enabling deep inspection almost always means the FortiGate's CA
  certificate (or the organization's PKI-issued equivalent referenced by
  `caname`) has not been distributed to and trusted by that client;
  confirm distribution mechanism (Group Policy/MDM) reached the affected
  device before assuming an inspection-profile misconfiguration.
- **Category-based web filter unexpectedly blocking legitimate traffic.**
  Use `diagnose webfilter fortiguard categories` and the GUI's URL lookup
  tool to confirm which FortiGuard category a specific destination is
  currently classified under; category misclassification is reportable to
  Fortinet through the same GUI tool, and the fix should go through both
  a review-approved local override and the vendor reclassification
  request, not just a permanent local override alone.
- **Sandbox verdict not reflected in AV blocking.** Confirm
  `config system fortisandbox` shows `status enable` and connectivity to
  the sandbox service, and check the sandbox submission/verdict log
  (**Security Fabric > Fabric Connectors** telemetry or
  `diagnose sandbox` where available on the release in use) — a common
  gap is a file type not included in `analytics-bl-filetype`, which
  silently skips sandbox submission for that type.

## Security and Best Practices

- Enable logging (`logtraffic all` plus profile-level logging) on every
  policy carrying security profiles; a block that is not logged cannot be
  investigated, tuned, or reported on.
- Keep FortiGuard content current through scheduled updates
  ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) covers scheduling and centralized update management in
  depth); an expired or stale FortiGuard subscription silently degrades
  every profile type described in this chapter without an obvious service
  interruption.
- Do not enable full SSL deep inspection organization-wide without a
  documented privacy/legal review and a category-based exemption list for
  sensitive destinations; document the practice in the acceptable use
  policy referenced in [Chapter 01](01-nse-1-cybersecurity-awareness-and-digital-safety.md).
- Rotate and protect the private key behind any CA certificate used for
  deep inspection with the same rigor as any other PKI root/intermediate
  key material — compromise of that key would allow undetected
  interception of any client that trusts it.
- Treat FortiSandbox integration as a meaningful gap-closer specifically
  for unknown/zero-day threats that signature-based AV cannot match
  (consistent with [Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md)'s kill-chain framing), not as a redundant
  feature layered on top of already-adequate AV coverage.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/8.0.0) — security profiles, SSL
  inspection, and FortiSandbox integration.
- [Fortinet, *FortiOS CLI Reference*](https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/84566/fortios-cli-reference) — `config antivirus profile`,
  `config ips sensor`, `config webfilter profile`,
  `config firewall ssl-ssh-profile`, `config system fortisandbox`.
- [Fortinet NSE Training Institute, *NSE 4: FortiGate Security* course
  (security profiles and SSL inspection domains).](https://training.fortinet.com/local/staticpage/view.php?page=nse_4)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. What is the practical difference between certificate inspection and
   full SSL deep inspection, and which profile types depend on which
   mode?
2. Why does full SSL deep inspection require distributing a CA certificate
   to every client, and what happens to a client that has not received
   it?
3. Name two reasons flow-based inspection is generally preferred over
   proxy-based inspection for most profile types on current FortiOS
   releases.
4. Why is a security-profile block that is not logged a practical problem
   even if the block itself is functioning correctly?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each task under the NSE 4
objective *Content Inspection* (25–30% — the largest single objective of the FortiOS
7.6 Administrator exam)** — mapped in the volume README's coverage tables. Every command
is a real FortiOS 7.6 CLI action; each lab ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 7.1–7.7** — a FortiGate on FortiOS 7.6 with a valid
FortiGuard subscription, a client behind it, and a permit policy from LAN to WAN to
attach profiles to. **Cost:** none beyond lab resources.

### Lab 7.1 — SSL/SSH deep inspection (Topic: SSL inspection)

**Eval FortiGate — config yes, re-sign no.** Deep inspection needs no FortiGuard subscription and its *configuration* is accepted on the eval — but a live test (below) shows the eval's low-encryption proxy cannot actually complete the re-signed TLS handshake for a modern flow. `certificate-inspection` (SNI/cert peek, no re-sign) works on the eval; full `deep-inspection` of a live session needs a licensed FortiGate. The profile still underpins the subscription-gated profiles that follow.

**Objective:** Apply deep-inspection so encrypted flows can be scanned.

```text
config firewall ssl-ssh-profile
    edit deep-lab
        set comment "Lab deep inspection"
        config https
            set ports 443
            set status deep-inspection
        end
    next
end
```

> **Eval adaptation — the profile table is capped, so reuse a built-in.** On the evaluation
> FortiGate-VM the `firewall ssl-ssh-profile` table is already full at its four built-ins, so
> creating a *new* `deep-lab` profile is refused: `edit deep-lab` returns `Command fail. Return
> code -4 (reached the maximum number of entries)` — the same low-tier resource cap that blocks
> an extra loopback in [Lab 6.6](06-firewall-policy-authentication-vpn-and-zero-trust-access.md).
> Deep inspection itself is fully supported; you just cannot hold it in a new profile. Instead
> **edit the built-in `custom-deep-inspection`** (its comment is literally *"Customizable deep
> inspection profile"*) or attach the read-only **`deep-inspection`** profile directly to the
> policy. On a licensed FortiGate `edit deep-lab` works normally.

**Confirmed live on the 7.6.7 cluster (17 August 2026).**

- **The re-sign trust anchor.** `get vpn certificate local details` shows `Fortinet_CA_SSL` is a
  **self-signed CA** (Subject equals Issuer, CN = the FortiGate's own serial number, valid ten
  years). Every server certificate the FortiGate intercepts is re-issued under this CA, so a
  client behind deep inspection sees an issuer of *the FortiGate's serial*, not the site's real
  CA. A second anchor, `Fortinet_CA_Untrusted`, re-signs sessions whose *original* server cert
  failed validation — so the client still gets a browser warning instead of a silently-trusted
  forgery.
- **The built-in `deep-inspection` reference** (`show full-configuration firewall ssl-ssh-profile
  deep-inspection`) is exactly what `custom-deep-inspection` inherits: `set server-cert-mode
  re-sign`, `set caname "Fortinet_CA_SSL"`, `set untrusted-caname "Fortinet_CA_Untrusted"`, and
  `config https` → `set status deep-inspection` on port 443 with `min-allowed-ssl-version tls-1.1`
  and `quic inspect`. The eval carries the full *config* for a deep profile, strong-cipher settings
  and all — whether it can actually re-sign a live session is a separate question, tested below.
- **A 32-entry `ssl-exempt` allow-list ships enabled by default**, so deep inspection deliberately
  does **not** decrypt FortiGuard categories **31 (Health)** and **33 (Finance and Banking)**, nor
  a list of certificate-pinned application FQDNs (Apple, Microsoft, Google, Dropbox, Skype, …).
  Deleting those exemptions is what breaks banking apps and pinned mobile clients — a classic
  deep-inspection support call.
- **Editing the built-in took and persisted:** `set comment "Lab 7.1 deep inspection"` on
  `custom-deep-inspection` saved cleanly, confirming the built-in is the eval's usable
  deep-inspection vehicle.
- **Live re-sign test — the eval proxies but cannot complete the handshake.** With
  `custom-deep-inspection` attached to the inter-segment policy (`utm-status enable`,
  `service ALL`), a client (`10.30.1.10`) opening TLS to an internal HTTPS server
  (`10.30.2.10`, a throwaway Python listener with a self-signed `CN=db.lab` cert) *through*
  the FortiGate **failed**: TLS 1.3 returned `SSL: RECORD_LAYER_FAILURE` and TLS 1.2 returned
  `SSL: BAD_SIGNATURE` — even with the client's OpenSSL security level dropped to `SECLEVEL=0`,
  so it was not the client being strict. The listener's log showed the FortiGate proxy *did*
  connect on the server side and then reset, so deep inspection was genuinely engaged — the
  eval's low-encryption proxy simply could not produce a re-signed handshake a current client
  accepts. Swapping the *same* policy to `certificate-inspection` (peek, no re-sign)
  **succeeded** immediately: TLS 1.3 / AES-256-GCM, and the client received the origin's real
  `CN=db.lab` certificate untouched. So on the eval, `certificate-inspection` is fully usable
  but full `deep-inspection` of a live modern-TLS session needs a **licensed** FortiGate — the
  strong crypto that completes the re-sign is the same ceiling that blocked the EMS leg in
  [Lab 6.6](06-firewall-policy-authentication-vpn-and-zero-trust-access.md).

**Expected result:** a deep-inspection profile that decrypts, inspects, and re-encrypts
HTTPS — without it, AV/IPS/web-filter see only ciphertext. The FortiGate CA certificate
must be trusted by clients or browsers warn.

**Negative test:** attach only `certificate-inspection` (SNI/cert view) and expect the
antivirus engine to catch malware inside a TLS download; it cannot see the payload —
only deep inspection exposes encrypted content.

**Rollback:**

```text
config firewall ssl-ssh-profile
    delete deep-lab
end
```

On the eval there is no `deep-lab` to delete — instead point the policy's `ssl-ssh-profile`
back to the built-in `no-inspection` and, if you edited it, clear the `custom-deep-inspection`
comment.

### Lab 7.2 — Web filtering (Topic: Web filter)

**Eval FortiGate — subscription-gated.** The profile and policy build fine, but *live* FortiGuard verdicts need an active security-services subscription — the eval's time-limited contract works briefly, then verdicts silently degrade (Chapter 04).

**Objective:** Block a FortiGuard URL category.

```text
config webfilter profile
    edit block-malicious
        config ftgd-wf
            config filters
                edit 0
                    set category 37
                    set action block
                next
            end
        end
    next
end
diagnose test application urlfilter 3
```

> **7.6 gotcha — a new profile's category table is already populated.** Do **not** write
> `edit 1` / `set category 26`: on FortiOS 7.6 a fresh `webfilter profile` pre-populates its
> `ftgd-wf` filters with every rated category, and the FortiGuard **Security Risk** group —
> **26 Malicious Websites, 61 Phishing, 86 Spam URLs, 90 Newly Observed Domain, 91 Newly
> Registered Domain** — already defaults to `action block`. So "block Malicious Websites" is
> the out-of-box state; there is nothing to add. Trying `set category 26` on another row fails
> with `Invalid category ID '26': Duplicate or Group 'Fortiguard' not included`, and `set
> category ?` hides already-used categories (which makes the Security Risk group look
> "missing"). To block a category that *isn't* blocked by default — e.g. Social Networking
> (37) above — add it with `edit 0` (auto-assigned id); to change a default, edit that
> category's existing row.

**Confirmed live on the 7.6.7 cluster (17 August 2026).** The profile builds without a cap
(unlike the SSL-profile table in Lab 7.1), and the pre-populated table above already blocks the
Security Risk categories. The gate is the subscription, and it is measured, not assumed:

- `get system fortiguard` reports `webfilter-license: Unknown` and `webfilter-expiration: N/A`
  (antispam and outbreak-prevention likewise) — no security-services contract on the eval.
- `diagnose debug rating` shows the Web-filter service `Status: Disable`; the default SDNS
  rating server (`208.91.112.220:53`) is configured but has no entitlement behind it.
- `diagnose test application urlfilter 3` returns `Invalid daemon index (.pid file not found)` —
  the urlfilter daemon is not even running, so no live category lookups occur.

So on the eval the block is *configured* (indeed default) but never *enforced against live
ratings*; a paid FortiGuard web-filter contract plus reachability to the rating service is what
turns the pre-populated block actions into real verdicts.

**Expected result:** requests to sites FortiGuard rates as category 26 (Malicious
Websites) are blocked with a replacement page; the web filter enforces acceptable-use
and threat categories against the live FortiGuard rating service.

**Negative test:** block by category but attach the profile to a policy using only
certificate inspection over HTTPS; full-URL and content checks degrade — deep
inspection (Lab 7.1) is what lets web filtering see the full URL and page.

**Rollback:** delete the `block-malicious` profile.

### Lab 7.3 — DNS filtering (Topic: DNS filter)

**Eval FortiGate — subscription-gated.** The profile and policy build fine, but *live* FortiGuard verdicts need an active security-services subscription — the eval's time-limited contract works briefly, then verdicts silently degrade (Chapter 04).

**Objective:** Block malicious domains at resolution time.

```text
config dnsfilter profile
    edit dns-guard
        config ftgd-dns
            config filters
                edit 1
                    set category 26
                    set action block
                next
            end
        end
        set block-botnet enable
    next
end
```

> **7.6 notes — pre-populated table and `block-botnet` placement.** A new `dnsfilter profile`
> pre-populates `ftgd-dns` with the DNS-relevant Security Risk categories — **26 Malicious
> Websites, 61 Phishing, 86 Spam URLs, 88** — all `block` by default, with 26 already in row 1.
> So `edit 1` / `set category 26` edits that existing row and succeeds (it does *not* hit the
> webfilter duplicate trap from Lab 7.2, because dnsfilter's table is short and 26 is slot 1) —
> though it is effectively redundant. And `set block-botnet enable` is a **profile-level**
> command: issue it under `edit dns-guard` *after* the `config ftgd-dns ... end` block — running
> it inside `config ftgd-dns` returns `parse error before 'block-botnet'`.

**Confirmed live on the 7.6.7 cluster (17 August 2026).** The profile and `block-botnet` both
build; the gate is the data behind them, measured with `diagnose autoupdate versions`:

- **The Botnet Domain Database is empty and cannot update:** `Version: 0.00000`, `Contract Expiry
  Date: n/a`, last updated `Mon Jan 1 00:00:00 2001` (i.e. never), and the most recent update
  attempt ended in `Result: Connectivity failure`. So `set block-botnet enable` is enabled but has
  **no domains to act on**.
- **Every FortiGuard fetch fails the same way** — Botnet Domain, Internet-service DB, URL Allow
  list, IP Geography, Certificate Bundle, AntiPhish, and Security Rating all report `Result:
  Connectivity failure`, and every package shows `Contract Expiry Date: n/a`. The isolated lab has
  no path to FortiGuard and no service is under contract.
- The FortiGuard **DNS category rating** that the `ftgd-dns` filters depend on is the same live
  rating service that `diagnose debug rating` reported as `Disable` in Lab 7.2 — so the category
  blocks (26/61/86/88) likewise have no live verdict source.

DNS filtering is therefore fully *configured* on the eval — categories pre-blocked, botnet blocking
enabled — but resolves nothing against live intelligence: the botnet database is empty and the
rating service is unreachable. A paid contract plus FortiGuard connectivity is what turns it on.

**Expected result:** DNS lookups for malicious/botnet domains are redirected to a
block IP before a connection is ever attempted — DNS filtering stops threats one layer
earlier than web filtering and catches non-HTTP protocols.

**Negative test:** rely on web filtering alone for a non-web C2 channel; it evades an
HTTP-only control — DNS filtering covers name resolution across all protocols.

**Rollback:** delete the `dns-guard` profile.

### Lab 7.4 — Application control (Topic: Application control)

**Eval FortiGate — works offline.** Application control matches traffic against the **local**
Application Definitions database (bundled with the firmware), not a live FortiGuard rating query — so
it runs fully on the eval, unlike the web/DNS filters in Labs 7.2–7.3. A subscription only keeps the
signature DB *current*; the eval's is from 2015 (Chapter 04), so it recognizes long-standing apps but
misses anything added since. Confirmed with a live capture below.

**Objective:** Block a peer-to-peer application category regardless of port.

```text
config application list
    edit appctrl-lab
        config entries
            edit 1
                set category 6
                set action block
            next
        end
    next
end
diagnose test application ipsmonitor
```

**Confirmed live on the 7.6.7 cluster (17 August 2026).** Proven end to end with a captured
app-control log. A client (`10.30.1.10`) fetched a plain-HTTP server on a peer (`10.30.2.10`)
listening on **port 8080** — a non-web port — through a policy carrying an application-control list
(with `set other-application-log enable`). The FortiGate identified it on the first request —
retrieved with `execute log filter category utm-app-ctrl` then `execute log display` (note the CLI
log category is `utm-app-ctrl`, not `app-ctrl`):

```text
type="utm" subtype="app-ctrl" eventtype="signature" appid=15893
srcip=10.30.1.10 dstip=10.30.2.10 dstport=8080 proto=6 service="HTTP"
policyid=1 applist="appctrl-lab" action="pass"
appcat="Web.Client" app="HTTP.BROWSER" agent="Wget" httpmethod="GET" url="/"
msg="Web.Client: HTTP.BROWSER" apprisk="medium"
```

- **Signature, not port.** HTTP on `dstport 8080` is still labelled `HTTP.BROWSER` — a port-based
  control would never flag 8080 as web. App control even parsed the request internals (`GET /`, the
  `Wget` agent), which is the whole point of the negative test below.
- **Fully offline.** Every FortiGuard fetch fails on this box (Lab 7.3: `diagnose autoupdate versions`
  → `Connectivity failure`), yet the classification is exact — it comes from the local Application
  Definitions DB with no live rating. That is what separates application control (and antivirus and
  IPS) from the connectivity-gated web and DNS filters in Labs 7.2–7.3.

**Expected result:** applications FortiGuard classifies in category 6 (P2P) are blocked
even when they hop ports or ride over 443 — application control identifies apps by
signature/behavior, not port number.

**Negative test:** try to block P2P with a port-based firewall service; modern apps use
dynamic ports and TLS to evade it — signature-based application control is what
identifies them.

**Rollback:** delete the `appctrl-lab` list.

### Lab 7.5 — Antivirus (Topic: Antivirus)

**Eval FortiGate — works offline.** Antivirus scans the payload against the **local** virus-signature
database and AV engine (both bundled with the firmware), not a live FortiGuard query — so it runs fully
on the eval, like application control (Lab 7.4). A subscription only keeps signatures *current*; the
eval's base set is from 2018 (Chapter 04) but still carries standard detections such as EICAR. Confirmed
with a live block below.

**Objective:** Scan traffic with antivirus and verify with EICAR.

```text
config antivirus profile
    edit av-lab
        set feature-set flow
        config http
            set av-scan block
        end
    next
end
# From a client behind an AV-enabled policy (or host EICAR on an internal server
# if the segment has no internet):
#   curl http://www.eicar.org/download/eicar.com.txt
```

**Confirmed live on the 7.6.7 cluster (17 August 2026).** Proven with a captured antivirus block. A
client (`10.30.1.10`) fetched a locally-hosted EICAR test file — the isolated lab cannot reach
`eicar.org` — from a peer (`10.30.2.10:8080`) through a policy carrying `av-lab`. The download was
**blocked**: the first request reset mid-stream (`200 OK` headers, then `Connection reset by peer`, zero
body bytes), the retry returned `HTTP/1.1 403 Forbidden`. The antivirus log (`execute log filter category
utm-virus`) recorded it:

```text
type="utm" subtype="virus" eventtype="infected" action="blocked"
virus="EICAR_TEST_FILE" virusid=2172 viruscat="Virus" crlevel="critical"
filename="eicar.com.txt" service="HTTP" dstport=8080 policyid=1 profile="av-lab"
srcip=10.30.1.10 dstip=10.30.2.10 dtype="av-engine"
```

- **The local AV engine did the detection** — `dtype="av-engine"` on the first hit (the cached retry
  logs `dtype="cached"`, which is why the repeat got an instant 403). No cloud lookup.
- **Fully offline** — every FortiGuard fetch fails on this box (Lab 7.3), yet AV scanned the HTTP payload
  and blocked a known signature from the bundled 2018 virus definitions. Like application control,
  antivirus is a *local-database* feature, not one of the connectivity-gated rating services.
- **7.6 config note:** the HTTP scan action is `set av-scan block` (or `monitor`), used above — **not**
  `enable`, which returns `command parse error`.

**Expected result:** the EICAR test file (a harmless standard AV test string) is
blocked with a virus replacement message; the antivirus engine scans HTTP/HTTPS/FTP/
SMTP/etc. against FortiGuard signatures (and optionally FortiSandbox).

**Negative test:** download EICAR over HTTPS with only certificate inspection; AV never
sees the payload and it passes — AV inside TLS requires deep inspection (Lab 7.1).

**Rollback:** delete the `av-lab` profile.

### Lab 7.6 — Intrusion prevention (Topic: IPS)

**Eval FortiGate — works offline.** IPS matches traffic against the **local** attack-signature database
in the IPS engine (both bundled with the firmware), not a live FortiGuard query — so it runs fully on the
eval, like application control (Lab 7.4) and antivirus (Lab 7.5). A subscription only keeps signatures
*current*; the eval's base set is from 2015 (Chapter 04) but still carries long-standing exploit
signatures such as Shellshock. Confirmed with a live block below.

**Objective:** Attach an IPS sensor to block known exploits.

```text
config ips sensor
    edit ips-lab
        config entries
            edit 1
                set severity high critical
                set status enable
                set action block
            next
        end
    next
end
diagnose ips signature status
```

**Confirmed live on the 7.6.7 cluster (17 August 2026).** Proven with a captured IPS drop. First,
`diagnose ips signature status` reported the engine loaded with a full pattern set (~10,000 TCP
signatures) — the database is present offline. Then a client (`10.30.1.10`) sent an HTTP request carrying
a **Shellshock** `User-Agent` (`() { :; }; echo shellshock` — harmless to the target but a critical IPS
signature since 2014) to a peer (`10.30.2.10:8080`) through a policy carrying `ips-lab`. The FortiGate
dropped it — the client got no response — and the IPS log (`execute log filter category utm-ips`) named
the signature:

```text
type="utm" subtype="ips" eventtype="signature" severity="critical" action="dropped"
attack="Bash.Function.Definitions.Remote.Code.Execution" attackid=39294
ref="http://www.fortinet.com/ids/VID39294" profile="ips-lab" policyid=1
srcip=10.30.1.10 dstip=10.30.2.10 dstport=8080 service="HTTP"
agent="() { :; }; echo shellshock"
```

- **Matched from the bundled DB, offline.** VID 39294 comes from the 2015 attack definitions; every
  FortiGuard fetch on this box fails (Lab 7.3), yet the engine detected and dropped the exploit pattern.
- **The offline-engine trio.** IPS joins application control (Lab 7.4) and antivirus (Lab 7.5) as
  features that run on their *local* signature databases; only the web and DNS filters (Labs 7.2–7.3) are
  gated by the live FortiGuard rating service and connectivity.

**Expected result:** the sensor blocks traffic matching high/critical FortiGuard IPS
signatures; `diagnose ips` shows the engine loaded — IPS detects and blocks exploit
attempts against known vulnerabilities in real time.

**Negative test:** set the sensor action to `monitor` (log only) and expect exploits to
be stopped; they are recorded but pass — the `block` action is what enforces IPS.

**Rollback:** delete the `ips-lab` sensor.

### Lab 7.7 — Assemble and attach a profile group (Topic: Security profiles on a policy)

**Eval FortiGate — capable.** Assembling and attaching a profile group is pure policy config; each member profile's *live* verdict still depends on its own subscription (Labs 7.2–7.6).

**Objective:** Bind the inspection profiles to a firewall policy.

```text
config firewall policy
    edit 1
        set utm-status enable
        set ssl-ssh-profile deep-lab
        set av-profile av-lab
        set webfilter-profile block-malicious
        set dnsfilter-profile dns-guard
        set application-list appctrl-lab
        set ips-sensor ips-lab
        set logtraffic all
    next
end
diagnose firewall iprope list 100004
```

**Expected result:** one policy now applies SSL inspection, AV, web/DNS filtering,
application control, and IPS to matching traffic — the UTM profile set is applied
**per policy**, so different flows get different inspection depth.

**Negative test:** enable `utm-status` but attach no profiles; nothing is inspected —
the profiles, not the flag alone, perform the content inspection.

**Rollback:** set `utm-status disable` on the policy and remove the profile references,
or delete the test policy.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter turned [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)'s permit/deny/NAT firewall policies into
fully threat-inspected traffic paths: antivirus, IPS, web filtering, and
application control profiles closing the delivery- and
exploitation-stage kill-chain gaps identified in [Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md), SSL
inspection (certificate and full deep-inspection modes) restoring
visibility into encrypted traffic with an explicit trust and privacy
trade-off, and FortiSandbox integration closing the unknown-threat gap
signature-based AV alone cannot close. [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) shifts focus to SD-WAN,
day-two operations, central management, and automation across this now
fully inspected policy set.

- [ ] Can configure and attach antivirus, IPS, web filtering, and
      application control profiles to a firewall policy.
- [ ] Can explain the difference between certificate inspection and full
      SSL deep inspection and the trust distribution deep inspection
      requires.
- [ ] Can integrate FortiSandbox and explain what gap it closes relative
      to signature-based AV.
- [ ] Can diagnose a security-profile block using logs and
      `diagnose debug flow`.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
