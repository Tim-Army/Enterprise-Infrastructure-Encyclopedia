# Chapter 05: Data Protection and Replication

## Learning Objectives

- Distinguish local snapshots/clones from remote replication.
- Describe Hitachi replication — ShadowImage, Thin Image, TrueCopy, and Universal Replicator.
- Explain synchronous versus asynchronous replication and RPO/RTO.
- Understand data protection's role in business continuity and disaster recovery.

*Cert relevance: this is the Data Protection & Replication track.*

## Local versus remote

Protecting data on a VSP happens at two distances:

- **Local protection** — copies **within the same array/site** for fast recovery from logical errors (a bad change, accidental deletion) or to create test/dev copies: **snapshots** (point-in-time, space-efficient) and **clones** (full copies).
- **Remote replication** — copies to a **second array at another site** so data survives a **site disaster** (fire, flood, outage). This is the foundation of **disaster recovery (DR)**.

Both matter: local copies give fast, frequent recovery points; remote replication gives geographic resilience. A complete protection strategy uses both. Knowing which technology serves which distance is core. The lab creates a local snapshot and a remote replica.

## Hitachi replication technologies

Hitachi has named technologies for each protection type:

- **ShadowImage** — **local clones** (full in-array copies) for backup, test/dev, and fast local recovery.
- **Thin Image** — **local snapshots** (space-efficient point-in-time copies) — many frequent recovery points without full-copy overhead.
- **TrueCopy** — **synchronous remote replication** — every write is committed to **both** the local and remote array before acknowledging, so the remote is **always identical** (zero data loss).
- **Universal Replicator** — **asynchronous remote replication** — writes replicate to the remote array with a small lag, so it works over **long distances** without slowing the application.

Knowing the technology names and what each does — local clone vs snapshot, synchronous vs asynchronous remote — is exactly the kind of knowledge the Data Protection track tests. The lab uses each type.

## Synchronous versus asynchronous

The crucial replication trade-off is **synchronous vs asynchronous**, governed by two metrics:

- **RPO (Recovery Point Objective)** — how much data you can afford to **lose** (measured in time). Synchronous replication (TrueCopy) gives **RPO = 0** (no loss) but requires low latency, so **limited distance**. Asynchronous (Universal Replicator) has a **small RPO** (seconds/minutes of possible loss) but works over **any distance**.
- **RTO (Recovery Time Objective)** — how quickly you must **recover** and resume operations after a failure.

The choice balances **data-loss tolerance, distance, and application performance**: synchronous for zero-loss over metro distances; asynchronous for long-distance DR where a tiny RPO is acceptable. Designing replication to meet the business's RPO/RTO is the heart of DR planning. The lab compares synchronous and asynchronous by RPO and distance.

## Business continuity and DR

Data protection exists to serve **business continuity** — keeping the business running through failures:

- **Local snapshots** recover from **operational** errors quickly (restore to a point in time before the mistake).
- **Remote replication** provides a **DR site** that can take over if the primary site is lost — **failover** to the replica, run there, and **fail back** when the primary recovers.
- **Testing** — a DR plan is only real if **tested**; you validate failover works without waiting for a real disaster.

Storage-based protection is a pillar of enterprise resilience, complementing backup software and application-level protection. Understanding how snapshots and replication map to **recovery scenarios** — and to RPO/RTO — is what the certification validates. The lab models a DR failover. *(This complements dedicated data-protection platforms like [Rubrik CXXX](../../volume-130-rubrik-certifications/README.md) and [Commvault CXXXIII](../../volume-133-commvault-certifications/README.md).)*

## Hands-On Lab

Python models local snapshots, remote replication (sync/async), RPO/RTO, and DR failover. **Cost:** none.

### Lab 5.1 — Protect data locally and remotely

**Objective:** Take a local snapshot, replicate remotely (sync and async), compare RPO, and fail over.

```bash
python3 - <<'EOF'
import time
# a volume with data; protect it locally (Thin Image snapshot) and remotely (TrueCopy / Universal Replicator)
primary = {"vol":"db-vol","data":"v100","site":"A"}

# LOCAL: Thin Image snapshot (point-in-time, for fast recovery from logical errors)
snapshot = dict(primary); snapshot["type"]="Thin Image snapshot (local, point-in-time)"
print("LOCAL PROTECTION:")
print(f"   {snapshot['type']}: recover '{primary['vol']}' to this point after a bad change")

# REMOTE: synchronous (TrueCopy, RPO=0) vs asynchronous (Universal Replicator, small RPO)
def replicate(mode):
    if mode=="sync":  return {"tech":"TrueCopy","rpo":"0 (zero data loss)","distance":"metro (low latency required)","perf":"write waits for remote ack"}
    else:             return {"tech":"Universal Replicator","rpo":"~seconds-minutes","distance":"any (long distance OK)","perf":"no app impact (async)"}
print("\nREMOTE REPLICATION (to site B):")
for mode in ("sync","async"):
    r = replicate(mode); print(f"   {mode:5}: {r['tech']:20} RPO={r['rpo']:20} distance={r['distance']:28} {r['perf']}")

# DR failover: primary site A lost -> fail over to remote replica at site B
print("\nDR FAILOVER:")
print("   site A lost -> promote replica at site B -> applications resume on B (failover)")
print("   site A recovered -> resync + fail back to A")
print()
print("LOCAL snapshots (Thin Image) recover fast from logical errors; CLONES (ShadowImage) make")
print("full copies. REMOTE replication protects against site disaster: TrueCopy SYNC = RPO 0 but")
print("metro distance only; Universal Replicator ASYNC = tiny RPO over ANY distance with no app")
print("impact. Choose by RPO/RTO + distance. Failover to the DR site, fail back after — business continuity.")
EOF
```

**Expected result:** A local Thin Image snapshot for point-in-time recovery, remote replication compared as synchronous (TrueCopy, RPO 0, metro distance) versus asynchronous (Universal Replicator, small RPO, any distance), and a DR failover/failback. The lesson is Hitachi data protection: local snapshots/clones (Thin Image/ShadowImage) for fast operational recovery, and remote replication (TrueCopy sync for zero loss, Universal Replicator async for distance) for disaster recovery, chosen by RPO/RTO and distance.

**Negative test:** Relying only on local snapshots and no remote replication. A site disaster destroys the array and every local snapshot with it; remote replication to a second site is what survives losing the primary site — local protection alone is not disaster recovery.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Local vs remote protection understood — snapshots/clones for operational recovery, replication for DR.
- [ ] Hitachi technologies understood — ShadowImage, Thin Image, TrueCopy, Universal Replicator.
- [ ] Sync vs async understood — RPO/RTO, zero-loss metro (sync) vs long-distance small-RPO (async).
- [ ] Business continuity understood — snapshots for errors, replication for site failover/failback, and testing.

## See also

- [Chapter 03 — Block Storage Administration](03-block-storage-administration.md) — the volumes being protected.
- [Chapter 06 — Hitachi Ops Center](06-hitachi-ops-center.md) — Ops Center Protection automates replication.
- [Volume CXXX — Rubrik](../../volume-130-rubrik-certifications/README.md) and [Volume CXXXIII — Commvault](../../volume-133-commvault-certifications/README.md) — data-protection software peers.
