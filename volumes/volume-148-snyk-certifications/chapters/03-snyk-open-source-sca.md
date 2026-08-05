# Chapter 03: Snyk Open Source — SCA

## Learning Objectives

- Explain software composition analysis (SCA) and the open-source risk.
- Understand transitive dependencies — the vulnerabilities you did not choose.
- Fix by dependency upgrade, and understand when you cannot.
- Recognize the software supply chain as an attack surface.

*Cert relevance: Snyk Open Source is the SCA engine — the dependency side of the app, and often the largest attack surface.*

## The open-source risk

Modern applications are mostly **not your code**. A typical app is a thin layer of first-party code over a deep stack of **open-source dependencies** — frameworks, libraries, utilities — that often make up **80% or more** of the shipped application. You did not write them, you may not have read them, but you *ship* them, and their vulnerabilities are *your* vulnerabilities.

**Software Composition Analysis (SCA)** — Snyk's **Open Source** product — inventories every open-source component in your app and matches it against a vulnerability database, telling you which of your dependencies have known CVEs. This is a different problem from scanning your own code (that is SAST, [Chapter 4](04-snyk-code-sast.md)): here the flaw is in someone else's code that you depend on.

## Transitive dependencies

The hard part is **transitivity**. You directly depend on library A; but A depends on B, and B depends on C, and the vulnerability is in **C** — a package you never chose, never named, and may not know you have. These **transitive dependencies** dominate the dependency tree: your `package.json` might list 20 direct dependencies that resolve to 1,500 total packages, and most vulnerabilities live in the transitive depths.

SCA must therefore analyze the **full dependency tree**, not just the top-level manifest. Snyk builds the tree, finds the vulnerable package wherever it hides, and — crucially — tells you **which direct dependency to change** to pull in a fixed version of the deep one. The lab models finding and fixing a transitive vulnerability.

## Fixing by upgrade

The good news about dependency vulnerabilities is that they usually have a **known fix**: the maintainer released a patched version. Remediation is often "**upgrade** dependency X to version Y." Snyk computes the **minimal upgrade** that resolves the vulnerability while respecting your version constraints, and can open the pull request for you.

The complication is the **transitive fix**: if the vulnerable package C is pulled in by your direct dependency A, you may need to upgrade **A** (which upgrades its dependency on C), not C directly — and sometimes no compatible upgrade exists yet, in which case you weigh a version override, a different library, or accepting and monitoring the risk. The lab models the upgrade calculation.

## Hands-On Lab

Python models dependency analysis. **Cost:** none.

### Lab 3.1 — Find the transitive vulnerability

**Objective:** Discover a vulnerability in a dependency you never chose.

```bash
python3 - <<'EOF'
# your dependency tree: direct deps -> their deps -> ...
TREE = {
  "my-app":       ["web-framework", "logger", "date-utils"],   # direct deps (you chose these)
  "web-framework":["http-parser", "template-engine"],
  "logger":       ["serializer"],
  "date-utils":   [],
  "http-parser":  ["stream-lib"],
  "template-engine":[],
  "serializer":   ["yaml-parser"],     # deep transitive
  "stream-lib":   [],
  "yaml-parser":  [],                  # <-- the vulnerable one, 4 levels deep
}
VULNERABLE = {"yaml-parser": "CVE-2025-XXXX: RCE via unsafe deserialization (CVSS 9.8)"}
DIRECT = set(TREE["my-app"])

def walk(node, path, depth=0):
    for child in TREE.get(node, []):
        p = path + [child]
        if child in VULNERABLE:
            yield (child, p, depth+1)
        yield from walk(child, p, depth+1)

print("Direct dependencies you CHOSE:", DIRECT)
print(f"(these {len(DIRECT)} direct deps resolve to {len(TREE)-1} total packages)\n")
print("SCA walks the FULL tree and finds:")
for vuln_pkg, path, depth in walk("my-app", ["my-app"]):
    print(f"   !! {VULNERABLE[vuln_pkg]}")
    print(f"      in '{vuln_pkg}' — a TRANSITIVE dependency, {depth} levels deep")
    print(f"      path: {' -> '.join(path)}")
    print(f"      you never named '{vuln_pkg}'; it came in via '{path[1]}'")
print("\nThe insight: the vulnerability is in 'yaml-parser', which you NEVER chose. It")
print("arrived: my-app -> logger -> serializer -> yaml-parser. Scanning only your")
print("direct deps (or only your code) would MISS it entirely.")
print("\nMost of an app's packages — and most of its dependency vulns — are TRANSITIVE:")
print("deps of deps you never named. SCA has to build the WHOLE tree to find them,")
print("then tell you which DIRECT dependency (logger) to change to fix the deep one.")
print("That's the open-source attack surface: 80%+ of the app is code you didn't")
print("write, and the risk hides in packages you didn't know you had.")
EOF
```

