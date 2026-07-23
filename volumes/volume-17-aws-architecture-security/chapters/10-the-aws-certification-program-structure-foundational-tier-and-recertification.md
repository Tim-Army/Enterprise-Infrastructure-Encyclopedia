# Chapter 10: The AWS Certification Program — Structure, Foundational Tier, and Recertification

![The complete AWS certification program as four stacked levels. Foundational (90 minutes / 65 questions, no prior experience needed): Cloud Practitioner CLF-C02 and AI Practitioner AIF-C01. Associate (130 minutes / 65 questions): Solutions Architect SAA-C03, Developer DVA-C02, CloudOps Engineer SOA-C03 (renamed from SysOps Administrator), Data Engineer DEA-C01, and Machine Learning Engineer MLA-C01 with MLA-C02 registration opening 1 September 2026. Professional (180 minutes / 75 questions, 2+ years AWS experience): Solutions Architect Professional SAP-C02, DevOps Engineer Professional DOP-C02, and Generative AI Developer Professional AIP-C01. Specialty (170 minutes / 65 questions): Advanced Networking ANS-C01, retiring 25 August 2026, and Security SCS-C03. No level is a formal prerequisite for another.](../../../diagrams/volume-17-aws-architecture-security/chapter-10-aws-certification-program-map.svg)

*Figure 10-1. The whole program on one page: four levels, twelve exams. Levels describe assumed depth, not a required sequence.*

## Learning Objectives

- Describe the four levels of the AWS certification program — foundational,
  associate, professional, and specialty — and explain why none of them is
  a formal prerequisite for another.
- Identify all twelve current AWS certifications and their exam codes, and
  read what the `-C0x` version suffix signals about a blueprint's age.
- Explain what the two foundational certifications, Cloud Practitioner
  (CLF-C02) and AI Practitioner (AIF-C01), assess and who should — and
  should not — spend time on them.
- Describe the three-year validity period and the recertification paths
  that reset it, including how a higher-level certification affects lower
  ones.
- Locate the authoritative source for any exam's current code, format, and
  status, and recognize why third-party summaries of this program go stale
  unusually fast.

## Theory and Architecture

[Chapters 1 through 9](01-cloud-foundations-accounts-and-well-architected-design.md)
built an AWS architecture and security practice and mapped it to two
certifications — Solutions Architect – Associate (SAA-C03) and Security –
Specialty (SCS-C03). Those two are a small part of a twelve-exam program.
This chapter and the three that follow map the rest of it, so the volume's
technical content can be aimed at whichever certification a reader actually
needs.

As with every certification chapter in this encyclopedia, this is study and
review material organized against publicly published structure. It does not
reproduce exam questions, does not reveal scoring weightings, and is not a
substitute for AWS's own exam guides. Every code below was verified against
AWS's certification pages on 23 July 2026; confirm currency before
scheduling, because this program changes faster than most.

### Four levels, and what "level" actually means

AWS organizes certifications into four levels. The critical structural
fact — and the one most often gotten wrong — is that **no AWS
certification is a formal prerequisite for any other**. AWS removed the
old "associate before professional" requirement years ago. The levels
describe the depth of knowledge and the amount of hands-on experience each
exam assumes, not a gate you must pass through:

- **Foundational** — broad conceptual understanding, no prior experience
  required. 90 minutes, 65 questions.
- **Associate** — working technical competence in one role. Cloud or IT
  experience recommended. 130 minutes, 65 questions.
- **Professional** — advanced, organization-scale competence. AWS states
  roughly two or more years of hands-on AWS experience. 180 minutes,
  75 questions.
- **Specialty** — deep expertise in one technical domain. 170 minutes,
  65 questions.

You may sit a professional exam first. Whether you *should* is a different
question, addressed in [Chapter 12](12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md).

### The twelve current certifications

| Level | Certification | Exam code |
| --- | --- | --- |
| Foundational | Cloud Practitioner | CLF-C02 |
| Foundational | AI Practitioner | AIF-C01 |
| Associate | Solutions Architect – Associate | SAA-C03 |
| Associate | Developer – Associate | DVA-C02 |
| Associate | CloudOps Engineer – Associate | SOA-C03 |
| Associate | Data Engineer – Associate | DEA-C01 |
| Associate | Machine Learning Engineer – Associate | MLA-C01 |
| Professional | Solutions Architect – Professional | SAP-C02 |
| Professional | DevOps Engineer – Professional | DOP-C02 |
| Professional | Generative AI Developer – Professional | AIP-C01 |
| Specialty | Advanced Networking – Specialty | ANS-C01 |
| Specialty | Security – Specialty | SCS-C03 |

