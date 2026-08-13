# Chapter 07: NCCSA — ZTNA and Private Access

## Learning Objectives

- Cover the NCCSA's ZTNA pillar: Zero Trust access to private applications.
- Understand the broker/publisher model and how it differs from a VPN.
- Model the reverse-broker (no-inbound) architecture with free primitives.

## ZTNA versus VPN

A **VPN** puts the user *on the network* — once connected, they can reach whatever the network routing allows (lateral movement risk). **ZTNA** (Zero Trust Network Access) grants access to **specific applications**, per identity and posture, without network-level connectivity. Netskope Private Access implements ZTNA with a **broker + publisher** model:

| Piece | Role |
|:---|:---|
| **Broker (cloud)** | Netskope's cloud service that authenticates users and connects them to apps |
| **Publisher** | A lightweight connector deployed *beside* the private app; it makes **outbound** connections to the broker |
| **No inbound** | The app/network exposes **no inbound ports** — the publisher dials out, so there's nothing to attack from the internet |
| **Per-app access** | A user reaches only the specific apps policy grants — never the network |

The security win: private apps are **invisible** to the internet (no inbound firewall holes), and access is per-app and identity-gated.

## Hands-On Lab

Namespaces + a reverse connection model the broker/publisher pattern. **Cost:** none.

### Lab 7.1 — The no-inbound broker model

**Objective:** Show the publisher dialing out — no inbound port on the app side.

```bash
sudo ip netns add appnet    # the private app's isolated network
sudo ip netns add broker    # the cloud broker (internet-reachable)
sudo ip link add pub-a type veth peer name pub-b
sudo ip link set pub-a netns appnet; sudo ip link set pub-b netns broker
sudo ip netns exec appnet ip addr add 10.70.0.2/30 dev pub-a; sudo ip netns exec appnet ip link set pub-a up
sudo ip netns exec broker ip addr add 10.70.0.1/30 dev pub-b; sudo ip netns exec broker ip link set pub-b up
sudo ip netns exec appnet ip link set lo up; sudo ip netns exec broker ip link set lo up
# the app listens ONLY inside appnet; the publisher (appnet side) dials OUT to the broker
sudo ip netns exec appnet bash -c 'nohup nc -lk -p 8443 >/dev/null 2>&1 &'   # private app
echo "app listens on 10.70.0.2:8443 inside appnet — NOT exposed to the internet"
sudo ip netns exec broker nc -z -w2 10.70.0.2 8443 && echo "broker reaches app via the publisher's outbound tunnel"
```

**Expected result:** The private app listens only inside its isolated network, and the broker reaches it **through the publisher's outbound path** — never via an inbound port on the app side. This is ZTNA's structural advantage: no internet-facing attack surface for private apps.

**Negative test:** Exposing the app with an inbound port (a classic VPN/DMZ approach) — it becomes internet-scannable and attackable; ZTNA's outbound-only publisher eliminates that exposure.

**Rollback:** Keep for the next lab.

### Lab 7.2 — Per-app, identity-gated access

**Objective:** Model access granted per app and identity, not per network.

```bash
python3 - <<'EOF'
# ZTNA policy: (user, app) pairs — access is to APPS, never the network
grants = {("alice","hr-portal"), ("alice","wiki"), ("bob","wiki")}
def can_access(user, app):
    return "ALLOW" if (user,app) in grants else "DENY (no per-app grant)"
for u,a in [("alice","hr-portal"),("bob","hr-portal"),("bob","wiki"),("alice","finance-db")]:
    print(f"{u} -> {a:12}: {can_access(u,a)}")
EOF
```

**Expected result:**

```text
alice -> hr-portal   : ALLOW
bob -> hr-portal     : DENY (no per-app grant)
bob -> wiki          : ALLOW
alice -> finance-db  : DENY (no per-app grant)
```

Access is a set of **(user, app) grants** — Bob reaching the wiki does not let him reach the HR portal, and no one gets "the network." Compare a VPN, where Bob on the network could probe the HR portal's port. Per-app, identity-gated access is ZTNA's model and a core NCCSA topic.

**Negative test:** Granting "network access to the private subnet" instead of per-app — you recreate VPN lateral movement; ZTNA's per-app grants are what prevent it.

**Rollback:** Keep for the next lab.

### Lab 7.3 — Posture and context in the decision

**Objective:** Add device posture to the ZTNA grant.

```bash
python3 - <<'EOF'
# ZTNA decision = identity AND device posture AND context
def ztna(user_ok, device_compliant, app, sensitivity):
    if not user_ok: return "DENY (auth)"
    if sensitivity == "high" and not device_compliant: return "DENY (device not compliant)"
    return "ALLOW"
print("compliant device, high app:  ", ztna(True, True, "finance-db","high"))
print("noncompliant device, high app:", ztna(True, False, "finance-db","high"))
EOF
```

**Expected result:**

```text
compliant device, high app:   ALLOW
noncompliant device, high app: DENY (device not compliant)
```

ZTNA folds **device posture** into the per-request decision — a valid user on a non-compliant device is denied a sensitive app. This continuous, context-aware evaluation is the Zero Trust principle from [Chapter 02](02-sase-accreditation-architecture.md) applied to private access.

**Negative test:** Authenticating the user but ignoring device posture — a compromised but "authorized" laptop reaches sensitive apps; posture is part of the ZTNA decision, not optional.

**Rollback:** `for ns in appnet broker; do sudo ip netns del $ns 2>/dev/null; done`.

### Lab 7.4 — ZTNA in the SASE whole

**Objective:** Place ZTNA alongside the other SSE controls.

```text
One Netskope policy engine, four surfaces:
  SWG   -> internet/web traffic      (Ch05)
  CASB  -> sanctioned/shadow SaaS    (Ch04)
  DLP   -> sensitive data everywhere (Ch06)
  ZTNA  -> private apps              (this chapter)
Same identity, posture, and data policy across all four — the SASE convergence payoff.
```

**Expected result:** ZTNA as one of four surfaces under **one policy engine** — the same identity/posture/DLP logic governs web, SaaS, data, and private apps. That single-policy convergence is what distinguishes SASE from four bolted-together point products, and a theme the NCCSA closes on.

**Negative test:** Running ZTNA, SWG, CASB, and DLP as separate products with separate policies — inconsistent enforcement and four consoles; the platform's value is one engine across all four.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The broker/publisher, no-inbound ZTNA model built and its VPN contrast understood.
- [ ] Per-app, identity-gated access and device posture in the decision drilled.
- [ ] ZTNA placed within the single-policy SSE convergence.
- [ ] NCCSA SSE coverage complete across Chapters 03–07.
