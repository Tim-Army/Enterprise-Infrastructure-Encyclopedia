# Chapter 08: Automation Security, Governance, and Supply Chains

## Learning Objectives

- Map the components of an infrastructure automation supply chain and the
  attack surface at each stage.
- Apply the SLSA framework's levels as a maturity model for pipeline and
  artifact integrity.
- Scan Terraform and Ansible content for misconfigurations with Checkov and
  tfsec, and generate a software bill of materials (SBOM) for an automation
  repository.
- Sign and verify a release artifact with Sigstore's `cosign`, and require
  verification before it is consumed.
- Configure a Terraform provider mirror and automated dependency updates
  with governed review.
- Diagnose supply-chain-specific failures: lockfile drift, signature
  verification failures, and unreachable mirrors.

## Theory and Architecture

Chapters 02 and 03 each deferred a promise to this chapter: that pinning
`.terraform.lock.hcl` and Ansible collection versions is a supply-chain
control, covered "in depth" here. This chapter delivers on that promise by
treating the entire automation toolchain — not just the infrastructure it
manages — as a system with its own attack surface, integrity requirements,
and governance needs.

### The automation supply chain

An infrastructure-as-code pipeline pulls in trusted content from several
independent points, each a potential compromise vector:

| Stage | Component | What could go wrong |
| --- | --- | --- |
| Source | The repository holding Terraform/Ansible content | An unreviewed, malicious commit merged directly or through a compromised contributor account |
| Dependency resolution | Terraform providers, Terraform modules, Ansible collections/roles | A typosquatted or compromised package published to a public registry (Terraform Registry, Ansible Galaxy) |
| Build/execution environment | The CI runner, its container image, its installed toolchain | A compromised runner image or a poisoned base image executing arbitrary code with pipeline credentials |
| Credential issuance | OIDC federation, Vault, static secrets ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)) | Overly broad trust policies or leaked static credentials granting more access than the pipeline needs |
| Artifact/output | The applied infrastructure, the module release, the container image | A tampered artifact between build and deploy, with no way to detect the tampering |

A control focused only on one stage — reviewing source code, for
example — leaves the others open. [Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)'s `.terraform.lock.hcl` and
[Chapter 03](03-configuration-management-and-desired-state-convergence.md)'s pinned `requirements.yml` address the dependency-resolution
stage specifically; this chapter completes the picture across all five.

### SLSA as a maturity model

The Supply-chain Levels for Software Artifacts (SLSA) framework defines
increasing levels of build and provenance integrity, originally aimed at
application software supply chains but directly applicable to
infrastructure-as-code pipelines:

| SLSA level | Requirement | IaC pipeline equivalent |
| --- | --- | --- |
| Build L1 | Build process is scripted and produces provenance | CI-driven `terraform apply`/`ansible-playbook` runs, not workstation applies |
| Build L2 | Build runs on a hosted, tamper-resistant build service | GitHub-hosted or self-hosted runners with restricted access, not developer laptops |
| Build L3 | Provenance is non-forgeable and the build is isolated per run | Ephemeral, single-use runners; provenance generated and signed by the CI platform itself |

Most enterprise infrastructure pipelines described in this volume already
satisfy Build L1 and L2 by construction — [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)'s plan/apply pipeline
runs on hosted CI, not workstations. Reaching L3 requires signed
provenance and ephemeral, isolated build environments, which this
chapter's `cosign` and SBOM sections work toward.

### Software bill of materials

A software bill of materials (SBOM) is a structured, machine-readable
inventory of every dependency a piece of software (or, here, an
automation repository) pulls in — providers, modules, collections, and
their transitive dependencies — generated so that a newly disclosed
vulnerability in any one of them can be matched against an organization's
actual exposure in minutes rather than by manually auditing every
`required_providers` block and `requirements.yml` across every repository.

## Design Considerations

### Trust boundaries: public registries versus private mirrors

The public Terraform Registry and Ansible Galaxy are convenient and
low-friction, but every module or collection pulled from them is code an
organization did not write, executing with the pipeline's credentials.
Define a deliberate trust boundary:

- **Small teams, low-risk estates.** Public registries are acceptable with
  disciplined pinning (exact or narrowly pessimistic version constraints)
  and routine scanning.
- **Regulated or high-value estates.** Mirror or vendor approved providers,
  modules, and collections into a private registry (Terraform Cloud's
  private registry, JFrog Artifactory, a private Automation Hub), so
  nothing reaches a pipeline without passing through an organization-
  controlled approval and scanning step first.

