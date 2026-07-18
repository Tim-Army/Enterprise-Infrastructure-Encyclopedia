# Volume VIII Glossary

Definitions for terms introduced in **Volume VIII — Containers and
Platform Engineering**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter section each
term is drawn from, and the [master glossary](../../GLOSSARY.md) for
cross-volume terminology.

**Access mode (RWO/ROX/RWX/RWOP)** — The concurrency contract a
PersistentVolume grants: `ReadWriteOnce` (single node), `ReadOnlyMany`
(many nodes, read-only), `ReadWriteMany` (many nodes, read-write), and
`ReadWriteOncePod` (exactly one pod cluster-wide). Introduced in
Chapter 05.

**Admission control** — The API server pipeline stage, after
authentication and authorization, where mutating and validating
controllers (Pod Security admission, Kyverno, `ValidatingAdmissionPolicy`)
inspect or modify an object before it is persisted. Introduced in
Chapter 02 and expanded in Chapter 06.

**Ambient mesh** — A service mesh data-plane model that moves mutual TLS
and identity enforcement to a per-node component rather than a per-pod
sidecar proxy, reducing resource overhead compared to the classic sidecar
model. Introduced in Chapter 04.

**Argo CD** — A GitOps controller that models each deployed unit as an
`Application` custom resource and continuously reconciles cluster state
toward a Git repository's declared state. Introduced in Chapter 07.

**Argo Rollouts** — A progressive-delivery controller that replaces a
Deployment with a `Rollout` custom resource supporting canary and
blue-green strategies gated by automated metric analysis. Introduced in
Chapter 07.

**Backstage** — A CNCF developer portal project providing a software
catalog, documentation rendering (TechDocs), and a self-service
scaffolder for generating new services from golden-path templates.
Introduced in Chapter 08.

**Bound ServiceAccount token** — A short-lived, audience-scoped
authentication token issued through the `TokenRequest` API and
automatically refreshed by kubelet, replacing the indefinitely valid
Secret-mounted tokens Kubernetes auto-minted before version 1.24.
Introduced in Chapter 06.

**cgroups v2** — The unified Linux control group hierarchy used to meter
and bound CPU, memory, I/O, and process count for a container; Kubernetes
1.31.x assumes cgroup v2 on the node. Introduced in Chapter 01.

**Chaos engineering** — The practice of deliberately injecting controlled
failure into a running system to validate that monitoring, alerting, and
automated remediation behave as designed. Introduced in Chapter 09.

**Cilium** — An eBPF-based CNI plugin capable of fully replacing
kube-proxy's Service load-balancing with in-kernel programs, alongside
NetworkPolicy enforcement and deep flow observability via Hubble.
Introduced in Chapter 04.

**Cluster API (CAPI)** — A Kubernetes subproject that manages Kubernetes
clusters themselves as declarative objects (`Cluster`,
`MachineDeployment`) on a management cluster, enabling fleet-scale,
reconciled cluster lifecycle operations. Introduced in Chapter 09.

**Cluster Autoscaler** — A controller that scales predefined cloud
provider node groups up or down based on unschedulable pods and node
underutilization, distinct from Karpenter's group-less provisioning
model. Introduced in Chapter 03.

**Container Network Interface (CNI)** — The plugin interface satisfying
Kubernetes' NAT-free, cluster-wide pod-to-pod networking requirement;
implementations range from overlay networks to native BGP routing to
eBPF dataplanes. Introduced in Chapter 04.

**Container Runtime Interface (CRI)** — The gRPC API kubelet uses to
control a node's high-level container runtime (containerd, CRI-O)
without depending on any runtime-specific implementation detail.
Introduced in Chapter 01.

**Control plane** — The set of components (kube-apiserver, etcd,
kube-scheduler, kube-controller-manager, cloud-controller-manager) that
expose the Kubernetes API, persist cluster state, and run the
reconciliation loops driving observed state toward desired state.
Introduced in Chapter 02.

**Crossplane** — A Kubernetes extension that represents external cloud
infrastructure as Kubernetes custom resources, using Composite Resource
Definitions and Compositions to expose platform-guardrailed,
developer-facing claims. Introduced in Chapter 08.

**Custom Resource Definition (CRD)** — An API extension mechanism that
registers a new API group/version/kind, giving it full CRUD, watch,
schema validation, and — paired with a controller — reconciliation
identical to a built-in Kubernetes object. Introduced in Chapter 02 and
central to the platform engineering pattern in Chapter 08.

**DaemonSet** — A workload controller guaranteeing exactly one pod copy
per node (or per matching node subset), used almost universally for
node-level agents such as CNI plugins and log shippers. Introduced in
Chapter 03.

**Distroless image** — A minimal container base image containing only a
language runtime and application dependencies, with no shell or package
manager, reducing CVE and attack surface compared to a full distribution
base. Introduced in Chapter 01.

