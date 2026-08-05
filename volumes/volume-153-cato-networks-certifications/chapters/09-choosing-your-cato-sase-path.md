# Chapter 09: Choosing Your Cato/SASE Path

## Learning Objectives

- Sequence a Cato certification path by role.
- Understand currency for a free, badge-based program.
- Place SASE skills in the network-and-security career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the free program [Chapter 1](01-the-cato-sase-certification-program.md) laid out.*

## Sequencing your path

Because the certifications are **free and have no prerequisites**, the path is about *which to take, in what order*, for your role:

| You are | Start | Then |
|:---|:---|:---|
| **Network/security generalist** | SASE Expert Level 1 | Level 2 → Deployment & Management |
| **Security engineer** | SASE Expert Level 1 | SSE Fundamentals → Zero Trust → Advanced Security |
| **Platform operator** | SASE Expert Level 1 | SASE Deployment & Management |
| **Architect** | SASE Expert Level 1 → Level 2 | Zero Trust + Advanced Security |
| **Leader / decision-maker** | SASE Expert Level 1 | SASE Business Impact & Strategy |

**SASE Expert Level 1 is everyone's start** — it grounds the SASE concept the rest assume. From there, follow your role: security engineers deepen into SSE/Zero Trust/Advanced Security, operators into Deployment & Management, architects into Level 2 plus the security disciplines, and leaders into Business Impact & Strategy for the "why change" case.

Because it is all **free and self-paced**, the sensible strategy is simply to **take the courses relevant to your role** — and the **CPE credits** are a bonus that helps maintain other security certifications (ISC2, etc.). It is a low-cost way to build genuine SASE literacy.

## Currency

A free, badge-based program does not "expire" like a proctored cert, but **SASE and the platform evolve fast** — new security capabilities, AI-driven features (the AI in Cybersecurity course reflects this), and the SASE/SSE category itself is still maturing. Currency means **re-engaging as Cato adds courses** and as the SASE landscape shifts.

The deeper point: SASE is a *moving* discipline. The convergence story is settled, but the capabilities (AI, new threat prevention, evolving zero-trust models) keep advancing. Treat each new course and each shift in the threat landscape as the drumbeat, and use the free, ongoing nature of the program to stay current at no cost.

## The network-and-security career

SASE skills sit at the convergence point of two previously-separate careers — **networking** and **network security** — which is exactly where the industry is heading. An engineer who understands SASE (convergence, SD-WAN, SSE, ZTNA) is fluent in *both* the network and the security transformation that every enterprise is undertaking, which is a valuable, in-demand profile.

The career pairs naturally with adjacent skills this shelf covers:

- **[Zscaler (XXXV)](../../volume-035-zscaler-zero-trust-exchange/README.md) / [Netskope (CXXVII)](../../volume-127-netskope-certifications/README.md) / [Cloudflare (CXLII)](../../volume-142-cloudflare-certifications/README.md)** — the other SASE/SSE platforms; the concepts transfer, and knowing several is valuable.
- **[Aviatrix (CXXVI)](../../volume-126-aviatrix-certifications/README.md)** — multicloud networking; the cloud side of connectivity.
- **[Ping Identity (CL)](../../volume-150-ping-identity-certifications/README.md) / identity** — ZTNA is identity-driven; identity is the control plane.
- **[Wiz (CXLVII)](../../volume-147-wiz-certifications/README.md) / cloud security** — securing the cloud workloads SASE connects users to.

Cato is the pure-play converged-SASE and SASE-education specialty at the moment networking and security are converging. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal SASE plan. **Cost:** none — literally.

### Lab 9.1 — Build your SASE certification path

**Objective:** Generate a role-appropriate sequence of free courses.

