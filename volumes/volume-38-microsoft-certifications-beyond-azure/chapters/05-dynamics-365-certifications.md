# Chapter 05: Dynamics 365 Certifications

## Learning Objectives

- Distinguish the Dynamics 365 Customer Engagement and Finance and Operations tracks.
- Enumerate the current MB-family certifications and exam codes.
- Explain the relationship between Dynamics functional exams and Power Platform.
- Recognize the newer AI-oriented Dynamics credentials.
- Build a study path for a Dynamics 365 functional consultant or architect.

## Theory and Architecture

**Dynamics 365** is Microsoft's business-applications suite, split into two
worlds. **Customer Engagement (CE)** — Sales, Customer Service, Field Service,
Customer Insights — is built on **Dataverse** and the **Power Platform**, so
its functional exams relate closely to the PL family. **Finance and
Operations (F&O)** — Finance, Supply Chain Management, Commerce — is the ERP
side with its own developer and architect exams. The **MB** family certifies
functional consultants, developers, and architects across both.

As verified on Microsoft Learn (26 July 2026), current MB credentials
include the **Fundamentals** pair — **MB-910** (Dynamics 365 Fundamentals,
Customer Engagement apps / CRM) and **MB-920** (Dynamics 365 Fundamentals,
Finance and Operations apps / ERP) — and functional/developer/architect
credentials such as:

- **Customer Service Functional Consultant** — **MB-230** (Associate).
- **Field Service Functional Consultant** — **MB-240** (Associate).
- **Customer Experience Analyst** — **MB-280** (Associate; the evolution of
  the Sales/Marketing functional line).
- **Supply Chain Management Functional Consultant** — **MB-330** (Associate),
  with the **Manufacturing** variant on **MB-300 + MB-320** and the **Expert**
  on **MB-335**.
- **Commerce Functional Consultant** — **MB-300 + MB-340** (Associate).
- **Finance and Operations Apps Developer** — **MB-500** (Associate).
- **Finance and Operations Apps Solution Architect Expert** — **MB-700**
  (Expert).
- **Business Central Functional Consultant** — **MB-800** (Associate) — and
  **Business Central Developer** — **MB-820** (Associate).

Newer **AI-oriented** Dynamics credentials have appeared — for example a
**Dynamics 365 Sales AI Consultant** and a **Dynamics 365 Contact Center AI
Engineer** (beta) — reflecting Copilot's spread into business apps. Confirm
these on Learn, as several are beta or recently added. **MB-901** (an older
Fundamentals exam) and **MB-600** (the CE + Power Platform Solution Architect,
whose scope moved to **PL-600**) are retired.

## Design Considerations

Choose the **track** first. A **CE** consultant works in Sales/Service/Field
Service/Customer Insights on Dataverse and Power Platform, so their path
crosses the **PL** family (Chapter 04) — historically a CE functional
credential paired a Dynamics MB exam with **PL-200**. An **F&O** professional
works in Finance/SCM/Commerce, with **MB-500** (developer) and **MB-700**
(architect Expert). **Business Central** is a distinct small-and-mid-market ERP
with its own **MB-800/MB-820**.

Sequence **MB-910 (CRM) or MB-920 (ERP) Fundamentals → the role's Associate →
the Expert architect (MB-700 for F&O, or PL-600 for CE + Power Platform)**.
Watch the **AI additions** — Copilot-driven roles are being certified, and
several are beta.

## Implementation and Automation

Verify the fundamentals and a functional exam from Microsoft Learn:

```bash
for slug in d365-fundamentals-customer-engagement-apps-crm \
            d365-fundamentals-finance-and-operations-apps-erp \
            d365-functional-consultant-supply-chain-management \
            d365-fundamentals; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bMB-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> ${code:-'(assessment/beta - see page)'}"
done
# d365-functional-consultant-supply-chain-management -> MB-330
```

## Validation and Troubleshooting

Map the main credentials to tracks:

