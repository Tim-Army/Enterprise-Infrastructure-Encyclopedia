# Chapter 03: Transparent Inline Deployment

## Learning Objectives

- Insert the inline device so all traffic to the PLC passes it — **without changing the PLC's IP**.
- Confirm legitimate traffic still flows transparently after insertion.
- Understand why transparent (bump-in-the-wire) placement is what makes OT insertion safe.

## Drop it in without re-addressing

The reason EdgeIPS can be deployed in a running plant is that it is **transparent**: it is cabled inline in front of a cell and inspects traffic **without any device changing its IP or the operator changing any configuration**. This chapter inserts the inline inspector on Track 2 so that traffic to the PLC (still `10.90.2.40`) is transparently intercepted and forwarded — no re-addressing, no client changes.

## Hands-On Lab

### Exercise 3.1 — Insert the inline inspector

**Objective.** Route all PLC-bound traffic through an inline inspector transparently.

**Track 1 — Walkthrough.** EdgeIPS is cabled between the operator network and the OT cell. Because it bridges at Layer 2, the PLC keeps its address and the operator keeps its configuration; the device simply inspects everything crossing it.

**Track 2 — Walkthrough.** Save the inline inspector as `/usr/local/bin/edgeips.py` (pass-through now; virtual-patch signatures load in Chapter 04):

```python
import socket, threading
PLC = ('10.90.2.40', 502)
def load_sigs():
    try:    return [l.strip().encode() for l in open('/etc/txone/signatures') if l.strip()]
    except FileNotFoundError: return []
def handle(c):
    d = c.recv(512)
    for sig in load_sigs():
        if sig and sig in d:
            print(f"VIRTUAL-PATCH DROP sig={sig.decode()}", flush=True); c.close(); return
    u = socket.socket(); u.settimeout(3)
    try:    u.connect(PLC); u.sendall(d); c.sendall(u.recv(512)); u.close()
    except Exception: pass
    c.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.90.1.1', 1502)); s.listen(5)
while True:
    conn, _ = s.accept(); threading.Thread(target=handle, args=(conn,)).start()
```

Start it and transparently redirect PLC-bound traffic into it with nftables (the client still targets `10.90.2.40` — no IP change):

```bash
sudo chmod 644 /usr/local/bin/edgeips.py
sudo bash -c 'nohup python3 /usr/local/bin/edgeips.py >/tmp/edgeips.log 2>&1 &'
sudo nft add table ip txone
sudo nft add chain ip txone prerouting '{ type nat hook prerouting priority -100 ; }'
sudo nft add rule ip txone prerouting ip daddr 10.90.2.40 tcp dport 502 dnat to 10.90.1.1:1502
```

**Expected result.** The operator reaches the PLC exactly as before — same IP, same command — but the traffic now crosses the inspector:

```bash
sudo ip netns exec hmi bash -c 'printf "READ\n" | nc -w2 10.90.2.40 502'
VALUE=50
```

**Negative test.** The operator's command did not change (`10.90.2.40:502`) — proof the insertion is transparent. A device that required re-addressing the PLC could not be inserted into a live plant.

**Rollback.** Keep the inspector; Chapter 04 adds the virtual patch.

### Exercise 3.2 — The exploit still lands (no signature yet)

**Objective.** Show that inserting the device is not enough — it must inspect for the exploit.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec atk bash -c 'printf "EXPLOIT payload\n" | nc -w2 10.90.2.40 502'
```

**Expected result.**

```text
PLC-COMPROMISED
```

The device is inline but is still passing everything — the exploit reaches the PLC. Insertion is the prerequisite; the **virtual patch** (Chapter 04) is what blocks the attack.

**Negative test.** Assume being inline is protection. It is only opportunity — without a signature or policy, an inline device that passes traffic protects nothing. Chapter 04 arms it.

**Rollback.** Keep the inline inspector for Chapter 04.

## Summary and Completion Checklist

- [ ] Inline inspector inserted; PLC keeps its IP (transparent).
- [ ] Legitimate traffic still flows to the same address.
- [ ] The exploit still lands (no signature yet) — insertion alone is not protection.
- [ ] Ready to arm the virtual patch.
