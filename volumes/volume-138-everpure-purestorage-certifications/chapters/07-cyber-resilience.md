# Chapter 07: Cyber Resilience

## Learning Objectives

- Explain why storage-enforced immutability is the control that survives a compromised administrator.
- Configure retention locks so snapshots cannot be deleted early.
- Plan and rehearse a clean recovery from a ransomware incident.
- Describe the eradication window and how it constrains retention.

## Storage is the last line

The **Cyber Resilience** Professional certification exists because ransomware changed what storage is for. An attacker who encrypts production and leaves the snapshots intact has not won; an attacker who **deletes the snapshots first** has removed the alternative to paying. Modern attacks therefore target the storage platform's own protection.

This reframes the requirement. The question is no longer "can we restore from yesterday?" but **"can we restore from yesterday when the attacker had our storage administrator's credentials?"**

## Storage-enforced immutability

The answer is immutability enforced **by the array**, not by policy. Everpure's mechanism (branded **SafeMode**) applies **retention locks** to snapshots such that they cannot be deleted or shortened before their retention expires — **not by an administrator, and not by anyone holding array credentials**. Changing the policy requires an out-of-band process involving the vendor, deliberately introducing friction and a second party.

That friction is the feature. A control an attacker can disable with the credentials they already stole is not a control, which is the same principle behind the storage-layer object lock in [Volume CXXXIII, Chapter 06](../../volume-133-commvault-certifications/chapters/06-cyber-resilience-immutability-threat-scan.md).

| Control | Stops |
|:---|:---|
| **Snapshot retention lock** | Deletion or early expiry of protection copies |
| **Out-of-band policy change** | An attacker with array admin turning immutability off |
| **Separate credentials for storage** | Production domain compromise extending to the array |
| **MFA on the array console** | Credential reuse |
| **Replication to a second array** | Loss of the site |

## The eradication window

The constraint people underestimate: **attackers dwell before they detonate.** If an intruder was present for six weeks before encrypting, then snapshots from the last six weeks may contain their tooling and persistence — restoring from them reinstates the compromise.

Therefore **retention must exceed plausible dwell time.** Seven days of immutable snapshots protects against accidental deletion and does not protect against an attacker who was patient. This is the arithmetic that determines retention policy, and it is why cyber-resilience retention is usually far longer than operational-recovery retention.

## Rehearsal

A recovery capability that has never been exercised is a hypothesis. Rehearsal answers questions you would rather not discover during an incident: how long a full restore actually takes, whether the recovery order is right, whether anyone knows the immutable-snapshot recovery procedure, and whether the recovered system actually works.

## Hands-On Lab

Python models resilience controls. **Cost:** none.

### Lab 7.1 — Immutability that resists a compromised administrator

**Objective:** Test retention locks against an attacker holding array credentials.

```bash
python3 - <<'EOF'
import datetime
today = datetime.date(2026, 8, 4)

class Array:
    def __init__(self): self.snapshots = {}
    def snap(self, name, retain_days, locked):
        self.snapshots[name] = {"expires": today + datetime.timedelta(days=retain_days), "locked": locked}
        return f"created {name} (retain {retain_days}d, {'IMMUTABLE' if locked else 'deletable'})"
    def delete(self, name, actor):
        s = self.snapshots.get(name)
        if not s: return f"{name}: not found"
        if s["locked"] and today < s["expires"]:
            return (f"DENIED — {name} is retention-locked until {s['expires']}. "
                    f"Refused even for {actor}; lifting it requires an OUT-OF-BAND process with the vendor")
        del self.snapshots[name]
        return f"DELETED {name} by {actor}"
    def shorten(self, name, actor):
        s = self.snapshots.get(name)
        if s and s["locked"]:
            return f"DENIED — cannot shorten retention on a locked snapshot ({actor})"
        return f"retention shortened by {actor}"

a = Array()
print(a.snap("nightly-2026-08-04", 30, locked=True))
print(a.snap("adhoc-test", 7, locked=False))
print()
print(a.delete("nightly-2026-08-04", "attacker with storage-admin credentials"))
print(a.shorten("nightly-2026-08-04", "attacker with storage-admin credentials"))
print(a.delete("adhoc-test", "attacker with storage-admin credentials"))
print("\nThe threat model ASSUMES the attacker has admin credentials — that is how ransomware")
print("operates. A protection copy an administrator can delete offers no protection against")
print("someone who has become an administrator.")
EOF
```

