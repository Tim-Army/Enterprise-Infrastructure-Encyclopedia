# Volume XXXVII Glossary

Definitions for terms used in **Volume XXXVII — Microsoft 365 and Modern
Work**, alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Access package** — An entitlement-management bundle of groups, apps, and
sites with a request-and-approval policy and expiration, used to make access
requestable and time-bound. Used in Chapter 04.

**App Protection Policy (APP/MAM)** — An Intune policy that protects corporate
data inside apps (PIN, encryption, restricted transfer, selective wipe)
without managing the whole device; the BYOD control. Used in Chapter 07.

**Conditional Access** — The Entra policy engine that evaluates users, apps,
and conditions at sign-in and applies grant and session controls (require MFA,
compliant device, block). Used in Chapter 03.

**Compliance policy** — An Intune policy defining a healthy device (encryption,
OS floor, risk) whose compliance state is consumed by Conditional Access. Used
in Chapter 06.

**DKIM (DomainKeys Identified Mail)** — An email-authentication method that
signs outbound mail with a DNS-published key so receivers can verify it was
not altered. Used in Chapter 08.

**DLP (Data Loss Prevention)** — Purview policies that detect sensitive content
across Exchange, SharePoint, OneDrive, Teams, endpoints, and cloud apps and
take action (notify, block, restrict). Used in Chapter 10.

**DMARC** — A DNS policy that tells receivers what to do when SPF/DKIM fail
(none/quarantine/reject) and where to send reports; the enforcer of email
authentication. Used in Chapter 08.

**Defender XDR** — Microsoft's extended detection and response suite that
correlates identity, endpoint, email, and cloud-app signals into unified
incidents in the Defender portal. Used in Chapter 11.

**Entitlement management** — The Entra identity-governance feature that
automates access request, approval, provisioning, and time-bound removal via
access packages. Used in Chapter 04.

**Known Folder Move (KFM)** — A OneDrive feature that redirects the Windows
Desktop, Documents, and Pictures folders into OneDrive for backup and roaming.
Used in Chapter 09.

**MDM / MAM** — Mobile Device Management (managing the whole enrolled device)
and Mobile Application Management (protecting corporate data inside apps); the
two Intune models. Used in Chapter 05.

**Microsoft 365 Group** — The membership object that provisions a SharePoint
site, group mailbox, planner, and (if a team) a Teams team; the substrate
behind the collaboration workloads. Used in Chapter 09.

**Microsoft Graph PowerShell SDK** — The supported, scriptable module over the
unified Microsoft Graph API used to administer Microsoft 365 at scale. Used in
Chapter 01.

**PHS (password hash synchronization)** — A hybrid sign-in method where a hash
of the on-premises password hash is synced to Entra so cloud authentication
works even if on-premises is down; usually the most resilient option. Used in
Chapter 04.

**PIM (Privileged Identity Management)** — The Entra P2 feature that makes
privileged roles eligible and just-in-time, requiring activation with
justification, MFA, time limits, and optional approval. Used in Chapter 04.

**Report-only (Conditional Access)** — A policy state that evaluates and logs
impact in the sign-in logs without enforcing, used to stage policies safely.
Used in Chapter 03.

**Retention policy / label** — Purview controls that keep content for a defined
period and then delete it (or trigger disposition), governing the data
lifecycle. Used in Chapter 10.

**Safe Attachments / Safe Links** — Defender for Office 365 features that
sandbox-detonate attachments and time-of-click-check URLs to protect against
malicious mail and collaboration content. Used in Chapter 11.

**Secure Score** — Microsoft's percentage measure of security posture against a
catalog of prioritized improvement actions. Used in Chapter 11.

**Sensitivity label** — A Purview label that classifies content and can apply
encryption, visual marking, and container protection, traveling with the file
so protection persists off-platform. Used in Chapter 10.

**Service plan** — An individual capability (Exchange Online, Intune, Entra ID
P2) bundled inside a licensing SKU; a user needs the plan enabled to use the
service. Used in Chapter 01.

**Settings catalog** — Intune's searchable library of individual configuration
settings that has largely replaced the older per-template profiles. Used in
Chapter 06.

**Tenant** — An isolated instance of Microsoft Entra ID that contains an
organization's identities, subscriptions, and data; the container every
Microsoft 365 service trusts. Used in Chapter 01.

**Windows Autopilot** — A zero-touch provisioning service that configures a new
Windows device (Entra join, Intune enrollment, policies, apps) on first boot
without imaging, gated by the Enrollment Status Page. Used in Chapter 07.

**Win32 app** — An Intune application packaged as `.intunewin` with
install/uninstall commands, detection rules, and requirement rules; the
workhorse format for enterprise Windows software. Used in Chapter 07.
