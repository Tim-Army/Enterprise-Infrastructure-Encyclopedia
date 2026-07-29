# Volume LXIX — CWNP Certification Tracks

> The whole CWNP vendor-neutral wireless program in one volume — the entry level, the CWNA
> foundation, the professional Wi-Fi (CWSP, CWAP, CWDP) and IoT (CWISA and beyond) tracks, and the
> CWNE/CWISE experts — with hands-on RF-math and 802.11 protocol-analysis labs, verified against
> cwnp.com.

## Overview

Volume LXIX maps the **CWNP** (Certified Wireless Network Professional) program — the
**vendor-neutral** standard for enterprise Wi-Fi and wireless-IoT certification. It teaches the RF
and 802.11 principles that underlie every vendor's gear, complementing the vendor wireless in HPE
Aruba (LXIV), MikroTik (LXVIII), and Cisco (XXV), and building on Wireshark (XX) and Network
Foundations (II).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXVIII): it maps
the program — the career levels and tracks — and teaches each with a hands-on walkthrough.
**CWNA is the foundation** for the professional level; every credential was **verified against
cwnp.com on 28 July 2026**, including the 2024 move to **Prometric** delivery and the Wi-Fi 6E/7
focus.

Chapters follow the career ladder:

- **Chapter 01** frames the program — the six levels, CWNA foundation, and Wi-Fi/IoT tracks.
- **Chapter 02** covers the **entry level and RF fundamentals**.
- **Chapters 03–04** take the **CWNA** administrator foundation.
- **Chapters 05–07** take the professional Wi-Fi track: **CWSP** (security), **CWAP** (analysis),
  **CWDP** (design).
- **Chapter 08** takes the **IoT track** (CWISA and beyond).
- **Chapter 09** covers the **CWNE/CWISE** experts, currency, and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** Wireless analysis uses packet capture. Every lab is **authorized capture and
> analysis** of your own or a lab network — never interception of networks you don't control.

## Chapters

1. [The CWNP Certification Program](chapters/01-the-cwnp-certification-program.md) — the six levels and tracks.
2. [Entry Level and RF Fundamentals](chapters/02-entry-and-rf-fundamentals.md) — dBm, FSPL, link budget, EIRP.
3. [CWNA — 802.11 Fundamentals](chapters/03-cwna-802-11-fundamentals.md) — bands, channels, frames, Wi-Fi 6/7.
4. [CWNA — WLAN Architecture and Security Basics](chapters/04-cwna-wlan-architecture-and-security-basics.md) — architectures, roaming, WPA2/WPA3.
5. [CWSP — Security Professional](chapters/05-cwsp-security.md) — 802.1X/EAP, 4-way handshake, PMF, WIPS.
6. [CWAP — Analysis Professional](chapters/06-cwap-analysis.md) — 802.11 protocol analysis and troubleshooting.
7. [CWDP — Design Professional](chapters/07-cwdp-design.md) — site survey, capacity, channel plan, validation.
8. [CWISA and the IoT Track](chapters/08-cwisa-iot-track.md) — BLE/Zigbee/LoRa, connectivity, integration.
9. [The Expert Level, Currency, and Career Paths](chapters/09-cwne-expert-currency-and-career.md) — CWNE/CWISE, recert.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for CWNP, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with the career
levels, tracks, and expert requirements is in the
[CWNP certification appendix](../volume-997-master-appendices/chapters/35-appendix-cwnp-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the HPE Aruba (LXIV), MikroTik
(LXVIII), Cisco (XXV), Wireshark (XX), and Network Foundations (II) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every exam domain** of
the ladder — **33 labs** in all. Because CWNP is vendor-neutral and RF/analysis-heavy, the
walkthroughs use **RF math** in `python3` (dBm/mW, FSPL, link budget, EIRP, capacity) and **802.11
protocol analysis** with `tshark`/Wireshark on **authorized** captures — all free tools. Each lab
states an objective, commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **cwnp.com** (the program) and the vendor-neutral **802.11** and wireless-IoT
standards, with **Wireshark/tshark** for protocol analysis and `python3` for RF math — no
proprietary tooling. The program was verified against cwnp.com on 28 July 2026, including the
Prometric delivery transition (1 August 2024) and the Wi-Fi 6E/7 exam focus; confirm the current
exam codes before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-069-cwnp-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
