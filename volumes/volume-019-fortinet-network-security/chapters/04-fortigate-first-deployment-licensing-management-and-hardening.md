# Chapter 04: FortiGate First Deployment, Licensing, Management, and Hardening

![Lab flow for this chapter: the lab firewall receives hostname, DNS, NTP, FortiCare licensing, a hardened management interface, a strong password policy, and a trusted-host restriction scoped to the lab management subnet. As a negative test, a workstation on a different subnet attempts to reach the GUI or SSH; the connection is refused or times out, confirming the trusted-host restriction is actively enforcing access rather than merely being configured. Two-factor authentication is then enabled on the admin account, and final validation confirms every hardening element together.](../../../diagrams/volume-019-fortinet-network-security/chapter-04-fortigate-trusthost-hardening-flow.svg)

*Figure 4-1. Flow used throughout this chapter's Hands-On Lab: FortiGate first deployment and hardening, tested against a management-access attempt from outside the trusted subnet.*

## Learning Objectives

- Describe FortiGate form factors and the FortiOS configuration model
  (global vs. VDOM scope, running configuration vs. flash).
- Explain FortiGuard licensing models and register a device with FortiCare.
- Configure hostname, DNS, NTP, and management access from the CLI.
- Apply baseline hardening: administrator password policy, trusted hosts,
  local-in access restriction, and administrative protocol selection.
- Validate a first deployment using status, licensing, and connectivity
  commands.
- Upgrade a FortiGate-VM's firmware over TFTP from the CLI, and recognize
  when the GUI upgrade path is unavailable on an evaluation license.

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
appliance would deliver; this distinction matters when [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)'s
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
in [Chapter 09](09-nse-4-fortios-administrator-training-and-enterprise-capstone.md)'s configuration lifecycle discussion. On a device with
multiple VDOMs enabled ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)), most `config` commands operate within
the currently selected VDOM scope unless issued from `config global`,
which is why VDOM-aware devices show a `global` vs. per-VDOM CLI prompt
distinction.

### FortiGuard licensing model

A FortiGate's base unit runs without any subscription, but its full
security-profile capability ([Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)) depends on FortiGuard
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
  [Chapter 02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md)'s technology-to-risk inventory should directly inform bundle
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
  ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)), FortiManager device lists ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)), and every log
  record, so a late rename has downstream cleanup cost.
- **Password policy vs. operational friction.** A password policy that is
  too strict for the administrative team's actual workflow invites
  workarounds (written-down passwords, shared accounts); balance
  complexity requirements against realistic administrator behavior and
  pair strong password policy with FortiToken MFA rather than relying on
  password complexity alone.

## Implementation and Automation

The lab environment introduced in [Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md) continues here as
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
timestamps, certificate validation ([Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)), and IPsec/SSL VPN session
negotiation ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)); configure NTP before any feature that depends on
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

**Gotcha — an unlicensed FortiGate-VM forwards no traffic (FortiOS 7.6).** Until a VM
license is applied, `get system status` reports `License Status: Invalid` and caps the
usable resources (for example `2 CPU/1 allowed`). In this state the appliance still accepts
*management and locally-destined* traffic — you can SSH in, and hosts can ping the
FortiGate's own interface IPs — but it **silently drops everything it must forward through a
firewall policy.** The signature is unmistakable in a flow trace: a forwarded packet reaches
`__vf_ip_route_input_rcu` ("find a route ... via `<egress>`") and the trace then simply
stops — the forward-policy engine (`iprope_check`) is never reached, no session installs
(`diagnose sys session list` shows `total session: 0`), and widening the policy service to
`ALL` changes nothing. It reads exactly like a broken firewall rule, but the policy is fine;
the license is the block. Register the VM serial (an evaluation serial begins `FGVMEV`) with
FortiCare to activate the free time-limited evaluation license, apply it with
`execute restore vmlicense`, and the identical configuration begins forwarding. This is why a
purely local test (each host pinging its own gateway) can pass while an inter-VLAN test
between two hosts fails on the very same box — see the inter-VLAN policy lab in
[Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md).

**Gotcha — the LENC (low-encryption) image cannot be licensed at all.** Fortinet publishes
two builds of every FortiGate-VM image: the standard build
(`FGT_VM64_KVM-...-FORTINET.out.kvm.zip`) and a **low-encryption (LENC)** build for
export-restricted markets. A LENC build tops out below TLS 1.2 — and Fortinet's FortiGuard
and FortiCare servers now *require* TLS 1.2 — so on a LENC image every cloud connection
fails with `SSL_connect ... tlsv1 alert protocol version` in
`diagnose debug application update -1`, and the GUI's license-activation dialog **silently
does nothing** when OK is clicked. The confirming tell: `set strong-crypto enable` and
`set ssl-min-proto-version TLSv1-2` both fail with `command parse error` — the strong-crypto
code is compiled out of the image, so no setting can fix it. The only cure is redeploying
with the standard image (back up with `show`, swap the boot disk, restore). Check *before*
deploying; the LENC trap costs a full rebuild.

