# Chapter 02: Business Strategy Design

## Learning Objectives

- Align network design to business strategy, drivers, and outcomes
- Gather and classify requirements, and translate business language
  into technical constraints
- Apply project delivery methodologies — Waterfall and Agile — to
  network design engagements
- Design for business continuity, operational sustainability, and
  acceptable risk
- Reason about cost: capex/opex trade-offs, total cost of ownership,
  and the cost of change

## Theory and Architecture

### Why business strategy leads

CCDE Domain 1 (15%) comes first for a reason: a network exists to
serve a business, and a technically excellent design that misses the
business goal is a failed design. The domain tests whether you can
start from *why the business is spending money on this network* and
let that drive the architecture — not the reverse. Business drivers
recur: growth (mergers, new sites, new markets), cost reduction,
risk/compliance, agility (faster time-to-service), resilience
(uptime obligations), and increasingly **AI adoption** (v3.1's
addition — the business wants AI capabilities, which reshape
infrastructure demand).

### Requirements engineering

The designer's first job is to elicit and classify requirements:

- **Functional** — what the network must do (connect these sites,
  carry this application, support this many users).
- **Non-functional** — how well: availability targets (the difference
  between 99.9% and 99.999% is millions of dollars and a different
  architecture), latency and throughput, scalability horizon,
  security and compliance posture.
- **Business constraints** — budget and its shape (capex vs opex),
  timelines tied to business events, existing contracts and
  installed base, team size and skills, regulatory and geographic
  limits.

Translating business language into technical requirements is the
craft: "we can't afford downtime during the holiday season" becomes a
change-freeze window and a resilience target; "we're expanding into
Europe" becomes data-residency (GDPR) and latency requirements.

### Delivery methodologies

The CCDE v3.x explicitly tests design in the context of project
management methodologies, because *how* a design is delivered shapes
*what* design is appropriate:

- **Waterfall** — sequential, fully specified up front; suits stable,
  well-understood requirements and heavy compliance environments, and
  produces a complete design before implementation. Its risk is late
  discovery of wrong assumptions.
- **Agile/iterative** — incremental delivery, design evolving with
  feedback; suits uncertain or fast-changing requirements (a cloud
  migration whose end-state is not fully known). Its design
  implication: favor modular, loosely coupled architectures that can
  change one part without redesigning the whole.

The methodology is itself a design input: an Agile program needs an
architecture tolerant of incremental change; a Waterfall program can
commit to a more monolithic optimum.

### Continuity, sustainability, and risk

- **Business continuity** — the design's answer to disaster: RPO
  (how much data loss is tolerable) and RTO (how fast to recover)
  are business decisions that dictate redundancy, site diversity, and
  failover architecture. Over-designing continuity wastes money;
  under-designing it risks the business.
- **Operational sustainability** — can the organization run this for
  years? Skills, tooling, documentation, and complexity all factor.
  The most common expert-level design error is an architecture the
  customer's team cannot operate.
- **Risk** — every design carries risk (of failure, of change, of
  obsolescence); the CCDE weighs and communicates it rather than
  pretending it away.

## Design Considerations

- **Availability targets drive architecture, not the reverse.** Decide
  the required nines first; they determine redundancy, diversity, and
  cost. Designing a five-nines architecture for a three-nines
  requirement is gold-plating.
- **Capex versus opex is a business preference to elicit, not assume.**
  Some organizations prefer owned infrastructure (capex); others
  prefer subscription/cloud (opex) for cash-flow or agility reasons —
  the same technical need yields different designs depending on which.
- **Match architectural coupling to the delivery methodology.** Agile
  programs need modularity; do not hand an Agile team a design that
  must be built all-or-nothing.
- **Sustainability is a requirement.** Weight team capacity and
  operational complexity as heavily as technical fit; hand the
  operable design to a small team even when a more elaborate one is
  technically superior.

## Applied Design Reasoning

A brief fragment — *"A hospital group is consolidating three
independent hospital networks after a merger; regulatory uptime and
patient-data confidentiality are paramount; the combined IT team is
being formed and skills vary; leadership wants 'quick wins' visible
each quarter."* — reasoned:

```text
Business drivers: post-merger consolidation; regulatory uptime;
  data confidentiality; visible incremental progress.
Requirements: very high availability (patient safety -> five-nines
  class for clinical systems); strong segmentation and audit
  (HIPAA-class confidentiality); overlapping address space likely
  (three independent networks).
Constraints: mixed/forming team (sustainability + training);
  "quick wins quarterly" -> Agile/iterative delivery.
Design-strategy decisions:
  - Iterative delivery with a modular target architecture, because
    leadership wants quarterly wins and the team is still forming
    (favor changeability over a single big-bang optimum).
  - Segmentation-first, because confidentiality is paramount and
    merging three networks multiplies exposure.
  - Standardize and document aggressively, because a forming team of
    varied skill must operate the result (sustainability).
  Trade-off named: iterative/modular design may cost some peak
  efficiency versus a monolithic optimum -> accepted, because
  deliverability and operability are the binding constraints here.
```

## Verification and Design Review

Business-strategy design is verified by tracing every architectural
choice back to a business driver, and by the reverse check that every
stated business driver is served. Additional review questions unique
to this domain: is the availability target justified by the business
(not inflated)? Does the delivery methodology match the architecture's
coupling? Can the named team operate it? Is the continuity design
proportionate to the RPO/RTO the business actually requires? A design
that is technically sound but business-misaligned fails this review.

## References and Knowledge Checks

- CCDE v3.1 Business Strategy Design domain (15%)
- Cisco design methodology references; ITIL/PMI concepts for delivery
  context; business-continuity (RPO/RTO) references
- Volume XII — Resilience and Lifecycle Management, for continuity
  implementation detail

Knowledge checks:

1. Translate "we cannot have outages during our quarterly close" into
   two technical requirements.
2. When does an Agile delivery methodology change the *architecture*
   you would choose, and how?
3. Distinguish RPO from RTO and give a design element each one drives.
4. Give an example where the operationally sustainable design beats
   the technically optimal one, and name the requirement that decides
   it.

## Design Exercise

Take the hospital-merger brief (or a merger/expansion brief from your
experience) and produce a business-alignment design document: a table
of business drivers → requirements → architectural implications; an
availability target with its business justification; a stated delivery
methodology and one architectural consequence of it; and an RPO/RTO
pair with the continuity element each drives. Close with three
strategy-level design decisions, each written as a sentence tying it
to a business driver and naming its cost.

## Lab Verification

The exercise is verified when every architectural implication traces
to a business driver, the availability and continuity targets are
justified (not inflated), the delivery methodology's architectural
consequence is stated, and the operating team's capacity is accounted
for. Until a reviewer confirms that, the exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Business strategy leads the design: architecture serves business
drivers, availability and continuity targets come from business
requirements (and are sized to them, not inflated), the delivery
methodology shapes how modular the architecture must be, and
operational sustainability is a hard requirement. This domain is where
the CCDE separates designers who start from the business from
engineers who start from the technology.

- [ ] I start designs from business drivers and trace back to them
- [ ] I size availability and continuity to the business requirement
- [ ] I match architectural coupling to the delivery methodology
- [ ] I treat operational sustainability as a binding requirement
