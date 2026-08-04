# Chapter 05: Data Reduction and Efficiency

## Learning Objectives

- Explain deduplication, compression, and thin provisioning as distinct mechanisms.
- Calculate a data-reduction ratio and know what it excludes.
- Recognize which workloads reduce well and which do not.
- Plan capacity against realistic ratios rather than marketing figures.

## Three different mechanisms

They are frequently lumped together and they do different things:

| Mechanism | What it removes | Where the saving comes from |
|:---|:---|:---|
| **Deduplication** | Identical blocks stored more than once | Repetition *across* data — 500 VMs from one template |
| **Compression** | Redundancy *within* a block | Patterns inside the data itself |
| **Thin provisioning** | Allocated-but-unwritten space | Provisioning ahead of actual use |

The distinction matters because they respond to different data. Encrypted data compresses and deduplicates poorly (it is statistically random by design — see [Volume CXXXIII, Chapter 04](../../volume-133-commvault-certifications/chapters/04-deduplication-and-efficiency.md)); already-compressed media does not compress further; a thousand near-identical virtual machines deduplicate spectacularly.

## Reading a ratio honestly

Vendors quote **total efficiency** figures that combine data reduction with thin provisioning, which is where confusion starts:

- **Data reduction ratio** = data written ÷ physical space used. This is deduplication and compression.
- **Total efficiency** additionally counts **thin provisioning** — space you provisioned and never wrote.

Thin provisioning "savings" are real in the sense that you did not need the space, and unhelpful for capacity planning, because a large ratio may simply mean somebody over-provisioned volumes. **Plan against the data reduction ratio**; treat total efficiency as marketing arithmetic.

## What reduces, and what does not

| Workload | Typical behavior |
|:---|:---|
| Virtual desktops from a common image | Deduplicates extremely well |
| Virtual servers | Deduplicates well |
| Databases | Compresses reasonably; deduplicates modestly |
| Already-compressed media (video, images) | Almost no further reduction |
| Encrypted data | **Essentially none** |
| Pre-deduplicated backups | Little left to remove |

The practical consequence: **a ratio observed on one workload does not transfer to another.** A 5:1 ratio from a virtual-desktop estate says nothing useful about the array you are sizing for encrypted archives.

## Hands-On Lab

Python models data reduction. **Cost:** none.

### Lab 5.1 — Ratios by workload

**Objective:** Show how much the workload determines the outcome.

```bash
python3 - <<'EOF'
workloads = [
  {"name":"VDI (1000 desktops, one image)","logical_tb":100,"dedup":8.0,"compress":1.6},
  {"name":"Virtual servers",               "logical_tb":100,"dedup":3.0,"compress":1.8},
  {"name":"Oracle database",               "logical_tb":100,"dedup":1.2,"compress":2.5},
  {"name":"Video archive (pre-compressed)","logical_tb":100,"dedup":1.05,"compress":1.02},
  {"name":"Encrypted backups",             "logical_tb":100,"dedup":1.0,"compress":1.0},
]
print(f"{'workload':38}{'dedup':>8}{'compress':>10}{'total':>8}{'physical TB':>13}")
for w in workloads:
    total = w["dedup"] * w["compress"]
    physical = w["logical_tb"] / total
    print(f"{w['name']:38}{w['dedup']:>7.2f}x{w['compress']:>9.2f}x{total:>7.2f}x{physical:>12.1f}")
print("\nSame 100 TB logical in every row; physical footprint ranges from 7.8 TB to 100 TB.")
print("A ratio measured on VDI tells you NOTHING about sizing for encrypted backups —")
print("and encrypted data is statistically random by design, so there is nothing to remove.")
EOF
```

**Expected result:** Identical logical capacity lands between 7.8 TB and 100 TB physical depending entirely on workload. The warning is the practical one: reduction ratios are workload properties, not array properties, so quoting a ratio without naming the data it came from is meaningless.

**Negative test:** Sizing a new array using the ratio observed on an existing one with different data — a VDI-derived 12:1 applied to a database estate under-provisions by roughly a factor of four.

**Cleanup:** None.

