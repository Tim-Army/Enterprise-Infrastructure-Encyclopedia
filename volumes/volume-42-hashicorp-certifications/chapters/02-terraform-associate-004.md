# Chapter 02: Terraform Associate (004)

## Learning Objectives

- Explain what the Terraform Associate (004) certifies and its exam mechanics.
- List the eight Terraform Associate objectives.
- Perform the core Terraform workflow with the CLI.
- Apply state, modules, configuration, and HCP Terraform concepts.
- Complete a per-objective walkthrough for each Terraform Associate objective.

## Theory and Architecture

The **Terraform Associate (004)** validates a practitioner's grasp of
**infrastructure as code** with Terraform — the declarative provisioning of
infrastructure through configuration files and the **plan/apply** workflow. It is
**one hour, online-proctored, multiple-choice**, and version **004** supersedes
the retired 003. Eight objectives:

| # | Objective |
|---|-----------|
| 1 | Infrastructure as Code (IaC) with Terraform |
| 2 | Terraform fundamentals |
| 3 | Core Terraform workflow |
| 4 | Terraform configuration |
| 5 | Terraform modules |
| 6 | Terraform state management |
| 7 | Maintain infrastructure with Terraform |
| 8 | HCP Terraform |

## Design Considerations

The exam rewards **doing the workflow**: writing HCL, running `init → plan →
apply → destroy`, reading state, and using variables, outputs, and modules. Know
**why** IaC matters (versioned, repeatable, reviewable), how Terraform differs
from configuration management, and how **HCP Terraform** (formerly Terraform
Cloud) adds remote state, runs, and access controls. The labs below use the
`local` and `random` providers so every objective runs without a cloud account.

## Implementation and Automation

Each lab exercises one objective with the real `terraform` CLI — from IaC
concepts through the core workflow, configuration, modules, state, day-two
maintenance, and HCP Terraform.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
developer.hashicorp.com/certifications > Terraform Associate (004):
  - eight objectives, one hour, multiple-choice, online proctored
  - study the 004 objectives (003 is retired)
