# Chapter 01: The Azure Certification Program — Levels, Codes, and Renewal

## Learning Objectives

- Map Microsoft's Azure certification program: four levels
  (fundamentals, associate, expert, specialty) and the role-based design
  that organizes them
- Read an exam code — the `AZ`, `AI`, `DP`, `SC`, and new `AB` families —
  and know what each signals about subject area
- Explain Microsoft's annual renewal model and how it differs from the
  fixed multi-year expiry used by most vendors
- Identify which certifications are current, which are retiring on a
  published date, and which are already retired
- Locate the authoritative source for any Azure exam's code and status,
  and understand why this program in particular resists memorization

## Theory and Architecture

### Four levels, organized by role

Microsoft organizes Azure certifications into **fundamentals**,
**associate**, **expert**, and **specialty** levels. As with AWS
(Volume XVII), the levels describe assumed depth rather than a required
sequence — **no Azure certification formally requires another**, though
Microsoft "strongly recommends" specific prerequisites on several pages
(the SAP Workloads specialty recommends Azure Administrator, for
instance). Recommendation is not a gate.

What distinguishes Microsoft's program is that it is **role-based by
construction**. Each certification is written against a job role —
administrator, developer, network engineer, solutions architect — and
Microsoft reorganizes the lineup when the roles themselves change. That is
not a hypothetical: the program is in the middle of exactly such a
reorganization as this volume is written, and Chapters 05 and 06 are
about it.

### Reading the exam code

The letter prefix identifies the subject family, not the level:

| Prefix | Family | Examples |
| --- | --- | --- |
| `AZ` | Core Azure platform | AZ-900, AZ-104, AZ-305, AZ-400 |
| `AI` | Artificial intelligence | AI-901, AI-103, AI-200 |
| `DP` | Data platform | DP-900, DP-300, DP-420, DP-750 |
| `SC` | Security, compliance, identity | SC-100, SC-200, SC-300 |
| `AB` | AI agent building | AB-620 |

The **`AB` family is new** — introduced with the AI Agent Builder
Associate certification (Chapter 06) — and its arrival is a useful signal
in itself: Microsoft creates a code family when it believes a job role has
become distinct enough to certify separately.

The number carries a rough convention: `-900` series are fundamentals,
`-100`/`-200` series are associate, `-300`/`-400` series expert, and
higher numbers tend to be specialty. Treat this as a pattern, not a rule —
AI-103 and AI-200 are both associate.

### The current lineup

Verified against Microsoft Learn on **23 July 2026**. Chapters 02 through
09 cover these in depth.

| Level | Certification | Exam | Status |
| --- | --- | --- | --- |
| Fundamentals | Azure Fundamentals | AZ-900 | Current |
| Fundamentals | Azure AI Fundamentals | AI-901 | Current (replaced AI-900) |
| Fundamentals | Azure Data Fundamentals | DP-900 | Current |
| Associate | Azure Administrator | AZ-104 | Current |
| Associate | Azure Network Engineer | AZ-700 | Current |
| Associate | Azure Database Administrator | DP-300 | Current |
| Associate | Azure Developer | AZ-204 | **Retires 31 July 2026** |
| Associate | Azure Security Engineer | AZ-500 | **Retires 31 August 2026** |
| Associate | Azure AI Engineer | AI-102 | **Retired** |
| Associate | Azure Data Scientist | DP-100 | **Retired** |
| Associate | Azure AI Apps and Agents Developer | AI-103 | Current (new) |
| Associate | Azure AI Cloud Developer | AI-200 | Current (new) |
| Associate | AI Agent Builder | AB-620 | Current (new) |
| Associate | Azure Databricks Data Engineer | DP-750 | Current (new) |
| Expert | Azure Solutions Architect Expert | AZ-305 | Current |
| Expert | DevOps Engineer Expert | AZ-400 | Current |
| Specialty | Azure Virtual Desktop | AZ-140 | Current |
| Specialty | Azure Cosmos DB Developer | DP-420 | Current |
| Specialty | Azure for SAP Workloads | AZ-120 | Current |
| Specialty | Azure IoT Developer | AZ-220 | **Retired** |
| Specialty | Azure Support Engineer for Connectivity | AZ-720 | **Retired** |
| Specialty | Azure Stack Hub Operator | AZ-600 | **Retired** |

