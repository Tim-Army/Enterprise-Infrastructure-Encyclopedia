# Chapter 02: Fundamentals — AZ-900, AI-901, and DP-900

## Learning Objectives

- Distinguish the three Azure fundamentals certifications and the audience
  each is written for
- Explain the AI-900 to **AI-901** renumbering, when it took effect, and
  what it means for study material you may already own
- Decide whether a fundamentals certification is worth your time, given
  that none is a prerequisite for anything
- Describe the core Azure concepts all three assume: subscriptions,
  resource groups, regions, and the shared responsibility model
- Use Microsoft Learn's free training paths, which cover the whole
  fundamentals tier at no cost

## Theory and Architecture

### Three fundamentals certifications, three audiences

| Certification | Exam | Written for |
| --- | --- | --- |
| Azure Fundamentals | AZ-900 | Anyone needing credible cloud fluency — including non-engineers |
| Azure AI Fundamentals | AI-901 | Those needing AI/ML vocabulary and the Azure AI service surface |
| Azure Data Fundamentals | DP-900 | Those needing core data concepts and Azure data services |

All three are **beginner level**, assume no prior Azure experience, and —
unlike the role-based certifications in later chapters — **do not
expire**. That single property makes them unusually low-maintenance: earn
once, hold indefinitely.

### AZ-900: the platform vocabulary

AZ-900 covers cloud concepts (shared responsibility, service and
deployment models, the economic case), Azure architecture and services
(regions, availability zones, resource groups, subscriptions, management
groups; compute, networking, storage, identity), and Azure management and
governance (cost management, SLAs, policy, RBAC, monitoring tooling).

Its real function is a **shared vocabulary**. A team where the project
manager, the finance analyst, and the engineer all mean the same thing by
"resource group" and "availability zone" argues less. That is a legitimate
reason to sit it even where the technical content is already familiar.

### AI-901 replaced AI-900

The Azure AI Fundamentals exam was renumbered. **AI-900 retired on 30 June
2026 and was replaced by AI-901**, and the certification itself was
updated on 15 April 2026 (verified against Microsoft Learn, 23 July 2026).

The practical consequence is unforgiving: any course, practice bank, or
book targeting **AI-900 is now aimed at a retired exam**. The subject area
did not vanish — generative AI and the Azure AI service surface moved
considerably between the two versions — but the code on the cover is the
fastest currency test available. Check it before spending money.

AI-901 covers AI workload types and considerations, responsible-AI
principles, and the fundamentals of machine learning, computer vision,
natural language processing, and generative AI as delivered by Azure AI
services.

### DP-900: the data vocabulary

DP-900 covers core data concepts (relational and non-relational data,
analytics workloads) and how Azure delivers them — Azure SQL, Cosmos DB,
Azure Storage, and the analytics stack. It is the on-ramp for the data
track that Chapter 07 develops through DP-300, DP-420, and DP-750.

### The concepts all three assume

Whichever you sit, the same platform scaffolding underlies it:

- **Subscription** — the billing and quota boundary, and the unit most
  governance attaches to.
- **Resource group** — a lifecycle container; resources in one are
  typically created, managed, and deleted together.
- **Management group** — a container *above* subscriptions, for applying
  policy across many of them.
- **Region and availability zone** — the placement and resilience
  primitives.
- **Shared responsibility** — what Microsoft secures versus what you
  secure, which shifts with the service model (IaaS to PaaS to SaaS).

## Design Considerations

- **Skip the fundamentals tier if you already work on Azure.** For an
  engineer heading toward AZ-104 (Chapter 03), AZ-900 certifies knowledge
  the associate exam tests anyway. Its value is for non-builders and for
  team vocabulary.
- **Never study AI-900 material.** The exam is retired. If a resource says
  AI-900 on the cover, it is aimed at content that no longer exists in the
  live blueprint.
- **Fundamentals do not expire — role-based ones do.** This asymmetry
  makes fundamentals a genuinely permanent credential and is worth knowing
  when comparing the total cost of a certification portfolio.
- **DP-900 is the cheapest way to test data-track interest.** Before
  committing to DP-300 or DP-420 (Chapter 07), DP-900 establishes whether
  the subject area suits you at low cost.
- **All three are covered free.** Microsoft Learn's training paths span
  the entire fundamentals tier at no cost, which makes paid courses at
  this level hard to justify.

## Implementation and Automation

### Confirming which AI fundamentals exam is live

```bash
# The retired exam's page states its replacement explicitly.
curl -s https://learn.microsoft.com/en-us/credentials/certifications/exams/ai-900/ \
  | sed 's/<[^>]*>/ /g' | tr -s ' ' \
  | grep -oE 'The AI-900 exam[^.]{0,120}\.'
```

