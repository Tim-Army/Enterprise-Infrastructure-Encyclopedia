# Chapter 04: Host Management, Administration, Inventory, and Reporting

![Lab flow for this chapter: a custom role scoped to a single lab group is assigned to a second test user, and logging in as that user shows only the scoped population; a dynamic group updates membership automatically as an underlying property is toggled, and a report scoped to that group exports and schedules correctly. As a negative test, the scoped read-only account attempts to modify a policy or host property outside its granted permissions; the platform denies the action, confirming RBAC scope restriction is enforced at the write layer, not merely cosmetic in the inventory view.](../../../diagrams/volume-015-forescout-platform-certifications/chapter-04-rbac-scope-enforcement-flow.svg)

*Figure 4-1. Flow used throughout this chapter's Hands-On Lab: a role-scoped read-only user, a dynamic group, and a scheduled report, tested against an out-of-scope write attempt.*

## Learning Objectives

- Perform day-to-day host management actions (manual property overrides,
  grouping, tagging, and action history review) from the asset inventory.
- Administer Console user accounts and role-based access control
  appropriate to NOC, SOC, and platform-administrator responsibilities.
- Manage platform administration tasks: appliance health monitoring,
  licensing, backup/restore, and update management.
- Design and build dashboards and scheduled reports that serve
  operational, compliance, and executive audiences from the same
  underlying inventory data.
- Apply data retention and audit-logging practices appropriate for a
  system of record that feeds compliance reporting.

## Theory and Architecture

Chapters 1–3 built the visibility and policy foundation: appliances and
plugins populate the property store, classification and clarification
resolve identity, and compliance/control policies govern network state.
This chapter turns to the operational layer that sits on top of that
foundation — the daily and periodic administrative work that keeps a
Forescout deployment trustworthy, available, and useful to the audiences
who depend on it without themselves being policy authors: NOC/SOC
analysts triaging alerts, IT administrators auditing device inventory,
platform administrators keeping the system itself healthy, and
compliance/executive stakeholders consuming reports.

### Host management from the inventory

While policies ([Chapter 3](03-clarification-compliance-and-control-policies.md)) handle governance at scale, individual host
records still need day-to-day human management:

- **Manual property overrides.** An administrator can manually set or
  correct a property value on an individual host record — useful when an
  automated source is temporarily wrong or unavailable, but a practice
  that should be logged and periodically reconciled, since a manual
  override can silently mask a plugin or classification problem that
  otherwise needs fixing at the source.
