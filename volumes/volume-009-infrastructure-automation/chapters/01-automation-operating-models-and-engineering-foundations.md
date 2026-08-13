# Chapter 01: Automation Operating Models and Engineering Foundations

![Lab flow for this chapter: a baseline repository skeleton is pushed to GitHub with branch protection on main requiring a pull request and passing terraform-fmt/ansible-lint status checks. As a negative test, a feature branch deliberately introduces unformatted HCL and opens a pull request; the terraform-fmt check fails and the merge button is disabled by branch protection, proving a non-conforming change is mechanically blocked rather than relying on manual review diligence. Running terraform fmt -recursive locally, committing the fix, and pushing again turns the check green and allows the merge.](../../../diagrams/volume-009-infrastructure-automation/chapter-01-branch-protection-lint-gate-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: a branch-protected CI lint gate that mechanically blocks a non-conforming pull request.*

## Learning Objectives

- Explain the difference between scripting, infrastructure as code, and
  platform engineering as successive stages of automation maturity.
- Compare centralized center-of-excellence, embedded, and platform-as-a-
  product operating models for an automation practice.
- Apply Team Topologies concepts (stream-aligned, platform, enabling,
  complicated-subsystem teams) to an infrastructure automation organization.
- Design a repository and change-management structure that supports
  trunk-based development for infrastructure code.
- Identify automation anti-patterns (snowflake automation, shadow tooling,
  credential sprawl) and the engineering practices that prevent them.
- Stand up a minimal automation repository with lint gates and branch
  protection as a reproducible starting point for later chapters.

## Theory and Architecture

Infrastructure automation is a software engineering discipline applied to
the operation of compute, network, storage, and platform resources. Treating
automation as software — with version control, code review, automated
testing, and staged delivery — is the foundational shift that separates a
mature automation practice from a collection of scripts on an
administrator's workstation. This chapter establishes the operating models,
organizational patterns, and engineering foundations that the rest of
Volume IX builds on: Terraform 1.9.x for infrastructure as code and Ansible
core 2.17 for configuration management, per the baseline in
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).

### The automation maturity curve

Most organizations progress through recognizable stages:

1. **Ad hoc scripting.** Individual engineers write shell, PowerShell, or
   Python scripts to solve immediate problems. Scripts are imperative,
   host-specific, and rarely version controlled. Knowledge lives in the
   author's head.
2. **Configuration management.** Tools such as Ansible, Chef, Puppet, or
   Salt introduce declarative or idempotent building blocks (modules,
   resources, states) and a shared inventory of managed hosts. Runs are
   still frequently manual or cron-triggered.
3. **Infrastructure as code (IaC).** Provisioning of the resources
   themselves — networks, compute instances, managed services, IAM — is
   expressed declaratively (Terraform, OpenTofu, CloudFormation, Bicep) and
   stored in version control alongside application code.
4. **Pipeline-driven delivery.** Plan, test, and apply stages run inside CI/
   CD pipelines with mandatory review, policy gates, and audit trails
   instead of engineer workstations. This is the subject of [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md).
5. **Self-service platform engineering.** Automation is packaged as a
   product: golden-path modules, service catalogs, and internal developer
   platforms that let application teams provision compliant infrastructure
   without direct access to the underlying APIs. [Chapter 09 of Volume VIII](../../volume-008-containers-platform-engineering/chapters/09-platform-observability-reliability-and-lifecycle-operations.md)
   (Containers and Platform Engineering) covers the platform-product layer
   in depth; this volume covers the automation engine underneath it.

No stage is skipped safely. A team that jumps straight to a self-service
portal without first mastering idempotent, tested, version-controlled
automation ends up automating chaos faster.

### Declarative versus imperative automation

Terraform and Ansible sit at different points on the declarative-imperative
spectrum, and understanding the distinction shapes how each tool is used in
this volume:

- **Terraform** is declarative and stateful. You describe the desired end
  state of infrastructure resources in HCL, and Terraform's provider plugins
  compute a diff against a persisted state file to determine the minimal set
  of create, update, or destroy operations required ([Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)).
