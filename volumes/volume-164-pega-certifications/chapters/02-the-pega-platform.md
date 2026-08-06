# Chapter 02: The Pega Platform — Low-Code and Model-Driven

## Learning Objectives

- Explain low-code, model-driven development.
- Describe App Studio versus Dev Studio.
- Understand "everything is a rule."
- Recognize guardrails and building for change.

*Cert relevance: the model-driven platform and guardrails underpin every Pega certification.*

## Low-code, model-driven development

The **Pega Platform** (Pega Infinity) is a **low-code, model-driven** platform. Instead of writing application code by hand, you **model** the application **visually** — define the case, the data, the UI, the logic — and Pega **generates the running application** from that model. "**Model-driven**" is the key idea: the model *is* the application, so changing the model changes the app, and there is no separate codebase to keep in sync. This lets **business and IT build together** (business analysts model requirements, developers add technical depth) and lets applications **change quickly** as needs evolve. Low-code, model-driven development is Pega's foundation and what every certification assumes. The lab models the approach.

## App Studio versus Dev Studio

Pega provides **two authoring environments** for different audiences:

- **App Studio** — a **low-code, business-friendly** environment for building and modifying applications visually (cases, data, UI, simple logic). Business architects and citizen developers work here.
- **Dev Studio** — the **full developer** environment with complete control over every rule and technical detail. System architects work here for advanced configuration.

The two share the **same underlying application** — App Studio is a simplified view, Dev Studio the complete one. This lets a team collaborate at the right level: business-friendly modeling in App Studio, deep configuration in Dev Studio, on **one** app. Knowing which environment does what is core System Architect knowledge. The lab models the two studios.

## Everything is a rule

A defining Pega concept: **everything is a rule**. In Pega, the building blocks of an application — a **flow**, a **UI screen**, a **data type**, a **decision**, a **validation**, a **report** — are all **rules**, stored in the platform's rule engine. This uniformity is powerful:

- **Reuse** — rules can be shared and specialized ([the layer cake, Ch 5](05-reusability-and-layer-cake.md)).
- **Versioning and governance** — rules are versioned and managed centrally.
- **Model-driven** — the app is a **set of rules**, not hand-written code, so it's inspectable and changeable.

Understanding that a Pega application is fundamentally a **collection of rules** is essential to how the platform works and how you build on it. The lab models rules.

## Guardrails and building for change

Pega enforces best practices through **guardrails** — the platform continuously **scores** your application against best-practice rules and gives a **guardrail compliance score**. High compliance means you've stayed **model-driven** (using standard Pega capabilities, minimal custom code); low compliance flags **risky custom code** that will be hard to maintain and upgrade. The philosophy is **"build for change"**: applications built the model-driven, guardrail-compliant way are **easy to change and upgrade**, while custom-code-heavy apps become brittle. Guardrails are a distinctive Pega discipline, and staying "in the guardrails" is a core skill the certifications reward. The lab models guardrails.

## Hands-On Lab

Python models rules, studios, and guardrails. **Cost:** none.

### Lab 2.1 — Rules, the two studios, and guardrail compliance

**Objective:** See the model-driven, rule-based, guardrail-scored approach.

```bash
python3 - <<'EOF'
# in Pega, EVERYTHING is a rule; App Studio (low-code) + Dev Studio (full) edit the SAME app
app_rules = {
  "flow: LoanReview":       {"type": "flow",       "studio": "App Studio (visual) / Dev Studio"},
  "UI: ApplicantForm":      {"type": "UI",         "studio": "App Studio (low-code)"},
  "data type: Applicant":   {"type": "data",       "studio": "App Studio / Dev Studio"},
  "decision: CreditCheck":  {"type": "decision",   "studio": "Dev Studio (advanced)"},
  "validation: IncomeReq":  {"type": "validation", "studio": "Dev Studio"},
}
print("A Pega application = a COLLECTION OF RULES (everything is a rule):\n")
for name, r in app_rules.items():
    print(f"   {name:24} [{r['type']:10}] edited in: {r['studio']}")
print("   App Studio (low-code, business-friendly) + Dev Studio (full dev) edit the SAME app\n")

# guardrail compliance score: model-driven vs custom code
def guardrail_score(app):
    base = 100
    base -= app["custom_java_activities"] * 8   # custom code hurts compliance + maintainability
    base -= app["hardcoded_values"] * 3
    return max(0, base)
model_driven = {"custom_java_activities": 0, "hardcoded_values": 1}
custom_heavy  = {"custom_java_activities": 6, "hardcoded_values": 8}
print("GUARDRAIL COMPLIANCE SCORE (Pega scores your app vs best practices):")
print(f"   model-driven app  (0 custom activities): score {guardrail_score(model_driven)}/100  -> easy to change + upgrade")
print(f"   custom-code-heavy (6 custom activities): score {guardrail_score(custom_heavy)}/100  -> brittle, hard to upgrade\n")
print("Pega is LOW-CODE + MODEL-DRIVEN: you MODEL the app (cases/data/UI/logic) and Pega GENERATES")
print("it — the model IS the app (no separate codebase). ★ EVERYTHING IS A RULE (flow/UI/data/")
print("decision = rules) -> reuse, versioning, governance. APP STUDIO (business-friendly) + DEV")
print("STUDIO (full dev) edit ONE app. ★ GUARDRAILS score you vs best practices — 'BUILD FOR CHANGE':")
print("stay model-driven (high score = easy to upgrade), avoid custom code (low score = brittle).")
EOF
```

**Expected result:** A Pega application shown as a collection of rules (flow, UI, data, decision, validation) edited in App Studio (low-code) or Dev Studio (full developer) on the same app, plus a guardrail compliance score where the model-driven app scores high (easy to upgrade) and the custom-code-heavy app scores low (brittle). The platform lesson is that Pega is low-code and model-driven (the model is the app, everything is a rule), the two studios serve business and developer audiences on one app, and guardrails score best-practice compliance to enforce "build for change."

**Negative test:** Building a Pega app with heavy custom Java and hardcoded values. Guardrail compliance drops, and the app becomes brittle and hard to upgrade; staying model-driven and in the guardrails keeps the application maintainable and upgradeable.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Low-code, model-driven development understood — modeling the app so Pega generates it.
- [ ] App Studio versus Dev Studio understood — business-friendly and full-developer views of one app.
- [ ] "Everything is a rule" understood — flows, UI, data, and decisions as rules enabling reuse and governance.
- [ ] Guardrails and building for change understood — best-practice scoring that keeps apps maintainable.
