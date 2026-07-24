# Chapter 01: The Google Cloud Certification Program — Levels and Validity

## Learning Objectives

- Map Google Cloud's certification program: three levels — foundational,
  associate, and professional — and the fourteen certifications in them
- Explain why Google Cloud certifications have **no exam codes**, and what
  that changes about verifying currency
- State the exam format, fee, and validity period for each level, and
  explain the unusual two-versus-three-year split
- Recognize the program-wide exam refresh following Google Cloud Next '26
  and its practical effect on study material
- Locate the authoritative source for any Google Cloud certification's
  scope and status

## Theory and Architecture

### Three levels, fourteen certifications

Google Cloud organizes certifications into **foundational**,
**associate**, and **professional**. There is no expert or specialty tier —
the professional level is the top, and it is wide rather than deep.

Verified against Google Cloud's certification pages on **23 July 2026**:

| Level | Certification |
| --- | --- |
| Foundational | Cloud Digital Leader |
| Foundational | Generative AI Leader |
| Associate | Cloud Engineer |
| Associate | Google Workspace Administrator |
| Associate | Data Practitioner |
| Professional | Cloud Architect |
| Professional | Cloud Database Engineer |
| Professional | Cloud Developer |
| Professional | Data Engineer |
| Professional | Cloud DevOps Engineer |
| Professional | Cloud Security Engineer |
| Professional | Cloud Network Engineer |
| Professional | Machine Learning Engineer |
| Professional | Security Operations Engineer |

**No certification is a prerequisite for another.** Google states no
prerequisites even at professional level, offering recommended experience
instead — typically three or more years of industry experience including
one or more with Google Cloud.

### No exam codes

Google Cloud is the only major cloud program in this encyclopedia with
**no exam codes**. There is no `AZ-104`, no `SAA-C03` — a certification is
identified solely by its name, as with the Palo Alto Networks program
([Volume XVI](../../volume-16-palo-alto-networks-security/README.md)).

This changes how you check currency. With AWS or Azure, a code's version
suffix is the fastest staleness test
([Volume XVII](../../volume-17-aws-architecture-security/README.md),
Chapter 10). Here there is no such signal, so the checks are:

- the certification still appears on Google Cloud's certification page;
- the **exam guide** on that page still describes the sections you are
  studying;
- the material you are using postdates the most recent exam refresh.

A renamed or re-scoped Google Cloud certification leaves no version
number behind to warn you. That absence is the single most important
operational fact in this chapter.

### Format, fee, and validity by level

| Level | Length | Fee (USD) | Format | Validity |
| --- | --- | --- | --- | --- |
| Foundational | 90 minutes | $99 | 50–60 multiple choice | **3 years** |
| Associate | 2 hours | $125 | 50–60 multiple choice and multiple select | **3 years** |
| Professional | 2 hours | $200 | 50–60 multiple choice and multiple select | **2 years** |

Fees exclude tax. All levels are delivered **online-proctored or onsite**
at a test center.

The validity split is counter-intuitive and worth internalizing:
**professional certifications expire sooner than foundational and
associate ones** — two years against three. The rationale is that
professional content tracks a faster-moving product surface. The practical
effect is that the certifications demanding the most preparation also
demand the most frequent recertification, which should be part of the
decision to pursue one.

Recertification means retaking the current exam; there is no free
unproctored renewal assessment of the kind Microsoft offers
([Volume XXXIII](../../volume-33-microsoft-azure-certifications/README.md),
Chapter 01). Budget the full fee again.

### The Google Cloud Next '26 refresh

Google's certification page currently carries a program-wide notice: exams
are being updated to reflect product announcements from **Google Cloud
Next '26**, specifically naming the **Gemini Enterprise Agent Platform**
and **Google Cloud's data and analytics stack**, and directing candidates
to each exam guide for the products actually covered.

