# Chapter 06: Connected Online Repositories and Update Workflows

## Learning Objectives

- Explain how OME's connected online catalog workflow retrieves and
  refreshes firmware and driver metadata from Dell's hosted repository.
- Configure outbound connectivity — direct or proxied — required for
  online catalog access, and validate it independently of any specific
  update operation.
- Schedule recurring catalog refreshes and understand how a refreshed
  catalog interacts with existing baselines.
- Automate connected-catalog operations (refresh, version inspection,
  baseline re-evaluation) through the REST API.
- Diagnose connectivity, proxy, and freshness failures specific to the
  online catalog path.

## Theory and Architecture

### The connected catalog source

Dell publishes a continuously maintained firmware and driver catalog for
supported PowerEdge platforms, hosted at `downloads.dell.com`. OME's
**connected (online) repository** workflow points a catalog definition at
this hosted source rather than at a locally imported file, so the catalog
metadata described in [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md) — which components, which versions, which
severity — updates automatically whenever Dell publishes new content and
the appliance refreshes.

This is the default and, for any OME appliance with outbound internet
access, the lowest-maintenance catalog sourcing model: an administrator
does not need to manually download, transfer, or import anything for the
catalog itself to stay current. [Chapter 7](07-isolated-offline-repositories-and-air-gapped-updates.md) covers the alternative —
offline, air-gapped repositories — for environments where the appliance
cannot reach `downloads.dell.com` at all.

### Catalog scope and variants

