# Volume CXLVIII — Snyk Certification Tracks

> The Snyk education and credentialing program — verified 5 August 2026 on `learn.snyk.io` and `snyk.io`. Snyk's
> program is **Snyk Learn**: free, interactive developer-security education and product training. It is important
> to state plainly what kind of program this is — **a certificate-of-completion program, not a proctored-exam
> certification.** You complete **learning paths** (sequences of interactive lessons) and earn a downloadable
> **Certificate of Completion** (a free account tracks progress). Snyk Learn has two axes — **type** (~128
> security-education vs ~64 product-training items) and **format** (~18 learning paths, ~174 lessons) — and a
> separate **Snyk AI Security University Program**. This is a genuine, valuable, free credential; the volume
> treats it as exactly that, neither inflating it into a proctored cert nor dismissing it (the same honest
> framing as the [Grafana free badges (CXXXIX)](../volume-139-grafana-observability/README.md)). Every lab runs
> free in Python, and Snyk offers a free product tier — so the real certification path here costs nothing.

## Overview

Snyk is a **developer security platform** — "visibility, context, and control to work alongside developers on
reducing application risk." Where the [Wiz volume (CXLVII)](../volume-147-wiz-certifications/README.md) secures
the *cloud*, Snyk secures the *application*: the code developers write, the open-source dependencies they pull
in, the containers they package, and the infrastructure-as-code they deploy. Its stance is **developer-first** —
security delivered to developers in their workflow (IDE, CLI, PR, CI/CD), to **find and fix** as they build.

Chapter 02 covers **developer-first application security** — the philosophy, and why adoption beats
exhaustiveness. Chapter 03 covers **Snyk Open Source** (SCA) — transitive dependencies and fix-by-upgrade.
Chapter 04 covers **Snyk Code** (SAST) — data-flow analysis, DeepCode AI, and the false-positive problem.
Chapter 05 covers **Snyk Container** — the base-image multiplier. Chapter 06 covers **Snyk IaC** — fixing the
blueprint and policy-as-code. Chapter 07 covers **AI and secure development** — securing AI-generated code and
the OWASP Top 10 for LLM/GenAI/agentic apps. Chapter 08 covers **prioritization, governance, and ASPM**.
Chapter 09 closes on choosing a path.

A theme runs through it: **the metric is fixed, not found** — security that developers actually use and act on,
across the whole application supply chain, beats exhaustive scanning that is ignored.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Snyk Learn Program](chapters/01-the-snyk-learn-program.md) | 1.1–1.2 |
| 02 | [Developer-First Application Security](chapters/02-developer-first-application-security.md) | 2.1–2.2 |
| 03 | [Snyk Open Source — SCA](chapters/03-snyk-open-source-sca.md) | 3.1–3.2 |
| 04 | [Snyk Code — SAST](chapters/04-snyk-code-sast.md) | 4.1–4.2 |
| 05 | [Snyk Container and Kubernetes](chapters/05-snyk-container-and-kubernetes.md) | 5.1 |
| 06 | [Snyk Infrastructure as Code](chapters/06-snyk-infrastructure-as-code.md) | 6.1 |
| 07 | [AI and Secure Development](chapters/07-ai-and-secure-development.md) | 7.1–7.2 |
| 08 | [Prioritization, Governance, and ASPM](chapters/08-prioritization-governance-and-aspm.md) | 8.1–8.2 |
| 09 | [Choosing Your Snyk Path](chapters/09-choosing-your-snyk-path.md) | 9.1–9.2 |

## The program

| Element | Is |
| --- | --- |
| **Snyk Learn** | Free, self-paced security education + product training |
| **Learning path** | A sequence of lessons → a **Certificate of Completion** |
| **Snyk AI Security University Program** | Structured AI-security education |
| **Credential type** | Certificate of completion (**not** proctored exams) |

## The platform (four engines + ASPM)

| Product | Scans |
| --- | --- |
| **Snyk Open Source** | Open-source dependencies (SCA) |
| **Snyk Code** | First-party code (SAST, DeepCode AI) |
| **Snyk Container** | Container images |
| **Snyk IaC** | Terraform / CloudFormation / K8s manifests |
| **ASPM** | Posture across the whole SDLC |

## What you will be able to do

- Read Snyk Learn for what it is — a free certificate-of-completion program across two axes.
- Explain developer-first security and why adoption and fix-rate beat raw detection.
- Find and fix transitive open-source vulnerabilities by minimal upgrade (SCA).
- Read SAST as source-to-sink data flow, and know why false positives are a security failure.
- Apply the base-image multiplier for containers and fix IaC at the blueprint with policy-as-code.
- Secure AI-generated code and AI applications (OWASP for LLM/GenAI, agentic least-privilege).
- Prioritize by reachability and exploit maturity, and set CI/CD gates developers keep on.

## Prerequisites

- Basic programming and familiarity with a package manager (npm, pip, Maven) helps.
- A Linux or macOS host with `python3`. **Snyk Learn is free** and Snyk has a **free product tier** — the real certification path costs nothing.

## See also

- [Volume CXLVII — Wiz](../volume-147-wiz-certifications/README.md) — the cloud-security side; together with Snyk's application side they cover code-to-cloud.
- [Volume CXXXVI — GitLab](../volume-136-gitlab-certifications/README.md), [Volume LXXXIX — GitHub](../volume-089-github-certifications/README.md) — the CI/CD pipeline Snyk gates plug into.
- [Volume XLI — CNCF Kubernetes](../volume-041-cncf-kubernetes-certifications/README.md) — the container/IaC runtime Snyk scans for.
- [Volume XLIII — OffSec](../volume-043-offensive-security-certifications/README.md) — the offensive counterpart to Snyk's find-and-fix defense.
