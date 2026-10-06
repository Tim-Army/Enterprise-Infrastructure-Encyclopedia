# Chapter 06: Hardening Windows to the STIG

## Learning Objectives

- Identify the STIGs that apply to a typical Windows server, beyond the
  operating system STIG itself.
- Read Windows STIG IDs and tell domain controller, member server, and
  shared rules apart.
- Apply DISA's STIG Group Policy Objects in a domain with GPMC, and on a
  standalone system with LGPO.
- Describe PowerSTIG as a Desired State Configuration alternative.
- Scan a Windows system with the SCAP Compliance Checker and work through the
  manual rules that remain.

## Theory and Architecture

A Windows server is rarely covered by one STIG. The operating system STIG is the
largest, but Microsoft components each have their own:

| STIG | Covers |
| --- | --- |
| **Windows Server (by release)** | The operating system: accounts, audit policy, security options, user rights, services, and more |
| **Windows 10 / Windows 11** | Client operating systems |
| **Active Directory Domain and Forest** | Directory configuration, beyond what applies to an individual domain controller |
| **Microsoft Defender Antivirus** | Antivirus configuration |
| **Microsoft Defender Firewall with Advanced Security** | Host firewall profiles and logging |
| **Microsoft Edge** | Browser policy |
| **Microsoft .NET Framework 4** | Framework security settings |
| **IIS 10.0 Server and Site** | Web server and per-site configuration, when IIS is installed |
| **Microsoft SQL Server** | Database instance and database, when SQL Server is installed |
| **Microsoft 365 Apps / Office** | Office application policy on clients |

A typical member server needs the Windows Server STIG plus the Defender
Antivirus, Defender Firewall, .NET Framework, and (if installed) Edge STIGs.
Add IIS or SQL Server STIGs when those roles are present, and the Active
Directory STIGs for domain controllers. Confirm the exact list and current
release names in the DoD Cyber Exchange library; DISA adds STIGs for new
Windows releases as they ship.

### Reading Windows STIG IDs

Windows STIG IDs encode the product and the policy area. For Windows Server
2022, IDs start with `WN22-`, followed by an area code:

| Area code | Meaning |
| --- | --- |
| `AC` | Account policies |
| `AU` | Audit policy |
| `CC` | Computer configuration (administrative templates) |
| `SO` | Security options |
| `UR` | User rights assignment |
| `DC` | Applies to domain controllers only |
| `MS` | Applies to member servers only |
| `00` | General requirements, often manual |

The `DC` and `MS` codes matter: on a member server, `DC` rules are Not
Applicable, and the other way round. Rules without either code apply to both.

### Group Policy does most of the work

Most Windows STIG rules are Group Policy settings: audit policy, security
options, user rights, and administrative template values. DISA publishes a
**STIG GPO package** on the DoD Cyber Exchange each quarter. It contains
importable GPO backups for current Windows releases and Microsoft products,
WMI filters to target domain controllers and member servers, the ADMX templates
some settings need, and a readme describing how to use them.

```text
Domain environment                       Standalone or workgroup system
──────────────────                       ─────────────────────────────
Import DISA GPO backups with GPMC        Apply GPO backups to local policy
Link to the right OUs, with WMI filters  with Microsoft's LGPO.exe
Group Policy keeps settings enforced     Reapply after changes or drift
```

Not every rule is a policy setting. The remainder includes items such as
installed roles and features, local account review, antivirus presence,
certificate stores, BitLocker or backup requirements, and documentation
requirements. Those need configuration by other means or manual review.

### PowerSTIG

**PowerSTIG** is an open-source Microsoft project that expresses STIG settings
as PowerShell **Desired State Configuration (DSC)** resources. You declare the
product, version, and role (for example Windows Server 2022, member server), list
any rules to skip and organization-specific values, and DSC applies and
monitors the configuration. It suits environments that already use DSC, or that
need the same baseline on systems outside a domain.

## Design Considerations

- **Use GPOs in a domain, LGPO or DSC outside one.** Group Policy reapplies
  settings continuously, which also corrects drift. Standalone systems need a
  repeatable alternative.
- **Import DISA's GPOs into a test OU first.** Settings such as NTLM
  restrictions, SMB signing, legacy protocol removal, and user rights can break
  applications and older clients.
- **Separate DC and member server policy.** Link the domain controller GPO only
  to the Domain Controllers OU, and use the WMI filters DISA supplies or
  dedicated OUs.
- **Manage exceptions explicitly.** If an application needs a setting relaxed,
  create a separate, clearly named exception GPO with higher precedence and
  document the deviation, rather than editing DISA's GPO. That keeps the DISA
  baseline replaceable each quarter.
- **Account for the DoD-specific rules.** Requirements such as installing DoD
  root certificates and using the DoD logon banner text are written for DoD
  networks. Outside DoD, record your organization's equivalent or justify the
  rule as Not Applicable.

## Implementation and Automation

### In a domain: import the DISA GPOs

1. Download and extract the current DISA STIG GPO package.
2. Copy the package's ADMX and ADML files into the domain's central store
   (`\\<DOMAIN>\SYSVOL\<DOMAIN>\Policies\PolicyDefinitions`) so every setting
   displays and applies.
3. In **Group Policy Management**, create an empty GPO for each baseline you
   need, right-click it, choose **Import Settings**, and point the wizard at the
   matching GPO backup from the package.
