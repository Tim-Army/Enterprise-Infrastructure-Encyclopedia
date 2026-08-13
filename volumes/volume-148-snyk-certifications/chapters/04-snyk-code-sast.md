# Chapter 04: Snyk Code — SAST

## Learning Objectives

- Explain static application security testing (SAST) and how it differs from SCA.
- Understand data-flow analysis — tracing untrusted input to a dangerous sink.
- Recognize why false positives are the SAST failure mode, and how Snyk reduces them.
- Place DeepCode AI and real-time in-IDE scanning.

*Cert relevance: Snyk Code is the SAST engine — securing the first-party code developers actually write.*

## SAST versus SCA

[Chapter 3](03-snyk-open-source-sca.md) covered SCA — vulnerabilities in *other people's* code (dependencies). **Snyk Code** is **SAST** (Static Application Security Testing) — vulnerabilities in **your** code, the first-party logic you write. Where SCA matches known packages to known CVEs, SAST **analyzes your source** for insecure patterns: SQL injection, cross-site scripting, path traversal, hardcoded secrets, unsafe deserialization — the [OWASP Top 10](07-ai-and-secure-development.md) classes, in the code you just wrote.

The two are complementary halves of application security: SCA covers the ~80% of the app that is dependencies, SAST covers the ~20% that is yours — and your 20% is where your *business logic* bugs live, the ones no CVE database knows about because you just invented them.

## Data-flow analysis

Good SAST is not grep for scary function names. The signal is **data flow**: does *untrusted input* (a request parameter, a form field) reach a *dangerous sink* (a SQL query, a shell command, an HTML response) **without sanitization** in between? That path — **source → (no sanitizer) → sink** — is the vulnerability; the same sink is perfectly safe if the data reaching it is trusted or sanitized.

This is why naive SAST drowns in noise: it flags every `execute()` call, most of which are safe. Snyk Code traces the actual flow from untrusted sources to sensitive sinks, flagging only the paths where tainted data reaches a sink unsanitized — dramatically fewer, truer findings. The lab models source-to-sink taint tracking.

## The false-positive problem

The historical curse of SAST is **false positives** — flagging code that is not actually vulnerable. False positives are not a minor annoyance; they are a *security* failure, because a tool that cries wolf gets **ignored**, and an ignored tool secures nothing (the [adoption lesson from Chapter 2](02-developer-first-application-security.md)). A scanner with 60% false positives trains developers to dismiss its output, including the 40% that are real.

Snyk Code's pitch is **high accuracy via DeepCode AI** — an AI engine trained on millions of commits and fixes that understands code semantics well enough to cut false positives, and to suggest fixes. Combined with **real-time in-IDE scanning** (results as you type, not in a batch report), the goal is findings developers *trust and act on*. The lab models why false-positive rate governs real-world value.

## Hands-On Lab

Python models SAST analysis. **Cost:** none.

### Lab 4.1 — Source-to-sink taint tracking

**Objective:** Distinguish a real vulnerability from a safe use of the same sink.

```bash
python3 - <<'EOF'
# code snippets: does untrusted input reach a dangerous sink WITHOUT sanitization?
SNIPPETS = [
  # id,   source(untrusted?),  sanitized,  sink
  ("A", True,  False, "db.execute(query)"),     # tainted -> sink, unsanitized -> VULN
  ("B", True,  True,  "db.execute(query)"),      # tainted but SANITIZED -> safe
  ("C", False, False, "db.execute(query)"),      # sink, but data is a constant -> safe
  ("D", True,  False, "os.system(cmd)"),         # tainted -> shell -> VULN (worse)
  ("E", False, False, "render(template)"),       # trusted -> safe
]
print("SAST via DATA FLOW: source -> (sanitizer?) -> sink\n")
print(f"   {'id':4}{'untrusted src':>15}{'sanitized':>11}{'sink':>22}   verdict")
vulns = []
for sid, src, san, sink in SNIPPETS:
    vuln = src and not san
    if vuln: vulns.append(sid)
    v = "!! VULNERABLE" if vuln else "safe"
    print(f"   {sid:4}{str(src):>15}{str(san):>11}{sink:>22}   {v}")
print(f"\nflagged: {vulns}  (only where UNTRUSTED input reaches a sink UNSANITIZED)")
print("\nWhy this beats grep-for-scary-functions:")
print("  - A and B call the SAME sink (db.execute) — but B sanitizes, so only A is a")
print("    vuln. A naive scanner flags BOTH and cries wolf on B.")
print("  - C calls db.execute too, but with a CONSTANT (trusted) — safe. Flagging it")
print("    is a false positive.")
print("  - the vulnerability is the PATH: untrusted SOURCE -> unsanitized -> dangerous")
print("    SINK. Same sink is safe or dangerous depending on what FLOWS to it.")
print("\nSnyk Code traces the actual data flow, so it flags A and D (real) and stays")
print("quiet on B, C, E (safe) — far fewer, TRUER findings than pattern-matching the")
print("sink name. That flow analysis is what separates SAST that devs trust from SAST")
print("that devs mute.")
EOF
```

