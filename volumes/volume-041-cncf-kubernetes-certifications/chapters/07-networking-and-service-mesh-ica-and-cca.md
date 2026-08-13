# Chapter 07: Networking and Service Mesh — ICA and CCA

## Learning Objectives

- Explain the two networking associate credentials: ICA (Istio) and CCA (Cilium).
- List the ICA and CCA domains and their exam weights.
- Distinguish the performance-based ICA from the multiple-choice CCA.
- Apply service-mesh (traffic, security) and eBPF-networking (policy, observability) skills.
- Complete a per-domain walkthrough for every ICA and CCA domain.

## Theory and Architecture

Two projects dominate cloud-native networking, each with a CNCF associate:

- **Istio Certified Associate (ICA)** — the **service mesh** credential.
  **Performance-based**, two hours, mixing hands-on tasks with questions. Four
  weighted domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Installation, Upgrade & Configuration | 20% |
  | 2 | Traffic Management | 35% |
  | 3 | Securing Workloads | 25% |
  | 4 | Troubleshooting | 20% |

- **Cilium Certified Associate (CCA)** — the **eBPF networking, security, and
  observability** credential. Multiple-choice. Eight weighted domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Architecture | 20% |
  | 2 | Network Policy | 18% |
  | 3 | Service Mesh | 16% |
  | 4 | Network Observability | 10% |
  | 5 | Installation and Configuration | 10% |
  | 6 | Cluster Mesh | 10% |
  | 7 | eBPF | 10% |
  | 8 | BGP and External Networking | 6% |

**Traffic Management (35%)** anchors ICA; **Architecture (20%)** and **Network
Policy (18%)** lead CCA.

## Design Considerations

**Istio** operates at L7 with sidecar or **ambient** proxies, giving fine traffic
control (routing, retries, fault injection) and workload identity (**mTLS**).
**Cilium** operates in the kernel via **eBPF**, giving high-performance
networking, **NetworkPolicy** (including L7), **Hubble** observability, cluster
mesh, and BGP. ICA is hands-on, so drill `istioctl`, VirtualServices, and
DestinationRules; CCA is knowledge-based, so understand the eBPF datapath and
Cilium's policy and observability model.

## Implementation and Automation

The labs below use `istioctl` and Istio CRDs (ICA) and Cilium CLI / policy
reasoning (CCA). Where a full mesh install is impractical, the manifests and
concepts are shown so they can be studied without a running mesh.

## Validation and Troubleshooting

Confirm both blueprints before studying:

```text
training.linuxfoundation.org > ICA and CCA > curricula:
  - ICA: four domains (20/35/25/20), performance-based, traffic-heavy
  - CCA: eight domains (20/18/16/10/10/10/10/6), multiple-choice
```

Common pitfalls: forgetting **sidecar injection** so Istio config has no effect;
confusing a **VirtualService** (routing) with a **DestinationRule** (subsets/
policies); and, for Cilium, conflating standard Kubernetes **NetworkPolicy** with
Cilium's richer **CiliumNetworkPolicy** (L7-aware).

## Security and Best Practices

Default to **mTLS STRICT** in Istio for workload-to-workload encryption and
identity; default-deny with **NetworkPolicy** in Cilium and add **L7** rules
where needed; and turn on **observability** (Istio telemetry, Cilium **Hubble**)
so traffic is visible. Keep the mesh/CNI version current.

## References and Knowledge Checks

- training.linuxfoundation.org: *ICA* and *CCA* curricula; istio.io; cilium.io / docs.

**Knowledge checks**

1. Which ICA domain is heaviest, and what does it cover?
2. What does eBPF let Cilium do that a traditional CNI cannot easily?
3. What is the difference between a VirtualService and a DestinationRule?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted ICA and CCA domain**.

**Shared prerequisites** — the `kind`/`minikube` cluster from Chapter 01,
`kubectl`, and (for ICA) `istioctl`; a Linux shell with `python3`. **Cost:**
none.

### ICA — Istio Certified Associate

### Lab 7.1 — ICA: Installation, Upgrade & Configuration (20%)

**Objective:** Install Istio and verify sidecar injection is enabled.

```bash
istioctl install --set profile=demo -y 2>/dev/null || echo "(install step)"
kubectl label namespace default istio-injection=enabled --overwrite
kubectl get namespace default --show-labels | grep istio-injection
```

