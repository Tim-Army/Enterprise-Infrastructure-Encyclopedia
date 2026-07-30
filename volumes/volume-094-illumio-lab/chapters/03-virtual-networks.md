# Chapter 03: Building the Virtual Networks

## Learning Objectives

- Configure the three VMware virtual networks that give the estate its shape.
- Understand why the OT cell has no host adapter and no DHCP.
- Add a host route so you retain an out-of-band management path into the Data Center segment.
- Verify each segment's reachability before you build a single VM.

## Hands-On Lab

### Lab 3.1 — Configure VMnet8 (NAT — IT / Corporate)

**Objective.** Provide the "corporate" segment with internet egress via NAT, on `192.168.170.0/24`.

**Walkthrough**

**Step 1.** Open **Edit → Virtual Network Editor** (elevate when prompted). Select **VMnet8**. Confirm:

- Type: **NAT**
- Subnet IP: `192.168.170.0`, Subnet mask: `255.255.255.0`
- **NAT Settings → Gateway IP:** `192.168.170.2`
- **DHCP:** enabled is fine for VMnet8, but every lab VM uses a static address, so it will not matter.

**Step 2.** Note the host's own vNIC address on this network:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet8*" -AddressFamily IPv4 |
    Select-Object InterfaceAlias, IPAddress
```

**Expected result.** The host holds `192.168.170.1` on the VMnet8 adapter; the NAT gateway is `192.168.170.2`.

**Negative test.** Change the VMnet8 subnet after building VMs and every guest loses egress until re-addressed. Fix the subnet now.

**Cleanup.** None.

### Lab 3.2 — Configure VMnet2 (host-only — Data Center)

**Objective.** Provide an internal, non-routed segment for the server tier on `10.10.20.0/24`, with a host adapter for out-of-band management but **no DHCP**.

**Walkthrough**

**Step 1.** In the Virtual Network Editor, add **VMnet2**:

- Type: **Host-only**
- Subnet IP: `10.10.20.0`, mask `255.255.255.0`
- **Uncheck** "Use local DHCP service to distribute IP addresses" — every server is static, and a stray DHCP server confuses segmentation labs.
- **Check** "Connect a host virtual adapter to this network" — this gives the host `10.10.20.1`, your break-glass path.

**Step 2.** Confirm the host adapter:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet2*" -AddressFamily IPv4 |
    Select-Object InterfaceAlias, IPAddress
```

**Expected result.** The host holds `10.10.20.1` on VMnet2. DHCP is off.

**Negative test.** Leave DHCP enabled here; when you later prove a policy blocks a host, a DHCP lease renewal can mask the result. Off is deliberate.

**Cleanup.** None.

### Lab 3.3 — Configure VMnet3 (host-only — OT Cell, fully isolated)

**Objective.** Provide a deliberately isolated segment for the OT device on `10.10.30.0/24`, with **no host adapter** and **no DHCP**, so the only path to it is through `il-gw`.

**Walkthrough**

**Step 1.** Add **VMnet3**:

- Type: **Host-only**
- Subnet IP: `10.10.30.0`, mask `255.255.255.0`
- **Uncheck** "Use local DHCP service…"
- **Uncheck** "Connect a host virtual adapter to this network" — this is the important one. The host must have no Layer 2 presence in the OT cell.

**Step 2.** Confirm the host has *no* address on VMnet3:

```powershell
Get-NetIPAddress -InterfaceAlias "*VMnet3*" -AddressFamily IPv4 -ErrorAction SilentlyContinue
```

**Expected result.** No output. The host cannot reach `10.10.30.0/24` directly — exactly the property that later lets `il-gw` be the single, complete enforcement point for the PLC.

**Negative test.** Tick "Connect a host virtual adapter" for VMnet3 and the host gains a direct path to the PLC that bypasses `il-gw`. Every enforcement result in Chapter 08 would then be a lie, because you would be testing from a host that does not traverse the choke point. Leave it unchecked.

**Cleanup.** None.

### Lab 3.4 — Plan the management route

**Objective.** Understand, before building VMs, how you will reach the Data Center servers for administration and how that path survives enforcement.

**Walkthrough**

**Step 1.** You will manage `il-app01`, `il-db01`, and `il-win01` over the VMnet2 host adapter (`10.10.20.1 → 10.10.20.0/24`). No extra route is needed; the host is directly attached.

**Step 2.** The OT cell (`10.10.30.0/24`) is reachable from the host only *through* `il-gw`. You will not add a host route to it — that is the point. When you need to test the PLC's reachability in Chapter 08, you will do it from `il-gw` or from a Data Center host, both of which legitimately transit the enforcement point.

**Expected result.** A clear mental model: two management-reachable segments (IT/NAT and Data Center) and one isolated segment reachable only via the router.

**Negative test.** Add a persistent host route `10.10.30.0/24 → 10.10.20.254` and then "prove" the PLC is blocked from the host; you would be measuring the wrong path. Do not add it.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] VMnet8 (NAT) on `192.168.170.0/24`, host at `.1`, gateway `.2`.
- [ ] VMnet2 (host-only) on `10.10.20.0/24`, host at `.1`, DHCP off.
- [ ] VMnet3 (host-only) on `10.10.30.0/24`, **no host adapter**, DHCP off.
- [ ] Management path understood; no route added to the OT cell.
