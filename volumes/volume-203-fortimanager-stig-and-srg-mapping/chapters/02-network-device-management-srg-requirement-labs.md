# Chapter 02: Network Device Management SRG Requirement Labs

## Learning Objectives

- Prove each Network Device Management SRG requirement of this volume on the Chapter 999 lab, with a positive and a negative test.
- Give each administrator a role and an ADOM, and limit the management path to the admin network.
- Set the logon, password, authentication server, and certificate rules.
- Produce, protect, store, and off-load the audit records the SRG lists, with accurate time.
- Control who may change a managed device, and how a change is approved, recorded, and backed up.
- Record what FortiManager 7.6 cannot meet, and the compensating control for it.
- Store the evidence for each lab so it can support an assessment.

## Theory and Architecture

The Network Device Management SRG covers how an administrator reaches, authenticates to, and is held accountable on a network device. FortiManager has no STIG, so it is assessed against this SRG. It is not an ordinary device, though. A FortiManager administrator can change every device it manages, so the requirements for access control, auditing, and change control carry more weight here than on a single device, as Chapter 01 explains.

The labs follow an administrator's work. Labs 2.1 and 2.2 decide who may connect, from where, and with what role. Labs 2.3 to 2.6 cover the logon: its protections, the password rules, the authentication servers, and certificates. Labs 2.7 to 2.11 produce the audit records, show what each one holds, record changes and privileged commands, protect and store the records, and send them away. Labs 2.12 and 2.13 cover time and cryptography. Lab 2.14 covers the part that is specific to FortiManager: who may change a managed device, and how. Labs 2.15 and 2.16 cover backup and the software release. Lab 2.17 documents the one requirement that FortiManager cannot meet.

All labs run on the network from [Chapter 999](999-shared-lab-infrastructure.md).

### Requirements and labs

This volume's tables cite 79 distinct Network Device Management SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 2.1 | 5 | Requirement lab: Roles and ADOMs: who may see and change what |
| 2.2 | 6 | Requirement lab: The management path: trusted hosts, local-in policy, services, and sessions |
| 2.3 | 4 | Requirement lab: Logon protections: lockout, banners, and session timeout |
| 2.4 | 6 | Requirement lab: Password policy: length, character classes, and change distance |
| 2.5 | 3 | Requirement lab: Authentication servers and the account of last resort |
| 2.6 | 7 | Requirement lab: Certificates and multifactor authentication: PKI administrators, revocation, and trust anchors |
| 2.7 | 9 | Requirement lab: Audit events: accounts, logons, and privileges |
| 2.8 | 6 | Requirement lab: Audit record content: what, when, where, source, outcome, and who |
| 2.9 | 5 | Requirement lab: Audit of changes and privileged commands: event log filters, revisions, and TACACS+ accounting |
| 2.10 | 6 | Requirement lab: Protecting and storing audit records: access, capacity, and alerts |
| 2.11 | 2 | Requirement lab: Off-loading the event log: syslog and FortiAnalyzer |
| 2.12 | 5 | Requirement lab: Time: authenticated NTP and time stamps |
| 2.13 | 5 | Requirement lab: Cryptography: strong ciphers, SNMPv3, and FIPS-CC mode |
| 2.14 | 2 | Requirement lab: Change control for managed devices: device authorization, the FGFM tunnel, workspace, and workflow |
| 2.15 | 2 | Requirement lab: Configuration backup: scheduled, on demand, and encrypted |
| 2.16 | 5 | Requirement lab: Software: supported release, security updates, and signed firmware |
| 2.17 | 1 | Gap lab: Gaps: passwords checked against a list of compromised passwords |

A **requirement lab** configures the FortiManager setting, proves it with a positive test, and proves the control with a negative test. A **gap lab** covers requirements that FortiManager cannot meet: it proves that the setting is absent, applies the nearest compensating control, and records the disposition.

## Design Considerations

- **The lab unit runs FortiManager 7.6.** Chapter 01 checked its commands against the FortiManager 8.0.1 CLI Reference. Its version column shows NTP authentication with SHA-256 as 8.0.0 and later (Lab 2.12). If release 7.6 rejects any other option, type `set ?` in that context, use what the release offers, and record the difference as a finding.
- **Use a throwaway account for lockout and password tests.** A lockout test can lock the account you are logged on with. Run it against a local test account, and keep the console of `fmg-203` open.
- **Test with a managed device.** The change control labs need a device to change. `fgt-202`, the FortiGate-VM of Volume CCII, is managed by `fmg-203` in this lab.
- **Prove the record, not only the setting.** For the audit requirements the evidence is a record: the event log line, the accounting record on `tacacs-201`, or the forwarded record on `syslog-201a`.
- **Run the FIPS-CC step last.** FIPS-CC mode can be enabled only from the console and changes how the unit works, so take the snapshot first and restore the baseline afterward.
- **Some requirements are procedures.** One local account only, a supported release, and updates within 30 days are shown by a record or a review, not by a setting alone.
- **Say what a lab CA cannot prove.** `ca-201` proves the certificate mechanics but not DoD trust, so the DoD PKI requirements keep a procedural check.

## Implementation and Automation

Each lab lists its commands in the order to enter them. Commands come from [Chapter 01](01-fortimanager-feature-version-and-srg-map.md), with the lab's values from Chapter 999 substituted.
The placeholders are `<LAB_ADMIN>` for a RADIUS-authenticated administrator, `<SECRET>`, `<KEY>`, and `<PASSWORD>` for values you generate for the run, `<PORT>` for the management port of `fmg-203`, and `<DOD_BANNER>` for the approved banner text. Addresses are those of Chapter 999. A step that names a GUI pane has no CLI command in Chapter 01.

Save the evidence for each lab in `evidence/<lab>/<date>/`, as Chapter 999 describes.

## Validation and Troubleshooting

Before each lab, confirm the baseline: `get system status` on `fmg-203` shows the release, `diagnose dvm device list` shows `fgt-202` as managed, and `fmg-203` answers a ping from `admin-201`. After each lab, restore the baseline and repeat the checks.

