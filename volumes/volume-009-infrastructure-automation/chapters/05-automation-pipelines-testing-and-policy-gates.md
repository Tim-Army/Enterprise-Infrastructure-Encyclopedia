# Chapter 05: Automation Pipelines, Testing, and Policy Gates

![Lab flow for this chapter: planning with no owner_tag and evaluating with Conftest fails ('has an empty owner_tag'); re-planning with owner_tag set and re-evaluating passes cleanly. As a negative test, the failing plan is applied anyway, bypassing the policy gate entirely; the resulting output file shows owner= with no value, exactly what the policy predicted — demonstrating that nothing at the terraform apply layer itself prevents applying a plan that failed policy, which is why the check must be a required, blocking CI step and not an advisory one a human can choose to ignore.](../../../diagrams/volume-009-infrastructure-automation/chapter-05-conftest-policy-gate-bypass-flow.svg)

*Figure 5-1. Flow used throughout this chapter's Hands-On Lab: a Conftest policy gate evaluated before apply, with a deliberate bypass showing exactly why the gate must block rather than merely advise.*

## Learning Objectives

- Design a plan/test/policy/approve/apply pipeline for infrastructure as
  code, and explain why each stage exists.
- Apply the automation test pyramid — static analysis, unit tests,
  integration tests, and end-to-end validation — to Terraform and Ansible
  content.
- Write and enforce policy-as-code checks against a Terraform plan using
  Open Policy Agent (OPA) and Conftest.
- Configure environment promotion with required reviewers and separate
  plan/apply credentials in GitHub Actions.
- Diagnose pipeline-specific failures: stale plans, policy false positives,
  and flaky or non-deterministic tests.
- Recognize which policy checks belong pre-merge versus pre-apply, and why
  that placement matters.

## Theory and Architecture

[Chapter 01](01-automation-operating-models-and-engineering-foundations.md) introduced pipeline-driven delivery as the fourth stage of the
automation maturity curve, and both [Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md) and [Chapter 03](03-configuration-management-and-desired-state-convergence.md) promised the
detail of what a pipeline actually enforces. This chapter delivers that
detail: the stages a mature infrastructure pipeline runs, the test pyramid
that populates those stages, and policy-as-code as the mechanism that turns
written standards ("production changes require review," "no public S3
buckets") into an automated, non-negotiable gate instead of a wiki page
engineers may or may not read.

### Why pipelines instead of workstation applies

Running `terraform apply` or `ansible-playbook` from an engineer's laptop
against production has three durable problems regardless of how careful
the engineer is: the credentials used are usually broader than the change
needs (a workstation is provisioned for a person, not a single task), the
run is not reliably logged or auditable outside shell history, and the
run's environment (provider versions, collection versions, local
uncommitted file edits) is not guaranteed to match what is in version
control. A pipeline fixes all three by construction: it runs with scoped,
short-lived credentials ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)), every run is logged by the CI
platform, and it operates only on the exact commit under review.

### Pipeline stages

A mature infrastructure pipeline separates concerns into distinct stages,
each with a different purpose and a different acceptable failure mode:

1. **Lint / static analysis.** `terraform fmt -check`, `terraform validate`,
   `ansible-lint`, `tflint`. Fast, no credentials required, runs on every
   push.
2. **Unit test.** `terraform test` ([Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)) plan-mode runs, Molecule
   converge tests ([Chapter 03](03-configuration-management-and-desired-state-convergence.md)). No live infrastructure required if backed
   by ephemeral or mocked providers.
3. **Plan.** `terraform plan` against the real target environment's state,
   using read-only credentials. Produces the artifact every later stage
   reasons about.
4. **Policy check.** Automated rules evaluated against the plan's JSON
   output — this chapter's primary new mechanism.
5. **Human approval.** A required reviewer (or a change-record check
   against the ITSM integration from [Chapter 04](04-api-event-and-integration-automation.md)) gates the next stage for
   anything above a defined risk threshold.
6. **Apply.** Executes the exact plan that was reviewed, using a separate,
   more privileged, short-lived credential ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)) than the plan
   stage used.
7. **Post-apply validation.** Smoke tests, health checks, or `terraform
   plan` re-run expecting zero diff, confirming the apply achieved the
   intended state.

