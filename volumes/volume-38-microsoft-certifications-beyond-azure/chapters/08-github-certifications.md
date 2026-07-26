# Chapter 08: GitHub Certifications

## Learning Objectives

- Enumerate the GitHub certifications and their GH-code exams.
- Distinguish the Foundations, Actions, Administration, Advanced Security, and Copilot credentials.
- Explain how GitHub certifications fit Microsoft's broader program.
- Recognize the new Agentic AI Developer credential.
- Build a study path for a DevOps or platform engineer using GitHub.

## Theory and Architecture

GitHub is a Microsoft company, and its certifications are part of the wider
Microsoft credential catalog, now using **GH-** exam codes and delivered
through the same Pearson VUE and Credly infrastructure. As verified on
Microsoft Learn (26 July 2026), the GitHub credentials are:

- **GitHub Foundations** — exam **GH-900** (Fundamentals). Git and GitHub
  basics — repositories, collaboration, issues, pull requests, and GitHub
  fundamentals. The gateway.
- **GitHub Actions** — the CI/CD credential for building, testing, and
  deploying with GitHub Actions workflows.
- **GitHub Administration** — exam **GH-100** (Associate-level). Administer
  GitHub organizations and enterprises — access, policies, and integrations.
- **GitHub Advanced Security** — exam **GH-500**. Code scanning, secret
  scanning, and dependency review with GitHub Advanced Security (GHAS).
- **GitHub Copilot** — exam **GH-300**. Use and administer GitHub Copilot
  effectively and responsibly.
- **GitHub Certified: Agentic AI Developer** — exam **GH-600**. A new
  credential for building agentic AI developer workflows on GitHub — part of
  the same 2026 agent wave seen across the AI family (Chapter 07).

These map directly to the automation, source-control, and DevOps skills in
**Volume IX — Infrastructure Automation** and the CI/CD and platform-
engineering content across the encyclopedia.

## Design Considerations

Start with **GH-900 (Foundations)** for anyone using GitHub seriously, then
choose by role. **DevOps/platform engineers** target **GitHub Actions** for
CI/CD; **GitHub administrators** take **GH-100**; **security engineers**
enabling GHAS take **GH-500**; and teams adopting **Copilot** take **GH-300**
(useful for both developers and the admins governing Copilot rollout — a
natural companion to the Microsoft 365 Copilot administration credential in
Chapter 07). The new **GH-600 Agentic AI Developer** suits engineers building
agent-driven developer workflows.

GitHub credentials complement the Azure **DevOps Engineer Expert (AZ-400)**
and the automation content of Volume IX — a modern platform engineer often
holds GitHub Actions plus AZ-400.

## Implementation and Automation

Verify the GitHub exam codes from Microsoft Learn:

```bash
for slug in github-foundations github-administration github-advanced-security github-copilot agentic-ai-developer; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bGH-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# github-foundations -> GH-900
# github-administration -> GH-100
# github-advanced-security -> GH-500
# github-copilot -> GH-300
# agentic-ai-developer -> GH-600
```

## Validation and Troubleshooting

Map the credentials:

| Credential | Exam | Focus |
| --- | --- | --- |
| GitHub Foundations | GH-900 | Git/GitHub basics |
| GitHub Actions | (GH-series) | CI/CD workflows |
| GitHub Administration | GH-100 | Org/enterprise administration |
| GitHub Advanced Security | GH-500 | Code/secret scanning (GHAS) |
| GitHub Copilot | GH-300 | Copilot use and administration |
| Agentic AI Developer | GH-600 | Agentic developer workflows |

Common pitfalls: assuming GitHub certifications are separate from the
Microsoft catalog (they are integrated, with **GH-** codes on Microsoft
Learn); confusing **GitHub Copilot (GH-300)** with the Microsoft 365 Copilot
and Agent Administration credential (Chapter 07) — the first is developer/tool
focused, the second is M365 governance; and overlooking the new **GH-600**
agentic credential.

## Security and Best Practices

