# Chapter 03: Terraform Authoring and Operations Professional

## Learning Objectives

- Explain what the Terraform Authoring and Operations Professional certifies and its lab-based format.
- List the six Professional objectives.
- Apply advanced authoring — lifecycle, dynamic configuration, modules, and providers.
- Operate collaborative Terraform workflows with HCP Terraform.
- Complete a per-objective walkthrough for each Professional objective.

## Theory and Architecture

The **Terraform Authoring and Operations Professional** is the hands-on,
**lab-based** credential for engineers who **author reusable Terraform and
operate it at team scale**. Unlike the Associate exam, it is **four hours,
lab-based plus multiple-choice**: you write and troubleshoot real configuration,
not just answer questions. Six objectives:

| # | Objective |
|---|-----------|
| 1 | Manage resource lifecycle |
| 2 | Develop and troubleshoot dynamic configuration |
| 3 | Develop collaborative Terraform workflows |
| 4 | Create, maintain, and use Terraform modules |
| 5 | Configure and use Terraform providers |
| 6 | Collaborate on infrastructure as code using HCP Terraform |

## Design Considerations

This exam rewards **authoring depth**: lifecycle meta-arguments
(`create_before_destroy`, `prevent_destroy`, `ignore_changes`), dynamic
configuration (`for_each`, `count`, `dynamic` blocks, expressions and functions),
robust **modules** (inputs, outputs, versioning, composition), **provider**
configuration (aliases, version constraints), and **collaboration** (remote
state, workspaces, HCP Terraform runs and policy). Prepare by building
non-trivial configurations and debugging them, since the exam is hands-on.

## Implementation and Automation

The labs below use the `terraform` CLI with the `local`, `random`, and `null`
providers to exercise each objective — lifecycle, dynamic blocks, collaborative
workflow, modules, providers, and HCP Terraform — without a cloud account.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
developer.hashicorp.com/certifications > Terraform Authoring and Operations Professional:
  - six objectives, four hours (incl. 15-min break), lab-based + multiple-choice
  - hands-on: prepare by authoring and troubleshooting real configuration
