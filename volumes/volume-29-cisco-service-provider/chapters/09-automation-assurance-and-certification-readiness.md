# Chapter 09: Automation, Assurance, and Certification Readiness

## Learning Objectives

- Automate IOS XR with model-driven interfaces: NETCONF, RESTCONF,
  gNMI, and YANG data models
- Stream model-driven telemetry and explain why it replaces SNMP
  polling for assurance
- Apply orchestration to provider services with Cisco NSO and the
  device-to-controller spectrum
- Operate the network as a system: deliberate change on IOS XR,
  validation, and rollback at scale
- Assemble a personal readiness plan for SPCOR and a chosen
  concentration from the verified blueprints

## Theory and Architecture

### Why automation is survival, not luxury, at SP scale

Chapter 01 named the scale: tens of thousands of devices, millions of
routes, SLAs measured in milliseconds of restoration. No team hand-
configures that, and no human polls it fast enough to meet an
assurance SLA. SPCOR's Automation and Assurance domain (15%) and the
whole of the retired SPAUTO (its four domains outline this chapter) treat
programmability as the operating model, and IOS XR — structured,
committed, model-native (Chapter 01) — is built for it.

### The model-driven interfaces

IOS XR exposes its configuration and state through **YANG** data
models over three transports, and knowing which fits what is exam and
job material:

- **NETCONF** (XML, SSH) — transactional configuration with candidate/
  commit semantics that map naturally onto XR's two-stage model.
- **RESTCONF** (HTTP verbs on YANG) — lighter, good for simple
  integrations and quick reads.
- **gNMI** (gRPC) — the modern high-performance interface, especially
  for **telemetry** subscriptions.

Models come in flavors: **native** (Cisco-XR YANG, full feature
coverage) versus **OpenConfig** (vendor-neutral, portable across a
multi-vendor core — the reason many providers prefer it). SPAUTO's
Automation APIs and Protocols and Network Device Programmability
domains (30% each) are exactly this.

### Model-driven telemetry: assurance that keeps up

**MDT** streams operational state — interface counters, BGP neighbor
states, LSP status, queue depths — from the device on subscription
(dial-out or dial-in via gNMI), continuously, instead of SNMP's
request/response polling. The difference is assurance-grade: sub-second
visibility, no polling gaps, and a data shape (structured, timestamped)
that a time-series pipeline consumes directly. SLA measurement,
capacity trending, and fast anomaly detection all depend on it — the
provider analog of Volume XXVII's "buy the telemetry" for AI fabrics.

### Orchestration: NSO and the spectrum

Beyond per-device automation, **Cisco NSO** (Network Services
Orchestrator) models *services* — an L3VPN, an EVPN, an SR-TE policy —
as intent, renders device configuration across every involved node,
and keeps a reconciled view (it knows what it deployed and detects
drift). The spectrum runs device-scripting (NETCONF/gNMI directly) →
configuration management → service orchestration (NSO) → closed-loop
(telemetry feeding automated remediation). SPAUTO's Automation and
Orchestration Platforms domain (30%) lives at the NSO end; the habits
below span all of it.

### The habits, unchanged

The automation discipline is the encyclopedia's throughout: idempotent
operations, secrets vaulted not scripted, post-condition asserts,
diff-before-apply, and change artifacts — the same rules Volumes IX,
XXVII, and XXVIII apply, here made easier by XR's native commit/
rollback and confirmed-commit.

## Design Considerations

- **OpenConfig where multi-vendor, native where feature-deep**: choose
  the model flavor for the estate; mixing is fine if deliberate.
- **Telemetry pipeline as core infrastructure**: collectors, a time-
  series store, dashboards, and alerting designed in — an assurance
  SLA with no telemetry is a promise with no instrument.
- **Service models over device scripts at scale**: NSO (or equivalent)
  for the services customers buy, so provisioning is consistent and
  auditable and drift is visible.
- **Closed-loop carefully**: automated remediation is powerful and
  dangerous — start with detect-and-alert, promote to auto-remediate
  only what you have rehearsed.

## Implementation and Automation

gNMI telemetry subscription and a NETCONF change on the volume's XR
estate:

```text
! Model-driven telemetry: stream BGP + interface state via gRPC dial-out
telemetry model-driven
 destination-group DC1
  address-family ipv4 10.50.0.5 port 57500
  encoding self-describing-gpb
 sensor-group SP-HEALTH
  sensor-path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/.../neighbors
  sensor-path Cisco-IOS-XR-infra-statsd-oper:infra-statistics/.../generic-counters
 subscription SP-SUB
  sensor-group-id SP-HEALTH sample-interval 5000
  destination-id DC1
```

