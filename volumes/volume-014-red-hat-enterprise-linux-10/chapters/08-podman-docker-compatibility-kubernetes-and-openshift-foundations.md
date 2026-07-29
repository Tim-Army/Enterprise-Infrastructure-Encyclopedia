# Chapter 08: Podman, Docker Compatibility, Kubernetes, and OpenShift Foundations

![Lab flow for this chapter: a custom container image runs rootless as a Quadlet-managed systemd user service publishing a high port, confirmed reachable with curl. A two-container pod shares one network namespace, and the sidecar container reaches the app container over localhost. The pod is exported as Kubernetes-compatible YAML, removed entirely, and recreated purely from that file. As a negative test, running the same image rootless bound to a privileged port fails with a permission error — the documented, deliberate limitation of rootless Podman without additional configuration.](../../../diagrams/volume-014-red-hat-enterprise-linux-10/chapter-08-podman-quadlet-kube-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: a custom container image run rootless as a Quadlet service, grouped into a pod, and recreated from exported Kubernetes YAML.*

## Learning Objectives

- Explain Podman's daemonless, rootless architecture and how it
  differs from the Docker daemon model.
- Build, run, and manage containers and pods with Podman, including
  Containerfile-based image builds.
- Run containers as systemd-managed services using Quadlet.
- Describe how Podman's Docker CLI compatibility layer eases migration
  from Docker-based workflows.
- Explain core Kubernetes objects and how OpenShift extends vanilla
  Kubernetes for enterprise application platforms.
- Diagnose common container runtime, networking, and permission
  failures.

## Theory and Architecture

RHEL 10's default container engine is **Podman**, and understanding
why it is architecturally different from Docker — not just a
drop-in replacement with a different name — is necessary before any of
the daily commands make full sense, because several of Podman's most
important operational properties follow directly from that
architecture.

### Daemonless, fork-exec architecture

Docker's architecture centers on `dockerd`, a long-running root daemon
that every `docker` CLI invocation talks to over a socket; the daemon
itself creates and manages every container process. Podman has no
daemon. Each `podman run` invocation directly forks and executes the
container process as a child of the invoking process (using `conmon` as
a lightweight per-container monitor), and containers are tracked as
ordinary process trees rather than children of a central service. This
has concrete consequences:

- **No single point of failure.** A `dockerd` crash or restart affects
  every container it manages; there is no equivalent shared process
  for Podman to crash.
- **No always-on root daemon socket.** Docker's daemon socket is
  itself a well-known privilege-escalation target (write access to the
  socket is equivalent to root); Podman has no comparable persistent,
  privileged listener by default.
- **Native systemd integration.** Because a Podman container is just a
  process tree, systemd can supervise it directly (via generated unit
  files or Quadlet, covered below) the same way it supervises any other
  service, rather than needing a Docker-specific integration layer.

### Rootless containers

Podman is designed to run **rootless** — as an unprivileged user —
using Linux user namespaces to remap container-internal UID 0 to an
unprivileged UID on the host. A process that believes it is root
inside the container has no actual root privilege on the host system,
which meaningfully narrows the impact of a container escape compared
to a rootful container (or a Docker daemon running as root managing
every container on the host). Podman also supports rootful operation
(`sudo podman ...`) for workloads that genuinely need host-level
privileges (binding privileged ports below 1024 without additional
configuration, certain storage drivers, or host device access) — the
choice between rootless and rootful is a deliberate per-workload
decision, not an either/or platform setting.

### Pods: Kubernetes-compatible grouping

Podman's second architectural distinction is native support for
**pods** — one or more containers sharing a network namespace (and
optionally other namespaces), directly modeled on the Kubernetes pod
concept rather than Docker's flatter container model. A Podman pod can
be exported to and imported from Kubernetes YAML (`podman generate
kube`, `podman play kube`), which is what makes Podman a practical
local development and testing tool for workloads ultimately destined
for Kubernetes or OpenShift.

### Docker CLI compatibility

The `podman-docker` package installs a `docker` command that is a thin
wrapper invoking `podman` with translated arguments, and Podman's REST
API layer (`podman system service`) can emulate the Docker API socket
closely enough for many Docker-API-aware tools (including
`docker-compose`, via `podman-compose` or native Podman compose
support) to work with minimal or no changes. This compatibility layer
exists specifically to ease migration — existing scripts, CI
pipelines, and muscle memory built around `docker` commands continue
to work, while the underlying execution model is Podman's daemonless,
rootless-capable engine.

### Quadlet: systemd-native container units

**Quadlet** is RHEL 10's supported mechanism for running Podman
containers, pods, networks, and volumes as first-class systemd units.
Instead of hand-writing a `.service` unit around a `podman run`
command (a fragile pattern for handling restarts, ordering, and
logging correctly), Quadlet reads a declarative `.container`,
`.pod`, `.network`, or `.volume` file from
`/etc/containers/systemd/` and generates the corresponding systemd
unit automatically, giving containers the same dependency ordering,
restart policy, resource control, and journal-integrated logging as
any other systemd-managed service described in [Chapter 03](03-boot-systemd-processes-logging-and-scheduled-work.md). Quadlet is
the recommended replacement for the older `podman generate systemd`
workflow, which required manually regenerating unit files whenever a
container's configuration changed.

### Kubernetes concepts

Kubernetes orchestrates containers across a cluster of machines,
built around a small set of core objects an administrator or developer
composes together:

| Object | Role |
| --- | --- |
| Pod | The smallest deployable unit — one or more co-located, co-scheduled containers |
| Deployment | Declares a desired number of pod replicas and manages rolling updates |
| Service | A stable network identity/load-balancing endpoint in front of a set of pods |
| Namespace | A logical partition of a cluster for multi-tenancy and resource scoping |
| ConfigMap / Secret | Externalized configuration and sensitive values injected into pods |

Kubernetes reconciles actual cluster state toward this declared desired
state continuously — the same declarative, reconciliation-based model
this encyclopedia applies to infrastructure as code elsewhere.

### OpenShift foundations

**Red Hat OpenShift** is an enterprise Kubernetes platform built on top
of upstream Kubernetes, adding an opinionated, supported operational
layer rather than replacing Kubernetes' core objects:

- **Integrated developer and administrator console** — a web UI for
  both cluster operations and application deployment, complementing
  `kubectl`/`oc` CLI access.
- **Routes** — OpenShift's layer built on top of (and largely
  superseding the need to hand-configure) Kubernetes Ingress, exposing
  a Service externally with integrated TLS handling.
