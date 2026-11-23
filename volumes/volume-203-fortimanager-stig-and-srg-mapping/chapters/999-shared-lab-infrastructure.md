# Chapter 999: Shared Lab Infrastructure

## Learning Objectives

- Build the lab that every requirement lab of this volume runs on.
- Add a FortiManager-VM to the lab network of Volume CCI, and give it a FortiGate-VM to manage.
- Reuse the FortiGate-VM and the mail server of Volume CCII, or build them if that lab does not exist.
- Name the host or service that stands behind each prerequisite of Chapter 01.
- Take a baseline that every lab starts from and returns to.
- Store the evidence of each lab in one place.

## Theory and Architecture

### What this chapter is for

The requirement labs of this volume share one lab, so that each lab starts from the same known state and the evidence of one lab can be compared with another. This chapter builds that lab and its baseline.

The lab is not a new network. It reuses the lab of
[Volume CCI, Chapter 999](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md),
which already has the services a FortiManager depends on: two RADIUS servers, a TACACS+ server, two syslog servers, two NTP servers, an SNMPv3 manager, an SFTP server, a certificate authority, and an administrator workstation. It also reuses two hosts of
[Volume CCII, Chapter 999](../../volume-202-fortianalyzer-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md):
the FortiGate-VM, which becomes the managed device, and the mail server. This chapter adds one host to the Lab-Services segment: the FortiManager under test.

### The FortiManager under test

The labs are written for a **FortiManager-VM on release 7.6**, named `fmg-203`. Three facts about it shape the labs:

- **The commands come from release 8.0.1.** Chapter 01 checked every command against the FortiManager 8.0.1 CLI Reference. Its version column shows that one setting the labs use was introduced in 8.0.0: NTP authentication with SHA-256. Lab 2.12 says what to do on release 7.6. If the unit rejects any other option, type `set ?` in that context and record what the release offers.
- **The license sets the limits.** Chapter 01 records that the model or the VM license sets the number of ADOMs and of managed devices, and that a VM license is activated through a FortiCloud registration. The labs need one ADOM besides the root ADOM and one managed device. Check the License Information widget of your unit before you plan more.
- **The console matters.** FIPS-CC mode can be enabled only from the console, which for a virtual machine is the console of the hypervisor.

A hardware FortiManager can take the place of `fmg-203`. The commands are the same.

### Topology

`fmg-203` has one management port on the Lab-Services segment of Volume CCI (segment 2, VLAN 2, `10.200.2.0/24`). Everything reaches it there:

- **Administrators** connect from `admin-201` on the Admin segment, through the gateway `gw-201`.
- **The managed device**, `fgt-202`, registers with it and receives its configuration over the FGFM tunnel.
- **Services** answer it on the same segment: the RADIUS, TACACS+, NTP, and certificate hosts.
- **Copies leave it** for other hosts of the segment: its event log goes to `syslog-201a`, and to `faz-202` if the lab has one, backups go to `files-201`, and alert and approval email goes to `mail-202`.

This volume has no diagram of its own yet. The diagram of Volume CCI's Chapter 999 shows the segment and the hosts of that volume.

### Address plan

The addresses follow the plan of Volume CCI: the IPv6 address of a host ends in the hexadecimal form of the last octet of its IPv4 address. Volume CCII took `.100` to `.120` on segment 2. `fmg-203` takes `.130`.

