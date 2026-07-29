# Chapter 05: CCSE — Advanced Gateway

## Learning Objectives

- Perform gateway and management upgrades.
- Build a ClusterXL high-availability cluster.
- Configure a site-to-site VPN.
- Understand SecureXL and CoreXL acceleration.
- Complete a walkthrough for each advanced topic.

## Theory and Architecture

The **CCSE** builds on CCSA with advanced deployment and performance. **Upgrades** move management
and gateways to a new release via **CPUSE** (the Gaia Deployment Agent) or migrate/import — always
management first, then gateways. **ClusterXL** provides **high availability** (and load sharing):
two or more gateways share a virtual IP, synchronize connection state over a dedicated sync network,
and fail over transparently — **High Availability (New Mode)** is the common design. **Site-to-site
VPN** connects gateways with **IKE/IPsec**, defined by a VPN community (star or meshed) with
encryption domains. Performance comes from **SecureXL** (fast-path packet acceleration, offloading
established connections) and **CoreXL** (spreads inspection across CPU cores via multiple firewall
instances). Together these deliver resilient, high-throughput, encrypted gateways — the CCSE core.

## Design Considerations

Upgrade **management first**, then gateways, with backups and a rollback plan. Use **ClusterXL** for
HA with a dedicated **sync** network. Design VPN communities (star for hub-and-spoke, meshed for
any-to-any) with clear **encryption domains**. Keep **SecureXL/CoreXL** enabled and size cores to
throughput. Test failover.

## Implementation and Automation

The labs plan an upgrade, verify a cluster, build a VPN, and check acceleration.

## Validation and Troubleshooting

Confirm advanced concepts:

```text
Upgrade: CPUSE/migrate, management first then gateways (backup + rollback).
ClusterXL: virtual IP + state sync -> transparent failover (HA New Mode / Load Sharing).
VPN: IKE/IPsec communities (star/meshed) + encryption domains. Acceleration: SecureXL (fast path) + CoreXL (multi-core).
```

Common pitfalls: upgrading **gateways before management** (unsupported); and no **sync network**
(state not synced, failover drops connections).

## Security and Best Practices

Upgrade in order with backups; build **ClusterXL** HA with a dedicated sync; design clean VPN
communities and encryption domains; keep **SecureXL/CoreXL** on and sized. Test failover before
production. Defensive administration.

## Hands-On Lab

Advanced walkthroughs. **Shared prerequisites** — Check Point management + two gateways (for
cluster/VPN labs) in a lab. **Cost:** none.

### Lab 5.1 — Verify a ClusterXL cluster

**Objective:** Confirm HA state.

```bash
cphaprob state       # cluster member states: ACTIVE / STANDBY
cphaprob -a if       # monitored interfaces + sync
cphaprob list        2>/dev/null | head || echo "cphaprob = ClusterXL health: one ACTIVE, others STANDBY, sync up"
```

**Expected result:** one **ACTIVE** and one **STANDBY** member with sync up — a healthy ClusterXL
cluster.

**Negative test:** build a cluster with **no dedicated sync** interface; failover loses connections
— provide a sync network.

**Cleanup:** none (read-only).

### Lab 5.2 — Test failover

**Objective:** Validate transparent failover.

```bash
# On the ACTIVE member (lab): trigger failover
clusterXL_admin down    # gracefully make this member fail over
cphaprob state          # the STANDBY becomes ACTIVE; connections persist (state was synced)
clusterXL_admin up      # restore
```

**Expected result:** the standby becomes **ACTIVE** and synced connections **persist** — transparent
failover.

**Negative test:** fail over with sync broken; established connections drop — sync must be healthy.

**Cleanup:** `clusterXL_admin up` to restore both members.

### Lab 5.3 — Build a site-to-site VPN

**Objective:** Encrypt gateway-to-gateway traffic.

```text
# SmartConsole -> VPN Communities -> new Star/Meshed community: add both gateways, set encryption
#   domains, IKE (v2) + IPsec settings; add an access rule allowing the VPN traffic; install policy.
"site-to-site VPN: community + encryption domains + IKEv2/IPsec -> encrypted tunnel between sites"
```

**Expected result:** an **IPsec tunnel** between gateways carrying the defined encryption domains —
a working site-to-site VPN.

**Negative test:** mismatch the **encryption domains**; interesting traffic isn't encrypted/routed —
align the domains on both sides.

**Cleanup:** disable the lab community.

### Lab 5.4 — Check SecureXL and CoreXL

**Objective:** Verify acceleration.

```bash
fwaccel stat         # SecureXL status (enabled, accelerated/… tables)
fw ctl affinity -l   # CoreXL instance/interface CPU affinity
fwaccel stats -s     2>/dev/null | head || echo "SecureXL = fast path; CoreXL = multiple fw instances across cores"
```

**Expected result:** **SecureXL enabled** and **CoreXL** instances across cores — accelerated
inspection.

**Negative test:** disable SecureXL under heavy load; throughput drops — keep acceleration on unless
troubleshooting requires otherwise.

**Cleanup:** none (read-only).

### Lab 5.5 — Plan a management-first upgrade

**Objective:** Sequence an upgrade safely.

```bash
# Gaia CPUSE (Deployment Agent):
clish -c "show installer packages"    # available packages/hotfixes
echo "Order: backup -> upgrade Management (CPUSE/migrate) -> upgrade gateways -> verify. Never gateways first."
```

**Expected result:** an upgrade plan — **management first, then gateways**, with backups.

**Negative test:** upgrade a gateway to a newer release than its management; unsupported — management
leads.

**Cleanup:** none (planning).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CCSE adds upgrades (management first), ClusterXL HA with state sync and transparent failover,
site-to-site IKE/IPsec VPN communities, and SecureXL/CoreXL acceleration — resilient, high-throughput
gateways.

- [ ] I can verify ClusterXL state and test failover.
- [ ] I can build a site-to-site VPN.
- [ ] I can check SecureXL and CoreXL.
- [ ] I can plan a management-first upgrade.
- [ ] I completed Labs 5.1–5.5 including each negative test.
