# Chapter 09: Choosing Your Pega Path

## Learning Objectives

- Sequence a Pega certification path by role and track.
- Understand currency for a versioned platform.
- Place Pega/low-code skills in the career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the tracks [Chapter 1](01-the-pega-program.md) laid out.*

## Sequencing your path

The [tracks (Ch 1)](01-the-pega-program.md) sequence by role:

| You are | Start | Then |
|:---|:---|:---|
| **Pega developer** | **CSA** (Certified System Architect) | **CSSA** → **CLSA** |
| **Business analyst** | **CPBA** (Business Architect) | (System Architect for depth) |
| **Decisioning / marketing tech** | **Decisioning Consultant (CPDC)** | Data Scientist → Lead Decisioning Architect |
| **RPA developer** | **Robotics System Architect** | System Architect |

**Start with the CSA** if you're a developer — it's the foundation the whole [System Architect ladder](01-the-pega-program.md) builds on, and the most common entry point. Climb to **CSSA** (reusability, [the layer cake, Ch 5](05-reusability-and-layer-cake.md)) and **CLSA** (the elite [two-part build exam](01-the-pega-program.md)) as you take on architecture. Business analysts start with **CPBA**; decisioning specialists with **CPDC**. Because the CSA is the gateway to the developer track, most Pega careers begin there. The lab builds a sequence.

## Currency

Pega certifications are **version-specific** — tied to a **Pega Infinity** release (currently **'25**; older versions retire, e.g. '24.2 on 30 June 2026). This means certifications **expire** as versions retire, and staying current requires **re-certifying** on the current version. Treat the version as central: certify on the **current** Infinity release, and keep up as Pega evolves (the [GenAI, Ch 7](07-robotics-and-genai.md) and decisioning advances are fast-moving). The durable core is the **model-driven, case-centric, reuse-oriented** way of building — which carries across versions even as the specifics change. The lab covers currency.

## The low-code / BPM career

Pega skills sit in the **low-code / enterprise-automation** career — durable and in-demand because organizations need to **automate complex work** and **build applications faster** than traditional coding allows. A Pega architect fluent in case management, model-driven development, reuse, and decisioning is exactly the profile enterprises building on Pega need — and Pega roles (especially CLSA) are well-compensated. The career pairs with adjacent skills this shelf covers:

- **[ServiceNow (LXXX)](../../volume-080-servicenow-certifications/README.md)** — the other major low-code enterprise workflow platform; the closest peer.
- **[Salesforce (LXXXIII)](../../volume-083-salesforce-certifications/README.md)** — CRM and low-code (Pega's customer-engagement competitor).
- **[UiPath (CXLIX)](../../volume-149-uipath-certifications/README.md)** — RPA, adjacent to Pega Robotics.
- **[MuleSoft (CLX)](../../volume-160-mulesoft-certifications/README.md)** — integration, connecting Pega to systems of record.

Pega is the model-driven, case-centric low-code specialty for complex enterprise automation. The lab positions it.

## Hands-On Lab

Python assembles a personal Pega plan. **Cost:** none.

### Lab 9.1 — Build your Pega path

**Objective:** Generate a role-appropriate sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "Pega developer": [
    ("Certified System Architect (CSA)", "foundation — build apps in App/Dev Studio"),
    ("Certified Senior System Architect (CSSA)", "reusability / the situational layer cake"),
    ("Certified Lead System Architect (CLSA)", "ELITE — 2-part written + hands-on BUILD exam"),
  ],
  "business analyst": [
    ("Certified Pega Business Architect (CPBA)", "capture requirements via DCO"),
    ("(CSA for technical depth)", "understand how it's built"),
  ],
  "decisioning specialist": [
    ("Certified Pega Decisioning Consultant (CPDC)", "Customer Decision Hub strategy"),
    ("Certified Pega Data Scientist", "the predictive/adaptive models"),
    ("Lead Decisioning Architect", "expert (interview; needs CPDC + Data Scientist)"),
  ],
}
role = "Pega developer"   # change to taste
print(f"Pega certification path for: {role}\n")
for i, (cert, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {cert:44} {why}")
print("\nGuidance:")
print("  - DEVELOPERS start with CSA (the gateway to the SA ladder), then CSSA (reuse/layer cake) ->")
print("    CLSA (elite, hands-on build exam). BUSINESS analysts start CPBA; DECISIONING start CPDC.")
print("  - certs are VERSION-SPECIFIC (Pega Infinity '25) — recertify as versions retire.")
print("  - the DURABLE core = model-driven + case-centric + reuse — it carries across versions.")
print("  - CLSA is hands-on (design + BUILD a real app) — practice building, don't just study.")
EOF
```

**Expected result:** A role-based sequence (e.g., developer: CSA → CSSA → CLSA; decisioning: CPDC → Data Scientist → Lead Decisioning Architect). The build-your-path lesson is that developers start with the CSA gateway and climb the reuse-focused CSSA to the elite hands-on CLSA, while business and decisioning specialists follow their tracks, recertifying as versions retire and investing in the durable model-driven, case-centric, reuse core.

**Negative test:** Chasing the CLSA without CSA/CSSA or hands-on practice. The ladder is prerequisite-gated and the CLSA requires building a real app; progress through CSA and CSSA with hands-on practice, not by jumping to the top.

**Cleanup:** None.

### Lab 9.2 — Position Pega in the low-code career

**Objective:** Map Pega skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Pega (model-driven low-code)", "case mgmt + BPM + decisioning", "the specialty itself"),
  ("ServiceNow (LXXX)", "low-code enterprise workflow", "the closest platform peer"),
  ("Salesforce (LXXXIII)", "CRM + low-code", "customer-engagement competitor"),
  ("UiPath (CXLIX)", "RPA", "adjacent to Pega Robotics"),
  ("MuleSoft (CLX)", "integration", "connects Pega to systems of record"),
]
print("Pega in the low-code / enterprise-automation skill map:\n")
print(f"   {'skill':32}{'domain':34}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:32}{domain:34}{why}")
print("\nThe career thesis: organizations need to AUTOMATE COMPLEX WORK and build apps FASTER than")
print("traditional coding allows — low-code is in-demand. A Pega architect fluent in CASE MANAGEMENT,")
print("MODEL-DRIVEN development, REUSE (layer cake), and DECISIONING is exactly that profile (and CLSA")
print("is well-compensated).")
print("\nThe rounded Pega professional:")
print("  MODEL     (low-code, everything-is-a-rule)  — build without hand-coding")
print("  ORCHESTRATE (case management)                — dynamic cases, humans + automation")
print("  REUSE     (situational layer cake)          — specialize by layer, no forking")
print("  DECIDE    (Next-Best-Action / CDH)          — real-time 1:1 AI decisioning")
print("  AUTOMATE  (robotics + GenAI)                — RPA + AI-assisted development")
print("Pega owns the MODEL-DRIVEN, CASE-CENTRIC low-code space. Learn it with ServiceNow (peer),")
print("Salesforce (CRM), UiPath (RPA), and MuleSoft (integration) — a low-code/automation career.")
EOF
```

**Expected result:** Pega mapped against ServiceNow (platform peer), Salesforce (CRM), UiPath (RPA), and MuleSoft (integration), across the model/orchestrate/reuse/decide/automate profile. The career-positioning lesson closes the volume: organizations need to automate complex work and build faster, so Pega's model-driven, case-centric low-code specialty (with reuse and decisioning) is in demand, learned alongside the ServiceNow platform peer, Salesforce CRM, UiPath RPA, and MuleSoft integration.

**Negative test:** Treating Pega as just a BPM workflow tool. It is a model-driven low-code platform spanning case management, reuse architecture, real-time AI decisioning, and robotics; the skills cover building, orchestrating, reusing, deciding, and automating across complex enterprise work.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Pega path sequenced by role — the CSA → CSSA → CLSA developer ladder, plus Business Architect and Decisioning tracks.
- [ ] Currency understood — version-specific certifications (Pega Infinity), recertifying as versions retire.
- [ ] Pega positioned in the low-code career alongside ServiceNow, Salesforce, UiPath, and MuleSoft.
- [ ] The volume assembled into a personal study and career plan — model, orchestrate, reuse, decide, automate.
