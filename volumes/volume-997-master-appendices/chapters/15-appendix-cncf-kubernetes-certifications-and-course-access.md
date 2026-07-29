# Chapter 15: Appendix — CNCF and Kubernetes Certifications and Course Access

The **Cloud Native Computing Foundation (CNCF)** and **Linux Foundation**
certification program — the performance-based and multiple-choice cloud-native
credentials — organized by line, with each credential's weighted curriculum
domains, exam format, and the training and simulator model. The lineup, domains,
and weights were harvested on **26 July 2026** from **training.linuxfoundation.org**
and the **cncf/curriculum** GitHub repository — the same sources that anchor
[Volume XLI — CNCF and Kubernetes Certification Tracks](../../volume-41-cncf-kubernetes-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works at the Linux Foundation.** Official training is delivered as
**Linux Foundation e-learning** (self-paced courses such as LFS258/LFD259/LFS260
and the project-specific courses), often **bundled with the exam** and, for the
Kubernetes core exams, with **two exam attempts** and **killer.sh** simulator
sessions. The **curricula are free and open** on GitHub (cncf/curriculum) and
name the exact **Kubernetes version**. Exams are **remote-proctored through
PSI**. Credentials appear as verifiable digital badges.

> **Currency.** The curricula are **version-pinned** (the Kubernetes core exams
> currently target **Kubernetes v1.35**) and the program **adds credentials
> regularly** — the **Kyverno (KCA)** associate and the **platform-engineering**
> track (**CNPA** associate and the performance-based **CNPE**, launched November
> 2025) are recent additions. Confirm the current curriculum, format, and pinned
> version on the Linux Foundation certification page before registering.

## Free training and entry points

- **[Linux Foundation certification catalog](https://training.linuxfoundation.org/certification/)** —
  the authoritative per-credential pages with curricula, format, and pricing
- **[cncf/curriculum on GitHub](https://github.com/cncf/curriculum)** — the free,
  open, version-pinned Kubernetes core curricula
- **killer.sh** — the exam simulator bundled with CKA/CKAD/CKS (two sessions)
- **Linux Foundation e-learning** — self-paced courses (LFS258 for CKA, LFD259
  for CKAD, LFS260 for CKS, plus project courses) often bundled with the exam
- **CNCF landscape and project docs** (kubernetes.io, prometheus.io,
  opentelemetry.io, istio.io, cilium.io, argoproj.github.io, backstage.io,
  kyverno.io) — free reference for each associate

## Fees, delivery, and renewal

- **Fee band (US pricing; bundles vary — confirm at registration):** the
  **associate** exams (KCNA, KCSA, PCA, OTCA, CCA, CAPA, CGOA, CBA, KCA, CNPA)
  are the lowest band; the **Kubernetes core** exams (CKA, CKAD, CKS) and **ICA**
  are the mid band and include killer.sh; the performance-based **CNPE** is the
  highest. Bundles (course + exam) are common.
- **Delivery:** **PSI remote-proctored**. **Performance-based** (live terminal):
  **CKA, CKAD, CKS, ICA, CNPE**. **Multiple-choice**: the remaining associates.
  Durations are typically **90 minutes** (associates) or **2 hours** (core/ICA/
  CNPE). Passing scores are published per exam (e.g., CKA/CKAD **66%**, CKS
  **67%**).
- **Prerequisites:** only **CKS requires an active CKA**; all others have none.
- **Version pinning:** the Kubernetes core curricula name the exact version
  (currently **v1.35**); practice against it.
- **Validity and renewal:** credentials carry a defined validity (commonly **two
  years** for the hands-on exams) and are renewed by retaking the current exam —
  confirm each credential's validity and renewal terms on its page.

## The credential map

Domains and weights verified against the Linux Foundation curricula on 26 July
2026.

| Credential | Line | Format | Domains |
| --- | --- | --- | --- |
| KCNA — Kubernetes and Cloud Native Associate | Kubernetes core (entry) | Multiple-choice | 4 |
| CKA — Certified Kubernetes Administrator | Kubernetes core | Performance-based | 5 |
| CKAD — Certified Kubernetes Application Developer | Kubernetes core | Performance-based | 5 |
| CKS — Certified Kubernetes Security Specialist | Kubernetes core (requires CKA) | Performance-based | 6 |
| KCSA — Kubernetes and Cloud Native Security Associate | Security | Multiple-choice | 6 |
| PCA — Prometheus Certified Associate | Observability | Multiple-choice | 5 |
| OTCA — OpenTelemetry Certified Associate | Observability | Multiple-choice | 4 |
| ICA — Istio Certified Associate | Networking / mesh | Performance-based | 4 |
| CCA — Cilium Certified Associate | Networking / eBPF | Multiple-choice | 8 |
| CAPA — Certified Argo Project Associate | Delivery | Multiple-choice | 4 |
| CGOA — Certified GitOps Associate | Delivery | Multiple-choice | 5 |
| CBA — Certified Backstage Associate | Developer portal | Multiple-choice | 4 |
| KCA — Kyverno Certified Associate | Policy | Multiple-choice | 6 |
| CNPA — Cloud Native Platform Engineering Associate | Platform engineering | Multiple-choice | 6 |
| CNPE — Certified Cloud Native Platform Engineer | Platform engineering | Performance-based | 5 |

## Weighted curriculum domains

- **KCNA:** Kubernetes Fundamentals 44% · Container Orchestration 28% · Cloud
  Native Application Delivery 16% · Cloud Native Architecture 12%.
- **CKA:** Cluster Architecture, Installation & Configuration 25% · Workloads &
  Scheduling 15% · Storage 10% · Services & Networking 20% · Troubleshooting 30%.
- **CKAD:** Application Design and Build 20% · Application Deployment 20% ·
  Observability and Maintenance 15% · Environment, Configuration and Security
  25% · Services and Networking 20%.
- **CKS:** Cluster Setup 15% · Cluster Hardening 15% · System Hardening 10% ·
  Minimize Microservice Vulnerabilities 20% · Supply Chain Security 20% ·
  Monitoring, Logging and Runtime Security 20%.
- **KCSA:** Overview of Cloud Native Security 14% · Cluster Component Security
  22% · Security Fundamentals 22% · Threat Model 16% · Platform Security 16% ·
  Compliance and Security Frameworks 10%.
- **PCA:** Observability Concepts 18% · Prometheus Fundamentals 20% · PromQL
  28% · Instrumentation and Exporters 16% · Alerting & Dashboarding 18%.
- **OTCA:** Fundamentals of Observability 18% · The OpenTelemetry API and SDK
  46% · The OpenTelemetry Collector 26% · Maintaining and Debugging Pipelines
  10%.
- **ICA:** Installation, Upgrade & Configuration 20% · Traffic Management 35% ·
  Securing Workloads 25% · Troubleshooting 20%.
- **CCA:** Architecture 20% · Network Policy 18% · Service Mesh 16% · Network
  Observability 10% · Installation and Configuration 10% · Cluster Mesh 10% ·
  eBPF 10% · BGP and External Networking 6%.
- **CAPA:** Argo Workflows 36% · Argo CD 34% · Argo Rollouts 18% · Argo Events
  12%.
- **CGOA:** GitOps Terminology 20% · GitOps Principles 30% · Related Practices
  16% · GitOps Patterns 20% · Tooling 14%.
- **CBA:** Backstage Development Workflow 24% · Backstage Infrastructure 22% ·
  Backstage Catalog 22% · Customizing Backstage 32%.
- **KCA:** Fundamentals of Kyverno 18% · Installation, Configuration, and
  Upgrades 18% · Kyverno CLI 12% · Applying Policies 10% · Writing Policies
  32% · Policy Management 10%.
- **CNPA:** Platform Engineering Core Fundamentals 36% · Platform Observability,
  Security, and Conformance 20% · Continuous Delivery & Platform Engineering
  16% · Platform APIs and Provisioning Infrastructure 12% · IDPs and Developer
  Experience 8% · Measuring your Platform 8%.
- **CNPE:** Platform Architecture and Infrastructure 15% · GitOps and Continuous
  Delivery 25% · Platform APIs and Self-Service Capabilities 25% · Observability
  and Operations 20% · Security and Policy Enforcement 15%.

## Notes

- **Performance-based means practice on a cluster.** CKA, CKAD, CKS, ICA, and
  CNPE are solved in a live terminal — prepare with `kind`/`minikube` and
  **killer.sh**, not reading alone.
- **CKS requires an active CKA;** no other credential has a prerequisite.
- **Curricula are version-pinned and open.** Study against the exact Kubernetes
  version (currently **v1.35**) named in the cncf/curriculum repo.
- **The program grows.** KCA, CNPA, and CNPE are recent — check
  training.linuxfoundation.org for new project associates.
- **Hands-on practice** for these skills lives in **Volume VIII (Containers and
  Platform Engineering)** and **Volume IX (Infrastructure Automation)**, with
  observability foundations in **Volume XI**.