| Symptom | Cause | Fix |
| --- | --- | --- |
| A command is rejected | The option belongs to a later release than 7.6 | Type `set ?` in that context, use what the release offers, and record the difference |
| The RADIUS administrator cannot log on | `fmg-203` is not a client of `radius-201a`, the secret differs, or the server does not accept RADIUS over TLS | Check the client entry and the secret on `radius-201a`, and the protocol under `config system admin radius` |
| `fgt-202` does not appear in Device Manager | The FortiGate does not point at `10.200.2.130`, or registration is disabled and the device was not added first | Check central management on the FortiGate, and add the device in Device Manager |
| An install to `fgt-202` is refused | The ADOM or the policy package is locked by another session, or the change is waiting for approval | Unlock it, or approve the change (Lab 2.14) |
| No alert email arrives | `mail-202` is unreachable, or the account or the STARTTLS setting is wrong | Check `config system mail` and the mail log on `mail-202` |
| You are locked out after a lockout or trusted-host test | The test hit your own account or address | Use the console of `fmg-203`, or restore the baseline |

## Security and Best Practices

- Run every test inside the lab network, and never point a negative test at a production FortiManager or at a production device it manages.
- Generate fresh secrets, keys, and passwords for each run, write them as `<SECRET>` in the evidence, and delete them in the cleanup.
- Keep the console of `fmg-203` open while you test lockout, trusted hosts, and FIPS-CC mode.
- Install to `fgt-202` only. A lab that pushes configuration must not have a second, real device in its ADOM.
- Treat a negative test that fails to refuse as a finding, not as a lab error.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortimanager-feature-version-and-srg-map.md) for the rows these labs prove.
- [Chapter 999](999-shared-lab-infrastructure.md) for the lab network, hosts, and baseline.
- DISA Network Device Management SRG V5R5, from the October 2026 STIG Library Compilation. Confirm the current release on the DoD Cyber Exchange.
- Fortinet, *FortiManager 8.0.1 CLI Reference* and the *FortiManager New Features Guides* for 7.0 to 8.0, which Chapter 01 used, and the *FortiManager Administration Guide* of your release for the GUI steps.
- [Volume CLXXII, Chapter 03](../../volume-172-disa-srgs-and-stigs/chapters/03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md) for assessing a product that has no STIG.

**Knowledge checks:**

1. Why do access control and change control carry more weight on a FortiManager than on one managed device?
2. Which two settings together keep an administrator from installing a policy package?
3. Why does the full text of a privileged command need a TACACS+ server?
4. What is the difference between workspace mode and workflow mode, and which requirement does each help meet?
5. Which requirement can FortiManager not meet, and what is the compensating control?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 and its baseline. The `baseline-203` snapshot of `fmg-203`, with `fgt-202` managed by it. The hypervisor console of `fmg-203`. A local test account, a RADIUS administrator, and an SSH client and a browser on `admin-201`. **Cost:** none beyond the Chapter 999 lab. A firmware image is needed only if you choose to run the upgrade in Lab 2.16.

### Lab 2.1 — Roles and ADOMs: who may see and change what

**Goal.** Show that each administrator has an account of their own with a profile and an ADOM, and that a profile decides what the administrator may read, change, and install.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000033-NDM-000212` | I | Assign a role or access level to each authenticated administrator. | Individual administrator accounts; Administrator profiles (role-based access); Administrative domains (ADOMs); and 29 more |
| `SRG-APP-000153-NDM-000249` | II | Authenticate each administrator before granting privileges by group or role. | Individual administrator accounts; TACACS+ administrator authentication; SAML SSO wildcard admin user to match all users on IdP server; and 1 more |
| `SRG-APP-000329-NDM-000287` | II | Enforce role-based access control over the defined subjects and objects. | Administrator profiles (role-based access); Access permission for the IPS Admin using the Restricted Admin profile gives granular access to a selected list of ADOMs; New firewall admin role with no RW permission on IPS objects; and 7 more |
| `SRG-APP-000340-NDM-000288` | I | Keep non-privileged users from privileged functions and from changing safeguards. | Administrator profiles (role-based access); Policy packages and installation to devices; CLI and TCL scripts; and 3 more |
| `SRG-APP-000231-NDM-000271` | I | Let only authorized administrators view or change the configuration and stored files. | Private data encryption; Administrator profiles (role-based access); TPM hardware module; and 4 more |

**Uses.** `fmg-203`, `fgt-202`, `admin-201`, and `radius-201a`.

**Configure.**

1. Enable ADOMs. Create the ADOM `lab-203` in the GUI, because Chapter 01 has no command for it, and put `fgt-202` in it.

   ```text
   config system global
       set adom-status enable
   end
   ```

2. Create a profile that can read the devices and the policy, and can neither change the system nor install.

   ```text
   config system admin profile
       edit lab-readonly
           set system-setting none
           set device-manager read
           set policy-objects read
           set deploy-management none
   end
   ```

3. Give each person an account of their own with a profile and an ADOM.

   ```text
   config system admin user
       edit <LAB_ADMIN>
           set profileid lab-readonly
           set adom lab-203
   end
   ```

4. Encrypt the private data the unit stores, such as the passwords and keys of the managed devices. If the unit asks for an encryption key, generate one for the run and record it as `<SECRET>`.

   ```text
   config system global
       set private-data-encryption enable
   end
   ```

**Positive test.** `<LAB_ADMIN>` logs on from `admin-201`, sees only the ADOM `lab-203`, and can read the configuration of `fgt-202` and its policy package.

**Negative test.** `<LAB_ADMIN>` cannot open the system settings, cannot change a policy, and cannot install to `fgt-202`: each action is refused or not offered. The administrator sees no device of another ADOM. A logon with a name that has no account of its own is refused.

**Evidence.** The profile and the administrator account from `show full-configuration`, the refused actions of `<LAB_ADMIN>`, and the event log lines for the logon and the refused actions.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.2 — The management path: trusted hosts, local-in policy, services, and sessions

**Goal.** Show that management is reachable only from the admin network, only over HTTPS and SSH, and that an administrator account has a limit on its sessions.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000038-NDM-000213` | II | Control the flow of management information by approved policy. | Trusted hosts for administrators; Administrative domains (ADOMs); JSON API administrators; and 8 more |
| `SRG-APP-000408-NDM-000314` | II | Restrict maintenance functions to authorized personnel. | Interface administrative access; Trusted hosts for administrators; Terminal (CLI) access to managed devices; and 7 more |
| `SRG-APP-000880-NDM-000290` | II | Separate nonlocal maintenance sessions from other network sessions. | Trusted hosts for administrators |
| `SRG-APP-000142-NDM-000245` | I | Prohibit unnecessary or nonsecure functions, ports, protocols, and services. | Interface administrative access; Debug tool; SNMP v1 and v2c communities; and 214 more |
| `SRG-APP-000435-NDM-000315` | II | Protect the unit against known kinds of denial-of-service attack. | Administrative access to FortiManager controlled by IPv4/IPv6 local-in policy |
| `SRG-APP-000001-NDM-000200` | II | Limit the concurrent sessions of each administrator account. | Concurrent administrator sessions |

