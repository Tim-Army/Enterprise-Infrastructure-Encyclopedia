# Chapter 01: The GitLab Program and the DevSecOps Platform

![The GitLab certification program in GitLab University: five Associate certifications — Certified Fundamentals Associate (the recommended starting point), Certified CI/CD Associate, Certified Agile Portfolio Management Associate, Certified Security Associate, and the new Certified GitLab Duo Agent Platform Associate covering agentic AI, custom agents and flows, and MCP tool connection. Each Associate exam is 75 minutes, 50 multiple-choice and multiple-select questions, delivered unproctored online, costing 150 US dollars, with a 75 percent passing score, a 14-day access period allowing two attempts, and results shown immediately. The handbook also defines a Professional level at 90 minutes and 60 questions, proctored through Certiverse. Distinctively, GitLab certifications do not expire: they are governed by GitLab product versioning rather than time-based expiry. Free self-paced learning paths back every exam, and badges issue through Credly.](../../../diagrams/volume-136-gitlab-certifications/chapter-01-certification-program.svg)

*Figure 1-1. GitLab's five Associate certifications, their shared exam mechanics, and the free learning paths beneath them.*

## Learning Objectives

- Describe the GitLab certification program and its five Associate certifications.
- Explain the exam mechanics: format, fee, attempts, passing score, and the access window.
- Understand GitLab's distinctive version-based (non-expiring) certification model.
- Set up a free study environment for the labs in this volume.

## What GitLab is

GitLab is a **single-application DevSecOps platform**. That phrase is marketing, but it describes a real architectural choice: source control, code review, CI/CD, security scanning, package registries, issue tracking, and deployment live in one product with one data model, rather than being assembled from separate tools.

The comparison worth holding is with [GitHub (Volume LXXXIX)](../../volume-089-github-certifications/README.md). Both host Git repositories and run pipelines; the difference is philosophical. GitHub grew from repository hosting outward and integrates heavily with a marketplace ecosystem; GitLab set out to include the whole lifecycle in one application. Neither approach is simply better, and both certifications are worth holding if you work across environments.

## The certification program

GitLab Certification runs in **GitLab University**, and its published **Candidate Handbook & Exam Guide** is unusually explicit — duration, question counts, passing score, retake rules, and accommodation policy are all stated outright, which is why this chapter can be precise where other vendors' chapters must hedge.

### The five Associate certifications

| Certification | Validates |
|:---|:---|
| **Certified Fundamentals Associate** | Core workflows (merge requests, issues), basic CI/CD pipelines, security scanning setup, agile planning across the SDLC |
| **Certified CI/CD Associate** | What CI/CD is, the components of a pipeline, GitLab's CI/CD functions and how to use them |
| **Certified Agile Portfolio Management Associate** | Organizational structure, issue lifecycles with labels and dependencies, boards, epics and roadmaps, team velocity |
| **Certified Security Associate** | SAST, DAST, secret detection, dependency and container scanning; security policies and merge-request approval workflows; license compliance |
| **Certified GitLab Duo Agent Platform Associate** *(new)* | Agentic chat, selecting the right agent for a task, configuring and publishing **custom agents and flows**, connecting external tools via **MCP**, and AI-assisted code creation, review, and security workflows |

GitLab recommends beginning with **Certified Fundamentals Associate**, because it assesses the foundational knowledge the others assume.

The handbook also defines a **Professional** level — 90 minutes, 60 questions, proctored through **Certiverse**, with Associate recommended first. At the time of writing the published catalog lists Associate certifications only, so treat Professional as the defined tier above rather than a specific exam you can book today.

### Exam mechanics

| | **Associate** | **Professional** (defined) |
|:---|:---|:---|
| Duration | **75 minutes** | 90 minutes |
| Questions | **50** | 60 |
| Types | Multiple choice, multiple select | Same |
| Delivery | **Unproctored online** | **Proctored** (Certiverse) |
| Prerequisites | None | Associate recommended |
| Recommended experience | **3–6 months** hands-on GitLab | 1–2 years professional development or DevSecOps |

- **Fee: $150 USD** — notably the *same* for both levels.
- **Passing score: 75%**, criterion-referenced, counting scored questions only.
- **Access period: 14 days** from purchase, with **automatic unenrollment** afterward regardless of completion.
- **Attempts: 2 per 14-day window.** Fail both and you wait out the window, then repurchase — unlimited repurchases, but **no discounted retake pricing**.
- **Results immediately**, then a **Credly** badge and a certificate with a verification code.
- **Prohibited during exams:** phones, smartwatches and devices, reference materials, other people in the room — and explicitly **"using artificial intelligence or automated tools."** Worth noting given that one of the certifications is *about* AI agents: knowing how to drive Duo is examinable, using an assistant to answer the exam is a Code of Conduct violation.

The unproctored delivery of Associate exams is unusual, and it rests on that Code of Conduct rather than on surveillance. Violations carry real consequences — score invalidation, certification revocation, program ban.

