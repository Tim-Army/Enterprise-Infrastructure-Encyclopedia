# Chapter 04: Configuration Profiles and Patch Management

## Learning Objectives

- Explain configuration profiles — the declarative unit of Apple settings management.
- Distinguish profiles (settings) from policies (actions).
- Understand patch management: keeping apps and the OS current across the fleet.
- Recognize the update-enforcement realities Apple's framework imposes.

*Cert relevance: configuration profiles and patching are core **Jamf 200/300** material — the two mechanisms that keep a fleet configured and current.*

## Profiles versus policies

Jamf has two distinct mechanisms, and confusing them is a classic beginner error:

| | **Configuration profile** | **Policy** |
|:---|:---|:---|
| Is a | *Settings* payload (declarative) | *Action* to run (imperative) |
| Expresses | Desired state — "Wi-Fi should be configured thus, FileVault on" | A task — "install this package, run this script" |
| Enforced by | The device maintains it continuously | Runs at a trigger (enrollment, check-in, schedule) |
| Reverts on | Profile removal (setting reverts) | Nothing — an action already happened |

A **configuration profile** is a bundle of settings — Wi-Fi, VPN, restrictions, certificates, FileVault, passcode requirements — that the device applies and *maintains*. It is declarative: while the profile is installed, the setting holds; remove the profile and the setting reverts. A **policy** is an action — install a package, run a script, set a printer — that fires at a trigger and is done.

The rule of thumb: **profiles for settings, policies for actions.** Want Wi-Fi configured? Profile. Want an app installed? Policy (or an app deployment). Want a restriction enforced continuously? Profile — because you need it *maintained*, not run once.

## Patch management

**Patch management** is keeping the fleet's software current — both third-party apps (browsers, productivity tools) and macOS itself. It is one of the highest-value things a management platform does, because *unpatched software is how fleets get compromised*, and doing it by hand across thousands of devices is impossible.

Jamf's patch management tracks available versions, reports which devices are behind, and deploys updates — ideally scoped to a Smart Group of "devices not on the latest version" so remediation is automatic and self-clearing (the [Chapter 3](03-jamf-pro-smart-groups-and-scope.md) pattern). The discipline the labs model: **patch compliance is a live number, and the gap between "released" and "installed" is the risk window.**

## The OS-update reality

Here Apple's cooperative framework bites in a way admins must understand: **you cannot silently force a major macOS upgrade the way you might push a Windows update.** Apple's model requires user interaction for many OS updates, especially on unsupervised devices, and supervised devices get more enforcement power (deferrals, scheduled installs, deadlines) but still within Apple's rules. The lab models the honest version: **you enforce updates by managing deadlines and deferrals, not by silent remote force** — and the compliance curve reflects users acting within the window you set.

This is the [cooperative-not-coercive](02-apple-management-fundamentals.md) principle applied to patching: you set the policy and the deadline, the framework nudges the user, and supervision determines how hard you can nudge. An admin who plans for this (realistic deadlines, good communication) succeeds; one who expects a silent-force button is surprised.

## Hands-On Lab

Python models profile and patch mechanics. **Cost:** none.

### Lab 4.1 — Profiles maintain state; policies are one-shot actions

**Objective:** See the declarative-versus-imperative distinction in behavior.

```bash
python3 - <<'EOF'
# A device's settings, and what happens under profile vs policy management
class Device:
    def __init__(self):
        self.wifi_configured = False
        self.app_installed = False
    def apply_profile(self, on): self.wifi_configured = on   # maintained
    def run_policy(self):        self.app_installed = True    # one-shot

d = Device()
print("PROFILE (settings, declarative): configure Wi-Fi")
d.apply_profile(True)
print(f"   profile installed -> wifi_configured = {d.wifi_configured}")
# user tampers / setting drifts -> device RE-ENFORCES from the profile
d.wifi_configured = False
d.apply_profile(True)   # device maintains the declared state
print(f"   user cleared it, device re-applies -> wifi_configured = {d.wifi_configured}")
print("   REMOVE the profile -> setting REVERTS:")
d.wifi_configured = False
print(f"   profile removed -> wifi_configured = {d.wifi_configured}  (gone with the profile)\n")

print("POLICY (action, imperative): install an app")
d.run_policy()
print(f"   policy ran -> app_installed = {d.app_installed}")
print("   'remove the policy' does NOT uninstall the app — the ACTION already happened.")
print(f"   removing the policy -> app_installed = {d.app_installed}  (still there)\n")

print("The distinction the 200 exam tests:")
print("  PROFILE = settings the device MAINTAINS; tied to the profile's presence,")
print("            reverts when removed, re-enforced if it drifts. Declarative.")
print("  POLICY  = an ACTION at a trigger; done once, not 'maintained', not reverted")
print("            by removing the policy. Imperative.")
print("\nRule of thumb: settings -> profile, actions -> policy. Want it MAINTAINED")
print("(a restriction, Wi-Fi, FileVault)? Profile. Want it DONE (install, script)?")
print("Policy. Same declarative-vs-imperative split as DDM vs old MDM (Chapter 2).")
EOF
```

**Expected result:** A profile maintaining and re-enforcing a setting that reverts when removed, versus a policy whose one-shot action persists after the policy is gone. The profiles-for-settings, policies-for-actions rule is the lesson — the same declarative-versus-imperative split as DDM versus old MDM, and confusing the two is the classic beginner error.

**Negative test:** Using a policy to "enforce" a setting. It runs once at a trigger and does not maintain the setting — drift goes uncorrected until the policy happens to run again, where a profile would hold it continuously.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Patch compliance is a live risk number

**Objective:** Quantify the gap between released and installed as a risk window.

