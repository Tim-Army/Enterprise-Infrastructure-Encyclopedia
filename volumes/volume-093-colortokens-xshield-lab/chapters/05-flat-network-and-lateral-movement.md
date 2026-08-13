# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Map what actually reaches what on a flat network.
- Establish the legitimate application and control flows.
- Reproduce lateral movement to document the blast radius microsegmentation must eliminate.

Before applying any control, prove the problem exists. Every exercise
here runs against the permissive baseline you just built. Keep the
output; Part E measures its success by reversing these results.

## Hands-On Lab

### Lab 5.1 — Map the flat network

**Objective.** Establish, with evidence, that any host on the Data
Center segment can reach every service on every other host — the
definition of a flat network.

**Walkthrough**

**Step 1.** On `ct-app01`, scan the Data Center segment as an attacker
who has just landed there would:

```text
nmap -sn 10.10.20.0/24

```

Expected — every live host discovered:

```text
Nmap scan report for 10.10.20.11   (ct-app01)
Nmap scan report for 10.10.20.12   (ct-db01)
Nmap scan report for 10.10.20.21   (ct-win01)
Nmap scan report for 10.10.20.254  (ct-gw)

```

**Step 2.** Service-scan the two most sensitive hosts:

```text
nmap -Pn -p 22,80,445,3389,5432 10.10.20.12 10.10.20.21

```

Expected — the database is wide open on the segment, and the Windows
host exposes SMB and RDP:

```text
Nmap scan report for 10.10.20.12
PORT     STATE  SERVICE
5432/tcp open   postgresql
22/tcp   open   ssh

Nmap scan report for 10.10.20.21
PORT     STATE  SERVICE
445/tcp  open   microsoft-ds
3389/tcp open   ms-wbt-server

```

**Step 3.** Build the reachability matrix that Part E will overturn.
Save it:

```bash
cat > ~/reach.sh <<'EOF'
#!/bin/bash
targets=("10.10.20.11:80" "10.10.20.12:5432" "10.10.20.21:445" "10.10.20.21:3389" "10.10.30.50:502")
echo "From $(hostname) @ $(date +%T)"
for t in "${targets[@]}"; do
  host="${t%:*}"; port="${t#*:}"
  if nc -z -w2 "$host" "$port" 2>/dev/null; then echo "  REACH  $t"; else echo "  BLOCK  $t"; fi
done
EOF
chmod +x ~/reach.sh
~/reach.sh

```

Expected from `ct-app01` on the flat network — **everything reachable,
including the OT PLC**:

```text
From ct-app01 @ ...
  REACH  10.10.20.11:80
  REACH  10.10.20.12:5432
  REACH  10.10.20.21:445
  REACH  10.10.20.21:3389
  REACH  10.10.30.50:502

```

**Expected result.** Documented proof that the web tier can reach the
database, the Windows host’s SMB and RDP, and the OT PLC’s Modbus port —
none of which it legitimately needs except the database.

**Negative test.** There is nothing to block yet — that is the finding.
A flat network has no negative test, which is precisely why it is
dangerous.

**Rollback.** Keep `~/reach.sh`; you will rerun it throughout Part E to
measure progress.

### Lab 5.2 — Establish the legitimate application flow

**Objective.** Record the one east-west flow that is *supposed* to
exist, so later policy permits it rather than breaking the application.

**Walkthrough**

**Step 1.** From `ct-app01`, connect to the database exactly as the
application would:

```text
PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d ctlab \
  -c "SELECT id, name FROM customers ORDER BY id;"

```

Expected:

```text
 id |   name
----+-----------
  1 | Acme Corp
  2 | Globex
  3 | Initech
(3 rows)

```

**Step 2.** Record the legitimate SCADA→PLC control flow. From
`ct-win01` PowerShell:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502

```

Expected: `TcpTestSucceeded : True`. This one is legitimate — the HMI
must talk to its PLC.

**Step 3.** Write down the two flows that must survive every policy you
author:

| Source | Destination | Service | Reason |
|:---|:---|:---|:---|
| ct-app01 (10.10.20.11) | ct-db01 (10.10.20.12) | TCP 5432 | App reads/writes its database |
| ct-win01 (10.10.20.21) | ct-ot01 (10.10.30.50) | TCP 502 | HMI polls its PLC |

**Expected result.** A definitive allow-list of two flows. In Xshield
terms this is your intended **policy** — everything else is noise to be
denied.

**Negative test.** Later, if a policy breaks either of these, you have
over-tightened. Knowing the allow-list in advance is what lets you tell
a real break from correct enforcement.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Simulate lateral movement (the attack)

**Objective.** Demonstrate the specific harm a flat network permits: a
compromised host with no relationship to the crown jewels reaches them
anyway.

**Scenario.** The Windows host `ct-win01` is the SCADA/HMI station. Its
only legitimate east-west relationship is polling the PLC. Imagine it is
phished. What can the attacker reach from it? On a flat network,
everything.

**Walkthrough**

**Step 1.** From `ct-win01` PowerShell — standing in for the attacker’s
foothold — sweep the Data Center:

```powershell
foreach ($p in 22,80,445,3389,5432) {
  $r = Test-NetConnection -ComputerName 10.10.20.12 -Port $p -WarningAction SilentlyContinue
  "{0,-6} {1}" -f $p, $(if ($r.TcpTestSucceeded) {"REACHABLE"} else {"blocked"})
}

```

Expected — the database is reachable from a host that should never touch
it:

```text
22     REACHABLE
80     blocked
445    blocked
3389   blocked
5432   REACHABLE

```

**Step 2.** Reach the OT cell from the “IT laptop” — a cross-segment
control-protocol reach that should be impossible:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502 -InformationLevel Detailed

```

Expected: `TcpTestSucceeded : True`.

**Step 3.** The full compromise. If the attacker has recovered the
application’s database credentials — from a config file, memory, or a
phished developer — the flat network lets them exfiltrate directly.
Install the `psql` client on `ct-win01` if you have not (Lab 4.4
Step 32), or run this equivalent from `ct-app01` to represent the
attacker having pivoted there. From a host with the client:

```text
PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d ctlab \
  -c "SELECT name, card_last4 FROM customers;"

```

Expected — the crown jewels, exfiltrated:

```text
   name    | card_last4
-----------+------------
 Acme Corp | 4242
 Globex    | 1881
 Initech   | 9003

```

**Step 4.** Document the blast radius. From the SCADA station, an
attacker reached: the database (port 5432, and its data), the database
host’s SSH, and the OT PLC’s control port. The only thing standing
between a phished HMI and the plant’s PLC was nothing at all.

**Expected result.** Concrete, reproduced evidence of lateral movement:
one compromised host, full reach to crown-jewel data and OT control.
This is the “before” picture microsegmentation exists to eliminate.

**Negative test.** This *is* the negative outcome. The remainder of the
lab turns every `REACHABLE` above — except the two legitimate flows from
D2 — into `blocked`, and you will rerun exactly these commands to prove
it.

**Rollback.** None. Leave the estate flat; Part E segments it.

## Summary and Completion Checklist

- [ ] Lab 5.1 complete, including its negative test.
- [ ] Lab 5.2 complete, including its negative test.
- [ ] Lab 5.3 complete, including its negative test.
