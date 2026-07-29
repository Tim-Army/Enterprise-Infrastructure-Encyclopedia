# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Plan preparation with GitHub's free learning resources.
- Register for a PSI-delivered exam.
- Sequence the five certifications into a career path.
- Keep certifications current with the evolving platform.
- Complete a walkthrough for each prep-and-career topic.

## Theory and Architecture

Earning GitHub certifications follows a consistent path. Preparation is **free**: **GitHub Skills**
(hands-on, interactive courses that run in real repositories), the **learning paths** on GitHub's
certification resources, and the **docs**. Each certification page lists the **skills measured** and links
to register. Exams are booked and delivered through **PSI** — at a test center or **online-proctored**
with a secure browser — for **$99** each (GitHub Foundations is currently **50% off**), with **100
minutes** to complete. Because there are no formal prerequisites, most people start with **Foundations**
and branch into **Actions**, **Advanced Security**, **Administration**, or **Copilot** by role. The
platform evolves quickly, so certifications should be refreshed as features change and exam objectives
are updated; the credentials are also visible on **Microsoft Learn** (GitHub is a Microsoft company). A
GitHub-skilled career ladders from developer (Foundations) into DevOps/platform (Actions,
Administration), application security (GHAS), and AI-assisted development (Copilot). This chapter closes
the volume with prep, currency, and career walkthroughs.

## Design Considerations

Prepare with the **free GitHub Skills** courses and learning paths, practicing in a real repository
(this volume's labs). Register early through **PSI** and check the **online-proctored** system
requirements. Start with **Foundations** (using the discount) and add role certifications. Keep skills
**current** as GitHub ships features (Actions, GHAS, Copilot evolve fast). Track objectives on the
official certification pages.

## Implementation and Automation

The labs plan a preparation path, model the registration flow, and map the five certifications to a
career — the progression the program supports.

## Validation and Troubleshooting

Confirm prep, currency, and career:

```text
Prep: GitHub Skills (interactive) + learning paths + docs (all free); practice in a real repo
Register: via PSI; test center or online-proctored (secure browser); $99 (Foundations 50% off); 100 min
Start: Foundations -> Actions / GHAS / Administration / Copilot by role
Currency: refresh as features + objectives change; credentials also on Microsoft Learn
```

Common pitfalls: studying only theory without **hands-on** practice for role exams; and letting skills
go **stale** as the platform ships new features — refresh periodically.

## Security and Best Practices

Prepare on your own repositories, keep tokens least-privilege, and apply the security practices
throughout this volume as you learn. All work is authorized development and administration of your own
GitHub.

## Hands-On Lab

Prep-and-career walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Plan a preparation path

**Objective:** Sequence free resources to an exam.

```python
python3 - <<'PY'
plan = [
  "1. GitHub Skills interactive courses (real repos) for the target track",
  "2. Learning path + docs for the skills measured on that exam",
  "3. Hands-on practice (this volume's git/gh/Actions labs)",
  "4. Register via PSI (test center or online-proctored)",
  "5. Sit the exam ($99; Foundations 50% off; 100 minutes)",
]
for step in plan: print(step)
PY
```

**Expected result:** a free-first preparation path ending at the PSI exam.

**Negative test:** cram theory with no hands-on repos; the role exams assume **practice** — use GitHub
Skills and real repos.

**Cleanup:** none.

### Lab 9.2 — Model the registration flow

**Objective:** Know what booking requires.

```python
python3 - <<'PY'
steps = {
  "Choose exam":   "Foundations / Actions / GHAS / Administration / Copilot",
  "Provider":      "PSI (from the GitHub certification registration page)",
  "Delivery":      "test center OR online-proctored (secure browser + reliable internet)",
  "Fee":           "$99 (Foundations 50% off, limited time)",
  "Duration":      "100 minutes",
}
for k, v in steps.items(): print(f"{k:12}: {v}")
PY
```

**Expected result:** the registration essentials — provider, delivery, fee, and duration.

**Negative test:** book an online-proctored exam without checking the **secure-browser/system**
requirements; verify them first to avoid a failed check-in.

**Cleanup:** none.

### Lab 9.3 — Map a GitHub career

**Objective:** Sequence the five certifications.

```python
python3 - <<'PY'
ladder = {
  "GitHub Foundations":     "developer baseline (Git + collaboration)",
  "GitHub Actions":         "DevOps / CI-CD engineer",
  "GitHub Administration":  "platform / org administrator",
  "GitHub Advanced Security":"application security engineer",
  "GitHub Copilot":         "AI-assisted development across roles",
}
for cert, arc in ladder.items(): print(f"{cert:26}: {arc}")
print("Currency: refresh as GitHub ships features; credentials also visible on Microsoft Learn")
PY
```

**Expected result:** the five certifications mapped to career arcs from developer to platform/security/AI
roles.

**Negative test:** collect a certification and never use the skills as the platform evolves; keep them
**current** with new features.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub certification prep is free — GitHub Skills, learning paths, and docs, practiced in real
repositories — with exams booked through PSI (test center or online-proctored, $99, 100 minutes,
Foundations discounted). Starting at Foundations and branching into Actions, Advanced Security,
Administration, and Copilot ladders a career from developer to DevOps, security, and AI-assisted roles,
kept current as the platform evolves.

- [ ] I can plan a preparation path with free resources.
- [ ] I can model the PSI registration flow.
- [ ] I can sequence the five certifications into a career.
- [ ] I can keep certifications current with the platform.
- [ ] I completed Labs 9.1–9.3 including each negative test.
