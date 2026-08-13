# Chapter 07: Process Discovery and Mining

## Learning Objectives

- Explain why choosing *what* to automate is as important as building it.
- Understand Process Mining and Task Mining as discovery tools.
- Prioritize automation candidates by ROI.
- Place the Business Analyst role and the automation pipeline.

*Cert relevance: process discovery and prioritization are the **Automation Business Analyst Professional** certification.*

## Automating the wrong thing

The most expensive automation mistake is not a bug — it is **automating the wrong process**. A beautifully-built automation of a process that runs twice a month, or that is about to be replaced, or that only saves a few minutes, is wasted effort. Conversely, the biggest wins come from finding the **high-volume, repetitive, stable, rule-heavy** processes where automation compounds. **Choosing what to automate is a discipline**, and it is the heart of the **Business Analyst** role.

The naive approach is to ask people what is painful — which surfaces the *loudest* complaints, not the *highest-value* opportunities. The better approach is **data-driven discovery**: measure how work actually flows and where the time goes, then prioritize by return.

## Process Mining and Task Mining

UiPath provides two discovery tools:

| Tool | Looks at | Answers |
|:---|:---|:---|
| **Process Mining** | Event logs from enterprise systems (ERP, CRM) | How does this *process* actually flow, end to end, including the detours? |
| **Task Mining** | User actions on the desktop (clicks, keystrokes) | What *tasks* do people actually do repetitively? |

**Process Mining** reconstructs the real process from system event logs — revealing that the "simple" purchase-order process actually has 40 variants, loops back for rework 30% of the time, and bottlenecks at approval. **Task Mining** watches (with consent) what people actually do at their desks, finding the repetitive copy-paste-between-apps tasks ripe for automation. Together they replace *opinion* about what to automate with *evidence*. **Automation Hub** then manages the pipeline of candidate ideas. The lab models ROI-based prioritization.

## Prioritizing by ROI

Once you have candidates, you **prioritize by return on investment**: the value of automating (volume × time-saved-per-run × frequency, minus errors avoided) against the cost (build effort, maintenance). A high-volume daily task that takes a person ten minutes is worth far more to automate than a monthly task that takes an hour — even though the monthly one *feels* more painful each time. Prioritization by ROI, not by loudness, is what makes an automation program deliver value. The lab models the calculation.

## Hands-On Lab

Python models automation prioritization. **Cost:** none.

### Lab 7.1 — Prioritize automation candidates by ROI

**Objective:** Rank candidates by return, not by how painful they feel.

```bash
python3 - <<'EOF'
# candidate processes with volume, time each, and build cost
CANDIDATES = [
  # name,                  runs/month, minutes/run, build_days, "loudness" (complaints)
  ("invoice entry",         6000,       8,           15,          "medium"),
  ("month-end report",      1,          240,         10,          "LOUD (everyone hates it)"),
  ("password reset tickets", 900,       6,           8,           "low"),
  ("quarterly audit pull",  4,          180,         12,          "loud"),
  ("onboarding data entry", 300,        25,          10,          "medium"),
]
MINUTES_PER_WORKDAY = 8*60
LOADED_COST_PER_MIN = 0.75   # $ per person-minute
BUILD_DAY_COST = 900

print(f"{'candidate':24}{'hrs saved/mo':>13}{'$ saved/mo':>12}{'build $':>10}{'payback(mo)':>12}")
scored = []
for name, runs, mins, build, loud in CANDIDATES:
    mins_saved = runs * mins
    hrs = mins_saved/60
    val = mins_saved * LOADED_COST_PER_MIN
    cost = build * BUILD_DAY_COST
    payback = cost/val if val else 999
    scored.append((name, hrs, val, cost, payback, loud))
for name, hrs, val, cost, payback, loud in sorted(scored, key=lambda x: x[4]):
    print(f"{name:24}{hrs:>13.0f}{val:>12,.0f}{cost:>10,.0f}{payback:>12.1f}")
print("\nRanked by PAYBACK (build cost / monthly savings), fastest first:")
print("  invoice entry + password resets pay back in DAYS-to-WEEKS: high volume x")
print("     small time each = huge monthly savings. These are the winners.")
print("  the 'month-end report' everyone HATES? Runs ONCE a month. Even at 4 hours,")
print("     it saves 4 hrs/mo — payback measured in YEARS. Loud, but low ROI.")
print("  the audit pull: only 4 runs a month — tiny volume, so ~20-month payback.")
print("\nThe discipline: prioritize by ROI (volume x time x frequency), NOT by how much")
print("people complain. The loudest pain is often a rare, low-volume task; the biggest")
print("VALUE is usually an unglamorous high-volume one nobody thinks to mention. This")
print("is why Process/Task Mining matter — they measure REAL volume and flow, replacing")
print("'what feels painful' with 'what actually costs the most time.' The Business")
print("Analyst's core skill.")
EOF
```

**Expected result:** High-volume small-time tasks (invoice entry, password resets) ranking far above a loudly-hated but once-monthly report on payback, because ROI is volume times time times frequency. The prioritization lesson is to rank by return, not by how painful something feels — the loudest pain is often low-volume, while the biggest value is an unglamorous high-volume task that mining surfaces with evidence.

**Negative test:** Automating the process people complain about most. The hated month-end report runs once a month, so automating it saves little; ROI-based prioritization surfaces the high-volume tasks that actually cost the most time.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Choosing what to automate recognized as a discipline as important as building — automating the wrong process wastes effort.
- [ ] Process Mining and Task Mining understood as evidence-based discovery of real process flow and repetitive tasks.
- [ ] ROI prioritization understood — rank by volume × time × frequency, not by how loud the complaint is.
- [ ] The Business Analyst role and the Automation Hub pipeline placed in the automation program.
