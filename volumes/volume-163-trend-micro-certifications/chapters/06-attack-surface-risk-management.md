# Chapter 06: Attack Surface Risk Management (ASRM)

## Learning Objectives

- Explain ASRM and the shift from reactive to proactive security.
- Describe discovering and assessing the attack surface.
- Understand risk scoring and prioritized remediation.
- Recognize ASRM as a Trend Vision One differentiator.

*Cert relevance: attack surface risk management is a Vision One pillar and a growing certification emphasis.*

## What ASRM is

**Attack Surface Risk Management (ASRM)** is a pillar of [Trend Vision One (Ch 2)](02-trend-vision-one.md) that shifts security from **reactive** (detect and respond after an attack) to **proactive** (discover and reduce risk **before** an attack). ASRM continuously **discovers** the organization's **attack surface** — all the assets, exposures, and vulnerabilities an attacker could target — **assesses** the risk each represents, and helps **prioritize** what to fix. Where [XDR (Ch 3)](03-xdr-detection-and-response.md) handles the attack when it happens, ASRM works to **prevent** the attack by shrinking the surface first. This proactive risk management is a distinctive Trend Micro emphasis. The lab models ASRM.

## Discovering and assessing the attack surface

You cannot secure what you don't know exists, so ASRM starts with **discovery** — continuously finding the **assets** (devices, servers, cloud resources, identities, applications, internet-facing services) across the environment, including **unknown** or **unmanaged** ones (shadow IT, forgotten cloud instances). For each asset, ASRM **assesses**:

- **Vulnerabilities** — unpatched software, weak configurations.
- **Exposure** — is it internet-facing? over-permissioned? unprotected?
- **Threat context** — is this vulnerability being actively exploited in the wild?

Combining these gives a real picture of **where the organization is exposed** — the attack surface as an attacker sees it. The lab models discovery and assessment.

## Risk scoring and prioritized remediation

The core value of ASRM is **prioritization through risk scoring**. A large organization has **thousands** of vulnerabilities and exposures — far more than any team can fix at once. ASRM computes a **risk score** for each, combining the **severity** of the issue, the **exposure** of the asset, the **value/criticality** of the asset, and the **threat context** (is it being exploited now?). This turns an overwhelming list into a **ranked** one: fix the **high-risk** items (critical, exposed, actively-exploited) first, and deprioritize the low-risk ones. Risk-based prioritization is what makes vulnerability and exposure management **actionable** at scale — you reduce the most risk with the least effort. The lab models risk scoring.

## ASRM as a differentiator

ASRM is a genuine **differentiator** for Trend Vision One — while many vendors focus on detection and response (the reactive side), Trend Micro integrates **proactive risk management** into the same platform. This lets a security team both **reduce** the attack surface (fewer ways in) and **detect/respond** to what still gets through, from **one console**. The convergence of exposure management and detection-and-response — understand risk, reduce it, and defend against the rest — is a modern direction, and Vision One's ASRM pillar is Trend Micro's expression of it. The lab synthesizes.

## Hands-On Lab

Python models attack-surface discovery and risk-based prioritization. **Cost:** none.

### Lab 6.1 — Risk-scored prioritization of the attack surface

**Objective:** See ASRM turn an overwhelming list into a ranked one.

```bash
python3 - <<'EOF'
# discovered assets + their exposures; compute a risk score to PRIORITIZE
assets = [
  {"asset": "public-web-server", "cvss": 9.8, "internet_facing": True,  "critical": True,  "exploited_in_wild": True},
  {"asset": "internal-print-srv","cvss": 7.5, "internet_facing": False, "critical": False, "exploited_in_wild": False},
  {"asset": "finance-db",        "cvss": 8.1, "internet_facing": False, "critical": True,  "exploited_in_wild": False},
  {"asset": "forgotten-cloud-vm","cvss": 9.1, "internet_facing": True,  "critical": False, "exploited_in_wild": True},  # shadow IT!
  {"asset": "dev-workstation",   "cvss": 6.0, "internet_facing": False, "critical": False, "exploited_in_wild": False},
]
def risk_score(a):
    s = a["cvss"]
    if a["internet_facing"]:    s += 4      # exposure
    if a["critical"]:           s += 3      # asset value
    if a["exploited_in_wild"]:  s += 5      # threat context (actively exploited)
    return round(s, 1)

print("ASRM — discover assets (incl. shadow IT), assess, and RISK-SCORE to prioritize:\n")
ranked = sorted(assets, key=risk_score, reverse=True)
for a in ranked:
    flags = []
    if a["internet_facing"]: flags.append("internet-facing")
    if a["critical"]: flags.append("critical")
    if a["exploited_in_wild"]: flags.append("EXPLOITED-IN-WILD")
    print(f"   risk {risk_score(a):>4}  {a['asset']:18} cvss={a['cvss']}  [{', '.join(flags) or 'low exposure'}]")
print(f"\n   FIX FIRST: {ranked[0]['asset']} + {ranked[1]['asset']} (high risk: exposed + exploited)")
print(f"   note: forgotten-cloud-vm (SHADOW IT) is high-risk — discovery FOUND it\n")
print("The ASRM insight: a big org has THOUSANDS of vulns/exposures — more than any team can fix.")
print("RISK-SCORE each = severity (CVSS) + EXPOSURE (internet-facing) + asset VALUE + THREAT CONTEXT")
print("(exploited in the wild). This turns an overwhelming list into a RANKED one -> fix the high-risk")
print("items first (critical + exposed + actively-exploited), reducing the MOST risk with the LEAST")
print("effort. PROACTIVE (reduce the surface BEFORE attack) vs XDR's reactive detect/respond — and")
print("ASRM found the SHADOW-IT cloud VM. Proactive risk mgmt is Trend Vision One's differentiator.")
EOF
```

**Expected result:** Discovered assets (including a forgotten shadow-IT cloud VM) risk-scored by combining CVSS severity, internet exposure, asset criticality, and active-exploitation context, then ranked so the public web server and forgotten cloud VM (both exposed and actively exploited) are fixed first. The ASRM lesson is that risk scoring turns thousands of vulnerabilities into a ranked, actionable list — reducing the most risk with the least effort — and discovery surfaces unknown assets, making proactive attack-surface reduction Vision One's differentiator alongside reactive XDR.

**Negative test:** Trying to patch every vulnerability by raw CVSS score alone. That ignores exposure, asset value, and whether a flaw is actually being exploited, so effort is wasted on low-risk issues; ASRM's risk scoring prioritizes what actually matters, and discovery finds the assets you didn't know you had.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] ASRM understood — proactively discovering and reducing risk before an attack.
- [ ] Discovering and assessing the attack surface understood — finding assets (including shadow IT) and their exposures.
- [ ] Risk scoring and prioritized remediation understood — ranking by severity, exposure, value, and threat context.
- [ ] ASRM recognized as a Trend Vision One differentiator — proactive risk management alongside reactive XDR.
