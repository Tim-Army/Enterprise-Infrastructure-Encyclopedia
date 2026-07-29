# Chapter 05: Actions — CI/CD, Secrets, and Security

## Learning Objectives

- Build a CI/CD pipeline with dependent jobs and environments.
- Use secrets and variables safely.
- Reason about `GITHUB_TOKEN` permissions and OIDC.
- Reuse logic with reusable and composite workflows.
- Complete a walkthrough for each CI/CD-and-security topic.

## Theory and Architecture

Beyond single workflows, **GitHub Actions** builds full **CI/CD** pipelines. Jobs are sequenced with
**`needs`** (build → test → deploy), and deployments target **environments** (with **protection rules**
like required reviewers and wait timers). Sensitive values are stored as **secrets** (encrypted;
referenced via `secrets.NAME`) and non-sensitive config as **variables** — scoped to a repo,
environment, or organization. Each workflow run gets an automatic **`GITHUB_TOKEN`** whose
**permissions** should be minimized (`permissions:` block) — least privilege for what the job actually
needs. For cloud deploys, **OIDC** lets a workflow exchange a short-lived token with a cloud provider
**without storing long-lived cloud keys**. Logic is reused through **reusable workflows** (`workflow_call`)
and **composite actions**. Security hardening — pinning actions, minimal token scope, protected
environments, and OIDC — is a tested theme. This chapter teaches CI/CD and security with hands-on
walkthroughs.

## Design Considerations

Sequence pipeline stages with **`needs`** and gate deploys with **environment protection rules**. Store
credentials as **secrets** (never in code or logs) and prefer **OIDC** over long-lived cloud keys. Set
**`GITHUB_TOKEN` permissions** to the minimum (`contents: read` unless more is needed). Factor shared
logic into **reusable/composite** workflows. Treat pull-request workflows from forks carefully (limited
token, no secrets by default).

## Implementation and Automation

The labs build a dependent pipeline with an environment, use a secret, and minimize the token — the CI/CD
and security skills the Actions exam validates.

## Validation and Troubleshooting

Confirm CI/CD and security:

```text
Pipeline: jobs sequenced with needs (build -> test -> deploy); deploy to environments (protection rules)
Secrets (encrypted, secrets.NAME) + variables; scoped repo/environment/org
GITHUB_TOKEN: minimize with permissions:; OIDC = short-lived cloud creds, no stored keys
Reuse: reusable workflows (workflow_call) + composite actions
```

Common pitfalls: printing a **secret** to the log (masked, but avoid it); and leaving `GITHUB_TOKEN` with
**write-all** default permissions — set least privilege.

## Security and Best Practices

Minimize `GITHUB_TOKEN` permissions, use **OIDC** instead of stored cloud keys, protect deploy
**environments** with required reviewers, and never echo secrets. These defend your own pipeline and
supply chain. All work is authorized.

## Hands-On Lab

CI/CD-and-security walkthroughs. **Shared prerequisites** — a GitHub repo with `gh` and Actions enabled.
**Cost:** none.

### Lab 5.1 — Build a dependent pipeline

**Objective:** Sequence build → deploy with an environment.

```yaml
# .github/workflows/deploy.yml
name: Deploy
on: { push: { branches: [ main ] } }
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [ { run: echo "build" } ]
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production   # protection rules (reviewers) apply here
    steps: [ { run: echo "deploying to prod" } ]
```

```text
# deploy waits for build; if 'production' requires a reviewer, deploy pauses for approval
```

**Expected result:** `deploy` runs only after `build` succeeds and targets the protected `production`
environment.

**Negative test:** run deploy in parallel with build (no `needs`); it may deploy an unbuilt artifact —
add **`needs: build`**.

**Cleanup:** none yet.

### Lab 5.2 — Use a secret safely

**Objective:** Reference an encrypted secret.

```bash
gh secret set API_TOKEN --body "s3cr3t-value"
```

```yaml
# in a workflow step
      - name: Deploy
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: ./deploy.sh   # reads $API_TOKEN; never echo it
```

```text
✓ Set secret API_TOKEN for octocat/repo
```

**Expected result:** the secret injected as an environment variable at run time — encrypted at rest,
masked in logs.

**Negative test:** hardcode the token in the workflow YAML; store it as a **secret** and reference
`secrets.API_TOKEN`.

**Cleanup:**

```bash
gh secret delete API_TOKEN
```

### Lab 5.3 — Minimize GITHUB_TOKEN permissions

**Objective:** Apply least privilege to the run token.

```yaml
# top of workflow: default to read-only, grant more per-job as needed
permissions:
  contents: read
jobs:
  release:
    permissions:
      contents: write      # only this job can push tags/releases
    runs-on: ubuntu-latest
    steps: [ { run: echo "create release" } ]
```

```text
# workflow token is read-only except where explicitly elevated
```

**Expected result:** the token defaults to read-only, with write granted only to the job that needs it —
least privilege.

**Negative test:** leave the default broad permissions; a compromised step could push code or create
releases — set **minimal `permissions`**.

**Cleanup:** none.

### Lab 5.4 — Reason about OIDC for cloud deploys

**Objective:** Avoid stored long-lived cloud keys.

```python
python3 - <<'PY'
options = {
  "Stored cloud keys (secret)": "long-lived AWS/Azure keys in secrets; rotate manually; leak risk",
  "OIDC federation":            "workflow requests a short-lived token from the cloud, trust via claims; no stored keys",
}
for k, v in options.items(): print(f"{k:28}: {v}")
print("Prefer OIDC: no long-lived cloud credentials stored in GitHub")
PY
```

**Expected result:** OIDC as the preferred, keyless approach for cloud deploys — short-lived tokens, no
stored secrets.

**Negative test:** store permanent cloud admin keys as secrets for deploys; use **OIDC** federation for
short-lived, scoped credentials.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub Actions CI/CD sequences jobs with `needs` and gates deploys behind protected environments, injects
encrypted secrets and variables at run time, minimizes `GITHUB_TOKEN` permissions to least privilege,
prefers OIDC over stored cloud keys, and reuses logic through reusable and composite workflows — the
security-hardened pipeline the Actions exam validates.

- [ ] I can build a dependent pipeline with an environment.
- [ ] I can use a secret safely.
- [ ] I can minimize `GITHUB_TOKEN` permissions.
- [ ] I can reason about OIDC for cloud deploys.
- [ ] I completed Labs 5.1–5.4 including each negative test.
