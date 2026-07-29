# Chapter 03: Defender — Vault and Account Management

## Learning Objectives

- Organize the Vault with safes and permissions.
- Onboard privileged accounts.
- Configure password management policies (CPM).
- Verify, reconcile, and rotate credentials.
- Complete a walkthrough for each account-management topic.

## Theory and Architecture

The **Defender** level validates daily PAM operations, starting with the **Vault** and **account
management**. Credentials live in **safes** — logical containers with their own **permissions**
(who can retrieve, use, or manage the accounts inside), the primary access-control boundary.
**Onboarding** brings privileged accounts under management: discovering them, storing them in the
right safe, and associating a **platform** (a template defining how that account type is managed).
The **CPM** then enforces **password management** per policy: **verify** (confirm the stored password
still works), **change/rotate** (set a new password on a schedule or on-demand), and **reconcile**
(fix a password that has drifted out of sync using a reconciliation account). Correct **safe design
and permissions** plus **automated rotation** is the heart of operational PAM — it ensures privileged
credentials are known, controlled, and regularly changed. This chapter teaches each with a hands-on
defensive walkthrough (safe permissions, onboarding logic, and CPM operations).

## Design Considerations

Design **safes by team/application** with least-privilege permissions. Onboard **all** privileged
accounts (unmanaged accounts are the risk). Associate the correct **platform** per account type. Set
CPM to **verify + rotate** on a schedule and **reconcile** on drift. Separate **use** from **manage**
permissions.

## Implementation and Automation

The labs design safe permissions, onboard an account, and run CPM operations.

## Validation and Troubleshooting

Confirm the account-management model:

```text
Vault -> safes (permission boundary: retrieve/use/manage). Onboard accounts -> safe + platform (management template).
CPM: verify (still valid) + change/rotate (schedule/on-demand) + reconcile (fix drift via reconciliation account).
```

Common pitfalls: over-broad **safe permissions** (everyone can retrieve everything); and **unmanaged**
privileged accounts CyberArk doesn't know about.

## Security and Best Practices

Least-privilege **safe permissions**, **onboard all** privileged accounts, correct **platforms**, and
CPM **verify/rotate/reconcile**. Separate use from manage. Audit for unmanaged accounts. All work is
defensive.

## Hands-On Lab

Account-management walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 3.1 — Design safe permissions

**Objective:** Least-privilege access to credentials.

```python
python3 - <<'PY'
safe={"name":"Windows-Servers","members":{
      "server-admins":["retrieve","use","list"],
      "pam-engineers":["manage","add/update accounts"],
      "auditors":["list","view audit"]}}
for role,perms in safe["members"].items(): print(f"{role:14}: {perms}")
print("Defender: separate use (server-admins) from manage (engineers); auditors read-only")
PY
```

**Expected result:** a safe with **role-separated** permissions — least-privilege credential access.

**Negative test:** give every group **manage** on the safe; anyone can alter credentials — separate
**use** from **manage**.

**Cleanup:** none.

### Lab 3.2 — Onboard a privileged account

**Objective:** Bring an account under management.

```python
python3 - <<'PY'
account={"address":"win-sql01","username":"Administrator","safe":"Windows-Servers",
         "platform":"WinDomainAccount","auto_manage":True}
for k,v in account.items(): print(f"{k:12}: {v}")
print("Onboarding: account -> correct safe + platform -> CPM now manages it")
PY
```

**Expected result:** the account **onboarded** to the right safe and platform, CPM-managed — bringing
it under control.

**Negative test:** leave the local Administrator unmanaged; it's an untracked risk — **onboard** it.

**Cleanup:** none.

### Lab 3.3 — Run CPM password operations

**Objective:** Verify, rotate, reconcile.

```python
python3 - <<'PY'
def cpm(op, works=True):
    return {"verify":"password confirmed valid" if works else "verify FAILED -> reconcile",
            "change":"new strong password set + stored",
            "reconcile":"password reset via reconciliation account -> back in sync"}[op]
for op in ["verify","change","reconcile"]: print(f"{op:9}: {cpm(op)}")
print("CPM lifecycle: verify -> change on schedule -> reconcile on drift")
PY
```

**Expected result:** the CPM **verify/change/reconcile** operations — automated password management.

**Negative test:** rotate a password in CyberArk but not on the target (or vice versa); they drift out
of sync — **reconcile** restores it.

**Cleanup:** none.

### Lab 3.4 — Detect an unmanaged account

**Objective:** Close discovery gaps.

```python
python3 - <<'PY'
discovered=["win-sql01\\Administrator","win-web01\\svc-iis","win-web01\\localadmin"]
managed=["win-sql01\\Administrator","win-web01\\svc-iis"]
gaps=[a for a in discovered if a not in managed]
print("unmanaged privileged accounts:", gaps)
print("Defender: onboard discovered gaps -> no privileged account left unmanaged")
PY
```

**Expected result:** the **unmanaged** `localadmin` flagged for onboarding — closing the discovery
gap.

**Negative test:** assume all privileged accounts are vaulted without **discovery**; shadow admins
persist — discover and onboard.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Defender account-management domain organizes the Vault into least-privilege safes, onboards all
privileged accounts to the right platforms, and uses the CPM to verify, rotate, and reconcile
credentials — known, controlled, regularly changed privileged access.

- [ ] I can design safe permissions.
- [ ] I can onboard a privileged account.
- [ ] I can run CPM verify/change/reconcile.
- [ ] I can detect unmanaged accounts.
- [ ] I completed Labs 3.1–3.4 including each negative test.
