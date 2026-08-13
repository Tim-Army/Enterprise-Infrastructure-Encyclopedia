# Chapter 08: Process Discovery, Bot Insight, and the CoE

## Learning Objectives

- Explain Process Discovery — finding the right processes to automate.
- Describe Bot Insight — measuring automation impact.
- Understand the Center of Excellence (CoE) and how automation scales.
- Recognize the business case: ROI, prioritization, and adoption.

*Cert relevance: discovery, measurement, and the CoE frame the program-level competency beyond building single bots.*

## Finding what to automate

A common failure of automation programs is **automating the wrong things** — pouring effort into a process that is low-value, unstable, or a poor fit. **Process Discovery** addresses this: it **analyzes how work is actually done** (from user interactions and system logs) to **surface automation opportunities** — the high-volume, repetitive, rules-based tasks where bots pay off most. Rather than guessing, you **discover** the best candidates from real evidence.

Process Discovery answers "**what should we automate first?**" with data: which processes are frequent, standardized, and time-consuming enough to justify a bot. Choosing well is what makes a program deliver value instead of building bots nobody needed. The lab scores automation candidates.

## Measuring impact with Bot Insight

Once bots run, you must **prove and improve** their value. **Bot Insight** is Automation Anywhere's **analytics**: it measures what the automation fleet is doing and the impact it delivers:

- **Operational metrics** — how many bots ran, success/failure rates, items processed, exceptions.
- **Business metrics** — hours saved, transactions completed, error reduction, cost avoided.
- **Dashboards** — surface this to operators (health) and to leadership (ROI).

Measurement closes the loop: it justifies continued investment, highlights failing or low-value bots to fix or retire, and turns automation from an act of faith into a **managed, data-driven program**. The lab computes automation ROI. *(This measurement discipline parallels observability across the encyclopedia — you cannot manage what you do not measure.)*

## The Center of Excellence

Scaling automation from a few bots to an enterprise program needs **organization**, not just technology. A **Center of Excellence (CoE)** is the team and operating model that makes automation scale:

- **Standards and reuse** — shared components, naming, and best practices so bots are consistent and maintainable ([Ch 3](03-building-bots.md)).
- **Governance** — the RBAC, credential, and audit discipline ([Ch 4](04-the-control-room.md)) applied as policy across teams.
- **Pipeline** — a repeatable flow from **discovery** (find) → **prioritization** (business case) → **build** → **deploy** → **measure** (Bot Insight) → **improve**.
- **Enablement** — training, support, and citizen-developer programs (aided by Automation Co-Pilot, [Ch 5](05-attended-unattended-and-copilot.md)) to spread capability.

The CoE is what turns individual automations into a **sustained capability** — the difference between a few bots and a digital workforce. The lab models the CoE pipeline.

## The business case

Underlying all of it is a **business case**. Automation competes for investment, so an automation engineer must think beyond the bot:

- **ROI** — value delivered (hours saved × rate, error/cost reduction) versus cost to build and run.
- **Prioritization** — sequence the backlog by value and feasibility (discovery informs this).
- **Adoption** — a technically perfect bot delivers nothing if people do not use it; change management and Co-Pilot-in-the-flow drive uptake.

Understanding discovery, measurement, the CoE, and ROI is the **program-level** competency that distinguishes an automation **leader** from a bot builder — and it is what makes an automation practice durable. The lab ties value to prioritization. *(These program concerns are shared with the automation platforms in [UiPath (CXLIX)](../../volume-149-uipath-certifications/README.md) and [Pega (CLXIV)](../../volume-164-pega-certifications/README.md).)*

## Hands-On Lab

Python models discovery scoring, Bot Insight ROI, and the CoE pipeline. **Cost:** none.

### Lab 8.1 — Discover, measure, and prioritize

**Objective:** Score automation candidates, compute ROI, and sequence the backlog through a CoE pipeline.

