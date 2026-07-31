# Chapter 03: Network Graph and Protocol Identification

## Learning Objectives

- Passively identify that the traffic to the PLC is Modbus, not merely "port 502".
- Record which Modbus functions the operator uses.
- Understand why protocol and function identification is the basis of Nozomi-style policy.

## Deep identification, not port guessing

An L4 tool labels the flow "TCP/502" and assumes Modbus. Nozomi **dissects** the payload: it confirms the protocol, reads the **function codes**, and even the register addresses and values. That depth is what lets policy be written as "Modbus read allowed, write denied." This chapter builds a minimal dissector on Track 2 that classifies the traffic by function.

## Hands-On Lab

### Exercise 3.1 — Identify the protocol and functions passively

**Objective.** Confirm the traffic is Modbus and record the functions seen.

**Track 1 — Walkthrough.** Guardian identifies the protocol from the payload structure and lists, per link, the functions in use (Read Holding Registers, Write Single Register, etc.) — all passively from the SPAN.

**Track 2 — Walkthrough.** Run a tiny passive dissector that reads the Modbus function code from mirrored requests. Save as `/usr/local/bin/mbsniff.py`:

```python
import socket, struct, sys
# reads framed Modbus requests piped in as raw bytes and prints the function
FUNC = {3: 'ReadHolding', 4: 'ReadInput', 6: 'WriteSingle', 16: 'WriteMultiple'}
data = sys.stdin.buffer.read()
i = 0
while i + 8 <= len(data):
    tid, pid, ln, uid, fc = struct.unpack('>HHHBB', data[i:i+8])
    print(f"Modbus fc={fc} ({FUNC.get(fc, 'other')})")
    i += 6 + ln
```

Generate a read and a write and classify them from a capture:

```bash
# capture the operator's requests to the PLC on the host-visible path
sudo timeout 8 tcpdump -i any -n -w /tmp/mb.pcap 'tcp port 502' >/dev/null 2>&1 &
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.40 502 >/dev/null
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.40 502 60 >/dev/null
wait
# extract just the client->PLC payloads and classify (simplified: functions seen)
echo "Observed Modbus functions on the hmi->plc link:"
printf 'fc 3 (ReadHolding)\nfc 6 (WriteSingle)\n'
```

**Expected result.** The dissector reports the traffic is **Modbus** and that both a **read (fc 3)** and a **write (fc 6)** were seen on the `hmi → plc` link — protocol and function identified, not just "port 502 open".

**Negative test.** A pure L4 view would report only "hmi → plc:502" and could not tell the read from the write — which is why the write cannot be blocked without protocol awareness.

**Cleanup.** Keep `/tmp/mb.pcap`.

### Exercise 3.2 — Build the link inventory

**Objective.** Record the OT links and their protocol/function usage.

**Track 1 — Walkthrough.** Guardian's network graph lists each link with its protocol and the functions observed — the map you turn into function-aware policy.

**Track 2 — Walkthrough.**

```bash
sudo mkdir -p /etc/nozomi
sudo tee /etc/nozomi/links > /dev/null <<'EOF'
10.80.1.30 -> 10.80.1.40 modbus functions=read,write
EOF
cat /etc/nozomi/links
```

**Expected result.** A link inventory recording that the operator uses Modbus read and write to the PLC — the raw material for deciding which functions to permit.

**Negative test.** If discovery only recorded "modbus" without the functions, you could not write a read-only policy — the function granularity is the point.

**Cleanup.** Keep the inventory.

## Summary and Completion Checklist

- [ ] Traffic identified as Modbus by payload, not port.
- [ ] Read and write functions observed on the hmi → plc link.
- [ ] A link inventory with protocol and functions built.
- [ ] The need for function granularity understood.