**Expected result:** the `default` namespace labeled `istio-injection=enabled`
— pods created here now get an Envoy sidecar, the prerequisite for all mesh
features (ICA Domain 1).

**Negative test:** apply Istio traffic rules in a namespace without injection;
with no sidecar, the rules do nothing — enable injection first.

**Rollback:** `kubectl label namespace default istio-injection- --overwrite`

### Lab 7.2 — ICA: Traffic Management (35%)

**Objective:** Route traffic with a VirtualService and DestinationRule (subsets).

```bash
cat <<'YAML'
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata: {name: reviews}
spec:
  host: reviews
  subsets: [{name: v1, labels: {version: v1}}, {name: v2, labels: {version: v2}}]
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: {name: reviews}
spec:
  hosts: [reviews]
  http: [{route: [{destination: {host: reviews, subset: v1}, weight: 90},
                  {destination: {host: reviews, subset: v2}, weight: 10}]}]
YAML
echo "90/10 canary split v1/v2 — traffic management, ICA's heaviest domain."
```

**Expected result:** a DestinationRule defining subsets and a VirtualService
splitting 90/10 across them — the weighted routing/canary pattern of ICA Domain 2.

**Negative test:** reference a `subset` in a VirtualService with no matching
DestinationRule; the subset is undefined — define subsets in the DestinationRule.

**Rollback:** delete the VirtualService/DestinationRule if applied.

### Lab 7.3 — ICA: Securing Workloads (25%)

**Objective:** Enforce mesh-wide mutual TLS (STRICT).

```bash
cat <<'YAML'
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: {name: default, namespace: istio-system}
spec: {mtls: {mode: STRICT}}
YAML
echo "STRICT mTLS: only mutually-authenticated, encrypted traffic between sidecars."
```

**Expected result:** a `PeerAuthentication` enforcing STRICT mTLS mesh-wide —
workload identity and encryption, ICA Domain 3.

**Negative test:** rely on `PERMISSIVE` mode in production; it also accepts
plaintext — use STRICT once all workloads are meshed.

**Rollback:** delete the PeerAuthentication if applied.

### Lab 7.4 — ICA: Troubleshooting (20%)

**Objective:** Diagnose mesh config with `istioctl`.

```bash
istioctl analyze 2>/dev/null || echo "(istioctl analyze checks config for issues)"
echo "Also: istioctl proxy-config routes/clusters <pod> ; check sidecar readiness"
```

**Expected result:** `istioctl analyze` output (or the concept) plus the
proxy-config commands — the mesh-troubleshooting workflow of ICA Domain 4.

**Negative test:** debug with `kubectl` alone; mesh problems live in the **Envoy
sidecar config** — use `istioctl proxy-config` and `analyze`.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### CCA — Cilium Certified Associate

### Lab 7.5 — CCA: Architecture (20%)

**Objective:** Describe Cilium's eBPF datapath and identity model.

```bash
python3 - <<'PY'
print("Cilium: CNI using eBPF programs in the kernel datapath (no per-packet iptables).")
print("Identity: security identity derived from labels, not IP — policy follows workloads.")
print("Components: cilium-agent (per node), operator, Hubble (observability).")
PY
```

**Expected result:** the eBPF datapath, label-based identity, and core components
— the architecture that leads CCA (Domain 1).

**Negative test:** assume policy is enforced by IP; Cilium uses **label-derived
identity**, so policy survives pod IP churn — think identity, not IP.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.6 — CCA: Network Policy (18%)

**Objective:** Write an L7-aware CiliumNetworkPolicy.

```bash
cat <<'YAML'
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata: {name: allow-get-api}
spec:
  endpointSelector: {matchLabels: {app: api}}
  ingress:
  - fromEndpoints: [{matchLabels: {app: web}}]
    toPorts: [{ports: [{port: "80", protocol: TCP}],
               rules: {http: [{method: "GET", path: "/v1/.*"}]}}]
YAML
echo "L7 rule: web may only GET /v1/* on api — beyond standard L3/L4 NetworkPolicy."
```

**Expected result:** a CiliumNetworkPolicy allowing only `GET /v1/*` from `web`
to `api` — L7-aware policy, a Cilium differentiator (CCA Domain 2).

**Negative test:** expect a standard Kubernetes NetworkPolicy to filter by HTTP
method/path; it is L3/L4 only — use a **CiliumNetworkPolicy** for L7.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.7 — CCA: Service Mesh (16%)

