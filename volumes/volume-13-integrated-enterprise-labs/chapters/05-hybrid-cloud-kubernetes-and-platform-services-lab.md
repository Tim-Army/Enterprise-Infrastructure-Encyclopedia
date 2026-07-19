# Chapter 05: Hybrid Cloud, Kubernetes, and Platform Services Lab

## Learning Objectives

- Stand up the `CLOUD1` landing zone from [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s topology as a real
  cloud VPC/VNet with guardrails, connected to `HQ` over a site-to-site VPN.
- Build a single Kubernetes cluster that spans an on-premises control
  plane and workers in both `HQ` and `CLOUD1`, demonstrating a genuinely
  hybrid platform rather than two clusters that happen to coexist.
- Deploy a minimal internal developer platform surface — a container
  registry and an ingress controller — as in-cluster platform services.
- Schedule a sample workload across both locations and verify traffic
  reaches it regardless of which node answers.
- Prove the cluster degrades gracefully, not catastrophically, when the
  hybrid VPN link fails.

## Theory and Architecture

`CLOUD1` has existed only as a name in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s topology manifest until
now. This chapter builds it: a landing zone following [Volume VII](../../volume-07-cloud-infrastructure/README.md) (Cloud
Infrastructure), [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) (Landing Zones, Resource Organization, and
Guardrails) for account/project structure and baseline controls, [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)
(Cloud Identity, Access, and Cryptographic Services) for the identity
boundary between the cloud account and `corp.meridian.example`, and Chapter
04 (Cloud Networking and Hybrid Connectivity) for the VPN attachment back
to `rtr-hq01`, the WAN edge router [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) built.

The Kubernetes design follows [Volume VIII](../../volume-08-containers-platform-engineering/README.md) (Containers and Platform
Engineering): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) (Kubernetes Architecture and Cluster Lifecycle)
for the control-plane/worker topology, [Chapter 04](04-virtualization-storage-and-data-protection-lab.md) (Kubernetes Networking,
Service Delivery, and Traffic Policy) for the CNI and ingress design, and
[Chapter 08](08-observability-operations-and-major-incident-lab.md) (Internal Developer Platforms and Platform Products) for framing
the registry and ingress as the beginning of a platform surface rather than
one-off deployments. Placing a worker node in `CLOUD1` and workers in `HQ`
under one control plane is the concrete expression of [Volume VII](../../volume-07-cloud-infrastructure/README.md), Chapter
07 (Hybrid and Multicloud Architecture): one workload-scheduling domain
spanning two infrastructure locations, connected by the link [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)
already proved can fail without warning.

Deliberately, the Kubernetes control plane stays entirely on-premises. A
control plane split across the VPN link would make every API operation
dependent on link health; keeping it at `HQ` means a VPN failure degrades
scheduling flexibility, not cluster availability — the distinction this
chapter's negative test is built to demonstrate.

### Systems and addressing introduced in this chapter

