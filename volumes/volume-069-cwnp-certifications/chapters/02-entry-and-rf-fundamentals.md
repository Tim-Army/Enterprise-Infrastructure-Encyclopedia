# Chapter 02: Entry Level and RF Fundamentals

## Learning Objectives

- Explain the entry-level certifications (CWSS, CWTS).
- Convert between dBm and milliwatts and reason in decibels.
- Calculate free-space path loss and a link budget.
- Compute EIRP from transmit power, cable loss, and antenna gain.
- Complete a walkthrough for each RF fundamentals topic.

## Theory and Architecture

Before any 802.11 detail, wireless rests on **radio-frequency (RF) math**, and the entry-level
**CWSS** (Sales Specialist) and **CWTS** (Technology Specialist) plus the start of CWNA build that
base. RF power is measured in **dBm** (decibels relative to 1 mW) because signals span huge
dynamic ranges; the **rules of 10s and 3s** (+10 dB = ×10 power, +3 dB ≈ ×2) let you do link math
in your head. **Free-space path loss (FSPL)** quantifies how signal weakens with distance and
frequency. A **link budget** adds transmit power and gains and subtracts losses to predict the
received signal, which must exceed the receiver's sensitivity (with margin) and the noise floor
(**SNR**). **EIRP** (Effective Isotropic Radiated Power) — transmit power minus cable loss plus
antenna gain — is what regulators cap and what actually radiates. These fundamentals decide
whether a link works at all.

## Design Considerations

Design to a **link budget** with **margin** above receiver sensitivity and enough **SNR** for the
target data rate. Respect **EIRP** regulatory limits per band. Remember FSPL rises with
**frequency** — 6 GHz (Wi-Fi 6E) attenuates more than 2.4 GHz, affecting range. Antenna gain
trades coverage shape for reach.

## Implementation and Automation

The labs convert dBm/mW, compute FSPL, build a link budget, and calculate EIRP.

## Validation and Troubleshooting

Confirm the RF model:

```text
dBm = 10*log10(mW). Rules: +10dB=x10, +3dB~x2 power. FSPL(dB)=20log10(d)+20log10(f)+const.
Link budget: Rx = Tx + gains - losses; need Rx > sensitivity (+ margin) and adequate SNR.
EIRP = Tx power - cable loss + antenna gain (regulatory cap per band).
```

Common pitfalls: adding **milliwatts** instead of working in **dB**; and ignoring **EIRP** limits.

## Security and Best Practices

Design with **margin** (don't run at the edge of sensitivity), respect **regulatory EIRP**, and
account for **noise/SNR**, not just signal. Higher bands (6 GHz) need more power budget for the
same range. Sound RF math prevents most "mysterious" Wi-Fi problems.

## Hands-On Lab

RF fundamentals walkthroughs. **Shared prerequisites for Labs 2.1–2.4** — a shell with `python3`.
**Cost:** none.

### Lab 2.1 — dBm and milliwatts

**Objective:** Convert power units and apply the rules.

```python
python3 - <<'PY'
import math
def dbm_to_mw(dbm): return 10**(dbm/10)
def mw_to_dbm(mw): return 10*math.log10(mw)
for dbm in [0,20,23,30]: print(f"{dbm} dBm = {dbm_to_mw(dbm):.1f} mW")
print("100 mW =", round(mw_to_dbm(100),1), "dBm")
PY
```

**Expected result:** 0 dBm=1 mW, 20 dBm=100 mW, 30 dBm=1000 mW — the dBm/mW relationship.

**Negative test:** add 20 dBm + 20 dBm and expect 40 dBm of power; **dB adds as ratios** — 20+20
dBm is not double, it's ×100 each; sum powers in mW.

**Cleanup:** none.

### Lab 2.2 — Free-space path loss

**Objective:** Compute FSPL for a link.

```python
python3 - <<'PY'
import math
def fspl_db(dist_m, freq_mhz): return 20*math.log10(dist_m)+20*math.log10(freq_mhz)-27.55
for f in [2400,5200,6000]:
    print(f"FSPL @100m, {f} MHz = {fspl_db(100,f):.1f} dB")
PY
```

**Expected result:** FSPL rising with **frequency** (6 GHz > 5 GHz > 2.4 GHz at the same distance)
— why higher bands have shorter range.

**Negative test:** assume 6 GHz reaches as far as 2.4 GHz at equal power; **higher frequency = more
path loss** — plan for it.

**Cleanup:** none.

### Lab 2.3 — Link budget

**Objective:** Predict received signal and margin.

```python
python3 - <<'PY'
import math
tx_dbm=20; tx_ant=6; rx_ant=6; fspl=100.0; sensitivity=-82; margin_target=15
rx = tx_dbm + tx_ant + rx_ant - fspl
print(f"Rx signal = {rx:.1f} dBm; sensitivity {sensitivity} dBm; margin {rx-sensitivity:.1f} dB")
print("link OK" if (rx-sensitivity)>=margin_target else "insufficient margin")
PY
```

**Expected result:** a received level and **margin** vs sensitivity — a pass/fail link prediction.

**Negative test:** deploy a link with **0 dB margin**; real environments need **fade margin** —
design headroom.

**Cleanup:** none.

### Lab 2.4 — EIRP

**Objective:** Compute radiated power against a regulatory cap.

```python
python3 - <<'PY'
tx_dbm=23; cable_loss=2; ant_gain=8; eirp = tx_dbm - cable_loss + ant_gain
cap=36  # example regulatory EIRP cap (dBm)
print(f"EIRP = {eirp} dBm (cap {cap} dBm) ->", "OK" if eirp<=cap else "OVER LIMIT")
PY
```

**Expected result:** **EIRP = 29 dBm**, within the example cap — compliant radiated power.

**Negative test:** add a high-gain antenna pushing EIRP over the **regulatory cap**; reduce Tx or
gain — stay legal.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The entry level and RF fundamentals cover dBm/decibel math, free-space path loss, link budgets
with margin, and EIRP against regulatory caps — the physics every wireless design obeys. Work in
dB, budget with margin, mind that higher bands lose more, and respect EIRP limits.

- [ ] I can convert dBm and milliwatts and apply the rules of 10s/3s.
- [ ] I can compute free-space path loss.
- [ ] I can build a link budget with margin.
- [ ] I can calculate EIRP against a cap.
- [ ] I completed Labs 2.1–2.4 including each negative test.
