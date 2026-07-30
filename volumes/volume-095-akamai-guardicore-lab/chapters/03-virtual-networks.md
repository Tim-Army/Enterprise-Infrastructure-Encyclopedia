# Chapter 03: Building the Virtual Networks

## Learning Objectives

- Configure the three VMware virtual networks that give the estate its shape.
- Understand why the OT cell has no host adapter and no DHCP.
- Keep an out-of-band management path into the Data Center segment.
- Verify each segment before building a single VM.

## Hands-On Lab

### Lab 3.1 — Configure VMnet8 (NAT — IT / Corporate)

**Objective.** Provide the "corporate" segment with internet egress via NAT on `192.168.170.0/24`.

**Walkthrough**

**Step 1.** Open **Edit → Virtual Network Editor** (elevate when prompted). Select **VMnet8**: Type **NAT**, Subnet `192.168.170.0/24`, **NAT gateway** `192.168.170.2`.

**Step 2.** Note the host's vNIC address:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet8*" -AddressFamily IPv4 |
    Select-Object InterfaceAlias, IPAddress
```

**Expected result.** The host holds `192.168.170.1` on VMnet8; the NAT gateway is `192.168.170.2`.

**Negative test.** Changing the subnet after building VMs breaks egress until every guest is re-addressed. Fix it now.

**Cleanup.** None.

### Lab 3.2 — Configure VMnet2 (host-only — Data Center)

**Objective.** Provide an internal segment on `10.10.20.0/24` with a host adapter for management but **no DHCP**.

**Walkthrough**

**Step 1.** Add **VMnet2**: Type **Host-only**, Subnet `10.10.20.0/24`. **Uncheck** local DHCP; **check** "Connect a host virtual adapter to this network" (gives the host `10.10.20.1`).

**Step 2.** Confirm:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet2*" -AddressFamily IPv4 |
    Select-Object InterfaceAlias, IPAddress
```

**Expected result.** The host holds `10.10.20.1` on VMnet2; DHCP is off.

**Negative test.** Leaving DHCP on lets a lease renewal mask a blocked-flow test result. Off is deliberate.

**Cleanup.** None.

### Lab 3.3 — Configure VMnet3 (host-only — OT Cell, fully isolated)

**Objective.** Provide an isolated segment on `10.10.30.0/24` with **no host adapter** and **no DHCP**, so the only path to it is through `gc-gw`.

**Walkthrough**

**Step 1.** Add **VMnet3**: Type **Host-only**, Subnet `10.10.30.0/24`. **Uncheck** local DHCP; **uncheck** "Connect a host virtual adapter to this network".

**Step 2.** Confirm the host has no address on VMnet3:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet3*" -AddressFamily IPv4 -ErrorAction SilentlyContinue
```

**Expected result.** No output. The host cannot reach `10.10.30.0/24` directly — the property that later makes `gc-gw` the single, complete enforcement point for the PLC.

**Negative test.** Ticking the host adapter here gives the host a path that bypasses `gc-gw`; every enforcement result in Chapter 08 would then be measured on the wrong path. Leave it unchecked.

**Cleanup.** None.

### Lab 3.4 — Plan the management route

**Objective.** Know how you will reach the servers, and how that path survives enforcement.

**Walkthrough**

**Step 1.** You manage the Data Center hosts over the VMnet2 host adapter (`10.10.20.1`); no extra route is needed.

**Step 2.** The OT cell is reachable from the host only through `gc-gw`. You will not add a host route to it — testing the PLC in Chapter 08 is done from `gc-gw` or a Data Center host, which legitimately transit the enforcement point.

**Expected result.** Two management-reachable segments, one isolated segment reachable only via the router.

**Negative test.** Adding a host route `10.10.30.0/24 → 10.10.20.254` and then "proving" the PLC is blocked measures the wrong path. Do not add it.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] VMnet8 (NAT) on `192.168.170.0/24`, host `.1`, gateway `.2`.
- [ ] VMnet2 (host-only) on `10.10.20.0/24`, host `.1`, DHCP off.
- [ ] VMnet3 (host-only) on `10.10.30.0/24`, **no host adapter**, DHCP off.
- [ ] Management path understood; no route added to the OT cell.
