# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability with a repeatable script.
- Prove that an unsegmented (fully forwarding) network permits lateral movement across the enforcement point.
- Frame the legitimate flows and the identities behind them, so identity-based policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before any policy — every cross-segment flow currently traverses `el-gw`, which forwards all of it.

**Walkthrough**

**Step 1.** On `el-app01`, create a reachability probe:

```bash
cat > ~/reach.sh <<'EOF'
#!/usr/bin/env bash
probe() { timeout 3 bash -c "echo > /dev/tcp/$1/$2" 2>/dev/null \
          && echo "REACH  $1:$2  ($3)" || echo "BLOCK  $1:$2  ($3)"; }
probe 10.10.40.40 5432 "app/hmi -> db"
probe 10.10.20.11 80   "-> app http"
probe 10.10.30.50 502  "-> plc modbus"
EOF
chmod +x ~/reach.sh
~/reach.sh
```

**Step 2.** Run the same probe from `el-win01` (PowerShell):

```powershell
"10.10.40.40:5432","10.10.20.11:80","10.10.30.50:502" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Expected result.** Every probe returns **REACH**. The network is unsegmented: `el-gw` forwards every cross-segment flow.

**Negative test.** Nothing is blocked to find — the finding is that the enforcement point currently enforces nothing, so any identity can reach any resource.

**Rollback.** Keep `~/reach.sh` as your regression test.

### Lab 5.2 — Identify the legitimate flows and their identities

**Objective.** Write down the only east-west flows the business needs — and the *identity* of each source, since Elisity policy is written against identity, not address.

**Walkthrough**

| # | Source (identity) | Destination (identity) | Port | Legitimate? |
|:--|:--|:--|:--|:--|
| 1 | el-app01 (**AppServer**) | el-db01 (**Database**) | 5432 | **Yes** |
| 2 | el-win01 (**HMI**) | el-ot01 (**PLC**) | 502 | **Yes** |
| 3 | el-win01 (**HMI**) | el-db01 (**Database**) | 5432 | **No** (lateral movement) |
| 4 | el-app01 (**AppServer**) | el-ot01 (**PLC**) | 502 | **No** |
| 5 | any | el-win01 (**HMI**) | * | **No** by default |

**Expected result.** Two legitimate flows, each expressed as *AppServer → Database* and *HMI → PLC* — identity to identity. This is the policy you will build in the IdentityGraph in Chapter 06.

**Negative test.** Express the policy as "10.10.20.11 → 10.10.40.40:5432" instead. It works until the app is re-addressed or replaced, then silently fails. Elisity writes policy by identity precisely so it survives re-addressing. Keep the identities, not the addresses.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show that a compromised HMI can reach the crown-jewel database across the enforcement point.

**Walkthrough**

**Step 1.** Treat `el-win01` as compromised. Reach the database on the other segment:

```powershell
Test-NetConnection -ComputerName 10.10.40.40 -Port 5432
```

**Step 2.** Make the theft tangible with harvested app credentials:

```powershell
$env:PGPASSWORD='LabAppPassw0rd!'
& psql -h 10.10.40.40 -U appuser -d ellab -c "SELECT * FROM customers;"
```

**Expected result.** The HMI reads customer rows — the lateral-movement-to-exfiltration chain, and every packet of it crossed `el-gw` without being stopped, because the enforcement point has no policy yet.

**Negative test.** Re-run the app's own query from `el-app01` (`~/checkdb.sh` → 3); it also crosses `el-gw` and works. The router forwards both identically — it cannot tell **AppServer** from **HMI** until Elisity gives it identity-based policy to enforce.

**Rollback.** `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline.
- [ ] The legitimate flows written as identity-to-identity (AppServer→Database, HMI→PLC).
- [ ] Lateral movement from the HMI to the database reproduced across the enforcement point.
- [ ] You can state the goal: enforce AppServer→Database and HMI→PLC at `el-gw`, deny the rest.
