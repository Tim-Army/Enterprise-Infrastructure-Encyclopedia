# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full matrix: legitimate traffic passes; exploit, untrusted source, dangerous command, and malware are all blocked.
- Read the inline and endpoint logs as one picture.
- Confirm each control is independent and layered.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
# A: legitimate operator read (allowed)
sudo ip netns exec hmi bash -c 'printf "READ\n"    | nc -w2 10.90.2.40 502'
# B: exploit from attacker (virtual patch drops it, and trust list drops the source)
sudo ip netns exec atk bash -c 'printf "EXPLOIT\n" | nc -w2 10.90.2.40 502'; echo "(B above)"
# C: dangerous command from trusted operator (command filter drops it)
sudo ip netns exec hmi bash -c 'printf "STOP\n"    | nc -w2 10.90.2.40 502'; echo "(C above)"
# D: unapproved binary on the EWS (endpoint lockdown blocks it)
sudo ip netns exec ews /usr/local/bin/stellar-run /usr/local/bin/evil-tool
```

**Expected result.**

```text
VALUE=50                                 (A: allowed)
(B above)                                (B: no PLC-COMPROMISED — dropped)
(C above)                                (C: STOP dropped)
StellarProtect: BLOCKED (not allowlisted) (D: malware blocked)
```

Only the legitimate operator read succeeds; the exploit, the untrusted source, the dangerous command, and the malware are each blocked by a different control.

**Negative test.** Disable one control (e.g., clear the trust-list rule) and confirm the *others* still hold — a clean read from the attacker would now pass the source check but an `EXPLOIT` still hits the virtual patch. Layered controls fail independently, not all at once. Restore the rule after.

**Rollback.** Restore any disabled control.

### Exercise 7.2 — One picture from inline and endpoint logs

**Objective.** Correlate network and host events.

**Track 2 — Walkthrough.**

```bash
echo "== inline (EdgeIPS) =="; sudo grep -E "VIRTUAL-PATCH|UNTRUSTED" /tmp/edgeips.log | tail -3
echo "== endpoint (StellarProtect) =="; journalctl -t stellar --no-pager | tail -2
```

**Expected result.** The inline log shows virtual-patch drops and untrusted-source drops; the endpoint log shows blocked binaries — network and host protection, visible together, which is the combined coverage TXOne provides.

**Negative test.** Relying on the network log alone would miss the blocked malware on the EWS; relying on the endpoint alone would miss the exploit on the wire. Both logs are needed for the full story.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.3 — The PLC stayed unpatched throughout

**Objective.** Confirm protection did not require touching the vulnerable device.

**Track 2 — Walkthrough.**

```bash
echo "PLC compromises recorded:"; grep -c PLC-COMPROMISED /tmp/vulnplc.log
echo "(the one from Chapter 02, before protection — none since)"
```

**Expected result.** Only the pre-protection compromise from Chapter 02 is recorded; none since the virtual patch — the vulnerable device was protected **without ever being modified**, the entire point of the approach.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Legitimate read allowed; exploit, untrusted source, dangerous command, and malware blocked.
- [ ] Inline and endpoint logs correlated.
- [ ] Controls confirmed independent and layered.
- [ ] The PLC protected without being patched.