### Exploring the concepts the exams assume

```bash
# Subscriptions, resource groups, and regions are the scaffolding all
# three fundamentals exams rest on. Read your own tenant's shape.
az account show --query '{subscription:name, id:id, tenant:tenantId}' -o table
```

```bash
az group list --query '[].{name:name, location:location}' -o table
```

```bash
# Which regions are available to you, and which support availability zones
az account list-locations \
  --query '[?metadata.regionType==`Physical`].{region:name, geo:metadata.geographyGroup}' \
  -o table | head -20
```

## Validation and Troubleshooting

- **Code check before purchase.** For AI fundamentals the only acceptable
  code is **AI-901**. Seeing AI-900 on a resource is disqualifying, not a
  minor version lag.
- **Confirm the non-expiry claim for your specific certification.**
  Fundamentals do not expire; role-based certifications renew annually.
  Check your Microsoft Learn profile rather than assuming which category a
  credential falls into.
- **Vocabulary test.** If you cannot explain the difference between a
  resource group and a management group, or say who secures what under
  shared responsibility for a PaaS service, the fundamentals content is
  not yet solid regardless of hands-on experience.
- **Free training first.** If a paid fundamentals course is under
  consideration, compare it against Microsoft Learn's free path for the
  same exam before buying.

## Security and Best Practices

- Even at fundamentals level, do exploration in a sandbox subscription
  with a budget alert (Chapter 01), not in a production tenant.
- `az account show` output includes tenant and subscription identifiers —
  treat them as sensitive when sharing terminal output or screenshots.
- Shared responsibility is examinable *and* operationally important:
  misplacing the boundary is how real misconfigurations happen, so learn
  it as a working model rather than a diagram to recall.
- Do not use unauthorized practice material; at this tier especially, the
  free official training makes it entirely unnecessary.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) (AZ-900)
- [Microsoft Certified: Azure AI Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/) (AI-901)
- [Microsoft Certified: Azure Data Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-fundamentals/) (DP-900)
- [Microsoft Learn training](https://learn.microsoft.com/en-us/training/) —
  free paths covering all three exams.
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 01](01-the-azure-certification-program-levels-codes-and-renewal.md)
  for the program map and renewal model.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name the three fundamentals certifications and the audience each
   targets.
2. What happened to AI-900, when, and what replaced it?
3. Why do fundamentals certifications cost less to hold than role-based
   ones?
4. Distinguish a resource group from a management group, and give a case
   for each.
5. Under shared responsibility, what changes as you move from IaaS to
   PaaS?

## Hands-On Lab