```bash
python3 - <<'EOF'
PATHS = {
  "security engineer": [
    ("SASE Expert Level 1", "the SASE concept — the anchor"),
    ("SSE Fundamentals", "the security subset (SWG/CASB/ZTNA/FWaaS)"),
    ("Zero Trust", "ZTNA — replace the VPN"),
    ("Advanced Security", "IPS, sandboxing, TLS inspection, DLP"),
  ],
  "platform operator": [
    ("SASE Expert Level 1", "the concept"),
    ("SASE Deployment & Management", "operating the platform"),
  ],
  "leader / decision-maker": [
    ("SASE Expert Level 1", "understand what SASE is"),
    ("SASE Business Impact & Strategy", "the business case for converging"),
  ],
}
role = "security engineer"   # change to taste
print(f"Cato/SASE path for: {role}\n")
print("   (all FREE, self-paced, Credly-badged, 85% to pass, + ISC2 CPE credits)\n")
for i, (cert, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {cert:34} {why}")
print("\nGuidance:")
print("  - EVERYONE starts at SASE Expert Level 1 — it grounds the concept the rest assume.")
print("  - then follow your ROLE: security -> SSE/Zero Trust/Advanced Security; operator")
print("    -> Deployment & Mgmt; leader -> Business Impact & Strategy.")
print("  - it's all FREE + self-paced, so just TAKE the relevant courses. The CPE credits")
print("    help maintain other security certs (ISC2, etc.) — a bonus.")
print("  - CURRENCY: no expiry fee, but SASE + the platform evolve fast (AI, new threat")
print("    prevention) — re-engage as new courses drop.")
EOF
```

**Expected result:** A role-specific sequence of free courses anchored on SASE Expert Level 1, branching into SSE/Zero Trust/Advanced Security for security engineers or Business Impact for leaders, all free and CPE-granting. The build-your-path lesson is that everything is free and self-paced, so the strategy is to take the role-relevant courses from the foundational anchor, with CPE credits helping maintain other certifications.

**Negative test:** Skipping SASE Expert Level 1 for an advanced course. The advanced courses assume the SASE concept Level 1 grounds; even for experienced engineers it is the sensible free starting point.

**Cleanup:** None.

### Lab 9.2 — Position SASE in the network-and-security career

**Objective:** Map SASE skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Cato / SASE", "converged networking + security", "the specialty itself"),
  ("Zscaler / Netskope / Cloudflare", "other SASE/SSE platforms", "concepts transfer; know several"),
  ("Aviatrix", "multicloud networking", "the cloud connectivity side"),
  ("Ping / identity", "identity is the control plane", "ZTNA is identity-driven"),
  ("Wiz / cloud security", "cloud posture", "secures the workloads SASE connects to"),
  ("Zero Trust (broad)", "the security model", "SASE is a delivery of zero trust"),
]
print("SASE in the network-and-security skill map:\n")
print(f"   {'skill':34}{'domain':36}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:34}{domain:36}{why}")
print("\nThe career thesis: NETWORKING and network SECURITY, long separate careers, are")
print("CONVERGING — and SASE is that convergence. An engineer fluent in SASE understands")
print("BOTH the network and the security transformation every enterprise is undertaking.")
print("\nThe rounded SASE engineer combines:")
print("  CONNECT   (SD-WAN, backbone)      — the networking half")
print("  SECURE    (SWG/CASB/FWaaS)        — the SSE security functions")
print("  ZERO TRUST (ZTNA)                 — least-privilege app access, no VPN")
print("  IDENTITY  (Ping/Okta)             — the control plane ZTNA runs on")
print("  CLOUD     (Wiz)                   — the workloads users connect to")
print("\nNone of it is siloed — it's the converge-networking-and-security story SASE")
print("tells, and Cato pioneered both the platform and the education. Start free at")
print("SASE Expert L1, follow your role, and pair with identity + cloud + other-SASE")
print("knowledge — that's a network-security career at the industry's convergence point.")
EOF
```

**Expected result:** SASE skills mapped to adjacent competencies — other SASE/SSE platforms, multicloud networking, identity, cloud security, zero trust — showing the rounded connect/secure/zero-trust/identity/cloud profile. The career-positioning lesson closes the volume: SASE is the convergence of networking and security careers, and Cato pioneered both the platform and the education, pairing with the identity, cloud, and other-SASE skills the rest of the shelf teaches.

**Negative test:** Treating SASE as a narrow product skill. It sits at the convergence of networking and security, is identity-driven (ZTNA), and connects users to cloud workloads — isolating it undersells both the discipline and the career at the industry's convergence point.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Cato/SASE path sequenced by role, anchored on the free SASE Expert Level 1.
- [ ] Currency understood for a free badge program — re-engaging as SASE and the platform evolve, with CPE credits as a bonus.
- [ ] SASE positioned in the network-and-security career at the industry's convergence point.
- [ ] The volume assembled into a personal study and career plan — connect, secure, zero trust, identity, cloud.
