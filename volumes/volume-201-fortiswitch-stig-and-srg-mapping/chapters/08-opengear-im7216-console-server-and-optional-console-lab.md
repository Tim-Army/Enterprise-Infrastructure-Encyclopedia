# Chapter 08: OpenGear IM7216-2-DAC-LMV Console Server (Firmware 5.5.3) and Optional Console Lab

## Learning Objectives

- Describe what an OpenGear IM7216-2-DAC-LMV running firmware 5.5.3 can do: serial console access, remote authentication, logging, monitoring, out-of-band paths, and cellular failover.
- Place the console server in the Chapter 999 lab without changing the `10.201.0.0/16` and `fd00:db8:201::/112` address plans.
- Cable and configure serial ports so each FortiSwitch console is reachable over SSH through the console server.
- Authenticate console users against the lab RADIUS servers, limit each group to its own ports, and keep a local emergency account.
- Send console logs, time, and SNMP traffic to the lab services, and harden the console server's own services.
- Recover a FortiSwitch from a lost management path by using only the serial console.

## Theory and Architecture

### Why a console server in this lab

Every lab in Chapters 04 to 07 reaches the switches over the network, through the management SVI on segment 30 or the management port on segment 0. That path fails in exactly the situations where an administrator most needs access: a bad VLAN change, a wrong routing key, a lost management address, or a switch that is booting. A console server keeps a second path alive. It connects to each device's serial console and offers that console over SSH, so an administrator can still log in when the data network is down.

The console server is **optional**. Chapters 04 to 07 and the labs in Chapter 999 run without it. Add it when you want to test console access, out-of-band management, or recovery, or when your lab switches sit in a rack you cannot reach.

### The device

The IM7216-2-DAC-LMV belongs to Opengear's IM7200 infrastructure manager family. Opengear's own part numbers carry a `-2-` after the port count, so this chapter uses the full `IM7216-2-DAC-LMV`. The name breaks down as follows, based on Opengear's Quick Start and retailer listings:

| Part of the name | Meaning |
| --- | --- |
| `IM7216` | IM7200 family, 16 serial ports |
| `-2` | Two network ports (NET1 and NET2) |
| `DAC` | Dual AC power supplies with automatic failover |
| `LMV` | The cellular variant. Retailer listings associate `-LMV` with a Verizon LTE modem. Read the SKU label on your unit to confirm the carrier and region. |

| Capability | What the device provides |
| --- | --- |
| Serial ports | 16 RJ45 RS-232 ports, numbered 1 to 16. The pinout is selectable per port: `X2` (Cisco Straight, the default) or `X1` (Cisco Rolled). |
| Network ports | NET1 and NET2. Each is a logical port with a copper 10/100/1000 connection and an SFP slot. Only one of the two is active at a time: with no SFP module the copper port works, and inserting an SFP module activates the SFP and turns the copper port off. |
| Other connectors | A local console port, two USB ports (USB consoles, or flash drives for firmware and configuration files), a modem connector, and SMA antenna connectors for the cellular modem. |
| Power | Two internal universal AC supplies with automatic failover. |
| Storage | Retailer listings and Opengear's IM7200 data sheet list 16 GB of internal flash. |
| Cellular | An internal LTE modem for out-of-band access and failover. It needs a SIM and a carrier plan. |

Hardware details above come from the IM7200 Quick Start (revision 1.5) and from retailer listings, not from a unit in this lab. Check each one against your device and its data sheet.

### What firmware 5.5.3 is

Firmware 5.5.3 was released in October 2026. Opengear classifies it as a **patch release**: it carries security and defect fixes and no new feature set. The same 5.x firmware supports the IM7200, CM7100, CM7196, and ACM700x families. The release notes list no known issues for 5.5.3.

The 5.5.3 release notes record these changes:

