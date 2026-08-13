# Chapter 07: AI and Copilot Certifications

## Learning Objectives

- Enumerate the current AI-family certifications and exam codes.
- Explain the AI-900 to AI-901 Fundamentals renumber.
- Distinguish the AI engineer, apps/agents developer, and multi-agent expert roles.
- Recognize the fast-moving Copilot and agent-administration credentials.
- Build a study path for an AI engineer or agent-focused role.

## Theory and Architecture

The **AI** family is Microsoft's fastest-changing certification area, expanded
sharply in 2025–2026 as **Azure AI Foundry**, **Copilot**, and **agents**
became central. As verified on Microsoft Learn (26 July 2026):

- **Microsoft Certified: Azure AI Fundamentals** — exam **AI-901**
  (Fundamentals). Core AI concepts and Azure AI services. **AI-901 replaced
  the retired AI-900** — a renumber worth remembering.
- **Microsoft Certified: Azure AI Engineer Associate** — exam **AI-102**
  (Associate). Build, deploy, and manage AI solutions with Azure AI services.
- **Microsoft Certified: Azure AI Apps and Agents Developer Associate** — exam
  **AI-103** (Associate). Build generative-AI applications and agents.
- **Microsoft Certified: Azure AI Cloud Developer Associate** — exam **AI-200**
  (Associate).
- **Microsoft Certified: Multi-Agent AI Solutions Expert** — exam **AI-500**
  (Expert; beta). Design and operate multi-agent AI systems.
- The data/AI **operations** exam **AI-300** (operationalizing ML and
  generative-AI solutions — MLOps/GenAIOps).
- The **Expansion "AB" family** of AI/agent certifications, each now with its own
  exam code: **AB-100** (Agentic AI Business Solutions Architect), **AB-410**
  (Building Intelligent Applications), **AB-620** (Designing and Building
  Integrated AI Solutions — Copilot Studio), **AB-730** (AI Business
  Professional), **AB-731** (AI Transformation Leader), and **AB-900**
  (Microsoft 365 Copilot and Agent Administration Fundamentals).

Two **business-level** credentials round out the family — **AI Business
Professional** and **AI Transformation Leader** — for non-engineering roles.
And crucially for administrators, **Microsoft 365 Certified: Copilot and Agent
Administration Fundamentals** certifies governing Copilot and agents in
Microsoft 365 — the administrative counterpart to the developer credentials,
and directly relevant to the oversharing/labeling governance covered in Volume
XXXVII (Chapter 11).

## Design Considerations

This family changes monthly — **verify every exam code and status on Microsoft
Learn**, and expect **betas**. Lead with **AI-901** (Fundamentals). Engineers
building on Azure AI take **AI-102**; those building **generative-AI apps and
agents** take **AI-103** (and watch AI-200 and the agent-builder credentials).
The **AI-500 Multi-Agent Expert** is the senior, design-level credential for
multi-agent systems. Data scientists coming from **DP-100** (Chapter 06) may
add the AI operations exam (**AI-300**).

For **administrators and business roles**, the **Copilot and Agent
Administration Fundamentals** credential is the practical one — it maps to
governing Copilot's data access, agents, and licensing in Microsoft 365. The
**business** credentials (AI Business Professional, AI Transformation Leader)
suit leaders and consultants rather than builders.

## Implementation and Automation

Verify the renumber and the newer credentials from Microsoft Learn:

```bash
for slug in azure-ai-fundamentals azure-ai-engineer azure-ai-apps-and-agents-developer-associate \
            multi-agent-ai-solutions-expert copilot-and-agent-administration-fundamentals; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bAI-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> ${code:-'(assessment/beta - see page)'}"
done
# azure-ai-fundamentals -> AI-901  (replaced AI-900)
# azure-ai-engineer -> AI-102
# multi-agent-ai-solutions-expert -> AI-500 (beta)
```

## Validation and Troubleshooting

