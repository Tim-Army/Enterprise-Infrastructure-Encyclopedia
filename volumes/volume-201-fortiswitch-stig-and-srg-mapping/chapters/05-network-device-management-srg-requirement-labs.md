# Chapter 05: Network Device Management SRG Requirement Labs

## Learning Objectives

- Prove each Network Device Management (NDM) SRG requirement in the crosswalk on the Chapter 999 lab, with a positive and a negative test.
- Configure administrator roles, trusted hosts, lockout, banner, session timeout, and password policy on FortiSwitchOS.
- Produce and forward the audit records the SRG lists, with accurate time and two central log servers.
- Apply FIPS-CC mode, strong ciphers, and SNMPv3 with SHA-2 and AES.
- Use two authentication servers, enroll a certificate, back up the configuration automatically, and check firmware integrity.
- Store the evidence for each lab so it can support an assessment.

## Theory and Architecture

The Network Device Management SRG covers how an administrator reaches, authenticates to, and is held accountable on a network device: access control, logon behavior, passwords, audit records, time, cryptography, and software integrity. It applies to any network device, whatever its forwarding role, so it is the largest SRG family in the crosswalk: 48 requirements. Chapters 01 and 02 map each one to a FortiSwitch setting. This chapter proves them.

The labs follow the lifecycle of an administrator session. Lab 5.1 decides who may connect and with what privilege. Lab 5.2 limits what a connection can do before and after logon. Lab 5.3 sets the password rules. Labs 5.4 to 5.6 produce, time-stamp, store, and off-load the audit records. Lab 5.7 secures the channel. Lab 5.8 moves authentication and certificates to central services. Lab 5.9 keeps the configuration backed up and the software supportable.

All labs run on the network from [Chapter 999](999-shared-lab-infrastructure.md): the management SVI on segment 30, the admin host on segment 20, and the services on segment 10.

### Requirements and labs

The crosswalk lists 48 distinct Network Device Management SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 5.1 | 8 | Requirement lab: Administrator access control: roles, trusted hosts, services, and the local account |
| 5.2 | 3 | Requirement lab: Logon protections: lockout, banner, and session timeout |
| 5.3 | 7 | Requirement lab: Password policy: length, character classes, change distance, and hashing |
| 5.4 | 10 | Requirement lab: Audit events: accounts, privileged commands, and logons |
| 5.5 | 6 | Requirement lab: Audit record content and time: time stamps, source, and clock |
| 5.6 | 4 | Requirement lab: Audit storage, failure alerts, and off-load to two log servers |
| 5.7 | 4 | Requirement lab: Cryptography and remote maintenance: FIPS mode, strong ciphers, and SNMPv3 |
| 5.8 | 2 | Requirement lab: Authentication servers and public key certificates |
| 5.9 | 4 | Requirement lab: Configuration backup, supported releases, and firmware integrity |

Every requirement here has a FortiSwitch setting or a procedure behind it, so this chapter has requirement labs only. Each lab configures the setting, proves it with a positive test, and proves the control with a negative test.

## Design Considerations

- **Use a throwaway account for lockout and password tests.** A lockout test can lock out the account you are logged in with, so run it against a local test account and keep the RADIUS administrator and a console session available.
- **Prove the record, not only the setting.** For the audit requirements the evidence is a log line with the user, action, and time, read on the switch and on the log server.
- **Both log servers matter.** The requirement is for two central servers, so each logging lab checks that records reach both, and that one failing does not stop the other.
- **FIPS-CC mode changes the unit.** It restricts algorithms and can reset the configuration, so take a backup first and run that lab last.
- **Say what a lab CA cannot prove.** The lab certificate authority proves enrollment mechanics but not DoD trust, so the DoD certificate requirement keeps a procedural check.
- **Some requirements are procedures.** Running a supported release, and applying security updates within the time the SRG sets, are shown by a record of dates, not a setting.

## Implementation and Automation

Each lab lists its commands in the order to enter them. Commands come from the crosswalk workbook (FortiSwitchOS 7.6.7 syntax) with the lab's values substituted: server addresses from Chapter 999, VLAN 30 for management, and `<LAB_ADMIN>` for a RADIUS-authenticated administrator. Where the workbook's command differs from the lab's setup (for example UDP syslog in the workbook against TLS in the lab), the lab says which to use.

