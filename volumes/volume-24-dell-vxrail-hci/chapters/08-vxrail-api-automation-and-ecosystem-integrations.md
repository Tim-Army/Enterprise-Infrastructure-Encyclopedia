# Chapter 08: VxRail API, Automation, and Ecosystem Integrations

## Learning Objectives

- Authenticate to the VxRail API and retrieve cluster, host, and health
  state.
- Explain how the VxRail API relates to the vSphere API and which
  operations belong to which.
- Write idempotent automation against VxRail that is safe to run
  repeatedly.
- Evaluate the available automation surfaces — REST, Ansible, PowerCLI —
  and choose appropriately.
- Identify the ecosystem integrations that apply to a VxRail estate and
  what each is actually for.

## Theory and Architecture

### Two APIs, two domains

A VxRail cluster exposes two distinct programmatic surfaces, and knowing
which one owns an operation is most of the skill:

| Surface | Owns | Reach for it when |
| --- | --- | --- |
| **vSphere API** (and PowerCLI over it) | Virtual machines, storage policies, resource pools, permissions, networking you created | Automating anything running *on* the platform |
| **VxRail API** | Cluster composition, node lifecycle, system health, upgrade operations, appliance state | Automating anything *about* the platform |

The division mirrors [Chapter 04](04-vsphere-and-vsan-integration-and-the-division-of-management.md)'s
ownership table exactly, which is not a coincidence: the APIs are drawn
along the same line as the management responsibilities.

The practical consequence is that most day-to-day automation on a VxRail
estate is ordinary vSphere automation, and the VxRail API is reached for
less often but for higher-stakes operations. That ratio is worth
internalizing before building tooling — a team that reaches for the
VxRail API to do vSphere work will find it inconvenient, because it is
not what it is for.

### The VxRail API's shape

The VxRail API is a versioned REST API served by VxRail Manager,
authenticated with vCenter credentials, returning JSON. Endpoints are
versioned in the path, and different resources sit at different versions
— a resource may be at `v1` while another has advanced to `v3`.

**Do not assume a uniform version prefix across endpoints.** This is the
most common source of confusion for someone writing VxRail automation for
the first time: a script that works against one endpoint returns 404
against another not because the resource is absent but because the
version in the path is wrong for it.

Consult the VxRail API reference for the version of VxRail you are
running. The API documentation is version-specific and the endpoint
inventory grows between releases.

### Read operations, write operations, and asynchrony

Read operations are straightforward and safe: system information, cluster
composition, host inventory, health state, available updates.

Write operations — node addition, upgrade initiation, configuration
change — are long-running and asynchronous. They return a request or job
identifier rather than a result, and the actual outcome is discovered by
polling that identifier.

This shapes automation design substantially. A script that fires a write
operation and exits has not done the job; it has started it. Automation
around VxRail write operations needs to poll for completion, handle the
job failing, and — importantly — be safe to re-run when a human restarts
it after an ambiguous failure.

### Idempotence, and why it matters more here

Idempotence is good practice everywhere and close to mandatory here,
because VxRail write operations are slow, cluster-wide, and expensive to
get wrong.

The pattern that works: **query state, compare against desired state, act
only on the difference.** A script that unconditionally issues an
operation will, when re-run, issue it again. On a cluster where that
operation is "begin an upgrade" or "add a node", the second issuance is
not harmless.

The same discipline applies to the vSphere side of VxRail automation, and
[Volume IX](../../volume-09-infrastructure-automation/README.md) covers
the general principles this chapter applies to a specific platform.

### Automation surfaces

Three surfaces, with different strengths:

| Surface | Strengths | Use for |
| --- | --- | --- |
| **REST directly** (curl, Python `requests`) | Complete access; nothing hidden | Anything the higher-level tools do not cover; exploration |
| **Ansible** — Dell publishes a VxRail collection | Declarative, idempotent by construction, fits existing playbook estates | Repeatable operational tasks in an Ansible-based estate |
| **PowerCLI** | Excellent for the vSphere side; familiar to VMware administrators | The majority of day-to-day work, which is vSphere work |

Dell maintains an Ansible collection for VxRail alongside its
`dellemc.openmanage` collection covered in
[Volume XXIII, Chapter 09](../../volume-23-dell-idrac-9-10-administration/chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md).
Where an estate already runs Ansible, it is the natural surface. Where it
does not, adopting Ansible solely for VxRail is rarely worth it — direct
REST plus PowerCLI covers the ground.

### Ecosystem integrations

Several integrations surround a VxRail estate. What each is actually for:

- **Secure Connect Gateway / SupportAssist** — call-home telemetry and
  automated case creation for hardware faults. This is the same mechanism
  described in [Volume XXII, Chapter 04](../../volume-22-dell-openmanage-enterprise/chapters/04-monitoring-alerts-reports-jobs-and-operational-integrations.md)
  and it is the practical realization of the single-support-boundary
  benefit from Chapter 01. Without it, Dell learns about a failed drive
  when you tell them.
