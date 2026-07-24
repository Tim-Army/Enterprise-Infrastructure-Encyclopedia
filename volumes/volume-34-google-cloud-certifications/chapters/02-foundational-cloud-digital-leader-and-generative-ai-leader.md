# Chapter 02: Foundational — Cloud Digital Leader and Generative AI Leader

## Learning Objectives

- Distinguish the two foundational certifications and the audience each is
  written for
- Explain why Generative AI Leader exists and what its arrival says about
  Google's certification strategy
- Describe the Google Cloud concepts both assume: projects, the resource
  hierarchy, billing accounts, and IAM at a conceptual level
- Decide whether a foundational certification is worth your time, given
  that neither is a prerequisite for anything
- Use Google Skills learning paths, which cover both at no cost

## Theory and Architecture

### Two foundational certifications

| Certification | Written for |
| --- | --- |
| Cloud Digital Leader | Anyone needing cloud fluency without a build role — including non-technical stakeholders |
| Generative AI Leader | Those needing to reason about generative AI adoption, capability, and risk |

Both are **90 minutes, $99, 50–60 multiple-choice questions**, delivered
online-proctored or onsite, and valid for **three years** — the longest
validity in the program (verified 23 July 2026).

Neither has prerequisites, and neither is required for anything else.

### Cloud Digital Leader: the shared vocabulary

Cloud Digital Leader validates broad knowledge of cloud concepts and of
Google Cloud's products, services, tools, features, benefits, and use
cases. Google's own candidate profile describes someone in a
**collaborative role with technical professionals** — which is the honest
description of its value.

Its function is a shared vocabulary. When a product manager, a finance
analyst, and an engineer all mean the same thing by "project," "billing
account," and "committed use discount," planning conversations get
shorter. That is a legitimate reason to sit it even where the technical
content is already familiar.

### Generative AI Leader: a foundational credential for a new conversation

The **Generative AI Leader** certification is the newer of the two and
sits at the same foundational level. It targets the ability to reason
about generative AI in an organizational context — what the technology can
and cannot do, where it creates value, how it is adopted responsibly, and
what Google Cloud offers to support it.

Its existence at *foundational* level is the interesting part. Compare
Microsoft, which placed AI fluency at foundational level (AI-901) *and*
built a full AI-centric associate tier
([Volume XXXIII](../../volume-33-microsoft-azure-certifications/README.md),
Chapter 06), and AWS, which placed AI Practitioner at foundational and
Generative AI Developer at *professional*
([Volume XVII](../../volume-17-aws-architecture-security/README.md),
Chapter 12). All three vendors reached the same conclusion — that
generative AI needs a non-builder credential — and Google's is aimed
squarely at the leadership conversation rather than the build.

Note the program-wide Next '26 refresh from
[Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md):
generative AI content is exactly the area moving fastest, so the exam
guide matters more here than anywhere else in the program.

### The concepts both assume

- **Project** — the fundamental unit of resource ownership, billing
  attribution, and IAM scope. Almost everything in Google Cloud belongs to
  a project.
- **Resource hierarchy** — organization → folders → projects → resources.
  IAM policies set high in the hierarchy are inherited downward, which is
  the mechanism behind most Google Cloud governance.
- **Billing account** — attached to projects, and separate from them; one
  billing account commonly funds many projects, which is why budget alerts
  are set on the billing account rather than the project.
- **IAM** — principals granted roles at a scope. Google Cloud's roles are
  additive; there is no deny by default at the role level, which differs
  from what administrators coming from other clouds often expect.

## Design Considerations

- **Skip the foundational tier if you already build on Google Cloud.** For
  an engineer heading toward Associate Cloud Engineer (Chapter 03), Cloud
  Digital Leader certifies knowledge that exam tests anyway.
- **Generative AI Leader is a fluency credential, not an engineering
  one.** If the goal is to build generative-AI systems, the relevant
  targets are the professional data and ML certifications (Chapter 08),
  not this.
- **Three-year validity makes these the cheapest credentials to hold.**
  Foundational and associate both run three years against professional's
  two, so a foundational certification is the lowest ongoing cost in the
  program.
- **Both are covered free.** Google Skills learning paths span both exams
  at no cost, which makes paid courses hard to justify at this level.
- **Watch the exam guide for generative AI content specifically.** It is
  the fastest-moving area in the program and the one the Next '26 refresh
  names directly.

## Implementation and Automation

### Reading the resource hierarchy the exams assume

