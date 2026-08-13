# Chapter 07: AI and Secure Development

## Learning Objectives

- Understand the security risk of AI-generated code.
- Place the OWASP Top 10 for LLM and GenAI applications.
- Explain securing AI-agent (agentic) applications.
- Recognize why AI raises the stakes on developer-first security.

*Cert relevance: AI security is Snyk Learn's fastest-growing area — Secure AI Development, OWASP for LLM/GenAI, agentic paths, and the AI Security University Program.*

> **Defensive framing.** This chapter is about *securing* AI-assisted development and AI applications — finding and fixing vulnerabilities in AI-generated code and in LLM/agent apps. Nothing here is about attacking systems; it is the defender's side of the AI shift.

## AI-generated code is not secure by default

The biggest change in how software is written is that a large and growing share of code is now **AI-generated** — from coding assistants and agents. This is a productivity revolution and a **security problem**, because AI coding tools are trained on public code that *includes insecure patterns*, and they generate what is *plausible*, not what is *secure*. AI-generated code confidently reproduces SQL injection, hardcoded secrets, weak crypto, and the rest of the [OWASP Top 10](#the-owasp-top-10-for-ai) — often more of it, faster, because the developer trusts the assistant and reviews less.

The developer-first thesis (Chapter 2) becomes *more* important here, not less: if code is generated faster than humans can review it, then **security has to be in the loop automatically** — scanning the AI's output in the IDE as it lands, the same way it scans human-written code. Snyk's positioning is exactly this: secure the AI-assisted SDLC by keeping the find-and-fix loop on *all* code, whoever (or whatever) wrote it. The lab models the AI-code review gap.

## The OWASP Top 10 for AI

Snyk Learn teaches the emerging AI-security frameworks, chiefly the **OWASP Top 10 for LLM and GenAI applications** — the canonical risk list for apps built *with* large language models. Its classes are genuinely new attack surfaces:

| Risk | Is |
|:---|:---|
| **Prompt injection** | Untrusted input that manipulates the model's instructions |
| **Insecure output handling** | Trusting model output as safe (it reaches a sink, like any untrusted data) |
| **Sensitive information disclosure** | The model leaking training data or context/secrets |
| **Excessive agency** | Giving an AI agent more power/tools than it should have |
| **Supply chain (models & data)** | Poisoned models, datasets, or plugins |

Notice **prompt injection** and **insecure output handling** are the [source-to-sink data-flow problem (Chapter 4)](04-snyk-code-sast.md) in AI clothing: untrusted input reaching a powerful sink (the model, or the model's output reaching *your* systems) without a trust boundary. The old discipline applies; the sink is new.

## Agentic applications and excessive agency

The frontier is **agentic applications** — AI agents that do not just answer but *act*: call tools, run code, make API calls, move money. Snyk Learn's **OWASP Top 10 for Agentic Applications** path addresses the risk that dominates here: **excessive agency**. An agent given broad tool access and acted-upon by untrusted input is a [toxic combination (CXLVII)](../../volume-147-wiz-certifications/chapters/03-attack-paths-and-toxic-combinations.md) — the least-privilege and trust-boundary disciplines from the whole security shelf, applied to autonomous software. The lab models constraining agent agency.

## Hands-On Lab

Python models AI-security concepts. **Cost:** none.

### Lab 7.1 — The AI-generated-code review gap

**Objective:** See why AI codegen needs automated security in the loop.

```bash
python3 - <<'EOF'
# developers generate code with an AI assistant; some fraction is insecure;
# human review catches only so much, and AI codegen outpaces review
LINES_PER_DAY_HUMAN = 200
LINES_PER_DAY_AI    = 1200     # AI assistant multiplies output
INSECURE_RATE       = 0.06     # fraction of generated code with a vuln
HUMAN_REVIEW_CATCH  = 0.40     # humans catch ~40% of vulns in review (fatigue, volume)
AUTO_SCAN_CATCH     = 0.90     # in-IDE scanner catches ~90%, on every line

for label, lines in [("human-written", LINES_PER_DAY_HUMAN), ("AI-generated", LINES_PER_DAY_AI)]:
    introduced = lines * INSECURE_RATE
    print(f"{label}: {lines} lines/day -> ~{introduced:.0f} insecure lines/day")

ai_vulns = LINES_PER_DAY_AI * INSECURE_RATE
print(f"\nWith AI codegen: ~{ai_vulns:.0f} insecure lines/day per dev.\n")
print("REVIEW ONLY (trust the human to catch it):")
missed_review = ai_vulns * (1 - HUMAN_REVIEW_CATCH)
print(f"   humans catch ~{HUMAN_REVIEW_CATCH:.0%} -> ~{missed_review:.0f} insecure lines/day SHIP")
print(f"   (AI writes faster than humans review; fatigue + trust make it worse)\n")
print("REVIEW + AUTO-SCAN in the IDE (scan the AI's output like any code):")
missed_auto = ai_vulns * (1 - AUTO_SCAN_CATCH)
print(f"   scanner catches ~{AUTO_SCAN_CATCH:.0%} in-workflow -> ~{missed_auto:.0f} ship")
print(f"\n   insecure lines caught by adding auto-scan: ~{missed_review - missed_auto:.0f}/day/dev")
print("\nAI codegen writes 6x the lines — and reproduces insecure patterns from its")
print("training data, confidently. Human review CAN'T keep up (more code, and devs")
print("trust the assistant, so they review LESS). The fix isn't 'review harder' — it's")
print("keeping the automated find-and-fix loop on ALL code, whoever wrote it. Snyk")
print("scans AI-generated code in the IDE exactly like human code. The developer-first")
print("loop matters MORE in the AI era, because generation outran manual review.")
EOF
```

**Expected result:** AI codegen producing far more insecure lines per day than human review can catch, with automated in-IDE scanning closing most of the gap. The AI-code lesson is that generation now outpaces manual review, so security must stay in the loop automatically — scanning AI output like any code — making the developer-first find-and-fix loop more important in the AI era, not less.

**Negative test:** Relying on human code review to catch insecure AI-generated code. AI writes several times faster than humans review, and developers trust the assistant and review less — automated scanning of the AI's output is what keeps pace.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Constrain excessive agency

**Objective:** Apply least privilege to an AI agent's tools.

```bash
python3 - <<'EOF'
# an AI agent with a set of tools; untrusted input can steer it (prompt injection)
AGENT_TOOLS = [
  # tool,              needed_for_task, risk_if_abused
  ("read_knowledge_base", True,  "low — read-only reference"),
  ("send_email",          False, "HIGH — can exfiltrate / phish as you"),
  ("execute_shell",       False, "CRITICAL — arbitrary code execution"),
  ("delete_records",      False, "HIGH — destructive"),
  ("summarize_text",      True,  "low — pure function"),
]
TASK = "answer customer questions from the knowledge base"
print(f"Agent task: '{TASK}'")
print("Untrusted input (a user's question) STEERS the agent — prompt injection is")
print("always possible. So agency must be constrained to the task.\n")
print(f"   {'tool':22}{'needed?':>9}   risk if abused")
granted, denied = [], []
for tool, needed, risk in AGENT_TOOLS:
    (granted if needed else denied).append(tool)
    mark = "grant" if needed else "DENY"
    print(f"   {tool:22}{str(needed):>9}   {risk}   [{mark}]")
print(f"\n   least-privilege grant: {granted}")
print(f"   denied (not needed for the task): {denied}")
print("\nWhy this is the whole ballgame for agentic apps: an agent acted-upon by")
print("untrusted input (prompt injection) + broad tool access = EXCESSIVE AGENCY, the")
print("top agentic risk. If this Q&A agent also had execute_shell and send_email, a")
print("crafted question could make it run commands or email data out — as YOU.")
print("\nThe fix is the oldest one in security: LEAST PRIVILEGE. Give the agent ONLY")
print("the tools its task needs (read + summarize), never the powerful ones it")
print("doesn't. Same trust-boundary + least-privilege discipline as CIEM effective")
print("permissions (Wiz, CXLVII) and the whole shelf — applied to autonomous AI. The")
print("model is new; the discipline is not.")
EOF
```

**Expected result:** An AI agent granted only the read-and-summarize tools its task needs, with powerful tools (shell, email, delete) denied to constrain excessive agency. The agentic lesson is that an agent steered by untrusted input plus broad tool access is the top agentic risk, resolved by the oldest discipline — least privilege — giving the agent only the tools its task requires.

**Negative test:** Giving an AI agent broad tool access "to be helpful." An agent that can be steered by untrusted input and holds powerful tools (shell, email) is a prompt-injection away from acting maliciously as you — least privilege on agent tools is the control.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] AI-generated code understood as insecure-by-default, requiring automated security in the loop as generation outpaces review.
- [ ] The OWASP Top 10 for LLM/GenAI placed — prompt injection and insecure output handling as the data-flow problem in AI form.
- [ ] Agentic applications and excessive agency understood as least privilege applied to autonomous software.
- [ ] AI recognized as raising the stakes on developer-first security, not lowering them.
