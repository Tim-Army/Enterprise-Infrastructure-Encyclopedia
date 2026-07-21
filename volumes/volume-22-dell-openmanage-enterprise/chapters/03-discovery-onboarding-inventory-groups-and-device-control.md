# Chapter 03: Discovery, Onboarding, Inventory, Groups, and Device Control

![Topology diagram showing an SNMP-discovered lab host onboarded into static and dynamic groups with inventory refresh, alongside a wrong-community-string discovery that never onboards the device and a power-control action rejected for lacking an iDRAC interface.](../../../diagrams/volume-22-dell-openmanage-enterprise/chapter-03-snmp-discovery-onboarding-topology.svg)

*Figure 3-1. The SNMP discovery and onboarding topology exercised in this chapter's lab, including both negative tests.*

## Learning Objectives

- Explain how OME's discovery engine locates devices across protocols and
  turns discovered endpoints into inventoried, managed devices.
- Select the correct discovery protocol and credential profile for each
  class of target: iDRAC-managed PowerEdge servers, third-party
  Redfish-compliant devices, and SNMP-manageable network and storage gear.
- Design a device-group strategy using static and dynamic (query-based)
  groups that supports both operational views and the scoped
  administration introduced in [Chapter 2](02-identity-licensing-security-and-administrative-control.md).
- Run and schedule discovery and inventory jobs from the console and the
  REST API, and interpret job and device-state outcomes.
- Perform device control operations (power actions, identification, and
  labeling) against managed devices and validate the results.
- Diagnose common discovery and inventory failures.

## Theory and Architecture

### From discovery to managed device

OME's fleet model runs through a consistent pipeline: **discovery** probes
a set of network targets using one or more protocols and credential sets
to determine what is reachable and what it is; **onboarding** commits
discovered endpoints that OME can positively identify into the managed
device inventory; and **inventory collection** then pulls detailed
hardware and software facts from each managed device on an ongoing
schedule. A device that is merely discovered but not confirmed as a
supported, credentialed target does not become a managed device — OME
distinguishes discovered-but-unmanaged endpoints from fully onboarded
devices, and only the latter participate in monitoring, firmware
compliance, templates, and the rest of this volume's remaining chapters.

### Discovery protocols by device class

OME's discovery engine is protocol-pluggable, and the protocol you choose
per discovery job depends on the target device class:

- **iDRAC-managed PowerEdge servers** — discovered over HTTPS using
  WS-Management and, increasingly, Redfish, directly against each server's
  iDRAC. This is the primary, richest-fidelity path: iDRAC exposes full
  hardware inventory, firmware versions, and update/configuration control
  to OME. iDRAC discovery and administration in depth is [Volume XXIII](../../volume-23-dell-idrac-9-10-administration/README.md)'s
  subject; this chapter treats iDRAC as one of several credentialed
  discovery targets from OME's side of the relationship.
- **Third-party Redfish-compliant servers** — discovered over HTTPS using
  generic Redfish, with a narrower feature set than native iDRAC discovery
  since OME cannot rely on Dell-specific Redfish extensions.
  **Third-party network and storage devices** — discovered primarily over
  SNMP (UDP 161), which yields basic identification and health polling
  but not the deep hardware/firmware inventory available from iDRAC.
- **In-band host/OS targets** — discovered over SSH (Linux) or WMI/WinRM
  (Windows) where an in-band agent-free inventory of the host operating
  system is required in addition to the out-of-band iDRAC view of the same
  physical server.
- **IPMI-only legacy targets** — discovered over IPMI (UDP 623) where
  neither WS-Management/Redfish nor SNMP is available; this path offers
  the least inventory and control fidelity of the options above and is
  primarily a compatibility fallback.

### Credential profiles

Discovery jobs reference one or more **discovery credential profiles** —
named, reusable sets of credentials (and, for SNMP, community strings or
SNMPv3 authentication parameters) scoped to a protocol. Separating
credential storage from individual discovery jobs means a credential
rotation only requires updating the profile, not every job that
references it, and means discovery jobs themselves do not need to embed
plaintext secrets in their own definitions.

