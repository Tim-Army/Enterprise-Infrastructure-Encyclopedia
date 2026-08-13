# Chapter 08: Service Routing Architect (SRA)

## Learning Objectives

- Explain the SRA credential (exam 4A0-112) and its design focus.
- Design a scalable IGP and BGP architecture for a service provider.
- Design MPLS/SR transport and a service architecture.
- Justify redundancy, scale, and convergence trade-offs.
- Complete a design exercise for each SRA topic.

## Theory and Architecture

The **Service Routing Architect (SRA)** — exam **4A0-112**, requiring NRS II — is Nokia's expert
**design** credential. Where NRS II proves you can configure and troubleshoot, SRA proves you can
**architect** an end-to-end service-provider network from requirements: an **IGP** design (area/
level structure, summarization, router-ID/loopback plan) that scales; a **BGP** design (route
reflectors, confederations, address families for services) that avoids full-mesh sprawl; an
**MPLS/SR transport** design (LDP vs RSVP-TE vs Segment Routing, fast reroute, TE) that meets
availability and bandwidth goals; and a **service** architecture (VPRN/VPLS/EVPN placement,
redundancy, QoS) that delivers customer SLAs. SRA is about **trade-offs** — scale vs simplicity,
redundancy vs cost, convergence vs stability — each justified against requirements and validated
by a failure analysis.

## Design Considerations

Design **requirement-first**. Scale the IGP with **levels/areas and summarization**, the BGP with
**route reflectors**, and the transport with **Segment Routing** to remove per-LSP state. Build in
**redundancy** (dual-homing, FRR, redundant RRs) with no single point of failure, and target
**convergence** goals. Document every trade-off.

## Implementation and Automation

The design exercises architect the IGP/BGP, the transport, and the service layer, with a failure
analysis.

## Validation and Troubleshooting

Confirm the design method:

```text
Requirements -> IGP design (levels/areas, summarization, loopbacks) -> BGP design (RRs, AFs)
-> transport (LDP/RSVP/SR, FRR, TE) -> services (VPRN/VPLS/EVPN, QoS, redundancy) -> failure analysis.
SRA: exam 4A0-112, requires NRS II. Design + trade-offs, not just config.
```

Common pitfalls: an IBGP **full mesh** that won't scale (use route reflectors); and a design with
**no failure analysis**.

## Security and Best Practices

Bake in **redundancy** and **no single point of failure**, secure the control plane, and prefer
**SR** for a stateless, scalable core. Keep the design **documented and traceable** to requirements
so it can be reviewed and defended.

## Hands-On Lab

Design exercises. **Shared prerequisites for Labs 8.1–8.4** — a shell with `python3` and a
requirements sheet. **Cost:** none.

### Lab 8.1 — IGP architecture

**Objective:** Choose an IGP structure for scale.

```python
python3 - <<'PY'
req={"routers":400,"core":"large SP","sr_ready":True}
design={"igp":"IS-IS (L2 backbone + L1 areas)","reason":"scales, SR-friendly",
        "loopbacks":"/32 system per node","summarize":"at L1/L2 boundaries"}
for k,v in design.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** an **IS-IS** design with levels and summarization justified by scale and SR
readiness — a scalable IGP.

**Negative test:** put 400 routers in one flat area; **structure and summarize** — flat doesn't
scale.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — BGP architecture

**Objective:** Scale IBGP for services.

```python
python3 - <<'PY'
n=400
full_mesh_sessions=n*(n-1)//2
design={"ibgp":"route reflectors (redundant pair per region)","afs":"VPN-IPv4 + EVPN",
        "full_mesh_would_need":f"{full_mesh_sessions} sessions (unscalable)"}
for k,v in design.items(): print(f"{k}: {v}")
PY
```

**Expected result:** **route reflectors** instead of ~79,800 full-mesh sessions — a scalable BGP
design.

**Negative test:** design IBGP as a full mesh at scale; use **route reflectors** — the mesh
explodes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Transport and service architecture

**Objective:** Choose transport and service placement.

```python
python3 - <<'PY'
design={"transport":"Segment Routing (SR-MPLS) + TI-LFA fast reroute",
        "reason":"stateless core, sub-50ms protection",
        "services":"VPRN (L3VPN) + EVPN (L2) at the PEs, QoS per SLA"}
for k,v in design.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** **Segment Routing** transport with fast reroute and EVPN/VPRN services — a
modern, resilient architecture.

**Negative test:** default to RSVP full-mesh LSPs for everything; **SR** removes state — prefer it
for scale.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Failure analysis

**Objective:** Prove resilience.

```python
python3 - <<'PY'
analysis={"link failure":"TI-LFA fast reroute (<50ms)","node failure":"IGP reconverge + backup path",
          "RR failure":"redundant RR pair keeps IBGP","PE failure":"dual-homed CE / EVPN active-active"}
spof=[k for k,v in analysis.items() if not v]
for scenario,mitigation in analysis.items(): print(f"{scenario:14}: {mitigation}")
print("unmitigated SPOF:", spof or "none")
PY
```

**Expected result:** each failure mode **mitigated** with no single point of failure — a defended
design.

**Negative test:** present a design with no **failure analysis**; the SRA expects one — analyze
every failure mode.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SRA (4A0-112, requires NRS II) tests end-to-end service-provider design: a scalable IGP, a
route-reflected BGP, an SR-based resilient transport, and an EVPN/VPRN service architecture — every
trade-off justified and backed by a failure analysis. Design requirement-first, scale
deliberately, and remove single points of failure.

- [ ] I can design a scalable IGP architecture.
- [ ] I can scale IBGP with route reflectors.
- [ ] I can choose SR transport and service placement.
- [ ] I can produce a failure analysis.
- [ ] I completed Labs 8.1–8.4 including each negative test.
