# Chapter 08: The Expert Tier — AZ-305 and AZ-400

## Learning Objectives

- Identify the two Azure expert certifications and what distinguishes
  expert-level assessment from associate
- Describe the solutions architect's design surface: identity, governance,
  data, infrastructure, and business continuity
- Describe the DevOps engineer's surface: continuous delivery, dependency
  and configuration management, and feedback loops
- Track the 2026 updates to both certifications and prepare against the
  current blueprint rather than an older one
- Apply requirement-driven design reasoning, which is what both exams
  actually test

## Theory and Architecture

### Two expert certifications

| Certification | Exam | Note |
| --- | --- | --- |
| Azure Solutions Architect Expert | AZ-305 | Certification updated 17 April 2026 |
| DevOps Engineer Expert | AZ-400 | Certification updated 27 June 2026 |

Verified against Microsoft Learn on **23 July 2026**. Both remain current
with no announced retirement, and **both were updated in 2026** — recent
enough that material predating those dates may not match the live
blueprint.

Microsoft has historically recommended holding an associate certification
before an expert one (AZ-104 for AZ-305; AZ-104 or a developer credential
for AZ-400). Confirm the current requirement on the certification page —
Microsoft has moved between recommending and requiring prerequisites more
than once, and with AZ-204 retiring
([Chapter 05](05-the-retiring-associate-tier-az-204-and-az-500.md)) the
developer-side prerequisite is a detail worth checking rather than
assuming.

### AZ-305: designing infrastructure solutions

The solutions architect designs across four areas, and the exam's framing
is consistently *design*, not configuration:

- **Identity, governance, and monitoring** — Entra ID architecture,
  management-group and subscription structure, governance through Policy
  and RBAC at scale, and the monitoring strategy for an estate.
- **Data storage solutions** — relational and non-relational choices,
  data lifecycle, and integration and analytics patterns.
- **Business continuity** — backup, recovery, and high availability driven
  by explicit RTO and RPO targets.
- **Infrastructure solutions** — compute, application architecture,
  networking, and migration.

The distinguishing skill is **reasoning from requirements to a defensible
design**, including the trade-off you accepted and why. This is the same
discipline VMware's design certifications test
([Volume V](../../volume-05-vmware-virtualization/README.md), Chapters
17–19) and AWS's professional tier rewards
([Volume XVII](../../volume-17-aws-architecture-security/README.md),
Chapter 12): several answers work, and the question is which one satisfies
the stated cost, recovery, and compliance constraints.

### AZ-400: DevOps as a system

The DevOps Engineer certification is not "Azure DevOps the product." It
covers designing and implementing a delivery system: source control
strategy, build and release pipelines, dependency management,
infrastructure as code, secrets and configuration management, and the
feedback mechanisms — monitoring, alerting, and post-incident review — that
close the loop.

Its distinctive demand is **breadth across the software delivery
lifecycle**. A candidate strong on pipelines but weak on, say, dependency
versioning or feedback instrumentation will find the gaps exposed, because
the exam treats delivery as one system rather than a set of tools.

### RTO and RPO drive continuity design

The single most reliable AZ-305 pattern: a scenario states a recovery-time
objective and a recovery-point objective, and the correct answer is the
cheapest design that meets both.

- **RPO** — how much data you may lose — selects the replication and
  backup frequency.
- **RTO** — how long recovery may take — selects the standby model:
  backup-and-restore, pilot light, warm standby, or active-active.

Designs that over-deliver on both are wrong answers in an exam that states
a cost constraint, which is a genuinely useful habit to carry into real
work.

## Design Considerations

- **Prepare against the 2026 updates.** Both certifications were revised
  this year. Check each page's "updated on" note and prefer material
  published after it.
- **Study by constraint, not by service.** For each Azure service you
  know, practice naming the requirement that makes it the *wrong* choice.
  That inversion is what expert scenarios test.
- **Give governance disproportionate weight for AZ-305.** Management
  groups, subscription topology, Policy, and Entra ID architecture carry
  more weight at this level than their share of most study guides.
- **Treat AZ-400 as lifecycle-wide.** If preparation consists of pipeline
  practice alone, the dependency-management and feedback areas will be
  weak. Deliberately rehearse the parts you touch least.
- **Confirm the prerequisite before booking.** Microsoft's stated
  requirement has changed before, and the developer-side associate is
  currently retiring.

## Implementation and Automation

### Reading an estate's governance shape — the AZ-305 starting point

```bash
# Management group hierarchy is where architect-level governance lives
az account management-group list --query '[].{name:displayName, id:name}' -o table
```

```bash
# Policy assignments in force across the estate, with their scope
az policy assignment list --disable-scope-strict-match \
  --query '[].{policy:displayName, scope:scope, enforcement:enforcementMode}' -o table
```

### Expressing an RTO/RPO decision as a check

```text
# Fill this from a scenario before choosing services. The design follows
# from the two numbers, not from service preference.

Requirement          RPO: ______   RTO: ______
Data replication     (RPO drives)  e.g. GRS / geo-replication / log shipping
Standby model        (RTO drives)  backup-restore | pilot light | warm | active-active
Cost accepted        ____________
Trade-off accepted   ____________
Why not the cheaper alternative: ____________
```

### Verifying an infrastructure-as-code path — the AZ-400 habit

```bash
# A pipeline that has never been validated against a what-if is unproven
az deployment group what-if --resource-group rg-az305-lab \
  --template-file ./main.bicep --parameters ./main.parameters.json
```

