# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: EdgeIPS inline in front of a cell, StellarProtect on the host.
- Stand up the Track 2 estate: an operator, an attacker, a vulnerable PLC behind an inline filter, and an engineering host.
- Confirm the vulnerable PLC and the exploit before any protection exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | EdgeIPS/EdgeFire inline, StellarProtect agent | TXOne (commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `python3`, `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: inline EdgeIPS and StellarProtect (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** **EdgeIPS** is cabled **inline** as a transparent Layer 2 device in front of the OT cell — no IP addresses change, no re-subnetting — and it inspects and blocks OT traffic. **StellarProtect** is installed on the OT host and locks it to an application allowlist. Both report to a central console (StellarOne / EdgeOne).

**Expected result (design).** A transparent inline shield and a locked-down endpoint. Track 2 builds working versions of both.

**Rollback.** None (design).

### Exercise 2.2 — Track 2: build the estate and a vulnerable PLC

**Objective.** Create the operator, attacker, PLC, and engineering host, and put the PLC behind an inline filter.

**Track 2 — Walkthrough.**

The operator, attacker, and engineering host share an IT segment; the PLC sits in its own **cell** segment reached only through the host, which is where the inline device will be inserted:

```bash
sudo apt-get update -qq && sudo apt-get install -y python3 nftables iproute2 netcat-openbsd
sudo ip link add ot   type bridge; sudo ip addr add 10.90.1.1/24 dev ot;   sudo ip link set ot up
sudo ip link add cell type bridge; sudo ip addr add 10.90.2.1/24 dev cell; sudo ip link set cell up
mkns() { sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master $3 up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via ${2%.*}.1; }
mkns hmi 10.90.1.30 ot
mkns atk 10.90.1.66 ot
mkns ews 10.90.1.50 ot
mkns plc 10.90.2.40 cell
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

A vulnerable Modbus-ish PLC — a "read" is safe, but a request carrying the marker `EXPLOIT` triggers an unsafe action (the vulnerability). Save as `/usr/local/bin/vulnplc.py`:

```python
import socket, threading
STATE = {'safe': True}
def handle(c):
    d = c.recv(256)
    if b'EXPLOIT' in d:                 # the un-patchable vulnerability
        STATE['safe'] = False
        c.sendall(b'PLC-COMPROMISED\n')
    elif d[:4] == b'READ':
        c.sendall(b'VALUE=50\n')
    else:
        c.sendall(b'OK\n')
    c.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 502)); s.listen(5)
while True:
    conn, _ = s.accept(); threading.Thread(target=handle, args=(conn,)).start()
```

Start it and confirm reachability:

```bash
sudo chmod 644 /usr/local/bin/vulnplc.py
sudo ip netns exec plc bash -c 'nohup python3 /usr/local/bin/vulnplc.py >/tmp/vulnplc.log 2>&1 &'
sudo ip netns exec hmi bash -c 'printf "READ\n" | nc -w2 10.90.2.40 502'
```

**Expected result.**

```text
VALUE=50
```

**Negative test.** The PLC has no authentication and a real vulnerability — it cannot be fixed. The next exercise shows the exploit landing.

**Rollback.** Leave the PLC running.

### Exercise 2.3 — Land the exploit (pre-protection)

**Objective.** Show the attacker compromising the unpatchable PLC.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec atk bash -c 'printf "EXPLOIT payload\n" | nc -w2 10.90.2.40 502'
```

**Expected result.**

```text
PLC-COMPROMISED
```

The exploit lands directly on the vulnerable device — the exact scenario a transparent inline **virtual patch** will block without touching the PLC.

**Negative test.** You cannot fix the PLC (no patch exists); the only options are to shield it inline or isolate it. Chapter 04 shields it.

**Rollback.** Leave the PLC running.

## Summary and Completion Checklist

- [ ] Track 1 inline EdgeIPS + StellarProtect shape understood.
- [ ] Track 2: operator, attacker, vulnerable PLC, and engineering host built.
- [ ] The exploit shown landing on the unpatchable PLC.
- [ ] Ready to insert a transparent inline shield.
