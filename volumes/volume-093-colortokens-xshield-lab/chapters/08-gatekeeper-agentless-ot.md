# Chapter 08: The Gatekeeper — Agentless OT Segmentation

## Learning Objectives

- Prove the Gatekeeper sits in the only path to the agentless device.
- Enforce default-deny for an OT cell, permitting one control flow.
- Argue why a heterogeneous estate needs both agent and Gatekeeper coverage.

This is where Xshield does something host-agent-only tools cannot:
protect a device that can host no agent. Your `ct-gw` VM has been the
router; now it takes on the **Gatekeeper** role — the default gateway
for the OT cell that enforces policy on traffic to and from the
agentless PLC.

The parallel to the real product is exact. The Xshield Gatekeeper is
deployed as a **VM in the data center or a hardware device on the shop
floor**, and it becomes the **default gateway for the devices it
protects**, so that **all of their communication traverses it**.
`ct-ot01`’s only route to anything is `10.10.30.254` = `ct-gw`. There is
no path around it — you guaranteed that in Lab 3.3 by giving VMnet3
no host adapter.

## Hands-On Lab

### Lab 8.1 — Confirm the Gatekeeper choke point

**Objective.** Prove, before enforcing anything, that `ct-gw` is the
sole path to the PLC — the physical precondition the Gatekeeper model
depends on.

**Walkthrough**

**Step 1.** From `ct-ot01`, confirm the gateway is `ct-gw` and there is
no other route:

```bash
ip route show

```

Expected — a single default route through the Gatekeeper and one
connected network:

```text
default via 10.10.30.254 dev ens33 proto static
10.10.30.0/24 dev ens33 proto kernel scope link src 10.10.30.50

```

**Step 2.** From `ct-gw`, confirm it sits on the OT segment:

```bash
ip -br addr show ens35

```

Expected: `ens35   UP   10.10.30.254/24`

**Step 3.** Prove the Windows host can currently reach the PLC *only* by
traversing `ct-gw`. From `ct-win01`, trace the path:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -TraceRoute

```

Expected — the route to the PLC passes through `10.10.20.254` (ct-gw) as
the first hop:

```text
TraceRoute : 10.10.20.254
             10.10.30.50
TcpTestSucceeded : True     (still true - we have not enforced yet)

```

**Step 4.** Confirm the isolation property one more time: the Windows
host has **no** direct adapter on `10.10.30.0/24`:

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object IPAddress -like "10.10.30.*"

```

Expected: **no output** — the host cannot bypass the Gatekeeper because
it has no leg in the OT cell.

**Expected result.** Verified: every packet reaching `ct-ot01` must pass
through `ct-gw`. The Gatekeeper sits in the only path.

**Negative test.** Recall Lab 3.3’s negative test — had you left a
host adapter on VMnet3, this `Get-NetIPAddress` would return
`10.10.30.1` and the host could reach the PLC at Layer 2, bypassing the
Gatekeeper entirely. The choke point is the whole game; verify it before
trusting any OT policy.

**Cleanup.** None.

### Lab 8.2 — Deploy the Gatekeeper policy (agentless OT segmentation)

**Objective.** Enforce, on `ct-gw`, a default-deny policy for the OT
cell that permits only the one legitimate control flow — HMI → PLC on
Modbus TCP 502 — and denies everything else, including all egress from
the PLC.

**The policy in plain language**

- **Allow:** `ct-win01` (10.10.20.21, the HMI) → `ct-ot01` (10.10.30.50)
  on **TCP 502** only.
- **Deny:** every other host → the PLC (IT laptops, the app tier, the
  database, the internet).
- **Deny:** the PLC → anything outbound (a compromised or malfunctioning
  PLC must not reach out).
- **Allow:** established/related return traffic, so the permitted flow
  works bidirectionally.

This is enforced on the **forward** chain of `ct-gw`, because the
Gatekeeper polices *transit* traffic, not traffic to itself.

**Track 1 — Real Xshield**

