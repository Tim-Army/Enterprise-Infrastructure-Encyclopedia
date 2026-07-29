# Volume XLI — CNCF and Kubernetes Certification Tracks

> The whole CNCF and Linux Foundation cloud-native certification program in one
> volume — the Kubernetes core (CKA, CKAD, CKS), the cloud-native associates
> (KCNA, KCSA, PCA, OTCA, ICA, CCA, CAPA, CGOA, CBA, KCA), and the new
> platform-engineering track (CNPA, CNPE) — with a walkthrough lab for every
> weighted exam domain, verified against the official Linux Foundation curricula.

## Overview

Volume XLI maps the **Cloud Native Computing Foundation (CNCF)** and **Linux
Foundation** certification program — the **performance-based**, hands-on
credentials for Kubernetes and the cloud-native ecosystem. What distinguishes
these exams is that the flagships (CKA, CKAD, CKS, ICA, CNPE) are solved in a
**live terminal** against real clusters, which is why this volume sits alongside
the encyclopedia's hands-on platform volumes — Containers and Platform
Engineering (VIII) and Infrastructure Automation (IX) — rather than the
knowledge tier.

This is a **certification-tracks** volume, like CompTIA (XXXIX), ISC2 (XL),
Microsoft (XXXVIII), Azure (XXXIII), and Google Cloud (XXXIV): its job is to map
the program — which credentials exist, their **weighted curriculum domains**,
exam mechanics, prerequisites, and the pinned Kubernetes version — and to teach
each domain with a hands-on walkthrough. Every domain and weight was **verified
against the official Linux Foundation certification curricula on 26 July 2026**,
which matters because the program is version-pinned and expanding fast: the
Kubernetes core exams track **Kubernetes v1.35**, and the **Kyverno (KCA)** and
**platform-engineering (CNPA, CNPE)** credentials are recent additions — CNPE
launched in November 2025.

Chapters are organized by role and project family:

- **Chapter 01** frames the whole program — the three lines, performance-based
  vs multiple-choice, PSI proctoring, killer.sh, version pinning, and standing up
  a practice cluster.
- **Chapters 02–04** take the Kubernetes core: KCNA (entry), CKA, and CKAD.
- **Chapter 05** covers Kubernetes security: CKS and KCSA.
- **Chapters 06–08** cover the project associates: observability (PCA, OTCA);
  networking and service mesh (ICA, CCA); and delivery and policy (CAPA, CGOA,
  CBA, KCA).
- **Chapter 09** covers the platform-engineering track (CNPA, CNPE) and keeping
  the program current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-domain
hands-on labs and knowledge checks.

## Chapters

1. [The CNCF and Kubernetes Certification Program](chapters/01-the-cncf-and-kubernetes-certification-program.md) — the three lines, performance-based vs multiple-choice, PSI proctoring, killer.sh, version-pinned curricula, and a practice cluster.
2. [Kubernetes and Cloud Native Associate (KCNA)](chapters/02-kubernetes-and-cloud-native-associate-kcna.md) — the multiple-choice entry credential; four domains.
3. [Certified Kubernetes Administrator (CKA)](chapters/03-certified-kubernetes-administrator-cka.md) — the flagship performance-based operations credential; five domains, troubleshooting-heavy.
4. [Certified Kubernetes Application Developer (CKAD)](chapters/04-certified-kubernetes-application-developer-ckad.md) — the performance-based developer credential; five domains.
5. [Kubernetes Security — CKS and KCSA](chapters/05-kubernetes-security-cks-and-kcsa.md) — the performance-based CKS (requires CKA) and the multiple-choice KCSA.
6. [Observability Associates — PCA and OTCA](chapters/06-observability-associates-pca-and-otca.md) — Prometheus (PromQL-heavy) and OpenTelemetry (SDK-heavy).
7. [Networking and Service Mesh — ICA and CCA](chapters/07-networking-and-service-mesh-ica-and-cca.md) — Istio (performance-based) and Cilium (eBPF).
8. [Delivery and Policy Associates — CAPA, CGOA, CBA, KCA](chapters/08-delivery-and-policy-associates-capa-cgoa-cba-kca.md) — Argo, GitOps, Backstage, and Kyverno.
9. [Platform Engineering (CNPA, CNPE) and Keeping Current](chapters/09-platform-engineering-cnpa-cnpe-and-keeping-current.md) — the new platform-engineering track, IDPs and golden paths, and program currency.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for CNCF/Kubernetes, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with the credential lines, exam mechanics, the Linux Foundation training and
killer.sh model, and the pinned Kubernetes version is in the
[CNCF/Kubernetes certification appendix](../volume-997-master-appendices/chapters/15-appendix-cncf-kubernetes-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Deeper hands-on Kubernetes practice lives in
Volume VIII (Containers and Platform Engineering) and the automation volume (IX).

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for
every weighted curriculum domain of every credential** — **77 domain labs** in
all — plus the program and currency labs in Chapters 01 and 09. The weight for
each domain comes from that credential's official Linux Foundation curriculum:
KCNA (4), CKA (5), CKAD (5), CKS (6) and KCSA (6), PCA (5) and OTCA (4), ICA (4)
and CCA (8), CAPA (4), CGOA (5), CBA (4) and KCA (6), and CNPA (6) and CNPE (5).
Because these are hands-on cloud-native credentials, the walkthroughs use the
real tooling — **`kubectl`** against a local `kind`/`minikube` cluster, plus
`istioctl`, the Cilium CLI, Argo/Kyverno CRDs, PromQL, and OpenTelemetry
Collector configuration — as concrete demonstrations of each domain. Each lab
states an objective, commands, expected results, a negative test, and cleanup,
and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references the **Linux Foundation** certification site
(`training.linuxfoundation.org`), the **cncf/curriculum** GitHub repository, the
**PSI** exam-delivery platform, and the **killer.sh** simulator. It practices
against **Kubernetes v1.35** (the current pinned version) via `kind` or
`minikube`. Domains, weights, and mechanics were verified against the Linux
Foundation on 26 July 2026; the curricula are version-pinned and updated, so
confirm the current curriculum and Kubernetes version before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-041-cncf-kubernetes-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
