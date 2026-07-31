# Chapter 07: Enforcement and Verification

## Learning Objectives

- Prove the lateral `HMI → DB` flow is now denied while `WEB → DB` still works.
- Read `show cts role-based counters` to see permits and drops per cell.
- Correlate a denied flow with the ISE live log / the Track 2 drop counter.

## Hands-On Lab

### Exercise 7.1 — The lateral flow is denied

**Objective.** Confirm the matrix closes `HMI → DB` and preserves `WEB → DB`.

**Track 1 — Walkthrough.**

```bash
# legitimate: still permitted
web:  nc -z -w2 10.10.1.20 5432 && echo "web->db OPEN" || echo "web->db BLOCKED"
# lateral: now denied by the matrix default
hmi:  nc -z -w2 10.10.1.20 5432 && echo "hmi->db OPEN" || echo "hmi->db BLOCKED"
# operator control: still permitted
hmi:  nc -z -w2 10.10.1.40 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The lateral path is closed by group identity; both legitimate flows are untouched.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.10.1.20 5432 && echo web->db OPEN || echo web->db BLOCKED'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432 && echo hmi->db OPEN || echo hmi->db BLOCKED'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.40 502  && echo hmi->plc OPEN || echo hmi->plc BLOCKED'
```

**Expected result.** Same three lines — `hmi->db BLOCKED`, the others OPEN.

**Negative test.** Move the operator's binding to WEB (10) temporarily and watch `hmi → db` start working — proof the decision is made purely on the tag, not the address. Restore HMI (30) afterward.

**Cleanup.** Restore any temporary binding.

### Exercise 7.2 — Read the enforcement counters

**Objective.** See the fabric count the permits and drops per cell.

**Track 1 — Walkthrough.**

```bash
show cts role-based counters
# From    To    SW-Denied  HW-Denied  SW-Permit  HW-Permit
# 10      20    0          0          0          42          (WEB->DB permitted)
# 30      20    0          17         0          0           (HMI->DB denied)
# 30      40    0          0          0          8           (HMI->PLC permitted)
```

**Expected result.** Non-zero **permit** counters on 10→20 and 30→40, and non-zero **denied** counters on 30→20 — the drop of the lateral flow is visible and countable.

**Negative test.** Counters that stay all-zero mean traffic is not hitting the enforcer's egress path (asymmetric routing, wrong VLAN, or enforcement off). Zero counters during an active test is a misconfiguration signal, not success.

**Track 2 — Walkthrough.** Add counters to the drop rule and read them:

```bash
sudo nft flush chain inet cts forward
sudo nft add rule inet cts forward ip saddr 10.10.1.10 ip daddr 10.10.1.20 tcp dport 5432 counter accept
sudo nft add rule inet cts forward ip saddr 10.10.1.30 ip daddr 10.10.1.40 tcp dport 502 counter accept
sudo nft add rule inet cts forward ip saddr 10.10.1.0/24 ip daddr 10.10.1.0/24 counter drop
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432; true'
sudo nft list chain inet cts forward | grep counter
```

**Expected result.** The drop rule's counter increments after the `hmi → db` attempt — the Track 2 equivalent of the HW-Denied column.

**Cleanup.** None.

### Exercise 7.3 — Correlate the denial centrally

**Objective.** Find the denied flow in the policy engine's view, not just on the enforcer.

**Track 1 — Walkthrough.** In ISE, **Operations → TrustSec → (Live Logs / RBACL drop reports)** show per-cell drops reported by the NAD (when `cts role-based enforcement logging-interval` and monitoring are enabled). Enable drop logging on the NAD:

```text
nad(config)# cts role-based enforcement logging-interval 60
```

**Expected result.** The NAD reports `HMI → DB` drops to ISE, giving a central, per-group view of what the fabric is denying — the input to tightening policy safely.

**Track 2 — Walkthrough.** Log drops to the system journal:

```bash
sudo nft add rule inet cts forward ip saddr 10.10.1.0/24 ip daddr 10.10.1.0/24 log prefix '"CTS-DROP "' drop
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432; true'
sudo dmesg | grep -o 'CTS-DROP.*SRC=10.10.1.30.*DPT=5432' | tail -1
```

**Expected result.** A `CTS-DROP` log line naming source 10.10.1.30 (HMI) to port 5432 — the centralized evidence of the denial.

**Negative test.** Without the `log` rule, drops are silent; you would see the connection fail but have no record. Always log denies during a rollout so you can tell a working policy from a broken one.

**Cleanup.** Keep the logging for Chapter 09's operations review.

## Summary and Completion Checklist

- [ ] `HMI → DB` denied; `WEB → DB` and `HMI → PLC` permitted.
- [ ] Per-cell permit and deny counters observed.
- [ ] The denied flow correlated centrally (ISE live log / journal).
- [ ] The decision confirmed to depend on tag, not address.
