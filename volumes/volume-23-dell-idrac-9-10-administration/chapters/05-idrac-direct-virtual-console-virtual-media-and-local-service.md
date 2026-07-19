# Chapter 05: iDRAC Direct, Virtual Console, Virtual Media, and Local Service

## Learning Objectives

- Use iDRAC Direct for local, network-independent configuration and
  troubleshooting access.
- Use Quick Sync to retrieve status and perform limited configuration from
  a mobile device without a network connection.
- Launch and use the HTML5 Virtual Console for remote KVM access,
  including during BIOS POST and OS installation.
- Mount Virtual Media (local image, remote file share, or a mapped folder)
  to install an operating system or run diagnostic media remotely.
- Install and use the iDRAC Service Module (iSM) to extend management
  visibility into the host OS, and explain what it adds beyond pure
  out-of-band monitoring.

## Theory and Architecture

### iDRAC Direct

iDRAC Direct is a local, physical connection to iDRAC over a USB port on
the front of the chassis (Micro-USB on older platforms, USB-C on current
15G/16G/17G hardware), independent of any network configuration. Connect
a laptop directly to this port and iDRAC presents itself as a USB network
adapter, reachable at a fixed local address without needing DHCP, DNS, or
any of the network configuration covered in [Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md). This makes iDRAC
Direct the single most important recovery tool in this volume: it works
even when the management network is entirely misconfigured, unplugged, or
unreachable, because it bypasses the network path entirely.

iDRAC Direct also supports a specific provisioning use case: connecting a
USB flash drive (rather than a laptop) to the same front port to run a
Server Configuration Profile import automatically at boot, useful for
zero-touch or low-touch initial configuration in environments without
convenient network access to a new server during unboxing.

### Quick Sync

Quick Sync (in its second and third-generation implementations, Quick
Sync 2/3 depending on platform and license tier) provides Bluetooth
Low Energy and near-field communication (NFC) access to basic iDRAC
status and limited configuration from Dell's OpenManage Mobile
application, without requiring any network connection at all — useful for
a walk-the-row health check or for grabbing a server's current IP address
and health state before deciding whether a laptop-based iDRAC Direct
session or a full network session is actually needed.

### Virtual Console

Virtual Console is a browser-based (HTML5) remote KVM (keyboard, video,
mouse) session, giving you the same experience as a monitor and keyboard
physically attached to the server — including full visibility into BIOS
POST screens, boot menu selection, and OS installer interaction, none of
which any in-OS remote access tool (RDP, SSH) can provide, because those
tools depend on an OS already being installed and running. Virtual
Console supports configurable screen resolution and color depth, session
recording (license-tier dependent), and multi-user collaborative sessions
where a specified number of users can view or share control of the same
console simultaneously — useful for pairing a remote engineer with
Dell support during a complex diagnostic session.

### Virtual Media

Virtual Media lets you attach an ISO or IMG image to the remote server as
if it were a physically inserted optical drive or USB device, from three
source types: a file on your local workstation (uploaded through the
browser session), a file on a network share (CIFS/NFS/HTTP(S)) that
iDRAC mounts directly without routing the image through your browser, and
a "Connect Virtual Media" mapped-folder mode for ad hoc local file access.
Combined with Virtual Console, Virtual Media makes full remote OS
installation possible on a server with no OS currently installed and no
physical media inserted — you watch BIOS POST, select the mounted image as
the boot device, and interact with the OS installer, entirely over the
network.

### The iDRAC Service Module (iSM)

Everything described above is purely out-of-band: iDRAC observes hardware
sensors and controls hardware directly, with no dependency on the host OS.
iSM is the deliberate exception — a lightweight agent installed inside the
host OS (Windows and major Linux distributions are supported; confirm
current OS support against the iSM release notes for your baseline) that
extends iDRAC's visibility with information genuinely easier or only
possible to gather in-band: the OS name and version, some in-band SSD/NVMe
wear-level detail, Windows Server Failover Clustering awareness for
coordinated maintenance operations, and a faster in-band channel for
certain operations (like triggering an OS-graceful shutdown) than a purely
out-of-band power command provides. iSM is optional — every core
capability in this volume works without it — but it materially improves
inventory accuracy and enables a small number of specific workflows that
this chapter and later chapters call out explicitly where iSM is required
rather than merely helpful.

