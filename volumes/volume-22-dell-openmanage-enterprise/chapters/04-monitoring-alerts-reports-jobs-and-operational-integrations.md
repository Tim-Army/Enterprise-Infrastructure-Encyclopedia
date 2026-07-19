# Chapter 04: Monitoring, Alerts, Reports, Jobs, and Operational Integrations

## Learning Objectives

- Describe OME's health-monitoring model and how device, group, and
  appliance-level status roll up into the console's dashboards.
- Design and implement alert policies that route the right severity and
  category of event to the right destination — console, email, SNMP trap,
  syslog, or webhook.
- Build and schedule custom reports against inventory and compliance data,
  and export report output through the console and the REST API.
- Interpret the OME job engine's queue, history, and retry model for both
  system-generated and user-initiated operations.
- Configure and validate operational integrations, including SMTP relay,
  syslog/SIEM forwarding, and the SupportAssist Enterprise pipeline.
- Diagnose common monitoring and alerting failures, including silent
  alert-delivery breakage.

## Theory and Architecture

### Health status and the monitoring model

Every managed device carries a rolled-up health status — commonly
represented as Normal (green), Warning, Critical, and Unknown — computed
from the individual sensor and component conditions iDRAC (or the
relevant discovery protocol) reports to OME. Health status rolls up from
component to device and from device to group, so a group's dashboard tile
reflects the worst status among its members. This roll-up model is what
makes OME's dashboards useful at fleet scale: an operator watching a
few dozen group tiles does not need to inspect thousands of individual
devices to notice where attention is needed.

Status in OME's dashboard is a **current-state snapshot** derived from the
device's last successfully processed telemetry, not a live stream — a
device that has gone unreachable retains its last known status (or moves
to Unknown after a defined threshold) rather than updating in real time,
which matters when interpreting a dashboard during a network outage
affecting the management network itself.

### The alert pipeline

OME's alert pipeline has three conceptually distinct stages:

1. **Alert sources** — the events OME can receive or generate: SNMP traps
   forwarded from managed devices, native iDRAC/Redfish event
   subscriptions, syslog messages received from in-band OS agents, and
   OME-internal events (job failures, discovery completion, license
   expiration warnings).
2. **Alert policies** — administrator-defined rules matching alerts by
   source device/group, category (System Health, Storage, Power,
   Configuration, Audit, and others), and severity, and associating
   matches with one or more actions.
3. **Alert actions** — what happens when a policy matches: display in the
   console alert log (always available), send an email through a
   configured SMTP relay, forward as an SNMP trap to an upstream manager,
   forward as a syslog message to a SIEM or log aggregator, or, in
   releases that support it, invoke a webhook against an external system.

Because policies are evaluated independently, the same underlying alert
can simultaneously appear in the console, generate an email, and forward
to a SIEM — there is no single "the" destination; each policy's action
list is additive.

### Reports and the report engine

OME's built-in reports cover common inventory, compliance, and
operational questions out of the box (firmware compliance summary,
warranty expiration, hardware inventory detail). The **custom report
builder** lets an administrator define a query against the appliance's
reporting data model — selecting fields, applying filters, and choosing
a device/group scope — without writing SQL against the embedded database
directly, which (as established in [Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)) has no supported direct
query path. Reports can be run on demand, scheduled for recurring
generation, and exported (commonly CSV, and in some builds PDF/HTML) or
emailed to a distribution list on a schedule.

### The job engine

Every asynchronous operation in OME — discovery, inventory refresh,
firmware update orchestration ([Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)), template deployment (Chapter
8), and report generation — runs as a tracked **job**. Jobs carry a type,
a target scope, a schedule (immediate or future), an execution history
with per-target status detail, and, for supported job types, automatic
retry behavior on transient failure. The job engine is the mechanism that
makes OME's operations auditable after the fact: when an update or
configuration push produces an unexpected result, the job's execution
history — not the device's current state alone — is the first place to
look for what actually happened, in what order, and with what per-device
result.

### Operational integrations

Beyond alert forwarding, OME integrates with the broader operational
toolchain in a few defined ways:

- **SupportAssist Enterprise** — when registered ([Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)), OME can
  forward qualifying hardware alerts as automated support cases to Dell,
  attaching relevant telemetry so a support engagement starts with
  diagnostic context already available.
- **SMTP relay** — a prerequisite for email alert actions and scheduled
  report delivery; OME does not send mail directly but relays through a
  configured mail server.
- **SNMP trap and syslog forwarding** — the primary mechanism for feeding
  OME's alert stream into an existing enterprise monitoring or SIEM
  platform rather than requiring operators to watch the OME console
  directly.
