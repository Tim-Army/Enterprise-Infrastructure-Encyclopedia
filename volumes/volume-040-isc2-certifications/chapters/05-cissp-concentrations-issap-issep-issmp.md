# Chapter 05: CISSP Concentrations — ISSAP, ISSEP, ISSMP

## Learning Objectives

- Explain the three CISSP concentrations and their prerequisite (CISSP + 2 years).
- List the ISSAP, ISSEP, and ISSMP domains and their 1 August 2025 weights.
- Distinguish the architecture, engineering, and management specializations.
- Apply concentration-level thinking to architecture modeling, systems engineering, and security management.
- Complete a per-domain walkthrough for each domain of all three concentrations.

## Theory and Architecture

The three **CISSP concentrations** let a CISSP prove deep specialization. Each
requires an **active CISSP plus two years** of experience in the concentration's
area, and each was **rewritten with a new exam outline effective 1 August
2025** — a significant refresh that changed domain counts and weights, so any
pre-2025 study material is out of date.

- **ISSAP — Information Systems Security Architecture Professional** designs the
  security *architecture*: the models, patterns, and infrastructure that
  implement policy. **4 domains** (125 items, 3 hours):

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Governance, Risk, and Compliance (GRC) | 21% |
  | 2 | Security Architecture Modeling | 22% |
  | 3 | Infrastructure and System Security | 32% |
  | 4 | Identity and Access Management (IAM) Architecture | 25% |

- **ISSEP — Information Systems Security Engineering Professional** engineers
  security *into* systems across their lifecycle (aligned to systems-security-
  engineering practice such as NIST SP 800-160). **5 domains**:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Systems Security Engineering Foundations | 25% |
  | 2 | Risk Management | 14% |
  | 3 | Security Planning and Design | 30% |
  | 4 | Systems Implementation, Verification, and Validation | 14% |
  | 5 | Secure Operations, Change Management, and Disposal | 17% |

- **ISSMP — Information Systems Security Management Professional** *manages* the
  security program — leadership, lifecycle, risk, operations, continuity, and
  compliance. **6 domains** (125 items, 3 hours):

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Leadership and Organizational Management | 21% |
  | 2 | Systems Lifecycle Management | 15% |
  | 3 | Risk Management | 20% |
  | 4 | Security Operations | 18% |
  | 5 | Contingency Management | 12% |
  | 6 | Law, Ethics, and Security Compliance Management | 14% |

## Design Considerations

Choose the concentration that matches the **role you are growing into**, not the
one that looks most prestigious. An enterprise **security architect** who draws
reference architectures and selects patterns takes **ISSAP**. A **security
systems engineer** embedded in an SDLC or a systems-engineering program (common
in defense and critical infrastructure) takes **ISSEP**. A **security manager,
CISO track, or program lead** takes **ISSMP**. All three assume the CISSP CBK;
they go *deeper*, not broader, so study the concentration outline against your
actual project artifacts.

## Implementation and Automation

Because these are architecture, engineering, and management credentials, the
labs below are **design and modeling walkthroughs**: they produce the artifacts
these roles own — a defense-in-depth model, a trust-boundary diagram as data, a
requirements-traceability check, a change-control gate, a RACI/authority map, a
BIA, and a compliance-control crosswalk — rather than tool operation for its own
sake.

## Validation and Troubleshooting

Confirm each concentration's blueprint before studying:

```text
isc2.org > Certifications > ISSAP | ISSEP | ISSMP > Exam Outline:
  - domains and weights (all effective 1 August 2025 - NEW outlines)
  - 125 items, 3 hours; requires active CISSP + 2 years
```

Common pitfalls: using **pre-August-2025** material (ISSAP dropped to 4 domains;
all three were re-weighted); pursuing a concentration **without an active
CISSP** (it is a hard prerequisite); and confusing ISSEP's **engineering**
(building security in) with ISSAP's **architecture** (designing the model) or
ISSMP's **management** (running the program).

## Security and Best Practices

Anchor each specialization to a recognized framework: ISSAP to enterprise
architecture patterns and zero-trust reference models; ISSEP to **NIST SP
800-160** systems-security engineering and the RMF; ISSMP to governance, BC/DR,
and compliance regimes. Maintain the **parent CISSP** (concentrations lapse if
the CISSP does) and record CPE against both.