These labs cover the "Skills measured" domains for all three fundamentals
certifications: **AZ-900** (cloud concepts; architecture and services;
management and governance), **AI-901** (AI, ML, computer vision, NLP, and
generative AI on Azure), and **DP-900** (core data concepts; relational;
non-relational; analytics). Fundamentals are knowledge credentials, so
these read the platform facts each exam asks about rather than building
production systems — each remains a walkthrough with the command and the
expected result. Mapping is in the
[volume README](../README.md#lab-coverage--fundamentals).

**Cost note:** every command here is a read or an availability check.
Nothing billable is created.

**Prerequisites**

```bash
az account show --query "{sub:name, id:id, tenant:tenantId}" -o table
```

**Expected result:** your subscription and tenant — the scaffolding all
three exams assume.

### Lab 2.1 — Describe cloud concepts *(AZ-900, 25–30%)*

```bash
az account list-locations --query "[?metadata.regionType=='Physical'].{region:name, geo:metadata.geographyGroup}" -o table | head -8
```

**Expected result:** physical regions grouped by geography. Regions,
geographies, and availability zones are the resilience primitives cloud
concepts covers; naming a region pair for a workload is the skill.

### Lab 2.2 — Describe Azure architecture and services *(AZ-900, 35–40%)*

```bash
az provider list --query "[?registrationState=='Registered'].namespace" -o tsv | head -10
```

**Expected result:** registered resource providers (Compute, Network,
Storage, …) — the service surface. AZ-900 is knowing these exist and what
each does, not operating them.

### Lab 2.3 — Describe Azure management and governance *(AZ-900, 30–35%)*

```bash
az group list --query "[].{name:name, location:location}" -o table
az consumption budget list --query "[].name" -o tsv 2>/dev/null || echo "no budgets (or billing-scope perms needed)"
```

**Expected result:** resource groups, and any budgets. Cost management,
resource groups, RBAC, and Policy are the governance tools AZ-900 names.

### Lab 2.4 — AI workloads and considerations *(AI-901, 15–20%)*

```bash
az cognitiveservices account list-kinds -o tsv | tr '\t' '\n' | head -12
```

**Expected result:** the Cognitive Services / Azure AI kinds (Vision,
Language, Speech, OpenAI, …). Recognizing which AI workload maps to which
service is the section-1 skill; responsible-AI considerations pair with it.

### Lab 2.5 — Machine learning fundamentals on Azure *(AI-901, 15–20%)*

```bash
az provider show --namespace Microsoft.MachineLearningServices --query "registrationState" -o tsv 2>/dev/null || echo "register to use Azure ML"
```

**Expected result:** `Registered` or the note. Azure Machine Learning is
the platform; the fundamentals point is distinguishing regression /
classification / clustering, not building a model.

### Lab 2.6 — Computer vision workloads *(AI-901, 15–20%)*

```bash
az cognitiveservices account list-skus --kind ComputerVision --location eastus \
  --query "[].name" -o tsv 2>/dev/null | head -3 || echo "Computer Vision SKUs (F0 free, S1 standard)"
```

**Expected result:** Vision SKUs including a free `F0` tier. Image
classification, object detection, OCR, and face are the vision capabilities
the section lists.

### Lab 2.7 — Natural language and generative AI workloads *(AI-901, 20–25%)*

```bash
az cognitiveservices account list-kinds -o tsv | tr '\t' '\n' | grep -iE "openai|language" || echo "OpenAI + Language kinds"
```

**Expected result:** `OpenAI` and `Language` among the kinds. Generative AI
on Azure (the highest-weighted AI-901 section) is delivered through Azure
OpenAI; know its use cases and the responsible-AI guardrails.

### Lab 2.8 — Core data concepts *(DP-900, 25–30%)*

```bash
az sql server list --query "[].name" -o tsv 2>/dev/null | head -3
echo "Data roles: administrator | engineer | analyst; workloads: transactional (OLTP) vs analytical (OLAP)"
```

**Expected result:** any SQL servers, plus the concept summary.
Structured / semi-structured / unstructured and OLTP vs OLAP are the
core-concepts vocabulary DP-900 tests.

### Lab 2.9 — Relational data on Azure *(DP-900, 20–25%)*

```bash
az sql db list-editions --location eastus --query "[].name" -o tsv | sort -u | head -6
```

**Expected result:** service tiers (Basic, Standard, GeneralPurpose,
Hyperscale, …). Azure SQL Database, Managed Instance, and SQL on a VM are
the relational options; the tier is the sizing decision.

### Lab 2.10 — Non-relational data on Azure *(DP-900, 15–20%)*

```bash
az cosmosdb list-capabilities -o tsv 2>/dev/null | head -5 || echo "Cosmos DB APIs: NoSQL, MongoDB, Cassandra, Gremlin, Table"
```

**Expected result:** Cosmos DB capabilities/APIs. Cosmos DB (document,
key-value, graph) and Table/Blob storage are the non-relational options —
choose by access pattern.

### Lab 2.11 — Analytics workload on Azure *(DP-900, 25–30%)*

```bash
az provider show --namespace Microsoft.Synapse --query "registrationState" -o tsv 2>/dev/null || echo "register Microsoft.Synapse"
```

**Expected result:** `Registered` or the note. Azure Synapse, Data
Factory, and Microsoft Fabric are the analytics surface; the modern data
warehouse pattern (ingest → store → prep → serve) is the examinable shape.

### Lab 2.12 — Negative test: recognize a disabled capability

```bash
az cognitiveservices account list --resource-group rg-does-not-exist 2>&1 | head -2
```

**Expected result:** an error naming the missing resource group — not an
empty list. Telling "not enabled / not present" from "nothing there" is
the foundational reading skill all three exams reward. Nothing to clean up;
no resources were created.

## Lab Verification

Complete this sign-off once the resource group has been created, explained,
and cleaned up. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The fundamentals tier holds three non-expiring certifications: AZ-900 for
platform vocabulary, **AI-901** for AI vocabulary, and DP-900 for data
vocabulary. AI-901 replaced AI-900, which retired on 30 June 2026 — so any
AI-900 study material is aimed at a dead exam, and the code on the cover is
the fastest currency check you have. None of the three is a prerequisite
for anything, and all three are covered by free Microsoft Learn training,
which makes them cheap to earn and cheap to hold. For a working Azure
engineer they are usually skippable; for non-builders and for establishing
a shared team vocabulary, they earn their place.

- [ ] Can name the three fundamentals certifications and their audiences.
- [ ] Knows AI-900 retired on 30 June 2026 and AI-901 replaced it.
- [ ] Can explain why fundamentals cost less to hold than role-based
      certifications.
- [ ] Can distinguish subscription, resource group, and management group.
- [ ] Can state the shared responsibility boundary across service models.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
