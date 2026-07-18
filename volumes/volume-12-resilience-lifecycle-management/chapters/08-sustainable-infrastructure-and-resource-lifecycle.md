# Chapter 8: Sustainable Infrastructure and Resource Lifecycle

## Learning Objectives

- Calculate and interpret Power Usage Effectiveness (PUE) and explain its limitations as a sole efficiency metric.
- Distinguish operational carbon from embodied carbon and explain why a "replace it, it's more efficient" decision can be carbon-negative in the near term.
- Apply the circular hardware lifecycle (reduce, reuse, refurbish, recycle) to enterprise hardware refresh decisions.
- Right-size infrastructure using observed utilization data and explain right-sizing's dual role as both a cost and a sustainability lever.
- Design carbon-aware or time-shifted workload scheduling for deferrable batch workloads.
- Build an asset lifecycle tracking process that captures sustainability-relevant data (utilization, age, refresh eligibility) alongside the CMDB fields established in Volume I.

## Theory and Architecture

### Why Sustainability Belongs in a Resilience and Lifecycle Volume

Sustainable infrastructure practice sits naturally alongside the rest of this volume because it shares its core discipline: measure the actual resource consumed against actual need, and manage the full lifecycle of an asset deliberately rather than by default. An over-provisioned, never-right-sized fleet is not only a cost problem — it is wasted embodied carbon and wasted energy sustained indefinitely because nobody revisited a sizing decision made at launch, the same "silent capacity drift" anti-pattern named in Chapter 1, viewed through a different lens. Sustainability and resilience occasionally trade off directly (extra redundant capacity has both a cost and a carbon cost) and this chapter treats that trade-off explicitly rather than treating sustainability as a purely separate initiative layered on top of infrastructure engineering.

### Data Center Efficiency Metrics

The most widely used data center efficiency metric is **Power Usage Effectiveness (PUE)**:

```text
PUE = Total Facility Energy / IT Equipment Energy
```

A PUE of 1.0 is the theoretical ideal (all facility energy goes directly to IT equipment, none to cooling, lighting, or power conversion losses); real-world facilities typically range from roughly 1.1 (highly efficient, purpose-built hyperscale facilities) to 2.0 or higher (older or poorly optimized facilities). Related metrics extend the same idea to other resources: **Water Usage Effectiveness (WUE)** measures water consumed per unit of IT energy, relevant for facilities using evaporative cooling, and **Carbon Usage Effectiveness (CUE)** measures carbon emissions per unit of IT energy, which depends heavily on the carbon intensity of the local electrical grid rather than the facility's engineering alone.

PUE's central limitation is that it measures efficiency of energy delivery to IT equipment, not whether that IT equipment is doing useful work — a facility with an excellent PUE running a fleet of severely underutilized, idle servers is efficiently delivering power to waste. PUE should be read alongside utilization metrics, not as a standalone sustainability scorecard, and should never be "improved" by simply reducing the denominator's apparent scope (excluding certain load types from IT equipment energy) without disclosing the change — a well-documented practice of PUE reporting manipulation that undermines the metric's comparability.

### Operational Carbon vs. Embodied Carbon

Two distinct carbon costs apply to any piece of infrastructure:

- **Operational carbon** — the emissions associated with the electricity consumed while the equipment runs, which vary continuously with the carbon intensity of the electricity source.
- **Embodied carbon** — the emissions associated with manufacturing, transporting, and eventually disposing of the equipment, incurred largely up front (and again at end of life) regardless of how the equipment is used afterward.

This distinction directly shapes refresh decisions: replacing hardware purely for a marginal operational-efficiency gain can be carbon-negative in the near term if it discards embodied carbon that has not yet been "paid off" by the operational savings — the equivalent of a payback-period calculation, but for carbon rather than dollars. A rough framework:

```text
Carbon payback period (years) =
    Embodied carbon of new equipment (kg CO2e)
    / Annual operational carbon savings vs. keeping old equipment (kg CO2e/year)

If the payback period exceeds the equipment's remaining useful life, an early
refresh is very likely carbon-negative over that life, even if it reduces
the electricity bill.
```

This does not mean equipment should never be refreshed early — a security-driven, EOL-driven refresh (Chapter 6, Chapter 7) is often necessary regardless of the carbon payback calculation — but a refresh justified purely on operational-efficiency or cost grounds should include this calculation rather than assuming newer is automatically better for total lifecycle impact.

