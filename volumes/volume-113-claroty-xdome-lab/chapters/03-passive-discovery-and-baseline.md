# Chapter 03: Passive Discovery and the Baseline

## Learning Objectives

- Passively discover the assets on the segment without touching them.
- Build a communication baseline — the matrix of who talks to whom, on what port.
- Understand why a *learned* baseline is the foundation of Claroty-style segmentation.

## You cannot segment what you cannot see

OT networks are full of devices no one has an inventory for. Claroty's first job is **passive discovery**: from a mirror of the traffic it fingerprints every asset and records every conversation, with zero risk to fragile equipment. The output is an **asset inventory** and a **communication baseline** — and that baseline is what the segmentation policy will be derived from. This chapter builds both on Track 2 by capturing traffic and reducing it to a flow matrix.

## Hands-On Lab

### Exercise 3.1 — Discover the assets passively

**Objective.** Enumerate the assets from observed traffic, not by scanning them.

**Track 1 — Walkthrough.** xDome fingerprints assets from the SPAN feed — MACs, IPs, vendors, protocols, firmware where visible — and lists them in the asset inventory, all passively.

**Track 2 — Walkthrough.** Generate some traffic, capture it passively on the host, and derive the asset list from the addresses seen (never by probing the devices):

```bash
# start a passive capture of inter-zone traffic on the host
sudo timeout 20 tcpdump -i any -n 'tcp' -w /tmp/span.pcap >/dev/null 2>&1 &
# meanwhile, normal operations happen
sudo ip netns exec web bash -c 'nc -z -w2 10.70.2.20 5432' ; sleep 1
sudo ip netns exec hmi bash -c 'nc -z -w2 10.70.4.40 502'  ; sleep 1
wait
# assets = distinct addresses observed
sudo tcpdump -nr /tmp/span.pcap 2>/dev/null | grep -oE '10\.70\.[0-9]+\.[0-9]+' | sort -u
```

**Expected result.** The four asset addresses (10.70.1.10, 10.70.2.20, 10.70.3.30, 10.70.4.40) appear — discovered purely from traffic, with nothing sent to the devices.

**Negative test.** An active port scan of the PLC could crash a fragile controller — the reason OT discovery must be passive. This lab never scans the devices; it only listens.

**Rollback.** Keep the capture.

### Exercise 3.2 — Build the communication baseline

**Objective.** Reduce the capture to a who-talks-to-whom-on-what-port matrix.

**Track 1 — Walkthrough.** xDome continuously maintains the baseline: for each pair of assets, the protocols and ports normally used, learned over a monitoring window.

**Track 2 — Walkthrough.** Extract source → destination:port flows from the capture:

```bash
sudo tcpdump -nr /tmp/span.pcap 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0' 2>/dev/null \
  | sed -E 's/.* IP (10\.70[0-9.]*)\.[0-9]+ > (10\.70[0-9.]*)\.([0-9]+):.*/\1 -> \2:\3/' \
  | sort -u | tee /tmp/baseline.txt
```

**Expected result.**

```text
10.70.1.10 -> 10.70.2.20:5432
10.70.3.30 -> 10.70.4.40:502
```

The baseline is the two flows that actually occurred — the raw material for a least-privilege policy.

**Negative test.** If the monitoring window is too short or misses a periodic flow (a nightly poll, a backup), that legitimate flow will be absent from the baseline and later denied. Baseline length and coverage matter — segment from a representative window, not a one-minute sample.

**Rollback.** Keep `/tmp/baseline.txt`.

## Summary and Completion Checklist

- [ ] Assets discovered passively from traffic (no scanning).
- [ ] A communication baseline (src → dst:port) built from the capture.
- [ ] The importance of a representative monitoring window understood.
- [ ] The baseline ready to become zones and policy.
