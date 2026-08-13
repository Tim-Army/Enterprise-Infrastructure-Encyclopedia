# Chapter 03: Repository Types and the Binary Flow

## Learning Objectives

- Distinguish local, remote, and virtual repositories.
- Understand remote repositories as caching proxies and the resilience they add.
- Understand virtual repositories as aggregation behind one URL.
- Recognize the standard repository topology.

*Cert relevance: repository types are foundational **Associate Artifactory** and **DevOps Engineer** material — the model everything else builds on.*

## The three repository types

Artifactory organizes binaries into three kinds of repository, and understanding the distinction is essential:

| Type | Holds | Is |
|:---|:---|:---|
| **Local** | *Your* artifacts | Where your build outputs are stored |
| **Remote** | *Cached copies* of an upstream | A caching proxy of a public registry (npmjs, Docker Hub, Maven Central) |
| **Virtual** | *Nothing itself* | An aggregation of several local + remote repos behind one URL |

A **local** repository is your own storage — your build produces a JAR, it goes in a local repo. A **remote** repository is a **caching proxy** of an external registry — when a developer requests a package from "npm-remote," Artifactory fetches it from npmjs *once*, caches it, and serves the cached copy thereafter. A **virtual** repository **aggregates** several repos (some local, some remote) behind a **single URL**, so developers point at one endpoint and get artifacts from everywhere.

## Remote repositories and resilience

The **remote (caching proxy)** repository solves a serious problem: **dependency on external registries.** If your builds pull directly from Docker Hub and Docker Hub is down (or rate-limits you, or a package is deleted), your builds break — a external outage becomes *your* outage. A remote repository **caches** every fetched package, so after the first fetch the package is served *locally* and fast, and your builds keep working even if the upstream is unavailable.

This is both **resilience** (immune to upstream outages for cached packages) and **speed** (local cache is faster than the internet) and **control** (every external package now passes through a point you can [scan and govern, Chapter 5–6](05-xray-security-and-license-compliance.md)). The lab models the resilience.

## Virtual repositories and aggregation

The **virtual** repository solves **complexity for developers.** Without it, a developer's tool must be configured with multiple repository URLs (the local repo for internal packages, the remote for public ones, maybe several of each). A **virtual** repository presents **one URL** that transparently resolves from all the underlying repos — the developer configures *one* endpoint, and Artifactory figures out whether a requested package is internal (local) or external (remote-cached).

This simplifies developer configuration enormously and lets ops **change the underlying topology** (add a repo, reorder resolution) without touching every developer's config. The lab models aggregation.

## Hands-On Lab

Python models repository topology. **Cost:** none.

### Lab 3.1 — Remote caching survives an upstream outage

**Objective:** See why a caching proxy keeps builds working.

```bash
python3 - <<'EOF'
# builds requesting packages; upstream (Docker Hub) goes DOWN partway through
UPSTREAM_PACKAGES = {"nginx:1.25", "node:20", "python:3.12", "redis:7"}
cache = set()
upstream_up = True

def fetch(pkg, use_remote_repo):
    global upstream_up
    if use_remote_repo:
        if pkg in cache:
            return "served from CACHE (fast, works even if upstream down)"
        elif upstream_up:
            cache.add(pkg)
            return "fetched from upstream -> cached"
        else:
            return "MISS + upstream DOWN -> but only NEW packages fail"
    else:  # pulling directly from upstream, no caching
        return "OK (direct)" if upstream_up else "BUILD FAILS (upstream down, no cache)"

print("Builds pull: nginx:1.25, node:20 (early), then upstream goes DOWN, then more builds\n")
print("WITHOUT a remote repo (pull direct from Docker Hub):")
upstream_up = True
print(f"   build 1 nginx:1.25 -> {fetch('nginx:1.25', False)}")
upstream_up = False
print("   ...Docker Hub goes DOWN (outage / rate limit)...")
print(f"   build 2 node:20    -> {fetch('node:20', False)}")
print(f"   build 3 nginx:1.25 -> {fetch('nginx:1.25', False)}  (even a REPEAT fails!)")
print("   -> ALL builds fail during the outage. Their outage = your outage.\n")

cache.clear()
print("WITH a remote (caching proxy) repo:")
upstream_up = True
print(f"   build 1 nginx:1.25 -> {fetch('nginx:1.25', True)}")
print(f"   build 2 node:20    -> {fetch('node:20', True)}")
upstream_up = False
print("   ...Docker Hub goes DOWN...")
print(f"   build 3 nginx:1.25 -> {fetch('nginx:1.25', True)}")
print(f"   build 4 node:20    -> {fetch('node:20', True)}")
print("   -> builds using ALREADY-CACHED packages KEEP WORKING through the outage.\n")
print("The remote repo CACHES every package it fetches, so after the first pull it's")
print("served locally — immune to upstream outages, faster than the internet, and every")
print("external package now passes through a point you CONTROL (and can scan, Ch 5).")
print("Pulling direct from public registries makes their reliability YOUR reliability.")
EOF
```

