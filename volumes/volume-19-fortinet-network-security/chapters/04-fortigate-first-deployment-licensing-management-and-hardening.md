# Chapter 04: FortiGate First Deployment, Licensing, Management, and Hardening

## Learning Objectives

- Describe FortiGate form factors and the FortiOS configuration model
  (global vs. VDOM scope, running configuration vs. flash).
- Explain FortiGuard licensing models and register a device with FortiCare.
- Configure hostname, DNS, NTP, and management access from the CLI.
- Apply baseline hardening: administrator password policy, trusted hosts,
  local-in access restriction, and administrative protocol selection.
- Validate a first deployment using status, licensing, and connectivity
  commands.

## Theory and Architecture

### FortiGate form factors

FortiGate ships in several form factors that run the same FortiOS image
and expose the same CLI, which is why this encyclopedia's CLI examples
apply regardless of which form factor a reader's lab uses:

| Form factor | Typical use |
| --- | --- |
| Hardware appliance | Physical branch or data-center deployment with purpose-built ASIC acceleration (NP/CP/SPU) |
| FortiGate-VM | Hypervisor-hosted virtual appliance (VMware, KVM, Hyper-V, and public cloud marketplaces), licensed by vCPU allocation |
| FortiGate Cloud-native (public cloud) | Cloud marketplace images with cloud-provider-integrated auto-scaling and load-balancer integration |
| FortiGate container form factor | Containerized deployment for specific orchestration environments |

This volume's labs use **FortiGate-VM64** on a reader-controlled hypervisor
specifically because it is free to evaluate, reproducible across
platforms, and does not require dedicated hardware.

### Hardware acceleration concept

Physical FortiGate appliances (and some VM deployment modes with SR-IOV
passthrough) use dedicated silicon — **Network Processors (NP)** for
line-rate stateful forwarding and IPsec offload, **Content Processors
(CP)** for pattern-matching-heavy inspection such as IPS and antivirus, and
**Security Processing Units (SPU)** as the umbrella term for this
acceleration architecture — to offload work from the general-purpose CPU.
A FortiGate-VM lab instance runs entirely in software with no ASIC
offload, which is sufficient for learning configuration and behavior but
is not representative of the throughput a comparably specified hardware
appliance would deliver; this distinction matters when Chapter 07's
SSL deep inspection discussion addresses performance.

### FortiOS configuration model

FortiOS configuration is a hierarchical, block-structured tree navigated
with `config`/`edit`/`set`/`next`/`end`:

- `config <table>` enters a configuration table (for example,
  `config system interface`).
- `edit <name>` creates or enters a specific entry within that table.
- `set <field> <value>` sets a field on the current entry.
- `next` commits the current entry and returns to the table level to edit
  another entry.
- `end` exits the configuration table back to the root prompt.

Configuration lives in a **running configuration** held in memory and
persisted to flash; `show` and `show full-configuration` display it, and
`execute backup config` exports it for external storage — covered further
in Chapter 09's configuration lifecycle discussion. On a device with
multiple VDOMs enabled (Chapter 05), most `config` commands operate within
the currently selected VDOM scope unless issued from `config global`,
which is why VDOM-aware devices show a `global` vs. per-VDOM CLI prompt
distinction.

### FortiGuard licensing model

A FortiGate's base unit runs without any subscription, but its full
security-profile capability (Chapter 07) depends on FortiGuard
subscriptions activated through **FortiCare**, Fortinet's device
registration and support portal:

| Bundle | Typical contents |
| --- | --- |
| FortiCare support | Firmware updates, TAC support access; required baseline for any licensed device |
| FortiGuard Unified Threat Protection (UTP) | IPS, application control, antivirus, web filtering, and basic sandboxing (cloud) content |
| FortiGuard Enterprise Protection | UTP content plus advanced services such as industrial signatures, credential/dark web monitoring, and SD-WAN overlay content, varying by model and release |
| FortiGuard Advanced Threat Protection (ATP) | IPS, application control, and antivirus content without the broader UTP web/sandbox bundle, for organizations layering a separate secure web gateway |
| FortiFlex | Consumption-based licensing that allows point allocation across FortiGate-VM, cloud, and certain hardware SKUs rather than a fixed per-device perpetual license |

A **FortiGate-VM** additionally requires a VM license file matched to its
allocated vCPU count (or an evaluation license with reduced throughput and
a fixed expiration, sufficient for lab use), uploaded separately from the
FortiGuard subscription activation.