| Host | Role | From | IPv4 | IPv6 |
| --- | --- | --- | --- | --- |
| fmg-203 | FortiManager-VM 7.6 under test | This volume | `10.200.2.130` | `fd00:db8:201::282` |
| fgt-202 | FortiGate-VM, the device that `fmg-203` manages | Volume CCII | `10.200.2.110` | `fd00:db8:201::26e` |
| mail-202 | SMTP server with STARTTLS and an account, for alert and approval email | Volume CCII | `10.200.2.120` | `fd00:db8:201::278` |
| faz-202 | FortiAnalyzer-VM that takes the event log in Lab 2.11 (optional) | Volume CCII | `10.200.2.100` | `fd00:db8:201::264` |
| gw-201 | Default gateway of the segment | Volume CCI | `10.200.2.1` | See Volume CCI |
| radius-201a | RADIUS server 1 | Volume CCI | `10.200.2.10` | `fd00:db8:201::20a` |
| radius-201b | RADIUS server 2 | Volume CCI | `10.200.2.11` | `fd00:db8:201::20b` |
| tacacs-201 | TACACS+ server, for authentication and accounting | Volume CCI | `10.200.2.12` | `fd00:db8:201::20c` |
| syslog-201a | Central syslog 1, TLS over TCP | Volume CCI | `10.200.2.20` | `fd00:db8:201::214` |
| syslog-201b | Central syslog 2 | Volume CCI | `10.200.2.21` | `fd00:db8:201::215` |
| ntp-201a | Authenticated NTP server 1 | Volume CCI | `10.200.2.30` | `fd00:db8:201::21e` |
| ntp-201b | Authenticated NTP server 2 | Volume CCI | `10.200.2.31` | `fd00:db8:201::21f` |
| nms-201 | SNMPv3 manager, and the host outside the admin network in Lab 2.2 | Volume CCI | `10.200.2.40` | `fd00:db8:201::228` |
| files-201 | SFTP server | Volume CCI | `10.200.2.60` | `fd00:db8:201::23c` |
| ca-201 | Lab certificate authority, which stands in for the DoD PKI | Volume CCI | `10.200.2.70` | `fd00:db8:201::246` |
| admin-201 | Administrator workstation | Volume CCI | `10.200.3.10` | `fd00:db8:201::30a` |

### How prerequisites map to this lab

Each prerequisite of [Chapter 01](01-fortimanager-feature-version-and-srg-map.md) needs a host or a service in the lab. A prerequisite that no requirement lab uses is not built.

| ID | Prerequisite | Lab host or service |
| --- | --- | --- |
| P1 | Managed devices | `fgt-202`, authorized in Lab 999.3 |
| P2 | ADOMs | The ADOM `lab-203` on `fmg-203` |
| P3 | FortiSwitches, FortiAPs, or FortiExtenders behind a managed FortiGate | Not built. No requirement lab uses them |
| P4 | The traffic-sniffer setting on the FortiGate | Not built. No requirement lab uses it |
| P5 | Workspace mode or workflow mode | A setting of `fmg-203`, which Lab 2.14 enables |
| P6 | A workflow approval matrix | The approval matrix of the ADOM `lab-203`, with `mail-202` for its notifications (Lab 2.14) |
| P7 | RADIUS, TACACS+, or LDAP servers | `radius-201a`, `radius-201b`, and `tacacs-201`. LDAP is not built |
| P8 | SAML identity provider | Not built. No requirement lab uses it |
| P9 | PKI | `ca-201` and its certificate revocation list |
| P10 | FortiToken Cloud | Not built. It is a cloud subscription (Lab 2.6) |
| P11 | SMTP server | `mail-202` |
| P12 | SNMPv3 manager | `nms-201` |
| P13 | NTP servers and their keys | `ntp-201a` and `ntp-201b` |
| P14 | Syslog server or SIEM | `syslog-201a` and `syslog-201b` |
| P15 | A FortiAnalyzer | `faz-202`, optional, for a step of Lab 2.11 |
| P16 | SFTP server | `files-201` |
| P17 | Fabric connector targets | Not built. No requirement lab uses them |
| P18 | FortiSASE entitlement | Not built. No requirement lab uses it |
| P19 | Console access | The hypervisor console of `fmg-203` |
| P20 | A hardware appliance, or one with a TPM | Not built. The lab unit is a virtual machine |
| P21 | A FortiManager-VM in Microsoft Azure | Not built. The lab unit does not run in Azure |
| P22 | FortiCloud account and registration | Your own FortiCloud account, to activate the VM license (Lab 999.2). FortiCloud SSO is not used |
| P23 | FortiCare support contract | Your own contract, if the unit has one. Lab 2.16 records it |

