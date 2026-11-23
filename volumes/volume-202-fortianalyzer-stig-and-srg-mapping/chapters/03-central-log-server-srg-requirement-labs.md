# Chapter 03: Central Log Server SRG Requirement Labs

## Learning Objectives

- Prove each Central Log Server SRG requirement that this volume's tables cite on the Chapter 999 lab, with a positive and a negative test.
- Give each administrator an account, a role, and an ADOM, and limit management to the admin network.
- Set the logon, password, and certificate rules, and read the log server's own audit records.
- Receive logs from a FortiGate and a syslog source over TLS, and protect, retain, forward, and back up the stored logs.
- Alert on full storage and silent devices, and use the analysis and report tools the SRG lists.
- Record what FortiAnalyzer 7.6 cannot meet, and the compensating control for each.
- Store the evidence for each lab so it can support an assessment.

## Theory and Architecture

The Central Log Server SRG covers a system that receives, stores, analyzes, and reports on the log records of other devices. FortiAnalyzer is that system for a Fortinet estate, and it has no STIG, so it is assessed against this SRG. The SRG has two kinds of requirement. About half are about the log server's own management plane: who may log on, how, and what the server records about itself. The rest are about its job: receiving records without loss or change, keeping them for the right time, sending them on, alerting when something stops, and letting authorized people search and report.

The labs follow that order. Labs 3.1 to 3.7 secure the unit itself: access, logon behavior, passwords, certificates, its own audit records, cryptography, and time. Labs 3.8 to 3.11 follow a log record through the server: it arrives, it is stored and protected, it is kept for the retention period, and it is forwarded and backed up. Labs 3.12 and 3.13 use the records: alerts, correlation, search, and reports. Lab 3.14 covers the software release. Lab 3.15 documents the two requirements that the lab unit cannot meet.

All labs run on the network from [Chapter 999](999-shared-lab-infrastructure.md).

### Requirements and labs

This volume's tables cite 60 distinct Central Log Server SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 3.1 | 5 | Requirement lab: Administrator access control: roles, ADOMs, individual accounts, trusted hosts, and services |
| 3.2 | 4 | Requirement lab: Logon protections: lockout, banner, and session timeout |
| 3.3 | 4 | Requirement lab: Password policy: length, character classes, change distance, and lifetime |
| 3.4 | 5 | Requirement lab: Certificates and multifactor authentication: PKI administrators, trust anchors, and revocation |
| 3.5 | 3 | Requirement lab: The log server's own audit records: accounts, logons, and event types |
| 3.6 | 2 | Requirement lab: Cryptography and key protection: FIPS-CC mode, strong ciphers, and private data encryption |
| 3.7 | 3 | Requirement lab: Time: authenticated NTP and receipt time stamps |
| 3.8 | 5 | Requirement lab: Receiving logs: authorized sources, TLS, TCP, source identity, and record attributes |
| 3.9 | 5 | Requirement lab: Protecting stored logs: integrity, reading, modification, deletion, and the analysis tools |
| 3.10 | 3 | Requirement lab: Retention and storage: data policy, automatic deletion, and the 75 percent alert |
| 3.11 | 4 | Requirement lab: Off-loading and backup: log forwarding, weekly backup, and aggregation |
| 3.12 | 4 | Requirement lab: Alerting: silent devices, attacks on several devices, event severity, and incidents |
| 3.13 | 8 | Requirement lab: Analysis and reporting: correlation, FortiView, Log View, audit reduction, and reports |
| 3.14 | 3 | Requirement lab: Software: supported release, security updates, and signed firmware |
| 3.15 | 2 | Gap lab: Gaps: account inactivity, and SHA-2 signatures for SAML on release 7.6 |

A **requirement lab** configures the FortiAnalyzer setting, proves it with a positive test, and proves the control with a negative test. A **gap lab** covers requirements that FortiAnalyzer cannot meet: it proves that the setting is absent, applies the nearest compensating control, and records the disposition.

## Design Considerations

- **The lab unit runs FortiAnalyzer 7.6.** Chapter 01 checked its commands against the FortiAnalyzer 8.0.0 CLI Reference. Two rows of this chapter need 8.0.0: NTP authentication with SHA-256 (Lab 3.7) and SHA-2 signatures for SAML (Lab 3.15). If release 7.6 rejects any other option, type `set ?` in that context, use what the release offers, and record the difference as a finding.
- **Use a throwaway account for lockout and password tests.** A lockout test can lock the account you are logged on with. Run it against a local test account, and keep the console of `faz-202` open.
- **Prove the record, not only the setting.** For the audit, alert, and forwarding requirements the evidence is a record: the event log line, the alert email on `mail-202`, or the forwarded record on `syslog-201a`.
- **Test with real log sources.** A receiving or alerting lab needs logs that arrive. `fgt-202` sends FortiGate logs, and `admin-201` sends syslog over TLS.
- **Run the FIPS-CC step last.** FIPS-CC mode can be enabled only from the console and changes how the unit works, so take the snapshot first and restore the baseline afterward.
- **Some requirements are procedures.** Running a supported release and installing updates within 30 days are shown by a record of dates, not by a setting.
- **Say what a lab CA cannot prove.** `ca-201` proves the certificate mechanics but not DoD trust, so the CAC and DoD PKI requirements keep a procedural check.

## Implementation and Automation

Each lab lists its commands in the order to enter them. Commands come from [Chapter 01](01-fortianalyzer-feature-version-and-srg-map.md), with the lab's values from Chapter 999 substituted.
The placeholders are `<LAB_ADMIN>` for a RADIUS-authenticated administrator, `<SECRET>`, `<KEY>`, and `<PASSWORD>` for values you generate for the run, `<PORT>` for the management port of `faz-202`, and `<DEVICE>` for the name that `fgt-202` has in Device Manager. Addresses are those of Chapter 999. A step that names a GUI pane has no CLI command in Chapter 01.

Save the evidence for each lab in `evidence/<lab>/<date>/`, as Chapter 999 describes.

## Validation and Troubleshooting

