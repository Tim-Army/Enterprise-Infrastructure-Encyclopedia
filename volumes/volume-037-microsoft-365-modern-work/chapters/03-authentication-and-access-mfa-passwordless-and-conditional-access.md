# Chapter 03: Authentication and Access — MFA, Passwordless, and Conditional Access

## Learning Objectives

- Compare authentication methods and choose phishing-resistant options.
- Deploy multifactor and passwordless authentication with the Authentication methods policy.
- Design Conditional Access policies from signals, conditions, and grant/session controls.
- Apply Entra ID Protection risk detection to user and sign-in risk.
- Validate access with the What If tool and troubleshoot with the sign-in logs.

## Theory and Architecture

Authentication proves who is signing in; **Conditional Access** decides
whether, and under what conditions, to allow the access. Together they are
the heart of Zero Trust in Microsoft 365: never trust, always verify, and
verify explicitly from multiple signals.

**Authentication methods** range in strength. Passwords alone are weak;
**multifactor authentication (MFA)** adds a second factor. Not all second
factors are equal: SMS and voice are phishable and being deprecated in favor
of the **Microsoft Authenticator** app (push with number matching),
**FIDO2 security keys**, **Windows Hello for Business**, and **certificate-
based authentication** — the last three are **phishing-resistant** because
the credential is bound to the device and cannot be replayed. The unified
**Authentication methods policy** in Entra controls which methods are
available and to whom, replacing the legacy per-user MFA and SSPR method
settings.

**Conditional Access (CA)** is an if-then policy engine evaluated at sign-in.
The **if** is assignments and conditions: **users/groups**, **target
resources** (cloud apps or actions), and **conditions** (sign-in risk, user
risk, device platform, location/named IPs, client app, device state). The
**then** is **grant controls** (block, or require MFA, compliant device,
hybrid-joined device, approved app, terms of use — combined with AND/OR) and
**session controls** (sign-in frequency, persistent browser, app-enforced
restrictions, and Conditional Access App Control via Defender for Cloud
Apps). Policies are **additive** and evaluated together; any **block** wins.

**Entra ID Protection** (P2) adds risk: **sign-in risk** (this authentication
looks malicious — impossible travel, anonymous IP, token anomalies) and
**user risk** (this identity is likely compromised — leaked credentials).
Risk becomes a CA condition, so a risky sign-in can be forced through MFA and
a risky user forced to reset their password, automatically.

## Design Considerations

Move toward **phishing-resistant, passwordless** authentication: enable
Microsoft Authenticator with number matching as the baseline, and roll out
FIDO2 keys and Windows Hello for privileged and high-value users. Use the
**Authentication methods policy** to enable methods by group and to **migrate
off** SMS/voice. Register users through **combined security-information
registration** (MFA + SSPR in one flow), ideally gated by a CA policy that
requires registration from a trusted location.

Design **Conditional Access** as a small, layered, well-named set, not a
sprawl. A common baseline: require MFA for all users to all apps; block
legacy authentication (which cannot do MFA and is a top attack vector);
require compliant or hybrid-joined devices for sensitive apps; require MFA
or block from risky sign-ins; and force password change on high user risk.
Always keep **emergency-access accounts excluded** from CA so a
misconfiguration cannot lock everyone out, and stage policies in **report-
only** mode first to see impact before enforcing.

Treat **named locations** and **device state** as trust signals, not
security by themselves — IP can be spoofed and location is coarse. Prefer
**device compliance** (Intune, Chapter 06) and phishing-resistant methods as
the strong controls.

## Implementation and Automation

Enable Microsoft Authenticator for a group via the Authentication methods
policy (Graph):

```powershell
Connect-MgGraph -Scopes "Policy.ReadWrite.AuthenticationMethod","Policy.Read.All"
$grpId = (Get-MgGroup -Filter "displayName eq 'DYN-Sales'").Id
Update-MgPolicyAuthenticationMethodPolicyAuthenticationMethodConfiguration `
  -AuthenticationMethodConfigurationId "MicrosoftAuthenticator" `
  -BodyParameter @{ state="enabled"; includeTargets=@(@{ id=$grpId; targetType="group" }) }
```