## Design Considerations

- **Licensing bundle selection against the technology inventory.**
  Chapter 02's technology-to-risk inventory should directly inform bundle
  selection — an organization that has identified sandboxing and IPS as
  coverage gaps needs UTP or Enterprise Protection content, not the bare
  FortiCare support tier.
- **Sizing for VM deployments.** FortiGate-VM throughput and session
  capacity scale with allocated vCPU count and license tier, not
  automatically with the underlying hypervisor's available capacity;
  under-provisioning vCPU allocation relative to expected throughput is a
  common lab and production sizing mistake.
- **Management network design.** Decide before deployment whether
  administrative access (GUI/SSH) will be reachable from a general LAN
  segment, a dedicated out-of-band management network, or only through a
  jump host — retrofitting this decision after policies and NAT already
  assume a particular interface's role is disruptive.
- **Hostname and naming standards.** Apply the organization's naming
  convention (site, role, sequence number) at first deployment rather than
  leaving a default hostname; hostname appears in HA configuration
  (Chapter 05), FortiManager device lists (Chapter 08), and every log
  record, so a late rename has downstream cleanup cost.
- **Password policy vs. operational friction.** A password policy that is
  too strict for the administrative team's actual workflow invites
  workarounds (written-down passwords, shared accounts); balance
  complexity requirements against realistic administrator behavior and
  pair strong password policy with FortiToken MFA rather than relying on
  password complexity alone.

## Implementation and Automation

The lab environment introduced in Chapter 03 continues here as
**FGT-LAB-01**, a FortiGate-VM64 instance. This chapter performs the
device's first formal deployment: hostname, DNS/NTP, FortiCare
registration, licensing, and baseline hardening.

### Setting hostname, DNS, and NTP

```text
FGT-LAB-01 # config system global
FGT-LAB-01 (global) # set hostname "FGT-LAB-01"
FGT-LAB-01 (global) # set timezone 04
FGT-LAB-01 (global) # end
FGT-LAB-01 # config system dns
FGT-LAB-01 (dns) # set primary 208.67.222.222
FGT-LAB-01 (dns) # set secondary 208.67.220.220
FGT-LAB-01 (dns) # end
FGT-LAB-01 # config system ntp
FGT-LAB-01 (ntp) # set ntpsync enable
FGT-LAB-01 (ntp) # set type fortiguard
FGT-LAB-01 (ntp) # end
```

Accurate time synchronization is a prerequisite for correct log
timestamps, certificate validation (Chapter 07), and IPsec/SSL VPN session
negotiation (Chapter 06); configure NTP before any feature that depends on
it rather than as an afterthought.

### Assigning a management interface address

```text
FGT-LAB-01 # config system interface
FGT-LAB-01 (interface) # edit "port2"
FGT-LAB-01 (port2) # set alias "lan-mgmt"
FGT-LAB-01 (port2) # set ip 10.10.10.1 255.255.255.0
FGT-LAB-01 (port2) # set allowaccess https ssh ping
FGT-LAB-01 (port2) # next
FGT-LAB-01 (interface) # end
```

`allowaccess` explicitly enumerates which administrative protocols are
permitted on this interface; only `https`, `ssh`, and `ping` are enabled
here — `http` (unencrypted) and `telnet` are deliberately omitted as part
of baseline hardening.

### Registering with FortiCare and licensing

```text
FGT-LAB-01 # execute update-now
```

Device registration itself is normally completed through the GUI's
**Dashboard > Licenses** widget (or the FortiCare portal directly), where
the device's serial number is associated with a FortiCare account and any
purchased or evaluation subscriptions are applied. Once registered and
licensed, confirm from the CLI:

```text
FGT-LAB-01 # diagnose autoupdate versions
FGT-LAB-01 # get system status
```

For a FortiGate-VM specifically, an evaluation or purchased VM license
file is uploaded via **System > FortiGuard > License Information** in the
GUI, or applied at initial boot depending on the cloud marketplace image
used; the CLI equivalent for a license file already staged is:

```text
FGT-LAB-01 # execute restore vmlicense <TFTP_or_local_path>
```

### Changing the default administrator password and enabling a password policy