Two consequences. First, **the exam guide is the authority**, not any
course, and not this volume — it is the artifact Google updates when
content moves. Second, material predating Next '26 may omit newly examined
products while remaining otherwise accurate, which is a subtler failure
than an outright wrong answer.

## Design Considerations

- **Pick by role; there is no ladder.** With no prerequisites anywhere,
  the right first certification is the one matching your work. Associate
  Cloud Engineer is the usual real starting point for infrastructure
  engineers, exactly as AZ-104 is on Azure.
- **Weigh the two-year professional clock before committing.** A
  professional certification is roughly twice the fee of an associate and
  expires a year sooner. That is a real ongoing cost, not a one-off.
- **Read the exam guide before choosing study material.** Because there
  are no codes, the guide's section list is the only reliable statement of
  scope, and it is what the Next '26 refresh updates.
- **Prefer Google's own learning paths for newly refreshed content.**
  Third-party material lags a refresh by months and gives no version
  signal that it has.
- **Do not assume a certification still exists because it once did.**
  Google has renamed and re-leveled credentials — Google Workspace
  Administrator now sits at associate level — and without codes those
  moves are easy to miss.

## Implementation and Automation

### Confirming the lineup from Google's own page

```bash
# The certification page lists every current certification grouped by
# level. This is the primary source — never a third-party summary.
curl -sL -A "Mozilla/5.0" https://cloud.google.com/learn/certification \
  | sed 's/<[^>]*>/\n/g' \
  | grep -nE '^(Foundational|Associate|Professional) certification$' -A 20 \
  | head -60
```

### Reading a certification's exam facts

```bash
# Length, fee, format, and validity are stated on each certification page.
curl -sL -A "Mozilla/5.0" https://cloud.google.com/certification/cloud-architect \
  | sed 's/<[^>]*>/ /g' | tr -s ' ' \
  | grep -oE '(Length|Registration fee|Exam format|Validity period)[^.]{0,70}' \
  | head -5
```

### A portfolio tracker built around expiry

```text
# Google Cloud has no free renewal path, so expiry is a budget event.
# Professional certifications expire a year sooner than the rest.

Certification              | Level        | Earned | Expires | Fee to renew
---------------------------|--------------|--------|---------|-------------
Associate Cloud Engineer   | associate    |        |         | $125
Professional Cloud Architect| professional |        |         | $200
```

## Validation and Troubleshooting

- **The certification's presence on the page is the pass signal.** With no
  codes, "does it still appear, and does its exam guide still match my
  study plan?" replaces a version check.
- **Compare your study material against the exam guide's section list.**
  If the guide names products your material never mentions, the material
  predates a refresh.
- **Check the level, not just the name.** Google Workspace Administrator
  is an associate certification; older references may present it
  differently.
- **Confirm the validity period per certification.** Three years at
  foundational and associate, two at professional — verify on the page
  rather than assuming a single program-wide number.
- **Recertification is a full retake.** If you are planning around a
  renewal assessment, you are planning around a Microsoft feature that
  Google does not offer.

## Security and Best Practices

- Register only through Google Cloud's official certification pages and
  its proctoring partner; confirm identification and online-proctoring
  requirements before exam day.
- Do not use unauthorized exam dumps. Beyond violating Google's
  certification agreement, the Next '26 refresh makes circulating material
  unusually likely to be both illicit and stale.
- Practice in a dedicated Google Cloud project with a **budget alert**, not
  in a project carrying real workloads. Every lab in this volume assumes
  that separation.
- Google Cloud's free tier and trial credit are finite; the most common
  preparation mistake is leaving lab resources running between sessions.
  Chapter 02 sets up the guardrail.

## References and Knowledge Checks

**References**

