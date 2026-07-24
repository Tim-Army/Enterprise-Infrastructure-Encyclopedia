# Chapter 06: The AI-Centric Associate Tier — AI-103, AI-200, and AB-620

## Learning Objectives

- Identify the three new AI-centric associate certifications and what each
  is written for
- Explain what replaced the retired Azure AI Engineer (AI-102) and Azure
  Data Scientist (DP-100) certifications
- Recognize the `AB` code family's arrival as a signal about how Microsoft
  reads the emerging agent-builder role
- Choose between AI-103, AI-200, and AB-620 by the work you actually do
- Understand what these certifications assume coming in, since none is an
  entry-level credential

## Theory and Architecture

### A tier rebuilt around AI

The clearest single fact about Microsoft's Azure program in 2026 is that
the associate tier is being rebuilt around artificial intelligence.
Verified against Microsoft Learn on **23 July 2026**:

| Certification | Exam | Status |
| --- | --- | --- |
| Azure AI Engineer Associate | AI-102 | **Retired** |
| Azure Data Scientist Associate | DP-100 | **Retired** |
| Azure AI Apps and Agents Developer Associate | AI-103 | Current (new) |
| Azure AI Cloud Developer Associate | AI-200 | Current (new) |
| AI Agent Builder Associate | AB-620 | Current (new) |

Two established certifications retired; three new ones arrived. Read
alongside the closures in
[Chapter 05](05-the-retiring-associate-tier-az-204-and-az-500.md), this
is not incremental maintenance — it is a redefinition of what Microsoft
thinks an Azure associate does.

### AI-103: Azure AI Apps and Agents Developer

Microsoft describes this certification as validating expertise in
designing, developing, and deploying advanced Azure AI solutions **using
Python and Microsoft Foundry**. Two things are worth drawing out:

- It is **explicitly language-specific**. Naming Python in the
  certification description is unusual for Microsoft's Azure line and sets
  a clear expectation: this is a developer certification for people who
  write Python, not a configuration credential.
- It centers on **Microsoft Foundry**, the platform for building AI
  applications and agents. Familiarity with the Foundry workflow is
  assumed rather than taught by the surrounding Azure fundamentals.

This is the closest successor to the retired AI-102, but it is not a
rename — the emphasis has moved from consuming pre-built Azure AI services
toward building applications and agents on top of models.

### AI-200: Azure AI Cloud Developer

This certification validates the ability to design, build, and implement
AI solutions on Azure with a focus on **back-end services, scalable
architectures, and the full development lifecycle**.

Where AI-103 leans toward the AI application and agent surface, AI-200
leans toward the **engineering around it** — the services, scale, and
lifecycle that turn a working prototype into a system that runs. A reader
choosing between them should ask whether their work is more about what the
AI application does or more about the platform that carries it.

### AB-620: AI Agent Builder

The **AI Agent Builder Associate** certification introduces an entirely
new exam-code family, `AB`. As
[Chapter 01](01-the-azure-certification-program-levels-codes-and-renewal.md)
notes, Microsoft creates a code family when it judges a role distinct
enough to certify separately — so the arrival of `AB` is a substantive
statement that *agent builder* has become a job, not a task within
another job.

Its subject is the construction of AI agents. Because the family is new
and the certification recent, third-party preparation material is thin;
Microsoft Learn's own training is the realistic source.

### What is gone, and what that means

- **AI-102 (Azure AI Engineer)** — retired. Its page states the
  certification and its renewal assessment are retired. Existing holders
  keep the credential to expiry but cannot renew.
- **DP-100 (Azure Data Scientist)** — retired, on the same terms.

The machine-learning-operations and data-science subject matter has not
left Azure; the credential recognizing it has. Readers whose work is
data-science-heavy should look to the data track in
[Chapter 07](07-data-on-azure-dp-300-dp-420-and-dp-750.md), particularly
the new Databricks-based DP-750, and treat model development itself as
uncertified ground for now.

