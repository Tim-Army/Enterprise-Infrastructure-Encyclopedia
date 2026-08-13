# Chapter 07: Zscaler Client Connector and Traffic Forwarding

## Learning Objectives

- Explain the **Zscaler Client Connector (ZCC)** as the endpoint agent that
  forwards user traffic into ZIA and ZPA.
- Distinguish **Z-Tunnel 1.0** from **Z-Tunnel 2.0** and know when each is used.
- Configure **forwarding** and **app profiles** that decide which traffic goes
  to ZIA, to ZPA, or direct.
- Forward site traffic with **GRE/IPSec location tunnels** and the **Cloud &
  Branch Connector**.
- Diagnose forwarding failures — the agent not forwarding, wrong tunnel mode,
  or a bypass leaking traffic.

## Theory and Architecture

Everything in the previous chapters only applies to traffic that actually
reaches the Zero Trust Exchange. **Forwarding** is what puts it there. For
users, the **Zscaler Client Connector** is the agent that enrolls the device,
authenticates the user, and steers traffic to ZIA (internet/SaaS) and ZPA
(private apps). For sites, **location tunnels** (GRE/IPSec) and the **Cloud &
Branch Connector** forward everything from a location.

### Z-Tunnel 1.0 vs 2.0

- **Z-Tunnel 1.0** forwards **web ports (80/443)** to ZIA — lightweight, proxy-
  oriented.
- **Z-Tunnel 2.0** forwards **all ports and protocols** to ZIA over a DTLS/TLS
  tunnel — required for the full cloud firewall to see non-web traffic.

The choice determines what the cloud firewall (Chapter 03) can enforce: with
1.0, only web is forwarded; with 2.0, everything is.

### Forwarding and app profiles

ZCC uses **forwarding profiles** (how to forward per network — on trusted
network, VPN, or off-net) and **app profiles** (per-app/domain steering) to
decide, for each flow, whether it goes to ZIA, to ZPA, or **DIRECT**. This is
where split behavior is defined: private-app domains go to ZPA, internet goes to
ZIA, and specific trusted destinations may bypass.

### Site forwarding

A branch can forward without agents using a **GRE or IPSec tunnel** from its
edge router/firewall to the nearest ZIA service edge, or the **Cloud & Branch
Connector** appliance/VM. The site's location identity then drives location-based
policy.

## Design Considerations

- **Use Z-Tunnel 2.0 when you need full firewalling.** If policy must see
  non-web ports, 1.0 is insufficient — 2.0 forwards all protocols.
- **Design bypasses deliberately.** Every DIRECT exception in a forwarding/app
  profile is traffic Zscaler never sees; keep the list short and justified
  (e.g., the update/telemetry endpoints that must not be proxied).
- **Agent for users, tunnel for sites.** Roaming users need ZCC; fixed sites
  are efficiently covered by GRE/IPSec or the Branch Connector.

## Implementation and Automation

### Forwarding/app profile (portal shape)

```text
# ZCC Portal:
#   Forwarding Profile: On Trusted Network=Tunnel(Z-Tunnel 2.0); Off-Net=Tunnel; VPN Trusted=Disable
#   App Profile (ZPA): domains *.internal.example.com -> ZPA
#   App Profile (ZIA): everything else -> ZIA;  bypass: *.mdm-vendor.example -> DIRECT
```

### Confirming the agent is forwarding

```bash
# From the enrolled endpoint: are you egressing via Zscaler (ZIA) ?
curl -s https://ip.zscaler.com/ | sed -n '1,4p'
# Is a private (ZPA) domain resolving to a synthetic ZPA IP rather than the real one?
dig +short hr.internal.example.com    # ZPA returns a synthetic/redirected address when brokering
```

### A location tunnel (site forwarding, shape)

```text
# Edge firewall: IPSec (or GRE) tunnel to the nearest ZIA edge (vpn.<cloud>);
# ZIA Portal > Administration > Location: define the location + its public IP/VPN credentials.
```

## Validation and Troubleshooting

- **Traffic not forwarded.** ZCC is off, in a disabled state on a "trusted"
  network, or the forwarding profile disables the tunnel there — check
  `ip.zscaler.com` and the ZCC status.
- **Non-web traffic not firewalled.** You are on Z-Tunnel 1.0 — switch to 2.0 to
  forward all ports.
