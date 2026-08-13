# Chapter 05: Reusability and the Situational Layer Cake

## Learning Objectives

- Explain the reusability problem in enterprise applications.
- Describe the situational layer cake architecture.
- Understand specialization by layer (business unit, channel, region).
- Recognize reuse as the Senior/Lead Architect focus.

*Cert relevance: the situational layer cake and reuse are the core of the CSSA and CLSA certifications.*

## The reusability problem

Large enterprises don't have **one** version of a process — they have **many variations**. A "loan application" differs by **business unit** (retail vs commercial), by **region** (different regulations), by **channel** (web vs branch vs mobile), and by **customer segment**. The naive approach — **copying** the application and modifying each copy — creates a maintenance nightmare: a change to the common logic must be made in **every** copy, variations **drift** apart, and the number of forks explodes. **Reuse** is the answer: build the **common** parts once and **specialize** only the differences. Pega's architecture for this is the **situational layer cake**, and mastering it is the core of the Senior and Lead System Architect certifications. The lab models the problem.

## The situational layer cake

The **situational layer cake** is Pega's **layered architecture for reuse**. Application logic (rules) is organized into **layers** (rulesets), from **general** at the bottom to **specific** at the top:

- **Enterprise / framework layer** — the **common** logic shared by everyone (the base loan process).
- **Division / business-unit layers** — specializations for a business unit (retail loans add their rules).
- **Region / channel / segment layers** — further specializations (EU region adds GDPR steps; mobile channel adds a mobile UI).

At runtime, Pega **assembles** the applicable layers for the **situation** (this user, this business unit, this region, this channel) — taking the common logic and applying only the specializations that apply. **Build once, specialize by layer.** The lab models the layers.

## Specialization by layer

The power is **specialization without forking**. When a business unit needs a **different** approval step, you **override** just that one rule **in that unit's layer** — the rest of the application (the common 90%) is **inherited** from the shared layers. So:

- **Common logic is defined once** — a bug fix or enhancement to the shared process applies **everywhere** automatically.
- **Variations live in their own layers** — each business unit/region/channel has only its **differences**, not a whole copy.
- **The right combination assembles per situation** — Pega picks the applicable layers at runtime.

This turns the copy-and-modify nightmare into a **clean, maintainable** structure where common and specific are cleanly separated. Designing this layering well is the essence of Senior/Lead architecture. The lab models specialization.

## Reuse as the Senior/Lead focus

The [System Architect ladder (Ch 1)](01-the-pega-program.md) reflects this: the **CSA** builds an application; the **CSSA** designs for **reusability across multiple business lines** (the layer cake); the **CLSA** architects **enterprise-scale** reuse and governance. As you climb, the skill shifts from **building one app** to **architecting a reusable platform** where many applications and variations share common foundations efficiently. Reuse — the situational layer cake — is what separates a senior/lead architect from a system architect, and it's what makes Pega scale across a large, varied enterprise. The lab synthesizes.

## Hands-On Lab

Python models the layer cake and specialization. **Cost:** none.

### Lab 5.1 — Build once, specialize by layer

**Objective:** See the situational layer cake assemble rules per situation.

```bash
python3 - <<'EOF'
# rules defined at different layers; Pega assembles the applicable ones per SITUATION
LAYERS = {
  "enterprise":      {"approval_limit": 10000, "process": "base loan process", "kyc": "standard"},
  "retail-division": {"approval_limit": 25000},                          # retail specializes the limit
  "eu-region":       {"kyc": "GDPR-enhanced"},                            # EU specializes KYC
  "mobile-channel":  {"ui": "mobile-optimized"},                         # mobile specializes UI
}
# situation = which layers apply (most-specific wins), assembled at runtime
def assemble(situation_layers):
    resolved = {}
    for layer in ["enterprise"] + situation_layers:   # general -> specific
        resolved.update(LAYERS.get(layer, {}))         # specific overrides general
    return resolved

print("SITUATIONAL LAYER CAKE — build COMMON once, SPECIALIZE by layer:\n")
print("   layers (general -> specific):")
for l, rules in LAYERS.items():
    print(f"      {l:16} {rules}")
print()
situations = {
  "Retail loan, EU, mobile":   ["retail-division", "eu-region", "mobile-channel"],
  "Enterprise default (base)": [],
}
for name, layers in situations.items():
    print(f"   SITUATION '{name}' -> assemble {['enterprise']+layers}:")
    print(f"      resolved rules: {assemble(layers)}")
print()
print("Instead of COPYING the app per variation (retail/EU/mobile...) — a maintenance nightmare")
print("(fix a bug in EVERY copy, variations drift, forks explode) — the LAYER CAKE defines COMMON")
print("logic ONCE (enterprise layer) and puts each variation in its OWN layer (retail overrides the")
print("limit; EU overrides KYC; mobile overrides UI). Pega ASSEMBLES the applicable layers per")
print("SITUATION at runtime (most-specific wins). Build once, specialize by layer — no forking. This")
print("reuse architecture is the CSSA/CLSA core, and what makes Pega scale across a varied enterprise.")
EOF
```

**Expected result:** A situational layer cake where enterprise-layer common rules (approval limit, base process, KYC) are specialized by retail (higher limit), EU (GDPR KYC), and mobile (UI) layers, and Pega assembles the applicable layers per situation (a retail/EU/mobile loan gets the specialized rules; the default gets the base). The reusability lesson is that the layer cake defines common logic once and puts each variation in its own layer, assembled per situation at runtime — replacing copy-and-modify forking with clean, maintainable reuse, the core of the Senior/Lead Architect certifications.

**Negative test:** Copying the application for each business unit, region, and channel. Common changes must be repeated in every copy, variations drift, and forks explode; the situational layer cake defines common logic once and specializes only the differences by layer.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The reusability problem understood — enterprise process variations and the copy-and-modify nightmare.
- [ ] The situational layer cake understood — layered rulesets from general to specific, assembled per situation.
- [ ] Specialization by layer understood — overriding only the differences while inheriting common logic.
- [ ] Reuse recognized as the Senior/Lead Architect focus — architecting reusable enterprise-scale applications.
