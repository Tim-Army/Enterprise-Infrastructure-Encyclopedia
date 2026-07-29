# Volume LXXXIX Glossary

Definitions for terms introduced in **Volume LXXXIX — GitHub Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Action** — a reusable unit of automation referenced by a workflow step's `uses` (from a repo, the Marketplace, or a composite action).
- **Branch protection / ruleset** — rules that must pass (review, checks, signed commits) before merging to a protected branch.
- **CodeQL** — GitHub's static-analysis engine that queries code as a database to find vulnerabilities (code scanning).
- **Composite action** — an action that bundles multiple steps for reuse.
- **Dependabot** — GitHub's tool that alerts on vulnerable dependencies and opens update pull requests.
- **GHAS (GitHub Advanced Security)** — the suite of code scanning, secret scanning, and dependency features for securing your own code.
- **GITHUB_TOKEN** — the automatic, scoped token issued to each workflow run, whose permissions should be minimized.
- **gh CLI** — GitHub's official command-line interface.
- **Job** — a set of steps in a workflow that runs on a single runner; jobs run in parallel unless sequenced with `needs`.
- **Matrix** — a workflow strategy that runs a job across multiple versions/OSes in parallel.
- **OIDC** — OpenID Connect federation that lets a workflow obtain short-lived cloud credentials without stored keys.
- **Pull request (PR)** — a proposal to merge a branch, the unit of review on GitHub.
- **Push protection** — a secret-scanning feature that blocks a push containing a detected secret.
- **Reusable workflow** — a workflow callable from other workflows via `workflow_call`.
- **Ruleset** — a modern, flexible policy object enforcing rules on branches/tags.
- **Runner** — the machine (GitHub-hosted or self-hosted) that executes a workflow job.
- **SAML SSO / SCIM** — single sign-on authentication and automated user provisioning tied to a corporate identity provider.
- **Secret** — an encrypted value stored in GitHub and referenced in workflows via `secrets.NAME`.
- **Workflow** — a YAML file in `.github/workflows/` that runs jobs in response to events.