Three of these rows carry news that a reader working from older material
will not have:

- **CloudOps Engineer – Associate (SOA-C03)** is the certification
  previously called **SysOps Administrator – Associate**. The role name
  changed; the `SOA` code prefix did not.
- **Generative AI Developer – Professional (AIP-C01)** is a new
  professional certification covering production generative-AI solutions on
  services such as Amazon Bedrock. It did not exist in earlier program maps.
- **Advanced Networking – Specialty (ANS-C01) retires 25 August 2026** —
  covered in [Chapter 13](13-specialty-certifications-and-keeping-the-aws-certification-program-current.md).

Reading the code is useful: the three-letter prefix identifies the
certification and the **`-C0x` suffix is the blueprint version**. `SAA-C03`
is the third-generation Solutions Architect – Associate blueprint;
`DEA-C01` is a first-generation blueprint on a young certification. A
suffix bump means the blueprint was rebuilt, so study material written
against the previous suffix is stale in a way that matters.

### The foundational tier

Two certifications sit at the foundational level, and they serve different
purposes:

- **Cloud Practitioner (CLF-C02)** validates broad understanding of AWS
  services, the shared responsibility model, pricing and support models,
  and core security concepts — the ground
  [Chapter 1](01-cloud-foundations-accounts-and-well-architected-design.md)
  covers. It is aimed at people who work *around* the cloud (sales,
  finance, project management, leadership) as much as at engineers.
- **AI Practitioner (AIF-C01)** validates conceptual understanding of AI,
  machine learning, and generative AI on AWS — terminology, use cases,
  responsible-AI considerations, and the relevant service surface — without
  requiring the ability to build or train models.

Neither is required for anything else, and for a working engineer neither
is usually the right place to spend exam money. Their value is for people
who need credible fluency without a build role, and for teams that want a
shared vocabulary before a migration.

### Validity and recertification

Every AWS certification is valid for **three years**. AWS's recertification
model has one property worth planning around: **earning a
higher-level certification generally extends the validity of lower-level
ones you hold**. A reader holding Solutions Architect – Associate who then
passes Solutions Architect – Professional does not separately need to renew
the associate credential during that window. Confirm the current rules on
AWS's recertification page before relying on this for a specific pair —
the policy has been revised before, and it is the kind of detail that
quietly changes.

## Design Considerations

- **Do not treat the levels as a ladder you must climb.** Because nothing
  is a prerequisite, the right first exam is the one matching the work you
  do. An experienced AWS engineer should usually start at associate level
  or above and skip the foundational tier entirely.
- **Skip Cloud Practitioner if you can already pass an associate exam.**
  Its value is credible fluency for non-builders and shared vocabulary for
  teams. For someone already administering AWS, it consumes an exam fee and
  several weeks to certify knowledge their associate exam will test anyway.
- **AI Practitioner is a fluency credential, not an engineering one.** If
  the goal is to *build* generative-AI systems on AWS, the relevant target
  is Generative AI Developer – Professional (Chapter 12), not AIF-C01. If
  the goal is to converse credibly about AI strategy, AIF-C01 is well
  aimed.
- **Sequence recertification deliberately.** Because a higher certification
  extends lower ones, a reader planning both an associate and a
  professional exam should sit them close enough together that the
  professional pass carries the associate's clock forward, rather than
  renewing the associate separately.
- **Budget for reading speed, not just knowledge.** The format differences
  across levels (65 questions in 130 minutes at associate versus 75 in 180
  at professional) change the pacing more than the raw difficulty does;
  this is developed further in Chapter 12.
- **Ethical preparation boundary.** Prepare only from AWS's own exam
  guides, AWS Skill Builder, official training, and hands-on practice.
  Material claiming to reproduce live exam questions violates the AWS
  Certification agreement and is frequently wrong against the current
  blueprint — treat any such resource as disqualifying rather than helpful.

## Implementation and Automation

### A program-wide readiness tracker

