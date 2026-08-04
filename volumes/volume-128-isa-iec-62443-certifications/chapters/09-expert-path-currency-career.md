# Chapter 09: The Expert Path, Currency, and Career

## Learning Objectives

- Understand the ISA/IEC 62443 Cybersecurity Expert designation and how to reach it.
- Choose a route through the certificates for your role.
- Keep knowledge current as the standard and threat landscape evolve.

## The Expert designation

There is no separate Expert exam. **Holding all four certificates — Fundamentals (IC32), Risk Assessment (IC33), Design (IC34), and Maintenance (IC37) — automatically confers the ISA/IEC 62443 Cybersecurity Expert designation.** It signals end-to-end command of the IACS security lifecycle: assess, design, and maintain, grounded in the standard.

| To reach… | You need |
|:---|:---|
| Fundamentals Specialist | IC32 + exam |
| Any Specialist (Risk/Design/Maintenance) | Fundamentals first, then that course + exam |
| **Expert** | **all four certificates** (no additional exam) |

## Choosing your route

The Fundamentals gate is fixed; after it, sequence the specialists by your role:

| If your role is… | After IC32, prioritize |
|:---|:---|
| Security assessor / auditor | **IC33 Risk Assessment** |
| Architect / integrator / OEM | **IC34 Design** |
| Plant security / operations / IR | **IC37 Maintenance** |
| Consultant / lead / aiming for Expert | all three (order by current project) |

Because the specialists can be taken in any order, take the one your **current work** exercises next — you'll retain it better and apply it immediately. Expert is the natural endpoint for OT security leads and consultants who must own the whole lifecycle.

## Currency

- **No renewal — but the standard evolves.** The credentials do not expire, yet IEC 62443 parts are revised and new parts published; a designation earned years ago rests on an older edition. Track updates (e.g. changes to 62443-3-2 risk methodology, 4-2 component requirements) on isa.org and the ISA Global Cybersecurity Alliance (ISAGCA).
- **The threat landscape moves faster than the standard.** OT-targeting malware and techniques evolve; pair the certificate knowledge with current threat intelligence and the OT-monitoring product skills in the encyclopedia's OT volumes.
- **Verify course/exam specifics before registering.** Formats (classroom/virtual/online/modular) and exam logistics change; confirm on isa.org. This volume was verified 4 August 2026.

## The 62443 context in the encyclopedia

62443 is the **standards-and-lifecycle** layer above the OT product volumes:

- **OT visibility & enforcement products:** [Forescout XV](../../volume-015-forescout-platform-certifications/README.md), [Xage CXII](../../volume-112-xage-security-lab/README.md), [Claroty CXIII](../../volume-113-claroty-xdome-lab/README.md), [Nozomi CXIV](../../volume-114-nozomi-networks-lab/README.md), [TXOne CXV](../../volume-115-txone-networks-lab/README.md) — the tools that *implement* the monitoring, segmentation, and virtual patching 62443 requires.
- **Segmentation landscape:** [Microsegmentation Options LXXXVII](../../volume-087-microsegmentation-options/README.md) — the zones/conduits realized as products.
- **Broader defense:** [Enterprise Cybersecurity X](../../volume-010-enterprise-cybersecurity/README.md).

62443 tells you *what* protection an IACS needs and *why*; those product volumes show *how* specific tools deliver it.

## Hands-On Lab

### Lab 9.1 — Build your 62443 certification plan

**Objective:** Commit a route to Expert.

```bash
cat > my-62443-plan.md <<'EOF'
Role: assessor / architect / operations / consultant
Step 1: IC32 Fundamentals Specialist (mandatory gate)     target: ___
Then (any order, by current project):
  [ ] IC33 Risk Assessment Specialist   (Assess)
  [ ] IC34 Design Specialist            (Design)
  [ ] IC37 Maintenance Specialist       (Operate/Maintain)
All four -> ISA/IEC 62443 Cybersecurity Expert (automatic)
No renewal — but re-read the current standard editions on a cadence.
Verify course/exam details on isa.org before each registration.
EOF
cat my-62443-plan.md
```

**Expected result:** A plan gated on IC32, then the three specialists ordered by your work, ending at Expert — the structure this volume follows. The "re-read the current standard" line replaces the renewal a non-expiring credential lacks.

**Negative test:** A plan that treats the credentials as "done forever" with no re-reading — the standard moves; the discipline of tracking editions is the real currency mechanism here.

**Cleanup:** Keep the plan.

### Lab 9.2 — Map a control to the standard

**Objective:** Practice tracing any control back to the standard — the Expert habit.

```bash
python3 - <<'EOF'
# Given a deployed control, name the FR, the SL it supports, and the lifecycle role
control = "deny-by-default conduit between supervisory and control zones, with passive monitoring"
print(f"Control: {control}")
print("  FR:            FR5 Restricted Data Flow (+ FR6 Timely Response via monitoring)")
print("  Supports:      SL3 on RDF for the control zone")
print("  Standard:      62443-3-3 (system SRs), designed per 62443-3-2, operated per 62443-2-1")
print("  Lifecycle:     designed (IC34), verified, maintained/monitored (IC37)")
EOF
```

**Expected result:** The control traced to its FR, SL, standard part, and lifecycle phase — the fluency the Expert designation certifies: any control on an IACS should be explainable in the standard's own terms.

**Negative test:** Deploying a control you can't map to an FR/SL/standard part — it may be useful, but you can't defend it in an audit or a design review; 62443 fluency is speaking the standard's language.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Expert designation (all four certificates, no separate exam) understood.
- [ ] A route through the specialists chosen for your role.
- [ ] Currency habit installed (re-read evolving standard editions; verify on isa.org).
- [ ] 62443 placed as the standards layer above the OT product volumes.
