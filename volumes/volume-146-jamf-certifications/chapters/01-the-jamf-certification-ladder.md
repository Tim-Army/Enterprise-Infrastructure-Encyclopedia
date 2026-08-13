# Chapter 01: The Jamf Certification Ladder

![The Jamf certification ladder across three product tracks. The Jamf Pro track for Apple device management runs Jamf 100 self-paced to Certified Associate, then instructor-led Jamf 200 to Certified Tech, Jamf 300 to Certified Admin, and Jamf 400 to Certified Expert. The Jamf School track for education runs Jamf 140 to Associate and Jamf 240 to Tech. The Jamf Protect track for Apple endpoint security runs Jamf 170 to Associate, Jamf 270 to Tech, and Jamf 370 to Admin. The exam format escalates with the level: Associate courses use multiple-choice questions, Tech courses add practical tasks, and Admin and Expert courses use graded scenarios and practical tasks. The Jamf 100 exam is one hundred US dollars, fifty multiple-choice questions, and the certification does not expire; the 200 through 400 certifications carry a three-year validity. The platform beneath is Jamf Pro for mobile device management on the Apple MDM framework, Jamf Connect for identity, Jamf Protect for endpoint security, and Jamf School for education, positioning Jamf as the Apple-in-enterprise specialist against the cross-platform generalists.](../../../diagrams/volume-146-jamf-certifications/chapter-01-certification-ladder.svg)

*Figure 1-1. Three product tracks, an ascending exam-format ladder, and the Apple-management platform beneath.*

## Learning Objectives

- Describe the Jamf certification ladder — the numbered courses and the certifications they lead to.
- Distinguish the three product tracks: Jamf Pro, Jamf School, Jamf Protect.
- Understand how the exam format escalates from recall to scenario judgment as you climb.
- Recognize Jamf's position as the Apple-in-enterprise specialist.

## What Jamf is

Jamf is the leader in **Apple enterprise management** — the platform organizations use to deploy, configure, secure, and support Mac, iPhone, iPad, and Apple TV at scale. Where [Microsoft Intune (XXXVII)](../../volume-037-microsoft-365-modern-work/README.md) is the cross-platform generalist managing Windows, Android, and Apple together, **Jamf is the Apple specialist** — it goes deeper on Apple's management framework than a generalist can, and that depth is its whole pitch and the subject of its certifications.

The distinction matters for the certifications too: they are not about managing devices in general, they are about managing *Apple* devices well, on Jamf's platform, following Apple's own management model.

## The certification ladder

Jamf's program is built on **numbered courses**, each culminating in a certification exam. The numbering encodes both level and track:

### Jamf Pro track (the flagship — device management)

| Course | Delivery | Certification | Format |
|:---|:---|:---|:---|
| **Jamf 100** | Self-paced | **Jamf Certified Associate – Jamf Pro** | Multiple choice |
| **Jamf 200** | Instructor-led | **Jamf Certified Tech – Jamf Pro** | Multiple choice + practical tasks |
| **Jamf 300** | Instructor-led | **Jamf Certified Admin – Jamf Pro** | Graded scenarios + practical tasks |
| **Jamf 400** | Instructor-led | **Jamf Certified Expert – Jamf Pro** | Scenario-based |

### Jamf School track (education)

| Course | Certification |
|:---|:---|
| **Jamf 140** (self-paced) | Certified Associate – Jamf School |
| **Jamf 240** (instructor-led) | Certified Tech – Jamf School |

### Jamf Protect track (Apple endpoint security)

| Course | Certification |
|:---|:---|
| **Jamf 170** (self-paced) | Certified Associate – Jamf Protect |
| **Jamf 270** (instructor-led) | Certified Tech – Jamf Protect |
| **Jamf 370** (instructor-led) | Certified Admin – Jamf Protect |

The **x00 numbering** is the mnemonic: 100/140/170 are the self-paced Associate on-ramps; 200/300/400 climb the Jamf Pro ladder; the middle digit marks the track (0 = Pro, 4 = School, 7 = Protect).

## The escalating exam format

The most instructive thing about Jamf's program is that **the exam format escalates with the level**, and it does so deliberately:

| Level | Format | Tests |
|:---|:---|:---|
| **Associate** (100/140/170) | Multiple choice | *Knowledge* — do you understand the concepts? |
| **Tech** (200/240/270) | Multiple choice **+ practical tasks** | *Can you do it* — perform real configuration |
| **Admin** (300/370) | **Graded scenarios** + practical tasks | *Judgment* — handle realistic situations |
| **Expert** (400) | **Scenario-based** | *Design and troubleshooting* — the hardest problems |

This is the same **practical-over-recall philosophy** [SAP is retrofitting across its whole program (CXLIV)](../../volume-144-sap-certifications/chapters/07-the-practical-exam-transition.md) — except Jamf built it into the ladder from the start. A multiple-choice Associate exam is fine for foundational knowledge; you would not certify someone as an Expert on multiple choice, because expertise is doing, not recalling. The format tells you what each level actually validates.

## What is published

Jamf publishes the ladder, the tracks, and the formats. The **Jamf 100 exam is the well-documented one**: USD 100, 50 multiple-choice questions, and — notably — the **Associate certification does not expire**, while the 200–400 certifications carry a **three-year validity**.

> **The published-versus-portal split, once more:** the 100-level specifics are public and stated here. Per-exam passing scores and exact durations for the instructor-led 200–400 courses vary and are not uniformly published; instructor-led course pricing is arranged rather than listed. This volume asserts the 100-level facts and points at the Jamf training portal for the rest.

## Hands-On Lab

