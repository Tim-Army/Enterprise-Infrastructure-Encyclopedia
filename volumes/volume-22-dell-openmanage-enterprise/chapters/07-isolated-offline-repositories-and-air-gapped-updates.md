# Chapter 07: Isolated Offline Repositories and Air-Gapped Updates

![Flow diagram showing a synthetic offline catalog export verified by checksum, hosted over HTTP, and registered in OME as a custom catalog, alongside a deliberately corrupted package file that the checksum verification catches and reports as failed.](../../../diagrams/volume-22-dell-openmanage-enterprise/chapter-07-offline-catalog-integrity-flow.svg)

*Figure 7-1. The offline catalog transfer-integrity and registration flow exercised in this chapter's lab, including the tampered-file negative test.*

## Learning Objectives

- Explain why and when an offline (disconnected) firmware repository
  model is required instead of [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s connected online catalog.
- Describe the role of Dell Repository Manager (DRM) in building custom
  and offline-exportable catalogs outside of a live OME appliance.
- Design a secure transfer and hosting process for moving catalog content
  into an air-gapped or otherwise network-isolated OME environment.
- Configure OME to consume a local or network-share-hosted custom catalog
  and validate it functions identically to a connected catalog for
  baseline and compliance purposes.
- Diagnose common failures specific to offline catalog hosting and
  transfer integrity.

## Theory and Architecture

### Why offline repositories exist

[Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s connected catalog model assumes the OME appliance can reach
`downloads.dell.com` directly or through a permitted proxy. Many
enterprise environments — classified or regulated networks, industrial
control system enclaves, disconnected edge sites, or any environment
where policy simply prohibits management-plane internet egress — cannot
make that assumption. OME's **offline (isolated) repository** model
exists for exactly this case: it separates catalog *creation* (which
requires internet access, but not from the OME appliance itself) from
catalog *consumption* (which the appliance performs entirely against
locally or network-hosted content, with no outbound dependency).

### Dell Repository Manager

**Dell Repository Manager (DRM)** is a separate, Windows-based Dell tool
used to build both custom catalogs (a curated subset of available
firmware/driver packages, useful even in connected environments for
change-controlled currency) and fully offline-exportable repositories.
DRM itself typically runs on a workstation or jump host that *does* have
internet access to Dell's package sources, and its output — a catalog
file plus the referenced DUP packages, organized in the directory
structure OME expects — is what gets transferred into the isolated
environment. DRM is conceptually the offline equivalent of [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s
`downloads.dell.com` connected source: both ultimately produce the same
catalog-plus-packages structure that OME's UpdateService consumes; they
differ only in how that structure reaches the appliance.

### Repository structure and integrity

A DRM-exported offline repository is a self-contained set of files: a
catalog index (commonly XML-based) describing available packages, their
target models/components, versions, and severity — structurally
equivalent in purpose to the metadata [Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md) and 6 described for the
connected catalog — alongside the actual DUP binaries the catalog index
references. OME validates catalog and package integrity ([Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md)'s
signature verification) regardless of source, so a tampered or
incompletely transferred offline repository is rejected the same way a
corrupted connected-catalog download would be, rather than being trusted
implicitly because it arrived out-of-band.

### Hosting models for the isolated environment

Once transferred into the air-gapped network, the repository content
needs to be reachable by the OME appliance over a protocol it supports
for a "custom catalog" source — commonly a network file share (CIFS/SMB
or NFS) or an internal HTTP/HTTPS server hosting the exported directory
structure. OME references this location as a **custom repository** source
in its catalog configuration, functionally parallel to the connected
source from [Chapter 6](06-connected-online-repositories-and-update-workflows.md) but pointed at a location entirely inside the
isolated network rather than at Dell's hosted endpoint.

## Design Considerations

- **Transfer medium and chain of custody.** Decide how content crosses
  the air gap — removable media (with your organization's required
  scanning/sanitization process), a mediated one-way data diode, or a
  controlled file-transfer gateway — and document the chain of custody
  for what was transferred, when, and by whom, consistent with whatever
  change-control and media-handling policy governs the isolated
  environment. This is as much a compliance artifact as a technical step
  in many regulated environments.
- **Refresh cadence is a manual process now.** Unlike [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s
  scheduled automatic refresh, an offline repository's currency is
  gated entirely by how often someone runs DRM, exports new content, and
  repeats the transfer process. Define an explicit cadence (monthly or
  quarterly is common for disconnected environments prioritizing
  stability) rather than leaving it ad hoc, and track the offline
  repository's effective "as-of" date the same way you would track any
  other point-in-time compliance artifact.
- **Custom catalog scope.** DRM lets you curate exactly which
  models/components/versions are included rather than exporting Dell's
  entire hosted catalog. For a disconnected environment with a known,
  fixed hardware population, scoping the export to only the relevant
  PowerEdge models materially reduces transfer size and simplifies
  validation versus exporting the full catalog.
- **Hosting location redundancy.** Decide whether the internal
  file-share or HTTP host serving the repository to OME is itself a
  single point of failure for firmware operations in the isolated
  environment, and whether that risk warrants a redundant or
  backed-up hosting location, particularly if the isolated environment
  has its own high-availability expectations independent of OME.
- **Verification before trust.** Establish a documented checksum or
  signature verification step performed on the transferred content
  *before* pointing OME at it, not relying solely on OME's own
  package-level signature verification as the only integrity gate for
  content that crossed a security boundary.

## Implementation and Automation

### Building an offline repository with Dell Repository Manager

DRM's export workflow (run from a connected workstation, not the OME
appliance) typically follows this pattern:

1. Install DRM on a Windows workstation or jump host with internet access
   to Dell's package sources.
2. Create a new repository, selecting the target PowerEdge models and
   component categories relevant to your isolated environment's actual
   hardware inventory.
3. Choose the **Deployment Type: Repository Manager Repository** (or the
   equivalent offline/custom-catalog export option in your DRM version)
   rather than a format intended for direct DRM-to-appliance connected
   use.
4. Export the repository to a local directory. DRM produces a catalog
   file and a structured set of downloaded DUP packages.
5. Package the exported directory for transfer (a checksummed archive is
   a reasonable practice) and move it across the air gap through your
   organization's approved transfer process.

Exact menu labels and export format names have varied across DRM
versions; confirm the current workflow against the DRM documentation
matching the version in use, and validate the export against a non-
production OME instance before relying on it in the isolated production
environment for the first time.

### Verifying transferred content integrity

```bash
# On the source (connected) side, before transfer: generate a manifest.
find ./drm-export -type f -exec sha256sum {} \; > drm-export.sha256

# On the destination (isolated) side, after transfer: verify.
sha256sum -c drm-export.sha256
```

Only proceed with configuring OME against the transferred content after
this verification step passes cleanly — any mismatch indicates
corruption or tampering during transfer and should halt the process
pending investigation, not be silently ignored.

### Hosting the repository for OME consumption

A minimal, reproducible way to host the transferred content for OME
inside the isolated network is a simple internal HTTP server pointed at
the exported directory:

```bash
# Example: host the transferred DRM export over HTTP for OME to consume.
cd /srv/drm-export
python3 -m http.server 8080 --bind 0.0.0.0
```

A production isolated environment would typically use a persistent,
access-controlled web server (or an existing internal file share) rather
than an ad hoc `http.server` process; the command above is shown for its
clarity in a lab context and is revisited in the Hands-On Lab.

### Registering the offline repository as a custom catalog in OME

```python
#!/usr/bin/env python3
"""ome_add_custom_catalog.py — register a locally/network-hosted custom
catalog (an offline DRM export) as an OME catalog source.

Usage: python3 ome_add_custom_catalog.py <ome-host> <user> <password> \
    <catalog-name> <source-path>

<source-path> is the HTTP(S) URL, or the UNC/NFS path in the format your
OME build expects for a share-hosted custom catalog.
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


def add_custom_catalog(session, host, name, source_path):
    body = {
        "Filename": name,
        "SourcePath": source_path,
        "Repository": {
            "Name": name,
            "Description": "Offline/air-gapped custom catalog (DRM export)",
            "RepositoryType": "NFS_NETWORK_SHARE",  # or HTTP/CIFS depending on build
            "Source": source_path,
            "CheckCertificate": False,
        },
    }
    resp = session.post(
        f"https://{host}/api/UpdateService/Catalogs", json=body, verify=False
    )
    resp.raise_for_status()
    return resp.json()


def main():
    host, user, password, name, source_path = sys.argv[1:6]
    session = get_session(host, user, password)
    catalog = add_custom_catalog(session, host, name, source_path)
    print(f"Registered custom catalog '{name}' (Id={catalog.get('Id', 'pending')})")


if __name__ == "__main__":
    main()
```

`RepositoryType` values and the exact custom-catalog payload shape are
among the more build-specific parts of the UpdateService API, since OME
has supported an evolving set of custom-repository hosting types
(network share variants, HTTP/HTTPS, and direct file upload in some
releases). Validate the current schema against your appliance's live API
reference, and treat this script as a starting pattern rather than a
drop-in for every build.

## Validation and Troubleshooting

- **OME cannot reach the custom catalog source.** Confirm basic network
  reachability from the appliance to the hosting share or HTTP endpoint
  first (the isolated-network equivalent of [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s direct
  reachability check), including any authentication required by a CIFS
  share or HTTP basic-auth front end.
- **Catalog registers but shows zero packages.** This commonly indicates
  the source path points at the wrong directory level relative to what
  OME expects (for example, pointing at the export's parent directory
  instead of the directory containing the actual catalog index file);
  re-check the DRM export's directory structure against your custom
  catalog source path.
- **Checksum verification fails after transfer.** Treat this as a hard
  stop, not a warning — do not register a catalog whose transfer
  integrity could not be confirmed. Re-transfer from the verified source
  side rather than attempting to selectively repair the destination
  copy.
- **Compliance evaluation against the custom catalog reports
  unexpectedly few devices as needing updates.** Confirm the DRM export's
  scoped model/component selection actually covers your fleet's hardware
  population — a custom catalog scoped narrowly during export (Design
  Considerations, above) will legitimately show fewer applicable updates
  than the full connected catalog would, which is expected, not a fault.
- **Package retrieval fails during an update job even though the catalog
  index loaded successfully.** As in [Chapter 6](06-connected-online-repositories-and-update-workflows.md), catalog metadata and
  package retrieval are separate steps; confirm the actual DUP package
  files, not just the catalog index, were fully transferred and are
  present at the expected relative path under the hosting location.

## Security and Best Practices

- Treat the air-gap transfer process itself as a security control, not
  merely a logistics step — scan removable media per your organization's
  policy, and log every transfer with what was moved, by whom, and when.
- Verify content integrity (checksums, and package signatures once
  imported into OME) before trusting transferred content, and halt on any
  mismatch rather than proceeding with a "probably fine" assumption.
- Restrict who can build and export DRM repositories and who can
  register a custom catalog in the isolated OME appliance — this is a
  supply-chain control point for firmware entering a sensitive network,
  and should be scoped as tightly as any other change to that network's
  trusted software supply.
- Keep the DRM workstation itself appropriately hardened and monitored;
  it is the connected system with the most direct influence over what
  firmware content eventually reaches the isolated environment.
- Document and retain the offline repository's build provenance (DRM
  version, export date, source package versions) as part of your
  organization's software bill-of-materials or change-control record for
  the isolated environment, since this content did not arrive through an
  auditable, always-current connected path the way [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s catalog
  does.
- Do not disable OME's package signature verification to work around an
  offline-repository integration issue; resolve the underlying transfer
  or hosting problem instead.

## References and Knowledge Checks

**References**

- [Dell Technologies, *Dell Repository Manager User's Guide*](https://www.dell.com/support/manuals/en-us/repository-manager/drm_3.4.7_ug/about-dell-repository-manager)
- [Dell Technologies, *OpenManage Enterprise User's Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_4_5_online_help_user_guide/overview) — custom/
  isolated repository configuration
- [Dell Technologies, *OpenManage Enterprise RESTful API Guide*](https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/ome_p_3.10_api_guide/preface) —
  UpdateService/Catalogs custom repository resources
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated 4.7.x baseline

**Knowledge Checks**

1. Why does Dell Repository Manager typically run on a separate,
   internet-connected workstation rather than on the OME appliance
   itself?
2. What is the practical tradeoff of scoping a DRM export to a curated
   subset of models/components rather than exporting Dell's full catalog?
3. Why should transfer integrity be verified with a checksum step before
   registering a custom catalog, even though OME independently verifies
   package signatures?
4. Why does an offline repository's currency require an explicit,
   organization-defined refresh cadence rather than relying on OME's
   scheduled refresh behavior from [Chapter 6](06-connected-online-repositories-and-update-workflows.md)?
5. Why might a custom catalog register successfully in OME but report
   unexpectedly few applicable updates for your fleet?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each air-gapped-update task under "Server
Maintenance"** — building an offline repository, hosting it, pointing OME at it, and validating an
air-gapped update. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.4** — a workstation with **Dell Repository Manager (DRM)**
and internet access (outside the air gap), a file share (HTTP/CIFS/NFS) reachable by OME inside the
air gap, and a deployed OME appliance with onboarded servers. **Cost:** none.

### Lab 7.1 — Build an offline repository with DRM (Topic: Offline repository)

**Objective:** Export a validated catalog + DUPs for the air gap.

```text
# On an internet-connected workstation, in Dell Repository Manager (DRM):
#   - create a repository scoped to your models (e.g. R760, R660)
#   - base it on the Dell online catalog
#   - export the deployment repository (catalog XML + Dell Update Packages) to a folder
```

**Expected result:** a self-contained folder with a catalog file and the DUPs for your models —
DRM curates exactly the firmware your fleet needs into a portable repository, so an air-gapped OME
can update from Dell-validated content without any internet access.

**Negative test:** copy random individual DUPs into a folder without DRM's catalog; OME has no
version reference and cannot evaluate compliance — the exported **catalog** is what makes the
offline content usable as a baseline.

**Cleanup:** none (retain the repository for the update).

### Lab 7.2 — Host the offline catalog (Topic: Repository hosting)

**Objective:** Make the repository reachable inside the air gap.

```bash
# Transfer the DRM export across the air gap, then host it on a share OME can reach:
#   HTTP (example): serve the folder
cd /srv/dell-repo && python3 -m http.server 8080 &     # or a real web server / CIFS / NFS
curl -sI http://<repo-host>:8080/catalog.xml | head -1  # confirm it is served
```

**Expected result:** the catalog and DUPs are reachable over HTTP/CIFS/NFS from inside the air gap
— OME consumes an offline catalog from a network share, so the repository must be hosted on a
path the appliance can reach on the isolated network.

**Negative test:** leave the repository on the DRM workstation outside the air gap; OME cannot
reach it — the content must be transferred in and hosted on the isolated network.

**Cleanup:** stop the lab web server (`kill %1`).

### Lab 7.3 — Point OME at the offline catalog (Topic: Offline catalogs)

**Objective:** Register the air-gapped repository as a catalog.

```text
# Console: Configuration > Firmware/Driver Compliance > Catalog Management > Add
#   > catalog source = "Network Path" > enter the share URL/UNC and credentials.
#   Validate that OME downloads/parses the offline catalog, then build a baseline from it.
```

**Expected result:** OME registers the offline catalog and evaluates baselines against it, exactly
as with the online catalog — the update model (catalog → baseline → compliance → update) is
identical; only the catalog *source* changes for an air-gapped fleet.

**Negative test:** enter the network path with wrong credentials or an unreachable host; catalog
validation fails — the offline catalog must be reachable and authenticated like any other source.

**Cleanup:** remove the lab offline catalog if created only for the exercise.

### Lab 7.4 — Air-gapped update and validation (Topic: Air-gapped updates)

**Objective:** Update from the offline catalog and prove it worked without internet.

```bash
# Console: build a baseline on the offline catalog, run compliance, and update a canary
#   from the air-gapped DUPs. Then confirm via the API that the job succeeded:
curl -sk -H "X-Auth-Token: $TOKEN" "https://<ome-ip>/api/JobService/Jobs?\$filter=JobType/Name eq 'Firmware_Task'" 2>/dev/null | \
  python3 -c "import json,sys; [print(j['JobName'], j['LastRunStatus']['Name']) for j in json.load(sys.stdin)['value'][:5]]"
```

**Expected result:** the canary updates from the offline DUPs and the firmware job reports success
with no outbound internet — this proves the air-gapped workflow end to end: DRM export → transfer
→ host → offline catalog → baseline → update, entirely inside the isolated network.

**Negative test:** assume the air-gapped fleet will "just get updates"; with no DRM pipeline it
falls behind on critical firmware — an isolated network needs the deliberate DRM offline workflow
to stay current.

**Cleanup:** none (leave the canary at the updated firmware).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter covered the offline, air-gapped alternative to [Chapter 6](06-connected-online-repositories-and-update-workflows.md)'s
connected catalog model: how Dell Repository Manager separates
internet-connected catalog *building* from disconnected OME catalog
*consumption*, how transferred content must be integrity-verified before
being trusted, and how a custom catalog source — hosted on an internal
file share or HTTP endpoint — lets an isolated OME appliance evaluate
firmware compliance with the same baseline and compliance mechanics from
[Chapter 5](05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md), entirely without internet access. The lab exercised the full
transfer-verify-host-register workflow using a reproducible synthetic
export, including a deliberate integrity-failure negative test. With both
catalog sourcing models covered, the volume turns next to extending the
baseline-and-compliance pattern from firmware to configuration through
templates.

- [ ] I can explain why DRM runs separately from the OME appliance and
      what it produces for offline consumption.
- [ ] I can describe the transfer-integrity verification step and why it
      matters independently of OME's own package signature verification.
- [ ] I hosted a synthetic offline repository export and registered it in
      OME as a custom catalog.
- [ ] I performed a negative test demonstrating that transfer corruption
      is detected before content is trusted.
- [ ] I can explain why offline repository currency depends on an
      explicit, organization-defined refresh cadence.