**Uses.** `fmg-203` and `admin-201`. For the negative test, a lab host outside the admin network, for example `nms-201`.

**Configure.**

1. Limit where an administrator may connect from.

   ```text
   config system admin user
       edit <LAB_ADMIN>
           set trusthost1 10.200.3.0 255.255.255.0
   end
   ```

2. Limit what reaches the management port with a local-in policy.

   ```text
   config system local-in-policy
       edit 1
           set intf <PORT>
           set src 10.200.3.0 255.255.255.0
           set dport 443
           set protocol tcp
           set action accept
   end
   ```

3. Allow only HTTPS and SSH on the port, and turn off the debug tool.

   ```text
   config system interface
       edit <PORT>
           set allowaccess https ssh
   end
   config system global
       set debug-tool disable
   end
   ```

4. Limit the concurrent sessions, for the unit and for one account.

   ```text
   config system admin setting
       set admin-login-max <NUMBER>
   end
   config system admin user
       edit <LAB_ADMIN>
           set login-max <NUMBER>
   end
   ```

**Positive test.** From `admin-201`, `<LAB_ADMIN>` logs on over HTTPS and over SSH. With the limit set to two, a first and a second session of the account are accepted.

**Negative test.** From `nms-201`, HTTPS and SSH to `fmg-203` are refused, because the address is outside the trusted host and the local-in policy. From `admin-201`, HTTP and Telnet are refused, because the port does not allow them. A third session of `<LAB_ADMIN>` is refused while two are open.

**Evidence.** The administrator account, the local-in policy, and the interface from `show full-configuration`, the refused connections from `nms-201`, the refused third session, and the event log lines for each.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.3 — Logon protections: lockout, banners, and session timeout

**Goal.** Show that repeated failures lock an account for 15 minutes, that the DoD notice is shown before logon and must be accepted, and that idle sessions end after five minutes.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000065-NDM-000214` | II | Block logons for 15 minutes after three consecutive failed attempts. | Administrator lockout |
| `SRG-APP-000068-NDM-000215` | II | Show the DoD Notice and Consent Banner before granting access. | Pre-login banner; Post-login access banner |
| `SRG-APP-000069-NDM-000216` | II | Keep the banner on screen until the administrator accepts it. | Pre-login banner |
| `SRG-APP-000190-NDM-000267` | I | End a management session when it closes or after five minutes of inactivity. | Idle session timeout |

**Uses.** `fmg-203` and `admin-201`. Use a local test account, so that a lockout does not block the RADIUS administrator.

**Configure.**

1. Block logons for 15 minutes after three failed attempts.

   ```text
   config system global
       set admin-lockout-threshold 3
       set admin-lockout-duration 900
       set admin-lockout-method user
   end
   ```

2. Show the DoD Notice and Consent Banner before logon, and again after logon until the administrator accepts it. Use the approved text from your authorizing official.

   ```text
   config system global
       set pre-login-banner enable
       set pre-login-banner-message <DOD_BANNER>
   end
   config system admin setting
       set access-banner enable
       set banner-message <DOD_BANNER>
   end
   ```

3. End idle sessions after five minutes, in the CLI, the GUI, and the API.

   ```text
   config system admin setting
       set idle_timeout 300
       set idle_timeout_gui 300
       set idle_timeout_api 300
   end
   ```

**Positive test.** Open an SSH session and the GUI logon page from `admin-201`: the banner appears before the password prompt. After the logon to the GUI, the banner stays on screen until you accept it. Leave a session idle for five minutes: the unit ends it.

**Negative test.** Fail three logons for the test account: the fourth attempt, even with the right password, is refused for 15 minutes. Read the lockout in the event log. Decline the banner after logon: the session does not open.

**Evidence.** The banner in the SSH client transcript and on the GUI logon page, the lockout lines of the event log with their times, and the idle-timeout disconnect.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.4 — Password policy: length, character classes, and change distance

**Goal.** Show that the unit refuses passwords that are too short or that lack a character class, and record how many characters must change.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000164-NDM-000252` | II | Require passwords of at least 15 characters. | Password policy |
| `SRG-APP-000166-NDM-000254` | II | Require at least one uppercase character. | Password policy |
| `SRG-APP-000167-NDM-000255` | II | Require at least one lowercase character. | Password policy |
| `SRG-APP-000168-NDM-000256` | II | Require at least one numeric character. | Password policy |
| `SRG-APP-000169-NDM-000257` | II | Require at least one special character. | Password policy |
| `SRG-APP-000170-NDM-000329` | II | Require at least eight changed positions when a password changes. | Password policy |

**Uses.** `fmg-203` and `admin-201`, with a local test account.

**Configure.**

1. Turn on the password policy.

   ```text
   config system password-policy
       set status enable
       set minimum-length 15
       set must-contain upper-case-letter lower-case-letter number non-alphanumeric
       set change-4-characters enable
   end
   ```

2. Note the limit that Chapter 01 documents. `change-4-characters` requires four changed characters, and `SRG-APP-000170-NDM-000329` requires eight. Chapter 01 says to use remote authentication, so that the authentication server enforces the rule.

**Positive test.** Give the test account a password of 15 characters with an uppercase letter, a lowercase letter, a number, and a special character: the unit accepts it.

**Negative test.** Try a password of 14 characters, then one that lacks each character class in turn, then one that changes fewer than four characters of the old password: the unit refuses each. Then try one that changes four to seven characters: the unit accepts it, although the SRG asks for eight. Record that as the finding.

**Evidence.** The policy from `show full-configuration`, the refusal message for each bad password, and the accepted password change that shows the finding.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.5 — Authentication servers and the account of last resort

**Goal.** Show that administrators are authenticated by the lab's servers, that a second server answers when the first is stopped, and that the unit has one local account for emergencies.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000516-NDM-000336` | I | Authenticate administrators through at least one authentication server (two for boundary devices). | RADIUS administrator authentication; TACACS+ administrator authentication; LDAP administrator authentication; and 2 more |
| `SRG-APP-000156-NDM-000250` | II | Use replay-resistant authentication for network access to privileged accounts. | RADIUS administrator authentication; SAML assertions and SAML requests can be now signed to better support third-party IdPs |
| `SRG-APP-000148-NDM-000346` | II | Keep only one local account, the account of last resort. | Account of last resort |

