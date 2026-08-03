# Chapter 03: CCA-V — Security, Monitoring, and Operations

## Learning Objectives

- Cover CCA-V modules 4–9: security, monitoring, troubleshooting, printing, PowerShell, and Citrix Cloud.
- Use Director and Citrix Scout the way the exam's troubleshooting scenarios expect.
- Complete a walkthrough lab per module.

## Modules 4–9 at a glance

| Module | Focus |
|:---|:---|
| 4 — Basic security | Delegated administration, HDX encryption, TLS on brokers/VDAs |
| 5 — Monitoring | Director dashboards, session details, historical trends |
| 6 — Troubleshooting | Director + Citrix Scout, session performance investigation |
| 7 — Printing | Auto-created client printers, session printers, the Universal Print Driver |
| 8 — PowerShell | The broker snap-ins/SDK for configuration and query |
| 9 — Citrix Cloud | Cloud Connectors, migrating the control plane, hybrid operations |

## Hands-On Lab

Same lab site as [Chapter 02](02-cca-v-deploying-and-delivering.md). **Cost:** none beyond the eval.

### Lab 3.1 — Delegated administration (module 4)

**Objective:** Scope an administrator to a role, the security model's core.

```powershell
Get-AdminAdministrator | Select-Object Name, Enabled
Get-AdminRole | Select-Object Name, Description
New-AdminAdministrator -Name "LAB\helpdesk1"
Add-AdminRight -Administrator "LAB\helpdesk1" -Role "Help Desk Administrator" -Scope "All"
```

**Expected result:** `helpdesk1` holds exactly the Help Desk role — session shadowing and troubleshooting in Director, no machine-catalog or policy rights. Role × scope is the exam's security grammar.

**Negative test:** Have `helpdesk1` attempt a catalog change in Studio; it is refused — the role does not carry it.

**Cleanup:** `Remove-AdminAdministrator -Name "LAB\helpdesk1"`.

### Lab 3.2 — Director for monitoring (module 5)

**Objective:** Read the monitoring data the way the exam scenarios present it.

```powershell
# Director's data, queried at the source:
Get-BrokerSession | Group-Object DesktopGroupName | Select-Object Name, Count
Get-BrokerMachine -SummaryState Unregistered | Measure-Object | Select-Object Count
```

**Expected result:** Session counts per delivery group and an unregistered-machine count of `0` on a healthy site — the two numbers Director's dashboard leads with. In Director itself: Dashboard → Infrastructure/Sessions panels show the same story.

**Negative test:** Filter Director's Trends view to a nonexistent time range or an idle group — empty panels are data ("nothing happened"), not a monitoring failure; the exam distinguishes the two.

**Cleanup:** None (read-only).

### Lab 3.3 — Citrix Scout (module 6)

**Objective:** Collect diagnostics the way support (and the exam) expects.

```text
studio> Citrix Scout > Collect > select controllers + VDAs > Start
# produces a .zip of CDF traces, event logs, and configuration for upload or analysis
```

**Expected result:** A collection archive per selected machine — the standard artifact for a support case; Scout's health checks also flag common misconfigurations inline.

**Negative test:** Run Scout against a VDA with WinRM blocked; collection for that machine fails — Scout depends on WinRM reachability, a detail the troubleshooting module tests.

**Cleanup:** Delete the lab archives.

### Lab 3.4 — Printing policies (module 7)

**Objective:** Set the session-printing behavior the exam drills.

```powershell
Get-BrokerSession | Select-Object -First 1 UserName   # confirm a session exists
# Policy (Studio > Policies): "Auto-create client printers" = Auto-create the client's default printer only
# Policy: "Universal print driver usage" = Use universal printing only
```

**Expected result:** New sessions map only the client's default printer, through the Universal Print Driver — the combination that eliminates driver sprawl, and the most-tested printing configuration.

**Negative test:** Set auto-create to all client printers with native drivers on a lab VDA; logon slows and the event log records driver installs — the failure mode the UPD policy exists to prevent.

**Cleanup:** Revert the lab policy.

### Lab 3.5 — PowerShell fluency (module 8)

**Objective:** Prove the four verbs the exam expects you to read.

```powershell
Get-BrokerDesktopGroup LabGroup | Select-Object Name, InMaintenanceMode
Set-BrokerDesktopGroup LabGroup -InMaintenanceMode $true
Get-BrokerDesktopGroup LabGroup | Select-Object Name, InMaintenanceMode
Set-BrokerDesktopGroup LabGroup -InMaintenanceMode $false
```

**Expected result:** Maintenance mode flips `$true` then back — `Get/Set/New/Remove` against broker objects is the whole SDK grammar; exam items show a cmdlet and ask what it does.

**Negative test:** While in maintenance mode, attempt a launch: the store hides or refuses the resource — maintenance mode drains without destroying.

**Cleanup:** Done in the walkthrough.

### Lab 3.6 — Citrix Cloud and Cloud Connectors (module 9)

**Objective:** Understand the hybrid model: control plane in Citrix Cloud, resources on-premises.

```powershell
# On a Cloud Connector:
Get-Service cdf* , Citrix* | Select-Object Name, Status | Sort-Object Name | Select-Object -First 8
```

**Expected result:** The connector services running — the connector pair (always deploy two per resource location) replaces local Delivery Controllers, outbound-443 only, no inbound firewall holes. Exam scenarios hinge on: connectors are stateless, the site database moves to the cloud, StoreFront can stay local.

**Negative test:** Stop both lab connectors; brokering for that resource location fails (local host cache on the connectors is the resilience story — one connector must be up).

**Cleanup:** Restart the services.

## Summary and Completion Checklist

- [ ] Delegated administration, Director, Scout, printing, PowerShell, and Cloud Connector labs complete.
- [ ] The Get/Set broker grammar is comfortable.
- [ ] Hybrid (Citrix Cloud) architecture understood: connectors out, controllers gone, StoreFront optional-local.
