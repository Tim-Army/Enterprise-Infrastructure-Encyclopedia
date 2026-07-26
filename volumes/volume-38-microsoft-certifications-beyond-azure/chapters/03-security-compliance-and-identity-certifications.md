# Chapter 03: Security, Compliance, and Identity Certifications

## Learning Objectives

- Enumerate the current SC-family certifications and their exam codes.
- Distinguish the identity, operations, information-security, and architect roles.
- Recognize the SC renames and additions — SC-401 and the new SC-500.
- Map each credential to hands-on skills across Volumes XXXVII and X.
- Build a security-focused study path from Fundamentals to Expert.

## Theory and Architecture

The **Security, Compliance, and Identity (SC)** family certifies the security
roles across Microsoft 365, Entra ID, Azure, and Microsoft Purview and
Defender. As verified on Microsoft Learn (26 July 2026), the current
credentials are:

- **Microsoft Certified: Security, Compliance, and Identity Fundamentals** —
  exam **SC-900** (Fundamentals). Zero Trust concepts and the Microsoft
  identity, security, compliance, and Defender/Purview landscape.
- **Microsoft Certified: Identity and Access Administrator Associate** — exam
  **SC-300** (Associate). Entra ID identities, authentication, Conditional
  Access, and identity governance.
- **Microsoft Certified: Security Operations Analyst Associate** — exam
  **SC-200** (Associate). Threat detection and response with Microsoft
  Defender XDR and Sentinel.
- **Microsoft Certified: Information Security Administrator Associate** — exam
  **SC-401** (Associate). Information protection, DLP, and compliance with
  Microsoft Purview. **SC-401 replaced the retired SC-400** (Information
  Protection Administrator).
- **Microsoft Certified: Cybersecurity Architect Expert** — exam **SC-100**
  (Expert). Design a Zero Trust security strategy and architecture across
  identity, data, applications, and infrastructure.
- **Microsoft Certified: Cloud and AI Security Engineer Associate** — exam
  **SC-500** (Associate). A newer credential covering securing cloud and AI
  workloads — one of the post-2025 additions to the family.

## Design Considerations

The SC family has clear role lanes. **SC-300** is for **identity and access**
engineers; **SC-200** for the **SOC/threat** analyst; **SC-401** for
**information protection and compliance**; **SC-100** for the **security
architect**; and the new **SC-500** for **cloud and AI security**
engineering — a signal of how much AI-workload security now matters.

Sequence deliberately: **SC-900 → (SC-300 and/or SC-200 and/or SC-401) →
SC-100**. SC-100 is Expert and cross-domain, and Microsoft recommends real
experience with at least one Associate area first. Pair SC credentials with
the hands-on identity and security work in **Volume XXXVII** (Conditional
Access, Purview, Defender XDR — Chapters 03, 10, 11) and the broader security
foundations in **Volume X — Enterprise Cybersecurity**.

## Implementation and Automation

Verify the SC family and the renames from Microsoft Learn:

```bash
for slug in security-compliance-and-identity-fundamentals identity-and-access-administrator \
            security-operations-analyst information-security-administrator \
            cybersecurity-architect-expert cloud-and-ai-security-engineer-associate; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bSC-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# information-security-administrator -> SC-401  (replaced SC-400)
# cloud-and-ai-security-engineer-associate -> SC-500  (new)
```

## Validation and Troubleshooting

Map credentials to blueprints and practice:

| Credential | Exam | Tier | Practice in |
| --- | --- | --- | --- |
| SC Fundamentals | SC-900 | Fundamentals | Vol X Ch 01; Vol XXXVII Ch 03 |
| Identity and Access Administrator | SC-300 | Associate | Vol XXXVII Ch 02–04 |
| Security Operations Analyst | SC-200 | Associate | Vol XXXVII Ch 11; Vol X |
| Information Security Administrator | SC-401 | Associate | Vol XXXVII Ch 10 |
| Cybersecurity Architect Expert | SC-100 | Expert | Vol X; Vol XXXVII |
| Cloud and AI Security Engineer | SC-500 | Associate | Vol XXXVII Ch 11; Vol XXXIII |

