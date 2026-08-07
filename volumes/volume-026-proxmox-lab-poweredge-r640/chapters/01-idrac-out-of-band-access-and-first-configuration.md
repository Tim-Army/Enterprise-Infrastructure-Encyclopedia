# Chapter 01: iDRAC Out-of-Band Access and First Configuration

## Learning Objectives

- Explain what iDRAC provides and why the build starts with it.
- Set the iDRAC to its assigned static address, 10.30.161.25/24, with
  gateway 10.30.161.1.
- Reach the iDRAC web interface and virtual console from a workstation.
- Confirm the server's health and inventory before touching storage.
- Establish the out-of-band access every later chapter depends on.

## Theory and Architecture

### Why the build begins at the iDRAC

Every phase after this one — configuring RAID, installing Proxmox, watching
the boot, recovering from a mistake — is far easier with out-of-band access
than without it. The **iDRAC (integrated Dell Remote Access Controller)**
is a small computer inside the R640 that runs independently of the host
operating system, with its own network port, its own address, and a virtual
console that shows the server's screen and keyboard over the network. It is
covered in depth in
[Volume XXIII](../../volume-023-dell-idrac-9-10-administration/README.md);
this chapter uses only what this build needs.

Starting here means the rest of the build can be done from a desk rather
than a crash cart. The RAID configuration in
[Chapter 02](02-storage-boss-boot-mirror-and-the-river-raid-5-array.md) and
the Proxmox installation in
[Chapter 03](03-installing-proxmox-ve.md) are both driven through the iDRAC
virtual console, so the iDRAC must be reachable first.

### The two addresses on the management subnet

This build places two things on the 10.30.161.0/24 management network, and
they are distinct:

- **The iDRAC itself** at **10.30.161.25/24** — the out-of-band controller,
  reachable whether or not the host OS is running.
- **The Proxmox host's management interface** at **10.30.161.10/24** —
  configured later, in
  [Chapter 05](05-network-architecture-management-nic-vlan-trunk-and-bridges.md),
  once the OS is installed.

Both use gateway **10.30.161.1**, and both are on the same subnet. That is
normal and intended: the out-of-band controller and the host management
interface commonly share a management network at different addresses. Do
not confuse them — the iDRAC address answers when the server is powered off
at the OS level; the host address does not.

### How the iDRAC gets its address

The iDRAC's network settings are set in one of three places, and any of
them works for this build:

- **The physical LCD panel** on the front of the server, if fitted.
- **The BIOS/UEFI System Setup**, reached by pressing F2 at boot and
  entering iDRAC Settings.
- **A DHCP lease**, if the network offers one, which can then be made
  static.

Because this build assigns a *specific* static address, the cleanest path
is to set it explicitly in System Setup rather than rely on DHCP and
convert it afterward.

## Design Considerations

- **Give the iDRAC a dedicated management port and keep it off the data
  network.** The R640's dedicated iDRAC port keeps out-of-band traffic
  separate from the VLAN-trunked data NIC configured in Chapter 05. This is
  a security boundary, not just tidiness — the iDRAC is a tier-0 access
  path into the server.
- **Assign the iDRAC address before anything else.** Every later step is
  easier with it, and setting it first means the storage and install phases
  can be done remotely.
- **Record the iDRAC address and credentials in a vault immediately.** It
  is the master key to the hardware; its default credentials must be
  changed and the new ones stored securely from the outset.
- **Confirm firmware currency early.** An out-of-date iDRAC or BIOS is
  easier to update now, before Proxmox and workloads are running, than
  during a maintenance window later.

## Implementation and Automation

### 1. Setting the iDRAC static address in System Setup

Power on the R640 and press **F2** for System Setup, then **iDRAC
Settings → Network**:

```text
Enable NIC:            Enabled
NIC Selection:         Dedicated          # the dedicated iDRAC port
IPv4 Settings:
  Enable IPv4:         Enabled
  Enable DHCP:         Disabled           # static, per this build
  Static IP Address:   10.30.161.25
  Static Subnet Mask:  255.255.255.0      # /24
  Static Gateway:      10.30.161.1
  Static DNS 1:        10.30.161.1         # the gateway also serves DNS
```

Apply, and the iDRAC restarts its network stack at the new address within a
minute or so.

