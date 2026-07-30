# Chapter 03: Building the Virtual Networks

## Learning Objectives

- Pin the NAT segment to a known subnet so the address plan holds.
- Build a host-only data-center segment with DHCP disabled.
- Build an isolated OT cell with no host adapter — the Gatekeeper precondition.
- Add a host route so the lateral-movement path exists to be denied later.

The three segments are the skeleton of the entire lab. Get them exactly
right and everything after works; get an IP wrong here and you will
spend Part D confused.

## Hands-On Lab

### Lab 3.1 — Configure VMnet8 (NAT) as the IT/Corporate segment

**Objective.** Pin the NAT network to a known subnet so the guide’s
addresses match yours.

**Walkthrough**

**Step 1.** Launch the Virtual Network Editor with elevation — this is
the step people miss.

```powershell
Start-Process -FilePath "C:\Program Files\VMware\VMware Workstation\vmnetcfg.exe" -Verb RunAs

```

Alternatively, from Workstation: **Edit → Virtual Network Editor**, then
click **Change Settings** at the bottom and accept the UAC prompt.
Without elevation the fields are read-only and you will think the tool
is broken.

**Step 2.** Select **VMnet8** in the list. Confirm or set:

- Type: **NAT (share the host’s IP address with VMs)**
- **Subnet IP:** `192.168.170.0`
- **Subnet mask:** `255.255.255.0`
- **Connect a host virtual adapter to this network:** **checked**
- **Use local DHCP service to distribute IP addresses to VMs:**
  **checked**

**Step 3.** Click **NAT Settings…** and confirm:

- **Gateway IP:** `192.168.170.2`

Leave port forwarding empty. Click **OK**.

**Step 4.** Click **DHCP Settings…** and confirm the pool does not
collide with our static addresses:

- **Starting IP address:** `192.168.170.128`
- **Ending IP address:** `192.168.170.254`

We statically assign `192.168.170.10` to `ct-gw`, comfortably below the
pool. Click **OK**.

**Expected result.** VMnet8 is NAT on `192.168.170.0/24`, gateway `.2`,
DHCP serving `.128`–`.254`.

**Negative test.** Set the DHCP pool to start at `192.168.170.1`
instead. A DHCP client will eventually be handed `192.168.170.10`,
colliding with `ct-gw`’s static address, and you will get intermittent,
maddening connectivity loss. Duplicate-address bugs are the classic lab
time sink — set the pool correctly and move on.

**Cleanup.** None.

### Lab 3.2 — Create VMnet2 as the Data Center segment

**Objective.** Build a host-only segment with **no DHCP**, so that every
address is one you chose.

**Walkthrough**

**Step 1.** In the Virtual Network Editor, click **Add Network…**,
choose **VMnet2**, click **OK**.

**Step 2.** With VMnet2 selected, configure:

- Type: **Host-only (connect VMs internally in a private network)**
- **Connect a host virtual adapter to this network:** **checked** ← this
  is your management path
- **Use local DHCP service to distribute IP addresses to VMs:**
  **UNCHECKED** ← important
- **Subnet IP:** `10.10.20.0`
- **Subnet mask:** `255.255.255.0`

**Step 3.** Click **Apply**.

Why disable DHCP? Two reasons. First, static addressing throughout means
the address plan in Chapter 01 (Address plan) is the truth, always. Second — and this
is the real lesson — microsegmentation policy is written against
identity, and in a lab the closest thing to stable identity is a stable
address. In production you would use Xshield **tags**, precisely so that
policy survives an address change. You will meet tags in Lab 7.2.
Here, statics keep the plumbing out of the way.

Note that the Windows host takes `10.10.20.1` on its virtual adapter for
VMnet2 automatically. That is why `ct-gw` uses `.254` on this segment
rather than the more conventional `.1`.

**Step 4.** Verify from the host after applying:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object InterfaceAlias -like "*VMnet*" |
    Format-Table -AutoSize InterfaceAlias, IPAddress, PrefixLength

```

Expected:

```text
InterfaceAlias        IPAddress      PrefixLength
--------------        ---------      ------------
VMware Network Adapter VMnet2   10.10.20.1               24
VMware Network Adapter VMnet8   192.168.170.1            24