Dell's hosted catalog is not a single monolithic file; OME's connected
catalog configuration typically lets you select a scope such as the full
PowerEdge component catalog or a narrower subset, and separately lets you
choose whether a given baseline tracks the latest published catalog
automatically or is pinned to a specific catalog version captured at
baseline-creation time ([Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s currency-vs-stability design point).
The distinction matters operationally: "the online catalog" is really a
*source* that produces a new catalog version each time Dell publishes
updates, and OME's refresh operation is what pulls a new version of that
source into the appliance for baselines to evaluate against.

### Refresh mechanics

A connected catalog refresh is itself a **job** ([Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md)) with its own
execution history: the appliance reaches out to `downloads.dell.com` over
HTTPS, retrieves updated catalog metadata (and, later, the actual DUP
payloads referenced by that metadata when an update job needs them — the
catalog refresh itself is a metadata operation, not a bulk download of
every possible update package), and records a new catalog version
timestamp. Refreshes can run on demand or on a configured recurring
schedule; a baseline configured to track "latest" picks up the refreshed
catalog's content on its next compliance evaluation without any further
administrator action.

### Proxy and firewall dependency

Because the connected catalog workflow depends entirely on the appliance
reaching an external Dell-operated endpoint, its correct operation is
gated by whatever egress path the appliance has — direct internet access,
or a configured explicit web proxy (established during first-run setup in
[Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md), and adjustable afterward in application settings). Unlike most
of OME's other operations, which are entirely internal to the managed
network, this is the one workflow in the volume with a hard external
network dependency, which makes it worth validating independently of any
specific baseline or update job.

## Design Considerations

- **Refresh cadence.** A daily or weekly scheduled refresh is typical;
  align cadence to how quickly your organization wants newly published
  Dell content reflected in compliance reporting versus the (modest)
  background load and change-visibility churn a frequent refresh
  introduces. A refresh that is too infrequent risks compliance reports
  looking stale relative to what Dell has actually published; one that is
  too frequent adds little value beyond a reasonable daily cadence for
  most organizations.
- **Proxy authentication and egress scope.** If a proxy is required,
  confirm it permits the specific `downloads.dell.com` endpoint (and any
  related CDN or redirect targets Dell's catalog service uses) rather than
  assuming a general-purpose outbound proxy rule covers it — content
  delivery endpoints for large vendor catalogs are sometimes routed
  through infrastructure not covered by a narrowly scoped allow-list
  written for other purposes.
- **"Latest" vs. pinned baselines interact with refresh cadence.** A
  baseline tracking "latest" will silently reflect whatever the most
  recent refresh pulled in; if your organization requires change-approval
  before a new compliance target takes effect in production, pin
  baselines to a specific captured catalog version and treat refreshing
  *that pin* as a deliberate, change-controlled action rather than
  letting scheduled refreshes automatically shift production compliance
  targets.
- **Bandwidth and timing.** Schedule catalog refreshes (and any resulting
  bulk update-package downloads) outside of peak business-hours WAN
  utilization where the appliance shares egress capacity with other
  production traffic, particularly for sites with constrained internet
  circuits.
- **Multi-appliance consistency.** In a multi-appliance estate ([Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)'s
  single-vs-multiple-appliance design point), decide whether each
  appliance refreshes independently against Dell's hosted source
  (simpler, no cross-appliance dependency) or whether one appliance's
  catalog is exported and distributed to others for consistency (more
  operational overhead, but guarantees every appliance evaluates
  compliance against the identical catalog version at a given time).

## Implementation and Automation

### Verifying outbound catalog reachability

Before troubleshooting any specific baseline or update job, validate
connectivity to Dell's catalog source independently:

```bash
# From a host with the same egress path as the appliance (direct or via
# the same proxy), confirm HTTPS reachability.
curl -sI https://downloads.dell.com/ --max-time 15
```

A successful response (even a redirect) confirms name resolution and TLS
reachability along the expected path; a timeout or DNS failure here
isolates the problem to network/proxy configuration before you spend time
inspecting catalog or baseline objects inside OME itself.

### Configuring or updating the proxy from the REST API

```python
#!/usr/bin/env python3
"""ome_set_proxy.py — configure the appliance's outbound web proxy used
for reaching downloads.dell.com.

Usage: python3 ome_set_proxy.py <ome-host> <user> <password> \
    <proxy-host> <proxy-port> [proxy-user] [proxy-password]
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


def set_proxy(session, host, proxy_host, proxy_port, proxy_user=None, proxy_pass=None):
    body = {
        "IpAddress": proxy_host,
        "PortNumber": int(proxy_port),
        "EnableProxy": True,
        "EnableAuthentication": bool(proxy_user),
        "Username": proxy_user or "",
        "Password": proxy_pass or "",
    }
    resp = session.put(
        f"https://{host}/api/ApplicationService/Network/ProxyConfiguration",
        json=body,
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    args = sys.argv[1:]
    host, user, password, proxy_host, proxy_port = args[:5]
    proxy_user = args[5] if len(args) > 5 else None
    proxy_pass = args[6] if len(args) > 6 else None
    session = get_session(host, user, password)
    result = set_proxy(session, host, proxy_host, proxy_port, proxy_user, proxy_pass)
    print(f"Proxy configuration applied: {result}")


if __name__ == "__main__":
    main()
```

Confirm the exact proxy-configuration resource path against your build;
network and proxy settings have occasionally moved between
`ApplicationService/Network` sub-resources across OME releases.

### Triggering a connected catalog refresh

```bash
# List existing catalogs and identify the connected (online) one.
curl -sk https://<appliance>/api/UpdateService/Catalogs \
  -H "X-Auth-Token: <token>" | jq '.value[] | {Id, Repository: .Repository.Name, SourcePath}'

# Trigger a refresh of a specific catalog.
curl -sk -X POST "https://<appliance>/api/UpdateService/Catalogs(<catalog-id>)/Actions/UpdateService.RefreshCatalog" \
  -H "X-Auth-Token: <token>" -H "Content-Type: application/json" -d '{}'
```

```python
def refresh_and_wait(session, host, catalog_id, job_poll_fn, timeout_s=900):
    """Trigger a catalog refresh and poll its job to completion."""
    resp = session.post(
        f"https://{host}/api/UpdateService/Catalogs({catalog_id})/Actions/UpdateService.RefreshCatalog",
        json={},
        verify=False,
    )
    resp.raise_for_status()
    job_id = resp.json().get("JobId") or resp.json().get("Id")
    return job_poll_fn(session, host, job_id, timeout_s)
```

### Scheduling recurring refresh

Recurring catalog refresh is typically configured as a schedule attribute
on the catalog resource itself (a cron-like recurrence rule) rather than
as an externally triggered cron job — set it once from the console's
catalog management screen, or via the API by including a `Schedule` block
in the catalog's create/update payload, and confirm the exact schema
against your build's API reference.

### Re-evaluating dependent baselines after refresh

Once a refresh completes, any baseline configured to track "latest" for
that catalog should have compliance re-evaluated to reflect the new
content:

```python
def reevaluate_dependent_baselines(session, host, catalog_id):
    resp = session.get(f"https://{host}/api/UpdateService/Baselines", verify=False)
    resp.raise_for_status()
    for baseline in resp.json().get("value", []):
        if baseline.get("CatalogId") == catalog_id:
            session.post(
                f"https://{host}/api/UpdateService/Baselines({baseline['Id']})"
                "/Actions/UpdateService.CheckBaselineCompliance",
                json={},
                verify=False,
            )
            print(f"Re-evaluation triggered for baseline: {baseline.get('Name')}")
```

## Validation and Troubleshooting

- **Catalog refresh job fails with a connectivity error.** Run the direct
  `curl` reachability check shown above from a host sharing the
  appliance's egress path before assuming an OME-internal fault; DNS
  resolution failures and proxy authentication failures both present
  similarly in the job's error detail but require different fixes.
- **Refresh succeeds but compliance reports do not change.** Confirm the
  baseline in question is actually configured to track "latest" rather
  than a pinned catalog version — a pinned baseline will not reflect a
  refresh until it is deliberately re-pointed, which is expected behavior
  given the design considerations above, not a defect.
- **Refresh works from a browser on the same network but not from the
  appliance.** This points at a difference between the appliance's
  configured egress path (direct vs. proxy) and your test host's path;
  confirm the appliance's actual proxy configuration via the API (`GET`
  the proxy configuration resource) rather than assuming it matches what
  was set during first-run setup, since it may have been changed since.
- **Scheduled refresh appears to silently stop running.** Check the job
  history for the recurring refresh's most recent execution — a schedule
  definition surviving but its executions consistently failing (for
  example, after a proxy credential rotation) looks identical to "nothing
  happening" from the catalog's last-refreshed timestamp alone.
- **Update job fails to retrieve a specific package after a successful
  catalog metadata refresh.** Remember that metadata refresh and package
  retrieval are separate operations (Theory and Architecture, above); a
  metadata-only refresh succeeding does not guarantee every referenced
  package is retrievable if, for example, a narrower firewall rule
  permits the catalog index host but not every package download path.

## Security and Best Practices

- Restrict outbound access from the appliance to the specific endpoints
  required for the connected catalog (and, if used, SupportAssist)
  rather than granting broad internet egress, consistent with [Chapter 1](01-architecture-requirements-deployment-and-first-configuration.md)'s
  hardening guidance.
- Route catalog refresh traffic through a logged, policy-enforced proxy
  where your organization's egress policy requires it, and treat proxy
  credential rotation for this path with the same discipline as any other
  service account credential.
- Avoid disabling package signature verification ([Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)) as a
  workaround for catalog or proxy connectivity issues; fix the
  connectivity problem rather than weakening package integrity checking.
- Log and periodically review catalog refresh job history as part of
  routine operations, since a silently failing scheduled refresh
  degrades compliance reporting accuracy without an obvious alert unless
  you are specifically watching for it ([Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md)'s alert policies can be
  scoped to job-failure events for this purpose).
- If pinning baselines to specific catalog versions for change control,
  document and enforce the approval process for moving that pin forward,
  so "latest" drift does not creep in informally outside the documented
  process.

## References and Knowledge Checks

**References**

- [Dell Technologies, *OpenManage Enterprise User's Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4_5_online_help_user_guide/overview) — connected
  (online) repository configuration
- [Dell Technologies, *OpenManage Enterprise RESTful API Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_p_3.10_api_guide/preface) —
  UpdateService/Catalogs and ApplicationService/Network resources
- [Dell Technologies, *OpenManage Enterprise Installation and Deployment
  Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4_1_online_help_and_user_guide/deployment) — outbound connectivity and proxy requirements
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated 4.7.x baseline

**Knowledge Checks**

1. Why is validating direct reachability to `downloads.dell.com`
   independently useful before troubleshooting a specific catalog refresh
   job failure?
2. What is the practical difference between a baseline that tracks
   "latest" catalog content and one pinned to a specific captured catalog
   version?
3. Why might a catalog metadata refresh succeed while a subsequent update
   job still fails to retrieve a specific package?
4. In a multi-appliance estate, what tradeoff exists between each
   appliance refreshing independently versus distributing one appliance's
   catalog to the others?
5. Why should a scheduled catalog refresh's job history be monitored
   rather than trusted to "just work" indefinitely?

## Hands-On Lab

**Objective:** Validate outbound catalog connectivity independently,
configure or confirm the connected catalog source, trigger a manual
refresh, and observe its effect on a dependent baseline's compliance
evaluation.

**Prerequisites**

- The OME appliance from earlier chapters' labs, with outbound internet
  access (direct or via a reachable proxy) for this specific lab — this
  is the one lab in the volume that requires real internet egress from
  the appliance, since it exercises the connected catalog path by
  definition.
- The `lab-firmware-baseline` baseline from [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s lab, or a newly
  created one following the same pattern.
- Python 3.11+ with `requests` installed.

**Steps**

1. From a workstation sharing the appliance's egress path, validate
   direct reachability:

   ```bash
   curl -sI https://downloads.dell.com/ --max-time 15
   ```

   **Expected result:** a response (2xx or 3xx) rather than a timeout or
   connection error.
2. In the OME console (or via `GET /api/UpdateService/Catalogs`), confirm
   a connected (online) catalog is configured. If none exists, create one
   pointing at Dell's hosted PowerEdge catalog source through the
   console's catalog management screen, since initial catalog-source
   creation is most reliably done through the guided console workflow.
3. Note the catalog's current "last refreshed" timestamp before
   proceeding.
4. Trigger a manual refresh using the `RefreshCatalog` action shown in
   Implementation and Automation, and poll its job to completion using
   [Chapter 4](04-monitoring-alerts-reports-jobs-and-operational-integrations.md)'s job-query pattern.
5. **Expected result:** the job completes successfully, and the catalog's
   "last refreshed" timestamp advances past the value recorded in step 3.
6. Re-run compliance evaluation on the `lab-firmware-baseline` baseline
   ([Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s `CheckBaselineCompliance` action) and confirm it completes
   without error, referencing the newly refreshed catalog content.
7. **Negative test:** using the `ome_set_proxy.py` script from
   Implementation and Automation, deliberately set the proxy configuration
   to an unreachable host (for example, `192.0.2.1`, a reserved
   documentation-only address guaranteed not to respond), then attempt
   another catalog refresh.

   **Expected result:** the refresh job fails with a connectivity-related
   error, demonstrating that catalog refresh genuinely depends on working
   egress rather than succeeding from cached state.
8. Restore the correct proxy configuration (or disable the proxy if your
   lab environment uses direct egress) and confirm a subsequent refresh
   succeeds again.

**Cleanup**

- Confirm the appliance's proxy configuration is restored to its correct
  production/lab value from step 8 before ending the lab — leaving the
  unreachable proxy address in place will silently break every later
  chapter's catalog-dependent exercises.
- No other cleanup is required; the connected catalog itself is expected
  to remain configured for use in [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s baseline exercises and
  later chapters.

## Summary and Completion Checklist

This chapter went deep on the connected, online catalog sourcing model
introduced generically in [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md): how Dell's hosted repository at
`downloads.dell.com` feeds catalog metadata into OME, how refresh
operations and job scheduling keep that metadata current, and how the
appliance's outbound network path — direct or proxied — is a hard
dependency worth validating independently of any specific baseline or
update job failure. The lab validated connectivity, exercised a real
catalog refresh, and included a deliberate negative test breaking egress
to confirm the dependency is real rather than assumed. [Chapter 7](07-isolated-offline-repositories-and-air-gapped-updates.md) now
covers the alternative model for environments where this chapter's
internet dependency is not acceptable at all: fully offline, air-gapped
repositories.

- [ ] I can explain the relationship between the connected catalog source,
      scheduled refresh, and dependent baselines.
- [ ] I can distinguish catalog metadata refresh from update package
      retrieval as separate operations with separate failure modes.
- [ ] I validated outbound catalog connectivity independently of any
      specific OME operation.
- [ ] I triggered a manual catalog refresh and confirmed its effect on a
      dependent baseline's compliance evaluation.
- [ ] I performed a negative test breaking proxy connectivity and
      confirmed catalog refresh fails as expected, then restored working
      connectivity.