In the console you would deploy an Xshield Gatekeeper appliance, set it
as the default gateway for the OT subnet (already true here), tag
`ct-ot01` as `role:plc`/`zone:ot`, and author: **allow**
`role:hmi → role:plc` **TCP 502; default-deny all other traffic
to/from** `zone:ot`**.** Run it in Observe first to confirm the HMI flow
is the only legitimate one, then Enforce. The concepts map one-to-one
onto the Track-2 ruleset below, which is what the Gatekeeper installs on
its forwarding path.

**Track 2 — Native equivalent — Gatekeeper enforcement on ct-gw**

**Step 1.** On `ct-gw`, extend the ruleset with an OT segmentation
policy on the **forward** chain. This preserves the existing NAT and
adds default-deny for the OT cell. First snapshot-safe: you already have
`C1-base-router`, and G2 covers break-glass.

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

define OT_NET   = 10.10.30.0/24
define PLC      = 10.10.30.50
define HMI      = 10.10.20.21
define MODBUS   = 502

table inet filter {
    chain input   { type filter hook input   priority 0; policy accept; }
    chain output  { type filter hook output  priority 0; policy accept; }

    chain forward {
        type filter hook forward priority 0; policy drop;   # DEFAULT-DENY transit

        # Return traffic for already-permitted flows
        ct state established,related accept

        # --- GATEKEEPER OT POLICY ---
        # The ONE legitimate control flow: HMI -> PLC on Modbus TCP 502
        ip saddr $HMI ip daddr $PLC tcp dport $MODBUS ct state new accept

        # Non-OT east-west (e.g. app<->db within the data center) still transits.
        # (In this lab those are also enforced at the hosts; here we let the DC segment route.)
        ip saddr 10.10.20.0/24 ip daddr 10.10.20.0/24 accept

        # Data center and IT may reach the internet (NAT egress)
        ip saddr 10.10.20.0/24 oifname "ens33" accept
        ip saddr 192.168.170.0/24 oifname "ens33" accept

        # Everything else crossing the Gatekeeper is logged and dropped,
        # which specifically catches: * -> PLC (except the HMI flow) and PLC -> *
        log prefix "GATEKEEPER-DROP: " level warn
        # (policy drop handles the actual drop)
    }
}

table ip nat {
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        oifname "ens33" masquerade
    }
}
EOF

```

**Step 2.** Review before loading — this policy default-denies transit,
so read it:

```bash
sudo cat /etc/nftables.conf
sudo nft -c -f /etc/nftables.conf && echo "syntax OK"

```

**Step 3.** Load it:

```bash
sudo nft -f /etc/nftables.conf
sudo nft list chain inet filter forward

```

**Step 4 — validate the legitimate control flow survives.** From
`ct-win01` (the HMI):

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502

```

Expected: `TcpTestSucceeded : True`. And confirm real Modbus data still
flows — from `ct-win01` if you have a client, or verify from `ct-gw`’s
vantage that the SYN is accepted. From `ct-app01` you can also prove the
*negative* below.

**Step 5 — validate the attack path is now denied.** The “IT laptop”
(Windows host) tries to reach the PLC:

First, note that in this lab the Windows *host* and `ct-win01` both sit
at addresses that could reach the OT cell. The legitimate HMI is
`ct-win01` (10.10.20.21). Test an *illegitimate* source — `ct-app01`
(10.10.20.11), which has no business touching the PLC:

```bash
# From ct-app01 - an app server reaching an industrial controller: must be denied
nc -z -w3 10.10.30.50 502 && echo "REACH (BAD)" || echo "BLOCKED (correct)"

```

Expected: `BLOCKED (correct)`.

And from the Windows **host** (the IT laptop, 192.168.170.1 /
10.10.20.1), with the B4 route in place:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502

```

Expected: `TcpTestSucceeded : False` — the IT laptop is denied by the
Gatekeeper.

**Step 6 — validate PLC egress is denied.** A real risk is a compromised
PLC reaching out. From `ct-ot01`:

```bash
nc -z -w3 10.10.20.12 5432 && echo "REACH (BAD)" || echo "BLOCKED (correct)"
ping -c 2 -W 2 8.8.8.8 && echo "INTERNET (BAD)" || echo "NO INTERNET (correct)"

