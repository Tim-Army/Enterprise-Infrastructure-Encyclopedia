# Chapter 08: Protecting the Agentless PLC

## Learning Objectives

- Explain why an agentless, remote-firewall platform still cannot protect a device that exposes no manageable firewall.
- Enforce the PLC's protection on its managed neighbors and on the router path.
- Validate the whole containment end to end.

## The problem restated

Zero Networks is agentless, but "agentless" does not mean "manages anything". It protects a host by remotely programming that host's **own** firewall. The PLC (`zn-ot01`) exposes no manageable firewall — no RPC, no SSH into a controllable packet filter — so there is nothing for the platform to program. The answer is the same one every platform in this series reaches for the un-agentable device: enforce on the managed hosts around it, and on the single path that reaches it.

## Hands-On Lab

### Lab 8.1 — Enforce at the managed neighbors

**Objective.** Ensure that among the managed hosts, only `zn-win01` (HMI) can reach the PLC, and only on Modbus 502.

**Track 1 — Real Zero Networks.** The learned rules already permit only HMI→PLC:502; ensure the other managed hosts have no rule permitting the PLC and are Protected, so their remotely-programmed firewalls block that outbound traffic.

**Track 2 — Native equivalent.** On `zn-app01` and `zn-db01`, add an explicit, logged outbound deny to the PLC:

```bash
sudo nft add rule inet zeronet input ip daddr 10.10.30.50 log prefix "ZN-DENY plc: " level warn drop
# (outbound example if you also filter output on these hosts)
```

Ensure `zn-win01`'s outbound is default-deny with only the Modbus allow from Lab 7.3.

**Expected result.** Among managed hosts, only the HMI reaches the PLC, and only on 502.

**Negative test.** From `zn-app01`, `nc -vz 10.10.30.50 502` is blocked and logged; add a temporary permit and it succeeds, proving the deny stops it. Remove the permit.

**Cleanup.** Keep the enforcement.

### Lab 8.2 — Enforce the path on the router

**Objective.** Stop any source — including a device the platform cannot manage — from reaching the PLC on anything but Modbus from the HMI.

**Background.** Because `zn-gw` is a managed Linux host *and* the sole path to the OT cell, its remotely-programmed firewall can police transit to the PLC. In this lab you write that forward-path rule natively; in a real deployment it is the same native firewall Zero Networks would program on the gateway.

**Track 2 — Native equivalent.**

```bash
sudo nft add chain inet zeronet forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo nft add rule inet zeronet forward ip daddr 10.10.30.0/24 ct state established,related accept
sudo nft add rule inet zeronet forward ip saddr 10.10.20.21 ip daddr 10.10.30.50 tcp dport 502 accept
sudo nft add rule inet zeronet forward ip daddr 10.10.30.0/24 log prefix "ZN-FWD-DENY ot: " level warn drop
```

**Expected result.** The router forwards only the HMI's Modbus poll into the OT cell and drops everything else, logging denials.

**Negative test.** From `zn-app01`, `nc -vz 10.10.30.50 502` is blocked at the router even if `zn-app01`'s own deny were removed. The choke point makes the control complete.

**Cleanup.** Keep the forward chain.

### Lab 8.3 — Validate the containment end to end

**Objective.** Prove the design: legitimate flows survive, every attack path is dead, admin ports are gated.

**Walkthrough.**

From `zn-app01`: `~/checkdb.sh` → `3`; `nc -vz 10.10.30.50 502` → blocked.
From `zn-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # expect False
Test-NetConnection -ComputerName 10.10.20.12 -Port 22    # expect False (until a JIT grant)
```

**Expected result.**

| Flow | Before (Chapter 05) | After |
|:---|:---|:---|
| app→db 5432 | REACH | **REACH** (legitimate) |
| hmi→plc 502 | REACH | **REACH** (legitimate) |
| hmi→db 5432 | REACH | **BLOCK** |
| app→plc 502 | REACH | **BLOCK** |
| any→db 22 (standing) | REACH | **BLOCK** (JIT-only) |
| any→win 3389 (standing) | REACH | **BLOCK** (JIT-only) |

Both legitimate flows work; lateral movement is denied at source, destination, and path; and every administrative port is closed until a just-in-time, MFA-verified grant opens it.

**Negative test.** Revert `zn-db01` to the monitoring (permissive) posture and re-run the HMI→db probe; it reaches again. Monitoring observes; only enforcement blocks. Re-enforce.

**Cleanup.** Leave the enforced estate for Chapter 09.

## Summary and Completion Checklist

- [ ] The PLC is protected: managed hosts cannot reach it except the HMI on 502.
- [ ] Router path enforcement in place; unauthorized approaches logged.
- [ ] End-to-end validation table reproduced, including the closed admin ports.
- [ ] You can explain why agentless still cannot manage a device with no firewall.
