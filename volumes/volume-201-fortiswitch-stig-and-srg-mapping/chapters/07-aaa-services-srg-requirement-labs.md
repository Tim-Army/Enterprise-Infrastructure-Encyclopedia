# Chapter 07: AAA Services SRG Requirement Labs

## Learning Objectives

- Prove both AAA Services SRG requirements in the crosswalk on the Chapter 999 lab.
- Explain why AAA Services requirements are met by the authentication system, with the switch as a client.
- Configure RadSec (RADIUS over TLS) on FortiSwitchOS and the RADIUS server, with certificate validation.
- Show with a capture that credentials are encrypted in transit and that an untrusted server is refused.

## Theory and Architecture

The AAA Services SRG applies to the authentication, authorization, and accounting service itself, for example a RADIUS or TACACS+ server, not to the network device that uses it. Chapters 01 and 02 decided that AAA Services is **inherited**: the authentication system is assessed on its own, and a FortiSwitch inherits its controls. Two crosswalk requirements still land on the switch, because the switch is the client that sends credentials to the server: they ask that credentials are encrypted in transit using FIPS-validated cryptography, and that protocols which encrypt credentials are used.

FortiSwitchOS meets both with RadSec, which carries RADIUS inside a TLS session. This chapter proves the switch side and the server side together on the lab from [Chapter 999](999-shared-lab-infrastructure.md).

### Requirements and labs

The crosswalk lists 2 distinct AAA Services SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 7.1 | 2 | Requirement lab: Encrypt RADIUS credentials with RadSec (TLS) |

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

1. Why is the AAA Services SRG inherited by the switch, and which two requirements still apply to it?
2. What does RadSec add to RADIUS?
3. What does the switch validate about the server, and what does the server validate about the switch?
4. What can the lab CA prove, and what can it not?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999, the RADIUS servers from Lab 999.2, and the certificate authority `ca-201`. `tcpdump` on `radius-201a`. **Cost:** none beyond the Chapter 999 lab.

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

## Lab Verification

Complete this sign-off once Labs 7.1 to 7.1 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from the workbook's CLI-checked syntax and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the two AAA Services SRG requirements that land on a FortiSwitch by running RADIUS over TLS between the switch and `radius-201a`, with certificate validation on both ends and a capture that shows the credentials are encrypted.

- [ ] Has a working RadSec login.
- [ ] Has a capture showing no clear-text RADIUS.
- [ ] Has shown the switch rejecting an untrusted server.
- [ ] Knows what the lab CA does not prove.
