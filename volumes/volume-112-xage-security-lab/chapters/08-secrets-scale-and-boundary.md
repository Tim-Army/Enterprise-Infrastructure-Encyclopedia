# Chapter 08: Secrets, Scale, and the Boundary

## Learning Objectives

- Rotate a credential and see access continue without a policy change.
- Understand how the fabric scales across sites and adds MFA and secure remote access.
- Recognize what identity brokering does not cover, and pair it with a complementary control.

## Hands-On Lab

### Exercise 8.1 — Rotate a credential

**Objective.** Change an identity's secret without touching the access policy.

**Track 1 — Walkthrough.** Xage rotates service credentials and enforces MFA for humans centrally; a rotation updates the credential the node verifies, and the access *policy* (who may reach what) is unchanged.

**Track 2 — Walkthrough.** Rotate `op-hmi`'s token and confirm the old one fails and the new one works — the grant is untouched:

```bash
sudo sed -i 's/TOKEN-HMI-7f3a/TOKEN-HMI-NEW01/' /etc/xage/identities
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n" | nc -w2 10.60.1.5 1502 || echo "old token DENIED"'
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-NEW01\n" | nc -w2 10.60.1.5 1502 && echo "new token OK"'
```

**Expected result.** The old token is denied and the new one works — credential rotation is independent of the access policy, so secrets can be rotated aggressively without re-authoring segmentation.

**Negative test.** If access were granted by IP, rotating a credential would do nothing to stop a stolen host — identity brokering is what makes rotation meaningful.

**Cleanup.** Leave the new token in place.

### Exercise 8.2 — Scale and remote access (design)

**Objective.** Understand the fabric at multi-site scale.

**Design walkthrough.** Enforcement nodes are deployed per site/cell and join one fabric; identities and policy replicate across them, so an operator authenticates once and is brokered to assets anywhere they are granted — including **secure remote access** to OT without a flat VPN into the plant. MFA, session recording, and just-in-time grants layer on top. The estate scales by adding nodes and identities, not by re-architecting the network.

**Expected result (on paper).** A design note: nodes per cell, one fabric, identities and policy replicated, MFA and session recording for humans, JIT grants for vendors — brokered access everywhere, no flat remote path.

**Cleanup.** None.

### Exercise 8.3 — The boundary

**Objective.** Identify what identity brokering does not cover.

**Track 1 & 2 — Walkthrough.** Brokered access controls **who reaches an asset through the broker**. It does not by itself cover:

- **Traffic that bypasses the broker** — if a device has any other network path, the broker is moot. The isolation (no direct route) is as important as the broker.
- **What an authorized identity does once connected** — brokering authorizes the session; protocol-aware inspection (an OT IPS) is needed to police the Modbus commands inside it.
- **Physical access** to the OT device or its cabling.

```bash
# a rogue path that skips the broker would defeat it — isolation must be complete
echo "If plc had a second NIC on a flat VLAN, the broker would be bypassed."
```

**Expected result.** A boundary note: pair identity brokering with strict isolation (no alternate path), an OT-protocol IPS for command-level control (see the TXOne volume), and monitoring (Claroty/Nozomi volumes) for detection.

**Negative test.** Assume the broker alone secures the PLC. If isolation is incomplete — any second path into the OT cell — the broker is bypassed. Brokering and isolation are one control, not two.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] A credential rotated without changing the access policy.
- [ ] Multi-site scale, MFA, and secure remote access understood.
- [ ] The bypass/inspection/physical boundary recognized and paired with controls.