Map the main credentials:

| Credential | Exam | Tier | Role |
| --- | --- | --- | --- |
| Azure AI Fundamentals | AI-901 | Fundamentals | Gateway (ex-AI-900) |
| Azure AI Engineer | AI-102 | Associate | AI engineer |
| Azure AI Apps and Agents Developer | AI-103 | Associate | GenAI/agent developer |
| Azure AI Cloud Developer | AI-200 | Associate | AI cloud developer |
| Multi-Agent AI Solutions Expert | AI-500 | Expert (beta) | Multi-agent designer |
| Copilot and Agent Administration Fundamentals | assessment | Fundamentals | Copilot/agent admin |

Common pitfalls: studying **AI-900** (renumbered to **AI-901**); assuming the
AI family is stable (it is the most volatile — re-verify constantly); and
treating **Copilot administration** as a developer topic when it is an
**administration/governance** credential tied to Microsoft 365 data protection
(Volume XXXVII, Chapters 10–11). Many of these are **beta** — beta exams score
after the beta period, so plan timing accordingly.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments** where
they exist, and practice in **Azure AI Foundry** and a **Microsoft 365**
tenant. **Re-verify this family on the Catalog API frequently** — it changes
faster than any other. For administrators, prioritize the **Copilot and Agent
Administration** credential and connect it to real **oversharing and labeling
governance** (Volume XXXVII). Renew annually through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for AI-901, AI-102, AI-103, AI-200, AI-500, and Copilot and Agent Administration Fundamentals.
- Cross-reference: [Volume XXXVII Ch 11](../../volume-037-microsoft-365-modern-work/chapters/11-microsoft-defender-xdr-secure-score-copilot-governance-and-capstone.md); [Chapter 06 — Data and Analytics](06-data-and-analytics-certifications.md).

**Knowledge checks**

1. Which exam replaced AI-900 for Azure AI Fundamentals?
2. What distinguishes the Copilot and Agent Administration credential from the AI developer credentials?
3. Why must you re-verify the AI family more often than the others?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of the AI family (AI-901 Fundamentals, AI-102, AI-103, AI-500). Domain weights
are from the current Azure AI Fundamentals/Engineer study guides.

**Shared prerequisites** — an **Azure subscription** with the **Azure CLI**
(`az`, `az extension add -n ml`), an **Azure AI Foundry / OpenAI** resource for
the generative labs, and Python with the `azure-ai-*` SDKs. Endpoints/keys are
shown as `$AOAI`, `$VISION`, etc.; prefer Entra/managed identity over keys.
**Cost:** small — use F0/free tiers and delete resources after.

### Lab 7.1 — AI-901: Describe Artificial Intelligence workloads and considerations (15–20%)

**Objective:** Enumerate the Azure AI service kinds (workload families).

```bash
az cognitiveservices account list-kinds -o tsv | tr '\t' '\n' | head
```

**Expected result:** service kinds (`OpenAI`, `ComputerVision`, `TextAnalytics`,
…) — the AI workloads Azure offers.

**Negative test:** deploy AI with no responsible-AI review; fairness,
reliability, and privacy are exam considerations.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — AI-901: Describe fundamental principles of machine learning on Azure (15–20%)

**Objective:** Classify ML task types.

```text
Supervised: regression (numeric), classification (label)
Unsupervised: clustering
Azure ML: Automated ML tunes models; Designer for no-code pipelines
```

**Expected result:** the ML task taxonomy and Azure ML tooling — ML
fundamentals.

**Negative test:** score a regression model with accuracy; use RMSE/R².

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — AI-901: Describe features of computer vision workloads on Azure (15–20%)

**Objective:** Create an AI Vision resource.

```bash
az cognitiveservices account create -n lab-vision -g rg-lab --kind ComputerVision --sku F0 -l eastus --yes
```

**Expected result:** an AI Vision resource (F0 free) — image analysis, OCR, and
face workloads.