- [Google Cloud certification](https://cloud.google.com/learn/certification) —
  the authoritative lineup by level, and the program-wide refresh notice.
- [Associate Cloud Engineer](https://cloud.google.com/certification/cloud-engineer)
  and [Professional Cloud Architect](https://cloud.google.com/certification/cloud-architect) —
  representative pages showing format, fee, and validity.
- [Google Cloud certification FAQ](https://support.google.com/cloud-certification/answer/9438208) —
  eligibility, cost, and recertification policy.
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Volume XXXIII](../../volume-33-microsoft-azure-certifications/README.md)
  and [Volume XVII](../../volume-17-aws-architecture-security/README.md)
  for the Azure and AWS programs this one is usefully contrasted with.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Name the three levels and say how many certifications sit in each.
2. Why does the absence of exam codes change how you check currency, and
   what replaces the version check?
3. State the fee and validity period for each level, and explain why the
   professional split is counter-intuitive.
4. What does the Google Cloud Next '26 notice mean for study material
   published before it?
5. How does Google's recertification model differ from Microsoft's, and
   what does that cost?

## Hands-On Lab

**Objective:** Build a verified Google Cloud certification plan from
primary sources, and stand up the cost-controlled project the later
chapters assume.

**Cost note:** Steps 1–3 are free. Step 4 creates a budget alert, itself
free; resources created later are not.

**Prerequisites**

- A Google Cloud account you may use as a sandbox.
- `gcloud` CLI installed and authenticated.

**Steps**

1. **List the lineup (10 minutes).** Run the certification-page query and
   compare its output against this chapter's table.

   **Expected result:** fourteen certifications across three levels, or a
   documented difference — which means this chapter has aged and
   Chapter 09's currency check is due.

2. **Read one exam guide (15 minutes).** Open the exam guide for a
   certification you are considering and list its top-level sections.

   **Expected result:** a section list to test study material against —
   the substitute for a version code.

3. **Record the economics (10 minutes).** For your candidate
   certification, note fee and validity, and compute the cost per year of
   holding it.

   **Expected result:** an explicit ongoing cost, especially for a
   two-year professional credential.

4. **Create the cost guardrail (10 minutes).**

   ```bash
   gcloud projects create gcp-cert-lab-$RANDOM --name="cert lab"
   ```

   Then create a budget with an alert threshold on the billing account
   linked to that project.

   **Expected result:** a budget alert that fires before study labs become
   expensive.

5. **Negative test (10 minutes).** Look up the same certification on a
   third-party listing site and compare level, fee, and whether the newer
   certifications appear.

   **Expected result:** at least one discrepancy — commonly a missing
   Generative AI Leader, Data Practitioner, or Security Operations
   Engineer, or Workspace Administrator shown at the wrong level.

6. **Cleanup:** keep the budget alert. Delete the project if you created
   one solely for this step:

   ```bash
   gcloud projects delete <PROJECT_ID>
   ```

## Lab Verification

Complete this sign-off once the plan is built from confirmed sources and
the budget guardrail is active. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Google Cloud's program has three levels — foundational, associate, and
professional — holding fourteen certifications, with **no prerequisites
anywhere** and, uniquely among the major clouds, **no exam codes**. That
absence removes the version signal AWS and Azure provide, so currency is
checked by the certification's continued presence on Google's page and by
its exam guide's section list. Fees run $99, $125, and $200 by level;
validity is three years at foundational and associate but **two years at
professional**, and recertification is a full paid retake rather than a
free renewal assessment. A program-wide refresh following Google Cloud
Next '26 is updating exams around the Gemini Enterprise Agent Platform and
the data and analytics stack, which makes the exam guide — not any
course — the authority on scope.

- [ ] Can name the three levels and the count in each.
- [ ] Can explain what the absence of exam codes changes about currency
      checks.
- [ ] Knows the fee and validity for each level, including the
      professional two-year clock.
- [ ] Can explain the Next '26 refresh's effect on older material.
- [ ] Knows recertification is a full paid retake.
- [ ] Completed the hands-on lab, including the budget guardrail and the
      third-party-discrepancy negative test.
