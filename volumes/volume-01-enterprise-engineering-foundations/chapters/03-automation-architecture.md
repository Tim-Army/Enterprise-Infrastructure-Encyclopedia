# Chapter 03: Automation Architecture

![Lab flow for this chapter: every pull request triggers a read-only Validate workflow automatically, while merging to main triggers a separate Deploy workflow that pauses until a configured reviewer approves it; removing the only eligible reviewer demonstrates the approval gate fails closed rather than open.](../../../diagrams/volume-01-enterprise-engineering-foundations/chapter-03-two-stage-pipeline-approval-gate-flow.svg)

*Figure 3-1. Flow used throughout this chapter's Hands-On Lab: the two-stage pipeline's validation job, merge, and approval-gated deploy job, including the no-reviewer negative test.*

## Learning Objectives

- Describe the layered automation model that spans workstation, repository,
  CI, and infrastructure provisioning.
- Distinguish declarative from imperative automation and choose correctly
  between them for a given task.
- Design a CI pipeline with least-privilege, short-lived credentials using
  OIDC federation instead of static secrets.
- Build reusable GitHub Actions workflows and a Terraform plan/apply
  pipeline that separates review from execution.
- Apply supply-chain controls — pinning, provenance, and dependency
  scanning — to automation itself.

## Theory and Architecture

Automation architecture is the design of how change moves from an
engineer's keystroke to a running system, and which automated gates a
change must pass through along the way. Every layer discussed elsewhere in
this volume — the workstation ([Chapter 01](01-building-the-enterprise-developer-workstation.md)), the repository ([Chapter 02](02-repository-architecture.md)),
GitHub project workflow ([Chapter 04](04-github-project-and-workflow-management.md)), and documentation publishing
([Chapter 05](05-documentation-pipelines-and-publishing.md)) — is bound together by automation. This chapter treats
automation itself as an architectural subject with its own design patterns,
failure modes, and security boundary.

### The automation stack

Enterprise automation is best understood as a stack of increasingly
consequential gates, each catching a class of defect the previous layer
cannot:

1. **Local automation** (pre-commit hooks, workstation linting) — catches
   defects before they enter version control, at zero shared-infrastructure
   cost.
2. **Continuous Integration (CI)** — catches defects on every push/PR using
   a shared, disposable execution environment, independent of any one
   engineer's machine.
3. **Continuous Delivery/Deployment (CD)** — promotes a validated artifact
   through environments (dev, staging, production) under progressively
   stricter approval gates.
4. **Infrastructure automation** — provisions and reconciles the actual
   compute, network, and platform resources the delivered artifact runs on,
   typically through infrastructure as code (IaC).

Each layer should fail fast and cheap relative to the layer above it: a
Markdown lint error caught by a pre-commit hook costs an engineer seconds;
the same error caught only by a production publishing job costs a failed
release and an incident review.

### Declarative vs. imperative automation

| Style | Description | Example | Best suited for |
| --- | --- | --- | --- |
| Imperative | A sequence of commands describing *how* to reach a state | A shell script that runs `apt install`, then edits a config file, then restarts a service | One-time bootstrap, glue logic, orchestration of declarative tools |
| Declarative | A description of the *desired end state*, reconciled by a tool | A Terraform `.tf` file, an Ansible playbook's target state, a Kubernetes manifest | Anything that must be idempotent, re-runnable, and diffable |

Enterprise automation architecture generally layers imperative
orchestration (CI workflow steps, bootstrap scripts) around declarative
execution (Terraform, Ansible, Kubernetes manifests) rather than choosing
one style exclusively. The declarative core is what makes infrastructure
changes reviewable as a diff before they are applied — the same "plan
before apply" discipline this volume's Hands-On Labs use for structural
changes.

### Idempotency as the central automation property

Idempotency — the property that running an operation multiple times
produces the same end state as running it once — is what allows automation
to be re-run safely after a partial failure, a network blip, or a retried
CI job. Every automation script in an enterprise pipeline should be
evaluated against this property explicitly; a script that is not idempotent
must be clearly labeled and gated so it cannot be re-run accidentally (for
example, a one-time data migration).

## Design Considerations

- **Where does a check belong?** A check that only needs the source tree
  (linting, structural validation, unit tests) belongs as early as possible
  — ideally pre-commit and again in CI. A check that needs a live
  environment (integration tests, a Terraform plan against real state)
  cannot run pre-commit and must live in CI/CD with appropriate credential
  scoping.
