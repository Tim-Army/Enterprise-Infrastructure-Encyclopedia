# Chapter 08: The DevOps Pipeline and Distribution

## Learning Objectives

- Place Artifactory as the hub of the CI/CD pipeline.
- Understand how the platform's capabilities compose into a delivery flow.
- Explain Distribution — delivering releases to edges at scale.
- Recognize the end-to-end binary journey the DevOps Engineer certifies.

*Cert relevance: the end-to-end pipeline is what the **DevOps Engineer** certification validates — how everything fits together.*

## Artifactory as the pipeline hub

The previous chapters each covered one capability; the **DevOps Engineer** certification is about how they **compose into one delivery flow**, with Artifactory as the hub. A modern pipeline runs:

```text
CI builds → store in Artifactory (+ build info) → Xray scans → Curation-gated deps → promote dev→staging→prod → Distribution to edges → deploy
```

The [source-code tools (Chapter 1)](01-the-jfrog-certification-program.md) hand off to JFrog the moment code becomes a binary, and JFrog carries it the rest of the way — storing, scanning, promoting, and distributing. Artifactory is the **hub every stage passes through**, which is exactly why it can enforce security ([Xray](05-xray-security-and-license-compliance.md), [Curation](06-software-supply-chain-security.md)), guarantee reproducibility ([promotion/immutability](04-build-info-promotion-and-immutability.md)), and provide traceability (build info) — *because all binaries flow through it*. The lab models the composed flow.

## Distribution: releases to the edge

**JFrog Distribution** solves **getting releases out at scale.** A finished release may need to reach hundreds or thousands of destinations — edge locations, remote data centers, retail stores, IoT/embedded devices, air-gapped environments. Serving all of them directly from the central Artifactory would overwhelm it and be slow for distant consumers.

Distribution packages a release into a signed, immutable **release bundle** and pushes it out to **distribution edges** (JFrog edge nodes) near the consumers, so downloads are fast and local and the central hub is not overwhelmed. This is the "**liquid software**" vision — releases flowing continuously and reliably all the way to where they run, however far and however many. The lab is covered within the pipeline exercise.

## The end-to-end journey

The whole volume assembles into one journey, and internalizing it is the **DevOps Engineer** mindset: a binary is *built once*, *stored* in Artifactory with *build info*, *scanned* by Xray (its dependencies *gated* by Curation), *promoted* immutably through environments, and *distributed* to the edge — traceable, secure, reproducible, and available the entire way. Every JFrog capability is one stage of this journey, and the hub is what makes the whole thing coherent. The lab traces it.

## Hands-On Lab

Python models the composed pipeline. **Cost:** none.

### Lab 8.1 — The binary's end-to-end journey through the hub

**Objective:** Trace an artifact through every stage, showing the hub enforces each.

```bash
python3 - <<'EOF'
# an artifact flows through the pipeline; the hub enforces a gate at each stage
artifact = {"name": "payments-api:3.2", "status": "built", "scanned": False,
            "promoted_to": "dev", "distributed": False}

def stage(name, action, gate_ok, gate_desc):
    print(f"[{name}] {action}")
    if not gate_ok:
        print(f"    GATE FAILED: {gate_desc} -> pipeline STOPS. Fix and retry.")
        return False
    print(f"    gate passed: {gate_desc}")
    return True

print(f"Artifact {artifact['name']} — end-to-end through the JFrog hub:\n")
steps = [
  ("BUILD",       "CI compiles + packages -> stored in Artifactory with BUILD INFO", True, "traceability recorded (commit, deps, env)"),
  ("DEPENDENCIES","pull deps via remote repos", True, "Curation blocked 0 malicious/forbidden this build"),
  ("SCAN",        "Xray deep-recursive scan", True, "no critical CVEs, no forbidden licenses"),
  ("PROMOTE dev->staging", "move the SAME immutable binary", True, "identical bytes; not rebuilt"),
  ("TEST",        "run tests in staging", True, "passed on the exact binary that will ship"),
  ("PROMOTE staging->prod","move the SAME immutable binary", True, "byte-for-byte what was tested"),
  ("DISTRIBUTE",  "package a signed release bundle -> push to edges", True, "fast local delivery to 200 edges"),
  ("DEPLOY",      "run the binaries", True, "traceable, scanned, reproducible, available"),
]
for name, action, ok, desc in steps:
    if not stage(name, action, ok, desc):
        break
print("\nThe DevOps Engineer mindset: a binary is BUILT ONCE, then flows through ONE HUB")
print("that enforces a gate at every stage — build info (traceable), Curation +")
print("Xray (secure), promotion + immutability (reproducible: ship what you tested),")
print("Distribution (available at the edge). Every JFrog capability is ONE STAGE of")
print("this journey, and Artifactory is the hub that makes it coherent — because EVERY")
print("binary flows through it, it can enforce security, reproducibility, and")
print("traceability end-to-end. That end-to-end flow is what the certification validates.")
EOF
```

**Expected result:** An artifact traced through build (with build info), dependency curation, Xray scan, immutable promotion dev-to-staging-to-prod, and distribution to edges — the hub enforcing a gate at each stage. The end-to-end lesson is the DevOps Engineer mindset: a binary built once flows through one hub that makes it traceable, secure, reproducible, and available, with every JFrog capability one stage of the journey.

**Negative test:** Treating each JFrog capability as an isolated feature. Their value is the composed, gated end-to-end flow through the hub — build info, Curation, Xray, promotion, and Distribution together deliver a binary that is traceable, secure, and reproducible, which no single feature provides alone.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Artifactory placed as the hub of the CI/CD pipeline that every stage passes through.
- [ ] The platform's capabilities understood as composing into one gated delivery flow.
- [ ] Distribution understood as delivering signed release bundles to edges for fast, scalable delivery.
- [ ] The end-to-end binary journey (build once, store, scan, promote, distribute) internalized as the DevOps Engineer mindset.
