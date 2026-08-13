# Chapter 05: Rollback and Remediation

## Learning Objectives

- Explain one-click remediation of an attack's changes.
- Understand rollback — restoring a system to its pre-attack state.
- Place ransomware rollback as the signature recovery capability.
- Recognize the operational value of recovery without reimaging.

*Cert relevance: remediation and rollback are core **SIREN** skills — closing out an incident by undoing its damage.*

## Remediation: undo the changes

Containing an attack ([Chapter 4](04-detection-and-response-edr-workflows.md)) stops it from continuing; **remediation** undoes what it already did. An attack leaves a trail: files dropped, registry keys added, scheduled tasks created for persistence, services installed, configurations changed. Cleaning all of this by hand — finding every artifact across every affected endpoint — is painstaking and error-prone; miss one persistence mechanism and the attacker returns.

SentinelOne uses the [Storyline (Chapter 3)](03-storyline-autonomous-correlation.md) to make remediation **one-click**: because the agent recorded *every* change the attack made (it tracked the whole story), it can **automatically reverse all of them** — delete the dropped files, remove the registry keys, kill the scheduled task, undo the configuration changes — across every affected endpoint. Remediation is comprehensive because the record is comprehensive. The lab models complete-versus-partial remediation.

## Rollback: restore the pre-attack state

**Rollback** goes further: it restores affected files to their **state before the attack**. The signature case is **ransomware rollback** — when ransomware encrypts files, SentinelOne can **restore the original, unencrypted files**, returning the endpoint to its pre-attack state. On Windows this leverages the OS's Volume Shadow Copy Service (VSS), which the agent protects and uses to recover the pre-encryption versions.

This is a genuine differentiator: most endpoint tools can *detect and stop* ransomware, but stopping it after it has encrypted 8% of the disk still leaves 8% encrypted. **Rollback recovers those too**, turning a ransomware incident from "restore from backup and lose hours of work (or pay the ransom)" into "click rollback, files restored, minutes later back to normal." The lab quantifies the recovery.

## Recovery without reimaging

The operational value is **recovery without reimaging**. Traditionally, a compromised endpoint is wiped and rebuilt from a golden image — hours of downtime per machine, lost local data, and IT labor, multiplied across every affected device in an incident. Rollback and one-click remediation let you **recover the machine in place**: undo the attack's changes, restore encrypted files, and return the endpoint to service *without* a reimage. At incident scale (dozens or hundreds of endpoints), this is the difference between a day of disruption and an hour. The lab models the scale.

## Hands-On Lab

Python models remediation and rollback. **Cost:** none.

### Lab 5.1 — Complete remediation from the recorded story

**Objective:** See why recording every change enables complete, one-click cleanup.

```bash
python3 - <<'EOF'
# every change the attack made, as recorded in the Storyline
ATTACK_CHANGES = [
  ("file",     "dropped C:\\Temp\\payload.exe"),
  ("file",     "dropped C:\\Users\\bob\\update.dll"),
  ("registry", "added HKCU\\...\\Run\\Updater"),
  ("task",     "created scheduled task 'Updater' (persistence)"),
  ("service",  "installed service 'WinHelpSvc'"),
  ("file",     "modified C:\\Windows\\hosts"),
]
print("The attack made 6 changes. Two ways to clean up:\n")
print("MANUAL remediation (analyst hunts for artifacts by hand):")
# realistically a human finds most but misses subtle ones under time pressure
found_manually = ATTACK_CHANGES[:4]   # misses the service + hosts edit
missed = ATTACK_CHANGES[4:]
for typ, ch in found_manually:
    print(f"   found + removed: {ch}")
for typ, ch in missed:
    print(f"   MISSED: {ch}")
print(f"   -> {len(missed)} artifact(s) missed. The service re-establishes persistence")
print("      -> the attacker is BACK next reboot. Incomplete cleanup = reinfection.\n")

print("ONE-CLICK remediation (from the recorded Storyline):")
print("   the agent recorded ALL 6 changes as they happened, so it reverses ALL 6:")
for typ, ch in ATTACK_CHANGES:
    print(f"   auto-reversed: {ch}")
print(f"   -> {len(ATTACK_CHANGES)}/{len(ATTACK_CHANGES)} changes undone. Nothing missed. Clean.\n")
print("The insight: remediation is only as complete as your RECORD of the attack.")
print("Manual cleanup misses subtle artifacts under time pressure (the installed")
print("service, the hosts edit) — and ONE missed persistence mechanism means the")
print("attacker returns. Because Storyline recorded EVERY change, SentinelOne reverses")
print("EVERY change in one click. Comprehensive record -> comprehensive remediation.")
EOF
```

