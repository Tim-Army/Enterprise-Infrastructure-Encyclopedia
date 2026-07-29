# Chapter 10: The Restored NSE Program and the Four Tracks

## Learning Objectives

- Explain the Fortinet NSE certification program as restructured on
  15 July 2026: eight numbered levels (NSE 1–8) across four tracks
- Map the four tracks — Secure Networking, Security Operations, Cloud
  Security, and SASE — and how NSE 4 (FortiGate/FortiOS) anchors all
  of them
- Position this volume's upper levels (NSE 5–8) against its own NSE 1–4
  foundation (Chapters 01–09)
- Read the level/track structure well enough to plan a path to any
  Fortinet credential

## Theory and Architecture

### The program in one sentence

On **15 July 2026** Fortinet retired the named FCF/FCA/FCP/FCSS/FCX
certifications and **restored the NSE 1–8 numbered progression**,
expanding from five levels to eight and organizing technical
certifications into **four tracks — Secure Networking, Security
Operations, Cloud Security, and SASE** (verified against Fortinet
Training Institute's certification pages on 22 July 2026; existing
FCP/FCSS/FCX holders were auto-mapped to NSE levels by Fortinet's
published table). This volume's Chapters 01–09 cover **NSE 1–4** (cybersecurity
fundamentals through the FortiGate/FortiOS Administrator); Chapters
10–15 cover **NSE 5–8** across all four tracks.

### The eight levels

**NSE 1–2** are cybersecurity fundamentals (awareness, threat
landscape, the Fortinet portfolio). **NSE 3** is the associate
technical tier. **NSE 4** — FortiGate/FortiOS Administrator — is the
universal foundation: every track requires it. **NSE 5 and NSE 6**
are the professional product tiers, populated by track-specific
administrator and analyst exams. **NSE 7** is the advanced tier —
architect and senior-analyst exams per track. **NSE 8** is the expert
tier: an NSE 8 Core practical exam plus one NSE 8 Specialization
practical (the specialization within one year of the core), with the
credential valid two years.

### Tracks are the organizing axis

The same level number means a different exam in each track. NSE 5 in
Secure Networking is FortiSwitch or Secure Wireless LAN
Administration; NSE 5 in Security Operations is FortiAnalyzer Analyst
or FortiSandbox; NSE 5 in Cloud Security is FortiWeb/FortiADC/
FortiAppSec; NSE 5 in SASE is FortiSASE and SD-WAN Core. This volume
devotes a chapter to each track's NSE 5–7 ladder and closes with NSE 8.

## Design Considerations

- Everyone starts at NSE 4 (Chapter 09); choose the track
  by role, not prestige
- Recertification runs on the level (Fortinet updated the rules in the
  2026 change; NSE 8 now carries recert points and a two-year term) —
  plan renewals against the level, and re-verify exam availability at
  registration
- Industry certifications (e.g., OT Security) sit alongside the NSE
  ladder; know they exist and map some product exams
- This program's naming changed twice in three years — treat every
  code and level as verify-before-booking

## Implementation and Automation

```text
# The path grammar, by track (NSE 4 is shared foundation)
Secure Networking : NSE1-2 -> NSE3 -> NSE4 -> NSE5 (FortiSwitch/Wireless)
                    -> NSE6 (FortiManager/NAC/Analyzer/...) -> NSE7 (Ent. Firewall) -> NSE8
Security Operations: ... NSE4 -> NSE5 (FortiAnalyzer/Sandbox)
                    -> NSE6 (FortiSIEM/SOAR/EDR/NDR/...) -> NSE7 (SecOps Analyst/Architect) -> NSE8
Cloud Security     : ... NSE4 -> NSE5 (FortiWeb/ADC/AppSec)
                    -> NSE6 (FortiMail/CNAPP/DDoS/AWS/Azure/GCP) -> NSE7 (Public Cloud Architect) -> NSE8
SASE               : ... NSE4 -> NSE5 (FortiSASE + SD-WAN Core)
                    -> NSE6 (FortiClient EMS/DLP/EDR/SD-WAN) -> NSE7 (FortiSASE [Enterprise]) -> NSE8
```

## Validation and Troubleshooting

- Verify each exam on Fortinet Training Institute the week you book —
  the 15 July 2026 transition renamed everything and a stale study
  guide will name a retired credential
