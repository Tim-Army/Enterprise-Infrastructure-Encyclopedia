# Chapter 04: Contracts — the Application-Centric Whitelist

## Learning Objectives

- Define contracts with filters for the two legitimate flows.
- Have EPGs provide and consume the contracts.
- Turn on the whitelist default so unlisted EPG pairs are denied.
- Build the equivalent EPG-to-EPG ruleset in Track 2.

## Deny between EPGs, permit by contract

In enforced ACI, traffic between two EPGs is dropped unless a **contract** permits it. A contract carries **filters** (protocol/port), one EPG **provides** it and the other **consumes** it. Microsegmentation is: define the contracts for the flows you need, bind provider/consumer, and rely on the whitelist default for everything else. This chapter applies the two contracts and denies the rest.

## Hands-On Lab

### Exercise 4.1 — Define the contracts and filters

**Objective.** Create `web-db` (tcp 5432) and `mgmt-ot` (tcp 502).

**Track 1 — Walkthrough.** On the APIC, create a filter for each port, a contract with a subject referencing that filter, then set `EPG-DB` to **provide** `web-db` and `EPG-Web` to **consume** it (and likewise `EPG-OT` provides / `EPG-Mgmt` consumes `mgmt-ot`):

```text
apic> Tenant > Contracts > Filters:  flt-pgsql (tcp/5432), flt-modbus (tcp/502)
apic> Contracts:  web-db (subject -> flt-pgsql), mgmt-ot (subject -> flt-modbus)
apic> EPG-DB provides web-db ; EPG-Web consumes web-db
apic> EPG-OT provides mgmt-ot ; EPG-Mgmt consumes mgmt-ot
```

**Expected result.** Two contracts, each with a port filter, bound provider→consumer.

**Negative test.** A contract with no filter (or `permit-all`) permits every port between the EPGs — the filter is what scopes the contract to the application. Always filter to the exact ports.

**Track 2 — Walkthrough.** Build the enforcement: default-deny between EPG subnets, permit the two contracted flows:

```bash
sudo nft add table inet aci
sudo nft add chain inet aci forward '{ type filter hook forward priority 0 ; policy drop ; }'
sudo nft add rule inet aci forward ct state established,related accept
# contract web-db: EPG-Web -> EPG-DB tcp/5432
sudo nft add rule inet aci forward ip saddr 10.110.1.10 ip daddr 10.110.2.20 tcp dport 5432 accept
# contract mgmt-ot: EPG-Mgmt -> EPG-OT tcp/502
sudo nft add rule inet aci forward ip saddr 10.110.3.30 ip daddr 10.110.4.40 tcp dport 502 accept
# whitelist default: deny (log) all other EPG-to-EPG
sudo nft add rule inet aci forward ip saddr 10.110.0.0/16 ip daddr 10.110.0.0/16 log prefix '"ACI-DENY "' drop
sudo nft list chain inet aci forward
```

**Expected result.** The forward chain permits exactly the two contracted flows and denies everything else between EPGs.

**Cleanup.** Keep the contracts.

### Exercise 4.2 — The whitelist holds

**Objective.** Confirm contracted flows work and the lateral flow is denied.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.110.2.20 5432 && echo web->db OPEN    || echo web->db BLOCKED'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.2.20 5432 && echo hmi->db OPEN    || echo hmi->db BLOCKED'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.4.40 502  && echo hmi->plc OPEN   || echo hmi->plc BLOCKED'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The two contracted flows pass; `EPG-Mgmt → EPG-DB` (hmi → db) is denied because no contract permits it — the whitelist default did the work, no explicit deny required.

**Negative test.** Remove the `web-db` accept rule and watch `web → db` break — proof it is the contract, not the routing, that permits the flow. Restore it.

**Cleanup.** Keep the enforcement for the next chapters.

## Summary and Completion Checklist

- [ ] Two contracts with port filters defined and bound provider/consumer.
- [ ] Whitelist default-deny between EPGs in force.
- [ ] Contracted flows pass; the lateral flow denied by default.
- [ ] Track 2 EPG-to-EPG ruleset matches the contracts.