### Pinning strategy trade-offs, revisited

[Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md) introduced pessimistic (`~> 5.60`) versus exact version
constraints for Terraform providers as a design choice. From a
supply-chain lens, the trade-off sharpens: an exact pin
(`version = "5.60.1"`) guarantees the pipeline never resolves a newly
published, potentially compromised patch release without a deliberate,
reviewed bump — but it also means a critical security fix in `5.60.2`
requires that same deliberate action to adopt. A pessimistic constraint
auto-adopts patch releases (faster security-fix adoption) at the cost of
trusting the upstream publisher's release process implicitly. Committing
`.terraform.lock.hcl` (Terraform) and a Galaxy requirements lockfile-
equivalent (Ansible) makes either strategy's actual resolved versions
explicit and reviewable in every pull request, regardless of which
constraint style is chosen — this is the non-negotiable control, not the
constraint style itself.

### Who approves a new dependency

Define an explicit governance step for introducing a *new* provider,
module, or collection — not just for version bumps of existing ones. A
lightweight review (who publishes it, how actively is it maintained, does
it need the broad permissions it requests) before the first `required_providers`
or `requirements.yml` entry catches a large share of typosquatting and
abandoned-package risk before it ever reaches a running pipeline, at far
lower cost than discovering the same problem after an incident.

### Vendoring and mirroring mechanics

Terraform's CLI configuration supports a `provider_installation` block
that redirects provider resolution through a network mirror or a local
filesystem mirror instead of the public registry, giving a private mirror
strategy technical enforcement rather than relying on engineers
remembering to configure a private source in every module:

```hcl
# ~/.terraformrc (or a CI-provisioned equivalent)
provider_installation {
  network_mirror {
    url = "https://artifacts.acme.internal/terraform-providers/"
  }
}
```

## Implementation and Automation

### Static scanning with Checkov and tfsec

```bash
pip install checkov
checkov -d environments/prod --framework terraform --compact

# tfsec (via the trivy config subcommand in current releases)
trivy config environments/prod
```

```yaml
# .github/workflows/iac-security-scan.yml
name: iac-security-scan

on:
  pull_request:
    paths: ["environments/**", "modules/**"]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Checkov scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: environments/prod
          framework: terraform
          soft_fail: false
      - name: Trivy config scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: config
          scan-ref: environments/prod
          exit-code: "1"
```

Both scanners operate on source HCL, before variables resolve — recall
from [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md) that this makes them the right tool for categorical
findings (a hardcoded credential, a disallowed resource type) and the
wrong tool for anything that depends on resolved variable values, which
belongs in the plan-JSON policy check instead.

### Generating an SBOM

```bash
# syft generates an SBOM from a directory, including lockfiles it recognizes
syft dir:. -o cyclonedx-json > sbom.cdx.json

# Inspect the SBOM for a specific dependency
jq '.components[] | select(.name | test("aws"; "i"))' sbom.cdx.json
```

```yaml
# .github/workflows/sbom.yml (excerpt)
  - name: Generate SBOM
    uses: anchore/sbom-action@v0
    with:
      path: .
      format: cyclonedx-json
      output-file: sbom.cdx.json
  - uses: actions/upload-artifact@v4
    with:
      name: sbom
      path: sbom.cdx.json
```

Publishing the SBOM as a build artifact on every release means a future
vulnerability disclosure in a specific provider version can be answered by
grepping stored SBOMs across every past release, rather than re-cloning
and re-inspecting every repository's lockfile history by hand.

### Signing and verifying a module release with cosign

```bash
# Sign a released module archive (keyless, using the CI platform's
# OIDC identity as the signing identity via Sigstore Fulcio/Rekor)
cosign sign-blob --yes \
  --output-signature module-v2.4.0.tar.gz.sig \
  --output-certificate module-v2.4.0.tar.gz.pem \
  module-v2.4.0.tar.gz

# Verify before consuming the artifact
cosign verify-blob \
  --certificate module-v2.4.0.tar.gz.pem \
  --signature module-v2.4.0.tar.gz.sig \
  --certificate-identity "https://github.com/acme/tf-modules/.github/workflows/release.yml@refs/tags/v2.4.0" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  module-v2.4.0.tar.gz
```

