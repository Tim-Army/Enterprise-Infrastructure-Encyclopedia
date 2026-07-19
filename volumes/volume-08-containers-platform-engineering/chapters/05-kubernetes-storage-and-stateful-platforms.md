# Chapter 05: Kubernetes Storage and Stateful Platforms

## Learning Objectives

- Explain the Container Storage Interface (CSI) architecture and how it
  replaced in-tree volume plugins.
- Trace the PersistentVolume/PersistentVolumeClaim/StorageClass binding
  model, including dynamic provisioning and topology-aware scheduling.
- Select the correct access mode and volume binding mode for a given
  workload's concurrency and placement requirements.
- Configure VolumeSnapshots for point-in-time recovery and explain a
  StatefulSet's persistent volume claim retention behavior.
- Evaluate when a Kubernetes-native data-service operator is appropriate
  versus a managed external database.

## Theory and Architecture

Kubernetes storage answers a question orthogonal to workload identity
([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)): how does a pod get durable, addressable storage that
survives the pod itself being rescheduled? The answer is layered into
three cooperating objects and a plugin interface that keeps the
storage-vendor-specific logic out of Kubernetes core entirely.

### The Container Storage Interface

The **Container Storage Interface (CSI)** is a gRPC API, analogous in
spirit to the CRI ([Chapter 01](01-container-architecture-images-runtimes-and-registries.md)), that decouples Kubernetes from any
specific storage backend. A CSI driver implements three gRPC services —
`Identity`, `Controller` (provisioning, attaching, snapshotting, running
off-node as a Deployment), and `Node` (mounting, running as a DaemonSet on
every node) — and Kubernetes talks only to this interface, never to the
storage backend's native API directly. This is why the same
`PersistentVolumeClaim` object works identically whether the underlying
driver is `ebs.csi.aws.com`, `pd.csi.storage.gke.io`, a NAS vendor's
driver, or Ceph's `rbd.csi.ceph.com` — the workload manifest never names
the backend. The legacy in-tree volume plugins (compiled directly into
kubelet and kube-controller-manager) have been migrated to CSI equivalents
across every major cloud provider; new storage integrations are written
as CSI drivers exclusively.

### PersistentVolume, PersistentVolumeClaim, and StorageClass

```text
Developer writes a PVC          Platform pre-defines a StorageClass
 (how much, what access mode) ─────► (which CSI driver, parameters,
        │                              reclaim policy, binding mode)
        │                                       │
        ▼                                       ▼
        └──────────► CSI provisioner creates a PersistentVolume ◄──┘
                      and binds it 1:1 to the PVC
```

A **PersistentVolumeClaim (PVC)** is a namespaced request for storage — a
developer states size and access mode without knowing or caring which
disk, array, or cloud volume type backs it. A **PersistentVolume (PV)** is
the cluster-scoped object representing the actual provisioned storage,
created automatically by the CSI provisioner in the common **dynamic
provisioning** path (static provisioning, where an administrator
pre-creates PVs by hand, still exists but is now the exception). A
**StorageClass** is the platform team's policy object: which CSI driver
services the request, driver-specific parameters (disk type, IOPS,
filesystem), the `reclaimPolicy` (`Delete` removes the backing volume when
its PVC is deleted; `Retain` leaves it for manual recovery), and the
`volumeBindingMode`.