**Expected result:** The locked snapshot resists both deletion and retention-shortening even for a credentialed attacker, while the unlocked one is removed instantly. The threat model stated at the end is the reason the friction exists: immutability is designed for the case where authentication has already failed.

**Negative test:** Relying on role-based access control alone to protect snapshots — RBAC governs who *should* delete them, and a compromised administrator account is, by definition, someone who should.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Retention against dwell time

**Objective:** Show why short retention fails against a patient attacker.

```bash
python3 - <<'EOF'
def survivable(retention_days, dwell_days):
    if retention_days > dwell_days:
        clean = retention_days - dwell_days
        return True, f"{clean} day(s) of PRE-COMPROMISE snapshots survive — clean recovery possible"
    return False, ("EVERY retained snapshot post-dates the intrusion. Restoring reinstates the "
                   "attacker's tooling and persistence — you recover the compromise")

scenarios = [
  ("operational retention",  7,  45),
  ("extended retention",    30,  45),
  ("cyber-resilience retention", 90, 45),
  ("cyber-resilience retention", 90, 120),
]
for label, retention, dwell in scenarios:
    ok, why = survivable(retention, dwell)
    print(f"{label:30} retention {retention:>3}d vs dwell {dwell:>3}d -> {'SAFE' if ok else 'COMPROMISED'}")
    print(f"{'':30} {why}\n")
print("Attackers commonly dwell for WEEKS before detonating. Retention sized for accidental")
print("deletion (7 days) is useless against that; cyber-resilience retention must EXCEED")
print("plausible dwell time. That is the arithmetic behind the policy — not a round number.")
EOF
```

**Expected result:** Seven- and thirty-day retention both fail against a 45-day dwell, ninety days survives it, and even ninety fails against a 120-day dwell. The framing is what matters: retention length is a **security parameter derived from dwell time**, not an operational convenience, and the two purposes justify different numbers.

**Negative test:** Setting immutable retention to match operational snapshot retention — you have made the operational copies tamper-proof and still cannot reach back past the intrusion.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Rehearse the clean recovery

**Objective:** Discover the gaps before an incident does.

```bash
python3 - <<'EOF'
def rehearse(name, steps):
    print(f"\n=== {name} ===")
    ok = True
    for step, passed, detail in steps:
        print(f"   [{'PASS' if passed else 'FAIL'}] {step}")
        if not passed:
            ok = False
            print(f"          {detail}")
    print(f"   => {'RECOVERY PROVEN' if ok else 'GAPS FOUND — fix them now, not during an incident'}")

rehearse("Q3 ransomware recovery rehearsal", [
  ("identify last clean snapshot (pre-dwell)", True,  ""),
  ("immutable snapshot present and locked",    True,  ""),
  ("restore to ISOLATED environment",          True,  ""),
  ("recovery procedure documented + findable", False, "the runbook was on the file share that was encrypted"),
  ("staff know the out-of-band unlock process",False, "only one engineer knew it, and they have left"),
  ("restore completes within RTO",             True,  ""),
  ("application starts and serves users",      True,  ""),
])
print("\nBoth failures are ORGANIZATIONAL, not technical — and both are invisible until you")
print("rehearse. Keep the runbook OFF the systems it protects (printed, or in a separate tenant),")
print("and make sure more than one person knows the vendor unlock procedure.")
EOF
```

**Expected result:** The technical steps pass and two organizational steps fail — a runbook stored on the encrypted file share, and unlock knowledge held by one departed engineer. Both are entirely realistic, neither is detectable from the array's configuration, and rehearsal is the only thing that surfaces them.

**Negative test:** Verifying immutability configuration and declaring the recovery capability proven — configuration is necessary and says nothing about whether your people can execute under pressure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Storage-enforced immutability understood as protection against a compromised administrator.
- [ ] Retention locks tested against deletion and early expiry, with the out-of-band unlock noted.
- [ ] Retention sized to exceed plausible attacker dwell time.
- [ ] Clean recovery rehearsed, with runbooks kept off the systems they protect.
