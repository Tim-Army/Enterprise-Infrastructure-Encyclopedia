# Chapter 03: FortiLink Provisioning and the Managed-Switch Lifecycle

## Learning Objectives

- Authorize a discovered FortiSwitch on the controller, follow its row in
  `execute switch-controller get-conn-status` from `Discovered/Down` to
  `Authorized/Up`, and read every column and flag of that table.
- Create a pre-authorized (pre-provisioned) managed-switch entry for a switch
  that has not connected, and explain how FortiOS matches it to a real switch.
- Identify the initial-config templates, the VLAN interfaces that FortiOS
  creates from them, the switch-controller reserved network, and the FortiLink
  management VLAN, and say when the templates can still be changed.
- Upload a FortiSwitchOS image to the controller, push it to a managed switch,
  and read the staging and upgrade status.
- Apply settings to a managed switch with a switch profile and with custom
  commands, and check and force configuration synchronization.
- Retire a managed switch with `set-standalone`, prove that it no longer
  rejoins on its own, and adopt it again.

## Theory and Architecture

### The managed-switch lifecycle

Chapter 02 left the lab at the first step of the lifecycle: the switch is
cabled, at factory defaults with your admin password, discovered by the
controller, and **not authorized**, and its managed-switch entry has been
deleted so that it was discovered afresh. Automatic authorization is off on the
FortiLink interface. This chapter walks the rest of the lifecycle:

```text
 factory default --(LLDP or FortiLink discovery)--> Discovered/Down        Lab 3.1
        ^                                                |  fsw-wan1-admin enable
        |                                                v
        |                                   reboot in FortiLink mode
        |                                                |
        |                                                v
        |        templates applied: auto-created VLANs   Authorized/Up     Lab 3.2
        |                                                |
        |                firmware staged and installed   |  (flag U, S, D) Lab 3.3
        |             switch profile, custom commands,   |  (flag C, E)    Lab 3.4
        |                                configuration sync
        |                                                |
        +---- execute factoryreset <---- set-standalone <+                 Lab 3.5
              (zero-touch defaults)      (standalone; not rediscovered)
```

### The managed-switch entry

Every switch the controller knows about has an entry under
`config switch-controller managed-switch`. Discovery creates the entry; you can
also create one yourself before the switch arrives. Three attributes control
the lifecycle:

| Attribute | Values (FortiOS 7.6.0 CLI Reference, p. 1076) | Meaning |
| --- | --- | --- |
| `fsw-wan1-admin` | `discovered` (default), `disable`, `enable` | "Link waiting to be authorized", "Link unauthorized", "Link authorized". Setting `enable` is the authorization |
| `fsw-wan1-peer` | An interface name | The controller's FortiLink interface the switch reaches it through |
| `sn` | A serial number | The switch serial. From FortiOS 7.4.0 the entry name can differ from the serial, and a pre-configured entry must store the serial in `sn` (FortiLink Guide 7.6.7, p. 318) |

From FortiOS 7.4.0 the entry is named after the serial number unless you give
it a name (`rename <serial> to <name>`, p. 318), and commands such as
`get-conn-status`, `get-upgrade-status`, `get-sync-status all`, and
`trigger config-sync` use that name (p. 319). This volume never renames the
switch, so `<SWITCH_SN>` is both the serial and the entry name.

Authorization makes the switch reboot in FortiLink mode (p. 41; p. 14 of the
same guide says no restart is needed, so record which you see). After that it leases an address from the FortiLink interface's DHCP server
(`10.255.1.2` in this lab), opens a management session to the controller
(CAPWAP by default, or HTTPS, pp. 50–52), and takes its whole configuration from
the controller. From then on, changes are made on the controller and pushed to
the switch.

### Reading `get-conn-status`

`execute switch-controller get-conn-status` is the first tool for every
FortiLink question. Its documented shape (FortiLink Guide 7.6.7, p. 52) is:

| Column | Content |
| --- | --- |
| SWITCH-ID | The managed-switch entry name (the serial unless renamed) |
| VERSION | The FortiSwitchOS version and build, or `N/A` when there is no management session |
| STATUS | `Authorized` or `Discovered` (and, after deauthorization or for an entry with no switch, other states), then `/Up` or `/Down` for the management session |
| FLAG | `C` config sync, `U` upgrading, `S` staged, `D` delayed reboot pending, `E` config sync error, `2` Layer 2, `3` Layer 3, `V` VXLAN, `T` tunnel (FortiLink over HTTPS), `X` external |
| ADDRESS | The switch's FortiLink address, `N/A` before authorization, `0.0.0.0` while down |
| JOIN-TIME | When the current session came up |

The last line summarizes the table, for example
`Managed-Switches: 4 (UP: 2 DOWN: 2 MAX: 72)`; MAX is the model's limit (8 on a
FortiGate 40F or FortiGate-VM01, 24 on a 60F, p. 12). The switch has its own
view of the same session: `execute switch-controller get-conn-status` on the
FortiSwitchOS CLI prints `Connection`, `Image Version`, `Remote Address`,
`Join Time`, and `DTLS Version` (FortiSwitchOS 7.6.7 CLI Reference, p. 451).

### Initial-config templates and the auto-created VLANs

When a switch is discovered, the switch controller creates VLAN interfaces on
the FortiLink interface for six traffic types, from templates (FortiLink Guide
7.6.7, pp. 34–37):

| Traffic type (`initial-config vlans`) | Guide example template and VLAN | Default address (p. 35) |
| --- | --- | --- |
| `default-vlan` | `default`, VLAN 1 | Not applicable |
| `quarantine` | `quarantine`, VLAN 4093 | `10.255.11.1/24` |
| `rspan` | `rspan`, VLAN 4092 | `10.255.12.1/24` |
| `voice` | `voice`, VLAN 4091 | Not applicable |
| `video` | `video`, VLAN 4090 | Not applicable |
| `nac` | `onboarding`, VLAN 4089 | Not applicable |
| `nac-segment` | (no example) | `10.255.13.1/24` |

A template with `auto-ip enable` takes an unused /24 from the
**switch-controller reserved network** (`config system global`,
`switch-controller-reserved-network`, default `10.255.0.0/16`), and one with
`dhcp-server enable` gets a DHCP server. In the root VDOM the interface names
are the template names. The FortiLink management VLAN is separate: it is set per
FortiLink interface with `switch-controller-mgmt-vlan`, default 4094 (p. 34).

