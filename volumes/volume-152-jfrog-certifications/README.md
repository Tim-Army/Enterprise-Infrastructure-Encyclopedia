# Volume CLII — JFrog Certification Tracks

> The JFrog certification program — verified 5 August 2026 on `academy.jfrog.com` and `jfrog.com/certification`.
> Delivered through **JFrog Academy** (free and paid courses, learning paths, instructor-led training), the
> program has two tiers: **three Associate certifications** (Associate JFrog **Artifactory**, Associate JFrog
> DevOps **HA/DR**, Associate JFrog **Security**), each valid **two years**, and the flagship **JFrog Artifactory
> Certified DevOps Engineer** — a web-based, **proctored** exam of **47** multiple-choice and multiple-answer
> questions in **90 minutes**, **70% to pass**, valid **two years**, validating binary repository management,
> security, and CI/CD pipelines. JFrog **publishes** these mechanics — a welcome contrast to portal-gated
> vendors. Every lab runs free in Python; JFrog offers a free tier and free JFrog Academy courses.

## Overview

JFrog is the leader in **binary and software-supply-chain management** — the **JFrog Platform**, centered on
**Artifactory**, is the **universal repository** where all of an organization's *binaries* (build artifacts,
packages, container images, dependencies) live and flow from development to production. Where
[GitLab (CXXXVI)](../volume-136-gitlab-certifications/README.md) and [GitHub (LXXXIX)](../volume-089-github-certifications/README.md)
manage the *source code*, **JFrog manages the *binaries*** the code becomes — positioning the platform as the
**Software Supply Chain Platform**.

Chapter 02 covers **Artifactory** — the universal binary repository. Chapter 03 covers **repository types** —
local, remote (caching), and virtual (aggregating). Chapter 04 covers **build info, promotion, and
immutability** — build once, promote many. Chapter 05 covers **Xray** — deep recursive scanning and impact
analysis. Chapter 06 covers **software supply chain security** — Curation, SBOMs, and provenance. Chapter 07
covers **high availability and disaster recovery**. Chapter 08 covers **the DevOps pipeline and Distribution**.
Chapter 09 closes on choosing a path.

A theme runs through it: **everything flows through the hub** — because every binary passes through Artifactory,
it becomes the point where security, reproducibility, and traceability are enforced.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The JFrog Certification Program](chapters/01-the-jfrog-certification-program.md) | 1.1–1.2 |
| 02 | [Artifactory — The Universal Binary Repository](chapters/02-artifactory-the-universal-binary-repository.md) | 2.1 |
| 03 | [Repository Types and the Binary Flow](chapters/03-repository-types-and-the-binary-flow.md) | 3.1–3.2 |
| 04 | [Build Info, Promotion, and Immutability](chapters/04-build-info-promotion-and-immutability.md) | 4.1 |
| 05 | [Xray — Security and License Compliance](chapters/05-xray-security-and-license-compliance.md) | 5.1–5.2 |
| 06 | [Software Supply Chain Security](chapters/06-software-supply-chain-security.md) | 6.1 |
| 07 | [High Availability and Disaster Recovery](chapters/07-high-availability-and-disaster-recovery.md) | 7.1 |
| 08 | [The DevOps Pipeline and Distribution](chapters/08-the-devops-pipeline-and-distribution.md) | 8.1 |
| 09 | [Choosing Your JFrog Path](chapters/09-choosing-your-jfrog-path.md) | 9.1–9.2 |

## The certifications

| Certification | Tier | Domain |
| --- | --- | --- |
| **Associate JFrog Artifactory** | Associate | Artifact management, deployment |
| **Associate JFrog DevOps HA/DR** | Associate | High availability, DR, federation |
| **Associate JFrog Security** | Associate | Application / supply-chain security |
| **JFrog Artifactory Certified DevOps Engineer** | Professional | Repos + security + CI/CD (47Q / 90min / 70%) |

## What you will be able to do

- Read the certification program and sequence Associate certs toward the DevOps Engineer credential.
- Explain Artifactory as the universal binary repository and single source of truth.
- Design a repository topology — local, remote (caching), and virtual (aggregating).
- Apply build-once-promote-many with build info and immutability for reproducible releases.
- Scan deeply with Xray and run impact analysis when a new CVE lands.
- Secure the supply chain with Curation, SBOMs, and provenance.
- Design HA clustering and DR replication so the binary hub never halts the pipeline.
- Wire the platform into an end-to-end CI/CD flow with Distribution to the edge.

## Prerequisites

- Familiarity with CI/CD, package managers, and containers helps.
- A Linux or macOS host with `python3`. JFrog offers a **free tier** and free **JFrog Academy** courses.

## See also

- [Volume CXXXVI — GitLab](../volume-136-gitlab-certifications/README.md), [Volume LXXXIX — GitHub](../volume-089-github-certifications/README.md) — the source-and-CI side JFrog's binary side completes.
- [Volume CXLVIII — Snyk](../volume-148-snyk-certifications/README.md) — developer-side SCA; Xray is the binary-hub-side complement.
- [Volume XLI — CNCF Kubernetes](../volume-041-cncf-kubernetes-certifications/README.md) — the container platform JFrog stores images for and deploys to.
- [Volume XLII — HashiCorp](../volume-042-hashicorp-certifications/README.md) — the IaC/automation that provisions the pipeline JFrog anchors.