- **SmartFabric Services** — automated configuration of a supported Dell
  PowerSwitch fabric for VxRail, removing the manual switch work in
  [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md).
  Applicable only where the switching is Dell and supported.
- **vRealize / Aria and third-party monitoring** — VxRail health and
  hardware state can be surfaced into existing monitoring rather than
  living only in the vSphere Client, which matters for an operations team
  that does not live there.
- **VMware Cloud Foundation on VxRail** — a distinct product model in
  which SDDC Manager, rather than VxRail Manager alone, drives lifecycle
  across a full software-defined stack. It is a substantially different
  operational model rather than an add-on, and its availability and shape
  have moved with Broadcom's portfolio changes. Confirm current status
  and licensing directly with Dell and Broadcom before designing around
  it.

**A note on that last point.** The VMware portfolio has changed
substantially since the Broadcom acquisition, and integration
availability, product names, and licensing have moved with it. This
volume deliberately does not restate current licensing or bundling for
VMware-adjacent products, because that information has a short shelf life
and the cost of stating it wrongly is high. Verify with the vendors.

## Design Considerations

- **Use the API for reading far more than for writing.** Automated
  inventory, health collection, and drift detection are high value and
  low risk. Automated upgrades and node additions are neither, and the
  case for automating a twice-yearly operation is weak.
- **Never embed credentials in scripts.** VxRail API credentials are
  vCenter credentials, which are tier-0. Source them from a secret store
  or an interactive prompt.
- **Build automation that reports rather than acts, first.** A script
  that detects drift and reports it is useful on day one and safe.
  Promoting it to remediate later is a decision made with evidence.
- **Pin the API version explicitly.** Endpoint versions differ per
  resource and change across releases; a script that hardcodes a version
  it verified is more maintainable than one that assumes.
- **Prefer the vSphere API where an operation exists on both sides.**
  It is better documented, more stable, and more widely understood by the
  people who will maintain the script after you.
- **Enable call-home before you need it.** It is the mechanism by which
  the support model actually functions, and configuring it during an
  incident is the wrong time.

## Implementation and Automation

### 1. Authenticating and reading system state

```bash
# VxRail API access uses vCenter credentials. Source them; never embed.
read -r -s -p "VxRail API password: " VXM_PASS; echo
VXM_HOST="vxm-01.lab.example.com"
VXM_USER="administrator@vsphere.local"

# System information — the first call to make against any cluster.
curl -sk -u "${VXM_USER}:${VXM_PASS}" \
  "https://${VXM_HOST}/rest/vxm/v1/system" | jq .
```

The `-k` flag skips certificate verification and is present here because
a freshly deployed cluster carries self-signed certificates. **Remove it
once certificates have been replaced**, per
[Chapter 03](03-vxrail-manager-deployment-and-first-run-configuration.md)'s
guidance — leaving `-k` in permanent automation discards the
authentication the certificate provides.

### 2. Collecting inventory and health

```bash
# Cluster hosts, with their service tags — the identifier Dell support
# will ask for.
curl -sk -u "${VXM_USER}:${VXM_PASS}" \
  "https://${VXM_HOST}/rest/vxm/v1/hosts" |
  jq -r '.[] | [.sn, .hostname, .health, .operational_status] | @tsv'

# System health summary.
curl -sk -u "${VXM_USER}:${VXM_PASS}" \
  "https://${VXM_HOST}/rest/vxm/v1/system" |
  jq '{version: .version, health: .health, installed_time: .installed_time}'
```

Endpoint paths and field names vary across VxRail versions. Treat the
above as the shape of the interaction and confirm specifics against the
API reference for your release — a script written against documented
fields for your version is maintainable; one written against remembered
fields is not.

### 3. A drift-detection script that reports and does not act

This is the highest-value automation in the chapter, and it is entirely
read-only:

```python
#!/usr/bin/env python3
"""Report VxRail cluster drift against a recorded baseline.

Reads only. Exits non-zero when drift is found, so it can be scheduled
and alerted on.
"""
import json
import os
import sys
import time
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VXM = os.environ["VXM_HOST"]
AUTH = (os.environ["VXM_USER"], os.environ["VXM_PASS"])
BASELINE = "vxrail-baseline.json"
VERIFY = os.environ.get("VXM_CA_BUNDLE", False)


def get(path):
    r = requests.get(f"https://{VXM}{path}", auth=AUTH, verify=VERIFY, timeout=30)
    r.raise_for_status()
    return r.json()


def current_state():
    system = get("/rest/vxm/v1/system")
    hosts = get("/rest/vxm/v1/hosts")
    return {
        "version": system.get("version"),
        "health": system.get("health"),
        "hosts": sorted(
            {"sn": h.get("sn"), "hostname": h.get("hostname")} for h in hosts
        ),
    }


def main():
    state = current_state()

    if not os.path.exists(BASELINE):
        with open(BASELINE, "w") as fh:
            json.dump(state, fh, indent=2, sort_keys=True)
        print(f"Baseline written to {BASELINE}")
        return 0

    with open(BASELINE) as fh:
        baseline = json.load(fh)

    drift = []
    if state["version"] != baseline["version"]:
        drift.append(f"version: {baseline['version']} -> {state['version']}")
    if state["health"] != "Healthy":
        drift.append(f"health: {state['health']}")
    if state["hosts"] != baseline["hosts"]:
        drift.append("host inventory changed")

    if drift:
        for item in drift:
            print(f"DRIFT: {item}", file=sys.stderr)
        return 1

    print("No drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note `VERIFY` defaults to `False` but reads a CA bundle path from the
environment. Once certificates are replaced, setting `VXM_CA_BUNDLE`
turns verification on without editing the script — which is the
difference between a temporary compromise and a permanent one.

### 4. Handling an asynchronous write correctly

The pattern, expressed generically because the specific endpoint depends
on the operation:

```python
def run_and_wait(path, payload, timeout_s=7200, interval_s=30):
    """Start a long-running VxRail operation and poll to completion."""
    start = requests.post(
        f"https://{VXM}{path}", auth=AUTH, json=payload,
        verify=VERIFY, timeout=60,
    )
    start.raise_for_status()
    request_id = start.json()["request_id"]

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        status = get(f"/rest/vxm/v1/requests/{request_id}")
        state = status.get("state")
        if state in ("COMPLETED", "FAILED"):
            return status
        time.sleep(interval_s)

    raise TimeoutError(f"Request {request_id} did not complete in {timeout_s}s")
```

Two things this does that a naive version does not: it returns the failed
status rather than raising on it, so the caller can inspect *why*; and it
has a bounded timeout, so a stuck operation does not produce a script
that runs forever.

### 5. Combining both APIs in one report

Most useful automation crosses the boundary — platform state from VxRail,
workload state from vSphere:

```powershell
# vSphere side of a combined report.
Connect-VIServer -Server vcsa-01.lab.example.com

