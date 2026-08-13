# Chapter 09: Guardian, Currency, and Career

## Learning Objectives

- Design an enterprise Identity Security architecture (Guardian).
- Build a PAM program and strategy.
- Keep credentials current as the platform evolves.
- Plan a career across the CyberArk progression.
- Complete a walkthrough for architecture and currency.

## Theory and Architecture

The **Guardian** is CyberArk's highest credential — validating the ability to **combine organizational
architecture with Identity Security strategy** across the full platform. A Guardian designs an
**enterprise PAM program**: which accounts to onboard first (risk-ranked — domain admins, then service
accounts, then the long tail), how to phase from **standing privilege to just-in-time and zero
standing privileges**, how to integrate PAM with **Identity, EPM, Secrets Manager, and Secure Cloud
Access**, and how to measure progress (percentage of privileged accounts managed, sessions isolated,
secrets removed from code). It is a **strategy and architecture** role, not just operations. On
**currency**: CyberArk's platform is evolving — now **part of Palo Alto Networks** and progressively
rebranding toward **Idira** — while the **component architecture and Defender/Sentry/Guardian
credentials remain**, so tracking cyberark.com is ongoing (exam names, delivery, and product
capabilities change). This closing chapter teaches architectural thinking and turns the volume into a
durable career and renewal plan.

## Design Considerations

Risk-rank the **privileged account onboarding** roadmap. Drive toward **JIT/ZSP** and **least standing
privilege** across the platform. Integrate PAM with **Identity/EPM/Secrets/Cloud**. Measure with clear
**metrics**. Track platform changes (Palo Alto Networks / Idira) on cyberark.com. Match certifications
to your **career** direction.

## Implementation and Automation

The labs risk-rank onboarding, define program metrics, and plan currency/career.

## Validation and Troubleshooting

Confirm the Guardian/currency map:

```text
Guardian = enterprise Identity Security architecture + strategy across PAM/Identity/EPM/Secrets/Cloud. Risk-ranked onboarding; drive to JIT/ZSP; measure.
Currency: CyberArk now part of Palo Alto Networks, rebranding toward Idira; architecture + Defender/Sentry/Guardian credentials remain. Track cyberark.com.
```

Common pitfalls: onboarding accounts **alphabetically** instead of by risk; and a program with **no
metrics** to show progress.

## Security and Best Practices

Design a **risk-ranked**, phased PAM program driving to **JIT/ZSP**, integrate the platform, and
**measure** progress. Track platform evolution (Palo Alto Networks / Idira). Renew as required. All
work is defensive Identity Security architecture.

## Hands-On Lab

Guardian and currency walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Risk-rank the onboarding roadmap

**Objective:** Onboard the riskiest accounts first.

```python
python3 - <<'PY'
accounts=[{"type":"Domain Admin","count":12,"risk":10},{"type":"Service accounts","count":800,"risk":7},
          {"type":"Local admins","count":5000,"risk":6},{"type":"App API keys","count":300,"risk":8}]
for a in sorted(accounts,key=lambda x:-x["risk"]):
    print(f"risk {a['risk']:>2}  {a['type']:16} ({a['count']}) -> onboard priority")
print("Guardian: onboard by RISK (domain admins first), not alphabetically")
PY
```

**Expected result:** an onboarding roadmap ordered by **risk** (domain admins first) — Guardian
program design.

**Negative test:** onboard 5000 local admins before 12 domain admins; you protect the low-risk first —
**risk-rank** it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Define PAM program metrics

**Objective:** Measure progress.

```python
python3 - <<'PY'
metrics={"% privileged accounts managed":"1120 / 6112 = 18% (target 90%)",
         "% sessions isolated (PSM)":"64%","% secrets removed from code":"40%",
         "standing cloud roles remaining":"37 (target 0 via ZSP)"}
for m,v in metrics.items(): print(f"{m:34}: {v}")
print("Guardian: a PAM program is measured, not declared 'done'")
PY
```

**Expected result:** program **metrics** showing coverage and gaps — Guardian measurement.

**Negative test:** report "we deployed CyberArk" with no coverage metrics; leadership can't see risk
reduction — **measure** it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Plan currency and career

**Objective:** Keep credentials and skills current.

```python
python3 - <<'PY'
routine={"Progression":"Trustee -> Defender -> Sentry -> Guardian (+ product Defenders: EPM/Privilege Cloud)",
         "Platform":"track changes on cyberark.com (Palo Alto Networks integration, Idira rebrand)",
         "Practice":"authorized CyberArk lab/trial for hands-on",
         "Renewal":"recertify per CyberArk policy as versions evolve"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — progression, platform tracking, practice, and
renewal.

**Negative test:** assume the exams never change after the Palo Alto acquisition; **verify** current
names/delivery on cyberark.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Guardian designs and drives an enterprise Identity Security program — risk-ranked onboarding,
JIT/ZSP, platform integration, and metrics; because CyberArk is evolving under Palo Alto Networks
(Idira) while the credentials remain, tracking the platform and recertifying keeps you current.

- [ ] I can risk-rank the onboarding roadmap.
- [ ] I can define PAM program metrics.
- [ ] I can plan currency and renewal.
- [ ] I can plan a career across the progression.
- [ ] I completed Labs 9.1–9.3 including each negative test.
