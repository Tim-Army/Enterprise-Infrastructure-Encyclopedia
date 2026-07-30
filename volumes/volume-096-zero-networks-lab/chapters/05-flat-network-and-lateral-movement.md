# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability with a repeatable script.
- Prove that a flat network permits lateral movement — including the wide-open administrative ports Zero Networks exists to close.
- Frame the legitimate and unwanted flows so later policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before any segmentation, including the privileged ports.

**Walkthrough**

**Step 1.** On `zn-app01`, create a reachability probe that also checks the administrative ports:

```bash
cat > ~/reach.sh <<'EOF'
#!/usr/bin/env bash
probe() { timeout 3 bash -c "echo > /dev/tcp/$1/$2" 2>/dev/null \
          && echo "REACH  $1:$2  ($3)" || echo "BLOCK  $1:$2  ($3)"; }
probe 10.10.20.12 5432 "app/hmi -> db"
probe 10.10.20.11 80   "-> app http"
probe 10.10.30.50 502  "-> plc modbus"
probe 10.10.20.12 22   "-> db SSH (privileged)"
probe 10.10.20.21 3389 "-> win RDP (privileged)"
EOF
chmod +x ~/reach.sh
~/reach.sh
```

**Step 2.** Run the same probe from `zn-win01` (PowerShell):

```powershell
"10.10.20.12:5432","10.10.20.11:80","10.10.30.50:502","10.10.20.12:22" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Expected result.** Every probe returns **REACH** — including SSH (22) and RDP (3389). The administrative surface is wide open to every host.

**Negative test.** There is nothing blocked to find, and the open privileged ports are the point: on a flat network any host can attempt RDP/SSH to any other, which is exactly the lateral-movement path Zero Networks closes with just-in-time MFA.

**Cleanup.** Keep `~/reach.sh` as your regression test.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the only east-west flows the business needs — and note that no host legitimately needs standing RDP/SSH to another.

**Walkthrough**

| # | Source | Destination | Port | Purpose | Legitimate? |
|:--|:--|:--|:--|:--|:--|
| 1 | zn-app01 | zn-db01 | 5432 | App reads the database | **Yes** |
| 2 | zn-win01 (HMI) | zn-ot01 (PLC) | 502 | HMI supervises the PLC | **Yes** |
| 3 | zn-win01 | zn-db01 | 5432 | — | **No** (lateral movement) |
| 4 | any | any | 22 / 3389 | Admin access | **Only just-in-time, after MFA** |
| 5 | any | zn-win01 | * | — | **No** by default |

**Expected result.** Two standing "yes" east-west flows; administrative access allowed only as a time-boxed, MFA-gated exception, never standing.

**Negative test.** Argue that "admins need SSH open to the servers." Standing administrative ports are the single most abused lateral-movement path; Zero Networks' answer is to keep them closed and open them just-in-time. Keep row 4 an exception, not a standing allow.

**Cleanup.** None.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show that a compromised HMI can reach the database and attempt administrative logons across the flat network.

**Walkthrough**

**Step 1.** Treat `zn-win01` as compromised. Reach the database directly:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432
```

**Step 2.** Attempt the administrative pivot every attacker tries — SSH to a server:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 22
```

**Step 3.** Make the data theft tangible:

```powershell
$env:PGPASSWORD='LabAppPassw0rd!'
& psql -h 10.10.20.12 -U appuser -d znlab -c "SELECT * FROM customers;"
```

**Expected result.** The HMI reaches the database (5432), can knock on SSH (22), and reads customer rows — the lateral-movement-and-privileged-access surface Zero Networks removes.

**Negative test.** Re-run the app's own query from `zn-app01` (`~/checkdb.sh` → 3); it works too. On a flat network nothing distinguishes the app from the attacker, and every server's admin port is reachable from every host. Segmentation plus just-in-time MFA supplies both missing controls.

**Cleanup.** `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline, including 22 and 3389.
- [ ] The legitimate flows and the "no standing admin access" rule are written down.
- [ ] Lateral movement and an administrative pivot attempt reproduced.
- [ ] You can state the goal: permit flows 1 and 2, deny the rest, and gate admin ports behind just-in-time MFA.