```

Common pitfalls: confusing `terraform plan` (preview) with `apply` (execute);
editing **state** by hand instead of with `terraform state` subcommands; and
assuming HCP Terraform and Terraform CLI are different tools — HCP Terraform runs
the same core workflow remotely.

## Security and Best Practices

Protect **state** (it can contain secrets) with a remote backend and locking;
never commit `.tfstate` or `*.tfvars` with secrets; pin **provider versions**;
and run `terraform plan` and code review before every `apply`.

## References and Knowledge Checks

- developer.hashicorp.com: *Terraform Associate (004)* objectives and tutorials; Terraform documentation.

**Knowledge checks**

1. What are the four commands of the core Terraform workflow?
2. Why must Terraform state be protected?
3. What does HCP Terraform add over the CLI alone?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every Terraform Associate objective**.

**Shared prerequisites** — a Linux shell with `terraform`; internet for the
one-time provider download. Work in an empty directory. **Cost:** none.

### Lab 2.1 — Objective 1: Infrastructure as Code with Terraform (IaC)

**Objective:** Declare infrastructure as code and see it version-controllable.

```bash
mkdir -p tf-lab && cd tf-lab
cat > main.tf <<'HCL'
terraform { required_providers { local = { source = "hashicorp/local" } } }
resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "infrastructure as code"
}
HCL
terraform fmt && cat main.tf | head -1
```

**Expected result:** `terraform fmt` reformats the file and the config declares a
`local_file` resource — infrastructure expressed as versionable code (Objective
1).

**Negative test:** create the file by hand with `echo`; that is not
reproducible or reviewable — declare it as code so it is.

**Cleanup:** stay in `tf-lab` for the following labs.

### Lab 2.2 — Objective 2: Terraform fundamentals

**Objective:** Initialize the working directory and download the provider.

```bash
terraform init
terraform providers
```

**Expected result:** `Terraform has been successfully initialized!` and the
`hashicorp/local` provider listed — the init step that installs providers and
prepares the backend (Objective 2).

**Negative test:** run `terraform plan` before `init`; it errors that the
directory is not initialized — always `init` first.

**Cleanup:** none.

### Lab 2.3 — Objective 3: Core Terraform workflow

**Objective:** Run the plan → apply → destroy workflow.

```bash
terraform plan
terraform apply -auto-approve
cat hello.txt
terraform destroy -auto-approve
```

**Expected result:** the plan shows `1 to add`, apply creates `hello.txt`
(content `infrastructure as code`), and destroy removes it — the core workflow
(Objective 3).

**Negative test:** skip `plan` and apply blind in real work; always review the
plan so you know what will change.

**Cleanup:** the destroy removed the resource; re-apply for the next labs:
`terraform apply -auto-approve`.

### Lab 2.4 — Objective 4: Terraform configuration

**Objective:** Parameterize with a variable and expose an output.

```bash
cat > variables.tf <<'HCL'
variable "greeting" { type = string, default = "hi" }
output "path" { value = local_file.hello.filename }
HCL
sed -i.bak 's/content  = .*/content  = var.greeting/' main.tf
terraform apply -auto-approve -var greeting="hello-from-var"
terraform output path
```

**Expected result:** apply succeeds using the variable, and `terraform output`
prints the file path — variables and outputs, the configuration language
(Objective 4).

**Negative test:** hard-code every value; **variables** make configuration
reusable across environments — parameterize.

**Cleanup:** `rm -f main.tf.bak`

### Lab 2.5 — Objective 5: Terraform modules

**Objective:** Understand module structure with the implicit root module.

```bash
terraform providers
echo "The current directory IS the root module; child modules are called with 'module' blocks:"
cat <<'HCL'
module "network" {
  source = "./modules/network"
  cidr   = "10.0.0.0/16"
}
HCL
```

**Expected result:** the root-module concept and a `module` block calling a child
module by `source` — module composition (Objective 5).

**Negative test:** copy-paste the same resources across projects; a **module**
packages and reuses them — factor shared config into modules.

**Cleanup:** none.

### Lab 2.6 — Objective 6: Terraform state management

**Objective:** Inspect and manipulate state with `terraform state`.

```bash
terraform state list
terraform state show local_file.hello | head -5
```

**Expected result:** `local_file.hello` in the state list and its attributes from
`state show` — state as the source of truth mapping config to real resources
(Objective 6).

**Negative test:** hand-edit `terraform.tfstate` in a text editor; use
`terraform state` subcommands — manual edits corrupt state.

**Cleanup:** none.

### Lab 2.7 — Objective 7: Maintain infrastructure with Terraform

**Objective:** Detect and reconcile drift; use targeted operations.

```bash
echo "tampered" > hello.txt                 # simulate out-of-band drift
terraform plan | grep -E 'change|update|~' | head
terraform apply -auto-approve               # reconcile back to desired state
cat hello.txt
```

**Expected result:** the plan detects drift (the file changed), and apply
restores the declared content — day-two maintenance and drift reconciliation
(Objective 7).

**Negative test:** fix drift by editing the file directly; Terraform will detect
it again — change the **config** and apply so state and reality agree.

**Cleanup:** none.

### Lab 2.8 — Objective 8: HCP Terraform

**Objective:** Understand HCP Terraform's remote workflow.

```bash
cat <<'HCL'
terraform {
  cloud {
    organization = "my-org"
    workspaces { name = "prod" }
  }
}
HCL
echo "HCP Terraform: remote state, remote runs, VCS-driven plans/applies, RBAC, policy (Sentinel/OPA)."
```

**Expected result:** a `cloud` block binding the config to an HCP Terraform
workspace, plus what HCP adds (remote state/runs, RBAC, policy) — Objective 8.

**Negative test:** store state locally for a team; concurrent applies corrupt it
— use **HCP Terraform** (or a locking remote backend) for collaboration.

**Cleanup:** `cd .. && rm -rf tf-lab`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Terraform Associate (004) certifies the fundamentals of infrastructure as
code with Terraform across eight objectives — IaC concepts, fundamentals, the
core `init/plan/apply/destroy` workflow, configuration (variables/outputs),
modules, state management, day-two maintenance, and HCP Terraform — in a one-hour
multiple-choice exam (study 004, not the retired 003).

- [ ] I can list the eight Terraform Associate objectives.
- [ ] I can run the core workflow and read/modify state safely.
- [ ] I can parameterize with variables and outputs and call a module.
- [ ] I can detect drift and explain what HCP Terraform adds.
- [ ] I completed Labs 2.1–2.8 including each negative test.
