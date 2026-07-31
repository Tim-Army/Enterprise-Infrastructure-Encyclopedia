# Chapter 03: Identities and the Fabric

## Learning Objectives

- Create the identities that will be allowed to reach each asset.
- Understand how the Xage Fabric stores identity and policy in a tamper-resistant, decentralized way.
- Build the identity and token store the Track 2 broker will check.

## Identity is the unit of policy

Xage policy is written for **identities**, not IP addresses: a user, a service, or a device, each with credentials (and, for humans, MFA). The web application is the identity `svc-web`; the operator is `op-hmi`. Only those identities — proven per connection — are allowed through the brokers. This chapter registers the identities and, on Track 2, builds the token store the broker validates against.

## Hands-On Lab

### Exercise 3.1 — Register identities

**Objective.** Define `svc-web` (may reach db) and `op-hmi` (may reach plc).

**Track 1 — Walkthrough.** In the Fabric Manager, create identities and assign credentials; human identities get MFA, service identities get a rotating secret or certificate:

```text
xage> Identities > add op-hmi   type=user    mfa=on
xage> Identities > add svc-web  type=service credential=rotating-secret
```

**Expected result (design).** Two identities exist in the fabric, each with a credential the enforcement node can verify.

**Track 2 — Walkthrough.** Model identities as tokens the broker will accept (a real deployment uses certificates/MFA; a shared secret suffices to demonstrate the *brokered-by-identity* property):

```bash
sudo mkdir -p /etc/xage
# identity -> token (in production: certs / MFA, not a flat file)
sudo tee /etc/xage/identities > /dev/null <<'EOF'
op-hmi   TOKEN-HMI-7f3a
svc-web  TOKEN-WEB-9c21
EOF
sudo chmod 600 /etc/xage/identities
cat /etc/xage/identities
```

**Expected result.** Two identities with tokens the broker can check.

**Negative test.** An identity with no token cannot be brokered — access requires a *proven* identity, not merely a network position. A blank token is rejected.

**Cleanup.** Keep the identities.

### Exercise 3.2 — Bind identities to assets (access policy)

**Objective.** Grant `svc-web → db:5432` and `op-hmi → plc:502`, nothing else.

**Track 1 — Walkthrough.**

```text
xage> Policies > add: identity=svc-web asset=db  service=5432 action=allow
xage> Policies > add: identity=op-hmi  asset=plc service=502  action=allow
xage> Policies > default: deny
```

**Expected result (design).** Two explicit grants; every other identity/asset pair is denied by the fabric default.

**Track 2 — Walkthrough.** Record the grants the broker enforces (identity + destination + port):

```bash
sudo tee /etc/xage/policy > /dev/null <<'EOF'
svc-web  10.60.1.20 5432
op-hmi   10.60.9.40 502
EOF
cat /etc/xage/policy
```

**Expected result.** Two grant rows; the broker will forward only when the presented identity matches a grant for the requested asset and port.

**Negative test.** A grant for `op-hmi → db:5432` is absent, so even a valid operator identity cannot reach the database through the broker — least privilege per identity, not per network.

**Cleanup.** Keep the policy.

## Summary and Completion Checklist

- [ ] Identities `svc-web` and `op-hmi` created (with tokens in Track 2).
- [ ] Access policy binds each identity to exactly one asset/service.
- [ ] The fabric default-deny understood.
- [ ] Track 2 identity and policy stores ready for the broker.