**Gotcha — the free evaluation license enforces a 3-interface budget, and built-ins count.**
The FGVMEV evaluation permits at most **three interface entries** (plus three policies and
three routes), and the factory defaults already spend the budget: `port1`, `port2`, the
switch-controller's `fortilink` aggregate, and the wireless mesh VAP `default-mesh` are all
table entries. Creating a VLAN sub-interface then fails with
`Command fail. Return code -4 (reached the maximum number of entries)` — and worse, when the
license first applies, FortiOS **purges over-budget interfaces at boot**, which can silently
delete VLAN interfaces (and orphan the policies referencing them) that worked minutes
earlier. Two remediations, both real on 7.6:

- *Reclaim slots from feature-owned interfaces.* `fortilink` deletes only after its bindings
  are cleared (`config system ntp → set server-mode disable`, delete the FortiSwitch DHCP
  server) and `set switch-controller disable` in `system global`. `default-mesh` is a WiFi
  VAP — deletable only from `config wireless-controller vap`, as its delete error hints. The
  `*.root` tunnel interfaces (`ssl.root`, `naf.root`, `l2t.root`) are permanent ("A tunnel
  interface cannot be deleted directly") but do not consume the budget. Use
  `diagnose sys cmdb refcnt show system.interface <name>` to find what pins an interface —
  though note a firewall policy reference reports through the delete error
  ("used by other 1 entries"), not always through refcnt.
- *Move VLAN tagging to the hypervisor.* Even with slots reclaimed, two VLAN sub-interfaces
  plus their parent trunk cannot fit a 3-slot budget (parent + two VLANs = 3 leaves no
  management port). The escape hatch is to give the VM one vNIC per segment as an **access
  port** — the hypervisor applies the VLAN tag (`qm set <vmid> --netN virtio,bridge=<br>,tag=<vlan>`
  on Proxmox) — and address the physical `portN` directly. Three physical ports, zero VLAN
  sub-interfaces, same routed topology; see Lab 5.1's variant note in
  [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md).

**Gotcha — the free evaluation license blocks the GUI firmware upgrade, and FortiOS
8.0.0 on a VM has an unusable GUI under evaluation.** Two independent facts converge here,
both observed on a KVM/Proxmox lab in August 2026, and together they dictate *how* you
upgrade an evaluation FortiGate-VM (Lab 4.8) and *which* release you run for GUI work:

- *The GUI firmware upgrade requires a FortiGuard firmware-upgrade entitlement the
  evaluation tier does not carry.* The upgrade wizard (*System > Firmware & Registration*,
  or the dashboard **Firmware** widget) validates entitlement before it will accept an
  image, and refuses the file with *"The FortiGuard license for firmware upgrades could not
  be verified."* Registering the `FGVMEV` serial with FortiCare does not grant it — the free
  evaluation license simply has no firmware-download contract. The supported escape is the
  CLI, which performs no such check: `execute restore image tftp <file> <tftp-server-ip>`
  (Lab 4.8) writes the image over TFTP and preserves both the configuration and the
  installed license.
- *FortiOS 8.0.0 on a VM logs an administrator out of the GUI moments after login.* A fresh
  login loads the dashboard and then bounces back to the login page (via a blank
  `…/prompt?viewOnly=` redirect). It reproduces on a clean reboot, in a private browser
  window, with no other session connected — so it is not a stale cookie, a concurrent
  administrator session, or a corrupted image. The **Dashboard > Status** page's real-time
  events WebSocket targets the device *hostname*, which a lab browser cannot resolve without
  DNS; navigating to that page triggers the logout, and after a firmware upgrade the behavior
  degrades to logging out on every page. The **same VM shell downgraded to 7.6.7** — the
  release the reference homelab's other FortiGate-VMs run without issue — has a stable GUI,
  which isolates the fault to the 8.0.0-VM image rather than the license, the hypervisor, or
  the configuration. **Run 7.6.7 for GUI work on an evaluation FortiGate-VM, and treat an
  8.0.0 evaluation VM as a CLI/API-only device.** The elimination sequence that reached this
  conclusion: re-imaged 8.0.0 from scratch (still bounced) → clean reboot, private-mode
  browser, single session (still bounced) → confirmed `diagnose debug vm-print-license`
  reports `Model: EVAL`, so the license was applied and was not the cause → ruled out the
  concurrent-session, admin-timeout, and events-WebSocket-to-hostname theories as sole causes
  → swapped the boot disk on the same VM (identical SMBIOS UUID and MACs) to 7.6.7, and the
  GUI was stable. The Alpine `in.tftpd` server in
  [Volume CLXXI](../../volume-171-alpine-linux/README.md) pairs with Lab 4.8 to stage the
  firmware image this workaround consumes.

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
resistant) exercise, consistent with [Chapter 01](01-nse-1-cybersecurity-awareness-and-digital-safety.md)'s MFA guidance.

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
  exactly why console access ([Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md)) is treated as the durable
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
  alone, consistent with [Chapter 01](01-nse-1-cybersecurity-awareness-and-digital-safety.md)'s MFA guidance.
