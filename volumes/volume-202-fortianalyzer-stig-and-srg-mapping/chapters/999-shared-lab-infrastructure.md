# Chapter 999: Shared Lab Infrastructure

## Learning Objectives

- Build the lab that every requirement lab of this volume runs on.
- Add a FortiAnalyzer-VM, a FortiGate-VM log source, and a mail server to the lab network of Volume CCI.
- Name the host or service that stands behind each prerequisite of Chapter 01.
- Take a baseline that every lab starts from and returns to.
- Store the evidence of each lab in one place.

## Theory and Architecture

### What this chapter is for

The requirement labs of this volume share one lab, so that each lab starts from the same known state and the evidence of one lab can be compared with another. This chapter builds that lab and its baseline.

The lab is not a new network. It reuses the lab of
[Volume CCI, Chapter 999](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md),
which already has the services a FortiAnalyzer depends on: two RADIUS servers, a TACACS+ server, two syslog servers, two NTP servers, an SNMPv3 manager, an SFTP server, a certificate authority, and an administrator workstation. This chapter adds four hosts to its Lab-Services segment: the FortiAnalyzer under test, a FortiGate-VM that sends it logs, a mail server for alert email, and an optional second FortiAnalyzer.

### The FortiAnalyzer under test

The labs are written for a **FortiAnalyzer-VM on release 7.6**, named `faz-202`. Three facts about it shape the labs:

- **The commands come from release 8.0.0.** Chapter 01 checked every command against the FortiAnalyzer 8.0.0 CLI Reference. Its version column shows that two settings the labs use were introduced in 8.0.0: NTP authentication with SHA-256 and SHA-2 signatures for SAML. Lab 3.7 and Lab 3.15 say what to do on release 7.6. If the unit rejects any other option, type `set ?` in that context and record what the release offers.
- **The license sets the limits.** Chapter 01 records that the license of a FortiAnalyzer-VM sets its daily log storage and its number of ADOMs, and that the unit must be registered with FortiCloud from release 7.2.1. Check the License Information widget of your unit before you plan a lab that needs a second ADOM or a large disk.
- **The console matters.** FIPS-CC mode can be enabled only from the console, which for a virtual machine is the console of the hypervisor.

A hardware FortiAnalyzer can take the place of `faz-202`. The commands are the same, except that `execute lvm` exists only on VM models.

### Topology

`faz-202` has one management port on the Lab-Services segment of Volume CCI (segment 2, VLAN 2, `10.201.2.0/24`). Everything reaches it there:

- **Administrators** connect from `admin-201` on the Admin segment, through the gateway `gw-201`.
- **Log sources** send to it: `fgt-202` sends FortiGate logs, and `admin-201` sends syslog over TLS.
- **Services** answer it on the same segment: the RADIUS, TACACS+, NTP, and certificate hosts.
- **Copies leave it** for other hosts of the segment: forwarded logs and its own event log go to `syslog-201a` and `syslog-201b`, backups go to `files-201`, and alert email goes to `mail-202`.

This volume has no diagram of its own yet. The diagram of Volume CCI's Chapter 999 shows the segment and the reused hosts.

### Address plan

The addresses follow the plan of Volume CCI: the IPv6 address of a host ends in the hexadecimal form of the last octet of its IPv4 address. The four new hosts take addresses from `.100` up, which Volume CCI leaves free on segment 2.

| Host | Role | From | IPv4 | IPv6 |
| --- | --- | --- | --- | --- |
| faz-202 | FortiAnalyzer-VM 7.6 under test | This volume | `10.201.2.100` | `fd00:db8:201::264` |
| faz-202b | Second FortiAnalyzer-VM, a collector for the aggregation step of Lab 3.11 (optional) | This volume | `10.201.2.101` | `fd00:db8:201::265` |
| fgt-202 | FortiGate-VM that sends its logs to `faz-202` | This volume | `10.201.2.110` | `fd00:db8:201::26e` |
| mail-202 | SMTP server with STARTTLS and an account, for alert email | This volume | `10.201.2.120` | `fd00:db8:201::278` |
| gw-201 | Default gateway of the segment | Volume CCI | `10.201.2.1` | See Volume CCI |
| radius-201a | RADIUS server 1 | Volume CCI | `10.201.2.10` | `fd00:db8:201::20a` |
| radius-201b | RADIUS server 2 | Volume CCI | `10.201.2.11` | `fd00:db8:201::20b` |
| tacacs-201 | TACACS+ server | Volume CCI | `10.201.2.12` | `fd00:db8:201::20c` |
| syslog-201a | Central syslog 1, TLS over TCP | Volume CCI | `10.201.2.20` | `fd00:db8:201::214` |
| syslog-201b | Central syslog 2 | Volume CCI | `10.201.2.21` | `fd00:db8:201::215` |
| ntp-201a | Authenticated NTP server 1 | Volume CCI | `10.201.2.30` | `fd00:db8:201::21e` |
| ntp-201b | Authenticated NTP server 2 | Volume CCI | `10.201.2.31` | `fd00:db8:201::21f` |
| nms-201 | SNMPv3 manager | Volume CCI | `10.201.2.40` | `fd00:db8:201::228` |
| files-201 | SFTP server | Volume CCI | `10.201.2.60` | `fd00:db8:201::23c` |
| ca-201 | Lab certificate authority, which stands in for the DoD PKI | Volume CCI | `10.201.2.70` | `fd00:db8:201::246` |
| admin-201 | Administrator workstation, and the syslog test source | Volume CCI | `10.201.3.10` | `fd00:db8:201::30a` |