4. Link the GPOs to a test OU, apply the WMI filters where appropriate, and run
   `gpupdate /force` on a test server.
5. Test the workload, then link to production OUs.

### On a standalone system: LGPO

Download **LGPO.exe** from Microsoft's Security Compliance Toolkit, then, from an
elevated PowerShell prompt:

```powershell
# Back up current local policy first
New-Item -ItemType Directory -Force C:\STIG\backup | Out-Null
.\LGPO.exe /b C:\STIG\backup

# Copy DISA's ADMX templates so administrative template settings apply
Copy-Item "<GPO_PACKAGE>\ADMX Templates\*\*.admx" C:\Windows\PolicyDefinitions\ -Force
Copy-Item "<GPO_PACKAGE>\ADMX Templates\*\en-US\*.adml" C:\Windows\PolicyDefinitions\en-US\ -Force

# Apply the member server GPO backups for this Windows release
.\LGPO.exe /g "<GPO_PACKAGE>\<WINDOWS_SERVER_RELEASE_FOLDER>\GPOs"
gpupdate /force
```

Template folder names vary between package releases. Check the package readme
for the exact layout before running the copy commands.

### With PowerSTIG

```powershell
Install-Module -Name PowerSTIG -Scope AllUsers
Get-Command -Module PowerSTIG          # list the composite resources
```

A minimal configuration for a Windows Server 2022 member server:

```powershell
Configuration StigBaseline {
    Import-DscResource -ModuleName PowerSTIG
    Node 'localhost' {
        WindowsServer BaseLine {
            OsVersion = '2022'
            OsRole    = 'MS'
            SkipRule  = @('<GROUP_ID_DOCUMENTED_AS_EXCEPTION>')
        }
    }
}
StigBaseline -OutputPath C:\STIG\mof
Start-DscConfiguration -Path C:\STIG\mof -Wait -Verbose
```

Check the PowerSTIG documentation for the STIG versions and parameters your
module release supports.

### Scan with the SCAP Compliance Checker

Install SCC from the DoD Cyber Exchange, load the DISA SCAP benchmarks for the
products on the host, and run a scan as an administrator. SCC writes an HTML
summary and XCCDF results to its sessions folder. Import the XCCDF results into
the host's checklist (Chapter 04) and review the manual rules that remain.

## Validation and Troubleshooting

- **A setting does not apply.** Run `gpresult /h C:\STIG\gpresult.html` and
  check which GPO won. A higher-precedence GPO or local policy can override the
  STIG GPO.
- **Administrative template settings are missing in GPMC.** The ADMX files were
  not copied to the central store or `PolicyDefinitions`.
- **Remote management stopped working after the baseline.** Check user rights
  (who may log on through Remote Desktop Services or access the computer from
  the network), WinRM settings, and the firewall profile.
- **Older clients cannot connect.** SMB signing, NTLM restrictions, and TLS
  settings are the usual causes. Identify the client and plan its upgrade
  instead of weakening the baseline.
- **SCC reports rules as "Not Checked."** Those are manual rules or rules the
  benchmark does not automate. Review them in the checklist.

## Security and Best Practices

- Keep DISA's GPOs unmodified and layer documented exceptions on top, so each
  quarterly package can replace the previous one cleanly.
- Back up local policy (`LGPO.exe /b`) before applying a baseline to a
  standalone system.
- Apply the matching browser, antivirus, firewall, and .NET STIGs along with the
  OS STIG. Assessors expect all applicable STIGs, not just the largest one.
- Remove roles, features, and software the server does not need. Every role
  installed can add STIG rules and attack surface.
- Rescan after every monthly patch cycle. Updates occasionally reset or add
  settings.

## References and Knowledge Checks

**References:**

- DISA Windows Server, Windows client, Defender, Edge, .NET, IIS, and SQL Server
  STIGs, and the quarterly STIG GPO package (DoD Cyber Exchange).
- Microsoft Security Compliance Toolkit, including LGPO.exe (Microsoft
  Download Center).
- PowerSTIG project (`github.com/microsoft/PowerStig`).
- SCAP Compliance Checker (DoD Cyber Exchange SCAP tools page).

**Knowledge checks:**

1. Which STIGs apply to a Windows Server member server that also runs IIS?
2. What do the `DC` and `MS` area codes in a Windows STIG ID tell you?
3. Why should exceptions go in a separate GPO rather than edits to DISA's GPO?
4. When would you use LGPO instead of GPMC, and what does `LGPO.exe /b` do?
5. Name three kinds of Windows STIG rules that Group Policy cannot satisfy.

## Summary and Completion Checklist

A Windows server falls under the operating system STIG plus separate STIGs for
Defender Antivirus, Defender Firewall, .NET, Edge, and any IIS, SQL Server, or
Active Directory roles. Windows STIG IDs show the policy area and whether a rule
applies to domain controllers, member servers, or both. DISA's quarterly GPO
package applies most rules, through GPMC in a domain or LGPO on standalone
systems, and PowerSTIG offers a DSC alternative. SCC measures the result, and
the manual rules that remain need review.

- [ ] Can list the STIGs that apply to a given Windows server.
- [ ] Can read Windows STIG IDs, including `DC` and `MS` codes.
- [ ] Can apply DISA's GPOs with GPMC and with LGPO.
- [ ] Can explain how to layer documented exceptions over DISA's baseline.
