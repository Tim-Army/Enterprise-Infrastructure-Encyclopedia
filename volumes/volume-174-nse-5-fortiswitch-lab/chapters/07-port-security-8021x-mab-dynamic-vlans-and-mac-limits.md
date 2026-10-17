# Chapter 07: Port Security: 802.1X, MAB, Dynamic VLANs, and MAC Limits

## Learning Objectives

- Explain how 802.1X works on a managed FortiSwitch: the switch is the
  authenticator, the RADIUS server decides, and the FortiGate holds the policy
  objects and must pass the switch's RADIUS traffic through a firewall policy.
- Prepare the controller's RADIUS side: the `radius-174` server object, a user
  group for the switch to use, and the global 802.1X settings, and test them
  with `diagnose test authserver`.
- Build an **802.1X security policy** (port-based and MAC-based), apply it to a
  managed port, authenticate endpoint A with `wpa_supplicant`, and read the
  session from the controller and from the switch.
- Configure **MAC authentication bypass (MAB)**, the authentication order and
  priority, a **guest VLAN**, an **auth-fail VLAN**, and a **dynamic VLAN**
  returned by RADIUS as an ID or as a name, and write the matching FreeRADIUS
  entries.
- Limit the number of MAC addresses a port or VLAN learns, read the
  learning-limit violation log, and make learned MAC addresses persistent with
  **sticky MAC**; state which switch models lack the per-VLAN limit (feature
  matrix note 3) and why sticky MAC and 802.1X are not used on the same port.

## Theory and Architecture

### Who does what in FortiLink mode

802.1X has three roles. The **supplicant** is software on the endpoint (here
`wpa_supplicant` on endpoint A). The **authenticator** is the switch port: it
blocks the port, relays the Extensible Authentication Protocol (EAP) exchange
between the supplicant and the server, and opens the port when the server
says yes. The **authentication server** is RADIUS (here FreeRADIUS on
`radius-174`).

On a managed FortiSwitch these roles land as follows (FortiLink Guide 7.6.7,
pp. 216–217):

| Piece | Where it lives | Configured with |
| --- | --- | --- |
| Authenticator | The managed FortiSwitch port | `port-security-policy` on the port (FortiGate) |
| Security policy (the FortiSwitch "security profile") | The FortiGate, pushed to the switch | `config switch-controller security-policy 802-1X` |
| Global 802.1X timers | The FortiGate, pushed to the switch; a per-switch override exists | `config switch-controller 802-1X-settings`; `config 802-1X-settings` under the managed-switch entry |
| RADIUS server and user group | The FortiGate; the policy names a user group whose member is the RADIUS server | `config user radius`, `config user group` |
| RADIUS packets | **From the switch** to the RADIUS server, through the FortiGate | A firewall policy from the FortiLink interface to the server |

The last row is the one that is easy to miss. The guide says that in FortiLink
mode you must create a firewall policy by hand to allow RADIUS traffic for
802.1X from the switch (for example, from the FortiLink interface) to the
RADIUS server through the FortiGate (p. 216). This volume built that policy in
Chapter 02: P2, `P2-fortilink-services`, allows UDP 1812–1813 from the
FortiLink port to `radius-174`. On C1 it applies source NAT, so FreeRADIUS sees
the switch's requests from `10.200.0.175` (the `c1-svc` client); on C2 and C3 it
does not, so they arrive from the switch's FortiLink address and match the
`fortilink-174` client (`10.255.1.0/24`). No new policy is needed in this
chapter, and the C2 budget is unchanged.

The managed switch supports EAP-PEAP, EAP-TTLS, and EAP-TLS; EAP-MD5 is not
supported (pp. 216, 247). This chapter uses PEAP with MSCHAPv2 inside, the
FreeRADIUS default inner method.

### Port-based and MAC-based authentication

`security-mode` chooses one of two modes (FortiLink Guide 7.6.7, pp. 228–229):

| Mode | Option | Use it when | What a dynamic VLAN changes |
| --- | --- | --- | --- |
| Port-based | `802.1X` (default) | One 802.1X-capable client is connected directly to the port | The port's native VLAN (FortiSwitchOS 7.6.7 Administration Guide, p. 192) |
| MAC-based | `802.1X-mac-based` | More than one device on the port must be authenticated, each by its MAC address | Only that client's MAC address; the native VLAN of the port is unchanged (p. 193) |

In MAC-based mode a port holds up to 20 client sessions, and each switch has a
model total (FortiLink Guide 7.6.7, p. 217):

| Model family | Sessions per switch |
| --- | --- |
| 108 (S1) | 80 |
| 124, 224 (S2, FS-224E on S3) | 240 |
| 148, 248 (FS-248E on S3) | 480 |

### MAB and the authentication order

Devices such as printers and sensors cannot run a supplicant. With **MAC
authentication bypass** (`mac-auth-bypass enable`), the switch sends the
device's MAC address to RADIUS as both the user name and the password
(FortiLink Guide 7.6.7, p. 216). The format of that MAC address is set in the
global 802.1X settings: hyphen delimiters and lowercase by default
(`mac-username-delimiter`, `mac-password-delimiter`, `mac-case`; FortiOS 7.6.0
CLI Reference), so a device `AA:BB:CC:DD:EE:FF` is sent as
`aa-bb-cc-dd-ee-ff`. The RADIUS server must hold an entry for every MAB device;
FortiSwitchOS does not keep a MAC list of its own for MAB (Administration Guide,
p. 200).

From FortiOS 7.6.0, two options shape the order when MAB and EAP are both on
(FortiLink Guide 7.6.7, pp. 234–240; both need `mac-auth-bypass enable`):

| Option | Values | Meaning |
| --- | --- | --- |
| `auth-priority` | `legacy` (default), `dot1x-mab`, `mab-dot1x` | `legacy`: EAP and MAB in the order received, EAP with absolute priority, no delay. `dot1x-mab`: EAP first, MAB if EAP fails. `mab-dot1x`: MAB first, EAP if MAB fails |
| `auth-order` | `dot1x-mab`, `mab-dot1x` (default in the 7.6.0 reference), `mab` | `mab` is **MAB-only**: the switch sends no EAP packets at all (FortiOS 7.6.0 with FortiSwitchOS 7.2.3 and later) |

The guide is not consistent about where a failed `legacy` client goes: one page
says to the auth-fail VLAN (p. 235), the option table says to the guest VLAN
(p. 240). This lab gives both the same VLAN, so the outcome does not depend on
which page is right; the session state in the diagnostics says which path was
taken.

### Guest, auth-fail, and server-timeout VLANs

A security policy can give a client restricted access instead of none:

| VLAN | Options | Who lands there |
| --- | --- | --- |
| Guest VLAN | `guest-vlan enable`, `guest-vlan-id <VLAN name>`, `guest-auth-delay` (1–900 s, default 30) | Clients that do not answer 802.1X (no supplicant) after the delay |
| Auth-fail VLAN | `auth-fail-vlan enable`, `auth-fail-vlan-id <VLAN name>` | Clients that tried and failed |
| Server-timeout VLAN | `authserver-timeout-vlan enable`, `authserver-timeout-vlanid`, `authserver-timeout-period` (3–15 s, default 3) | Clients whose RADIUS server did not answer (untagged, from FortiSwitchOS 6.4.3) |
| Server-timeout tagged VLAN | `authserver-timeout-tagged {disable \| lldp-voice \| static}`, `authserver-timeout-tagged-vlanid` | The same, as a tagged VLAN; MAC-based mode only, from FortiOS 7.4.4 |

The options and defaults are from the FortiOS 7.6.0 CLI Reference; the behavior
is from the FortiLink Guide 7.6.7 (pp. 216, 228–229). The VLAN ID options take
a FortiGate VLAN interface name of at most 15 characters. **Monitor mode**
(`open-auth enable`) lets traffic flow even when authentication fails, for
testing a rollout without locking anyone out (p. 240).

### Dynamic VLANs from RADIUS

RADIUS can return a VLAN in its Access-Accept with three attributes
(Administration Guide, p. 193; RFC 3580):

| Attribute | Value | FreeRADIUS dictionary |
| --- | --- | --- |
| `Tunnel-Type` (64) | `VLAN` (13) | `dictionary.rfc3580` defines the value `VLAN` |
| `Tunnel-Medium-Type` (65) | `IEEE-802` (6) | `dictionary.rfc2868` |
| `Tunnel-Private-Group-Id` (81) | The VLAN ID or a VLAN name | `dictionary.rfc2868` (a string) |

