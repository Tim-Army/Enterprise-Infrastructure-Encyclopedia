# Chapter 02: Microsoft 365 Certifications

## Learning Objectives

- Enumerate the current Microsoft 365 certifications and their exam codes.
- Distinguish the Fundamentals, Administrator Expert, and specialist credentials.
- Map each credential to the hands-on skills in Volume XXXVII.
- Recognize the Microsoft 365 exams that were retired or renumbered.
- Build a study path for a Microsoft 365 administrator role.

## Theory and Architecture

The **Microsoft 365** family certifies the roles that run the modern-work
cloud — administration, endpoints, and collaboration. As verified on
Microsoft Learn (26 July 2026), the current credentials are:

- **Microsoft 365 Certified: Fundamentals** — exam **MS-900** (Fundamentals).
  Cloud concepts, the Microsoft 365 services, security/compliance basics, and
  licensing. The gateway to the family.
- **Microsoft 365 Certified: Administrator Expert** — exam **MS-102**
  (Expert). Tenant, identity, security, and compliance administration across
  the suite; the senior M365 administration credential.
- **Microsoft 365 Certified: Endpoint Administrator Associate** — exam
  **MD-102** (Associate). Deploy and manage Windows and endpoints with
  Intune: enrollment, compliance, configuration, apps, and Autopilot.
- **Microsoft 365 Certified: Teams Administrator Associate** — exam **MS-700**
  (Associate). Manage Teams: policies, teams and channels, meetings, and the
  app catalog.
- **Microsoft 365 Certified: Collaboration Communications Systems Engineer
  Associate** — exam **MS-721** (Associate). Teams Phone and meeting-room
  voice engineering.

Several older Microsoft 365 exams have **retired or been folded in**: MS-100
and MS-101 (the two-exam Enterprise Administrator that MS-102 replaced),
MS-500 (Security Administrator, moved into the SC family), MS-203 (Messaging
Administrator), MS-700's older siblings, and MS-720 (Teams Voice Engineer
Expert, whose scope moved to the MS-721 Associate). Always confirm status on
Microsoft Learn.

## Design Considerations

For a **Microsoft 365 administrator**, the path is **MS-900 → MS-102**, with
**MD-102** if the role owns endpoints and **MS-700/MS-721** if it owns Teams
and voice. MS-102 is labelled **Expert** and is broad — tenant, identity,
security, and compliance — so it rewards real administrative experience and
the identity/security depth of the SC family (Chapter 03). Endpoint-focused
staff should prioritize **MD-102**, which maps directly to the Intune,
compliance, configuration, app, and Autopilot skills in Volume XXXVII
(Chapters 05–07). Voice engineers add **MS-721** on top of **MS-700**.

Because Microsoft 365 security overlaps the SC family, plan them together: an
M365 administrator often pairs **MS-102** with **SC-300** (identity) and
**SC-401** (information security), and a security-operations focus adds
**SC-200**.

## Implementation and Automation

Verify the family and codes from Microsoft Learn:

```bash
for slug in microsoft-365-fundamentals m365-administrator-expert modern-desktop \
            m365-teams-administrator-associate m365-collaboration-communications-systems-engineer; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\b(MS|MD)-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# -> microsoft-365-fundamentals -> MS-900
# -> m365-administrator-expert -> MS-102
# -> modern-desktop -> MD-102
# -> m365-teams-administrator-associate -> MS-700
# -> m365-collaboration-communications-systems-engineer -> MS-721
```

## Validation and Troubleshooting

Map each credential to its skills-measured blueprint on Learn, then to
hands-on practice:

| Credential | Exam | Practice in |
| --- | --- | --- |
| M365 Fundamentals | MS-900 | Vol XXXVII Ch 01 |
| M365 Administrator Expert | MS-102 | Vol XXXVII Ch 01–04, 08–11 |
| Endpoint Administrator | MD-102 | Vol XXXVII Ch 05–07 |
| Teams Administrator | MS-700 | Vol XXXVII Ch 09 |
| Collaboration Communications Systems Engineer | MS-721 | Vol XXXVII Ch 09 |

Common pitfalls: preparing for **MS-100/MS-101** (retired — MS-102 is the
current single exam); expecting **MS-500** here (it moved into the SC family
and was itself retired); and underestimating **MS-102**'s breadth because it
is a single exam — it still spans tenant, identity, security, and compliance
at Expert depth.

