# Chapter 04: Module Authoring

## Learning Objectives

- Explain module structure and metadata.
- Use modules from the Puppet Forge.
- Apply the roles and profiles pattern.
- Test modules with puppet-lint and rspec-puppet.
- Complete a walkthrough for each module-authoring topic.

## Theory and Architecture

The **Module Authoring** domain covers packaging Puppet code. A **module** is a directory with a standard
layout: **`manifests/`** (classes and defined types; `init.pp` holds the module's main class),
**`files/`** (static files served to nodes), **`templates/`** (EPP/ERB templates), **`data/`** (Hiera
data, Chapter 05), **`functions/`**, **`examples/`**, and **`metadata.json`** (name, version,
dependencies, supported OSes). The autoloader maps class names to files (`apache::vhost` →
`apache/manifests/vhost.pp`). The **Puppet Forge** is the public registry of reusable modules (install
with `puppet module install`). The **roles and profiles** pattern organizes code: a **profile** wraps and
configures a single technology (e.g., `profile::apache`), a **role** composes profiles to describe a
whole machine (e.g., `role::webserver` includes several profiles), and nodes are classified by **exactly
one role**. Modules are tested with **puppet-lint** (Style Guide) and **rspec-puppet** (catalog unit
tests). This chapter teaches module authoring with hands-on walkthroughs.

## Design Considerations

Keep modules **single-purpose** and Forge-quality (metadata, tests, README). Use **Forge** modules for
common technologies rather than reinventing them (but pin versions and review). Adopt **roles and
profiles**: technology config in **profiles**, machine composition in **roles**, one role per node. Lint
and **rspec-puppet** test before deploying. Follow the autoloader naming convention.

## Implementation and Automation

The labs scaffold a module, reason about a Forge install, structure a role/profile, and lint code — the
module authoring the domain validates.

## Validation and Troubleshooting

Confirm module authoring:

```text
Module: manifests/ (init.pp + classes) + files/ + templates/ + data/ + metadata.json
Autoloader: apache::vhost -> apache/manifests/vhost.pp
Forge: reusable modules (puppet module install author-name); pin + review
Roles & profiles: profile = one technology config; role = composed profiles; ONE role per node
Test: puppet-lint (Style Guide) + rspec-puppet (catalog unit tests)
```

Common pitfalls: putting business logic in a **role** (it should only compose profiles); and using a
Forge module without **pinning** its version or reviewing it.

## Security and Best Practices

Review and pin **Forge** modules (supply-chain), keep profiles least-privilege, and test before deploy.
Modular, tested code is safer to change. All work is authorized administration.

## Hands-On Lab

Module-authoring walkthroughs. **Shared prerequisites** — open-source Puppet 8, `puppet module`, and
`puppet-lint` (gem). **Cost:** none.

### Lab 4.1 — Scaffold a module

**Objective:** Create the standard layout.

```bash
mkdir -p demo/{manifests,files,templates,data}
cat > demo/metadata.json <<'JSON'
{ "name": "me-demo", "version": "0.1.0",
  "dependencies": [], "operatingsystem_support": [ { "operatingsystem": "Ubuntu" } ] }
JSON
cat > demo/manifests/init.pp <<'PP'
class demo { notify { 'demo module loaded': } }
PP
find demo -type f
```

```text
demo/metadata.json
demo/manifests/init.pp
```

**Expected result:** a module with `manifests/init.pp` and `metadata.json` — the standard structure the
autoloader expects.

**Negative test:** put the class in `demo/demo.pp`; the autoloader looks in **`manifests/init.pp`** — use
the standard layout.

**Cleanup:**

```bash
rm -rf demo
```

### Lab 4.2 — Reason about a Forge install

**Objective:** Reuse a trusted module.

```python
python3 - <<'PY'
# puppet module install puppetlabs-ntp --version 10.1.0
mod = {"slug": "puppetlabs-ntp", "version": "10.1.0 (pinned)",
       "why": "maintained, tested NTP module vs writing your own",
       "review": "check metadata, dependencies, and the code before use"}
for k, v in mod.items(): print(f"{k:8}: {v}")
PY
```

**Expected result:** a pinned Forge module reused instead of hand-writing NTP config — with review.

**Negative test:** `puppet module install` without a version and auto-update; **pin** the version and
review changes.

**Cleanup:** none.

### Lab 4.3 — Structure roles and profiles

**Objective:** Compose a machine from profiles.

```bash
cat > /tmp/rp.pp <<'PP'
# profile: configures one technology
class profile::base { include ntp }
class profile::web  { package { 'nginx': ensure => installed } }
# role: composes profiles for a whole machine (one role per node)
class role::webserver {
  include profile::base
  include profile::web
}
PP
puppet parser validate /tmp/rp.pp && echo "valid roles/profiles"
```

```text
valid roles/profiles
```

**Expected result:** profiles configuring technologies and a role composing them — the standard
organization.

**Negative test:** classify a node with five profiles directly and no role; use **one role** that
composes them.

**Cleanup:**

```bash
rm -f /tmp/rp.pp
```

### Lab 4.4 — Lint module code

**Objective:** Enforce the Style Guide.

```bash
cat > /tmp/bad.pp <<'PP'
class bad { file { "/tmp/x": ensure => present, mode => 644 } }
PP
puppet-lint /tmp/bad.pp
```

```text
WARNING: mode should be represented as a quoted octal value, e.g. '0644' (mode_string)
WARNING: double quoted string containing no variables (double_quoted_strings)
```

**Expected result:** puppet-lint flagging Style-Guide violations (unquoted mode, needless double quotes)
— the idiomatic-code check.

**Negative test:** ship unlinted, non-idiomatic code; run **puppet-lint** (and rspec-puppet) first.

**Cleanup:**

```bash
rm -f /tmp/bad.pp
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Puppet modules package code in a standard layout (manifests, files, templates, data, metadata.json) that
the autoloader maps by name; the Forge supplies reusable modules; the roles-and-profiles pattern puts
technology config in profiles composed by one role per node; and puppet-lint plus rspec-puppet enforce
the Style Guide and test catalogs before deployment.

- [ ] I can scaffold a module with the standard layout.
- [ ] I can reason about a pinned Forge install.
- [ ] I can structure roles and profiles.
- [ ] I can lint module code.
- [ ] I completed Labs 4.1–4.4 including each negative test.
