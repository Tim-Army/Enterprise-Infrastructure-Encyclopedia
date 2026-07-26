# Chapter 10: Microsoft Purview — Information Protection, DLP, Retention, and Compliance

## Learning Objectives

- Classify data with sensitive information types, trainable classifiers, and sensitivity labels.
- Protect labeled content with encryption, marking, and access controls.
- Prevent data loss with DLP policies across Microsoft 365, endpoints, and the cloud.
- Govern the data lifecycle with retention labels and policies.
- Use compliance solutions — eDiscovery, audit, and insider risk — and interpret Compliance Manager.

## Theory and Architecture

**Microsoft Purview** is the data governance, protection, and compliance suite
for Microsoft 365 (and beyond). It rests on **classification**: knowing what
data is sensitive. **Sensitive information types (SITs)** detect patterns
(credit-card numbers, national IDs) with regex, keywords, and confidence
levels; **exact data match (EDM)** matches against your own uploaded data
sets; and **trainable classifiers** use machine learning to recognize
categories (resumes, source code) that patterns cannot.

**Sensitivity labels** apply protection to content and containers. A label can
**encrypt** (with usage rights — who can open, and what they can do), apply
**visual marking** (headers/footers/watermarks), set **container** protection
(site/team privacy, external sharing, unmanaged-device access), and drive
**auto-labeling** (client-side by conditions, or service-side for data at
rest). Labels travel with the file, so protection persists outside Microsoft
365.

**Data Loss Prevention (DLP)** stops sensitive data leaving. A DLP policy
scopes **locations** (Exchange, SharePoint, OneDrive, Teams, **endpoints** via
Intune, and cloud apps via Defender for Cloud Apps), matches on SITs, labels,
or classifiers, and takes **actions** — block, block with override, notify the
user with a policy tip, or restrict — with incident reports for the admin.
**Endpoint DLP** extends this to actions on the device (copy to USB, print,
paste to browser, cloud upload).

**Data lifecycle / records management** controls how long data is kept and
when it is deleted. **Retention labels and policies** retain content for a
period, then delete it (or trigger disposition review), and **records
management** adds regulatory records with immutability and event-based
retention. **Compliance solutions** include **eDiscovery** (search, hold, and
export content for legal/investigation), the **unified audit log**, **insider
risk management** (behavioral signals for data theft/leak), and
**Communication Compliance**. **Compliance Manager** scores your posture
against regulations and recommends improvement actions.

## Design Considerations

Start with a **label taxonomy** users can understand — a small set
(Public, General, Confidential, Highly Confidential) with sub-labels for
scope — and publish it with a **label policy** to the right users, setting a
**default** and **mandatory labeling** where appropriate. Use **auto-labeling**
(service-side for data at rest, client-side for prompts) to catch what users
miss. Configure **encryption and rights** on the labels that need it, and use
**container labels** to enforce site/team privacy and external-sharing
posture (linking to Chapter 09).

Design **DLP** in **stages**: start in **test/audit with policy tips** to
learn and reduce false positives, then move to **block with override**, then
**block** for the most sensitive. Scope the right **locations** including
**endpoints**, and match on **labels** where possible (more reliable than raw
SITs). Plan **retention** to satisfy legal/regulatory requirements without
hoarding — retain what you must, delete what you should, and reserve
**records management** for true regulatory records. Enable the **unified audit
log**, scope **eDiscovery** and **insider risk** with privacy and least
privilege, and use **Compliance Manager** to prioritize.

## Implementation and Automation

Purview uses the **Security & Compliance PowerShell** endpoint:

```powershell
Connect-IPPSSession -UserPrincipalName admin@contoso.com
# Sensitivity label with encryption + marking
New-Label -Name "Confidential" -DisplayName "Confidential" -Tooltip "Company confidential" `
  -EncryptionEnabled $true -EncryptionRightsDefinitions "GG-Employees:VIEW,EDIT,PRINT" `
  -ApplyContentMarkingFooterEnabled $true -ApplyContentMarkingFooterText "Confidential"
New-LabelPolicy -Name "Default labeling" -Labels "Confidential" -ExchangeLocation "All"
```