Before each lab, confirm the baseline: `get system status` on `faz-202` shows the release, `diagnose dvm device list` shows `fgt-202` as authorized, and `faz-202` answers a ping from `admin-201`. After each lab, restore the baseline and repeat the checks.

| Symptom | Cause | Fix |
| --- | --- | --- |
| A command is rejected | The option belongs to a later release than 7.6 | Type `set ?` in that context, use what the release offers, and record the difference |
| The RADIUS administrator cannot log on | `faz-202` is not a client of `radius-201a`, the secret differs, or the server does not accept RADIUS over TLS | Check the client entry and the secret on `radius-201a`, and the protocol under `config system admin radius` |
| No logs arrive from `fgt-202` | The device is not authorized, or it sends without encryption | Authorize it in Device Manager and check `diagnose dvm device list` |
| No syslog arrives from `admin-201` | The sender uses UDP or plain TCP, or its certificate is not from `ca-201` | Send over TLS to port 6514 with a certificate that `ca-201` issued |
| No alert email arrives | `mail-202` is unreachable, or the account or the STARTTLS setting is wrong | Check `config system mail` and the mail log on `mail-202` |
| You are locked out after a lockout or trusted-host test | The test hit your own account or address | Use the console of `faz-202`, or restore the baseline |

## Security and Best Practices

- Run every test inside the lab network, and never point a negative test at a production FortiAnalyzer.
- Generate fresh secrets, keys, and passwords for each run, write them as `<SECRET>` in the evidence, and delete them in the cleanup.
- Keep the console of `faz-202` open while you test lockout, trusted hosts, and FIPS-CC mode.
- Record the release and the build of `faz-202` with every result, because behavior differs between releases.
- Treat a negative test that fails to refuse as a finding, not as a lab error.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortianalyzer-feature-version-and-srg-map.md) and [Chapter 02](02-fortianalyzer-and-cisco-stig-crosswalk.md) for the rows these labs prove.
- [Chapter 999](999-shared-lab-infrastructure.md) for the lab network, hosts, and baseline.
- DISA Central Log Server SRG V3R5, from the October 2026 STIG Library Compilation. Confirm the current release on the DoD Cyber Exchange.
- Fortinet, *FortiAnalyzer 8.0.0 CLI Reference* and the *FortiAnalyzer New Features Guides* for 7.0 to 8.0, which Chapter 01 used, and the *FortiAnalyzer Administration Guide* of your release for the GUI steps.
- [Volume CLXXII, Chapter 03](../../volume-172-disa-srgs-and-stigs/chapters/03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md) for assessing a product that has no STIG.

**Knowledge checks:**

1. Why does a lockout lab need a throwaway account and an open console?
2. Which two settings together keep an administrator from reading logs outside their ADOM?
3. Why does a log source have to be authorized before the unit stores its logs?
4. Why is a forwarded record on `syslog-201a` better evidence of off-loading than the forwarding configuration?
5. Which two requirements can the lab unit not meet, and what is the compensating control for each?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 and its baseline. The `baseline-202` snapshot of `faz-202`, `fgt-202`, and `mail-202`. The hypervisor console of `faz-202`. A local test account, a RADIUS administrator, and an SSH client and a browser on `admin-201`. **Cost:** none beyond the Chapter 999 lab. A firmware image is needed only if you choose to run the upgrade in Lab 3.14.

### Lab 3.1 — Administrator access control: roles, ADOMs, individual accounts, trusted hosts, and services

**Goal.** Show that each administrator has an account of their own with a role and an ADOM, that management is reachable only from the admin network over HTTPS and SSH, and that unused modules are off.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000033-AU-001610` | I | Enforce approved authorizations (roles) for access to the log server and its data. | Equivalent requirement | Device registration and authorization; Administrative domains (ADOMs); Administrator profiles (role-based access); and 12 more |
| `SRG-APP-000148-AU-002270` | I | Uniquely identify and authenticate every user. | No Cisco STIG counterpart | Individual administrator accounts; RADIUS administrator authentication; TACACS+ administrator authentication; and 6 more |
| `SRG-APP-000815-AU-000260` | II | Authenticate users individually before access to shared accounts. | No Cisco STIG counterpart | Individual administrator accounts; SAML SSO wildcard admin user to match all users on IdP server |
| `SRG-APP-000516-AU-000410` | II | Analysis and viewing functions meet DoD trusted path and access rules. | No Cisco STIG counterpart | Trusted hosts for administrators; Interface administrative access; Local-in policies; and 2 more |
| `SRG-APP-000141-AU-000090` | II | Disable non-essential capabilities. | No Cisco STIG counterpart | Interface administrative access; High availability (HA); Disable unused analytics modules; and 87 more |

**Uses.** `faz-202`, `admin-201`, and `radius-201a`. For the negative test, a lab host outside the admin network, for example `nms-201`.

**Configure.**

1. Enable ADOMs and create a read-only profile. Create the ADOM `lab-202` in the GUI, because Chapter 01 has no command for it.

   ```text
   config system global
       set adom-status enable
   end
   config system admin profile
       edit lab-readonly
           set log-viewer read
           set report-viewer read
           set system-setting none
   end
   ```

2. Point the unit at the RADIUS server, and give each person an account of their own with a profile and an ADOM. `set protocol tls` needs RADIUS over TLS on `radius-201a` (Chapter 999).

   ```text
   config system admin radius
       edit radius-201a
           set server 10.200.2.10
           set secret <SECRET>
           set protocol tls
           set message-authenticator require
   end
   config system admin user
       edit <LAB_ADMIN>
           set user_type radius
           set radius_server radius-201a
           set profileid lab-readonly
           set adom lab-202
   end
   ```

3. Limit where the administrator may connect from, and what reaches the management port.

   ```text
   config system admin user
       edit <LAB_ADMIN>
           set trusthost1 10.200.3.0 255.255.255.0
   end
   config system local-in-policy
       edit 1
           set intf <PORT>
           set src 10.200.3.0 255.255.255.0
           set dport 443
           set action accept
   end
   ```

4. Allow only HTTPS and SSH on the management port, and turn off the modules the lab does not use.

   ```text
   config system interface
       edit <PORT>
           set allowaccess https ssh
   end
   config system global
       set disable-module <MODULES>
   end
   ```

**Positive test.** From `admin-201`, `<LAB_ADMIN>` logs on over HTTPS and over SSH. The administrator sees only the ADOM `lab-202`, can read its logs and reports, and cannot open the system settings.

**Negative test.** From `nms-201`, HTTPS and SSH to `faz-202` are refused, because the address is outside the trusted host. From `admin-201`, HTTP and Telnet are refused, because the port does not allow them. A logon with a name that has no account of its own is refused. `<LAB_ADMIN>` cannot change a system setting or see another ADOM.

**Evidence.** The profile, the administrator account, the interface, and the local-in policy from `show full-configuration`, the refused connections from `nms-201`, and the event log lines for the allowed and the refused logons.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4).

### Lab 3.2 — Logon protections: lockout, banner, and session timeout

**Goal.** Show that repeated failures lock an account, that the DoD notice is shown before logon, and that idle sessions end.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000065-AU-000240` | II | Limit logons to three consecutive failures in 15 minutes. | Equivalent requirement | Administrator lockout |
| `SRG-APP-000345-AU-000400` | II | Keep an account locked until an administrator releases it after three failures in 15 minutes. | No Cisco STIG counterpart | — |
| `SRG-APP-000068-AU-000035` | III | Show the DoD Notice and Consent Banner before logon. | Equivalent requirement | Pre-login banner |
| `SRG-APP-000295-AU-000190` | II | End user sessions after organization-defined conditions. | No Cisco STIG counterpart | Idle session timeout |