- **Power Manager plugin** — where installed and licensed, extends
  monitoring to rack/row-level power and thermal telemetry beyond
  individual server health.

## Design Considerations

- **Alert policy granularity.** Design alert policies around who needs to
  act on what, not around mirroring every possible category/severity
  combination. A small number of well-scoped policies (critical
  hardware alerts to the on-call pager path, all Warning-and-above to a
  SIEM, configuration/audit events to a compliance mailbox) is easier to
  operate and reason about than dozens of narrow, overlapping policies.
- **Avoid alert fatigue by tuning severity thresholds deliberately.**
  Forwarding every Informational-severity event to an on-call channel
  trains responders to ignore the channel. Reserve high-urgency delivery
  paths (paging, SMS-style email-to-SMS gateways) for Critical severity
  and route lower severities to dashboards or digestible scheduled
  reports instead.
- **SMTP relay placement and authentication.** Decide whether the
  appliance relays through an internal open-relay-restricted SMTP
  server or an authenticated relay, and whether TLS is required — this
  affects both the trusted-certificate configuration from [Chapter 2](02-identity-licensing-security-and-administrative-control.md) and
  firewall rules between the appliance and the relay.
- **Report scheduling load.** Large, fleet-wide custom reports scheduled
  at high frequency add load to the appliance's reporting engine; align
  report frequency to actual consumption cadence (a weekly warranty
  report is rarely read daily) rather than defaulting every report to the
  shortest available interval.
- **Job concurrency and maintenance windows.** Some job types (firmware
  updates in particular, covered in depth in [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)) are sensitive to
  how many devices execute concurrently and when. Plan job scheduling
  around defined maintenance windows rather than allowing large,
  disruptive jobs to run against production hours by default.
- **Integration blast radius.** SupportAssist and any webhook-based alert
  action send data (and in SupportAssist's case, potentially open support
  cases) outside the appliance automatically. Decide deliberately which
  alert categories are appropriate to auto-forward externally versus
  which should stay internal pending human review.

## Implementation and Automation

### Creating an alert policy via the REST API

```python
#!/usr/bin/env python3
"""ome_create_alert_policy.py — create an alert policy forwarding
Critical-severity System Health alerts for a device group to syslog.

Usage: python3 ome_create_alert_policy.py <ome-host> <user> <password> \
    <group-id> <syslog-target-ip>
"""
import sys
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


def create_policy(session, host, group_id, syslog_ip):
    body = {
        "Name": "critical-system-health-to-siem",
        "Enabled": True,
        "Scope": {"GroupIds": [group_id]},
        "Severities": ["Critical"],
        "Categories": ["System Health"],
        "Actions": [
            {
                "TemplateId": None,
                "Name": "Syslog",
                "Parameters": [
                    {"Name": "destinationAddress", "Value": syslog_ip},
                    {"Name": "port", "Value": "514"},
                ],
            }
        ],
    }
    resp = session.post(
        f"https://{host}/api/AlertService/AlertPolicies", json=body, verify=False
    )
    resp.raise_for_status()
    return resp.json()


def main():
    host, user, password, group_id, syslog_ip = sys.argv[1:6]
    session = get_session(host, user, password)
    policy = create_policy(session, host, int(group_id), syslog_ip)
    print(f"Created alert policy: {policy.get('Name', policy)}")


if __name__ == "__main__":
    main()
```

The `AlertPolicies` payload shape — particularly the action parameter
naming — has been extended as additional action types (webhook support in
newer releases) were added. Confirm current field names against your
build's live API reference before scripting this into a multi-appliance
rollout.

### Querying and monitoring the job queue

```bash
# List recent jobs and their status.
curl -sk https://<appliance>/api/JobService/Jobs \
  -H "X-Auth-Token: <token>" | jq '.value[] | {Id, JobName, LastRunStatus: .LastRunStatus.Name}'

# Pull execution history detail for a specific job.
curl -sk "https://<appliance>/api/JobService/Jobs(<job-id>)/ExecutionHistories" \
  -H "X-Auth-Token: <token>"
```

Polling the job queue this way is the basis for automation that waits on
a long-running operation (an inventory refresh, a firmware update job)
before proceeding to a dependent step, rather than assuming a fixed sleep
interval is long enough.

### Generating and exporting a report via the API

