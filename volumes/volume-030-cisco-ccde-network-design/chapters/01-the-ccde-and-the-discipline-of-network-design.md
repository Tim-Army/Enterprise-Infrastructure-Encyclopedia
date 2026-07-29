# Chapter 01: The CCDE and the Discipline of Network Design

## Learning Objectives

- Distinguish network *design* from network engineering, and
  high-level design (HLD) from low-level design (LLD)
- Describe the CCDE program: the Written and Practical exams, the
  unified topics, and the elective model
- Apply the requirements → constraints → trade-offs method that
  underlies every CCDE decision
- Read a design brief and separate stated requirements, implied
  requirements, and constraints
- Explain why the "best" technology is rarely the right design answer

## Theory and Architecture

### Design is a different discipline

Every other Cisco track in this encyclopedia certifies building and
operating technology. The CCDE certifies deciding — choosing among
technologies, topologies, and protocols to satisfy a business's goals
under real constraints. A CCNP knows *how* OSPF, BGP, and segment
routing work; a CCDE knows *which* to choose for a given merger,
budget, risk tolerance, and operational team, and can defend the
choice. The exam reflects this: it is closed-book and design-only,
because looking up a command is engineering, while weighing a
trade-off is design.

### HLD versus LLD

- **High-level design (HLD)** — the architecture: topology, protocol
  selection, addressing strategy, failure domains, service model,
  security posture. It answers "what shape, and why," and it is the
  CCDE's entire focus.
- **Low-level design (LLD)** — the implementation: specific device
  models, interface assignments, exact configuration, IP addresses.
  It answers "exactly how," and it is where the CCNP work (and the
  rest of this encyclopedia) lives.

The CCDE operates at HLD. A practical-exam answer is a design decision
with rationale, not a configuration.

### The CCDE program

- **CCDE Written (400-007) v3.1** — a two-hour, 90–110-question
  multiple-choice qualifying exam on the design domains and business
  alignment. Passing it is the gate to the Practical.
- **CCDE Practical v3.1** — an eight-hour scenario-based exam. Three
  modules are **Core** (enterprise architecture and technologies); the
  fourth is a **selected elective** (Chapter 08). You are given
  evolving requirements, emails, diagrams, and constraints, and must
  make and justify design decisions as the scenario develops — a
  simulation of a real design engagement.

Both exams share one **unified** set of exam topics, five domains,
each design-oriented (see the alignment table in the volume README).

### The method that runs through everything

Every CCDE decision follows the same three-step method, and it is
worth internalizing now because Chapters 02–09 apply it repeatedly:

1. **Requirements** — what the design must achieve. *Explicit*
   (stated: "sub-second convergence," "support 50 branch sites") and
   *implicit* (unstated but necessary: a merger implies overlapping
   address space; a compliance mention implies segmentation).
2. **Constraints** — what limits the solution: budget, existing
   estate and contracts, team skills, timelines, facilities,
   regulatory boundaries, installed vendor base.
3. **Trade-offs** — because requirements and constraints conflict,
   design is choosing which to favor and being explicit about the
   cost. There is no free lunch: resilience costs money, simplicity
   costs flexibility, security costs latency and operational effort.
   The CCDE answer names the trade-off and ties it to a requirement.

The failure mode the exam punishes is reaching for the most advanced
or most familiar technology without tracing it to a requirement. The
"best" answer is the one that best fits *this* context.

## Design Considerations

- **Read for constraints first.** Novice designers optimize for
  requirements and get ambushed by constraints (budget, an installed
  base, a team that cannot operate the elegant solution). Experienced
  designers surface constraints early because they eliminate options
  fastest.
- **Separate what is asked from what is needed.** A brief that says
  "we're acquiring a competitor" has not asked for address
  translation, but it needs it. Implied requirements are where
  designs succeed or fail.
- **Design for the operator, not the architect.** A design the
  customer's team cannot run is a failed design regardless of
  technical elegance — operational sustainability is a first-class
  requirement (Domain 2).
- **Every decision is a sentence.** "I chose X because requirement/
  constraint Y, accepting cost Z." If a decision cannot be written
  that way, it is not yet a design decision — it is a preference.

## Applied Design Reasoning

The CCDE has no configuration, so this section models the reasoning an
answer should show. Given a brief fragment — *"A retailer with 400
stores wants to add guest Wi-Fi and cut WAN cost; the existing MPLS
contract has 18 months to run; the network team is four people"* — a
CCDE reads:

```text
Explicit requirements: guest Wi-Fi at stores; lower WAN cost.
Implicit requirements: guest traffic segmented from PCI cardholder
  data (retail + guest = PCI scope concern); scale to 400 sites;
  changes deployable by a small team.
Constraints: 18-month MPLS contract (cost floor until it expires);
  4-person team (operational simplicity is mandatory, not optional);
  brownfield (cannot forklift).

Trade-off framing (not yet the answer):
  SD-WAN over internet cuts WAN cost and adds segmentation, BUT the
  MPLS contract limits savings for 18 months and a 4-person team
  must be able to operate it -> favor a phased hybrid (SD-WAN
  overlay alongside MPLS now, internet-primary at contract renewal),
  because it satisfies cost + segmentation while respecting the
  contract and the team's capacity.
```

Notice: no CLI, no product SKUs — a shape and a justified sequence,
each decision tied to a requirement or constraint. That is the unit of
CCDE work.

## Verification and Design Review