- **Source-to-Image (S2I)** — builds a container image directly from
  application source code and a language-specific builder image,
  without requiring the developer to author a Containerfile for common
  frameworks.
- **Operators** — packaged, Kubernetes-native applications that also
  encode their own day-2 operational knowledge (upgrades, backup,
  scaling), extending the Kubernetes API with custom resources rather
  than relying on external scripts.
- **Integrated security defaults** — including Security Context
  Constraints (SCCs), OpenShift's admission-control layer restricting
  what a pod is permitted to do (comparable in spirit to SELinux's
  role at the OS level, applied at the cluster-scheduling layer
  instead).

For hands-on local exploration, **CRC (CodeReady Containers)** runs a
minimal, single-node OpenShift cluster inside a VM on a workstation or
lab host, letting an administrator learn OpenShift concepts without a
multi-node production cluster.

## Design Considerations

- **Rootless by default, rootful by exception.** Default new container
  workloads to rootless Podman; justify rootful operation per workload
  (privileged port binding, specific device access) rather than
  running everything as root out of habit carried over from Docker
  workflows.
- **Quadlet vs. ad hoc `podman run` in scripts.** Any container
  intended to persist across reboots or be observable/restartable like
  a normal service belongs in a Quadlet unit, not a `podman run`
  invoked from `rc.local` or a login profile — this mirrors the
  systemd unit-vs-cron-script design point from [Chapter 03](03-boot-systemd-processes-logging-and-scheduled-work.md).
  Interactive, disposable containers (`podman run --rm` for local
  testing) are the appropriate place for ad hoc invocation.
- **Image provenance and registry trust.** Decide which registries are
  trusted for pulls (`/etc/containers/registries.conf`) before a
  fleet-wide default of "search everywhere" becomes an established
  habit; an unscoped image source is a supply-chain risk regardless of
  how well the runtime itself is hardened.
- **Podman as a Kubernetes/OpenShift on-ramp, not a replacement.**
  Podman is well suited to single-host workloads, CI build steps, and
  local development against pod definitions later deployed to a
  cluster; multi-host orchestration, scheduling, and self-healing at
  scale are Kubernetes/OpenShift's job, not Podman's — design the
  handoff between the two deliberately rather than trying to scale
  single-host Podman into a substitute orchestrator.
