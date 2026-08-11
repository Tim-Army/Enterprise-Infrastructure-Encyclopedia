# Chapter 03: NSE 3 Security Fabric and FortiGate Operator Foundations

![Lab flow for this chapter: a factory-default FortiGate is explored read-only, including its Security Fabric topology and a low initial Security Rating tied to its unlicensed, unhardened state. A least-privilege operator account is created and logged into. As a negative test, that account attempts a configuration write; FortiOS denies it with a permission error, while read commands continue to succeed in the same session, confirming the profile's read/write boundary is enforced precisely. The lab account is removed afterward, returning the device to a clean baseline.](../../../diagrams/volume-019-fortinet-network-security/chapter-03-fortigate-operator-least-privilege-flow.svg)

*Figure 3-1. Flow used throughout this chapter's Hands-On Lab: a factory-default FortiGate explored read-only as an operator, then a least-privilege account tested against a configuration write attempt.*

## Learning Objectives

- Describe the five pillars of the Fortinet Security Fabric architecture
  and how fabric components exchange telemetry.
- Explain the role of FortiTelemetry and Security Rating in fabric-wide
  visibility.
- Navigate the FortiGate GUI dashboard and CLI console as a read-only
  operator.
- Distinguish operator-level (read-only) access from administrator-level
  (configuration) access and explain why the distinction matters.
- Run safe, non-disruptive diagnostic commands to check system status,
  performance, and connectivity.

## Theory and Architecture

### From individual products to a fabric

[Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md) mapped individual technology categories to individual Fortinet
product families. The Security Fabric is the architectural layer that
connects those products so they function as a coordinated system rather
than a collection of independently managed appliances. Fabric components
register with a **root FortiGate**, exchange status and threat telemetry
over **FortiTelemetry**, and expose a single topology and security-posture
view rather than requiring an operator to check each product's own console
separately.

### The five Security Fabric pillars

Fortinet organizes the Security Fabric around five architectural pillars:

| Pillar | What it addresses |
| --- | --- |
| Security-Driven Networking | Converges networking and security functions (routing, SD-WAN, and inspection) into the same enforcement points instead of bolting security onto a separately designed network |
| Zero Trust Access | Verifies user and device identity and posture continuously, rather than granting broad trust once a connection is established ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)) |
| AI-driven Security Operations | Uses machine learning and automation (FortiGuard AI-based detection, FortiAnalyzer/FortiSIEM analytics, FortiSOAR playbooks) to reduce manual triage load |
| Adaptive Cloud Security | Extends consistent policy and visibility into public and private cloud workloads, not only on-premises appliances |
| Open Ecosystem | Fabric Connectors and published APIs allow third-party products to participate in fabric telemetry sharing and automated response |

These pillars are a planning taxonomy, not a checklist an organization
completes once. Chapters 04 through 09 build Security-Driven Networking and
Zero Trust Access capability directly on a FortiGate; [Volume XI](../../volume-011-observability-enterprise-operations/README.md) and Volume
X address AI-driven operations and broader security architecture across
the encyclopedia's vendor-neutral volumes.

### Fabric topology and FortiTelemetry

A root FortiGate discovers and displays connected fabric components —
additional FortiGates, FortiSwitches, FortiAPs, FortiClient EMS,
FortiAnalyzer, and Fabric Connectors to third-party or cloud platforms — in
a **Physical Topology** and **Logical Topology** view. This discovery and
status exchange runs over FortiTelemetry, a lightweight protocol fabric
components use to report identity, health, and configuration status to the
root device. A single-FortiGate lab environment (as used starting in
[Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)) will show a minimal topology consisting of just that device
until additional fabric components are added in later volumes or advanced
labs; the topology view's value scales with the number of participating
components.

### Security Rating

**Security Rating** is a continuously evaluated scorecard that checks the
fabric's current configuration against Fortinet-maintained best-practice
rules — spanning device hardening, security posture (are security profiles
actually applied, not just licensed), and Security Fabric coverage itself.
It groups findings by severity and links each finding to the specific
configuration change that resolves it, making it a practical, prioritized
starting point for a new operator auditing an existing device, and a
recurring health check for a device already in production. This chapter's
lab uses Security Rating in read-only observation mode; [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md) begins
acting on its findings as the device is formally licensed and hardened.