## References and Knowledge Checks

- isc2.org: *ISSAP*, *ISSEP*, *ISSMP* pages and Exam Outlines; *ISC2 Insights* on the 2025 advanced-certification refresh.

**Knowledge checks**

1. What single credential and experience do all three concentrations require?
2. How do ISSAP, ISSEP, and ISSMP divide the "design / build / run" of security?
3. What changed for the concentrations on 1 August 2025?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted domain of all three
concentrations** (ISSAP 4, ISSEP 5, ISSMP 6).

**Shared prerequisites** — a Linux shell with `python3`; `openssl` for one lab.
**Cost:** none.

### ISSAP — Architecture

### Lab 5.1 — ISSAP D1: Governance, Risk, and Compliance (21%)

**Objective:** Map a driver (law/policy/risk) to an architectural requirement.

```bash
python3 - <<'PY'
drivers = {"GDPR Art.32":"encrypt PII at rest and in transit",
           "PCI DSS":"segment the cardholder data environment",
           "Risk: ransomware":"immutable, offline backups"}
for d,req in drivers.items():
    print(f"{d:18} -> architecture requirement: {req}")
PY
```

**Expected result:** each governance/risk driver traced to a concrete
architectural requirement — the GRC-to-design linkage ISSAP tests.

**Negative test:** design controls first and retrofit compliance; drivers should
*originate* requirements, not be reverse-justified.

**Cleanup:** none.

### Lab 5.2 — ISSAP D2: Security Architecture Modeling (22%)

**Objective:** Express a layered defense-in-depth model as data.

```bash
python3 - <<'PY'
layers = ["perimeter (WAF/FW)","network (segmentation)","host (EDR/hardening)",
          "app (input validation)","data (encryption/DLP)","identity (MFA/RBAC)"]
for i,l in enumerate(layers,1): print(f"Layer {i}: {l}")
print("A single control failure at one layer is contained by the others.")
PY
```

**Expected result:** a six-layer defense-in-depth model — the kind of reference
model an ISSAP produces and defends.

**Negative test:** rely on a single strong perimeter; once breached there is no
depth — model multiple independent layers.

**Cleanup:** none.

### Lab 5.3 — ISSAP D3: Infrastructure and System Security (32%)

**Objective:** Define trust boundaries and required crossings for a 3-tier app.

```bash
python3 - <<'PY'
tiers = ["Internet","DMZ/web","app","database"]
for a,b in zip(tiers, tiers[1:]):
    print(f"{a:9} -> {b:9} : allow only required ports; authenticate + inspect at the boundary")
PY
```

**Expected result:** three trust-boundary crossings, each restricted and
authenticated — the infrastructure-security design that is ISSAP's heaviest
domain.

**Negative test:** allow the web tier to reach the database directly; the app
tier is the enforced boundary — do not bypass it.

**Cleanup:** none.

### Lab 5.4 — ISSAP D4: Identity and Access Management Architecture (25%)

**Objective:** Design federation/SSO token flow at a conceptual level.

```bash
python3 - <<'PY'
flow = ["User -> SP requests resource","SP -> IdP redirect (SAML/OIDC)",
        "IdP authenticates (MFA)","IdP -> signed assertion/token",
        "SP validates signature + claims -> grant"]
for step in flow: print(step)
PY
```

**Expected result:** the federated SSO sequence with a signed assertion — the
IAM architecture pattern ISSAP designs (SAML/OIDC, IdP/SP trust).

**Negative test:** have each application store its own passwords; that multiplies
credential risk — federate to a central IdP.

**Cleanup:** none.

### ISSEP — Engineering

### Lab 5.5 — ISSEP D1: Systems Security Engineering Foundations (25%)

**Objective:** Place security activities in the systems-engineering V-model.

```bash
python3 - <<'PY'
vmodel = {"Requirements":"security requirements + threat model",
          "Design":"security architecture + controls selection",
          "Implementation":"secure build + config",
          "Verification":"security test + assessment",
          "Validation":"accreditation + operational acceptance"}
for phase,act in vmodel.items(): print(f"{phase:14}: {act}")
PY
```

**Expected result:** security engineering activity mapped to each V-model phase —
the SP 800-160 mindset ISSEP is built on.

**Negative test:** add security only at verification; engineering security in
starts at requirements — "shift left."

