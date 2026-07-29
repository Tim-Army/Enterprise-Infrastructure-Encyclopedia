# Chapter 10: Security and Identity Hardening — AD CS, gMSA, LAPS, Credential Guard, and Defender

## Learning Objectives

- Deploy Active Directory Certificate Services and issue certificates from templates.
- Replace service-account passwords with group managed service accounts (gMSA).
- Rotate and secure local administrator passwords with Windows LAPS.
- Protect credentials with Credential Guard, Protected Users, and administrative tiering.
- Harden Windows Server with Microsoft Defender, attack-surface reduction, and baselines.

## Theory and Architecture

Identity is the modern attack surface, and Windows Server provides the
building blocks to defend it. **Active Directory Certificate Services (AD
CS)** is a public-key infrastructure: an enterprise **Certification
Authority (CA)** issues certificates from **templates** to users, computers,
and services for authentication, encryption, and signing. Enterprise CAs are
integrated with AD so **auto-enrollment** can silently issue and renew (for
example, computer certificates for 802.1X or LDAPS). AD CS is powerful and
dangerous — misconfigured templates are a well-known privilege-escalation
path (the "ESC" issues), so template permissions and enrollment rights must
be tight.

**Service accounts** are a perennial weakness: shared passwords that never
change and end up in scripts. **Group managed service accounts (gMSA)** solve
this — AD generates and rotates a long, random password automatically (every
30 days by default), and authorized hosts retrieve it via the **KDS root
key**; the password is never known to a human. **Windows LAPS** solves the
same problem for **local administrator** accounts: it randomizes each
machine's local admin password on a schedule and stores it (encrypted) in AD
or Microsoft Entra ID, killing the "same local admin password everywhere"
lateral-movement path.

**Credential theft** defenses limit what an attacker gains from a foothold.
**Credential Guard** uses virtualization-based security to isolate secrets
(NTLM hashes, Kerberos tickets) from the OS so tools like Mimikatz cannot
scrape them. The **Protected Users** group hardens its members (no NTLM, no
unconstrained delegation, no long-lived Kerberos tickets). **Administrative
tiering** (Tier 0 = identity/DCs, Tier 1 = servers, Tier 2 = workstations)
plus **privileged access workstations (PAWs)** prevent a Tier-0 credential
from ever being exposed on a lower-tier, more-exposed machine.

**Microsoft Defender Antivirus** and the broader Defender stack provide
real-time protection, **attack-surface-reduction (ASR)** rules,
**controlled folder access**, and (with Defender for Endpoint) EDR. Combined
with **security baselines** from the Security Compliance Toolkit, they
harden the OS itself.

## Design Considerations

Deploy AD CS deliberately: a **two-tier PKI** (offline root, online issuing)
for production, tight **template** permissions (no "Supply in the request"
for authentication EKUs unless controlled, restricted enrollment groups),
and monitoring for the known ESC misconfigurations. Use **gMSA** for every
service that supports it, and **LAPS** on every workstation and member
server; store LAPS secrets in **Entra ID** for cloud-joined devices and AD
for domain-joined, and restrict who can read them.

Adopt **administrative tiering** as the organizing principle: Tier-0 admins
log on only to Tier-0 systems from PAWs, never to a workstation; put
sensitive accounts in **Protected Users**; and enable **Credential Guard**
on all supported machines. Deploy **Defender** with **ASR rules** in audit
first, then enforce, and apply the **Microsoft security baselines** via
Group Policy (Chapter 05) with Enforced links. Every one of these is
defense-in-depth; none alone is sufficient.

## Implementation and Automation

Create the KDS root key and a gMSA:

```powershell
Add-KdsRootKey -EffectiveImmediately          # in a lab, backdate to use immediately
New-ADServiceAccount -Name "gmsa-web" -DNSHostName "gmsa-web.corp.contoso.lab" `
  -PrincipalsAllowedToRetrieveManagedPassword "GG-Web-Servers"