- **OpenShift adoption scope.** A full OpenShift cluster is a
  significant operational commitment (control plane nodes, storage,
  networking, ongoing platform upgrades); CRC and a scoped pilot are
  appropriate ways to validate developer and platform-team readiness
  before a production cluster commitment.

## Implementation and Automation

### 1. Basic Podman operations

```bash
# Rootless by default for a normal user
podman run -d --name web1 -p 8080:80 registry.access.redhat.com/ubi9/httpd-24

podman ps
podman logs web1
podman inspect web1 --format '{{.State.Status}}'

# Stop, remove, and clean up
podman stop web1
podman rm web1

# Pull and inspect an image without running it
podman pull registry.access.redhat.com/ubi9/ubi-minimal
podman images
```

### 2. Building an image from a Containerfile

```bash
mkdir -p ~/lab-app && cd ~/lab-app
cat > Containerfile <<'EOF'
FROM registry.access.redhat.com/ubi9/ubi-minimal
RUN microdnf install -y httpd && microdnf clean all
COPY index.html /var/www/html/index.html
EXPOSE 80
CMD ["httpd", "-D", "FOREGROUND"]
EOF
echo "<h1>lab-app</h1>" > index.html

podman build -t localhost/lab-app:1.0 .
podman run -d --name lab-app -p 8081:80 localhost/lab-app:1.0
curl -s http://localhost:8081/
```

### 3. Docker CLI compatibility

```bash
dnf install -y podman-docker

# The docker command now transparently invokes podman
docker ps
docker run -d --name compat-test -p 8082:80 localhost/lab-app:1.0
```

### 4. Pods and podman play kube

```bash
# Create a pod with two containers sharing a network namespace
podman pod create --name lab-pod -p 8090:80
podman run -d --pod lab-pod --name lab-pod-app localhost/lab-app:1.0
podman ps --pod

# Export the pod definition as Kubernetes-compatible YAML
podman generate kube lab-pod > lab-pod.yaml
cat lab-pod.yaml

# Tear down and recreate purely from the exported YAML
podman pod rm -f lab-pod
podman play kube lab-pod.yaml
```

### 5. Running a container as a Quadlet-managed systemd service

```bash
mkdir -p ~/.config/containers/systemd
cat > ~/.config/containers/systemd/lab-app.container <<'EOF'
[Unit]
Description=Lab app container managed by Quadlet

[Container]
Image=localhost/lab-app:1.0
PublishPort=8091:80

[Service]
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now lab-app.service
systemctl --user status lab-app.service
loginctl enable-linger "$(whoami)"   # keep the user service running after logout
```

### 6. Local OpenShift exploration with CRC

```bash
# Install and start a local single-node cluster (large download; run only in a lab)
crc setup
crc start

eval $(crc oc-env)
oc login -u developer https://api.crc.testing:6443

# Deploy an application using Source-to-Image
oc new-project lab-project
oc new-app python:3.12~https://github.com/example/sample-python-app
oc expose svc/sample-python-app
oc get routes
```

## Validation and Troubleshooting

- **Confirm rootless vs. rootful state.** `podman info --format
  '{{.Host.Security.Rootless}}'` confirms which mode a given
  invocation is running in; a container that needs to bind a
  privileged port or access a host device failing under a plain
  `podman run` is frequently a rootless-vs-rootful mismatch, not an
  application bug.
