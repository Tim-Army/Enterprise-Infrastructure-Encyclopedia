# Chapter 03: File Security (OFSA) — Content Disarm and Reconstruction

## Learning Objectives

- Cover OPSWAT's signature technique: Deep CDR (Content Disarm and Reconstruction).
- Understand why CDR is zero-day-resistant where detection alone is not.
- Build a working CDR model that strips active content from files.

## The certificate in brief

**OFSA** (File Security Associate) is about protecting critical file systems: the risks of unsecured file uploads, static vs dynamic analysis, and the technologies that defend against known and unknown threats. Its centerpiece — and OPSWAT's flagship — is **Deep CDR**. This chapter builds CDR; [Chapter 04](04-file-security-multiscanning.md) covers multiscanning and DLP.

## What CDR does (and why it beats detection)

**Detection** (antivirus, sandboxing) asks *"is this file malicious?"* — and can be wrong on a zero-day. **CDR** doesn't ask; it **assumes every file may be weaponized and rebuilds a clean one**: it deconstructs the file, removes any active/abnormal content (macros, scripts, embedded objects, JavaScript), and reconstructs a usable file with only legitimate content. The threat is gone whether or not anyone recognized it.

| Approach | Question | Zero-day? |
|:---|:---|:---|
| Signature AV | "Does this match known malware?" | Misses unknowns |
| Sandbox | "Does this behave maliciously?" | Evadable; slow |
| **Deep CDR** | *(doesn't ask)* — "rebuild it clean" | **Removes the vector regardless** |

## Hands-On Lab

Python models CDR on real file structures. **Cost:** none.

### Lab 3.1 — Strip active content from a document (CDR core)

**Objective:** Model CDR: rebuild an Office document without its macros.

```bash
python3 - <<'EOF'
import zipfile, io, os
# An OOXML document (.docx/.xlsm) is a ZIP; macros live in vbaProject.bin + a content-type entry.
# Build a tiny "document with a macro", then CDR it by rebuilding WITHOUT the active parts.
def make_doc(with_macro=True):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", "<Types>...docx...</Types>")
        z.writestr("word/document.xml", "<w:document>legitimate text</w:document>")
        if with_macro:
            z.writestr("word/vbaProject.bin", b"\x00MACRO-PAYLOAD\x00")   # active content
    return buf.getvalue()

def deep_cdr(data):
    ACTIVE = ("vbaProject.bin", "vbaData.xml", "/macros/")   # parts CDR removes
    src = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO(); removed = []
    with zipfile.ZipFile(out, "w") as z:
        for name in src.namelist():
            if any(a in name for a in ACTIVE):
                removed.append(name); continue          # disarm: drop active content
            z.writestr(name, src.read(name))            # reconstruct: keep legitimate content
    return out.getvalue(), removed

original = make_doc(with_macro=True)
cleaned, removed = deep_cdr(original)
print("original parts:", zipfile.ZipFile(io.BytesIO(original)).namelist())
print("removed by CDR:", removed)
print("rebuilt  parts:", zipfile.ZipFile(io.BytesIO(cleaned)).namelist())
print("document text preserved:", "legitimate text" in zipfile.ZipFile(io.BytesIO(cleaned)).read("word/document.xml").decode())
EOF
```

**Expected result:**

```text
original parts: ['[Content_Types].xml', 'word/document.xml', 'word/vbaProject.bin']
removed by CDR: ['word/vbaProject.bin']
rebuilt  parts: ['[Content_Types].xml', 'word/document.xml']
document text preserved: True
```

The macro (`vbaProject.bin`) is removed and a clean, still-usable document is rebuilt — **the legitimate text survives, the active content does not**. That is Deep CDR: not detection, but reconstruction. Production CDR does this for 100+ file types with far deeper structural rebuilding, but the principle is exactly this.

**Negative test:** "Detecting and quarantining" the macro instead — if the macro is a novel variant AV doesn't flag, detection passes it through; CDR removes it whether recognized or not, which is why CIP uses CDR for the file boundary.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — CDR handles nested and evasive structures

**Objective:** Show CDR recursing into nested archives (a common evasion).

```bash
python3 - <<'EOF'
import zipfile, io
# Malware nests payloads in archives-within-archives to evade shallow scanners.
def build_nested():
    inner = io.BytesIO()
    with zipfile.ZipFile(inner, "w") as z:
        z.writestr("readme.txt", "ok")
        z.writestr("payload.exe", b"MZ...executable...")    # hidden deep inside
    outer = io.BytesIO()
    with zipfile.ZipFile(outer, "w") as z:
        z.writestr("docs/report.txt", "ok")
        z.writestr("docs/bundle.zip", inner.getvalue())
    return outer.getvalue()

def cdr_recursive(data, depth=0, max_depth=5):
    if depth > max_depth: return "REJECT (archive too deep — possible zip bomb/evasion)"
    z = zipfile.ZipFile(io.BytesIO(data)); actions = []
    for name in z.namelist():
        if name.endswith(".exe"):
            actions.append(f"{'  '*depth}remove {name} (executable in archive)")
        elif name.endswith(".zip"):
            actions.append(f"{'  '*depth}recurse into {name}:")
            actions.append(cdr_recursive(z.read(name), depth+1, max_depth))
        else:
            actions.append(f"{'  '*depth}keep {name}")
    return "\n".join(actions)

print(cdr_recursive(build_nested()))
EOF
```

**Expected result:** CDR recurses into `bundle.zip` and removes the buried `payload.exe`, with a depth limit rejecting suspiciously deep nesting (zip-bomb/evasion defense). Shallow scanners that don't unpack nested archives miss the payload; **CDR's recursive reconstruction reaches it** — a distinction OFSA tests.

**Negative test:** A scanner that only inspects the top-level archive — the nested `.exe` sails through; recursion (with a sane depth limit) is mandatory for the file boundary.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — When CDR must preserve function

**Objective:** Understand CDR's usability trade-off and configuration.

```bash
python3 - <<'EOF'
# CDR removes active content — but some workflows legitimately need macros/scripts.
# The design choice: sanitize by default; allow-list only vetted, signed exceptions by policy.
def cdr_policy(file_type, has_active, source_trusted, signed):
    if not has_active: return "PASS (no active content)"
    if source_trusted and signed: return "ALLOW active content (vetted signed exception) — logged"
    return "DISARM active content, deliver rebuilt file"
print(cdr_policy("docx", True, False, False))
print(cdr_policy("xlsm", True, True, True))
print(cdr_policy("pdf",  True, False, False))
EOF
```

**Expected result:** Default disarm, with a narrow, logged allow-list only for trusted+signed active content — the CDR usability trade-off. CDR that breaks every macro-driven business workflow gets disabled; the OFSA skill is configuring **sanitize-by-default with vetted exceptions**, preserving legitimate function while removing the threat vector.

**Negative test:** Disabling CDR because "it broke a spreadsheet" — you reopen the whole active-content vector; the correct response is a scoped, signed exception, not turning off the control.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CDR's reconstruct-don't-detect principle (zero-day resistance) internalized.
- [ ] A working CDR model built: active content stripped, legitimate content preserved.
- [ ] Recursive handling of nested archives and the sanitize-by-default-with-exceptions policy drilled.
