# Chapter 04: Virtual Patching

## Learning Objectives

- Arm a virtual-patch signature that blocks the exploit inline.
- Confirm the exploit is stopped while the PLC stays unpatched.
- Understand why virtual patching is the defining OT-IPS capability.

## Patch the network, not the device

The PLC cannot be fixed — no patch exists, and taking it offline is not an option. **Virtual patching** solves this by putting the fix in the **inline device**: an IPS signature recognizes the exploit and drops it before it reaches the vulnerable PLC. The device is unchanged; the attack is neutralized at the wire. This is the capability that lets OT run unpatchable equipment safely.

## Hands-On Lab

### Exercise 4.1 — Arm the virtual patch

**Objective.** Add a signature for the exploit and reload the inline inspector.

**Track 1 — Walkthrough.** In EdgeIPS you enable the virtual-patch signature (or an OT-specific filter) that matches the exploit for the vulnerable device; the device begins dropping matching traffic immediately, with no change to the PLC.

**Track 2 — Walkthrough.** Add the exploit signature the inline inspector already checks for:

```bash
sudo mkdir -p /etc/txone
echo 'EXPLOIT' | sudo tee /etc/txone/signatures >/dev/null
cat /etc/txone/signatures
```

The inspector loads signatures per connection, so the patch is live immediately — no restart, no PLC change.

**Expected result.** The signature file contains the exploit marker; the inline inspector will now drop any request containing it.

**Negative test.** A signature that is too broad (e.g., matching `READ`) would block legitimate traffic — virtual patches must be specific to the exploit. Keep it to `EXPLOIT`.

**Cleanup.** Keep the signature.

### Exercise 4.2 — The exploit is blocked; the PLC is untouched

**Objective.** Prove the attack is stopped inline while legitimate traffic still flows.

**Track 2 — Walkthrough.**

```bash
# exploit attempt is now dropped at the inline device
sudo ip netns exec atk bash -c 'printf "EXPLOIT payload\n" | nc -w2 10.90.2.40 502'; echo "(atk result above)"
# the inline log shows the virtual-patch drop
sudo grep -m1 "VIRTUAL-PATCH" /tmp/edgeips.log
# legitimate read still works
sudo ip netns exec hmi bash -c 'printf "READ\n" | nc -w2 10.90.2.40 502'
```

**Expected result.**

```text
(atk result above)                       # no PLC-COMPROMISED — dropped inline
VIRTUAL-PATCH DROP sig=EXPLOIT
VALUE=50
```

The exploit never reaches the PLC — it is dropped by the virtual patch — yet the PLC is entirely unchanged and legitimate reads still succeed.

**Negative test.** Confirm the PLC was never compromised this time by checking its log has no new compromise line since the patch:

```bash
sudo ip netns exec atk bash -c 'printf "EXPLOIT again\n" | nc -w2 10.90.2.40 502' >/dev/null
grep -c PLC-COMPROMISED /tmp/vulnplc.log
```

The compromise count does not increase — the attack is stopped before the device sees it.

**Cleanup.** Keep the virtual patch for the following chapters.

## Summary and Completion Checklist

- [ ] A specific virtual-patch signature armed on the inline device.
- [ ] The exploit dropped inline; the PLC never reached.
- [ ] Legitimate traffic unaffected; the PLC unpatched.
- [ ] Why virtual patching is the core OT-IPS capability understood.
