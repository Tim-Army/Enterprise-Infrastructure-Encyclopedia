# Chapter 09: Design, Troubleshooting, and Certification Readiness

## Learning Objectives

- Apply a requirements-driven design method to data center projects,
  producing decisions that trace to constraints — DCID's discipline
- Run a structured troubleshooting methodology across network,
  compute, and storage, with evidence at every elimination — DCIT's
  discipline
- Operate the estate on purpose: upgrades, capacity, configuration
  management, and the management-and-operations practices DCIT
  weights at 20%
- Assemble a personal readiness plan for DCCOR and your chosen
  concentration, aligned to the verified blueprint weights

## Theory and Architecture

### Design as constraint satisfaction

DCID's four domains — network design 35%, compute 25%, storage 20%,
automation 20% — share one method. Gather **requirements**
(applications, growth, availability targets, compliance); surface
**constraints** (budget, facilities power/cooling — decisive since
Chapter 07 — existing estate, team skills); then make **traceable
decisions**. A design decision without a requirement behind it is
taste; the exam's scenario questions and real design reviews both
probe for the trace.

The recurring data center decisions, with their tension named:

- **ACI versus NX-OS/NDFC fabric**: policy model and integrations
  versus operational transparency and team familiarity. The deciding
  requirement is usually operational: who runs it, and what do they
  need to see?
- **Oversubscription ratios**: cost versus the applications' real
  concurrency — 3:1 general purpose, tighter for storage-heavy, 1:1
  for AI backends (Chapter 07's arithmetic).
- **Scale-up versus scale-out compute**: fewer bigger nodes (license
  economics, blast radius) versus more smaller ones (failure
  granularity, scheduling freedom).
- **Where inspection lives**: contracts/enforcement in-fabric versus
  service-graph steering through firewalls — decided by compliance
  requirements, not preference (Chapter 08).
- **Multi-site model**: EVPN Multi-Site or ACI Multi-Site for
  active-active tenancy, versus DR-oriented designs; RPO/RTO
  requirements decide, and they must be written down first.

### Troubleshooting as hypothesis elimination

DCIT's method, generalized from the ladders every chapter built:
**define the failure precisely** (who, to what, since when, what
changed); **draw the path** — for a data center flow that means
host → vNIC/profile → leaf → fabric → policy layer → storage or
peer; **split the path** at the easiest observable point and prove
each half; **consult the system's own diagnosis first** (ACI faults,
UCS FSM, FLOGI/FCNS, EVPN route presence — this volume's platforms
narrate their failures); and **change one thing**, verifying after.
The discipline that separates professionals: evidence at each step —
the counters, route entries, or fault codes that eliminated a layer —
because evidence survives handoffs and postmortems, and hunches do
not.

### Operations as a designed system

DCIT's Management and Operations domain (20%) is the chapter's third
leg. Upgrades: staged, rehearsed on virtual twins (CML, ACI
Simulator), rolled by automation with health asserts between waves —
ISSU where supported, maintenance-mode drains where not. Capacity:
watched as trends (telemetry into time series), acted on before the
fabric teaches the lesson. Configuration: rendered from source of
truth, drift-detected, snapshotted before every window (APIC
config-export, NX-OS checkpoints, UCS backups — all automatable, so
all automated). Incident practice: runbooks per failure class
(Chapters 02–08 each produced entries), postmortems that feed the
runbooks, and the on-call rotation actually drilled on the
break-glass path.

## Design Considerations

This section, unusually, is the chapter: the design method above
applied as a checklist for any new data center project —
requirements written and signed, constraints surfaced early
(facilities first for AI), decisions traced, failure domains drawn
on the diagram, operational model chosen with the team that will run
it, and day-2 tooling (telemetry, automation, backups) in the design
rather than appended after go-live.

## Implementation and Automation

The rehearsal pattern that makes upgrades boring, expressed as
pipeline stages (Chapter 06 tooling):

