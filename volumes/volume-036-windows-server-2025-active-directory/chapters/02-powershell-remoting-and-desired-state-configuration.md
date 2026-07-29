# Chapter 02: PowerShell, Remoting, and Desired State Configuration

## Learning Objectives

- Use cmdlets, the object pipeline, and providers to administer Windows Server without the GUI.
- Run PowerShell 7 alongside the built-in Windows PowerShell 5.1 and know when each matters.
- Administer remote servers with WinRM remoting, persistent sessions, and Just Enough Administration (JEA).
- Discover, install, and trust modules from the PowerShell Gallery safely.
- Express server configuration as code and enforce it with Desired State Configuration.

## Theory and Architecture

PowerShell is the administrative engine of Windows Server. Unlike a
text-stream shell, it passes **objects** along the pipeline: `Get-Service`
emits service objects, not lines of text, so `Get-Service | Where-Object
Status -eq 'Running' | Sort-Object DisplayName` filters and sorts on real
properties without parsing. Cmdlets follow a `Verb-Noun` grammar
(`Get-`, `Set-`, `New-`, `Remove-`), and `Get-Command`, `Get-Help`, and
`Get-Member` make the whole surface discoverable from the prompt.

Two PowerShells coexist. **Windows PowerShell 5.1** ships in the box, is
built on the .NET Framework, and hosts the largest set of Windows
management modules; some modules still run only there. **PowerShell 7**
(the `pwsh` executable) is built on modern .NET, is cross-platform, and is
installed separately. On a server you generally keep 5.1 for
Windows-specific modules and add 7 for everything else; the **Windows
Compatibility** module lets 7 proxy to 5.1 modules when needed.

**Remoting** is built on **WinRM** (WS-Management over HTTP 5985 / HTTPS
5986). `Enter-PSSession` gives an interactive remote prompt; `Invoke-Command`
runs a script block against one or many servers in parallel and returns
objects tagged with their source computer. Persistent sessions
(`New-PSSession`) keep state across calls. Because full remoting grants
broad rights, **JEA** constrains it: a session configuration plus a role
capability file expose only named cmdlets and parameters, running under a
temporary virtual account, so a help-desk operator can restart a service
without being a local administrator.

**Desired State Configuration (DSC)** shifts administration from imperative
steps to declarative state. A configuration document names resources
(`WindowsFeature`, `File`, `Service`, `Registry`) and their desired state;
the Local Configuration Manager compiles it to a MOF and continuously
enforces it, correcting drift. DSC is the Windows analogue of the
Ansible/Puppet model covered in Volume IX and the foundation for
configuration-as-code on Windows.

## Design Considerations

Decide early whether a task is a one-off or a standard. One-offs are fine
as ad-hoc cmdlets; standards — "every web server has IIS, the firewall
rule, and this app pool" — belong in DSC or an idempotent script so the
result is reproducible and drift is detectable. Prefer idempotent building
blocks (`Install-WindowsFeature`, `Set-` cmdlets, DSC resources) over
imperative sequences that fail messily on re-run.

For remoting, choose HTTPS (5986) with a proper certificate outside a
trusted domain, and rely on Kerberos inside the domain where 5985 traffic
is authenticated and the payload is encrypted at the WS-Man layer. Design
JEA roles around job function, not convenience: the point is least
privilege, so expose the minimum cmdlet set and audit transcripts.

Version matters. Test scripts against the PowerShell edition they will run
under; a script that works in 7 may fail in 5.1 if it uses newer syntax,
and a module that only exists in 5.1 must be proxied. Pin module versions
in automation so a Gallery update cannot change behavior underneath you.

## Implementation and Automation

The discovery loop is the first thing to internalize:

```powershell
Get-Command -Noun NetIPAddress          # what can I do to IP addresses?
Get-Help New-NetIPAddress -Examples     # how do I use it?
Get-NetIPAddress | Get-Member           # what properties/methods exist?
```

