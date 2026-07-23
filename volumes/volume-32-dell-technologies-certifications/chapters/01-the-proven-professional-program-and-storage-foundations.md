# Chapter 01: The Proven Professional Program and Storage Foundations

## Learning Objectives

- Map Dell's certification framework: portfolios, the
  function-based exam naming (Foundations, Operate, Deploy, Design,
  Install, Maintain), and the D-code format
- Explain modern data center building blocks through the ISM lens:
  storage architectures, RAID, SAN/NAS/object, and cloud models
- Choose an entry certification — ISM Foundations (D-ISM-FN-01), Cloud
  Infrastructure and Services Foundations (D-CIS-FN-01), or a
  portfolio Foundations exam — by role
- Read any Dell exam code on sight and locate its authority page

## Theory and Architecture

### The program in one sentence

Dell Technologies certifications are organized by **portfolio**
(servers, storage platforms, data protection, networking, HCI/cloud,
AI, security, client) and **function** — the exam code says both:
`D-<product>-<function>-<version>`, where the function is FN
(Foundations), OE (Operate), DY (Deploy), DS (Design), IN (Install),
or MN (Maintain), and `-A-` marks an achievement-style credential.
Seventy-seven exams were live when this volume's tables were verified
against Dell Learning's certification pages on **22 July 2026** — the
README carries the complete grouped list; each exam's authority page
is its entry at Dell Learning's certification catalog.

### ISM: the vendor's vendor-neutral spine

**Information Storage and Management Foundations (D-ISM-FN-01)** is the
program's conceptual backbone: intelligent storage systems, RAID and
erasure coding, FC SAN / IP SAN / NAS / object protocols, replication
and archive, and software-defined storage — taught platform-neutrally
before any Power-branded product applies them. Pair it with **CIS
Foundations (D-CIS-FN-01)** where the role leans cloud: service
models, orchestration, and the consumption economics APEX later
productizes.

### Functions define depth, not products

Operate exams certify administration of a running platform; Deploy
adds installation and integration; Design tests sizing and
architecture; Install/Maintain certify field service. The same product
ladder repeats across the portfolio, so mastering one platform's
ladder teaches you to read every other track in the program.

## Design Considerations

- Enter through the Foundations exam nearest your role, not the most
  famous product; the OE exam of the platform you actually run is the
  correct second step
- Dell exams are delivered by Pearson VUE; training lives on Dell
  Learning (subscription Learning Hub, ILT, and on-demand) — plan
  budget accordingly, and mine the free exam-description documents
  hard: they carry the objectives and weights
- This encyclopedia's Volumes XXII (OpenManage), XXIII (iDRAC), and
  XXVI (the R640 lab) are the hands-on companions to this track

## Implementation and Automation

```text
# Reading a D-code, worked examples from the verified table
D-PST-OE-23   -> PowerStore, Operate, 2023 series
D-PDD-DY-01   -> PowerProtect Data Domain, Deploy, -01 series
D-PSC-MN-01   -> PowerScale, Maintain, -01 series
D-AX-RH-A-00  -> APEX Cloud Platform for Red Hat OpenShift, achievement
D-ISM-FN-01   -> Information Storage and Management, Foundations
```

Lab base for the whole volume: the Volume XXVI R640/Proxmox estate
hosts the simulators and virtual editions used throughout — Dell's
hands-on story is appliance-centric, so labs emphasize the management
planes (OME, iDRAC) and virtual/community editions where they exist.

## Validation and Troubleshooting

- Verify any code before study or booking: Dell Learning's
  certification catalog is the authority; the -23 to -01 to -A-00
  series rolls are frequent and silent
- The exam description PDF for each exam lists objectives, weights,
  and recommended training — treat it the way Cisco volumes treat
  exam-topics pages
- CertTracker/Credly records the earned badge; employers verify there

## Security and Best Practices

- Buy exams and courseware only through Dell Learning and Pearson VUE;
  the braindump economy is an integrity trap
- Keep one primary study identity: Dell Learning account, Pearson
  profile, and badge wallet aligned to the same email

## References and Knowledge Checks

- Dell Learning certification overview and available-exams catalog —
  the primary source for every code in this volume
- ISM participant guide (Dell's flagship storage text)

Knowledge checks:

1. Decode D-PCR-DY-01 and D-XTR-MN-A-24 completely.
2. Which two Foundations exams anchor the program, and which roles
   choose each?
3. Where do objectives and weights for a Dell exam live, and why does
   this volume not restate them?

## Hands-On Lab

Build the program map for your own role: pick a target portfolio,
pull the exam-description documents for its Foundations/OE/DY ladder,
and produce a one-page plan (codes, objectives themes, training
sources, order). Verify every code against Dell Learning's catalog the
same day and date-stamp the plan.

## Lab Verification

Verification means the plan's every exam code matched the live
catalog on the stated date, each ladder step has its description
document archived, and the role-to-entry-exam choice is defended in
two sentences.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] D-code grammar internalized (portfolio x function x series)
- [ ] ISM/CIS foundations positioned and chosen by role
- [ ] Exam-description documents located for one full ladder
- [ ] Program map produced with same-day code verification
