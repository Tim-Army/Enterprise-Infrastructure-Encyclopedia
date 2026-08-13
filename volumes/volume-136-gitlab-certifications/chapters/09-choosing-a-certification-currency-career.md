# Chapter 09: Choosing a Certification, Currency, and Career

## Learning Objectives

- Choose and sequence GitLab certifications for your role.
- Use the free learning paths before paying for an exam.
- Track GitLab product versions rather than an expiry date.
- Place GitLab among the encyclopedia's other DevOps and platform volumes.

## Choosing a certification

| If you… | Take | Chapters |
|:---|:---|:---|
| Are new to GitLab | **Certified Fundamentals Associate** (GitLab's recommended first) | 02–04, 06 |
| Build and maintain pipelines | **Certified CI/CD Associate** | 04, 05, 08 |
| Plan and coordinate work | **Certified Agile Portfolio Management Associate** | 03 |
| Own application security | **Certified Security Associate** | 06 |
| Work with AI agents in the platform | **Certified GitLab Duo Agent Platform Associate** | 07 |

**Start with Fundamentals** regardless of specialization — GitLab says so explicitly, and it is sound: it assesses the foundational platform knowledge the other four assume, so taking a specialist exam first means learning that material anyway without the credential.

A practical sequence: **Fundamentals → the specialization matching your daily work → a second specialization as your role widens.** All five are Associate level, so this is a breadth ladder rather than a depth one; the handbook's **Professional** tier (90 minutes, 60 questions, proctored via Certiverse) is the defined depth step above.

## Work the free paths first

Every exam has **free, self-paced learning content** with interactive elements and practice opportunities: **GitLab Fundamentals**, **GitLab CI Fundamentals**, **Agile Portfolio Management**, **GitLab Security Essentials**, and **GitLab Duo**.

The economics make this unambiguous. Exams cost **$150** with **no discounted retake** — a failed attempt means paying full price again. The learning path costs nothing. There is no scenario in which skipping it is rational.

Two mechanics to plan around, both from the handbook:

- **The 14-day access window starts at purchase**, and enrollment auto-expires whether or not you sat the exam. Buy when you can actually sit it.
- **Two attempts per window.** Fail both and you wait out the window before repurchasing.

## Currency: track versions, not dates

GitLab's model inverts the usual advice. Certifications **do not expire**; they are governed by **product versioning**. Recertification may be required when a major version materially changes the validated skills, with advance notice, multiple options, and existing certifications valid through the transition.

So there is no renewal date to diary. What you should track instead is **GitLab's release cadence and major version changes** — that is the trigger for revalidation, and it is also simply how you stay useful, since the platform ships continuously.

The **Duo Agent Platform** certification is the one most exposed to this. It covers the newest, fastest-moving surface of the product (agentic flows, MCP tool connection), so expect its content to move more than, say, the CI/CD fundamentals.

## Where GitLab sits in the encyclopedia

- **GitLab (this volume)** — the single-application DevSecOps platform: source, CI/CD, security, planning, and deployment in one product.
- [**GitHub LXXXIX**](../../volume-089-github-certifications/README.md) — the counterpart platform. Worth holding both if you work across organizations; the concepts transfer and the vocabulary does not.
- [**Docker XCII**](../../volume-092-docker-certifications/README.md) and [**CNCF/Kubernetes XLI**](../../volume-041-cncf-kubernetes-certifications/README.md) — what pipelines usually build and deploy to.
- [**HashiCorp XLII**](../../volume-042-hashicorp-certifications/README.md) — Terraform and Vault, commonly driven *from* GitLab CI.
- [**Infrastructure Automation IX**](../../volume-009-infrastructure-automation/README.md) and [**Containers and Platform Engineering VIII**](../../volume-008-containers-platform-engineering/README.md) — the vendor-neutral disciplines.

GitLab's distinctive contribution to this shelf is **integration**: the security findings of Chapter 06 appear in the merge request of Chapter 02, gated by the pipeline of Chapter 05, planned by the epics of Chapter 03 — one data model rather than five tools wired together.

## Hands-On Lab

### Lab 9.1 — Build your GitLab certification plan

**Objective:** Sequence free learning before a paid exam.

```bash
cat > my-gitlab-plan.md <<'EOF'
My role:          developer / platform engineer / security / delivery lead
FREE FIRST:       [ ] GitLab Fundamentals learning path
                  [ ] the path matching my target exam (CI, Agile PM, Security, or Duo)
Then exam 1:      Certified Fundamentals Associate      ($150, 75 min, 50 Q, 75% to pass)
Then exam 2:      CI/CD  /  Agile Portfolio Mgmt  /  Security  /  Duo Agent Platform
Buy when ready:   the 14-DAY window starts AT PURCHASE and auto-expires
Attempts:         2 per window; fail both -> wait out the window, repurchase at FULL price
During the exam:  no phone, no notes, no other people — and NO AI/automated tools (Code of Conduct)
Expiry:           NONE — version-based. Track GitLab MAJOR RELEASES instead of a renewal date.
Practice:         model pipelines, rules, scanners, agent permissions free in Python
EOF
cat my-gitlab-plan.md
```

**Expected result:** A plan that puts the free path before the paid exam, buys only when the two-week window can be used, and replaces the usual renewal-date reminder with release tracking. The AI line is worth keeping in writing: it is easy to assume a certification *about* AI agents tolerates AI assistance during the exam, and it does not.

**Negative test:** Buying all five exams at once to "lock in" a plan — every enrollment starts its own 14-day clock, and the ones you cannot reach in two weeks expire unused at $150 each.

**Rollback:** Keep the plan.

### Lab 9.2 — Self-assess against the exam domains

**Objective:** Find the weak domain for your specific target exam.

```bash
python3 - <<'EOF'
domains = {
  "Git, groups, MRs (ch02)":              4,
  "Agile portfolio management (ch03)":    2,
  "CI/CD fundamentals (ch04)":            3,
  "Advanced CI/CD: rules, DAG (ch05)":    2,
  "Security scanning (ch06)":             1,
  "Duo & Agent Platform (ch07)":          1,
  "Runners & administration (ch08)":      3,
}
print("Self-rated confidence (0-5):\n")
for d, s in sorted(domains.items(), key=lambda kv: kv[1]):
    print(f"{d:40} [{'#'*s}{'.'*(5-s)}] {'STUDY FIRST' if s <= 2 else ('review' if s < 4 else 'ready')}")

exams = {
  "Fundamentals Associate":   ["ch02","ch03","ch04","ch06"],
  "CI/CD Associate":          ["ch04","ch05","ch08"],
  "Agile Portfolio Mgmt":     ["ch03"],
  "Security Associate":       ["ch06"],
  "Duo Agent Platform":       ["ch07"],
}
print("\nChapter coverage per exam:")
for e, chs in exams.items():
    weak = [c for c in chs if domains[[k for k in domains if c in k][0]] <= 2]
    flag = f"   <-- weak in {weak}" if weak else ""
    print(f"  {e:26} {', '.join(chs)}{flag}")
print("\nFundamentals is broad (ch02-04, 06), so a weak ch06 blocks it AND the Security exam.")
print("Study for your TARGET exam's scope — a low ch07 is irrelevant unless you're sitting Duo.")
EOF
```

**Expected result:** Security scanning and the Duo material sort to the bottom, and the coverage map shows a weak Chapter 06 blocking **two** exams — Fundamentals (which includes security scanning) and the Security Associate. That overlap is the useful output: it identifies the single domain whose improvement unlocks the most, rather than treating all weak areas as equally urgent.

**Negative test:** Studying evenly across all nine chapters for the Agile Portfolio Management exam — its scope is essentially one chapter, so most of that effort earns nothing toward the credential.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A target certification chosen, with Fundamentals sequenced first.
- [ ] Free learning paths worked before any $150 purchase.
- [ ] The 14-day window, two-attempt limit, and full-price retake planned around.
- [ ] Version-based (non-expiring) currency understood: track major releases, not a renewal date.
- [ ] GitLab placed against GitHub, Docker, Kubernetes, and HashiCorp on the platform shelf.
