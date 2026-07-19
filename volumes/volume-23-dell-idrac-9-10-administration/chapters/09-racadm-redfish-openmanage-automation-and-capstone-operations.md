# Chapter 09: RACADM, Redfish, OpenManage, Automation, and Capstone Operations

![Flow diagram showing a full provisioning runbook combining network, identity, storage, and firmware baselines from every prior chapter into a Virtual Media OS deployment recorded end to end in the Lifecycle Log, with the Virtual Media fail-safe from Chapter 5 re-verified inside the combined sequence.](../../diagrams/volume-23-dell-idrac-9-10-administration/chapter-09-capstone-provisioning-runbook-flow.svg)

*Figure 9-1. The capstone provisioning runbook exercised in this chapter's lab, including the re-verified Virtual Media negative test.*

## Learning Objectives

- Compare RACADM, Redfish, and WS-Management as iDRAC automation
  interfaces and choose the right one for a given tool or pipeline.
- Build idempotent automation against iDRAC using Python and the Redfish
  API, applying the session-token authentication pattern used elsewhere in
  this encyclopedia.
- Use the `dellemc.openmanage` Ansible collection to express iDRAC
  configuration as declarative, version-controlled automation.
- Explain how single-server iDRAC automation composes with fleet-scale
  OpenManage Enterprise workflows ([Volume XXII](../../volume-22-dell-openmanage-enterprise/README.md)) rather than duplicating
  them.
- Execute a capstone runbook that provisions a server end to end —
  network, identity, storage, firmware baseline, and OS deployment —
  using only the tools and patterns from this volume.

## Theory and Architecture

### Three automation interfaces, one underlying controller

Every capability covered in this volume is reachable through three
interfaces, and understanding their relationship — rather than treating
them as competing, unrelated tools — is the foundation of good iDRAC
automation:

- **RACADM** — a command-line interface, usable locally (via SSH or the
  local RACADM utility on a host with OpenManage tools installed) or
  remotely, that has existed across every iDRAC generation this volume
  covers. RACADM's attribute-group model (`iDRAC.NIC.Selection`,
  `iDRAC.IPv4.Address`, and so on, used throughout this volume) predates
  Redfish's adoption and remains the most complete single interface for
  some legacy or deeply platform-specific settings, though on current
  firmware RACADM increasingly operates as a client that itself issues
  Redfish calls underneath, rather than a wholly independent code path.
- **Redfish** — the DMTF-standard, HTTP/JSON RESTful API this volume has
  used for every scripted example, and Dell's clearly stated strategic
  direction for iDRAC automation. Redfish's schema-driven, discoverable
  design (every resource links to related resources, and
  `/redfish/v1/$metadata` documents the schema) makes it substantially
  better suited than RACADM to generic tooling, cross-vendor automation
  frameworks, and long-term automation investment.
- **WS-Management (WSMAN)** — an older SOAP-based management protocol
  that iDRAC has supported for backward compatibility with tooling
  written before Redfish's adoption. New automation should not target
  WSMAN directly; it is mentioned here only because you may encounter it
  in legacy scripts or in OpenManage Enterprise's own internal
  communication with older-firmware iDRACs ([Volume XXII, Chapter 1](../../volume-22-dell-openmanage-enterprise/chapters/01-architecture-requirements-deployment-and-first-configuration.md)).

The practical guidance this chapter draws from that comparison: write new
automation against Redfish first, reach for RACADM for specific settings
or operations where Redfish coverage is incomplete on your firmware
baseline or where an existing script library already exists, and treat
WSMAN as something to recognize rather than something to author against.

### Idempotent automation against iDRAC