$report = Get-VMHost | ForEach-Object {
  [pscustomobject]@{
    Host      = $_.Name
    Build     = $_.Build
    State     = $_.ConnectionState
    VMs       = (Get-VM -Location $_).Count
    MemUsedPc = [math]::Round(($_.MemoryUsageGB / $_.MemoryTotalGB) * 100, 1)
  }
}
$report | Export-Csv "./vsphere-side-$(Get-Date -Format 'yyyy-MM-dd').csv" -NoTypeInformation
$report | Format-Table -AutoSize
```

Join this against the VxRail host inventory on service tag or hostname to
get a single view spanning hardware identity and workload placement —
which is the view an operations team actually wants and neither API
provides alone.

## Validation and Troubleshooting

### API returns 404 for an endpoint that exists

Almost always the version in the path. Different resources sit at
different API versions; check the reference for the correct version of
that specific endpoint rather than assuming the one that worked
elsewhere.

### API returns 401

Credentials are vCenter credentials. Confirm the account authenticates to
vCenter directly, and confirm it has sufficient privilege — an account
that can read vCenter may not be authorized for VxRail operations.

### Certificate errors after replacing certificates

Expected, and a sign the replacement worked. Automation carrying `-k` or
`verify=False` will keep working and keep discarding the benefit; this is
the moment to point it at the CA bundle instead.

### A long-running operation appears stuck

Distinguish "slow" from "stuck" before acting. The operations in this API
are genuinely long — an upgrade runs for hours, as
[Chapter 06](06-lifecycle-management-and-the-continuously-validated-state.md)
established. Poll the request status and check whether it is advancing
through stages. A request whose state has not changed over a long
interval, on a cluster whose hosts are not changing, is a support case
rather than something to cancel and retry.

### Automation that worked before an upgrade fails after

Endpoint versions and field names change across VxRail releases. This is
the argument for pinning versions explicitly and for testing automation
after a bundle upgrade as part of the upgrade's validation, rather than
discovering it at the next scheduled run.

## Security and Best Practices

- **Source credentials from a secret store, never from the script.**
  VxRail API credentials are vCenter credentials with cluster-wide reach.
- **Use a dedicated service account with the minimum privilege the
  automation needs**, rather than the administrator account. Read-only
  automation should authenticate as a read-only account, which makes the
  drift detector above safe by construction rather than by intent.
- **Restore certificate verification once certificates are replaced.**
  `verify=False` in permanent automation is an unauthenticated connection
  to a tier-0 system.
- **Log what automation did, with request identifiers.** When a write
  operation is investigated later, the request identifier is what ties
  the script's action to VxRail's own record of it.
- **Keep automation in version control and review changes to it.** A
  script with cluster-wide write access deserves the same review as the
  change it performs.
- **Enable call-home and verify it works.** Test that a case actually
  gets raised, rather than assuming the integration functions because it
  is configured.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — the VxRail API reference, which is version-specific and authoritative
  for endpoints, versions, and field names.
- [Volume IX](../../volume-09-infrastructure-automation/README.md)
  — general automation principles, idempotence, and secret handling that
  this chapter applies to a specific platform.
- [Volume XXIII, Chapter 09](../../volume-23-dell-idrac-9-10-administration/chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md)
  — Dell's automation ecosystem and the `dellemc` Ansible collections.
- [Volume V, Chapter 09](../../volume-05-vmware-virtualization/chapters/09-vsphere-lifecycle-automation-observability-and-troubleshooting.md)
  — PowerCLI and vSphere automation, which is most VxRail automation.

**Knowledge checks**

1. An operation needs to change a VM's storage policy. Which API, and
   why?
2. Why does a VxRail write operation return a request identifier rather
   than a result, and what must automation do about it?
3. A script that works against `/rest/vxm/v1/system` returns 404 against
   another endpoint. What is the most likely cause?
4. Why is `verify=False` acceptable on a freshly deployed cluster and not
   acceptable six months later?
5. Explain why a drift-detection script is better automation to build
   first than an upgrade-automation script.

## Hands-On Lab

**Objective:** Build a read-only drift detector and a combined platform
and workload report, exercising idempotence and safe credential handling.

**Prerequisites:** Python 3 with `requests`, PowerCLI, and a vSphere
environment from [Volume V](../../volume-05-vmware-virtualization/README.md).

**The VxRail API cannot be reached without VxRail.** For the VxRail half
of this lab, work against the API reference documentation and build the
script's structure, credential handling, and error paths — then exercise
the identical patterns against the vSphere API, which is reachable. The
skills that transfer are the ones the lab can teach: idempotent design,
polling asynchronous operations, and never embedding secrets.

**Procedure**

1. Write the drift-detection script from *Implementation and Automation*,
   adapting `current_state()` to read from the vSphere API via `pyvmomi`
   or by shelling out to PowerCLI. Keep the baseline-write-on-first-run
   behavior.
2. Run it once to establish the baseline. Confirm it exits zero and
   writes the baseline file.
3. Run it again unchanged. Confirm it exits zero and reports no drift —
   this is the idempotence check.
4. Change something it monitors: add a host, or change a build. Run again
   and confirm it exits non-zero and names the change.
5. Build the combined report by joining the PowerCLI host output against
   your inventory source on hostname.
6. Move credentials out of the environment into a prompt or a secret
   store, and confirm the script still works with no secret anywhere in
   the file.

**Negative test**

7. Point the script at an unreachable host and confirm it fails clearly
   with a timeout rather than hanging indefinitely. If it hangs, the
   `timeout=` parameters are missing — add them. This is the failure mode
   that turns a scheduled job into a stuck job.
8. Supply deliberately wrong credentials and confirm the script reports
   an authentication failure distinguishable from a connectivity failure.
   Automation that cannot tell these apart generates useless alerts.

**Expected results**

- A script that is safe to run repeatedly and detects real change.
- Clear, distinguishable failures for unreachable, unauthorized, and
  drifted conditions.
- No credential present in any file under version control.

**Cleanup**

9. Revert any environment change made in step 4, and retain the script —
   [Chapter 09](09-day-2-operations-troubleshooting-support-and-capstone.md)
   builds it into a day-2 operations routine.

## Summary and Completion Checklist

VxRail exposes two APIs along the same line that divides management
responsibility: vSphere for what runs on the platform, VxRail for the
platform itself — and most automation on a VxRail estate is ordinary
vSphere automation. VxRail's write operations are long-running and
asynchronous, returning request identifiers rather than results, which
makes polling, bounded timeouts, and idempotence structural requirements
rather than good practice. The highest-value automation to build first is
read-only drift detection, which is useful immediately and cannot cause
harm. Around the API sit the ecosystem integrations, of which call-home
matters most because it is the mechanism that makes the single support
boundary function in practice.

- [ ] Can route an operation to the correct API and justify the choice.
- [ ] Can authenticate to the VxRail API without embedding credentials.
- [ ] Writes automation that polls asynchronous operations with bounded
      timeouts.
- [ ] Builds idempotent scripts that compare state before acting.
- [ ] Knows to restore certificate verification once certificates are
      replaced.
- [ ] Has call-home configured and has verified it actually raises a
      case.
