# Chapter 01: Security Concepts, the Threat Landscape, and the CCNP Security Track

## Learning Objectives

- Describe the CCNP Security track structure and where the SCOR core and
  each concentration fit.
- Explain the security concepts SCOR treats as foundational: the threat
  landscape, common attack methods, and the defensive model that answers
  them.
- Apply cryptography and PKI fundamentals to the decisions later chapters
  make about VPNs, TLS inspection, and identity.
- Situate Cisco's security portfolio against the vendor-neutral security
  material in Volume X, without re-learning it.
- Read the SCOR blueprint — including its 2026 v1.1-to-v2.0 change — well
  enough to plan study against the correct edition.

## Theory and Architecture

### The CCNP Security track, and why SCOR comes first

CCNP Security is earned by passing two exams: the **SCOR core**
(`350-701`) and **one concentration**. This volume covers the core and
four concentrations — SVPN, SCAZT, SISE, and SDSI — but the structure
matters before the content does, because it determines the order of
study.

SCOR is first for three reasons. It is required regardless of
concentration, so no path avoids it. It is the broadest of the exams,
spanning network, cloud, endpoint, and access security, so it establishes
the vocabulary every concentration assumes. And it is simultaneously the
**CCIE Security qualifying exam**, so the effort compounds toward the
expert track for anyone continuing.

The concentrations then go deep on one slice: VPNs (SVPN), zero-trust
cloud access (SCAZT), the Identity Services Engine (SISE), or security
design (SDSI). [Chapter 09](09-designing-security-infrastructure-automation-and-capstone.md)'s
capstone composes them back together, which is closer to how the role
actually works than any single exam suggests.

### What "security concepts" means on this exam

SCOR's Security Concepts domain is not a soft introduction. It is the
domain that makes the rest coherent, and it carries **20% of SCOR v2.0**
(down from 25% in v1.1). It covers the threat landscape, common attack
methods, security intelligence, and the cryptographic and PKI foundations
that VPNs and TLS inspection later depend on.

**The threat landscape as the exam frames it.** The role this certifies
is defending an enterprise against a set of attack classes it expects you
to recognize on sight: reconnaissance and scanning; denial of service and
distributed denial of service; man-in-the-middle and on-path attacks;
malware families (viruses, worms, trojans, ransomware); social
engineering and phishing; and the exploitation of specific protocol
weaknesses — DNS, DHCP, ARP, and the routing protocols Volume III covers.
The point is not to memorize a taxonomy but to connect each attack to the
control that answers it, which is the through-line of the whole volume.

**The defensive model.** Cisco frames its portfolio around defense in
depth applied to a specific set of enforcement points: the network edge
and internal segments (firewalls, IPS — [Chapter 02](02-network-security-with-cisco-secure-firewall-and-ips.md)),
the cloud and the service edge ([Chapter 03](03-cloud-security-and-the-secure-service-edge.md)),
the endpoint ([Chapter 04](04-content-security-and-endpoint-protection.md)),
and network access itself ([Chapters 05](05-secure-network-access-visibility-and-enforcement.md)
and [06](06-identity-services-engine-deployment-policy-and-services.md)).
Each later chapter is one enforcement point; this chapter is the model
that says why there are several.

### Cryptography and PKI, only as far as the role needs

SCOR expects working fluency with cryptography, not a course in it. The
examinable core:

- **Symmetric versus asymmetric encryption**, and why real systems use
  both — asymmetric to exchange a key, symmetric to move the data.
- **Hashing and message authentication** (SHA-2 family, HMAC) for
  integrity, distinct from encryption for confidentiality.
- **Digital signatures** and the certificate chain of trust: a
  certificate authority, intermediate CAs, and the leaf certificate an
  endpoint presents.
- **PKI mechanics** an operator meets daily: certificate signing
  requests, validity and revocation (CRL and OCSP), and what a trust
  store is.

This is the foundation [Chapter 07](07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md)'s
IPsec and the TLS inspection in [Chapters 03](03-cloud-security-and-the-secure-service-edge.md)
and [04](04-content-security-and-endpoint-protection.md) build directly
on. Volume X covers the same material vendor-neutrally and in more depth;
this chapter assumes it and names the parts SCOR tests.

### Where this volume sits against Volume X

[Volume X — Enterprise Cybersecurity](../../volume-10-enterprise-cybersecurity/README.md)
teaches security architecture, threat modeling, cryptography, and
operations without reference to any one vendor. This volume specializes
that to Cisco's products. The division is deliberate and worth stating so
neither is over-read:

- **Concepts, threat models, and cryptographic theory** — Volume X. This
  volume assumes them.