**Uses.** `faz-202` and `admin-201`. Use a local test account, so that a lockout does not block the RADIUS administrator.

**Configure.**

1. Lock an account after three failed logons. The SRG also asks that the account stay locked until an administrator releases it. `admin-lockout-duration` unlocks after a set time, so Chapter 01 says to set a long duration and to document the release procedure.

   ```text
   config system global
       set admin-lockout-threshold 3
       set admin-lockout-duration <SECONDS>
   end
   ```

2. Show the DoD Notice and Consent Banner before logon. Use the approved text from your authorizing official.

   ```text
   config system global
       set pre-login-banner enable
       set pre-login-banner-message <DOD_BANNER>
   end
   ```

3. End idle sessions.

   ```text
   config system admin setting
       set idle_timeout <MINUTES>
   end
   ```

**Positive test.** Open an SSH session and the GUI logon page from `admin-201`: the banner appears before the password prompt. Leave a session idle for the time you set: the unit ends it.

**Negative test.** Fail three logons for the test account: the fourth attempt, even with the right password, is refused. Read the lockout in the event log. The account stays refused for the duration you set. Record that the unit releases it by time and not by an administrator's action, which is the difference from `SRG-APP-000345-AU-000400` that Chapter 01 documents.

**Evidence.** The banner in the SSH client transcript and on the GUI logon page, the lockout lines of the event log with their times, the idle-timeout disconnect, and the written release procedure.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4).

### Lab 3.3 — Password policy: length, character classes, change distance, and lifetime

**Goal.** Show that the unit refuses passwords that are too short or too simple, and that the policy sets a lifetime of 180 days.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000164-AU-002480` | II | Require passwords of at least 15 characters. | Equivalent requirement | Password policy |
| `SRG-APP-000166-AU-002490` | III | Require at least one uppercase character in passwords. | Equivalent requirement | Password policy |
| `SRG-APP-000170-AU-002530` | III | Require at least eight changed characters when a password changes. | Equivalent requirement | Password policy |
| `SRG-APP-000174-AU-002570` | III | Limit password lifetime to 180 days. | No Cisco STIG counterpart | Password policy |

**Uses.** `faz-202` and `admin-201`, with a local test account.

**Configure.**

1. Turn on the password policy.

   ```text
   config system password-policy
       set status enable
       set minimum-length 15
       set must-contain upper-case-letter lower-case-letter number non-alphanumeric
       set change-4-characters enable
       set expire 180
   end
   ```

2. Note the limit that Chapter 01 documents. `change-4-characters` requires four changed characters, and `SRG-APP-000170-AU-002530` requires eight. Chapter 01 says to use remote authentication, so that the authentication server enforces the rule.

**Positive test.** Give the test account a password of 15 characters with an uppercase letter, a lowercase letter, a number, and a special character: the unit accepts it.

**Negative test.** Try a password of 14 characters, then one with no uppercase letter, then one that changes fewer than four characters of the old password: the unit refuses each. Then try one that changes four to seven characters: the unit accepts it, although the SRG asks for eight. Record that as the finding.

**Evidence.** The policy from `show full-configuration`, the refusal message for each bad password, the accepted password change that shows the finding, and the `expire 180` value. The lab cannot wait 180 days, so the lifetime is shown by the setting.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4).

### Lab 3.4 — Certificates and multifactor authentication: PKI administrators, trust anchors, and revocation

**Goal.** Show that an administrator logs on with a certificate of the lab PKI, that the unit trusts only the lab CA, and that it refuses a revoked certificate.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000149-AU-002280` | II | Use multifactor authentication for network access to privileged accounts. | Equivalent requirement | PKI (certificate) administrator authentication; Two-factor authentication (FortiToken Cloud) |
| `SRG-APP-000175-AU-002630` | I | Validate PKI certificates to a trust anchor, including revocation status. | No Cisco STIG counterpart | PKI (certificate) administrator authentication; CA certificates and CRLs |
| `SRG-APP-000391-AU-002290` | II | Accept the DoD CAC credential. | No Cisco STIG counterpart | PKI (certificate) administrator authentication |
| `SRG-APP-000427-AU-000040` | II | Trust only DoD PKI certificate authorities for protected sessions. | No Cisco STIG counterpart | PKI (certificate) administrator authentication |
| `SRG-APP-000910-AU-000390` | II | Keep only approved trust anchors in certificate stores. | Equivalent requirement | CA certificates and CRLs |