### Groups: static and dynamic

OME organizes devices into groups for both operational visibility and, as
established in [Chapter 2](02-identity-licensing-security-and-administrative-control.md), scoped administration:

- **Static groups** hold an explicitly assigned device membership list;
  membership changes only when an administrator (or automation) adds or
  removes a device.
- **Dynamic (query-based) groups** define membership by a filter
  expression evaluated against device attributes — model, service tag
  prefix, firmware version, location tag, or custom attribute — so
  membership updates automatically as devices are onboarded, retired, or
  change state, without manual curation.
- **Plugin-defined groups** are created automatically by certain plugins
  (for example, chassis-derived groupings from an OME-Modular federation)
  and are generally not hand-edited.

A common pattern is to use dynamic groups for broad operational categories
(all PowerEdge R760 servers, all devices with non-compliant firmware) and
static groups for scope boundaries tied to organizational structure
(region, business unit) that should not shift automatically based on
device attributes alone.

### Inventory collection

Once a device is onboarded, OME schedules recurring **inventory jobs**
that refresh hardware inventory (CPU, memory, storage controllers and
drives, network adapters, power supplies), firmware and driver versions,
and, where license and connectivity permit, warranty entitlement pulled
from Dell's backend services. Inventory data is what firmware compliance
([Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)) and configuration compliance ([Chapter 8](08-templates-configuration-compliance-automation-and-apis.md)) are evaluated
against, so inventory freshness directly affects the accuracy of those
reports.

## Design Considerations

- **Protocol selection drives fidelity.** Prefer native iDRAC
  (WS-Management/Redfish) discovery for every PowerEdge server in scope;
  reserve SNMP and IPMI paths for genuinely third-party or legacy targets
  where no richer protocol is available. Mixing protocols unnecessarily
  for devices that support the richer path only reduces the inventory and
  control fidelity you get for no operational benefit.
- **Credential profile scope and rotation.** Build credential profiles
  around logical device populations (for example, one profile per site's
  iDRAC service account) rather than one profile per device, and align
  profile credential rotation with your organization's broader service
  account rotation policy — an out-of-date discovery credential does not
  break already-onboarded devices immediately, but it silently blocks
  future re-discovery and can cause intermittent authentication failures
  on scheduled inventory refresh.
- **Network segmentation and discovery scope.** Scope discovery jobs to
  address ranges or subnets that intentionally match your out-of-band
  management network design ([Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)); an overly broad discovery range
  risks probing devices outside your management intent and generating
  noisy, irrelevant discovery-job results.
- **Group hierarchy mirrors administrative intent.** Design your dynamic
  and static group taxonomy together with the scope model from [Chapter 2](02-identity-licensing-security-and-administrative-control.md)
  — decide up front which groups exist to answer an operational question
  ("show me everything running firmware older than X") versus which exist
  to bound who can act on what. Conflating the two produces either overly
  broad delegated-admin scopes or operational views cluttered with
  administrative artifacts.
- **Inventory schedule cadence.** A shorter inventory refresh interval
  gives more current compliance and monitoring data but adds load to both
  OME and the managed fleet's management controllers; align cadence to
  how quickly your organization needs to detect drift versus the
  acceptable background load on iDRACs, which also service other
  management traffic.
- **Discovery job ownership and scheduling.** Decide whether discovery is
  a one-time bulk onboarding exercise (typical for a new OME deployment
  absorbing an existing fleet) or an ongoing scheduled job (typical for an
  environment where new servers are racked continuously) — the two
  patterns warrant different job scheduling and different alerting on
  discovery-job failure.

## Implementation and Automation

### Creating a discovery credential profile and running discovery via the API