### Lab 5.2 — Data reduction versus total efficiency

**Objective:** Separate the two numbers and plan on the right one.

```bash
python3 - <<'EOF'
provisioned_tb = 500      # volumes created
written_tb     = 120      # actually written by hosts
physical_tb    = 40       # consumed on the array

data_reduction = written_tb / physical_tb
total_efficiency = provisioned_tb / physical_tb

print(f"provisioned (thin) : {provisioned_tb} TB")
print(f"written by hosts   : {written_tb} TB")
print(f"physical used      : {physical_tb} TB\n")
print(f"DATA REDUCTION ratio : {data_reduction:5.2f}:1   (dedup + compression — plan with THIS)")
print(f"TOTAL EFFICIENCY     : {total_efficiency:5.2f}:1   (adds thin provisioning)")

print("\nThe 12.5:1 headline is largely thin provisioning — space nobody has written yet.")
print("If those volumes fill up, the thin saving evaporates and only the 3:1 reduction remains.")
print("\nCapacity planning question: if the 500 TB provisioned were fully written at 3:1,")
print(f"you would need {provisioned_tb/data_reduction:.0f} TB physical — not {physical_tb} TB.")
print("Plan for the written case, or a growing estate quietly walks into a full array.")
EOF
```

**Expected result:** A 3:1 data-reduction ratio sits behind a 12.5:1 total-efficiency headline, and fully written volumes would need 167 TB rather than the current 40 TB. That gap is the capacity-planning trap: thin provisioning defers the requirement rather than removing it, and an array sized on total efficiency runs out when the provisioned volumes fill.

**Negative test:** Reporting total efficiency to finance as the sizing basis — the array looks four times more capable than it is, and the shortfall appears as an emergency purchase.

**Cleanup:** None.

### Lab 5.3 — Capacity forecast against realistic ratios

**Objective:** Forecast runway using per-workload ratios.

```bash
python3 - <<'EOF'
ARRAY_PHYSICAL_TB = 100
workloads = [
  {"name":"VDI",        "logical_now":60, "growth_tb_month":2,  "ratio":10.0},
  {"name":"databases",  "logical_now":40, "growth_tb_month":3,  "ratio":2.5},
  {"name":"archives",   "logical_now":20, "growth_tb_month":5,  "ratio":1.05},
]
def physical_at(month):
    return sum((w["logical_now"] + w["growth_tb_month"]*month) / w["ratio"] for w in workloads)

print(f"array physical capacity: {ARRAY_PHYSICAL_TB} TB\n")
print(f"{'month':>6}{'physical used TB':>18}{'headroom':>11}")
full_at = None
for m in range(0, 37, 6):
    used = physical_at(m)
    head = ARRAY_PHYSICAL_TB - used
    print(f"{m:>6}{used:>18.1f}{head:>11.1f}")
    if head < 0 and full_at is None: full_at = m
for m in range(0, 60):
    if physical_at(m) > ARRAY_PHYSICAL_TB:
        full_at = m; break
print(f"\nArray fills at about month {full_at}.")
print("\nNote which workload drives it: ARCHIVES grow fastest (5 TB/mo) AND reduce worst (1.05:1),")
print("so they consume ~4.8 TB physical per month. VDI grows 2 TB/mo but at 10:1 costs only 0.2 TB.")
print("Growth in POORLY-REDUCING data is what fills arrays — forecast per workload, not in aggregate.")
EOF
```

**Expected result:** The array fills at roughly month 15, driven overwhelmingly by the archive workload — fastest-growing *and* least reducible, consuming about 24 times the physical space per logical terabyte that VDI does. Forecasting in aggregate would have hidden that; forecasting per workload identifies exactly which data to move elsewhere.

**Negative test:** Forecasting with a single blended ratio — the blend is dominated by whichever workload is largest today, and it mis-predicts as the mix shifts.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Deduplication, compression, and thin provisioning distinguished by what each removes.
- [ ] Reduction ratios understood as workload properties, not array properties.
- [ ] Data reduction separated from total efficiency, with planning based on the former.
- [ ] Capacity forecast per workload, identifying poorly-reducing growth as the driver.
