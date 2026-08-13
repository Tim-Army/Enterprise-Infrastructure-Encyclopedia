# Chapter 08: Threat Intelligence and Zero Trust

## Learning Objectives

- Explain the Smart Protection Network global threat intelligence.
- Describe how intelligence feeds detection and response.
- Understand Zero Trust Secure Access (ZTSA).
- Recognize risk-based, continuous access control.

*Cert relevance: threat intelligence and zero trust round out the Vision One platform and the certifications.*

## The Smart Protection Network

Trend Micro's **Smart Protection Network** is its **global threat-intelligence backbone** — a cloud infrastructure that collects and correlates **threat telemetry** from hundreds of millions of sensors worldwide (endpoints, email, web, network) plus Trend's threat research. From this vast, continuously-updated data, it identifies **new threats** — malicious files, URLs, IPs, domains, and attack patterns — and pushes that intelligence to **every Trend Micro product** in near real time. This means a threat seen **anywhere** in the network protects **everyone**: when the Smart Protection Network learns of a new malicious URL from one customer, all customers are protected against it almost immediately. Global, shared, real-time intelligence is a core advantage of a large security vendor with decades of telemetry. The lab models shared intelligence.

## Intelligence feeding detection and response

Threat intelligence is only valuable when it **acts**. The Smart Protection Network's intelligence feeds directly into every layer:

- **Prevention** — blocking known-malicious files, URLs, and connections across endpoint, email, network, and cloud.
- **Detection** — enriching [XDR (Ch 3)](03-xdr-detection-and-response.md) with **threat context**: is this file/IP/domain known-bad? is this vulnerability being actively exploited? (which powers [ASRM risk scoring, Ch 6](06-attack-surface-risk-management.md)).
- **Response** — informing responders with intelligence about the adversary and campaign.

Intelligence turns raw detections into **informed** decisions — you know not just *that* something happened but *what* it is and *how dangerous* it is. Current, global intelligence woven through the platform is what makes detection accurate and prioritization meaningful. The lab models intelligence-enriched detection.

## Zero Trust Secure Access

**Zero Trust Secure Access (ZTSA)** brings **zero-trust** principles to Vision One — *never trust, always verify*. Rather than granting broad network access based on being "inside" the perimeter, ZTSA grants access to **specific resources** based on **continuous verification** of the user's and device's **identity, health, and risk**. Key ideas:

- **Per-resource access** — users reach only the specific applications/resources they're authorized for (like [ZTNA](../../volume-162-sophos-certifications/README.md)), not the whole network.
- **Continuous, risk-based** — access is re-evaluated continuously; if a device's **risk** rises (a detection, an anomaly), access is **restricted** automatically.

ZTSA integrates with the platform's **risk signals** (from XDR and ASRM), so access decisions reflect the **live security posture** of the user and device. The lab models risk-based access.

## Risk-based, continuous access control

The unifying idea is **risk-based, continuous access control** — access is not a one-time gate but an **ongoing** decision driven by **live risk**. Because Vision One knows each user's and device's risk (from detections, exposures, and behavior), ZTSA can **adapt** access in real time: a healthy device gets normal access; a device showing signs of compromise gets **restricted or blocked** automatically, containing a threat by cutting its access. This ties zero-trust access to the platform's **detection and risk intelligence** — access control that responds to the security state, not a static rule. The lab synthesizes.

## Hands-On Lab

Python models shared intelligence and risk-based access. **Cost:** none.

### Lab 8.1 — Global intelligence and risk-based continuous access

**Objective:** See shared threat intelligence and adaptive zero-trust access.

```bash
python3 - <<'EOF'
# 1) Smart Protection Network: a threat seen ANYWHERE protects EVERYONE
global_intel = set()   # known-bad indicators, shared globally in near real time
def sighting(indicator, customer):
    global_intel.add(indicator)
    return f"{customer} reported {indicator} -> added to global intel -> ALL customers now protected"
print("SMART PROTECTION NETWORK — global, shared, real-time threat intelligence:")
print("   " + sighting("evil-c2.example", "Customer A"))
def is_blocked(indicator):
    return indicator in global_intel
print(f"   Customer B encounters evil-c2.example -> blocked? {is_blocked('evil-c2.example')} (protected instantly)\n")

# 2) Zero Trust Secure Access: continuous, RISK-based access
def ztsa_access(user, device_risk, resource):
    if device_risk >= 70:  return f"DENY {resource} (device risk {device_risk} HIGH -> contain)"
    if device_risk >= 40:  return f"LIMITED {resource} (risk {device_risk} medium -> step-up MFA)"
    return f"ALLOW {resource} (risk {device_risk} low)"
print("ZERO TRUST SECURE ACCESS — per-resource, CONTINUOUS, RISK-based:")
for risk in [10, 50, 85]:
    print(f"   device_risk={risk:>2} -> {ztsa_access('jsmith', risk, 'finance-app')}")
print("   -> access ADAPTS to LIVE risk: healthy device = normal; compromised device = auto-restricted\n")
print("The SMART PROTECTION NETWORK = global threat intel from 100Ms of sensors: a threat seen ANYWHERE")
print("protects EVERYONE in near real time. It feeds PREVENTION (block known-bad), DETECTION (enrich XDR")
print("with threat context), and ASRM risk scoring (is it exploited in the wild?). ZERO TRUST SECURE")
print("ACCESS grants PER-RESOURCE access by CONTINUOUS, RISK-based verification — tied to the platform's")
print("live risk signals, so a device showing compromise is auto-restricted (containment via access control).")
EOF
```

**Expected result:** The Smart Protection Network adding a customer's threat sighting to global intelligence so all customers are instantly protected, and Zero Trust Secure Access granting, limiting, or denying resource access based on live device risk (low → allow, medium → step-up MFA, high → deny/contain). The lesson is that global shared threat intelligence protects everyone from a threat seen anywhere and enriches detection and risk scoring, while ZTSA ties per-resource access to continuous risk verification so a compromised device is automatically restricted.

**Negative test:** Treating access as a one-time perimeter gate with no threat intelligence. Static access ignores a device becoming compromised mid-session, and without shared intelligence each org faces new threats alone; global intelligence plus risk-based continuous access adapt protection to the live threat landscape and security posture.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Smart Protection Network understood — global, shared, real-time threat intelligence.
- [ ] Intelligence feeding detection and response understood — prevention, XDR enrichment, and ASRM risk context.
- [ ] Zero Trust Secure Access understood — per-resource access by continuous, risk-based verification.
- [ ] Risk-based, continuous access control recognized — access adapting to the live security posture.