### OS-to-iDRAC Pass-through

A related, Enterprise-tier capability, OS-to-iDRAC Pass-through, lets iSM
and iDRAC communicate over an internal USB-based network path (or, on
some configurations, the shared LOM path) rather than requiring the host
OS to reach iDRAC's management network at all — useful where host OS
network policy is deliberately restrictive and you don't want to carve out
an explicit path to the management network just for iSM's traffic.

## Design Considerations

- **Treat iDRAC Direct access as a documented recovery procedure, not an
  ad hoc one.** Every administrator who might need to recover a
  misconfigured server should know, before an incident, where the front
  USB port is on each platform in your fleet and what the fixed local
  address is — this is exactly the kind of procedure that is trivial when
  documented in advance and frustrating to reconstruct during an actual
  outage.
- **Decide Virtual Console resolution/bandwidth trade-offs for your WAN
  topology.** A high-resolution, high-color-depth console session over a
  low-bandwidth WAN link to a remote site produces a sluggish experience;
  lower the configured resolution for remote-site servers rather than
  troubleshooting apparent "slowness" that is actually a bandwidth
  mismatch.
- **Prefer network-share-based Virtual Media for repeated or large-image
  operations; reserve browser-upload mode for occasional single
  operations.** Uploading a multi-gigabyte ISO through a browser session
  is slow and ties up your workstation's upload bandwidth for the
  duration; a CIFS/NFS/HTTP(S) share iDRAC mounts directly is both faster
  and reusable across multiple servers without re-uploading.
- **Decide iSM deployment policy fleet-wide, driven by which specific
  capabilities you need.** If your environment depends on in-band OS
  version inventory accuracy, Windows cluster-aware maintenance, or
  OS-to-iDRAC Pass-through, standardize iSM installation into your OS
  build/image process so it is present from first boot rather than
  retrofitted inconsistently across an existing fleet.
- **Plan for the case where a remote site has no local hands and no
  physical access.** iDRAC Direct's local-only nature means it cannot help
  a truly remote administrator with no one at the site; for such
  locations, invest more heavily in getting the network path ([Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md))
  and Virtual Console/Media reliably right the first time, since physical
  recovery is not a realistic fallback.

## Implementation and Automation

### Connecting via iDRAC Direct

1. Connect a laptop's USB port to the server's front iDRAC Direct port
   using a USB-C-to-USB-C or Micro-USB cable, depending on platform.
2. Wait for the laptop to detect a new USB network adapter (typically
   completes within 10-30 seconds).
3. Browse to the fixed iDRAC Direct address (commonly `169.254.1.1` or a
   platform-documented equivalent; confirm the exact address for your
   specific generation in the iDRAC User's Guide, since it is a
   link-local address reserved specifically for this purpose and has been
   consistent across recent generations but should be confirmed rather
   than assumed).
4. Log in with the same credentials used for network access — iDRAC
   Direct is the same controller, reached over a different physical path,
   not a separate management identity.

### Enabling and using Quick Sync

```bash
racadm set iDRAC.QuickSync.Enable Enabled
racadm set iDRAC.QuickSync.ReadAuthentication Enabled
```

Pair a mobile device running OpenManage Mobile per the app's pairing flow;
no further RACADM configuration is required for basic read access once
Quick Sync is enabled.

### Launching Virtual Console

From the GUI: System > Virtual Console, or directly via a launch URL
pattern once authenticated. Over RACADM, you can confirm and adjust
Virtual Console configuration:

```bash
racadm set iDRAC.VirtualConsole.Enable Enabled
racadm set iDRAC.VirtualConsole.MaxSessions 2
racadm set iDRAC.VirtualConsole.AttachState Auto
```

