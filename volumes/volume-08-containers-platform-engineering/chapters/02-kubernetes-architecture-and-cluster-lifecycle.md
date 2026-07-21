# Chapter 02: Kubernetes Architecture and Cluster Lifecycle

![Lab topology for this chapter: a three-node kind cluster runs etcd, kube-apiserver, kube-scheduler, and kube-controller-manager as static pods on the control-plane node; etcd cluster health is confirmed and a snapshot is taken and verified as structurally valid. As a negative test, one worker's container is stopped; the node transitions to NotReady after the default node-monitor-grace-period, and any pods scheduled there are marked for eviction and rescheduled onto the remaining worker. Restarting the stopped worker returns it to Ready within about a minute as kubelet re-registers.](../../../diagrams/volume-08-containers-platform-engineering/chapter-02-kind-cluster-etcd-node-loss-topology.svg)

*Figure 2-1. Topology used throughout this chapter's Hands-On Lab: a kind cluster's control-plane static pods and etcd snapshot, tested against a simulated worker-node failure and recovery.*

## Learning Objectives

- Identify every control plane and node component in a Kubernetes 1.31.x
  cluster and describe the responsibility boundary between them.
- Explain the API server's request pipeline: authentication, authorization,
  admission control, and persistence to etcd.
- Stand up a multi-node cluster, verify component health, and read static
  pod manifests that bootstrap the control plane.
- Back up and restore etcd, and reason about the blast radius of etcd
  quorum loss.
- Apply the Kubernetes version skew policy to plan a safe control-plane and
  node upgrade sequence.

## Theory and Architecture

A Kubernetes cluster is a distributed control system: a declarative API,
a strongly consistent store, and a set of independent controllers that
continuously reconcile observed state toward desired state. Nothing in the
architecture is monolithic — every component can be read, understood, and
replaced in isolation, which is what makes managed offerings (EKS, AKS, GKE)
and self-managed `kubeadm` clusters interoperable at the API level despite
very different control-plane operations underneath.

### Control plane components

- **kube-apiserver** — the only component that talks to etcd directly. It
  exposes the Kubernetes REST API, validates and persists objects, and
  serves as the front door for every other component, including
  controllers and kubelets. It is horizontally scalable and stateless
  behind a load balancer in an HA topology.
- **etcd** — a distributed, strongly consistent key-value store using the
  Raft consensus algorithm. Every Kubernetes object lives here. etcd
  requires a quorum (a majority) of its members to be healthy to accept
  writes, which is why production etcd topologies run an odd number of
  members (3 or 5), never an even number.
- **kube-scheduler** — watches for pods with no assigned node, runs them
  through a filtering phase (which nodes are feasible) and a scoring phase
  (which feasible node is best), and writes the binding back through the
  API server. The scheduler itself never talks to kubelet directly.
- **kube-controller-manager** — runs the core reconciliation loops compiled
  into a single binary for operational simplicity: the node controller,
  replication controller, endpoint(-slice) controller, service account and
  token controllers, and more. Each loop watches the API server and drives
  observed state toward spec.
- **cloud-controller-manager** — isolates cloud-provider-specific
  reconciliation (node lifecycle tied to a cloud instance, route
  configuration, LoadBalancer-type Service provisioning) out of the core
  controller-manager so the core Kubernetes codebase stays cloud-agnostic.

### Node components

- **kubelet** — the primary node agent. It registers the node with the API
  server, watches for pods assigned to that node, and drives the CRI
  runtime ([Chapter 01](01-container-architecture-images-runtimes-and-registries.md)) to start containers, mounts volumes through CSI
  ([Chapter 05](05-kubernetes-storage-and-stateful-platforms.md)), and reports pod and node status back to the API server.
  kubelet does not read the API server's object store directly for every
  decision — it maintains a local cache via watch and reconciles the
  container runtime state against it.
- **kube-proxy** — implements the Service abstraction on each node by
  programming packet-handling rules — historically `iptables`, optionally
  IPVS for large Service counts, with an nftables-mode maturing across
  recent releases — so traffic to a Service's ClusterIP reaches a backing
  pod. Many CNI implementations, notably Cilium, can replace kube-proxy
  entirely with eBPF-based dataplane programming; this is covered in
  [Chapter 04](04-kubernetes-networking-service-delivery-and-traffic-policy.md).
- **Container runtime** — containerd or CRI-O, speaking CRI to kubelet, as
  detailed in [Chapter 01](01-container-architecture-images-runtimes-and-registries.md).

### The request pipeline and API machinery

Every write to the cluster — `kubectl apply`, a controller's reconcile
write, a kubelet status update — passes through the same pipeline inside
kube-apiserver:

```text
Client (kubectl, controller, kubelet)
   │
   ▼
Authentication  — who are you? (client cert, bearer/service-account
                   token, OIDC token, webhook)
   │
   ▼
Authorization   — are you allowed to do this? (RBAC is the default and
                   near-universal mode in 1.31.x; Chapter 06 covers RBAC
                   in depth)
   │
   ▼
Admission control (mutating)   — defaulting, sidecar/label injection
   │
   ▼
Object schema validation (OpenAPI/CRD schema)
   │
   ▼
Admission control (validating) — Pod Security admission, policy engines
                                   (Kyverno/Gatekeeper), resource quota
   │
   ▼
Persisted to etcd, watch events fan out to controllers and kubelets
```

**Custom Resource Definitions (CRDs)** extend this same pipeline to
non-built-in types. A CRD registers a new API group/version/kind; the API
server then serves full CRUD, watch, validation (via an embedded OpenAPI
schema), and — if a controller is running that watches the CRD — full
reconciliation, identically to a built-in object like Deployment. This is
the mechanism every operator, GitOps controller ([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)), and
platform abstraction ([Chapter 08](08-internal-developer-platforms-and-platform-products.md)) in this volume is built on.
**API aggregation** is the related mechanism that lets an entirely separate
API server (such as the metrics API server backing `kubectl top`) appear
under the same `kubectl`/API surface without being compiled into
kube-apiserver itself.

## Design Considerations

**Stacked vs. external etcd.** In a stacked topology, etcd runs as a static
pod co-located with each control-plane node's kube-apiserver — simpler to
operate, and `kubeadm`'s default. In an external topology, etcd runs on a
dedicated set of hosts separate from the API server nodes — more moving
parts, but it decouples etcd's resource and failure profile from the API
server's and allows independent scaling and hardware selection (etcd is
extremely latency-sensitive to its backing disk; it wants low fsync
latency, not necessarily large storage). Most production self-managed
clusters above a handful of nodes choose external etcd; managed offerings
abstract this decision away entirely.

