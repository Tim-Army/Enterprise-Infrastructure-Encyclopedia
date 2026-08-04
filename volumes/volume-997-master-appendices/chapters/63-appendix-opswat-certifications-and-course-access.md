# Chapter 63: Appendix — OPSWAT Certifications and Course Access

The **OPSWAT Academy** certification program — the tracks, the Associate and Professional
certifications, and the training/access model. Verified on **4 August 2026** from **opswatacademy.com**
(and opswat.com/academy), the sources that anchor
[Volume CXXIX — OPSWAT Certification Tracks](../../volume-129-opswat-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** OPSWAT Academy is a **free-first Critical Infrastructure Protection (CIP)**
academy: the foundational and **Associate** certifications are **free** (explicitly to close the CIP
skills gap), delivered self-paced (Teachable-hosted at opswat-academy.teachable.com) with **Credly**
digital badges and, for qualifying courses, **ISC2 CPE credit** (maintaining CISSP/SSCP/CCSP).
**Professional** (product) certifications on the **MetaDefender** platform are paid (around US$1,000
each), plus a 3-day MetaDefender Platform Bootcamp and instructor-led options; the **OPSWAT OT Security
Expert** designation is the expert tier. Register on opswatacademy.com.

> **Currency.** The **free-vs-paid split can shift**, and **some Associate certifications carry a
> validity window** (Credly shows expiry) — re-verify which certs are free and their validity on
> opswatacademy.com/Credly before planning. MetaDefender products and the Professional cert lineup
> evolve; confirm the current catalog.

## Free and low-cost resources and entry points

- **[OPSWAT Academy](https://opswatacademy.com/)** — the authoritative program page (start for free)
- **[OPSWAT Academy courses](https://opswatacademy.com/courses)** — the full IT/OT CIP catalog
- **[OPSWAT Academy FAQs](https://opswatacademy.com/company/faqs)** — free-vs-paid, validity, badges
- **[OPSWAT OT Security training](https://opswatacademy.com/opswat-ot-security-expert-training-course)**
  — the OT Security Expert track
- **[OPSWAT Academy (Cybersecurity Training for Critical Infrastructure)](https://www.opswat.com/academy)**
  — program overview
- **Free study lab:** any Linux host with `python3` (plus `nftables`/`iproute2` for the network labs)
  models Deep CDR, multiscanning, endpoint posture, NAC, and secure boundary transfer — see the
  volume's labs

## Fees, delivery, and renewal

- **Fees:** foundational + **Associate certifications are free**; **MetaDefender Professional** certs are
  paid (~US$1,000 each); confirm current pricing on opswatacademy.com. Lab practice is free.
- **Delivery:** self-paced online (Teachable) for Associates; instructor-led / bootcamp / on-site for
  product training. Badges via Credly; ISC2 CPE credit for qualifying courses.
- **Prerequisites:** none for the foundational/Associate certs (ICIP is the free entry); Professional
  product certs assume the relevant foundation and target MetaDefender deployment.
- **Validity/renewal:** some Associate certs expire (validity window on Credly) — re-verify and
  renew/retake as required; the free-first model itself can change.

## The certifications

Verified against opswatacademy.com on 4 August 2026.

### Tracks

| Track | Focus |
| --- | --- |
| CIP Essentials | Vendor-neutral Critical Infrastructure Protection foundations |
| CyberOps | Hands-on red/blue, ethical hacking, OSINT, protocol analysis, PLC security (authorized/defensive) |
| OPSWAT Product Training | MetaDefender platform technical training |
| End-User Guides | Product usage |

### Associate certifications (Credly, many free)

| Cert | Focus |
| --- | --- |
| ICIP — Introduction to Critical Infrastructure Protection | CIP concepts; identifying critical networks (free intro) |
| OCFA — Cybersecurity Fundamentals Associate | Infosec vs cybersecurity vs ethical hacking; technologies; careers |
| OFSA — File Security Associate | File-system protection; Deep CDR, multiscanning, static vs dynamic analysis |
| OECA — Endpoint Compliance Associate | Endpoint posture, NAC, BYOD risk, enforcement without killing productivity |
| ONSA — Network Security Associate | NAC; layer-2 vs layer-3 deployments; network security principles |
| OSSA — Secure Storage Associate | Secure file storage and transfer (MetaDefender Vault) |

### Professional (product) and Expert

| Credential | Focus |
| --- | --- |
| MetaDefender Core Professional | Multiscanning + Deep CDR + DLP + sandbox engine (the scanning hub) |
| MetaDefender ICAP Professional | CDR/multiscan for web/proxy traffic (inline via ICAP) |
| MetaDefender Kiosk Professional | Removable-media scanning stations (into air-gapped OT) |
| MetaDefender MFT Professional | Managed/secure file transfer across zones |
| OPSWAT OT Security Expert | End-to-end critical-infrastructure/OT defense (products + boundary architecture + operations) |

## Notes

- **Free-first is the defining feature:** the Associate certifications are genuinely free and
  vendor-useful (CIP concepts apply beyond OPSWAT), which is why they are the recommended starting
  point regardless of which products you deploy.
- **Deep CDR is the signature technology:** rebuild files clean rather than detect — the differentiator
  the file-security track centers on.
- **CIP/OT context:** this program pairs with [ISA/IEC 62443 (Volume CXXVIII)](../../volume-128-isa-iec-62443-certifications/README.md)
  — the standard OPSWAT's kiosk/vault/CDR implement — and the OT-monitoring product volumes
  ([Claroty CXIII](../../volume-113-claroty-xdome-lab/README.md),
  [Nozomi CXIV](../../volume-114-nozomi-networks-lab/README.md),
  [TXOne CXV](../../volume-115-txone-networks-lab/README.md)).