Templates can be created **only before the controller has authorized any
switch** (p. 34). Chapter 02 authorized a switch during the go/no-go test, so on
Track 1 the templates are now fixed, and Lab 3.2 inspects what they produced.
FortiOS 7.6.3 added `set optional-vlans disable` under
`config switch-controller initial-config vlans`, which stops the optional VLANs
from being created on new FortiLink configurations (pp. 37–38); it is not in the
FortiOS 7.6.0 CLI Reference, and this volume keeps the default.

### Pre-authorized switches

You can create an entry for a switch before it is connected and assign its
ports to VLANs (FortiLink Guide 7.6.7, p. 319). With a wildcard serial number
(`PREFIX****nnnnnn`, the first six characters of a real serial followed by
asterisks), one entry acts as a template that the first matching switch
consumes (pp. 320–321). FortiOS takes the model from the serial prefix, which is
why Chapter 02 used a documented FS-248E-POE serial for its pre-provisioning
test.

### Firmware from the controller

The controller can hold FortiSwitchOS images and push them to managed switches
(pp. 343–349):

1. `execute switch-controller switch-software upload tftp <file> <server>`
   copies an image to the controller, which renames it per model (for example
   `S248EP-IMG.swtp`). FortiGate models without a hard disk hold one image per
   switch model; models with a disk hold up to four (p. 38).
2. `execute switch-controller switch-software upgrade <switch> <image>`
   upgrades one switch; `stage all <image>` stages an image on every compatible
   switch, and `switch-action restart delay all` restarts them after a
   two-minute delay (p. 344).
3. `execute switch-controller get-upgrade-status` reports three percentages
   (downloaded, erased, written) and the state (`Staging`, `Upgrading`,
   `Idle`), plus the image for the next boot (p. 347).

The image is pushed over HTTPS by default (`https-image-push enable`, p. 344).
Two automatic methods exist as well: `firmware-provision` with
`firmware-provision-version` upgrades a switch to an uploaded image when it is
authorized, and `firmware-provision-latest once` (or
`firmware-provision-on-authorization enable` globally) fetches the latest image
from FortiGuard (pp. 38–41). The FGT-1 evaluation has no FortiGuard
entitlement, so this lab uses TFTP.

### Switch profiles, custom commands, and synchronization

A **switch profile** (`config switch-controller switch-profile`) holds settings
that FortiOS applies to the switches bound to it: the admin password override
(`login-passwd-override`, `login-passwd`), console login (`login`), and
configuration revision backups on logout or before an upgrade (FortiLink Guide
7.6.7, pp. 43–44, 352). Every switch uses the `default` profile unless its entry
names another (`set switch-profile`, p. 44).

A **custom command** (`config switch-controller custom-command`) carries
FortiSwitchOS CLI text, with `%0a` for each line break, for settings the
controller has no option for. It can be executed once on a switch, in which case
the switch may reset the setting when it restarts, or bound to the switch's
entry, which makes it part of the switch's configuration. A command that sets
something the switch controls locally can be overwritten (pp. 362–363).

The controller keeps the switch's configuration synchronized. The `C` flag in
`get-conn-status` marks a synchronization in progress and `E` a synchronization
error; `execute switch-controller get-sync-status all` reports the state, and
`diagnose switch-controller trigger config-sync <switch>` forces a full
synchronization (pp. 318–319, 343).

### Leaving FortiLink mode

The FortiLink Guide (p. 322) gives two ways to return a managed switch to
standalone mode:

| Command | Effect |
| --- | --- |
| `execute switch-controller factory-reset <switch-id>` | Factory defaults and reboot; a switch with FortiLink auto-discovery can be detected and authorized again |
| `execute switch-controller switch-action set-standalone <switch-id>` | Factory defaults and reboot, and the controller does not detect and authorize it automatically |

The FortiOS 8.0.1 CLI Reference lists the first as
`execute switch-controller switch-action factory-reset <switch>`, and the
guide's own example of the second omits `switch-action`; type `?` on your build
before you rely on either spelling. The controller also keeps a list of switches
with discovery disabled (`config switch-controller global`,
`disable-discovery`), which you change with `append` and `unselect` (p. 322).

Deauthorizing (`set fsw-wan1-admin disable`) ends management but does not by
itself change the switch's configuration. The FortiLink Guide (p. 43) documents
`set switch-on-deauth {factory-reset | no-op}` under
`config switch-controller global`, to reset a switch or keep its password when
it is deauthorized; that option is **not** in the FortiOS 7.6.0 CLI Reference,
so check with `?` before you use it. Replacing a failed switch with one of the
same model is a separate procedure (`execute replace-device fortiswitch`,
pp. 355–356) and is not part of this lab.

## Design Considerations

### Manual or automatic authorization

| | Manual (this lab) | Automatic (`auto-auth-extension-device enable`) |
| --- | --- | --- |
| Who decides | An administrator, per serial | Any switch that reaches the FortiLink interface |
| Risk | A forgotten switch stays `Discovered` | A rogue or wrong switch is adopted and configured |
| Lab value | Every state is visible and repeatable | Hides the `Discovered` state |
| Fits | Labs, sites with physical-security doubts | Large rollouts with pre-authorized wildcard entries |

Keep manual authorization. The negative test of Lab 3.1 shows the most common
manual mistake: an entry with a mistyped serial.

### Templates before the first switch

Decide template changes (VLAN IDs, a different reserved network, no optional
VLANs) before the first switch is ever authorized, because afterwards they
cannot be created (p. 34). This volume keeps the defaults; Chapter 01's
addresses (`10.255.11.1/24` and so on) assume them. If you rebuild the lab on a
new controller and want different values, change them in Lab 2.2, before any
switch is cabled, and adjust Chapter 01's addressing plan to match.

### Firmware choices

| Method | Needs | Use it when |
| --- | --- | --- |
| Console and TFTP on the switch (Lab 2.4) | Console cable, temporary address | The switch is standalone or new |
| `switch-software upload` and `upgrade` (Lab 3.3) | A downloaded image; TFTP or FTP from the controller | The switch is managed and you control the version |
| `firmware-provision` on authorization | An uploaded image | New switches should all start on one build |
| `firmware-provision-latest once` or GUI **Upgrade all** | FortiGuard entitlement (not on C2) | Production controllers with FortiGuard |

Always check the FortiLink Compatibility table (p. 12) for the target
FortiSwitchOS build and your FortiOS version first. On C2, the evaluation's
low-encryption limit may affect the HTTPS image push; Lab 3.3 shows how to fall
back to the CAPWAP push.

### What to keep after this chapter

