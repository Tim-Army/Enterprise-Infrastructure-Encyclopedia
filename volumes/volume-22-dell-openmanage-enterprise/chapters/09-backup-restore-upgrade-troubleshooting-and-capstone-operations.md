# Chapter 09: Backup, Restore, Upgrade, Troubleshooting, and Capstone Operations

## Learning Objectives

- Explain OME's appliance-level backup and restore model and how it
  differs from backing up the devices OME manages.
- Plan and execute an appliance upgrade with an appropriate pre-upgrade
  checklist and rollback posture.
- Collect and interpret appliance diagnostic bundles for support
  escalation and self-directed troubleshooting.
- Recognize common failure patterns that span multiple subsystems covered
  earlier in this volume, and know which chapter's diagnostic approach
  applies.
- Execute a capstone exercise that exercises discovery, monitoring,
  firmware compliance, templates, and backup together as a single
  operational workflow, consistent with how these subsystems interact in
  a real environment.

## Theory and Architecture

### What an appliance backup protects

Chapter 1 established that OME's entire management plane — device
inventory, job history, alert policies, templates, discovery credential
profiles, user accounts, and configuration — lives inside one appliance's
embedded database. An **appliance backup** captures this application
state so it can be restored onto a newly deployed appliance instance,
distinct in every respect from backing up the *managed devices'* own
data, which is entirely out of scope for OME and is covered by each
platform's own backup tooling (Volume VI for storage and data
protection patterns generally). Losing the OME appliance without a
current backup does not lose any data on the managed fleet itself — it
loses the fleet-management configuration and history that took time to
build: discovery credentials, curated groups, alert policies, templates,
and accumulated job/alert history.

### Backup mechanism

OME's supported backup path exports appliance application data to a
network-accessible location (a CIFS or NFS share is the typical target)
as a versioned backup file, triggered on demand or on a schedule from the
console's application settings. This is distinct from — and a better
practice than relying solely on — a hypervisor-level VM snapshot: a
snapshot captures disk state at a point in time and is useful for rapid
rollback during upgrade testing, but an application-level backup is the
supported, version-portable mechanism recommended for disaster recovery
and appliance-to-appliance migration, and is what Dell support expects
when assisting with a restore.

### Restore mechanism

Restoring an appliance backup is performed during the deployment of a
**new** appliance instance: rather than the first-run setup wizard from
Chapter 1, a freshly deployed appliance offers a restore path that
consumes a prior backup file from the same network location, bringing the
new instance up with the prior appliance's application state rather than
an empty one. This is why appliance backup and restore are covered
together with upgrade in this chapter — both are "replace or move the
appliance while preserving its state" operations, just triggered by
different circumstances (planned upgrade vs. unplanned recovery vs.
appliance migration).

### Upgrade model

OME appliance upgrades are applied as a version-to-version update package,
either retrieved automatically (if the appliance has connectivity to
Dell's update-check endpoint, conceptually parallel to Chapter 6's
connected catalog dependency) or uploaded manually to the appliance
(conceptually parallel to Chapter 7's offline model, for disconnected
environments). Upgrades are applied in place to the running appliance
instance rather than requiring a fresh deployment, but carry the same
general precautions as any infrastructure management-plane upgrade:
version-to-version compatibility constraints (not every upgrade path
skips versions freely), plugin compatibility (an installed plugin, such
as Power Manager, must support the target OME version), and a
maintenance window, since the appliance's console and API are unavailable
for the duration of the upgrade itself.

### Diagnostics and support bundles

The appliance's application settings include a diagnostics/log export
function producing a bundle suitable for Dell support escalation,
referenced already in Chapter 1's troubleshooting guidance. This bundle
aggregates appliance logs, configuration state, and recent job/error
history into a single artifact, and is the standard first request from
Dell support when engaging on an appliance-level issue — collecting it
promptly, while a failure state is still current, produces more useful
diagnostic data than collecting it after a remediation attempt has
already changed appliance state.

## Design Considerations

- **Backup schedule vs. change cadence.** Align backup frequency to how
  often meaningful appliance state actually changes — a fleet with
  frequent template edits, alert policy changes, or user/role changes
  warrants more frequent backups than a stable, slow-changing
  environment. A daily or weekly scheduled backup is a reasonable
  starting point for most production appliances.
- **Backup storage location resilience.** The network share holding
  appliance backups is itself a critical dependency for disaster
  recovery; ensure it has its own backup/redundancy posture and is not
  co-located exclusively on infrastructure that a single failure domain
  could take out alongside the appliance itself.
