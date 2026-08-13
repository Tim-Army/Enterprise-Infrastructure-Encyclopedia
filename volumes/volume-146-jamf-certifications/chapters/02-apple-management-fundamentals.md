# Chapter 02: Apple Management Fundamentals

## Learning Objectives

- Explain the Apple MDM framework Jamf builds on, and what supervision means.
- Understand enrollment: Automated Device Enrollment, Apple Business Manager, and user-initiated.
- Place declarative device management (DDM) as the modern direction.
- Recognize why Apple management differs fundamentally from Windows management.

*Cert relevance: the foundation of every Jamf Pro certification (100–400) — you cannot administer Jamf without understanding the Apple framework beneath it.*

## Jamf sits on Apple's framework

The single most important thing to understand about Jamf is that **it does not invent its own management protocol — it implements Apple's.** Apple defines the **MDM (Mobile Device Management) framework**; Jamf is an MDM *server* that speaks it. This has a consequence that surprises Windows admins: **Jamf can only do what Apple's framework permits.** You cannot force arbitrary changes onto a Mac the way Group Policy can force them onto Windows — you send Apple-defined commands and configuration profiles, and the device obeys within Apple's model.

This is a feature, not a limitation, and it defines the whole discipline: **Apple management is cooperative, not coercive.** The device honors management because it was enrolled into it, and the boundaries are Apple's. An admin who fights this — trying to make a Mac behave like a Windows box under an iron fist — is fighting the platform.

## Supervision

**Supervision** is the elevated management state that unlocks the fuller set of MDM capabilities. A supervised device (typically one enrolled through Automated Device Enrollment on organization-owned hardware) accepts management commands a personally-owned, user-enrolled device does not — more configuration, more restrictions, more control.

The distinction maps to ownership:

| | **Supervised** (org-owned) | **Unsupervised / user-enrolled** (BYOD) |
|:---|:---|:---|
| Enrolled via | Automated Device Enrollment (ADE) | User-initiated |
| Management scope | Full — restrictions, wipe, app management | Limited — respects personal data boundaries |
| Right for | Corporate/education fleet | Employee-owned devices |

The privacy line is deliberate and Apple enforces it: a personally-owned device under user enrollment walls off personal data from the organization, which is *correct* — the org manages the work, not the person's photos. An admin who wants full control must own the device.

## Enrollment

How a device comes under management determines what management can do:

| Method | Is | Produces |
|:---|:---|:---|
| **Automated Device Enrollment (ADE)** | Zero-touch — device enrolls automatically on first boot, via Apple Business/School Manager | Supervised, org-owned, hands-off deployment |
| **Apple Business Manager (ABM) / School Manager (ASM)** | The Apple portal linking purchased devices and apps to your MDM | The supply chain for zero-touch |
| **User-initiated enrollment** | The user opts in (BYOD) | Unsupervised, privacy-preserving |

**ADE is the prize**: a device shipped from Apple (or a reseller) with its serial number assigned to your organization in ABM enrolls into Jamf *automatically on first power-on*, configured before the user touches it — true zero-touch deployment. The lab models why ADE beats manual enrollment at scale.

## Declarative device management

**Declarative Device Management (DDM)** is Apple's modern direction, and the certifications are moving toward it. The old MDM model is *imperative*: the server sends commands and polls for status. DDM is *declarative*: the server declares a desired state, and the **device itself** proactively works to reach and maintain it, reporting status changes without being polled.

The parallel is exact to [Kubernetes' declarative model](../../volume-041-cncf-kubernetes-certifications/README.md) and [Terraform's desired-state](../../volume-042-hashicorp-certifications/README.md): declare what you want, let the system converge, rather than issuing step-by-step commands. DDM scales better (the device does the work, the server is not polling thousands of devices) and is more reliable (the device maintains state even when offline from the server). It is where Apple management is going, and a current Jamf admin needs to understand it.

## Hands-On Lab

Python models Apple management concepts. **Cost:** none.