Save evidence in `evidence/<lab>/<date>/` on `admin-201`, as Chapter 999 describes. For every audit lab, copy the log line from both the switch and a log server.

## Validation and Troubleshooting

Before each lab, confirm the baseline: login through RADIUS, `get system ntp`, and a test log line on both log servers. After each lab, restore the baseline.

| Symptom | Cause | Fix |
| --- | --- | --- |
| A lockout test locks the only administrator | The test used a production account | Use a local test account; clear the lock from the console |
| No log lines for an action | The event category is not enabled, or the log server is unreachable | Check `config log eventfilter` and the syslog path |
| NTP shows the server but never synchronizes | The key ID or key differs | Match them on server and switch |
| A password change is refused unexpectedly | A policy setting applies to a different scope than you expect | Check `apply-to` in the password policy |
| A FIPS-mode switch lost its configuration | The mode change resets the unit | Restore the backup after the change |

## Security and Best Practices

- Keep the console session open while you test lockout, trusted hosts, and FIPS mode.
- Use lab-only secrets and passwords, and delete them after the run.
- Never put the real DoD notice text or real credentials in a screenshot or log you share.
- Record the model and release with every result, because FIPS-CC and logging features differ by model.
- Treat a negative test that fails to deny as a finding.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortiswitch-feature-version-and-srg-map.md) and [Chapter 02](02-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md) for the rows these labs prove.
- [Chapter 999](999-shared-lab-infrastructure.md) for the lab network and baseline.
- Network Device Management SRG (DISA, V5R5 as compared with a third-party mirror; confirm against DISA's own file).
- FortiSwitchOS 7.6.7 CLI Reference and Administration Guide (Fortinet Document Library).
- [Volume CLXXII, Chapter 07](../../volume-172-disa-srgs-and-stigs/chapters/07-network-device-stigs-management-routing-and-filtering.md) for network device STIGs.

**Knowledge checks:**

1. Why do the audit labs read the log on the switch and on the log server?
2. What is the difference between a lockout threshold and a lockout duration?
3. Why should a lockout test not use the account you are logged in with?
4. What can a lab certificate authority prove about the DoD certificate requirement, and what can it not?
5. Which NDM requirements are shown by procedure and not by a setting?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 (Labs 999.1 to 999.6) and the `baseline-201` snapshot. A console connection to each switch. A local test account, a RADIUS administrator, and an SSH client on `admin-201`. **Cost:** none beyond the Chapter 999 lab. A firmware image is needed only for the upgrade check in Lab 5.9.

### Lab 5.1 — Administrator access control: roles, trusted hosts, services, and the local account

**Goal.** Show that only authorized administrators reach management from approved networks over approved protocols, with the least privilege their role needs, and that one local account remains for emergencies.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000001-NDM-000200` | II | Limit concurrent management sessions to an organization-defined number | Partial | FortiSwitchOS 7.6.7 CLI Reference p233 |
| `SRG-APP-000033-NDM-000212` | I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. | feature row (no Cisco rule) | FortiOS 7.6.7 CLI Reference p1268; FortiSwitchOS 7.6.7 CLI Reference p193 |
| `SRG-APP-000038-NDM-000213` | II | Allow management access only from authorized networks and over approved protocols | Same requirement | FortiSwitch 7.6.7 Feature Matrix p2; FortiSwitchOS 7.6.7 CLI Reference p198 |
| `SRG-APP-000133-NDM-000244` | II | Limit who can change the installed software | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p196 |
| `SRG-APP-000119-NDM-000236` | II | Protect audit information from unauthorized modification | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p196 |
| `SRG-APP-000120-NDM-000237` | II | Protect audit information from unauthorized deletion | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p196 |
| `SRG-APP-000142-NDM-000245` | I | Disable unnecessary and nonsecure functions and services | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p193; FortiSwitchOS 7.6.7 CLI Reference p269 |
| `SRG-APP-000148-NDM-000346` | II | Keep only one local account, as the account of last resort | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p233 |

**Uses.** `sw-648f-1`, `admin-201` on segment 20 and a second host on segment 40, `radius-201a` (P1, P10). Workbook prerequisites: P1, P10 (P1 Reachable RADIUS or TACACS+ servers; P10 A management interface with an address: the management port or a management SVI on a dedicated VLAN).

**Configure.**

1. Restrict management to SSH and HTTPS on the management SVI, and stop nonsecure services.

   ```text
   config system interface
       edit <MGMT>
           set allowaccess https ssh
   end
   config system global
       set admin-ssh-v1 disable
   end
   ```

2. Allow administrators in only from the admin network, and block concurrent logins from two addresses.

   ```text
   config system admin
       edit <ADMIN>
           set trusthost1 10.201.20.0 <MASK>
   end
   config system interface
       edit mgmt-svi
           set allowaccess https ssh
   end
   ```

3. Block two simultaneous logins of the same administrator name.

   ```text
   config system global
       set admin-concurrent enable
   end
   ```

4. Create a read-only profile for log access and a profile that cannot change software.

   ```text
   config system accprofile
       edit <PROFILE>
           set mntgrp none
           set sysgrp read
   end
   ```

5. Make the log group read-only for the audit role so it cannot change or delete logs.

   ```text
   config system accprofile
       edit <PROFILE>
           set loggrp read
   end
   ```

6. Keep only one local account for emergencies; everyone else uses RADIUS.

   ```text
   config system global
       set admin-restrict-local enable
   end
   ```

7. Assign the roles: bind `<LAB_ADMIN>` to a profile through `set accprofile`, and a second RADIUS user to the read-only profile. The roles requirement (`SRG-APP-000033-NDM-000212`) is also met through the profile assignments; in managed mode the FortiGate's administrator profiles apply the same way.

**Positive test.** Log in over SSH from `admin-201` as `<LAB_ADMIN>`: the session opens. The read-only user can run `get` and `show` but a `config` change is refused. A second login with the same name from another address is refused.

**Negative test.** From the segment 40 host, try SSH, HTTPS, and Telnet to `10.201.30.11`: all are refused. Log in as the read-only user and try to delete a log or install an image: the switch denies it. Try to log in as `admin` from a host not on the trusted list.

**Evidence.** The `config system admin`, `accprofile`, and interface `allowaccess` output, the refused-login lines in the syslog, and the denied commands.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.2 — Logon protections: lockout, banner, and session timeout

**Goal.** Show that repeated failures lock an account, the DoD notice is shown before logon, and idle sessions end.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000065-NDM-000214` | II | Lock an account for 15 minutes after three failed logons | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p233 |
| `SRG-APP-000068-NDM-000215` | II | Show the DoD Notice and Consent Banner before logon | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p232-233 |
| `SRG-APP-000190-NDM-000267` | I | End management sessions after five minutes of inactivity | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p234 |

**Uses.** `sw-648f-1`, `admin-201`. Use a local test account so a lockout does not block the RADIUS administrator.

**Configure.**

1. Lock an account for 15 minutes after three failed logons.

   ```text
   config system global
       set admin-lockout-threshold 3
       set admin-lockout-duration 900
   end
   ```

2. Set the DoD Notice and Consent Banner shown before logon (use the approved text from your authorizing official).

   ```text
   config system global
       set pre-login-banner "<DOD_NOTICE_AND_CONSENT_BANNER_TEXT>"
   end
   ```

3. End idle management sessions after five minutes.

   ```text
   config system global
       set admintimeout 5
   end
   ```

**Positive test.** Open an SSH session: the banner appears before the password prompt. Leave a session idle for five minutes: the switch ends it.

**Negative test.** Fail three logons for the test account: the fourth attempt, even with the right password, is refused for 15 minutes. Check the lockout in the log. Wait out the timer, or clear it from the console, and confirm the account works again.

**Evidence.** The banner in the SSH client transcript, the lockout log lines with times, and the idle-timeout disconnect.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.3 — Password policy: length, character classes, change distance, and hashing

**Goal.** Show that the switch rejects weak administrator passwords and stores only hashed ones.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000164-NDM-000252` | II | Require passwords of at least 15 characters | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p262 |
| `SRG-APP-000166-NDM-000254` | II | Require at least one uppercase character in passwords | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p262 |
| `SRG-APP-000167-NDM-000255` | II | Require at least one lowercase character in passwords | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p262 |
| `SRG-APP-000168-NDM-000256` | II | Require at least one numeric character in passwords | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p262 |
| `SRG-APP-000169-NDM-000257` | II | Require at least one special character in passwords | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p262 |
| `SRG-APP-000170-NDM-000329` | II | Change at least eight character positions when a password changes | Partial | FortiSwitchOS 7.6.7 CLI Reference p262 |
| `SRG-APP-000171-NDM-000258` | I | Store only cryptographic representations (hashes) of passwords | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p233 |

**Uses.** `sw-648f-1` with a local test account.

**Configure.**

1. Require at least 15 characters.

   ```text
   config system password-policy
       set status enable
       set apply-to admin-password
       set minimum-length 15
   end
   ```

2. Require upper case, lower case, a number, and a special character.

   ```text
   config system password-policy
       set status enable
       set min-upper-case-letter 1
   end
   ```

3. Require that a password change alters several characters.

   ```text
   config system password-policy
       set status enable
       set change-4-characters enable
   end
   ```

4. Store passwords as strong hashes.

   ```text
   config system global
       set admin-password-hash pbkdf2-high
   end
   ```

5. Add the remaining character-class settings from the same `config system password-policy` block: `set min-lower-case-letter 1`, `set min-number 1`, `set min-non-alphanumeric 1`.

**Positive test.** Set a 15-character password with all four classes: it is accepted. Change it to a password that differs by at least eight characters: accepted. `show full-configuration system admin` shows a hash, not the clear password.

**Negative test.** Try to set a short password, one with no upper-case letter, one with no digit, and one with no special character: each is refused with a message naming the rule. Try a change that alters only one character: refused.

**Evidence.** The password-policy configuration, each refusal message, and the stored hash form in the configuration.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.4 — Audit events: accounts, privileged commands, and logons

**Goal.** Show that the switch records account creation, modification, disabling, enabling, and removal, privileged commands, administrator activity, privilege removal, and successful and failed logons.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000026-NDM-000208` | II | Audit the creation of accounts | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000027-NDM-000209` | II | Audit the modification of accounts | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000028-NDM-000210` | II | Audit the disabling of accounts | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000029-NDM-000211` | II | Audit the removal of accounts | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000319-NDM-000283` | II | Audit the enabling of accounts | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000080-NDM-000220` | II | Audit all administrator activity | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000101-NDM-000231` | II | Log the full text of privileged commands | Partial | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000499-NDM-000319` | II | Log the deletion of administrator privileges | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000503-NDM-000320` | II | Log successful and unsuccessful logons | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |
| `SRG-APP-000504-NDM-000321` | II | Log privileged activities | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p24 |

**Uses.** `sw-648f-1`, `syslog-201a`, `admin-201`.

**Configure.**

1. Turn on system and user event logging.

   ```text
   config log eventfilter
       set event enable
       set system enable
       set user enable
   end
   ```

2. Forward the events to `syslog-201a` (Lab 999.4).

**Positive test.** Create an account, change its profile, disable it, enable it, and delete it. Run a privileged `config` command. Log in successfully and unsuccessfully. Each action produces a log line with the user name, the action, and the time, both in `execute log display` and in `/var/log/lab201/sw-648f-1.log`.

**Negative test.** Turn event logging off for the system category and repeat one action: no log line is written, which proves the setting is what produces the record. Turn it back on. Note that the command text of a privileged command may not be logged in full; record that result for `SRG-APP-000101-NDM-000231`.

**Evidence.** One log line for each of the ten actions, with the timestamp and user, copied from both the switch and the log server.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.5 — Audit record content and time: time stamps, source, and clock

**Goal.** Show that audit records carry an accurate time and the device name, and that the clock follows two authenticated sources.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000096-NDM-000226` | II | Record the date and time of each audited event | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p234, 261 |
| `SRG-APP-000097-NDM-000227` | II | Record where each audited event occurred | Partial | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-APP-000374-NDM-000299` | II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p261 |
| `SRG-APP-000925-NDM-000330` | II | Synchronize the clock with two redundant authoritative time sources | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p261 |
| `SRG-APP-000395-NDM-000347` | II | Authenticate NTP sources cryptographically | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p261 |
| `SRG-APP-000920-NDM-000320` | II | The network device must be configured to synchronize system clocks within and between systems or system components. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p164; FortiSwitchOS 7.6.7 CLI Reference p261 |

**Uses.** `sw-648f-1`, `ntp-201a`, `ntp-201b` (P5), `syslog-201a`. Workbook prerequisites: P5 (P5 Authoritative NTP servers and their authentication keys).

**Configure.**

1. Set the time zone and enable NTP.

   ```text
   config system global
       set timezone <TIMEZONE_NUMBER>
   end
   config system ntp
       set ntpsync enable
   end
   ```

2. Use two NTP servers with authentication.

   ```text
   config system ntp
       set ntpsync enable
       set authentication enable
       config ntpserver
           edit 1
               set server <NTP_IP>
               set authentication enable
               set key-id <ID>
               set key <KEY>
       end
   end
   ```

3. Set the device name so records identify where the event happened.

   ```text
   config system global
       set hostname <HOSTNAME>
   end
   config switch acl ingress
       edit <ID>
           config action
               set count enable
           end
   end
   ```

4. Optionally enable the precision time protocol, if the model supports it.

   ```text
   config switch ptp settings
       set status enable
   end
   ```

**Positive test.** `get system ntp` shows both servers synchronized. A log line carries the host name `sw-648f-1` and a time within a second of `admin-201`.

**Negative test.** Stop `ntp-201a`: the switch falls back to `ntp-201b`. Change the key on the server: the switch reports the authentication failure and stops trusting that server. Set the switch clock wrong by hand and show NTP correcting it.

**Evidence.** `get system ntp` before and after each change and a log line showing the host name and time.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.6 — Audit storage, failure alerts, and off-load to two log servers

**Goal.** Show that local storage is sized, a full or failing log raises an alert, and records go to two central servers.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000357-NDM-000293` | II | Allocate local audit record storage as the organization requires | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p23 |
| `SRG-APP-000360-NDM-000295` | II | Alert on audit failures | Partial | FortiSwitchOS 7.6.7 CLI Reference p23 |
| `SRG-APP-000515-NDM-000325` | II | The network device must off-load audit records onto a different system or media than the system being audited. | feature row (no Cisco rule) | FortiOS 7.6.7 CLI Reference p1337; FortiSwitchOS 7.6.7 CLI Reference p29 |
| `SRG-APP-000516-NDM-000350` | I | Send logs to at least two central log servers | Same requirement | FortiOS 7.6.7 CLI Reference p1337; FortiSwitchOS 7.6.7 CLI Reference p115 |

**Uses.** `sw-648f-1`, `syslog-201a`, `syslog-201b` (P4), a model with a log disk (check the Model Support sheet). Workbook prerequisites: P4, P9 (P4 Central syslog servers that accept reliable; P9 A switch model series that supports the feature).

**Configure.**

1. Set the local log storage and its warning thresholds.

   ```text
   config log disk setting
       set status enable
       set diskfull overwrite
       set full-first-warning-threshold 75
   end
   ```

2. Set the warning percentages for audit failure.

   ```text
   config log disk setting
       set full-first-warning-threshold <PERCENT>
       set full-second-warning-threshold <PERCENT>
       set full-final-warning-threshold <PERCENT>
   end
   ```

3. Send logs to both servers over TLS. The workbook command uses UDP; use reliable mode with encryption as in Lab 999.4.

   ```text
   config log syslogd setting
       set status enable
       set server 10.201.10.20
       set mode udp
       set enc-algorithm high
   end
   config log syslogd2 setting
       set status enable
       set server <SYSLOG_SERVER_2>
       set mode reliable
       set enc-algorithm high
   end
   ```

4. In managed mode, configure the FortiGate to collect the switch logs.

   ```text
   FortiGate: config switch-controller remote-log
   edit <NAME>
       set status enable
       set server <SYSLOG_IP>
   end
   ```

**Positive test.** A configuration change appears on both log servers within seconds. `show log disk setting` shows the thresholds.

**Negative test.** Stop `rsyslog` on `syslog-201a`: the switch still delivers to `syslog-201b` and logs the failed connection. Fill the local log to the warning level: an alert line is written.

**Evidence.** Log lines on both servers, the disk settings, and the alert line.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.7 — Cryptography and remote maintenance: FIPS mode, strong ciphers, and SNMPv3

**Goal.** Show that management sessions use encrypted, integrity-protected channels and approved algorithms, and that SNMP uses SHA-2 and AES.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000411-NDM-000330` | I | Protect remote maintenance sessions with a FIPS-validated HMAC | Same requirement | FortiSwitch 7.6.7 Feature Matrix p2; FortiSwitchOS 7.6.7 CLI Reference p269 |
| `SRG-APP-000412-NDM-000331` | I | Encrypt remote maintenance sessions | Same requirement | FortiSwitch 7.6.7 Feature Matrix p2; FortiSwitchOS 7.6.7 CLI Reference p145 |
| `SRG-APP-000179-NDM-000265` | I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p269 |
| `SRG-APP-000395-NDM-000310` | II | Authenticate SNMP messages with a FIPS-validated HMAC | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p126; FortiSwitchOS 7.6.7 CLI Reference p277 |

**Uses.** `sw-2048f-1` (FIPS-CC support depends on the model and image; check the Model Support sheet), `nms-201` (P6), `admin-201`. Workbook prerequisites: P6, P9 (P6 SNMPv3 manager configured with the same user; P9 A switch model series that supports the feature).

Enabling FIPS-CC mode resets the unit and restricts it to approved algorithms. Take a backup first, expect the configuration to be wiped on some releases, and run this lab last.

**Configure.**

1. Enable the FIPS-CC (or the lower-restriction) mode and strong cryptography.

   ```text
   config system security
       set mode fips-cc
   end
   config system global
       set strong-crypto enable
   end
   ```

2. Create an SNMPv3 user with SHA-2 and AES.

   ```text
   config system snmp user
       edit <USER>
           set security-level auth-priv
           set auth-proto sha256
           set auth-pwd <AUTH_PASSWORD>
   end
   ```

3. Use the approved mode for cryptographic authentication.

   ```text
   config system security
       set mode lince
   end
   ```

**Positive test.** `ssh -vv` from `admin-201` shows an approved cipher and MAC. `snmpwalk -v3 -l authPriv -u lab-snmp -a SHA-256 -A <SECRET> -x AES-256 -X <SECRET> 10.201.30.12 1.3.6.1.2.1.1` returns the system group.

**Negative test.** Connect with an old cipher (`ssh -c 3des-cbc`) or MAC (`-m hmac-md5`): the switch refuses. Query with SNMPv2c or with MD5 authentication: the switch refuses.

**Evidence.** The SSH negotiation output, the refused connections, and the SNMP query results.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.8 — Authentication servers and public key certificates

**Goal.** Show that administrators authenticate to two servers with failover, and that the switch enrolls a certificate from a certificate authority.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000516-NDM-000336` | I | Use at least two authentication servers for administrator logons | Same requirement | FortiSwitch 7.6.7 Feature Matrix p2; FortiSwitchOS 7.6.7 CLI Reference p289 |
| `SRG-APP-000516-NDM-000344` | II | Obtain public key certificates from an approved (DoD) certificate authority | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p215 |

**Uses.** `sw-648f-1`, `radius-201a`, `radius-201b` (P1, P2), `ca-201` (P3) as a stand-in for the DoD CA. Workbook prerequisites: P1, P2, P3 (P1 Reachable RADIUS or TACACS+ servers; P2 User group that lists the authentication servers; P3 PKI: the DoD CA certificate on the switch).

**Configure.**

1. Define two RADIUS servers and the group.

   ```text
   config user radius
       edit radius-201a
           set server 10.201.10.10
           set secret <KEY_1>
       next
       edit radius-201b
           set server 10.201.10.11
           set secret <KEY_2>
   end
   config user group
       edit <ADMIN_GROUP>
           set member radius-201a radius-201b
   end
   config system admin
       edit <ADMIN>
           set remote-auth enable
           set remote-group <ADMIN_GROUP>
           set wildcard enable
   end
   ```

2. Enroll a local certificate from the CA's SCEP service.

   ```text
   config system certificate local
       edit <CERT_NAME>
           set scep-url <DOD_CA_SCEP_URL>
   end
   ```

**Positive test.** Log in as a RADIUS administrator. `get system certificate local` lists the enrolled certificate issued by `ca-201`.

**Negative test.** Stop FreeRADIUS on `svc-201a`: the login still works through `radius-201b`. Stop both: only the local emergency account works. Point the enrollment at a URL with no CA: it fails and no certificate is installed. Note that `ca-201` cannot prove DoD trust; the DoD CA requirement stays a procedural check.

**Evidence.** Both servers' log lines, the failover test, and the certificate details.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 5.9 — Configuration backup, supported releases, and firmware integrity

**Goal.** Show that a configuration change triggers an off-box backup, that the running release is still supported by the vendor, and that firmware is checked before and after an upgrade.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000516-NDM-000340` | II | Back up the configuration whenever it changes | Same requirement | FortiOS 7.6.7 CLI Reference p1268; FortiSwitchOS 7.6.7 CLI Reference p210 |
| `SRG-APP-001035-NDM-000340` | I | Run a software release the vendor still supports | By procedure | FortiSwitch 7.6.7 Feature Matrix p1; FortiSwitchOS 7.6.7 CLI Reference p535 |
| `SRG-APP-000457-NDM-000352` | II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). | feature row (no Cisco rule) | FortiSwitch 7.6.7 Feature Matrix p1; FortiSwitchOS-7.6.7-Administration_Guide—Standalone_Mode.pdf p60 |
| `SRG-APP-000131-NDM-000243` | II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p233; FortiSwitchOS 7.6.7 CLI Reference p389 |

