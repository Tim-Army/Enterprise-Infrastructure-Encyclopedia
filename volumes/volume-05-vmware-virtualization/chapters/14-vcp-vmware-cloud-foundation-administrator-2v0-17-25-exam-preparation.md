# Chapter 14: VCP VMware Cloud Foundation Administrator 2V0-17.25 Exam Preparation

![Lab flow for this chapter: host commissioning prerequisites (NTP sync, DNS resolution, acceptance level) are verified on an additional host. As a negative test, NTP is deliberately misconfigured and commissioning is attempted; the validation fails or warns specifically on the time-synchronization prerequisite, naming the actual root cause rather than a generic error. NTP is corrected and re-verified, then a new cluster is created with HA/DRS and the host joins successfully. A scoped RBAC role at the new cluster's folder confirms a test account can manage the new cluster but is denied against the pre-existing standalone infrastructure. The standalone vCenter's certificate store is inspected as import-path preparation.](../../../diagrams/volume-05-vmware-virtualization/chapter-14-vcf-admin-commissioning-rbac-flow.svg)

*Figure 14-1. Flow used throughout this chapter's Hands-On Lab: host commissioning prerequisites, a deliberately broken NTP negative test, workload-domain-style cluster creation, and RBAC layering.*

## Learning Objectives

- Map the 2V0-17.25 blueprint's deployment, design, and day-2 operational
  domains to the VCF architecture concepts introduced in [Chapter 1](01-vmware-virtualization-architecture-and-design.md) and
  the underlying vSphere/NSX chapters throughout this volume.
- Explain workload domain deployment models and the operational
  responsibilities an administrator (as distinct from a support engineer
  or solution architect) owns.
- Build a study plan emphasizing deployment procedure, day-2 lifecycle
  operations, and identity/licensing/certificate administration.
- Practice designing and deploying a VI workload domain end to end in a
  lab, including importing an existing vCenter Server into fleet
  management.
- Complete a comprehensive administrator-track readiness lab covering
  deployment, RBAC, licensing, and certificate lifecycle tasks.

## Theory and Architecture

This chapter is study and review material for the **VMware Certified
Professional – VMware Cloud Foundation Administrator (VCP-VCF
Administrator), exam 2V0-17.25**. Confirm current domain names, item
count, and exam duration against Broadcom's published exam guide before
relying on this chapter — it organizes concepts against the publicly
published blueprint structure and points to grounding material in this
volume; it does not reproduce the blueprint or any exam content.

### How this exam differs from the support and architecture exams

The 2V0-17.25 blueprint targets the **VCF Administrator** role
specifically: the practitioner who deploys, configures, and operates VCF
day to day — provisioning workload domains, managing fleet-wide identity
and licensing, handling certificate lifecycle, and importing existing
infrastructure into VCF management — rather than the support engineer's
break-fix diagnostic focus ([Chapter 13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md)) or a solution architect's
requirements-to-design translation focus. Its blueprint's later sections
explicitly cover both **planning/design** skills and **deploy/configure/
operate** skills, meaning preparation should cover both "what is the
correct design given these requirements" judgment and "how do I actually
execute that design" procedural competency — administrators are expected
to do both, not hand a design off to someone else to build.

### Workload domain deployment models

Building on [Chapter 1](01-vmware-virtualization-architecture-and-design.md)'s introduction of the **management domain** and
**VI workload domains**, an administrator-level understanding requires
knowing the concrete deployment mechanics:

- **Management domain bring-up** happens once, using **Cloud Builder** —
  an appliance that validates a deployment specification (a filled-out
  deployment parameter workbook or equivalent structured input) against
  prerequisites (DNS, NTP, network pools, host readiness) and then
  automates the initial deployment of the management domain's vCenter
  Server, NSX Manager cluster, and SDDC Manager itself. Cloud Builder is
  explicitly a bring-up tool — once the management domain exists, ongoing
  lifecycle operations transfer entirely to SDDC Manager, and Cloud
  Builder is not used again for that instance's day-2 operations.