```text
FGT-LAB-01 # config system admin
FGT-LAB-01 (admin) # edit "admin"
FGT-LAB-01 (admin) # set password <NEW_STRONG_PASSWORD>
FGT-LAB-01 (admin) # next
FGT-LAB-01 (admin) # end
FGT-LAB-01 # config system password-policy
FGT-LAB-01 (password-policy) # set status enable
FGT-LAB-01 (password-policy) # set minimum-length 14
FGT-LAB-01 (password-policy) # set min-upper-case-letter 1
FGT-LAB-01 (password-policy) # set min-lower-case-letter 1
FGT-LAB-01 (password-policy) # set min-number 1
FGT-LAB-01 (password-policy) # set min-non-alphanumeric 1
FGT-LAB-01 (password-policy) # set expire-status enable
FGT-LAB-01 (password-policy) # set expire-day 90
FGT-LAB-01 (password-policy) # end
```

### Restricting administrative access with trusted hosts and local-in policy

```text
FGT-LAB-01 # config system admin
FGT-LAB-01 (admin) # edit "admin"
FGT-LAB-01 (admin) # set trusthost1 10.10.10.0 255.255.255.0
FGT-LAB-01 (admin) # set trusthost2 172.16.99.0 255.255.255.0
FGT-LAB-01 (admin) # next
FGT-LAB-01 (admin) # end
```

`trusthost` fields restrict where this specific administrator account is
permitted to authenticate from, independent of which interfaces have
`allowaccess` enabled — the two controls are complementary: `allowaccess`
governs the interface, `trusthost` governs the account.

### Enabling FortiToken MFA for the admin account

```text
FGT-LAB-01 # config system admin
FGT-LAB-01 (admin) # edit "admin"
FGT-LAB-01 (admin) # set two-factor fortitoken
FGT-LAB-01 (admin) # set fortitoken <SERIAL_OR_MOBILE_TOKEN_ID>
FGT-LAB-01 (admin) # next
FGT-LAB-01 (admin) # end
```

A lab environment without a provisioned FortiToken can substitute
`two-factor email` for a functionally similar (though less phishing
resistant) exercise, consistent with Chapter 01's MFA guidance.

## Validation and Troubleshooting

- **Confirm licensing state.** `get system status` reports overall license
  validity; the GUI **Dashboard > Licenses** widget provides a
  per-subscription breakdown. A subscription showing as expired or
  unlicensed after registration usually indicates the device has not yet
  reached FortiGuard's update infrastructure — check DNS and outbound
  HTTPS reachability from the interface configured with internet egress.
- **`execute update-now` reports no contact.** Confirm the device has a
  default route and working DNS resolution (`execute ping fortiguard.com`
  once DNS is configured), and that no upstream firewall blocks outbound
  HTTPS to FortiGuard's distribution network.
- **Locked out of GUI/SSH after trusted-host configuration.** If the
  administering workstation's subnet was not included in `trusthost1`/
  `trusthost2`, access is denied immediately upon the next login attempt;
  recover via console access and correct the `trusthost` values, which is
  exactly why console access (Chapter 03) is treated as the durable
  fallback access path.
- **NTP not synchronizing.** `diagnose sys ntp status` reports current
  sync state; certificate and log-timestamp problems downstream (Chapters
  06 and 07) frequently trace back to unnoticed NTP failure at initial
  deployment.
- **Password policy rejects a password unexpectedly.** Confirm the
  intended complexity fields (`min-upper-case-letter`, `min-number`,
  `min-non-alphanumeric`) against the password actually being entered;
  `config system password-policy` failures report which specific
  requirement was not met.

## Security and Best Practices

- Disable `http` administrative access entirely (`allowaccess` should
  include `https`, not `http`) on every interface; unencrypted
  administrative sessions expose credentials to any on-path observer.
- Never leave administrative GUI/SSH access reachable from a WAN-facing
  interface; restrict `allowaccess` on internet-facing interfaces to none
  of the administrative protocols, and manage the device only from trusted
  internal or out-of-band networks.
- Pair password policy with FortiToken (or an equivalent phishing-resistant
  second factor) for every administrator account, not password complexity
  alone, consistent with Chapter 01's MFA guidance.
- Rename the default `admin` account's role going forward to a named,
  individually attributable administrator account per person where the
  organization's scale supports it, rather than multiple staff sharing one
  `admin` login — this materially improves audit trail quality.
- Keep FortiGuard content and firmware update schedules current
  (Chapter 08 covers scheduled and centrally managed update automation);
  an under-licensed or stale device silently degrades protection exactly
  as described for other vendors' platforms elsewhere in this encyclopedia
  (see Volume XVI, Chapter 02, for the equivalent Palo Alto Networks
  licensing-currency discussion).

