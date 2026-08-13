# Chapter 05: Zero Networks

## Learning Objectives

- Explain Zero Networks' agentless, automated segmentation model.
- Explain network-layer multi-factor authentication (multi-factor segmentation).
- Reason about the learn-then-enforce automation and the "firewall bubble."
- State the pros, cons, compatibility, and requirements.
- Complete a walkthrough for each Zero Networks topic.

## Theory and Architecture

**Zero Networks (Segment)** takes an **agentless, automated** approach. Instead of installing an agent,
its controller **remotely programs the host's built-in firewall** (Windows Firewall on Windows, the
native firewall on Linux) to wrap each asset in a **"firewall bubble."** It first runs in a **learning**
phase — observing client-to-server and server-to-server traffic for a period — then, with **human-on-the
-loop** review, automatically builds **allowlist** rules for the flows each asset actually needs and
denies the rest. Its signature capability is patented **network-layer multi-factor authentication**
("**multi-factor segmentation**"): privileged/administrative ports (RDP, SSH, WMI, SMB) are kept
**closed** and opened **just-in-time only after the user passes MFA** — so even a valid credential
cannot move laterally without a second factor. Zero Networks reports deploying in about an hour and
reaching **90%+ segmentation depth within 90 days**, across IT and **OT/IoT**, on-prem, cloud, and
hybrid.

## Pros, Cons, Compatibility, and Requirements

- **Pros:** **agentless** (fast deployment, no agent to install/maintain, no host performance hit);
  **automated** learn-then-enforce policy (low manual modeling); **network-layer MFA** on privileged
  ports stops credential-based lateral movement; covers **OT/IoT** and legacy without an agent; rapid
  time-to-value (hours to deploy, ~90 days to depth).
- **Cons:** depends on the host having a **reachable, controllable OS firewall** and remote management;
  strongest in **Windows/Active Directory** environments; enforcement quality depends on the accuracy of
  the learning phase; a relatively newer vendor than the incumbents.
- **Compatibility:** Windows and Linux hosts (via their native firewalls); OT/IoT and legacy devices;
  on-prem, cloud, and hybrid networks; integrates with identity/MFA providers.
- **Requirements:** network reachability to hosts' management interfaces (e.g., RPC/WinRM) so the
  controller can program firewalls; the Zero Networks segment/trust server; an identity/MFA provider for
  multi-factor segmentation; a learning window before enforcement.

## Design Considerations

Zero Networks fits organizations that want **fast, low-touch** segmentation without an agent rollout,
especially **Windows/AD-heavy** estates and mixed environments with **OT/IoT** that cannot take agents.
Give it a proper **learning window** and review the generated allowlist with human-on-the-loop before
enforcing. Ensure the controller can **reach and program** host firewalls (network path, permissions).
Use **multi-factor segmentation** to lock down administrative ports as a high-value early win.

## Implementation and Automation

The labs model the learn-then-enforce "firewall bubble," the MFA-gated privileged port, and the coverage
profile — the Zero Networks option in the rubric.

## Validation and Troubleshooting

Confirm the Zero Networks model:

```text
Agentless: controller programs the host's BUILT-IN firewall (no agent) -> "firewall bubble" per asset
Learn phase (observe flows) -> human-on-the-loop -> auto allowlist (default-deny the rest)
Multi-factor segmentation: privileged ports (RDP/SSH/WMI/SMB) closed; open just-in-time after MFA
Coverage: Windows/Linux + OT/IoT + legacy; on-prem/cloud/hybrid; ~1h deploy, 90%+ depth in 90 days
```

Common pitfalls: enforcing before the **learning** phase captures real flows (false denies); and missing
**remote-management reachability** so the controller cannot program a host's firewall.

## Security and Best Practices

Multi-factor segmentation of administrative ports is a strong defensive win against credential-based
lateral movement. Protect the Zero Networks controller and the identity/MFA integration. Review
auto-generated policy before enforcing. All work is authorized administration of your own network.

## Hands-On Lab

Zero Networks walkthroughs. **Shared prerequisites** — `python3` (modeling the learn/enforce and MFA
logic). **Cost:** none.

### Lab 5.1 — Model the learn-then-enforce bubble

**Objective:** Build an allowlist from observed flows.