- Rename the default `admin` account's role going forward to a named,
  individually attributable administrator account per person where the
  organization's scale supports it, rather than multiple staff sharing one
  `admin` login — this materially improves audit trail quality.
- Keep FortiGuard content and firmware update schedules current
  ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) covers scheduled and centrally managed update automation);
  an under-licensed or stale device silently degrades protection exactly
  as described for other vendors' platforms elsewhere in this encyclopedia
  (see [Volume XVI, Chapter 02](../../volume-016-palo-alto-networks-security/chapters/02-cybersecurity-practitioner-and-platform-portfolio.md), for the equivalent Palo Alto Networks
  licensing-currency discussion).

## References and Knowledge Checks

**References**

- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/8.0.0) — initial setup, licensing, and
  hardening.
- [Fortinet, *FortiOS CLI Reference*](https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/84566/fortios-cli-reference) — `config system global`,
  `config system interface`, `config system admin`,
  `config system password-policy`.
- [Fortinet NSE Training Institute, *NSE 4: FortiGate Security* course
  (initial configuration and administrative access domains).](https://training.fortinet.com/local/staticpage/view.php?page=nse_4)
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

This chapter carries a topic-level walkthrough lab for **each task under the NSE 4
objective *Deployment and System Configuration* (20–25% of the FortiOS 7.6
Administrator exam)** — mapped in the volume README's coverage tables. Every command
is a real FortiOS 7.6 CLI action; each lab ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 4.1–4.6** — a FortiGate (VM or hardware) on FortiOS
7.6, console or GUI access, and internet reachability for FortiGuard. **Cost:** none
beyond the appliance/VM.

### Lab 4.1 — Initial deployment: interfaces, DNS, and default route (Topic: Initial configuration)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Bring a FortiGate online with a WAN, a LAN, DNS, and a default route.

```text
config system interface
    edit port1
        set alias WAN
        set mode static
        set ip 203.0.113.2 255.255.255.0
        set allowaccess ping https ssh
    next
    edit port2
        set alias LAN
        set ip 10.10.10.1 255.255.255.0
        set allowaccess ping https
    next
end
config system dns
    set primary 208.91.112.53
end
config router static
    edit 1
        set gateway 203.0.113.1
        set device port1
    next
end
execute ping 208.91.112.53
```

**Expected result:** both interfaces show addresses in `get system interface`, and the
ping to the DNS server succeeds via the default route — the FortiGate is online with a
WAN, a LAN, name resolution, and a gateway.

**Negative test:** omit the static default route and ping an internet host; it fails
(`no route to destination`) — routing, not just an interface IP, is what reaches
off-subnet.

**Rollback:** restore lab addressing, or `execute factoryreset` on a throwaway VM.

### Lab 4.2 — Licensing and FortiGuard registration (Topic: Licensing and FortiGuard)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Verify FortiGuard entitlement and force an update.

```text
get system status | grep -iE "License|Serial"
diagnose fortiguard-service status 2>/dev/null | head
execute update-now
diagnose autoupdate versions | grep -iE "AV|IPS|version|expire" | head
```

**Expected result:** a registered serial, contracts with future expiry, and current
AV/IPS DB versions after `execute update-now` — FortiGuard licensing is what feeds
antivirus, IPS, web-filter, and application-control signatures.

**Negative test:** run security profiles with an expired FortiGuard contract; signature
DBs stop updating and new threats pass — the license state (this lab) governs
protection currency.

**Rollback:** none (read-only / update).

### Lab 4.3 — Harden administrative access (Topic: Administrative access and hardening)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Lock admin access to trusted hosts, drop HTTP, and shorten idle timeout.

```text
config system admin
    edit admin
        set trusthost1 10.10.10.0 255.255.255.0
    next
end
config system global
    set admin-scp enable
    set admintimeout 5
    set admin-lockout-threshold 3
    set admin-lockout-duration 60
end
config system interface
    edit port1
        unset allowaccess
        set allowaccess ping https ssh
    next
end
```

**Expected result:** admin login is refused from any source outside `10.10.10.0/24`,
plain HTTP admin is gone, idle sessions expire in 5 minutes, and an admin account locks
for 60 seconds after 3 failed logins — the FortiOS hardening baseline for management-plane
exposure.

**Version note:** older FortiOS had `set admin-https-redirect enable` under `config
system global` to bounce HTTP admin to HTTPS; **FortiOS 7.6 removed it**. It is
unnecessary here anyway — dropping `http` from the interface `allowaccess` above leaves no
plain-HTTP admin listener to redirect, which is the stronger posture.

**Negative test:** leave `allowaccess http telnet` on the WAN interface; the management
plane is reachable in clear text from the internet — exactly what trusted-host + HTTPS
hardening removes.

**Common mistake — a mistyped trusted-host subnet.** The CLI accepts any syntactically
valid network without warning, so a single wrong or dropped digit trusts the wrong one —
`set trusthost2 10.30.9.0 255.255.255.0` when you meant `10.30.99.0`, say. It fails two
ways: if the fat-fingered range is your *only* trusted entry and it excludes your
workstation, your next login is refused (lockout); and if it does **not** lock you out,
you have quietly trusted a network you never intended, or left a dead entry that gives
false confidence the source is covered. Nothing flags it — you catch it only by reading
`show system admin` back, line by line. Fix it by clearing the bad entry and re-adding the
correct one, then re-checking:

```text
config system admin
    edit admin
        unset trusthost2
        set trusthost2 10.30.99.0 255.255.255.0
    next
end
show system admin
```

The habit that makes this safe: keep your current session open and confirm a **fresh
login from the trusted subnet** before you rely on the restriction — a typo (or a NAT
that rewrites your source address, so the FortiGate sees an address outside every
`trusthost`) is only recoverable while you still have a way in. The out-of-band console
(iDRAC or the hypervisor console) is the last-resort recovery path.

**Add email-OTP MFA (when FortiToken is not available).** FortiToken Mobile is the
preferred second factor, but its two free licenses require the FortiGate to be
**registered with FortiCare** and able to reach Fortinet's token server — on an
unregistered evaluation VM that server is unreachable (`diagnose fortitoken info` shows
`Token server status: unreachable` and `0` tokens). Email OTP has no such dependency; it
needs only a reachable SMTP server.

```text
config system email-server
    set type custom
    set security starttls
    set port 587
    set server mail.example.com
    set authenticate enable
    set username otp@example.com
    set password <smtp-password>
    set source-ip <fortigate-mgmt-ip>
end
config system admin
    edit admin
        set two-factor email
        set email-to admin@example.com
    next
end
config system global
    set two-factor-email-expiry 300
end
```

**Expected result:** a password login (GUI, or SSH with a password) now prompts for an
emailed six-digit code; entering it within the expiry window completes the login.
`execute log display` on the event log shows `Two-factor authentication code sent`
followed by `Admin login successful`.

**Four gotchas this exercises, all real on FortiOS 7.6:**

- **`set type custom` is mandatory.** `system email-server` defaults to the FortiGuard
  message relay (which needs FortiCare registration); without `type custom` your SMTP
  settings are silently ignored.
- **Set `port` *after* `security`.** Setting `security` (or `type`) resets the port to
  that mode's default (`25`), so if you set the port first it is clobbered — set it last.
- **`two-factor-email-expiry` defaults to 60 seconds** — the emailed code's lifetime. With
  mail-delivery latency that is tight; raise it (30–600) for a workable window. It couples
  to the lockout: an expired code is a *failed* login, and `admin-lockout-threshold` such
  failures lock the account for `admin-lockout-duration` seconds, so a too-short code
  window cascades into a lockout loop.
- **SSH public-key auth bypasses two-factor.** An admin with `ssh-public-key1` set logs in
  over SSH with the key alone, no OTP — email OTP guards *password* logins (GUI and
  SSH-with-password), not key logins. Account for that in your access model.

**Negative test:** set `two-factor-email-expiry` very low and log in slowly; the code
expires mid-entry and the login fails — trip that three times and the lockout engages,
demonstrating why the code window and the lockout threshold must be tuned together.

**Teardown — disable email OTP when finished.** Return the account to key/password-only so a
later login never waits on a code:

```text
config system admin
    edit admin
        set two-factor disable
        unset email-to
    next
end
```

**Gotcha — an evaluation-licensed FortiGate-VM cannot enable strong-crypto, which can break
STARTTLS OTP delivery.** The hardened-TLS step often paired with this lab —
`config system global` / `set strong-crypto enable`, forcing the FortiGate's own TLS to
1.2/1.3 — **fails on an eval VM** with `command parse error before 'strong-crypto'` and
`Return code -61`, even when `get system status` reports `License Status: Valid`. The tell
that it is gated rather than mistyped: the field shows in `get system global` as a read-only
`disable`, is absent from `show full-configuration system global`, and `set
ssl-min-proto-version TLSv1-2` is rejected the same way (it stays pinned at `SSLv3`). The
FGVMEV evaluation runs the appliance in **low-encryption mode only**, which compiles those
knobs out — no CLI, toggle, or reboot re-enables them; only a paid or FortiFlex license lifts
the restriction. The sting is downstream: the FortiGate's *outbound* SMTP `STARTTLS` to your
mail server may fail to negotiate on the low-encryption stack, so the OTP email never arrives
— and because an admin with `two-factor email` set can no longer finish a *password* login
without that code, you can lock yourself out of the GUI (SSH public-key auth still works,
being 2FA-exempt). On an eval VM, verify OTP delivery end-to-end before you depend on it, or
leave email OTP off (the teardown above) and rely on `trusthost` plus SSH keys until the box
carries a full license.

**Stronger second factors when you have the infrastructure (RSA SecurID, passkeys/FIDO2).**
Email OTP is the lab-friendly native factor, but a production estate usually wants a
phishing-resistant token, or one it has already deployed. Two common requests — an **RSA
SecurID** token generator, or Apple/platform **passkeys** — are both supported, but neither
is a token type you configure *on* the FortiGate. Each is brokered by an external system
the FortiGate trusts, and knowing which broker to reach for is the point:

- **RSA SecurID — via RADIUS.** FortiOS's native second factors are FortiToken (Mobile or
  hardware), FortiToken Cloud, email, and SMS; RSA is not among them. Instead, point the
  FortiGate at the **RSA Authentication Manager** RADIUS interface (`config user radius`),
  then bind the admin to that server for remote authentication. RSA validates the passcode —
  a hardware fob or the RSA soft-token app — typically as a RADIUS *challenge* presented
  after the password. A generic RSA or TOTP token **cannot** be imported as a local
  FortiToken (FortiToken accepts only Fortinet-provisioned seeds), so RSA is always
  RADIUS-delegated, never a local token.