**EndpointSlice** — The sharded, topology-aware object tracking a
Service's backing pod addresses, which replaced the monolithic
`Endpoints` object as the default to reduce reprocessing cost at scale.
Introduced in Chapter 04.

**Error budget** — The amount of unreliability a Service Level Objective
permits over a period; a platform's error budget burn rate is the basis
for both paging alerts and automated progressive-delivery rollback gates.
Introduced in Chapter 09 and first defined in Volume I.

**External Secrets Operator (ESO)** — A controller that syncs secret
material from an external store (Vault, cloud secret managers) into
native Kubernetes Secrets on a refresh interval, keeping the source of
truth and rotation outside the cluster. Introduced in Chapter 06.

**Gateway API** — The Kubernetes-standardized successor to Ingress,
separating a shared `Gateway` listener (platform-owned) from
per-team `HTTPRoute`/`GRPCRoute`/`TCPRoute` objects with richer, portable
traffic matching. Introduced in Chapter 04.

**GitOps** — A delivery model in which an in-cluster controller
continuously and automatically reconciles live cluster state toward a
Git repository's declared state, rather than a CI pipeline pushing
changes directly with cluster credentials. Introduced in Chapter 07.

**Golden path** — An opinionated, supported, self-service route from
zero to a running, production-ready workload, with a platform team's
security and reliability defaults built in rather than left to each
application team to reproduce. Introduced in Chapter 08.

**Horizontal Pod Autoscaler (HPA)** — A controller (`autoscaling/v2`)
that adjusts a workload's replica count based on resource utilization or
custom/external metrics, reading live usage from metrics-server or a
metrics adapter. Introduced in Chapter 03.

**In-place pod resize** — An alpha-stage Kubernetes feature
(`InPlacePodVerticalScaling`) allowing a pod's resource requests/limits
to be changed without restarting the container, distinct from the
restart-based Vertical Pod Autoscaler update modes it may eventually
supersede. Introduced in Chapter 03.

**Ingress** — A stable API for HTTP(S) routing into a cluster, using
host/path rules and a pluggable Ingress controller, with an
intentionally narrow, controller-annotation-dependent feature set.
Introduced in Chapter 04.

**Internal Developer Platform (IDP)** — The concrete system — portal,
CRDs, operators, scaffolding — that implements an organization's golden
paths and exposes infrastructure as a self-service product rather than a
ticket queue. Introduced in Chapter 08.

**Job** — A workload controller that runs a pod (or set of pods) to
successful completion rather than indefinitely, with `backoffLimit` and
`podFailurePolicy` governing retry behavior. Introduced in Chapter 03.

**Karpenter** — A node-provisioning controller that creates individual
nodes directly from a `NodePool`/`NodeClass` specification at the moment
a pod is unschedulable, without relying on predefined cloud node groups.
Introduced in Chapter 03.

**kube-proxy** — The node component that programs Service load-balancing
rules (`iptables`, IPVS, or beta `nftables` mode) so traffic to a
Service's ClusterIP reaches a backing pod; can be fully replaced by an
eBPF dataplane such as Cilium. Introduced in Chapter 02 and expanded in
Chapter 04.

**Kustomize** — A template-free Kubernetes manifest composition tool
that applies structured patches from environment-specific overlays onto
a shared base of plain YAML. Introduced in Chapter 07.

**Kyverno** — A Kubernetes-native policy engine that authors validation,
mutation, resource generation, and image-verification rules as ordinary
Kubernetes YAML `ClusterPolicy` objects. Introduced in Chapter 06.

**Multi-tenancy model** — The isolation boundary chosen for tenants
sharing a platform: namespace-based soft multi-tenancy, virtual clusters,
hierarchical namespaces, or fully dedicated (hard) clusters per tenant.
Introduced in Chapter 08.

**NetworkPolicy** — A default-allow, opt-in-deny API for pod-level
network segmentation, enforced only by CNI plugins that implement it.
Introduced in Chapter 04.

**Node affinity** — A scheduling mechanism that pulls a pod toward nodes
matching a label expression, supporting both hard requirements and soft
preferences, distinct from a taint's node-side repulsion. Introduced in
Chapter 03.

**Operator pattern** — The practice of pairing a Custom Resource
Definition with a purpose-built controller that encodes operational
knowledge (provisioning, failover, upgrade) for a specific application or
infrastructure type. Introduced in Chapter 08.

**OpenTelemetry** — The vendor-neutral instrumentation standard and
Collector pipeline for traces, metrics, and logs, allowing
instrumentation written once to survive a backend migration unchanged.
Introduced in Chapter 09.

**Pod Security admission** — The built-in, namespace-label-driven
admission controller enforcing the `privileged`, `baseline`, or
`restricted` Pod Security Standards, which replaced PodSecurityPolicy
(removed in Kubernetes 1.25). Introduced in Chapter 06.