```python
python3 - <<'PY'
learned = {("app01","db01","tcp/5432"), ("admin","app01","tcp/22"), ("web01","app01","tcp/8080")}
def enforce(src, dst, svc):
    return "ALLOW" if (src,dst,svc) in learned else "DENY (bubble default-deny)"
for f in [("web01","app01","tcp/8080"), ("web01","db01","tcp/5432"), ("attacker","db01","tcp/5432")]:
    print(f"{f} -> {enforce(*f)}")
PY
```

```text
('web01', 'app01', 'tcp/8080') -> ALLOW
('web01', 'db01', 'tcp/5432') -> DENY (bubble default-deny)
('attacker', 'db01', 'tcp/5432') -> DENY (bubble default-deny)
```

**Expected result:** learned flows allowed; unlearned/lateral flows denied by the per-asset bubble — no
agent required.

**Negative test:** skip the learning phase and enforce immediately; legitimate but unobserved flows are
denied — learn first, review, then enforce.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Model multi-factor segmentation on a privileged port

**Objective:** Gate admin access behind MFA.

```python
python3 - <<'PY'
def rdp_allowed(user, mfa_passed):
    # privileged port (RDP 3389) is closed unless MFA just-in-time opens it
    return mfa_passed
for user, mfa in [("admin", True), ("admin", False), ("stolen-cred", False)]:
    state = "OPEN (JIT after MFA)" if rdp_allowed(user, mfa) else "CLOSED"
    print(f"user={user:12} mfa={mfa!s:5} -> RDP/3389 {state}")
PY
```

```text
user=admin        mfa=True  -> RDP/3389 OPEN (JIT after MFA)
user=admin        mfa=False -> RDP/3389 CLOSED
user=stolen-cred  mfa=False -> RDP/3389 CLOSED
```

**Expected result:** RDP stays closed until MFA passes — a stolen credential alone cannot open the
privileged port.

**Negative test:** leave admin ports permanently open to a management subnet; a compromised jump host
moves laterally — gate them with **MFA** just-in-time.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reason about coverage and requirements

**Objective:** Confirm the agentless reachability requirement.

```python
python3 - <<'PY'
assets = {
  "win-srv (WinRM reachable)":  "controller can program Windows Firewall -> covered",
  "linux-srv (mgmt reachable)": "controller can program host firewall -> covered",
  "ot-plc (no agent possible)": "agentless segmentation applies -> covered",
  "isolated-host (no mgmt path)":"controller cannot reach firewall -> NOT covered until path exists",
}
for a, note in assets.items(): print(f"{a:30}: {note}")
print("Requirement: remote-management reachability so the controller can program the OS firewall")
PY
```

**Expected result:** coverage where the controller can reach host management; a gap where it cannot — the
core requirement.

**Negative test:** assume 100% coverage without checking management reachability; hosts with no path are
uncovered — verify reachability.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Score Zero Networks against the rubric

**Objective:** Place it in the comparison.

```python
python3 - <<'PY'
weights = {"coverage":0.25,"visibility":0.15,"automation":0.15,"granularity":0.10,
           "scale":0.10,"failure_mode":0.05,"compliance":0.10,"tco":0.10}
scores  = {"coverage":4,"visibility":4,"automation":5,"granularity":3,
           "scale":4,"failure_mode":3,"compliance":4,"tco":5}  # low TCO: no agents
total = sum(weights[k]*scores[k] for k in weights)
print(f"Zero Networks weighted score: {total:.2f}/5 (strengths: automation, agentless TCO, MFA)")
PY
```

**Expected result:** a weighted score highlighting automation and low agent-TCO — its comparative
strengths.

**Negative test:** score it only on granularity vs an L7 agent tool; weight **automation/agentless/MFA**
where they matter to you.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Zero Networks is agentless microsegmentation: its controller programs each host's built-in firewall into
a per-asset "bubble" after a learning phase (human-on-the-loop), and its patented network-layer MFA keeps
privileged ports closed until a second factor opens them just-in-time — fast to deploy, low TCO, strong
on Windows/AD and OT/IoT, but dependent on management reachability to program firewalls.

- [ ] I can explain the agentless learn-then-enforce model.
- [ ] I can explain multi-factor segmentation of privileged ports.
- [ ] I can state the pros, cons, compatibility, and requirements.
- [ ] I completed Labs 5.1–5.4 including each negative test.