**Uses.** `faz-202`, `ca-201`, and `admin-201`. `ca-201` stands in for the DoD PKI, and a certificate file on `admin-201` stands in for the CAC.

**Configure.**

1. Install the CA certificate of `ca-201` and its certificate revocation list.

   ```text
   config system certificate ca
       edit lab-ca-201
           set ca <CERTIFICATE>
   end
   config system certificate crl
       edit lab-crl-201
           set http-url <CRL_URL>
   end
   ```

2. Create an administrator that logs on with a certificate, and ask every client for a certificate.

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

3. Read the list under `config system certificate ca` and keep only the trust anchors your organization approves. In the lab that is `lab-ca-201` and the certificates the unit ships with and needs.
4. Chapter 01 also lists FortiToken Cloud as a second factor (`set two-factor-auth ftc-ftm`). It needs a FortiToken Cloud subscription, which this lab does not have, so the lab proves the certificate logon only. On a CAC the PIN unlocks the private key, which makes the logon multifactor. The certificate file of the lab does not prove that part.

**Positive test.** From `admin-201`, open the GUI with the certificate of `<LAB_PKI_ADMIN>`: the logon succeeds, and the event log names the administrator.

**Negative test.** Connect with no certificate: the unit refuses the session. Connect with a certificate that another CA issued, for example a self-signed one: refused. Revoke the administrator's certificate on `ca-201`, publish the list, and wait until the unit has fetched it: the logon is refused.

**Evidence.** The CA, the revocation list, and the administrator from `show full-configuration`, the event log lines for the successful and the refused logons, and the revocation list with the revoked serial number.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4).

### Lab 3.5 — The log server's own audit records: accounts, logons, and event types

**Goal.** Show that the unit records account creation and logons in its own event log, and that each record names the type of event.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000026-AU-000580` | II | Audit the creation of accounts on the log server. | Equivalent requirement | FortiAnalyzer event log (own audit records) |
| `SRG-APP-000095-AU-000680` | III | The log server's own audit records show what type of event occurred. | Equivalent requirement | FortiAnalyzer event log (own audit records); Event log easier to read; Generate system event log when daemon crashes; and 2 more |
| `SRG-APP-000503-AU-000280` | II | Audit successful and unsuccessful logons. | Equivalent requirement | FortiAnalyzer event log (own audit records) |

**Uses.** `faz-202` and `admin-201`.

**Configure.**

1. Turn on the local event log at the information level.

   ```text
   config system locallog disk setting
       set status enable
       set severity information
   end
   ```

**Positive test.** Create a local test account, log on with it, and log off. The event log has a record for the account creation and one each for the logon and the logoff. Each record names the type of event, the administrator, and the time. Fail one logon with a wrong password: the event log records the failed attempt too.

**Negative test.** Set the status of the local event log to `disable`, create a second test account, and confirm that no record is written. This shows that the records depend on the setting. Enable the log again.

**Evidence.** The event log records for the account creation, the successful logon, the failed logon, and the logoff, and the setting from `show full-configuration`.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4).

### Lab 3.6 — Cryptography and key protection: FIPS-CC mode, strong ciphers, and private data encryption

**Goal.** Show that management sessions use only strong protocols and ciphers, that stored keys are encrypted, and that the unit can run in FIPS-CC mode.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000514-AU-002890` | I | Use FIPS-validated cryptography for signatures, hashes, and encryption. | No Cisco STIG counterpart | HTTPS and SSH management encryption; FIPS-CC mode |
| `SRG-APP-000915-AU-000400` | II | Protect stored cryptographic keys. | No Cisco STIG counterpart | Private data encryption |

**Uses.** `faz-202` with its hypervisor console, and `admin-201`.

**Configure.**

1. Allow only TLS 1.2 and strong ciphers for management.

   ```text
   config system global
       set global-ssl-protocol tlsv1.2
       set ssl-low-encryption disable
       set enc-algorithm high
   end
   ```

2. Encrypt the private data the unit stores, such as keys and passwords. If the unit asks for an encryption key, generate one for the run and record it as `<SECRET>`.

   ```text
   config system global
       set private-data-encryption enable
   end
   ```

3. Enable FIPS-CC mode last, from the console, after you have taken a snapshot. Chapter 01 records that the mode can be enabled only there.

   ```text
   config system fips
       set status enable
   end
   ```

**Positive test.** From `admin-201`, an HTTPS session with TLS 1.2 and a strong cipher succeeds, and an SSH session with a current client succeeds. After step 3, the unit reports that FIPS-CC mode is enabled.

**Negative test.** From `admin-201`, try TLS 1.0 and TLS 1.1 against port 443, and then a low-strength cipher, for example with `openssl s_client`: the unit refuses each handshake. Try step 3 over SSH instead of the console: the unit does not offer the option.

**Evidence.** The settings from `show full-configuration`, the transcripts of the accepted and the refused handshakes, and the status output that shows FIPS-CC mode.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4). After FIPS-CC mode this is required, not optional.

### Lab 3.7 — Time: authenticated NTP and receipt time stamps

**Goal.** Show that `faz-202` takes authenticated time from the lab's NTP servers, the same sources its log sources use, and that it stamps each record on receipt.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000920-AU-000410` | II | Synchronize system clocks within and between systems. | Equivalent requirement | NTP server; FortiAnalyzer supports NTPv4 with SHA-256 encryption |
| `SRG-APP-000086-AU-000030` | III | Keep log time stamps within one second, using the same NTP source as the devices. | Log-source counterpart only | Log receipt time stamps; NTP server; Time zone settings per ADOMs/Reports |
| `SRG-APP-000374-AU-000290` | III | Time-stamp records on receipt in a form that maps to UTC. | Equivalent requirement | Log receipt time stamps |

**Uses.** `faz-202`, `ntp-201a`, `ntp-201b`, and `fgt-202`.

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
3. Check that `fgt-202` takes its time from the same two servers.

**Positive test.** The time that `get system status` shows on `faz-202` is within one second of `ntp-201a`. A log from `fgt-202` arrives with a receipt time stamp that maps to UTC and is within one second of the time the device gave the record.

