# Chapter 09: Cortex Cloud Security Professional

![Lab flow for this chapter: a sample Terraform file with an unrestricted SSH ingress rule and an unencrypted S3 bucket is scanned with Checkov, reporting at least one failed check for the open ingress rule — the expected, correct behavior for a known-bad configuration, since a scan reporting no findings against this specific file would indicate a broken Checkov installation, not a secure configuration. Narrowing the security group's CIDR block to a lab subnet and re-scanning shows the finding now passing, and a documented suppression is added for the remaining S3 finding. Pushed to a CI/CD pipeline, the unremediated branch fails the check and the remediated branch passes.](../../../diagrams/volume-16-palo-alto-networks-security/chapter-09-checkov-iac-scan-remediation-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: a Terraform configuration scanned with Checkov, deliberately failing first, then remediated and gated in CI/CD.*

## Learning Objectives

- Describe Cortex Cloud's cloud-native application protection platform
  (CNAPP) architecture and how it unifies CSPM, CWPP, CIEM, and IaC/API
  security under a single platform, superseding the earlier standalone
  Prisma Cloud product line.
- Onboard a public cloud account to Cortex Cloud and explain agentless
  versus agent-based workload visibility trade-offs.
- Scan infrastructure-as-code templates for misconfiguration before
  deployment ("shift-left" security) using an open-source policy engine
  aligned with Cortex Cloud's policy set.
- Interpret CSPM findings and CIEM entitlement risk, and describe a
  remediation workflow that closes the loop from detection to fixed code.
- Map foundational knowledge to the Cortex Cloud Security Professional
  certification blueprint domains.

## Theory and Architecture

[Chapter 01](01-cybersecurity-apprentice-foundations.md)'s portfolio table placed Cortex Cloud (formerly Prisma Cloud) at
the cloud workload and posture security layer of defense-in-depth,
distinct from Strata's network-perimeter enforcement and from the
detection/response focus of Cortex XDR and XSIAM. This chapter goes deep on
that layer: securing workloads, configurations, and identities *inside*
public cloud environments — a fundamentally different problem than
inspecting traffic crossing a network boundary, because the attack surface
is API-driven cloud configuration and identity entitlement, not packets on
a wire.

### CNAPP: the unifying architecture

A **cloud-native application protection platform (CNAPP)** converges
several previously separate security disciplines into a single platform
with a shared data model and unified findings/alerting:

| Discipline | Function |
| --- | --- |
| CSPM (Cloud Security Posture Management) | Continuously evaluates cloud account/resource configuration against best-practice and compliance frameworks (CIS Benchmarks, PCI-DSS, NIST, SOC 2), flagging drift and misconfiguration |
| CWPP (Cloud Workload Protection Platform) | Runtime protection and vulnerability scanning for VMs, containers, and serverless functions |
| CIEM (Cloud Infrastructure Entitlement Management) | Analyzes IAM policies and actual permission usage to identify excessive, unused, or toxic-combination entitlements across cloud identities |
| IaC security | Scans Terraform, CloudFormation, ARM/Bicep, and Kubernetes manifests for misconfiguration before deployment, not just after |
| API security | Discovers and assesses the risk of APIs exposed by cloud-native applications |
| Container/Kubernetes security | Image vulnerability scanning, registry scanning, and Kubernetes-specific posture and runtime controls |

Palo Alto Networks' 2025 rebrand consolidated the former standalone Prisma
Cloud product into **Cortex Cloud**, integrating this CNAPP capability
directly with Cortex XSIAM/XDR's detection and response data model — the
practical implication is that a cloud misconfiguration finding and a
runtime threat detection on the same workload now correlate within one
platform's case management rather than requiring an analyst to pivot
between two disconnected tools.

### Agentless versus agent-based workload visibility

Cortex Cloud offers two complementary approaches to workload visibility:

- **Agentless scanning** connects to the cloud provider's API (using a
  read-only, cross-account IAM role) and snapshots workload disks and
  configuration without installing any software inside the workload
  itself. This provides near-immediate, low-friction coverage across an
  entire cloud estate — including workloads a security team does not
  directly manage — at the cost of not detecting genuinely runtime-only
  behavior (a process spawned transiently and gone before the next
  snapshot cycle).
  
