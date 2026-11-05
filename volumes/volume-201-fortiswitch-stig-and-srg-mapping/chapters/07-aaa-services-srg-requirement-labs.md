# Chapter 07: AAA Services SRG Requirement Labs

## Learning Objectives

- Prove all seven AAA Services SRG requirements in the crosswalk on the Chapter 999 lab.
- Explain why AAA Services requirements are met by the authentication system, with the switch as a client.
- Configure RadSec (RADIUS over TLS) on FortiSwitchOS and the RADIUS server, with certificate validation.
- Show with a capture that credentials are encrypted in transit and that an untrusted server is refused.

## Theory and Architecture

The AAA Services SRG applies to the authentication, authorization, and accounting service itself, for example a RADIUS or TACACS+ server, not to the network device that uses it. Chapters 01 and 02 decided that AAA Services is **inherited**: the authentication system is assessed on its own, and a FortiSwitch inherits its controls. Seven crosswalk requirements still land on the switch, because the switch is the client that sends credentials to the server and the authenticator for 802.1X. Two ask that credentials are encrypted in transit using FIPS-validated cryptography and with a protocol that encrypts them; FortiSwitchOS meets both with RadSec, which carries RADIUS inside a TLS session (Lab 7.1). Three ask that 802.1X identify and authenticate each endpoint before it connects, using a secure EAP type (Lab 7.2). One asks for automated account management, which RADIUS accounting supports (Lab 7.3), and one asks for a unique shared secret for each client (Lab 7.4). This chapter proves the switch side and the server side together on the lab from [Chapter 999](999-shared-lab-infrastructure.md).

### Requirements and labs

The crosswalk lists 7 distinct AAA Services SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 7.1 | 2 | Requirement lab: Encrypt RADIUS credentials with RadSec (TLS) |
| 7.2 | 3 | Requirement lab: 802.1X on the authentication server: unique identification, authentication, and EAP type |
| 7.3 | 1 | Requirement lab: Automated account management with RADIUS accounting |
| 7.4 | 1 | Requirement lab: Unique shared secret for each RADIUS and TACACS+ client |

Every requirement here has a FortiSwitch setting or a procedure behind it, so this chapter has requirement labs only. Each lab configures the setting, proves it with a positive test, and proves the control with a negative test.

## Design Considerations

- **Inherited does not mean untested.** The switch has to be configured to use the encrypted transport, and a lab proves it does.
- **Both ends matter.** RadSec needs the server to listen for TLS and require a client certificate, as well as the switch to validate the server.
- **A lab CA proves the mechanism only.** `ca-201` is not the DoD CA, so the lab cannot show DoD trust.
- **FIPS-validated crypto depends on mode.** The strong-cryptography and FIPS-CC settings in Lab 5.7 decide which algorithms the TLS session may use.

## Implementation and Automation

The lab follows Lab 999.2 (service hosts and certificates) and Lab 999.4 (RADIUS on the switch). Switch commands come from the crosswalk workbook (FortiSwitchOS 7.6.7 syntax). Save evidence in `evidence/<lab>/<date>/` on `admin-201`.

## Validation and Troubleshooting

Before the lab, confirm that a UDP RADIUS login works (Lab 999.4). After it, restore the baseline.

| Symptom | Cause | Fix |
| --- | --- | --- |
| The TLS session never starts | The server is not listening on 2083, or the firewall policy blocks it | Check `ss -ltn` and add port 2083 to the gateway policy |
| The switch rejects the server | The name in `radsec-cert-cn-dns` does not match the certificate, or the CA is not imported | Match the name and import the CA |
| The server rejects the switch | The client certificate is missing or issued by another CA | Import the client certificate and check the CA file on the server |
| The login works over UDP but not TLS | The user is fine; the transport is the problem | Check the handshake in a capture |

## Security and Best Practices

