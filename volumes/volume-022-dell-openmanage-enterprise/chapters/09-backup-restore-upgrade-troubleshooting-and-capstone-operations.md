# Chapter 09: Backup, Restore, Upgrade, Troubleshooting, and Capstone Operations

![Flow diagram showing an on-demand backup to a validated NFS share and a pre/post-change operational snapshot diff confirming only expected changes across a cross-chapter operational sequence, alongside the same snapshot script failing on an intentionally invalid password.](../../../diagrams/volume-022-dell-openmanage-enterprise/chapter-09-capstone-backup-snapshot-flow.svg)

*Figure 9-1. The capstone backup and operational snapshot flow exercised in this chapter's lab, including the invalid-credentials negative test.*

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

[Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md) established that OME's entire management plane — device
inventory, job history, alert policies, templates, discovery credential
profiles, user accounts, and configuration — lives inside one appliance's
embedded database. An **appliance backup** captures this application
state so it can be restored onto a newly deployed appliance instance,
distinct in every respect from backing up the *managed devices'* own
data, which is entirely out of scope for OME and is covered by each
platform's own backup tooling ([Volume VI](../../volume-006-enterprise-storage-data-protection/README.md) for storage and data
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
[Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md), a freshly deployed appliance offers a restore path that
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
Dell's update-check endpoint, conceptually parallel to [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s
connected catalog dependency) or uploaded manually to the appliance
(conceptually parallel to [Chapter 7](07-isolated-offline-repositories-and-air-gapped-updates.md)'s offline model, for disconnected
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
referenced already in [Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)'s troubleshooting guidance. This bundle
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
  every external integration ([Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md)'s SIEM/SMTP forwarding, Chapter
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
  permission symptoms point to [Chapter 2](02-identity-licensing-security-and-administrative-control.md); a device missing or showing
  stale data points to [Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md); an alert not arriving points to Chapter
  4; firmware compliance or update issues point to Chapters 5–7; a
  configuration drift or deployment issue points to [Chapter 8](08-templates-configuration-compliance-automation-and-apis.md); and an
  appliance-wide symptom affecting every function simultaneously points
  back to this chapter's backup/restore/upgrade and diagnostics guidance.

## Security and Best Practices

- Encrypt or otherwise protect the network share holding appliance
  backups — a backup file contains discovery credentials, user account
  metadata, and configuration templates, making it as sensitive as the
  appliance itself and a high-value target if exposed.
- Restrict who can trigger a restore or initiate an appliance upgrade
  through role and scope ([Chapter 2](02-identity-licensing-security-and-administrative-control.md)); both are high-impact, disruptive
  operations that warrant tight access control distinct from routine
  device-management rights.
- Test the restore path periodically, not only the backup path — a backup
  process that has never been proven to actually restore successfully is
  an unverified assumption, not a working disaster recovery capability.
- Apply appliance upgrades on a defined cadence aligned with your
  organization's patch management program ([Volume I, Chapter 8](../../volume-001-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md)), rather
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

- [Dell Technologies, *OpenManage Enterprise User's Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4_5_online_help_user_guide/overview) — backup,
  restore, and appliance upgrade
- [Dell Technologies, *OpenManage Enterprise Release Notes* (version-
  specific, for supported upgrade paths)](https://www.dell.com/support/home/en-us/product-support/product/dell-openmanage-enterprise/drivers)
- [Dell Technologies, *OpenManage Enterprise RESTful API Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_p_3.10_api_guide/preface)
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated 4.7.x baseline

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

This chapter closes the volume with **appliance lifecycle and troubleshooting** — the
"Troubleshooting" domain — and a **Design Exercise** capstone synthesizing OME fleet management.
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.4** — a deployed OME appliance with devices onboarded, a
backup share, and API credentials. **Cost:** none.

### Lab 9.1 — Appliance backup and restore (Topic: Backup and restore)

**Objective:** Protect the appliance's configuration and data.

```text
# Console: Application Settings > Console and Extensions / Backup.
#   Configure a scheduled backup to a network share (config + database).
#   Then validate recoverability by restoring to a fresh appliance in a lab and confirming
#   devices, groups, baselines, and users return.
```

**Expected result:** a scheduled backup lands on the share, and a test restore brings back devices,
groups, baselines, and users — the OME database holds all onboarding, grouping, baseline, and
policy state, so a tested backup/restore is the appliance's disaster-recovery guarantee.

**Negative test:** run OME with no backups; losing the appliance means re-discovering the entire
fleet and rebuilding every group, baseline, and policy by hand — the backup preserves all that
state.

**Cleanup:** remove the lab restore appliance if created only for the test.

### Lab 9.2 — Appliance upgrade (Topic: Lifecycle)

**Objective:** Upgrade OME safely.

```bash
curl -sk -H "X-Auth-Token: $TOKEN" https://<ome-ip>/api/ApplicationService/Version | \
  python3 -c "import json,sys; print('current:', json.load(sys.stdin).get('Version'))"
# Console: Application Settings > Console and Extensions > Update Console.
#   Take a backup first (Lab 9.1), review the release notes/compatibility, then apply the update.
```

**Expected result:** OME reports its version and upgrades to the target from an online or uploaded
package, backup-first — appliance upgrades follow the supported path (backup → check release notes
→ update console), and a pre-upgrade backup is the rollback if an upgrade misbehaves.

**Negative test:** upgrade with no backup and no release-note review; if the upgrade fails or a
plugin is incompatible, there is no clean rollback — the pre-upgrade backup is what makes the
change reversible.

**Cleanup:** none.

### Lab 9.3 — Structured troubleshooting (Topic: Troubleshooting)

**Objective:** Diagnose a common failure by layer.

```bash
# A discovery/update failure: work from credentials -> connectivity -> job logs.
curl -sk -H "X-Auth-Token: $TOKEN" "https://<ome-ip>/api/JobService/Jobs?\$filter=LastRunStatus/Name eq 'Failed'" 2>/dev/null | \
  python3 -c "import json,sys; [print(j['JobName'], j['Id']) for j in json.load(sys.stdin)['value'][:5]]"
# Then fetch the failed job's execution detail for the root cause:
curl -sk -H "X-Auth-Token: $TOKEN" "https://<ome-ip>/api/JobService/Jobs(<Id>)/ExecutionHistories" 2>/dev/null | head
# Console: Monitor > Jobs > failed job > view execution details / download appliance logs
```

**Expected result:** the failed job and its execution detail point to the cause (bad credential,
unreachable iDRAC, protocol mismatch) — structured troubleshooting works the layers in order
(credentials → network/protocol → job execution log), and OME's job execution history is where the
specific error lives.

**Negative test:** re-run a failing discovery repeatedly without reading the job's execution log;
you repeat the same failure — the execution detail names the cause (e.g. "invalid credentials"),
which guessing does not.

**Cleanup:** none (read-only).

### Lab 9.4 — Capstone Design Exercise: OME fleet management (Topic: Synthesis)

**Objective:** Produce a defensible OME operations design — the deliverable, not a click-path.

> **Scenario.** Manage 800 PowerEdge servers across two data centers (one internet-connected, one
> air-gapped) plus regional edge sites: consistent configuration, current firmware, proactive
> monitoring, delegated operations, and disaster recovery.

Work through and **write down**:

1. **Deploy & scope** — appliance placement/sizing and HA considerations; static/reserved
   addressing (Ch01).
2. **Identity & delegation** — directory-integrated RBAC with roles + group scope, TLS, and
   licensing tiers for template/compliance features (Ch02).
3. **Onboard & organize** — discovery protocols per class, credential profiles, and **dynamic
   groups** that keep membership current (Ch03).
4. **Firmware currency** — online catalog + scheduled refresh for the connected DC (Ch06), and the
   DRM offline pipeline for the air-gapped DC (Ch07), both driving baseline compliance (Ch05),
   rolled out through canary/rings.
5. **Configuration** — golden templates and configuration-compliance baselines to hold servers
   uniform (Ch08).
6. **Operate & recover** — health roll-up, alert policies, reports, SupportAssist; scheduled
   backups and a tested restore/upgrade path (Ch04, Ch09).

**Expected result:** a written design where a mixed connected/air-gapped fleet is discovered,
grouped dynamically, held to firmware and configuration baselines, monitored and delegated safely,
and recoverable — the operational deliverable the PowerEdge management domains build toward.

**Negative test:** manage 800 servers by logging into individual iDRACs, with ad-hoc firmware and
no templates, groups, backups, or DRM pipeline; it does not scale, drifts immediately, and the
air-gapped DC falls behind — OME's catalog/baseline/template/group model is what makes the fleet
operable.

**Cleanup:** none (design artifact).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

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
[Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md). Across all nine chapters, this volume established Dell
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
