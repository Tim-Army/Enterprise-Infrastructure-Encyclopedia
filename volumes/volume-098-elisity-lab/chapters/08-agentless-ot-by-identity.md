# Chapter 08: The Agentless PLC, Segmented by Identity

## Learning Objectives

- Explain why Elisity's identity-based, network-enforced model is a natural fit for agentless OT and IoT.
- Confirm the PLC is protected by the same network policy that protects everything else.
- Validate the whole containment end to end.

## The problem restated

Every other platform in this series treats the agentless PLC as a special case — a device that cannot host the agent the platform normally relies on, requiring a neighbor or an inline appliance. Elisity does not, and that is precisely its point: because it classifies from network context (not an agent) and enforces on the network (not the host), the PLC is **already** a first-class identity in the IdentityGraph and **already** policed at the enforcement point. The agentless device needs no special handling.

## Hands-On Lab

### Lab 8.1 — The PLC as an identity

**Objective.** Confirm the PLC is classified and policed exactly like every other asset, with no agent.

**Track 1 — Real Elisity.** The IdentityGraph classifies `el-ot01` as **PLC** from profiling and CMDB context. Policy references that identity: *HMI → PLC on 502 (allow)*, and the PLC is default-denied from everything else — the same policy engine, no OT-specific product.

**Track 2 — Native equivalent.** Confirm the PLC is in the graph and policed by the Chapter 07 rules:

```bash
sudo nft list set inet elisity grp_plc          # the PLC is a classified identity
sudo nft list chain inet elisity forward | grep -E "grp_plc|502"
```

**Expected result.** `grp_plc` contains `10.10.30.50`; the forward chain permits only `grp_hmi → grp_plc:502` and denies the rest — the same rules that protect the database protect the PLC.

**Negative test.** Try to add a host agent to `el-ot01` to "manage it like a server". It cannot take one — and it does not need to, because Elisity never depended on an agent. The agentless device is protected by classification and network enforcement, not by software on the device.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Tighten and confirm the OT boundary

**Objective.** Confirm the PLC accepts only the HMI's Modbus and nothing else, at the network.

**Walkthrough.** The Chapter 07 forward chain already denies all approaches to `grp_plc` except `grp_hmi → 502`. Verify other ports and other sources are dropped.

From `el-win01` (the HMI):

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True  (allowed identity + service)
Test-NetConnection -ComputerName 10.10.30.50 -Port 22    # expect False (allowed identity, wrong service)
```

From `el-app01` (an app server, not the HMI):

```bash
nc -vz 10.10.30.50 502   # expect blocked - wrong source identity
```

**Expected result.** Only *HMI → PLC on 502* passes; the HMI on other ports, and any other identity to the PLC, are dropped at `el-gw`.

**Negative test.** Broaden the OT allow to `ip daddr @grp_plc tcp dport 502 accept` (dropping the `grp_hmi` source match). Now *any* identity may reach the PLC on 502 — an app server, a compromised host. Identity on both ends of the rule is what makes it least-privilege. Restore the source match.

**Rollback.** Ensure the source-matched rule is restored.

### Lab 8.3 — Validate the containment end to end

**Objective.** Prove the design: legitimate flows survive, every attack path is dead — all at the network.

**Walkthrough.**

From `el-app01`: `~/checkdb.sh` → `3`; `nc -vz 10.10.30.50 502` → blocked.
From `el-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True
Test-NetConnection -ComputerName 10.10.40.40 -Port 5432  # expect False
```

**Expected result.**

| Flow | Identity | Before (Chapter 05) | After |
|:---|:---|:---|:---|
| app→db 5432 | AppServer→Database | REACH | **REACH** |
| hmi→plc 502 | HMI→PLC | REACH | **REACH** |
| hmi→db 5432 | HMI→Database | REACH | **BLOCK** |
| app→plc 502 | AppServer→PLC | REACH | **BLOCK** |
| hmi→plc 22 | HMI→PLC wrong service | REACH | **BLOCK** |

Both legitimate identity-to-identity flows work; every other approach to the protected identities is denied at the network enforcement point — with no agent on any endpoint.

**Negative test.** Flip the forward chain back to `policy accept` with no deny rules (Chapter 05 state) and re-run the HMI→db probe; it reaches again. The enforcement point enforces only what you compile onto it. Re-enforce.

**Rollback.** Leave the enforced estate for Chapter 09.

## Summary and Completion Checklist

- [ ] The PLC is a classified identity, policed by the same network policy as everything else.
- [ ] Only HMI→PLC on 502 passes; other ports and identities are denied.
- [ ] End-to-end validation table reproduced, with no endpoint agents anywhere.
- [ ] You can explain why identity-based network enforcement is a natural fit for agentless OT.
