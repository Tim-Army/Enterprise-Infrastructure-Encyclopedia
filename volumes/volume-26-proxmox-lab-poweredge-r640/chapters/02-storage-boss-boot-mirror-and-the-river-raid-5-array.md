# Chapter 02: Storage — The BOSS Boot Mirror and the `river` RAID 5 Array

## Learning Objectives

- Explain the two-tier storage design: a BOSS mirror for boot, a RAID 5
  array for data.
- Configure the BOSS card as a RAID 1 mirror across two 256 GB SSDs.
- Configure the six front drives as a RAID 5 array named `river`.
- Verify both virtual disks are healthy before installing an operating
  system.
- Understand the resilience and capacity trade-offs of each choice.

## Theory and Architecture

### Two tiers, two jobs

This build separates *where the operating system lives* from *where the
virtual machines live*, and uses different RAID for each:

- **BOSS (Boot Optimized Storage Solution)** — a small dedicated controller
  carrying two 256 GB SSDs in a **RAID 1 mirror**, holding only Proxmox VE
  itself. It keeps the boot device off the main data array, so the OS
  survives and boots independently of the workload storage.
- **`river`** — the **six front drives in a RAID 5 array**, holding virtual
  machine disks and the ISO library. This is the capacity tier, and RAID 5
  balances usable space against single-drive fault tolerance.

The separation is deliberate. Booting from the mirror means the OS is small,
mirrored, and independent; keeping VMs on the RAID 5 array means data
capacity scales with the front drives without touching the boot device.
This is the same boot/data separation the iDRAC volume describes for
PowerEdge generally
([Volume XXIII, Chapter 07](../../volume-23-dell-idrac-9-10-administration/chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md)),
applied here to one concrete build.

### Why RAID 1 for boot

The BOSS mirror holds one thing — the hypervisor — and its priority is
*survivability*, not capacity. RAID 1 writes the same data to both SSDs, so
either drive can fail and the system keeps booting. 256 GB is far more than
Proxmox needs, which is fine: the point of the mirror is resilience, not
size. If one SSD dies, the server keeps running on the other and the failed
drive is replaced without reinstalling.

### Why RAID 5 for `river`

The data array holds ten virtual machines and a library of ISO files, so
its priorities are *usable capacity with fault tolerance*. RAID 5 across six
drives gives the capacity of five drives (one drive's worth of space is
consumed by parity) and tolerates any single drive failing without data
loss — the array rebuilds onto a replacement.

The trade-offs SDSI-style design thinking would name:

- **Usable capacity** ≈ five drives out of six.
- **Fault tolerance** — one drive. A *second* failure during a rebuild loses
  the array, and rebuild time on large drives is not short, so RAID 5's
  single-failure tolerance is a real design limit, not a formality.
- **Write behavior** — RAID 5 pays a parity cost on writes; for a
  mixed-workload lab this is acceptable, but a write-heavy production array
  might prefer RAID 6 or RAID 10.

For a lab hosting mixed VMs, RAID 5 on six drives is a reasonable balance,
and it is what this build specifies. The name — `river` — is just the
array's label, used later when Proxmox references the storage.

## Design Considerations

- **Build the boot mirror and the data array as separate virtual disks.**
  The BOSS mirror and the `river` RAID 5 are on different controllers (the
  BOSS card and the PERC), which is exactly the separation that lets the OS
  boot independently of the data.
- **Confirm all drives are present and healthy before creating arrays.** A
  RAID 5 built while a drive is marginal starts life degraded. The iDRAC
  inventory from Chapter 01 should already show all eight drives; re-confirm
  before building.
- **Understand RAID 5's single-failure limit before relying on it.** It
  tolerates one drive; it does not tolerate a second failure during the
  rebuild window. For a lab this is acceptable, but it should be a conscious
  acceptance, and backups of anything irreplaceable belong off this array.
- **Note the rebuild-capacity reality.** After a drive replacement the array
  rebuilds, which takes time and load. Plan changes and heavy workloads
  around not being mid-rebuild where possible.

## Implementation and Automation

