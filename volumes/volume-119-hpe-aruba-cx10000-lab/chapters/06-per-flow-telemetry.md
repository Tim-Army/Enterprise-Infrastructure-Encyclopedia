# Chapter 06: Per-Flow Telemetry and Connection Visibility

## Learning Objectives

- Read the connection table the DPU maintains for every east-west flow.
- Use per-flow visibility to confirm what is permitted and see denies.
- Understand why in-fabric telemetry complements the stateful policy.

## The DPU sees every flow

Because the CX 10000's DPU tracks every connection, it also has **per-flow telemetry** for all east-west traffic in the rack — who is talking to whom, on what, for how long — without a separate tap or SPAN. That visibility is both an operational aid (spotting unexpected flows) and the raw material for tightening policy. This chapter reads the connection table on Track 2, the model of the DPU's flow view.

## Hands-On Lab

### Exercise 6.1 — Read the connection table

**Objective.** See the tracked connections for the permitted flows.

**Track 1 — Walkthrough.** In PSM the CX 10000 exposes per-session flow records and statistics for east-west traffic, so you can see every active connection and its policy verdict from the switch itself.

**Track 2 — Walkthrough.** Generate the permitted flows and read the conntrack table:

```bash
sudo ip netns exec web bash -c 'nc -w2 10.130.2.20 5432 </dev/null' &
sudo ip netns exec hmi bash -c 'nc -w2 10.130.4.40 502  </dev/null' &
sleep 1
sudo conntrack -L 2>/dev/null | grep -E '5432|502'
```

**Expected result.** Tracked connections for `10.130.1.10 → 10.130.2.20:5432` and `10.130.3.30 → 10.130.4.40:502` — the DPU's per-flow view, showing exactly the sanctioned east-west conversations.

**Negative test.** A denied flow (`hmi → db`) never establishes, so it does not appear as an established connection; it appears instead in the deny log — permitted flows in the connection table, denied ones in the log.

**Cleanup.** None.

### Exercise 6.2 — Denies and unexpected flows

**Objective.** Surface a denied/unexpected flow from the telemetry.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.2.20 5432; true'
echo "== denied east-west (from the fabric log) =="; sudo dmesg | grep -o 'CX-DENY.*SRC=10.130.3.30.*DPT=5432' | tail -1
echo "== active permitted flows =="; sudo conntrack -L 2>/dev/null | grep -c ESTABLISHED
```

**Expected result.** A `CX-DENY` record for the attempted `hmi → db`, plus a count of active established (permitted) flows — the two views together tell you what is allowed and what tried and failed.

**Negative test.** Without in-fabric telemetry you would need a separate SPAN/collector (as in the OT-monitoring volumes) to see east-west flows; the DPU provides it inline, which is a distinguishing benefit of doing enforcement in the fabric.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] The connection table for permitted flows read.
- [ ] Denied flows surfaced from the log.
- [ ] In-fabric per-flow telemetry understood.
- [ ] Why telemetry complements the stateful policy internalized.
