# Chapter 07: GitLab Duo and the Agent Platform

## Learning Objectives

- Describe GitLab Duo's AI capabilities across the DevSecOps lifecycle.
- Explain agentic chat and how to select an appropriate agent for a task.
- Configure and publish custom agents and flows, and connect external tools via MCP.
- Apply least privilege and human review to AI-assisted workflows.

## The newest certification

The **Certified GitLab Duo Agent Platform Associate** is the newest exam in the program, and its published scope is specific: use **agentic chat** and **select the appropriate agent** for a development task, **configure and publish custom agents and flows**, **connect external tools via MCP**, and apply **AI-assisted code creation, review, and security workflows**.

That is a meaningfully different syllabus from "the AI writes code for you." It is about **operating an agent platform** — choosing the right agent, granting it the right tools, and keeping a human accountable for the result.

## From assistant to agent

| Mode | What it does | Human role |
|:---|:---|:---|
| **Suggestion** | Completes code as you type | Accept or reject each suggestion |
| **Chat** | Answers questions about code, explains, drafts | Ask, evaluate, apply |
| **Agentic chat / flows** | Takes multi-step actions using tools, across files and systems | Define scope, approve consequential steps, review the outcome |

The step from chat to agent is where the operational questions arrive. A chat response is inert text you choose to use; an agent **acts** — editing files, opening merge requests, calling external systems. Everything that follows exists because acting has consequences that answering does not.

## MCP: connecting external tools

The **Model Context Protocol (MCP)** is an open standard for connecting AI systems to external tools and data sources. In the Agent Platform it is how an agent reaches beyond GitLab — to an issue tracker, a documentation source, a monitoring system.

Each connected tool expands what the agent can do and, identically, what it can do *wrong*. The governing principle is **least privilege**, exactly as with any other identity: grant the narrowest tool set that lets the agent complete its task. An agent that only needs to read issues should not hold write access to repositories, and the fact that granting more is easier is not a reason to do it.

## The honest limits

The certification is worth holding and the tooling is genuinely useful, and both of those are compatible with being clear-eyed:

- **AI-generated code needs the same review as human code** — arguably more, because it is produced faster and reads plausibly regardless of correctness.
- **AI-generated code needs the same scanning** (Chapter 06). It is not exempt from SAST, dependency, or secret checks, and it can reproduce insecure patterns from its training.
- **Accountability does not transfer.** The engineer who merges is responsible for the change, whatever produced it.
- **Untrusted content is untrusted, even when an agent reads it.** An agent that ingests an issue comment, a web page, or a dependency's README is processing text that someone else wrote — and that text may contain instructions aimed at the agent. Tool permissions and human approval on consequential actions are what contain that risk.

And a piece of program trivia with a sharp edge: GitLab's exam Code of Conduct **prohibits using artificial intelligence or automated tools during exams**. You may be certified in operating AI agents; you may not use one to sit the exam.

## Hands-On Lab

Python models agent governance. **Cost:** none.

### Lab 7.1 — Select the appropriate agent for the task

**Objective:** Match task to agent, and recognize where none is appropriate.

```bash
python3 - <<'EOF'
AGENTS = {
  "code-assistant":   {"good_at":["write code","refactor","explain code"], "tools":["read_repo","write_files"]},
  "review-agent":     {"good_at":["review MR","find bugs","suggest tests"], "tools":["read_repo","comment_mr"]},
  "security-agent":   {"good_at":["triage findings","explain CVE","suggest fix"], "tools":["read_repo","read_scans"]},
  "docs-agent":       {"good_at":["write docs","summarize"], "tools":["read_repo","write_files"]},
}
def select(task):
    for name, a in AGENTS.items():
        if task in a["good_at"]:
            return name, a["tools"]
    return None, []

for task in ["review MR","triage findings","write docs","approve production deploy","decide if a risk is acceptable"]:
    name, tools = select(task)
    if name:
        print(f"{task:32} -> {name:16} tools={tools}")
    else:
        print(f"{task:32} -> NO AGENT — this is a HUMAN JUDGMENT/ACCOUNTABILITY decision")
print("\nSelecting the agent is half the skill; knowing which tasks are NOT delegable is the other half.")
print("Approving a production deploy and accepting a risk are accountability decisions — a person owns them.")
EOF
```

**Expected result:** Four tasks route to specialized agents; production approval and risk acceptance route to **no agent at all**. That second category is the part the certification's framing implies and that operators must internalize: the limit on delegation is not capability but **accountability** — someone must own the decision, and ownership cannot be assigned to a tool.