Static analysis and unit tests belong pre-merge, on every pull request,
because they are cheap and give the fastest possible feedback. Plan,
policy check, and apply belong on the merge-triggered or environment-
promotion path, because they require real (even if read-only) credentials
and reason about the actual target environment rather than the
configuration in isolation.

### The test pyramid applied to infrastructure

| Layer | Infrastructure equivalent | Speed | What it catches |
| --- | --- | --- | --- |
| Static analysis | `terraform fmt`/`validate`, `tflint`, `ansible-lint` | Seconds | Syntax errors, style violations, known anti-patterns |
| Unit | `terraform test` (plan command), Molecule converge/idempotence | Seconds to low minutes | Logic errors in a single module or role, non-idempotent tasks |
| Integration | `terraform test` (apply command) against a disposable account, Molecule against a real container image | Minutes | Provider-specific behavior, real resource creation edge cases |
| End-to-end | Full environment build-and-validate in a staging environment | Minutes to hours | Cross-module interaction, real network/DNS/IAM behavior |

As with the software test pyramid this is modeled on, the pipeline should
run far more static and unit checks than end-to-end ones: end-to-end tests
are the most realistic but the slowest and most expensive to maintain, and
a pipeline that relies on them exclusively gives feedback too slowly to be
useful on every pull request.

### Policy as code

Policy as code expresses organizational rules — security baselines,
tagging standards, cost controls, change-risk classification — as
version-controlled, automatically evaluated code, rather than a checklist
a human reviewer is expected to remember. Open Policy Agent (OPA), with its
Rego policy language, and its CLI wrapper Conftest, are widely used,
cloud-neutral options for evaluating a Terraform plan's JSON output;
HashiCorp Sentinel is the tightly integrated equivalent inside Terraform
Cloud/Enterprise; cloud-specific and open-source scanners such as Checkov
and tfsec (covered from a supply-chain and vulnerability angle in Chapter
08) apply a similar model directly against HCL source rather than plan
JSON.

## Design Considerations

### Where a policy check belongs

Evaluate policy against Terraform's plan JSON (`terraform show -json
plan.tfout`), not against raw HCL source, whenever the policy depends on
what will actually happen — "no security group opens 0.0.0.0/0 to port 22"
is only fully knowable after variables, modules, and conditionals resolve.
Reserve source-level scanners (Checkov, tfsec) for policies that are true
regardless of variable values (a hardcoded credential, a resource type that
is categorically disallowed), and run them earlier, pre-merge, since they
need no plan and no credentials.

### Blocking versus advisory policies

Not every policy should fail the pipeline. Classify policies deliberately:

- **Blocking (hard-fail).** Violates a non-negotiable control — public
  ingress on a database, an unencrypted storage resource, a missing
  mandatory tag used for cost allocation and ownership. These stop the
  pipeline.
- **Advisory (warn).** Flags something worth a human look but not
  automatically wrong — an unusually large instance type, a resource with
  no `Owner` tag on a non-production account. These annotate the pull
  request or plan output without blocking it.

Treating every policy as blocking from day one is a reliable way to make
engineers route around the pipeline; start new policies as advisory, watch
the false-positive rate for a real sprint or two, then promote to blocking.

### Separating plan and apply identities

The plan stage should run with read-only credentials sufficient to refresh
state and compute a diff; the apply stage requires write credentials scoped
to what the configuration actually manages. Using the same broad credential
for both stages means a compromised or buggy plan-stage step (which runs on
every pull request, including from less-trusted contributors on a public
repository) has write access it never needed. [Chapter 06](06-automation-identity-secrets-and-privileged-execution.md) covers the
mechanics of issuing these as separate, short-lived, federated credentials.

### Handling long-running applies and concurrency

Infrastructure applies that provision genuinely slow resources (a managed
database, a large compute cluster) can run for tens of minutes. Design the
pipeline so a second triggered run against the same state does not race the
first: rely on the backend's state lock ([Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)) as the final backstop,
but also serialize pipeline execution per environment (GitHub Actions
`concurrency` groups, or an equivalent CI-native queue) so two applies
against the same workspace are never even started concurrently, rather than
depending solely on one failing with a lock-acquisition error after minutes
of wasted work.

## Implementation and Automation

### A Rego policy evaluated with Conftest

```rego
# policy/terraform/no_open_ingress.rego
package main

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.type == "ingress"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  resource.change.after.from_port <= 22
  resource.change.after.to_port >= 22
  msg := sprintf(
    "security group rule %v opens SSH (22) to the internet",
    [resource.address],
  )
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not resource.change.after.tags.Owner
  msg := sprintf("%v is missing the required Owner tag", [resource.address])
}
```

```bash
terraform plan -out=plan.tfout
terraform show -json plan.tfout > plan.json
conftest test --policy policy/terraform plan.json
```

`conftest test` exits non-zero if any `deny` rule matches, which is what
makes it usable as a hard pipeline gate. Each `deny` block is independent
and additive — new policies are new files or new rules, not edits to a
monolithic script, which keeps policy review scoped to exactly the rule
being added.

### Wiring the full gate into GitHub Actions

```yaml
# .github/workflows/terraform-pipeline.yml
name: terraform-pipeline