Common pitfalls: studying **SC-400** (retired — the current information-
security exam is **SC-401**); missing the new **SC-500** in an older program
map; and taking **SC-100** without Associate-level experience — as an Expert
architecture exam it assumes fluency across identity, data, and infrastructure
security.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
get hands-on with Conditional Access, Purview, and Defender in a developer
tenant (Volume XXXVII). Verify **SC-401** and **SC-500** on Learn — both are
recent changes an older study guide will get wrong. Because the SC family
overlaps Microsoft 365 and Azure security, plan it alongside **MS-102** and
the Azure security content (Volume XXXIII). Renew annually through the free
assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for SC-900, SC-300, SC-200, SC-401, SC-100, SC-500.
- Cross-reference: [Volume XXXVII](../volume-37-microsoft-365-modern-work/README.md), [Volume X — Enterprise Cybersecurity](../volume-10-enterprise-cybersecurity/README.md).

**Knowledge checks**

1. Which exam replaced SC-400, and what does it cover?
2. What role does the new SC-500 certify?
3. Why sequence SC-100 after an Associate credential?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of the SC family (SC-900, SC-300, SC-200, SC-401, SC-100, SC-500).

**Shared prerequisites** — a Microsoft 365/Azure **developer tenant**, the
**Microsoft Graph PowerShell SDK**, the **Purview/IPPS** module
(`Connect-IPPSSession`), and the **Azure CLI** (`az login`) for the SC-500 and
SC-100 infrastructure labs. Commands are illustrative walkthroughs against a
tenant; consent to the listed scopes. **Cost:** none on a developer tenant.

### Lab 3.1 — SC-900: Describe the concepts of security, compliance, and identity (10–15%)

**Objective:** Identify the tenant's identity authority (cloud vs hybrid).

```powershell
Connect-MgGraph -Scopes "Organization.Read.All" -NoWelcome
Get-MgOrganization | Select-Object DisplayName, OnPremisesSyncEnabled
```

**Expected result:** the tenant and whether it syncs from on-prem AD — a core
identity concept (cloud vs hybrid).

**Negative test:** assume cloud identity removes shared responsibility; the
customer still owns identity governance.

**Cleanup:** none.

### Lab 3.2 — SC-900: Describe the capabilities of Microsoft Entra (25–30%)

**Objective:** Enumerate Entra directory roles (identity RBAC).

```powershell
Connect-MgGraph -Scopes "RoleManagement.Read.Directory" -NoWelcome
Get-MgDirectoryRole | Select-Object DisplayName | Select-Object -First 8
```

**Expected result:** activated directory roles (Global Administrator, …) —
Entra's access-management capabilities.

**Negative test:** assume every role is always active; some are eligible via PIM
until activated.

**Cleanup:** none.

### Lab 3.3 — SC-900: Describe the capabilities of Microsoft security solutions (35–40%)

**Objective:** Read the Defender security posture.

```powershell
Connect-MgGraph -Scopes "SecurityEvents.Read.All" -NoWelcome
Get-MgSecuritySecureScore -Top 1 | Select-Object CurrentScore, MaxScore
```

**Expected result:** current vs max Secure Score — the Microsoft Defender
security-solution posture.

**Negative test:** equate Secure Score with Sentinel coverage; they are
different tools (posture vs SIEM).

**Cleanup:** none.

### Lab 3.4 — SC-900: Describe the capabilities of Microsoft compliance solutions (20–25%)

**Objective:** List Purview retention (compliance) policies.

```powershell
Connect-IPPSSession
Get-RetentionCompliancePolicy | Select-Object Name, Workload
```

**Expected result:** retention policies by workload — Purview compliance
capabilities.

**Negative test:** assume Purview auto-classifies with no labels; you configure
sensitivity/retention labels first.

**Cleanup:** none.

### Lab 3.5 — SC-300: Implement and manage user identities (20–25%)

