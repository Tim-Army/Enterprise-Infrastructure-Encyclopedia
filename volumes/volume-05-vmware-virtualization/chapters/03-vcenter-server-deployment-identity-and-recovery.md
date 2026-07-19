# Chapter 3: vCenter Server Deployment, Identity, and Recovery

## Learning Objectives

- Explain the vCenter Server Appliance (VCSA) architecture, including its
  embedded PostgreSQL database and the deployment sizes available.
- Compare vCenter deployment topologies, including Enhanced Linked Mode,
  and explain why the external Platform Services Controller model no
  longer applies to current deployments.
- Explain the vSphere Single Sign-On (SSO) domain architecture, identity
  source types, and identity federation with an external identity
  provider.
- Deploy a VCSA using the command-line installer and a JSON configuration
  template, suitable for repeatable, scripted deployment.
- Configure vCenter High Availability (VCHA) and explain its failover
  model versus backup/restore.
- Perform a file-based backup and restore of a vCenter Server Appliance,
  and explain the recovery-time trade-offs against VCHA.
- Apply certificate management fundamentals — VMCA versus externally
  signed certificates — to a vCenter deployment.

## Theory and Architecture

vCenter Server is the centralized management plane for a vSphere
environment: the object model, authentication and authorization boundary,
task/event/alarm engine, and API surface that PowerCLI, the vSphere
Client, and every third-party integration in this volume talk to. Since
the vSphere 6.5/6.7 generation, vCenter Server ships exclusively as the
**vCenter Server Appliance (VCSA)** — a preconfigured Photon OS-based Linux
virtual appliance with an embedded **PostgreSQL** database (referred to in
VMware documentation as vPostgres) and every required service bundled in a
single deployable unit. The Windows-installable vCenter Server and the
externally deployable **Platform Services Controller (PSC)** as a separate
appliance were both removed years before the vSphere 9.x baseline; every
current deployment uses an **embedded** architecture where SSO,
certificate authority, and licensing services run inside the same
appliance as the vCenter Server service itself. Any documentation or
tooling that still references a standalone external PSC is describing a
topology that predates the current baseline and does not apply to new
deployments.

### VCSA deployment sizes

VCSA deployment is sized at install time based on expected inventory
scale, which determines the vCPU/memory/storage allocation the deployer
provisions:

| Size | Approximate inventory ceiling (hosts / powered-on VMs) | Typical fit |
| --- | --- | --- |
| Tiny | 10 / 100 | Lab, small proof-of-concept |
| Small | 100 / 1,000 | Small production environment, single site |
| Medium | 400 / 4,000 | Typical mid-size enterprise site |
| Large | 1,000 / 10,000 | Large single-vCenter environment |
| X-Large | 2,000 / 35,000 | Very large single-vCenter environment |

These figures are approximate ceilings, not hard enforcement limits, and
the deployer (both the GUI and CLI installer) uses the selected size
purely to set initial vCPU/memory/disk allocation — sizing can be revised
upward later by editing the appliance's VM compute resources, but not
downward without a redeploy. Undersizing a production vCenter is a common,
avoidable source of degraded UI responsiveness and slow task/event
processing under real inventory load; size to expected inventory at
steady state, not day-one inventory.

### Topology: Enhanced Linked Mode

A single VCSA instance manages one vCenter Server, but multiple vCenter
Server instances can be joined into **Enhanced Linked Mode (ELM)** —
sharing a single SSO domain across all joined instances so that licensing,
global permissions, tags, and a combined inventory view (across up to the
platform's supported number of linked instances) are visible from any
member's vSphere Client session, without requiring an external PSC (ELM in
the embedded-architecture model is implemented through direct
replication between embedded SSO instances). ELM does not create a single
point of management failure for the joined vCenter Servers' independent
inventories — each vCenter Server instance continues to manage its own
hosts and VMs independently; ELM's shared scope is identity, licensing,
tags, and global permissions, not inventory ownership.

### SSO domain, identity sources, and identity federation