- **Passkeys / FIDO2 (including Apple passkeys) — via SAML.** FortiOS 7.6 supports FIDO2
  administrator login with the FortiGate acting as the **WebAuthn relying party** and
  delegating the login to a SAML identity provider. Fortinet's reference path uses
  [FortiAuthenticator as the SAML IdP](https://docs.fortinet.com/document/fortiauthenticator/6.6.0/examples/795009/logging-in-to-fortigate-as-an-administrator-using-fido2-authentication);
  any passkey-capable IdP (Microsoft Entra ID, Okta, Google) works the same way. Because
  Apple passkeys are ordinary FIDO2 credentials synced through iCloud Keychain, a Touch ID /
  Face ID gesture at the IdP satisfies the SAML assertion the FortiGate trusts — configure it
  under the admin's SAML/remote-auth binding
  ([administrator account options](https://docs.fortinet.com/document/fortigate/7.6.4/administration-guide/14906/administrator-account-options)).
  If you instead use **FortiToken Cloud / FortiIdentity Cloud** as the MFA back-end, it
  supports passkeys directly, including hardware FIDO keys such as the FortiToken 410.

Both paths need infrastructure this evaluation VM lacks — an RSA Authentication Manager, or
an IdP plus a SAML trust — which is exactly why email OTP is the right factor for *this* lab.
Delegating admin login to FortiAuthenticator over SAML and signing in with a passkey is the
natural production capstone once that infrastructure exists.

**Rollback:** widen `trusthost1` back to your admin range if you locked yourself to a
lab subnet.

**Lessons learned — a live FortiGate-VM evaluation deployment.** The gotchas scattered
through this chapter and the next two were not invented for teaching; they emerged, in order,
from a single modest goal — *route a ping between two VLANs on a free-eval FortiGate-VM* — and
each one first presented as a different fault than it was. Collected here as a checklist,
because the pattern behind them is the real lesson:

- **Second factors are brokered, not local.** RSA SecurID rides RADIUS; passkeys/FIDO2 ride
  SAML to an IdP — neither is a token type you set on the FortiGate (Lab 4.3).
- **`diagnose firewall iprope lookup` will not evaluate ICMP on 7.6.** A ping-only policy
  cannot be confirmed with the lookup tool; verify with a live ping, or use a TCP flow that
  resolves to the implicit deny to prove least-privilege
  ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md), Lab 6.1).
- **An unlicensed FortiGate-VM forwards no traffic.** Management and local pings work while
  every *forwarded* packet is dropped before the policy engine — it reads exactly like a
  broken rule, but the license is the block (the licensing gotcha above).
- **The LENC (low-encryption) image cannot be licensed at all.** It tops out below TLS 1.2,
  so FortiCare activation silently no-ops; only a standard-image redeploy cures it.
- **The free evaluation enforces a 3-interface / 3-policy / 3-route budget, and the built-ins
  spend it.** Over-budget interfaces are purged at boot; reclaim slots from
  `fortilink`/`default-mesh`, or fit the design under the cap.
- **When VLAN sub-interfaces will not fit, tag at the hypervisor.** One vNIC per segment as an
  access port turns two VLANs into two physical ports and fits the eval budget — at the cost
  of making the hypervisor bridge part of the trust boundary
  ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.1
  variant).
