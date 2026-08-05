# Chapter 08: Jamf School and Compliance

## Learning Objectives

- Explain Jamf School — Apple management tailored to education.
- Understand shared-device and classroom workflows unique to education.
- Place compliance benchmarks (CIS macOS) as the baseline Jamf enforces.
- Recognize how management, security, and compliance compose into a posture.

*Cert relevance: Jamf School has its own ladder (**140/240**), and compliance underpins the **Jamf Pro 300** and **Protect 370** exams — the "prove it" layer over management and security.*

## Jamf School

**Jamf School** is Jamf's education-tailored management product — the same Apple-management foundation as Jamf Pro, shaped for schools. Its own certification ladder ([140/240](01-the-jamf-certification-ladder.md), Associate/Tech) reflects that it is a distinct product for a distinct sector, not merely "Jamf Pro for teachers."

Education has needs a corporate fleet does not:

- **Shared devices.** A cart of iPads used by different students each period — one device, many users, each getting their own environment and having it cleaned up for the next. This is genuinely different from the corporate one-device-one-user model.
- **Classroom workflows.** A teacher guiding devices during a lesson — focusing students on an app, viewing screens, locking devices to keep attention. Management in service of *teaching*, not just IT control.
- **Student/teacher roles and simplicity.** Non-technical teachers must operate it; the tooling is deliberately simpler than Jamf Pro's full surface.

The lab models the shared-device workflow, because it is the clearest example of education needing a different model, not just a different logo.

## Compliance and the CIS benchmark

Underneath both the corporate and education stories sits **compliance** — proving and maintaining that devices meet a security baseline. The standard benchmark for macOS is the **CIS (Center for Internet Security) macOS Benchmark**: a published, consensus set of security settings (FileVault on, firewall on, secure screen-lock, disabled guest account, and dozens more) that define a hardened Mac.

Jamf's role in compliance is the composition of everything in this volume:

- [Configuration profiles (Chapter 4)](04-configuration-profiles-and-patch-management.md) *set* the hardened state.
- [Smart Groups and scope (Chapter 3)](03-jamf-pro-smart-groups-and-scope.md) *target* remediation at drifting devices.
- [Jamf Protect (Chapter 7)](07-jamf-protect-endpoint-security.md) *continuously measures* against the benchmark and reports drift.

Compliance is where **management + security + measurement** become one posture: the profiles enforce the baseline, the Smart Groups catch drift, and the monitoring proves it — continuously, not at audit time. The lab models mapping a CIS benchmark to Jamf mechanisms.

## Hands-On Lab

Python models education and compliance workflows. **Cost:** none.

### Lab 8.1 — Shared-device workflow: one iPad, many students

**Objective:** Model the education-specific shared-device lifecycle.

```bash
python3 - <<'EOF'
# a cart iPad cycles through students across the school day
class SharedCart:
    def __init__(self, name): self.name=name; self.user=None; self.data=[]
    def check_out(self, student, apps):
        self.user = student
        self.data = list(apps)      # student's assignment/session set up
        print(f"   period start: {student:8} checks out {self.name} -> apps {apps}")
    def check_in(self):
        who = self.user
        self.user=None; self.data=[]  # session cleaned for the next student
        print(f"   period end:   {who:8} returns {self.name} -> WIPED CLEAN for next user")

ipad = SharedCart("ipad-cart-07")
print("ONE iPad, a full school day of different students (shared-device model):\n")
schedule = [("Ava",  ["Math", "Reader"]),
            ("Ben",  ["Science", "Sketch"]),
            ("Chen", ["History", "Reader"])]
for student, apps in schedule:
    ipad.check_out(student, apps)
    ipad.check_in()
print("\nWhy this needs a DIFFERENT model from corporate (one-device-one-user):")
print("  - each student gets THEIR OWN environment on the SAME hardware, then it's")
print("    cleaned for the next — no data bleed between students")
print("  - the device is OWNED by the school, SHARED by many; corporate assumes a")
print("    device belongs to one person indefinitely")
print("  - it's a per-PERIOD lifecycle (minutes/hours), not a per-EMPLOYEE one (years)")
print("\nJamf School models this natively: shared iPad carts, per-student sessions,")
print("automatic cleanup. Trying to force the corporate one-user model onto a")
print("classroom cart is the mismatch Jamf School exists to fix — same Apple")
print("foundation (Chapter 2), a sector-specific workflow on top. This is why")
print("education gets its OWN product and ladder (140/240), not a Jamf Pro setting.")
EOF
```

