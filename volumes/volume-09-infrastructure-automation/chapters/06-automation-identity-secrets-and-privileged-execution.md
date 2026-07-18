# Chapter 06: Automation Identity, Secrets, and Privileged Execution

## Learning Objectives

- Distinguish static long-lived credentials from federated, short-lived
  workload identity, and explain why the latter is preferred for
  automation.
- Configure OIDC federation so a CI pipeline authenticates to a cloud
  provider without a stored secret.
- Deploy HashiCorp Vault in dev mode, enable AppRole authentication, and
  issue a dynamic, time-limited secret consumed by Terraform and Ansible.
- Apply `ansible-vault` correctly for content that must ship encrypted
  values inside version control.
- Implement plan/apply credential separation and just-in-time privileged
  execution for infrastructure pipelines.
- Diagnose credential-related pipeline failures: expired tokens, sealed
  vaults, and overly narrow policies.

## Theory and Architecture

Every chapter so far has deferred a question to this one: what actually
authenticates the automation itself? Chapter 02 deferred "prefer
short-lived, federated credentials"; Chapter 03 deferred
`ansible-vault` and external secrets lookups; Chapter 05 built a pipeline
around a plan identity and an apply identity without explaining how either
is issued. This chapter is the mechanics behind all three: how automation
proves who it is, how it obtains secrets it needs at run time, and how
privileged execution is scoped and time-limited rather than standing.

### Identity types in automation

- **Human identity.** An engineer's own account, used interactively
  (`terraform apply` from a workstation during a Chapter 02 lab, or an
  `az login` session). Appropriate for local development and labs, never
  for production pipeline execution.
- **Static service identity.** A dedicated non-human account (`svc_ansible`
  from Chapter 03, an IAM user with an access key) with credentials that
  do not expire on their own. Simpler to reason about but a standing
  target: the credential is valid whether or not automation is actively
  running, and compromise or leakage grants access until someone manually
  rotates or revokes it.
- **Federated / workload identity.** A short-lived credential issued at run
  time, scoped to a single execution, based on a trust relationship between
  the automation platform and the target system rather than a stored
  secret at all. OIDC federation between a CI platform and a cloud
  provider's IAM is the dominant pattern in 2026 for exactly this reason.

The trajectory across an automation practice's maturity is a steady move
away from static service identities and toward federated, short-lived
credentials issued per run — not because static credentials are unusable,
but because every one that exists is a standing secret with its own
rotation burden, blast radius, and audit gap between issuance and use.

### OIDC federation, in detail

OpenID Connect federation lets a CI platform (GitHub Actions, GitLab CI)
present a signed identity token describing the exact workflow run — the
repository, the branch or tag, the environment — to a cloud provider's
identity broker, which exchanges that token for temporary cloud credentials
scoped by a trust policy the cloud account owner controls:

```text
1. CI job starts; CI platform mints a short-lived OIDC token
   describing (repo, ref, environment, workflow).
2. Job presents the token to the cloud provider's identity broker
   (AWS STS AssumeRoleWithWebIdentity, Azure Workload Identity Federation,
   GCP Workload Identity Federation).
3. Broker validates the token's signature against the CI platform's
   published OIDC discovery document, and checks the token's claims
   against the configured trust policy.
4. Broker issues a credential valid for minutes to a few hours, scoped
   to exactly the IAM role the trust policy names.
5. Credential expires automatically; no secret was ever stored.
```

No long-lived secret exists anywhere in this flow — not in the CI
platform's secret store, not in the cloud account. The trust boundary is
entirely the broker's policy, which is why that policy (which repository,
which branch, which environment) must be scoped as tightly as the
role it grants.

### Secrets managers and dynamic secrets

Where automation genuinely needs a secret — a database password, a
third-party API token that has no federation mechanism of its own — a
dedicated secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key
Vault) centralizes storage, access policy, and audit logging, instead of
scattering secrets across `.tfvars` files, CI platform secret stores, and
Ansible variable files with inconsistent access control across each.

