# Chapter 02: Repository Architecture

## Learning Objectives

- Compare monorepo, polyrepo, and hybrid source-control topologies against
  concrete organizational criteria.
- Design a repository directory layout that scales predictably as content or
  code volume grows.
- Configure branch protection, CODEOWNERS, and commit conventions that
  enforce review and ownership boundaries.
- Implement pre-commit and structural validation that catches defects before
  they reach code review.
- Evaluate the trade-offs of Git submodules, subtrees, and monorepo tooling
  for sharing code across repositories.

## Theory and Architecture

Repository architecture is the set of decisions that determine how source
content is grouped into repositories, how those repositories are internally
organized, and how ownership and change control are enforced at the
version-control layer. Poor repository architecture is expensive to unwind
because build tooling, CI pipelines, access-control policy, and engineer
habits all accrete around whatever structure exists — so this decision
deserves the same design rigor as a network topology or a storage layout.

### Monorepo vs. polyrepo

| Model | Description | Strengths | Weaknesses |
| --- | --- | --- | --- |
| Polyrepo | One repository per service, library, or content domain | Clear ownership boundaries, independent access control, small clone size | Cross-cutting changes require coordinated multi-repo PRs; shared tooling must be versioned and distributed |
| Monorepo | All (or most) related code/content in a single repository | Atomic cross-cutting changes, single CI/lint/version policy, simpler dependency graphs | Requires investment in path-scoped CI, larger clones, coarser default access control |
| Hybrid | A small number of monorepos grouped by domain, plus polyrepos for genuinely independent services | Balances blast radius against coordination cost | Requires an explicit, documented rule for which model a new project falls under |

The right choice depends on team topology, not fashion. Conway's Law applies
directly: a monorepo assumes teams are comfortable reviewing and being
affected by changes outside their immediate area, while a polyrepo assumes
strong team-level autonomy is more valuable than atomic cross-cutting
commits. This encyclopedia's own source repository is itself a working
example of a **structured single-repository, multi-domain layout**: 24
independently versioned content volumes share one root-level toolchain,
validation gate, and publishing pipeline, which is a monorepo pattern
applied to documentation rather than code.

### Directory layout as a contract

A repository's directory layout is a contract with every tool that reads
it — CI workflows, linters, build scripts, and human contributors. The
layout should make three things discoverable within seconds of opening the
repository:

1. **Where source content lives**, and how it is subdivided (by domain, by
   service, by volume).
2. **Where automation lives**, separated from the content it operates on.
3. **Where the canonical rules live** — the file that defines the contract
   itself, so the layout does not silently drift from its documentation.

A layout that requires reading a README before you can find anything has
already failed part of this contract; naming conventions should make most
structure self-evident, with root documentation reserved for rules that
cannot be expressed by directory names alone (ordering, numbering,
required-file sets).

### Ownership and change control primitives

Git hosting platforms provide three primitives that, combined, express an
organization's change-control policy without needing an external system for
routine repository governance:

- **CODEOWNERS** maps paths to required reviewers, so review responsibility
  is declared in-repository and enforced automatically rather than relying
  on tribal knowledge.
- **Branch protection rules** enforce required status checks, required
  reviews, and linear history before a change can reach the protected
  branch.
- **Commit conventions** (such as Conventional Commits) turn commit history
  into machine-parseable metadata that can drive changelog generation and
  semantic versioning without a separate manual step.

## Design Considerations

- **Blast radius vs. coordination cost.** A monorepo minimizes the cost of
  coordinated changes (one PR touches everything affected) but maximizes
  blast radius (a single misconfigured CI job can block every team). A
  polyrepo inverts both. Choose based on how often cross-cutting changes
  actually occur in practice, not how often they seem like they might.
- **CI cost at scale.** Monorepos require path-scoped or affected-only CI
  (build/test only what changed) to avoid CI time growing linearly with
  unrelated content. Decide this before the repository grows past the point
  where a full-repository CI run is tolerable.
- **Access control granularity.** Git hosts generally grant repository-level
  permissions. A monorepo that needs directory-level access restriction
  (for example, a compliance-sensitive subdirectory) may need to extract
  that content into its own repository regardless of other trade-offs,
  because CODEOWNERS enforces required reviewers but not read/write access.
- **Numbering and stable identifiers.** When content or services are
  numbered (`volume-01`, `service-03`), decide up front whether numbers are
  permanent identifiers or ordering hints, and document it — renumbering
  after external systems (build manifests, deployment configs) reference the
  original numbers is expensive.
- **Submodules vs. subtrees vs. package registries.** Submodules pin an
  exact commit of another repository but are notorious for confusing
  contributors who forget to update them; subtrees vendor a copy without a
  separate clone step but complicate upstream sync; a package registry
  (npm, a private OCI registry, a Terraform module registry) is usually the
  better answer when the shared unit is a versioned, publishable artifact
  rather than another team's live source tree.
- **Root-level file sprawl.** Every root-level policy file (README,
  CONTRIBUTING, SECURITY, CODEOWNERS) is a discoverability aid for humans and
  automated scanners alike; missing ones are flagged by many open-source
  health-check tools and by enterprise compliance scanners.