Remoting against many servers at once returns source-tagged objects:

```powershell
$servers = 'DC01','FS01','WEB01'
Invoke-Command -ComputerName $servers -ScriptBlock {
  Get-Service -Name W32Time | Select-Object Status, StartType
}   # each result carries a PSComputerName property
```

A minimal JEA endpoint exposes only what an operator needs:

```powershell
# Role capability: allow restarting the Spooler service, nothing else
New-Item -Path 'C:\Program Files\WindowsPowerShell\Modules\HelpDeskRC\RoleCapabilities' -ItemType Directory -Force
New-PSRoleCapabilityFile -Path '...\HelpDeskRC\RoleCapabilities\HelpDesk.psrc' `
  -VisibleCmdlets @{ Name='Restart-Service'; Parameters=@{ Name='Name'; ValidateSet='Spooler' } }
Register-PSSessionConfiguration -Name 'HelpDesk' -Path .\HelpDesk.pssc -Force
```

DSC expresses a web server as state, not steps:

```powershell
Configuration WebBaseline {
  Import-DscResource -ModuleName PSDesiredStateConfiguration
  Node 'WEB01' {
    WindowsFeature IIS { Ensure = 'Present'; Name = 'Web-Server' }
    Service W3SVC     { Name = 'W3SVC'; State = 'Running'; DependsOn = '[WindowsFeature]IIS' }
  }
}
WebBaseline -OutputPath C:\DSC
Start-DscConfiguration -Path C:\DSC -Wait -Verbose
```

## Validation and Troubleshooting

Confirm which PowerShell you are in and test a remote path:

```powershell
$PSVersionTable.PSVersion         # 5.1.x in Windows PowerShell, 7.x in pwsh
Test-WSMan -ComputerName DC01     # WinRM reachable and responding?
Test-DscConfiguration -Detailed   # is the node in desired state?
```

`Test-DscConfiguration` returns `InDesiredState : True` when no drift
exists and lists the non-compliant resources when it does. Common
remoting failures: WinRM not running or not trusted (`Enable-PSRemoting`
on the target, or add to `TrustedHosts` outside a domain); the firewall
blocking 5985/5986; or double-hop failures where a remote session cannot
authenticate onward to a third server — solved with CredSSP or, better,
resource-based Kerberos constrained delegation. For DSC, `Get-DscConfigurationStatus`
shows the last run's result and whether a reboot is pending.

## Security and Best Practices

Treat remoting endpoints as privileged surface: prefer HTTPS listeners
outside the domain, keep `TrustedHosts` empty inside it (Kerberos handles
trust), and enable PowerShell **script block logging** and **transcription**
so administrative actions are auditable. Use JEA to eliminate standing
local-admin rights for routine tasks. Set the execution policy to
`RemoteSigned` and **sign** production scripts and DSC modules. Pull
modules only from the trusted PowerShell Gallery (or an internal
repository), pin versions, and review any module before running it as
administrator. Never paste credentials into scripts — use `Get-Credential`,
gMSA (Chapter 10), or a secrets vault.

## References and Knowledge Checks

- Microsoft Learn: *PowerShell documentation*; *about_Remote*; *Just Enough Administration*; *Desired State Configuration*.
- Microsoft Learn: AZ-800 — *Manage Windows Servers and workloads by using PowerShell and DSC*.

**Knowledge checks**

1. Why does `Get-Service | Where-Object Status -eq 'Running'` work without text parsing?
2. When must you keep Windows PowerShell 5.1 rather than moving entirely to PowerShell 7?
3. What problem does JEA solve that plain remoting does not?

## Hands-On Lab

Topic-level walkthroughs for the AZ-800 "manage with PowerShell and DSC"
skills. Each step is runnable.

**Shared prerequisites for Labs 2.1–2.4** — a Windows Server 2025 host, a
second reachable server (or `localhost`) for remoting, and Administrator
rights. **Cost:** none.

### Lab 2.1 — Explore the object pipeline (Topic: Administer with cmdlets)

**Objective:** Filter, sort, and select on object properties.

```powershell
Get-Service | Where-Object Status -eq 'Running' |
  Sort-Object DisplayName | Select-Object -First 5 Name, DisplayName, StartType
