# Chapter 08: FlexPod and Security Hardening

## Learning Objectives

- Explain FlexPod converged infrastructure and its validated designs.
- Distinguish the FlexPod Design and Implementation-and-Administration specialists.
- Harden ONTAP administrative access (RBAC, MFA, secure protocols).
- Enable volume/aggregate encryption (NVE/NAE).
- Complete a walkthrough for each FlexPod-and-hardening topic.

## Theory and Architecture

**FlexPod** is the **Cisco and NetApp** converged-infrastructure architecture: Cisco **UCS** compute and
**Nexus/MDS** networking with NetApp **ONTAP** storage, validated together as **Cisco Validated Designs
(CVDs)**. Two joint **Specialist** credentials cover it — **Cisco and NetApp Certified FlexPod Design
Specialist** (sizing and architecting a FlexPod) and **Cisco and NetApp Certified FlexPod Implementation
and Administration Specialist** (deploying and operating it). Alongside converged infrastructure, the
NCDA's **Security** domain and every path expect hardened storage: least-privilege **RBAC** (scoped
`security login` roles), **multi-factor authentication** for administrators, **secure management
protocols** (SSH/HTTPS, disabling Telnet/RSH), and **encryption** — **NetApp Volume Encryption (NVE)**
per volume or **NetApp Aggregate Encryption (NAE)** for a whole aggregate, keyed by **Onboard Key
Manager** or an external KMIP server. This chapter teaches FlexPod design and security hardening with
hands-on walkthroughs.

## Design Considerations

Size a **FlexPod** from a **CVD** so compute, network, and storage are balanced and supported. Separate
**Design** (architecture, sizing) from **Implementation and Administration** (deploy, operate). Harden
every cluster: scope admin **roles**, require **MFA**, disable insecure protocols, and encrypt data at
rest with **NVE/NAE**. Manage keys with **Onboard Key Manager** or external **KMIP** with escrow.

## Implementation and Automation

The labs reason about FlexPod's validated stack, create a scoped admin role, and enable volume
encryption — the converged-design and hardening work these credentials validate.

## Validation and Troubleshooting

Confirm converged design and hardening:

```text
FlexPod = Cisco UCS + Nexus/MDS + NetApp ONTAP, validated as CVDs
Specialists: FlexPod Design (architect/size) | FlexPod Implementation & Administration (deploy/operate)
Harden: scoped RBAC roles + MFA + SSH/HTTPS (no Telnet/RSH)
Encrypt at rest: NVE (per volume) / NAE (per aggregate); keys via Onboard Key Manager or KMIP
```

Common pitfalls: sizing a FlexPod outside a **CVD** (an unsupported combination); and enabling
encryption without securing/escrowing the **keys** (lose the keys, lose the data).

## Security and Best Practices

Least-privilege **roles**, **MFA** for admins, **secure protocols** only, and **encryption at rest**
with escrowed keys are the baseline. These controls protect **your own** storage and administrators —
defensive hardening, authorized on systems you operate.

## Hands-On Lab

FlexPod-and-hardening walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster
(`admin@cluster1`), SVM `svm_app`, volume `vol_finance`, and `python3`. **Cost:** none.

### Lab 8.1 — Reason about the FlexPod stack

**Objective:** Map the converged components and the two specialists.

```python
python3 - <<'PY'
flexpod = {
  "Compute":  "Cisco UCS (blades / X-Series)",
  "Network":  "Cisco Nexus (LAN) + MDS (SAN fabric)",
  "Storage":  "NetApp ONTAP (AFF/FAS)",
  "Blueprint":"Cisco Validated Design (CVD) — tested end to end",
}
for k, v in flexpod.items():
    print(f"{k:9}: {v}")
specialists = ["FlexPod Design (architect + size)",
               "FlexPod Implementation & Administration (deploy + operate)"]
print("Specialists:", " | ".join(specialists))
PY
```

**Expected result:** the Cisco+NetApp stack and the two joint specialists — the FlexPod credential map.

**Negative test:** mix an unvalidated switch/firmware combination into a FlexPod; it falls outside the
**CVD** and loses joint support — build to a validated design.

**Cleanup:** none.

### Lab 8.2 — Create a scoped admin role

**Objective:** Apply least-privilege RBAC.

```text
cluster1::> security login role create -role vol_operator -cmddirname "volume" -access all
cluster1::> security login role create -role vol_operator -cmddirname "volume snapshot" -access all
cluster1::> security login create -user-or-group-name opsvc -application ssh -authentication-method password \
  -role vol_operator -vserver cluster1

cluster1::> security login show -user-or-group-name opsvc -fields role,application
user-or-group-name application role
------------------ ----------- ------------
opsvc              ssh         vol_operator
```

**Expected result:** an `opsvc` account limited to volume commands — least privilege, not full admin.

**Negative test:** give the operator the built-in `admin` role for convenience; that grants
cluster-wide power — bind the scoped `vol_operator` role instead.

**Cleanup:**

```text
cluster1::> security login delete -user-or-group-name opsvc -application ssh -vserver cluster1
cluster1::> security login role delete -role vol_operator -cmddirname "volume"
cluster1::> security login role delete -role vol_operator -cmddirname "volume snapshot"
```

### Lab 8.3 — Enable volume encryption at rest

**Objective:** Protect data with NVE and an onboard key manager.

```text
cluster1::> security key-manager onboard enable -cc-mode-enabled no
Enter the onboard key-manager passphrase: ********

cluster1::> volume encryption conversion start -vserver svm_app -volume vol_finance
[Job 81] Job succeeded: DONE

cluster1::> volume show -vserver svm_app -volume vol_finance -fields encryption-state,encrypt
vserver  volume       encryption-state encrypt
-------- ------------ ---------------- -------
svm_app  vol_finance  encrypted        true
```

**Expected result:** the volume converted to `encrypted` under NetApp Volume Encryption — data at rest
is protected.

**Negative test:** enable encryption but never back up/escrow the onboard **passphrase**; losing it
makes the data unrecoverable — escrow keys (or use external KMIP).

**Cleanup:** none (encryption is left enabled; it is the hardened state).

### Lab 8.4 — Disable insecure management protocols

**Objective:** Enforce secure administration.

```text
cluster1::> security ssl show -vserver cluster1 -fields server-enabled
vserver  server-enabled
-------- --------------
cluster1 true

cluster1::> system services web show -fields http-enabled,https-enabled
http-enabled https-enabled
------------ -------------
false        true
```

**Expected result:** HTTPS/SSL enabled and plain HTTP disabled — management traffic is encrypted.

**Negative test:** leave plain HTTP (or Telnet/RSH) enabled for management; credentials cross the wire
in clear text — disable insecure protocols and use SSH/HTTPS.

**Cleanup:** none (secure state is the goal).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

FlexPod is the Cisco-and-NetApp converged architecture validated as CVDs, with joint Design and
Implementation-and-Administration specialists; every cluster is hardened with least-privilege RBAC, MFA,
secure protocols, and NVE/NAE encryption at rest keyed by an onboard or KMIP key manager — defensive
protection of your own infrastructure.

- [ ] I can explain FlexPod and its two specialists.
- [ ] I can create a scoped admin role.
- [ ] I can enable volume encryption at rest.
- [ ] I can enforce secure management protocols.
- [ ] I completed Labs 8.1–8.4 including each negative test.
