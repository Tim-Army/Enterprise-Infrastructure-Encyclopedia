# Chapter 06: GitHub Advanced Security

## Learning Objectives

- Enable CodeQL code scanning.
- Enable secret scanning and push protection.
- Reason about Dependabot alerts, updates, and dependency review.
- Read the security overview and triage alerts.
- Complete a walkthrough for each Advanced Security topic.

## Theory and Architecture

**GitHub Advanced Security (GHAS)** is the platform's suite for finding and fixing vulnerabilities in
**your own** code and supply chain — entirely **defensive**. Its pillars:

- **Code scanning with CodeQL** — static analysis that queries your code as a database to find
  vulnerabilities (injection, path traversal, and more), run as an Actions workflow and surfaced as
  alerts on PRs and in the Security tab.
- **Secret scanning** — detects committed credentials (tokens, keys) against hundreds of partner
  patterns, with **push protection** that **blocks** a push containing a detected secret before it lands.
- **Dependabot** — **alerts** on vulnerable dependencies (via the GitHub Advisory Database), automated
  **security/version updates** that open PRs to bump them, and **dependency review** that flags risky
  dependency changes in a PR.
- **Security overview** — an organization-wide dashboard of alerts and coverage.

These tools shift security **left** — catching issues in the PR, before they ship. This chapter teaches
GHAS with hands-on walkthroughs (workflow/config plus alert triage), all defensive on your own repos.

## Design Considerations

Enable **code scanning** on your default branch and PRs, and triage alerts by severity. Turn on **secret
scanning with push protection** so secrets are blocked at push time (and rotate any already leaked). Let
**Dependabot** alert and open update PRs, and require **dependency review** on PRs to block known-vulnerable
additions. Use the **security overview** to track coverage across the org. Treat findings as work to fix,
not noise to dismiss.

## Implementation and Automation

The labs enable CodeQL code scanning, reason about secret-scanning push protection, and reason about
Dependabot — the defensive security the GHAS exam validates.

## Validation and Troubleshooting

Confirm Advanced Security:

```text
Code scanning (CodeQL): static analysis -> alerts on PRs + Security tab (run via Actions)
Secret scanning: detect committed credentials; PUSH PROTECTION blocks the push before it lands
Dependabot: alerts (Advisory DB) + security/version update PRs + dependency review on PRs
Security overview: org-wide alert + coverage dashboard; shift security LEFT (catch in the PR)
```

Common pitfalls: enabling scanning but never **triaging** the alerts; and disabling **push protection**
because it "gets in the way" — it prevents leaks (rotate any secret that slipped through).

## Security and Best Practices

Everything here is **defensive**: scanning and securing **your own** code, secrets, and dependencies.
Fix findings, rotate leaked secrets, and keep dependencies patched. There is no offensive content. All
work is authorized security of your own repositories.

## Hands-On Lab

Advanced Security walkthroughs (defensive). **Shared prerequisites** — a GitHub repo with GHAS features
available; `gh` and a workflow file. **Cost:** none (public repos; GHAS on private per plan).

### Lab 6.1 — Enable CodeQL code scanning

**Objective:** Statically analyze code for vulnerabilities.

```yaml
# .github/workflows/codeql.yml
name: CodeQL
on:
  push: { branches: [ main ] }
  pull_request: { branches: [ main ] }
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions: { security-events: write, contents: read }
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with: { languages: javascript }
      - uses: github/codeql-action/analyze@v3
```

```text
# after a run, alerts appear under Security > Code scanning
gh api repos/octocat/repo/code-scanning/alerts --jq 'length'
2
```

**Expected result:** CodeQL runs on push/PR and reports code-scanning alerts in the Security tab.

**Negative test:** run CodeQL but never look at the Security tab; **triage** the alerts and fix the
high-severity ones.

**Rollback:** none yet.

### Lab 6.2 — Reason about secret scanning and push protection

**Objective:** Block secrets before they land.

```python
python3 - <<'PY'
def push(files, push_protection):
    leaked = [f for f in files if "AKIA" in files[f] or "ghp_" in files[f]]
    if push_protection and leaked:
        return f"BLOCKED: secret detected in {leaked} (rotate + remove before pushing)"
    return "pushed"
files = { "config.js": 'const key="AKIAEXAMPLE123";' }
print(push(files, push_protection=True))
print(push(files, push_protection=False))
PY
```

```text
BLOCKED: secret detected in ['config.js'] (rotate + remove before pushing)
pushed
```

**Expected result:** with push protection on, the commit containing a key is **blocked**; without it, the
secret lands (and must be rotated).

**Negative test:** commit an API key with push protection off and assume it is fine; enable **push
protection** and rotate any leaked secret.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Reason about Dependabot

**Objective:** Keep dependencies patched.

```python
python3 - <<'PY'
deps = { "lodash": "4.17.11", "express": "4.18.2" }
advisories = { "lodash": ("<4.17.12", "high - prototype pollution") }
for pkg, ver in deps.items():
    if pkg in advisories:
        rng, sev = advisories[pkg]
        print(f"Dependabot ALERT: {pkg}@{ver} vulnerable ({sev}) -> opens PR to bump")
    else:
        print(f"{pkg}@{ver}: no known advisory")
PY
```

```text
Dependabot ALERT: lodash@4.17.11 vulnerable (high - prototype pollution) -> opens PR to bump
express@4.18.2: no known advisory
```

**Expected result:** Dependabot flags the vulnerable dependency and opens an update PR — automated
supply-chain patching.

**Negative test:** ignore Dependabot PRs for months; review and merge **security updates** promptly, and
require **dependency review** on PRs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Require dependency review on PRs

**Objective:** Block known-vulnerable additions at PR time.

```yaml
# .github/workflows/dep-review.yml
name: Dependency Review
on: pull_request
permissions: { contents: read }
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/dependency-review-action@v4
        with: { fail-on-severity: high }
```

```text
# a PR adding a high-severity vulnerable dependency fails the check
```

**Expected result:** PRs that introduce a high-severity vulnerable dependency **fail** the check —
blocked before merge.

**Negative test:** allow any dependency to be added and scan only after release; **dependency review**
catches it in the PR.

**Rollback:**

```bash
git rm .github/workflows/codeql.yml .github/workflows/dep-review.yml && git commit -m "Remove demo GHAS workflows" && git push
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub Advanced Security is defensive: CodeQL code scanning finds vulnerabilities and reports them on PRs;
secret scanning with push protection blocks committed credentials; Dependabot alerts on and updates
vulnerable dependencies while dependency review blocks risky PR additions; and the security overview
tracks coverage — shifting security left into the pull request.

- [ ] I can enable CodeQL code scanning.
- [ ] I can reason about secret scanning and push protection.
- [ ] I can reason about Dependabot alerts and updates.
- [ ] I can require dependency review on PRs.
- [ ] I completed Labs 6.1–6.4 including each negative test.