- **Agent-based protection** (the Cortex Cloud runtime agent, a
  descendant of the former Prisma Cloud Defender) runs inside the
  workload — as a host agent, a container sidecar/DaemonSet, or a
  serverless layer — providing continuous, real-time visibility into
  process execution, network connections, and file integrity, at the cost
  of deployment and lifecycle management overhead across every covered
  workload.

Most mature deployments run both: agentless scanning for broad,
low-friction estate-wide coverage, and agents on the workload tiers where
runtime detection materially matters (Internet-facing application tiers,
regulated-data workloads, and container/Kubernetes runtime environments
where in-memory or ephemeral-process threats are a realistic concern).

### CIEM and the entitlement problem

Cloud identity and access management (IAM) systems make it easy to grant
broad permissions and hard to know, later, which of those permissions are
actually used. **CIEM** closes this gap by continuously comparing granted
IAM policy against actual API call history, surfacing three categories of
risk: unused permissions (attack surface with no operational benefit),
overly permissive roles (a role granting `*:*` when the identity's actual
usage touches three specific actions), and toxic combinations (a set of
permissions that individually look reasonable but together enable a
privilege-escalation or data-exfiltration path). This is a distinct
discipline from network-layer least privilege ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)) but the same
underlying principle — Zero Trust's "use least-privilege access" — applied
to cloud identity rather than network traffic.

### Shift-left: IaC security before deployment

Every CSPM finding against a live cloud resource represents a
misconfiguration that already reached production. **IaC security scanning**
moves the same policy checks earlier in the pipeline — evaluating a
Terraform plan or CloudFormation template in CI/CD, before `apply`, so a
misconfigured security group or a publicly exposed storage bucket is
rejected at pull-request time rather than remediated after the fact.
Cortex Cloud's IaC scanning is built on **Checkov**, an open-source policy
engine (originally from Bridgecrew, acquired by Palo Alto Networks) that
can run standalone in a CI/CD pipeline using the same policy library
Cortex Cloud enforces against live resources — giving an organization one
consistent policy set enforced at both the pre-deployment (shift-left) and
runtime (posture management) stages, rather than two independently
maintained policy sets that can drift apart.

## Design Considerations

- **Onboarding scope and IAM role design.** Scope the cross-account IAM
  role Cortex Cloud uses for agentless onboarding to read-only permissions
  sufficient for the CNAPP capabilities actually licensed and in use —
  granting broader write access than the platform requires increases the
  blast radius of the connector role itself becoming a target.
- **Agent rollout sequencing.** Do not attempt fleet-wide agent deployment
  on day one. Prioritize agent coverage by workload risk: Internet-facing
  tiers and regulated-data workloads first, internal/low-risk batch
  workloads later or not at all if agentless coverage and compensating
  network controls ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)) are judged sufficient for that tier.
- **Policy tuning against alert fatigue.** A freshly onboarded cloud
  account commonly surfaces a large initial backlog of CSPM findings.
  Triage by severity and exploitability (Internet-facing plus
  high-severity first) rather than attempting to remediate the entire
  backlog before any finding is addressed, and tune or formally accept
  findings that reflect an intentional, documented risk decision rather
  than leaving them as perpetual unaddressed noise.
- **Shift-left enforcement level.** Decide deliberately whether IaC
  scanning in CI/CD blocks a pull request (hard gate) or only annotates it
  (soft gate/advisory) per policy severity and per repository maturity —
  a hard gate on every policy from day one on a repository with no prior
  scanning discipline tends to generate pipeline friction that leads teams
  to bypass the check rather than fix the finding; a phased hard-gate
  rollout (critical/high severity first) is more sustainable.
- **CIEM remediation ownership.** Cross-functional ownership matters here
  more than in most security domains — an overly permissive IAM role is
  frequently owned by an application or platform team, not the security
  team, so CIEM findings need a defined handoff and remediation SLA to the
  actual role owner rather than accumulating as security-team-only
  backlog.