### The Circular Hardware Lifecycle

Circular economy principles reframe the hardware lifecycle away from a linear "buy, use, discard" model toward stages that each extend useful life before final disposal:

1. **Reduce** — right-size and consolidate before acquiring new capacity at all; the least-carbon-intensive unit of compute is the one never purchased because existing capacity was fully utilized instead.
2. **Reuse** — redeploy existing hardware for a different, less demanding workload (a retired production server repurposed for a development or test environment) rather than retiring it outright.
3. **Refurbish** — component-level repair or upgrade (replacing drives, adding memory) to extend a system's productive life beyond its original refresh cycle.
4. **Recycle** — at true end of life, route hardware through a certified electronics recycler that recovers materials responsibly, connecting directly to the secure-decommissioning practices in Chapter 9.

Each stage deferred is embodied carbon amortized over a longer useful life, and a mature asset lifecycle program measures and reports how much equipment moves through reuse and refurbishment rather than treating "recycle" as the only stage worth tracking.

## Design Considerations

### Right-Sizing as a Dual-Purpose Lever

Right-sizing — matching provisioned capacity to observed demand rather than a conservative guess made at launch — reduces both cost and energy consumption simultaneously, making it one of the few sustainability levers with no inherent trade-off against the resilience goals elsewhere in this volume, provided redundancy requirements from Chapter 1 are respected during right-sizing rather than eroded by it. A right-sizing review should distinguish genuinely idle or over-provisioned capacity from capacity intentionally held as HA or DR headroom (Chapters 3 and 4) — the latter looks "wasted" by a naive utilization metric but is a deliberate resilience investment, not waste, and right-sizing automation must be able to tell the two apart or it will silently degrade availability while chasing an efficiency metric.

### Redundancy vs. Efficiency Trade-off

Every additional unit of standby or redundant capacity carries an energy and embodied-carbon cost proportional to its size, independent of whether it is ever called upon to absorb a failure. This is not an argument against redundancy — Chapter 1 already established that redundancy investment should match criticality tier — but it is an argument for being deliberate: a Tier 3 service over-provisioned to a Tier 0 redundancy level pays a sustainability cost with no corresponding resilience benefit, exactly mirroring the cost argument made in Chapter 1 for the same scenario.

### Carbon-Aware and Time-Shifted Workload Placement

Not all workloads are equally deferrable. Batch jobs, non-urgent data processing, and other work without a tight latency requirement can be scheduled to run when the carbon intensity of the local electrical grid is lowest (commonly when renewable generation — solar, wind — is highest), a practice known as carbon-aware or carbon-shifted scheduling. This requires the workload's own deferrability to be classified explicitly — attempting to time-shift a latency-sensitive, Tier 0/1 service is not appropriate and would directly conflict with its RTO/availability requirements from Chapters 1 through 3; carbon-aware scheduling is a Tier 3/4, deferrable-batch-workload technique, not a general-purpose infrastructure practice.

### Sustainable Procurement

Procurement decisions carry lifecycle sustainability consequences before a single watt is consumed: vendor take-back and recycling programs, manufacturer-published embodied carbon and energy-efficiency disclosures, repairability and upgradeability of purchased hardware (a system designed for component-level upgrades extends its own useful life more easily than one that is not), and supplier environmental and labor practices all belong in a sustainability-aware procurement evaluation, alongside the traditional cost and performance criteria.

## Implementation and Automation

### PUE Calculation

```python
def calculate_pue(total_facility_energy_kwh: float, it_equipment_energy_kwh: float) -> float:
    """Return PUE for a given measurement period. Lower is better; 1.0 is ideal."""
    if it_equipment_energy_kwh <= 0:
        raise ValueError("IT equipment energy must be greater than zero")
    return round(total_facility_energy_kwh / it_equipment_energy_kwh, 3)

# Example: a facility consuming 1,450,000 kWh total against 1,000,000 kWh
# delivered to IT equipment in the same period.
print(calculate_pue(1_450_000, 1_000_000))  # 1.45
```

Compute PUE over a consistent measurement period (commonly trailing 12 months, to smooth out seasonal cooling-load variation) rather than a single snapshot, which can be misleadingly favorable during mild weather and misleadingly poor during extreme conditions.

### Right-Sizing Candidate Identification