- The transition-mapping table is the authority on how a legacy
  FCP/FCSS credential became an NSE level; read it before assuming
- Prerequisites: NSE technical exams assume NSE 4; NSE 8 assumes the
  track's NSE 7 path — plan the chain, not the endpoint

## Security and Best Practices

- Book only through Fortinet Training Institute and Pearson VUE; the
  braindump economy voids credentials
- Keep the Fortinet credential record current; employers verify there
- Practice on FortiGate VM / the free Fortinet labs, licensed images
  only (the FortiGate VM lab platform from Chapters 03–09 extends here)

## References and Knowledge Checks

- Fortinet Training Institute certification pages and the 2026
  program-change FAQ (the authority on levels, tracks, and mapping)
- Chapters 01–09 of this volume (NSE 1–4)

Knowledge checks:

1. Name the four tracks and the single certification level they all
   share, and why it is shared.
2. What are the two components of NSE 8, and what is the one-year rule?
3. A candidate held an active FCSS on 14 July 2026. What determined the
   NSE level they woke up with on the 15th?

## Hands-On Lab

This chapter orients you in the **restored Network Security Expert (NSE) program**
(effective 15 July 2026): NSE 1–3 foundational, NSE 4 associate (FortiOS Administrator),
NSE 5–7 across four professional **tracks** (Secure Networking, Security Operations,
Cloud Security, SASE), and NSE 8 expert. The labs are planning/orientation exercises
using the live Fortinet Training Institute catalog and your own FortiGate. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 10.1–10.2** — a browser for the Fortinet Training
Institute site and a FortiGate for the inventory step. **Cost:** none.

### Lab 10.1 — Map the NSE certification program (Topic: Program structure)

**Objective:** Lay out the NSE levels and where each exam sits.

```text
# On the Fortinet Training Institute catalog, record for each level:
#   NSE 1  Cybersecurity awareness            (foundational, self-paced)
#   NSE 2  Threat landscape + portfolio        (foundational, self-paced)
#   NSE 3  Security Fabric + product operator  (foundational, self-paced)
#   NSE 4  FortiOS 7.6 Administrator           (associate, proctored exam)
#   NSE 5  Track specialist  (four tracks)     (professional, proctored)
#   NSE 6  Track professional (four tracks)    (professional, proctored)
#   NSE 7  Track expert      (four tracks)     (professional, proctored)
#   NSE 8  Expert practical  (Core + Specialization)
```

**Expected result:** a one-page ladder from awareness (NSE 1) to expert practical
(NSE 8), with NSE 4 as the pivot where hands-on FortiOS competence is proven and the
four tracks branch — the structure the rest of this volume follows chapter by chapter.

**Negative test:** assume the tracks start at NSE 4; they branch at NSE 5 — NSE 4 is a
single common associate exam that all four tracks build on.

**Cleanup:** none.

### Lab 10.2 — Choose a track and build a study plan (Topic: Track selection)

**Objective:** Match your role to a track and inventory the gear you can practice on.

```text
# Decide the track from your job function:
#   Secure Networking  -> firewall/switch/AP/SD-WAN engineers   (Chapter 11)
#   Security Operations -> SOC / detection & response analysts    (Chapter 12)
#   Cloud Security     -> app/cloud/email security engineers     (Chapter 13)
#   SASE               -> remote-access / edge / SD-WAN teams     (Chapter 14)
# Then inventory what you can lab on:
get system status | grep -i Model
diagnose sys fortiguard-service status 2>/dev/null | head
```

**Expected result:** a chosen track aligned to your daily work and a list of the
products you already have to practice on — the plan that makes the NSE 5–7 chapters
(11–14) actionable rather than abstract.

**Negative test:** pick a track by prestige rather than role; you will study products you
never touch and retain little — track choice should follow the systems you operate.

**Cleanup:** none.

## Lab Verification

Verification means the plan's chain is correct for the chosen track,
every exam was confirmed live on Fortinet's pages on the stated date,
and the NSE 8 two-part requirement and prerequisites are captured.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] NSE 1–8 structure and the 15 July 2026 change explained
- [ ] Four tracks mapped with NSE 4 as shared foundation
- [ ] The chosen track's NSE 5–8 chain drafted and live-verified
- [ ] Relationship to the NSE 1–4 foundation (Chapters 01–09) understood
