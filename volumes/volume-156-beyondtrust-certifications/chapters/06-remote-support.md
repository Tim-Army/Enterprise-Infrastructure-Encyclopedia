# Chapter 06: Remote Support

## Learning Objectives

- Explain BeyondTrust Remote Support and its secure-remote-support role.
- Distinguish Remote Support from Privileged Remote Access.
- Describe granular permissions, session recording, and consent.
- Recognize Remote Support's security model versus consumer remote tools.

*Cert relevance: Remote Support is a Certified Administrator product — secure remote support with the Bomgar heritage.*

## What Remote Support is

**BeyondTrust Remote Support** (the product with the **Bomgar** heritage) provides **secure remote support** — the ability for a help-desk or support technician to **remotely access and control** a user's device to fix a problem. This is the classic "let me take over your screen" support scenario, but built for the enterprise with **security and auditability** at its center. It handles both **attended** support (the user is present and consents) and **unattended** access (to servers or unattended endpoints under policy), always through a **hardened, access-controlled** channel rather than an open remote-desktop port. The lab models the secure-support model.

## Remote Support versus Privileged Remote Access

Remote Support and [PRA (Chapter 5)](05-privileged-remote-access.md) are siblings with different audiences:

| | Serves | Typical use |
|:---|:---|:---|
| **Remote Support** | Help desk / support technicians | Fix an end user's device; troubleshoot |
| **Privileged Remote Access** | Admins / vendors with privileged access | Administer servers/systems |

Both broker access, record sessions, and enforce granular permissions; Remote Support is oriented to **supporting people and their devices**, PRA to **privileged administration of systems**. Knowing which tool fits which job is part of the BeyondTrust picture. The lab contrasts them.

## Granular permissions, recording, and consent

Remote Support's security model rests on:

- **Granular permissions** — a technician gets only the capabilities their role allows (view-only vs full control, file transfer on/off, which systems they may reach).
- **Session recording** — every support session is recorded for audit, exactly as with privileged sessions.
- **Consent** — for attended support, the end user explicitly grants control, and can see and end the session; support is *cooperative*, not covert.
- **A hardened channel** — access runs through the BeyondTrust appliance/service with authentication and encryption, not an exposed RDP/VNC port.

This turns remote support — historically a soft spot, since support tools are powerful and widely targeted — into a **controlled, accountable** function. The lab models permissions and consent.

## Versus consumer remote tools

The contrast is with **consumer/ad-hoc remote tools** (open remote-desktop ports, consumer screen-sharing utilities), which attackers routinely abuse: tech-support scams, exposed RDP, and support-tool compromise are common initial-access vectors. Remote Support replaces these with **authenticated, permissioned, recorded, consent-based** access — the support technician's power is bounded and audited. Enterprise remote support is a **security control**, not just a convenience. The lab synthesizes.

## Hands-On Lab

Python models secure, consent-based support. **Cost:** none.

### Lab 6.1 — Permissioned, consent-based, recorded support

**Objective:** See how Remote Support bounds and audits a session.

```bash
python3 - <<'EOF'
# a help-desk technician's role-bounded capabilities + a consent-gated attended session
ROLE = {
    "technician": "tier1-helpdesk",
    "can_view": True, "can_control": True, "can_transfer_files": False,
    "reachable": ["employee-laptops"], "not_reachable": ["prod-servers", "domain-controller"],
    "records_session": True, "requires_consent": True,
}
def start_session(target_class, user_consents):
    if target_class not in ROLE["reachable"]:
        return f"DENIED — role can't reach {target_class}"
    if ROLE["requires_consent"] and not user_consents:
        return "WAITING — attended support needs the user's explicit consent"
    caps = [c for c in ("view","control") if ROLE[f"can_{c}"]]
    ft = "file-transfer BLOCKED by role" if not ROLE["can_transfer_files"] else "file-transfer ok"
    rec = "RECORDED" if ROLE["records_session"] else "not recorded"
    return f"session started ({'+'.join(caps)}; {ft}; {rec}; user can end anytime)"

print("Tier-1 help-desk technician, role-bounded:\n")
print("  fix an employee laptop, user consents:")
print("    ", start_session("employee-laptops", user_consents=True))
print("  same, but user hasn't consented yet:")
print("    ", start_session("employee-laptops", user_consents=False))
print("  technician tries to reach a production server:")
print("    ", start_session("prod-servers", user_consents=True))
print("\nRemote Support makes support a CONTROLLED, ACCOUNTABLE function:")
print("  GRANULAR PERMISSIONS — tier-1 can view/control laptops but NOT prod servers, and")
print("     file transfer is off for this role. Power is bounded to the job.")
print("  CONSENT — attended support waits for the user's explicit grant; they see it and")
print("     can end it. Support is COOPERATIVE, not covert.")
print("  RECORDING — every session is audited (who supported whom, and did what).")
print("Versus exposed RDP or consumer screen-share tools (routinely abused for tech-support")
print("scams + initial access), this is a SECURITY CONTROL, not just a convenience.")
EOF
```

**Expected result:** A tier-1 technician who can view and control employee laptops (with the user's consent, session recorded) but is denied file transfer and blocked from production servers. The Remote Support lesson is that granular permissions bound the technician's power to the job, consent makes attended support cooperative rather than covert, and recording makes it accountable — turning remote support from a soft spot into a security control versus exposed RDP or consumer tools.

**Negative test:** Using exposed RDP or a consumer screen-sharing tool for enterprise support. Those grant broad, unaudited control, often without consent, and are routinely abused; enterprise Remote Support bounds capabilities by role, requires consent, and records every session.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Remote Support understood — secure, enterprise remote support (the Bomgar heritage).
- [ ] Distinguished from PRA — supporting users' devices versus privileged administration of systems.
- [ ] Granular permissions, session recording, and consent understood as the security model.
- [ ] Remote Support recognized as a security control versus exposed RDP and consumer remote tools.