**Negative test.** Change the key on `faz-202` to a wrong value: the unit no longer takes time from that server. Record how the unit shows it. Then stop NTP on `fgt-202` and set its clock several minutes off: the device time and the receipt time of its next record differ, which is why both must use the same source. Put both settings back.

**Evidence.** The NTP settings from `show full-configuration`, the two time comparisons, one record with its device time and its receipt time, and the key type the release offered.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` and `fgt-202` (Lab 999.4).

### Lab 3.8 — Receiving logs: authorized sources, TLS, TCP, source identity, and record attributes

**Goal.** Show that `faz-202` accepts logs only from authorized sources, only over TLS on TCP, and that it keeps the source and the fields of each record.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000086-AU-000020` | III | Aggregate log records from the devices and hosts in scope. | Log-source counterpart only | Log collection from Fortinet devices (OFTP); Syslog collection from third-party devices; Model device support for central logging; and 19 more |
| `SRG-APP-000516-AU-000330` | II | Keep the identity of the original source host in each record. | Log-source counterpart only | Log collection from Fortinet devices (OFTP); Device registration and authorization; Model device support for central logging; and 4 more |
| `SRG-APP-000516-AU-000340` | II | Use TCP to receive and transmit log records. | Log-source counterpart only | Log collection from Fortinet devices (OFTP); Syslog collection from third-party devices; Log forwarding to syslog, CEF, or another FortiAnalyzer |
| `SRG-APP-000439-AU-004310` | I | Protect the confidentiality and integrity of transmitted information, including logs. | No Cisco STIG counterpart | Log collection from Fortinet devices (OFTP); Syslog collection from third-party devices; Log forwarding to syslog, CEF, or another FortiAnalyzer; and 7 more |
| `SRG-APP-000089-AU-000400` | II | Keep the DoD-defined attributes of the records the devices send. | Log-source counterpart only | Support parsing and addition of third-party application logs to the SIEM DB; Support parsing and addition of third-party application logs to the SIEM DB in JSON format; FortiAnalyzer supports packet header information for FortiWeb traffic log; and 5 more |

**Uses.** `faz-202`, `fgt-202`, `admin-201` as the syslog source, and `ca-201`.

**Configure.**

1. Use TLS 1.2 and strong ciphers for the logs of Fortinet devices.

   ```text
   config system global
       set oftp-ssl-protocol tlsv1.2
       set enc-algorithm high
   end
   ```

2. Give an unknown device no service until an administrator authorizes it.

   ```text
   config system admin setting
       set unreg_dev_opt add_no_service
   end
   ```

3. Take syslog only over TLS, and only from senders with a certificate.

   ```text
   config system log settings
       set syslog-over-tls-port 6514
       set unencrypted-logging-tcp disable
       set unencrypted-logging-udp disable
       config client-cert-auth
           set mode strict
       end
   end
   ```

4. Authorize `fgt-202` in the GUI under Device Manager, and check it with `diagnose dvm device list`.
5. In the GUI under Log View, give the syslog source a log parser, so that the fields of its records are kept. Chapter 01 lists log parsers as 7.4.0 and later.

**Positive test.** Cause a log on `fgt-202`, for example with a logon: the record appears in Log View with `fgt-202` as its source. From `admin-201`, send a syslog message over TLS to port 6514 with a certificate that `ca-201` issued: the record is stored with `admin-201` as its source and with its fields parsed.

**Negative test.** From `admin-201`, send syslog over UDP port 514 and then over plain TCP: neither message is stored. Send over TLS with no certificate, and then with a certificate of another CA: the unit refuses both. Point a device that is not authorized at `faz-202`: it is listed as unauthorized, and none of its logs is stored.

**Evidence.** The settings from `show full-configuration`, the output of `diagnose dvm device list`, one stored record of each source with its source and fields, and the refused attempts with their times.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` and `fgt-202` (Lab 999.4).

### Lab 3.9 — Protecting stored logs: integrity, reading, modification, deletion, and the analysis tools

**Goal.** Show that stored logs carry an integrity check, that only authorized roles can read them or reach the analysis tools, and that deleting a device does not delete its logs.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000080-AU-000010` | II | Protect received log data from alteration that would break attribution. | No Cisco STIG counterpart | Log file integrity (hash and authentication code); SAML assertions and SAML requests can be now signed to better support third-party IdPs |
| `SRG-APP-000118-AU-000100` | II | Protect stored log data from unauthorized reading. | No Cisco STIG counterpart | Administrative domains (ADOMs); Administrator profiles (role-based access); Data masking for administrators; and 3 more |
| `SRG-APP-000119-AU-000110` | II | Protect stored log data from unauthorized modification. | Equivalent requirement | Log file integrity (hash and authentication code); Administrator profiles (role-based access) |
| `SRG-APP-000120-AU-000120` | II | Protect stored log data from unauthorized deletion. | Equivalent requirement | Keep logs after a device is deleted; Administrator profiles (role-based access) |
| `SRG-APP-000121-AU-000130` | II | Protect the log analysis tools from unauthorized access. | No Cisco STIG counterpart | Administrator profiles (role-based access) |

**Uses.** `faz-202`, `fgt-202`, and `admin-201`.

**Configure.**

1. Record a checksum for each log file. Chapter 01 documents that the checksum is MD5-based, which is not a FIPS-approved hash, so enable it for tamper detection and record the finding.

   ```text
   config system global
       set log-checksum md5-auth
   end
   ```

2. Give the reviewers a profile that can read and cannot change, and a second profile that masks sensitive fields.

   ```text
   config system admin profile
       edit lab-readonly
           set log-viewer read
           set report-viewer read
           set system-setting none
   end
   config system admin profile
       edit lab-masked
           set datamask enable
           set datamask-fields <FIELDS>
   end
   ```

3. Keep the logs of a device after the device is deleted.

   ```text
   config system log settings
       set keep-dev-logs enable
   end
   ```

