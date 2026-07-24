# Chapter 05: Professional Cloud Architect

## Learning Objectives

- Place Professional Cloud Architect as the flagship of the Google Cloud
  program and describe what distinguishes professional-level assessment
- Describe the architect's design surface: solution infrastructure,
  security and compliance, reliability, and business requirement analysis
- Explain the case-study format that distinguishes this exam from every
  other in the program
- Design a landing zone using the resource hierarchy, shared VPC, and
  organization policy
- Apply the two-year professional validity to a realistic portfolio
  decision

## Theory and Architecture

### The flagship

**Professional Cloud Architect** is Google Cloud's best-known
certification and the widest in scope: **2 hours, $200, 50–60 multiple
choice and multiple select questions**, valid **two years**, with no
prerequisites and a recommended three or more years of industry experience
including one or more designing and managing Google Cloud solutions
(verified 23 July 2026).

Note the validity: two years, against three for associate and foundational
([Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md)).
The most demanding certification in the program is also the one you must
retake soonest, at $200 each time.

### Case studies — the format that sets it apart

This exam is distinctive in using **published case studies**: fictional
company scenarios, available in advance on the exam guide, that a portion
of the questions reference. Each describes a business, its existing
technical estate, its business and technical requirements, and statements
from executives.

That has direct preparation consequences:

- **Read the case studies before exam day.** They are published; arriving
  cold wastes exam minutes on reading you could have done for free.
- **Practice extracting requirements.** The skill tested is turning
  prose — including vague executive statements — into technical
  requirements and then into a design. That is the actual job.
- **Expect the business constraint to decide.** Where several designs
  work, the stated cost ceiling, compliance boundary, or migration
  timeline selects one.

### The design surface

Google organizes the role into four areas:

- **Designing and planning a cloud solution architecture** — business and
  technical requirements, network/storage/compute design, migration
  planning, and future-proofing.
- **Managing and provisioning the solution infrastructure** — networking,
  compute, storage, and the operational plan around them.
- **Designing for security and compliance** — IAM design, organization
  policy, data protection, and regulatory considerations.
- **Analyzing and optimizing technical and business processes** —
  reliability, cost, and the operational feedback loop.

### The landing zone: hierarchy, shared VPC, and organization policy

The architectural core, and the ground most professional questions stand
on:

- **Resource hierarchy** — organization → folders → projects. Folders
  usually mirror environments or business units, because IAM and policy
  inherit downward
  ([Chapter 02](02-foundational-cloud-digital-leader-and-generative-ai-leader.md)).
- **Shared VPC** — a host project owns the network; service projects
  attach to it and run workloads on its subnets. This separates network
  administration from workload administration, which is the standard
  answer to "central networking team, many application teams."
- **Organization policy** — constraints applied at organization, folder,
  or project scope that restrict what *can* be configured, independent of
  IAM. Restricting external IP addresses or permitted resource locations
  are the canonical examples.

The distinction to hold clearly: **IAM decides who may act; organization
policy decides what may be configured.** It is the same split Azure draws
between RBAC and Azure Policy
([Volume XXXIII](../../volume-33-microsoft-azure-certifications/README.md),
Chapter 03), and it is examined the same way — a Project Owner can still
be blocked by an organization policy.

## Design Considerations

- **Read the case studies as preparation, not as exam-day reading.** They
  are published in advance; treating them as homework is free time.
- **Design from stated constraints.** Practice naming which requirement
  eliminates each alternative. That inversion is what professional
  scenarios reward.
- **Reach for Shared VPC when networking is centralized.** It is the
  standard answer to separating network ownership from workload ownership,
  and recognizing when it applies is worth more than memorizing its
  configuration.
- **Use organization policy for guardrails, IAM for permission.** A
  requirement phrased as "no resource may ever…" is organization policy; a
  requirement phrased as "team X may…" is IAM.
- **Budget the two-year clock.** At $200 every two years, decide whether
  this credential is worth holding continuously or earning once for a
  specific role.

## Implementation and Automation

### Reading the hierarchy an architect designs

```bash
gcloud organizations list
gcloud resource-manager folders list --organization=<ORG_ID>
gcloud projects list --format='table(projectId, parent.type, parent.id)'
```

### Shared VPC: host and service projects

```bash
# Enable a host project, then attach a service project
gcloud compute shared-vpc enable <HOST_PROJECT_ID>
gcloud compute shared-vpc associated-projects add <SERVICE_PROJECT_ID> \
  --host-project <HOST_PROJECT_ID>
```

```bash
# Confirm the association from the host side
gcloud compute shared-vpc list-associated-resources <HOST_PROJECT_ID>
```

### Organization policy: a guardrail IAM cannot express

```bash
# List effective constraints on a project
gcloud resource-manager org-policies list --project=<PROJECT_ID>
```

```bash
# Deny external IPs on VM instances — a guardrail that binds even Owners
gcloud resource-manager org-policies deny \
  compute.vmExternalIpAccess all --project=<PROJECT_ID>
```

## Validation and Troubleshooting