```python
def run_report(session, host, report_definition_id):
    """Trigger an existing report definition and retrieve its result set."""
    resp = session.post(
        f"https://{host}/api/ReportService/ReportDefs({report_definition_id})/Actions/ReportDefService.RunReport",
        json={},
        verify=False,
    )
    resp.raise_for_status()
    # Result retrieval resource varies by build; some releases return
    # results inline, others require polling a separate ReportResults
    # resource. Confirm the current pattern for your appliance.
    return resp.json()
```

### Configuring SMTP relay and syslog forwarding (console)

SMTP relay (hostname/IP, port, authentication, and TLS mode) and the
default syslog forwarding destination are configured together under the
console's application "Alerts" or "Console and Settings" area, alongside
the alert policy definitions themselves. Configure and validate the SMTP
relay connection (most builds provide a "send test email" action) before
building alert policies that depend on it, so a policy failure is not
mistaken for a policy-configuration defect when the real cause is an
unreachable relay.

## Validation and Troubleshooting

- **Alert policy exists but nothing arrives at the destination.** Confirm
  the policy is enabled, its scope actually includes the devices
  generating the test event, and that its severity/category filter
  matches the event being tested — a policy scoped to Critical will not
  fire on a Warning-severity test alert, which is a common false-negative
  during initial policy testing.
  - **Email alerts silently fail while syslog alerts from the same policy
  succeed.** This points at the SMTP relay configuration specifically —
  check relay reachability, authentication, and whether the relay is
  rejecting mail from the appliance's configured "from" address rather
  than assuming the alert policy itself is broken.
- **Console dashboard shows stale status for a device that is actually
  back online.** As covered in Theory and Architecture, dashboard status
  is a snapshot; force an inventory/health refresh ([Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md)'s
  `RefreshInventory` action) rather than assuming a display bug.
- **A scheduled report never runs.** Check the report's schedule
  definition and the job engine for a corresponding failed or skipped job
  entry — report generation is itself a job, and a report job failure
  (for example, due to an appliance under heavy load at the scheduled
  time) surfaces in job history, not as a report-specific error message.
- **SupportAssist does not open a case for a qualifying hardware alert.**
  Confirm the appliance can still reach the SupportAssist submission
  endpoint (a common regression after firewall or proxy changes made
  after initial registration in [Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)) and that the specific alert
  category is one SupportAssist is configured to act on — not every
  alert category is eligible for automatic case creation.
- **Job execution history shows partial success across a multi-device
  job.** Read the per-device detail, not just the job's overall rolled-up
  status; a job reporting "Completed with Errors" across 50 devices could
  mean one transient failure or a systemic problem affecting many
  devices, and only the per-device detail distinguishes the two.

## Security and Best Practices

- Restrict who can create or modify alert policies and report definitions
  through role/scope assignment ([Chapter 2](02-identity-licensing-security-and-administrative-control.md)); alert routing and report
  distribution lists are a data-exposure surface, since reports and
  forwarded alerts can carry sensitive inventory and configuration detail
  off the appliance.
- Use an authenticated, TLS-protected SMTP relay rather than an open
  relay, and avoid embedding relay credentials anywhere outside the
  appliance's own configuration store.
- Validate syslog/SNMP trap forwarding destinations before relying on
  them operationally, and monitor the forwarding path itself (a silently
  broken forwarder is worse than an acknowledged gap, since it creates
  false confidence).
- Review SupportAssist's data-sharing scope with your organization's data
  handling policy before enabling automatic case creation, particularly
  in regulated environments where telemetry leaving the premises requires
  explicit approval.
- Treat report output as sensitive by default — exported inventory and
  configuration reports are a reconnaissance asset if they reach the
  wrong audience — and restrict scheduled report distribution lists
  accordingly.
- Periodically audit configured alert policies and report schedules for
  ones that reference stale distribution lists, decommissioned SIEM
  endpoints, or departed personnel's mailboxes.

## References and Knowledge Checks

**References**

