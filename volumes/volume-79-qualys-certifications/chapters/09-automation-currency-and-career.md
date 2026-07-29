# Chapter 09: Automation, Currency, and Career

## Learning Objectives

- Automate with Qualys Flow (QFlow) and Custom Assessment and Remediation (CAR).
- Query and integrate with QQL and the API.
- Keep skills current as the platform evolves.
- Plan a career across the Qualys paths.
- Complete a walkthrough for automation and currency.

## Theory and Architecture

Qualys's final layer is **automation and integration**, which scales the whole platform. **Qualys Flow
(QFlow)** is a **no-code** workflow engine — visual flows that automate identity/security tasks
(auto-tag new assets, open a ticket when a critical exploitable vuln appears, trigger a patch job).
**Custom Assessment and Remediation (CAR)** runs **custom scripts** through the Cloud Agent to assess
or fix conditions Qualys doesn't check natively — extending detection and response with your own
logic, safely and centrally. **QQL (Qualys Query Language)** and the **REST API** enable integration:
export findings to a SIEM/ticketing system, build custom dashboards, and drive Qualys from CI/CD.
Together these turn Qualys from a console into a **programmable security platform**. On **currency**:
Qualys evolves continuously (the shift to **Enterprise TruRisk**, new applications like TotalCloud and
TotalAppSec), and its training is **free** and updated — so revisiting qualys.com is low-cost and
worthwhile. This closing chapter teaches automation and turns the volume into a durable career and
currency plan.

## Design Considerations

Automate repetitive tasks with **QFlow** (least code, auditable). Extend native checks with **CAR**
scripts (tested, least-privilege). Integrate via **QQL/API** into SIEM/ticketing/CI-CD. Keep skills
current with the **free** training as the platform evolves. Match certifications to your **career**
path.

## Implementation and Automation

The labs build a QFlow, outline a CAR script, and plan currency/career.

## Validation and Troubleshooting

Confirm the automation/currency map:

```text
QFlow = no-code automation (auto-tag, ticket, trigger patch). CAR = custom scripts via Cloud Agent (assess/remediate what's not native). QQL + REST API = integration (SIEM/ticketing/CI-CD, dashboards).
Currency: platform evolves (Enterprise TruRisk, TotalCloud/TotalAppSec); training is FREE and updated. Track qualys.com.
```

Common pitfalls: scripting what **QFlow** does natively (harder to audit); and running **CAR** scripts
without testing/least-privilege.

## Security and Best Practices

Automate with **QFlow**, extend safely with **CAR** (tested, least-privilege), integrate via
**QQL/API**, and keep skills current with **free** training. Match certs to your career. All work is
defensive.

## Hands-On Lab

Automation/currency walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Build a QFlow automation

**Objective:** No-code security automation.

```python
python3 - <<'PY'
def qflow(event):
    if event["type"]=="new_asset":
        return ["auto-tag by OS/exposure","assign to VMDR scan","notify owner"]
    if event["type"]=="critical_exploitable_vuln":
        return ["open high-priority ticket","trigger patch job","alert SOC"]
    return []
print("new asset ->", qflow({"type":"new_asset"}))
print("critical vuln ->", qflow({"type":"critical_exploitable_vuln"}))
PY
```

**Expected result:** event-driven **no-code** flows (tag/ticket/patch) — QFlow automation.

**Negative test:** handle new assets and critical vulns manually; it doesn't scale — automate with
**QFlow**.

**Cleanup:** none.

### Lab 9.2 — Outline a CAR remediation script

**Objective:** Extend with custom logic.

```python
python3 - <<'PY'
# CAR (Custom Assessment and Remediation) via Cloud Agent — pseudo:
car={"assess":"check registry key HKLM\\...\\InsecureFlag == 1","remediate":"set InsecureFlag = 0",
     "scope":"tag:Windows-Servers","safety":"tested in lab + least-privilege + logged"}
for k,v in car.items(): print(f"{k:10}: {v}")
print("CAR: custom assess/remediate what Qualys doesn't check natively — tested + scoped")
PY
```

**Expected result:** a scoped, tested **CAR** assess-and-remediate outline — custom extension.

**Negative test:** push an untested CAR script fleet-wide; it could break systems — **test** and scope
first.

**Cleanup:** none.

### Lab 9.3 — Plan currency and career

**Objective:** Keep skills and path current.

```python
python3 - <<'PY'
routine={"Training":"FREE Qualys Certified Specialist courses — updated with the platform",
         "Platform":"track Enterprise TruRisk + new apps (TotalCloud/TotalAppSec) on qualys.com",
         "Automation":"learn QQL -> QFlow -> CAR -> API for scale",
         "Career":"VMDR -> CSAM/TruRisk -> Policy/PCI or TotalCloud/EDR by role"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — free training, platform tracking, automation, and
a path.

**Negative test:** learn one module and stop; the platform is **broad and evolving** — keep learning
via the free courses.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Qualys automation (QFlow no-code, CAR custom scripts, QQL/API integration) turns the platform
programmable; with free, continuously-updated training and the shift to Enterprise TruRisk, learning
the automation layer and following the platform keeps you current.

- [ ] I can build a QFlow automation.
- [ ] I can outline a CAR remediation script.
- [ ] I can plan currency with free training.
- [ ] I can plan a career across the Qualys paths.
- [ ] I completed Labs 9.1–9.3 including each negative test.
