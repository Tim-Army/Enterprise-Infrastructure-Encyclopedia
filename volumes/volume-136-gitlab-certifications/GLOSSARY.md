# Volume CXXXVI — Glossary

| Term | Definition |
|:---|:---|
| **Artifact** | Files a job produces that are guaranteed to later jobs and downloadable; if the pipeline breaks without it, it is an artifact, not cache. |
| **Cache** | Files reused between pipelines to save time (dependencies); a miss must be survivable, and the key determines whether it ever hits. |
| **Certiverse** | The proctoring provider for GitLab's Professional-level exams; Associate exams are unproctored. |
| **DAG (`needs`)** | Declaring per-job dependencies so a job starts as soon as its named jobs finish, rather than waiting for the whole preceding stage. |
| **DAST** | Dynamic application security testing — exercises a running application; fewer false positives than SAST but only covers paths it reaches. |
| **Environment** | A named deployment target GitLab tracks, with history, rollback, and optional protection restricting who may deploy. |
| **Epic** | A group-level body of work spanning issues, possibly across projects — the reason portfolio management is a group-level topic. |
| **Executor** | How a runner runs a job: `docker` (fresh container), `shell` (on the host, an isolation risk), `kubernetes`, and others. |
| **MCP** | Model Context Protocol — the open standard by which the Agent Platform connects agents to external tools; each connection widens capability and blast radius alike. |
| **Merge request (MR)** | GitLab's unit of code review, bundling diff, discussion, approvals, pipeline results, and security findings. |
| **Protected branch** | A branch restricting who may push and merge; an empty push list is what converts code review from convention into control. |
| **Protected variable** | A CI variable exposed only to jobs on protected branches or tags — the control that keeps production credentials out of feature-branch pipelines. |
| **`rules`** | The modern keyword deciding whether a job runs, evaluated first-match-wins; supersedes `only/except`, which must not be mixed with it. |
| **Runner** | The agent that executes CI jobs, defined by scope (shared/group/project) and executor; jobs whose tags match no runner sit pending rather than failing. |
| **SAST** | Static application security testing — reads source without executing it; broad coverage, more false positives, finds what DAST cannot. |
| **Scan execution / result policy** | Group-level enforcement that scanners run and that findings gate merges — placed above the project's CI file because a control the controlled party can edit is not a control. |
| **Scoped label** | A label using `::` syntax that is mutually exclusive within its scope, which is what keeps an issue in exactly one board column. |
| **Secret detection** | Scanning for committed credentials; uniquely, removal does not remediate — rotate first, because history and every clone retain the secret. |
| **Stage** | An ordered pipeline phase; stages run sequentially while jobs within a stage run in parallel, so only the slowest job in a stage affects duration. |
| **Version-based recertification** | GitLab's model in which certifications do not expire but may require revalidation when a major product version materially changes the validated skills. |
