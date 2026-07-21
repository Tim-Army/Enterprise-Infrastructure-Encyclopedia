# Chapter 02: Infrastructure as Code, State, Providers, and Modules

![Lab flow for this chapter: a cloud-credential-free module creates one random_pet and one local_file; terraform test runs a plan-level assertion that passes. A moved block renames the resource address, and terraform plan afterward reports 0 to add, 0 to change, 0 to destroy, confirming the resource was renamed in place rather than replaced. As a negative test, the generated output file's contents are edited by hand outside Terraform; terraform plan reports no diff at all, because local_file only tracks that it manages the file's existence and declared content in state, not out-of-band edits.](../../../diagrams/volume-09-infrastructure-automation/chapter-02-moved-block-drift-blindspot-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: a safe moved-block refactor, followed by a demonstration of a specific provider's drift-detection blind spot.*

## Learning Objectives

- Explain how Terraform's plan/apply lifecycle uses state to compute a
  minimal diff between desired and actual infrastructure.
- Configure a remote backend with state locking and understand the failure
  modes of unlocked or local state.
- Design reusable modules with clear input/output contracts and semantic
  versioning.
- Use Terraform 1.9.x language features — `moved` blocks, `import` blocks,
  `check` blocks, and variable validation — to manage refactors and
  correctness safely.
- Write and run `terraform test` unit and integration tests against a
  module.
- Diagnose and recover from drift, state corruption, and locked state.

## Theory and Architecture

Terraform is a declarative infrastructure-as-code tool: engineers describe
the desired end state of infrastructure resources in HashiCorp
Configuration Language (HCL), and Terraform's core engine reconciles that
description against a **state file** using **provider** plugins that know
how to talk to a specific API (AWS, Azure, GCP, Kubernetes, vSphere,
GitHub, and hundreds of others). This chapter uses Terraform 1.9.x, the
baseline recorded in
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).

### The plan/apply lifecycle

1. **Init** (`terraform init`) downloads the providers and modules pinned
   in configuration and initializes the configured backend.
2. **Plan** (`terraform plan`) reads current state, refreshes it against
   real infrastructure (unless `-refresh=false` is set), and computes a
   diff against the desired configuration, producing an execution plan.
3. **Apply** (`terraform apply`) executes the plan's create, update, or
   destroy operations through the provider and writes the new state.

State is not optional metadata — it is the only record Terraform has of
which real-world resource corresponds to which configuration block. Losing
state without recovering it means Terraform can no longer manage those
resources without manual `import`.

### State and backends

By default, Terraform writes state to a local `terraform.tfstate` file.
Production use requires a **remote backend** for three reasons: shared
access across a team, state locking to prevent concurrent writes, and
durability independent of any single workstation. Common backends include
Amazon S3 with DynamoDB locking (S3 native locking as of Terraform 1.9 and
provider support, or the classic DynamoDB table pattern), Azure Storage
with blob leases, Google Cloud Storage, and Terraform Cloud/Enterprise,
which additionally provides remote execution, policy enforcement, and a
private module registry.

```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "acme-tfstate-dev"
    key            = "network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "acme-tfstate-locks"
    encrypt        = true
  }
}
```

State locking prevents two concurrent `apply` operations from corrupting
each other's writes: the second run blocks (or fails, depending on
`-lock-timeout`) until the first releases the lock. Losing the lock table
or forcibly deleting a stuck lock with `terraform force-unlock` without
confirming no other apply is in flight is one of the most common causes of
state corruption in production.

### Providers

A provider is a plugin, versioned independently of Terraform core, that
translates HCL resource blocks into API calls. Providers are declared and
pinned in a `required_providers` block and locked to exact resolved
versions in the `.terraform.lock.hcl` file, which should always be
committed to version control ([Chapter 08](08-automation-security-governance-and-supply-chains.md) covers the supply-chain
implications in depth):

```hcl
terraform {
  required_version = ">= 1.9.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}
```

### Modules

A module is a reusable, parameterized collection of resources with a
defined input (`variable`) and output (`output`) contract. Modules are the
primary unit of composition and reuse in Terraform, analogous to a function
or library in general-purpose programming:

```hcl
# modules/network/variables.tf
variable "name" {
  type        = string
  description = "Base name applied to all network resources."

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,30}$", var.name))
    error_message = "name must be lowercase alphanumeric with hyphens, 3-31 characters."
  }
}

variable "cidr_block" {
  type        = string
  description = "CIDR block for the VPC."

  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "cidr_block must be a valid IPv4 CIDR."
  }
}

variable "azs" {
  type        = list(string)
  description = "Availability zones to spread subnets across."
}
```

