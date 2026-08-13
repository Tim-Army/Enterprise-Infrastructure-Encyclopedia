# Chapter 03: Building the Cluster with Cilium

## Learning Objectives

- Create a `kind` cluster with the default CNI disabled.
- Install Cilium as the CNI and enable Hubble.
- Verify Cilium is healthy before deploying any workload.

## Hands-On Lab

### Lab 3.1 — Create a kind cluster without a default CNI

**Objective.** Build the cluster so that *Cilium* provides the dataplane and policy.

**Walkthrough**

```bash
cat > kind-cilium.yaml <<'EOF'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  disableDefaultCNI: true
  podSubnet: "10.244.0.0/16"
EOF
kind create cluster --name cilium-lab --config kind-cilium.yaml
kubectl get nodes
```

**Expected result.** One node, `NotReady` — no CNI yet. Correct at this stage.

**Negative test.** Omit `disableDefaultCNI: true` and kind installs `kindnet`; you would then be running two CNIs or the wrong one. Recreate with the config above.

**Rollback.** None yet.

### Lab 3.2 — Install Cilium and enable Hubble

**Objective.** Install the Cilium CNI, bring the node Ready, and turn on Hubble observability.

**Walkthrough**

**Step 1.** Install Cilium (the CLI auto-detects kind). Pin a version for reproducibility:

```bash
cilium install --version 1.16.5
cilium status --wait
kubectl get nodes
```

**Step 2.** Enable Hubble (the flow-observability layer) and open a local relay:

```bash
cilium hubble enable
cilium status --wait
# in a second terminal, port-forward the Hubble relay so the CLI can read flows:
cilium hubble port-forward &
hubble status
```

**Expected result.** `cilium status` reports Cilium and Hubble OK; the node is **Ready**; `hubble status` connects. Cilium is now the eBPF dataplane and policy engine, and Hubble is watching.

**Negative test.** Deploy a workload before `cilium status` is OK and its pod stays `ContainerCreating` — no CNI, no networking. Wait for the status.

**Rollback.** Keep the cluster; Chapter 04 deploys the workloads.

### Lab 3.3 — Meet Cilium identities

**Objective.** See that Cilium identifies workloads by a **security identity** derived from labels, not by IP.

**Walkthrough**

```bash
cilium identity list 2>/dev/null | head
kubectl -n kube-system exec ds/cilium -- cilium identity list | head
```

**Expected result.** A list of numeric identities, each tied to a set of labels (namespace, app, and Kubernetes metadata). When you write policy in Chapters 07–08, Cilium resolves your label selectors to these identities and enforces on them in eBPF — which is why policy follows the workload, not its address.

**Negative test.** Look for an identity keyed on pod IP; there is none. Identity is label-derived, so it survives the pod's IP changing.

**Rollback.** Keep the cluster.

## Summary and Completion Checklist

- [ ] kind cluster created with the default CNI disabled.
- [ ] Cilium installed; node Ready; `cilium status` OK.
- [ ] Hubble enabled and reachable via `hubble status`.
- [ ] The label-derived identity model seen with `cilium identity list`.
