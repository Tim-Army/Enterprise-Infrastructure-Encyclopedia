# Chapter 05: Function-Aware Segmentation

## Learning Objectives

- Remove the direct path to the PLC so all Modbus passes the enforcer.
- Deploy a function-aware proxy that permits Modbus reads and denies writes and non-Modbus.
- Prove reads pass and writes are blocked at the function level.

## Enforcing by function, not by port

The policy from Chapter 04 permits Modbus **reads** and denies **writes** — a distinction that lives inside the Modbus payload, not in the TCP header. This chapter isolates the PLC behind a **function-aware proxy** (standing in for a Nozomi-integrated enforcer or an OT-aware IPS) that parses the function code and applies the policy. On Track 2 the proxy is the concrete enforcer; in a real Nozomi deployment the assertion is pushed to an integrated OT firewall/IPS.

## Hands-On Lab

### Exercise 5.1 — Deploy the function-aware proxy and isolate the PLC

**Objective.** Make the PLC reachable only via the proxy, which enforces the function policy.

**Track 1 — Walkthrough.** Nozomi identifies the disallowed function and, via integration with an OT-aware enforcer (a next-gen OT firewall or IPS), the write is dropped while reads pass — enforcement at the protocol layer.

**Track 2 — Walkthrough.** Save the proxy as `/usr/local/bin/mbproxy.py`:

```python
import socket, struct, threading
ALLOW_FC = {3, 4}                 # reads only
LO, HI = 20, 80                   # learned range for register 0
PLC = ('10.80.1.40', 502)
def handle(c):
    req = c.recv(256)
    if len(req) < 8: c.close(); return
    fc = req[7]
    if fc not in ALLOW_FC:                       # deny writes / non-read functions
        print(f"DENY fc={fc} (write/non-read blocked)", flush=True); c.close(); return
    u = socket.socket(); u.settimeout(3)
    try:
        u.connect(PLC); u.sendall(req); resp = u.recv(256)
    except Exception:
        c.close(); return
    u.close()
    if fc in (3, 4) and len(resp) >= 11:          # behavioral check on the value
        val = struct.unpack('>H', resp[9:11])[0]
        if not (LO <= val <= HI):
            print(f"ANOMALY value={val} out of [{LO},{HI}]", flush=True)
    c.sendall(resp); c.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.80.1.1', 1502)); s.listen(5)
while True:
    conn, _ = s.accept(); threading.Thread(target=handle, args=(conn,)).start()
```

Start the proxy on the host and isolate the PLC so only the proxy may reach 502:

```bash
sudo chmod 644 /usr/local/bin/mbproxy.py
sudo bash -c 'nohup python3 /usr/local/bin/mbproxy.py >/tmp/mbproxy.log 2>&1 &'
sudo ip netns exec plc nft -f - <<'EOF'
table inet ot { chain input { type filter hook input priority 0 ; policy drop ;
  ct state established,related accept
  iif "lo" accept
  ip saddr 10.80.1.1 tcp dport 502 accept
} }
EOF
```

**Expected result.** The PLC now answers only the proxy; the operator must go through `10.80.1.1:1502`.

**Negative test.** Direct `hmi → plc:502` now fails (isolated), so a rogue write cannot bypass the function check by going straight to the PLC:

```bash
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.40 502 10
NO-RESPONSE (denied?)
```

**Cleanup.** Keep the proxy and isolation.

### Exercise 5.2 — Reads pass, writes are denied

**Objective.** Prove the function-level policy through the proxy.

**Track 2 — Walkthrough.** The operator now uses the proxy:

```bash
# read is permitted
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.1 1502
# write is denied at the function level
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.1 1502 30
# proxy log shows the denied write
sudo grep -m1 DENY /tmp/mbproxy.log
```

**Expected result.**

```text
READ value= 250
NO-RESPONSE (denied?)
DENY fc=6 (write/non-read blocked)
```

The read passes; the write is blocked because its Modbus function code is not permitted — segmentation by function, which no L4 rule can do. (The read shows 250, the out-of-range value from Chapter 04 — Chapter 06 flags that.)

**Negative test.** Send a non-Modbus payload through the proxy — it has no allowed function code and is dropped:

```bash
sudo ip netns exec hmi bash -c 'printf "GET / HTTP/1.0\r\n\r\n" | nc -w2 10.80.1.1 1502'; echo "(dropped: not Modbus read)"
```

**Cleanup.** Keep the enforcement for Chapter 06.

## Summary and Completion Checklist

- [ ] PLC isolated so all Modbus passes the proxy.
- [ ] Reads permitted; writes denied at the function level.
- [ ] Non-Modbus dropped.
- [ ] Function-aware segmentation demonstrated beyond L4.
