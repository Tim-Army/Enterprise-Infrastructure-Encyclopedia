# Chapter 03: Storage, Plans, and Retention Policies

## Learning Objectives

- Configure plans and storage policies that express business retention requirements.
- Model retention rules, including cycles and the grandfather-father-son pattern.
- Place data across storage tiers and calculate the cost consequences.
- Distinguish backup retention from archival and legal hold.

## Plans and storage policies

A **plan** (the modern Command Center construct; historically a **storage policy**) is the object that binds together *what* gets protected, *where the copies go*, *how long they are kept*, and *when the job runs*. It is where business requirements become configuration:

| Element | Question it answers |
|:---|:---|
| **Storage / copies** | Where does the data land — primary disk, cloud tier, tape? |
| **Retention** | How long is each copy kept? |
| **RPO / schedule** | How often do we protect it? |
| **Options** | Deduplication, encryption, throttling |

The design discipline is to build **a small number of plans that express real service levels** (gold/silver/bronze, or per-regulation), rather than a bespoke plan per application. Plan sprawl is the data-protection equivalent of the role explosion in identity: inconsistent, impossible to review, and impossible to audit.

## Retention

Retention is more subtle than "keep for 30 days," and the subtlety is exam-relevant.

- **Time-based retention** — keep for N days.
- **Cycle-based retention** — keep N *cycles*, where a cycle is a full backup plus all the incrementals that depend on it. Data is only prunable when its whole cycle is prunable, which is why deleting "old" incrementals individually does not free space.
- **Grandfather-father-son (GFS)** — daily copies kept briefly, weekly kept longer, monthly/yearly kept longest. The standard way to satisfy long-term compliance without keeping every daily forever.

**Backup retention is not archival.** Backups exist to restore a recent, working state; archives exist to retain specific data for a long time for compliance or reference. **Legal hold** overrides both: data under hold cannot be pruned regardless of policy — a rule that must be implemented, not merely intended.

## Storage tiers

Cloud object storage offers tiers that trade retrieval cost and latency against storage cost:

| Tier | Storage cost | Retrieval | Fits |
|:---|:---|:---|:---|
| **Hot / standard** | Highest | Immediate | Recent backups, likely restores |
| **Cool / infrequent** | Medium | Fast, small fee | Backups 30–90 days old |
| **Archive / deep archive** | Lowest | Hours, higher fee | Long-term compliance copies |

The trap is optimizing storage cost into a **recovery-time failure**: a copy in deep archive with a multi-hour retrieval cannot serve a 1-hour RTO, no matter how cheap it is. Tiering must be driven by the recovery objective (Chapter 05), not by the storage bill alone.

## Hands-On Lab

Python models retention and tiering. **Cost:** none.

### Lab 3.1 — Build a plan with tiered copies

**Objective:** Express a service level as a plan.

```bash
python3 - <<'EOF'
plans = {
  "Gold (tier-1 apps)":   {"rpo_hours":1,  "copies":[("primary-disk",14),("cloud-cool",90),("cloud-archive",2555)]},
  "Silver (standard)":    {"rpo_hours":24, "copies":[("primary-disk",7), ("cloud-cool",30),("cloud-archive",365)]},
  "Bronze (dev/test)":    {"rpo_hours":168,"copies":[("primary-disk",7)]},
}
for name, p in plans.items():
    print(f"\n{name}  RPO={p['rpo_hours']}h")
    for target, days in p["copies"]:
        years = days/365
        span = f"{days} days" + (f" (~{years:.0f} yr)" if years >= 1 else "")
        print(f"   copy -> {target:14} retain {span}")
print("\nThree plans express three service levels; per-application plans would be unmaintainable.")
EOF
```

**Expected result:** Three plans, each with a copy chain from fast local disk through cool cloud to long-term archive, with retention lengthening as the storage gets cheaper and slower. Gold's 2,555-day archive copy is seven years — a common regulatory retention. Building service levels rather than per-app snowflakes is what keeps the estate auditable.

**Negative test:** Giving every application its own plan — hundreds of plans with slightly different retention, no two alike, and no way to answer "what is our retention policy?" in an audit.

**Cleanup:** None.

