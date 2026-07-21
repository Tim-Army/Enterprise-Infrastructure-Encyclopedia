# Chapter 04: Kubernetes Networking, Service Delivery, and Traffic Policy

![Lab topology for this chapter: client and server pods in the netpol-lab namespace initially reach each other freely, with no NetworkPolicy in place. A default-deny-all policy is applied; the same request now times out and fails, confirming Calico is actually enforcing the policy rather than it being merely configured. A scoped allow-client-to-server policy permitting only that pair on port 8080 is then added; connectivity is restored for exactly that path, while any other pod added later to the namespace remains denied by default.](../../../diagrams/volume-08-containers-platform-engineering/chapter-04-networkpolicy-default-deny-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: a NetworkPolicy default-deny baseline enforced by Calico, then narrowed back open with a single scoped allow rule.*

## Learning Objectives

- Explain the Kubernetes networking model's four addressing problems and
  how the Container Network Interface (CNI) satisfies them.
- Differentiate Service types (`ClusterIP`, `NodePort`, `LoadBalancer`,
  `ExternalName`, headless) and trace how EndpointSlices connect a Service
  to backing pods.
- Compare kube-proxy's `iptables`, `IPVS`, and `nftables` modes against an
  eBPF-based kube-proxy replacement, and explain the trade-offs.
- Choose between Ingress and the Gateway API for north-south traffic, and
  configure `NetworkPolicy` for east-west segmentation.
- Explain when a service mesh's mTLS and traffic-shaping capabilities
  justify its added operational surface, including the sidecar vs.
  ambient data-plane trade-off.

## Theory and Architecture

The Kubernetes networking model rests on a small set of hard requirements
defined by the API, deliberately silent on *how* any particular CNI plugin
satisfies them:

- Every pod gets its own IP address; no port mapping is required between
  containers in the same pod (they share a network namespace) or between
  pods.
- Pods can reach all other pods' IPs across the entire cluster without
  Network Address Translation (NAT), regardless of which node they run
  on.
- A node can reach every pod on that node without NAT.
- The IP a pod sees itself as is the same IP everyone else sees it as.

Satisfying "any pod reaches any pod, cluster-wide, without NAT" is the
**CNI plugin's** job. Implementations diverge sharply in mechanism:
overlay networks (Flannel VXLAN, Calico IP-in-IP) encapsulate pod traffic
inside a tunnel between nodes, trading a small per-packet overhead for
independence from the underlying network's routing; native-routed
implementations (Calico BGP mode, Cilium's native routing mode) instead
advertise pod CIDRs into the underlying network's routing table directly,
avoiding encapsulation overhead at the cost of needing routing
cooperation from the physical or cloud network fabric. **Cilium**, built
on eBPF, additionally replaces large parts of the traditional CNI plus
kube-proxy stack with in-kernel programs attached at multiple hook points,
which is why it is discussed separately below rather than as just another
overlay option.

### Services, EndpointSlices, and kube-proxy

A pod's IP is not a stable address — pods are replaced constantly by
their controllers ([Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md)). The **Service** object provides the
stable address and load-balancing abstraction pods rely on instead:

| Service type | Address scope | Typical use |
| --- | --- | --- |
| `ClusterIP` (default) | Virtual IP, cluster-internal only | Internal service-to-service traffic |
| `NodePort` | `ClusterIP` plus a port (30000-32767) opened on every node | Simple external access without a cloud load balancer |
| `LoadBalancer` | `NodePort` plus cloud-provisioned external load balancer (via cloud-controller-manager, [Chapter 02](02-kubernetes-architecture-and-cluster-lifecycle.md)) | External access with cloud-native L4 load balancing |
| `ExternalName` | DNS `CNAME` to an external name, no proxying | Referencing an external dependency by an in-cluster name |
| Headless (`clusterIP: None`) | No virtual IP; DNS returns pod IPs directly | StatefulSet peer discovery, client-side load balancing |

A Service's backing pods are tracked through **EndpointSlices**
(`discovery.k8s.io/v1`), which superseded the monolithic `Endpoints`
object as the default: EndpointSlices shard large backend sets across
multiple objects (capped around 100 addresses each) so a single pod
churn event does not force every node's kube-proxy to reprocess a
cluster-wide list, and they carry topology hints used for
topology-aware/zone-aware routing.

**kube-proxy** watches Services and EndpointSlices and programs each
node's dataplane so traffic to a `ClusterIP` reaches a real pod:

- **iptables mode** (long-time default) — programs DNAT rules; scales
  reasonably to a few thousand Services but rule evaluation is O(n) and
  large rule sets add tail latency and slow rule-table reprogramming
  under high Service churn.
- **IPVS mode** — uses the kernel's IP Virtual Server, a purpose-built L4
  load balancer with O(1) lookup regardless of Service count; the correct
  choice at very large Service counts where iptables rule evaluation
  becomes a bottleneck.
- **nftables mode** — the iptables successor framework in the Linux
  kernel; at the 1.31.x baseline this mode is beta, offering better rule
  update performance than legacy iptables without requiring IPVS's kernel
  modules.

**Cilium's kube-proxy replacement** bypasses this layer entirely: eBPF
programs attached to the CNI's network interfaces perform Service
load-balancing directly at the earliest possible packet-processing point
(often before the packet reaches the normal netfilter path), which both
removes kube-proxy as a component and, in benchmarks, reduces both
latency and CPU cost at high Service and connection-churn rates. The
trade-off is operational: eBPF dataplane behavior is debugged with
different tools (`cilium monitor`, `hubble`) than the `iptables-save`
familiarity most engineers already have.

### North-south routing: Ingress and the Gateway API

**Ingress** (`networking.k8s.io/v1`) is a stable, widely implemented API
for HTTP(S) routing into the cluster: host/path-based rules, TLS
termination, and a pluggable **Ingress controller** (ingress-nginx,
Traefik, HAProxy, or a cloud provider's own controller) that actually
implements the routing. Ingress's API surface is intentionally narrow —
it standardized only the common case, pushing anything more advanced
(traffic splitting, header-based routing, protocol support beyond HTTP)
into controller-specific annotations that are not portable between
implementations.

The **Gateway API** (a separate, more expressive API group —
`gateway.networking.k8s.io`) is the standardized successor path: `Gateway`
resources represent a listener (protocol, port, TLS config) provisioned
by a `GatewayClass`, and route resources (`HTTPRoute`, `GRPCRoute`,
`TCPRoute`) attach to a `Gateway` with rich, portable matching and traffic
weighting, plus a role-oriented design that lets infrastructure teams own
the `Gateway` while application teams own their own `HTTPRoute` objects.
The core resource kinds reached GA (v1) ahead of the 1.31.x baseline and
Gateway API implementations exist for most major ingress controllers and
service meshes; it does not replace Ingress overnight in a given
environment, but it is the direction new traffic-routing investment
should take.

### East-west segmentation: NetworkPolicy

`NetworkPolicy` (`networking.k8s.io/v1`) is a **default-allow, opt-in
deny** model at the namespace/pod level: with zero NetworkPolicy objects
selecting a pod, all traffic is allowed; the moment one NetworkPolicy
selects a pod for a given direction (ingress or egress), that direction
becomes default-deny except for what the policy explicitly permits.
Crucially, `NetworkPolicy` is only enforced if the CNI plugin implements
it — the reference `kubenet`/basic bridge networking does not, while
Calico, Cilium, and most production CNIs do.

## Design Considerations

**Overlay vs. native routing is a network-ownership decision.** An
overlay decouples pod networking from the physical/cloud network
entirely, which is attractive when the platform team does not control
routing on the underlying fabric (shared or restrictive cloud VPC
routing, multi-tenant physical networks). Native routing removes
encapsulation overhead and makes pod traffic visible to existing network
tooling (firewalls, flow logs, packet captures) as ordinary routed
traffic, but requires routing cooperation — BGP peering with the
network's routers, or a cloud VPC's native pod-CIDR routing support (as
used by GKE's VPC-native clusters and comparable AWS/Azure CNI modes).

**kube-proxy mode selection should track Service count and churn, not
habit.** iptables mode remains adequate for most clusters under roughly
a thousand Services with moderate churn. IPVS earns its complexity at
larger Service counts. A full eBPF replacement (Cilium) is the strongest
choice for very high connection-churn workloads (serverless-style,
autoscaled-to-zero microservices) or when the mesh and CNI are already
consolidating onto Cilium's `hubble` observability stack — but it is a
CNI-level architectural choice, not a flag you flip independently of
which CNI plugin the cluster runs.

**Choose Ingress or Gateway API based on how much routing expressiveness
and multi-team ownership the environment needs today, but design new
platform tooling against the Gateway API.** A single-team cluster with
simple host-based routing gains little from Gateway API's added resource
types. A platform serving many application teams behind a shared entry
point benefits immediately from Gateway API's role separation — platform
engineers manage `Gateway`/`GatewayClass`, application teams self-serve
`HTTPRoute` objects in their own namespaces without needing access to the
shared listener configuration ([Chapter 08](08-internal-developer-platforms-and-platform-products.md) returns to this
platform/tenant boundary in depth).

**NetworkPolicy default-allow means segmentation is opt-in, not
automatic.** A cluster with no NetworkPolicy objects has flat, fully open
pod-to-pod networking regardless of namespace boundaries. A namespace's
security posture should include, at minimum, a default-deny-all baseline
policy per namespace with explicit allow rules layered on top — an
"implicit trust" cluster network is a common finding in security reviews
of otherwise well-hardened clusters ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md) covers this alongside
RBAC and admission policy as part of the same defense-in-depth posture).

**A service mesh trades operational surface for uniform mTLS, retries,
and traffic shaping independent of application code.** The classic
sidecar model (Istio, Linkerd) injects a proxy container into every pod,
giving per-pod policy enforcement and telemetry at the cost of a proxy
container (and its resource footprint) multiplying with pod count.
**Ambient mode** (Istio Ambient, Cilium Service Mesh) moves L4
encryption/identity enforcement to a per-node component and layers
optional per-namespace L7 processing only where needed, substantially
reducing the sidecar tax for services that only need mTLS and basic
authorization without full L7 policy. The decision to adopt a mesh at all
should be driven by a concrete requirement — mandatory mTLS between
services, fine-grained traffic shifting for progressive delivery
([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)), or uniform retry/circuit-breaking policy — rather than
adopted by default, since every mesh adds a control plane, a certificate
lifecycle, and a new failure domain to operate.

## Implementation and Automation

### Service types and headless discovery

```yaml
apiVersion: v1
kind: Service
metadata:
  name: checkout-api
  namespace: payments
spec:
  type: ClusterIP
  selector: { app: checkout-api }
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: order-db
  namespace: payments
spec:
  clusterIP: None          # headless: DNS returns pod IPs directly
  selector: { app: order-db }
  ports:
    - port: 5432
```

```bash
# EndpointSlices backing a Service — the object kube-proxy actually watches.
kubectl get endpointslices -n payments -l kubernetes.io/service-name=checkout-api

# Headless-service DNS resolves to individual pod A/AAAA records, one per
# ready pod — this is how StatefulSet peers discover each other by ordinal.
kubectl run dns-test -n payments --rm -it --restart=Never --image=busybox:1.36 \
  -- nslookup order-db.payments.svc.cluster.local
```

### Ingress and Gateway API side by side

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: checkout-api
  namespace: payments
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
    - host: checkout.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: checkout-api
                port: { number: 80 }
  tls:
    - hosts: ["checkout.example.com"]
      secretName: checkout-tls
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: platform-gateway
  namespace: platform-ingress
spec:
  gatewayClassName: cilium
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs: [{ name: wildcard-example-com-tls }]
      allowedRoutes:
        namespaces: { from: All }
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: checkout-api
  namespace: payments
spec:
  parentRefs:
    - name: platform-gateway
      namespace: platform-ingress
  hostnames: ["checkout.example.com"]
  rules:
    - backendRefs:
        - name: checkout-api
          port: 80
```

The Gateway API example shows the ownership split directly: the platform
team owns `platform-gateway` in a shared namespace, while the `payments`
team self-serves its own `HTTPRoute` without needing write access to the
shared listener at all.

### Default-deny NetworkPolicy with explicit allows

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: payments
spec:
  podSelector: {}
  policyTypes: ["Ingress", "Egress"]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-checkout-to-order-db
  namespace: payments
spec:
  podSelector:
    matchLabels: { app: order-db }
  policyTypes: ["Ingress"]
  ingress:
    - from:
        - podSelector: { matchLabels: { app: checkout-api } }
      ports:
        - protocol: TCP
          port: 5432
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: payments
spec:
  podSelector: {}
  policyTypes: ["Egress"]
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
```

Every default-deny namespace needs an explicit DNS-egress allow rule —
without one, pods can neither resolve internal Service names nor external
hosts, a frequent first surprise when rolling out default-deny policies.

## Validation and Troubleshooting

```bash
# Confirm kube-proxy's active mode on a node.
kubectl logs -n kube-system -l k8s-app=kube-proxy --tail=20 | grep -i "proxy mode"

# For a Cilium-based cluster, confirm kube-proxy replacement is active.
cilium status | grep -i "kubeproxyreplacement"

# Trace whether a NetworkPolicy is actually blocking traffic (Cilium).
cilium monitor --type drop

# Confirm a Service resolves and load-balances across all expected pods.
kubectl run curl-test -n payments --rm -it --restart=Never --image=curlimages/curl:8.10.1 \
  -- curl -s -o /dev/null -w '%{http_code}\n' http://checkout-api.payments.svc.cluster.local
```

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| Pod cannot reach a Service it should be allowed to reach | A `NetworkPolicy` default-deny with no matching allow rule, or missing DNS-egress allow | `kubectl get networkpolicy -n <namespace>`; test with a temporary policy-free namespace to isolate |
| `LoadBalancer` Service stuck `<pending>` external IP | cloud-controller-manager cannot provision (quota, IAM permission, unsupported cloud) | `kubectl describe svc`; cloud-controller-manager logs |
| Ingress returns 404 for a known-good path | `ingressClassName` mismatch, or Ingress controller has not reconciled the object | `kubectl get ingressclass`; Ingress controller logs |
| Intermittent connection resets at high Service churn | iptables rule-table reprogramming lag under heavy churn | Compare against IPVS/nftables/eBPF mode; check kube-proxy sync duration metrics |
| StatefulSet peers cannot discover each other by hostname | Governing Service is not headless, or pod is not yet `Ready` | `kubectl get svc -o yaml \| grep clusterIP`; confirm `clusterIP: None` |

## Security and Best Practices

- Treat a cluster with no `NetworkPolicy` objects as flat and fully open;
  deploy a default-deny-all baseline per namespace and layer explicit
  allow rules on top, rather than relying on Service-level access alone.
- Always include an explicit DNS-egress allow rule in any default-deny
  namespace; forgetting it is the most common self-inflicted outage when
  adopting NetworkPolicy.
- Terminate TLS at the Ingress/Gateway edge at minimum, and use a service
  mesh's mutual TLS when pod-to-pod traffic itself must be encrypted and
  cryptographically authenticated, not just network-segmented.
- Prefer the Gateway API's role-oriented ownership model for any platform
  serving multiple application teams, so application teams cannot
  accidentally modify shared listener or TLS configuration.
- Avoid `NodePort` for anything but small or lab environments; it opens a
  port on every node's host network and provides none of a
  `LoadBalancer`'s health-checked, provider-managed load balancing.
- If adopting an eBPF kube-proxy replacement, validate kernel version and
  feature-gate compatibility with target nodes before rollout — eBPF
  capability varies meaningfully across kernel versions.
- Scope a service mesh's mTLS enforcement to `STRICT` mode only after
  confirming every namespace's workloads are mesh-enrolled; a mixed
  `PERMISSIVE` rollout is the safe default during migration to avoid
  silently dropping legitimate unencrypted traffic from not-yet-enrolled
  services.

## References and Knowledge Checks

**Authoritative references**

- Kubernetes documentation, [Cluster Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) and [Service](https://kubernetes.io/docs/concepts/services-networking/service/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- Kubernetes documentation, [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
- Kubernetes SIG Network, [Gateway API](https://gateway-api.sigs.k8s.io/).
- Cilium documentation, [eBPF-based Networking, Observability, and Security](https://docs.cilium.io/).
- Istio project documentation, [Ambient Mesh](https://istio.io/latest/docs/ambient/).

**Knowledge check**

1. What four guarantees does the Kubernetes networking model require, and
   why does satisfying them fall to the CNI plugin rather than to
   Kubernetes core?
2. Why did EndpointSlices replace the monolithic `Endpoints` object as the
   default, and what problem does sharding solve?
3. Under what conditions does IPVS or an eBPF kube-proxy replacement
   materially outperform the default iptables mode?
4. What does a `NetworkPolicy`'s default-allow-until-selected model mean
   for a namespace that has zero NetworkPolicy objects applied to it?
5. What ownership problem does the Gateway API's `Gateway`/`HTTPRoute`
   split solve that a single shared Ingress object does not?

## Hands-On Lab

**Objective:** Deploy two workloads in the same namespace, confirm they
can reach each other with no policy in place, apply a default-deny
baseline with explicit allows, and prove the deny is actually enforced
with a negative test.

### Prerequisites

- A `kind` cluster whose CNI enforces `NetworkPolicy`. Default `kindnet`
  does **not** enforce NetworkPolicy, so this lab installs Calico.
- `kubectl` matching the 1.31.x baseline.

### Procedure

1. Create a cluster with the default CNI disabled, then install Calico so
   NetworkPolicy is actually enforced.

   ```bash
   cat > kind-config.yaml <<'EOF'
   kind: Cluster
   apiVersion: kind.x-k8s.io/v1alpha4
   networking:
     disableDefaultCNI: true
   nodes:
     - role: control-plane
     - role: worker
   EOF
   kind create cluster --name netpol-lab --config kind-config.yaml --image kindest/node:v1.31.4
   kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/calico.yaml
   kubectl wait --for=condition=Ready pods -l k8s-app=calico-node -n kube-system --timeout=180s
   ```

2. Deploy a client and a server pod plus a Service for the server.

   ```bash
   kubectl create namespace netpol-lab
   kubectl run server -n netpol-lab --image=registry.k8s.io/e2e-test-images/agnhost:2.53 \
     --labels="app=server" -- netexec --http-port=8080
   kubectl expose pod server -n netpol-lab --port=80 --target-port=8080
   kubectl run client -n netpol-lab --image=curlimages/curl:8.10.1 \
     --labels="app=client" --command -- sleep infinity
   kubectl wait --for=condition=Ready pod/server pod/client -n netpol-lab --timeout=60s
   ```

3. Confirm open connectivity before any policy exists.

   ```bash
   kubectl exec -n netpol-lab client -- curl -s -o /dev/null -w '%{http_code}\n' http://server
   ```

   **Expected result:** `200`.

4. Apply a default-deny-all policy for the namespace.

   ```bash
   cat > default-deny.yaml <<'EOF'
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: default-deny-all
     namespace: netpol-lab
   spec:
     podSelector: {}
     policyTypes: ["Ingress", "Egress"]
   EOF
   kubectl apply -f default-deny.yaml
   ```

### Negative test

5. Re-test connectivity and confirm it now fails.

   ```bash
   kubectl exec -n netpol-lab client -- curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://server || echo "connection blocked as expected"
   ```

   **Expected result:** the `curl` call times out and the command exits
   non-zero, printing `connection blocked as expected` — the default-deny
   policy is now enforced by Calico.

6. Add a scoped allow rule for exactly `client -> server` on port 8080 and
   confirm connectivity is restored for that path only.

   ```bash
   cat > allow-client-to-server.yaml <<'EOF'
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-client-to-server
     namespace: netpol-lab
   spec:
     podSelector:
       matchLabels: { app: server }
     policyTypes: ["Ingress"]
     ingress:
       - from:
           - podSelector: { matchLabels: { app: client } }
         ports:
           - protocol: TCP
             port: 8080
   EOF
   kubectl apply -f allow-client-to-server.yaml
   kubectl exec -n netpol-lab client -- curl -s -o /dev/null -w '%{http_code}\n' http://server
   ```

   **Expected result:** `200` — connectivity is restored for the
   explicitly allowed path, while any other pod that might be added to
   the namespace remains denied by default.

### Cleanup

```bash
kubectl delete namespace netpol-lab
kind delete cluster --name netpol-lab
rm -f kind-config.yaml default-deny.yaml allow-client-to-server.yaml
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Kubernetes networking guarantees a flat, NAT-free pod address space and
leaves the mechanism to the CNI plugin, ranging from simple overlays to
eBPF-based dataplanes that can replace kube-proxy entirely. Services and
EndpointSlices provide stable addressing over an unstable pod population;
Ingress and the Gateway API handle north-south entry, with Gateway API's
role separation the better fit for multi-team platforms; NetworkPolicy
provides east-west segmentation that is opt-in and only as strong as the
CNI's enforcement and the completeness of a namespace's allow rules. A
service mesh adds uniform mTLS and traffic shaping at the cost of a new
control plane, and the sidecar-vs-ambient choice is primarily a
resource-footprint and operational-complexity trade-off.

- [ ] Can explain the Kubernetes networking model's core guarantees and
      the CNI plugin's role in satisfying them.
- [ ] Can differentiate Service types and explain how EndpointSlices back
      them.
- [ ] Can compare kube-proxy modes and an eBPF kube-proxy replacement.
- [ ] Can choose between Ingress and Gateway API and configure a
      default-deny NetworkPolicy baseline with explicit allows.
- [ ] Can explain the sidecar-vs-ambient service mesh trade-off.
- [ ] Completed the hands-on lab, including the default-deny negative
      test, and performed cleanup.
