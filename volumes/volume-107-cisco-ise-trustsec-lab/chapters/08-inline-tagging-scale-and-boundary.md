# Chapter 08: Inline Tagging, Scale, and the Boundary

## Learning Objectives

- Understand **inline SGT propagation (CMD)** and why it needs capable hardware — a design exercise.
- Plan a safe rollout with **monitor mode** before enforcement.
- Recognize the boundary: what TrustSec cannot tag, and how to cover it.

## Hands-On Lab

### Exercise 8.1 — Inline SGT propagation (design exercise)

**Objective.** Understand how SGTs travel *in the packet* rather than in SXP binding tables, and why this lab used SXP instead.

**Design walkthrough.** With **inline tagging**, a TrustSec-capable switch inserts the SGT into a **Cisco Meta Data (CMD)** field in the Layer 2 frame on egress, and the next hop reads it directly — no binding table, no SXP. This is the highest-fidelity propagation but requires ASICs that support CMD insertion (Catalyst 9000, Nexus, ASR/ISR with the right line cards). On a link between two capable switches you would configure:

```text
nadA(config-if)# cts manual
nadA(config-if-cts-manual)#  policy static sgt 10 trusted
```

and the peer trusts and forwards the tag. Because virtual IOS-XE images and this lab's Track 2 model cannot insert CMD, the lab used **SXP** — which distributes the *bindings* so an enforcer derives the SGT from the source IP instead of reading it off the wire.

**Expected result (on paper).** A design note stating: inline CMD for links between capable hardware; SXP to reach devices (or virtual/lab environments) that cannot read inline tags; both feed the same egress matrix. Enforcement logic is identical; only propagation differs.

**Negative test (reasoning).** Assume you can enable inline tagging everywhere in a mixed estate. You cannot — a non-capable hop strips the CMD field, so the tag is lost downstream. This is exactly why SXP exists and why real deployments are hybrid.

**Rollback.** None (design).

### Exercise 8.2 — Monitor mode before enforcement

**Objective.** Roll out the matrix without risking an outage by observing drops before enforcing them.

**Track 1 — Walkthrough.** TrustSec **monitor mode** lets the enforcer evaluate the matrix and *report* what it would deny without actually dropping:

```text
nad(config)# cts role-based monitor all
```

Run the workload, review the would-be drops in `show cts role-based counters` (monitored column) and ISE reports, confirm only illegitimate flows appear, then disable monitor mode to enforce for real:

```text
nad(config)# no cts role-based monitor all
```

**Expected result.** In monitor mode `HMI → DB` shows as a *monitored* drop while still passing; after disabling monitor mode it is a *real* drop. You proved the policy before it could cause an outage.

**Track 2 — Walkthrough.** Model monitor mode by logging instead of dropping, then switch to drop:

```bash
# monitor: log-only (no drop)
sudo nft flush chain inet cts forward
sudo nft add rule inet cts forward ip saddr 10.10.1.30 ip daddr 10.10.1.20 log prefix '"WOULD-DROP "' accept
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432; true'
sudo dmesg | grep -c 'WOULD-DROP'
```

**Expected result.** The `WOULD-DROP` line appears while the flow still succeeds — the safe preview. Replacing `accept` with `drop` enforces it.

**Negative test.** Enforcing a large matrix without a monitor-mode pass risks denying a flow you did not know was legitimate. Monitor mode is the standard, and skipping it is the classic TrustSec outage.

**Rollback.** Return the chain to the enforcing ruleset from Chapter 06.

### Exercise 8.3 — The boundary: what cannot be tagged

**Objective.** Identify traffic TrustSec cannot classify and pair it with a complementary control.

**Track 1 & 2 — Walkthrough.** TrustSec tags what passes through TrustSec-aware devices with a known binding. It does not help with:

- **Endpoints with no binding and no 802.1X** — they are `Unknown (0)`; decide deliberately whether Unknown is permitted or denied in the default row.
- **Intra-subnet traffic on a non-enforcing switch** — two hosts on the same access switch that does not enforce east-west never hit an SGACL. Enforce at the access layer, not only the distribution layer.
- **Encrypted overlays / third-party fabrics** that strip CMD — fall back to SXP or host controls.

```bash
# an Unknown endpoint (no binding) hitting the fabric
sudo ip netns exec web bash -c 'nc -z -w2 10.10.1.99 5432 || echo "unknown-dst unreachable / policy-dependent"'
```

**Expected result.** A short boundary note: set the Unknown row explicitly, enforce at the access edge, and cover un-taggable segments with host firewalls or a dedicated microsegmentation product (Volumes XCIII–CVI).

**Negative test.** Assume an empty Unknown row is safe. It defaults to the matrix default — if that is Permit IP, every unclassified device roams freely. The Unknown group must be a conscious decision.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Inline CMD vs SXP propagation understood; why this lab used SXP.
- [ ] Monitor mode practiced as the safe rollout path.
- [ ] The Unknown group and access-edge enforcement addressed.
- [ ] The boundary paired with a complementary control.