**Uses.** `sw-648f-1`, `files-201` (P15, P16), the Fortinet support site, and a firmware image for an upgrade test. Workbook prerequisites: P15 (P15 An SFTP server and account for configuration backups).

**Configure.**

1. Create a stitch that backs up the configuration on every change.

   ```text
   config system automation-trigger
       edit <TRIGGER>
           set trigger-type event-based
           set event-type config-change
   end
   config system automation-action
       edit <ACTION>
           set action-type cli-script
           set script "execute backup config sftp <FILE> <SFTP_SERVER> <USER> <PASSWORD>"
   end
   config system automation-stitch
       edit <STITCH>
           set trigger <TRIGGER>
           set action <ACTION>
   end
   config system global
       set revision-backup-on-logout enable
   end
   ```

2. Record the release and compare it with the vendor's support dates (by procedure).

   ```text
   get system status
   ```

3. Check the firmware information before and after an upgrade.

   ```text
   diagnose sys firmware info
   ```

4. Plan security updates: read the release notes and record the date you applied each security-relevant release. In managed mode the FortiGate performs the upgrade (`SRG-APP-000457-NDM-000352`); in standalone mode use `execute restore image` from `files-201`.

**Positive test.** Change any setting: within a minute a new configuration file appears on `files-201`. `get system status` shows the release, and the support-dates check shows it is current.

**Negative test.** Try to load a corrupted or unsigned image from `files-201`: the switch refuses it and `diagnose sys firmware info` still shows the old release. Stop the SFTP service: the stitch logs a failed backup.

**Evidence.** The backup file listing, `get system status`, the support-date record, and the refused-image output.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

## Lab Verification

Complete this sign-off once Labs 5.1 to 5.9 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from the workbook's CLI-checked syntax and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the Network Device Management SRG requirements on FortiSwitch in nine labs that follow an administrator session from access, through logon, passwords, audit records, time, and cryptography, to central authentication and software integrity.

- [ ] Has run each NDM lab and its negative test.
- [ ] Has confirmed audit records on the switch and both log servers.
- [ ] Has the evidence for FIPS mode, SNMPv3, and certificates.
- [ ] Knows which requirements are procedures.