- [Dell Technologies, *OpenManage Enterprise User's Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4_5_online_help_user_guide/overview) — alerts,
  reports, and job management
- [Dell Technologies, *OpenManage Enterprise RESTful API Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_p_3.10_api_guide/preface) —
  AlertService, ReportService, and JobService resources
- [Dell Technologies, *SupportAssist Enterprise documentation*](https://www.dell.com/support/product-details/en-us/product/supportassist-enterprise-v2.0/docs)
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated 4.7.x baseline

**Knowledge Checks**

1. Why can the same alert simultaneously appear in the console, generate
   an email, and forward to a SIEM, rather than being routed to a single
   destination?
2. Why does the OME dashboard's health status not necessarily reflect a
   device's real-time state?
3. Why is job execution history, not the current device state alone, the
   correct place to investigate an unexpected outcome from a firmware or
   configuration operation?
4. What is the operational risk of routing every alert severity to a
   paging channel, and how does policy design mitigate it?
5. Why should SMTP relay connectivity be validated independently before
   troubleshooting an alert policy that uses email as its action?

## Hands-On Lab

**Objective:** Configure an alert policy that forwards test alerts to a
local syslog listener, generate a qualifying test event, confirm delivery,
and validate the job engine's execution history for the underlying
operations.

**Prerequisites**

- The OME appliance and at least one onboarded device from the [Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md)
  lab (the SNMP-discovered lab Linux host is sufficient).
- A syslog listener reachable from the OME appliance. This lab uses a
  simple Python UDP listener on your workstation or lab host rather than
  a full SIEM, keeping the exercise reproducible without external
  infrastructure.
- Python 3.11+ with `requests` installed.

**Steps**

1. On your lab listener host, start a minimal syslog receiver:

   ```python
   # syslog_listener.py
   import socketserver

   class Handler(socketserver.BaseRequestHandler):
       def handle(self):
           data = self.request[0].decode(errors="replace")
           print(f"[{self.client_address[0]}] {data.strip()}")

   with socketserver.UDPServer(("0.0.0.0", 5514), Handler) as server:
       print("Listening for syslog on UDP/5514 ...")
       server.serve_forever()
   ```

   Run it with `python3 syslog_listener.py`. **Expected result:** the
   listener prints a startup message and waits for traffic.
2. In the OME console (or using the script in Implementation and
   Automation, pointed at your listener host's IP and port 5514 instead
   of 514 to avoid requiring root/administrator privileges on the
   listener host), create an alert policy scoped to the lab device group
   from [Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md), matching Warning-and-above severity across all
   categories, with a syslog forwarding action targeting your listener.
3. Confirm the policy is enabled and visible in the alert policy list.
4. Generate a qualifying test event. If your console build offers a
   built-in "generate test alert" action, use it targeting the lab
   device; otherwise, force an event by temporarily stopping the SNMP
   agent on the lab host from [Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md) (`sudo systemctl stop snmpd`) and
   forcing an inventory/health refresh so OME detects the device as
   unreachable.
5. **Expected result:** within a few minutes, a line appears in the
   syslog listener's output corresponding to the alert, and the same
   event appears in the OME console's alert log.
6. Query the job engine for the job associated with the health/inventory
   refresh from step 4 using the `JobService/Jobs` endpoint shown in
   Implementation and Automation, and retrieve its execution history.
   **Expected result:** the job's execution history shows a status
   consistent with the device becoming unreachable.
7. **Negative test:** create a second alert policy identical to the
   first but scoped to Critical-only severity, and re-run the same test
   event (a stopped SNMP agent typically registers below Critical
   severity). **Expected result:** no new line appears in the syslog
   listener for this second policy, confirming severity filtering
   correctly suppresses a non-matching event rather than forwarding
   everything regardless of policy scope.
8. Restart the SNMP agent on the lab host (`sudo systemctl start snmpd`)
   and force another inventory refresh to restore its status to Normal.

**Cleanup**

- Delete both alert policies created during the lab from the OME console.
- Stop the syslog listener script (Ctrl+C).
- Confirm the lab device's health status has returned to Normal before
  proceeding to later chapters' labs.

## Summary and Completion Checklist

This chapter connected the managed fleet from [Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md) to operational
visibility: health status roll-up and its snapshot nature, the three-stage
alert pipeline (sources, policies, actions), the custom report engine, the
job engine that underlies and makes auditable every asynchronous OME
operation, and the SupportAssist/SMTP/syslog integrations that connect
OME to the broader operational toolchain. The lab built and validated a
real alert policy against a reproducible lab target, including a severity
negative test proving policy filtering works as designed. With monitoring
and alerting in place, the volume turns next to firmware and driver
lifecycle management, the operation most OME deployments exist to
orchestrate at scale.

- [ ] I can explain how device health status rolls up to group and
      dashboard level, and why it is a snapshot rather than a live feed.
- [ ] I can describe the three stages of the alert pipeline and how a
      single alert can trigger multiple simultaneous actions.
- [ ] I created and validated an alert policy forwarding to an external
      destination, including a severity-based negative test.
- [ ] I queried the job engine's execution history to investigate an
      operation's outcome at the per-device level.
- [ ] I can name the operational integrations available (SupportAssist,
      SMTP, syslog/SNMP trap) and what each depends on to function.