### Renewal: annual, free, and unproctored

Microsoft's renewal model is genuinely different from most of this
encyclopedia's other vendors and is worth planning around. A role-based
Azure certification is valid for **one year**, and it is renewed by
passing a **free, online, unproctored renewal assessment** on Microsoft
Learn, available in the six months before expiry. There is no fee and no
test center.

Two consequences follow. First, the real cost of holding an Azure
certification is an hour a year, not a re-sit — cheaper than the
three-year proctored re-examination model AWS and others use. Second, a
renewal assessment tracks the *current* blueprint, so a certification you
renew is quietly re-based onto newer content each year. Fundamentals
certifications (AZ-900, AI-901, DP-900) do **not** expire.

## Design Considerations

- **Pick by role, then check status before studying.** In a program mid-
  reorganization, the second step matters as much as the first. Two
  associate certifications carry published retirement dates within weeks
  of this writing.
- **Do not treat the levels as a ladder.** Fundamentals is optional for
  anyone already working on Azure; AZ-104 is the usual real starting point
  for infrastructure roles.
- **Budget for renewal, not re-certification.** Put the renewal window in
  a calendar. The assessment is free and unproctored, but it still lapses
  silently if ignored, and a lapsed certification must be re-earned by
  full exam.
- **Prefer certifications with no announced end date.** Where two options
  serve a role, the one without a retirement notice is the better
  multi-year investment — see Chapters 05 and 06 for the live example.
- **Verify every code before buying anything.** This program has renumbered
  (AI-900 → AI-901), retired (AI-102, DP-100, AZ-220, AZ-720, AZ-600), and
  introduced a whole new code family (AB-620) inside a single year.

## Implementation and Automation

### Confirming the live lineup from Microsoft's own catalog

```bash
# Microsoft Learn publishes a public catalog API. This is the primary
# source for what exists right now — never a third-party summary.
curl -s 'https://learn.microsoft.com/api/catalog/?locale=en-us&type=certifications' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin);
certs=[c for c in d["certifications"] if "azure" in (c["title"]+c["uid"]).lower()]
print(len(certs), "Azure certifications")
[print(c["certification_type"], "|", c["title"]) for c in sorted(certs, key=lambda x: x["certification_type"])]'
```

### Reading a certification's exam code and retirement notice

```bash
# The certification page carries both the exam code and any retirement
# banner in its HTML. Substitute the slug from the catalog output above.
curl -s https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/ \
  | grep -oE '\b(AZ|AI|DP|SC|AB)-[0-9]{3}\b' | sort -u
```

```bash
# The retirement sentence, if present:
curl -s https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/ \
  | sed 's/<[^>]*>/ /g' | tr -s ' ' \
  | grep -oE 'This certification[^.]{0,160}\.' | head -1
```

## Validation and Troubleshooting

- **A code that resolves is the pass signal.** If a certification page
  shows a different code than you expected, you have found a renumbering,
  not an error in your reading — AI-900 to AI-901 is the current example.
- **Read the retirement banner's scope.** Microsoft's banners state
  whether the *certification*, the *exam*, and the *renewal assessment*
  are all affected. Some notices cover only the exam.
- **Distinguish "retired" from "will retire".** AI-102 and DP-100 are
  already gone; AZ-204 and AZ-500 have future dates and can still be
  earned before them.
- **Renewal lapses are silent.** Microsoft emails, but the certification
  simply expires if the window closes. Check your Microsoft Learn profile
  rather than assuming.

## Security and Best Practices

- Register through Microsoft's official scheduling flow and its authorized
  delivery partner; confirm identification and online-proctoring
  requirements before exam day.
- Do not use unauthorized exam dumps. Beyond the Microsoft Certification
  agreement violation, a program renumbering and retiring exams this
  quickly makes circulating material unusually likely to be wrong.
