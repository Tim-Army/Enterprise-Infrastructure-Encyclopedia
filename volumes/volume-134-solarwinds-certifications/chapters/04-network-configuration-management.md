# Chapter 04: Network Configuration and Change Management

## Learning Objectives

- Back up device configurations and detect drift from an approved baseline.
- Assess configurations against compliance policies and produce audit evidence.
- Manage change through review, staged deployment, and rollback.
- Track end-of-life and vulnerability exposure across the device estate.

## Why configuration is monitored

This is the **Observability Self-Hosted Network Management** exam's territory (the historical NCM product), and it answers a different question from Chapter 03. Monitoring asks *is it working?*; configuration management asks *is it configured correctly, did someone change it, and can we prove compliance?*

Four capabilities carry the discipline:

| Capability | Purpose |
|:---|:---|
| **Configuration backup** | A current copy of every device config — the precondition for recovery |
| **Change detection / drift** | Know that a config changed, what changed, and when |
| **Compliance assessment** | Check configs against policy (hardening standards, regulatory requirements) |
| **Change deployment** | Push changes in a controlled, reviewable, reversible way |

The single most valuable of these is the least glamorous: **a current configuration backup turns a dead switch into a twenty-minute swap** instead of an afternoon of reconstruction from memory.

## Drift

**Configuration drift** is divergence between the approved baseline and what is actually running. It arrives through emergency fixes never documented, changes made directly on the device, vendor defaults after a replacement, or an undocumented tweak that "fixed" something years ago.

Drift matters for three reasons: it breaks the assumption that your documentation describes reality, it silently erodes hardening, and — most practically — a device restored from a stale backup loses whatever undocumented change was keeping something working.

## Compliance

A **compliance policy** is a rule evaluated against a configuration: SSH rather than Telnet, no default community strings, AAA configured, NTP set, logging to the right collector, encrypted passwords. Real rule sets derive from hardening guides (CIS, DISA STIGs) or regulation (PCI DSS, HIPAA), and the platform's value is producing **evidence at scale** — hundreds of devices assessed on a schedule, with exceptions tracked — rather than a spreadsheet built by hand before an audit.

## Change management

Controlled change looks the same everywhere: **review → back up → deploy to a pilot → verify → deploy widely → keep a rollback path**. Configuration management tooling adds the ability to do that across hundreds of devices consistently — and, critically, to **prove afterwards what was changed and by whom**.

## Hands-On Lab

Python models configuration management. **Cost:** none.

### Lab 4.1 — Detect configuration drift

**Objective:** Diff a running config against the approved baseline.

```bash
python3 - <<'EOF'
import difflib
baseline = """hostname core-sw-1
ip ssh version 2
no ip http server
snmp-server community PRIVATE-STR-1 RO
ntp server 10.0.0.10
logging host 10.0.0.20
line vty 0 4
 transport input ssh""".splitlines()

running = """hostname core-sw-1
ip ssh version 2
ip http server
snmp-server community public RO
ntp server 10.0.0.10
logging host 10.0.0.20
line vty 0 4
 transport input ssh telnet""".splitlines()

print("=== DRIFT: running vs approved baseline ===")
for line in difflib.unified_diff(baseline, running, "baseline", "running", lineterm="", n=0):
    if line.startswith(("---","+++","@@")): continue
    print(f"  {line}")
print("\nAssessment of the drift:")
print("  + ip http server        -> unencrypted management plane re-enabled")
print("  + community 'public'    -> DEFAULT community string (was a unique one)")
print("  + transport input telnet-> cleartext management re-enabled alongside SSH")
print("\nAll three are SECURITY REGRESSIONS, and none of them caused an outage —")
print("which is exactly why drift detection exists: nothing else would have reported them.")
EOF
```

**Expected result:** Three drifted lines, each a security regression: HTTP management re-enabled, the SNMP community reverted to the default `public`, and Telnet added back to the VTY lines. The closing observation is the argument for the discipline — **none of these break anything**, so availability monitoring stays green while the device's hardening quietly unravels. Drift detection is how you find changes that have no symptom.

**Negative test:** Comparing only against the last backup rather than an approved baseline — if the bad change was captured in last night's backup, it becomes the new "normal" and the diff is clean.

**Cleanup:** None.

### Lab 4.2 — Compliance assessment at scale

**Objective:** Evaluate policy rules and produce audit evidence.

