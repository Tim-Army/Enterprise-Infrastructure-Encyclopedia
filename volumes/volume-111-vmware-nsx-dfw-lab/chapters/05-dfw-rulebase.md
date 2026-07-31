# Chapter 05: The DFW Rulebase

## Learning Objectives

- Author DFW rules by group that permit only the two legitimate flows.
- Set the DFW default rule to Drop for zero-trust.
- Understand the **Applied To** field that scopes where a rule is enforced.
- Build the equivalent per-workload ruleset in Track 2.

## Rules by group, default Drop, applied at the vNIC

A DFW rule names a **source group**, a **destination group**, a **service**, an **action**, and an **Applied To** scope. Rules are ordered within a policy; the **default rule** is the catch-all you flip to **Drop** for zero-trust. Because enforcement is at the vNIC, a rule takes effect on the destination workload's own interface — which is why it can filter a same-subnet peer.

## Hands-On Lab

### Exercise 5.1 — Author the two permit rules

**Objective.** Permit Web→Database (PGSQL) and Operators→OT (MODBUS) by group.

**Track 1 — Walkthrough.** Create a security policy with two rules, each scoped **Applied To** the destination group so it is programmed on those VMs' vNICs:

```text
nsx> PATCH /policy/api/v1/infra/domains/default/security-policies/microseg
       rule web-to-db:   source_groups=[Web]       destination_groups=[Database] services=[PGSQL]  action=ALLOW  scope=[Database]
       rule hmi-to-plc:  source_groups=[Operators] destination_groups=[OT]       services=[MODBUS] action=ALLOW  scope=[OT]
```

**Expected result.**

```text
nsx> GET .../security-policies/microseg/rules | grep -E "display_name|action"
     web-to-db   ALLOW
     hmi-to-plc  ALLOW
```

**Negative test.** Using the built-in `ANY` service instead of `PGSQL` permits every port from Web to Database — scope the service. Source group + destination group + service is the microsegmentation granularity.

**Track 2 — Walkthrough.** Distributed enforcement means each workload filters its **own** inbound traffic. Program the db namespace to accept 5432 only from the Web group, and plc to accept 502 only from Operators — each at its own "vNIC":

```bash
# db enforces its own ingress
sudo ip netns exec db nft -f - <<'EOF'
table inet vnic {
  set g_web { type ipv4_addr ; elements = { 10.50.1.10 } }
  chain input { type filter hook input priority 0 ; policy drop ;
    ct state established,related accept
    iif "lo" accept
    ip saddr @g_web tcp dport 5432 accept
  }
}
EOF
# plc enforces its own ingress
sudo ip netns exec plc nft -f - <<'EOF'
table inet vnic {
  set g_hmi { type ipv4_addr ; elements = { 10.50.1.30 } }
  chain input { type filter hook input priority 0 ; policy drop ;
    ct state established,related accept
    iif "lo" accept
    ip saddr @g_hmi tcp dport 502 accept
  }
}
EOF
```

**Expected result.** Each workload now enforces at its own interface — the distributed model. The db namespace accepts 5432 only from web; plc accepts 502 only from hmi.

**Cleanup.** Keep the rules.

### Exercise 5.2 — Set the default to Drop

**Objective.** Make the DFW zero-trust so unlisted flows fail closed.

**Track 1 — Walkthrough.** Change the DFW **default layer-3 rule** action from Allow to Drop and publish:

```text
nsx> PATCH .../security-policies/default-layer3-section/rules/default-rule  action=DROP
```

**Expected result.**

```text
nsx> GET .../default-layer3-section/rules/default-rule | grep action
     action: DROP
# Operators->Database now falls through to the default Drop
```

**Negative test.** Leaving the default at Allow means `hmi → db` still passes despite the specific permits — the **default rule** is what makes DFW zero-trust. Specific allows over an allow-default is not microsegmentation.

**Track 2 — Walkthrough.** The per-namespace chains already use `policy drop`, which *is* the zero-trust default at each vNIC. Confirm web (which has no ingress rules of its own) drops unsolicited inbound while still making outbound connections:

```bash
sudo ip netns exec web nft -f - <<'EOF'
table inet vnic {
  chain input { type filter hook input priority 0 ; policy drop ;
    ct state established,related accept
    iif "lo" accept
  }
}
EOF
```

**Expected result.** Every workload defaults to drop-inbound; only the explicit accepts (db:5432 from web, plc:502 from hmi) let traffic in — zero-trust, distributed.

**Cleanup.** Keep the rulesets; Chapter 06 proves the same-subnet win, Chapter 07 verifies.

## Summary and Completion Checklist

- [ ] Web→Database (PGSQL) and Operators→OT (MODBUS) permitted by group.
- [ ] DFW default rule set to Drop (zero-trust).
- [ ] Applied To understood as scoping enforcement to the destination vNIC.
- [ ] Track 2 per-workload chains implement distributed default-drop.
