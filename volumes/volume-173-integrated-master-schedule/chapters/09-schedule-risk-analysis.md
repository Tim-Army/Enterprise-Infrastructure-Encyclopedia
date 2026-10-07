# Chapter 09: Schedule Risk Analysis

## Learning Objectives

- Explain why a single deterministic finish date overstates confidence.
- Prepare three-point duration estimates and discrete risk events for a schedule
  risk analysis (SRA).
- Run a Monte Carlo simulation and interpret P50 and P80 dates, criticality
  indices, and sensitivity results.
- Explain merge bias and why parallel paths push finish dates later.
- Size schedule margin from SRA results.

## Theory and Architecture

The critical path method gives one finish date, computed as if every duration
were exactly right. Real durations vary, and the variation is lopsided: tasks
rarely finish much early, but they can finish very late. A **schedule risk
analysis (SRA)** replaces single durations with ranges and simulates the
schedule thousands of times to show the *probability* of meeting each date. The
GAO's eighth best practice calls for one, and DoD guidance expects SRAs on major
programs.

### Inputs

| Input | What it is | Example |
| --- | --- | --- |
| **Three-point estimates** | Optimistic, most likely, and pessimistic durations for uncertain tasks | Hardware delivery: 20 / 30 / 50 days |
| **Distribution** | The shape used to sample between the three points | Triangular or BetaPERT |
| **Risk events** | Discrete risks from the risk register, with a probability and an impact on specific tasks | 30% chance of a customs hold adding 10 days to delivery |
| **Correlation** | Tasks whose durations tend to move together | Four site cutovers by the same team |

Get three-point estimates from the people doing the work, and challenge
pessimistic values that are too optimistic. A narrow range is the most common
SRA mistake.

### Monte Carlo simulation

```text
repeat 5,000 times:
    for each task: sample a duration from its distribution
    for each risk event: roll whether it occurs; if so, add its impact
    run the forward pass (Chapter 05) and record the finish date
    record which tasks were on the critical path
sort the 5,000 finish dates → a probability distribution
```

### Outputs

| Output | Meaning |
| --- | --- |
| **P50, P80, and other percentiles** | The date by which the program finishes in 50 percent, 80 percent, and so on, of simulated outcomes |
| **Probability of the deterministic date** | How often the simulated finish is on or before the CPM finish; usually well under 50 percent |
| **Criticality index** | The share of simulations in which a task was on the critical path |
| **Sensitivity (tornado chart)** | Which tasks' duration uncertainty most affects the finish |

### Merge bias

Where several paths join, the task after the join starts when the *latest* path
finishes. Each path might have a reasonable chance of finishing on time, but the
chance that *all* of them do is lower. This **merge bias** is why simulated
finish dates are later than the CPM date even when every task's most likely
duration equals its CPM duration. Schedules with many parallel paths feeding
milestones are especially affected.

### Sizing margin

SRA gives a defensible basis for schedule margin (Chapter 05). For the sample
program in this chapter, the deterministic finish is day 99 and the simulated
P80 is about day 124, so holding about 25 days of margin before the committed
date gives roughly 80 percent confidence, provided the inputs are honest.

## Design Considerations

- **Start from a healthy schedule.** An SRA on a network with open ends or hard
  constraints produces meaningless results. Pass the Chapter 06 checks first.
- **Model only real uncertainty.** Give ranges to tasks that are genuinely
  uncertain; keep fixed durations for fixed events such as a contractual review
  date.
- **Include discrete risks from the risk register.** Duration ranges capture
  everyday variation; risk events capture specific things that might go wrong.
  Keep them consistent with the program's risk register.
- **Account for correlation.** Treating related tasks as independent lets high
  and low samples cancel out, which understates risk.
- **Report confidence, not just dates.** "The baseline finish has a 25 percent
  chance; the P80 is three weeks later" is more useful than a single date.

## Implementation and Automation

### Tool options

| Tool | SRA option |
| --- | --- |
| Microsoft Project | Third-party add-ins, such as Barbecana Full Monte or @RISK for Project |
| Primavera P6 | Oracle Primavera Risk Analysis, or third-party tools that read P6 data (for example Deltek Acumen Risk or Safran Risk) |
| ProjectLibre | No built-in or common add-in; export the network and use a script such as the one below |

Commercial SRA tools read the schedule directly, apply ranges and risks, and
produce histograms, tornado charts, and criticality reports.