A design is "verified" not by a converged lab but by review against
its brief: does every requirement (explicit and implicit) have a
design element that satisfies it; does every design element trace to a
requirement or constraint; are the trade-offs stated with their costs;
and can the customer's team operate the result? A design that adds
elements no requirement asked for is as flawed as one that misses a
requirement — gold-plating is a design defect. The habit to build:
**walk the brief and the design against each other, both directions.**

## References and Knowledge Checks

- CCDE v3.1 unified exam topics and exam format (Cisco Learning
  Network)
- Cisco Validated Designs and SRND/Preferred Architecture guides as
  models of documented design reasoning
- The design chapters of the technology volumes cross-referenced in
  the volume README

Knowledge checks:

1. Distinguish HLD from LLD with one example decision that belongs to
   each.
2. A brief mentions an imminent acquisition but asks only for "more
   bandwidth." Name two implied requirements and why they matter.
3. Rewrite a bare preference ("use segment routing") as a proper
   design decision sentence.
4. Why can the most advanced technology be the wrong design answer?
   Give a constraint that would make it so.

## Design Exercises

The CCDE is a **design** certification: there are no devices to configure and no commands to
run. In place of hands-on labs, this volume carries **topic-level Design Exercises** — scenario
briefs that ask you to produce and defend a design, the way the eight-hour practical exam does.
Work each one to a written deliverable, then review it against the brief both ways (does the
design meet every requirement, and is every design choice traceable to a requirement?). Each
chapter's exercises end with a shared **`**Lab verified by:** *pending*`** sign-off, marking the
design as reviewed only once a human has worked it.

**How to work a Design Exercise.** For every major choice, write one
*decision → driver → cost* sentence: what you chose, which requirement/constraint drove it, and
what it costs (money, complexity, risk, or a capability given up). A design with no stated costs
is not a design — it is a wish list.

### Design Exercise 1.1 — Turn a vague brief into requirements (Topic: Requirements)

> **Scenario.** A CIO says: "Our network is old and slow, we're opening three sites next year,
> and the board is worried about security. Fix it."

Produce, in writing: **functional requirements** (what the network must do), **non-functional
requirements** (availability, performance, scale, security targets — made measurable),
**constraints** (budget, timeline, existing gear, skills), and the **assumptions** you must
confirm. Rank them, and flag which are actually business drivers versus stated solutions.

**Expected result:** a structured requirements set where every vague phrase ("old and slow",
"worried about security") is converted into a testable requirement or an explicit question back
to the business — CCDE design begins by eliciting and prioritizing requirements, because you
cannot design to "fix it."

**Common mistake:** jumping to technology ("we'll deploy SD-WAN and a next-gen firewall") before
the requirements are pinned down; you may solve the wrong problem — requirements precede
solutions, always.

### Design Exercise 1.2 — Scope an HLD versus an LLD (Topic: Design deliverables)

> **Scenario.** You are handed the requirements from Exercise 1.1 and asked "what will you
> deliver, and in what order?"

Define the **High-Level Design** (topology/modules, technology choices, addressing/segmentation
strategy, resilience model — the *what and why*) and the **Low-Level Design** (specific
device configs, interface/IP assignments, protocol parameters — the *how*), and state which
decisions belong in each and why the HLD is agreed before the LLD begins.

**Expected result:** a clear split where the HLD captures the design *decisions* and their
drivers, and the LLD captures the *implementation* — the CCDE operates at the HLD level, where
trade-offs live, and confusing the two (arguing timers before topology) is a classic error.

**Common mistake:** designing at the LLD level first (picking OSPF timers before deciding the
routing hierarchy); the big decisions that constrain everything else are made in the HLD.

### Design Exercise 1.3 — Make a defensible trade-off (Topic: Decision discipline)

> **Scenario.** Two valid designs meet the requirements: (A) a simpler single-vendor fabric that
> costs more and locks you in; (B) a standards-based multi-vendor design that is cheaper but
> more complex to operate.

Write the trade-off analysis: the drivers each design serves, what each costs (capex/opex, risk,
operational skill, lock-in, agility), the assumptions that would change the answer, and a
**recommendation with its condition** ("choose A if operational simplicity and time-to-value
outweigh lock-in; choose B if cost and vendor flexibility dominate").

**Expected result:** a recommendation that names the deciding factor rather than declaring one
option universally "best" — CCDE scenarios rarely have a single right answer; they have a
best answer *given these requirements*, and your job is to make the reasoning explicit and
defensible.

**Common mistake:** asserting one option is "best practice" without tying it to the scenario's
drivers; the same choice can be right in one context and wrong in another — the justification,
not the choice, is what is graded.

## Lab Verification

For this volume, verification reviews the design artifact rather than
a lab. The exercise is verified when every requirement (explicit and
implicit) maps to a decision, every decision traces to a driver, the
trade-offs are stated with their costs, and nothing is gold-plated.
Until a reviewer confirms that, the exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCDE certifies design judgment: choosing and justifying an
architecture that fits a business's requirements and constraints, at
the HLD level, closed-book. Its method — requirements (explicit and
implicit), constraints, and explicit trade-offs — runs through every
chapter of this volume and every module of the Practical exam. The
best design is the best-fitting design, and every decision is a
sentence that names its driver and its cost.

- [ ] I can separate HLD from LLD and stay at HLD
- [ ] I read a brief for constraints and implied requirements, not
      just stated ones
- [ ] Every design decision I make is a sentence with a driver and a
      cost
- [ ] I review designs against the brief in both directions