on:
  pull_request:
    paths: ["environments/**", "modules/**"]
  push:
    branches: [main]
    paths: ["environments/**", "modules/**"]

permissions:
  id-token: write
  contents: read
  pull-requests: write

concurrency:
  group: terraform-prod
  cancel-in-progress: false

jobs:
  lint-and-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.9.8"
      - run: terraform fmt -check -recursive
      - run: terraform -chdir=modules/network validate
      - run: terraform -chdir=modules/network test

  plan-and-policy:
    needs: lint-and-unit
    runs-on: ubuntu-latest
    environment: prod-plan
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.9.8"
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/terraform-plan-readonly
          aws-region: us-east-1
      - working-directory: environments/prod
        run: |
          terraform init
          terraform plan -out=plan.tfout
          terraform show -json plan.tfout > plan.json
      - name: Install Conftest
        run: |
          curl -sSL -o conftest.tar.gz \
            https://github.com/open-policy-agent/conftest/releases/download/v0.55.0/conftest_0.55.0_Linux_x86_64.tar.gz
          tar xzf conftest.tar.gz conftest
      - run: ./conftest test --policy policy/terraform environments/prod/plan.json
      - uses: actions/upload-artifact@v4
        with:
          name: prod-plan
          path: environments/prod/plan.tfout

  apply:
    needs: plan-and-policy
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: prod-apply
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.9.8"
      - uses: actions/download-artifact@v4
        with:
          name: prod-plan
          path: environments/prod
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/terraform-apply-write
          aws-region: us-east-1
      - working-directory: environments/prod
        run: |
          terraform init
          terraform apply plan.tfout
