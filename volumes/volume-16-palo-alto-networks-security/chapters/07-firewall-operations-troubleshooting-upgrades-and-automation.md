# Chapter 07: Firewall Operations, Troubleshooting, Upgrades, and Automation

![Lab flow for this chapter: suspending the passive HA member for upgrade preparation leaves the active peer serving traffic uninterrupted; returning the member to functional state completes the sequence. A filtered packet-diag capture confirms matching packets for a specific test flow, an XML API request retrieves system info matching the CLI's output, and a REST API call creates an address object confirmed at the CLI. As a negative test, the same system info request is repeated with a deliberately invalid API key; the API returns an authentication failure rather than falling back to an unauthenticated default, confirming key validation is actually enforced.](../../../diagrams/volume-16-palo-alto-networks-security/chapter-07-ha-upgrade-api-key-validation-flow.svg)

*Figure 7-1. Flow used throughout this chapter's Hands-On Lab: an HA-aware upgrade sequence, packet-diag capture, and XML/REST API operations, tested against an invalid API key.*

## Learning Objectives

- Plan and execute a PAN-OS software upgrade across an HA pair with zero
  planned traffic loss, following the correct sequential upgrade path.
- Use PAN-OS packet capture, global counters, and log-follow commands to
  diagnose a live traffic problem.
- Generate and interpret a tech support file for vendor escalation.
- Automate configuration and operational tasks using the PAN-OS/Panorama
  XML API and REST API, and describe how Terraform and Ansible extend that
  automation into infrastructure-as-code pipelines.
- Schedule and validate configuration backups and content/software
  deployment across a Panorama-managed fleet.

## Theory and Architecture

Chapters 03–06 built and centrally managed a PAN-OS environment. This
chapter covers what keeps that environment running correctly over time:
disciplined upgrade procedures, a systematic troubleshooting toolkit, and
automation that scales operational tasks beyond what manual CLI/Web UI
work can sustain across a large fleet.

### PAN-OS upgrade paths

PAN-OS enforces a **sequential upgrade path** between major/minor
releases — a firewall generally cannot skip directly from one feature
release to a release more than one major version ahead without passing
through each intermediate base image first (for example, upgrading from
10.2.x to 11.1.x typically requires installing the 11.0.x base image
before 11.1.x, even if the final target skips 11.0.x's own feature
release). The exact required path is release-specific and published in
each release's upgrade/downgrade documentation; always confirm the current
path against Palo Alto Networks' official guidance rather than assuming
the pattern from a prior release cycle still applies, since Palo Alto
Networks periodically changes minimum-hop requirements between release
trains.

### HA-aware upgrade sequencing

Upgrading an HA pair ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)) without planned downtime relies on the
pair's redundancy: the **passive** (or, in active/active, one designated)
member is upgraded first while its peer continues actively forwarding
traffic, then a controlled failover shifts traffic to the newly upgraded
member, and finally the second member is upgraded. This is why HA
existence matters operationally, not just for unplanned-failure
resilience — it is the mechanism that makes planned software maintenance
non-disruptive. Content updates (Applications and Threats, Antivirus,
WildFire) are lower-risk than full software upgrades but still benefit
from staggered installation across a fleet (introduced in [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)) so a
problematic content release affects a canary subset before reaching every
enforcement point.

### The troubleshooting toolkit

PAN-OS exposes several distinct layers of operational visibility, each
suited to a different class of problem:

| Tool | Use case |
| --- | --- |
| `show counter global` | Dataplane packet-processing counters — drops, resets, and their specific named reasons |
| `show session all` / `show session id <id>` | Live session table lookups, including NAT translation and applied policy |
| Packet capture (`debug dataplane packet-diag`) | Captures packets at specific dataplane processing stages (receive, firewall, transmit) to isolate where a packet is dropped or altered |
| `tail follow yes mp-log <logfile>` | Live-tail management-plane process logs (for example, `pan_dp0`, `system`, `configd`) |
| Tech support file | A comprehensive, vendor-support-ready bundle of configuration, logs, and system state for escalation |