- **Groups.** Static or dynamic (property-driven) collections of hosts
  used as scope boundaries for policies, reports, and dashboards. Dynamic
  groups defined by a property condition (for example, "all hosts with
  `Function = Printer`") stay current automatically; static groups
  require manual membership maintenance and are appropriate for
  fixed, well-known populations (a named list of executive devices, for
  example).
- **Tags.** Lightweight, human-applied labels for ad hoc triage state
  ([Chapter 2](02-console-plugins-properties-and-asset-classification.md)), distinct from groups in that a tag typically does not
  drive policy scope the way a group does, though the platform allows
  tags to be used as policy conditions where useful.
- **Action history.** Every automated and manual action taken against a
  host — policy-driven property changes, control actions, and manual
  overrides — is recorded in a host-level history, which is the first
  place to look when investigating why a host is in its current state.

### Console user administration and role-based access control

Console access is itself governed by role-based access control (RBAC),
typically combining:

- **Built-in and custom roles**, scoping what a user can view (read-only
  inventory access) versus what they can change (policy authoring,
  plugin configuration, control-action execution, platform
  administration).
- **Scope restriction**, limiting a role to a subset of the inventory —
  for example, a regional NOC analyst role scoped only to that region's
  appliances and host groups, rather than the full enterprise inventory.
- **Centralized authentication**, integrating Console accounts with the
  organization's identity provider (RADIUS/LDAP/SAML, per the current
  release's supported provider list) so that account lifecycle
  (provisioning, deprovisioning, MFA) rides on existing identity
  governance rather than a separate local account store.

Designing roles around job function — not around individual named users —
keeps the model maintainable as staff turn over: a "SOC Analyst" role
definition should outlive any specific analyst assigned to it.

### Platform administration

Platform administration covers the health and lifecycle of the platform
itself, distinct from the policies and data it manages:

- **Appliance and Enterprise Manager health monitoring.** Dashboards and
  alerts covering CPU, memory, disk, plugin status, and monitor-interface
  link state across every appliance, so degradation is caught before it
  becomes a visibility or enforcement gap.
- **Licensing management.** Tracking licensed host-count consumption
  against purchased entitlement per capability module ([Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)), with
  alerting before a deployment exceeds its licensed ceiling.
- **Backup and restore.** Scheduled configuration and database backups
  from the Enterprise Manager, covering policy definitions, plugin
  configuration, custom properties, and user/role definitions — the
  artifacts that would otherwise require a full manual rebuild after a
  catastrophic failure.
- **Update and patch management.** Applying vendor-released updates to
  appliance/EM software and to individual plugins on a defined
  maintenance cadence, distinct from the endpoint-facing patch
  compliance checks a compliance policy might evaluate.
- **Audit logging.** A record of administrative actions taken within the
  Console itself (policy edits, user account changes, plugin
  reconfiguration) — the platform's own change log, which is as
  important to review periodically as the action history it keeps on
  managed hosts.

### Reporting and dashboards

Reporting turns the same inventory and policy data multiple audiences
already depend on into a form each audience can consume without needing
Console access or query skill:

- **Dashboards** present near-real-time widgets (compliance posture by
  site, unclassified host trend, control actions in the last 24 hours)
  for operational staff who need current state at a glance.
- **Scheduled reports** run on a fixed cadence (daily, weekly, monthly)
  and are distributed by email or exported to a file share — typically
  the mechanism compliance and executive audiences actually consume,
  since they do not log into the Console directly.
- **Ad hoc/on-demand reports** support point-in-time investigations (an
  auditor's specific data request, an incident's asset-scope question)
  without waiting for the next scheduled run.

## Design Considerations

- **Dynamic groups over static where possible.** Prefer property-driven
  dynamic groups for anything that should track the environment
  automatically; reserve static groups for genuinely fixed, small
  populations where manual maintenance is acceptable.
- **Role design around function, not individuals.** Build the RBAC model
  around job functions and the minimum access each function needs,
  independent of who currently holds that job — this is what keeps the
  model correct through staff turnover without a redesign.
- **Report audience alignment.** Design each report or dashboard for one
  primary audience and its actual decision — a compliance report for an
  auditor should read differently from an operational dashboard for a
  NOC shift, even when both draw from the same compliance-status data.
- **Manual override discipline.** Decide, as a documented policy, when a
  manual property override is acceptable versus when it signals a plugin
  or classification defect that must be fixed at the source; an
  environment with many long-lived manual overrides usually has an
  underlying data-quality problem being papered over.
- **Backup scope and frequency.** Size backup frequency to the
  organization's tolerance for reconfiguration work after a failure —
  policy-heavy deployments with frequent tuning need more frequent
  backups than a stable, mature deployment.
- **Data retention vs. compliance requirement.** Align host-history and
  report data retention with the organization's actual compliance
  obligations (PCI DSS, HIPAA, or sector-specific requirements) rather
  than a default retention window that may be shorter than what an
  auditor will ask for.
- **License headroom.** Plan licensed host-count headroom above current
  count for a deployment expected to grow (new sites, IoT/OT expansion),
  since a license ceiling reached unexpectedly during an onboarding wave
  is an avoidable operational disruption.

## Implementation and Automation

1. **Define the RBAC role model** before creating individual accounts:
   enumerate job functions (platform administrator, policy author, SOC
   analyst, read-only auditor, regional NOC analyst) and the minimum
   Console capability and inventory scope each needs.
2. **Integrate centralized authentication** (RADIUS/LDAP/SAML) and map
   identity-provider groups to the defined Console roles, so account
   provisioning and deprovisioning follow the organization's existing
   identity lifecycle process.
3. **Build dynamic groups** for the operational populations staff will
   triage against daily — for example, a group defined as `Compliance
   Status != "Compliant" AND Function = "Windows Workstation"`.
4. **Configure appliance/EM health monitoring and alerting**, routing
   critical alerts (appliance offline, disk-space threshold, plugin
   failure) to the platform administration team's existing alerting
   channel (email, syslog to SIEM, or a ticketing integration).
5. **Schedule configuration backups** from the Enterprise Manager on a
   cadence matched to the deployment's change frequency, and store
   backups in a location independent of the appliance/EM infrastructure
   itself.
6. **Build core dashboards** for each primary operational audience —
   for example, a NOC dashboard showing appliance health and active
   control actions, and a SOC dashboard showing compliance posture and
   unclassified-host trend.
7. **Build and schedule compliance/executive reports**, aligning report
   fields to the specific compliance framework or executive metric being
   reported (for example, a monthly PCI-scoped-segment compliance summary
   distributed automatically to the named stakeholder distribution
   list). A representative scheduled-report definition in outline form:

   ```text
   REPORT "Monthly PCI Segment Compliance"
     SCOPE: group "PCI Scoped Hosts"
     FIELDS: Host, IP, Function, Compliance Status, Last Seen
     SCHEDULE: monthly, 1st business day, 06:00 local
     DISTRIBUTION: email to compliance-reporting distribution list
     FORMAT: CSV attachment + summary in email body
   ```

8. **Review the administrative audit log** on a defined cadence
   (weekly or monthly, depending on deployment change velocity) as a
   standing operational task, not only during incident investigation.
9. **Test the restore procedure** at least once outside of an actual
   failure, against a non-production appliance or EM instance, so the
   backup process is validated before it is needed under pressure.

## Validation and Troubleshooting

- **A user cannot see hosts they should be able to.** Check the role's
  scope restriction first; an overly narrow group or site scope on the
  assigned role is the most common cause, ahead of an outright
  permissions bug.
- **A scheduled report stops arriving.** Confirm the distribution
  mechanism (SMTP relay credentials, file-share connectivity) rather than
  assuming the report definition itself broke — delivery-path failures
  are more common than report-logic failures once a report has run
  successfully at least once.
- **Dashboard data looks stale.** Confirm the underlying dynamic group or
  widget's refresh interval, and cross-check against known appliance
  health — a dashboard fed by an appliance that has silently dropped
  offline will show stale data without an obvious visual error unless
  appliance health alerting (Implementation step 4) is also configured.
- **A restored backup does not fully recover expected state.** Confirm
  the backup scope actually covered what was expected (some backup
  configurations exclude certain plugin credentials or large historical
  data by design) and that the restore was performed against a
  compatible platform version.
- **License consumption alert fires unexpectedly.** Cross-check actual
  managed host count against recent group or plugin scope changes; a
  newly onboarded segment or a plugin scope expansion is the most common
  cause of an unplanned consumption jump.

## Security and Best Practices

- Enforce MFA at the identity provider for any Console role with
  policy-authoring, plugin-configuration, or control-action privileges,
  given the platform's privileged reach into network infrastructure and
  endpoint data.
- Review RBAC role assignments on a fixed cadence (quarterly is common)
  as part of standard access recertification, not only when a new
  employee starts.
- Restrict who can review or export full inventory and report data
  containing sensitive properties (user identity, device ownership); not
  every read-only role needs every property visible.
- Encrypt backup files at rest and restrict access to backup storage —
  a configuration backup contains policy logic and, depending on scope,
  plugin credentials, making it as sensitive as the live system.
- Log and periodically review manual property overrides distinctly from
  automated changes, since a pattern of manual overrides can itself be
  an indicator of either a data-quality problem or, in rare cases,
  deliberate evasion of a compliance or control policy.
- Retain the administrative audit log for at least as long as the
  organization's compliance or incident-investigation retention
  requirement, and forward it to the SIEM ([Chapter 5](05-advanced-policy-integrations-and-business-outcomes.md)) for tamper-resistant
  storage independent of the platform itself.

## References and Knowledge Checks

**References**

- [Forescout Technologies Console administration, user/role management,
  and reporting guides for the 8.5.x release.](https://docs.forescout.com/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- Chapters 1–3 of this volume for the appliance, property, and policy
  model that host management, administration, and reporting build on.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA/FSCP/FSCE blueprint domain mapping for this volume.

**Knowledge Checks**

1. What is the difference between a dynamic group and a static group, and
   when is a static group still the correct choice?
2. Why should RBAC roles be designed around job function rather than
   individual users?
3. Name three platform administration tasks distinct from policy
   authoring, and explain why each matters operationally.
4. Why should a scheduled report's audience shape its content and format,
   even when it draws from the same underlying data as an operational
   dashboard?
5. Why is a documented, tested restore procedure necessary in addition to
   a scheduled backup?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each theme of host management,
administration, inventory, and reporting** — which maps to the FSCA course's Host
Management, Administration, and Inventory/Assets/Reporting/Dashboard lessons. These are
Console and CLI operator tasks. Each ends **`**Lab verified by:** *pending*`** until a
human runs it.

**Shared prerequisites for Labs 4.1–4.4** — a Forescout deployment with the Console,
discovered hosts, and appliance CLI access. **Cost:** none beyond lab resources.

### Lab 4.1 — Inventory groups and tags (Topic: Inventory and Assets)

**Objective:** Organize hosts with groups and confirm they drive policy scope.

```text
# Console: Asset Inventory > create a group (e.g. "Finance-Endpoints"). Add hosts
#   manually or via a policy action that assigns membership. Then use the group as
#   the scope of a policy or the filter of a report.
```

**Expected result:** the group populates and can be referenced as a policy scope or
report filter — groups and tags are the organizing layer that lets one deployment apply
different policy and reporting to different populations (finance, guests, IoT, servers).

**Negative test:** scope enforcement to "all hosts" instead of a group; the action hits
populations it was never meant for — groups are what keep policy blast-radius controlled.

**Rollback:** delete the lab group.

### Lab 4.2 — Console RBAC and user management (Topic: Administration — console users)

**Objective:** Create a scoped Console operator role.

```text
# Console: Options > Console User Profiles (User Management). Create a user with a
#   role granting read/operate on a limited set of groups or functions (e.g. a
#   help-desk role that can view inventory and run a remediation action but cannot
#   edit policies). Log in as that user and confirm the boundary.
```

**Expected result:** the scoped user sees and does only what the role permits — Console
RBAC enforces least privilege so operators, auditors, and administrators each get an
appropriate slice of a shared deployment.

**Negative test:** give every operator full administrator rights; any one can rewrite
enforcement policy or export the full asset inventory — role scoping is what prevents
that.

**Rollback:** delete the lab user/role.

### Lab 4.3 — Platform administration: backup and updates (Topic: Administration — maintenance)

**Objective:** Take a configuration backup and check update state — the operator safety net.

```text
# Console: Tools > Backup (or Options > for scheduled backups) to export the
#   configuration; note the backup file/location. Then check component/plugin
#   update status.
fsctl status        # confirm services healthy before/after maintenance
```

**Expected result:** a stored configuration backup you could restore, and a clear view of
component/plugin versions and available updates — backups before changes and controlled
updates are the core administration discipline for a Forescout deployment.

**Negative test:** apply a major component update with no backup and no maintenance
window; if it misbehaves there is nothing to restore and enforcement may disrupt users —
the backup is what makes the change reversible.

**Rollback:** none (keep the backup; remove it later if lab-only).

### Lab 4.4 — Dashboards and reports (Topic: Reporting and Dashboard)

**Objective:** Build a report that communicates a security outcome.

```text
# Console: Reports > create a report (e.g. "Compliance by Department" or "Devices by
#   Classification"). Scope it to a group from Lab 4.1, run it, and schedule delivery.
#   Add a matching Dashboard widget for at-a-glance status.
```

**Expected result:** a runnable, schedulable report and a live dashboard widget that turn
raw visibility into something a manager or auditor can read — reporting is how a
deployment demonstrates value and compliance, not just enforces it.

**Negative test:** present raw Asset Inventory exports as the security report; stakeholders
cannot read thousands of rows — a scoped, aggregated report is what communicates outcome.

**Rollback:** delete the lab report/dashboard widget.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter moved from policy design ([Chapter 3](03-clarification-compliance-and-control-policies.md)) to the operational
layer that keeps a Forescout deployment usable and trustworthy day to day:
host management actions available directly from the inventory, Console
user administration and role-based access control, platform
administration tasks (health monitoring, licensing, backup/restore,
updates, audit logging), and a reporting/dashboard model that serves
operational, compliance, and executive audiences from the same underlying
data.

**Completion checklist**

- [ ] Can distinguish dynamic groups, static groups, and tags, and choose
      correctly among them for a given use case.
- [ ] Can design an RBAC role model scoped to job function and
      inventory/site boundaries.
- [ ] Can list the core platform administration tasks and why each is
      operationally necessary.
- [ ] Completed the hands-on lab, including the RBAC negative test and a
      validated configuration backup.
- [ ] Understands why report design should start from audience and
      decision, not from available fields.
