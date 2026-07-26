# Chapter 11: Microsoft Defender XDR, Secure Score, Copilot Governance, and Capstone

## Learning Objectives

- Describe Microsoft Defender XDR and its workloads across identity, endpoints, email, and cloud apps.
- Configure Defender for Office 365 Safe Links and Safe Attachments and Defender for Endpoint onboarding.
- Investigate incidents and use advanced hunting across the unified portal.
- Raise posture with Microsoft Secure Score and govern Microsoft 365 Copilot and agents.
- Integrate the volume's services in a provision-to-protect capstone.

## Theory and Architecture

**Microsoft Defender XDR** is the extended detection and response suite that
correlates signals across the estate into unified **incidents**. Its
workloads are **Defender for Identity** (on-premises AD and Entra signals —
Kerberoasting, lateral movement), **Defender for Endpoint** (endpoint EDR,
vulnerability management, attack-surface reduction), **Defender for Office
365** (email and collaboration — Safe Links, Safe Attachments, anti-phishing),
and **Defender for Cloud Apps** (SaaS discovery, session control, and the
CASB layer). Alerts from each are stitched into **incidents** in the unified
**Microsoft Defender portal**, where **advanced hunting** (KQL over a shared
schema) and **automated investigation and response (AIR)** speed triage and
remediation. This is where the security-operations analyst (SC-200) works.

**Defender for Office 365** hardens the mail flow of Chapter 08. **Safe
Attachments** detonate attachments in a sandbox before delivery; **Safe
Links** rewrite and time-of-click-check URLs in mail and Office/Teams; and
enhanced **anti-phishing** adds user/domain impersonation and mailbox
intelligence. **Defender for Endpoint** onboards devices (via Intune,
Chapter 06) for EDR, exposes a **vulnerability management** view, and feeds
device risk back to Conditional Access.

**Microsoft Secure Score** measures security posture as a percentage against a
catalog of **improvement actions** across identity, devices, apps, and data,
with points and implementation guidance — the running scorecard for hardening
the tenant.

**Microsoft 365 Copilot and agents** are now part of the administered surface.
Copilot honors the existing permission and label model — it can only surface
content a user can already access — so **oversharing** and **label/DLP
hygiene** (Chapters 09–10) directly govern what Copilot exposes. The **Copilot
and Agent Administration** discipline covers licensing, access, agent
governance (which agents are allowed, what data they reach), and monitoring —
a fundamentals credential now exists for exactly this.

## Design Considerations

Enable **Defender for Office 365** protection through the **Standard/Strict
preset policies** so Safe Links, Safe Attachments, and anti-phishing are on
without hand-building each policy. **Onboard endpoints** to Defender for
Endpoint through Intune and feed **device risk** into Conditional Access.
Turn on **Defender for Identity** sensors on domain controllers (Volume XXXVI)
and **Defender for Cloud Apps** for SaaS visibility and session control.

Operate from the **unified incidents** queue, tune **AIR** to auto-remediate
high-confidence detections, and build **advanced hunting** queries for your
top risks. Drive continuous improvement with **Secure Score**, prioritizing
high-impact, low-friction actions (MFA everywhere, block legacy auth, disable
risky consent). For **Copilot governance**, fix **oversharing first** (site
access reviews, sensitivity labels, DLP), decide **which agents** are allowed,
scope agent data access, and monitor usage — Copilot amplifies whatever
permission and labeling posture already exists, good or bad.

## Implementation and Automation

Apply the Strict preset and enable Safe Attachments/Links (Security &
Compliance / Defender PowerShell):

```powershell
Connect-ExchangeOnline -UserPrincipalName admin@contoso.com
New-SafeAttachmentPolicy -Name "SA-Strict" -Enable $true -Action Block
New-SafeAttachmentRule -Name "SA-Strict" -SafeAttachmentPolicy "SA-Strict" -RecipientDomainIs "contoso.com"
New-SafeLinksPolicy -Name "SL-Strict" -EnableSafeLinksForEmail $true -EnableSafeLinksForTeams $true -ScanUrls $true
New-SafeLinksRule -Name "SL-Strict" -SafeLinksPolicy "SL-Strict" -RecipientDomainIs "contoso.com"
```

