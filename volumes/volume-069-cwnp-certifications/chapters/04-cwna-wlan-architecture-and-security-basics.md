# Chapter 04: CWNA — WLAN Architecture and Security Basics

## Learning Objectives

- Explain WLAN architectures (autonomous, controller, cloud).
- Describe roaming within an ESS and its requirements.
- Configure the conceptual model of WPA2/WPA3 security.
- Relate power-save and QoS (WMM) to client experience.
- Complete a walkthrough for each WLAN architecture topic.

## Theory and Architecture

The second half of **CWNA** covers how WLANs are **built and secured**. Architectures range from
**autonomous APs** (each standalone) through **controller-based** (a WLC centrally manages APs and
often tunnels traffic) to **cloud-managed** (a cloud controller). Clients form a **BSS** with an AP
and roam across an **ESS** (one SSID) as they move — smooth roaming needs overlapping coverage,
consistent security, and fast-roaming mechanisms (802.11r/k/v). **Security basics**: **WPA2** and
the modern **WPA3** protect the air — **Personal** (a passphrase → PSK/SAE) or **Enterprise**
(802.1X/EAP to a RADIUS server, per-user credentials, covered deeply in CWSP). **QoS** via **WMM**
prioritizes voice/video, and **power-save** modes extend client battery. CWNA gives the whole
picture; CWSP, CWAP, and CWDP each go deep on security, analysis, and design.

## Design Considerations

Choose the **architecture** by scale and operations (cloud for distributed sites, controller for
large campuses). Design **overlapping coverage** for roaming and enable **fast roaming** (802.11r/
k/v) for voice. Use **WPA3** where clients support it, **Enterprise** (802.1X) for corporate.
Enable **WMM** for real-time traffic.

## Implementation and Automation

The labs reason about architecture choice, roaming, and the WPA2/WPA3 security model.

## Validation and Troubleshooting

Confirm the architecture model:

```text
Architectures: autonomous | controller (WLC) | cloud-managed. BSS -> ESS roaming (802.11r/k/v).
Security: WPA2/WPA3 Personal (PSK/SAE) or Enterprise (802.1X/EAP + RADIUS). QoS: WMM. Power-save.
```

Common pitfalls: **no coverage overlap** (roaming gaps/drops); and **WPA2-Personal** for corporate
where **Enterprise/802.1X** belongs.

## Security and Best Practices

Design **overlapping coverage** with **fast roaming**, use **WPA3** and **Enterprise 802.1X** for
corporate, and enable **WMM** for voice/video. Separate guest to its own SSID/VLAN. Plan for the
weakest clients. Deeper security is CWSP (next chapter).

## Hands-On Lab

WLAN architecture walkthroughs. **Shared prerequisites for Labs 4.1–4.4** — a shell with `python3`.
**Cost:** none.

### Lab 4.1 — Choose an architecture

**Objective:** Match architecture to requirements.

```python
python3 - <<'PY'
def choose(sites, aps, ops):
    if sites>20: return "cloud-managed (distributed sites, central ops)"
    if aps>200: return "controller-based (large campus)"
    return "autonomous or cloud (small)"
print(choose(50,300,"lean")); print(choose(1,400,"campus"))
PY
```

**Expected result:** architecture recommendations by scale — cloud for many sites, controller for
big campuses.

**Negative test:** deploy autonomous APs across 50 sites; that doesn't scale operationally — use
**cloud/controller** management.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Roaming requirements

**Objective:** Check readiness for smooth roaming.

```python
python3 - <<'PY'
def roam_ready(overlap_pct, same_security, fast_roam):
    return overlap_pct>=15 and same_security and fast_roam
print("ready:", roam_ready(20, True, True))
print("gap:", roam_ready(5, True, True))
PY
```

**Expected result:** roaming is ready with **coverage overlap + consistent security + fast
roaming**; a 5% overlap fails — roaming needs overlap.

**Negative test:** expect seamless voice roaming with cell-edge-only coverage; add **overlap and
802.11r/k/v**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — WPA2 vs WPA3 model

**Objective:** Choose the security mode.

```python
python3 - <<'PY'
modes={"Guest":"WPA3-Personal (SAE) or Passpoint","Corporate":"WPA3-Enterprise (802.1X/EAP)",
       "Legacy IoT":"WPA2-PSK (isolated VLAN)"}
for use,mode in modes.items(): print(f"{use:12}: {mode}")
PY
```

**Expected result:** the right **security mode per use case** — WPA3-Enterprise for corporate,
SAE for guest, isolated WPA2 for legacy.

**Negative test:** put corporate users on **WPA2-PSK**; use **Enterprise 802.1X** for per-user
security.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — WMM QoS

**Objective:** Prioritize real-time traffic.

```python
python3 - <<'PY'
wmm={"Voice (AC_VO)":1,"Video (AC_VI)":2,"Best Effort (AC_BE)":3,"Background (AC_BK)":4}
for ac,prio in sorted(wmm.items(), key=lambda x:x[1]): print(f"{prio}. {ac}")
PY
```

**Expected result:** the **WMM access categories** in priority order — voice first — for real-time
QoS.

**Negative test:** treat voice as best-effort; enable **WMM** so voice/video get priority.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CWNA's architecture half covers autonomous/controller/cloud WLANs, ESS roaming with 802.11r/k/v,
the WPA2/WPA3 Personal/Enterprise security model, and WMM QoS. Choose architecture by scale,
design overlap for roaming, use WPA3-Enterprise for corporate, and prioritize with WMM.

- [ ] I can choose a WLAN architecture by requirements.
- [ ] I can assess roaming readiness.
- [ ] I can select the WPA2/WPA3 mode per use case.
- [ ] I can order WMM access categories.
- [ ] I completed Labs 4.1–4.4 including each negative test.
