# Chapter 06: Infrastructure as Code and Automated Delivery Lab

![Lab flow for this chapter: a secrets manager centralizes the DHCP failover secret and both IPsec pre-shared keys; Terraform imports the existing cloud landing zone and HQ vSphere cluster with a clean plan, and the earlier chapter's manual DHCP configuration converts to an idempotent Ansible playbook whose second run reports zero changed tasks. A compliant pull request adding a resource tag runs plan, passes the policy gate, and applies only after merge and approval. As a negative test, a second pull request introduces a security group rule permitting SSH from anywhere; the policy gate reports the specific deny message and the pipeline blocks the apply stage from running, confirmed in the pipeline UI itself, not just local output.](../../../diagrams/volume-13-integrated-enterprise-labs/chapter-06-iac-policy-gate-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: Terraform, Ansible, and centralized secrets brought under a CI pipeline with a policy gate, tested against a policy-violating pull request.*

## Learning Objectives

- Convert the manually built `CLOUD1` landing zone and vSphere inventory
  from Chapters 04–05 into Terraform-managed state without recreating any
  resource.
- Convert the manual host configuration from [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) into idempotent
  Ansible playbooks, and prove re-running them changes nothing.
- Build a pipeline with a policy gate that blocks a non-compliant change
  before it reaches `apply`, using a less-privileged identity for `plan`
  than for `apply`.
- Manage every credential this volume has accumulated so far — DHCP
  failover secret, IPsec pre-shared keys, cloud credentials — in a
  dedicated secrets manager instead of scattered configuration files.
- Diagnose a failed policy gate from its output alone, without needing to
  re-read the entire pipeline log.

## Theory and Architecture

Every chapter so far has deliberately used manual, CLI-driven steps —
[Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) said as much, so the reader understands exactly what this
chapter's automation replaces. This chapter converts that manual history
into code, following [Volume IX](../../volume-09-infrastructure-automation/README.md) (Infrastructure Automation): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)
(Infrastructure as Code, State, Providers, and Modules) for bringing the
`CLOUD1` VPC and vSphere inventory under Terraform management, [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)
(Configuration Management and Desired-State Convergence) for turning
[Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)'s manual AD/DNS/DHCP steps into Ansible playbooks, [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md)
(Automation Pipelines, Testing, and Policy Gates) for the CI pipeline and
its policy gate, and Chapter 06 (Automation Identity, Secrets, and
Privileged Execution) for centralizing every secret this volume has
accumulated into one managed store.

The plan/apply separation this chapter implements is the practical
application of the principle [Volume I, Chapter 03](../../volume-01-enterprise-engineering-foundations/chapters/03-automation-architecture.md) (Automation Architecture)
introduced abstractly: a `plan` identity that can read and diff but not
write, and a separate, more privileged `apply` identity gated behind human
approval. [Volume IX, Chapter 08](../../volume-09-infrastructure-automation/chapters/08-automation-security-governance-and-supply-chains.md) (Automation Security, Governance, and
Supply Chains) frames why this matters beyond convenience — an automation
identity with unchecked apply rights is one compromised pipeline away from
being a domain administrator equivalent across every system this volume
has built.

Two artifacts this chapter produces are meant to outlive this chapter: the
Terraform/Ansible codebase itself, and a working policy gate. [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md)'s
capstone decommissioning exercise runs largely through this chapter's
automation rather than the manual commands used to build the environment,
so a gap here becomes a gap in that chapter too.

### Systems introduced in this chapter

| Hostname | Role | Address |
| --- | --- | --- |
| `git01` | Self-hosted Git service with CI runner | `10.13.10.31` |
| `vault01` | Secrets manager | `10.13.10.32` |

`ctrl01` (`10.13.10.30`) becomes the Terraform/Ansible execution host that
`git01`'s CI pipeline drives remotely, rather than a host an engineer logs
into to run commands by hand.

## Design Considerations

- **Import existing resources instead of rebuilding.** `terraform import`
  brings the `CLOUD1` VPC, subnet, and VPN gateway from [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md), and the
  vSphere cluster/VM inventory from [Chapter 04](04-virtualization-storage-and-data-protection-lab.md), under management without
  destroying and recreating them — the realistic path for automating an
  already-running environment, and a deliberately different exercise than
  greenfield IaC.
