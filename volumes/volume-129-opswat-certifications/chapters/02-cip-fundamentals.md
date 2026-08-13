# Chapter 02: CIP Fundamentals (ICIP / OCFA)

## Learning Objectives

- Cover the ICIP and OCFA foundations: critical infrastructure, the CIP threat model, and defense philosophy.
- Understand OPSWAT's "trust no file, trust no device" premise and its core technologies.
- Model the CIP threat surfaces the rest of the volume defends.

## The certificates in brief

**ICIP** (Introduction to Critical Infrastructure Protection) is the free entry point: what critical infrastructure is, how to identify critical networks, and the CIP mindset. **OCFA** (Cybersecurity Fundamentals Associate) grounds the broader vocabulary — information security vs cybersecurity vs ethical hacking, technologies, and career paths. Together they are the vendor-neutral CIP foundation the Associate certs build on.

## What is critical infrastructure, and why it's different

**Critical infrastructure** is the systems society depends on: energy, water, manufacturing, transportation, healthcare, finance, government. Attacks on it threaten **physical safety and continuity of essential services**, not just data. That raises the stakes and shifts the defensive priorities toward the OT concerns of [Volume CXXVIII](../../volume-128-isa-iec-62443-certifications/README.md) (availability and safety first).

OPSWAT's premise for defending it: **trust no file and no device** entering a critical environment. Every file could carry weaponized content; every removable device or endpoint could be a carrier. CIP defense inspects and sanitizes at every boundary.

## Hands-On Lab

Python models the CIP threat surfaces. **Cost:** none.

### Lab 2.1 — Identify critical networks and their boundaries

**Objective:** Map where untrusted data enters a critical environment — the ICIP core skill.

```bash
python3 - <<'EOF'
# CIP entry points: every path by which external files/devices reach critical assets
entry_points = [
  {"path":"email attachments -> workstation", "boundary":"mail gateway", "control":"CDR + multiscan"},
  {"path":"web downloads -> workstation",     "boundary":"web proxy (ICAP)", "control":"CDR + multiscan"},
  {"path":"USB drive -> engineering laptop",  "boundary":"kiosk", "control":"scan media before use"},
  {"path":"vendor file -> OT via transfer",   "boundary":"secure transfer/vault", "control":"scan + escort"},
  {"path":"contractor laptop -> plant net",   "boundary":"NAC", "control":"posture check before admit"},
]
print(f"{'entry path':<32}{'boundary':<22}control")
for e in entry_points:
    print(f"{e['path']:<32}{e['boundary']:<22}{e['control']}")
print("\nCIP principle: inspect/sanitize at EVERY boundary — trust no file, no device.")
EOF
```

**Expected result:** A map of entry paths (email, web, USB, vendor transfer, contractor laptop) each with its boundary and control — the ICIP skill of finding where untrusted data crosses into a critical network. Every one of these boundaries is a place OPSWAT's technologies (CDR, multiscan, kiosk, vault, NAC) apply, and each maps to a later chapter.

**Negative test:** Securing only the internet perimeter while leaving USB and vendor-file paths uninspected — the majority of OT infections arrive via removable media and trusted-vendor files, not the internet; CIP covers *every* boundary.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — The threat model: weaponized files and carrier devices

**Objective:** Understand what "trust no file" defends against.

```bash
python3 - <<'EOF'
# Why a "clean-looking" file is still untrusted: active content is the payload vector
file_risks = {
  "invoice.docx": ["macros (VBA)", "embedded OLE objects", "remote template injection"],
  "report.pdf":   ["JavaScript", "embedded files", "launch actions"],
  "firmware.zip": ["nested archives (evasion)", "unexpected executables", "path traversal"],
  "image.jpg":    ["polyglot / appended payload", "malformed headers (parser exploits)"],
}
for f, risks in file_risks.items():
    print(f"{f:<14} active-content risks: {', '.join(risks)}")
print("\nA signature-clean file can still carry weaponized active content -> the case for CDR (Ch 03).")
EOF
```

**Expected result:** Common file types with their active-content risks — macros in documents, JavaScript in PDFs, nested archives, polyglots. The CIP insight: **a file that passes antivirus can still be weaponized** through active content antivirus doesn't flag; that gap is exactly what Content Disarm & Reconstruction (Chapter 03) closes.

**Negative test:** Relying on a single antivirus scan to "clear" a file — signature AV misses zero-days and benign-looking active content; CIP combines multiscanning (Chapter 04) with CDR (Chapter 03), not AV alone.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — OPSWAT core technologies at a glance

**Objective:** Name the technologies and the threat each addresses.

```bash
python3 - <<'EOF'
tech = {
  "Deep CDR":       "rebuild the file without active content (zero-day-proof for embedded threats)",
  "Multiscanning":  "many AV engines in parallel (raise detection of known malware)",
  "Proactive DLP":  "find/redact sensitive data before it crosses a boundary",
  "Sandbox":        "detonate the unknown to observe behavior",
  "MetaAccess (NAC)":"admit only compliant devices (endpoint posture)",
  "Kiosk":          "scan removable media before it enters the network (esp. air-gapped OT)",
  "Vault":          "secure, scanned file storage and transfer across trust zones",
  "ICAP":           "apply CDR/multiscan to web/proxy traffic inline",
}
for t, purpose in tech.items(): print(f"{t:<18}{purpose}")
EOF
```

**Expected result:** The technology-to-threat map — CDR for active content, multiscanning for known malware, NAC for device trust, kiosk/vault for the OT boundary, ICAP for web. OCFA/ICIP establish this vocabulary; the rest of the volume drills each. Together they implement "trust no file, no device" at every boundary from Lab 2.1.

**Negative test:** Treating any single technology as sufficient — CDR handles active content but not a compromised device; NAC handles device trust but not a weaponized file. CIP layers them, which is the program's through-line.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Critical infrastructure and why its stakes differ (safety/continuity) understood.
- [ ] Every CIP entry boundary mapped (email/web/USB/vendor/contractor).
- [ ] The "trust no file, no device" threat model and OPSWAT's core technologies internalized.
