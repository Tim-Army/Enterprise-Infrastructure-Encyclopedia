# Chapter 01: The Pega Certification Program

![The Pega Academy certification program and the Pega Platform beneath it. Pega offers certifications across several tracks on the Pega Infinity 25 version. The System Architect ladder is the flagship developer path: Certified Pega System Architect validates foundational app-building in App Studio and Dev Studio; Certified Pega Senior System Architect, requiring the System Architect credential, validates designing for reusability across multiple business lines; and Certified Pega Lead System Architect, requiring the Senior credential, is the expert tier earned through a two-part process of a written Architecture Exam plus a hands-on Application Exam that designs and builds a real application. The Business Architect track has the Certified Pega Business Architect for capturing business requirements. The decisioning track has the Certified Pega Data Scientist, the Certified Pega Decisioning Consultant for Customer Decision Hub, and the interview-based Lead Decisioning Architect. The Robotics track has the Certified Pega Robotics System Architect. The platform beneath is Pega Platform, a low-code, model-driven platform where everything is a rule, spanning case management, the situational layer cake for reuse, model-driven UI, Next-Best-Action decisioning, and robotics.](../../../diagrams/volume-164-pega-certifications/chapter-01-program.svg)

*Figure 1-1. The Pega certification tracks and the low-code Pega Platform they validate.*

## Learning Objectives

- Describe the Pega certification tracks and the System Architect ladder.
- Understand the CSA → CSSA → CLSA progression and prerequisites.
- Recognize the two-part Lead System Architect exam.
- Place the Pega Platform and Pega's position as a low-code leader.

## What Pega is

Pega (Pegasystems) is a leader in **low-code** enterprise software — a platform for **business process management (BPM) and case management**, **customer engagement (CRM)**, and **AI-driven decisioning**. Its distinctive approach is **model-driven development**: rather than hand-coding, you **model** an application visually and Pega generates it, so business and IT can build together and adapt quickly ([Chapter 2](02-the-pega-platform.md)). Pega is used by large enterprises to automate complex work — loan origination, customer service, claims — as **cases**. It sits alongside the other enterprise-platform and automation vendors this shelf covers ([ServiceNow LXXX](../../volume-080-servicenow-certifications/README.md), [Salesforce LXXXIII](../../volume-083-salesforce-certifications/README.md), [UiPath CXLIX](../../volume-149-uipath-certifications/README.md)). The lab models the program.

## The certification tracks

**Pega Academy** runs the certification program across several **tracks**, all on the **Pega Infinity '25** version:

| Track | Certifications |
|:---|:---|
| **System Architect** (developer) | Certified System Architect (CSA) → Senior (CSSA) → Lead (CLSA) |
| **Business Architect** | Certified Pega Business Architect (CPBA) |
| **Decisioning / AI** | Certified Data Scientist · Decisioning Consultant (CPDC) · Lead Decisioning Architect |
| **Robotics** | Certified Pega Robotics System Architect |

The **System Architect** track is the flagship developer path; the **Business Architect** track serves the business-analysis role; the **Decisioning** track covers Pega's [AI decisioning (Ch 6)](06-decisioning-and-next-best-action.md); and **Robotics** covers [RPA (Ch 7)](07-robotics-and-genai.md). You certify for the role you perform. The lab maps the tracks.

## The System Architect ladder

The **System Architect ladder** is a **prerequisite-gated** progression — you climb it in order:

- **Certified Pega System Architect (CSA)** — the **foundation**, no prerequisite: building Pega applications in **App Studio and Dev Studio**.
- **Certified Pega Senior System Architect (CSSA)** — requires **CSA**: designing and building for **reusability across multiple business lines** ([the situational layer cake, Ch 5](05-reusability-and-layer-cake.md)).
- **Certified Pega Lead System Architect (CLSA)** — requires **CSSA**: the **expert/elite** tier.

Each rung requires the one below, so you build genuine, cumulative capability. The lab models the ladder.

## The two-part Lead System Architect exam

The **CLSA** is distinctive: rather than a single written test, it is a **two-part** process — a **written Architecture Exam** *and* a **hands-on Application Exam** where you **design and build a real application** on the Pega Platform. This **prove-you-can-build-it** model (like the practical exams the [OffSec volume, XLIII](../../volume-043-offensive-security-certifications/README.md) uses, but for low-code enterprise development) makes the CLSA a strong signal of real architectural skill — you demonstrate design *and* implementation, not just recall. This is the top of the ladder and the elite Pega credential. The lab models the format.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the tracks and the System Architect ladder

**Objective:** Represent the tracks and the prerequisite-gated ladder.