`show counter global` is frequently the fastest first step for a "traffic
is being dropped" report — its output is organized by processing stage and
named drop reason (for example, a specific counter increments for a
session aged out, a different one for a decrypt failure, a different one
for a zone protection flood-mitigation drop), which usually narrows the
investigation immediately without needing a full packet capture.

### Automation surfaces

PAN-OS and Panorama expose the same configuration and operational
capability available through the CLI and Web UI via two API surfaces:

- **XML API.** The original, comprehensive API; supports configuration
  (`type=config`, with `action=get/set/edit/delete`), operational commands
  (`type=op`, wrapping the same commands available at the CLI), commit
  operations, and log retrieval, authenticated with an API key generated
  from a username/password exchange.
- **REST API.** A more modern, resource-oriented API covering the most
  commonly automated configuration objects (address objects, security
  rules, NAT rules, and more) with standard HTTP verbs and JSON payloads,
  authenticated the same way as the XML API.

Both APIs are the foundation for higher-level infrastructure-as-code
tooling: the official **Terraform provider for PAN-OS/Panorama** manages
firewall and Panorama configuration declaratively (consistent with Volume
IX's plan/apply automation model), and the **Ansible Collection for PAN-OS**
provides idempotent modules for the same configuration surface, suited to
procedural playbook-driven automation and integration into existing
Ansible-based operational pipelines.

## Design Considerations

- **Upgrade ring strategy.** Do not upgrade an entire fleet simultaneously,
  even when Panorama makes doing so mechanically easy. Establish a staged
  upgrade ring — a small canary group first, then a broader wave, then the
  remaining fleet — with a defined observation period between waves, so a
  release-specific defect is caught against a small blast radius rather
  than the whole environment.
- **Downgrade planning.** Before any upgrade, confirm the documented
  downgrade path and take a configuration backup and, where supported, a
  pre-upgrade state snapshot; some PAN-OS features and configuration
  constructs introduced in a newer release are not preserved cleanly on
  downgrade, so a rollback plan validated in advance is materially safer
  than discovering that fact mid-incident.
- **Automation authentication model.** A shared, long-lived API key used
  by every automation script and stored in plaintext in a script or
  repository is a common, avoidable weakness. Prefer a dedicated
  automation service account with role-scoped permissions, API keys
  retrieved from a secrets manager at runtime ([Volume IX](../../volume-09-infrastructure-automation/README.md)), and rotation on
  a defined schedule.
- **REST API vs. XML API for a given task.** Prefer the REST API for
  standard object CRUD operations it supports natively — its resource
  model and JSON payloads are simpler to integrate into modern
  infrastructure-as-code and CI/CD pipelines. Fall back to the XML API for
  operational commands, less common configuration paths, or bulk
  operations the REST API does not yet expose equivalently.
- **Terraform vs. Ansible for PAN-OS automation.** Favor the Terraform
  provider where firewall/Panorama configuration is managed as part of a
  broader declarative infrastructure stack alongside cloud resources
  ([Volume VII](../../volume-07-cloud-infrastructure/README.md), [Volume IX](../../volume-09-infrastructure-automation/README.md)) and state-tracked drift detection is valuable.
  Favor the Ansible Collection where the organization's existing
  operational automation is already Ansible-centric ([Volume IX](../../volume-09-infrastructure-automation/README.md)) or where a
  more procedural, playbook-driven change (for example, a one-time bulk
  object cleanup) fits the task better than a persistent declarative
  state file.

## Implementation and Automation

### Checking and downloading a new PAN-OS software version

```text
admin@pa-fw01> request system software check
admin@pa-fw01> request system software download version 11.1.4
admin@pa-fw01> request system software info
```

### HA-aware upgrade: suspend, upgrade, and reintroduce the passive member

On the currently passive HA member:

```text
admin@pa-fw01-b> request high-availability state suspend
admin@pa-fw01-b> request system software install version 11.1.4
admin@pa-fw01-b> request restart system
```

After the member reboots and rejoins as passive (verify with `show
high-availability state`):

```text
admin@pa-fw01-b> request high-availability state functional
```

Trigger a controlled failover to shift active traffic handling to the
now-upgraded member, then repeat the install/restart sequence on the
formerly active member:

```text
admin@pa-fw01-a> request high-availability state suspend
admin@pa-fw01-a> request system software install version 11.1.4
admin@pa-fw01-a> request restart system
```

### Packet capture for a drop investigation

```text
admin@pa-fw01# set deviceconfig setting session packet-diag enable yes
admin@pa-fw01> debug dataplane packet-diag set filter match source 10.10.20.15 destination 8.8.8.8
admin@pa-fw01> debug dataplane packet-diag set capture-file stage receive file rx.pcap
admin@pa-fw01> debug dataplane packet-diag set capture-file stage transmit file tx.pcap
admin@pa-fw01> debug dataplane packet-diag set capture on
# Generate the traffic under investigation, then:
admin@pa-fw01> debug dataplane packet-diag set capture off
admin@pa-fw01> tftp export mgmt-pcap from rx.pcap to 10.10.10.50
```

### Global counters for a drop reason

```text
admin@pa-fw01> show counter global filter delta yes | match drop
```

### Generating a tech support file

```text
admin@pa-fw01> request tech-support
admin@pa-fw01> scp export tech-support from <generated-filename> to admin@10.10.10.50:/support/
```

### XML API: retrieving system info

```bash
# Generate an API key from a username/password (do once, store securely).
curl -sk "https://pa-fw01.acme.local/api/?type=keygen&user=automation&password=<PASSWORD>"

# Use the returned key for subsequent operational calls.
curl -sk "https://pa-fw01.acme.local/api/?type=op&cmd=<show><system><info/></system></show>&key=<API_KEY>"
```

### REST API: creating an address object

```bash
curl -sk -X POST \
  "https://pa-fw01.acme.local/restapi/v11.1/Objects/Addresses?location=vsys&vsys=vsys1" \
  -H "X-PAN-KEY: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"entry": [{"@name": "app-server-01", "ip-netmask": "10.10.20.50/32"}]}'
```

### Ansible: adding a security rule (illustrative)

```yaml
- name: Add a security rule via the PAN-OS Ansible Collection
  hosts: localhost
  connection: local
  tasks:
    - name: Allow branch web access
      paloaltonetworks.panos.panos_security_rule:
        provider:
          ip_address: "pa-fw01.acme.local"
          api_key: "{{ panos_api_key }}"
        rule_name: "Allow-Branch-Web"
        source_zone: ["trust"]
        destination_zone: ["untrust"]
        application: ["web-browsing", "ssl"]
        action: "allow"
        commit: true
```

### Terraform: a minimal address object (illustrative)

```hcl
resource "panos_address_object" "app_server" {
  name    = "app-server-01"
  value   = "10.10.20.50/32"
  vsys    = "vsys1"
}
```

## Validation and Troubleshooting

- **Upgrade install fails validation.** Confirm the release notes' minimum
  content version and disk-space requirements are met before install;
  `request system software info` and `show system disk-space` catch the
  two most common preconditions before attempting the install command.
- **HA pair does not resynchronize after upgrade.** A version mismatch
  between HA peers (one upgraded, one not yet) is an *expected* transient
  state during a staged upgrade — `show high-availability state` reports
  this explicitly; do not treat it as a fault until the second member's
  upgrade is complete and the pair still fails to synchronize afterward.
- **Packet capture shows no packets.** Confirm the packet-diag filter
  criteria actually match the traffic under test (source/destination/
  port/protocol) and that `debug dataplane packet-diag set capture on` was
  issued after the filter and stage/file settings — capture state and
  filter state are independent settings and a capture left on with no
  filter captures everything, while a filter set with capture left off
  captures nothing.
- **API calls return an authentication error.** Confirm the API key has
  not expired or been revoked (`request auto-renew-api-key` or Panorama
  RBAC changes can invalidate stored keys), that the automation service
  account still holds the required role-based permissions, and that the
  target Web UI/API service is reachable and not restricted by the
  permitted-IP list from [Chapter 01](01-cybersecurity-apprentice-foundations.md).
- **Ansible/Terraform run reports drift immediately after a successful
  apply.** This typically indicates the change was applied to the
  candidate configuration but not committed — both the Ansible collection
  and Terraform provider expose a `commit` parameter/resource
  independently of the object change itself; confirm it is set, or that a
  separate commit step follows in the pipeline.

## Security and Best Practices

- Stage every software and content upgrade through a canary ring before
  fleet-wide rollout, and maintain a tested, documented downgrade/rollback
  procedure for both.
- Never embed a live API key or automation credential in a committed
  script or playbook; retrieve it at runtime from a secrets manager and
  scope the automation account's role to only the operations it performs.
- Rotate API keys and automation service account credentials on a defined
  schedule, and immediately upon any suspected exposure or personnel
  change involving access to them.
- Restrict which source addresses/networks may reach the management
  interface's API and Web UI endpoints, exactly as with interactive
  administrative access ([Chapter 01](01-cybersecurity-apprentice-foundations.md)) — an API credential is not a lesser
  target than an interactive login.
- Retain and securely store tech support files only as long as needed for
  the active support case; they contain configuration and log data that
  can include sensitive network and policy detail, and should be handled
  with the same care as the running configuration itself.
- Log and review automation-driven configuration changes with the same
  change-management discipline as manual changes — an API-driven change
  should be as auditable (who, what, when, why) as a Panorama commit
  description, not a blind spot outside normal change review.

## References and Knowledge Checks

**References**

- [Palo Alto Networks, *PAN-OS Upgrade/Downgrade Considerations*
  documentation (version 11.1).](https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-upgrade/upgrade-pan-os/upgradedowngrade-considerations)
- [Palo Alto Networks, *PAN-OS and Panorama API* reference (XML API and
  REST API).](https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-panorama-api)
- [Palo Alto Networks, *Terraform Provider for PAN-OS* and *Ansible
  Collection for PAN-OS* documentation.](https://registry.terraform.io/providers/PaloAltoNetworks/panos/latest/docs)
- [Palo Alto Networks, *Packet Capture and Troubleshooting* technical
  documentation.](https://docs.paloaltonetworks.com/ngfw/administration/monitoring/take-packet-captures)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — PAN-OS 11.x /
  Panorama 11.x baseline; Terraform and Ansible baselines used in the
  automation examples above.
- [Volume IX](../../volume-09-infrastructure-automation/README.md) — Infrastructure Automation, for plan/apply and idempotency
  principles applied to the Terraform/Ansible examples here.

**Knowledge checks**

1. Why must a passive HA member be suspended and upgraded before its
   active peer in a zero-downtime upgrade sequence, and what step
   transfers active traffic handling to the newly upgraded member?
2. Which single CLI command most efficiently narrows down a "traffic is
   being dropped" report before a full packet capture is taken, and why?
3. What are the two independent settings that must both be configured
   correctly for `debug dataplane packet-diag` to capture the intended
   traffic?
4. Name one reason to prefer the REST API over the XML API for a given
   automation task, and one reason to prefer the XML API instead.

## Hands-On Lab

**Objective:** Perform a simulated HA-aware upgrade sequence, capture and
inspect traffic using packet-diag, retrieve system information via the XML
API, and create an address object via the REST API — including a negative
test using an invalid API key.

**Prerequisites**

- The HA pair built in [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)'s lab (or a single lab firewall if HA is
  unavailable — the upgrade sequencing steps can be read/adapted rather
  than fully executed against a single node).
- `curl` available on the workstation used for API testing.
- A lab-scoped automation username/password with API access enabled on the
  target firewall.
- Available PAN-OS software images for the upgrade steps, or read-only
  familiarity if a live upgrade is not practical in this lab environment.

**Steps**

1. Check current and available software versions:

   ```text
   admin@pa-fw01> request system software info
   admin@pa-fw01> request system software check
   ```

2. On the passive HA member, suspend it in preparation for upgrade:

   ```text
   admin@pa-fw01-b> request high-availability state suspend
   admin@pa-fw01-b> show high-availability state
   ```

   **Expected result:** The member reports a `suspended` state while its
   peer remains `active`, confirming traffic continues uninterrupted on
   the peer.

3. Return the member to a functional state (skip the actual software
   install if no target image is staged in this lab):

   ```text
   admin@pa-fw01-b> request high-availability state functional
   ```

4. Generate a filtered packet capture for a specific test flow:

   ```text
   admin@pa-fw01> debug dataplane packet-diag set filter match source 10.10.20.15 destination 8.8.8.8
   admin@pa-fw01> debug dataplane packet-diag set capture-file stage receive file rx.pcap
   admin@pa-fw01> debug dataplane packet-diag set capture on
   ```

   From the test host, generate matching traffic (for example, `ping
   8.8.8.8`), then:

   ```text
   admin@pa-fw01> debug dataplane packet-diag set capture off
   ```

5. Confirm packets were captured:

   ```text
   admin@pa-fw01> view-pcap dpc-log rx.pcap
   ```

   **Expected result:** Captured packets matching the filter appear.

6. Generate an API key and retrieve system info via the XML API:

   ```bash
   curl -sk "https://pa-fw01.acme.local/api/?type=keygen&user=automation&password=<PASSWORD>"
   curl -sk "https://pa-fw01.acme.local/api/?type=op&cmd=<show><system><info/></system></show>&key=<API_KEY>"
   ```

   **Expected result:** An XML response containing the firewall's hostname
   and software version, matching `show system info` at the CLI.

7. Create an address object via the REST API:

   ```bash
   curl -sk -X POST \
     "https://pa-fw01.acme.local/restapi/v11.1/Objects/Addresses?location=vsys&vsys=vsys1" \
     -H "X-PAN-KEY: <API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"entry": [{"@name": "lab-api-test", "ip-netmask": "10.10.20.99/32"}]}'
   ```

   **Expected result:** A success response; confirm the object exists with
   `show object address lab-api-test` at the CLI.

8. **Negative test:** Repeat the system info request using a deliberately
   invalid API key:

   ```bash
   curl -sk "https://pa-fw01.acme.local/api/?type=op&cmd=<show><system><info/></system></show>&key=INVALID-KEY-VALUE"
   ```

   **Expected result:** An authentication failure response, confirming the
   API enforces key validation rather than falling back to an unauthenticated
   default.

9. **Cleanup:** Remove the lab address object created via the API and clear
   the packet-diag filter/capture state:

   ```text
   admin@pa-fw01# delete object address lab-api-test
   admin@pa-fw01# commit
   admin@pa-fw01> debug dataplane packet-diag clear filter-marked-session all
   admin@pa-fw01> debug dataplane packet-diag set capture off
   ```

   Revoke or rotate the lab automation API key if it will not be reused.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Sustained PAN-OS operations depend on a disciplined upgrade sequence that
uses HA redundancy to avoid planned downtime, a layered troubleshooting
toolkit that starts with global counters and escalates to packet capture
only when needed, and automation surfaces — the XML API, REST API,
Terraform provider, and Ansible collection — that let fleet-scale
operational and configuration tasks run as reliable, auditable code rather
than repetitive manual work. These skills, combined with Panorama's
centralized management from [Chapter 06](06-panorama-installation-central-management-and-logging.md), are what a Practitioner-level
engineer is expected to demonstrate operationally in production.

- [ ] Can plan and describe a zero-downtime HA-aware software upgrade
      sequence.
- [ ] Can use global counters and packet capture to diagnose a traffic drop.
- [ ] Can generate a tech support file for vendor escalation.
- [ ] Can retrieve data and create objects using both the XML API and REST
      API, and explain when Terraform or Ansible is the better automation
      fit.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