```

Common pitfalls: overusing `count` where `for_each` is safer (index shifts
destroy/recreate resources); ignoring **provider version constraints** (breaking
changes on upgrade); and treating the exam as multiple-choice — it is **lab-
based**.

## Security and Best Practices

Use **`for_each`** over `count` for stable addressing; pin **module and provider
versions**; mark sensitive outputs `sensitive = true`; protect **remote state**
with locking and least-privilege access; and gate applies with **policy**
(Sentinel/OPA) in HCP Terraform.

## References and Knowledge Checks

- developer.hashicorp.com: *Terraform Authoring and Operations Professional* objectives; Terraform language docs.

**Knowledge checks**

1. When should you use `for_each` instead of `count`, and why?
2. What do `create_before_destroy` and `prevent_destroy` do?
3. What does HCP Terraform add for collaborative workflows?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every Professional objective**.

**Shared prerequisites** — a Linux shell with `terraform`; internet for provider
downloads. Work in an empty directory. **Cost:** none.

### Lab 3.1 — Objective 1: Manage resource lifecycle

**Objective:** Use lifecycle meta-arguments to control replacement.

```bash
mkdir -p tf-pro && cd tf-pro
cat > main.tf <<'HCL'
terraform { required_providers { local = { source = "hashicorp/local" } } }
resource "local_file" "cfg" {
  filename = "cfg.txt"
  content  = "v1"
  lifecycle { create_before_destroy = true, ignore_changes = [content] }
}
HCL
terraform init -no-color >/dev/null && terraform apply -auto-approve -no-color | tail -2
```

**Expected result:** apply creates `cfg.txt`; `ignore_changes = [content]` means
later content edits won't trigger a change, and `create_before_destroy` reorders
replacement — lifecycle control (Objective 1).

**Negative test:** rely on default replacement for a resource that must not have
downtime; use **`create_before_destroy`** so the new resource exists before the
old is removed.

**Rollback:** stay in `tf-pro`.

### Lab 3.2 — Objective 2: Develop and troubleshoot dynamic configuration

**Objective:** Generate resources dynamically with `for_each` and functions.

```bash
cat > dyn.tf <<'HCL'
locals { envs = toset(["dev", "stage", "prod"]) }
resource "local_file" "env" {
  for_each = local.envs
  filename = "${each.key}.txt"
  content  = upper(each.key)
}
HCL
terraform apply -auto-approve -no-color >/dev/null && ls *.txt && cat prod.txt
```

**Expected result:** three files (`dev.txt`, `stage.txt`, `prod.txt`) with
uppercased content — `for_each` plus the `upper()` function, dynamic
configuration (Objective 2).

**Negative test:** use `count` with a list and then reorder it; indices shift and
resources are destroyed/recreated — `for_each` keys are stable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Objective 3: Develop collaborative Terraform workflows

**Objective:** Use workspaces to separate environments' state.

```bash
terraform workspace new staging 2>/dev/null; terraform workspace new production 2>/dev/null
terraform workspace list
terraform workspace select production && terraform workspace show
```

**Expected result:** `staging` and `production` workspaces listed with
`production` selected — isolated state per environment, a collaborative-workflow
pattern (Objective 3).

**Negative test:** run dev and prod from one default workspace/state; a mistake in
one affects the other — separate with **workspaces** or separate state.

**Rollback:** `terraform workspace select default`

### Lab 3.4 — Objective 4: Create, maintain, and use Terraform modules

**Objective:** Author and call a local module.

```bash
mkdir -p modules/greeting
cat > modules/greeting/main.tf <<'HCL'
variable "name" { type = string }
resource "local_file" "g" { filename = "${var.name}.greet", content = "hi ${var.name}" }
output "file" { value = local_file.g.filename }
HCL
cat > usemod.tf <<'HCL'
module "greet_team" { source = "./modules/greeting", name = "team" }
output "greet_file" { value = module.greet_team.file }
HCL
terraform init -no-color >/dev/null && terraform apply -auto-approve -no-color >/dev/null
terraform output greet_file
```

**Expected result:** the module creates `team.greet` and its output surfaces
through the root — authoring, calling, and wiring module I/O (Objective 4).

**Negative test:** duplicate the resource block in every config; a **module**
encapsulates and versions it — call the module instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.5 — Objective 5: Configure and use Terraform providers

**Objective:** Pin a provider version and use a provider alias.

```bash
cat > providers.tf <<'HCL'
terraform {
  required_providers {
    random = { source = "hashicorp/random", version = "~> 3.6" }
  }
}
resource "random_pet" "a" { length = 2 }
HCL
terraform init -no-color | grep -iE 'random|version' | head
terraform apply -auto-approve -no-color >/dev/null && terraform output 2>/dev/null; terraform state list | grep random
```

**Expected result:** the `random` provider installed under the `~> 3.6`
constraint and a `random_pet` resource in state — provider configuration and
version pinning (Objective 5).

**Negative test:** leave providers unpinned; a major-version bump can break the
config — constrain versions with `~>`.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.6 — Objective 6: Collaborate on IaC using HCP Terraform

**Objective:** Configure the HCP Terraform remote workflow and policy.

```bash
cat <<'HCL'
terraform {
  cloud {
    organization = "acme"
    workspaces { tags = ["app", "prod"] }
  }
}
HCL
echo "HCP Terraform: remote runs, VCS-driven plans, state + locking, RBAC, and Sentinel/OPA policy gates."
```

**Expected result:** a `cloud` block using workspace **tags** for team
collaboration, plus what HCP enforces (remote runs, RBAC, policy) — Objective 6.

**Negative test:** share a local state file over a network drive; concurrent runs
corrupt it — use **HCP Terraform** or a locking remote backend.

**Rollback:** `cd .. && rm -rf tf-pro`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Terraform Authoring and Operations Professional certifies advanced,
hands-on Terraform across six objectives — resource lifecycle, dynamic
configuration, collaborative workflows, modules, providers, and HCP Terraform —
in a four-hour lab-based exam. It rewards authoring reusable configuration and
operating it at team scale.

- [ ] I can list the six Professional objectives.
- [ ] I can use lifecycle meta-arguments and `for_each` dynamic config.
- [ ] I can author/call a module and pin provider versions.
- [ ] I can use workspaces and the HCP Terraform remote workflow.
- [ ] I completed Labs 3.1–3.6 including each negative test.