## Validation and Troubleshooting

- **Design readiness is spoken, not recognized.** If you cannot justify a
  design decision aloud against "why not the cheaper option?", the
  knowledge is descriptive rather than architectural — the exact gap the
  expert tier exposes.
- **Check the blueprint date before trusting a resource.** Both
  certifications were updated in 2026; a course published earlier may
  omit current content.
- **Use `what-if` before deployment, always.** It is the infrastructure-
  as-code analogue of a dry run and the habit AZ-400 rewards; it also
  catches the drift that causes most "it worked in staging" failures.
- **Verify governance from the top down.** Policy assigned at a
  management group applies to everything beneath it; inspecting a single
  resource group will not reveal why a deployment was denied.
- **For continuity claims, test a restore.** A backup policy that has
  never been restored from is a plan, not a capability — the same
  standard Chapter 07 applies to databases.

## Security and Best Practices

- Architect-level access is broad. Use Privileged Identity Management for
  just-in-time elevation rather than standing Owner assignments, and
  design that pattern into the estates you propose.
- Secrets belong in Key Vault with managed identities, never in pipeline
  variables or repository files. This is examinable in AZ-400 and is the
  most common real-world failure it addresses.
- Design least-privilege service connections for pipelines: a deployment
  identity scoped to a subscription it does not need is how a compromised
  pipeline becomes an estate-wide incident.
- Governance is a security control, not an administrative one. Policy that
  denies non-compliant resources prevents misconfiguration that RBAC alone
  cannot.
- Run all lab work in the sandbox subscription; `what-if` is safe, but
  the deployments it previews are not.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Solutions Architect Expert](https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/) (AZ-305)
- [Microsoft Certified: DevOps Engineer Expert](https://learn.microsoft.com/en-us/credentials/certifications/devops-engineer/) (AZ-400)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 03](03-azure-administrator-az-104.md) for the governance
  foundation, and
  [Volume XVII, Chapter 12](../../volume-17-aws-architecture-security/chapters/12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md)
  for the comparable AWS tier.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name the two expert certifications, their codes, and when each was
   updated.
2. What distinguishes expert-level assessment from associate-level?
3. Explain how RPO and RTO each select a different part of a continuity
   design.
4. Why is AZ-400 not "the Azure DevOps product exam"?
5. Why does governance carry more weight in AZ-305 than its page count in
   most study guides suggests?

## Hands-On Lab

**Objective:** Practice the expert-tier skill directly — turning stated
requirements into a justified design — and adopt the `what-if` habit
before any deployment.

**Cost note:** `what-if` and read commands are free. The lab creates only a
resource group.

**Prerequisites**

- The sandbox subscription and budget alert from Chapter 01.
- Azure CLI authenticated; a simple Bicep template if you have one.

**Steps**

1. **Read the estate (10 minutes).** Run the management-group and policy
   queries and describe, in one paragraph, the governance shape they
   reveal.

   **Expected result:** an accurate description including which scope each
   policy applies at.

2. **Take a requirement (15 minutes).** Use: *"A line-of-business
   application must survive the loss of an Azure region with no more than
   15 minutes of data loss and be serving again within 4 hours, at the
   lowest cost that meets both."* Complete the RTO/RPO check from the
   Implementation section.

   **Expected result:** a filled check naming a replication approach, a
   standby model, and the cheaper alternative you rejected with a reason.

3. **Defend it (15 minutes).** Have a colleague — or a recording — ask
   "why not the cheaper option?" for each decision.

   **Expected result:** every decision justified without notes; mark any
   you could not defend.

4. **Change the constraint (10 minutes).** Re-answer with RTO relaxed to
   24 hours. State precisely which decisions change.

   **Expected result:** a cheaper design, with the changed decisions named
   — demonstrating that the numbers, not preference, drive the design.

5. **Negative test — `what-if` before deploy (15 minutes).** Run a
   `what-if` against a template with a deliberate error (a bad SKU name or
   missing parameter).

   **Expected result:** `what-if` reports the problem **without** creating
   anything. If it deploys instead, you ran the wrong command — which is
   exactly the habit this step exists to build.

6. **Cleanup:** delete any resource group created, and confirm no
   deployment succeeded during step 5.

## Lab Verification

Complete this sign-off once a design has been defended unaided and
`what-if` has caught a deliberate error without deploying. Until then, the
lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Azure expert tier holds **AZ-305** (Solutions Architect, updated 17
April 2026) and **AZ-400** (DevOps Engineer, updated 27 June 2026). Both
are current with no announced retirement, and both were revised this year —
so prefer material published after those dates. AZ-305 tests design
reasoning across identity and governance, data, continuity, and
infrastructure, with RPO and RTO selecting different halves of any
continuity design and cost constraints ruling out over-delivery. AZ-400
tests the delivery lifecycle as one system, not a product. At this tier the
readiness signal is spoken justification — being able to answer "why not
the cheaper option?" for every decision — and the operative habit is
`what-if` before deployment.

- [ ] Can name both expert certifications and their 2026 update dates.
- [ ] Can explain what expert-level assessment adds over associate.
- [ ] Can select replication from RPO and a standby model from RTO.
- [ ] Can explain why AZ-400 spans the whole delivery lifecycle.
- [ ] Has defended a design aloud against the cheaper alternative.
- [ ] Completed the hands-on lab, including the `what-if` negative test.