- **Ansible** is procedural in its task list but idempotent by convention at
  the module level. Each module (`ansible.builtin.file`,
  `ansible.builtin.package`, `community.general.*`) checks current state
  before acting, so a well-written playbook converges a host to the desired
  state regardless of its starting point ([Chapter 03](03-configuration-management-and-desired-state-convergence.md)).

Neither model is strictly superior. Terraform's state model is well suited
to resources with a clear provider-managed lifecycle (cloud infrastructure,
DNS, SaaS configuration). Ansible's stateless, agentless model is well
suited to configuring hosts and applications where no external state file
should be the source of truth — the running system itself is the state.

### Push versus pull execution models

Automation tooling also differs in how work is delivered to a target:

| Model | Description | Representative tools |
| --- | --- | --- |
| Push | A controller connects outward (SSH, WinRM, API) and executes work on demand. | Ansible, Terraform, Fabric |
| Pull | An agent on the target polls a server or repository and applies configuration locally. | Puppet agent, Chef Client, `rpm-ostree`/image-based pull models |
| Event-driven | Work is triggered by an external event (webhook, queue message, state-change notification) rather than a schedule. | Event-Driven Ansible, AWS EventBridge + Lambda, StackStorm ([Chapter 07](07-workflow-orchestration-and-event-driven-operations.md)) |

Push models are easier to reason about and audit (the controller log is
authoritative) but require network reachability and credentials to every
target. Pull models scale better to large, dynamic, or intermittently
connected fleets but require a trusted agent and a secure enrollment
process. Most enterprise estates use a mix: push-based Ansible for
configuration, pull-based agents for autoscaling fleets, and event-driven
automation for reactive operations.

### Automation control plane

A production automation practice separates four concerns, regardless of
which tools implement them:

- **Source of truth** — version-controlled repositories holding HCL,
  playbooks, roles, and policy definitions.
- **Execution plane** — the runners or workers that actually execute plans
  and playbooks (CI runners, Ansible Automation Platform execution nodes,
  Terraform Cloud/Enterprise agents).
- **State and inventory** — Terraform state backends, Ansible dynamic
  inventory sources, and configuration management databases (CMDBs) that
  describe what exists.
- **Identity and secrets** — the credentials the execution plane uses to
  authenticate to target platforms, covered in depth in [Chapter 06](06-automation-identity-secrets-and-privileged-execution.md).

Keeping these four concerns architecturally distinct — rather than
collapsing them onto a single engineer's laptop — is what allows automation
to be audited, recovered, and scaled.

## Design Considerations

### Choosing an operating model

| Operating model | Description | Strengths | Risks |
| --- | --- | --- | --- |
| Centralized center of excellence (CoE) | A dedicated automation team owns all IaC and playbooks on behalf of consumers. | Strong consistency, deep tooling expertise, easier compliance. | Becomes a bottleneck; consumers lose context on their own infrastructure. |
| Embedded | Automation engineers sit inside product/application teams. | High context, fast iteration for that team. | Duplicated effort, divergent standards across teams. |
| Platform as a product | A platform team builds paved-road modules, pipelines, and self-service interfaces; stream-aligned teams consume them. | Scales expertise without becoming a bottleneck; consistent guardrails. | Requires product-management discipline; a poorly designed paved road gets bypassed. |

Team Topologies maps directly onto this: the platform team is a **platform
team** in the Team Topologies sense, application teams are
**stream-aligned teams**, and a security/compliance function acts as an
**enabling team** that raises the platform team's and stream-aligned teams'
capability rather than doing the work itself. A **complicated-subsystem
team** may own genuinely specialized automation (for example, a network
automation team maintaining Cisco or firewall integrations elsewhere in
this encyclopedia) that is too deep to embed everywhere.

Most enterprises converge on platform-as-a-product for infrastructure
automation once they exceed roughly a dozen application teams, because the
embedded model's duplicated effort and the CoE model's bottleneck both
become unsustainable at that scale.

### Repository topology

Two broad choices, both defensible:

- **Monorepo**: all Terraform modules, environment root modules, and
  Ansible content live in one repository with path-based CI triggers. Easier
  atomic cross-cutting changes and single source of truth; requires careful
  CODEOWNERS and CI path filtering to avoid unrelated teams blocking each
  other.