```bash
python3 - <<'EOF'
import re
POLICIES = [
  {"id":"SEC-01","desc":"SSH v2 enabled",          "must_match":r"ip ssh version 2"},
  {"id":"SEC-02","desc":"HTTP server disabled",    "must_match":r"no ip http server"},
  {"id":"SEC-03","desc":"No default SNMP community","must_not_match":r"community\s+(public|private)\b"},
  {"id":"SEC-04","desc":"Telnet not permitted",    "must_not_match":r"transport input .*telnet"},
  {"id":"OPS-01","desc":"NTP configured",          "must_match":r"ntp server"},
  {"id":"OPS-02","desc":"Central logging",         "must_match":r"logging host"},
]
devices = {
  "core-sw-1": "hostname core-sw-1\nip ssh version 2\nip http server\nsnmp-server community public RO\nntp server 10.0.0.10\nlogging host 10.0.0.20\ntransport input ssh telnet",
  "core-sw-2": "hostname core-sw-2\nip ssh version 2\nno ip http server\nsnmp-server community Uniq-Str RO\nntp server 10.0.0.10\nlogging host 10.0.0.20\ntransport input ssh",
}
total_fail = 0
for dev, cfg in devices.items():
    fails = []
    for p in POLICIES:
        if "must_match" in p and not re.search(p["must_match"], cfg):     fails.append(p)
        if "must_not_match" in p and re.search(p["must_not_match"], cfg): fails.append(p)
    total_fail += len(fails)
    print(f"\n{dev}: {len(POLICIES)-len(fails)}/{len(POLICIES)} policies passed")
    for f in fails:
        print(f"    FAIL {f['id']}: {f['desc']}")
print(f"\nEstate summary: {total_fail} violation(s). Evidence = policy id, device, timestamp, pass/fail.")
print("Scheduled assessment turns 'we think we're compliant' into a dated, per-device record.")
EOF
```

**Expected result:** `core-sw-1` fails four policies (HTTP enabled, default community, Telnet permitted) while `core-sw-2` passes all six. The value is in the last line: assessing on a schedule produces **dated, per-device evidence**, which is what an auditor asks for and what a hand-built spreadsheet cannot credibly provide across hundreds of devices.

**Negative test:** Assessing compliance only before an audit — you learn about violations in the week you can least afford to remediate them, and you have no evidence the controls operated over the period under review.

**Cleanup:** None.

### Lab 4.3 — Controlled change with rollback

**Objective:** Gate a configuration change through the change process.

```bash
python3 - <<'EOF'
def deploy(change, backed_up, reviewed, pilot_ok, window, rollback_ready):
    steps = []
    if not backed_up:      return ["BLOCKED: no current backup — you cannot roll back what you did not save"]
    steps.append("current config backed up")
    if not reviewed:       return steps + ["BLOCKED: change not peer-reviewed"]
    steps.append("peer review complete")
    if pilot_ok is None:   return steps + ["BLOCKED: deploy to a pilot device first"]
    if not pilot_ok:       return steps + ["STOPPED: pilot failed — fix before wider rollout"]
    steps.append("pilot device verified")
    if not window:         return steps + ["HELD: outside the approved change window"]
    steps.append("in change window")
    if not rollback_ready: return steps + ["BLOCKED: no rollback plan"]
    steps += ["rollback plan confirmed", "DEPLOY to remaining devices", "verify + record who/what/when"]
    return steps

cases = [
  ("harden VTY (no telnet)", True,  True,  True,  True,  True),
  ("emergency ACL fix",      True,  True,  None,  True,  True),
  ("SNMP community rotation",False, True,  True,  True,  True),
]
for name, *args in cases:
    print(f"\n{name}:")
    for s in deploy(name, *args): print(f"   - {s}")
EOF
```

**Expected result:** The hardening change proceeds through every gate; the emergency ACL fix is blocked for skipping the pilot; the SNMP rotation is blocked for having **no backup**, on the reasoning that you cannot roll back what you never saved. The gate ordering encodes the lesson — backup first, because it is the only step that makes every later step reversible.

**Negative test:** Pushing a VTY or ACL change to every device at once — a mistake in that change locks you out of the entire estate simultaneously, and the fix requires physical console access to hundreds of devices.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Configuration backups established as the precondition for recovery and rollback.
- [ ] Drift detected against an approved baseline, including changes with no symptom.
- [ ] Compliance assessed at scale with dated, per-device evidence.
- [ ] Change gated through backup, review, pilot, window, and rollback.
