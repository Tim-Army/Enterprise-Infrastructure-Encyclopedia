# Chapter 05: CCA-AppDS — NetScaler Platform, Networking, and Load Balancing

## Learning Objectives

- Cover the foundation modules shared by both CCA-AppDS exams: platform, networking, HA, load balancing, and SSL offload.
- Drill the NetScaler CLI shapes (`add/set/bind/show`) the performance-based items examine.
- Complete a walkthrough lab per module.

## The shared foundation

Both CCA-AppDS exams — *NetScaler 14.x Essentials and NetScaler Gateway* and *Deploy and Manage Citrix ADC 14.x with Traffic Management* — open with the same foundation, taught in NS-201 (formerly CNS-225). This chapter covers it once; [Chapter 06](06-cca-appds-gateway-secure-remote-access.md) and [Chapter 07](07-cca-appds-traffic-management.md) cover each exam's specific modules.

| Foundation module | Content |
|:---|:---|
| Getting started | Architecture, nsroot, NSIP/SNIP/VIP, deployment modes |
| Basic networking | Topologies (one-arm/inline), routing, VLANs, link aggregation |
| Platforms | MPX (hardware), VPX (virtual), CPX (container), BLX (bare-metal Linux), SDX (multi-tenant) |
| High availability | HA pairs, propagation/synchronization, failover |
| Load balancing | Virtual servers, services, methods, monitors, persistence |
| SSL offload | Certificate-key pairs, offload vs end-to-end, profiles |

**Free practice target:** NetScaler **CPX Express** runs as a container and accepts the same CLI — every lab below runs against it or any lab VPX.

## Hands-On Lab

Walkthroughs use the NetScaler CLI (`ssh nsroot@<NSIP>`). **Cost:** none with CPX Express.

### Lab 5.1 — The three addresses (getting started)

**Objective:** Read the address model every AppDS question assumes.

```bash
show ns ip
```

**Expected result:** The **NSIP** (management), at least one **SNIP** (subnet IP — the address NetScaler sources back-end traffic from), and any **VIPs** (where client traffic lands). One packet path: client → VIP → (SNIP) → server. Misidentifying which address does what is the classic foundation error.

**Negative test:** `add lb vserver` with a VIP that overlaps the NSIP subnet incorrectly and the config is accepted but traffic hairpins — the model, not the syntax, is what protects you.

**Cleanup:** None (read-only).

### Lab 5.2 — Platforms and modes (networking + platforms)

**Objective:** Confirm platform, modes, and features — the `show` triple.

```bash
show ns hardware
show ns mode
show ns feature
```

**Expected result:** The platform identity (CPX/VPX/MPX...), enabled modes (`L3`, `MBF`, ...), and licensed/enabled features (`LB`, `SSL`, `CS`, ...). Exam items quote these outputs; features must be **enabled** (`enable ns feature LB SSL`) before their commands work.

**Negative test:** `add lb vserver` with the LB feature disabled — the CLI warns the feature is not enabled; a favorite lab-sim gotcha.

**Cleanup:** None.

### Lab 5.3 — High availability pair (HA module)

**Objective:** Read an HA pair's state and force a failover.

```bash
show ha node
force ha failover
show ha node
```

**Expected result:** Two nodes, one `Primary` one `Secondary`, `Synchronization SUCCESS`; after the forced failover the roles swap. Configuration propagates primary→secondary; only the primary owns traffic.

**Negative test:** Configure on the secondary (it refuses or warns) — changes belong on the primary; propagation is one-way.

**Cleanup:** Fail back if desired.

### Lab 5.4 — Load balancing end to end (LB module)

**Objective:** Build the canonical service → vserver → bind chain.

```bash
add service web1 10.150.9.11 HTTP 80
add service web2 10.150.9.12 HTTP 80
add lb vserver lb_web HTTP 10.150.9.100 80 -lbMethod LEASTCONNECTION -persistenceType COOKIEINSERT
bind lb vserver lb_web web1
bind lb vserver lb_web web2
show lb vserver lb_web
```

**Expected result:** `lb_web` **UP** with two bound services, least-connection method, cookie persistence — the exam's core object chain, and the shape the CLI simulations present.

**Negative test:** Stop one back-end; its default `tcp-default` monitor marks the service **DOWN** and traffic shifts to the survivor — monitors, not hope, decide membership.

**Cleanup:** `rm lb vserver lb_web; rm service web1; rm service web2`.

### Lab 5.5 — Monitors and persistence (LB module)

**Objective:** Attach an HTTP monitor and verify persistence behavior.

```bash
add lb monitor http_ok HTTP -respCode 200 -httpRequest "GET /health"
bind service web1 -monitorName http_ok
show service web1
```

**Expected result:** `web1` probed by `http_ok`; state follows the health endpoint. With `COOKIEINSERT` persistence, repeated client requests land on one back-end — method chooses the first hit, persistence pins the rest.

**Negative test:** Point the monitor at a path returning 404; the service goes DOWN though TCP/80 is open — application-level health beats port-level.

**Cleanup:** Unbind the monitor.

### Lab 5.6 — SSL offload (SSL module)

**Objective:** Terminate TLS on NetScaler with a cert-key pair.

```bash
add ssl certKey lab_cert -cert lab.crt -key lab.key
add lb vserver lb_web_ssl SSL 10.150.9.101 443
bind ssl vserver lb_web_ssl -certkeyName lab_cert
bind lb vserver lb_web_ssl web1
show ssl vserver lb_web_ssl
```

**Expected result:** An SSL vserver UP with the cert-key bound: TLS terminates at the VIP, back-end runs HTTP (offload) — or SSL service for end-to-end. The offload/end-to-end distinction and cert-key binding order are exam staples.

**Negative test:** Skip the certkey bind; the vserver stays DOWN — an SSL vserver without a certificate can never come up.

**Cleanup:** `rm lb vserver lb_web_ssl; rm ssl certKey lab_cert`.

## Summary and Completion Checklist

- [ ] NSIP/SNIP/VIP model, platforms, and modes drilled.
- [ ] HA pair behavior and one-way propagation exercised.
- [ ] LB chain, monitors, persistence, and SSL offload built by hand at the CLI.