- **Strong crypto is eval-gated.** `set strong-crypto enable` fails on an eval VM even when
  licensed, which can break outbound STARTTLS email OTP and lock a password login out (the
  email-OTP teardown above).

The meta-lesson: on a virtualized security appliance, **the license tier and the hypervisor
are part of the topology.** Faults that present as routing or policy problems are frequently
license limits, image variants, or bridge tags in disguise — rule those out before you
rebuild a working rule.

### Lab 4.4 — Firmware management (Topic: Firmware lifecycle)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Read the firmware state and validate an upgrade path before applying.

```text
get system status | grep -i Version
diagnose sys firmware upgrade-paths 2>/dev/null | head
execute backup config flash pre-upgrade
```

**Expected result:** the running build, the supported upgrade path (FortiOS enforces
stepping through intermediate releases), and a saved pre-upgrade config revision —
firmware changes follow the vendor upgrade path and are always preceded by a backup.

**Negative test:** jump several major versions in one step; the FortiGate rejects it or
corrupts the config — skipping the documented upgrade path is unsupported.

**Rollback:** none (no actual upgrade performed).

### Lab 4.5 — Operation mode and global settings (Topic: NAT vs transparent, system settings)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Read the operation mode and set the hostname/timezone.

```text
get system settings | grep -i opmode
config system global
    set hostname LAB-FGT-01
    set timezone 04
end
get system global | grep -iE "hostname|timezone"
```

