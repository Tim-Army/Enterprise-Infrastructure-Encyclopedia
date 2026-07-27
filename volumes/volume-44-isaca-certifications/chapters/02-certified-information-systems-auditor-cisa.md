# Chapter 02: Certified Information Systems Auditor (CISA)

## Learning Objectives

- Explain what CISA certifies and its standing as the benchmark IS-audit credential.
- List the five CISA domains and their exam weights.
- Apply the IS-audit process: planning, evidence, controls, and reporting.
- Relate CISA concepts to governance, resilience, and asset protection.
- Complete a per-domain walkthrough for each CISA domain.

## Theory and Architecture

The **Certified Information Systems Auditor (CISA)** is the global benchmark for
professionals who **audit, control, and assure** information systems. It
certifies the ability to plan and execute a **risk-based audit**, evaluate
controls, gather evidence, and report findings to stakeholders. The exam is **150
questions** across five weighted job-practice domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Information Systems Auditing Process | 18% |
| 2 | Governance and Management of IT | 18% |
| 3 | Information Systems Acquisition, Development and Implementation | 12% |
| 4 | Information Systems Operations and Business Resilience | 26% |
| 5 | Protection of Information Assets | 26% |

**Operations/resilience (26%)** and **asset protection (26%)** together are more
than half the exam — the audit of running systems and their security dominates.

## Design Considerations

CISA rewards a **risk-based, evidence-driven** mindset. The auditor's job is not
to fix systems but to **assess** whether controls are designed and operating
effectively, and to document that with sufficient, reliable **evidence**. Study
the **audit process** (Domain 1) as the backbone, and treat every other domain as
a control area to audit. CISA pairs naturally with **CGEIT** (governance) and
**CRISC** (risk), and with the CISM security-management view.

## Implementation and Automation

Because auditing is a methodology, the labs below model the **artifacts and
decisions** of an audit: an audit plan and sampling, a governance/control
mapping, an SDLC control review, an operations/resilience (RTO/RPO) assessment,
and an asset-protection control test — the workpapers a CISA produces.

## Validation and Troubleshooting

Confirm the CISA blueprint before studying:

```text
isaca.org > Credentialing > CISA > Exam Content Outline:
  - five domains and weights (18/18/12/26/26), 150 questions
  - five years of IS audit/control experience (waivers available)
```

Common pitfalls: thinking like an **engineer** (fixing) instead of an **auditor**
(assessing with evidence); under-weighting the large **operations/resilience** and
**asset-protection** domains; and confusing **control design** with **operating
effectiveness** — an auditor tests both.

## Security and Best Practices

Audit against a **framework** (COBIT, NIST, ISO 27001), sample defensibly,
document evidence to a standard that supports the finding, and report with clear
**risk ratings** and recommendations. Maintain **independence** and objectivity —
the auditor's value is credibility. Renew via CPE and the annual maintenance fee.

## References and Knowledge Checks

- isaca.org: *CISA* Exam Content Outline and review manual; COBIT; NIST; ISO 27001.

**Knowledge checks**

1. Which two CISA domains together make up more than half the exam?
2. What is the difference between auditing control design and operating effectiveness?
3. Why is auditor independence essential?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CISA domain**.

**Shared prerequisites** — a Linux shell with `python3`. **Cost:** none.

### Lab 2.1 — CISA D1: Information Systems Auditing Process (18%)

**Objective:** Build a risk-based audit plan with sampling.

```bash
python3 - <<'PY'
areas = [("Change management", 5),("Access provisioning", 4),("Backup/restore", 3)]
areas.sort(key=lambda x:-x[1])
print("Risk-ranked audit scope (test highest risk first):")
for name,risk in areas: print(f"  {name:20} risk={risk}")
print("Sampling: for 1,000 changes, test a risk-weighted sample; document population + method.")
PY
```

**Expected result:** a risk-ranked scope and a sampling approach — the audit
planning that opens every CISA engagement (Domain 1).