Both arrays are built through the iDRAC — either the Lifecycle Controller's
RAID configuration UI (from the virtual console) or RACADM.

### 1. The BOSS RAID 1 mirror

The BOSS card usually presents its own configuration. From the Lifecycle
Controller (F10 at boot) or the BOSS setup (Ctrl+key at POST for the
Marvell BOSS controller), create a **RAID 1** virtual disk across the two
256 GB SSDs. Via RACADM against the BOSS controller:

```bash
# Identify the BOSS controller and its two SSDs.
racadm -r 10.30.161.25 -u root -p <password> storage get controllers
racadm -r 10.30.161.25 -u root -p <password> storage get pdisks -o \
  -p Disk.Bay.0:Enclosure.Internal.0-1:AHCI.Slot.1-1   # example FQDD

# Create the RAID 1 mirror on the BOSS controller (FQDDs are examples;
# read the real ones from the commands above).
racadm -r 10.30.161.25 -u root -p <password> storage createvd \
  -c AHCI.Slot.1-1 -rl r1 \
  -pdkey <ssd1-fqdd>,<ssd2-fqdd>

# Apply the pending storage job and let it run at the next reboot.
racadm -r 10.30.161.25 -u root -p <password> jobqueue create AHCI.Slot.1-1 \
  -s TIME_NOW
```

### 2. The `river` RAID 5 array

On the PERC controller, create a **RAID 5** virtual disk across the six
front drives and name it `river`:

```bash
# The six front physical disks on the PERC.
racadm -r 10.30.161.25 -u root -p <password> storage get pdisks \
  -c RAID.Slot.1-1

# Create the RAID 5 virtual disk named "river" across all six.
racadm -r 10.30.161.25 -u root -p <password> storage createvd \
  -c RAID.Slot.1-1 -rl r5 -name river \
  -pdkey <d0>,<d1>,<d2>,<d3>,<d4>,<d5>

# Apply the storage job.
racadm -r 10.30.161.25 -u root -p <password> jobqueue create RAID.Slot.1-1 \
  -s TIME_NOW
```

The RAID 5 initialization runs in the background; the array is usable
during it but not yet fully redundant until initialization completes.

### 3. Confirming both virtual disks

```bash
# Both virtual disks should be listed and Online/Optimal.
racadm -r 10.30.161.25 -u root -p <password> storage get vdisks -o \
  -p Name,Status,RaidStatus,Size,Layout
```

The output should show the BOSS mirror (RAID 1) and `river` (RAID 5,
Optimal) with the expected sizes.

## Validation and Troubleshooting

### Confirming the arrays before install

| Check | Expectation | If wrong |
| --- | --- | --- |
| BOSS virtual disk | RAID 1, Online, ~256 GB usable | Re-check both SSDs are seen; recreate the mirror |
| `river` virtual disk | RAID 5, Optimal, ~5 drives usable | A drive missing or failed; replace and rebuild |
| Drive count on PERC | Six physical disks | A drive not seated or not spun up |
| Initialization | Completing or complete | Array usable but not yet fully redundant |

### The degraded-from-birth trap

The most consequential storage mistake is building the RAID 5 while one of
the six drives is marginal or not fully present. The array creates
successfully but starts *degraded* or fails its first initialization,
leaving no fault tolerance from day one. The guard is confirming all six
drives are present and healthy in the iDRAC inventory *before* creating the
array, and confirming the array reaches Optimal *after* — not assuming
"created" means "healthy."

### BOSS versus PERC confusion

BOSS and the PERC are different controllers, and the mirror and the RAID 5
live on different ones. A common confusion is trying to build the boot
mirror on the PERC or the data array on the BOSS. Confirm the controller
FQDD for each operation matches its intended role: BOSS for the boot
mirror, PERC for `river`.

## Security and Best Practices

- **Keep the boot device separate and mirrored.** Booting Proxmox from the
  BOSS RAID 1 means the hypervisor survives a boot-drive failure and can be
  recovered independently of the VM data.
- **Do not treat RAID 5 as a backup.** It tolerates a drive failure; it does
  not protect against deletion, corruption, or a second concurrent failure.
  Anything irreplaceable on `river` needs a real backup elsewhere — the same
  availability-is-not-backup point the storage volumes make.
