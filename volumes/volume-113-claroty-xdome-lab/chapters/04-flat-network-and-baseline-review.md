# Chapter 04: The Flat Network and Baseline Review

## Learning Objectives

- Demonstrate the operator-to-database lateral movement on the flat network.
- Understand the critical pitfall: if the attack happens *during* baselining, it becomes "normal".
- Review and curate the baseline so it contains only intended flows.

## The baseline is only as good as the window

The observe-then-enforce model has a trap: a **learned baseline records whatever happened**, including a lateral movement that occurred during the monitoring window. If you enforce that baseline blindly, you bless the attack. Claroty's answer — and this chapter's — is a **review step**: an engineer curates the baseline, confirming each flow is intended before it becomes policy. This chapter reproduces the lateral movement, shows it polluting the baseline, and curates it out.

## Hands-On Lab

### Exercise 4.1 — Reproduce the lateral movement (during monitoring)

**Objective.** Show `hmi → db` succeeding on the flat network — and being observed.

**Track 2 — Walkthrough.** Capture a fresh window in which the attack also happens:

```bash
sudo timeout 20 tcpdump -i any -n 'tcp' -w /tmp/span2.pcap >/dev/null 2>&1 &
sudo ip netns exec web bash -c 'nc -z -w2 10.70.2.20 5432'                 # legitimate
sudo ip netns exec hmi bash -c 'nc -z -w2 10.70.4.40 502'                  # legitimate
sudo ip netns exec hmi bash -c 'nc -z -w2 10.70.2.20 5432 && echo "PIVOT: hmi->db during monitoring"'  # attack
wait
```

**Expected result.** `PIVOT: hmi->db during monitoring` — the operator reaches the database, and because it happened during the window, it will appear in the raw baseline.

**Negative test.** A closed port (`hmi->db:502`) never appears in the baseline because no connection succeeds — the baseline records conversations, so a failed probe does not pollute it, but a *successful* lateral movement does.

**Rollback.** Keep the capture.

### Exercise 4.2 — See the attack in the raw baseline

**Objective.** Prove the naive baseline now includes the lateral flow.

**Track 2 — Walkthrough.**

```bash
sudo tcpdump -nr /tmp/span2.pcap 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0' 2>/dev/null \
  | sed -E 's/.* IP (10\.70[0-9.]*)\.[0-9]+ > (10\.70[0-9.]*)\.([0-9]+):.*/\1 -> \2:\3/' \
  | sort -u | tee /tmp/baseline-raw.txt
```

**Expected result.**

```text
10.70.1.10 -> 10.70.2.20:5432
10.70.3.30 -> 10.70.2.20:5432   <-- the lateral movement, now "baselined"
10.70.3.30 -> 10.70.4.40:502
```

Enforcing this raw baseline would permit the very flow you want to stop.

**Negative test.** Assume a learned baseline is automatically a safe policy. It is not — it is a record of what happened, attacks included. Blindly enforcing it is how observe-then-enforce goes wrong.

**Rollback.** Keep the raw baseline.

### Exercise 4.3 — Curate the baseline

**Objective.** Review each flow and keep only the intended ones.

**Track 1 — Walkthrough.** In xDome an engineer reviews the learned communications and marks each as sanctioned or not; `hmi → db` is rejected as not a legitimate business flow. The curated set becomes the policy.

**Track 2 — Walkthrough.** Remove the unintended flow to produce the curated baseline:

```bash
grep -v '^10.70.3.30 -> 10.70.2.20:5432$' /tmp/baseline-raw.txt > /tmp/baseline.txt
cat /tmp/baseline.txt
```

**Expected result.**

```text
10.70.1.10 -> 10.70.2.20:5432
10.70.3.30 -> 10.70.4.40:502
```

The curated baseline contains only the two intended flows — the same result as monitoring a clean window, reached by review.

**Negative test.** Skipping the review and shipping `baseline-raw.txt` would encode the attack as policy. The human sanction step is not optional.

**Rollback.** Keep the curated `/tmp/baseline.txt`.

## Summary and Completion Checklist

- [ ] The lateral movement reproduced during a monitoring window.
- [ ] The raw baseline shown to include the attack.
- [ ] The baseline curated to only intended flows.
- [ ] The observe-then-enforce review step internalized.