Create a Conditional Access policy in report-only that requires MFA:

```powershell
$params = @{
  displayName = "CA01 - Require MFA for all users (report-only)"
  state = "enabledForReportingButNotEnforced"
  conditions = @{
    users = @{ includeUsers = @("All"); excludeGroups = @("<breakglass-group-id>") }
    applications = @{ includeApplications = @("All") }
  }
  grantControls = @{ operator = "OR"; builtInControls = @("mfa") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $params
```

Block legacy authentication:

```powershell
$legacy = @{
  displayName="CA02 - Block legacy authentication"; state="enabled"
  conditions=@{ users=@{includeUsers=@("All");excludeGroups=@("<breakglass-group-id>")}
    applications=@{includeApplications=@("All")}
    clientAppTypes=@("exchangeActiveSync","other") }
  grantControls=@{ operator="OR"; builtInControls=@("block") } }
New-MgIdentityConditionalAccessPolicy -BodyParameter $legacy
```

## Validation and Troubleshooting

Use **What If** (portal) to predict policy application, and the sign-in logs
to see what actually happened:

```powershell
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State
# Sign-in logs (AuditLog.Read.All): which CA policies applied and their result
Get-MgAuditLogSignIn -Top 5 |
  Select-Object UserPrincipalName, AppDisplayName, @{n='CA';e={($_.AppliedConditionalAccessPolicies |
    ForEach-Object { "$($_.DisplayName)=$($_.Result)" }) -join '; '}}
```

The sign-in log's **Conditional Access** tab shows each policy and whether it
was `success`, `failure`, `notApplied`, or `reportOnlyFailure`. Common
issues: a user locked out because a policy required a control they cannot
satisfy (device compliance before Intune is deployed) — stage in report-only
first; **legacy auth** still working because the blocking policy excludes an
app or the client-app condition is wrong; MFA prompting more than expected
because sign-in frequency or a risk policy is triggering; and the dreaded
**self-lockout** — always exclude break-glass accounts and verify with What
If before enforcing.

## Security and Best Practices

Make **MFA universal** and move to **phishing-resistant, passwordless**
methods for everyone, prioritizing admins. **Block legacy authentication**
tenant-wide. Use **Entra ID Protection** to require MFA on risky sign-ins and
password reset on risky users. Keep CA policies **few, named, layered, and
staged in report-only**, and always **exclude break-glass accounts**. Require
**compliant or hybrid-joined devices** for sensitive resources. Enforce
**sign-in frequency** and **no persistent browser** on unmanaged devices.
Review CA changes through change control and monitor the sign-in and audit
logs continuously. Treat Conditional Access as the tenant's front door — test
every change before it is enforced.

## References and Knowledge Checks

- Microsoft Learn: *Authentication methods policy*; *Conditional Access*; *Entra ID Protection*; *Passwordless authentication*.
- Microsoft Learn: SC-300 — *Implement authentication and access management*; MS-102 — *Manage secure access*.

**Knowledge checks**

1. Why are FIDO2 keys and Windows Hello considered phishing-resistant while SMS is not?
2. What are the grant controls in Conditional Access, and how do AND/OR combine them?
3. Why must you exclude break-glass accounts from Conditional Access?

## Hands-On Lab

Topic-level walkthroughs for SC-300 access-management skills. Conditional
Access labs are staged in **report-only** to avoid lockout.

**Shared prerequisites for Labs 3.1–3.4** — a Microsoft 365 tenant with Entra
ID P1 (P2 for risk), a Graph session with `Policy.ReadWrite.ConditionalAccess`
and `Policy.ReadWrite.AuthenticationMethod`, a break-glass group, and admin
rights. **Cost:** none (trial licensing).

### Lab 3.1 — Enable Microsoft Authenticator for a group (Topic: Authentication methods)

**Objective:** Turn on app-based MFA for a population.

