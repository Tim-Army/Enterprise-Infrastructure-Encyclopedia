# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability on the underlay.
- Prove that a flat underlay permits lateral movement, and that every device is discoverable.
- Frame the legitimate flows so the overlay trust policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what on the flat underlay, before any overlay exists.

**Walkthrough**

**Step 1.** On `aw-app01`, create a reachability probe:

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

**Step 2.** Run the same probe from `aw-win01` (PowerShell):

```powershell
"10.10.20.12:5432","10.10.20.11:80","10.10.30.50:502" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Step 3.** Confirm every device is also *discoverable* — the property Airwall's cloaking removes:

```bash
ping -c1 10.10.20.12   # the db answers pings; it is visible on the underlay
```

**Expected result.** Every probe returns **REACH**, and the database answers pings. The underlay is flat and every device is visible and addressable.

**Negative test.** Nothing is blocked to find, and everything is discoverable — which is the finding: on the underlay, an attacker can both *see* and *reach* every device. Airwall's overlay makes protected devices invisible (cloaked) and reachable only by authorized identities.

**Cleanup.** Keep `~/reach.sh` as your regression test.

### Lab 5.2 — Identify the legitimate flows

**Objective.** Write down the only east-west flows the business needs — the overlay membership you will build in Chapter 06.

**Walkthrough**

| # | Source | Destination | Port | Legitimate? |
|:--|:--|:--|:--|:--|
| 1 | aw-app01 | aw-db01 | 5432 | **Yes** |
| 2 | aw-win01 (HMI) | aw-ot01 (PLC) | 502 | **Yes** |
| 3 | aw-win01 | aw-db01 | 5432 | **No** (lateral movement) |
| 4 | aw-app01 | aw-ot01 | 502 | **No** |
| 5 | any | aw-win01 | * | **No** by default |

**Expected result.** Two legitimate flows, which become two overlay trust relationships: *app ↔ db* and *hmi ↔ plc*. Everything else is off the overlay and therefore dark.

**Negative test.** Try to justify flow 3. On an Airwall overlay, unless the HMI and the database are placed in the same overlay network, the HMI cannot even *see* the database — so the burden is not "block it" but "never authorize it". Keep flow 3 a "no".

**Cleanup.** None.

### Lab 5.3 — Reproduce lateral movement

**Objective.** Show that a compromised HMI can reach the crown-jewel database across the flat underlay.

**Walkthrough**

**Step 1.** Treat `aw-win01` as compromised. Reach the database directly:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432
```

**Step 2.** Make the theft tangible with harvested app credentials:

```powershell
$env:PGPASSWORD='LabAppPassw0rd!'
& psql -h 10.10.20.12 -U appuser -d awlab -c "SELECT * FROM customers;"
```

**Expected result.** The HMI reads customer rows across the flat underlay — the lateral-movement-to-exfiltration chain that cloaking plus overlay policy will make impossible, because after Chapter 06 the database will not be visible or reachable off the overlay at all.

**Negative test.** Re-run the app's own query from `aw-app01` (`~/checkdb.sh` → 3); it works too, over the same flat underlay. The underlay cannot tell the app from the attacker — the overlay's cryptographic identity can.

**Cleanup.** `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline; devices are discoverable.
- [ ] The two legitimate flows written down as future overlay trust relationships.
- [ ] Lateral movement from the HMI to the database reproduced on the flat underlay.
- [ ] You can state the goal: put protected devices on an encrypted overlay, cloak the underlay, and authorize only app↔db and hmi↔plc.