## Design Considerations

- **Reuse before you build.** The hosts of Volume CCI already meet six of the prerequisites (P7, P9, P12, P13, P14, and P16), and the hosts of Volume CCII meet three more (P1, P11, and P15). Building them twice would give two secrets, two certificate authorities, and two sources of time to keep apart.
- **Keep the lab closed.** The lab network must not reach a production network. The one outward step is the registration of `fmg-203` with FortiCloud, which activates its license.
- **One managed device, and it is a lab device.** `fmg-203` installs configuration on what it manages. Keep `fgt-202` as the only device in the ADOM `lab-203`, and never add a production device to this unit.
- **A FortiGate can serve both volumes.** `fgt-202` can send its logs to `faz-202` and be managed by `fmg-203` at the same time. The two settings are independent on the FortiGate.
- **One baseline for this volume.** The snapshots of `fmg-203` and of `fgt-202` in its managed state are named `baseline-203`. The reused hosts of Volume CCI keep their `baseline-201` state, and `mail-202` and `faz-202` keep `baseline-202`. A lab of this volume that changes a reused host, such as a stopped RADIUS server, puts it back by hand.
- **Make the unit a client everywhere first.** `fmg-203` can use a RADIUS, TACACS+, NTP, or syslog server only after that server knows its address and shares a secret, a key, or a certificate with it. Lab 999.1 does that once.

## Implementation and Automation

### Addressing and naming rules

Host names end in `-203` for the host this volume adds, in `-202` for hosts of Volume CCII, and in `-201` for hosts of Volume CCI. `fmg-203` has the address `10.200.2.130`. The ADOM of the labs is `lab-203`, the read-only profile is `lab-readonly`, the profile that edits and cannot install is `lab-editor`, and the snapshot is `baseline-203`.

The lab scripts of [Volume CMI](../../volume-901-lab-selector/README.md) build the reused hosts of Volume CCI, and its Lab Selector plans a build for the labs of this volume. [Open it with the FortiManager lab set ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortimanager), or tick that lab set on the page. The scripts do not build `fmg-203`, `fgt-202`, or `mail-202`, which you deploy by hand in Labs 999.2 and 999.3. The Lab Selector lists them with their addresses in your build.

### Evidence

Save the output that each lab's **Evidence** line names in `evidence/<lab>/<date>/` on `admin-201`, the folder Volume CCI uses. Put the model, the release, and the build of `fmg-203` at the top of each file (`get system status`), and replace passwords, keys, and secrets with `<SECRET>`. A finished lab sign-off points at that folder.

## Validation and Troubleshooting

The lab is at its baseline when these checks pass without an edit:

- `fmg-203` answers a ping from `admin-201`, and `get system status` shows the release.
- `diagnose dvm device list` shows `fgt-202` as a managed device in the ADOM `lab-203`.
- A test message from the account of `fmg-203` reaches a mailbox on `mail-202`.
- The checks of Lab 999.1 pass.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `fmg-203` cannot be reached from `admin-201` | The port has no address, the wrong VLAN, or no default route to `10.200.2.1` | Check the port from the console and the port group or bridge of the virtual machine |
| The GUI asks for registration and offers nothing else | The unit is not registered with FortiCloud | Register it with your own account (Lab 999.2) |
| `fgt-202` does not appear in Device Manager | The FortiGate does not point at `10.200.2.130`, or the two cannot reach each other | Check the central management setting on the FortiGate and ping between the two |
| `fgt-202` appears and cannot be authorized | The license of `fmg-203` allows no more devices, or the release of the FortiGate is newer than the unit supports | Check the License Information widget, and the release notes for the FortiOS releases the unit manages |
| A reused server refuses `fmg-203` | The server has no client entry for `10.200.2.130` | Add the entry (Lab 999.1) |

## Security and Best Practices

