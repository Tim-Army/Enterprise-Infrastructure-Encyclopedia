# Chapter 05: CWSP — Security Professional

## Learning Objectives

- Explain the CWSP scope: enterprise Wi-Fi security.
- Describe 802.1X/EAP authentication and the RADIUS exchange.
- Analyze the WPA2/WPA3 4-way handshake and key hierarchy.
- Apply Protected Management Frames (PMF) and WIPS.
- Complete a walkthrough for each Wi-Fi security topic (defensive).

## Theory and Architecture

**CWSP** (Certified Wireless Security Professional) is the deep security certification. Enterprise
Wi-Fi authenticates users with **802.1X/EAP**: the client (supplicant) authenticates through the AP
(authenticator) to a **RADIUS** server, using an EAP method (**EAP-TLS** with certificates,
**PEAP/EAP-TTLS** with tunneled credentials). On success, keying material derives the **PMK**
(Pairwise Master Key), and the **4-way handshake** derives the per-session **PTK** (Pairwise
Transient Key) and installs the **GTK** — this is where the actual encryption keys are established.
**WPA3** strengthens this with **SAE** (Simultaneous Authentication of Equals, replacing the
WPA2-PSK handshake's offline-attack weakness) and mandates **Protected Management Frames (PMF,
802.11w)** to stop deauth/disassoc attacks. Defense also includes a **WIPS** (Wireless Intrusion
Prevention System) to detect rogue APs and attacks, and **network segmentation**. CWSP is
**defensive** — understanding attacks to prevent them, not to perform them.

## Design Considerations

Use **802.1X/EAP** (prefer **EAP-TLS** with certificates) for corporate, **WPA3** with **SAE** and
**PMF** everywhere clients support it, and a **WIPS** to catch rogues and deauth attacks. Segment
SSIDs to VLANs. Protect the **RADIUS** infrastructure. Design assuming the air is hostile.

## Implementation and Automation

The labs reason about EAP selection, analyze a 4-way handshake capture, and check PMF — all
**defensive analysis**.

## Validation and Troubleshooting

Confirm the security model:

```text
802.1X/EAP: supplicant -> authenticator (AP) -> RADIUS. EAP-TLS (certs) / PEAP-TTLS (tunneled creds).
Keys: PMK -> 4-way handshake -> PTK (+ GTK). WPA3: SAE (anti-offline-attack) + mandatory PMF (802.11w).
Defense: WIPS (rogue/deauth detection), segmentation. CWSP = defensive.
```

Common pitfalls: **WPA2-PSK** for corporate (offline-crackable); and **no PMF**, leaving clients
open to deauth attacks.

## Security and Best Practices

Deploy **802.1X/EAP-TLS**, **WPA3-SAE**, and **PMF**; run a **WIPS**; and **segment** wireless from
sensitive networks. Protect RADIUS and certificates. Study attacks **to defend** — all analysis
here is on authorized networks only.

## Hands-On Lab

Security walkthroughs (defensive). **Shared prerequisites** — a shell with `python3`; Labs 5.2/5.4
use `tshark`/Wireshark on an **authorized** capture of your own lab WLAN. **Cost:** none.

### Lab 5.1 — Choose an EAP method

**Objective:** Match EAP to requirements.

```python
python3 - <<'PY'
eap={"EAP-TLS":"client + server certificates (strongest; needs PKI)",
     "PEAP-MSCHAPv2":"server cert + tunneled username/password",
     "EAP-TTLS":"server cert + flexible inner auth"}
for m,d in eap.items(): print(f"{m:16}: {d}")
print("recommend: EAP-TLS where PKI exists")
PY
```

**Expected result:** the EAP options with **EAP-TLS** recommended where PKI exists — strong
enterprise auth.

**Negative test:** use PSK for enterprise to "keep it simple"; **802.1X/EAP** gives per-user
security — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Analyze the 4-way handshake

**Objective:** Observe key establishment in a capture.

```bash
tshark -r wlan-auth.pcapng -Y "eapol" -T fields -e wlan.sa -e eapol.type -c 8 2>/dev/null \
  | head || echo "EAPOL frames = the 4-way handshake (messages 1-4) that derive the PTK/GTK"
```

**Expected result:** the **EAPOL** 4-way handshake messages — where per-session keys are derived.

**Negative test:** assume encryption "just happens"; the **4-way handshake** establishes keys —
analyze it to troubleshoot auth.

**Rollback:** none (read-only analysis of your own lab capture).

### Lab 5.3 — WPA3 SAE and PMF

**Objective:** Explain WPA3's improvements.

```python
python3 - <<'PY'
improvements={"SAE":"replaces WPA2-PSK handshake -> resists offline dictionary attacks",
              "PMF (802.11w)":"protects mgmt frames -> blocks deauth/disassoc attacks",
              "192-bit mode":"WPA3-Enterprise high-security suite"}
for k,v in improvements.items(): print(f"{k:16}: {v}")
PY
```

**Expected result:** WPA3's **SAE** and **PMF** improvements over WPA2 — stronger air security.

**Negative test:** rely on WPA2-PSK and disabled PMF; enable **WPA3-SAE + PMF** to close offline-
attack and deauth gaps.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Detect a deauth attack (defensive)

**Objective:** Recognize deauth flooding in a capture.

```bash
tshark -r wlan.pcapng -Y "wlan.fc.type_subtype==0x0c" -c 20 2>/dev/null | wc -l \
  || echo "subtype 0x0c = deauthentication; a flood of these signals a deauth attack (PMF mitigates)"
```

**Expected result:** a count of **deauthentication** frames — a spike indicates an attack that
**PMF** would mitigate.

**Negative test:** ignore deauth frames as normal; a **flood** is an attack signature — a **WIPS**
and **PMF** address it.

**Rollback:** none (read-only analysis).

### Lab 5.5 — WIPS and segmentation

**Objective:** Describe layered wireless defense.

```text
# WIPS detects rogue/evil-twin APs and wireless attacks; segmentation isolates SSIDs to VLANs so
#   a compromised guest network can't reach corporate resources.
"defense-in-depth: WPA3+PMF (air) + 802.1X (identity) + WIPS (detection) + VLAN segmentation"
```

**Expected result:** a **layered** wireless defense — encryption, identity, detection, and
segmentation.

**Negative test:** rely on encryption alone; add **WIPS + segmentation** for defense in depth.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CWSP covers enterprise Wi-Fi security: 802.1X/EAP with RADIUS, the 4-way handshake key hierarchy,
WPA3's SAE and mandatory PMF, and WIPS/segmentation defense — all studied defensively. Use
EAP-TLS, WPA3-SAE, and PMF, run a WIPS, and segment wireless.

- [ ] I can choose an appropriate EAP method.
- [ ] I can analyze a 4-way handshake capture.
- [ ] I can explain WPA3 SAE and PMF.
- [ ] I can recognize a deauth attack and layered defenses.
- [ ] I completed Labs 5.1–5.5 including each negative test.
