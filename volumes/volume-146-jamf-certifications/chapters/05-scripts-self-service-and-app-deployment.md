# Chapter 05: Scripts, Self Service, and App Deployment

## Learning Objectives

- Understand how scripts extend Jamf beyond built-in actions.
- Explain Self Service — the user-initiated app and workflow catalog.
- Distinguish app deployment models: managed apps, VPP/ABM, and installers.
- Recognize when to automate silently versus offer a choice through Self Service.

*Cert relevance: Self Service and app deployment are day-to-day **Jamf 200/300** administration — how software and workflows actually reach users.*

## Scripts

Jamf's built-in policy actions cover the common cases, but the real world needs more, and **scripts** are the escape hatch: a policy can run a shell (or Python) script on the device to do whatever the built-ins do not — remediate a specific condition, reconfigure an app, collect a fact. Scripts are also how [extension attributes](03-jamf-pro-smart-groups-and-scope.md) collect custom inventory.

The discipline is the same as any fleet automation: **a script runs on every device in scope, so a bad script breaks every device in scope.** Test on a pilot group before broad deployment — the blast-radius lesson from [Chapter 3's scoping](03-jamf-pro-smart-groups-and-scope.md) applies doubly to scripts, because a script can do anything, not just what an Apple profile permits.

## Self Service

**Self Service** is Jamf's app-store-like catalog on the managed device: a branded app where users can *choose* to install software, run workflows (fix printing, reset a setting), and access resources — on demand, without a ticket. It inverts the usual push model: instead of IT deciding and pushing everything, IT *publishes* options and users pull what they need.

The judgment Self Service demands is **push versus offer**:

- **Push (silent, mandatory)** for what everyone must have — the security agent, required configuration, critical updates. No choice; it just happens.
- **Offer (Self Service, optional)** for what *some* users want — a design tool, a language pack, an optional VPN profile, a self-heal workflow. A choice, on demand.

Getting this line right is a real admin skill: push too much and you bloat every device and annoy users; offer too much (or offer the mandatory) and critical software does not land. The lab models the split.

## App deployment models

Apps reach devices several ways, and knowing which to use is exam material:

| Model | Is | Use for |
|:---|:---|:---|
| **Managed App Store apps (VPP via ABM)** | App Store apps bought/assigned through Apple Business Manager, installed and managed by Jamf | Most commercial apps — licensed, updatable, removable |
| **Jamf-deployed packages (.pkg)** | Installer packages Jamf pushes via policy | Non-App-Store software, custom installers |
| **Self Service items** | Either of the above, offered rather than pushed | Optional software users choose |

**VPP (Volume Purchase Program) through ABM** is the clean path for App Store software: licenses are managed centrally, apps install without an Apple ID on the device, and they are removable and updatable as managed apps. Custom or non-App-Store software goes through **packages**. Either can be pushed or placed in Self Service. The [ABM supply-chain](02-apple-management-fundamentals.md) point from Chapter 2 extends here: ABM is not just device enrollment, it is also how you license and distribute apps at scale.

## Hands-On Lab

Python models deployment decisions. **Cost:** none.

### Lab 5.1 — Push versus offer: the Self Service line

**Objective:** Sort software into mandatory-push and optional-offer.

```bash
python3 - <<'EOF'
SOFTWARE = [
  # name,                everyone_needs, why
  ("security agent",         True,  "mandatory — compliance; no opt-out"),
  ("device config profile",  True,  "mandatory — Wi-Fi/VPN/restrictions"),
  ("critical OS patch",      True,  "mandatory — closes a CVE"),
  ("company VPN (required)", True,  "mandatory for the role"),
  ("Photoshop",              False, "some designers want it; most don't"),
  ("Slack",                  False, "most want it, but let them pull it"),
  ("Xcode (14 GB)",          False, "developers only — pushing to all wastes 14GB each"),
  ("printer-fix workflow",   False, "on-demand self-heal; run when needed"),
  ("optional language pack", False, "a minority need it"),
]
push, offer = [], []
for name, mand, why in SOFTWARE:
    (push if mand else offer).append((name, why))
print("PUSH (silent, mandatory) — everyone must have it, no choice:")
for name, why in push:
    print(f"   [PUSH]  {name:24} {why}")
print("\nOFFER (Self Service, optional) — publish it, users PULL what they need:")
for name, why in offer:
    print(f"   [OFFER] {name:24} {why}")
print("\nThe line the exam tests:")
print("  PUSH what EVERYONE must have (security, config, critical patches) — silent,")
print("       mandatory, no opt-out. It just happens.")
print("  OFFER what SOME want (optional apps, big installs, self-heal workflows) via")
print("       Self Service — a catalog users pull from on demand, no ticket.")
print("\nTwo failure modes:")
print("  push too much  -> every device bloated (14GB Xcode on non-developers),")
print("                    users annoyed, bandwidth wasted")
print("  offer the mandatory -> critical software doesn't land; you can't 'offer'")
print("                    a security agent and hope users install it")
print("\nSelf Service INVERTS the push model for optional software: IT publishes")
print("choices, users pull. It cuts tickets and respects that not everyone needs")
print("everything — but the MANDATORY set is never optional.")
EOF
```

**Expected result:** Mandatory software (security, config, critical patches) sorted to silent push and optional software (big or minority-need apps, self-heal workflows) to Self Service. The push-versus-offer line is the admin skill — push what everyone must have, offer what some want, and the two failure modes are pushing too much (bloat) or offering the mandatory (critical software never lands).

**Negative test:** Putting the security agent in Self Service as an optional install. It is mandatory; offering it means the devices that most need it are the ones whose users never install it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Test scripts on a pilot before fleet-wide

**Objective:** Model the blast radius of a script deployed without piloting.

```bash
python3 - <<'EOF'
FLEET = 3000
print(f"Deploy a remediation script to {FLEET} Macs. The script has a bug on")
print("machines with a non-default disk layout (~4% of the fleet) — it fails there.\n")
bad_fraction = 0.04

print("STRAIGHT TO FLEET (no pilot):")
broken = int(FLEET * bad_fraction)
print(f"   script runs on all {FLEET} -> {broken} devices hit the bug and break")
print(f"   {broken} simultaneous breakages = a flood of tickets, a bad day, a rollback\n")

print("PILOT FIRST (scope to a 50-device pilot Smart Group):")
pilot = 50
pilot_broken = round(pilot * bad_fraction)
print(f"   script runs on {pilot} pilot devices -> ~{pilot_broken} break")
print(f"   you SEE the failure on {pilot_broken} device(s), fix the script, THEN go wide")
print(f"   fleet impact of the bug: {pilot_broken}, not {broken}")
print(f"\n   avoided breakages: {broken - pilot_broken}")
print("\nA script can do ANYTHING on the device — unlike a configuration profile, it")
print("isn't bounded by Apple's framework. That power is why the blast-radius")
print("discipline matters DOUBLE for scripts:")
print("  1. scope to a PILOT Smart Group first, watch it, then widen")
print("  2. make scripts idempotent and defensive (check before you change)")
print("  3. a bad script scoped to the fleet breaks the fleet — at check-in speed")
print("\nSame lesson as pre-flighting a destructive policy scope (Chapter 3), sharper:")
print("the profile is limited to Apple-sanctioned settings; the script is limited")
print("only by what you wrote. Pilot it.")
EOF
```

**Expected result:** A buggy script breaking over a hundred devices fleet-wide versus one or two on a scoped pilot. The pilot-first discipline is the lesson, sharper for scripts than profiles — a script can do anything on the device, so a bad one scoped to the fleet breaks the fleet, and piloting on a small Smart Group contains the blast radius.

**Negative test:** Deploying an untested script straight to the fleet because it "worked on my machine." The 4% with a different disk layout break simultaneously — a pilot would have surfaced the bug on one or two devices instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Pick the app-deployment model

**Objective:** Match software to VPP, package, or Self Service.

```bash
python3 - <<'EOF'
APPS = [
  # app,                 app_store?, mandatory?,  best model
  ("Slack",              True,  False, "VPP via ABM, in Self Service (App Store, optional)"),
  ("company security agent", False, True,  "package (.pkg) pushed by policy (not App Store, mandatory)"),
  ("Microsoft Office",   True,  True,  "VPP via ABM, pushed (App Store, everyone)"),
  ("in-house tool",      False, False, "package in Self Service (custom, optional)"),
  ("Xcode",              True,  False, "VPP via ABM, in Self Service (App Store, big, dev-only)"),
]
print(f"{'app':24}{'store?':>8}{'mandatory?':>12}   deployment model")
for app, store, mand, model in APPS:
    print(f"{app:24}{('yes' if store else 'no'):>8}{('yes' if mand else 'no'):>12}   {model}")
print("\nTwo axes decide the model:")
print("  App Store or not?  ->  App Store: VPP via ABM (managed, no Apple ID needed,")
print("                          licensed centrally, removable/updatable).")
print("                          Not App Store: a .pkg pushed by policy.")
print("  Mandatory or not?  ->  Mandatory: PUSH it. Optional: put it in SELF SERVICE.")
print("\nThese combine: 'Office' = App Store + mandatory = VPP, pushed. 'in-house tool'")
print("= custom + optional = package, in Self Service. The delivery mechanism (VPP vs")
print("package) and the delivery MODE (push vs Self Service) are independent choices.")
print("\nVPP through ABM is the clean path for App Store apps — the same Apple Business")
print("Manager that supplies zero-touch enrollment (Chapter 2) also licenses and")
print("distributes apps. That's why getting purchasing into ABM pays off twice:")
print("devices self-enroll AND apps deploy as managed, license-tracked, removable.")
EOF
```

**Expected result:** Apps sorted by two independent axes — App Store (VPP via ABM) versus custom (package), and mandatory (push) versus optional (Self Service). The pick-the-model lesson is that delivery mechanism and delivery mode are separate choices, and ABM pays off twice as both the enrollment and the app-licensing supply chain.

**Negative test:** Treating "push versus Self Service" and "VPP versus package" as the same choice. They are independent — an App Store app can be pushed or offered, and a custom package can be pushed or offered; you decide both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Scripts understood as the escape hatch beyond built-in actions — with doubled blast-radius discipline and mandatory piloting.
- [ ] Self Service understood as the user-pull catalog, with the push-versus-offer line drawn correctly.
- [ ] App-deployment models (VPP via ABM, packages, Self Service) matched by the App-Store and mandatory axes.
- [ ] ABM recognized as both the enrollment and the app-licensing supply chain.