## Security and Best Practices

Prepare with the **Microsoft Learn** learning paths and the **free practice
assessment** for each exam, and get hands-on in a **Microsoft 365 Developer**
tenant (Volume XXXVII). Verify the **current exam code** before studying —
the M365 family has renumbered more than once. Pair M365 credentials with the
**SC** identity and security exams for a complete administrator profile, and
renew on time through the free annual assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for MS-900, MS-102, MD-102, MS-700, MS-721.
- Cross-reference: [Volume XXXVII — Microsoft 365 and Modern Work](../volume-037-microsoft-365-modern-work/README.md).

**Knowledge checks**

1. Which single exam replaced the two-exam MS-100/MS-101 Enterprise Administrator?
2. Which credential maps to Intune, compliance, and Autopilot?
3. Why plan Microsoft 365 and SC credentials together?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of each M365 certification (MS-900, MS-102, MD-102, MS-700, MS-721), with the
domain weight from the Microsoft Learn study guide.

**Shared prerequisites** — a Microsoft 365 **developer tenant** and the
**Microsoft Graph PowerShell SDK** (`Connect-MgGraph`), **Teams PowerShell**
(`Connect-MicrosoftTeams`), and the **Purview/IPPS** module (`Connect-IPPSSession`).
Commands are illustrative walkthroughs against a tenant (read-only unless a
cleanup is shown); consent to the listed scopes at first connect. **Cost:** none
on a developer tenant.

### Lab 2.1 — MS-900: Describe cloud concepts (5–10%)

**Objective:** See the SaaS subscriptions the tenant consumes.

```powershell
Connect-MgGraph -Scopes "Organization.Read.All" -NoWelcome
(Get-MgSubscribedSku).SkuPartNumber
```

**Expected result:** SKU part numbers (e.g., `SPE_E3`, `ENTERPRISEPREMIUM`) —
the cloud (SaaS) services M365 delivers.

**Negative test:** try to "install" M365 on a server; it is SaaS — Microsoft
operates the infrastructure.

**Cleanup:** none (read-only).

### Lab 2.2 — MS-900: Describe Microsoft 365 apps and services (45–50%)

**Objective:** Enumerate the service plans bundled in the tenant.

```powershell
(Get-MgSubscribedSku).ServicePlans.ServicePlanName | Sort-Object -Unique | Select-Object -First 8
```

**Expected result:** service-plan names (`EXCHANGE_S_ENTERPRISE`,
`SHAREPOINTENTERPRISE`, `TEAMS1`, …) — the apps and services M365 bundles.

**Negative test:** assume every SKU includes Teams Phone; add-ons like Teams
Phone are separate service plans.

**Cleanup:** none.

### Lab 2.3 — MS-900: Describe security, compliance, privacy, and trust in Microsoft 365 (25–30%)

**Objective:** Read the tenant's Microsoft Secure Score.

```powershell
Connect-MgGraph -Scopes "SecurityEvents.Read.All" -NoWelcome
(Get-MgSecuritySecureScore -Top 1).CurrentScore
```

**Expected result:** a numeric Secure Score — the posture measure M365 exposes
for trust and security.

**Negative test:** treat a high Secure Score as "fully compliant"; it measures
configuration, not regulatory compliance.

**Cleanup:** none.

### Lab 2.4 — MS-900: Describe Microsoft 365 pricing, licensing, and support (10–15%)

**Objective:** Inspect license consumption (assigned vs available).

```powershell
Get-MgSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits, @{n='Total';e={$_.PrepaidUnits.Enabled}}
```

**Expected result:** per-SKU consumed vs total units — the licensing model you
manage and pay for.

**Negative test:** assign a plan that has a prerequisite service plan without
it; the dependency blocks activation.

**Cleanup:** none.

### Lab 2.5 — MS-102: Deploy and manage a Microsoft 365 tenant (25–30%)

**Objective:** Read core tenant/organization settings.

```powershell
Get-MgOrganization | Select-Object DisplayName, City, CountryLetterCode -ExpandProperty VerifiedDomains
```

**Expected result:** the tenant name, location, and verified domains — the
tenant configuration MS-102 manages.

**Negative test:** try to rename the initial `*.onmicrosoft.com` domain; it is
fixed — add a custom verified domain instead.

**Cleanup:** none.

### Lab 2.6 — MS-102: Implement and manage Microsoft Entra identity and access (25–30%)

