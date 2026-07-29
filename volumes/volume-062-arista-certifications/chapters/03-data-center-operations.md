# Chapter 03: Data Center — Operations

## Learning Objectives

- Explain the Data Center Operations specialist scope.
- Operate a leaf-spine fabric and MLAG.
- Monitor fabric health and telemetry.
- Troubleshoot common data-center issues.
- Complete a walkthrough for each DC-Ops topic.

## Theory and Architecture

The **Data Center Track** leads to **Specialist** credentials, and the **Data Center
Operations (DC Ops)** specialization focuses on **operating** an Arista data-center fabric
day to day. Arista data centers are **leaf-spine** (Clos) fabrics — leaves connect hosts,
spines interconnect leaves — with **MLAG** (dual-homing hosts to two leaves without STP
blocking) and, at scale, **EVPN/VXLAN** (Chapter 04). Operations covers **health
monitoring** (interface/optics/environment via `show` and CloudVision telemetry), **change
verification**, and **troubleshooting** (link, LACP/MLAG, routing, and forwarding issues).

## Design Considerations

Operate the fabric with **telemetry-first** visibility (CloudVision streaming vs polling),
verify **MLAG** consistency, and troubleshoot systematically (physical → L2 → L3 →
forwarding). Keep configs consistent across the leaf-spine with automation.

## Implementation and Automation

The labs use EOS `show`/eAPI for fabric state, MLAG, and troubleshooting.

## Validation and Troubleshooting

Confirm the scope:

```text
DC Operations: operate leaf-spine + MLAG; monitor (show/optics/environment + CloudVision telemetry);
verify changes; troubleshoot (link/LACP/MLAG/routing/forwarding).
```

Common pitfalls: **MLAG** inconsistency (mismatched config between peers); and polling where
**streaming telemetry** gives real-time state.

## Security and Best Practices

Monitor with **streaming telemetry**, keep **MLAG** peers consistent, verify every change,
and troubleshoot **layer by layer**. Baseline fabric health so anomalies stand out.

## Hands-On Lab

DC-Operations walkthroughs. **Shared prerequisites** — a cEOS leaf-spine (containerlab) or
the patterns. **Cost:** none.

### Lab 3.1 — Verify fabric interfaces and optics

**Objective:** Check fabric link health.

```text
switch# show interfaces status
switch# show interfaces transceiver | include Et
```

**Expected result:** interface status and **optics/transceiver** data — fabric health
visibility.

**Negative test:** assume a "down" link is a config issue; check **optics/DOM** — it may be
a physical/transceiver fault.

**Cleanup:** none (read-only).

### Lab 3.2 — Verify MLAG

**Objective:** Confirm MLAG peer consistency.

```text
switch# show mlag
switch# show mlag interfaces detail
```

**Expected result:** MLAG state **Active/Consistent** with peer — dual-homing health.

**Negative test:** ignore an **Inconsistent** MLAG state; mismatched peer config causes
forwarding problems — reconcile it.

**Cleanup:** none (read-only).

### Lab 3.3 — Monitor with telemetry

**Objective:** Read fabric state programmatically.

```bash
curl -sS -k -u admin:admin https://<leaf>/command-api \
  -d '{"jsonrpc":"2.0","method":"runCmds","params":{"version":1,"cmds":["show interfaces counters rates"],"format":"json"},"id":1}' \
  | python3 -c "import sys,json;print('interfaces reporting rates:',len(json.load(sys.stdin)['result'][0].get('interfaces',{})))"
```

**Expected result:** per-interface **rate counters** via eAPI — programmatic monitoring
(CloudVision streams this fleet-wide).

**Negative test:** screen-scrape CLI for metrics; **eAPI/CloudVision telemetry** gives
structured, streamed data — use it.

**Cleanup:** none (read-only).

### Lab 3.4 — Troubleshoot a forwarding issue

**Objective:** Trace a reachability problem layer by layer.

```text
switch# show ip route 10.20.0.0/24
switch# show ip arp 10.20.0.10
switch# show mac address-table address 0011.2233.4455
```

**Expected result:** route → ARP → MAC evidence to localize the fault — the
troubleshooting methodology.

**Negative test:** reboot the switch hoping it fixes it; **trace L3→L2→forwarding** to find
the root cause.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Data Center Operations certifies running an Arista leaf-spine fabric: verifying interfaces/
optics and MLAG, monitoring with eAPI/CloudVision telemetry, and troubleshooting layer by
layer. This chapter checked fabric health, MLAG, telemetry, and traced a forwarding issue.

- [ ] I can verify fabric interfaces and optics.
- [ ] I can verify MLAG consistency.
- [ ] I can monitor fabric state via eAPI/telemetry.
- [ ] I can troubleshoot forwarding layer by layer.
- [ ] I completed Labs 3.1–3.4 including each negative test.