```python
#!/usr/bin/env python3
"""ome_discover_range.py — create an iDRAC discovery credential profile
and launch a discovery job against an IP range, then poll it to
completion.

Usage: python3 ome_discover_range.py <ome-host> <user> <password> \
    <idrac-user> <idrac-password> <ip-range-start> <ip-range-end>
"""
import sys
import time
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


def start_discovery(session, host, idrac_user, idrac_pass, ip_start, ip_end):
    body = {
        "DiscoveryConfigGroupName": f"api-discovery-{int(time.time())}",
        "DiscoveryConfigModels": [
            {
                "DiscoveryConfigTargets": [
                    {"NetworkAddressDetail": f"{ip_start}-{ip_end}"}
                ],
                "ConnectionProfile": (
                    '{"profileName":"","credentials":[{"type":"WSMAN",'
                    f'"authType":"Basic","modified":false,'
                    f'"credentials":{{"username":"{idrac_user}",'
                    f'"password":"{idrac_pass}","port":443,"retries":3,'
                    f'"timeout":60}}}}]}}'
                ),
                "DeviceType": [1000],  # server device type
            }
        ],
    }
    resp = session.post(
        f"https://{host}/api/DiscoveryConfigService/DiscoveryConfigGroups",
        json=body,
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    host, user, password, idrac_user, idrac_pass, ip_start, ip_end = sys.argv[1:8]
    session = get_session(host, user, password)
    result = start_discovery(session, host, idrac_user, idrac_pass, ip_start, ip_end)
    print(f"Discovery job group created: {result.get('DiscoveryConfigGroupName', result)}")
    print("Poll GET /api/JobService/Jobs for the associated job to track completion; "
          "confirm the exact discovery-config payload shape and job linkage against "
          "your build's API reference, as this resource's schema has been extended "
          "across OME releases.")


if __name__ == "__main__":
    main()
```

The discovery configuration payload above is intentionally illustrative:
`DeviceType` codes, the `ConnectionProfile` JSON-in-JSON encoding, and the
exact set of required fields have changed across OME releases as
additional protocols and device classes were added. Always validate the
current schema against the live API reference on your appliance before
building this into unattended automation.

### Creating groups

Static groups are created and populated directly; dynamic groups are
created with a filter/query definition evaluated by the appliance:

```bash
# Create a static group.
curl -sk -X POST https://<appliance>/api/GroupService/Groups \
  -H "X-Auth-Token: <token>" -H "Content-Type: application/json" \
  -d '{"Name": "site-east-prod", "Description": "Production servers, East site", "MembershipTypeId": 12}'

# Add devices to a static group (device IDs from DeviceService/Devices).
curl -sk -X POST https://<appliance>/api/GroupService/Groups\(<group-id>\)/AddMemberDevices \
  -H "X-Auth-Token: <token>" -H "Content-Type: application/json" \
  -d '{"MemberDeviceIds": [10001, 10002, 10003]}'
```

Dynamic (query) group creation typically requires a filter expression
against device attributes; confirm the current dynamic-group resource and
filter syntax for your build, since query-group support has matured
across OME 3.x and 4.x releases.

### Device control operations

Power control and identification (chassis LED blink/locate) are exposed
through a device-action resource that accepts a list of target device IDs
and an action code:

```python
def power_control(session, host, device_ids, action="PowerCycle"):
    """action: PowerOn, PowerOffGraceful, PowerOffNonGraceful, PowerCycle,
    ColdBoot, WarmBoot"""
    body = {
        "DeviceIds": device_ids,
        "Action": action,
    }
    resp = session.post(
        f"https://{host}/api/DeviceService/Devices/Actions/DeviceService.PowerControl",
        json=body,
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()
```

Confirm the exact action resource path and the accepted `Action` value set
against your build; power-control action naming has been one of the more
frequently revised parts of the device-action API surface.

### Forcing an out-of-cycle inventory refresh

```bash
curl -sk -X POST https://<appliance>/api/DeviceService/Devices/Actions/DeviceService.RefreshInventory \
  -H "X-Auth-Token: <token>" -H "Content-Type: application/json" \
  -d '{"DeviceIds": [10001, 10002]}'
```

This queues an immediate inventory job for the specified devices rather
than waiting for the next scheduled refresh interval, useful for
confirming a change (a driver update, a newly added drive) is reflected
before the next automatic cycle.

## Validation and Troubleshooting