**Cleanup:** none.

### Lab 5.6 — ISSEP D2: Risk Management (14%)

**Objective:** Walk the RMF steps that gate an engineered system.

```bash
python3 - <<'PY'
rmf = ["Prepare","Categorize","Select","Implement","Assess","Authorize","Monitor"]
print(" -> ".join(rmf))
print("Authorize (ATO) is a risk-acceptance decision by the Authorizing Official.")
PY
```

**Expected result:** the seven-step RMF ending in continuous monitoring — the
risk process ISSEP applies to systems.

**Negative test:** treat authorization as a one-time checkbox; RMF's final step
is *continuous* monitoring — risk is managed over time.

**Cleanup:** none.

### Lab 5.7 — ISSEP D3: Security Planning and Design (30%)

**Objective:** Trace a security requirement to a design control (traceability).

```bash
python3 - <<'PY'
matrix = [("SR-1 encrypt PII","AES-256 at rest + TLS1.2+ in transit"),
          ("SR-2 authenticate users","MFA via central IdP"),
          ("SR-3 audit access","centralized, tamper-evident logging")]
for req,ctrl in matrix: print(f"{req:22} -> design control: {ctrl}")
PY
```

**Expected result:** each security requirement mapped to a design control — the
requirements-traceability matrix that is ISSEP's heaviest domain.

**Negative test:** implement controls with no requirement behind them; every
control should trace to a requirement, and every requirement to a control.

**Cleanup:** none.

### Lab 5.8 — ISSEP D4: Systems Implementation, Verification, and Validation (14%)

**Objective:** Verify an implemented control meets its requirement (a test case).

```bash
openssl s_client -connect www.isc2.org:443 -tls1_1 2>&1 | grep -qi "protocol" \
  && echo "TLS1.1 negotiated (FAIL requirement SR-1)" \
  || echo "TLS1.1 refused -> PASS: meets 'TLS1.2+' requirement"
```

**Expected result:** `TLS1.1 refused -> PASS` — a verification test proving the
implementation satisfies the security requirement, ISSEP's V&V activity.

**Negative test:** declare a control "done" without a test; verification requires
*evidence* that the requirement is met.

**Cleanup:** none.

### Lab 5.9 — ISSEP D5: Secure Operations, Change Management, and Disposal (17%)

**Objective:** Gate a change and define secure disposal (sanitization).

```bash
python3 - <<'PY'
change = {"request":"open firewall 8443","security_review":"required",
          "approved_by":"CAB","rollback":"documented","post_verify":"scan"}
for k,v in change.items(): print(f"{k:15}: {v}")
print("Disposal: NIST 800-88 -> Clear / Purge / Destroy by media + sensitivity")
PY
```

**Expected result:** a change gated by security review and rollback, plus the
NIST 800-88 sanitization tiers — the operate-and-dispose end of the lifecycle.

**Negative test:** decommission a disk by deleting files; deletion is not
sanitization — purge or destroy per data sensitivity.

**Cleanup:** none.

### ISSMP — Management

### Lab 5.10 — ISSMP D1: Leadership and Organizational Management (21%)

**Objective:** Build a RACI for a security decision to clarify authority.

```bash
python3 - <<'PY'
raci = {"CISO":"A","Security Eng":"R","IT Ops":"C","Legal":"C","Board":"I"}
for role,r in raci.items(): print(f"{role:14}: {r}")
print("R=Responsible A=Accountable C=Consulted I=Informed (exactly one A).")
PY
```

**Expected result:** a RACI with a single Accountable owner — the
organizational-authority clarity ISSMP leadership requires.

**Negative test:** assign two Accountable parties; accountability must be
singular or decisions stall — exactly one "A."

**Cleanup:** none.

### Lab 5.11 — ISSMP D2: Systems Lifecycle Management (15%)

**Objective:** Attach security gates to each lifecycle phase (governance view).

```bash
python3 - <<'PY'
gates = {"Initiate":"security categorization","Acquire/Develop":"secure SDLC + review",
         "Implement":"ATO / go-live gate","Operate":"continuous monitoring",
         "Dispose":"sanitization + records retention"}
for ph,g in gates.items(): print(f"{ph:16} gate -> {g}")
PY
```

**Expected result:** a security gate per lifecycle phase — the management-level
oversight of the system lifecycle ISSMP owns.

