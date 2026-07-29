# Chapter 08: Cybersecurity Leadership

## Learning Objectives

- Lead a security program with governance and technical controls (GSLC).
- Build strategy, policy, and plans (GSTRT).
- Run a security operations function (GSOM).
- Prioritize with a controls framework (GCCC).
- Complete a walkthrough for each Leadership domain.

## Theory and Architecture

The **Cybersecurity Leadership** focus area validates managers and technical leaders. **GSLC
(Security Leadership)** covers governance plus the technical breadth a leader needs to protect,
detect, and respond across the security lifecycle — bridging management and technology. **GSTRT
(Strategic Planning, Policy, and Leadership)** covers building a security **strategy**, writing
**policy**, business alignment, and leading change. **GSOM (Security Operations Manager)** covers
building and running a **SOC** — team, process, metrics, and continuous improvement. **GCCC (Critical
Controls)** covers implementing and auditing the **CIS Critical Security Controls** — a prioritized,
measurable set of safeguards. **GCIL (Cyber Incident Leader)** covers leading the organization
through a major incident. These credentials translate technical work into **risk decisions, teams,
and programs**. This chapter teaches each with a hands-on walkthrough (risk prioritization, policy
structure, SOC metrics, CIS Controls mapping).

## Design Considerations

Align security to **business risk**, not just technology (GSTRT). Lead with **governance + measurable
controls** (GSLC/GCCC). Run the SOC on **metrics** (MTTD/MTTR) and continuous improvement (GSOM).
Prioritize with a **framework** (CIS Controls) so limited budget hits the highest-value safeguards.
Communicate to both **technical teams and executives**.

## Implementation and Automation

The labs prioritize risk, structure a policy, compute SOC metrics, and map CIS Controls.

## Validation and Troubleshooting

Confirm the Leadership map:

```text
GSLC = governance + technical breadth across the lifecycle. GSTRT = strategy/policy/business alignment.
GSOM = build & run the SOC (team/process/metrics). GCCC = CIS Critical Security Controls (prioritized, measurable).
```

Common pitfalls: buying tools with no **strategy or metrics**; and treating all risks equally instead
of **prioritizing** with a framework.

## Security and Best Practices

Lead with **risk-aligned strategy**, measurable **controls**, and SOC **metrics**. Prioritize with
the CIS Controls. Communicate risk in business terms. Build and develop the **team**. Leadership is a
defensive, program-level discipline.

## Hands-On Lab

Leadership walkthroughs. **Shared prerequisites** — Linux with `python3`, in a lab. **Cost:** none.

### Lab 8.1 — GSLC/GSTRT: prioritize risk for the roadmap

**Objective:** Turn risk into a plan.

```python
python3 - <<'PY'
risks=[{"risk":"no MFA on VPN","likelihood":5,"impact":5},
       {"risk":"legacy TLS on intranet","likelihood":2,"impact":2},
       {"risk":"no EDR on servers","likelihood":4,"impact":5}]
for r in sorted(risks,key=lambda x:-(x["likelihood"]*x["impact"])):
    print(f"score {r['likelihood']*r['impact']:>2}  {r['risk']}")
print("GSTRT: fund the highest risk-score items first; align to business impact")
PY
```

**Expected result:** risks ranked by **likelihood × impact** — a risk-driven roadmap (GSTRT).

**Negative test:** fund the loudest request instead of the highest **risk score**; scarce budget
misses the real exposure — prioritize by risk.

**Cleanup:** none.

### Lab 8.2 — GSOM: compute SOC metrics

**Objective:** Run the SOC on numbers.

```python
python3 - <<'PY'
incidents=[{"detect_min":30,"respond_min":90},{"detect_min":15,"respond_min":45},{"detect_min":60,"respond_min":120}]
mttd=sum(i["detect_min"] for i in incidents)/len(incidents)
mttr=sum(i["respond_min"] for i in incidents)/len(incidents)
print(f"MTTD={mttd:.0f} min  MTTR={mttr:.0f} min")
print("GSOM: track MTTD/MTTR over time; falling trend = improving SOC")
PY
```

**Expected result:** **MTTD/MTTR** computed for the SOC — the metrics GSOM manages by.

**Negative test:** report "we handled some incidents" with no metrics; leaders can't see trend or
improvement — measure **MTTD/MTTR**.

**Cleanup:** none.

### Lab 8.3 — GCCC: map to the CIS Critical Controls

**Objective:** Prioritize with a framework.

```python
python3 - <<'PY'
cis={"CIS 1":"Inventory of enterprise assets","CIS 4":"Secure configuration",
     "CIS 5":"Account management","CIS 6":"Access control management","CIS 8":"Audit log management"}
have={"CIS 1":True,"CIS 4":False,"CIS 5":True,"CIS 6":False,"CIS 8":True}
for c,name in cis.items():
    print(f"{c} {name:32}: {'implemented' if have[c] else 'GAP -> prioritize'}")
PY
```

**Expected result:** CIS Controls status with **gaps flagged** — the GCCC prioritization method.

**Negative test:** audit against an ad-hoc checklist; a recognized **framework** (CIS Controls) makes
gaps measurable and comparable — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cybersecurity Leadership spans governance and technical breadth (GSLC), strategy and policy (GSTRT),
running the SOC (GSOM), and prioritizing with the CIS Controls (GCCC) — translating technical work
into risk-aligned programs, teams, and measurable controls.

- [ ] I can prioritize risk for a roadmap (GSTRT).
- [ ] I can compute and use SOC metrics (GSOM).
- [ ] I can map to the CIS Critical Controls (GCCC).
- [ ] I understand governance-plus-technical leadership (GSLC).
- [ ] I completed Labs 8.1–8.3 including each negative test.
