# Chapter 02: Enterprise Identity, Zero Trust, and Privileged Access

## Learning Objectives

- Explain the NIST SP 800-207 Zero Trust Architecture model and its policy
  decision point / policy enforcement point (PDP/PEP) pattern.
- Design an identity architecture spanning workforce identity, machine
  identity, and privileged access, including federation and conditional
  access.
- Compare privileged access management (PAM) patterns: standing access,
  just-in-time (JIT) elevation, and break-glass accounts.
- Implement phishing-resistant multi-factor authentication (MFA) and
  explain why SMS/OTP-based MFA is insufficient against modern
  adversary-in-the-middle (AiTM) phishing.
- Configure conditional access policies and validate them against both
  legitimate and denied-access scenarios.
- Build and test a working PAM session-brokering and audit workflow.

## Theory and Architecture

### Zero Trust as an architecture, not a product

NIST SP 800-207 defines Zero Trust Architecture (ZTA) as a set of
principles, not a specific product: no implicit trust is granted based on
network location or asset ownership; every access request is evaluated
using the least privilege necessary, based on identity, device posture,
and context, before access is granted. The core architectural components
are:

- **Policy Engine (PE)** — evaluates trust and generates an access
  decision using policy plus signals (identity, device compliance, threat
  intelligence, behavioral risk).
- **Policy Administrator (PA)** — establishes or terminates the connection
  between subject and resource based on the PE's decision, and configures
  the PEP accordingly.
- **Policy Enforcement Point (PEP)** — the gateway that actually permits,
  monitors, and terminates connections (identity-aware proxy, next-
  generation firewall, service mesh sidecar).

This PDP/PEP separation is the pattern behind every modern access-control
technology covered in this chapter: an identity provider's conditional
access engine is a Policy Engine; a reverse proxy enforcing that decision
at the application edge is a Policy Enforcement Point. Zero Trust does not
eliminate network segmentation ([Chapter 4](04-network-security-architecture-and-infrastructure-defense.md) covers that layer) — it adds an
identity- and context-aware decision layer on top of network controls, so
that network location alone is never sufficient for access.

### Identity taxonomy

Enterprise environments manage several distinct identity populations, each
with different lifecycle and risk characteristics:

| Identity type | Examples | Primary control concern |
| --- | --- | --- |
| Workforce (human) | Employees, contractors | Joiner/mover/leaver lifecycle, MFA, conditional access |
| Privileged (human) | Domain admins, cloud admins, DBAs | Standing-access minimization, session recording |
| Machine / workload | Service accounts, CI/CD runners, workload identities | Credential rotation, scoped short-lived tokens |
| Non-human / API | API keys, integration accounts | Key rotation, least-privilege scoping |
| Customer / external | B2C or B2B federated users | Separate identity store, breach-resilient auth |

Treating these as one undifferentiated "user" population is a common root
cause of privilege sprawl: a service account created with interactive-user
permissions inherits password-expiration and MFA exemptions never intended
for machine credentials.

### Authentication and federation

- **Multi-factor authentication (MFA)** should be evaluated by phishing
  resistance, not merely presence. SMS one-time passcodes and
  push-notification approval are vulnerable to SIM-swap and MFA-fatigue
  (prompt-bombing) attacks, respectively. **FIDO2/WebAuthn** hardware
  security keys and platform authenticators (passkeys) bind the credential
  to the origin, defeating adversary-in-the-middle (AiTM) phishing proxies
  that can otherwise relay OTP and push approvals in real time.
- **Federation protocols**: SAML 2.0 remains common for legacy enterprise
  SSO; **OpenID Connect (OIDC)** on top of OAuth 2.1 is the modern standard
  for API-driven and cloud-native federation. Both rely on a trusted
  identity provider (IdP) issuing signed assertions/tokens consumed by
  relying-party applications, removing the need for each application to
  manage credentials directly.
- **Conditional access** evaluates signals — device compliance state,
  network location, sign-in risk score, application sensitivity — at
  authentication time and enforces graduated responses: allow, require
  step-up MFA, require a compliant/managed device, or block.

### Privileged access management patterns

Privileged accounts (domain administrators, cloud IAM administrators,
database superusers, network device enable-mode credentials) carry
disproportionate blast radius and are the primary target in most
ransomware and business-email-compromise escalation chains. Three
architectural patterns reduce that exposure:

- **Standing privileged access** — a named account holds administrative
  rights continuously. Highest risk; should be reserved for a small set of
  break-glass accounts, not routine administration.
