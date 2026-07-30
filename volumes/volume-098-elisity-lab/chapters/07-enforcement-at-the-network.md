# Chapter 07: Identity-Based Enforcement at the Network

## Learning Objectives

- Enforce identity-based policy at the network point and confirm the intended flows survive while the attack is blocked.
- Prove that identity-based policy follows the identity, not the address.
- Understand why this model needs no endpoint changes at all.

You authored and validated identity-based policy in Chapter 06. Now you enforce it on `el-gw`, the network enforcement point standing in for the Elisity-managed access switch.

## Hands-On Lab

### Lab 7.1 — Enforce the identity-based policy

**Objective.** Permit AppServer→Database on 5432 and HMI→PLC on 502; deny every other approach to those protected identities.

**Track 1 — Real Elisity.** Move the policy from simulation to enforced. Elisity compiles the identity-based policy and, through the Virtual Edge, programs the access switches so only the permitted identity-to-identity flows pass.

**Track 2 — Native equivalent.** On `el-gw`, replace the observing forward chain with an enforcing one that references the IdentityGraph groups:

```bash
sudo nft flush chain inet elisity forward
sudo nft add rule inet elisity forward ct state established,related accept
# identity-based allows:
sudo nft add rule inet elisity forward ip saddr @grp_appserver ip daddr @grp_database tcp dport 5432 accept
sudo nft add rule inet elisity forward ip saddr @grp_hmi ip daddr @grp_plc tcp dport 502 accept
# default-deny toward the protected identities (everything not allowed above):
sudo nft add rule inet elisity forward ip daddr @grp_database log prefix "ELISITY-DENY db: " level warn drop
sudo nft add rule inet elisity forward ip daddr @grp_plc log prefix "ELISITY-DENY plc: " level warn drop
```

**Step 2.** Confirm the legitimate flows survive and the attack is blocked. From `el-app01`: `~/checkdb.sh` → `3`. From `el-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.40.40 -Port 5432   # HMI -> DB : expect False
Test-NetConnection -ComputerName 10.10.30.50 -Port 502    # HMI -> PLC: expect True
```

**Expected result.** AppServer→Database and HMI→PLC work; the HMI's lateral movement to the database is dropped at the network enforcement point and logged. Notice you changed **nothing on any endpoint** — all enforcement is on `el-gw`, exactly as Elisity enforces on the switch.

**Negative test.** Add `el-win01` to `grp_appserver` in the inventory, rebuild the IdentityGraph, and re-run the attack — it succeeds, because the HMI is now classified as an app server and inherits app-server access. Identity is policy; a misclassification is a hole. Restore the inventory and rebuild.

**Cleanup.** Keep the enforced policy.

### Lab 7.2 — Policy follows identity, not address

**Objective.** Show that re-addressing a workload does not break policy — the IdentityGraph re-binds the identity to its new address and the policy is unchanged.

**Track 1 — Real Elisity.** When a workload's IP changes, the connected sources update the IdentityGraph, and Elisity recompiles the switch policy automatically. The policy text — *AppServer → Database* — never changed.

**Track 2 — Native equivalent.** Simulate a re-address of the app server and watch policy follow.

**Step 1.** Change `el-app01`'s address to `10.10.20.15` (edit its netplan and `sudo netplan apply`), then update the source of truth and rebuild the graph:

```bash
# on el-gw, reflect the new address in the CMDB source and rebuild:
sudo sed -i 's/el-app01,10.10.20.11/el-app01,10.10.20.15/' /etc/elisity/inventory.csv
sudo /usr/local/bin/build-identitygraph.sh
```

**Step 2.** From `el-app01` (now `.15`), `~/checkdb.sh` → `3`. The policy rule (`@grp_appserver → @grp_database`) never changed; only the group membership updated.

**Expected result.** The app keeps its database access at its new address, with no policy edit — because policy names the identity, and the identity's address is resolved by the graph.

**Negative test.** Re-address the app but *forget* to update the source; the graph still lists the old address, and the app is denied. The model is only as live as its sources — which is why Elisity ingests continuously rather than relying on manual updates. (Restore `el-app01` to `.11` and rebuild.)

**Cleanup.** Ensure `el-app01` is back at `.11` and the graph rebuilt.

### Lab 7.3 — No endpoint agents (the model's point)

**Objective.** Confirm and reflect on the fact that the entire enforcement was achieved without touching a single endpoint.

**Walkthrough.** Review what you did in Labs 7.1–7.2: you built an IdentityGraph and wrote policy on `el-gw`. You installed no agent on `el-app01`, `el-db01`, `el-win01`, or `el-ot01`, and you changed no host firewall. That is the defining property of Elisity's model — it uses the network you already have and the identity sources you already run.

**Expected result.** A clear statement of the trade-off: no endpoint footprint and immediate coverage of un-agentable devices, at the cost of depending on the network's enforcement points (switches) and the fidelity of the identity sources.

**Negative test.** Argue you should "also" put agents on the servers for defense in depth. Nothing stops you (that is what the other volumes in this series do), but note that Elisity's value proposition — protect OT/IoT and unmanaged devices with no agent — evaporates if agents become mandatory. The point is coverage without an endpoint footprint.

**Cleanup.** None.

### Lab 7.4 — The Virtual Edge and live ingestion (Design Exercise)

**Objective.** Reason about the two capabilities with no faithful native stand-in.

**Design Exercise.**

1. In this lab you enforced on one Linux router. In a real network there are many access switches. Explain the role of the **Virtual Edge** connector and Elisity Cloud in compiling one identity-based policy into consistent enforcement across many switches — and why that is hard to do by hand.
2. Track 2 rebuilt the IdentityGraph by running a script. Explain what **live ingestion** from AD/Entra ID, vCenter, and EDR adds: classification that updates the instant a device's posture, owner, or attributes change, without anyone editing a CSV.

**Model answer.**

1. The Virtual Edge is the on-network broker that lets Elisity Cloud program the switches without cloud-to-switch direct exposure; Cloud holds the single identity-based policy and compiles it per switch platform, so *AppServer → Database* becomes the right ACL on a Catalyst, on another vendor's switch, and at every access point — consistently. By hand, you would translate and maintain that policy per device and per address change, which does not scale and drifts.
2. Live ingestion means the graph reflects reality continuously: a device that fails an EDR posture check, a VM retagged in vCenter, a user moved to a new AD group — each changes classification and therefore policy immediately. A CSV rebuilt manually is a snapshot that is stale the moment something moves.

**Expected result.** A written justification for cloud-compiled, continuously-ingested identity policy.

**Negative test.** Argue manual classification is "fine for a stable estate." Estates are not stable; the manual model fails exactly when it matters — during change, which is when attackers move.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Identity-based policy enforced at `el-gw`; AppServer→Database and HMI→PLC work, HMI→Database blocked.
- [ ] Policy shown to follow identity across a re-address, with no policy edit.
- [ ] The no-endpoint-agent property understood, with its trade-offs.
- [ ] Virtual Edge and live ingestion reasoned through.