| Area | Change in 5.5.3 |
| --- | --- |
| IPsec | The web UI now selects Phase 1 and Phase 2 ciphers and algorithms separately, and hides fields that do not apply. |
| Passwords | A configurable password complexity policy is available on the Authentication page and in the REST API. |
| Secrets in the configuration | Password obfuscation now also covers PPP (dial-in and PPTP) and EAPoL (802.1X) secrets. The option moved from the Authentication page to the System page, and permissions on AAA files that hold secrets were tightened. |
| Web service | The web server version is no longer reported in response headers. New fields set Cherokee `keepalive_max_requests` and a per-source connection rate limit. |
| Monitoring | `nagios-plugins` was upgraded to 2.4.12, with more checks configured in `nagios_check.xml`. A fix lets an SNMP walk read the `ogPowerSupplyTable` power-supply status. |
| Security fixes | A potential heap overflow in a multipart web request was fixed. OpenSSH, strongSwan, libexpat, ISC DHCP, and json-c were upgraded. CVE remediation details are in the Opengear portal. |

Earlier 5.x releases matter for upgrades:

- **Upgrade path.** A CM71xx or IM72xx must run a 4.13.x release at or after 4.13.3 before it upgrades to 5.0.0 or later.
- **Backups.** A backup file from a different major version is no longer applied, so take a new backup after every successful upgrade. To go back to 4.x, re-apply a 4.x backup.
- **FIPS mode.** The FIPS provider no longer permits 1024-bit OpenSSL keys, so every 1024-bit web certificate request becomes 2048 bits. The OpenSSL MD5 digest is not available in FIPS mode from 5.1.0.
- **Lighthouse.** A security change can stop a device from enrolling when the Lighthouse VPN server certificate is signed with SHA-1.
- **Kernel.** Release 5.0.0 changed the Linux kernel, and Opengear advises validating on a few devices before a wide rollout.

### What the console server does

The device does the following, according to the Quick Start, the 5.5.3 release notes, and the product family manuals. Menu names and some options vary by release, so confirm each against the 5.5.3 web UI.

1. **Serial console access.** Each serial port is set to a mode (the default is Infrastructure Manager mode), a baud rate, parity, data bits, stop bits, and flow control. A port is offered over SSH, Telnet, a web terminal, and RFC 2217. SSH to TCP port `3000` plus the port number (for example `3001` for port 1), or add the port to the user name, such as `user:port01`. Telnet uses `2000` plus the port number.
2. **Access control.** Local users and groups, and a list of ports each user may reach. The `admin` group grants the management UI and CLI.
3. **Remote authentication.** Local, RADIUS, TACACS+, and LDAP, with group support. The ACM7000 manual, for the same software family, also covers Kerberos.
4. **Port logging.** A logging level per port records the data sent in each direction.
5. **Firewall and services.** A built-in firewall. By default only HTTPS and SSH reach the device itself, and the Service Access settings control the rest.
6. **Management LAN.** NET2 can serve as a separate management LAN gateway, a failover or out-of-band interface, or a redundant link that shares NET1's settings through interface aggregation.
7. **Out-of-band and failover.** Cellular failover, and dial-in access through the modem connector on models that have one.
8. **Monitoring and time.** NTP, remote syslog, SNMP (v1, v2c, v3), and Nagios-style checks.
9. **Tunnels and fleet management.** IPsec and OpenVPN, and enrollment in Opengear Lighthouse.
10. **Automation.** A REST API, USB-stick configuration loading, and configuration backup and restore.

### Where it fits in the SRG labs

This volume maps FortiSwitch to the SRGs. It does not assess the console server. A console server is a network device with management interfaces, so the Network Device Management SRG applies to it the same way. The table points to the existing labs whose controls show the same ideas on the console server.

| Console server control | Matching lab |
| --- | --- |
| Roles, trusted sources, and services | Lab 5.1 |
| Lockout, banner, and session timeout | Lab 5.2 |
| Password policy | Lab 5.3 |
| Audit events, time stamps, and off-load to two log servers | Labs 5.4 to 5.6 |
| FIPS mode, strong ciphers, SNMPv3 | Lab 5.7 |
| Central authentication and a unique shared secret per client | Labs 5.8 and 7.4 |
| Configuration backup and supported releases | Lab 5.9 |

