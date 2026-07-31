# Chapter 08: Central Management, Scale, and the Boundary

## Learning Objectives

- Understand how EdgeOne/StellarOne manage many inline devices and endpoints at scale.
- See how TXOne pairs with the passive monitors of the previous volumes.
- Recognize the limits of inline protection and endpoint lockdown.

## Hands-On Lab

### Exercise 8.1 — Central management at scale (design)

**Objective.** Understand fleet management.

**Design walkthrough.** Many **EdgeIPS/EdgeFire** devices (one per cell) report to **EdgeOne**, and many **StellarProtect** agents to **StellarOne**; signatures, trust lists, and allowlists are distributed centrally, and a virtual patch for a newly-disclosed OT vulnerability can be pushed fleet-wide in minutes — protecting every instance of an unpatchable device at once. Each device stays transparent and inline at its own cell.

**Expected result (on paper).** A design note: one inline device per cell managed by EdgeOne, StellarProtect on each OT host managed by StellarOne, virtual patches and allowlists distributed centrally.

**Cleanup.** None.

### Exercise 8.2 — Pairing with passive monitors (design)

**Objective.** See where TXOne fits with Claroty/Nozomi.

**Design walkthrough.** The passive monitors (Volumes CXIII–CXIV) **see and decide** but delegate blocking; TXOne is the **inline enforcer** that does the blocking, plus the endpoint layer they lack. A complete OT program is: passive discovery and process baselining for visibility and detection, an inline OT IPS for transparent enforcement and virtual patching, and endpoint lockdown for the hosts — each covering what the others cannot.

**Expected result (on paper).** A layered design: monitor (Claroty/Nozomi) + inline enforce (TXOne EdgeIPS) + endpoint lockdown (StellarProtect) + identity brokering (Xage) for remote access.

**Cleanup.** None.

### Exercise 8.3 — The boundary

**Objective.** Identify the limits of inline + lockdown.

**Track 1 & 2 — Walkthrough.** TXOne's inline model has boundaries:

- **It must be in the path.** A cell reachable by a route that bypasses the inline device is unprotected; placement must cover every path.
- **A signature must exist.** Virtual patching blocks *known* exploits; a novel zero-day with no signature can pass — behavioral detection (Nozomi) complements it.
- **Allowlist maintenance.** Endpoint lockdown blocks the unknown, but legitimate software updates must be re-approved or they break.
- **Deep parsing needs the right protocol.** An unknown or encrypted OT protocol limits command filtering.

```bash
echo "Inline protects the paths it is on; lockdown protects the hosts it runs on. Cover every path and host."
```

**Expected result.** A boundary note: place inline devices on every path, pair virtual patching with behavioral detection for the unknown, maintain allowlists through change control, and cover hosts and network both.

**Negative test.** Assume one EdgeIPS secures the whole plant. It secures the cells it is inline for; a bypass path or an unprotected host is a gap. Coverage is a placement problem, not a product toggle.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Central management of inline devices and endpoints understood.
- [ ] TXOne's inline-enforcer role alongside passive monitors understood.
- [ ] The bypass, zero-day, and allowlist-maintenance boundaries recognized.
- [ ] Layered OT design articulated.
