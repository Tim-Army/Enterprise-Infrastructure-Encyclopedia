# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability with a repeatable script.
- Prove that a flat network permits lateral movement an attacker would exploit.
- Frame the two legitimate east-west flows and the unwanted ones, so later policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what *before* any segmentation, and capture it as a script you can re-run after every policy change.

**Walkthrough**

**Step 1.** On `il-app01`, create a reachability probe covering every host-to-service pair that matters:

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

**Step 2.** Run the same probe from `il-win01` (PowerShell), which is the machine that will be "compromised" in Lab 5.3:

```powershell
"10.10.20.12:5432","10.10.20.11:80","10.10.30.50:502" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Expected result.** Every probe returns **REACH** from both hosts. The network is flat: any host can reach any service.

**Negative test.** There is nothing blocked to find yet — and that is the finding. A flat network has no negative result, which is precisely why it is dangerous.

**Rollback.** Keep `~/reach.sh`; it is your regression test for the rest of the lab.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the *only* two east-west flows the business needs, so every other flow is, by definition, a candidate for denial.

**Walkthrough**

**Step 1.** Record the specification:

| # | Source | Destination | Port | Purpose | Legitimate? |
|:--|:--|:--|:--|:--|:--|
| 1 | il-app01 | il-db01 | 5432 | App reads the database | **Yes** |
| 2 | il-win01 (HMI) | il-ot01 (PLC) | 502 | HMI supervises the PLC | **Yes** |
| 3 | il-win01 | il-db01 | 5432 | — | **No** (lateral movement) |
| 4 | il-app01 | il-ot01 | 502 | — | **No** |
| 5 | any | il-win01 | * | — | **No** by default |

**Expected result.** Two "yes" rows, everything else "no". This table is the policy you will implement in Chapters 06–08.

**Negative test.** Try to justify flow 3 ("maybe the HMI reports to the database"). It does not — the HMI's only job is polling the PLC. Every "convenient" allow you cannot tie to a real dependency is how estates stay flat. Keep flow 3 a "no".

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Demonstrate concretely that a compromised HMI can reach and read the crown-jewel database across the flat network.

**Walkthrough**

**Step 1.** Treat `il-win01` as compromised (an attacker has code execution on the HMI). From it, reach straight into the database that the HMI has no business touching:

```powershell
# From the "compromised" HMI - pivot to the database
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432
```

**Step 2.** If you want to make the theft tangible, install the PostgreSQL client for Windows (or use the Linux `il-app01` as a stand-in attacker) and read the table with the app credentials an attacker would have harvested:

```powershell
# Using psql.exe if installed; demonstrates data exfiltration from the HMI
$env:PGPASSWORD='LabAppPassw0rd!'
& psql -h 10.10.20.12 -U appuser -d illab -c "SELECT * FROM customers;"
```

**Expected result.** The HMI reads customer rows out of the database — a full lateral-movement-to-exfiltration chain that no rule currently stops. This is the attack the rest of the lab defeats.

**Negative test.** Re-run the app's own legitimate query from `il-app01` (`~/checkdb.sh` → 3). It also works. The network cannot tell the difference between the app and the attacker, because on a flat network there is no policy to tell them apart. Segmentation is what supplies that difference.

**Rollback.** Clear the credential from the Windows session: `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline.
- [ ] The two legitimate flows and the unwanted flows are written down.
- [ ] Lateral movement from the HMI to the database reproduced.
- [ ] You can state, in one sentence, what policy must achieve: permit flows 1 and 2, deny the rest.