**Expected result:** the mode reported as `nat` (routed, the default) — transparent
mode makes the FortiGate a bump-in-the-wire L2 device — and the hostname/timezone
applied, which timestamps every log correctly.

**Negative test:** troubleshoot logs across sites with the timezone left at default;
event correlation is off by hours — accurate time is a prerequisite for forensics.

**Rollback:** restore your lab hostname if changed.

### Lab 4.6 — Admin profiles and role-based access (Topic: Administrative roles)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Create a read-only admin profile and account.

```text
config system accprofile
    edit read-only
        set secfabgrp read
        set ftviewgrp read
        set sysgrp read
        set fwgrp read
        set loggrp read
    next
end
config system admin
    edit auditor
        set accprofile read-only
        set password <set-a-strong-password>
    next
end
```

**Expected result:** the `auditor` account can view configuration and logs but cannot
change policy — least-privilege RBAC so operators, auditors, and admins get only the
access their role needs.

**Negative test:** give every operator the `super_admin` profile; any one of them can
disable security or exfiltrate config — role separation is what this profile enforces.

**Rollback:**

```text
config system admin
    delete auditor
end
config system accprofile
    delete read-only
end
```

### Lab 4.7 — Deploying the FortiGate-VM appliance (Topic: FortiGate-VM deployment)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Stand up a FortiGate-VM from a downloaded image, complete the
first-boot console login, reach the GUI on the default management address, and
confirm the evaluation-license state — the appliance that Labs 4.1–4.6 assume
is already running.

**Prerequisites (this lab only):** any hypervisor the encyclopedia covers (Step 1 and the deployment
appendix list them) and a FortiGate-VM image such as
`fortinet-FGT-v7.6.2.F-build3462.tgz` (the EVE-NG package: FortiOS 7.6.2, build
3462) or the equivalent `FGT_VM64_KVM-v7.6.2.F-build3462-FORTINET.out.kvm.zip`
(the KVM qcow2 disk). **Cost:** none — FortiGate-VM boots in evaluation mode
with no purchased license.

**Step 1 — Deploy the FortiGate-VM on your hypervisor.** Fortinet ships a per-platform image:
the KVM `qcow2` (`FGT_VM64_KVM-*.out.kvm.zip` — used by Proxmox, KVM/QEMU, EVE-NG, GNS3, and
containerlab), the VMware OVF (`FGT_VM64-*.out.ovf.zip` — ESXi/vSphere, Workstation/Fusion,
VirtualBox), the Hyper-V VHD (`FGT_VM64_HV-*.out.hyperv.zip`), the Xen image
(`FGT_VM64_XEN-*`), and a Nutanix AHV `qcow2`. Import the form factor your hypervisor uses and
create the VM with **≥ 1 vCPU and ≥ 2 GB RAM** (the FortiOS 7.6 minimum) and at least the
interfaces your topology needs — the evaluation instantiates up to three. The per-hypervisor
create/import/NIC mechanics are the same for every appliance and are collected once in the
Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md).