The switch reads `Tunnel-Private-Group-Id` two ways (FortiLink Guide 7.6.7,
p. 221). An integer is used as the VLAN ID. A string is matched against the
**description** of the switch's VLANs, and in FortiLink mode the controller
copies each FortiGate VLAN interface name (up to 15 characters) into that
description. So `"1743"` and `"fsw-iot"` both select VLAN 1743 in this lab.
`vlan-identity description` under `config switch-controller global` copies the
interface's description (up to 63 characters) instead of its name (FortiOS
7.4.1 and later). If several VLANs carry the same name, the managed switch picks
the one with the lowest `assignment-priority` (1–255, default 128; set under the
managed-switch entry's `config vlan`), from FortiOS 7.4.2 with FortiSwitchOS
7.4.2 (pp. 222–223). The guide notes that VLAN-by-name, RADIUS accounting, and
CoA need `eap-passthru enable` (p. 246), which is the default.

**Spanning tree.** The FortiSwitchOS Administration Guide suggests disabling STP
on 802.1X ports, or else making sure their STP instance holds the dynamic,
guest, and auth-fail VLANs; otherwise connectivity fails once a port moves into
one of them (p. 247). Chapter 05 mapped `fsw-users`, `fsw-voice`, `fsw-iot`, and
`fsw-guest` to MSTP instance 1, so every VLAN this chapter assigns is in the same
instance as the ports' native VLANs. `port1` and `port2` keep STP and BPDU guard.

### Global 802.1X settings and session control

| Option (`config switch-controller 802-1X-settings`) | Default | Meaning |
| --- | --- | --- |
| `link-down-auth` | `set-unauth` | A link-down makes the port unauthenticated, so the client must authenticate again |
| `reauth-period` | 60 | Reauthentication interval; 0 disables it |
| `max-reauth-attempt` | 3 | Reauthentication attempts; 0 disables them |
| `tx-period` | 30 | 802.1X transmission period in seconds |
| `mab-reauth` | `disable` | Whether MAB sessions reauthenticate |
| `mac-username-delimiter`, `mac-password-delimiter`, `mac-case` | `hyphen`, `hyphen`, `lowercase` | The MAB user name and password format |

The defaults are from the FortiOS 7.6.0 CLI Reference. Its text gives
`reauth-period` in seconds (range 1–1440) while the FortiLink Guide (p. 218) and
the Administration Guide (p. 207) give minutes; the session output prints
`reAuth=` with a value, so read it from your own switch rather than trusting
either page. Under the managed-switch entry, `config 802-1X-settings` with
`local-override enable` overrides these for one switch (pp. 218–220). Sessions
are cleared from the controller with `execute switch-controller switch-action
802-1X clear-auth-port` or `clear-auth-mac` (p. 241), or on the switch with
`execute 802-1x clear interface` (FortiSwitchOS 7.6.7 CLI Reference).

Three newer features appear in the guide but need builds later than FGT-1's
7.6.2, so this chapter only reads about them: 802.1X user groups in firewall
policies (the `Fortinet-Group-Name` attribute) and NAC together with 802.1X on
one port, both from FortiOS 7.6.4 with FortiSwitchOS 7.6.4 (pp. 230–234), and
dynamic access control lists (DACLs) from RADIUS, from FortiOS 7.4.4
(pp. 223–227); the 7.6.7 feature matrix lists Dynamic ACLs (IPv4) for both
the 1xxE/1xxF and 200 Series columns.

### MAC learning limits, the violation log, and sticky MAC

A **MAC learning limit** caps how many dynamic MAC addresses a port or a VLAN
learns, from 1 to 128; 0, the default, means no limit, and static MAC addresses
do not count (FortiLink Guide 7.6.7, pp. 141–142). In FortiOS 7.6.0 the two
limits are:

| Scope | Where | Option |
| --- | --- | --- |
| Port | `config switch-controller managed-switch`, `config ports` | `learning-limit <0-128>` |
| VLAN | `config system interface`, the FortiSwitch VLAN interface | `switch-controller-learning-limit <0-128>` |

The FortiLink Guide prints the per-VLAN form as `set
switch-controller-learning-limit` under `config switch vlan` (p. 142), which
mixes the FortiGate option name with the switch-side table; the FortiOS 7.6.0
reference puts the option under `config system interface`, and this chapter uses
that.

The **learning-limit violation log** records the first MAC address that exceeded
a limit on each port or VLAN; it is off by default and is enabled with
`log-mac-limit-violations enable` (and its retention set with
`mac-violation-timer`) under `config switch-controller global` (p. 143). It is
read with `diagnose switch-controller switch-info mac-limit-violations` on the
controller or `get switch mac-limit-violations` on the switch, and reset with
`execute switch-controller mac-limit-violation reset`. The FortiOS 8.0.1 CLI
Reference prints the reset as `execute switch-controller switch-action
mac-limit-violation reset`; type `?` to see which form your build takes.

A **learning-limit violation action** (`learning-limit-action {none |
shutdown}`, physical ports only) exists on the switch side
(`config switch interface`, FortiSwitchOS 7.6.7 CLI Reference, p. 130). The
FortiOS 7.6.0 managed-switch `ports` table has no matching option, so this
chapter does not set it in FortiLink mode; Chapter 11 can use it standalone.

**Sticky MAC** (`sticky-mac enable` on a port) keeps dynamically learned MAC
addresses when the port goes down and up; they are lost at a reboot unless saved
to the switch configuration with `execute switch-controller switch-action
sticky-mac save`, and unsaved entries are removed with `... sticky-mac
delete-unsaved` (FortiLink Guide 7.6.7, p. 144). Two warnings come with it: a
device with a sticky entry that moves to another port is not learned on the new
port until the entry is cleared, and static or sticky MAC addresses and 802.1X
are **not used on the same port** (Administration Guide, pp. 247, 362; FortiLink
Guide, p. 246). That is why Lab 7.4 removes the security policy from `port2`
first.

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| 802.1X port mode, MAC-based mode | Chain | Chain | |
| User-based (802.1X) VLAN assignment | Chain | Chain | |
| Priority for dynamic or egress VLAN assignment | Chain | Chain | |
| MAB, MAB entry aging, 802.1X/MAB priority | Chain | Chain | |
| Limiting the number of MAB sessions | Check | Check | Standalone only |
| Tagged VLAN for authserver-timeout | Chain | Chain | |
| open-auth (monitor) mode | Chain | Chain | |
| EAP pass-through | Chain | Chain | |
| RADIUS accounting server, CoA and disconnect messages | Chain | Chain | |
| RadSec | Check | Check | Standalone only |
| MAC learning limit | Chain | Chain | Note 3: no **per-VLAN** limit on the FS-108F, FS-124F (all variants), FS-124E, FS-110G-FPOE, FS-124G, FS-248E-POE, FS-248E-FPOE, and FS-248D; no **per-trunk** limit on the FS-248E-POE, FS-248E-FPOE, and FS-248D |
| Learning-limit violation log | Check | Check | Standalone only in the matrix, although the controller has the command |
| Learning-limit violation action | Chain | Check | |
| Sticky MAC | Chain | Chain | |

So the per-port limit and sticky MAC are hands-on on every switch option, but
the per-VLAN limit is hands-on only on an S3 pair of FS-224E switches; on S1, S2,
and an FS-248E-POE or -FPOE pair it is read-and-predict.

## Design Considerations

### The VLANs this chapter uses

| Role | VLAN | Why it fits |
| --- | --- | --- |
| Native VLAN of `port1` (endpoint A) | `fsw-users` 1741, DHCP `.100`–`.199` | Chapter 04's user VLAN |
| Native VLAN of `port2` (endpoint B) | `fsw-iot` 1743, endpoint B static `10.174.43.20` | Chapter 04's device VLAN, the natural home of a MAB device |
| Dynamic VLAN from RADIUS | `fsw-iot` 1743 (by name for endpoint A, by ID for endpoint B) | In MSTP instance 1 with the native VLANs |
| Guest and auth-fail VLAN | `fsw-guest` 1744, no DHCP | Chapter 01 reserved it for this; restricted by design |

All four are in instance 1 (Chapter 05), which satisfies the Administration
Guide's STP rule. `fsw-guest` has no DHCP server, so a client placed there gets
no lease; the labs give the endpoint a static address in `10.174.44.0/24` to
prove where it landed. The lab VLANs are members of `FSW-LAN`, whose
`intrazone deny` keeps a guest from reaching the user VLANs.

After a C2 lab-VLAN NO-GO in Lab 4.1, Chapter 04 sends this chapter to C1 or C3.
On C2 itself, Lab 7.1 runs as written, Lab 7.2 runs on `port1` with the native
VLAN `video`, Lab 7.4's per-port steps run, and the VLAN assignment parts of Lab
7.3 are read-and-predict.

### The RADIUS side

| Object | Built in | Contents |
| --- | --- | --- |
| `radius-174` server object | Chapter 02 | `10.200.0.174`, `<RADIUS_SECRET>` |
| FreeRADIUS clients | Chapter 02 | `fgt-1` `10.200.0.1`, `c1-svc` `10.200.0.175`, `fortilink-174` `10.255.1.0/24`, one secret |
| `labuser` | Chapter 02 | Password only; no reply attributes |
| User group `dot1x-174` | Lab 7.1 | Member `radius-174`; the security policies name it |
| `vlanuser` | Lab 7.3 | Password and the three tunnel attributes, VLAN by **name** (`fsw-iot`) |
| Endpoint B's MAB entry | Lab 7.3 | User name and password `<MAC_B_HYPHEN>`; tunnel attributes with VLAN by **ID** (`1743`) |
| Inner-tunnel reply copy | Lab 7.3 | The FreeRADIUS change that lets PEAP replies carry the tunnel attributes |

The last row matters for PEAP. FreeRADIUS processes the PEAP user's password
check in the `inner-tunnel` virtual server, and reply attributes found there do
not reach the outer Access-Accept that the switch reads unless they are copied.
The stock `sites-available/inner-tunnel` file contains that copy in its
`post-auth` section, disabled by `if (0)`, and says to change it to `if (1)`
instead of using the older `use_tunneled_reply` (FreeRADIUS 3.2
`inner-tunnel`). MAB uses PAP in the outer server, so its reply attributes need
no copy.

Track 2 runs the whole RADIUS side live: the user group, the FreeRADIUS entries,
`radtest` on `radius-174`, and `diagnose test authserver` from the controller.
Only the switch's own requests are missing.

### Port plan for this chapter

| Port | Lab 7.2 | Lab 7.3 | Lab 7.4 | After the chapter |
| --- | --- | --- | --- | --- |
| `port1` (endpoint A) | `dot1x-174-port` (port-based) | Same policy with guest and auth-fail VLANs; dynamic VLAN for `vlanuser` | No policy | Native `fsw-users`, no security policy |
| `port2` (endpoint B) | Unchanged | `mab-174` (MAC-based, MAB-only) | No policy; learning limit, then sticky MAC | Native `fsw-iot`, no security policy, no limit, sticky MAC off |

### What to keep after this chapter

| Object | Kept | Why |
| --- | --- | --- |
| User group `dot1x-174` (member `radius-174`) | Yes | Chapter 09 and Lab 12.5 can reuse it |
| Security policies `dot1x-174-port` and `mab-174` | Yes, attached to no port | Ready objects; Chapter 08 and 09 ports start without 802.1X |
| `port-security-policy` on `port1` and `port2` | No | Removed at the end of Labs 7.3 and 7.4 |
| FreeRADIUS entries `vlanuser` and `<MAC_B_HYPHEN>`; inner-tunnel copy enabled | Yes | Chapter 09 can use endpoint B's MAB entry |
| Global `802-1X-settings` | Defaults | Nothing in the labs changes them |
| `learning-limit`, `sticky-mac`, sticky entries, per-VLAN limit | No | Lab 7.4 removes them |
| `log-mac-limit-violations` | Back to `disable` | Lab 7.4 turns it on only for the test |
| `wpa_supplicant` on endpoint A | Stopped | Endpoint A returns to plain DHCP |

## Implementation and Automation

The labs are the implementation. Four habits make 802.1X work traceable.

**Watch the server.** Every decision is made on `radius-174`; its debug mode
prints each request, the client it came from, the user name, and the reply
attributes it sends. Stop the service and run it in the foreground in a second
window during Labs 7.2 and 7.3:

```bash
# on radius-174
sudo systemctl stop freeradius
sudo freeradius -X
```

Press Ctrl+C and run `sudo systemctl start freeradius` when you finish.

**Read both sides of the port.** The controller and the switch print the same
802.1X status block (FortiLink Guide 7.6.7, p. 232; FortiSwitchOS 7.6.7 CLI
Reference, p. 346). The switch command's port argument is optional, so it was
matched to the CLI Reference by hand:

```text
FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
FSW # diagnose switch 802-1x status port1
```

**Start from a clean session.** Clear a port's sessions before each test, so an
old authorization does not answer for a new one:

```text
FGT # execute switch-controller switch-action 802-1X clear-auth-port <SWITCH_SN> port1
```

**Run the supplicant in the foreground first.** `wpa_supplicant -d` prints the
EAP exchange on endpoint A; once it works, run it in the background with `-B`.

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference; `execute`, `diagnose`, and `get` commands against
the FortiLink Guide 7.6.7, or the FortiOS 8.0.1 CLI Reference as a cross-check
where the guide prints no syntax line (each case is marked). Switch commands
were checked against the FortiSwitchOS 7.6.7 CLI Reference; `diagnose switch
802-1x status` and `diagnose switch physical-ports summary` take an optional
port argument and were matched by hand, and `show switch static-mac` is the
`show` form of the documented `config switch static-mac` table. The FreeRADIUS
entries follow `users(5)` and the FreeRADIUS 3.2 `raddb` files; the supplicant
configuration follows `wpa_supplicant.conf(5)`.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| `freeradius -X` shows nothing when endpoint A connects | The switch's RADIUS request is not reaching the server: no security policy on the port, P2 missing or not matching, or the switch has no RADIUS server definition | `diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1`; `show firewall policy <P2_ID>`; `get user radius` on the switch |
| `Ignoring request ... from unknown client` in `freeradius -X` | The source address is not in `clients.conf` (on C1, NAT makes it `10.200.0.175`) | The source address in the message; `clients.conf` |
| Access-Request arrives, then `Access-Reject` | Wrong password, user missing from the users file, or an entry placed below a `DEFAULT` entry that stops processing | `freeradius -X`; move test entries to the top of `authorize` |
| The client authenticates but stays in its native VLAN | The tunnel attributes were not sent (PEAP without the inner-tunnel copy), the name does not match a VLAN description, or `eap-passthru` is disabled | The `Sent Access-Accept` lines in `freeradius -X`; `diagnose switch vlan assignment mac list` on the switch (MAC-based) |
| The client is in the dynamic VLAN but has no connectivity | The VLAN is in a different STP instance from the port's other VLANs, or the endpoint still has its old address | `diagnose stp vlan list <VLAN_ID>` on the switch; the endpoint's address |
| MAB fails for a device that has an entry | The MAC format differs from the entry (delimiter, case) | The `User-Name` in `freeradius -X`; `get switch-controller 802-1X-settings` |
| MAB requests are rejected for a missing Message-Authenticator | The FreeRADIUS `require_message_authenticator` setting for that client | The client's setting in `clients.conf` and its documentation in your version's `radiusd.conf` |
| A second device on a port with `learning-limit 1` cannot communicate | The limit is working: its MAC address was not learned | `diagnose switch mac-address list` on the switch |
| A device moved to another port is not learned there | A sticky entry for it remains on the old port | `execute switch-controller switch-action sticky-mac delete-unsaved interface <SWITCH_SN> <port>` |
| The per-VLAN limit has no effect | Note 3: the model does not support it | Your model against the matrix note |

## Security and Best Practices

- **Prefer 802.1X to MAB.** MAB authenticates a MAC address, which any device
  can copy; give MAB devices their own VLAN with narrow policies, and use
  MAB-only (`auth-order mab`) only on ports meant for such devices.
- **Validate the server certificate.** This lab's supplicant does not check the
  RADIUS server's certificate, which lets a rogue server collect credentials. In
  production, set `ca_cert` in the supplicant configuration and use a server
  certificate from your own CA, not the FreeRADIUS test certificates.
- **Roll out in monitor mode.** `open-auth enable` shows which clients would
  fail without cutting them off; turn it off when the session table is clean.
- **Keep guest and auth-fail VLANs restricted.** They exist to give limited
  access, so give them no route to user VLANs (`intrazone deny` here) and only
  the policies they need.
- **Keep 802.1X VLANs in one STP instance**, or turn STP off on the 802.1X
  ports, as the Administration Guide advises.
- **Do not mix sticky or static MAC entries with 802.1X** on the same port.
- **Protect the RADIUS path.** Keep the shared secret long and unique, limit
  `clients.conf` to the addresses that send requests, and keep the firewall
  policy to UDP 1812–1813 toward the server.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — dynamic MAC learning, learning limits, violation log, sticky MAC
  (pp. 141–144); FortiSwitch security policies, sessions per switch, 802.1X
  settings and override, RADIUS attribute formats, NAS-IP-Address (pp. 216–220);
  dynamic VLAN assignment and assignment priority (pp. 221–223); DACLs
  (pp. 223–227); defining and applying a security policy (pp. 227–230); 802.1X
  user groups and NAC with 802.1X (pp. 230–234); MAB and EAP priority
  (pp. 234–240); monitor mode, clearing sessions, accounting, CoA (pp. 240–244);
  deployment example and notes (pp. 244–247).
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — 802.1X sessions per switch and server-timeout VLANs (pp. 190–191), dynamic
  VLAN assignment and RADIUS attributes (pp. 192–193), MAB (p. 200), global
  settings (pp. 206–207), viewing 802.1X details (pp. 213–214), deployment notes
  including STP and sticky MAC (p. 247), sticky MAC (pp. 362–363).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config switch interface` (`learning-limit`, `learning-limit-action`,
  `sticky-mac`, pp. 129–130), `diagnose switch 802-1x status` (pp. 346–347),
  `diagnose switch mac-address` (pp. 354–355), `diagnose switch vlan assignment
  mac list`, `execute 802-1x clear`, `execute mac-limit-violation reset`
  (pp. 428–429), `execute sticky-mac` (p. 450), `get switch mac-limit-violations`
  (pp. 500–501), `get user group`, `get user radius` (pp. 537–538).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config switch-controller security-policy
  802-1X`, `config switch-controller 802-1X-settings`, `config
  switch-controller global`, `config switch-controller managed-switch`
  (`ports`, `802-1X-settings`, `static-mac`), `config system interface`
  (`switch-controller-learning-limit`), `config user radius`, `config user
  group`.
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose switch-controller
  switch-info mac-table`; `execute switch-controller switch-action
  mac-limit-violation reset`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — the 802.1X rows, MAC learning limit (note 3), violation log and action,
  sticky MAC.
- FreeRADIUS 3.2:
  [`users(5)`](https://manpages.ubuntu.com/manpages/noble/man5/users.5.html)
  (entry format and operators), the stock
  [`mods-config/files/authorize`](https://github.com/FreeRADIUS/freeradius-server/blob/v3.2.x/raddb/mods-config/files/authorize)
  ("add test accounts to the TOP"),
  [`sites-available/inner-tunnel`](https://github.com/FreeRADIUS/freeradius-server/blob/v3.2.x/raddb/sites-available/inner-tunnel)
  (the `post-auth` reply copy),
  [`mods-available/eap`](https://github.com/FreeRADIUS/freeradius-server/blob/v3.2.x/raddb/mods-available/eap)
  (PEAP and the test certificates), and the dictionaries
  [`dictionary.rfc2868`](https://github.com/FreeRADIUS/freeradius-server/blob/v3.2.x/share/dictionary.rfc2868)
  and
  [`dictionary.rfc3580`](https://github.com/FreeRADIUS/freeradius-server/blob/v3.2.x/share/dictionary.rfc3580).
- [`wpa_supplicant.conf(5)`](https://manpages.ubuntu.com/manpages/noble/man5/wpa_supplicant.conf.5.html)
  — the wired Ethernet example (`ap_scan=0`, `key_mgmt=IEEE8021X`, `-Dwired`)
  and the PEAP/MSCHAPv2 example.
- [`ip-link(8)`](https://man7.org/linux/man-pages/man8/ip-link.8.html) — the
  `macvlan` link type used to give endpoint B a second MAC address.

**Knowledge checks**

1. In FortiLink mode, which device sends the RADIUS Access-Request for a client
   on a managed port, and what must exist on the FortiGate for it to reach the
   server?
2. When do you choose MAC-based mode over port-based mode, and what does a
   dynamic VLAN change in each?
3. RADIUS returns `Tunnel-Private-Group-Id = "fsw-iot"`. How does the managed
   switch turn that into a VLAN, and what limits the name's length?
4. What is the difference between `auth-priority mab-dot1x` and `auth-order
   mab`?
5. A client has no supplicant, and another client types the wrong password. With
   a guest VLAN and an auth-fail VLAN configured, where does each go?
6. Why must the dynamic, guest, and auth-fail VLANs share an STP instance with
   the port's native VLAN?
7. On which of S1, S2, and S3 can you set a per-VLAN MAC learning limit, and
   where is that option on the FortiGate?
8. Why is sticky MAC not used on a port that has an 802.1X security policy?

## Hands-On Lab

**Shared prerequisites.** Chapter 06 complete: `<SWITCH_SN>` `Authorized/Up` at
`10.255.1.2` with profile `fsw-174-prof` (on S3, `FSW-A`; `FSW-B` is managed but
not used here); MSTP instance 1 holds `fsw-users`, `fsw-voice`, `fsw-iot`, and
`fsw-guest`; `port1` native `fsw-users` (endpoint A, DHCP) and `port2` native
`fsw-iot` (endpoint B, `10.174.43.20/24`), both with BPDU guard. P2
(`P2-fortilink-services`) in place with `FSW-LAN` among its sources, its policy
ID recorded as `<P2_ID>`. `radius-174` running, with the three clients and
`labuser` from Chapter 02. Endpoint A with `wpasupplicant` installed and endpoint
B's wired MAC address recorded in Lab 2.5. Track 2: `radius-174`, the Lab 2.2
pre-provisioning outcome, and the stand-in entry `S248EPTF18000000` if that
outcome allowed it. **Cost:** none.

As in earlier chapters, `FGT #` is the controller on any option, and blocks
written for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>`.
`<SWITCH_SN>` is your switch's serial number; on Track 2 it is
`S248EPTF18000000`. `<IFACE>` is endpoint A's wired interface and `<IFACE_B>`
endpoint B's. `<MAC_B>` is endpoint B's MAC address as `ip -br link` prints it,
and `<MAC_B_HYPHEN>` the same address in lowercase with hyphens (for example
`aa-bb-cc-dd-ee-ff`). `<LAB_PASSWORD>` is `labuser`'s password from Chapter 02
and `<VLAN_PASSWORD>` a new one for `vlanuser`. Before the first change, back up
the controller:

```text
FGT # execute backup config tftp fgt-pre-7-1-174.conf 10.30.99.50
```

### Lab 7.1 — RADIUS server, user group, and 802.1X settings on the controller

**Objective:** Confirm that the controller authenticates against `radius-174`,
create the user group that the switch's security policies will use, confirm
that the switch's RADIUS requests have a path to the server, and read the global
802.1X settings, including the MAB user name format.

**Platform notes:** Hands-on on C1, C2, and C3 and on Track 2: everything here
is controller and server configuration. The only option difference is the source
address FreeRADIUS will see for the switch's requests: `10.200.0.175` on C1
(P2 uses source NAT), the switch's `10.255.1.x` address on C2 and C3. No switch
option matters; no policy, route, or interface is added (C2: P3 stays free).

**Track 1:**

1. Read the server object and repeat the Chapter 02 test (the argument order is
   from a Fortinet Community troubleshooting tip, as in Lab 2.5):

   ```text
   FGT # show user radius radius-174
   FGT # diagnose test authserver radius radius-174 pap labuser <LAB_PASSWORD>
   ```

   Expect the success line that Lab 2.5 recorded. If it fails now, fix it before
   going on; Chapter 02's troubleshooting table lists the causes.

2. Create the user group. A security policy must name a user group
   (`user-group` is mandatory, FortiLink Guide 7.6.7, p. 229), and the group's
   member is the RADIUS server:

   ```text
   FGT # config user group
   edit "dot1x-174"
   set member "radius-174"
   next
   end
   FGT # show user group dot1x-174
   ```

3. Check the path the switch's own requests will take. The guide requires a
   policy from the FortiLink interface to the RADIUS server (p. 216); P2 is that
   policy:

   ```text
   FGT # show firewall policy <P2_ID>
   ```

   Confirm that `srcintf` includes the FortiLink port, `dstaddr` includes
   `radius-174`, and `service` is `lab-svc-174` (UDP 1812–1813 among its ports).
   On `radius-174`, confirm the client that will match:

   ```bash
   # on radius-174
   sudo grep -A3 -E "client (c1-svc|fortilink-174)" /etc/freeradius/3.0/clients.conf
   ```

4. Read the global 802.1X settings. `get` prints every field, defaults
   included:

   ```text
   FGT # get switch-controller 802-1X-settings
   ```

   Predict `link-down-auth`, `reauth-period`, `max-reauth-attempt`,
   `tx-period`, `mab-reauth`, and the MAB user name format for endpoint B before
   you read. **Answer:** `set-unauth`, 60, 3, 30, `disable` (FortiOS 7.6.0 CLI
   Reference), and `<MAC_B_HYPHEN>`: `mac-username-delimiter` and
   `mac-password-delimiter` default to `hyphen` and `mac-case` to `lowercase`.
   Leave the settings at their defaults.

**Track 2:** Run steps 1 to 4 on your controller; they are all live. Step 3's
policy exists on Track 2 as well (Chapter 02).

**Track 2: read-and-predict.**

1. The FortiLink Guide's deployment example (p. 245) creates a firewall policy
   named `fortilink-to-radius` with `srcintf "fortilink"`, `service "ALL"`, and
   `nat enable`. Predict what changes on the RADIUS server if NAT is on.
   **Answer:** the server sees the FortiGate's egress address instead of the
   switch's, so that address must be the RADIUS client; this is why C1's P2
   requests arrive as `c1-svc`. The guide also notes that RADIUS CoA in FortiLink
   mode needs NAT disabled in that policy and routable FortiLink addresses
   (p. 246); this lab does not use CoA.
2. Predict how many 802.1X security policies a FortiGate can apply to one switch.
   **Answer:** as many as there are ports; the guide says you can define multiple
   policies (p. 227) and apply a different one to each port (p. 230).

**Expected result:** The authserver test succeeds; `dot1x-174` exists with
member `radius-174`; P2 permits the FortiLink port to reach `radius-174` on UDP
1812–1813, and FreeRADIUS has a client for the address the switch's requests will
come from; the global settings are at their defaults, and the MAB user name for
endpoint B is written down as `<MAC_B_HYPHEN>`.

**Negative test:** Test with a wrong password and watch the server:

```text
FGT # diagnose test authserver radius radius-174 pap labuser wrong-password-174
```

The test fails, and `freeradius -X` on `radius-174` shows the request from the
controller's address and an `Access-Reject`. Compare Lab 2.5's negative test: a
wrong **secret** fails before the password is checked, a wrong **password**
fails at the check.

**Rollback:** Delete the group (`config user group`, `delete "dot1x-174"`) only
if you are not continuing; Labs 7.2 and 7.3 need it.

**Lab verified by:** *pending*

### Lab 7.2 — An 802.1X security policy on a managed port

**Objective:** Build a port-based 802.1X security policy, apply it to `port1`,
authenticate endpoint A with `wpa_supplicant` and PEAP, read the session from
both sides, and see the port block an endpoint that does not authenticate.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`): 802.1X port mode and EAP pass-through are chain in the 1xxE/1xxF and
200 Series columns. After a C2 lab-VLAN NO-GO, `port1`'s native VLAN is `video`
and endpoint A needs a static address there. Track 2: build the security policy
live; apply it to the stand-in's `port1` only with Lab 2.2's third outcome
(ports accepted); the session steps are read-and-predict.

