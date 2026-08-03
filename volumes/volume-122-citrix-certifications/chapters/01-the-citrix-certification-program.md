# Chapter 01: The Citrix Certification Program

![Citrix certification program: two tracks under Cloud Software Group. The Virtualization track runs CCA-V to CCP-V on Citrix Virtual Apps and Desktops; the App Delivery and Security track runs CCA-AppDS (two exam options, Gateway or Traffic Management) to CCP-AppDS on NetScaler 14.x. Exams are delivered on Webassessor, the Expert tier is discontinued, and the program is under an announced overhaul.](../../../diagrams/volume-122-citrix-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The current Citrix program: two tracks, two levels each, five exams total — and an explicitly announced overhaul in progress, which makes verification-before-scheduling part of the study plan itself.*

## Learning Objectives

- Describe the current Citrix certification program under Cloud Software Group: two tracks, five exams.
- Know what was retired: the Expert tier (CCE-V, CCE-N), the 1Y0-204 exam, and the old exam-code system.
- Understand exam logistics: Webassessor/Kryterion delivery, formats, languages, and prerequisites.
- Plan verification-first study: the program is mid-overhaul, so re-check before scheduling.

## The program today

Citrix certifications are run by **Cloud Software Group (CSG)**, the company formed from Citrix and TIBCO after the 2022 take-private. Two product families anchor the program:

- **Citrix Virtual Apps and Desktops (CVAD)** — application and desktop virtualization; the **Virtualization** track.
- **NetScaler** — application delivery and security (the product returned to its NetScaler name after years as "Citrix ADC"); the **App Delivery and Security (AppDS)** track.

The certification ladder has two levels per track:

| Certification | Level | Exam | Prerequisite |
|:---|:---|:---|:---|
| **CCA-V** | Associate | Citrix Virtual Apps and Desktops Administration | None |
| **CCP-V** | Professional | Citrix Virtual Apps and Desktops 7 Advanced Administration | CCA-V |
| **CCA-AppDS** (Gateway option) | Associate | NetScaler 14.x Essentials and NetScaler Gateway | None |
| **CCA-AppDS** (Traffic Management option) | Associate | Deploy and Manage Citrix ADC 14.x with Traffic Management | None |
| **CCP-AppDS** | Professional | 1Y0-342: NetScaler Advanced Topics — Security, Management and Optimization | Either CCA-AppDS exam |

Two structural notes:

- **CCA-AppDS is one certification with two exam options.** Pass either the Gateway exam or the Traffic Management exam and you hold CCA-AppDS; either one satisfies the CCP-AppDS prerequisite.
- **Only CCP-AppDS still carries a legacy exam code** (1Y0-342). The other exams are named, not numbered — the old 1Y0-numbering system is being phased out with the platform move.

## What was retired

- **The Expert tier is gone.** CCE-V (Citrix Certified Expert — Virtualization) and CCE-N (Networking) are discontinued; the ladder now tops out at Professional.
- **1Y0-204 is retired.** The CCA-V exam ("Citrix Virtual Apps and Desktops Administration") is its stated replacement, refocused on real-world scenarios and hands-on skills.
- **The old training/exam platforms were replaced.** Exams moved to **Webassessor** (Kryterion); `training.citrix.com` no longer resolves. Existing certification holders recover their records on the new platform with their certification email plus a password reset.

## The overhaul warning

The official program page states, verbatim in intent: the Citrix and NetScaler certification programs are **undergoing a comprehensive overhaul to better align with the product roadmap, with additional certifications planned**. Treat this volume's tables as verified on **3 August 2026** — and before scheduling an exam, re-verify the certification list and exam names on the official pages, because a mid-overhaul program can add, rename, or retire exams with little notice.

## Exam logistics

| Fact | Value |
|:---|:---|
| Delivery | Webassessor (Kryterion), proctored |
| CCA-V format | ~60–65 questions, 90 minutes, ~65% passing, English |
| CCP-V format | 60–70 questions, 64% minimum passing |
| AppDS exams format | 60–70 questions per form, ~10% performance-based items, English + Japanese |
| Reference materials | None allowed in any exam |
| Digital badge | Credly |

The AppDS exams are notable for **performance-based items** (about 10% of the form) and, on the Traffic Management exam, **CLI-environment simulations** — hands-on NetScaler CLI fluency is examined, not just recall. That is why every AppDS chapter in this volume drills the `add/set/show/bind` CLI shapes.

## Hands-On Lab

### Lab 1.1 — Verify the program before you rely on it

**Objective:** Practice the verification-first habit the overhaul makes mandatory.

```bash
curl -s https://www.citrix.com/training-and-certifications/ | tr -s ' \n' ' ' | grep -o "Citrix Certified [A-Za-z– ]*" | sort -u
```

**Expected result:** The current certification names, straight from the official page — compare against the table above; any difference means the overhaul moved and this volume's map needs re-checking against the source.

**Negative test:** Search a third-party training site for "Citrix certification list" — many still show CCE-V, 1Y0-204, or CCA-N. Stale mirrors are the norm mid-overhaul; only citrix.com, netscaler.com, and Webassessor are authoritative.

**Cleanup:** None.

### Lab 1.2 — Locate the exam prep guides

**Objective:** Download the five official exam prep guides — the closest thing the program has to public blueprints.

```bash
base="https://www.citrix.com/content/dam/citrix61/en_us/documents/exam-prep-guides"
for g in citrix-certified-associate-virtualization-cca-v-exam-prep-guide \
         citrix-certified-professional-virtualization-ccp-v-exam-prep-guide_updated \
         citrix-certified-associate-app-delivery-and-security-cca-appds-gateway-exam-prep-guide \
         citrix-certified-associate-app-delivery-and-security-cca-appds-traffic-management-exam-prep-guide \
         citrix-certified-professional-appds-exam-prep-guide; do
  curl -sL -A "Mozilla/5.0" -o "$g.pdf" "$base/$g.pdf"; head -c4 "$g.pdf"; echo "  $g"
done
```

**Expected result:** Five files each starting `%PDF` — the official guides (updated 15 September 2025 as of this writing), each listing the exam's modules and recommended course.

**Negative test:** Fetch without the browser user-agent or use an old `1Y0-204` guide URL — you get an HTML soft-404 a few hundred bytes long, not a PDF. Check the magic bytes, not just the HTTP status.

**Cleanup:** Keep the PDFs for the track chapters.

## Summary and Completion Checklist

- [ ] Two tracks, five exams, two levels — and no Expert tier — internalized.
- [ ] Retirements known: CCE-V/CCE-N, 1Y0-204, the old platforms.
- [ ] Exam logistics known, including the AppDS performance-based items.
- [ ] Verification-first habit practiced; prep guides downloaded.
