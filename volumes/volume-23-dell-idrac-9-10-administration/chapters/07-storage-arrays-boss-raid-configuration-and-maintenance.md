# Chapter 07: Storage Arrays, BOSS, RAID Configuration, and Maintenance

## Learning Objectives

- Explain how PERC RAID controllers and BOSS boot-optimized storage
  controllers are represented and managed through iDRAC.
- Create and delete virtual disks with an appropriate RAID level for a
  given workload, using RACADM and Redfish.
- Configure hot spares and explain automatic rebuild behavior after a
  drive failure.
- Distinguish RAID mode from HBA (non-RAID/pass-through) mode and identify
  when each is appropriate.
- Perform routine storage maintenance: proactive drive health monitoring,
  predictive failure response, and physical drive replacement procedure.

## Theory and Architecture

### PERC controllers and how iDRAC exposes them

The PowerEdge RAID Controller (PERC) family is Dell's storage controller
line, available as an add-in card or, on many current platforms, as an
integrated (motherboard-down) controller. Regardless of physical form,
PERC controllers are enumerated and managed through iDRAC's Storage
service — you do not need a separate management path or a controller-
specific BIOS utility for routine RAID administration, because Lifecycle
Controller and iDRAC's Redfish Storage resources expose full controller,
physical disk, and virtual disk management out-of-band, including before
any OS is installed.

Current-generation PERC controllers (the H755, H965i, and similar
families spanning the iDRAC9/iDRAC10 platform range; confirm the exact
controller matrix for a specific PowerEdge SKU against the platform's
technical guide) support the RAID levels covered later in this chapter,
NVMe and SAS/SATA drive mixing within platform-specific constraints, and
both RAID mode and HBA (pass-through) mode, selectable per controller.

### BOSS: Boot Optimized Storage Solution

BOSS is a dedicated, small-form-factor boot controller separate from the
main PERC controller — typically a pair of M.2 (BOSS-S1/S2, SATA-based)
or, on current platforms, NVMe (BOSS-N1) drives in a mirrored (RAID 1)
configuration dedicated specifically to hosting the boot OS. The design
intent is separation of concerns: boot storage on small, inexpensive,
mirrored drives independent of the larger data-serving RAID array on the
main PERC controller, so a data-volume RAID rebuild or reconfiguration
never risks the boot volume, and vice versa. BOSS is managed through the
same iDRAC Storage service as PERC, appearing as its own controller
instance with its own pair of physical disks and a single virtual disk.

### RAID levels and workload fit

| RAID Level | Redundancy | Usable Capacity | Typical Fit |
| --- | --- | --- | --- |
| RAID 0 | None | 100% of member disks | Scratch/temp data only; any single drive failure loses all data. |
| RAID 1 | Mirrors 2 disks | 50% | BOSS boot volumes; small, redundancy-critical volumes. |
| RAID 5 | Single-parity, distributed | (n-1)/n | Read-heavy workloads tolerating one drive failure; rebuild is I/O-intensive. |
| RAID 6 | Dual-parity, distributed | (n-2)/n | Larger arrays or environments wanting to tolerate a second failure during a long rebuild window. |
| RAID 10 | Mirrored stripe | 50% | Write-heavy, performance-sensitive workloads (databases) needing both redundancy and better write performance than RAID 5/6. |

Choosing among these is a workload and risk-tolerance decision, not a
purely technical one — RAID 5's rebuild-time exposure on very large,
high-utilization drives is a real operational risk that has pushed many
environments toward RAID 6 or RAID 10 as drive capacities have grown,
independent of iDRAC/PERC capability, which supports all of the levels
above.

### RAID mode vs. HBA mode

A PERC controller can operate in RAID mode (the controller presents
virtual disks to the OS, handling redundancy and caching itself) or HBA
mode (the controller presents physical disks directly to the OS with no
RAID abstraction, sometimes called pass-through or non-RAID mode). HBA
mode is the correct choice when the OS or an overlying platform provides
its own redundancy and storage management — software-defined storage
platforms, certain hyperconverged stacks, and some Linux software RAID or
ZFS deployments explicitly expect direct disk access rather than a
hardware RAID abstraction sitting between them and physical media.
Switching a controller's mode is disruptive (it typically requires
clearing existing virtual disk configuration) and should be decided as
part of initial platform design, not changed casually on a
production system with data already in place.

### Predictive failure and hot spares

iDRAC/PERC continuously evaluates drive SMART and controller-level health
telemetry and can flag a drive as predicted-to-fail before it actually
fails outright, based on manufacturer-defined thresholds. A **hot spare**
— a physical disk assigned to a controller (global) or a specific virtual
disk (dedicated) but not part of any array's active capacity — allows an
automatic rebuild to begin immediately upon a real or predicted failure,
without waiting for a technician to physically replace the failed drive
first. This meaningfully reduces the window of reduced redundancy after a
failure, at the cost of the spare drive's capacity sitting unused until
needed.