**Track 1:**

1. Prepare FreeRADIUS for PEAP. PEAP needs a server certificate; the stock
   `eap` module points at `server.pem` and `ca.pem` in the certificate directory,
   and its comments say that test certificates can be generated with `make` in
   that directory if they were not generated at install (FreeRADIUS 3.2
   `mods-available/eap`). Check that the files exist:

   ```bash
   # on radius-174
   sudo ls -l /etc/freeradius/3.0/certs/
   sudo grep -nE "^\s*(default_eap_type|private_key_file|certificate_file|ca_file)" /etc/freeradius/3.0/mods-enabled/eap
   ```

   If `freeradius -X` later stops with a certificate error, create the files as
   the `eap` file's comments describe. These test certificates are for the lab
   only. Start `sudo freeradius -X` in a second window (Implementation and
   Automation).

2. Create the security policy. Port-based mode, no MAB, no guest or auth-fail
   VLAN yet, monitor mode off:

   ```text
   FGT # config switch-controller security-policy 802-1X
   edit "dot1x-174-port"
   set security-mode 802.1X
   set user-group "dot1x-174"
   set mac-auth-bypass disable
   set guest-vlan disable
   set auth-fail-vlan disable
   set open-auth disable
   next
   end
   FGT # show switch-controller security-policy 802-1X dot1x-174-port
   ```

   `eap-passthru` stays at its default, `enable`.

