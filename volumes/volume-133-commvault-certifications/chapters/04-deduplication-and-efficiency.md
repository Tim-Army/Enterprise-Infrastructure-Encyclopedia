# Chapter 04: Deduplication and Storage Efficiency

## Learning Objectives

- Explain block-level deduplication and the deduplication database (DDB).
- Calculate deduplication ratios and the storage they save.
- Size and protect the DDB, and know when to seal it.
- Combine deduplication with compression and encryption in the correct order.

## How deduplication works

Deduplication stores each unique block **once**, replacing repeats with references. Because backup data is enormously repetitive — the same operating system files on 500 servers, the same document backed up nightly for a year — the savings are large in a way that is hard to intuit.

The mechanism:

1. Data is divided into **blocks** (a configurable block size).
2. Each block is **hashed** into a signature.
3. The signature is looked up in the **deduplication database (DDB)**.
4. **Hit** → store only a reference. **Miss** → store the block and record its signature.

The DDB is therefore the index that makes the whole scheme work, and it lives on the MediaAgent (Chapter 02).

## Where deduplication happens

| Mode | Hashing occurs | Trade-off |
|:---|:---|:---|
| **Client-side (source)** | On the protected client | Sends far less data over the network; costs client CPU |
| **MediaAgent-side (target)** | On the MediaAgent | No client CPU cost; sends full data over the network |

Client-side deduplication is the answer to the Branch-A problem from Chapter 02: if the network is the constraint, deduplicate before the wire, not after it.

## The DDB is critical infrastructure

Two properties make DDB care a real operational discipline:

- **Performance:** every block hashes into a lookup, so the DDB is I/O-intensive and belongs on **fast, low-latency storage** (SSD). A slow DDB throttles the entire backup.
- **Criticality:** if the DDB is lost, the *references* cannot be resolved. Commvault protects the DDB and can reconstruct it, but the recovery is expensive — so the DDB is backed up and monitored, not treated as a scratch index.

**Sealing** the DDB starts a fresh one, deliberately giving up deduplication against older data. It is done when the DDB grows past its efficient size, becomes corrupted, or when a retention boundary makes a clean break useful. The cost is a temporary drop in dedup efficiency as the new DDB fills with baseline blocks.

## Order of operations

The order is not arbitrary, and getting it wrong destroys the savings:

**Deduplicate → compress → encrypt.**

Encrypted data is, by design, statistically random: identical plaintext blocks encrypt to different ciphertext (with proper unique initialization), so **deduplication after encryption finds no duplicates**. Compression likewise reduces the block-level similarity dedup depends on. Deduplicate first, always.

## Hands-On Lab

Python models deduplication. **Cost:** none.

### Lab 4.1 — Block-level deduplication and the DDB

**Objective:** Build the signature-lookup mechanism.

```bash
python3 - <<'EOF'
import hashlib
ddb = {}                       # signature -> stored block id
stored_blocks, total_blocks = 0, 0

def backup(name, blocks):
    global stored_blocks, total_blocks
    new, refs = 0, 0
    for b in blocks:
        total_blocks += 1
        sig = hashlib.sha256(b.encode()).hexdigest()[:12]
        if sig in ddb:
            refs += 1                      # HIT: store only a reference
        else:
            ddb[sig] = f"blk{len(ddb):04d}"  # MISS: store the block
            stored_blocks += 1; new += 1
    print(f"{name:22} blocks={len(blocks):3}  new={new:3}  deduped={refs:3}")

os_files   = ["kernel","libc","systemd","bash","openssl"]
app_files  = ["app-bin","app-cfg"]
backup("server-01 (full)",      os_files + app_files)
backup("server-02 (full)",      os_files + ["app-bin","other-app"])   # same OS
backup("server-03 (full)",      os_files + ["third-app"])            # same OS again
backup("server-01 (next day)",  os_files + app_files)               # unchanged

ratio = total_blocks / stored_blocks
print(f"\nlogical blocks={total_blocks}  stored={stored_blocks}  dedup ratio={ratio:.1f}:1")
print(f"space saved: {(1 - stored_blocks/total_blocks)*100:.0f}%")
EOF
```