**`volumeBindingMode` is the detail most often overlooked.** `Immediate`
binds and provisions a volume the moment the PVC is created, before the
scheduler has chosen a node for the consuming pod — fine for
network-attached storage reachable from any node, but a scheduling trap
for storage with placement constraints (a single-zone disk, or a **local
persistent volume** tied to one specific node's local disk), because the
volume might be provisioned in a zone the scheduler then cannot place the
pod into. `WaitForFirstConsumer` defers binding until a pod actually
claims the PVC, so the provisioner can see the scheduler's chosen node and
provision storage compatible with it — the correct default for anything
with topology constraints.

### Access modes

| Access mode | Meaning | Typical backend |
| --- | --- | --- |
| `ReadWriteOnce` (RWO) | Read-write by a single node | Cloud block storage (EBS, PD, Azure Disk) |
| `ReadOnlyMany` (ROX) | Read-only by many nodes simultaneously | Shared reference data, NFS |
| `ReadWriteMany` (RWX) | Read-write by many nodes simultaneously | NFS, CephFS, cloud file services (EFS, Filestore, Azure Files) |
| `ReadWriteOncePod` (RWOP) | Read-write by exactly one *pod*, cluster-wide | Any backend; enforces single-writer at the pod level rather than the node level |

`ReadWriteOnce` is frequently misunderstood: it restricts a volume to a
single *node*, not a single *pod* — multiple pods on the same node can
still mount an RWO volume simultaneously, which has caused real data
corruption incidents for workloads that assumed single-writer semantics.
`ReadWriteOncePod`, generally available since the 1.29 line, closes that
gap by enforcing the single-pod guarantee directly.

### StatefulSets and per-ordinal storage

[Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md) introduced StatefulSet's stable ordinal identity; the storage
half of that contract is `volumeClaimTemplates`: the StatefulSet
controller creates one PVC per ordinal (`data-web-0`, `data-web-1`, ...)
the first time each pod is created, and — critically — reattaches the
*same* PVC to the *same* ordinal on every subsequent reschedule, even
across node failures. By default those PVCs outlive the StatefulSet
itself when it is deleted or scaled down, a deliberate safety default;
`persistentVolumeClaimRetentionPolicy` (stable since 1.27) makes that
behavior explicit and configurable per StatefulSet rather than leaving it
as an implicit, easy-to-forget default.

### Snapshots and cloning

The `snapshot.storage.k8s.io` API group — `VolumeSnapshotClass`,
`VolumeSnapshot`, and the resulting `VolumeSnapshotContent` — provides a
CSI-driver-backed, point-in-time snapshot mechanism with the same
claim/class separation pattern as PVs: a `VolumeSnapshot` is the
namespaced request, `VolumeSnapshotContent` is the cluster-scoped backing
object. A new PVC can be provisioned directly `dataSource`-ed from an
existing `VolumeSnapshot` (or, with a supporting driver, cloned directly
from another live PVC), which underlies both database restore workflows
and much of how backup tools like Velero perform application-consistent
recovery.

## Design Considerations

**Local vs. network-attached storage is a durability-vs-performance
trade.** Local persistent volumes (a specific node's NVMe/SSD, exposed
through the `local-path-provisioner`, Rancher's `local-path-provisioner`,
or a CSI driver like `local-static-provisioner`) deliver the lowest
latency and highest IOPS because there is no network hop, but the data
dies with the node — durability must come from the application layer
(a replicated database, a distributed filesystem) rather than the
storage layer. Network-attached block or file storage decouples data
from any single node's lifecycle at the cost of network latency and, for
block storage, single-node attach semantics (`ReadWriteOnce`).

**Reclaim policy is a data-loss decision, not a cleanup preference.** A
`StorageClass` with `reclaimPolicy: Delete` means deleting the PVC — a
routine, easily scripted action — permanently deletes the underlying
volume with it. Production data volumes should default to `Retain`
(recovering an orphaned volume manually is inconvenient; silently losing
one is a much worse outcome), reserving `Delete` for ephemeral or
easily-reprovisioned workloads such as CI scratch space or cache
volumes.

**Topology-aware provisioning is mandatory once a cluster spans zones.**
`Immediate` binding mode on a zonal storage backend routinely produces
pods stuck `Pending` because the volume landed in a zone with no
available scheduling capacity for the pod. `WaitForFirstConsumer`, paired
with a StorageClass's `allowedTopologies` when tighter control is needed,
keeps volume placement and pod placement in agreement by construction
rather than by chance.

**RWX is a capability gap, not a universal default.** Many high-performance
block storage backends only support `ReadWriteOnce`; workloads that
genuinely need concurrent multi-node write access (shared upload
directories, some batch-processing patterns) need a file-storage-backed
StorageClass (NFS, CephFS, EFS/Filestore/Azure Files) explicitly
provisioned for that purpose, and that storage class typically carries
different performance and cost characteristics than the default block
StorageClass — it should not be the platform's default for workloads that
do not need it.

**Running stateful data services on Kubernetes is a genuine operational
commitment, evaluated per service, not a blanket policy.** A well-built
Kubernetes operator (CloudNativePG for PostgreSQL, the Strimzi operator
for Kafka, the Elastic Cloud on Kubernetes operator) automates failover,
backup, and version upgrades using the same reconciliation model as
built-in controllers, and keeps the data service co-located with the
applications that consume it under the same GitOps and RBAC model
([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)). A managed external service (a cloud-managed database)
removes that operational surface entirely at the cost of a
network hop out of the cluster and a separate control plane to integrate
with the platform's identity and observability stack. The deciding factor
is usually less "can Kubernetes run this" — CSI, StatefulSets, and mature
operators make the technical answer yes for most data services — and more
whether the platform team is staffed to own database operations
day-two, including the failure modes a managed service's SLA already
absorbs.

## Implementation and Automation

### A topology-aware StorageClass and dynamically provisioned PVC

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-retained
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "6000"
  throughput: "250"
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: order-db-data
  namespace: payments
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: fast-retained
  resources:
    requests:
      storage: 100Gi
```

### A StatefulSet with per-ordinal storage and an explicit retention policy

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: order-db
  namespace: payments
spec:
  serviceName: order-db
  replicas: 3
  podManagementPolicy: OrderedReady
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Retain
  selector:
    matchLabels: { app: order-db }
  template:
    metadata:
      labels: { app: order-db }
    spec:
      containers:
        - name: order-db
          image: postgres:16.4
          ports: [{ containerPort: 5432, name: postgres }]
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-retained
        resources:
          requests:
            storage: 100Gi
```

`whenScaled: Retain` keeps `data-order-db-2`'s volume intact if the
StatefulSet is scaled from 3 to 2 and later back to 3 — the returning
ordinal reattaches its original volume rather than starting from an empty
one.

### VolumeSnapshot and restore-from-snapshot

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: ebs-csi-snapshot-class
driver: ebs.csi.aws.com
deletionPolicy: Retain
---
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: order-db-data-snap-2026-07-18
  namespace: payments
spec:
  volumeSnapshotClassName: ebs-csi-snapshot-class
  source:
    persistentVolumeClaimName: data-order-db-0
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: order-db-data-restored
  namespace: payments
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: fast-retained
  resources:
    requests:
      storage: 100Gi
  dataSource:
    name: order-db-data-snap-2026-07-18
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
```

```bash
# Confirm a snapshot became ready to use before relying on it.
kubectl get volumesnapshot -n payments order-db-data-snap-2026-07-18 \
  -o jsonpath='{.status.readyToUse}'

# Expand a PVC in place (only if allowVolumeExpansion: true on the class).
kubectl patch pvc order-db-data -n payments \
  -p '{"spec":{"resources":{"requests":{"storage":"150Gi"}}}}'
```

### Cluster-level backup with Velero and CSI snapshots

```bash
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.11.0,velero/velero-plugin-for-csi:v0.8.0 \
  --features=EnableCSI \
  --bucket platform-velero-backups \
  --backup-location-config region=us-east-2 \
  --snapshot-location-config region=us-east-2

velero backup create payments-namespace-backup --include-namespaces payments
velero backup describe payments-namespace-backup --details
```

## Validation and Troubleshooting

```bash
# Confirm the CSI driver is installed and its node/controller pods are healthy.
kubectl get csidrivers
kubectl get pods -n kube-system -l app=ebs-csi-controller
kubectl get pods -n kube-system -l app=ebs-csi-node -o wide

# Trace a PVC's binding state and the events explaining a stuck Pending claim.
kubectl describe pvc order-db-data -n payments

# Confirm which node a WaitForFirstConsumer volume actually landed in.
kubectl get pv <pv-name> -o jsonpath='{.spec.nodeAffinity}'
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| PVC stuck `Pending` | No StorageClass matches, provisioner unhealthy, or quota exhausted at the backend | `kubectl describe pvc`; CSI controller pod logs |
| Pod stuck `Pending` with a bound PVC | Volume provisioned in a zone/node the scheduler cannot place the pod into (`Immediate` binding on zonal storage) | `kubectl describe pod` events; compare PV `nodeAffinity` to available node zones |
| `multi-attach error for volume` | An RWO volume's previous pod was not fully released before rescheduling (e.g., after an ungraceful node loss) | `kubectl describe pod`; confirm the old pod/node is actually gone before forcing detach |
| StatefulSet pod reattaches to the wrong data on scale-down/up | `persistentVolumeClaimRetentionPolicy` not set, or PVCs manually deleted between scale events | `kubectl get pvc -l app=<name>`; verify ordinal-to-PVC mapping matches expectation |
| `VolumeSnapshot` never reaches `readyToUse: true` | Missing `VolumeSnapshotClass`, or CSI driver lacks snapshot support enabled | `kubectl describe volumesnapshot`; confirm the CSI driver's snapshot sidecar is running |

## Security and Best Practices

- Default production `StorageClass` objects to `reclaimPolicy: Retain`;
  reserve `Delete` for explicitly ephemeral or trivially reprovisioned
  storage.
- Use `WaitForFirstConsumer` binding mode for any storage with topology
  constraints — effectively all zonal block storage and all local
  persistent volumes.
- Encrypt volumes at the storage backend (EBS/PD/Azure Disk encryption,
  or a Ceph/NAS-level encryption feature) in addition to the etcd-level
  Secrets encryption covered in [Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md); volume encryption and
  control-plane data-at-rest encryption protect different assets.
- Restrict who can create `PersistentVolume` objects and `StorageClass`
  objects directly (as opposed to PVCs) via RBAC ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)); a
  statically provisioned PV can point at storage an administrator did not
  intend a tenant to access.
