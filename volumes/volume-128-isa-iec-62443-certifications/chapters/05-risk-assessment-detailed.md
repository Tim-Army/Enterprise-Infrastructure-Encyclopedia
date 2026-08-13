# Chapter 05: Risk Assessment (IC33) — Detailed Assessment and Target Security Levels

## Learning Objectives

- Cover the IC33 detailed risk assessment: per-zone threat/vulnerability analysis and residual risk.
- Determine the Target Security Level (SL-T) for each zone and conduit.
- Model the detailed-assessment loop that outputs SL-T and a gap list.

## From high-level to detailed

The detailed risk assessment (per IEC 62443-3-2) takes each prioritized zone/conduit and works it in depth:

1. **Identify threats and vulnerabilities** for the zone.
2. **Determine unmitigated (inherent) risk** — likelihood × consequence *before* countermeasures.
3. **Determine the Target Security Level (SL-T)** — the SL vector the zone must achieve to reduce risk to tolerable.
4. **Compare to existing controls (SL-A)** — the gap.
5. **Identify countermeasures** to close the gap, then re-score **residual risk**.

The key output is **SL-T per zone/conduit** — the requirement that the Design certificate ([Chapters 06–07](06-design-requirements.md)) turns into an architecture.

## Hands-On Lab

Python models the detailed loop and SL-T determination. **Cost:** none.

### Lab 5.1 — Threat/vulnerability to inherent risk

**Objective:** Score a zone's inherent risk before countermeasures.

```bash
python3 - <<'EOF'
# For the control zone: enumerate threats x vulnerabilities -> inherent risk
threats = [
  {"threat":"USB-borne malware", "vuln":"no removable-media control", "L":3, "C":5},
  {"threat":"lateral move from IT", "vuln":"flat conduit, weak auth", "L":3, "C":5},
  {"threat":"unpatched PLC firmware CVE", "vuln":"no patch process", "L":2, "C":4},
]
for t in threats:
    inherent = t["L"] * t["C"]
    print(f"inherent risk {inherent:2}  <- {t['threat']} via {t['vuln']}")
worst = max(t["L"]*t["C"] for t in threats)
print(f"\nzone inherent (worst) = {worst}  -> drives SL-T")
EOF
```

**Expected result:** Per-threat inherent risk, with the worst case (15) driving the zone's protection requirement. The detailed assessment enumerates **threat × vulnerability** pairs — a vulnerability with no threat, or a threat with no vulnerability, is not a risk; both must be present.

**Negative test:** Listing vulnerabilities alone (a scanner dump) and calling it a risk assessment — 62443 requires the threat and the consequence too; a CVE with no reachable threat path and no consequence is not top-priority.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Determine SL-T from tolerable risk

**Objective:** Map inherent risk to a Target Security Level vector.

```bash
python3 - <<'EOF'
# SL-T: the SL needed to bring inherent risk down to the organization's tolerable level.
# Higher inherent risk (esp. safety consequence) -> higher SL-T across the relevant FRs.
def sl_t(inherent, safety):
    base = 1
    if inherent >= 15 or safety: base = 3
    elif inherent >= 9: base = 2
    # the FRs most relevant to the threats above: IAC, UC, RDF, SI
    return {"IAC":base, "UC":base, "SI":base, "DC":1, "RDF":base, "TRE":max(base-1,1), "RA":base}
target = sl_t(15, safety=True)
print("Control zone SL-T vector:")
for fr, v in target.items(): print(f"  {fr}: SL{v}")
EOF
```

**Expected result:** An SL-T vector of mostly SL3 for the high-risk control zone (safety consequence pushes it up), with data confidentiality low (OT rarely prioritizes DC). SL-T is **derived from tolerable risk**, not chosen arbitrarily — the higher the inherent (especially safety) risk, the higher the SL-T on the relevant FRs.

**Negative test:** Setting SL-T to SL4 everywhere "to be safe" — SL4 is for nation-state-resistant zones and is expensive/operationally heavy; over-specifying SL-T wastes resources and can hurt availability. SL-T must match the risk, not exceed it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Gap analysis and residual risk

**Objective:** Compare SL-T to SL-A and score residual risk after countermeasures.

```bash
python3 - <<'EOF'
FRS = ["IAC","UC","SI","DC","RDF","TRE","RA"]
sl_t = {"IAC":3,"UC":3,"SI":3,"DC":1,"RDF":3,"TRE":2,"RA":3}
sl_a = {"IAC":1,"UC":1,"SI":2,"DC":1,"RDF":2,"TRE":1,"RA":3}   # current controls
print("FR   SL-T SL-A  gap -> countermeasure needed")
for fr in FRS:
    gap = sl_t[fr] - sl_a[fr]
    note = "OK" if gap <= 0 else f"+{gap} (design work)"
    print(f"{fr:<4} {sl_t[fr]:^4}{sl_a[fr]:^4}  {note}")
gaps = sum(max(sl_t[f]-sl_a[f],0) for f in FRS)
print(f"\ntotal SL gap = {gaps} FR-levels -> hand to Design (IC34); residual risk re-scored after")
EOF
```

**Expected result:** A per-FR gap list (IAC/UC/RDF below target) totaling the design work, with residual risk to be re-scored once countermeasures close the gap. This gap list is the **deliverable that feeds the Design certificate** — the assessment says *what* protection is needed; design says *how*.

**Negative test:** Declaring the zone "assessed" without residual-risk re-scoring after countermeasures — you don't know if the design actually brings risk to tolerable; the loop closes only when residual risk is acceptable (or formally accepted).

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Threat × vulnerability → inherent risk scored per zone.
- [ ] SL-T vectors derived from tolerable risk (not chosen arbitrarily).
- [ ] Gap analysis (SL-T vs SL-A) and residual-risk re-scoring completed.
- [ ] IC33 Risk Assessment coverage complete across Chapters 04–05.
