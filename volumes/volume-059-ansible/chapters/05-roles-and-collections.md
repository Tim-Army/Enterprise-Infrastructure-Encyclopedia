# Chapter 05: Roles and Collections

## Learning Objectives

- Structure reusable automation as roles.
- Scaffold and use a role.
- Install collections from Ansible Galaxy.
- Manage dependencies with requirements.yml.
- Complete a walkthrough for each reuse skill.

## Theory and Architecture

As playbooks grow, **roles** organize them into reusable units with a standard directory
layout: **`tasks/`**, **`handlers/`**, **`templates/`**, **`files/`**, **`vars/`**,
**`defaults/`**, and **`meta/`**. A play includes a role and its tasks/handlers/vars load
automatically. **Collections** are the modern packaging/distribution format — bundles of
modules, plugins, and roles namespaced as `namespace.collection` (e.g.,
`community.general`, `ansible.posix`) — installed from **Ansible Galaxy** or a private
hub, with dependencies declared in **`requirements.yml`**.

## Design Considerations

Factor common automation into **roles** (with sensible `defaults/`), share via Galaxy or a
private hub, and pin collection/role versions in **`requirements.yml`** for reproducibility.
Use the **FQCN** (fully qualified collection name) for modules to avoid ambiguity.

## Implementation and Automation

The labs scaffold a role, use it, install a collection, and pin requirements.

## Validation and Troubleshooting

Confirm the model:

```text
Role dirs: tasks/ handlers/ templates/ files/ vars/ defaults/ meta/. Include with 'roles:' or import/include_role.
Collections: namespace.collection (FQCN). Install: ansible-galaxy collection install; pin in requirements.yml.
```

Common pitfalls: copy-pasting tasks instead of a **role**; and unpinned collections
(non-reproducible).

## Security and Best Practices

Reuse with **roles** and **collections**, pin versions in **`requirements.yml`**, use
**FQCN** module names, and vet third-party content before installing. Keep role defaults
overridable.

## Hands-On Lab

Reuse walkthroughs. **Shared prerequisites** — ansible-core; `ansible-galaxy`. **Cost:**
none.

### Lab 5.1 — Scaffold a role

**Objective:** Create the role skeleton.

```bash
ansible-galaxy init roles/webserver
ls roles/webserver
```

**Expected result:** the standard role directories (**tasks, handlers, defaults, …**) — a
reusable unit.

**Negative test:** put everything in one giant playbook; a **role** structures and reuses
it — factor it out.

**Cleanup:** `rm -rf roles`.

### Lab 5.2 — Use a role

**Objective:** Include a role in a play.

```yaml
# add a task to roles/webserver/tasks/main.yml first:
#   - ansible.builtin.debug: { msg: "webserver role ran" }
- hosts: localhost
  connection: local
  roles:
    - webserver
```

**Expected result:** the role's tasks run as part of the play — role inclusion.

**Negative test:** duplicate the role's tasks inline in every play; **include the role** to
stay DRY.

**Cleanup:** none.

### Lab 5.3 — Install a collection

**Objective:** Add a Galaxy collection.

```bash
ansible-galaxy collection install community.general
ansible-doc -l community.general 2>/dev/null | head -3
```

**Expected result:** the **community.general** collection installed and its modules
listable — extended module set.

**Negative test:** call a module from a collection you haven't installed; install the
**collection** first (or it's not found).

**Cleanup:** none.

### Lab 5.4 — Pin dependencies

**Objective:** Declare reproducible requirements.

```yaml
# requirements.yml
collections:
  - name: community.general
    version: ">=9.0.0"
  - name: ansible.posix
```

```bash
ansible-galaxy collection install -r requirements.yml
```

**Expected result:** the pinned collections installed from **`requirements.yml`** —
reproducible dependencies.

**Negative test:** install collections ad hoc with no file; **requirements.yml** makes the
set reproducible across machines/CI.

**Cleanup:** `rm -f requirements.yml`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Roles package reusable automation in a standard layout; collections (FQCN, from Galaxy)
distribute modules/plugins/roles, pinned in requirements.yml. This chapter scaffolded a
role, used it, installed a collection, and pinned requirements.

- [ ] I can scaffold a role with ansible-galaxy.
- [ ] I can include a role in a play.
- [ ] I can install a Galaxy collection.
- [ ] I can pin dependencies in requirements.yml.
- [ ] I completed Labs 5.1–5.4 including each negative test.