```bash
# The organization → folder → project shape, if you have an organization
gcloud organizations list
gcloud resource-manager folders list --organization=<ORG_ID>
```

```bash
# Projects you can see, with their lifecycle state
gcloud projects list --format='table(projectId, name, lifecycleState)'
```

### Billing: the separation these exams test

```bash
# Billing accounts are separate from projects — one funds many
gcloud billing accounts list
```

```bash
# Which billing account funds a given project
gcloud billing projects describe <PROJECT_ID>
```

### Inspecting IAM at the conceptual level

```bash
# Roles granted on a project, by principal — note roles are additive
gcloud projects get-iam-policy <PROJECT_ID> \
  --flatten='bindings[].members' \
  --format='table(bindings.role, bindings.members)'
```

## Validation and Troubleshooting

- **Vocabulary test.** If you cannot explain the difference between a
  project and a billing account, or say how an IAM policy set on a folder
  affects a project inside it, the foundational content is not yet solid
  regardless of hands-on experience.
- **Check the exam guide before trusting generative-AI material.** With
  the Next '26 refresh naming this area, a course from a year ago may omit
  products now examined.
- **Confirm the validity period.** Three years at this level, but verify
  on the page — the program's two-versus-three-year split is easy to
  misremember.
- **Free training first.** If a paid foundational course is under
  consideration, compare it against the Google Skills path for the same
  exam before buying.

## Security and Best Practices

- Do exploration in a sandbox project with a billing budget alert, not in
  a project holding real workloads.
- `gcloud projects list` and billing output identify your organization and
  spending; treat that output as sensitive in screenshots and pasted
  terminal sessions.
- Google Cloud IAM roles are **additive** — granting a broad role does not
  get narrowed by also granting a narrow one. Understanding that early
  prevents a class of over-permissioning mistakes that persists into the
  associate and professional material.
- Responsible-AI considerations are examinable in Generative AI Leader and
  operationally real: know the limits of what a model output can be
  trusted to assert before recommending an adoption path.

## References and Knowledge Checks

**References**

