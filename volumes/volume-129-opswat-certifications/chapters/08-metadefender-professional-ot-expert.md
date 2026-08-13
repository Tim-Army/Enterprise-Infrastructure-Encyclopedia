# Chapter 08: MetaDefender Professional and OT Security Expert

## Learning Objectives

- Cover the Professional (product) tier: the MetaDefender platform certifications.
- Cover ICAP-based web protection and the OT Security Expert designation.
- Model where each MetaDefender product sits in the CIP architecture.

## From Associate to Professional to Expert

The Associate certs ([Chapters 02–07](02-cip-fundamentals.md)) teach the concepts vendor-neutrally. The **Professional** tier certifies you on the **MetaDefender platform** that implements them — deploying, configuring, and operating the products. The **Expert** tier (OPSWAT OT Security Expert) certifies end-to-end OT security command.

## The MetaDefender product certifications

Professional-level, paid (around US$1,000 each), plus a 3-day MetaDefender Platform Bootcamp:

| Product Professional | What it deploys | Boundary it defends |
|:---|:---|:---|
| **MetaDefender Core** | The multiscan + Deep CDR + DLP + sandbox engine | The scanning brain behind every other product |
| **MetaDefender ICAP** | CDR/multiscan for web/proxy traffic (ICAP protocol) | Web downloads and uploads, inline |
| **MetaDefender Kiosk** | Media-scanning stations | Removable media into OT/air gaps |
| **MetaDefender MFT** | Managed/secure file transfer | Controlled cross-zone file movement |

**MetaDefender Core** is the hub: the other products feed files through Core's engines. The Professional exams test deploying and configuring these in a real architecture.

## Hands-On Lab

Python models the platform architecture and ICAP flow. **Cost:** none.

### Lab 8.1 — MetaDefender Core as the scanning hub

**Objective:** Model how every product routes files through Core's engines.

```bash
python3 - <<'EOF'
# Core exposes scan(file) -> {multiscan, cdr, dlp, sandbox}; other products call it.
def core_scan(file, malicious=False, active=False, sensitive=False, unknown=False):
    result = {"multiscan": "malicious" if malicious else "clean",
              "cdr": "sanitized (active content removed)" if active else "no change needed",
              "dlp": "sensitive data found -> block/redact" if sensitive else "clean",
              "sandbox": "detonated -> malicious behavior" if unknown else "not needed"}
    verdict = "BLOCK" if (malicious or sensitive or unknown) else "ALLOW (sanitized)" if active else "ALLOW"
    return result, verdict
for product, f in [("ICAP (web dl)", dict(active=True)),
                   ("Kiosk (USB)", dict(malicious=True)),
                   ("MFT (transfer)", dict(sensitive=True))]:
    res, verdict = core_scan("file", **f)
    print(f"{product:<16} -> Core verdict: {verdict}  ({res['cdr'] if f.get('active') else res['multiscan'] if f.get('malicious') else res['dlp']})")
EOF
```

**Expected result:** ICAP, Kiosk, and MFT each hand their files to Core, which returns a unified verdict from its engines. The Professional-tier insight: **Core is the shared scanning brain**; the edge products (ICAP for web, Kiosk for media, MFT for transfer) are delivery mechanisms feeding the same multiscan + CDR + DLP + sandbox pipeline. Deploying the platform means wiring the edges to Core.

**Negative test:** Deploying Kiosk without Core's engines configured — the kiosk has nothing to scan *with*; the product certs test the whole platform wiring, not one box in isolation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — ICAP: inline web protection

**Objective:** Model the ICAP flow — CDR/multiscan on web traffic inline.

```bash
python3 - <<'EOF'
# ICAP: the web proxy hands each download/upload to MetaDefender before delivering it.
def icap(proxy_request):
    f = proxy_request
    if f["direction"] == "download":
        if f["malicious"]: return "proxy BLOCKS download (Core: malicious)"
        if f["active"]:    return "proxy delivers SANITIZED file (Core: CDR applied)"
        return "proxy delivers file (clean)"
    else:  # upload
        if f["sensitive"]: return "proxy BLOCKS upload (Core: DLP — sensitive data)"
        return "proxy allows upload"
print(icap({"direction":"download","malicious":False,"active":True,"sensitive":False}))
print(icap({"direction":"download","malicious":True,"active":False,"sensitive":False}))
print(icap({"direction":"upload","malicious":False,"active":False,"sensitive":True}))
EOF
```

**Expected result:** Downloads are sanitized/blocked and sensitive uploads blocked, all inline at the proxy via ICAP — web traffic gets the same CDR/multiscan/DLP as the file boundary, transparently. ICAP (the protocol proxies use to offload content inspection) is how MetaDefender protects the web path without being inline itself. This complements the SWG/CASB model in the SASE volumes.

**Negative test:** A web proxy with no content inspection — it enforces URL categories but passes the file contents unchecked; ICAP integration is what adds CDR/multiscan to the download path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — The OT Security Expert designation

**Objective:** Understand the Expert tier's scope.

```bash
python3 - <<'EOF'
# OT Security Expert: command of the whole CIP/OT defense, integrating the products + standards
expert_scope = [
  "IT/OT boundary architecture (kiosk, vault, MFT, unidirectional flow)",
  "MetaDefender platform deployment across the boundary",
  "OT protocol awareness and passive monitoring (cf. Claroty/Nozomi/TXOne volumes)",
  "alignment with ISA/IEC 62443 zones/conduits/security levels (Volume CXXVIII)",
  "incident response and secure operations for critical infrastructure",
]
print("OPSWAT OT Security Expert — scope:")
for s in expert_scope: print(f"  - {s}")
EOF
```

**Expected result:** The Expert scope — boundary architecture, platform deployment, OT monitoring, 62443 alignment, and OT incident response — end-to-end command of critical-infrastructure defense. The OT Security Expert is where OPSWAT's products meet the standards (62443) and the OT-monitoring products, making it the capstone for critical-infrastructure defenders.

**Negative test:** Expert-level OT security that knows the products but not the standard (62443) or the OT operational constraints — the tools protect the boundary, but the design and lifecycle come from the standard; the Expert must speak both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Professional product certs and Core-as-hub architecture understood.
- [ ] ICAP inline web protection modeled.
- [ ] The OT Security Expert scope (products + 62443 + OT ops) internalized.
