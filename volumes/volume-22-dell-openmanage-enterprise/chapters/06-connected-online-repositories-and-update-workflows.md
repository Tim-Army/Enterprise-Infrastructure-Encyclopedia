# Chapter 06: Connected Online Repositories and Update Workflows

![Flow diagram showing a connected catalog manually refreshed with its timestamp advancing and a dependent baseline's compliance evaluation succeeding afterward, alongside a refresh that fails with a connectivity error when the appliance's proxy is pointed at an unreachable address.](../../../diagrams/volume-22-dell-openmanage-enterprise/chapter-06-connected-catalog-refresh-flow.svg)

*Figure 6-1. The connected catalog refresh flow exercised in this chapter's lab, including the broken-egress negative test.*

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

This chapter carries a topic-level walkthrough lab for **each connected-update task under "Server
Maintenance"** — online catalogs, scheduled refresh, SupportAssist-connected updates, and staged
rollout. Each lab pairs the console with `curl`. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 6.1–6.4** — a deployed OME appliance with outbound access to
`downloads.dell.com` (directly or via proxy), onboarded PowerEdge servers, and API credentials.
**Cost:** none. Chapter 07 covers the air-gapped alternative.

### Lab 6.1 — Online Dell catalog (Topic: Connected catalogs)

**Objective:** Use Dell's live online catalog as the version source.

```text
# Console: Configuration > Firmware/Driver Compliance > Catalog Management > Add
#   > "Latest component firmware versions on Dell.com" (online).
#   If behind a proxy: Application Settings > Network > Proxy, then validate the catalog downloads.
```

**Expected result:** OME pulls the current validated catalog directly from Dell — the online
catalog always reflects Dell's latest tested versions with no manual downloads, so baselines stay
current automatically; a proxy is the only extra step in a filtered network.

**Negative test:** point OME at the online catalog with outbound HTTPS blocked and no proxy; the
catalog fails to download — connected updates need reachability to `downloads.dell.com` (or the
Chapter 07 offline path).

**Cleanup:** none (keep the online catalog if desired).

### Lab 6.2 — Scheduled catalog refresh (Topic: Update currency)

**Objective:** Keep the catalog and compliance current automatically.

```text
# Console: on the online catalog, set an Update Schedule (e.g. weekly) so OME re-downloads
#   the catalog and re-evaluates baselines without manual action.
```

Verify the schedule via the job engine:

```bash
curl -sk -H "X-Auth-Token: $TOKEN" "https://<ome-ip>/api/JobService/Jobs?\$filter=JobType/Name eq 'Catalog_Refresh_Task'" 2>/dev/null | head
```

**Expected result:** a recurring catalog-refresh job keeps the catalog and compliance results
current — scheduling the refresh means new Dell firmware releases show up as compliance gaps
automatically, so you learn what needs updating without checking manually.

**Negative test:** load a catalog once and never refresh it; months later your "baseline" is stale
and misses critical firmware fixes — a scheduled refresh keeps the reference current.

**Cleanup:** remove the lab schedule if created only for the exercise.

### Lab 6.3 — SupportAssist-connected updates (Topic: Connected support)

**Objective:** Link OME to Dell for proactive, connected maintenance.

```text
# Console: Application Settings > Console and Plugins / SupportAssist Enterprise integration.
#   Register the appliance, confirm connectivity, and enable automated case creation for
#   hardware faults and connected firmware recommendations.
```

**Expected result:** OME reports telemetry to Dell and can auto-open support cases and surface
firmware recommendations — SupportAssist connects the fleet to Dell for proactive/predictive
support (automatic case creation, parts dispatch, tailored update guidance) beyond manual catalog
management.

**Negative test:** run disconnected with no SupportAssist; a predicted disk failure generates no
proactive case and you react only after the outage — the connected integration is what enables
proactive support.

**Cleanup:** deregister SupportAssist if enabled only for the lab.

### Lab 6.4 — Staged rollout workflow (Topic: Update workflow)

**Objective:** Roll updates through rings, not all at once.

```text
# Define rollout rings by group: canary (1-2 servers) -> ring 1 (non-critical) -> ring 2 (prod).
#   Update the canary, validate (health, workload), then promote to ring 1, then ring 2, each
#   in its own maintenance window.
```

**Expected result:** each ring updates and is validated before the next, so a bad update is caught
on the canary — a staged rollout limits blast radius: the canary and rings turn a risky fleet-wide
change into a validated, progressive one.

**Negative test:** push a new firmware release to all production servers the day it lands; an
undiscovered regression takes the fleet down together — ringed rollout with validation gates is
what prevents that.

**Cleanup:** none (leave devices at validated firmware).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

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