**Negative test:** expect custom object detection from the prebuilt Read API;
custom models use Custom Vision / AI Foundry.

**Rollback:** `az cognitiveservices account delete -n lab-vision -g rg-lab`.

### Lab 7.4 — AI-901: Describe features of Natural Language Processing (NLP) workloads on Azure (15–20%)

**Objective:** Create a Language (Text Analytics) resource.

```bash
az cognitiveservices account create -n lab-lang -g rg-lab --kind TextAnalytics --sku F0 -l eastus --yes
```

**Expected result:** a Language resource — sentiment, key phrases, entity
recognition, and question answering.

**Negative test:** expect translation here; use the Translator resource.

**Rollback:** `az cognitiveservices account delete -n lab-lang -g rg-lab`.

### Lab 7.5 — AI-901: Describe features of generative AI workloads on Azure (20–25%)

**Objective:** List Azure OpenAI model deployments.

```bash
az cognitiveservices account deployment list -n <openai-acct> -g rg-lab -o table
```

**Expected result:** deployed generative models (`gpt-4o`, embeddings) — the
generative-AI workload.

**Negative test:** send unbounded prompts expecting unlimited context; models
have token limits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.6 — AI-102: Plan and manage an Azure AI solution (20–25%)

**Objective:** Provision a multi-service AI resource and read a key.

```bash
az cognitiveservices account create -n lab-aisvc -g rg-lab --kind AIServices --sku S0 -l eastus --yes
az cognitiveservices account keys list -n lab-aisvc -g rg-lab --query key1 -o tsv
```

**Expected result:** an AI Services resource and a key — the managed AI solution
AI-102 plans.

**Negative test:** embed the key in client code; use Entra/managed identity and
Key Vault.

**Rollback:** `az cognitiveservices account delete -n lab-aisvc -g rg-lab`.

### Lab 7.7 — AI-102: Implement generative AI solutions (15–20%)

**Objective:** Call a chat completion (Azure OpenAI).

```bash
curl "$AOAI/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-21" \
  -H "api-key: $KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Say hi"}]}'
```

**Expected result:** a JSON completion with the assistant message — a
generative-AI call.

**Negative test:** send PII with no content filtering/logging controls;
configure data-privacy settings.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.8 — AI-102: Implement an agentic solution (5–10%)

**Objective:** Define a tool-using agent (Azure AI Agent Service).

```python
agent = project.agents.create_agent(model="gpt-4o", name="lab",
        instructions="Use tools to answer.", tools=[code_interpreter])
```

**Expected result:** an agent with a tool attached — the agentic pattern (LLM +
tools + instructions).

**Negative test:** grant broad tool access with no guardrails; scope tools and
add approvals.

**Rollback:** delete the agent.

### Lab 7.9 — AI-102: Implement computer vision solutions (10–15%)

**Objective:** Run image analysis (caption + read).

```bash
curl "$VISION/computervision/imageanalysis:analyze?api-version=2024-02-01&features=caption,read" \
  -H "Ocp-Apim-Subscription-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://aka.ms/azai/vision/example"}'
```

**Expected result:** a caption and OCR text JSON — implementing vision.

**Negative test:** trust OCR of a rotated low-DPI scan blindly; preprocess and
validate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.10 — AI-102: Implement natural language processing solutions (15–20%)

**Objective:** Run sentiment analysis (Language service).

```bash
curl "$LANG/language/:analyze-text?api-version=2023-04-01" \
  -H "Ocp-Apim-Subscription-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"kind":"SentimentAnalysis","analysisInput":{"documents":[{"id":"1","text":"Great service"}]}}'
```

**Expected result:** a positive sentiment score JSON — NLP implementation.

**Negative test:** use sentiment for intent; use conversational language
understanding (CLU) for intent.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.11 — AI-102: Implement knowledge mining and information extraction solutions (15–20%)

**Objective:** Create an Azure AI Search service (knowledge mining backbone).