**vSphere Single Sign-On** issues the SAML tokens that authenticate every
vCenter Server session. Every VCSA belongs to an SSO domain (named
`vsphere.local` by default, though the name is chosen at deployment time
and should not be changed casually once federated systems depend on it).
Authentication against that domain can draw from multiple **identity
source** types simultaneously:

- **vCenter Single Sign-On (local)** — the built-in local identity source,
  holding the initial administrator account (`administrator@vsphere.local`
  by default) used to bootstrap all other configuration; not intended as
  the ongoing source of day-to-day administrative identities.
- **Active Directory over LDAPS** — the common enterprise pattern,
  integrating vCenter directly with an existing AD forest for user and
  group lookups, secured with LDAPS rather than unencrypted LDAP.
- **Identity federation (OIDC)** — vCenter Server delegates authentication
  entirely to an external OpenID Connect identity provider (Okta,
  Microsoft Entra ID, VMware Workspace ONE Access, or any
  standards-compliant OIDC provider), enabling centralized MFA, conditional
  access, and single sign-on policy enforcement at the identity provider
  rather than inside vCenter itself. Identity federation is the current
  recommended pattern for organizations with mature centralized identity
  and MFA requirements, since it avoids duplicating access-policy logic
  inside vCenter's own, more limited local authentication controls.

Regardless of identity source, **role-based access control (RBAC)** —
roles, privileges, and permission assignment at specific inventory objects
— is a vCenter-native construct applied on top of whichever identity
source authenticated the user; identity source selection determines *who
can authenticate*, RBAC determines *what an authenticated identity can do*
and *where*.

### vCenter High Availability (VCHA)

**VCHA** provides automated failover for the vCenter Server Appliance
itself, using a three-node architecture:

- **Active node** — the running, serving VCSA instance under normal
  operation.
- **Passive node** — a continuously replicated standby, kept in sync with
  the active node's database and file state, ready to take over.
- **Witness node** — a lightweight quorum node (not a full VCSA replica)
  that breaks ties and prevents split-brain, analogous in role to a vSAN
  witness host.

On detected failure of the active node, the passive node promotes itself
and assumes the active node's identity (IP address and hostname), typically
completing failover within a few minutes — meaningfully faster recovery
than restoring from a file-based backup, at the cost of running (and
network-isolating, since VCHA requires a dedicated private network between
the three nodes) three appliance instances instead of one. VCHA protects
against vCenter Server appliance/VM/host failure; it does not protect
against database-level logical corruption or an administrator error that
replicates faithfully to the passive node before anyone notices — backup
and restore remains necessary even in a VCHA-protected environment for
that class of failure.

### Backup and restore

Independent of VCHA, every VCSA supports **file-based backup** — a
scheduled or on-demand backup, initiated from the VAMI (vCenter Server
Appliance Management Interface, the appliance's own administrative web UI
at port 5480) or its API, that streams a consistent backup of the
appliance's database and key configuration state to a remote target over
SCP, HTTPS, FTPS, or a supported object-storage-compatible protocol,
depending on release. Restore uses the same CLI installer used for initial
deployment, in restore mode, deploying a new appliance and rehydrating it
from the chosen backup rather than repairing an existing damaged instance
in place. File-based backup/restore has a materially longer recovery time
than VCHA failover (a new appliance must be deployed and the backup
replayed) but is the correct recovery path for logical corruption,
accidental deletion, or any scenario where the passive VCHA node's
faithfully replicated state is not actually what you want restored.

## Design Considerations

- **VCSA sizing at deployment, not as an afterthought.** Size to the
  inventory expected at steady state within the environment's planning
  horizon; resizing upward later is supported but is still a
  change-managed VM resource edit best avoided under production load
  pressure.
- **ELM scope boundaries.** Understand precisely what ELM shares (SSO
  domain, licensing, global permissions, tags, a combined inventory *view*)
  versus what remains per-vCenter-Server (actual host/VM management,
  cluster configuration, most alarms) before assuming ELM creates a single
  unified management plane — it creates a unified identity and visibility
  plane over still-independent vCenter Server instances.
