# Chapter 04: Enterprise Identity and Directory Services

![Lab topology for this chapter: a Linux VM discovers and joins the example.com Active Directory domain using realmd/sssd/adcli with the svc-joiner account, then restricts interactive login to the linux-admins@example.com group; jdoe@example.com, a group member, resolves identity and obtains a Kerberos ticket successfully. Separately, a GPO named 'Lab Baseline' is created and linked to OU=Windows,OU=Servers,DC=example,DC=com; a Windows Server VM in that OU applies the policy after gpupdate /force. As a negative test, an AD user who is not a member of linux-admins is refused interactive login to the Linux host, while jdoe@example.com logs in successfully.](../../../diagrams/volume-04-enterprise-systems-administration/chapter-04-ad-domain-join-gpo-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: one Active Directory domain governing both a group-restricted Linux login and a GPO applied to a Windows Server in the same OU.*

## Learning Objectives

- Explain Active Directory Domain Services (AD DS) architecture: forests,
  domains, organizational units, trusts, sites, and replication.
- Describe how Kerberos and LDAP function as the authentication and
  directory-access protocols underneath AD DS and most enterprise identity
  systems.
- Design and apply Group Policy to enforce configuration at scale.
- Join Linux hosts to Active Directory and integrate them with centralized
  identity using SSSD or realmd.
- Explain hybrid identity concepts (on-premises AD synchronized to a
  cloud identity provider) at an architectural level.
- Identify the FSMO roles and site/replication topology decisions that
  keep a multi-site directory healthy.

## Theory and Architecture

Enterprise identity is the control plane that both Windows Server
([Chapter 03](03-windows-server-administration.md)) and Linux ([Chapter 02](02-enterprise-linux-administration.md)) administration ultimately depend on:
almost every access-control decision in this volume — who can log in to a
host, who can approve a change, which service account a scheduled task
runs as — traces back to a directory service. This chapter covers Active
Directory Domain Services as the dominant enterprise directory, the
protocols it is built on, and how Linux systems integrate with it,
alongside a brief look at hybrid and cloud-federated identity.

### Active Directory Domain Services structure

AD DS organizes identity into a hierarchy:

- **Forest** — the security boundary. A forest contains one or more
  domains that share a common schema, configuration partition, and Global
  Catalog.
- **Domain** — a partition of the forest with its own domain-naming
  context; hosts and users are joined to a specific domain.
- **Organizational Unit (OU)** — a container within a domain used to
  organize objects and scope Group Policy and delegated administration.
  OUs are an administrative construct, not a security boundary.
- **Trust** — a relationship that allows authentication to flow between
  domains or forests (one-way, two-way, transitive, or external).
- **Site** — a construct mapped to physical network topology (typically
  one site per data center/office) used to control which domain
  controller a client authenticates against and how replication traffic
  flows between locations.

```text
Forest: example.com
├── Domain: example.com
│   ├── OU: Servers
│   │   ├── OU: Linux
│   │   └── OU: Windows
│   ├── OU: Workstations
│   └── OU: Service Accounts
└── Domain: emea.example.com   (child domain, transitive trust to parent)
```

### FSMO roles

Within a forest and domain, five Flexible Single Master Operations (FSMO)
roles are each held by exactly one domain controller at a time, because
the underlying operation cannot be safely multi-mastered:

| Role | Scope | Function |
| --- | --- | --- |
| Schema Master | Forest | Controls schema modifications |
| Domain Naming Master | Forest | Controls addition/removal of domains |
| RID Master | Domain | Allocates relative ID pools for new security principals |
| PDC Emulator | Domain | Time synchronization source, password-change authority, GPO conflict handling |
| Infrastructure Master | Domain | Maintains cross-domain object references |

Losing a FSMO role holder does not stop authentication (most AD functions
are multi-master), but it does stop the specific operation that role
controls — a lost RID Master, for example, eventually prevents new object
creation once the last domain controller's cached RID pool is exhausted.

### Kerberos and LDAP

- **Kerberos** is the default authentication protocol. A client obtains a
  Ticket-Granting Ticket (TGT) from the Key Distribution Center (KDC —
  co-located with every domain controller), then requests service tickets
  for specific resources without re-sending credentials. Kerberos is
  time-sensitive: clock skew beyond the default five-minute tolerance
  causes authentication failures, which is why the PDC Emulator's time
  authority matters operationally.
- **LDAP** (Lightweight Directory Access Protocol) is the query and
  read/write protocol for directory objects. AD DS exposes LDAP on port
  389 (and LDAPS/636 for TLS-protected access), and it is the protocol
  Linux identity integration tools speak to read user and group objects.

### Group Policy

Group Policy Objects (GPOs) apply configuration to computers and users
based on their OU, site, or domain membership, following a documented
precedence order — Local, Site, Domain, OU (LSDOU) — with the closest
(most specific) GPO winning on conflict unless a parent GPO is enforced.
Group Policy is the primary mechanism for applying the security and
configuration baselines discussed in [Chapter 08](08-systems-security-automation-and-compliance.md) across a Windows fleet.

### Linux integration with Active Directory

Linux hosts join an AD domain to use centralized identity rather than
maintaining local `/etc/passwd` accounts. The standard modern integration
path uses **SSSD** (System Security Services Daemon) with **realmd** as
the discovery/enrollment front end:

```text
Linux host                          Active Directory
+-----------+  realmd/adcli join   +------------------+
|  realmd   | --------------------> | Domain Controller|
+-----------+                       +------------------+
      |
      v
+-----------+   Kerberos/LDAP lookups
|   SSSD    | <----------------------------------------+
+-----------+
      |
      v
  NSS / PAM  (id, getent passwd, login)
```

The older Winbind/Samba integration path (presenting AD accounts through
NSS/PAM via a Samba-managed connection) still exists for legacy
environments but SSSD is the current, actively maintained standard and
the one assumed by RHEL 10 and Ubuntu 26.04 LTS.

### Hybrid and cloud-federated identity

Most enterprises now synchronize on-premises AD DS to a cloud identity
provider (Microsoft Entra ID or an equivalent) using a directory-sync
agent, enabling single sign-on to SaaS applications while retaining AD as
the on-premises authority. Architecturally, this adds a synchronization
and federation layer on top of everything above; it does not replace
Kerberos/LDAP for on-premises resource authentication. Cloud-provider-
specific identity services (AWS IAM Identity Center, and similar) are
covered in their respective volumes.

## Design Considerations

- **Forest and domain count.** A single forest, single domain design is
  the right default for most enterprises; additional domains or forests
  add administrative overhead and should be justified by a genuine
  security or regulatory boundary (an entirely separate company acquired
  through M&A, for example), not by organizational chart mirroring.
- **OU design for delegation, not organization chart mirroring.** Design
  OU structure around what needs distinct Group Policy application or
  delegated administration, not around the company's reporting structure.
- **Site topology accuracy.** Sites must reflect actual network topology
  and link cost, or clients will authenticate against a distant domain
  controller across a slow WAN link instead of a local one, and
  replication schedules will not match available bandwidth.
- **Tiered administration model.** Separate credentials for workstation
  administration, server administration, and domain-controller/Tier-0
  administration (Microsoft's tiered administration model) so that
  compromising a workstation-admin credential cannot escalate to domain
  compromise.
- **Linux join method at scale.** Decide whether Linux hosts join AD
  individually (`realm join`, requiring a privileged one-time credential
  per host) or through a pre-provisioned computer-object/keytab pattern
  suitable for automated image builds — the latter scales far better for
  golden-image pipelines ([Chapter 06](06-configuration-software-and-patch-management.md)).
- **Group Policy sprawl.** Every additional GPO adds processing time at
  logon/boot and a place for conflicting settings to hide. Consolidate
  related settings into fewer, well-documented GPOs rather than one GPO
  per setting.

## Implementation and Automation

### Querying AD DS with PowerShell

```powershell
# Requires the RSAT Active Directory module (RSAT-AD-PowerShell feature).
Get-ADDomain | Select-Object DNSRoot, DomainMode, PDCEmulator

Get-ADDomainController -Filter * |
    Select-Object Name, Site, OperationMasterRoles

# Create an OU structure and a scoped service account (used later for a
# gMSA-backed scheduled task, as introduced in Chapter 03).
New-ADOrganizationalUnit -Name 'Linux' -Path 'OU=Servers,DC=example,DC=com'

New-ADServiceAccount -Name 'svc-appmon' -DNSHostName 'appmon.example.com' `
    -PrincipalsAllowedToRetrieveManagedPassword 'App-Servers'
```

### Joining a Linux host to Active Directory

```bash
# Discover the domain, then join it. realmd wraps adcli/sssd
# configuration so a single command performs discovery, Kerberos
# enrollment, and SSSD configuration.
sudo dnf install -y realmd sssd adcli krb5-workstation oddjob-mkhomedir \
  # Debian/Ubuntu equivalent: sudo apt install realmd sssd adcli \
  #   krb5-user oddjob-mkhomedir

sudo realm discover example.com

sudo realm join --user=svc-joiner example.com

# Restrict interactive login to a specific AD group rather than every
# domain user.
sudo realm permit -g 'linux-admins@example.com'
```

```ini
# /etc/sssd/sssd.conf (key settings realmd generates; shown for
# clarity — edit through realm/authselect tooling rather than by hand
# where possible).
[sssd]
domains = example.com
services = nss, pam

[domain/example.com]
id_provider = ad
access_provider = ad
override_homedir = /home/%d/%u
```

```bash
sudo systemctl restart sssd
id 'jdoe@example.com'
getent passwd 'jdoe@example.com'
```

### Group Policy authoring

```powershell
# Create a GPO, link it to the Linux/Windows server OU split, and set a
# security-relevant registry preference (screen-lock timeout) as an
# example of configuration delivered through Group Policy.
New-GPO -Name 'Server Baseline - Screen Lock' |
    New-GPLink -Target 'OU=Windows,OU=Servers,DC=example,DC=com'

Set-GPRegistryValue -Name 'Server Baseline - Screen Lock' `
    -Key 'HKLM\Software\Policies\Microsoft\Windows\Control Panel\Desktop' `
    -ValueName 'InactivityTimeoutSecs' -Type DWord -Value 900
```

### Verifying replication health

```powershell
# Run on a domain controller or a workstation with RSAT AD DS tools.
repadmin /replsummary
repadmin /showrepl * /csv | ConvertFrom-Csv | 
    Where-Object 'Number of Failures' -gt 0
```

## Validation and Troubleshooting

- Confirm Kerberos time sync tolerance: `w32tm /query /status` on
  Windows, `chronyc tracking` or `timedatectl` on Linux — both should be
  within a few seconds of the domain's authoritative time source (the PDC
  Emulator).
- Confirm a Linux host's domain trust: `realm list` should show the
  domain with `configured: kerberos-member`, and `kinit jdoe@EXAMPLE.COM`
  followed by `klist` should return a valid ticket.
- Confirm Group Policy application: `gpresult /r` (or
  `Get-GPResultantSetOfPolicy` for a report) on the target Windows host
  shows the expected GPO in the "Applied Group Policy Objects" list, not
  the "Denied" list.
- Confirm replication health across sites: `repadmin /replsummary`
  should show zero failures; persistent failures indicate a network,
  firewall, or DNS issue between sites.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Kerberos authentication fails intermittently | Clock skew beyond tolerance | Compare `w32tm /query /status` / `chronyc tracking` against the PDC Emulator |
| Linux `id` returns local user only, not AD user | SSSD not running or misconfigured | `systemctl status sssd`; `sudo sssctl domain-status example.com` |
| GPO setting not applied on a specific host | GPO linked to the wrong OU, or a security filter/WMI filter excludes the host | `gpresult /r` "Denied GPOs" section |
| New user cannot be created anywhere in the domain | RID pool exhausted and RID Master unreachable | `dcdiag /test:ridmanager`; confirm RID Master role holder is online |
| Site-to-site replication backlog growing | Site link cost/schedule misconfigured, or WAN link down | `repadmin /replsummary`; check site link schedule against actual link availability |

## Security and Best Practices

- Apply a tiered administration model: Tier 0 (domain controllers, PKI),
  Tier 1 (servers), Tier 2 (workstations) with no credential reuse across
  tiers, and use Privileged Access Workstations for Tier 0 administration.
- Prefer Group Managed Service Accounts over manually managed service
  account passwords wherever the consuming application supports gMSA
  (Chapter 03).
- Restrict which AD groups may interactively log on to Linux hosts with
  `realm permit -g`, rather than permitting the entire domain by default.
- Enable LDAP signing and channel binding, and disable unauthenticated
  LDAP binds, to prevent credential relay attacks against the directory.
- Monitor and alert on FSMO role holder availability and AD replication
  health as a standing operational control, not only during an incident.
- Enforce the principle of least privilege in OU delegation: grant
  specific permissions (reset password, unlock account) rather than
  delegating full control of an OU.
- Regularly audit privileged group membership (Domain Admins, Enterprise
  Admins, Schema Admins) and remove standing membership in favor of
  just-in-time elevation where a Privileged Access Management solution is
  available.

## References and Knowledge Checks

**References**

- [Microsoft Learn: "Active Directory Domain Services Overview" and
  "Understanding FSMO Roles in Active Directory."](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-fsmo-roles)
- [Microsoft Learn: "Group Policy Overview" and "How Core Group Policy
  Works."](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-overview)
- RFC 4511 (LDAP: The Protocol) and RFC 4120 (Kerberos Network
  Authentication Service V5).
- [Red Hat documentation: "Integrating RHEL Systems Directly with Windows
  Active Directory" (SSSD/realmd).](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/integrating_rhel_systems_directly_with_windows_active_directory/connecting-rhel-systems-directly-to-ad-using-sssd)
- [Microsoft Learn: "Group Managed Service Accounts Overview."](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview)

**Knowledge Checks**

1. What is the difference between a domain, a forest, and an OU, and
   which of the three is a genuine security boundary?
2. Which FSMO role, if unavailable for an extended period, eventually
   prevents new object creation in a domain?
3. Why does Kerberos authentication depend on accurate time
   synchronization?
4. What is the difference between the SSSD/realmd integration path and
   the legacy Winbind path for joining Linux to Active Directory?
5. Why is a tiered administration model (Tier 0/1/2) recommended, and
   what does it prevent?

## Hands-On Lab

**Objective:** Join a Linux host to an existing Active Directory domain,
restrict interactive login to a specific group, apply a Group Policy
setting to a Windows server in the same OU, and validate both.

### Prerequisites

- A functioning Active Directory domain with at least one domain
  controller (this lab assumes `example.com`; substitute your lab
  domain).
- One Linux VM not yet joined to the domain, with DNS pointed at the
  domain's DNS servers and network connectivity to a domain controller.
- One Windows Server VM already domain-joined, located in (or moved to)
  an OU you control, such as `OU=Windows,OU=Servers`.
- An AD account with permission to join computers to the domain
  (`svc-joiner` in the examples), and RSAT AD DS/Group Policy tools
  available on an administrative workstation.

### Procedure

1. On the Linux VM, install the required packages and discover the
   domain:

   ```bash
   sudo dnf install -y realmd sssd adcli krb5-workstation oddjob-mkhomedir
   sudo realm discover example.com
   ```

   **Expected result:** output shows `example.com` with
   `type: kerberos` and `server-software: active-directory`.

2. Join the domain:

   ```bash
   sudo realm join --user=svc-joiner example.com
   ```

   **Expected result:** the command completes without error; a computer
   object for this host now exists in AD (verify with
   `Get-ADComputer <hostname>` from an administrative workstation).

3. Restrict interactive login to a specific group:

   ```bash
   sudo realm permit -g 'linux-admins@example.com'
   ```

4. Confirm identity resolution and authentication:

   ```bash
   id 'jdoe@example.com'
   kinit 'jdoe@example.com'
   klist
   ```

   **Expected result:** `id` resolves UID/GID information from AD, and
   `klist` shows a valid Kerberos ticket for `jdoe@EXAMPLE.COM`.

5. On an administrative workstation, create a GPO and link it to the OU
   containing the Windows Server VM:

   ```powershell
   New-GPO -Name 'Lab Baseline' |
       New-GPLink -Target 'OU=Windows,OU=Servers,DC=example,DC=com'

   Set-GPRegistryValue -Name 'Lab Baseline' `
       -Key 'HKLM\Software\Policies\Microsoft\Windows\Control Panel\Desktop' `
       -ValueName 'InactivityTimeoutSecs' -Type DWord -Value 900
   ```

6. On the Windows Server VM, force policy refresh and confirm
   application:

   ```powershell
   gpupdate /force
   gpresult /r
   ```

   **Expected result:** `Lab Baseline` appears under "Applied Group
   Policy Objects."

### Negative Test

Attempt to log in interactively to the Linux VM as an AD user who is
**not** a member of `linux-admins` (for example, over SSH with password
authentication, or `su - otheruser@example.com` if using a shared
console). The login should be refused, confirming `realm permit -g`
correctly restricts access rather than merely documenting an intended
restriction. Then confirm `jdoe@example.com` (a member of
`linux-admins`) can log in successfully.

### Cleanup

```bash
# On the Linux VM: leave the domain and remove SSSD state.
sudo realm leave example.com
sudo rm -rf /var/lib/sss/db/*
```

```powershell
# From an administrative workstation: remove the GPO link and the GPO,
# and remove the stale Linux computer object if it was not cleaned up
# automatically by realm leave.
Remove-GPLink -Name 'Lab Baseline' -Target 'OU=Windows,OU=Servers,DC=example,DC=com'
Remove-GPO -Name 'Lab Baseline'
Get-ADComputer -Filter "Name -eq '<linux-hostname>'" | Remove-ADObject -Recursive -Confirm:$true
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Active Directory Domain Services is the identity backbone this volume's
Windows and Linux administration chapters both depend on: forests,
domains, and OUs provide structure; FSMO roles handle operations that
cannot be multi-mastered; Kerberos and LDAP provide authentication and
directory access; Group Policy delivers configuration at scale; and SSSD/
realmd extend that same identity fabric to Linux hosts. Hybrid identity
extends the same on-premises authority to cloud and SaaS access without
replacing it.

- [ ] Can explain the forest/domain/OU hierarchy and identify which
      level is a genuine security boundary.
- [ ] Can name all five FSMO roles and the operational impact of losing
      each one.
- [ ] Can join a Linux host to Active Directory with SSSD/realmd and
      restrict interactive login to a specific group.
- [ ] Can create, link, and verify application of a Group Policy Object.
- [ ] Completed the hands-on lab, including the negative login-
      restriction test.