- **Just-in-time (JIT) elevation** — administrative rights are granted for
  a bounded time window after an approval workflow (self-service request,
  peer approval, or automatic approval against policy), then automatically
  revoked. This is the pattern implemented by PAM platforms and by
  cloud-native mechanisms such as time-bound role assumption.
- **Break-glass accounts** — a small number of emergency accounts, stored
  offline or in a sealed vault, used only when the identity provider or
  PAM system itself is unavailable. Their use should trigger mandatory
  post-incident review, and credentials should rotate immediately after
  use.

A PAM platform typically brokers privileged sessions rather than revealing
credentials to the requester at all: the administrator authenticates to
the PAM broker with their own (non-privileged) identity plus MFA, the
broker checks out a rotated credential from a vault, establishes the
session on the target system, and records it — the human operator never
sees the privileged password.

### Machine and workload identity

Static, long-lived credentials embedded in configuration files or CI/CD
pipelines are a persistent source of breaches. The Zero Trust pattern for
machine identity replaces static secrets with **short-lived, dynamically
issued credentials** bound to a verifiable workload identity — for
example, a CI/CD job authenticating to a secrets manager using a
platform-issued OIDC token, then receiving a credential scoped to that
job's exact permissions and expiring within minutes. This eliminates the
class of vulnerability where a leaked long-lived API key remains valid for
months after exposure.

## Design Considerations

- **Identity provider consolidation vs. resilience.** A single IdP
  simplifies conditional access policy and reduces attack surface, but
  becomes a single point of failure for the entire enterprise — an IdP
  outage or compromise can lock out the whole workforce, including the
  administrators needed to respond. Break-glass accounts and an
  out-of-band administrative path are mandatory design elements, not
  optional hardening.
- **Phishing-resistant MFA rollout order.** Migrating the entire workforce
  to FIDO2 hardware keys simultaneously is rarely feasible; prioritize
  privileged accounts, finance/payments roles, and IT administrators first
  — the accounts whose compromise causes the most damage — before a
  broader workforce rollout.
- **JIT elevation approval friction.** Fully automatic approval against
  policy minimizes delay but weakens the control if policy is too
  permissive; mandatory peer approval improves assurance but adds latency
  that during an active incident can itself become a risk. Many programs
  use automatic approval for routine, well-scoped requests and mandatory
  human approval for higher-risk scope (for example, production database
  write access).
- **Conditional access policy conflicts.** Overlapping policies (device
  compliance required, plus location-based block, plus risk-based step-up)
  can produce unexpected denials for legitimate users. Design policies with
  explicit precedence and test them against representative user personas
  before enforcement, not just against the policy author's own session.
- **Service account ownership.** Every non-human identity should have a
  named human owner and a documented purpose; unowned service accounts
  accumulate stale permissions and are rarely included in workforce
  offboarding processes, becoming a common persistence mechanism.
- **Session recording retention** for privileged access must balance
  investigative value against storage cost and privacy law — retain
  recordings long enough to support incident investigation timelines
  (commonly 90–365 days) and align retention with the data handling
  policy in [Chapter 8](08-data-security-cryptography-privacy-and-ransomware-resilience.md).

## Implementation and Automation

### Conditional access policy as code

Represent conditional access policy in structured form so it can be
version-controlled, peer-reviewed, and tested like any other
infrastructure change:

```yaml
# conditional-access/privileged-admin-access.yaml
policy_id: ca-priv-001
name: "Require compliant device and phishing-resistant MFA for admin roles"
applies_to:
  roles:
    - global-administrator
    - privileged-role-administrator
    - identity-administrator
conditions:
  device_compliance: required
  authentication_strength: phishing-resistant-mfa
  network_location: exclude(trusted-corporate-ranges) -> require(compliant_device)
grant_controls:
  action: block
  unless_all:
    - device_compliance == "compliant"
    - auth_strength == "phishing-resistant-mfa"
session_controls:
  sign_in_frequency_hours: 4
  persistent_browser_session: never
```

### Just-in-time privileged elevation workflow

```bash
# Example: JIT elevation request against a PAM CLI (vendor-neutral pattern)
pam-cli request-access \
  --target prod-db-cluster-03 \
  --role db-admin \
  --justification "INC-20458 replication lag remediation" \
  --duration 60m

# Approval (peer or policy-driven), then session brokering:
pam-cli session start --request-id JIT-88213
# The broker checks out a rotated credential from the vault, opens the
# session, and begins recording without exposing the credential value.
```

A minimal Python illustration of the JIT approval-and-expiry logic a PAM
broker enforces:

```python
#!/usr/bin/env python3
"""jit_elevation.py — illustrates JIT privilege grant/expiry logic."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class ElevationGrant:
    principal: str
    role: str
    justification: str
    granted_at: datetime
    duration_minutes: int

    def is_active(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now < self.granted_at + timedelta(minutes=self.duration_minutes)


def request_elevation(principal: str, role: str, justification: str,
                       duration_minutes: int = 60) -> ElevationGrant:
    if not justification.strip():
        raise ValueError("Elevation requests require a justification (ticket reference).")
    if duration_minutes > 480:
        raise ValueError("Elevation duration exceeds policy maximum of 8 hours.")
    return ElevationGrant(principal, role, justification,
                           datetime.now(timezone.utc), duration_minutes)


if __name__ == "__main__":
    grant = request_elevation("alice@corp.example", "db-admin",
                               "INC-20458 replication lag remediation", 60)
    print(f"Granted {grant.role} to {grant.principal} — active={grant.is_active()}")
```

### Machine identity: short-lived credential issuance

```yaml
# ci-pipeline.yaml (excerpt) — OIDC federation replaces static cloud keys
steps:
  - name: authenticate-to-cloud
    uses: workload-identity-federation
    with:
      oidc_audience: "https://vault.corp.example"
      role_to_assume: "ci-deploy-readonly"
      token_ttl_seconds: 900
```

Short-lived, audience-scoped tokens (900 seconds in this example) replace
a static access key that would otherwise need manual rotation and, if
leaked, would remain valid indefinitely.

## Validation and Troubleshooting

- **Validate conditional access with both allow and deny test cases.**
  Maintain a test matrix of representative personas (compliant-device
  admin, unmanaged-device contractor, high-risk-sign-in workforce user) and
  confirm each receives the expected decision after every policy change,
  in a staging tenant before production rollout.