3. Before applying it, write endpoint A's supplicant configuration. It follows
   the wired example and the PEAP example of `wpa_supplicant.conf(5)`; there is
   no `ca_cert`, so the server certificate is not checked (lab only, see
   Security and Best Practices). Save it as
   `/etc/wpa_supplicant/wired-174.conf` on endpoint A, readable by root only:

   ```text
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   ap_scan=0
   network={
       key_mgmt=IEEE8021X
       eap=PEAP
       identity="labuser"
       password="<LAB_PASSWORD>"
       phase2="auth=MSCHAPV2"
       eapol_flags=0
   }
   ```

   ```bash
   # endpoint A
   sudo chmod 600 /etc/wpa_supplicant/wired-174.conf
   ```

4. Apply the policy to `port1`:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set port-security-policy "dot1x-174-port"
   next
   end
   next
   end
   ```

5. Read the port before endpoint A authenticates:

   ```text
   FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
   FSW # diagnose switch 802-1x status port1
   FSW # get user radius
   FSW # get user group
   ```

   Predict the `Port State` and the session count. **Answer:** not authorized,
   with no client sessions; the port admits only EAPOL frames until a client
   authenticates. The documentation prints only authorized examples, so record
   the exact unauthorized wording. Also record the names that `get user radius`
   and `get user group` list: they are what the controller pushed so that the
   switch can reach `radius-174`.

6. Authenticate endpoint A. Run the supplicant in the foreground first and
   watch both it and `freeradius -X`:

   ```bash
   # endpoint A
   sudo wpa_supplicant -D wired -i <IFACE> -c /etc/wpa_supplicant/wired-174.conf -d
   ```

   In `freeradius -X`, expect a series of Access-Requests from the switch's
   address (C2, C3) or `10.200.0.175` (C1), each answered by an
   `Access-Challenge` while PEAP runs, and finally an `Access-Accept` for
   `labuser`. Once it works, stop it with Ctrl+C and run it in the background:

   ```bash
   # endpoint A
   sudo wpa_supplicant -B -D wired -i <IFACE> -c /etc/wpa_supplicant/wired-174.conf
   sudo wpa_cli -i <IFACE> status
   ```

7. Read the session from both sides:

   ```text
   FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
   FSW # diagnose switch 802-1x status port1
   ```

   Predict the client row and the session line. **Answer:** one client, endpoint
   A's MAC address, `Type` `802.1x`, `Traffic-Vlan` 1741 (the VLAN it was
   authenticated in), `Dynamic-Vlan` 0 (RADIUS returned none), and a session line
   with `PEAP`, `state=AUTHENTICATED`, and `user="labuser"` (the shape of the
   guide's example, pp. 232–233, and the CLI Reference's, p. 347). Record the
   `Mode` line: the documentation's examples are all MAC-based, so the port-based
   wording is yours to record, as is the `reAuth=` value.

8. Get an address and test the path. If endpoint A has no lease yet, bounce
   its link (Lab 4.2 step 4); the supplicant authenticates again after the link
   returns, because `link-down-auth` is `set-unauth`:

   ```bash
   # endpoint A
   ip -br addr show <IFACE>
   ping -c 3 10.174.41.1
   ```

**Track 2:** Run step 2 on your controller. If Lab 2.2's third outcome applies,
run step 4 against `S248EPTF18000000` and check it with `show
switch-controller managed-switch S248EPTF18000000`. Skip the server, endpoint,
and switch steps.

**Track 2: read-and-predict.**

1. The FortiSwitchOS 7.6.7 CLI Reference (pp. 346–347) prints this example of
   `diagnose switch 802-1x status`, trimmed:

   ```text
   S548DF4K15000195 # diagnose switch 802-1x status
   port3 : Mode: mac-based (mac-by-pass disable)
   Port State: authorized: ( )
   Native Vlan : 10
   Allowed Vlan list: 10,15
   Switch sessions 2/240, Local port sessions:2/20
   Client MAC Type Traffic-Vlan Dynamic-Vlan
   94:10:3e:b9:12:65 802.1x 10 0
   cc:5a:53:5f:d5:16 802.1x 10 15
   ```

   Predict which client RADIUS placed in a dynamic VLAN, and what model family
   the switch belongs to. **Answer:** `cc:5a:53:5f:d5:16`, whose `Dynamic-Vlan`
   is 15 (the other shows 0). `Switch sessions 2/240` gives a switch total of
   240, the 124/224/424/524/1024 family in the guide's table (p. 217); the
   prompt in the reference names an FS-548D, so the printed total does not match
   that table's 480, and you should read the total from your own switch.
2. A colleague applies a security policy whose `security-mode` is `802.1X` to a
   port that serves an IP phone with a PC behind it. Predict the problem.
   **Answer:** port-based mode authorizes the port for one client; two devices
   that each authenticate need MAC-based mode (FortiLink Guide 7.6.7, p. 228).
3. Predict whether this lab's PEAP exchange would work with EAP-MD5 instead.
   **Answer:** no; the managed switch does not support EAP-MD5 (pp. 216, 247),
   even though the `wpa_supplicant.conf(5)` wired example uses it.

**Expected result:** Track 1: `dot1x-174-port` exists and is applied to `port1`;
before authentication the port shows no session; after it, one `802.1x` session
for endpoint A in VLAN 1741 with user `labuser`, and endpoint A has a lease and
reaches `10.174.41.1`; `freeradius -X` showed the challenge-and-accept sequence.
Track 2: the policy exists (and is on the stand-in's port, if accepted), and the
predictions are answered.

**Negative test:** Stop the supplicant, clear the session, and try to use the
port:

```bash
# endpoint A
sudo pkill wpa_supplicant
```

```text
FGT # execute switch-controller switch-action 802-1X clear-auth-port <SWITCH_SN> port1
FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
```

```bash
# endpoint A
ping -c 3 10.174.41.1
```

The session is gone and the ping fails: without authentication, the port passes
no traffic. Then run the policy in monitor mode and repeat the ping:

```text
FGT # config switch-controller security-policy 802-1X
edit "dot1x-174-port"
set open-auth enable
next
end
```

Predict and observe: the ping succeeds although nobody authenticated (FortiLink
Guide 7.6.7, p. 240); the guide's example shows the state as
`authorized:open_auth` (p. 232). Set `open-auth disable` again afterwards. Track
2: prediction 2 is the negative test.

**Rollback:** Normally keep the policy on `port1` for Lab 7.3. To remove it,
`unset port-security-policy` under `port1` and delete `dot1x-174-port`; stop
`wpa_supplicant` on endpoint A and bounce its link to get a lease.

**Lab verified by:** *pending*

### Lab 7.3 — Dynamic VLANs, guest and auth-fail VLANs, and MAB

**Objective:** Make FreeRADIUS return a VLAN by name and by ID, see a port-based
port and a MAC-based client move into it, send a client that fails and a client
that never tries to the guest and auth-fail VLAN, and authenticate endpoint B by
MAB alone.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`): MAB, user-based VLAN assignment, and the 802.1X/MAB priority are chain
in both columns. After a C2 lab-VLAN NO-GO, Part A runs and Parts B to D are
read-and-predict (they need `fsw-iot` and `fsw-guest`). Track 2: Part A (the
FreeRADIUS entries, `radtest`, and the authserver tests) and the security-policy
changes run live; the port and endpoint steps are read-and-predict.

