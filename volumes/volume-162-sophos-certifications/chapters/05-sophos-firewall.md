# Chapter 05: Sophos Firewall — Next-Generation Firewall

## Learning Objectives

- Explain Sophos Firewall as a next-generation firewall (NGFW).
- Describe TLS inspection, IPS, and web/application control.
- Understand the Xstream architecture and sandboxing.
- Recognize the firewall's role in the security estate.

*Cert relevance: Sophos Firewall is a core product with its own Engineer and Architect certifications.*

## What Sophos Firewall is

**Sophos Firewall** is Sophos's **next-generation firewall (NGFW)** — delivered as **XGS** hardware appliances, or as virtual/cloud instances — that secures the **network perimeter and segments**. Beyond classic firewalling (allow/deny by port and address), an NGFW inspects traffic **deeply** to enforce security: identifying applications and users, detecting intrusions, filtering web content, and blocking threats in traffic. Sophos Firewall is managed through [Sophos Central (Ch 2)](02-sophos-central.md) and participates in [Synchronized Security (Ch 6)](06-synchronized-security.md), and it is the network-security counterpart to the firewall vendors this shelf covers ([Fortinet XIX](../../volume-019-fortinet-network-security/README.md), [Check Point LXXIII](../../volume-073-check-point-certifications/README.md), [Palo Alto XVI](../../volume-016-palo-alto-networks-security/README.md)). The lab models the NGFW.

## TLS inspection, IPS, and web/app control

Sophos Firewall's NGFW capabilities include:

- **TLS/SSL inspection** — decrypting encrypted traffic to inspect it for threats. Since most traffic is now encrypted, threats hide inside TLS; inspecting it (under policy, respecting privacy) is essential to catch them. Sophos emphasizes **high-performance** TLS inspection ([Xstream, below](#the-xstream-architecture)).
- **IPS (Intrusion Prevention System)** — detecting and blocking **network attacks and exploits** in traffic by matching known attack patterns and anomalies.
- **Web control** — filtering **web access** by category and reputation (blocking malicious, inappropriate, or forbidden sites).
- **Application control** — identifying and controlling **applications** in traffic (allow business apps, block risky ones), regardless of port.

Together these let the firewall enforce security on the *content and intent* of traffic, not just its addresses. The lab models NGFW inspection.

## The Xstream architecture and sandboxing

Sophos Firewall's **Xstream architecture** is designed for **high-performance deep inspection** — especially **TLS inspection at scale**, which is computationally expensive and often a bottleneck on firewalls. Xstream's streaming packet-processing and acceleration aim to inspect encrypted traffic without crippling throughput. The firewall also integrates **sandboxing** (**Sophos Sandstorm** / threat intelligence): suspicious files are detonated in an **isolated cloud sandbox** to see if they're malicious before delivery, catching **unknown** threats that static inspection misses. Performance plus sandboxing lets the firewall inspect thoroughly at network speed. The lab models these.

## The firewall in the security estate

The firewall is one pillar of the Sophos estate, complementing the [endpoint (Intercept X, Ch 3)](03-intercept-x.md): the firewall protects the **network** (perimeter, segments, traffic), the endpoint protects the **device**. Their real power emerges when they **work together** via [Synchronized Security (Ch 6)](06-synchronized-security.md) — the firewall and endpoint sharing intelligence so a threat seen by one triggers a response by the other. Understanding the firewall's role, and how it fits the broader estate, is core to the Firewall certifications. The lab synthesizes.

## Hands-On Lab

Python models NGFW inspection. **Cost:** none.

### Lab 5.1 — NGFW deep inspection versus a port-only firewall

**Objective:** See TLS inspection, IPS, web/app control catch what ports cannot.

```bash
python3 - <<'EOF'
# traffic flows; a port-only firewall vs Sophos NGFW deep inspection
FLOWS = [
  {"desc": "HTTPS to malware-c2.xyz (encrypted)", "port": 443, "tls": True, "content": "C2 beacon", "app": "unknown", "web_cat": "malware"},
  {"desc": "HTTPS to salesforce.com",             "port": 443, "tls": True, "content": "CRM data", "app": "salesforce", "web_cat": "business"},
  {"desc": "exploit packet to web server",        "port": 80,  "tls": False,"content": "SQLi-exploit", "app": "http", "web_cat": "ok"},
  {"desc": "BitTorrent over port 443",            "port": 443, "tls": True, "content": "p2p", "app": "bittorrent", "web_cat": "ok"},
]
print("PORT-ONLY firewall (allow 443/80): everything on allowed ports passes ->")
print("   ALL 4 flows ALLOWED — incl. C2, exploit, and BitTorrent hiding on 443.  BLIND.\n")
print("SOPHOS NGFW — deep inspection:")
for f in FLOWS:
    reasons = []
    if f["tls"]:                       reasons.append("TLS-inspect (decrypt+scan)")
    if f["web_cat"] == "malware":      reasons.append("WEB CONTROL: malware category -> BLOCK")
    if "exploit" in f["content"]:      reasons.append("IPS: exploit pattern -> BLOCK")
    if f["app"] == "bittorrent":       reasons.append("APP CONTROL: BitTorrent -> BLOCK")
    blocked = any("BLOCK" in r for r in reasons)
    verdict = "BLOCKED" if blocked else "allowed"
    print(f"   {f['desc']:38} -> {verdict}")
    for r in reasons: print(f"        - {r}")
print("\nAn NGFW inspects the CONTENT + INTENT of traffic, not just port/address:")
print("  TLS INSPECTION decrypts encrypted traffic (where most threats now hide) — Xstream does it")
print("     at PERFORMANCE. IPS blocks exploit patterns. WEB CONTROL blocks malicious categories.")
print("  APP CONTROL identifies apps regardless of port (BitTorrent on 443 is caught). SANDBOXING")
print("     (Sandstorm) detonates unknown files in an isolated cloud to catch novel threats.")
print("A port-only firewall is BLIND to all of this. Sophos Firewall protects the NETWORK, pairing")
print("with Intercept X on the ENDPOINT — and they work TOGETHER via Synchronized Security (Ch 6).")
EOF
```

**Expected result:** A port-only firewall allowing all four flows (blind to C2, exploits, and BitTorrent hiding on 443), versus the Sophos NGFW blocking the malware C2 (web control after TLS inspection), the exploit (IPS), and BitTorrent (app control) while allowing legitimate Salesforce traffic. The firewall lesson is that an NGFW inspects the content and intent of traffic — TLS inspection (at Xstream performance), IPS, web control, app control, and sandboxing — catching threats a port-only firewall cannot see, protecting the network alongside Intercept X on the endpoint.

**Negative test:** Trusting a port-based firewall because "443 is HTTPS." Threats hide in encrypted traffic and misuse allowed ports (BitTorrent, C2 on 443); an NGFW with TLS inspection, IPS, and app control sees the content and intent, which port rules cannot.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Sophos Firewall understood as a next-generation firewall (XGS hardware or virtual/cloud).
- [ ] TLS inspection, IPS, and web/application control understood — inspecting content and intent.
- [ ] The Xstream architecture and sandboxing understood — high-performance inspection and detonating unknowns.
- [ ] The firewall's role in the estate recognized — protecting the network, pairing with endpoint via Synchronized Security.
