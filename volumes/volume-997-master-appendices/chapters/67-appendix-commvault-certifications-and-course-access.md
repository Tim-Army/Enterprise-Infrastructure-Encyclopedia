# Chapter 67: Appendix — Commvault Certifications and Course Access

The **Commvault** certification program — the four tiers, courses, and access model. Verified on
**4 August 2026** from **readiverse.com/academy** (Readiverse Academy) and Commvault's own program
announcements, the sources that anchor [Volume CXXXIII — Commvault Certification
Tracks](../../volume-133-commvault-certifications/README.md). Third-party training resellers and
exam-dump sites were excluded as sources — see the currency note below for why that matters especially
here.

**How access works.** Training and certification run in **Readiverse Academy**, whose program is branded
"**four tiers, one path**" and described as "**vendor-validated credentials, not just course
completions**." Credentials are earned through a combination of **coursework, hands-on lab activities,
and validated assessments**, with **digital badges** on completion. Delivery is **self-paced**, with
select courses offered **instructor-led**. The program serves platform administrators, security
specialists, cloud engineers, and workload owners across **SaaS, software, and hybrid** deployments.

**Commvault is an [ISC2 CPE Authorized Submitter](https://www.readiverse.com/academy)** — Readiverse
coursework earns continuing professional education credits toward ISC2 certifications such as the CISSP
([Volume XL](../../volume-040-isc2-certifications/README.md)).

> **Currency — read this before planning.** The four-tier structure was **introduced in June 2026**:
> Practitioner launched first, Specialist and Professional about a week later, and Expert about a month
> later. Requirements and exam details for the upper tiers were still being finalized at announcement,
> so **verify current requirements on Readiverse Academy before committing**. This also means most
> third-party "Commvault certification" courses on the market still describe the *previous* scheme —
> a common trap when a vendor restructures a program.

## Free and low-cost resources and entry points

- **[Readiverse Academy](https://www.readiverse.com/academy)** — the authoritative training and certification hub
- **[Commvault Cloud Community](https://community.commvault.com/)** — including the [Readiverse Academy community](https://community.commvault.com/readiverse-academy-60) where program changes are announced
- **Live simulations** — the **Cyber Resilience Workshop** (2-hour interactive session), **Minutes to Meltdown** (ransomware decision simulation), and **Minutes to Recovery** (3-hour exercise taking the attacker, defender, and recovery roles)
- **Guides and whitepapers** — Commvault Guide to Cleanroom; *Anomaly and Threat Detection Primer*; *Mastering Cyber Resilience*
- **Free study lab:** any host with `python3` models retention and cycle pruning, deduplication and DDB behavior, RPO/RTO arithmetic, immutability/WORM semantics, ransomware anomaly detection, cleanroom orchestration, and dependency-ordered recovery (see the volume's labs) — no Commvault software needed

## Fees, delivery, and renewal

- **Fees:** not published on the public academy pages; exam and course fees vary by track. Confirm with Commvault or a partner. Lab practice on free primitives is free.
- **Delivery:** self-paced online, with select instructor-led courses; certification requires coursework **plus hands-on labs plus validated assessments**. Badges are digital and claimed on completion.
- **Prerequisites:** none formal for Practitioner; the tiers form a ladder, each building on the one below.
- **Validity/renewal:** verify the current recertification policy on Readiverse Academy — the program is new enough that renewal terms were not published at announcement.

## The four tiers

Verified against Readiverse Academy and the June 2026 program announcement.

| Tier | Focus | Requirements as announced |
| --- | --- | --- |
| **Commvault Cloud Practitioner** | Foundational platform and cyber-resilience knowledge | **Commvault Cloud Administrator** course (~4 h) + **Cyber Resilience** course (~4 h) + **one workload course** (~30 min) + **exams for the Administrator and Cyber Resilience components** + claim the digital badge |
| **Commvault Cloud Specialist** | Expanded operational, workload, and security depth | Builds on Practitioner |
| **Commvault Cloud Professional** | Advanced recovery and workload expertise | Includes **Cloud Rewind** or **Cleanroom Recovery** coursework |
| **Commvault Cloud Expert** | Cloud engineering and resilience leadership | **Cloud Engineer** coursework + advanced feature courses + **Cloud Rewind** + **Cleanroom Recovery** |

### The three learning pillars

Every tier is built on the same three skill areas: **foundational platform skills**, **cyber
resilience**, and **workload and feature expertise**. Note that resilience is examined from the entry
tier upward — it is not an advanced add-on.

## Named certifications

| Certification | Subject |
| --- | --- |
| **Commvault Cloud Administrator** | Platform administration core |
| **Cyber Resilience Certification** | Immutability, air gap, anomaly detection, resilience practice |
| **Commvault Cloud SaaS — Threat Scan** | Detecting corruption, encryption, and malware in protected data |
| **Commvault Cloud SaaS — Commvault Cleanroom** | Isolated, on-demand clean recovery environments |
| **Commvault Cloud SaaS — Cloud Rewind** | Cloud application and dependency rebuild |

## Workload and quick-solution courses

| Course group | Titles |
| --- | --- |
| **Workload Hero** | Commvault Cloud SaaS — Microsoft 365; Active Directory & Entra ID; File Server Protection; VMware; Oracle |
| **Problem Solvers** (quick solutions) | Configure Cloud Storage; Overview of Virtualization; Secondary and Auxiliary Copies; Oracle Agent — Troubleshooting Performance; M365 Exchange Operations hands-on guide |

## Notes

- **Resilience from the first tier:** the Practitioner tier requires both a platform exam *and* a cyber
  resilience exam, reflecting Commvault's positioning of backup as a security control rather than an
  operations task. Experienced backup administrators often find the resilience half the harder one.
- **The Professional tier is defined by recovery capability** — Cloud Rewind or Cleanroom Recovery — which
  are the capabilities that answer "where do we restore to when production is compromised?"
- **Widest workload coverage** among the encyclopedia's data-protection volumes, alongside
  [Veeam LXXXV](../../volume-085-veeam-certifications/README.md),
  [Rubrik CXXX](../../volume-130-rubrik-certifications/README.md), and
  [NetApp LXXXIV](../../volume-084-netapp-certifications/README.md).
- **The ISC2 CPE tie-in is unusual and useful:** training you would take anyway also maintains an ISC2
  credential.
