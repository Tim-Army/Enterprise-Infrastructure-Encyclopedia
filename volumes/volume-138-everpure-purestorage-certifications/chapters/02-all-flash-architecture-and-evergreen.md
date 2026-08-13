# Chapter 02: All-Flash Architecture and the Evergreen Model

## Learning Objectives

- Explain why purpose-built flash differs from SSDs in a legacy array.
- Describe the Evergreen architecture and non-disruptive upgrades.
- Compare owning hardware with the Evergreen//One consumption model.
- Reason about controller redundancy and upgrade sequencing.

## Flash, done deliberately

The first generation of "flash storage" was legacy disk arrays with SSDs substituted in. That works, and it wastes most of what flash offers: the controller software still assumes rotational latency, RAID schemes still assume disk failure characteristics, and the SSD's own controller duplicates work the array is already doing.

Everpure's approach — **DirectFlash** — manages raw flash directly from the array software rather than through commodity SSD firmware. The practical consequences worth knowing:

| Property | Why it follows |
|:---|:---|
| Consistent low latency | The array schedules flash operations globally rather than each drive deciding independently |
| Better endurance | Global wear levelling and garbage collection, rather than per-drive |
| Higher density | No duplicated translation layer |

The exam-relevant point is the principle, not the marketing: **software that knows it is driving flash makes different decisions from software written for disks.**

## Evergreen

**Evergreen** is the architecture and the commercial promise that you never repurchase the array to modernize it. Controllers upgrade, media upgrades, capacity grows — all **non-disruptively**, with the data staying where it is.

That is possible because of the controller design: an array has **two controllers**, either of which can serve all workload. Upgrading one at a time keeps the array online:

1. Fail workload over to controller B.
2. Upgrade controller A; verify.
3. Fail back to A.
4. Upgrade controller B; verify.
5. Return to normal operation.

The rule that follows, and the one operators must respect: **during the upgrade the array is running on a single controller.** Redundancy is temporarily gone, so an upgrade window is not the moment to also perform risky maintenance elsewhere.

## Evergreen//One

**Evergreen//One** is the same architecture consumed as a service: you subscribe to capacity and performance with committed service levels, rather than buying arrays. The vendor owns refresh, and you pay for what you use above a committed baseline.

| | **Own the hardware** | **Evergreen//One (subscription)** |
|:---|:---|:---|
| Cost shape | Capital, up front | Operating, ongoing |
| Capacity planning | You buy ahead for growth | Grow as needed above a commitment |
| Refresh | Your project | Vendor's obligation |
| Fits | Stable, predictable demand; capital-friendly finance | Uncertain growth; opex preference |

The honest comparison is not "subscription good, capital bad" — it depends on how predictable your growth is and how your organization finances infrastructure. Buying ahead for three years of growth means paying for idle capacity; subscribing means paying a margin for someone else to carry that risk.

## Hands-On Lab

Python models the architecture. **Cost:** none.

### Lab 2.1 — Non-disruptive upgrade sequencing

**Objective:** Model the controller failover sequence and the redundancy gap.

```bash
python3 - <<'EOF'
state = {"A":{"role":"active","version":"6.4"}, "B":{"role":"active","version":"6.4"}}
TARGET = "6.5"

def show(step, note):
    up = [c for c,v in state.items() if v["role"] != "upgrading"]
    redundancy = "REDUNDANT" if len(up) == 2 else "*** SINGLE CONTROLLER — no redundancy ***"
    versions = {c: v["version"] for c, v in state.items()}
    print(f"{step:38} {versions}  [{redundancy}]")
    if note: print(f"{'':38} {note}")

show("start", "both controllers active, serving I/O")
state["A"]["role"] = "upgrading"
show("fail over to B, upgrade A", "workload continues on B; array is EXPOSED to a B failure")
state["A"].update(role="active", version=TARGET)
show("A back online at 6.5", "redundancy restored, mixed versions temporarily")
state["B"]["role"] = "upgrading"
show("fail over to A, upgrade B", "workload on A; EXPOSED again")
state["B"].update(role="active", version=TARGET)
show("complete", "both at 6.5, no downtime, no data moved")

print("\nData never moved and hosts never lost access — that is what 'non-disruptive' means.")
print("But note the two windows on a SINGLE controller. Do not schedule other risky work then,")
print("and do not start an upgrade while a controller is already faulted.")
EOF
```