| Object | Kept | Why |
| --- | --- | --- |
| Managed-switch entry `<SWITCH_SN>`, authorized | Yes | Chapters 04–12 configure this switch |
| Switch profile `fsw-174-prof`, bound to the switch | Yes | Keeps your admin password and pre-upgrade backups under controller control |
| Custom commands `fsw174-timeout-15` and `fsw174-timeout-orig` | No | Lab 3.4 removes them |
| Uploaded switch image on the controller | Optional | Not needed by later labs; Lab 12.4 only predicts the firmware fault |
| Track 2 pre-provisioned entry `S248EPTF18000000` | Yes, if FortiOS accepted it | Track 2's per-port steps in Chapters 04–08 use it |

## Implementation and Automation

The labs are the implementation. Two habits help.

**Check the state before and after every lifecycle step.** One command answers
most questions; run it before and after each change and keep the output in
your lab notes:

```text
FGT # execute switch-controller get-conn-status
```

**Save the switch's own view at each step.** On the switch console, the same
two commands show what the switch thinks:

```text
FSW # get system status
FSW # execute switch-controller get-conn-status
```

The FortiOS commands in this chapter were checked against the FortiOS 7.6.0 CLI
Reference (configuration commands) and the FortiLink Guide 7.6.7 (`execute` and
`diagnose` commands), with the FortiOS 8.0.1 CLI Reference as a cross-check
where the guide prints no syntax line. Switch commands were checked against the
FortiSwitchOS 7.6.7 CLI Reference.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| The switch stays `Discovered/Down` after `fsw-wan1-admin enable` | The entry you edited is not the switch's (mistyped serial); the switch has not finished rebooting | `get-conn-status` lists two rows; compare the serial with `get system status` on the switch |
| `Authorized/Down` and ADDRESS `0.0.0.0` | Management session down: reboot in progress, link down, firmware incompatible, or (C2) the evaluation license | Wait for the reboot; Lab 2.4 go/no-go checks; switch-side `execute switch-controller get-conn-status` |
| FLAG `E` | Configuration synchronization error | `execute switch-controller get-sync-status all`; `diagnose switch-controller trigger config-sync <SWITCH_SN>` |
| `get-upgrade-status` stuck at `Upgrading` | The switch lost contact during the upgrade | `execute switch-controller switch-software cancel` (the guide's form is `cancel sn <serial>`, p. 352; the 8.0.1 reference lists `cancel switch-id <switch>`) |
| The image push stalls on C2 | HTTPS image push under the evaluation's low-encryption limit (unconfirmed) | Cancel, `set https-image-push disable`, and retry |
| A custom command's setting is gone after a restart | It was executed once, not bound | Bind it under the switch's `config custom-command` |
| No quarantine or RSPAN interface on the controller | No switch has been discovered yet (Track 2), or optional VLANs disabled | `show switch-controller initial-config vlans` |
| A retired switch never reappears after cabling | Intended: `set-standalone`, or its serial is in `disable-discovery` | `show switch-controller global`; `execute factoryreset` on the switch |
| The switch console rejects the admin password after authorization | FortiOS 7.6.1 and later generate a password for a switch that has none (p. 43) | Set a password before authorizing, or use a switch profile with `login-passwd-override` |

## Security and Best Practices

- **Authorize by serial, by hand.** Leave `auto-auth-extension-device`
  disabled, and compare every serial with the switch label or its
  `get system status` before you authorize.
- **Own the admin password.** Fortinet recommends setting the managed switches'
  admin password through a switch profile (p. 43). Use the password you recorded
  in Chapter 02, and keep it out of screenshots.
- **Verify every image.** Check the image's checksum against the support portal
  before you upload it, and run `execute verify image primary` on the switch
  after every upgrade.
- **Back up before upgrades.** Take a controller backup before Lab 3.3; the
  switch profile's `revision-backup-on-upgrade` adds a revision on the switch
  as well.
- **Retire switches cleanly.** Use `set-standalone` (or a factory reset) and
  delete the entry, so that a retired switch cannot be re-adopted by accident and
  keeps no lab configuration.
- **Treat custom commands as code.** They bypass the controller's model of the
  switch; keep them short, name them clearly, and remove them when they are no
  longer needed.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — supported switch counts (p. 12), auto-discovery ports and automatic ISLs
  (pp. 30–31), VLAN templates and the reserved network (pp. 34–38), firmware
  provisioning (pp. 38–41), authorizing (p. 41), admin passwords and the switch
  profile (pp. 43–44), FortiLink with HTTPS and `get-conn-status` (pp. 50–52),
  names and pre-configured entries (pp. 317–321), standalone conversion
  (p. 322), configuration sync and firmware upgrade (pp. 343–352), replacing a
  switch (pp. 355–357), custom commands (pp. 362–363).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `execute switch-controller get-conn-status` (p. 451),
  `diagnose switch trunk summary` (p. 381), `get system global` (pp. 522–523),
  `admintimeout` (p. 239).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config switch-controller managed-switch`
  (`fsw-wan1-admin`, p. 1076), `config switch-controller global` (p. 1044),
  `switch-profile`, `custom-command`, `initial-config template` and `vlans`.
- FortiOS 8.0.1 CLI Reference (cross-check only) — `execute switch-controller`
  syntax lines for `custom-command`, `get-physical-conn`, `get-sync-status`,
  `switch-software cancel`, and `switch-action factory-reset`.

**Knowledge checks**

1. A switch shows `S124EN5918003682 N/A Discovered/Down 2 N/A`. What does each
   of the five fields tell you, and what single change makes it manageable?
2. Why can Track 1 no longer create initial-config templates in this chapter,
   while Track 2 still can?
3. In `get-upgrade-status`, a row reads `(0/100/100) ... (Idle)` with a newer
   build in Next-boot. Is the switch running the new build?
4. You executed a custom command once and the setting disappeared after the
   switch restarted. What should you have done?
5. What is the difference between `factory-reset` and `set-standalone` from the
   controller, and which one did Lab 3.5 use, and why?
6. Which `get-conn-status` flag marks a switch managed over FortiLink with
   HTTPS?

## Hands-On Lab

**Shared prerequisites.** Chapter 02 complete: the controller's FortiLink
interface at `10.255.1.1/24` with LLDP neighbor detection and manual
authorization; the switch cabled on `<FSW_FL_PORT>`, discovered, unauthorized,
at factory defaults with your recorded admin password (on S3, only `FSW-A` is
cabled); the go/no-go result recorded; the TFTP VM 140 at `10.30.99.50`; a
console connection to the switch. Track 2: the Lab 2.2 pre-provisioning outcome
recorded. **Cost:** none beyond Chapter 02.

As in Chapter 02, `FGT #` is the controller on any option, and blocks written
for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>`. `<SWITCH_SN>`
is your switch's serial number (on S3, `FSW-A`'s). On Track 2, `<SWITCH_SN>` is
the stand-in serial `S248EPTF18000000` from Lab 2.2, created again in Lab 3.1.
This chapter adds no firewall policies, routes, or physical interfaces, so the
C2 budget is unchanged.

### Lab 3.1 — Discover and authorize the switch

**Objective:** Authorize the discovered switch, follow its state on the
controller and on the switch, find the trunk that FortiLink formed, and see
what a mistyped authorization does.

**Platform notes:** Hands-on on C1, C2 (after a GO in Lab 2.4), and C3 with S1,
S2, or S3; on S3, authorize `FSW-A` only. Port names differ only in the
controller's FortiLink port (`<FL_PORT>`, `port3`, `port4`) and the switch's
`<FSW_FL_PORT>` (Chapter 02). Track 2: build a pre-provisioned entry if Lab 2.2's
outcome allows it, plus read-and-predict.

**Track 1:**

1. Confirm the starting state. The switch is listed with STATUS
   `Discovered/Down`, FLAG `2`, and VERSION and ADDRESS `N/A`:

   ```text
   FGT # execute switch-controller get-conn-status
   ```

2. Read the entry that discovery created. `get` prints default values, which
   `show` hides:

   ```text
   FGT # get switch-controller managed-switch <SWITCH_SN>
   ```

   Before you read the output, predict `fsw-wan1-admin` and `fsw-wan1-peer`.
   **Answer:** `fsw-wan1-admin` is `discovered` ("link waiting to be
   authorized", the default in the FortiOS 7.6.0 CLI Reference), and
   `fsw-wan1-peer` names your FortiLink port (`port3` on C2), which discovery
   filled in.

3. Compare the serial with the switch's own report, then authorize it and give
   it a description:

   ```text
   FSW # get system status
   ```

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set description "FSW-A lab-174"
   set fsw-wan1-admin enable
   next
   end
   ```

4. The switch reboots in FortiLink mode (FortiLink Guide 7.6.7, p. 41; p. 14
   says no restart is needed, so record whether it does). Repeat
   `get-conn-status` every minute until the row reads `Authorized/Up` with
   the FortiSwitchOS build in VERSION and `10.255.1.2` in ADDRESS, then check
   the lease and reachability:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # execute dhcp lease-list port3
   FGT # execute ping 10.255.1.2
   ```

   On FortiOS 7.6.3 or later you can also read the switch's status from the
   controller (FortiLink Guide 7.6.7, p. 332; FGT-1's 7.6.2 does not have it):

   ```text
   FGT # diagnose switch-controller switch-info status
   ```

5. Look from the switch side. Log in on the console with your admin password:

   ```text
   FSW # execute switch-controller get-conn-status
   ```

   `Connection` reads `Connected` and `DTLS Version` shows the session's
   protocol (FortiSwitchOS 7.6.7 CLI Reference, p. 451).

6. Find the trunk that FortiLink formed on `<FSW_FL_PORT>` (exam task 1.3, the
   ports used for stacking and FortiLink):

   ```text
   FSW # diagnose switch trunk summary
   ```

   Look for a trunk whose status is up; its Mode is expected to include
   `auto-isl`, as in the documented examples of automatically formed trunks.
   Record its name and mode. In both documented examples of automatically formed trunks
   (FortiLink Guide 7.6.7, p. 48; FortiSwitchOS 7.6.7 CLI Reference, p. 381),
   the name is the peer device's serial number without its first three
   characters, followed by `-0`. After authorization every switch port is
   enabled for FortiLink, so a second switch cabled to any port forms an
   inter-switch link the same way (FortiLink Guide 7.6.7, p. 31); Chapter 06
   uses this.

7. See the physical FortiLink graph from the controller (FortiLink Guide
   7.6.7, p. 181):

   ```text
   FGT # execute switch-controller get-physical-conn standard port3
   ```

   In the GUI, **WiFi & Switch Controller > Managed FortiSwitches** shows the
   switch faceplate, and the **Topology** view draws a solid line for a healthy
   FortiLink (p. 322).

**Track 2:** If FortiOS accepted the pre-provisioned entry in Lab 2.2 (the
second or third outcome), create the stand-in entry again. It stays for the rest
of the volume as Track 2's `<SWITCH_SN>`. From FortiOS 7.4.0 a pre-configured
entry stores the serial in `sn` (FortiLink Guide 7.6.7, p. 318); if your build
rejects `set sn` because the entry name is already the serial, leave that line
out:

```text
FGT # config switch-controller managed-switch
edit S248EPTF18000000
set sn "S248EPTF18000000"
set description "Track 2 stand-in"
set fsw-wan1-peer "port3"
set fsw-wan1-admin enable
next
end
FGT # execute switch-controller get-conn-status
```

Record the STATUS that `get-conn-status` shows for an entry whose switch has
never connected; the documentation does not print one. If FortiOS rejected the
entry in Lab 2.2, skip this step: Track 2's managed-switch steps in later
chapters are read-and-predict.

**Track 2: read-and-predict.**

1. The FortiLink Guide (p. 52) prints this table from a controller managing
   switches over FortiLink with HTTPS:

   ```text
   SWITCH-ID VERSION STATUS FLAG ADDRESS JOIN-TIME
   S524DN4K16000116 v7.4.0 (0796) Authorized/Up 2T 10.255.1.2 Mon Dec 18 15:41:34 2023
   S248EPTF18001384 v7.4.1 (787) Authorized/Up 2 10.255.1.5 Mon Dec 18 15:41:43 2023
   S248EPTF18001827 N/A Discovered/Down 2 N/A
   S124EN5918003682 N/A Discovered/Down 2 N/A
   Flags: C=config sync, U=upgrading, S=staged, D=delayed reboot pending, E=config sync error,
   2=L2, 3=L3, V=VXLAN, T=tunnel, X=External
   Managed-Switches: 4 (UP: 2 DOWN: 2 MAX: 72)
   ```

   Predict which switch is managed over the HTTPS tunnel, and how many of the
   four the controller can configure right now. **Answer:**
   `S524DN4K16000116` (FLAG `2T`: Layer 2 and tunnel), and two. Only the
   `Authorized/Up` rows have a management session; the `Discovered/Down` rows
   wait for `fsw-wan1-admin enable`, which is why the summary reads UP 2,
   DOWN 2.
2. The FortiSwitchOS 7.6.7 CLI Reference (p. 451) prints the switch-side view:

   ```text
   S524DF4K15000024 # execute switch-controller get-conn-status
   Get managed-switch S524DF4K15000024 connection status:
   Connection: Connected
   Image Version: FG100D-v6.2-build849
   Remote Address: xxx.xxx.x.x
   Join Time: Wed Mar 13 08:38:57 2019
   DTLS Version: DTLSv1.2
   ```

   Predict whose firmware `Image Version` describes. **Answer:** the
   controller's. The `FG100D` prefix is a FortiGate 100D image, not a
   FortiSwitch one; the switch reports the version of the FortiGate it is
   managed by. `DTLS Version` shows that the CAPWAP management session is
   encrypted with DTLS.

**Expected result:** Track 1: `get-conn-status` shows `<SWITCH_SN>` as
`Authorized/Up`, FLAG `2`, ADDRESS `10.255.1.2`, with your FortiSwitchOS 7.6.x
build; the switch reports `Connection: Connected`; the trunk that FortiLink
formed is up, and its name and mode are recorded; the entry's description is `FSW-A lab-174`. Track 2: the
stand-in entry exists (if accepted) and its status is recorded.

**Negative test:** This builds on Lab 2.4's negative test (discovery alone gives
no management session). Authorize a serial that differs from your switch's by
its last character, as a mistyped authorization would:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN_TYPO>
set fsw-wan1-peer "port3"
set fsw-wan1-admin enable
next
end
FGT # execute switch-controller get-conn-status
```

The typo entry is listed but never reaches `Up`, because no switch with that
serial exists, and your real switch is unaffected. Had you made this mistake in
step 3, the real switch would have stayed `Discovered/Down`. Delete the typo
entry:

```text
FGT # config switch-controller managed-switch
delete <SWITCH_SN_TYPO>
end
```

**Rollback:** To return to the start of this lab, deauthorize the switch, reset
it from its console, and delete its entry, as in Lab 2.4 step 7. Track 2: delete
`S248EPTF18000000`. Normally you keep the authorized switch for Lab 3.2.

**Lab verified by:** *pending*

### Lab 3.2 — Initial-config templates and the auto-created VLANs

**Objective:** Find the templates, the traffic-type mapping, the reserved
network, and the VLAN interfaces and DHCP servers they produced, and match them
to Chapter 01's addressing plan.

**Platform notes:** Hands-on on every option and on Track 2 (the templates are
controller configuration). On Track 1 the VLAN interfaces exist because a switch
has been discovered; on Track 2 they may not, because the guide says they are
created when a switch is discovered (p. 37). C1, C2, and C3 differ only in the
parent interface of the VLANs (`<FL_PORT>`, `port3`, `port4`). Track 2 adds a
read-and-predict.

**Track 1:**

1. Show the templates and which template serves each traffic type:

   ```text
   FGT # show switch-controller initial-config template
   FGT # show switch-controller initial-config vlans
   ```

   Record each template's `vlanid` and whether it has `auto-ip` and
   `dhcp-server`. Compare them with the guide's example in Theory and
   Architecture.

2. Show the reserved network. `get` shows the default value, which `show` hides:

   ```text
   FGT # get system global
   ```

   Find `switch-controller-reserved-network`; expect `10.255.0.0 255.255.0.0`.

3. Show each VLAN interface the templates created. Use the template names from
   step 1 for `<VLAN_IF>` (in the root VDOM the interface name is the template
   name, p. 34):

   ```text
   FGT # show system interface <VLAN_IF>
   ```

   For each, record `vlanid`, `interface` (your FortiLink port), `ip`, and
   `switch-controller-feature`. The quarantine interface should have
   `10.255.11.1/24` and the RSPAN interface `10.255.12.1/24`, matching
   Chapter 01.

4. Show the DHCP servers. Besides the FortiLink server from Lab 2.2, there is
   one per template with `dhcp-server enable`:

   ```text
   FGT # show system dhcp server
   ```

5. Confirm the FortiLink management VLAN. It is 4094 unless
   `switch-controller-mgmt-vlan` appears in the interface configuration
   (p. 34):

   ```text
   FGT # show system interface port3
   ```

6. In the GUI, **WiFi & Switch Controller > FortiSwitch VLANs** lists the same
   interfaces (FortiLink Guide 7.6.7, "Viewing FortiSwitch VLANs", p. 104).

**Track 2:** Run steps 1, 2, 4, and 5. Then run step 3 for the quarantine
template's name and record whether the interface exists. On a controller that
has never discovered a switch, the guide's wording (p. 37) suggests it does not.
Track 2 has never authorized a switch, so it could still create or change
templates; do not, because the rest of the volume assumes the defaults.

**Track 2: read-and-predict.** The FortiLink Guide (pp. 36–37) shows this part
of an automatically created quarantine interface (its reserved network was
`169.254.0.0/16`):

```text
edit "quarantine"
    set vdom "root"
    set ip 169.254.11.1 255.255.255.0
    set description "Quarantine VLAN"
    set security-mode captive-portal
    set device-identification enable
    set switch-controller-access-vlan enable
    set switch-controller-feature quarantine
    set interface "fortilink"
    set vlanid 4093
next
```

1. Predict the address this interface has in this volume's lab. **Answer:**
   `10.255.11.1/24`. The template uses `auto-ip`, so the address comes from the
   reserved network; the guide's example used `169.254.0.0/16`, and this lab
   keeps the default `10.255.0.0/16`, from which the quarantine template's
   default is `10.255.11.1/24` (p. 35).
2. Predict what makes this a FortiLink VLAN rather than an ordinary VLAN
   interface. **Answer:** `set interface "fortilink"` (its parent is the
   FortiLink interface, so the VLAN is carried to the managed switches) and
   `switch-controller-feature quarantine` (the role FortiOS gives it).
   `switch-controller-access-vlan enable` blocks traffic between hosts in the
   VLAN; Lab 8.5 uses that option on a lab VLAN.

**Expected result:** You have a table of the templates (name, VLAN ID,
`auto-ip`, `dhcp-server`), the reserved network `10.255.0.0/16`, and, on Track
1, the auto-created VLAN interfaces on the FortiLink port with the addresses of
Chapter 01 and their DHCP servers. Track 2 has recorded whether the interfaces
exist without a discovered switch.

**Negative test:** Track 1: try to create a new template now that a switch has
been authorized:

```text
FGT # config switch-controller initial-config template
edit "lab-test-174"
set vlanid 1749
next
end
FGT # show switch-controller initial-config template
```

The guide says templates can be created only before any switch is authorized
(p. 34) but does not say how FortiOS enforces it. Record whether FortiOS
refuses the entry, or accepts it without creating any VLAN interface
(`show system interface lab-test-174` finds nothing). Delete it if it was
created:

```text
FGT # config switch-controller initial-config template
delete "lab-test-174"
end
```

Track 2 has no negative test beyond the existence check in its steps.

**Rollback:** Nothing to roll back; this lab changes nothing except the deleted
test template.

**Lab verified by:** *pending*

### Lab 3.3 — Push firmware from the controller

**Objective:** Upload a FortiSwitchOS image to the controller, upgrade the
managed switch with it, and read the staging, upgrade, and connection status as
it happens.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`). Every option uses TFTP from VM 140: FGT-1 (`port1`) and the C1
`<WAN_PORT>` are both on VLAN 99 with the TFTP server. C1 and C3 with FortiGuard
can also use the GUI or `firmware-provision-latest`; C2 cannot. Track 2: upload
and list the image live if you have one, set firmware provisioning on the
stand-in entry, and read-and-predict the upgrade.

**Track 1:**

1. Choose the image. Use a FortiSwitchOS 7.6.x GA image for your exact model
   other than the build installed in Lab 2.4, preferably a newer one that the
   FortiLink Compatibility table supports with your FortiOS version. Copy it to
   `/tftpboot` on VM 140 and check its checksum against the support portal. If
   the build you installed is the only one available, use it; the documentation
   does not say whether the controller reinstalls an identical build, so record
   what happens.
2. Back up the controller and record the switch's current build:

   ```text
   FGT # execute backup config tftp fgt-pre-3-3-174.conf 10.30.99.50
   FGT # execute switch-controller get-conn-status
   ```

3. Upload the image to the controller and list it. The controller renames it
   per model; record the new name as `<IMAGE_NAME>` (p. 346):

   ```text
   FGT # execute switch-controller switch-software upload tftp <FSW_IMAGE> 10.30.99.50
   FGT # execute switch-controller switch-software list-available
   ```

4. Upgrade the switch:

   ```text
   FGT # execute switch-controller switch-software upgrade <SWITCH_SN> <IMAGE_NAME>
   ```

5. Watch the upgrade. Repeat both commands every minute. In
   `get-upgrade-status` the three numbers are the percentage downloaded,
   erased, and written (p. 347); in `get-conn-status`, look for FLAG `U` while
   the switch upgrades, then `Authorized/Down` while it reboots:

   ```text
   FGT # execute switch-controller get-upgrade-status
   FGT # execute switch-controller get-conn-status
   ```

6. When the row is `Authorized/Up` again, VERSION shows the new build. Verify
   it on the switch:

   ```text
   FSW # get system status
   FSW # execute verify image primary
   ```

7. If the push stalls (C2 especially), cancel it, switch the controller to the
   CAPWAP image push, and repeat from step 4. The cancel syntax differs between
   references: the FortiLink Guide 7.6.7 (p. 352) gives
   `execute switch-controller switch-software cancel sn <serial>`, the FortiOS
   8.0.1 CLI Reference `cancel switch-id <switch>`; use `?` to see which your
   build accepts.

   ```text
   FGT # config switch-controller global
   set https-image-push disable
   end
   ```

   Set it back to `enable` after the upgrade.

**Track 2:**

1. If you have a FortiSwitchOS image (for example the one from Lab 2.4), upload
   it and list it. This works without a switch:

   ```text
   FGT # execute switch-controller switch-software upload tftp <FSW_IMAGE> 10.30.99.50
   FGT # execute switch-controller switch-software list-available
   ```

2. If the stand-in entry exists, set it to receive an uploaded image when it is
   authorized (FortiLink Guide 7.6.7, pp. 38–39). The version format is
   `major.minor.build`, for example `7.6.1234`:

   ```text
   FGT # config switch-controller managed-switch
   edit S248EPTF18000000
   set firmware-provision enable
   set firmware-provision-version <MAJOR.MINOR.BUILD>
   next
   end
   FGT # show switch-controller managed-switch S248EPTF18000000
   ```

**Track 2: read-and-predict.** The FortiLink Guide (pp. 347–348) shows a staged
upgrade of four switches:

```text
Device Running-version Status Next-boot
S224ENTF18001408 S224EN-v6.2.1-build176,190620 (GA) (100/0/0) S224EN-v6.2-build176 (Staging)
S108FP5918008265 S108FP-v6.2.1-build176,190620 (GA) (18/0/0) S108FP-v6.2-build176 (Staging)
...
S108FP5918008265 S108FP-v6.2.1-build176,190620 (GA) (0/100/100) S108FP-v6.2-build194 (Idle)
...
SWITCH-ID VERSION STATUS FLAG ADDRESS JOIN-TIME NAME
S108FP5918008265 v6.2.1 () Authorized/Down D 0.0.0.0 N/A -
```

1. In the first `S108FP` row, predict what `18` means. **Answer:** 18 percent
   of the new image has been downloaded; the three fields are downloaded,
   erased, and written.
2. In the `(0/100/100) ... (Idle)` row, predict which build the switch is
   running. **Answer:** still build 176 (Running-version). The new build 194
   is written and waits in Next-boot; it runs only after a restart.
3. After `execute switch-controller switch-action restart delay all`, predict
   the meaning of FLAG `D` and ADDRESS `0.0.0.0`. **Answer:** `D` is "delayed
   reboot pending"; the session is down (`Authorized/Down`), so there is no
   address until the switch returns with the new build.

**Expected result:** Track 1: `list-available` shows the uploaded image,
`get-upgrade-status` progressed through download and write, FLAG `U` appeared
during the upgrade, and the switch is `Authorized/Up` on the chosen build with a
verified image. Track 2: the image is listed (if uploaded), the stand-in entry
shows `firmware-provision enable`, and the predictions are answered.

**Negative test:** Ask for an upgrade with an image name that is not on the
controller:

```text
FGT # execute switch-controller switch-software upgrade <SWITCH_SN> no-such-image.swtp
FGT # execute switch-controller get-conn-status
```

The command is rejected or does nothing, and VERSION does not change. Track 2:
run the same upgrade command against the stand-in entry and record the error:
there is no switch to upgrade.

**Rollback:** To return to the previous build, upload it and upgrade again (a
downgrade can reset settings; read the release notes first), or restore with
Lab 2.4's console procedure. Track 2: on the stand-in entry,
`set firmware-provision disable` and `unset firmware-provision-version`. Leave
`https-image-push` enabled.

**Lab verified by:** *pending*

### Lab 3.4 — Switch profiles, custom commands, and configuration sync

**Objective:** Bind a switch profile that sets the admin password and a backup
policy, change a switch setting with a custom command executed once and then
bound, and check and force configuration synchronization.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`; later chapters bind `FSW-B` too). The commands are the same on every
option. Track 2: build the profile and the custom commands live and bind them
to the stand-in entry (if it exists), plus read-and-predict.

