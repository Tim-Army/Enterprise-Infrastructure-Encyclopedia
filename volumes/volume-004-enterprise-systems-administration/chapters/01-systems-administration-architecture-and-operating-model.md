# Chapter 01: Systems Administration Architecture and Operating Model

![Lab topology for this chapter: the administrator workstation's SSH config routes all access to web01 through bastion01 via ProxyJump, using a dedicated lab key; web01's hosts.allow/hosts.deny restrict sshd to only accept connections from bastion01's address (10.0.0.10). A simple inventory-drift check compares a static inventory file (web01, web02) against hosts that actually respond: web01 is OK, web02 is flagged as DRIFT because it does not exist. As a negative test, a direct connection attempt to web01 that bypasses bastion01 times out or is refused, confirming the management-plane control is enforced at the network layer, not by convention.](../../../diagrams/volume-004-enterprise-systems-administration/chapter-01-bastion-mediated-access-topology.svg)

*Figure 1-1. Topology used throughout this chapter's Hands-On Lab: a bastion-mediated access pattern enforced at the network layer, plus a one-line inventory-drift check.*

## Learning Objectives

- Describe the organizational and technical operating model that enterprise
  systems administration teams use to run mixed Linux and Windows Server
  fleets at scale.
- Differentiate centralized, federated, and platform-team operating models
  and identify when each is appropriate.
- Map ITIL-aligned service management processes (incident, problem, change,
  request) to the day-to-day work of a systems administrator.
- Explain the role of a management plane — jump hosts, out-of-band access,
  configuration management, and monitoring — in a cross-platform estate.
- Identify the tooling categories every enterprise administration function
  depends on and how they interact.
- Design a tiered support and escalation model with defined service levels.
- Build a documentation and runbook discipline that scales beyond a single
  administrator's institutional knowledge.

## Theory and Architecture

Enterprise systems administration is the discipline of operating the
compute, identity, storage, and service layers that sit beneath
applications — servers, operating systems, directory services, patching,
and the automation that ties them together. Unlike a single-server
"sysadmin" role, enterprise administration is a coordinated operating
model spanning hundreds or thousands of Linux and Windows Server hosts
across data centers, colocation facilities, and cloud regions. This volume
establishes the cross-platform foundation; distribution- and
vendor-specific depth (Red Hat Enterprise Linux 10, Ubuntu Server
26.04 LTS, VMware, and the hardware management platforms) is covered in
their dedicated volumes later in this encyclopedia.

### The three operating models

Enterprise organizations typically run administration under one of three
structures:

- **Centralized.** A single systems administration team owns every host,
  regardless of business unit or application. This model maximizes
  standardization and audit consistency but can become a bottleneck as
  request volume grows.
- **Federated.** A central team owns platform standards (golden images,
  patch cadence, identity integration) while embedded administrators inside
  business units or application teams operate day-to-day. This model scales
  request throughput but requires strong governance to prevent
  configuration drift between business units.
- **Platform team / infrastructure-as-a-service.** The administration team
  exposes self-service provisioning (via a service catalog, Infrastructure
  as Code, or a private cloud portal) and owns the underlying platform,
  while consumers request compute rather than filing tickets against a
  human queue. This model is the end state most enterprises converge toward
  as automation maturity increases, and it is the model assumed by later
  automation-focused volumes ([Volume IX](../../volume-009-infrastructure-automation/README.md), Infrastructure Automation).

Most enterprises run a hybrid: a platform team owns the automation and
image pipeline, a federated model handles application-specific tuning, and
a centralized security/compliance function enforces baseline policy across
all of it.

### The management plane

Regardless of operating model, every enterprise fleet depends on a
**management plane** — the set of systems administrators use to reach,
configure, and observe the **workload plane** (the servers actually running
business applications). A mature management plane includes:

- **Bastion/jump hosts** — hardened, heavily audited hosts that broker SSH
  and RDP access into production networks, so administrator workstations
  never connect directly to production hosts.
- **Out-of-band (OOB) management** — iDRAC, iLO, or equivalent baseboard
  management controllers (BMCs) that provide console and power control
  independent of the host operating system. Covered in depth in
  [Volume XXII](../../volume-022-dell-openmanage-enterprise/README.md) (Dell OpenManage Enterprise) and [Volume XXIII](../../volume-023-dell-idrac-9-10-administration/README.md) (Dell iDRAC).
- **Configuration management control plane** — the Ansible control node,
  Puppet server, Chef server, or Windows Server DSC pull server that pushes
  and enforces desired state ([Chapter 06](06-configuration-software-and-patch-management.md)).
- **Centralized identity** — Active Directory, LDAP, or a federated
  identity provider that both platforms authenticate against ([Chapter 04](04-enterprise-identity-and-directory-services.md)).
- **Monitoring and log aggregation** — the telemetry pipeline that gives the
  team visibility before a customer notices an outage ([Chapter 09](09-monitoring-troubleshooting-and-lifecycle-operations.md); deep
  dive in [Volume XI](../../volume-011-observability-enterprise-operations/README.md)).
- **Ticketing and CMDB** — the system of record for requests, incidents,
  and the configuration items (CIs) that make up the fleet.

```text
                     +---------------------+
                     |   Identity / AD     |
                     |  (Chapter 04)       |
                     +----------+----------+
                                |
  Admin Workstation             |
        |                       |
        v                       v
   +---------+   SSH/RDP   +---------+   push/pull   +------------------+
   | Bastion | <---------> | Jump/PAM| <-----------> | Config Mgmt CP   |
   +---------+             +---------+                | (Ansible/DSC)   |
                                |                       +---------+--------+
                                v                                 |
                        +----------------+                        v
                        | Linux fleet    | <----- desired state -+
                        | Windows fleet  |
                        | (workload plane)|
                        +--------+-------+
                                 |
                                 v
                        +----------------+
                        | Monitoring /   |
                        | Log aggregation|
                        | (Chapter 09)   |
                        +----------------+
```

### ITIL-aligned process model

Enterprise administration teams generally structure work around four ITIL
service-management processes, even when the organization does not run a
formal ITIL practice:

| Process | Purpose | Typical SLA driver |
| --- | --- | --- |
| Incident management | Restore service after an unplanned interruption | Time to restore, by severity |
| Problem management | Find and eliminate the root cause behind recurring incidents | Mean time between recurrence |
| Change management | Control the introduction of planned modifications | Change failure rate |
| Request fulfillment | Handle routine, pre-approved asks (new account, disk expansion) | Time to fulfill |

Systems administrators sit at the intersection of all four: they execute
changes, respond to incidents, feed root-cause data into problem records,
and fulfill day-to-day requests, usually through the same ticketing and
change-approval tooling that governs the rest of IT.

## Design Considerations

- **Blast radius vs. throughput.** Centralized models reduce blast radius
  (one team, one standard) but slow throughput. Federated and platform
  models trade some standardization for speed; the platform team model
  minimizes the trade-off through automation and guardrails rather than
  manual review.
- **Standardization boundary.** Decide explicitly what must be identical
  across every host (patch baseline, logging agent, identity source,
  firewall default) versus what teams may customize (application runtime
  versions, non-privileged package sets). Publish this boundary; do not
  leave it implicit.
- **Change windows and freeze periods.** Cross-platform fleets must
  coordinate Linux and Windows patch cycles against the same business
  calendar (quarter-end freezes, retail peak-season freezes) even though
  the platforms patch on different cadences ([Chapter 06](06-configuration-software-and-patch-management.md)).
- **Segregation of duties.** Administrators who can approve a change should
  generally not be the sole approver of their own change in regulated
  environments (PCI DSS, SOX). Build this into the change-management
  workflow rather than relying on informal review.
- **Tooling sprawl.** Every additional point tool (a second ticketing
  system, a one-off monitoring agent) adds an integration and an audit
  surface. Favor platforms that integrate with the existing identity and
  observability stack over best-of-breed tools that do not.
- **On-call sustainability.** A tiered support model (below) only works if
  each tier has a documented escalation path and realistic staffing;
  design the rotation before the incident volume forces one on you.

### Tiered support model

| Tier | Scope | Typical response |
| --- | --- | --- |
| Tier 1 | Service desk triage, password resets, known-error workarounds from the knowledge base | Minutes, 24x7 |
| Tier 2 | Systems administrators — service restarts, standard remediation, request fulfillment | Within SLA, business hours or on-call |
| Tier 3 | Senior/platform engineers — root-cause analysis, vendor escalation, architecture changes | Escalation only |
| Vendor | Vendor support (Microsoft, Red Hat, Canonical, hardware OEM) | Contractual SLA |

## Implementation and Automation

A documented operating model is only useful if it is enforced by tooling,
not just policy. The following patterns implement the architecture above.

### Standardize remote access through a bastion

```bash
# Linux administrator workstation: SSH config that forces all production
# traffic through the bastion using ProxyJump (OpenSSH 7.3+).
cat >> ~/.ssh/config <<'EOF'
Host bastion
    HostName bastion.example.internal
    User admin.jdoe
    IdentityFile ~/.ssh/id_ed25519_prod

Host 10.20.*.*
    ProxyJump bastion
    User admin.jdoe
    IdentityFile ~/.ssh/id_ed25519_prod
EOF
```

```powershell
# Windows administrator workstation: PowerShell remoting through a
# hardened jump host (PowerShell 7.4+, WinRM over HTTPS).
$jumpHost   = 'jump01.example.internal'
$targetHost = 'winsrv12.example.internal'

$jumpSession = New-PSSession -ComputerName $jumpHost -UseSSL `
    -Credential (Get-Credential 'EXAMPLE\admin.jdoe')

Invoke-Command -Session $jumpSession -ScriptBlock {
    param($Target)
    Invoke-Command -ComputerName $Target -UseSSL -ScriptBlock {
        Get-Service -Name 'W32Time'
    }
} -ArgumentList $targetHost
```

### Track the fleet as configuration items

Treat every host as a configuration item (CI) in a CMDB or inventory
source of truth. Configuration management tools should read from this
inventory rather than maintaining a second, divergent host list:

```yaml
# ansible/inventory/production.yml — grouped by platform and role,
# consumed by both the config-management control plane and the
# monitoring stack's service-discovery job.
all:
  children:
    linux_web:
      hosts:
        web-lnx-[01:04].example.internal:
    windows_app:
      hosts:
        app-win-[01:02].example.internal:
    linux_db:
      hosts:
        db-lnx-[01:02].example.internal:
  vars:
    ansible_user: svc.ansible
    environment: production
```

### Enforce change management in the pipeline

```bash
# Pre-change hook example: block a config-management run outside an
# approved change window unless an emergency-change tag is present.
change_id="${CHANGE_ID:?CHANGE_ID is required}"
if ! curl -sf "https://cmdb.example.internal/api/changes/${change_id}" \
     | jq -e '.status == "approved"' >/dev/null; then
  echo "Change ${change_id} is not approved. Aborting run." >&2
  exit 1
fi
```

Wire this check into the CI/CD pipeline or Ansible/DSC job runner so that
no configuration change reaches production without a linked, approved
change record — this is the control that most audit frameworks (SOC 2,
ISO 27001, PCI DSS) require evidence of.

## Validation and Troubleshooting

- **Verify bastion enforcement.** Attempt a direct connection to a
  production host from outside the bastion path; it should be rejected at
  the network or security-group layer, not merely discouraged by policy.
- **Verify CMDB/inventory accuracy.** Reconcile the configuration
  management inventory against actual running hosts on a schedule
  (`ansible-inventory --graph` compared to a cloud/hypervisor host list, or
  `Get-ADComputer -Filter *` against the same). Drift between the two is
  the leading cause of "unmanaged" hosts that miss patch and monitoring
  coverage.
- **Verify change-gate enforcement.** Submit a deliberately unapproved
  change through the pipeline in a non-production environment and confirm
  it is blocked — this is the negative test for the control above.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Host missing from monitoring | Inventory drift or agent not bootstrapped at provisioning | Compare CMDB/inventory to monitoring target list |
| Change applied without an approved ticket | Pipeline gate misconfigured or bypassed with direct access | Audit pipeline logs and bastion session logs for the time window |
| Escalation stalls between Tier 1 and Tier 2 | No documented ownership for the affected service in the CMDB | Confirm service-to-team mapping is current |
| Two teams maintain conflicting configuration for the same host | Federated model without a published standardization boundary | Review and republish the standardization boundary (Design Considerations) |

## Security and Best Practices

- Require multi-factor authentication (MFA) at the bastion/jump host, not
  just at the identity provider's web portal — this is the single highest-
  leverage control in the management plane.
- Log and retain full session recordings (`script`, `asciinema`, or a
  privileged-access-management product) for bastion sessions; most
  compliance frameworks require this for privileged access.
- Apply least privilege to the configuration-management control plane
  itself: the Ansible control node or DSC pull server is a high-value
  target because compromising it compromises every host it manages.
- Separate the identity used for interactive administrator login from the
  service account used by automation; rotate and vault both.
- Keep the standardization boundary and escalation model as living
  documents in version control alongside the automation code, not as
  static slide decks that go stale.
- Review the tiered support model's staffing and escalation paths at least
  annually, and after every major incident postmortem.

## References and Knowledge Checks

**References**

- [ITIL 4 Foundation (AXELOS/PeopleCert)](https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil-4-foundation-2565) — service management process
  definitions referenced above.
- [NIST SP 800-53 Rev. 5, control family CM (Configuration Management) and
  AC (Access Control).](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [Microsoft Learn: "Privileged Access Workstations" and "Windows Admin
  Center" documentation.](https://learn.microsoft.com/en-us/security/privileged-access-workstations/)
- [Red Hat and Canonical enterprise administration guides (see Volume XIV
  and Volume XXI for distribution-specific references).](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10)

**Knowledge Checks**

1. What distinguishes a federated operating model from a platform-team
   operating model?
2. Name the four ITIL processes most directly executed by systems
   administrators, and give one example task for each.
3. Why should the identity used for interactive administrator access be
   separate from the service account used by automation?
4. What is the purpose of a bastion/jump host, and what control makes it
   effective rather than a false sense of security?
5. How would you detect inventory drift between a configuration management
   system and the actual running fleet?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each element of the systems-administration
operating model** — the administrative model, cross-platform inventory, standardization, and change/
access discipline. This volume is cross-platform, so labs span Linux and Windows. Each ends **`**Lab
verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 1.1–1.4** — a Linux host (CLI) and, where noted, a Windows Server
(PowerShell). **Cost:** none.

### Lab 1.1 — The administrative operating model (Topic: Operating model)

**Objective:** Define roles, least privilege, and runbooks for a service.

```text
# For a managed service, write down:
#   - roles: who administers, who operates, who audits (separation of duties)
#   - access: least-privilege accounts (no shared root/Administrator), break-glass procedure
#   - runbooks: the documented procedures for routine + emergency tasks
#   - change: how changes are proposed, reviewed, and recorded
```

**Expected result:** an operating model naming roles, least-privilege access, runbooks, and change
process — systems administration at scale is a *discipline*, not ad-hoc fixes: defined roles,
least-privilege access, and documented runbooks make operations repeatable, auditable, and safe.

**Negative test:** run everything as shared root/Administrator with tribal knowledge and no runbooks;
access is un-attributable and procedures live in one person's head — the operating model is what makes
administration sustainable and auditable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Cross-platform inventory (Topic: Inventory)

**Objective:** Capture a host's identity on either platform.

```bash
# Linux:
hostnamectl ; uname -a ; cat /etc/os-release | grep PRETTY
```

```powershell
# Windows (PowerShell):
Get-ComputerInfo -Property CsName,OsName,OsVersion,OsArchitecture
```

**Expected result:** each host reports its name, OS, and version — an accurate inventory (OS,
version, role, owner) is the foundation of administration: you cannot patch, secure, or troubleshoot
what you have not inventoried, and cross-platform estates need consistent facts from both Linux and
Windows.

**Negative test:** manage an estate with no inventory; you miss unpatched or unknown hosts — an
authoritative inventory (ideally automated) is the prerequisite for every other discipline.

**Rollback:** none (read-only).

### Lab 1.3 — Standardization and baselines (Topic: Standardization)

**Objective:** Reason about golden images and configuration baselines.

```text
# Define the standard build for a server role (web/app/db):
#   - a golden image / base install with the org's hardening + agents pre-applied
#   - a configuration baseline (packages, settings, users) enforced by config management
#   - a naming/tagging convention so every host is identifiable and grouped
```

**Expected result:** a standard build and enforced baseline per role — standardization (golden images plus
config-management-enforced baselines) makes hosts consistent, so they are predictable to operate,
patch, and troubleshoot; each snowflake host is a liability.

**Negative test:** build each server by hand differently; troubleshooting and patching become
per-host guesswork — a standard baseline makes the fleet uniform and manageable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.4 — Change and access discipline (Topic: Governance)

**Objective:** Ensure changes are attributable and access is controlled.

```bash
# Linux: named admins escalate via sudo (logged), no direct root login
grep -E "PermitRootLogin" /etc/ssh/sshd_config
sudo grep -h "sudo:" /var/log/auth.log 2>/dev/null | tail -3 || journalctl _COMM=sudo -n3 --no-pager
```

**Expected result:** root login is disabled and privileged actions run via named, logged sudo — change
and access discipline means every privileged action is attributable (named accounts, logged
escalation) and changes are reviewed/recorded, so an audit can reconstruct who did what.

**Negative test:** allow shared privileged logins with no logging; when something breaks you cannot
tell who changed what — named accounts with logged escalation are what make actions attributable.

**Rollback:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter established the operating model that the rest of Volume IV
builds on: a management plane (bastion access, out-of-band management,
configuration management, identity, monitoring) that mediates
administrator access to a workload plane of Linux and Windows Server
hosts, governed by ITIL-aligned incident, problem, change, and request
processes, and executed under a deliberately chosen centralized,
federated, or platform-team structure.

- [ ] Can describe the three enterprise operating models and articulate a
      trade-off for each.
- [ ] Can diagram the management-plane components and explain what each
      one mediates.
- [ ] Can map incident, problem, change, and request management to
      concrete administrator tasks.
- [ ] Completed the hands-on lab, including the negative test proving
      direct access to the workload host is blocked.
- [ ] Understands why segregation of duties and session logging are
      required, not optional, controls for privileged access.
