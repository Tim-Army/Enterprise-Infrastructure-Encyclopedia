# Chapter 09: Choosing Your Snyk Path

## Learning Objectives

- Sequence a Snyk Learn path by role.
- Understand what "currency" means for a certificate-of-completion program.
- Place Snyk skills in the AppSec / DevSecOps career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate Snyk Learn [Chapter 1](01-the-snyk-learn-program.md) laid out.*

## Sequencing your path

Snyk Learn is free and self-paced, so the path is about **which learning paths, in what order**, for your role:

| You are | Start | Then |
|:---|:---|:---|
| **Developer** | Security for Developers | OWASP Top 10 → language-specific lessons → Snyk product training |
| **AppSec engineer** | OWASP Top 10 | Snyk Open Source / Code / Container / IaC product paths |
| **Platform / DevSecOps** | Snyk product training (all four engines) | Implementing Snyk: Enterprise Admin & Architecture |
| **AI-focused developer** | Secure AI Development | OWASP Top 10 for LLM/GenAI → Agentic → AI Security University |

**Security for Developers is the anchor** for anyone writing code — it grounds the vulnerability classes ([OWASP](07-ai-and-secure-development.md)) that every engine and every language lesson build on. From there, the product training teaches the four engines, and the **Enterprise Admin & Architecture** path is the destination for whoever will *roll Snyk out* across an organization.

Because everything is **free and self-paced**, the sensible strategy is simply to *walk the paths* — earn the certificates of completion as you go, and let the AI-security paths (the fastest-moving, most in-demand area) be the differentiator on top of the fundamentals.

## Currency

A certificate of completion does not "expire" the way a proctored cert does — but the **knowledge does**, and fast. Application security moves quickly: new vulnerability classes (the whole [AI-security wave, Chapter 7](07-ai-and-secure-development.md) is barely two years old), new OWASP revisions, new language and framework risks. The currency discipline here is not "renew a badge" but "**keep walking the paths**" — Snyk Learn adds content continuously, and the free model means staying current costs only time.

This is the flip side of the [badges-only nature (Chapter 1)](01-the-snyk-learn-program.md): there is no renewal fee and no expiry pressure, but also no external forcing function — *you* have to keep learning, because a two-year-old understanding of AppSec (pre-agentic-AI) is genuinely out of date. Treat each major OWASP update and AI-security release as the drumbeat.

## The AppSec / DevSecOps career

Snyk skills sit in a growing, well-paid specialty: **application security is where software risk concentrates**, and "shift-left, developer-first AppSec" is the model the industry has converged on. A developer who can find-and-fix across code, dependencies, containers, and IaC — and who understands AI-code security — is exactly the DevSecOps profile in demand.

The career pairs naturally with adjacent skills this shelf covers:

- **[Wiz (CXLVII)](../../volume-147-wiz-certifications/README.md)** — the *cloud* security side; Snyk is the *application* side, and together they cover code-to-cloud.
- **[GitLab (CXXXVI)](../../volume-136-gitlab-certifications/README.md) / [GitHub (LXXXIX)](../../volume-089-github-certifications/README.md)** — the pipeline Snyk plugs into for CI/CD gating.
- **[CNCF Kubernetes (XLI)](../../volume-041-cncf-kubernetes-certifications/README.md)** — the container/IaC runtime Snyk scans for.
- **[OffSec (XLIII)](../../volume-043-offensive-security-certifications/README.md)** — the offensive counterpart; Snyk is the find-and-fix defense to their find-and-exploit.

Snyk is the developer-first AppSec specialty in a world where software (increasingly AI-written) is the attack surface. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal Snyk plan. **Cost:** none — literally, in this case.

### Lab 9.1 — Build your Snyk Learn path

**Objective:** Generate a role-appropriate sequence of learning paths.

