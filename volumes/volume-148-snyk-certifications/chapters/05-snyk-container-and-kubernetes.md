# Chapter 05: Snyk Container and Kubernetes

## Learning Objectives

- Explain container image scanning and the layered-image risk.
- Understand base-image recommendations — the multiplier fix.
- Place Kubernetes workload configuration in the security picture.
- Recognize the container as its own attack surface.

*Cert relevance: Snyk Container is the image-scanning engine — the packaging layer between your code and the cloud.*

## The container risk

A container image is not just your app — it is your app **plus an operating system**. A typical image layers your code on top of a **base image** (e.g. `node:20`, `python:3.12`, `ubuntu:22.04`) that brings a whole userland: system libraries, package managers, shells, utilities — each with its own vulnerabilities. You may have written perfect code and used clean dependencies, and still ship an image full of OS-level CVEs inherited from the base.

**Snyk Container** scans the **whole image** — every layer — and reports the vulnerabilities in the OS packages and system libraries, not just your application. This is a distinct surface from SCA (your language dependencies) and SAST (your code): here the flaw is in the **image's operating-system layer**, and it is often the largest source of raw CVE counts.

## The base-image multiplier

The signature Snyk Container move is the **base-image recommendation**. Because most image vulnerabilities come from the base image, and because *many* of your images share the *same* base, the highest-leverage fix is **changing the base image** — to a newer, slimmer, or better-patched variant that eliminates dozens of CVEs at once, across every image built on it.

This is the [code-to-cloud "fix at the source" lesson (CXLVII)](../../volume-147-wiz-certifications/chapters/06-wiz-code-shift-left.md) in container form: do not chase individual OS CVEs in individual images; **change the base**, and every image inheriting it is fixed. Snyk recommends the specific alternative base (often "switch to the slim or alpine variant, or bump the minor version") and quantifies how many vulnerabilities it removes. The lab models the multiplier.

## Kubernetes configuration

Beyond the image, **how the container runs** matters: a perfectly-patched image deployed with a **misconfigured Kubernetes manifest** — running as root, privileged, with no resource limits, with a host-path mount, with excessive capabilities — reintroduces risk the image scan cannot see. Snyk covers **Kubernetes workload configuration** (overlapping with [Snyk IaC, Chapter 6](06-snyk-infrastructure-as-code.md)): are your Pod specs following security best practice? The image and its runtime configuration are two halves of container security. The lab is covered within the base-image exercise and Chapter 6's IaC labs.

## Hands-On Lab

Python models container image analysis. **Cost:** none.

### Lab 5.1 — The base-image multiplier

**Objective:** See why changing the base image beats chasing individual CVEs.

```bash
python3 - <<'EOF'
# your image = your app layer + a base image (which brings most of the vulns)
IMAGE_VULNS = {
  "your app layer":       2,     # your code/deps (small)
  "base: node:20 (full)": 47,    # OS + system libs inherited from the base
}
total = sum(IMAGE_VULNS.values())
print("Image scan: vulnerabilities by layer")
for layer, n in IMAGE_VULNS.items():
    print(f"   {layer:24} {n} vulns")
print(f"   TOTAL: {total} vulns in the shipped image\n")
print(f"Note WHERE the vulns are: {IMAGE_VULNS['base: node:20 (full)']}/{total} come from the")
print("BASE IMAGE (OS + system libs you inherited), not your app.\n")

# base-image recommendation: switch full -> slim
RECOMMENDATION = {"base: node:20-slim": 9, "base: node:20-alpine": 4}
print("Snyk base-image RECOMMENDATION (change the base, fix many at once):")
for base, remaining in RECOMMENDATION.items():
    fixed = IMAGE_VULNS["base: node:20 (full)"] - remaining
    print(f"   switch to {base:22} -> removes {fixed} vulns (from 47 to {remaining})")
print("\nAnd the MULTIPLIER: if 30 of your images use node:20 as their base...")
IMAGES_SHARING_BASE = 30
print(f"   fixing individual CVEs: 47 vulns x {IMAGES_SHARING_BASE} images = "
      f"{47*IMAGES_SHARING_BASE} fixes, forever")
print(f"   changing the base ONCE in your base Dockerfile: fixes all {IMAGES_SHARING_BASE}")
print("   images at once, and every FUTURE image built on it.")
print("\nThe insight: most image vulns come from the BASE, and many images SHARE a base.")
print("So the highest-leverage fix isn't patching CVEs image-by-image — it's changing")
print("the BASE IMAGE (slim/alpine/newer). One change, dozens of vulns gone, across")
print("every image that inherits it. Same 'fix at the source, it multiplies' lesson as")
print("Wiz's IaC fix (CXLVII) — here the source is the base image.")
EOF
```

**Expected result:** Most image vulnerabilities traced to the base image, resolved by switching to a slimmer base that removes dozens at once across every image sharing it, rather than patching CVEs image-by-image. The base-image-multiplier lesson is that the highest-leverage container fix is changing the shared base — one change fixes all inheriting images and every future one, the same fix-at-the-source principle in container form.

**Negative test:** Remediating container vulnerabilities CVE-by-CVE in each image. Most come from the shared base, so patching individually is endless — changing the base image once removes dozens across every image that inherits it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Container image scanning understood as covering the whole image — your app plus the OS layers of the base image.
- [ ] The base-image recommendation understood as the multiplier fix — change the shared base, fix every inheriting image.
- [ ] Kubernetes workload configuration recognized as the runtime half of container security, alongside the image.
- [ ] The container understood as its own attack surface, distinct from code and dependency vulnerabilities.
