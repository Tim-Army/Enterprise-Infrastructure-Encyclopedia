# Volume XXV Glossary

Definitions for terms introduced in **Volume XXV — Cisco Security**,
alphabetized. See also the [volume index](INDEX.md) for pointers back to
the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**802.1X** — A port-based network access control standard that
authenticates a device or user before granting network access, using the
supplicant, authenticator, and authentication-server roles. Introduced in
Chapter 05.

**ASA (Adaptive Security Appliance)** — Cisco's long-established stateful
firewall operating system, strong at filtering, NAT, and VPN termination.
Contrast *FTD*. Introduced in Chapter 02.

**Authorization (vs. authentication)** — In an ISE policy set, the stage
that decides *what* an established identity may do, returning a permit,
VLAN, ACL, or security group tag — distinct from authentication, which
establishes *who* the identity is. Most access problems are authorization,
not authentication. Introduced in Chapter 06.

**BYOD (bring your own device)** — Securely onboarding personal devices,
typically by provisioning a certificate so the device can perform
certificate-based 802.1X. Introduced in Chapter 06.

**Child SA** — In IKEv2, the security association negotiated within the
IKE SA that actually protects data traffic; its failure is a phase-2
problem, commonly a transform or proxy-identity mismatch. Introduced in
Chapter 07.

**DMVPN (Dynamic Multipoint VPN)** — A hub-and-spoke VPN architecture in
which spokes build on-demand tunnels directly to each other, scaling a
mesh without configuring one. Introduced in Chapter 07.

**DNS-layer security** — Blocking malicious destinations at name
resolution, before a connection is attempted; the distinctive early
control in Cisco Umbrella. Introduced in Chapter 03.

**EDR (endpoint detection and response)** — Endpoint security that detects
threats by behavior rather than signature, catching novel malware by what
it does. Contrast signature antivirus. Introduced in Chapter 04.

**FlexVPN** — A unified, IKEv2-based VPN framework covering site-to-site,
hub-and-spoke, and remote access under one configuration model; Cisco's
strategic VPN direction. Introduced in Chapter 07.

**FTD (Firepower Threat Defense)** — Cisco's next-generation firewall
platform, unifying stateful firewalling with Snort IPS, application
visibility, and URL filtering, managed by FMC or FDM. Introduced in
Chapter 02.

**IKEv2 (Internet Key Exchange version 2)** — The protocol two IPsec peers
use to authenticate and negotiate the security associations that protect a
tunnel. Introduced in Chapter 07.

**ISE (Identity Services Engine)** — Cisco's identity and access-control
platform: the authentication server for 802.1X, the policy engine for
network access, and the subject of the SISE concentration. Introduced in
Chapter 06.

**MAB (MAC Authentication Bypass)** — Authenticating a device by its MAC
address when it cannot perform 802.1X; weak on its own and corroborated by
profiling. Introduced in Chapter 05.

**Order of operations** — On FTD, the fixed sequence — prefilter, access
control, NAT, intrusion inspection — in which a packet is evaluated;
knowing it determines firewall troubleshooting method. Introduced in
Chapter 02.

**Persona (ISE)** — A role an ISE node performs: Policy Administration
(PAN), Policy Service (PSN), Monitoring (MnT), or pxGrid. A deployment
distributes personas for scale and resilience. Introduced in Chapter 06.

**Policy set (ISE)** — The two-stage rule structure — authentication then
authorization — through which ISE evaluates network access; SISE's
largest domain. Introduced in Chapter 06.

**Profiling** — ISE's identification of what a device *is* from its
observed attributes, without asking it, corroborating MAB. Introduced in
Chapter 06.

**Retrospection** — Secure Endpoint's ability to identify every endpoint
that received a file after that file's verdict changes to malicious;
impossible for signature antivirus. Introduced in Chapter 04.

**Route-based VPN (VTI)** — A site-to-site VPN where the tunnel is a
routable interface and normal routing decides what it carries; the modern
default, avoiding the proxy-ID failures of policy-based VPNs. Introduced in
Chapter 07.

**SASE (secure access service edge)** — The convergence of networking
(SD-WAN) and security (SSE) into a single cloud-delivered service.
Introduced in Chapter 03.

**SCOR** — The `350-701` core exam of the CCNP Security track (and CCIE
Security qualifier), covering security concepts, network, cloud, endpoint,
and access security. Its v1.1 edition tests through 26 August 2026 and
v2.0 from 27 August 2026. Introduced in Chapter 01.

**Secure service edge (SSE)** — The security half of SASE: secure web
gateway, CASB, ZTNA, and cloud firewall delivered from the cloud rather
than an appliance. A new SCOR v2.0 domain. Introduced in Chapter 03.

**Security Group Tag (SGT)** — In Cisco TrustSec, an identity-based label
assigned at authentication and used to write segmentation policy between
groups rather than between subnets. Introduced in Chapter 05.

**Shared-responsibility model** — The division of security duties between
a cloud provider and its customer, which shifts with the IaaS/PaaS/SaaS
service model. Introduced in Chapter 03.

**TACACS+** — The protocol ISE uses for device administration —
controlling who may log in to network devices and what commands they may
run — as opposed to RADIUS for network access. Introduced in Chapter 06.

**TrustSec** — Cisco's identity-based segmentation technology, using
security group tags so policy follows identity rather than network
location. Introduced in Chapter 05.

**Zero trust** — A security model that discards perimeter trust,
verifying every access request explicitly on identity, device health, and
context regardless of origin. Introduced in Chapter 08.

**ZTNA (zero-trust network access)** — Zero trust applied to reaching
applications: connecting a verified user to a single authorized
application rather than placing them on a network; the successor to
remote-access VPN for application access. Introduced in Chapter 08.
