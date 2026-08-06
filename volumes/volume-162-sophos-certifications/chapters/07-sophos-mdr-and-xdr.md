# Chapter 07: Sophos MDR and XDR

## Learning Objectives

- Explain Sophos MDR — managed detection and response.
- Describe the 24/7 SOC-as-a-service model.
- Understand XDR — extended detection across data sources.
- Recognize threat hunting and human-led response.

*Cert relevance: Sophos MDR is a flagship service and a distinct certification/product area.*

## What Sophos MDR is

**Sophos MDR (Managed Detection and Response)** is a **fully-managed service** in which Sophos's own **security operations analysts** monitor, detect, investigate, and respond to threats **on the customer's behalf, 24/7**. Many organizations lack a round-the-clock **security operations center (SOC)** with skilled threat hunters — MDR provides one **as a service**. Sophos's team watches the customer's environment (endpoints, network, cloud, identity, email), **hunts** for threats, **investigates** detections, and **takes response actions** to stop attacks, continuously. MDR is one of Sophos's flagship offerings — and a growing part of the security market, because the shortage of security talent makes **outsourcing detection and response** compelling. The lab models the service.

## The 24/7 SOC-as-a-service model

The core value is a **24/7 SOC without building one**. A capable in-house SOC requires **hiring, training, and retaining** scarce security analysts, tooling, and around-the-clock staffing — expensive and hard. Sophos MDR delivers the **outcome** (continuous expert monitoring and response) as a **subscription**:

- **24/7 coverage** — attacks happen at 3 a.m. on holidays; MDR watches always.
- **Expert analysts** — skilled threat hunters and responders, without the hiring burden.
- **Response included** — not just alerts, but **actions taken** to stop threats (the "response" in MDR).

This makes enterprise-grade detection and response **accessible** to organizations that could never staff it themselves. The lab models the SOC-as-a-service value.

## XDR: extended detection

Sophos MDR is built on **XDR (Extended Detection and Response)** — extending detection **beyond the endpoint** ([EDR, Ch 3](03-intercept-x.md)) to **correlate signals across many data sources**: endpoint, network (firewall), email, cloud, and identity. Where EDR sees one domain, **XDR sees the whole picture** — correlating a suspicious email, an endpoint detection, and unusual network traffic into **one attack story** that no single tool would recognize. This cross-domain correlation is what lets analysts (and the MDR team) detect sophisticated, multi-stage attacks. (Following Sophos's acquisition of **Secureworks**, its **Taegis** XDR platform strengthens this.) XDR is the modern evolution of detection and response. The lab models cross-domain correlation.

## Threat hunting and human-led response

A defining MDR element is **human-led threat hunting** — expert analysts **proactively searching** for threats that automated tools miss, using hypotheses, threat intelligence, and the correlated XDR data. Automation catches the known; **skilled humans** catch the novel, subtle, and hands-on-keyboard adversaries. And MDR includes **response** — the analysts don't just alert the customer, they **act** (contain, remediate) under agreed authority. Human expertise plus response authority is what separates MDR from a mere alerting tool, and it is the value the service delivers. The lab synthesizes.

## Hands-On Lab

Python models XDR correlation and MDR response. **Cost:** none.

### Lab 7.1 — XDR correlation and 24/7 human-led response

**Objective:** See cross-domain correlation and managed response.

```bash
python3 - <<'EOF'
# signals from multiple domains; XDR correlates them into ONE attack story
signals = [
  {"domain": "email",    "event": "phishing email opened by user jsmith", "alone": "low"},
  {"domain": "endpoint", "event": "jsmith's laptop ran a suspicious script","alone": "medium"},
  {"domain": "identity", "event": "jsmith account logged in from new country","alone": "low"},
  {"domain": "network",  "event": "laptop beaconing to unknown host",        "alone": "medium"},
]
print("Individual signals (each ALONE looks minor):")
for s in signals:
    print(f"   [{s['domain']:8}] {s['event']}  (alone: {s['alone']})")
# XDR correlation: same user/asset, time-ordered -> ONE multi-stage attack
print("\nXDR CORRELATION (across email+endpoint+identity+network, same user jsmith):")
print("   phishing -> script exec -> anomalous login -> beaconing  =  ONE MULTI-STAGE ATTACK (HIGH)")
print("   -> no SINGLE tool would flag this; correlating domains reveals the full story\n")
# MDR: 24/7 human analysts hunt, confirm, and RESPOND
print("Sophos MDR (24/7 SOC-as-a-service) acts on it:")
print("   03:14 (holiday) — MDR analyst confirms the correlated attack (human-led hunt)")
print("   RESPONSE (included): isolate jsmith's laptop, disable the account, remediate — attack stopped")
print("   -> the customer had NO in-house 24/7 SOC; MDR provided the outcome as a subscription\n")
print("Sophos MDR = MANAGED detection + response: Sophos's own analysts monitor/hunt/investigate/")
print("RESPOND 24/7 on your behalf. Built on XDR (EXTENDED detection — correlate endpoint+network+")
print("email+cloud+identity into one attack story, vs EDR's single domain; Taegis post-Secureworks).")
print("The value: a 24/7 SOC + expert threat HUNTERS + response authority WITHOUT hiring them — enterprise")
print("detection-and-response as a subscription, for the many orgs that can't staff a SOC themselves.")
EOF
```

**Expected result:** Four individually-minor signals (phishing, script execution, anomalous login, beaconing) correlated by XDR into one high-severity multi-stage attack no single tool would flag, then Sophos MDR analysts confirming and responding (isolate, disable, remediate) at 3 a.m. on a holiday. The MDR lesson is that Sophos MDR is a 24/7 SOC-as-a-service where expert analysts hunt, investigate, and respond on the customer's behalf, built on XDR that correlates signals across endpoint, network, email, cloud, and identity — enterprise detection and response without staffing a SOC.

**Negative test:** Relying on siloed alerts and business-hours staff. Multi-stage attacks span domains and strike off-hours; XDR correlation reveals the full attack and 24/7 MDR analysts respond when no in-house SOC could, which is the service's value.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Sophos MDR understood — a fully-managed 24/7 detection-and-response service.
- [ ] The SOC-as-a-service model understood — expert monitoring and response as a subscription.
- [ ] XDR understood — extended detection correlating signals across endpoint, network, email, cloud, and identity.
- [ ] Threat hunting and human-led response recognized as what distinguishes MDR from mere alerting.