**Uses.** `fmg-203`, `radius-201a`, `radius-201b`, `tacacs-201`, and `admin-201`.

**Configure.**

1. Use the two RADIUS servers over TLS, which also makes the logon replay-resistant. `set protocol tls` needs RADIUS over TLS on the servers (Chapter 999).

   ```text
   config system admin radius
       edit radius-201
           set server 10.200.2.10
           set secondary-server 10.200.2.11
           set secret <SECRET>
           set protocol tls
           set message-authenticator require
   end
   ```

2. Add the TACACS+ server, which Lab 2.9 also uses for accounting.

   ```text
   config system admin tacacs
       edit tacacs-201
           set server 10.200.2.12
           set key <KEY>
           set protocol tls
           set authorization enable
   end
   ```

3. Keep one local account as the account of last resort, and make every other administrator a remote account. Nothing in FortiManager limits the number of local accounts, so review the list by a documented procedure.

   ```text
   config system admin user
       edit <EMERGENCY_ADMIN>
           set user_type local
           set profileid <PROFILE>
   end
   ```

**Positive test.** A RADIUS administrator logs on. Stop `radius-201a`: the administrator still logs on, through `radius-201b`, and the event log names the logon. Stop both RADIUS servers and the TACACS+ server: `<EMERGENCY_ADMIN>` logs on from the console.

**Negative test.** Change the secret on `fmg-203` to a wrong value: a RADIUS logon is refused. List the administrators: any local account other than `<EMERGENCY_ADMIN>` is a finding. A capture of a RADIUS logon on `radius-201a` shows TLS and no password in clear text.

**Evidence.** The `radius`, `tacacs`, and administrator settings from `show full-configuration`, the event log lines for each logon, the list of local accounts with the review record, and the capture.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), and start the stopped servers again.

### Lab 2.6 — Certificates and multifactor authentication: PKI administrators, revocation, and trust anchors

**Goal.** Show that an administrator logs on with a certificate of the lab PKI that maps to one account, that the unit trusts only the lab CA, that it refuses a revoked certificate, and that its own HTTPS certificate comes from that CA.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000149-NDM-000247` | I | Use DoD PKI as multifactor authentication for interactive logons. | PKI (certificate) administrator authentication |
| `SRG-APP-000820-NDM-000170` | II | Implement multifactor authentication for access to privileged accounts. | FortiManager supports MFA with FortiToken Cloud |
| `SRG-APP-000177-NDM-000263` | I | Map each validated certificate to a unique user account. | PKI (certificate) administrator authentication |
| `SRG-APP-000175-NDM-000262` | I | Validate certificates with DoD-approved OCSP responders or CRLs. | PKI (certificate) administrator authentication; CA certificates and CRLs |
| `SRG-APP-000875-NDM-000280` | II | Check certificate revocation for public key-based authentication. | PKI (certificate) administrator authentication; CA certificates and CRLs |
| `SRG-APP-000910-NDM-000300` | II | Keep only approved trust anchors in the certificate stores. | CA certificates and CRLs |
| `SRG-APP-000516-NDM-000344` | II | Obtain public key certificates from an approved service provider. | Management (HTTPS) server certificate; Certificate/Certificate Template integrated to the SD-WAN Overlay Template; Certificate Template supports Enrollment over Secure Transport (EST) method; and 3 more |

**Uses.** `fmg-203`, `ca-201`, and `admin-201`. `ca-201` stands in for the DoD PKI, and a certificate file on `admin-201` stands in for the CAC.

**Configure.**

1. Install the CA certificate of `ca-201` and import its certificate revocation list. Chapter 01 documents that the list is imported and that the CLI Reference has no setting for OCSP or for fetching the list, so keep it current by procedure.

   ```text
   config system certificate ca
       edit lab-ca-201
           set ca <CERTIFICATE>
   end
   config system certificate crl
       edit lab-crl-201
           set crl <CRL>
   end
   ```

2. Create an administrator that logs on with a certificate, and ask every client for a certificate. The subject maps the certificate to this one account.

   ```text
   config system admin user
       edit <LAB_PKI_ADMIN>
           set user_type pki-auth
           set subject <CERT_SUBJECT>
           set ca lab-ca-201
   end
   config system global
       set clt-cert-req enable
   end
   ```

3. Use a certificate that `ca-201` issued for the HTTPS server of the unit.

   ```text
   config system admin setting
       set admin_server_cert <DOD_ISSUED_CERT>
   end
   ```

4. Read the list under `config system certificate ca` and keep only the trust anchors your organization approves.
5. Chapter 01 also lists FortiToken Cloud as a second factor (`set two-factor-auth ftc-ftm`). It needs a FortiToken Cloud subscription, which this lab does not have, so the lab proves the certificate logon only. On a CAC the PIN unlocks the private key, which makes the logon multifactor. The certificate file of the lab does not prove that part.

**Positive test.** From `admin-201`, open the GUI with the certificate of `<LAB_PKI_ADMIN>`: the browser shows the server certificate that `ca-201` issued, the logon succeeds, and the event log names the administrator.

**Negative test.** Connect with no certificate: the unit refuses the session. Connect with a certificate that another CA issued: refused. Revoke the administrator's certificate on `ca-201`, import the new list, and try again: refused. Before the new list is imported the revoked certificate still works, which is the limit that Chapter 01 documents. Record how old the list may get under your procedure.

**Evidence.** The CA, the revocation list, the administrator, and the server certificate from `show full-configuration`, the event log lines for the successful and the refused logons, and the date of the imported list.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.7 — Audit events: accounts, logons, and privileges

**Goal.** Show that the unit records account changes, privilege changes, logons, and the start and end of each session in its own event log, from startup.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000026-NDM-000208` | II | Audit the creation of accounts. | Individual administrator accounts; FortiManager event log (own audit records); ADOM Scoped Admin is a new admin profile to permit ADOM users to manage their own admin accounts within the ADOM |
| `SRG-APP-000027-NDM-000209` | II | Audit the modification of accounts. | FortiManager event log (own audit records) |
| `SRG-APP-000028-NDM-000210` | II | Audit the disabling of accounts. | FortiManager event log (own audit records) |
| `SRG-APP-000029-NDM-000211` | II | Audit the removal of accounts. | FortiManager event log (own audit records) |
| `SRG-APP-000495-NDM-000318` | II | Audit attempts to modify administrator privileges. | FortiManager event log (own audit records) |
| `SRG-APP-000091-NDM-000223` | II | Audit successful and unsuccessful attempts to access privileges. | FortiManager event log (own audit records) |
| `SRG-APP-000503-NDM-000320` | II | Audit successful and unsuccessful logon attempts. | FortiManager event log (own audit records); TACACS+ accounting of CLI commands, configuration changes, and logins |
| `SRG-APP-000505-NDM-000322` | II | Record the start and end time of each administrator session. | FortiManager event log (own audit records) |
| `SRG-APP-000092-NDM-000224` | II | Start session auditing at startup. | FortiManager event log (own audit records) |