## References and Knowledge Checks

**References**

- Fortinet, *FortiOS Administration Guide* — initial setup, licensing, and
  hardening.
- Fortinet, *FortiOS CLI Reference* — `config system global`,
  `config system interface`, `config system admin`,
  `config system password-policy`.
- Fortinet NSE Training Institute, *NSE 4: FortiGate Security* course
  (initial configuration and administrative access domains).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. What is the difference between what `allowaccess` controls and what
   `trusthost1`/`trusthost2` control on an administrator account?
2. Why does FortiGate-VM licensing depend on allocated vCPU count in a way
   that a hardware appliance's license does not?
3. Name two FortiGuard subscription bundles and one capability each
   contains.
4. Why should NTP be configured before certificate-dependent features are
   deployed?

## Hands-On Lab

**Objective:** Perform a complete first deployment of FGT-LAB-01: hostname,
DNS/NTP, FortiCare registration and licensing, management interface
configuration, and baseline hardening including trusted hosts and password
policy.

**Prerequisites**

- FGT-LAB-01 from Chapter 03, reachable via console or its factory-default
  management IP, with the `admin` password already set.
- A free Fortinet Developer Network or FortiCare account for evaluation
  registration.
- Outbound internet reachability from the interface that will serve as the
  device's egress path.

**Steps**

1. Set hostname, timezone, DNS, and NTP as shown in Implementation and
   Automation.

   **Expected result:** `get system status` reflects the new hostname; `diagnose sys ntp status` shows a synchronized state within a few minutes.

2. Configure the management/LAN interface (`port2` in this lab) with a
   static IP and restricted `allowaccess`.

   **Expected result:** The GUI and SSH remain reachable from the
   `10.10.10.0/24` subnet only.

3. Register the device with FortiCare (GUI **Dashboard > Licenses**, or the
   FortiCare portal) using an evaluation or lab license, and confirm
   activation:

   ```text
   FGT-LAB-01 # execute update-now
   FGT-LAB-01 # diagnose autoupdate versions
   ```

   **Expected result:** FortiGuard content versions populate with current
   dates rather than showing as unlicensed.

4. Set a new, strong administrator password and enable the password
   policy exactly as shown in Implementation and Automation.

5. Configure `trusthost1` for the `admin` account to the lab management
   subnet only.

6. **Negative test:** From a workstation or VM on a different subnet than
   the one specified in `trusthost1` (or by temporarily adjusting your own
   workstation's IP outside that range), attempt to reach the GUI or SSH.

   **Expected result:** The connection is refused or times out, confirming
   `trusthost` enforcement is active. Return your workstation to the
   permitted subnet before continuing.

7. Enable FortiToken (or `two-factor email` as a lab substitute) on the
   `admin` account and confirm the next login prompts for the second
   factor.

8. Run final validation:

   ```text
   FGT-LAB-01 # get system status
   FGT-LAB-01 # show system admin
   FGT-LAB-01 # show system password-policy
   ```

   **Expected result:** Output confirms hostname, licensing state, the
   hardened `admin` account configuration, and an enabled password policy.

**Cleanup**

- This lab's changes are the intended persistent baseline for Chapters
  05–09; no rollback is required. If the lab instance will be rebuilt from
  scratch for a different purpose, record these settings so they can be
  reapplied quickly.

## Summary and Completion Checklist

This chapter took FGT-LAB-01 from Chapter 03's factory-default state
through a complete first deployment: hostname and time synchronization,
FortiCare registration and FortiGuard licensing, a properly restricted
management interface, and baseline hardening covering password policy,
trusted hosts, and MFA on the administrator account. This hardened,
licensed baseline is the foundation Chapter 05 builds on for interfaces,
routing, NAT, VDOMs, and high availability.

- [ ] Can explain the FortiOS `config`/`edit`/`set`/`next`/`end` model and
      global vs. VDOM configuration scope.
- [ ] Can describe FortiGuard licensing bundles and FortiGate-VM licensing
      by vCPU.
- [ ] Can configure hostname, DNS, NTP, and a restricted management
      interface from the CLI.
- [ ] Can apply password policy, trusted hosts, and MFA hardening to an
      administrator account.
- [ ] Completed the hands-on lab, including the negative test.
