# Chapter 03: Building the Virtual Networks

## Learning Objectives

- Configure the three VMware underlay networks that carry the estate and, later, the encrypted overlay.
- Understand why the OT cell has no host adapter and no DHCP.
- Keep an out-of-band underlay management path that stays off the overlay.
- Verify each segment before building a single VM.

The three networks here are the **underlay**. The Airwall/WireGuard **overlay** (10.99.0.0/24) is built on top of them in Chapter 06 — it needs no VMware network of its own.

## Hands-On Lab

### Lab 3.1 — Configure VMnet8 (NAT — IT / Corporate)

**Objective.** Provide the "corporate" underlay segment with internet egress via NAT on `192.168.170.0/24` (protected devices need to reach the overlay hub and, in production, the Conductor).

**Walkthrough**

**Step 1.** Open **Edit → Virtual Network Editor** (elevate when prompted). Select **VMnet8**: Type **NAT**, Subnet `192.168.170.0/24`, **NAT gateway** `192.168.170.2`.

**Step 2.** Confirm the host's vNIC:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet8*" -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress
```

**Expected result.** Host holds `192.168.170.1`; NAT gateway `192.168.170.2`.

**Negative test.** Changing the subnet after building VMs breaks egress until re-addressed. Fix it now.

**Cleanup.** None.

### Lab 3.2 — Configure VMnet2 (host-only — Data Center)

**Objective.** Provide the underlay segment for the servers and HMI on `10.10.20.0/24`, with a host adapter for management and **no DHCP**.

**Walkthrough**

**Step 1.** Add **VMnet2**: Type **Host-only**, Subnet `10.10.20.0/24`. **Uncheck** local DHCP; **check** "Connect a host virtual adapter" (host gets `10.10.20.1`).

**Step 2.** Confirm:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet2*" -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress
```

**Expected result.** Host holds `10.10.20.1`; DHCP off. This underlay adapter deliberately stays *off* the overlay — it is your break-glass in Lab 9.2.

**Negative test.** Leaving DHCP on lets a lease renewal mask a blocked-flow result. Off is deliberate.

**Cleanup.** None.

### Lab 3.3 — Configure VMnet3 (host-only — OT Cell, fully isolated)

**Objective.** Provide the isolated OT underlay on `10.10.30.0/24` with **no host adapter** and **no DHCP**, reachable only through `aw-gw` — which will carry the PLC onto the overlay as a gateway.

**Walkthrough**

**Step 1.** Add **VMnet3**: Type **Host-only**, Subnet `10.10.30.0/24`. **Uncheck** local DHCP; **uncheck** "Connect a host virtual adapter".

**Step 2.** Confirm the host has no address on VMnet3:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet3*" -AddressFamily IPv4 -ErrorAction SilentlyContinue
```

**Expected result.** No output. Only `aw-gw` can reach the OT cell — exactly what an Airwall Gateway relies on to carry an un-agentable device onto the overlay.

**Negative test.** Ticking the host adapter here gives a path that bypasses the gateway; the PLC could then be reached off-overlay. Leave it unchecked.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] VMnet8 (NAT) `192.168.170.0/24`, host `.1`, gateway `.2`.
- [ ] VMnet2 (host-only) `10.10.20.0/24`, host `.1`, DHCP off.
- [ ] VMnet3 (host-only) `10.10.30.0/24`, **no host adapter**, DHCP off.
- [ ] Understood that the overlay (10.99.0.0/24) is built on these underlays in Chapter 06.