### How prerequisites map to this lab

Each prerequisite of [Chapter 01](01-fortianalyzer-feature-version-and-srg-map.md) needs a host or a service in the lab. A prerequisite that no requirement lab uses is not built.

| ID | Prerequisite | Lab host or service |
| --- | --- | --- |
| P1 | Log sources | `fgt-202` for FortiGate logs, and `admin-201` for syslog over TLS |
| P2 | ADOMs | The ADOM `lab-202` on `faz-202` |
| P3 | Log storage | The virtual disk of `faz-202`, sized in Lab 999.2 |
| P4 | RADIUS, TACACS+, or LDAP servers | `radius-201a`, `radius-201b`, and `tacacs-201`. LDAP is not built |
| P5 | SAML identity provider | Not built. The SAML settings the labs would test need release 8.0.0 (Lab 3.15) |
| P6 | PKI | `ca-201` and its certificate revocation list |
| P7 | FortiToken Cloud | Not built. It is a cloud subscription (Lab 3.4) |
| P8 | SMTP server | `mail-202` |
| P9 | SNMPv3 manager | `nms-201` |
| P10 | NTP servers and their keys | `ntp-201a` and `ntp-201b` |
| P11 | Syslog server or SIEM | `syslog-201a` and `syslog-201b` |
| P12 | Public cloud log service | Not built. No requirement lab uses it |
| P13 | Another FortiAnalyzer | `faz-202b`, optional, for the aggregation step of Lab 3.11 |
| P14 | SFTP server | `files-201` |
| P15 | HA peer | Not built. No requirement lab uses it |
| P16 | FortiAnalyzer Fabric | Not built. No requirement lab uses it |
| P17 | Fabric connector targets | Not built. No requirement lab uses them |
| P18 | FortiSIEM Supervisor | Not built. No requirement lab uses it |
| P19 | Console access | The hypervisor console of `faz-202` |
| P20 | Web proxy | Not built. No requirement lab uses it |
| P21 | FortiCloud account and registration | Your own FortiCloud account (Lab 999.2) |
| P22 | FortiCare support contract | Your own contract, if the unit has one. Lab 3.14 records it |
| P23 | Outbreak Detection Service license | Not built. No requirement lab uses it |
| P24 | Indicators of compromise license | Not built. Lab 3.12 leaves that step out and says so |
| P25 | Security Automation Service license | Not built. No requirement lab uses it |
| P26 | Security Rating Update license | Not built. No requirement lab uses it |
| P27 | Industrial Security Service license | Not built. No requirement lab uses it |
| P28 | FortiAI license | Not built. No requirement lab uses it |
| P29 | SOCaaS remote access license | Not built. No requirement lab uses it |
| P30 | Licenses on the FortiGates that send logs | Not built. No requirement lab uses them |

## Design Considerations

- **Reuse before you build.** The hosts of Volume CCI already meet six of the prerequisites (P4, P6, P9, P10, P11, and P14). Building them twice would give two secrets, two certificate authorities, and two sources of time to keep apart.
- **Keep the lab closed.** The lab network must not reach a production network. The one outward step is the registration of `faz-202` with FortiCloud, which the unit needs from release 7.2.1.
- **One baseline for the new hosts.** The snapshots are named `baseline-202`. The reused hosts keep the `baseline-201` state of Volume CCI. A lab of this volume that changes a reused host, such as a stopped RADIUS server, puts it back by hand.
- **Make the unit a client everywhere first.** `faz-202` can use a RADIUS, TACACS+, NTP, or syslog server only after that server knows its address and shares a secret, a key, or a certificate with it. Lab 999.1 does that once.
- **Use real log sources.** A log server with no logs proves nothing. `fgt-202` gives the lab FortiGate logs with a device identity, and `admin-201` gives it syslog from a host that is not a Fortinet device.
- **Size the disk for the retention lab.** Lab 3.10 fills an ADOM's quota. A small quota fills fast, so the disk of the virtual machine can stay small.

