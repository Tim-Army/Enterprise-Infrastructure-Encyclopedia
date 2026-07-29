# Chapter 08: Orchestration with Kubernetes and Security

## Learning Objectives

- Explain Kubernetes basics (pods, deployments, services) alongside Docker.
- Scan images for vulnerabilities.
- Sign and verify images with content trust.
- Harden containers (rootless, non-root user, least privilege).
- Complete a walkthrough for each Kubernetes-and-security topic.

## Theory and Architecture

The **Orchestration** domain also covers **Kubernetes**, and the **Security** domain (~15%) rounds out the
exam. On the orchestration side, the DCA expects Kubernetes fundamentals: a **pod** is the smallest
deployable unit (one or more containers), a **Deployment** manages replicated pods with rolling updates,
and a **Service** gives them a stable network endpoint — the same "declare desired state, controller
reconciles" model as Swarm, at larger scale. On **security** — all **defensive**: **image scanning**
finds known CVEs in image layers before deploy; **Docker Content Trust (DCT)** uses Notary to **sign**
images so only signed images run; **secrets** (Swarm/Kubernetes) keep credentials out of images and env
vars; running as a **non-root user** (`USER` in the Dockerfile) and **rootless mode** (the daemon and
containers run as an unprivileged user) shrink the blast radius; and **seccomp**/**AppArmor** profiles,
**read-only** root filesystems, and dropped **capabilities** enforce least privilege. Securing your own
images and containers is the goal. This chapter teaches Kubernetes basics and security with hands-on
walkthroughs.

## Design Considerations

Understand the **pod → Deployment → Service** model for Kubernetes. On security: **scan** images in the
pipeline and fix high CVEs; **sign** images with DCT and verify on pull; store credentials as **secrets**;
run as a **non-root user** and consider **rootless** mode; drop Linux **capabilities**, use **read-only**
root filesystems and **seccomp/AppArmor**; never expose the **daemon socket** to containers. Least
privilege at every layer.

## Implementation and Automation

The labs reason about the Kubernetes objects, scan an image, reason about content trust, and run a
hardened non-root container — the Kubernetes and defensive security the domains validate.

## Validation and Troubleshooting

Confirm Kubernetes and security:

```text
Kubernetes: pod (smallest unit) -> Deployment (replicas + rolling update) -> Service (stable endpoint)
Security (defensive): image scan (CVEs) | Docker Content Trust (sign/verify via Notary) | secrets
Harden: non-root USER + rootless mode + drop capabilities + read-only rootfs + seccomp/AppArmor
Never mount the docker.sock into containers (root-equivalent)
```

Common pitfalls: running containers as **root** by default (unnecessary privilege); and deploying
**unscanned/unsigned** images — scan and sign in the pipeline.

## Security and Best Practices

Everything here is **defensive**: scanning, signing, secrets, non-root/rootless, and least-privilege
profiles protect **your own** images and clusters. There is no offensive content. Never expose the daemon
socket. All work is authorized administration of your own environment.

## Hands-On Lab

Kubernetes-and-security walkthroughs (defensive). **Shared prerequisites** — the Docker Engine (with
`docker scout` or a scanner where available), and `python3`. **Cost:** none.

### Lab 8.1 — Reason about the Kubernetes objects

**Objective:** Map the core Kubernetes model.

```python
python3 - <<'PY'
objects = {
  "Pod":        "smallest deployable unit (1+ containers sharing net/storage)",
  "Deployment": "manages replicated pods + rolling updates (desired replica count)",
  "Service":    "stable network endpoint / load balancing across pods",
  "ConfigMap/Secret": "config and credentials injected into pods",
}
for o, role in objects.items(): print(f"{o:18}: {role}")
print("Same declarative reconcile model as Swarm services, at larger scale")
PY
```

**Expected result:** the pod → Deployment → Service model mapped — Kubernetes fundamentals for the DCA.

**Negative test:** run bare pods for a scaled app; a **Deployment** manages replicas and rolling updates.

**Cleanup:** none.

### Lab 8.2 — Scan an image for vulnerabilities

**Objective:** Find CVEs before deploy.

```bash
docker scout cves nginx:alpine --only-severity critical,high 2>/dev/null | tail -5 || \
  echo "use docker scout / trivy to scan images for CVEs"
```

```text
  ✓ 0 critical, 2 high  (fix: upgrade base image / patched tag)
```

**Expected result:** a scan reporting the image's high/critical CVEs — a fix-before-deploy signal.

**Negative test:** deploy an unscanned base image; **scan** it and patch/upgrade high-severity CVEs first.

**Cleanup:** none.

### Lab 8.3 — Reason about content trust

**Objective:** Run only signed images.

```python
python3 - <<'PY'
# DOCKER_CONTENT_TRUST=1 makes push sign and pull verify (via Notary)
print("export DOCKER_CONTENT_TRUST=1")
print("docker push registry/app:1.0  -> signs the image")
print("docker pull registry/app:1.0  -> verifies signature; UNSIGNED image is REFUSED")
print("Rule: enforce Content Trust so only signed images run")
PY
```

**Expected result:** content trust signing on push and verifying on pull — unsigned images refused.

**Negative test:** pull and run any tag without verification; enable **Docker Content Trust** to require
signatures.

**Cleanup:** none.

### Lab 8.4 — Run a hardened non-root container

**Objective:** Least privilege at runtime.

```bash
docker run --rm \
  --user 1000:1000 \
  --read-only --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  alpine:3.20 id
```

```text
uid=1000 gid=1000 groups=1000
```

**Expected result:** the container running as non-root, read-only, with all capabilities dropped and no
privilege escalation — a hardened runtime.

**Negative test:** run as **root** with default capabilities and a writable root filesystem; drop
privileges (**non-root**, `--cap-drop ALL`, `--read-only`, `no-new-privileges`).

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The DCA covers Kubernetes fundamentals (pods, Deployments, Services — the declarative reconcile model at
scale) and defensive container security: scanning images for CVEs, signing and verifying with Docker
Content Trust, storing credentials as secrets, and hardening the runtime with non-root users, rootless
mode, dropped capabilities, read-only filesystems, and seccomp/AppArmor — never exposing the daemon
socket.

- [ ] I can explain the Kubernetes pod/Deployment/Service model.
- [ ] I can scan an image for vulnerabilities.
- [ ] I can reason about content trust.
- [ ] I can run a hardened non-root container.
- [ ] I completed Labs 8.1–8.4 including each negative test.