```text
# Rate each certification 1-5 for current readiness. Below 3 means the
# volume chapters listed need lab time before the exam is worth booking.
# Only fill rows you actually intend to sit — most readers need two or
# three, not twelve.

Level        | Certification (code)             | Chapters      | Rating
-------------|----------------------------------|---------------|-------
Foundational | Cloud Practitioner (CLF-C02)     | 1             |
Foundational | AI Practitioner (AIF-C01)        | 1 (concepts)  |
Associate    | Solutions Architect (SAA-C03)    | 1-9           |
Associate    | Developer (DVA-C02)              | 4, 7          |
Associate    | CloudOps Engineer (SOA-C03)      | 6, 7          |
Associate    | Data Engineer (DEA-C01)          | 5             |
Associate    | ML Engineer (MLA-C01)            | 5 + SageMaker |
Professional | Solutions Architect (SAP-C02)    | 2, 3, 6, 7    |
Professional | DevOps Engineer (DOP-C02)        | 6, 7          |
Professional | Generative AI Developer (AIP-C01)| beyond volume |
Specialty    | Advanced Networking (ANS-C01)    | 3  [retiring] |
Specialty    | Security (SCS-C03)               | 8             |
```

### Confirming a certification's current code from the authoritative source

```bash
# AWS certification pages no longer print the exam code in body text, but
# the Skill Builder exam-prep link on each page embeds it. This is the
# most reliable way to confirm a code without trusting a third-party page.
curl -s https://aws.amazon.com/certification/certified-solutions-architect-associate/ \
  | grep -oE 'skillbuilder\.aws/[^"]*exam-prep[^"]*' | head -1
# -> .../category/exam-prep/solutions-architect-associate-SAA-C03
```

### Checking your own certification validity window

```bash
# Certifications are valid three years. Record the expiry for each
# credential you hold so recertification is planned, not discovered.
# (Values come from your AWS Certification Account; this is a local
# tracker, not an API call.)
cat > ~/aws-cert-expiry.txt <<'TRACKER'
certification,code,earned,expires,recert_plan
Solutions Architect - Associate,SAA-C03,,,
Security - Specialty,SCS-C03,,,
TRACKER
```

## Validation and Troubleshooting

- **Code check before study.** Before buying a course or book, confirm its
  target code matches the current one from the certification's own AWS
  page. A course built for `SAA-C02` or `SCS-C02` is a blueprint behind,
  and the gap is real content, not cosmetics.
- **Distinguish a language retirement from an exam retirement.** AWS
  publishes end-of-support notices for individual *language versions* of an
  exam alongside notices for the exam itself. The Cloud Practitioner page,
  for instance, carries a retirement notice that applies to its Indonesian
  language version, not to CLF-C02. Read which noun the notice attaches to
  before concluding a certification is closing.
- **Verify the level's format, not just its name.** If you have prepared
  for a 65-question associate exam and are sitting a 75-question
  professional one, the pacing plan is wrong even if the knowledge is
  right. Confirm duration and question count from the exam page.
- **Recertification assumptions age badly.** Before relying on a higher
  certification to carry a lower one's expiry, re-read AWS's current
  recertification policy; this is a rule that has changed and will likely
  change again.

## Security and Best Practices

- Register only through your AWS Certification Account and AWS's
  authorized testing partners; confirm identification and
  online-proctoring requirements from the official portal before exam day.
- Do not use, buy, or share unauthorized exam dumps. Beyond the
  certification-agreement violation, the fast `-C0x` turnover in this
  program makes circulating material unusually likely to be both illicit
  and wrong.
- Protect the AWS account you practice in with the same discipline
  [Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)
  teaches — a dedicated sandbox account under an organization, with a
  budget alarm — rather than practicing in an account that carries real
  workloads.
- Every hands-on exercise in this volume can incur charges. Keep the
  cost-control habits from
  [Chapter 7](07-observability-automation-performance-and-cost-governance.md)
  active during exam preparation, when the temptation to leave lab
  resources running between study sessions is highest.

## References and Knowledge Checks

**References**

