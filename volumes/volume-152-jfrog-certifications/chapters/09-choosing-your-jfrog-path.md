# Chapter 09: Choosing Your JFrog Path

## Learning Objectives

- Sequence a JFrog certification path by role.
- Understand the two-year currency cycle.
- Place JFrog skills in the DevOps / platform-engineering career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the program [Chapter 1](01-the-jfrog-certification-program.md) laid out.*

## Sequencing your path

The path depends on whether you want **domain depth** (an Associate cert) or the **end-to-end credential** (DevOps Engineer):

| You are | Start | Then |
|:---|:---|:---|
| **DevOps / platform engineer** | Associate Artifactory | → **DevOps Engineer** (the flagship) |
| **Platform reliability / ops** | Associate Artifactory | Associate HA/DR |
| **DevSecOps / security engineer** | Associate Security | + Associate Artifactory → DevOps Engineer |
| **Aiming for the full credential** | Associate Artifactory | Associate Security + HA/DR → DevOps Engineer |

**Associate Artifactory is the foundation** — you cannot do HA/DR, security, or the DevOps Engineer credential without understanding the repository model first. From there, add the Associate that matches your focus (HA/DR for reliability, Security for DevSecOps), and the **DevOps Engineer** is the capstone that validates the whole end-to-end flow ([Chapter 8](08-the-devops-pipeline-and-distribution.md)) — the highest-value single JFrog credential for a DevOps role.

Because the DevOps Engineer covers repos + security + CI/CD together, the Associates are natural stepping stones toward it, and the strongest path for most is **Associate Artifactory → the domain Associate you need → DevOps Engineer.**

## Currency

JFrog certifications carry a **two-year validity**. The platform moves — new package-type support, Advanced Security capabilities, supply-chain features (SBOMs, provenance evolving with regulation) — so a two-year cycle keeps the credential current. Renewal, and staying engaged with **JFrog Academy** as the platform adds capabilities, is the discipline.

Supply-chain security especially is a fast-moving area: SBOM mandates, provenance standards (SLSA and successors), and new classes of supply-chain attack keep emerging. Pair certification with hands-on operation and treat each major platform release and each shift in supply-chain regulation as the drumbeat that keeps your *skill* current.

## The DevOps / platform-engineering career

JFrog skills sit at the center of modern software delivery: **every organization that ships software has a binary supply chain**, and managing it — securely, reliably, at scale — is core platform engineering. An engineer who can run the binary hub, secure the supply chain, keep it highly available, and wire it into CI/CD is exactly the DevOps/platform profile in demand, made more valuable by the surging focus on **software supply chain security**.

The career pairs naturally with adjacent skills this shelf covers:

- **[GitLab (CXXXVI)](../../volume-136-gitlab-certifications/README.md) / [GitHub (LXXXIX)](../../volume-089-github-certifications/README.md)** — the source-and-CI side JFrog's binary side completes.
- **[Snyk (CXLVIII)](../../volume-148-snyk-certifications/README.md)** — developer-side SCA; Xray is the binary-hub-side complement (both secure the supply chain).
- **[CNCF Kubernetes (XLI)](../../volume-041-cncf-kubernetes-certifications/README.md)** — the container platform JFrog stores images for and deploys to.
- **[HashiCorp (XLII)](../../volume-042-hashicorp-certifications/README.md)** — the IaC/automation that provisions the pipeline JFrog anchors.

JFrog is the binary-and-supply-chain specialty at the moment supply-chain security became a board-level concern. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal JFrog plan. **Cost:** none.

### Lab 9.1 — Build your JFrog certification path

**Objective:** Generate a role-appropriate sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "DevOps / platform engineer": [
    ("Associate Artifactory", "the foundation — the repository model", "2 yrs"),
    ("Associate Security or HA/DR", "your focus domain", "2 yrs"),
    ("DevOps Engineer", "the capstone — repos + security + CI/CD (47Q/90min/70%)", "2 yrs"),
  ],
  "platform reliability / ops": [
    ("Associate Artifactory", "the repository model", "2 yrs"),
    ("Associate HA/DR", "clustering, replication, federation — keep the hub up", "2 yrs"),
  ],
  "DevSecOps / security engineer": [
    ("Associate Security", "Xray, Curation, supply-chain security", "2 yrs"),
    ("Associate Artifactory", "the model security sits on", "2 yrs"),
    ("DevOps Engineer", "the end-to-end secure pipeline", "2 yrs"),
  ],
}
role = "DevOps / platform engineer"   # change to taste
print(f"JFrog path for: {role}\n")
print(f"   {'step':32}{'validity':>9}")
for cert, why, val in PATHS[role]:
    print(f"   {cert:32}{val:>9}   {why}")
