# Chapter 07: AD Bridge

## Learning Objectives

- Explain AD Bridge and extending Active Directory to non-Windows systems.
- Describe unified authentication, single sign-on, and Group Policy for Linux/Unix/Mac.
- Understand the consolidation benefit — one identity, one policy.
- Recognize AD Bridge's role in consistent access control.

*Cert relevance: AD Bridge is a Certified Administrator product — extending AD authentication and policy across the estate.*

## Extending Active Directory

**AD Bridge** extends **Active Directory** authentication, single sign-on, and policy to **non-Windows systems** — Linux, Unix, and macOS. In most enterprises, **Active Directory** is the identity authority for Windows: users authenticate to AD, and their group memberships drive access. But Linux/Unix/macOS systems have historically lived **outside** AD, with their **own local accounts** and separate password stores. AD Bridge closes that gap: it lets a Linux, Unix, or Mac system **join the AD domain** and authenticate users against **their existing AD credentials** — so one identity works everywhere. The lab models the consolidation.

## Unified authentication, SSO, and Group Policy

With AD Bridge, a non-Windows host participates in AD much as a Windows host does:

- **Unified authentication** — users log in to Linux/Unix/Mac with their **AD username and password** (via Kerberos), no separate local account.
- **Single sign-on** — the same identity and session context carry across systems.
- **Group Policy** — AD **Group Policy** can apply configuration and security settings to non-Windows hosts, extending centralized policy management beyond Windows.

The result is that the whole estate — Windows *and* Linux/Unix/Mac — is governed by **one directory, one set of credentials, and one policy framework.** The lab models unified authentication.

## The consolidation benefit

The security value is **consolidation**. Scattered **local accounts** on Linux/Unix/Mac systems are a governance nightmare: they multiply, they're rarely reviewed, they don't get disabled when someone leaves, and each is an independent credential to steal. Bringing those systems under AD means:

- **One identity** per person, centrally managed — disable the AD account and access ends *everywhere*, including the Linux fleet.
- **Consistent policy** — the same password rules, group-based access, and controls apply across platforms.
- **Central auditability** — authentication across the estate is visible in one place.

This is the identity-hygiene counterpart to PAM's credential control: fewer, centrally-governed identities are inherently more secure than sprawling local accounts. The lab models the deprovisioning benefit.

## Consistent access control

AD Bridge underpins **consistent access control**: because access on non-Windows systems now derives from **AD group membership**, the same governance that applies to Windows — [identity governance from SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md), group-based least privilege — extends to the Linux/Unix/Mac estate. Identity becomes uniform across the organization rather than fragmented by platform. The lab synthesizes.

## Hands-On Lab

Python models AD-centralized identity. **Cost:** none.

### Lab 7.1 — One identity beats scattered local accounts

**Objective:** See the deprovisioning and consistency benefit of bridging to AD.

```bash
python3 - <<'EOF'
# an employee "jsmith" leaving the company — with vs without AD Bridge
LINUX_UNIX_MAC = ["web01 (Linux)", "db02 (Linux)", "build03 (Unix)", "designer-mac", "jump-host (Linux)"]

print("Employee jsmith leaves. Revoke ALL their access.\n")
print("WITHOUT AD Bridge — scattered LOCAL accounts on each non-Windows host:")
for h in LINUX_UNIX_MAC:
    print(f"   must find + disable local 'jsmith' on {h}  (manual, easy to MISS one)")
print("   + their Windows AD account (separate)")
print("   -> miss ONE host and jsmith retains a working login = an orphaned back door\n")

print("WITH AD Bridge — all hosts authenticate against AD:")
print("   disable ONE AD account 'jsmith'")
print(f"   -> access ends IMMEDIATELY on all {len(LINUX_UNIX_MAC)} non-Windows hosts + Windows")
print("   -> nothing to miss; one identity, one revocation\n")
print("The consolidation benefit: scattered LOCAL accounts multiply, go unreviewed, and")
print("linger after people leave — each an independent credential to steal and an orphan")
print("to miss at offboarding. AD Bridge makes each person ONE AD identity across Windows")
print("AND Linux/Unix/Mac, so central controls (disable-on-exit, group-based access,")
print("password policy, audit) apply everywhere. Fewer, governed identities = more secure.")
EOF
```

**Expected result:** Without AD Bridge, offboarding requires finding and disabling a local account on every non-Windows host (easy to miss one, leaving an orphaned login); with AD Bridge, disabling one AD account ends access everywhere at once. The AD Bridge lesson is that scattered local accounts multiply and linger as independent, unreviewed credentials, while bridging to AD makes each person one governed identity across the whole estate, so central controls apply uniformly.

**Negative test:** Managing Linux/Unix/Mac with independent local accounts alongside AD for Windows. Identities fragment by platform, offboarding misses hosts, and each local account is a separate credential to steal; AD Bridge consolidates to one directory and one revocation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] AD Bridge understood — extending Active Directory authentication and policy to Linux/Unix/Mac.
- [ ] Unified authentication, SSO, and Group Policy for non-Windows systems understood.
- [ ] The consolidation benefit understood — one identity, central deprovisioning, consistent policy.
- [ ] AD Bridge's role in consistent, estate-wide access control recognized.
