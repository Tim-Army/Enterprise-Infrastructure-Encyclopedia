# Chapter 01: The GitHub Certification Program

## Learning Objectives

- Describe the five GitHub certifications and what each validates.
- Explain the exam format, PSI delivery, and pricing.
- Explain the free GitHub learning resources.
- Place the certifications against the platform skill set.
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

**GitHub** certifications validate skills on the world's largest software-development platform. There are
five:

- **GitHub Foundations** — the foundational topics of collaborating and contributing on GitHub: Git
  basics, GitHub products, and working within repositories.
- **GitHub Actions** — automating workflows and accelerating development: streamlining workflows,
  automating tasks, and optimizing software pipelines (CI/CD).
- **GitHub Advanced Security (GHAS)** — security practices and vulnerability management: vulnerability
  identification, workflow security, and security implementation.
- **GitHub Administration** — optimizing and managing a healthy GitHub environment: repository
  management, workflow optimization, and efficient collaboration at organization/enterprise scale.
- **GitHub Copilot** — optimizing development with AI: responsible AI, Copilot plans and features, data
  and functionality, prompt engineering, AI developer use cases, testing with Copilot, and privacy and
  exclusions.

All exams are **$99 USD** (GitHub Foundations is **50% off** for a limited time), delivered through
**PSI** at a test center or **online-proctored** with a secure browser, with **100 minutes** to
complete. GitHub is a Microsoft company, and the certifications are cross-listed on Microsoft Learn.
Preparation is free through **GitHub's learning resources** (learning paths and the interactive **GitHub
Skills** courses) and the docs. This chapter orients you on a free GitHub account and local `git`/`gh`
so the certifications map to real commands.

## Design Considerations

Pick the certification that matches your role — **Foundations** to start, **Actions** for CI/CD,
**GHAS** for application security, **Administration** for platform operations, **Copilot** for AI-assisted
development. Because there are **no formal prerequisites**, you can start with **Foundations** (and take
advantage of its discount) and branch. Prepare with the free **GitHub Skills** interactive courses and
the learning paths.

## Implementation and Automation

The labs authenticate the `gh` CLI, read the platform version/context, and map the certification ladder —
the orientation every GitHub candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Foundations : Git + GitHub collaboration basics (50% off, limited time)
Actions     : workflow automation + CI/CD
Advanced Security (GHAS): code/secret/dependency scanning + vulnerability management
Administration: org/enterprise management, policies, SSO
Copilot     : responsible AI, features, prompt engineering, privacy
Exams: $99; PSI (test center / online-proctored); 100 minutes; cross-listed on Microsoft Learn
```

Common pitfalls: assuming a single "GitHub exam" — there are **five** role-specific certifications; and
paying full price for **Foundations** while the **50% discount** is available.

## Security and Best Practices

GitHub certifications validate building, automating, securing, and administering **your own**
repositories and organizations. Authenticate the `gh` CLI with least-privilege scopes and protect your
tokens. All work in this volume is authorized administration.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a free **GitHub account**, local **`git`**
and the **`gh`** CLI, and `python3` for ladder planning. **Cost:** none (free account + free tools).

### Lab 1.1 — Authenticate and read your context

**Objective:** Confirm a working GitHub CLI session.

```bash
gh auth status
gh api user --jq '.login'
```

```text
github.com
  ✓ Logged in to github.com account octocat (keyring)
  - Token scopes: 'repo', 'read:org', 'workflow'
octocat
```

**Expected result:** an authenticated `gh` session with least-privilege scopes — the platform the
certifications validate.

**Negative test:** authenticate a token with `admin:org`/broad scopes for routine work; request only the
scopes you need (`repo`, `workflow`).

**Rollback:** none (read-only).

### Lab 1.2 — Map the certification ladder

**Objective:** Reason about the five credentials.

```python
python3 - <<'PY'
certs = {
  "GitHub Foundations":     "Git + collaboration basics (start here; 50% off)",
  "GitHub Actions":         "workflow automation + CI/CD",
  "GitHub Advanced Security":"code/secret/dependency scanning (defensive)",
  "GitHub Administration":  "org/enterprise management + policies + SSO",
  "GitHub Copilot":         "responsible AI + prompt engineering + privacy",
}
for cert, focus in certs.items():
    print(f"{cert:26}: {focus}")
print("All $99 (Foundations 50% off); PSI-proctored; 100 minutes; no formal prereqs")
PY
```

**Expected result:** the five certifications mapped to their focus.

**Negative test:** plan to sit **Administration** to learn Git basics; **Foundations** grounds Git and
collaboration — start there.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Confirm the tooling and a practice repo

**Objective:** See the tools the exams assume.

```bash
git --version
gh repo create cert-practice --private --clone
cd cert-practice && ls -a
```

```text
git version 2.46.0
✓ Created repository octocat/cert-practice on GitHub
✓ Cloned repository
.  ..  .git
```

**Expected result:** `git` and `gh` working, with a private practice repository cloned — a ready
environment.

**Negative test:** practice only in the web UI; the exams and real work assume **`git`/`gh`** fluency —
use the CLI too.

**Rollback:**

```bash
gh repo delete octocat/cert-practice --yes
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub offers five certifications — Foundations, Actions, Advanced Security, Administration, and Copilot —
each a $99 PSI-proctored, 100-minute exam (Foundations 50% off), with no formal prerequisites, free
GitHub learning resources, and cross-listing on Microsoft Learn, spanning Git collaboration, CI/CD,
application security, platform administration, and AI-assisted development.

- [ ] I can describe the five certifications.
- [ ] I can explain the exam format, PSI delivery, and pricing.
- [ ] I can explain the free GitHub learning resources.
- [ ] I completed Labs 1.1–1.3 including each negative test.
