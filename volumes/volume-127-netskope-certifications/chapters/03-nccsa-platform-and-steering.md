# Chapter 03: NCCSA — The Netskope One Platform and Traffic Steering

## Learning Objectives

- Cover the NCCSA's platform foundations: how traffic reaches Netskope and how the tenant is administered.
- Understand steering methods — client, proxy, tunnel, and API — and inline vs out-of-band.
- Model traffic steering with a forward proxy.

## The exam in brief

**NCCSA** (exam **NSK101**, Pearson VUE, ~70 questions, ~2 hours, 70% pass, valid 2 years) certifies that you can **configure, monitor, and troubleshoot** the Netskope platform. The **Netskope One Administrator** course is the recommended prep. This chapter covers steering and the console; [Chapters 04–07](04-nccsa-casb-cloud-app-control.md) cover the SSE controls (CASB, SWG, DLP, ZTNA).

## Getting traffic to Netskope

Netskope can only inspect traffic that **reaches** it. Steering is the first thing the NCCSA tests:

| Method | What it is |
|:---|:---|
| **Netskope Client** | An endpoint agent that steers selected traffic (web/cloud) to NewEdge |
| **Explicit/forward proxy** | Browsers/apps point at Netskope as a proxy (PAC file, explicit settings) |
| **IPsec/GRE tunnel** | Site-level steering from a router/SD-WAN device |
| **Reverse proxy** | Steers traffic to sanctioned SaaS without an agent (for BYOD/unmanaged) |
| **API (out-of-band)** | Connects to SaaS vendor APIs to scan data at rest — no traffic steering |

Two axes the exam stresses: **inline** (traffic passes through Netskope in real time — enforce/block) vs **API/out-of-band** (scan what's already in the SaaS — retroactive), and **agent vs agentless** steering.

## Hands-On Lab

Squid (forward proxy) models steering and the inline inspection point. **Cost:** none.

### Lab 3.1 — Steer traffic through an inline proxy

**Objective:** Model the Netskope Client/proxy steering: traffic passes through an inspection point.

```bash
sudo apt-get install -y squid 2>/dev/null
sudo sed -i 's/^http_access deny all/http_access allow all/' /etc/squid/squid.conf 2>/dev/null || true
sudo systemctl restart squid 2>/dev/null || sudo squid -f /etc/squid/squid.conf 2>/dev/null
# a client "steered" to the proxy (models the Netskope Client sending traffic to NewEdge)
curl -s -x http://127.0.0.1:3128 -o /dev/null -w "via-proxy HTTP %{http_code}\n" http://example.com/ 2>/dev/null || \
  echo "proxy models the inline inspection point traffic is steered through"
sudo tail -2 /var/log/squid/access.log 2>/dev/null || echo "access log = the visibility steering creates"
```

**Expected result:** The request flows through the proxy and appears in its access log — the essence of steering: traffic is directed through an inline inspection point (Netskope's NewEdge) where policy applies and visibility is created. The access log models Netskope's visibility.

**Negative test:** Traffic that isn't steered (direct, bypassing the proxy) is invisible and uncontrolled — the NCCSA lesson that **coverage depends on steering**; unsteered traffic is a blind spot.

**Cleanup:** `sudo systemctl stop squid 2>/dev/null`.

### Lab 3.2 — Steering configuration: what to send, what to bypass

**Objective:** Model a steering config (which traffic goes to Netskope).

```bash
cat > steering.conf <<'EOF'
# Netskope steering config (modeled): steer web + sanctioned SaaS, bypass a few
steer:  *.example-saas.com     # cloud apps -> inspect
steer:  all-web (80/443)       # general web -> SWG
bypass: *.internal.corp        # internal apps -> don't steer
bypass: update.trusted-vendor  # known-good, high-volume -> bypass to save capacity
EOF
grep -c "^steer" steering.conf; grep -c "^bypass" steering.conf
echo "steering decides Netskope's scope: too little = blind spots; too much = needless load/breakage"
```

**Expected result:** A steering policy with explicit steer and bypass rules — the NCCSA's steering-config skill: send the traffic you must inspect, bypass what you shouldn't (internal apps, certified-safe high-volume flows). Getting this wrong causes either blind spots or broken apps.

**Negative test:** Bypassing a category "to fix a breakage" without understanding why — you may open a data-exfiltration path; bypasses are security decisions, and the exam treats them as such.

**Cleanup:** `rm steering.conf`.

### Lab 3.3 — Inline vs API protection

**Objective:** Contrast real-time enforcement with out-of-band scanning.

```bash
python3 - <<'EOF'
# Inline: inspect as traffic flows -> can BLOCK in real time
# API: scan data already in the SaaS -> can find & remediate, but AFTER the fact
scenarios = [
  ("user uploads a file with PII to sanctioned SaaS", "inline", "BLOCK the upload in real time"),
  ("a file with PII already sits in the SaaS from last year", "API", "find it, quarantine/remediate retroactively"),
  ("user pastes secrets into a chat app", "inline", "block/alert as it happens"),
]
for s, mode, action in scenarios:
    print(f"[{mode:6}] {s} -> {action}")
EOF
```

**Expected result:** Inline blocks in real time; API finds and remediates what's already there — the NCCSA's core distinction. Full coverage needs **both**: inline to stop new violations, API to clean up existing exposure.

**Negative test:** Relying on API-only protection and expecting real-time blocking — API is retroactive; it can't stop the upload as it happens. The exam tests knowing which mode does which.

**Cleanup:** None.

### Lab 3.4 — The admin console and monitoring

**Objective:** Know the NCCSA's console surfaces.

```text
Netskope One console (NCCSA administration):
  - Skope IT: activity/alerts/page events — the visibility and troubleshooting view
  - Policies: real-time protection (inline) + API-enabled protection policies
  - App instances: distinguish corporate vs personal instances of the same SaaS
  - Steering config + client management
  - Incident management: DLP incidents, malware, anomalies
Monitoring/troubleshooting = Skope IT + client status; the exam tests reading these.
```

**Expected result:** The console map — **Skope IT** for visibility/troubleshooting, Policies for enforcement, app-instance awareness, steering/client management. NCCSA is fundamentally about operating this console.

**Negative test:** Looking for blocked events in the wrong view — Skope IT's event types (application, page, alert) must be matched to what you're troubleshooting; the exam tests console fluency.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Steering methods (client/proxy/tunnel/reverse-proxy/API) and inline-vs-API understood.
- [ ] Traffic steered through an inline inspection point and its visibility modeled.
- [ ] Steer/bypass trade-offs and the Skope IT console surfaces internalized.
