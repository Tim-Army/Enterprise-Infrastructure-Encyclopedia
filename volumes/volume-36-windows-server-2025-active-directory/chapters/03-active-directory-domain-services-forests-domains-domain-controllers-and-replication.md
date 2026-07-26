# Chapter 03: Active Directory Domain Services — Forests, Domains, Domain Controllers, and Replication

## Learning Objectives

- Describe the AD DS logical model — forest, domain tree, domain, and the schema and partitions.
- Explain the physical model — domain controllers, the global catalog, sites, and replication.
- Install AD DS and promote the first and additional domain controllers with PowerShell.
- Identify the five FSMO roles, where they belong, and how to transfer or seize them.
- Validate replication health and diagnose common replication failures.

## Theory and Architecture

Active Directory Domain Services is a hierarchical, multi-master directory.
The **forest** is the top-level security and replication boundary: it
shares one **schema** (the definition of every object class and attribute)
and one **configuration** partition, and it is the true trust boundary in
Active Directory — everything inside a forest trusts everything else by
default. Within a forest, **domains** are administrative and replication
partitions of the directory tree; a **domain tree** is a set of domains
sharing a contiguous DNS namespace (`corp.contoso.lab`,
`emea.corp.contoso.lab`). A single-domain forest is the modern default —
extra domains add replication and trust complexity that most organizations
no longer need.

The directory is divided into **naming contexts (partitions)**: the
**schema** and **configuration** partitions replicate to every DC in the
forest; each **domain** partition replicates only to DCs in that domain;
and **application partitions** (used by AD-integrated DNS) replicate to a
chosen set. A **domain controller** hosts writable copies of these
partitions and answers authentication and directory queries. The **global
catalog** is a partial, read-only copy of every object in the forest,
letting a user log on and search forest-wide without contacting every
domain.

The **physical topology** is expressed with **sites** — collections of
well-connected IP subnets — and **site links** that model the WAN. AD uses
sites to send clients to a nearby DC and to control replication: within a
site replication is near-immediate change notification; between sites it is
compressed and scheduled over site links by the Knowledge Consistency
Checker (KCC), which builds the replication topology automatically. Because
AD is **multi-master**, any writable DC accepts changes and replicates them
out; conflicts are resolved by version numbers and timestamps.

Five operations are too sensitive for multi-master and are held by a single
DC each — the **FSMO (Flexible Single Master Operations)** roles. Two are
forest-wide: **Schema Master** and **Domain Naming Master**. Three are
per-domain: **RID Master** (hands out pools of relative IDs), **PDC
Emulator** (time source, password-change chaining, and lockout authority),
and **Infrastructure Master** (cross-domain reference updates). Knowing
which DC holds each — and how to move them — is core operational knowledge.

## Design Considerations

Prefer a **single forest, single domain** unless a hard requirement forces
otherwise: a separate schema/security boundary (a genuinely separate
organization), regulatory isolation, or a resource forest for a specific
workload. Every extra domain multiplies DCs, trusts, and replication paths.

Set the **forest and domain functional levels** to the highest the DCs can
support; 2025 continues the trend of few new level-gated features, but the
level still governs which capabilities are available. Place **at least two
DCs per domain** for availability, and put a DC (often a read-only DC,
Chapter 04) in each site with local authentication needs. Make DCs **global
catalog** servers except where a specific single-master role
(Infrastructure Master in a multi-domain forest) argues otherwise.

Design **sites and subnets** to match the physical network so clients find
local DCs and inter-site replication follows the WAN. Keep FSMO placement
simple: leave all roles on the first DC in a small domain, and in larger
ones put the two forest roles and the RID/PDC/Infrastructure roles on
well-connected DCs, keeping the PDC Emulator on a reliable, well-synced
time source because it anchors domain time (Chapter 06).

## Implementation and Automation

Promoting the first domain controller creates the forest:

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSForest -DomainName "corp.contoso.lab" -DomainNetbiosName "CORP" `
  -ForestMode WinThreshold -DomainMode WinThreshold `
  -InstallDns -SafeModeAdministratorPassword (Read-Host -AsSecureString) -Force
```

`WinThreshold` is the functional-level identifier used by recent releases.
The server reboots as `DC01`, a domain controller and DNS server. Add a
second DC to the existing domain:

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSDomainController -DomainName "corp.contoso.lab" `
  -InstallDns -Credential (Get-Credential) `
  -SafeModeAdministratorPassword (Read-Host -AsSecureString) -Force
```

Inspect and move FSMO roles:

```powershell
Get-ADForest | Select-Object SchemaMaster, DomainNamingMaster
Get-ADDomain  | Select-Object PDCEmulator, RIDMaster, InfrastructureMaster
Move-ADDirectoryServerOperationMasterRole -Identity "DC02" `
  -OperationMasterRole PDCEmulator, RIDMaster
```

Define a site and associate a subnet:

```powershell
New-ADReplicationSite -Name "London"
New-ADReplicationSubnet -Name "10.20.0.0/24" -Site "London"
```

## Validation and Troubleshooting

Replication health is the single most important DC check:

```powershell
repadmin /replsummary
repadmin /showrepl
dcdiag /test:Replications /test:FSMOCheck
Get-ADReplicationPartnerMetadata -Target "DC01" |
  Select-Object Partner, LastReplicationSuccess, LastReplicationResult
