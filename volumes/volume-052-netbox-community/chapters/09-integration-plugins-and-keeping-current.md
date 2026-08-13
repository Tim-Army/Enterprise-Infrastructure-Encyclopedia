# Chapter 09: Integration, Plugins, and Keeping Current

## Learning Objectives

- Use NetBox as an Ansible dynamic inventory.
- Manage NetBox data as code with the Terraform provider.
- Extend NetBox with plugins.
- Track releases and the community.
- Complete a walkthrough for each integration.

## Theory and Architecture

As the source of truth, NetBox drives automation: the **`netbox.netbox` Ansible
collection** provides a **dynamic inventory** and modules, the community **Terraform
provider** manages NetBox objects declaratively, and **`pynetbox`** is the Python SDK.
NetBox is extensible with **plugins** (packaged Django apps adding models/views/API).
The project ships frequent releases (current series **4.6.x**); track them on GitHub.

## Design Considerations

Feed automation from NetBox rather than static files: **Ansible dynamic inventory**
groups hosts by NetBox attributes; **Terraform** codifies NetBox objects for review and
drift control. Add a **plugin** only when the core model genuinely lacks something.
Pin to a supported release and read release notes before upgrading.

## Implementation and Automation

The labs use the Ansible inventory plugin, the Terraform provider, a plugin install,
and a currency check.

## Validation and Troubleshooting

Confirm the integration surfaces:

```text
Ansible: netbox.netbox.nb_inventory plugin -> dynamic inventory grouped by NetBox data.
Terraform: netbox provider -> resources (e.g., netbox_site) as code.
Plugins: PLUGINS list in configuration.py; pip-installed Django apps.
Releases: github.com/netbox-community/netbox/releases (4.6.x current).
```

Common pitfalls: static inventories that drift from NetBox; and plugins incompatible
with the running NetBox version.

## Security and Best Practices

Drive **inventory and config** from NetBox (single source of truth), manage objects as
**code** where practical, vet **plugins** for version compatibility and maintenance,
and upgrade on a cadence within supported releases.

## Hands-On Lab

Integration walkthroughs. **Shared prerequisites** — a running NetBox with a device
that has a primary IP; `$NB`/`$TOKEN`; `ansible`, `terraform`, `pip`. **Cost:** none.

### Lab 9.1 — Ansible dynamic inventory

**Objective:** Build an inventory from NetBox.

```yaml
# netbox_inv.yml
plugin: netbox.netbox.nb_inventory
api_endpoint: http://localhost:8000
token: TOKEN
group_by: ["sites"]
```

```bash
ansible-inventory -i netbox_inv.yml --list | python3 -c "import sys,json;print('groups:',list(json.load(sys.stdin).keys())[:5])"
```

**Expected result:** inventory **groups derived from NetBox** (e.g., a `sites_dc1`
group) — dynamic, drift-free inventory.

**Negative test:** maintain a static `hosts` file; it **drifts** from NetBox — generate
it dynamically.

**Rollback:** `rm netbox_inv.yml`.

### Lab 9.2 — Terraform-managed object

**Objective:** Create a NetBox site as code.

```hcl
terraform { required_providers { netbox = { source = "e-breuninger/netbox" } } }
provider "netbox" { server_url = "http://localhost:8000" api_token = "TOKEN" }
resource "netbox_site" "dc2" { name = "DC2" slug = "dc2" status = "active" }
```

```bash
terraform init -no-color >/dev/null && terraform apply -auto-approve -no-color | tail -2
```

**Expected result:** Terraform reports **1 added** — a NetBox site managed as code.

**Negative test:** click-create critical objects; **Terraform** gives review, history,
and drift detection.

**Rollback:** `terraform destroy -auto-approve`.

### Lab 9.3 — Install a plugin

**Objective:** Enable a plugin in configuration.

```python
# configuration.py
PLUGINS = ["netbox_topology_views"]   # pip install netbox-topology-views (version-matched)
```

**Expected result:** the plugin listed in **`PLUGINS`** and loaded after restart —
NetBox extended with new views/models.

**Negative test:** install a plugin built for an older NetBox; **version-match** it or
NetBox fails to start.

**Rollback:** remove it from `PLUGINS` and uninstall.

### Lab 9.4 — Check the current release

**Objective:** Read the latest NetBox release.

```bash
curl -sS "https://api.github.com/repos/netbox-community/netbox/releases/latest" \
  | python3 -c "import sys,json;print('latest:',json.load(sys.stdin)['tag_name'])"
```

**Expected result:** the latest tag (a **v4.6.x** release) — what to track for upgrades.

**Negative test:** run an unsupported old release; track **releases** and stay on a
supported series.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NetBox integrates with Ansible (dynamic inventory), Terraform (objects as code), and
`pynetbox`, and extends via plugins — all anchored on the source of truth. Track the
4.6.x releases and upgrade within supported versions.

- [ ] I can generate an Ansible dynamic inventory from NetBox.
- [ ] I can manage NetBox objects with Terraform.
- [ ] I can enable a version-matched plugin.
- [ ] I can find the current release to plan upgrades.
- [ ] I completed Labs 9.1–9.4 including each negative test.
