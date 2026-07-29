# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Prepare for SUSE's Questionmark-delivered exams.
- Practice hands-on with free SUSE/openSUSE tools.
- Keep credentials current across product versions.
- Plan a career across the SUSE portfolio.
- Complete a walkthrough for exam prep and currency.

## Theory and Architecture

SUSE certifications are delivered through **Questionmark** (remote, proctored), so preparation combines
**conceptual knowledge** and **practical decision-making** across the exam domains. Effective prep
combines the **official SUSE training** for the target certification, the **product documentation**
(documentation.suse.com), and **hands-on practice** — and SUSE makes practice accessible: **openSUSE
Leap** (a free community distribution close to SLES) for Linux administration, **K3s** for Kubernetes,
and free trials for SLES and Rancher. On **currency**: SUSE refreshes exams with **product versions**
(SLES 15 and later, Rancher releases), so a certification is tied to a version and should be renewed as
products advance — tracking suse.com is ongoing. A SUSE career can span **Linux administration**
(SCA/SCE in SUSE Linux Enterprise), **cloud-native** (Rancher/Kubernetes), **fleet management** (SUSE
Manager), and **container security** (NeuVector). This closing chapter turns the volume into a durable
exam-prep, currency, and career plan.

## Design Considerations

Prepare with **official training + docs + hands-on** (openSUSE/K3s free). Match the exam to the
**product version** you'll be tested on. Renew as **product versions** advance. Match certifications to
your **career** direction across Linux, cloud-native, fleet, and security.

## Implementation and Automation

The labs plan prep, verify a free practice setup, and plan currency/career.

## Validation and Troubleshooting

Confirm the prep/currency model:

```text
Exams: Questionmark (remote proctored), conceptual + practical decision-making. Prepare: official training + documentation.suse.com + hands-on (openSUSE Leap, K3s, free trials).
Currency: exams tied to product versions (SLES 15+, Rancher releases) -> renew as products advance. Track suse.com.
```

Common pitfalls: studying the wrong **product version**; and concepts-only prep with no **hands-on**.

## Security and Best Practices

Prepare with training, docs, and **hands-on** practice on free tools, match the **product version**,
and renew as products advance. Match certs to your career. All practice is authorized.

## Hands-On Lab

Prep and currency walkthroughs. **Shared prerequisites** — `python3`; openSUSE/K3s optional. **Cost:**
none.

### Lab 9.1 — Plan exam preparation

**Objective:** Cover concepts and practice.

```python
python3 - <<'PY'
prep={"Training":"official SUSE course for the target cert (SCA/SCDS/SCE + product)",
      "Docs":"documentation.suse.com (SLES/Rancher/SUSE Manager/NeuVector)",
      "Hands-on":"openSUSE Leap (Linux) + K3s (Kubernetes) + free SLES/Rancher trials",
      "Domains":"map study to the exam's domain list (e.g., SCA_SLES15 domains)"}
for k,v in prep.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** a prep plan covering **concepts + hands-on** across the domains — balanced
preparation.

**Negative test:** memorize commands with no **hands-on**; SUSE exams test practical decisions —
practice.

**Cleanup:** none.

### Lab 9.2 — Verify a free practice setup

**Objective:** Practice at no cost.

```bash
for t in zypper systemctl kubectl; do command -v "$t" >/dev/null && echo "$t: ok" || echo "$t: install (openSUSE Leap for zypper/systemctl; K3s for kubectl)"; done
echo "SUSE practice: openSUSE Leap (free, close to SLES) + K3s (free K8s) cover most hands-on"
```

**Expected result:** a **free** practice toolset check — accessible hands-on preparation.

**Negative test:** assume you need a paid SLES license to practice; **openSUSE Leap** is free and
close — use it.

**Cleanup:** none.

### Lab 9.3 — Plan currency and career

**Objective:** Stay current and plan a path.

```python
python3 - <<'PY'
routine={"Versions":"exams tied to product versions (SLES 15+, Rancher) — renew as products advance",
         "Track":"new products/exams on suse.com/training/certification",
         "Practice":"keep openSUSE Leap + a K3s cluster",
         "Career":"SCA SLES -> SCE; + Rancher (cloud-native) / SUSE Manager (fleet) / NeuVector (security)"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — version tracking, practice, and a portfolio path.

**Negative test:** hold an old SLES-version cert forever; renew as **product versions** advance.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SUSE exams are Questionmark-delivered and test concepts plus practical decisions, prepared with
official training, docs, and free hands-on (openSUSE Leap, K3s); certifications track product versions,
so version-aware prep and renewal across the SLES/Rancher/SUSE Manager/NeuVector portfolio keep you
current.

- [ ] I can plan exam preparation.
- [ ] I can verify a free practice setup.
- [ ] I can plan version-aware currency.
- [ ] I can plan a career across the portfolio.
- [ ] I completed Labs 9.1–9.3 including each negative test.
