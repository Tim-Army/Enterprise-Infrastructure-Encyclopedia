# Chapter 01: The Snyk Learn Program

![The Snyk Learn program and the developer-security platform beneath it. Snyk Learn is free developer security education and product training, organized as learning paths and individual lessons: roughly eighteen learning paths and one hundred seventy-four lessons, split into security education and product training. Completing a learning path earns a downloadable Certificate of Completion; a free account tracks progress. Learning paths include Security for Developers, the OWASP Top 10, the OWASP Top 10 for large language models and generative AI, the OWASP Top 10 for agentic applications, OWASP Top 10 risks for open source software, Secure AI Development, and Implementing Snyk enterprise administration and architecture. A separate Snyk AI Security University Program offers structured AI-security education. The platform the product training covers spans four scanning engines plus posture management: Snyk Open Source for software composition analysis of dependencies, Snyk Code for static application security testing powered by DeepCode AI, Snyk Container for container image scanning with base-image recommendations, Snyk Infrastructure as Code for scanning Terraform, CloudFormation, and Kubernetes manifests before deployment, and an Application Security Posture Management solution across the software development lifecycle. Snyk positions itself as a developer security platform that gives visibility, context, and control to work alongside developers on reducing application risk, meeting developers in the IDE, command line, pull request, and CI/CD pipeline to find and fix vulnerabilities.](../../../diagrams/volume-148-snyk-certifications/chapter-01-snyk-learn-program.svg)

*Figure 1-1. Free learning paths with certificates of completion, over the developer-first application-security platform.*

## Learning Objectives

- Describe the Snyk Learn program — learning paths, lessons, and certificates of completion.
- Distinguish security education from product training.
- Place the four scanning engines (Open Source, Code, Container, IaC) plus ASPM.
- Recognize Snyk's position as the developer-first application-security platform.

## What Snyk is

Snyk is a **developer security platform** — its own words are "visibility, context, and control to work alongside developers on reducing application risk." Where the [Wiz volume (CXLVII)](../../volume-147-wiz-certifications/README.md) secures the *cloud*, Snyk secures the *application*: the code developers write, the open-source dependencies they pull in, the containers they package, and the infrastructure-as-code they deploy. Its defining stance is **developer-first** — security delivered *to developers, in their workflow*, so they find and fix issues as they build, rather than security handed down by a separate team after the fact.

## The Snyk Learn program

Snyk's education and credentialing is **Snyk Learn** — free, interactive developer-security education and product training. It is important to be precise about what kind of program this is:

> **A certificate-of-completion program, stated plainly.** Snyk Learn is **not** a proctored-exam certification like the cloud vendors'. You complete **learning paths** — sequences of interactive lessons — and earn a **downloadable Certificate of Completion** (a free account tracks your progress). It is a *learning* credential, not an *examination* credential. That is a genuine, valuable thing — free, hands-on, current — and this volume treats it as exactly what it is, neither inflating it into a proctored cert nor dismissing it.

Snyk Learn is organized in two axes:

| Axis | Meaning | Rough scale |
|:---|:---|:---|
| **Type** | Security education vs product training | ~128 security education, ~64 product training |
| **Format** | Learning paths vs individual lessons | ~18 learning paths, ~174 lessons |

A **learning path** bundles related lessons into a coherent journey with a certificate at the end; a **lesson** is a single interactive topic. The separate **Snyk AI Security University Program** offers structured AI-security education on top.

## The learning paths

The paths span both **vendor-neutral security education** and **Snyk product training**:

| Path | Is | Roughly |
|:---|:---|:---|
| **Security for Developers** | The flagship developer path | ~16 lessons / ~4 hrs |
| **OWASP Top 10** | The canonical web-app risk list | ~2.5 hrs |
| **OWASP Top 10 for LLM & GenAI** | AI-application risks | ~2.5 hrs |
| **OWASP Top 10 for Agentic Applications** | AI-agent risks | — |
| **OWASP Top 10 for Open Source** | Dependency risks | ~2.5 hrs |
| **Secure AI Development** | Securing the AI-assisted SDLC | ~1.5 hrs |
| **Implementing Snyk: Enterprise Admin & Architecture** | Admin/architect product training | ~1.25 hrs |

The **OWASP-heavy, AI-forward** shape is the signal: Snyk Learn teaches *security itself* (not just its own product), and it has pivoted hard toward **AI security** (LLM, GenAI, agentic) — the subject of [Chapter 7](07-ai-and-secure-development.md).

## The platform beneath

Snyk's product training covers four scanning engines plus posture management:

| Product | Scans | Chapter |
|:---|:---|:---|
| **Snyk Open Source** | Open-source dependencies (SCA) | [03](03-snyk-open-source-sca.md) |
| **Snyk Code** | Your first-party code (SAST, DeepCode AI) | [04](04-snyk-code-sast.md) |
| **Snyk Container** | Container images | [05](05-snyk-container-and-kubernetes.md) |
| **Snyk IaC** | Terraform / CloudFormation / K8s manifests | [06](06-snyk-infrastructure-as-code.md) |
| **ASPM** | Posture across the whole SDLC | [08](08-prioritization-governance-and-aspm.md) |

Together they cover the whole application supply chain — **your code, their code, the container, the infrastructure** — which is the developer's actual attack surface.