- **Identity source strategy.** Active Directory over LDAPS is the
  well-understood default for organizations without a centralized OIDC
  identity provider; identity federation is the stronger choice where
  centralized MFA/conditional-access policy already exists and
  administrators want it enforced uniformly for vCenter access rather than
  configured separately inside vCenter. Do not mix strategies
  inconsistently across vCenter Server instances in the same
  organization without a clear reason — it multiplies the access-review
  burden.
- **VCHA versus backup/restore, not either/or.** VCHA answers "how fast can
  I recover from infrastructure failure of the vCenter appliance/host,"
  backup/restore answers "how do I recover from logical corruption or
  human error." Production environments with a meaningful RTO requirement
  on vCenter typically need both, not a choice between them.
- **VCHA network isolation requirement.** The VCHA private network between
  active, passive, and witness nodes must be genuinely isolated from
  general management traffic — plan a dedicated VLAN/port group for it at
  design time, not as a retrofit once VCHA deployment is already underway.
- **Certificate authority choice.** VMCA (VMware Certificate Authority,
  bundled in every VCSA) can operate as a self-signed root or be configured
  as a subordinate CA under an existing enterprise PKI; either is
  supported, but replacing VMCA-issued machine certificates with fully
  externally issued and managed certificates (VMCA is bypassed entirely)
  is also supported and preferred by some security teams needing full
  control over the certificate chain. Decide this posture before initial
  deployment where practical — retrofitting certificate architecture onto
  an already-running environment with dependent integrations is more
  disruptive than deciding it up front.
- **Backup target independence.** Store file-based vCenter backups on
  infrastructure that does not itself depend on the vCenter Server being
  backed up (a circular dependency — for example, a backup target that is
  itself a VM the vCenter being backed up manages, with no path to restore
  vCenter without vCenter already running — defeats the purpose of the
  backup).

## Implementation and Automation

### Deploying VCSA with the CLI installer and a JSON template

The VCSA installation media ships a command-line installer (`vcsa-deploy`)
alongside the GUI installer, driven by a JSON configuration template —
the correct tool for repeatable, scripted, or CI-driven vCenter
deployment.

```json
{
  "new_vcsa": {
    "esxi": {
      "hostname": "esxi01.corp.example",
      "username": "root",
      "password": "<ESXI_ROOT_PASSWORD>",
      "deployment_network": "VM Network",
      "datastore": "ds-vmfs6-tier1"
    },
    "appliance": {
      "thin_disk_mode": true,
      "deployment_option": "small",
      "name": "vcenter01"
    },
    "network": {
      "ip_family": "ipv4",
      "mode": "static",
      "system_name": "vcenter01.corp.example",
      "ip": "10.10.10.5",
      "prefix": "24",
      "gateway": "10.10.10.1",
      "dns_servers": ["10.10.10.10"]
    },
    "os": {
      "password": "<APPLIANCE_ROOT_PASSWORD>",
      "ntp_servers": "10.10.10.10,10.10.10.11",
      "ssh_enable": true
    },
    "sso": {
      "password": "<SSO_ADMINISTRATOR_PASSWORD>",
      "domain_name": "vsphere.local"
    }
  },
  "ceip": {
    "settings": {
      "ceip_enabled": false
    }
  }
}
```

```bash
# Run the CLI installer against the JSON template (deployment stage 1: deploy the OVA)
vcsa-deploy install --accept-eula --no-ssl-certificate-verification \
  vcsa-deploy-template.json
```

### Joining an Active Directory identity source over LDAPS

```powershell
# PowerCLI: add an Active Directory (LDAPS) identity source to the SSO domain
Connect-VIServer -Server vcenter01.corp.example
Add-LDAPIdentitySource -Name "corp.example" `
  -DomainName "corp.example" -DomainAlias "CORP" `
  -PrimaryUrl "ldaps://dc01.corp.example:636" `
  -BaseDNUsers "OU=Users,DC=corp,DC=example" `
  -BaseDNGroups "OU=Groups,DC=corp,DC=example" `
  -Username "svc-vcenter-ldap@corp.example" -Password "<SERVICE_ACCOUNT_PASSWORD>"