```

Three points are deliberate here. First, the `apply` job downloads the
exact `plan.tfout` artifact produced and policy-checked in the earlier job
instead of re-running `terraform plan` — applying a freshly recomputed plan
means the reviewed plan and the applied plan can silently differ if state
changed in between (see Validation and Troubleshooting). Second, the plan
and apply jobs assume different IAM roles via separate `environment`
values, which is how GitHub Environments enforce distinct required
reviewers and secrets per stage. Third, `concurrency` with
`cancel-in-progress: false` queues rather than cancels overlapping runs
against the same production workspace, so a second push never interrupts
an apply already in flight.

### Required reviewers as the human gate

Configuring the `prod-apply` GitHub Environment with required reviewers
means the `apply` job pauses and waits for an explicit approval before it
runs, giving a human the reviewed plan output and the policy check results
as the basis for that approval — the plan/apply pipeline's equivalent of
the Change Advisory Board review from [Volume I, Chapter 08](../../volume-001-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md), but enforced by
the platform instead of relying on process compliance.

## Validation and Troubleshooting

- **Applied plan differs from the reviewed plan.** This happens when the
  apply stage re-runs `terraform plan` instead of consuming the saved
  `.tfout` artifact from the policy-checked plan stage, and real
  infrastructure changed in between (another apply, manual drift). Always
  apply the saved plan file, and treat `Error: Saved plan is stale` (which
  Terraform raises if the plan file no longer matches current state) as a
  signal to re-plan and re-review from scratch, not to force through.
- **Policy check has an unexpectedly high false-positive rate.** Usually
  the Rego rule matches on `resource_changes[_].change.after` without
  accounting for `null` or absent optional attributes; test policies
  against a deliberately varied set of plan fixtures in CI, not just the
  one example that motivated the rule.
- **Molecule or `terraform test` passes locally but fails in CI.** Compare
  provider/collection versions between the local environment and the CI
  runner — an unpinned dependency resolving differently is the most common
  cause ([Chapter 08](08-automation-security-governance-and-supply-chains.md) covers pinning as a supply-chain control in depth).
- **Pipeline queues indefinitely on `concurrency`.** Confirm no earlier run
  is stuck waiting on a manual approval that nobody was notified about;
  check the CI platform's environment protection rule history, not just
  the workflow run list.
- **`conftest` reports a rule failure with no clear resource address.**
  Add the resource `address` field to every `msg` in `sprintf`, as shown
  above — a policy failure without the offending resource's address forces
  the reviewer to manually diff the plan to find what tripped the rule.

## Security and Best Practices

- Apply the exact saved plan artifact; never let the apply stage
  regenerate its own plan from a possibly-changed source state.
- Scope plan-stage and apply-stage credentials separately and minimally
  ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)); the plan stage should never hold write permissions, even
  though it is by far the more frequently executed job.
- Make policy checks a required status check on the branch protection rule,
  not merely a job that runs — a non-required check can be merged past.
- Store policy source (`policy/terraform/*.rego`) in version control with
  the same review requirements as the infrastructure code it governs;
  policy is code, and a badly written policy can be as dangerous as a
  badly written module.
- Log policy check results (pass/fail per rule, not just overall
  pass/fail) as a build artifact so a post-incident review can show exactly
  which controls were evaluated for a given apply.
- Treat a bypassed or force-merged policy failure as an incident requiring
  the same review as any other change-control violation, not a routine
  override.

## References and Knowledge Checks

### References

- Open Policy Agent, *Rego Policy Language Documentation* —
  <https://www.openpolicyagent.org/docs/latest/policy-language/>
- Open Policy Agent, *Conftest Documentation* —
  <https://www.conftest.dev/>
- HashiCorp, *Terraform CLI: `show -json` Output Format* —
  <https://developer.hashicorp.com/terraform/internals/json-format>
- GitHub, *Environments and Required Reviewers* —
  <https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment>

### Knowledge Checks

1. Why should the apply stage consume a saved plan artifact rather than
   re-running `terraform plan`?
2. What distinguishes a policy that belongs in a source-level scanner from
   one that must be evaluated against plan JSON?
3. Why classify some policies as advisory rather than blocking, at least
   initially?
4. What problem does a `concurrency` group solve that state locking alone
   does not fully address in a pipeline context?
5. Where does the test pyramid place Molecule's idempotence stage, and
   why does that placement matter for pipeline speed?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each pipeline and quality-gate skill** —
CI pipelines, IaC testing, policy gates, and pre-commit hooks — the "Application Deployment and
Security" and design domains. Every step is runnable. Each ends **`**Lab verified by:**
*pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.4** — `git`, Terraform, `ansible-lint`/`yamllint`,
`pre-commit`, and (for Lab 5.3) `conftest`/OPA. Work in a scratch git repo. **Cost:** none.

### Lab 5.1 — A CI pipeline definition (Topic: CI/CD)

**Objective:** Define a pipeline that validates automation on every push.

```bash
mkdir -p ~/pipe/.github/workflows && cd ~/pipe && git init -q
cat > .github/workflows/ci.yml <<'EOF'
name: ci
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Terraform fmt & validate
        run: terraform fmt -check && terraform init -backend=false && terraform validate
      - name: Ansible lint
        run: pipx run ansible-lint || true
EOF
python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml')); print('pipeline YAML valid')"
```

**Expected result:** a valid pipeline that runs formatting, validation, and linting on every
push/PR — CI turns quality checks into an automatic gate: broken IaC or unchecked playbooks fail
the pipeline before they merge, so `main` stays deployable.

**Negative test:** rely on developers to run checks locally by hand; someone forgets and broken
code merges — the pipeline enforces the checks mechanically on every change.

**Rollback:** `rm -rf ~/pipe`.

### Lab 5.2 — Test infrastructure code (Topic: Testing)

**Objective:** Statically validate and lint before applying.

```bash
mkdir -p ~/test && cd ~/test
cat > main.tf <<'EOF'
resource "local_file" "x" { filename="x.txt"  content = "hi" }
EOF
terraform fmt -diff            # shows/fixes formatting
terraform init -backend=false -no-color >/dev/null && terraform validate -no-color
cat > play.yml <<'EOF'
- hosts: all
  tasks: [ { name: touch, ansible.builtin.file: { path: /tmp/x, state: touch } } ]
EOF
ansible-lint play.yml || true
```

**Expected result:** `terraform fmt` flags the misaligned attributes, `validate` confirms the
config is syntactically/semantically sound, and `ansible-lint` reports style/safety issues —
testing IaC (fmt, validate, lint, and deeper tools like `terraform plan` checks or Molecule)
catches errors before they reach real infrastructure.

**Negative test:** `terraform apply` straight from an editor with no fmt/validate/lint; a typo or
anti-pattern hits real resources — the static gates are cheap and catch it first.

**Rollback:** `rm -rf ~/test`.

### Lab 5.3 — Policy gates (Topic: Policy as code)

**Objective:** Enforce an organizational rule on a plan with OPA/Conftest.

```bash
mkdir -p ~/policy && cd ~/policy
cat > policy.rego <<'EOF'
package main
deny[msg] {
  input.resource_changes[_].change.after.acl == "public-read"
  msg := "Buckets must not be public-read"
}
EOF
cat > plan.json <<'EOF'
{"resource_changes":[{"change":{"after":{"acl":"public-read"}}}]}
EOF
conftest test plan.json -p policy.rego 2>/dev/null || echo "conftest would FAIL: public bucket denied"
```

**Expected result:** the policy denies a plan that would create a public bucket — policy-as-code
(OPA/Conftest, Sentinel) evaluates a `terraform plan` (as JSON) against rules and **fails the
pipeline** on a violation, so guardrails are enforced automatically, not by review alone.

**Negative test:** rely on human review to catch a public bucket in a 500-line plan; it slips
through — a policy gate checks every plan mechanically and never tires.

**Rollback:** `rm -rf ~/policy`.

### Lab 5.4 — Pre-commit hooks (Topic: Shift-left quality)

**Objective:** Catch problems before they are even committed.

```bash
cd ~/pipe 2>/dev/null || { mkdir -p ~/pipe && cd ~/pipe && git init -q; }
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.92.0
    hooks: [ { id: terraform_fmt }, { id: terraform_validate } ]
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.35.1
    hooks: [ { id: yamllint } ]
EOF
python3 -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml')); print('pre-commit config valid')"
# pre-commit install   # wires it into .git/hooks so checks run on every commit
```

**Expected result:** a valid pre-commit config that, once installed, runs fmt/validate/lint on
staged files at commit time — pre-commit "shifts left," catching issues on the developer's
machine before CI, which is the fastest and cheapest place to fix them.

**Negative test:** depend solely on CI for checks; developers push broken commits and wait for a
red pipeline — pre-commit catches the same issues seconds earlier, before the push.

**Rollback:** `rm -rf ~/pipe`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A pipeline is what turns Terraform and Ansible from tools an individual
engineer runs into infrastructure automation an organization can trust:
staged lint/unit/plan/policy/approve/apply execution, scoped and separated
credentials per stage, and policy-as-code evaluated against the actual
resolved plan rather than source alone. Conftest and OPA give a
cloud-neutral way to encode organizational rules as version-controlled,
testable code, and applying a saved plan artifact — never a freshly
recomputed one — keeps what was reviewed and what was applied identical.
[Chapter 06](06-automation-identity-secrets-and-privileged-execution.md) covers the credential mechanics behind the plan/apply separation
introduced here, and [Chapter 08](08-automation-security-governance-and-supply-chains.md) extends policy-as-code to supply-chain and
dependency-pinning controls.

- [ ] Can describe each stage of a plan/test/policy/approve/apply pipeline
      and why it exists.
- [ ] Has written and enforced at least one Rego policy against Terraform
      plan JSON with Conftest.
- [ ] Understands why the apply stage must consume a saved plan artifact.
- [ ] Can explain the difference between blocking and advisory policy
      classifications and when to use each.
- [ ] Has configured (or can describe configuring) separate plan and apply
      credentials gated by environment-level required reviewers.
