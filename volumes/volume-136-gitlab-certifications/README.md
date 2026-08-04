# Volume CXXXVI — GitLab Certification Tracks

> The certification map for **GitLab**, the single-application DevSecOps platform — verified on GitLab
> University and its official **Candidate Handbook & Exam Guide**, 4 August 2026. Five **Associate**
> certifications: **Certified Fundamentals Associate** (GitLab's recommended starting point),
> **Certified CI/CD Associate**, **Certified Agile Portfolio Management Associate**, **Certified Security
> Associate**, and the new **Certified GitLab Duo Agent Platform Associate** covering agentic chat,
> custom agents and flows, and connecting external tools via **MCP**. Each Associate exam is **75
> minutes, 50 questions, unproctored online, $150**, needs **75%** to pass, and allows **two attempts
> inside a 14-day access window** that starts at purchase. The handbook also defines a **Professional**
> tier (90 minutes, 60 questions, proctored via Certiverse). Distinctively, **GitLab certifications do
> not expire** — they are governed by **product versioning** rather than a clock, so you track major
> releases instead of a renewal date. Free, self-paced learning paths back every exam. The volume models
> the concepts free in Python: pipeline DAG scheduling, `rules` evaluation, artifact-versus-cache
> classification, scanner triage, approval-policy gates, agent tool permissions, and runner sizing. No
> GitLab account required.

## Overview

Volume CXXXVI is a **certification-tracks volume** organized by the five exams' subject matter. Chapter
02 covers the group/project hierarchy, role inheritance, protected branches, and merge requests; Chapter
03 the Agile Portfolio Management material (scoped labels, boards, dependencies, honest velocity);
Chapters 04–05 the CI/CD pair, from `.gitlab-ci.yml` fundamentals through `rules` evaluation, `needs`
DAGs, and protected environments; Chapter 06 the security scanners and the policy gates that enforce
them; Chapter 07 the new **GitLab Duo Agent Platform** certification, including MCP tool connection under
least privilege; and Chapter 08 runners, executors, capacity, and cache strategy. Chapter 09 closes on
exam selection and GitLab's version-based currency model.

Its place on the encyclopedia's platform shelf is the **integrated** counterpart to
[GitHub LXXXIX](../volume-089-github-certifications/README.md), alongside
[Docker XCII](../volume-092-docker-certifications/README.md),
[CNCF/Kubernetes XLI](../volume-041-cncf-kubernetes-certifications/README.md), and
[HashiCorp XLII](../volume-042-hashicorp-certifications/README.md).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The GitLab Program and the DevSecOps Platform](chapters/01-the-gitlab-program-and-devsecops.md) | 1.1–1.2 |
| 02 | [Git, Groups, Projects, and Merge Requests](chapters/02-git-groups-projects-and-merge-requests.md) | 2.1–2.3 |
| 03 | [Agile Portfolio Management](chapters/03-agile-portfolio-management.md) | 3.1–3.3 |
| 04 | [CI/CD Fundamentals](chapters/04-ci-cd-fundamentals.md) | 4.1–4.3 |
| 05 | [Advanced CI/CD — Rules, DAGs, and Environments](chapters/05-advanced-ci-cd.md) | 5.1–5.3 |
| 06 | [Security Scanning and Compliance](chapters/06-security-scanning-and-compliance.md) | 6.1–6.3 |
| 07 | [GitLab Duo and the Agent Platform](chapters/07-gitlab-duo-and-the-agent-platform.md) | 7.1–7.3 |
| 08 | [Runners, Scaling, and Administration](chapters/08-runners-scaling-and-administration.md) | 8.1–8.3 |
| 09 | [Choosing a Certification, Currency, and Career](chapters/09-choosing-a-certification-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the five Associate certifications and sequence them from Fundamentals outward.
- Reason about group role inheritance and protect branches so review is enforced rather than encouraged.
- Plan with scoped labels, epics, and dependency-aware critical paths, and forecast velocity honestly.
- Write pipelines that exploit parallelism, and tune the job that actually determines duration.
- Evaluate `rules` first-match-wins, build `needs` DAGs, and gate environments behind human approval.
- Configure the scanner set, remediate secrets rotate-first, and enforce policy above the project's CI file.
- Operate AI agents under least privilege, with identical review and scanning for AI-authored code.
- Size runners against queue time and key caches so they actually hit.

## Prerequisites

- Git fundamentals and general software-delivery familiarity; [Volume VIII](../volume-008-containers-platform-engineering/README.md) and [Volume IX](../volume-009-infrastructure-automation/README.md) for platform context.
- A Linux or macOS host with `python3` and `git` — every lab runs on the standard library. GitLab.com's free tier and self-managed Community Edition are both free if you want a live instance.

## See also

- [Volume LXXXIX — GitHub](../volume-089-github-certifications/README.md) — the counterpart platform; concepts transfer, vocabulary does not.
- [Volume XCII — Docker](../volume-092-docker-certifications/README.md), [Volume XLI — CNCF and Kubernetes](../volume-041-cncf-kubernetes-certifications/README.md), [Volume XLII — HashiCorp](../volume-042-hashicorp-certifications/README.md) — what pipelines build, deploy to, and drive.
- [Volume VIII — Containers and Platform Engineering](../volume-008-containers-platform-engineering/README.md), [Volume IX — Infrastructure Automation](../volume-009-infrastructure-automation/README.md) — the vendor-neutral disciplines.
- [Master Appendices — GitLab appendix](../volume-997-master-appendices/chapters/70-appendix-gitlab-certifications-and-course-access.md) — certifications, learning paths, and access.
