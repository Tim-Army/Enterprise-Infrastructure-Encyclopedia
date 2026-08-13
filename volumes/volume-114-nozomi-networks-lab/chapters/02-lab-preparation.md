# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: a Guardian sensor on a SPAN feeding Vantage.
- Stand up the Track 2 estate: a minimal Modbus PLC, an operator, and a function-aware proxy.
- Confirm the operator can read the PLC before any segmentation exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Nozomi Guardian sensor on a SPAN, Vantage tenant | Nozomi (commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `python3`, `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: Guardian + Vantage (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** A **Guardian** sensor is placed on a **SPAN** of the OT segment; it passively dissects the industrial protocols, builds the network graph, and learns the process baseline. **Vantage** aggregates one or many Guardians, holds the alerts, and is where protocol-aware assertions and segmentation policy are managed.

**Expected result (design).** Guardian on a mirror, feeding Vantage. Track 2 builds a working protocol-aware enforcer to make the concepts concrete.

**Rollback.** None (design).

### Exercise 2.2 — Track 2: build the PLC, operator, and function-aware proxy

**Objective.** Create a minimal Modbus PLC and a proxy that can inspect the Modbus function code.

**Track 2 — Walkthrough.** Create the namespaces on one segment; the proxy runs on the host gateway and is the only thing allowed to reach the PLC:

```bash
sudo apt-get update -qq && sudo apt-get install -y python3 nftables iproute2 netcat-openbsd
sudo ip link add ot type bridge; sudo ip addr add 10.80.1.1/24 dev ot; sudo ip link set ot up
mkns() { sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master ot up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.80.1.1; }
mkns hmi 10.80.1.30
mkns plc 10.80.1.40
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

A minimal Modbus-TCP PLC (reads register 0; accepts writes) — save as `/usr/local/bin/mbserver.py`:

```python
import socket, struct, threading
REG = {0: 50}                                   # process variable, starts at 50
def handle(c):
    d = c.recv(256)
    if len(d) < 8: c.close(); return
    tid, pid, ln, uid, fc = struct.unpack('>HHHBB', d[:8])
    if fc in (3, 4):                            # read registers
        addr, qty = struct.unpack('>HH', d[8:12])
        vals = b''.join(struct.pack('>H', REG.get(addr+i, 0)) for i in range(qty))
        pdu = struct.pack('>BB', fc, len(vals)) + vals
    elif fc in (6, 16):                         # write register(s)
        addr, val = struct.unpack('>HH', d[8:12]); REG[addr] = val
        pdu = struct.pack('>B', fc) + d[8:12]
    else:
        pdu = struct.pack('>BB', fc | 0x80, 1)  # exception
    c.sendall(struct.pack('>HHHB', tid, pid, len(pdu)+1, uid) + pdu); c.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 502)); s.listen(5)
while True:
    conn, _ = s.accept(); threading.Thread(target=handle, args=(conn,)).start()
```

An operator client — save as `/usr/local/bin/mbclient.py`:

```python
import socket, struct, sys
op, host, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
if op == 'read':  pdu = struct.pack('>BHH', 3, 0, 1)
else:             pdu = struct.pack('>BHH', 6, 0, int(sys.argv[4]) if len(sys.argv) > 4 else 99)
frame = struct.pack('>HHHB', 1, 0, len(pdu)+1, 1) + pdu
s = socket.socket(); s.settimeout(3)
try:
    s.connect((host, port)); s.sendall(frame); r = s.recv(256)
    if len(r) < 8: print("NO-RESPONSE (denied?)")
    elif r[7] & 0x80: print("MODBUS-EXCEPTION")
    elif op == 'read': print("READ value=", struct.unpack('>H', r[9:11])[0])
    else: print("WRITE-ACK")
except Exception: print("NO-RESPONSE (denied?)")
```

Save both scripts to the paths shown, make them readable, and start the PLC:

```bash
sudo chmod 644 /usr/local/bin/mbserver.py /usr/local/bin/mbclient.py
sudo ip netns exec plc bash -c 'nohup python3 /usr/local/bin/mbserver.py >/tmp/mbserver.log 2>&1 &'
```

**Expected result.** The operator can read the PLC directly (no segmentation yet):

```bash
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read 10.80.1.40 502
READ value= 50
```

**Negative test.** A non-Modbus probe to 502 gets no valid Modbus reply — the port is Modbus-only, which is exactly what a protocol-aware control will enforce (an L4 firewall would happily allow any payload to 502).

**Rollback.** Leave the PLC running.

### Exercise 2.3 — Confirm a write also works (pre-segmentation)

**Objective.** Show that, unprotected, the operator can also *write* the PLC — the dangerous capability.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.40 502 99
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.40 502
```

**Expected result.**

```text
WRITE-ACK
READ value= 99
```

The operator changed a control value directly — the flow an L4 firewall cannot distinguish from a read, because both are "TCP to 502". Chapter 05 denies the write while keeping the read.

**Negative test.** Resetting the value needs another write; leave it at 99 for now (Chapter 06 uses the out-of-range value for anomaly detection).

**Rollback.** Leave the PLC running.

## Summary and Completion Checklist

- [ ] Track 1 Guardian/Vantage shape understood.
- [ ] Track 2: PLC, operator, and (to come) function-aware proxy scripted.
- [ ] Operator can read and write the PLC directly (pre-segmentation).
- [ ] The read-vs-write distinction an L4 firewall misses is clear.