- [AWS Certification](https://aws.amazon.com/certification/) — the
  authoritative list of current certifications, levels, and retirement
  notices; the source verified for this chapter on 23 July 2026.
- [AWS Certified Cloud Practitioner](https://aws.amazon.com/certification/certified-cloud-practitioner/)
  and [AWS Certified AI Practitioner](https://aws.amazon.com/certification/certified-ai-practitioner/) —
  the two foundational certifications, with current exam guides.
- [AWS Skill Builder](https://skillbuilder.aws/) — official digital
  training, including free exam-prep plans per certification.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — AWS Certifications and Course Access](../../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md) —
  every certification with its code, exam end date, and training access.
- See [Chapter 1](01-cloud-foundations-accounts-and-well-architected-design.md)
  for the shared responsibility model and Well-Architected content the
  foundational tier assesses.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any AWS exam item)*

1. Explain why "associate before professional" is a planning heuristic
   rather than a rule, and give a case where skipping the associate is
   defensible.
2. What does the `-C0x` suffix tell you, and why does it matter when
   choosing a study resource?
3. Which certification was previously named SysOps Administrator –
   Associate, and did its exam code prefix change?
4. Distinguish the audiences for Cloud Practitioner and AI Practitioner,
   and name one reader who should sit neither.
5. How does earning a professional certification affect the validity of an
   associate one you already hold, and where would you confirm that?

## Hands-On Lab

**Objective:** Build a verified, personal certification plan from
authoritative sources — confirming current codes yourself rather than
trusting this chapter — and stand up the cost-safe sandbox account you will
practice in.

**Cost note:** Steps 1–3 are free. Step 4 creates a budget alarm, which is
free; any resources you later create in the sandbox are not. Step 6 cleans
up.

**Prerequisites**

- An AWS account you may use as a sandbox, ideally a dedicated member
  account under an organization
  ([Chapter 2](02-multi-account-identity-governance-and-landing-zones.md)).
- The readiness tracker from the Implementation section.

**Steps**

1. **Confirm the lineup (target 10 minutes).** From
   [aws.amazon.com/certification](https://aws.amazon.com/certification/),
   list the current certifications and note any retirement text appearing
   in a certification's name.

   **Expected result:** a list matching this chapter's table — or a
   documented difference, which means this chapter has aged and the
   currency check in Chapter 13 is due.

2. **Confirm three codes (target 10 minutes).** For three certifications
   you might sit, open each certification's own page and extract the code
   from its Skill Builder exam-prep link.

   **Expected result:** three codes confirmed from primary sources, not
   from this chapter.

3. **Choose and justify (target 15 minutes).** Fill the readiness tracker
   for only the certifications your role justifies, and write one sentence
   per row explaining why it is on your list.

   **Expected result:** a short, defensible plan — for most readers two or
   three certifications, not twelve.

4. **Create the cost guardrail (target 10 minutes).** In the sandbox
   account, create an AWS Budget with an alert threshold, as in
   [Chapter 7](07-observability-automation-performance-and-cost-governance.md).

   **Expected result:** a budget alarm that will email you before study
   labs become an expensive surprise.

5. **Negative test (target 5 minutes).** Deliberately look up one
   certification on a third-party "AWS certification list" site and compare
   its code and lineup against what you confirmed in steps 1–2.

   **Expected result:** you find at least one discrepancy — a stale code, a
   retired certification still listed, or a missing new one. This is the
   point of the exercise: it demonstrates why step 2 uses primary sources.

6. **Cleanup:** the budget alarm is free and worth keeping. Remove any
   other resources created while exploring, and confirm the sandbox has no
   running compute before you stop.

## Lab Verification

Complete this sign-off once the plan has been built from confirmed codes
and the budget guardrail is active. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The AWS certification program has four levels — foundational, associate,
professional, and specialty — and twelve current certifications, none of
which is a formal prerequisite for another. Levels describe assumed depth
and experience, so the right first exam is the one matching your role.
The `-C0x` suffix is the blueprint version and is the fastest way to spot
stale study material. The foundational tier (Cloud Practitioner CLF-C02,
AI Practitioner AIF-C01) exists mainly for people who need credible cloud
or AI fluency without a build role; working engineers should usually start
higher. Certifications last three years, and a higher-level pass generally
carries lower-level ones forward. Because the program churns, confirm every
code from AWS's own pages rather than from any summary, including this one.

- [ ] Can name the four levels and explain that none gates another.
- [ ] Can list the twelve current certifications and read the `-C0x`
      suffix.
- [ ] Knows CloudOps Engineer – Associate is the renamed SysOps
      Administrator.
- [ ] Can say who should and should not sit the foundational exams.
- [ ] Understands the three-year validity and how higher certifications
      extend lower ones.
- [ ] Has confirmed at least three exam codes from primary AWS sources.
- [ ] Completed the hands-on lab, including the budget guardrail and the
      third-party-discrepancy negative test.