**Positive test.** After the logs of `fgt-202` have rolled into a file, `execute log-integrity <DEVICE> <VDOM> <LOG_FILE>` reports that the file is intact. An administrator with `lab-readonly` reads the logs and the reports. An administrator with `lab-masked` sees the masked fields hidden.

**Negative test.** An administrator with `lab-readonly` cannot delete logs and cannot change a log setting. An administrator whose profile does not grant the log viewer cannot open Log View, FortiView, or the reports. Delete `fgt-202` from Device Manager: its logs remain. Add the device again. The unit gives an administrator no way to edit a stored log file, so note in the evidence that an altered file was not tested.

**Evidence.** The settings from `show full-configuration`, the output of `execute log-integrity`, the refused actions of each profile, and the logs of `fgt-202` that remain after the device was deleted.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` and `fgt-202` (Lab 999.4).

### Lab 3.10 — Retention and storage: data policy, automatic deletion, and the 75 percent alert

**Goal.** Show that only an appointed role sets what is kept and for how long, that old logs are deleted by policy, and that the unit warns when storage fills.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000090-AU-000070` | III | Only the ISSM, or roles the ISSM appoints, select which events are retained. | Log-source counterpart only | Data policy (log retention by ADOM) |
| `SRG-APP-000095-AU-000050` | III | Configure log retention by criticality, event type, or retention period. | No Cisco STIG counterpart | Data policy (log retention by ADOM); Automatic deletion of logs, reports, and archives; Time-base retention is configurable for the task monitor and event log |
| `SRG-APP-000359-AU-000120` | III | Alert the SA and ISSO when log storage reaches 75 percent. | No Cisco STIG counterpart | Per-ADOM disk quota; Per-device disk quota; Disk-full alerting; and 1 more |

**Uses.** `faz-202`, `fgt-202`, `mail-202`, and `admin-201`.

**Configure.**

1. In the GUI under System Settings, open the data policy of the ADOM `lab-202` and set the Analytics and the Archive retention to the periods your organization defines. For the test, give the ADOM a small disk quota. If the pane of your release offers the level at which the unit alerts, set it to 75 percent. If it does not, record the level the unit uses.
2. Delete old logs automatically.

   ```text
   config system auto-delete
       config log-auto-deletion
           set status enable
           set retention months
           set value <MONTHS>
       end
   end
   ```

3. Send an alert by email when the disk fills.

   ```text
   config system locallog setting
       set log-interval-disk-full <MINUTES>
   end
   config system mail
       edit mail-202
           set server 10.200.2.120
           set secure-option starttls
           set auth enable
   end
   config system alert-event
       edit lab-disk-alert
           config alert-destination
               edit 1
                   set type mail
                   set to <ISSO_EMAIL>
               end
   end
   ```

**Positive test.** Send logs from `fgt-202` until the ADOM passes 75 percent of its quota: an alert email for the SA and the ISSO arrives on `mail-202`, and the event log records the alert. The retention periods you set are shown in the data policy.

**Negative test.** Log on as an administrator with the `lab-readonly` profile of Lab 3.1: the data policy cannot be opened or changed, so only the appointed role selects what is kept. While the ADOM is below the level, no alert is sent.

**Evidence.** The data policy, the `auto-delete`, `locallog`, `mail`, and `alert-event` settings from `show full-configuration`, the alert email with its time, the storage level at that time, and the refused change of the read-only administrator.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202`, `fgt-202`, and `mail-202` (Lab 999.4).

### Lab 3.11 — Off-loading and backup: log forwarding, weekly backup, and aggregation

**Goal.** Show that collected logs are forwarded in real time to a different system over TLS, that they are backed up to another system, and that a second log server aggregates to the first.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000358-AU-000100` | II | Off-load log records to a different system or media. | No Cisco STIG counterpart | Log backup to another system; Log forwarding to syslog, CEF, or another FortiAnalyzer; Sending FortiAnalyzer event logs to a syslog server; and 5 more |
| `SRG-APP-000515-AU-000110` | III | Off-load records in real time (interconnected systems) or weekly (standalone). | Equivalent requirement | Log forwarding to syslog, CEF, or another FortiAnalyzer; Log forwarding enhancement |
| `SRG-APP-000125-AU-000300` | III | Back up the log repository at least weekly to another system. | No Cisco STIG counterpart | Log backup to another system; New API to restore logs; Backup strategy and configuration setup added to the FortiAnalyzer setup wizard |
| `SRG-APP-000086-AU-000390` | II | Where several log servers exist, aggregate them to a central repository. | No Cisco STIG counterpart | Log aggregation (collector to analyzer); Log fetching between FortiAnalyzer units; New management extension - FortiSIEM Collector; and 12 more |

**Uses.** `faz-202`, `fgt-202`, `syslog-201a`, and `files-201`. The aggregation step also needs `faz-202b`, which is optional.

**Configure.**

1. Forward the collected logs to `syslog-201a` in real time, over TCP with TLS.

   ```text
   config system log-forward
       edit 1
           set mode forwarding
           set fwd-server-type syslog
           set server-addr 10.200.2.20
           set fwd-reliable enable
           set fwd-secure enable
           set fwd-max-delay realtime
   end
   ```

2. Back up the logs of the device to `files-201`. The SRG asks for a backup at least weekly. Chapter 01 gives this command and no schedule for it, so run it weekly by procedure and keep the dated files as the record.

   ```text
   execute backup logs <DEVICE> sftp 10.200.2.60 <USER> <PASSWORD> <DIRECTORY>
   ```

3. If the lab has `faz-202b`, make it a collector that aggregates to `faz-202`. On `faz-202b`:

   ```text
   config system global
       set log-mode collector
   end
   config system log-forward
       edit 1
           set mode aggregation
           set server-addr 10.200.2.100
   end
   ```

   On `faz-202`:

   ```text
   config system log-forward-service
       set accept-aggregation enable
   end
   ```

   If the lab has one FortiAnalyzer, the requirement to aggregate several log servers does not apply to it. Record that, and skip this step.

