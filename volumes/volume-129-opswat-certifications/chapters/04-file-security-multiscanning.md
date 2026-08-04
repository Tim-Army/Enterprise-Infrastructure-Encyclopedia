# Chapter 04: File Security (OFSA) — Multiscanning, DLP, and Analysis

## Learning Objectives

- Cover the rest of OFSA: multiscanning, Proactive DLP, and static vs dynamic analysis.
- Understand why many engines beat one, and where DLP fits the file boundary.
- Model multiscanning aggregation and DLP detection.

## Beyond CDR: knowing what a file is

CDR ([Chapter 03](03-file-security-cdr.md)) removes active content; the file boundary also needs to **detect** known malware and **find sensitive data**. That is multiscanning and DLP.

| Technique | Question |
|:---|:---|
| **Multiscanning** | Do *any* of many AV engines flag this as known malware? |
| **Proactive DLP** | Does this file contain sensitive data (PII/PHI/secrets) that shouldn't cross this boundary? |
| **Static analysis** | What is the file's structure/metadata without running it? |
| **Dynamic analysis (sandbox)** | What does it do when detonated? |

## Hands-On Lab

Python models multiscanning and DLP. **Cost:** none.

### Lab 4.1 — Multiscanning: many engines beat one

**Objective:** Aggregate several detection sources — the multiscanning premise.

```bash
python3 - <<'EOF'
# Each "engine" catches a different subset; the union catches more than any single one.
engines = {
  "engineA": {"hash1", "hash2"},
  "engineB": {"hash2", "hash3"},
  "engineC": {"hash3", "hash4", "hash5"},
}
def scan(file_hash):
    hits = [e for e, sigs in engines.items() if file_hash in sigs]
    return hits
for h in ["hash1", "hash4", "cleanhash"]:
    hits = scan(h)
    verdict = f"MALICIOUS ({len(hits)}/{len(engines)} engines: {','.join(hits)})" if hits else "no detections (this pass)"
    print(f"{h:<12} -> {verdict}")
best_single = max(len(s) for s in engines.values())
union = len(set().union(*engines.values()))
print(f"\nbest single engine covers {best_single} sigs; multiscan union covers {union} -> more coverage")
EOF
```

**Expected result:** `hash1` and `hash4` are each caught by only one engine — a single-vendor scanner would miss one of them, but **multiscanning's union catches both**. No single AV has complete coverage; running many in parallel raises detection of known malware substantially. OFSA tests this "no single engine is enough" premise.

**Negative test:** Trusting one AV verdict as authoritative — vendors have blind spots and detection lag; multiscanning's value is precisely the coverage no single engine provides. (It still won't catch a true zero-day — that's CDR's job.)

**Cleanup:** None.

### Lab 4.2 — Proactive DLP at the file boundary

**Objective:** Detect sensitive data before a file crosses a trust boundary.

```bash
python3 - <<'EOF'
import re
detectors = {
  "US SSN": r"\b\d{3}-\d{2}-\d{4}\b",
  "Credit Card": r"\b(?:\d[ -]?){16}\b",
  "API key": r"\bAKIA[0-9A-Z]{16}\b",
}
def dlp(text):
    found = {name: len(re.findall(pat, text)) for name, pat in detectors.items()}
    return {k: v for k, v in found.items() if v}
doc = "Export for vendor: SSN 123-45-6789, card 4111 1111 1111 1111"
hits = dlp(doc)
action = "BLOCK / redact before transfer" if hits else "allow"
print(f"DLP hits: {hits} -> {action}")
EOF
```

**Expected result:** SSN and credit-card matches trigger a block/redact before the file leaves the boundary — **Proactive DLP** finds sensitive data in outbound (or cross-zone) files and stops leakage. At the file boundary, DLP complements CDR (which handles inbound weaponization) and multiscanning (known malware): three checks, three different risks.

**Negative test:** Applying DLP only to email bodies, not file *contents* — the SSN sitting inside an attached spreadsheet leaks; file-content DLP (into archives and documents) is what OPSWAT's platform provides.

**Cleanup:** None.

### Lab 4.3 — Static vs dynamic analysis

**Objective:** Distinguish the two analysis modes OFSA tests.

```bash
python3 - <<'EOF'
# Static: inspect without executing (fast, safe, structural). Dynamic: detonate and observe (slow, catches behavior).
def analyze(file):
    static = {"true_file_type": "PE executable (not the .jpg extension!)",
              "entropy": "high (possibly packed/encrypted)",
              "metadata": "compiled yesterday, no signature"}
    dynamic = {"network": "beacons to unknown-c2.example:443",
               "filesystem": "writes to startup folder",
               "verdict": "malicious behavior observed"}
    return static, dynamic
s, d = analyze("photo.jpg")
print("STATIC (no execution):"); [print(f"  {k}: {v}") for k,v in s.items()]
print("DYNAMIC (sandbox detonation):"); [print(f"  {k}: {v}") for k,v in d.items()]
print("\nStatic caught the type/extension mismatch; dynamic caught the C2 beacon — use both.")
EOF
```

**Expected result:** Static analysis flags a **file-type/extension mismatch** (a `.jpg` that's actually a PE executable) and high entropy without running anything; dynamic analysis (sandbox) catches the C2 beacon on detonation. OFSA expects you to know **static is fast/safe and catches structural lies; dynamic catches behavior** — and that true-file-type detection (not trusting the extension) is a core file-security control.

**Negative test:** Trusting the `.jpg` extension — the real file type is what matters; extension spoofing is trivial, and static true-type detection is the counter.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Multiscanning's union-of-engines coverage advantage internalized.
- [ ] Proactive DLP at the file boundary (into file contents) modeled.
- [ ] Static vs dynamic analysis and true-file-type detection drilled.
- [ ] OFSA File Security coverage complete across Chapters 03–04.