Read incidents and Secure Score with Graph:

```powershell
Connect-MgGraph -Scopes "SecurityEvents.Read.All","SecurityIncident.Read.All"
Get-MgSecurityIncident -Top 5 | Select-Object DisplayName, Severity, Status, CreatedDateTime
Get-MgSecuritySecureScore -Top 1 | Select-Object CurrentScore, MaxScore, @{n='Pct';e={[math]::Round(100*$_.CurrentScore/$_.MaxScore)}}
```

Advanced hunting query (Defender portal or Graph security API), for example
failed sign-ins by IP:

```kusto
SigninLogs
| where TimeGenerated > ago(1d) and ResultType != 0
| summarize attempts = count() by IPAddress, UserPrincipalName
| where attempts > 10
| order by attempts desc
```

## Validation and Troubleshooting

Confirm protection, onboarding, incidents, and score:

```powershell
Get-SafeAttachmentPolicy | Select-Object Name, Enable, Action
Get-MgSecurityIncident -Top 5 | Select-Object DisplayName, Severity, Status
Get-MgSecuritySecureScore -Top 1 | Select-Object CurrentScore, MaxScore
# Endpoint onboarding: Defender portal > Assets > Devices shows onboarded state
```

Common issues: **Safe Attachments/Links** not applying because the rule's
recipient scope is wrong or the preset policy already governs those users
(preset wins by priority); **Defender for Endpoint** devices not onboarded
because the Intune onboarding policy did not deploy or the device is not
enrolled (Chapter 05); **incidents** missing expected alerts because a
workload (Identity, Cloud Apps) is not enabled or licensed; **Secure Score**
not moving after a change because it recalculates on a cycle; and **Copilot**
surfacing content a user should not see — almost always an **oversharing** or
**missing-label** problem in SharePoint/OneDrive, not a Copilot bug. Fix the
permission and labeling posture and Copilot's exposure narrows accordingly.

## Security and Best Practices

Turn on **Defender across all workloads** (Identity, Endpoint, Office 365,
Cloud Apps) and operate from **unified incidents** with **AIR**. Use **preset
security policies** for a strong, maintained baseline. Feed **device and user
risk** into **Conditional Access** so posture gates access. Drive hardening
with **Secure Score**, closing high-impact actions first. For **Copilot and
agents**, treat **oversharing and labeling as the primary control** — remediate
site/OneDrive access, apply sensitivity labels and DLP, then govern which
agents are permitted and what data they reach, and monitor usage. Enable
**audit logging** and integrate Defender with the SIEM/SOAR (Volume XI) for
correlation and response. Security is continuous: detect, investigate,
remediate, and improve the score.

## References and Knowledge Checks

- Microsoft Learn: *Microsoft Defender XDR*; *Defender for Office 365 / Endpoint / Identity / Cloud Apps*; *Microsoft Secure Score*; *Microsoft 365 Copilot governance*.
- Microsoft Learn: SC-200 — *Mitigate threats using Microsoft Defender XDR*; MS-102 — *Manage security and threats*.

**Knowledge checks**

1. What four workloads does Defender XDR correlate into unified incidents?
2. Why is oversharing the primary risk to govern before deploying Copilot?
3. How does device risk from Defender for Endpoint strengthen Conditional Access?

## Hands-On Lab

Topic-level walkthroughs for SC-200/MS-102 threat-protection skills, closing
with a capstone.

**Shared prerequisites for Labs 11.1–11.4** — a Microsoft 365 tenant with
Defender for Office 365 and Defender XDR (E5/trial), the Exchange and Graph
sessions, and admin rights. **Cost:** none (trial licensing).

### Lab 11.1 — Enable Safe Attachments (Topic: Defender for Office 365)

**Objective:** Sandbox-detonate email attachments.

```powershell
New-SafeAttachmentPolicy -Name "SA-Strict" -Enable $true -Action Block
New-SafeAttachmentRule -Name "SA-Strict" -SafeAttachmentPolicy "SA-Strict" -RecipientDomainIs "contoso.com"
Get-SafeAttachmentPolicy | Select-Object Name, Enable, Action
```

