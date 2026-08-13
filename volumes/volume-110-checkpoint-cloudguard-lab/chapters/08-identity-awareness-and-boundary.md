# Chapter 08: Identity Awareness, Scale, and the Boundary

## Learning Objectives

- Add a user/machine dimension to the rulebase with Identity Awareness — a design exercise.
- Scale one policy across many gateways with a shared policy package.
- Recognize what the gateway cannot segment and pair it with a complementary control.

## Hands-On Lab

### Exercise 8.1 — Identity Awareness (design exercise)

**Objective.** Understand adding *who* to the source/destination/service/action rule.

**Design walkthrough.** **Identity Awareness** lets an access rule match an **access role** — a user, group, or machine identity from AD/Entra ID, an identity agent, or captive portal — as its source, so a rule reads "operators may reach the OT jump host" rather than "10.40.3.0/24 may." Combined with the tag-based objects of Chapter 06, a rule can require both the right workload tag *and* the right user identity:

```text
mgmt> mgmt_cli add access-role name "OT-Operators" \
        users "CN=OT-Operators,..." machines any --session-id "$SID"
mgmt> mgmt_cli set access-rule name "hmi-to-plc" layer "Network" \
        source.1 role_hmi source.2 OT-Operators --session-id "$SID"
```

**Expected result (on paper).** A rule that permits hmi→plc only when the traffic both originates from a `role_hmi` workload and carries an authenticated OT-operator identity — segmentation by workload *and* user, the granularity a pure network rule cannot express.

**Negative test (reasoning).** Assume network segmentation alone is enough for the OT jump path. A shared workstation used by any employee would pass a network-only rule; Identity Awareness is what ties the flow to authorized operators.

**Rollback.** None (design).

### Exercise 8.2 — Scale with one policy package across gateways

**Objective.** Understand estate-wide enforcement from one management server.

**Track 1 — Walkthrough.** A single **policy package** installs to many gateways, and **shared layers** let a common segmentation layer be reused across packages. Add a second gateway and install the same package:

```text
mgmt> mgmt_cli install-policy policy-package "Standard" access true \
        targets.1 gw targets.2 gw2 --session-id "$SID"
```

**Expected result.** Both gateways enforce the identical rulebase; the tag-based objects keep membership consistent across them. One authored policy, many enforcement points.

**Negative test.** Editing a rule but not re-installing leaves the gateways on the old policy — on Check Point, *install* is the action that changes enforcement, not *publish*. Always install after publishing.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.3 — The boundary

**Objective.** Identify traffic the gateway cannot see, and cover it.

**Track 1 & 2 — Walkthrough.** A gateway segments what **transits** it. It does not help with:

- **Intra-segment / same-subnet east-west** — two hosts on the same segment never reach the gateway. Separate them into segments/VLANs or add host controls.
- **Traffic on paths that bypass the gateway** — anything not routed through it.
- **Encrypted payloads** without HTTPS inspection.

```bash
sudo ip netns exec db bash -c 'nc -z -w2 10.40.2.11 5432 2>/dev/null || echo "intra-segment flow not seen by the gateway"'
```

**Expected result.** A boundary note: use segment/VLAN design to force sensitive flows through the gateway, enforce at the access edge for intra-segment traffic, and pair with host-based microsegmentation (Volumes XCIII–CVI) where the gateway has no path.

**Negative test.** Assume one flat segment with a "deny same-subnet" rule suffices — same-subnet traffic never reaches the gateway, so the rule never applies. Segmentation design decides what the gateway can enforce.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Identity Awareness understood as adding *who* to the rule.
- [ ] One policy package scaling across gateways understood.
- [ ] Publish-vs-install distinction internalized.
- [ ] Intra-segment and bypassed traffic recognized as the boundary.
