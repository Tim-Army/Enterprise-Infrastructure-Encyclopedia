# Chapter 04: Configuration Templates, Baselines, and Change Records

## Learning Objectives

- Distinguish a configuration template, a golden baseline, and a
  drift-detection report, and explain how the three fit together in a
  managed configuration lifecycle.
- Produce a minimal, parameterized configuration template for at least
  three platform families (Linux service, network device, cloud/IaC
  resource) using the placeholder conventions established in this
  encyclopedia.
- Write a change record complete enough to satisfy the four
  safe-administration gates from [Chapter 01](01-command-quick-reference-and-safe-administration.md) (authorization, backup, dry
  run, rollback plan).
- Detect configuration drift between a running system and its declared
  baseline using at least one automated method per platform family.
- Version and review configuration templates with the same rigor applied
  to application source code.

## Theory and Architecture

A **configuration template** is a parameterized document that produces a
concrete configuration when combined with variable values — a Jinja2
file rendered by Ansible, a Terraform module accepting input variables, or
a Cisco IOS XE configuration snippet with `<PLACEHOLDER>` tokens replaced
per device. Templates exist to make configuration reproducible: the same
template, given the same inputs, produces the same result every time.

A **baseline** is a specific, approved, versioned instance of a
configuration — the answer to "what should this system's configuration
be right now." A baseline is not the template; it is a template rendered
with a specific, reviewed set of values (or, for systems without native
templating, a captured known-good configuration file) that has been
approved as the standard for a role, tier, or fleet segment. CIS Benchmarks
and vendor hardening guides ([Chapter 07](07-security-hardening-incident-response-and-risk-reference.md)) are examples of externally
published baselines; most enterprises also maintain internal baselines
layered on top of those.

A **change record** is the governance artifact that authorizes moving a
system from its current state toward a new baseline. It is distinct from
both the template (the mechanism) and the baseline (the target state): the
change record captures who approved the change, why, what backup and
rollback exist, and what evidence will confirm success — the same four
gates introduced in [Chapter 01](01-command-quick-reference-and-safe-administration.md), now formalized as a document rather than
an in-the-moment checklist.

**Drift** is any divergence between a system's actual, running
configuration and its declared baseline. Drift is not automatically a
defect — an emergency change made outside the normal pipeline is drift
until it is either reconciled into the baseline or reverted — but
undetected, unexplained drift is one of the most common root causes of "it
worked in the last environment but not this one" failures across every
platform in this encyclopedia.

## Design Considerations

- **Store templates and baselines as code, in the same repository
  discipline as application source** ([Volume I, Chapter 02](../../volume-01-enterprise-engineering-foundations/chapters/02-repository-architecture.md)): version
  control, pull request review, and CI validation apply to a Jinja2
  template or a Terraform module exactly as they apply to a Python
  service.
- **Separate the template from the values file.** A template with
  environment-specific values hardcoded cannot be reused; keep variables
  (`vars/prod.yml`, `terraform.tfvars`, device-specific data files)
  distinct from the logic that renders them, so the same template serves
  every environment/tier.
- **Decide the baseline's source of truth explicitly.** For imperative
  platforms without native state reconciliation (most network devices,
  many appliances), the baseline is the last-approved configuration file
  in version control, and the device's running-config is expected to
  match it. For declarative platforms (Terraform, Kubernetes, Ansible in
  its idempotent mode), the baseline is the declared manifest itself, and
  the platform's own reconciliation loop (or a scheduled `plan`/`--check`
  run) is the drift detector.
- **Right-size change record formality to risk tier** ([Chapter 01](01-command-quick-reference-and-safe-administration.md)'s
  Tier 0–3 model): a Tier 1 change needs a lightweight record; a Tier 3
  change needs full CAB review, a named approver distinct from the
  executor, and a tested rollback procedure attached before execution
  begins.
