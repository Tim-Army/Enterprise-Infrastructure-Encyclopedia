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

## Design Exercise

AZ-305 is a design exam built on case studies, so this paper exercise
precedes the command-driven walkthroughs below. Work it from requirements
to a defensible design with no console — the skill is turning stated
constraints into decisions you can defend against "why not the cheaper
option?"

**Scenario.** A retailer runs a line-of-business web application and its
SQL database on-premises. Requirements, quoted as an exam would state them:

1. Survive the loss of an entire Azure region with **no more than 15
   minutes of data loss** and be serving again within **1 hour**.
2. The database must remain **queryable with strong consistency**; the
   application is latency-sensitive within a region.
3. Personal data must **never leave the organization's Azure tenant**,
   even for an authorized administrator.
4. The identity team already runs **Microsoft Entra ID**; no new identity
   provider.
5. Cost must be **as low as the above allow** — do not over-provision.

**Produce, for each, the decision and the constraint that forced it:**

| Design area | Decision | Forced by requirement | Rejected alternative (and why) |
| --- | --- | --- | --- |
| Compute | | | |
| Relational data | | | |
| Business continuity (RPO/RTO) | | | |
| Data residency / exfiltration | | | |
| Identity | | | |
| Networking | | | |

**A defensible answer** names: zone-redundant App Service or AKS for
in-region HA; Azure SQL Database with an **auto-failover group** to a
second region (async geo-replication meets a 15-minute RPO; a read-write
listener meets the 1-hour RTO) over a costlier active-active or a
non-compliant single-region design; **VPC-equivalent isolation via VNet +
Private Endpoint plus a `resourceLocations` Azure Policy and, for
requirement 3, VNet/Private Link so data has no public path**; managed
identities against the existing Entra tenant rather than a new IdP; and
hub-spoke networking with the database reachable only privately. Each cell
must trace to a quoted requirement — a decision that traces to nothing is
unjustified, and a requirement no decision serves is unmet.

**Then defend it.** Have a colleague (or a recorded self-review) ask "why
not the cheaper option?" for every row. Any decision you cannot justify
unaided is a gap to close before the exam — that spoken defense is the
readiness signal, exactly as it is for the VMware VCDX defense
([Volume V](../../volume-05-vmware-virtualization/README.md), Chapter 19)
and the AWS professional tier
([Volume XVII](../../volume-17-aws-architecture-security/README.md),
Chapter 12).

## Hands-On Lab

