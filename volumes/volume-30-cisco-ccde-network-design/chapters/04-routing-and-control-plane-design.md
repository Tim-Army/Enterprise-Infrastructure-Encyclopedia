# Chapter 04: Routing and Control Plane Design

## Learning Objectives

- Select routing protocols by design requirement, not preference
- Design IGP architecture — hierarchy, areas/levels, summarization —
  for scale and convergence
- Design BGP for the enterprise: where it belongs, policy, and
  scaling
- Design convergence: detection, propagation, and precomputed
  protection, sized to requirements
- Reason about redistribution, route policy, and the control-plane
  risks each introduces

## Theory and Architecture

### Protocol selection is a design decision

CCDE Domains 2 (25%) and 3 (30%) overlap heavily in the control plane,
and the exam's favorite question is *which routing protocol, and why*.
There is rarely one right answer — there is the answer that best fits
the requirements:

- **OSPF** — well-understood, fast, structured areas; strong where the
  team knows it and the topology suits area hierarchy. Its area design
  is rigid (everything through area 0).
- **IS-IS** — address-family agnostic, TLV-extensible (segment routing),
  flexible hierarchy; favored where scale, SR, or multi-address-family
  futures matter (the reasoning of Volume XXIX, Chapter 02).
- **EIGRP** — simple, fast, flexible summarization anywhere; Cisco-
  centric, less common in greenfield expert designs but present in
  installed bases.
- **BGP** — the scaling and policy protocol: internet edge, DMVPN/
  SD-WAN overlays, data-center fabrics (Volume XXVII), and anywhere
  policy or massive scale is needed.

The CCDE weighs team familiarity, existing estate, scale horizon,
multi-vendor needs, and future direction (SR) — and defends the choice.

### IGP architecture

Designing the IGP is designing for **scale and convergence**:

- **Hierarchy** — OSPF areas or IS-IS levels bound LSA/LSP flooding
  and SPF scope; the design decides the boundaries, and they should
  align with summarization points and failure domains (Chapter 03).
- **Summarization** — at hierarchy boundaries, summarization shrinks
  tables and, crucially, *hides* churn — a flapping link inside a
  summarized area does not trigger SPF network-wide. This is a primary
  convergence and stability lever.
- **Stub techniques** — stub/totally-stubby areas and their IS-IS
  analogs reduce edge routers' burden; a design choice trading
  flexibility for simplicity and scale.

### BGP in the enterprise

BGP appears wherever policy or scale demands it: internet multihoming
(path selection, provider-independent addressing, traffic engineering
with communities and local-preference), SD-WAN and DMVPN overlays,
and as the control plane of modern fabrics. The design questions are
where the iBGP/eBGP boundaries sit, how policy expresses the business's
routing relationships, and how to scale (route reflection — Volume
XXIX, Chapter 03 — applies at enterprise scale too).

### Convergence design

Meeting an availability/convergence requirement is a stack of design
choices:

- **Detection** — fast: BFD (sub-second, protocol-independent) versus
  slower protocol hellos; the faster the detection the tighter the
  restoration, at some CPU cost and false-positive risk.
- **Propagation** — how fast the failure information spreads: SPF/
  flooding tuning, but bounded by summarization (which also *hides*
  events).
- **Protection** — precomputed backups (LFA/rLFA/TI-LFA, Volume XXIX
  Chapter 05) so the data plane switches before the control plane
  reconverges, delivering sub-50-ms restoration where required.

The design sizes these to the requirement: five-nines and real-time
apps justify BFD + TI-LFA everywhere; a best-effort branch does not.

### Redistribution and policy risk

Wherever two routing domains meet (merger, multi-protocol estate,
PE-CE), **redistribution** is a design hazard: routing loops,
suboptimal paths, and feedback are all born here. The CCDE designs
redistribution defensively — tagging and filtering to prevent
re-injection, controlling metrics, and minimizing the number of
redistribution boundaries. Route policy (community schemes,
local-preference, tags) is the tool; the design keeps it comprehensible.

## Design Considerations

- **Choose the IGP for the estate and the future, then commit.**
  Running two IGPs long-term (outside migration) is a redistribution
  liability; pick one for the core and mean it.
