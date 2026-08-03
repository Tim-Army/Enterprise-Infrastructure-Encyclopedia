# Chapter 04: DPU-Enforced Microsegmentation

## Learning Objectives

- Apply a default-deny policy **in each DPU namespace** (not on the workload).
- Permit only each workload's sanctioned flow.
- Confirm the lateral flows are denied at the DPU.

## Policy lives in the DPU

Each BlueField DPU enforces its own host's traffic. On Track 2 the policy goes **in the DPU namespace** (`dpu-web`, `dpu-hmi`), which the workload cannot reach — so the enforcement is beside the workload but outside its control. This chapter applies default-deny plus the one permit in each DPU.

## Hands-On Lab

### Exercise 4.1 — Apply policy in each DPU

**Objective.** Default-deny in `dpu-web` and `dpu-hmi`, permitting only the sanctioned flow.

**Track 1 — Walkthrough.** In DOCA/partner segmentation you deploy each server's DPU a policy: default deny, permit the workload's sanctioned flow; the DPU enforces it at the NIC.

**Track 2 — Walkthrough.**

```bash
# DPU-web: permit only web -> db:5432
sudo ip netns exec dpu-web nft -f - <<'EOF'
table inet dpu { chain forward { type filter hook forward priority 0 ; policy drop ;
  ct state established,related accept
  ip saddr 10.140.1.10 ip daddr 10.140.0.20 tcp dport 5432 accept
  log prefix "DPU-WEB-DENY " drop
} }
EOF
# DPU-hmi: permit only hmi -> plc:502
sudo ip netns exec dpu-hmi nft -f - <<'EOF'
table inet dpu { chain forward { type filter hook forward priority 0 ; policy drop ;
  ct state established,related accept
  ip saddr 10.140.3.30 ip daddr 10.140.0.40 tcp dport 502 accept
  log prefix "DPU-HMI-DENY " drop
} }
EOF
```

**Expected result.** Each DPU enforces default-deny with one permit; the policy sits in the DPU namespaces, not the workloads.

**Negative test.** The policy is not in the workload namespaces — `sudo ip netns exec web nft list ruleset` shows nothing, yet web's traffic is filtered. Enforcement is beside the workload, not on it.

**Cleanup.** Keep the policies.

### Exercise 4.2 — The DPU policy holds

**Objective.** Confirm each workload's permitted flow works and the lateral flows are denied.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.20 5432 && echo "web->db OPEN"  || echo "web->db BLOCKED"'
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502  && echo "web->plc OPEN" || echo "web->plc BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.20 5432 && echo "hmi->db OPEN"  || echo "hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.40 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
web->plc BLOCKED
hmi->db BLOCKED
hmi->plc OPEN
```

Each workload reaches only its sanctioned target; the lateral flows are denied at the workload's own DPU.

**Cleanup.** Keep the policies for the out-of-band chapter.

## Summary and Completion Checklist

- [ ] Default-deny plus one permit applied in each DPU namespace.
- [ ] Policy confirmed to live in the DPU, not the workload.
- [ ] Each workload reaches only its sanctioned target.
- [ ] Ready to demonstrate the out-of-band advantage.