```yaml
# .github/workflows/release.yml (excerpt)
permissions:
  id-token: write
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: tar czf module-v2.4.0.tar.gz modules/network
      - uses: sigstore/cosign-installer@v3
      - run: |
          cosign sign-blob --yes \
            --output-signature module-v2.4.0.tar.gz.sig \
            --output-certificate module-v2.4.0.tar.gz.pem \
            module-v2.4.0.tar.gz
```

This is keyless signing: `cosign` uses the CI job's own OIDC identity
([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)) as the signing identity, recorded in the public Rekor
transparency log, rather than requiring the team to generate, store, and
protect a long-lived private signing key — the signing-key equivalent of
preferring federated credentials over static ones.

### Governed dependency updates with Renovate

```json
// renovate.json
{
  "extends": ["config:recommended"],
  "terraform": {
    "enabled": true
  },
  "packageRules": [
    {
      "matchManagers": ["terraform"],
      "matchDepTypes": ["required_provider"],
      "groupName": "terraform providers",
      "schedule": ["before 9am on monday"],
      "reviewers": ["team:platform-engineering"]
    }
  ]
}
```

Renovate opens a pull request for each eligible version bump instead of
silently widening a floating constraint, so a version bump — whether a
patch fixing a CVE or a major version with breaking changes — goes through
the same review, plan, and policy-check pipeline as any other change
([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)), keeping automatic dependency freshness and reviewed change
control simultaneously true instead of trading one for the other.

## Validation and Troubleshooting

- **Lockfile drift between local and CI.** `terraform init` on a
  contributor's workstation resolved a different provider version than
  the committed `.terraform.lock.hcl` expects; run
  `terraform providers lock -platform=linux_amd64` (and any other CI
  runner platforms in use) to regenerate the lockfile with all needed
  platform hashes committed, not just the contributor's local platform.
- **`cosign verify-blob` fails with an identity mismatch.** Confirm the
  `--certificate-identity` and `--certificate-oidc-issuer` values match
  exactly what the signing workflow's OIDC token actually asserted —
  a wildcard or overly loose identity match defeats the purpose of
  verification, but an overly exact one (pinned to a specific run ID
  instead of the workflow path) breaks on every legitimate new release.
- **Checkov or tfsec reports a finding on a resource intentionally
  configured that way.** Use an inline suppression with a documented
  reason (`# checkov:skip=CKV_AWS_XXX: justification`) rather than
  disabling the check repository-wide — a scoped, justified suppression
  stays reviewable; a global disable silently reopens the check for every
  other resource too.
- **A private provider mirror is unreachable.** Confirm the CLI
  configuration's `network_mirror` URL and TLS trust chain independently
  of Terraform with `curl -v`, and check whether `provider_installation`
  needs a `direct` fallback block for providers not yet mirrored, or
  whether the intent is a hard failure for anything not mirrored — decide
  and document which.
- **SBOM is missing a known dependency.** Confirm the generator (`syft` or
  equivalent) actually supports the lockfile format in use — some tools
  need an explicit catalger enabled for less common ecosystems, and a
  silently incomplete SBOM is worse than an SBOM that fails loudly when it
  cannot parse a dependency file.

## Security and Best Practices

- Commit `.terraform.lock.hcl` and an Ansible collection lockfile-
  equivalent on every change; treat an unpinned or floating dependency
  version as a finding, not a style preference.
- Require static scanning (Checkov/tfsec or equivalent) as a required,
  pre-merge CI check, separate from the plan-JSON policy check in Chapter
  05.
- Generate and retain an SBOM for every release or environment promotion,
  and establish a process for matching newly disclosed CVEs against stored
  SBOMs on a defined cadence.
- Sign release artifacts (modules, collections, container images used by
  execution environments) with `cosign`, and make signature verification a
  required step before any pipeline consumes them — an unsigned or
  unverifiable artifact should fail closed, not warn and proceed.
- Route dependency resolution through a private mirror for any estate with
  regulatory or high-value production exposure, and document the fallback
  behavior (fail closed versus fall through to the public registry)
  explicitly.
- Require review on every dependency-update pull request, whether opened
  by a human or by Renovate/Dependabot — automated proposal is not the
  same as automated approval.

## References and Knowledge Checks

### References

- OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA)* —
  <https://slsa.dev/>
- Sigstore, *cosign Documentation* —
  <https://docs.sigstore.dev/cosign/overview/>
- Bridgecrew, *Checkov Documentation* —
  <https://www.checkov.io/1.Welcome/What%20is%20Checkov.html>
- Anchore, *Syft Documentation* —
  <https://github.com/anchore/syft>

### Knowledge Checks