# On the member server:
Install-ADServiceAccount -Identity "gmsa-web"
Test-ADServiceAccount -Identity "gmsa-web"      # True when the host can use it
```

Enable Windows LAPS to store the local admin password in AD:

```powershell
Update-LapsADSchema
Set-LapsADComputerSelfPermission -Identity "OU=Servers,DC=corp,DC=contoso,DC=lab"
# via GPO or directly:
Set-LapsADPasswordExpirationTime -Identity "FS01"
Get-LapsADPassword -Identity "FS01" -AsPlainText   # authorized readers only
```

Harden with Credential Guard and a Defender ASR rule:

```powershell
# Credential Guard via registry/GPO (VBS + Secure Boot required):
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard' -Name 'EnableVirtualizationBasedSecurity' -Value 1
# ASR: block credential stealing from LSASS
Add-MpPreference -AttackSurfaceReductionRules_Ids 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2 `
  -AttackSurfaceReductionRules_Actions Enabled
```

## Validation and Troubleshooting

Verify accounts, secrets, and protections:

```powershell
Test-ADServiceAccount -Identity "gmsa-web"          # True = usable
Get-MpComputerStatus | Select-Object AMRunningMode, RealTimeProtectionEnabled
Get-MpPreference | Select-Object -Expand AttackSurfaceReductionRules_Ids
# Credential Guard running?
(Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard).SecurityServicesRunning
```