For example, on **Proxmox VE**:

```text
unzip FGT_VM64_KVM-*.out.kvm.zip                 # -> fortios.qcow2
qm create 900 --name fgt --cores 1 --memory 2048 --scsihw virtio-scsi-pci \
  --serial0 socket --net0 virtio,bridge=vmbr0
qm importdisk 900 fortios.qcow2 local-lvm
qm set 900 --virtio0 local-lvm:vm-900-disk-0 --boot order=virtio0
qm start 900
```

On **EVE-NG** the qemu image *directory name is the version string* and the disk must be
`virtioa.qcow2` — `tar zxf fortinet-FGT-*.tgz --strip-components=1` into
`/opt/unetlab/addons/qemu/fortinet-FGT-<version>/`, then `unl_wrapper -a fixpermissions`, and add
the node to the canvas.

**Step 2 — First-boot console login.** Boot the VM and open its console.
FortiGate-VM ships with username `admin` and an **empty** password; FortiOS 7.6
forces a password change on first login:

```text
FortiGate-VM64-KVM login: admin
Password:                       # empty — press Enter
You are forced to change your password. Please input a new password.
New Password: ********
Confirm Password: ********
```

**Step 3 — Confirm the build and the VM/eval-license state:**

```text
get system status
```

**Expected result:** the header reports the image and its evaluation state:

```text
Version: FortiGate-VM64-KVM v7.6.2,build3462 (GA.F)
Serial-Number: FGVMEV0000000000
License Status: Warning
VM Resources: 1 CPU/1 allowed, 1024 MB RAM/2048 MB allowed
```

The `FGVMEV` serial, `License Status: Warning`, and the capped `1 CPU allowed`
are normal for an unlicensed FortiGate-VM — it runs, but vCPU count and
throughput stay limited until a `.lic` is installed.

**Step 4 — Reach the GUI.** FortiGate-VM defaults `port1` to `192.168.1.99/24`
with management access already enabled:

```text
show system interface port1
    edit "port1"
        set ip 192.168.1.99 255.255.255.0
        set allowaccess ping https ssh http fgfm
    next
```

Put a host on that subnet and browse to `https://192.168.1.99`; the FortiOS
login page loads. If your hypervisor instead bridges `port1` to a DHCP network,
read the leased address with `get system interface physical | grep -A1 port1`.

**Step 5 (optional) — Install the VM license** to leave evaluation mode. Upload
the `.lic` from *System > FortiGuard > VM License* in the GUI, or from the CLI:

```text
execute restore vmlicense tftp FGVM.lic 10.10.10.5
get system status | grep -i "License Status"     # -> License Status: Valid
```

**Expected result:** with a valid `.lic`, `License Status: Valid`, the vCPU cap
rises to the entitlement you purchased, and FortiGuard contracts appear — which
Lab 4.2 then verifies.

**Negative test:** boot the VM with only 512 MB of RAM, or point the hypervisor
at the `.out` upgrade file instead of the full disk image; FortiOS fails to
start or comes up in a limited conserve-mode state — the full disk image and the
vendor-minimum resources (≥ 1 vCPU and ≥ 2 GB RAM for FortiOS 7.6) are what a
healthy first boot needs.

**Rollback:** snapshot the freshly-deployed VM as your lab baseline, or
`execute factoryreset` to hand a known-clean appliance to Lab 4.1.

### Lab 4.8 — Upgrading firmware over TFTP from the CLI (Topic: Firmware lifecycle)

**Eval FortiGate — capable via CLI (GUI upgrade blocked).** The GUI upgrade wizard refuses
an evaluation FortiGate-VM because the evaluation tier carries no FortiGuard firmware-upgrade
entitlement; the CLI `execute restore image tftp` performs no entitlement check and completes
the upgrade with the configuration and license intact. See the licensing Gotcha above for the
reason and the elimination steps behind it.

**Objective:** Upgrade a FortiGate-VM from the CLI by pulling a firmware image from a TFTP
server — the supported path when the GUI upgrade is unavailable — and confirm that the
configuration and the evaluation license survive the reboot.