Vault's further refinement is the **dynamic secret**: rather than storing
and handing out a static database password, Vault's database secrets
engine creates a brand-new, time-limited database user on demand for each
request, and Vault (or the database) automatically revokes it at expiry.
No password is ever "the" credential to rotate — every consumer gets its
own, and a leaked one expires on its own schedule.

### `ansible-vault` versus an external secrets manager

`ansible-vault` encrypts specific files or in-line values with a symmetric
key, so encrypted content can be committed to version control safely:

```bash
ansible-vault encrypt_string 'S3cr3t-DB-Password!' --name 'db_password'
```

This is appropriate for small teams, air-gapped environments without a
running secrets manager, or values that genuinely belong versioned
alongside the playbook (an encrypted TLS private key used only in a lab).
It does not solve dynamic issuance, per-consumer scoping, or automatic
expiry — the vault-encryption key itself becomes a new static secret that
must be distributed and rotated. For any estate already running Vault or a
cloud secrets manager, prefer an external lookup at run time over
`ansible-vault`-encrypted static content, reserving `ansible-vault` for the
smaller footprint use cases above.

## Design Considerations

### The secret-zero problem

Every secrets manager access chain terminates in some initial credential
that is not, itself, dynamically issued — the "secret zero" that
bootstraps trust. OIDC federation is the preferred answer because it
replaces secret zero with a cryptographic trust relationship (the CI
platform's signed token, verified against its public discovery document)
rather than a stored value at all. Where OIDC federation is unavailable
(an on-premises CI runner with no federation path to Vault), AppRole
authentication's `role_id`/`secret_id` pair is Vault's own answer: the
`role_id` can be treated as semi-public configuration, and the `secret_id`
is provisioned to the CI runner through a narrower, still-privileged
channel (a CI platform's own secret store, or a wrapped single-use
response), keeping the standing secret's scope as small as achievable.

### Scoping credentials to plan versus apply

Chapter 05's pipeline used two separate IAM roles: a read-only plan role
and a write-capable apply role. Design the corresponding Vault or cloud
IAM policies to match that separation explicitly — the plan-stage identity
should be unable to write, full stop, not merely "trusted not to," because
a read-only policy is a technical control that survives a compromised or
buggy plan-stage script, while a discipline of "the plan stage just
doesn't call apply" is not.

### Rotation cadence and blast radius

For any secret that cannot be made fully dynamic (a third-party SaaS API
key with no federation support), define a rotation cadence proportional to
its blast radius: a key that can only read non-sensitive metadata can
rotate quarterly; a key with write access to production billing or DNS
should rotate on a much shorter cycle, and ideally be wrapped behind a
secrets manager even if the manager cannot rotate it automatically — at
minimum centralizing where it lives and who can read it.

### Break-glass access

Federated, just-in-time credentials are, by design, unavailable when the
system issuing them is down (Vault is sealed, the CI platform's OIDC
endpoint is unreachable). A break-glass procedure — a small number of
static, tightly access-controlled, heavily audited credentials, stored
separately from day-to-day automation and used only when the normal
issuance path is provably unavailable — is a deliberate exception to the
"no standing secrets" principle, not a loophole. Break-glass credentials
should be rotated immediately after any use and their use should always
trigger a review.

## Implementation and Automation

### GitHub Actions OIDC to AWS

```hcl
# environments/global/oidc-trust.tf
data "aws_iam_policy_document" "gha_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::111122223333:oidc-provider/token.actions.githubusercontent.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:acme/infra:environment:prod-apply"]
    }
  }
}

resource "aws_iam_role" "terraform_apply" {
  name               = "terraform-apply-write"
  assume_role_policy = data.aws_iam_policy_document.gha_trust.json
}
```

The `sub` claim condition — `repo:acme/infra:environment:prod-apply` — is
the entire trust boundary: only workflow runs from the named repository,
executing against the named GitHub Environment, can assume this role. A
plan-stage role uses the same pattern with a `plan` environment name and a
read-only policy attached instead.

```yaml
# .github/workflows/oidc-plan.yml (excerpt)
permissions:
  id-token: write
  contents: read

jobs:
  plan:
    environment: prod-plan
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/terraform-plan-readonly
          aws-region: us-east-1
```

`permissions: id-token: write` is what allows the job to mint the OIDC
token in the first place; without it, `aws-actions/configure-aws-credentials`
has nothing to exchange.

### Vault in dev mode, AppRole, and a dynamic-feeling KV secret

```bash
vault server -dev -dev-root-token-id="root" &
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="root"

vault secrets enable -path=secret kv-v2
vault kv put secret/pipeline/db_password value="temporary-dev-password"

vault auth enable approle
vault policy write pipeline-read - <<'EOF'
path "secret/data/pipeline/*" {
  capabilities = ["read"]
}
EOF

vault write auth/approle/role/ci-pipeline \
  token_policies="pipeline-read" \
  token_ttl=10m \
  token_max_ttl=30m

vault read auth/approle/role/ci-pipeline/role-id
vault write -f auth/approle/role/ci-pipeline/secret-id
```

The `token_ttl=10m` / `token_max_ttl=30m` pair is what makes this
short-lived in practice: a token issued to a pipeline job expires whether
or not anyone remembers to revoke it, bounding how long a leaked token
remains useful.

### Reading a Vault secret from Terraform

```hcl
terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.4"
    }
  }
}

provider "vault" {
  address = var.vault_address
  # Authentication is supplied out-of-band via VAULT_TOKEN,
  # itself obtained through the AppRole login below — never
  # hardcode a Vault token in configuration.
}

data "vault_kv_secret_v2" "db_password" {
  mount = "secret"
  name  = "pipeline/db_password"
}

output "db_password_length_check" {
  value     = length(data.vault_kv_secret_v2.db_password.data["value"]) > 0
  sensitive = true
}
```

### Reading the same secret from Ansible

```yaml
# playbooks/roles/app_deploy/tasks/main.yml
---
- name: Retrieve database password from Vault
  ansible.builtin.set_fact:
    db_password: "{{ lookup('community.hashi_vault.hashi_vault',
                    'secret=secret/data/pipeline/db_password:value') }}"
  no_log: true
```

`no_log: true` is deliberate and required here: without it, Ansible would
echo the resolved secret value into the task's verbose/debug output, which
frequently ends up captured in CI logs.

### CI login sequence tying it together

```bash
ROLE_ID=$(vault read -field=role_id auth/approle/role/ci-pipeline/role-id)
SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/ci-pipeline/secret-id)

VAULT_TOKEN=$(vault write -field=token auth/approle/login \
  role_id="${ROLE_ID}" secret_id="${SECRET_ID}")

export VAULT_TOKEN
terraform apply -auto-approve
```

In a real pipeline, `SECRET_ID` itself is provisioned to the runner through
the CI platform's own secret store (or a Vault response-wrapped, single-use
token), not printed to a shared terminal as shown here for lab clarity —
this sequence is deliberately spelled out step-by-step for the Hands-On Lab
below, where clarity matters more than production secret hygiene.