## The distinctive part: certifications do not expire

Most vendor certifications expire on a clock — two years for [Confluent](../../volume-135-confluent-certifications/README.md) and [SailPoint](../../volume-132-sailpoint-certifications/README.md), three for [SolarWinds](../../volume-134-solarwinds-certifications/README.md). GitLab does something different:

> GitLab certifications **do not expire** and are governed by **GitLab product versioning** rather than time-based expiration.

Recertification may be required when a **major product version** materially changes the skills a certification validates. When that happens, GitLab commits to advance notice, multiple recertification options, and existing certifications remaining valid during the transition.

This is a defensible model: a time-based clock assumes knowledge decays at a fixed rate, whereas version-based recertification ties revalidation to the thing that actually invalidates knowledge — the product changing. The practical implication for you is the reverse of the usual advice: there is no renewal date to diary, but you *should* track major GitLab releases, because that is what will trigger revalidation.

## Free preparation

Every exam has **free, self-paced learning content** with interactive elements and practice opportunities. The published learning paths are: **GitLab Fundamentals**, **GitLab CI Fundamentals**, **Agile Portfolio Management**, **GitLab Security Essentials**, and **GitLab Duo**.

Because the exams cost $150 with no discounted retake, working the free path first is straightforwardly economical.

## Free study environment

GitLab itself is free to use — GitLab.com has a free tier, and self-managed Community Edition costs nothing. This volume's labs, though, model the **concepts** the exams test — pipeline dependency resolution, `rules` evaluation, scanner findings triage, approval-policy gates, agent tool permissions, runner and cache sizing — in plain Python, so they run in seconds without any account.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain for this volume.

```bash
python3 --version
git --version
mkdir -p ~/gitlab-study && cd ~/gitlab-study
python3 - <<'EOF'
print("DevSecOps study environment ready.")
print("Labs model: pipeline DAGs, rules evaluation, scanner triage, approval policies,")
print("agent tool permissions, runner sizing — no GitLab account required.")
print("Optional: GitLab.com free tier or self-managed CE, both free.")
EOF
```

**Expected result:** Python and Git report versions and the message prints. Git is worth having because Chapter 02's material is genuinely about Git underneath GitLab's interface.

**Negative test:** Assuming you need a paid GitLab tier to study — the free tier covers everything the Associate exams assess, and the concepts model fine locally.

**Cleanup:** `rm -rf ~/gitlab-study` when finished.

### Lab 1.2 — Plan against the exam mechanics

**Objective:** Turn the handbook's rules into a plan that avoids wasting a $150 purchase.

```bash
python3 - <<'EOF'
FEE, WINDOW_DAYS, ATTEMPTS, PASS_PCT, QUESTIONS, MINUTES = 150, 14, 2, 75, 50, 75

def plan(free_path_done, practice_score, days_free_in_window):
    notes = []
    ready = True
    if not free_path_done:
        notes.append("Work the FREE learning path first — same content, no cost, and retakes are full price")
        ready = False
    if practice_score < PASS_PCT:
        notes.append(f"Practice at {practice_score}% is below the {PASS_PCT}% pass mark — keep studying")
        ready = False
    if days_free_in_window < 3:
        notes.append(f"Only {days_free_in_window} usable day(s) in the {WINDOW_DAYS}-day window — "
                     "buy when you can actually sit it; enrollment auto-expires")
        ready = False
    return ready, notes

for case in [(False, 60, 10), (True, 68, 10), (True, 82, 1), (True, 88, 9)]:
    ready, notes = plan(*case)
    print(f"\nfree_path={case[0]} practice={case[1]}% days_free={case[2]} -> {'BUY AND SIT' if ready else 'NOT YET'}")
    for n in notes: print(f"   - {n}")

print(f"\nMechanics: ${FEE} · {MINUTES} min · {QUESTIONS} questions · {PASS_PCT}% to pass")
print(f"{ATTEMPTS} attempts inside a {WINDOW_DAYS}-day window, then auto-unenrollment.")
print(f"Pace: {MINUTES*60/QUESTIONS:.0f} seconds per question.")
EOF
```

**Expected result:** Only the last case clears every gate. The 14-day window is the trap the handbook makes explicit and candidates still fall into — **purchase starts the clock**, and enrollment expires whether or not you sat the exam. Buying "to commit yourself" and then getting busy costs the full $150 with nothing to show. The closing line converts the format into a pace: 90 seconds per question.

**Negative test:** Buying the exam before working the free learning path — you pay $150 for content that was available at no cost, and a failed second attempt means paying again at full price.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The five Associate certifications named, with Fundamentals identified as the starting point.
- [ ] Exam mechanics recorded: $150, 75 minutes, 50 questions, 75% to pass, 2 attempts per 14-day window.
- [ ] Associate exams understood as unproctored, governed by the Code of Conduct (AI tools prohibited).
- [ ] The version-based, non-expiring certification model understood, and its practical implication.
- [ ] Free learning paths identified as the first step; study environment ready.