- **Plan baseline review cadence, not just initial creation.** A CIS
  Benchmark or vendor hardening guide is dated; schedule a recurring
  review (quarterly or aligned to major release changes recorded in
  `SOFTWARE_VERSIONS.md`) rather than treating the baseline as a one-time
  artifact.
- **Make drift detection continuous where the platform supports it.**
  A nightly `terraform plan`, `ansible-playbook --check --diff`, or
  configuration-compliance scan surfaces drift within a day rather than
  at the next audit cycle, when root cause is far harder to establish.

## Implementation and Automation

### Template placeholder conventions used across this encyclopedia

| Convention | Meaning | Example |
| --- | --- | --- |
| `<UPPER_SNAKE_CASE>` | A required, human-supplied value with no safe default | `<VLAN_ID>`, `<HOSTNAME>` |
| `{{ jinja_variable }}` | An Ansible/Jinja2-rendered value, typically sourced from inventory or a vars file | `{{ ntp_server_primary }}` |
| `${terraform_variable}` / `var.name` | A Terraform input variable | `var.instance_type` |
| `# TODO:` | A template section intentionally left for environment-specific completion, flagged for review before use | `# TODO: confirm subnet CIDR with network team` |

### Example templates by platform family

**Linux service configuration (Jinja2, rendered by Ansible)**

```jinja2
# /etc/chrony.conf.j2 - NTP client baseline (see Chapter 03 stratum design)
{% for server in ntp_servers %}
server {{ server }} iburst
{% endfor %}
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
logdir /var/log/chrony
```

```yaml
# vars/prod.yml
ntp_servers:
  - 10.10.1.10
  - 10.10.1.11
```

**Network device configuration (Cisco IOS XE, values file + template)**

```text
! access-vlan-template.txt
interface <INTERFACE>
 description <DESCRIPTION>
 switchport mode access
 switchport access vlan <VLAN_ID>
 spanning-tree portfast
 spanning-tree bpduguard enable
!
```

```yaml
# access-vlan-values.yml (rendered by a script or Ansible `ios_config`)
INTERFACE: GigabitEthernet1/0/12
DESCRIPTION: "Workstation - Bldg A - Port 12"
VLAN_ID: 110
```

**Cloud/IaC resource (Terraform)**

```hcl
variable "environment" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.baseline.id
  instance_type = var.instance_type
  tags = {
    Name        = "app-${var.environment}-01"
    Environment = var.environment
    Baseline    = "v2026.07"
  }
}
```

### Change record template

Every Tier 1–3 change ([Chapter 01](01-command-quick-reference-and-safe-administration.md)) should produce a record containing, at
minimum, the fields below. Store change records in the same repository as
the templates and baselines they affect, or in a linked change-management
system referenced by ID.

```markdown
## Change Record: <short title>

- **Change ID:** <tracking ID>
- **Risk tier:** <0-3, per Chapter 01>
- **Requested by / Approved by:** <two distinct names for Tier 2/3>
- **Systems affected:** <hostnames, device names, or resource IDs>
- **Baseline reference:** <link to the template/baseline version being applied>
- **Change window:** <date/time, or "standard" for pre-approved changes>
- **Authorization:** <link to approval - ticket, CAB minutes, or pre-approved runbook ID>
- **Backup:** <what was captured, where, and how to restore it>
- **Dry run evidence:** <plan/check/diff output or link to it>
- **Rollback procedure:** <exact command(s) or steps to revert>
- **Validation plan:** <what will be checked after the change, referencing Chapter 05>
- **Result:** <success / rolled back / partial, completed after execution>
```

### Drift detection by platform family