Prepare with **Microsoft Learn** and **GitHub Skills** free interactive
courses, and practice in a **free GitHub account** and organization. Pair
**GitHub Actions** with the Azure **AZ-400** DevOps credential and the
automation practice in **Volume IX**. For security teams, **GH-500 (Advanced
Security)** pairs with the SC family (Chapter 03). Renew per the credential's
stated validity on Microsoft Learn.

## References and Knowledge Checks

- Microsoft Learn: certification pages for GitHub Foundations (GH-900), Administration (GH-100), Advanced Security (GH-500), Copilot (GH-300), Agentic AI Developer (GH-600).
- Cross-reference: [Volume IX — Infrastructure Automation](../volume-09-infrastructure-automation/README.md).

**Knowledge checks**

1. What exam code prefix do GitHub certifications use, and where are they catalogued?
2. How does GitHub Copilot (GH-300) differ from the M365 Copilot administration credential?
3. Which GitHub credential pairs naturally with the Azure AZ-400 DevOps Expert?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of the GitHub family (GH-900, GH-100, GH-300, GH-500, GH-600).

**Shared prerequisites** — `git`, the **GitHub CLI** (`gh auth login`), and a
GitHub account (an org with GitHub Advanced Security for the GH-500 labs; Copilot
access for GH-300). Most commands run against a repo you own. **Cost:** none
(free tier; some GHAS/Copilot features require a paid plan).

### Lab 8.1 — GH-900: Understand Git and GitHub basics (25–30%)

**Objective:** Initialize a repo and make the first commit.

```bash
d=$(mktemp -d); cd "$d"; git init -q; echo "# lab" > README.md
git add README.md; git -c user.email=a@b.c -c user.name=lab commit -qm init; git log --oneline
```

**Expected result:** one commit in the log — the Git basics GH-900 opens with.

**Negative test:** commit with nothing staged; there is nothing to commit.

**Cleanup:** `rm -rf "$d"`.

### Lab 8.2 — GH-900: Work with GitHub repositories (10–15%)

**Objective:** Create and inspect a remote repository.

```bash
gh repo create lab-demo --private --clone; cd lab-demo; gh repo view --json name,visibility
```

**Expected result:** a private repo created and cloned — repository management.

**Negative test:** push to a repo you have no write access to; permissions block
it.

**Cleanup:** `gh repo delete lab-demo --yes`.

### Lab 8.3 — GH-900: Collaborate using GitHub (10–15%)

**Objective:** Open a pull request from a branch.

```bash
git checkout -b feature; echo x >> README.md; git commit -aqm "edit"
git push -u origin feature; gh pr create --fill
```

**Expected result:** a PR opened from `feature` — the collaboration flow
(branch → PR → review).

**Negative test:** commit straight to `main` on a protected branch; branch
protection requires a PR.

**Cleanup:** `gh pr close feature`.

### Lab 8.4 — GH-900: Apply modern development practices (10–15%)

**Objective:** Add a minimal CI workflow (GitHub Actions).

```yaml
# .github/workflows/ci.yml
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [{ uses: actions/checkout@v4 }, { run: echo "build ok" }]
```

**Expected result:** a workflow that runs on push — CI/CD, a modern dev
practice.

**Negative test:** store secrets in the YAML; use encrypted Actions secrets.

**Cleanup:** remove the workflow file.

### Lab 8.5 — GH-900: Manage projects with GitHub (5–10%)

**Objective:** Create an issue and add it to a project.

```bash
gh issue create --title "Lab task" --body "demo"
gh project list --owner @me
```

**Expected result:** an issue and your Projects list — planning with GitHub
Projects.

**Negative test:** track work only in commit messages; issues/projects give
visibility and triage.

**Cleanup:** close the issue.

### Lab 8.6 — GH-900: Explore the GitHub community (5–10%)

**Objective:** Read a repo's community health files.

```bash
gh api repos/{owner}/{repo}/community/profile --jq '.files | keys'
```

**Expected result:** health files (README, LICENSE, CODE_OF_CONDUCT,
CONTRIBUTING) — the open-source community practices GH-900 covers.