**Negative test:** Using one general-purpose agent with every tool for all tasks — it works, and you have granted write access for jobs that only needed read, expanding the blast radius of every mistake.

**Cleanup:** None.

### Lab 7.2 — Least privilege for agent tools via MCP

**Objective:** Grant the narrowest tool set that completes the task.

```bash
python3 - <<'EOF'
TOOL_RISK = {
  "read_repo":"low", "read_scans":"low", "read_issues":"low",
  "comment_mr":"medium", "write_files":"medium",
  "create_mr":"medium", "merge_mr":"HIGH", "deploy":"HIGH", "delete_branch":"HIGH",
}
def grant(agent, task_needs, requested):
    print(f"\n{agent}: needs {task_needs}")
    approved, refused = [], []
    for t in requested:
        (approved if t in task_needs else refused).append(t)
    for t in approved:
        print(f"   GRANT  {t:14} risk={TOOL_RISK[t]}")
    for t in refused:
        marker = "  <-- would allow irreversible action" if TOOL_RISK[t] == "HIGH" else ""
        print(f"   REFUSE {t:14} risk={TOOL_RISK[t]} — not required by the task{marker}")
    if any(TOOL_RISK[t] == "HIGH" for t in approved):
        print("   NOTE: a HIGH-risk tool is granted — require human approval before it fires")

grant("docs-agent",     ["read_repo","write_files"], ["read_repo","write_files","merge_mr","deploy"])
grant("review-agent",   ["read_repo","comment_mr"],  ["read_repo","comment_mr"])
grant("security-agent", ["read_repo","read_scans"],  ["read_repo","read_scans","delete_branch"])
print("\nEvery connected MCP tool widens both capability and blast radius. Grant the minimum;")
print("gate anything irreversible behind a human, exactly as you would for a service account.")
EOF
```

**Expected result:** Each agent receives only what its task requires, with `merge_mr`, `deploy`, and `delete_branch` refused as unnecessary. The framing in the last line is the useful one: an agent with tools **is** a service account with unusually flexible behavior, so apply the same least-privilege reasoning you would apply to any automation credential.

**Negative test:** Granting an agent `merge_mr` so it can "finish the job" — you have removed the human review step that catches the cases where the agent was confidently wrong.

**Cleanup:** None.

### Lab 7.3 — AI-assisted code still goes through the pipeline

**Objective:** Show that provenance does not change the required controls.

```bash
python3 - <<'EOF'
def gate(change):
    checks, blocked = [], False
    for name, passed in change["checks"].items():
        checks.append(f"   [{'PASS' if passed else 'FAIL'}] {name}")
        blocked |= not passed
    if not change["human_reviewed"]:
        checks.append("   [FAIL] human review — accountability requires a named reviewer")
        blocked = True
    return checks, blocked

changes = [
  {"author":"human",         "human_reviewed":True,  "checks":{"SAST":True,"dependency scan":True,"tests":True}},
  {"author":"GitLab Duo",    "human_reviewed":True,  "checks":{"SAST":True,"dependency scan":True,"tests":True}},
  {"author":"GitLab Duo",    "human_reviewed":False, "checks":{"SAST":True,"dependency scan":True,"tests":True}},
  {"author":"GitLab Duo",    "human_reviewed":True,  "checks":{"SAST":False,"dependency scan":True,"tests":True}},
]
for c in changes:
    lines, blocked = gate(c)
    print(f"\nauthored by {c['author']}:")
    for l in lines: print(l)
    print(f"   => {'BLOCKED' if blocked else 'MERGE ALLOWED'}")
print("\nThe pipeline does not care who wrote the code, and that is the point: identical controls")
print("regardless of provenance. 'Duo wrote it' is not a review, and it is not a scan result.")
EOF
```

**Expected result:** Human- and Duo-authored changes face **identical gates**; the unreviewed change is blocked, and so is the one failing SAST. The uniformity is deliberate — the temptation with AI-generated code is to treat it as pre-validated because it was produced by a system that sounds authoritative, when in fact speed of production is a reason for more scrutiny, not less.

**Negative test:** Exempting AI-generated merge requests from review to capture the productivity gain — you have removed the control precisely where volume increased, which is the worst possible place to remove it.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Duo's suggestion / chat / agentic modes distinguished by what the human is accountable for.
- [ ] Agent selection practiced, including tasks that are not delegable.
- [ ] MCP tool connection governed by least privilege, with irreversible actions human-gated.
- [ ] AI-assisted code held to identical review and scanning requirements.
- [ ] The exam Code of Conduct's prohibition on AI tools during exams noted.