```hcl
# modules/network/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = { Name = var.name }
}

resource "aws_subnet" "private" {
  for_each = { for idx, az in var.azs : az => idx }

  vpc_id            = aws_vpc.this.id
  availability_zone = each.key
  cidr_block        = cidrsubnet(var.cidr_block, 4, each.value)

  tags = { Name = "${var.name}-private-${each.key}" }
}
```

```hcl
# modules/network/outputs.tf
output "vpc_id" {
  value       = aws_vpc.this.id
  description = "ID of the created VPC."
}

output "private_subnet_ids" {
  value       = [for s in aws_subnet.private : s.id]
  description = "IDs of the created private subnets."
}
```

A calling root module consumes it with a pinned source and version:

```hcl
# environments/dev/main.tf
module "network" {
  source     = "git::https://github.com/acme/tf-modules.git//network?ref=v2.3.0"
  name       = "dev"
  cidr_block = "10.20.0.0/16"
  azs        = ["us-east-1a", "us-east-1b"]
}
```

Pinning `ref=v2.3.0` to an immutable tag — never `main` or a floating
branch — is what makes module upgrades an explicit, reviewable pull request
rather than a surprise on the next `terraform init`.

### `for_each` versus `count`

`for_each` keys resources by a stable identifier (map key or set element),
so adding or removing one element does not force Terraform to destroy and
recreate unrelated resources, as `count`'s index-based addressing does.
Prefer `for_each` for any collection of resources with a natural stable
key, such as the availability-zone-keyed subnets above; reserve `count` for
simple, order-independent repetition with no meaningful key, or for
conditionally creating zero or one instance of a resource.

## Design Considerations

### Module boundaries