```python
# NETCONF edit-config maps onto XR's candidate/commit (ncclient)
from ncclient import manager
with manager.connect(host="pe1", username="auto", key_filename="…",
                     hostkey_verify=True) as m:
    m.edit_config(target="candidate", config=vrf_payload)   # stage
    m.commit(confirmed=True, timeout="120")                 # confirmed commit
    assert bgp_vrf_up(m, "CUST-A"), "post-condition: VRF must be up"
    m.commit()                                              # confirm
```

```text
! OpenConfig read for portability
show yang-library
# gnmic -a pe1 get --path 'openconfig-interfaces:interfaces/interface'
```

## Validation and Troubleshooting

Automation is validated like any change plus its own layer:
**diff before apply** (NETCONF `show configuration` on the candidate,
NSO dry-run), **assert after** (the post-condition in the snippet —
the VRF must actually come up, mirroring Chapter 06's isolation
proof), and **confirmed commit** so a change that breaks reachability
rolls itself back (Chapter 01's safety, wired into automation).
Telemetry validation: the subscription is established and data is
arriving at the collector (gaps mean transport/encoding or a bad
sensor path). Troubleshooting: NETCONF/gNMI errors name the failing
YANG path precisely — more honest than screen-scraping; OpenConfig-
versus-native mismatches surface as unsupported paths (check
`show yang-library`); NSO out-of-sync means someone changed a device
by hand (reconcile, then find who and fix the process — the Chapter
09 lesson of Volume XXVII, restated for XR).

## Security and Best Practices

- gNMI/NETCONF over TLS in production (the lab's `no-tls`/`no-tls`
  shortcuts are flagged as lab-only, as in Chapter 01); mutual auth
  where the platform supports it.
- Automation accounts with XR task-group authorization scoped to what
  they manage; tokens and keys vaulted; no credentials in repositories.
- Telemetry and orchestration controllers are privileged network-wide
  — hold them to the management-plane standard of Chapter 08, and
  audit their actions.

## References and Knowledge Checks

- SPCOR 350-501 v1.1 Automation and Assurance (15%); SPAUTO 300-535
  v1.1 (all four domains) — retired 2026, kept for the record
- Cisco IOS XR programmability and telemetry configuration guides;
  Cisco NSO documentation; OpenConfig models

Knowledge checks:

1. Match NETCONF, RESTCONF, and gNMI to their best-fit tasks, and say
   which pairs naturally with XR's commit model and which with
   telemetry.
2. Why does model-driven telemetry meet an assurance SLA that SNMP
   polling cannot?
3. What does NSO know that a device-scripting approach does not, and
   how does that surface drift?
4. Build a weight-ordered SPCOR study sequence from this volume's
   README and defend the ordering.

## Hands-On Lab

Capstone across the volume's XR estate. **Programmability**: a NETCONF
(ncclient) script that provisions a new CUST-E L3VPN on two PEs with
a confirmed commit and a post-condition assert that the VRF and its
routes come up — run twice to prove idempotency. **Telemetry**: stand
up a collector, subscribe via gNMI to BGP neighbor and interface
state, and show sub-second updates; then fail a link and watch the
telemetry reflect it faster than a polling interval would. **Assurance
scenario**: define one SLA signal (e.g., a BGP session flap or a
queue-drop threshold) and alert on it from the telemetry stream.
**Orchestration (optional/where available)**: model the L3VPN as an
NSO service and show a single service edit rendering both PEs, then
induce device drift and show NSO detecting out-of-sync. **Readiness**:
draft your SPCOR plan weight-ordered against the README, concentration
chosen with a one-sentence reason, mock-exam checkpoints scheduled.

## Lab Verification

Verification means the NETCONF provisioning was idempotent with its
assert and confirmed-commit, telemetry showed sub-second state and
beat polling on a failure, the SLA alert fired on demand, and the
study plan exists. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

At provider scale, automation and assurance are the operating model:
YANG over NETCONF/RESTCONF/gNMI configures the network, model-driven
telemetry observes it fast enough to keep SLAs, and NSO orchestrates
the services customers buy while detecting drift — all riding IOS XR's
native commit, confirm, and rollback. This closes SPCOR's Automation
and Assurance domain and the whole of the retired SPAUTO, and with
the core and concentrations verified, mapped, and practiced, the CCNP
Service Provider track is yours to schedule.

- [ ] I can match the model-driven interfaces to their tasks
- [ ] My provisioning is idempotent, asserted, and confirm-committed
- [ ] My telemetry beat polling on a real failure
- [ ] My exam plan is weight-ordered against the verified blueprints
