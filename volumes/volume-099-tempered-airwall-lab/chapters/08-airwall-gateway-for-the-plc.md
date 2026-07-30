# Chapter 08: The Airwall Gateway for the Agentless PLC

## Learning Objectives

- Explain how an Airwall Gateway carries a device that can run no agent onto the encrypted overlay.
- Configure `aw-gw` as the PLC's gateway and authorize only the HMI to reach it.
- Validate the whole containment end to end.

## The problem restated

`aw-ot01` is a PLC: no OS to host an Airwall Agent, no way to hold a cryptographic identity or a tunnel. Airwall's answer is the **Airwall Gateway** — an appliance placed in front of such a device that holds the identity and the encrypted tunnel *on the device's behalf*, and carries it onto the overlay. In this lab `aw-gw` already sits between the overlay and the isolated OT cell (it is the only path there), so it plays the gateway: it terminates the overlay and forwards authorized overlay traffic to the plain PLC, cloaking the PLC from everything else.

## Hands-On Lab

### Lab 8.1 — Carry the PLC onto the overlay via the gateway

**Objective.** Let the HMI reach the PLC over the encrypted overlay, through `aw-gw` acting as the PLC's gateway, and no one else.

**Track 1 — Real Airwall.** Deploy an Airwall Gateway in front of the PLC; it presents the PLC on the overlay behind its own identity. Place the gateway and the HMI's agent in one overlay network; the HMI now reaches the PLC through the encrypted overlay, and the PLC remains dark to everything else.

**Track 2 — Native equivalent.** `aw-gw` receives the HMI's overlay traffic on `wg0` and forwards the authorized flow to the PLC on the OT segment (`ens35`), source-NATing so the PLC replies back through the gateway:

```bash
# Allow only the HMI overlay identity -> PLC on Modbus 502, forwarded to the OT cell
sudo nft add rule inet airwall forward iifname "wg0" oifname "ens35" \
    ip saddr 10.99.0.21 ip daddr 10.10.30.50 tcp dport 502 accept
sudo nft add rule inet airwall forward iifname "wg0" oifname "ens35" \
    ip daddr 10.10.30.50 log prefix "AIRWALL-DENY plc: " level warn drop
# SNAT overlay->PLC so return traffic comes back through the gateway
sudo nft add rule ip nat postrouting oifname "ens35" ip saddr 10.99.0.0/24 masquerade
```

**Step 2.** From `aw-win01` (the HMI), reach the PLC over the overlay via the gateway. The HMI targets the PLC's address; the gateway carries it:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # HMI -> PLC via gateway/overlay: expect True
```

**Expected result.** The HMI reaches the PLC on 502 through the encrypted overlay and the gateway; the PLC never held a key or a tunnel of its own.

**Negative test.** From `aw-app01` (on the overlay but not authorized to the PLC), `nc -vz 10.10.30.50 502` — denied at the gateway (the `AIRWALL-DENY plc:` rule). Only the HMI identity is carried to the PLC.

**Cleanup.** Keep the gateway rules.

### Lab 8.2 — Confirm the PLC is dark except through the gateway

**Objective.** Verify the PLC is reachable only by the authorized identity, only on Modbus, only through the gateway.

**Walkthrough.** From `aw-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True  (authorized)
Test-NetConnection -ComputerName 10.10.30.50 -Port 22    # expect False (wrong service)
```

From `aw-app01`: `nc -vz 10.10.30.50 502` → blocked. And recall the Windows host has no adapter on the OT segment at all — so off the overlay, the PLC is unreachable by construction.

**Expected result.** Only *HMI → PLC on 502*, over the overlay through the gateway, succeeds; every other approach is denied or impossible.

**Negative test.** Broaden the gateway allow to `ip daddr 10.10.30.50 tcp dport 502 accept` (dropping the `saddr 10.99.0.21` match). Now any overlay member reaches the PLC — you widened the overlay around the controller. Restore the identity match.

**Cleanup.** Ensure the identity-matched gateway rule is restored.

### Lab 8.3 — Validate the containment end to end

**Objective.** Prove the design: legitimate flows survive on the encrypted overlay, every attack path is dead.

**Walkthrough.**

From `aw-app01`: `~/checkdb.sh 10.99.0.12` → `3`; `nc -vz 10.10.30.50 502` → blocked.
From `aw-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True  (via gateway/overlay)
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # underlay: expect False (cloaked)
Test-NetConnection -ComputerName 10.99.0.12  -Port 5432  # overlay:  expect False (not authorized)
```

**Expected result.**

| Flow | Path | Before (Chapter 05) | After |
|:---|:---|:---|:---|
| app→db 5432 | overlay (authorized) | REACH | **REACH** |
| hmi→plc 502 | overlay via gateway | REACH | **REACH** |
| hmi→db 5432 | underlay | REACH | **BLOCK** (cloaked) |
| hmi→db 5432 | overlay | n/a | **BLOCK** (not authorized) |
| app→plc 502 | overlay | REACH | **BLOCK** (not authorized) |

Both legitimate flows work over the encrypted overlay; every lateral-movement path is dead — the underlay is dark, and the overlay authorizes only the two relationships that exist. Data never crosses the wire in the clear.

**Negative test.** Stop WireGuard on `aw-db01` (`sudo systemctl stop wg-quick@wg0`) and re-run the app query over the overlay; it fails — no overlay, no connectivity, because there is no underlay path left either (the db is cloaked). The overlay is now the *only* way in, which is the point. Restart it.

**Cleanup.** Leave the enforced overlay for Chapter 09.

## Summary and Completion Checklist

- [ ] The PLC carried onto the overlay by the `aw-gw` gateway; only the HMI identity reaches it on 502.
- [ ] The PLC confirmed dark except through the gateway.
- [ ] End-to-end validation table reproduced; the underlay is dark and the overlay is encrypted.
- [ ] You can explain how an Airwall Gateway protects a device that can hold no identity of its own.