- Never reuse a lab certificate or private key outside the lab.
- Keep private keys on the issuing host only, and delete them in the cleanup step.
- Treat a successful UDP fallback as a finding.
- Record the TLS version and cipher from the capture.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortiswitch-feature-version-and-srg-map.md) and [Chapter 02](02-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md) for the AAA decision and the RadSec row.
- [Chapter 999](999-shared-lab-infrastructure.md) for the lab network and services.
- [Chapter 05](05-network-device-management-srg-requirement-labs.md), Lab 5.7 and Lab 5.8, for cryptography and authentication servers.
- AAA Services SRG (DISA, V2R3 as compared with a third-party mirror; confirm against DISA's own file).
- FortiSwitchOS 7.6.7 CLI Reference, `config user radius`.

**Knowledge checks:**

1. Why is the AAA Services SRG inherited by the switch, and which seven requirements still apply to it?
2. What does RadSec add to RADIUS?
3. What does the switch validate about the server, and what does the server validate about the switch?
4. What can the lab CA prove, and what can it not?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999, the RADIUS servers from Lab 999.2, and the certificate authority `ca-201`. `tcpdump` on `radius-201a`. **Cost:** none beyond the Chapter 999 lab.

![Shared lab network from Chapter 999. Two FortiSwitches, sw-648f-1 and sw-2048f-1, are joined by routed link L5 and each has an 802.1Q trunk to a hypervisor that hosts the gateway, service hosts, certificate authority, DHCP server, administrator workstation, and two routing peers. Routed links L1 to L4 join each switch to each peer, an out-of-band management network joins the switch management ports to the gateway, and test endpoints connect directly to the switches.](../../../diagrams/volume-201-fortiswitch-stig-and-srg-mapping/chapter-999-shared-lab-topology.svg)

### Lab 7.1 — Encrypt RADIUS credentials with RadSec (TLS)

**Goal.** Show that the switch sends authentication traffic to the RADIUS servers inside a TLS session with certificate validation, and refuses a server it cannot validate.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000172-AAA-000520` | I | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p289 |
| `SRG-APP-000142-AAA-000020` | I | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p289 |

**Uses.** `sw-648f-1`, `radius-201a` with a RadSec (TLS) listener, `ca-201` (P3) to issue the server and client certificates, `syslog-201a` for the switch log.

AAA Services requirements are met by the authentication system, not by the switch alone. The switch side proves that it speaks RadSec and validates the server; the RADIUS server side proves that it accepts only TLS from the switch. The lab CA stands in for the DoD CA, so the lab proves the mechanism and not DoD trust.

**Configure.**

1. Issue a server certificate for `radius-201a` (name `radius-201a`) and a client certificate for the switch from `ca-201`. On the switch, import the CA certificate (see P3) and the client certificate.

2. On `radius-201a`, add a RadSec listener to FreeRADIUS: in `/etc/freeradius/3.0/sites-available/tls`, define a `listen` section with `proto = tcp`, `type = auth+acct`, `port = 2083`, and a `tls` block that names the server certificate, the private key, and the CA file, and that requires a client certificate. Enable the site, restart `freeradius`, and confirm with `ss -ltn` that port 2083 is listening.

3. Point the switch at the server using TLS, validate the server certificate, and require TLS 1.2 or later. Use the RadSec port and the client certificate.

   ```text
   config user radius
       edit radius-201a
           set transport-type TLS
           set radsec-tls-min-ver TLSv1-2
           set radsec-cert-validate enable
   end
   ```

4. Add the CA and the client certificate names to the same `config user radius` entry with `set radsec-server-ca-cert <CA_CERT>` and `set radsec-client-cert <CLIENT_CERT>`, and set `set radsec-cert-cn-dns radius-201a`.

**Positive test.** Log in with a RADIUS administrator. `tcpdump -n port 2083` on `radius-201a` shows a TLS handshake and encrypted application data, and no clear-text RADIUS on UDP 1812. The FreeRADIUS log shows the request arrived over TLS.

**Negative test.** Replace the server certificate with one signed by a different CA: the switch rejects the server and the login fails. Set `radsec-tls-min-ver TLSv1` on the server side only for a moment and confirm the switch still refuses anything below TLS 1.2. Send the switch's request over UDP 1812 with `transport-type UDP` to see the credentials in a capture, then restore TLS, which shows the difference the setting makes.

**Evidence.** The `config user radius` entry, the handshake capture, the FreeRADIUS TLS log, and the refused-server log line.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 7.2 — 802.1X on the authentication server: unique identification, authentication, and EAP type

**Goal.** Show that the switch and the RADIUS service identify each endpoint uniquely and authenticate it before any connection is established, and that the server accepts only a secure EAP method (EAP-TLS, EAP-TTLS, or PEAP).

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000158-AAA-000420` | II | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p127 |
| `SRG-APP-000394-AAA-000430` | II | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p127 |
| `SRG-APP-000516-AAA-000440` | II | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p127 |

**Uses.** `sw-648f-1`, `radius-201a` and `radius-201b` (P1, P2), `ca-201` (P3) for the server and client certificates, a laptop with a supplicant on `<PORT_EP1>`, and a second host on `<PORT_EP2>` for the MAC-based test. Workbook prerequisites: P1, P2 (P1 Reachable RADIUS or TACACS+ servers; P2 User group that lists the authentication servers).

The authenticator (the switch) and the authentication server (FreeRADIUS) share these requirements. Lab 4.1 proves the port behavior; this lab proves the server side and the choice of EAP method. `eap-passthru` lets the switch pass the EAP exchange to the server, which then decides the method. The lab CA stands in for the DoD CA, so the lab proves the mechanism and not DoD trust.

**Configure.**

1. Enable 802.1X port mode on the supplicant port, so no traffic passes until authentication succeeds.

   ```text
   config switch interface
       edit <PORT_EP1>
           config port-security
               set port-security-mode 802.1X
           end
           set security-groups lab-radius
   end
   ```

2. Enable MAC-based mode on the second port, so each endpoint is identified by its own address and a second device on the same port authenticates separately.

   ```text
   config switch interface
       edit <PORT_EP1>
           config port-security
               set port-security-mode 802.1X-mac-based
           end
           set security-groups lab-radius
   end
   ```

3. Let the switch pass the EAP exchange to the server.

   ```text
   config switch interface
       edit <PORT_EP1>
           config port-security
               set eap-passthru enable
           end
   end
   ```

4. On `radius-201a` and `radius-201b`, permit only secure EAP types: in `/etc/freeradius/3.0/mods-enabled/eap`, set `default_eap_type = tls`, keep the `tls-config`, `ttls`, and `peap` blocks, and remove or comment the `md5`, `leap`, and `gtc` blocks. Restart `freeradius`.

5. Issue a client certificate for the laptop from `ca-201` and set up the supplicant (`wpa_supplicant` with `eap=TLS`, or the operating system's 802.1X settings) to use it.

**Positive test.** Connect the laptop. `diagnose switch 802-1x status` lists the port as authorized only after the exchange, the FreeRADIUS log shows `EAP-TLS` and an Access-Accept, and the laptop receives a DHCP address. Before authentication, `ping` from the laptop to any host fails. On the MAC-based port, connect two hosts through a small switch: each is listed under its own MAC address.

**Negative test.** Configure a supplicant for EAP-MD5 or LEAP: the server rejects the method and the port stays unauthorized. Present a certificate from a different CA: Access-Reject. Connect a host without a supplicant: no traffic passes. Before any of these, confirm with a capture that no frame other than EAPOL reaches the network.

**Evidence.** `diagnose switch 802-1x status` before and after, the FreeRADIUS lines for the accepted and rejected methods, the EAPOL-only capture, and the list of EAP blocks that remain enabled.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 7.3 — Automated account management with RADIUS accounting

**Goal.** Show that the switch sends accounting records to the RADIUS server, so the server can record when remote accounts are used, and that account creation and removal happen on the server and take effect on the switch without a manual step.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000023-AAA-000030` | II | AAA Services must be configured to provide automated account management functions. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p289 |

**Uses.** `sw-648f-1`, `radius-201a` and `radius-201b` (P1), `syslog-201a`. Workbook prerequisites: P1 (P1 Reachable RADIUS or TACACS+ servers).

Account management is automated on the server: a user created, disabled, or removed in the directory behind RADIUS takes effect at the next logon with no change on the switch. The switch side proves that it sends the accounting records.

**Configure.**

1. Add the accounting server to the RADIUS entry.

   ```text
   config user radius
       edit radius-201a
           config acct-server
               edit 1
                   set status enable
                   set server 10.201.10.10
                   set secret <KEY_1>
           end
   end
   ```

2. On `radius-201a`, confirm that the detail accounting file is on (`/var/log/freeradius/radacct/<switch-ip>/detail-<date>`).

**Positive test.** Log in as a RADIUS administrator. The Accounting-Start record appears in the detail file with the user name and the switch address, and the Accounting-Stop record appears after logout. Create a new user on the server and log in with it with no change on the switch.

**Negative test.** Disable the new user on the server: the next logon fails, with no change on the switch. Stop `freeradius` accounting and log in again: the switch records no accounting for that session, which shows the server holds the record.

**Evidence.** The accounting detail records for one session, the user created and then disabled on the server, and the switch configuration unchanged between the two.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 7.4 — Unique shared secret for each RADIUS and TACACS+ client

**Goal.** Show that each switch uses its own shared secret with the authentication servers, and that one switch's secret does not work for another.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-APP-000516-AAA-000640` | II | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p289 |

**Uses.** `sw-648f-1`, `sw-2048f-1`, `radius-201a` (P1, P2), and the secret rule from Chapter 999 (one key per lab, never reused). Workbook prerequisites: P1, P2 (P1 Reachable RADIUS or TACACS+ servers; P2 User group that lists the authentication servers).

**Configure.**

1. Generate two different secrets, one per switch. On `radius-201a`, add each switch as a separate client in `clients.conf`, each with its own `secret`.

   ```text
   openssl rand -base64 24
   ```

2. On each switch, set that switch's secret on the RADIUS entry and then use the entry for administrator logins.

   ```text
   config user radius
       edit radius-201a
           set server 10.201.10.10
           set secret <KEY_1>
   end
   ```

3. Bind remote administrator logins to the server group.

   ```text
   config system admin
       edit admin-lab
           set remote-auth enable
           set remote-group lab-radius
   end
   ```

**Positive test.** Log in with a RADIUS administrator on both switches. The FreeRADIUS log shows each request under its own client name.

**Negative test.** Copy `sw-648f-1`'s secret to `sw-2048f-1` and log in: the server answers with a message authenticator error and the login fails. Set the same secret for both clients in `clients.conf` and note that the server cannot tell which switch is which, so the requirement is not met; restore the unique secrets.

**Evidence.** The two `clients.conf` entries with the secrets masked, the log lines for each client, and the failed login with the wrong secret.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

## Lab Verification

Complete this sign-off once Labs 7.1 to 7.4 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from the workbook's CLI-checked syntax and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the seven AAA Services SRG requirements that land on a FortiSwitch: RADIUS over TLS with certificate validation and a capture that shows the credentials are encrypted, 802.1X with a secure EAP type, RADIUS accounting for automated account management, and a unique shared secret for each client.

- [ ] Has a working RadSec login.
- [ ] Has a capture showing no clear-text RADIUS.
- [ ] Has shown the switch rejecting an untrusted server.
- [ ] Knows what the lab CA does not prove.