1. Name the five stages of an automation supply chain and one concrete
   attack vector at each.
2. What does an exact version pin protect against that a pessimistic
   constraint (`~>`) does not, and what does it cost in return?
3. Why is keyless signing with `cosign` and OIDC preferred over a
   long-lived private signing key?
4. What is the practical difference between a source-level scanner
   (Checkov/tfsec) finding and a policy-as-code ([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)) finding, in
   terms of what each can actually evaluate?
5. Why should an automated dependency-update pull request still require
   human review before merge?

## Hands-On Lab

### Objective

Scan a small Terraform module for misconfigurations with Checkov, generate
an SBOM for the same directory, sign the module archive with `cosign` in
keyless mode against a local OIDC-less fallback (key-pair mode, since
keyless signing requires a real CI OIDC issuer), and verify the signature
before and after tampering with the archive.

### Prerequisites

- `pip install checkov`.
- `cosign` installed locally (`brew install cosign` or download from the
  Sigstore releases page).
- `syft` installed locally (`brew install syft` or the official install
  script) — optional; the lab notes a manual fallback if unavailable.
- No cloud account required.

### Steps

1. Reuse (or recreate) the demo module from [Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md):

   ```bash
   mkdir -p supplychain-lab/modules/demo && cd supplychain-lab
   cat > modules/demo/main.tf <<'EOF'
   terraform {
     required_providers {
       random = { source = "hashicorp/random", version = "~> 3.6" }
       local  = { source = "hashicorp/local",  version = "~> 2.5" }
     }
   }

   resource "random_pet" "example" {
     length = 2
   }

   resource "local_file" "example" {
     filename = "${path.module}/output-${random_pet.example.id}.txt"
     content  = "Managed by Terraform: ${random_pet.example.id}\n"
   }
   EOF
   ```

2. Run Checkov against the module:

   ```bash
   checkov -d modules/demo --framework terraform --compact
   ```

3. Generate a signing key pair (local key-pair mode, since this lab has
   no real CI OIDC issuer to use for keyless signing):

   ```bash
   cosign generate-key-pair
   # produces cosign.key (private, keep local) and cosign.pub (public)
   ```

4. Package and sign the module:

   ```bash
   tar czf demo-module.tar.gz -C modules demo
   cosign sign-blob --key cosign.key --yes \
     --output-signature demo-module.tar.gz.sig \
     demo-module.tar.gz
   ```

5. Verify the signature against the public key:

   ```bash
   cosign verify-blob --key cosign.pub \
     --signature demo-module.tar.gz.sig \
     demo-module.tar.gz
   ```

### Expected Results

- Checkov reports its scan summary (passed/failed checks) against
  `modules/demo`; a minimal module like this should pass cleanly or show
  only low-severity informational findings.
- Step 5 prints `Verified OK`.

### Negative Test

Tamper with the archive after signing and re-verify:

```bash
echo "tampered" >> demo-module.tar.gz
cosign verify-blob --key cosign.pub \
  --signature demo-module.tar.gz.sig \
  demo-module.tar.gz
```

Confirm verification fails with an error indicating the signature does not
match — proving that even a one-line append invalidates the signature, and
that consuming this artifact without verification would have gone
undetected.

### Cleanup

```bash
cd .. && rm -rf supplychain-lab
```

## Summary and Completion Checklist

Automation supply-chain security extends far past pinning a provider
version: it spans source review, dependency resolution, the build
environment, credential issuance, and artifact integrity, each with its
own controls. SLSA gives a maturity model for where a pipeline sits today
and what the next concrete improvement is; Checkov/tfsec and policy-as-code
([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)) divide misconfiguration detection between source-level and
resolved-plan-level findings; SBOMs make dependency exposure answerable in
minutes instead of a manual audit; and keyless `cosign` signing extends the
federated-identity principle from [Chapter 06](06-automation-identity-secrets-and-privileged-execution.md) to artifact provenance itself.
None of these controls are effective as one-time setup — lockfiles,
scanners, SBOMs, and signature verification only protect an estate that
keeps running them on every change.

- [ ] Can name the five stages of an automation supply chain and a control
      for each.
- [ ] Has run a source-level scanner (Checkov or tfsec) against a
      Terraform module.
- [ ] Has generated an SBOM for an automation repository.
- [ ] Has signed and verified an artifact with `cosign`, and observed
      verification fail after tampering.
- [ ] Understands the trade-off between exact and pessimistic version
      pinning from a supply-chain perspective, not just a compatibility
      one.
