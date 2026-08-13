# Chapter 08: Protecting the Agentless PLC

## Learning Objectives

- Explain Illumio's answer to a device that cannot host a VEN: represent it as an unmanaged workload and enforce its protection on the managed workloads around it.
- Enforce outbound policy on the managed estate so only the HMI may reach the PLC, and only on Modbus.
- Understand, honestly, where the host VEN stops and where a Network Enforcement Node or switch ACL takes over — and implement that path-based control natively on the router.

## The problem restated

`il-ot01` is a PLC. It has no general-purpose OS, no package manager, no place to put an agent — like most of the installed base of industrial controllers. ColorTokens answers this with an inline **Gatekeeper** appliance that becomes the device's gateway. Illumio Core answers it differently, and the difference is worth understanding rather than glossing:

- Illumio does not sell an inline appliance that sits in front of the PLC. Its enforcement lives on **managed** workloads.
- So the PLC is protected in two complementary ways: (1) every managed host that *could* reach it is put under Full Enforcement with **no** rule permitting the PLC — so their VENs block that traffic outbound; and (2) for path-based control of traffic from *unmanaged* sources, Illumio uses a **Network Enforcement Node (NEN)** that pushes ACLs to switches, or Illumio for OT. This lab has no managed switch, so you will implement that path control natively on `il-gw`, the single router every OT packet must cross — and you will label clearly which mechanism is doing the work.

## Hands-On Lab

### Lab 8.1 — Enforce at the managed neighbors (only the HMI may reach the PLC)

**Objective.** Ensure that among the managed hosts, only `il-win01` (HMI) can reach the PLC, and only on Modbus 502.

**Track 1 — Real Illumio.**

**Step 1.** You already created the PLC as an unmanaged workload (`il-ot01-plc`, `10.10.30.50`) in Lab 6.3, and allowed HMI→PLC 502 in Lab 7.3. Now confirm the *other* managed hosts have no rule permitting the PLC.

**Step 2.** Ensure `il-app01`, `il-db01`, and `il-gw` are at **Full Enforcement**. With no rule permitting them to reach `10.10.30.50`, their VENs block that outbound traffic. Provision.

**Track 2 — Native equivalent.**

**Step 1.** On `il-app01` and `il-db01`, add an explicit outbound deny to the PLC (their default-deny already covers it, but an explicit, logged rule makes the intent auditable):

```bash
# On il-app01 and il-db01 - these hosts must never reach the OT cell
sudo nft add rule inet illumio segmentation ip daddr 10.10.30.50 \
    log prefix "ILLUMIO-DENY plc: " level warn drop
```

**Step 2.** Confirm `il-win01`'s outbound rule from Lab 7.3 already restricts the HMI to 502 toward the PLC (it does — default-deny outbound plus the single Modbus allow).

**Expected result.** Among managed hosts, only the HMI can reach the PLC, and only on 502.

**Negative test.** From `il-app01`, try to reach the PLC: `nc -vz 10.10.30.50 502`. It is blocked and logged. Now temporarily add a permit and it succeeds — proving the deny, not the network, is what stops it. Remove the permit.

**Rollback.** Keep the managed-host enforcement.

### Lab 8.2 — Enforce the path on the router (the NEN's job, done natively)

**Objective.** Stop *any* source — including a hypothetical unmanaged or rogue host — from reaching the PLC on anything but Modbus from the HMI, by enforcing on the one link every OT packet crosses.

**Background.** The host VEN protects the endpoints it runs on. It does **not**, by default, police traffic merely *transiting* a Linux router. In production, path-based enforcement for unmanaged assets is a **Network Enforcement Node (NEN)** pushing an ACL to the switch, or Illumio for OT. Here you implement the same idea natively on `il-gw`'s forward path — and you should read this as "the native stand-in for a NEN," not "the Illumio host VEN."

**Track 1 — Design Exercise.** Describe how you would deliver this with Illumio: a NEN paired to the PCE, the PLC modelled as an unmanaged workload behind a managed switch, and the PCE compiling the HMI→PLC 502 rule into a switch ACL the NEN programs. State the one property of the lab topology (`il-gw` is the sole path to VMnet3) that makes a single enforcement point sufficient.

**Track 2 — Native equivalent.** Add a default-deny **forward** chain on `il-gw`, permitting only HMI→PLC 502 in transit:

```bash
sudo nft add chain inet illumio forward '{ type filter hook forward priority 0 ; policy accept ; }'
# Traffic destined to the OT cell is policed here:
sudo nft add rule inet illumio forward ip daddr 10.10.30.0/24 ct state established,related accept
sudo nft add rule inet illumio forward ip saddr 10.10.20.21 ip daddr 10.10.30.50 tcp dport 502 accept
sudo nft add rule inet illumio forward ip daddr 10.10.30.0/24 \
    log prefix "ILLUMIO-FWD-DENY ot: " level warn drop
```

**Expected result.** The router now forwards only the HMI's Modbus poll into the OT cell and drops everything else, logging denials — regardless of whether the source is managed.

**Negative test.** From `il-app01`, `nc -vz 10.10.30.50 502` — blocked at the router even though `il-app01`'s own outbound deny were removed. The choke point makes the control complete. This is exactly why "one path in" is a security property, not an inconvenience.

**Rollback.** Keep the forward chain.

### Lab 8.3 — Validate the containment end to end

**Objective.** Prove the whole design: the two legitimate flows survive, every attack path is dead.

**Walkthrough.**

**Step 1.** Re-run the regression from `il-app01`:

```bash
~/checkdb.sh                     # app -> db : expect 3
nc -vz 10.10.30.50 502           # app -> plc : expect blocked
```

**Step 2.** From `il-win01` (HMI / the compromised host):

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # HMI -> PLC : expect True
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # HMI -> DB  : expect False
Test-NetConnection -ComputerName 10.10.30.50 -Port 22    # HMI -> PLC other port : expect False
```

**Expected result.**

| Flow | Before (Chapter 05) | After |
|:---|:---|:---|
| app→db 5432 | REACH | **REACH** (legitimate) |
| hmi→plc 502 | REACH | **REACH** (legitimate) |
| hmi→db 5432 | REACH | **BLOCK** |
| app→plc 502 | REACH | **BLOCK** |
| hmi→plc 22 | REACH | **BLOCK** |

Both legitimate flows work; every lateral-movement path proven in Chapter 05 is now denied — at the source (managed VEN), at the destination (database ring-fence), and in the path (router).

**Negative test.** Revert `il-db01` to Visibility Only (Track 1) or flip its segmentation policy back to `accept` (Track 2) and re-run the HMI→db probe; it reaches again. Enforcement, not visibility, is what blocks — a reminder that a map alone protects nothing. Re-enforce.

**Rollback.** Leave the enforced estate for Chapter 09, which operates and then tears it down.

## Summary and Completion Checklist

- [ ] The PLC exists as an unmanaged workload; managed hosts cannot reach it except the HMI on 502.
- [ ] Router forward-path enforcement (the native NEN stand-in) in place and understood as such.
- [ ] End-to-end validation table reproduced: two flows allowed, all attacks blocked.
- [ ] You can explain how Illumio's agentless-device story differs from an inline appliance.