## Design Considerations

- **One address plan.** The console server uses the existing plan. It joins segment 0 (the out-of-band management network) at `.13`, which the host table already reserves for infrastructure that shares the segment (`.11` and `.12` are the switches). The IPv6 host part is the same hexadecimal as the IPv4 host part, so `.13` is `::d`.
- **One new segment.** Break-glass access needs a path that does not depend on gw-201, so the lab takes the first free lab-specific segment, **segment 100** (`10.201.100.0/24`, `fd00:db8:201::6400/120`, no gateway). NET2 sits on it at `.2` and the break-glass laptop `oob-admin-201` at `.10`. Chapter 999 reserves segments 100 to 199 for this purpose and lists segment 100 in its segment table.
- **No forwarding between networks.** The console server is not a router in this lab. NET2 stays on its own LAN, and the device's firewall does not forward between NET1 and NET2.
- **Segment 0 stays out of band.** Chapter 999 says segment 0 carries no test traffic. The console server adds only management and console traffic there.
- **Unique secrets.** The console server is a RADIUS client, so it gets its own shared secret in `clients.conf`, never the one a switch uses (Lab 7.4).
- **A local emergency account.** Remote authentication fails when RADIUS is unreachable, which is the situation the console server exists for. Keep one local administrator, stored offline, and test it (Lab 8.3).
- **Pinout is per cable.** Console cables vary by vendor. Start with `X2` and switch a port to `X1` if the terminal stays silent.

## Implementation and Automation

All settings come from the 5.5.3 web UI. The Quick Start for the IM7200 names the menus (for example *Serial & Network: Serial Port* and *System: IP*), but that document is revision 1.5 and older than 5.5.3, so a menu may sit in a different place. Record the exact path you used in the evidence folder.

| Item | Lab value |
| --- | --- |
| Host name | `og-201` |
| NET1 (segment 0) | `10.201.0.13/24`, gateway `10.201.0.1`; `fd00:db8:201::d/120`, gateway `fd00:db8:201::1` |
| NET2 (segment 100) | `10.201.100.2/24`; `fd00:db8:201::6402/120`; no gateway |
| Break-glass laptop | `oob-admin-201`, `10.201.100.10`, `fd00:db8:201::640a` |
| Serial port 1 | `sw-648f-1` console |
| Serial port 2 | `sw-2048f-1` console |
| Serial port 3 | `fgt-201` console, only if the FortiGate is hardware |
| Serial port 16 | Loopback test cable |
| Console speed | `115200` baud, 8 data bits, no parity, 1 stop bit, no flow control (FortiSwitchOS 7.6.7 default for `config system console`) |
| Services | RADIUS `10.201.10.10` and `.11`; syslog `.20`; NTP `.30` and `.31`; SNMPv3 manager `10.201.10.40` |

Automation is limited on purpose. The REST API and a configuration file loaded from a USB stick can repeat a build, but this chapter configures the device by hand so each setting is visible. Save the exported configuration after each lab (Lab 8.7) so the baseline can return.

## Validation and Troubleshooting

Before each lab, check the path in this order: power and link lights, `ping 10.201.0.13` from `admin-201`, then an SSH login to the console server. After each lab, restore the saved configuration.

| Symptom | Cause | Fix |
| --- | --- | --- |
| The console shows nothing | The port pinout does not match the cable | Switch the port between `X2` (Cisco Straight) and `X1` (Cisco Rolled) and press Enter |
| The console shows garbage | The port baud rate differs from the switch | Set `115200` on the port, or read the switch's `config system console` value |
| `Permission denied` on a port | The user's group has no access to that port | Add the port to the group under *Users & Groups* |
| SSH to `3001` times out | The firewall or Service Access blocks the source, or SSH is off | Allow SSH from the admin network (Lab 8.5) |
| RADIUS logins fail | The shared secret differs, or gw-201 blocks the path | Match the secret in `clients.conf`, and allow UDP 1812 and 1813 from `10.201.0.13` |
| Logins work with RADIUS up and fail with it down | No local fallback | Keep the local administrator and test it (Lab 8.3) |
| The copper port stopped working | An SFP module is in the same NET port | Remove the module, or move the cable to the SFP |
| No cellular registration | No SIM, no plan, or no antenna | Install the SIM and antennas, and check carrier status |