**Uses.** `fmg-203` and `admin-201`.

**Configure.**

1. Turn on the local event log at the information level.

   ```text
   config system locallog disk setting
       set status enable
       set severity information
   end
   ```

**Positive test.** Create a local test account, change its profile, disable it, and delete it. Log on and log off once with another account, and fail one logon. The event log has a record for each of the four account actions, for the change of privileges, for the successful and the failed logon, and for the logoff. Restart `fmg-203`: the event log has records from the start of the unit.

**Negative test.** Set the status of the local event log to `disable`, create a second test account, and confirm that no record is written. This shows that the records depend on the setting. Enable the log again.

**Evidence.** The event log records for each action, with their times, the records after the restart, and the setting from `show full-configuration`.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.8 — Audit record content: what, when, where, source, outcome, and who

**Goal.** Show that one event log record holds everything the SRG lists: what happened, when, where, from which source, with what outcome, and by whom.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000095-NDM-000225` | II | Records show what type of event occurred. | FortiManager event log (own audit records); Event log easier to read; CLI option enables JSON API event log for both request and response |
| `SRG-APP-000096-NDM-000226` | II | Records show when the event occurred. | FortiManager event log (own audit records) |
| `SRG-APP-000097-NDM-000227` | II | Records show where the event occurred. | FortiManager event log (own audit records) |
| `SRG-APP-000098-NDM-000228` | II | Records show the source of the event. | FortiManager event log (own audit records) |
| `SRG-APP-000099-NDM-000229` | II | Records show the outcome of the event. | FortiManager event log (own audit records) |
| `SRG-APP-000100-NDM-000230` | II | Records identify the person or process behind the event. | FortiManager event log (own audit records); Firewall policy creator exposed; Per-admin mode: sync page shows administrator name and timestamp; and 1 more |

**Uses.** `fmg-203` and `admin-201`.

**Configure.**

1. Keep the local event log on at the information level, as in Lab 2.7.

   ```text
   config system locallog disk setting
       set status enable
       set severity information
   end
   ```

2. Open the event log in the GUI under System Settings, cause one successful and one failed action, for example a policy change that is allowed and one that is refused, and read the two records field by field.

**Positive test.** Each of the two records shows the type of event, the date and time, the part of the unit where it occurred, the source address, the outcome, and the administrator. In the GUI under Policy & Objects, the policy that was changed shows who created it.

**Negative test.** Look for a record that lacks one of the six items, among the records of this lab and of Lab 2.7. A record without one of them is a finding: note the event type and the missing item.

**Evidence.** The two records with each of the six items marked, and any record that lacks an item.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.9 — Audit of changes and privileged commands: event log filters, revisions, and TACACS+ accounting

**Goal.** Show that every configuration change and every privileged command is recorded with its author, on the unit and on a system the administrator cannot change.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000080-NDM-000220` | II | Protect against an administrator falsely denying an action. | Event log filters for configuration changes; Device configuration revision history and revert; Workspace mode (ADOM and policy package locking); and 6 more |
| `SRG-APP-000343-NDM-000289` | II | Audit the execution of privileged functions. | Event log filters for configuration changes; TACACS+ accounting of CLI commands, configuration changes, and logins; CLI option enables JSON API event log for both request and response |
| `SRG-APP-000504-NDM-000321` | II | Audit privileged activities and other system-level access. | Event log filters for configuration changes |
| `SRG-APP-000381-NDM-000305` | II | Audit the enforcement of access restrictions on changes. | Event log filters for configuration changes; Device configuration revision history and revert; ADOM revision history; and 30 more |
| `SRG-APP-000101-NDM-000231` | II | Record the full text of privileged commands. | TACACS+ accounting of CLI commands, configuration changes, and logins |

**Uses.** `fmg-203`, `fgt-202`, `tacacs-201`, and `admin-201`.

**Configure.**

1. Record configuration changes of every kind in the event log.

   ```text
   config system locallog disk filter
       set event enable
       set devcfg enable
       set dm enable
       set dvm enable
       set objcfg enable
       set scply enable
       set system enable
   end
   ```

2. Keep the revision history of each device, and let no ordinary profile revert or delete a revision.

   ```text
   config system dm
       set max-revs <NUMBER>
   end
   config system admin profile
       edit lab-readonly
           set config-revert none
           set device-revision-deletion none
   end
   ```

3. Send the full text of CLI commands, the configuration changes, and the logons to the TACACS+ server. Chapter 01 documents that the event log records configuration changes, and that the full command text comes from TACACS+ accounting.

   ```text
   config system locallog tacacs+accounting setting
       set status enable
       set tacacs-name tacacs-201
   end
   config system locallog tacacs+accounting filter
       set cli-cmd-audit enable
       set config-change-audit enable
       set login-audit enable
   end
   ```

**Positive test.** Change an object, change a policy, and install to `fgt-202`. The event log has a record for each, with the administrator. The revision history of `fgt-202` has a new revision with its author. Enter three CLI commands: `tacacs-201` has an accounting record with the full text of each.

**Negative test.** An administrator with `lab-readonly` tries to revert and to delete a revision: both are refused, and the refusals are recorded. Stop `tacacs-201` and enter a CLI command: the event log still records the change, and the full command text is missing on the server. Record that as the reason the server must be available.

**Evidence.** The filter, the `dm`, and the accounting settings from `show full-configuration`, the event log records, the revision history of `fgt-202`, and the accounting records on `tacacs-201`.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), and start `tacacs-201` again.

### Lab 2.10 — Protecting and storing audit records: access, capacity, and alerts