## Hands-On Lab

The labs in this volume model application-security concepts in Python at no cost. Snyk Learn is **free**, and Snyk offers a **free tier** of the product — so unlike most volumes, the *real* certification path here (completing Snyk Learn paths) costs nothing to walk.

### Lab 1.1 — Read the program for what it is

**Objective:** Place Snyk Learn as a certificate-of-completion program with two axes.

```bash
python3 - <<'EOF'
CONTENT = [
  # item,                              type,               format,          credential
  ("Security for Developers",          "security education","learning path", "Certificate of Completion"),
  ("OWASP Top 10",                     "security education","learning path", "Certificate of Completion"),
  ("OWASP Top 10 for LLM & GenAI",     "security education","learning path", "Certificate of Completion"),
  ("Secure AI Development",            "security education","learning path", "Certificate of Completion"),
  ("Implementing Snyk (Admin/Arch)",   "product training",  "learning path", "Certificate of Completion"),
  ("(a single XSS lesson)",            "security education","lesson",        "progress only"),
]
print(f"{'item':34}{'type':20}{'format':16}credential")
for item, typ, fmt, cred in CONTENT:
    print(f"{item:34}{typ:20}{fmt:16}{cred}")
print("\nWhat KIND of program this is (stated plainly):")
print("  - it's a CERTIFICATE-OF-COMPLETION program, NOT proctored exams. You finish a")
print("    LEARNING PATH and download a certificate. A learning credential, not an")
print("    examination credential — free, interactive, and current.")
print("  - TWO axes: TYPE (security education vs product training) x FORMAT (learning")
print("    path vs single lesson). Certificates attach to PATHS.")
print("  - ~18 paths, ~174 lessons; ~128 security-education vs ~64 product-training items.")
print("\nDon't inflate it into a proctored cert, don't dismiss it. Free, hands-on")
print("developer-security education with a completion certificate is genuinely useful —")
print("this volume treats it as exactly that. (Same honest framing as Grafana's free")
print("badges, Vol CXXXIX.)")
EOF
```

**Expected result:** Snyk Learn placed as a certificate-of-completion program across two axes (education versus product training, path versus lesson), with certificates attaching to completed learning paths. The stated-plainly lesson is the honest framing — this is a free, interactive *learning* credential, not a proctored exam, and it is treated as exactly that, neither inflated nor dismissed.

**Negative test:** Describing Snyk Learn as a proctored certification like AWS's or Wiz's. It is not — it awards certificates of completion for finishing learning paths; conflating the two misrepresents the program.

**Cleanup:** None.

### Lab 1.2 — Map the platform to the application supply chain

**Objective:** See how the four engines cover the developer's attack surface.

```bash
python3 - <<'EOF'
SUPPLY_CHAIN = [
  # stage,                    snyk product,        what it catches
  ("your first-party code",   "Snyk Code (SAST)",  "injection, XSS, insecure patterns you wrote"),
  ("open-source dependencies","Snyk Open Source",  "known CVEs in libs you pulled in (SCA)"),
  ("the container image",     "Snyk Container",    "OS/package vulns in the image you ship"),
  ("infrastructure-as-code",  "Snyk IaC",          "misconfig in Terraform/K8s before deploy"),
  ("posture across the SDLC", "ASPM",              "which apps are risky, coverage gaps"),
]
print("The application supply chain = the developer's real attack surface:\n")
print(f"   {'stage':28}{'Snyk product':22}catches")
for stage, prod, catches in SUPPLY_CHAIN:
    print(f"   {stage:28}{prod:22}{catches}")
print("\nThe insight: a modern app is NOT just the code you wrote. It's YOUR code +")
print("THEIR code (open-source deps, often 80%+ of the app) + the CONTAINER it runs in")
print("+ the INFRASTRUCTURE that deploys it. Each layer has its own risk, and an")
print("attacker takes the easiest one.")
print("\nSnyk covers all four with a dedicated engine, plus ASPM to see posture ACROSS")
print("them. That's the 'developer security platform' scope: not one scanner, but the")
print("whole supply chain a developer is responsible for — code to container to cloud")
print("config. Snyk Learn's product training teaches each engine; the security")
print("education teaches the vulnerability CLASSES (OWASP) underneath them.")
EOF
```

**Expected result:** The four Snyk engines mapped to the four layers of the application supply chain — first-party code, dependencies, container, and IaC — plus ASPM for cross-cutting posture. The supply-chain lesson is that a modern app is your code plus their code plus the container plus the infrastructure, each a distinct attack surface, and Snyk's scope is covering all of them rather than one scanner.

**Negative test:** Equating "application security" with scanning only your own source code. Open-source dependencies are often the majority of an app and a prime attack surface; covering only first-party code leaves the largest layer unscanned.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Snyk Learn understood as a free certificate-of-completion program (learning paths and lessons), stated plainly — not proctored exams.
- [ ] The two axes (security education vs product training, learning path vs lesson) understood, with certificates attaching to paths.
- [ ] The four scanning engines (Open Source, Code, Container, IaC) plus ASPM mapped to the application supply chain.
- [ ] Snyk positioned as the developer-first application-security platform, complementary to Wiz's cloud focus.
