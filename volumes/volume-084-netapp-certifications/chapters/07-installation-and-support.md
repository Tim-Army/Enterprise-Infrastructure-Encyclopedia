# Chapter 07: Installation and Support

## Learning Objectives

- Reason about cluster setup and node installation.
- Configure and trigger AutoSupport (ASUP).
- Triage storage performance with QoS and statistics.
- Place the E-Series Implementation Engineer in the ladder.
- Complete a walkthrough for each installation-and-support topic.

## Theory and Architecture

Two Professional/Specialist paths cover the operational life of a system. The **Installation** path runs
from **Storage Installation Engineer — ONTAP (Professional)** to **Implementation Engineer —
MetroCluster (Specialist)**; the **Support** path runs from **Support Engineer (Professional)** to
**Support Engineer ONTAP (Specialist)**; and the **Installation E-Series** path leads to **Implementation
Engineer — SAN E-Series (Specialist)** for NetApp's **E-Series** block arrays (managed by **SANtricity**,
not ONTAP). Installation covers racking, cabling, node setup, and **cluster setup** (the `cluster setup`
wizard, joining nodes, configuring the cluster and node-management LIFs). Support rests on
**AutoSupport (ASUP)** — ONTAP's phone-home telemetry that opens cases and drives proactive health
(Active IQ) — plus **performance triage** using **QoS** policies (min/max throughput and IOPS ceilings)
and the `statistics`/`qos statistics` commands. This chapter teaches installation and support with
hands-on ONTAP walkthroughs.

## Design Considerations

Follow the **Hardware Universe** for supported configurations when installing. Configure **AutoSupport**
to a reachable transport (HTTPS) and to NetApp plus an internal mailhost. Use **QoS** ceilings to stop a
noisy neighbor and QoS floors to guarantee a critical workload. Keep firmware and ONTAP within supported
versions. Manage **E-Series** with SANtricity separately from ONTAP.

## Implementation and Automation

The labs read cluster setup state, configure and trigger AutoSupport, apply a QoS ceiling, and reason
about E-Series — the install-and-run work these paths validate.

## Validation and Troubleshooting

Confirm the operational model:

```text
Install: rack/cable -> cluster setup wizard -> join nodes -> mgmt LIFs; Hardware Universe = supported configs
Support: AutoSupport (ASUP) phone-home -> cases + Active IQ proactive health
Performance: QoS min/max (floors/ceilings) + statistics / qos statistics
E-Series: block arrays managed by SANtricity (not ONTAP)
```

Common pitfalls: **AutoSupport** disabled or blocked by a firewall (no proactive support, slower case
resolution); and a missing **QoS** ceiling letting one workload starve others.

## Security and Best Practices

Send **AutoSupport** over HTTPS, restrict who can modify it, and review what telemetry is shared. Protect
management LIFs and use scoped support roles. All work is authorized administration.

## Hands-On Lab

Installation-and-support walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster
(`admin@cluster1`) with SVM `svm_app` and volume `vol_finance`, and `python3`. **Cost:** none.

### Lab 7.1 — Read cluster setup state

**Objective:** Confirm the cluster and management network.

```text
cluster1::> cluster show -fields node,health,eligibility
node         health eligibility
------------ ------ -----------
cluster1-01  true   true
cluster1-02  true   true

cluster1::> network interface show -role cluster-mgmt,node-mgmt -fields lif,address,status-oper
vserver  lif             address        status-oper
-------- --------------- -------------- -----------
cluster1 cluster_mgmt    192.168.0.10   up
cluster1 cluster1-01_mgmt 192.168.0.11  up
```

**Expected result:** a healthy cluster with cluster- and node-management LIFs up — a completed install.

**Negative test:** join a node running a different ONTAP version to the cluster; the join fails on
version mismatch — bring nodes to a matching release first.

**Cleanup:** none (read-only).

### Lab 7.2 — Configure and trigger AutoSupport

**Objective:** Enable proactive support telemetry.

```text
cluster1::> system node autosupport modify -node * -state enable -transport https \
  -support enable -mail-hosts mailhost.lab.local
cluster1::> system node autosupport invoke -node cluster1-01 -type test -message "install validation"

cluster1::> system node autosupport history show -node cluster1-01 -fields destination,status
node        destination status
----------- ----------- ---------
cluster1-01 http        sent-successful
```

**Expected result:** a test AutoSupport sent successfully — proactive support is working.

**Negative test:** leave AutoSupport disabled; NetApp cannot open proactive cases and support is slower
— enable it over HTTPS.

**Cleanup:**

```text
cluster1::> system node autosupport modify -node * -mail-hosts -
```

### Lab 7.3 — Apply a QoS ceiling

**Objective:** Stop a noisy-neighbor workload.

```text
cluster1::> qos policy-group create -policy-group pg_limit -vserver svm_app -max-throughput 5000IOPS
cluster1::> volume modify -vserver svm_app -volume vol_finance -qos-policy-group pg_limit

cluster1::> qos statistics performance show -iterations 1
Policy Group     IOPS    Throughput   Latency
---------------- ------- ------------ --------
pg_limit         4980    39.84MB/s    1.20ms
```

**Expected result:** the volume capped at 5,000 IOPS — it can no longer starve neighbors.

**Negative test:** run a batch job with no QoS ceiling on a shared cluster; it consumes all IOPS and
critical apps slow down — apply a max-throughput ceiling.

**Cleanup:**

```text
cluster1::> volume modify -vserver svm_app -volume vol_finance -qos-policy-group none
cluster1::> qos policy-group delete -policy-group pg_limit
```

### Lab 7.4 — Reason about E-Series

**Objective:** Place E-Series/SANtricity in the portfolio.

```python
python3 - <<'PY'
portfolio = {
  "ONTAP (AFF/ASA/FAS)": "unified NAS+SAN+object; managed by ONTAP / System Manager / BlueXP",
  "E-Series (EF/E)":     "high-performance block SAN; managed by SANtricity (not ONTAP)",
}
for k, v in portfolio.items():
    print(f"{k:22}: {v}")
print("Rule: E-Series certs (Impl Engineer SAN E-Series) use SANtricity, a separate management stack")
PY
```

**Expected result:** ONTAP and E-Series distinguished by management stack — the E-Series path uses
SANtricity.

**Negative test:** expect ONTAP clustershell commands to manage an E-Series array; use **SANtricity**
System Manager/CLI instead.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Installation and Support paths cover a system's operational life: cluster setup and node
installation against the Hardware Universe, AutoSupport phone-home feeding proactive Active IQ health,
performance triage with QoS floors/ceilings and statistics, and the E-Series/SANtricity block arrays for
the E-Series Implementation Engineer.

- [ ] I can read cluster setup and management-network state.
- [ ] I can configure and trigger AutoSupport.
- [ ] I can apply a QoS ceiling and read qos statistics.
- [ ] I can place E-Series/SANtricity in the portfolio.
- [ ] I completed Labs 7.1–7.4 including each negative test.
