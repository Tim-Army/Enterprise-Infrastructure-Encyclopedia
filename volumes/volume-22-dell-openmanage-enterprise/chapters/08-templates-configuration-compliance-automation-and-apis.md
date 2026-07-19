# Chapter 08: Templates, Configuration Compliance, Automation, and APIs

## Learning Objectives

- Explain how OME configuration templates capture, represent, and deploy
  server configuration state as a first-class, version-comparable object.
- Distinguish deployment templates from compliance templates and choose
  the right one for a given operational goal.
- Design a configuration compliance program that applies the
  baseline-and-drift pattern from [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md) to configuration rather than
  firmware.
- Automate template creation, deployment, and compliance evaluation
  through the REST API, including pagination and asynchronous job
  patterns used across the OME API surface.
- Diagnose common template deployment and compliance evaluation failures.

## Theory and Architecture

### Templates as captured configuration state

An OME **configuration template** is a structured, exportable
representation of a server's configurable settings — BIOS options, RAID
and storage controller configuration, NIC settings, iDRAC network and
management settings, boot order, and related attributes exposed through
each device's iDRAC. Templates are built on the same underlying
mechanism iDRAC itself uses for configuration export/import — the Server
Configuration Profile (SCP) — which OME wraps with fleet-scale
capture, storage, comparison, and deployment tooling. This is the same
architectural pattern the volume has used twice already for firmware: a
reference object (catalog in [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md), template here) that a device
population is evaluated against or deployed from, producing a
compliance or deployment result you can audit.

### Deployment templates vs. compliance use

A template can be created two ways: **captured from a reference
device** (an already-configured, known-good server whose current
settings become the template baseline) or **built from scratch** by
defining desired attribute values directly. Once created, the same
template object supports two distinct operational uses:

- **Deployment** — pushing the template's captured configuration onto one
  or more target devices, typically used for standardizing newly
  onboarded servers to a known configuration baseline before they enter
  production, or for bulk-remediating a fleet to a corrected setting.