```powershell
$grpId = (Get-MgGroup -Filter "displayName eq 'DYN-Sales'").Id
Update-MgPolicyAuthenticationMethodPolicyAuthenticationMethodConfiguration `
  -AuthenticationMethodConfigurationId "MicrosoftAuthenticator" `
  -BodyParameter @{ state="enabled"; includeTargets=@(@{ id=$grpId; targetType="group" }) }
Get-MgPolicyAuthenticationMethodPolicyAuthenticationMethodConfiguration `
  -AuthenticationMethodConfigurationId "MicrosoftAuthenticator" | Select-Object State
```

**Expected result:** Microsoft Authenticator is `enabled` for the group — the
unified methods policy targets methods by group.

**Negative test:** target a group that does not exist; the update errors —
the target must be a real group id.

**Rollback:** set state back to `disabled` for the group if lab-only.

### Lab 3.2 — Create a report-only MFA policy (Topic: Conditional Access)

**Objective:** Require MFA without risking lockout.

```powershell
$bg = (Get-MgGroup -Filter "displayName eq 'SG-BreakGlass'").Id
New-MgIdentityConditionalAccessPolicy -BodyParameter @{
  displayName="CA01 - Require MFA (report-only)"; state="enabledForReportingButNotEnforced"
  conditions=@{ users=@{includeUsers=@("All");excludeGroups=@($bg)}; applications=@{includeApplications=@("All")} }
  grantControls=@{ operator="OR"; builtInControls=@("mfa") } }
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State
```

**Expected result:** the policy exists in `enabledForReportingButNotEnforced`
— report-only shows impact in the sign-in logs before enforcement.

**Negative test:** create the same policy `enabled` without excluding
break-glass; you risk locking out every admin — always exclude break-glass
and stage first.

**Rollback:** `Remove-MgIdentityConditionalAccessPolicy -ConditionalAccessPolicyId <id>`.

### Lab 3.3 — Block legacy authentication (Topic: Reduce attack surface)

**Objective:** Stop protocols that cannot do MFA.

```powershell
$bg = (Get-MgGroup -Filter "displayName eq 'SG-BreakGlass'").Id
New-MgIdentityConditionalAccessPolicy -BodyParameter @{
  displayName="CA02 - Block legacy auth"; state="enabledForReportingButNotEnforced"
  conditions=@{ users=@{includeUsers=@("All");excludeGroups=@($bg)}; applications=@{includeApplications=@("All")}
    clientAppTypes=@("exchangeActiveSync","other") }
  grantControls=@{ operator="OR"; builtInControls=@("block") } }
```

**Expected result:** a report-only policy targets legacy client-app types for
blocking — legacy auth is a top attack vector because it bypasses MFA.

**Negative test:** set `clientAppTypes=@("all")`; the policy would also catch
modern auth and could block everything — target only the legacy client types.

**Rollback:** remove the policy after reviewing report-only impact.

### Lab 3.4 — Read Conditional Access results from sign-in logs (Topic: Validate access)

**Objective:** Prove which policies applied.

```powershell
Get-MgAuditLogSignIn -Top 5 | Select-Object UserPrincipalName, AppDisplayName,
  @{n='CApolicies';e={ ($_.AppliedConditionalAccessPolicies | ForEach-Object { "$($_.DisplayName)=$($_.Result)" }) -join '; ' }}
```

**Expected result:** each sign-in lists the CA policies evaluated and their
result (`reportOnlySuccess`, `success`, `notApplied`) — the sign-in log is the
authoritative record of access decisions.

**Negative test:** query sign-ins immediately after creating a policy; recent
sign-ins predate it and show `notApplied` — evaluate against sign-ins after
the policy existed.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Authentication proves identity and Conditional Access governs access.
Phishing-resistant, passwordless methods (Authenticator with number
matching, FIDO2, Windows Hello) beat SMS/voice; the Authentication methods
policy controls them. Conditional Access combines users, apps, and
conditions with grant and session controls, strengthened by Entra ID
Protection risk. Stage in report-only and exclude break-glass accounts.

- [ ] I can choose phishing-resistant authentication methods.
- [ ] I can design layered Conditional Access from signals and controls.
- [ ] I can apply sign-in and user risk with Entra ID Protection.
- [ ] I can validate with What If and the sign-in logs.
- [ ] I completed Labs 3.1–3.4 including each negative test.
