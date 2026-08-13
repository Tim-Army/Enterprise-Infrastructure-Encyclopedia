# Chapter 03: Building the Virtual Networks

## Learning Objectives

- Configure the four VMware virtual networks that give this estate its shape.
- Understand why the database and the OT device each sit on their own segment behind the enforcement point.
- Keep out-of-band management paths that survive enforcement.
- Verify each segment before building a single VM.

This estate has **four** segments, one more than the other labs in the series: the database gets its own segment so that every access to it crosses the network enforcement point (`el-gw`).

## Hands-On Lab

### Lab 3.1 — Configure VMnet8 (NAT — IT / Corporate)

**Objective.** Provide the "corporate" segment with internet egress via NAT on `192.168.170.0/24`.

**Walkthrough**

**Step 1.** Open **Edit → Virtual Network Editor** (elevate when prompted). Select **VMnet8**: Type **NAT**, Subnet `192.168.170.0/24`, **NAT gateway** `192.168.170.2`.

**Step 2.** Confirm the host's vNIC:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet8*" -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress
```

**Expected result.** The host holds `192.168.170.1`; the NAT gateway is `192.168.170.2`.

**Negative test.** Changing the subnet after building VMs breaks egress until every guest is re-addressed. Fix it now.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Configure VMnet2 (host-only — Data Center)

**Objective.** Provide the segment for the app and HMI on `10.10.20.0/24`, with a host adapter for management and **no DHCP**.

**Walkthrough**

**Step 1.** Add **VMnet2**: Type **Host-only**, Subnet `10.10.20.0/24`. **Uncheck** local DHCP; **check** "Connect a host virtual adapter" (host gets `10.10.20.1`).

**Step 2.** Confirm:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet2*" -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress
```

**Expected result.** Host holds `10.10.20.1`; DHCP off.

**Negative test.** DHCP on lets a lease renewal mask a blocked-flow result. Off is deliberate.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Configure VMnet4 (host-only — Database)

**Objective.** Give the database its **own** segment on `10.10.40.0/24`, with a host adapter for out-of-band management and **no DHCP**, so all access to the database routes through `el-gw`.

**Walkthrough**

**Step 1.** Add **VMnet4**: Type **Host-only**, Subnet `10.10.40.0/24`. **Uncheck** local DHCP; **check** "Connect a host virtual adapter" (host gets `10.10.40.1`, your DB management/break-glass path).

**Step 2.** Confirm:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet4*" -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress
```

**Expected result.** Host holds `10.10.40.1`; DHCP off. The database will be the only workload here.

**Negative test.** Put the database back on VMnet2 with the app and HMI, and `el-gw` (a router) no longer sees app→db or HMI→db — they become intra-segment L2 traffic. Every enforcement result in Chapters 07–08 would then be untestable on this router-only lab. Keep the database on its own segment.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Configure VMnet3 (host-only — OT Cell, fully isolated)

**Objective.** Provide the isolated OT segment on `10.10.30.0/24` with **no host adapter** and **no DHCP**, reachable only through `el-gw`.

**Walkthrough**

**Step 1.** Add **VMnet3**: Type **Host-only**, Subnet `10.10.30.0/24`. **Uncheck** local DHCP; **uncheck** "Connect a host virtual adapter".

**Step 2.** Confirm the host has no address on VMnet3:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet3*" -AddressFamily IPv4 -ErrorAction SilentlyContinue
```

**Expected result.** No output — the host has no Layer 2 presence in the OT cell.

**Negative test.** Ticking the host adapter here gives a path that bypasses `el-gw`; enforcement results in Chapter 08 would be measured on the wrong path. Leave it unchecked.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] VMnet8 (NAT) `192.168.170.0/24`, host `.1`, gateway `.2`.
- [ ] VMnet2 (host-only) `10.10.20.0/24`, host `.1`, DHCP off.
- [ ] VMnet4 (host-only) `10.10.40.0/24`, host `.1`, DHCP off — database segment.
- [ ] VMnet3 (host-only) `10.10.30.0/24`, **no host adapter**, DHCP off — OT cell.