- **Compliance evaluation** — comparing a device's *current* configuration
  against a template without changing anything, producing a drift report
  analogous to [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s firmware compliance report, but for
  configuration attributes instead of component versions.

This dual use is why templates are described as first-class objects
rather than one-shot deployment scripts: the same captured "what good
looks like" definition serves both provisioning new devices and detecting
drift on existing ones.

### License dependency

As established in [Chapter 2](02-identity-licensing-security-and-administrative-control.md), configuration templates and configuration
compliance are gated behind an OpenManage Enterprise Advanced (or
Advanced Plus) entitlement — the base license does not include this
capability. Confirm your appliance's license state before relying on this
chapter's workflows in a production environment; the API and console
paths described here will not function against an unlicensed appliance.

### Template scope and attribute editing

A captured template includes far more attributes than an administrator
typically wants to standardize verbatim across dissimilar hardware — a
template captured from one server includes that server's specific
hostname-adjacent iDRAC settings, for instance, which should not be
blindly pushed to every other device. OME's template editing surface lets
an administrator selectively include, exclude, or override specific
attributes before deployment, and supports identity-pool-backed
attributes (for settings like IP addresses or IQNs that must be unique
per device rather than copied verbatim) in more advanced deployment
scenarios. Understanding which attributes are safe to standardize
verbatim versus which require per-device handling is the central design
skill this chapter builds toward.

## Design Considerations

- **Reference device selection.** Capture templates from a genuinely
  representative, correctly configured device — a template inherits every
  quirk and misconfiguration of whatever device it was captured from, so
  capturing from an already-drifted or nonstandard server just
  standardizes the fleet on that server's mistakes.
  - **Attribute scope discipline.** Explicitly review and prune captured
  attributes before treating a template as a deployment or compliance
  source; leaving device-unique attributes (hostnames, static IPs, iDRAC
  network settings tied to a specific physical location) in a template
  meant for broad deployment is one of the most common template-design
  mistakes and can cause address conflicts or unreachable devices after
  deployment.
- **Deployment vs. compliance-only templates.** Some organizations
  deliberately maintain a template purely for compliance/drift detection
  (never deployed directly, treated as a read-only reference standard)
  separate from templates actively used for provisioning new hardware.
  Decide whether your organization needs this separation or whether a
  single template serving both purposes is sufficient for your fleet's
  homogeneity.
- **Identity pools for unique attributes.** For attributes that must be
  unique per device (IP addresses, iSCSI IQNs, MAC-adjacent identity
  settings in some configurations), plan an identity pool strategy rather
  than relying on manual per-device attribute overrides at deployment
  time — manual overrides do not scale and are a common source of
  deployment-time transcription errors.
- **Compliance remediation policy.** Decide, analogous to [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s
  firmware severity policy, how quickly configuration drift must be
  remediated once detected, and whether remediation is automatic
  (re-deploying the template to correct drift) or requires a change
  ticket and human approval given that configuration changes can be more
  behaviorally disruptive than a firmware update.
- **Automation and infrastructure-as-code alignment.** If your
  organization manages server configuration as code elsewhere (Ansible
  playbooks, Terraform, or similar, covered in [Volume IX](../../volume-09-infrastructure-automation/README.md)), decide how
  OME templates fit into that model — as the source of truth, as a
  downstream enforcement mechanism reflecting a source of truth defined
  elsewhere, or as a narrower safety net layered under a primarily
  code-driven process. Conflicting sources of truth between OME templates
  and an external IaC pipeline is a design risk worth resolving
  explicitly rather than discovering during an incident.

## Implementation and Automation

### Capturing a template from a reference device

```python
#!/usr/bin/env python3
"""ome_capture_template.py — create a configuration template captured
from a reference device.

Usage: python3 ome_capture_template.py <ome-host> <user> <password> \
    <reference-device-id> <template-name>
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


def capture_template(session, host, device_id, name):
    body = {
        "Name": name,
        "Description": "Captured from reference device via API",
        "TypeId": 2,  # deployment template type; confirm against your build
        "ViewTypeId": 2,
        "SourceDeviceId": device_id,
    }
    resp = session.post(
        f"https://{host}/api/TemplateService/Templates", json=body, verify=False
    )
    resp.raise_for_status()
    return resp.json()


def main():
    host, user, password, device_id, name = sys.argv[1:6]
    session = get_session(host, user, password)
    template = capture_template(session, host, int(device_id), name)
    print(f"Template capture job submitted for '{name}': {template}")


if __name__ == "__main__":
    main()
```

Template capture is asynchronous — it queues a job ([Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md)'s pattern)
that reads the reference device's current SCP-equivalent state; poll the
returned job before assuming the template is ready to view or deploy.

### Pruning attributes before deployment

```bash
# List a template's attributes to review before deployment.
curl -sk "https://<appliance>/api/TemplateService/Templates(<template-id>)/AttributeDetails" \
  -H "X-Auth-Token: <token>" | jq '.'

# Update specific attributes (for example, excluding a device-unique
# iDRAC network setting) before deployment.
curl -sk -X PUT "https://<appliance>/api/TemplateService/Templates(<template-id>)/AttributeDetails" \
  -H "X-Auth-Token: <token>" -H "Content-Type: application/json" \
  -d '{"Attributes": [{"Id": 12345, "IsIgnored": true}]}'
```

### Deploying a template to a device group

```python
def deploy_template(session, host, template_id, group_id):
    body = {
        "Id": 0,
        "JobName": f"deploy-template-{template_id}",
        "JobDescription": "API-orchestrated configuration deployment",
        "Targets": [
            {"Id": group_id, "TargetType": {"Id": 6000, "Name": "GROUP"}}
        ],
        "TemplateId": template_id,
        "Schedule": "RunNow",
    }
    resp = session.post(
        f"https://{host}/api/TemplateService/Actions/TemplateService.Deploy",
        json=body,
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()
```

### Running configuration compliance evaluation

```python
def check_config_compliance(session, host, template_id):
    resp = session.post(
        f"https://{host}/api/TemplateService/Templates({template_id})"
        "/Actions/TemplateService.CheckConfigurationCompliance",
        json={},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def get_compliance_detail(session, host, template_id):
    resp = session.get(
        f"https://{host}/api/TemplateService/Templates({template_id})/ComplianceReports",
        verify=False,
    )
    resp.raise_for_status()
    return resp.json().get("value", [])
```

As with the firmware update job payload in [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md), confirm exact
`TemplateService` action names, `TypeId`/`ViewTypeId` values, and
target-type identifiers against your build's live API reference — the
template and configuration compliance surface has been one of the more
actively developed parts of the OME API across 4.x releases.

### Handling pagination and OData filters at scale

Fleet-scale automation against OME's REST API needs to handle
server-side pagination correctly rather than assuming a single response
page contains every result:

```python
def get_all_pages(session, host, resource_path):
    """Follow @odata.nextLink until all pages are retrieved."""
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
```

Combine this with OData `$filter`, `$select`, and `$top` query parameters
(supported across most OME list resources) to keep large-fleet
automation efficient rather than always retrieving and filtering full
result sets client-side.

## Validation and Troubleshooting

- **Template deployment succeeds but a device becomes unreachable
  afterward.** This is the classic symptom of an unpruned, device-unique
  network attribute (a static IP or iDRAC network setting copied verbatim
  from the reference device) being deployed to a device that needed a
  different value — review the deployed attribute set against the
  Design Considerations guidance above before the next deployment
  attempt, and use the device's local/out-of-band console ([Volume XXIII](../../volume-23-dell-idrac-9-10-administration/README.md))
  to recover network access if needed.
- **Template capture job never completes.** Confirm the reference
  device's iDRAC is reachable and its Lifecycle Controller is not busy
  with another operation (a concurrent firmware update job, for example)
  — SCP export operations queue behind other Lifecycle Controller work on
  the same device rather than running in true parallel.
- **Configuration compliance reports drift on an attribute you did not
  expect to be tracked.** Check whether that attribute was left
  un-pruned in the template (Implementation and Automation's
  `AttributeDetails` pattern) — an unintentionally broad template will
  report every device as "non-compliant" on attributes that were never
  meant to be standardized in the first place.
- **Deployment job partially fails across a device group.** As with
  firmware update jobs, check per-device execution history rather than
  the job's rolled-up status; a common partial-failure cause is one or
  more target devices running a Lifecycle Controller version that
  rejects a specific attribute the template attempts to set.
- **License-gated 403/feature-unavailable responses.** Revisit Chapter
  2's license validation guidance — the most common root cause of
  template API calls failing outright on an otherwise healthy appliance
  is a missing or expired Advanced/Advanced Plus entitlement.

## Security and Best Practices

- Restrict template creation, editing, and deployment rights through role
  and scope ([Chapter 2](02-identity-licensing-security-and-administrative-control.md)) — a template deployment is a fleet-wide
  configuration-change capability and warrants the same access discipline
  as firmware update orchestration.
- Review captured templates for embedded secrets or sensitive
  configuration values (for example, SNMP community strings or
  service-account-adjacent settings sometimes captured as part of iDRAC
  configuration) before sharing template exports outside the immediate
  administrative team.
- Treat identity pools and any per-device unique attribute handling with
  the same rigor as IP address management elsewhere in your
  organization — a misconfigured identity pool can produce address
  conflicts across an entire deployment batch simultaneously.
- Version and change-control your organization's canonical templates the
  same way you would infrastructure-as-code definitions elsewhere,
  including a review step before a modified template is deployed broadly.
- Use compliance-only evaluation to validate a template's effect on a
  representative subset of devices before broad deployment, rather than
  deploying directly to an entire device group as the first real-world
  test of a newly captured or edited template.

## References and Knowledge Checks

**References**

- Dell Technologies, *OpenManage Enterprise User's Guide* — configuration
  templates and configuration compliance
- Dell Technologies, *OpenManage Enterprise RESTful API Guide* —
  TemplateService resources
- Dell Technologies, *iDRAC Server Configuration Profile (SCP) reference*
- `SOFTWARE_VERSIONS.md` in this repository for the dated 4.7.x baseline

**Knowledge Checks**

1. What is the relationship between an OME configuration template and an
   iDRAC Server Configuration Profile?
2. Why does capturing a template from a poorly configured reference
   device propagate that misconfiguration rather than correcting it?
3. Why is attribute pruning specifically important for network-adjacent
   settings before a template is deployed broadly?
4. What distinguishes deployment use of a template from compliance-only
   use, and why might an organization maintain both a deployment template
   and a separate compliance-only reference template?
5. Why must fleet-scale API automation against OME follow
   `@odata.nextLink` pagination rather than assuming one response page is
   complete?

## Hands-On Lab

**Objective:** Capture a configuration template from a reference device,
prune a device-unique attribute, run compliance evaluation against a
target group, and validate the results — using a compliance-only
workflow so the lab does not risk making an unreviewed configuration
change to a live device.

**Prerequisites**

- The OME appliance with an OpenManage Enterprise Advanced (or Advanced
  Plus) license imported ([Chapter 2](02-identity-licensing-security-and-administrative-control.md)) — this lab's core functionality is
  unavailable without it.
- At least one onboarded, iDRAC-managed reference device (a real or
  virtual PowerEdge/iDRAC target, consistent with [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s hardware
  requirement).
- Python 3.11+ with `requests` installed.

**Steps**

1. Confirm license status permits template operations
   (`GET /api/ApplicationService/License` or the equivalent resource for
   your build); stop and resolve licensing before proceeding if this
   check fails.
2. Capture a template from your reference device using the
   `ome_capture_template.py` script from Implementation and Automation:

   ```bash
   python3 ome_capture_template.py <appliance-ip> admin '<password>' \
     <reference-device-id> lab-config-template
   ```

   **Expected result:** the script reports a submitted capture job; poll
   it ([Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md)'s job-query pattern) until it completes successfully.
3. Retrieve the template's attribute list using the `AttributeDetails`
   endpoint shown in Implementation and Automation, and identify at least
   one device-unique attribute (a static IP-adjacent iDRAC network
   setting is a representative example).
4. Mark that attribute as ignored using the `PUT AttributeDetails`
   pattern shown above.
5. **Expected result:** re-querying `AttributeDetails` shows the
   attribute's `IsIgnored` flag set to `true`, confirming the prune took
   effect.
6. Run configuration compliance evaluation against your [Chapter 3](03-discovery-onboarding-inventory-groups-and-device-control.md) device
   group using the `check_config_compliance` function, and poll its
   associated job to completion.
7. Retrieve compliance detail using `get_compliance_detail` and confirm
   the pruned attribute from step 4 does **not** appear as a source of
   reported drift for any device, while other, non-pruned attributes are
   evaluated normally.
8. **Negative test:** attempt to run configuration compliance evaluation
   against a template ID that does not exist:

   ```bash
   curl -sk -X POST "https://<appliance-ip>/api/TemplateService/Templates(999999)/Actions/TemplateService.CheckConfigurationCompliance" \
     -H "X-Auth-Token: <token>" -H "Content-Type: application/json" -d '{}'
   ```

   **Expected result:** an HTTP 4xx error, confirming the API rejects
   evaluation against a nonexistent template rather than silently
   succeeding.

**Cleanup**

- Delete the `lab-config-template` template from OME if it is not needed
  for later exercises.
- No device configuration was changed during this lab, since it used
  compliance-only evaluation rather than deployment — confirm this by
  reviewing the reference device's configuration is unchanged from before
  the lab began.

## Summary and Completion Checklist

This chapter extended the catalog/baseline/compliance pattern the volume
established for firmware in Chapters 5–7 to server configuration:
templates capture SCP-equivalent configuration state from a reference
device or manual definition, support both deployment and compliance-only
use, and depend on the Advanced-tier licensing introduced in [Chapter 2](02-identity-licensing-security-and-administrative-control.md).
It covered the attribute-pruning discipline required before broad
deployment, identity pools for per-device-unique attributes, and
fleet-scale REST API patterns — pagination, OData filtering, and
asynchronous job polling — that apply across every OME automation surface
covered in this volume. The lab captured a real template, pruned an
attribute, and validated compliance evaluation without risking an
unreviewed configuration change. The volume's final chapter now covers
protecting and operating the OME appliance itself: backup, restore,
upgrade, and troubleshooting.

- [ ] I can explain the relationship between an OME template and an
      iDRAC Server Configuration Profile, and the license dependency
      that gates this capability.
- [ ] I can distinguish deployment use of a template from compliance-only
      evaluation.
- [ ] I captured a template from a reference device and pruned a
      device-unique attribute before further use.
- [ ] I ran configuration compliance evaluation and confirmed the pruned
      attribute was correctly excluded from drift reporting.
- [ ] I can explain why fleet-scale REST API automation must follow
      OData pagination rather than assuming single-page results.
