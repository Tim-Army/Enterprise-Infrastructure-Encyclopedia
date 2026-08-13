# Chapter 09: Technical Architect, Currency, and Career

## Learning Objectives

- Design scalable, resilient identity architectures (Technical Architect).
- Prepare for the board-defense exam.
- Keep credentials current across the two-year cycle.
- Plan a career across the Okta ladder.
- Complete a walkthrough for architecture and currency.

## Theory and Architecture

The **Okta Certified Technical Architect** is the program's peak — validating the ability to
**design** identity solutions across an enterprise: multi-org strategy, directory and source-of-truth
architecture, authentication and authorization design, migration and coexistence, high availability
and disaster recovery, and governance. It requires the **Professional, Administrator, Consultant, and
WIC Developer** certifications first, and culminates in a **board-defense** exam — the candidate
presents and defends a solution design before Okta architects (first attempt $5,000). It is valid
**three years** (with an automatic one-year extension). Architecture is about **trade-offs**:
security vs. friction, centralization vs. autonomy, and resilience vs. cost — justified against
requirements. On **currency**: standard Okta certifications are valid **two years** and renewed by
re-examination as the platform evolves (new authenticators, governance features, Auth0 capabilities),
so tracking okta.com is ongoing. This closing chapter teaches architectural thinking and turns the
volume into a durable career and renewal plan.

## Design Considerations

Design to **requirements and trade-offs**, not features. Plan **HA/DR** and multi-org strategy. Make
**source-of-truth** and attribute flow explicit. Justify every choice for the **board defense**. Meet
**prerequisites** before attempting Architect. Renew on the **two/three-year** cycle. Match
certifications to your **career** direction.

## Implementation and Automation

The labs evaluate an architecture trade-off, outline a board-defense design, and plan currency.

## Validation and Troubleshooting

Confirm the architect/currency map:

```text
Technical Architect: design (multi-org, directory/source-of-truth, authN/authZ, migration, HA/DR, governance). Prereqs: Prof+Admin+Consultant+WIC Dev. Board defense; valid 3yr.
Currency: standard certs valid 2 years, renew by re-exam as the platform evolves. Track okta.com.
```

Common pitfalls: designing to **features** instead of requirements; and attempting **Architect**
without the prerequisite stack.

## Security and Best Practices

Design to **requirements and trade-offs**, plan **resilience**, justify choices for the **board
defense**, and renew on the **two/three-year** cycle. Practice on a developer org. All work is
defensive identity architecture.

## Hands-On Lab

Architecture and currency walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Evaluate an architecture trade-off

**Objective:** Justify a design choice.

```python
python3 - <<'PY'
options={"single global org":{"pros":"simple, central policy","cons":"blast radius, less tenant autonomy"},
         "multi-org (per region)":{"pros":"isolation, data residency","cons":"more admin overhead"}}
requirement="strict EU data residency + regional autonomy"
choice="multi-org (per region)"
for o,pc in options.items(): print(f"{o}: +{pc['pros']} / -{pc['cons']}")
print(f"\nRequirement: {requirement}\nArchitect choice: {choice} (residency + autonomy outweigh overhead)")
PY
```

**Expected result:** a design choice **justified against the requirement** — architectural thinking.

**Negative test:** pick the architecture you like best regardless of requirements; the **requirement**
(data residency) must drive it — justify to requirements.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Outline a board-defense design

**Objective:** Structure a defensible design.

```python
python3 - <<'PY'
design=["Requirements & constraints","Directory & source-of-truth","AuthN/AuthZ (MFA, policies, API access)",
        "Lifecycle & governance","Migration & coexistence","HA/DR & scale","Trade-offs & justification"]
for i,s in enumerate(design,1): print(f"{i}. {s}")
print("Board defense: present each section + defend the trade-offs against requirements")
PY
```

**Expected result:** a structured, **defensible design** outline — board-defense preparation.

**Negative test:** present a design with no **trade-off justification**; the board probes exactly
there — justify every choice.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Plan currency and career

**Objective:** Keep credentials and skills current.

```python
python3 - <<'PY'
routine={"Validity":"standard certs 2 years (Architect 3yr) — renew by re-exam",
         "Platform":"track new authenticators/governance/Auth0 features on okta.com",
         "Practice":"keep a free developer org for hands-on",
         "Career":"Professional->Administrator->Consultant->Architect; +Developer/Workflows/Auth0 by role"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — renewals, platform tracking, practice, and a
ladder plan.

**Negative test:** let a cert lapse past **two years**; it's no longer current — **re-examine** ahead
of expiry.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Technical Architect designs scalable, resilient identity to requirements and defends it before a
board; standard certifications renew on a two-year cycle (Architect three), so tracking the platform,
practicing, and climbing the ladder keeps you current.

- [ ] I can evaluate an architecture trade-off.
- [ ] I can outline a board-defense design.
- [ ] I can plan two/three-year renewal.
- [ ] I can plan a career across the ladder.
- [ ] I completed Labs 9.1–9.3 including each negative test.