```python
def find_rightsizing_candidates(instances: list[dict], cpu_threshold_pct: float = 20.0,
                                  min_days_observed: int = 14) -> list[dict]:
    """Flag instances with sustained low utilization as right-sizing
    candidates, excluding those tagged as intentional HA/DR standby capacity."""
    candidates = []
    for inst in instances:
        if inst.get("role") in ("ha-standby", "dr-standby"):
            continue  # deliberate redundancy headroom, not waste
        if inst["days_observed"] < min_days_observed:
            continue  # insufficient data to judge sustained utilization
        if inst["avg_cpu_pct"] < cpu_threshold_pct:
            candidates.append({
                "instance_id": inst["instance_id"],
                "avg_cpu_pct": inst["avg_cpu_pct"],
                "current_size": inst["size"],
                "recommended_action": "downsize or consolidate",
            })
    return candidates
```

Explicitly excluding tagged HA/DR standby capacity in this function is the implementation of the design consideration above — an automated right-sizing tool that cannot distinguish deliberate redundancy from genuine waste will, if acted upon without review, quietly undermine the resilience posture built up over the rest of this volume.

### Carbon-Aware Batch Scheduling

```yaml
# carbon-aware-schedule.yaml
job_id: nightly-analytics-rollup
deferrable: true
latest_completion_deadline: "06:00"
carbon_intensity_source: "grid-intensity-api.internal.example/region/us-central"
scheduling_policy: "run within the lowest-carbon-intensity 3-hour window before deadline"
```

```python
def select_run_window(hourly_intensity: dict[str, float], deadline_hour: int, window_hours: int = 3) -> int:
    """Return the start hour of the lowest-average-carbon-intensity
    window that still completes before the deadline."""
    best_start, best_avg = None, float("inf")
    for start in range(0, deadline_hour - window_hours + 1):
        window = [hourly_intensity[str(h)] for h in range(start, start + window_hours)]
        avg = sum(window) / len(window)
        if avg < best_avg:
            best_avg, best_start = avg, start
    return best_start
```

### Asset Lifecycle Tracking With Sustainability Fields

```yaml
# asset-lifecycle-register.yaml
- asset_id: srv-compute-0231
  acquired_date: "2022-03-15"
  expected_refresh_date: "2027-03-15"
  role: production
  avg_utilization_pct_trailing_90d: 61
  refurbish_eligible: true
  disposition_at_refresh: "refurbish-and-redeploy-to-dev"

- asset_id: srv-compute-0198
  acquired_date: "2019-11-02"
  expected_refresh_date: "2024-11-02"
  role: ha-standby
  avg_utilization_pct_trailing_90d: 4
  refurbish_eligible: false
  disposition_at_refresh: "certified-recycle"
```

Extending the CMDB-style asset record from Volume I with utilization and disposition fields lets the same inventory that tracks configuration items also drive right-sizing review, refresh scheduling, and the reuse/refurbish/recycle decision at end of life — one authoritative record rather than a separate, easily-out-of-sync sustainability spreadsheet.

## Validation and Troubleshooting

### Validating Sustainability Claims

- Confirm PUE is calculated over a consistent, disclosed measurement boundary and period; compare year-over-year trends rather than a single isolated figure, and be skeptical of a PUE improvement that coincides with a change in what is counted as "IT equipment energy" rather than an actual efficiency improvement.
- Confirm right-sizing recommendations have been cross-checked against the HA/DR role tagging described above before any capacity is actually reduced — validate on a sample before trusting the automation at fleet scale.
- Confirm carbon-aware scheduling is applied only to workloads explicitly classified as deferrable; audit that no Tier 0/1 service has been inadvertently included in a time-shifted schedule.

### Common Failure Modes

| Symptom | Likely Cause |
| --- | --- |
| PUE reported as excellent but utilization is very low | PUE measures delivery efficiency, not IT productivity; the facility is efficiently powering idle equipment |
| Right-sizing automation reduces capacity on an HA pair, causing a subsequent outage | Standby/redundant role tagging missing or not honored by the automation |
| Carbon-aware scheduling delays a job past a business-critical deadline | Deferrability was assumed rather than confirmed with the process owner; deadline field was set too loosely |
| Early hardware refresh reduces the electricity bill but net sustainability reporting worsens | Embodied carbon of the replacement was not accounted for; carbon payback period exceeded remaining useful life |
| Asset register shows systems well past expected refresh date with no action taken | No forcing function or review cadence tied to the register, mirroring the same "register exists but nothing gets prioritized" failure from Chapter 7 |