This chapter adds one subnet to [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s topology manifest: the
`CLOUD1` VPC private subnet, `10.13.90.0/24`, carved from the same lab
supernet so traffic between HQ and the cloud stays [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918)-to-[RFC 1918](https://www.rfc-editor.org/rfc/rfc1918)
across the VPN without NAT.

| Hostname | Role | Address |
| --- | --- | --- |
| `cloud-vpgw01` | Cloud VPN gateway (site-to-site endpoint) | `203.0.113.10` (public, illustrative cloud edge), `10.13.90.1` (VPC gateway) |
| `k8s-cp01` | Kubernetes control plane (on-premises, HQ) | `10.13.20.31` |
| `k8s-wk01` | Kubernetes worker (on-premises, HQ) | `10.13.20.32` |
| `k8s-wk02` | Kubernetes worker (`CLOUD1`) | `10.13.90.31` |

`k8s-cp01` and `k8s-wk01` run as VMs on the `HQ-Cluster` built in Chapter
04; `k8s-wk02` runs as a cloud compute instance inside the `CLOUD1` VPC.

## Design Considerations

- **One cluster, not two clusters joined by a service mesh.** A single
  control plane with geographically split workers is simpler to operate
  for this lab's purposes and directly demonstrates hybrid scheduling; a
  multi-cluster federation pattern is a legitimate alternative [Volume VII](../../volume-07-cloud-infrastructure/README.md),
  [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) discusses, but it solves a different problem (workload
  portability across truly independent clusters) than this chapter targets
  (extending one scheduling domain across a hybrid link).
- **Control plane placement is the single most consequential decision in
  this chapter.** Placing it on-premises trades some cloud elasticity for
  a hard guarantee: the cluster's brain does not depend on the WAN link
  this volume has already shown can fail.
- **Landing zone guardrails before workloads.** Baseline guardrails
  (a restricted default network ACL, mandatory resource tagging, and a
  dedicated IAM role for cluster nodes rather than long-lived static
  credentials) are configured before the first Kubernetes node is created,
  matching the sequencing [Volume VII, Chapter 02](../../volume-07-cloud-infrastructure/chapters/02-landing-zones-resource-organization-and-guardrails.md) recommends — retrofitting
  guardrails onto an already-running environment is materially harder.
- **Topology-aware scheduling, not accidental placement.** Nodes are
  labeled by location (`topology.kubernetes.io/zone=hq` or `=cloud1`) and
  the sample workload uses pod topology spread constraints so replicas are
  deliberately distributed across both locations — without this, the
  scheduler could place every replica in one location by chance, silently
  defeating the point of the exercise.
- **In-cluster platform services, not managed equivalents.** The registry
  and ingress controller run as workloads inside the cluster rather than
  as managed cloud services, keeping the platform surface portable and
  keeping this chapter's lesson focused on Kubernetes-native patterns
  [Volume VIII, Chapter 08](../../volume-08-containers-platform-engineering/chapters/08-internal-developer-platforms-and-platform-products.md) builds on.

## Implementation and Automation

Establish the VPN tunnel from `rtr-hq01` (built in [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)) to
`cloud-vpgw01`, extending the crypto map already configured for the HQ–BR1
tunnel with a second peer:

```text
! rtr-hq01 (additional peer for the cloud VPN)
crypto isakmp key <CLOUD_PSK> address 203.0.113.10
crypto map MERIDIAN-MAP 20 ipsec-isakmp
 set peer 203.0.113.10
 set transform-set MERIDIAN-TS
 match address CLOUD-TRAFFIC
```

Initialize the Kubernetes control plane on `k8s-cp01`:

```bash
sudo kubeadm init --apiserver-advertise-address=10.13.20.31 \
  --pod-network-cidr=192.168.0.0/16 \
  --kubernetes-version=v1.31.0
```

Join both workers, labeling each by location immediately after it joins:

```bash
# On k8s-wk01 (HQ) and k8s-wk02 (CLOUD1), using the join command kubeadm printed
sudo kubeadm join 10.13.20.31:6443 --token <TOKEN> \
  --discovery-token-ca-cert-hash sha256:<HASH>

# From k8s-cp01, after both nodes are Ready
kubectl label node k8s-wk01 topology.kubernetes.io/zone=hq
kubectl label node k8s-wk02 topology.kubernetes.io/zone=cloud1
```

Deploy the sample workload with topology spread constraints so replicas
land in both locations:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meridian-web
spec:
  replicas: 4
  selector:
    matchLabels:
      app: meridian-web
  template:
    metadata:
      labels:
        app: meridian-web
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: meridian-web
      containers:
        - name: web
          image: registry.corp.meridian.example/meridian-web:1.0
          ports:
            - containerPort: 8080
```

## Validation and Troubleshooting

- **VPN and cluster reachability.** Confirm the cloud VPN tunnel is
  established (`show crypto ipsec sa peer 203.0.113.10` on `rtr-hq01`)
  before joining `k8s-wk02` — a worker joined over a tunnel that later
  flaps will produce confusing `NotReady` symptoms that look like a
  Kubernetes problem but are actually a network problem.
- **Node and pod placement.** `kubectl get nodes -L
  topology.kubernetes.io/zone` must show all three nodes `Ready` with the
  correct zone label; `kubectl get pods -o wide` should show
  `meridian-web` replicas spread across both `hq` and `cloud1` nodes, not
  concentrated on one.
- **Common failure: pod network CIDR overlapping lab addressing.** The
  `192.168.0.0/16` pod CIDR used above must not collide with any VLAN or
  VPC subnet in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s topology manifest; if it does, choose a CNI
  pod CIDR outside `10.13.0.0/16` entirely, as done here.
- **Common failure: MTU mismatch across the VPN-plus-overlay path.** As
  flagged generically in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md), a CNI overlay (VXLAN or similar)
  running on top of an already-encapsulated IPsec tunnel to `CLOUD1` can
  silently drop larger packets. Verify with `ping -M do -s 1400
  <cloud-node-pod-ip>` from an on-premises pod before assuming an
  application-layer bug.
- **Ingress and registry reachability.** Confirm `kubectl get ingress` shows
  an assigned address and that `curl` against it returns a response from
  `meridian-web` regardless of which pod answers — the ingress controller,
  not the individual pod, is what callers should depend on.

## Security and Best Practices

- Scope the cloud IAM role attached to `k8s-wk02`'s compute instance to
  only what the node needs (image pull, logging, metrics) — not a broad
  administrative role, consistent with [Volume VII, Chapter 03](../../volume-07-cloud-infrastructure/chapters/03-cloud-identity-access-and-cryptographic-services.md).
- Enforce Kubernetes RBAC and a restrictive default `NetworkPolicy` before
  deploying any workload; an open-by-default cluster network defeats the
  segmentation work planned for [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md).
- Require signed, scanned images from the in-cluster registry before they
  can run — [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) formalizes this as a pipeline policy gate, but the
  registry's access controls should already be correctly scoped by the
  time that gate exists.
- Encrypt the VPN tunnel to `CLOUD1` with the strongest transform set the
  cloud provider's VPN gateway supports, and store the pre-shared key the
  same way [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)'s WAN key is stored — never in a manifest committed
  to the lab's Git history.
- Tag every cloud resource with owner and expiration metadata per Chapter
  01's tagging requirement; an untagged cloud resource is the easiest kind
  of resource to forget during [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md)'s decommissioning exercise.

## References and Knowledge Checks

**References**

- [Volume VII](../../volume-07-cloud-infrastructure/README.md), Chapters 02–04 and 07 — landing zones, cloud identity, cloud
  networking/hybrid connectivity, and hybrid/multicloud architecture.
- [Volume VIII](../../volume-08-containers-platform-engineering/README.md), Chapters 02, 04, and 08 — Kubernetes architecture,
  networking/traffic policy, and internal developer platforms.
- [Volume III, Chapter 04](../../volume-03-cisco-enterprise-networking/chapters/04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md) — Enterprise WAN, Internet Edge, and Catalyst
  SD-WAN (the `rtr-hq01` side of this chapter's VPN).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Kubernetes
  1.31.x and current-GA AWS service-surface baseline used in this chapter.

**Knowledge checks**

1. Why does keeping the Kubernetes control plane entirely on-premises
   change the blast radius of a VPN failure compared to splitting it
   across both locations?
2. What does a topology spread constraint guarantee that a plain
   `replicas: 4` Deployment without it does not?
3. Why must the CNI pod network CIDR avoid `10.13.0.0/16` in this lab
   specifically?
4. Name one guardrail this chapter configures before any workload exists,
   and explain why sequencing matters.

## Hands-On Lab

**Objective:** Build the `CLOUD1` landing zone, connect it to `HQ` over a
VPN, form one Kubernetes cluster spanning both locations, deploy a
topology-aware sample workload, and confirm the cluster degrades safely
when the hybrid link fails.

**Prerequisites**

- [Chapter 04](04-virtualization-storage-and-data-protection-lab.md) complete, with `rtr-hq01` and the `HQ-Cluster` healthy.
- A cloud account/subscription scoped for lab use only, with the
  landing-zone guardrails from [Volume VII, Chapter 02](../../volume-07-cloud-infrastructure/chapters/02-landing-zones-resource-organization-and-guardrails.md) understood.
- Comfort with `kubectl` and basic Kubernetes manifests at the level of
  [Volume VIII, Chapter 02](../../volume-08-containers-platform-engineering/chapters/02-kubernetes-architecture-and-cluster-lifecycle.md).

**Steps**

1. Restore or confirm the `ch04-baseline` state.

2. Create the `CLOUD1` landing zone: a dedicated account/project, the
   `10.13.90.0/24` VPC subnet, baseline guardrails (restricted default
   network ACL, mandatory tagging policy), and `cloud-vpgw01` as the VPN
   attachment point.

3. Extend `rtr-hq01`'s crypto map with the `CLOUD1` peer per Implementation
   and Automation.

4. **Expected result — cloud VPN.**

   ```bash
   ./evidence.sh "ssh admin@rtr-hq01 'show crypto ipsec sa peer 203.0.113.10'"
   ```

   Must show an established SA before continuing.

5. Provision `k8s-cp01` and `k8s-wk01` as VMs on the `HQ-Cluster`, and
   `k8s-wk02` as a compute instance inside the `CLOUD1` VPC.

6. Initialize the control plane on `k8s-cp01` and join both workers per
   Implementation and Automation, labeling each by zone immediately.

7. **Expected result — cluster formed.**

   ```bash
   ./evidence.sh "kubectl get nodes -L topology.kubernetes.io/zone"
   ```

   All three nodes must show `Ready` with the correct zone label.

8. Deploy an in-cluster container registry and ingress controller as
   platform services, then deploy `meridian-web` with the topology spread
   constraint from Implementation and Automation.

9. **Expected result — spread and reachability.**

   ```bash
   ./evidence.sh "kubectl get pods -o wide -l app=meridian-web"
   ./evidence.sh "curl -s http://<ingress-address>/ | head -n 5"
   ```

   Replicas must be present on both `hq`- and `cloud1`-zoned nodes, and
   the `curl` must succeed regardless of which pod answers.

10. Take a snapshot/state export labeled `ch05-baseline` (cluster
    manifests exported via `kubectl get all -A -o yaml`, plus cloud
    landing-zone configuration export).

11. **Negative test:** Fail the cloud VPN tunnel to simulate a hybrid link
    outage:

    ```bash
    ./evidence.sh "ssh admin@rtr-hq01 'no crypto map MERIDIAN-MAP 20'"
    ./evidence.sh "kubectl get nodes -L topology.kubernetes.io/zone"
    ```

    **Expected result:** Within the node-heartbeat timeout, `k8s-wk02`
    transitions to `NotReady`. On-premises nodes (`k8s-cp01`, `k8s-wk01`)
    remain `Ready`, and the Kubernetes control plane keeps responding to
    `kubectl` commands throughout — because it never depended on the VPN.

12. Confirm workload continuity:

    ```bash
    ./evidence.sh "kubectl get pods -o wide -l app=meridian-web"
    ./evidence.sh "curl -s http://<ingress-address>/ | head -n 5"
    ```

    **Expected result:** Pods that were on `k8s-wk02` are rescheduled
    (once their grace period expires) onto `k8s-wk01`, and `meridian-web`
    continues answering requests throughout — degraded scheduling
    flexibility, not an outage.

13. **Recovery:** Restore the crypto map entry on `rtr-hq01`, confirm the
    tunnel re-establishes, and confirm `k8s-wk02` returns to `Ready`:

    ```bash
    ./evidence.sh "ssh admin@rtr-hq01 'crypto map MERIDIAN-MAP 20 ipsec-isakmp'"
    ./evidence.sh "kubectl get nodes -L topology.kubernetes.io/zone"
    ```

14. **Cleanup:** No teardown — the cluster and landing zone are retained
    for Chapters 06–09. Commit the updated topology record:

    ```bash
    cd ~/vol13-lab
    git add topology.yml
    git commit -m "Chapter 05: hybrid cloud, Kubernetes, and platform services"
    ```

## Summary and Completion Checklist

This chapter turned `CLOUD1` from a name in a topology manifest into a
real landing zone, connected it to `HQ` over a VPN, and joined it to a
single Kubernetes cluster with an on-premises control plane. The negative
test proved that keeping the control plane on-premises limits a hybrid
link failure to reduced scheduling flexibility rather than a cluster-wide
outage — and that topology-aware scheduling is what made the workload's
recovery automatic rather than manual.

- [ ] Built the `CLOUD1` landing zone with guardrails in place before any
      workload existed.
- [ ] Formed one Kubernetes cluster spanning on-premises and cloud
      workers with an on-premises-only control plane.
- [ ] Deployed platform services (registry, ingress) and a topology-aware
      sample workload.
- [ ] Verified workload placement and reachability across both locations.
- [ ] Completed the VPN-failure negative test and confirmed graceful
      degradation and recovery.