print("\nGuidance:")
print("  - START with Associate ARTIFACTORY — the repository model everything builds on.")
print("  - add the Associate for your focus: HA/DR (reliability) or Security (DevSecOps).")
print("  - the DEVOPS ENGINEER is the capstone — it validates the full end-to-end flow")
print("    (repos + security + CI/CD). Its exam is public: 47Q, 90min, 70% to pass.")
print("  - CURRENCY: 2-year validity; supply-chain security moves fast (SBOM mandates,")
print("    provenance standards). Re-engage with JFrog Academy as the platform evolves.")
EOF
```

**Expected result:** A role-specific sequence starting with Associate Artifactory, adding the focus Associate (HA/DR or Security), and capping with the DevOps Engineer credential, all on a two-year cycle. The build-your-path lesson is to anchor on the repository model, add your domain Associate, and pursue the DevOps Engineer as the end-to-end capstone, keeping currency against fast-moving supply-chain security.

**Negative test:** Attempting the DevOps Engineer or an HA/DR cert without the Artifactory foundation. They assume the repository model; Associate Artifactory is the prerequisite understanding that the others build on.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Position JFrog in the DevOps career

**Objective:** Map JFrog skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("JFrog (binary/supply chain)", "the binary hub + supply-chain security", "the specialty itself"),
  ("GitLab / GitHub", "source code + CI",              "the code side JFrog's binary side completes"),
  ("Snyk (CXLVIII)", "developer-side SCA",             "Xray is the binary-hub-side complement"),
  ("CNCF / Kubernetes", "container platform",          "JFrog stores the images + deploys to it"),
  ("HashiCorp (Terraform)", "IaC / automation",        "provisions the pipeline JFrog anchors"),
  ("SBOM / SLSA", "supply-chain transparency + provenance","the standards JFrog implements"),
]
print("JFrog in the DevOps / platform-engineering skill map:\n")
print(f"   {'skill':30}{'domain':42}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:30}{domain:42}{why}")
print("\nThe career thesis: EVERY org that ships software has a BINARY supply chain, and")
print("managing it securely, reliably, at scale is core platform engineering — made")
print("board-level urgent by the surge in SOFTWARE SUPPLY CHAIN SECURITY concern.")
print("\nThe rounded platform engineer combines:")
print("  CODE      (GitLab/GitHub)   — the source + CI")
print("  BINARIES  (JFrog Artifactory)— the single source of truth for artifacts")
print("  SECURE    (Xray/Curation + Snyk) — scan + gate the supply chain")
print("  RUN       (Kubernetes)      — where the binaries deploy")
print("  AUTOMATE  (Terraform)       — provision it all as code")
print("  PROVE     (SBOM/provenance) — transparent, verifiable supply chain")
print("\nNone of it is siloed — it's the build/secure/ship pipeline the DevOps shelf")
print("teaches, and JFrog owns the BINARY + supply-chain heart of it. Start with")
print("Associate Artifactory, climb to DevOps Engineer, and pair with code + container")
print("+ IaC skills — that's a platform-engineering career, not just a certificate.")
EOF
```

**Expected result:** JFrog skills mapped to adjacent competencies — GitLab/GitHub (code/CI), Snyk (dev SCA), Kubernetes (runtime), Terraform (IaC), SBOM/SLSA (provenance) — showing the rounded code/binaries/secure/run/automate/prove platform profile. The career-positioning lesson closes the volume: JFrog owns the binary and supply-chain heart of software delivery at the moment supply-chain security became board-level, pairing with the code, container, and IaC skills the rest of the shelf teaches.

**Negative test:** Treating JFrog as an isolated artifact-storage tool. It is the binary hub and supply-chain-security control point at the center of the delivery pipeline, complementing source-code tools, dev-side scanners, container platforms, and IaC — isolating it undersells both the platform and the career.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A JFrog path sequenced by role, anchored on Associate Artifactory and capped by the DevOps Engineer credential.
- [ ] Currency understood as the two-year cycle against a fast-moving platform and supply-chain-security landscape.
- [ ] JFrog positioned in the DevOps / platform-engineering career alongside code, container, IaC, and provenance skills.
- [ ] The volume assembled into a personal study and career plan — code, binaries, secure, run, automate, prove.