**PodDisruptionBudget (PDB)** — An object constraining voluntary
disruptions (drains, autoscaler consolidation) via `minAvailable` or
`maxUnavailable`, with no effect on involuntary disruptions such as a
node crash or a direct pod-kill chaos action. Introduced in Chapter 03.

**PriorityClass** — An object assigning an integer priority to a pod,
used by the scheduler to determine preemption order when resources are
scarce, distinct from a PodDisruptionBudget's disruption limits.
Introduced in Chapter 03.

**Progressive delivery** — Deployment strategies (canary, blue-green)
that shift traffic to a new version incrementally, gated by automated
metric analysis that can abort and roll back before a full rollout
completes. Introduced in Chapter 07.

**Quality of Service (QoS) class** — The `Guaranteed`, `Burstable`, or
`BestEffort` classification the kubelet derives from a pod's
requests/limits, determining eviction order under node resource
pressure. Introduced in Chapter 03.

**RBAC (Role-Based Access Control)** — Kubernetes' strictly additive
authorization model built from `Role`/`ClusterRole` (permission sets) and
`RoleBinding`/`ClusterRoleBinding` (grants to subjects), with no native
deny rule. Introduced in Chapter 06.

**Reclaim policy** — The `StorageClass`/`PersistentVolume` setting
(`Delete` or `Retain`) governing whether the backing storage is destroyed
or preserved when its claim is deleted. Introduced in Chapter 05.

**Secrets Store CSI Driver** — A CSI-based mechanism that mounts secret
material from an external store directly into a pod's filesystem without
creating a persistent native Kubernetes Secret object. Introduced in
Chapter 06.

**Service** — The stable-address, load-balancing abstraction over an
unstable population of pods, with types including `ClusterIP`,
`NodePort`, `LoadBalancer`, `ExternalName`, and headless. Introduced in
Chapter 04.

**ServiceAccount** — The namespaced, workload-facing identity every pod
runs as by default, analogous to a human user but native to Kubernetes.
Introduced in Chapter 06.

**SLSA (Supply-chain Levels for Software Artifacts)** — A framework
defining a ladder of increasing build-integrity guarantees, from a
documented build process through non-forgeable, cryptographically
verifiable provenance. Introduced in Chapter 07.

**Software Bill of Materials (SBOM)** — A structured inventory of a
container image's software components and dependencies, generated at
build time and usable as both a vulnerability-response input and a
supply-chain policy input. Introduced in Chapter 01.

**Static pod** — A pod manifest the kubelet reads directly from a local
directory rather than from the API server, used to bootstrap control
plane components on `kubeadm`-managed clusters. Introduced in Chapter 02.

**StatefulSet** — A workload controller providing stable ordinal pod
identity, stable per-pod DNS, and a stable PersistentVolumeClaim per
ordinal that survives pod rescheduling, via `volumeClaimTemplates`.
Introduced in Chapter 03 and expanded in Chapter 05.

**StorageClass** — The platform-defined policy object naming a CSI
driver, its provisioning parameters, reclaim policy, and
`volumeBindingMode` for dynamically provisioned storage. Introduced in
Chapter 05.

**Taint and toleration** — A node-side repulsion mechanism (`taint`)
paired with a pod-side opt-in (`toleration`), used to reserve nodes for
specific workloads. Introduced in Chapter 03.

**Topology spread constraint** — A scheduling control that limits the
skew in pod distribution across a topology domain (zone, node), softer
and more scalable than a hard pod anti-affinity rule at high replica
counts. Introduced in Chapter 03.

**ValidatingAdmissionPolicy** — A native, in-process admission mechanism
(GA since Kubernetes 1.30) using CEL expressions directly in the API
server, avoiding the webhook round trip and failure-mode trade-offs of
Kyverno or Gatekeeper for validation-only rules. Introduced in
Chapter 06.

**Version skew policy** — The Kubernetes compatibility rules bounding how
far kubelet, kube-proxy, and control-plane components may differ in
version from kube-apiserver during an upgrade. Introduced in Chapter 02.

**Vertical Pod Autoscaler (VPA)** — A separate autoscaler add-on that
recommends or applies resource request/limit changes for a workload
based on historical usage, typically restart-based in its automatic
update modes. Introduced in Chapter 03.

**VolumeSnapshot** — A CSI-driver-backed API (`snapshot.storage.k8s.io`)
for point-in-time volume snapshots, usable as a `dataSource` for
provisioning a new PVC. Introduced in Chapter 05.

**`volumeBindingMode`** — The `StorageClass` setting controlling whether
a PersistentVolume is provisioned immediately on PVC creation
(`Immediate`) or deferred until a pod actually claims it
(`WaitForFirstConsumer`), critical for topology-constrained storage.
Introduced in Chapter 05.

**Workload identity federation** — The pattern (IRSA on EKS, Workload
Identity on GKE, Azure AD Workload Identity on AKS) that exchanges a
pod's bound ServiceAccount token for short-lived cloud credentials,
eliminating static cloud access keys stored as Secrets. Introduced in
Chapter 06.