**Negative test:** publish a public repo with no LICENSE; without one, others
have no legal right to reuse it.

**Cleanup:** none.

### Lab 8.7 — GH-100: Manage GitHub identities and access (15–20%)

**Objective:** Manage org members and teams.

```bash
gh api orgs/{org}/members --jq 'length'
gh api orgs/{org}/teams --jq '.[].slug'
```

**Expected result:** the member count and team slugs — identity and access
administration.

**Negative test:** grant repo access to individuals instead of teams; teams
scale permission management.

**Cleanup:** none.

### Lab 8.8 — GH-100: Administer GitHub Enterprise environment (10–15%)

**Objective:** Read enterprise/org policy settings.

```bash
gh api orgs/{org} --jq '{2fa:.two_factor_requirement_enabled, default_perm:.default_repository_permission}'
```

**Expected result:** the org's 2FA requirement and default repo permission —
enterprise governance.

**Negative test:** leave the default repo permission at `write` for all members;
tighten to `read` and grant up.

**Cleanup:** none.

### Lab 8.9 — GH-100: Implement secure software development and compliance (25–30%)

**Objective:** Enforce branch protection / rulesets (the top domain).

```bash
gh api -X PUT repos/{owner}/{repo}/branches/main/protection \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -F enforce_admins=true -F required_status_checks=null -F restrictions=null
```

**Expected result:** required reviews and admin enforcement on `main` — secure
SDLC controls.

**Negative test:** allow force-pushes to `main`; protect history on default
branches.

**Cleanup:** delete the protection rule.

### Lab 8.10 — GH-100: Manage GitHub Actions (20–25%)

**Objective:** Set org Actions policy (allowed actions).

```bash
gh api -X PUT orgs/{org}/actions/permissions -f enabled_repositories=all -f allowed_actions=selected
```

**Expected result:** an org Actions policy limiting to selected actions —
governing CI/CD.

**Negative test:** allow all actions from any author; restrict to verified/local
actions for supply-chain safety.

**Cleanup:** revert the policy.

### Lab 8.11 — GH-100: Monitor and optimize GitHub usage (10–15%)

**Objective:** Read Actions billing/usage.

```bash
gh api /orgs/{org}/settings/billing/actions --jq '{minutes_used:.total_minutes_used, included:.included_minutes}'
```

**Expected result:** Actions minutes used vs included — monitoring and optimizing
usage/cost.

**Negative test:** run every job on the largest runner; right-size runners and
cache to cut minutes.

**Cleanup:** none.

### Lab 8.12 — GH-300: Use GitHub Copilot responsibly (15–20%)

**Objective:** Recognize responsible-use practices.

```text
Always review suggestions; never accept secrets/keys or license-incompatible code
Copilot may reproduce patterns — verify correctness, security, and licensing
```

**Expected result:** the responsible-use checklist — the domain GH-300 opens
with.

**Negative test:** merge Copilot output unreviewed; the developer is accountable
for the code.

**Cleanup:** none.

### Lab 8.13 — GH-300: Use GitHub Copilot features (25–30%)

**Objective:** Use Copilot in the CLI (the largest domain).

```bash
gh extension install github/gh-copilot
gh copilot suggest "list the 5 largest files in this repo"
```

**Expected result:** a suggested shell command — Copilot's chat/CLI features
(completions, chat, CLI).

**Negative test:** treat Copilot Chat and code completion as the same feature;
they have distinct contexts and controls.

**Cleanup:** `gh extension remove gh-copilot`.

### Lab 8.14 — GH-300: Understand GitHub Copilot data and architecture (10–15%)

**Objective:** Map the Copilot request flow.

```text
IDE/editor context -> proxy -> LLM; prompt = current file + open tabs + context
Business/Enterprise: prompts not retained for training; content exclusions honored
```

**Expected result:** the context-to-model flow and data-handling model — Copilot
architecture.

**Negative test:** assume Copilot indexes your whole repo by default; it uses
in-editor context (plus indexing when enabled).

**Cleanup:** none.

