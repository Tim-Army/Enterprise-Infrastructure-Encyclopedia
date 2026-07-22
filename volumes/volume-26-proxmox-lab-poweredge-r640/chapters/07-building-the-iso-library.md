# Chapter 07: Building the ISO Library

## Learning Objectives

- Obtain each of the nine installation images this lab requires.
- Understand the licensing and entitlement reality of each image honestly.
- Place the ISOs into the `river` ISO repository correctly.
- Verify image integrity before an image becomes a running system.
- Distinguish plain ISO installs from appliance imports.

## Theory and Architecture

### The library and where it lives

The nine virtual machines in
[Chapter 08](08-deploying-the-virtual-machines.md) are each built from an
image in the ISO repository created on `river` in
[Chapter 06](06-proxmox-storage-the-river-datastore-and-iso-repository.md).
This chapter assembles that library. The images fall into three groups by
how you obtain them, and being honest about that distinction matters — some
are free downloads, some need an account or entitlement, and one is
commercial and cannot be redistributed.

### The honest licensing picture

This encyclopedia's editorial standard is to name resources plainly and
state their real constraints rather than pretend everything is a free
download. The nine images:

| Image | Obtaining it | Licensing reality |
| --- | --- | --- |
| Ubuntu Desktop | ubuntu.com | Free, open — download and use |
| Ubuntu Server | ubuntu.com | Free, open — download and use |
| EVE-ng | eve-ng.net (Community) | Free community edition; an OVA/ISO |
| GNS3 | gns3.com | Free; deployed as the **GNS3 VM appliance**, not a plain OS ISO |
| Cisco CML | Cisco (licensed customers) | **Commercial, license-gated** — no free download; requires purchase and entitlement |
| Red Hat Desktop | Red Hat (account) | Needs a Red Hat account; the **free Developer subscription** covers lab use up to a set number of systems |
| Red Hat Server | Red Hat (account) | Same RHEL image as above, installed with a server profile |
| Windows 11 | Microsoft | **Evaluation** ISO (time-limited), or a licensed image |
| Windows Server | Microsoft | **Evaluation** ISO (180-day), or a licensed image |

Two points worth stating clearly:

- **Cisco CML is not free and cannot be redistributed.** This volume
  documents deploying it, but the licensed image must come from your own
  Cisco entitlement. There is no "copy the free CML ISO" step, because there
  is no free CML ISO.
- **Red Hat provides a genuinely free path for labs.** The Red Hat Developer
  subscription issues licenses at no cost for lab use up to a set quantity of
  systems, which is the route this build uses for the two RHEL machines — one
  image, installed twice with different profiles (desktop and server).

### ISOs versus appliances

Not everything in the library is a plain operating-system ISO you boot an
installer from:

- **Plain ISOs** — Ubuntu Desktop/Server, RHEL, Windows 11/Server: you boot
  the installer and install the OS. These go in the ISO repository and are
  used as boot media in Chapter 08.
- **Appliances** — GNS3 is normally deployed as the **GNS3 VM**, a
  pre-built appliance image rather than an OS you install; EVE-ng is
  distributed as an OVA/ISO that is more appliance than plain installer.
  These are imported rather than installed from scratch.

The distinction changes how Chapter 08 creates the VM — an installer ISO
boots into a setup program, an appliance is imported as an existing disk.

## Design Considerations

- **Verify every image's checksum before it enters the library.** An image
  becomes a running system; a corrupted or tampered image becomes a
  corrupted or compromised VM. Verify against the publisher's checksum.
- **Obtain licensed images only through your own entitlement.** CML through
  your Cisco license, RHEL through your Red Hat account, Windows through
  evaluation or your license. Do not source them from unofficial mirrors.
- **Keep the library organized and named clearly.** Nine images, some large,
  some similar (two RHEL profiles from one image); clear filenames prevent
  building a VM from the wrong image in Chapter 08.
- **Account for the appliance images' different workflow.** GNS3 and EVE-ng
  are imported, not installed; note which library entries are appliances so
  Chapter 08's procedure matches.
- **Mind the repository's capacity.** The Windows and CML images in
  particular are large; confirm `river`'s ISO repository has room for the
  full set.

## Implementation and Automation

### 1. Obtaining and verifying an ISO

The pattern for every downloadable image — shown for Ubuntu Server, applied
to each:

```bash
# Download from the official source (example URL shape).
curl -fLO https://releases.ubuntu.com/.../ubuntu-<ver>-live-server-amd64.iso

# Verify the checksum against the publisher's published value.
sha256sum ubuntu-<ver>-live-server-amd64.iso
# Compare to the SHA256SUMS the publisher provides; they must match.
```

For entitlement-gated images (RHEL, CML, Windows), download through the
vendor's authenticated portal rather than a direct URL, then verify the
checksum the vendor publishes the same way.

### 2. Placing ISOs in the `river` repository

Proxmox stores ISOs under the repository's `template/iso/` path:

```bash
# Copy a verified ISO into the river ISO repository.
cp ubuntu-<ver>-live-server-amd64.iso /mnt/river/template/iso/

# Or upload through the web UI: Storage (river-iso) > ISO Images > Upload,
# which places it in the same path and shows it in the VM creation dialog.

# Confirm the repository sees it.
pvesm list river-iso
```

### 3. Handling the appliance images

For GNS3 and EVE-ng, obtain the appliance image (GNS3 VM, EVE-ng OVA/ISO)
and note it for import in Chapter 08 rather than treating it as an installer:

```bash
# Appliance images may be OVA (import as a VM) or a qcow2/disk image.
# Place them where Chapter 08 can reference them; an OVA is imported with
# qm importovf / qm importdisk rather than booted as an installer ISO.
ls -lh /mnt/river/template/iso/ /mnt/river/images/ 2>/dev/null
```