These labs cover the **AZ-305 "Skills measured" outline** (Solutions
Architect), domain by domain at Microsoft's published weights, and touch
the AZ-400 DevOps surface where it adjoins. AZ-305 is a **design** exam, so
most labs read the evidence a design decision rests on and then record the
decision with its rejected alternative — that is the skill under test, and
it is still a walkthrough: run the command, compare the result, write the
conclusion. Mapping is in the
[volume README](../README.md#lab-coverage--az-305-solutions-architect).

**Cost note:** these labs are almost entirely read operations and `what-if`
previews. The only billable resource is the Lab 8.7 storage account.
Lab 8.19 cleans up.

**Prerequisites**

```bash
az group create --name rg-az305-lab --location eastus
az configure --defaults group=rg-az305-lab location=eastus
```

**Expected result:** `"provisioningState": "Succeeded"`.

### Domain 1 — Design identity, governance, and monitoring (25–30%)

### Lab 8.1 — Recommend a logging and monitoring solution *(topic 1.1)*

```bash
az monitor log-analytics workspace create --workspace-name law-az305
az monitor log-analytics workspace show --workspace-name law-az305 \
  --query "{name:name, sku:sku.name, retention:retentionInDays}" -o table
```

**Expected result:** the workspace with its SKU and retention days. Record
which log-routing target (Log Analytics vs. Event Hub vs. Storage) a
stated requirement — query, stream, or archive — selects.

### Lab 8.2 — Recommend authentication and identity management *(topic 1.2)*

```bash
az ad signed-in-user show --query "{upn:userPrincipalName, id:id}" -o table
```

**Expected result:** your identity. Then write the decision: managed
identity for Azure-to-Azure, workload identity federation for external,
service principal only where neither fits — with the constraint that
selected each.

### Lab 8.3 — Recommend a secrets, keys, and certificates solution *(topic 1.2)*

```bash
az keyvault create --name kv-az305-$RANDOM --enable-rbac-authorization true
az keyvault list --query "[].{name:name, rbac:properties.enableRbacAuthorization}" -o table
```

**Expected result:** a vault with `rbac: True`. RBAC-authorized Key Vault
(over access policies) is the current recommendation — note it as the
design default.

### Lab 8.4 — Recommend a management-group and governance structure *(topic 1.3)*

```bash
az account management-group list --query "[].{name:displayName, id:name}" -o table 2>/dev/null \
  || echo "management groups require tenant-level access"
az policy assignment list --disable-scope-strict-match \
  --query "[].{policy:displayName, enforcement:enforcementMode}" -o table | head -5
```

**Expected result:** the management-group hierarchy (or the access note)
and effective policy assignments. Governance design is a management-group
and Policy structure together — sketch the one your scenario needs.

### Domain 2 — Design data storage solutions (20–25%)

### Lab 8.5 — Recommend a relational data solution and tier *(topic 2.1)*

```bash
az sql db list-editions --location eastus \
  --query "[?name=='GeneralPurpose'].supportedServiceLevelObjectives[0].name" -o tsv | head -5
```

**Expected result:** service-level objectives (compute sizes) for General
Purpose. Record: Azure SQL DB vs. Managed Instance vs. SQL on a VM, and the
tier, against a stated performance and compatibility requirement.

### Lab 8.6 — Recommend a solution for database scalability and protection *(topic 2.1)*

```bash
az sql db list-editions --location eastus \
  --query "[?name=='Hyperscale'].name" -o tsv | head -1
```

**Expected result:** `Hyperscale`. Note when Hyperscale (rapid scale, large
DB) beats General Purpose, and pair the choice with a data-protection
recommendation (geo-replication vs. failover group) for the stated RPO.

### Lab 8.7 — Recommend semi-structured and unstructured storage *(topic 2.2)*

```bash
SA="stdata305$RANDOM"
az storage account create --name "$SA" --sku Standard_GRS --kind StorageV2 \
  --enable-hierarchical-namespace true
az storage account show --name "$SA" \
  --query "{sku:sku.name, adls:isHnsEnabled}" -o table
```

**Expected result:** `Standard_GRS True` — GRS for region durability, and
hierarchical namespace (ADLS Gen2) for analytics. State the requirement
that selected each.

### Lab 8.8 — Recommend data integration and analysis *(topic 2.3)*

```bash
az provider show --namespace Microsoft.DataFactory --query "registrationState" -o tsv 2>/dev/null \
  || echo "register Microsoft.DataFactory to use Data Factory"
```

**Expected result:** `Registered` or the register note. Data Factory
(orchestration) vs. Synapse (analytics) vs. Databricks is the integration
decision — record which the scenario's data shape and skills favor.

### Domain 3 — Design business continuity (15–20%)

### Lab 8.9 — Recommend backup and disaster recovery *(topic 3.1)*

```bash
az backup vault create --name rsv-az305 --location eastus
az backup vault show --name rsv-az305 --query "properties.provisioningState" -o tsv
```

**Expected result:** `Succeeded`. Then write the DR design from an
RTO/RPO pair: Azure Backup for restore, Site Recovery for replication,
zone-redundant vs. geo-redundant for the tier of loss survived.

### Lab 8.10 — Recommend a high-availability solution for compute *(topic 3.2)*

```bash
az vm list-skus --location eastus --zone --query "[?resourceType=='virtualMachines'].locationInfo[0].zones" -o tsv 2>/dev/null | head -1
```

**Expected result:** available zones (e.g. `1 2 3`). Availability zones
survive a datacenter; availability sets survive a rack. Record which a
stated SLA requires, and the HA choice for relational data (failover
groups / always-on).

### Domain 4 — Design infrastructure solutions (30–35%)

### Lab 8.11 — Recommend a compute solution *(topic 4.1)*

```bash
az vm list-sizes --location eastus --query "[?numberOfCores>=\`4\`].name" -o tsv | head -5
```

**Expected result:** a VM-size shortlist. Record the compute decision
across VM / container (AKS, Container Apps) / serverless (Functions) /
batch, and the requirement that eliminated each rejected option.

### Lab 8.12 — Recommend a messaging and event architecture *(topic 4.2)*

```bash
az provider show --namespace Microsoft.ServiceBus --query "registrationState" -o tsv
az provider show --namespace Microsoft.EventGrid --query "registrationState" -o tsv
```

**Expected result:** both `Registered`. The examinable distinction: Service
Bus for commands/queues, Event Grid for reactive events, Event Hubs for
high-throughput streams — pick by the message pattern, not preference.

### Lab 8.13 — Recommend API, caching, and config management *(topic 4.2)*

```bash
az provider show --namespace Microsoft.ApiManagement --query "registrationState" -o tsv
az provider show --namespace Microsoft.Cache --query "registrationState" -o tsv
```

**Expected result:** registration states. API Management fronts APIs; Azure
Cache for Redis is the caching recommendation; App Configuration + Key
Vault hold config and secrets. Record which the scenario needs.

### Lab 8.14 — Recommend an automated deployment solution *(topic 4.2 / AZ-400)*

```bash
cat > /tmp/az305.bicep <<'BICEP'
param location string = resourceGroup().location
resource law 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'law-deploy-${uniqueString(resourceGroup().id)}'
  location: location
  properties: { sku: { name: 'PerGB2018' } }
}
BICEP
az deployment group what-if --resource-group rg-az305-lab --template-file /tmp/az305.bicep | tail -4
```

**Expected result:** `+ create` for one workspace. Bicep/ARM with a
pipeline is the automated-deployment recommendation; `what-if` before apply
is the AZ-400 habit this shares.

### Lab 8.15 — Recommend a migration solution *(topic 4.3)*

```bash
az provider show --namespace Microsoft.Migrate --query "registrationState" -o tsv 2>/dev/null \
  || echo "register Microsoft.Migrate for Azure Migrate"
```

**Expected result:** `Registered` or the note. Map a workload to a
migration approach — rehost (Azure Migrate/ASR), replatform, or refactor —
and the database path (DMS online vs. offline) for the stated cutover
window.

### Lab 8.16 — Recommend a connectivity solution *(topic 4.4)*

```bash
az network vnet create --name vnet-az305 --address-prefix 10.30.0.0/16 \
  --subnet-name snet-a --subnet-prefix 10.30.1.0/24
az network vnet show --name vnet-az305 --query "{name:name, space:addressSpace.addressPrefixes[0]}" -o table
```

**Expected result:** the VNet. Record the hybrid choice — VPN Gateway
(cost, quick) vs. ExpressRoute (predictable latency, private) — and note
peering is not transitive, so a hub is needed to interconnect spokes.

### Lab 8.17 — Recommend a network-security and load-balancing solution *(topic 4.4)*

```bash
az network firewall list --query "[].name" -o tsv 2>/dev/null | head -1
echo "LB tiers: Basic (regional L4) | Standard (zonal L4) | App Gateway (L7+WAF) | Front Door (global L7)"
```

**Expected result:** any firewalls, plus the load-balancer decision table.
Choose by layer and scope; Azure Firewall or NVA in the hub is the
egress-control recommendation.

### Lab 8.18 — Negative test: prove a design guardrail enforces

```bash
az policy assignment create --name deny-sql-public \
  --policy "8c122334-9d20-4eb8-89ea-ac9a705b74ae" \
  --scope "$(az group show --name rg-az305-lab --query id -o tsv)" 2>&1 | tail -2
az sql server create --name sqlbad$RANDOM --admin-user azadmin \
  --admin-password "$(openssl rand -base64 18)Aa1!" \
  --enable-public-network true 2>&1 | tail -3
```

**Expected result:** the SQL server create is **denied**, the error naming
the policy — proving a design's compliance guardrail (public-network
denial) enforces regardless of the creator's rights. A design that names
the control but never tests it is unverified.

### Lab 8.19 — Cleanup

```bash
az group delete --name rg-az305-lab --yes --no-wait
az group exists --name rg-az305-lab
```

**Expected result:** `false` shortly after — the workspace, vault,
storage, VNet, and policy removed together.

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