### Lab 8.15 — GH-300: Apply prompt engineering and context crafting (10–15%)

**Objective:** Improve a suggestion with better context.

```text
Weak:  "make a function"
Strong: leading comment + signature + example:
  // returns weekday name for a 0-6 index; throw on out-of-range
  function weekday(i) {
```

**Expected result:** a specified prompt (intent, signature, constraints, example)
— prompt/context crafting.

**Negative test:** prompt with a vague one-liner; specific context yields better
completions.

**Cleanup:** none.

### Lab 8.16 — GH-300: Improve developer productivity with GitHub Copilot (10–15%)

**Objective:** Use Copilot for tests/docs from existing code.

```text
Copilot Chat: /tests generate unit tests for the selected function
              /doc  add a docstring; /explain summarize a diff
```

**Expected result:** generated tests/docs from a selection — productivity
workflows.

**Negative test:** accept generated tests without running them; verify they pass
and are meaningful.

**Cleanup:** none.

### Lab 8.17 — GH-300: Configure privacy, content exclusions, and safeguards (10–15%)

**Objective:** Configure content exclusions for a repo/org.

```text
Org/repo settings -> Copilot -> Content exclusions (paths/repos Copilot ignores)
Duplication detection filter blocks public-code matches
```

**Expected result:** content-exclusion paths and the duplication filter — Copilot
safeguards.

**Negative test:** rely on exclusions to protect secrets; never commit secrets in
the first place.

**Cleanup:** none.

### Lab 8.18 — GH-500: Describe GitHub Security suites, features, and ecosystem (15–20%)

**Objective:** Read a repo's security feature status.

```bash
gh api repos/{owner}/{repo} --jq '.security_and_analysis'
```

**Expected result:** the enablement status of secret scanning, Dependabot, and
code scanning — the GHAS suite overview.

**Negative test:** assume GHAS is on by default for private repos; it must be
enabled (and licensed).

**Cleanup:** none.

### Lab 8.19 — GH-500: Configure and use Secret Protection (formerly secret scanning) (15–20%)

**Objective:** Enable secret scanning + push protection.

```bash
gh api -X PATCH repos/{owner}/{repo} \
  -F security_and_analysis.secret_scanning.status=enabled \
  -F security_and_analysis.secret_scanning_push_protection.status=enabled
```

**Expected result:** secret scanning and push protection enabled — blocking
leaked credentials.

**Negative test:** rely on scanning after the fact; push protection stops the
secret before it lands.

**Cleanup:** disable as needed.

### Lab 8.20 — GH-500: Configure and use supply chain security (formerly Dependabot/Dependency Review) (15–20%)

**Objective:** Enable Dependabot alerts/updates.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule: { interval: "weekly" }
```

**Expected result:** Dependabot configured for weekly npm updates — supply-chain
security (SBOM, alerts, updates).

**Negative test:** ignore Dependabot PRs; unpatched dependencies are a top supply-
chain risk.

**Cleanup:** remove the file.

### Lab 8.21 — GH-500: Configure and use Code Security (formerly Code Scanning with CodeQL) (10–15%)

**Objective:** Add the CodeQL scanning workflow.

```yaml
# .github/workflows/codeql.yml
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with: { languages: javascript }
      - uses: github/codeql-action/analyze@v3
```

**Expected result:** a CodeQL analysis workflow — static analysis for
vulnerabilities.

**Negative test:** treat every CodeQL alert as critical; triage by severity and
exploitability.

**Cleanup:** remove the workflow.

### Lab 8.22 — GH-500: Security operations: best practices, prioritization, and remediation (15–20%)

**Objective:** List and triage open code-scanning alerts.

```bash
gh api repos/{owner}/{repo}/code-scanning/alerts --jq '.[] | {rule:.rule.id, sev:.rule.severity, state:.state}'
```

**Expected result:** alerts with rule and severity — the SecOps triage/remediation
workflow.

**Negative test:** dismiss alerts as "won't fix" without justification; record a
dismissal reason for audit.

**Cleanup:** none.

### Lab 8.23 — GH-500: GitHub Security suites administration (10–15%)

**Objective:** Enable GHAS features org-wide by default.

```bash
gh api -X PATCH orgs/{org} \
  -F secret_scanning_enabled_for_new_repositories=true \
  -F dependabot_alerts_enabled_for_new_repositories=true