- Keep the lab network apart from production, and keep the lab's secrets out of production systems.
- Generate the secrets, keys, and passwords for a run, write them as `<SECRET>` in the evidence, and delete them from every host when the run ends.
- Use your own FortiCloud account for the registration, and do not share its password or token with anyone, including an assistant.
- Never add a production device to `fmg-203`. An install from a lab unit changes the device.
- Take the snapshot before a lab that can lock you out or change the unit, such as Lab 2.2, Lab 2.3, and Lab 2.13.
- Shut the virtual machines down when the lab is idle.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortimanager-feature-version-and-srg-map.md) for the prerequisites this lab provides.
- [Volume CCI, Chapter 999](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md) for the lab network, the reused service hosts, and how they are built.
- [Volume CCII, Chapter 999](../../volume-202-fortianalyzer-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md) for `fgt-202`, `mail-202`, and `faz-202`.
- Fortinet, *FortiManager Administration Guide* and the VM installation guide for your hypervisor, for release 7.6 (Fortinet Document Library). Chapter 01 has no command for the first setup of a unit.

**Knowledge checks:**

1. Which host does this volume add to the lab, and which hosts does it reuse from Volumes CCI and CCII?
2. Why must `fmg-203` be made a client of the reused servers before the requirement labs?
3. Why does the ADOM `lab-203` hold only `fgt-202`?
4. Which prerequisites of Chapter 01 are not built in this lab, and why?

## Hands-On Lab

**Shared prerequisites.** The lab of Volume CCI, built through its Labs 999.1 and 999.2, so that the gateway and the service hosts run. A hypervisor with room for one more virtual machine, or for three more if `fgt-202` and `mail-202` do not exist yet. A FortiManager-VM image for that hypervisor, and a FortiGate-VM image if you build `fgt-202`, which you download from the vendor with your own account, and a FortiCloud account. **Cost:** none, unless your FortiManager-VM needs a paid license for the ADOM or the device you plan.

### Lab 999.1 — Prepare the reused servers for a new client

**Goal.** Each reused server accepts `fmg-203` as a client before the unit exists, so the requirement labs do not stop at the server.

1. Confirm that the lab of Volume CCI runs: from `admin-201`, ping `10.200.2.1` and each reused host of the address plan.
2. On `radius-201a` and `radius-201b`, add `10.200.2.130` as a client with a shared secret, and make the servers accept RADIUS over TLS, because the commands of Chapter 01 use `set protocol tls`. Add a test administrator.
3. On `tacacs-201`, which is optional in Volume CCI and needed here for Labs 2.5 and 2.9, add `10.200.2.130` as a client with a key, turn on accounting, and add a test administrator.
4. On `ntp-201a` and `ntp-201b`, note the key ID and the key that the unit will use.
5. On `syslog-201a` and `syslog-201b`, confirm that the listener takes TLS on TCP, and that its certificate comes from `ca-201`.
6. On `nms-201`, plan the SNMPv3 user, with SHA-256 authentication and AES-256 privacy.
7. On `files-201`, create an account and a directory for the backups of `fmg-203`.
8. On `ca-201`, note where the CA certificate and the certificate revocation list are published, issue a client certificate for a test administrator, and plan the server certificate of `fmg-203`.

**Expected result.** Every reused server has an entry for `10.200.2.130`, and you hold the secrets, keys, and certificates the labs name.

### Lab 999.2 — Deploy the FortiManager-VM

**Goal.** `fmg-203` runs release 7.6, has an active license, and is reachable from `admin-201` over HTTPS and SSH only.

1. Deploy the FortiManager-VM image on the hypervisor, with one port on the Lab-Services segment. Follow the vendor's installation guide for your hypervisor.
2. From the hypervisor console, give the port the address `10.200.2.130/24`, set the default route to `10.200.2.1`, and set the host name `fmg-203`. Chapter 01 has no command for these three settings, so take them from the Administration Guide.
3. Allow only HTTPS and SSH on the port.

   ```text
   config system interface
       edit <PORT>
           set allowaccess https ssh
   end
   ```