`Test-ADServiceAccount` returning `True` confirms the host can retrieve the
gMSA password; `False` usually means the host is not in the
`PrincipalsAllowedToRetrieveManagedPassword` group or the KDS key is not yet
effective. Common issues: **AD CS** auto-enrollment not firing (check the
template's Read/Enroll/Autoenroll permissions and the GPO); **LAPS** not
populating because the schema was not extended or the computer lacks
self-permission; **Credential Guard** not running because VBS/Secure Boot or
firmware settings are missing; and **ASR rules** breaking a legitimate app —
always deploy in **audit** mode first (`Warn`/`AuditMode`) and review events
before enforcing.

## Security and Best Practices

Treat **domain controllers and AD CS CAs as Tier 0** and never expose their
credentials on lower tiers. Enforce **LAPS** everywhere and **gMSA** for
services so no static secret persists. Put privileged accounts in
**Protected Users**, enable **Credential Guard**, and require **PAWs** for
Tier-0 work. Audit **AD CS templates** against the ESC issues and monitor
certificate issuance. Deploy **Defender** with ASR and controlled folder
access, keep definitions current, and apply **security baselines** via
Enforced GPOs. Enable **LDAP signing and channel binding**, disable **NTLM**
where possible, and turn on **advanced audit policy** so credential-theft and
privileged-logon events are captured for the SIEM (Volume XI). Assume breach:
segment, least-privilege, and log.

## References and Knowledge Checks

- Microsoft Learn: *Active Directory Certificate Services*; *Group managed service accounts*; *Windows LAPS*; *Credential Guard*; *Protected Users*; *Microsoft Defender Antivirus*.
- Microsoft Learn: AZ-801 — *Secure Windows Server on-premises and hybrid infrastructures*.

**Knowledge checks**

1. What lateral-movement path does Windows LAPS eliminate?
2. Why is a gMSA safer than a traditional service account?
3. What must be true (firmware/OS) for Credential Guard to run, and what does it protect?

## Hands-On Lab

Topic-level walkthroughs for AZ-801's security-hardening skills.

**Shared prerequisites for Labs 10.1–10.4** — the `corp.contoso.lab` domain,
a member server, Secure Boot/VBS-capable hardware for the Credential Guard
lab, and Administrator rights. **Cost:** none.

### Lab 10.1 — Create and use a gMSA (Topic: Managed service accounts)

**Objective:** Replace a service password with an auto-rotating account.

```powershell
Add-KdsRootKey -EffectiveTime ((Get-Date).AddHours(-10))   # lab: usable immediately
New-ADServiceAccount -Name "gmsa-web" -DNSHostName "gmsa-web.corp.contoso.lab" `
  -PrincipalsAllowedToRetrieveManagedPassword "GG-Web-Servers"
# on the web server (member of GG-Web-Servers):
Install-ADServiceAccount "gmsa-web"
Test-ADServiceAccount "gmsa-web"
```

**Expected result:** `Test-ADServiceAccount` returns `True` — the host can
retrieve the rotating password with no human ever knowing it.

**Negative test:** run `Test-ADServiceAccount` on a host **not** in
`GG-Web-Servers`; it returns `False` — only authorized principals can use the
gMSA.

**Cleanup:** `Remove-ADServiceAccount "gmsa-web" -Confirm:$false`.

### Lab 10.2 — Enable Windows LAPS on an OU (Topic: Local admin password rotation)

**Objective:** Randomize and store the local admin password in AD.

```powershell
Update-LapsADSchema
Set-LapsADComputerSelfPermission -Identity "OU=Servers,DC=corp,DC=contoso,DC=lab"
Set-LapsADPasswordExpirationTime -Identity "FS01"
Get-LapsADPassword -Identity "FS01" -AsPlainText
```

**Expected result:** LAPS stores an encrypted, randomized local admin
password in AD that an authorized reader can retrieve — every machine's local
admin password is now unique.

**Negative test:** try `Get-LapsADPassword` as a non-authorized user; access
is denied — LAPS read rights are tightly scoped.

**Cleanup:** none (leave LAPS enabled; it is a best practice).

### Lab 10.3 — Enable a Defender ASR rule in audit then enforce (Topic: Attack-surface reduction)

**Objective:** Reduce attack surface safely.

```powershell
# Audit first:
Add-MpPreference -AttackSurfaceReductionRules_Ids 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2 `
  -AttackSurfaceReductionRules_Actions AuditMode
Get-MpPreference | Select-Object -Expand AttackSurfaceReductionRules_Actions
# then enforce after reviewing events:
Set-MpPreference -AttackSurfaceReductionRules_Ids 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2 `
  -AttackSurfaceReductionRules_Actions Enabled
```

**Expected result:** the "block credential stealing from LSASS" rule is first
in audit (logging only) then enforced — audit-first prevents breaking a
legitimate application.

**Negative test:** enable a strict ASR rule directly in `Enabled` mode
without auditing; a legitimate line-of-business app may be blocked — always
audit first.

**Cleanup:** set the rule back to `Disabled` if it was lab-only.

### Lab 10.4 — Confirm Credential Guard and Defender status (Topic: Credential protection)

**Objective:** Verify the credential-theft defenses are running.

```powershell
(Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard -ClassName Win32_DeviceGuard).SecurityServicesRunning
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, AMRunningMode
Get-ADGroupMember "Protected Users"
```

**Expected result:** `SecurityServicesRunning` includes the Credential Guard
service (value `1`), Defender real-time protection is on, and privileged
accounts appear in `Protected Users` — layered credential defenses in place.

**Negative test:** query Credential Guard on hardware without VBS/Secure
Boot; it reports not running — the platform prerequisites are mandatory.

**Cleanup:** none (leave protections enabled).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Windows Server hardens identity with AD CS (PKI, tightly governed
templates), gMSA and Windows LAPS (no static secrets for services or local
admins), Credential Guard, Protected Users, and administrative tiering
(credential-theft defense), and Microsoft Defender with ASR and security
baselines (OS hardening). These are layered, assume-breach defenses applied
together.

- [ ] I can issue certificates from AD CS and reason about template risk.
- [ ] I can deploy gMSA and Windows LAPS to eliminate static secrets.
- [ ] I can enable Credential Guard, Protected Users, and tiering.
- [ ] I can harden with Defender ASR using audit-then-enforce.
- [ ] I completed Labs 10.1–10.4 including each negative test.
