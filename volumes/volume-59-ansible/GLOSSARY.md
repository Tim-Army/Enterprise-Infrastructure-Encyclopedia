# Volume LIX Glossary

Definitions for terms used in **Volume LIX — Ansible**, alphabetized.
See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**ansible-core** — The Ansible automation engine (CLI + core modules); current series
2.21.x. Used in Chapters 01 and 09.

**Ansible Vault** — The feature that encrypts variables/files so secrets are safe to
commit, decrypted at runtime. Used in Chapter 07.

**AWX / Ansible Automation Platform** — The open-source (AWX) and Red Hat (AAP) web/API
platform adding RBAC, scheduling, credentials, and audit. Used in Chapter 09.

**Block** — A group of tasks supporting `rescue` (on failure) and `always` (regardless)
handling. Used in Chapter 06.

**Collection** — A namespaced bundle of modules/plugins/roles (`namespace.collection`)
distributed via Galaxy. Used in Chapter 05.

**Execution environment** — A container image bundling ansible-core plus pinned
collections/deps for reproducible runs. Used in Chapter 09.

**Facts** — System data Ansible gathers from hosts (`ansible_facts`). Used in Chapter 04.

**Handler** — A task run only when notified by a changed task, once at the play's end.
Used in Chapter 03.

**Idempotence** — The property that re-running converges to desired state, reporting
`changed` only when it actually changes something. Used in Chapters 01 and 03.

**Inventory** — The definition of managed hosts and groups (static or dynamic). Used in
Chapter 02.

**Module** — A unit of work a task invokes (idempotent, desired-state). Used in Chapter
03.

**Molecule** — The role-testing framework (converge + idempotence + verify). Used in
Chapter 08.

**Playbook** — A YAML file of plays (host groups + ordered tasks). Used in Chapter 03.

**register** — Captures a task's result into a variable for later use. Used in Chapter 04.

**Role** — A reusable, standard-layout unit of automation (tasks/handlers/templates/
defaults/…). Used in Chapter 05.

**Strategy** — How Ansible schedules tasks across hosts (`linear`, `free`, `host_pinned`).
Used in Chapter 09.

**Tag** — A label on tasks enabling targeted `--tags`/`--skip-tags` runs. Used in Chapter
06.

**Template module** — Renders a Jinja2 template to a file using variables/facts. Used in
Chapter 04.
