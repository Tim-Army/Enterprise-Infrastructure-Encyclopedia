# Chapter 06: CWAP — Analysis Professional

## Learning Objectives

- Explain the CWAP scope: 802.11 protocol analysis and troubleshooting.
- Capture 802.11 frames in monitor mode.
- Analyze the association and authentication exchange.
- Diagnose retries, interference, and performance issues.
- Complete a walkthrough for each analysis topic (defensive).

## Theory and Architecture

**CWAP** (Certified Wireless Analysis Professional) is the deep-dive into **802.11 protocol
analysis** — reading what actually happens on the air to troubleshoot WLANs. It requires
**monitor-mode** capture (a radio that records all frames on a channel, not just its own traffic),
producing a capture you analyze in **Wireshark/tshark** with the **radiotap** header (RSSI, data
rate, channel) and 802.11 fields. The analyst follows the **connection lifecycle**: beacon → probe
request/response → **authentication** → **association** → 4-way handshake → data. Problems show up
as **retries** (`wlan.fc.retry`), low **data rates** (rate shifting from poor SNR), **excessive
management traffic**, **retransmissions**, and airtime consumed by legacy/slow clients. CWAP also
covers **spectrum analysis** (non-Wi-Fi interference) versus **protocol analysis** (Wi-Fi
behavior). Analysis is **defensive** — you capture and read your own or authorized networks to fix
them.

## Design Considerations

Capture in **monitor mode** on the **right channel** (the one under test). Use the **radiotap**
metadata (RSSI/rate/retry) with 802.11 fields. Distinguish a **protocol** problem (Wi-Fi behavior)
from a **spectrum** problem (interference) — they need different tools. Baseline healthy behavior so
anomalies stand out.

## Implementation and Automation

The labs capture and filter 802.11, follow the association exchange, and quantify retries — all
**defensive analysis**.

## Validation and Troubleshooting

Confirm the analysis model:

```text
Monitor-mode capture -> Wireshark/tshark + radiotap (RSSI/rate/channel) + 802.11 fields.
Lifecycle: beacon -> probe -> auth -> assoc -> 4-way handshake -> data.
Symptoms: retries (wlan.fc.retry), rate shifting (low SNR), mgmt overhead, legacy airtime.
Protocol analysis (Wi-Fi behavior) vs spectrum analysis (interference). CWAP = defensive.
```

Common pitfalls: capturing on the **wrong channel** (miss the traffic); and confusing
**interference** (spectrum) with a **protocol** issue.

## Security and Best Practices

Capture only **authorized** networks, on the **correct channel**, in **monitor mode**. Use
**baselines** to spot anomalies. Separate **spectrum** from **protocol** diagnosis. Document
findings. This is defensive troubleshooting.

## Hands-On Lab

Analysis walkthroughs (defensive). **Shared prerequisites** — `tshark`/Wireshark and an
**authorized** 802.11 monitor-mode capture of your own lab WLAN. **Cost:** none.

### Lab 6.1 — Read radiotap metadata

**Objective:** Extract RSSI, rate, and channel per frame.

```bash
tshark -r wlan.pcapng -T fields -e wlan_radio.signal_dbm -e wlan_radio.data_rate -e wlan_radio.channel -c 5 2>/dev/null \
  | head || echo "radiotap gives per-frame RSSI (signal_dbm), data_rate, and channel for analysis"
```

**Expected result:** per-frame **RSSI, data rate, and channel** — the analyst's raw signal view.

**Negative test:** analyze 802.11 with no **radiotap** metadata; RSSI/rate/channel are essential —
capture with radiotap.

**Rollback:** none (read-only analysis).

### Lab 6.2 — Follow the association exchange

**Objective:** Trace a client joining a BSS.

```bash
tshark -r wlan.pcapng -Y "wlan.fc.type_subtype in {0x00 0x01 0x0b 0x00}" -c 10 2>/dev/null | head \
  || echo "assoc-req(0x00)/assoc-resp(0x01)/auth(0x0b): follow the join sequence in order"
```

**Expected result:** the **authentication → association** management frames in order — the join
lifecycle.

**Negative test:** debug a "won't connect" issue by looking only at data frames; the failure is in
the **auth/assoc** exchange — analyze it.

**Rollback:** none (read-only analysis).

### Lab 6.3 — Quantify retries

**Objective:** Measure retransmission rate.

```bash
total=$(tshark -r wlan.pcapng 2>/dev/null | wc -l); retries=$(tshark -r wlan.pcapng -Y "wlan.fc.retry==1" 2>/dev/null | wc -l); \
python3 -c "print(f'retry rate: {100*$retries/max(1,$total):.1f}%')" 2>/dev/null \
  || echo "wlan.fc.retry==1 counts retransmissions; a high retry % indicates RF problems"
```

**Expected result:** a **retry percentage** — high values point to interference, low SNR, or
contention.

**Negative test:** blame the AP for "slow Wi-Fi" without measuring retries; a high **retry rate**
localizes the RF problem — measure it.

**Rollback:** none (read-only analysis).

### Lab 6.4 — Protocol vs spectrum

**Objective:** Decide which analysis a symptom needs.

```python
python3 - <<'PY'
symptoms={"High retries but clean protocol":"spectrum analysis (non-Wi-Fi interference)",
          "Auth/assoc failures":"protocol analysis (Wi-Fi behavior/config)",
          "Throughput low, SNR low":"RF/coverage (design)","Legacy client slowing cell":"protocol (airtime)"}
for s,tool in symptoms.items(): print(f"- {s} -> {tool}")
PY
```

**Expected result:** each symptom routed to **protocol** or **spectrum** analysis — the right tool
for the problem.

**Negative test:** use protocol analysis for a **microwave-oven interference** problem; that needs
**spectrum analysis** — match the tool.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CWAP covers 802.11 protocol analysis: monitor-mode capture with radiotap, following the
beacon→probe→auth→assoc→handshake lifecycle, quantifying retries and rate shifting, and separating
protocol from spectrum problems. Capture authorized networks on the right channel, baseline, and
diagnose systematically.

- [ ] I can read radiotap RSSI/rate/channel.
- [ ] I can follow the association exchange.
- [ ] I can quantify the retry rate.
- [ ] I can distinguish protocol from spectrum issues.
- [ ] I completed Labs 6.1–6.4 including each negative test.