```yaml
# upgrade-wave.yml (conceptual stages)
- stage: preflight
  checks: [snapshot_taken, evpn_peers_established, vpc_consistent,
           faults_below_threshold, backup_verified]
- stage: drain
  action: maintenance-mode isolate {{ node }}     # GIR on NX-OS
- stage: upgrade
  action: install nxos {{ target_image }}
- stage: verify
  checks: [version_matches, evpn_peers_established, endpoints_relearned,
           copp_violations_flat]
- stage: restore
  action: maintenance-mode insert {{ node }}
- stage: soak
  wait: 30m
  checks: [no_new_faults, telemetry_deltas_nominal]
```

NX-OS Graceful Insertion and Removal (GIR) is the drain primitive:

```text
system mode maintenance      ! isolate: protocols withdraw gracefully
show system mode
system mode normal           ! reinsert after verification
```

Snapshot and checkpoint primitives worth muscle memory:

```text
checkpoint pre-change        ! NX-OS local checkpoint
rollback running-config checkpoint pre-change
show diff rollback-patch checkpoint pre-change running-config
```

## Validation and Troubleshooting

A worked elimination, the volume's flows in one scenario — "app tier
cannot reach its database, started 09:12": define (one EPG pair, all
endpoints, after a change window); path (VM → vNIC → leaf →
contract → leaf → VM); system's own diagnosis first — APIC faults
show a contract render failure on one leaf (fault code against the
zoning rule); evidence — `show zoning-rule` on that leaf missing the
entry present on its peers; cause — last night's automation ran
against a leaf mid-upgrade and skipped its assert (the Chapter 06
post-condition existed and was ignored — process failure, not tool
failure); fix — re-run render on that leaf, verify rule presence and
hit counters, then fix the pipeline so asserts gate the change
record. The postmortem writes itself because every step left
evidence — which is the point of the method.

## Security and Best Practices

- Rehearsed rollback is a security control: the fastest way out of a
  bad change is the difference between an incident and an outage.
- Upgrade currency is vulnerability management for infrastructure —
  the estate that fears its upgrade process accumulates CVEs with
  its technical debt (Chapter 03's ACI note, generalized).
- Evidence discipline doubles as audit readiness; the same artifacts
  serve postmortems and compliance.

## References and Knowledge Checks

- DCID 300-610 v1.2, DCIT 300-615 v1.2 exam topics (the method
  chapters' blueprints)
- Cisco NX-OS GIR and ISSU documentation; ACI upgrade guides
- This volume's chapters 02–08 runbook entries

Knowledge checks:

1. A design review asks for 1:1 oversubscription on a
   general-purpose fabric "to be safe." Argue from requirements —
   both the case against and the single workload class that changes
   the answer.
2. Name the drain-verify-restore primitives on NX-OS and in ACI
   terms, and where health asserts belong in the wave.
3. In the worked scenario, identify the two distinct failures — the
   technical one and the process one — and the artifact that caught
   each.
4. Build the weight-ordered study sequence for *your* concentration
   from the verified tables in this volume's README, and defend the
   ordering.

## Hands-On Lab

Capstone, on the full running estate of Chapters 01–08: (1) execute a
complete upgrade wave on one leaf — checkpoint, GIR drain, image
change simulated or real per lab constraints, verification asserts,
reinsertion, soak — with every stage's evidence captured; (2) have a
partner (or your past self, via a scripted fault injector) break one
thing anywhere in the estate; run the elimination method to
diagnosis, producing the evidence chain; (3) write the postmortem
and its runbook delta; (4) draft your personal exam plan: DCCOR
weeks mapped to weakest domains first, concentration chosen with a
sentence of justification, and mock-exam checkpoints scheduled.

## Lab Verification

Verification means the upgrade wave completed with all asserts green
and evidence archived, the injected fault was diagnosed by method
with its chain intact, and the postmortem and study plan exist.
Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Design traces decisions to requirements; troubleshooting eliminates
hypotheses with evidence; operations rehearses change until it is
boring. Those three disciplines are DCID and DCIT by name, but they
are also simply how the estate this volume built stays up. With the
core and five concentrations verified, mapped, and practiced, the
track is yours to schedule.

- [ ] My design checklist starts from requirements and facilities
- [ ] My elimination method leaves an evidence chain by habit
- [ ] My upgrade wave ran green end to end
- [ ] My exam plan is weight-ordered against the verified blueprints
