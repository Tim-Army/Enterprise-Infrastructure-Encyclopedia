# Chapter 08: Cloud-Native and Kubernetes Microsegmentation

## Learning Objectives

- Use cloud-native controls (security groups, NSGs, firewall rules) for segmentation.
- Write a Kubernetes NetworkPolicy.
- Reason about Calico and Cilium (eBPF) enforcement.
- State the pros, cons, compatibility, and requirements.
- Complete a walkthrough for each cloud/Kubernetes topic.

## Theory and Architecture

Public clouds and Kubernetes provide **native** microsegmentation without a third-party product.
**Cloud-native:** **AWS security groups** (stateful, instance-level allowlists) and **network ACLs**
(subnet-level, stateless); **Azure network security groups (NSGs)** with **application security groups
(ASGs)** for tag-like grouping; and **GCP firewall rules** keyed by network **tags** and **service
accounts**. These are free, agentless, and provider-integrated — but **cloud-only**, often **coarse**
(instance/subnet), and **siloed per cloud**. **Kubernetes:** the built-in **NetworkPolicy** object
selects pods by **label** and allows ingress/egress only from matching peers — enforced by the **CNI**.
Default Kubernetes is allow-all between pods; a NetworkPolicy that selects pods flips them to
**default-deny** for the specified direction. Richer enforcement comes from CNIs: **Calico**
(NetworkPolicy plus GlobalNetworkPolicy, and WireGuard encryption) and **Cilium** (**eBPF**-based,
identity-aware L3–L7 policy with the **Hubble** observability layer). This chapter covers both with real
commands.

## Pros, Cons, Compatibility, and Requirements

**Cloud-native (SG/NSG/firewall)**

- **Pros:** native, agentless, free, provider-integrated, IaC-friendly.
- **Cons:** cloud-only; coarse (instance/subnet); per-cloud silos; no on-prem/OT; limited L7.
- **Compatibility:** the provider's own VMs/subnets; not on-prem, OT, or cross-cloud uniformly.
- **Requirements:** cloud account + IAM to manage SG/NSG/firewall; an IaC workflow is strongly advised.

**Kubernetes NetworkPolicy / Calico / Cilium**

- **Pros:** native to clusters; **label/identity-based** (survives pod churn/IP change); Cilium adds
  **eBPF** performance and **L3–L7** policy + Hubble visibility; Calico adds cluster-wide policy and
  encryption.
- **Cons:** **CNI-dependent** (NetworkPolicy is inert without a policy-capable CNI); cluster-scoped (not
  a whole-estate control); a learning curve for L7/eBPF.
- **Compatibility:** any conformant Kubernetes with a policy-capable **CNI** (Calico, Cilium, and
  others); not for non-container assets.
- **Requirements:** a Kubernetes cluster with a **NetworkPolicy-enforcing CNI**; `kubectl`; for Calico/
  Cilium, their CLIs (`calicoctl`, `cilium`).

## Design Considerations

Use **cloud-native** controls as the baseline in each cloud (they are free and native), but do not
expect uniform policy **across** clouds or on-prem — a cross-environment product (Chapters 04–07) may be
needed for one policy model. In Kubernetes, adopt a **default-deny** NetworkPolicy per namespace and
allow only needed flows; choose **Cilium** for L7/identity policy and observability or **Calico** for
cluster-wide policy and encryption. Manage all of it as **code**.

## Implementation and Automation

The labs create a cloud security-group rule, apply a default-deny plus allow NetworkPolicy, and reason
about Calico/Cilium — the cloud and container options in the rubric.

## Validation and Troubleshooting

Confirm cloud/Kubernetes enforcement:

```text
Cloud-native: AWS SG (instance, stateful) / NACL (subnet, stateless); Azure NSG+ASG; GCP firewall (tags/SAs)
K8s NetworkPolicy: label-selected pods; default allow-all -> selecting a pod makes it default-deny (that direction); CNI enforces
Calico: NetworkPolicy + GlobalNetworkPolicy + WireGuard; Cilium: eBPF, L3-L7 identity, Hubble
Requirement: cloud IAM (cloud) / a policy-capable CNI (K8s)
```

Common pitfalls: writing a Kubernetes NetworkPolicy on a CNI that does **not enforce** it (no effect);
and treating cloud security groups as a **whole-estate** control (they are per-cloud only).

## Security and Best Practices

Default-deny per namespace and per subnet, allow only needed flows, and manage rules as code with review.
Add encryption (WireGuard/Cilium) where required. These are defensive controls on your own cloud and
clusters. All work is authorized.

## Hands-On Lab