- Take application-consistent backups, not just crash-consistent
  snapshots, for stateful data services — quiesce or use the data
  service's native backup hooks (a `pg_basebackup`-integrated operator,
  for example) alongside or instead of a raw CSI snapshot when
  transactional consistency matters.
- Test restore procedures on the same cadence as etcd restore drills
  ([Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md)); an unverified snapshot or Velero backup carries the same
  false confidence as an unverified etcd snapshot.
- Set `allowVolumeExpansion: true` deliberately, and pair it with
  monitoring on volume utilization so expansion is a planned operation,
  not an emergency response to a full disk.

## References and Knowledge Checks

**Authoritative references**

- Kubernetes documentation, [Storage](https://kubernetes.io/docs/concepts/storage/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Kubernetes documentation, [Container Storage Interface (CSI)](https://kubernetes.io/docs/concepts/storage/volumes/#csi) and [Volume Snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/).
- Kubernetes documentation, [StatefulSet Basics](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/).
- CNCF, [Velero documentation](https://velero.io/docs/).
- CloudNativePG and Strimzi project documentation, [cloudnative-pg.io](https://cloudnative-pg.io/) and [strimzi.io](https://strimzi.io/).

**Knowledge check**

1. What three gRPC services does a CSI driver implement, and why does
   Kubernetes never call a storage backend's native API directly?
2. Why can `ReadWriteOnce` still allow two pods to corrupt the same
   volume simultaneously, and what access mode closes that gap?
3. Why does `Immediate` volume binding mode risk producing an unschedulable
   pod on zonal storage, and what does `WaitForFirstConsumer` change about
   the provisioning order to fix it?
4. What does `persistentVolumeClaimRetentionPolicy: whenScaled: Retain`
   preserve that the pre-1.27 default behavior did not make explicit?
5. What operational responsibility does a Kubernetes-native database
   operator take on that a managed external database service instead
   absorbs on the provider's side?

## Hands-On Lab

**Objective:** Provision topology-aware local storage, deploy a
StatefulSet with per-ordinal PVCs, take a snapshot, restore it into a new
PVC, and prove reclaim-policy `Retain` survives PVC deletion as a negative
test.

### Prerequisites

- A `kind` cluster (`kind` ships `local-path-provisioner` as its default
  `StorageClass`, sufficient for this lab; snapshot support is simulated
  via a manual copy step since `local-path-provisioner` has no CSI
  snapshot sidecar).
- `kubectl` matching the 1.31.x baseline.

### Procedure

1. Create the cluster and confirm the default StorageClass.

   ```bash
   kind create cluster --name storage-lab --image kindest/node:v1.31.4
   kubectl get storageclass
   ```

   **Expected result:** `standard` (provisioner `rancher.io/local-path`)
   listed with `(default)`.

2. Deploy a StatefulSet with `volumeClaimTemplates` and an explicit
   retention policy.

   ```bash
   kubectl create namespace storage-lab
   cat > statefulset.yaml <<'EOF'
   apiVersion: v1
   kind: Service
   metadata:
     name: data-svc
     namespace: storage-lab
   spec:
     clusterIP: None
     selector: { app: data-svc }
     ports: [{ port: 80 }]
   ---
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: data-svc
     namespace: storage-lab
   spec:
     serviceName: data-svc
     replicas: 2
     persistentVolumeClaimRetentionPolicy:
       whenDeleted: Retain
       whenScaled: Retain
     selector:
       matchLabels: { app: data-svc }
     template:
       metadata:
         labels: { app: data-svc }
       spec:
         containers:
           - name: writer
             image: busybox:1.36
             command: ["sh", "-c", "echo \"identity: $(hostname)\" > /data/identity.txt && sleep infinity"]
             volumeMounts:
               - { name: data, mountPath: /data }
     volumeClaimTemplates:
       - metadata: { name: data }
         spec:
           accessModes: ["ReadWriteOnce"]
           resources: { requests: { storage: 1Gi } }
   EOF
   kubectl apply -f statefulset.yaml
   kubectl rollout status statefulset/data-svc -n storage-lab
   ```

3. Confirm each ordinal wrote its own identity to its own volume.

   ```bash
   kubectl exec -n storage-lab data-svc-0 -- cat /data/identity.txt
   kubectl exec -n storage-lab data-svc-1 -- cat /data/identity.txt
   kubectl get pvc -n storage-lab
   ```

   **Expected result:** each pod reports its own hostname, and two PVCs
   (`data-data-svc-0`, `data-data-svc-1`) are `Bound`.

4. Delete `data-svc-1`'s pod directly and confirm the StatefulSet
   controller reattaches the *same* PVC rather than provisioning a new
   one.

   ```bash
   kubectl delete pod data-svc-1 -n storage-lab
   kubectl wait --for=condition=Ready pod/data-svc-1 -n storage-lab --timeout=60s
   kubectl exec -n storage-lab data-svc-1 -- cat /data/identity.txt
   ```

   **Expected result:** the identity file still reads `data-svc-1` — the
   original volume was reattached, not recreated empty.

### Negative test

5. Delete the entire StatefulSet with `--cascade=orphan` to simulate a
   controller-level deletion, then delete one PVC directly, and confirm
   that even with reclaim policy behavior, deleting the PVC is what
   removes the data — reinforcing why `Retain` matters for the underlying
   `PersistentVolume`.

   ```bash
   kubectl delete statefulset data-svc -n storage-lab --cascade=orphan
   kubectl get pvc -n storage-lab
   kubectl get pv | grep storage-lab
   ```

   **Expected result:** both PVCs and their bound PVs still exist after
   the StatefulSet itself is gone — `persistentVolumeClaimRetentionPolicy`
   (and the orphan cascade) preserved the data independent of the
   controller's own lifecycle, exactly as intended for a stateful
   workload.

6. Now delete one PVC directly and confirm this is the actual destructive
   action, distinct from deleting the StatefulSet.

   ```bash
   kubectl delete pvc data-data-svc-1 -n storage-lab
   kubectl get pv | grep storage-lab
   ```

   **Expected result:** the PV bound to `data-data-svc-1` is now either
   removed or, on a `Retain`-configured class, transitions to `Released`
   with no claim — demonstrating that reclaim policy governs PVC
   deletion, not StatefulSet deletion.

### Cleanup

```bash
kubectl delete namespace storage-lab
kind delete cluster --name storage-lab
rm -f statefulset.yaml
```

## Summary and Completion Checklist

CSI decouples Kubernetes from any specific storage backend behind a
common gRPC interface; PersistentVolumeClaim, PersistentVolume, and
StorageClass separate the developer's request from the platform's
provisioning policy, with `volumeBindingMode` and access mode as the two
settings most likely to cause a stuck or unschedulable workload when
chosen incorrectly. StatefulSets pair ordinal identity with per-ordinal
PVCs that survive rescheduling by default, and
`persistentVolumeClaimRetentionPolicy` makes that survival explicit.
VolumeSnapshots and Velero extend the same CSI foundation to point-in-time
recovery and namespace-level backup. Running stateful data services
directly on Kubernetes is a mature, well-supported option through
operators, but it is a deliberate operational commitment each platform
team should evaluate service by service.

- [ ] Can explain the CSI architecture and why Kubernetes never talks to
      a storage backend directly.
- [ ] Can trace the PVC/PV/StorageClass binding model, including dynamic
      provisioning and `volumeBindingMode`.
- [ ] Can select the correct access mode for a workload's concurrency
      requirement, including the RWO node-vs-pod distinction.
- [ ] Can configure VolumeSnapshots and explain StatefulSet PVC retention
      behavior.
- [ ] Can articulate the trade-off between a Kubernetes-native data
      operator and a managed external database.
- [ ] Completed the hands-on lab, including the reclaim/retention
      negative test, and performed cleanup.