- **VI workload domain creation** is SDDC Manager's ongoing
  responsibility: an administrator selects available hosts (already
  commissioned into SDDC Manager's free-host pool), a network pool for
  vMotion/vSAN IP addressing, and a cluster configuration (including
  vSAN as the default principal storage, though other supported principal
  storage options exist depending on the VCF edition/configuration), and
  SDDC Manager orchestrates deployment of a new vCenter Server (or
  attachment to an existing one) and cluster for that workload domain,
  optionally with its own dedicated NSX instance for isolation from other
  workload domains.
- **Importing an existing vCenter Server** into VCF/fleet management —
  bringing already-deployed, standalone vSphere infrastructure (of the
  kind built using Chapters 2–4 of this volume) under VCF's centralized
  lifecycle and fleet-management umbrella — is a distinct administrator
  workflow from creating a new workload domain from scratch, with its own
  prerequisite validation (version compatibility, configuration
  conformance) that must pass before import succeeds.

### Day-2 administrator responsibilities

Beyond initial deployment, the blueprint's deploy/configure/operate
domain covers ongoing administrator responsibilities:

- **Fleet management operations** — centralized version/patch tracking
  and, where supported, coordinated lifecycle operations across managed
  VCF instances (introduced from a support-troubleshooting angle in
  [Chapter 13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md); here, the administrator's responsibility is correctly
  initiating and sequencing these operations, not only diagnosing their
  failures).
- **Identity and role-based access** — SDDC Manager's own RBAC model for
  administrator/operator access, integrated with Identity Broker
  federation ([Chapter 13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md)), extending the vCenter Server RBAC concepts
  from [Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md) to the fleet/orchestration layer.
- **Licensing** — applying and managing VCF-level licensing across
  workload domains as they are created and expanded, distinct from (but
  coordinated with) individual component licensing.
- **Certificate handling** — VCF-wide certificate lifecycle management
  across managed components, extending the certificate management
  concepts from [Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md) (VMCA versus externally issued certificates)
  and [Chapter 8](08-vsphere-and-nsx-security-architecture.md) to a fleet-orchestrated scope, where SDDC Manager
  coordinates certificate requests/renewals/installation across multiple
  managed components rather than an administrator handling each
  component's certificate independently.

## Design Considerations

- **Balance design judgment and procedural competency in study time.**
  Because this exam's blueprint explicitly covers both planning/design
  and deploy/configure/operate skills, do not over-invest in one at the
  expense of the other — practice both articulating *why* a workload
  domain configuration choice is correct for a given requirement and
  actually executing that configuration in a lab.
- **Cloud Builder scope discipline.** Understand precisely that Cloud
  Builder's role ends at management domain bring-up — a common
  misconception is treating it as an ongoing management tool, when SDDC
  Manager owns every subsequent lifecycle operation, including
  management domain patching/upgrades themselves.
- **Import-versus-create workload domain decision.** Recognize when
  importing existing vSphere infrastructure into VCF management is the
  correct path (an organization with substantial existing standalone
  vSphere investment moving to VCF) versus creating new workload domains
  from freshly commissioned hosts — the prerequisite validation and
  procedural steps differ meaningfully between the two paths.
- **Fleet-scope RBAC versus per-component RBAC.** Study SDDC Manager's
  RBAC model as a genuinely separate layer from vCenter Server's own RBAC
  ([Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md)) and NSX's RBAC ([Chapter 10](10-installing-vmware-nsx.md)/11) — an administrator role at
  the fleet/SDDC Manager layer does not automatically imply equivalent
  access at every managed component's own layer, and the exam's identity/
  RBAC objectives test this layered understanding specifically.
- **Certificate lifecycle coordination complexity.** Fleet-orchestrated
  certificate management across multiple components (vCenter Server, NSX
  Manager, SDDC Manager itself) introduces sequencing and trust-
  propagation considerations beyond a single component's certificate
  replacement ([Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md)) — study this as its own workflow, not simply as
  "the same thing as [Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md), done several times."

## Implementation and Automation

### Building a domain-mapped study tracker

```text
# Example self-assessment tracker for the administrator-exam's domain structure

Domain                                  | Grounding chapter(s) | Self-rating | Notes
------------------------------------------|-------------------------|--------------|----------------------------------
IT architecture/standards fundamentals    | 1, 4                     |              | General SDDC/networking concepts
VCF fundamentals (components, roles)      | 1                        |              | SDDC Manager, workload domains
Plan and design                           | 1, 3, 4, 6, 7            |              | Sizing, topology, HA/DRS design carryover
Workload domain deployment                | 2, 3, 4                 |              | Host commissioning, vCenter/NSX per domain
Fleet management operations               | 9, 13                    |              | Version tracking, coordinated lifecycle
Identity and RBAC (fleet layer)           | 3, 13                    |              | SDDC Manager RBAC vs component RBAC
Licensing administration                  | (VCF-specific)           |              | Fleet-level license application
Certificate handling (fleet layer)        | 3, 8                     |              | Coordinated multi-component lifecycle
Importing existing vCenter Servers        | 3                        |              | Prerequisite/version conformance checks
```

### Practicing the underlying deployment mechanics in a lab

```powershell
# PowerCLI: as administrator-exam preparation, practice the underlying
# host-commissioning and cluster-creation mechanics that SDDC Manager
# orchestrates on your behalf during workload domain creation — knowing
# what SDDC Manager is actually doing under the hood strengthens both
# the design and deploy/configure/operate domains

Connect-VIServer -Server vcenter-wld01.corp.example
$cluster = New-Cluster -Name "wld01-cluster-a" -Location (Get-Datacenter -Name "wld01-dc") `
  -HAEnabled -DrsEnabled -DrsAutomationLevel FullyAutomated
```

```bash
# esxcli: confirm a host is genuinely ready for commissioning
# (NTP synchronized, correct acceptance level, no residual configuration
# from a prior role) before it would pass SDDC Manager's own prerequisite
# validation for workload domain host assignment
esxcli system ntp get
esxcli software acceptance get
```

### Rehearsing certificate lifecycle coordination

```bash
# From the vCenter Server appliance shell: the same certificate-store
# inspection skill from Chapter 3, rehearsed here as the foundation for
# understanding what a fleet-orchestrated certificate operation is
# actually coordinating across each managed component
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text
```

## Validation and Troubleshooting

- **Design-versus-execution self-check.** For each workload domain design
  scenario practiced, explicitly answer both "what would I configure"
  and "why is this the correct choice given the stated requirement"
  separately — a candidate who can execute correctly but cannot justify
  the choice, or vice versa, has an identifiable gap the blueprint's dual
  planning/execution structure will expose.
- **Prerequisite-validation rehearsal.** Deliberately omit a prerequisite
  (misconfigured NTP on a host intended for commissioning, for instance)
  and observe how SDDC Manager's validation surfaces it — this builds the
  same prerequisite-first diagnostic instinct Chapter 13 emphasizes for
  the support exam, valuable here for correctly interpreting validation
  failures during deployment rather than only for post-deployment
  troubleshooting.
- **RBAC layering self-check.** Practice explicitly tracing a specific
  administrative action (creating a workload domain, modifying a
  certificate) through which RBAC layer(s) actually gate it — SDDC
  Manager's own role assignment, and potentially the underlying
  component's RBAC as well — rather than assuming a single unified
  permission model.
- **Import-path rehearsal.** In a lab, attempt importing an existing
  standalone vCenter Server (built using Chapters 2–3's methods) into
  fleet management, and note every prerequisite validation step
  encountered — this is difficult to internalize from documentation
  reading alone and benefits substantially from at least one hands-on
  repetition.

## Security and Best Practices

- Register for the exam only through Broadcom's authorized testing
  partner and verify current requirements directly from official
  registration channels before exam day.
- Do not use unauthorized exam dump material; administrator-role
  competency in particular depends on genuine design judgment that
  memorized question/answer pairs cannot substitute for, since real
  deployment scenarios vary by environment in ways a fixed question bank
  cannot capture.
- Practice workload domain deployment, RBAC changes, licensing
  application, and certificate operations exclusively in isolated lab
  environments — certificate and RBAC mistakes in particular can lock an
  administrator out of production management interfaces if rehearsed
  carelessly against real infrastructure.
- Apply least-privilege discipline to lab SDDC Manager administrator
  accounts used during practice, consistent with the RBAC hardening
  guidance in Chapters 3 and 8, rather than defaulting every practice
  session to a fully privileged account.

## References and Knowledge Checks

**References**

- [Broadcom Education Services](https://www.broadcom.com/support/education/vmware) — official 2V0-17.25 exam guide (current
  blueprint domains, item count, exam duration, and candidate profile —
  verify directly before scheduling).
- [VMware Cloud Foundation Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1.html) — *SDDC Manager*, *Cloud
  Builder*, *Workload Domain Management*, *Fleet Management*,
  *Certificate Management*.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 1](01-vmware-virtualization-architecture-and-design.md) for the conceptual introduction to VCF, SDDC Manager,
  Cloud Builder, and workload domains.
- See Chapters 2, 3, and 4 for the ESXi, vCenter Server, and networking
  foundations workload domain deployment builds on.
- See [Chapter 13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) for the support-role troubleshooting perspective on
  many of these same VCF components.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain precisely where Cloud Builder's responsibility ends and SDDC
   Manager's begins, and why conflating the two is a common
   misconception.
2. What distinguishes the prerequisite validation path for importing an
   existing vCenter Server into fleet management from creating a new VI
   workload domain from freshly commissioned hosts?
3. Describe a specific administrative action and trace which RBAC
   layer(s) — SDDC Manager, vCenter Server, NSX — actually gate it.
4. Why does fleet-orchestrated certificate management introduce
   sequencing/trust-propagation considerations that single-component
   certificate replacement (Chapter 3) does not?
5. Give an example of a host-commissioning prerequisite that, if missed,
   would cause a workload domain creation to fail validation — and
   explain how you would recognize that root cause from the validation
   output.

## Hands-On Lab

**Objective:** Practice the core administrator workflow — host
commissioning prerequisites, workload domain-equivalent cluster creation,
RBAC layering, and certificate-store inspection — culminating in an
attempted import of a standalone vCenter Server into a fleet-management-
style workflow, with a deliberate prerequisite-failure negative test.

**Prerequisites**

- A lab environment with an existing, standalone vCenter Server and at
  least two ESXi hosts (built using Chapters 2 and 3), plus at least one
  additional host available for commissioning into a new workload-
  domain-style cluster.
- If SDDC Manager itself is available in the lab, use it directly for
  this exercise; if not, perform the equivalent underlying vSphere/
  PowerCLI steps as a substitute, noting explicitly which steps SDDC
  Manager would otherwise orchestrate automatically.

**Steps**

1. Verify host commissioning prerequisites on the additional host: NTP
   synchronization, DNS forward/reverse resolution, and acceptance
   level.

   ```bash
   esxcli system ntp get
   esxcli network ip dns server list
   esxcli software acceptance get
   ```

   **Expected result:** all three report correct, expected values.

2. **Negative test:** deliberately misconfigure NTP on the host (point it
   at an unreachable server) and attempt commissioning (via SDDC Manager
   if available, or by attempting to add the host to a new cluster and
   observing any time-skew-related warnings otherwise).

   **Expected result:** commissioning/validation fails or warns
   specifically on the time synchronization prerequisite, not a generic
   error — confirm the failure output names the actual root cause.

3. Correct the NTP configuration and re-verify:

   **Expected result:** the prerequisite check now passes.

4. Create a new cluster (representing a VI workload domain's compute
   layer) and add the host, enabling HA and DRS consistent with Chapter 7
   design guidance:

   ```powershell
   New-Cluster -Name "lab-wld-cluster" -Location (Get-Datacenter -Name "lab-dc") `
     -HAEnabled -DrsEnabled -DrsAutomationLevel FullyAutomated
   ```

   **Expected result:** the cluster is created and the host joins
   successfully.

5. Create a scoped RBAC role at the new cluster's folder level (not
   vCenter root) for a lab "workload domain administrator" test account,
   and confirm least-privilege scoping (the test account cannot act
   outside the new cluster).

   **Expected result:** the test account can manage the new cluster but
   is denied actions against the pre-existing standalone infrastructure —
   demonstrating the RBAC layering concept from Design Considerations.