- **Polyrepo**: modules, environments, and playbook collections are split
  into separate repositories, often published through a module/role
  registry. Better isolation of blast radius and access control; requires
  version pinning discipline so consumers do not silently pick up breaking
  changes.

A common middle ground used throughout this volume: a **module/collection
repository** per reusable component (versioned, tagged, tested in
isolation) and a small number of **environment repositories** that pin
specific module versions and hold only environment-specific variables and
state configuration.

### Change velocity versus blast radius

Automation increases both the speed of beneficial change and the speed of
harmful change. Risk-tier automation explicitly:

- **Low blast radius** (a single non-production host, a scoped tag-based
  Ansible run) can auto-apply on merge.
- **High blast radius** (production networking, IAM, account-level
  Terraform) requires plan review, a policy gate, and a human approval step
  before apply, as detailed in [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md).

### Toil and the case for automation

Google's Site Reliability Engineering literature defines toil as manual,
repetitive, automatable work with no enduring value. An automation
operating model should track toil explicitly — through ticket categorization
or time-tracking — and treat toil reduction as a measurable objective, not
an incidental benefit. A platform team that cannot show toil trending down
is building automation nobody uses.

## Implementation and Automation

### Baseline repository layout

The following layout is used as the running example throughout this
volume. It applies the module/environment split described above inside a
single repository for teams that have not yet split into polyrepo:

```text
infra-automation/
├── .github/
│   └── workflows/
│       ├── lint.yml
│       └── terraform-plan.yml
├── modules/
│   └── network/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       └── backend.tf
├── playbooks/
│   ├── site.yml
│   ├── roles/
│   └── inventory/
│       ├── dev.yml
│       └── prod.yml
├── policy/
│   └── opa/
├── docs/
│   └── adr/
│       └── 0001-record-architecture-decisions.md
└── .pre-commit-config.yaml
```

### Architecture decision records

Every non-trivial automation decision (tool choice, state backend, naming
convention, module boundary) should be recorded as an ADR so future
engineers understand *why*, not just *what*:

```markdown
# 0001: Record Architecture Decisions

## Status
Accepted

## Context
The automation platform team needs a lightweight, durable way to record
significant technical decisions as the repository grows past a single team.

## Decision
We will record architecture decisions as numbered Markdown files under
docs/adr/, following the Michael Nygard ADR format.

## Consequences
Decisions are reviewable in the same pull request as the code that
implements them, and the history survives tool and team changes.
```

### Pre-commit and lint gates

A minimal `.pre-commit-config.yaml` enforces formatting before code ever
reaches CI:

```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.1
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
  - repo: https://github.com/ansible/ansible-lint
    rev: v24.7.0
    hooks:
      - id: ansible-lint
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict
```

### CI lint workflow

```yaml
# .github/workflows/lint.yml
name: lint

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  terraform-fmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.9.8"
      - name: terraform fmt check
        run: terraform fmt -check -recursive
      - name: terraform validate
        run: |
          for dir in environments/*/ modules/*/; do
            (cd "$dir" && terraform init -backend=false -input=false && terraform validate)
          done

  ansible-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install "ansible-core==2.17.*" ansible-lint
      - run: ansible-lint playbooks/
```

Pinning `terraform_version` and `ansible-core` to the versions recorded in
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) keeps local
developer environments, CI, and production execution planes consistent —
the single most common source of "works on my machine" automation failures.

### Trunk-based branching

Use short-lived feature branches merged into `main` through required pull
request review; avoid long-lived environment branches (`dev`, `staging`,
`prod` as branches). Environment promotion is handled by pinned module
versions and separate state, not by branches — branches for environments
inevitably drift and produce merge conflicts that hide real configuration
differences.

## Validation and Troubleshooting

- **Symptom: "it worked when I ran it locally."** Root cause is almost
  always a version or credential mismatch between the engineer's
  workstation and the execution plane. Enforce version pinning (`tfenv`,
  `.terraform-version`, `ansible-core` pinned in `requirements.txt`) and
  require all applies to run through CI, never from a workstation, once a
  repository leaves the bootstrap phase.
