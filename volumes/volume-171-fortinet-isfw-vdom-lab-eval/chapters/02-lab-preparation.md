# Chapter 02: Lab Preparation

## Learning Objectives

- Stand up the Track 1 estate: a FortiGate-VM and four endpoint VMs across four segments.
- Stand up the Track 2 estate: a Linux host modeling four zones with nftables.
- Confirm baseline reachability before any policy exists.
- Scope cross-subnet management with a specific static route, leaving the default route free.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | FortiGate-VM evaluation (KVM/ESXi/Workstation), 4 endpoint VMs, management + one trunk data port | Fortinet support portal (VM eval) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

**The FortiGate-VM needs a valid license even to *forward* traffic.** Unlicensed, `get system status` reports `License Status: Invalid` and the VM runs in a failsafe mode: management works, but it **drops all transit** — so the lab's inter-segment flows silently go nowhere (a flow trace dies right after the route lookup, before any policy check). Activate the **free FortiGate-VM evaluation license** — done from inside the FortiGate GUI via your FortiCloud account — to enable forwarding. This lab is plaintext Layer 3/4 policy, so the evaluation's DES-only crypto limit is irrelevant here; strong crypto (IPsec/SSL-VPN, ZTNA, the FortiClient EMS Fabric join over TLS) would need a paid license, but none of that is used.

**The evaluation also caps the VM at 1 vCPU and three network interfaces.** Four physical data ports plus management is five — over the cap, and the extra interfaces vanish the moment the license applies. Rather than buy a bigger license, put the four segments on **VLAN subinterfaces of one trunk port**: a single physical data interface carrying the four segment VLANs tagged, with four `system interface` VLAN subinterfaces addressed as the segment gateways (`10.30.1.1` … `10.30.4.1`) and grouped into the same four zones. VLAN subinterfaces are logical and do not count against the physical-interface cap, so management + one trunk = two physical interfaces, comfortably under the limit — and a trunk-with-subinterfaces ISFW is closer to a real deployment than four physical ports. (On current FortiOS a VLAN subinterface requires `set vdom root` even in single-VDOM mode.) This volume *is* that trunk build — the interfaces you configure below are the four VLAN subinterfaces `v2001`–`v2004`, grouped into the zones `APP`/`DB`/`MGMT`/`OT`. For the four-physical-port version on a licensed FortiGate, see the companion **licensed volume (Volume CLXXII)**.

## Hands-On Lab

### Exercise 2.1 — Track 1: boot the evaluation FortiGate and build the trunk

**Objective.** Get a FortiGate running with one VLAN subinterface per segment on a single trunk port — the layout that fits the evaluation's 3-interface cap.

**Track 1 — Walkthrough.** Deploy the FortiGate-VM with two interfaces: `port1` for management and `port2` as a trunk carrying the four segment VLANs (2001–2004) tagged. Then create four VLAN subinterfaces on `port2`, one per segment, each addressed as that segment's gateway. On current FortiOS a VLAN subinterface requires `set vdom root` even in single-VDOM mode:

```text
FGT # config system interface
FGT (interface) # edit v2001
FGT (v2001) # set vdom root
FGT (v2001) # set interface port2
FGT (v2001) # set vlanid 2001
FGT (v2001) # set ip 10.30.1.1/24
FGT (v2001) # set allowaccess ping
FGT (v2001) # next
FGT (interface) # edit v2002
FGT (v2002) # set vdom root
FGT (v2002) # set interface port2
FGT (v2002) # set vlanid 2002
FGT (v2002) # set ip 10.30.2.1/24
FGT (v2002) # set allowaccess ping
FGT (v2002) # next
FGT (interface) # edit v2003
FGT (v2003) # set vdom root
FGT (v2003) # set interface port2
FGT (v2003) # set vlanid 2003
FGT (v2003) # set ip 10.30.3.1/24
FGT (v2003) # set allowaccess ping
FGT (v2003) # next
FGT (interface) # edit v2004
FGT (v2004) # set vdom root
FGT (v2004) # set interface port2
FGT (v2004) # set vlanid 2004
FGT (v2004) # set ip 10.30.4.1/24
FGT (v2004) # set allowaccess ping
FGT (v2004) # end
```

**Expected result.**

```text
FGT # get system interface physical | grep -A1 "v200[1-4]"
== [ v2001 ]  ip: 10.30.1.1 255.255.255.0
== [ v2002 ]  ip: 10.30.2.1 255.255.255.0
== [ v2003 ]  ip: 10.30.3.1 255.255.255.0
== [ v2004 ]  ip: 10.30.4.1 255.255.255.0
```

**Negative test.** With no firewall policy (next chapters), transit traffic between ports is dropped by the implicit deny — addressing the interfaces is necessary but not sufficient. The FortiGate forwards nothing until a policy permits it.

**Cleanup.** Leave running.

