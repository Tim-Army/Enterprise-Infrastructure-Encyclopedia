# Chapter 01: Container Architecture, Images, Runtimes, and Registries

## Learning Objectives

- Explain how Linux namespaces, control groups (cgroups v2), and capabilities
  combine to isolate a container process from the host.
- Describe the OCI Image Specification, Runtime Specification, and
  Distribution Specification, and how each governs interoperability between
  build tools, runtimes, and registries.
- Differentiate the high-level runtime layer (Docker Engine, Podman,
  containerd, CRI-O) from the low-level runtime layer (runc, crun, gVisor,
  Kata Containers) and explain where the Container Runtime Interface (CRI)
  fits between kubelet and the runtime.
- Build a minimal, non-root, multi-stage container image with a Dockerfile
  and produce a multi-architecture manifest list with `buildx`.
- Push, pull, scan, and cryptographically sign a container image against an
  OCI-compliant registry.

## Theory and Architecture

A container is not a virtual machine. It is a standard Linux process that the
kernel has been told to see a restricted view of the system through. Three
kernel primitives make that restriction possible, and every runtime discussed
in this chapter — Docker, Podman, containerd, CRI-O — is ultimately a
convenience layer over the same three mechanisms.

**Namespaces** partition a global kernel resource so a process believes it has
its own private copy. The Linux kernel provides eight namespace types that
matter for container engineering: `PID` (process tree), `NET` (network
stack), `MNT` (filesystem mounts), `UTS` (hostname/domain), `IPC`
(inter-process communication primitives), `USER` (UID/GID mapping),
`CGROUP` (cgroup root view), and `TIME` (boot/monotonic clocks, since Linux
5.6). A container is, at minimum, a process launched into a fresh set of
these namespaces.

**Control groups (cgroups)** meter and bound what a process (or namespace) is
allowed to consume: CPU shares and quotas, memory limits and OOM behavior,
block I/O weight, and PID counts. Kubernetes 1.31.x assumes **cgroup v2**
(the unified hierarchy) on the node; cgroup v1 support is effectively legacy
and several kubelet features (memory QoS, swap accounting) require v2.
Requests and limits set in a pod spec are translated by the kubelet and CRI
runtime into cgroup v2 controller settings on the container's cgroup.

**Capabilities** split the monolithic root privilege into 40-plus discrete
grants (`CAP_NET_BIND_SERVICE`, `CAP_SYS_ADMIN`, `CAP_CHOWN`, and so on).
Container runtimes drop most capabilities by default and add back a small
default set; a security-conscious image drops all of them and adds back only
what the workload needs. Seccomp (filtering allowed syscalls) and, on Debian-
and SUSE-family hosts, AppArmor or SELinux (mandatory access control on file
and process labels) provide additional layers on top of namespaces, cgroups,
and capabilities.

### The runtime stack, layer by layer

```text
kubectl / docker CLI / podman CLI
        │
        ▼
High-level runtime  (containerd, CRI-O, Docker Engine, Podman)
   - image pull, unpack, storage/snapshot management
   - exposes CRI (gRPC) to the kubelet
        │
        ▼
Low-level runtime   (runc, crun, gVisor/runsc, Kata Containers)
   - OCI Runtime Spec consumer: creates namespaces, cgroups,
     sets capabilities/seccomp, execs the container process
        │
        ▼
Linux kernel (namespaces, cgroups v2, capabilities, seccomp, LSM)
```

Kubernetes talks to the node's high-level runtime exclusively through the
**Container Runtime Interface (CRI)**, a gRPC API defined by
`k8s.io/cri-api`. This is why Kubernetes 1.31.x can run identically on nodes
using **containerd** or **CRI-O** — dockershim was removed in Kubernetes
1.24, and Docker Engine is no longer a supported node runtime unless fronted
by `cri-dockerd`. containerd and CRI-O both delegate the actual process
creation to a low-level, OCI Runtime Spec–compliant binary, almost always
**runc**. Alternative low-level runtimes swap out that final step:
**gVisor** (`runsc`) interposes a user-space kernel that intercepts
syscalls for stronger isolation at a performance cost, and **Kata
Containers** runs each pod's containers inside a lightweight
hardware-virtualized VM, trading some density for a true VM security
boundary. Both integrate with Kubernetes through the `RuntimeClass` API,
covered in the Design Considerations section below.