- **Symptom: two engineers' changes silently overwrite each other.** This
  indicates missing state locking ([Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)) or missing branch
  protection. Enable required reviews and required status checks on `main`.
- **Symptom: automation debt accumulates invisibly.** Track a toil ledger:
  every manual runbook step or one-off script gets a ticket tagged
  `toil`, reviewed quarterly. A rising toil count with no automation backlog
  movement is a leading indicator of an operating-model failure, not a
  tooling failure.
- **Symptom: shadow automation.** Teams stand up their own scripts or
  Jenkins jobs outside the sanctioned platform because the paved road is
  too slow or too restrictive. Treat this as product feedback: audit for
  shadow tooling during platform reviews and fix the paved road rather than
  only banning the workaround.

## Security and Best Practices

- Require pull request review and passing status checks before any merge to
  `main` that can trigger an apply; use CODEOWNERS to route
  security-sensitive paths (`policy/`, `environments/prod/`) to the
  appropriate reviewers.
- Never grant automation service accounts standing production credentials
  on a developer workstation; scope workstation credentials to read-only or
  non-production access and drive production applies exclusively through
  CI (expanded in [Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)).
- Treat the automation repository itself as a production system: enable
  branch protection, signed commits where feasible, and audit logging on
  the git hosting platform.
- Keep an explicit, reviewed list of who can approve high-blast-radius
  changes (production Terraform applies, inventory changes touching
  security groups or firewall rules); do not rely on implicit trust.
- Record every ADR and keep it discoverable — undocumented decisions are
  reproduced incorrectly by the next engineer who hits the same problem.

## References and Knowledge Checks

### References

- HashiCorp, *Terraform Documentation*, version 1.9.x —
  <https://developer.hashicorp.com/terraform/docs>
- Red Hat, *Ansible Documentation*, ansible-core 2.17 —
  <https://docs.ansible.com/ansible-core/2.17/>
- Skelton, M. and Pais, M., *Team Topologies* (IT Revolution Press, 2019).
- Google, *Site Reliability Engineering* — chapter on eliminating toil —
  <https://sre.google/sre-book/eliminating-toil/>
- Nygard, M., *Documenting Architecture Decisions* —
  <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>

### Knowledge Checks

1. What distinguishes infrastructure as code from earlier configuration
   management practices in the automation maturity curve?
2. In Team Topologies terms, what type of team is a platform-as-a-product
   automation team, and what type of team consumes its paved roads?
3. Why does pinning tool versions across workstation, CI, and execution
   plane reduce production incidents?
4. Give two reasons a monorepo might be preferred over a polyrepo for a
   mid-size automation practice, and two reasons for the reverse.
5. Why is "toil trending down" a better platform team metric than "number
   of playbooks written"?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each engineering foundation of
automation** — version control, structured data, scripting, and idempotence — mapping to the
Cisco Automation "Software Development and Design" domain. Every step is runnable. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 1.1–1.4** — a Linux/macOS host with `git`, `python3`, and
`jq`/`yq` installed. Work in a scratch dir: `mkdir -p ~/auto && cd ~/auto`. **Cost:** none.

### Lab 1.1 — Version control as the source of truth (Topic: Software development)

**Objective:** Track automation code with a branch-and-merge workflow.

```bash
cd ~/auto && git init -q repo && cd repo
echo "name: demo" > config.yaml
git add config.yaml && git commit -qm "initial config"
git switch -c feature/add-region
echo "region: us-east-1" >> config.yaml
git commit -qam "add region"
git switch main && git merge --no-ff feature/add-region -m "merge region" && git log --oneline
```

**Expected result:** a repo whose history shows the feature branch merged into `main` — version
control is the non-negotiable foundation of automation: every change is reviewable, revertible,
and auditable, which is what makes automation safe to run at scale.

**Negative test:** edit infrastructure config directly on a server with no version control; there
is no history, no review, and no rollback — the un-tracked change is exactly what GitOps and
automation discipline exist to eliminate.

**Rollback:** `rm -rf ~/auto/repo`.

### Lab 1.2 — Structured data formats (Topic: Data formats)

