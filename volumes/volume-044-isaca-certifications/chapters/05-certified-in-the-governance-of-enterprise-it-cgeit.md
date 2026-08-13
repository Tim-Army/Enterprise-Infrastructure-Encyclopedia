# Chapter 05: Certified in the Governance of Enterprise IT (CGEIT)

## Learning Objectives

- Explain what CGEIT certifies and who should pursue it.
- List the four CGEIT domains and their exam weights.
- Apply enterprise IT-governance thinking: frameworks, resources, value, and risk.
- Relate CGEIT to COBIT and to CISM/CRISC.
- Complete a per-domain walkthrough for each CGEIT domain.

## Theory and Architecture

The **Certified in the Governance of Enterprise IT (CGEIT)** is ISACA's
**board- and executive-facing** credential for professionals who **govern** IT at
the enterprise level — establishing the governance framework, allocating
resources, realizing value from IT investments, and optimizing risk. It is the
most strategic of ISACA's certifications. The exam is **150 questions** across
four weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Governance of Enterprise IT | 40% |
| 2 | IT Resources | 15% |
| 3 | Benefits Realization | 26% |
| 4 | Risk Optimization | 19% |

**Governance of Enterprise IT (40%)** dominates — the framework, structures, and
strategy of governance are the core of the exam.

## Design Considerations

CGEIT is for **senior** professionals — CIOs, IT directors, governance and
audit leaders — who set direction rather than operate controls. It aligns tightly
with **COBIT** (ISACA's governance framework). Study Domain 1 as the backbone
(governance framework, operating model, strategy alignment), and treat resources,
value, and risk as what governance directs and monitors. CGEIT complements
**CRISC** (risk) and **CISM** (security management) with the top-level governance
view.

## Implementation and Automation

The labs below model the governance artifacts: a governance framework/operating
model (D1), a resource-allocation decision (D2), a benefits/value case (D3), and a
risk-optimization decision balancing risk and opportunity (D4).

## Validation and Troubleshooting

Confirm the CGEIT blueprint before studying:

```text
isaca.org > Credentialing > CGEIT > Exam Content Outline:
  - four domains and weights (40/15/26/19), 150 questions
  - five years of enterprise IT governance experience
```

Common pitfalls: approaching CGEIT operationally instead of **strategically**;
under-weighting the dominant **Governance** domain; and treating **benefits
realization** as accounting rather than governed **value delivery**.

## Security and Best Practices

Govern with a recognized framework (**COBIT**), define clear **decision rights**
and accountability, tie IT investment to **business value** and monitor its
realization, and **optimize** (not merely minimize) risk against opportunity.
Renew via CPE and the annual maintenance fee.

## References and Knowledge Checks

- isaca.org: *CGEIT* Exam Content Outline and review manual; COBIT 2019.

**Knowledge checks**

1. Which CGEIT domain dominates, and what does it cover?
2. What does "risk optimization" mean versus risk minimization?
3. How does CGEIT relate to COBIT?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CGEIT domain**.

**Shared prerequisites** — a Linux shell with `python3`. **Cost:** none.

### Lab 5.1 — CGEIT D1: Governance of Enterprise IT (40%)

**Objective:** Define governance decision rights (who decides what).

```bash
python3 - <<'PY'
raci = {"IT strategy":"Board=A, CIO=R, Exec Committee=C",
        "IT investment approval":"Investment Board=A, CIO=R, CFO=C",
        "Architecture standards":"Architecture Board=A, Enterprise Architect=R"}
for decision,rights in raci.items(): print(f"{decision:24} -> {rights}")
PY
```

**Expected result:** governance decisions mapped to accountable/responsible bodies
— the governance framework/operating model that is CGEIT's dominant domain.

**Negative test:** leave IT decision rights undefined; governance requires clear
**accountability** for each decision — define it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — CGEIT D2: IT Resources (15%)

**Objective:** Allocate constrained IT resources to strategy.

```bash
python3 - <<'PY'
budget=100  # units
alloc={"Keep-the-lights-on":45,"Strategic transformation":35,"Innovation/experiment":20}
print("Portfolio allocation (must sum to budget):", sum(alloc.values())==budget)
for k,v in alloc.items(): print(f"  {k:26} {v}%")
PY
```

**Expected result:** a resource portfolio summing to budget across run/grow/
transform — the resource-allocation governance of Domain 2.

**Negative test:** spend everything on "keep the lights on"; governance balances
**run vs grow vs transform** — allocate deliberately.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — CGEIT D3: Benefits Realization (26%)

**Objective:** Build a value case and track realization.

```bash
python3 - <<'PY'
invest=500000; expected_annual_benefit=250000; realized_year1=180000
roi = (expected_annual_benefit - invest*0.2)/invest
print(f"Expected ROI ~ {roi*100:.0f}% ; Year-1 realized ${realized_year1:,} of ${expected_annual_benefit:,}")
print("Governance action: investigate the realization gap; adjust or stop if value not delivered.")
PY
```

**Expected result:** an ROI/value case and a realization gap to govern — the
benefits-realization domain (D3), CGEIT's second-largest.

**Negative test:** approve an investment and never track its benefits; governance
**monitors value delivery**, not just approval.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — CGEIT D4: Risk Optimization (19%)

**Objective:** Optimize (not just minimize) risk against opportunity.

```bash
python3 - <<'PY'
options = {"Ship fast, more risk":("higher reward","MODERATE risk within appetite -> proceed"),
           "Delay for full hardening":("lower reward","LOW risk but misses market -> weigh cost")}
for opt,(reward,decision) in options.items(): print(f"{opt:26} {reward:14} -> {decision}")
PY
```

**Expected result:** a decision balancing risk and opportunity within appetite —
risk **optimization** (Domain 4), not blanket minimization.

**Negative test:** minimize all risk regardless of opportunity cost; governance
**optimizes** risk to enable value — over-controlling destroys value too.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CGEIT is ISACA's enterprise IT-governance credential: four domains weighted
40/15/26/19, dominated by the governance framework itself. It is the strategic,
board-facing tier — decision rights, resource allocation, value realization, and
risk optimization — aligned to COBIT and complementing CRISC and CISM.

- [ ] I can list the four CGEIT domains and their weights.
- [ ] I can define governance decision rights and allocate a portfolio.
- [ ] I can build a value case and track benefits realization.
- [ ] I can optimize risk against opportunity within appetite.
- [ ] I completed Labs 5.1–5.4 including each negative test.
