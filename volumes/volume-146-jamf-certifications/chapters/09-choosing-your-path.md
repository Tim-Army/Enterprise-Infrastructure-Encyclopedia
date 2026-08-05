# Chapter 09: Choosing Your Jamf Path

## Learning Objectives

- Sequence a Jamf certification path by role and track.
- Understand currency: what expires, what does not, and how to renew.
- Place Jamf certification in the Apple-in-enterprise career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to actually navigate the ladder [Chapter 1](01-the-jamf-certification-ladder.md) laid out.*

## Sequencing your path

The path follows the [track that matches your job](01-the-jamf-certification-ladder.md), climbed in order:

| You are | Start | Then | Then |
|:---|:---|:---|:---|
| **Corporate Apple admin** | Jamf 100 (Associate) | Jamf 200 (Tech) | Jamf 300 (Admin) → 400 (Expert) |
| **Education IT** | Jamf 140 (School Associate) | Jamf 240 (School Tech) | + Jamf Pro for depth |
| **Apple security / SOC** | Jamf 170 (Protect Associate) | Jamf 270 (Protect Tech) | Jamf 370 (Protect Admin) |
| **Full Apple-platform engineer** | Jamf 100 → 200 | + Jamf 170/270 (Protect) | + Connect integration |

The **Jamf 100 is nearly everyone's start** — self-paced, USD 100, non-expiring, and it grounds the Apple-management model the other tracks assume. From there you climb the ladder your job lives on, and the strongest Apple engineers **span Pro + Protect**: they manage the fleet *and* secure it, because on Apple those are two halves of one job.

The numbering is your map: leading digit = level (climb it), middle digit = track (pick yours). Do not treat Protect as "advanced Pro" — it is a *different* ladder for a *different* job, and a Pro Admin is not partway to a Protect cert.

## Currency

What expires and what does not is a real distinction from [Chapter 1](01-the-jamf-certification-ladder.md):

- **The Associate tier (100/140/170) does not expire.** Foundational knowledge of the Apple-management model does not go stale the way hands-on platform skills do.
- **Tech / Admin / Expert (200/300/400, 240, 270/370) carry a three-year validity.** The platform and Apple's framework move — macOS ships yearly, DDM advances, Jamf adds features — so the hands-on certifications renew to prove current skill.

The renewal discipline is the same as [every currency-sensitive program on this shelf](../../volume-047-oracle-certifications/README.md): the platform moving *under* a cert is exactly why the cert expires. Plan renewals into your three-year horizon, and treat the yearly macOS release as the drumbeat that keeps your knowledge — not just your certificate — current.

## The Apple-in-enterprise career

Jamf certification sits in a specific, growing niche: **Apple is no longer the exception in the enterprise.** Macs are a first-class corporate choice, iPads run point-of-sale and clinical and classroom workflows, and someone has to manage and secure them *well* — not as an afterthought on a Windows-first team. That someone is the Apple-management specialist, and Jamf is the platform they specialize in.

The career pairs naturally with adjacent skills this shelf covers:

- **[Microsoft Intune (XXXVII)](../../volume-037-microsoft-365-modern-work/README.md)** — the cross-platform generalist; many shops run Intune *and* Jamf, Jamf for Apple depth.
- **[Okta (LXXVI)](../../volume-076-okta-certifications/README.md) / identity** — Jamf Connect is the Apple side of the identity story.
- **[Endpoint security / SOC (Splunk XLV, CrowdStrike)](../../volume-045-splunk-certifications/README.md)** — Jamf Protect feeds the same defensive pipeline, Apple-specialized.

Jamf is the deep specialty on Apple in a world that increasingly runs Apple. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal Jamf plan. **Cost:** none.

### Lab 9.1 — Build your Jamf certification path

**Objective:** Generate a role-appropriate sequence with currency planning.

