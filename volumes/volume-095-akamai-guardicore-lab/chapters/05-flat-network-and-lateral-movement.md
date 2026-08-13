# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability with a repeatable script.
- Prove that a flat network permits lateral movement an attacker would exploit.
- Frame the legitimate and unwanted flows so later policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before any segmentation, and capture it as a re-runnable script.

**Walkthrough**

**Step 1.** On `gc-app01`, create a reachability probe:

```bash
cat > ~/reach.sh <<'EOF'
#!/usr/bin/env bash
probe() { timeout 3 bash -c "echo > /dev/tcp/$1/$2" 2>/dev/null \
          && echo "REACH  $1:$2  ($3)" || echo "BLOCK  $1:$2  ($3)"; }
probe 10.10.20.12 5432 "app/hmi -> db"
probe 10.10.20.11 80   "-> app http"
probe 10.10.30.50 502  "-> plc modbus"
EOF
chmod +x ~/reach.sh
~/reach.sh
```

**Step 2.** Run the same probe from `gc-win01` (PowerShell):

```powershell
"10.10.20.12:5432","10.10.20.11:80","10.10.30.50:502" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Expected result.** Every probe returns **REACH** from both hosts. The network is flat.

**Negative test.** Nothing is blocked to find — and that is the finding. A flat network has no negative result, which is why it is dangerous.

**Rollback.** Keep `~/reach.sh` as your regression test.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the only two east-west flows the business needs.

**Walkthrough**

| # | Source | Destination | Port | Purpose | Legitimate? |
|:--|:--|:--|:--|:--|:--|
| 1 | gc-app01 | gc-db01 | 5432 | App reads the database | **Yes** |
| 2 | gc-win01 (HMI) | gc-ot01 (PLC) | 502 | HMI supervises the PLC | **Yes** |
| 3 | gc-win01 | gc-db01 | 5432 | — | **No** (lateral movement) |
| 4 | gc-app01 | gc-ot01 | 502 | — | **No** |
| 5 | any | gc-win01 | * | — | **No** by default |

**Expected result.** Two "yes" rows; everything else "no". This is the policy for Chapters 06–08.

**Negative test.** Try to justify flow 3. The HMI's only job is polling the PLC; every "convenient" allow you cannot tie to a real dependency keeps estates flat. Keep flow 3 a "no".

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show that a compromised HMI can reach and read the crown-jewel database across the flat network.

**Walkthrough**

**Step 1.** Treat `gc-win01` as compromised. From it, reach the database it has no business touching:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432
```

**Step 2.** Make the theft tangible with the app credentials an attacker would harvest:

```powershell
$env:PGPASSWORD='LabAppPassw0rd!'
& psql -h 10.10.20.12 -U appuser -d gclab -c "SELECT * FROM customers;"
```

**Expected result.** The HMI reads customer rows — a full lateral-movement-to-exfiltration chain no rule currently stops.

**Negative test.** Re-run the app's own query from `gc-app01` (`~/checkdb.sh` → 3); it also works. On a flat network the network cannot tell the app from the attacker. Segmentation supplies that difference — and, as Chapter 06 shows, Guardicore's process-aware Reveal makes the difference visible even when the addresses look alike.

**Rollback.** `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline.
- [ ] The legitimate and unwanted flows are written down.
- [ ] Lateral movement from the HMI to the database reproduced.
- [ ] You can state the goal in one sentence: permit flows 1 and 2, deny the rest.