## Validation and Troubleshooting

- **`AccessDenied` on `AssumeRoleWithWebIdentity`.** The most common cause
  is a `sub` claim mismatch — confirm the GitHub Environment name in the
  trust policy exactly matches the `environment:` value the workflow job
  actually uses; a typo here fails silently with a generic access-denied
  error, not a claim-mismatch error.
- **Vault returns `permission denied` for a policy that looks correct.**
  Confirm the path in the policy matches the KV engine's actual mount
  path and version — KV v2 requires a `data/` segment in the API path
  (`secret/data/pipeline/*`) that does not appear in the CLI shorthand
  (`secret/pipeline/*`), and mismatching the two is a frequent source of
  "the policy is right but it still fails."
- **Vault is sealed after a restart.** Dev-mode Vault auto-unseals for
  lab convenience; a production Vault cluster does not, and requires an
  unseal operation (or auto-unseal via a cloud KMS) before it will serve
  any request, including reads. Treat "Vault is sealed" as an availability
  incident requiring the documented unseal runbook, not a configuration
  bug to work around.
- **Token expires mid-pipeline-run.** Compare `token_ttl` against the
  pipeline stage's actual duration; a long apply against slow-provisioning
  resources needs a `token_ttl` (or `token_max_ttl`) with headroom, not
  just the shortest value that passed a quick test.
