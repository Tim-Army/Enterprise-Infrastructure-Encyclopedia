# Volume X Glossary

Definitions for terms introduced in **Volume X — Enterprise
Cybersecurity**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**3-2-1-1-0 backup rule** — A ransomware-resilience extension of the
traditional 3-2-1 backup rule: three copies of data, on two different
media types, with one copy offsite, plus one immutable or air-gapped
copy, and zero verified recovery errors from tested restores. Introduced
in Chapter 08.

**Alert fatigue** — The degradation in analyst detection accuracy caused
by a high volume of low-value or false-positive alerts, which measurably
increases the chance a genuine positive is missed among the noise.
Introduced in Chapter 06.

**AppArmor** — A Linux mandatory access control system, default on
Ubuntu and Debian-family distributions, that constrains process behavior
using path-based profiles rather than SELinux's label-based type
enforcement. Introduced in Chapter 03.

**Application allow-listing** — A control that inverts the default
execution posture from "block known-bad" to "permit only known-good,"
blocking any binary or script not explicitly authorized, used to defeat
living-off-the-land (LOLBin) abuse. Introduced in Chapter 03.

**Attack surface management (ASM)** — Continuous, outside-in discovery
of an organization's internet-facing assets, including unmanaged and
shadow IT assets never formally inventoried. Introduced in Chapter 05.

**Break-glass account** — A small number of emergency, offline-stored
privileged accounts used only when the identity provider or PAM system
itself is unavailable, whose use should trigger mandatory post-incident
review. Introduced in Chapter 02.

**Breach and Attack Simulation (BAS)** — Scheduled, safe, non-destructive
simulation of specific adversary techniques against production-
representative environments, used to verify that an expected detection
or prevention control actually fires. Introduced in Chapter 09.

**Chain of custody** — A documented, unbroken record of who collected a
piece of digital evidence, when, how, and who has held or accessed it
since, with a cryptographic hash recorded at each handoff to prove
integrity. Introduced in Chapter 07.

**CIS Benchmarks** — Consensus-developed, vendor-agnostic hardening
baselines published by the Center for Internet Security, each defining
Level 1 (broadly applicable) and Level 2 (defense-in-depth) profiles.
Introduced in Chapter 03.

**CISA Known Exploited Vulnerabilities (KEV) catalog** — An
authoritative, continuously updated list of vulnerabilities with
confirmed, active real-world exploitation, used as a high-priority
remediation signal. Introduced in Chapter 05.

**Conditional access** — An identity policy engine capability that
evaluates signals (device compliance, network location, sign-in risk) at
authentication time and enforces a graduated response: allow, step-up
MFA, require a compliant device, or block. Introduced in Chapter 02.

**Configuration drift** — The gradual divergence of a system's running
configuration from its documented hardening baseline, caused by ad hoc
changes, patches, or temporary troubleshooting exceptions left in place.
Introduced in Chapter 03.

**Continuous control validation** — Scheduled, automated checks run
against production or production-representative systems to confirm a
security control is actually functioning as designed, not merely
configured. Introduced in Chapter 09.

**Continuous Threat Exposure Management (CTEM)** — A five-stage program
model (scoping, discovery, prioritization, validation, mobilization) that
generalizes vulnerability management to cover misconfigurations, exposed
secrets, and identity exposures alongside CVE-numbered flaws. Introduced
in Chapter 05.

**Control crosswalk** — A table mapping one control catalog's control IDs
to another's, so a single technical control can satisfy multiple
compliance frameworks from one piece of audit evidence. Introduced in
Chapter 01.

**CVSS (Common Vulnerability Scoring System)** — A standardized 0–10
scoring system for a vulnerability's technical severity, currently at
version 4.0, based on attack vector, complexity, and required privileges.
Introduced in Chapter 05.

**Data classification** — The assignment of a sensitivity tier (public,
internal, confidential, restricted/regulated) to data at creation time,
used to drive encryption, access, DLP, and retention controls
programmatically. Introduced in Chapter 08.

**Data Encryption Key (DEK)** — A unique symmetric key that encrypts the
actual bulk data in an envelope-encryption scheme, itself wrapped by a
key encryption key (KEK) rather than stored in plaintext. Introduced in
Chapter 08.

**Data Loss Prevention (DLP)** — Controls that inspect data in motion,
at rest, and in use for classification-matching content, enforcing
policy (block, quarantine, alert, encrypt) on unauthorized movement.
Introduced in Chapter 08.

**Data Subject Request (DSR)** — A request from an individual, under
regulations such as GDPR or CCPA/CPRA, to access, correct, or delete
their personal data, requiring the organization to locate every copy of
that data across its systems. Introduced in Chapter 08.

**DDoS protection** — Controls distinguishing volumetric attacks
(mitigated by upstream scrubbing and anycast distribution) from
application-layer attacks (mitigated by rate limiting and bot
management). Introduced in Chapter 04.

