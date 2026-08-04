# Chapter 62: Appendix — ISA/IEC 62443 Certifications and Course Access

The **ISA/IEC 62443 Cybersecurity Certificate Program** — the four certificates, their courses, and the
training/access model. Verified on **4 August 2026** from **isa.org** (the certificate-program page),
the source that anchors
[Volume CXXVIII — ISA/IEC 62443 Certification Tracks](../../volume-128-isa-iec-62443-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** Each certificate requires an **ISA course plus a proctored exam**. Courses are
offered by **ISA** (the International Society of Automation) in multiple formats — classroom, virtual
instructor-led (`V`), online self-paced (`E`), and modular (`M`) — so a course code like IC32 has
IC32/IC32V/IC32E/IC32M variants. **Certificate 1 (IC32) is a hard prerequisite** for Certificates 2–4,
which may be taken in any order; all four automatically confer the **Expert** designation. Register
through isa.org; related standards and community resources come from the **ISA Global Cybersecurity
Alliance (ISAGCA)**, and conformance certification of *products/systems* (a separate track from these
personnel certificates) is run by **ISASecure**.

> **Currency.** The certificates **do not expire** — there is no renewal requirement. But the IEC 62443
> standard is revised and extended over time, so a designation rests on the edition current when earned;
> re-read the current standard parts (e.g. 62443-3-2 risk methodology, 4-2 component requirements) on a
> cadence. Verify current course formats and exam logistics on isa.org before registering.

## Free and low-cost resources and entry points

- **[ISA/IEC 62443 Cybersecurity Certificate Program](https://www.isa.org/certification/certificate-programs/isa-iec-62443-cybersecurity-certificate-program)**
  — the authoritative program page (certificates, courses, registration)
- **[ISA Connectivity & Cybersecurity training](https://www.isa.org/connectivity-and-cybersecurity/training-and-certificates)**
  — the broader training catalog
- **[ISA Global Cybersecurity Alliance (ISAGCA)](https://isagca.org/)** — standards resources, white
  papers, and free educational material on 62443
- **[ISASecure](https://isasecure.org/)** — 62443 *conformance* certification for products and systems
  (distinct from these personnel certificates)
- **Free study lab:** any Linux host with `nftables`, `iproute2`, `netcat`, and `python3` models zones,
  conduits, security levels, and risk scoring (see the volume's labs)

## Fees, delivery, and renewal

- **Fees:** course + exam pricing is published per course on isa.org (ISA member discounts apply);
  confirm current pricing there. The volume's lab practice is free.
- **Delivery:** ISA courses in classroom / virtual (`V`) / online self-paced (`E`) / modular (`M`)
  formats; each certificate's exam is proctored. Verify exam length/format on the course page.
- **Prerequisites:** none for Certificate 1 (IC32); **Certificate 1 is required** before Certificates 2
  (IC33), 3 (IC34), and 4 (IC37), which may be taken in any order.
- **Validity/renewal:** the certificates **do not expire**; there is no renewal. Staying current with
  the evolving standard is the practitioner's responsibility.

## The certificates

Verified against isa.org on 4 August 2026.

| Certificate | Course | Lifecycle phase | Prerequisite | Focus |
| --- | --- | --- | --- | --- |
| 1 — Cybersecurity Fundamentals Specialist | IC32 (V/E/M) | Foundation | none | Standards to secure ICS: reference model, zones/conduits, security levels, foundational requirements |
| 2 — Cybersecurity Risk Assessment Specialist | IC33 (V/E/M) | Assess | Certificate 1 | Assessing the cybersecurity of new/existing IACS; high-level + detailed risk assessment; SL-Target |
| 3 — Cybersecurity Design Specialist | IC34 (V/M) | Design | Certificate 1 | IACS cybersecurity design & implementation; CRS, segmentation, countermeasures, SL-Achieved |
| 4 — Cybersecurity Maintenance Specialist | IC37 (V/M) | Operate/Maintain | Certificate 1 | IACS cybersecurity operations & maintenance; OT patching, monitoring, IR, change control |
| ISA/IEC 62443 Cybersecurity Expert | — | (all phases) | all four certificates | Automatic designation; no separate exam |

## Notes

- **Certificates vs conformance:** these are **personnel** certificates (individuals). 62443
  *conformance* certification of products and systems is a separate program run by **ISASecure**
  (SDLA, SSA, CSA, etc.) — relevant to product suppliers, not covered by these four certificates.
- **The Expert designation is earned, not examined:** hold all four certificates and it is conferred
  automatically.
- **OT context:** this program pairs with the encyclopedia's OT product volumes
  ([Forescout XV](../../volume-015-forescout-platform-certifications/README.md),
  [Claroty CXIII](../../volume-113-claroty-xdome-lab/README.md),
  [Nozomi CXIV](../../volume-114-nozomi-networks-lab/README.md),
  [TXOne CXV](../../volume-115-txone-networks-lab/README.md)) — the tools that implement what 62443
  requires.
