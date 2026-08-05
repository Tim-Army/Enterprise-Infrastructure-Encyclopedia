# Chapter 05: Privileged Remote Access

## Learning Objectives

- Explain privileged remote access (PRA) and the VPN problem it solves.
- Describe brokered, least-privilege access without exposing the network.
- Understand credential injection — users never see the credentials.
- Recognize PRA for third-party/vendor access.

*Cert relevance: Privileged Remote Access is a Certified Administrator product — securing privileged sessions without a VPN.*

## The VPN problem

**Privileged Remote Access (PRA)** secures **remote privileged access** — administrators and, especially, **third parties/vendors** connecting to internal systems — **without a VPN.** The VPN problem is that a VPN typically drops the remote user **onto the network** with broad reachability; a compromised vendor laptop on a VPN can then scan and reach far more than the one system it needed. VPNs also distribute credentials and offer little session-level control. PRA replaces this with **brokered, least-privilege access to specific systems** — the user reaches only the exact target they're authorized for, and nothing else on the network is exposed. This is [ZTNA (zero trust network access)](../../volume-150-ping-identity-certifications/README.md) applied specifically to **privileged** sessions. The lab models the difference.

## Brokered least-privilege access

With PRA, access is **brokered**: the user connects to the PRA appliance/service, is authenticated and authorized, and is then connected **only to the specific system and protocol** they're permitted — RDP to one server, SSH to another — for the duration of an approved session. The internal network is **never directly exposed**; there is no broad network foothold to abuse. Access is scoped per-user, per-system, per-time, and every session is **recorded and monitorable** (as with [Password Safe's session management, Chapter 3](03-password-safe.md)). This is least privilege applied to remote connectivity: reach exactly what you need, nothing more. The lab models brokering.

## Credential injection

A defining PRA feature is **credential injection**: when the session opens, PRA **injects the privileged credential** into it directly (pulled from the vault), so the remote user — often an outside vendor — **never sees or holds the credential.** The vendor does their work on the target system, but the admin password for that system was never disclosed to them. This is powerful for third-party access: you grant a contractor the ability to *work on* a system without ever giving them its credentials, and when the engagement ends there is nothing for them to retain, leak, or reuse. Credential injection is the remote-access expression of the [never-expose-the-credential principle (Chapter 3)](03-password-safe.md). The lab models injection.

## Third-party and vendor access

PRA's sharpest use case is **vendor/third-party privileged access** — the hardware vendor who needs to service a system, the software partner debugging in production, the outsourced IT team. These are high-risk (you don't control their endpoints or their staff) and a frequent breach vector. PRA lets you grant them **scoped, credential-injected, recorded, time-bounded** access to exactly the systems they need — a controlled alternative to hosting a wide-open VPN account or, worse, sharing an admin password over email. The lab synthesizes.

## Hands-On Lab

Python models brokered access and credential injection. **Cost:** none.

### Lab 5.1 — Brokered, credential-injected access vs a VPN

**Objective:** Contrast a VPN foothold with PRA's scoped session.

```bash
python3 - <<'EOF'
NETWORK = ["db-prod-01", "app-prod-01", "app-prod-02", "domain-controller",
           "finance-fileserver", "backup-server", "hr-database"]
# a vendor needs to service exactly ONE system:
authorized_target = "app-prod-01"

print("A VENDOR needs to service ONE system: app-prod-01.\n")
print("VPN approach:")
print(f"   vendor laptop lands ON the network -> can reach ALL {len(NETWORK)} systems:")
print(f"      {NETWORK}")
print(f"   + vendor is given app-prod-01's admin PASSWORD (now on their laptop forever)")
print(f"   -> compromised vendor endpoint = whole network exposed + a leaked credential\n")

print("PRA approach (brokered + credential injection):")
reachable = [authorized_target]
print(f"   vendor authenticates to PRA -> connected ONLY to: {reachable}")
print(f"   the other {len(NETWORK)-1} systems are NOT exposed to them at all")
print(f"   credential for app-prod-01 is INJECTED into the session — vendor never sees it")
print(f"   session is recorded + time-bounded; ends -> nothing retained\n")
print(f"   network exposure reduced from {len(NETWORK)} systems to {len(reachable)}")
print("\nPRA = ZTNA for PRIVILEGED sessions: reach EXACTLY the authorized target (no network")
print("foothold), with the credential INJECTED (never disclosed). You grant the vendor the")
print("ability to WORK ON a system without ever giving them its password or the run of your")
print("network — and when they're done, there's nothing to leak or reuse. The safe answer")
print("to third-party privileged access, replacing wide-open VPNs and emailed passwords.")
EOF
```

**Expected result:** A VPN exposing all seven network systems plus a disclosed credential, versus PRA connecting the vendor only to the one authorized target with the credential injected (never seen) and the session recorded and time-bounded. The PRA lesson is that it is ZTNA for privileged sessions — the user reaches exactly the authorized system with no network foothold, credential injection means outside vendors never hold the password, and nothing is retained when the session ends.

**Negative test:** Giving a third-party vendor a VPN account and the target's admin password. That grants broad network reach and leaves a credential on an endpoint you don't control; PRA brokers access to just the target and injects the credential so it is never disclosed.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] PRA understood — secure remote privileged access without a VPN's broad network foothold.
- [ ] Brokered least-privilege access understood — reach exactly the authorized system, nothing more.
- [ ] Credential injection understood — the user (often a vendor) never sees or holds the credential.
- [ ] PRA's third-party/vendor-access use case recognized as the safe alternative to VPNs and shared passwords.
