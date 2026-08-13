# Chapter 04: Administrator — Security, MFA, and Policies

## Learning Objectives

- Configure Adaptive MFA and authenticator options.
- Build authentication and sign-on policies.
- Apply risk-based, context-aware access.
- Use ThreatInsight and understand phishing-resistant factors.
- Complete a walkthrough for each security topic.

## Theory and Architecture

The **Certified Administrator** security domain is Okta's strongest value: controlling **how** users
authenticate. **Multi-factor authentication (MFA)** requires additional factors beyond a password;
**Adaptive MFA** makes that requirement **context-aware** — stepping up based on risk signals
(network, device, location, behavior). Okta evaluates access through **authentication policies**
(per-app rules) and **global sign-on policies**, each with conditions (group, network zone, device
trust, risk) and actions (allow, deny, require factor, prompt frequency). **ThreatInsight** blocks or
audits requests from IPs Okta has observed in credential attacks. The strongest factors are
**phishing-resistant**: **FIDO2/WebAuthn** (passkeys) and PIV/smart cards, which defeat phishing that
defeats OTP. The design goal is **least-friction, risk-appropriate** access — strong where risk is
high, smooth where it is low. This chapter teaches each with a hands-on defensive walkthrough (policy
logic, risk evaluation, and factor selection).

## Design Considerations

Prefer **phishing-resistant** factors (FIDO2/passkeys) for privileged access. Make MFA **adaptive** —
step up on risk, not on every login. Order **authentication policy** rules specific-first. Use
**network zones** and **device trust** as conditions. Enable **ThreatInsight**. Balance security with
**user friction**.

## Implementation and Automation

The labs build an adaptive policy, evaluate risk, and select factors.

## Validation and Troubleshooting

Confirm the security model:

```text
MFA = extra factor; Adaptive MFA = context-aware step-up (network/device/location/risk).
Authentication policy (per-app) + global sign-on policy: conditions (group/zone/device/risk) -> actions (allow/deny/require factor).
ThreatInsight = block known-bad IPs. Strongest factors = phishing-resistant (FIDO2/WebAuthn, PIV).
```

Common pitfalls: requiring MFA on **every** action (friction → workarounds); and allowing **OTP-only**
for admins (phishable) instead of FIDO2.

## Security and Best Practices

Use **adaptive**, **phishing-resistant** MFA (FIDO2) for privileged access, order policies
specific-first, condition on **zone/device/risk**, and enable **ThreatInsight**. Minimize friction
for low risk. All work is defensive.

## Hands-On Lab

Security walkthroughs. **Shared prerequisites** — `python3`, a developer org. **Cost:** none.

### Lab 4.1 — Build an adaptive authentication policy

**Objective:** Step up on risk.

```python
python3 - <<'PY'
def decision(ctx):
    if ctx["risk"]=="high" or ctx["network"]=="untrusted":
        return "require phishing-resistant MFA (FIDO2)"
    if ctx["new_device"]:
        return "require MFA (Okta Verify)"
    return "allow (password + session)"
for ctx in [{"risk":"high","network":"untrusted","new_device":True},
            {"risk":"low","network":"trusted","new_device":False}]:
    print(ctx, "->", decision(ctx))
PY
```

**Expected result:** high-risk/untrusted context requires **FIDO2**, trusted low-risk allows a smooth
sign-in — adaptive MFA.

**Negative test:** require the same heavy MFA for every login regardless of context; users seek
workarounds — make it **adaptive**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Order authentication policy rules

**Objective:** Specific rules first.

```python
python3 - <<'PY'
rules=[{"n":1,"match":"admins","action":"require FIDO2"},
       {"n":2,"match":"off-network","action":"require MFA"},
       {"n":3,"match":"any","action":"allow with password+MFA (catch-all)"}]
for r in rules: print(f"rule {r['n']} [{r['match']:11}] -> {r['action']}")
print("Administrator: evaluate top-down; specific (admins) before catch-all")
PY
```

**Expected result:** an ordered policy with **admins first** and a catch-all last — correct policy
precedence.

**Negative test:** put the catch-all first; the admin rule never evaluates — order **specific
first**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Choose phishing-resistant factors

**Objective:** Defeat phishing for privileged access.

```python
python3 - <<'PY'
factors={"SMS OTP":"phishable + SIM-swap risk","TOTP app":"phishable (relay)",
         "Okta Verify push + number match":"stronger","FIDO2 / WebAuthn (passkey)":"phishing-resistant",
         "PIV/smart card":"phishing-resistant"}
for f,note in factors.items(): print(f"{f:34}: {note}")
print("Administrator: require FIDO2/PIV for admins; retire SMS OTP")
PY
```

**Expected result:** factors ranked by phishing resistance, with **FIDO2/PIV** for admins — factor
selection.

**Negative test:** protect admins with **SMS OTP**; it's phishable and SIM-swappable — use
**phishing-resistant** factors.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Apply ThreatInsight

**Objective:** Block known-bad sources.

```python
python3 - <<'PY'
requests=[{"ip":"198.51.100.7","threatinsight":"known credential-attack source"},
          {"ip":"10.0.0.5","threatinsight":"clean"}]
for r in requests:
    action="block/audit" if "known" in r["threatinsight"] else "allow"
    print(f"{r['ip']:16} {r['threatinsight']:32} -> {action}")
print("ThreatInsight: leverage Okta's cross-tenant threat data to block bad IPs")
PY
```

**Expected result:** the known-bad IP **blocked/audited**, the clean one allowed — ThreatInsight in
action.

**Negative test:** ignore ThreatInsight and rely on lockouts alone; you miss distributed credential
attacks — enable **ThreatInsight**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Administrator security domain builds adaptive, phishing-resistant MFA and ordered authentication/
sign-on policies conditioned on risk, device, and network, backed by ThreatInsight — least-friction,
risk-appropriate access.

- [ ] I can build an adaptive authentication policy.
- [ ] I can order policy rules specific-first.
- [ ] I can choose phishing-resistant factors.
- [ ] I can apply ThreatInsight.
- [ ] I completed Labs 4.1–4.4 including each negative test.
