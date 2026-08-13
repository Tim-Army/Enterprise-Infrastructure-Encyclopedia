# Chapter 08: The Agentless PLC and Guardicore Detection

## Learning Objectives

- Protect a device that can run no agent by enforcing on its managed neighbors and on the router path.
- Reason about Guardicore's detection and deception coverage for the OT segment.
- Validate the whole containment end to end.

## The problem restated

`gc-ot01` is a PLC — no OS to host an agent, like most industrial controllers. Guardicore's answer has two parts, and it is worth stating both honestly:

1. **Enforce on the managed estate.** Every managed host that could reach the PLC is enforced with no rule permitting it, so the agents block that traffic. The one allowed path (HMI→PLC:502) is an explicit allow.
2. **Enforce the path and watch it.** For traffic from *unmanaged* sources, host agents cannot help; enforcement must live on the path. In production that is a network integration; in this lab it is native rules on `gc-gw`, the single link every OT packet crosses. Guardicore's **detection and deception** then turns the OT segment's "one allowed flow" into a tripwire: anything else is, by definition, suspicious.

## Hands-On Lab

### Lab 8.1 — Enforce at the managed neighbors

**Objective.** Ensure that among managed hosts, only `gc-win01` (HMI) can reach the PLC, and only on Modbus 502.

**Track 1 — Real Guardicore.** With the HMI→PLC 502 allow from Lab 7.3 in place, ensure `gc-app01`, `gc-db01`, and `gc-gw` have no rule permitting the PLC and are enforced; their agents block that outbound traffic.

**Track 2 — Native equivalent.** On `gc-app01` and `gc-db01`, add an explicit, logged outbound deny to the PLC:

```bash
sudo nft add rule inet guardicore segmentation ip daddr 10.10.30.50 \
    log prefix "GC-BLOCK plc: " level warn drop
```

**Expected result.** Among managed hosts, only the HMI reaches the PLC, and only on 502.

**Negative test.** From `gc-app01`, `nc -vz 10.10.30.50 502` is blocked and logged; add a temporary permit and it succeeds, proving the deny (not the network) stops it. Remove the permit.

**Rollback.** Keep the enforcement.

### Lab 8.2 — Enforce the path on the router

**Objective.** Stop any source — including a hypothetical rogue host — from reaching the PLC on anything but Modbus from the HMI.

**Background.** Host agents protect the endpoints they run on, not traffic merely transiting a router. In production, path enforcement for unmanaged assets is a network integration; here you implement it natively on `gc-gw`.

**Track 1 — Design Exercise.** Describe how you would deliver path enforcement with Guardicore for an unmanaged OT asset: the segment's single ingress (`gc-gw`) as the enforcement/observation point, the PLC modeled as a labeled asset, and the HMI→PLC 502 allow as the only permitted transit. State the topology property (`gc-gw` is the sole path to VMnet3) that makes one enforcement point sufficient.

**Track 2 — Native equivalent.**

```bash
sudo nft add chain inet guardicore forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo nft add rule inet guardicore forward ip daddr 10.10.30.0/24 ct state established,related accept
sudo nft add rule inet guardicore forward ip saddr 10.10.20.21 ip daddr 10.10.30.50 tcp dport 502 accept
sudo nft add rule inet guardicore forward ip daddr 10.10.30.0/24 \
    log prefix "GC-FWD-BLOCK ot: " level warn drop
```

**Expected result.** The router forwards only the HMI's Modbus poll into the OT cell and drops everything else, logging denials.

**Negative test.** From `gc-app01`, `nc -vz 10.10.30.50 502` is blocked at the router even if `gc-app01`'s own deny were removed. The choke point makes the control complete.

**Rollback.** Keep the forward chain.

### Lab 8.3 — Detection and deception on the OT segment (Design Exercise + native tripwire)

**Objective.** Turn the OT segment's single allowed flow into a detection signal, and reason about Guardicore's deception.

**Design Exercise.** Guardicore offers threat detection (reputation, indicators, and breadcrumbs) and **dynamic deception** — redirecting a suspicious connection to a decoy so the attacker's next move is observed rather than served. Explain why an OT segment with exactly one legitimate flow (HMI→PLC:502) is an ideal place for deception: any *other* connection attempt is unambiguously anomalous, so a decoy costs almost no false positives and yields high-fidelity alerts.

**Track 2 — Native tripwire.** You cannot reproduce Guardicore's deception, but you can build the high-fidelity alert its OT posture depends on: any non-HMI attempt to reach the PLC is logged as an incident. On `gc-gw`, watch the forward-deny log you created in Lab 8.2:

```bash
sudo journalctl -kf | grep "GC-FWD-BLOCK ot:"
```

From `gc-app01`, attempt the PLC: `nc -vz 10.10.30.50 502`. A `GC-FWD-BLOCK ot:` line appears — a precise, low-noise detection that something on the estate tried to reach the controller.

**Expected result.** Every unauthorized approach to the PLC is both blocked and logged as a distinct event.

**Negative test.** Widen the forward allow to `10.10.20.0/24 → PLC:502` "for convenience"; the tripwire goes silent for the whole Data Center segment, and an attacker on any DC host reaches the PLC unseen. Narrow allows are what make the detection meaningful.

**Rollback.** Stop the log tail.

### Lab 8.4 — Validate the containment end to end

**Objective.** Prove the design: legitimate flows survive, every attack path is dead.

**Walkthrough.**

From `gc-app01`: `~/checkdb.sh` → `3`; `nc -vz 10.10.30.50 502` → blocked.
From `gc-win01`:

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

Both legitimate flows work; every lateral-movement path from Chapter 05 is denied at the source, the destination, and the path — and unauthorized approaches to the PLC raise an alert.

**Negative test.** Revert `gc-db01` to alert-only and re-run the HMI→db probe; it reaches again. Detection alone protects nothing; enforcement does. Re-enforce.

**Rollback.** Leave the enforced estate for Chapter 09.

## Summary and Completion Checklist

- [ ] The PLC is protected: managed hosts cannot reach it except the HMI on 502.
- [ ] Router path enforcement in place; unauthorized approaches logged.
- [ ] Deception's fit for a single-flow OT segment reasoned through.
- [ ] End-to-end validation table reproduced.
