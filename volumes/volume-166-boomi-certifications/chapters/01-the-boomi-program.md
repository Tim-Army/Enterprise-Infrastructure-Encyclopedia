# Chapter 01: The Boomi Certification Program

## Learning Objectives

- Describe Boomi as the iPaaS pioneer and where certification fits.
- Map the certification tracks — Developer, Administrator, Architect, API Management, Data Hub, Flow, B2B/EDI.
- Understand the Associate → Professional progression.
- Recognize the exam mechanics — open-book, open-platform, no time limit, course-backed, $125.

*Cert relevance: this chapter frames the whole program — the tracks, the levels, and the exam format the rest of the volume develops.*

## Boomi and its certifications

**Boomi** is the **iPaaS pioneer** — the company that coined **AtomSphere** and helped define **Integration Platform as a Service**: a cloud-native, low-code platform for connecting **applications, data, people, and devices**. When an enterprise needs to wire together dozens of SaaS apps, on-premises systems, databases, and trading partners — and do it **visually and fast** rather than hand-coding integrations — Boomi is one of the names that does it. Its platform is the **Boomi Enterprise Platform** (formerly AtomSphere), and its signature is the **Atom** runtime ([Ch 3](03-atoms-molecules-atom-clouds.md)). Boomi was **Dell Boomi** until it became independent in 2021.

Boomi certifications are delivered through the **Boomi Training & Certification** portal (`train.boomi.com`) and are organized by **platform service and role**. You certify on the service you work with — integration, API management, master data, EDI, low-code apps — at a level that matches your role. Because Boomi is a broad platform, the certification catalog is broad too. The lab builds the track map.

## The certification tracks

Boomi's certifications span the platform's services and roles:

| Track | Certifications |
| --- | --- |
| **Integration Developer** | Associate Integration Developer · Professional Integration Developer ([Ch 4](04-building-integrations.md)) |
| **Administrator** | Associate Administrator · Professional Windows Operational Administrator · Professional Linux Operational Administrator ([Ch 8](08-administration-and-architecture.md)) |
| **Architect** | Associate Integration Architect · Associate Runtime Architect ([Ch 8](08-administration-and-architecture.md)) |
| **API Management** | Professional API Design · Professional API Management ([Ch 5](05-api-management.md)) |
| **Data Hub (MDM)** | Associate Data Hub · Professional Data Hub Developer ([Ch 6](06-data-hub-mdm.md)) |
| **Flow (low-code apps)** | Associate Flow Essentials ([Ch 7](07-b2b-edi-and-flow.md)) |
| **B2B/EDI** | Associate EDI for X12 ([Ch 7](07-b2b-edi-and-flow.md)) |

The **Integration Developer** track is the flagship and the natural starting point. The other tracks specialize into the platform's services. **Boomi AI** (Companion, Agentstudio, Boomi GPT, [Ch 8](08-administration-and-architecture.md)) has training but no dedicated certification yet. The lab assembles the track map.

## Associate and Professional levels

Most tracks follow an **Associate → Professional** progression:

- **Associate** — validates **foundational** knowledge and skills for the service (Associate Integration Developer, Associate Data Hub, Associate Flow Essentials). The entry credential.
- **Professional** — validates **advanced** skills and real-world competency (Professional Integration Developer, Professional API Management, Professional Data Hub Developer). The deeper credential.

Each certification is paired with a **required course** — for example, the Integration Developer path runs *Integration Essentials* → *Associate Integration Developer* (course + cert) → *Professional Integration Developer* (course + cert) → *Implementation Readiness*. Start Associate, then climb to Professional in the track your role centers on. The lab models the level progression.

## Exam mechanics

Boomi certification exams share a distinctive, practical format:

- **Open-book and open-platform.** You may consult documentation **and the Boomi platform itself** during the exam — the test is about **applying** knowledge, not memorizing it.
- **No time limit.** You work at your own pace.
- **Question types:** multiple-choice and multiple-response, and **some exams include a practical section** — a multiple-choice section where you **apply concepts in the Boomi platform** to determine the correct answers.
- **Course-backed.** Each exam is tied to a required course (self-paced on-demand; instructor-led training is also available for purchase).
- **Fee: $125** per exam. You register on the training portal and choose when and where to take it.

