# Chapter 08: Deployment, Policy, and Administration

## Learning Objectives

- Understand agent deployment and the management console.
- Design protection policy — detect versus protect modes and exclusions.
- Place API-driven automation and RemoteOps.
- Recognize the administrator's role in balancing security and disruption.

*Cert relevance: deployment, policy, and administration are the **Administrator (Levels 1–3)** and **CTP** territory — the operational backbone.*

## Deployment and the console

Every protection story starts with **getting the agent onto endpoints** and managing it centrally. SentinelOne is administered from a **management console** where admins deploy agents (via installers, software-distribution tools, or the API), organize endpoints into **groups and sites** (by department, region, or role), monitor agent health, and set policy. The **Administrator** certification ladder (Levels 1–3) progresses from basic console operation to advanced, API-driven management.

Organizing endpoints sensibly matters because **policy is applied by group**: putting servers, workstations, and kiosks in appropriate groups lets you give each the right policy — a domain controller needs different protection settings than a developer's laptop. Good group structure is the foundation of good policy. The lab touches this within the policy exercise.

## Policy: detect versus protect

The central policy decision is the **response mode**:

| Mode | The agent... | Use when |
|:---|:---|:---|
| **Detect (alert-only)** | Detects and alerts, but does *not* auto-respond | Initial rollout, tuning, sensitive systems |
| **Protect (autonomous)** | Detects *and* autonomously responds (kill, quarantine) | Steady state, most endpoints |

The [autonomy trade-off (Chapter 2)](02-autonomous-endpoint-protection.md) lives here: **protect mode** stops attacks at machine speed but risks a false positive autonomously disrupting a legitimate process; **detect mode** is safe but requires a human to act. The discipline is to **roll out in detect mode first** (observe, tune, build confidence that the agent is not flagging legitimate business software), then move to protect mode once tuned. **Exclusions** (telling the agent to ignore specific known-good software) are how you prevent false positives on legitimate but unusual applications — but every exclusion is a hole, so they must be *minimal and justified*. The lab models the rollout.

## API and RemoteOps

Two advanced-administration capabilities the higher tiers cover:

- **API-driven automation** — everything in the console is available via API, so administration scales through automation (auto-deploy to new endpoints, auto-tag, integrate with ITSM/SOAR). Level 3 administration is largely API work.
- **RemoteOps** — remote forensics and response: run scripts, collect forensic artifacts, and remediate across endpoints *at scale* from the console, without physically touching machines. Essential for incident response across a distributed fleet.

The lab is covered within the policy exercise.

## Hands-On Lab

Python models policy administration. **Cost:** none.

### Lab 8.1 — Roll out policy: detect first, then protect

**Objective:** Design a safe rollout that avoids disrupting the business.

```bash
python3 - <<'EOF'
# endpoint groups, and how to phase them from detect -> protect
GROUPS = [
  # group,           count, sensitivity,          rollout note
  ("pilot-IT",        20,   "low (IT can react)",  "protect mode day 1 — they'll catch FPs"),
  ("workstations",    2000, "medium",              "detect 2 weeks -> tune -> protect"),
  ("developers",      300,  "high (weird tools)",  "detect longer; devs run unusual binaries -> tune exclusions"),
  ("domain-controllers",8,  "CRITICAL",            "detect first; a FP auto-isolating a DC = outage. Protect only when confident"),
  ("kiosks",          150,  "low, static",         "protect mode — behavior is predictable"),
]
print("PHASED ROLLOUT (detect -> tune -> protect), by group sensitivity:\n")
print(f"   {'group':20}{'count':>6}{'sensitivity':>22}   approach")
for g, n, sens, note in GROUPS:
    print(f"   {g:20}{n:>6}{sens:>22}   {note}")
print("\nThe policy discipline:")
print("  START IN DETECT mode where a false positive would HURT (domain controllers,")
print("     developer machines with weird-but-legit tools). Observe, tune exclusions,")
print("     build confidence, THEN switch to protect.")
print("  GO STRAIGHT TO PROTECT where behavior is predictable and low-risk (kiosks) or")
print("     the team can self-recover (IT pilot).")
print("\nWhy: protect mode stops attacks at machine speed — but a FALSE POSITIVE in")
print("protect mode AUTONOMOUSLY isolates/kills, and doing that to a domain controller")
print("is a self-inflicted outage. Detect-first lets you find the FPs (a legit dev tool")
print("that looks like injection) and add MINIMAL exclusions BEFORE autonomy can act on")
print("them. The admin balances security (protect ASAP) against disruption (don't break")
print("the business). This tuning judgment is what the Administrator certs validate.")
EOF
```

**Expected result:** A phased rollout putting sensitive groups (domain controllers, developer machines) in detect mode to tune before protect, while predictable low-risk groups (kiosks, IT pilot) go straight to protect. The policy lesson is to balance security against disruption — detect-first where a false positive would hurt, so you tune minimal exclusions before autonomy can act, which is the tuning judgment the Administrator certifications validate.

**Negative test:** Enabling protect mode everywhere on day one. A false positive autonomously isolates a domain controller — a self-inflicted outage; detect-first on sensitive groups surfaces and tunes false positives before autonomy acts.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Agent deployment and the management console understood, with endpoint grouping as the basis for policy.
- [ ] Detect versus protect modes understood, with detect-first rollout and minimal, justified exclusions.
- [ ] API-driven automation and RemoteOps placed as advanced-administration capabilities for scale and IR.
- [ ] The administrator's role recognized as balancing security against business disruption through tuned policy.
