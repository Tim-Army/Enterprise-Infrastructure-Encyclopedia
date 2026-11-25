# Chapter 04: Network Device Management SRG Requirement Labs

## Learning Objectives

- Prove each Network Device Management SRG requirement that this volume's tables cite on the Chapter 999 lab, with a positive and a negative test.
- Query the unit with SNMPv3 that uses SHA-2 authentication and AES privacy.
- Authenticate the NTP sources, and authenticate administrators through more than one authentication server.
- Back up the configuration to another system, and send the unit's own event log to a central log server.
- Store the evidence for each lab so it can support an assessment.

## Theory and Architecture

The Network Device Management SRG covers how an administrator reaches, authenticates to, and is held accountable on a network device. FortiAnalyzer is assessed against the Central Log Server SRG, which states most of those management requirements in its own words, so Chapter 01 maps only five NDM requirements: the ones the Central Log Server SRG does not cover. They are about the services a managed device depends on: SNMP, time, authentication servers, backup, and sending its own logs away.

Lab 4.1 covers the three services that answer or authenticate. Lab 4.2 covers the two that copy data off the unit.

All labs run on the network from [Chapter 999](999-shared-lab-infrastructure.md).

### Requirements and labs

Chapter 01 lists 5 distinct Network Device Management SRG requirements for FortiAnalyzer. Each one has a lab in this chapter, so none is left without a test. The crosswalk in Chapter 02 also cites 21 NDM IDs that belong to Cisco rules. They are not requirements of FortiAnalyzer, and they have no lab.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 4.1 | 3 | Requirement lab: Management services: SNMPv3, authenticated NTP sources, and authentication servers |
| 4.2 | 2 | Requirement lab: Configuration backup and the unit's own logs to a central log server |

Every requirement here has a FortiAnalyzer setting behind it, so this chapter has requirement labs only. Each lab configures the setting, proves it with a positive test, and proves the control with a negative test.

## Design Considerations

- **These labs build on Chapter 03.** NTP authentication is configured in Lab 3.7 and RADIUS in Lab 3.1. The labs here prove the NDM wording of the requirement: every source authenticated, and more than one server.
- **Two servers where the SRG says two.** The SRG asks for at least one authentication server and one central log server, and for two of each on a boundary device. The lab configures two, so that the failure of one can be tested.
- **The lab unit runs FortiAnalyzer 7.6.** NTP authentication with SHA-256 needs 8.0.0, as Lab 3.7 records. If release 7.6 rejects any other option, type `set ?` in that context, use what the release offers, and record the difference as a finding.
- **Prove the copy, not only the setting.** The evidence for a backup is the file on `files-201`, and for logging it is the record on `syslog-201a`.

## Implementation and Automation

Each lab lists its commands in the order to enter them. Commands come from [Chapter 01](01-fortianalyzer-feature-version-and-srg-map.md), with the lab's values from Chapter 999 substituted.
The placeholders are `<SNMP_USER>` for the SNMPv3 user, `<SECRET>`, `<KEY>`, and `<PASSWORD>` for values you generate for the run, and `<ENCRYPTION_PASSWORD>` for the password that encrypts the backup. Addresses are those of Chapter 999.

Save the evidence for each lab in `evidence/<lab>/<date>/`, as Chapter 999 describes.

## Validation and Troubleshooting

Before each lab, confirm the baseline: `get system status` on `faz-202` shows the release, and `faz-202` answers a ping from `admin-201`. After each lab, restore the baseline and repeat the checks.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `nms-201` gets no SNMP answer | The user, the authentication key, or the privacy key differs between `nms-201` and `faz-202` | Compare both ends, and check `config system snmp user` |
| The backup does not arrive | The SFTP account or the directory on `files-201` is wrong | Log on to `files-201` with the same account by hand |
| No record arrives on `syslog-201a` | The server does not accept TLS on TCP, or `faz-202` does not trust its certificate | Check the listener on `syslog-201a` and the CA certificate on `faz-202` |
| A logon still works with the first server stopped, and you expected a failure | The second server answered | That is the wanted result; read which server the event log names |