- **Snapshot vs. application backup, used together deliberately.** A
  pre-upgrade VM snapshot is a reasonable fast-rollback safety net for
  the upgrade window specifically; it should complement, not replace, a
  current application-level backup intended for longer-term disaster
  recovery and appliance migration.
- **Upgrade path validation.** Confirm supported upgrade paths (which
  source versions can upgrade directly to your target version, and which
  require an intermediate hop) against Dell's current release notes
  before planning an upgrade, particularly for appliances that have been
  running an older version for an extended period.
- **Plugin and integration compatibility.** Before upgrading, confirm
  every installed plugin (Power Manager, SupportAssist integration) and
  every external integration (Chapter 4's SIEM/SMTP forwarding, Chapter
  8's IaC-adjacent automation) is validated against the target version,
  not only the base console functionality.
- **Recovery time objective.** Decide, as an explicit organizational
  decision rather than an afterthought, how long your organization can
  operate without OME console/API access during an unplanned outage
  before a restore-to-new-appliance process must begin — this drives how
  current your backups need to be and how rehearsed your restore process
  needs to be before it is actually needed.

## Implementation and Automation

### Triggering an on-demand appliance backup (console-driven)

Appliance backup is primarily a console-driven and scheduled operation
rather than a heavily used REST API surface in most OME releases; from
application settings, configure the backup destination (network share
path and credentials) and either trigger an immediate backup or define a
recurring schedule. Where your build exposes a corresponding API
resource, the same session-token authentication pattern used throughout
this volume applies — confirm the exact resource path against your
appliance's live API reference, since appliance-lifecycle operations
(backup, restore, upgrade) have historically had narrower API coverage
than device-management operations like discovery, templates, and
firmware.

### Scripting a pre-backup health baseline

While backup triggering itself is console-driven, scripting a health and
inventory snapshot immediately before a backup (or before an upgrade) is
good practice and fully achievable through the API patterns already
established in this volume:

```python
#!/usr/bin/env python3
"""ome_pre_change_snapshot.py — capture a point-in-time operational
snapshot (device counts by health status, active alert counts, job
queue state) before a backup or upgrade, for before/after comparison.

Usage: python3 ome_pre_change_snapshot.py <ome-host> <user> <password>
"""
import sys
import json
import requests

requests.packages.urllib3.disable_warnings()


def get_session(host, user, password):
    session = requests.Session()
    resp = session.post(
        f"https://{host}/api/SessionService/Sessions",
        json={"UserName": user, "Password": password, "SessionType": "API"},
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()
    session.headers.update({"X-Auth-Token": resp.headers["X-Auth-Token"]})
    return session


def get_all_pages(session, host, resource_path):
    results = []
    url = f"https://{host}/api/{resource_path}"
    while url:
        resp = session.get(url, verify=False)
        resp.raise_for_status()
        payload = resp.json()
        results.extend(payload.get("value", []))
        next_link = payload.get("@odata.nextLink")
        url = f"https://{host}{next_link}" if next_link else None
    return results


def main():
    host, user, password = sys.argv[1:4]
    session = get_session(host, user, password)

    devices = get_all_pages(session, host, "DeviceService/Devices")
    alerts = get_all_pages(session, host, "AlertService/Alerts")
    jobs = get_all_pages(session, host, "JobService/Jobs")

    health_counts = {}
    for d in devices:
        status = d.get("Status", "Unknown")
        health_counts[status] = health_counts.get(status, 0) + 1

    snapshot = {
        "device_count": len(devices),
        "device_health_counts": health_counts,
        "active_alert_count": len(alerts),
        "job_count": len(jobs),
    }
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
```

Run this script (redirecting output to a timestamped file) immediately
before a scheduled backup or an upgrade window, and again immediately
after, as a fast, scriptable sanity check that the appliance's managed
population and health picture are consistent across the operation —
distinct from, and complementary to, a full restore test.

### Collecting a diagnostics/support bundle

```bash
# Diagnostics export is triggered from Application Settings in the
# console; where an API resource is exposed for it in your build,
# it follows the same job-based pattern as other long-running operations.
curl -sk -X POST "https://<appliance>/api/ApplicationService/Actions/ApplicationService.ExportDebugLogs" \
  -H "X-Auth-Token: <token>" -H "Content-Type: application/json" -d '{}'
```

Confirm the exact resource name for your build; if no API path is exposed
for diagnostics export in your release, use the console's application
settings diagnostics screen directly.

### Checking for and applying an available upgrade

```bash
# Check current appliance version and available update status.
curl -sk https://<appliance>/api/ApplicationService/Info \
  -H "X-Auth-Token: <token>"
```

Applying the upgrade itself — whether retrieved automatically or uploaded
manually as an offline package — is a console-driven workflow given its
disruptive, all-or-nothing nature; scripting the *decision* of whether an
upgrade is available (as shown above) is reasonable, but triggering the
actual upgrade through unattended automation is not a common or
recommended pattern given the value of a human confirming maintenance
window timing immediately before initiating it.

## Validation and Troubleshooting

- **Backup job fails to reach its destination share.** Verify network
  reachability and credential validity to the backup share independently
  of the backup feature itself, the same "validate the dependency first"
  principle used for catalog connectivity in Chapters 6 and 7.
- **Restore during new-appliance deployment fails to find the backup
  file.** Confirm the new appliance instance has network access to the
  exact same share path used during backup, and that the backup file was
  not partially written (check its completion status against the backup
  job history on the original appliance before treating a file as
  restorable).
- **Upgrade fails partway through.** Do not attempt to force a retry
  immediately; collect a diagnostics bundle first (state is most useful
  while still current), and restore from the pre-upgrade snapshot
  (VM-level or application-level, per your design choice above) rather
  than attempting ad hoc in-place remediation of a partially upgraded
  appliance, which is not a supported state.
- **Post-upgrade, a plugin stops functioning.** Check plugin-to-appliance
  version compatibility first (Design Considerations, above); this is a
  more common cause than an upgrade defect and is usually resolved by
  upgrading the plugin itself to a compatible version.
- **A problem spans multiple subsystems and it's unclear where to start.**
  Use this volume's chapter structure as a triage map: authentication or
  permission symptoms point to Chapter 2; a device missing or showing
  stale data points to Chapter 3; an alert not arriving points to Chapter
  4; firmware compliance or update issues point to Chapters 5–7; a
  configuration drift or deployment issue points to Chapter 8; and an
  appliance-wide symptom affecting every function simultaneously points
  back to this chapter's backup/restore/upgrade and diagnostics guidance.

## Security and Best Practices

- Encrypt or otherwise protect the network share holding appliance
  backups — a backup file contains discovery credentials, user account
  metadata, and configuration templates, making it as sensitive as the
  appliance itself and a high-value target if exposed.
- Restrict who can trigger a restore or initiate an appliance upgrade
  through role and scope (Chapter 2); both are high-impact, disruptive
  operations that warrant tight access control distinct from routine
  device-management rights.
- Test the restore path periodically, not only the backup path — a backup
  process that has never been proven to actually restore successfully is
  an unverified assumption, not a working disaster recovery capability.
- Apply appliance upgrades on a defined cadence aligned with your
  organization's patch management program (Volume I, Chapter 8), rather
  than deferring indefinitely; OME itself is internet-adjacent
  infrastructure software with an ongoing need for security patching.
- Retain diagnostic bundles only as long as needed for the active support
  case or investigation, and handle them with the same care as other
  artifacts containing configuration and credential-adjacent metadata.
- Document and rehearse your restore-to-new-appliance runbook before it
  is needed under incident pressure — this is a capability best validated
  in a planned exercise, not for the first time during an actual
  disaster.

## References and Knowledge Checks

**References**

- Dell Technologies, *OpenManage Enterprise User's Guide* — backup,
  restore, and appliance upgrade
- Dell Technologies, *OpenManage Enterprise Release Notes* (version-
  specific, for supported upgrade paths)
- Dell Technologies, *OpenManage Enterprise RESTful API Guide*
- `SOFTWARE_VERSIONS.md` in this repository for the dated 4.7.x baseline

**Knowledge Checks**

1. Why does an OME appliance backup not protect any data residing on the
   managed device fleet itself?
2. Why is an application-level backup recommended as the primary
   disaster-recovery mechanism rather than relying solely on a
   hypervisor-level VM snapshot?
3. Why should a diagnostics bundle be collected before attempting
   remediation of a failure, rather than after?
4. Why is triggering an appliance upgrade itself a poor candidate for
   fully unattended automation, even though checking for upgrade
   availability is reasonable to automate?
5. Using this chapter's triage map, which earlier chapter's diagnostic
   approach applies to a device showing stale inventory data, and which
   applies to a missing alert notification?

## Hands-On Lab

**Objective:** Perform a capstone exercise that exercises discovery,
monitoring, firmware compliance, and appliance operational hygiene
together as a single scripted workflow, producing a before/after
operational snapshot consistent with a real pre-change validation
practice — and separately walk through the appliance backup
configuration screens to establish (without requiring a second appliance
for a full restore test) a validated backup destination.

**Prerequisites**

- The OME appliance and lab devices established across this volume's
  earlier chapters (the SNMP-discovered Linux lab host from Chapter 3 at
  minimum; a real or virtual iDRAC-managed device if you completed the
  optional hardware-dependent portions of Chapters 5 and 8).
- A network share (a lab NFS or CIFS export is sufficient — a single
  lab-purpose Linux host running an NFS export works well) reachable from
  the OME appliance, to serve as the backup destination.
- Python 3.11+ with `requests` installed.

**Steps**

1. Configure a lab NFS export to serve as the backup destination target,
   for example on a lab Linux host:

   ```bash
   sudo mkdir -p /srv/ome-backup
   echo "/srv/ome-backup <ome-appliance-ip>(rw,sync,no_subtree_check,no_root_squash)" \
     | sudo tee -a /etc/exports
   sudo exportfs -ra
   ```

   **Expected result:** `showmount -e <lab-host-ip>` run from another
   host shows `/srv/ome-backup` exported to the appliance's address.
2. In the OME console's application settings, configure the backup
   destination to point at this share, and confirm the appliance reports
   the share as reachable (a connectivity validation step is typically
   part of this configuration screen).
3. Trigger an on-demand backup and monitor it to completion in the
   console.
4. **Expected result:** a backup file appears in `/srv/ome-backup` on the
   lab host after the job completes:

   ```bash
   ls -lh /srv/ome-backup
   ```

5. Run the `ome_pre_change_snapshot.py` script from Implementation and
   Automation and save its output:

   ```bash
   python3 ome_pre_change_snapshot.py <appliance-ip> admin '<password>' \
     > pre-change-snapshot.json
   ```

6. Exercise a representative cross-chapter operational sequence: force an
   inventory refresh on your lab device(s) (Chapter 3), confirm no new
   unexpected alerts appear in the alert log (Chapter 4), and if you
   completed Chapter 5's optional hardware-dependent steps, re-run
   compliance evaluation on `lab-firmware-baseline`.
7. Run the snapshot script again and compare:

   ```bash
   python3 ome_pre_change_snapshot.py <appliance-ip> admin '<password>' \
     > post-change-snapshot.json
   diff pre-change-snapshot.json post-change-snapshot.json
   ```

   **Expected result:** the diff shows only the changes attributable to
   the operations performed in step 6 (for example, an updated job
   count), with no unexplained changes in device health counts —
   confirming the operational sequence behaved as expected.
8. **Negative test:** attempt to authenticate the snapshot script with an
   intentionally invalid password:

   ```bash
   python3 ome_pre_change_snapshot.py <appliance-ip> admin 'WrongPassword123!'
   ```

   **Expected result:** the script fails with an HTTP error from the
   session endpoint, consistent with Chapter 1's original bootstrap
   validation lab, confirming this final capstone script correctly
   depends on the same authentication discipline established at the very
   start of the volume.

**Cleanup**

- Remove the on-demand backup file from the lab share if it is not
  needed further, and remove the NFS export from the lab host:

  ```bash
  sudo sed -i '\|/srv/ome-backup|d' /etc/exports
  sudo exportfs -ra
  ```

- Remove the snapshot JSON files from your workstation if not needed for
  reference:

  ```bash
  rm -f pre-change-snapshot.json post-change-snapshot.json
  ```

- If any lab devices, groups, baselines, templates, or alert policies
  created across this volume's chapters are no longer needed, remove them
  from the appliance to leave it in a clean state, or retain the
  appliance as a standing lab environment for further study at your
  discretion.

## Summary and Completion Checklist

This chapter closed the volume by covering how to protect the OME
appliance itself: the distinction between appliance-level backup and
device-level data protection, the backup-and-restore-to-new-instance
model, upgrade planning and its connected/offline parallels to Chapters 6
and 7, and diagnostics collection for support escalation. The capstone
lab tied the volume together operationally — configuring a real backup
destination, exercising a representative cross-chapter workflow, and
validating it with a scripted before/after snapshot, closing with the
same authentication negative-test discipline the volume opened with in
Chapter 1. Across all nine chapters, this volume established Dell
OpenManage Enterprise's architecture, identity and access model, device
lifecycle from discovery through decommission-adjacent operations,
monitoring and alerting, firmware and configuration lifecycle management
across both connected and air-gapped environments, and the appliance
operational hygiene needed to run it as production infrastructure rather
than a one-time deployment.

- [ ] I can explain what an appliance backup protects and what it
      explicitly does not protect.
- [ ] I configured a real backup destination and completed an on-demand
      backup.
- [ ] I can describe the pre-upgrade checklist items — version path,
      plugin compatibility, and maintenance window — before planning an
      appliance upgrade.
- [ ] I ran a scripted before/after operational snapshot around a
      representative change, including a negative authentication test.
- [ ] I can use this chapter's cross-chapter triage map to route a given
      symptom to the correct earlier chapter's diagnostic approach.