**Expected result:** An iPad cycling through students with per-period checkout and cleanup, each getting an isolated environment on shared hardware. The shared-device lesson is why education needs its own model — a per-period, one-device-many-users lifecycle that the corporate one-device-one-user assumption cannot express, which is why Jamf School is a distinct product and ladder.

**Negative test:** Managing a classroom iPad cart with the corporate one-device-one-user model. It has no concept of per-period student sessions or between-user cleanup; student data bleeds across periods where Jamf School isolates it.

**Cleanup:** None.

### Lab 8.2 — Map a CIS benchmark to Jamf mechanisms

**Objective:** Compose profiles, Smart Groups, and monitoring into a compliance posture.

```bash
python3 - <<'EOF'
# CIS macOS-style controls and how each maps to a Jamf mechanism
CONTROLS = [
  # control,               how Jamf ENFORCES,                 how Jamf MEASURES
  ("FileVault enabled",    "config profile (FileVault payload)", "Protect/ext-attr check -> Smart Group"),
  ("firewall on",          "config profile (firewall payload)",  "ext-attr check -> Smart Group"),
  ("Gatekeeper on",        "config profile / policy",            "Protect telemetry + ext-attr"),
  ("auto-updates on",      "config profile (SoftwareUpdate)",    "inventory + Smart Group"),
  ("screen-lock <= 5 min", "config profile (passcode payload)",  "profile presence + ext-attr"),
  ("guest account off",    "config profile (login window)",      "ext-attr check -> Smart Group"),
]
print("CIS macOS baseline -> Jamf mechanisms (ENFORCE + MEASURE):\n")
print(f"   {'control':22}{'enforce with':36}measure with")
for ctrl, enforce, measure in CONTROLS:
    print(f"   {ctrl:22}{enforce:36}{measure}")
print("\nEvery control decomposes into TWO Jamf jobs:")
print("  ENFORCE — a configuration PROFILE sets the hardened state and MAINTAINS it")
print("            (declarative; reverts drift automatically — Chapter 4).")
print("  MEASURE — an extension attribute / Jamf Protect check reports the actual")
print("            state, feeding a Smart Group of NON-COMPLIANT devices (Ch 3, 7).")
print("\nThe posture is the COMPOSITION of the whole volume:")
print("  profiles (Ch4) SET the baseline -> Smart Groups (Ch3) TARGET the drift ->")
print("  Protect (Ch7) MEASURES continuously -> remediation policies self-clear it.")
print("\nCompliance is not a document you write once — it's management + security +")
print("continuous measurement composed into one LIVE posture. That composition is")
print("what the 300/370 exams test: not any single mechanism, but wiring them")
print("together so 'CIS-compliant' is a number you hold up and MAINTAIN, not claim.")
EOF
```

**Expected result:** Each CIS control decomposed into a Jamf enforcement mechanism (a configuration profile) and a measurement mechanism (an extension attribute or Protect check feeding a Smart Group). The compliance-as-composition lesson is the volume's synthesis — profiles set the baseline, Smart Groups target drift, and Protect measures continuously, wiring management plus security plus measurement into one live posture.

**Negative test:** Enforcing a benchmark with profiles but never measuring compliance. You set the baseline but cannot prove it holds — drift goes unseen, and "we're CIS-compliant" is a claim, not a number.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Jamf School understood as education-tailored management with its own ladder — shared devices and classroom workflows.
- [ ] The shared-device lifecycle recognized as a genuinely different model from corporate one-device-one-user.
- [ ] The CIS macOS benchmark placed as the compliance baseline Jamf enforces and measures.
- [ ] Compliance understood as the composition of profiles, Smart Groups, and continuous monitoring into one live posture.