```bash
az search service create -n lab-search -g rg-lab --sku basic -l eastus
```

**Expected result:** an AI Search service — skillsets, indexers, and vector
search for RAG/knowledge mining.

**Negative test:** build RAG with no chunking; indexing whole documents degrades
retrieval.

**Rollback:** `az search service delete -n lab-search -g rg-lab -y`.

### Lab 7.12 — AI-103: Plan and manage an Azure AI solution (25–30%)

**Objective:** Create an AI Foundry project under a hub.

```bash
az ml workspace create --kind project --hub-id <hub> -n lab-proj -g rg-lab
```

**Expected result:** an AI Foundry project — the managed, Python-centric
environment AI-103 plans.

**Negative test:** share one project across unrelated teams; isolate with
projects and RBAC.

**Rollback:** delete the project.

### Lab 7.13 — AI-103: Implement generative AI and agentic solutions (30–35%)

**Objective:** Ground an agent with retrieval (RAG) — the largest AI-103 domain.

```python
from azure.ai.projects import AIProjectClient
client = AIProjectClient.from_connection_string(conn, cred)
agent = client.agents.create_agent(model="gpt-4o", tools=[file_search])  # RAG
```

**Expected result:** an agent grounded with file search (RAG) — generative +
agentic development.

**Negative test:** fine-tune for changing facts; ground with retrieval instead.

**Rollback:** delete the agent.

### Lab 7.14 — AI-103: Implement computer vision solutions (10–15%)

**Objective:** Caption an image via the Foundry vision client.

```python
result = vision_client.analyze(image_url=url, visual_features=[VisualFeatures.CAPTION])
print(result.caption.text)
```

**Expected result:** a generated caption string — vision in an app.

**Negative test:** display captions with no moderation; apply content safety.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.15 — AI-103: Implement text analysis solutions (10–15%)

**Objective:** Extract key phrases.

```python
docs = ["Contoso ships the order next week"]
print(text_client.extract_key_phrases(docs)[0].key_phrases)
```

**Expected result:** key phrases (e.g., `['Contoso','order','next week']`) —
text analysis.

**Negative test:** run one language model over mixed-language text; detect
language first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.16 — AI-103: Implement information extraction solutions (10–15%)

**Objective:** Extract invoice fields with Document Intelligence.

```bash
curl "$DOC/documentintelligence/documentModels/prebuilt-invoice:analyze?api-version=2024-11-30" \
  -H "Ocp-Apim-Subscription-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"urlSource":"https://aka.ms/az-invoice"}'
```

**Expected result:** an `operation-location` for the async invoice analysis —
structured field extraction.

**Negative test:** regex-parse a PDF invoice; use Document Intelligence
prebuilt/custom models.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.17 — AI-500: Architect multi-agent solutions (15–20%)

**Objective:** Design an orchestrator/worker topology.

```text
Orchestrator agent -> specialist agents (retriever, coder, reviewer)
Shared memory + message passing; explicit handoff/routing between agents
```

**Expected result:** the orchestrator-plus-specialists topology — multi-agent
architecture.

**Negative test:** build one giant agent for every task; decompose into
specialists.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.18 — AI-500: Develop multi-agent solutions in Azure (30–35%)

**Objective:** Coordinate two agents with a group chat (top domain).

```python
# Semantic Kernel AgentGroupChat / AutoGen
chat = AgentGroupChat(agents=[planner, coder], termination_strategy=max_turns(6))
await chat.invoke("Build and review a function")
```

**Expected result:** a group chat coordinating a planner and coder — multi-agent
development on Azure.

**Negative test:** let agents loop with no termination strategy; set
turn/termination limits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.19 — AI-500: Evaluate, optimize, and monitor multi-agent solutions (20–25%)

**Objective:** Score agent output with the Azure AI Evaluation SDK.