## Implementation and Automation

### Addressing and naming rules

Host names end in `-202` for hosts this volume adds and in `-201` for hosts of Volume CCI. New hosts take addresses from `10.201.2.100` up. The ADOM of the labs is `lab-202`, the read-only profile is `lab-readonly`, and the snapshot is `baseline-202`.

The lab scripts and the Lab Builder of Volume CCI build the reused hosts. They do not build the four hosts of this volume, which you deploy by hand in Labs 999.2 and 999.3.

### Evidence

Save the output that each lab's **Evidence** line names in `evidence/<lab>/<date>/` on `admin-201`, the folder Volume CCI uses. Put the model, the release, and the build of `faz-202` at the top of each file (`get system status`), and replace passwords, keys, and secrets with `<SECRET>`. A finished lab sign-off points at that folder.

## Validation and Troubleshooting

The lab is at its baseline when these checks pass without an edit:

- `faz-202` answers a ping from `admin-201`, and `get system status` shows the release.
- `diagnose dvm device list` shows `fgt-202` as authorized.
- A test message from the account of `faz-202` reaches a mailbox on `mail-202`.
- The checks of Lab 999.1 pass.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `faz-202` cannot be reached from `admin-201` | The port has no address, the wrong VLAN, or no default route to `10.201.2.1` | Check the port from the console and the port group or bridge of the virtual machine |
| The GUI asks for registration and offers nothing else | The unit is not registered with FortiCloud | Register it with your own account (Lab 999.2) |
| `fgt-202` does not appear in Device Manager | The FortiGate does not send to `10.201.2.100`, or the two cannot reach each other | Check the log setting on the FortiGate and ping between the two |
| A reused server refuses `faz-202` | The server has no client entry for `10.201.2.100` | Add the entry (Lab 999.1) |

## Security and Best Practices

- Keep the lab network apart from production, and keep the lab's secrets out of production systems.
- Generate the secrets, keys, and passwords for a run, write them as `<SECRET>` in the evidence, and delete them from every host when the run ends.
- Use your own FortiCloud account for the registration, and do not share its password or token with anyone, including an assistant.
- Take the snapshot before a lab that can lock you out or change the unit, such as Lab 3.2 and Lab 3.6.
- Shut the virtual machines down when the lab is idle.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortianalyzer-feature-version-and-srg-map.md) for the prerequisites this lab provides.
- [Volume CCI, Chapter 999](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md) for the lab network, the reused hosts, and how they are built.
- Fortinet, *FortiAnalyzer Administration Guide* and the VM installation guide for your hypervisor, for release 7.6 (Fortinet Document Library). Chapter 01 has no command for the first setup of a unit.

**Knowledge checks:**

1. Which hosts does this volume add to the lab of Volume CCI, and what is each one for?
2. Why must `faz-202` be made a client of the reused servers before the requirement labs?
3. Which prerequisites of Chapter 01 are not built in this lab, and why?
4. Why does the baseline of this volume cover only the new hosts?

## Hands-On Lab

**Shared prerequisites.** The lab of Volume CCI, built through its Labs 999.1 and 999.2, so that the gateway and the service hosts run. A hypervisor with room for three or four more virtual machines. A FortiAnalyzer-VM image and a FortiGate-VM image for that hypervisor, which you download from the vendor with your own account, and a FortiCloud account. **Cost:** none, unless your FortiAnalyzer-VM needs a paid license for the storage or the ADOMs you plan.

### Lab 999.1 — Prepare the lab of Volume CCI for a new client

**Goal.** Each reused server accepts `faz-202` as a client before the unit exists, so the requirement labs do not stop at the server.

1. Confirm that the lab of Volume CCI runs: from `admin-201`, ping `10.201.2.1` and each reused host of the address plan.
2. On `radius-201a` and `radius-201b`, add `10.201.2.100` as a client with a shared secret, and make the servers accept RADIUS over TLS, because the commands of Chapter 01 use `set protocol tls`. Add a test administrator.
3. On `tacacs-201`, which is optional in Volume CCI and needed here for Lab 4.1, add `10.201.2.100` as a client with a key, and add a test administrator.
4. On `ntp-201a` and `ntp-201b`, note the key ID and the key that the unit will use.
5. On `syslog-201a` and `syslog-201b`, confirm that the listener takes TLS on TCP, and that its certificate comes from `ca-201`.
6. On `nms-201`, plan the SNMPv3 user, with SHA-256 authentication and AES-256 privacy.
7. On `files-201`, create an account and a directory for the backups of `faz-202`.
8. On `ca-201`, note where the CA certificate and the certificate revocation list are published, and issue a client certificate for `admin-201` and one for a test administrator.

**Expected result.** Every reused server has an entry for `10.201.2.100`, and you hold the secrets, keys, and certificates the labs name.

