# Chapter 09: Choosing Your Sysdig/Falco Path

## Learning Objectives

- Sequence a Sysdig/Falco learning path by role.
- Understand currency for a fast-moving cloud-native platform.
- Place Sysdig skills in the cloud-native-security career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the two-strand program [Chapter 1](01-the-sysdig-program.md) laid out.*

## Sequencing your path

The [two strands](01-the-sysdig-program.md) — open-source Falco and Sysdig product — combine by role:

| You are | Start | Then |
|:---|:---|:---|
| **Cloud/security engineer** | Falco LFS254 (runtime fundamentals) | Sysdig **Kraken Hunter** accreditation |
| **Kubernetes/platform engineer** | [CNCF K8s (XLI)](../../volume-041-cncf-kubernetes-certifications/README.md) foundation | Falco LFS254 → Sysdig |
| **SOC / detection engineer** | Falco (detection-as-code) | Sysdig CDR + accreditations |
| **Sysdig partner / SE** | Sysdig enablement | Partner Technical Accreditation |

**Falco is the free, open, foundational start** — because it is the CNCF-standard runtime engine, learning it (via LFS254) grounds the runtime-security concepts that Sysdig Secure builds on, and it is *free and open-source*. From there, the **Kraken Hunter** accreditation validates hands-on Sysdig tooling skill, and the **Partner** track serves partners/SEs.

Because Falco is open-source and the certs are badge-based, this is a **low-cost, hands-on** path: run Falco yourself (it is free), take the LF course, and add the Sysdig accreditations. Pairing **Falco + Kraken Hunter** is a strong, demonstrable cloud-native-runtime-security profile.

## Currency

Cloud-native security moves **fast** — Kubernetes releases regularly, eBPF and Falco advance, attack techniques evolve, and Sysdig adds capabilities continuously. Currency means **following the platform and the ecosystem** — re-engaging with Sysdig enablement and the Falco project as they evolve. Because Falco is open-source and community-driven, staying current is partly *participating* (the rules, the project) as much as re-certifying.

The discipline is the shelf-wide one: the [threat landscape and the platform move under the credential](../../volume-151-sentinelone-certifications/chapters/09-choosing-your-sentinelone-path.md), so pair the badges with hands-on operation and treat each Kubernetes release and each shift in cloud-native attack technique as the drumbeat.

## The cloud-native-security career

Sysdig/Falco skills sit in a fast-growing specialty: **everything is moving to containers and Kubernetes, and securing them at runtime is a distinct, in-demand discipline** that traditional endpoint and network security do not cover. An engineer who understands runtime detection, Falco, eBPF, and the runtime-first CNAPP is exactly the cloud-native-security profile the market needs — and the **open-source Falco angle** (a widely-adopted CNCF standard) makes the skills broadly transferable.

The career pairs naturally with adjacent skills this shelf covers:

- **[CNCF Kubernetes (XLI)](../../volume-041-cncf-kubernetes-certifications/README.md)** — the platform you are securing; Falco is itself a CNCF project.
- **[Wiz (CXLVII)](../../volume-147-wiz-certifications/README.md)** — agentless posture CNAPP; Sysdig's runtime-first complements it (posture + runtime).
- **[SentinelOne (CLI)](../../volume-151-sentinelone-certifications/README.md) / SOC** — runtime detection and response, the endpoint parallel.
- **[Snyk (CXLVIII)](../../volume-148-snyk-certifications/README.md)** — shift-left/AppSec; the prevention half of the lifecycle.

Sysdig is the runtime-first, Falco-powered cloud-native-security specialty at the moment everything runs in containers. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal Sysdig/Falco plan. **Cost:** none.

### Lab 9.1 — Build your Sysdig/Falco path

