# Chapter 03: Building the Cluster and Installing Consul

## Learning Objectives

- Create a `kind` cluster.
- Install Consul with Connect (the service mesh) and ACLs via Helm.
- Verify Consul is healthy and reach its UI.

## Hands-On Lab

### Lab 3.1 — Create a kind cluster

**Objective.** Build a standard single-node cluster (Consul runs on top of the default CNI).

**Walkthrough**

```bash
kind create cluster --name consul-lab
kubectl get nodes
```

**Expected result.** One node, `Ready`.

**Negative test.** Disabling the default CNI here leaves the node `NotReady`; Consul needs a working pod network. Leave the default CNI.

**Rollback.** None yet.

### Lab 3.2 — Install Consul with Connect

**Objective.** Install the Consul control plane, the mesh (Connect), and ACLs.

**Walkthrough**

**Step 1.** Add the Helm repo and write values that enable the mesh and security:

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com && helm repo update
cat > consul-values.yaml <<'EOF'
global:
  name: consul
  datacenter: dc1
  tls:
    enabled: true
  acls:
    manageSystemACLs: true
connectInject:
  enabled: true
  default: false          # opt in per workload, not everywhere
ui:
  enabled: true
EOF
helm install consul hashicorp/consul --namespace consul --create-namespace --values consul-values.yaml --wait
kubectl -n consul get pods
```

**Step 2.** Confirm the servers and injector are up:

```bash
kubectl -n consul get pods | grep -E "consul-server|connect-injector"
```

**Expected result.** `consul-server-0` and the `connect-injector` are `Running`. TLS and ACLs are on, and Connect (the mesh) is ready. `connectInject.default: false` means you opt each workload into the mesh explicitly (Chapter 04).

**Negative test.** On a 4 GB host that is already busy, the Consul server can stay `Pending` for lack of memory; give the host 6 GB or free some. Check `kubectl -n consul describe pod consul-server-0`.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Reach the Consul UI and CLI

**Objective.** Access Consul's UI and CLI to see the catalog and (later) intentions.

**Walkthrough**

```bash
# port-forward the UI (in a second terminal)
kubectl -n consul port-forward svc/consul-ui 8501:443 &
# use the CLI against the server via a port-forward + token
kubectl -n consul get secret consul-bootstrap-acl-token -o jsonpath='{.data.token}' | base64 -d; echo
```

**Expected result.** The UI is reachable at `https://localhost:8501` (accept the self-signed cert); the bootstrap ACL token is printed for CLI/UI login. You can now see the service catalog — empty of app services until Chapter 04.

**Negative test.** Skip the token and the UI shows nothing (ACLs deny anonymous read by default). Log in with the bootstrap token.

**Rollback.** Keep Consul running; Chapter 04 deploys the workloads.

## Summary and Completion Checklist

- [ ] kind cluster created; node Ready.
- [ ] Consul installed with Connect, TLS, and ACLs; servers and injector Running.
- [ ] UI reachable and the bootstrap ACL token retrieved.