**HA control plane sizing.** Three control-plane nodes is the practical
minimum for tolerating a single node failure while keeping etcd quorum (2 of
3 remaining). Five tolerates two failures at the cost of more Raft replication
traffic. Even-numbered etcd clusters are strictly worse than the
odd-numbered cluster one smaller — they add a member without adding
fault tolerance.

**Managed vs. self-managed.** A managed control plane (EKS, AKS, GKE)
removes etcd operations, API server scaling, and control-plane upgrade
mechanics from your team's responsibility entirely, at the cost of losing
direct access to control-plane flags, static pod manifests, and (in most
cases) etcd itself. Self-managed clusters, typically bootstrapped with
`kubeadm` or Cluster API, give full control at the cost of owning etcd
backup/restore, certificate rotation, and upgrade sequencing — the
operational surface this chapter focuses on.

**Version skew policy.** Kubernetes supports a bounded skew between
components during an upgrade: kube-apiserver instances in an HA cluster may
differ by at most one minor version from each other; kubelet may be up to
three minor versions older than kube-apiserver (as of the current skew
policy); kube-scheduler, kube-controller-manager, and kube-proxy must not be
newer than kube-apiserver. This is why upgrades proceed
control-plane-first, one minor version at a time, never skipping a minor
version.

**Node pools and lifecycle.** Grouping nodes into pools by instance
type, taint, or workload class ([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md) covers taints/tolerations)
lets you upgrade or replace one pool without touching another, and is the
basis for surge-upgrade strategies where new nodes on the new version join
before old nodes are drained and removed.

## Implementation and Automation

### Bootstrapping an HA control plane with kubeadm

```bash
# On the first control-plane node, behind a load balancer at
# control-plane-lb.example.internal:6443
kubeadm init \
  --control-plane-endpoint "control-plane-lb.example.internal:6443" \
  --upload-certs \
  --pod-network-cidr "10.244.0.0/16" \
  --kubernetes-version "v1.31.4"

# On additional control-plane nodes, using the join command and
# certificate key printed by kubeadm init.
kubeadm join control-plane-lb.example.internal:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <certificate-key>

# On worker nodes.
kubeadm join control-plane-lb.example.internal:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>
```

### Reading the static pod manifests that define the control plane

`kubeadm`-bootstrapped control-plane components run as **static pods** —
manifests the kubelet reads directly from a local directory, not from the
API server, which solves the chicken-and-egg problem of running the API
server as a pod scheduled by... the API server.

```bash
ls /etc/kubernetes/manifests/
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

# Editing a static pod manifest and saving it triggers the kubelet to
# restart that component automatically — no `kubectl apply` involved.
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

### etcd backup and restore

```bash
# Snapshot etcd (run on a control-plane node with access to etcd's
# client certs).
ETCDCTL_API=3 etcdctl snapshot save /var/backups/etcd-snapshot-$(date +%F).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify the snapshot is structurally sound before you need it.
ETCDCTL_API=3 etcdctl snapshot status /var/backups/etcd-snapshot-2026-07-18.db -w table