- **Cisco product architecture, configuration, and the exam blueprints**
  — here.

A reader strong in general security but new to Cisco should skim this
chapter and spend time on Chapters 02 onward. A reader new to security
should work Volume X first; SCOR assumes the concepts this chapter only
summarizes.

### The SCOR blueprint, and the 2026 edition change

SCOR is mid-transition, and studying the wrong edition is a real risk
right now. **v1.1 is testable through 26 August 2026; v2.0 begins 27
August 2026.** The volume README carries the full weights; the change that
matters for this chapter is that v2.0 lowered Security Concepts from 25%
to 20%, added a Secure Service Edge domain, and removed Content Security
as a standalone domain.

Because SCOR preparation runs eight to ten weeks, anyone starting now
finishes after the cutoff and should prepare for **v2.0**. This volume
targets v2.0 and flags v1.1 differences where they matter.

## Design Considerations

- **Choose the concentration before you finish SCOR, not after.** The
  concentration shapes how you weight SCOR's later domains — a future
  SISE candidate should go deeper on access and identity, a future SVPN
  candidate on secure communications. Deciding early makes SCOR study do
  double duty.
- **Map every attack to a control as you learn it.** The exam rewards the
  connection, not the list. A reconnaissance scan maps to firewall and
  IPS visibility; ARP spoofing to dynamic ARP inspection; a phishing
  payload to endpoint and content security. Learn them paired.
- **Treat PKI as operational, not theoretical.** Every certificate
  problem later in the volume — an expired VPN certificate, a failed TLS
  decryption, an ISE portal warning — is a PKI problem. Time spent here is
  repaid across five chapters.
- **Do not let the portfolio's size drive the study order.** Cisco's
  security product line is large. The blueprint weights, not the catalog,
  determine where time goes.

## Implementation and Automation

This chapter is conceptual; its "implementation" is establishing a lab
account and confirming the tools later chapters need. The security-stack
automation SCOR tests is developed in
[Chapter 09](09-designing-security-infrastructure-automation-and-capstone.md);
what belongs here is the habit of treating security state as inspectable.

### 1. Confirming a certificate chain from the command line

Every VPN and TLS-inspection chapter depends on reading a certificate
chain. Establish the habit against any HTTPS service:

```bash
# Show the full presented chain: leaf, intermediates, and issuer names.
openssl s_client -connect example.com:443 -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -issuer -subject -dates

# Inspect a local certificate's validity and purpose before deploying it.
openssl x509 -in device.pem -noout -text | grep -A2 "Validity\|Key Usage"
```

The `Validity` window and the issuer chain are the two things a broken VPN
or a failed decryption most often comes down to. Reading them fluently is
a SCOR-level skill.

### 2. Recording an attack-to-control map as a study artifact

Rather than a flat list, build the mapping the exam actually tests:

```text
# threat-control-map.txt — extend as each chapter adds a control
Reconnaissance / scanning     -> firewall policy + IPS signatures (Ch 02)
ARP spoofing / on-path        -> Dynamic ARP Inspection, DHCP snooping (Ch 05)
Malware delivery (web/email)  -> content security + Secure Endpoint (Ch 04)
Phishing / credential theft   -> MFA, ISE posture, DNS-layer (Ch 03, 06)
Data exfiltration to cloud    -> CASB / secure service edge (Ch 03, 08)
Lateral movement              -> segmentation, TrustSec, ISE (Ch 05, 06)
```

## Validation and Troubleshooting

Validation here means confirming your own readiness rather than a system's
state.

- **Can you name the control for an arbitrary attack?** Pick any row of
  the map above from memory and state the Cisco control and the chapter.
  If you cannot, that chapter is where your study needs to go.
- **Can you read a certificate chain without notes?** Issuer, subject,
  validity, and whether the chain is complete. This is a prerequisite for
  Chapters 03, 04, and 07, not an optional extra.
- **Do you know which SCOR edition you are sitting?** If the answer is not
  immediate and specific, resolve it before building a study schedule —
  the v1.1/v2.0 domains differ enough to waste weeks.

**A common early misconception.** Candidates from a routing-and-switching
background often treat security as a set of features bolted onto the
network they already know. SCOR treats it as a discipline with its own
threat model and its own enforcement architecture. The features are real,
but the exam tests whether you can reason about *why* a control exists,
not only how to configure it.

## Security and Best Practices

- **Least privilege is the organizing principle, not a feature.** Every
  later chapter — firewall policy, ISE authorization, VPN split tunneling,
  cloud access — is an application of it. Adopt it as the default lens.