- Practice in a dedicated Azure subscription with a spending limit or
  budget alert, not in a subscription carrying production workloads.
  Chapter 03's labs assume this separation.
- Treat the free Azure account's credit as finite — the most common
  preparation mistake is leaving lab resources running between study
  sessions.

## References and Knowledge Checks

**References**

- [Microsoft Learn — Browse Credentials](https://learn.microsoft.com/en-us/credentials/browse/?products=azure) —
  the authoritative lineup, filtered to Azure.
- [Microsoft Learn Catalog API](https://learn.microsoft.com/api/catalog/) —
  machine-readable certification and exam data.
- [Certification renewal](https://learn.microsoft.com/en-us/credentials/support/renew-your-microsoft-certification) —
  the annual free renewal-assessment model.
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md) —
  every certification with code, exam end date, and training access.
- See [Volume XVII](../../volume-17-aws-architecture-security/README.md)
  for the AWS program this one is usefully contrasted with.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name the four levels and explain why none is a prerequisite for
   another.
2. What does the `AB` prefix signal, and why is the appearance of a new
   code family informative?
3. How does Microsoft's renewal model differ from a three-year proctored
   re-examination, and what are the two practical consequences?
4. Which certifications currently carry a future retirement date, and
   which are already retired?
5. Why is a third-party "Azure certification list" a particularly poor
   source for this program right now?

## Hands-On Lab

**Objective:** Build a verified, personal Azure certification plan from
primary sources, and stand up the cost-controlled subscription the later
chapters' labs assume.

**Cost note:** Steps 1–3 are free. Step 4 creates a budget alert, which is
also free; resources you later create are not.

**Prerequisites**

- An Azure account you may use as a sandbox.
- Web access to Microsoft Learn.

**Steps**

1. **List the lineup (10 minutes).** Run the catalog query from the
   Implementation section and compare its output against this chapter's
   table.

   **Expected result:** a match, or a documented difference — which means
   this chapter has aged and Chapter 09's currency check is due.

2. **Confirm three codes (10 minutes).** For three certifications relevant
   to your role, pull the exam code and any retirement sentence from the
   certification page.

   **Expected result:** three codes confirmed from Microsoft, not from
   this chapter.

3. **Choose and justify (15 minutes).** Write down the one or two
   certifications your role justifies, with a sentence each. Exclude
   anything carrying a retirement date you cannot beat.

   **Expected result:** a short, defensible plan.

4. **Create the cost guardrail (10 minutes).** In the sandbox
   subscription, create a budget with an alert threshold.

   **Expected result:** an alert that fires before study labs become
   expensive.

5. **Negative test (10 minutes).** Look up the same certifications on a
   third-party listing site and compare against step 2.

   **Expected result:** at least one discrepancy — a retired certification
   still listed, or AI-900 shown instead of AI-901. This is why step 2
   uses primary sources.

6. **Cleanup:** keep the budget alert. Remove anything else created while
   exploring, and confirm no compute is running.

## Lab Verification

Complete this sign-off once the plan is built from confirmed codes and the
budget guardrail is active. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsoft's Azure certification program has four levels and is role-based
by construction, which is why it reorganizes when roles change — and it is
mid-reorganization now. Exam codes carry a subject-family prefix (`AZ`,
`AI`, `DP`, `SC`, and the new `AB`), not a level. Renewal is annual, free,
and unproctored, which makes holding a certification cheap but means a
lapse is silent and re-based content arrives yearly. Two associate
certifications carry retirement dates within weeks of this writing and four
certifications are already retired, so confirming status against Microsoft
Learn is not optional politeness — it is the difference between studying
for something that will exist and something that will not.

- [ ] Can name the four levels and explain that none gates another.
- [ ] Can read an exam code's subject family, including the new `AB`.
- [ ] Can explain the annual free renewal model and its two consequences.
- [ ] Knows which certifications are retiring and which are retired.
- [ ] Has confirmed at least three codes from Microsoft's own pages.
- [ ] Completed the hands-on lab, including the budget guardrail and the
      third-party-discrepancy negative test.