```bash
python3 - <<'EOF'
# PROCESS DISCOVERY: score candidates by volume, standardization, and rules-fit
CANDIDATES = [
  {"name": "invoice entry",     "volume": 5000, "standardized": 0.9, "rules_based": 0.9, "hours_each": 0.10},
  {"name": "contract review",   "volume": 200,  "standardized": 0.3, "rules_based": 0.2, "hours_each": 1.0},
  {"name": "password resets",   "volume": 3000, "standardized": 0.95,"rules_based": 0.95,"hours_each": 0.05},
]
def fit_score(c):  # higher = better automation candidate
    return round(c["volume"] * c["standardized"] * c["rules_based"] / 1000, 2)

print("1) PROCESS DISCOVERY — score candidates (volume x standardized x rules-based):")
for c in CANDIDATES:
    c["score"] = fit_score(c)
    print(f"      {c['name']:16} score={c['score']}")
ranked = sorted(CANDIDATES, key=lambda c: c["score"], reverse=True)

# BOT INSIGHT: ROI = hours saved (value) vs build+run cost
RATE, BUILD_COST = 40, 4000     # $/hr, one-time build cost per bot
print("\n2) BOT INSIGHT — ROI per candidate (annual hours saved vs cost):")
for c in ranked:
    hours_saved = c["volume"] * c["hours_each"]
    value = hours_saved * RATE
    roi = round((value - BUILD_COST) / BUILD_COST, 1)
    c["roi"] = roi
    print(f"      {c['name']:16} hours_saved={hours_saved:>5.0f}  value=${value:>7.0f}  ROI={roi}x")

# CoE PIPELINE: discover -> prioritize (by score AND ROI) -> build -> deploy -> measure -> improve
print("\n3) CoE PIPELINE — prioritized backlog (build high score + positive ROI first):")
backlog = [c for c in ranked if c["score"] >= 1 and c["roi"] > 0]
for i, c in enumerate(backlog, 1):
    print(f"      {i}. {c['name']} (score {c['score']}, ROI {c['roi']}x)")
print(f"      deferred (poor fit / negative ROI): {[c['name'] for c in CANDIDATES if c not in backlog]}")
print()
print("PROCESS DISCOVERY scores candidates from real evidence (invoice entry + password resets")
print("are high-volume/standardized/rules-based; contract review is not). BOT INSIGHT computes")
print("ROI (hours saved x rate vs build cost). The CoE PIPELINE prioritizes high-fit, positive-ROI")
print("work and defers poor fits — turning automation into a data-driven PROGRAM, not scattered bots.")
EOF
```

**Expected result:** Discovery scores invoice-entry and password-resets high (high volume, standardized, rules-based) and contract-review low; Bot Insight computes ROI per candidate; and the CoE pipeline prioritizes the high-fit, positive-ROI automations while deferring the poor fit. The lesson is the program-level discipline: discover the right processes from evidence, measure impact and ROI, and run a CoE pipeline that prioritizes value — the competency that scales automation beyond individual bots.

**Negative test:** Automating whatever is requested with no discovery or ROI. Effort goes into a low-volume, unstandardized process (contract review) that a bot handles poorly and that never pays back; discovery scoring and ROI measurement are what direct effort to the automations that deliver.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Process Discovery understood — finding high-value automation candidates from real evidence.
- [ ] Bot Insight understood — measuring operational and business impact and ROI.
- [ ] The CoE understood — standards, governance, pipeline, and enablement that scale automation.
- [ ] The business case understood — ROI, prioritization, and adoption beyond building the bot.

## See also

- [Chapter 04 — The Control Room](04-the-control-room.md) — the governance the CoE applies as policy.
- [Chapter 09 — Choosing Your Automation Anywhere Path](09-choosing-your-path.md) — turning these skills into a role and plan.
- [Chapter 01 — The Automation Anywhere Certification Program](01-the-automation-anywhere-program.md) — the certifications that map to these skills.