```bash
python3 - <<'EOF'
PATHS = {
  "corporate Apple admin": [
    ("Jamf 100", "Associate–Pro", "no expiry", "self-paced $100, the foundation"),
    ("Jamf 200", "Tech–Pro",      "3 years",   "instructor-led + practical tasks"),
    ("Jamf 300", "Admin–Pro",     "3 years",   "graded scenarios — judgment"),
    ("Jamf 400", "Expert–Pro",    "3 years",   "scenario-based — design/troubleshoot"),
  ],
  "education IT": [
    ("Jamf 140", "Associate–School", "no expiry", "self-paced, education foundation"),
    ("Jamf 240", "Tech–School",      "3 years",   "shared devices, classroom workflows"),
    ("Jamf 100", "Associate–Pro",    "no expiry", "optional: general Apple-mgmt depth"),
  ],
  "Apple security / SOC": [
    ("Jamf 170", "Associate–Protect", "no expiry", "self-paced, endpoint-security foundation"),
    ("Jamf 270", "Tech–Protect",      "3 years",   "telemetry, threat prevention"),
    ("Jamf 370", "Admin–Protect",     "3 years",   "compliance, SOC integration"),
  ],
}
import sys
role = "corporate Apple admin"   # change to taste
print(f"Jamf path for: {role}\n")
print(f"   {'step':10}{'certification':20}{'validity':>11}   note")
renew = []
for course, cert, val, note in PATHS[role]:
    print(f"   {course:10}{cert:20}{val:>11}   {note}")
    if val != "no expiry": renew.append(course)
print(f"\nrenewal planning: {', '.join(renew)} renew every 3 years")
print("   -> the Associate rung is permanent; the hands-on rungs track a moving")
print("      platform (yearly macOS, DDM, new Jamf features) and renew.")
print("\nGuidance:")
print("  - almost everyone starts at Jamf 100 (or 140/170) — cheap, self-paced, permanent")
print("  - climb the LEADING digit (level) within your track's MIDDLE digit")
print("  - the strongest Apple engineers add Protect (170/270) to their Pro path —")
print("    manage AND secure, the two halves of the Apple-platform job")
print("  - Jamf Connect isn't a separate cert ladder but IS integration knowledge the")
print("    Pro Admin needs (Chapter 6)")
print("\nSet the yearly macOS release as your currency drumbeat: when Apple ships a")
print("major version, your hands-on knowledge (not just your certificate) needs a")
print("refresh. Plan the 3-year renewals; let the OS cycle keep you actually current.")
EOF
```

**Expected result:** A role-specific certification sequence with each rung's validity and a renewal plan separating the permanent Associate tier from the three-year hands-on tier. The build-your-path lesson is the volume's practical close — start at the self-paced Associate, climb your track's ladder, add Protect for the full Apple-platform job, and treat the yearly macOS release as the currency drumbeat.

**Negative test:** Collecting certs across all three tracks at once without a role focus. The tracks are three jobs; depth in yours beats breadth across all three, and the ladder rewards climbing one track before spanning.

**Cleanup:** None.

### Lab 9.2 — Position Jamf in the Apple-in-enterprise career

**Objective:** Map Jamf skills to adjacent competencies for a rounded profile.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Jamf Pro",       "Apple device management (the core)",      "the specialty itself"),
  ("Intune (XXXVII)","cross-platform MDM generalist",           "many shops run BOTH — Jamf for Apple depth"),
  ("Okta (LXXVI)",   "cloud identity / SSO",                    "Jamf Connect is the Apple side of this"),
  ("Jamf Protect",   "Apple endpoint security",                 "the security half — pairs with SOC skills"),
  ("Splunk (XLV)",   "SIEM / detection engineering",            "where Protect telemetry lands"),
  ("CIS benchmarks", "compliance baselines",                    "the 'prove it' layer (Chapter 8)"),
]
print("Jamf in the Apple-in-enterprise skill map:\n")
print(f"   {'skill':18}{'domain':40}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:18}{domain:40}{why}")
print("\nThe career thesis: Apple is now a FIRST-CLASS enterprise platform (corporate")
print("Macs, iPad workflows in retail/health/education), and it needs specialists who")
print("go DEEPER than a cross-platform generalist can. That's the Jamf niche.")
print("\nThe rounded Apple-platform engineer combines:")
print("  MANAGE   (Jamf Pro)      — deploy, configure, patch the fleet")
print("  SECURE   (Jamf Protect)  — detect, prevent, monitor compliance")
print("  IDENTITY (Jamf Connect + Okta/Entra) — cloud identity at the Mac")
print("  PROVE    (CIS + SIEM)    — continuous compliance, telemetry to the SOC")
print("\nNone of these is exotic — they're the same management/identity/security/")
print("compliance pillars this whole shelf teaches, SPECIALIZED to Apple. Jamf is")
print("how you own the Apple corner of an enterprise that, increasingly, runs Apple.")
print("Start at Jamf 100, climb your track, and pair it with the identity and SOC")
print("skills the adjacent volumes cover — that's a career, not just a certificate.")
EOF
```

**Expected result:** Jamf skills mapped to adjacent competencies — Intune, Okta, Splunk, CIS — showing the rounded Apple-platform profile of manage, secure, identity, and prove. The career-positioning lesson closes the volume: Jamf is the deep Apple specialty in an enterprise that increasingly runs Apple, and it pairs with the same identity, security, and compliance pillars the rest of the shelf teaches.

**Negative test:** Treating Jamf as a niche skill with no adjacencies. It sits squarely in the management/identity/security/compliance story — isolating it from Intune, identity, and SOC skills undersells both the platform and the career.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Jamf path sequenced by role and track, climbing the leading digit within your track's middle digit.
- [ ] Currency understood — the permanent Associate tier versus the three-year hands-on tier, paced by the yearly macOS release.
- [ ] Jamf positioned in the Apple-in-enterprise career alongside Intune, identity, and SOC skills.
- [ ] The volume assembled into a personal study and career plan — manage, secure, identity, prove.