### A Monte Carlo script for the sample program

This script simulates the sample network from Chapter 03 with three-point
estimates and one risk event. It uses only the Python standard library:

```python
#!/usr/bin/env python3
"""Monte Carlo schedule risk analysis of the sample branch network IMS."""
import random
import statistics

# id: (optimistic, most likely, pessimistic, [(predecessor, type, lag), ...])
TASKS = {
    1: (0, 0, 0, []),
    2: (1, 1, 1, [(1, "FS", 0)]),
    3: (8, 10, 15, [(2, "FS", 0)]),
    4: (8, 10, 16, [(3, "FS", 0)]),
    5: (4, 5, 10, [(4, "FS", 0)]),
    6: (2, 2, 3, [(5, "FS", 0)]),
    7: (0, 0, 0, [(6, "FS", 0)]),
    8: (2, 3, 5, [(5, "FS", 0)]),
    9: (2, 2, 2, [(8, "FS", 0)]),
    10: (20, 30, 50, [(9, "FS", 0)]),
    11: (2, 3, 5, [(10, "FS", 0)]),
    12: (4, 5, 7, [(7, "FS", 0)]),
    13: (8, 10, 18, [(12, "FS", 0)]),
    14: (4, 5, 10, [(11, "FS", 0), (13, "FS", 0)]),
    15: (0, 0, 0, [(14, "FS", 0)]),
    16: (4, 5, 9, [(15, "FS", 0)]),
    17: (4, 5, 9, [(16, "FS", 0)]),
    18: (4, 5, 9, [(17, "FS", 0)]),
    19: (4, 5, 9, [(18, "FS", 0)]),
    20: (0, 0, 0, [(19, "FS", 0)]),
    21: (8, 10, 15, [(20, "FS", 0)]),
    22: (8, 10, 14, [(13, "SS", 5)]),
    23: (3, 3, 4, [(20, "FS", 0), (22, "FS", 0)]),
    24: (0, 0, 0, [(21, "FS", 0), (23, "FS", 0)]),
    25: (0, 0, 0, [(24, "FS", 0)]),
}
RISKS = [  # (task, probability, added days)
    (10, 0.30, 10),  # customs hold on the hardware shipment
]
RUNS = 5000

def simulate(durations):
    start, finish, driver = {}, {}, {}
    for tid in sorted(TASKS):
        es, drv = 0.0, None
        for pred, kind, lag in TASKS[tid][3]:
            ref = (start[pred] if kind == "SS" else finish[pred]) + lag
            if ref >= es:
                es, drv = ref, pred
        start[tid], finish[tid], driver[tid] = es, es + durations[tid], drv
    path, node = set(), max(TASKS)
    while node is not None:  # walk the driving predecessors back from the finish
        path.add(node)
        node = driver[node]
    return finish[max(TASKS)], path

random.seed(1)
deterministic, _ = simulate({t: v[1] for t, v in TASKS.items()})
finishes, critical = [], {t: 0 for t in TASKS}
for _ in range(RUNS):
    durations = {t: (random.triangular(o, p, m) if p > o else m) for t, (o, m, p, _) in TASKS.items()}
    for task, prob, days in RISKS:
        if random.random() < prob:
            durations[task] += days
    end, path = simulate(durations)
    finishes.append(end)
    for t in path:
        critical[t] += 1

finishes.sort()
pct = lambda p: finishes[min(int(p / 100 * RUNS), RUNS - 1)]
print(f"Deterministic (CPM) finish: day {deterministic:.0f}")
print(f"Mean {statistics.mean(finishes):.1f}  P10 {pct(10):.1f}  P50 {pct(50):.1f}  "
      f"P80 {pct(80):.1f}  P90 {pct(90):.1f}")
print(f"Probability of finishing by day {deterministic:.0f}: "
      f"{100 * sum(f <= deterministic for f in finishes) / RUNS:.1f}%")
print("Criticality index (share of runs on the critical path), tasks with work:")
for t in sorted(critical, key=lambda t: (-critical[t], t)):
    if TASKS[t][2] > 0:
        print(f"  task {t:>2}: {100 * critical[t] / RUNS:5.1f}%")
```

The script walks each run's **driving path**: for every task, it records the
predecessor that set its start, then traces those back from the finish
milestone. Tasks on that chain are counted as critical for the run.

## Validation and Troubleshooting

- **The P50 equals the deterministic date.** Ranges may be symmetric or too
  narrow. Check pessimistic values with the task owners, and confirm the
  distribution is skewed where it should be.
