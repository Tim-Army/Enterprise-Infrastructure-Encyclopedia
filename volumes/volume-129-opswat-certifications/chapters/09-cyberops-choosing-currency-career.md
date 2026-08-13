# Chapter 09: The CyberOps Track, Choosing a Path, and Currency

## Learning Objectives

- Cover the CyberOps track: hands-on defensive and analysis skills.
- Choose and sequence the OPSWAT certifications for your role.
- Keep credentials current given the free-first model and validity windows.

## The CyberOps track

Beyond CIP Essentials, OPSWAT Academy's **CyberOps** track is hands-on: red/blue team skills, ethical hacking fundamentals, OSINT, protocol analysis, and **PLC security**. In an encyclopedia framing this is **authorized, defensive** skill-building — understanding attacker techniques to defend critical infrastructure, always in an authorized, educational context. It complements the file/endpoint/network defenses of the Associate track with the analysis and detection side.

| CyberOps area | Defensive use |
|:---|:---|
| Protocol analysis | Understand OT protocols (Modbus, DNP3) to baseline and detect anomalies |
| PLC security | Understand control-device weaknesses to protect them |
| OSINT | Know your organization's exposed footprint to reduce it |
| Red/blue fundamentals | Test and validate your own defenses (authorized) |

## Choosing a path

The free-first model means you can build a real foundation at no cost:

| If your role is… | Start (free) with | Then |
|:---|:---|:---|
| New to CIP/security | ICIP + OCFA | OFSA |
| File/email/web security | OFSA | MetaDefender Core/ICAP Professional |
| Endpoint/network admin | OECA + ONSA | MetaAccess deployment |
| OT/critical-infrastructure defender | ICIP + OFSA + OECA | OSSA → **OT Security Expert** |
| SOC/analyst | OCFA + CyberOps | protocol analysis, detection |

The natural CIP spine: **ICIP → OFSA (CDR/multiscan) → OECA/ONSA (device/network) → OSSA (boundary) → OT Security Expert**. Take the free Associates first (they stand alone on a résumé and carry ISC2 CPE credit), then the paid Professionals where your work uses the MetaDefender products.

## The OPSWAT context in the encyclopedia

OPSWAT sits at the **data-and-device boundary** of critical-infrastructure defense, alongside:

- [Volume CXXVIII — ISA/IEC 62443](../../volume-128-isa-iec-62443-certifications/README.md) — the standard and lifecycle; OPSWAT's kiosk/vault/CDR *implement* 62443's boundary controls.
- OT monitoring products — [Claroty CXIII](../../volume-113-claroty-xdome-lab/README.md), [Nozomi CXIV](../../volume-114-nozomi-networks-lab/README.md), [TXOne CXV](../../volume-115-txone-networks-lab/README.md) — passive detection inside the OT network.
- [Volume X — Enterprise Cybersecurity](../../volume-010-enterprise-cybersecurity/README.md) — the broader defensive program.

OPSWAT's distinctive angle is the **file/media/data-transfer boundary** — the CDR, multiscanning, kiosk, and vault that most other vendors don't center on.

## Currency

- **The free-first model can change.** Which courses are free and which are paid shifts; verify on opswatacademy.com before planning.
- **Some certifications expire.** Associate badges have carried validity windows (Credly shows expiry); re-verify validity and renew/retake as required.
- **Products evolve.** MetaDefender capabilities (engine count, CDR file-type coverage, new products) advance; the Professional exams follow. Track current platform capabilities, not a cached list. Verified 4 August 2026.

## Hands-On Lab

### Lab 9.1 — Build your OPSWAT certification plan

**Objective:** Commit a free-first, role-aligned plan.

```bash
cat > my-opswat-plan.md <<'EOF'
Role: new / file-sec / endpoint-net / OT-defender / SOC
Free foundation: ICIP + OCFA                          target: ___
Associates (free, per role): OFSA / OECA / ONSA / OSSA -> ___
Professionals (paid, where products are used): MetaDefender Core / ICAP / Kiosk / MFT
Expert: OPSWAT OT Security Expert (OT-defender capstone)
CPE: log ISC2 CPE credits for CISSP/SSCP/CCSP maintenance.
Validity: check Credly expiry; re-verify free-vs-paid on opswatacademy.com.
EOF
cat my-opswat-plan.md
```

**Expected result:** A plan that front-loads the free Associates and adds paid Professionals only where your work uses the products — the free-first model used deliberately. The CPE line captures the side benefit of maintaining an ISC2 credential.

**Negative test:** A plan that jumps to paid product Professionals without the free CIP/Associate foundation — you learn the buttons without the boundary-defense concepts the Associates teach; the free foundation is the point.

**Rollback:** Keep the plan.

### Lab 9.2 — Currency check

**Objective:** Make re-verification routine.

```bash
cat <<'EOF'
Before relying on this volume, re-check on opswatacademy.com:
  [ ] which certs are currently FREE vs paid (the model shifts)
  [ ] validity/expiry of the Associate certs (Credly)
  [ ] current MetaDefender products + Professional cert lineup
  [ ] OT Security Expert requirements
EOF
echo "verified 4 Aug 2026 — re-verify before scheduling"
```

**Expected result:** A short checklist covering the free-vs-paid shift, validity windows, and product lineup — the currency habits a free-first, product-linked program needs.

**Negative test:** Assuming "free forever" and "never expires" — both have exceptions here; opswatacademy.com and Credly are authoritative.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The CyberOps track (authorized/defensive analysis skills) understood.
- [ ] A free-first, role-aligned path chosen (ICIP → OFSA → OECA/ONSA → OSSA → OT Expert).
- [ ] Currency habits installed (free-vs-paid shifts, cert validity, product lineup).
- [ ] OPSWAT placed as the file/media/data-transfer boundary of CIP defense.
