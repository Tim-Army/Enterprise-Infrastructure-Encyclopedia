# Chapter 03: Windows Server Administration

## Learning Objectives

- Describe the Windows Server architecture: installation options, the
  services model, and the roles/features framework.
- Administer Windows Server primarily through PowerShell rather than the
  graphical console, consistent with enterprise automation practice.
- Manage Windows services, scheduled tasks, and the registry safely.
- Use Windows Admin Center and Server Manager for fleet-level
  administration and understand when each tool is appropriate.
- Configure and interpret the Windows Event Log subsystem.
- Perform remote administration with PowerShell Remoting (WinRM) and
  understand its trust model.
- Explain how this chapter's cross-platform Windows Server coverage
  complements the Linux coverage in Chapter 02 and the identity coverage
  in Chapter 04.

## Theory and Architecture

Windows Server is administered as a **role-and-feature** platform: a base
operating system image to which administrators add discrete roles (Active
Directory Domain Services, DNS Server, File and Storage Services, Hyper-V,
IIS) and features (Failover Clustering, .NET Framework components, Windows
Server Backup). This model is conceptually equivalent to Linux package
groups, but roles carry configuration wizards and dependency logic beyond
a simple package install.

### Installation options

Since Windows Server 2016, every role and feature can run on either a
full **Desktop Experience** installation or the minimal **Server Core**
installation, which omits the Windows Explorer shell and most GUI
management consoles:

| Installation option | Footprint | Management surface | Typical use |
| --- | --- | --- | --- |
| Server Core | Smaller disk/patch footprint, fewer reboot-triggering updates | PowerShell, WinRM, Windows Admin Center, `sconfig` | Production servers, especially domain controllers and Hyper-V hosts |
| Desktop Experience | Full GUI, MMC snap-ins | Local console, RDP, PowerShell | Servers requiring a GUI-only vendor management console |

Enterprise fleets should default to Server Core and reserve Desktop
Experience for the narrow set of workloads whose management tooling has
no PowerShell or Server Core-compatible path. A smaller installation
footprint directly reduces patch volume and reboot frequency (Chapter 06).

### The services model

Windows Server runs long-lived background work as **services**, managed
by the Service Control Manager (SCM). Each service has a startup type
(`Automatic`, `Automatic (Delayed Start)`, `Manual`, `Disabled`), a logon
identity (Local System, Network Service, Local Service, or a dedicated
service account — often a Group Managed Service Account, or gMSA, in an
Active Directory environment), and a recovery policy governing what
happens after a crash. This is the direct Windows analog to a `systemd`
service unit covered in Chapter 02, and the two are compared side by side
in Chapter 05.

### PowerShell as the primary administration surface

PowerShell (version 7.4+ in this baseline, alongside the in-box Windows
PowerShell 5.1 that ships with the OS) is the primary interface for
enterprise Windows administration, not a supplementary scripting tool.
Nearly every GUI action in Server Manager or Windows Admin Center is
backed by a PowerShell cmdlet, and every cmdlet can be scripted,
version-controlled, and run unattended — which is why automation-first
enterprises standardize on PowerShell (and its Desired State Configuration
extension, covered in Chapter 06) as the primary administration surface,
with the GUI reserved for exploration and troubleshooting.

### Fleet-level management tools

- **Server Manager** — the built-in console for adding roles/features and
  viewing a small number of remote servers' status. Largely superseded by
  Windows Admin Center for day-to-day operations but still used for
  role/feature installation workflows.
- **Windows Admin Center (WAC)** — a browser-based, gateway-deployed
  management surface that consolidates certificate, storage, networking,
  Hyper-V, and update management for many servers from a single pane,
  connecting to each managed node over WinRM.
- **PowerShell Remoting (WinRM)** — the transport underlying both WAC and
  ad hoc remote administration; see Implementation and Automation below.

## Design Considerations

- **Server Core by default.** Standardizing on Server Core reduces the
  patch and reboot burden across the fleet; budget time for validating
  that every vendor agent (backup, monitoring, security) supports Server
  Core before committing to it as the default image.
