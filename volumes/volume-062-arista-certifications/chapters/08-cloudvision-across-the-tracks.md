# Chapter 08: CloudVision Across the Tracks

## Learning Objectives

- Explain CloudVision's role across the ACE tracks.
- Provision devices with Studios and configlets.
- Use streaming telemetry and analytics.
- Govern change with Change Control.
- Complete a walkthrough for each CloudVision topic.

## Theory and Architecture

**CloudVision (CVP)** is Arista's single management plane across data center, campus, and
WAN — it appears in every ACE track. It provides **provisioning** (**Studios** — a modern,
abstracted, workflow-driven model — and legacy **configlets**), **streaming telemetry** (a
real-time state database of every device, replacing polling for analytics, dashboards, and
event history), **Change Control** (staged, reviewed, executed deployments with rollback and
snapshots), and services like **MSS** (Macro-Segmentation Service) for security insertion
and **network-wide search/analytics**. Because EOS streams state, CloudVision gives
fleet-wide visibility and governed change — the operational backbone the certifications
build on.

## Design Considerations

Provision with **Studios** (abstracted, reusable) over per-device configlets, rely on
**streaming telemetry** for real-time state, and gate all production changes through
**Change Control** (with snapshots/rollback). Use CloudVision as the single source of
operational truth across tracks.

## Implementation and Automation

The labs cover Studios/configlets, telemetry, Change Control, and the CloudVision API.

## Validation and Troubleshooting

Confirm the model:

```text
CloudVision: Studios/configlets (provision); streaming telemetry (real-time state/analytics);
Change Control (staged + reviewed + rollback + snapshots); MSS (segmentation); network-wide search.
```

Common pitfalls: per-device **configlets** where **Studios** scale better; and deploying
without **Change Control** snapshots.

## Security and Best Practices

Provision with **Studios**, monitor with **streaming telemetry**, gate changes through
**Change Control** with snapshots/rollback, segment with **MSS**, and secure CloudVision
access (RBAC, TLS, API tokens). Keep telemetry as the operational source of truth.

## Hands-On Lab

CloudVision walkthroughs. **Shared prerequisites** — a CloudVision instance (or CVaaS/the
patterns); an API token. **Cost:** none.

### Lab 8.1 — Provision with Studios/configlets

**Objective:** Describe abstracted provisioning.

```text
# Studios: fill a data-driven workflow (e.g., a fabric Studio) -> CloudVision builds configs.
# Configlets: static config snippets assigned to devices (legacy). Prefer Studios for scale.
"provision: Studios (workflow, reusable) > configlets (static)"
```

**Expected result:** the **Studios vs configlets** provisioning model — scalable
provisioning.

**Negative test:** assign a unique configlet per device; **Studios** generate from a model —
scale with them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Read streaming telemetry

**Objective:** Query device state via the CloudVision API.

```bash
curl -sS -H "Authorization: Bearer $CVP_TOKEN" \
  "https://<cvp>/api/resources/inventory/v1/Device/all" 2>/dev/null \
  | python3 -c "import sys,json;print('devices streaming to CVP:', sum(1 for _ in sys.stdin))" 2>/dev/null \
  || echo "query CloudVision inventory/telemetry via the resource APIs"
```

**Expected result:** the inventory of devices **streaming telemetry** to CloudVision —
real-time fleet state.

**Negative test:** poll each switch by SNMP for state; **streaming telemetry** is real-time
and scalable — use CloudVision.

**Rollback:** none (read-only).

### Lab 8.3 — Change Control

**Objective:** Deploy through a governed workflow.

```text
# Change Control: stage config changes -> optional snapshot -> review/approve -> execute ->
#   automatic rollback on failure. Batches changes across the fleet safely.
"change control: stage -> snapshot -> approve -> execute -> rollback-on-fail"
```

**Expected result:** the **Change Control** workflow — governed, reversible deployment.

**Negative test:** push config directly with no snapshot/approval; **Change Control** adds
review and rollback — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Network-wide search and MSS

**Objective:** Use CloudVision services.

```text
# Search: query state/events across the whole fleet from one place (e.g., find a MAC/host).
# MSS: CloudVision orchestrates firewall insertion/segmentation policy across the fabric.
"services: network-wide search + MSS segmentation from CloudVision"
```

**Expected result:** CloudVision **search** and **MSS** — fleet analytics and segmentation.

**Negative test:** log into each switch to find a host; **network-wide search** answers it
from one place.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CloudVision is the single management plane across all ACE tracks: Studios/configlets for
provisioning, streaming telemetry for real-time state, Change Control for governed
deployment, and services like search and MSS. This chapter covered each.

- [ ] I can describe Studios vs configlets provisioning.
- [ ] I can read streaming telemetry via the API.
- [ ] I can deploy through Change Control with rollback.
- [ ] I can use network-wide search and MSS.
- [ ] I completed Labs 8.1–8.4 including each negative test.