- **Results change a lot between runs.** Use more iterations (5,000 or more) and
  a fixed random seed when comparing scenarios.
- **A non-critical task has a high criticality index.** It has little float and
  wide uncertainty, so it often becomes critical. Treat it as near-critical and
  manage it.
- **The commercial tool and the script disagree.** Check that both use the same
  ranges, distributions, risk events, calendars, and handling of correlation.

## Security and Best Practices

- Record the source of every three-point estimate and risk event, so the SRA can
  be repeated and challenged.
- Re-run the SRA at major milestones and when significant risks change.
- Present results as ranges and probabilities to decision makers, with the
  assumptions behind them.
- Keep SRA inputs and outputs with the IMS cycle archive; they are part of the
  program's evidence for its dates.

## References and Knowledge Checks

**References:**

- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G), best practice on
  conducting a schedule risk analysis.
- NASA, *Schedule Management Handbook* (schedule risk analysis chapter).
- AACE International, recommended practices on schedule risk analysis.
- Documentation for the SRA tools listed in the Implementation section.

**Knowledge checks:**

1. Why does a deterministic CPM finish usually have less than a 50 percent
   chance of being met?
2. What are the inputs to an SRA?
3. Explain merge bias in one or two sentences.
4. What does a criticality index of 60 percent mean for a task?
5. How would you use a P80 result to size schedule margin?

## Hands-On Lab

**Objective:** Run a Monte Carlo SRA on the sample program, interpret it, and
size margin.

**Shared prerequisites** — Python 3. Commercial SRA tools are optional; the
script covers all three scheduling tools by working from the network itself.
**Cost:** none.

### Lab 9.1 — Run the simulation

**Objective:** Produce the finish date distribution.

1. Save the script as `sra.py` and run it: `python3 sra.py`.
2. Record the deterministic finish, P50, P80, and the probability of finishing by
   the deterministic date.

**Expected result:** a deterministic finish of day 99, a P50 of about day 116, a
P80 of about day 124, and only about a 1 percent chance of finishing by day 99,
because the ranges are skewed late and the risk event adds delay. (Exact values
vary slightly with the random seed and Python version.)

**Negative test:** set every task's optimistic, most likely, and pessimistic
values equal and remove the risk event. Every run gives day 99 and the
probability is 100 percent: without uncertainty, simulation adds nothing.
Restore the inputs.

**Rollback:** restore the original script.

### Lab 9.2 — Read the criticality index

**Objective:** Find which tasks most often drive the finish.

1. Read the criticality index output.
2. Compare it with the deterministic critical path from Chapter 05.

**Expected result:** the hardware path (tasks 8 to 11), the site cutovers, and
acceptance testing are critical in every run, while the design document and
template path (tasks 6, 12, and 13) is never critical: its 21 days of float is
more than its uncertainty can consume.

**Negative test:** change hardware delivery's range to 5 / 8 / 12 days and re-run.
The design and template path now becomes critical in most runs and the hardware
tasks in a minority, which shows how a criticality index follows where the
uncertainty and float are.

**Rollback:** restore the original range.

### Lab 9.3 — Size schedule margin

**Objective:** Turn SRA results into a margin recommendation.

1. Calculate margin as P80 minus the deterministic finish.
2. Compare it with the 10-day margin added in Chapter 05.

**Expected result:** a recommendation of about 25 days (P80 of about day 124 minus
day 99), well above the arbitrary 10 days used in Chapter 05.

**Negative test:** double the risk event's probability to 60 percent and re-run.
The P80 and the recommended margin grow, which shows why margin must be revisited
when risks change.

**Rollback:** restore the risk probability.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A deterministic CPM date hides uncertainty. A schedule risk analysis uses
three-point estimates, risk events, and correlation in a Monte Carlo simulation
to produce probabilistic finish dates, criticality indices, and sensitivity
results. Skewed durations and merge bias push likely finishes later than the CPM
date. P80 results provide a defensible basis for schedule margin, and the SRA
should be repeated as the program and its risks change.

- [ ] Can explain why CPM dates overstate confidence.
- [ ] Can prepare SRA inputs: three-point estimates, risk events, correlation.
- [ ] Can run a simulation and interpret percentiles and criticality indices.
- [ ] Can explain merge bias and size margin from P80 results.
- [ ] Completed Labs 9.1–9.3 including each negative test.