### Troubleshooting Utilization Data Quality

Right-sizing and PUE conclusions are only as good as the underlying utilization data. Before acting on a right-sizing recommendation, verify the observation window is long enough to capture cyclical peaks (end-of-month batch processing, seasonal traffic) that a short window would miss, and verify the metric itself (commonly average CPU) is not masking a different bottleneck resource (memory, I/O, network) that would make a downsizing recommendation actively harmful despite low CPU utilization.

## Security and Best Practices

- Extend the secure decommissioning practices from Chapter 9 to every hardware disposition path in the circular lifecycle, not only final recycling — a reused or refurbished system redeployed to a lower-trust environment (production hardware repurposed for development) must still have its data sanitized to the same standard as a system going to disposal.
- Vet electronics recyclers and refurbishment partners for data destruction certification and chain-of-custody practices; a recycling vendor that cannot provide a certificate of data destruction is a data-exfiltration risk regardless of its environmental credentials.
- Do not let carbon-aware time-shifting introduce an unreviewed dependency on an external carbon-intensity data API becoming a new operational SPOF for otherwise-independent batch processing; apply the same dependency-mapping discipline from Chapter 1 to this new external dependency.
- Review right-sizing and asset-disposition automation changes through the same change-management process as any other production infrastructure change (Volume I, Chapter 8); a script that silently resizes or redeploys hardware without change review can just as easily cause an outage as manual misconfiguration.
- Report sustainability metrics (PUE, refresh rates, reuse/refurbish/recycle proportions) with the same rigor and auditability as financial or security metrics; unverified or self-reported figures used externally (in ESG disclosures) carry reputational and, increasingly, regulatory risk if later found inaccurate.

## References and Knowledge Checks

### References

- [Chapter 1](01-resilience-engineering-and-critical-service-design.md) for the redundancy-vs-cost trade-off this chapter extends to redundancy-vs-carbon.
- [Chapter 9](09-retirement-decommissioning-and-lifecycle-governance.md) for the secure data sanitization practices that apply across every hardware disposition path in this chapter.
- The Green Grid, *PUE: A Comprehensive Examination of the Metric*, for PUE methodology and known reporting pitfalls.
- ISO/IEC 30134 series, data center resource-efficiency metrics (PUE, WUE, and related standards).
- Volume I, Chapter 8, *Infrastructure Lifecycle Management*, for the CMDB and asset lifecycle foundation this chapter extends with sustainability fields.

### Knowledge Checks

1. Explain why PUE alone is an incomplete sustainability metric and describe what additional data should accompany it.
2. Given an embodied carbon figure and an annual operational carbon savings figure, walk through the carbon payback period calculation and explain what it means if the payback period exceeds the equipment's remaining useful life.
3. Why must right-sizing automation distinguish HA/DR standby capacity from genuinely idle capacity, and what happens if it does not?
4. Describe the four stages of the circular hardware lifecycle (reduce, reuse, refurbish, recycle) and give an infrastructure-specific example of each.
5. Explain why carbon-aware time-shifted scheduling is appropriate for some workloads but not others, using the criticality tiers from Chapter 1.

## Hands-On Lab

### Lab: PUE Calculation and Redundancy-Aware Right-Sizing

**Objective:** Calculate PUE from sample facility data, run a right-sizing scan against a sample fleet, and confirm the scan correctly excludes tagged HA/DR standby capacity from its recommendations.

**Prerequisites:**

- `python3` (3.11+) with `pyyaml` (`pip install pyyaml`).

**Procedure:**

1. Create a working directory:

   ```bash
   mkdir -p ~/labs/resilience-ch8 && cd ~/labs/resilience-ch8
   ```

2. Save the `calculate_pue` function from this chapter as `pue.py` and run it against two sample periods:

   ```python
   def calculate_pue(total_facility_energy_kwh, it_equipment_energy_kwh):
       if it_equipment_energy_kwh <= 0:
           raise ValueError("IT equipment energy must be greater than zero")
       return round(total_facility_energy_kwh / it_equipment_energy_kwh, 3)

   print("Q1 PUE:", calculate_pue(1_450_000, 1_000_000))
   print("Q3 PUE:", calculate_pue(1_620_000, 1_000_000))
   ```

   ```bash
   python3 pue.py
   ```

   **Expected Result:** `Q1 PUE: 1.45` and `Q3 PUE: 1.62`, illustrating a seasonal cooling-load increase in the summer quarter against identical IT load — the reason a single-period PUE snapshot can be misleading.