The open-book, open-platform, hands-on style reflects Boomi's philosophy: certification should prove you can **do the work on the platform**, not recall trivia. The lab records the mechanics. *(This differs from closed-book, timed, weighted-blueprint exams — Boomi has no percentage domain weights; the required course is the blueprint.)*

## Hands-On Lab

Python models the program: the tracks, the levels, and the exam mechanics. **Cost:** none.

### Lab 1.1 — Map the tracks and levels

**Objective:** Record the Boomi certification tracks and the Associate → Professional progression.

```bash
python3 - <<'EOF'
TRACKS = {
  "Integration Developer": ["Associate Integration Developer", "Professional Integration Developer"],
  "Administrator":         ["Associate Administrator", "Professional Windows Operational Administrator",
                            "Professional Linux Operational Administrator"],
  "Architect":             ["Associate Integration Architect", "Associate Runtime Architect"],
  "API Management":        ["Professional API Design", "Professional API Management"],
  "Data Hub (MDM)":        ["Associate Data Hub", "Professional Data Hub Developer"],
  "Flow (low-code apps)":  ["Associate Flow Essentials"],
  "B2B/EDI":               ["Associate EDI for X12"],
}
print("BOOMI CERTIFICATION TRACKS (train.boomi.com):\n")
total = 0
for track, certs in TRACKS.items():
    print(f"   {track}")
    for c in certs:
        level = "Associate" if c.startswith("Associate") else "Professional"
        print(f"      [{level:12}] {c}")
        total += 1
    print()
print(f"   {total} certifications across {len(TRACKS)} tracks.")
print("   Boomi AI (Companion / Agentstudio / GPT): training only, no cert yet.")
print()
print("Certify on the SERVICE you work with, at the LEVEL that matches your role.")
print("Integration Developer is the flagship starting track; the rest specialize.")
EOF
```

**Expected result:** A track map listing Boomi's certifications across seven tracks (Integration Developer, Administrator, Architect, API Management, Data Hub, Flow, B2B/EDI), each labeled Associate or Professional, with a note that Boomi AI is training-only. The lesson is that Boomi certifications are organized by platform service and role, you certify on the service you use, and Integration Developer is the flagship starting track.

**Cleanup:** None.

### Lab 1.2 — Record the exam mechanics

**Objective:** Capture Boomi's distinctive open-book, open-platform exam format.

```bash
python3 - <<'EOF'
MECHANICS = {
  "format":        "open-book AND open-platform (consult docs + the Boomi platform)",
  "time_limit":    "none (work at your own pace)",
  "questions":     "multiple-choice + multiple-response",
  "practical":     "some exams add a practical section — apply concepts in the platform",
  "prerequisite":  "a required course (self-paced on-demand; ILT also available)",
  "fee":           "$125 per exam (register on the training portal)",
  "blueprint":     "no percentage domain weights — the required COURSE is the blueprint",
}
print("BOOMI EXAM MECHANICS (all certifications):\n")
for k, v in MECHANICS.items():
    print(f"   {k:12}: {v}")
print()
print("The OPEN-BOOK, OPEN-PLATFORM, hands-on style reflects Boomi's philosophy: prove you")
print("can DO THE WORK on the platform, not recall trivia. There is no timer and no weighted")
print("blueprint — you take the required course, then apply it, with the platform open.")
EOF
```

**Expected result:** A record of Boomi's exam mechanics — open-book and open-platform, no time limit, multiple-choice/multiple-response plus an optional practical section, course-backed, $125, with no weighted blueprint. The lesson is that Boomi certification proves applied, hands-on competency on the live platform rather than closed-book recall, and the required course is the effective blueprint.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Boomi placed — the iPaaS pioneer; the Boomi Enterprise Platform (formerly AtomSphere).
- [ ] The tracks mapped — Developer, Administrator, Architect, API Management, Data Hub, Flow, B2B/EDI.
- [ ] The Associate → Professional progression understood — foundational then advanced, course-paired.
- [ ] The exam mechanics recorded — open-book, open-platform, no time limit, course-backed, $125.

## See also

- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — the closest integration-platform peer.
- [Volume CLXV — Informatica](../../volume-165-informatica-certifications/README.md) — data management and Cloud Application Integration, an adjacent space.
- [Chapter 02 — The Boomi Enterprise Platform](02-the-boomi-platform.md).
