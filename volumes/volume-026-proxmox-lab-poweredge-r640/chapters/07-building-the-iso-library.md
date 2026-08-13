# Chapter 07: Building the ISO Library

## Learning Objectives

- Obtain each of the nine installation images this lab requires.
- Understand the licensing and entitlement reality of each image honestly.
- Place the ISOs into the `river` ISO repository correctly.
- Verify image integrity before an image becomes a running system.
- Distinguish plain ISO installs from appliance imports.

## Theory and Architecture

### The library and where it lives

The ten virtual machines in
[Chapter 08](08-deploying-the-virtual-machines.md) are built from the images
in the ISO repository created on `river` in
[Chapter 06](06-proxmox-storage-the-river-datastore-and-iso-repository.md).
This chapter assembles that library. The images fall into three groups by
how you obtain them, and being honest about that distinction matters — some
are free downloads, some need an account or entitlement, and one is
commercial and cannot be redistributed.

**Nine images serve ten machines.** As with the single RHEL image that
builds both Red Hat machines, the Ubuntu Server image builds two: the
`ubuntu-server1` VM and the `netbox` VM. NetBox Community Edition is a
Django web application with no operating-system ISO of its own — it is
installed onto a new Ubuntu Server guest, so it needs no tenth image. The
library therefore holds nine operating-system images, and NetBox is
deployed in [Chapter 08](08-deploying-the-virtual-machines.md) as an
application on top of the Ubuntu Server base.

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

**Host setup — deploying this image on your hypervisor.** The create/import and interface-mapping steps are the same for every appliance and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

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

- [Volume XXI, Chapter 01](../../volume-021-ubuntu-server-cloud-26-04-lts/chapters/01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md)
  — Ubuntu installation media and options.
- [Volume XIV, Chapter 01](../../volume-014-red-hat-enterprise-linux-10/chapters/01-installation-subscriptions-repositories-and-cockpit.md)
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

This chapter carries a topic-level walkthrough lab for **each step of building the ISO/image
library** — downloading install media, verifying integrity, listing it in Proxmox, and preparing
cloud images for templates. Commands are runnable. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 7.1–7.4** — a Proxmox node with the `riverfiles` (iso-content)
storage from Chapter 06, internet access, and root SSH. **Cost:** none.

### Lab 7.1 — Download install ISOs (Topic: Install media)

**Objective:** Populate the ISO storage.

```bash
cd /river/template/iso
wget -q https://releases.ubuntu.com/24.04/ubuntu-24.04-live-server-amd64.iso
# (Proxmox GUI: Datacenter > riverfiles > ISO Images > Download from URL does the same.)
pvesm list riverfiles --content iso
```

**Expected result:** the ISO lands in the `iso`-content storage and appears in `pvesm list` — the
ISO library holds the OS install media the VMs boot from; storing it on the `river` array's directory
storage keeps it available to every VM without re-downloading.

**Negative test:** point a VM at an ISO that is not in an `iso`-content storage; Proxmox will not
offer it as a CD/DVD source — install media must live in an `iso`-capable storage.

**Rollback:** remove unused ISOs to reclaim space.

### Lab 7.2 — Verify ISO integrity (Topic: Integrity)

**Objective:** Confirm the download is authentic and complete.

```bash
cd /river/template/iso
sha256sum ubuntu-24.04-live-server-amd64.iso
# Compare to the publisher's SHA256SUMS (and verify its GPG signature for authenticity):
# wget -q https://releases.ubuntu.com/24.04/SHA256SUMS && grep live-server SHA256SUMS
```

**Expected result:** the ISO's SHA-256 matches the publisher's published value — verifying the hash
(and ideally the signed SHASUMS file) confirms the media is complete and unaltered before you build
ten VMs from it; a corrupt ISO causes install failures that look like hardware faults.

**Negative test:** install from an ISO whose hash you never checked; a truncated or tampered image
fails partway or installs compromised software — verifying integrity first rules that out.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — List and manage the library (Topic: Library management)

**Objective:** Inventory the available media.

```bash
pvesm list riverfiles
pvesm list riverfiles --content iso | awk '{print $1, $4}'    # volid + size
```

**Expected result:** a listed inventory of ISOs (and later container templates/backups) with their
volume IDs and sizes — `pvesm list` gives the authoritative inventory of what a storage holds, and
the volid (`riverfiles:iso/ubuntu-24.04...iso`) is how VMs reference the media.

**Negative test:** reference an ISO by a guessed path instead of its Proxmox volid; the VM config is
invalid — Proxmox addresses media by `storage:content/name` volid, which `pvesm list` gives you.

**Rollback:** none (read-only).

### Lab 7.4 — Cloud images for templates (Topic: Cloud images)

**Objective:** Stage a cloud image for fast VM cloning.

```bash
cd /river/template/cache
wget -q https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
# This qcow2 cloud image becomes a cloud-init template in Chapter 08 (imported as a VM disk).
ls -lh noble-server-cloudimg-amd64.img
```

**Expected result:** a downloaded Ubuntu cloud image (qcow2) ready to import — cloud images are
pre-installed, cloud-init-ready disk images, so instead of running the installer for each of the ten
VMs, you import one cloud image, make it a template, and clone it (Chapter 08), which is far faster
and consistent.

**Negative test:** install all ten VMs from the full ISO one by one; it is slow and inconsistent — a
cloud-init template cloned ten times is the efficient, repeatable approach.

**Rollback:** none (the image is used in Chapter 08).

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
build is ready to deploy the ten machines.

- [ ] All nine images obtained through legitimate sources.
- [ ] Every image checksum-verified against its publisher's value.
- [ ] Installer ISOs present in `river`'s `template/iso/` path.
- [ ] GNS3 and EVE-ng noted as appliance imports.
- [ ] CML, RHEL, and Windows sourced through proper entitlements.
