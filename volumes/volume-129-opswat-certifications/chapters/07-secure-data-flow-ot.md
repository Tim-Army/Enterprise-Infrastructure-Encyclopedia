# Chapter 07: Secure Data Flow into OT (OSSA, Kiosk, Vault)

## Learning Objectives

- Cover OSSA and the OT data-transfer boundary: secure storage, kiosk media scanning, and secure transfer.
- Understand how files cross into air-gapped/critical networks safely.
- Model the scan-before-cross workflow.

## The certificate in brief

**OSSA** (Secure Storage Associate) covers protecting critical file storage and transfer. It is the storage/transfer half of the CIP boundary story, realized by **MetaDefender Kiosk** (scan removable media before it enters the network — vital for **air-gapped OT**) and **MetaDefender Vault** (secure, scanned file storage and controlled transfer across trust zones). This is where the file-security techniques of [Chapters 03–04](03-file-security-cdr.md) meet the OT-boundary reality of [Volume CXXVIII](../../volume-128-isa-iec-62443-certifications/README.md).

## The problem: getting files into a network you can't reach over the wire

An air-gapped OT network has no internet path — but it still needs files (firmware updates, config files, vendor deliverables). Those arrive on **removable media** or through a **controlled transfer**, which is exactly how OT malware historically spread. The CIP answer: **every file is scanned, sanitized (CDR), and escorted across the boundary; nothing crosses unchecked.**

| Mechanism | Role |
|:---|:---|
| **Kiosk** | A scanning station at the OT perimeter: insert media → multiscan + CDR + verdict → only clean, sanitized files proceed |
| **Vault** | Secure storage + workflow: files are scanned on ingest, access-controlled, and released across zones with approval |
| **Unidirectional / escorted transfer** | Move sanitized files inward with logging and (often) one-way flow |

## Hands-On Lab

Python models the boundary-crossing workflow. **Cost:** none.

### Lab 7.1 — The kiosk: scan media before it enters OT

**Objective:** Model the kiosk gate — nothing crosses without scan + sanitize.

```bash
python3 - <<'EOF'
# A USB is presented at the OT kiosk; each file must pass multiscan + CDR before release inward.
usb_files = [
  {"name":"firmware.bin", "malware":False, "active_content":False},
  {"name":"manual.pdf",   "malware":False, "active_content":True},   # has JS -> CDR
  {"name":"tool.exe",     "malware":True,  "active_content":False},  # flagged by multiscan
]
def kiosk(f):
    if f["malware"]: return f"BLOCK {f['name']} (multiscan detection) — do NOT cross into OT"
    if f["active_content"]: return f"SANITIZE {f['name']} (CDR strips active content) -> release clean copy"
    return f"RELEASE {f['name']} (clean)"
for f in usb_files: print(kiosk(f))
print("\nOnly scanned + sanitized files cross the air gap; the original media never touches OT.")
EOF
```

**Expected result:**

```text
RELEASE firmware.bin (clean)
SANITIZE manual.pdf (CDR strips active content) -> release clean copy
BLOCK tool.exe (multiscan detection) — do NOT cross into OT
```

The kiosk enforces the boundary: clean files pass, active content is disarmed, malware is blocked — and the **original untrusted media never enters OT** (only vetted copies cross). This scan-before-cross gate is the single most important control for air-gapped environments, and the reason kiosks exist.

**Negative test:** Letting an engineer plug the USB directly into an OT workstation "just this once" — that is precisely how Stuxnet-class incidents began; the kiosk exists so no removable media ever touches OT unscanned.

**Cleanup:** None.

### Lab 7.2 — The vault: scanned storage with controlled release

**Objective:** Model secure storage + approval-gated cross-zone transfer.

```bash
python3 - <<'EOF'
# Vault: files scanned on INGEST, access-controlled, released across zones only with approval + audit
class Vault:
    def __init__(self): self.store = {}
    def ingest(self, name, malicious):
        verdict = "quarantined" if malicious else "clean"
        self.store[name] = {"verdict": verdict, "approved": False}
        return f"ingest {name}: {verdict}"
    def request_release(self, name, approver):
        f = self.store.get(name)
        if not f or f["verdict"] != "clean": return f"release {name}: DENIED (not clean)"
        f["approved"] = True
        return f"release {name}: APPROVED by {approver} (audited) -> crosses to OT zone"
v = Vault()
print(v.ingest("update.zip", malicious=False))
print(v.ingest("suspicious.doc", malicious=True))
print(v.request_release("update.zip", "ot-lead"))
print(v.request_release("suspicious.doc", "ot-lead"))
EOF
```

**Expected result:** Clean files are stored and released only with named approval and audit; quarantined files can't be released. The vault adds **workflow and accountability** to the boundary — files are scanned on ingest, and crossing into OT requires approval and leaves an audit trail. Storage isn't a dumping ground; it's a controlled, scanned, access-gated waypoint.

**Negative test:** A shared drive both IT and OT can write to freely — it becomes an unscanned bridge across the boundary; the vault's scan-on-ingest and approval-gated release are what a shared drive lacks.

**Cleanup:** None.

### Lab 7.3 — The full boundary crossing

**Objective:** Assemble the end-to-end sanctioned path into OT.

```bash
python3 - <<'EOF'
# The complete sanctioned inbound path — every step from the CIP toolkit
steps = [
  "1. File arrives (email/web/USB/vendor) at the IT/OT boundary",
  "2. Multiscan (many engines) — block known malware",
  "3. Deep CDR — rebuild without active content (zero-day vector removed)",
  "4. DLP — check nothing sensitive is leaving; sandbox the truly unknown",
  "5. Vault ingest — store clean, access-controlled",
  "6. Approval + audit — named release across the zone boundary",
  "7. (Air-gapped) Kiosk / escorted media — vetted copy only crosses",
]
for s in steps: print(s)
print("\nEvery inbound file traverses this pipeline; nothing crosses the OT boundary unchecked.")
EOF
```

**Expected result:** The end-to-end pipeline — multiscan → CDR → DLP/sandbox → vault → approval/audit → kiosk/escort — the complete CIP inbound path OPSWAT's platform implements. OSSA ties the file-security techniques together into a **defensible boundary crossing**, which is the whole point of protecting critical infrastructure: untrusted data becomes trusted only after passing every gate.

**Negative test:** Any single gate skipped (no CDR, or no approval on release) reopens a vector; the pipeline is defense-in-depth, and its value is the *combination*, not any one stage.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The kiosk scan-before-cross gate for removable media/air gaps modeled.
- [ ] The vault (scan-on-ingest, approval-gated release, audit) drilled.
- [ ] The full multiscan→CDR→DLP→vault→approval→kiosk boundary pipeline assembled.
