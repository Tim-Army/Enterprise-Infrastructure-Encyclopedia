# Volume XCI Glossary

Definitions for terms introduced in **Volume XCI — Puppet Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Bolt** — Puppet's agentless orchestration tool that runs commands, scripts, tasks, and plans over SSH/WinRM.
- **Catalog** — the compiled, node-specific document of desired state that the primary server builds and the agent applies.
- **Class** — the unit of configuration in Puppet, optionally parameterized, that you include on a node.
- **Code Manager / r10k** — tools that deploy a control repo (a Puppetfile and a Git branch per environment) into Puppet environments.
- **Defined type** — a reusable resource type you can declare many times.
- **Facter / facts** — the tool and the system data it gathers, available as variables in manifests.
- **Forge** — the Puppet Forge, the public registry of reusable modules.
- **Hiera** — Puppet's hierarchical key/value lookup system that separates data from code.
- **Idempotence** — the property that applying a catalog repeatedly converges to the same desired state.
- **Module** — a directory of Puppet code and data in a standard layout (manifests, files, templates, data, metadata.json).
- **Primary server** — the Puppet Enterprise server running Puppet Server (catalog compilation), the console, orchestrator, CA, and PuppetDB.
- **PuppetDB** — the data warehouse storing facts, catalogs, and reports, enabling exported resources and PQL queries.
- **Puppet Certified Professional (PPT-PCP-24)** — Puppet's certification exam (60 questions, 90 minutes, $200, Questionmark).
- **Resource** — the atomic unit of Puppet configuration (`type { 'title': attr => value }`).
- **Resource abstraction** — Puppet's translation of a resource type through a platform-specific provider.
- **Roles and profiles** — the pattern where profiles configure single technologies and one role composes profiles per node.
- **Task / plan** — a single packaged action (task) and a multi-step orchestrated workflow (plan) run by Bolt/Orchestrator.
