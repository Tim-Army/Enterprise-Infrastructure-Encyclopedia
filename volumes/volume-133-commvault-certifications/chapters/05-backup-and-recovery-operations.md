# Chapter 05: Backup and Recovery Operations

## Learning Objectives

- Schedule backups against RPO, and size them against the backup window.
- Distinguish full, incremental, differential, and synthetic full backups.
- Manage auxiliary and secondary copies for the 3-2-1 rule.
- Verify recoverability rather than assuming it.

## RPO, RTO, and what they actually cost

Two objectives drive every design decision in this chapter:

| Objective | Definition | Determined by |
|:---|:---|:---|
| **RPO** (Recovery Point Objective) | How much data you can afford to lose | **Backup frequency** |
| **RTO** (Recovery Time Objective) | How long you can afford to be down | **Recovery speed**, which depends on storage tier, copy location, and rehearsal |

A one-hour RPO requires hourly protection; there is no way to configure a nightly backup into an hourly recovery point. Conversely, a one-hour RTO cannot be met by data sitting in an archive tier with six-hour retrieval (Chapter 03). These objectives should come from the business, cost real money, and are the first thing to pin down.

## Backup types

| Type | What it copies | Restore cost |
|:---|:---|:---|
| **Full** | Everything | Fastest — one job to read |
| **Incremental** | Changes since the *last backup of any type* | Slowest — full plus every subsequent incremental |
| **Differential** | Changes since the last *full* | Moderate — full plus one differential |
| **Synthetic full** | A new full **assembled from existing backup data**, not re-read from the client | Fast restore, **no client impact** |

The **synthetic full** is the one worth understanding properly. It manufactures a fresh full backup on the MediaAgent by combining the previous full with subsequent incrementals — so you get a full's restore performance without ever re-reading the production system. Combined with deduplication (Chapter 04), it is why "incremental forever plus synthetic fulls" is the standard modern pattern: minimal production impact, fast restores, minimal storage.

## Auxiliary copies and 3-2-1

An **auxiliary copy** duplicates a backup to another location or medium. This is how the **3-2-1 rule** gets implemented:

> **3** copies of the data, on **2** different media types, with **1** off-site.

Modern practice extends it to **3-2-1-1-0**: one copy **immutable or air-gapped** (Chapter 06), and **zero** errors on verification. The final digit is the one organizations skip, and it is the one that matters.

## Verification: the discipline that separates real protection from theater

A backup that has never been restored is a hypothesis, not a recovery capability. Verification comes in escalating strength:

1. **Job success** — the job reported completion. Weakest; means data was written.
2. **Data verification** — read back the blocks and check integrity/hashes.
3. **Synthetic full completion** — proves the chain can be assembled.
4. **Actual test restore** — restore to an alternate location and open the data.
5. **Full recovery rehearsal** — restore the application and confirm it *works* (Chapter 07's cleanroom).

Only levels 4 and 5 prove recoverability. Most organizations stop at 1.

## Hands-On Lab

Python models the operations. **Cost:** none.

### Lab 5.1 — Schedule against RPO and the backup window

**Objective:** Check that a schedule can meet its objective.

```bash
python3 - <<'EOF'
def evaluate(name, rpo_hours, schedule_hours, data_tb, throughput_tb_per_hour, window_hours):
    rpo_ok = schedule_hours <= rpo_hours
    duration = data_tb / throughput_tb_per_hour
    window_ok = duration <= window_hours
    print(f"{name}")
    print(f"   RPO {rpo_hours}h vs backup every {schedule_hours}h -> {'MEETS RPO' if rpo_ok else 'FAILS RPO'}")
    print(f"   {data_tb} TB at {throughput_tb_per_hour} TB/h = {duration:.1f}h vs {window_hours}h window -> "
          f"{'FITS' if window_ok else 'OVERRUNS WINDOW'}")
    if not rpo_ok:    print("      fix: increase frequency (more incrementals, or CDP/log backups)")
    if not window_ok: print("      fix: incremental-forever + synthetic fulls, more streams, or a closer MediaAgent")

evaluate("Tier-1 database", rpo_hours=1,  schedule_hours=24, data_tb=8,  throughput_tb_per_hour=2, window_hours=8)
print()
evaluate("File server",     rpo_hours=24, schedule_hours=24, data_tb=30, throughput_tb_per_hour=2, window_hours=8)
print()
evaluate("Dev/test",        rpo_hours=168,schedule_hours=168,data_tb=2,  throughput_tb_per_hour=2, window_hours=8)
EOF
```

**Expected result:** The tier-1 database **fails its RPO** (nightly backups cannot deliver a one-hour recovery point — it needs frequent log backups), the file server meets RPO but **overruns the window** at 15 hours against 8, and dev/test is fine. These are two genuinely different failures with different fixes: RPO failures are solved by *frequency*, window failures by *efficiency*. Conflating them leads to the useless remedy of running the same slow full backup more often.

**Negative test:** Reporting "backups are green" for the tier-1 database — every job succeeds, and the organization still loses up to 24 hours of transactions, because the schedule was never capable of the stated RPO.

**Cleanup:** None.

### Lab 5.2 — Backup types and restore chains

**Objective:** Compare restore cost across strategies.

```bash
python3 - <<'EOF'
def restore_chain(strategy, days_since_full):
    if strategy == "full-daily":
        return ["FULL (today)"], "fastest restore, heaviest production impact + storage"
    if strategy == "full-weekly + incremental":
        return ["FULL (day 0)"] + [f"INCR (day {d})" for d in range(1, days_since_full+1)], \
               "light backups, but restore reads the full plus EVERY incremental"
    if strategy == "full-weekly + differential":
        return ["FULL (day 0)", f"DIFF (day {days_since_full})"], \
               "restore reads only full + one differential"
    if strategy == "incremental-forever + synthetic full":
        return ["SYNTHETIC FULL (assembled on the MediaAgent)"], \
               "fast restore AND no client impact — the modern default"

for s in ["full-daily","full-weekly + incremental","full-weekly + differential","incremental-forever + synthetic full"]:
    chain, note = restore_chain(s, days_since_full=6)
    print(f"\n{s}")
    print(f"   restore reads {len(chain)} job(s): {chain if len(chain)<=3 else chain[:2]+['...']+chain[-1:]}")
    print(f"   {note}")
EOF
```

**Expected result:** Daily fulls restore from one job but hammer production; weekly-plus-incremental restores read seven jobs; differentials read two; and **incremental-forever plus synthetic fulls restores from a single job with no client impact at all**. That last row is why the pattern dominates modern deployments — the synthetic full is assembled from data already on the MediaAgent, so you stop trading restore speed against production load.

**Negative test:** Long incremental chains with no synthetic fulls — restore time grows with every day since the last full, and a single corrupt link in the chain can break the restore entirely.

**Cleanup:** None.

### Lab 5.3 — Verify recoverability, not just job success

**Objective:** Score protection against the verification ladder.

```bash
python3 - <<'EOF'
LEVELS = {
  1:"job success only            (data was written)",
  2:"data verification           (blocks read back and checksummed)",
  3:"synthetic full completes    (chain assembles)",
  4:"test restore to alt location(data opens)",
  5:"full recovery rehearsal     (application works)",
}
systems = [
  {"name":"tier-1 ERP",   "highest_level":1},
  {"name":"file server",  "highest_level":2},
  {"name":"SQL cluster",  "highest_level":4},
  {"name":"domain controllers","highest_level":5},
]
for s in systems:
    lvl = s["highest_level"]
    proven = "RECOVERABILITY PROVEN" if lvl >= 4 else "NOT PROVEN — recovery is an assumption"
    print(f"{s['name']:22} level {lvl}: {LEVELS[lvl]}")
    print(f"{'':22} -> {proven}")
print("\nOnly levels 4-5 prove you can recover. 'All jobs green' is level 1.")
EOF
```

**Expected result:** The tier-1 ERP — the most important system listed — has the **weakest** verification, proven only to level 1, while the domain controllers are rehearsed to level 5. The inversion is realistic and is the point: verification effort tends to follow whoever is enthusiastic rather than business criticality. The ladder makes "are we actually protected?" an answerable question instead of a matter of confidence.

**Negative test:** Equating a green dashboard with recoverability — job success proves bytes were written, not that they can be read back, assembled, or used to run the application.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] RPO and RTO distinguished, with frequency and recovery speed as their respective levers.
- [ ] Full, incremental, differential, and synthetic full compared by restore chain.
- [ ] Auxiliary copies mapped onto 3-2-1 (and 3-2-1-1-0).
- [ ] Recoverability verified up the ladder, not assumed from job success.