- [Cloud Digital Leader](https://cloud.google.com/certification/cloud-digital-leader) —
  90 minutes, $99, three-year validity.
- [Generative AI Leader](https://cloud.google.com/learn/certification/generative-ai-leader)
- [Google Skills](https://cloud.google.com/learn) — free learning paths
  covering both exams.
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md)
  for the program map and the Next '26 refresh.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Name the two foundational certifications and the audience each targets.
2. What does the existence of a foundational generative-AI credential
   suggest, and how do AWS and Microsoft compare?
3. Distinguish a project from a billing account, and say where a budget
   alert attaches.
4. How does an IAM policy set on a folder affect projects inside it?
5. Why does "IAM roles are additive" matter for a newcomer's mental model?

## Hands-On Lab

These labs cover the exam-guide topics for both foundational
certifications. **Cloud Digital Leader** is a knowledge credential, so its
labs read the platform facts the exam asks about (there is no build to
perform). **Generative AI Leader** is exercised against its published
guide sections (fundamentals, Google Cloud's offerings, techniques,
business strategy). Mapping is in the
[volume README](../README.md#lab-coverage--foundational).

**Cost note:** every command here is a read or an API-availability check.
Nothing billable is created; there is nothing to clean up beyond the
optional project deletion in Lab 2.10.

**Prerequisites**

```bash
export PROJECT_ID="$(gcloud config get-value project)"; echo "$PROJECT_ID"
```

**Expected result:** your sandbox project ID.

### Lab 2.1 — Digital transformation with Google Cloud *(Cloud Digital Leader)*

```bash
gcloud services list --available --format='value(name)' | wc -l
```

**Expected result:** a count in the hundreds — the breadth of the service
catalogue a digital-transformation conversation draws on. The leader
credential is about knowing this surface exists, not operating it.

### Lab 2.2 — Infrastructure and application modernization *(Cloud Digital Leader)*

```bash
gcloud compute machine-types list --filter="zone:us-central1-a" \
  --format='value(name)' | head -5
gcloud run services list --format='value(name)' 2>/dev/null | head -3
```

**Expected result:** VM types (lift-and-shift) and any Cloud Run services
(modernized). Naming the spectrum from VM to container to serverless is
the modernization talking point the exam tests.

### Lab 2.3 — Data and AI in the cloud *(Cloud Digital Leader)*

```bash
gcloud services list --available \
  --filter="name:(bigquery.googleapis.com OR aiplatform.googleapis.com)" \
  --format='value(name)'
```

**Expected result:** both `bigquery.googleapis.com` and
`aiplatform.googleapis.com` listed — the data and AI pillars a leader is
expected to place in the portfolio.

### Lab 2.4 — Trust, security, scaling, and operations *(Cloud Digital Leader)*

```bash
gcloud resource-manager org-policies list --project="$PROJECT_ID" \
  --format='value(constraint)' | head -5
```

**Expected result:** governance constraints (or none on a bare project).
The leader-level point is that trust and security are configurable
controls, not properties you hope for.

### Lab 2.5 — Fundamentals of gen AI *(Generative AI Leader §1)*

```bash
gcloud ai models list --region=us-central1 --filter="displayName:gemini" \
  --format='value(displayName)' 2>&1 | head -5
```

**Expected result:** Gemini foundation models, or an enable-API message.
Section 1 is about recognizing foundation-model use cases and strengths —
this is where they live.

### Lab 2.6 — Google Cloud's gen AI offerings *(Generative AI Leader §2)*

```bash
gcloud services list --available \
  --filter="name:(aiplatform.googleapis.com OR discoveryengine.googleapis.com)" \
  --format='value(name)'
```

**Expected result:** Vertex AI (`aiplatform`) and the agent/search surface
(`discoveryengine`). These are the offerings the section names for
building and for agents.

### Lab 2.7 — Techniques to improve gen AI output *(Generative AI Leader §3)*

```text
# Grounding is the section-3 technique that most changes output quality.
# On Vertex AI it is enabled per request. Record the difference:
Ungrounded prompt  : "What is our Q3 refund policy?"  -> model may invent
Grounded prompt    : same prompt + a grounding source (your docs / Search)
                     -> answer cites the source
```

**Expected result:** a written contrast showing grounding replaces
plausible-but-invented answers with sourced ones — the exam's core
technique point, alongside prompt engineering.

### Lab 2.8 — Business strategies and responsible AI *(Generative AI Leader §4)*

```bash
gcloud services list --available --filter="name:modelarmor OR name:dlp" \
  --format='value(name)' 2>&1 | head -3
```

**Expected result:** data-protection / safety services available.
Responsible AI (4.3) is examinable and real — knowing which controls
exist is the business-strategy competence the section rewards.

### Lab 2.9 — Verify the fundamentals scaffolding *(both certifications)*

```bash
gcloud projects describe "$PROJECT_ID" --format='value(projectId, lifecycleState)'
gcloud billing projects describe "$PROJECT_ID" --format='value(billingEnabled)'
```

**Expected result:** an `ACTIVE` project with `billingEnabled: True`.
Project, billing, and hierarchy are the shared vocabulary both foundational
exams assume — confirm you can read them.

### Lab 2.10 — Negative test: recognizing a disabled service

```bash
gcloud ai models list --region=us-central1 2>&1 | head -3
```

**Expected result:** either a model list, **or** the message
`API [aiplatform.googleapis.com] not enabled`. Being able to tell "the
service is off" from "there is nothing there" is the foundational
troubleshooting skill — and the leader exams frame it as knowing that
capabilities must be *enabled* before they exist for a project.

```bash
# Optional cleanup if this was a throwaway project:
gcloud projects delete "$PROJECT_ID" --quiet
```

**Expected result:** `DELETE_REQUESTED`, or skip this to keep the sandbox.

## Lab Verification

Complete this sign-off once the hierarchy has been read, IAM inspected, and
the permission-error negative test observed. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Google Cloud's foundational tier holds **Cloud Digital Leader** and
**Generative AI Leader** — both 90 minutes, $99, and valid three years,
which makes them the cheapest credentials in the program to hold. Neither
is a prerequisite for anything, and for an engineer already building on
Google Cloud both are usually skippable; their value is fluency for
non-builders and a shared vocabulary across a team. Generative AI Leader's
placement at foundational level mirrors decisions AWS and Microsoft made
independently, and its subject matter is the area the Google Cloud Next '26
refresh names directly — so the exam guide, not any course, is the
authority. Both rest on the same scaffolding: projects, the organization →
folder → project hierarchy, billing accounts held separately from
projects, and additive IAM roles inherited downward.

- [ ] Can name both foundational certifications and their audiences.
- [ ] Can explain why a foundational generative-AI credential exists.
- [ ] Can distinguish project, billing account, and resource hierarchy.
- [ ] Can explain downward IAM inheritance and additive roles.
- [ ] Knows both are three-year credentials covered by free training.
- [ ] Completed the hands-on lab, including the permission-error negative
      test.
