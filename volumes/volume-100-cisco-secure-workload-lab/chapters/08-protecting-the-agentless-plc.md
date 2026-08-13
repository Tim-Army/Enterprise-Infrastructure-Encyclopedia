# Chapter 08: Protecting the Agentless PLC

## Learning Objectives

- Explain why an agent-based platform cannot enforce on a device that runs no agent.
- Enforce the PLC's protection on its managed neighbors and on the router path.
- Validate the whole containment end to end.

## The problem restated

`cw-ot01` is a PLC: no OS to host the Secure Workload agent, so it enforces nothing itself and appears in telemetry only as the far end of the HMI's flows. The answer is the one every agent-based platform in this series reaches: enforce on the managed hosts around it, and on the single path that reaches it.

## Hands-On Lab

### Lab 8.1 — Enforce at the managed neighbors

**Objective.** Ensure that among managed hosts, only `cw-win01` (HMI) can reach the PLC, and only on Modbus 502.

**Track 1 — Real Secure Workload.** The discovered policy permits only HMI→PLC:502; ensure the other agents have no rule permitting the PLC and are enforced, so their host firewalls block that outbound traffic.

**Track 2 — Native equivalent.** On `cw-app01` and `cw-db01`, add an explicit, logged deny to the PLC:

```bash
sudo iptables -I CW-SEG -d 10.10.30.50 -j LOG --log-prefix "CW-DENY plc: "
sudo iptables -I CW-SEG -d 10.10.30.50 -j DROP
```

Ensure `cw-win01`'s outbound is default-deny with only the Modbus allow from Lab 7.3.

**Expected result.** Among managed hosts, only the HMI reaches the PLC, and only on 502.

**Negative test.** From `cw-app01`, `nc -vz 10.10.30.50 502` is blocked and logged; a temporary permit makes it succeed, proving the deny stops it. Remove the permit.

**Rollback.** Keep the enforcement.

### Lab 8.2 — Enforce the path on the router

**Objective.** Stop any source from reaching the PLC on anything but Modbus from the HMI, at the one link every OT packet crosses.

**Background.** `cw-gw` is a managed host and the sole path to the OT cell, so its firewall can police transit to the PLC. In production, path enforcement for an unmanaged asset is a network integration; here you write it natively on the gateway.

**Track 2 — Native equivalent.**

```bash
sudo iptables -N CW-FWD 2>/dev/null || sudo iptables -F CW-FWD
sudo iptables -A CW-FWD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A CW-FWD -s 10.10.20.21 -d 10.10.30.50 -p tcp --dport 502 -j ACCEPT
sudo iptables -A CW-FWD -d 10.10.30.0/24 -j LOG --log-prefix "CW-FWD-DENY ot: "
sudo iptables -A CW-FWD -d 10.10.30.0/24 -j DROP
sudo iptables -C FORWARD -j CW-FWD 2>/dev/null || sudo iptables -A FORWARD -j CW-FWD
```

**Expected result.** The router forwards only the HMI's Modbus poll into the OT cell and drops everything else, logging denials.

**Negative test.** From `cw-app01`, `nc -vz 10.10.30.50 502` is blocked at the router even if `cw-app01`'s own deny were removed. The choke point makes the control complete.

**Rollback.** Keep the forward chain.

### Lab 8.3 — Validate the containment end to end

**Objective.** Prove the design: legitimate flows survive, every attack path is dead.

**Walkthrough.**

From `cw-app01`: `~/checkdb.sh` → `3`; `nc -vz 10.10.30.50 502` → blocked.
From `cw-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # expect False
Test-NetConnection -ComputerName 10.10.30.50 -Port 22    # expect False
```

**Expected result.**

| Flow | Before (Chapter 05) | After |
|:---|:---|:---|
| app→db 5432 | REACH | **REACH** (legitimate) |
| hmi→plc 502 | REACH | **REACH** (legitimate) |
| hmi→db 5432 | REACH | **BLOCK** |
| app→plc 502 | REACH | **BLOCK** |
| hmi→plc 22 | REACH | **BLOCK** |

Both legitimate flows work; every lateral-movement path from Chapter 05 is denied at the source, the destination, and the path.

**Negative test.** Flush the enforcement (`sudo iptables -F CW-SEG`) and re-run the HMI→db probe; it reaches again. Discovery and analysis inform; only enforcement blocks. Re-enforce.

**Rollback.** Leave the enforced estate for Chapter 09.

## Summary and Completion Checklist

- [ ] The PLC is protected: managed hosts cannot reach it except the HMI on 502.
- [ ] Router path enforcement in place; unauthorized approaches logged.
- [ ] End-to-end validation table reproduced.
- [ ] You can explain why an agent-based platform still needs neighbor enforcement for an agentless device.