### Lab 999.2 — Deploy the FortiAnalyzer-VM

**Goal.** `faz-202` runs release 7.6, is registered, and is reachable from `admin-201` over HTTPS and SSH only.

1. Deploy the FortiAnalyzer-VM image on the hypervisor, with one port on the Lab-Services segment and a virtual disk for the logs. Follow the vendor's installation guide for your hypervisor.
2. From the hypervisor console, give the port the address `10.201.2.100/24`, set the default route to `10.201.2.1`, and set the host name `faz-202`. Chapter 01 has no command for these three settings, so take them from the Administration Guide.
3. Allow only HTTPS and SSH on the port.

   ```text
   config system interface
       edit <PORT>
           set allowaccess https ssh
   end
   ```

4. Open the GUI from `admin-201` and register the unit in the setup wizard with your own FortiCloud account. Check the result in the GUI under Dashboards > Status > License Information.
5. Record the release and the build with `get system status`, and the size of the log disk with `execute lvm info`. If the disk is too small, add a virtual disk and run `execute lvm extend`.
6. Enable ADOMs, create the ADOM `lab-202` in the GUI, and assign your administrator to it.

   ```text
   config system global
       set adom-status enable
   end
   config system admin user
       edit <ADMIN>
           set adom lab-202
   end
   ```

7. If you want the aggregation step of Lab 3.11, deploy `faz-202b` at `10.201.2.101` in the same way.

**Expected result.** `faz-202` answers HTTPS and SSH from `admin-201` and nothing else, shows release 7.6, and is registered.

### Lab 999.3 — Add the log sources and the mail server

**Goal.** `faz-202` receives logs from a FortiGate and from a syslog host, and a mail server takes its alerts.

1. Deploy `fgt-202`, a FortiGate-VM, with a port at `10.201.2.110/24` on the Lab-Services segment. On the FortiGate, send the logs to `10.201.2.100`. The command is in the FortiOS documentation, not in this volume.
2. Authorize `fgt-202` on `faz-202` in the GUI under Device Manager, put it in the ADOM `lab-202`, and check it.

   ```text
   diagnose dvm device list
   ```

3. On `admin-201`, set up a syslog sender that uses TLS on TCP port 6514 with the client certificate from Lab 999.1. The requirement labs send test messages with it.
4. Deploy `mail-202`, a small Linux host at `10.201.2.120/24`, with an SMTP server that offers STARTTLS and requires an account. Create a mailbox for the SA and one for the ISSO, and an account for `faz-202`.
5. Point both `fgt-202` and `faz-202` at the same time sources, `ntp-201a` and `ntp-201b`. Lab 3.7 adds the authentication.

**Expected result.** A log caused on `fgt-202` appears in Log View on `faz-202`, a test syslog message from `admin-201` is ready to send, and a test email reaches a mailbox on `mail-202`.

### Lab 999.4 — Take the baseline and reset to it

**Goal.** A saved state that every requirement lab starts from.

1. Save the configuration of `faz-202` off the unit.

   ```text
   execute backup all-settings sftp 10.201.2.60 <FILE> <USER> <PASSWORD>
   ```

2. Snapshot `faz-202`, `fgt-202`, and `mail-202`, and `faz-202b` if you built it. Name each snapshot `baseline-202`.
3. To reset between labs, restore the snapshots. Put back by hand anything a lab changed on a reused host of Volume CCI.
4. In `evidence/` on `admin-201`, add a text file with the release and the build of `faz-202`, its license, the hypervisor, and where the lab's secrets are stored, not their values.

**Expected result.** After a reset, the checks under *Validation and Troubleshooting* pass without an edit.

### Cleanup

When a run of labs ends, delete the lab's secrets from every host, remove the client entries for `10.201.2.100` from the reused servers if the unit will not return, and shut the four virtual machines down.

## Lab Verification

Complete this sign-off once Labs 999.1 to 999.4 have been run end to end. Until then, the lab is unverified: this chapter was written from Chapter 01 and from Volume CCI's Chapter 999, and no host of it has been built.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter adds a FortiAnalyzer-VM on release 7.6, a FortiGate-VM log source, a mail server, and an optional second FortiAnalyzer to the lab network of Volume CCI, and reuses that lab's authentication, time, logging, file, and certificate hosts. It names the host or service behind each prerequisite of Chapter 01, and it takes the `baseline-202` snapshots that every requirement lab returns to.

- [ ] Has made `faz-202` a client of the reused servers.
- [ ] Has deployed and registered `faz-202`, and limited its port to HTTPS and SSH.
- [ ] Has authorized `fgt-202`, and has a syslog sender and a mail server ready.
- [ ] Has taken the `baseline-202` snapshots and can reset to them.
