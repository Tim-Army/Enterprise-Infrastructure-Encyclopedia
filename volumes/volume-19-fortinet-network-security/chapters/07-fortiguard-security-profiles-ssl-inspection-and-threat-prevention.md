# Chapter 07: FortiGuard Security Profiles, SSL Inspection, and Threat Prevention

![Lab flow for this chapter: antivirus, IPS, web-filter, and application-control profiles attach to the outbound policy with SSL certificate inspection; downloading a standard antivirus test file is blocked and logged, and browsing a filtered category is blocked and logged. Switching to full deep inspection without installing the firewall's CA certificate produces a browser trust warning; installing the certificate removes the warning and gives antivirus and IPS visibility into HTTPS content they couldn't inspect before. As a negative test, an explicit allow override is added for the previously blocked category; the site becomes reachable, confirming the override mechanism works, before it is reverted.](../../../diagrams/volume-19-fortinet-network-security/chapter-07-security-profiles-ssl-inspection-flow.svg)

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
  Policy, MDM, or a configuration management baseline ([Volume IX](../../volume-09-infrastructure-automation/README.md)) rather
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

**Objective:** Build antivirus, IPS, web filtering, and application
control profiles plus a full SSL deep-inspection profile, attach them to
an existing outbound policy, verify blocking behavior against a safe test
file and a known test category, and validate the client certificate trust
requirement — including a negative test exempting one category.

**Prerequisites**

- FGT-LAB-01 with the firewall policies from [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md).
- A LAN test client able to browse the internet through FGT-LAB-01 and
  install the FortiGate's deep-inspection CA certificate for this lab.
- Access to the EICAR standard antivirus test file (a widely published,
  harmless string used specifically to validate AV detection without
  using real malware) for the AV verification step.

**Steps**

1. Create the `AV-Standard`, `IPS-Standard`, `WebFilter-Standard`, and
   `AppCtrl-Standard` profiles as shown in Implementation and Automation.

2. Create the `Certificate-Inspection` and `Full-Deep-Inspection` SSL
   inspection profiles.

3. Attach `AV-Standard`, `IPS-Standard`, `WebFilter-Standard`,
   `AppCtrl-Standard`, and `Certificate-Inspection` to the
   `LAN-to-WAN-Outbound` policy from [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md), with `logtraffic all`
   enabled.

4. From the LAN test client, attempt to download the EICAR test file over
   HTTP.

   **Expected result:** The download is blocked and a FortiGuard block
   page (or connection reset) is returned; confirm the corresponding log
   entry shows `AV-Standard` as the blocking profile.

5. Attempt to browse to a site in a category configured for blocking in
   `WebFilter-Standard` (a FortiGuard test/demo category page is
   appropriate for this validation).

   **Expected result:** A FortiGuard category block page is displayed;
   confirm the log entry shows the matched category.

6. Switch the policy's `ssl-ssh-profile` to `Full-Deep-Inspection`, and
   without installing the FortiGate's CA certificate on the test client
   yet, attempt to browse to any HTTPS site.

   **Expected result:** The browser reports a certificate trust
   error/warning, demonstrating the trust-distribution requirement
   described in Theory and Architecture.

7. Export the FortiGate's deep-inspection CA certificate
   (**System > Certificates**, or `execute vpn certificate ca export`) and
   install it in the test client's trusted root certificate store.

8. Re-attempt HTTPS browsing.

   **Expected result:** The certificate warning no longer appears, and
   AV/IPS logs now show visibility into HTTPS-delivered content that
   `Certificate-Inspection` could not previously inspect.

9. **Negative test:** Add a filter entry to `WebFilter-Standard`
   explicitly allowing (rather than blocking) the previously blocked test
   category, apply the change, and re-attempt step 5's browse test.

   **Expected result:** The site is now reachable, confirming the
   override took effect and demonstrating the exception mechanism
   referenced in Design Considerations. Revert the override afterward.

**Cleanup**

- Revert the `LAN-to-WAN-Outbound` policy's `ssl-ssh-profile` back to
  `Certificate-Inspection` to avoid breaking other labs (notably
  [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)'s SSL VPN and [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)'s SD-WAN and REST API examples,
  which do not require deep inspection and should not incur its
  performance cost by default).
- Remove the temporary web filter override added in step 9 if not already
  reverted.
- Optionally uninstall the FortiGate CA certificate from the test
  client if it will not be used again in later chapters.

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