### Operator access vs. administrator access

FortiOS separates **what an administrator account can see** from **what it
can change** through **admin profiles** (`config system accprofile`). A
profile can grant read-only visibility to some or all configuration areas
while denying write access entirely — the correct model for an operator
role such as a help-desk analyst, a NOC monitoring role, or a
new-hire shadowing an experienced administrator. This is distinct from the
`super_admin` profile, which has unrestricted read/write access to every
configuration area including administrator account management itself.
Least-privilege operator access is a foundational control this chapter
introduces and [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md) formalizes as part of initial hardening.

### GUI and CLI as parallel interfaces

Every configuration change available through the FortiGate GUI has a
corresponding CLI representation, and the reverse is true for the vast
majority of settings — the GUI is not a restricted subset bolted onto a
"real" CLI-only product, and the CLI is not a legacy fallback. Operators
and administrators move between both fluidly: the GUI is generally faster
for exploring an unfamiliar configuration or reviewing logs visually; the
CLI is generally faster for precise, scriptable, or bulk changes, and it
is the only interface exposed identically across every FortiGate form
factor (hardware appliance, VM, and cloud). This encyclopedia uses CLI
syntax throughout Chapters 04–09 specifically because it is complete,
reproducible, and version-controllable in a way that GUI screenshots are
not.

## Design Considerations

- **Role-appropriate access from day one.** Do not provision every new
  administrator with `super_admin` "to keep things simple" — decide the
  operator/administrator boundary before the device goes into production,
  since retrofitting least-privilege access onto an estate of
  already-provisioned super-admin accounts is organizationally harder than
  starting correctly.
- **Console vs. SSH vs. GUI access trade-offs.** Console (serial) access
  works even when the network stack is misconfigured or the device is
  unreachable over IP, making it the correct out-of-band access method for
  initial deployment and disaster recovery; SSH and HTTPS GUI access
  require a functioning management IP and are the normal day-to-day access
  path once initial configuration exists.
- **Fabric topology as a design input, not just a display.** A newly
  provisioned fabric root device with no connected components is not
  itself a finding, but Security Rating checks that reference fabric
  coverage should inform later design decisions about which components
  (FortiAnalyzer for centralized logging, FortiClient EMS for endpoint
  posture) the organization intends to add and when.
- **Jump host / bastion access pattern.** For any production deployment,
  plan administrative access (GUI and SSH) to route through a jump host or
  bastion on a restricted management network rather than being reachable
  directly from a general user VLAN — this is formalized as a hardening
  control in [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md).

## Implementation and Automation

This chapter's hands-on activity uses a FortiGate in its **factory default
state** — before formal licensing, hostname configuration, or hardening,
which is [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)'s subject. The commands below are read-only or
limited to a scoped, reversible operator-account exercise; no network,
policy, or licensing configuration is performed here.

### Logging in for the first time

A factory-default FortiGate (hardware or VM) is reachable on its default
internal interface (commonly `port1` on many models, or the interface
FortiOS designates in its default configuration) at a documented default
IP, typically `192.168.1.99/24`, with the default `admin` account and an
empty password. Console access uses the device's serial/console port at
9600 baud regardless of network state.

```text
FortiGate-VM64 login: admin
Password:
```

FortiOS prompts a factory-default login to set an administrator password
immediately; a lab environment should always complete this step even
before further configuration, rather than leaving the default account
passwordless for any longer than the immediate login.

### Read-only status commands

```text
FGT-LAB-01 # get system status
FGT-LAB-01 # get system performance status
FGT-LAB-01 # get system interface physical
FGT-LAB-01 # get hardware status
FGT-LAB-01 # diagnose sys top
```

`get system status` reports the FortiOS build/version, serial number, and
current operation mode. `get system performance status` reports current
CPU, memory, and session count — useful both as a first-look health check
and as a baseline to compare against later once real traffic and
inspection profiles are applied ([Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)). `diagnose sys top` is an
interactive, `top`-style process view; press `q` to exit without making
any change.

### Read-only connectivity check

```text
FGT-LAB-01 # execute ping 8.8.8.8
FGT-LAB-01 # execute traceroute 8.8.8.8
```

