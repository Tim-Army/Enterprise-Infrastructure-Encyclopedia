# Chapter 07: Veeam Recovery Orchestrator

## Learning Objectives

- Explain Veeam Recovery Orchestrator and its recovery plans.
- Build an orchestration plan with steps and readiness checks.
- Run a non-disruptive DR test and generate documentation.
- Verify recoverability with SureBackup.
- Complete a walkthrough for each scale-automate-secure topic.

## Theory and Architecture

The third VMCE+ training — **Veeam Data Platform: Scale, Automate, Secure (Veeam Recovery Orchestrator)**
— covers **Veeam Recovery Orchestrator (VRO)**, which turns backups and replicas into **tested,
documented, one-click disaster recovery**. A **recovery plan** (orchestration plan) sequences the
recovery of an application's tiers — network, databases, app servers, web servers — with dependency
ordering, custom steps/scripts, and **readiness checks**. VRO can run **non-disruptive DR tests** in an
isolated environment, automatically generate **DR documentation** and test reports (for audits and
compliance), and continuously score **recovery readiness** against RTO/RPO SLAs. Underpinning
verification is **SureBackup**, which powers on backups in an isolated **virtual lab** to prove they
boot and applications respond — recoverability verified without touching production. This chapter teaches
orchestration and verification with hands-on walkthroughs.

## Design Considerations

Model each application as a **recovery plan** with correct **dependency order** (network first, then
data, then app tiers). Add **readiness checks** and custom steps so recovery is repeatable. Schedule
**non-disruptive DR tests** and keep the generated **documentation** for audits. Use **SureBackup** to
verify backups routinely. Map plans to real **RTO/RPO SLAs** and let VRO score readiness.

## Implementation and Automation

The labs reason about VRO, build a recovery plan with ordered steps, run a DR test with documentation,
and verify a backup with SureBackup — the automation the third VMCE+ course validates.

## Validation and Troubleshooting

Confirm orchestration:

```text
Recovery plan = ordered recovery of app tiers (network -> data -> app -> web) + readiness checks
Non-disruptive DR test = isolated run -> auto documentation + test report (audit-ready)
Readiness scoring = continuous RTO/RPO SLA compliance
SureBackup = power on backups in an isolated virtual lab -> verify boot + app response
```

Common pitfalls: a recovery plan with wrong **dependency order** (app boots before its database); and
claiming DR works without ever running a **non-disruptive test** or **SureBackup**.

## Security and Best Practices

Rehearse recovery with non-disruptive tests, keep audit documentation, and verify backups with
SureBackup so recovery is proven, not assumed — defensive assurance for your own environment. All work
is authorized.

## Hands-On Lab

Scale-automate-secure walkthroughs. **Shared prerequisites** — a Veeam Recovery Orchestrator/Premium
environment (or the concepts, modeled in `python3`) with backups/replicas; the Veeam PowerShell module
for SureBackup. **Cost:** none (eval/Community as available).

### Lab 7.1 — Reason about Recovery Orchestrator

**Objective:** Place VRO in the platform.

```python
python3 - <<'PY'
vro = {
  "Orchestrate": "one-click recovery of a whole application, ordered by dependency",
  "Test":        "non-disruptive DR test in an isolated environment",
  "Document":    "auto-generated DR docs + test reports for audits",
  "Assure":      "continuous readiness scoring vs RTO/RPO SLAs",
}
for k, v in vro.items():
    print(f"{k:11}: {v}")
print("VRO = tested, documented, one-click DR built on backups and replicas")
PY
```

**Expected result:** VRO's four functions — orchestrate, test, document, assure — mapped to real DR
value.

**Negative test:** treat manual runbooks as DR; VRO makes recovery **tested and documented** — automate
it.

**Cleanup:** none.

### Lab 7.2 — Build a recovery plan with ordered steps

**Objective:** Sequence an application's recovery.

```python
python3 - <<'PY'
plan = [
  (1, "Recover network / VLAN mapping"),
  (2, "Recover database tier (db-vm02)  [readiness: SQL online]"),
  (3, "Recover app tier (app-vm01)      [readiness: service up]"),
  (4, "Recover web tier (web-vm05)      [readiness: HTTP 200]"),
]
for step, action in plan:
    print(f"Step {step}: {action}")
print("Dependency order: network -> data -> app -> web; each with a readiness check")
PY
```

**Expected result:** an ordered recovery plan with per-step readiness checks — repeatable DR.

**Negative test:** recover the app tier before its database; the app fails its readiness check — order
network → data → app → web.

**Cleanup:** none.

### Lab 7.3 — Run a non-disruptive DR test

**Objective:** Prove DR without touching production.

```python
python3 - <<'PY'
test = {
  "environment": "isolated virtual lab (fenced network)",
  "steps_run":   4, "steps_passed": 4,
  "rto_target_min": 60, "rto_actual_min": 22,
  "artifact":    "auto-generated DR test report (PDF) for audit",
}
for k, v in test.items():
    print(f"{k:14}: {v}")
print("Result: DR test PASSED in an isolated lab; documentation generated -> production untouched")
PY
```

**Expected result:** a passed DR test in an isolated lab with auto-generated documentation — audit-ready
proof.

**Negative test:** "test" DR by failing over production; use a **non-disruptive** isolated test instead.

**Cleanup:** none (the fenced lab tears down automatically).

### Lab 7.4 — Verify a backup with SureBackup

**Objective:** Prove a backup is recoverable.

```powershell
PS> $job = Get-VBRSureBackupJob -Name "SureBackup-App"
PS> Start-VBRSureBackupJob -Job $job

PS> Get-VBRSureBackupJob -Name "SureBackup-App" | Select-Object Name, LastResult
Name             LastResult
----             ----------
SureBackup-App   Success
```

**Expected result:** a SureBackup job that boots the backup in an isolated lab and verifies it —
`Success` means the backup is recoverable.

**Negative test:** trust untested backups; a corrupt backup only shows up at restore time — verify with
**SureBackup**.

**Cleanup:** none (SureBackup tears down its virtual lab automatically).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Veeam Recovery Orchestrator turns backups and replicas into tested, documented, one-click DR: recovery
plans with dependency-ordered steps and readiness checks, non-disruptive DR tests that auto-generate
audit documentation, continuous RTO/RPO readiness scoring, and SureBackup verification of
recoverability.

- [ ] I can explain Recovery Orchestrator's role.
- [ ] I can build a recovery plan with ordered steps.
- [ ] I can run a non-disruptive DR test.
- [ ] I can verify a backup with SureBackup.
- [ ] I completed Labs 7.1–7.4 including each negative test.
