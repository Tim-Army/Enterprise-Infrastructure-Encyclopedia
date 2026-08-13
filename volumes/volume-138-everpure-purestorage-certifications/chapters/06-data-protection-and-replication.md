# Chapter 06: Data Protection and Replication

## Learning Objectives

- Use snapshots for local recovery and understand what they do not protect against.
- Compare asynchronous and synchronous replication by RPO and distance.
- Describe active/active clustering for continuous availability.
- Design a topology that meets stated RPO and RTO targets.

## Snapshots are not backups

A snapshot is a point-in-time image on the **same array**, near-instant and space-efficient because it stores only changed blocks. Snapshots are excellent for the common recovery case — a deleted file, a failed upgrade, a bad deployment — and they are not backups, because:

- They live on the array they protect. Lose the array and you lose them.
- They share its fate in a site event, a firmware fault, or an administrator error affecting the array.
- Unless made **immutable** (Chapter 07), an attacker with array credentials can delete them.

The relationship is complementary: snapshots give fast recovery from common problems; replication gives survival of the array; immutable copies give survival of an attacker.

## Replication

| Mode | How it works | RPO | Distance |
|:---|:---|:---|:---|
| **Asynchronous** | Periodic snapshot-based replication to a target array | Minutes to hours — whatever the interval is | Effectively unlimited |
| **Synchronous** | Every write is acknowledged only when both arrays have it | **Zero** | Limited by latency — typically metropolitan |
| **Active/active** | Both arrays serve the same volumes simultaneously | Zero, with transparent failover | Metropolitan |

The physics that constrains synchronous replication is worth stating explicitly: light in fibre travels roughly 200 km per millisecond, so a 100 km round trip adds about **1 ms** to every single write before any equipment overhead. At 300 km that becomes ~3 ms, which many latency-sensitive databases will not tolerate. **Synchronous replication is a metropolitan technology**, and no amount of tuning changes the speed of light.

## Active/active

Everpure's **ActiveCluster** presents the same volume from two arrays simultaneously, both serving I/O, with automatic transparent failover. The requirement most people miss is the **mediator/witness** — a third site or cloud service that decides which array survives a link failure. Without it, both arrays might assume the other has failed and continue serving independently — **split brain**, which corrupts data in a way that is painful to unpick.

## Hands-On Lab

Python models replication design. **Cost:** none.

### Lab 6.1 — RPO from replication interval

**Objective:** Compute worst-case data loss and check it against the target.

```bash
python3 - <<'EOF'
def rpo(mode, interval_min=None):
    if mode == "sync":  return 0, "every write acknowledged at BOTH arrays before the host sees success"
    return interval_min, f"worst case = the full interval ({interval_min} min) since the last replication"

configs = [
  {"app":"payments",    "mode":"sync",  "interval":None, "target_rpo":0},
  {"app":"CRM",         "mode":"async", "interval":15,   "target_rpo":30},
  {"app":"reporting",   "mode":"async", "interval":240,  "target_rpo":60},
  {"app":"file share",  "mode":"async", "interval":60,   "target_rpo":60},
]
for c in configs:
    actual, why = rpo(c["mode"], c["interval"])
    ok = actual <= c["target_rpo"]
    print(f"{c['app']:12} {c['mode']:6} -> RPO {actual:>4} min vs target {c['target_rpo']:>3} min  "
          f"{'MET' if ok else '*** BREACHED ***'}")
    print(f"{'':12} {why}")
    if not ok:
        need = c["target_rpo"]
        print(f"{'':12} FIX: replicate at least every {need} min, or move to synchronous")
    print()
print("RPO is set by the replication INTERVAL, not by intent. A 4-hour interval cannot")
print("deliver a 1-hour RPO no matter what the service catalogue claims.")
EOF
```

**Expected result:** Payments and CRM meet their targets, the file share exactly meets its 60-minute target, and reporting **breaches** — a four-hour interval against a one-hour RPO. The closing line is the discipline: RPO is an arithmetic consequence of configuration, so a documented target that the schedule cannot deliver is a fiction that will only be discovered during a recovery.