**Negative test:** manage only the build phase; security governance spans
initiate-to-dispose, not just development.

**Cleanup:** none.

### Lab 5.12 — ISSMP D3: Risk Management (20%)

**Objective:** Build a risk-treatment decision (accept/mitigate/transfer/avoid).

```bash
python3 - <<'PY'
def treat(ale, control_cost):
    if control_cost < ale*0.5: return "MITIGATE (control cheaper than risk)"
    if ale < 5000: return "ACCEPT (low residual risk)"
    return "TRANSFER (insure) or AVOID"
for name,ale,cost in [("DDoS",80000,15000),("Minor defacement",3000,20000)]:
    print(f"{name:18} ALE ${ale:,} cost ${cost:,} -> {treat(ale,cost)}")
PY
```

**Expected result:** DDoS → MITIGATE, minor defacement → ACCEPT — risk-treatment
decisions a security manager defends, ISSMP's second-heaviest domain.

**Negative test:** mitigate every risk regardless of cost; some risks are cheaper
to accept or transfer — treatment is an economic decision.

**Cleanup:** none.

### Lab 5.13 — ISSMP D4: Security Operations (18%)

**Objective:** Define SOC alerting metrics (MTTD/MTTR) that a manager governs.

```bash
python3 - <<'PY'
incidents = [(12,240),(5,60),(30,180)]  # (detect_min, resolve_min)
mttd = sum(d for d,_ in incidents)/len(incidents)
mttr = sum(r for _,r in incidents)/len(incidents)
print(f"MTTD = {mttd:.0f} min, MTTR = {mttr:.0f} min")
print("Manager's job: drive both down with tuning, automation, and staffing.")
PY
```

**Expected result:** MTTD ~16 min and MTTR ~160 min — the operational metrics an
ISSMP manages, not the packet-level work SSCP does.

**Negative test:** measure alert *volume* as success; fewer, higher-fidelity
alerts and faster MTTR matter more than raw counts.

**Cleanup:** none.

### Lab 5.14 — ISSMP D5: Contingency Management (12%)

**Objective:** Produce a Business Impact Analysis ranking by criticality.

```bash
python3 - <<'PY'
bia = [("Payments",1,15),("Email",3,120),("Marketing site",4,480)]  # (rank,RTO min)
for svc,rank,rto in sorted(bia,key=lambda x:x[1]):
    print(f"{svc:16} criticality {rank}  RTO {rto} min")
print("Recovery sequence follows criticality: restore Payments first.")
PY
```

**Expected result:** services ordered by criticality with RTOs — the BIA that
drives BC/DR priorities, ISSMP's contingency domain.

**Negative test:** restore easiest systems first during a disaster; recover by
**business criticality**, per the BIA.

**Cleanup:** none.

### Lab 5.15 — ISSMP D6: Law, Ethics, and Security Compliance Management (14%)

**Objective:** Crosswalk one control to multiple compliance regimes.

```bash
python3 - <<'PY'
control = "Encrypt PII at rest"
maps = {"GDPR":"Art. 32","PCI DSS":"Req. 3","HIPAA":"164.312(a)(2)(iv)",
        "ISO 27001":"A.8.24"}
print(f"Control: {control}")
for reg,ref in maps.items(): print(f"  satisfies {reg:10} {ref}")
PY
```

**Expected result:** one control mapped across GDPR, PCI, HIPAA, and ISO 27001 —
the compliance crosswalk an ISSMP maintains, plus the binding ISC2 ethics
obligation.

**Negative test:** track each regulation's controls separately; a crosswalk
shows one control often satisfies many — reduce duplicated effort.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The three CISSP concentrations certify depth: ISSAP designs the architecture (4
domains), ISSEP engineers security across the lifecycle (5 domains), and ISSMP
manages the program (6 domains). All require an active CISSP plus two years and
were re-issued with new outlines effective 1 August 2025 — study only current
material.

- [ ] I can name the three concentrations and their prerequisite.
- [ ] I can list each concentration's domains and 2025 weights.
- [ ] I can produce an architecture model, a traceability matrix, and a BIA.
- [ ] I can explain the design / build / run division across ISSAP/ISSEP/ISSMP.
- [ ] I completed Labs 5.1–5.15 including each negative test.