**Positive test.** A log caused on `fgt-202` appears on `syslog-201a` within seconds, received over TLS on TCP. The backup files appear in the directory on `files-201`. With `faz-202b`, logs that it collected appear on `faz-202`.

**Negative test.** A capture on `syslog-201a` shows no log from `faz-202` over UDP or in clear text. Run the backup with a wrong password: it fails, the unit reports the failure, and the earlier backup files remain.

**Evidence.** The forwarding settings from `show full-configuration`, one record on `faz-202` and the same record on `syslog-201a` with both times, the list of backup files on `files-201` with their dates, and the failed backup.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` and `fgt-202` (Lab 999.4), and delete the test backup files from `files-201`.

### Lab 3.12 — Alerting: silent devices, attacks on several devices, event severity, and incidents

**Goal.** Show that the unit alerts when a device stops sending logs, raises an event when the same activity is seen on several devices, gives the event the severity you define, and opens an incident for it.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000360-AU-000130` | III | Alert the SA and ISSO in real time on audit failures, such as devices that stop sending logs. | Equivalent requirement | No-logging detection for devices; Event handlers and alerts; Alert email (SMTP); and 5 more |
| `SRG-APP-000516-AU-000350` | II | Notify the SA and ISSO when an attack is seen on multiple devices. | Log-source counterpart only | Event handlers and alerts; Indicators of compromise (IOC); Event correlation across devices; and 25 more |
| `SRG-APP-000516-AU-000380` | II | Configure the defined severity of each event the devices send. | Log-source counterpart only | Event handlers and alerts; FortiClient event handler update; FortiDeceptor default handler; and 6 more |
| `SRG-APP-000516-AU-000360` | II | Create trouble tickets automatically for defined threats, within seconds. | No Cisco STIG counterpart | Incidents; Attach FortiMail connector actions to incidents; Assign events for alert triage; and 12 more |

**Uses.** `faz-202`, `fgt-202`, `admin-201` as the second log source, and `mail-202`.

**Configure.**

1. Detect a device that stops logging, and use the mail server of Lab 3.10 for the alert.

   ```text
   config system locallog setting
       set no-log-detection-threshold <MINUTES>
       set log-interval-dev-no-logging <MINUTES>
   end
   config system mail
       edit mail-202
           set server 10.200.2.120
           set secure-option starttls
           set auth enable
   end
   ```

2. In the GUI under Incidents & Events, create an event handler that matches a test event from more than one device. Give it the severity your organization defines for that event, and add an email notification to the SA and the ISSO. System alerts use `config system alert-event`, as in Lab 3.10.
3. In the same pane, open an incident for the event. If the handler of your release can create the incident itself, use that, and record the time between the event and the incident.
4. Chapter 01 also lists indicators of compromise for this requirement (`config system log ioc`). The service needs a license, which this lab does not have, so the lab leaves it out and records that.

**Positive test.** Stop the logs of `fgt-202` for longer than the threshold: an alert email arrives on `mail-202`, and the event log records that the device is silent. Cause the test event on `fgt-202` and on `admin-201`: the handler raises one event with the severity you set, the email arrives, and an incident exists for it.

**Negative test.** While `fgt-202` logs normally, no alert about a silent device is sent. An event that does not match the handler raises nothing. Cause the test event on one device only, if your handler requires several: no event is raised.

**Evidence.** The `locallog` and `mail` settings from `show full-configuration`, the handler, the two alert emails with their times, the event with its severity, and the incident with its time.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202`, `fgt-202`, and `mail-202` (Lab 999.4).

### Lab 3.13 — Analysis and reporting: correlation, FortiView, Log View, audit reduction, and reports

**Goal.** Show that authorized users can correlate, search, reduce, and report on the records of several devices in one place.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000111-AU-000150` | III | Analyze log records across multiple devices for review by authorized users. | No Cisco STIG counterpart | FortiView; Event correlation across devices; SIEM correlation and analysis; and 3 more |
| `SRG-APP-000115-AU-000160` | III | Filter log records on demand for events of interest. | No Cisco STIG counterpart | Log View: search and filter; Manage subnets; Filter syntax enhancement; and 2 more |
| `SRG-APP-000516-AU-000370` | II | Aggregate events that show account actions on the devices in scope. | Log-source counterpart only | Event correlation across devices; Central UEBA table for custom reporting and widgets; New charts in the Asset Identity Center; and 6 more |
| `SRG-APP-000745-AU-000120` | II | Review and analyze audit records from many components centrally. | No Cisco STIG counterpart | FortiView; Data sources tuning; Asset and Identity Dashboards; and 19 more |
| `SRG-APP-000750-AU-000130` | II | Provide audit reduction for on-demand review. | No Cisco STIG counterpart | SQL database for analytics |
| `SRG-APP-000770-AU-000170` | II | Generate reports on demand. | No Cisco STIG counterpart | Reports and report templates; FortiDeceptor report; Central UEBA table for custom reporting and widgets; and 39 more |
| `SRG-APP-000775-AU-000180` | II | Generate reports for after-the-fact incident investigations. | No Cisco STIG counterpart | Reports and report templates; Incidents; IPS signature lookup; and 13 more |
| `SRG-APP-000790-AU-000210` | II | Process, sort, and search records by defined audit fields. | No Cisco STIG counterpart | Log View: search and filter; Filter syntax enhancement; Search by object names; and 3 more |

**Uses.** `faz-202` with the logs of `fgt-202` and `admin-201`, and `admin-201` as the reviewer's workstation.

**Configure.**

1. Use the local SQL database for analytics.

   ```text
   config system sql
       set status local
   end
   ```

2. The other steps are in the GUI, because Chapter 01 names a pane for them and no command:

   - **Log View:** filter the records by device, user, and time, and sort them by a field.
   - **FortiView:** open a view that shows the records of both log sources together.
   - **Incidents & Events, Handlers:** add a correlation rule that matches an account action, such as an administrator logon, on both log sources.
   - **Reports:** run a report on demand, and run one for the incident of Lab 3.12.

