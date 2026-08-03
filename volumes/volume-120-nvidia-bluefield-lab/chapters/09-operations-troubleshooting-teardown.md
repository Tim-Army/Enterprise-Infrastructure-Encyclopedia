# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for per-server DPU segmentation.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is DPU segmentation working?"

**Track 1 — Walkthrough.** In DOCA/management: each DPU has the current policy, enforcement is active out-of-band of the host, telemetry shows per-workload flows and denies, and the policy source of truth is intact.

**Track 2 — Walkthrough.**

```bash
for d in web hmi; do echo "== dpu-$d policy =="; sudo ip netns exec dpu-$d nft list chain inet dpu forward 2>/dev/null | grep -E "accept|drop|policy"; done
echo "== workloads have no policy of their own =="; for w in web hmi; do echo -n "$w: "; sudo ip netns exec $w nft list ruleset 2>/dev/null | wc -l; done
sudo dmesg | grep -cE 'DPU-(WEB|HMI)-DENY'
```

**Expected result.** Each DPU holds its policy, the workloads hold none, denies recorded — enforcement out-of-band.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Sanctioned flow blocked | DPU permit wrong 5-tuple | `dpu-X` forward rules |
| Return traffic blocked | `established,related` rule missing in the DPU | DPU chain |
| Lateral flow permitted | permit too broad, or policy in the wrong namespace | DPU rules; where policy lives |
| Workload can disable policy | enforcement placed in the workload namespace | move policy into the DPU namespace |
| No return route | network lacks a route to the workload subnet via the DPU | host `ip route` for the workload subnet |
| Non-DPU server unprotected | no BlueField on that host | coverage |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The defining mistake is placing enforcement **in the workload namespace** (a host-agent model) and believing it is out-of-band — it is not. The policy must live in the DPU namespace, which the workload cannot reach.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
for ns in web hmi dpu-web dpu-hmi db plc; do sudo ip netns del $ns 2>/dev/null; done
sudo ip route del 10.140.1.0/24 2>/dev/null; sudo ip route del 10.140.3.0/24 2>/dev/null
sudo ip link del net 2>/dev/null
echo "teardown complete"
```

**Expected result.** Workload and DPU namespaces, target namespaces, routes, and the network bridge removed.

**Negative test.** Leaving the workload-subnet routes on the host is harmless once the namespaces are gone, but removing them keeps the routing table clean.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Enforce beside the workload, outside its trust boundary.** The DPU policy survives host compromise.
- **Policy in the DPU, never the workload.** If the host can edit it, it is not out-of-band.
- **Zero host-CPU cost.** Enforcement and datapath on the DPU, at line rate.
- **Secure the management plane.** The DPU is tamper-resistant; the plane that programs it must be too.
- **Per-server DPU plus fabric plus host context.** Layer the enforcement locations for coverage and depth.
- **Non-DPU hosts need complementary controls.** Pair with fabric/host controls (Volumes XCIII–CXIX) where there is no DPU.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Out-of-band enforcement (policy in the DPU) internalized.
- [ ] Track 2 namespaces, routes, and bridge removed.