Cloud/Kubernetes walkthroughs. **Shared prerequisites** — `kubectl` against a cluster with a
policy-capable CNI (e.g., `kind` + Calico or Cilium), and a cloud CLI (`aws`) for the cloud lab; `python3`
optional. **Cost:** none (kind + free-tier).

### Lab 8.1 — Create a cloud security-group rule (AWS)

**Objective:** Allowlist instance-level traffic.

```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-app --protocol tcp --port 5432 \
  --source-group sg-web
aws ec2 describe-security-groups --group-ids sg-app \
  --query "SecurityGroups[0].IpPermissions[?FromPort==\`5432\`]"
```

```json
[ { "FromPort": 5432, "ToPort": 5432, "IpProtocol": "tcp",
    "UserIdGroupPairs": [ { "GroupId": "sg-web" } ] } ]
```

**Expected result:** the app security group allows Postgres only from the web security group — group-to
-group allowlisting (no CIDR).

**Negative test:** open `5432` to `0.0.0.0/0` for convenience; that exposes the database — scope the
rule to the **source security group**.

**Rollback:**

```bash
aws ec2 revoke-security-group-ingress --group-id sg-app --protocol tcp --port 5432 --source-group sg-web
```

### Lab 8.2 — Apply a default-deny Kubernetes NetworkPolicy

**Objective:** Flip a namespace to default-deny ingress.

```bash
kubectl apply -f - <<'YAML'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny-ingress, namespace: shop }
spec:
  podSelector: {}
  policyTypes: ["Ingress"]
YAML
kubectl get networkpolicy -n shop
```

```text
NAME                   POD-SELECTOR   AGE
default-deny-ingress   <none>         3s
```

**Expected result:** all pods in `shop` now deny ingress by default (with a policy-capable CNI enforcing
it).

**Negative test:** apply this on a cluster whose CNI does not enforce NetworkPolicy; nothing changes —
use Calico/Cilium (or another enforcing CNI).

**Rollback:**

```bash
kubectl delete networkpolicy default-deny-ingress -n shop
```

### Lab 8.3 — Allow a specific pod-to-pod flow

**Objective:** Permit only web→app on the app port.

```bash
kubectl apply -f - <<'YAML'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-web-to-app, namespace: shop }
spec:
  podSelector: { matchLabels: { role: app } }
  policyTypes: ["Ingress"]
  ingress:
    - from: [ { podSelector: { matchLabels: { role: web } } } ]
      ports: [ { protocol: TCP, port: 8080 } ]
YAML
kubectl describe networkpolicy allow-web-to-app -n shop | grep -A3 Ingress
```

```text
Ingress:
  To Port: 8080/TCP
  From:
    PodSelector: role=web
```

**Expected result:** app pods accept traffic only from web pods on 8080 — label-selected, IP-independent
allowlisting.

**Negative test:** select peers by pod **IP**; pods are ephemeral and IPs churn — select by **label**.

**Rollback:**

```bash
kubectl delete networkpolicy allow-web-to-app -n shop
```

### Lab 8.4 — Reason about Calico vs Cilium

**Objective:** Choose the right CNI enforcement.

```python
python3 - <<'PY'
cni = {
  "NetworkPolicy (built-in)": "namespace/pod label rules; needs an enforcing CNI; L3/L4",
  "Calico": "NetworkPolicy + GlobalNetworkPolicy (cluster-wide) + WireGuard encryption",
  "Cilium": "eBPF; identity-based L3-L7 (HTTP/gRPC/Kafka); Hubble observability",
}
for tool, note in cni.items(): print(f"{tool:26}: {note}")
print("Pick Cilium for L7/identity + visibility; Calico for cluster-wide policy + encryption")
PY
```

**Expected result:** the three K8s options contrasted — pick by whether you need L7/identity (Cilium) or
cluster-wide policy/encryption (Calico).

**Negative test:** expect L7 (HTTP path) filtering from plain NetworkPolicy; it is L3/L4 — use **Cilium**
for L7.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Clouds and Kubernetes segment natively: AWS/Azure/GCP security groups/NSGs/firewall rules are free,
agentless, and provider-integrated but cloud-only and coarse; Kubernetes NetworkPolicy label-selects pods
into default-deny (enforced by a policy-capable CNI), with Calico adding cluster-wide policy and
encryption and Cilium adding eBPF L3–L7 identity policy and Hubble visibility.

- [ ] I can create a cloud security-group allowlist rule.
- [ ] I can apply a default-deny and an allow NetworkPolicy.
- [ ] I can reason about Calico vs Cilium.
- [ ] I can state the pros, cons, compatibility, and requirements.
- [ ] I completed Labs 8.1–8.4 including each negative test.