# Restore into a fresh data directory (performed offline, one member at a
# time, as part of full disaster recovery — not a routine operation).
ETCDCTL_API=3 etcdctl snapshot restore /var/backups/etcd-snapshot-2026-07-18.db \
  --data-dir /var/lib/etcd-restored
```

### Upgrading a kubeadm cluster, one minor version at a time

```bash
# On the first control-plane node.
apt-get update && apt-get install -y kubeadm=1.31.4-1.1
kubeadm upgrade plan
kubeadm upgrade apply v1.31.4

# On every node, including the one just upgraded, refresh kubelet/kubectl
# and drain before touching the node's packages.
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
apt-get install -y kubelet=1.31.4-1.1 kubectl=1.31.4-1.1
systemctl daemon-reload && systemctl restart kubelet
kubectl uncordon <node-name>
```

## Validation and Troubleshooting

```bash
# Cluster-level health (componentstatuses is deprecated; prefer these).
kubectl get nodes -o wide
kubectl get pods -n kube-system
kubectl version

# etcd member health and quorum from inside the etcd static pod.
kubectl exec -n kube-system etcd-<node> -- etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health --cluster -w table

# Node-level runtime and kubelet diagnostics without the API server.
sudo crictl ps
sudo crictl info
sudo journalctl -u kubelet -f --no-pager
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| `kubectl` hangs or times out entirely | API server unreachable — LB misconfigured, or all API server instances down | `curl -k https://control-plane-lb:6443/healthz`; check static pod status via `crictl ps` on each control-plane node |
| Writes fail with `etcdserver: request timed out` | etcd has lost quorum (fewer than a majority of members healthy) | `etcdctl endpoint health --cluster`; check disk fsync latency, a frequent root cause of etcd instability |
| Node stuck `NotReady` after reboot | kubelet cannot reach the API server, or CRI socket path mismatch | `journalctl -u kubelet`; verify `crictl` reaches the runtime socket |
| `kubeadm upgrade apply` fails preflight | Version skew violated, or control-plane component drift from expected manifest | `kubeadm upgrade plan` output; compare running component versions against target |
| Certificates expired, cluster-wide auth failures | kubeadm-managed certs (1-year default validity) not rotated | `kubeadm certs check-expiration`; `kubeadm certs renew all` |

## Security and Best Practices

- Restrict etcd to a private network reachable only by control-plane nodes;
  etcd has no object-level authorization of its own — anyone who can reach
  its client port with valid certs can read or write the entire cluster
  state, including Secrets.
- Enable **encryption at rest** for Secrets (and any other sensitive
  resource) via an `EncryptionConfiguration` on kube-apiserver so etcd's
  on-disk data is not plaintext even if the storage volume is exfiltrated.
- Disable anonymous authentication and legacy ABAC on the API server;
  RBAC should be the sole authorization mode ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)).
- Enable and ship **audit logs** from kube-apiserver to a system outside
  the cluster's own control plane, so an attacker who compromises the
  control plane cannot also erase the record of how.
- Rotate kubelet and control-plane certificates before their default
  validity window expires; monitor `kubeadm certs check-expiration` output
  as a recurring operational check, not a break-glass step.
- Take etcd snapshots on a defined schedule and — critically — practice
  the restore procedure before you need it in an incident; an untested
  backup is not a recovery plan.
- Apply the version skew policy strictly during upgrades: control plane
  before nodes, one minor version at a time, never skipping a minor
  version even under upgrade pressure.

## References and Knowledge Checks

**Authoritative references**