**Expected result:** 26 logical blocks reduce to 9 stored — roughly a **2.9:1 ratio, about 65% saved** — because the five OS blocks are stored once and referenced by every server, and the unchanged next-day backup stores nothing new. That last case is the important one: repeated backups of unchanged data cost essentially zero, which is why daily full backups become affordable under deduplication.

**Negative test:** Deduplicating within a single client only, rather than globally across the MediaAgent — you lose exactly the cross-server OS savings that produce most of the ratio.

**Cleanup:** None.

### Lab 4.2 — Order of operations: dedup before encryption

**Objective:** Show why encryption-first destroys deduplication.

```bash
python3 - <<'EOF'
import hashlib, os
blocks = ["kernel","libc","kernel","libc","kernel"]   # highly repetitive

def sig(data): return hashlib.sha256(data).hexdigest()[:10]

# CORRECT: dedup on plaintext, then encrypt what you store
plain_sigs = {sig(b.encode()) for b in blocks}
print(f"dedup THEN encrypt: {len(blocks)} blocks -> {len(plain_sigs)} unique stored")

# WRONG: encrypt first (unique IV per block), then try to dedup
enc_sigs = {sig(b.encode() + os.urandom(8)) for b in blocks}   # IV makes each ciphertext unique
print(f"encrypt THEN dedup: {len(blocks)} blocks -> {len(enc_sigs)} unique stored  <-- NO savings")
print("\nProperly encrypted data is indistinguishable from random: identical plaintext yields")
print("different ciphertext, so no duplicates are ever found. Always dedup -> compress -> encrypt.")
EOF
```

**Expected result:** Deduplicating first reduces five blocks to two; encrypting first leaves all five, because each ciphertext is unique. The savings do not degrade gracefully — they vanish entirely. This ordering is a standard exam point and a real configuration mistake with a large, quiet cost.

**Negative test:** Enabling client-side encryption before deduplication to "be secure by default" — you get the same security posture and lose the entire deduplication benefit, potentially multiplying the storage bill several-fold.

**Cleanup:** None.

### Lab 4.3 — Size the DDB and decide when to seal

**Objective:** Apply the DDB operational rules.

```bash
python3 - <<'EOF'
def ddb_health(unique_blocks_millions, storage_type, corrupted, growth_pct_per_month):
    notes = []
    if storage_type != "SSD":
        notes.append("MOVE TO SSD — DDB lookups are I/O-bound; slow media throttles every backup")
    if corrupted:
        notes.append("SEAL — corruption; start a fresh DDB and let the old one age out with its data")
    elif unique_blocks_millions > 750:
        notes.append("SEAL — DDB past its efficient size; expect a temporary dedup dip as the new one baselines")
    if growth_pct_per_month > 25:
        notes.append("INVESTIGATE growth — new workloads, changed block size, or encryption before dedup")
    return notes or ["healthy"]

cases = [
  ("DDB-01", 200, "SSD",  False, 8),
  ("DDB-02", 900, "SSD",  False, 10),
  ("DDB-03", 150, "HDD",  False, 40),
  ("DDB-04", 300, "SSD",  True,  5),
]
for name, blocks, media, corrupt, growth in cases:
    print(f"{name}: {blocks}M blocks on {media}, growth {growth}%/mo")
    for n in ddb_health(blocks, media, corrupt, growth):
        print(f"    - {n}")
EOF
```

**Expected result:** Each DDB gets a specific verdict — move to SSD, seal for size, seal for corruption, or investigate abnormal growth. The growth check is the diagnostic worth remembering: a DDB growing 40% a month usually means something upstream changed, and "encryption enabled before deduplication" (Lab 4.2) is a leading cause.

**Negative test:** Sealing the DDB routinely "to keep it tidy" — every seal discards deduplication against all prior data, so the next backups store full baselines again and storage jumps.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Block-level deduplication and the DDB signature lookup modeled.
- [ ] Client-side vs MediaAgent-side deduplication matched to the network constraint.
- [ ] The dedup → compress → encrypt ordering justified and its failure demonstrated.
- [ ] DDB sizing, placement on fast storage, and sealing criteria applied.