## Security and Best Practices

- Use an SNMP user, keys, and a backup password that exist only for the run, write them as `<SECRET>` in the evidence, and delete them in the cleanup.
- Encrypt the configuration backup, because it holds every secret of the unit.
- Do not send the unit's own log in clear text to test a failure. Break the certificate instead.
- Record the release and the build of `faz-202` with every result.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortianalyzer-feature-version-and-srg-map.md) and [Chapter 02](02-fortianalyzer-and-cisco-stig-crosswalk.md) for the rows these labs prove.
- [Chapter 999](999-shared-lab-infrastructure.md) for the lab network, hosts, and baseline.
- DISA Network Device Management SRG V5R5, from the October 2026 STIG Library Compilation. Confirm the current release on the DoD Cyber Exchange.
- Fortinet, *FortiAnalyzer 8.0.0 CLI Reference*, which Chapter 01 used.
- [Volume CLXXII, Chapter 03](../../volume-172-disa-srgs-and-stigs/chapters/03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md) for assessing a product that has no STIG.

**Knowledge checks:**

1. Why does Chapter 01 map only five NDM requirements to FortiAnalyzer?
2. Which three values must match on `nms-201` and `faz-202` for an SNMPv3 query to be answered?
3. Why does the lab configure two authentication servers?
4. Why is the configuration backup encrypted?
5. What is the evidence that the unit's own log left the unit?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 and its baseline. The `baseline-202` snapshot of `faz-202`. An SNMPv3 client on `nms-201`, and an SSH client and a browser on `admin-201`. **Cost:** none beyond the Chapter 999 lab.

### Lab 4.1 — Management services: SNMPv3, authenticated NTP sources, and authentication servers

**Goal.** Show that SNMP, NTP, and administrator logons each authenticate against the lab's servers, and that a second authentication server takes over when the first fails.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000395-NDM-000310` | II | Authenticate SNMP messages with a FIPS-validated HMAC. | Same requirement | SNMPv3 |
| `SRG-APP-000395-NDM-000347` | II | Authenticate NTP sources cryptographically. | Same requirement | NTP server; FortiAnalyzer supports NTPv4 with SHA-256 encryption |
| `SRG-APP-000516-NDM-000336` | I | Authenticate administrators through at least one authentication server (two for boundary devices). | Same requirement | RADIUS administrator authentication; TACACS+ administrator authentication; LDAP administrator authentication |

**Uses.** `faz-202`, `nms-201`, `ntp-201a`, `ntp-201b`, `radius-201a`, `radius-201b`, `tacacs-201`, and `admin-201`.

**Configure.**

1. Create an SNMPv3 user with SHA-2 authentication and AES privacy, for queries and notifications from `nms-201`.

   ```text
   config system snmp user
       edit <SNMP_USER>
           set security-level auth-priv
           set auth-proto sha256
           set priv-proto aes256
           set notify-hosts 10.200.0.49
           set queries enable
   end
   ```

2. Authenticate both NTP sources, `ntp-201a` and `ntp-201b`, as in Lab 3.7. The note there about the key type on release 7.6 applies here too.
3. Use more than one authentication server: the two RADIUS servers and the TACACS+ server. `set protocol tls` needs RADIUS over TLS on the RADIUS servers (Chapter 999).

   ```text
   config system admin radius
       edit radius-201a
           set server 10.200.0.42
           set secret <SECRET>
           set protocol tls
           set message-authenticator require
   end
   config system admin radius
       edit radius-201b
           set server 10.200.0.43
           set secret <SECRET>
           set protocol tls
           set message-authenticator require
   end
   config system admin tacacs
       edit tacacs-201
           set server 10.200.0.44
           set key <KEY>
           set authorization enable
   end
   ```

**Positive test.** From `nms-201`, an SNMPv3 query with the user, SHA-256 authentication, and AES-256 privacy is answered. A RADIUS administrator logs on. Stop `radius-201a`: an administrator of `radius-201b` or of `tacacs-201` still logs on, and the event log names the server that answered.