```

### Configuring identity federation with an external OIDC provider

```powershell
# PowerCLI: configure vCenter Server identity federation against an OIDC provider
New-IdentityFederationConfig -IssuerUrl "https://idp.corp.example/oauth2/default" `
  -ClientId "<OIDC_CLIENT_ID>" -ClientSecret "<OIDC_CLIENT_SECRET>" `
  -OrgId "corp-vsphere"
```

### Enabling vCenter High Availability

```powershell
# PowerCLI: configure VCHA in automatic deployment mode, letting vCenter
# clone the active node to create the passive and witness nodes
$vcha = Get-VCHAClusterConfiguration
Set-VCHAClusterMode -Mode "Enabled"

New-VCHAClusterConfiguration -DeploymentType "Automatic" `
  -PassiveNodeManagementIP "10.10.11.6" -PassiveNodeManagementSubnetMask "255.255.255.0" `
  -WitnessNodeManagementIP "10.10.11.7" -WitnessNodeManagementSubnetMask "255.255.255.0" `
  -ClusterNetworkPortGroup (Get-VirtualPortGroup -Name "pg-vcha-private") `
  -Datastore (Get-Datastore -Name "ds-vmfs6-tier1")
```

### Taking a file-based backup and restoring from it

```bash
# From the VAMI CLI shell on the appliance (or via VAMI REST API): take an
# on-demand file-based backup to a remote SFTP target
/opt/vmware/appliance/bin/backup.py \
  --location "sftp://backup01.corp.example/vcenter-backups/" \
  --username backupsvc --password '<BACKUP_TARGET_PASSWORD>' \
  --comment "Pre-upgrade backup, 2026-07-18"
```

```bash
# Restore: run the CLI installer in restore mode, pointing at the backup location
vcsa-deploy restore --accept-eula --no-ssl-certificate-verification \
  vcsa-restore-template.json