- **Summarize to hide churn, not just shrink tables.** Place
  summarization at failure-domain boundaries so instability is
  contained — this is often the single biggest stability lever.
- **Size convergence to the requirement.** BFD + TI-LFA where
  sub-50-ms matters; do not pay their cost where best-effort suffices.
- **Minimize and defend redistribution points.** Every mutual
  redistribution boundary is a potential loop; tag, filter, and count
  them. Two-way redistribution at two points without loop prevention
  is the classic expert-exam trap.
- **BGP where policy or scale lives, not everywhere.** Do not reach
  for BGP internally when a well-summarized IGP meets the need.

## Applied Design Reasoning

Brief fragment — *"A logistics firm is merging its OSPF network with
an acquired EIGRP network; both use 10.0.0.0/8 internally with overlap;
the merged network must converge sub-second for a real-time tracking
app; the team knows OSPF well, EIGRP barely."* — reasoned:

```text
Requirements: merge two IGP domains; sub-second convergence for the
  tracking app; operable by an OSPF-fluent team.
Constraints: overlapping 10/8 space; EIGRP skills weak; brownfield
  (cannot renumber overnight).
Design decisions:
  - Target a single OSPF core (team fluency + convergence design
    maturity), migrating the EIGRP estate into it over a phased plan
    rather than running both indefinitely.
  - During migration, redistribute at a MINIMAL, controlled set of
    boundaries with route tagging + filtering to prevent loops
    (defensive redistribution), because two domains must coexist
    temporarily.
  - Resolve overlap with NAT at the merger boundary short-term and a
    renumbering plan for one side long-term, because sub-second intra-
    domain convergence requires clean addressing eventually.
  - BFD + LFA/TI-LFA on the core paths carrying the tracking app,
    sized to the sub-second requirement (not network-wide waste).
  Trade-off: temporary NAT + redistribution complexity during
  migration -> accepted, because the end-state (single OSPF domain,
  clean addressing) meets convergence and operability, and the mess is
  bounded and time-limited.
```

## Verification and Design Review

Control-plane design is verified by checking protocol choice against
requirements and team; IGP hierarchy/summarization aligned with
failure domains; convergence mechanisms sized to the availability
requirement (and not over-applied); redistribution boundaries
minimized and loop-protected; and BGP used where policy/scale
genuinely require it. The specific expert-review question: **trace
every redistribution boundary and prove it cannot loop** — this is
where otherwise-good designs fail.

## References and Knowledge Checks

- CCDE v3.1 Network Design (30%) and Control/Data/Management Plane
  design (25%)
- Volume III (enterprise routing), Volume XXIX (IS-IS, BGP, SR, TI-LFA
  at scale)
- IETF routing RFCs as design references

Knowledge checks:

1. Give two requirements that would steer a core IGP choice to IS-IS
   over OSPF, and one that would keep it OSPF.
2. Beyond shrinking tables, what stability benefit does summarization
   provide, and where must it be placed to deliver it?
3. Why is two-point mutual redistribution dangerous, and what two
   techniques make it safe?
4. When is BFD + TI-LFA justified, and when is it over-design?

## Design Exercises

These Design Exercises cover the CCDE **routing and control-plane** design topics — IGP structure,
BGP scaling, route control, and convergence. Work each to a written design, stating every choice as
a *decision → driver → cost* sentence. They share the chapter's **`**Lab verified by:** *pending*`**
sign-off.

### Design Exercise 4.1 — IGP selection and hierarchy (Topic: IGP design)

> **Scenario.** A national network of 300 routers across a core and 40 regional POPs needs fast
> convergence and must scale for another decade. The team knows both OSPF and IS-IS.

Design the IGP: **OSPF vs IS-IS** with a driver (scalability, simplicity, multi-topology, operator
familiarity); the area/level hierarchy and where boundaries fall; the summarization strategy at
those boundaries; and how the hierarchy bounds the size of any single flooding/SPF domain. State
what the chosen structure costs in flexibility.