## Design Considerations

- **Separate boot and data storage architecturally, using BOSS where
  available.** Even on platforms without a BOSS card, consider a small,
  dedicated boot virtual disk distinct from the primary data array, for
  the same reason BOSS exists: isolating boot-volume risk from
  data-volume maintenance operations.
- **Choose RAID level by rebuild-time risk tolerance, not just capacity
  efficiency.** On very large drives, a RAID 5 array's single-parity
  exposure during a multi-hour (or longer) rebuild is a meaningful risk;
  weigh RAID 6 or RAID 10 for arrays where a second failure during
  rebuild would be unacceptable, even though both cost more usable
  capacity than RAID 5.
- **Decide hot spare policy (global vs. dedicated, and count) based on
  fleet-wide drive failure rates you actually observe, not assumption.**
  A single global hot spare covering multiple arrays on the same
  controller is efficient but only protects one concurrent failure across
  all of them; dedicated spares per critical array cost more capacity but
  provide independent protection.
- **Decide RAID vs. HBA mode as part of initial platform design,
  explicitly tied to what will manage redundancy.** Never leave this
  decision implicit — document which layer (hardware RAID vs. software/OS
  layer) is authoritative for redundancy on a given server, since mixing
  assumptions (an OS-level tool assuming HBA mode against a controller
  actually in RAID mode, or vice versa) produces confusing, hard-to-
  diagnose behavior.
- **Plan physical drive replacement procedure per your redundancy model.**
  A hot-spare-protected array tolerates a leisurely, scheduled physical
  swap since the rebuild already started automatically; an array with no
  spare needs an expedited replacement process to minimize the reduced-
  redundancy window, and that urgency difference should be reflected in
  your operational runbooks and alerting severity.

## Implementation and Automation

### Enumerating storage controllers and physical disks

```bash
racadm storage get controllers
racadm storage get pdisks -o -c RAID.Integrated.1-1
```

Over Redfish:

```bash
curl -s -k -u root:'<password>' \
  https://192.168.1.120/redfish/v1/Systems/System.Embedded.1/Storage \
  | python3 -m json.tool
```

### Creating a virtual disk (RAID 10 example)

```bash
racadm storage createvd:RAID.Integrated.1-1 \
  -rl r10 \
  -pdkey Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1,Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1,Disk.Bay.2:Enclosure.Internal.0-1:RAID.Integrated.1-1,Disk.Bay.3:Enclosure.Internal.0-1:RAID.Integrated.1-1 \
  -name data-vd01
```

Over Redfish, using Dell's OEM RAID service action (the standard Swordfish
`Volumes` POST is also supported for basic creation on current firmware;
the Dell OEM action exposes additional PERC-specific options such as
stripe size and disk cache policy):

```bash
curl -s -k -u root:'<password>' -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "TargetFQDD": "RAID.Integrated.1-1",
        "PDArray": [
          "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1",
          "Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1",
          "Disk.Bay.2:Enclosure.Internal.0-1:RAID.Integrated.1-1",
          "Disk.Bay.3:Enclosure.Internal.0-1:RAID.Integrated.1-1"
        ],
        "RAIDLevel": "RAID10",
        "VDPropMap": {"Name": "data-vd01"}
      }' \
  https://192.168.1.120/redfish/v1/Dell/Systems/System.Embedded.1/DellRaidService/Actions/DellRaidService.CreateVirtualDisk
```

This returns a job ID; the virtual disk is not usable until the job
completes:

```bash
racadm jobqueue view -i <job-id>
```

### Configuring a hot spare

```bash
racadm storage hotspare:Disk.Bay.4:Enclosure.Internal.0-1:RAID.Integrated.1-1 \
  -assign dedicated -vdkey Disk.Virtual.0:RAID.Integrated.1-1
```

### Deleting a virtual disk

```bash
racadm storage deletevd:Disk.Virtual.0:RAID.Integrated.1-1
```

Confirm no needed data remains on the target virtual disk before running
this — deletion is immediate and does not prompt for a secondary
confirmation at the RACADM layer the way some GUI workflows do.

### Switching a PERC controller to HBA mode

```bash
racadm storage set controller:RAID.Integrated.1-1 -mode HBA
```

Expect this to require an existing virtual disk configuration to be
cleared first, and expect the change to require a server reboot to take
effect; plan this as a scheduled maintenance action on any system with
existing data.

### Checking predictive failure status

```bash
racadm storage get pdisks -o -c RAID.Integrated.1-1 | grep -i "predictive\|status"
```

A Python script to poll storage health and flag any physical disk in a
degraded or predictive-failure state, suitable for a scheduled monitoring
job independent of whether alerting (Chapter 6) is also configured:

```python
#!/usr/bin/env python3
"""idrac_storage_health_check.py — poll all physical disks under a given
storage controller and flag any not in an Enabled/OK state.

Usage: python3 idrac_storage_health_check.py <idrac-ip> <username> <password>
"""
import sys
import requests

requests.packages.urllib3.disable_warnings()


def main() -> None:
    host, user, password = sys.argv[1], sys.argv[2], sys.argv[3]
    session = requests.Session()
    session.auth = (user, password)
    session.verify = False

    storage = session.get(
        f"https://{host}/redfish/v1/Systems/System.Embedded.1/Storage",
        timeout=30,
    )
    storage.raise_for_status()
    controllers = [m["@odata.id"] for m in storage.json().get("Members", [])]

    for controller_uri in controllers:
        detail = session.get(f"https://{host}{controller_uri}", timeout=30)
        detail.raise_for_status()
        drives = detail.json().get("Drives", [])
        for drive_ref in drives:
            drive = session.get(f"https://{host}{drive_ref['@odata.id']}", timeout=30)
            drive.raise_for_status()
            d = drive.json()
            health = d.get("Status", {}).get("Health")
            if health != "OK":
                print(f"ATTENTION: {d.get('Id')} on {controller_uri} health={health}")

    print("Storage health check complete.")


if __name__ == "__main__":
    main()
```

## Validation and Troubleshooting

- **Newly created virtual disk isn't visible to the OS.** Confirm the
  creation job actually completed (`racadm jobqueue view`) — a virtual
  disk in a pending/in-progress initialization state may not yet be
  presented to the OS, and on some configurations a host reboot is
  required for the OS to enumerate a newly created disk.
- **Automatic rebuild doesn't start after a drive failure despite a
  configured hot spare.** Confirm the spare is scoped correctly (global
  vs. dedicated to the specific affected virtual disk) and confirm the
  spare drive's capacity and type (SAS/SATA/NVMe) are compatible with the
  array it's meant to protect — an incompatible spare is silently
  ineligible rather than producing an obvious configuration error at
  assignment time on some firmware versions, so verify compatibility
  explicitly when assigning.
- **Predictive failure flag on a drive that seems to be performing
  normally.** Treat predictive failure as a leading indicator worth
  planning around, not a false positive to dismiss — manufacturer
  predictive-failure thresholds are deliberately conservative, and
  proactive replacement before outright failure is the intended response,
  not a wait-and-see approach.
- **HBA mode switch fails or is blocked.** Confirm all existing virtual
  disks on the controller have been deleted first (data loss risk — back
  up first) and confirm the controller model actually supports HBA mode,
  since not every PERC SKU does.
- **RAID 5/6 rebuild is taking far longer than expected.** This is
  expected behavior on large-capacity drives under load, not necessarily
  a fault — parity-based rebuilds are inherently I/O-intensive and scale
  with drive capacity; this is precisely the rebuild-time risk that
  should have informed the original RAID-level decision in Design
  Considerations.

## Security and Best Practices

- Require explicit confirmation and a documented change record before any
  virtual disk deletion or controller mode change — both are
  high-consequence, effectively irreversible-in-practice operations
  (data loss, in the case of deletion; a disruptive reconfiguration
  requiring OS-level adjustment, in the case of mode change).
- Monitor predictive failure and degraded-state alerts (Chapter 6)
  specifically for storage, and treat them as a higher operational
  priority than most other Warning-level events, given the compounding
  risk of a second failure during an active rebuild window.
- Physically label and track drive bay assignments during replacement, so
  a technician replacing a failed drive removes the correct physical unit
  — pulling the wrong drive from a degraded array can convert a
  single-drive failure into a data-loss event.
- Where System Erase (Chapter 4) includes storage-level secure erase,
  confirm it covers every physical disk intended for sanitization,
  including any drives outside the primary data array (BOSS boot drives
  in particular are easy to overlook in a decommissioning checklist
  focused on the "main" array).
- Document RAID level, hot spare policy, and RAID/HBA mode per server (or
  per platform standard) as part of your configuration baseline (SCP
  export, Chapter 2), so storage configuration is recoverable and
  auditable the same way network and identity configuration are.

## References and Knowledge Checks

**References**

- Dell Technologies, *iDRAC9/iDRAC10 User's Guide* — Storage Devices
  chapter
- Dell Technologies, *PERC Family Technical Guide*
- Dell Technologies, *iDRAC RACADM CLI Guide* — `storage` command
  reference
- Dell Technologies, *iDRAC Redfish API Guide* — `Storage`, `Volumes`, and
  `DellRaidService` OEM resources
- `SOFTWARE_VERSIONS.md` in this repository for the dated iDRAC9/iDRAC10
  baseline

**Knowledge Checks**

1. Why does BOSS exist as a separate controller from the main PERC array,
   rather than simply using a small virtual disk on the same controller?