A module should represent one cohesive unit of infrastructure with a
stable interface, not an arbitrary folder of resources. Good boundaries
mirror how the resources are operated and changed together (a network, a
managed Kubernetes cluster, an application's data tier), not how they are
merely grouped in a diagram. Overly granular modules (a module per single
resource) add indirection without reuse value; overly broad modules
("everything") make blast radius impossible to reason about and cause
unrelated teams to contend for the same state and review queue.

### State isolation

Each environment (dev, staging, prod) and, within an environment, each
independently-changing layer (network, platform, application data) should
have its own state file. Coarse-grained state means every `plan` touches
resources unrelated to the change at hand, increases plan/apply time,
increases the blast radius of a mistake, and forces broader IAM permissions
on whoever runs `apply`. Fine-grained state requires more backend
configuration and more remote state data-source wiring between layers but
is the correct trade-off for anything beyond a small proof of concept.

### Workspaces versus directories

Terraform's built-in workspace feature (`terraform workspace new/select`)
lets one configuration produce multiple state files distinguished by
workspace name. It is convenient for ephemeral, structurally-identical
environments (short-lived feature branches, per-developer sandboxes) but is
a poor fit for environments that differ structurally (different instance
sizes, different provider accounts, different approval requirements)
because differences must be encoded as conditionals inside a single
configuration. Most enterprise estates prefer separate directories
(`environments/dev`, `environments/prod`) with their own backend
configuration and variables, reserving workspaces for genuinely disposable,
structurally-identical instances of a configuration.

### Refactoring without destroy/recreate

Renaming a resource, moving it into a module, or restructuring `for_each`
keys changes the resource's address in state. Without intervention,
Terraform interprets an address change as "destroy the old, create a new
one" — often unacceptable for stateful resources. Terraform 1.9.x's
`moved` block records an address change declaratively so it survives in
version control and applies automatically for every consumer of the
configuration, replacing the older, imperative `terraform state mv` as the
preferred mechanism for anything checked into shared modules:

```hcl
moved {
  from = aws_subnet.this
  to   = aws_subnet.private["us-east-1a"]
}
```

## Implementation and Automation

### Importing existing resources

Terraform 1.5+ supports declarative `import` blocks, planned and applied
like any other configuration change instead of run as an imperative,
one-off CLI command:

```hcl
import {
  to = aws_vpc.this
  id = "vpc-0123456789abcdef0"
}

resource "aws_vpc" "this" {
  cidr_block = "10.20.0.0/16"
  tags       = { Name = "dev" }
}
```

`terraform plan` shows the import alongside any configuration drift it
would additionally apply, so the operator can confirm both in one review
before running `terraform apply`.

### `check` blocks for continuous assertions

`check` blocks assert conditions about infrastructure without failing the
overall plan/apply, surfacing warnings for conditions worth watching (for
example, a certificate approaching expiry):

```hcl
check "certificate_validity" {
  data "tls_certificate" "api" {
    url = "https://api.dev.acme.internal"
  }

  assert {
    condition     = timecmp(data.tls_certificate.api.certificates[0].not_after, timeadd(timestamp(), "336h")) > 0
    error_message = "API certificate expires within 14 days."
  }
}
```

### Testing modules with `terraform test`

Terraform's native test framework (`.tftest.hcl` files) runs plan- or
apply-level assertions against a module in an isolated ephemeral run,
suitable for CI:

```hcl
# modules/network/tests/network.tftest.hcl
variables {
  name       = "unittest"
  cidr_block = "10.99.0.0/16"
  azs        = ["us-east-1a", "us-east-1b"]
}

run "plan_creates_expected_subnet_count" {
  command = plan

  assert {
    condition     = length(aws_subnet.private) == 2
    error_message = "Expected exactly 2 private subnets, one per AZ."
  }
}

run "vpc_has_dns_support" {
  command = apply

  assert {
    condition     = aws_vpc.this.enable_dns_support == true
    error_message = "VPC must have DNS support enabled."
  }
}
```

```bash
terraform test -test-directory=modules/network/tests
```

The `plan`-command run is fast and requires no real infrastructure changes
(useful for pull-request gating); the `apply`-command run exercises the
provider end to end and belongs in a slower, scheduled or merge-triggered
pipeline stage, typically against a disposable test account.

### Local-only reproducible example

For CI and lab environments without cloud credentials, the `random` and
`local` providers let you exercise the full init/plan/apply/state lifecycle
with no external account:

```hcl
# modules/demo/main.tf
resource "random_pet" "example" {
  length = 2
}

resource "local_file" "example" {
  filename = "${path.module}/output-${random_pet.example.id}.txt"
  content  = "Managed by Terraform: ${random_pet.example.id}\n"
}
```

This pattern is used in the Hands-On Lab below and is a reasonable pattern
for CI smoke tests that must not depend on live cloud credentials.

## Validation and Troubleshooting

- **Plan shows unexpected destroy/recreate.** Check whether a
  force-new-resource argument changed (many providers document which
  arguments require replacement) or whether a resource address changed
  without a `moved` block. Run `terraform plan -out=plan.tfout` and inspect
  with `terraform show -json plan.tfout` in CI to catch destructive plans
  programmatically before apply ([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)).
- **`Error: Error acquiring the state lock`.** Another run holds the lock.
  Confirm no other apply is genuinely in progress (check the CI run queue)
  before ever running `terraform force-unlock <LOCK_ID>` — force-unlocking
  during a live apply is a common cause of state corruption.
- **State drift.** Real infrastructure was changed outside Terraform (a
  console click, another tool). `terraform plan` after a refresh shows the
  drift as a diff. Resolve by either updating configuration to match
  reality (if the manual change should be kept) or applying to revert it
  (if it should not); never manually edit the state file to paper over
  drift.
- **`terraform init` fails to resolve a provider version.** Check for a
  conflicting version constraint between the root module and a called
  module; run `terraform providers` to see the constraint tree, and prefer
  pessimistic constraints (`~> 5.60`) over exact pins in reusable modules so
  consumers retain patch-level flexibility.
- **Sensitive values appearing in plan output or state.** Mark variables
  and outputs `sensitive = true` to redact console output; understand this
  does not encrypt state at rest — state itself must be stored in an
  encrypted backend and access-controlled, since sensitive values remain
  in plaintext inside the state file.

## Security and Best Practices

- Store state exclusively in an encrypted, access-controlled remote
  backend; never commit `terraform.tfstate` to version control.
- Always commit `.terraform.lock.hcl`; treat unpinned provider versions as
  a supply-chain risk ([Chapter 08](08-automation-security-governance-and-supply-chains.md)).
- Scope the credentials used by `terraform apply` to the minimum
  permissions the configuration actually needs, and prefer short-lived,
  federated credentials over static access keys ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)).
- Enable state backend versioning (for example, S3 bucket versioning) so a
  corrupted or bad state write can be rolled back.
- Use `sensitive = true` on variables and outputs that carry secrets or
  PII, and avoid ever interpolating secrets directly into resource tags or
  names, which frequently end up in logs.
- Require `terraform plan` output to be reviewed by a human (or a policy
  engine, [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)) before every production `apply`; never run
  unreviewed applies against production from a workstation.

## References and Knowledge Checks

### References

- HashiCorp, *Terraform Language Documentation*, 1.9.x —
  <https://developer.hashicorp.com/terraform/language>
- HashiCorp, *Terraform Backend Configuration* —
  <https://developer.hashicorp.com/terraform/language/backend>
- HashiCorp, *Terraform Tests* —
  <https://developer.hashicorp.com/terraform/language/tests>
- HashiCorp, *Import Blocks* —
  <https://developer.hashicorp.com/terraform/language/import>