- **Ansible `no_log` accidentally suppresses useful non-secret debugging.**
  Scope `no_log: true` to the specific task handling the secret, not an
  entire play — over-broad `no_log` hides legitimate troubleshooting
  output for unrelated tasks in the same play.

## Security and Best Practices

- Prefer OIDC federation over any stored static cloud credential for CI
  pipelines; if a platform or provider does not yet support it, treat that
  gap as a finding to remediate, not a permanent exception.
- Scope every IAM role and Vault policy to the minimum actions and paths
  the specific pipeline stage needs; a plan-stage role should be
  technically incapable of writing, not merely configured not to.
- Set the shortest `token_ttl`/credential lifetime that comfortably covers
  the stage's real run time, and monitor for tokens issued but never used,
  which usually indicates a scoping or trigger-condition bug.
- Mark every secret-bearing variable and task `sensitive`/`no_log` in
  Terraform and Ansible respectively, and audit CI logs periodically for
  accidental secret leakage regardless.
- Rotate any secret that cannot be made dynamic on a cadence proportional
  to its blast radius, and treat unrotated long-lived keys as technical
  debt with an owner and a date, not a permanent state.
- Restrict, document, and audit break-glass credential use; rotate
  immediately after every use.

## References and Knowledge Checks

### References

- HashiCorp, *Vault AppRole Auth Method* —
  <https://developer.hashicorp.com/vault/docs/auth/approle>
- HashiCorp, *Vault KV Secrets Engine v2* —
  <https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2>
- GitHub, *About Security Hardening with OpenID Connect* —
  <https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect>
- Red Hat, *`community.hashi_vault` Collection Documentation* —
  <https://docs.ansible.com/ansible/latest/collections/community/hashi_vault/>

### Knowledge Checks

1. What is "secret zero," and how does OIDC federation change what secret
   zero actually is?
2. Why is a Vault dynamic database credential a stronger control than a
   static password stored in a secrets manager?
3. What specific claim in a GitHub Actions OIDC token is the trust
   boundary in an AWS IAM role's assume-role policy, and what happens if
   it is scoped too broadly?
4. Why is `ansible-vault` alone insufficient for dynamic, per-consumer
   secret issuance, even though it solves safe storage in version control?
5. What is a break-glass credential, and what two things should always
   happen after one is used?

## Hands-On Lab

### Objective

Run Vault in dev mode, configure AppRole authentication with a scoped
read-only policy, issue a short-lived token, and use it to read a secret
from both a CLI login flow and an Ansible lookup — then prove the policy
boundary by attempting a write with the same token.

### Prerequisites