**Expected result:** Manual remediation missing a couple of subtle artifacts (an installed service, a hosts-file edit) that re-establish the attacker's foothold, versus one-click remediation reversing all recorded changes completely. The remediation lesson is that cleanup is only as complete as the record of the attack — because Storyline recorded every change, SentinelOne reverses every one, where manual cleanup misses persistence and invites reinfection.

**Negative test:** Cleaning up an incident by manually hunting for artifacts. Under time pressure a responder misses subtle persistence (a service, a scheduled task), and one missed mechanism brings the attacker back — the recorded Storyline enables complete automated reversal instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Ransomware rollback and recovery at scale

**Objective:** Quantify rollback versus reimaging across an incident.

```bash
python3 - <<'EOF'
ENDPOINTS = 60            # endpoints hit in a ransomware incident
FILES_PER = 20000
ENCRYPTED_FRACTION = 0.08 # autonomous response stopped it fast, but 8% got encrypted first

print(f"Ransomware incident: {ENDPOINTS} endpoints, ~{ENCRYPTED_FRACTION:.0%} of files")
print(f"encrypted before autonomous response killed it.\n")
encrypted_per = int(FILES_PER*ENCRYPTED_FRACTION)
print(f"per endpoint: {encrypted_per} files encrypted (of {FILES_PER})\n")

print("OPTION A — reimage every affected endpoint:")
REIMAGE_HOURS = 3         # wipe, rebuild, reconfigure, restore data per machine
total_reimage = ENDPOINTS * REIMAGE_HOURS
print(f"   {REIMAGE_HOURS}h/machine x {ENDPOINTS} = {total_reimage} IT-hours of downtime")
print("   + lost local data since last backup, + users idle for hours each\n")

print("OPTION B — restore from backup (no rollback):")
print("   recover encrypted files from last night's backup -> lose up to a day's work")
print("   (and hope the backups weren't also encrypted)\n")

print("OPTION C — SentinelOne ROLLBACK:")
ROLLBACK_MIN = 5         # click rollback, files restored from protected shadow copies
total_rollback_h = ENDPOINTS * ROLLBACK_MIN / 60
print(f"   click rollback -> encrypted files restored to pre-attack state (VSS)")
print(f"   ~{ROLLBACK_MIN} min/endpoint x {ENDPOINTS} = {total_rollback_h:.1f} IT-hours, no reimage,")
print("   no lost data (restored to the moment before encryption), users back in minutes\n")
print(f"   reimaging: {total_reimage} IT-hours  vs  rollback: {total_rollback_h:.1f} IT-hours")
print(f"   -> ~{total_reimage/total_rollback_h:.0f}x less effort, and ZERO data loss\n")
print("The differentiator: most tools DETECT and STOP ransomware — but the files")
print("encrypted BEFORE it was stopped are still lost (restore from backup, or pay).")
print("SentinelOne ROLLS BACK those files to their pre-attack state, so a ransomware")
print("hit becomes 'click rollback, back in minutes' instead of a day of reimaging and")
print("lost work. Recovery IN PLACE, at incident scale — the signature recovery feature.")
EOF
```

**Expected result:** Reimaging 60 endpoints costing far more IT-hours and data loss than one-click rollback restoring encrypted files to their pre-attack state in minutes. The rollback lesson is that detecting and stopping ransomware still leaves the already-encrypted files lost — rollback recovers those in place, turning an incident from a day of reimaging into minutes, the signature SentinelOne recovery capability.

**Negative test:** Recovering a ransomware incident by reimaging every affected endpoint. It costs hours per machine and loses local data; rollback restores the encrypted files in place in minutes with no reimage and no data loss.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Remediation understood as reversing every change an attack made — complete because the Storyline record is complete.
- [ ] Rollback understood as restoring files to their pre-attack state, notably recovering ransomware-encrypted files.
- [ ] Ransomware rollback placed as the signature recovery capability (Windows VSS-based).
- [ ] Recovery-without-reimaging recognized as the operational value at incident scale.