| Platform Family | Drift Detection Method | Automation Example |
| --- | --- | --- |
| Linux (RHEL/Ubuntu) | Configuration management check mode; file-integrity monitoring | `ansible-playbook site.yml --check --diff` |
| Cisco IOS XE | Compare running-config against last committed baseline in version control | `show archive config differences system:running-config nvram:startup-config` |
| PAN-OS / FortiOS | Candidate vs. running config diff before commit; scheduled config export compared to baseline in version control | PAN-OS: `show config diff`; FortiOS: `diff` against last `execute backup config` output |
| Terraform-managed cloud resources | Native plan-based drift detection | `terraform plan -detailed-exitcode` (exit code 2 indicates drift) |
| Kubernetes | Reconciliation loop is continuous; GitOps tooling reports out-of-sync state | `kubectl diff -f <manifest>`; Argo CD/Flux sync status |
| VMware vSphere | Host profile compliance check against a reference host | `Test-VMHostProfileCompliance` (PowerCLI) |
| Windows Server | Group Policy / Desired State Configuration compliance report | `Get-DscConfigurationStatus`; `gpresult /h report.html` |

## Validation and Troubleshooting

- **Render the template against a test value set before applying it to a
  target system.** `ansible-playbook --check --diff`, `terraform plan`,
  or manual template rendering to a local file catches syntax and
  variable-resolution errors before they reach production, satisfying the
  dry-run gate from [Chapter 01](01-command-quick-reference-and-safe-administration.md).
- **Diff the rendered output against the previous baseline, not just
  against "nothing."** A clean render with no syntax errors can still
  introduce an unintended change if a variable default shifted; comparing
  against the prior approved baseline surfaces intent, not just syntax
  validity.
- **When drift is detected, classify it before reacting.** Determine
  whether the drift is unauthorized (investigate as a possible incident,
  [Chapter 07](07-security-hardening-incident-response-and-risk-reference.md)), an undocumented emergency change (reconcile into the
  baseline and back-fill a change record), or a detection false positive
  (a value that legitimately varies per host, such as a hostname, that
  was incorrectly included in the compliance check).
- **Confirm the rollback procedure works before relying on it in an
  emergency.** A rollback step that has only ever been read, not
  executed, is a common source of a failed recovery; validate rollback
  procedures for Tier 2/3 changes in a lab or staging environment on a
  recurring basis.
- **Trace template rendering failures to the variable source first.**
  Most template failures in Ansible/Terraform are undefined or
  incorrectly typed variables, not template logic errors; `ansible-playbook
  -vvv` or `terraform console` isolates the failing variable quickly.

## Security and Best Practices

- Never commit secrets (passwords, API keys, private keys) directly into
  a template or values file; reference a secrets manager or vault
  (HashiCorp Vault, AWS Secrets Manager, Ansible Vault) and inject values
  at render or apply time.
- Require pull request review for any change to a baseline or template
  that affects a production-tier fleet segment, mirroring the CODEOWNERS
  pattern established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md).
- Restrict who can approve Tier 2/3 change records to named individuals
  distinct from the person executing the change, and log both identities
  in the change record itself, not only in an external ticketing system
  that may not be retained as long as the configuration history.
- Treat a baseline's approval date and reviewer as part of the baseline,
  not metadata to be inferred from commit history; an auditor should be
  able to answer "who approved this configuration, and when" from the
  record itself.
- Encrypt or restrict access to exported configuration backups
  (`copy running-config tftp:`-style operations); a plaintext
  configuration backup routinely contains hashed or, on older platforms,
  cleartext credentials and should be treated with the same handling
  rules as the live system.
- Periodically re-validate that the current baseline still matches the
  current CIS Benchmark or vendor hardening guide version ([Chapter 07](07-security-hardening-incident-response-and-risk-reference.md));
  hardening guidance changes across major releases tracked in
  `SOFTWARE_VERSIONS.md`.

## References and Knowledge Checks

**References**

- [Volume I, Chapter 02](../../volume-01-enterprise-engineering-foundations/chapters/02-repository-architecture.md) — Repository Architecture (version control
  discipline applied to configuration).
- [Volume I, Chapter 03](../../volume-01-enterprise-engineering-foundations/chapters/03-automation-architecture.md) — Automation Architecture (plan/apply separation).
- [Volume IX](../../volume-09-infrastructure-automation/README.md) — Infrastructure Automation (full Ansible/Terraform template
  and module design treatment).
