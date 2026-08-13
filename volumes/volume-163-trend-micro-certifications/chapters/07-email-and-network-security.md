# Chapter 07: Email and Network Security

## Learning Objectives

- Explain email security — the top attack vector.
- Describe Cloud App Security for Microsoft 365 and Google.
- Understand network security — TippingPoint IPS and Deep Discovery.
- Recognize these as XDR sensor layers.

*Cert relevance: email and network security are Trend Micro layers feeding the XDR platform.*

## Email security: the top vector

**Email is the number-one attack vector** — most breaches begin with a **phishing** email, a **business email compromise (BEC)**, or a malicious attachment or link. Trend Micro's email security defends this front, and its cloud offering — **Cloud App Security** — protects **Microsoft 365** and **Google Workspace** by inspecting email (and collaboration apps) for:

- **Phishing and BEC** — detecting fraudulent messages, including AI/ML detection of the subtle, payload-free social-engineering that BEC uses.
- **Malicious attachments** — sandboxing suspicious files before delivery.
- **Malicious URLs** — checking links (including time-of-click, since a link can turn malicious after delivery).

Because email is where so many attacks start, strong email security **prevents** a large share of incidents before they reach the endpoint. The lab models email defense.

## Cloud App Security

**Cloud App Security** integrates directly with **cloud email/collaboration** (Microsoft 365, Google Workspace) via API — no mail-routing changes — to add a **security layer** on top of the platform's built-in protection. It scans inbound, outbound, and internal messages and shared files, catching threats the native filtering misses (advanced phishing, BEC, and malware). It also protects **collaboration** apps (SharePoint, OneDrive, Teams, Google Drive) where malware can spread internally. As organizations move to cloud email, API-based security that layers onto it is the modern approach. The lab models cloud-email protection.

## Network security: TippingPoint and Deep Discovery

Trend Micro's **network security** inspects traffic for threats:

- **TippingPoint** — a **network IPS (intrusion prevention system)**: in-line appliances that inspect network traffic and **block exploits, malware, and attacks** in real time, at network speed — the network counterpart to endpoint IPS/virtual patching, competing with [Fortinet (XIX)](../../volume-019-fortinet-network-security/README.md) and [Palo Alto (XVI)](../../volume-016-palo-alto-networks-security/README.md).
- **Deep Discovery** — **network detection and sandboxing** for **targeted attacks and APTs**: it watches network traffic for the subtle signs of advanced, targeted attacks (unusual lateral movement, C2, data staging) and **detonates** suspicious files in a sandbox, catching threats that evade signature-based tools.

Network-layer visibility catches attacks in transit and adds another detection domain. The lab models network detection.

## XDR sensor layers

The strategic point is that email and network security are not just **standalone** products — they are **sensor layers** feeding [Trend Vision One's XDR (Ch 3)](03-xdr-detection-and-response.md). Email telemetry (a phishing click), network telemetry (a C2 connection), endpoint telemetry (an execution), and cloud telemetry combine into **cross-layer attack stories**. Because email and network are where attacks often **begin** and **spread**, including them as XDR sensors dramatically improves detection — XDR sees the attack from the **initial email** through the **network movement** to the **endpoint and cloud**. Email and network security are both protective layers and XDR sensors. The lab synthesizes.

## Hands-On Lab

Python models email defense and network detection as XDR sensors. **Cost:** none.

### Lab 7.1 — Email and network layers feed the attack story

**Objective:** See email and network detection as protective layers and XDR sensors.

```bash
python3 - <<'EOF'
# email security catches phishing/BEC; network security catches C2/exploits; both feed XDR
def email_security(msg):
    if msg.get("bec_indicators"):     return "BLOCKED: BEC (AI-detected social engineering)"
    if msg.get("malicious_url"):      return "BLOCKED: malicious URL (time-of-click)"
    if msg.get("malicious_attach"):   return "BLOCKED: malware (sandboxed before delivery)"
    return "delivered (clean)"
def network_security(flow):
    if flow.get("exploit"):           return "TippingPoint IPS: BLOCKED exploit"
    if flow.get("c2_beacon"):         return "Deep Discovery: C2 beacon detected (APT indicator)"
    return "allowed"

print("EMAIL SECURITY (Cloud App Security — M365/Google, top attack vector):")
for m in [{"from": "ceo-spoof", "bec_indicators": True}, {"link": "x", "malicious_url": True}, {"clean": True}]:
    print(f"   {email_security(m)}")
print("\nNETWORK SECURITY (TippingPoint IPS + Deep Discovery):")
for f in [{"exploit": True}, {"c2_beacon": True}, {"normal": True}]:
    print(f"   {network_security(f)}")
print("\nBoth are ALSO XDR SENSORS — a multi-stage attack seen across layers:")
attack = ["email: phishing link clicked (email sensor)", "network: C2 beacon (Deep Discovery sensor)",
          "endpoint: payload run (Apex One sensor)"]
print("   " + "\n   ".join(attack))
print("   -> XDR CORRELATES email + network + endpoint -> ONE attack story from INITIAL EMAIL to endpoint\n")
print("EMAIL is the #1 attack vector — Cloud App Security defends M365/Google (phishing/BEC/malware,")
print("API-based, no mail-routing change). NETWORK security (TippingPoint IPS blocks exploits inline;")
print("Deep Discovery sandboxes + catches APT/C2). Both are protective layers AND ★ XDR SENSORS: since")
print("attacks BEGIN in email and SPREAD over the network, including them lets XDR see the attack from")
print("the first phishing click through network movement to endpoint + cloud — the full story.")
EOF
```

**Expected result:** Email security blocking BEC, malicious URLs, and attachments (Cloud App Security on M365/Google), network security blocking exploits (TippingPoint) and detecting C2 (Deep Discovery), and both feeding XDR so a phishing→C2→endpoint attack correlates into one story from the initial email. The lesson is that email (the top attack vector) and network security are both protective layers and XDR sensors — since attacks begin in email and spread over the network, including them lets XDR see the full attack from first click through network movement to endpoint and cloud.

**Negative test:** Securing only the endpoint and cloud while treating email and network as out of scope. Attacks start in email and traverse the network, so those layers are where you catch them earliest and where XDR gains the most context; email and network security are essential protective layers and XDR sensors.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Email security understood as defending the top attack vector — phishing, BEC, malicious attachments/URLs.
- [ ] Cloud App Security understood — API-based protection for Microsoft 365 and Google Workspace.
- [ ] Network security understood — TippingPoint IPS (block exploits) and Deep Discovery (APT detection and sandboxing).
- [ ] Email and network recognized as both protective layers and XDR sensors feeding cross-layer attack stories.