```

`repadmin /replsummary` shows the largest replication deltas and any
failures; a healthy forest shows `0` failures and small deltas.
`dcdiag` runs a battery of DC health tests. Common failures: **DNS**
misconfiguration (a DC must point its DNS at a working AD-integrated DNS
server, never only itself in a way that breaks bootstrap), **time skew**
beyond five minutes breaking Kerberos, **lingering objects** after a DC was
offline past the tombstone lifetime, and **blocked ports** (RPC/135, LDAP,
Kerberos, DNS) across a firewall between sites. The **PDC Emulator** in the
forest root domain is the default authoritative time source; if it drifts,
authentication fails domain-wide.

## Security and Best Practices

Domain controllers are the crown jewels — compromise of a DC is compromise
of the domain. Run DCs on **Server Core**, keep them **physically and
logically isolated** (dedicated hosts, no extra roles, no browsing), and
place them in **Tier 0** of an administrative tiering model (Chapter 10).
Protect the **DSRM** (Directory Services Restore Mode) password and store
it in a vault. Enable **AD Recycle Bin** so deleted objects can be
restored. Monitor replication and event logs, and back up **system state**
on multiple DCs so the directory can be authoritatively restored. Never
expose LDAP/Kerberos/RPC ports to untrusted networks, and require **LDAP
signing and channel binding** to resist relay attacks.

## References and Knowledge Checks

- Microsoft Learn: *Active Directory Domain Services overview*; *Install a new AD forest with PowerShell*; *FSMO roles*.
- Microsoft Learn: AZ-800 — *Deploy and manage AD DS domain controllers*.

**Knowledge checks**

1. Which partitions replicate forest-wide, and which replicate only within a domain?
2. Why is the PDC Emulator's time source operationally critical?
3. What does `repadmin /replsummary` tell you that `dcdiag` alone does not?

## Hands-On Lab

Topic-level walkthroughs for AZ-800's "deploy and manage AD DS" skills.

**Shared prerequisites for Labs 3.1–3.4** — a Windows Server 2025 host that
will become `DC01`, static IP `10.10.0.10`, and Administrator rights.
**Cost:** none.

### Lab 3.1 — Promote the first domain controller (Topic: Create a forest)

**Objective:** Stand up a new forest and domain.

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSForest -DomainName "corp.contoso.lab" -DomainNetbiosName "CORP" `
  -InstallDns -SafeModeAdministratorPassword (ConvertTo-SecureString 'P@ssw0rd-DSRM!' -AsPlainText -Force) -Force
```

**Expected result:** the server reboots and comes up as a DC; after reboot
`Get-ADDomain` returns the `corp.contoso.lab` domain — promotion installs
AD DS and (with `-InstallDns`) an AD-integrated DNS zone in one step.

**Negative test:** promote with the DC's DNS client pointing at an
unreachable server; promotion warns about DNS delegation and later
replication/logon fail — a DC depends on working DNS.

**Cleanup:** demote with `Uninstall-ADDSDomainController` (lab only).

### Lab 3.2 — Inspect FSMO role placement (Topic: Manage operations masters)

**Objective:** Find which DC holds each of the five roles.

```powershell
netdom query fsmo
Get-ADForest | Select-Object SchemaMaster, DomainNamingMaster
Get-ADDomain  | Select-Object PDCEmulator, RIDMaster, InfrastructureMaster
```

**Expected result:** all five roles report on `DC01` in a fresh
single-DC forest — the first DC holds every FSMO role until they are moved.

**Negative test:** run `Move-ADDirectoryServerOperationMasterRole` targeting
an offline DC; it fails (or a seize is required) — roles transfer cleanly
only between online DCs; seizing is for permanent loss.

**Cleanup:** none (read-only).

### Lab 3.3 — Create a site and subnet (Topic: Configure sites)

**Objective:** Model a branch location for DC locator and replication.

```powershell
New-ADReplicationSite -Name "London"
New-ADReplicationSubnet -Name "10.20.0.0/24" -Site "London"
Get-ADReplicationSubnet -Filter * | Select-Object Name, Site
```

**Expected result:** the `10.20.0.0/24` subnet is bound to the `London`
site — clients in that subnet will authenticate against a London DC when one
exists, and inter-site replication follows the site link.

**Negative test:** create two subnets that overlap; AD rejects the overlap —
a subnet maps to exactly one site.

**Cleanup:** `Remove-ADReplicationSubnet "10.20.0.0/24"; Remove-ADReplicationSite "London"`.

### Lab 3.4 — Check replication health (Topic: Monitor replication)

**Objective:** Prove the directory is converging.

```powershell
repadmin /replsummary
dcdiag /test:Replications
```

**Expected result:** `repadmin /replsummary` shows `0` failures and small
largest-delta values; `dcdiag` reports the Replications test passed — a
healthy multi-master directory converges with no failures.

**Negative test:** block RPC (TCP 135) to a partner DC and re-run; deltas
grow and `dcdiag` flags a replication error — replication needs RPC and the
directory ports open between DCs.

**Cleanup:** restore the firewall rule.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

AD DS is a multi-master directory bounded by the forest (one schema, one
configuration), partitioned into schema/configuration/domain/application
naming contexts, and made physical by domain controllers, the global
catalog, sites, and KCC-built replication. Five FSMO roles handle the
operations that cannot be multi-master. Promotion, role management, and
site design are scriptable, and replication health (`repadmin`, `dcdiag`)
is the first thing to verify.

- [ ] I can explain forest, domain, partitions, and the global catalog.
- [ ] I can promote DCs and place/move FSMO roles.
- [ ] I can model sites and subnets for locator and replication.
- [ ] I can validate replication and diagnose common failures.
- [ ] I completed Labs 3.1–3.4 including each negative test.
