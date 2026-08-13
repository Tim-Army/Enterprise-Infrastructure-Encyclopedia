# Chapter 08: Protecting the Agentless PLC

## Learning Objectives

- Explain why a telemetry-driven platform cannot baseline a device that emits no telemetry.
- Enforce the PLC's protection on its managed neighbors and on the router path.
- Validate the whole containment, including the service-account boundary, end to end.

## The problem restated

TrueFort reasons over host telemetry. The PLC (`tf-ot01`) runs no agent and no EDR, so it emits none — TrueFort sees it only as the far end of flows observed on other hosts. It cannot be baselined or enforced directly. The answer is the one every platform in this series reaches for the un-agentable device: enforce on the managed hosts around it, and on the single path that reaches it.

## Hands-On Lab

### Lab 8.1 — Enforce at the managed neighbors

**Objective.** Ensure that among managed hosts, only `tf-win01` (HMI) can reach the PLC, and only on Modbus 502.

**Track 1 — Real TrueFort.** The baselined behavior permits only HMI→PLC:502; ensure the other managed hosts have no permitted path to the PLC and are enforced, so their firewalls block that traffic.

**Track 2 — Native equivalent.** On `tf-app01` and `tf-db01`, add an explicit, logged deny to the PLC:

```bash
sudo nft add rule inet truefort input ip daddr 10.10.30.50 log prefix "TF-DENY plc: " level warn drop
```

Ensure `tf-win01`'s outbound is default-deny with only the Modbus allow from Lab 7.3.

**Expected result.** Among managed hosts, only the HMI reaches the PLC, and only on 502.

**Negative test.** From `tf-app01`, `nc -vz 10.10.30.50 502` is blocked and logged; a temporary permit makes it succeed, proving the deny stops it. Remove the permit.

**Rollback.** Keep the enforcement.

### Lab 8.2 — Enforce the path on the router

**Objective.** Stop any source — including a device that emits no telemetry — from reaching the PLC on anything but Modbus from the HMI.

**Background.** `tf-gw` is a managed host and the sole path to the OT cell, so its firewall can police transit to the PLC. In production this is a network integration; here you write it natively on the gateway.

**Track 2 — Native equivalent.**

```bash
sudo nft add chain inet truefort forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo nft add rule inet truefort forward ip daddr 10.10.30.0/24 ct state established,related accept
sudo nft add rule inet truefort forward ip saddr 10.10.20.21 ip daddr 10.10.30.50 tcp dport 502 accept
sudo nft add rule inet truefort forward ip daddr 10.10.30.0/24 log prefix "TF-FWD-DENY ot: " level warn drop
```

**Expected result.** The router forwards only the HMI's Modbus poll into the OT cell and drops everything else, logging denials.

**Negative test.** From `tf-app01`, `nc -vz 10.10.30.50 502` is blocked at the router even if `tf-app01`'s own deny were removed. The choke point makes the control complete.

**Rollback.** Keep the forward chain.

### Lab 8.3 — Validate the containment end to end

**Objective.** Prove the design: legitimate flows survive, every attack path — including service-account misuse — is dead.

**Walkthrough.**

From `tf-app01`: `sudo -u svcapp /opt/svcapp/checkdb.sh` → `3`; `nc -vz 10.10.30.50 502` → blocked.
From `tf-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # expect False
$env:PGPASSWORD='Svc!AppPassw0rd'; & psql -h 10.10.20.12 -U svc_app -d tflab -c "SELECT 1;"  # expect: no route / blocked
Remove-Item Env:\PGPASSWORD
```

**Expected result.**

| Flow | Before (Chapter 05) | After |
|:---|:---|:---|
| app→db 5432 (as svcapp) | REACH | **REACH** (legitimate) |
| hmi→plc 502 | REACH | **REACH** (legitimate) |
| hmi→db 5432 (stolen svc_app) | REACH | **BLOCK** (network) |
| non-svcapp→db on tf-app01 | REACH | **BLOCK** (identity) |
| app→plc 502 | REACH | **BLOCK** |

Both legitimate flows work; lateral movement is denied at source, destination, and path; and the stolen service account is useless both from the wrong host (network rule) and from the wrong process on the right host (identity rule).

**Negative test.** Revert `tf-db01` to the observing (permissive) posture and re-run the HMI misuse; it reaches again. Observation detects; only enforcement blocks. Re-enforce.

**Rollback.** Leave the enforced estate for Chapter 09.

## Summary and Completion Checklist

- [ ] The PLC is protected: managed hosts cannot reach it except the HMI on 502.
- [ ] Router path enforcement in place; unauthorized approaches logged.
- [ ] End-to-end validation table reproduced, including both service-account controls.
- [ ] You can explain why a telemetry-driven platform still needs neighbor enforcement for a silent device.