### The three OCI specifications

The Open Container Initiative defines three specifications that keep this
stack interoperable regardless of which vendor's tool produced or consumes
an artifact:

| Specification | Governs | Reference implementation examples |
| --- | --- | --- |
| **OCI Image Spec** | Layout of an image: config JSON, manifest, layer tarballs (typically gzip-compressed tar diffs), media types | `docker build`, `buildah`, `img`, `kaniko`, Cloud Native Buildpacks |
| **OCI Runtime Spec** | The `config.json` contract a low-level runtime consumes to create a container from an unpacked bundle | `runc`, `crun`, `runsc`, `kata-runtime` |
| **OCI Distribution Spec** | The HTTP API for pushing/pulling image content (`/v2/<name>/manifests/<reference>`, content-addressable blobs) | Docker Hub, Harbor, Amazon ECR, GHCR, Quay, `zot` |

An **image** is layers plus a config object; layers are content-addressed by
the SHA-256 digest of their (typically) compressed tar content and are
stacked with a union filesystem — almost always **overlayfs** on Linux nodes
— at container start. Because layers are addressed by digest and shared
across images, pulling a second image that shares a base layer with an
already-cached image only transfers the delta. A **manifest list** (also
called an image index) lets one human-readable tag (`app:1.4.0`) resolve to
different per-architecture manifests (`linux/amd64`, `linux/arm64`), which is
how `docker buildx build --platform linux/amd64,linux/arm64` produces a
single pushable reference that resolves correctly on both Intel/AMD nodes and
Graviton/Ampere nodes.

## Design Considerations

**Base image selection is an attack-surface decision, not just a size
decision.** A full distribution base (`ubuntu:24.04`, `debian:12`) gives you
a shell, a package manager, and libc tooling for debugging, at the cost of
hundreds of megabytes of packages that are rarely patched inside the image
after build time. Distroless images (`gcr.io/distroless/*`) and `scratch`
strip everything except the language runtime and the application, which
shrinks the CVE surface an image scanner reports but also removes the shell
an attacker — or an on-call engineer — would use to `exec` in. The common
production pattern is a multi-stage build: compile or `npm install` in a
full-featured builder stage, then `COPY --from=builder` only the compiled
artifact into a minimal runtime stage.

**Rootless vs. rootful matters for both the build and the run path.** Podman
and `buildah` run daemonless and support fully rootless builds and rootless
container execution, mapping container UID 0 to an unprivileged host UID via
user namespaces. Docker Engine historically required a root daemon; recent
Docker Engine releases support a rootless mode, but it is not the default. In
Kubernetes, the equivalent decision is enforced per-pod through
`securityContext.runAsNonRoot` and `runAsUser`, and cluster-wide through
Pod Security admission ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md)) — but the image itself should not
require root to begin with. Baking a `USER` directive into the Dockerfile is
a control that survives even if a cluster's admission policy is
misconfigured.

**Tag mutability is a supply-chain decision.** A floating tag (`latest`,
`stable`, even a semantic version like `1.4`) can be repointed to different
content after you have already tested and approved it. Production manifests
should pin to an immutable digest (`app@sha256:...`) or, at minimum, a fully
qualified, non-floating tag, with the digest recorded in the deployment
pipeline's provenance record ([Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md)). Registries that support tag
immutability policies (Harbor project-level immutability rules, ECR tag
immutability) should have it enabled for any tag pattern used in production.

**Registry topology affects both reliability and egress cost.** A single
upstream registry dependency (Docker Hub, a public GHCR namespace) becomes a
pull-rate-limit and availability risk at cluster scale. Enterprise patterns
mirror or pull-through-cache upstream images into a registry you control
(Harbor, an internal `zot` instance, or a cloud registry with a pull-through
cache feature) and configure containerd's `registry` mirror settings so
nodes resolve `docker.io/library/nginx` to the internal mirror transparently.
This also gives you a single point to enforce scanning and signature
verification before an image is ever reachable from a cluster node.

