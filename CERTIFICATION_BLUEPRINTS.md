# Certification Blueprints

Maps each volume to relevant current vendor certifications and training
paths. This file names blueprint domains and points to the controlling
vendor source; it does not reproduce proprietary assessment content.

| Volume | Certification / Training Path | Vendor Source |
| --- | --- | --- |
| II — Network Engineering Foundations | CCST Networking (100-150) | Cisco Learning & Certifications |
| III — Cisco Enterprise Networking | CCNA, CCNP Enterprise (ENCOR/ENARSI), CCNP Wireless: WLCOR core (350-101) + WLSD (300-110) or WLSI (300-120); WLCOR also qualifies CCIE Wireless | Cisco Learning & Certifications |
| IV — Enterprise Systems Administration | CCST IT Support (100-140) | Cisco Learning & Certifications |
| V — VMware Virtualization | VCP-NV (2V0-41.24), VCP-VCF Support (2V0-15.25), VCP-VCF Administrator (2V0-17.25), VCP-VVF Administrator (2V0-16.25), VCP-VVF Support (2V0-18.25) | Broadcom/VMware Learning |
| IX — Infrastructure Automation | CCNA Automation (200-901), CCNP Automation: core (350-901) + one concentration, CCIE Automation — rebranded from DevNet on 3 February 2026 | Cisco Learning & Certifications |
| X — Enterprise Cybersecurity | CCST Cybersecurity (100-160), CCNA Cybersecurity (200-201), CCNP Cybersecurity: CBRCOR core (350-201) + CBRFIR (300-215) — rebranded from CyberOps on 3 February 2026 | Cisco Learning & Certifications |
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
| XXVII — Cisco Data Center | CCNP Data Center: DCCOR core (350-601) + concentrations DCID (300-610), DCIT (300-615), DCACI (300-620), DCAUTO (300-635, rebranding to DCNAUTO), DCAI (300-640); DCCOR also qualifies CCIE Data Center | Cisco Learning & Certifications |
| XXVIII — Cisco Collaboration | CCNP Collaboration: CLCOR core (350-801) + concentrations CLICA (300-810), CLACCM (300-815), CLCEI (300-820), CLCCE (300-830), CLAUTO (300-835, EOL announced); CLCOR also qualifies CCIE Collaboration | Cisco Learning & Certifications |
| XXIX — Cisco Service Provider | CCNP Service Provider: SPCOR core (350-501) + concentrations SPRI (300-510), SPVI (300-515), SPAUTO (300-535, EOL announced); SPCOR also qualifies CCIE Service Provider | Cisco Learning & Certifications |
| XXX — Cisco CCDE Network Design | CCDE (expert-level design): Written (400-007) + Practical, v3.1 unified topics, with AI Infrastructure / Large Scale Networks / On-Prem and Cloud Services / Workforce Mobility electives | Cisco Learning & Certifications |

Volumes not listed (I, VI–VIII, XI–XIII, XCIX) are vendor-neutral or
cross-domain and are not mapped to a single certification blueprint; they
support the certification-track volumes above with foundational and
integrated-lab material.

Always confirm the current blueprint against the vendor's official page
before using a chapter for exam preparation — blueprints change independently
of this repository's release cycle.

## Cisco portfolio coverage

The Cisco certification portfolio is now fully mapped. Owning volumes
exist for every CCNP professional track — Enterprise (III), Security
(XXV), Data Center (XXVII), Collaboration (XXVIII), and Service
Provider (XXIX) — for the expert-level CCDE design path (XXX), and
alignment sections cover the entry/associate CCST, Automation, and
Cybersecurity tracks (Volumes II, IV, IX, X). No Cisco track is
awaiting a volume.

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

The rest of the Cisco portfolio was added on **22 July 2026**, all
against Cisco's own exam-topics documents or Learning Network topic
pages: the three CCST entry exams (100-150 Networking, 100-160
Cybersecurity, 100-140 IT Support — Cisco publishes no domain weights at
this tier), the Automation track (200-901 v1.1 and 350-901 v1.1 —
rebranded from DevNet on 3 February 2026, with v1.2 minor updates
announced), the Cybersecurity track (200-201 v1.1, CBRCOR 350-201 v1.1,
and CBRFIR 300-215 v1.1 — rebranded from CyberOps the same day), and the
three unmapped cores (DCCOR 350-601 v1.2, CLCOR 350-801 v2.0, SPCOR
350-501 v1.1). Every weighted domain set sums to 100%. One stale-page
find worth recording: Cisco's own exam page still described SPCOR as
v1.0 while its Learning Network exam-topics page carries v1.1 — the
topics page is the authority.

Volume XXVII (Cisco Data Center) was created on **22 July 2026**,
promoting the Data Center track out of the awaiting list. All six exams
were verified against their Cisco exam-topics documents the same day:
DCCOR `350-601` v1.2 (120 min) and the 90-minute concentrations DCID
`300-610` v1.2, DCIT `300-615` v1.2, DCACI `300-620` v1.2, DCAUTO
`300-635` v1.1, and DCAI `300-640` v1.0 (GA 3 February 2026 — DCAI
plus DCCOR earns the certification). Each domain set sums to 100%.
DCAUTO is being rebranded DCNAUTO under the CCNP Automation
restructure with the code unchanged; confirm its Data Center
concentration status at registration.

Volume XXVIII (Cisco Collaboration) was created on **22 July 2026**,
promoting the Collaboration track out of the awaiting list. All six
exams were verified against their Cisco exam-topics documents the same
day: CLCOR `350-801` v2.0 (120 min) and the 90-minute concentrations
CLICA `300-810` v1.2, CLACCM `300-815` v1.2, CLCEI `300-820` v1.2,
CLCCE `300-830` v1.0 (new, GA 3 February 2026), and CLAUTO `300-835`
v1.1. Each domain set sums to 100%. **CLAUTO's end-of-life is
announced** under the Automation restructure — the volume records it
and tells readers to confirm availability before scheduling.

Volume XXIX (Cisco Service Provider) was created on **22 July 2026**,
promoting the last CCNP track out of the awaiting list — only the CCDE
design-expert path now remains unmapped. All four exams were verified
the same day (SPCOR against its Learning Network exam-topics page,
which carries v1.1 where Cisco's exam page still shows v1.0; the rest
against their exam-topics documents): SPCOR `350-501` v1.1 (120 min)
and the 90-minute concentrations SPRI `300-510` v1.1, SPVI `300-515`
v1.1, and SPAUTO `300-535` v1.1. Each domain set sums to 100%.
**SPAUTO's end-of-life is announced** under the Automation restructure
— the volume records it and tells readers to confirm availability
before scheduling.

Volume XXX (Cisco CCDE Network Design) was created on **22 July 2026**,
completing the Cisco portfolio. The CCDE was verified the same day
against Cisco's Learning Network **CCDE v3.1 unified exam topics** page
(the written and practical now share one topic set), clearing the
"not verified" flag it had carried: the CCDE Written (400-007) is a
2-hour, 90–110-question exam and the Practical is an 8-hour scenario
exam (three Core Enterprise modules plus one elective — AI
Infrastructure, Large Scale Networks, On-Prem and Cloud Services, or
Workforce Mobility). The five unified design domains — Business
Strategy 15%, Control/Data/Management Plane and Operational 25%,
Network Design 30%, Service Design 15%, Security Design 15% — sum to
100%. Version 3.1 adds AI/ML and generative-AI topics.

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