The labs in this volume model Apple management concepts in Python at no cost — Jamf Pro is enterprise software, so the labs model the *decisions and disciplines* the certifications test. Jamf offers a **free trial** of Jamf Pro, and the self-paced Jamf 100 course is the standard free-ish on-ramp.

### Lab 1.1 — Read the ladder by track and format

**Objective:** Place a certification by track, level, and what its format tests.

```bash
python3 - <<'EOF'
CERTS = [
  # course, track,    level,       format,                          validity
  ("100",  "Pro",     "Associate", "multiple choice",               "no expiry"),
  ("200",  "Pro",     "Tech",      "MC + practical tasks",          "3 years"),
  ("300",  "Pro",     "Admin",     "graded scenarios + practical",  "3 years"),
  ("400",  "Pro",     "Expert",    "scenario-based",                "3 years"),
  ("140",  "School",  "Associate", "multiple choice",               "no expiry"),
  ("240",  "School",  "Tech",      "MC + practical tasks",          "3 years"),
  ("170",  "Protect", "Associate", "multiple choice",               "no expiry"),
  ("270",  "Protect", "Tech",      "MC + practical tasks",          "3 years"),
  ("370",  "Protect", "Admin",     "graded scenarios + practical",  "3 years"),
]
FORMAT_TESTS = {"multiple choice": "KNOWLEDGE (recall)",
                "MC + practical tasks": "CAN YOU DO IT (hands-on)",
                "graded scenarios + practical": "JUDGMENT (situations)",
                "scenario-based": "DESIGN + TROUBLESHOOTING"}
print(f"{'course':>7}{'track':>10}{'level':>11}{'validity':>11}   format tests")
for c, track, level, fmt, val in CERTS:
    print(f"{c:>7}{track:>10}{level:>11}{val:>11}   {FORMAT_TESTS[fmt]}")
print("\nTwo things to read from this:")
print("  1. The middle DIGIT is the track: x0x=Pro, x4x=School, x7x=Protect. The")
print("     leading digit (1/2/3/4) is the LEVEL. '370' = Protect Admin.")
print("  2. The FORMAT escalates with level, and it tells you what's validated:")
print("     Associate = recall, Tech = hands-on, Admin = judgment, Expert = design.")
print("\nYou would not certify an Expert on multiple choice — expertise is DOING, and")
print("the 400 exam is scenario-based for exactly that reason. The format is the")
print("honest signal of what each level means (same philosophy SAP is retrofitting,")
print("Vol CXLIV — Jamf built it in from the start).")
print("\nAlso note: the ASSOCIATE tier does not expire (foundational knowledge doesn't")
print("go stale the way hands-on platform skills do); Tech/Admin/Expert renew every")
print("3 years because the platform and Apple's framework move.")
EOF
```

**Expected result:** The nine certifications sorted by track (via middle digit) and level (via leading digit), with the format mapped to what it validates. The escalation is the lesson — recall → hands-on → judgment → design — and it is the honest signal of what each rung certifies, with the non-expiring Associate reflecting that foundational knowledge ages slower than platform skills.

**Negative test:** Assuming all Jamf exams are multiple choice like the 100. The Tech level adds practical tasks and the Admin/Expert levels are scenario-based — you cannot cram them from a question bank.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Choose a track by what you manage

**Objective:** Match the track to the job.

```bash
python3 - <<'EOF'
ROLES = [
  ("enterprise Mac/iPhone fleet admin",   "Pro",     "the flagship — general Apple device mgmt"),
  ("K-12 / university device manager",     "School",  "education-tailored MDM (shared iPads, etc.)"),
  ("Apple endpoint security / SOC",        "Protect", "threat prevention, compliance, telemetry"),
  ("does all three at a small org",        "Pro + Protect", "Pro for mgmt, Protect for security"),
]
print(f"{'role':38}{'track':>16}   why")
for role, track, why in ROLES:
    print(f"{role:38}{track:>16}   {why}")
print("\nThe three tracks are three JOBS, not three difficulty levels:")
print("  JAMF PRO     — device management: enrollment, config, policies, apps. The")
print("                 flagship; most Apple admins live here.")
print("  JAMF SCHOOL  — the same idea tailored to EDUCATION (shared devices, classroom")
print("                 workflows, student/teacher roles). A different sector, not a")
print("                 different difficulty.")
print("  JAMF PROTECT — SECURITY: this is the endpoint-security half (Chapter 07),")
print("                 the SOC/compliance job, not device configuration.")
print("\nStart in the track that matches your work. A corporate Apple admin starts")
print("Jamf Pro (100->200->300); a security engineer securing Macs starts Jamf")
print("Protect (170->270); an education IT person starts Jamf School (140->240).")
print("\nMany real Apple admins end up spanning Pro + Protect — you manage the fleet")
print("AND secure it — but you certify per track, one ladder at a time.")
EOF
```

**Expected result:** The three tracks mapped to three distinct jobs — device management, education, and security — rather than difficulty tiers. The choose-by-what-you-manage rule is the guidance, with the Pro+Protect span reflecting the common reality that Apple admins both manage and secure the fleet.

**Negative test:** Treating Jamf Protect as "advanced Jamf Pro." It is a different product (security, not management) with its own ladder; a Pro Admin is not partway to a Protect cert.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The numbered-course ladder read by leading digit (level) and middle digit (track).
- [ ] The three tracks (Pro, School, Protect) matched to three distinct jobs.
- [ ] The escalating exam format understood as the honest signal of what each level validates.
- [ ] The 100-level specifics ($100, 50 MC, no expiry) known; 200–400 mechanics identified as portal-gated.