**Negative test:** audit everything equally; a **risk-based** plan focuses effort
where it matters — rank by risk.

**Cleanup:** none.

### Lab 2.2 — CISA D2: Governance and Management of IT (18%)

**Objective:** Map an IT control to a governance framework objective.

```bash
python3 - <<'PY'
mapping = {"Board IT oversight":"COBIT EDM (Evaluate, Direct, Monitor)",
           "IT strategy alignment":"COBIT APO (Align, Plan, Organize)",
           "Change control":"COBIT BAI (Build, Acquire, Implement)"}
for control,obj in mapping.items(): print(f"{control:22} -> {obj}")
PY
```

**Expected result:** IT controls mapped to COBIT governance objectives — the
governance-audit linkage of Domain 2.

**Negative test:** audit IT in isolation from business governance; CISA assesses
IT **governance** — tie controls to enterprise objectives.

**Cleanup:** none.

### Lab 2.3 — CISA D3: IS Acquisition, Development and Implementation (12%)

**Objective:** Review SDLC controls at each phase.

```bash
python3 - <<'PY'
sdlc = {"Requirements":"security/control requirements documented + approved",
        "Design":"segregation of duties, control points designed in",
        "Testing":"UAT + security testing evidence",
        "Implementation":"change approval, rollback, post-implementation review"}
for phase,ctrl in sdlc.items(): print(f"{phase:14}: audit -> {ctrl}")
PY
```

**Expected result:** a control per SDLC phase to audit — the acquisition/
development review of Domain 3.

**Negative test:** review only production; controls must be built and evidenced
**across** the SDLC — audit each phase.

**Cleanup:** none.

### Lab 2.4 — CISA D4: IS Operations and Business Resilience (26%)

**Objective:** Assess recovery objectives against capability.

```bash
python3 - <<'PY'
rto_required, rto_actual = 60, 240   # minutes
rpo_required, rpo_actual = 15, 60
def gap(req,act,name): print(f"{name}: required {req}m vs actual {act}m -> {'FINDING' if act>req else 'OK'}")
gap(rto_required, rto_actual, "RTO"); gap(rpo_required, rpo_actual, "RPO")
PY
```

**Expected result:** RTO and RPO gaps flagged as findings — the operations/
resilience assessment that is CISA's largest domain (tied).

**Negative test:** accept a DR plan on paper without testing; audit the **tested**
recovery capability against the requirement — evidence, not intent.

**Cleanup:** none.

### Lab 2.5 — CISA D5: Protection of Information Assets (26%)

**Objective:** Test an access-control (least-privilege) design.

```bash
python3 - <<'PY'
access = {"analyst":{"read"},"admin":{"read","write","delete"},"contractor":{"read"}}
def review(role, perms):
    excess = perms - {"read"} if role in ("analyst","contractor") else set()
    return "OK" if not excess else f"FINDING: excess {excess}"
for r,p in access.items(): print(f"{r:11} {sorted(p)} -> {review(r,p)}")
PY
```

**Expected result:** access reviewed against least privilege, flagging excess
rights — the asset-protection control testing that ties for CISA's largest
domain.

**Negative test:** confirm access "looks fine" without a least-privilege baseline;
test against the **required** entitlements, not appearances.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CISA is the benchmark IS-audit credential: five domains weighted 18/18/12/26/26,
dominated by operations/resilience and asset protection. It certifies risk-based,
evidence-driven auditing of information systems — planning, control testing,
resilience, and asset protection — framed against COBIT/NIST/ISO and maintained
with CPE.

- [ ] I can list the five CISA domains and their weights.
- [ ] I can build a risk-based audit plan and sample defensibly.
- [ ] I can map controls to governance and audit the SDLC.
- [ ] I can assess RTO/RPO and test least-privilege access.
- [ ] I completed Labs 2.1–2.5 including each negative test.
