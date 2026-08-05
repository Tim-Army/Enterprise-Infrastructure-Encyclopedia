# Chapter 06: Jamf Connect — Identity

## Learning Objectives

- Explain what Jamf Connect does — cloud identity at the Mac login window.
- Understand password synchronization between the cloud IdP and the local account.
- Place Jamf Connect in the zero-trust and conditional-access picture.
- Recognize why local-account/cloud-identity drift is the problem it solves.

*Cert relevance: Jamf Connect is its own product area, appearing in **Jamf Pro** administration and integration topics — the identity half of the Apple-management story.*

## The problem: two identities

A Mac has a **local account** — the user's macOS login, with its own password stored on the device. The organization has a **cloud identity provider** (Okta, Entra ID, Google) — the user's *real* corporate identity, with its own password, MFA, and lifecycle. Historically these are two separate things, and that gap causes real pain:

- The local password and the cloud password **drift apart** — the user changes one, not the other, and gets confused about "which password."
- A new hire needs a **local account created** before they can log in — friction at exactly the wrong moment.
- When someone leaves, disabling their **cloud** identity does nothing to their **local** account — the Mac still logs in.

**Jamf Connect closes the gap**: it brings the cloud identity to the Mac login window, so the corporate identity *is* the login, and keeps the local password synchronized with the cloud one.

## What Jamf Connect does

Two core capabilities:

1. **Cloud identity at the login window.** Instead of a local-only macOS login, the user authenticates against the cloud IdP (with its MFA, its policies) right at the Mac's login screen. A new user's local account is *created on first login* from their cloud identity — no pre-provisioning. This is the [zero-touch](02-apple-management-fundamentals.md) principle extended to identity: the device is ready, and the user's real identity brings them in.

2. **Password synchronization.** Jamf Connect keeps the local macOS account password in sync with the cloud IdP password. Change it in the cloud, and the Mac's local password follows — no more "which password is this?" and no more drift. This matters especially for FileVault, where a stale local password can lock a user out of their own encrypted disk.

## Identity in the zero-trust picture