Over Redfish, Virtual Console session launch is typically initiated
through iDRAC's OEM `VirtualConsole` action or by retrieving a
console-launch URL/token from the `Oem.Dell` extension of the `Manager`
resource; confirm the current mechanism against your firmware's Redfish
API guide, since browser-based KVM session establishment is one of the
less standardized corners of the Redfish schema across BMC vendors.

### Mounting Virtual Media from a network share

Via RACADM, attaching an ISO from a CIFS share and setting it as the next
boot device:

```bash
racadm remoteimage -c -l //10.0.0.60/images/rhel10-install.iso \
  -u svc-media -p '<password>'
racadm set iDRAC.ServerBoot.FirstBootDevice VCD-DVD
racadm set iDRAC.ServerBoot.BootOnce Enabled
racadm serveraction powercycle
```

Over Redfish, using the standard `VirtualMedia` resource:

```bash
curl -s -k -u root:'<password>' -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "Image": "https://10.0.0.60/images/rhel10-install.iso",
        "Inserted": true,
        "WriteProtected": true
      }' \
  https://192.168.1.120/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia

curl -s -k -u root:'<password>' -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"Boot": {"BootSourceOverrideTarget": "Cd", "BootSourceOverrideEnabled": "Once"}}' \
  https://192.168.1.120/redfish/v1/Systems/System.Embedded.1

curl -s -k -u root:'<password>' -X POST \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "ForceRestart"}' \
  https://192.168.1.120/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset
```

A Python helper that combines these steps into a single unattended-install
bootstrap, useful when kicking off a batch of OS installations from a
provisioning pipeline:

```python
#!/usr/bin/env python3
"""idrac_mount_and_boot.py — mount a network-hosted ISO as Virtual Media,
set it as the one-time boot device, and force-restart the server.

Usage: python3 idrac_mount_and_boot.py <idrac-ip> <username> <password> \
    <iso-http-url>
"""
import sys
import requests

requests.packages.urllib3.disable_warnings()


def main() -> None:
    host, user, password, iso_url = sys.argv[1:5]
    session = requests.Session()
    session.auth = (user, password)
    session.verify = False

    insert = session.post(
        f"https://{host}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia",
        json={"Image": iso_url, "Inserted": True, "WriteProtected": True},
        timeout=60,
    )
    insert.raise_for_status()

    boot = session.patch(
        f"https://{host}/redfish/v1/Systems/System.Embedded.1",
        json={"Boot": {"BootSourceOverrideTarget": "Cd", "BootSourceOverrideEnabled": "Once"}},
        timeout=30,
    )
    boot.raise_for_status()

    restart = session.post(
        f"https://{host}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
        json={"ResetType": "ForceRestart"},
        timeout=30,
    )
    restart.raise_for_status()
    print("ISO mounted, one-time boot to CD set, server restarted.")


if __name__ == "__main__":
    main()
```

### Installing the iDRAC Service Module

On a running host OS (Linux example, package delivered as part of the
Dell OpenManage/System Update repository or a downloaded installer):

```bash
sudo yum install -y --nogpgcheck dell-system-update-idsm
sudo systemctl enable --now dcism
```

Confirm current package names and install method against the iSM release
notes for your host OS and version — package naming and the supported OS
matrix change across iSM releases. Confirm installation succeeded from
the iDRAC side:

```bash
racadm get iDRAC.OS-BMC.OSInfo
```

## Validation and Troubleshooting

- **Laptop doesn't detect a USB network adapter when connected via iDRAC
  Direct.** Confirm the correct port (front iDRAC Direct port, not a host
  OS-facing USB port — these are physically distinct and easy to confuse
  on some chassis) and confirm your laptop's OS has picked up the correct
  USB networking driver; a reboot of the USB connection (unplug/replug)
  resolves most detection issues.
- **Virtual Console launches but shows a black screen.** Confirm the host
  is actually powered on and past very early POST (a screen genuinely has
  no video output during the first moment of power-on); if the host is
  confirmed running and the screen remains black, check Virtual Console
  plugin/Java or HTML5 renderer compatibility in your browser, and
  confirm `iDRAC.VirtualConsole.Enable` is set to `Enabled`.