- **A destination leaking direct.** An app-profile bypass is sending it DIRECT —
  audit the bypass list; a stale exception is a policy hole.

## Security and Best Practices

- **Prefer Z-Tunnel 2.0** so the cloud firewall and threat engines see all
  traffic, not just web.
- **Minimize and review bypasses** — they are deliberate blind spots and drift
  into policy holes over time.
- **Enforce the agent** (anti-tamper, trusted-network detection) so users cannot
  silently disable forwarding.

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Client Connector* (forwarding/app profiles, Z-Tunnel
  1.0/2.0) and *Forwarding Traffic* (GRE/IPSec, Cloud & Branch Connector).

### Knowledge Checks

- What does Z-Tunnel 2.0 forward that 1.0 does not, and why does it matter for
  the cloud firewall?
- How do forwarding profiles and app profiles decide ZIA vs ZPA vs DIRECT?
- When would you forward a site with a GRE/IPSec tunnel instead of the agent?
- Why is every DIRECT bypass a security consideration?

## Hands-On Lab

This chapter's labs cover forwarding — verifying the agent forwards, the
tunnel-mode choice, and site tunnels. Verification runs locally on an enrolled
endpoint; portal steps reference the tenant. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.3** — an endpoint with ZCC enrolled;
`curl`, `dig`. **Cost:** none.

### Lab 7.1 — Confirm the agent forwards to ZIA and ZPA (Topic: Forwarding)

**Objective:** Verify internet and private-app steering.

```bash
echo "== ZIA egress =="
curl -s https://ip.zscaler.com/ | sed -n '1,4p'
echo "== ZPA brokering (private domain returns a synthetic address) =="
dig +short hr.internal.example.com
```

**Expected result:** internet traffic egresses via a Zscaler node and the
private domain resolves to a synthetic ZPA address (not the real server IP) —
ZCC steers internet flows to ZIA and private-app flows to ZPA, which is why the
private domain is brokered rather than routed.

**Negative test:** disable ZCC or mark the network "trusted, disable"; traffic
egresses from your local ISP and the private app is unreachable — nothing is
protected unless it is forwarded.

**Rollback:** none (read-only).

### Lab 7.2 — Choose the tunnel mode (Topic: Z-Tunnel 1.0 vs 2.0)

**Objective:** Match tunnel mode to the policy you need.

```text
# ZCC Forwarding Profile:
#   Z-Tunnel 1.0 -> forwards 80/443 only (web)
#   Z-Tunnel 2.0 -> forwards all ports/protocols (needed for full cloud firewall)
# Set 2.0 when non-web ports must be firewalled (Chapter 03).
```

**Expected result:** with Z-Tunnel 2.0 the cloud firewall sees all ports; with
1.0 only web is forwarded — the tunnel mode sets the ceiling on what ZIA can
enforce, so full firewalling requires 2.0.

**Negative test:** expect the cloud firewall to block a non-web port on Z-Tunnel
1.0; that traffic was never forwarded — 1.0 carries web only.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Forward a site with a location tunnel (Topic: Site forwarding)

**Objective:** Cover a branch without agents.

```text
# Edge firewall: IPSec tunnel to the nearest ZIA edge; ZIA Portal > Location defines the site.
# Location-based policy now applies to all traffic from that branch.
```

**Expected result:** all branch traffic forwards to ZIA over the tunnel and
location policy applies — GRE/IPSec (or the Cloud & Branch Connector) forwards a
fixed site without per-device agents, complementing ZCC for roaming users.

**Negative test:** rely on the agent for a shared kiosk/OT device that cannot
run ZCC; it is unprotected — site tunnels exist precisely for what the agent
cannot cover.

**Rollback:** tear down the lab tunnel/location.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Forwarding is what makes the whole platform apply: the Client Connector steers
each user flow to ZIA, ZPA, or DIRECT via forwarding/app profiles, Z-Tunnel 2.0
carries all ports so the cloud firewall can see everything, and GRE/IPSec or the
Branch Connector forwards fixed sites. Bypasses are deliberate blind spots to
minimize and review.

- [ ] Can verify the agent forwards to both ZIA and ZPA.
- [ ] Knows when Z-Tunnel 2.0 is required over 1.0.
- [ ] Can forward a site with a location tunnel.
- [ ] Treats every DIRECT bypass as a reviewed exception.