### Lab 3.2 — Cycle-based retention and why space does not free

**Objective:** Model the dependency chain that governs pruning.

```bash
python3 - <<'EOF'
# A cycle = one FULL + the INCREMENTALs that depend on it
jobs = [
  {"id":1,"type":"FULL","cycle":1,"age_days":40},
  {"id":2,"type":"INCR","cycle":1,"age_days":39},
  {"id":3,"type":"INCR","cycle":1,"age_days":38},
  {"id":4,"type":"FULL","cycle":2,"age_days":10},
  {"id":5,"type":"INCR","cycle":2,"age_days":9},
]
RETAIN_DAYS, RETAIN_CYCLES = 30, 1
newest_cycle = max(j["cycle"] for j in jobs)
keep_cycles = set(range(newest_cycle - RETAIN_CYCLES + 1, newest_cycle + 1))

for cyc in sorted({j["cycle"] for j in jobs}):
    members = [j for j in jobs if j["cycle"] == cyc]
    all_expired = all(j["age_days"] > RETAIN_DAYS for j in members)
    prunable = all_expired and cyc not in keep_cycles
    print(f"cycle {cyc}: jobs={[j['id'] for j in members]} "
          f"all-past-{RETAIN_DAYS}d={all_expired} in-retained-cycles={cyc in keep_cycles} -> "
          f"{'PRUNABLE' if prunable else 'RETAINED'}")
print("\nA cycle prunes as a UNIT: one in-retention job holds the whole chain, so space does not free.")
EOF
```

**Expected result:** Cycle 1 is fully aged out and prunable; cycle 2 is retained. The closing line is the operational lesson people learn the hard way: you cannot reclaim space by deleting individual old incrementals, because the **cycle prunes as a unit** — a single job still within retention pins the entire chain. This is the usual explanation for "we set 30-day retention but storage keeps growing."

**Negative test:** Manually deleting backup jobs to free space — you break the dependency chain and can render the remaining jobs in that cycle unrestorable, converting a capacity problem into a data-loss problem.

**Cleanup:** None.

### Lab 3.3 — Tier for cost without breaking recovery

**Objective:** Check tiering against the recovery objective.

```bash
python3 - <<'EOF'
COST_PER_TB_MONTH = {"primary-disk":25.0, "cloud-cool":10.0, "cloud-archive":1.0}
RETRIEVAL_HOURS   = {"primary-disk":0.1,  "cloud-cool":0.5,  "cloud-archive":6.0}

def evaluate(tier, data_tb, rto_hours):
    cost = COST_PER_TB_MONTH[tier] * data_tb
    ok = RETRIEVAL_HOURS[tier] <= rto_hours
    return cost, ok

print(f"{'tier':15}{'$/month':>10}{'retrieval':>11}{'meets RTO?':>12}")
for tier in COST_PER_TB_MONTH:
    cost, ok = evaluate(tier, 50, rto_hours=1.0)
    print(f"{tier:15}{cost:>10.0f}{RETRIEVAL_HOURS[tier]:>10.1f}h{('YES' if ok else 'NO'):>12}")
print("\n50 TB with a 1-hour RTO: archive is 25x cheaper but CANNOT meet the objective (6h retrieval).")
print("Correct design: recent copies on fast tiers for RTO; archive tier only for long-term compliance copies.")
EOF
```

**Expected result:** Archive storage is dramatically cheaper — and fails the 1-hour RTO outright at six hours' retrieval. The right answer is not "pick the cheap tier" or "pick the fast tier" but to let **each copy's purpose** decide: the operational-recovery copy lives on fast storage, and the seven-year compliance copy lives in archive where its retrieval time is irrelevant.

**Negative test:** Tiering aggressively to cut the storage bill without checking RTO — the savings are real and invisible until the recovery, at which point the six-hour retrieval turns a one-hour outage into a day-long one.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Plans built as a small set of service levels rather than per-application snowflakes.
- [ ] Time-based, cycle-based, and GFS retention distinguished; cycle pruning understood.
- [ ] Backup retention separated from archival and legal hold.
- [ ] Storage tiering validated against the recovery-time objective, not just cost.
