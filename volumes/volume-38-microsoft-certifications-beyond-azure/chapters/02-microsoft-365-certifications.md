# Chapter 02: Microsoft 365 Certifications

## Learning Objectives

- Enumerate the current Microsoft 365 certifications and their exam codes.
- Distinguish the Fundamentals, Administrator Expert, and specialist credentials.
- Map each credential to the hands-on skills in Volume XXXVII.
- Recognize the Microsoft 365 exams that were retired or renumbered.
- Build a study path for a Microsoft 365 administrator role.

## Theory and Architecture

The **Microsoft 365** family certifies the roles that run the modern-work
cloud — administration, endpoints, and collaboration. As verified on
Microsoft Learn (26 July 2026), the current credentials are:

- **Microsoft 365 Certified: Fundamentals** — exam **MS-900** (Fundamentals).
  Cloud concepts, the Microsoft 365 services, security/compliance basics, and
  licensing. The gateway to the family.
- **Microsoft 365 Certified: Administrator Expert** — exam **MS-102**
  (Expert). Tenant, identity, security, and compliance administration across
  the suite; the senior M365 administration credential.
- **Microsoft 365 Certified: Endpoint Administrator Associate** — exam
  **MD-102** (Associate). Deploy and manage Windows and endpoints with
  Intune: enrollment, compliance, configuration, apps, and Autopilot.
- **Microsoft 365 Certified: Teams Administrator Associate** — exam **MS-700**
  (Associate). Manage Teams: policies, teams and channels, meetings, and the
  app catalog.
- **Microsoft 365 Certified: Collaboration Communications Systems Engineer
  Associate** — exam **MS-721** (Associate). Teams Phone and meeting-room
  voice engineering.

Several older Microsoft 365 exams have **retired or been folded in**: MS-100
and MS-101 (the two-exam Enterprise Administrator that MS-102 replaced),
MS-500 (Security Administrator, moved into the SC family), MS-203 (Messaging
Administrator), MS-700's older siblings, and MS-720 (Teams Voice Engineer
Expert, whose scope moved to the MS-721 Associate). Always confirm status on
Microsoft Learn.

## Design Considerations

For a **Microsoft 365 administrator**, the path is **MS-900 → MS-102**, with
**MD-102** if the role owns endpoints and **MS-700/MS-721** if it owns Teams
and voice. MS-102 is labelled **Expert** and is broad — tenant, identity,
security, and compliance — so it rewards real administrative experience and
the identity/security depth of the SC family (Chapter 03). Endpoint-focused
staff should prioritize **MD-102**, which maps directly to the Intune,
compliance, configuration, app, and Autopilot skills in Volume XXXVII
(Chapters 05–07). Voice engineers add **MS-721** on top of **MS-700**.

Because Microsoft 365 security overlaps the SC family, plan them together: an
M365 administrator often pairs **MS-102** with **SC-300** (identity) and
**SC-401** (information security), and a security-operations focus adds
**SC-200**.

## Implementation and Automation

Verify the family and codes from Microsoft Learn:

```bash
for slug in microsoft-365-fundamentals m365-administrator-expert modern-desktop \
            m365-teams-administrator-associate m365-collaboration-communications-systems-engineer; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\b(MS|MD)-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# -> microsoft-365-fundamentals -> MS-900
# -> m365-administrator-expert -> MS-102
# -> modern-desktop -> MD-102
# -> m365-teams-administrator-associate -> MS-700
# -> m365-collaboration-communications-systems-engineer -> MS-721
```

## Validation and Troubleshooting

Map each credential to its skills-measured blueprint on Learn, then to
hands-on practice:

| Credential | Exam | Practice in |
| --- | --- | --- |
| M365 Fundamentals | MS-900 | Vol XXXVII Ch 01 |
| M365 Administrator Expert | MS-102 | Vol XXXVII Ch 01–04, 08–11 |
| Endpoint Administrator | MD-102 | Vol XXXVII Ch 05–07 |
| Teams Administrator | MS-700 | Vol XXXVII Ch 09 |
| Collaboration Communications Systems Engineer | MS-721 | Vol XXXVII Ch 09 |

Common pitfalls: preparing for **MS-100/MS-101** (retired — MS-102 is the
current single exam); expecting **MS-500** here (it moved into the SC family
and was itself retired); and underestimating **MS-102**'s breadth because it
is a single exam — it still spans tenant, identity, security, and compliance
at Expert depth.

## Security and Best Practices

Prepare with the **Microsoft Learn** learning paths and the **free practice
assessment** for each exam, and get hands-on in a **Microsoft 365 Developer**
tenant (Volume XXXVII). Verify the **current exam code** before studying —
the M365 family has renumbered more than once. Pair M365 credentials with the
**SC** identity and security exams for a complete administrator profile, and
renew on time through the free annual assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for MS-900, MS-102, MD-102, MS-700, MS-721.
- Cross-reference: [Volume XXXVII — Microsoft 365 and Modern Work](../volume-37-microsoft-365-modern-work/README.md).

**Knowledge checks**

1. Which single exam replaced the two-exam MS-100/MS-101 Enterprise Administrator?
2. Which credential maps to Intune, compliance, and Autopilot?
3. Why plan Microsoft 365 and SC credentials together?

## Hands-On Lab

Exam-preparation walkthroughs for the Microsoft 365 family.

**Shared prerequisites for Labs 2.1–2.2** — a browser; `curl` for Lab 2.1.
**Cost:** none.

### Lab 2.1 — Confirm the M365 exam codes (Topic: Verify the family)

**Objective:** Prove the current codes from Learn.

```bash
for slug in microsoft-365-fundamentals m365-administrator-expert modern-desktop; do
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\b(MS|MD)-[0-9]{3}\b' | sort -u | tr '\n' ' '; echo " <- $slug"
done
```

**Expected result:** MS-900, MS-102, and MD-102 respectively — verified codes,
not memory.

**Negative test:** search for "MS-101" on the Endpoint Administrator page; it
is not there — MS-101 is retired.

**Cleanup:** none.

### Lab 2.2 — Build an M365 administrator path (Topic: Study plan)

**Objective:** Sequence the family for a real role.

```text
Endpoint-and-tenant administrator:
  MS-900 (Fundamentals) -> MD-102 (Endpoint) -> MS-102 (Administrator Expert)
  + SC-300 (Identity) for the security half of MS-102.
Map to Vol XXXVII: Ch 01 (tenant), Ch 05–07 (endpoints), Ch 02–04 (identity),
Ch 08–11 (workloads, compliance, protection).
```

**Expected result:** a Fundamentals→Associate→Expert path anchored to hands-on
chapters — the deliberate order for the M365 role.

**Negative test:** attempt MS-102 first with no tenant experience; its
identity/security/compliance breadth is punishing without the Associate and SC
groundwork.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Microsoft 365 family runs MS-900 (Fundamentals), MS-102 (Administrator
Expert), MD-102 (Endpoint Administrator), and MS-700/MS-721 (Teams and voice).
Older exams (MS-100/101, MS-500, MS-203, MS-720) retired or folded in. The
credentials map directly to the hands-on skills of Volume XXXVII and pair
naturally with the SC family.

- [ ] I can list the current M365 credentials and exam codes.
- [ ] I can map each to hands-on practice in Volume XXXVII.
- [ ] I know which older M365 exams retired.
- [ ] I can build an M365 administrator study path.
- [ ] I completed Labs 2.1–2.2 including each negative test.
