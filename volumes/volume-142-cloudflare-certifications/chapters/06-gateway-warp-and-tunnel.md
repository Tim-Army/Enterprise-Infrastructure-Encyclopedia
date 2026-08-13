# Chapter 06: Gateway, WARP, and Tunnel

## Learning Objectives

- Filter outbound traffic with Gateway at the DNS and HTTP layers.
- Deploy the WARP client as both on-ramp and posture source.
- Connect origins with Tunnel and retire inbound firewall holes.
- Reason about what each layer can and cannot see.

*Exam relevance: the second half of Zero Trust Associate territory — Chapter 05 governed traffic **into** your applications; this chapter governs traffic **out of** your users and **between** the edge and your origins. **Defensive** throughout. [Volume XXXV (Zscaler)](../../volume-035-zscaler-zero-trust-exchange/README.md) and [Volume CXXVII (Netskope)](../../volume-127-netskope-certifications/README.md) cover the rival SSE stacks.*

## Gateway

**Gateway** is Cloudflare's secure web gateway: user traffic egresses through the edge, where policy applies at escalating depth:

| Layer | Sees | Can decide | Cannot |
|:---|:---|:---|:---|
| **DNS filtering** | The domain being resolved | Block known-bad and category domains before any connection | See paths, uploads, or anything inside the connection |
| **Network (L4)** | IP, port, protocol, SNI | Block non-web protocols, odd ports | Inspect content |
| **HTTP (L7)** | Full requests (with TLS inspection) | File-type rules, upload/download control, per-path decisions, DLP hooks | Anything in traffic it is not allowed to decrypt |

The layer table is the exam-relevant judgment: **DNS filtering is cheap, universal, and shallow; HTTP inspection is deep and requires TLS interception** — with its certificate deployment, its privacy conversation, and its exception list (banking, health) that must itself be maintained. The failure mode of the exception list is Chapter 03's allow-rule audit wearing new clothes: every bypass is a blind spot someone chose, and the list only stays defensible while someone can say why each entry exists.

## WARP

**WARP** is the device client: it delivers device traffic to Gateway (the on-ramp), and it reports **device posture** — managed status, disk encryption, OS version, running security software — which Chapter 05's Access policies consume.

That dual role makes deployment order matter. WARP-enrolled devices give you posture signals *and* egress filtering; unenrolled devices give you neither. A Zero Trust rollout that publishes apps through Access but skips client deployment has identity signals only — real progress, half the model.

## Tunnel

**Tunnel** (the `cloudflared` daemon) inverts the origin connection: instead of the edge connecting *in* to your origin — which requires a public IP, open inbound ports, and firewall rules — the origin connects *out* to the edge and keeps the connection alive. Traffic to your hostname rides the established tunnel back.

The consequences stack up quickly:

- **No inbound ports.** The origin firewall allows *nothing* in. There is no port 443 to scan, no origin IP to find — Chapter 02's origin-exposure problem does not need auditing when there is no public origin at all.
- **The DNS record points at the tunnel**, not an IP. The gray-cloud leak class disappears structurally.
- **Anything can be published** — an internal wiki on a NAS, a dev box, a Raspberry Pi — without DMZ engineering, and always behind Access policies.

## Hands-On Lab

Python models egress and origin connectivity. **Cost:** none.

### Lab 6.1 — What each Gateway layer catches

**Objective:** Route detections to the cheapest layer that can make them.

```bash
python3 - <<'EOF'
EVENTS = [
  # event,                                            dns_layer, l4, http_layer
  ("malware C2 domain resolution",                     True,  True,  True),
  ("phishing site, newly registered domain",           True,  True,  True),
  ("file upload to personal cloud storage",            False, False, True),
  ("SSH to an unsanctioned external host",             False, True,  True),
  ("credential POST to a lookalike login page",        False, False, True),
  ("malware download renamed as .txt",                 False, False, True),
]
print(f"{'event':46}{'DNS':>6}{'L4':>5}{'HTTP':>6}   cheapest sufficient layer")
for name, d, l4, h in EVENTS:
    cheapest = "DNS" if d else ("L4" if l4 else "HTTP (TLS inspection)")
    print(f"{name:46}{'yes' if d else '--':>6}{'yes' if l4 else '--':>5}{'yes' if h else '--':>6}   {cheapest}")

dns_only = sum(1 for _, d, _, _ in EVENTS if d)
http_needed = sum(1 for _, d, l4, h in EVENTS if h and not d and not l4)
print(f"\n{dns_only} of {len(EVENTS)} detections are available at the DNS layer — deploy that")
print("first; it is one resolver change, no certificates, immediate coverage.")
print(f"{http_needed} of {len(EVENTS)} require HTTP inspection, which requires TLS interception,")
print("which requires: certificate deployment to every device, a privacy policy")
print("conversation, and a maintained exception list (banking, health...).")
print("\nEvery exception is a chosen blind spot. The uploads/credentials/renamed-")
print("malware detections DO NOT EXIST inside excepted traffic — write the list")
print("with the same discipline as Chapter 03's allow rules: named, owned, justified.")
EOF
```