**Track 1:**

1. Create the profile with your recorded switch admin password. Fortinet
   recommends managing the password this way (FortiLink Guide 7.6.7, p. 43):

   ```text
   FGT # config switch-controller switch-profile
   edit "fsw-174-prof"
   set login-passwd-override enable
   set login-passwd <FSW_ADMIN_PASSWORD>
   set login enable
   set revision-backup-on-upgrade enable
   next
   end
   ```

2. Bind it to the switch:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set switch-profile "fsw-174-prof"
   next
   end
   ```

   On the switch, predict the `revision-backup-on-upgrade` line in
   `get system global` (FortiSwitchOS 7.6.7 CLI Reference, pp. 522–523), then
   check. Log in again on the console with the same password; it still works,
   because the profile pushes the password you already use.

   ```text
   FSW # get system global
   ```

   **Answer:** `enable`. The guide documents the profile option (p. 352) but
   not how it appears on the switch; record what you see.

3. Record the switch's current `admintimeout` from the same output (the
   FortiSwitchOS default is 5 minutes, CLI Reference p. 239). Create two custom
   commands, one that sets 15 minutes and one that restores the value you
   recorded (`<ORIG_TIMEOUT>`). `%0a` is a line break (p. 362):

   ```text
   FGT # config switch-controller custom-command
   edit "fsw174-timeout-15"
   set description "Lab 3.4: admin idle timeout 15 minutes"
   set command "config system global %0a set admintimeout 15 %0a end %0a"
   next
   edit "fsw174-timeout-orig"
   set description "Lab 3.4: restore the recorded admin idle timeout"
   set command "config system global %0a set admintimeout <ORIG_TIMEOUT> %0a end %0a"
   next
   end
   ```

   The command text is FortiSwitchOS CLI; on the switch it is equivalent to:

   ```text
   FSW # config system global
   set admintimeout 15
   end
   ```

4. Execute the first command once, then check on the switch:

   ```text
   FGT # execute switch-controller custom-command fsw174-timeout-15 <SWITCH_SN>
   FSW # get system global
   ```

   `admintimeout` reads `15`.

5. Bind the same command to the switch's entry, so that it becomes part of the
   switch's configuration (p. 363):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config custom-command
   edit 1
   set command-name "fsw174-timeout-15"
   next
   end
   next
   end
   ```