- **Diagnose a container that exits immediately.** `podman logs
  <name>` shows the container's own output; `podman inspect <name>
  --format '{{.State.ExitCode}}'` confirms the exit code — this is the
  container-runtime equivalent of the systemd `ExecStart` diagnosis
  pattern from [Chapter 03](03-boot-systemd-processes-logging-and-scheduled-work.md), and the two should be checked with the same
  discipline.
- **Diagnose a Quadlet unit that never appears.** Quadlet files must be
  syntactically correct and in the expected directory
  (`~/.config/containers/systemd/` for rootless user units,
  `/etc/containers/systemd/` for rootful system units); confirm with
  `systemctl --user list-unit-files | grep <name>` (or without
  `--user` for rootful) after `daemon-reload`, and check
  `/usr/lib/systemd/system-generators/podman-system-generator`
  execution via `systemd-analyze --user` if the unit is simply absent.
- **Diagnose networking between containers in a pod vs. across
  pods.** Containers in the same pod share a network namespace and
  reach each other over `localhost`; containers in different pods
  need an explicit `podman network` or Kubernetes/OpenShift Service —
  "why can't my two containers reach each other" is very often this
  distinction.
- **Diagnose an image pull failure.** Check
  `/etc/containers/registries.conf` for the configured search order
  and any blocked registries; `podman pull --log-level=debug <image>`
  surfaces authentication and TLS errors that the default output
  summarizes too tersely to act on directly.
- **Diagnose an OpenShift/CRC application that will not build or
  deploy.** `oc get events -n <project>` and `oc logs
  build/<build-name>` are the first two commands for a failed S2I
  build; `oc get pods` plus `oc describe pod <pod>` are the
  equivalents for a pod that will not reach `Running`, mirroring the
  `systemctl status`/`journalctl` pairing used for plain systemd
  services throughout this volume.
- **Common failure: forgetting `loginctl enable-linger` for rootless
  Quadlet/systemd user services.** Without lingering enabled, a
  rootless user's systemd instance (and everything it manages) stops
  when that user's last session ends, which looks like a container
  crashing for no reason shortly after an administrator logs out.

## Security and Best Practices

- Default to rootless Podman for new workloads, and treat a request
  for rootful operation as requiring the same justification as a
  request for root shell access anywhere else.
- Scope `/etc/containers/registries.conf` to an explicit, trusted
  registry allowlist rather than the unrestricted default search
  behavior, and enable `podman pull --tls-verify` (the default)
  everywhere except a deliberately configured, trusted internal
  registry.
- Build images from minimal, Red Hat–maintained base images (UBI —
  Universal Base Image) where possible, and rebuild images on a
  schedule to pick up base-image security patches rather than treating
  a built image as permanent.
- Prefer Quadlet-managed containers over ad hoc `podman run` for
  anything running unattended, so container workloads inherit the same
  restart, logging, and resource-control discipline as native systemd
  services.
- Apply the principle of least privilege inside Kubernetes/OpenShift
  the same way it is applied at the OS level: scope Security Context
  Constraints and RBAC roles narrowly, and avoid granting the
  cluster-admin-equivalent role to workloads or users that only need
  namespace-scoped access.
- Scan built images for known vulnerabilities before promoting them
  beyond a development registry, and treat an image's vulnerability
  scan the same way `dnf`/`rpm` package auditing is treated elsewhere
  in this volume — a routine, automated gate, not an occasional manual
  check.
- Keep container engine and orchestration platform versions current
  against [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) and
  vendor security advisories; container runtime CVEs are a direct
  path to host compromise when unpatched.

## References and Knowledge Checks

**References**

- [`podman(1)`, `podman-run(1)`, `containers.conf(5)` man pages.](https://docs.podman.io/en/latest/markdown/podman.1.html)
- [`quadlet(5)` man page](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) — Quadlet unit file syntax.
- [Podman documentation](https://docs.podman.io/) — rootless containers and Docker compatibility,
  podman.io.
- [Kubernetes documentation](https://kubernetes.io/docs/home/) — Pods, Deployments, and Services concepts.
- [Red Hat OpenShift Container Platform documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/) — Routes, S2I,
  Operators, and Security Context Constraints.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Kubernetes
  baseline referenced in this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. What specific operational risk does Podman's daemonless architecture
   eliminate that exists in Docker's `dockerd` model?
2. How does a Linux user namespace make a rootless container's
   internal "root" user meaningfully less dangerous than true host
   root?
3. Why is Quadlet preferred over a hand-written systemd unit wrapping
   `podman run` for a container that must persist across reboots?
4. What does an OpenShift Route add on top of a plain Kubernetes
   Service, and what does Source-to-Image remove from the standard
   "write a Containerfile" workflow?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each container skill** — Podman
basics, persistent storage, containers as systemd services, and Kubernetes/OpenShift
foundations. Containers are **no longer on the RHEL 10 RHCSA blueprint**, so treat these as
platform-engineering and RHCE-adjacent skills rather than exam objectives. Every step is a
runnable RHEL 10 command. Each ends **`**Lab verified by:** *pending*`** until a human runs
it.

**Shared prerequisites for Labs 8.1–8.4** — a RHEL 10 system with `sudo`, `podman` installed,
and (for Lab 8.4) access to a Kubernetes/OpenShift cluster or `kind`/CRC. **Cost:** none.

### Lab 8.1 — Podman basics, rootless (Topic: Podman)

**Objective:** Run and manage a container without root.

```bash
podman run -d --name web -p 8080:80 registry.access.redhat.com/ubi9/httpd-24
podman ps
curl -s http://localhost:8080/ | head -1
podman logs web | tail -3
```

**Expected result:** the container runs **rootless** (as your user, no `sudo`), serves on
8080, and `podman ps`/`logs` inspect it — Podman is the daemonless, rootless container engine
on RHEL; rootless operation is a key security advantage over a root daemon.

**Negative test:** publish to a privileged port (`-p 80:80`) as a rootless user; it is denied
(ports <1024 need privilege) — rootless containers map to high ports unless the sysctl/
capability is granted.

**Cleanup:** `podman rm -f web`.

### Lab 8.2 — Persistent storage with volumes (Topic: Container storage)

**Objective:** Persist container data across restarts.

```bash
mkdir -p ~/cdata && echo "persistent" > ~/cdata/index.html
podman run -d --name web2 -p 8081:8080 \
  -v ~/cdata:/var/www/html:Z registry.access.redhat.com/ubi9/httpd-24
