# Chapter 05: Digital Forensics and Incident Response

## Learning Objectives

- Handle an incident through the response lifecycle (GCIH).
- Analyze hosts and memory forensically (GCFA).
- Perform network forensics (GNFA).
- Triage malware with reverse-engineering basics (GREM).
- Apply cyber threat intelligence (GCTI).
- Complete a walkthrough for each DFIR domain.

## Theory and Architecture

The **DFIR** focus area validates responders and forensic analysts. **GCIH (Certified Incident
Handler)** covers the **incident-response lifecycle** — preparation, identification, containment,
eradication, recovery, and lessons learned — and common attack techniques from the defender's side.
**GCFA (Certified Forensic Analyst)** covers deep host and **memory forensics** — timelines,
artifacts, and threat detection on disk and in RAM (with **CyberLive**). **GNFA (Network Forensic
Analyst)** covers reconstructing activity from **network evidence** (pcap, flows, protocol
artifacts). **GREM (Reverse-Engineering Malware)** covers analyzing malicious code — behavioral and
static triage — to produce indicators. **GCTI (Cyber Threat Intelligence)** covers turning
observations into **structured intelligence** (indicators, ATT&CK mapping, attribution) that drives
detection and response. Many DFIR exams are **CyberLive**. This chapter teaches each with a hands-on
defensive walkthrough using open tools (Volatility concepts, strings/YARA, tshark, STIX/ATT&CK).

## Design Considerations

Preserve **evidence integrity** (hashes, chain of custody) before analysis. Work from a **timeline**
(GCFA). Prefer **memory** for volatile artifacts. Reconstruct from **network evidence** when hosts
are unavailable (GNFA). Triage malware for **indicators**, not just verdicts (GREM). Structure
intelligence to **ATT&CK/STIX** so it is actionable (GCTI). Follow the **IR lifecycle** end to end
(GCIH).

## Implementation and Automation

The labs walk the IR lifecycle, hash evidence, extract IOCs, analyze a capture, and structure intel.

## Validation and Troubleshooting

Confirm the DFIR map:

```text
GCIH = IR lifecycle (prep/identify/contain/eradicate/recover/lessons). GCFA = host + memory forensics + timelines.
GNFA = network forensics (pcap/flows). GREM = malware reverse-engineering/triage -> IOCs. GCTI = structured intel (IOC/ATT&CK/STIX).
```

Common pitfalls: analyzing evidence before **preserving** it (integrity lost); and producing a
malware "verdict" with no **indicators** for detection.

## Security and Best Practices

Preserve integrity first (hash + custody), analyze from timelines, extract **actionable indicators**,
and structure intelligence to ATT&CK/STIX. Work on authorized evidence in a lab. All DFIR work is
defensive.

## Hands-On Lab

DFIR walkthroughs. **Shared prerequisites** — Linux with `python3`, `sha256sum`, `strings`, `tshark`,
in a lab. **Cost:** none.

### Lab 5.1 — GCIH: walk the incident-response lifecycle

**Objective:** Structure a response.

```python
python3 - <<'PY'
phases=["Preparation","Identification","Containment","Eradication","Recovery","Lessons Learned"]
incident="phishing -> credential theft -> suspicious VPN login"
for i,p in enumerate(phases,1):
    print(f"{i}. {p}")
print("\nGCIH: every incident follows this lifecycle;", incident)
PY
```

**Expected result:** the **six IR phases** applied to an incident — the GCIH structure.

**Negative test:** jump to eradication before **containment**; the adversary spreads while you clean
one host — contain first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — GCFA: preserve evidence integrity

**Objective:** Hash before analysis.

```bash
echo "suspicious artifact bytes" > evidence.bin
sha256sum evidence.bin | tee evidence.sha256      # baseline hash (chain of custody)
# ... analysis happens on a copy ...
sha256sum -c evidence.sha256                       # prove the evidence is unchanged
```

**Expected result:** a recorded hash and an **OK** integrity check — evidence preservation, the GCFA
foundation.

**Negative test:** edit the evidence in place then compute a hash; you've destroyed the original —
**hash first**, analyze a copy.

**Rollback:** `rm -f evidence.bin evidence.sha256`.

### Lab 5.3 — GREM: triage a sample for indicators

**Objective:** Extract IOCs without executing.

```bash
printf 'MZ\x90\x00 evilhost.example.com POST /c2 kernel32.dll' > sample.bin
strings sample.bin | grep -Ei 'http|\.com|dll|POST' \
  | tee /dev/stderr | wc -l                        # candidate IOCs (domains, URIs, imports)
echo "GREM: static triage -> indicators (never run malware outside an isolated lab)"
```

**Expected result:** extracted candidate **indicators** (host, URI, imported DLL) via static
strings — safe GREM triage.

**Negative test:** run the sample to "see what it does" on your workstation; malware triage is
**static/isolated** — never execute on a live host.

**Rollback:** `rm -f sample.bin`.

### Lab 5.4 — GNFA: reconstruct from network evidence

**Objective:** Find activity in a capture.

```bash
tcpdump -w /tmp/net.pcap -c 30 -i lo 2>/dev/null & (ping -c 4 127.0.0.1 >/dev/null); wait
tshark -r /tmp/net.pcap -q -z endpoints,ip 2>/dev/null | head    # who talked to whom
tshark -r /tmp/net.pcap -Y "icmp" -T fields -e ip.src -e ip.dst 2>/dev/null | head
```

**Expected result:** endpoints and flows reconstructed from the **pcap** — network forensics (GNFA).

**Negative test:** rely on host logs alone after they've been wiped; **network evidence** survives
independently — capture and analyze it.

**Rollback:** `rm -f /tmp/net.pcap`.

### Lab 5.5 — GCTI: structure threat intelligence

**Objective:** Make intel actionable.

```python
python3 - <<'PY'
ioc={"type":"domain","value":"evilhost.example.com","attck":"T1071 App-Layer C2",
     "confidence":"medium","action":"add to DNS blocklist + hunt in proxy logs"}
for k,v in ioc.items(): print(f"{k:11}: {v}")
print("GCTI: an indicator + ATT&CK mapping + action = intelligence, not just data")
PY
```

**Expected result:** an indicator mapped to **ATT&CK** with a defensive action — structured GCTI
intelligence.

**Negative test:** dump a raw IOC list with no context or action; defenders can't operationalize it
— add **mapping and action**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

DFIR spans incident handling (GCIH), host/memory forensics (GCFA), network forensics (GNFA), malware
reverse-engineering (GREM), and threat intelligence (GCTI) — preserving evidence, extracting
indicators, and structuring intel to ATT&CK, validated hands-on with CyberLive.

- [ ] I can walk the IR lifecycle (GCIH).
- [ ] I can preserve evidence integrity (GCFA).
- [ ] I can triage malware for indicators safely (GREM).
- [ ] I can reconstruct from network evidence and structure intel (GNFA/GCTI).
- [ ] I completed Labs 5.1–5.5 including each negative test.
