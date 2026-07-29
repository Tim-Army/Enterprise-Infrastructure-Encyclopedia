# Chapter 09: SharePoint Online, OneDrive, and Microsoft Teams

## Learning Objectives

- Administer SharePoint Online sites, storage, and the external-sharing model.
- Manage OneDrive for Business and Known Folder Move.
- Explain how Microsoft 365 Groups underpin Teams, SharePoint, and shared mailboxes.
- Administer Microsoft Teams with policies, teams, and the app catalog.
- Configure Teams Phone (voice) fundamentals and validate collaboration services.

## Theory and Architecture

The collaboration workloads share one substrate. A **Microsoft 365 Group** is
the membership object that, when created, provisions a **SharePoint site**, a
**group mailbox**, a **planner**, and — if it is a team — a **Microsoft Teams
team**. Understanding that a **Team is backed by a SharePoint site and a
group** explains where files live (the site's document library), how
membership flows, and why governance must span all three.

**SharePoint Online** hosts **sites**: **team sites** (group-connected,
collaborative) and **communication sites** (broadcast). Content lives in
**document libraries** and **lists**; **storage** is pooled at the tenant with
per-site quotas. **External sharing** is governed at two levels — the
**tenant** (the maximum permissiveness) and the **site** (which cannot exceed
the tenant) — with settings from **Anyone** (anonymous links) down to
**existing guests only** or **only people in your organization**. Sensitivity
labels (Chapter 10) can enforce site privacy and sharing.

**OneDrive for Business** is each user's personal SharePoint-backed library.
**Known Folder Move (KFM)** redirects the Windows Desktop, Documents, and
Pictures folders into OneDrive so user data is backed up to the cloud and
roams — a key endpoint-resilience feature managed by policy.

**Microsoft Teams** is the collaboration hub for chat, meetings, calling, and
apps. Administration is **policy-based**: **messaging**, **meeting**,
**calling**, **app permission/setup**, and **live events** policies are
assigned to users to control features. Teams and channels (standard, private,
shared) structure collaboration; the **app catalog** governs which apps are
allowed. **Teams Phone** adds PSTN calling through **Calling Plans**,
**Operator Connect**, or **Direct Routing**, with **phone number** assignment,
**voice routing**, **emergency calling**, and **auto attendants/call queues**.

## Design Considerations

Govern **group/team creation** — unrestricted creation leads to sprawl.
Restrict who can create Microsoft 365 groups (a security group of approved
creators), apply **naming policies** and **expiration policies**, and use
**sensitivity labels** to set default privacy and sharing on new
teams/sites. Decide the **external-sharing** posture at the tenant level
first (the ceiling), then tighten per site; prefer **guest** sharing with B2B
governance (Chapter 04) over **Anyone** links, and disable anonymous links
for sensitive content.

Roll out **OneDrive KFM** by policy so user data is protected and migration is
transparent, and set a reasonable **storage quota**. For **Teams**, design a
small set of **policies** per persona (standard user, meeting-heavy, external-
facing) rather than per-user settings, control the **app catalog** to allowed
apps, and plan **channel types** (private/shared) for the right access
boundaries. For **Teams Phone**, choose the PSTN connectivity model per region
(Calling Plans where available, Operator Connect/Direct Routing otherwise),
and always configure **emergency calling** and **dynamic emergency
addresses**.

## Implementation and Automation

SharePoint and Teams have dedicated modules. Manage SharePoint sharing and a
site:

```powershell
Install-Module Microsoft.Online.SharePoint.PowerShell -Scope AllUsers
Connect-SPOService -Url "https://contoso-admin.sharepoint.com"
Set-SPOTenant -SharingCapability ExternalUserSharingOnly          # tenant ceiling: guests, no anonymous
New-SPOSite -Url "https://contoso.sharepoint.com/sites/Project-Falcon" -Owner "aruiz@contoso.com" `
  -StorageQuota 5120 -Title "Project Falcon" -Template "STS#3"
Set-SPOSite -Identity "https://contoso.sharepoint.com/sites/Project-Falcon" -SharingCapability Disabled
```

Manage Teams with the Teams module:

```powershell
Install-Module MicrosoftTeams -Scope AllUsers
Connect-MicrosoftTeams
New-Team -DisplayName "Project Falcon" -Visibility Private
New-CsMessagingPolicy -Identity "NoExternalGifs" -AllowGiphy $false
Grant-CsMessagingPolicy -PolicyName "NoExternalGifs" -Identity "aruiz@contoso.com"
```

Assign a phone number (Calling Plan example):

```powershell
Set-CsPhoneNumberAssignment -Identity "aruiz@contoso.com" -PhoneNumber "+12025550123" -PhoneNumberType CallingPlan
Grant-CsTeamsCallingPolicy -Identity "aruiz@contoso.com" -PolicyName "AllowCalling"
```

## Validation and Troubleshooting

Confirm sharing, sites, policies, and voice:

```powershell
Get-SPOTenant | Select-Object SharingCapability
Get-SPOSite -Identity "https://contoso.sharepoint.com/sites/Project-Falcon" | Select-Object Url, SharingCapability, StorageQuota
Get-CsOnlineUser -Identity "aruiz@contoso.com" | Select-Object UserPrincipalName, LineUri, EnterpriseVoiceEnabled
```

Common issues: external sharing not working on a site because the **tenant
ceiling** is more restrictive than the site setting (the site can never exceed
the tenant); a **Team** created but its files/permissions confusing because
administration touched the Team but not the underlying **SharePoint site or
group**; **OneDrive KFM** not redirecting because the policy targets the wrong
group or the user has not signed in; a **Teams policy** not taking effect
because it can take time to propagate and the user must restart Teams; and
**Teams Phone** calls failing because the user is not **EnterpriseVoice
enabled**, lacks a **number assignment**, or has no **emergency address**.
The **Teams admin center** call analytics and the **SharePoint admin center**
site details resolve most issues.

## Security and Best Practices

Control **group/team sprawl** with creation restrictions, naming, and
expiration, and set **default privacy/sharing** with sensitivity labels. Set
the **external-sharing ceiling** conservatively at the tenant and tighten per
site; prefer **governed guest sharing** over anonymous links and disable
anonymous links for sensitive sites. Protect user data with **OneDrive KFM**
and reasonable quotas. Keep **Teams app catalog** to allowed apps, use
**private/shared channels** for access boundaries, and manage features by
**policy** per persona. For **Teams Phone**, always configure **emergency
calling** and dynamic addresses, and secure **Direct Routing** SBCs. Apply
**Conditional Access** and **sensitivity labels** to SharePoint/OneDrive/Teams
so data protection (Chapter 10) is consistent across the collaboration stack.

## References and Knowledge Checks

- Microsoft Learn: *SharePoint Online administration*; *External sharing*; *OneDrive Known Folder Move*; *Microsoft Teams administration*; *Teams Phone*.
- Microsoft Learn: MS-700 — *Manage Teams*; MS-721 — *Teams voice*; MS-102 — *Manage SharePoint and OneDrive*.

**Knowledge checks**

1. What does creating a Microsoft 365 Group provision, and why does that matter for governance?
2. Why can a site's external-sharing setting never exceed the tenant setting?
3. What three things must be true for a user to make PSTN calls in Teams Phone?

## Hands-On Lab

Topic-level walkthroughs for MS-700/MS-102 collaboration skills.

**Shared prerequisites for Labs 9.1–9.4** — a Microsoft 365 tenant, the
SharePoint and Teams PowerShell modules, and SharePoint/Teams admin rights.
**Cost:** none.

### Lab 9.1 — Set the external-sharing ceiling (Topic: SharePoint sharing)

**Objective:** Cap tenant sharing at governed guests.

```powershell
Connect-SPOService -Url "https://contoso-admin.sharepoint.com"
Set-SPOTenant -SharingCapability ExternalUserSharingOnly
Get-SPOTenant | Select-Object SharingCapability
```

**Expected result:** the tenant allows guest sharing but not anonymous links —
the ceiling every site inherits.

**Negative test:** set a site to `ExternalUserAndGuestSharing` (anonymous)
while the tenant is `ExternalUserSharingOnly`; the site cannot exceed the
tenant — the stricter tenant setting wins.

**Cleanup:** restore the prior tenant sharing setting.

### Lab 9.2 — Create a site with a quota and disable its sharing (Topic: Sites and storage)

**Objective:** Provision a controlled site.

```powershell
New-SPOSite -Url "https://contoso.sharepoint.com/sites/Falcon" -Owner "admin@contoso.com" `
  -StorageQuota 5120 -Title "Falcon" -Template "STS#3"
Set-SPOSite -Identity "https://contoso.sharepoint.com/sites/Falcon" -SharingCapability Disabled
Get-SPOSite -Identity "https://contoso.sharepoint.com/sites/Falcon" | Select-Object Url, SharingCapability, StorageQuota
```

**Expected result:** the site exists with a 5 GB quota and sharing disabled —
per-site control within the tenant ceiling.

**Negative test:** set a quota larger than the tenant pool allows; it is capped
— site quotas draw from the tenant storage pool.

**Cleanup:** `Remove-SPOSite -Identity "https://contoso.sharepoint.com/sites/Falcon"`.

### Lab 9.3 — Create a Team and assign a messaging policy (Topic: Teams administration)

**Objective:** Stand up a team and control a feature.

```powershell
Connect-MicrosoftTeams
New-Team -DisplayName "Falcon" -Visibility Private
New-CsMessagingPolicy -Identity "NoGifs" -AllowGiphy $false
Grant-CsMessagingPolicy -PolicyName "NoGifs" -Identity "aruiz@contoso.com"
Get-CsMessagingPolicy -Identity "NoGifs" | Select-Object Identity, AllowGiphy
```

**Expected result:** a private team exists and the user has a messaging policy
disabling GIFs — Teams features are governed by assigned policies.

**Negative test:** expect the policy to apply instantly; it can take time to
propagate and needs a Teams restart — allow for propagation.

**Cleanup:** remove the team and the messaging policy.

### Lab 9.4 — Check a user's voice enablement (Topic: Teams Phone)

**Objective:** Confirm the prerequisites for PSTN calling.

```powershell
Get-CsOnlineUser -Identity "aruiz@contoso.com" |
  Select-Object UserPrincipalName, EnterpriseVoiceEnabled, LineUri, OnlineVoiceRoutingPolicy
```

**Expected result:** a fully provisioned user shows `EnterpriseVoiceEnabled
True` and a `LineUri` — both are required to place PSTN calls.

**Negative test:** check a user with no number assignment; `LineUri` is empty
and calls fail — assign a number and enable enterprise voice first.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsoft 365 Groups underpin Teams, SharePoint sites, and group mailboxes.
SharePoint sites and OneDrive host content with a two-level external-sharing
model (tenant ceiling, site setting) and KFM for user-data resilience. Teams
is administered by policy, with Teams Phone adding governed PSTN calling.
Governance must span group, site, and team together.

- [ ] I can administer SharePoint sites, storage, and sharing.
- [ ] I can deploy OneDrive KFM and explain the group substrate.
- [ ] I can manage Teams with policies and the app catalog.
- [ ] I can configure and validate Teams Phone fundamentals.
- [ ] I completed Labs 9.1–9.4 including each negative test.
