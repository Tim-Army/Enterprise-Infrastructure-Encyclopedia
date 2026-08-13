# Chapter 05: uSeg Micro-EPGs

## Learning Objectives

- Reclassify an endpoint into a micro-EPG by **attribute**, independent of its base EPG.
- Quarantine a compromised endpoint by moving it into a deny-all micro-EPG.
- Understand why attribute-based classification is finer than port-based grouping.

## Segmentation by attribute, not just port

A base EPG groups endpoints by their network attachment; a **uSeg EPG (micro-EPG)** classifies by **attribute** — IP, MAC, or VM property — so an endpoint can be pulled into a different policy group *dynamically* without re-cabling or re-addressing. The classic use is **quarantine**: when an endpoint is flagged compromised, an attribute match moves it into a micro-EPG whose contracts permit nothing, isolating it instantly while everything else is unchanged.

## Hands-On Lab

### Exercise 5.1 — Define a quarantine micro-EPG

**Objective.** Create `uSeg-Quarantine` that matches a flagged attribute and permits nothing.

**Track 1 — Walkthrough.** On the APIC, create a uSeg EPG with a matching attribute (e.g. IP equals the compromised host, or a VM tag `quarantine=true`) and give it no contracts; any endpoint matching the attribute is reclassified into it and, having no contracts, is denied all communication.

```text
apic> uSeg EPG "uSeg-Quarantine": match attribute ip == 10.110.3.30 (or tag quarantine)
apic> (no contracts) -> matched endpoints are isolated
```

**Track 2 — Walkthrough.** Model the micro-EPG as a set that, when populated, overrides an endpoint's normal contracts with deny-all:

```bash
sudo nft add set inet aci quarantine '{ type ipv4_addr ; flags dynamic ; }'
# quarantine is consulted first: any member is dropped regardless of base-EPG contracts
sudo nft insert rule inet aci forward ip saddr @quarantine log prefix '"USEG-QUARANTINE "' drop
sudo nft insert rule inet aci forward ip daddr @quarantine drop
sudo nft list set inet aci quarantine
```

**Expected result.** An empty quarantine micro-EPG and a first-match rule that isolates any member — the reclassification override.

**Negative test.** Placing the quarantine rule *after* the contract permits would let a quarantined endpoint keep a contracted flow — the uSeg override must be evaluated first, like a top-priority micro-EPG.

**Rollback.** Keep the micro-EPG.

### Exercise 5.2 — Quarantine a compromised endpoint

**Objective.** Reclassify the operator host by attribute and watch it lose all access.

**Track 2 — Walkthrough.** The operator `hmi` (10.110.3.30) is flagged compromised; the attribute match moves it into `uSeg-Quarantine`:

```bash
sudo nft add element inet aci quarantine '{ 10.110.3.30 }'
# its previously-contracted flow (hmi -> plc) is now denied
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.4.40 502 && echo "hmi->plc OPEN" || echo "hmi->plc QUARANTINED"'
```

**Expected result.** `hmi->plc QUARANTINED` — the endpoint that had a valid `mgmt-ot` contract is now isolated because its attribute pulled it into the deny-all micro-EPG, with no change to any contract.

**Negative test.** Remove it from quarantine and its contracted access returns:

```bash
sudo nft delete element inet aci quarantine '{ 10.110.3.30 }'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.4.40 502 && echo "hmi->plc OPEN (released)"'
```

`hmi->plc OPEN (released)` — membership, driven by attribute, decided isolation; the base contracts never changed.

**Rollback.** Leave `hmi` out of quarantine for the remaining chapters.

## Summary and Completion Checklist

- [ ] A deny-all quarantine micro-EPG created and evaluated first.
- [ ] A compromised endpoint reclassified by attribute and isolated.
- [ ] Releasing it restored its contracted access.
- [ ] Attribute-based micro-segmentation understood as finer than base EPGs.