**Goal.** Show that only an auditor's role can reach the event log, that the log has a defined size and lifetime, and that the unit alerts when the log fills.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000119-NDM-000236` | II | Protect audit information from unauthorized modification. | Event log access restriction |
| `SRG-APP-000120-NDM-000237` | II | Protect audit information from unauthorized deletion. | Event log access restriction |
| `SRG-APP-000121-NDM-000238` | II | Protect audit tools from unauthorized access. | Event log access restriction |
| `SRG-APP-000357-NDM-000293` | II | Allocate audit record storage to meet the organization's requirements. | Event log storage and disk-full alerting; Time-base retention is configurable for the task monitor and event log |
| `SRG-APP-000360-NDM-000295` | II | Alert in real time on audit failure events. | Event log storage and disk-full alerting; Alert email (SMTP) |
| `SRG-APP-000795-NDM-000130` | II | Alert the defined roles when audit information is accessed, modified, or deleted without authorization. | Alert email (SMTP) |

**Uses.** `fmg-203`, `mail-202`, and `admin-201`.

**Configure.**

1. Keep the system settings, which hold the event log, away from every profile except the auditors' and the security administrators'.

   ```text
   config system admin profile
       edit lab-readonly
           set system-setting none
   end
   ```

2. Give the event log a quota, an alert level of 75 percent, and a lifetime.

   ```text
   config system locallog disk setting
       set log-disk-quota <MB>
       set log-disk-full-percentage 75
       set log-max-days <DAYS>
   end
   config system locallog setting
       set log-interval-disk-full <MINUTES>
   end
   ```

3. Send alerts by email.

   ```text
   config system mail
       edit mail-202
           set server 10.200.2.120
           set secure-option starttls
           set auth enable
   end
   ```

**Positive test.** With a small quota, cause event log records until the log passes 75 percent: an alert email arrives on `mail-202`. An administrator with an auditor's profile opens the event log.

**Negative test.** An administrator with `lab-readonly` cannot open the event log and cannot clear it or change its settings. While the log is below the level, no alert is sent. Chapter 01 maps the alert on unauthorized access to audit information to this email alert and names no separate setting, so record what the unit sends when the refused attempt above occurs.

**Evidence.** The profile, the `locallog`, and the `mail` settings from `show full-configuration`, the alert email with its time and the level of the log at that time, and the refused actions.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

### Lab 2.11 — Off-loading the event log: syslog and FortiAnalyzer

**Goal.** Show that the unit's own event log reaches a central log server over TCP with TLS, and a FortiAnalyzer if the lab has one.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000515-NDM-000325` | II | Off-load audit records to a different system or media. | Sending FortiManager event logs to a syslog server; Sending FortiManager event logs to FortiAnalyzer; TACACS+ accounting of CLI commands, configuration changes, and logins; and 1 more |
| `SRG-APP-000516-NDM-000350` | I | Send log data to at least one central log server (two for boundary devices). | Sending FortiManager event logs to a syslog server; Sending FortiManager event logs to FortiAnalyzer; Add TLS-SSL support for local log SYSLOG forwarding; and 1 more |

**Uses.** `fmg-203`, `syslog-201a`, `syslog-201b`, and `admin-201`. The FortiAnalyzer step also needs `faz-202` of Volume CCII, which is optional here.

**Configure.**

1. Send the event log to `syslog-201a`.

   ```text
   config system syslog
       edit syslog-201a
           set ip 10.200.2.20
           set reliable enable
           set secure-connection enable
   end
   config system locallog syslogd setting
       set status enable
       set syslog-name syslog-201a
       set severity information
   end
   ```

2. Add `syslog-201b` (`10.200.2.21`) under `config system syslog` in the same way. Chapter 01 gives one `syslogd` setting. Type `config system locallog ?` to see whether your release has a second one. If it has, point it at `syslog-201b`. If it has not, record that the unit sends its own log to one syslog server.
3. If the lab has `faz-202`, send the event log to it in real time as well, and authorize `fmg-203` on it as a log source.

   ```text
   config system locallog fortianalyzer setting
       set status realtime
       set server 10.200.2.100
       set secure-connection enable
       set reliable enable
   end
   ```

**Positive test.** Log on and log off: the records appear on `syslog-201a` within seconds, received over TLS on TCP, with `fmg-203` as their source. With `faz-202`, the same records appear in its Log View.

**Negative test.** Give `syslog-201a` a certificate that `fmg-203` does not trust: the unit sends nothing, and a capture on `syslog-201a` shows no record from `fmg-203` in clear text or over UDP.

**Evidence.** The `syslog` and `locallog` settings from `show full-configuration`, one record on `fmg-203` and the same record on `syslog-201a` with both times, and the capture.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), and give `syslog-201a` its own certificate back.

### Lab 2.12 — Time: authenticated NTP and time stamps

**Goal.** Show that `fmg-203` takes authenticated time from the lab's NTP servers, keeps comparing its clock with them, and stamps its records with a time that maps to UTC.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000920-NDM-000320` | II | Synchronize system clocks within and between systems. | NTP server |
| `SRG-APP-000925-NDM-000330` | II | Compare the internal clock with an authoritative time source at a defined frequency. | NTP server |
| `SRG-APP-000395-NDM-000347` | II | Authenticate NTP sources cryptographically. | NTP server; FortiManager supports NTPv4 with SHA-256 encryption |
| `SRG-APP-000116-NDM-000234` | II | Use the internal system clock for the time stamps of audit records. | NTP server |
| `SRG-APP-000374-NDM-000299` | II | Record time stamps that map to UTC. | NTP server |

**Uses.** `fmg-203`, `ntp-201a`, and `ntp-201b`.

**Configure.**

1. Use `ntp-201a` with authentication. `set key-type sha256` belongs to a feature that Chapter 01 lists as 8.0.0 and later. On release 7.6, type `set key-type ?`, use the strongest type the release offers, and record that SHA-256 needs 8.0.0.

   ```text
   config system ntp
       set status enable
       config ntpserver
           edit 1
               set server 10.200.2.30
               set authentication enable
               set key-type sha256
               set key-id <ID>
               set key <KEY>
           end
   end
   ```

2. Add `ntp-201b` (`10.200.2.31`) as server 2 in the same way.

**Positive test.** The time that `get system status` shows on `fmg-203` is within one second of `ntp-201a`. Set the clock of `fmg-203` a few minutes off by hand: the unit corrects it from the server. An event log record written afterward carries a time that maps to UTC.

**Negative test.** Change the key on `fmg-203` to a wrong value: the unit no longer takes time from that server. Record how the unit shows it. Stop `ntp-201a`: the unit keeps time from `ntp-201b`.

