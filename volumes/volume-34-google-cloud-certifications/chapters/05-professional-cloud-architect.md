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

## Design Exercise

Professional Cloud Architect is built on **published case studies**, so
this paper exercise precedes the command-driven walkthroughs below. Work it
from requirements to a defensible design with no console — turning stated
constraints into decisions you can defend is the skill the case-study
questions test.

**Scenario.** A media company runs a customer-facing web platform and an
analytics pipeline. Requirements, as a case study would state them:

1. Serve users in North America and Europe with **low latency**, from a
   single global entry point.
2. Survive the loss of an entire region with **no more than 5 minutes of
   data loss** for transactional data.
3. A **central network team** owns all connectivity; application teams
   deploy workloads but must not alter networking.
4. Analytics data **must not be exportable outside the organization**, even
   by an authorized analyst.
5. Cost must be **the lowest that meets the above** — no over-provisioning.

**Produce, for each, the decision and the constraint that forced it:**

| Design area | Decision | Forced by requirement | Rejected alternative (and why) |
| --- | --- | --- | --- |
| Global entry / load balancing | | | |
| Transactional data + RPO | | | |
| Network ownership separation | | | |
| Data-exfiltration control | | | |
| Compute | | | |

**A defensible answer** names: a **global external HTTP(S) load balancer**
(one anycast IP fronting multi-region backends) over a per-region DNS
scheme; **Spanner** (multi-region, strong consistency, ≤5-minute RPO) where
the transactional requirement needs all three properties, over a
regional Cloud SQL that fails requirement 2; **Shared VPC** with a host
project the network team owns and service projects for the app teams,
satisfying requirement 3; **VPC Service Controls** as the only mechanism
that stops exfiltration by an authorized identity (requirement 4 — IAM and
org policy do not satisfy it); and Cloud Run or GKE for compute by
statefulness. Every cell must trace to a quoted requirement.

**Then defend it.** Have a colleague — or a recorded self-review — ask "why
not the cheaper option?" for each row (why Spanner over Cloud SQL, why VPC
Service Controls over IAM). Any decision you cannot justify unaided is a
gap to close. This spoken defense is the same readiness signal the AWS
professional tier and the VMware VCDX defense reward
([Volume XVII](../../volume-17-aws-architecture-security/README.md),
Chapter 12; [Volume V](../../volume-05-vmware-virtualization/README.md),
Chapter 19).

## Hands-On Lab

