# Chapter 04: Power Platform Certifications

## Learning Objectives

- Enumerate the current Power Platform certifications and exam codes.
- Distinguish the maker, developer, analyst, RPA, and architect roles.
- Recognize the PL retirements and the shared-exam relationships with Dynamics 365.
- Map each credential to the underlying Power Platform skills.
- Build a study path for a Power Platform functional or developer role.

## Theory and Architecture

**Power Platform** is Microsoft's low-code suite — **Power Apps**, **Power
Automate**, **Power BI**, **Power Pages**, and **Copilot Studio** — over
**Dataverse**. The **PL** certification family certifies the roles that build
and govern it. As verified on Microsoft Learn (26 July 2026):

- **Microsoft Certified: Power Platform Fundamentals** — exam **PL-900**
  (Fundamentals). The platform's capabilities, Dataverse, and business value.
- **Microsoft Certified: Power Platform Functional Consultant Associate** —
  exam **PL-200** (Associate). Configure Dataverse, apps, automation, and
  Copilot Studio to meet requirements. *Verify status — this credential was
  flagged for change in 2026.*
- **Microsoft Certified: Power BI Data Analyst Associate** — exam **PL-300**
  (Associate). Model, visualize, and analyze data with Power BI.
- **Microsoft Certified: Power Platform Developer Associate** — exam
  **PL-400** (Associate). Extend Power Platform with code — plug-ins, custom
  connectors, and PCF controls.
- **Microsoft Certified: Power Automate RPA Developer Associate** — exam
  **PL-500** (Associate). Robotic process automation with Power Automate
  desktop flows.
- **Microsoft Certified: Power Platform Solution Architect Expert** — exam
  **PL-600** (Expert). Lead the design of Power Platform and Dynamics 365
  solutions end to end.

**PL-100** (App Maker) was retired, and **PL-200** overlaps the **Dynamics
365** functional-consultant credentials, which historically paired a
Dynamics MB exam with PL-200. Confirm the current shared-exam structure on
Learn.

## Design Considerations

Choose by role. **PL-900** is the gateway. Makers and functional consultants
target **PL-200**; **PL-300** is the widely held **Power BI** analyst
credential (relevant well beyond Power Platform teams and overlapping the data
family, Chapter 06); pro-code developers take **PL-400**; automation
specialists take **PL-500**; and solution architects lead with **PL-600**
(Expert), which spans Power Platform *and* Dynamics 365 (Chapter 05).

Because **PL-600** and the Dynamics architect credential (MB-700) both
certify solution architecture, decide which platform centre of gravity the
role has. **PL-300** is a strong standalone analyst credential and a natural
companion to the data and Fabric certifications (Chapter 06).

## Implementation and Automation

Verify the PL family from Microsoft Learn:

```bash
for slug in power-platform-fundamentals power-platform-functional-consultant-associate \
            data-analyst-associate power-platform-developer-associate \
            power-automate-rpa-developer-associate power-platform-solution-architect-expert; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bPL-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# power-platform-functional-consultant-associate -> PL-200 (confirm status)
# data-analyst-associate -> PL-300   (Power BI Data Analyst)
```

## Validation and Troubleshooting

Map credentials to roles and tiers:

| Credential | Exam | Tier | Role |
| --- | --- | --- | --- |
| Power Platform Fundamentals | PL-900 | Fundamentals | Gateway |
| Functional Consultant | PL-200 | Associate | Maker/consultant |
| Power BI Data Analyst | PL-300 | Associate | Analyst |
| Power Platform Developer | PL-400 | Associate | Pro-code developer |
| Power Automate RPA Developer | PL-500 | Associate | Automation |
| Power Platform Solution Architect | PL-600 | Expert | Architect |

Common pitfalls: preparing for **PL-100** (retired); assuming **PL-200** and
the Dynamics functional exams are unrelated (they overlap, and shared-exam
structures change — verify on Learn); and treating **PL-300** as
Power-Platform-only when it is really the general **Power BI** analyst
credential relevant to any data role.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
build in a free **Power Platform developer environment**. Verify **PL-200**'s
current status and any shared-exam relationship with Dynamics 365 before
planning a functional-consultant path. Treat **PL-300** as a cross-family
analyst credential. Renew annually through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for PL-900, PL-200, PL-300, PL-400, PL-500, PL-600.

**Knowledge checks**

1. Which PL credential is the widely held Power BI analyst certification?
2. What does PL-600 span beyond Power Platform?
3. Which PL exam was retired?

## Hands-On Lab

Exam-preparation walkthroughs for the Power Platform family.

**Shared prerequisites for Labs 4.1–4.2** — a browser; `curl` for Lab 4.1.
**Cost:** none.

### Lab 4.1 — Confirm the PL family (Topic: Verify the family)

**Objective:** Prove the current codes and roles.

```bash
for slug in power-platform-fundamentals data-analyst-associate power-platform-solution-architect-expert; do
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bPL-[0-9]{3}\b' | sort -u | tr '\n' ' '; echo " <- $slug"
done
```

**Expected result:** PL-900, PL-300, and PL-600 respectively — the analyst
credential is PL-300 under the "data-analyst" slug.

**Negative test:** search for PL-100; the App Maker exam is retired and not
listed.

**Cleanup:** none.

### Lab 4.2 — Plan a Power Platform path (Topic: Study plan)

**Objective:** Sequence for a functional consultant becoming an architect.

```text
PL-900 (Fundamentals) -> PL-200 (Functional Consultant)
  -> PL-400 (Developer) for pro-code, or PL-300 (Power BI) for analytics
  -> PL-600 (Solution Architect Expert), which also spans Dynamics 365 (Ch 05).
```

**Expected result:** a Fundamentals→Associate→Expert path with a clear branch
by specialization.

**Negative test:** jump to PL-600 with no functional-consultant experience;
the architecture exam assumes deep platform and Dynamics fluency.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Power Platform family runs PL-900 (Fundamentals), PL-200 (Functional
Consultant), PL-300 (Power BI Data Analyst), PL-400 (Developer), PL-500 (RPA
Developer), and PL-600 (Solution Architect Expert). PL-100 retired; PL-200 and
PL-600 overlap Dynamics 365; PL-300 is the cross-family analyst credential.

- [ ] I can list the PL credentials and exam codes.
- [ ] I can distinguish the maker, developer, analyst, RPA, and architect roles.
- [ ] I know PL-100 retired and PL-200/PL-600 relate to Dynamics.
- [ ] I can build a Power Platform study path.
- [ ] I completed Labs 4.1–4.2 including each negative test.
