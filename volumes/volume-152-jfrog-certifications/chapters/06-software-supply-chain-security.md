# Chapter 06: Software Supply Chain Security

## Learning Objectives

- Explain the software supply chain and its attack surface.
- Understand Curation — blocking malicious packages at the gate.
- Place SBOMs and provenance in supply-chain security.
- Recognize JFrog Advanced Security's role beyond dependency CVEs.

*Cert relevance: supply-chain security is central to the **Associate Security** and **DevOps Engineer** certifications — the modern security frontier.*

## The software supply chain attack surface

A **software supply chain attack** targets not your code but the **components you build with** — a compromised open-source package, a poisoned base image, a malicious dependency uploaded to a public registry. The SolarWinds and various npm/PyPI incidents proved that attackers get far more leverage by compromising *one widely-used component* than by attacking targets individually: every organization that pulls the poisoned package is compromised at once.

This makes the **binaries entering your organization** a critical attack surface — and because [every binary flows through Artifactory (Chapter 2)](02-artifactory-the-universal-binary-repository.md), the binary hub is exactly the right place to *defend* that surface. [Xray (Chapter 5)](05-xray-security-and-license-compliance.md) scans for *known* vulnerabilities; supply-chain security adds defenses against *malicious* and *untrustworthy* components.

## Curation: block at the gate

**JFrog Curation** is a **gate** on packages *entering* the organization: before a developer can pull a public package through a [remote repository (Chapter 3)](03-repository-types-and-the-binary-flow.md), Curation evaluates it against policy — is it known-malicious? does it have a critical unpatched CVE? an unacceptable license? is it suspiciously new or unmaintained? — and **blocks the bad ones before they ever enter.**

This is **prevention at the front door**, the complement to Xray's detection. Rather than pulling in a malicious package and *then* finding it, Curation stops it from entering at all — the [narrow-the-entry-point discipline](../../volume-148-snyk-certifications/chapters/06-snyk-infrastructure-as-code.md) applied to the dependency supply. The lab models the gate.

## SBOMs and provenance

Two supply-chain-transparency concepts the certifications cover:

- **SBOM (Software Bill of Materials)** — a complete, machine-readable list of *every* component in an artifact (like an ingredients label). Increasingly *required* (regulation, customer demand), an SBOM lets anyone — you, an auditor, a customer — know exactly what is inside a piece of software. Because the binary hub knows every component ([build info, Chapter 4](04-build-info-promotion-and-immutability.md)), it can *generate* accurate SBOMs automatically.
- **Provenance** — verifiable evidence of *where an artifact came from and how it was built* (which pipeline, which source, signed). Provenance lets a consumer *trust* an artifact is what it claims to be and was not tampered with — the answer to "is this really our build, or did someone slip something in?"

Together, SBOMs (what's inside) and provenance (where it's from) make the supply chain **transparent and verifiable**. The lab is covered within the Curation exercise.

## Hands-On Lab

Python models supply-chain defenses. **Cost:** none.

### Lab 6.1 — Curation blocks malicious packages at the gate

**Objective:** Stop bad components from entering, rather than finding them later.

```bash
python3 - <<'EOF'
# packages a developer tries to pull from public registries; Curation evaluates each
PACKAGES = [
  # name,                  known_malicious, critical_cve, license,   age_days, maintained
  ("express@4.18",         False, False, "MIT",   3000, True),   # fine
  ("left-pad-evil@1.0",    True,  False, "MIT",   2,    False),  # known-malicious, brand new
  ("coolutils@0.0.1",      False, False, "MIT",   1,    False),  # suspiciously new + unmaintained (typosquat?)
  ("legacy-lib@2.1",       False, True,  "MIT",   1500, True),   # critical unpatched CVE
  ("agpl-tool@3.0",        False, False, "AGPL",  900,  True),   # forbidden license
]
POLICY = {"block_malicious": True, "block_critical_cve": True,
          "forbidden_licenses": {"AGPL"}, "block_new_unmaintained": True}
def curate(name, mal, cve, lic, age, maint):
    if POLICY["block_malicious"] and mal: return "BLOCK — known malicious"
    if POLICY["block_critical_cve"] and cve: return "BLOCK — critical unpatched CVE"
    if lic in POLICY["forbidden_licenses"]: return f"BLOCK — forbidden license ({lic})"
    if POLICY["block_new_unmaintained"] and age < 30 and not maint:
        return "BLOCK — suspiciously new + unmaintained (possible typosquat/supply-chain)"
    return "ALLOW"
print("Curation gate — evaluating packages BEFORE they enter the org:\n")
print(f"   {'package':22}decision")
allowed = blocked = 0
for name, *attrs in PACKAGES:
    d = curate(name, *attrs)
    if d.startswith("BLOCK"): blocked += 1
    else: allowed += 1
    print(f"   {name:22}{d}")
print(f"\n   allowed: {allowed}, blocked at the gate: {blocked}")
print("\nCuration is PREVENTION AT THE FRONT DOOR: it evaluates each public package")
print("BEFORE a developer can pull it — blocking known-malicious code, critical")
print("unpatched CVEs, forbidden licenses, and suspiciously-new/unmaintained packages")
print("(a classic typosquat / supply-chain vector). The bad ones NEVER ENTER.")
print("\nThis complements Xray (which DETECTS known vulns in what you have): Curation")
print("STOPS bad components at the gate, so you're not pulling in malware and finding")
print("it later. Because every dependency flows through Artifactory's remote repos,")
print("the gate is at the one point everything passes through — the right place to")
print("defend the software supply chain.")
EOF
```

**Expected result:** Curation blocking known-malicious, critically-vulnerable, forbidden-license, and suspiciously-new-unmaintained packages at the gate while allowing clean ones. The Curation lesson is prevention at the front door — evaluating public packages before they enter and blocking the bad ones, complementing Xray's detection at the one point every dependency flows through.

**Negative test:** Relying only on scanning after packages are pulled in. A malicious or typosquatted package is already inside before detection; Curation blocks it at the gate so it never enters the organization.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The software supply chain attack surface understood — attackers compromise widely-used components for leverage.
- [ ] Curation understood as a gate blocking malicious, vulnerable, or non-compliant packages before they enter.
- [ ] SBOMs (what's inside) and provenance (where it's from) placed as supply-chain transparency and trust.
- [ ] JFrog Advanced Security recognized as extending defense beyond dependency CVEs to the supply chain itself.
