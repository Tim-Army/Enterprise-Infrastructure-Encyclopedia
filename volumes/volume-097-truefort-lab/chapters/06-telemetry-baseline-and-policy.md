# Chapter 06: Telemetry, the Application Baseline, and Policy

## Learning Objectives

- Explain how TrueFort obtains telemetry — from an existing EDR or its own agent — and what that telemetry contains.
- Bring the estate under observation, or stand up the equivalent native telemetry and enforcement.
- Build an application behavior baseline from process, network, and identity data.
- Ring-fence a two-tier application from the baseline.

This is the core of the lab. Each exercise carries both tracks. TrueFort's method is **observe behavior, baseline it, then enforce least privilege** — and, crucially, tie policy to *identity and process*, not only to address and port.

## Hands-On Lab

### Lab 6.1 — Where the telemetry comes from

**Objective.** Decide how TrueFort will see each host's behavior.

**Background.** TrueFort reasons over **process, network, and identity** telemetry. It can source that telemetry two ways:

- **EDR-leveraged** — ingesting from an EDR you already run (CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint). Where EDR is deployed, you add no new agent.
- **TrueFort agent** — a lightweight agent, where no suitable EDR exists.

Either way the enforcement lands on the **native host firewall**. In this lab you have no EDR, so Track 2 gathers the same signals from native OS tooling.

**Walkthrough.**

**Step 1.** Classify each host's telemetry source for this lab:

| Host | Telemetry source (real) | Native stand-in (Track 2) |
|:---|:---|:---|
| tf-app01 | EDR or TrueFort agent | `ss -tnp`, `auditd`, PostgreSQL logs |
| tf-db01 | EDR or TrueFort agent | `ss -tnp`, `auditd`, PostgreSQL `log_connections` |
| tf-win01 | EDR or TrueFort agent | Windows Firewall log, Sysmon (optional) |
| tf-gw | EDR or TrueFort agent | `conntrack`, `ss -tnp` |
| tf-ot01 | **none** (no agent possible) | observed only from `tf-gw` |

**Step 2.** State the model: *TrueFort turns process-network-identity telemetry into a behavior baseline, then enforces least privilege on the native firewall — binding permissions to the process and account, not just the address.*

**Expected result.** A per-host telemetry plan.

**Negative test.** Assume the PLC can be baselined like the others. It runs no agent and emits no host telemetry; TrueFort sees it only as the far end of flows observed elsewhere. That is why Chapter 08 protects it from a neighbor.

**Cleanup.** None.

### Lab 6.2 — Bring the estate under observation

**Objective.** Establish observation and a native enforcement layer.

**Track 1 — Real TrueFort.** Connect the EDR integration (or deploy the TrueFort agent) so the hosts report to the console, and confirm each appears with live process and network activity. Enforcement remains off while you baseline.

**Track 2 — Native equivalent.** Turn on the native telemetry and a permissive-but-logging firewall.

**Step 1 — tf-app01, tf-db01, tf-gw.**

```bash
sudo apt -y install nftables conntrack auditd
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
table inet truefort {
    chain input {
        type filter hook input priority 0; policy accept;   # observe, do not block
        ct state established,related accept
        iif "lo" accept
        log prefix "TF-OBSERVE: " level info
    }
}
EOF
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables auditd
```

On `tf-gw`, this `truefort` table coexists with the `ip nat` table.

**Step 2.** Confirm you can see process-attributed behavior — the heart of TrueFort's telemetry. On `tf-db01`, watch who serves 5432:

```bash
sudo ss -tnp state established '( sport = :5432 )'   # process + peer for each db connection
```

**Expected result.** Every host is observed (Track 1) or emitting native process/network telemetry (Track 2); nothing is blocked yet.

**Negative test.** Rely on network telemetry alone (no process attribution). You will see "10.10.20.11 → 10.10.20.12:5432" but not *which process* opened it, and you will be unable to distinguish the app from a webshell on the same host. Process context is the signal that makes identity-aware policy possible.

**Cleanup.** Leave observation in place.

### Lab 6.3 — Build the application behavior baseline

**Objective.** Derive the normal behavior of the two-tier application — which process, which account, which peer, which port.

**Track 1 — Real TrueFort.** Let the platform baseline the application over its learning window. It records that on `tf-app01` the application process, running as its service identity, connects to `tf-db01:5432` as `svc_app`, and that the HMI polls the PLC on 502 — and nothing else.

**Track 2 — Native equivalent.** Generate legitimate traffic, then record the baseline as behavior, not just flows.

**Step 1.** On `tf-app01`, run `~/checkdb.sh` a few times; on `tf-win01`, poll the PLC.

**Step 2.** On `tf-db01`, extract the identity-aware baseline from the connection log:

```bash
sudo grep "connection authorized" /var/log/postgresql/postgresql-*-main.log \
  | sed -E 's/.*user=([^ ]+).*/user=\1/' | sort | uniq -c
# and the process/peer view:
sudo ss -tnp state established '( sport = :5432 )'
```

**Expected result.** A behavior baseline, for example: *`svc_app` connects to 5432 only from `10.10.20.11`; the HMI reaches the PLC only on 502.* Note it captures **identity** (`svc_app`) and **source**, not just ports.

**Negative test.** Baseline while the Lab 5.3 misuse is running and the baseline learns `svc_app` from `10.10.20.21` as "normal". Behavioral baselines faithfully record whatever happens, so the window must observe clean behavior — and be reviewed.

**Cleanup.** Keep the baseline.

### Lab 6.4 — Ring-fence the application

**Objective.** From the baseline, author the coarse boundary: permit the app→db flow, deny other ingress to the database — validated before enforcing.

**Track 1 — Real TrueFort.** Create an application policy permitting the baselined app→db behavior and denying the rest, in a monitoring (non-blocking) posture first; confirm the simulation would deny the HMI→db misuse.

**Track 2 — Native equivalent.** On `tf-db01`, express the ring-fence with the segmentation still observing (log-and-accept):

```bash
sudo nft add chain inet truefort seg '{ }'
sudo nft add rule inet truefort input jump seg
sudo nft add rule inet truefort seg ip saddr 10.10.20.11 tcp dport 5432 accept
sudo nft add rule inet truefort seg tcp dport 5432 log prefix "TF-WOULD-DENY db: " level warn accept
```

Reproduce the misuse from `tf-win01` and confirm a `TF-WOULD-DENY db:` line appears while the app's own query raises none.

**Expected result.** A validated ring-fence: app→db permitted, HMI→db flagged — before anything is blocked.

**Negative test.** Add `10.10.20.21` to the allowed sources "temporarily"; the misuse stops being flagged. Over-broad allows hide the very behavior you are hunting. Remove it.

**Cleanup.** Keep the ring-fence; Chapter 07 enforces it and adds the identity binding.

## Summary and Completion Checklist

- [ ] Telemetry sources (EDR/agent vs native) understood, including why process context matters.
- [ ] Estate under observation (or native telemetry + logging firewall).
- [ ] An identity-aware application baseline built and reviewed.
- [ ] The application ring-fenced and validated in a non-blocking posture.
