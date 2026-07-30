# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Establish and record the estate's baseline reachability with a repeatable script.
- Prove that a flat network permits lateral movement — including reuse of a stolen **service-account** credential.
- Frame the legitimate flows and the service-account boundary so later policy has a specification.

## Hands-On Lab

### Lab 5.1 — Baseline reachability

**Objective.** Measure what talks to what before any segmentation.

**Walkthrough**

**Step 1.** On `tf-app01`, create a reachability probe:

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

**Step 2.** Run the same probe from `tf-win01` (PowerShell):

```powershell
"10.10.20.12:5432","10.10.20.11:80","10.10.30.50:502" | ForEach-Object {
    $h,$p = $_.Split(":")
    $r = Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue
    "{0,-20} {1}" -f $_, $(if ($r.TcpTestSucceeded){"REACH"}else{"BLOCK"})
}
```

**Expected result.** Every probe returns **REACH**. The network is flat.

**Negative test.** Nothing is blocked to find — the finding is that any host can reach any service, and any host can *present the app's service account* to the database.

**Cleanup.** Keep `~/reach.sh` as your regression test.

### Lab 5.2 — Identify the legitimate flows and the service-account boundary

**Objective.** Write down the only east-west flows the business needs, and the identity boundary TrueFort adds: `svc_app` is legitimate **only** from `tf-app01`.

**Walkthrough**

| # | Source | Destination | Port | Identity | Legitimate? |
|:--|:--|:--|:--|:--|:--|
| 1 | tf-app01 | tf-db01 | 5432 | `svc_app` | **Yes** |
| 2 | tf-win01 (HMI) | tf-ot01 (PLC) | 502 | — | **Yes** |
| 3 | tf-win01 | tf-db01 | 5432 | `svc_app` (stolen) | **No** (service-account misuse) |
| 4 | tf-app01 | tf-ot01 | 502 | — | **No** |
| 5 | any | tf-win01 | * | — | **No** by default |

**Expected result.** Two legitimate flows; use of `svc_app` from anywhere but `tf-app01` is misuse by definition.

**Negative test.** Argue that "`svc_app` is a valid account, so its use is fine wherever it appears." That is exactly the assumption attackers exploit: a valid credential used from an invalid place. Binding the account to its legitimate host is the control TrueFort adds. Keep row 3 a "no".

**Cleanup.** None.

### Lab 5.3 — Reproduce lateral movement and service-account misuse

**Objective.** Show that a compromised HMI can reach the database and reuse the stolen `svc_app` credential.

**Walkthrough**

**Step 1.** Treat `tf-win01` as compromised. The attacker has harvested the `svc_app` credential (from app config, memory, or a script). Reach the database:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432
```

**Step 2.** Use the stolen service account from the HMI — the misuse:

```powershell
$env:PGPASSWORD='Svc!AppPassw0rd'
& psql -h 10.10.20.12 -U svc_app -d tflab -c "SELECT * FROM customers;"
```

**Step 3.** On `tf-db01`, observe that the database itself logged the connection — including that `svc_app` connected from `10.10.20.21`, not `10.10.20.11`:

```bash
sudo tail -5 /var/log/postgresql/postgresql-*-main.log | grep -i "connection authorized"
```

**Expected result.** The HMI reads customer rows as `svc_app`, and the database log shows the service account connecting from the *wrong* host — the exact signal TrueFort turns into a detection and a block.

**Negative test.** Re-run the app's own query from `tf-app01` (`~/checkdb.sh` → 3); `svc_app` connects from `10.10.20.11`, which is legitimate. The credential is identical in both cases — only the *source and process* differ, which is why identity-aware policy, not a password check, is what distinguishes them.

**Cleanup.** `Remove-Item Env:\PGPASSWORD`.

## Summary and Completion Checklist

- [ ] `~/reach.sh` created and shows all REACH at baseline.
- [ ] The legitimate flows and the `svc_app`-only-from-tf-app01 boundary are written down.
- [ ] Lateral movement and stolen-service-account reuse reproduced, and seen in the database log.
- [ ] You can state the goal: permit flows 1 and 2, deny the rest, and bind `svc_app` to its legitimate host.