6. Inspect the standalone vCenter Server's certificate store as
   preparation for the import-path exercise:

   ```bash
   /usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text
   ```

   **Expected result:** valid, non-expired certificate entries are
   confirmed — a prerequisite that a real fleet-management import
   workflow would also validate.

7. If SDDC Manager/fleet management is available in the lab, attempt to
   import the standalone vCenter Server; if not, document the specific
   prerequisite checks (version compatibility, certificate validity,
   configuration conformance) that would be validated, based on the
   Theory and Architecture discussion above.

   **Expected result:** either a successful import, or a clearly
   documented understanding of each prerequisite gate the import
   workflow would enforce.

8. **Cleanup:** remove the test RBAC role and account, remove the lab
   workload-domain-style cluster if created solely for this exercise, and
   restore any hosts to their prior state.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VCP-VCF Administrator (2V0-17.25) exam blueprint covers both planning/
design judgment and hands-on deploy/configure/operate competency across
workload domain deployment, fleet management, identity/RBAC, licensing,
and certificate lifecycle — distinguishing it from the support exam's
troubleshooting focus ([Chapter 13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md)) and requiring administrators to both
design and execute rather than hand off one to the other. Cloud Builder's
scope (management domain bring-up only) versus SDDC Manager's scope
(everything after, including all workload domain and day-2 lifecycle
operations) is a foundational distinction, and RBAC/certificate
management at the fleet-orchestration layer extends — but is not
identical to — the per-component concepts covered in Chapters 3 and 8.
Hands-on rehearsal of host commissioning prerequisites, workload domain
creation mechanics, RBAC layering, and the import-existing-infrastructure
workflow is the most direct preparation for this exam's dual design-and-
execution structure.

- [ ] Can explain the Cloud Builder / SDDC Manager scope boundary
      precisely.
- [ ] Can distinguish the import-existing-vCenter path from new workload
      domain creation, including differing prerequisites.
- [ ] Can trace a given administrative action through the correct RBAC
      layer(s).
- [ ] Can explain why fleet-orchestrated certificate management is a
      distinct workflow from single-component certificate replacement.
- [ ] Can articulate both the design rationale and execution steps for a
      workload domain deployment scenario.
- [ ] Has verified the current live exam guide against this chapter's
      summary before scheduling.
- [ ] Completed the comprehensive hands-on lab, including the
      prerequisite-failure negative test and cleanup.