4. Open the GUI from `admin-201` and register the unit with your own FortiCloud account, which activates the license. Check the result in the GUI under System Settings > Dashboard > License Information.
5. Record the release and the build with `get system status`, and the license with `diagnose license list`.
6. Enable ADOMs, create the ADOM `lab-203` in the GUI, and assign your administrator to it.

   ```text
   config system global
       set adom-status enable
   end
   config system admin user
       edit <ADMIN>
           set adom lab-203
   end
   ```

**Expected result.** `fmg-203` answers HTTPS and SSH from `admin-201` and nothing else, shows release 7.6, and has an active license.

### Lab 999.3 — Add the managed device and the mail server

**Goal.** `fmg-203` manages one FortiGate, and a mail server takes its alerts and its approval notifications.

1. If the lab of Volume CCII exists, start its `fgt-202` and `mail-202`. If it does not, deploy the two hosts as Lab 999.3 of that volume's Chapter 999 describes: a FortiGate-VM with a port at `10.200.2.110/24`, and a small Linux host at `10.200.2.120/24` with an SMTP server that offers STARTTLS and requires an account. You do not need `faz-202` for this.
2. On `fgt-202`, set `10.200.2.130` as the FortiManager for central management. The command is in the FortiOS documentation, not in this volume.
3. Authorize `fgt-202` on `fmg-203` in the GUI under Device Manager, put it in the ADOM `lab-203`, and check it.

   ```text
   diagnose dvm device list
   ```

4. Import the policy of `fgt-202` into a policy package in the GUI, so that the labs have a package to change and to install.
5. On `mail-202`, create a mailbox for an approver and one for the ISSO, and an account for `fmg-203`.
6. Point both `fgt-202` and `fmg-203` at the same time sources, `ntp-201a` and `ntp-201b`. Lab 2.12 adds the authentication.

**Expected result.** `fgt-202` is a managed device in the ADOM `lab-203` with a policy package, and a test email reaches a mailbox on `mail-202`.

### Lab 999.4 — Take the baseline and reset to it

**Goal.** A saved state that every requirement lab starts from.

1. Save the configuration of `fmg-203` off the unit.

   ```text
   execute backup all-settings sftp 10.200.2.60 <FILE> <USER> <PASSWORD>
   ```

2. Snapshot `fmg-203`, and `fgt-202` in its managed state. Name each snapshot `baseline-203`. If `fgt-202` also serves Volume CCII, keep its `baseline-202` snapshot as well.
3. To reset between labs, restore the `baseline-203` snapshots. Put back by hand anything a lab changed on a reused host of Volume CCI or on `mail-202`.
4. In `evidence/` on `admin-201`, add a text file with the release and the build of `fmg-203`, its license, the hypervisor, and where the lab's secrets are stored, not their values.

**Expected result.** After a reset, the checks under *Validation and Troubleshooting* pass without an edit.

### Cleanup

When a run of labs ends, delete the lab's secrets from every host, remove the client entries for `10.200.2.130` from the reused servers if the unit will not return, remove the central management setting from `fgt-202` if it goes back to Volume CCII alone, and shut the virtual machines down.

## Lab Verification

Complete this sign-off once Labs 999.1 to 999.4 have been run end to end. Until then, the lab is unverified: this chapter was written from Chapter 01 and from the Chapter 999 of Volumes CCI and CCII, and no host of it has been built.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter adds a FortiManager-VM on release 7.6 to the lab network of Volume CCI, gives it the FortiGate-VM of Volume CCII to manage, and reuses the mail server of that volume and the authentication, time, logging, file, and certificate hosts of Volume CCI. It names the host or service behind each prerequisite of Chapter 01, and it takes the `baseline-203` snapshots that every requirement lab returns to.

- [ ] Has made `fmg-203` a client of the reused servers.
- [ ] Has deployed `fmg-203`, activated its license, and limited its port to HTTPS and SSH.
- [ ] Has authorized `fgt-202` in the ADOM `lab-203`, and has a mail server ready.
- [ ] Has taken the `baseline-203` snapshots and can reset to them.
