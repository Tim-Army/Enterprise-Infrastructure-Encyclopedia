# Chapter 02: Inventory and Connections

## Learning Objectives

- Build static inventories with groups.
- Assign variables with host_vars and group_vars.
- Use dynamic inventory from a source of truth.
- Configure connection settings.
- Complete a walkthrough for each inventory skill.

## Theory and Architecture

The **inventory** defines the hosts Ansible manages and how they're grouped. A **static
inventory** is an INI or YAML file listing hosts and **groups** (with special groups
`all` and `ungrouped`); **dynamic inventory** generates the list at runtime from a source
of truth (cloud APIs, NetBox) via an inventory plugin. Variables attach to hosts and
groups through **`host_vars/`** and **`group_vars/`** directories (or inline), following a
defined precedence. **Connection settings** (`ansible_host`, `ansible_user`,
`ansible_connection`) control how Ansible reaches each host — SSH by default, or `network_cli`/
API for network gear.

## Design Considerations

Group hosts by **function/role/location** so plays target the right set. Keep variables in
**`group_vars/`** and **`host_vars/`** (version-controlled), not inline. Use **dynamic
inventory** in cloud/dynamic environments so the host list never drifts.

## Implementation and Automation

The labs build a static inventory, assign group/host vars, and describe dynamic inventory.

## Validation and Troubleshooting

Confirm the model:

```text
Static: inventory.ini/yaml with [group] hosts. Dynamic: inventory plugin from an API/SoT.
Vars: group_vars/<group>.yml, host_vars/<host>.yml (precedence-ordered).
Connection: ansible_host/user/connection; verify with ansible-inventory --list.
```

Common pitfalls: variables scattered inline (hard to manage); and a static inventory that
drifts from reality.

## Security and Best Practices

Group by **function**, keep vars in **group_vars/host_vars** under version control, use
**dynamic inventory** from a source of truth where possible, and store connection secrets
in Vault. Validate with `ansible-inventory`.

## Hands-On Lab

Inventory walkthroughs. **Shared prerequisites** — ansible-core installed. **Cost:** none.

### Lab 2.1 — Build a static inventory

**Objective:** Define hosts and groups.

```ini
# inventory.ini
[web]
web1 ansible_host=127.0.0.1 ansible_connection=local
web2 ansible_host=127.0.0.1 ansible_connection=local
[app]
app1 ansible_host=127.0.0.1 ansible_connection=local
```

```bash
ansible-inventory -i inventory.ini --graph
```

**Expected result:** a graph showing **web** and **app** groups with their hosts — a
structured inventory.

**Negative test:** list hosts with no groups; **group** them so plays can target subsets.

**Cleanup:** `rm inventory.ini`.

### Lab 2.2 — Assign group variables

**Objective:** Attach vars to a group.

```bash
mkdir -p group_vars
echo "http_port: 8080" > group_vars/web.yml
ansible -i inventory.ini web -m debug -a "var=http_port"
```

**Expected result:** `http_port: 8080` for the **web** group hosts — group-scoped vars.

**Negative test:** repeat the variable on every host; **group_vars** sets it once for the
group.

**Cleanup:** `rm -rf group_vars`.

### Lab 2.3 — Host variables

**Objective:** Override a var for one host.

```bash
mkdir -p host_vars
echo "http_port: 9090" > host_vars/web1.yml
ansible -i inventory.ini web -m debug -a "var=http_port"
```

**Expected result:** **web1** shows 9090 while web2 shows the group value — host override
precedence.

**Negative test:** edit the group value to change one host; **host_vars** overrides just
that host.

**Cleanup:** `rm -rf host_vars group_vars`.

### Lab 2.4 — Dynamic inventory (describe)

**Objective:** Describe sourcing inventory from a source of truth.

```yaml
# netbox_inv.yml  (netbox.netbox.nb_inventory plugin)
plugin: netbox.netbox.nb_inventory
api_endpoint: http://localhost:8000
token: "{{ lookup('env','NETBOX_TOKEN') }}"
group_by: ["device_roles"]
```

**Expected result:** an inventory generated **from NetBox** at runtime — drift-free
inventory.

**Negative test:** maintain a static list in a dynamic cloud/SoT environment; it
**drifts** — generate it dynamically.

**Cleanup:** `rm -f netbox_inv.yml`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Inventory defines managed hosts and groups (static or dynamic from a source of truth),
with variables in group_vars/host_vars by precedence and connection settings per host.
This chapter built an inventory, assigned group/host vars, and described dynamic
inventory.

- [ ] I can build a static inventory with groups.
- [ ] I can assign group variables.
- [ ] I can override with host variables.
- [ ] I can describe dynamic inventory from a source of truth.
- [ ] I completed Labs 2.1–2.4 including each negative test.