**Expected result:** Only the snippets where untrusted input reaches a dangerous sink without sanitization flagged, while the same sink used safely (sanitized, or with constant data) is correctly not. The data-flow lesson is that the vulnerability is the source-to-sink path, not the sink name — tracing actual flow yields far fewer, truer findings than pattern-matching function names.

**Negative test:** Flagging every call to a dangerous sink like `db.execute`. Snippets B and C use it safely (sanitized, constant data); flagging them is the false-positive noise that trains developers to ignore the tool.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — False-positive rate governs real-world value

**Objective:** Show why accuracy, not raw detection, decides whether SAST helps.

```bash
python3 - <<'EOF'
REAL_VULNS = 100        # actual vulnerabilities present
TOOLS = [
  # tool,                 detected_real, false_positives, dev_trust_threshold
  ("noisy SAST",           95,            900,             None),
  ("Snyk Code (DeepCode)", 88,            70,              None),
]
print("100 real vulns in the codebase. Two SAST tools:\n")
for name, real, fp, _ in TOOLS:
    total = real + fp
    precision = 100*real/total
    print(f"{name}:")
    print(f"   finds {real}/100 real  +  {fp} false positives  =  {total} alerts")
    print(f"   precision (real / total alerts): {precision:.0f}%")
    # model dev behavior: above ~50% noise, devs start ignoring ALL output
    if precision < 20:
        acted = int(real * 0.15)
        print(f"   -> {precision:.0f}% precision: devs DROWN in noise, mute the tool,")
        print(f"      fix only ~{acted} even of the real ones\n")
    else:
        acted = int(real * 0.75)
        print(f"   -> {precision:.0f}% precision: devs TRUST it, fix ~{acted} of the real vulns\n")
print("The noisy tool DETECTS more (95 vs 88) but its 900 false positives bury the")
print("signal at ~10% precision. Developers learn the tool cries wolf and MUTE it —")
print("so even its real findings go unfixed. The accurate tool finds slightly fewer")
print("but at ~56% precision devs TRUST and act on it, fixing far more real vulns.")
print("\nFalse positives aren't a UX nit — they're a SECURITY failure: a muted tool")
print("secures nothing. This is why Snyk Code leans on DeepCode AI for accuracy and")
print("runs in the IDE in real time: the goal is findings developers BELIEVE and FIX,")
print("not the biggest detection number. Same 'adoption is the multiplier' lesson as")
print("Chapter 2, sharpened — here trust is destroyed by noise.")
EOF
```

**Expected result:** The noisy SAST tool detecting slightly more but drowning developers at ~10% precision so its findings get muted, while the accurate tool at higher precision is trusted and its real findings fixed. The false-positive lesson is that accuracy governs real-world value — a muted tool secures nothing, so precision (and the DeepCode AI and in-IDE experience behind it) is a security property, not a nicety.

**Negative test:** Choosing SAST by detection count. The noisy tool finds 95 of 100 but with 900 false positives at ~10% precision it gets ignored — a tool that finds fewer at high precision reduces more real risk because developers trust and act on it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SAST distinguished from SCA — first-party code vulnerabilities versus dependency vulnerabilities.
- [ ] Data-flow analysis understood as tracing untrusted source to dangerous sink without sanitization.
- [ ] False positives recognized as a security failure — a muted tool secures nothing.
- [ ] DeepCode AI and real-time in-IDE scanning placed as the accuracy-and-trust play.