**Track 1, Part A — the RADIUS entries:**

1. Add two entries at the **top** of
   `/etc/freeradius/3.0/mods-config/files/authorize`, above `labuser` and every
   `DEFAULT` entry (the file asks for test accounts at the top). Reply items go
   on lines that begin with a tab, each ending with a comma except the last
   (`users(5)`). `vlanuser` gets VLAN 1743 by name; endpoint B's MAB entry gets
   it by ID. The entries read as follows, with each indented reply line
   starting with a tab character (shown here as spaces):

   ```text
   vlanuser Cleartext-Password := "<VLAN_PASSWORD>"
       Tunnel-Type = VLAN,
       Tunnel-Medium-Type = IEEE-802,
       Tunnel-Private-Group-Id = "fsw-iot"

   <MAC_B_HYPHEN> Cleartext-Password := "<MAC_B_HYPHEN>"
       Tunnel-Type = VLAN,
       Tunnel-Medium-Type = IEEE-802,
       Tunnel-Private-Group-Id = "1743"
   ```

   To write them with real tabs, build the new file with `printf` (`\t` is a
   tab), keep a copy of the old one, and put the new one in place; `cp` onto
   the existing file keeps its owner and mode:

   ```bash
   # on radius-174
   F=/etc/freeradius/3.0/mods-config/files/authorize
   sudo cp "$F" "$F.pre-7-3"
   {
     printf 'vlanuser Cleartext-Password := "%s"\n' '<VLAN_PASSWORD>'
     printf '\tTunnel-Type = VLAN,\n\tTunnel-Medium-Type = IEEE-802,\n'
     printf '\tTunnel-Private-Group-Id = "fsw-iot"\n\n'
     printf '%s Cleartext-Password := "%s"\n' '<MAC_B_HYPHEN>' '<MAC_B_HYPHEN>'
     printf '\tTunnel-Type = VLAN,\n\tTunnel-Medium-Type = IEEE-802,\n'
     printf '\tTunnel-Private-Group-Id = "1743"\n\n'
     sudo cat "$F.pre-7-3"
   } > /tmp/authorize.new
   sudo cp /tmp/authorize.new "$F" && rm /tmp/authorize.new
   sudo head -12 "$F" | cat -A
   ```

   `cat -A` shows each tab as `^I`.

   The three attributes and the values `VLAN` and `IEEE-802` are defined in the
   FreeRADIUS dictionaries `dictionary.rfc3580` and `dictionary.rfc2868`. The
   attributes are tagged in the dictionary; FortiSwitchOS 7.4.3 and later ignores
   the tag (Administration Guide, p. 193).

