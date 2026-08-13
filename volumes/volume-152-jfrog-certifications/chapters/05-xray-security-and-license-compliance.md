# Chapter 05: Xray — Security and License Compliance

## Learning Objectives

- Explain deep recursive scanning of artifacts and their dependencies.
- Understand impact analysis — which builds are affected by a vulnerability.
- Place license compliance alongside vulnerability scanning.
- Recognize scanning the binary hub as a supply-chain control point.

*Cert relevance: Xray is the subject of the **Associate Security** certification and a core **DevOps Engineer** topic.*

## Deep recursive scanning

**Xray** is JFrog's security and compliance scanner, and its signature is **deep recursive scanning.** A container image or package is not one thing — it is layers of *other* packages, which contain *other* dependencies, several levels deep. A vulnerability might live not in the artifact you built but in a **transitive dependency buried inside a base image layer**. Xray **recursively decomposes** each artifact — unpacking images, reading manifests, walking the full dependency tree — and scans *every* component against vulnerability databases.

This is the same [transitive-dependency problem the Snyk volume (CXLVIII)](../../volume-148-snyk-certifications/chapters/03-snyk-open-source-sca.md) teaches, from the **binary-hub** side: because *every* binary flows through Artifactory ([Chapter 2](02-artifactory-the-universal-binary-repository.md)), Xray can scan *everything* the organization uses — first-party and third-party, in every package type — at the one point they all pass through. The lab models recursive scanning.

## Impact analysis

The signature *operational* capability is **impact analysis**: when a new CVE is announced in some widely-used component (say, a Log4j-style event), Xray can instantly answer "**which of our artifacts, builds, and deployments contain the vulnerable component?**" — tracing the dependency (via [build info, Chapter 4](04-build-info-promotion-and-immutability.md)) through every artifact that includes it, transitively.

This turns the panic of a major vulnerability disclosure into a **query**. Without it, "are we affected by CVE-X?" is a frantic manual audit across every team and repo that takes days; with Xray's impact analysis and the centralized binary hub, it is an instant, authoritative answer: *these* 14 artifacts and *these* 3 running services contain it, fix these. The lab models impact analysis.

## License compliance

Beyond security, Xray enforces **license compliance.** Open-source packages carry licenses (MIT, Apache, GPL, AGPL…), and some licenses impose obligations incompatible with commercial software — a copyleft license like AGPL pulled in transitively can create legal exposure. Xray detects the **license of every component** (recursively, like vulnerabilities) and flags policy violations — "this artifact contains an AGPL dependency, which your policy forbids."

Because it works on the same recursive scan of the same centralized binaries, license compliance is *automatic* and *complete* — you learn about a forbidden license when the artifact enters the repository, not when a lawyer finds it later. The lab is covered within the scanning exercise.

## Hands-On Lab

Python models Xray scanning. **Cost:** none.

### Lab 5.1 — Deep recursive scan finds the buried vulnerability

**Objective:** See why scanning must recurse into transitive components.

```bash
python3 - <<'EOF'
# an artifact is layers of packages containing dependencies, several levels deep
ARTIFACT = {
  "my-service:2.1 (Docker image)": {
    "base: node:20": {
      "openssl (OS lib)": {},
      "libxml2 2.9.10": {"VULN": "CVE-2024-XXXX (CVSS 9.1) in libxml2"},  # buried deep
    },
    "app dependencies": {
      "express 4.18": {},
      "lodash 4.17.21": {},
    },
  }
}
def scan(tree, depth=0, path=""):
    findings = []
    for name, sub in tree.items():
        p = f"{path} > {name}" if path else name
        if isinstance(sub, dict) and "VULN" in sub:
            findings.append((sub["VULN"], p))
        elif isinstance(sub, dict):
            findings += scan(sub, depth+1, p)
    return findings

print("Artifact: my-service:2.1 (a Docker image = layers of packages of dependencies)\n")
print("SHALLOW scan (top-level only — 'what did MY build declare?'):")
print("   sees: express 4.18, lodash 4.17.21 -> both clean. 'All good!'")
print("   MISSES the vulnerability buried in the base image's libxml2.\n")
print("DEEP RECURSIVE scan (Xray — decompose every layer + dependency):")
for vuln, path in scan(ARTIFACT):
    print(f"   !! {vuln}")
    print(f"      location: {path}")
print("\n   the CVE is in libxml2 2.9.10 — pulled in by the node:20 BASE IMAGE, several")
print("   levels deep. You never declared it; it came with the base. A shallow scan")
print("   of your declared dependencies would NEVER find it.")
print("\nXray RECURSIVELY decomposes each artifact — unpacks image layers, walks the")
print("full dependency tree — and scans EVERY component. And because every binary")
print("flows through Artifactory, Xray scans EVERYTHING the org uses, first- and third-")
print("party, at one control point. The risk is almost always in what you DIDN'T")
print("declare — the transitive, buried components — so the scan has to go all the way down.")
EOF
```

