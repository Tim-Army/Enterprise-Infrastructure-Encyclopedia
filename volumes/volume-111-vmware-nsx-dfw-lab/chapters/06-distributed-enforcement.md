# Chapter 06: Distributed Enforcement and the Same-Subnet Win

## Learning Objectives

- Prove the DFW denies `hmi → db` between two VMs on the **same subnet** with no gateway.
- Understand why this is the property a centralized firewall cannot provide.
- See that the rule is enforced at the destination's own vNIC.

## The property that defines microsegmentation

Every earlier fabric/firewall volume reached the same honest boundary: two hosts on the same segment never transit the firewall, so intra-subnet traffic is a blind spot. **NSX DFW closes exactly that gap.** Because the rule lives at each VM's vNIC in the hypervisor, `hmi → db` is evaluated on the db VM's own interface — no routing, no chokepoint, no blind spot. This chapter demonstrates the win directly.

## Hands-On Lab

### Exercise 6.1 — Deny a same-subnet peer

**Objective.** Show `hmi → db` is dropped though both are on `10.50.1.0/24` with no router between them.

**Track 1 — Walkthrough.**

```text
# from hmi (10.50.1.30): nc db (10.50.1.20) 5432  -> dropped at db's vNIC
```

Confirm on the host that the rule is programmed at the db VM's filter:

```text
esxi> vsipioctl getrules -f <db-vnic-filter>
      rule ... match src=Web dst=Database svc=PGSQL action=allow
      rule ... default action=drop
```

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.50.1.20 5432 && echo web->db OPEN || echo web->db BLOCKED'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432 && echo hmi->db OPEN || echo hmi->db BLOCKED'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
```

`hmi → db` is blocked at db's own interface even though hmi and db are direct L2 peers — the same-subnet case no centralized firewall in Volumes CVII–CX could filter.

**Negative test.** On Track 2, flush db's `vnic` table (removing its distributed rule) and watch `hmi → db` succeed again — proof the enforcement was at db itself, not on any gateway. Re-apply db's ruleset from Chapter 05.

```bash
sudo ip netns exec db nft flush ruleset
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432 && echo hmi->db OPEN (rule removed)'
```

**Cleanup.** Restore db's ruleset.

### Exercise 6.2 — Confirm the legitimate same-subnet flow still works

**Objective.** Show `web → db` and `hmi → plc` still pass, also on the same subnet.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.50.1.20 5432 && echo web->db OPEN'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.40 502  && echo hmi->plc OPEN'
```

**Expected result.**

```text
web->db OPEN
hmi->plc OPEN
```

The legitimate same-subnet flows pass while the lateral one is denied — per-workload precision that does not depend on network topology at all.

**Negative test.** Try `web → plc:502` (not a permitted pair) — dropped at plc's vNIC, because plc only accepts 502 from Operators. Every workload independently enforces who may reach it.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] `hmi → db` denied between same-subnet peers with no gateway.
- [ ] The rule confirmed to be enforced at the destination's own vNIC.
- [ ] Legitimate same-subnet flows still pass.
- [ ] The distributed-firewall advantage over centralized models understood.
