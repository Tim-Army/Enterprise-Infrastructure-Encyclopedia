# Certification Blueprints

Maps each volume to relevant current vendor certifications and training
paths. This file names blueprint domains and points to the controlling
vendor source; it does not reproduce proprietary assessment content.

| Volume | Certification / Training Path | Vendor Source |
| --- | --- | --- |
| III — Cisco Enterprise Networking | CCNA, CCNP Enterprise (ENCOR/ENARSI), CCNP Wireless: WLCOR core (350-101) + WLSD (300-110) or WLSI (300-120); WLCOR also qualifies CCIE Wireless | Cisco Learning & Certifications |
| V — VMware Virtualization | VCP-NV (2V0-41.24), VCP-VCF Support (2V0-15.25), VCP-VCF Administrator (2V0-17.25), VCP-VVF Administrator (2V0-16.25), VCP-VVF Support (2V0-18.25) | Broadcom/VMware Learning |
| XIV — Red Hat Enterprise Linux 10 | RHCSA (EX200) | Red Hat Training and Certification |
| XV — Forescout Platform | FSCA, FSCP, FSCE, FSCA: OT/ICS, FSCE: OT/ICS | Forescout Technologies |
| XVI — Palo Alto Networks Security | Cybersecurity Apprentice, Cybersecurity Practitioner, Network Security Professional, Network Security Analyst, Next-Generation Firewall Engineer, SD-WAN Engineer, Security Service Edge Engineer, Network Security Architect, Cloud Security Professional (secures the Cortex Cloud platform) | Palo Alto Networks Education |
| XVII — AWS Architecture and Security | AWS Certified Solutions Architect – Associate (SAA-C03), AWS Certified Security – Specialty (SCS-C03) | AWS Training and Certification |
| XVIII — Gigamon Network Visibility | Gigamon Certified Professional (GCP) | Gigamon Education Services |
| XIX — Fortinet Network Security | NSE 1–4 of the NSE 1–8 program; NSE 4 — FortiOS 7.6 Administrator (FCF/FCA/FCP/FCSS/FCX retired 15 July 2026) | Fortinet Training Institute |
| XX — Wireshark and Packet Analysis | WCA-101 | Wireshark Certified Analyst Program |
| XXI — Ubuntu Server and Cloud | Canonical Academy SysAdmin qualification (four exams) | Canonical Academy |
| XXII / XXIII — Dell OpenManage / iDRAC | PowerEdge Foundations v2 (D-PE-FN-01), PowerEdge Operate v2 (D-PE-OE-01; supersedes the retired D-PE-OE-23) | Dell Technologies Proven Professional |
| XXIV — Dell VxRail | VxRail Deploy v2 (D-VXR-DY-01), VxRail Operate v2 (D-VXR-OE-01) | Dell Technologies Proven Professional |
| XXV — Cisco Security | CCNP Security: SCOR core (350-701) + concentrations SVPN (300-730), SCAZT (300-740), SISE (300-715), SDSI (300-745); SCOR also qualifies CCIE Security | Cisco Learning & Certifications |

Volumes not listed (I, II, IV, VI–XIII, XCIX) are vendor-neutral or
cross-domain and are not mapped to a single certification blueprint; they
support the certification-track volumes above with foundational and
integrated-lab material.

Always confirm the current blueprint against the vendor's official page
before using a chapter for exam preparation — blueprints change independently
of this repository's release cycle.

## Currency

Every exam code in this table was verified against its vendor's own
published exam description or exam-topics document on **21 July 2026**.
Third-party summaries were not treated as sources; several were found to
be wrong during the check, including one that reported a superseded Cisco
ENCOR version.

The Palo Alto Networks and Canonical Academy programs were confirmed in a
follow-up pass the same day. All four Canonical exams and eight of the
nine Palo Alto certifications matched as written; the ninth was corrected
from "Cortex Cloud Security Professional" to **Cloud Security
Professional**, its official credential name — *Cortex Cloud* is the
platform the exam secures, not part of the certification's title.

The Cisco CCNP Security exams (Volume XXV) were added the same day, each
verified against its Cisco exam-topics document and each summing to 100%.
**Two are mid-transition on 26–27 August 2026:** SCOR `350-701` moves
v1.1→v2.0 (a real reweighting — Content Security dropped as a domain,
Secure Service Edge added), and SISE `300-715` moves v1.1→v1.2 (identical
weights, label change only). Volume XXV targets SCOR v2.0 because its
study plan outlasts the v1.1 cutoff. Re-confirm both at the next currency
check, which now falls inside the transition window.

The CCNP Wireless track (Volume III) was added on **22 July 2026**:
WLCOR `350-101` v1.0, WLSD `300-110` v1.2, and WLSI `300-120` v1.2 were
each verified against its Cisco exam-topics document, and each domain
set sums to 100%. The track launched 19 March 2026, carrying the
wireless content that ENCOR v1.2 removed; WLCOR also replaces ENCOR as
the qualifying written exam for CCIE Wireless (renamed from CCIE
Enterprise Wireless).

Drift in this table is normal and has been frequent. Within a single year
the Dell PowerEdge Operate exam was rebuilt and renumbered, AWS replaced
its Security Specialty blueprint, Fortinet retired and then restored its
NSE naming, and Cisco moved ENCOR to v1.2. **Treat any code here older
than a few months as needing re-confirmation**, and re-run the check when
planning study time rather than assuming this file is current.

Two vendor-side arithmetic artifacts are recorded deliberately in the
volumes rather than silently corrected, because a reader who adds the
numbers up will otherwise assume the transcription is wrong: the Dell
VxRail Operate weights sum to 101%, and the Wireshark WCA-101 protocol
domain is published as 43% while its stated internal split sums to 44%.
Both are as published.
