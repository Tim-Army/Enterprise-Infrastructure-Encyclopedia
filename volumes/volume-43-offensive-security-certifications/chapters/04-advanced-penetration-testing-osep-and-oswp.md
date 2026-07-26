# Chapter 04: Advanced Penetration Testing — OSEP and OSWP

## Learning Objectives

- Explain the advanced pentest credentials: OSEP (PEN-300) and OSWP (PEN-210).
- Describe OSEP's evasion and breaching focus and OSWP's wireless focus.
- Understand advanced techniques well enough to detect and defend against them.
- Practice authorized-lab methodology and the defensive counterpart for each area.
- Complete per-topic walkthroughs for the OSEP and OSWP topic areas.

## Theory and Architecture

Two credentials sit above OSCP for specialized offensive depth:

- **OSEP (OffSec Experienced Penetration Tester, PEN-300)** — the advanced
  penetration-testing credential focused on **evasion and breaching defenses**:
  bypassing antivirus and endpoint detection, application whitelisting, and
  network filtering; advanced **Active Directory** and **Kerberos** attacks; and
  sophisticated post-exploitation and lateral movement. It is one of the three
  **OSCE³** credentials and does **not** expire.
- **OSWP (OffSec Wireless Professional, PEN-210)** — the wireless credential
  covering wireless reconnaissance and attacks against **WPA/WPA2** and **WPA
  Enterprise** networks, practiced against **your own** access points in an
  authorized lab.

Both go deeper than OSCP: OSEP into defeating modern defenses (understood here to
**build** those defenses), and OSWP into the wireless layer most engagements
touch.

## Design Considerations

**OSEP** is for red-teamers who must operate against **defended** environments;
its real value is a deep understanding of **how detections work**, which is
exactly what a blue team needs to improve them. Study it with a **detection-first
mindset**: for every evasion, ask what telemetry would still catch it. **OSWP** is
for anyone assessing **wireless** security; the same techniques inform hardening
(WPA3, strong PSKs, enterprise auth, rogue-AP detection). Practice wireless only
against **hardware you own**.

## Implementation and Automation

Because these areas are sensitive, the labs below stay at **methodology, concept,
and defense** — they do not provide operational evasion or wireless-cracking
payloads. Each pairs the offensive concept with the **detection or control** that
counters it, which is the durable, legitimate takeaway.

## Validation and Troubleshooting

Confirm the courses on offsec.com:

```text
offsec.com/courses:
  - PEN-300 -> OSEP (evasion, breaching defenses, advanced AD/Kerberos) — no expiry, part of OSCE3
  - PEN-210 -> OSWP (wireless: WPA/WPA2, WPA Enterprise) — your own APs only
```

Common pitfalls: pursuing OSEP without solid OSCP fundamentals; and practicing
**wireless attacks on networks you do not own** — OSWP practice must use your own
equipment in an authorized lab.

## Security and Best Practices

Treat evasion knowledge as **detection engineering**: the point is to make
defenses that survive it (EDR tuning, application control, network monitoring,
Kerberos hardening, honeytokens). For wireless, deploy **WPA3**, strong
passphrases or **enterprise (802.1X)** authentication, and **rogue-AP
detection**. Never operate outside authorization.

## References and Knowledge Checks

- offsec.com: *PEN-300 (OSEP)* and *PEN-210 (OSWP)* course pages and exam guides.

**Knowledge checks**

1. What is OSEP's focus, and which umbrella credential does it contribute to?
2. Why is a detection-first mindset the right way to study evasion?
3. What wireless controls counter the attacks OSWP teaches?

## Hands-On Lab

Per-topic walkthroughs — **concept and defense only; authorized labs and your own
hardware only.**

**Shared prerequisites** — a Kali shell with `python3`; for the wireless concept
lab, your **own** access point (no commands target third-party networks).
**Cost:** none.

### OSEP — Evasion and Breaching Defenses

### Lab 4.1 — OSEP: antivirus / EDR evasion (detection-first)

**Objective:** Understand evasion by enumerating what still detects it.

```bash
python3 - <<'PY'
evasion = {"Obfuscation/packing":"detected by: behavioral EDR, AMSI, memory scanning",
           "Living-off-the-land (LOLBins)":"detected by: command-line + parent-child process telemetry",
           "In-memory execution":"detected by: EDR memory/API hooks, ETW"}
for tech,detect in evasion.items(): print(f"{tech:28} -> {detect}")
PY
```

**Expected result:** evasion categories each mapped to the telemetry that still
catches them — OSEP knowledge framed as **detection engineering**.

**Negative test:** assume signature AV is the only control; modern **behavioral
EDR/AMSI/ETW** catch what signatures miss — defense is layered.