#### Real-world note — pin the management interface, and give it a return route

`port1` is the management interface; the walkthrough above leaves it as the
FortiGate deployed it. In a real build you pin management to a **static IP** so
the address never moves. There is a catch worth knowing: an interface configured
by **DHCP also learns a default route** from the DHCP server, and switching that
interface to static **silently drops the learned route**. If you manage the
FortiGate from a *different* subnet — your traffic reaches it through a gateway
rather than on the same wire — the box will now *receive* your packets but have
**no route to send the reply back**. It looks "unreachable" even though the
interface is up and `ping` is in `allowaccess`. Pin the IP **and** add the return
route:

```text
config system interface
  edit port1
    set mode static
    set ip <mgmt-ip>/24
    set allowaccess ping https ssh http
  next
end
config router static
  edit 1
    set gateway <mgmt-gateway>
    set device port1
  next
end
```

Confirm with `get router info routing-table all` — you want a default route
(`S* 0.0.0.0/0 [10/0] via <mgmt-gateway>, port1`). Same-subnet management works
without the route; **cross-subnet management needs it**. DHCP was providing this
route for free, which is why management "breaks" only *after* you pin the
interface static.

### Exercise 2.2 — Track 2: build the native zone host

**Objective.** Create four endpoint namespaces on four subnets, routed by the enforcer host.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd

mkzone() { # $1 name  $2 subnet-3rd-octet  $3 host-ip
  sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip addr add 10.30.$2.1/24 dev $1-br; sudo ip link set $1-br up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up
  sudo ip netns exec $1 ip route add default via 10.30.$2.1; }
mkzone web 1 10.30.1.10     # zone APP
mkzone db  2 10.30.2.10     # zone DB
mkzone hmi 3 10.30.3.10     # zone MGMT
mkzone plc 4 10.30.4.10     # zone OT
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

**Expected result.**

```bash
sudo ip netns exec hmi ping -c1 10.30.2.10 | grep -o "1 received"
1 received
```

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.30.9.9 | grep -o "0 received"
0 received
```

**Cleanup.** Namespaces persist for the lab.

### Exercise 2.3 — Start the workload services

**Objective.** Put a listener on db:5432 and plc:502.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

On Track 1, run PostgreSQL on the db VM and a Modbus simulator on the plc VM.

**Expected result.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Cleanup.** Leave services running.

### Exercise 2.4 — Track 1: scope management with a specific route (the surgical alternative)

**Objective.** Reach the FortiGate's management interface from a *different*
subnet **without** giving the box a default route — add a **specific** static
route back to the admin network only, leaving `0.0.0.0/0` free.

**Why this instead of a default route.** The management note in Exercise 2.1
restores cross-subnet management with a default route (`0.0.0.0/0` via the
management gateway). That is the simplest fix, but it commits the box's *only*
default path to the management interface. When the FortiGate will later carry a
real internet/WAN default out a data interface, you route management
**surgically** — a route to just the admin subnet(s) — so the default route
stays available for production traffic. Same outcome (management answers from
another subnet), tighter blast radius.

**Track 1 — Walkthrough.** With `port1` pinned static (Exercise 2.1 note), add a
route to the admin subnet via the management gateway, and do *not* set a default.
Here `10.30.161.0/24` is the admin workstation's subnet and `10.30.99.1` is the
management network's gateway — substitute your own:

```text
FGT # config router static
FGT (static) # edit 1
FGT (1) # set dst 10.30.161.0/24
FGT (1) # set gateway 10.30.99.1
FGT (1) # set device port1
FGT (1) # end
```

**Expected result.** The routing table carries the scoped route but no default:

```text
FGT # get router info routing-table all
S       10.30.161.0/24 [10/0] via 10.30.99.1, port1
C       10.30.99.0/24 is directly connected, port1
# (note: no  S*  0.0.0.0/0  line)
```

A host on `10.30.161.0/24` can now `ping` and manage the FortiGate — the reply
follows the specific route out `port1` — while `0.0.0.0/0` stays unset for a
future data-side default.

**Negative test.** Manage the box from a subnet the route does *not* name (say
`10.30.50.10`): it fails, because the FortiGate still has no route back to
`10.30.50.0/24`. That is the point of the surgical route — it grants return
reachability to **named** admin networks only, not to everything a default route
would. Add an `edit 2` route for each additional admin subnet.

**Cleanup.** Keep the route if you manage across subnets; otherwise
`config router static` → `delete 1` → `end`. The default route (Exercise 2.1) and
this scoped route are **alternatives — use one, not both**.

## Summary and Completion Checklist

- [ ] Track 1: FortiGate-VM up with four addressed data interfaces.
- [ ] Track 2: four zone namespaces routing through the enforcer host.
- [ ] Listeners up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (implicit deny still blocks transit on Track 1 until policy exists).
- [ ] Cross-subnet management works via a scoped static route (default route left free).
