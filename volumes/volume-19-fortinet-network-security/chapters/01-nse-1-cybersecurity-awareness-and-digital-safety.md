# Chapter 01: NSE 1 Cybersecurity Awareness and Digital Safety

![Lab flow for this chapter: a password manager's breach report identifies reused or weak credentials, and the highest-value reused account gets a unique generated password and authenticator-app MFA. As a negative test, signing in from a fresh private browser session using only the password is rejected or paused pending the second factor, confirming MFA is actually enforced rather than merely available but optional. Separately, a sample phishing message is analyzed without clicking any link, producing a written analysis of its structural indicators.](../../../diagrams/volume-19-fortinet-network-security/chapter-01-security-hygiene-mfa-enforcement-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: a personal security hygiene audit culminating in an MFA enforcement check, with a structural phishing-message analysis.*

## Learning Objectives

- Describe the categories of threats an individual user encounters (phishing,
  social engineering, malware, credential theft) and the mechanics behind
  each one.
- Explain why security awareness is treated as a control alongside technical
  controls, not a substitute for them.
- Identify the structural indicators of a phishing message and a spoofed
  website independent of specific brand examples.
- Configure multi-factor authentication (MFA) and a password manager as
  personal baseline controls.
- Place NSE 1 in the Fortinet NSE Training Institute's eight-level
  certification structure and describe what each surrounding level covers.

## Theory and Architecture

### Why awareness is a control, not a formality

Every technical control this encyclopedia describes — a firewall policy, an
IPS signature, an SSL inspection profile — sits downstream of a human
decision: whether to click a link, open an attachment, approve a
multi-factor prompt, or read a password over the phone. Verizon's annual
Data Breach Investigations Report and equivalent industry studies have
consistently found that a majority of confirmed breaches involve a human
element — a credential handed over, a message trusted, an approval granted
without verification. Fortinet's NSE 1 curriculum exists because a security
architecture with a hardened perimeter and an unaware workforce still fails
at its weakest point. Awareness training is not a compliance checkbox
layered on top of technical controls; it is the control that determines
whether the technical controls ever get bypassed through the user rather
than through the network.

### Social engineering mechanics

Social engineering is the manipulation of a person, rather than a system,
into taking an action that benefits the attacker. It works by exploiting
predictable human responses:

- **Authority** — a message impersonating a executive, IT administrator, or
  law enforcement, relying on the target's reluctance to question a
  perceived superior.
- **Urgency** — a deadline, a threatened account suspension, or a "your
  package could not be delivered" pretext that pressures the target to act
  before verifying.
- **Reciprocity and trust** — a message that appears to come from a known
  colleague, vendor, or service the target already has a relationship with.
- **Scarcity and fear** — limited-time offers, account lockout threats, or
  claims of compromised credentials that must be "verified immediately."

Phishing is the most common delivery mechanism for social engineering and
comes in several distinct forms an aware user should be able to name:

| Variant | Mechanism |
| --- | --- |
| Phishing | Bulk, untargeted email impersonating a trusted brand or service |
| Spear phishing | Targeted at a specific individual using researched personal or organizational detail |
| Whaling | Spear phishing targeted at an executive or other high-value individual |
| Smishing | Phishing delivered by SMS text message |
| Vishing | Phishing conducted by voice call, increasingly assisted by AI voice cloning |
| Business email compromise (BEC) | Impersonation of an executive or vendor to redirect a legitimate financial transaction |
| Quishing | Phishing delivered via a malicious QR code, which bypasses URL-hover inspection on the underlying link |

### Structural indicators, not brand memorization

Training that teaches "watch for emails claiming to be from Bank X" fails
the moment the attacker impersonates Bank Y instead. NSE 1-level awareness
instead teaches structural indicators that generalize across any
impersonated brand:

- **Sender domain mismatch** — the display name says one organization but
  the underlying sending domain (visible by expanding the sender detail, not
  just the display name) does not match that organization's actual domain,
  or uses a look-alike domain (character substitution, added subdomain, or
  a different top-level domain).
- **Mismatched or shortened links** — the visible link text does not match
  the actual destination shown when hovering over it, or the link uses a
  URL shortener that hides the true destination.
- **Unsolicited attachment or credential request** — a request to open an
  unexpected invoice, resume, or shipping document, or a login page
  requesting credentials reached by clicking a link rather than by
  navigating directly.
- **Pressure and consequence framing** — any message that discourages the
  recipient from pausing to verify through a second channel.
- **Generic or malformed greeting/grammar** — decreasingly reliable as an
  indicator, since AI-assisted phishing has largely eliminated the awkward
  phrasing that used to be a strong signal.

### Malware categories relevant to an end user

| Category | Behavior |
| --- | --- |
| Ransomware | Encrypts accessible files and demands payment for a decryption key; increasingly paired with data exfiltration ("double extortion") |
| Trojan | Disguises itself as legitimate software to gain execution, then delivers a separate payload |
| Worm | Self-propagates across a network without requiring further user action once launched |
| Spyware / keylogger | Captures credentials, keystrokes, or screen activity and exfiltrates them |
| Adware | Delivers unwanted advertising, often bundled with legitimate-looking free software |
| Rootkit | Embeds itself at a privileged system level to hide its own presence and other malware |
| Fileless malware | Executes in memory or through legitimate system tools (living-off-the-land) rather than writing a detectable file to disk |

### Identity risk: passwords, reuse, and MFA

Password-based authentication fails predictably: users reuse passwords
across services, choose memorable-but-guessable patterns, and fall for
credential-harvesting phishing pages. Once one service is breached and its
password database leaked, attackers run **credential stuffing** — testing
the same username/password pair against many other services, betting on
reuse. Two controls address this directly:

- **A password manager** generates and stores a unique, high-entropy
  password per service, removing the human incentive to reuse or
  simplify passwords.
- **Multi-factor authentication (MFA)** requires a second, independent proof
  of identity — a time-based one-time code (TOTP), a push approval to a
  registered device, or a hardware security key (FIDO2/WebAuthn) — so a
  leaked password alone is insufficient to authenticate.

MFA is not uniformly resistant to attack. **MFA fatigue** (or "push
bombing") sends repeated push approval requests until an annoyed or
distracted user approves one; **SIM swapping** ports a victim's phone
number to an attacker-controlled device to intercept SMS codes. This is why
FIDO2 hardware security keys and number-matching push approval are
considered stronger MFA than SMS-delivered codes: they are not
phishable or approvable by accident in the same way.

### The Fortinet NSE Training Institute structure

The Fortinet Network Security Expert (NSE) program is an eight-level
training and certification path. NSE 1 through 3 are free, vendor-neutral
or lightly vendor-flavored awareness and portfolio-overview content
available to anyone; NSE 4 and above require hands-on product knowledge and
increasingly specialized, role-based tracks:

| Level | Focus |
| --- | --- |
| NSE 1 | Cybersecurity awareness and digital safety for any end user (this chapter) |
| NSE 2 | Threat landscape evolution and a technology-category overview of the Fortinet Security Fabric portfolio ([Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md)) |
| NSE 3 | Security Fabric architecture and introductory product-level knowledge for pre-sales, support, and operator roles ([Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md)) |
| NSE 4 | FortiOS administrator: hands-on FortiGate policy, VPN, security profile, routing, and HA configuration (Chapters 04–09) |
| NSE 5–7 | Role-based tracks covering central management (FortiManager/FortiAnalyzer), advanced security architecture, and specialist product tracks |
| NSE 8 | Expert-level, lab-based practical exam validating hands-on architecture and troubleshooting mastery |

This volume's chapter sequence follows that structure through NSE 4: it
builds awareness (NSE 1), portfolio literacy (NSE 2), and Security Fabric
familiarity (NSE 3) before the deep, hands-on FortiOS administrator content
that maps to NSE 4 (Chapters 04–09).

## Design Considerations

- **Program cadence, not a one-time event.** A single onboarding training
  session has a short half-life. Effective awareness programs combine
  periodic refresher training, simulated phishing campaigns with
  measured click/report rates, and just-in-time coaching delivered at the
  moment a user reports or nearly falls for a real attempt.
- **Positive reporting culture over punishment.** A user who clicks a
  malicious link and immediately reports it gives the security team a fast
  detection signal; a punitive culture teaches users to hide mistakes
  instead, which delays detection far more than the original click
  cost. Design the program to reward reporting, including false positives.
- **Simulated phishing realism vs. trust erosion.** Simulated phishing
  campaigns that are too aggressive, too frequent, or thematically
  distasteful (for example, impersonating a benefits or emergency
  announcement) can erode trust in real organizational communications.
  Calibrate difficulty progressively and exclude sensitive themes.
- **Acceptable use policy (AUP) as the written baseline.** Awareness
  training explains the "why"; the AUP is the enforceable "what" —
  acceptable device use, data handling, and reporting obligations that
  employment and disciplinary processes can reference.
- **BYOD and personal-device exposure.** Where personal devices access
  organizational resources, awareness content must cover device-level
  hygiene (screen lock, OS patching, avoiding sideloaded applications) in
  addition to organization-owned endpoint expectations, since the
  organization has less direct technical control over a personal device.

## Implementation and Automation

Awareness-level controls are personal and organizational procedures rather
than device configuration, but they are still implemented in a
repeatable, checklist-driven way rather than left informal. The following
baseline applies at the individual level and scales to a rollout runbook at
the organizational level.

### Personal security hygiene baseline

1. Install a reputable password manager and migrate reused or weak
   passwords to unique, generated ones, prioritizing email, financial, and
   single sign-on (SSO) identity accounts first.
2. Enable MFA on every account that supports it, preferring an
   authenticator app or FIDO2 hardware key over SMS where available.
3. Verify the device operating system and browser are set to install
   security updates automatically.
4. Confirm the mail client or webmail provider has a one-click "report
   phishing" action enabled and know where reported messages route.
5. Review account recovery options (backup email, recovery phone number)
   for currency — a stale recovery phone number is a common account-takeover
   vector after a number is reassigned by a carrier.

### Organizational rollout runbook (checklist form)

```text
1. Baseline: run a benign, unannounced phishing simulation to record a
   starting click-rate and report-rate metric.
2. Policy: publish or refresh the Acceptable Use Policy and a one-page
   "how to report suspicious messages" reference.
3. Enrollment: require MFA enrollment for all accounts within a fixed
   grace period; track completion percentage as a rollout metric.
4. Training: deliver role-appropriate awareness training (general staff,
   privileged/administrative users, and finance/HR staff who are
   disproportionately targeted by BEC).
5. Cadence: schedule recurring simulated phishing at a randomized interval
   (not a predictable monthly date) and quarterly refresher content.
6. Feedback loop: route every simulation result and every real user report
   into a tracked metric reviewed by security leadership, not just IT.
```

This runbook produces auditable artifacts — enrollment percentage,
click-rate trend, and report-rate trend — that a security program can
report as measurable risk reduction rather than an assumed benefit of
training having been delivered.

## Validation and Troubleshooting

- **Verify MFA enrollment, not just policy existence.** A policy requiring
  MFA is not evidence that MFA is enforced. Pull an enrollment report from
  the identity provider and confirm the percentage, not the policy
  document.
- **Click-rate trending upward instead of downward.** If simulated phishing
  click-rates rise or plateau across quarters, the content is likely
  becoming predictable (same sender pattern, same time of month) or
  training is not reaching the population that is clicking; segment results
  by department to find where remediation is actually needed.
- **Reused password exposure.** Password managers and some identity
  providers can check current credentials against known-breach datasets;
  treat any match as a mandatory, immediate password rotation, not just an
  advisory.
- **MFA fatigue indicators.** A spike in denied or ignored push approval
  requests for a given account, especially outside that user's normal
  working hours, is a strong signal of an in-progress credential-stuffing
  or push-bombing attempt and should route to the security operations
  workflow described in [Volume X](../../volume-10-enterprise-cybersecurity/README.md), not be dismissed as user error.
- **Recovery-path drift.** Periodically audit recovery email/phone fields
  across critical accounts; a recovery contact that has quietly gone stale
  (old phone number, departed employee's personal email) undermines account
  recovery security even when the primary MFA method is strong.

## Security and Best Practices

- Treat every unsolicited request for credentials, payment redirection, or
  urgent action through an unusual channel as unverified until confirmed
  through a second, independently sourced channel (a known phone number,
  not one provided in the suspicious message itself).
- Prefer phishing-resistant MFA (FIDO2 hardware keys, platform passkeys) for
  high-value accounts — email, identity provider/SSO, and financial systems
  — over SMS or push-only MFA.
- Never disable or bypass MFA to "make something work faster"; if MFA is
  blocking a legitimate workflow, fix the workflow, not the control.
- Report suspected phishing even after acting on it (clicking a link,
  entering credentials); fast reporting shrinks the response window far
  more than the embarrassment of having clicked costs.
- Keep awareness content current with the threat landscape described in
  [Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md) — AI-assisted phishing, deepfake voice/video vishing, and
  QR-code quishing are materially changing what "looks suspicious" means
  relative to a decade-old awareness curriculum.

## References and Knowledge Checks

**References**

- [Fortinet NSE Training Institute, *NSE 1: Cybersecurity Awareness*
  learning path.](https://training.fortinet.com/local/staticpage/view.php?page=nse_1)
- [Verizon, *Data Breach Investigations Report* (annual), human-element
  breach statistics.](https://www.verizon.com/business/resources/reports/dbir/)
- [FIDO Alliance, *FIDO2/WebAuthn* specification overview.](https://fidoalliance.org/specifications/)
- [NIST Special Publication 800-63B, *Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/b/upd2/final) —
  Authentication and Lifecycle Management*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — encyclopedia-wide
  dated baseline reference.

**Knowledge checks**

1. Name three structural indicators of a phishing message that generalize
   across any impersonated brand.
2. Why is SMS-delivered MFA considered weaker than a FIDO2 hardware key or
   authenticator app?
3. Describe the mechanism behind an MFA fatigue (push-bombing) attack and
   one behavioral indicator that should trigger investigation.
4. Why does a punitive response to a reported phishing click reduce an
   organization's overall detection speed?
5. Where does NSE 1 sit relative to NSE 2 and NSE 3 in the Fortinet NSE
   Training Institute's certification structure?

## Hands-On Lab

**Objective:** Perform a personal security hygiene self-audit, enable MFA
on a test account, and analyze a sample phishing message for structural
indicators — no FortiGate hardware or lab appliance is required for this
chapter.

**Prerequisites**

- A password manager (any reputable option with a free tier is sufficient).
- A test or personal email account that supports authenticator-app MFA.
- A text editor to record findings.

**Steps**

1. Open your password manager's built-in security/breach report (or
   equivalent free breach-check service) and record how many accounts show
   reused or weak passwords.

   **Expected result:** A count of reused/weak credentials, which most
   users find is greater than zero on a first run.

2. Rotate the password for your single highest-value reused account
   (typically the primary email account) to a unique, generated password
   stored in the password manager.

3. Enable authenticator-app-based MFA on that same account, following the
   provider's setup flow, and store the recovery codes in the password
   manager's secure notes rather than as a plain text file.

   **Expected result:** The account now requires a TOTP code or push
   approval in addition to the password at sign-in; confirm this by signing
   out and back in.

4. **Negative test:** Attempt to sign in to the account using only the
   password, from a fresh browser session or private/incognito window.

   **Expected result:** Authentication is rejected or paused pending the
   second factor — confirming MFA is actually enforced, not merely
   available but optional.

5. Locate or construct a sample phishing email (many mail providers keep a
   "Junk"/"Spam" folder with real examples, or use a published awareness
   training sample). Without clicking any link, identify and record:
   - The sender's actual domain versus the displayed name.
   - Whether hovering over the primary call-to-action link shows a
     mismatched destination.
   - Which social engineering lever (authority, urgency, fear, reciprocity)
     the message uses.

6. Use the mail client's "report phishing" action on the sample message, or
   describe the reporting path if the sample was not a real inbox item.

   **Expected result:** A completed written analysis identifying at least
   three structural indicators, independent of the specific brand
   impersonated.

**Cleanup**

- No system changes require reverting; MFA and the rotated password should
  remain in place as a permanent security improvement rather than being
  undone.
- If a shared or lab email account was used for the phishing sample review,
  delete the sample from the mailbox after analysis is recorded.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Security awareness is the human-layer control every subsequent chapter's
technical controls depend on. This chapter established the mechanics of
social engineering and phishing, malware categories relevant to an end
user, identity risk from password reuse, MFA as the primary mitigating
control (and its own weaknesses, such as fatigue and SIM swapping), and
where NSE 1 sits in the Fortinet NSE Training Institute's eight-level
program. [Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md) builds on this awareness foundation with a
technology-category view of the threat landscape and the Fortinet Security
Fabric portfolio that responds to it.

- [ ] Can describe at least four social engineering mechanisms and three
      phishing variants.
- [ ] Can list structural phishing indicators independent of specific
      brand impersonation.
- [ ] Can explain why MFA is not uniformly phishing-resistant and name a
      stronger alternative to SMS-delivered codes.
- [ ] Can place NSE 1 correctly within the NSE 1–8 program structure.
- [ ] Completed the hands-on lab, including the negative test.