```

**Expected result:** a table of the first five running services by display
name — the pipeline filtered and sorted on real properties, not text, which
is the core of PowerShell administration.

**Negative test:** run `Get-Service | Where-Object {$_.Status = 'Running'}`
(single `=`); it errors or matches everything — `=` assigns, `-eq`
compares. Use the comparison operator.

**Cleanup:** none (read-only).

### Lab 2.2 — Run a command across multiple servers (Topic: Remote administration)

**Objective:** Fan a command out and get source-tagged results.

```powershell
Invoke-Command -ComputerName localhost -ScriptBlock {
  [pscustomobject]@{ Host = $env:COMPUTERNAME; Uptime = (Get-Uptime) }
} | Format-Table Host, Uptime, PSComputerName
```

**Expected result:** one row per target carrying a `PSComputerName`
property — `Invoke-Command` runs in parallel and tags each object with its
origin, so results from many servers stay attributable.

**Negative test:** target a name that is not in `TrustedHosts` outside a
domain; it fails with an access-denied/trust error — remoting requires
Kerberos (domain) or an explicit trust.

**Cleanup:** none.

### Lab 2.3 — Install a module from the Gallery with a pinned version (Topic: Extend PowerShell)

**Objective:** Add a module safely and confirm its version.

```powershell
Install-Module -Name PSWindowsUpdate -RequiredVersion 2.2.1.5 -Scope AllUsers -Force
Get-Module -ListAvailable PSWindowsUpdate | Select-Object Name, Version
```

**Expected result:** the exact pinned version installs — pinning stops a
later Gallery release from silently changing automation behavior.

**Negative test:** run `Install-Module SomeTypo-Module`; it fails with "no
match found" — module names are exact and the Gallery is the trust boundary.

**Cleanup:** `Uninstall-Module PSWindowsUpdate -AllVersions`.

### Lab 2.4 — Enforce state with DSC (Topic: Configuration as code)

**Objective:** Declare a feature's desired state and correct drift.

```powershell
Configuration DnsPresent {
  Import-DscResource -ModuleName PSDesiredStateConfiguration
  Node 'localhost' { WindowsFeature DNS { Ensure='Present'; Name='DNS' } }
}
DnsPresent -OutputPath C:\DSC\DnsPresent
Start-DscConfiguration -Path C:\DSC\DnsPresent -Wait -Force
Test-DscConfiguration -Detailed
```

**Expected result:** the DNS feature is installed and
`Test-DscConfiguration` reports `InDesiredState : True`; remove the feature
by hand and re-run, and DSC reinstalls it — DSC enforces declared state and
corrects drift.

**Negative test:** set `Ensure='Absent'` and re-apply while DNS is in use;
DSC removes the role and dependent services stop — declared state is
authoritative, so review a configuration before applying it.

**Cleanup:** `Remove-Item C:\DSC -Recurse -Force`; uninstall the DNS feature if lab-only.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

PowerShell administers Windows Server through objects, not text; two
editions (5.1 and 7) coexist for compatibility and modernity; WinRM
remoting and JEA run commands remotely with least privilege; the Gallery
extends the surface (pin versions); and DSC turns configuration into
declarative, drift-correcting code.

- [ ] I can discover and use cmdlets with `Get-Command`/`Help`/`Get-Member`.
- [ ] I can choose between PowerShell 5.1 and 7 for a given module.
- [ ] I can run commands across servers and constrain access with JEA.
- [ ] I can express and enforce configuration with DSC.
- [ ] I completed Labs 2.1–2.4 including each negative test.
