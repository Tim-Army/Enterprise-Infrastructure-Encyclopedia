# Chapter 01: The Cato SASE Certification Program

![The Cato SASE certification program and the converged platform beneath it. The program is free, awards Credly badges and downloadable certificates, requires no prerequisites, and passes at eighty-five percent, with each course granting ISC2 CPE credits. Cato pioneered the industry's first SASE certification. The eight certifications span levels: SASE Expert Level 1 and the AI in Cybersecurity course at the foundational level, SASE Expert Level 2 and SSE Fundamentals at the intermediate level, SASE Deployment and Management at the technical level, Zero Trust and Advanced Security at the advanced level, and SASE Business Impact and Strategy at the executive level. The platform beneath is a single-vendor converged SASE cloud that combines networking and security: SD-WAN for optimized connectivity, Firewall-as-a-Service, Secure Web Gateway, Cloud Access Security Broker, Zero Trust Network Access, and intrusion prevention, all delivered from a global private backbone of points of presence through a single-pass architecture that inspects traffic once for every function, replacing the traditional stack of separate point products with one platform, one policy, and one console.](../../../diagrams/volume-153-cato-networks-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Eight free, Credly-badged certifications over the converged single-vendor SASE cloud.*

## Learning Objectives

- Describe the Cato SASE certification program — free, Credly-badged, and level-based.
- Place the certifications across foundational, intermediate, advanced, and executive levels.
- Understand Cato's position as the SASE pioneer and pure-play.
- Recognize the converged SASE platform beneath the certifications.

> **Defensive framing.** This volume is about *securing* connectivity — converging network security functions (firewall, secure web gateway, zero trust) into one cloud service to protect an organization's users, sites, and cloud. Nothing here is about attacking networks.

## What Cato is

Cato Networks is the **pioneer of SASE** (Secure Access Service Edge) — it built one of the first **single-vendor converged SASE clouds** and launched the **industry's first SASE certification**. Its platform delivers *both* networking (SD-WAN) *and* security (firewall, secure web gateway, CASB, zero trust) as **one cloud service** from a **global private backbone**. Where the [Zscaler (XXXV)](../../volume-035-zscaler-zero-trust-exchange/README.md), [Netskope (CXXVII)](../../volume-127-netskope-certifications/README.md), and [Cloudflare (CXLII)](../../volume-142-cloudflare-certifications/README.md) volumes cover other SASE/SSE players, **Cato is the converged single-vendor pure-play** — and the certification program teaches SASE as a discipline, not just a product.

## The certification program

Cato's certifications are notable for being **free** and **Credly-badged** — a low-barrier, education-first program. The key facts:

> **Free, badged, 85% to pass.** Every Cato certification course is **free**, has **no prerequisites**, requires **85% to pass**, and awards a **downloadable certificate plus a Credly badge**. Courses grant **ISC2 CPE credits** (roughly one CPE credit per hour of eligible learning) — useful for maintaining other security certifications. This is a *learning* program, stated plainly: valuable, free, and current, not a proctored gate.

The eight certifications span levels:

| Level | Certifications |
|:---|:---|
| **Foundational** | SASE Expert Level 1 · AI in Cybersecurity |
| **Intermediate** | SASE Expert Level 2 · SSE Fundamentals |
| **Technical** | SASE Deployment & Management |
| **Advanced** | Zero Trust · Advanced Security |
| **Executive** | SASE Business Impact & Strategy |

**SASE Expert Level 1 is the anchor** — the foundational course grounding the SASE concept that everything else builds on. From there the program branches by depth and role: deeper SASE (Level 2), the security subset (SSE Fundamentals), specific disciplines (Zero Trust, Advanced Security), operations (Deployment & Management), and even a business-strategy track for executives.

## The converged platform

Every certification teaches the **converged SASE cloud**:

| Capability | Is |
|:---|:---|
| **SD-WAN** | Optimized software-defined connectivity (the networking) |
| **FWaaS / SWG / CASB / IPS** | Cloud-delivered security functions |
| **ZTNA** | Zero-trust app access (replacing VPN) |
| **Global backbone** | A private worldwide network of PoPs |
| **Single-pass architecture** | Inspect traffic *once* for all functions |

The unifying idea is **convergence**: networking and all security functions delivered as *one* cloud service, one policy, one console — versus the traditional stack of separate point products ([Chapter 3](03-traditional-stack-vs-converged-sase.md)). The lab reads the program and the convergence idea.

## Hands-On Lab

The labs in this volume model SASE concepts in Python at no cost — Cato is a cloud service, so the labs model the *decisions and disciplines* the certifications test (convergence, single-pass, zero trust). The certifications themselves are **free** on Cato's site.

### Lab 1.1 — Read the free, level-based program

**Objective:** Place a certification by level and focus.

```bash
python3 - <<'EOF'
CERTS = [
  # cert,                       level,        focus
  ("SASE Expert Level 1",       "Foundational","the SASE concept — the anchor"),
  ("AI in Cybersecurity",       "Foundational","AI's role in security"),
  ("SASE Expert Level 2",       "Intermediate","deeper SASE architecture"),
  ("SSE Fundamentals",          "Intermediate","the security subset (SSE)"),
  ("SASE Deployment & Management","Technical", "operating the platform"),
  ("Zero Trust",                "Advanced",    "ZTNA — replace the VPN"),
  ("Advanced Security",         "Advanced",    "advanced threat prevention"),
  ("SASE Business Impact & Strategy","Executive","the business case"),
]
print(f"{'certification':32}{'level':14}focus")
for cert, level, focus in CERTS:
    print(f"{cert:32}{level:14}{focus}")
print("\nHow to read it — FREE, Credly-badged, 85% to pass, no prerequisites, CPE credits:")
print("  - SASE EXPERT LEVEL 1 is the anchor: the foundational course that grounds the")
print("    SASE CONCEPT everything else assumes.")
print("  - the program branches by DEPTH and ROLE: deeper SASE (L2), the security")
print("    subset (SSE Fundamentals), specific disciplines (Zero Trust, Advanced")
print("    Security), operations (Deployment & Mgmt), even an EXECUTIVE strategy track.")
print("\nBeing FREE + badged makes this a low-barrier way to learn SASE as a DISCIPLINE")
print("(Cato pioneered SASE education). It's a LEARNING program — genuine and current —")
print("not a proctored gate. The CPE credits also help maintain other security certs.")
print("Start at SASE Expert L1, then follow the level/role that matches you.")
EOF
```

**Expected result:** The eight free, Credly-badged certifications placed across foundational-to-executive levels, anchored on SASE Expert Level 1. The program lesson is a low-barrier, education-first structure — free, 85% to pass, CPE-granting — that teaches SASE as a discipline, branching by depth and role from the foundational anchor.

**Negative test:** Expecting an expensive, proctored certification gate. Cato's program is free, badged, and education-first; it validates learning the SASE discipline, and its CPE credits even help maintain other certifications.

**Cleanup:** None.

### Lab 1.2 — Convergence: one service versus a stack

**Objective:** See the core SASE idea the whole program teaches.

```bash
python3 - <<'EOF'
FUNCTIONS = [
  ("connect sites/users/cloud", "SD-WAN"),
  ("firewall / threat prevention","FWaaS"),
  ("secure web access",         "SWG"),
  ("cloud app control",         "CASB"),
  ("remote app access",         "ZTNA (replaces VPN)"),
  ("intrusion prevention",      "IPS"),
]
print("The functions an enterprise needs at its network edge:\n")
print("TRADITIONAL STACK — a separate POINT PRODUCT for each:")
for need, func in FUNCTIONS:
    print(f"   {need:28} -> a separate {func} box/console/policy/vendor")
print(f"   -> {len(FUNCTIONS)} products, {len(FUNCTIONS)} consoles, {len(FUNCTIONS)} policies to keep in sync,")
print("      traffic hair-pinned through each in sequence. Complex, slow, gaps between.\n")
print("CONVERGED SASE (Cato) — ALL of it as ONE cloud service:")
for need, func in FUNCTIONS:
    print(f"   {need:28} -> {func}  (same platform, same policy, same console)")
print("   -> 1 platform, 1 policy, 1 console; traffic inspected ONCE (single-pass) at a")
print("      global PoP near the user; networking + security CONVERGED.\n")
print("The core idea the whole program teaches: SASE (Gartner, 2019) CONVERGES")
print("networking (SD-WAN) and network security (SWG/CASB/FWaaS/ZTNA) into ONE cloud-")
print("delivered service. Instead of buying, integrating, and operating a STACK of")
print("point products with gaps between them, you get one converged platform with one")
print("policy. That convergence — simpler, faster, more secure — is Cato's whole thesis")
print("and the subject of SASE Expert (Chapters 2-4).")
EOF
```

**Expected result:** The edge functions (SD-WAN, FWaaS, SWG, CASB, ZTNA, IPS) provided either as a stack of separate point products with their own consoles and policies, or converged into one Cato cloud service with one policy and single-pass inspection. The convergence lesson is SASE's core idea — networking and security unified as one cloud-delivered service instead of an integrated stack of point products with gaps between them.

**Negative test:** Assembling SASE from separate best-of-breed point products. Each has its own console and policy, traffic hair-pins through them in sequence, and gaps open between them — convergence into one service is the SASE proposition Cato pioneered.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Cato program understood as free, Credly-badged, 85%-to-pass, and level-based, with CPE credits.
- [ ] The eight certifications placed across foundational, intermediate, technical, advanced, and executive levels.
- [ ] Cato recognized as the SASE pioneer and single-vendor converged pure-play.
- [ ] Convergence understood as the core SASE idea — networking and security as one cloud service.