6. Check synchronization, force a full synchronization, and check again. Watch
   for FLAG `C` (sync in progress) or `E` (sync error) in `get-conn-status`:

   ```text
   FGT # execute switch-controller get-sync-status all
   FGT # diagnose switch-controller trigger config-sync <SWITCH_SN>
   FGT # execute switch-controller get-conn-status
   FGT # execute switch-controller get-sync-status all
   ```

   The local references print no example of `get-sync-status` output; record
   the fields your build shows for an in-sync switch, because Lab 12.4 compares
   against them.

7. Clean up the custom commands, keeping the profile. Remove the binding,
   restore the original timeout once, check it, and delete both commands:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config custom-command
   delete 1
   end
   next
   end
   FGT # execute switch-controller custom-command fsw174-timeout-orig <SWITCH_SN>
   FSW # get system global
   FGT # config switch-controller custom-command
   delete "fsw174-timeout-15"
   delete "fsw174-timeout-orig"
   end
   ```

**Track 2:** Run steps 1, 3, and 5 against `S248EPTF18000000` instead of
`<SWITCH_SN>` (step 2's binding too, if the stand-in entry exists), and
`show switch-controller managed-switch S248EPTF18000000` to see the bindings.
Skip the switch-side checks and the `execute` steps, which need a connected
switch. Then do step 7's unbinding and deletions, keeping the profile and its
binding.

**Track 2: read-and-predict.**

1. After an upgrade, the FortiLink Guide (p. 40) shows
   `S248EPTF18000000 v6.4.4 (454) Authorized/Up C 169.254.1.6`. Predict what
   the controller is doing with this switch. **Answer:** synchronizing its
   configuration (FLAG `C`). A switch that has just rebooted onto new firmware
   receives its configuration again; `E` instead would mean the
   synchronization failed.
2. A custom command that sets the STP `max-age` was executed once on a switch,
   which then restarted. Predict whether the setting survives. **Answer:** not
   necessarily. An unbound custom command is not part of the switch's
   configuration on the controller, so the switch may reset it when it restarts
   (p. 362); binding it under the switch's `config custom-command` keeps it.

**Expected result:** Track 1: the profile `fsw-174-prof` is bound, the console
password is unchanged, and `get system global` shows the backup setting; the
custom command changed `admintimeout` to 15 when executed once and when bound;
synchronization was forced and the switch returned to an in-sync state without
FLAG `E`; afterwards the custom commands are gone and `admintimeout` is back at
`<ORIG_TIMEOUT>`. Track 2: the profile exists and is bound to the stand-in entry
(if it exists).

**Negative test:** Disable console login in the profile, try to log in on the
switch console, then enable it again (FortiLink Guide 7.6.7, p. 44):

```text
FGT # config switch-controller switch-profile
edit "fsw-174-prof"
set login disable
next
end
```

The console no longer accepts your login, although the switch stays
`Authorized/Up`; management continues over FortiLink. Restore console login and
check that it works:

```text
FGT # config switch-controller switch-profile
edit "fsw-174-prof"
set login enable
next
end
```

Track 2: set and restore `login` on the profile and confirm the change with
`show switch-controller switch-profile fsw-174-prof`.

**Rollback:** Set `switch-profile "default"` on the entry and delete
`fsw-174-prof`. If you remove a password override, the guide warns that the old
password stays on the switch unless a profile with the override enabled and no
password is applied (p. 43). Normally keep `fsw-174-prof` bound.

**Lab verified by:** *pending*

### Lab 3.5 — Retire the switch and adopt it again

**Objective:** Convert the managed switch to standalone mode from the
controller, show that it does not rejoin on its own, then return it to factory
defaults and adopt it again, leaving it managed for Chapter 04.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`). The switch reboots twice; allow about 20 minutes. Port names differ
only as in Lab 3.1. Track 2: practice the discovery list and the
deauthorization state on the stand-in entry, plus read-and-predict.