- **A device is discovered but never becomes managed.** Confirm the
  credential profile used actually authenticates against the target — a
  discovery job can report a device as reachable at the network layer
  (ICMP/port responds) while still failing authentication, which prevents
  onboarding. Check the discovery job's per-target result detail rather
  than only its summary status.
  - **Discovery succeeds intermittently across an otherwise uniform
  subnet.** This pattern often points to a credential profile with stale
  credentials for a subset of devices (for example, after a partial
  password rotation) rather than a network issue, since a true network
  problem would typically fail uniformly.
- **Inventory data looks stale.** Check the device's last inventory job
  timestamp and status before assuming a hardware-level problem; a failed
  or skipped inventory job (commonly due to a credential or connectivity
  regression after initial onboarding) will leave the last-known-good
  inventory in place without an obvious visual indicator that it is out
  of date.
- **A dynamic group has unexpected membership.** Re-check the filter
  expression against actual device attribute values (attribute names and
  available values can differ subtly from what an administrator expects,
  especially for firmware version strings) rather than assuming a group
  engine defect.
- **Power control action reports success but the device state does not
  change.** Confirm the action was issued against the correct device
  identity (iDRAC-managed device ID versus a raw discovered endpoint ID
  can differ) and check the corresponding job's detailed status; a
  gracefully requested power-off issued to an OS that ignores ACPI
  shutdown signals will report the command as delivered without the host
  actually powering off.
- **SNMP-discovered devices show minimal inventory.** This is expected:
  SNMP discovery yields identification and basic health polling, not the
  deep component-level inventory available from native iDRAC discovery.
  Do not treat sparse SNMP inventory as a discovery failure.

## Security and Best Practices

- Use dedicated, least-privilege discovery credentials distinct from
  broader administrative credentials, and store them only inside OME's
  credential profiles rather than in ad hoc scripts or spreadsheets used
  during a bulk onboarding project.
- Scope discovery IP ranges tightly to your intended management network;
  broad or default-route-adjacent discovery ranges risk probing
  unrelated infrastructure and generating findable evidence of scanning
  activity that a security team will reasonably want explained.
- Rotate discovery credentials on the same cadence as other privileged
  service accounts, and update the corresponding credential profile
  immediately — do not let discovery accounts silently drift out of an
  organization's credential rotation program because they are "just for
  discovery."
- Align group-based scope ([Chapter 2](02-identity-licensing-security-and-administrative-control.md)) with actual organizational
  boundaries and review group membership periodically, particularly for
  dynamic groups whose membership can shift in ways that quietly widen a
  delegated administrator's effective access.
- Treat device control actions (power operations in particular) as
  privileged operations gated by role and scope, not as available to any
  authenticated console user — a broadly granted power-control permission
  is an easy path to accidental or malicious fleet-wide disruption.

## References and Knowledge Checks

**References**

