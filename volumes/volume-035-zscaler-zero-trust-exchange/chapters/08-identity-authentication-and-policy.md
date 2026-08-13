# Chapter 08: Identity, Authentication, and Policy

## Learning Objectives

- Integrate an **identity provider (IdP)** with Zscaler using **SAML** for
  authentication and **SCIM** for user/group provisioning.
- Explain why identity — users and groups from the IdP — is the anchor of every
  ZIA and ZPA policy.
- Configure authentication settings, including hosted vs. IdP authentication and
  multi-factor via the IdP.
- Build policy that references IdP groups so access follows identity, not IP.
- Diagnose identity failures: SAML assertion mismatch and missing group
  attributes.

## Theory and Architecture

Every policy in the previous chapters referenced *users and groups* — "allow
HR," "block Gambling for Contractors." Those identities come from an **identity
provider**, and getting identity right is a prerequisite for the entire
deployment, not a later step. Zscaler federates authentication to the IdP with
**SAML** and synchronizes the user/group directory with **SCIM**.

### SAML authentication

With **SAML**, Zscaler is the service provider and the IdP (Entra ID, Okta,
Ping, etc.) is the identity authority. When a user needs to authenticate,
Zscaler redirects to the IdP; the IdP authenticates (including MFA) and returns
a signed **SAML assertion** carrying the user's identity and **group
attributes**. Zscaler trusts the assertion because it is signed by the IdP's
certificate. The group attributes in the assertion are what policy matches on,
so the IdP must be configured to *send groups*.

### SCIM provisioning

**SCIM** keeps Zscaler's view of users and groups in sync with the IdP
automatically — new hires appear, leavers are deprovisioned, group membership
changes propagate. Without SCIM (or SAML-pushed groups), Zscaler has no
authoritative directory to write policy against. SCIM provisions the directory;
SAML authenticates the session and asserts group membership at login.

### Authentication settings

Zscaler supports IdP authentication (the norm) and can enforce re-authentication
intervals and device-token binding. MFA is delegated to the IdP — Zscaler
consumes the outcome of the IdP's MFA in the assertion rather than running its
own second factor.

## Design Considerations

- **Send groups in the assertion.** Policy is group-based; if the IdP does not
  release group claims, every user looks group-less and group policy silently
  fails.
- **SCIM for lifecycle, SAML for login.** Use both — SCIM so the directory is
  correct and leavers lose access, SAML so each session is authenticated with
  current MFA.
- **One source of truth.** Keep the IdP authoritative; do not maintain a
  divergent local user list in Zscaler.

## Implementation and Automation

### SAML + SCIM integration (portal shape)

```text
# ZIA/ZPA Portal > Authentication:
#   SAML: upload IdP metadata/certificate; map NameID=email, attribute "groups"
#   SCIM: enable provisioning; give the IdP the SCIM base URL + bearer token; sync users/groups
```

### Inspecting a SAML assertion's group claims

```bash
# A SAML Response is base64-encoded XML. Decode a captured assertion and look
# for the group attribute policy will match on:
python3 - <<'EOF'
import base64
# Illustrative decoded snippet (what to look for in a real captured assertion):
assertion_b64 = base64.b64encode(b'''<saml:AttributeStatement>
  <saml:Attribute Name="groups"><saml:AttributeValue>HR</saml:AttributeValue></saml:Attribute>
</saml:AttributeStatement>''').decode()
xml = base64.b64decode(assertion_b64).decode()
print("groups present:", "groups" in xml, "| HR asserted:", "HR" in xml)
EOF
```

### Group-based policy (shape)

```text
# Any ZIA/ZPA rule references IdP groups:
#   ZPA Access: Allow group "HR" -> HR-App
#   ZIA URL Filtering: Block "Streaming" for group "Contractors"
```

## Validation and Troubleshooting

- **Group policy never matches.** The IdP is not releasing group claims in the
  SAML assertion — fix the attribute mapping at the IdP, not the Zscaler rule.
- **Leaver still has access.** SCIM deprovisioning is not configured; the user
  remains in Zscaler's directory — SCIM is what removes them.