2. Let PEAP replies carry the attributes. Open
   `/etc/freeradius/3.0/sites-available/inner-tunnel`, find the `post-auth`
   block whose comment says to copy the inner reply attributes to the outer
   session, and change its `if (0) {` to `if (1) {`, as the comment instructs.
   Then check the configuration and run the server in debug mode:

   ```bash
   # on radius-174
   sudo grep -n "if (0)" /etc/freeradius/3.0/sites-available/inner-tunnel
   sudo freeradius -CX | tail -3
   sudo systemctl stop freeradius
   sudo freeradius -X
   ```

   `freeradius -C` checks the configuration and exits; its last lines should
   report that the configuration appears to be OK.

3. Test both entries on the server itself, in a third window. The stock
   `localhost` client's secret is `testing123` (Lab 2.5):

   ```bash
   # on radius-174
   radtest vlanuser '<VLAN_PASSWORD>' 127.0.0.1 10 testing123
   radtest <MAC_B_HYPHEN> <MAC_B_HYPHEN> 127.0.0.1 10 testing123
   ```

   Both return `Access-Accept`, and each reply lists the three tunnel attributes
   with its VLAN value. `radtest` sends PAP, so this proves the entries, not the
   PEAP copy of step 2; Part B proves that.

4. Test from the controller, the same way the switch will ask for a MAB device:

   ```text
   FGT # diagnose test authserver radius radius-174 pap vlanuser <VLAN_PASSWORD>
   FGT # diagnose test authserver radius radius-174 pap <MAC_B_HYPHEN> <MAC_B_HYPHEN>
   ```

   Both succeed. The controller's output shows success; the tunnel attributes
   appear in the `Sent Access-Accept` lines of `freeradius -X`.

**Track 1, Part B — a dynamic VLAN by name on a port-based port:**

5. Change endpoint A's supplicant identity to `vlanuser` (edit `identity` and
   `password` in `wired-174.conf`), restart it, and clear the old session:

   ```bash
   # endpoint A
   sudo pkill wpa_supplicant
   sudo wpa_supplicant -B -D wired -i <IFACE> -c /etc/wpa_supplicant/wired-174.conf
   ```

   ```text
   FGT # execute switch-controller switch-action 802-1X clear-auth-port <SWITCH_SN> port1
   ```

6. Read the result:

   ```text
   FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
   FSW # diagnose switch 802-1x status port1
   FSW # diagnose switch physical-ports summary port1
   ```

   Predict the `Dynamic-Vlan` and the port's native VLAN. **Answer:** 1743 in the
   `Dynamic-Vlan` column, and in port-based mode the switch changes the port's
   native VLAN to the RADIUS VLAN (Administration Guide, p. 192), so the summary
   shows 1743 while the session lasts. The string `fsw-iot` matched the switch
   VLAN whose description the controller set from the interface name
   (FortiLink Guide 7.6.7, p. 221). In `freeradius -X`, the final
   `Access-Accept` lists the three tunnel attributes; if it does not, step 2's
   change is not in effect.

7. Prove where endpoint A is. `fsw-iot` has no DHCP server, so add a static
   address in that subnet, ping its gateway, and remove the address:

   ```bash
   # endpoint A
   sudo ip addr add 10.174.43.21/24 dev <IFACE>
   ping -c 3 10.174.43.1
   sudo ip addr del 10.174.43.21/24 dev <IFACE>
   ```

**Track 1, Part C — the guest and auth-fail VLANs:**

8. Add both VLANs to `dot1x-174-port`, with the default 30-second guest delay:

   ```text
   FGT # config switch-controller security-policy 802-1X
   edit "dot1x-174-port"
   set guest-vlan enable
   set guest-vlan-id "fsw-guest"
   set guest-auth-delay 30
   set auth-fail-vlan enable
   set auth-fail-vlan-id "fsw-guest"
   next
   end
   ```

9. Fail on purpose: put a wrong password in `wired-174.conf`, restart the
   supplicant, clear the session, and read the port after a minute:

   ```bash
   # endpoint A
   sudo pkill wpa_supplicant
   sudo wpa_supplicant -B -D wired -i <IFACE> -c /etc/wpa_supplicant/wired-174.conf
   ```

   ```text
   FGT # execute switch-controller switch-action 802-1X clear-auth-port <SWITCH_SN> port1
   FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
   ```

   Predict the VLAN. **Answer:** 1744: the client tried and failed, so it goes to
   the auth-fail VLAN; the `Auth-Fail Vlan` and `Guest VLAN` lines now show
   1744. Prove it with a static `10.174.44.21/24` and `ping 10.174.44.1`, as in
   step 7. Record the session state string and the number of retries you see in
   `freeradius -X` before the move.