**Objective:** Generate a role-appropriate sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "cloud / security engineer": [
    ("Falco LFS254", "runtime security fundamentals (FREE, open-source, CNCF/LF)"),
    ("Sysdig Kraken Hunter", "hands-on Sysdig tooling accreditation (workshop + exam)"),
    ("(runtime CDR + CNAPP depth)", "the unified platform"),
  ],
  "SOC / detection engineer": [
    ("Falco (detection-as-code)", "write + tune runtime detection rules"),
    ("Sysdig CDR", "5-second detection, drift, forensics"),
  ],
  "Kubernetes / platform engineer": [
    ("CNCF Kubernetes foundation (Vol XLI)", "the platform you're securing"),
    ("Falco LFS254", "runtime security on K8s"),
    ("Sysdig accreditations", "the commercial CNAPP"),
  ],
}
role = "cloud / security engineer"   # change to taste
print(f"Sysdig/Falco path for: {role}\n")
for i, (cert, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {cert:32} {why}")
print("\nGuidance:")
print("  - START with FALCO (LFS254) — it's FREE + open-source (CNCF standard), and it")
print("    grounds the runtime-security concepts Sysdig Secure builds on. Run Falco")
print("    yourself; it costs nothing.")
print("  - then KRAKEN HUNTER (Sysdig's Credly accreditation — workshop labs + exam)")
print("    validates hands-on Sysdig tooling skill.")
print("  - it's a LOW-COST, HANDS-ON path: open-source Falco + badge-based accreditations.")
print("  - CURRENCY: cloud-native moves fast (K8s, eBPF, Falco, attack techniques) —")
print("    follow the platform + the Falco project; staying current is partly PARTICIPATING.")
EOF
```

**Expected result:** A role-specific sequence starting with the free, open-source Falco LFS254 course and adding the Sysdig Kraken Hunter accreditation, a low-cost hands-on path. The build-your-path lesson is to anchor on open-source Falco (the CNCF runtime standard, free to run and learn), add the Sysdig accreditations, and keep currency by following the fast-moving cloud-native ecosystem.

**Negative test:** Skipping Falco to jump straight to Sysdig product accreditation. Falco is the free, open-source engine Sysdig Secure is built on; learning it first grounds the runtime concepts the product assumes — and it costs nothing.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Position Sysdig in the cloud-native-security career

**Objective:** Map Sysdig/Falco skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Sysdig / Falco (runtime)", "runtime-first cloud-native security", "the specialty itself"),
  ("CNCF / Kubernetes (XLI)", "the platform being secured",          "Falco is a CNCF project"),
  ("Wiz (CXLVII)", "agentless posture CNAPP",                          "runtime complements posture"),
  ("SentinelOne (CLI) / SOC", "runtime detection & response",         "the endpoint parallel"),
  ("Snyk (CXLVIII)", "shift-left / AppSec",                            "the prevention half"),
  ("eBPF / Linux internals", "kernel instrumentation",                "how runtime visibility works"),
]
print("Sysdig/Falco in the cloud-native-security skill map:\n")
print(f"   {'skill':28}{'domain':40}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:28}{domain:40}{why}")
print("\nThe career thesis: EVERYTHING is moving to containers + Kubernetes, and securing")
print("them AT RUNTIME is a distinct, in-demand discipline traditional endpoint/network")
print("security doesn't cover. An engineer who gets runtime detection, Falco, eBPF, and")
print("the runtime-first CNAPP is exactly the cloud-native-security profile in demand.")
print("\nThe rounded cloud-native security engineer combines:")
print("  PREVENT   (Snyk, image scanning)  — shift-left, shrink the attack surface")
print("  POSTURE   (Wiz, CSPM)             — what COULD be wrong")
print("  RUNTIME   (Sysdig/Falco)          — what IS happening (the differentiator)")
print("  RESPOND   (CDR, drift)            — stop it in seconds")
print("  UNDERSTAND (K8s, eBPF)            — the platform + the instrumentation")
print("\nNone of it is siloed — it's the prevent/posture/runtime/respond loop, and Sysdig")
print("owns the RUNTIME-FIRST + open-source-Falco heart of it. Start FREE with Falco, add")
print("Kraken Hunter, and pair with K8s + posture + AppSec skills — that's a cloud-native")
print("security career, not just a badge. And Falco being open-source + CNCF makes it")
print("broadly transferable, not locked to one vendor.")
EOF
```

**Expected result:** Sysdig/Falco skills mapped to adjacent competencies — CNCF Kubernetes, Wiz posture, SentinelOne/SOC, Snyk shift-left, and eBPF — showing the rounded prevent/posture/runtime/respond profile. The career-positioning lesson closes the volume: Sysdig owns the runtime-first, open-source-Falco heart of cloud-native security, pairing with the Kubernetes, posture, and AppSec skills the rest of the shelf teaches, with Falco's CNCF-standard status making the skills transferable.

**Negative test:** Treating runtime security as covered by endpoint or network tools. Container runtime security is a distinct discipline (ephemeral workloads, eBPF, Falco, drift) — isolating Sysdig/Falco from the Kubernetes and cloud-security stack undersells both the specialty and the career.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A Sysdig/Falco path sequenced by role, anchored on the free open-source Falco LFS254 and the Kraken Hunter accreditation.
- [ ] Currency understood as following a fast-moving cloud-native ecosystem, partly through participating in the Falco project.
- [ ] Sysdig positioned in the cloud-native-security career alongside Kubernetes, posture, SOC, and shift-left skills.
- [ ] The volume assembled into a personal study and career plan — prevent, posture, runtime, respond, understand.
