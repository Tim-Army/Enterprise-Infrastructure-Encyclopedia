# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability with a repeatable script.
- Prove that a flat network permits lateral movement.
- Frame the legitimate flows so the discovered policy has a specification to check against.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before any segmentation.

**Walkthrough**

**Step 1.** On `cw-app01`, create a reachability probe:

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

**Step 2.** Run the same probe from `cw-win01` (PowerShell):

```powershell
"10.10.20.12:5432","10.10.20.11:80","10.10.30.50:502" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Expected result.** Every probe returns **REACH**. The network is flat.

**Negative test.** Nothing is blocked to find — the finding is that any host can reach any service.

**Cleanup.** Keep `~/reach.sh` as your regression test.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the only two east-west flows the business needs — the ground truth you will check the *discovered* policy against in Chapter 06.

**Walkthrough**

| # | Source | Destination | Port | Purpose | Legitimate? |
|:--|:--|:--|:--|:--|:--|
| 1 | cw-app01 | cw-db01 | 5432 | App reads the database | **Yes** |
| 2 | cw-win01 (HMI) | cw-ot01 (PLC) | 502 | HMI supervises the PLC | **Yes** |
| 3 | cw-win01 | cw-db01 | 5432 | — | **No** (lateral movement) |
| 4 | cw-app01 | cw-ot01 | 502 | — | **No** |
| 5 | any | cw-win01 | * | — | **No** by default |

**Expected result.** Two "yes" flows; everything else "no". Secure Workload will *discover* this from telemetry — but only if the telemetry window sees clean traffic, which is why you keep this ground truth for comparison.

**Negative test.** Try to justify flow 3. The HMI's only job is polling the PLC; discovery run over traffic that includes the attack would learn flow 3 as normal. Keep flow 3 a "no" and review what discovery proposes.

**Cleanup.** None.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show that a compromised HMI can reach and read the crown-jewel database.

**Walkthrough**

**Step 1.** Treat `cw-win01` as compromised. Reach the database directly:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432
```

**Step 2.** Make the theft tangible with harvested app credentials:

```powershell
$env:PGPASSWORD='LabAppPassw0rd!'
& psql -h 10.10.20.12 -U appuser -d cwlab -c "SELECT * FROM customers;"
```

**Expected result.** The HMI reads customer rows — a full lateral-movement-to-exfiltration chain no rule currently stops.

**Negative test.** Re-run the app's own query from `cw-app01` (`~/checkdb.sh` → 3); it works too. On a flat network nothing distinguishes the app from the attacker. Discovered, telemetry-driven policy supplies the difference.

**Cleanup.** `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline.
- [ ] The two legitimate flows recorded as ground truth for the discovery step.
- [ ] Lateral movement from the HMI to the database reproduced.
- [ ] You can state the goal: discover, then enforce, permit flows 1 and 2 and deny the rest.