- **Service account strategy.** Choose between built-in identities (Local
  System, Network Service), standalone service accounts, and Group Managed
  Service Accounts (gMSA) deliberately. gMSA is the preferred pattern for
  domain-joined services because Active Directory manages password
  rotation automatically, eliminating a common source of expired-password
  outages (see Chapter 04 for AD-integrated identity design).
  Which pattern a given service supports is a factor in role placement,
  not an afterthought.
- **WinRM trust boundary.** Decide whether PowerShell Remoting traverses
  HTTP (5985, encrypted at the Kerberos/NTLM layer) or HTTPS (5986, TLS
  plus a server certificate). Enterprise environments should standardize
  on HTTPS listeners with certificates issued by an internal CA, especially
  for remoting that crosses network segments.
- **Update ring placement.** Decide which servers land in early validation
  rings versus broad deployment rings before you need WSUS/Windows Update
  for Business groups configured (Chapter 06) — retrofitting ring
  membership after an incident is reactive, not designed.
- **Cluster-eligible roles.** Roles that support Failover Clustering
  (file services, Hyper-V, SQL Server as a clustered role) should be
  evaluated for clustering at design time if the workload's availability
  requirement exceeds what a single host and a good backup can provide.

## Implementation and Automation

### Installing roles and features with PowerShell

```powershell
# Query available roles/features, then install one with its management
# tools, targeting a remote Server Core host.
Get-WindowsFeature -ComputerName winsrv12 | Where-Object Installed -eq $false

Install-WindowsFeature -ComputerName winsrv12 `
    -Name FS-FileServer, RSAT-File-Services `
    -IncludeManagementTools
```

### Managing services

```powershell
# Inspect a service, then set it to Automatic (Delayed Start) with a
# restart-on-failure recovery policy, using the classic sc.exe for the
# recovery action (no native cmdlet exists for recovery options).
Get-Service -Name Spooler | Select-Object Name, Status, StartType

Set-Service -Name Spooler -StartupType AutomaticDelayedStart

sc.exe failure Spooler reset= 86400 actions= restart/60000/restart/60000/""/0
```

### Scheduled tasks

```powershell
# Create a scheduled task equivalent to the systemd timer example in
# Chapter 02: run a cleanup script daily at 02:00, using a gMSA so no
# password needs to be stored or rotated manually.
$action    = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument '-NoProfile -File C:\Scripts\Cleanup-Temp.ps1'
$trigger   = New-ScheduledTaskTrigger -Daily -At 2:00AM
$principal = New-ScheduledTaskPrincipal `
    -UserId 'EXAMPLE\svc-cleanup$' -LogonType Password -RunLevel Limited

Register-ScheduledTask -TaskName 'Nightly Temp Cleanup' `
    -Action $action -Trigger $trigger -Principal $principal `
    -Description 'Purges C:\Temp files older than 7 days'
```

### Remote administration with PowerShell Remoting

```powershell
# Enable and harden WinRM on a target host (run once, typically via
# configuration management rather than interactively).
Enable-PSRemoting -Force
Set-Item WSMan:\localhost\Service\Auth\Basic -Value $false
Set-Item WSMan:\localhost\Service\AllowUnencrypted -Value $false

# From an administrator workstation, run a command against a remote host.
Invoke-Command -ComputerName winsrv12 -ScriptBlock {
    Get-EventLog -LogName System -EntryType Error -Newest 10
} -Credential (Get-Credential 'EXAMPLE\admin.jdoe')
```

### Registry management

```powershell
# Query and set a registry value through PowerShell's registry provider
# rather than regedit.exe, so the change is scriptable and auditable.
Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters' `
    -Name 'SMB1'

Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters' `
    -Name 'SMB1' -Value 0 -Type DWord
```

### Event Log queries

```powershell
# Query the Windows Event Log for failed logon attempts (Event ID 4625)
# in the last 24 hours — the Windows analog to journalctl -p err in
# Chapter 02.
Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4625
    StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Id, Message
```

## Validation and Troubleshooting

- Confirm a feature installed successfully and did not require a pending
  reboot: `Get-WindowsFeature -Name FS-FileServer` should report
  `Installed`, and `Get-Item 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending' -ErrorAction SilentlyContinue`
  should return nothing.