**Negative test.** From `nms-201`, a query with an SNMPv2c community, and then an SNMPv3 query with a wrong authentication key, get no answer. Change the secret for `radius-201a` on `faz-202` to a wrong value: a logon through that server is refused. An NTP source with a wrong key is not accepted (Lab 3.7).

**Evidence.** The `snmp`, `ntp`, `radius`, and `tacacs` settings from `show full-configuration`, the answered and the unanswered SNMP queries, and the event log lines that name the authentication server for each logon.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4), and start `radius-201a` again.

### Lab 4.2 — Configuration backup and the unit's own logs to a central log server

**Goal.** Show that the configuration is backed up to another system, and that the unit's own event log reaches a central log server over TLS.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 | Features in Chapter 01 |
| --- | --- | --- | --- | --- |
| `SRG-APP-000516-NDM-000340` | II | Back up system-level information when changes occur. | Same requirement | Configuration backup; Suggest backup before upgrade; Backup strategy and configuration setup added to the FortiAnalyzer setup wizard; and 1 more |
| `SRG-APP-000516-NDM-000350` | I | Send the device's own logs to at least one central log server (two for boundary devices). | Same requirement | Sending FortiAnalyzer event logs to a syslog server; FortiAnalyzer supports IPv6 address type for syslog server configuration |

**Uses.** `faz-202`, `files-201`, `syslog-201a`, `syslog-201b`, and `admin-201`.

**Configure.**

1. Schedule an encrypted backup of the configuration to `files-201`. The SRG asks for a backup when changes occur. Chapter 01 gives the scheduled backup, so after a change also run the backup at once with the second command.

   ```text
   config system backup all-settings
       set status enable
       set protocol sftp
       set server 10.200.0.51
       set user <USER>
       set passwd <PASSWORD>
       set crptpasswd <ENCRYPTION_PASSWORD>
   end
   execute backup all-settings sftp 10.200.0.51 <FILE> <USER> <PASSWORD>
   ```

2. Send the unit's own event log to `syslog-201a` over TCP with TLS.

   ```text
   config system syslog
       edit syslog-201a
           set ip 10.200.0.45
           set reliable enable
           set secure-connection enable
   end
   config system locallog syslogd setting
       set status enable
       set syslog-name syslog-201a
   end
   ```

3. Add `syslog-201b` (`10.200.0.46`) under `config system syslog` in the same way. Chapter 01 gives one `syslogd` setting. Type `config system locallog ?` to see whether your release has a second one. If it has, point it at `syslog-201b`. If it has not, record that the unit sends its own log to one server.

**Positive test.** Change a setting, for example add a test account, and run the backup: a dated, encrypted file appears on `files-201`. Log on and log off: the records appear on `syslog-201a`, received over TLS on TCP, with `faz-202` as their source.

**Negative test.** Run the backup with a wrong password: it fails, and the unit reports the failure. Give `syslog-201a` a certificate that `faz-202` does not trust: the unit sends nothing, and a capture on `syslog-201a` shows no record from `faz-202` in clear text.

**Evidence.** The `backup`, `syslog`, and `locallog` settings from `show full-configuration`, the list of backup files on `files-201` with their dates, one record on `syslog-201a` with its time, and the failed backup.

**Return to baseline.** Restore the `baseline-202` snapshot of `faz-202` (Lab 999.4), delete the test backup files from `files-201`, and give `syslog-201a` its own certificate back.

## Lab Verification

Complete this sign-off once Labs 4.1 to 4.2 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from Chapter 01 and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the five Network Device Management SRG requirements that Chapter 01 maps to FortiAnalyzer, in two labs: SNMPv3, authenticated time, and authentication servers in Lab 4.1, and the configuration backup and the unit's own logs in Lab 4.2. FortiAnalyzer has a setting for each of the five, so the chapter has no gap lab.

- [ ] Has run each requirement lab and its negative test.
- [ ] Has shown that a second authentication server answers when the first is stopped.
- [ ] Has stored the evidence for each lab.
