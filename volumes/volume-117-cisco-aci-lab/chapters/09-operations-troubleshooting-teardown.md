# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for EPG/contract segmentation.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is the whitelist working?"

**Track 1 — Walkthrough.** On the APIC: EPG membership resolves as expected, the intended contracts are provided/consumed, the VRF is in enforced mode, contract statistics move, and uSeg/intra-EPG policies are applied.

**Track 2 — Walkthrough.**

```bash
cat /etc/aci/epgs                                        # EPG membership
sudo nft list chain inet aci forward | grep -E "accept|drop|policy"   # contracts + whitelist default
sudo nft list set inet aci quarantine                    # uSeg quarantine members
sudo dmesg | grep -cE 'ACI-DENY|USEG-QUARANTINE|INTRA-EPG-DENY'       # denies recorded
```

**Expected result.** Membership correct, default-drop with the two contracts, quarantine as expected, denies recorded.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| All inter-EPG dropped | no contract, or VRF not enforced | contracts; enforced mode |
| Contracted flow blocked | filter wrong, or provide/consume not bound | contract subject/filter; relationships |
| Lateral flow permitted | VRF unenforced, or a permit-all contract | VRF mode; contract filters |
| Quarantine has no effect | uSeg rule after contracts, or attribute wrong | rule order; uSeg match |
| Intra-EPG peers still talk | intra-EPG isolation not enforced | EPG isolation setting |
| Endpoint in wrong EPG | classification/attribute mismatch | EPG/uSeg attributes |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The subtle failure is a **permit-all contract**: a contract whose filter allows any port defeats the whitelist between those EPGs. Scope every contract to its exact application ports.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet aci 2>/dev/null
for ns in web db db2 hmi plc; do sudo ip netns del $ns 2>/dev/null; done
for b in bd1 bd2 bd3 bd4; do sudo ip link del $b 2>/dev/null; done
sudo rm -rf /etc/aci
echo "teardown complete"
```

**Expected result.** Policy table, namespaces, bridge domains, and config removed.

**Negative test.** Leaving the `aci` table behind keeps enforcing on the host; remove it too.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Whitelist by contract, scoped to exact ports.** Deny is the default; a contract is a filtered exception.
- **Group by application role; refine by attribute.** EPGs for roles, uSeg for dynamic micro-segmentation and quarantine.
- **Isolate within EPGs where peers should not talk.** Intra-EPG isolation closes the last lateral path.
- **Enforce fabric-wide; stretch with Multi-Site.** One application policy, every leaf and site.
- **Insert inspection with service graphs** where L7 control is needed.
- **On-fabric plus complementary controls.** Pair ACI with host/cloud controls (Volumes XCIII–CXVI) for off-fabric workloads.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Contracts + uSeg + intra-EPG isolation internalized.
- [ ] Track 2 table, namespaces, bridge domains, and config removed.
