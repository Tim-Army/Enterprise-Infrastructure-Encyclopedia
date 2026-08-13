# Chapter 08: Docker, LXD, Canonical Kubernetes, and OpenShift Interoperability

![Flow diagram showing a Docker container and an independent LXD system container each serving the same application, alongside a naive container image that fails under an arbitrary UID and a portable chgrp-0/chmod-g=u image that succeeds under the same UID.](../../../diagrams/volume-021-ubuntu-server-cloud-26-04-lts/chapter-08-docker-lxd-arbitrary-uid-flow.svg)

*Figure 8-1. The Docker-and-LXD coexistence and OpenShift-compatible image pattern exercised in this chapter's lab, including the arbitrary-UID negative test.*

## Learning Objectives

- Install and operate Docker Engine on Ubuntu Server, including Compose
  workflows.
- Deploy and manage system containers with LXD, including profiles,
  storage pools, and clustering basics.
- Install Canonical Kubernetes and perform first-cluster operations.
- Build container images on Ubuntu that run correctly under OpenShift's
  restricted Security Context Constraints (SCCs), and use `oc` from an
  Ubuntu administrative workstation.
- Distinguish when Docker, LXD, or Canonical Kubernetes is the right
  tool for a given workload.

## Theory and Architecture

Ubuntu Server offers three distinct container/orchestration paths, each
solving a different problem, plus a practical need — covered here as
"interoperability" rather than a full OpenShift deployment guide — to
build workloads on Ubuntu that behave correctly when they land on a
Red Hat OpenShift cluster (documented in depth in [Volume XIV](../../volume-014-red-hat-enterprise-linux-10/README.md)).

### Docker: application containers

**Docker Engine** on Ubuntu runs as `dockerd`, managed by systemd,
providing the standard OCI-compatible application container runtime
most administrators already associate with "containers." Ubuntu
packages Docker both through Canonical's own `docker.io` package and
through Docker's official upstream APT repository (`docker-ce`); the
upstream repository generally tracks newer releases and is what Docker
Inc. itself supports, while `docker.io` is Ubuntu-maintained and tied
to the distribution's own update cadence. Docker Compose (the `docker
compose` plugin, not the legacy standalone `docker-compose` Python
tool) provides multi-container application definition and lifecycle
management from a single YAML file.

### LXD: system containers and lightweight VMs

**LXD** is Canonical's container and virtual-machine manager, distinct
from Docker in a fundamental way: where Docker containers are
purpose-built to run a single application process, **LXD system
containers** boot a full init system (systemd) and behave like a
lightweight virtual machine — multiple services, SSH access,
package management, the works — while still sharing the host kernel
for near-native performance. LXD also manages actual KVM-backed virtual
machines through the same `lxc`/`lxd` command surface, unifying
container and VM management under one tool. Concepts worth knowing:

- **Profiles** — reusable configuration (network, resource limits,
  device mounts) applied to one or more instances.
- **Storage pools** — backend storage (ZFS, Btrfs, LVM, or plain
  directory) instances draw their root disk from; ZFS-backed pools gain
  instant, space-efficient snapshots and clones.
- **Clustering** — multiple LXD servers joined into a single
  management domain, distributing instances across members.

LXD's project was forked by much of its original community as
**Incus** after a 2023 governance dispute; both remain actively
developed, and Canonical continues to ship and support LXD directly on
Ubuntu, distributed as a snap.

### Canonical Kubernetes

**Canonical Kubernetes** (`k8s`, distributed as a snap) is Canonical's
upstream-conformant Kubernetes distribution, positioned for production
clusters that want a CNCF-conformant Kubernetes with Canonical's
enterprise support and integration with the rest of the Ubuntu
ecosystem (Juju, Landscape — [Chapter 09](09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md)). It installs as a single snap
per node, bundles a default CNI and DNS add-on, and clusters additional
nodes with a token-based join, deliberately minimizing the number of
separate components an administrator must assemble compared to a
from-scratch `kubeadm` build.

### OpenShift interoperability

Most enterprise environments running Red Hat OpenShift ([Volume XIV](../../volume-014-red-hat-enterprise-linux-10/README.md))
still rely on Ubuntu somewhere in the pipeline — developer
workstations, CI/CD runners, or hosts building the container images
OpenShift will run. Two things matter for that hand-off:

1. **`oc` (the OpenShift CLI) runs natively on Ubuntu** as a standalone
   binary, letting an Ubuntu-based CI runner or admin workstation manage
   OpenShift projects, builds, and deployments without needing RHEL
   anywhere in that toolchain.
2. **OpenShift enforces restricted Security Context Constraints (SCCs)
   by default**, meaning containers run with an arbitrarily assigned,
   non-root UID unless explicitly granted otherwise — a container image
   built on Ubuntu (or anywhere) that hard-codes a specific UID, writes
   to paths owned by `root`, or otherwise assumes it controls its own
   UID will fail under OpenShift even though it runs fine under plain
   Docker or Kubernetes elsewhere. Building images with group-writable,
   GID-0-owned application directories (the pattern Red Hat's own base
   images use) is what makes an Ubuntu-built image portable to
   OpenShift's default posture without a custom SCC.

## Design Considerations

- **Docker vs. LXD for a given workload.** Choose Docker for
  single-process, horizontally scalable application workloads that
  will eventually run under an orchestrator; choose LXD when the
  workload genuinely needs a full OS environment (legacy application
  migration, a workload that expects to manage its own services via
  systemd, or infrastructure that benefits from VM-like isolation
  without full virtualization overhead).
- **Docker Compose vs. Kubernetes for multi-container applications.**
  Compose is appropriate for single-host development and small,
  non-clustered production deployments; anything needing multi-host
  scheduling, self-healing, or rolling updates across nodes belongs on
  Canonical Kubernetes (or another Kubernetes distribution) instead.
- **LXD storage backend selection.** A ZFS-backed storage pool gives
  LXD instant snapshots and efficient clones (useful for golden-image
  workflows spinning up many similar containers); a plain directory
  backend is simpler but loses those capabilities — decide before
  significant instance population exists, since migrating a pool's
  backend later is disruptive.
- **Canonical Kubernetes vs. a hand-assembled `kubeadm` cluster.**
  Canonical Kubernetes trades some configuration flexibility for a
  dramatically simpler install and upgrade path and Canonical support;
  a hand-assembled cluster offers maximum control over every component
  version at the cost of the operational burden of tracking upstream
  compatibility yourself.
- **Building OpenShift-portable images from an Ubuntu build host.**
  Decide this at Dockerfile-authoring time, not deployment time — retrofitting
  arbitrary-UID compatibility into an image that assumed a fixed UID
  is a bigger change than designing for it from the start (`chgrp -R 0`
  and `chmod g=u` on writable paths, avoiding `USER <fixed-uid>` unless
  that UID is also `0`-group-writable-compatible).
- **Multi-tool sprawl.** Running Docker, LXD, and Canonical Kubernetes
  simultaneously on the same fleet without a clear rule for which tool
  owns which workload class creates real operational confusion; document
  the decision, not just the tools.

## Implementation and Automation

### 1. Docker Engine installation and basic operation

```bash
# Install from Docker's official upstream repository
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Allow a non-root administrator to use docker without sudo
sudo usermod -aG docker "$USER"