2. What is the practical trade-off between RAID 5 and RAID 6 as drive
   capacities grow?
3. When is HBA mode the correct choice over RAID mode, and why is
   switching between them disruptive?
4. What is the operational value of a hot spare beyond simply having a
   replacement drive available in inventory?
5. Why should a predictive failure flag be treated as an action item
   rather than dismissed if the drive still appears to be functioning?

## Hands-On Lab

**Objective:** Enumerate storage controllers and physical disks, create
and delete a test virtual disk, and configure a hot spare — using lab
hardware or spare drives you are explicitly authorized to reconfigure,
since virtual disk creation/deletion is destructive to any data present.

**Prerequisites**

- The lab server configured in Chapters 1 through 6, with a PERC
  controller and at least four unused/spare physical disks (no existing
  data you need to preserve on them) or a virtual lab environment that
  simulates storage enumeration.
- **Safety note:** confirm explicitly, before running any command in this
  lab, that the physical disks or slots you target hold no data you need.
  Virtual disk creation and deletion are effectively irreversible for any
  existing data.
- An SSH client and Python 3.11+ with `requests` installed.

**Steps**

1. Enumerate available controllers and physical disks:

   ```bash
   racadm storage get controllers
   racadm storage get pdisks -o -c RAID.Integrated.1-1
   ```

   **Expected result:** a list of physical disk IDs, states (should show
   Ready or Online for available spares), and sizes.
2. Create a RAID 1 test virtual disk using two confirmed-spare disks:

   ```bash
   racadm storage createvd:RAID.Integrated.1-1 \
     -rl r1 \
     -pdkey Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1,Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1 \
     -name lab-test-vd
   ```

   **Expected result:** a job ID is returned; poll it with
   `racadm jobqueue view -i <job-id>` until it reports `Completed`.
3. Confirm the virtual disk exists and is healthy:

   ```bash
   racadm storage get vdisks -o -c RAID.Integrated.1-1
   ```

   **Expected result:** `lab-test-vd` appears with state `Ready`/`Online`
   and RAID level `RAID-1`.
4. Assign a third spare disk as a dedicated hot spare for the test virtual
   disk:

   ```bash
   racadm storage hotspare:Disk.Bay.2:Enclosure.Internal.0-1:RAID.Integrated.1-1 \
     -assign dedicated -vdkey Disk.Virtual.0:RAID.Integrated.1-1
   ```

   **Expected result:** the disk's role changes to `Dedicated Hot Spare`
   in subsequent `storage get pdisks` output.
5. Run the `idrac_storage_health_check.py` script from the Implementation
   and Automation section to confirm a clean bill of health:

   ```bash
   python3 idrac_storage_health_check.py <idrac-ip> root '<password>'
   ```

   **Expected result:** no drives are flagged, confirming a healthy
   baseline before the negative test.
6. **Negative test:** attempt to delete the virtual disk while
   deliberately referencing an incorrect (non-existent) disk identifier,
   to confirm the platform validates targets rather than silently
   accepting an invalid one:

   ```bash
   racadm storage deletevd:Disk.Virtual.99:RAID.Integrated.1-1
   ```

   **Expected result:** the command returns an error indicating the
   target does not exist, rather than succeeding or silently no-op'ing.
7. Delete the actual test virtual disk to complete the exercise:

   ```bash
   racadm storage deletevd:Disk.Virtual.0:RAID.Integrated.1-1
   ```

   **Expected result:** the job completes and `lab-test-vd` no longer
   appears in `storage get vdisks` output.

**Cleanup**

- Release the hot spare assignment if it persisted past the virtual disk
  deletion (`racadm storage get pdisks` to confirm current role; some
  firmware automatically releases a dedicated spare when its associated
  virtual disk is deleted, some do not).
- Confirm all disks used in this lab return to an unassigned/Ready state
  before considering the lab complete.

## Summary and Completion Checklist

This chapter covered iDRAC's role as the management plane for PERC and
BOSS storage controllers: RAID level selection against workload and
rebuild-risk trade-offs, the architectural rationale for BOSS as separate
boot storage, RAID mode versus HBA mode, hot spare configuration, and
predictive failure response. The lab exercised the full lifecycle of a
test virtual disk — creation, hot spare assignment, health validation, and
deletion — including a negative test confirming the platform validates
targets rather than accepting invalid ones silently.

- [ ] I can explain how BOSS relates architecturally to the main PERC
      array and why the separation exists.
- [ ] I can create and delete virtual disks with an appropriate RAID level
      for a given workload, using RACADM and Redfish.
- [ ] I can configure a hot spare and explain what automatic rebuild
      behavior it enables.
- [ ] I can explain when HBA mode is the correct choice over RAID mode.
- [ ] I validated storage health programmatically and understand how to
      respond to a predictive failure flag.