These confirm basic IP reachability from the device itself and are safe to
run against any destination without affecting device configuration.

### Creating a least-privilege operator profile

This is the one configuration change this chapter makes, deliberately
scoped and reversed at the end of the lab to leave the device in its
original state for [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md).

```text
FGT-LAB-01 # config system accprofile
FGT-LAB-01 (accprofile) # edit "operator-readonly"
FGT-LAB-01 (operator-readonly) # set secfabgrp read
FGT-LAB-01 (operator-readonly) # set ftviewgrp read
FGT-LAB-01 (operator-readonly) # set authgrp read
FGT-LAB-01 (operator-readonly) # set sysgrp read
FGT-LAB-01 (operator-readonly) # set netgrp read
FGT-LAB-01 (operator-readonly) # set loggrp read
FGT-LAB-01 (operator-readonly) # set fwgrp read
FGT-LAB-01 (operator-readonly) # set vpngrp read
FGT-LAB-01 (operator-readonly) # set utmgrp read
FGT-LAB-01 (operator-readonly) # end
FGT-LAB-01 # config system admin
FGT-LAB-01 (admin) # edit "operator1"
FGT-LAB-01 (operator1) # set accprofile "operator-readonly"
FGT-LAB-01 (operator1) # set password <STRONG_TEMP_PASSWORD>
FGT-LAB-01 (operator1) # next
FGT-LAB-01 (admin) # end
```

Every access-control group field set to `read` grants visibility without
write access; leaving a field at its default (which may include write
access on a freshly created profile depending on the field) would defeat
the purpose of this exercise, so each relevant group is set explicitly.

## Validation and Troubleshooting

- **Confirming operator access is actually read-only.** Log out and log
  back in as `operator1`, then attempt a trivial configuration change (for
  example, entering `config system interface` and attempting to edit an
  interface). FortiOS should reject the write attempt with a permission
  error while still allowing the `get`/`show`/`diagnose` read commands used
  earlier in this chapter.
- **Console access unavailable.** If console access does not respond,
  confirm the serial console cable/adapter, baud rate (9600 8-N-1 is the
  common FortiGate default), and that no other management session is
  already bound to the console port.
- **Default IP unreachable over the network.** Confirm the connecting
  workstation is on the same subnet as the documented factory-default
  interface and IP before assuming the device itself is unreachable; this
  is a common first-contact issue distinct from any FortiGate
  misconfiguration.
- **Security Rating shows a low score on a fresh device.** This is
  expected on an unlicensed, unhardened, factory-default device — Chapter
  04's licensing and hardening steps directly address the findings a
  fresh Security Rating check will surface, and re-checking after Chapter
  04 is a natural validation point.
- **Topology view shows only the local device.** Expected for a
  single-appliance lab with no additional fabric components registered;
  this is not a fault to troubleshoot at this stage.

## Security and Best Practices

- Never leave a factory-default `admin` account with an empty password
  reachable on any network beyond the immediate, isolated first-login
  session — set a strong password as the very first action after console
  or direct network access is established.
- Default to creating scoped operator profiles for any role that does not
  require configuration write access, rather than issuing `super_admin` by
  default and narrowing later.
- Treat console/serial access physically the way any other privileged
  access path is treated — restrict physical access to console ports and
  console servers to authorized personnel.
- Review Security Rating findings on a recurring basis even after initial
  hardening ([Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)); best-practice checks evolve with FortiOS releases
  and FortiGuard-delivered rule updates, so a device hardened correctly at
  deployment can still drift out of alignment with current guidance over
  time.
- Document the operator/administrator access boundary in an organizational
  access policy, not only in the device configuration itself, so the
  intent survives staff turnover.

## References and Knowledge Checks

**References**

- [Fortinet NSE Training Institute, *NSE 3: Fortinet Security Fabric* and
  associated product-introduction modules.](https://training.fortinet.com/local/staticpage/view.php?page=nse_3)
- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/8.0.0) — Security Fabric setup and
  Security Rating.
- [Fortinet, *FortiOS CLI Reference*](https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/84566/fortios-cli-reference) — `config system accprofile`,
  `config system admin`.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. Name the five Security Fabric pillars and give one example capability
   under each.