- **Self-hosted vs. vendor-hosted runners.** Vendor-hosted CI runners (for
  example, GitHub-hosted runners) minimize operational burden but limit
  network reachability into private infrastructure and cap compute/time
  per job. Self-hosted runners solve reachability and custom-hardware needs
  but become infrastructure the team must patch, scale, and secure —
  effectively expanding the automation architecture to include runner
  fleet management.

2. **Secrets in CI: static vs. federated.** Static long-lived secrets
  stored as CI secrets are simple but represent a standing credential that
  can leak through logs, forks, or compromised dependencies. OpenID Connect
  (OIDC) federation lets CI exchange a short-lived, workflow-scoped identity
  token for cloud credentials that expire in minutes, with no long-lived
  secret stored anywhere. Prefer OIDC federation wherever the cloud
  provider supports it.

- **Blast radius of a single pipeline identity.** A CI pipeline that can
  both plan and apply infrastructure changes with the same broad credential
  collapses the review/execution boundary that pull-request review is
  supposed to enforce. Separate "plan" (read-only, runs on every PR) from
  "apply" (write-capable, runs only after merge and human approval).
- **Reusable vs. duplicated workflows.** Copy-pasted CI YAML across
  repositories drifts silently; a reusable/composite workflow centralizes
  the logic so a security fix (for example, an action-pinning update)
  propagates from one place. The trade-off is an added layer of indirection
  that engineers must understand to debug a failing pipeline.
- **Matrix explosion.** Testing across multiple OS/version combinations via
  a CI matrix multiplies job count and cost; scope matrices to combinations
  that have actually diverged in behavior historically, not every
  theoretically supported combination.
- **Drift between declared and actual infrastructure state.** Declarative
  IaC assumes it is the sole writer of the resources it manages; manual
  console changes cause drift that a subsequent automated apply may either
  silently revert or fail loudly on, depending on the tool. Decide and
  document which behavior is intended per environment.

## Implementation and Automation

### 1. A layered CI workflow (GitHub Actions)

```yaml
# .github/workflows/validate.yml
name: Validate

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version-file: .node-version

      - name: Enable Corepack
        run: corepack enable

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint and structural validation
        run: scripts/bash/validate.sh
```

Note the explicit, minimal `permissions:` block — GitHub Actions grants a
broad default `GITHUB_TOKEN` scope unless a workflow declares otherwise, and
least-privilege automation starts with narrowing that default.

### 2. Reusable workflow for shared validation logic

```yaml
# .github/workflows/reusable-lint.yml
name: Reusable Lint
on:
  workflow_call:
    inputs:
      working-directory:
        required: false
        type: string
        default: "."

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile
        working-directory: ${{ inputs.working-directory }}
      - run: pnpm exec markdownlint-cli2 "**/*.md"
        working-directory: ${{ inputs.working-directory }}
```

```yaml
# .github/workflows/validate.yml (caller)
jobs:
  lint:
    uses: ./.github/workflows/reusable-lint.yml
```

### 3. OIDC federation instead of static cloud secrets

```yaml
# .github/workflows/terraform-plan.yml
name: Terraform Plan

on:
  pull_request:
    branches: [main]

permissions:
  id-token: write   # required for OIDC
  contents: read
  pull-requests: write

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-terraform-plan
          aws-region: us-east-1

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.9.8

      - run: terraform init
        working-directory: infra/

      - run: terraform plan -no-color -out=tfplan
        working-directory: infra/
```

No AWS access key or secret key is stored anywhere; the IAM role trust
policy restricts which repository and branch may assume it, and the
assumed session expires automatically.

### 4. Separating plan from apply

```yaml
# .github/workflows/terraform-apply.yml
name: Terraform Apply

on:
  push:
    branches: [main]
    paths: ["infra/**"]

permissions:
  id-token: write
  contents: read

jobs:
  apply:
    runs-on: ubuntu-latest
    environment: production   # requires manual approval via environment protection rules
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-terraform-apply
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.9.8
      - run: terraform init
        working-directory: infra/
      - run: terraform apply -auto-approve
        working-directory: infra/
```

The `apply` job uses a GitHub Environment with required reviewers, so a
human must approve execution even though the plan already ran automatically
on the pull request.

### 5. An Ansible playbook invoked from CI for configuration management

```yaml
# playbooks/harden-baseline.yml
---
- name: Apply baseline hardening
  hosts: all
  become: true
  tasks:
    - name: Ensure firewalld is enabled and running
      ansible.builtin.systemd:
        name: firewalld
        enabled: true
        state: started

    - name: Enforce SSH key-only authentication
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PasswordAuthentication'
        line: 'PasswordAuthentication no'
      notify: restart sshd

  handlers:
    - name: restart sshd
      ansible.builtin.systemd:
        name: sshd
        state: restarted
```