## Implementation and Automation

### 1. Establish the directory contract

Document the canonical path pattern once, in a single root-level file, and
treat every deviation as a defect:

```text
volumes/volume-NN-volume-slug/
├── README.md
├── INDEX.md
├── GLOSSARY.md
└── chapters/
    ├── 01-chapter-slug.md
    └── 02-chapter-slug.md
```

Numbering rules (zero-padded two-digit numbers, kebab-case slugs) should be
written down explicitly rather than inferred, since inference is exactly
where drift enters.

### 2. CODEOWNERS

```text
# .github/CODEOWNERS
# Default owners for everything not matched below.
*                                   @platform-eng-team

# A content domain owned by a dedicated working group.
/volumes/volume-05-vmware-virtualization/  @virtualization-sme-team

# Automation and CI changes require platform review regardless of path.
/.github/                          @platform-eng-team
/scripts/                          @platform-eng-team
```

### 3. Branch protection via the GitHub CLI

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  repos/example-org/example-repo/branches/main/protection \
  -f required_status_checks.strict=true \
  -f 'required_status_checks.contexts[]=validate' \
  -f enforce_admins=true \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -f restrictions=null
```

### 4. Commit conventions

```text
feat(volume-02): add chapter on IP routing fundamentals
fix(scripts): correct chapter-count check in validate.sh
docs(readme): update build instructions for website ZIP output
```

Enforce the pattern with a commit-msg hook (see below) rather than relying
on reviewers to catch violations manually.

### 5. Pre-commit structural validation

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: structure-check
        name: Repository structure validation
        entry: scripts/bash/validate.sh
        language: system
        pass_filenames: false
      - id: commit-msg-format
        name: Conventional commit message check
        entry: scripts/bash/check-commit-msg.sh
        language: system
        stages: [commit-msg]
```

```bash
# scripts/bash/check-commit-msg.sh
#!/usr/bin/env bash
set -euo pipefail
pattern='^(feat|fix|docs|chore|refactor|test)(\([a-z0-9-]+\))?: .+'
if ! grep -qE "$pattern" "$1"; then
  echo "Commit message does not match Conventional Commits format." >&2
  exit 1
fi
```

