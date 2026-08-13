# Chapter 02: Host Preparation

## Learning Objectives

- Install Docker, `kind`, `kubectl`, the `cilium` CLI, and the `hubble` CLI.
- Confirm the host can run a Kubernetes-in-Docker cluster.

Any Linux host with 2 vCPU and 4 GB RAM works: an Ubuntu 22.04 VM, a cloud VM, or WSL2. The commands are for Ubuntu 22.04 on x86-64.

## Hands-On Lab

### Lab 2.1 — Install Docker, kind, and kubectl

**Objective.** Install the container runtime, the cluster builder, and the cluster CLI.

**Walkthrough**

```bash
# Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"   # then log out/in, or: newgrp docker
# kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl && sudo mv ./kubectl /usr/local/bin/kubectl
docker run --rm hello-world && kind version && kubectl version --client
```

**Expected result.** `hello-world` runs without `sudo`; `kind` and `kubectl` report versions.

**Negative test.** Skip the `usermod`/re-login and every `docker`/`kind` command needs `sudo`, which then owns your kubeconfig. Fix the group membership now.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Install the cilium and hubble CLIs

**Objective.** Install the tools that install Cilium and observe flows.

**Walkthrough**

```bash
# cilium CLI (installs and manages Cilium)
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
curl -Lo cilium.tgz "https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-amd64.tar.gz"
sudo tar xzf cilium.tgz -C /usr/local/bin && rm cilium.tgz
# hubble CLI (observes flows)
HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
curl -Lo hubble.tgz "https://github.com/cilium/hubble/releases/download/${HUBBLE_VERSION}/hubble-linux-amd64.tar.gz"
sudo tar xzf hubble.tgz -C /usr/local/bin && rm hubble.tgz
cilium version --client && hubble version
```

**Expected result.** Both CLIs report their versions.

**Negative test.** Try `cilium status` now; it errors because no cluster exists yet. The CLI is a client — the cluster arrives in Chapter 03.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Docker installed; `hello-world` runs without `sudo`.
- [ ] `kind` and `kubectl` installed.
- [ ] `cilium` and `hubble` CLIs installed and reporting versions.