Create a DLP policy for credit-card data across the main locations:

```powershell
New-DlpCompliancePolicy -Name "PCI - Block CC" -ExchangeLocation "All" `
  -SharePointLocation "All" -OneDriveLocation "All" -EndpointDlpLocation "All" -Mode Enable
New-DlpComplianceRule -Name "CC block" -Policy "PCI - Block CC" `
  -ContentContainsSensitiveInformation @{ Name="Credit Card Number"; minCount="1" } `
  -BlockAccess $true -NotifyUser "Owner","LastModifier"
```

Create a retention policy and label:

```powershell
New-RetentionCompliancePolicy -Name "Keep 7 years" -ExchangeLocation "All" -SharePointLocation "All"
New-RetentionComplianceRule -Name "7yr rule" -Policy "Keep 7 years" -RetentionDuration 2555 -RetentionComplianceAction Keep
```

## Validation and Troubleshooting

Confirm labels, DLP, and retention, and read incidents:

```powershell
Get-Label | Select-Object DisplayName, EncryptionEnabled
Get-DlpCompliancePolicy | Select-Object Name, Mode, Workload
Get-RetentionCompliancePolicy | Select-Object Name, Enabled
# DLP incidents/alerts surface in the Purview portal (Data loss prevention > Alerts)
```

Common issues: a **sensitivity label** not appearing for users because the
**label policy** does not target them or the client is stale; **auto-labeling**
not matching because the SIT confidence/count threshold is too high or the
data is not where the policy scopes; **DLP false positives** flooding users
because the policy started in Enable/Block instead of **test with tips** —
stage it; **Endpoint DLP** not acting because devices are not **onboarded**
(Intune/Defender) or the location is not enabled; and **retention conflicts**
where multiple policies apply — the **principles of retention** resolve them
(retention wins over deletion, longest wins, explicit over implicit, shortest
deletion wins). eDiscovery holds preserve content even if a user deletes it —
verify the hold before assuming loss.

## Security and Best Practices

Classify first — **SITs, EDM, and trainable classifiers** feed everything
else. Publish a **simple label taxonomy**, set **defaults/mandatory** where
needed, and use **auto-labeling** to reduce reliance on users. Protect
sensitive labels with **encryption and rights** so protection persists off-
platform, and use **container labels** to enforce site/team privacy and
sharing. Roll out **DLP in stages** (audit → override → block), scope
**endpoints** and match on **labels**, and review **incidents**. Retain and
delete per legal requirements with **retention** and **records management** —
do not hoard. Enable the **unified audit log**, scope **eDiscovery/insider
risk** with least privilege and privacy controls, and drive improvement with
**Compliance Manager**. Protection, prevention, and governance work together.

## References and Knowledge Checks

- Microsoft Learn: *Sensitivity labels*; *Data loss prevention*; *Endpoint DLP*; *Retention and records management*; *eDiscovery*; *Compliance Manager*.
- Microsoft Learn: SC-401 — *Information security administrator*; MS-102 — *Manage compliance*.

**Knowledge checks**

1. What can a sensitivity label do beyond visual marking, and why does protection persist off-platform?
2. Why stage DLP through audit and override before blocking?
3. How do the principles of retention resolve conflicting retention/deletion policies?

## Hands-On Lab

Topic-level walkthroughs for SC-401 information-protection skills.

**Shared prerequisites for Labs 10.1–10.4** — a Microsoft 365 tenant with
Purview (E5/compliance add-on for advanced features), a
`Connect-IPPSSession` connection, compliance admin rights, and (for endpoint
DLP) onboarded devices. **Cost:** none (trial compliance licensing).

### Lab 10.1 — Create a sensitivity label with encryption (Topic: Information protection)

**Objective:** Protect content with rights and marking.

```powershell
Connect-IPPSSession -UserPrincipalName admin@contoso.com
New-Label -Name "Confidential" -DisplayName "Confidential" -Tooltip "Company confidential" `
  -EncryptionEnabled $true -EncryptionRightsDefinitions "GG-Employees:VIEW,EDIT,PRINT" `
  -ApplyContentMarkingFooterEnabled $true -ApplyContentMarkingFooterText "Confidential"