## Implementation and Automation

### Onboarding an AWS account (agentless)

```bash
# Cortex Cloud provides a CloudFormation template that provisions the
# read-only cross-account IAM role; apply it via the AWS CLI or console.
aws cloudformation create-stack \
  --stack-name cortex-cloud-onboarding \
  --template-url https://cortex-cloud-templates.paloaltonetworks.com/aws-onboarding.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=ExternalId,ParameterValue=<CORTEX_EXTERNAL_ID>
```

After the stack completes, register the account in Cortex Cloud with the
resulting role ARN (via the console or the platform API) to begin
agentless scanning.

### Scanning Terraform with Checkov before deployment

```bash
pip install checkov
checkov -d ./terraform/branch-network --framework terraform
```

Example finding output:

```text
Check: CKV_AWS_24: "Ensure no security groups allow ingress from 0.0.0.0:0 to port 22"
    FAILED for resource: aws_security_group.bastion_sg
    File: /terraform/branch-network/main.tf:14-22

        14 | resource "aws_security_group" "bastion_sg" {
        15 |   ingress {
        16 |     from_port   = 22
        17 |     to_port     = 22
        18 |     protocol    = "tcp"
        19 |     cidr_blocks = ["0.0.0.0/0"]
        20 |   }
        21 | }
```

### Integrating Checkov into a CI/CD pipeline (illustrative)

```yaml
# .github/workflows/iac-scan.yml
name: IaC Security Scan
on: [pull_request]
jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          soft_fail: false
          check: CKV_AWS_24,CKV_AWS_23,CKV_AWS_18
```

`soft_fail: false` makes matching findings a hard pipeline gate; a phased
rollout (Design Considerations) would begin with `soft_fail: true` and a
narrower `check` scope, then tighten both over time.

### Scanning a container image with twistcli

```bash
twistcli images scan \
  --address https://cortex-cloud-compute.paloaltonetworks.com \
  --user <API_USER> --password <API_PASSWORD> \
  acme/branch-app:1.4.2
```

### Querying CIEM findings via the platform API (illustrative)

```bash
curl -sk -X GET \
  "https://api.cortex-cloud.paloaltonetworks.com/ciem/v1/findings?severity=high&type=unused-permission" \
  -H "Authorization: Bearer ${CORTEX_CLOUD_API_TOKEN}"
```

## Validation and Troubleshooting

- **Onboarded account shows no resources.** Confirm the cross-account IAM
  role's trust policy correctly references the Cortex Cloud external
  account ID and external ID (a mismatch is the most common agentless
  onboarding failure), and confirm the role's attached policy actually
  grants read access to the resource types expected in findings — an
  overly narrow initial role scope silently under-reports rather than
  erroring visibly.
- **Checkov reports a false positive against an intentionally accepted
  risk.** Use an inline suppression comment (`#checkov:skip=CKV_AWS_24:
  <justification>`) rather than disabling the check organization-wide —
  scoped suppression with a documented reason preserves the check's value
  for every other resource while formally recording the accepted
  exception.
- **CI/CD pipeline blocks on a finding the team disputes.** Confirm
  whether the finding reflects the same policy enforced by CSPM against
  live resources (in which case the dispute is a policy-tuning
  conversation with the security team) or a stale/local Checkov policy
  version out of sync with the platform's current policy set (in which
  case updating the pinned Checkov/policy version resolves it).
- **Agent-based workload not reporting runtime data.** Confirm the agent
  process is running and has outbound reachability to the Cortex Cloud
  compute/runtime service endpoint; a common cause in restrictive network
  environments is an egress security policy ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)) blocking the
  agent's reporting traffic, which is a self-inflicted visibility gap
  worth checking before assuming an agent installation defect.
- **CIEM shows a permission as "unused" that is actually used
  infrequently.** Confirm the platform's lookback window for usage
  analysis covers the permission's actual usage cadence (for example, a
  quarterly batch job's IAM role may appear unused against a 30-day
  window) before remediating — CIEM findings should specify their
  observation window, and remediation decisions should account for it.