**Evidence.** The NTP settings from `show full-configuration`, the time comparisons, one event log record with its time, and the key type the release offered.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), and start `ntp-201a` again.

### Lab 2.13 — Cryptography: strong ciphers, SNMPv3, and FIPS-CC mode

**Goal.** Show that management sessions use only strong protocols and ciphers, so that no password crosses the network in clear text, that SNMP is authenticated and encrypted, and that the unit can run in FIPS-CC mode.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000172-NDM-000259` | I | Transmit only encrypted representations of passwords. | HTTPS and SSH management encryption |
| `SRG-APP-000411-NDM-000330` | I | Protect the integrity of nonlocal maintenance sessions with a FIPS-validated HMAC. | HTTPS and SSH management encryption; FIPS-CC mode; FortiGate-to-FortiManager (FGFM) management tunnel; and 1 more |
| `SRG-APP-000412-NDM-000331` | I | Protect the confidentiality of remote maintenance sessions with FIPS-approved algorithms. | HTTPS and SSH management encryption; FIPS-CC mode; FortiGate-to-FortiManager (FGFM) management tunnel; and 6 more |
| `SRG-APP-000179-NDM-000265` | I | Use FIPS 140-2 approved algorithms for authentication to a cryptographic module. | HTTPS and SSH management encryption; FIPS-CC mode; SAML SSO supports SHA-256 and SHA-512 for both IdP and SP |
| `SRG-APP-000395-NDM-000310` | II | Authenticate SNMP messages with a FIPS-validated HMAC. | SNMPv3; Support higher authentication and encryption for SNMP v3 |

**Uses.** `fmg-203` with its hypervisor console, `nms-201`, and `admin-201`.

**Configure.**

1. Allow only TLS 1.2 and strong ciphers for HTTPS and SSH.

   ```text
   config system global
       set global-ssl-protocol tlsv1.2
       set ssl-low-encryption disable
       set enc-algorithm high
       set ssh-enc-algo aes256-ctr aes256-gcm@openssh.com
       set ssh-mac-algo hmac-sha2-256 hmac-sha2-512
   end
   ```

2. Create an SNMPv3 user with SHA-2 authentication and AES privacy, for queries and notifications from `nms-201`. Chapter 01 lists these stronger choices as 7.6.0 and later.

   ```text
   config system snmp user
       edit <SNMP_USER>
           set security-level auth-priv
           set auth-proto sha256
           set priv-proto aes256
           set notify-hosts 10.200.2.40
           set queries enable
   end
   ```

3. Enable FIPS-CC mode last, from the console, after you have taken a snapshot. Chapter 01 records that the mode can be enabled only there.

   ```text
   config system fips
       set status enable
   end
   ```

**Positive test.** From `admin-201`, an HTTPS session with TLS 1.2 and a strong cipher succeeds, and an SSH session with a current client succeeds. From `nms-201`, an SNMPv3 query with the user, SHA-256 authentication, and AES-256 privacy is answered. After step 3, the unit reports that FIPS-CC mode is enabled.

**Negative test.** From `admin-201`, try TLS 1.0 and TLS 1.1 against port 443, a low-strength cipher, and an SSH client limited to an old cipher, for example with `openssl s_client` and the options of your SSH client: the unit refuses each. A capture of a logon shows no password in clear text. From `nms-201`, a query with an SNMPv2c community, and one with a wrong authentication key, get no answer.

**Evidence.** The settings from `show full-configuration`, the transcripts of the accepted and the refused handshakes, the SNMP queries, the capture, and the status output that shows FIPS-CC mode.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4). After FIPS-CC mode this is required, not optional.

### Lab 2.14 — Change control for managed devices: device authorization, the FGFM tunnel, workspace, and workflow

**Goal.** Show that only an authorized device can be managed, that only an authorized administrator can change and install its configuration, and that a change is locked, approved, and recorded.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000380-NDM-000304` | II | Enforce access restrictions on changes to the device configuration. | Administrator profiles (role-based access); Administrative domains (ADOMs); Device registration and authorization; and 165 more |
| `SRG-APP-000516-NDM-000335` | II | Enforce access restrictions on changes to the system components. | FortiGate-to-FortiManager (FGFM) management tunnel; Device registration and authorization; More secure request authorization with OAuth protocol; and 4 more |

**Uses.** `fmg-203`, `fgt-202`, `mail-202`, and `admin-201`, with two administrators: one who makes a change and one who approves it.

**Configure.**

1. Protect the tunnel to the managed devices, and refuse a device that was not added first.

   ```text
   config system global
       set fgfm-ssl-protocol tlsv1.2
       set fgfm-cert-exclusive enable
       set fgfm-deny-unknown enable
   end
   config system admin setting
       set allow_register disable
       set unreg_dev_opt add_no_service
   end
   ```

2. Separate who may edit from who may install. This profile can read the policy packages and cannot install them.

   ```text
   config system admin profile
       edit lab-editor
           set adom-policy-packages read
           set deploy-management none
   end
   ```

3. Lock what an administrator changes, with workspace mode.

   ```text
   config system global
       set workspace-mode normal
   end
   ```

4. For approval of changes, give the ADOM a workflow approval matrix with an approver and the mail server.

   ```text
   config system workflow approval-matrix
       edit lab-203
           set mail-server mail-202
           config approver
               edit 1
                   set member <APPROVERS>
               end
   end
   ```

**Positive test.** The first administrator locks the ADOM, changes a policy, and submits the change. The approver receives the notification on `mail-202` and approves. The change is installed to `fgt-202`, and the event log and the revision history name both administrators.

**Negative test.** A FortiGate that was not added in Device Manager tries to register: `fmg-203` refuses it. An administrator with `lab-editor` tries to install: refused. A second administrator tries to change the locked ADOM: refused. A change that the approver rejects is not installed.

**Evidence.** The `global`, `admin setting`, profile, and approval matrix settings from `show full-configuration`, the refused registration, the refused install and change, the approval email, and the revision history of `fgt-202`.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), and put `fgt-202` back to its baseline.

### Lab 2.15 — Configuration backup: scheduled, on demand, and encrypted

