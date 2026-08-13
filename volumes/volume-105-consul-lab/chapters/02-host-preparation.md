# Chapter 02: Host Preparation

**Host setup — creating these VMs on your hypervisor.** The per-hypervisor steps to create each VM (install from an ISO or boot a cloud image), size it, and map its NICs to the segments in this lab are the same for every hypervisor and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

## Learning Objectives

- Install Docker, `kind`, `kubectl`, `helm`, and the `consul` CLI.
- Confirm the host can run a Kubernetes-in-Docker cluster.

Any Linux host with 2 vCPU and 4 GB RAM works (6 GB is comfortable — Consul runs several server pods). The commands are for Ubuntu 22.04 on x86-64.

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

### Lab 2.2 — Install helm and the consul CLI

**Objective.** Install the tools that install Consul and inspect its catalog and intentions.

**Walkthrough**

```bash
# helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
# consul CLI
CONSUL_VER=1.19.1
curl -Lo consul.zip "https://releases.hashicorp.com/consul/${CONSUL_VER}/consul_${CONSUL_VER}_linux_amd64.zip"
unzip -o consul.zip && sudo mv consul /usr/local/bin/ && rm consul.zip
helm version && consul version
```

**Expected result.** Both report their versions.

**Negative test.** Run `consul members` now; it errors because no Consul agent is reachable. The cluster and Consul arrive in Chapter 03.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Docker installed; `hello-world` runs without `sudo`.
- [ ] `kind` and `kubectl` installed.
- [ ] `helm` and the `consul` CLI installed and reporting versions.
