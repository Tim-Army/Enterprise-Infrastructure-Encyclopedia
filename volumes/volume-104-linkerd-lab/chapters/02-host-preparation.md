# Chapter 02: Host Preparation

## Learning Objectives

- Install Docker, `kind`, `kubectl`, and the `linkerd` CLI.
- Confirm the host can run a Kubernetes-in-Docker cluster.

Any Linux host with 2 vCPU and 4 GB RAM works: an Ubuntu 22.04 VM, a cloud VM, or WSL2.

## Hands-On Lab

### Lab 2.1 — Install Docker, kind, and kubectl

**Objective.** Install the container runtime, the cluster builder, and the cluster CLI.

**Walkthrough**

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"    # then log out/in, or: newgrp docker
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl && sudo mv ./kubectl /usr/local/bin/kubectl
docker run --rm hello-world && kind version && kubectl version --client
```

**Expected result.** `hello-world` runs without `sudo`; `kind` and `kubectl` report versions.

**Negative test.** Skip the `usermod`/re-login and every `docker`/`kind` command needs `sudo`. Fix the group membership now.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Install the linkerd CLI

**Objective.** Install the tool that installs Linkerd and inspects the mesh.

**Walkthrough**

```bash
curl -fsSL https://run.linkerd.io/install | sh
sudo cp "$HOME/.linkerd2/bin/linkerd" /usr/local/bin/linkerd
linkerd version --client
```

**Expected result.** `linkerd` reports its client version (there is no control plane yet).

**Negative test.** Run `linkerd check` now; it warns there is no cluster or control plane. Both arrive in Chapter 03.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Docker installed; `hello-world` runs without `sudo`.
- [ ] `kind` and `kubectl` installed.
- [ ] `linkerd` CLI installed and reporting a version.