**Expected result:** Two detections are free at the DNS layer; three exist only under TLS inspection with its full deployment cost. The rollout order falls out of the table — DNS filtering today, HTTP inspection as a project — and the exception-list warning lands because the deepest layer's blind spots are precisely the ones someone chose on purpose.

**Negative test:** Buying the HTTP-layer detections by enabling TLS inspection with no exception governance. Six months later the "temporary" bypass list has forty entries and nobody can say which of them still deserve to be blind spots.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Tunnel versus open inbound ports

**Objective:** Compare origin exposure under the two connection models.

```bash
python3 - <<'EOF'
ORIGINS = [
  # service,            model,        inbound_ports, public_ip, access_in_front
  ("www (main site)",   "tunnel",     [],            False,     True),
  ("internal wiki",     "tunnel",     [],            False,     True),
  ("legacy-erp",        "port-fwd",   [443, 8443],   True,      False),
  ("dev-jumphost",      "port-fwd",   [22],          True,      False),
  ("grafana",           "tunnel",     [],            False,     True),
]
print(f"{'service':16}{'model':>10}{'inbound':>10}{'public IP':>11}{'scannable':>11}")
for name, model, ports, pub, access in ORIGINS:
    scannable = "YES" if pub else "no"
    print(f"{name:16}{model:>10}{str(ports) if ports else '[]':>10}{'yes' if pub else 'no':>11}{scannable:>11}")

exposed = [o for o in ORIGINS if o[3]]
print(f"\n{len(exposed)} origins still hold public IPs with open ports: "
      f"{', '.join(o[0] for o in exposed)}")
print("\nWhat the tunnel model removed, structurally rather than by configuration:")
print("   - nothing to port-scan: the firewall allows NO inbound connections")
print("   - no origin IP in DNS, certificate-transparency logs, or history")
print("   - the WAF/Access bypass path from Chapter 02 (hit the origin directly)")
print("     is gone because 'directly' no longer names a route")
print("\ndev-jumphost is the finding that matters: port 22 open to the internet in")
print("2026 is an SSH brute-force feed. The same box behind Tunnel + Access gets")
print("identity, posture, and MFA in front of SSH — and closes the port.")
print("\n(The tunnel daemon itself is now critical infrastructure: run it redundantly")
print("and monitor it — Chapter 08. Removing one risk class always installs a")
print("smaller, more manageable one; the trade is good, not free.)")
EOF
```

**Expected result:** Three tunnel-connected origins with zero scannable surface against two port-forward legacies, with the internet-facing SSH jumphost flagged as the urgent migration. The closing parenthesis keeps it honest — the tunnel daemon becomes a dependency worth monitoring, which is a much better problem than an open port 22, but is still a problem someone must own.

**Negative test:** Migrating www to Tunnel and leaving the "temporary" port-forward on legacy-erp. The attacker's scanner does not read your migration roadmap; the remaining public IP is the whole attack surface now.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Posture-gated access, end to end

**Objective:** Combine Chapter 05's policies with WARP's posture signals.

```bash
python3 - <<'EOF'
DEVICES = [
  # device,                     warp, managed, encrypted, os_current
  ("corp laptop (compliant)",   True,  True,  True,  True),
  ("corp laptop (stale OS)",    True,  True,  True,  False),
  ("BYOD phone, enrolled",      True,  False, True,  True),
  ("BYOD laptop, no client",    False, False, None,  None),
]
APPS = {
  "wiki":     lambda d: d[1],                                 # any WARP-enrolled device
  "grafana":  lambda d: d[1] and d[2],                        # + managed
  "finance":  lambda d: d[1] and d[2] and d[3] and d[4],      # + encrypted + current OS
}
print(f"{'device':28}" + "".join(f"{a:>10}" for a in APPS))
for dev in DEVICES:
    row = "".join(f"{'ALLOW' if rule(dev) else '--':>10}" for rule in APPS.values())
    print(f"{dev[0]:28}{row}")

print("\nThe BYOD-no-client row is the design point: WITHOUT the client there are")
print("no posture signals, so posture-gated apps are unreachable — not as")
print("punishment, but because the claim 'this device is safe' cannot be evaluated.")
print("Unknown posture must fail closed; treating unknown as compliant makes every")
print("posture rule optional for exactly the least-known devices.")
print("\nThe stale-OS row shows graduated response: the device keeps wiki and")
print("grafana, loses finance until patched. Posture gating that is all-or-nothing")
print("gets disabled the first week; graduated gating survives contact with reality.")
EOF
```

**Expected result:** The unenrolled device reaches nothing posture-gated, and the stale-OS laptop loses only the highest-sensitivity app. Two principles carry: unknown posture fails closed because it cannot be evaluated — not as policy aggression — and graduated consequences are what make posture rules politically survivable enough to keep enabled.

**Negative test:** Exempting executives' unenrolled personal devices from posture checks on the finance app. The highest-value targets now reach the highest-value app on the least-known devices — an inversion an attacker could not have designed better.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Gateway layers deployed cheapest-first, with TLS-inspection exceptions governed.
- [ ] WARP understood as both on-ramp and posture source, with unknown posture failing closed.
- [ ] Origins migrated to Tunnel, closing inbound ports and the origin-IP bypass class.
- [ ] The tunnel daemon itself monitored as the new (smaller) critical dependency.