### 2. Confirming reachability from a workstation

From a machine on (or routed to) the management network:

```bash
# The iDRAC should answer at its new address.
ping -c 3 10.30.161.25

# The web interface listens on HTTPS.
curl -sk -o /dev/null -w '%{http_code}\n' https://10.30.161.25/
```

A `200` (or a redirect to the login page) confirms the web interface is up.
Browse to `https://10.30.161.25/` and log in with the iDRAC credentials —
change the default password immediately if it has not been changed.

### 3. Confirming health and inventory before proceeding

From the RACADM command line (over SSH to the iDRAC, or the Lifecycle
Controller), confirm the server is healthy and has the hardware this build
assumes:

```bash
# Overall system health — should be OK before configuring storage.
racadm -r 10.30.161.25 -u root -p <password> getsensorinfo | head

# Confirm the storage controllers and physical disks are seen: the BOSS
# card and the six front drives Chapter 02 will use.
racadm -r 10.30.161.25 -u root -p <password> storage get controllers
racadm -r 10.30.161.25 -u root -p <password> storage get pdisks
```

The physical-disk list must show the two BOSS SSDs and the six front
drives; if it does not, the storage in Chapter 02 cannot be built.

## Validation and Troubleshooting

### Confirming the iDRAC is genuinely reachable

| Check | Command | Failure means |
| --- | --- | --- |
| Address is live | `ping 10.30.161.25` | Wrong NIC selection, cabling, or address not applied |
| Web UI responds | `curl -sk https://10.30.161.25/` | iDRAC web service down or firewall in the path |
| Virtual console opens | Launch from the web UI | Java/HTML5 console or browser issue |
| Disks are visible | `racadm ... storage get pdisks` | A drive not seated, or a controller fault |

### The most common first-access problem

If the iDRAC does not answer at 10.30.161.25, the usual cause is **NIC
Selection**: the address was set but applied to the shared LOM rather than
the dedicated port, or vice versa, so it is live on a port that is not
cabled. Re-check that **NIC Selection is Dedicated** and that the cable is
in the dedicated iDRAC port, not a data port. This single setting accounts
for most "the iDRAC won't come up" cases.

## Security and Best Practices

- **Change the default iDRAC password before connecting it to any
  network.** The out-of-band controller is a full remote path into the
  server, including power control and the console; default credentials on
  it are a critical exposure.
- **Keep the iDRAC on an isolated management network.** It should not be
  reachable from the VLAN-trunked data network or the internet. The
  dedicated port and the separate 10.30.161.0/24 subnet are that isolation.
- **Restrict and log iDRAC access.** Limit which management stations may
  reach it, and enable its logging; the Lifecycle Log records who did what
  through the controller.
- **Update iDRAC and BIOS firmware now.** Doing it before workloads run
  avoids a disruptive update later, and current firmware closes known
  vulnerabilities in the most privileged component of the server.

## References and Knowledge Checks

**References**

- [Volume XXIII, Chapter 01](../../volume-023-dell-idrac-9-10-administration/chapters/01-architecture-generations-licensing-and-first-access.md)
  — iDRAC architecture, generations, and first access in depth.
- [Volume XXIII, Chapter 03](../../volume-023-dell-idrac-9-10-administration/chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)
  — iDRAC management networking, which this chapter applies to one host.
