# Chapter 06: MSS Macro-Segmentation — Firewall Redirect

## Learning Objectives

- Redirect an inter-group flow through a firewall without re-cabling endpoints.
- Confirm the redirected flow is inspected while other flows are not.
- Understand when to use macro (redirect) versus micro (group permit/deny).

## Segment by steering, not just by dropping

MSS-Group permits or denies group flows in the fabric. **MSS macro-segmentation** adds a third option: **redirect** a flow through an inserted **firewall** for deeper inspection, then return it — so an existing firewall protects the flow without any endpoint moving or re-addressing. This chapter redirects `SG-Web → SG-DB` through the firewall while leaving `SG-Mgmt → SG-OT` enforced directly by group policy.

## Hands-On Lab

### Exercise 6.1 — Insert the firewall and redirect the flow

**Objective.** Steer `SG-Web → SG-DB:5432` through the firewall namespace.

**Track 1 — Walkthrough.** In CloudVision you mark the `SG-Web → SG-DB` policy for **redirect** to the attached firewall; the switches steer that flow to the firewall and back, transparently to the endpoints.

**Track 2 — Walkthrough.** Run an inspecting proxy in the firewall namespace and redirect the web→db flow to it. Save the firewall as `/usr/local/bin/mssfw.py`:

```python
import socket, threading
DB = ('10.120.2.20', 5432)
def handle(c):
    d = c.recv(512)
    if b'DROP TABLE' in d or b'EXPLOIT' in d:            # inspection: block a bad payload
        print("FW-DROP malicious payload", flush=True); c.close(); return
    u = socket.socket(); u.settimeout(3)
    try: u.connect(DB); u.sendall(d); c.sendall(u.recv(512)); u.close()
    except Exception: pass
    c.close()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.120.9.90', 15432)); s.listen(5)
while True:
    conn, _ = s.accept(); threading.Thread(target=handle, args=(conn,)).start()
```

Start it and redirect the group flow to it (replacing the direct SG-Web→SG-DB accept):

```bash
sudo chmod 644 /usr/local/bin/mssfw.py
sudo ip netns exec fw bash -c 'nohup python3 /usr/local/bin/mssfw.py >/tmp/mssfw.log 2>&1 &'
# redirect SG-Web -> SG-DB:5432 to the firewall (MSS macro)
sudo nft add chain ip mssnat prerouting '{ type nat hook prerouting priority -100 ; }' 2>/dev/null || \
  { sudo nft add table ip mssnat; sudo nft add chain ip mssnat prerouting '{ type nat hook prerouting priority -100 ; }'; }
sudo nft add rule ip mssnat prerouting ip saddr 10.120.1.10 ip daddr 10.120.2.20 tcp dport 5432 dnat to 10.120.9.90:15432
# allow web -> firewall and firewall -> db in the group chain
sudo nft add rule inet mss forward ip saddr 10.120.1.10 ip daddr 10.120.9.90 tcp dport 15432 accept
sudo nft add rule inet mss forward ip saddr 10.120.9.90 ip daddr 10.120.2.20 tcp dport 5432 accept
```

**Expected result.** `SG-Web → SG-DB` now traverses the firewall; a clean request still works:

```bash
sudo ip netns exec web bash -c 'printf "SELECT 1\n" | nc -w2 10.120.2.20 5432 && echo "web->db via firewall OK"'
```

**Negative test.** A malicious payload on the same flow is now dropped by the inserted firewall — inspection the direct group permit could not do:

```bash
sudo ip netns exec web bash -c 'printf "DROP TABLE users\n" | nc -w2 10.120.2.20 5432'; sudo grep -m1 FW-DROP /tmp/mssfw.log
```

**Cleanup.** Keep the redirect.

### Exercise 6.2 — Other flows are not redirected

**Objective.** Confirm only the marked flow traverses the firewall.

**Track 2 — Walkthrough.**

```bash
# SG-Mgmt -> SG-OT is enforced directly by group policy, not redirected
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.4.40 502 && echo "hmi->plc OPEN (direct group policy)"'
# the firewall only saw the web->db flow
sudo grep -c . /tmp/mssfw.log
```

**Expected result.** `hmi → plc` works via direct group policy (no firewall in its path), and the firewall log shows only web→db activity — macro redirect is per-flow, applied where inspection is wanted.

**Negative test.** Redirecting *every* flow through one firewall would make it a bottleneck; MSS macro is used selectively, with MSS-Group handling the bulk at line rate.

**Cleanup.** Keep both policies for verification.

## Summary and Completion Checklist

- [ ] The SG-Web→SG-DB flow redirected through the firewall (no endpoint change).
- [ ] A malicious payload dropped by the inserted firewall.
- [ ] SG-Mgmt→SG-OT enforced directly by group policy, not redirected.
- [ ] Macro (redirect) vs micro (group permit/deny) understood.