## Security and Best Practices

- Change the factory password at the first login and create a named administrator for daily use. Release 5.5.3 does not let you set the password `default` or close variants (a restriction listed in the 5.5.0 release notes).
- Keep the console server off any production network. Segment 0 and segment 100 are lab segments.
- Turn off Telnet and any other clear-text service. Allow SSH and HTTPS only from the admin network and segment 100.
- Give the device a unique RADIUS secret and a unique SNMPv3 user. Do not reuse a switch's secret.
- Turn on the password complexity policy in 5.5.3 and the configuration-secret obfuscation on the System page.
- A console log can hold secrets that appear on the console. Send port logs to the lab log server and protect them like an audit log.
- Back up the configuration before every firmware change and after every successful upgrade, and apply the 4.13.3 or later 4.13.x step before any move to 5.x from 4.x.
- Read the FIPS notes before enabling FIPS mode: it changes accepted keys and algorithms.
- Treat the cellular link as an internet path. Leave it off unless a lab uses it, and never route lab traffic over it.

## References and Knowledge Checks

**References:**

- Opengear, [firmware 5.5.3 release notes](https://ftp.opengear.com/download/opengear_appliances/ACM/current/release-notes.pdf) (IM7200, CM7100, CM7196, ACM700x), October 2026 revision.
- Opengear, [IM7200 Quick Start](https://ftp.opengear.com/download/documentation/quickstart/x-quickstart/IM7200%20Quick%20Start.pdf), revision 1.5 (older than 5.5.3).
- Opengear, [IM7200 Infrastructure Manager data sheet](https://opengear.com/wp-content/uploads/2020/07/Spanish-Mexico_IM7200_Infrastructure_Manager-Data_Sheet-1.pdf) (Spanish edition).
- Opengear documentation, [opengear.com/documentation](https://opengear.com/documentation), for the current user manual and Knowledge Base.
- [Chapter 999](999-shared-lab-infrastructure.md) for the address plan, hosts, and baseline. [Chapter 05](05-network-device-management-srg-requirement-labs.md) and [Chapter 07](07-aaa-services-srg-requirement-labs.md) for the matching SRG labs.
- FortiSwitchOS 7.6.7 CLI Reference, `config system console`.

**Knowledge checks:**

1. Why does the lab put the console server on segment 0 and add a separate segment 100 for NET2?
2. A switch console shows garbage after you connect. List two settings to check, in order.
3. What does a user need, in addition to a valid password, to open a session on serial port 2?
4. Why must the console server keep a local administrator when it uses RADIUS?
5. What is the upgrade path from firmware 4.x to 5.5.3, and what happens to a 4.x backup file on 5.x?
6. Which two things in the 5.5.3 release notes change how stored secrets and passwords are protected?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 (Labs 999.1 to 999.6), including gw-201 routing between segment 0 and segment 10, the RADIUS, syslog, NTP, and SNMP hosts, and the `baseline-201` snapshot. One IM7216-2-DAC-LMV running firmware 5.5.3, RJ45 console cables for each device you connect (the FortiSwitch console cable, or the adapters in the console server kit), a spare laptop for `oob-admin-201`, and a loopback test cable. A SIM and a carrier plan are needed only for the optional cellular step. **Cost:** the console server and, if you want Lab 8.6's cellular step, a data plan.

![Console access for the optional lab. The OpenGear console server og-201 connects NET1 (10.201.0.13) to segment 0, where gw-201 and the management ports of sw-648f-1 and sw-2048f-1 sit. Administrators on segment 20 reach og-201 through gw-201 and use SSH to TCP port 3000 plus the serial port number. og-201 reaches RADIUS, syslog, NTP, and SNMP on segment 10 through gw-201. NET2 (10.201.100.2) joins segment 100, an isolated break-glass network with no gateway, where oob-admin-201 (10.201.100.10) sits. Serial ports 1, 2, and 3 connect to the consoles of sw-648f-1, sw-2048f-1, and the optional fgt-201, and an optional cellular link provides failover.](../../../diagrams/volume-201-fortiswitch-stig-and-srg-mapping/chapter-08-console-access-topology.svg)

### Lab 8.1 — Install the console server on segment 0

**Goal.** Put `og-201` on the lab network at `10.201.0.13` and `fd00:db8:201::d`, on firmware 5.5.3, with the factory credentials replaced.

**Uses.** `og-201`, a laptop on `192.168.0.0/24` for the first login, `gw-201`, `admin-201`.

**Configure.**

1. Rack the unit, connect both power cords, and connect NET1 to the segment 0 network (the same switch or cable path that carries the switch management ports). Leave NET2 unplugged for now.
2. Browse to `https://192.168.0.1` from a laptop in `192.168.0.0/24` and sign in with the factory user. Change that password at once. A DHCP client is on by default, so the unit also answers at any DHCP address it received.
3. Create a named administrator in the `admin` group, sign out, and sign back in as that user.
4. Set the host name `og-201`. Under the network settings for NET1, choose a static configuration:

   ```text
   NET1 IPv4:  10.201.0.13  netmask 255.255.255.0  gateway 10.201.0.1
   NET1 IPv6:  fd00:db8:201::d  prefix 120  gateway fd00:db8:201::1
   DNS:        10.201.10.1
   ```

5. Check the firmware version in the system status. It must read 5.5.3. If it reads 4.x, first move to the last 4.13.x release (4.13.3 or later), take a backup, and then upgrade to 5.5.3, as the release notes require. Take a new backup after the upgrade.
6. Add `og-201` to the host list on `admin-201` and give it a DNS name if the lab has one.

**Positive test.** From `admin-201`, `ping 10.201.0.13` and `ping -6 fd00:db8:201::d` succeed, and `ssh <admin>@10.201.0.13` opens the console server shell. The web UI answers on `https://10.201.0.13`.

**Negative test.** Try to sign in with the factory credentials: it fails. Try to set the new administrator's password to `default`: the device refuses it.

**Evidence.** The status page showing firmware 5.5.3, the NET1 settings, the ping and SSH output, and the refused factory login.

**Return to baseline.** Export the configuration as `og-201-8.1.config` and keep it in the evidence folder (Lab 8.7 restores from it).

### Lab 8.2 — Serial access to both switches

**Goal.** Open each switch's console through the console server over SSH, with the right serial settings, and show that a bad setting fails visibly.

**Uses.** `og-201`, `sw-648f-1`, `sw-2048f-1`, `admin-201`, the loopback test cable on port 16.

**Configure.**

1. Cable serial port 1 to the console port of `sw-648f-1`, port 2 to `sw-2048f-1`, and port 3 to `fgt-201` if it is hardware. Plug the loopback cable into port 16.
2. For each port, open the serial port settings and set:

   ```text
   Label:           sw-648f-1          (port 1)
                    sw-2048f-1         (port 2)
                    fgt-201            (port 3)
   Mode:            Infrastructure manager (console server)
   Pinout:          X2 (Cisco Straight); use X1 if no output appears
   Baud rate:       115200
   Data bits:       8
   Parity:          none
   Stop bits:       1
   Flow control:    none
   Protocols:       SSH
   Logging level:   all data
   ```

3. Confirm the switch side. On each switch run `show system console` (or `get system console`) and write down the baud rate. If it differs from `115200`, either set the port to match or change the switch with `config system console` and `set baudrate 115200`.
4. Turn off Telnet and web terminal on each port if you do not need them.

**Positive test.** From `admin-201`:

```text
ssh -p 3001 <admin>@10.201.0.13       (port 1, sw-648f-1)
ssh <admin>:port02@10.201.0.13        (port 2, sw-2048f-1)
```

Press Enter at the console. The FortiSwitchOS login prompt appears. Log in, run `get system status`, and log out. Run the same test on port 2. Then press Enter on the loopback port from a second session and type text: the text echoes back.

**Negative test.** Change port 1's baud rate to `9600` and reconnect: the console shows garbage or nothing. Switch the pinout to the other mode and repeat to see the effect, then restore `X2` and `115200`. Open a second session to port 1: record whether the console server permits a second session or shows the first user's activity (this depends on port mode and settings).

**Evidence.** Both port settings pages, the login prompt from each switch, the loopback echo, and the garbage output with the wrong baud.

**Return to baseline.** Restore the baud rates and pinouts, and save the configuration.

### Lab 8.3 — Authenticate console users against RADIUS

**Goal.** Make the console server use the lab RADIUS servers for logins, limit each group to its own ports, and keep a tested local emergency account.

**Uses.** `og-201`, `radius-201a` and `radius-201b` (P1, P2), `gw-201`, `admin-201`.

**Configure.**

1. Create a unique shared secret for `og-201` (Chapter 999's rule: one key per client, never reused). On `radius-201a` and `radius-201b`, add the console server as a client in `/etc/freeradius/3.0/clients.conf`:

   ```text
   client og-201 {
       ipaddr = 10.201.0.13
       ipv6addr = fd00:db8:201::d
       secret = <KEY_OG>
       shortname = og-201
   }
   ```

   Restart `freeradius` on both servers. On `gw-201`, allow UDP 1812 and 1813 from `10.201.0.13` to `10.201.10.10` and `10.201.10.11`.

2. On the console server, create groups named `netops` (access to ports 1 and 2) and `audit` (no ports). Keep the built-in `admin` group for the administrators.
3. Under the authentication settings, set the method to RADIUS first with local as the fallback. Enter both servers, the secret, the authentication port 1812, and the accounting port 1813.
4. Create two RADIUS users, `lab-netops` and `lab-audit`, and map them to the groups (the device maps a RADIUS user to a group by user name or by a returned group attribute; use the method your 5.5.3 UI offers and note which one).
5. Keep one local administrator and store its password offline. Do not rely on it for daily work.

**Positive test.** Sign in as `lab-netops` over SSH. Open port 1 and port 2: both open. Sign in as `lab-audit`: the console server accepts the login but offers no serial ports. The FreeRADIUS log shows each request from `og-201` with an Access-Accept.

**Negative test.** Sign in as `lab-netops` and try port 3: refused. Enter a wrong password: Access-Reject. Stop `freeradius` on both servers and sign in with the local administrator: the login works through the fallback. Restart `freeradius`.

**Evidence.** The authentication settings, the group-to-port table, the FreeRADIUS accept and reject lines, and the local fallback login with RADIUS down.

**Return to baseline.** Restore the saved configuration, and keep the client entry in `clients.conf` for later labs.

### Lab 8.4 — Logs, time, and SNMP

**Goal.** Send the console server's logs and each port's console log to the lab syslog server, set its clock from the lab NTP servers, and let `nms-201` read it with SNMPv3.

**Uses.** `og-201`, `syslog-201a` (P4), `ntp-201a` and `ntp-201b` (P5), `nms-201` (P6).

**Configure.**

1. Set the time zone and enter both NTP servers, `10.201.10.30` and `10.201.10.31`, with the authentication keys from Chapter 999 if the device supports keyed NTP.
2. Set the remote syslog server to `10.201.10.20` and use TCP if the 5.5.3 UI offers it. On `gw-201`, allow the syslog port from `10.201.0.13`.
3. On each serial port, keep the logging level at all data and send the log to syslog.
4. Under SNMP, enable SNMPv3 and create one user with authentication and privacy keys (generate unique keys per Chapter 999). Disable SNMPv1 and v2c. Allow `10.201.10.40` to query.

**Positive test.** The console server's time matches `ntp-201a` (compare `date -u` on both). Open and close a session on port 1: `/var/log/lab201/` on `syslog-201a` holds the login, logout, and console lines. From `nms-201`:

```text
snmpwalk -v3 -l authPriv -u <SNMP_USER> -a SHA -A <AUTH_KEY> -x AES -X <PRIV_KEY> 10.201.0.13 system
```

The walk returns the system group. Also walk the power-supply table (the 5.5.3 release notes record a fix so `ogPowerSupplyTable` returns supply status).

**Negative test.** Query with SNMPv2c and a community string: no answer. Query with a wrong privacy key: authentication error. Block UDP 514 or the syslog TCP port on `gw-201` briefly: the device logs locally, and the evidence shows the gap, which you close by restoring the rule.

**Evidence.** The time comparison, the syslog lines, the successful and failed SNMP queries, and the power-supply table output.

**Return to baseline.** Keep NTP and syslog settings. Restore the SNMP settings from the saved configuration if you changed them.

### Lab 8.5 — Harden the console server's own services

**Goal.** Reduce the device's exposed services to SSH and HTTPS from the admin network, set a password policy, and prove that everything else is closed.

**Uses.** `og-201`, `admin-201` (segment 20), `attacker-201` (segment 42), `oob-admin-201` (Lab 8.6).

**Configure.**

1. Under service access, leave HTTPS and SSH enabled and turn off Telnet, HTTP, and any other service you do not need (including serial-port Telnet and RFC 2217 unless a lab uses them).
2. Restrict the source of SSH and HTTPS to `10.201.20.0/24` and, after Lab 8.6, `10.201.100.0/24`. Use the device's firewall rules for this.
3. Set a web session timeout and an SSH idle timeout, and add a login banner.
4. Turn on the password complexity policy that 5.5.3 adds under the authentication settings (length, character classes), and turn on configuration-secret obfuscation on the System page.
5. Check the web certificate. If the default certificate is in use, replace it with one signed by `ca-201` (the lab CA from P3). A certificate request in FIPS mode produces a 2048-bit key at minimum.

**Positive test.** From `admin-201`, `nmap -p 22,23,80,443 10.201.0.13` shows 22 and 443 open and 23 and 80 closed. The banner appears on SSH login.

**Negative test.** Run the same scan from `attacker-201` on segment 42: the console server drops the traffic. Try to set a short password for a test user: the policy refuses it. Let an SSH session sit past the idle timeout: the device closes it.

**Evidence.** Both `nmap` scans, the firewall and service settings, the refused weak password, and the closed idle session.

**Return to baseline.** Keep this configuration for the remaining labs.

### Lab 8.6 — Break-glass access on segment 100 (and optional cellular failover)

**Goal.** Reach a switch console when the data network path to `og-201` is down, using NET2 on the isolated segment 100, and, if a SIM is available, show the cellular path.

**Uses.** `og-201` NET2, `oob-admin-201` (a laptop), `sw-648f-1`, `gw-201`.

**Configure.**

1. Connect NET2 to a switch or cable that carries only segment 100. Connect `oob-admin-201` to the same segment.
2. On the console server, enable the NET2 interface and give it the static settings with no gateway:

   ```text
   NET2 IPv4:  10.201.100.2  netmask 255.255.255.0   (no gateway)
   NET2 IPv6:  fd00:db8:201::6402  prefix 120         (no gateway)
   ```

   Keep NET2 as an interface of its own. Do not turn on aggregation with NET1, and do not enable forwarding between NET1 and NET2.
3. On `oob-admin-201`, set `10.201.100.10/24` and `fd00:db8:201::640a/120`.
4. Allow SSH on NET2 from `10.201.100.0/24` in the firewall rules from Lab 8.5.
5. **Optional cellular.** Install the SIM and antennas, enter the carrier's APN under the cellular settings, and set the failover to use the cellular interface with a probe address of `10.201.0.1` (gw-201). Verify the carrier's data plan allows a management connection before you enable it.

**Positive test.** Disconnect the NET1 cable. From `oob-admin-201`:

```text
ping 10.201.100.2
ssh -p 3001 <admin>@10.201.100.2
```

The session opens the `sw-648f-1` console even though NET1 is down. Run `get system status` in the console, then log out. Reconnect NET1.

**Optional cellular test.** With NET1 and NET2 both disconnected, wait for the probe to fail. The cellular status shows an address, and an SSH login over the cellular address reaches the console server. Record the failover time.

**Negative test.** From `oob-admin-201`, try to reach `10.201.10.10` or `10.201.0.1`: no route, because NET2 does not forward and has no gateway. From a host on segment 20, try `10.201.100.2`: no route either.

**Evidence.** The NET2 settings, the NET1-down SSH session, the failed attempts to cross segments, and, for the optional step, the cellular status and failover time.

**Return to baseline.** Reconnect NET1, remove the cellular failover setting if you do not need it, and restore the saved configuration.

### Lab 8.7 — Recover a switch from a lost management path

**Goal.** Break the management path to a switch on purpose, recover it using only the console server, and return the lab to its baseline.

**Uses.** `og-201`, `sw-648f-1`, `admin-201`, the `baseline-201` snapshot.

**Configure.**

1. Export the configuration of `og-201` and save a copy of the switch's current configuration with `show full-configuration` through the serial console, so the recovery has a known good source.
2. From the serial console of `sw-648f-1`, change the management SVI on segment 30 so it stops answering:

   ```text
   config system interface
       edit mgmt-svi
           set ip 10.201.30.99/24
   end
   ```

   The address on segment 30 is now `10.201.30.99`, so `10.201.30.11` no longer answers.
3. Confirm that the in-band path is gone from `admin-201`: `ping 10.201.30.11` fails and SSH to `10.201.30.11` times out.
4. Recover through the console server. Open the port 1 session and restore the address:

   ```text
   config system interface
       edit mgmt-svi
           set ip 10.201.30.11/24
   end
   ```

5. Save the recovered switch configuration, and export the console server configuration again as `og-201-8.7.config`.

**Positive test.** After step 4, `ping 10.201.30.11` and SSH from `admin-201` work again. The log on `syslog-201a` shows the serial login, the change, and the logout under the user's name.

**Negative test.** Sign in to the console server as `lab-audit` and try to open port 1: refused. Try the recovery as `lab-netops` from `oob-admin-201` with RADIUS stopped: the login fails, and the local administrator is the only way in, which is why Lab 8.3 keeps one.

**Evidence.** The ping failures before recovery, the recovery commands from the serial session, the ping successes afterward, the syslog lines, and the two exported configurations.

**Return to baseline.** Restore the `baseline-201` snapshot and the switch configuration (Lab 999.6), and restore the console server from `og-201-8.1.config` if you want the factory-fresh state for the next run.

## Lab Verification

Complete this sign-off once Labs 8.1 to 8.7 have been run end to end, including each negative test, on a real IM7216-2-DAC-LMV running firmware 5.5.3. Until then, the labs are unverified. The hardware facts in this chapter come from Opengear's release notes, the IM7200 Quick Start (revision 1.5), and retailer listings, and menu names may differ in 5.5.3. The optional cellular step is not verified at all.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter describes the OpenGear IM7216-2-DAC-LMV on firmware 5.5.3 and adds it to the Chapter 999 lab as an optional console path. It uses the existing `10.201.0.0/16` and `fd00:db8:201::/112` plans, puts the console server on segment 0 at `.13`, and adds one new segment, 100, for break-glass access. Seven labs cover installation, serial access, RADIUS logins, logging, hardening, break-glass and cellular access, and recovery.

- [ ] Has `og-201` on segment 0 at `10.201.0.13` and `fd00:db8:201::d`, running firmware 5.5.3.
- [ ] Has opened both switch consoles over SSH through the console server.
- [ ] Has tested RADIUS logins, a group limited to its ports, and the local fallback.
- [ ] Has sent logs, time, and SNMPv3 to the lab services.
- [ ] Has closed every service except SSH and HTTPS from the admin network.
- [ ] Has reached a switch console over NET2 with the in-band path down.
- [ ] Has recovered a switch from a lost management path and restored the baseline.