## Implementation and Automation

### A minimal, non-root, multi-stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.23-bookworm AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian12:nonroot AS runtime
WORKDIR /app
COPY --from=builder /out/app /app/app
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/app"]
```

The builder stage never ships; only the compiled static binary crosses into
the `distroless/static` runtime stage, which has no shell, no package
manager, and a non-root default user baked in. Build and inspect the result:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  --tag registry.example.internal/platform/app:1.4.0 \
  --push .

docker buildx imagetools inspect registry.example.internal/platform/app:1.4.0
```

### Producing a Software Bill of Materials and scanning

```bash
# Generate an SPDX SBOM for the built image.
syft registry.example.internal/platform/app:1.4.0 -o spdx-json > app-1.4.0.sbom.json

# Scan for known vulnerabilities; fail the pipeline on HIGH/CRITICAL.
trivy image --severity HIGH,CRITICAL --exit-code 1 \
  registry.example.internal/platform/app:1.4.0
```

### Signing and verifying with Sigstore cosign (keyless, OIDC-based)

```bash
# Sign the pushed digest using the CI identity's OIDC token — no long-lived key material.
cosign sign --yes registry.example.internal/platform/app@sha256:<digest>

# Verify at deploy time, pinning to the expected CI identity and issuer.
cosign verify \
  --certificate-identity "https://ci.example.internal/app-build" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  registry.example.internal/platform/app@sha256:<digest>
```

### Working with Podman and containerd's native CLIs

```bash
# Rootless build and run with Podman — no daemon, mapped user namespace.
podman build -t app:1.4.0 .
podman run --rm -p 8080:8080 app:1.4.0

# Inspecting images directly against a containerd namespace (node-level debugging).
sudo ctr -n k8s.io images ls
sudo crictl images
sudo crictl pull registry.example.internal/platform/app:1.4.0
```

`nerdctl` provides a Docker-CLI-compatible front end for containerd,
including `nerdctl compose` support, and is useful when you want
Docker-familiar ergonomics against the same containerd that Kubernetes nodes
run.

## Validation and Troubleshooting

Confirm the image was built as intended before it ever reaches a cluster:

```bash
# Layer-by-layer history, including the effective USER and ENTRYPOINT.
docker history --no-trunc registry.example.internal/platform/app:1.4.0
docker inspect registry.example.internal/platform/app:1.4.0 \
  --format '{{.Config.User}} {{.Config.Entrypoint}}'

# Confirm the manifest list actually contains both architectures before relying on it.
crane manifest registry.example.internal/platform/app:1.4.0 | jq '.manifests[].platform'
```

Common failure modes and their diagnostics:

| Symptom | Likely cause | Diagnostic |
| --- | --- | --- |
| `exec /app/app: permission denied` at container start | Binary lacks execute bit after `COPY`, or `USER` cannot read the file | `docker run --entrypoint sh <image>` against an intermediate debug stage, or add a temporary debug stage with a shell |
| `no match for platform in manifest` on an ARM node | Image was built single-arch and pushed without `buildx --platform` | `crane manifest` / `docker buildx imagetools inspect` to confirm platforms present |
| Cluster nodes cannot pull from the internal registry | Missing `imagePullSecrets`, or containerd's `certs.d` mirror config is stale on the node | `crictl pull <image>` directly on the node to isolate kubelet vs. runtime vs. registry |
| Rootless Podman build fails on `mkdir: permission denied` | Host `/etc/subuid` / `/etc/subgid` ranges not configured for the build user | `podman unshare cat /proc/self/uid_map`; verify subuid/subgid entries exist |
| Signature verification fails at admission time | Image was rebuilt/re-pushed after signing, changing the digest | Compare the digest referenced in the deployment manifest against `crane digest` output |

For interactive debugging of a running container without a shell baked into
the image, use an **ephemeral debug container** rather than adding tooling to
the production image — this is covered in depth for Kubernetes pods in
[Chapter 03](03-kubernetes-workloads-scheduling-and-capacity.md), and the same `crictl` / `ctr` node-level tooling above applies
when the failure is below the pod abstraction, at the runtime or image layer.

