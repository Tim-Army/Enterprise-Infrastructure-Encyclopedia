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
- Assessment-based and beta credentials in the same space — **AI Agent Builder
  Associate**, **Agentic AI Business Solutions Architect**, **Intelligent
  Applications Builder Associate (beta)**, plus a data/AI operations exam
  (**AI-300**, operationalizing ML and generative-AI solutions).

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
- Cross-reference: [Volume XXXVII Ch 11](../volume-37-microsoft-365-modern-work/chapters/11-microsoft-defender-xdr-secure-score-copilot-governance-and-capstone.md); [Chapter 06 — Data and Analytics](06-data-and-analytics-certifications.md).

**Knowledge checks**

1. Which exam replaced AI-900 for Azure AI Fundamentals?
2. What distinguishes the Copilot and Agent Administration credential from the AI developer credentials?
3. Why must you re-verify the AI family more often than the others?

## Hands-On Lab

Exam-preparation walkthroughs for the AI family.

**Shared prerequisites for Labs 7.1–7.2** — a browser; `curl` for Lab 7.1.
**Cost:** none.

### Lab 7.1 — Confirm the AI Fundamentals renumber (Topic: Verify currency)

**Objective:** Prove AI-901 is current.

```bash
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/" \
  | grep -oE '\bAI-[0-9]{3}\b' | sort -u
```

**Expected result:** **AI-901** — the current Azure AI Fundamentals exam
(AI-900 retired).

**Negative test:** search for an "AI-900" certification page; it is retired —
study AI-901.

**Cleanup:** none.

### Lab 7.2 — Plan an AI/agent path (Topic: Study plan)

**Objective:** Sequence for a generative-AI/agent developer.

```text
AI-901 (Fundamentals)
  -> AI-102 (Azure AI Engineer) as the core
  -> AI-103 (AI Apps and Agents Developer) for GenAI/agents
  -> AI-500 (Multi-Agent Expert, beta) for senior multi-agent design.
Administrators instead: Copilot and Agent Administration Fundamentals,
tied to Vol XXXVII Ch 10–11 governance.
```

**Expected result:** a Fundamentals→Associate→Expert developer path, with a
separate administration branch.

**Negative test:** plan around AI-900; it is renumbered — anchor on AI-901.

**Cleanup:** none.

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