3. Create `fleet.yaml` with six sample instances, three production, two HA/DR standby, one clearly idle production instance:

   ```yaml
   - instance_id: web-01
     role: production
     avg_cpu_pct: 55
     days_observed: 30
     size: large
   - instance_id: web-02
     role: production
     avg_cpu_pct: 12
     days_observed: 30
     size: large
   - instance_id: batch-01
     role: production
     avg_cpu_pct: 8
     days_observed: 21
     size: xlarge
   - instance_id: db-standby-01
     role: ha-standby
     avg_cpu_pct: 3
     days_observed: 30
     size: xlarge
   - instance_id: dr-replica-01
     role: dr-standby
     avg_cpu_pct: 2
     days_observed: 30
     size: xlarge
   - instance_id: web-03
     role: production
     avg_cpu_pct: 18
     days_observed: 5
     size: medium
   ```

4. Save `find_rightsizing_candidates` from this chapter as `rightsize.py` with a driver that loads `fleet.yaml` and prints candidates:

   ```python
   import yaml

   def find_rightsizing_candidates(instances, cpu_threshold_pct=20.0, min_days_observed=14):
       candidates = []
       for inst in instances:
           if inst.get("role") in ("ha-standby", "dr-standby"):
               continue
           if inst["days_observed"] < min_days_observed:
               continue
           if inst["avg_cpu_pct"] < cpu_threshold_pct:
               candidates.append({
                   "instance_id": inst["instance_id"],
                   "avg_cpu_pct": inst["avg_cpu_pct"],
                   "current_size": inst["size"],
                   "recommended_action": "downsize or consolidate",
               })
       return candidates

   fleet = yaml.safe_load(open("fleet.yaml"))
   for c in find_rightsizing_candidates(fleet):
       print(c)
   ```

5. Run the scan:

   ```bash
   python3 rightsize.py
   ```

**Expected Result:** The scan flags exactly `web-02` and `batch-01` as right-sizing candidates. It correctly excludes `db-standby-01` and `dr-replica-01` despite their very low CPU utilization (deliberate redundancy headroom, not waste), and excludes `web-03` despite low utilization because it has fewer than 14 days of observed data.

**Negative Test:** Remove the `role` field entirely from `db-standby-01` in `fleet.yaml` (simulating an untagged standby instance) and rerun the scan. Confirm `db-standby-01` now incorrectly appears as a right-sizing candidate — demonstrating exactly the failure mode described in this chapter's Validation section: automation that cannot distinguish deliberate redundancy from waste will recommend reducing HA capacity if the underlying data is not properly tagged. Restore the `role: ha-standby` field afterward and confirm the candidate list returns to its expected state.

**Cleanup:**

```bash
cd ~ && rm -rf ~/labs/resilience-ch8
```

No shared or production systems were modified; all data was a local YAML fixture.

## Summary and Completion Checklist

Sustainable infrastructure practice extends the same discipline this volume has applied to availability and cost throughout: measure actual consumption against actual need, and manage every stage of an asset's lifecycle deliberately. PUE and related efficiency metrics describe delivery efficiency, not utilization, and must be read alongside right-sizing data that itself must be redundancy-aware to avoid silently eroding the resilience investments from earlier chapters. The embodied-versus-operational carbon distinction reframes "replace it, it's more efficient" as a calculation rather than an assumption, and the circular hardware lifecycle (reduce, reuse, refurbish, recycle) extends useful asset life before final disposition — which Chapter 9 covers in full, including the secure data sanitization every disposition path in this chapter ultimately depends on.

**Completion checklist:**

- [ ] Can calculate PUE from facility and IT equipment energy figures and explain its limitations as a standalone metric.
- [ ] Can distinguish operational carbon from embodied carbon and apply a carbon payback period calculation to a refresh decision.
- [ ] Can describe the four stages of the circular hardware lifecycle with an infrastructure-specific example of each.
- [ ] Implemented a right-sizing scan that correctly excludes tagged HA/DR standby capacity from its recommendations.
- [ ] Designed a carbon-aware scheduling approach limited to explicitly deferrable workloads.
- [ ] Understands why redundancy and sustainability trade off directly, and how criticality tiering from Chapter 1 resolves that trade-off.