| Credential | Exam(s) | Track |
| --- | --- | --- |
| D365 Fundamentals (CRM) | MB-910 | Customer Engagement |
| D365 Fundamentals (ERP) | MB-920 | Finance and Operations |
| Customer Service Functional Consultant | MB-230 | CE |
| Field Service Functional Consultant | MB-240 | CE |
| Customer Experience Analyst | MB-280 | CE |
| Supply Chain Management FC | MB-330 (Expert MB-335) | F&O |
| Commerce Functional Consultant | MB-300 + MB-340 | F&O |
| F&O Apps Developer | MB-500 | F&O |
| F&O Apps Solution Architect Expert | MB-700 | F&O |
| Business Central Functional Consultant / Developer | MB-800 / MB-820 | BC |

Common pitfalls: studying **MB-901** or **MB-600** (retired); missing that CE
functional roles overlap **Power Platform** (PL-200/PL-600); assuming a single
exam where a credential needs two (Commerce and some SCM paths pair **MB-300**
with a specialty exam); and overlooking the **beta AI** Dynamics credentials.
Confirm every code on Learn — the Dynamics family is large and changes often.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
practice in a **Dynamics 365 trial** environment. Because the CE track leans
on **Power Platform**, plan MB and PL together; because F&O is its own world,
keep that path separate. Confirm the **shared-exam** structures (MB-300 pairs)
and the **AI/beta** additions on Learn before committing. Renew annually
through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for MB-910, MB-920, MB-230, MB-240, MB-280, MB-330/335, MB-500, MB-700, MB-800, MB-820.
- Cross-reference: [Chapter 04 — Power Platform](04-power-platform-certifications.md).

**Knowledge checks**

1. What is the difference between the CE and F&O tracks, and why does CE overlap Power Platform?
2. Which two Fundamentals exams anchor the Dynamics family?
3. Which retired Dynamics architect exam had its scope moved to PL-600?

## Hands-On Lab

Exam-preparation walkthroughs for the Dynamics 365 family.

**Shared prerequisites for Labs 5.1–5.2** — a browser; `curl` for Lab 5.1.
**Cost:** none.

### Lab 5.1 — Identify the two Fundamentals tracks (Topic: Verify the family)

**Objective:** Confirm the CRM/ERP split.

```bash
for slug in d365-fundamentals-customer-engagement-apps-crm d365-fundamentals-finance-and-operations-apps-erp; do
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oiE 'MB-9[0-9]{2}' | sort -u | tr '\n' ' '; echo " <- $slug"
done
```

**Expected result:** the CRM Fundamentals (MB-910) and ERP Fundamentals
(MB-920) pages — the two gateways into the Dynamics family. (If a page renders
the code only in script, read it in the browser — the split itself is the
point.)

**Negative test:** search for MB-901; it is the retired single Fundamentals
exam, superseded by the MB-910/MB-920 split.

**Cleanup:** none.

### Lab 5.2 — Plan a Dynamics path (Topic: Study plan)

**Objective:** Sequence for an F&O solution architect.

```text
MB-920 (ERP Fundamentals)
  -> MB-330 (Supply Chain Management) or MB-500 (F&O Developer)
  -> MB-700 (F&O Solution Architect Expert).
For a CE architect instead: MB-910 -> MB-230/MB-280 (+ PL-200) -> PL-600.
```

**Expected result:** a Fundamentals→Associate→Expert path that respects the
CE-vs-F&O split and the Power Platform overlap.

**Negative test:** mix CE and F&O exams into one path expecting them to
compound; they are different products — choose a track.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Dynamics 365 splits into Customer Engagement (Dataverse/Power Platform) and
Finance and Operations (ERP), anchored by the MB-910/MB-920 Fundamentals. The
MB family certifies functional consultants, developers (MB-500/MB-820), and
architects (MB-700), with CE roles overlapping Power Platform (PL-200/PL-600)
and a wave of new Copilot/AI Dynamics credentials. MB-901 and MB-600 retired.

- [ ] I can distinguish the CE and F&O tracks.
- [ ] I can list the main MB credentials and their exams.
- [ ] I understand the Power Platform overlap and the AI additions.
- [ ] I can build a Dynamics study path within a track.
- [ ] I completed Labs 5.1–5.2 including each negative test.