```python
from azure.ai.evaluation import evaluate, GroundednessEvaluator
evaluate(data="runs.jsonl", evaluators={"groundedness": GroundednessEvaluator(model)})
```

**Expected result:** groundedness/relevance scores per run — evaluating and
monitoring agents.

**Negative test:** ship agents with no eval harness; regressions go unnoticed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.20 — AI-500: Secure, govern, and deploy multi-agent solutions (20–25%)

**Objective:** Front the agents with Content Safety (governance).

```bash
az cognitiveservices account create -n lab-safety -g rg-lab --kind ContentSafety --sku S0 -l eastus --yes
```

**Expected result:** a Content Safety resource — securing/governing multi-agent
deployments (identity, safety, quotas).

**Negative test:** expose agent tools publicly with no auth; require Entra and
network controls.

**Rollback:** `az cognitiveservices account delete -n lab-safety -g rg-lab`.

### Lab 7.21 — AI-300: Design and implement an MLOps infrastructure (15–20%)

**Objective:** Register an Azure ML workspace + compute as the MLOps foundation.

```bash
az ml workspace show -n <ws> -g rg-lab --query name
az ml compute create -f cluster.yml -w <ws> -g rg-lab   # scalable training compute
```

**Expected result:** the workspace and a compute cluster — the MLOps
infrastructure AI-300 designs.

**Negative test:** train on a single fixed VM; MLOps needs elastic, reproducible
compute.

**Rollback:** delete the compute.

### Lab 7.22 — AI-300: Implement machine learning model lifecycle and operations (25–30%)

**Objective:** Register and version a model; deploy to a managed endpoint (top
domain).

```bash
az ml model create -n churn -v 1 -p ./model -w <ws> -g rg-lab
az ml online-deployment create -f deploy.yml -w <ws> -g rg-lab
```

**Expected result:** a versioned model and an online deployment — the ML
lifecycle (register → deploy → monitor).

**Negative test:** overwrite a production model in place; version models for
rollback and lineage.

**Rollback:** delete the deployment.

### Lab 7.23 — AI-300: Design and implement a GenAIOps infrastructure (20–25%)

**Objective:** Stand up prompt-flow + a model deployment for GenAIOps.

```text
AI Foundry project -> prompt flow (RAG) -> connections (Azure OpenAI, AI Search)
CI/CD: flow evaluated in a pipeline before promotion; environments dev/test/prod
```

**Expected result:** a prompt-flow app with grounded connections and a promotion
pipeline — GenAIOps infrastructure.

**Negative test:** ship a flow with no evaluation gate; GenAIOps requires
automated quality checks before promotion.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.24 — AI-300: Implement generative AI quality assurance and observability (10–15%)

**Objective:** Evaluate and trace a generative app.

```python
from azure.ai.evaluation import evaluate, GroundednessEvaluator, RelevanceEvaluator
evaluate(data="eval.jsonl", evaluators={"grounded":GroundednessEvaluator(m),"rel":RelevanceEvaluator(m)})
```

**Expected result:** groundedness/relevance scores plus traces — QA and
observability for generative AI.

**Negative test:** rely on manual spot-checks; automated evaluators catch
regressions across releases.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.25 — AI-300: Optimize generative AI systems and model performance (10–15%)

**Objective:** Tune cost/latency levers.

```text
Levers: model choice (mini vs full), max tokens, caching, batching, PTUs vs PAYG
Measure: latency p95, tokens/request, $/1k requests before/after each change
```

**Expected result:** a measured before/after on latency and cost — optimizing a
generative system.

**Negative test:** raise `max_tokens` "to be safe"; unbounded tokens inflate cost
and latency.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.26 — AB-900: Identify the core features and objects of Microsoft 365 services (30–35%)

**Objective:** Enumerate the M365 objects Copilot reasons over.

```powershell
Connect-MgGraph -Scopes "User.Read.All","Group.Read.All" -NoWelcome
Get-MgUser -Top 3 | Select-Object DisplayName; Get-MgGroup -Top 3 | Select-Object DisplayName
```

