# Chapter 06: CCTE — Troubleshooting

## Learning Objectives

- Capture and read traffic with fw monitor and tcpdump.
- Use kernel debugging (fw ctl zdebug) responsibly.
- Diagnose with cpview and the chain of inspection.
- Follow a structured troubleshooting method.
- Complete a walkthrough for each diagnostic topic.

## Theory and Architecture

The **CCTE (Certified Troubleshooting Expert, 156-588)** validates deep diagnostics. Check Point
inspects packets through a **chain of modules** (the "inspection chain"); understanding where a
packet is dropped is the key skill. **fw monitor** captures packets at four inspection points
(**i/I/o/O** — pre/post inbound and pre/post outbound), showing exactly where a packet is dropped or
translated — more precise than tcpdump for firewall logic. **tcpdump** captures raw traffic on an
interface (wire-level). **fw ctl zdebug drop** shows kernel drop reasons in real time (a focused
kernel debug), and full **fw ctl debug** modules trace specific subsystems. **cpview** gives live
resource and connection stats. A structured method — reproduce, capture at the right point, read the
drop reason, correlate with logs — resolves most issues. Troubleshooting is **read-only diagnosis**
of an authorized system.

## Design Considerations

Pick the **right tool**: tcpdump for wire-level, **fw monitor** for inspection-point logic,
**zdebug drop** for kernel drop reasons, **cpview** for resources. Debugs are verbose — **scope with
filters** and turn them **off** afterward (they load the CPU). Change one variable at a time.
Correlate captures with **SmartConsole logs**.

## Implementation and Automation

The labs capture with fw monitor and tcpdump, read drops with zdebug, and monitor with cpview.

## Validation and Troubleshooting

Confirm the method:

```text
Inspection chain: fw monitor points i/I (inbound pre/post) o/O (outbound pre/post) -> see where a packet dies.
tcpdump = wire-level. fw ctl zdebug drop = kernel drop reasons. cpview = live resources. Scope debugs; turn them OFF.
Method: reproduce -> capture at the right point -> read drop reason -> correlate with logs.
```

Common pitfalls: leaving a **kernel debug running** (CPU spike); and using tcpdump when the drop is
in firewall logic (use **fw monitor**).

## Security and Best Practices

Troubleshoot on **authorized** systems only. Use focused **filters**, capture at the right point, and
**disable debugs** immediately after. Correlate with logs. Never run verbose kernel debug on a busy
production gateway without care. Defensive diagnosis only.

## Hands-On Lab

Troubleshooting walkthroughs. **Shared prerequisites** — Check Point gateway (expert mode), a test
flow to diagnose. **Cost:** none.

### Lab 6.1 — Capture with fw monitor

**Objective:** See a packet through the chain.

```bash
# Capture one flow at all four inspection points (Ctrl-C to stop):
fw monitor -e "accept host(10.0.0.50);" 2>/dev/null | head \
  || echo "fw monitor points i/I/o/O show where the packet is seen or dropped in the inspection chain"
```

**Expected result:** the packet at inspection points **i/I/o/O** — showing where it passes or dies.

**Negative test:** debug a firewall drop with **tcpdump** only; it shows the wire, not the
inspection point — use **fw monitor** for firewall logic.

**Rollback:** stop the capture (Ctrl-C).

### Lab 6.2 — Capture with tcpdump

**Objective:** Wire-level capture.

```bash
tcpdump -nni eth0 host 10.0.0.50 and port 443 -c 20 2>/dev/null \
  || echo "tcpdump = raw packets on the interface; complements fw monitor"
```

**Expected result:** raw packets on eth0 for the host/port — wire-level confirmation.

**Negative test:** capture with **no filter** on a busy link; the output is unreadable — always
filter by host/port.

**Rollback:** none (capture stops at -c count).

### Lab 6.3 — Read kernel drops

**Objective:** Find the drop reason.

```bash
# Real-time kernel drop reasons (scope tightly; turn off promptly):
fw ctl zdebug + drop 2>/dev/null | head \
  || echo "fw ctl zdebug drop = kernel drop reason (e.g., rulebase drop, anti-spoofing) in real time"
```

**Expected result:** live **drop reasons** (e.g., rulebase, anti-spoofing) — the "why" behind a drop.

**Negative test:** leave `fw ctl zdebug`/`fw ctl debug` running; CPU spikes — **turn debugs off**
(`fw ctl debug 0`) immediately after.

**Rollback:** `fw ctl debug 0` to reset debug flags.

### Lab 6.4 — Diagnose resources with cpview

**Objective:** Correlate load with symptoms.

```bash
cpview     # CPU/memory/connections/throughput over time (navigate views; q to quit)
echo "cpview correlates high CPU/drops with the symptom; combine with fw monitor + logs"
```

**Expected result:** live resource trends — correlating **load/drops** with the reported problem.

**Negative test:** blame the network before checking gateway CPU/memory; **cpview** may show
saturation — check resources first.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CCTE troubleshooting reads the inspection chain: fw monitor (i/I/o/O), tcpdump (wire), fw ctl zdebug
drop (kernel reasons), and cpview (resources), following a reproduce → capture → read → correlate
method — always scoping debugs and turning them off.

- [ ] I can capture a flow with fw monitor.
- [ ] I can capture wire-level with tcpdump.
- [ ] I can read kernel drop reasons and turn debugs off.
- [ ] I can diagnose resources with cpview.
- [ ] I completed Labs 6.1–6.4 including each negative test.
