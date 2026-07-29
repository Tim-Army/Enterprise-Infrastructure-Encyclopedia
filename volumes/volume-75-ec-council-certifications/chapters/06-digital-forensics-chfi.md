# Chapter 06: Digital Forensics — CHFI

## Learning Objectives

- Understand the CHFI forensic-investigation process.
- Preserve evidence and maintain chain of custody.
- Acquire and analyze disk and memory artifacts.
- Extract indicators and build a timeline.
- Complete a walkthrough for each forensics domain.

## Theory and Architecture

The **Computer Hacking Forensic Investigator (CHFI)** validates the **digital-forensics
investigation process** — the disciplined, legally-defensible practice of collecting, preserving,
analyzing, and reporting digital evidence. CHFI covers the forensic method: **identification and
preservation** (write-blocking, hashing, chain of custody), **acquisition** (forensic imaging of
disk and memory), **analysis** (file systems, artifacts, deleted-data recovery, memory, network,
logs), and **reporting** for legal or organizational proceedings. It spans Windows, Linux, mobile,
cloud, and anti-forensics awareness, and aligns to **US DoD 8140/8570**. The defining principle is
**integrity**: evidence must be provably unaltered (hashes, custody) and every step documented. This
chapter teaches the process with a hands-on defensive walkthrough — hashing and custody, safe
acquisition of a copy, IOC extraction, and timeline building — using open tools.

## Design Considerations

**Preserve before you analyze**: write-block, image, and hash the original; work on the **copy**.
Maintain an unbroken **chain of custody**. Build a **timeline** from artifacts. Correlate disk,
memory, network, and logs. Document everything so findings are **legally defensible**. Be aware of
**anti-forensics** (timestomping, wiping).

## Implementation and Automation

The labs preserve evidence, image a copy, extract indicators, and build a timeline.

## Validation and Troubleshooting

Confirm the CHFI map:

```text
CHFI process: identify/preserve (write-block, hash, custody) -> acquire (image disk/memory) -> analyze (FS/artifacts/memory/logs) -> report.
Principle: integrity (provably unaltered) + documentation. Windows/Linux/mobile/cloud. DoD 8140 aligned.
```

Common pitfalls: analyzing the **original** (contaminates evidence); and a broken **chain of
custody** (evidence inadmissible).

## Security and Best Practices

Preserve first (write-block + hash + custody), analyze a **copy**, build a **timeline**, correlate
sources, and **document** every step for defensibility. Watch for anti-forensics. All work is
authorized and defensive.

## Hands-On Lab

Forensics walkthroughs. **Shared prerequisites** — Linux with `python3`, `sha256sum`, `strings`, in
a lab. **Cost:** none.

### Lab 6.1 — Preserve evidence with hashing and custody

**Objective:** Prove integrity.

```bash
echo "disk-image-stand-in" > image.dd
sha256sum image.dd | tee custody.txt          # acquisition hash
cp image.dd image.copy.dd                      # analyze the COPY, not the original
sha256sum -c custody.txt                        # original still matches -> integrity intact
```

**Expected result:** an acquisition hash and an **OK** verification — CHFI preservation and custody.

**Negative test:** open and edit `image.dd` directly; the hash changes and the evidence is
contaminated — analyze the **copy**.

**Cleanup:** `rm -f image.dd image.copy.dd custody.txt`.

### Lab 6.2 — Extract indicators from an artifact

**Objective:** Pull IOCs without executing.

```bash
printf 'user=admin\nhost=evilhost.example\nurl=http://evilhost.example/x\nts=2026-08-01T02:14Z' > artifact.txt
strings artifact.txt | grep -Ei 'host=|url=|user=' | tee /dev/stderr | wc -l
echo "CHFI: static extraction of indicators (host, URL, account) for correlation"
```

**Expected result:** extracted **indicators** (host, URL, account) — CHFI artifact analysis.

**Negative test:** execute an unknown artifact to "see what it does"; analysis is **static/isolated**
— never run evidence on a live host.

**Cleanup:** `rm -f artifact.txt`.

### Lab 6.3 — Build an evidence timeline

**Objective:** Order events for the narrative.

```python
python3 - <<'PY'
events=[("2026-08-01T02:14Z","suspicious login (admin)"),
        ("2026-08-01T02:16Z","new scheduled task created"),
        ("2026-08-01T02:20Z","outbound connection to evilhost.example")]
for ts,desc in sorted(events): print(f"{ts}  {desc}")
print("CHFI: a timeline turns artifacts into a defensible narrative")
PY
```

**Expected result:** an ordered **timeline** of events — the CHFI investigative narrative.

**Negative test:** present artifacts with no timeline; investigators can't see causality — **order**
them.

**Cleanup:** none.

### Lab 6.4 — Verify report reproducibility

**Objective:** Make findings defensible.

```bash
echo "finding: admin login -> task -> C2 to evilhost.example" > report.txt
sha256sum report.txt image_hash 2>/dev/null || sha256sum report.txt
echo "CHFI: hashes + documented steps let another examiner reproduce and verify the findings"
```

**Expected result:** a hashed, documented report — **reproducible, defensible** CHFI findings.

**Negative test:** report conclusions with no hashes or steps; they can't be **verified** — document
and hash.

**Cleanup:** `rm -f report.txt`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CHFI validates the digital-forensics process — preserve (write-block, hash, custody), acquire,
analyze (artifacts, memory, timeline), and report defensibly — with integrity and documentation at
its core, aligned to DoD 8140.

- [ ] I can preserve evidence with hashing and custody.
- [ ] I can extract indicators from an artifact.
- [ ] I can build an evidence timeline.
- [ ] I can make findings reproducible and defensible.
- [ ] I completed Labs 6.1–6.4 including each negative test.