**Expected result:** an IGP hierarchy whose area/level boundaries align with the topology and
addressing so each domain stays small and summarization contains LSA/SPF scope — the IGP choice
matters less than the *hierarchy*, which is what delivers scale and convergence.

**Common mistake:** a single flat area/level "for simplicity"; it does not scale — flooding and SPF
cost grow with the domain, so the design must partition into summarized hierarchies.

### Design Exercise 4.2 — BGP scaling and policy (Topic: BGP design)

> **Scenario.** The same network runs iBGP for internal reachability and eBGP to two upstreams.
> iBGP full mesh is no longer viable at 300 routers, and policy must prefer one upstream for
> outbound and control inbound traffic engineering.

Design the BGP: **route reflectors vs confederations** for iBGP scaling (with the trade-offs:
redundancy, path visibility, migration, complexity); RR placement/redundancy and cluster design;
and the inbound/outbound policy (local-pref, AS-path prepend, MED, communities) that meets the
traffic-engineering requirement.

**Expected result:** an iBGP scaling design (typically redundant route reflectors) with a policy
framework using communities for maintainable traffic engineering — BGP design is about scaling the
control plane and expressing policy cleanly, and RR redundancy/placement determines path diversity.

**Common mistake:** scaling iBGP with a partial mesh of static peerings, or encoding policy as
per-neighbor one-offs; both become unmaintainable — RR/confederation plus community-based policy is
the scalable, reviewable approach.

### Design Exercise 4.3 — Redistribution and route control (Topic: Route control)

> **Scenario.** A merger connects two routing domains (one OSPF, one EIGRP/IS-IS) at two points for
> redundancy, and routes must flow both ways.

Design the redistribution: the two mutual-redistribution points and the **loop/suboptimal-routing
risk** they create; the controls (route tags to prevent re-injection, administrative distance,
filtering, summarization) that prevent loops; and how you keep the domains loosely coupled rather
than fully merged. State the operational cost of the boundary.

**Expected result:** a controlled two-point redistribution using route tags and filtering to prevent
loops and metric administrative-distance issues, with summarization to limit leakage — multipoint
mutual redistribution is a classic loop source, and the tag/filter controls are the design that
tames it.

**Common mistake:** redistributing mutually at two points with no tags or filtering; routes
re-inject across the boundary and form loops or black holes — the loop-prevention controls are the
whole point of the design.

### Design Exercise 4.4 — Convergence and fast reroute (Topic: Convergence design)

> **Scenario.** A financial network requires sub-50 ms recovery for a subset of critical flows and
> "good enough" recovery elsewhere, without destabilizing the control plane.

Design convergence: where **fast mechanisms** (BFD, LFA/remote-LFA or TI-LFA with SR, tuned timers)
are applied versus default timers; the trade-off between aggressive timers and control-plane
stability/false failovers; and how topology (link/node redundancy, failure-domain size) sets the
achievable floor. Scope the fast path to the critical flows.

**Expected result:** a design applying fast-reroute (e.g. TI-LFA/BFD) selectively to the critical
domain while keeping conservative timers elsewhere, recognizing that topology and failure-domain
size, not just timers, bound convergence — sub-50 ms is a design outcome, not a knob.

**Common mistake:** globally cranking timers to their minimum for speed; you invite flapping and
control-plane instability that causes *more* outage — fast reroute is engineered where needed, with
stability preserved elsewhere.

## Lab Verification

The exercise is verified when protocol choice fits requirements and
team, summarization aligns with failure domains, convergence is sized
(not over-applied) to the requirement, and every redistribution
boundary is shown to be loop-safe. Until a reviewer confirms that, the
exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Routing and control-plane design is protocol selection by requirement,
IGP hierarchy and summarization that bound failures and hide churn,
convergence mechanisms sized to availability needs, and redistribution
handled defensively so domains meet without looping. BGP enters where
policy and scale live. This spans the CCDE's two heaviest domains and
is where expert designs are made or undone.

- [ ] I choose routing protocols from requirements, team, and future
- [ ] My summarization is placed to hide churn at failure boundaries
- [ ] My convergence design is sized to the requirement, not maximal
- [ ] Every redistribution boundary in my design is proven loop-safe