**Detection engineering** — The discipline of treating detection logic
as version-controlled, tested, and peer-reviewed software, following a
lifecycle from hypothesis through deployment and retirement. Introduced
in Chapter 06.

**DevSecOps** — The practice of distributing security checks (SAST, SCA,
DAST, infrastructure-as-code scanning, container image scanning) across
the CI/CD pipeline rather than gating security review to the end of the
delivery lifecycle. Introduced in Chapter 09.

**DISA STIGs (Security Technical Implementation Guides)** — Mandatory
hardening baselines for U.S. Department of Defense systems, generally
more prescriptive than CIS Level 1, distributed with machine-readable
SCAP content. Introduced in Chapter 03.

**Endpoint Detection and Response (EDR)** — A platform that instruments
the operating system kernel and monitors behavioral telemetry (process
trees, command-line arguments, network connections), correlating it
against behavioral detection logic rather than relying on signature
matching alone. Introduced in Chapter 03.

**Envelope encryption** — The standard pattern for encrypting data at
rest at scale: a data encryption key (DEK) encrypts the data, and the DEK
is itself wrapped by a key encryption key (KEK) held in a centralized
KMS/HSM, allowing key rotation without bulk data re-encryption.
Introduced in Chapter 08.

**EPSS (Exploit Prediction Scoring System)** — A FIRST.org-maintained
score estimating the probability a vulnerability will be exploited in the
wild within the next 30 days, used alongside CVSS to prioritize
remediation by actual risk rather than severity alone. Introduced in
Chapter 05.

**FAIR (Factor Analysis of Information Risk)** — A quantitative risk
model that produces a probabilistic loss-exposure range in dollars,
generally reserved for top-tier risks reaching the board given its
higher data and analyst-training requirements. Introduced in Chapter 01.

**FIDO2/WebAuthn** — A phishing-resistant authentication standard using
hardware security keys or platform authenticators (passkeys) that bind
the credential to the origin, defeating adversary-in-the-middle phishing
proxies. Introduced in Chapter 02.

**Hardware Security Module (HSM)** — A dedicated, tamper-resistant
hardware device that generates and holds cryptographic keys, performing
operations inside the device boundary so private key material is never
exposed in plaintext. Introduced in Chapter 08.

**Hunting Maturity Model (HMM)** — A self-assessment scale (HMM0 through
HMM4) describing a threat hunting program's maturity, from purely
reactive to substantially automated with hunt techniques continuously
converted into permanent detections. Introduced in Chapter 09.

**Just-in-time (JIT) elevation** — A privileged access pattern that
grants administrative rights for a bounded time window after an approval
workflow, then automatically revokes them, replacing standing
administrative access. Introduced in Chapter 02.

**Key Encryption Key (KEK)** — The key held in a centralized KMS/HSM
that wraps (encrypts) data encryption keys in an envelope-encryption
scheme; the KEK itself never leaves the key management boundary.
Introduced in Chapter 08.

**Key Management Service (KMS)** — A managed service providing
centralized cryptographic key generation, wrapping, rotation, and audit
logging, commonly backed by an HSM at the provider layer. Introduced in
Chapter 08.

**LOLBin (living-off-the-land binary)** — A legitimate, pre-installed
system utility (scripting interpreter, archive tool, remote management
tool) abused by an adversary to execute malicious actions without
introducing a detectable malware file. Introduced in Chapter 03.

**Mandatory access control (MAC)** — An access control model enforcing a
system-wide policy that even a compromised or misconfigured process
running as an authorized user cannot override, implemented on Linux by
SELinux and AppArmor. Introduced in Chapter 03.

**Microsegmentation** — Network policy enforcement between individual
workloads or small workload groups, independent of network topology,
limiting east-west lateral movement after an initial compromise.
Introduced in Chapter 04.

**MITRE ATT&CK** — A catalog of adversary tactics and techniques built
from observed real-world intrusions, used defensively in this volume as
a coverage-mapping and gap-analysis tool for detection engineering and
architecture review. Introduced in Chapter 01; expanded in Chapter 06.

**NIST Cybersecurity Framework (CSF) 2.0** — A six-function model
(Govern, Identify, Protect, Detect, Respond, Recover) for structuring a
security program, with Govern added as a first-class function in the
2024 revision. Introduced in Chapter 01.

**NIST SP 800-61** — The NIST Incident Handling Guide, defining the
four-phase incident response lifecycle: Preparation; Detection and
Analysis; Containment, Eradication, and Recovery; and Post-Incident
Activity. Introduced in Chapter 07.

**NIST SP 800-207** — The NIST publication defining Zero Trust
Architecture (ZTA), including the Policy Engine, Policy Administrator,
and Policy Enforcement Point (PE/PA/PEP) model. Introduced in Chapter 02.

**Next-generation firewall (NGFW)** — A firewall extending stateful
packet inspection with application awareness, user/identity awareness,
and integrated intrusion prevention. Introduced in Chapter 04.