**Goal.** Show that the configuration is backed up to another system on a schedule and after a change, and that the backup is encrypted.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000516-NDM-000340` | II | Back up system-level information when changes occur. | Scheduled configuration backup; On-demand configuration backup; Device configuration revision history and revert; and 12 more |
| `SRG-APP-000516-NDM-000341` | II | Back up the system documentation when changes occur. | Scheduled configuration backup |

**Uses.** `fmg-203`, `files-201`, and `admin-201`.

**Configure.**

1. Schedule an encrypted backup to `files-201`.

   ```text
   config system backup all-settings
       set status enable
       set protocol sftp
       set server 10.200.2.60
       set user <USER>
       set passwd <PASSWORD>
       set crptpasswd <ENCRYPTION_PASSWORD>
       set week_days <DAYS>
       set time <HH:MM:SS>
   end
   ```

2. The SRG asks for a backup when changes occur. After a change, run the backup at once.

   ```text
   execute backup all-settings sftp 10.200.2.60 <FILE> <USER> <PASSWORD>
   ```

3. Keep the documents that describe the unit, such as the security plan and this lab's notes, with the backup files. No setting covers that part of the requirement.

**Positive test.** Change a setting and run the backup: a dated file appears on `files-201`. At the scheduled time, a second, encrypted file appears.

**Negative test.** Run the backup with a wrong password: it fails, and the unit reports the failure. Open the scheduled backup file without the encryption password: its content cannot be read.

**Evidence.** The `backup` settings from `show full-configuration`, the list of backup files on `files-201` with their dates, the failed backup, and the place where the documents are kept.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), and delete the test backup files from `files-201`.

### Lab 2.16 — Software: supported release, security updates, and signed firmware

**Goal.** Show that `fmg-203` runs a release the vendor supports, that updates are installed within 30 days by a recorded procedure, that only a privileged administrator can install, and that the unit installs only a valid image.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-001035-NDM-000340` | I | Run hardware and software that the vendor supports. | FortiManager firmware upgrade; FortiManager introduces OS firmware levels Feature(F) and Mature(M); FortiManager firmware upgrade enhancements |
| `SRG-APP-000457-NDM-000352` | II | Install security-relevant firmware updates within 30 days. | FortiManager firmware upgrade; FortiManager setup wizard improvement with optional firmware upgrade step; FortiManager introduces OS firmware levels Feature(F) and Mature(M); and 1 more |
| `SRG-APP-000131-NDM-000243` | II | Install only patches and components with a verified digital signature. | FortiManager firmware upgrade |
| `SRG-APP-000133-NDM-000244` | II | Limit the privilege to change the software on the unit. | FortiManager firmware upgrade |
| `SRG-APP-000378-NDM-000302` | II | Prohibit software installation without explicit privileged status. | FortiManager firmware upgrade |

**Uses.** `fmg-203`, `files-201`, and `admin-201`.

**Configure.**

1. Record the release with `get system status`, and compare it with the vendor's list of supported releases. In the GUI under Firmware Management, choose a Mature (M) release where possible. Check the support contract with `diagnose fmupdate dbcontract` and `diagnose license list`.
2. Keep a patch record: for each security update, the date the vendor released it and the date you installed it. The requirement is met by this record, not by a setting.
3. To install a release, take the snapshot and a configuration backup first. Download the image from the vendor with your own account, put it on `files-201`, and load it.

   ```text
   execute backup all-settings sftp 10.200.2.60 <FILE> <USER> <PASSWORD>
   execute restore image sftp <IMAGE_PATH> 10.200.2.60 <USER> <PASSWORD>
   ```

**Positive test.** The release of `fmg-203` is on the vendor's list of supported releases, and the patch record shows each security update installed within 30 days. If you run step 3 as a privileged administrator, the unit installs the vendor's image and starts on the new release.

**Negative test.** An administrator with the `lab-readonly` profile of Lab 2.1 cannot upgrade the unit. Change one byte of a copy of the image and try to load the copy: the unit refuses it. If the unit accepts an altered image, record that as a finding.

**Evidence.** The output of `get system status` and of the two `diagnose` commands, the vendor's list with its date, the patch record, the refused upgrade, and the refused image.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4), unless the upgrade is meant to stay. In that case take a new baseline.

### Lab 2.17 — Gaps: passwords checked against a list of compromised passwords

**Goal.** Confirm that FortiManager has no setting that checks a new password against a list of commonly used or compromised passwords, apply the compensating control, and record the disposition.

| SRG ID | CAT | Requirement | Features in Chapter 01 |
| --- | --- | --- | --- |
| `SRG-APP-000845-NDM-000220` | II | Check new passwords against a list of commonly used, expected, or compromised passwords. | — |

**Uses.** `fmg-203`, `radius-201a`, and `admin-201`.

**Configure.**

1. Confirm that no such setting exists. In the CLI, enter each of these contexts and type `set ?`, and search the output for an option that names a password list or a dictionary. Keep the output.

   ```text
   config system password-policy
       set ?
   end
   config system admin setting
       set ?
   end
   ```

2. Apply the compensating control that Chapter 01 names: meet the requirement on the authentication server. Make every administrator a RADIUS account, as in Lab 2.5, and let the directory behind `radius-201a` refuse listed passwords.
3. The one local account of last resort has no such check. Give it a long random password that a password manager generates, and record how it is stored.

**Positive test.** The `set ?` output shows no option for a password list. A RADIUS administrator whose password is changed to a listed password on the directory side is refused there, so the listed password never reaches `fmg-203`.

**Negative test.** Set a commonly used password of 15 characters that meets the policy of Lab 2.4 on a local test account: `fmg-203` accepts it. That is the gap, and it is the reason local accounts are limited to the account of last resort.

**Evidence.** The `set ?` output of the two contexts, the refusal on the directory side, the accepted common password on the local test account, and the disposition: an open finding with the compensating control.

**Return to baseline.** Restore the `baseline-203` snapshot of `fmg-203` (Lab 999.4).

## Lab Verification

Complete this sign-off once Labs 2.1 to 2.17 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from Chapter 01 and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the 79 Network Device Management SRG requirements of FortiManager in seventeen labs, on a FortiManager-VM that runs release 7.6. Sixteen labs configure a setting and test it both ways. Lab 2.17 documents the one requirement the unit cannot meet: it has no check of new passwords against a list of compromised passwords. The labs also record the requirements that the unit meets only in part or by procedure: a password change of four characters, a revocation list that is imported by hand, the full text of commands only through TACACS+ accounting, one local account kept by review, and NTP authentication with SHA-256, which needs 8.0.0.

- [ ] Has run each requirement lab and its negative test.
- [ ] Has recorded the gap evidence and the compensating control for each gap lab.
- [ ] Has stored the evidence for each lab.