- [Ansible Jinja2 templating documentation
  (`docs.ansible.com/ansible/latest/playbook_guide`).](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)
- [Terraform Configuration Language documentation
  (`developer.hashicorp.com/terraform/language`).](https://developer.hashicorp.com/terraform/language)
- CIS Benchmarks (`cisecurity.org/cis-benchmarks`) — external baseline
  source referenced in [Chapter 07](07-security-hardening-incident-response-and-risk-reference.md).
- [Chapter 01](01-command-quick-reference-and-safe-administration.md) of this volume — the four safe-administration gates that
  change records formalize.

**Knowledge checks**

1. Explain the difference between a template, a baseline, and a change
   record using an example from your own environment.
2. Why should secrets never be committed directly into a template or
   values file, even in a private repository?
3. A `terraform plan -detailed-exitcode` run returns exit code 2 on a
   resource nobody recalls changing. What are the two possible
   explanations, and what should happen next in each case?
4. What two identities must a Tier 2/3 change record capture, and why
   must they be distinct?

## Hands-On Lab

**Objective:** Produce a parameterized template, an approved baseline
instance, and a complete change record for a lab configuration change,
then detect and reconcile intentionally introduced drift.

**Prerequisites:** A lab system you can safely modify (a Linux VM is
sufficient); a text editor; optionally Ansible or Terraform installed for
the automation steps; version control (local Git repository is
sufficient).

1. Create a simple configuration template for a lab service (for example,
   a `chrony.conf.j2` or a plain config file with `<PLACEHOLDER>` tokens)
   with at least two variables. **Expected result:** a template file with
   clearly marked placeholders exists in version control.
2. Render the template with a specific values file to produce a
   concrete baseline configuration, and save the rendered output as
   `baseline-v1.conf`. **Expected result:** a fully resolved configuration
   file with no remaining placeholders.
3. Write a complete change record using the template in this chapter for
   applying `baseline-v1.conf` to the lab system, including a real backup
   step and a real rollback command. **Expected result:** a change record
   with all fields populated before any change is executed.
4. Execute the dry run named in the change record (a `--check`/`plan`
   run, or a manual diff against the currently running configuration) and
   attach its output to the record. **Expected result:** dry-run evidence
   shows only the intended difference.
5. Apply the change, then immediately re-capture the running
   configuration and diff it against `baseline-v1.conf`. **Expected
   result:** no unexpected difference; the system matches its declared
   baseline.
6. Manually introduce one small, undocumented change directly on the lab
   system (drift), then re-run the drift detection method appropriate to
   the platform. **Expected result:** the drift is detected and reported.
7. Reconcile the drift by either updating the baseline (with a new change
   record documenting the intentional change) or reverting the system to
   match `baseline-v1.conf`, and record which path was chosen and why.
   **Expected result:** the system and its declared baseline agree again,
   with the reconciliation decision documented.

**Cleanup:** Revert the lab system to its pre-lab state if it is shared,
remove any temporary backup files, and delete lab-only entries from
version control if the repository is shared beyond this exercise.

## Summary and Completion Checklist

This chapter distinguished three artifacts that are often conflated —
templates (the parameterized mechanism), baselines (the specific approved
target state), and change records (the governance artifact authorizing
movement toward that state) — and provided example templates,
a change-record format, and a per-platform drift-detection reference
spanning Linux, network devices, security appliances, Terraform, Kubernetes,
VMware, and Windows Server.

- [ ] I can explain the difference between a template, a baseline, and a
      change record.
- [ ] I produced a working parameterized template and rendered it into a
      concrete baseline.
- [ ] I wrote a complete change record satisfying all four
      safe-administration gates from [Chapter 01](01-command-quick-reference-and-safe-administration.md).
- [ ] I detected drift using an automated method appropriate to at least
      one platform family.
- [ ] I reconciled detected drift and documented the decision path taken.