- Confirm WinRM connectivity before troubleshooting anything else remote:
  `Test-WSMan -ComputerName winsrv12`.
- Confirm a scheduled task's last run result:
  `Get-ScheduledTaskInfo -TaskName 'Nightly Temp Cleanup'` — a
  `LastTaskResult` of `0` indicates success; nonzero values map to
  documented Win32 error codes.
- Confirm service recovery policy took effect:
  `sc.exe qfailure Spooler`.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| `Invoke-Command` fails with an access-denied or Kerberos error | Target host not in the same domain/trust, or double-hop authentication issue | `Test-WSMan`, then check `klist` for a valid Kerberos ticket; consider `CredSSP` or resource-based constrained delegation for double-hop |
| Service repeatedly stops shortly after starting | Crash loop; recovery action set to "Restart the Service" is masking the underlying failure | Check `Get-WinEvent -LogName Application` for the service's error entries around the crash time |
| Scheduled task shows `LastTaskResult` of `0x1` | Script exited with error, often a permissions issue for the task's run-as account | Run the script interactively as the same account to reproduce |
| Server Core host cannot be managed by a GUI tool | Tool requires local console/GUI shell not present on Server Core | Use Windows Admin Center or the PowerShell-equivalent cmdlet instead |
| WinRM HTTPS listener fails to bind | No valid certificate bound, or port 5986 blocked | `winrm enumerate winrm/config/listener`; verify certificate chain and firewall rule |

## Security and Best Practices

- Default new server builds to Server Core; require an explicit,
  documented exception to deploy Desktop Experience.
- Use Group Managed Service Accounts (gMSA) for domain-joined services
  wherever the role supports them, eliminating manually managed service
  account passwords.
- Disable the WinRM Basic and unencrypted transport options; require
  Kerberos or a certificate-backed HTTPS listener for PowerShell
  Remoting.
- Apply the principle of least privilege to scheduled tasks: run with a
  `Limited` run level and a scoped service account rather than
  `SYSTEM` unless the task genuinely requires system-level access.
- Forward Security and System event logs to a centralized collector
  (Windows Event Forwarding or a SIEM agent) rather than relying on local
  retention alone (Chapter 09).
- Disable legacy protocols still present for compatibility (SMBv1, as
  shown above) unless a specific, documented legacy dependency requires
  them.
- Apply DISA STIG or CIS Benchmark hardening baselines for Windows Server
  through Group Policy or Desired State Configuration, not manual
  per-server edits (Chapter 08).

## References and Knowledge Checks

**References**

- Microsoft Learn: "Windows Server documentation" and "PowerShell
  Remoting Overview."
- Microsoft Learn: "Group Managed Service Accounts Overview."
- Microsoft Learn: "Windows Admin Center overview."
- DISA STIG for Microsoft Windows Server (Server Core and Member Server
  documents).

**Knowledge Checks**

1. What is the operational advantage of Server Core over Desktop
   Experience, and what is the trade-off?
2. Why is a Group Managed Service Account preferred over a manually
   created service account for a domain-joined Windows service?
3. What two authentication issues commonly cause `Invoke-Command` to fail
   across a "double hop" (workstation to server A to server B)?
4. Why should WinRM Basic authentication and unencrypted transport be
   disabled in an enterprise environment?
5. Which Event Log and Event ID would you query to find failed logon
   attempts, and what PowerShell cmdlet performs that query?

## Hands-On Lab

**Objective:** Install a Windows Server role remotely, configure a
scheduled task under a scoped identity, harden WinRM, and validate
enforcement — using PowerShell Remoting end to end.

### Prerequisites

- One Windows Server VM (Server Core or Desktop Experience, this baseline
  targets the current Windows Server LTSC release) reachable from an
  administrator workstation running PowerShell 7.4+.
- A local administrator account on the target server (a domain is not
  required for this lab; gMSA steps are described in Chapter 04's lab
  once Active Directory is introduced).
- WinRM enabled on the target (`Enable-PSRemoting -Force`, run once at the
  console or via existing remote access).

### Procedure

1. From your workstation, confirm remoting connectivity to the target:

   ```powershell
   Test-WSMan -ComputerName winsrv-lab
   ```

   **Expected result:** the command returns WSMan identity information
   without error.