## Security and Best Practices

- Build `FROM` a minimal, actively maintained base; prefer distroless or
  purpose-built minimal images over general-purpose distribution images for
  production runtime stages.
- Always set an explicit non-root `USER` in the image; do not rely solely on
  cluster-side `runAsNonRoot` to catch an image that defaults to root.
- Drop all Linux capabilities in the image/runtime and add back only what is
  required (`cap_drop: ["ALL"]`, `cap_add: [...]` for the few needed).
- Generate and retain an SBOM for every image at build time; store it
  alongside build provenance so a future CVE disclosure can be answered by a
  query instead of a re-scan of production.
- Scan every image before it is promoted past a development registry, and
  gate promotion on severity thresholds rather than scanning only in CI as
  an informational step.
- Sign every image that reaches a production registry and enforce signature
  verification at cluster admission ([Chapter 06](06-kubernetes-identity-configuration-policy-and-security.md) and [Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md) cover the
  admission-side enforcement with Kyverno/cosign policies).
- Prefer immutable digests in deployment manifests; if tags must be used,
  enable registry-side tag immutability for production tag patterns.
- Mirror or pull-through-cache all upstream base images through a registry
  you control so you can enforce scanning before an unreviewed image ever
  reaches a node.
- Enable content trust / provenance attestation (SLSA-style build
  provenance, in-toto attestations) so a consumer can verify not just what
  is in an image but how and where it was built — expanded in [Chapter 07](07-cloud-native-delivery-gitops-and-software-supply-chains.md).

## References and Knowledge Checks

**Authoritative references**