```

Expected: both `BLOCKED (correct)` / `NO INTERNET (correct)`. The PLC
can no longer initiate anything.

**Step 7 — watch the Gatekeeper deny log.** On `ct-gw`:

```bash
sudo journalctl -kf | grep "GATEKEEPER-DROP"

```

Re-run the denied tests from Steps 5–6 and watch each blocked flow
appear:

```text
GATEKEEPER-DROP: IN=ens34 OUT=ens35 SRC=10.10.20.11 DST=10.10.30.50 ... DPT=502
GATEKEEPER-DROP: IN=ens35 OUT=ens34 SRC=10.10.30.50 DST=10.10.20.12 ... DPT=5432

```

**Expected result.** The PLC is segmented without any agent on it: only
the HMI’s Modbus flow is permitted, every other inbound is denied, and
all PLC-initiated egress is denied — all enforced at the Gatekeeper
choke point, all logged.

**Negative test.** Recall the HMI flow’s importance: change the allow
rule’s port from 502 to 5020 (a typo), reload, and the HMI can no longer
poll the PLC — a plant outage. Segmentation that breaks the one flow the
plant needs is worse than none, because it stops production. This is why
the Gatekeeper policy, like every other, should run in Observe first.
Fix the port and reload.

**Cleanup.** To return `ct-gw` to the permissive baseline, restore
snapshot `C1-base-router` or reload the Part C ruleset.

### Lab 8.3 — Compare Gatekeeper coverage to agent coverage **Design Exercise**

**Objective.** Articulate precisely why the estate needs *both* the host
agent and the Gatekeeper — the IT/OT convergence argument that is
Xshield’s signature.

**Questions (answer before reading the model)**

1. Why can’t you simply put the host agent on `ct-ot01` and skip the

```text
Gatekeeper?

```

2. Why can’t you simply put everything behind a Gatekeeper and skip the

```text
agent?

```

3. What does “one console spanning IT and OT” buy an operator that two

```text
separate tools do not?

```

**Model answer**

1. **The PLC cannot run an agent.** No shell, no installer, no

```text
third-party software on a real controller, often a hard real-time OS
with no spare cycles and vendor warranties voided by any
modification. The host-agent mode is simply inapplicable. The
Gatekeeper enforces *in the network path* precisely because the
device itself cannot participate.

```

2. **A Gatekeeper in front of every server is operationally and

```text
architecturally wrong for agent-capable hosts.** It forces all their
traffic through an inline choke point (a scale and failure-domain
concern), it cannot see intra-host or same-subnet flows that never
cross it, and it gives coarser, network-level enforcement than an
agent that sits *on* the host and can enforce per-process at the
native firewall. Agents give granularity and see everything the host
does; Gatekeepers give reach to things that can host nothing.
Different tools for different asset classes.

```

1. **One policy model, one flow map, one Observe→Enforce lifecycle, one

```text
tag vocabulary across both IT and OT.** With two separate tools you
maintain two policy languages, reconcile two visibility pictures,
and have no unified way to express “the HMI in IT may talk to the
PLC in OT” — the one cross-domain flow that matters most. Xshield’s
coverage breadth means that cross-domain rule is a single policy in
a single console. That is the IT/OT convergence value, and it is why
the platform pairs the agent and the Gatekeeper rather than choosing
one.

```

**Expected result.** A clear, defensible statement of why heterogeneous
estates need multiple enforcement modes under one console — the core
Xshield thesis, argued from your own lab evidence.

**Negative test (conceptual).** Argue for a single enforcement mode
across the whole estate. Whichever you pick, you strand an asset class:
agent-only strands the PLC; Gatekeeper-only cripples the servers. The
estate’s heterogeneity is exactly why single-mode tools lose here.

## Summary and Completion Checklist

- [ ] Lab 8.1 complete, including its negative test.
- [ ] Lab 8.2 complete, including its negative test.
- [ ] Lab 8.3 complete, including its negative test.
