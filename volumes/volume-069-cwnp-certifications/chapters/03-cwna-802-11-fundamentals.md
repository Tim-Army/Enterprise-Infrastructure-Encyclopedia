# Chapter 03: CWNA — 802.11 Fundamentals

## Learning Objectives

- Explain the CWNA foundation and the 802.11 standard family.
- Identify the frequency bands and channels (2.4/5/6 GHz).
- Distinguish 802.11 frame types (management, control, data).
- Reason about Wi-Fi 6/6E and Wi-Fi 7 features.
- Complete a walkthrough for each 802.11 fundamentals topic.

## Theory and Architecture

**CWNA** is the foundation certification, and its core is the **802.11** standard. Wi-Fi operates
in **bands**: **2.4 GHz** (three non-overlapping 20 MHz channels — crowded), **5 GHz** (many
channels, some **DFS** for radar avoidance), and **6 GHz** (**Wi-Fi 6E** — wide, clean spectrum).
Channels bond into **20/40/80/160 MHz** widths (and **320 MHz** in Wi-Fi 7). 802.11 traffic uses
three **frame types**: **management** (beacons, probe/association/authentication — building and
maintaining connectivity), **control** (RTS/CTS, ACK — coordinating access), and **data** (the
payload). Devices form a **BSS** (one AP + clients) identified by a **BSSID**, joined into an
**ESS** (one SSID across many APs) for roaming. **Wi-Fi 6/6E (802.11ax)** adds **OFDMA** (dividing
a channel among clients), **MU-MIMO**, and **BSS coloring**; **Wi-Fi 7 (802.11be)** adds **320 MHz
channels**, **4K-QAM**, and **Multi-Link Operation (MLO)**. CWNA proves you understand how Wi-Fi
actually works on the air.

## Design Considerations

Plan **channels** to avoid co-channel/adjacent-channel interference (only 3 usable 20 MHz channels
in 2.4 GHz — use 1/6/11). Prefer **5/6 GHz** for capacity. Match **channel width** to density
(wider = more throughput but fewer non-overlapping channels). Exploit **OFDMA/MU-MIMO** for
efficiency in dense areas.

## Implementation and Automation

The labs reason about bands/channels, decode frame types (via capture), and compare Wi-Fi
generations.

## Validation and Troubleshooting

Confirm the 802.11 model:

```text
Bands: 2.4 GHz (1/6/11), 5 GHz (+DFS), 6 GHz (Wi-Fi 6E). Widths: 20/40/80/160 (320 in Wi-Fi 7).
Frames: management (beacon/probe/assoc/auth), control (RTS/CTS/ACK), data.
BSS (AP+clients, BSSID) -> ESS (one SSID, roaming). Wi-Fi 6/6E: OFDMA/MU-MIMO/BSS coloring. Wi-Fi 7: 320MHz/4K-QAM/MLO.
```

Common pitfalls: using overlapping **2.4 GHz** channels (only 1/6/11 don't overlap); and
over-wide channels in dense areas (fewer non-overlapping channels).

## Security and Best Practices

Use **1/6/11** in 2.4 GHz, prefer **5/6 GHz** for capacity, and size **channel width** to density.
Understand **management frames** (many are unprotected without PMF — Chapter 5). Design for the
Wi-Fi generation your clients actually support.

## Hands-On Lab

802.11 walkthroughs. **Shared prerequisites** — a shell with `python3`; Labs 3.2/3.4 use
`tshark`/Wireshark on an authorized capture. **Cost:** none (analysis of your own lab capture).

### Lab 3.1 — 2.4 GHz channel plan

**Objective:** Choose non-overlapping channels.

```python
python3 - <<'PY'
non_overlap=[1,6,11]
plan={"AP1":1,"AP2":6,"AP3":11,"AP4":1}
bad=[ap for ap,ch in plan.items() if ch not in non_overlap]
print("plan:",plan); print("all non-overlapping channels used:", not bad, "(reuse 1/6/11)")
PY
```

**Expected result:** a **1/6/11** reuse plan — non-overlapping 2.4 GHz channels.

**Negative test:** assign channels 1, 3, 6 to adjacent APs; 1 and 3 **overlap** — use only 1/6/11.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Decode 802.11 frame types

**Objective:** Classify frames in a capture.

```bash
tshark -r wlan.pcapng -Y "wlan.fc.type==0" -c 5 2>/dev/null | head \
  || echo "wlan.fc.type: 0=management, 1=control, 2=data (filter an 802.11 capture by type)"
```

**Expected result:** **management** frames (type 0) filtered from the capture — recognizing frame
types.

**Negative test:** treat all 802.11 traffic as data; **management/control** frames run the network
— filter and study them.

**Rollback:** none (read-only analysis).

### Lab 3.3 — Compare Wi-Fi generations

**Objective:** Match features to 802.11ax vs 802.11be.

```python
python3 - <<'PY'
gens={"Wi-Fi 6/6E (802.11ax)":["OFDMA","MU-MIMO","BSS coloring","6 GHz (6E)"],
      "Wi-Fi 7 (802.11be)":["320 MHz channels","4K-QAM","Multi-Link Operation (MLO)"]}
for g,feats in gens.items(): print(f"{g}: {', '.join(feats)}")
PY
```

**Expected result:** the defining features of **Wi-Fi 6/6E** vs **Wi-Fi 7** — current 802.11 scope.

**Negative test:** attribute MLO to Wi-Fi 6; **MLO is Wi-Fi 7 (802.11be)** — match features to the
generation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Read a beacon

**Objective:** Inspect an AP's advertised parameters.

```bash
tshark -r wlan.pcapng -Y "wlan.fc.type_subtype==0x08" -T fields -e wlan.ssid -e wlan_radio.channel -c 3 2>/dev/null \
  | head || echo "beacon (subtype 0x08) advertises SSID, channel, capabilities, supported rates"
```

**Expected result:** the **SSID and channel** from **beacon** frames — how clients discover a BSS.

**Negative test:** assume clients "just find" the network; **beacons/probes** (management frames)
advertise it — inspect them.

**Rollback:** none (read-only analysis).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CWNA's 802.11 foundation covers the bands and channels (2.4/5/6 GHz), channel widths, the three
frame types (management/control/data), the BSS→ESS model, and the Wi-Fi 6/6E and Wi-Fi 7 feature
sets. Plan channels as 1/6/11 in 2.4 GHz, prefer 5/6 GHz, and know your frame types.

- [ ] I can build a non-overlapping 2.4 GHz channel plan.
- [ ] I can classify 802.11 frame types in a capture.
- [ ] I can compare Wi-Fi 6/6E and Wi-Fi 7 features.
- [ ] I can read a beacon's advertised parameters.
- [ ] I completed Labs 3.1–3.4 including each negative test.