New-LabelPolicy -Name "Default labeling" -Labels "Confidential" -ExchangeLocation "All"
Get-Label | Select-Object DisplayName, EncryptionEnabled
```

**Expected result:** a Confidential label that encrypts with employee-only
rights and marks documents — protection travels with the file.

**Negative test:** apply the label without publishing a **label policy**; users
never see it — the policy scopes the label to people.

**Cleanup:** remove the label policy and label.

### Lab 10.2 — Create a staged DLP policy (Topic: Data loss prevention)

**Objective:** Detect credit-card data safely.

```powershell
New-DlpCompliancePolicy -Name "PCI - detect" -ExchangeLocation "All" -SharePointLocation "All" -OneDriveLocation "All" -Mode TestWithNotifications
New-DlpComplianceRule -Name "CC detect" -Policy "PCI - detect" `
  -ContentContainsSensitiveInformation @{ Name="Credit Card Number"; minCount="1" } -NotifyUser "Owner"
Get-DlpCompliancePolicy | Select-Object Name, Mode
```

**Expected result:** a policy in **TestWithNotifications** shows policy tips
and generates incidents without blocking — the safe first stage.

**Negative test:** create the policy in `Enable` with `-BlockAccess $true`
immediately; users are blocked and false positives spike — stage through test
first.

**Cleanup:** remove the DLP policy.

### Lab 10.3 — Create a retention policy (Topic: Data lifecycle)

**Objective:** Retain content for a required period.

```powershell
New-RetentionCompliancePolicy -Name "Keep 7 years" -ExchangeLocation "All" -SharePointLocation "All"
New-RetentionComplianceRule -Name "7yr" -Policy "Keep 7 years" -RetentionDuration 2555 -RetentionComplianceAction Keep
Get-RetentionCompliancePolicy | Select-Object Name, Enabled
```

**Expected result:** content is retained for seven years — retention protects
against premature deletion.

**Negative test:** apply two policies, one keeping and one deleting the same
content; the **principles of retention** resolve the conflict (retention wins
over deletion) — understand precedence before layering policies.

**Cleanup:** remove the retention policy.

### Lab 10.4 — Confirm the unified audit log is on (Topic: Compliance solutions)

**Objective:** Ensure activity is recorded for eDiscovery/investigation.

```powershell
Connect-ExchangeOnline -UserPrincipalName admin@contoso.com
Get-AdminAuditLogConfig | Select-Object UnifiedAuditLogIngestionEnabled
Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-1) -EndDate (Get-Date) -RecordType AzureActiveDirectory -ResultSize 5 |
  Select-Object CreationDate, Operations, UserIds
```

**Expected result:** unified audit logging is enabled and recent activity is
searchable — the basis for eDiscovery and investigations.

**Negative test:** search the audit log with it disabled; no results — enable
`UnifiedAuditLogIngestionEnabled` first.

**Cleanup:** none (leave auditing enabled — a best practice).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Purview classifies data (SITs, EDM, trainable classifiers), protects it with
sensitivity labels (encryption, marking, containers), prevents loss with DLP
across Microsoft 365 and endpoints, governs the lifecycle with retention and
records, and provides compliance solutions (eDiscovery, audit, insider risk)
scored by Compliance Manager. Stage DLP and understand retention precedence.

- [ ] I can classify data and publish a sensitivity-label taxonomy.
- [ ] I can protect content with encryption and container labels.
- [ ] I can stage DLP through audit, override, and block.
- [ ] I can govern retention and use compliance solutions.
- [ ] I completed Labs 10.1–10.4 including each negative test.