- [Dell Technologies, *OpenManage Enterprise User's Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4_5_online_help_user_guide/overview) — discovery,
  inventory, and group management
- [Dell Technologies, *OpenManage Enterprise RESTful API Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_p_3.10_api_guide/preface) —
  DiscoveryConfigService, DeviceService, and GroupService resources
- [Dell Technologies, *OpenManage Enterprise Support Matrix*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4.x.x_support_matrix/openmanage-enterprise-4xx-support-matrix) — supported
  discovery protocols by device class
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated 4.7.x baseline

**Knowledge Checks**

1. Why does OME distinguish a discovered endpoint from a fully onboarded
   managed device, and what data does a device gain access to only after
   onboarding?
2. Why does native iDRAC discovery yield richer inventory than SNMP
   discovery of the same physical server?
3. When would a dynamic (query-based) group be a better fit than a static
   group, and when is the reverse true?
4. Why can a discovery job report a target as network-reachable while
   still failing to onboard it as a managed device?
5. Why should device power-control actions be treated as a
   role/scope-gated privileged operation rather than a general console
   capability?

## Hands-On Lab

**Objective:** Discover a device over SNMP, onboard it, place it into
both a static and a dynamic group, run an inventory refresh, and exercise
a device-control action, without requiring physical Dell hardware.

**Prerequisites**

- The OME appliance from [Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)/2's labs, reachable from your
  workstation, with an account holding at least Device Manager-tier
  rights.
- A Linux host (a lab VM is sufficient) on the same network as the OME
  appliance, with `net-snmp` installed and an SNMP daemon configured with
  a read-only community string — this lab host stands in for a
  third-party SNMP-manageable device so the exercise does not depend on
  owning a physical PowerEdge server.
- Python 3.11+ with `requests` installed on your workstation.

**Steps**

1. On the lab Linux host, install and enable a minimal SNMP agent:

   ```bash
   sudo apt-get update && sudo apt-get install -y snmpd
   sudo sed -i 's/^agentAddress.*/agentAddress udp:161,udp6:[::1]:161/' /etc/snmp/snmpd.conf
   echo 'rocommunity labpublic default' | sudo tee -a /etc/snmp/snmpd.conf
   sudo systemctl restart snmpd
   ```

   **Expected result:** `snmpwalk -v2c -c labpublic <lab-host-ip> system`
   run from another host returns system description output, confirming
   the agent is reachable.
2. In the OME console, create an SNMP discovery credential profile using
   community string `labpublic`, then create and run a discovery job
   targeting the lab host's single IP address with the SNMP protocol
   selected.
3. **Expected result:** the discovery job completes and the lab host
   appears in the discovered-device results; onboard it into managed
   inventory.
4. Create a static group named `lab-snmp-devices` and add the onboarded
   lab host to it through the console or the `AddMemberDevices` API call
   shown in Implementation and Automation.
5. Create a dynamic group filtered on device type or discovery protocol
   equal to SNMP (exact filter field names depend on your build), and
   confirm the lab host's membership appears automatically without being
   manually added.
6. Force an out-of-cycle inventory refresh against the lab host using the
   `RefreshInventory` action shown above, and confirm in the console that
   the device's last-inventoried timestamp updates.
7. **Negative test:** create a second discovery job against the same lab
   host IP address using an intentionally wrong SNMP community string.
   **Expected result:** the discovery job completes but reports the
   target as unauthenticated/unidentified rather than onboarding it,
   demonstrating that network reachability alone does not produce a
   managed device.
8. Attempt a device-control power action against the lab host through the
   API. **Expected result:** the action fails or is rejected, since a
   generic SNMP-discovered Linux host does not expose the out-of-band
   power-control interface that a real iDRAC-managed PowerEdge would —
   this illustrates the inventory/control fidelity gap between SNMP and
   native iDRAC discovery described in this chapter's theory section.

**Cleanup**

- In the OME console, remove the lab host from managed inventory and
  delete the `lab-snmp-devices` static group and the dynamic group
  created in step 5.
- Delete the discovery credential profile and both discovery jobs created
  during the lab.
- On the lab Linux host, disable and remove the SNMP agent if it is not
  needed for later chapters:

  ```bash
  sudo systemctl disable --now snmpd
  sudo apt-get remove -y snmpd
  ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter turned a bare, secured appliance into one actively managing
a fleet: it explained the discovery-to-onboarding-to-inventory pipeline,
the protocol tradeoffs between native iDRAC discovery and SNMP/IPMI paths
for third-party or legacy targets, and how static and dynamic groups
support both operational visibility and the scoped administration
established in [Chapter 2](02-identity-licensing-security-and-administrative-control.md). The lab exercised the full pipeline — discovery,
onboarding, grouping, inventory refresh, and device control — against a
reproducible SNMP-based lab target, including a negative test showing why
network reachability alone does not equal a managed device. With devices
under management, the volume now turns to monitoring, alerting, and
reporting on the fleet in [Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md).

- [ ] I can describe the discovery-to-onboarding-to-inventory pipeline and
      why onboarding, not raw discovery, is the gate to full functionality.
- [ ] I can select an appropriate discovery protocol for a given device
      class and explain the resulting inventory fidelity tradeoff.
- [ ] I designed and created both a static and a dynamic device group.
- [ ] I ran a discovery job, onboarded a device, and forced an
      out-of-cycle inventory refresh, including a negative test with
      invalid discovery credentials.
- [ ] I attempted a device-control action and can explain why its
      required interface differs by discovery protocol.
