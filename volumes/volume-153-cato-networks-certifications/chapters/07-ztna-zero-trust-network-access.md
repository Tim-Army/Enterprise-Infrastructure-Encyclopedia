# Chapter 07: ZTNA — Zero Trust Network Access

## Learning Objectives

- Explain zero trust and why "never trust, always verify" replaces perimeter trust.
- Understand ZTNA and how it differs from VPN.
- Describe per-application, identity-based access and the reduced attack surface.
- Recognize ZTNA as the modern replacement for remote-access VPN.

*Cert relevance: ZTNA is the subject of the **Zero Trust** certification and core to **SASE Expert** and **SSE**.*

## Zero trust: never trust, always verify

The old perimeter model was **implicitly trusting**: once you were *on the network* (through the VPN, or in the office), you were trusted to reach lots of things. This is dangerous — a single compromised device or stolen VPN credential gives an attacker broad **lateral movement** across the internal network, because being "inside" conferred trust.

**Zero trust** inverts this: **never trust, always verify.** No user or device is trusted by virtue of network location; *every* access request is authenticated, authorized, and continuously verified, and access is granted at **least privilege** — only to the specific resource needed, only for as long as needed. Trust is earned per-request from *identity and context*, not granted by network position. This is the same [identity-as-the-control-plane](../../volume-150-ping-identity-certifications/chapters/02-identity-and-access-management-fundamentals.md) principle from the identity volumes, applied to network access.

## ZTNA versus VPN

**ZTNA** (Zero Trust Network Access) is the concrete technology, and it is the **modern replacement for the remote-access VPN.** The difference is fundamental:

| | **VPN** | **ZTNA** |
|:---|:---|:---|
| Grants | Access to the *network* | Access to specific *applications* |
| Trust model | On the VPN = trusted, broad reach | Per-request, identity-verified, least-privilege |
| Attack surface | The whole internal network | Only the authorized apps (rest is invisible) |
| Visibility | Apps are network-reachable | Apps are *hidden* until authorized |

A **VPN** drops the remote user *onto the network*, where they can reach broadly — so a compromised VPN user is a compromised network. **ZTNA** connects a verified user to *only the specific applications they are authorized for*, and everything else is **invisible** (not just blocked — undiscoverable). An attacker with stolen credentials reaches only what that identity was authorized for, with no lateral movement and no visibility of the rest. The lab models the difference.

## Reduced attack surface

The security win is a **dramatically reduced attack surface.** With VPN, the internal network is exposed to anyone who gets on it; the attack surface is *everything*. With ZTNA, applications are **not exposed to the network at all** — they are reached only through the ZTNA broker after identity verification, so an unauthorized user cannot even *see* them to attack them. This "**dark**" posture (resources invisible until authorized) plus least-privilege access is what makes ZTNA the zero-trust remote-access model, and why organizations are replacing VPNs with it. In SASE, ZTNA is delivered from the same converged cloud as everything else. The lab quantifies the surface reduction.

## Hands-On Lab

Python models ZTNA versus VPN. **Cost:** none.

### Lab 7.1 — ZTNA least-privilege versus VPN broad access

**Objective:** See how a compromised credential's blast radius differs under VPN and ZTNA.

```bash
python3 - <<'EOF'
# internal resources, and what a "sales" user is actually authorized for
RESOURCES = ["crm", "email", "wiki", "finance-db", "hr-system", "source-code",
             "prod-servers", "admin-panel", "customer-db", "backups"]
SALES_AUTHORIZED = {"crm", "email", "wiki"}   # least privilege: only what sales needs

print("A SALES user's credential is compromised. What can the attacker reach?\n")
print("VPN model (user is dropped ONTO the network):")
print(f"   the VPN grants access to the NETWORK -> the attacker can reach/scan ALL")
print(f"   {len(RESOURCES)} internal resources: {RESOURCES}")
print(f"   -> attack surface = {len(RESOURCES)} resources; lateral movement to finance-db,")
print("      source-code, prod-servers, customer-db, backups... the whole network.\n")
print("ZTNA model (user connects only to AUTHORIZED apps, rest is INVISIBLE):")
print(f"   the sales identity is authorized for: {sorted(SALES_AUTHORIZED)}")
invisible = [r for r in RESOURCES if r not in SALES_AUTHORIZED]
print(f"   the attacker reaches ONLY those {len(SALES_AUTHORIZED)} apps.")
print(f"   the other {len(invisible)} are INVISIBLE (not blocked — UNDISCOVERABLE):")
print(f"      {invisible}")
print(f"   -> attack surface = {len(SALES_AUTHORIZED)} apps; NO lateral movement, NO")
print("      visibility of finance-db/source-code/customer-db/backups to even attack.\n")
reduction = 100*(len(RESOURCES)-len(SALES_AUTHORIZED))/len(RESOURCES)
print(f"   attack surface reduced by {reduction:.0f}% ({len(RESOURCES)} -> {len(SALES_AUTHORIZED)} reachable)")
print("\nThe difference: VPN grants access to the NETWORK (broad, trusted-once-on),")
print("so a stolen sales credential can reach and pivot across EVERYTHING. ZTNA grants")
print("access to specific APPLICATIONS by verified identity, at least privilege — the")
print("sales user reaches CRM/email/wiki and nothing else, and the rest is DARK")
print("(undiscoverable). Same stolen credential, blast radius cut from 'the whole")
print("network' to '3 apps.' That's why ZTNA replaces the VPN: never trust network")
print("location, verify every request, grant least privilege. Zero trust, applied.")
EOF
```

**Expected result:** A compromised sales credential reaching the entire internal network under VPN but only three authorized apps under ZTNA, with the rest invisible — a large attack-surface reduction. The ZTNA lesson is that VPN grants broad network access (so a stolen credential can pivot everywhere) while ZTNA grants least-privilege per-application access by verified identity with everything else dark, cutting the blast radius dramatically.

**Negative test:** Using a VPN for remote access in a zero-trust world. Once on the VPN, a compromised user reaches and pivots across the whole internal network; ZTNA connects verified identities to only authorized applications and hides the rest, eliminating the lateral movement.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Zero trust understood as "never trust, always verify" — trust from identity and context, not network location.
- [ ] ZTNA distinguished from VPN — per-application least-privilege access versus broad network access.
- [ ] The reduced attack surface understood — authorized apps only, everything else invisible (dark).
- [ ] ZTNA recognized as the modern VPN replacement, delivered from the converged SASE cloud.
