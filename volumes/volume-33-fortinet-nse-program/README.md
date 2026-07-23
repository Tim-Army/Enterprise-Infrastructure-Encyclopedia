# Volume XXXIII — Fortinet NSE Program: Security Operations, Cloud, and SASE

Fortinet's certification program above the FortiGate foundation: the
restored NSE 5–8 tiers across the Security Operations, Cloud Security,
and SASE tracks (and the Secure Networking upper levels), with every
certification verified against Fortinet Training Institute after the
15 July 2026 program restructure.

## Overview

On 15 July 2026 Fortinet retired the named FCF/FCA/FCP/FCSS/FCX
certifications and restored an eight-level NSE 1–8 progression across
four tracks. [Volume XIX](../volume-19-fortinet-network-security/README.md)
covers NSE 1–4 (cybersecurity fundamentals through the FortiGate/
FortiOS Administrator). This volume covers **NSE 5–8** across all four
tracks — Secure Networking's upper levels, and the Security Operations,
Cloud Security, and SASE tracks end to end — closing with the NSE 8
expert practical.

## Certification alignment

This volume maps to the Fortinet NSE certification program as
restructured on 15 July 2026, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md).
Chapter content describes exam scope and points to Fortinet Training
Institute's official pages; it does not reproduce proprietary exam
questions or licensed courseware. **Verify the live exam before every
booking** — this program was renamed twice in three years (NSE →
FCP/FCSS/FCX → NSE).

### The exams

Verified against Fortinet Training Institute's certification pages and
the 2026 program-change transition mapping on **22 July 2026**. NSE 4
(FortiGate/FortiOS Administrator, Volume XIX) is the shared
prerequisite for every track. An exam may map to a level within more
than one track (for example FortiClient EMS in Secure Networking and
SASE). NSE 8 is a two-module practical — an NSE 8 Core plus one NSE 8
Specialization (within one year of the core), valid two years.

#### Secure Networking (Chapter 02)

| NSE level | Certification exams |
| --- | --- |
| **NSE 5** | FortiSwitch Administrator; Secure Wireless LAN Administrator |
| **NSE 6** | FortiAnalyzer Administrator; FortiAuthenticator Administrator; FortiClient EMS Administrator; FortiManager Administrator; FortiNAC Administrator; FortiVoice Administrator; LAN Edge Architect; OT Security Architect; SD-WAN Architect; SD-WAN Enterprise Administrator; Secure Networking Support Engineer |
| **NSE 7** | Enterprise Firewall Administrator |
| **NSE 8** | Core practical + one Specialization practical (this track) |

#### Security Operations (Chapter 03)

| NSE level | Certification exams |
| --- | --- |
| **NSE 5** | FortiAnalyzer Analyst; FortiSandbox Administrator |
| **NSE 6** | FortiEDR Administrator; FortiSIEM Analyst; FortiSOAR Administrator; FortiSOAR Analyst; FortiDeceptor Administrator; FortiNDR Analyst; FortiRecon Analyst |
| **NSE 7** | Security Operations Analyst; Security Operations Architect |
| **NSE 8** | Core practical + one Specialization practical (this track) |

#### Cloud Security (Chapter 04)

| NSE level | Certification exams |
| --- | --- |
| **NSE 5** | FortiADC Administrator; FortiAppSec Administrator; FortiWeb Administrator |
| **NSE 6** | AWS Cloud Security Administrator; Azure Cloud Security Administrator; GCP Cloud Security Administrator; FortiMail Administrator; FortiMail Workspace Administrator; FortiCNAPP Analyst; FortiDDoS Administrator |
| **NSE 7** | Public Cloud Security Architect |
| **NSE 8** | Core practical + one Specialization practical (this track) |

#### SASE (Chapter 05)

| NSE level | Certification exams |
| --- | --- |
| **NSE 5** | FortiSASE and SD-WAN Core Administrator |
| **NSE 6** | FortiClient EMS Administrator; FortiDLP Administrator; FortiEDR Administrator; SD-WAN Architect; SD-WAN Enterprise Administrator |
| **NSE 7** | FortiSASE Administrator; FortiSASE Enterprise Administrator |
| **NSE 8** | Core practical + one Specialization practical (this track) |

**Fundamentals and associate (Volume XIX).** NSE 1 and NSE 2
(cybersecurity awareness and the threat landscape / Fortinet
portfolio), NSE 3 (associate technical), and NSE 4 (FortiGate/FortiOS
Administrator) are covered in Volume XIX, Chapters 01–09, and remain
the on-ramp to every track above.

## Chapters

1. [The Restored NSE Program and the Four Tracks](chapters/01-the-restored-nse-program-and-the-four-tracks.md)
2. [Secure Networking Upper Levels — Switching, Wireless, and Management](chapters/02-secure-networking-upper-levels-switching-wireless-and-management.md)
3. [Security Operations Track — FortiAnalyzer, SIEM, SOAR, and EDR](chapters/03-security-operations-track-fortianalyzer-siem-soar-and-edr.md)
4. [Cloud Security Track — FortiWeb, CNAPP, Mail, and Public Cloud](chapters/04-cloud-security-track-fortiweb-cnapp-mail-and-public-cloud.md)
5. [SASE Track — FortiSASE, SD-WAN, and the Secure Edge](chapters/05-sase-track-fortisase-sd-wan-and-the-secure-edge.md)
6. [NSE 8 Expert Practical and Certification Operations](chapters/06-nse-8-expert-practical-and-certification-operations.md)

## Study plans

**Pick a track after NSE 4** (Volume XIX). Each track's chapter maps
its NSE 5→7 chain; plan four to six weeks per level with the chapter's
lab and the exam's current objectives from Fortinet Training Institute.
**NSE 8** follows Chapter 06's regimen: full fabric mocks, two clean
mocks as the booking gate, and the Core-then-Specialization sequence
inside the one-year window. Re-verify every exam the week you book.

## Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official objectives | Fortinet Training Institute exam pages | The authority on domains, levels, and current names |
| Free training | Fortinet self-paced NSE courses and labs (free account) | Much of the NSE 1–7 objective set is practicable at no cost |
| Paid training | Fortinet instructor-led training (ILT) | Deep, hands-on preparation for the upper levels |
| Hands-on | FortiGate VM and the Volume XIX/XXVI lab host | The Security Fabric labs this volume builds on |

## Volume resources

- [Volume index](INDEX.md)
- [Volume glossary](GLOSSARY.md)
- [Master table of contents](../../MASTER_TOC.md)
- [Fortinet courses appendix — Volume XCVII](../volume-97-master-appendices/README.md)

## Building and validating this volume

```bash
# Full validation and repo-wide link checks.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-33-fortinet-nse-program
```
