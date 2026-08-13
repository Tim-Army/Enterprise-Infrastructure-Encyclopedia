# Chapter 06: Technology Specialist — DNS

## Learning Objectives

- Explain the CTS DNS specialization (exam 302) and BIG-IP DNS/GTM.
- Configure wide IPs and pools for global server load balancing.
- Apply GSLB load balancing methods and topology.
- Integrate DNS health monitoring and failover.
- Complete a walkthrough for each DNS topic.

## Theory and Architecture

The **F5 Certified Technology Specialist, DNS** (exam **302**) covers **BIG-IP DNS** (formerly
GTM, Global Traffic Manager) — intelligent, **global** load balancing at the DNS layer across
data centers and clouds. Where LTM balances within a site, BIG-IP DNS answers **DNS queries** with
the best resource for the client. The core object is the **wide IP** — a DNS name (e.g.,
`www.example.com`) mapped to **pools** of virtual servers across sites; a **GSLB load balancing
method** (round robin, ratio, global availability, topology, least connections via iQuery from
LTMs) chooses which pool/member to return. **Topology** records steer clients by geography.
**Health** comes from monitors and from **iQuery** (BIG-IP DNS learning LTM virtual-server state).
The result is **GSLB**: site failover, geographic proximity, and disaster recovery driven by DNS.

## Design Considerations

Use **wide IPs** with multiple pools for multi-site resilience. Choose a GSLB method that fits the
goal — **topology** for proximity, **global availability** for ordered failover, **ratio** for
weighted capacity. Feed BIG-IP DNS real health via **iQuery/monitors** so it never returns a dead
site. Mind DNS **TTLs** — they bound how fast failover propagates.

## Implementation and Automation

The labs configure a wide IP with pools, a GSLB method, topology, and verify resolution.

## Validation and Troubleshooting

Confirm the DNS/GSLB model:

```text
BIG-IP DNS (GTM): wide IP (DNS name) -> pools -> members (virtual servers across sites).
GSLB methods: round robin/ratio/global availability/topology/least conn (iQuery).
Health: monitors + iQuery (learn LTM VS state). TTL bounds failover speed. Exam 302.
```

Common pitfalls: returning a **dead site** because health isn't wired in; and a **long TTL** that
slows failover.

## Security and Best Practices

Wire **health** into every wide IP so DNS never sends clients to a down site. Keep **TTLs** short
enough for timely failover but not so short they overload resolvers. Secure zone transfers and DNS
(DNSSEC where required). Authorized administration throughout.

## Hands-On Lab

DNS walkthroughs. **Shared prerequisites** — a BIG-IP VE with DNS provisioned, in an authorized
lab. **Cost:** none.

### Lab 6.1 — Create a GSLB pool

**Objective:** Group virtual servers across sites.

```bash
tmsh create gtm pool a site_pool members add { site1_vs:0 site2_vs:0 } load-balancing-mode global-availability
tmsh show gtm pool a site_pool
```

**Expected result:** a **GSLB pool** with members in two sites and a load-balancing mode — the
resource set for a wide IP.

**Negative test:** point a wide IP at raw server IPs with no pool; use a **GSLB pool** so health
and method apply.

**Rollback:** `tmsh delete gtm pool a site_pool`.

### Lab 6.2 — Create a wide IP

**Objective:** Map a DNS name to the pool.

```bash
tmsh create gtm wideip a www.example.com pools add { site_pool }
tmsh show gtm wideip a www.example.com
```

**Expected result:** the **wide IP** `www.example.com` resolving via the GSLB pool — global load
balancing by DNS.

**Negative test:** publish an A record straight to one site; a **wide IP** gives multi-site
failover — use it.

**Rollback:** `tmsh delete gtm wideip a www.example.com`.

### Lab 6.3 — Topology-based steering

**Objective:** Return the nearest site by geography.

```bash
tmsh create gtm topology ldns: region /Common/north_america server: pool /Common/site1_pool
tmsh modify gtm wideip a www.example.com pool-lb-mode topology
tmsh list gtm topology
```

**Expected result:** clients in a region steered to the **nearest pool** via **topology** —
proximity-based GSLB.

**Negative test:** send all clients to one site regardless of location; **topology** returns the
closest — configure it for proximity.

**Rollback:** delete the topology record and reset the wide IP mode.

### Lab 6.4 — Verify resolution and health

**Objective:** Confirm the wide IP answers with a healthy site.

```bash
dig @<bigip-dns> www.example.com +short
tmsh show gtm pool a site_pool members
```

**Expected result:** a resolved address from a **healthy** pool member — GSLB working end to end.

**Negative test:** trust configuration without querying; **dig** the wide IP and check member
health to prove it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CTS DNS specialization (302) covers BIG-IP DNS/GTM: wide IPs mapping names to multi-site
pools, GSLB methods, topology steering, and health via monitors/iQuery. Wire health into every
wide IP, choose the method for the goal, and mind TTLs for failover speed.

- [ ] I can create a GSLB pool.
- [ ] I can map a wide IP to pools.
- [ ] I can steer clients by topology.
- [ ] I can verify resolution and member health.
- [ ] I completed Labs 6.1–6.4 including each negative test.