**Objective:** Describe Cilium's sidecar-free service mesh.

```bash
python3 - <<'PY'
print("Cilium mesh: eBPF + per-node Envoy (no per-pod sidecar) -> lower overhead.")
print("Provides L7 traffic management, mTLS (WireGuard/IPsec transparent encryption), and observability.")
PY
```

**Expected result:** the sidecar-free mesh model and transparent encryption —
Cilium's service-mesh approach (CCA Domain 3), contrasted with Istio's sidecars.

**Negative test:** assume every mesh needs per-pod sidecars; Cilium's eBPF model
avoids them — know both architectures.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.8 — CCA: Network Observability (10%)

**Objective:** Describe Hubble flow visibility.

```bash
cilium hubble enable 2>/dev/null || echo "(Hubble provides flow-level observability)"
echo "hubble observe --namespace default   # per-flow: identities, verdict (FORWARDED/DROPPED), L7"
```

**Expected result:** the Hubble observability concept and `hubble observe`
pattern — per-flow visibility with policy verdicts (CCA Domain 4).

**Negative test:** debug drops by guesswork; **Hubble** shows the exact flow and
whether policy `DROPPED` it — observe, don't guess.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.9 — CCA: Installation and Configuration (10%)

**Objective:** Check Cilium status and connectivity.

```bash
cilium status 2>/dev/null || echo "(cilium status shows agent/operator health)"
cilium connectivity test 2>/dev/null | head -3 || echo "(connectivity test validates the datapath)"
```

**Expected result:** Cilium agent/operator health and a connectivity-test summary
— the install-and-verify workflow of CCA Domain 5.

**Negative test:** assume the CNI is healthy because pods have IPs; run `cilium
status` and the **connectivity test** to confirm the datapath.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.10 — CCA: Cluster Mesh (10%)

**Objective:** Describe multi-cluster service connectivity.

```bash
python3 - <<'PY'
print("Cluster Mesh: connect multiple clusters into one policy/identity/service domain.")
print("Global services: a Service marked global load-balances across clusters.")
print("Requires unique cluster IDs and non-overlapping (or routable) pod CIDRs.")
PY
```

**Expected result:** the Cluster Mesh model — global services and the identity/
CIDR requirements (CCA Domain 6).

**Negative test:** overlap pod CIDRs across clusters and expect mesh to work;
CIDRs must be routable/unique — plan addressing first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.11 — CCA: eBPF (10%)

**Objective:** Explain what eBPF is and why Cilium uses it.

```bash
python3 - <<'PY'
print("eBPF: run sandboxed programs in the Linux kernel on events (packets, syscalls) safely.")
print("Cilium uses eBPF for routing, load-balancing, policy, and observability -")
print("bypassing much of iptables for performance and per-identity enforcement.")
PY
```

**Expected result:** a correct explanation of eBPF and its role in Cilium — the
technology domain of CCA (Domain 7).

**Negative test:** describe eBPF as a userspace proxy; it runs **in the kernel**
— that is the source of its performance.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.12 — CCA: BGP and External Networking (6%)

**Objective:** Describe advertising service/pod routes via BGP.

```bash
python3 - <<'PY'
print("Cilium BGP: advertise LoadBalancer/pod CIDRs to the physical network via BGP peers.")
print("Enables on-prem external reachability without a cloud load balancer.")
PY
```

**Expected result:** the BGP advertisement model for external reachability — the
smallest CCA domain (Domain 8), important for on-prem/bare-metal.

**Negative test:** assume a cloud LoadBalancer exists on bare metal; on-prem you
advertise routes with **BGP** (or use MetalLB) instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cloud-native networking is certified by **ICA** (Istio; four domains
20/35/25/20, performance-based, traffic-heavy) and **CCA** (Cilium; eight domains
led by Architecture and Network Policy, multiple-choice). Istio is an L7 sidecar/
ambient mesh; Cilium is eBPF-based networking, security, and observability — two
complementary models of the same problem.

- [ ] I can list the ICA and CCA domains and their weights.
- [ ] I can split traffic and enforce mTLS in Istio.
- [ ] I can write an L7 CiliumNetworkPolicy and explain eBPF.
- [ ] I can describe Hubble, Cluster Mesh, and BGP external networking.
- [ ] I completed Labs 7.1–7.12 including each negative test.