- **Assume breach.** Cisco's zero-trust and secure-service-edge direction
  (Chapters 03 and 08) rests on not trusting the network perimeter.
  Carrying that assumption from the start makes those chapters follow
  naturally rather than arriving as a reversal.
- **Protect the security control plane itself.** ISE, FMC, and VPN
  headends are tier-0 systems; compromising the thing that enforces
  security defeats everything it enforces. This theme recurs in every
  management-plane discussion in the volume.
- **Keep cryptographic choices current.** Deprecated ciphers and hashes
  are exam material and production risk alike; the strong-by-default
  posture SCOR expects is the one to build habits around.

## References and Knowledge Checks

**References**

- [Cisco 350-701 SCOR exam topics](https://learningnetwork.cisco.com/s/scor-exam-topics)
  — the controlling source for the current and incoming editions.
- [Volume X — Enterprise Cybersecurity](../../volume-10-enterprise-cybersecurity/README.md)
  — the vendor-neutral concepts, threat models, and cryptography this
  chapter assumes.
- [Volume III — Cisco Enterprise Networking](../../volume-03-cisco-enterprise-networking/README.md)
  — the routing and switching foundation the security controls sit on.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  — the full CCNP Security blueprint set with verified weights.

**Knowledge checks**

1. State the two exams required for CCNP Security and explain why SCOR is
   taken first.
2. Give three attack classes SCOR expects you to recognize and the Cisco
   control that answers each.
3. Explain why real systems combine symmetric and asymmetric encryption
   rather than choosing one.
4. What changed in the SCOR blueprint between v1.1 and v2.0, and which
   edition should someone starting today prepare for?
5. Where is the boundary between this volume and Volume X, and which
   should a reader new to security work first?

## Hands-On Lab

**Objective:** Build the study infrastructure the rest of the volume
assumes — a Cisco lab account, a certificate-reading workflow, and a
living attack-to-control map — and confirm you are targeting the correct
SCOR edition.

**Prerequisites:** A computer with `openssl`, internet access, and a free
[Cisco account](https://id.cisco.com/) for dCloud and the Learning
Network.

**This lab requires no licensed Cisco products.** It establishes the
scaffolding; the product-specific labs begin in Chapter 02.

**Procedure**

1. Create or confirm a Cisco account and log in to the Cisco Learning
   Network. Locate the 350-701 SCOR exam-topics page and confirm the
   current edition and its last testable date.
2. Compute your own timeline: from today, add ten weeks. If that date is
   after the v1.1 cutoff, record "target: v2.0" at the top of your study
   notes.
3. Run the `openssl s_client` chain inspection against three different
   HTTPS sites. For each, write down the issuer, the leaf subject, and the
   validity window.
4. Build `threat-control-map.txt` from the template above. For every row,
   confirm you can state the control from memory before reading the
   chapter that covers it.
5. Browse the Cisco dCloud catalog and note which Secure Firewall and ISE
   demonstrations are available to your account — Chapters 02 and 06 will
   use them.

**Negative test**

6. Inspect a certificate chain for a site using a certificate that is
   expired or self-signed (many lab appliances present one). Observe how
   the tooling reports the failure — an expired or untrusted leaf is the
   single most common cause of the VPN and decryption failures in later
   chapters, and recognizing it here saves hours there.

**Expected results**

- A study timeline that names the correct SCOR edition.
- Fluency reading a certificate chain, demonstrated on three sites.
- A completed attack-to-control map you can recite.
- A confirmed dCloud catalog for the labs ahead.

**Cleanup**

7. This lab produces notes and an account, not infrastructure; retain
   both. The map and timeline are inputs to every subsequent chapter.

## Summary and Completion Checklist

CCNP Security is SCOR plus one concentration, and SCOR comes first because
it is required, broadest, and doubles as the CCIE Security qualifier. Its
Security Concepts domain is the connective tissue of the whole track: the
threat landscape paired to the controls that answer it, and the
cryptography and PKI foundation that VPNs, TLS inspection, and identity
all rest on. This volume specializes Volume X's vendor-neutral security to
Cisco's portfolio rather than repeating it, and it targets SCOR v2.0
because the August 2026 transition puts anyone starting now on that
edition.

- [ ] Can describe the CCNP Security track and SCOR's role in it.
- [ ] Can pair common attack classes with their Cisco controls.
- [ ] Can read a certificate chain and explain symmetric/asymmetric use.
- [ ] Knows the v1.1-to-v2.0 SCOR change and which edition to target.
- [ ] Has a study timeline, a dCloud account, and an attack-to-control
      map in hand.