```

## Validation and Troubleshooting

- **Deployment failure triage.** `vcsa-deploy` failures write a detailed
  log under the operator's local temp directory (the CLI output names the
  exact path on failure); the two most common root causes are DNS
  resolution failure for the new appliance's forward/reverse records not
  yet existing, and NTP/time skew between the deploying ESXi host and the
  new appliance during SSO bootstrap — validate both before assuming a
  deeper platform issue.
- **SSO/identity source connectivity.** `Get-IdentitySource` (PowerCLI) or
  `vSphere Client > Administration > Single Sign On > Configuration >
  Identity Sources` reports configured sources and their test-connection
  status; an AD identity source that validates at configuration time but
  later fails authentication usually traces to the LDAPS service
  account's password expiring or a certificate trust change on the domain
  controller.
- **VCHA state and failover history.** `Get-VCHAClusterConfiguration` and
  the VAMI's VCHA status page report current cluster health (`healthy`,
  `degraded`) and node roles; a cluster stuck in `degraded` state most
  commonly indicates a witness node connectivity issue or a replication
  lag past the supported threshold, not necessarily an active-node
  problem.
- **Backup job verification.** Do not treat a scheduled backup job's "no
  error reported" status as sufficient validation — periodically perform an
  actual test restore into an isolated lab environment; a backup target
  that silently stopped receiving new backups (a full disk, an expired
  credential) is a common, otherwise undetected failure mode until the
  restore is actually needed.
- **Certificate expiration.** `vSphere Client > Administration >
  Certificate Management` (or `/usr/lib/vmware-vmafd/bin/vecs-cli entry
  list --store MACHINE_SSL_CERT --text` from the appliance shell) reports
  current certificate validity; VMCA-issued certificates and any
  externally issued replacements both require the same proactive
  expiration monitoring — a lapsed machine SSL certificate breaks nearly
  every vCenter Server API/UI interaction simultaneously.

  ```bash
  # From the appliance shell: list vCenter's certificate store entries and expiry
  /usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text
  ```

## Security and Best Practices

- Reserve `administrator@vsphere.local` (or the equivalent local SSO
  administrator account) strictly for identity-source bootstrap and
  break-glass recovery; route ongoing administrative access through named
  AD or federated identities with scoped RBAC roles, and monitor/alert on
  any login using the local SSO administrator account outside a defined
  break-glass procedure.
- Prefer identity federation with MFA enforced at the identity provider
  for any environment with a centralized IdP available; where AD over
  LDAPS is the only practical option, enforce LDAPS (not unencrypted LDAP)
  and rotate the LDAP bind service account credential on a defined
  schedule.
- Isolate the VCHA private network at the VLAN/port-group level from
  general management traffic, and restrict access to it to the three VCHA
  nodes only.
- Encrypt file-based backups in transit (the supported transport protocols
  — HTTPS/FTPS/SCP-based targets — should be configured to their
  encrypted variant, not left on an unauthenticated or cleartext path) and
  store them on a target with access control and retention independent of
  the vCenter Server environment itself.
- Establish a deliberate certificate authority posture (VMCA as
  self-signed root, VMCA as a subordinate CA under enterprise PKI, or full
  externally managed certificates) at design time, and monitor certificate
  expiration proactively rather than reactively.
- Restrict VAMI (port 5480) and SSH access on the appliance to a
  management network reachable only by authorized administrative
  workstations/jump hosts, consistent with the broader host/appliance
  hardening approach covered in Chapter 8.

## References and Knowledge Checks

**References**

- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vCenter Server Installation and
  Setup* (VCSA deployment sizes, CLI installer, JSON templates).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Platform Services* (SSO domain,
  identity sources, identity federation, Enhanced Linked Mode).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vCenter Server High Availability*.
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vCenter Server Appliance Management
  Interface (VAMI) file-based backup and restore*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 1](01-vmware-virtualization-architecture-and-design.md) for the vSphere inventory hierarchy vCenter Server manages.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for full certificate management, Lockdown Mode, and RBAC
  hardening depth.

**Knowledge checks**

1. Why does current vSphere documentation no longer describe a standalone
   external Platform Services Controller topology?
2. What specifically does Enhanced Linked Mode share across joined vCenter
   Server instances, and what does it explicitly not share?
3. Contrast the recovery-time and failure-scope characteristics of VCHA
   failover versus file-based backup/restore. Why does a production
   environment typically need both rather than choosing one?
4. What is the practical difference between an Active Directory (LDAPS)
   identity source and identity federation, in terms of where
   authentication policy (including MFA) is actually enforced?
5. Why must the VCHA private network be isolated from general management
   traffic, and what specific role does the witness node play that the
   passive node alone cannot fulfill?

## Hands-On Lab

**Objective:** Deploy a VCSA using the CLI installer against a JSON
template, configure an Active Directory identity source, take a
file-based backup, simulate appliance loss, and restore from the backup —
then validate and clean up.

**Prerequisites**

- A lab ESXi host (physical or nested) reachable by the deploying
  workstation, with sufficient free capacity for at least a "tiny"-sized
  VCSA deployment.
- The VCSA installer media (ISO) mounted or extracted on the deploying
  workstation, providing the `vcsa-deploy` CLI tool.
- Lab DNS able to resolve the new appliance's forward and reverse records,
  and lab NTP reachable from both the ESXi host and the new appliance.
- A lab Active Directory domain controller reachable over LDAPS, with a
  service account for LDAP bind.
- A remote SFTP (or supported equivalent) target reachable from the
  appliance for backup storage.

**Steps**

1. Build a JSON deployment template (adapt the example in Implementation
   and Automation) with lab-appropriate values, and deploy:

   ```bash
   vcsa-deploy install --accept-eula --no-ssl-certificate-verification \
     vcsa-deploy-lab-template.json
   ```

   **Expected result:** the installer reports successful stage 1 (OVA
   deployment) and stage 2 (appliance setup, including SSO domain
   creation) completion, and the vSphere Client is reachable at the new
   appliance's configured IP/hostname.

2. Add the lab Active Directory domain as an LDAPS identity source:

   ```powershell
   Add-LDAPIdentitySource -Name "lab.example" -DomainName "lab.example" `
     -DomainAlias "LAB" -PrimaryUrl "ldaps://dc01.lab.example:636" `
     -BaseDNUsers "OU=Users,DC=lab,DC=example" `
     -BaseDNGroups "OU=Groups,DC=lab,DC=example" `
     -Username "svc-vcenter-ldap@lab.example" -Password "<LAB_SERVICE_ACCOUNT_PASSWORD>"
   ```

   **Expected result:** the identity source appears under `Administration
   > Single Sign On > Configuration > Identity Sources` and a test login
   using a lab AD account succeeds.

3. Assign a scoped RBAC role (not Administrator) to the AD test account at
   a specific folder, and confirm least-privilege behavior:

   **Expected result:** logging in as the AD test account shows only the
   permitted scope and denies actions outside the assigned role's
   privileges.

4. Take an on-demand file-based backup to the lab SFTP target through the
   VAMI (`https://<appliance-fqdn>:5480` > Backup > Backup Now), noting the
   backup's timestamp and comment.

   **Expected result:** the backup completes successfully and a new backup
   set is visible at the SFTP target.