**Negative test:** Publishing RPO targets in a service catalogue without verifying the replication schedules behind them — the numbers are aspirational and the gap surfaces at the worst possible moment.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Distance limits synchronous replication

**Objective:** Compute the latency the speed of light imposes.

```bash
python3 - <<'EOF'
LIGHT_KM_PER_MS = 200          # ~speed of light in fibre
def sync_penalty(distance_km, equipment_ms=0.3):
    round_trip = (distance_km * 2) / LIGHT_KM_PER_MS
    return round_trip + equipment_ms

print(f"{'distance':>10}{'added write latency':>22}   verdict")
for km in (10, 50, 100, 300, 1000, 5000):
    lat = sync_penalty(km)
    if lat <= 1.0:    v = "fine for synchronous"
    elif lat <= 3.0:  v = "acceptable for many workloads; test latency-sensitive databases"
    elif lat <= 10.0: v = "painful — most transactional databases will suffer"
    else:             v = "IMPOSSIBLE for synchronous — use asynchronous"
    print(f"{km:>8} km{lat:>19.2f} ms   {v}")
print("\nEvery synchronous write waits for the far array to acknowledge. At 5000 km that is 50 ms")
print("added to EVERY write — a database doing 1000 writes/sec would be crippled.")
print("\nThis is physics, not a product limitation: synchronous replication is METROPOLITAN,")
print("and cross-continent protection is asynchronous by necessity.")
EOF
```

**Expected result:** Latency climbs from 0.4 ms at 10 km to 50.3 ms at 5,000 km, crossing from comfortable to impossible. Framing it as physics rather than a product constraint is the useful part — candidates sometimes look for a configuration that gives zero-RPO protection at continental distance, and no such configuration exists.

**Negative test:** Specifying synchronous replication between continents for regulatory zero-RPO — the requirement cannot be met as stated, and the honest response is to renegotiate the requirement or accept asynchronous with a short interval.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Active/active and the split-brain mediator

**Objective:** Show why a witness is mandatory.

```bash
python3 - <<'EOF'
def cluster_behavior(link_up, mediator_present, mediator_reachable_from):
    if link_up:
        return "NORMAL — both arrays serve the same volumes; hosts use whichever is closer"
    if not mediator_present:
        return ("*** SPLIT BRAIN *** link down and NO mediator: each array assumes the other failed "
                "and keeps serving. Two divergent copies of the same volume — data corruption that is "
                "extremely painful to reconcile")
    winner = mediator_reachable_from
    loser = "B" if winner == "A" else "A"
    return (f"SAFE — mediator arbitrates: array {winner} keeps serving, array {loser} stops. "
            "One surviving copy, hosts fail over transparently")

print("link UP,   mediator yes ->", cluster_behavior(True,  True,  "A"), "\n")
print("link DOWN, mediator NO  ->", cluster_behavior(False, False, None), "\n")
print("link DOWN, mediator yes ->", cluster_behavior(False, True,  "A"), "\n")
print("The mediator/witness is a THIRD site (or cloud service) — it must be independent of both")
print("arrays, or it fails with the thing it is meant to arbitrate.")
print("Active/active without a mediator is not a resilience design; it is a corruption waiting")
print("for a fibre cut.")
EOF
```

**Expected result:** Normal operation and mediated failover are safe; a link failure without a mediator produces **split brain**. The requirement that the witness live at a *third*, independent location is the detail that gets compromised in practice — placing it at one of the two sites means it dies with that site and cannot arbitrate the case it exists for.

**Negative test:** Hosting the mediator on a VM in one of the two data centers — losing that site takes the mediator with it, and the surviving array has nothing to confirm it should take over.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Snapshots understood as fast local recovery, not as backups.
- [ ] Asynchronous and synchronous replication compared by RPO and distance.
- [ ] Synchronous replication's metropolitan limit derived from the speed of light.
- [ ] Active/active designed with an independent third-site mediator to prevent split brain.