**Expected result:** Direct-from-upstream builds all failing during a Docker Hub outage while remote-repo builds using cached packages keep working. The remote-caching lesson is that a caching proxy makes cached packages immune to upstream outages (and faster, and governable), where pulling directly from public registries makes their reliability your reliability.

**Negative test:** Pulling dependencies directly from public registries in CI. An upstream outage, rate limit, or removed package breaks your builds — a remote caching repository serves cached copies through the disruption.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Virtual repositories simplify developer config

**Objective:** See how one aggregating URL hides topology from developers.

```bash
python3 - <<'EOF'
# underlying repos
LOCAL = {"my-app:2.1", "my-lib:1.4", "internal-tool:3.0"}      # our artifacts
REMOTE_CACHE = {"nginx:1.25", "node:20", "lodash:4.17.21"}      # cached public
# a virtual repo aggregates both behind ONE url, resolving in order: local first, then remote
def virtual_resolve(pkg):
    if pkg in LOCAL:  return "local (internal artifact)"
    if pkg in REMOTE_CACHE: return "remote-cache (public, cached)"
    return "remote fetch (public, not yet cached)"

print("WITHOUT a virtual repo — the developer configures MANY URLs:")
print("   registry-1 = https://artifactory/local-releases")
print("   registry-2 = https://artifactory/local-snapshots")
print("   registry-3 = https://artifactory/npm-remote")
print("   registry-4 = https://artifactory/docker-remote ...")
print("   -> every dev + CI job hard-codes 4+ URLs; change topology = update them ALL\n")

print("WITH a virtual repo — ONE url resolves everything:")
print("   registry = https://artifactory/my-team-virtual   (that's it)")
for pkg in ["my-app:2.1", "node:20", "brand-new-pkg:1.0"]:
    print(f"   request {pkg:18} -> resolves from {virtual_resolve(pkg)}")
print("\n   the developer points at ONE URL. Artifactory transparently figures out")
print("   whether each package is internal (local) or external (remote-cached), in a")
print("   configured resolution order.")
print("\nThe win: developers configure ONE endpoint, not a list. And ops can change the")
print("underlying topology (add a repo, reorder resolution, swap an upstream) by editing")
print("the VIRTUAL repo — WITHOUT touching a single developer's config. Aggregation")
print("behind one URL is what makes a complex repo topology simple to consume.")
EOF
```

**Expected result:** Developers configuring one virtual-repository URL that transparently resolves internal and external packages, versus hard-coding many repository URLs. The virtual-repository lesson is that aggregation behind one URL simplifies developer configuration and lets ops change the underlying topology without touching every developer's config.

**Negative test:** Making developers configure every underlying repository URL directly. Each change to the topology requires updating every developer and CI config; a virtual repository presents one stable URL and hides the topology.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Local, remote, and virtual repositories distinguished by what they hold.
- [ ] Remote repositories understood as caching proxies providing resilience, speed, and a control point.
- [ ] Virtual repositories understood as aggregation behind one URL, simplifying developer config.
- [ ] The standard topology (local for yours, remote for cached upstreams, virtual to aggregate) internalized.
