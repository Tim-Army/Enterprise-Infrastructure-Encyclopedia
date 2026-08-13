# Chapter 03: Building the Cluster with Calico

## Learning Objectives

- Create a single-node Kubernetes cluster with `kind`, with the default CNI disabled.
- Install Calico as the cluster's CNI and policy engine.
- Verify Calico is healthy before deploying any workload.

## Hands-On Lab

### Lab 3.1 — Create a kind cluster without a default CNI

**Objective.** Build the cluster so that *Calico* — not kind's built-in networking — provides the dataplane and policy.

**Walkthrough**

**Step 1.** Write a kind config that disables the default CNI and sets a pod subnet Calico expects:

```bash
cat > kind-calico.yaml <<'EOF'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  disableDefaultCNI: true
  podSubnet: "192.168.0.0/16"
EOF
kind create cluster --name calico-lab --config kind-calico.yaml
```

**Step 2.** Confirm the cluster exists but nodes are **NotReady** (expected — there is no CNI yet):

```bash
kubectl get nodes
```

**Expected result.** One node, `calico-lab-control-plane`, in `NotReady` — because no CNI is installed. That is correct at this stage.

**Negative test.** Create the cluster *without* `disableDefaultCNI: true` and kind installs `kindnet`, which does not enforce Calico policy. You would be testing the wrong dataplane. Delete and recreate with the config above.

**Rollback.** None yet.

### Lab 3.2 — Install Calico

**Objective.** Install the Calico CNI and policy engine and bring the node Ready.

**Walkthrough**

**Step 1.** Apply the Calico manifest and wait for it to roll out:

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/calico.yaml
kubectl -n kube-system rollout status daemonset/calico-node --timeout=180s
kubectl get nodes
```

**Step 2.** Point `calicoctl` at the cluster and confirm it can read Calico state:

```bash
export DATASTORE_TYPE=kubernetes
export KUBECONFIG="$HOME/.kube/config"
calicoctl get nodes -o wide
```

**Expected result.** The node moves to **Ready**; `calico-node` is Running; `calicoctl get nodes` lists the node. Calico is now the dataplane and policy engine.

**Negative test.** Deploy a workload before `calico-node` is Ready and its pod stays `ContainerCreating` with a CNI error — no dataplane, no networking. Wait for the rollout.

**Rollback.** Keep the cluster; Chapter 04 deploys the workloads.

## Summary and Completion Checklist

- [ ] kind cluster created with the default CNI disabled.
- [ ] Calico installed; the node is Ready and `calico-node` Running.
- [ ] `calicoctl` can read cluster state.