**Objective:** Parse and transform JSON and YAML — the lingua franca of automation.

```bash
cd ~/auto
cat > data.json <<'EOF'
{"hosts":[{"name":"web1","role":"web"},{"name":"db1","role":"db"}]}
EOF
jq -r '.hosts[] | select(.role=="web") | .name' data.json
python3 -c "import json,yaml,sys; print(yaml.safe_dump(json.load(open('data.json'))))" 2>/dev/null || \
  python3 -c "import json; print(json.load(open('data.json'))['hosts'][0]['name'])"
```

**Expected result:** `jq` extracts the web host name and Python round-trips JSON↔YAML — APIs,
IaC, and config management all exchange JSON/YAML, so filtering (`jq`/`yq`) and
parsing/generating them in code is a core daily automation skill.

**Negative test:** parse YAML with a plain text tool (grep/sed) instead of a real parser; nested
structures and multi-line values break it — structured data needs a structured parser, not line
matching.

**Rollback:** `rm -f ~/auto/data.json`.

### Lab 1.3 — Python for automation (Topic: Scripting)

**Objective:** Build an isolated environment and a small automation script.

```bash
cd ~/auto
python3 -m venv .venv && source .venv/bin/activate
pip -q install requests
cat > check.py <<'EOF'
import sys, json
def summarize(path):
    data = json.load(open(path))
    return {h["role"]: h["name"] for h in data["hosts"]}
if __name__ == "__main__":
    print(json.dumps(summarize(sys.argv[1]), indent=2))
EOF
echo '{"hosts":[{"name":"web1","role":"web"}]}' > d.json
python3 check.py d.json
deactivate
```

**Expected result:** a virtualenv with `requests` installed and a script that summarizes the
data — a **venv** isolates dependencies per project (no system-wide conflicts), and small,
testable functions are the building blocks of automation tooling.

**Negative test:** `pip install` globally as root across many projects; versions collide and one
project's upgrade breaks another — the venv is what isolates each project's dependency set.

**Rollback:** `rm -rf ~/auto/.venv ~/auto/check.py ~/auto/d.json`.

### Lab 1.4 — Idempotence and desired-state thinking (Topic: Design methodology)

**Objective:** Write an operation that is safe to run repeatedly.

```bash
cd ~/auto
cat > ensure.sh <<'EOF'
#!/bin/bash
# Idempotent: ensure a line exists exactly once
f="$1"; line="$2"
grep -qxF "$line" "$f" 2>/dev/null || echo "$line" >> "$f"
EOF
chmod +x ensure.sh
touch hosts.txt
./ensure.sh hosts.txt "10.0.0.1 web1"
./ensure.sh hosts.txt "10.0.0.1 web1"     # run again
wc -l < hosts.txt                          # still 1 line
```

**Expected result:** running the operation twice leaves exactly one line — **idempotence**
(the same result no matter how many times you apply it) is the defining property of good
automation, and the reason declarative tools (Terraform, Ansible) converge to a desired state
rather than blindly repeating actions.

**Negative test:** replace the guarded append with a plain `echo >>`; each run adds a duplicate
line — a non-idempotent operation produces drift and damage when re-run, which automation must
avoid.

**Rollback:** `rm -f ~/auto/ensure.sh ~/auto/hosts.txt`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter framed infrastructure automation as a software engineering
discipline, walked through the maturity curve from ad hoc scripts to
self-service platforms, compared centralized, embedded, and
platform-as-a-product operating models through a Team Topologies lens, and
established the repository, branching, and lint-gate foundations that every
later chapter in this volume assumes are already in place.

- [ ] Can describe the five-stage automation maturity curve and identify
      where a given organization sits on it.
- [ ] Can choose and justify an operating model (CoE, embedded, platform as
      a product) for a given organizational size.
- [ ] Can distinguish push, pull, and event-driven execution models and
      name a representative tool for each.
- [ ] Has a working repository skeleton with pre-commit hooks, a CI lint
      gate, and branch protection enforced on `main`.
- [ ] Understands why version pinning across workstation, CI, and
      execution plane is a security and reliability control, not a
      convenience.