**Expected result:** users and groups (plus mailboxes/sites/Teams) — the M365
objects a Copilot admin governs.

**Negative test:** assume Copilot ignores permissions; it honors the user's
existing access to these objects.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.27 — AB-900: Understand data protection and governance tasks for Microsoft 365 and Copilot (35–40%)

**Objective:** Inspect the sensitivity labels/DLP that bound Copilot (top domain).

```powershell
Connect-IPPSSession
Get-Label | Select-Object DisplayName; Get-DlpCompliancePolicy | Select-Object Name
```

**Expected result:** labels and DLP policies — the Purview controls that govern
what Copilot can surface and generate.

**Negative test:** deploy Copilot with unlabeled oversharing; Copilot can surface
over-permissioned content — fix access first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.28 — AB-900: Perform basic administrative tasks for Copilot and agents (25–30%)

**Objective:** Read Copilot/agent admin settings.

```powershell
Get-MgUser -Filter "assignedLicenses/any(x:x/skuId eq <copilot-sku>)" -CountVariable c -ConsistencyLevel eventual | Out-Null; $c
```

**Expected result:** the count of Copilot-licensed users — a basic Copilot admin
task (licensing, agent management, usage).

**Negative test:** enable agents org-wide with no governance review; scope agent
availability and data access.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.29 — AB-730: Understand generative AI fundamentals (25–30%)

**Objective:** Distinguish the generative-AI concepts AB-730 tests.

```text
LLM vs traditional ML; tokens/context window; grounding (RAG) vs training
Hallucination + verification; responsible-AI limits
```

**Expected result:** the generative-AI vocabulary — the foundation for the AI
Business Professional.

**Negative test:** treat a model's fluent answer as fact; verify — models can
hallucinate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.30 — AB-730: Manage prompts and conversations by using AI (35–40%)

**Objective:** Craft and iterate a business prompt (top domain).

```text
Prompt = role + task + context + constraints + format
Iterate: refine with follow-ups; keep a reusable prompt library per task
```

**Expected result:** a structured, reusable prompt and an iteration loop —
managing prompts/conversations at work.

**Negative test:** paste confidential data into a consumer AI tool; use the
approved, governed tenant tools.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.31 — AB-730: Draft and analyze business content by using AI (25–30%)

**Objective:** Use AI to draft and analyze a business document.

```text
Draft: summary/email/report from bullet inputs -> review for tone/accuracy
Analyze: extract action items, sentiment, risks from a document; verify outputs
```

**Expected result:** an AI-drafted document and an analysis, both human-reviewed
— applied business content work.

**Negative test:** send AI output unreviewed to a customer; the human is
accountable for accuracy and tone.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.32 — AB-731: Identify the business value of generative AI solutions (35–40%)

**Objective:** Build a value case for a generative-AI initiative.

```text
Value: time saved, quality, revenue, risk reduction -> KPI + baseline + target
Prioritize use cases by value x feasibility; note change-management cost
```

**Expected result:** a KPI-anchored value case — the AI Transformation Leader's
core skill.

**Negative test:** adopt AI for novelty with no KPI; value must be measurable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.33 — AB-731: Identify benefits, capabilities, and opportunities for Microsoft's AI apps and services (35–40%)

**Objective:** Map Microsoft's AI portfolio to opportunities.

```text
Copilot (M365/security/Dynamics) | Copilot Studio (agents) | Azure AI Foundry (build)
Match each opportunity to the right product tier and licensing
```

**Expected result:** an opportunity-to-product map across the Microsoft AI stack.

**Negative test:** propose custom-built AI where Copilot already solves it; buy
before build when it fits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.34 — AB-731: Identify an implementation and adoption strategy for Microsoft's AI apps and services (20–25%)

**Objective:** Draft an AI adoption roadmap.