# Basic lifecycle
docker run --rm hello-world
docker ps -a
docker images

# Compose-based multi-container application
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
EOF
docker compose up -d
docker compose ps
docker compose down
```

### 2. LXD system containers

```bash
sudo snap install lxd
sudo lxd init --auto

# Launch a system container from an Ubuntu image
lxc launch ubuntu:24.04 web01

# Execute a command inside it, or get an interactive shell
lxc exec web01 -- apt update
lxc exec web01 -- bash

# Apply a reusable profile (resource limits, extra device)
lxc profile create constrained
lxc profile set constrained limits.cpu 2
lxc profile set constrained limits.memory 2GB
lxc profile add web01 constrained

# Snapshot and clone (fast, copy-on-write, on a ZFS storage pool)
lxc snapshot web01 pre-change
lxc copy web01 web02

# Inspect storage pools and profiles
lxc storage list
lxc profile list
lxc list
```

### 3. Canonical Kubernetes

```bash
# Install on the first (control-plane) node
sudo snap install k8s --classic

# Bootstrap the cluster
sudo k8s bootstrap

# Confirm cluster status and get a join token for additional nodes
sudo k8s status
sudo k8s get-join-token worker-node-01

# On a second node, install the snap and join using the token
sudo snap install k8s --classic
sudo k8s join-cluster <join-token>

# Standard kubectl workflow (bundled with the snap)
sudo k8s kubectl get nodes
sudo k8s kubectl get pods -A
sudo k8s kubectl create deployment demo --image=nginx --replicas=2
sudo k8s kubectl expose deployment demo --port=80 --type=NodePort
```

### 4. An OpenShift-portable Dockerfile built on Ubuntu

```dockerfile
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ /app/

# Make application directories writable by any UID in the root group,
# not just a hard-coded owner — this is what makes the image run
# correctly under OpenShift's default arbitrary-UID SCC.
RUN chgrp -R 0 /app && chmod -R g=u /app

# Do not pin a specific non-root UID; let the runtime (Docker,
# Kubernetes, or OpenShift) assign one.
USER 1001

EXPOSE 8080
ENTRYPOINT ["python3", "app.py"]
```

### 5. Using `oc` from an Ubuntu administrative workstation

```bash
# Install the OpenShift CLI binary (no RHEL dependency)
curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz \
  -o oc.tar.gz