- **Virtual Media mount from a network share fails.** Confirm the iDRAC
  network path ([Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)) can reach the share host specifically — this
  is a common gap when the share lives on a general file-server VLAN not
  included in the management network's routing/firewall rules — and
  confirm the share credentials and permissions allow read access to the
  specific image path.
- **OS installer boots from local disk instead of the mounted image.**
  Confirm `BootSourceOverrideEnabled`/`FirstBootDevice` was actually set
  before the restart, not after — a restart issued before the boot
  override is applied simply boots the existing configured device order.
- **iSM shows as not installed or not communicating from the iDRAC
  side even after installation.** Confirm the service
  (`dcism` on Linux, the equivalent Windows service) is running, and check
  OS-to-iDRAC Pass-through configuration if you expect iSM traffic to use
  that path rather than the host's production network route to iDRAC.

## Security and Best Practices

- Restrict who has physical rack access, since iDRAC Direct intentionally
  bypasses network-layer access controls — physical access control is the
  actual security boundary for this path, not an iDRAC setting.
  Confirm this expectation is documented in your physical security policy
  rather than assumed.
- Use write-protected (`WriteProtected: true`) Virtual Media mounts for
  installer and diagnostic images, so a mounted image cannot be
  inadvertently modified by the booted environment.
  - Prefer HTTPS-hosted or authenticated CIFS/NFS shares for Virtual Media
  sources over unauthenticated network paths, since the mount operation
  itself transmits share credentials and, depending on protocol, image
  content across the network.
- Limit Virtual Console `MaxSessions` and monitor concurrent session
  count; an unexpectedly high concurrent session count on a server that
  should have none active is a meaningful anomaly signal worth alerting
  on.
- Standardize iSM deployment through your OS build pipeline rather than
  ad hoc post-install scripts, so its presence (and therefore the
  in-band inventory and pass-through capabilities it enables) is
  consistent and auditable across the fleet rather than dependent on
  whether an individual administrator remembered to install it.

## References and Knowledge Checks

**References**

