# Chapter 05: Scale-Out Repositories and Cloud

## Learning Objectives

- Build a scale-out backup repository (SOBR) with performance and capacity tiers.
- Tier backups to object storage with immutability.
- Reason about Veeam Data Cloud Vault.
- Apply the 3-2-1-1-0 rule with a backup copy job.
- Complete a walkthrough for each scale-out-and-cloud topic.

## Theory and Architecture

A **scale-out backup repository (SOBR)** aggregates several storage devices into one logical repository
with tiers: the **performance tier** (fast local storage for recent backups), the **capacity tier**
(**object storage** — Amazon S3, Azure Blob, S3-compatible, or **Veeam Data Cloud Vault** — for older
restore points), and the **archive tier** (cheap cold object storage such as S3 Glacier for long-term
retention). Object tiers support **immutability** (S3 Object Lock / immutable Vault) so copies cannot be
altered or deleted before their retention expires — the backbone of ransomware resilience. **Veeam Data
Cloud Vault** is Veeam's fully managed, pre-secured immutable cloud object storage. All of this serves
the **3-2-1-1-0 rule**: **3** copies of data, on **2** media, with **1** offsite, **1** offline/immutable,
and **0** errors after recovery verification — implemented with **backup copy jobs** to a second
repository or the cloud. This chapter teaches scale-out and cloud with hands-on Veeam PowerShell
walkthroughs.

## Design Considerations

Build a **SOBR** so capacity grows without re-pointing jobs, and set **tiering** to move older points to
object storage automatically. Turn on **immutability** on the object tier / Vault for a ransomware-proof
copy. Meet **3-2-1-1-0** with a **backup copy job** to offsite/immutable storage. Balance restore speed
(performance tier) against cost (capacity/archive tiers).

## Implementation and Automation

The labs build a SOBR, add an immutable object-storage capacity tier, create a backup copy job for
3-2-1-1-0, and reason about Data Cloud Vault — the scale and resilience VMCE+ expects.

## Validation and Troubleshooting

Confirm scale-out and cloud:

```text
SOBR tiers: performance (fast local) -> capacity (object, immutable) -> archive (cold object)
Immutability: S3 Object Lock / immutable Vault = cannot alter/delete before retention expires
Data Cloud Vault = Veeam-managed, pre-secured immutable cloud object storage
3-2-1-1-0: 3 copies, 2 media, 1 offsite, 1 offline/immutable, 0 recovery errors -> backup copy job
```

Common pitfalls: a SOBR with only local tiers (no offsite/immutable copy — fails 3-2-1-1-0); and object
storage **without** immutability (deletable by ransomware/insiders).

## Security and Best Practices

Keep at least one **immutable, offsite** copy (object lock or Vault), verify recoverability (the "0"),
and separate credentials for the object tier. This is the defensive core of ransomware resilience. All
work is authorized.

## Hands-On Lab

Scale-out-and-cloud walkthroughs. **Shared prerequisites** — a Veeam Backup & Replication Community
Edition server with two repositories and an object-storage endpoint (or Data Cloud Vault); the Veeam
PowerShell module. **Cost:** none (lab object storage).

### Lab 5.1 — Build a scale-out backup repository

**Objective:** Aggregate storage into one logical repository.

```powershell
PS> $ext = Get-VBRBackupRepository -Name "Repo-01","Repo-02"
PS> Add-VBRScaleOutBackupRepository -Name "SOBR-01" -Extent $ext -PolicyType DataLocality
PS> Get-VBRScaleOutBackupRepository -Name "SOBR-01" | Select-Object Name, PolicyType

Name     PolicyType
----     ----------
SOBR-01  DataLocality
```

**Expected result:** a SOBR aggregating two extents into one performance tier.

**Negative test:** keep a dozen separate repositories and re-point jobs by hand as they fill; use a
**SOBR** so capacity scales transparently.

**Cleanup:**

```powershell
PS> Remove-VBRScaleOutBackupRepository -Repository (Get-VBRScaleOutBackupRepository -Name "SOBR-01")
```

### Lab 5.2 — Add an immutable object capacity tier

**Objective:** Add a ransomware-proof cloud tier.

```powershell
PS> $obj = Add-VBRAmazonS3Repository -Name "Cap-S3" -AmazonS3Folder "veeam-cap" -EnableBackupImmutability -ImmutabilityPeriod 30
PS> Set-VBRScaleOutBackupRepository -Repository (Get-VBRScaleOutBackupRepository -Name "SOBR-01") -EnableCapacityTier -ObjectStorageRepository $obj

PS> Get-VBRAmazonS3Repository -Name "Cap-S3" | Select-Object Name, ImmutabilityPeriod
Name    ImmutabilityPeriod
----    ------------------
Cap-S3  30
```

**Expected result:** an object capacity tier with **30-day immutability** — backups cannot be deleted
early.

**Negative test:** add object storage without immutability; ransomware or an insider can delete the
cloud copy — enable **Object Lock / immutability**.

**Cleanup:** none (immutable objects persist until retention expires — expected).

### Lab 5.3 — Create a backup copy job (3-2-1-1-0)

**Objective:** Keep an offsite/immutable second copy.

```powershell
PS> $job = Get-VBRJob -Name "Daily-App"
PS> $target = Get-VBRScaleOutBackupRepository -Name "SOBR-01"
PS> Add-VBRViBackupCopyJob -Name "Copy-App-Offsite" -BackupJob $job -Repository $target

PS> Get-VBRJob -Name "Copy-App-Offsite" | Select-Object Name, JobType
Name              JobType
----              -------
Copy-App-Offsite  BackupSync
```

**Expected result:** a backup copy job placing a second copy on the SOBR/object tier — satisfying the
offsite/immutable legs of 3-2-1-1-0.

**Negative test:** keep only the primary backup on one repository; one site loss destroys all copies —
add a **backup copy** offsite.

**Cleanup:**

```powershell
PS> Remove-VBRJob -Job (Get-VBRJob -Name "Copy-App-Offsite") -Confirm:$false
```

### Lab 5.4 — Reason about Veeam Data Cloud Vault

**Objective:** Choose managed immutable cloud storage.

```python
python3 - <<'PY'
options = {
  "Self-managed S3 + Object Lock": "you configure the bucket, IAM, and immutability",
  "Veeam Data Cloud Vault":        "Veeam-managed, pre-secured, immutable by default, predictable cost",
}
for k, v in options.items():
    print(f"{k:32}: {v}")
print("Rule: Data Cloud Vault = fastest path to an immutable, offsite copy (the '1' offline in 3-2-1-1-0)")
PY
```

**Expected result:** Data Cloud Vault as the managed, immutable-by-default option for the offsite copy.

**Negative test:** hand-roll object-lock IAM under time pressure and misconfigure it; **Data Cloud
Vault** ships pre-secured and immutable — use it when you want managed resilience.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Scale-out backup repositories tier data from fast local performance storage to immutable object capacity
and cold archive tiers (including Veeam Data Cloud Vault), and backup copy jobs implement the 3-2-1-1-0
rule — three copies, two media, one offsite, one offline/immutable, zero recovery errors.

- [ ] I can build a scale-out backup repository.
- [ ] I can add an immutable object capacity tier.
- [ ] I can create a backup copy job for 3-2-1-1-0.
- [ ] I can reason about Veeam Data Cloud Vault.
- [ ] I completed Labs 5.1–5.4 including each negative test.