tar xzf oc.tar.gz
sudo install -m 0755 oc /usr/local/bin/oc

oc login https://api.ocp-cluster.example.com:6443 --token=<sha256~token>
oc new-project lab-interop
oc apply -f deployment.yaml
oc get pods
oc logs deployment/demo
```

## Validation and Troubleshooting

- **Docker Compose service fails to start.** `docker compose logs
  <service>` shows the container's stdout/stderr directly; `docker
  compose config` renders the fully resolved configuration, useful for
  catching variable-substitution or override-file mistakes before they
  cause a confusing runtime failure.
- **An LXD container won't launch — `Failed to create instance`.**
  `lxc info --show-log web01` shows the console log from the failed
  launch; a common cause is insufficient storage pool space
  (`lxc storage info default`) or a kernel missing a required feature
  for the chosen storage backend.
- **Canonical Kubernetes node won't join.** `sudo k8s status` on the
  control-plane node confirms it's healthy and the join token hasn't
  expired; `journalctl -u snap.k8s.*` on the joining node surfaces
  network reachability or certificate errors.
- **A pod is `CrashLoopBackOff` under plain Kubernetes but the same
  image fails differently (`Permission denied`) under OpenShift.**
  This is almost always the arbitrary-UID SCC: `oc get pod <name> -o
  yaml | grep -A2 securityContext` shows the assigned UID, and
  `oc logs` typically shows a specific path write failure — the fix is
  the `chgrp 0`/`chmod g=u` pattern in the Dockerfile, not a custom SCC
  grant, in the general case.
- **`oc login` fails from an Ubuntu workstation but succeeds from a
  RHEL host.** This is essentially never distribution-specific;
  confirm system time is correct ([Chapter 07](07-dns-ntp-dhcp-web-database-and-common-server-services.md) — a skewed clock breaks
  TLS validation), and confirm the CA bundle the OpenShift API server's
  certificate chains to is trusted on the Ubuntu host
  (`update-ca-certificates` after adding an internal CA).

## Security and Best Practices

- Add administrators to the `docker` group deliberately and sparingly —
  membership is equivalent to root on the host, since the Docker
  daemon socket has no further access control layer by default.
- Prefer LXD's unprivileged containers (the default) over privileged
  containers; a privileged LXD container's root user maps to the
  host's real root, materially weakening the isolation LXD otherwise
  provides.
- Scan container images (Docker or LXD-hosted OCI images alike) for
  known vulnerabilities as part of the build pipeline, not only at
  deploy time, and keep base images (`ubuntu:24.04`, etc.) updated on a
  defined cadence rather than pinning indefinitely.
- Apply Canonical Kubernetes RBAC and network policy deliberately from
  the first workload deployed; a default-open cluster network is a
  common and avoidable finding in early-stage Kubernetes adoption.
- Build container images to run correctly as an arbitrary non-root UID
  by default (the `chgrp 0`/`chmod g=u` pattern), even for workloads
  not immediately destined for OpenShift — it is strictly more
  portable and more secure than assuming a fixed UID or root.
- Rotate and scope `oc` and `kubectl` credentials (service account
  tokens, `kubeconfig` contexts) the same way SSH keys are scoped
  ([Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)); do not share a single cluster-admin token across an
  entire team's workstations.

## References and Knowledge Checks

**References**

- [Docker Engine documentation, `docker.com`.](https://docs.docker.com/engine/)
- [LXD documentation, `documentation.ubuntu.com/lxd`.](https://documentation.ubuntu.com/lxd/latest/)
- [Canonical Kubernetes documentation, `documentation.ubuntu.com/canonical-kubernetes`.](https://documentation.ubuntu.com/canonical-kubernetes/latest/)
- OpenShift Security Context Constraints documentation, Red Hat
  (cross-referenced with [Volume XIV](../../volume-014-red-hat-enterprise-linux-10/README.md)).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Ubuntu Server
  26.04 and Kubernetes baselines referenced throughout this chapter.

**Knowledge checks**

1. What is the fundamental difference between an LXD system container
   and a Docker application container, and when does that difference
   matter for a workload decision?
2. Why does Canonical continue to ship and support LXD after the Incus
   community fork, and how does that affect an administrator's tool
   choice today?
3. Why does a container image that works under plain Docker or
   Kubernetes sometimes fail under OpenShift, and what Dockerfile
   pattern resolves it?
4. Why can `oc` be used effectively from an Ubuntu workstation with no
   RHEL host involved anywhere in the toolchain?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each container technology in the
"Deployment Technologies" competency** — LXD system containers, Docker Engine, Canonical
Kubernetes, and OpenShift-compatible images. Every step is a runnable Ubuntu 26.04 command. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.4** — an Ubuntu 26.04 system with `sudo` and enough
resources for containers; `snap` available. **Cost:** none.

### Lab 8.1 — LXD system containers (Topic: System containers)

**Objective:** Launch and manage a full-OS container.

```bash
sudo snap install lxd
sudo lxd init --minimal
lxc launch ubuntu:24.04 c1
lxc list
lxc exec c1 -- hostnamectl | head -3
```

**Expected result:** `c1` runs as a lightweight system container with its own init, users, and
network — LXD provides **system** containers (a full Ubuntu userspace, like a fast VM) as opposed
to Docker's single-process **application** containers, and it is Canonical's native container
technology.

**Negative test:** expect a Docker application container to run a full multi-service OS with its
own init; that is LXD's model, not Docker's — choose LXD for machine-like containers, Docker/OCI
for single-app images.

**Rollback:** `lxc delete -f c1`.

### Lab 8.2 — Docker Engine (Topic: Application containers)

**Objective:** Run an OCI application container.

```bash
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo docker run -d --name web -p 8080:80 nginx
curl -s http://localhost:8080/ | head -1
sudo docker ps
```

**Expected result:** the nginx application container serves on 8080 — Docker runs OCI
application containers (one main process per container), the format shared across the container
ecosystem; on Ubuntu it installs as the `docker.io` package or the upstream Docker CE repo.

**Negative test:** run the container as a non-docker-group user without sudo; access to the Docker
socket is denied — Docker daemon access is root-equivalent, so socket membership is a privilege to
grant carefully.

**Rollback:** `sudo docker rm -f web`.

### Lab 8.3 — Canonical Kubernetes (Topic: Orchestration)

**Objective:** Bootstrap a single-node Kubernetes and run a workload.

```bash
sudo snap install k8s --classic
sudo k8s bootstrap
sudo k8s status --wait-ready
sudo k8s kubectl create deployment web --image=nginx --replicas=2
sudo k8s kubectl get pods -o wide
```

**Expected result:** the `k8s` snap bootstraps a working cluster and schedules the Deployment's
pods — Canonical Kubernetes (the `k8s` snap, successor to MicroK8s for many uses) gives a
production-capable, batteries-included Kubernetes installed from a single snap.

**Negative test:** expect `kubectl` to work before `k8s bootstrap` completes; the API server is
not up and commands fail — the cluster must finish bootstrapping (`status --wait-ready`) first.

**Rollback:** `sudo k8s kubectl delete deployment web`; `sudo snap remove k8s` if lab-only.

### Lab 8.4 — OpenShift-compatible images (Topic: Interoperability)

**Objective:** Build an image that runs under OpenShift's restrictive defaults.

```bash
mkdir -p ~/oci && cd ~/oci
cat > Dockerfile <<'EOF'
FROM ubuntu:24.04
RUN groupadd -g 1001 app && useradd -u 1001 -g 0 -m app
# OpenShift runs containers with a random UID in group 0 (root group), non-root:
RUN mkdir -p /data && chgrp -R 0 /data && chmod -R g=u /data
USER 1001
WORKDIR /data
CMD ["sleep","3600"]
EOF
sudo docker build -t localhost/os-compat:1.0 . && echo "built OpenShift-compatible image"
```

**Expected result:** an image that does not assume a fixed UID and grants group-0 write access, so
it runs under OpenShift's default `restricted` SCC (arbitrary non-root UID, GID 0) — building for
arbitrary-UID/non-root is what makes an image portable to OpenShift, not just permissive Docker.

**Negative test:** build an image that runs as root or hard-codes UID 0 paths; OpenShift's
`restricted` SCC refuses it — images must tolerate a random non-root UID in group 0 to
interoperate.

**Rollback:** `sudo docker rmi localhost/os-compat:1.0; rm -rf ~/oci`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Docker, LXD, and Canonical Kubernetes cover three distinct needs on
Ubuntu Server: single-process application containers, full-OS system
containers and lightweight VMs, and production Kubernetes
orchestration, respectively. LXD's continued Canonical support
alongside the community Incus fork means Ubuntu administrators have a
stable, supported system-container option regardless of that
governance split. Building images with the `chgrp 0`/`chmod g=u`
arbitrary-UID pattern makes Ubuntu-built container images portable to
OpenShift's default restricted SCC without custom security exceptions,
and the `oc` CLI runs natively on Ubuntu with no RHEL dependency
anywhere in the administrative toolchain.

- [ ] Can install and operate Docker Engine and Docker Compose on
      Ubuntu Server.
- [ ] Can launch, profile, snapshot, and clone LXD system containers.
- [ ] Can bootstrap and join nodes to a Canonical Kubernetes cluster.
- [ ] Can build a container image that runs correctly under OpenShift's
      default arbitrary-UID SCC.
- [ ] Can use `oc` from an Ubuntu workstation to manage OpenShift
      resources.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