```bash
python3 - <<'EOF'
TRACKS = {
  "System Architect (developer)": [
    ("Certified System Architect (CSA)", None,   "foundational: build apps in App Studio + Dev Studio"),
    ("Certified Senior System Architect (CSSA)", "CSA",  "design/build for REUSABILITY across business lines"),
    ("Certified Lead System Architect (CLSA)", "CSSA", "EXPERT: 2-part written Architecture + hands-on Build exam"),
  ],
  "Business Architect": [("Certified Pega Business Architect (CPBA)", None, "capture business requirements")],
  "Decisioning / AI": [
    ("Certified Pega Data Scientist", None, "Next-Best-Action + predictive analytics"),
    ("Certified Pega Decisioning Consultant (CPDC)", None, "Decision Management + Customer Decision Hub"),
    ("Certified Lead Decisioning Architect", "CPDC + Data Scientist", "expert (two-phase INTERVIEW)"),
  ],
  "Robotics": [("Certified Pega Robotics System Architect", None, "robotic automation, Robot Studio")],
}
print("Pega Academy certifications (Pega Infinity '25) — by track:\n")
for track, certs in TRACKS.items():
    print(f"   {track}:")
    for name, prereq, what in certs:
        pre = f"  [prereq: {prereq}]" if prereq else ""
        print(f"      - {name}{pre}")
        print(f"          {what}")
    print()
print("The flagship SYSTEM ARCHITECT ladder is PREREQUISITE-GATED: CSA -> CSSA (needs CSA) ->")
print("CLSA (needs CSSA). ★ CLSA is TWO-PART: a written ARCHITECTURE exam + a hands-on APPLICATION")
print("exam where you DESIGN + BUILD a real app — prove-you-can-build-it, not recall. Other tracks:")
print("BUSINESS ARCHITECT (requirements), DECISIONING (AI/Next-Best-Action), ROBOTICS (RPA). Certify")
print("for the role you perform. Pega = LOW-CODE, model-driven enterprise BPM/CRM/decisioning.")
EOF
```

**Expected result:** The Pega tracks — the prerequisite-gated System Architect ladder (CSA → CSSA → CLSA, the last a two-part written Architecture plus hands-on Application exam), Business Architect, Decisioning (Data Scientist, CPDC, interview-based Lead Decisioning Architect), and Robotics. The program lesson is that Pega's flagship System Architect ladder is prerequisite-gated to build cumulative capability, the CLSA proves design-and-build skill through a hands-on exam, and separate tracks serve business, decisioning, and robotics roles on the low-code Pega Platform.

**Negative test:** Attempting the CSSA or CLSA without the prerequisite below it. The System Architect ladder is gated — CSSA requires CSA and CLSA requires CSSA — so you build capability in order rather than skipping to the top.

**Cleanup:** None.

### Lab 1.2 — The two-part CLSA proves design and build

**Objective:** Contrast a written-only exam with the CLSA's hands-on component.

```bash
python3 - <<'EOF'
MODELS = {
  "written-only exam":       {"proves_design_knowledge": True, "proves_can_build": False},
  "CLSA (written + hands-on)":{"proves_design_knowledge": True, "proves_can_build": True},
}
print("What does each Lead-level model prove?\n")
for model, p in MODELS.items():
    score = sum(p.values())
    print(f"   {model:28} design_knowledge={p['proves_design_knowledge']}  can_build={p['proves_can_build']}  -> {score}/2")
print("\nThe CLSA is TWO-PART:")
print("   1. written ARCHITECTURE exam  -> proves you know the design principles")
print("   2. hands-on APPLICATION exam  -> DESIGN + BUILD a real app on Pega Platform")
print("      -> proves you can actually IMPLEMENT the architecture, not just describe it")
print("\nFor an ELITE architect credential, proving you can BUILD (not just recall) matters — a")
print("Lead System Architect designs AND delivers real Pega applications. It's the low-code")
print("counterpart to a practical exam: demonstrate, don't recite. The top of the SA ladder.")
EOF
```

**Expected result:** A written-only exam proving design knowledge (1/2) versus the CLSA's two-part written-plus-hands-on proving both design knowledge and build capability (2/2). The lesson is that the CLSA's hands-on Application exam (design and build a real app) validates real architectural implementation skill, not just recall — the elite credential at the top of the System Architect ladder.

**Negative test:** Judging Lead-architect competence by a written exam alone. Designing and delivering real Pega applications is a hands-on skill; the CLSA's Application exam proves the candidate can build, which is what an elite architect does.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Pega certification tracks understood — System Architect, Business Architect, Decisioning, Robotics.
- [ ] The System Architect ladder understood — CSA → CSSA → CLSA, prerequisite-gated.
- [ ] The two-part Lead System Architect exam understood — written Architecture plus hands-on Application (build).
- [ ] The Pega Platform placed, and Pega recognized as a low-code BPM/CRM/decisioning leader.