```bash
ansible-playbook -i inventory/production.yml playbooks/harden-baseline.yml --check --diff
```

The `--check --diff` combination is Ansible's plan-equivalent: it reports
what would change without applying it, giving the same review-before-apply
pattern as `terraform plan`.

## Validation and Troubleshooting

- **Workflow syntax and logic errors.** Run `actionlint` locally before
  pushing; it catches invalid expressions, unpinned actions, and permission
  misconfigurations that GitHub's own YAML parser does not flag until
  runtime.
- **OIDC trust failures.** An error like `Not authorized to perform
  sts:AssumeRoleWithWebIdentity` almost always means the IAM role's trust
  policy condition (`token.actions.githubusercontent.com:sub`) does not
  match the actual repository/branch/environment claim in the token; print
  the claim with a debug step or check the role's trust policy against the
  workflow's `ref`.
- **Terraform plan/apply drift.** If `terraform apply` reports changes
  immediately after a clean `plan` showed none, suspect a non-idempotent
  provisioner or a resource attribute computed differently between plan and
  apply (common with time-based or randomly generated values); pin or mark
  such attributes with `lifecycle { ignore_changes = [...] }` deliberately,
  not accidentally.
- **Ansible check-mode false confidence.** `--check` mode cannot predict
  the outcome of tasks with conditional logic that depends on facts only
  known after a prior task runs in the same play; treat check-mode plans as
  a strong signal, not an absolute guarantee, for complex playbooks.
- **Matrix job failures isolated to one leg.** When only one matrix
  combination fails, diff its exact tool/OS version against the passing
  legs rather than assuming the code is broken everywhere — this is usually
  a version-specific behavior change, not a universal regression.
- **Reusable workflow debugging.** Failures inside a `workflow_call` job
  report against the calling workflow's run, but the actual failing step is
  in the called workflow's file; open the specific job's logs, not just the
  summary, to find the real file and line.

## Security and Best Practices

- Pin every third-party GitHub Action to a full commit SHA
  (`actions/checkout@<sha>`), not a mutable tag, and use a bot
  (Dependabot or Renovate) to propose SHA updates through normal PR review.
- Prefer OIDC federation over static cloud credentials for every CI-to-cloud
  interaction; where a provider does not support OIDC, use the
  shortest-lived credential mechanism available and rotate on a defined
  schedule.
- Set `permissions:` explicitly and minimally on every workflow and job;
  do not rely on the repository-wide default token scope.
- Separate the identity that can `plan`/`--check` (broad read access) from
  the identity that can `apply` (narrow, environment-scoped write access),
  and gate the latter behind required human approval.
- Scan infrastructure-as-code for misconfiguration before apply (for
  example, `tfsec`/`checkov` for Terraform, `ansible-lint` for playbooks) as
  a CI step, not as a manual habit.
- Treat automation scripts and CI workflow files with the same code-review
  rigor as application code — a malicious or careless change to a workflow
  file can exfiltrate secrets or escalate privilege for the entire
  repository.
- Log automation actions with enough context (who triggered it, what
  changed, what approved it) to support an audit; CI run history plus
  environment approval records typically satisfy this if retained per
  organizational policy.

## References and Knowledge Checks

**References**