**Prerequisites (this lab only):** a running FortiGate-VM (this lab upgrades one from FortiOS
7.6.7); a TFTP server reachable on the same subnet with the target image staged in its root —
the Alpine `in.tftpd` server built in
[Volume CLXXI, Lab 5.1](../../volume-171-alpine-linux/chapters/05-building-a-linux-tftp-server-on-alpine.md)
serves this role at `10.30.99.50`; and the matching build for the platform — for KVM,
`FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out`. **Cost:** none. **Confirm the path first:**
FortiOS enforces stepping through intermediate releases on multi-version jumps, so verify that
7.6.7 → 8.0.0 is a single supported step on the Fortinet Upgrade Path tool before proceeding.

**Step 1 — Record the current build and back up the configuration:**

```text
FGT-LAB-01 # get system status | grep -i Version
Version: FortiGate-VM64-KVM v7.6.7,build3704 (GA.F)
FGT-LAB-01 # execute backup config flash pre-8.0-upgrade
FGT-LAB-01 # execute backup config tftp fgt-pre-upgrade.conf 10.30.99.50
```

**Expected result:** the running 7.6.7 build and a saved configuration revision, both on
flash and on the TFTP server — a firmware change is always preceded by a backup.

**Step 2 — Verify the image on the TFTP server, then confirm reachability.** On the TFTP
host, checksum the staged file so a truncated transfer is caught before it reaches the
firewall:

```text
tftp-server:~# md5sum /tftpboot/FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out
5a7da77d58860321789b133e967bdb7d  /tftpboot/FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out
```

From the FortiGate, confirm the server answers:

```text
FGT-LAB-01 # execute ping 10.30.99.50
PING 10.30.99.50 (10.30.99.50): 56 data bytes
64 bytes from 10.30.99.50: icmp_seq=0 ttl=64 time=0.4 ms
```

**Expected result:** a matching MD5 and a successful ping — the image is intact and the
transport path to the TFTP server is open.

**Step 3 — Run the CLI upgrade.** `execute restore image tftp` downloads the image, verifies
it, writes it, and reboots into it:

```text
FGT-LAB-01 # execute restore image tftp FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out 10.30.99.50
This operation will replace the current firmware version!
Do you want to continue? (y/n)y

Please wait...
Connect to tftp server 10.30.99.50 ...
Get image from tftp server OK.
Check image OK.
This operation will download and upgrade the firmware, and the system will reboot.
Do you want to continue? (y/n)y

Image checking...
Programming the boot device now.
Please wait for system to restart.
```

**Expected result:** the image transfers, passes the internal checksum, and the appliance
reboots into the new firmware — with no GUI entitlement check anywhere in the flow.

**Step 4 — After the reboot, confirm the new build and that the configuration and license
survived:**

```text
FGT-LAB-01 # get system status | grep -i Version
Version: FortiGate-VM64-KVM v8.0.0,build0167 (GA.F)
FGT-LAB-01 # diagnose debug vm-print-license | grep -i model
Model: EVAL
FGT-LAB-01 # show firewall policy | grep name
        set name "web-to-db"
        set name "hmi-to-plc"
        set name "deny-mgmt-db"
```

**Expected result:** the new 8.0.0 build, an intact `Model: EVAL` license, and the
pre-upgrade policy set still present — the CLI restore is config- and license-preserving,
unlike re-deploying a factory disk image.

**Negative test:** attempt the same upgrade from the GUI wizard on the evaluation license; it
is refused with *"The FortiGuard license for firmware upgrades could not be verified"* before
the file is even accepted — the CLI `execute restore image tftp` is the supported path when no
firmware-upgrade entitlement is present. Note also that an 8.0.0 FortiGate-VM's GUI is itself
unusable under evaluation (the licensing Gotcha above); plan to manage the upgraded appliance
over CLI/API, or stay on 7.6.7 where GUI access is required.

**Rollback:** snapshot the upgraded VM as a new baseline, or `execute restore image tftp` the
7.6.7 image back to return the appliance to a GUI-capable state for later labs.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter took FGT-LAB-01 from [Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md)'s factory-default state
through a complete first deployment: hostname and time synchronization,
FortiCare registration and FortiGuard licensing, a properly restricted
management interface, and baseline hardening covering password policy,
trusted hosts, and MFA on the administrator account. This hardened,
licensed baseline is the foundation [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) builds on for interfaces,
routing, NAT, VDOMs, and high availability.

- [ ] Can explain the FortiOS `config`/`edit`/`set`/`next`/`end` model and
      global vs. VDOM configuration scope.
- [ ] Can describe FortiGuard licensing bundles and FortiGate-VM licensing
      by vCPU.
- [ ] Can configure hostname, DNS, NTP, and a restricted management
      interface from the CLI.
- [ ] Can apply password policy, trusted hosts, and MFA hardening to an
      administrator account.
- [ ] Can upgrade a FortiGate-VM over TFTP from the CLI when the GUI upgrade
      is blocked on evaluation, preserving configuration and license.
- [ ] Completed the hands-on lab, including the negative test.
