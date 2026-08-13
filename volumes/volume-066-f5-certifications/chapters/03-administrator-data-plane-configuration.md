# Chapter 03: Administrator — Data Plane Configuration

## Learning Objectives

- Configure the core BIG-IP data-plane objects (F5CAB3).
- Build a virtual server, pool, and pool members.
- Attach profiles and monitors to control traffic.
- Apply SNAT for return-path symmetry.
- Complete a walkthrough for each data-plane configuration topic.

## Theory and Architecture

The **F5CAB3** exam (Data Plane Configuration) covers how traffic is actually served. The central
object is the **virtual server** — a listener (IP:port) that receives client traffic and applies
policy. Behind it, a **pool** groups the backend **pool members** (servers), and a **load
balancing method** (round robin, least connections, ratio, etc.) distributes across them.
**Monitors** (health checks — ICMP, TCP, HTTP, HTTPS) mark members up or down so traffic only
goes to healthy servers. **Profiles** attached to the virtual server control protocol behavior
(TCP, HTTP, Client/Server SSL for offload, persistence). **SNAT** (Secure/Source NAT) replaces the
client source IP with a BIG-IP self-IP so servers return traffic through the BIG-IP, preserving
the full-proxy path. Together these objects turn a listener into a load-balanced, health-checked,
policy-controlled service.

## Design Considerations

Choose a **load balancing method** that fits the workload (least connections for uneven requests,
ratio for heterogeneous servers). Always attach a **monitor** so dead members are removed. Use
**SNAT** when servers lack a route back through the BIG-IP. Attach only the **profiles** you need;
each adds processing.

## Implementation and Automation

The labs build a pool with a monitor, a virtual server with profiles, SNAT, and verify via tmsh.

## Validation and Troubleshooting

Confirm the data-plane object model:

```text
Virtual server (IP:port listener) -> pool -> pool members (servers).
LB method: round robin | least connections | ratio | ...
Monitor: health check (ICMP/TCP/HTTP/HTTPS) marks members up/down.
Profiles: TCP/HTTP/SSL(offload)/persistence. SNAT: rewrite source for return symmetry.
```

Common pitfalls: a pool with **no monitor** (traffic hits dead servers); and asymmetric routing
with **no SNAT** (servers reply around the BIG-IP, breaking the proxy).

## Security and Best Practices

Health-check every pool, terminate/inspect TLS with **SSL profiles** where policy requires, and
use **SNAT** to keep the traffic path symmetric. Keep virtual servers least-exposed (specific
IP/port, only needed profiles). Defensive administration throughout.

## Hands-On Lab

Data-plane walkthroughs. **Shared prerequisites** — a BIG-IP VE with LTM provisioned, in an
authorized lab. **Cost:** none.

### Lab 3.1 — Create a pool with a health monitor

**Objective:** Group backend servers with a health check.

```bash
tmsh create ltm pool web_pool monitor http members add { 10.10.30.11:80 10.10.30.12:80 }
tmsh show ltm pool web_pool
```

**Expected result:** a **pool** with two members and an **HTTP monitor** — health-checked backend.

**Negative test:** create the pool with `monitor none`; traffic will hit **dead** members —
always attach a monitor.

**Rollback:** `tmsh delete ltm pool web_pool`.

### Lab 3.2 — Create a virtual server

**Objective:** Publish a listener bound to the pool.

```bash
tmsh create ltm virtual web_vs destination 10.10.20.100:80 \
    ip-protocol tcp profiles add { http tcp } pool web_pool source-address-translation { type automap }
tmsh show ltm virtual web_vs
```

**Expected result:** a **virtual server** on 10.10.20.100:80 load-balancing to `web_pool` with
HTTP/TCP profiles and **SNAT automap** — a live service.

**Negative test:** omit the pool; a virtual server with **no pool** has nowhere to send traffic —
bind the pool.

**Rollback:** `tmsh delete ltm virtual web_vs`.

### Lab 3.3 — SSL offload profile

**Objective:** Terminate TLS at the BIG-IP.

```bash
tmsh create ltm profile client-ssl web_clientssl cert default.crt key default.key
tmsh modify ltm virtual web_vs profiles add { web_clientssl }
tmsh list ltm virtual web_vs profiles
```

**Expected result:** a **Client SSL** profile on the virtual server — TLS terminated (offloaded)
at the BIG-IP so it can inspect and steer.

**Negative test:** pass TLS straight through when the design needs inspection; **offload** with a
Client SSL profile so the proxy can act on content.

**Rollback:** `tmsh modify ltm virtual web_vs profiles delete { web_clientssl }; tmsh delete ltm profile client-ssl web_clientssl`.

### Lab 3.4 — Verify load balancing state

**Objective:** Confirm distribution and member health.

```bash
tmsh show ltm pool web_pool members
# Look for member availability (up/down) and current connections per member.
```

**Expected result:** each member's **health and connection counts** — evidence the pool is
distributing to healthy servers.

**Negative test:** assume traffic is balanced without checking; **verify** member state and
counts — monitors and stats prove it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The F5CAB3 exam covers the data-plane objects: virtual servers, pools and members, load balancing
methods, health monitors, profiles (including SSL offload), and SNAT. Health-check every pool,
offload/inspect TLS where required, and keep the traffic path symmetric with SNAT.

- [ ] I can create a pool with a health monitor.
- [ ] I can publish a virtual server bound to a pool.
- [ ] I can offload TLS with a Client SSL profile.
- [ ] I can verify load-balancing and member health.
- [ ] I completed Labs 3.1–3.4 including each negative test.
