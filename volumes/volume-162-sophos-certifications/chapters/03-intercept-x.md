# Chapter 03: Intercept X — Endpoint Protection and EDR

## Learning Objectives

- Explain Intercept X as Sophos's endpoint protection and EDR.
- Describe Deep Learning malware detection.
- Understand Exploit Prevention against attack techniques.
- Recognize EDR/XDR — detection, threat hunting, and response.

*Cert relevance: Intercept X is Sophos's flagship endpoint product, central to the Endpoint certifications.*

## What Intercept X is

**Intercept X** is Sophos's **endpoint protection** product — defending laptops, desktops, and servers against malware, ransomware, and exploits, with **EDR (endpoint detection and response)** capabilities layered on top. It combines multiple protection technologies: **Deep Learning** AI to detect malware, **Exploit Prevention** to block attack techniques, **CryptoGuard** anti-ransomware ([Chapter 4](04-cryptoguard-and-ransomware-defense.md)), and **EDR/XDR** ([Chapter 7](07-sophos-mdr-and-xdr.md)) for detection and investigation. Intercept X is the Sophos counterpart to the endpoint platforms this shelf covers ([SentinelOne CLI](../../volume-151-sentinelone-certifications/README.md), [CrowdStrike L](../../volume-050-crowdstrike-certifications/README.md)), and it is the flagship of the Central Endpoint certifications. The lab models the layered defense.

## Deep Learning malware detection

A defining Intercept X capability is **Deep Learning** — a **neural-network AI model** trained on hundreds of millions of malware and clean-file samples that detects malware by its **characteristics**, including **never-before-seen** (zero-day) threats. Unlike signature-based detection (which only catches known malware), the Deep Learning model **predicts** whether a file is malicious from its features, catching new and modified malware without a prior signature. This **predictive** detection is a core modern-endpoint capability — the same shift to AI/ML detection the whole endpoint market has made. The lab models predictive detection.

## Exploit Prevention

**Exploit Prevention** takes a different, complementary angle: rather than detecting the *malware*, it blocks the **techniques** attackers use to exploit vulnerabilities and run code. Attackers rely on a relatively small set of **exploit techniques** (buffer overflows, code injection, privilege escalation, credential theft methods) regardless of the specific malware; Exploit Prevention watches for these **behaviors** and blocks them. This means it can stop an attack **even if the malware is unknown**, because it targets the *how* of the attack rather than the *what*. Combining Deep Learning (detect the file) with Exploit Prevention (block the technique) gives layered, technique- and content-aware defense. The lab models technique blocking.

## EDR/XDR: detection, hunting, and response

Beyond prevention, Intercept X provides **EDR** (and, extended across data sources, [XDR, Ch 7](07-sophos-mdr-and-xdr.md)): it **records endpoint activity** and lets analysts **detect**, **investigate**, and **respond** to threats that prevention alone might miss. Analysts can **hunt** for threats across endpoints, examine a detection's full story, and take **response** actions (isolate the device, terminate a process, clean up). EDR acknowledges that **prevention is not perfect** — you also need to detect and respond to what gets through, which is the discipline the whole detection-and-response market centers on. The lab models detection and response.

## Hands-On Lab

Python models layered endpoint defense. **Cost:** none.

### Lab 3.1 — Deep Learning, Exploit Prevention, and EDR layered

**Objective:** See how multiple Intercept X layers catch different attacks.

```bash
python3 - <<'EOF'
# an incoming set of threats; each Intercept X layer catches different ones
def deep_learning(f):       # predicts malicious from file characteristics (incl. zero-day)
    return f["ml_malicious_score"] > 0.8
def exploit_prevention(f):  # blocks known exploit TECHNIQUES regardless of the malware
    return f.get("technique") in {"buffer-overflow", "code-injection", "cred-theft"}

THREATS = [
  {"name": "known-trojan.exe",   "ml_malicious_score": 0.97, "technique": None},
  {"name": "novel-malware.exe",  "ml_malicious_score": 0.91, "technique": None},           # zero-day, no signature
  {"name": "exploit-doc.docx",   "ml_malicious_score": 0.30, "technique": "buffer-overflow"}, # weaponized doc
  {"name": "legit-app.exe",      "ml_malicious_score": 0.05, "technique": None},           # benign
]
print("Intercept X — LAYERED endpoint defense:\n")
for t in THREATS:
    dl = deep_learning(t)
    ep = exploit_prevention(t)
    if dl or ep:
        by = " + ".join([x for x, hit in [("Deep Learning", dl), ("Exploit Prevention", ep)] if hit])
        verdict = f"BLOCKED by {by}"
    else:
        verdict = "allowed (benign)"
    print(f"   {t['name']:20} {verdict}")
print("\nThe layers catch DIFFERENT attacks:")
print("  DEEP LEARNING (AI) — predicts malicious from file CHARACTERISTICS -> catches known AND")
print("     NOVEL/zero-day malware WITHOUT a signature (novel-malware.exe blocked, no prior sig).")
print("  EXPLOIT PREVENTION — blocks the TECHNIQUE (buffer overflow/injection/cred-theft) regardless")
print("     of the malware -> stops the weaponized doc EVEN THO its ML score is low.")
print("  EDR/XDR (Ch 7) — records activity to DETECT + investigate + RESPOND to what prevention misses,")
print("     because prevention is never perfect. Layered defense: detect the FILE + block the TECHNIQUE")
print("     + hunt/respond. This is modern endpoint protection — Intercept X, the Sophos flagship.")
EOF
```

**Expected result:** A known trojan and a novel zero-day both blocked by Deep Learning (no signature needed), a weaponized document blocked by Exploit Prevention (despite a low ML score, because it uses a buffer-overflow technique), and a benign app allowed. The Intercept X lesson is that layered defense combines Deep Learning (predicts malicious files, including zero-days) with Exploit Prevention (blocks attack techniques regardless of malware) and EDR/XDR (detect, hunt, and respond to what prevention misses) — modern endpoint protection.

**Negative test:** Relying only on signature-based antivirus. It misses novel malware and technique-based attacks; Intercept X layers predictive Deep Learning, technique-blocking Exploit Prevention, and EDR so new and evasive threats are caught and what gets through is detected.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Intercept X understood as Sophos's endpoint protection and EDR flagship.
- [ ] Deep Learning malware detection understood — predictive AI catching known and zero-day malware.
- [ ] Exploit Prevention understood — blocking attack techniques regardless of the specific malware.
- [ ] EDR/XDR understood — detecting, hunting, and responding to what prevention misses.