```

**Expected result:** GHAS defaults applied to new repos — suite administration.

**Negative test:** enable per repo forever; set org defaults so new repos inherit
protection.

**Cleanup:** none.

### Lab 8.24 — GH-600: Prepare agent architecture and SDLC processes (15–20%)

**Objective:** Map an agent into the SDLC.

```text
Agent lifecycle: plan -> act (tools) -> observe -> reflect
SDLC integration: PR-based review of agent changes; CI gates; human approval
```

**Expected result:** the agent loop wired into a PR/CI-gated SDLC — agentic
development architecture.

**Negative test:** let an agent merge to `main` unattended; require review and
CI gates.

**Cleanup:** none.

### Lab 8.25 — GH-600: Implement tool use and environment interaction (20–25%)

**Objective:** Give an agent scoped tools (the largest domain).

```text
Tools: read_file, run_tests, gh api (scoped token)
Least privilege: a fine-grained PAT limited to the target repo and required scopes
```

**Expected result:** a tool set with a least-privilege token — safe environment
interaction.

**Negative test:** hand the agent a classic PAT with full scopes; use
fine-grained, minimal permissions.

**Cleanup:** none.

### Lab 8.26 — GH-600: Manage memory, state, and execution (10–15%)

**Objective:** Design short- vs long-term agent memory.

```text
Short-term: conversation/turn state; Long-term: vector store of prior results
Execution: idempotent steps + checkpoints so a rerun does not duplicate side effects
```

**Expected result:** the memory/state/execution model — reliable agent runs.

**Negative test:** stuff all history into the prompt; summarize/retrieve to stay
within context limits.

**Cleanup:** none.

### Lab 8.27 — GH-600: Perform evaluation, error analysis, and tuning (15–20%)

**Objective:** Evaluate agent runs against a fixed test set.

```text
Golden tasks -> run agent -> score (pass/fail, cost, latency) -> error taxonomy
Tune: prompts, tool descriptions, retries; track deltas per change
```

**Expected result:** an eval loop with an error taxonomy — measuring and tuning
agent quality.

**Negative test:** tune on vibes with no fixed test set; regressions hide without
measurement.

**Cleanup:** none.

### Lab 8.28 — GH-600: Orchestrate multi-agent coordination (15–20%)

**Objective:** Coordinate specialist agents.

```text
Orchestrator -> planner, coder, reviewer; explicit handoffs + shared task state
Terminate on success criteria or a max-step budget
```

**Expected result:** a coordinated multi-agent workflow — orchestration.

**Negative test:** run agents in parallel on shared state with no locking; serialize
or partition to avoid conflicts.

**Cleanup:** none.

### Lab 8.29 — GH-600: Implement guardrails and accountability (10–15%)

**Objective:** Add guardrails and an audit trail.

```text
Guardrails: allow-list of commands/paths; human approval for writes/merges
Accountability: log every tool call + decision; sign commits/attest provenance
```

**Expected result:** approval gates plus an auditable log — guardrails and
accountability for agents.

**Negative test:** allow autonomous writes with no approval or logging; agents
need bounded, auditable authority.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub certifications are part of the Microsoft catalog with **GH-** codes:
Foundations (GH-900), Actions, Administration (GH-100), Advanced Security
(GH-500), Copilot (GH-300), and the new Agentic AI Developer (GH-600). They
complement Azure DevOps (AZ-400) and the automation practice in Volume IX.

- [ ] I can list the GitHub credentials and GH-codes.
- [ ] I can distinguish GH-300 from M365 Copilot administration.
- [ ] I can pair GitHub credentials with Azure DevOps and Volume IX.
- [ ] I recognize the new GH-600 agentic credential.
- [ ] I completed Labs 8.1–8.2 including each negative test.
