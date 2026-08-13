# Chapter 02: Host Preparation

## Learning Objectives

- Install Docker, `kind`, `kubectl`, and `istioctl` on a single Linux host.
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

### Lab 2.2 — Install istioctl

**Objective.** Install Istio's CLI, which installs the mesh and inspects it.

**Walkthrough**

```bash
curl -L https://istio.io/downloadIstio | sh -
sudo mv istio-*/bin/istioctl /usr/local/bin/istioctl
istioctl version --remote=false
```

**Expected result.** `istioctl` reports its version (client only — there is no mesh yet).

**Negative test.** Run `istioctl proxy-status` now; it errors because no cluster or mesh exists. The mesh arrives in Chapter 03.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Docker installed; `hello-world` runs without `sudo`.
- [ ] `kind` and `kubectl` installed.
- [ ] `istioctl` installed and reporting a version.