- **Split declarative and imperative automation by what they are good
  at.** Terraform manages resource existence and topology (VPCs, VMs,
  security policy objects); Ansible manages configuration state inside
  already-existing hosts (DNS forwarders, DHCP scopes, package state) —
  the same division [Volume IX, Chapter 02](../../volume-09-infrastructure-automation/chapters/02-infrastructure-as-code-state-providers-and-modules.md) draws between provisioning and
  configuration concerns.
- **Policy as code, enforced before apply, not after.** Compliance checks
  (mandatory tags, no `0.0.0.0/0` ingress rules, encrypted state backend)
  run as an automated gate in the pipeline's `plan` stage. [Volume IX](../../volume-09-infrastructure-automation/README.md),
  [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md) treats a policy check that only runs after resources already
  exist as a compliance report, not a control — this chapter builds a
  control.
- **Centralized secrets, referenced not copied.** Every secret this volume
  has generated so far (the [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) DHCP failover key, the [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)
  IPsec pre-shared keys, cloud credentials from [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md)) moves into
  `vault01`, retrieved at runtime by automation rather than stored in
  version-controlled files — closing the exact gap [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s Security
  and Best Practices section flagged as a dependency of this chapter.
- **OIDC federation for the apply identity, not a stored long-lived
  credential.** The CI runner exchanges a short-lived, pipeline-scoped
  identity token for cloud and vSphere credentials at apply time,
  eliminating a standing credential an attacker could steal from the CI
  system at rest — directly reusing the pattern from [Volume I, Chapter 03](../../volume-01-enterprise-engineering-foundations/chapters/03-automation-architecture.md).

## Implementation and Automation

Import the existing `CLOUD1` VPC and the HQ vSphere cluster into Terraform
state:

```bash
terraform import aws_vpc.cloud1 <vpc-id>
terraform import vsphere_compute_cluster.hq_cluster \
  '/HQ/host/HQ-Cluster'
```

Define the policy gate as an OPA/Conftest rule evaluated against every
Terraform plan:

```rego
package terraform.policy

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  resource.change.after.from_port <= 22
  resource.change.after.to_port >= 22
  msg := sprintf("SSH exposed to 0.0.0.0/0 in %s", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  not resource.change.after.tags.owner
  msg := sprintf("missing required 'owner' tag on %s", [resource.address])
}
```

Wire the pipeline stages so `plan` runs on every pull request with a
read-only identity, and `apply` runs only after merge, using a separate,
more privileged identity obtained through OIDC:

```yaml
# .ci/pipeline.yml (excerpt)
stages:
  - plan:
      identity: ci-plan-readonly
      run:
        - terraform plan -out=tfplan
        - conftest test tfplan.json --policy policy/
  - apply:
      identity: ci-apply-oidc   # exchanged at runtime, never stored
      when: merged_to_main
      requires_approval: true
      run:
        - terraform apply tfplan
```

Convert [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)'s manual DHCP scope configuration into an idempotent
Ansible playbook:

```yaml
- name: Configure VLAN120 DHCP scope and failover
  hosts: dc01
  tasks:
    - name: Ensure DHCP scope exists
      win_dhcp_scope:
        name: VLAN120-User
        state: present
        start_range: 10.13.20.50
        end_range: 10.13.20.200
        subnet_mask: 255.255.255.0
    - name: Ensure failover relationship exists
      win_dhcp_failover:
        name: dc01-dc02-vlan120
        partner_server: dc02.corp.meridian.example
        scope_id: 10.13.20.0
        load_balance_percent: 50
        shared_secret: "{{ vault_dhcp_failover_secret }}"
```

Retrieve the failover secret from Vault at run time rather than storing it
in the playbook or its variable files:

```bash
export VAULT_ADDR="https://vault01.corp.meridian.example:8200"
vault kv get -field=secret meridian/dhcp/failover
```

## Validation and Troubleshooting

- **Terraform plan produces no unexpected diff after import.** Immediately
  after `terraform import`, `terraform plan` should show no changes (or
  only cosmetic ones you explicitly reconcile) — a large diff means the
  Terraform resource definition does not actually match the imported
  resource's real configuration, and applying it would silently change
  production-equivalent infrastructure.
- **Playbook idempotency.** A second, back-to-back run of the DHCP
  playbook must report zero changed tasks — the end state is the same
  after the first run as it is after the second and every intervening
  run, the definition of idempotency from [Volume I, Chapter 01](../../volume-01-enterprise-engineering-foundations/chapters/01-building-the-enterprise-developer-workstation.md), now
  proven rather than assumed.
- **Policy gate failure is readable on its own.** A blocked pipeline run
  must show the Conftest `deny` message directly in the pipeline output;
  if diagnosing a policy failure requires opening the raw Terraform plan
  JSON, the policy message needs to be more specific, not the engineer
  more patient.
- **Common failure: OIDC trust misconfiguration.** If the `apply` stage
  fails with an authentication error despite a clean `plan`, check the
  federated identity's trust policy (issuer, audience, subject claim
  matching the pipeline's actual repository and branch) before assuming
  the credentials themselves are wrong.
- **Common failure: Vault seal state.** If a playbook run fails to
  retrieve a secret with a connection-refused or sealed-vault error, check
  `vault status` first — a restarted `vault01` returns to a sealed state
  by default and requires an unseal operation before it serves any
  secret.

## Security and Best Practices

- Never commit an unseal key, root token, or any secret's plaintext value
  to `~/vol13-lab`'s Git history — even in a disposable lab, this chapter
  is where the habit either forms correctly or does not.
- Scope the `ci-plan-readonly` identity so it cannot modify any resource,
  even accidentally; a `plan`-stage identity with write access defeats the
  entire purpose of the separation.
- Require pipeline approval from a human other than the change's author
  before `apply` runs against anything beyond the lab's own scope — a
  one-person-approves-their-own-change pipeline is not a control.
- Protect the branch the pipeline treats as authoritative so every change
  arrives as a reviewed pull request rather than a direct push, consistent
  with the branch protection practices in [Volume I, Chapter 02](../../volume-01-enterprise-engineering-foundations/chapters/02-repository-architecture.md).
- Rotate the Vault root token generated during initialization and store
  the unseal keys split across more than one location, mirroring the
  key-custody discipline a production secrets manager requires.
- Scan every Terraform module and Ansible role for known-vulnerable
  provider/collection versions as part of the pipeline, consistent with
  the supply-chain practices in [Volume IX, Chapter 08](../../volume-09-infrastructure-automation/chapters/08-automation-security-governance-and-supply-chains.md).

## References and Knowledge Checks

**References**

- [Volume I, Chapter 03](../../volume-01-enterprise-engineering-foundations/chapters/03-automation-architecture.md) — Automation Architecture (plan/apply separation,
  OIDC federation).
- [Volume IX](../../volume-09-infrastructure-automation/README.md), Chapters 02–03 and 05–06, 08 — IaC/state/providers,
  configuration management, pipelines/policy gates, automation
  identity/secrets, and automation security/governance.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Terraform 1.9.x
  and Ansible core 2.17/ansible 10.x baseline used in this chapter.

**Knowledge checks**

1. Why does `terraform import` followed by an unexpected plan diff
   indicate a problem with the Terraform definition rather than with the
   imported resource?
2. What specific risk does OIDC federation for the `apply` identity
   eliminate that a long-lived stored credential would not?
3. Why is a policy gate that runs after resources are created a report
   rather than a control?
4. Name two secrets generated in earlier chapters that this chapter
   centralizes into `vault01`, and the risk of leaving them where they
   were.

## Hands-On Lab

**Objective:** Bring the `CLOUD1` landing zone and HQ vSphere inventory
under Terraform management, convert [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)'s manual DHCP configuration
into an idempotent Ansible playbook, centralize this volume's secrets into
Vault, and prove the pipeline's policy gate blocks a non-compliant change.

**Prerequisites**

- [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md) complete, with the hybrid Kubernetes cluster and `CLOUD1`
  landing zone healthy.
- Terraform 1.9.x, Ansible core 2.17, and a Vault-compatible secrets
  manager installed on or reachable from `ctrl01`.
- Familiarity with Git-based pipelines at the level of [Volume I](../../volume-01-enterprise-engineering-foundations/README.md), Chapter
  04 (GitHub Project and Workflow Management).

**Steps**

1. Restore or confirm the `ch05-baseline` state.

2. Provision `git01` and `vault01` per the addressing table above. Deploy
   Vault, initialize it, and record the unseal keys and root token in a
   physically separate location from the lab notes (not in this
   repository, which stores no reader lab state).

3. Migrate the DHCP failover secret and both IPsec pre-shared keys from
   Chapters 02–03 into Vault:

   ```bash
   ./evidence.sh "vault kv put meridian/dhcp/failover secret='<value>'"
   ./evidence.sh "vault kv put meridian/wan/ipsec-br1 psk='<value>'"
   ./evidence.sh "vault kv put meridian/wan/ipsec-cloud1 psk='<value>'"
   ```

4. Initialize a Terraform working directory on `ctrl01`, define the
   `CLOUD1` VPC and HQ vSphere cluster as resources, and import the
   existing objects per Implementation and Automation.

5. **Expected result — clean import.**

   ```bash
   ./evidence.sh "terraform plan -detailed-exitcode"
   ```

   Exit code `0` (no changes) is expected; investigate and reconcile any
   diff before continuing.

6. Convert the [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) DHCP configuration into the Ansible playbook
   shown in Implementation and Automation, referencing the secret from
   Vault rather than a static value.

7. **Expected result — idempotent playbook run.**

   ```bash
   ./evidence.sh "ansible-playbook dhcp-vlan120.yml"
   ./evidence.sh "ansible-playbook dhcp-vlan120.yml"
   ```

   The second run must report zero changed tasks.

8. Push the Terraform and Ansible code to `git01`, and configure the
   pipeline with separate `plan` and `apply` stages and identities per
   Implementation and Automation, including the Conftest policy gate.

9. **Expected result — clean pipeline run.** Open a pull request with a
   trivial, compliant change (for example, an additional resource tag)
   and confirm the pipeline's `plan` stage runs, the policy gate passes,
   and `apply` runs only after merge and approval.

10. Take a state backup/snapshot labeled `ch06-baseline` (Terraform state
    file backup, Vault snapshot, Git repository tag).

11. **Negative test:** Open a second pull request that introduces a
    policy-violating change — a security group rule permitting SSH from
    `0.0.0.0/0`:

    ```bash
    ./evidence.sh "terraform plan -out=tfplan.bad && \
      conftest test tfplan.bad.json --policy policy/ || true"
    ```

    **Expected result:** The Conftest policy gate reports the specific
    `deny` message from Implementation and Automation, and the pipeline
    blocks the `apply` stage from running — confirm this in the pipeline
    UI or logs, not just the local Conftest output.

12. **Recovery:** Revert the offending change, re-run `plan` and the
    policy gate, and confirm a clean pass before closing the pull
    request.

13. **Cleanup:** No teardown — the automation codebase, Vault instance,
    and CI pipeline are retained and used directly in Chapters 07–09.
    Commit the final state:

    ```bash
    cd ~/vol13-lab
    git add topology.yml
    git commit -m "Chapter 06: infrastructure as code and automated delivery"
    ```

## Summary and Completion Checklist

This chapter converted five chapters' worth of manual builds into
Terraform and Ansible, added a pipeline with a real plan/apply identity
separation, centralized every secret this volume had accumulated into
Vault, and proved a policy gate blocks a non-compliant change before it
reaches production-equivalent infrastructure. Every later chapter's
remaining infrastructure work should route through this pipeline rather
than through the manual commands used in Chapters 02–05.

- [ ] Imported the `CLOUD1` VPC and HQ vSphere cluster into Terraform
      state with no unexpected diff.
- [ ] Converted the [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) DHCP configuration into an idempotent
      Ansible playbook and proved a second run changes nothing.
- [ ] Centralized this volume's accumulated secrets into `vault01`.
- [ ] Built a pipeline with separate `plan`/`apply` identities and a
      working policy gate.
- [ ] Completed the negative test (blocked non-compliant change) and its
      recovery.
