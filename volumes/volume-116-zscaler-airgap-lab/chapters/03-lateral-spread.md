# Chapter 03: Lateral Spread on the Flat VLAN

## Learning Objectives

- Simulate a worm scanning and reaching every peer on the flat VLAN.
- Understand why a flat VLAN turns one infection into a plant-wide outbreak.
- Capture the single sanctioned flow that must survive isolation.

## One infection, everywhere

Ransomware does not need to defeat a firewall to spread across a flat VLAN — every device is already reachable. This chapter simulates a worm on the compromised `victim` finding and connecting to every peer, which is exactly the lateral movement Airgap's network-of-one eliminates. It also records the one flow that is legitimate, so isolation does not break the application.

## Hands-On Lab

### Exercise 3.1 — Simulate the worm's scan-and-spread

**Objective.** Show the compromised victim reaching every other device.

**Track 2 — Walkthrough.** A worm sweeps the /24 and connects to whatever answers:

```bash
sudo ip netns exec victim bash -c '
for ip in 10.100.1.10 10.100.1.20 10.100.1.30 10.100.1.40; do
  for p in 22 502 5432; do
    nc -z -w1 $ip $p 2>/dev/null && echo "SPREAD: victim reached $ip:$p"
  done
done'
```

**Expected result.** The worm reaches multiple peers, for example:

```text
SPREAD: victim reached 10.100.1.20:5432
SPREAD: victim reached 10.100.1.40:502
```

One compromised device found and connected to the database and the PLC — on a flat VLAN, the blast radius is the whole subnet.

**Negative test.** No firewall was bypassed and no credential was needed — the flat VLAN *is* the vulnerability. A control that only guards the perimeter does nothing against this east-west spread.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.2 — Record the one sanctioned flow

**Objective.** Note the single legitimate east-west flow so isolation preserves it.

**Track 1 & 2 — Walkthrough.**

```text
web (10.100.1.10) -> db (10.100.1.20) : tcp 5432   the only sanctioned east-west flow
```

Everything else east-west — including all of the worm's connections — is illegitimate.

**Expected result.** A one-line allow list. After isolation, only `web → db:5432` should survive; every other east-west path, including the worm's, must be gone.

**Negative test.** If isolation were done by broad subnet rules it might also break `web → db`; the network-of-one model isolates *by default* and re-permits the single flow explicitly, so nothing legitimate is guessed at.

**Rollback.** None — Chapter 04 isolates every device.

## Summary and Completion Checklist

- [ ] The worm shown reaching multiple peers on the flat VLAN.
- [ ] The flat VLAN understood as the lateral-movement vulnerability.
- [ ] The single sanctioned flow (web → db:5432) recorded.
- [ ] Ready to isolate every device into a network of one.
