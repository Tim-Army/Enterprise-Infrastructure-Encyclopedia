# Chapter 01: The Microsoft Certification Program Beyond Azure

## Learning Objectives

- Describe Microsoft's role-based certification model and its four tiers.
- Explain the Fundamentals tier as the gateway across every product family.
- Navigate Microsoft Learn, exam pages, and the Catalog API to confirm current facts.
- Describe the exam experience: Pearson VUE/OnVUE, formats, and Credly badges.
- Explain free annual renewal and why it makes Microsoft credentials cheap to hold.

## Theory and Architecture

Microsoft certifications are **role-based**: each credential validates the
skills of a **job role** (administrator, developer, functional consultant,
security operations analyst, solution architect) rather than a single
product. A credential is earned by passing one or more **exams**, each with a
code (`MS-102`, `SC-300`, `DP-700`, `GH-100`) and a published **exam
blueprint** of weighted skill domains. Beyond Azure — which has its own
volume — the program spans seven families: **Microsoft 365**, **Security,
Compliance, and Identity (SC)**, **Power Platform (PL)**, **Dynamics 365
(MB)**, **Data and Analytics (DP)**, **AI (AI)**, and **GitHub (GH)**.

There are four **tiers**. **Fundamentals** credentials (the `x-900` exams —
MS-900, SC-900, PL-900, DP-900, AI-900/AI-901, plus MB-910/MB-920 and GitHub
Foundations GH-900) prove foundational understanding of a family and have no
prerequisites; they are the gateway. **Associate** credentials validate the
core role (MS-102, MD-102, SC-300, PL-400, DP-700, AI-102). **Expert**
credentials (MS-102 Administrator Expert, SC-100 Cybersecurity Architect,
PL-600 Solution Architect) validate senior, cross-domain roles. **Specialty**
credentials cover a focused technology. Some Expert credentials historically
required a prerequisite Associate; Microsoft has removed most hard
prerequisites, but the intended learning order still runs Fundamentals →
Associate → Expert.

The authority for every fact is **Microsoft Learn** (`learn.microsoft.com/
credentials`). Each certification has a page with its exams, blueprint (skills
measured), study guide, free practice assessment where available, and status.
The **Microsoft Learn Catalog API** (`learn.microsoft.com/api/catalog`)
returns the whole catalog as JSON — the reliable way to enumerate current
credentials and detect renames, new betas, and retirements programmatically.

Exams are delivered through **Pearson VUE**, in a test center or online-
proctored with **OnVUE**, and most role-based exams are multiple-choice with
case studies and, historically, interactive labs. Passing earns a **Credly**
digital badge and a certificate. Crucially, Microsoft role-based
certifications are valid for **one year** and renew through a **free online
assessment** on Microsoft Learn in the six months before expiry — no re-exam,
no fee — which makes a Microsoft credential unusually cheap to *hold* compared
with the paid-retake model of AWS, Google Cloud, or Zscaler.

## Design Considerations

Plan a certification path by **role and family**, not by collecting badges.
Start at **Fundamentals** for an unfamiliar family to learn the vocabulary and
service map cheaply, then target the **Associate** that matches the day job,
and pursue **Expert** only when the role is genuinely senior and
cross-domain. Because most hard prerequisites are gone, you *can* take an
Expert exam directly, but the Fundamentals-first order still produces better
outcomes and a cheaper failure surface.

Treat **currency** as a first-class concern. Microsoft renames and retires
exams frequently, so verify a target exam's **code, name, and status** on
Microsoft Learn before investing study time, and diarize the **free renewal**
window so a hard-won credential does not lapse. For teams, map required roles
to credentials, track renewals centrally, and use the free practice
assessments to gate exam registration.

## Implementation and Automation

Confirm current facts from the authoritative sources. Enumerate the catalog
with the Learn Catalog API (parse the JSON, do not eyeball a rendered page):

```bash
curl -s "https://learn.microsoft.com/api/catalog/?type=certifications&locale=en-us" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin);
print(len(d["certifications"]), "certifications");
[print(c["certification_type"], "|", c["title"]) for c in d["certifications"]
 if c["certification_type"] in ("fundamentals","role-based") and "(legacy" not in c["title"].lower()][:10]'
```

Read an individual certification's exams and blueprint from its page (the
exam code and "skills measured" domains live there):

```bash
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/m365-administrator-expert/" \
  | grep -oE '\bMS-[0-9]{3}\b' | sort -u   # -> MS-102
```

## Validation and Troubleshooting

Confirm a credential is current and understand its requirements:

```text
Microsoft Learn > Credentials > Browse > filter to Certifications
  -> the certification page lists: exam(s), Skills measured (blueprint),
     Study guide, Practice assessment, and any "retiring" banner.
```

Common pitfalls: studying an **exam code from an old blog** that has since
been renumbered (verify on Learn — for example AI-900 became AI-901 for Azure
AI Fundamentals, and SC-400 became SC-401); assuming a credential still needs
a **prerequisite** that Microsoft has since removed; letting a credential
**lapse** because the free renewal window was missed (it opens six months
before expiry); and confusing a **certification** with a single **exam** (some
credentials, historically, needed two exams). The Catalog API's
`certification_type` and title (which flags `(legacy)`/`(beta)`) are the fast
way to see what is current.

## Security and Best Practices

Verify certification claims against **Microsoft Learn**, never a third-party
exam-dump site — dumps are inaccurate, violate the exam agreement, and can
void a credential. Use the **free practice assessments** to measure readiness
honestly. Protect the value of a credential by **renewing on time** through
the free assessment. For organizations, treat the certification map as living
data — re-verify against the Catalog API on a cadence, because the program
(especially the AI and agent family) changes fast.

## References and Knowledge Checks

- Microsoft Learn: *Browse Credentials*; *Certification renewal*; *Exam formats and question types*; *Microsoft Learn Catalog API*.

**Knowledge checks**

1. What are the four tiers, and which exams mark the Fundamentals tier?
2. How does Microsoft's renewal model differ from AWS's or Google Cloud's?
3. Why should you verify an exam code on Microsoft Learn before studying?

## Hands-On Lab

Exam-preparation walkthroughs for navigating and verifying the program.

**Shared prerequisites for Labs 1.1–1.3** — a web browser and (for Lab 1.2)
`curl` and `python3`. **Cost:** none.

### Lab 1.1 — Read a certification page (Topic: Use Microsoft Learn)

**Objective:** Extract the exam, blueprint, and renewal facts for a credential.

```text
1. Open learn.microsoft.com/credentials and Browse > Certifications.
2. Open "Microsoft 365 Certified: Administrator Expert."
3. Record: the exam code, the "Skills measured" domains and weights, whether a
   free practice assessment exists, and the renewal note.
```

**Expected result:** you find exam **MS-102**, a weighted skills-measured
blueprint, a practice assessment, and a one-year validity with free renewal —
the page is the authoritative source for every fact.

**Negative test:** search a third-party site for the "MS-102 domains"; the
weights differ from Learn — trust the Learn page, not dumps.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Enumerate the catalog with the API (Topic: Verify currency)

**Objective:** List current credentials programmatically.

```bash
curl -s "https://learn.microsoft.com/api/catalog/?type=certifications&locale=en-us" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin);
certs=[c for c in d["certifications"] if c["certification_type"] in ("fundamentals","role-based") and "(legacy" not in c["title"].lower()];
print(len(certs),"current credentials");
print([c["title"] for c in certs if "Fundamentals" in c["title"]][:8])'
```

**Expected result:** a count of current credentials and the Fundamentals list
— the API is the reliable enumeration source; a rendered page is
JavaScript-built and hard to scrape.

**Negative test:** try to read the browse page HTML with `curl | grep` for
titles; you get the SPA shell, not the list — use the Catalog API.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a role-based path (Topic: Build a study plan)

**Objective:** Sequence credentials for a target role.

```text
For a "Microsoft 365 security administrator" role, sequence:
  1. SC-900 (Fundamentals) -> 2. SC-300 (Identity and Access Associate)
  -> 3. SC-200 (Security Operations Associate) -> 4. SC-401 (Information
  Security Administrator), with SC-100 (Cybersecurity Architect Expert) later.
Map each to hands-on practice in Volume XXXVII (Chapters 03, 10, 11).
```

**Expected result:** a Fundamentals→Associate→Expert path tied to hands-on
labs — the intended learning order even where prerequisites are not enforced.

**Negative test:** start at SC-100 (Expert) with no security background; the
cross-domain architecture exam is far harder without the Associate foundation
— sequence deliberately.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsoft's role-based program certifies job roles across seven families
beyond Azure, in four tiers (Fundamentals, Associate, Expert, Specialty).
Microsoft Learn and its Catalog API are the authority for exam codes,
blueprints, and status; exams run on Pearson VUE/OnVUE and earn Credly
badges; and credentials renew for free every year on Learn.

- [ ] I can explain the role-based model and the four tiers.
- [ ] I can use Microsoft Learn and the Catalog API to verify facts.
- [ ] I can describe the exam experience and renewal model.
- [ ] I can sequence a Fundamentals→Associate→Expert path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
