# Chapter 08: Security Director, Policy Enforcer, and the Boundary

## Learning Objectives

- Understand how Security Director and Policy Enforcer scale this policy across many SRX — a design exercise.
- Plan a safe rollout (staged permits, logging) before enforcing broadly.
- Recognize what the firewall cannot segment and pair it with a complementary control.

## Hands-On Lab

### Exercise 8.1 — Central management with Security Director (design exercise)

**Objective.** Understand how the hand-authored policy scales to an estate.

**Design walkthrough.** Editing zones and policies device by device does not scale. **Junos Security Director** centralizes policy authoring across many SRX; **Policy Enforcer** connects Security Director to threat intelligence (Juniper ATP Cloud, SecIntel feeds, third-party) and to the enforcement points — pushing the quarantine group membership of Chapter 06 automatically when a host is judged infected. In a production Connected Security deployment:

```text
ATP Cloud / SecIntel  --(verdict: host infected)-->  Policy Enforcer
Policy Enforcer  --(add to Infected-Hosts feed)-->  Security Director
Security Director  --(push dynamic-address update)-->  every SRX
SRX  --(standing deny-quarantine policy)-->  contains the host
```

**Expected result (on paper).** A design note: author zones/policies once in Security Director, template them across sites, and let Policy Enforcer drive dynamic containment from feeds — the same enforcement mechanics you built by hand, automated and estate-wide.

**Negative test (reasoning).** Assume threat feeds alone segment the network. They do not — feeds drive *reaction*; the *static* least-privilege policy (Chapter 05) is what stops lateral movement in the absence of any alert. You need both.

**Rollback.** None (design).

### Exercise 8.2 — Staged rollout

**Objective.** Tighten policy without an outage.

**Track 1 — Walkthrough.** Junos has no "monitor mode" like some fabrics, so stage the rollout with **logged permits first**: permit the intended flows with `then log session-init`, watch the logs to confirm only legitimate sessions appear, then remove the permit-any and let the default deny take over:

```text
set from-zone APP to-zone DB policy web-to-db then log session-init
# observe show log security, confirm only web->db:5432, then delete allow-all
```

**Track 2 — Walkthrough.** Model the staged rollout by logging would-be drops before switching them to real drops:

```bash
sudo nft add rule inet jsec forward ip saddr 10.20.3.10 ip daddr 10.20.2.10 log prefix '"WOULD-DENY "' accept
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432; true'
sudo dmesg | grep -c 'WOULD-DENY'
```

**Expected result.** The `WOULD-DENY` line appears while the flow still passes; replacing `accept` with `drop` enforces it. You proved the policy before it could cause an outage.

**Negative test.** Deleting the permit-any before authoring the specific permits denies the legitimate flows too — order the change as permit-first, then remove permit-any.

**Rollback.** Return to the enforcing ruleset from Chapter 05.

### Exercise 8.3 — The boundary

**Objective.** Identify traffic the SRX cannot see, and cover it.

**Track 1 & 2 — Walkthrough.** A firewall segments what **transits** it. It does not help with:

- **Intra-zone / same-subnet east-west** — two hosts in the same zone on the same switch never reach the SRX. Put sensitive peers in different zones, or add host controls / access-layer enforcement.
- **Encrypted or tunnelled payloads** the policy cannot inspect beyond L4 without decryption.
- **Endpoints the firewall never routes for** — anything on a bypassed path.

```bash
# same-subnet peers do not transit the enforcer host
sudo ip netns exec db bash -c 'nc -z -w2 10.20.2.11 5432 2>/dev/null || echo "intra-zone flow not seen by firewall"'
```

**Expected result.** A boundary note: separate sensitive peers into distinct zones, enforce at the access edge for intra-zone traffic, and pair the firewall with host-based microsegmentation (Volumes XCIII–CVI) where it has no path.

**Negative test.** Assume one big zone with an intra-zone deny suffices. Intra-zone traffic on the same L2 segment never reaches the SRX, so the deny never applies — zone design, not policy alone, determines what the firewall can enforce.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Security Director / Policy Enforcer scaling understood as automation of what you built.
- [ ] A staged, logged rollout practiced.
- [ ] Intra-zone and bypassed traffic recognized as the boundary.
- [ ] The boundary paired with a complementary control.
