# Chapter 07: GitHub Administration

## Learning Objectives

- Explain organizations, enterprises, and teams.
- Apply role-based access and repository roles.
- Enforce policy with rulesets and branch protection.
- Reason about SAML/SSO, SCIM, and the audit log.
- Complete a walkthrough for each administration topic.

## Theory and Architecture

**GitHub Administration** validates running a healthy GitHub environment at scale. GitHub's hierarchy is
**enterprise → organizations → repositories**, with **teams** grouping members for access. Access is
**role-based**: organization roles (member, owner) and **repository roles** (read, triage, write,
maintain, admin), assignable to users or **teams** (which can nest). Policy is enforced with **rulesets**
and **branch protection** — requiring pull-request review, status checks, signed commits, or linear
history before merging to protected branches. Identity integrates through **SAML single sign-on (SSO)**
and **SCIM** provisioning so accounts follow the corporate directory. The **audit log** records
administrative and security events for compliance. Administrators also manage **runner groups**, **GHAS**
enablement (Chapter 06), and organization-wide **policies** (repository creation, visibility, Actions
permissions). This chapter teaches administration with hands-on `gh`/API walkthroughs and policy
reasoning.

## Design Considerations

Grant access through **teams** with the **least repository role** needed, not individual grants. Protect
important branches with **rulesets** requiring review and checks. Enforce **SAML SSO** (and SCIM) so
access follows the directory and deprovisions on offboarding. Restrict org **policies** (who can create
public repos, which Actions are allowed). Monitor the **audit log**. Use runner groups to control where
self-hosted runners are used.

## Implementation and Automation

The labs assign a repository role to a team, enforce a branch-protection ruleset, and reason about
SSO/audit — the administration the GitHub Administration exam validates.

## Validation and Troubleshooting

Confirm administration:

```text
Hierarchy: enterprise -> organizations -> repositories; teams group members (nestable)
Roles: org (member/owner) + repo (read/triage/write/maintain/admin); assign to teams (least privilege)
Policy: rulesets / branch protection (require PR review, checks, signed commits, linear history)
Identity: SAML SSO + SCIM provisioning; audit log records admin/security events
```

Common pitfalls: granting **admin** repo role broadly (use `write`/`maintain`); and no **branch
protection** on `main` (anyone can force-push) — require review and checks via a ruleset.

## Security and Best Practices

Least-privilege team roles, enforced SSO/SCIM, protected branches, and audit-log review are the
administrative baseline that keeps the environment secure — defensive management of your own org. All
work is authorized administration.

## Hands-On Lab

Administration walkthroughs. **Shared prerequisites** — an organization you administer, `gh`, and API
access; `python3` for policy reasoning. **Cost:** none.

### Lab 7.1 — Assign a repository role to a team

**Objective:** Grant least-privilege access through a team.

```bash
gh api -X PUT orgs/acme/teams/backend/repos/acme/service-api \
  -f permission=write
gh api orgs/acme/teams/backend/repos/acme/service-api --jq '.permissions'
```

```text
{ "pull": true, "triage": true, "push": true, "maintain": false, "admin": false }
```

**Expected result:** the `backend` team granted **write** (push) on the repo — least privilege, not
admin.

**Negative test:** grant the team `admin` for convenience; use **write**/**maintain** unless they truly
administer the repo.

**Cleanup:**

```bash
gh api -X DELETE orgs/acme/teams/backend/repos/acme/service-api
```

### Lab 7.2 — Enforce a branch-protection ruleset

**Objective:** Require review and checks on `main`.

```bash
gh api -X POST repos/acme/service-api/rulesets --input - <<'JSON'
{ "name": "protect-main", "target": "branch", "enforcement": "active",
  "conditions": { "ref_name": { "include": ["refs/heads/main"], "exclude": [] } },
  "rules": [ { "type": "pull_request", "parameters": { "required_approving_review_count": 1 } },
             { "type": "required_status_checks",
               "parameters": { "required_status_checks": [ { "context": "CI" } ] } } ] }
JSON
```

```text
{ "name": "protect-main", "enforcement": "active" }
```

**Expected result:** a ruleset requiring 1 approval and a passing `CI` check before merging to `main`.

**Negative test:** leave `main` unprotected; anyone with write can push or force-push — enforce a
**ruleset**.

**Cleanup:** delete the ruleset via the API/UI if not needed.

### Lab 7.3 — Reason about SSO and provisioning

**Objective:** Tie access to the corporate directory.

```python
python3 - <<'PY'
controls = {
  "SAML SSO":   "members authenticate via the IdP; org access requires a valid SSO session",
  "SCIM":       "provision/deprovision accounts + team membership from the IdP automatically",
  "Result":     "offboarding in the IdP removes GitHub access; no orphaned accounts",
}
for k, v in controls.items(): print(f"{k:10}: {v}")
print("Enforce SSO + SCIM so GitHub access follows the directory lifecycle")
PY
```

**Expected result:** SAML SSO plus SCIM tying GitHub access to the IdP — automatic deprovisioning on
offboarding.

**Negative test:** manage members by hand without SSO/SCIM; leavers keep access — enforce **SSO + SCIM**.

**Cleanup:** none.

### Lab 7.4 — Review the audit log

**Objective:** Track administrative and security events.

```bash
gh api "orgs/acme/audit-log?phrase=action:repo.create&per_page=3" \
  --jq '.[] | {action, actor, repo, created_at}'
```

```text
{ "action": "repo.create", "actor": "carol", "repo": "acme/new-svc", "created_at": "2026-07-29T10:00:00Z" }
```

**Expected result:** audit-log entries for administrative events (here, repo creation) — visibility for
compliance.

**Negative test:** rely on memory for who changed what; query the **audit log** for an authoritative
record.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub Administration manages the enterprise → organization → repository hierarchy with team-based,
least-privilege repository roles; enforces policy through rulesets and branch protection (required
review, checks, signed commits); ties identity to the directory with SAML SSO and SCIM; and audits
administrative and security events — the healthy environment the Administration exam validates.

- [ ] I can explain organizations, enterprises, and teams.
- [ ] I can assign a least-privilege repository role to a team.
- [ ] I can enforce a branch-protection ruleset.
- [ ] I can reason about SSO, SCIM, and the audit log.
- [ ] I completed Labs 7.1–7.4 including each negative test.
