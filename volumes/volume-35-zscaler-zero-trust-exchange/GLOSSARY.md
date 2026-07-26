# Volume XXXV Glossary

Definitions for terms introduced in **Volume XXXV — Zscaler Zero Trust
Exchange**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

- **App Connector** — A lightweight ZPA software connector deployed beside
  private applications that makes only outbound connections to the ZPA
  service edge, so the application has no inbound attack surface.
- **AppProtection** — ZPA inline inspection (an OWASP-style ruleset) applied
  to private-application traffic to catch web attacks a plain tunnel would
  pass.
- **Application segment** — The ZPA definition of an application: its
  FQDNs/IPs and ports, bound to a server group and referenced by access
  policy.
- **CASB (Cloud Access Security Broker)** — Control of SaaS usage; *inline*
  CASB governs SaaS as users access it (tenant restriction, activity
  control), while *out-of-band* CASB scans SaaS data at rest via API.
- **Cloud Browser Isolation (CBI)** — Rendering a site in a remote,
  disposable browser and streaming only pixels, with upload/download/copy/
  paste optionally disabled, to preserve access while removing the data path.
- **Cloud Path** — A ZDX hop-by-hop path trace (latency and loss per hop)
  from the endpoint to the application, used to localize a problem to the
  network.
- **Cloud Sandbox** — The ZIA engine that detonates unknown files in
  isolation and scores their behavior; with patient-zero blocking it holds a
  file until a verdict is returned so even the first user is protected.
- **DLP dictionary / engine** — A dictionary defines what sensitive content
  to match (patterns, keywords, exact data); an engine combines dictionaries
  with logic and thresholds for precision; a rule binds an engine to an
  action.
- **DNS Control** — ZIA policy governing name resolution — blocking or
  redirecting domain categories, enforcing a resolver, and detecting DNS
  tunneling — the earliest chokepoint against threats.
- **EICAR** — The industry-standard harmless antivirus test file, used to
  confirm malware protection without real malware.
- **Forwarding profile / app profile** — Zscaler Client Connector settings
  that decide, per network and per application, whether traffic goes to ZIA,
  to ZPA, or DIRECT.
- **PAC file** — A proxy auto-config script whose `FindProxyForURL(url,
  host)` function returns, per request, the proxy to use (Zscaler) or
  `DIRECT`.
- **Patient-zero blocking** — A sandbox posture that holds an unknown file
  until a verdict is returned, protecting even the first user to request it.
- **Posture profile** — A set of device checks (encryption, EDR, OS version,
  certificate) used as a condition in ZPA access policy so access depends on
  device trustworthiness.
- **Privileged Remote Access (PRA)** — Browser-based, agentless RDP/SSH/VNC to
  named systems for third parties and OT, with session recording and
  credential injection, and no network access.
- **SAML** — The protocol by which Zscaler (service provider) federates
  authentication to an identity provider, which returns a signed assertion
  carrying identity and group attributes.
- **SCIM** — The protocol that synchronizes users and groups from the
  identity provider into Zscaler, keeping the directory authoritative and
  deprovisioning leavers.
- **Secure Web Gateway (SWG)** — The ZIA cloud forward proxy that terminates,
  inspects, and re-originates internet/SaaS sessions to enforce URL and
  content policy.
- **Server group** — The set of ZPA App Connectors that can reach a given
  application.
- **SSL/TLS inspection** — ZIA's policy-based man-in-the-middle that decrypts,
  inspects, and re-encrypts TLS traffic; it requires the Zscaler
  root/intermediate certificate to be trusted on the endpoint.
- **Z-Tunnel 1.0 / 2.0** — Client Connector tunnel modes: 1.0 forwards web
  ports (80/443) to ZIA; 2.0 forwards all ports and protocols, required for
  the full cloud firewall.
- **ZDX Score** — A 0–100 measure of user experience blending device health,
  Cloud Path network metrics, and web/application probes.
- **Zero Trust Exchange (ZTE)** — Zscaler's cloud-delivered Security Service
  Edge that brokers every connection inline and grants per-session access to
  an application rather than to a network.
- **ZIA (Zscaler Internet Access)** — The Zero Trust Exchange pillar securing
  access to the internet and SaaS.
- **ZPA (Zscaler Private Access)** — The pillar providing VPN-less zero-trust
  access to private applications via outbound-only App Connectors.
- **ZCC (Zscaler Client Connector)** — The endpoint agent that enrolls the
  device and forwards user traffic to ZIA and ZPA.
- **ZDX (Zscaler Digital Experience)** — The pillar that monitors end-to-end
  user experience across device, network, and application.
