# Chapter 06: Hardware Health, Power, Thermal, Logs, and Support

![Flow diagram showing an email alert delivered end to end and confirmed in the Lifecycle Log alongside a generated Tech Support Report bundle, and an unreachable SMTP relay causing the same test alert to fail with a delivery error instead of silently succeeding.](../../../diagrams/volume-23-dell-idrac-9-10-administration/chapter-06-idrac-alerting-lifecycle-log-flow.svg)

*Figure 6-1. The alerting pipeline and Lifecycle Log validation flow exercised in this chapter's lab, including the unreachable-relay negative test.*

## Learning Objectives

- Interpret iDRAC's hardware health rollup and sensor data for CPU,
  memory, storage, fans, and power supplies.
- Configure power monitoring, power capping, and PSU redundancy policy.
- Understand and tune thermal control and fan response behavior.
- Distinguish the System Event Log (SEL) from the Lifecycle Log and use
  each appropriately during troubleshooting.
- Configure alerting (SNMP traps, email, Redfish eventing) so hardware
  events reach the right destination without depending on someone
  actively watching the console.
- Generate and interpret a Tech Support Report (TSR) for support
  escalation.

## Theory and Architecture

### The health rollup model

iDRAC continuously polls hundreds of hardware sensors — voltage, current,
temperature, fan speed, memory correctable/uncorrectable error counters,
drive SMART status, PSU state, and more — and rolls them up into a small
set of top-level health indicators (commonly represented as Normal /
Warning / Critical, color-coded and paired with text labels per this
encyclopedia's accessibility standard) for the overall system, and
separately for major subsystems: System, Storage, Power/Thermal, and each
individually addressable component underneath. The rollup model exists so
that a single glance (dashboard, LCD panel, or a single Redfish
`Status.Health` field) tells you whether deeper investigation is needed,
while the full sensor detail remains available underneath for the
investigation itself.

### Power monitoring and capping

Beyond simple current-draw reporting, iDRAC supports **power capping**: an
administrator-configured ceiling on the server's power draw, enforced by
iDRAC throttling CPU performance states as needed to stay under the cap.
This is a deliberate trade-off tool, not merely a monitoring feature —
used in power-constrained data center environments (a rack or row with
fixed power budget shared across many servers) where guaranteeing a
maximum draw per server matters more than guaranteeing peak performance at
all times. Power monitoring also tracks historical peak and average
consumption, useful for capacity planning independent of whether capping
is actually enforced.

### PSU redundancy policy

On servers with redundant power supplies, iDRAC enforces a configurable
redundancy policy — commonly modes equivalent to "no redundancy" (all
PSUs load-shared, no guaranteed failover capacity), "AC redundancy" (input
power redundancy, tolerating loss of one AC feed), and "PSU redundancy"
(tolerating outright failure of one PSU while running from the
remainder). The configured policy determines both alerting behavior
(whether losing one PSU is a Critical or a Warning-level event) and, on
some configurations, active load-balancing behavior across the PSUs
present.

### Thermal control and fan response

iDRAC manages fan speed dynamically based on the thermal profile it
observes across CPU, memory, storage, and ambient inlet sensors, following
a thermal control algorithm tuned by Dell per platform to balance
acoustic/power draw against cooling headroom. Administrators can influence
this within defined bounds — a minimum fan speed offset for environments
with unusual airflow characteristics (non-standard rack cooling, altitude
extremes, third-party PCIe cards without their own adequate cooling
profile registered with the system) — but should not treat thermal
control as an area for aggressive manual tuning outside vendor-documented
adjustment ranges, since it exists specifically to protect hardware
across a wide range of operating conditions that Dell has validated.

### System Event Log vs. Lifecycle Log

Two distinct, persistent log stores exist on iDRAC, and conflating them is
a common source of confusion during troubleshooting:

- **System Event Log (SEL)** — a hardware-event-focused log recording
  sensor threshold crossings, component state changes, and similar
  low-level events, in a format aligned with the IPMI SEL specification.
  SEL is the log most directly comparable to what a pure IPMI-based BMC
  from another vendor would expose.
  - **Lifecycle Log (LC Log)** — a broader, richer log covering
  configuration changes, firmware update history, job execution history,
  user login/logout events, and license changes, in addition to
  hardware events — effectively iDRAC's complete audit trail of
  everything that happened to the server through its management plane,
  not only hardware sensor events. The Lifecycle Log is generally the
  more useful starting point for "what happened to this server and
  when" investigations, precisely because it correlates configuration and
  administrative actions alongside hardware events on a single timeline.

Both logs persist across host OS reinstalls and most component swaps
(a replaced component typically logs its own installation event into
both), which is what makes them valuable for incident reconstruction
regardless of what state the host OS was in at the time.

### Alerting: SNMP, email, and Redfish eventing

iDRAC can push alerts through several channels, each suited to different
consumer types: SNMP traps (v1/v2c/v3) for integration with a traditional
NOC monitoring stack, email/SMTP for direct human notification, and
Redfish eventing (subscription-based webhook delivery to a listener URL,
following the DMTF Redfish EventService model) for modern automation and
SIEM integration. Alerts are filterable by category and severity, so a
fleet's alerting configuration can route, for example, only
Critical-severity storage events to a pager-integrated channel while
routing all events to a lower-urgency log aggregation destination.

### Tech Support Report (TSR)

The Tech Support Report is a comprehensive diagnostic bundle — hardware
inventory, sensor readings, both logs, firmware inventory, and (optionally)
OS-level data if iSM is installed — generated on demand and formatted for
Dell support case attachment. Generating a TSR is standard practice for
any hardware fault escalated to Dell, and generating it while the fault
condition is still current (rather than after a remediation attempt has
already changed system state) preserves the most diagnostically useful
version of the report.

## Design Considerations

- **Decide PSU redundancy policy based on actual facility power topology,
  not a fleet-wide default.** A server fed from genuinely redundant,
  independent power feeds benefits from AC redundancy mode; a server on a
  single feed with dual PSUs for component-failure tolerance only should
  use PSU redundancy mode instead — applying the wrong mode either
  under-alerts on a real exposure or over-alerts on a condition your
  facility's actual topology already tolerates.
- **Use power capping deliberately, and document the cap's rationale.** A
  cap set without documented justification looks, to a future
  administrator troubleshooting unexplained CPU throttling, like a
  performance bug rather than an intentional facility-power constraint.
  Record the cap value and the power-budget reasoning behind it alongside
  the configuration itself.
- **Route alerts by severity and category to appropriately scoped
  destinations, not one firehose.** A single alert destination receiving
  every event regardless of severity trains recipients to ignore
  notifications; scope Critical hardware alerts to an urgent channel and
  route everything else to a lower-urgency aggregation point, mirroring
  the alert-fatigue guidance covered more generally in [Volume XI](../../volume-11-observability-enterprise-operations/README.md).
- **Decide your Lifecycle Log retention and export strategy before you
  need historical data past the log's rolling capacity.** Both SEL and
  the Lifecycle Log have finite capacity and roll over; if
  long-term retention matters for compliance or trend analysis, export
  periodically to external log aggregation (via Redfish log retrieval or
  syslog forwarding) rather than assuming the on-box log is a permanent
  record.
- **Standardize your TSR generation and escalation procedure before an
  incident, not during one.** Decide who is authorized to generate and
  transmit a TSR to Dell support (it can contain configuration and
  environment detail some organizations want reviewed before external
  transmission), and have the procedure and required case information
  ready in your runbooks.

## Implementation and Automation

### Checking overall and component health

```bash
racadm getsysinfo -d
```

Over Redfish, the top-level rollup is on the `Systems` resource, and
detailed sensor data is under `Chassis`:

```bash
curl -s -k -u root:'<password>' \
  https://192.168.1.120/redfish/v1/Systems/System.Embedded.1 \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['Status'])"

curl -s -k -u root:'<password>' \
  https://192.168.1.120/redfish/v1/Chassis/System.Embedded.1/Thermal \
  | python3 -m json.tool
```

### Configuring power capping and PSU redundancy

```bash
racadm set iDRAC.Power.PowerCapEnable Enabled
racadm set iDRAC.Power.PowerCapWatt 750
racadm set iDRAC.Power.PowerCapMaxThreshold 900
racadm set iDRAC.Power.PSRedPolicy PSU-Redundancy
```

### Adjusting the thermal profile within supported bounds

```bash
racadm set iDRAC.ThermalSettings.AirExhaustTemp 40
racadm set iDRAC.ThermalSettings.FanSpeedOffset Medium
```

Confirm current allowable values and their effect for your specific
platform against the Thermal chapter of the iDRAC User's Guide before
applying non-default settings — appropriate ranges vary meaningfully by
chassis and cooling design, and the goal of any adjustment should be
documented environmental compensation, not undocumented acoustic or power
tuning.

### Retrieving the Lifecycle Log and SEL

```bash
racadm getsel
racadm lclog view
```

Over Redfish:

```bash
curl -s -k -u root:'<password>' \
  https://192.168.1.120/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel/Entries \
  | python3 -m json.tool

curl -s -k -u root:'<password>' \
  https://192.168.1.120/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries \
  | python3 -m json.tool
```

### Configuring SNMP trap and email alert destinations

```bash
racadm set iDRAC.SNMP.AgentEnable Enabled
racadm set iDRAC.SNMP.TrapFormat SNMPv3
racadm set iDRAC.SNMPAlert.1.DestAddr 10.0.0.90
racadm set iDRAC.SNMPAlert.1.State Enabled

racadm set iDRAC.EmailAlert.1.Address noc-alerts@lab.example.com
racadm set iDRAC.EmailAlert.1.Enable Enabled
racadm set iDRAC.RemoteHosts.SMTPServerIPAddress 10.0.0.25
```

### Configuring Redfish event subscriptions

```bash
curl -s -k -u root:'<password>' -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "Destination": "https://siem.lab.example.com/idrac-events",
        "EventTypes": ["Alert"],
        "Context": "idrac-rack12-u20",
        "Protocol": "Redfish"
      }' \
  https://192.168.1.120/redfish/v1/EventService/Subscriptions
```

A Python script to poll and summarize recent Lifecycle Log entries,
suitable for a scheduled health-check job that doesn't depend on
push-based alerting arriving correctly:

```python
#!/usr/bin/env python3
"""idrac_recent_events.py — retrieve and summarize the most recent
Lifecycle Log entries, flagging any at Critical severity.

Usage: python3 idrac_recent_events.py <idrac-ip> <username> <password>
"""
import sys
import requests

requests.packages.urllib3.disable_warnings()


def main() -> None:
    host, user, password = sys.argv[1], sys.argv[2], sys.argv[3]
    resp = requests.get(
        f"https://{host}/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries",
        auth=(user, password),
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()
    entries = resp.json().get("Members", [])[:20]

    critical = [e for e in entries if e.get("Severity") == "Critical"]
    print(f"Retrieved {len(entries)} recent entries; {len(critical)} Critical.")
    for e in critical:
        print(f"  [{e.get('Created')}] {e.get('Message')}")


if __name__ == "__main__":
    main()
```

### Generating a Tech Support Report

```bash
racadm techsupreport collect -t idrac,raidcontroller,systeminfo \
  -l //10.0.0.60/tsr-share -u svc-tsr -p '<password>'
```

## Validation and Troubleshooting

- **Overall health shows Warning/Critical but the specific failing
  component isn't obvious from the dashboard.** Drill into the
  component-level Redfish `Chassis` and `Systems` sub-resources
  (`Memory`, `Processors`, `Storage`, `Power`, `Thermal`) rather than
  relying on the single rollup indicator — the rollup tells you
  *that* something needs attention, not *what*.
- **PSU redundancy alert fires unexpectedly during planned maintenance.**
  Confirm whether the redundancy policy matches your actual maintenance
  activity (for example, pulling one PSU cord to test failover
  intentionally will and should trigger this alert) — this is often
  correct behavior being observed for the first time, not a fault.
- **Power capping causes unexpected performance degradation under load.**
  Check `iDRAC.Power.PowerCapWatt` against actual peak draw requirements
  for the current workload; a cap set appropriately for a prior workload
  can become a bottleneck after a workload change on the same hardware.
- **Expected alerts never arrive at the SIEM/SNMP destination.** Confirm
  network reachability from iDRAC's management interface to the
  destination specifically ([Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)) — a destination on a different
  VLAN/subnet than what the management network firewall permits is a
  common, silent alerting gap. Also confirm alert category/severity
  filtering is not inadvertently excluding the event type you expected.
- **Lifecycle Log entries appear to be missing for a known event.**
  Confirm you're not hitting log rollover for a high-event-volume
  period — check the oldest retained timestamp against when the event of
  interest occurred, and if retention doesn't cover the needed window,
  this validates the need for the export strategy discussed in Design
  Considerations.
- **TSR generation fails or times out.** Confirm the target share is
  reachable and has adequate free space — TSR bundles, especially with
  full component scope, can be substantial, and a small or unreachable
  share is a common, easily overlooked cause of failure.

## Security and Best Practices

- Use SNMPv3 rather than v1/v2c wherever your monitoring stack supports
  it — community-string-based SNMP is a weak authentication model for
  infrastructure that controls physical hardware.
- Send alerts and TSR exports over encrypted channels (HTTPS destinations
  for Redfish eventing, TLS-enabled SMTP) rather than plaintext where the
  destination supports it, since both can carry configuration and
  environment detail with some sensitivity.
- Restrict who can generate and transmit a TSR externally — the bundle can
  include hostname, network configuration, and other environment detail
  that some organizations require review of before it leaves the
  perimeter toward vendor support.
- Alert on log-related anomalies themselves, not only hardware faults —
  an unexpected gap in Lifecycle Log continuity, or an unexpected user
  login/logout pattern visible in the log, can be a meaningful security
  signal independent of any hardware health concern.
- Periodically validate that your alerting pipeline actually works end to
  end (a deliberate test alert, covered in this chapter's lab) rather than
  assuming configuration correctness; alerting that silently stopped
  working is worse than no alerting, because it creates false confidence.

## References and Knowledge Checks

**References**

- [Dell Technologies, *iDRAC9/iDRAC10 User's Guide*](https://www.dell.com/support/product-details/en-us/product/idrac10-lifecycle-controller-v1-xx-series/resources/manuals) — Power, Thermal, Logs,
  and Alerts chapters
- [Dell Technologies, *iDRAC RACADM CLI Guide*](https://www.dell.com/support/manuals/en-us/idrac9-lifecycle-controller-v4.x-series/idrac_4.00.00.00_racadm/supported-racadm-interfaces?guid=guid-a5747353-fc88-4438-b617-c50ca260448e&lang=en-us) — `iDRAC.Power`,
  `iDRAC.ThermalSettings`, `getsel`, `lclog`, and `techsupreport` command
  reference
- [Dell Technologies, *iDRAC Redfish API Guide*](https://www.dell.com/support/kbdoc/en-us/000178045/redfish-api-with-dell-integrated-remote-access-controller) — `Chassis`, `LogServices`,
  and `EventService` resources
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated iDRAC9/iDRAC10
  baseline

**Knowledge Checks**

1. What is the difference between the top-level health rollup and the
   underlying sensor detail, and why do you need both?
2. What is the practical difference between the System Event Log and the
   Lifecycle Log, and which would you check first for "what changed on
   this server last week"?
3. Why should PSU redundancy policy be set based on actual facility power
   topology rather than a fleet-wide default?
4. Why is Redfish eventing generally preferable to polling for
   integration with a modern SIEM, and when might polling still be a
   useful supplement?
5. Why does the timing of TSR generation (during the fault vs. after
   remediation) matter for its diagnostic value?

## Hands-On Lab

**Objective:** Configure an alert destination, trigger a test alert to
validate the pipeline end to end, review the Lifecycle Log, and generate
a Tech Support Report.

**Prerequisites**

- The lab server configured in Chapters 1 through 5, network-reachable.
- A reachable destination for at least one alert channel: an SNMP trap
  receiver, an SMTP relay, or an HTTP(S) endpoint capable of receiving a
  Redfish event POST (a simple local listener script is sufficient for
  this lab).
- A network share (or local export via GUI) with adequate free space for
  a TSR bundle.
- Python 3.11+ with `requests` installed.

**Steps**

1. Configure an email alert destination (or SNMP, depending on what your
   lab environment provides):

   ```bash
   racadm set iDRAC.EmailAlert.1.Address lab-alerts@lab.example.com
   racadm set iDRAC.EmailAlert.1.Enable Enabled
   racadm set iDRAC.RemoteHosts.SMTPServerIPAddress <your-lab-smtp-relay>
   ```

2. Send a test alert:

   ```bash
   racadm testemail -i 1
   ```

   **Expected result:** the configured destination receives a test
   message within a few minutes, confirming the alerting pipeline works
   end to end rather than only appearing correctly configured.
3. Review the Lifecycle Log for the test-alert event you just generated:

   ```bash
   racadm lclog view | tail -20
   ```

   **Expected result:** an entry corresponding to the test alert appears
   with a recent timestamp, confirming Lifecycle Log capture of
   administrative/alerting actions, not only hardware sensor events.
4. Run the `idrac_recent_events.py` script from the Implementation and
   Automation section:

   ```bash
   python3 idrac_recent_events.py <idrac-ip> root '<password>'
   ```

   **Expected result:** the script prints the recent entry count and
   flags any Critical-severity entries (none expected in a healthy lab
   unit, which is itself a useful confirmation).
5. Generate a Tech Support Report scoped to iDRAC and system information
   only (a smaller, faster bundle appropriate for this lab):

   ```bash
   racadm techsupreport collect -t idrac,systeminfo \
     -l //<share-ip>/tsr-share -u <svc-user> -p '<password>'
   ```

   **Expected result:** the job completes and a TSR bundle file appears
   on the target share.
6. **Negative test:** attempt `testemail` with the SMTP relay address
   intentionally set to an unreachable address:

   ```bash
   racadm set iDRAC.RemoteHosts.SMTPServerIPAddress 10.0.0.254
   racadm testemail -i 1
   ```

   **Expected result:** the test fails with a delivery error rather than
   silently reporting success, confirming the pipeline surfaces delivery
   failures rather than masking them. Restore the correct SMTP relay
   address afterward.

**Cleanup**

- Restore the correct SMTP/alert destination address if you performed the
  negative test.
- Remove the TSR bundle from the shared location once you've reviewed it,
  if the share is shared or temporary storage.
- No other cleanup is required; this lab makes no destructive changes.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter covered how iDRAC observes and reports hardware state: the
health rollup model, power monitoring and capping, PSU redundancy policy,
thermal control within supported bounds, the distinction between the
System Event Log and the richer Lifecycle Log, multi-channel alerting
(SNMP, email, Redfish eventing), and the Tech Support Report as the
standard artifact for vendor escalation. The lab validated the alerting
pipeline end to end with both a positive and negative test — the single
most important habit this chapter establishes, since unvalidated alerting
configuration is a common, easy-to-miss operational gap.

- [ ] I can interpret the health rollup and drill into component-level
      detail when it indicates a problem.
- [ ] I can configure power capping and PSU redundancy policy
      appropriately for a given facility power topology.
- [ ] I can distinguish the System Event Log from the Lifecycle Log and
      choose the right one for a given troubleshooting question.
- [ ] I configured an alert destination and validated it end to end with
      both a successful test and a negative (delivery-failure) test.
- [ ] I generated a Tech Support Report and know what triggers its use in
      a real support escalation.