**Order of volatility** — The digital forensics principle of collecting
evidence from most to least volatile (registers/cache, RAM, network
state, running processes, disk, archival media), since later collection
steps can destroy earlier volatile evidence. Introduced in Chapter 07.

**Policy Enforcement Point (PEP)** — The gateway (identity-aware proxy,
NGFW, ZTNA broker, service mesh sidecar) that permits, monitors, and
terminates connections based on a decision from the Policy Engine, per
the NIST SP 800-207 model. Introduced in Chapter 02.

**Privileged Access Management (PAM)** — The discipline and platform
category for controlling standing, just-in-time, and break-glass access
to privileged accounts, typically brokering sessions so the human
operator never sees the privileged credential. Introduced in Chapter 02.

**Public Key Infrastructure (PKI)** — The trust hierarchy of root and
intermediate certificate authorities and issued end-entity certificates
that binds a public key to a verified identity, underlying TLS and
certificate-based authentication. Introduced in Chapter 08.

**Purple teaming** — A collaborative exercise where an offensive-minded
team and the defensive SOC work together in real time to test and
immediately improve detection and response, in contrast to a blind
penetration test. Introduced in Chapter 09.

**Ransomware kill chain** — The typical progression of a ransomware
incident from initial access through lateral movement, data
exfiltration, encryption/detonation, and extortion, used as a defensive
planning framework for mapping which controls interrupt each stage.
Introduced in Chapter 08.

**Risk register** — A structured (not free-text) inventory of identified
risks, their likelihood and impact scores, mapped controls, residual
score, named owner, and review date, maintained as a living governance
artifact. Introduced in Chapter 01.

**SASE (Secure Access Service Edge)** — The convergence of SD-WAN
networking with a cloud-delivered security stack (secure web gateway,
CASB, ZTNA, firewall-as-a-service) enforced close to the user rather than
backhauled through a data center. Introduced in Chapter 04.

**SBOM (Software Bill of Materials)** — A structured, machine-readable
inventory of every direct and transitive component in a piece of
software, typically in SPDX or CycloneDX format, used to rapidly assess
software-supply-chain exposure. Introduced in Chapter 05.

**Security architecture review board (SARB)** — A recurring,
cross-functional gate that evaluates proposed system designs against
STRIDE threat modeling and architecture principles before a change
reaches production. Introduced in Chapter 01.

**Security Orchestration, Automation, and Response (SOAR)** — A platform
that automates repetitive alert-triage actions (enrichment, standard
containment, case creation) so analyst time concentrates on judgment
calls, typically with human-approval gates for high-impact actions.
Introduced in Chapter 06.

**SELinux** — A Linux mandatory access control system, default on
RHEL-family distributions, that labels every process and object with a
security context and enforces policy through type enforcement.
Introduced in Chapter 03.

**Sigma** — A vendor-neutral, structured detection rule format that
converts to a specific SIEM's native query language, keeping detection
content portable across platforms. Introduced in Chapter 06.

**Software Composition Analysis (SCA)** — A CI/CD pipeline check that
scans third-party and open-source dependencies against known-
vulnerability databases, directly consuming SBOM data. Introduced in
Chapter 09.

**Staged patch rollout ring** — A phased deployment sequence (canary,
broader validation, production-wide) with a bake-in period between rings,
so a patch-induced regression is caught on a small fraction of the fleet.
Introduced in Chapter 05.

**STRIDE** — A threat modeling framework (Spoofing, Tampering,
Repudiation, Information disclosure, Denial of service, Elevation of
privilege) used to systematically review an architecture diagram for
design weaknesses before implementation. Introduced in Chapter 01.

**Tabletop exercise** — A discussion-based walkthrough of a realistic
incident scenario used to validate an incident response plan, playbooks,
and team decision-making before a real incident tests them instead.
Introduced in Chapter 07.

**Three lines of defense** — An organizational governance model
separating operational control ownership (first line), risk and policy
functions (second line), and independent audit (third line), preserving
audit independence architecturally. Introduced in Chapter 01.

**UEBA (User and Entity Behavior Analytics)** — A detection method that
builds a statistical baseline of normal behavior per user or entity and
flags deviations, complementary to rule-based detection for insider
threats and slow, low-and-slow compromise. Introduced in Chapter 06.

**Virtual patching** — A compensating control (WAF or IPS rule blocking
a specific exploitation pattern) applied while a real patch is pending,
which must carry an expiration date tied to actual patch deployment.
Introduced in Chapter 05.

**Zero Trust Architecture (ZTA)** — The NIST SP 800-207 principle that no
implicit trust is granted based on network location or asset ownership;
every access request is evaluated using least privilege, based on
identity, device posture, and context. Introduced in Chapter 02.

**Zero Trust Network Access (ZTNA)** — A remote-access model that
replaces network-level trust (as granted by traditional VPN) with
per-application, identity- and posture-verified access brokered by a
proxy, never placing the client device on the internal network.
Introduced in Chapter 04.