**Objective:** Provision an Entra user (identity lifecycle).

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All" -NoWelcome
$d=(Get-MgOrganization).VerifiedDomains[0].Name
$pp=@{Password='TempP@ss2026!';ForceChangePasswordNextSignIn=$true}
New-MgUser -DisplayName "Lab User" -AccountEnabled -MailNickname labuser -UserPrincipalName "labuser@$d" -PasswordProfile $pp
```

**Expected result:** a new enabled user with a UPN — Entra identity
provisioning.

**Negative test:** omit the `PasswordProfile`; a cloud account cannot be created
without it.

**Cleanup:** `Remove-MgUser -UserId "labuser@$d"`.

### Lab 2.7 — MS-102: Manage security and threats by using Microsoft Defender XDR (30–35%)

**Objective:** Triage the Defender XDR incident queue.

```powershell
Connect-MgGraph -Scopes "SecurityIncident.Read.All" -NoWelcome
Get-MgSecurityIncident -Top 5 | Select-Object DisplayName, Severity, Status
```

**Expected result:** incidents with severity and status — the XDR queue an M365
admin works.

**Negative test:** expect endpoint alerts with no Defender for Endpoint
onboarding; unonboarded devices produce none.

**Cleanup:** none.

### Lab 2.8 — MS-102: Manage compliance by using Microsoft Purview (10–15%)

**Objective:** List retention (compliance) policies.

```powershell
Connect-IPPSSession
Get-RetentionCompliancePolicy | Select-Object Name, Enabled, Workload
```

**Expected result:** retention policies with their workloads — the Purview
controls MS-102 covers.

**Negative test:** apply a delete-retention policy without review; retention
actions can be irreversible.

**Cleanup:** none.

### Lab 2.9 — MD-102: Prepare infrastructure for devices (20–25%)

**Objective:** Read the Intune enrollment configuration.

```powershell
Connect-MgGraph -Scopes "DeviceManagementServiceConfig.Read.All" -NoWelcome
Get-MgDeviceManagementDeviceEnrollmentConfiguration | Select-Object DisplayName, Priority
```

**Expected result:** enrollment restriction/configuration profiles — the device
infrastructure Intune prepares.

**Negative test:** enroll a device with the MDM authority unset; enrollment
fails until Intune is the MDM authority.

**Cleanup:** none.

### Lab 2.10 — MD-102: Manage and maintain devices (25–30%)

**Objective:** List managed devices with their compliance state.

```powershell
Connect-MgGraph -Scopes "DeviceManagementManagedDevices.Read.All" -NoWelcome
Get-MgDeviceManagementManagedDevice -Top 5 | Select-Object DeviceName, OperatingSystem, ComplianceState
```

**Expected result:** enrolled devices with OS and compliance state — the managed
estate.

**Negative test:** expect a device to appear instantly after enrollment; sync
latency delays inventory.

**Cleanup:** none.

### Lab 2.11 — MD-102: Protect devices (15–20%)

**Objective:** Read a device compliance policy.

```powershell
Get-MgDeviceManagementDeviceCompliancePolicy -Top 3 | Select-Object DisplayName
```

**Expected result:** compliance policy names (BitLocker/OS-version rules) —
device protection controls.

**Negative test:** rely on a compliance policy with no Conditional Access;
without CA, non-compliant devices still get access.

**Cleanup:** none.

### Lab 2.12 — MD-102: Manage and secure applications (15–20%)

**Objective:** List deployed client apps.

```powershell
Get-MgDeviceAppManagementMobileApp -Top 5 | Select-Object DisplayName, AdditionalProperties
```

**Expected result:** app assignments (Win32/store/protected apps) — application
management.

**Negative test:** deploy a required app with no assignment group; unassigned
apps never install.

**Cleanup:** none.

### Lab 2.13 — MD-102: Optimize endpoint operations by using automation, monitoring, and reporting (10–15%)

**Objective:** Produce an endpoint compliance report metric.

```powershell
(Get-MgDeviceManagementManagedDevice -All).ComplianceState | Group-Object | Select-Object Name, Count
```

**Expected result:** device counts grouped by compliance state — the reporting
that drives endpoint operations.

**Negative test:** read one snapshot as a trend; endpoint reporting needs a
time series.

**Cleanup:** none.

### Lab 2.14 — MS-700: Configure and manage a Teams environment (40–45%)

**Objective:** Read org-wide Teams client configuration.

```powershell
Connect-MicrosoftTeams
Get-CsTeamsClientConfiguration | Select-Object Identity, AllowGuestUser
```

**Expected result:** the client configuration including guest access — the
org-wide environment settings.

**Negative test:** enable Teams guest access while Entra external collaboration
is off; both layers must allow it.

**Cleanup:** none.

### Lab 2.15 — MS-700: Manage teams, channels, chats, and apps (20–25%)

**Objective:** List teams and their visibility.

```powershell
Get-Team | Select-Object -First 3 DisplayName, Visibility
```

**Expected result:** teams with Public/Private visibility — the collaboration
objects you manage.

**Negative test:** delete a team to "archive" it; archiving preserves content,
deletion removes it — use archive.

**Cleanup:** none.

### Lab 2.16 — MS-700: Manage meetings and calling (15–20%)

**Objective:** Inspect the global meeting policy.

```powershell
Get-CsTeamsMeetingPolicy -Identity Global | Select-Object AllowCloudRecording, AllowMeetNow
```

**Expected result:** meeting policy settings (recording, meet-now) — meeting
governance.

**Negative test:** expect recordings with cloud recording off; recording needs
the policy on and OneDrive/SharePoint storage.

**Cleanup:** none.

### Lab 2.17 — MS-700: Monitor, report on, and troubleshoot Teams (15–20%)

**Objective:** Read the Teams upgrade/coexistence mode.

```powershell
Get-CsTeamsUpgradePolicy | Select-Object Identity, Mode
```

**Expected result:** upgrade policy modes (`TeamsOnly`, `Islands`) — a frequent
root cause when chats/calls route unexpectedly.

**Negative test:** troubleshoot missing chats without checking coexistence mode;
`Islands` splits activity across clients.

**Cleanup:** none.

### Lab 2.18 — MS-721: Plan and design collaboration communications systems (20–25%)

**Objective:** Read the tenant's voice-routing design.

```powershell
Get-CsOnlineVoiceRoutingPolicy | Select-Object Identity
```

**Expected result:** voice routing policies — the calling-design foundation for
Teams Phone.

**Negative test:** design Direct Routing with an uncertified SBC; unsupported
SBCs break call flows.

**Cleanup:** none.

### Lab 2.19 — MS-721: Configure and manage Teams meetings, webinars, and town halls (15–20%)

**Objective:** Inspect the events policy for webinars/town halls.

```powershell
Get-CsTeamsEventsPolicy | Select-Object Identity, AllowWebinars, AllowTownhalls
```

**Expected result:** event policy settings for webinars and town halls —
large-scale meeting governance.

**Negative test:** assume every license can host town halls; premium
capabilities require the right license.

**Cleanup:** none.

### Lab 2.20 — MS-721: Implement and configure Teams Phone (30–35%)

**Objective:** Read phone-number assignments.

```powershell
Get-CsPhoneNumberAssignment -Top 3 | Select-Object TelephoneNumber, NumberType, AssignedPstnTargetId
```

**Expected result:** assigned phone numbers with type — the Teams Phone
provisioning core to MS-721.

**Negative test:** assign a Calling Plan number with no Calling Plan license;
the assignment fails.

**Cleanup:** none.

### Lab 2.21 — MS-721: Configure and manage Teams Rooms and devices (20–25%)

**Objective:** List the resource accounts Teams Rooms/attendants use.

```powershell
Get-CsOnlineUser -Filter "AccountType -eq 'ResourceAccount'" | Select-Object -First 3 DisplayName
```

**Expected result:** resource accounts (used by Teams Rooms and auto attendants)
— room/device management.

**Negative test:** manage a Teams Room with no Teams Rooms license on its
resource account; features are license-gated.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Microsoft 365 family runs MS-900 (Fundamentals), MS-102 (Administrator
Expert), MD-102 (Endpoint Administrator), and MS-700/MS-721 (Teams and voice).
Older exams (MS-100/101, MS-500, MS-203, MS-720) retired or folded in. The
credentials map directly to the hands-on skills of Volume XXXVII and pair
naturally with the SC family.

- [ ] I can list the current M365 credentials and exam codes.
- [ ] I can map each to hands-on practice in Volume XXXVII.
- [ ] I know which older M365 exams retired.
- [ ] I can build an M365 administrator study path.
- [ ] I completed Labs 2.1–2.2 including each negative test.