Jamf Connect is the Apple-side of the identity story this shelf tells repeatedly: **identity is the control plane.** The same principle behind [Okta (LXXVI)](../../volume-076-okta-certifications/README.md), [conditional access in Microsoft (XXXVII)](../../volume-037-microsoft-365-modern-work/README.md), and [SailPoint's IGA (CXXXII)](../../volume-132-sailpoint-certifications/README.md) applies at the Mac login window: authenticate against the real corporate identity, carry its MFA and policies, and tie device access to identity lifecycle so that disabling the cloud account actually locks the user out.

Combined with [Jamf Protect (Chapter 7)](07-jamf-protect-endpoint-security.md) for device compliance signals, this is Apple-native **zero trust**: access decisions from *who you are* (Jamf Connect identity) and *whether your device is healthy* (Jamf Protect compliance), not from network location. The lab models why identity-anchored login beats the drift-prone local-account world.

## Hands-On Lab

Python models identity synchronization. **Cost:** none.

### Lab 6.1 — Password drift: the problem Jamf Connect solves

**Objective:** Watch local and cloud passwords diverge without synchronization.

```bash
python3 - <<'EOF'
import random
random.seed(11)
USERS = 500
# each user has a local Mac password and a cloud IdP password; without sync they drift
class User:
    def __init__(self): self.local = "pw-v1"; self.cloud = "pw-v1"

def cloud_rotation(users, sync):
    """org forces a cloud password change (policy/expiry); does the local follow?"""
    confused = 0
    for u in users:
        u.cloud = "pw-v2"              # user changes cloud password (forced rotation)
        if sync:
            u.local = u.cloud          # Jamf Connect syncs local -> matches
        else:
            pass                       # local stays "pw-v1" -> DRIFT
        if u.local != u.cloud:
            confused += 1
    return confused

print(f"{USERS} users. Org enforces a cloud password rotation (expiry/policy).\n")
without = cloud_rotation([User() for _ in range(USERS)], sync=False)
print("WITHOUT Jamf Connect (local account separate from cloud):")
print(f"   {without} users now have local != cloud password -> DRIFT")
print("   symptoms: 'which password?' confusion, help-desk resets, and worst of all")
print("   FileVault unlock uses the STALE local password -> lockout risk")
print(f"   help-desk tickets: ~{without} (one per confused user)\n")

with_ = cloud_rotation([User() for _ in range(USERS)], sync=True)
print("WITH Jamf Connect (password sync):")
print(f"   {with_} users with drift -> the local password FOLLOWS the cloud change")
print("   one identity, one password; FileVault stays unlockable; zero confusion")
print(f"   help-desk tickets: {with_}\n")
print(f"tickets avoided by sync: {without - with_}")
print("\nThe core problem: a Mac's LOCAL account password and the CLOUD IdP password")
print("are two separate things that DRIFT the moment one changes without the other.")
print("Jamf Connect keeps them synchronized — change the cloud password, the local")
print("one follows. 'Which password is this?' stops being a question, and FileVault")
print("(which unlocks with the local password) never goes stale. Identity becomes")
print("ONE thing at the Mac login window, not two that fall out of step.")
EOF
```

**Expected result:** A cloud password rotation leaving every unsynced user with a drifted local password and a help-desk ticket, versus zero drift with synchronization. The password-drift lesson is the problem Jamf Connect solves — local and cloud passwords are two things that diverge the moment one changes, and syncing them collapses the confusion and the FileVault-lockout risk.

**Negative test:** Assuming a cloud password change updates the Mac's local login. Without Jamf Connect it does not — the local password is separate, drifts stale, and can lock the user out of their FileVault-encrypted disk.

**Cleanup:** None.

### Lab 6.2 — Identity lifecycle: does disabling the cloud account lock the Mac?

**Objective:** See why identity-anchored login matters for offboarding.

```bash
python3 - <<'EOF'
print("A user leaves. IT disables their CLOUD identity (Okta/Entra). Can they still")
print("log into their Mac?\n")

print("LOCAL-ONLY login (no Jamf Connect):")
print("   the Mac login is a LOCAL account, independent of the cloud.")
print("   disabling the cloud identity does NOTHING to the local account.")
print("   -> the ex-user's Mac STILL LOGS IN until someone manually kills the local")
print("      account. On a lost/kept device, that's an open door.\n")

print("CLOUD-ANCHORED login (Jamf Connect):")
print("   the login authenticates against the cloud IdP.")
print("   disable the cloud identity -> the login is DENIED at the window.")
print("   -> offboarding the cloud account offboards the Mac. One lifecycle.\n")

# quantify across a fleet with normal churn
YEARLY_LEAVERS = 120
print(f"with {YEARLY_LEAVERS} leavers/year:")
print(f"   local-only: {YEARLY_LEAVERS} Macs where cloud-disable != login-disabled")
print(f"               -> {YEARLY_LEAVERS} manual local-account cleanups to remember")
print(f"               (each one forgotten = a device that still logs in)")
print(f"   cloud-anchored: 0 gaps — disabling the identity disables the login")
print("\nThis is IDENTITY AS THE CONTROL PLANE (the Okta/SailPoint/conditional-access")
print("lesson) at the Mac login window: tie device access to the identity lifecycle,")
print("so that the ONE action of disabling the corporate identity actually revokes")
print("access to the device. Local-only accounts break that link — the Mac outlives")
print("the identity. Jamf Connect restores it: one identity, one lifecycle, one")
print("place to grant and revoke.")
EOF
```

**Expected result:** Local-only logins surviving cloud-account disablement (requiring manual cleanup that gets forgotten), versus cloud-anchored logins denied the moment the identity is disabled. The identity-lifecycle lesson is the offboarding payoff — anchoring the Mac login to the cloud identity means one disable action revokes device access, closing the gap local-only accounts leave open.

**Negative test:** Relying on cloud-account disablement to lock a Mac with local-only login. It does not — the local account is independent, and the device keeps logging in until someone manually removes it.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The two-identities problem (local account versus cloud IdP) understood as the drift Jamf Connect solves.
- [ ] Cloud identity at the login window and password synchronization understood as the two core capabilities.
- [ ] Jamf Connect placed in the identity-as-control-plane, zero-trust picture alongside Okta and conditional access.
- [ ] The offboarding payoff internalized — anchoring login to the cloud identity closes the local-account lifecycle gap.
