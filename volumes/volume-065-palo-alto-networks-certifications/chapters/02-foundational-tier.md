# Chapter 02: The Foundational Tier

## Learning Objectives

- Explain the shared Foundational credentials (Cybersecurity Apprentice, Cybersecurity Practitioner).
- Apply core security concepts: the CIA triad, Zero Trust, and defense in depth.
- Describe the Palo Alto platform portfolio at a conceptual level.
- Relate the SASE and SOC models to the three tracks.
- Complete a walkthrough for each Foundational topic.

## Theory and Architecture

The **Foundational** level is shared across all three tracks and comprises **Cybersecurity
Apprentice** and **Cybersecurity Practitioner**. These credentials establish the vocabulary and
mental models the rest of the program assumes: the **CIA triad** (confidentiality, integrity,
availability), **Zero Trust** ("never trust, always verify" — authenticate and authorize every
access), **defense in depth** (layered controls), the **cyberattack lifecycle** (and how
controls break it), and conceptual literacy across the **Palo Alto portfolio** — NGFW/Strata
for network security, Cortex (XDR/XSIAM/XSOAR) for security operations, and Prisma/Cortex Cloud
for cloud security, unified by the **SASE** model (network + security delivered from the cloud).
These are the concepts a practitioner reasons with before touching a specific product.

## Design Considerations

Build every design on **Zero Trust** and **defense in depth** — no single control is trusted
alone. Understand where each portfolio piece fits (perimeter/inline vs endpoint/SOC vs cloud
posture) so you choose the right tool per problem. The Foundational concepts are the "why"
behind every later configuration.

## Implementation and Automation

The labs reason about the CIA triad, Zero Trust, defense in depth, and the portfolio mapping.

## Validation and Troubleshooting

Confirm the foundational model:

```text
CIA triad: confidentiality, integrity, availability.
Zero Trust: authenticate + authorize every access; least privilege; assume breach.
Defense in depth: layered controls (network + endpoint + cloud + identity).
Portfolio: NGFW/Strata (network), Cortex XDR/XSIAM/XSOAR (SecOps), Prisma/Cortex Cloud (cloud); SASE unifies.
```

Common pitfalls: treating the firewall as the **only** control (defense in depth needs
layers); and equating Zero Trust with a single product (it is an **architecture**).

## Security and Best Practices

Apply **least privilege** and **assume breach** everywhere. Layer controls so one failure is not
fatal. Keep the portfolio mapping straight so security problems go to the right platform. These
habits carry through every track.

## Hands-On Lab

Foundational walkthroughs. **Shared prerequisites for Labs 2.1–2.3** — a shell with `python3`.
**Cost:** none.

### Lab 2.1 — Classify controls by CIA and layer

**Objective:** Map controls to the triad and to depth layers.

```python
python3 - <<'PY'
controls={
 "Firewall policy":("Confidentiality/Integrity","network"),
 "EDR (Cortex XDR)":("Integrity/Availability","endpoint"),
 "Backups":("Availability","data"),
 "MFA":("Confidentiality","identity"),
}
for c,(cia,layer) in controls.items(): print(f"{c:20} CIA={cia:24} layer={layer}")
PY
```

**Expected result:** each control mapped to a **CIA** property and a **defense-in-depth layer** —
layered coverage.

**Negative test:** rely on one control for all of CIA; **defense in depth** spreads coverage —
map several layers.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Evaluate a Zero Trust decision

**Objective:** Decide access under Zero Trust.

```python
python3 - <<'PY'
def zero_trust(authenticated, authorized, device_healthy, least_privilege):
    return "allow (scoped)" if all([authenticated,authorized,device_healthy,least_privilege]) else "deny"
print("healthy managed user:", zero_trust(True,True,True,True))
print("unauthenticated:", zero_trust(False,True,True,True))
PY
```

**Expected result:** access only when **authenticated, authorized, healthy, and scoped** —
Zero Trust in action.

**Negative test:** allow by network location ("inside the perimeter"); Zero Trust **verifies
every access** regardless of location.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Map the portfolio to a problem

**Objective:** Route a security need to the right platform.

```python
python3 - <<'PY'
needs={"Block malicious traffic inline":"NGFW / Strata (Network Security)",
       "Detect endpoint compromise":"Cortex XDR (Security Operations)",
       "Automate incident response":"Cortex XSOAR (Security Operations)",
       "Find cloud misconfigurations":"Prisma / Cortex Cloud (Cloud Security)"}
for need,platform in needs.items(): print(f"{need:34} -> {platform}")
PY
```

**Expected result:** each need routed to the correct **platform and track** — portfolio
literacy.

**Negative test:** try to fix a cloud misconfiguration with the firewall; use **Prisma/Cortex
Cloud** — match the platform to the problem.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Foundational tier (Cybersecurity Apprentice and Practitioner), shared across tracks,
establishes the CIA triad, Zero Trust, defense in depth, and portfolio literacy — the concepts
every later track applies. Layer controls, verify every access, and route each problem to the
right platform.

- [ ] I can map controls to CIA and defense-in-depth layers.
- [ ] I can evaluate a Zero Trust access decision.
- [ ] I can route a need to the right platform and track.
- [ ] I can explain how SASE unifies the portfolio.
- [ ] I completed Labs 2.1–2.3 including each negative test.