**Expected result:** attachments to your domain are detonated and malicious
ones blocked before delivery — protection beyond baseline EOP.

**Negative test:** create the rule scoped to a domain you do not own; it never
matches your mail — the recipient scope must be your accepted domain.

**Cleanup:** remove the Safe Attachments rule and policy.

### Lab 11.2 — Read the incidents queue (Topic: Investigation)

**Objective:** See correlated incidents.

```powershell
Connect-MgGraph -Scopes "SecurityIncident.Read.All"
Get-MgSecurityIncident -Top 10 | Select-Object DisplayName, Severity, Status, CreatedDateTime |
  Sort-Object CreatedDateTime -Descending
```

**Expected result:** incidents list with severity and status — Defender XDR
correlates alerts across workloads into a single incident per attack.

**Negative test:** expect incidents from a workload that is not enabled (e.g.,
Cloud Apps) — none appear until that workload is licensed and turned on.

**Cleanup:** none (read-only).

### Lab 11.3 — Read Secure Score (Topic: Posture management)

**Objective:** Measure and target improvement.

```powershell
Connect-MgGraph -Scopes "SecurityEvents.Read.All"
Get-MgSecuritySecureScore -Top 1 |
  Select-Object CurrentScore, MaxScore, @{n='Pct';e={[math]::Round(100*$_.CurrentScore/$_.MaxScore)}}
```

**Expected result:** the current score, maximum, and percentage — the running
scorecard whose improvement actions guide hardening.

**Negative test:** implement one action and re-check immediately; the score may
not move until the next recalculation — Secure Score updates on a cycle.

**Cleanup:** none (read-only).

### Lab 11.4 — Capstone: onboard-to-protect a new user and device (Topic: Integrate the volume)

**Objective:** Combine the volume's services in one workflow.

```powershell
# 1. Identity (Ch02): create the user, add to role/license groups
$dom=(Get-MgOrganization).VerifiedDomains[0].Name
New-MgUser -DisplayName "Sam Lee" -UserPrincipalName "slee@$dom" -MailNickname "slee" -AccountEnabled `
  -UsageLocation "US" -PasswordProfile @{Password='Start-123!';ForceChangePasswordNextSignIn=$true}
# 2. Access (Ch03): user is covered by the require-MFA + block-legacy CA policies
# 3. Endpoint (Ch05/06/07): device auto-enrolls via Autopilot, gets compliance + baseline + apps
# 4. Data (Ch10): sensitivity labels + DLP protect what Sam creates
# 5. Protection (Ch11): device onboarded to Defender for Endpoint; risk feeds Conditional Access
Get-MgUser -UserId "slee@$dom" | Select-Object DisplayName, AccountEnabled, UsageLocation
```

**Expected result:** Sam has an identity governed by Conditional Access, a
compliant Autopilot-provisioned device with apps, data protected by labels and
DLP, and endpoint protection whose risk gates access — the whole volume in one
onboarding.

**Negative test:** skip the license/CA group membership; Sam can sign in but
lacks services and is not covered by access policies — group membership drives
entitlement and protection.

**Cleanup:** `Remove-MgUser -UserId "slee@$dom"` and remove any test device.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Defender XDR correlates identity, endpoint, email, and cloud-app signals into
unified incidents, with Safe Links/Attachments hardening mail and EDR
onboarding feeding device risk to Conditional Access. Secure Score drives
continuous hardening. Microsoft 365 Copilot honors the existing permission and
label model, so oversharing and labeling hygiene are the primary Copilot
controls. The capstone ties identity, access, endpoint, data, and protection
together.

- [ ] I can describe Defender XDR's workloads and unified incidents.
- [ ] I can enable Defender for Office 365 and onboard endpoints.
- [ ] I can raise posture with Secure Score.
- [ ] I can govern Copilot by fixing oversharing and labeling first.
- [ ] I completed Labs 11.1–11.4, including the capstone and each negative test.