**Expected result:** A shallow scan of declared dependencies missing a critical CVE buried in a base image's transitive component, which Xray's deep recursive scan finds by decomposing every layer and dependency. The recursive-scanning lesson is that risk is usually in the undeclared, transitive, buried components, so scanning must walk the full tree — which the centralized binary hub lets Xray do for everything the organization uses.

**Negative test:** Scanning only an artifact's top-level declared dependencies. The critical vulnerability is in a transitive component inside a base image layer, invisible to a shallow scan — deep recursive scanning is required to find it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Impact analysis turns a CVE panic into a query

**Objective:** Instantly find every artifact affected by a new vulnerability.

```bash
python3 - <<'EOF'
# the binary hub knows which artifacts contain which components (via build info)
ARTIFACTS = {
  "payments-api:3.2":   ["log4j-core:2.14", "spring:5.3", "jackson:2.13"],
  "auth-service:1.8":   ["log4j-core:2.14", "spring:5.3"],
  "web-frontend:4.0":   ["react:18", "webpack:5"],
  "batch-worker:2.1":   ["log4j-core:2.17", "spring:5.3"],   # already patched
  "reporting:1.1":      ["log4j-core:2.14", "poi:5.2"],
}
DEPLOYED = {"payments-api:3.2", "auth-service:1.8", "web-frontend:4.0"}  # running in prod

VULN_COMPONENT = "log4j-core:2.14"   # a new critical CVE just announced
print(f"BREAKING: critical CVE announced in {VULN_COMPONENT}\n")
print("WITHOUT impact analysis:")
print("   'Are we affected?' -> frantic manual audit: every team greps every repo,")
print("   checks every build, for DAYS. Some get missed. Nobody's sure it's complete.\n")
print("WITH Xray impact analysis (the hub knows what contains what):")
affected = [a for a, comps in ARTIFACTS.items() if VULN_COMPONENT in comps]
affected_deployed = [a for a in affected if a in DEPLOYED]
print(f"   affected artifacts: {affected}")
print(f"   -> {len(affected)} artifacts contain {VULN_COMPONENT}")
print(f"   RUNNING IN PRODUCTION (fix FIRST): {affected_deployed}")
print(f"   NOT affected: batch-worker (has log4j 2.17, already patched), web-frontend")
print("\n   instant, authoritative answer: fix these 3 artifacts, and payments-api +")
print("   auth-service are LIVE so they're the priority.")
print("\nImpact analysis turns 'are we affected by CVE-X?' from a days-long panic into a")
print("QUERY. Because every binary flows through the hub and build info records what")
print("contains what, Xray traces the vulnerable component through EVERY artifact")
print("(transitively) in seconds — and cross-references what's DEPLOYED so you fix the")
print("live, exposed ones first. This is the payoff of the centralized binary hub for")
print("supply-chain security: you always know what you're running.")
EOF
```

**Expected result:** A newly-announced CVE traced instantly to the exact affected artifacts (and which are deployed in production) via impact analysis, versus a days-long manual audit. The impact-analysis lesson is that the centralized binary hub plus build info turns "are we affected?" into an authoritative query — finding every artifact containing the vulnerable component and prioritizing the deployed ones.

**Negative test:** Answering "are we affected by this CVE?" by manual audit across teams and repos. It takes days and misses artifacts; impact analysis on the centralized hub answers instantly and completely, cross-referenced with what is deployed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Deep recursive scanning understood as decomposing artifacts into every transitive component and scanning all of them.
- [ ] Impact analysis understood as instantly finding every artifact affected by a new vulnerability via build info.
- [ ] License compliance placed alongside vulnerability scanning, working on the same recursive scan.
- [ ] Scanning the centralized binary hub recognized as the supply-chain control point covering everything the org uses.