```bash
pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

### 6. A minimal structure validator

A structural gate like the one this repository runs before every commit
(`scripts/bash/validate.sh`) typically checks, in order: required files per
unit (README/INDEX/GLOSSARY per volume), sequential/gap-free numbering, and
cross-references between a manifest file and the files that actually exist
on disk:

```bash
#!/usr/bin/env bash
# validate-structure.sh — confirm every volume has required files
set -euo pipefail
fail=0
for vol in volumes/*/; do
  for required in README.md INDEX.md GLOSSARY.md; do
    if [[ ! -f "${vol}${required}" ]]; then
      echo "MISSING: ${vol}${required}" >&2
      fail=1
    fi
  done
done
exit "$fail"
```

## Validation and Troubleshooting

- **CODEOWNERS syntax errors fail silently.** GitHub validates CODEOWNERS
  files and surfaces errors under the repository's Insights tab rather than
  blocking a push; check that tab after any CODEOWNERS change, since a typo
  in a path pattern simply results in no required reviewer being assigned.
- **Branch protection not applying to administrators.** If
  `enforce_admins` is left `false` (the API default), repository admins can
  bypass required checks entirely, which defeats the control for exactly
  the accounts most likely to have broad access. Verify with `gh api
  repos/<org>/<repo>/branches/main/protection | jq .enforce_admins`.
- **Pre-commit hook not running.** `pre-commit install` only wires hooks
  into the current clone's `.git/hooks`; a fresh clone must run it again.
  Add a bootstrap step (see Chapter 01) that runs `pre-commit install`
  automatically after clone.
- **Structural validator false negatives.** A validator that only checks
  file *existence* will not catch an empty or stub file; extend checks to a
  minimum content length or a required heading where that risk matters.
- **Diverged submodule pointer.** `git status` reporting a submodule as
  modified with no visible diff usually means the submodule's checked-out
  commit no longer matches the pointer recorded in the parent repository;
  resolve with `git submodule update --init --recursive` and confirm the
  intended commit with `git submodule status`.

## Security and Best Practices

- Require signed commits on protected branches (`required_signatures` in
  branch protection) so history integrity does not depend solely on process
  discipline — see Chapter 01 for signing setup.
- Enable secret scanning and push protection at the repository or
  organization level; treat a blocked push due to a detected secret as a
  correct outcome to investigate, not a false positive to bypass.
- Scope CODEOWNERS and branch protection together: a required reviewer with
  no corresponding write-access restriction can be bypassed by anyone with
  repository write access self-approving through an alternate path (for
  example, merging without review if reviews are not actually required).
  Confirm both controls are active, not just one.
- Keep automation credentials (CI service tokens, bot accounts) scoped to
  the minimum repository set they operate on; a monorepo's single CI
  identity having write access to every path undermines directory-level
  ownership boundaries defined in CODEOWNERS.
- Pin third-party GitHub Actions and pre-commit hook repositories to a full
  commit SHA, not a mutable tag, to prevent a compromised upstream tag from
  silently changing hook or workflow behavior.
- Document repository-architecture decisions as Architecture Decision
  Records (see Chapter 07) so a future reorganization has to justify itself
  against the recorded original reasoning, not against nothing.

## References and Knowledge Checks

**References**

- GitHub documentation — CODEOWNERS syntax and branch protection rules.
- [Structure.md](../../../Structure.md) — this encyclopedia's canonical
  path and naming rules, a working example of a documented directory
  contract.
- [AUTOMATION.md](../../../AUTOMATION.md) — this repository's own
  validation and safe-automation rules.
- Conventional Commits specification — `https://www.conventionalcommits.org`.
- `pre-commit` framework documentation.

**Knowledge checks**

1. What organizational signal should drive a monorepo-vs-polyrepo decision,
   beyond team preference?
2. Why is `enforce_admins: true` necessary for branch protection to be a
   real control rather than an advisory one?
3. Give a scenario where a Git submodule is the right choice over a package
   registry, and one where the reverse is true.
4. What is the difference between CODEOWNERS enforcing review and a
   repository permission enforcing write access, and why do both matter?

## Hands-On Lab

**Objective:** Stand up a small repository with an enforced directory
contract, CODEOWNERS, branch protection, and a pre-commit structural check,
then prove the controls work with both a passing and a failing change.

**Prerequisites**

- `git`, `gh` (authenticated), and `pre-commit` installed.
- Permission to create a repository in your GitHub account or a sandbox
  organization.

**Steps**

1. Create and clone a scratch repository:

   ```bash
   gh repo create repo-architecture-lab --private --clone
   cd repo-architecture-lab
   ```

2. Create the directory contract and a structure validator:

   ```bash
   mkdir -p units/unit-01-example
   touch units/unit-01-example/README.md
   mkdir -p scripts
   cat > scripts/validate-structure.sh <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   fail=0
   for u in units/*/; do
     [[ -f "${u}README.md" ]] || { echo "MISSING: ${u}README.md" >&2; fail=1; }
   done
   exit "$fail"
   EOF
   chmod +x scripts/validate-structure.sh
   ```

3. Add CODEOWNERS and a pre-commit config:

   ```bash
   mkdir -p .github
   echo "* @$(gh api user --jq .login)" > .github/CODEOWNERS
   cat > .pre-commit-config.yaml <<'EOF'
   repos:
     - repo: local
       hooks:
         - id: structure-check
           name: structure check
           entry: scripts/validate-structure.sh
           language: system
           pass_filenames: false
   EOF
   pre-commit install
   ```

4. Commit and push the baseline, then enable branch protection:

   ```bash
   git add -A && git commit -m "feat: initial repository contract"
   git push -u origin main
   gh api --method PUT -H "Accept: application/vnd.github+json" \
     repos/:owner/repo-architecture-lab/branches/main/protection \
     -f required_status_checks.strict=false \
     -f 'required_status_checks.contexts[]=' \
     -f enforce_admins=true \
     -f required_pull_request_reviews.required_approving_review_count=1 \
     -f restrictions=null
   ```

5. **Expected result:** Confirm protection is active:

   ```bash
   gh api repos/:owner/repo-architecture-lab/branches/main/protection --jq .enforce_admins
   ```

   Output must be `true`.

6. Add a second unit that satisfies the contract and confirm the local hook
   passes:

   ```bash
   mkdir -p units/unit-02-example
   touch units/unit-02-example/README.md
   git add -A
   git commit -m "feat: add unit-02"
   ```

   **Expected result:** the `structure-check` hook runs and the commit
   succeeds.

7. **Negative test:** Add a unit that violates the contract and confirm the
   hook blocks it:

   ```bash
   mkdir -p units/unit-03-broken
   git add -A
   git commit -m "feat: add unit-03 (missing README)"
   ```

   **Expected result:** the commit is rejected locally with
   `MISSING: units/unit-03-broken/README.md` before it ever reaches GitHub,
   demonstrating that the structural gate runs pre-commit rather than only
   in CI.

8. **Cleanup:**

   ```bash
   cd .. && rm -rf repo-architecture-lab
   gh repo delete repo-architecture-lab --yes
   ```

## Summary and Completion Checklist

Repository architecture is a durable design decision, not an incidental
file layout. Choosing between monorepo, polyrepo, and hybrid topologies
should be driven by coordination cost, blast radius, and access-control
granularity. Once chosen, the layout becomes a contract enforced by
CODEOWNERS, branch protection, commit conventions, and structural
validation — ideally checked both locally, via pre-commit hooks, and
centrally, in CI.

- [ ] Can compare monorepo and polyrepo trade-offs against a team's actual
      coordination and access-control needs.
- [ ] Can write a CODEOWNERS file and verify it takes effect.
- [ ] Can configure branch protection that genuinely blocks unreviewed or
      unchecked merges, including for administrators.
- [ ] Can implement and test a pre-commit structural validation hook.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