### None of these is an entry point

All three new certifications sit at **associate** level and assume real
development competence. They are not a first Azure certification. The
usual sequence is AZ-104 or a fundamentals credential first
(Chapters 02–03), then these — and for AI-103 specifically, working
Python.

## Design Considerations

- **Choose by what you build.** AI applications and agents in Python →
  AI-103. Back-end services and scalable architecture for AI systems →
  AI-200. Agents as the primary deliverable → AB-620.
- **Do not study AI-102 or DP-100 material.** Both are retired. Content
  aimed at them describes a credential that no longer exists, even where
  the underlying services remain.
- **Expect thin third-party material.** These are new certifications, and
  the `AB` family is brand new. Microsoft Learn's training paths and the
  official exam pages are the realistic preparation sources — which is
  also the safest, since nothing else is current.
- **Confirm the Python assumption before committing to AI-103.** A
  certification that names a language in its description will test it. If
  Python is not your working language, AI-200 is likely the better fit.
- **Watch this tier closely.** A tier that added three certifications and
  retired two within a year is the least stable part of the program.
  Chapter 09's currency check exists largely for this.

## Implementation and Automation

### Confirming the new lineup and codes

```bash
# The three new certifications and their codes, from Microsoft's pages.
for c in azure-ai-apps-and-agents-developer-associate \
         azure-ai-cloud-developer-associate \
         ai-agent-builder-associate; do
  printf '%-46s ' "$c"
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$c/" \
    | grep -oE '\b(AI|AB|AZ|DP)-[0-9]{3}\b' | sort -u | tr '\n' ' '
  echo
done
```

### Confirming the retirements

```bash
for c in azure-ai-engineer azure-data-scientist; do
  printf '%-24s ' "$c"
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$c/" \
    | sed 's/<[^>]*>/ /g' | tr -s ' ' \
    | grep -oE 'This certification[^.]{0,90}\.' | head -1
done
```

### Finding the official training for a new certification

```bash
# For new certifications, Microsoft Learn's own training is the only
# reliably current preparation. The certification page links it.
curl -s https://learn.microsoft.com/en-us/credentials/certifications/ai-agent-builder-associate/ \
  | grep -oE 'https://learn\.microsoft\.com/[a-z-]+/training/[^"]+' | sort -u | head -5
```

## Validation and Troubleshooting

- **Verify a code before believing any resource.** `AI-103`, `AI-200`, and
  `AB-620` are recent enough that a mistyped or guessed code is easy to
  propagate. Read it from the certification page.
- **Distinguish retired from superseded.** AI-102 is retired, and no
  Microsoft page declares a one-to-one successor. Describing AI-103 as
  "the new AI-102" overstates it — the scope moved.
- **Check whether training exists yet.** For very new certifications the
  exam can appear before a full learning path does. If the official
  training query above returns little, factor that into the schedule.
- **Treat absence of third-party material as expected, not as a red
  flag.** It reflects recency. It does, however, mean official sources are
  effectively the only option.

## Security and Best Practices

- AI application work involves model endpoints, keys, and often customer
  data. Apply the same credential hygiene as any other Azure workload:
  Key Vault for secrets, Entra ID authentication over keys where
  supported, and no secrets in notebooks or sample code.
- Responsible-AI considerations are examinable across this tier and
  operationally material — content filtering, grounding, evaluation, and
  the limits of what a model output can be trusted to assert.
- Agents act. An agent with credentials can take real actions, so scope
  its identity to least privilege exactly as you would a service
  principal, and prefer managed identities over stored keys.
- Practice in the sandbox subscription with a budget alert; AI inference
  is among the easier Azure costs to run up accidentally while iterating.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure AI Apps and Agents Developer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-apps-and-agents-developer-associate/) (AI-103)