10. Never try: stop the supplicant, clear the session, and wait at least 30
    seconds:

    ```bash
    # endpoint A
    sudo pkill wpa_supplicant
    ```

    ```text
    FGT # execute switch-controller switch-action 802-1X clear-auth-port <SWITCH_SN> port1
    FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port1
    ```

    Predict the result. **Answer:** after `guest-auth-delay` the client, which
    sends no EAPOL, goes to the guest VLAN, 1744 here (FortiLink Guide 7.6.7,
    p. 228). `freeradius -X` shows no request at all, which is how you tell the
    guest path from the auth-fail path when both VLANs are the same. Restore the
    correct `vlanuser` password in `wired-174.conf` but leave the supplicant
    stopped.

**Track 1, Part D — MAB-only on endpoint B:**

11. Create a MAC-based, MAB-only policy for `port2`, with the same restricted
    VLAN for devices that fail:

    ```text
    FGT # config switch-controller security-policy 802-1X
    edit "mab-174"
    set security-mode 802.1X-mac-based
    set user-group "dot1x-174"
    set mac-auth-bypass enable
    set auth-order mab
    set guest-vlan enable
    set guest-vlan-id "fsw-guest"
    set auth-fail-vlan enable
    set auth-fail-vlan-id "fsw-guest"
    next
    end
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port2"
    set port-security-policy "mab-174"
    next
    end
    next
    end
    ```

    `auth-order mab` makes the switch skip EAP entirely (FortiLink Guide 7.6.7,
    p. 240); the FortiOS 7.6.0 CLI Reference lists `mab` among the
    `auth-order` values.

12. Make endpoint B send a frame (MAB starts from the device's first frame), then
    read the session:

    ```bash
    # endpoint B
    ping -c 3 10.174.43.1
    ```

    ```text
    FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port2
    FSW # diagnose switch 802-1x status port2
    FSW # diagnose switch vlan assignment mac list
    ```

    Predict the client row and the native VLAN. **Answer:** one client,
    `<MAC_B>`, with a MAB type, `Traffic-Vlan` 1743 and `Dynamic-Vlan` 1743 (the
    integer `"1743"` from RADIUS); in MAC-based mode the assignment is for that
    MAC address only and the port's native VLAN stays `fsw-iot` (Administration
    Guide, p. 193), and `diagnose switch vlan assignment mac list` lists the
    MAC-to-VLAN entry. In `freeradius -X`, the request's `User-Name` is
    `<MAC_B_HYPHEN>`. Record the exact `Type` string and the `Mode` line
    (`mac-by-pass enable`). Endpoint B's first pings may be lost while it
    authenticates; repeat them.

**Track 2:** Run steps 1 to 4 on `radius-174` and your controller (all live),
then the security-policy blocks of steps 8 and 11. If Lab 2.2's third outcome
applies, also apply `mab-174` to the stand-in's `port2` (step 11's second block)
and check it with `show switch-controller managed-switch S248EPTF18000000`.
Skip Parts B to D's endpoint and diagnostic steps.

**Track 2: read-and-predict.**

1. The FortiLink Guide (pp. 232–233) prints this controller output for a
   MAC-based port with MAB enabled, trimmed:

   ```text
   port1 : Mode: mac-based (mac-by-pass enable)
   Port State: authorized:open_auth (  )
   Dynamic Allowed Vlan list: 33
   Dynamic Untagged Vlan list: 33
   Auth Order : MAB-dot1x
   Auth Priority : Legacy
   Native Vlan : 1
   Allowed Vlan list: 1,33,4093
   Untagged Vlan list: 33,4093
   Switch sessions 1/100, Local port sessions:1/20, Client limit:20:
   Client MAC Type Traffic-Vlan Dynamic-Vlan
   f0:18:98:e9:54:80 802.1x 1 33
   ```

   Predict three things: whether the client used MAB, how VLAN 33 reached the
   port, and whether the port's native VLAN changed. **Answer:** the client used
   EAP, not MAB (`Type` is `802.1x`); VLAN 33 came from RADIUS (`Dynamic-Vlan`
   33, added to the dynamic allowed and untagged lists); and the native VLAN is
   still 1, as MAC-based mode leaves it. `open_auth` shows the policy is in
   monitor mode.
2. RADIUS returns `Tunnel-Private-Group-Id = "Users"`, and no FortiGate VLAN
   interface is named `Users`. Predict the result. **Answer:** the string matches
   no switch VLAN description, so no dynamic VLAN is assigned; with `vlan-identity
   description`, an interface whose **description** is `Users` would match
   instead (FortiLink Guide 7.6.7, p. 221). Record what your switch does with the
   session in that case if you test it.
3. Predict what happens to `mab-174`'s clients if `radius-174` stops answering.
   **Answer:** with no server-timeout VLAN configured, the MAB attempt fails, and
   the device ends in the guest or auth-fail VLAN; with `authserver-timeout-vlan
   enable` it would go to the timeout VLAN after `authserver-timeout-period`
   (3 seconds by default) instead (pp. 228–229).

**Expected result:** Track 1: `radtest` and the authserver tests accept
`vlanuser` and `<MAC_B_HYPHEN>`; `vlanuser` on `port1` moved the port's native
VLAN to 1743 by name; a wrong password and a missing supplicant each put endpoint
A in 1744 (with and without a RADIUS request respectively); endpoint B
authenticated by MAB only, into 1743 by ID, with `port2`'s native VLAN unchanged.
Track 2: the RADIUS tests pass, both policies exist (and `mab-174` is on the
stand-in's port, if accepted), and the predictions are answered.

**Negative test:** Remove endpoint B's MAB entry (comment out its four lines
with `#` in `authorize`), restart `freeradius -X`, clear the session, and make
endpoint B send traffic:

```text
FGT # execute switch-controller switch-action 802-1X clear-auth-mac <SWITCH_SN> <MAC_B>
FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port2
```

Predict and observe: `freeradius -X` rejects `<MAC_B_HYPHEN>`, and endpoint B
lands in 1744; its pings to `10.174.43.1` fail (it is no longer in VLAN 1743).
The Administration Guide says MAB retries three times before the device goes to
the guest VLAN (p. 200); record the retries and the VLAN line that shows 1744.
Restore the entry, restart FreeRADIUS, and clear the session again so endpoint B
returns to 1743. Track 2: prediction 2 is the negative test.