curl -s http://localhost:8081/ | head -1
podman rm -f web2 ; ls ~/cdata/index.html    # data survives the container
```

**Expected result:** the container serves the host file, and the data remains after the
container is removed — a bind mount (`-v`, with `:Z` to set the SELinux label) decouples data
lifetime from container lifetime, the basis for stateful containers.

**Negative test:** bind-mount a host directory without `:Z` under enforcing SELinux; the
container gets permission denied on the volume — `:Z`/`:z` relabels the content so the
container may access it.

**Cleanup:** `rm -rf ~/cdata`.

### Lab 8.3 — Containers as systemd services (Topic: Container services)

**Objective:** Run a container under systemd with a Quadlet unit.

```bash
mkdir -p ~/.config/containers/systemd
cat > ~/.config/containers/systemd/web.container <<'EOF'
[Container]
Image=registry.access.redhat.com/ubi9/httpd-24
PublishPort=8082:8080

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user start web.service
systemctl --user status web.service --no-pager | head
```

**Expected result:** systemd generates and starts a service from the Quadlet `.container`
unit, so the container is managed like any service (start on boot, restart on failure) —
Quadlet is the modern RHEL way to run containers under systemd, replacing
`podman generate systemd`.

**Negative test:** expect a plain `podman run` container to restart after a reboot; it does
not — only a systemd-managed (Quadlet) unit gives you boot-time start and restart policy.

**Cleanup:** `systemctl --user stop web.service; rm ~/.config/containers/systemd/web.container;
systemctl --user daemon-reload`.

### Lab 8.4 — Kubernetes/OpenShift foundations (Topic: Orchestration)

**Objective:** Deploy a pod and read its state.

```bash
kubectl run web --image=registry.access.redhat.com/ubi9/httpd-24 --port=8080
kubectl get pods -o wide
kubectl describe pod web | sed -n '1,20p'
# On OpenShift, the equivalent is: oc new-app / oc get pods
```

**Expected result:** the pod is scheduled and reaches `Running`; `describe` shows events and
node placement — Kubernetes/OpenShift orchestrate containers across nodes (scheduling,
scaling, self-healing), the platform layer above single-host Podman.

**Negative test:** treat a single Podman host as a substitute for orchestration for a
multi-node HA app; it has no scheduling, scaling, or self-healing — that is precisely what
Kubernetes/OpenShift add.

**Cleanup:** `kubectl delete pod web`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Podman's daemonless, rootless-capable, pod-native architecture
eliminates the always-on privileged daemon at the center of Docker's
model while remaining largely command-compatible through
`podman-docker`. Quadlet extends the same systemd supervision,
restart, and logging discipline used throughout this volume to
container workloads. Kubernetes generalizes the pod concept to
multi-host orchestration, and OpenShift layers a supported developer
and operator experience — routes, Source-to-Image, Operators, and
Security Context Constraints — on top of that same Kubernetes
foundation.

- [ ] Can explain the architectural differences between Podman and
      Docker, including rootless operation.
- [ ] Can build a Containerfile-based image and run it as a
      Quadlet-managed systemd service.
- [ ] Can create a multi-container pod and export/import it as
      Kubernetes-compatible YAML.
- [ ] Can describe core Kubernetes objects and what OpenShift adds on
      top of them.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