## Validation and Troubleshooting

### Confirming the library is complete and sound

| Check | Expectation | Failure means |
| --- | --- | --- |
| All images present | Nine entries accounted for | A download or entitlement step incomplete |
| Checksums verified | Each matches the publisher's value | A corrupted or wrong download |
| ISOs visible in Proxmox | `pvesm list river-iso` shows them | Wrong path, or not in `template/iso/` |
| Appliances noted | GNS3/EVE-ng flagged as imports | Treating an appliance as an installer |
| Licensed images entitled | CML/RHEL/Windows sourced legitimately | Sourced from an unofficial mirror |

### The "CML isn't downloading for free" non-problem

If the plan was to download a free Cisco CML ISO and it cannot be found,
that is not a broken link — **CML is commercial and has no free download.**
The image comes from your Cisco entitlement. Recognizing this up front avoids
hunting for something that does not exist; the same is true, to a lesser
degree, for RHEL (needs an account, free though it is) and Windows (evaluation
or license).

### An appliance that will not "install"

If GNS3 or EVE-ng is treated as a plain installer ISO and booted, it will not
behave like an OS setup, because it is an appliance. The fix is to import it
as an existing disk/appliance in Chapter 08 rather than boot it as installer
media.

## Security and Best Practices

- **Only checksum-verified images enter the library.** This is the single
  most important control here: an unverified image is an unverified system.
- **Source licensed images through official, authenticated channels.**
  Unofficial mirrors of RHEL, CML, or Windows are a supply-chain risk and,
  for CML, a licensing violation.
- **Keep evaluation images' expiry in mind.** Windows evaluation ISOs are
  time-limited; a VM built from one will eventually expire, which is a lab
  consideration to plan around, not a fault.
- **Restrict who can add images to the repository.** The ISO library is the
  source of every VM; controlling what goes into it controls what can be
  built.

## References and Knowledge Checks

**References**

- [Volume XXI, Chapter 01](../../volume-21-ubuntu-server-cloud-26-04-lts/chapters/01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md)
  — Ubuntu installation media and options.
- [Volume XIV, Chapter 01](../../volume-14-red-hat-enterprise-linux-10/chapters/01-installation-subscriptions-repositories-and-cockpit.md)
  — RHEL installation and the developer-subscription route.
- [Proxmox VE storage documentation](https://pve.proxmox.com/wiki/Storage)
  — how the ISO repository presents media to VM creation.
- [Chapter 08](08-deploying-the-virtual-machines.md)
  — where each image becomes a running virtual machine.

**Knowledge checks**

1. Which of the nine images are free downloads, which need an account, and
   which is commercial with no free download?
2. What is the free, legitimate route for the two RHEL machines, and how many
   RHEL images does the build actually need?
3. Why can you not simply download a free Cisco CML ISO?
4. How do the GNS3 and EVE-ng images differ from the plain OS ISOs in how
   they are deployed?
5. Why is checksum verification the most important control in this chapter?

## Hands-On Lab

**Objective:** Assemble the nine-image library in the `river` ISO
repository, verifying each image and noting the appliances and the licensed
images.

**Prerequisites:** The ISO repository on `river` from
[Chapter 06](06-proxmox-storage-the-river-datastore-and-iso-repository.md),
and access to the appropriate download/entitlement sources.

**Reproducible to the extent your entitlements allow.** The free images are
fully reproducible; the licensed ones require your own CML, RHEL, and Windows
access.

**Procedure**

1. Download the free images (Ubuntu Desktop, Ubuntu Server, EVE-ng, GNS3)
   from their official sources and verify each checksum.
2. Obtain RHEL through your Red Hat account (developer subscription) and note
   that one image serves both the desktop and server machines.
3. Obtain the Windows 11 and Windows Server evaluation ISOs from Microsoft
   and verify them.
4. Obtain Cisco CML through your Cisco entitlement — recognizing there is no
   free download.
5. Place the installer ISOs in `river`'s `template/iso/` path, confirm
   `pvesm list river-iso` shows them, and note GNS3/EVE-ng as appliances to
   import in Chapter 08.

**Negative test**

6. Alter one byte of a downloaded ISO (a copy, not the original) and re-run
   its checksum; confirm it no longer matches the publisher's value —
   demonstrating that verification catches corruption before an image
   becomes a VM. Discard the altered copy.

**Expected results**

- All nine images accounted for, each obtained through a legitimate source.
- Every image checksum-verified.
- Installer ISOs visible in the `river-iso` repository; appliances noted for
  import.

**Cleanup**

7. Keep the verified library in place; Chapter 08 builds every VM from it.
   Remove any altered test copies from the negative test.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The ISO library on `river` is the source of every virtual machine, and this
chapter assembles it honestly: the images divide into free downloads (Ubuntu,
EVE-ng, GNS3), account-gated but free-for-labs RHEL (one image for both the
desktop and server machines, via the Red Hat Developer subscription),
evaluation Windows images, and commercial Cisco CML — which has no free
download and must come from your own entitlement. GNS3 and EVE-ng are
appliances that are imported rather than installed, unlike the plain OS
ISOs. The one non-negotiable control is checksum verification: an image
becomes a running system, so an unverified or tampered image becomes a
compromised VM. With a complete, verified library in the repository, the
build is ready to deploy the nine machines.

- [ ] All nine images obtained through legitimate sources.
- [ ] Every image checksum-verified against its publisher's value.
- [ ] Installer ISOs present in `river`'s `template/iso/` path.
- [ ] GNS3 and EVE-ng noted as appliance imports.
- [ ] CML, RHEL, and Windows sourced through proper entitlements.