- [Dell Technologies, *iDRAC9/iDRAC10 User's Guide*](https://www.dell.com/support/product-details/en-us/product/idrac10-lifecycle-controller-v1-xx-series/resources/manuals) — iDRAC Direct, Quick
  Sync, Virtual Console, and Virtual Media chapters
- [Dell Technologies, *iDRAC Service Module Installation Guide*](https://www.dell.com/support/manuals/en-us/dell-idrac-service-module-2.0/ism_ig_2.5/introduction)
- [Dell Technologies, *iDRAC RACADM CLI Guide*](https://www.dell.com/support/manuals/en-us/idrac9-lifecycle-controller-v4.x-series/idrac_4.00.00.00_racadm/supported-racadm-interfaces?guid=guid-a5747353-fc88-4438-b617-c50ca260448e&lang=en-us) — `remoteimage`,
  `iDRAC.VirtualConsole`, and `iDRAC.QuickSync` command/attribute
  reference
- [Dell Technologies, *iDRAC Redfish API Guide*](https://www.dell.com/support/kbdoc/en-us/000178045/redfish-api-with-dell-integrated-remote-access-controller) — `VirtualMedia` resource
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated iDRAC9/iDRAC10
  baseline

**Knowledge Checks**

1. Why is iDRAC Direct considered the most important recovery access path
   in this volume, and what does it not depend on that every other access
   path does?
2. What can Virtual Console show you that no in-OS remote access tool
   (RDP, SSH) can, and why?
3. Why is a network-share-based Virtual Media mount generally preferred
   over browser-upload mode for repeated operations?
4. What does the iDRAC Service Module add that pure out-of-band
   monitoring cannot provide, and why is it optional rather than
   required?
5. What is the actual security boundary that protects against misuse of
   iDRAC Direct, given that it bypasses network-layer access controls?

## Hands-On Lab

**Objective:** Use iDRAC Direct (or, if physical USB access is
unavailable in your lab, thoroughly document the procedure as a
walkthrough) for local access, mount a Virtual Media image from a network
share, and boot to it via Virtual Console.

**Prerequisites**

- The lab server configured in Chapters 1 through 4, with physical access
  for the iDRAC Direct portion of this lab (or willingness to complete
  that step as a documented walkthrough if physical access is
  unavailable).
- A small ISO image suitable for a boot test (a lightweight Linux live
  image is sufficient and avoids a lengthy install) hosted on an
  HTTP(S) or CIFS/NFS share reachable from the lab iDRAC's management
  network.
- A laptop with a compatible USB port and cable for the iDRAC Direct
  portion.
- Python 3.11+ with `requests` installed for the scripted portion.

**Steps**

1. Connect your laptop to the server's front iDRAC Direct port and
   confirm a USB network adapter is detected. Browse to the documented
   iDRAC Direct address and log in. **Expected result:** you reach the
   same iDRAC login and dashboard as network access provides, confirming
   this is the same controller reached over a different physical path.
2. Disconnect the iDRAC Direct cable and reconnect over your normal
   management network for the remainder of this lab.
3. Launch Virtual Console from the GUI. **Expected result:** you see the
   server's current console output (OS login prompt, BIOS setup, or POST,
   depending on current host state).
4. From your workstation, mount your test ISO as Virtual Media using the
   `idrac_mount_and_boot.py` script from the Implementation and
   Automation section:

   ```bash
   python3 idrac_mount_and_boot.py <idrac-ip> root '<password>' \
     https://10.0.0.60/images/test-live.iso
   ```

   **Expected result:** the script completes without error; within a
   short time, the Virtual Console window shows the server restarting and
   booting from the mounted image rather than its normal boot device.
5. Confirm virtual media state via RACADM:

   ```bash
   racadm get iDRAC.VirtualMedia
   ```

   **Expected result:** the CD/DVD virtual media slot reports as attached
   with the mounted image path.
6. **Negative test:** attempt to mount an image path that does not exist
   on the share:

   ```bash
   python3 idrac_mount_and_boot.py <idrac-ip> root '<password>' \
     https://10.0.0.60/images/does-not-exist.iso
   ```

   **Expected result:** the insert-media call fails with an error
   (typically a Redfish extended-info error indicating the image could
   not be retrieved), and the server does not boot from an empty/invalid
   mount — confirming the mount step fails safely rather than booting to
   an unpredictable state.
7. Eject the virtual media and restore normal boot order:

   ```bash
   curl -s -k -u root:'<password>' -X POST \
     -H "Content-Type: application/json" -d '{}' \
     https://<idrac-ip>/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia
   racadm set iDRAC.ServerBoot.BootOnce Disabled
   ```

**Cleanup**

- Confirm Virtual Media is ejected (step 7) so a subsequent normal reboot
  does not unexpectedly boot to test media again.
- Power the host back to its prior state (off, if it was off before this
  lab; running its normal OS, if it was running one) to leave the lab
  server in the same condition later chapters expect.

## Summary and Completion Checklist

This chapter covered the full set of local and remote interactive access
paths iDRAC provides beyond pure API/CLI automation: iDRAC Direct as the
network-independent recovery path, Quick Sync for connectionless status
checks, Virtual Console for full remote KVM including BIOS-level access,
Virtual Media for remote OS installation and diagnostics, and the iDRAC
Service Module as the deliberate, optional bridge between out-of-band and
in-band visibility. These capabilities underpin the hardware health
monitoring in [Chapter 6](06-hardware-health-power-thermal-logs-and-support.md) and the firmware/OS deployment workflows in
Chapters 8 and 9.

- [ ] I can use iDRAC Direct to reach iDRAC locally, independent of
      network configuration.
- [ ] I can explain what Quick Sync provides and when it's the right tool
      versus a full network or Virtual Console session.
- [ ] I launched Virtual Console and can explain what it shows that no
      in-OS remote access tool can.
- [ ] I mounted Virtual Media from a network share and booted a server
      from it, including a negative test for an invalid image path.
- [ ] I can explain what the iDRAC Service Module adds beyond pure
      out-of-band monitoring and when it's required versus optional.