- Kubernetes documentation, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Kubernetes documentation, [Operating etcd clusters for Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) and [etcd documentation](https://etcd.io/docs/).
- Kubernetes documentation, [Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/).
- Kubernetes documentation, [kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/).
- Kubernetes SIG Cluster Lifecycle, [Cluster API](https://cluster-api.sigs.k8s.io/).

**Knowledge check**

1. Why must etcd clusters use an odd number of members, and what does
   "quorum" mean in terms of that number?
2. Which control-plane component is the only one that communicates
   directly with etcd, and what problem does that design constraint solve?
3. What is a static pod, and why does kube-apiserver itself have to run as
   one in a kubeadm-bootstrapped cluster rather than a normal Deployment?
4. Under the Kubernetes version skew policy, in what order must you upgrade
   kube-apiserver, kubelet, and kube-proxy, and why?
5. What single API-server configuration prevents Secrets from being stored
   as plaintext inside etcd's data files?

## Hands-On Lab

**Objective:** Build a multi-node cluster with `kind` (which bootstraps
each node with `kubeadm` internally), inspect control-plane static pods and
etcd health, take and verify an etcd snapshot, and observe cluster behavior
under a simulated node loss.

### Prerequisites

- Docker Engine running locally.
- `kind` v0.24+, `kubectl` matching the 1.31.x baseline, `etcdctl` v3.5+
  installed locally (or run it via `kubectl exec` against the etcd static
  pod as shown below, which requires no local `etcdctl`).

### Procedure

1. Define a three-node cluster (one control plane, two workers) and create
   it.

   ```bash
   cat > kind-config.yaml <<'EOF'
   kind: Cluster
   apiVersion: kind.x-k8s.io/v1alpha4
   nodes:
     - role: control-plane
     - role: worker
     - role: worker
   EOF
   kind create cluster --name lifecycle-lab --config kind-config.yaml --image kindest/node:v1.31.4
   ```

2. Confirm all nodes are `Ready` and identify the control-plane node's
   static pods.

   ```bash
   kubectl get nodes -o wide
   kubectl get pods -n kube-system -o wide
   ```

   **Expected result:** three `Ready` nodes; `etcd-lifecycle-lab-control-plane`,
   `kube-apiserver-lifecycle-lab-control-plane`,
   `kube-scheduler-...`, and `kube-controller-manager-...` pods running.

3. Read the static pod manifest directly from the control-plane container
   (kind runs each "node" as a container).

   ```bash
   docker exec lifecycle-lab-control-plane cat /etc/kubernetes/manifests/kube-apiserver.yaml | head -20
   ```

4. Check etcd cluster health via `kubectl exec` into the etcd static pod.

   ```bash
   kubectl exec -n kube-system etcd-lifecycle-lab-control-plane -- etcdctl \
     --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     endpoint health -w table
   ```

   **Expected result:** a table reporting the single etcd endpoint as
   healthy with a measured latency.

5. Take an etcd snapshot and verify it.

   ```bash
   kubectl exec -n kube-system etcd-lifecycle-lab-control-plane -- etcdctl \
     --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     snapshot save /var/lib/etcd-snapshot.db

   kubectl exec -n kube-system etcd-lifecycle-lab-control-plane -- etcdctl \
     snapshot status /var/lib/etcd-snapshot.db -w table
   ```

   **Expected result:** `snapshot status` reports a hash, revision, total
   keys, and size — confirming the snapshot is structurally valid.

6. Deploy a trivial workload so there is observable state to protect.

   ```bash
   kubectl create deployment hello --image=registry.k8s.io/e2e-test-images/agnhost:2.53 -- /agnhost netexec --http-port=8080
   kubectl rollout status deployment/hello
   ```

### Negative test

7. Simulate a worker node failure by stopping its container, and observe
   how the control plane reacts within its default `node-monitor-grace-period`.

   ```bash
   docker stop lifecycle-lab-worker
   kubectl get nodes -w
   ```

   **Expected result:** the stopped node transitions to `NotReady` after
   roughly 40 seconds (the default `node-monitor-grace-period`), and after
   the pod eviction timeout, any pods scheduled there are marked for
   eviction and rescheduled onto the remaining worker if the workload's
   controller (ReplicaSet/Deployment) demands a replica count greater than
   zero. Press Ctrl+C once you observe the `NotReady` transition.

8. Restore the node and confirm the cluster self-heals.

   ```bash
   docker start lifecycle-lab-worker
   kubectl get nodes -w
   ```

   **Expected result:** the node returns to `Ready` within roughly a
   minute as kubelet re-registers.

### Cleanup

```bash
kubectl delete deployment hello
kind delete cluster --name lifecycle-lab
rm -f kind-config.yaml
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Kubernetes separates concerns cleanly: kube-apiserver is the sole gateway
to etcd's strongly consistent state; independent controllers reconcile
observed state toward desired state; kubelet and kube-proxy carry that
state onto each node. Static pods solve the bootstrap problem for the
control plane itself. Operating a self-managed cluster means owning etcd
quorum health, backup/restore, certificate rotation, and a version-skew-
respecting upgrade sequence — all of which managed Kubernetes offerings
absorb on your behalf, at the cost of direct control-plane access.

- [ ] Can name every control-plane and node component and its single
      responsibility.
- [ ] Can trace a write request through authentication, authorization,
      admission, and persistence.
- [ ] Can locate and interpret static pod manifests on a control-plane
      node.
- [ ] Can take and verify an etcd snapshot and explain what quorum loss
      means operationally.
- [ ] Can state the version skew policy and apply it to plan an upgrade
      order.
- [ ] Completed the hands-on lab, including the simulated node-loss
      negative test, and performed cleanup.