**Rollback:** Remove the security policies from both ports and return endpoint A
to plain DHCP; keep the policy objects and the FreeRADIUS entries:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
unset port-security-policy
next
edit "port2"
unset port-security-policy
next
end
next
end
```

```bash
# endpoint A (the supplicant is already stopped)
sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
sleep 10; ip -br addr show <IFACE>
```

Run `sudo systemctl start freeradius` on `radius-174` after stopping the debug
session. Leave the inner-tunnel change in place.

**Lab verified by:** *pending*

### Lab 7.4 — MAC learning limits and sticky MAC

**Objective:** Limit `port2` to one learned MAC address and see a second MAC
address refused, read the violation log, try the per-VLAN limit where the model
supports it, and make endpoint B's MAC address persistent with sticky MAC.

**Platform notes:** The per-port learning limit and sticky MAC are hands-on on
C1, C2, and C3 with S1, S2, or S3 (on S3, `FSW-A`). The **per-VLAN** limit is
hands-on only on S3 with FS-224E switches; on S1, S2, and FS-248E-POE or -FPOE
switches it is not supported (feature matrix note 3) and is read-and-predict.
The violation log is marked standalone-only in the matrix for all three options,
so its step records what your switch does. Track 2: the per-VLAN option and the
global log setting are controller configuration and run live; the per-port steps
run on the stand-in only with Lab 2.2's third outcome; the rest is
read-and-predict.

**Track 1:**

1. Confirm that `port2` has no security policy (Lab 7.3's rollback); sticky MAC
   and 802.1X are not used on one port. Then read the MAC table for VLAN 1743
   from both sides. The controller command is from the FortiOS 8.0.1 CLI
   Reference (cross-check):

   ```text
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # diagnose switch-controller switch-info mac-table <SWITCH_SN> 1743
   FSW # diagnose switch mac-address list
   ```

   Find endpoint B's `<MAC_B>` on `port2`, VLAN 1743.

2. Turn on the violation log and limit `port2` to one MAC address:

   ```text
   FGT # config switch-controller global
   set log-mac-limit-violations enable
   end
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set learning-limit 1
   next
   end
   next
   end
   ```

3. Give endpoint B a second MAC address with a `macvlan` link (`ip-link(8)`)
   and send traffic from it:

   ```bash
   # endpoint B
   sudo ip link add link <IFACE_B> name mv174 address 02:17:40:00:00:02 type macvlan mode bridge
   sudo ip addr add 10.174.43.22/24 dev mv174
   sudo ip link set mv174 up
   ping -c 3 10.174.43.1
   ping -c 3 -I mv174 10.174.43.1
   ```

4. Read the table and the log:

   ```text
   FSW # diagnose switch mac-address list
   FSW # get switch mac-limit-violations interface port2
   FGT # diagnose switch-controller switch-info mac-limit-violations interface <SWITCH_SN> port2
   ```

   Predict the MAC table and the log. **Answer:** only `<MAC_B>` is learned on
   `port2`; `02:17:40:00:00:02` is not, because the port's limit of one is
   reached (FortiLink Guide 7.6.7, p. 141). Record whether the `mv174` ping
   succeeded: the documentation says the address is not learned but does not say
   whether its frames are dropped. If the log works on your switch, it shows
   `port2*` (the asterisk marks a port-based limit), VLAN 1743, the refused MAC
   address, and a timestamp (the shape of the CLI Reference example, p. 501);
   the matrix marks the log standalone-only, so an empty log here is a valid
   result to record.

5. Reset the log, then remove the limit and the second MAC address:

   ```text
   FGT # execute switch-controller mac-limit-violation reset interface <SWITCH_SN> port2
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   unset learning-limit
   next
   end
   next
   end
   ```

   The reset line is the FortiLink Guide's form (p. 143); if your build rejects
   it, try `execute switch-controller switch-action mac-limit-violation reset
   interface <SWITCH_SN> port2`, the FortiOS 8.0.1 form, and record which
   worked.

   ```bash
   # endpoint B
   sudo ip link delete mv174
   ```

6. The per-VLAN limit. On S3 with FS-224E switches, limit `fsw-iot` to one MAC
   address and repeat steps 3 and 4 (with `mv174` re-created); on every other
   switch, read the prediction below instead of running it:

   ```text
   FGT # config system interface
   edit "fsw-iot"
   set switch-controller-learning-limit 1
   next
   end
   ```

   Predict the log entry on an FS-224E. **Answer:** VLAN `1743*` (the asterisk
   marks a VLAN-based limit, CLI Reference, p. 500) with the refused address.
   Then remove it:

   ```text
   FGT # config system interface
   edit "fsw-iot"
   unset switch-controller-learning-limit
   next
   end
   ```

7. Turn on sticky MAC on `port2`, let endpoint B send traffic, and bounce the
   link by unplugging endpoint B's cable for ten seconds:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set sticky-mac enable
   next
   end
   next
   end
   ```

   ```text
   FSW # diagnose switch mac-address list
   ```

   Read the table with the cable out. Predict whether `<MAC_B>` is still listed.
   **Answer:** yes; sticky MAC keeps dynamically learned addresses when the port
   goes down (FortiLink Guide 7.6.7, p. 144). Record the flags the entry shows
   (the documented example prints `static`, `hit`, and similar flags but no
   sticky example).

8. Save the sticky entry to the switch configuration, and find where it appears:

   ```text
   FGT # execute switch-controller switch-action sticky-mac save interface <SWITCH_SN> port2
   FSW # show switch static-mac
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Predict where the saved entry is. **Answer:** in the switch's configuration,
   where `config switch static-mac` has a `type` of `sticky` or `static`
   (FortiSwitchOS 7.6.7 CLI Reference). The FortiOS 7.6.0 managed-switch entry
   also has a `config static-mac` table with `type [static|sticky]`; the
   documentation does not say whether a save on the switch appears there, so
   record whether it does.

**Track 2:** Run step 2's global setting and step 6's per-VLAN option on your
controller (each with its removal), and check them with `show switch-controller
global` and `show system interface fsw-iot`. FortiOS accepts the per-VLAN option
whatever the switch model; acceptance on the controller does not mean the switch
enforces it. If Lab 2.2's third outcome applies, run step 2's port block and
step 7's controller block against `S248EPTF18000000`.

**Track 2: read-and-predict.**

1. The CLI Reference (p. 501) prints:

   ```text
   S524DF4K16000028 # get switch mac-limit-violations all
   Port VLAN ID MAC Address Timestamp
   ----------------------------------------------------------------------------------
   port3* 5 00:00:01:00:00:01 2017-12-05 15:55:20
   port15 9* 0a:c1:08:bf:cc:80 2017-12-05 15:55:44
   ```

   Predict which limit each row records. **Answer:** `port3*` is a port limit on
   `port3`; `9*` is a VLAN limit on VLAN 9 (the asterisk marks which limit was
   exceeded, p. 500). Only the first violation per port or VLAN is logged until
   the log is reset (FortiLink Guide 7.6.7, p. 143).
2. The Track 2 stand-in is an FS-248E-POE. Predict whether a per-VLAN or
   per-trunk learning limit would work on it. **Answer:** neither; note 3 lists
   the FS-248E-POE among the models without the per-VLAN limit and without the
   per-trunk limit. The per-port limit is supported.
3. A port has `sticky-mac enable` and an 802.1X security policy. Predict the
   guidance. **Answer:** do not combine them; static and sticky MAC addresses
   are local authorization and 802.1X is protocol-based authorization, and they
   are not used on the same port at the same time (FortiLink Guide 7.6.7, p. 246;
   Administration Guide, p. 362).
4. A device with a sticky entry on `port2` is moved to `port3`. Predict what
   happens. **Answer:** `port3` does not learn its MAC address until the sticky
   entry is removed from `port2` (Administration Guide, p. 362).

**Expected result:** Track 1: with `learning-limit 1`, only endpoint B's own MAC
address was learned on `port2` and the result for the second address (and the
violation log) is recorded; the per-VLAN limit worked on an FS-224E pair or was
predicted elsewhere; with sticky MAC, `<MAC_B>` stayed in the table with the
cable out, and the saved entry's location is recorded. Track 2: the global and
per-VLAN options were set and removed, and the predictions are answered.

**Negative test:** Delete the unsaved sticky entries and show that the address
then ages normally:

```text
FGT # execute switch-controller switch-action sticky-mac delete-unsaved interface <SWITCH_SN> port2
FSW # diagnose switch mac-address list
```

Unplug endpoint B's cable again and read the table: predict that `<MAC_B>`
disappears from `port2` this time if no saved entry exists, and stays if step 8's
save created one. The difference is the point of step 8. Track 2: prediction 4 is
the negative test.

**Rollback:** Return `port2` and the switch to the chapter's end state:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set sticky-mac disable
unset learning-limit
next
end
next
end
FGT # config switch-controller global
set log-mac-limit-violations disable
end
```

Remove the entry that step 8 saved from wherever it appeared: from the
controller's `config static-mac` table under the managed-switch entry if it is
there; otherwise from `config switch static-mac` on the switch, followed by a
configuration synchronization check (Chapter 03). Confirm that
`diagnose switch mac-address list` shows `<MAC_B>` as an ordinary dynamic entry
on `port2`, and that endpoint B still reaches `10.174.43.1`. Restore
`fgt-pre-7-1-174.conf` only if something else differs.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 7.1 to 7.4 have been run end to end, including
each negative test. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

On a managed FortiSwitch, the switch is the 802.1X authenticator and sends its
own RADIUS requests, which the FortiGate must allow through a firewall policy;
the FortiGate holds the security policy, the user group, and the global 802.1X
settings and pushes them to the switch. Port-based mode authorizes the port and
moves its native VLAN for a dynamic VLAN; MAC-based mode authorizes each MAC
address and assigns VLANs per client. MAB sends the MAC address as user name and
password, and `auth-order mab` skips EAP. RADIUS returns a VLAN as an ID or as a
name that matches the switch VLAN description synchronized from the FortiGate
interface name. Guest and auth-fail VLANs give restricted access to clients that
never try or that fail, and they must share the STP instance of the port's other
VLANs. MAC learning limits cap learned addresses per port (and per VLAN on models
outside note 3), and sticky MAC keeps learned addresses across link changes but
does not mix with 802.1X. The chapter ends with the policy objects and RADIUS
entries in place and both endpoint ports back to plain access ports.

- [ ] `diagnose test authserver` succeeds, `dot1x-174` exists, and I know which
      FreeRADIUS client the switch's requests match on my controller option.
- [ ] I built `dot1x-174-port`, authenticated endpoint A with PEAP, and read the
      session from the controller and the switch.
- [ ] I saw the port block an unauthenticated endpoint and pass it in monitor
      mode.
- [ ] `vlanuser` moved `port1` into VLAN 1743 by name, and endpoint B was placed
      in 1743 by ID through MAB-only.
- [ ] A wrong password and a missing supplicant each put endpoint A in the
      guest/auth-fail VLAN, and I can tell the two paths apart.
- [ ] A learning limit of one refused a second MAC address on `port2`, and I
      recorded what the violation log showed.
- [ ] I know whether my switch supports the per-VLAN limit (note 3).
- [ ] Sticky MAC kept endpoint B's address with the cable out, and I recorded
      where the saved entry appeared.
- [ ] `port1` and `port2` have no security policy, learning limit, or sticky MAC,
      and `log-mac-limit-violations` is disabled.