2. What protocol do Security Fabric components use to exchange status and
   telemetry with the root FortiGate?
3. Why does a least-privilege operator profile need explicit `read`
   settings on each access-control group rather than relying on default
   values?
4. Give one operational reason console access remains necessary even in an
   environment where SSH and GUI access are normally used.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each theme of NSE 3 (Security
Fabric fundamentals and day-to-day FortiGate operator tasks)** — mapped in the volume
README's coverage tables. Every command is a real FortiOS 7.6 CLI/GUI action; each lab
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.4** — a FortiGate (VM or hardware) on FortiOS
7.6 with admin access by HTTPS GUI and SSH CLI, and a client behind it. **Cost:** none
beyond lab resources.

### Lab 3.1 — First login and system inventory (Topic: FortiGate operator basics)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Log in and read the appliance's identity and health.

```text
get system status
get system performance status
```

**Expected result:** `get system status` prints the model, serial, firmware
(`v7.6.x`), and license/FortiGuard state; `performance status` shows CPU, memory, and
session counts — the operator's first orientation on any FortiGate.

**Negative test:** skip reading firmware/license state and troubleshoot blindly; an
expired FortiGuard contract silently stops signature updates, which this check reveals.

**Cleanup:** none (read-only).

### Lab 3.2 — Build and read the Security Fabric (Topic: Security Fabric fundamentals)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Enable Fabric on the root FortiGate and read the topology.

```text
config system csf
    set status enable
    set group-name "Lab-Fabric"
    set configuration-sync default
end
diagnose sys csf global | head -20
```

**Expected result:** the FortiGate becomes the Fabric root; `diagnose sys csf global`
lists the Fabric group and any joined members — the Security Fabric stitches
FortiGate, FortiSwitch, FortiAP, and FortiAnalyzer into one topology with shared
telemetry and a Security Rating.

**Negative test:** join a downstream device without a matching group name/authorization
on the root; it never appears in the topology — Fabric membership is authorized, not
automatic.

**Cleanup:**

```text
config system csf
    set status disable
end
```

### Lab 3.3 — FortiView and logging (Topic: Monitoring and logging)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Enable logging and read live sessions in FortiView.

```text
config log memory setting
    set status enable
end
diagnose sys session stat
get system session-info full 2>/dev/null | head -20
```

**Expected result:** session statistics (setup rate, active session count) and, in the
GUI, **FortiView → Sources/Destinations** populating with live traffic — the operator's
window into who is talking to what, backed by memory or disk logs (or FortiAnalyzer).

**Negative test:** rely on FortiView with all logging disabled; the panes stay empty —
FortiView renders logged data, so logging must be on for a policy or globally.

**Cleanup:** none (leave logging enabled; it is expected in operation).

### Lab 3.4 — Back up and restore configuration (Topic: Operator lifecycle tasks)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Take a config backup — the operator's safety net before any change.

```text
execute backup config flash pre-change
execute revision list config
```

**Expected result:** a stored configuration revision listed by `execute revision list
config`, timestamped and labeled — you can restore it with `execute restore config
flash <id>` if a change misfires; taking a backup before edits is the core operator
discipline.

**Negative test:** make a sweeping policy change with no backup and no revision; there
is nothing to roll back to when connectivity breaks — the backup is what makes the
change reversible.

**Cleanup:** none (keep the revision).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter connected the individual products from [Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md) into the
Security Fabric's five architectural pillars, explained how fabric
components share telemetry and how Security Rating turns best-practice
guidance into an actionable, prioritized checklist, and drew the
operator/administrator access boundary that governs least-privilege
account design. The hands-on lab exercised first login, read-only status
and connectivity commands, GUI topology and rating review, and creation
and validation of a scoped operator account — the last piece of
foundational knowledge before [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md) begins formal FortiGate
deployment, licensing, and hardening.

- [ ] Can name the five Security Fabric pillars and one capability under
      each.
- [ ] Can explain FortiTelemetry's role in fabric topology and status
      exchange.
- [ ] Can distinguish operator (read-only) from administrator
      (read/write) access and explain why the distinction matters
      operationally.
- [ ] Can run safe, read-only CLI diagnostic commands without risk of
      configuration impact.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup, leaving the device ready for [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md).