```bash
python3 - <<'EOF'
PATHS = {
  "developer": [
    ("Security for Developers", "the anchor — OWASP vuln classes in your code"),
    ("OWASP Top 10", "the canonical web-app risks in depth"),
    ("(language lessons)", "Python/Java/JS/Go... secure patterns for your stack"),
    ("Secure AI Development", "securing AI-generated code (the differentiator)"),
  ],
  "AppSec / DevSecOps engineer": [
    ("OWASP Top 10 (+ OSS, LLM)", "the risk frameworks across web/deps/AI"),
    ("Snyk product training (4 engines)", "Open Source, Code, Container, IaC"),
    ("Implementing Snyk: Admin & Architecture", "rolling it out at scale"),
  ],
  "AI-focused developer": [
    ("Secure AI Development", "securing the AI-assisted SDLC"),
    ("OWASP Top 10 for LLM & GenAI", "AI-application risks"),
    ("OWASP Top 10 for Agentic Applications", "AI-agent / excessive-agency risks"),
    ("AI Security University Program", "the structured AI-security track"),
  ],
}
role = "developer"   # change to taste
print(f"Snyk Learn path for: {role}\n")
print("   (all free, self-paced, Certificate of Completion per path)\n")
for i, (path, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {path:42} {why}")
print("\nGuidance:")
print("  - developers ANCHOR on 'Security for Developers' — it grounds the OWASP vuln")
print("    classes every engine and language lesson builds on.")
print("  - then walk product training (the 4 engines) and/or the language paths.")
print("  - let the AI-SECURITY paths be your differentiator — fastest-moving, most")
print("    in-demand, and barely two years old.")
print("  - it's all FREE and self-paced: just WALK the paths, earn the certificates.")
print("  - 'currency' = keep walking (no expiry fee, but no forcing function either —")
print("    a pre-agentic-AI understanding of AppSec is already out of date).")
EOF
```

**Expected result:** A role-specific sequence of free Snyk Learn paths anchored on Security for Developers, with AI-security paths as the differentiator, each earning a certificate of completion. The build-your-path lesson is that everything is free and self-paced, so the strategy is simply to walk the paths — and currency means continuing to walk them, since there is no expiry fee but no forcing function either.

**Negative test:** Treating a Snyk certificate of completion as a done-forever credential. AppSec moves fast (the AI-security classes are barely two years old); a stale understanding is genuinely out of date, so currency here means continuing to learn, not holding a badge.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Position Snyk in the AppSec / DevSecOps career

**Objective:** Map Snyk skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Snyk (AppSec)",     "find-and-fix across code/deps/container/IaC", "the specialty itself"),
  ("Wiz (CNAPP)",       "cloud security posture",                      "the cloud side — together = code-to-cloud"),
  ("GitLab / GitHub",   "CI/CD pipeline",                              "where Snyk gates plug in"),
  ("CNCF / Kubernetes", "containers + orchestration",                  "what Snyk Container/IaC scan for"),
  ("OWASP",             "vulnerability taxonomy",                      "the risk classes underneath it all"),
  ("OffSec",            "offensive security",                          "the find-and-exploit to Snyk's find-and-fix"),
]
print("Snyk in the AppSec / DevSecOps skill map:\n")
print(f"   {'skill':20}{'domain':44}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:20}{domain:44}{why}")
print("\nThe career thesis: APPLICATION SECURITY is where software risk concentrates,")
print("and 'shift-left, developer-first AppSec' is the model the industry converged on.")
print("A dev who finds-AND-fixes across code, deps, containers, and IaC — and gets")
print("AI-code security — is the DevSecOps profile in demand.")
print("\nThe rounded AppSec engineer combines:")
print("  CODE + DEPS   (Snyk Code + Open Source) — your code and their code")
print("  CONTAINER+IaC (Snyk Container + IaC)    — the package and the infrastructure")
print("  CLOUD         (Wiz, CXLVII)             — code-to-cloud continuity")
print("  PIPELINE      (GitLab/GitHub)           — gate risk in CI/CD")
print("  AI            (Secure AI Development)    — the new, fast-growing surface")
print("\nNone of it is exotic — it's the same find/prioritize/fix loop the security")
print("shelf teaches, specialized to the APPLICATION and delivered to DEVELOPERS. Snyk")
print("Learn is free, so this is the rare career path you can start TONIGHT at zero")
print("cost. Walk the paths, pair with cloud + pipeline skills — that's a DevSecOps")
print("career, not just a certificate.")
EOF
```

**Expected result:** Snyk skills mapped to adjacent competencies — Wiz (cloud), GitLab/GitHub (pipeline), CNCF (containers), OWASP (taxonomy), OffSec (offense) — showing the rounded code/deps/container/IaC/cloud/AI DevSecOps profile. The career-positioning lesson closes the volume: Snyk is the developer-first AppSec specialty, free to start, pairing with the same cloud, pipeline, and AI skills the rest of the shelf teaches.

**Negative test:** Treating Snyk as a standalone scanner skill. It sits in the code-to-cloud continuum with Wiz, plugs into GitLab/GitHub pipelines, and rests on the OWASP taxonomy — isolating it undersells both the platform and the DevSecOps career.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A Snyk Learn path sequenced by role, anchored on Security for Developers with AI-security as the differentiator.
- [ ] Currency understood for a certificate-of-completion program — no expiry fee, but keep-walking is the discipline as AppSec moves fast.
- [ ] Snyk positioned in the AppSec / DevSecOps career alongside cloud (Wiz), pipeline, container, and AI skills.
- [ ] The volume assembled into a personal study and career plan — code, dependencies, container, IaC, cloud, AI.