5. **Negative test (simulated loss):** power off and delete the deployed
   VCSA VM entirely, simulating total appliance loss.

   **Expected result:** the vSphere Client and all vCenter-dependent
   management access are now unavailable — hosts continue running
   existing VMs (ESXi does not depend on vCenter to keep already-running
   workloads up), but no centralized management, DRS, or vCenter-mediated
   HA orchestration is available until vCenter Server is restored.

6. Restore from the backup using the CLI installer in restore mode,
   pointing at the SFTP backup location and the noted backup timestamp:

   ```bash
   vcsa-deploy restore --accept-eula --no-ssl-certificate-verification \
     vcsa-restore-lab-template.json
   ```

   **Expected result:** a new appliance deploys and rehydrates from the
   backup, restoring the SSO domain, the AD identity source configuration,
   the scoped RBAC role assignment, and the prior inventory view once
   hosts reconnect.

7. Validate: confirm the AD test account can still authenticate and that
   its scoped role assignment survived the restore; confirm the original
   ESXi host(s) reconnect to the restored vCenter Server automatically or
   via `Add-VMHost` if reconnection requires re-adding.

8. **Cleanup:** remove the lab AD identity source and RBAC role
   assignment if no longer needed, delete the test backup set from the
   SFTP target, and decommission the lab VCSA if it was deployed solely
   for this exercise.

## Summary and Completion Checklist

vCenter Server ships exclusively as the VCSA, with SSO, certificate
authority, and licensing services embedded rather than split across a
separate Platform Services Controller. Deployment sizing, Enhanced Linked
Mode, and identity source selection (local SSO, Active Directory over
LDAPS, or OIDC-based identity federation) are architectural decisions made
largely at design time, while RBAC governs authorization independently of
whichever identity source authenticated a given session. VCHA and
file-based backup/restore address different failure classes —
infrastructure failure with fast automated failover versus logical
corruption or human error requiring full appliance rehydration from a
retained backup — and a production environment's recovery strategy
typically needs both rather than treating them as alternatives.

- [ ] Can describe the embedded VCSA architecture and explain why an
      external PSC no longer applies to current deployments.
- [ ] Can explain Enhanced Linked Mode's actual sharing boundary.
- [ ] Can deploy a VCSA using the CLI installer and a JSON template.
- [ ] Can configure an Active Directory (LDAPS) identity source and
      describe when identity federation is the stronger choice.
- [ ] Can configure VCHA and explain its failover model versus
      backup/restore.
- [ ] Can perform a file-based backup and a full restore from it.
- [ ] Completed the hands-on lab, including the simulated total-loss
      negative test and restore validation.