**Track 1:**

1. Record the state and back up the controller:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # show switch-controller global
   FGT # execute backup config tftp fgt-pre-3-5-174.conf 10.30.99.50
   ```

2. Convert the switch to standalone mode. It returns to factory defaults and
   reboots (FortiLink Guide 7.6.7, p. 322):

   ```text
   FGT # execute switch-controller switch-action set-standalone <SWITCH_SN>
   ```

3. After a few minutes, look at both sides. On the controller, the entry is no
   longer `Up`. Check whether the controller added the serial to the
   discovery-disabled list; the guide says only that `set-standalone` prevents
   automatic detection and authorization, not how:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # show switch-controller global
   ```

   On the switch console, log in (factory defaults: `admin` with no password,
   then set your recorded password when prompted) and ask for the FortiLink
   session. The command is valid only on a switch managed by a FortiGate
   (FortiSwitchOS 7.6.7 CLI Reference, p. 451), so it reports no connection:

   ```text
   FSW # execute switch-controller get-conn-status
   FSW # get system status
   ```

4. Deauthorize and delete the entry on the controller:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set fsw-wan1-admin disable
   next
   end
   FGT # config switch-controller managed-switch
   delete <SWITCH_SN>
   end
   ```

5. Adopt the switch again. If step 3 showed `<SWITCH_SN>` in
   `disable-discovery`, remove it. The removal uses `unselect`, which the
   FortiLink Guide documents (p. 322); type it at the prompt inside
   `config switch-controller global`:

   ```text
   FGT # config switch-controller global
   unselect disable-discovery <SWITCH_SN>
   end
   ```

   Then reset the switch from its console, so that it returns to the zero-touch
   defaults with FortiLink discovery enabled, and set your admin password at
   the next login before it is authorized (FortiOS 7.6.1 and later generate a
   password for a switch that has none, p. 43):

   ```text
   FSW # execute factoryreset
   ```

6. Wait for `Discovered/Down`, then authorize, describe, and re-bind the profile
   in one step:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set description "FSW-A lab-174"
   set switch-profile "fsw-174-prof"
   set fsw-wan1-admin enable
   next
   end
   ```