**Objective:** Provision a user identity.

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All" -NoWelcome
$d=(Get-MgOrganization).VerifiedDomains[0].Name
New-MgUser -DisplayName "SC Lab" -AccountEnabled -MailNickname sclab -UserPrincipalName "sclab@$d" -PasswordProfile @{Password='TempP@ss2026!';ForceChangePasswordNextSignIn=$true}
```

**Expected result:** a provisioned user — the identity lifecycle SC-300 manages.

**Negative test:** reuse an existing UPN; Entra rejects duplicate
userPrincipalNames.

**Cleanup:** `Remove-MgUser -UserId "sclab@$d"`.

### Lab 3.6 — SC-300: Implement authentication and access management (20–25%)

**Objective:** List Conditional Access policies.

```powershell
Connect-MgGraph -Scopes "Policy.Read.All" -NoWelcome
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State
```

**Expected result:** CA policies with state (enabled/report-only) —
authentication and access management.

**Negative test:** enforce a block-all CA policy with no emergency-access
account; you can lock everyone out.

**Cleanup:** none.

### Lab 3.7 — SC-300: Plan and implement workload identities (20–25%)

**Objective:** Enumerate service principals (workload identities).

```powershell
Connect-MgGraph -Scopes "Application.Read.All" -NoWelcome
Get-MgServicePrincipal -Top 5 | Select-Object DisplayName, AppId
```

**Expected result:** service principals — the non-human identities SC-300
governs.

**Negative test:** leave a workload identity with a never-expiring secret;
rotate credentials and prefer managed identities.

**Cleanup:** none.

### Lab 3.8 — SC-300: Plan and automate identity governance (20–25%)

**Objective:** Read entitlement-management access packages.

```powershell
Connect-MgGraph -Scopes "EntitlementManagement.Read.All" -NoWelcome
Get-MgEntitlementManagementAccessPackage -Top 5 | Select-Object DisplayName
```

**Expected result:** access packages — the entitlement-management governance
SC-300 automates.

**Negative test:** grant standing access instead of time-bound; governance
favors access reviews and expiry.

**Cleanup:** none.

### Lab 3.9 — SC-200: Manage a security operations environment (40–45%)

**Objective:** Read the Defender XDR alert surface.

```powershell
Connect-MgGraph -Scopes "SecurityAlert.Read.All" -NoWelcome
Get-MgSecurityAlertV2 -Top 5 | Select-Object Title, Severity, Status
```

**Expected result:** security alerts with severity/status — the SecOps
environment SC-200 operates.

**Negative test:** suppress all informational alerts; some feed correlation into
incidents.

**Cleanup:** none.

### Lab 3.10 — SC-200: Respond to security incidents (35–40%)

**Objective:** Move an incident into investigation.

```powershell
Connect-MgGraph -Scopes "SecurityIncident.ReadWrite.All" -NoWelcome
$i = Get-MgSecurityIncident -Top 1
Update-MgSecurityIncident -IncidentId $i.Id -Status "inProgress"
```

**Expected result:** an incident set to `inProgress` — the response workflow.

**Negative test:** close an incident with no classification; SC-200 requires
triage/classification for metrics.

**Cleanup:** set the incident status back as appropriate.

### Lab 3.11 — SC-200: Perform threat hunting (20–25%)

**Objective:** Run a KQL hunting query (Defender/Sentinel).

```kusto
DeviceProcessEvents
| where FileName in~ ("powershell.exe","cmd.exe")
| where ProcessCommandLine has_any ("-enc","IEX","DownloadString")
| take 20
```

**Expected result:** suspicious encoded/download process events — proactive
threat hunting with KQL.

**Negative test:** hunt with no time window; unbounded queries are slow and
noisy — scope by timestamp.

**Cleanup:** none.

### Lab 3.12 — SC-401: Implement information protection (30–35%)

**Objective:** List sensitivity labels.

```powershell
Connect-IPPSSession
Get-Label | Select-Object DisplayName, ContentType
```

**Expected result:** sensitivity labels (Confidential, …) — information-protection
classification.

**Negative test:** create a label but never publish a label policy; unpublished
labels never reach users.

**Cleanup:** none.

### Lab 3.13 — SC-401: Implement data loss prevention and retention (30–35%)

**Objective:** List DLP policies.

```powershell
Get-DlpCompliancePolicy | Select-Object Name, Mode, Workload
```

**Expected result:** DLP policies with mode/workload — data loss prevention
controls.

**Negative test:** deploy a DLP policy in enforce mode with no simulation;
start in test mode to avoid false blocks.

**Cleanup:** none.

### Lab 3.14 — SC-401: Manage risks, alerts, and activities (30–35%)

**Objective:** Read protection/compliance alerts.

```powershell
Get-ProtectionAlert | Select-Object Name, Severity, Category | Select-Object -First 5
```

**Expected result:** protection alerts by category/severity — the risk and alert
surface SC-401 manages.

**Negative test:** ignore low-severity DLP alerts wholesale; patterns of low
alerts can indicate exfiltration.

**Cleanup:** none.

### Lab 3.15 — SC-100: Design solutions that align with security best practices and priorities (20–25%)

**Objective:** Baseline posture to inform a Zero Trust design.

```powershell
Connect-MgGraph -Scopes "SecurityEvents.Read.All" -NoWelcome
(Get-MgSecuritySecureScore -Top 1).CurrentScore
```

**Expected result:** the current Secure Score — the baseline an SC-100 architect
designs improvements against (Zero Trust/MCRA).

**Negative test:** design controls without measuring the baseline; you cannot
prioritize unmeasured gaps.

**Cleanup:** none.

### Lab 3.16 — SC-100: Design security operations, identity, and compliance capabilities (25–30%)

**Objective:** Inventory the identity capability to design a target state.

```powershell
Get-MgIdentityConditionalAccessPolicy | Measure-Object | Select-Object Count
```

**Expected result:** the count of existing CA policies — the identity capability
an architect extends toward least privilege.

**Negative test:** design SecOps with no log-retention plan; detection needs
sufficient retention.

**Cleanup:** none.

### Lab 3.17 — SC-100: Design security solutions for infrastructure (25–30%)

**Objective:** Read Defender for Cloud coverage (infrastructure design input).

```bash
az security pricing list --query "value[].{plan:name,tier:pricingTier}" -o table
```

**Expected result:** Defender for Cloud plans and tiers per resource type — the
infrastructure protection an architect designs.

**Negative test:** assume free-tier Defender protects servers; server protection
needs the paid plan.

**Cleanup:** none.

### Lab 3.18 — SC-100: Design security solutions for applications and data (20–25%)

**Objective:** Inventory data-classification labels to design app/data security.

```powershell
Connect-IPPSSession
Get-Label | Measure-Object | Select-Object Count
```

**Expected result:** the count of sensitivity labels — the classification
foundation an architect builds app/data protection on.

**Negative test:** design DLP without classification; DLP is far weaker on
unlabeled data.

**Cleanup:** none.

### Lab 3.19 — SC-500: Manage identity, access, and governance (20–25%)

**Objective:** List Azure RBAC role assignments (cloud access governance).

```bash
az role assignment list --all --query "[].{principal:principalName,role:roleDefinitionName}" -o table | head
```

**Expected result:** Azure role assignments — the cloud access governance SC-500
manages.

**Negative test:** grant Owner broadly for convenience; least privilege
(Contributor/custom roles) is required.

**Cleanup:** none.

### Lab 3.20 — SC-500: Secure storage, databases, and networking (25–30%)

**Objective:** Check storage secure-transfer and public-access posture.

```bash
az storage account list --query "[].{name:name,https:enableHttpsTrafficOnly,public:allowBlobPublicAccess}" -o table
```

**Expected result:** per-account HTTPS-only and public-access flags — storage
security posture.

**Negative test:** leave `allowBlobPublicAccess=true` on sensitive data; disable
public blob access.

**Cleanup:** none.

### Lab 3.21 — SC-500: Secure compute (20–25%)

**Objective:** Read Defender for Cloud recommendations for compute.

```bash
az security assessment list --query "[?contains(displayName,'machine')].displayName" -o tsv | head
```

**Expected result:** compute-related security recommendations — securing
VMs/containers.

**Negative test:** expose SSH/RDP to the internet on a VM; use just-in-time
access and a bastion instead.

**Cleanup:** none.

### Lab 3.22 — SC-500: Manage and monitor security posture (20–25%)

**Objective:** Read the Defender for Cloud secure score.

```bash
az security secure-scores list --query "value[].{name:displayName,score:score.percentage}" -o table
```

**Expected result:** the cloud secure-score percentage — the posture SC-500
monitors and improves.

**Negative test:** chase 100% by exempting findings; exemptions hide risk rather
than remediate it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SC family runs SC-900 (Fundamentals), SC-300 (Identity and Access),
SC-200 (Security Operations), SC-401 (Information Security, replacing SC-400),
SC-100 (Cybersecurity Architect Expert), and the new SC-500 (Cloud and AI
Security Engineer). The credentials map to Conditional Access, Purview, and
Defender practice in Volume XXXVII and the security foundations in Volume X.

- [ ] I can list the SC credentials and exam codes.
- [ ] I know SC-401 replaced SC-400 and SC-500 is new.
- [ ] I can map each to hands-on practice.
- [ ] I can sequence a security study path to Expert.
- [ ] I completed Labs 3.1–3.2 including each negative test.