### Lab 2.1 — Cooperative, not coercive: what MDM can and cannot do

**Objective:** Understand the boundaries Apple's framework sets.

```bash
python3 - <<'EOF'
ACTIONS = [
  # action,                              supervised, unsupervised, note
  ("install a configuration profile",     True,  True,  "both — it's the core mechanism"),
  ("enforce a passcode policy",           True,  True,  "allowed on both"),
  ("install/remove managed apps",         True,  True,  "managed apps, both"),
  ("restrict AirDrop, screen recording",  True,  False, "supervised only"),
  ("remotely wipe the device",            True,  "partial", "full on supervised; user-data-only on BYOD"),
  ("silently install any app",            True,  False, "supervised only — Apple gates this"),
  ("read the user's personal photos",     False, False, "NEITHER — Apple forbids it, by design"),
  ("force arbitrary registry-style edits","n/a", "n/a", "IMPOSSIBLE — no such concept on Apple"),
]
print(f"{'action':38}{'supervised':>12}{'unsupervised':>14}")
for act, sup, unsup, note in ACTIONS:
    print(f"{act:38}{str(sup):>12}{str(unsup):>14}")
    print(f"{'':38}   {note}")
print("\nTwo boundaries Windows admins keep hitting:")
print("  1. NO arbitrary control. There is no 'force anything' — you send Apple-")
print("     DEFINED commands and profiles. The Mac obeys WITHIN Apple's model. This")
print("     is not Jamf being weak; it's Apple's framework, and Jamf implements it.")
print("  2. PRIVACY is enforced by Apple, not by policy. You CANNOT read personal")
print("     data on a user-enrolled device — the framework doesn't expose it. Trying")
print("     is not 'against policy,' it is IMPOSSIBLE.")
print("\nApple management is COOPERATIVE: the device honors management because it was")
print("enrolled, within boundaries Apple sets. Supervision (org-owned) unlocks more;")
print("BYOD deliberately walls off the person. An admin who understands this designs")
print("with the grain; one who fights it files support tickets that end in 'Apple")
print("doesn't allow that' — the single most common realization on the Jamf 100.")
EOF
```

**Expected result:** A capability matrix where supervision unlocks restrictions and silent installs, BYOD preserves privacy, and reading personal data is impossible on either. The cooperative-not-coercive framing is the foundational lesson — Apple's framework sets the boundaries, Jamf implements within them, and fighting that is the commonest Windows-admin mistake.

**Negative test:** Expecting Group-Policy-style total control over a Mac. Apple's framework does not offer it; management is what Apple's commands and profiles permit, no more.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Why ADE (zero-touch) beats manual enrollment

**Objective:** Quantify enrollment at fleet scale.

```bash
python3 - <<'EOF'
FLEET = 2000
MANUAL_MIN_PER_DEVICE = 25    # unbox, enroll, configure, hand over
ADE_MIN_PER_DEVICE = 2        # verify it enrolled itself; user completes setup
IT_HOURLY = 45

manual_hours = FLEET * MANUAL_MIN_PER_DEVICE / 60
ade_hours = FLEET * ADE_MIN_PER_DEVICE / 60
print(f"deploying {FLEET} Macs:\n")
print(f"MANUAL enrollment: {MANUAL_MIN_PER_DEVICE} min/device -> {manual_hours:,.0f} IT-hours -> ${manual_hours*IT_HOURLY:,.0f}")
print(f"ADE (zero-touch):  {ADE_MIN_PER_DEVICE} min/device  -> {ade_hours:,.0f} IT-hours -> ${ade_hours*IT_HOURLY:,.0f}")
print(f"\nsaving: {manual_hours-ade_hours:,.0f} IT-hours (${(manual_hours-ade_hours)*IT_HOURLY:,.0f})")
print("\nBut the hours are not even the main point. With ADE:")
print("  - the device ships from Apple/reseller straight to the USER, never touching IT")
print("  - it enrolls into Jamf on FIRST POWER-ON, configured before the user logs in")
print("  - a remote/new-hire employee gets a ready-to-work Mac in the mail — no IT")
print("    depot, no imaging bench, no shipping-to-IT-first")
print("\nThe precondition: the device's serial must be in Apple Business Manager,")
print("assigned to your MDM. That is why ABM/ASM is the SUPPLY CHAIN for zero-touch —")
print("buy through channels that add serials to your ABM, and enrollment becomes")
print("automatic. Buy off a random shelf and you are back to manual.")
print("\nThe Jamf admin's job here is upstream: get purchasing into ABM, so every")
print("device arrives ready to self-enroll. Manual enrollment at 2000 devices is a")
print("choice to spend ${:,.0f} that ADE makes unnecessary.".format((manual_hours-ade_hours)*IT_HOURLY))
EOF
```