## Security and Best Practices

- Scope every Cortex Cloud onboarding IAM role to the minimum permissions
  the licensed CNAPP capabilities require, and review that scope whenever
  new Cortex Cloud modules are enabled.
- Enforce IaC scanning as a required, non-bypassable CI/CD check for
  critical/high-severity findings once the phased rollout (Design
  Considerations) reaches that maturity stage — a scan that developers can
  silently skip provides a false sense of coverage.
- Treat CIEM remediation as an identity-governance workflow with defined
  ownership and SLA, not a security-team-only backlog; unused or
  excessive cloud entitlements are one of the highest-leverage attack
  surface reductions available in a cloud environment and are frequently
  under-prioritized relative to their risk.
- Correlate CSPM/CWPP findings with Cortex XDR/XSIAM detections
  ([Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)) for the same workload rather than reviewing each platform's
  findings in isolation — the unified Cortex Cloud data model exists
  specifically to make this correlation available without manual
  cross-referencing.
- Rotate and scope any Cortex Cloud API tokens used for automation
  (Checkov CI/CD integration, CIEM API queries) with the same discipline
  as the PAN-OS/Panorama automation credentials from [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md).
- Periodically re-validate that agent-based coverage still matches the
  current risk-tiered rollout plan — workload inventories drift, and a
  newly provisioned Internet-facing tier deployed outside the original
  rollout plan is a common coverage gap.

## References and Knowledge Checks

**References**

