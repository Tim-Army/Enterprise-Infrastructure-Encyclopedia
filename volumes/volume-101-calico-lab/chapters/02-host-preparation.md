# Chapter 02: Host Preparation

## Learning Objectives

- Install Docker, `kind`, `kubectl`, and `calicoctl` on a single Linux host.
- Confirm the host can run a Kubernetes-in-Docker cluster.
- Understand what each tool does before you build the cluster.

Any Linux host with 2 vCPU and 4 GB RAM works: an Ubuntu 22.04 VM in VMware Workstation, a cloud VM, or WSL2 on Windows 11. The commands below are for Ubuntu 22.04.

## Hands-On Lab

### Lab 2.1 — Install Docker

**Objective.** Install the container runtime `kind` uses to host the cluster.

**Walkthrough**

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
# log out and back in (or: newgrp docker) so the group membership takes effect
docker run --rm hello-world
```

**Expected result.** `hello-world` prints its greeting — Docker works without `sudo`.

**Negative test.** Skip the `usermod`/re-login and every `docker` and `kind` command needs `sudo`, which then owns the kubeconfig. Fix the group membership now.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Install kind and kubectl

**Objective.** Install the cluster builder and the cluster CLI.

**Walkthrough**

```bash
# kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind
# kubectl (matched to a current stable release)
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl && sudo mv ./kubectl /usr/local/bin/kubectl
kind version && kubectl version --client
```

**Expected result.** Both report their versions.

**Negative test.** Install a `kubectl` more than one minor version away from the cluster you build in Chapter 03 and you may see version-skew warnings; keep them close.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Install calicoctl

**Objective.** Install Calico's CLI, which you need for `GlobalNetworkPolicy`, `HostEndpoint`, and `NetworkSet` resources that `kubectl` alone does not manage as first-class objects.

**Walkthrough**

```bash
curl -Lo ./calicoctl https://github.com/projectcalico/calico/releases/download/v3.28.0/calicoctl-linux-amd64
chmod +x ./calicoctl && sudo mv ./calicoctl /usr/local/bin/calicoctl
calicoctl version --config /dev/null 2>/dev/null || calicoctl version
```

**Expected result.** `calicoctl` reports its client version. (It reports cluster details only after Chapter 03.)

**Negative test.** Try to manage a `GlobalNetworkPolicy` with `kubectl` before installing the Calico CRDs; it fails with "no matches for kind". Calico's CRDs arrive with the CNI in Chapter 03.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Docker installed; `hello-world` runs without `sudo`.
- [ ] `kind` and `kubectl` installed and reporting versions.
- [ ] `calicoctl` installed.
- [ ] Host has 2 vCPU / 4 GB RAM free.