- **Prove the guardrail blocks, do not assume it.** The lab below attempts
  a violating action as a highly privileged principal, because an
  organization policy that has never denied anything is unverified.
- **Distinguish policy denial from permission denial.** An organization
  policy violation names the constraint; an IAM failure names a missing
  permission. The remedies are unrelated.
- **Check effective policy, not the assignment.** Constraints inherit, so
  a project may be governed by a policy set at the folder or organization
  level that does not appear in a project-scoped view.
- **Verify Shared VPC from both sides.** The host project lists associated
  service projects; a service project that believes it is attached but is
  not will fail at subnet selection.
- **Design readiness is spoken.** If you cannot justify a design decision
  aloud against "why not the cheaper option?", the knowledge is
  descriptive rather than architectural.

## Security and Best Practices

- Organization policy is a security control, not an administrative
  convenience: constraints such as restricting external IPs or resource
  locations prevent misconfiguration that IAM alone cannot.
- Design Shared VPC so the network team holds network admin roles in the
  host project and application teams hold none — the separation is the
  point.
- Avoid basic roles in any architecture you propose
  ([Chapter 03](03-associate-cloud-engineer.md)); an architecture diagram
  that hand-waves IAM is incomplete at this level.
- Data residency and encryption choices (CMEK versus Google-managed keys)
  are examinable and are usually driven by a stated compliance
  requirement — let the requirement select, not preference.
- Run lab work in a sandbox organization or project; organization policy
  changes are disruptive by design and can lock out legitimate work.

## References and Knowledge Checks

**References**

- [Professional Cloud Architect](https://cloud.google.com/certification/cloud-architect) —
  2 hours, $200, two-year validity, with the exam guide and case studies.
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Organization policy constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 03](03-associate-cloud-engineer.md) for the IAM foundation
  this builds on.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. What is distinctive about this exam's format, and what should you do
   about it before exam day?
2. Explain the difference between IAM and organization policy, and give a
   requirement that needs each.
3. When is Shared VPC the right answer, and what does it separate?
4. Why does the professional validity period change the portfolio
   calculation?
5. A Project Owner cannot create a VM with an external IP. What happened,
   and how would you confirm it?

## Hands-On Lab

**Objective:** Build the architectural guardrail an architect designs —
and prove an organization policy blocks a fully privileged principal,
which IAM alone could not.

**Cost note:** Organization policy operations are free. The VM attempt in
step 3 is expected to fail, so nothing is provisioned. Step 5 cleans up.

**Prerequisites**

- The sandbox project and budget alert from Chapter 01.
- Rights to set organization policy at project scope.

**Steps**

1. **Read the current policy (10 minutes).** List effective org policies
   on the sandbox project.

   **Expected result:** the current constraint set, including anything
   inherited from above.

2. **Apply the guardrail (10 minutes).** Deny
   `compute.vmExternalIpAccess` at project scope.

   **Expected result:** the constraint appears in the project's policy
   list.

3. **Negative test (15 minutes).** As a principal with Owner or Editor,
   attempt to create a VM with an external IP:

   ```bash
   gcloud compute instances create vm-should-fail --zone=us-central1-a \
     --machine-type=e2-micro --image-family=debian-12 \
     --image-project=debian-cloud
   ```

   **Expected result:** the request is **denied** and the error names the
   constraint. If it succeeds, the policy is not effective at the scope
   you think — diagnose that before continuing.

4. **Distinguish the failure (10 minutes).** Compare that error against an
   IAM denial (attempt an action outside your roles).

   **Expected result:** you can state, from the message alone, which
   mechanism blocked you.

5. **Design exercise (20 minutes).** Take a requirement — *"a central
   network team owns all subnets and VPC firewall rules; four application
   teams deploy workloads but must not alter networking"* — and write the
   design.

   **Expected result:** Shared VPC with a host project holding network
   admin roles and service projects attached, plus a statement of what you
   rejected and why.

6. **Cleanup:**

   ```bash
   gcloud resource-manager org-policies delete \
     compute.vmExternalIpAccess --project=<PROJECT_ID>
   ```

   Confirm the constraint is gone and no VM was created.

## Lab Verification

Complete this sign-off once the organization policy has been proven to
deny a privileged principal and the design exercise written. Until then,
the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Professional Cloud Architect is the flagship of the Google Cloud program —
2 hours, $200, and valid only **two years**, so the most demanding
credential is also the most frequently repurchased. It is the one exam
built on **published case studies**, which makes reading them in advance
free preparation and makes requirement extraction the skill under test.
Its architectural core is the landing zone: the organization → folder →
project hierarchy with downward inheritance, **Shared VPC** separating
network ownership from workload ownership, and **organization policy**
constraining what may be configured regardless of IAM — the same
"who may act versus what may exist" split Azure draws, and examined the
same way.

- [ ] Can explain the case-study format and how to prepare for it.
- [ ] Can distinguish IAM from organization policy with examples.
- [ ] Can say when Shared VPC is the right design and what it separates.
- [ ] Has proven an org policy denial against a privileged principal.
- [ ] Can defend a design aloud against a cheaper alternative.
- [ ] Completed the hands-on lab, including cleanup.