- Open Container Initiative, [Image Format Specification](https://github.com/opencontainers/image-spec), [Runtime Specification](https://github.com/opencontainers/runtime-spec), and [Distribution Specification](https://github.com/opencontainers/distribution-spec).
- Kubernetes documentation, [Container Runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) and [Container Runtime Interface (CRI)](https://kubernetes.io/docs/concepts/architecture/cri/), version 1.31.x baseline per [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).
- containerd documentation, [containerd.io](https://containerd.io/docs/).
- Sigstore project documentation, [cosign](https://docs.sigstore.dev/cosign/signing/overview/).
- Anchore, [syft](https://github.com/anchore/syft) and Aqua Security, [Trivy](https://aquasecurity.github.io/trivy/).

**Knowledge check**

1. Which OCI specification defines the HTTP API a registry must implement,
   and which defines the on-disk bundle a low-level runtime consumes?
2. Why does the removal of dockershim in Kubernetes 1.24 mean Docker Engine
   is no longer directly usable as a node's CRI runtime, and what bridges
   that gap when it is required?
3. What is the practical security difference between running a workload
   under runc versus under Kata Containers, and when would the added
   isolation of Kata justify its overhead?
4. Why is pinning to an image digest a stronger supply-chain control than
   pinning to a semantic-version tag, even a specific one like `1.4.0`?
5. Name two reasons an organization would run a pull-through cache or mirror
   registry rather than allowing nodes to pull directly from public
   registries.

## Hands-On Lab

**Objective:** Build a minimal non-root image, run a local OCI-compliant
registry, push/pull/scan/sign the image, and verify a tampering scenario is
detectable.

### Prerequisites

- Docker Engine 25.x+ or Podman 5.x with `buildx`/native multi-arch support.
- `trivy`, `syft`, and `cosign` CLIs installed locally.
- `jq` installed.
- Network access to pull `gcr.io/distroless/static-debian12` and
  `registry:2` on first run.

### Procedure

1. Create a working directory and a minimal application.

   ```bash
   mkdir -p ~/labs/oci-image && cd ~/labs/oci-image
   cat > main.go <<'EOF'
   package main

   import ("fmt"; "net/http")

   func main() {
       http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
           fmt.Fprintln(w, "hello from a distroless container")
       })
       http.ListenAndServe(":8080", nil)
   }
   EOF
   cat > go.mod <<'EOF'
   module app
   go 1.23
   EOF
   ```

2. Write the multi-stage Dockerfile from the Implementation section above
   into `Dockerfile` in the same directory.

3. Start a local, unauthenticated OCI registry for the lab.

   ```bash
   docker run -d --name lab-registry -p 5000:5000 registry:2
   ```

4. Build and push the image to the local registry.

   ```bash
   docker build -t localhost:5000/app:1.0.0 .
   docker push localhost:5000/app:1.0.0
   ```

   **Expected result:** the push completes and reports a manifest digest,
   for example `1.0.0: digest: sha256:... size: 528`.

5. Verify the image runs as a non-root user and exposes the app.

   ```bash
   docker run -d --name app-test -p 8080:8080 localhost:5000/app:1.0.0
   curl -s http://localhost:8080/
   docker inspect app-test --format '{{.Config.User}}'
   ```

   **Expected result:** curl returns the hello message; `Config.User`
   reports `nonroot` (or its numeric UID), not empty/root.

6. Generate an SBOM and scan the pushed image.

   ```bash
   syft localhost:5000/app:1.0.0 -o table
   trivy image --severity HIGH,CRITICAL localhost:5000/app:1.0.0
   ```

   **Expected result:** Trivy reports the distroless base's minimal package
   set with few or no HIGH/CRITICAL findings, demonstrating the attack
   surface reduction from Chapter 01's Design Considerations.

7. Sign the pushed digest with cosign, using a local key pair for a
   registry that has no OIDC issuer configured in this lab.

   ```bash
   cosign generate-key-pair
   DIGEST=$(docker inspect localhost:5000/app:1.0.0 --format '{{index .RepoDigests 0}}' 2>/dev/null || \
     crane digest localhost:5000/app:1.0.0)
   cosign sign --key cosign.key localhost:5000/app@$(crane digest localhost:5000/app:1.0.0)
   ```

8. Verify the signature.

   ```bash
   cosign verify --key cosign.pub localhost:5000/app@$(crane digest localhost:5000/app:1.0.0)
   ```

   **Expected result:** cosign prints the verified claims and exits 0.

### Negative test

9. Push a modified image under the same tag, then attempt to verify the
   *original* signature against the *new* digest to confirm tampering is
   detected.

   ```bash
   echo "# tampered" >> Dockerfile
   docker build -t localhost:5000/app:1.0.0 .
   docker push localhost:5000/app:1.0.0
   cosign verify --key cosign.pub localhost:5000/app@$(crane digest localhost:5000/app:1.0.0)
   ```

   **Expected result:** verification fails with `no matching signatures`
   because the tampered image's digest was never signed — the tag moved,
   but the digest it now points to has no valid signature. This is the
   mechanism that makes digest-pinned, signature-verified deployments safe
   against a compromised or mistakenly overwritten tag.

### Cleanup

```bash
docker rm -f app-test lab-registry
docker rmi localhost:5000/app:1.0.0
rm -f cosign.key cosign.pub app-1.0.0.sbom.json
```

## Summary and Completion Checklist

Containers are ordinary Linux processes confined by namespaces, cgroups, and
capabilities; Kubernetes standardizes on the OCI Image, Runtime, and
Distribution specifications so that build tools, runtimes (containerd,
CRI-O, and their low-level runc/crun/gVisor/Kata backends), and registries
remain interchangeable. Minimal, non-root, multi-stage images reduce attack
surface; digest pinning, SBOM generation, scanning, and cosign signing turn
image supply chain integrity from a hope into a verifiable, enforceable
property.

- [ ] Can explain namespaces, cgroups v2, and capabilities as the three
      kernel primitives underlying container isolation.
- [ ] Can distinguish high-level runtimes (containerd, CRI-O) from
      low-level runtimes (runc, crun, gVisor, Kata) and the role of CRI.
- [ ] Can write a multi-stage, non-root Dockerfile and build a
      multi-architecture manifest list.
- [ ] Can push/pull against an OCI-compliant registry and inspect a
      manifest list's platforms.
- [ ] Can generate an SBOM, scan an image for vulnerabilities, and sign and
      verify an image digest with cosign.
- [ ] Completed the hands-on lab, including the tampered-image negative
      test, and performed cleanup.
