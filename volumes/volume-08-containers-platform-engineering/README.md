# Volume VIII — Containers and Platform Engineering

> Container fundamentals, Kubernetes architecture and operations, and the
> platform engineering practices — delivery, developer platforms,
> observability, and reliability — that turn a cluster into a product
> other teams can safely self-serve.

## Overview

Volume VIII takes an infrastructure engineer from a single container
process on one host to a fleet of Kubernetes clusters operated as a
platform product. It assumes the engineering and automation practices
established in [Volume I](../volume-01-enterprise-engineering-foundations/README.md)
and builds toward the automation, security, and observability disciplines
covered in depth across
[Volume IX](../volume-09-infrastructure-automation/README.md),
[Volume X](../volume-10-enterprise-cybersecurity/README.md), and
[Volume XI](../volume-11-observability-enterprise-operations/README.md) —
this volume applies those disciplines specifically to containers and
Kubernetes rather than restating them generically.

The volume is organized in three arcs:

- **Chapters 01–02** cover container fundamentals and Kubernetes
  architecture: the kernel primitives and OCI specifications behind every
  container runtime, and the control-plane/node component model,
  request pipeline, and cluster lifecycle operations (bootstrap, etcd
  backup/restore, upgrades) that every later chapter assumes.
- **Chapters 03–06** cover the four pillars of running workloads on
  Kubernetes in production: scheduling and capacity, networking and
  traffic policy, storage and stateful platforms, and identity,
  configuration, policy, and security.
- **Chapters 07–09** cover platform engineering itself: GitOps-based
  delivery and software supply chain security, building an Internal
  Developer Platform with CRDs, operators, and Crossplane, and the
  observability, reliability, and fleet lifecycle operations that keep
  the whole platform healthy and correctly sized over time.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md). Each hands-on lab
is a reproducible, disposable exercise (built primarily on local `kind`
clusters) with a stated objective, prerequisites, numbered steps,
expected results, a negative test, and cleanup instructions.

## Chapters

1. [Container Architecture, Images, Runtimes, and Registries](chapters/01-container-architecture-images-runtimes-and-registries.md) — namespaces, cgroups v2, and capabilities; the OCI Image/Runtime/Distribution specifications; CRI, containerd/CRI-O, and runc/gVisor/Kata; building, scanning, and cosign-signing images.
2. [Kubernetes Architecture and Cluster Lifecycle](chapters/02-kubernetes-architecture-and-cluster-lifecycle.md) — control plane and node components, the API request pipeline, CRDs and API aggregation, `kubeadm` bootstrap, etcd backup/restore, and the version skew upgrade policy.
3. [Kubernetes Workloads, Scheduling, and Capacity](chapters/03-kubernetes-workloads-scheduling-and-capacity.md) — Deployment/StatefulSet/DaemonSet/Job/CronJob selection, the scheduler's filter/score model, QoS classes, affinity/anti-affinity/topology spread, HPA and cluster autoscaling, and PodDisruptionBudgets.
4. [Kubernetes Networking, Service Delivery, and Traffic Policy](chapters/04-kubernetes-networking-service-delivery-and-traffic-policy.md) — the CNI networking model, Service types and EndpointSlices, kube-proxy modes and eBPF replacement, Ingress versus the Gateway API, NetworkPolicy segmentation, and service mesh trade-offs.
5. [Kubernetes Storage and Stateful Platforms](chapters/05-kubernetes-storage-and-stateful-platforms.md) — the Container Storage Interface, PV/PVC/StorageClass dynamic provisioning, access modes, StatefulSet per-ordinal storage, VolumeSnapshots, Velero backup, and running stateful data-service operators.
6. [Kubernetes Identity, Configuration, Policy, and Security](chapters/06-kubernetes-identity-configuration-policy-and-security.md) — RBAC design, bound ServiceAccount tokens, ConfigMaps/Secrets and external secrets management, Pod Security admission, Kyverno/Gatekeeper/`ValidatingAdmissionPolicy`, and workload identity federation.
7. [Cloud-Native Delivery, GitOps, and Software Supply Chains](chapters/07-cloud-native-delivery-gitops-and-software-supply-chains.md) — Helm and Kustomize, GitOps reconciliation with Argo CD and Flux, progressive delivery with Argo Rollouts/Flagger, and SLSA-aligned supply chain provenance and enforcement.
8. [Internal Developer Platforms and Platform Products](chapters/08-internal-developer-platforms-and-platform-products.md) — platform engineering and golden paths, CRDs and the operator pattern, Crossplane composite resources, Backstage software catalogs, and multi-tenancy models.
9. [Platform Observability, Reliability, and Lifecycle Operations](chapters/09-platform-observability-reliability-and-lifecycle-operations.md) — the Prometheus metrics stack, OpenTelemetry tracing, platform SLOs and error-budget alerting, chaos engineering, Cluster API fleet upgrades, and Kubernetes cost attribution.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.
- [Master index](../../INDEX.md) and [master glossary](../../GLOSSARY.md)
  — cross-volume topics and terminology for the complete encyclopedia.

## Software and platform baseline

Every chapter in this volume references the dated Kubernetes 1.31.x
baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md). Ecosystem tooling
versions used in examples and labs (containerd, Helm, Argo CD, Chaos
Mesh, and similar) are pinned inline in each chapter's commands rather
than tracked in the root baseline table; update the chapter's examples,
not this README, when a newer tool release changes example output.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-08-containers-platform-engineering

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-08-containers-platform-engineering/chapters/03-kubernetes-workloads-scheduling-and-capacity.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
