# Chapter 09: The CCDE Practical: Scenario Method, Trade-offs, and Readiness

## Learning Objectives

- Describe the CCDE Practical exam's structure, timing, and scenario
  format
- Apply a repeatable method to attack an evolving design scenario
  under time pressure
- Make and justify design decisions as requirements change mid-scenario
- Manage the eight hours: pacing, the elective module, and avoiding the
  common failure modes
- Assemble a readiness plan that builds design judgment, not
  memorization

## Theory and Architecture

### What the Practical actually is

The CCDE Practical v3.1 is an **eight-hour, scenario-based** design
exam. You are placed in the role of a design consultant and given a
scenario that unfolds through documents — a design brief, emails,
existing-network diagrams, meeting notes, constraints that emerge — and
you make design decisions as it develops. **Three modules are Core**
(enterprise architecture and technologies); the **fourth is your chosen
elective** (Chapter 08). It is closed-book: no lookups, because it
tests judgment, not recall. The scenario evolves deliberately — new
requirements and constraints arrive mid-module, and a good early
decision may need revisiting when the business changes its mind, which
is exactly what real design engagements do.

### The scenario method

Every module rewards the same disciplined approach — the method from
Chapter 01, executed under time pressure:

1. **Read the whole scenario before deciding anything.** The
   constraint that changes your answer is often in the last email.
   Skimming and committing early is the top failure mode.
2. **Extract requirements and constraints explicitly.** Build the
   three-column view (explicit requirements, implicit requirements,
   constraints) — mentally or on scratch paper — before designing.
3. **Identify what is actually being asked** in each question. The
   Practical asks specific design decisions, not "design everything";
   answer the question posed, in scope.
4. **Decide, and justify from a driver.** Every answer is a design
   decision tied to a requirement or constraint, with the trade-off
   acknowledged. The exam frequently offers several *workable* options
   and rewards the best-fitting one with the right reasoning.
5. **Re-evaluate when the scenario changes.** When a new requirement
   arrives, revisit affected decisions — consistency across the
   evolving scenario is itself tested. Clinging to an early decision
   after its premise changed is a failure mode.

### Trade-off analysis under pressure

The Practical's essence is trade-off analysis: given a real conflict
between requirements and constraints, choose and defend. The habits
that hold up under the clock:

- **Name the axis of the trade-off** (cost vs resilience, simplicity
  vs flexibility, security vs latency/operability) so the decision is
  reasoned, not guessed.
- **Let the binding constraint decide.** In any scenario one or two
  constraints dominate (budget, team, a contract, a regulation);
  identify them and let them break ties.
- **Prefer the operable over the clever** unless a requirement demands
  the clever — the sustainability lesson of Chapter 02, restated as an
  exam instinct.
- **Do not gold-plate.** Adding unrequested capability is a design
  defect the Practical penalizes; answer to the requirements, not to
  your enthusiasm.

### Managing the eight hours

- **Pace by module.** Budget time per module and hold to it; an
  unfinished module scores zero on its questions regardless of a
  perfect earlier one.
- **Elective last, chosen to your strength.** The fourth module is
  your elective — pick the one you actually design in (Chapter 08),
  and do not let a hard Core module rob its time.
- **Read-first discipline survives the clock.** The time "lost"
  reading the full scenario is recovered by not designing the wrong
  thing.
- **Watch for the reversal.** Scenarios plant a mid-course business
  change; expect it, and treat revisiting decisions as intended, not
  as having been wrong.

## Design Considerations

The design considerations of this chapter are the exam-taking
translations of the whole volume:

- **Method over memory.** Closed-book means judgment; a candidate who
  reasons from requirements beats one who memorized reference designs.
- **Scope discipline.** Answer the question asked at the altitude
  asked (HLD); do not drift into LLD or out-of-scope design.
- **Consistency across evolution.** The scenario is one coherent
  engagement; decisions must cohere as it changes.
- **Breadth then a chosen depth.** Strong across all five domains and
  the Core enterprise technologies, deep in one elective.

## Applied Design Reasoning

A compressed scenario-evolution illustration:

```text
Module opens: design WAN for a 300-site retailer; cost-sensitive.
  -> Draft: SD-WAN, internet-primary, MPLS at critical sites.
Email arrives: "we just signed a 3-year MPLS renewal for all sites."
  -> Revisit: internet-primary savings are now constrained for 3
     years; shift to hybrid (MPLS active + internet augment), because
     the binding constraint changed. NOT a mistake in the first
     answer -- a response to new information (the intended test).
Meeting note: "PCI audit next quarter; cardholder data at all sites."
  -> Add: segmentation of cardholder traffic across the SD-WAN overlay
     and scoped enforcement, because a compliance requirement just
     became explicit. Revisit security decisions for consistency.
Question posed: "What is your WAN transport recommendation and why?"
  -> Answer in scope: hybrid MPLS+internet with SD-WAN overlay and PCI
     segmentation, justified by the contract constraint and the
     compliance requirement, trade-off (less cost saving now, revisit
     at contract renewal) named. Do NOT redesign the campus -- out of
     scope for the question asked.
```

## Verification and Design Review

Practical readiness is verified by self-review of full practice
scenarios: did you read completely before deciding; extract
requirements and constraints; answer the questions actually asked at
HLD; justify each decision from a driver with the trade-off named;
revisit decisions when the scenario changed; and finish every module
within time. A practice scenario "passed" without that discipline
teaches the wrong habit — grade the method, not just the answer.

## References and Knowledge Checks

- CCDE v3.1 Practical exam format and release notes (Cisco Learning
  Network)
- The five-domain chapters of this volume (02–07) and the electives
  (08)
- Full-scenario practice from Cisco U. and reputable CCDE providers

Knowledge checks:

1. Why is "read the entire scenario before deciding" the highest-value
   habit, and what failure does skipping it cause?
2. A mid-module email invalidates your earlier decision. What does the
   exam expect you to do, and what does clinging to the old decision
   signal?
3. How do you decide a trade-off when several options are all workable?
4. Why is gold-plating penalized, and how do you catch yourself doing
   it?

## Design Exercise

Assemble and take a **full timed scenario** in your chosen elective:
gather (or write, from real experience) a multi-part brief with an
existing-network diagram, an evolving requirement delivered partway
through, and three or four specific design questions. Time yourself to
a module budget. Produce decisions with driver-and-trade-off
justification, revise appropriately when the injected requirement
lands, and keep every answer in scope. Then self-review against the
verification checklist above — grading your *method*, not only your
conclusions — and repeat with new scenarios until the method is
automatic.

## Lab Verification

The exercise is verified when the full scenario was completed within a
realistic time budget, every decision was justified from a driver with
its trade-off named, the injected mid-scenario change was handled with
consistency, answers stayed in scope and at HLD, and the self-review
graded the method. Until a reviewer confirms that, the exercise is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCDE Practical is an eight-hour evolving design engagement — three
Core modules and one elective, closed-book — that tests judgment through
trade-off analysis under time. The winning method is the volume's
throughout: read fully, extract requirements and constraints, answer
the question asked at HLD, justify from drivers, revisit as the
scenario changes, and never gold-plate. Build it by taking scenarios
until the method is reflex. With the five domains, the electives, and
the scenario method in hand, the CCDE is a matter of practiced
judgment.

- [ ] I read entire scenarios before committing to decisions
- [ ] I justify every decision from a driver and name the trade-off
- [ ] I revisit decisions consistently when the scenario evolves
- [ ] I practice full timed scenarios and grade my method
