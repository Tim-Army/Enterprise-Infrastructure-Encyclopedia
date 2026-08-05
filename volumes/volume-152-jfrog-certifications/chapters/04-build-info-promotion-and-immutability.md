# Chapter 04: Build Info, Promotion, and Immutability

## Learning Objectives

- Explain build info and artifact traceability.
- Understand promotion — moving an artifact through environments without rebuilding.
- Describe immutability and why "build once, promote many" matters.
- Recognize the reproducibility and audit value of the model.

*Cert relevance: promotion and build info are core **DevOps Engineer** concepts — how artifacts flow to production reliably.*

## Build info: traceability

Every time your CI builds an artifact, Artifactory can capture **build info** — a rich record of *how* that artifact was produced: which source commit, which dependencies (exact versions) went into it, which build tool and environment, who triggered it, and when. This metadata is attached to the artifact permanently.

Build info makes artifacts **traceable**: given a binary running in production, you can answer "what commit is this? what dependencies does it contain? when and how was it built?" — essential for debugging, compliance, and (critically) [security response, Chapter 5](05-xray-security-and-license-compliance.md): when a CVE is announced in a dependency, build info lets you find *every* artifact that contains it. Without build info, a binary is an opaque blob; with it, it is a fully-documented, auditable object. The lab models traceability.

## Promotion: build once, promote many

The central release concept is **promotion**. An artifact is **built once** and then **promoted** through environments — from a `dev` repository to `staging` to `production` — *without rebuilding*. The **exact same binary** that passed testing in staging is what goes to production; promotion just moves it (or copies it) between repositories and updates its status.

This is the opposite of the anti-pattern where each environment *rebuilds* from source. Rebuilding is dangerous because a rebuild can produce a *different* binary (a dependency updated, a build tool changed, a non-reproducible build) — so the thing you tested is *not* the thing you shipped. **Build once, promote many** guarantees that the artifact tested in staging is *byte-for-byte* the artifact in production. The lab models the difference.

## Immutability

Underpinning promotion is **immutability**: a published artifact **does not change**. Version `2.1.0` of your package is always the same bytes — you cannot overwrite it with different content. This is essential because the whole delivery model assumes that the artifact you scanned, tested, and promoted is the *same* artifact throughout. If artifacts could be silently overwritten, none of the guarantees hold — you might scan one binary and deploy another under the same version.

Immutability makes the supply chain **trustworthy and reproducible**: a version identifies exact bytes, forever. Combined with build info (traceability) and promotion (build-once), it gives you a supply chain where every deployed artifact is documented, unchanged since it was built, and identical to what was tested. The lab is covered within the promotion exercise.

## Hands-On Lab

Python models promotion and immutability. **Cost:** none.

### Lab 4.1 — Build once and promote, versus rebuild per environment

**Objective:** See why promotion guarantees you ship what you tested.

```bash
python3 - <<'EOF'
import random
random.seed(7)
# building from source is not perfectly reproducible: a transitive dep may float
def build_from_source():
    # a floating dependency version sneaks in sometimes
    dep = random.choice(["lib-1.4.2", "lib-1.4.2", "lib-1.4.3"])  # occasionally different!
    return f"artifact(dep={dep})"

print("ANTI-PATTERN: rebuild from source in each environment")
dev     = build_from_source()
staging = build_from_source()
prod    = build_from_source()
print(f"   dev build:     {dev}")
print(f"   staging build: {staging}")
print(f"   prod build:    {prod}")
same = dev == staging == prod
print(f"   all identical? {same}")
if not same:
    print("   -> !! the PROD binary differs from what you TESTED in staging (a dep floated).")
    print("      You tested one thing and shipped ANOTHER. Heisenbug territory.\n")
else:
    print("   -> happened to match this time — but you're relying on LUCK.\n")

print("CORRECT: build ONCE, PROMOTE the same binary")
artifact = build_from_source()
print(f"   CI builds ONCE: {artifact}  (immutable — these exact bytes)")
print(f"   promote dev -> staging: SAME binary {artifact}")
print(f"   test in staging: PASS on {artifact}")
print(f"   promote staging -> prod: SAME binary {artifact}")
print(f"   -> prod runs the EXACT bytes you tested. Guaranteed identical.\n")
print("The principle: BUILD ONCE, PROMOTE MANY. Rebuilding per environment can produce")
print("a DIFFERENT binary (a floated dependency, a changed build tool), so 'tested in")
print("staging' no longer means 'this is in prod.' Promotion moves the SAME immutable")
print("artifact dev->staging->prod, so what you tested is BYTE-FOR-BYTE what you ship.")
print("Immutability (a version = fixed bytes forever) is what makes this trustworthy —")
print("and build info makes it traceable. That's a reliable supply chain.")
EOF
```

**Expected result:** Rebuilding per environment occasionally producing a different binary in production than was tested in staging (a floated dependency), versus building once and promoting the same immutable artifact through environments. The promotion lesson is build-once-promote-many — the exact bytes tested in staging are what ship to production, which rebuilding cannot guarantee, and immutability is what makes it trustworthy.

**Negative test:** Rebuilding the artifact from source in each environment. A rebuild can pull a different dependency or use a changed tool, so the production binary differs from the tested one — promotion moves the same immutable artifact instead.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Build info understood as the traceability record (commit, dependencies, environment) attached to each artifact.
- [ ] Promotion understood as moving one artifact through environments without rebuilding — build once, promote many.
- [ ] Immutability understood as a version meaning fixed bytes forever — the basis of a trustworthy supply chain.
- [ ] The reproducibility and audit value recognized — you ship byte-for-byte what you tested, fully documented.