- Vault binary installed locally (`brew install vault` or download from
  HashiCorp's releases page); `vault version` succeeds.
- Python 3.10+, `pip install "ansible-core==2.17.*" ansible-hashi-vault`
  (installs the `community.hashi_vault` collection's Python dependencies).
- `ansible-galaxy collection install community.hashi_vault`.
- No cloud account required — Vault dev mode runs entirely locally.

### Steps

1. Start Vault in dev mode in one terminal and leave it running:

   ```bash
   vault server -dev -dev-root-token-id="root"
   ```

2. In a second terminal, configure the CLI and seed a secret:

   ```bash
   export VAULT_ADDR="http://127.0.0.1:8200"
   export VAULT_TOKEN="root"

   vault secrets enable -path=secret kv-v2
   vault kv put secret/pipeline/db_password value="lab-password-123"
   ```

3. Enable AppRole and create a read-only policy and role:

   ```bash
   vault auth enable approle

   cat > /tmp/pipeline-read.hcl <<'EOF'
   path "secret/data/pipeline/*" {
     capabilities = ["read"]
   }
   EOF
   vault policy write pipeline-read /tmp/pipeline-read.hcl

   vault write auth/approle/role/ci-pipeline \
     token_policies="pipeline-read" \
     token_ttl=10m \
     token_max_ttl=30m
   ```

4. Retrieve the `role_id` and generate a `secret_id`, then log in:

   ```bash
   ROLE_ID=$(vault read -field=role_id auth/approle/role/ci-pipeline/role-id)
   SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/ci-pipeline/secret-id)

   CI_TOKEN=$(vault write -field=token auth/approle/login \
     role_id="${ROLE_ID}" secret_id="${SECRET_ID}")

   echo "Issued token: ${CI_TOKEN}"
   ```

5. Use the scoped token to read the secret directly:

   ```bash
   VAULT_TOKEN="${CI_TOKEN}" vault kv get secret/pipeline/db_password
   ```

6. Use the same token from an Ansible lookup:

   ```bash
   mkdir -p vault-lab && cd vault-lab
   cat > read_secret.yml <<'EOF'
   ---
   - name: Read a secret via community.hashi_vault
     hosts: localhost
     connection: local
     gather_facts: false
     tasks:
       - name: Look up the database password
         ansible.builtin.set_fact:
           db_password: "{{ lookup('community.hashi_vault.hashi_vault',
                           'secret=secret/data/pipeline/db_password:value') }}"
         no_log: true

       - name: Confirm a non-empty value was retrieved (without printing it)
         ansible.builtin.assert:
           that:
             - db_password | length > 0
   EOF

   VAULT_ADDR="http://127.0.0.1:8200" VAULT_TOKEN="${CI_TOKEN}" \
     ansible-playbook read_secret.yml
   ```

### Expected Results

- Step 5 prints the `value` key with `lab-password-123`.
- Step 6's `ansible-playbook` run reports `ok=2` with the assertion task
  passing, and the actual secret value never appears in the task output
  because of `no_log: true`.

### Negative Test

Attempt a write with the same scoped token, which the `pipeline-read`
policy does not grant:

```bash
VAULT_TOKEN="${CI_TOKEN}" vault kv put secret/pipeline/db_password value="should-fail"
```

Confirm this returns `Error writing data to secret/data/pipeline/db_password:
... permission denied` — proving the read-only policy is enforced by
Vault itself, not merely by convention, exactly as Design Considerations
argued a plan-stage credential should behave.

### Cleanup

```bash
cd .. && rm -rf vault-lab
# In the terminal running Vault dev mode, press Ctrl+C to stop it.
# Dev-mode Vault is entirely in-memory; no persistent state remains.
```

## Summary and Completion Checklist

Automation identity has a clear direction of travel: away from static,
standing credentials and toward federated, short-lived, narrowly scoped
identity issued at run time — OIDC federation for CI-to-cloud
authentication, and Vault's AppRole and dynamic secrets engines for
everything else automation needs to read. `ansible-vault` remains useful
for small-footprint, version-controlled encrypted content, but is not a
substitute for centralized, policy-enforced, audited secret issuance at
any real scale. The plan/apply credential separation from Chapter 05 is
only a real control once the underlying identities are actually distinct
and actually least-privileged, which is what this chapter's OIDC trust
policy and Vault AppRole policy both enforce technically rather than by
convention.

- [ ] Can explain why federated, short-lived credentials are preferred
      over static service-account credentials for CI pipelines.
- [ ] Has configured (or can describe configuring) OIDC federation between
      a CI platform and a cloud IAM role.
- [ ] Has run Vault in dev mode, created an AppRole with a scoped policy,
      and retrieved a secret using an issued token.
- [ ] Has read a Vault secret from an Ansible playbook using `no_log` to
      suppress it from output.
- [ ] Can explain the secret-zero problem and how OIDC federation and
      break-glass access each relate to it.