**Expected result:** The array traverses the upgrade with continuous service, passing through two windows where it runs on one controller. The operational caution in the closing lines is the part that matters in practice: non-disruptive does not mean risk-free, and the temporary loss of redundancy is exactly why upgrades are scheduled rather than performed casually.

**Negative test:** Beginning an upgrade with one controller already in a degraded state — the failover has nowhere to go, and a "non-disruptive" procedure becomes an outage.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Own versus subscribe

**Objective:** Compare cost shapes against growth uncertainty.

```bash
python3 - <<'EOF'
def owned(capex, years, growth_tb_per_year, bought_tb, cost_per_tb):
    over_provisioned = bought_tb - growth_tb_per_year * years
    return {
        "model":"owned",
        "upfront": capex,
        "idle_capacity_tb": max(0, over_provisioned),
        "note": ("bought ahead for growth — idle capacity is paid for from day one"
                 if over_provisioned > 0 else "UNDER-provisioned; a mid-life purchase is required"),
    }

def subscription(committed_tb, rate_per_tb_year, years, actual_tb_per_year):
    total = sum(max(committed_tb, actual_tb_per_year * y) * rate_per_tb_year for y in range(1, years+1))
    return {"model":"Evergreen//One", "upfront":0, "total_over_term":total,
            "note":"pay above a commitment as you grow; vendor carries refresh risk"}

print("Scenario A — predictable growth (20 TB/yr, confident):")
print("  ", owned(capex=300000, years=3, growth_tb_per_year=20, bought_tb=60, cost_per_tb=0))
print("  ", subscription(committed_tb=20, rate_per_tb_year=1800, years=3, actual_tb_per_year=20))
print("\nScenario B — uncertain growth (planned 20 TB/yr, actual 5 TB/yr):")
print("  ", owned(capex=300000, years=3, growth_tb_per_year=5, bought_tb=60, cost_per_tb=0))
print("  ", subscription(committed_tb=20, rate_per_tb_year=1800, years=3, actual_tb_per_year=5))
print("\nPredictable growth favors owning: you use what you bought.")
print("Uncertain growth is where subscription earns its margin — in Scenario B the owned array")
print("carries 45 TB of idle capacity paid for up front, for three years.")
EOF
```

**Expected result:** With predictable growth the owned array is fully used; with growth at a quarter of forecast it carries 45 TB idle for the whole term. The framing in the closing lines is the honest one — the subscription's premium buys **transfer of forecasting risk**, which is worth paying when your forecast is genuinely uncertain and is waste when it is not.

**Negative test:** Choosing a consumption model purely to move spend from capital to operating budget — the accounting treatment changes and the underlying economics do not, so a confident, stable workload usually pays more.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Controller sizing and failover headroom

**Objective:** Check that one controller can carry the load.

```bash
python3 - <<'EOF'
def assess(name, workload_pct_of_one_controller):
    # Two controllers; during upgrade or failure ONE must carry everything.
    single = workload_pct_of_one_controller
    if single > 100:
        verdict = f"CANNOT FAIL OVER — one controller would be at {single}% (impossible); expect severe degradation"
    elif single > 85:
        verdict = f"TIGHT — {single}% on one controller; latency will rise noticeably during upgrades"
    else:
        verdict = f"healthy — {single}% on one controller, failover is transparent"
    print(f"{name:22} normal load {single/2:5.1f}% per controller | on ONE controller {single:5.1f}% -> {verdict}")

assess("array-dev",    40)
assess("array-prod-1", 120)
assess("array-prod-2", 90)
print("\nSizing rule: a two-controller array must run its full workload on ONE controller during")
print("upgrades and failures. If normal load exceeds ~50% per controller, you have no real")
print("failover headroom — the array is sized for the good day, not the bad one.")
EOF
```

**Expected result:** The development array fails over transparently, one production array is tight, and another cannot fail over at all. The sizing rule stated at the end is the one people get wrong by treating both controllers' capacity as usable: in an active/active pair, **the usable steady-state capacity is one controller's worth**, because the other must be able to absorb everything.

**Negative test:** Sizing to 80% utilization across both controllers because "we have two" — the first upgrade or controller fault leaves 160% of one controller's capacity demanded from it, and the array degrades badly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Purpose-built flash (DirectFlash) distinguished from SSDs in a legacy array.
- [ ] Non-disruptive upgrade sequencing modeled, including the single-controller exposure windows.
- [ ] Evergreen//One compared with ownership on growth predictability rather than accounting treatment.
- [ ] Controller headroom sized so one controller can carry the full workload.