- **Authentication loops.** SAML metadata/certificate mismatch between IdP and
  Zscaler — re-import current metadata.

## Security and Best Practices

- **Delegate MFA to the IdP** and require it — Zscaler consumes the assertion,
  so strong IdP MFA protects every Zscaler session.
- **Automate deprovisioning with SCIM** so access ends when employment does.
- **Match on groups, not individuals**, so policy scales and joins/leaves are
  handled by directory membership.

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Authentication: SAML* and *Provisioning: SCIM* for ZIA
  and ZPA (`help.zscaler.com`).

### Knowledge Checks

- What does SAML provide (authentication) versus SCIM (provisioning)?
- Why must the IdP send group attributes in the SAML assertion?
- How is MFA handled in a Zscaler + IdP integration?
- Why is group-based policy preferable to per-user rules?

## Hands-On Lab

This chapter's labs cover identity — reading a SAML assertion's group claims,
the SCIM lifecycle, and group-based policy. The assertion inspection runs
locally; IdP/portal steps reference the tenant. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.3** — `python3`; a Zscaler tenant + IdP
for portal steps. **Cost:** none.

### Lab 8.1 — Inspect a SAML assertion's group claim (Topic: SAML)

**Objective:** Confirm the IdP asserts the groups policy needs.

```bash
python3 - <<'EOF'
import base64
resp = base64.b64encode(b'<saml:Attribute Name="groups"><saml:AttributeValue>HR</saml:AttributeValue></saml:Attribute>').decode()
xml = base64.b64decode(resp).decode()
assert "groups" in xml and "HR" in xml, "IdP is not asserting group membership"
print("assertion carries group 'HR' -> group policy can match")
EOF
```

**Expected result:** the decoded assertion contains a `groups` attribute with
the user's group — Zscaler matches policy on the groups the IdP asserts at
login, so the IdP must be configured to release group claims or all group-based
policy silently fails.

**Negative test:** an assertion with no `groups` attribute; every user appears
group-less and group rules never match — the fix is the IdP's attribute
mapping, not the Zscaler rule.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — SCIM lifecycle (Topic: Provisioning)

**Objective:** Keep the directory authoritative.

```text
# ZIA/ZPA Portal > Provisioning (SCIM): enable; give the IdP the SCIM URL + bearer token.
# Add a user to group "HR" at the IdP -> appears in Zscaler; disable the user -> deprovisioned.
```

**Expected result:** IdP changes propagate to Zscaler — new users and group
changes appear, disabled users are removed — because SCIM synchronizes the
directory; SAML authenticates sessions but SCIM is what makes leavers lose
access.

**Negative test:** rely on SAML alone with no SCIM; a disabled employee's
Zscaler identity lingers — provisioning/deprovisioning needs SCIM.

**Rollback:** revert lab user/group changes.

### Lab 8.3 — Group-based policy (Topic: Identity-driven policy)

**Objective:** Bind access to IdP groups.

```text
# ZPA Access: Allow group "HR" -> HR-App
# ZIA URL Filtering: Block "Streaming" for group "Contractors"
```

**Expected result:** access and web policy follow IdP group membership, not IP —
identity is the anchor of the zero-trust model, so a join/leave or role change
in the IdP changes Zscaler access automatically.

**Negative test:** write rules against IP ranges instead of groups; policy
breaks the moment addresses change and does not follow the user — identity-based
rules are what make policy portable and correct.

**Rollback:** remove lab rules.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Identity is the anchor of the whole platform: SAML federates authentication and
asserts group membership (with MFA delegated to the IdP), SCIM keeps the
user/group directory authoritative and deprovisions leavers, and every ZIA/ZPA
policy matches on IdP groups so access follows identity rather than IP. Getting
identity right is a prerequisite, not a later step.

- [ ] Can confirm an assertion carries the group claims policy needs.
- [ ] Understands SCIM for lifecycle vs. SAML for login.
- [ ] Writes group-based rather than IP-based policy.
- [ ] Delegates and requires MFA at the IdP.
