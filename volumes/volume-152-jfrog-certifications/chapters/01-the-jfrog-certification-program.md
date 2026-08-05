# Chapter 01: The JFrog Certification Program

![The JFrog certification program and the Software Supply Chain Platform beneath it. The program is delivered through JFrog Academy with free and paid courses, learning paths, and certifications. Three Associate-level certifications, each valid for two years, cover distinct domains: Associate JFrog Artifactory for artifact management and application deployment, Associate JFrog DevOps High Availability and Disaster Recovery for distributed systems and repository federation, and Associate JFrog Security for application security and protection practices. Above them, the JFrog Artifactory Certified DevOps Engineer is the flagship credential, a web-based proctored exam of forty-seven multiple-choice and multiple-answer questions in ninety minutes with a passing score of seventy percent, valid two years, validating binary repository management, security, and CI/CD pipelines. The platform beneath is the JFrog Software Supply Chain Platform, centered on Artifactory, the universal binary repository manager that stores every package type in local, remote, and virtual repositories, with Xray for deep recursive vulnerability and license scanning, JFrog Advanced Security and Curation for supply-chain protection, Distribution for release delivery to edges, Pipelines for CI/CD, and JFrog ML for models, unified as the single source of truth for binaries flowing from developer to production.](../../../diagrams/volume-152-jfrog-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Associate certifications and the DevOps Engineer credential over the Software Supply Chain Platform.*

## Learning Objectives

- Describe the JFrog certification program — the Associate certs and the DevOps Engineer credential.
- Distinguish the three Associate domains: Artifactory, HA/DR, and Security.
- Place the JFrog Software Supply Chain Platform and the universal binary repository.
- Recognize JFrog's position in the DevOps toolchain.

## What JFrog is

JFrog is the leader in **binary and software-supply-chain management** — the **JFrog Platform**, centered on **Artifactory**, is the **universal repository** where all of an organization's *binaries* (build artifacts, packages, container images, dependencies) live and flow from development to production. Where [GitLab (CXXXVI)](../../volume-136-gitlab-certifications/README.md) and [GitHub (LXXXIX)](../../volume-089-github-certifications/README.md) manage the *source code*, **JFrog manages the *binaries*** — the compiled, packaged output the code becomes and that actually ships. It positions the platform as the **Software Supply Chain Platform**: the secure path from a developer's commit to running software.

## The certification program

JFrog certifications are delivered through **JFrog Academy** (free and paid courses, learning paths, and instructor-led training). The structure has two tiers:

| Certification | Tier | Domain |
|:---|:---|:---|
| **Associate JFrog Artifactory** | Associate | Artifact management, deployment |
| **Associate JFrog DevOps HA/DR** | Associate | High availability, disaster recovery, federation |
| **Associate JFrog Security** | Associate | Application security, protection |
| **JFrog Artifactory Certified DevOps Engineer** | Professional | Repos, security, and CI/CD together — the flagship |

The **three Associate certifications** each validate one domain; the **DevOps Engineer** credential is the flagship, validating the full picture — binary repository management, security, and CI/CD pipelines. All certifications carry a **two-year validity**.

## What is published

JFrog publishes the program and the **DevOps Engineer exam mechanics**:

> **Published:** the **DevOps Engineer** exam is **web-based and proctored** (online or at a test center), **47 questions** (multiple choice and multiple answer), **90 minutes**, **70% to pass**, valid **two years**. The three Associate certifications also carry a two-year validity. This is a program that *publishes* its mechanics — a welcome contrast to the portal-gated vendors.

## The Software Supply Chain Platform

Every certification sits on the **JFrog Platform**:

| Module | Does |
|:---|:---|
| **Artifactory** | The universal binary repository — all package types ([Chapter 2](02-artifactory-the-universal-binary-repository.md)) |
| **Xray** | Security & license scanning ([Chapter 5](05-xray-security-and-license-compliance.md)) |
| **Advanced Security / Curation** | Supply-chain protection ([Chapter 6](06-software-supply-chain-security.md)) |
| **Distribution** | Release delivery to edges ([Chapter 8](08-the-devops-pipeline-and-distribution.md)) |
| **Pipelines** | CI/CD |

The unifying idea: Artifactory is the **single source of truth for binaries**, and everything else secures, scans, and distributes what flows through it. The lab reads the program and the platform.

## Hands-On Lab

The labs in this volume model binary-management and supply-chain concepts in Python at no cost — JFrog is enterprise software, so the labs model the *decisions and disciplines* the certifications test (repository types, promotion, scanning, HA). JFrog offers a **free tier** and **free JFrog Academy courses**.

### Lab 1.1 — Read the certification program

**Objective:** Place a certification by tier and domain.

```bash
python3 - <<'EOF'
CERTS = [
  # cert,                              tier,          domain,                          mechanics
  ("Associate Artifactory",           "Associate",   "artifact mgmt, deployment",      "2-yr validity"),
  ("Associate DevOps HA/DR",          "Associate",   "high availability, DR, federation","2-yr validity"),
  ("Associate Security",              "Associate",   "application security",           "2-yr validity"),
  ("Artifactory Certified DevOps Engineer","Professional","repos + security + CI/CD","47Q / 90min / 70% / 2-yr / proctored"),
]
print(f"{'certification':42}{'tier':14}domain")
for cert, tier, domain, mech in CERTS:
    print(f"{cert:42}{tier:14}{domain}")
    print(f"{'':42}{'':14}  ({mech})")
print("\nHow to read it — two tiers:")
print("  THREE ASSOCIATE certs, each validating ONE domain: Artifactory (the repo),")
print("     HA/DR (keep it running), Security (protect it).")
print("  the DEVOPS ENGINEER credential is the flagship — the FULL picture (repos +")
print("     security + CI/CD together). Its exam is PUBLIC: 47Q, 90min, 70% to pass,")
print("     proctored, 2-year validity.")
print("\nAll certs carry a 2-YEAR validity. JFrog PUBLISHES the DevOps Engineer mechanics")
print("(unlike portal-gated vendors). Pick the Associate for your focus, or go for the")
print("DevOps Engineer to prove the end-to-end binary + supply-chain skill.")
EOF
```

**Expected result:** Three Associate certifications (Artifactory, HA/DR, Security) each validating one domain, with the DevOps Engineer as the flagship covering repos, security, and CI/CD together — its public mechanics being 47 questions, 90 minutes, 70% to pass, proctored, two-year validity. The program lesson is the two-tier structure with published DevOps Engineer mechanics.

**Negative test:** Assuming one general JFrog certification. There are three domain-specific Associate certs plus the flagship DevOps Engineer — you pick the Associate for your focus or the DevOps Engineer for the end-to-end credential.

**Cleanup:** None.

### Lab 1.2 — Source code versus binaries: where JFrog fits

**Objective:** See why binaries need their own management layer.

```bash
python3 - <<'EOF'
STAGES = [
  # stage,                what it is,               tool layer
  ("developer writes code","source (human-readable)","Git / GitHub / GitLab"),
  ("CI builds it",         "compile/package",        "CI (Jenkins/GitLab CI/Actions)"),
  ("output = BINARIES",    "artifacts, images, pkgs","JFROG ARTIFACTORY  <-- here"),
  ("pull dependencies",    "3rd-party binaries",     "JFROG (remote repos, cached)"),
  ("scan for risk",        "vulns + licenses",       "JFROG XRAY"),
  ("promote + distribute", "dev -> staging -> prod", "JFROG (promotion + Distribution)"),
  ("deploy to production", "run the binaries",       "k8s / servers"),
]
print(f"{'stage':26}{'what':26}tool")
for stage, what, tool in STAGES:
    mark = "  <==" if "JFROG" in tool.upper() and "here" in tool else ""
    print(f"{stage:26}{what:26}{tool}")
print("\nThe insight: SOURCE CODE and BINARIES are different things needing different")
print("management. Git manages the code (text, diffs, branches). But what actually")
print("SHIPS is BINARIES — the compiled artifacts, container images, and the hundreds")
print("of third-party packages you depend on. Those need a BINARY repository.")
print("\nJFrog Artifactory is that layer: the single source of truth for ALL binaries —")
print("yours (build outputs) AND theirs (cached dependencies) — from the moment CI")
print("produces them, through scanning (Xray) and promotion, to distribution. Git owns")
print("the SOURCE; JFrog owns the BINARIES the source becomes. Both halves of the")
print("software supply chain, and JFrog is the half that runs in production.")
EOF
```

**Expected result:** The software delivery pipeline showing source-code tools (Git) handling human-readable code and JFrog Artifactory handling the binaries — build outputs, cached dependencies, scanning, promotion, and distribution. The positioning lesson is that source and binaries are different things needing different management, and JFrog is the single source of truth for the binaries that actually ship.

**Negative test:** Treating a Git repository as sufficient for the whole delivery pipeline. Git manages source code, not the binaries, container images, and third-party packages that ship — those need a binary repository like Artifactory.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The JFrog program understood as three Associate certs plus the flagship DevOps Engineer, via JFrog Academy.
- [ ] The three Associate domains (Artifactory, HA/DR, Security) distinguished, and the DevOps Engineer's public mechanics known.
- [ ] The Software Supply Chain Platform placed, with Artifactory as the single source of truth for binaries.
- [ ] JFrog positioned as the binary/supply-chain layer complementing source-code tools like Git.
