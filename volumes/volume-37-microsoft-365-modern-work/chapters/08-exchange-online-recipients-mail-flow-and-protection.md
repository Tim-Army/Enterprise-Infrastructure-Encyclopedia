# Chapter 08: Exchange Online — Recipients, Mail Flow, and Protection

## Learning Objectives

- Manage Exchange Online recipients: mailboxes, shared mailboxes, groups, and contacts.
- Control mail flow with connectors, transport rules, and accepted domains.
- Configure email authentication — SPF, DKIM, and DMARC — to stop spoofing.
- Apply Exchange Online Protection anti-spam, anti-malware, and anti-phishing policies.
- Validate mail flow and troubleshoot delivery with message trace.

## Theory and Architecture

**Exchange Online** is the hosted email service in Microsoft 365. Its objects
are **recipients**: **user mailboxes** (a licensed person's mailbox),
**shared mailboxes** (no license needed under the size limit, accessed by
delegated users), **room and equipment mailboxes** (resources booked in
calendars), **mail-enabled security groups** and **distribution groups**,
**Microsoft 365 groups** (with a group mailbox), and **mail contacts/users**
(external addresses in the address book). Mailboxes have **permissions** —
Full Access, Send As, Send on Behalf — and archives and retention
(Chapter 10).

**Mail flow** is how messages move. **Accepted domains** tell Exchange which
domains it is authoritative for. **Connectors** define secured mail paths to
or from partner organizations or on-premises systems. **Transport (mail flow)
rules** inspect and act on messages in transit — add disclaimers, block or
redirect, encrypt, or apply headers based on conditions. Mail routes through
**Exchange Online Protection (EOP)** on the way in and out.

**Email authentication** stops spoofing of your domain. **SPF** (a DNS TXT
record) lists the servers allowed to send for your domain. **DKIM** signs
outbound mail with a key published in DNS so recipients can verify it was not
altered. **DMARC** (a DNS record) tells receivers what to do when SPF/DKIM
fail (none/quarantine/reject) and where to send reports — the policy that
makes SPF and DKIM enforceable.

**Exchange Online Protection** is the built-in security stack every mailbox
gets: **anti-malware**, **anti-spam** (connection and content filtering),
**anti-phishing** (spoof intelligence, and with Defender for Office 365,
impersonation protection), and **outbound spam** controls. **Defender for
Office 365** (Chapter 11) adds Safe Links, Safe Attachments, and richer
anti-phishing.

## Design Considerations

Use **shared mailboxes** for team addresses (support@, sales@) rather than
licensed accounts, and grant access by **group** for manageable delegation.
Use **room/equipment** mailboxes with booking policies for resources. Keep
**distribution** vs **Microsoft 365 groups** deliberate — Microsoft 365 groups
add collaboration (site/team) but are heavier.

Lock down **mail flow**: define **accepted domains** correctly, use
**connectors** only for genuine partner or hybrid paths (and secure them with
TLS and certificate/IP restrictions), and keep **transport rules** few and
well-documented — they are powerful and easy to misconfigure into a mail loop
or open relay. Publish **SPF, DKIM, and DMARC** for every sending domain and
move DMARC from `p=none` (monitor) to `p=quarantine`/`p=reject` once reports
show legitimate senders are aligned — this is the single biggest anti-spoofing
win.

Tune **EOP** policies (or use the **preset security policies** Standard/Strict
for a strong default), set **quarantine** policies so users can review or
release safely, and configure **anti-phishing** impersonation protection for
your executives and domains.

## Implementation and Automation

Exchange Online is managed with the **Exchange Online PowerShell V3** module:

```powershell
Install-Module ExchangeOnlineManagement -Scope AllUsers
Connect-ExchangeOnline -UserPrincipalName admin@contoso.com
# Shared mailbox + delegated access
New-Mailbox -Shared -Name "Support" -PrimarySmtpAddress "support@contoso.com"
Add-MailboxPermission -Identity "support@contoso.com" -User "GG-Helpdesk" -AccessRights FullAccess -InheritanceType All
Add-RecipientPermission -Identity "support@contoso.com" -Trustee "GG-Helpdesk" -AccessRights SendAs -Confirm:$false
```

Enable DKIM and create a transport rule:

```powershell
New-DkimSigningConfig -DomainName "contoso.com" -Enabled $true
Get-DkimSigningConfig -Identity "contoso.com" | Select-Object Domain, Enabled, Status
New-TransportRule -Name "External disclaimer" -FromScope InOrganization -SentToScope NotInOrganization `
  -ApplyHtmlDisclaimerText "<i>Sent from Contoso</i>" -ApplyHtmlDisclaimerLocation Append
```

Apply an anti-phishing policy (or the Strict preset):

```powershell
New-AntiPhishPolicy -Name "AP-Exec" -EnableTargetedUserProtection $true `
  -TargetedUsersToProtect "CEO;ceo@contoso.com" -EnableMailboxIntelligence $true `
  -EnableMailboxIntelligenceProtection $true
```

## Validation and Troubleshooting

Trace delivery and verify authentication:

```powershell
Get-MessageTrace -SenderAddress "user@contoso.com" -StartDate (Get-Date).AddHours(-2) -EndDate (Get-Date) |
  Select-Object Received, SenderAddress, RecipientAddress, Status, Subject
Get-DkimSigningConfig | Select-Object Domain, Enabled, Status
Resolve-DnsName -Type TXT -Name "contoso.com" | Where-Object Strings -like "*spf*"
Resolve-DnsName -Type TXT -Name "_dmarc.contoso.com"
```

`Get-MessageTrace` shows each message's status (`Delivered`, `FailedToDeliver`,
`Quarantined`, `FilteredAsSpam`). Common issues: mail from your domain marked
as spoof because **SPF/DKIM/DMARC** are missing or misaligned (a top cause of
deliverability problems); a **transport rule** silently redirecting or dropping
mail (audit rules when messages vanish); a **connector** misconfiguration
causing rejection or, worse, an **open relay**; a shared mailbox a user cannot
open because **Full Access** was granted but Outlook has not refreshed
automapping; and legitimate mail in **quarantine** because a policy is too
aggressive — tune the policy and let users review. Message trace plus the
message header analyzer resolve most delivery mysteries.

## Security and Best Practices

Publish and enforce **SPF, DKIM, and DMARC** on every sending domain, moving
DMARC to **reject** once aligned — this stops others spoofing you. Apply the
**Standard or Strict preset security policies** for a strong EOP/Defender
baseline, with **impersonation protection** for executives and domains and
sensible **quarantine** policies. Prefer **shared mailboxes** (unlicensed,
group-delegated) over shared user accounts. Keep **transport rules** and
**connectors** minimal, documented, and TLS-secured; audit them regularly for
loops or relay risk. Enable **outbound spam** limits so a compromised account
cannot mass-mail. Use **modern authentication** only — legacy protocols to
Exchange are blocked by Conditional Access (Chapter 03).

## References and Knowledge Checks

- Microsoft Learn: *Exchange Online recipients*; *Mail flow rules and connectors*; *SPF/DKIM/DMARC*; *Exchange Online Protection*; *Preset security policies*.
- Microsoft Learn: MS-102 — *Manage Exchange Online* (as part of managing Microsoft 365).

**Knowledge checks**

1. When should a shared mailbox be used instead of a licensed user mailbox?
2. What do SPF, DKIM, and DMARC each do, and why is DMARC the enforcer?
3. What does message trace tell you that the sender's Sent Items cannot?

## Hands-On Lab

Topic-level walkthroughs for Exchange Online administration.

**Shared prerequisites for Labs 8.1–8.4** — a Microsoft 365 tenant, the
`ExchangeOnlineManagement` module, an Exchange admin account, and a verified
custom domain for the DKIM/DMARC labs. **Cost:** none.

### Lab 8.1 — Create a shared mailbox with delegated access (Topic: Recipients)

**Objective:** Provide a team address without a license.

```powershell
Connect-ExchangeOnline -UserPrincipalName admin@contoso.com
New-Mailbox -Shared -Name "Support" -PrimarySmtpAddress "support@contoso.com"
Add-MailboxPermission "support@contoso.com" -User "GG-Helpdesk" -AccessRights FullAccess -InheritanceType All
Get-MailboxPermission "support@contoso.com" | Where-Object User -like "*Helpdesk*"
```

**Expected result:** a shared mailbox exists with the help-desk group granted
Full Access — shared mailboxes need no license under the size limit.

**Negative test:** grant Send As without Full Access and expect the group to
open the mailbox; they can send as it but not read it — the two rights are
separate.

**Cleanup:** `Remove-Mailbox "support@contoso.com" -Confirm:$false`.

### Lab 8.2 — Enable DKIM signing (Topic: Email authentication)

**Objective:** Sign outbound mail for a domain.

```powershell
New-DkimSigningConfig -DomainName "contoso.com" -Enabled $true
Get-DkimSigningConfig -Identity "contoso.com" | Select-Object Domain, Enabled, Status
```

**Expected result:** DKIM signing is enabled once the two CNAME selector
records are published in DNS — DKIM lets receivers verify your mail is
unaltered.

**Negative test:** enable DKIM before publishing the selector CNAMEs; the
status shows the records are missing and signing does not fully activate —
DNS records are the prerequisite.

**Cleanup:** `Set-DkimSigningConfig -Identity "contoso.com" -Enabled $false`.

### Lab 8.3 — Create a mail flow rule (Topic: Mail flow)

**Objective:** Append a disclaimer to external mail.

```powershell
New-TransportRule -Name "External disclaimer" -FromScope InOrganization -SentToScope NotInOrganization `
  -ApplyHtmlDisclaimerText "<i>Sent from Contoso</i>" -ApplyHtmlDisclaimerLocation Append
Get-TransportRule "External disclaimer" | Select-Object Name, State, Priority
```

**Expected result:** external outbound mail gets the disclaimer — transport
rules act on messages in transit.

**Negative test:** create a rule that redirects all mail to an external
address; you have built an exfiltration/loop risk — review rule scope and
actions carefully.

**Cleanup:** `Remove-TransportRule "External disclaimer" -Confirm:$false`.

### Lab 8.4 — Trace a message (Topic: Troubleshoot delivery)

**Objective:** Follow a message's fate.

```powershell
Get-MessageTrace -StartDate (Get-Date).AddHours(-2) -EndDate (Get-Date) |
  Select-Object Received, SenderAddress, RecipientAddress, Status, Subject | Sort-Object Received -Descending
```

**Expected result:** recent messages list with a `Status` of `Delivered`,
`Quarantined`, or `FilteredAsSpam` — the authoritative delivery record, unlike
the sender's Sent Items.

**Negative test:** search a time window before the message was sent; it does
not appear — trace within the correct window (extended trace for older mail).

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Exchange Online manages recipients (user, shared, resource mailboxes and
groups), controls mail flow with accepted domains, connectors, and transport
rules, and protects mail with EOP anti-spam/malware/phishing plus SPF, DKIM,
and DMARC. Message trace is the tool for delivery troubleshooting.

- [ ] I can manage mailboxes and delegate access correctly.
- [ ] I can configure SPF, DKIM, and DMARC and explain each.
- [ ] I can build safe mail flow rules and connectors.
- [ ] I can apply EOP protection and trace delivery.
- [ ] I completed Labs 8.1–8.4 including each negative test.
