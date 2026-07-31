# Chapter 08: Zero Trust Exchange, Scale, and the Boundary

## Learning Objectives

- Understand how the Zscaler Zero Trust Exchange delivers north-south access alongside east-west isolation.
- Understand scaling agentless isolation across VLANs and sites.
- Recognize the limits of the network-of-one approach.

## Hands-On Lab

### Exercise 8.1 — North-south access via the Zero Trust Exchange (design)

**Objective.** See how users reach applications without a flat network path.

**Design walkthrough.** East-west isolation stops lateral movement; **north-south access** — a user or remote technician reaching an application — is delivered by the **Zscaler Zero Trust Exchange (ZTE)**. Instead of putting the user on the network, ZTE brokers an identity-based, per-application tunnel (ZTNA): the user connects to Zscaler, Zscaler connects to the app, and the two are stitched only for that session. The user is never *on* the VLAN, so they cannot move laterally even if compromised — the same zero-trust principle as the network-of-one, applied to access.

**Expected result (on paper).** A design note: Airgap network-of-one for east-west isolation on the VLAN, Zscaler ZTE for identity-based north-south access, together covering both directions without a flat path anywhere.

**Cleanup.** None.

### Exercise 8.2 — Scale across VLANs and sites (design)

**Objective.** Understand estate-scale deployment.

**Design walkthrough.** An enforcement point is deployed per VLAN/site; policy and the kill switch are managed centrally, so isolation is uniform and an incident anywhere can be contained instantly. Because the approach is agentless and preserves addressing, rolling it out to a new VLAN is inserting an enforcement point, not re-architecting the network — the property that makes it deployable in brownfield OT and IT alike.

**Expected result (on paper).** A design note: one enforcement point per segment, central policy and kill switch, no re-addressing — segmentation added without disruption.

**Cleanup.** None.

### Exercise 8.3 — The boundary

**Objective.** Identify the limits of agentless network-of-one isolation.

**Track 1 & 2 — Walkthrough.** The approach has boundaries:

- **The enforcement point must be in the path.** A device on a segment with no enforcement point, or with an alternate path, is not isolated — coverage is per-segment.
- **It controls the network, not the host or the payload.** It stops lateral *reach*; it does not inspect application content or lock down the endpoint — pair it with an OT-protocol IPS and endpoint controls for those.
- **Correct ARP/DHCP control is essential.** If a device can still resolve peers directly (misconfiguration, static ARP), the isolation leaks.

```bash
echo "Network-of-one stops the reach; it does not inspect the payload or the host."
```

**Expected result.** A boundary note: deploy an enforcement point on every segment, verify ARP/DHCP control is complete, and pair the reach-isolation with protocol inspection (TXOne/Nozomi) and endpoint controls where content or host protection is needed.

**Negative test.** Assume network-of-one secures everything. It removes the lateral *path*; a permitted flow carrying a malicious payload, or a compromised host acting within its allowed flow, still needs inspection and endpoint control. Reach-isolation is one layer.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] The Zero Trust Exchange's north-south role alongside east-west isolation understood.
- [ ] Per-segment, agentless scaling understood.
- [ ] The path-coverage, payload, and ARP-control boundaries recognized.
- [ ] Complementary controls identified.