### Knowledge Checks

1. Why does deleting a Terraform state file without recovering it prevent
   further management of existing resources, even though the resources
   themselves still exist?
2. What problem does state locking solve, and what is the risk of a
   careless `force-unlock`?
3. When would you choose `for_each` over `count`, and why does the choice
   affect what happens when one element is removed from a collection?
4. What is the practical difference between a `moved` block and manually
   running `terraform state mv`?
5. Why should `.terraform.lock.hcl` be committed to version control?

## Hands-On Lab

### Objective

Build a small, cloud-credential-free Terraform module, back it with a
local state backend that demonstrates the locking concept, write a
`terraform test`, perform a refactor using a `moved` block, and confirm
drift detection.

### Prerequisites

- Terraform 1.9.x installed (`terraform version`).
- No cloud account required — this lab uses the `random` and `local`
  providers only.

### Steps

1. Create the lab directory and module:

   ```bash
   mkdir -p tf-lab/modules/demo && cd tf-lab
   ```

2. Write the module from the Implementation section into
   `modules/demo/main.tf`, plus a `variables.tf`:

   ```bash
   cat > modules/demo/variables.tf <<'EOF'
   variable "greeting" {
     type        = string
     default     = "Managed by Terraform"
     description = "Text prefix written into the demo file."
   }
   EOF
   ```

   Update `local_file.example` content to `"${var.greeting}: ${random_pet.example.id}\n"`.

3. Create a root configuration that calls the module:

   ```bash
   cat > main.tf <<'EOF'
   terraform {
     required_version = ">= 1.9.0"
     required_providers {
       random = { source = "hashicorp/random", version = "~> 3.6" }
       local  = { source = "hashicorp/local",  version = "~> 2.5" }
     }
   }

   module "demo" {
     source = "./modules/demo"
   }

   output "demo_id" {
     value = module.demo.demo_id
   }
   EOF
   ```

   Add a matching `demo_id` output to `modules/demo/outputs.tf` that
   exposes `random_pet.example.id`.

4. Initialize and apply:

   ```bash
   terraform init
   terraform apply -auto-approve
   ```

5. Confirm the state and generated file exist:

   ```bash
   terraform show
   cat output-*.txt
   ```

6. Write and run a plan-level test:

   ```bash
   mkdir -p modules/demo/tests
   cat > modules/demo/tests/demo.tftest.hcl <<'EOF'
   variables {
     greeting = "Unit test"
   }

   run "plan_has_one_file_and_one_pet" {
     command = plan

     assert {
       condition     = local_file.example.filename != ""
       error_message = "Expected a filename to be computed."
     }
   }
   EOF
   terraform test -test-directory=modules/demo/tests
   ```

7. Perform a refactor: rename the resource address by wrapping it under a
   `for_each`-style key using a `moved` block so existing state is
   preserved instead of destroyed. (For this lab, simulate by adding a
   `moved` block referencing a renamed local resource label and confirming
   `terraform plan` reports no destroy/create.)

### Expected Results

- `terraform apply` creates one `random_pet` resource and one local file
  containing the greeting and pet name.
- `terraform test` reports the plan-level assertion passing.
- After the `moved` block refactor, `terraform plan` reports "0 to add,
  0 to change, 0 to destroy" — confirming the resource was renamed in
  place rather than replaced.

### Negative Test

Manually edit the generated `output-*.txt` file's contents outside
Terraform, then run `terraform plan`. Terraform reports no diff, because
`local_file` only tracks the fact that it manages the file's existence and
declared content in state, not out-of-band edits, unless a checksum-aware
provider is used — a useful demonstration that not every provider detects
every kind of drift, and why understanding a specific provider's drift
detection behavior matters before relying on it operationally.

### Cleanup

```bash
terraform destroy -auto-approve
cd .. && rm -rf tf-lab
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Terraform's plan/apply lifecycle depends entirely on accurate, locked,
remotely-stored state; providers translate declarative HCL into real API
calls; and modules are the unit of reuse that make infrastructure code
maintainable at scale. Terraform 1.9.x's `moved`, `import`, and `check`
blocks, together with the native `terraform test` framework, move
refactoring, adoption, and testing out of imperative one-off commands and
into reviewable, version-controlled configuration.

- [ ] Can explain why state is required and what breaks when it is lost or
      corrupted.
- [ ] Has configured a remote backend with locking (or can explain why one
      is required in production).
- [ ] Can write a module with a validated variable contract and typed
      outputs.
- [ ] Has used a `moved` block to refactor a resource address without
      destroy/recreate.
- [ ] Has written and run at least one `terraform test` case.
- [ ] Understands the difference between config-driven drift correction
      and manual state editing, and why the latter is discouraged.