7. Wait for `Authorized/Up` at `10.255.1.2`, and check that the switch kept the
   firmware from Lab 3.3 (a factory reset does not change the image):

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # execute ping 10.255.1.2
   FSW # get system status
   ```

**Track 2:** Practice the discovery-disabled list with the serial of a
documented switch that is not yours, `S124EN5918003682` (FortiLink Guide 7.6.7,
p. 52). Add it, show it, and remove it again with `unselect` inside
`config switch-controller global` (p. 322):

```text
FGT # config switch-controller global
append disable-discovery S124EN5918003682
end
FGT # show switch-controller global
FGT # config switch-controller global
unselect disable-discovery S124EN5918003682
end
```

Then, if the stand-in entry exists, deauthorize it, record its STATUS in
`get-conn-status`, and authorize it again:

```text
FGT # config switch-controller managed-switch
edit S248EPTF18000000
set fsw-wan1-admin disable
next
end
FGT # execute switch-controller get-conn-status
FGT # config switch-controller managed-switch
edit S248EPTF18000000
set fsw-wan1-admin enable
next
end
```

**Track 2: read-and-predict.**

1. An administrator retires a switch with
   `execute switch-controller factory-reset <switch-id>`, leaves it cabled,
   and finds it managed again the next morning. Predict why, and which command
   would have prevented it. **Answer:** `factory-reset` returns the switch to
   factory defaults with FortiLink auto-discovery, so a controller can detect
   it, and with automatic authorization enabled, adopt it (p. 322).
   `switch-action set-standalone` also resets the switch but prevents automatic
   detection and authorization; this lab's manual authorization would also have
   kept it at `Discovered`.
2. After deauthorizing a FortiSwitch through **Security Fabric > Fabric
   Connectors**, `show system csf` contains:

   ```text
   config trusted-list
       edit "S248DF3X17000482"
           set action deny
       next
   end
   ```

   Predict what this entry records. **Answer:** that the switch was
   deauthorized from the Security Fabric; the FortiLink Guide (p. 321) says
   deauthorized devices' serial numbers are saved in this trusted list, here
   with `action deny`.

**Expected result:** Track 1: after `set-standalone`, the switch ran standalone,
reported no FortiLink session, and did not rejoin on its own; after the reset and
re-authorization, `<SWITCH_SN>` is `Authorized/Up` at `10.255.1.2` on the Lab 3.3
build, with description `FSW-A lab-174` and profile `fsw-174-prof`, and
`disable-discovery` does not list it. Track 2: `S124EN5918003682` was added to
and removed from `disable-discovery`, and the stand-in entry is authorized
again.

**Negative test:** Between steps 3 and 4, unplug and replug the FortiLink cable
on the standalone switch and wait five minutes without resetting it.
`get-conn-status` does not show it as `Authorized/Up`, and the switch console
still reports no FortiLink session: a switch retired with `set-standalone` does
not rejoin when it is reconnected. Record whether it appears as `Discovered` at
all. Track 2: `show switch-controller global` after `unselect` no longer lists
`S124EN5918003682`.

**Rollback:** If the re-adoption fails, run Lab 2.4's go/no-go checks; the
switch's state after a failed attempt is the same as at the start of Lab 3.1, so
you can repeat Lab 3.1. Restore the controller from `fgt-pre-3-5-174.conf` only
if the entries are damaged.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 3.1 to 3.5 have been run end to end, including
each negative test. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A managed FortiSwitch moves from `Discovered/Down` to `Authorized/Up` when you
set `fsw-wan1-admin enable` on its entry, and `get-conn-status` on the
controller, with the switch's own `get-conn-status`, shows every step. The
initial-config templates turn into the auto-created VLANs and DHCP servers on
the FortiLink interface, and they are fixed once a switch has been authorized.
The controller stages and installs switch firmware, applies switch profiles and
custom commands, and keeps the configuration synchronized. `set-standalone`
retires a switch so that it does not rejoin; a factory reset and a new
authorization adopt it again. The switch ends the chapter managed, on your
chosen build, with the profile `fsw-174-prof` bound.

- [ ] I authorized the switch and read every column of `get-conn-status`,
      including the flags.
- [ ] I found the trunk that FortiLink formed on the switch and know how a
      second switch would join.
- [ ] I recorded the templates, the reserved network, and the auto-created VLAN
      interfaces and their addresses.
- [ ] I pushed a FortiSwitchOS image from the controller and read
      `get-upgrade-status`.
- [ ] I bound a switch profile, used a custom command executed once and bound,
      and forced a configuration synchronization.
- [ ] I retired the switch with `set-standalone`, showed that it did not rejoin,
      and adopted it again.
- [ ] On Track 2, the stand-in entry `S248EPTF18000000` exists (if FortiOS
      accepted it) with `fsw-174-prof` bound, and my predictions are recorded.
