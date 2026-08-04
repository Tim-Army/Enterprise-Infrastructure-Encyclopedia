# Chapter 03: Immutability and Air-Gap

## Learning Objectives

- Cover Rubrik's cyber-resilience foundation: immutable, logically air-gapped backups.
- Understand why immutability defeats ransomware's attack on backups.
- Model an append-only, immutable backup store and prove it resists tampering.

## Why the backup must be immutable

Modern ransomware doesn't just encrypt production — it **hunts and destroys the backups first**, so you have no choice but to pay. The counter is **immutability**: once written, a backup **cannot be modified or deleted** (by anyone — including an admin whose credentials the attacker stole) until its retention expires. Rubrik's architecture is immutable by design (append-only file system, no direct data access), with a **logical air-gap** (the data plane isn't openly reachable/writable from production).

| Property | Effect |
|:---|:---|
| **Immutable (append-only)** | Existing snapshots can't be encrypted, altered, or deleted |
| **Logical air-gap** | Backups aren't mounted/writable from the production network an attacker controls |
| **Retention lock** | Not even an administrator can shorten retention or delete early |
| **No open protocols to the data** | No CIFS/NFS share of the backup an attacker can reach and encrypt |

## Hands-On Lab

Python models an immutable store. **Cost:** none.

### Lab 3.1 — An append-only immutable backup store

**Objective:** Build a store where snapshots can be added but never altered or deleted before expiry.

```bash
python3 - <<'EOF'
import hashlib, datetime
class ImmutableStore:
    def __init__(self):
        self.snaps = {}   # id -> {data_hash, created, retain_until, locked}
    def write(self, snap_id, data, retain_days):
        if snap_id in self.snaps:
            return f"REJECT: {snap_id} already exists (append-only — cannot overwrite)"
        self.snaps[snap_id] = {
            "hash": hashlib.sha256(data).hexdigest()[:12],
            "created": datetime.date(2026,8,4),
            "retain_until": datetime.date(2026,8,4) + datetime.timedelta(days=retain_days),
            "locked": True,
        }
        return f"WROTE {snap_id} (immutable until {self.snaps[snap_id]['retain_until']})"
    def delete(self, snap_id, today=datetime.date(2026,8,4)):
        s = self.snaps.get(snap_id)
        if not s: return f"{snap_id}: not found"
        if s["locked"] and today < s["retain_until"]:
            return f"DENY delete {snap_id}: retention-locked until {s['retain_until']} (even for admins)"
        del self.snaps[snap_id]; return f"deleted {snap_id} (retention expired)"
    def modify(self, snap_id, data):
        return f"DENY modify {snap_id}: snapshots are append-only/immutable"

store = ImmutableStore()
print(store.write("db-prod@0800", b"snapshot-1", retain_days=30))
print(store.write("db-prod@0800", b"tampered",   retain_days=30))   # cannot overwrite
print(store.modify("db-prod@0800", b"ransomware-encrypted"))         # cannot modify
print(store.delete("db-prod@0800"))                                  # cannot delete early
EOF
```

**Expected result:**

```text
WROTE db-prod@0800 (immutable until 2026-09-03)
REJECT: db-prod@0800 already exists (append-only — cannot overwrite)
DENY modify db-prod@0800: snapshots are append-only/immutable
DENY delete db-prod@0800: retention-locked until 2026-09-03 (even for admins)
```

The snapshot can be written once and then **cannot be overwritten, modified, or deleted** before retention expires — the immutability property. Ransomware (or a malicious admin with stolen credentials) that reaches this store can *add* data but cannot *destroy* what's there, so a clean recovery point always survives. This is the foundation of Rubrik's cyber resilience.

**Negative test:** A traditional backup on a writable CIFS share — ransomware mounts it and encrypts every backup file; the immutable, no-open-protocol store is exactly what removes that attack path.

**Cleanup:** None.

### Lab 3.2 — The logical air-gap

**Objective:** Model why the backup data isn't reachable from the compromised production network.

```bash
python3 - <<'EOF'
# Logical air-gap: production can request backup/restore via API, but cannot directly read/write the data
def access_backup_data(actor, via):
    if via == "direct-mount-from-production":
        return f"DENY {actor}: backup data is not mounted/writable from production (logical air-gap)"
    if via == "authenticated-api-restore":
        return f"ALLOW {actor}: orchestrated restore via API (read-only pull to a clean target)"
    return "DENY (unknown access path)"
print(access_backup_data("ransomware on prod host", "direct-mount-from-production"))
print(access_backup_data("recovery admin (MFA)", "authenticated-api-restore"))
EOF
```

**Expected result:** Ransomware on a production host cannot directly reach/encrypt the backup data (no mount, logical air-gap); a recovery is an **orchestrated, authenticated API operation** that pulls known-clean data to a clean target. The air-gap means the blast radius of a production compromise stops at production — the recovery data is out of reach.

**Negative test:** A backup server joined to the same domain with an open SMB share — one compromised domain admin reaches and destroys it; the logical air-gap (no direct data access, separate auth) is what breaks that chain.

**Cleanup:** None.

### Lab 3.3 — The 3-2-1-1-0 rule (immutability's context)

**Objective:** Place immutability in the modern backup-rule framing.

```bash
cat <<'EOF'
Modern resilient backup: 3-2-1-1-0
  3 copies of data
  2 different media
  1 offsite
  1 IMMUTABLE / air-gapped (the ransomware-era addition)
  0 errors (verified/tested recoverability — see Ch 06)
Rubrik centers the "1 immutable" and "0 errors": immutable snapshots + recovery validation.
EOF
```

**Expected result:** The 3-2-1-1-0 rule, with the modern additions of **1 immutable copy** and **0 recovery errors** — the framing that positions immutability (this chapter) and recovery validation ([Chapter 06](06-recovery-orchestration.md)) as the ransomware-era essentials. Rubrik's platform is built around exactly these two.

**Negative test:** Classic 3-2-1 without the immutable copy — ransomware that reaches any writable copy compromises the whole set; the immutable "1" is what guarantees a survivable recovery point.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Immutability (append-only, retention-locked, no early delete) built and proven.
- [ ] The logical air-gap (no direct data access from production) modeled.
- [ ] The 3-2-1-1-0 rule and where immutability fits internalized.