**Expected result:** A critical vulnerability found four levels deep in a transitive dependency the developer never chose, reached through a chain from a direct dependency. The transitive lesson is that most of an app's packages and vulnerabilities are dependencies-of-dependencies, so SCA must analyze the full tree — scanning only direct dependencies or first-party code misses the deep packages where risk hides.

**Negative test:** Auditing only the direct dependencies in your manifest. The vulnerable `yaml-parser` is four levels deep and never named directly — only walking the full transitive tree surfaces it.

**Cleanup:** None.

### Lab 3.2 — Fix by minimal upgrade (including the transitive case)

**Objective:** Compute the upgrade that resolves the vulnerability.

```bash
python3 - <<'EOF'
# the vulnerable transitive package and the upgrade options
# vulnerable: yaml-parser 1.1 (pulled in by logger 2.0 which pins yaml-parser <2.0)
# fixed:      yaml-parser 2.1
# logger 3.0 depends on yaml-parser >=2.1  -> upgrading logger fixes it transitively
print("VULNERABLE: yaml-parser 1.1 (RCE). Fixed in yaml-parser 2.1.")
print("But yaml-parser is TRANSITIVE — pulled in by your direct dep 'logger'.\n")
options = [
  ("force yaml-parser -> 2.1 directly", "override", "works, but a manual override you must maintain; can break logger"),
  ("upgrade logger 2.0 -> 3.0",         "clean",    "logger 3.0 depends on yaml-parser>=2.1 -> pulls the FIX transitively"),
  ("do nothing",                        "risk",     "RCE stays shipped"),
]
print("Remediation options:")
for opt, kind, note in options:
    tag = {"clean":"[BEST]","override":"[ok]","risk":"[NO]"}[kind]
    print(f"   {tag:8} {opt:36} {note}")
print("\nThe KEY move (transitive fix): you don't patch yaml-parser directly — you")
print("upgrade the DIRECT dependency that pulls it in. logger 2.0 -> 3.0, and logger")
print("3.0's own dependency on yaml-parser>=2.1 brings the fixed version with it.")
print("ONE change to something you actually control (a direct dep) fixes a package 3")
print("levels down. That's what Snyk computes: the MINIMAL upgrade to a dependency you")
print("own that resolves the deep vuln — and it opens the PR for you.")
print("\nWhen NO compatible upgrade exists yet (logger hasn't bumped yaml-parser), you")
print("weigh an override, a different library, or accept-and-monitor. But the default")
print("and best path is: upgrade the direct dep, let the fix flow down the tree.")
EOF
```

**Expected result:** A transitive vulnerability resolved by upgrading the direct dependency that pulls it in, rather than patching the deep package directly, with the direct upgrade carrying the fixed version down the tree. The fix-by-upgrade lesson is that Snyk computes the minimal upgrade to a dependency you control that resolves the deep vulnerability — and when no compatible upgrade exists, the fallback is an override, a swap, or accept-and-monitor.

**Negative test:** Trying to patch the vulnerable transitive package directly. It works as a manual override you must maintain and can break the parent that pinned the old version — upgrading the direct dependency that pulls it in is the clean fix.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] SCA understood as inventorying open-source dependencies against a vulnerability database — the majority of the app.
- [ ] Transitive dependencies understood as the vulnerabilities you never chose, requiring full-tree analysis.
- [ ] Fixing by minimal upgrade understood, including upgrading the direct dependency to fix a transitive one.
- [ ] The open-source supply chain recognized as the largest attack surface in most applications.