```text
Roadmap: pilot -> measure -> scale; governance, security, and training as gates
Adoption: champions, usage analytics, feedback loop; responsible-AI policy
```

**Expected result:** a phased adoption strategy with governance gates — leading
the transformation.

**Negative test:** roll out org-wide with no pilot or training; adoption stalls
without enablement.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.35 — AB-100: Plan AI-powered business solutions (25–30%)

**Objective:** Scope an agentic business solution from requirements.

```text
Plan: business outcome -> agent tasks/tools -> data sources (RAG) -> success metrics
Architecture-review the trust boundaries and human-in-the-loop points
```

**Expected result:** a planned agentic solution mapped to outcomes — the
architect's planning domain.

**Negative test:** plan an agent with no human oversight for high-risk actions;
insert approvals.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.36 — AB-100: Design AI-powered business solutions (25–30%)

**Objective:** Design the agent topology and integrations.

```text
Design: Copilot Studio agents + connectors + Dataverse/knowledge; orchestration
Non-functional: security (least privilege), monitoring, cost, latency
```

**Expected result:** a solution design with agents, data, and guardrails — the
design domain.

**Negative test:** grant an agent broad write connectors; scope tools to the task.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.37 — AB-100: Deploy AI-powered business solutions (40–45%)

**Objective:** Deploy and manage the solution through ALM (the largest domain).

```bash
pac solution export --path ./ai-sln.zip --managed true
pac solution import --path ./ai-sln.zip   # to the target environment
```

**Expected result:** a managed solution deployed to the target — deploying the
agentic business solution.

**Negative test:** deploy unmanaged to production; export as managed and promote
via pipelines.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.38 — AB-410: Create a foundation for intelligent applications (25–30%)

**Objective:** Provision the data/AI foundation for an intelligent app.

```bash
az cognitiveservices account create -n lab-ai -g rg-lab --kind AIServices --sku S0 -l eastus --yes
az search service create -n lab-idx -g rg-lab --sku basic -l eastus   # retrieval foundation
```

**Expected result:** AI Services + AI Search — the foundation intelligent apps
build on (models + retrieval).

**Negative test:** build RAG with no index; retrieval needs a search/vector store.

**Rollback:** delete both resources.

### Lab 7.39 — AB-410: Create intelligent applications (25–30%)

**Objective:** Wire a model call with grounding into an app.

```python
# retrieve -> augment -> generate
docs = search_client.search("policy question", top=3)
resp = openai_client.chat.completions.create(model="gpt-4o",
        messages=[{"role":"system","content":"Answer only from context."},
                  {"role":"user","content": f"{context(docs)}\nQ: ..."}])
```

**Expected result:** a grounded generation using retrieved context — building the
intelligent application.

**Negative test:** answer without grounding for company-specific questions; the
model guesses.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.40 — AB-410: Build business application logic and automation (40–45%)

**Objective:** Add business logic/automation around the AI (top domain).

```text
Automation: Power Automate flow triggers on an event -> calls the AI app -> writes Dataverse
Logic: validation, approvals, error handling, and audit of AI outputs
```

**Expected result:** an automated flow embedding the AI with validation/approval
— the largest AB-410 domain.

**Negative test:** auto-commit AI output to a system of record with no validation;
add checks and approvals.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The AI family — the fastest-changing area — runs AI-901 (Fundamentals,
replacing AI-900), AI-102 (AI Engineer), AI-103/AI-200 (AI apps/agents and
cloud developer), and the beta AI-500 (Multi-Agent Expert), plus a wave of
agent-builder and business credentials and the Copilot and Agent
Administration Fundamentals for admins. Re-verify constantly.

- [ ] I can list the current AI credentials and exam codes.
- [ ] I know AI-900 became AI-901.
- [ ] I can distinguish developer from administration credentials.
- [ ] I can build an AI/agent study path and know to re-verify often.
- [ ] I completed Labs 7.1–7.2 including each negative test.