- [Palo Alto Networks, *Cortex Cloud* product and administrator
  documentation.](https://docs-cortex.paloaltonetworks.com/)
- [Palo Alto Networks / Bridgecrew, *Checkov* open-source documentation.](https://www.checkov.io/)
- [Palo Alto Networks, *Cortex Cloud Compute* (container/twistcli) scanning
  documentation.](https://docs-cortex.paloaltonetworks.com/r/Cortex-CLOUD/Cortex-Cloud-Runtime-Security-Documentation/Code-Security-scanners)
- [Palo Alto Networks, *Cortex Cloud Security Professional* certification
  blueprint.](https://www.paloaltonetworks.com/services/education/certification)
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this volume's certification mapping.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated baseline
  reference for this volume.
- [Volume VII](../../volume-07-cloud-infrastructure/README.md) — Cloud Infrastructure and [Volume IX](../../volume-09-infrastructure-automation/README.md) — Infrastructure
  Automation, for the IAM and CI/CD pipeline concepts this chapter builds
  on.

**Knowledge checks**

1. What five (or more) previously separate disciplines does a CNAPP
   converge, and which one specifically analyzes IAM entitlement usage
   rather than resource configuration?
2. What is the practical trade-off between agentless and agent-based
   workload visibility in Cortex Cloud?
3. Why does running the same Checkov policy set in CI/CD and in live CSPM
   scanning matter, compared to maintaining two independently managed
   policy sets?
4. Give one reason a CIEM "unused permission" finding might be a false
   positive, and what additional information resolves the ambiguity.

## Hands-On Lab

**Objective:** Scan a Terraform configuration with Checkov, identify and
remediate an intentionally introduced misconfiguration, integrate the scan
into a CI/CD gate, and validate an agentless cloud account connection
concept — including a negative test confirming the scan correctly fails a
known-bad configuration before remediation.

**Prerequisites**

- Python 3.9+ available on the lab workstation to install Checkov.
- A small sample Terraform configuration directory (can reuse or adapt the
  address-object/security-group patterns from earlier chapters' lab
  environments, or a minimal standalone example as used below).
- Optional: a lab or trial cloud account and Cortex Cloud tenant for the
  onboarding portion; the Checkov-based steps do not require this and can
  be completed standalone.
- Optional: a GitHub (or equivalent) repository to exercise the CI/CD
  integration step.

**Steps**

1. Install Checkov:

   ```bash
   pip install checkov
   checkov --version
   ```

2. Create a sample Terraform file with an intentional misconfiguration:

   ```bash
   mkdir -p lab-iac-scan
   cat > lab-iac-scan/main.tf <<'EOF'
   resource "aws_security_group" "bastion_sg" {
     name        = "bastion-sg"
     description = "Bastion host access"

     ingress {
       from_port   = 22
       to_port     = 22
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
     }
   }

   resource "aws_s3_bucket" "app_data" {
     bucket = "acme-app-data-lab"
   }
   EOF
   ```

3. Run Checkov against the directory:

   ```bash
   checkov -d lab-iac-scan --framework terraform
   ```

   **Expected result:** Checkov reports at least one `FAILED` check for
   the unrestricted SSH ingress rule (`CKV_AWS_24` or equivalent) and
   likely additional findings for the S3 bucket lacking encryption/public-
   access-block configuration.

4. **Negative test (confirm the scan fails as expected before
   remediation):** Note the specific check ID and resource reported as
   failed; this is the expected, correct behavior for a known-bad
   configuration — a scan that reported no findings against this file
   would indicate a broken or misconfigured Checkov installation, not a
   secure configuration.

5. Remediate the security group finding:

   ```bash
   sed -i.bak 's/cidr_blocks = \["0.0.0.0\/0"\]/cidr_blocks = ["10.10.0.0\/16"]/' lab-iac-scan/main.tf
   ```

6. Re-run the scan and confirm the specific finding now passes:

   ```bash
   checkov -d lab-iac-scan --framework terraform --check CKV_AWS_24
   ```

   **Expected result:** `PASSED` for `CKV_AWS_24` against
   `aws_security_group.bastion_sg`.

7. Add a scoped suppression for the remaining S3 finding, with a
   documented reason, to demonstrate the disputed-finding workflow from
   Validation and Troubleshooting:

   ```bash
   cat >> lab-iac-scan/main.tf <<'EOF'
   # checkov:skip=CKV2_AWS_6: Lab bucket, no production data; documented exception for training purposes
   EOF
   ```

8. If a CI/CD repository is available, add the illustrative GitHub Actions
   workflow from Implementation and Automation, push a branch containing
   the unremediated version of `main.tf`, and confirm the pipeline check
   fails; then push the remediated version and confirm it passes.

9. **Optional cloud onboarding validation.** If a lab cloud account and
   Cortex Cloud tenant are available, apply the onboarding CloudFormation
   template (or equivalent for another cloud provider), register the
   account in Cortex Cloud, and confirm the account appears with an
   initial CSPM finding count within the platform console.

10. **Cleanup:** Remove the lab directory and any lab-only CI/CD workflow
    file if not needed going forward:

    ```bash
    rm -rf lab-iac-scan
    ```

    If a lab cloud account was onboarded, deregister it from Cortex Cloud
    and delete the onboarding CloudFormation stack (or equivalent) to
    remove the cross-account IAM role:

    ```bash
    aws cloudformation delete-stack --stack-name cortex-cloud-onboarding
    ```

## Summary and Completion Checklist

Cortex Cloud extends Zero Trust's least-privilege and continuous-
verification principles from [Chapter 01](01-cybersecurity-apprentice-foundations.md) into the cloud control plane
itself: CSPM continuously assesses configuration posture, CWPP protects
running workloads, CIEM closes the identity-entitlement gap traditional
network controls cannot see, and IaC scanning with Checkov shifts the same
policy enforcement left into CI/CD so misconfiguration is rejected before
it ever reaches production. Combined with [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)'s portfolio-wide
Cortex overview and [Chapter 08](08-role-based-certification-portfolio-and-enterprise-capstone.md)'s enterprise capstone, this chapter
completes the volume's coverage of the Palo Alto Networks platform across
network, management, and cloud-native security domains.

- [ ] Can describe the CNAPP disciplines Cortex Cloud unifies and how it
      relates to the former standalone Prisma Cloud product.
- [ ] Can explain the agentless vs. agent-based workload visibility
      trade-off and a reasonable rollout sequencing.
- [ ] Can scan an IaC template with Checkov, interpret a finding, and
      remediate it.
- [ ] Can explain CIEM's purpose and describe a defensible remediation
      ownership model.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