- [Microsoft Certified: Azure AI Cloud Developer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-cloud-developer-associate/) (AI-200)
- [Microsoft Certified: AI Agent Builder Associate](https://learn.microsoft.com/en-us/credentials/certifications/ai-agent-builder-associate/) (AB-620)
- [Microsoft Certified: Azure AI Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/) (AI-102 — retired)
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 05](05-the-retiring-associate-tier-az-204-and-az-500.md)
  for the developer certification this tier displaces.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name the three new AI-centric associate certifications and their codes.
2. Which two certifications retired, and what happens to holders?
3. What does the arrival of the `AB` code family signal?
4. Distinguish AI-103 from AI-200 by the work each is written for.
5. Why is third-party study material a particularly poor choice for this
   tier right now?

## Hands-On Lab

These labs cover the AI-centric associate tier: **AI-103** (Azure AI Apps
and Agents Developer — Python and Microsoft Foundry), **AI-200** (Azure AI
Cloud Developer — back-end AI services and lifecycle), and **AB-620** (AI
Agent Builder). These certifications are **new** (Chapter 06 body), so
their published skills outlines are still thin — these labs exercise the
stated scope (the Azure AI service surface, Foundry, and agent building)
against what is verifiable today. **Re-check each exam guide before relying
on this**, and treat generative-AI content as the fastest-moving in the
program. Mapping is in the
[volume README](../README.md#lab-coverage--the-ai-centric-associate-tier).

**Cost note:** these labs are availability checks and one small Azure AI
resource. Azure OpenAI / AI inference bills per token — Lab 6.9 deletes
the resource group. Do not leave a deployed model endpoint running.

**Prerequisites**

```bash
az group create --name rg-ai-lab --location eastus
az configure --defaults group=rg-ai-lab location=eastus
```

**Expected result:** `"provisioningState": "Succeeded"`.

### Lab 6.1 — Locate the Azure AI service surface *(AI-103 / AI-200 foundations)*

```bash
az cognitiveservices account list-kinds -o tsv | tr '\t' '\n' | grep -iE "AIServices|OpenAI"
```

**Expected result:** `AIServices` and `OpenAI` among the kinds. The
multi-service `AIServices` resource is the modern single endpoint for
Vision, Language, Speech, and OpenAI — the surface both developer
certifications build on.

### Lab 6.2 — Create a multi-service Azure AI resource *(AI-200 back-end)*

```bash
AI="ai-svc-$RANDOM"
az cognitiveservices account create --name "$AI" --kind AIServices --sku S0 \
  --custom-domain "$AI" --yes
az cognitiveservices account show --name "$AI" \
  --query "{name:name, endpoint:properties.endpoint, kind:kind}" -o table
```

**Expected result:** the resource with an `https://...cognitiveservices.azure.com/`
endpoint. A custom domain is required for token-based (Entra) auth — the
recommended pattern over keys.

### Lab 6.3 — Authenticate to AI services without keys *(AI-200 security)*

```bash
az cognitiveservices account keys list --name "$AI" --query "key1" -o tsv | head -c 8; echo "... (key exists)"
echo "Prefer: managed identity + 'Cognitive Services User' role over these keys"
```

**Expected result:** a key prefix, plus the guidance. AI-200 rewards
identity-based access to model endpoints over distributed keys — the same
credential-hygiene rule as the rest of Azure.

### Lab 6.4 — Microsoft Foundry: the app and agent platform *(AI-103)*

```bash
az extension add --name ml 2>/dev/null; az extension show --name ml --query "version" -o tsv 2>/dev/null \
  || echo "Azure AI Foundry / ML tooling — install the 'ml' CLI extension"
az provider show --namespace Microsoft.MachineLearningServices --query "registrationState" -o tsv
```

**Expected result:** the `ml` extension version and a `Registered`
provider. AI-103 names **Microsoft Foundry** and **Python** explicitly —
Foundry hubs/projects are where apps and agents are built, and the SDK is
Python.

### Lab 6.5 — Deploy a model (the serving surface) *(AI-103 / AB-620)*

```bash
az cognitiveservices account deployment list --name "$AI" \
  --query "[].{name:name, model:properties.model.name}" -o table 2>/dev/null \
  || echo "no deployments yet — a deployment is a served model version"
```

**Expected result:** an empty list on a fresh resource. The examinable
point: a **model** and a **deployment** are distinct — you deploy a model
version to get a callable endpoint, and an agent calls that endpoint.

### Lab 6.6 — Agent building concepts *(AB-620)*

```text
# An agent = a model deployment + tools (function calling) + grounding +
# an orchestration loop. The AB-620 skill is composing these safely:
#   - tools the agent may call (each scoped to least privilege)
#   - grounding sources so answers are sourced, not invented
#   - guardrails (content filters, output validation)
Record, for a simple "order status" agent: which tool it calls, what
grounds its answer, and what it is NOT allowed to do.
```

**Expected result:** a written agent spec naming a tool, a grounding
source, and an explicit prohibition. Agents *act*, so scoping the tool's
identity to least privilege is the security core AB-620 tests.

### Lab 6.7 — Responsible AI and content safety *(all three, cross-topic)*

```bash
az cognitiveservices account list-kinds -o tsv | tr '\t' '\n' | grep -i "ContentSafety" \
  || echo "Azure AI Content Safety — moderation for prompts and responses"
```

**Expected result:** `ContentSafety` (or the note). Content filtering,
grounding, and evaluation are examinable and operationally real —
responsible AI is a build requirement, not a checkbox.

### Lab 6.8 — Negative test: prove endpoint access needs a role/key

```bash
ENDPOINT=$(az cognitiveservices account show --name "$AI" --query "properties.endpoint" -o tsv)
curl -s -o /dev/null -w "%{http_code}\n" "${ENDPOINT}language/:analyze-text?api-version=2023-04-01" \
  -H "Content-Type: application/json" -d '{"kind":"LanguageDetection","analysisInput":{"documents":[{"id":"1","text":"hello"}]}}'
```

**Expected result:** `401` — the call is **rejected** without an
authentication header, even though the endpoint URL is public. That
401-without-credentials is the proof that the AI endpoint is secured by
identity, not obscurity — the AI-200 security lesson. Add the key or a
bearer token and the same call returns `200`.

### Lab 6.9 — Cleanup

```bash
az group delete --name rg-ai-lab --yes --no-wait
az group exists --name rg-ai-lab
```

**Expected result:** `false` shortly after — the AI resource and any
model deployments removed together. Token-billed inference stops only when
the deployment is gone, so confirm deletion.

## Lab Verification

Complete this sign-off once all three codes and both retirements have been
confirmed from Microsoft and a choice recorded. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsoft has rebuilt the Azure associate tier around AI: **AI-102 and
DP-100 are retired**, and **AI-103** (Azure AI Apps and Agents Developer,
explicitly Python and Microsoft Foundry), **AI-200** (Azure AI Cloud
Developer, back-end services and lifecycle), and **AB-620** (AI Agent
Builder, on an entirely new code family) have arrived. None is a one-to-one
replacement for what closed, and none is an entry-level credential — all
three assume real development competence and follow, rather than precede,
AZ-104 or a fundamentals certification. Because the tier is this new,
Microsoft Learn is effectively the only current preparation source, and
third-party material still promoting AI-102 is the clearest available proof
of why primary sources matter here.

- [ ] Can name the three new certifications and their codes.
- [ ] Knows AI-102 and DP-100 are retired and what that means for holders.
- [ ] Can explain what a new code family such as `AB` signals.
- [ ] Can distinguish AI-103 from AI-200 by intended work.
- [ ] Has confirmed every code and retirement from Microsoft's own pages.
- [ ] Completed the hands-on lab, including the negative test.