```

**Expected result.** VMnet2 exists as host-only on `10.10.20.0/24` with
DHCP off and a host adapter at `10.10.20.1`.

**Negative test.** Leave DHCP enabled on VMnet2. Boot `ct-app01` before
you configure its static address and it will pick up a lease from the
VMware DHCP server on an address you did not plan, then answer to that
address as well as the static one — producing a host that is reachable
on an address absent from every policy you write. Genuinely confusing.
Leave DHCP off.

**Cleanup.** None.

### Lab 3.3 — Create VMnet3 as the isolated OT cell

**Objective.** Build a segment with **no host adapter and no DHCP** — an
air-gapped-from-the-host cell reachable only through the Gatekeeper.

**Walkthrough**

**Step 1.** **Add Network… → VMnet3 → OK**.

**Step 2.** Configure precisely:

- Type: **Host-only**
- **Connect a host virtual adapter to this network:** **UNCHECKED** ← the
  defining choice
- **Use local DHCP service to distribute IP addresses to VMs:**
  **UNCHECKED**
- **Subnet IP:** `10.10.30.0`
- **Subnet mask:** `255.255.255.0`

**Step 3.** Click **Apply**, then **OK** to close the editor.

**Step 4.** Verify the host has **no** adapter on this network:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object IPAddress -like "10.10.30.*"

```

Expected output: **nothing at all**. Silence here is success.

Unchecking the host virtual adapter is the single most important click in
Part B. It is what makes the OT cell genuinely isolated: the Windows
host cannot put a frame on that wire. Every packet that reaches
`ct-ot01` must be routed by `ct-gw`. When you place enforcement on
`ct-gw` in Part F, there is no path around it — which is precisely the
property that lets a Gatekeeper appliance protect a device that cannot
defend itself.

**Expected result.** Three networks configured, and the host is present
on two of them only.

**Negative test.** Check **Connect a host virtual adapter** on VMnet3,
then in Part F try to prove the PLC is protected. You will find the
Windows host can still reach `10.10.30.50` directly at Layer 2,
completely bypassing every rule on `ct-gw`. This is not a lab artifact —
it is exactly the real-world failure of deploying a Gatekeeper without
removing the alternate paths around it. If a device has two routes and
you police one, you have policed nothing. Uncheck it, and remember why.

**Cleanup.** None.

### Lab 3.4 — Add a host route to the OT cell

**Objective.** Give the Windows host — playing the “IT laptop” — a Layer
3 path to the OT cell, so that Part F can prove the Gatekeeper denies
it.

**Walkthrough**

You cannot complete this exercise until `ct-gw` exists, so bookmark it
and return after Lab 4.2. It belongs here logically because it is
network plumbing.

**Step 1.** From an elevated PowerShell on the host, add a persistent
route to `10.10.30.0/24` via `ct-gw`’s Data Center address:

```powershell
New-NetRoute -DestinationPrefix "10.10.30.0/24" -NextHop "10.10.20.254" `
    -InterfaceAlias "VMware Network Adapter VMnet2" -RouteMetric 1 -PolicyStore PersistentStore

```

**Step 2.** Verify:

```powershell
Get-NetRoute -DestinationPrefix "10.10.30.0/24" |
    Format-Table -AutoSize DestinationPrefix, NextHop, InterfaceAlias, RouteMetric

```

**Step 3.** Test once `ct-gw` and `ct-ot01` are up:

```bash
ping 10.10.30.50

```

**Expected result.** The host reaches the PLC *only* by routing through
`ct-gw`. That is the point: the attack path in Part F must be one the
Gatekeeper can see and stop.

**Negative test.** Remove the route and ping again —
`PING: transmit failed. General failure` or “Destination host
unreachable”. The host has no other way in. Re-add the route before
continuing; you need the attack path to exist so that blocking it means
something.

**Cleanup.**

```powershell
Remove-NetRoute -DestinationPrefix "10.10.30.0/24" -Confirm:$false -PolicyStore PersistentStore

```

## Summary and Completion Checklist

- [ ] Lab 3.1 complete, including its negative test.
- [ ] Lab 3.2 complete, including its negative test.
- [ ] Lab 3.3 complete, including its negative test.
- [ ] Lab 3.4 complete, including its negative test.