- [GitHub Actions documentation](https://docs.github.com/en/actions) — reusable workflows, OIDC, and environment
  protection rules.
- [HashiCorp Terraform documentation](https://developer.hashicorp.com/terraform/docs) — `terraform plan`, `terraform apply`,
  and the `lifecycle` meta-argument.
- [Ansible documentation](https://docs.ansible.com/) — check mode and idempotency guarantees per module.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Terraform 1.9.x
  and Ansible core 2.17 / ansible 10.x baseline used throughout this
  encyclopedia.
- [AUTOMATION.md](../../../AUTOMATION.md) — this repository's own
  validation and publishing automation as a worked example.

**Knowledge checks**

1. Why should the "plan" and "apply" stages of an infrastructure pipeline
   use different identities with different privilege levels?
2. What problem does OIDC federation solve that a rotated static secret
   does not?
3. Give an example of automation that must not be treated as idempotent,
   and explain how the pipeline should gate against accidental re-runs.
4. Why is pinning a GitHub Action to a SHA stronger than pinning to a
   version tag such as `v4`?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each element of automation architecture** —
task automation, CI pipelines, pre-commit hooks, and idempotence. Labs use `make`, GitHub Actions
YAML, and `pre-commit`. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.4** — `git`, `make`, and (Lab 3.3) `pre-commit`. Work in a
scratch repo. **Cost:** none.

### Lab 3.1 — Task automation with a Makefile (Topic: Task automation)

**Objective:** Give the project one consistent command interface.

```bash
mkdir -p ~/auto && cd ~/auto
cat > Makefile <<'EOF'
.PHONY: lint build test
lint:  ; @echo "running linters..."
build: lint ; @echo "building..."
test:  build ; @echo "running tests..."
EOF
make test
```

**Expected result:** `make test` runs lint → build → test via declared dependencies — a Makefile (or
task runner) gives every contributor and CI one canonical set of commands (`make lint/build/test`),
so the "how do I build this" knowledge lives in the repo, not in someone's head.

**Negative test:** document build steps only in a README prose paragraph; steps drift from reality and
CI runs different commands than developers — a task runner makes the commands executable and shared.

**Cleanup:** `rm -rf ~/auto`.

### Lab 3.2 — A CI pipeline (Topic: CI/CD)

**Objective:** Run the same tasks automatically on every change.

```bash
mkdir -p ~/auto/.github/workflows && cd ~/auto
cat > .github/workflows/ci.yml <<'EOF'
name: ci
on: [push, pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make lint
      - run: make build
      - run: make test
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('workflow valid')"
```

**Expected result:** a pipeline that runs `make lint/build/test` on every push/PR — CI executes the
same task interface (Lab 3.1) automatically, so broken changes fail before merge and `main` stays
green; the pipeline is the mechanical gate that enforces quality.

**Negative test:** rely on contributors to run checks locally; someone forgets and a broken change
merges — CI runs the checks on every change without depending on anyone's memory.

**Cleanup:** `rm -rf ~/auto`.

### Lab 3.3 — Pre-commit hooks (Topic: Shift-left checks)

**Objective:** Catch issues before they are committed.

```bash
cd ~/auto 2>/dev/null || mkdir -p ~/auto && cd ~/auto && git init -q
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks: [ {id: trailing-whitespace}, {id: end-of-file-fixer}, {id: check-yaml} ]
EOF
python3 -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml')); print('config valid')"
# pre-commit install   # wires hooks into .git/hooks so they run on every commit
```

**Expected result:** a valid pre-commit config that, once installed, fixes whitespace/EOF and
validates YAML at commit time — pre-commit "shifts left," catching trivial issues on the developer's
machine before they reach CI, the cheapest place to fix them.

**Negative test:** depend only on CI for whitespace/YAML checks; developers push broken commits and
wait for a red pipeline — pre-commit catches the same issues seconds earlier, locally.

**Cleanup:** `rm -rf ~/auto`.

### Lab 3.4 — Idempotent automation (Topic: Idempotence)

**Objective:** Make an automation script safe to re-run.

```bash
cat > ensure.sh <<'EOF'
#!/bin/bash
# Idempotent: converge to desired state, safe on repeat
mkdir -p /tmp/app/config                       # -p: no error if it exists
grep -qxF "mode=prod" /tmp/app/config/app.conf 2>/dev/null || echo "mode=prod" >> /tmp/app/config/app.conf
EOF
bash ensure.sh; bash ensure.sh          # run twice
cat /tmp/app/config/app.conf            # still one 'mode=prod' line
```

**Expected result:** running twice leaves the same single-line result — **idempotence** (same outcome
however many times it runs) is the property that lets automation be re-run safely after a failure or
on a schedule, the basis of declarative tools (Terraform, Ansible).

**Negative test:** replace the guarded append with a plain `echo >>`; each run adds a duplicate line
and re-running corrupts state — non-idempotent automation is dangerous to re-run, which idempotence
fixes.

**Cleanup:** `rm -rf /tmp/app ensure.sh`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Automation architecture layers local, CI, CD, and infrastructure automation
so each layer catches defects as early and cheaply as possible. Declarative
tools provide the reviewable, idempotent execution model that makes
"plan before apply" possible, while OIDC federation and separated
plan/apply identities keep credential exposure and blast radius minimal.
Every automation surface — scripts, workflows, and IaC — deserves the same
review rigor as application code, because it holds equivalent or greater
privilege.

- [ ] Can describe the four-layer automation stack and what each layer
      catches.
- [ ] Can explain when to use declarative versus imperative automation.
- [ ] Can configure OIDC federation in place of a static cloud credential.
- [ ] Can separate a read-only plan stage from an approval-gated apply
      stage in a CI/CD pipeline.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