- [Dell iDRAC documentation](https://www.dell.com/support/home/en-us/product-support/product/idrac9-lifecycle-controller-v4.x-series/docs)
  — the authoritative configuration reference.

**Knowledge checks**

1. Why does this build configure the iDRAC before anything else?
2. Distinguish the iDRAC address (10.30.161.25) from the Proxmox management
   address (10.30.161.10) — what is different about when each responds?
3. What NIC Selection value does this build use, and what is the symptom of
   getting it wrong?
4. Which two sets of physical disks must appear in the iDRAC inventory
   before Chapter 02 can proceed?
5. Why is changing the default iDRAC password a critical first step rather
   than a later hardening task?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each first-access task on the lab R640's
iDRAC** — the out-of-band foundation the whole build depends on. Commands are real RACADM/iDRAC
actions on the specific server. Each ends **`**Lab verified by:** *pending*`** until a human runs
it.

**Shared prerequisites for Labs 1.1–1.4** — the target Dell PowerEdge R640 racked and powered, its
iDRAC cabled to the management network, and a workstation with SSH and a browser. **Cost:** none.

### Lab 1.1 — First iDRAC access and password change (Topic: First access)

**Objective:** Log in and secure the controller.

```bash
ssh <idrac-ip> -l root        # default password on the pull-out service tag / factory label
racadm getsysinfo | grep -iE "System Model|Service Tag|iDRAC"
racadm set iDRAC.Users.2.Password '<strong-password>'    # change the default admin password
```

**Expected result:** `getsysinfo` prints the R640 model, service tag, and iDRAC version, and the
default password is changed — the iDRAC is the out-of-band controller that will drive storage,
install, and console for this build, so securing it first is step zero.

**Negative test:** leave the factory-default iDRAC password; anyone on the management network can
take over the server's out-of-band controller — changing it is the first hardening step.

**Cleanup:** none (keep the new password).

### Lab 1.2 — iDRAC management network (Topic: Network configuration)

**Objective:** Give the iDRAC a stable static address.

```bash
racadm set iDRAC.IPv4.DHCPEnable Disabled
racadm set iDRAC.IPv4.Address 10.30.161.25
racadm set iDRAC.IPv4.Netmask 255.255.255.0
racadm set iDRAC.IPv4.Gateway 10.30.161.1
racadm get iDRAC.IPv4.Address
```

**Expected result:** the iDRAC holds a static management IP — the controller must be reliably
reachable at a fixed address throughout the build (and afterward for operations), so it is not left
on DHCP.

**Negative test:** run the build with the iDRAC on DHCP; a lease change mid-install drops your
console/virtual-media session — a static address keeps out-of-band access stable.

**Cleanup:** none (keep the static address).

### Lab 1.3 — Virtual console and virtual media (Topic: Remote presence)

**Objective:** Prepare the remote install path.

```bash
racadm set iDRAC.VirtualConsole.Enable Enabled
racadm get iDRAC.VirtualConsole.Enable
# GUI: https://10.30.161.25 > Virtual Console (HTML5) launches the server screen;
#   Virtual Media will mount the Proxmox ISO in Chapter 03.
```

**Expected result:** the virtual console launches to the server's screen and virtual media is
available — these are how Proxmox is installed with no monitor or USB stick at the rack; the whole
OS install (Chapter 03) runs through them.

**Negative test:** plan to install Proxmox by walking a USB stick to the rack; virtual console/media
do it remotely — for a headless lab server they are the install path.

**Cleanup:** none.

### Lab 1.4 — Server readiness and health (Topic: Operational readiness)

**Objective:** Confirm the server is healthy before building on it.

```bash
racadm getsensorinfo | grep -iE "System Board|PS Redundancy|Fan" | head
racadm serveraction powerstatus
racadm getversion
```

**Expected result:** healthy sensors, known power state, and current firmware versions (iDRAC/BIOS/
PERC) — verifying hardware health and firmware before installing avoids building on a faulty PSU,
fan, or an out-of-date controller that would cause problems later.

**Negative test:** install the OS onto a server with a failing PSU or badly outdated PERC firmware;
you chase phantom OS issues that are really hardware — a health/firmware check first rules that out.

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The build begins at the iDRAC because out-of-band access makes every
subsequent phase — RAID, install, recovery — remotely operable rather than
requiring a crash cart. The iDRAC is set to its static address
10.30.161.25/24 on gateway 10.30.161.1 through System Setup, on the
dedicated management port that keeps out-of-band traffic isolated from the
VLAN-trunked data network. It shares the management subnet with the host's
own management address (10.30.161.10, configured later) at a distinct
address. Before touching storage, the iDRAC inventory must confirm the two
BOSS SSDs and six front drives the next chapter depends on, and the default
password must be changed — the controller is the most privileged access
path into the server.

- [ ] iDRAC reachable at 10.30.161.25 with the web UI and console open.
- [ ] NIC Selection is Dedicated and the address survives a reboot.
- [ ] Overall system health is OK.
- [ ] The BOSS SSDs and six front drives appear in the inventory.
- [ ] The default iDRAC password has been changed and vaulted.