```bash
python3 - <<'EOF'
import random
random.seed(9)
FLEET = 1500
# a critical browser CVE is patched in version 128; how fast does the fleet converge?
versions = {}
for i in range(FLEET):
    # before management: versions scattered, many behind
    versions[i] = random.choice([124,125,126,127,128,128,128])
def compliant(v): return v >= 128
def report(label):
    n = sum(1 for v in versions.values() if compliant(v))
    pct = 100*n/FLEET
    exposed = FLEET - n
    print(f"   {label:26} {pct:5.1f}% patched   {exposed:4} devices EXPOSED to the CVE")
    return pct

print(f"Critical CVE patched in v128. Fleet of {FLEET} devices.\n")
print("WITHOUT managed patching (hope users update):")
report("day 0 (disclosure)")
# organic updates: slow, incomplete — many users never update
for i in versions:
    if not compliant(versions[i]) and random.random() < 0.25:
        versions[i] = 128
report("day 14 (organic drift)")
print("   -> a long tail NEVER updates; the exposure window stays open for weeks\n")

# reset, this time with a managed patch policy scoped to 'version < 128'
for i in range(FLEET):
    versions[i] = random.choice([124,125,126,127,128,128,128])
print("WITH a managed patch policy (Smart Group 'version < 128' -> deploy v128):")
report("day 0 (disclosure)")
for i in versions:
    if not compliant(versions[i]) and random.random() < 0.85:
        versions[i] = 128   # policy reaches most devices at next check-in
report("day 2 (policy deployed)")
for i in versions:
    if not compliant(versions[i]) and random.random() < 0.85:
        versions[i] = 128
final = report("day 4 (stragglers caught)")
print(f"\n   -> {final:.0f}% patched in DAYS, not weeks; the Smart Group is self-clearing")
print("      (devices leave 'version < 128' as they update — no manual tracking)")
print("\nPatch compliance is a LIVE RISK NUMBER: every unpatched device is exposure,")
print("and the gap between 'released' and 'installed' is the window attackers use.")
print("Managed patching closes it in days and clears its own target group; hoping")
print("users update leaves a long tail open for weeks. This is the highest-value")
print("routine thing Jamf does, and why the exams weight it.")
EOF
```

**Expected result:** Managed patching converging the fleet to compliance in days via a self-clearing Smart Group, versus organic updates leaving a long exposed tail for weeks. The patch-compliance-as-live-risk framing is the lesson — the released-to-installed gap is the attacker's window, and scoped patch policies close it automatically where hoping-users-update does not.

**Negative test:** Relying on users to update after a CVE disclosure. A quarter update in two weeks and a long tail never does — the exposure window stays open exactly where managed patching would have closed it in days.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — You enforce OS updates by deadlines, not silent force

**Objective:** Model realistic macOS-update enforcement under Apple's rules.

```bash
python3 - <<'EOF'
import random
random.seed(3)
FLEET = 800
print("Enforce macOS 15 across the fleet. Apple's framework: NO silent major-OS")
print("force on most devices — you set a DEADLINE and DEFERRALS; users act within it.\n")

# model: each day some fraction of not-yet-updated users update, rising as the deadline nears
DEADLINE_DAY = 14
updated = 0
print(f"policy: 'update to macOS 15 by day {DEADLINE_DAY}', reminders escalate near the deadline")
print(f"   {'day':>4}{'updated':>10}{'compliance':>12}   note")
day_data = [(1,0.06,''), (4,0.10,'early adopters'), (8,0.14,'reminders escalate'),
            (12,0.22,'deadline approaching'), (14,0.55,'DEADLINE — forced install prompt'),
            (16,0.80,'past deadline — supervised devices auto-install')]
remaining = FLEET
for day, rate, note in day_data:
    n = int(remaining * rate) if day < 14 else int(remaining * rate)
    updated += n
    remaining = FLEET - updated
    print(f"   {day:>4}{updated:>10}{100*updated/FLEET:>11.0f}%   {note}")
print(f"\nfinal: {100*updated/FLEET:.0f}% on macOS 15; the last few need hands-on follow-up")
print("\nThe enforcement reality Apple imposes (and the 300 exam tests):")
print("  - you CANNOT silently push a major OS upgrade to most devices — the user")
print("    must interact. You manage the DEADLINE and DEFERRAL window, not a force button.")
print("  - SUPERVISED (org-owned) devices give you more teeth: enforced deadlines,")
print("    scheduled installs, deferral limits. UNSUPERVISED (BYOD) gives you less.")
print("  - the compliance curve is USERS ACTING within the window you set, steepening")
print("    as the deadline nears — plan realistic deadlines and communicate them.")
print("\nAn admin who expects 'push update, done' is surprised; one who plans deadlines,")
print("deferrals, and comms succeeds. This is cooperative-not-coercive (Chapter 2)")
print("applied to patching — the framework nudges, supervision sets how hard.")
EOF
```

**Expected result:** An OS-update compliance curve driven by deadline and deferral management, steepening as the deadline nears rather than jumping to 100% on a silent push. The enforce-by-deadlines lesson is the point — Apple's framework requires user interaction for major OS updates, supervision sets how hard you can nudge, and planning deadlines beats expecting a silent-force button.

**Negative test:** Scheduling a major macOS upgrade as a silent forced push. Apple's framework requires user interaction on most devices; the "force" does not fire silently, and an admin who planned around it is caught short at the deadline.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Configuration profiles understood as maintained, declarative settings — reverting on removal.
- [ ] Policies distinguished as one-shot actions at a trigger — the profiles-for-settings rule internalized.
- [ ] Patch management treated as a live risk number, closed by scoped, self-clearing policies.
- [ ] OS-update enforcement understood as deadline-and-deferral management within Apple's cooperative framework.