**Cleanup:** none.

### Lab 4.2 — OSEP: application whitelisting and its bypass classes (concept)

**Objective:** Reason about application control and how it is bypassed and
hardened.

```bash
python3 - <<'PY'
print("App control (e.g., WDAC/AppLocker): allow only approved binaries/publishers.")
print("Bypass classes (concept): trusted LOLBins, writable allowed paths, misconfigured rules.")
print("Harden: publisher rules > path rules, block known LOLBins, audit then enforce.")
PY
```

**Expected result:** how application whitelisting works, the bypass *classes*, and
the hardening — OSEP-level understanding aimed at stronger controls.

**Negative test:** allow-list by **path**; writable allowed paths are bypassable —
prefer publisher/hash rules.

**Cleanup:** none.

### Lab 4.3 — OSEP: advanced Active Directory and Kerberos (concept)

**Objective:** Map advanced AD attacks to their detections.

```bash
python3 - <<'PY'
attacks = {"Kerberoasting":"detect: TGS requests for many SPNs; harden: strong service-account pwds/gMSA",
           "Unconstrained delegation":"detect/audit delegation config; harden: remove/limit delegation",
           "DCSync":"detect: replication from non-DC; harden: restrict replication rights"}
for a,d in attacks.items(): print(f"{a:24} -> {d}")
PY
```

**Expected result:** advanced AD/Kerberos attacks each paired with detection and
hardening — the OSEP AD depth, oriented to defense.

**Negative test:** rely on password length alone against Kerberoasting; **gMSA**
and monitoring are the durable controls.

**Cleanup:** none.

### Lab 4.4 — OSEP: post-exploitation and lateral movement (concept)

**Objective:** Understand stealthy lateral movement and how it is caught.

```bash
python3 - <<'PY'
print("Lateral movement (concept): remote services (WMI/WinRM/SMB), token/credential reuse.")
print("Detect: unusual auth graphs, service creation, remote-exec telemetry, honeytokens.")
print("Harden: segmentation, LAPS, credential guard, tiered admin.")
PY
```

**Expected result:** lateral-movement techniques with their detections and
hardening — OSEP post-exploitation framed defensively.

**Negative test:** trust a flat, unmonitored network; **segmentation + telemetry**
are what stop and reveal lateral movement.

**Cleanup:** none.

### OSWP — Wireless

### Lab 4.5 — OSWP: wireless security models (concept, your own AP)

**Objective:** Compare wireless security modes and their weaknesses.

```bash
python3 - <<'PY'
modes = {"WEP":"broken — never use",
         "WPA2-PSK":"offline handshake capture -> dictionary attack if PSK weak",
         "WPA2-Enterprise (802.1X)":"per-user auth; watch for evil-twin/cred theft",
         "WPA3":"SAE resists offline dictionary attacks — preferred"}
for m,note in modes.items(): print(f"{m:26} -> {note}")
PY
```

**Expected result:** the wireless security modes and their weaknesses — OSWP's
core knowledge, used to choose **WPA3** and strong auth.

**Negative test:** run WPA2 with a short PSK; a captured handshake yields the key
offline — use a long passphrase or **WPA3/enterprise**.

**Cleanup:** none.

### Lab 4.6 — OSWP: your own wireless posture (authorized)

**Objective:** Assess the security mode of a network **you own**.

```bash
nmcli -t -f SSID,SECURITY dev wifi list 2>/dev/null | head \
  || echo "(list your OWN networks' security; confirm WPA2/WPA3 and no open/WEP SSIDs)"
echo "Only assess networks you own or are authorized to test."
```

**Expected result:** the security mode of networks in range (assess only **your
own**) — confirming WPA2/WPA3 and no weak/open SSIDs. **Defense:** WPA3, hidden
management, rogue-AP detection.

**Negative test:** capture or attack a neighbor's network; that is illegal — OSWP
practice uses **your own** access points only.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OSEP (PEN-300) and OSWP (PEN-210) add advanced offensive depth: OSEP in evasion,
breaching defenses, and advanced Active Directory/Kerberos (one of the three
OSCE³ credentials, no expiry), and OSWP in wireless security. This chapter treats
both **detection-first** — every technique paired with the telemetry and controls
that counter it — and restricts all practice to authorized labs and your own
hardware.

- [ ] I can describe OSEP's and OSWP's focus and OSEP's OSCE³ role.
- [ ] I can map evasion and AD attacks to their detections.
- [ ] I can compare wireless security modes and choose WPA3/enterprise.
- [ ] I only assess systems and networks I own or am authorized to test.
- [ ] I completed Labs 4.1–4.6 including each negative test.