- **Enable controller alerting.** The iDRAC can raise an alert on a drive
  predictive failure; catching a failing drive before it fails avoids
  entering a rebuild unexpectedly.
- **Record the array layout.** Note which physical bay maps to which array,
  so a drive replacement targets the right bay under pressure.

## References and Knowledge Checks

**References**

- [Volume XXIII, Chapter 07](../../volume-23-dell-idrac-9-10-administration/chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md)
  — BOSS, PERC, and RAID configuration in depth.
- [Volume VI, Chapter 02](../../volume-06-enterprise-storage-data-protection/chapters/02-block-storage-and-storage-area-networks.md)
  — RAID levels and their capacity/resilience trade-offs.
- [Dell BOSS documentation](https://www.dell.com/support/home/en-us/product-support/product/boss-controller/docs)
  — the boot-optimized storage controller.

**Knowledge checks**

1. Why does this build boot from a BOSS mirror rather than from the `river`
   array?
2. How much usable capacity does a six-drive RAID 5 provide, and where does
   the rest go?
3. What is RAID 5's fault-tolerance limit, and why does rebuild time make it
   a real design concern?
4. Which controller carries the boot mirror, and which carries `river`?
5. What must you confirm before *and* after creating the RAID 5 array, and
   why is "created" not the same as "healthy"?

## Hands-On Lab

**Objective:** Build the BOSS RAID 1 boot mirror and the six-drive RAID 5
array `river`, and confirm both are healthy before installing an OS.

**Prerequisites:** The R640 with iDRAC access from
[Chapter 01](01-idrac-out-of-band-access-and-first-configuration.md), the
two BOSS SSDs, and the six front drives, all visible in the inventory.

**This lab requires the physical server and its drives.** RAID
configuration is a hardware operation with no virtual substitute.

**Procedure**

1. From the iDRAC virtual console, enter the Lifecycle Controller (or BOSS
   setup) and create a RAID 1 mirror across the two 256 GB BOSS SSDs.
2. On the PERC, create a RAID 5 virtual disk across all six front drives and
   name it `river`.
3. Apply the storage jobs and let them run (a reboot may be required for the
   pending configuration).
4. After the jobs complete, confirm with `storage get vdisks` that the BOSS
   mirror is RAID 1 Online and `river` is RAID 5 Optimal, with the expected
   sizes.
5. Note which physical bay corresponds to which array member for future
   drive replacement.

**Negative test**

6. Before building `river`, if it is safe in your environment, remove and
   reseat one of the six front drives and observe the inventory reflect its
   absence, then presence. Confirm you would have caught a missing drive
   *before* building the array — the guard against a degraded-from-birth
   RAID 5. (Do not build the array with a drive absent.)

**Expected results**

- A BOSS RAID 1 mirror, Online, ready to receive the OS.
- A `river` RAID 5 array, Optimal, ready to hold VM storage.
- A recorded bay-to-array mapping.

**Cleanup**

7. The arrays are the foundation for every later chapter; leave them in
   place. Nothing to remove.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The build uses two storage tiers with different RAID because they have
different jobs: a BOSS RAID 1 mirror across two 256 GB SSDs holds only
Proxmox VE, prioritizing survivability so the hypervisor boots independently
of the data and survives a boot-drive failure; the six front drives form a
RAID 5 array named `river`, prioritizing usable capacity with single-drive
fault tolerance for the virtual machines and ISO library. RAID 5's tolerance
is one drive and not a second during rebuild, which is an acceptable but
conscious limit for a lab. Both arrays are built through the iDRAC, on their
respective controllers — BOSS for the mirror, PERC for `river` — and both
must reach a healthy state (Online, Optimal) before an operating system is
installed, because "created" is not "healthy."

- [ ] BOSS RAID 1 mirror built and Online.
- [ ] `river` RAID 5 array built across six drives and Optimal.
- [ ] Both virtual disks show the expected sizes.
- [ ] All six front drives confirmed present and healthy before building.
- [ ] Bay-to-array mapping recorded for future replacement.