These labs cover **every topic in the Professional Cloud Architect exam
guide**, section by section. The architect exam is design-weighted, so
several labs produce the *evidence* a design decision rests on and then
record the decision — that is the skill under test, and it is still a
walkthrough: run the command, compare the stated result, write the
conclusion. Mapping is in the
[volume README](../README.md#lab-coverage--professional-cloud-architect).

**Cost note:** these labs are almost entirely read operations and design
artifacts. The only billable resource is the Lab 5.9 bucket. Lab 5.19
cleans up.

**Prerequisites**

- The sandbox project and budget alert from
  [Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md).
- `gcloud` authenticated:

  ```bash
  export PROJECT_ID="$(gcloud config get-value project)"; echo "$PROJECT_ID"
  ```

  **Expected result:** your sandbox project ID.

- The published case studies from the exam guide, read in advance.

### Lab 5.1 — Infrastructure meeting business requirements *(topic 1.1)*

```bash
gcloud billing accounts list --format='table(name, displayName, open)'
```

**Expected result:** at least one account with `open: True`. Now write the
business-requirement chain for a case study:

```text
Business requirement : ______________________  (quote it verbatim)
Implied constraint   : ______________________  (cost / time / compliance)
Design decision      : ______________________
Rejected alternative : ______________________  because ______________
```

**Expected result:** a filled chain where the decision traces to a quoted
requirement — not to a preference.

### Lab 5.2 — Infrastructure meeting technical requirements *(topic 1.2)*

```bash
gcloud compute regions list --filter="name:(us-central1 europe-west1)" \
  --format='table(name, status, quotas[0].limit)'
```

**Expected result:** both regions `UP` with quota figures. Record which
technical requirement (latency, residency, quota headroom) each region
satisfies, and which it fails.

### Lab 5.3 — Designing network, storage, and compute *(topic 1.3)*

```bash
gcloud compute machine-types list --filter="zone:us-central1-a AND guestCpus>=4" \
  --format='table(name, guestCpus, memoryMb)' --limit=6
gcloud storage buckets list --format='value(name, location, storageClass)' 2>/dev/null | head -3
```

**Expected result:** a machine-type shortlist and any existing buckets.
Choose one machine type and one storage class, and state the requirement
that eliminated each rejected option.

### Lab 5.4 — Creating a migration plan *(topic 1.4)*

```bash
gcloud services list --available --filter="name:migrationcenter OR name:datamigration" \
  --format='value(name)' | head -5
```

**Expected result:** migration-related APIs listed as available. Then map
a workload to one of the 7 Rs (rehost, replatform, refactor, repurchase,
retire, retain, relocate) and state the constraint that selected it.

### Lab 5.5 — Envisioning future solution improvements *(topic 1.5)*

```bash
gcloud recommender recommendations list \
  --project="$PROJECT_ID" --location=us-central1-a \
  --recommender=google.compute.instance.MachineTypeRecommender \
  --format='table(name, primaryImpact.category)' 2>/dev/null | head -5
```

**Expected result:** either recommendations, or an empty list if the
project has no sustained workload history — both are informative. The
Recommender API is Google's own answer to "where would this design
improve next?"

### Lab 5.6 — Configuring network topologies *(topic 2.1)*

```bash
gcloud compute networks create vpc-pca --subnet-mode=custom
gcloud compute networks subnets create snet-pca-us \
  --network=vpc-pca --range=10.50.0.0/24 --region=us-central1
gcloud compute networks subnets create snet-pca-eu \
  --network=vpc-pca --range=10.51.0.0/24 --region=europe-west1
gcloud compute networks subnets list --network=vpc-pca \
  --format='table(name, region, ipCidrRange)'
```

**Expected result:** two subnets in different regions inside **one**
network — the global-VPC property that removes the need for peering
between regions.

### Lab 5.7 — Configuring individual storage systems *(topic 2.2)*

```bash
gcloud storage buckets create "gs://pca-lab-${PROJECT_ID}" \
  --location=us-central1 --uniform-bucket-level-access \
  --default-storage-class=NEARLINE
gcloud storage buckets describe "gs://pca-lab-${PROJECT_ID}" \
  --format='value(storageClass, location)'
```

**Expected result:** `NEARLINE US-CENTRAL1`. Nearline is the correct
answer only when access is infrequent — state the access pattern that
justified it.

### Lab 5.8 — Configuring compute systems *(topic 2.3)*

```bash
gcloud compute instance-templates create tpl-pca \
  --machine-type=e2-micro --subnet=snet-pca-us --region=us-central1 \
  --image-family=debian-12 --image-project=debian-cloud --no-address
gcloud compute instance-templates describe tpl-pca \
  --format='value(properties.machineType, properties.disks[0].initializeParams.sourceImage.basename())'
```

**Expected result:** `e2-micro` and a `debian-12-*` image. A template is
the unit a managed instance group scales from, which is why it is the
architect's compute artifact rather than a single VM.

### Lab 5.9 — Gemini Enterprise Agent Platform for ML workflows *(topic 2.4)*

```bash
gcloud services list --available \
  --filter="name:aiplatform OR name:discoveryengine" --format='value(name)'
```

**Expected result:** `aiplatform.googleapis.com` and
`discoveryengine.googleapis.com` among the available services. This topic
entered the guide with the **Google Cloud Next '26 refresh**
([Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md));
confirm the current guide wording before studying it in depth, since it is
the newest content on the exam.

### Lab 5.10 — Prebuilt solutions and APIs with Agent Platform *(topic 2.5)*

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services list --enabled --filter="name:aiplatform" --format='value(config.name)'
```

**Expected result:** `aiplatform.googleapis.com` now enabled. Enabling an
API is the architect-level decision point — it is where a prebuilt service
becomes available to a project, and where org policy can prevent it.

### Lab 5.11 — Designing for security *(topic 3.1)*

```bash
gcloud resource-manager org-policies list --project="$PROJECT_ID" \
  --format='table(constraint, listPolicy.allValues, booleanPolicy.enforced)'
```

**Expected result:** the constraints in force, inherited ones included. A
security design that names only IAM is incomplete — organization policy is
the half that binds Owners.

### Lab 5.12 — Designing for compliance *(topic 3.2)*

```bash
gcloud resource-manager org-policies describe \
  constraints/gcp.resourceLocations --project="$PROJECT_ID" --effective 2>/dev/null \
  || echo "no location constraint in force"
```

**Expected result:** either a location allow-list or the fallback message.
Data-residency compliance is expressed as this constraint, not as a
promise in a design document.

### Lab 5.13 — Analyzing and defining technical processes *(topic 4.1)*

```bash
gcloud logging read 'protoPayload.methodName:"SetIamPolicy"' \
  --limit=5 --format='table(timestamp, protoPayload.authenticationInfo.principalEmail)'
```

**Expected result:** recent IAM changes with the principal who made them —
or an empty set on a new project. This is the audit trail a change-control
process is built on.

### Lab 5.14 — Analyzing and defining business processes *(topic 4.2)*

```bash
gcloud billing budgets list --billing-account="$(gcloud billing projects describe "$PROJECT_ID" --format='value(billingAccountName)' | cut -d/ -f2)" \
  --format='table(displayName, amount.specifiedAmount.units)' 2>/dev/null \
  || echo "no budgets visible with current permissions"
```

**Expected result:** your budget from Chapter 01, or the permissions
message. A budget is where a business process (cost ownership) becomes a
technical control.

### Lab 5.15 — Advising development and operation teams *(topic 5.1)*

```bash
gcloud projects get-iam-policy "$PROJECT_ID" \
  --flatten='bindings[].members' --filter='bindings.role:roles/owner' \
  --format='value(bindings.members)'
```

**Expected result:** the Owner principals. Write the RACI line: who
deploys, who approves, who is paged. An architecture without named
ownership is not deployable advice.

### Lab 5.16 — Interacting with Google Cloud programmatically *(topic 5.2)*

```bash
gcloud compute instances list --format=json 2>/dev/null | head -20
gcloud compute instance-templates list --format='value(name)' --limit=3
```

**Expected result:** JSON output (possibly `[]`) and the template from
Lab 5.8. The architect is expected to read the API surface, not only the
console — `--format=json` is that surface.

### Lab 5.17 — Google Cloud Observability solutions *(topic 6.2)*

```bash
gcloud logging metrics list --format='table(name, filter)' --limit=5 2>/dev/null \
  || echo "no custom log metrics defined"
gcloud monitoring dashboards list --format='value(displayName)' 2>/dev/null | head -3
```

**Expected result:** existing metrics/dashboards, or the fallback
messages. Observability is a design input: name the SLI before the system
ships, per [Chapter 06](06-infrastructure-professionals-network-engineer-devops-engineer-and-developer.md).

### Lab 5.18 — Deployment, release management, and quality control *(topics 6.3, 6.5)*

```bash
gcloud compute instance-templates create tpl-pca-v2 \
  --machine-type=e2-small --subnet=snet-pca-us --region=us-central1 \
  --image-family=debian-12 --image-project=debian-cloud --no-address
gcloud compute instance-templates list --format='table(name, properties.machineType)'
```

**Expected result:** both `tpl-pca` and `tpl-pca-v2` listed. Two immutable
templates side by side **is** the release mechanism — a managed instance
group rolls between them, and rollback is selecting the previous template.

### Lab 5.19 — Negative test and cleanup

Prove a guardrail binds before tearing down. Apply the external-IP
constraint, then attempt a violating instance:

```bash
gcloud resource-manager org-policies deny compute.vmExternalIpAccess all \
  --project="$PROJECT_ID"
gcloud compute instances create vm-pca-fail --zone=us-central1-a \
  --machine-type=e2-micro --subnet=snet-pca-us \
  --image-family=debian-12 --image-project=debian-cloud
```

**Expected result:** the create **fails** with a message naming
`constraints/compute.vmExternalIpAccess`. That error — not the policy's
presence in a list — is the evidence the design decision is enforced.

```bash
gcloud projects delete "$PROJECT_ID" --quiet
gcloud projects describe "$PROJECT_ID" --format='value(lifecycleState)'
```

**Expected result:** `DELETE_REQUESTED`, removing the VPC, templates,
bucket, and policy together.

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