- **Common failure: policy exclusion sprawl.** Emergency exclusions added
  during an outage ("exclude executive assistant account from device
  compliance requirement") are frequently never removed. Require an
  expiration date on every conditional access exception and review
  exceptions on a fixed cadence.
- **Common failure: break-glass account drift.** Break-glass credentials
  that are never rotated or tested become unusable exactly when needed.
  Test break-glass access on a quarterly schedule in a controlled window,
  and rotate credentials immediately afterward.
- **Common failure: orphaned service accounts.** Cross-reference the
  identity directory's service account list against a current inventory of
  applications; accounts with no matching owner or application should be
  disabled pending investigation, not left active by default.
- **Diagnosing unexpected MFA prompts or lockouts**: review the identity
  provider's sign-in log for the specific conditional access policy and
  grant control that triggered the decision — most modern IdPs surface a
  per-sign-in policy evaluation trace; do not guess from policy text alone.
- **PAM session brokering failures** typically trace to vault credential
  rotation timing (the broker checked out a credential that rotated before
  the session opened) or network path changes between the broker and
  target; validate the broker-to-target network path separately from the
  vault integration when troubleshooting.

## Security and Best Practices

- Require phishing-resistant MFA (FIDO2/WebAuthn) for all privileged and
  remote-access accounts; treat SMS-based MFA as a legacy fallback only,
  scheduled for deprecation.
- Eliminate standing privileged access wherever JIT elevation is feasible;
  reserve standing access only for accounts that must respond to identity
  system outages.
- Record and retain privileged sessions, and route session recordings to
  the SIEM/detection pipeline described in [Chapter 6](06-security-telemetry-detection-engineering-and-soc-operations.md) so anomalous
  privileged behavior is monitored, not just archived.
- Rotate machine and API credentials automatically, and prefer workload
  identity federation (short-lived, audience-scoped tokens) over static
  secrets wherever the platform supports it.
- Apply the joiner/mover/leaver lifecycle rigorously: access must be
  revoked on the same day as termination, and role changes must trigger a
  re-certification of retained access, not just an addition of new access.
- Conduct periodic access certification (quarterly for privileged roles,
  semi-annually for standard workforce access) with the resource owner —
  not IT — attesting that access remains necessary.
- Treat the identity provider and PAM platform as Tier 0 infrastructure:
  apply the same change control, monitoring, and architecture review
  rigor from [Chapter 1](01-cybersecurity-governance-risk-and-architecture.md) that production business systems receive.

## References and Knowledge Checks

**References**

- NIST SP 800-207, *Zero Trust Architecture*
- NIST SP 800-63B, *Digital Identity Guidelines: Authentication and
  Lifecycle Management*
- CISA, *Zero Trust Maturity Model*
- FIDO Alliance, *FIDO2/WebAuthn Specifications*
- OpenID Foundation, *OpenID Connect Core 1.0*
- CIS Controls v8.1, Control 5 (Account Management) and Control 6 (Access
  Control Management)

**Knowledge Checks**

1. In the NIST SP 800-207 model, what is the difference between the Policy
   Administrator and the Policy Enforcement Point?
2. Why is push-notification MFA considered less phishing-resistant than
   FIDO2/WebAuthn, even though both are "multi-factor"?
3. Describe the difference between standing privileged access, JIT
   elevation, and a break-glass account, and when each is appropriate.
4. Why should machine identities use short-lived, federated credentials
   instead of long-lived API keys?
5. What is the risk of accumulating conditional access policy exceptions
   without expiration dates?
6. Why must break-glass account access be tested on a schedule rather than
   assumed to work?

## Hands-On Lab

**Objective:** Implement and test a just-in-time privileged elevation
workflow, including policy-enforced validation and a negative test for an
over-duration request.

**Prerequisites**

- A workstation with Python 3.11 or later.
- No production identity system access is required — this lab uses the
  local simulation script from the Implementation and Automation section.

**Steps**

1. Create a lab directory and save the `jit_elevation.py` script from this
   chapter:

   ```bash
   mkdir -p ~/labs/vol10-ch02 && cd ~/labs/vol10-ch02
   # save jit_elevation.py here
   ```

2. Run the baseline scenario:

   ```bash
   python3 jit_elevation.py
   ```

3. **Expected result:** Output shows
   `Granted db-admin to alice@corp.example — active=True`, confirming the
   grant is active immediately after issuance.

4. Extend the script to test expiry by adding this block at the end of the
   file (replacing the existing `__main__` block):

   ```python
   if __name__ == "__main__":
       from datetime import datetime, timedelta, timezone

       grant = request_elevation("alice@corp.example", "db-admin",
                                  "INC-20458 replication lag remediation", 60)
       print(f"Granted {grant.role} to {grant.principal} — active={grant.is_active()}")

       future = datetime.now(timezone.utc) + timedelta(minutes=61)
       print(f"After 61 minutes — active={grant.is_active(future)}")
   ```

5. Re-run the script:

   ```bash
   python3 jit_elevation.py
   ```

6. **Expected result:** The second line prints `active=False`, confirming
   the elevation automatically expires after its 60-minute window without
   requiring manual revocation.

7. **Negative test:** Attempt a policy-violating request — no
   justification, and a duration exceeding the 8-hour policy maximum:

   ```bash
   python3 -c "
   from jit_elevation import request_elevation
   request_elevation('bob@corp.example', 'domain-admin', '', 60)
   "
   ```

   **Expected result:** The script raises
   `ValueError: Elevation requests require a justification (ticket reference).`
   Then test the duration guard:

   ```bash
   python3 -c "
   from jit_elevation import request_elevation
   request_elevation('bob@corp.example', 'domain-admin', 'INC-1', 600)
   "
   ```

   **Expected result:**
   `ValueError: Elevation duration exceeds policy maximum of 8 hours.`
   Both failures demonstrate the policy engine rejecting a non-compliant
   elevation request before any credential is ever issued.

**Cleanup**

```bash
cd ~ && rm -rf ~/labs/vol10-ch02
```

## Summary and Completion Checklist

This chapter built the identity and access layer that Zero Trust
architecture depends on: the PDP/PEP pattern from NIST SP 800-207, the
distinct lifecycle needs of workforce, privileged, and machine identities,
phishing-resistant MFA and federation, and the just-in-time privileged
access pattern that replaces standing administrative rights. The hands-on
lab exercised a working elevation-request workflow, including automatic
expiry and policy-enforced rejection of non-compliant requests — the same
validation logic a production PAM platform performs before ever issuing a
privileged credential.

- [ ] I can describe the Policy Engine, Policy Administrator, and Policy
      Enforcement Point roles in NIST SP 800-207.
- [ ] I can explain why FIDO2/WebAuthn resists AiTM phishing that defeats
      OTP and push-based MFA.
- [ ] I can compare standing access, JIT elevation, and break-glass
      accounts and choose the right pattern for a given role.
- [ ] I can write a conditional access policy as structured, reviewable
      configuration.
- [ ] I can explain why machine identities should use short-lived
      federated credentials instead of static keys.
- [ ] I implemented and tested a JIT elevation workflow, including a
      negative test for policy violations, in the hands-on lab.