**Expected result:** ADE cutting deployment from hundreds of IT-hours to a fraction, with the deeper win being that devices ship straight to users and self-enroll on first boot. The ABM-as-supply-chain point is the actionable lesson — zero-touch depends on serials being in Apple Business Manager, so the admin's real work is getting purchasing into that channel.

**Negative test:** Manually enrolling a large fleet because "that's how we've always done it." At 2000 devices it is a five-figure labor cost ADE eliminates, plus every device routing through IT instead of straight to the user.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Imperative MDM versus declarative (DDM)

**Objective:** See why declarative scales and survives disconnection.

```bash
python3 - <<'EOF'
DEVICES = 5000
print("SCENARIO: enforce 'FileVault encryption ON' across the fleet.\n")
print("IMPERATIVE MDM (old model): server commands + polls each device")
poll_interval_min = 15
commands_per_day = DEVICES * (24*60//poll_interval_min)   # server checks each device repeatedly
print(f"   server polls {DEVICES:,} devices every {poll_interval_min} min = {commands_per_day:,} checks/day")
print("   a device OFFLINE at check time is missed; caught only on the next poll")
print("   the SERVER does all the work and must scale with the fleet\n")
print("DECLARATIVE (DDM): server DECLARES 'FileVault must be ON'; devices comply")
print(f"   server sends the declaration ONCE to each of {DEVICES:,} devices")
print("   each DEVICE proactively enforces it and maintains it — even OFFLINE")
print("   the device reports status changes; the server does NOT poll")
print(f"   server load: ~{DEVICES:,} declarations, then status callbacks — not {commands_per_day:,}/day\n")
print("Two wins, the same as Kubernetes/Terraform desired-state:")
print("  SCALE   — the DEVICE does the enforcement work, so the server load does not")
print("            grow with polling frequency. 5,000 or 50,000, the model holds.")
print("  RESILIENCE — a declaratively-managed device MAINTAINS its state while")
print("            disconnected (on a plane, off-VPN); imperative management can only")
print("            act when it reaches the device.")
print("\nDDM is where Apple management is GOING, and the Jamf certifications are")
print("following. 'Declare the state, let the device converge' replaces 'command and")
print("poll' — the same shift the infra world made from scripts to Terraform.")
EOF
```

**Expected result:** Imperative MDM generating hundreds of thousands of daily polls and missing offline devices, versus DDM declaring state once and letting devices self-enforce even offline. The Kubernetes/Terraform parallel is the framing — declarative desired-state scales and survives disconnection, and it is where Apple management (and the certifications) are heading.

**Negative test:** Assuming polling frequency can be raised to catch offline devices sooner. It multiplies server load without helping — the offline device is unreachable regardless; DDM sidesteps the problem by moving enforcement to the device.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Jamf understood as an MDM server implementing Apple's framework — cooperative, not coercive.
- [ ] Supervision distinguished from user enrollment by ownership and the privacy boundary.
- [ ] ADE zero-touch enrollment understood, with ABM/ASM as its supply-chain precondition.
- [ ] Declarative device management placed as the scalable, resilient modern direction.