**Positive test.** In Log View, a filter by device, user, and time returns the matching records, and a sort by a field orders them. FortiView shows both sources in one view. The correlation rule raises one event for the account action on both sources. A report runs on demand, and the report for the incident lists the records behind it.

**Negative test.** A filter for an event that did not happen returns nothing. An administrator of another ADOM sees none of these records. An administrator whose profile does not grant the report viewer cannot run a report.

**Evidence.** The `sql` setting from `show full-configuration`, the filtered and sorted Log View, the FortiView view, the correlated event, and the two reports.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` and `fgt-202` (Lab 999.4).

### Lab 3.14 — Software: supported release, security updates, and signed firmware

**Goal.** Show that `faz-202` runs a release the vendor supports, that updates are installed within 30 days by a recorded procedure, and that the unit installs only a valid firmware image.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-001035-AU-000430` | I | Run a release the vendor supports. | Equivalent requirement | Firmware upgrade; Prevent FortiAnalyzers with an expired support contract from upgrading to a major or minor firmware release; FortiAnalyzer introduces OS firmware levels Feature(F) and Mature(M) |
| `SRG-APP-000456-AU-000270` | I | Install security-relevant updates within 30 days. | No Cisco STIG counterpart | Firmware upgrade; FortiAnalyzer HA graceful upgrade; Check for new MEA versions using CLI; and 4 more |
| `SRG-APP-000810-AU-000250` | II | Install only software and firmware with a verified, approved signature. | No Cisco STIG counterpart | Firmware upgrade |

**Uses.** `faz-202`, `files-201`, and `admin-201`.

**Configure.**

1. Record the release with `get system status`, and compare it with the vendor's list of supported releases. Check the support contract with `diagnose fmupdate dbcontract` and `diagnose license list`.
2. Keep a patch record: for each security update, the date the vendor released it and the date you installed it. The requirement is met by this record, not by a setting.
3. To install a release, take the snapshot and a configuration backup first. Download the image from the vendor with your own account, put it on `files-201`, and load it.

   ```text
   execute backup all-settings sftp 10.200.2.60 <FILE> <USER> <PASSWORD>
   execute restore image sftp <IMAGE_PATH> 10.200.2.60 <USER> <PASSWORD>
   ```

**Positive test.** The release of `faz-202` is on the vendor's list of supported releases, and the patch record shows each security update installed within 30 days. If you run step 3, the unit installs the vendor's image and starts on the new release.

**Negative test.** Change one byte of a copy of the image and try to load the copy: the unit refuses it. If the unit accepts an altered image, record that as a finding. A release that is no longer on the vendor's list is a finding, whatever the settings are.

**Evidence.** The output of `get system status` and of the two `diagnose` commands, the vendor's list with its date, the patch record, and the refused image.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4), unless the upgrade is meant to stay. In that case take a new baseline.

### Lab 3.15 — Gaps: account inactivity, and SHA-2 signatures for SAML on release 7.6

**Goal.** Confirm that FortiAnalyzer 7.6 has no setting that disables an account after 35 days of inactivity and no SHA-2 choice for SAML signatures, apply the nearest compensating control for each, and record the disposition.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000163-AU-002470` | II | Disable accounts after 35 days of inactivity. | No Cisco STIG counterpart | — |
| `SRG-APP-000610-AU-000050` | I | Use SHA-2 or stronger for digital signatures. | No Cisco STIG counterpart | SAML SSO supports SHA-256 and SHA-512 for both IdP and SP |

**Uses.** `faz-202`, `radius-201a`, and `admin-201`.

**Configure.**

1. Confirm that no setting disables an inactive account. In the CLI, enter each of these contexts and type `set ?`, and search the output for an inactivity option. Keep the output.

   ```text
   config system admin setting
       set ?
   end
   config system password-policy
       set ?
   end
   config system admin user
       edit <LAB_ADMIN>
           set ?
   end
   ```

2. Apply the compensating control that Chapter 01 names: let the authentication server disable inactive accounts. Make every administrator a RADIUS account, as in Lab 3.1, and keep one local account for emergencies. Review the local account by a documented procedure.
3. Confirm that release 7.6 has no SHA-2 choice for SAML signatures. Chapter 01 lists the four options `digest-method`, `signature-algorithm`, `idp-digest-method`, and `idp-signature-algorithm` as 8.0.0 and later. Type `set ?` in the context and keep the output.

   ```text
   config system saml
       set ?
   end
   ```

4. Apply the compensating control: do not configure SAML single sign-on on this release, and authenticate administrators with certificates (Lab 3.4) or RADIUS (Lab 3.1). The requirement is met when the unit runs 8.0.0 or later.

**Positive test.** The `set ?` output shows no inactivity option and none of the four SAML signature options. An administrator who is disabled on `radius-201a` can no longer log on to `faz-202`, which is how the inactivity rule is enforced.

**Negative test.** The unit never disables the local emergency account, however long it is idle. The lab cannot wait 35 days, so record this from the absence of the setting. If one of the four SAML options does appear on your release, the gap is closed for it: configure the option as Chapter 01 gives it, and say so in the evidence.

**Evidence.** The `set ?` output of the four contexts, the refused logon of the disabled RADIUS administrator, the review procedure for the local account, and the two dispositions: an open finding with a compensating control for inactivity, and an open finding until release 8.0.0 for SAML signatures.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4).

## Lab Verification

Complete this sign-off once Labs 3.1 to 3.15 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from Chapter 01 and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the 60 Central Log Server SRG requirements of FortiAnalyzer in fifteen labs, on a FortiAnalyzer-VM that runs release 7.6. Fourteen labs configure a setting and test it both ways. Lab 3.15 documents the two requirements the lab unit cannot meet: it has no setting that disables an inactive account, and release 7.6 has no SHA-2 choice for SAML signatures. The labs also record four requirements that the unit meets only in part: a lockout that ends by time, a password change of four characters, a log checksum that is MD5-based, and NTP authentication with SHA-256, which needs 8.0.0.

- [ ] Has run each requirement lab and its negative test.
- [ ] Has recorded the gap evidence and the compensating control for each gap lab.
- [ ] Has stored the evidence for each lab.
