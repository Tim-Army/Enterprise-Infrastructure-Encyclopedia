# Chapter 09: Architect, Currency, and Career

## Learning Objectives

- Understand the CTA and CMA architect credentials.
- Design a scalable, maintainable ServiceNow implementation.
- Keep credentials current across named releases.
- Plan a career across the ServiceNow ladder.
- Complete a walkthrough for architecture and currency.

## Theory and Architecture

At the top of the program sit the **Certified Technical Architect (CTA)** and **Certified Master
Architect (CMA)** — experience-heavy, practical credentials for those who **design** ServiceNow
solutions across an enterprise. Architecture is about **platform health and scalability**: a sound
**instance strategy** (how many instances, dev/test/prod), **data model** decisions (extend vs
create, table hygiene), **integration architecture**, **performance** (efficient queries, avoiding
customization debt), and **governance** (a Center of Excellence, coding standards, Update Set
discipline). The CMA adds enterprise-scale design and stakeholder leadership, assessed through
**practical, multi-day** evaluation. A recurring architectural principle is **"stay on the platform"**
— use out-of-box capabilities and configuration before custom code, because heavy customization
raises upgrade cost. On **currency**: ServiceNow ships **named releases roughly twice a year**, and
certifications require **delta exams** to stay current with each major release (plus new Now Assist/
GenAI credentials), so tracking servicenow.com is ongoing. This closing chapter teaches architectural
thinking and turns the volume into a durable career and renewal plan.

## Design Considerations

Design a clean **instance strategy** and **data model** (extend before create). Minimize
**customization** (upgrade cost). Govern with a **CoE**, coding standards, and Update Set discipline.
Plan **integration** and **performance** deliberately. Keep certifications current with **delta exams**
each named release. Match credentials to your **career** direction.

## Implementation and Automation

The labs evaluate an architecture decision, plan governance, and plan currency/career.

## Validation and Troubleshooting

Confirm the architect/currency model:

```text
CTA/CMA: design (instance strategy, data model, integration, performance, governance/CoE). Principle: stay on the platform (config before custom code -> lower upgrade cost). CMA = enterprise-scale, multi-day practical.
Currency: named releases ~twice a year; delta exams keep certs current; new Now Assist/GenAI credentials. Track servicenow.com.
```

Common pitfalls: heavy **customization** (painful upgrades); and letting certifications go **stale**
across named releases (skip the delta exam).

## Security and Best Practices

Design for **platform health** (clean data model, minimal customization, governance), stay
**out-of-box** where possible, and keep certifications current with **delta exams**. Match certs to
your career. All work is authorized architecture.

## Hands-On Lab

Architecture and currency walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Evaluate an architecture decision

**Objective:** Choose config over customization.

```python
python3 - <<'PY'
options={"out-of-box + configuration":{"upgrade_cost":"low","time":"fast","fit":"90%"},
         "heavy custom code":{"upgrade_cost":"high","time":"slow","fit":"100%"}}
requirement="approval workflow with one unusual step"
choice="out-of-box + configuration (accept 90% fit; small config for the edge case)"
for o,d in options.items(): print(f"{o}: {d}")
print(f"\nRequirement: {requirement}\nArchitect choice: {choice} (minimize upgrade cost)")
PY
```

**Expected result:** the **configuration-first** choice justified by lower upgrade cost — architectural
thinking.

**Negative test:** build heavy custom code for a 10% edge case; upgrades become painful — **stay on the
platform**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan platform governance

**Objective:** Keep the instance healthy.

```python
python3 - <<'PY'
governance={"CoE":"Center of Excellence owns standards + reviews","instances":"dev -> test -> prod (no direct prod edits)",
            "standards":"naming, coding, Update Set discipline","reviews":"design + code review before promotion"}
for k,v in governance.items(): print(f"{k:11}: {v}")
print("CTA/CMA: governance (CoE + standards + review) keeps a growing platform maintainable")
PY
```

**Expected result:** a **governance** model (CoE, instance strategy, standards, review) — sustainable
scale.

**Negative test:** let every team build freely with no standards; the platform becomes unmaintainable
— govern with a **CoE**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Plan currency and career

**Objective:** Stay current and plan a path.

```python
python3 - <<'PY'
routine={"Releases":"named releases ~twice a year -> take delta exams to keep certs current",
         "New credentials":"track Now Assist/GenAI + new CIS specializations on servicenow.com",
         "Practice":"keep a free Personal Developer Instance (PDI)",
         "Career":"CSA -> CAD/CIS (your product area) -> CTA -> CMA"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — delta exams, new credentials, PDI, and a path.

**Negative test:** skip the **delta exam** after a named release; your certification goes stale —
take it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CTA/CMA architect tiers design scalable, governed ServiceNow implementations that stay on the
platform; because named releases ship twice a year with delta exams and new Now Assist credentials,
tracking releases and stacking from CSA keeps you current.

- [ ] I can evaluate a config-vs-customization decision.
- [ ] I can plan platform governance.
- [ ] I can plan release-delta currency.
- [ ] I can plan a career across the ladder.
- [ ] I completed Labs 9.1–9.3 including each negative test.