2. Install the File Server role remotely:

   ```powershell
   Install-WindowsFeature -ComputerName winsrv-lab `
       -Name FS-FileServer -IncludeManagementTools
   ```

   **Expected result:** `Success` is `True` in the returned object.

3. Create a local folder and share it, using `Invoke-Command` to run the
   commands on the target:

   ```powershell
   Invoke-Command -ComputerName winsrv-lab -ScriptBlock {
       New-Item -Path 'C:\LabShare' -ItemType Directory -Force
       New-SmbShare -Name 'LabShare' -Path 'C:\LabShare' -FullAccess 'Administrators'
   }
   ```

   **Expected result:** the SMB share object is returned with
   `ShareState` equal to `Online`.

4. Register a scheduled task on the target that writes a heartbeat file
   every minute:

   ```powershell
   Invoke-Command -ComputerName winsrv-lab -ScriptBlock {
       $action  = New-ScheduledTaskAction -Execute 'powershell.exe' `
           -Argument '-NoProfile -Command "Get-Date | Out-File C:\LabShare\heartbeat.txt"'
       $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
           -RepetitionInterval (New-TimeSpan -Minutes 1) `
           -RepetitionDuration (New-TimeSpan -Hours 1)
       Register-ScheduledTask -TaskName 'LabHeartbeat' -Action $action `
           -Trigger $trigger -User 'SYSTEM' -RunLevel Limited
   }
   ```

5. Wait at least 90 seconds, then confirm the task executed:

   ```powershell
   Invoke-Command -ComputerName winsrv-lab -ScriptBlock {
       Get-ScheduledTaskInfo -TaskName 'LabHeartbeat'
       Get-Content 'C:\LabShare\heartbeat.txt'
   }
   ```

   **Expected result:** `LastTaskResult` is `0`, and `heartbeat.txt`
   contains a recent timestamp.

6. Harden the WinRM listener by disabling Basic authentication:

   ```powershell
   Invoke-Command -ComputerName winsrv-lab -ScriptBlock {
       Set-Item WSMan:\localhost\Service\Auth\Basic -Value $false
       Set-Item WSMan:\localhost\Service\AllowUnencrypted -Value $false
   }
   ```

### Negative Test

From your workstation, attempt Basic authentication against the target
explicitly:

```powershell
$cred = Get-Credential 'winsrv-lab\labuser'
Invoke-Command -ComputerName winsrv-lab -Authentication Basic `
    -Credential $cred -ScriptBlock { hostname }
```

**Expected result:** the connection is rejected because Basic
authentication was disabled in step 6, confirming the hardening control
is enforced. A subsequent attempt using default (Kerberos/Negotiate)
authentication with a valid domain or local administrator credential
should succeed.

### Cleanup

```powershell
Invoke-Command -ComputerName winsrv-lab -ScriptBlock {
    Unregister-ScheduledTask -TaskName 'LabHeartbeat' -Confirm:$false
    Remove-SmbShare -Name 'LabShare' -Force
    Remove-Item -Path 'C:\LabShare' -Recurse -Force
}
Uninstall-WindowsFeature -ComputerName winsrv-lab -Name FS-FileServer
```

## Summary and Completion Checklist

Windows Server administration in an enterprise fleet is a PowerShell-
first, Server Core-default discipline: roles and features replace ad hoc
software installs, the Service Control Manager and Task Scheduler provide
the Windows analogs to `systemd` services and timers, and PowerShell
Remoting over a hardened WinRM listener is the standard remote-
administration transport. Windows Admin Center and Server Manager remain
useful for fleet-level visibility, but every action they perform can — and
in production should — be scripted.

- [ ] Can choose between Server Core and Desktop Experience for a given
      workload and justify the choice.
- [ ] Can install a role, manage a service's startup type and recovery
      policy, and register a scheduled task entirely through PowerShell.
- [ ] Can enable, harden, and troubleshoot PowerShell Remoting (WinRM).
- [ ] Can query the Windows Event Log for a specific event ID and time
      window.
- [ ] Completed the hands-on lab, including the negative Basic-
      authentication test.