Idempotent automation — running the same operation repeatedly produces
the same end state rather than compounding changes or erroring on
re-application — is a general automation principle covered in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md),
[Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md), and applies directly to iDRAC scripting. A well-written iDRAC
automation script checks current state before changing it (for example,
confirming an IPv4 address isn't already set to the target value before
issuing a `PATCH`), handles the case where a resource already exists
(a user account, a virtual disk) gracefully rather than erroring, and
uses the session-token authentication pattern — establishing a session,
using its token for subsequent calls, and explicitly deleting the session
when done — that this encyclopedia has used consistently since Volume
XXII, [Chapter 1](01-architecture-generations-licensing-and-first-access.md)'s OME bootstrap example, because it avoids either leaving
idle sessions to expire uncleanly or repeatedly re-authenticating with
full credentials on every call.

### The `dellemc.openmanage` Ansible collection

For teams standardized on Ansible for infrastructure automation (Volume
IX), Dell publishes the `dellemc.openmanage` collection, which wraps
Redfish and RACADM-equivalent operations in Ansible modules covering
iDRAC network configuration, user management, firmware updates, storage
configuration, and Server Configuration Profile export/import — the same
operations this volume has covered directly via RACADM/Redfish, expressed
instead as declarative Ansible tasks. This is the natural next step for
an environment that has validated the underlying operations manually (as
this volume's labs have done) and now wants them expressed as reusable,
version-controlled playbooks rather than one-off scripts.

### Where iDRAC automation ends and OME orchestration begins

Every OME workflow covered in [Volume XXII](../../volume-22-dell-openmanage-enterprise/README.md) — discovery, inventory,
firmware compliance and update, configuration templates and compliance,
monitoring and alerting — resolves, underneath, into iDRAC-level Redfish
and WS-Management calls against individual servers, exactly the calls this
volume has taught directly. The practical dividing line: reach for direct
iDRAC automation (this volume) when working with a single server, when
building bring-up/provisioning tooling that runs before a server is
onboarded into fleet management, or when debugging why an OME-driven
operation failed on one specific unit; reach for OME ([Volume XXII](../../volume-22-dell-openmanage-enterprise/README.md)) when
the unit of work is "the fleet" or "a defined group of servers" rather
than one server, since OME's discovery, grouping, template, and
compliance-reporting layers exist specifically to avoid re-implementing
per-server orchestration logic at scale.

## Design Considerations

- **Standardize on Redfish for new automation investment, deliberately.**
  Existing RACADM-based scripts don't need to be rewritten reflexively,
  but new automation should default to Redfish given Dell's stated
  direction and Redfish's better fit for modern tooling ecosystems
  (Ansible, Terraform providers, generic Redfish client libraries) that
  extend beyond Dell-specific hardware.
- **Decide script vs. Ansible collection vs. OME template based on reuse
  scope and team tooling investment, not habit.** A one-off diagnostic
  script is fine as raw Python; a repeatable per-server provisioning step
  used across many bring-up events is a strong candidate for an Ansible
  role using `dellemc.openmanage`; a setting that should be enforced
  consistently and reported on across an entire managed fleet belongs in
  an OME configuration template ([Volume XXII, Chapter 8](../../volume-22-dell-openmanage-enterprise/chapters/08-templates-configuration-compliance-automation-and-apis.md)), not
  reimplemented as a script that has to be run against every server
  individually.
- **Design automation idempotently from the start, not as a later
  refactor.** Retrofitting idempotency into a script that assumes a clean
  starting state is more work than designing for it initially, and the
  cost of non-idempotent automation compounds specifically at the moment
  you need to re-run a partially failed provisioning job — exactly when
  reliability matters most.
- **Plan credential handling for automation the same way you planned it
  for human accounts in [Chapter 4](04-identity-certificates-security-and-compliance.md).** Automation service accounts should
  be scoped with discrete privileges appropriate to what the automation
  actually does, stored in a secrets manager rather than embedded in
  scripts, and rotated on the same cadence as any other privileged
  credential.
- **Decide your capstone runbook's failure/rollback behavior before
  running it against anything beyond a lab.** A multi-step provisioning
  runbook that fails partway through should leave the server in a
  known, documented state (or explicitly roll back via a retained SCP
  baseline, [Chapter 2](02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md)) rather than an ambiguous partial-configuration
  state that the next operator has to reverse-engineer.

## Implementation and Automation

### Session-token authentication (the pattern used throughout this volume)

Every scripted example across this volume's chapters has used either
HTTP Basic authentication (`auth=(user, password)`) for simplicity in
single-call examples, or could equally use iDRAC's session-token pattern
for a longer-running automation session, exactly as [Volume XXII](../../volume-22-dell-openmanage-enterprise/README.md), Chapter
1 established for OME:

```python
import requests

requests.packages.urllib3.disable_warnings()


def get_session(host: str, user: str, password: str) -> tuple[str, requests.Session]:
    session = requests.Session()
    resp = session.post(
        f"https://{host}/redfish/v1/SessionService/Sessions",
        json={"UserName": user, "Password": password},
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.headers["X-Auth-Token"], session
```

Use this pattern for any automation issuing more than a handful of calls
against the same iDRAC, and always explicitly delete the session
(`DELETE` to the session's own resource URI) when the automation
completes, rather than letting it idle out.

### An idempotent configuration-check-and-apply pattern

```python
#!/usr/bin/env python3
"""idrac_idempotent_ntp.py — ensure NTP is enabled with the expected
server, changing nothing if already correct.

Usage: python3 idrac_idempotent_ntp.py <idrac-ip> <username> <password> \
    <ntp-server>
"""
import sys
import requests

requests.packages.urllib3.disable_warnings()


def main() -> None:
    host, user, password, ntp_server = sys.argv[1:5]
    session = requests.Session()
    session.auth = (user, password)
    session.verify = False

    current = session.get(
        f"https://{host}/redfish/v1/Managers/iDRAC.Embedded.1/NetworkProtocol",
        timeout=30,
    )
    current.raise_for_status()
    ntp_current = current.json().get("NTP", {})

    if ntp_current.get("ProtocolEnabled") and ntp_server in ntp_current.get("NTPServers", []):
        print("NTP already correctly configured; no change made.")
        return

    resp = session.patch(
        f"https://{host}/redfish/v1/Managers/iDRAC.Embedded.1/NetworkProtocol",
        json={"NTP": {"ProtocolEnabled": True, "NTPServers": [ntp_server]}},
        timeout=30,
    )
    resp.raise_for_status()
    print(f"NTP configuration applied: {ntp_server}")


if __name__ == "__main__":
    main()
```

Note this uses the standard Redfish `NetworkProtocol` resource's `NTP`
object as an alternative to the `iDRAC.NTPConfigGroup` RACADM attributes
used in [Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md) — both configure the same underlying setting; confirm
which surface your firmware exposes most completely and prefer the
standard Redfish resource where available, consistent with this
chapter's Redfish-first guidance.

### Using the `dellemc.openmanage` Ansible collection

```yaml
# playbook: idrac_baseline.yml
---
- name: Apply baseline iDRAC configuration
  hosts: localhost
  gather_facts: false
  vars:
    idrac_ip: "192.168.1.120"
    idrac_user: "root"
    idrac_password: "{{ vault_idrac_password }}"
  tasks:
    - name: Ensure NTP is configured
      dellemc.openmanage.idrac_network:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        validate_certs: false
        ntp_configuration:
          enable_ntp: "Enabled"
          ntp_server_1: "ntp1.lab.example.com"

    - name: Export current configuration for backup
      dellemc.openmanage.idrac_server_config_profile:
        idrac_ip: "{{ idrac_ip }}"
        idrac_user: "{{ idrac_user }}"
        idrac_password: "{{ idrac_password }}"
        validate_certs: false
        command: export
        share_name: "/tmp/scp_backups"
        job_wait: true
```

Run with:

```bash
ansible-playbook idrac_baseline.yml --vault-password-file .vault-pass
```

Confirm exact module names and parameter structures against the current
`dellemc.openmanage` collection documentation for the collection version
your automation pins to — module parameters have evolved as the
collection has added coverage for newer iDRAC features.

## Validation and Troubleshooting

- **Redfish and RACADM report apparently conflicting state for the same
  setting.** This can occur transiently immediately after a change (one
  interface's cache or view may lag the other briefly) or, less commonly,
  reflect a genuine gap where a specific attribute is exposed differently
  by each interface. Re-query after a short delay; if the discrepancy
  persists, treat the Redfish value as authoritative given this chapter's
  Redfish-first guidance, and file the discrepancy against your firmware
  version for tracking.
- **Automation script works against one server but fails against another
  of the same model.** Confirm firmware version parity between the two —
  attribute names, available Redfish actions, and even RACADM syntax can
  shift between firmware releases within the same iDRAC generation, which
  is why this volume has consistently recommended confirming
  attribute/resource names against the live Attribute Registry or schema
  rather than hardcoding assumptions across an entire fleet's firmware
  range.
- **Ansible module task fails with an authentication or connectivity
  error despite correct credentials.** Confirm `validate_certs` is set
  appropriately for your certificate state ([Chapter 4](04-identity-certificates-security-and-compliance.md)) — a non-CA-signed
  or newly replaced certificate can cause an Ansible task using strict
  certificate validation to fail differently than a `curl -k`/`verify=False`
  script would, since the failure modes for certificate handling differ
  by client library default behavior.
- **A capstone-style multi-step runbook fails partway through.** Confirm
  your runbook logs enough state at each step to know exactly which steps
  completed before the failure — this is the practical payoff of
  designing for idempotency and clear step boundaries from the start
  (Design Considerations), since it turns "start over from scratch" into
  "resume from the failed step."
- **OME shows a device as non-compliant or unreachable even though direct
  iDRAC access works fine.** This points to an OME-side discovery or
  credential-profile issue rather than an iDRAC fault — confirm OME's
  configured discovery credentials match the current iDRAC credentials
  (a password rotated per [Chapter 4](04-identity-certificates-security-and-compliance.md) without updating OME's credential
  profile is a common cause) per [Volume XXII, Chapter 3](../../volume-22-dell-openmanage-enterprise/chapters/03-discovery-onboarding-inventory-groups-and-device-control.md).

## Security and Best Practices

- Store automation credentials (Redfish/RACADM service accounts, Ansible
  Vault passwords) in a dedicated secrets manager, never in plaintext
  playbooks, scripts, or version-controlled files — this applies to every
  script in this volume, not only the capstone examples in this chapter.
- Scope automation service accounts to the minimum discrete privileges
  the automation actually exercises ([Chapter 4](04-identity-certificates-security-and-compliance.md)), and use distinct
  accounts for distinct automation purposes where practical, so a
  compromised credential's blast radius is bounded.
- Pin your Ansible collection version explicitly in your automation's
  requirements rather than always pulling latest, so a collection update
  is a deliberate, tested change rather than an uncontrolled variable
  introduced into production automation runs.
- Log every automated change with enough context (which script/playbook,
  which run, what changed) to reconstruct history alongside the
  Lifecycle Log's own record ([Chapter 6](06-hardware-health-power-thermal-logs-and-support.md)) — the two should corroborate
  each other during an incident investigation.
- Review automation scripts and playbooks for the same security posture
  you'd expect of a human administrator: least privilege, no
  unnecessary certificate validation bypasses in anything beyond a lab
  context, and explicit handling of failure paths rather than assuming
  the happy path.

## References and Knowledge Checks

**References**

- [Dell Technologies, *iDRAC RACADM CLI Guide*](https://www.dell.com/support/manuals/en-us/idrac9-lifecycle-controller-v4.x-series/idrac_4.00.00.00_racadm/supported-racadm-interfaces?guid=guid-a5747353-fc88-4438-b617-c50ca260448e&lang=en-us)
- [Dell Technologies, *iDRAC Redfish API Guide*](https://www.dell.com/support/kbdoc/en-us/000178045/redfish-api-with-dell-integrated-remote-access-controller)
- [Dell Technologies, `dellemc.openmanage` Ansible Collection documentation
  (Ansible Galaxy / Dell GitHub)](https://docs.ansible.com/projects/ansible/latest/collections/dellemc/openmanage/index.html)
- Dell Technologies, *OpenManage Enterprise RESTful API Guide* (Volume
  XXII, [Chapter 1](01-architecture-generations-licensing-and-first-access.md) reference)
- [DMTF, *Redfish Specification* (DSP0266) and *Redfish Schema Supplement*](https://www.dmtf.org/standards/redfish)
- [`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md) in this repository for the dated iDRAC9/iDRAC10
  baseline

**Knowledge Checks**

1. Why does this chapter recommend Redfish over RACADM for new automation
   investment, even though RACADM remains fully supported?
2. What makes an iDRAC automation script idempotent, and why does that
   matter most at the moment a script needs to be re-run after a partial
   failure?
3. When is direct iDRAC automation the right tool versus reaching for
   OpenManage Enterprise, given that OME calls resolve to the same
   underlying iDRAC operations?
4. What is the practical difference between storing a setting in a
   one-off script, an Ansible role, and an OME configuration template,
   and what should drive the choice among them?
5. Why can the same automation script behave differently against two
   servers of the same model, and what should you check first?

## Hands-On Lab

**Objective:** Execute an end-to-end provisioning runbook against a lab
server — network configuration, identity hardening, storage baseline,
firmware inventory check, and OS deployment via Virtual Media — combining
techniques from every chapter in this volume into a single automated
sequence, run first manually as a rehearsal, then as a scripted pass.

**Prerequisites**

- The lab server used throughout this volume's chapters, reset to a known
  state (either the original [Chapter 1](01-architecture-generations-licensing-and-first-access.md) baseline, restored via the SCP
  export from [Chapter 2](02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md), or left in its current state if you are
  comfortable applying this capstone on top of it).
- All prerequisites from Chapters 1 through 8: network reachability, a
  test OS ISO on a reachable share, spare disks for storage
  configuration, and a firmware image or online catalog access.
- Python 3.11+ with `requests`, and optionally Ansible with the
  `dellemc.openmanage` collection installed
  (`ansible-galaxy collection install dellemc.openmanage`).

**Steps**

1. Export a pre-capstone SCP baseline as your rollback point, following
   [Chapter 2](02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md)'s procedure:

   ```bash
   racadm systemconfig export -t xml -f pre-capstone-baseline.xml \
     -l //<share-ip>/scp-share -u <svc-user> -p '<password>'
   ```

2. Confirm and, if needed, reapply network configuration from [Chapter 3](03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)
   (static IPv4, DNS registration, NTP) — this capstone assumes that
   baseline is already correct from earlier labs; re-verify rather than
   re-apply if unchanged.
3. Confirm identity hardening from [Chapter 4](04-identity-certificates-security-and-compliance.md) is in place: a non-default
   local password, a CA-signed (or lab-CA-signed) certificate installed.
   **Expected result:** browsing to the iDRAC no longer shows the
   original factory self-signed certificate warning.
4. Confirm storage baseline from [Chapter 7](07-storage-arrays-boss-raid-configuration-and-maintenance.md): at minimum, run
   `idrac_storage_health_check.py` and confirm a clean result before
   proceeding.

   ```bash
   python3 idrac_storage_health_check.py <idrac-ip> root '<password>'
   ```

5. Confirm firmware inventory from [Chapter 8](08-firmware-idrac-bios-lifecycle-controller-and-platform-updates.md) and record current versions
   as this capstone's firmware baseline:

   ```bash
   racadm swinventory > capstone-firmware-baseline.txt
   ```

6. Deploy a test OS using the Virtual Media pattern from [Chapter 5](05-idrac-direct-virtual-console-virtual-media-and-local-service.md):

   ```bash
   python3 idrac_mount_and_boot.py <idrac-ip> root '<password>' \
     https://<share-host>/images/test-os.iso
   ```

   **Expected result:** the server boots from the mounted image, visible
   via Virtual Console, confirming the full chain — network, identity,
   storage, firmware baseline, and remote media boot — functions
   together as a coherent provisioning sequence.
7. Confirm the Lifecycle Log captured this capstone's activity as a
   single reviewable timeline:

   ```bash
   racadm lclog view | tail -30
   ```

   **Expected result:** entries corresponding to each major step (network
   changes if any were reapplied, the firmware inventory check, the
   Virtual Media mount and boot) appear in chronological order, confirming
   [Chapter 6](06-hardware-health-power-thermal-logs-and-support.md)'s log guidance holds up as a real audit trail across a
   multi-step operation.
8. **Negative test:** deliberately re-run step 6 with an unreachable
   image URL, confirming the same fail-safe behavior validated in
   [Chapter 5](05-idrac-direct-virtual-console-virtual-media-and-local-service.md)'s lab still holds when invoked as part of a larger sequence:

   ```bash
   python3 idrac_mount_and_boot.py <idrac-ip> root '<password>' \
     https://<share-host>/images/does-not-exist.iso
   ```

   **Expected result:** the mount fails cleanly with an error; the server
   does not boot to an unpredictable state.

**Cleanup**

- Eject any mounted Virtual Media and clear one-time boot overrides,
  following [Chapter 5](05-idrac-direct-virtual-console-virtual-media-and-local-service.md)'s cleanup procedure.
- If this lab server will be decommissioned or repurposed outside this
  volume's labs, follow [Chapter 4](04-identity-certificates-security-and-compliance.md)'s System Erase guidance rather than
  leaving lab configuration and test data in place.
- If it will be reused, retain `pre-capstone-baseline.xml` and
  `capstone-firmware-baseline.txt` as documented reference points for any
  future troubleshooting.

## Summary and Completion Checklist

This capstone chapter tied together every prior chapter in the volume
into a coherent automation model: RACADM, Redfish, and (for historical
context) WS-Management as the three interfaces every capability in this
volume is reachable through; idempotent, session-token-based Python
automation as the scripting pattern used consistently since [Chapter 1](01-architecture-generations-licensing-and-first-access.md);
the `dellemc.openmanage` Ansible collection as the declarative-automation
path for teams standardized on Ansible; and an explicit dividing line
between single-server iDRAC automation (this volume) and fleet-scale
OpenManage Enterprise orchestration ([Volume XXII](../../volume-22-dell-openmanage-enterprise/README.md)), which resolves to the
same underlying operations at scale. The capstone lab exercised network,
identity, storage, firmware, and OS-deployment techniques from every
chapter in a single, auditable, idempotent-by-design sequence — the
practical demonstration that this volume's single-server administrative
model is a complete, production-usable skill set on its own, and the
foundation every fleet-scale OME workflow in [Volume XXII](../../volume-22-dell-openmanage-enterprise/README.md) ultimately
depends on.

- [ ] I can compare RACADM, Redfish, and WS-Management and justify a
      Redfish-first approach for new automation.
- [ ] I built and ran idempotent Python automation against iDRAC using the
      session-token authentication pattern.
- [ ] I expressed an iDRAC configuration task as a `dellemc.openmanage`
      Ansible playbook.
- [ ] I can explain the practical dividing line between direct iDRAC
      automation and OpenManage Enterprise fleet orchestration.
- [ ] I executed the capstone runbook end to end, including a negative
      test, tying together network, identity, storage, firmware, and OS
      deployment from every chapter in this volume.
