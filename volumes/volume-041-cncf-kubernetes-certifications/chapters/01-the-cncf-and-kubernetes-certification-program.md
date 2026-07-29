# Chapter 01: The CNCF and Kubernetes Certification Program

## Learning Objectives

- Explain what the CNCF and the Linux Foundation certify and why the program is performance-based.
- Describe the full credential map: the Kubernetes core, the cloud-native associates, and the new platform-engineering track.
- Distinguish performance-based exams (CKA/CKAD/CKS/ICA/CNPE) from the multiple-choice associates.
- Explain exam mechanics: PSI remote proctoring, the live terminal, killer.sh, and the passing scores.
- Verify a current curriculum and its Kubernetes version from the authoritative source.

## Theory and Architecture

The **Cloud Native Computing Foundation (CNCF)**, part of the **Linux
Foundation**, hosts Kubernetes and the cloud-native ecosystem (Prometheus,
Envoy, Istio, Argo, Cilium, OpenTelemetry, Backstage, and more) and publishes the
industry's **cloud-native certifications**. What sets them apart is that the
flagship exams are **performance-based**: the candidate solves real tasks in a
**live terminal** against real clusters, not a bank of multiple-choice
questions. That makes a CKA or CKS a demonstration of *ability*, which is why
these credentials sit alongside the hands-on volumes of this encyclopedia rather
than the knowledge tier.

The program has grown into **fifteen** credentials on three lines:

- **Kubernetes core (performance-based):** **CKA** (administrator), **CKAD**
  (application developer), and **CKS** (security specialist; requires an active
  CKA).
- **Cloud-native associates (mostly multiple-choice):** **KCNA** (the entry
  credential) and **KCSA** (security), plus project-focused associates —
  **PCA** (Prometheus), **OTCA** (OpenTelemetry), **ICA** (Istio,
  performance-based), **CCA** (Cilium), **CAPA** (Argo), **CGOA** (GitOps),
  **CBA** (Backstage), and **KCA** (Kyverno).
- **Platform engineering (new):** **CNPA** (Cloud Native Platform Engineering
  Associate) and the performance-based expert **CNPE** (Certified Cloud Native
  Platform Engineer, launched November 2025) — CNCF's response to the rise of
  platform engineering and internal developer platforms.

Exams are delivered **online, remote-proctored through PSI**. The Kubernetes core
exams and CKS bundle **two attempts** and **killer.sh** simulator sessions.
Passing scores are published per exam (CKA/CKAD **66%**, CKS **67%**); the
curricula are **open on GitHub** and pinned to a specific **Kubernetes version**
(currently v1.35 for the core exams), so they track the project closely.

## Design Considerations

Plan a cloud-native path by **role and depth**. Newcomers start at **KCNA** to
learn the vocabulary and the ecosystem, then choose a hands-on track: operators
take **CKA**, developers take **CKAD**, and security engineers take **CKA → CKS**
(the CKA is a hard prerequisite for CKS). From there, the **associates** validate
specific projects a platform actually runs — Prometheus/OpenTelemetry for
observability, Istio/Cilium for networking and mesh, Argo/GitOps/Backstage/Kyverno
for delivery and policy. The new **CNPA → CNPE** track is for engineers building
**internal developer platforms** on top of Kubernetes.

Because the exams are **performance-based and version-pinned**, prepare by
**doing** on a current cluster, not by reading. Budget time on **killer.sh**
(included with the core exams) and practice against the exact Kubernetes version
in the curriculum.

## Implementation and Automation

The curricula live in the open and name the exact Kubernetes version — confirm
before studying:

```bash
# The Kubernetes core curricula are published in a CNCF GitHub repo
curl -sSL "https://raw.githubusercontent.com/cncf/curriculum/master/README.md" \
  | grep -iE 'CKA|CKAD|CKS|v1\.[0-9]+' | head
```

A local cluster is all you need to practice every domain in this volume:

```bash
# kind (Kubernetes in Docker) spins up a throwaway cluster for lab work
kind create cluster --name lab
kubectl version --output=json | grep -E 'gitVersion' | head -2
```

## Validation and Troubleshooting

Confirm a credential's curriculum, format, and version on the Linux Foundation
certification page:

```text
training.linuxfoundation.org > Certifications > open the credential:
  - the weighted domains and competencies (the curriculum)
  - performance-based vs multiple-choice, duration, and passing score
  - the pinned Kubernetes/project version
  - prerequisites (CKS requires an active CKA)
```

Common pitfalls: practicing on an **old Kubernetes version** when the curriculum
has moved on; treating a **performance-based** exam like a reading test; missing
that **CKS requires an active CKA**; and confusing the many **associate** exams —
each targets a specific project (Prometheus vs OpenTelemetry, Istio vs Cilium,
Argo vs Kyverno).

## Security and Best Practices

Verify facts on **training.linuxfoundation.org** and the **cncf/curriculum**
GitHub repo, never a dump site (dumps violate the exam agreement). Practice with
official CNCF/LF training and **killer.sh**. Learn the **kubectl** muscle memory
the timed exams demand — imperative commands, `--dry-run=client -o yaml`, and
fast context/namespace switching. Renew on the LF schedule (associates and the
core exams carry defined validity — confirm each on its page).

## References and Knowledge Checks

- training.linuxfoundation.org: the certification catalog and per-credential curricula.
- github.com/cncf/curriculum: the open Kubernetes core curricula, version-pinned.

**Knowledge checks**

1. What makes the CKA/CKAD/CKS exams different from the associate exams?
2. Which credential is the hard prerequisite for CKS?
3. Where do the Kubernetes core curricula live, and why does the pinned version matter?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and preparing a cluster.

**Shared prerequisites for Labs 1.1–1.3** — a Linux shell with `curl`, `docker`
or `podman`, `kind` (or `minikube`), and `kubectl`. **Cost:** none.

### Lab 1.1 — Enumerate the certification catalog (Topic: Read the program)

**Objective:** List the current credentials and confirm the pinned version.

```bash
curl -sSL "https://raw.githubusercontent.com/cncf/curriculum/master/README.md" \
  | grep -oiE 'CK[AS]D?|v1\.[0-9]+' | sort -u | head
```

**Expected result:** the Kubernetes core exams (`CKA`, `CKAD`, `CKS`) and a
`v1.3x` version tag — the authoritative, version-pinned curriculum index.

**Negative test:** rely on a years-old course syllabus; it targets a retired
Kubernetes version and outdated `kubectl` behavior — use the live curriculum.

**Cleanup:** none.

### Lab 1.2 — Stand up a practice cluster (Topic: Prepare to practice)

**Objective:** Create the local cluster every lab in this volume uses.

```bash
kind create cluster --name lab 2>/dev/null || minikube start -p lab
kubectl get nodes -o wide
```

**Expected result:** at least one node in `Ready` state — a working cluster for
performance-based practice.

**Negative test:** try to study a performance-based exam with no cluster; there
is nothing to practice against — always have a live cluster.

**Cleanup:** keep the cluster for the rest of the volume, or `kind delete cluster --name lab`.

### Lab 1.3 — Build kubectl muscle memory (Topic: Exam technique)

**Objective:** Generate a manifest imperatively, the core exam-speed technique.

```bash
kubectl create deployment web --image=nginx --dry-run=client -o yaml | head -12
```

**Expected result:** a valid Deployment manifest printed without creating
anything — `--dry-run=client -o yaml` is the fastest way to scaffold objects in
a timed exam.

**Negative test:** hand-write every YAML from memory under time pressure;
generate a skeleton imperatively and edit it instead.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CNCF/Linux Foundation program certifies cloud-native skill through
**performance-based** exams: the Kubernetes core (CKA, CKAD, CKS), the
cloud-native associates (KCNA, KCSA, PCA, OTCA, ICA, CCA, CAPA, CGOA, CBA, KCA),
and the new platform-engineering track (CNPA, CNPE). Exams run remote-proctored
via PSI against version-pinned, open curricula, and reward doing over reading.

- [ ] I can map the fifteen credentials across the three lines.
- [ ] I can distinguish performance-based from multiple-choice exams.
- [ ] I can find the version-pinned curriculum and stand up a practice cluster.
- [ ] I know CKS requires an active CKA.
- [ ] I completed Labs 1.1–1.3 including each negative test.
