# Chapter 06: Hubble and the Identity Model

## Learning Objectives

- Observe real flows — with identities and verdicts — using Hubble.
- Read the Hubble service map.
- Understand how Cilium enforces by identity in eBPF.

Before enforcing anything, use Hubble to *see* what the cluster does. Visibility first: you cannot segment well what you cannot observe.

## Hands-On Lab

### Lab 6.1 — Observe flows with Hubble

**Objective.** Watch the real flows, including the lateral-movement attempt, with their source and destination identities.

**Walkthrough**

**Step 1.** With `cilium hubble port-forward` running (from Chapter 03), stream flows while you generate traffic. In one terminal:

```bash
hubble observe --namespace dc --namespace ot --follow &
```

**Step 2.** Generate the flows from Chapter 05 again (web→db, hmi→plc, hmi→db, web→api GET and POST), then read what Hubble recorded:

```bash
hubble observe --from-pod ot/hmi --to-pod dc/db          # the lateral flow, with verdict
hubble observe --to-pod dc/api --protocol http           # L7 detail on the API
```

**Expected result.** Hubble shows each flow with the **source and destination identity** (e.g., `ot/hmi` → `dc/db`), the port, and the verdict (`FORWARDED` — nothing is enforced yet). For the API it shows the HTTP method and path, because Hubble understands Layer 7. You are seeing exactly what you will later enforce.

**Negative test.** Try to get this identity-and-verdict view from `tcpdump`; you get packets and IPs, not workload identities or verdicts. Hubble's value is that it speaks in the same identity terms your policy will.

**Cleanup.** Stop the background `hubble observe` with `kill %1` when done.

### Lab 6.2 — The Hubble service map

**Objective.** See the application's dependencies as a map, drawn from observed flows.

**Walkthrough**

```bash
cilium hubble ui &
# open the printed URL (a port-forward to the Hubble UI) in a browser
```

If you are headless, use the CLI equivalent — a summary of who talks to whom:

```bash
hubble observe --namespace dc --namespace ot -o compact | sort -u | head -20
```

**Expected result.** A service map (UI) or an edge list (CLI) showing `web → db`, `web → api`, `hmi → plc`, and the unwanted `hmi → db`. This is the dependency map you segment against — and, unlike a static diagram, it reflects what the app actually did.

**Negative test.** Design policy without looking at the map and you will miss a real dependency (breaking the app) or overlook an unwanted flow (leaving a hole). Observe first.

**Cleanup.** Stop the UI port-forward when done.

### Lab 6.3 — Identity-based enforcement

**Objective.** Understand what Cilium will enforce on: label-derived identities, in eBPF.

**Walkthrough**

```bash
kubectl -n kube-system exec ds/cilium -- cilium identity list | grep -E "app=web|app=db|app=hmi|app=plc|app=api"
```

**Expected result.** Each workload maps to a numeric **security identity** derived from its labels. When you apply policy in Chapters 07–08, Cilium compiles your label selectors to these identities and enforces them in the kernel — so a pod's IP changing, or the pod rescheduling to another node, does not affect policy. Identity, not address, is the unit of enforcement.

**Negative test.** Note there is no identity keyed on IP. A policy engine that enforced on IP would need constant updates as pods churn; identity-based enforcement does not.

**Cleanup.** Keep the cluster for Chapter 07.

## Summary and Completion Checklist

- [ ] Flows observed in Hubble with identities and verdicts.
- [ ] The service map (UI or CLI edge list) read.
- [ ] The label-derived identity model understood.
