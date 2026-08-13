# Chapter 03: The Puppet Language

## Learning Objectives

- Declare resources and use resource attributes.
- Group resources into classes and defined types.
- Use variables, data types, and conditionals.
- Order resources with relationships and notifications.
- Complete a walkthrough for each language topic.

## Theory and Architecture

The **Language** domain is the Puppet DSL. The atom is the **resource** — `type { 'title': attr => value
}`. Resources are grouped into **classes** (`class name { ... }`), the unit of configuration you include
on a node, optionally with **parameters** (`class ntp (String $server) { ... }`). A **defined type**
(`define name { ... }`) is a reusable resource you can declare many times (e.g., one per vhost).
**Variables** hold data (`$x = 'value'`), are strongly **typed** (String, Integer, Boolean, Array, Hash,
and more), and interpolate into strings. **Conditionals** — `if`/`elsif`/`else`, `case`, and the
selector (`$x ? { ... }`) — branch on facts or variables. **Relationships** order resources:
`require`/`before` set ordering, and `notify`/`subscribe` also **restart** a dependent (e.g., a service
restarts when its config file changes). **Templates** (**EPP** — Puppet's — or **ERB**) render dynamic
files. Writing idiomatic, ordered, parameterized code is the heart of the language. This chapter teaches
it with hands-on `puppet` walkthroughs.

## Design Considerations

Model configuration as **classes** with **parameters** (data in, from Hiera — Chapter 05). Use **defined
types** for "many of a thing." Order with **relationships**, and use **notify/subscribe** so a service
restarts on config change. Keep code **typed** and follow the **Style Guide** (idiomatic naming,
arrows aligned). Prefer templates for dynamic files over inline content.

## Implementation and Automation

The labs declare resources with relationships, write a parameterized class and a defined type, and use a
conditional — the language the domain validates.

## Validation and Troubleshooting

Confirm the language:

```text
Resource: type { 'title': attr => value }; class = unit of config (with params); defined type = reusable
Variables: typed ($String/$Integer/$Array/$Hash); interpolation "${var}"
Conditionals: if/elsif/else | case | selector ($x ? { ... })
Relationships: require/before (order) + notify/subscribe (order + refresh, e.g., restart service)
Templates: EPP (Puppet) / ERB for dynamic files
```

Common pitfalls: relying on **file order** for execution (Puppet is not ordered by default) — declare
**relationships**; and hardcoding config in classes instead of **parameters**.

## Security and Best Practices

Parameterize classes (no secrets hardcoded — use Hiera + eyaml, Chapter 05), order security-relevant
changes with relationships, and follow the Style Guide. All work is authorized administration.

## Hands-On Lab

Language walkthroughs. **Shared prerequisites** — open-source Puppet 8, sudo, `puppet apply`. **Cost:**
none.

### Lab 3.1 — Declare resources with a relationship

**Objective:** Order a file before a service and notify it.

```bash
cat > /tmp/rel.pp <<'PP'
file { '/tmp/app.conf':
  ensure  => file,
  content => "mode = strict\n",
  notify  => Exec['reload-app'],     # restart/reload when the file changes
}
exec { 'reload-app':
  command     => '/bin/echo reloaded > /tmp/reloaded',
  refreshonly => true,               # only runs when notified
}
PP
sudo puppet apply /tmp/rel.pp && cat /tmp/reloaded
```

```text
Notice: /File[/tmp/app.conf]/ensure: defined content ...
Notice: /Exec[reload-app]: Triggered 'refresh'
reloaded
```

**Expected result:** the config file managed, and the reload triggered **because** the file changed —
notify/subscribe in action.

**Negative test:** put the exec before the file and hope it runs after; declare a **relationship**
(`notify`) so ordering and refresh are explicit.

**Rollback:**

```bash
sudo rm -f /tmp/app.conf /tmp/reloaded /tmp/rel.pp
```

### Lab 3.2 — Write a parameterized class

**Objective:** Pass data into configuration.

```bash
cat > /tmp/cls.pp <<'PP'
class banner (String $text = 'Default') {
  file { '/tmp/banner':
    ensure  => file,
    content => "${text}\n",
  }
}
include banner
class { 'banner': text => 'Authorized use only' }   # override the default
PP
# (illustrative: a class is declared once; shown here for the parameter concept)
puppet parser validate /tmp/cls.pp && echo "valid"
```

```text
valid
```

**Expected result:** a class with a typed `String` parameter and a default — data-driven configuration.

**Negative test:** hardcode the banner text inside the class; **parameterize** it so Hiera can supply the
value per node.

**Rollback:**

```bash
sudo rm -f /tmp/cls.pp
```

### Lab 3.3 — Use a defined type

**Objective:** Declare a reusable resource many times.

```bash
cat > /tmp/def.pp <<'PP'
define motd_line (String $content) {
  file_line { "motd-${title}":
    path => '/tmp/motd',
    line => $content,
  }
}
PP
puppet parser validate /tmp/def.pp && echo "valid defined type"
```

```text
valid defined type
```

**Expected result:** a **defined type** you can declare repeatedly (one per line/vhost/user) — reusable
config.

**Negative test:** copy-paste the same resource block ten times; use a **defined type** with a title.

**Rollback:**

```bash
sudo rm -f /tmp/def.pp
```

### Lab 3.4 — Branch on a fact with a conditional

**Objective:** Adapt code per platform.

```bash
cat > /tmp/cond.pp <<'PP'
$pkg = $facts['os']['family'] ? {
  'Debian' => 'apache2',
  'RedHat' => 'httpd',
  default  => 'httpd',
}
notice("Web package for this OS: ${pkg}")
PP
sudo puppet apply /tmp/cond.pp
```

```text
Notice: Scope(Class[main]): Web package for this OS: apache2
```

**Expected result:** the selector picking the right package name from the OS family fact — portable code.

**Negative test:** assume the Debian package name everywhere; branch on **`$facts['os']['family']`**.

**Rollback:**

```bash
sudo rm -f /tmp/cond.pp
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Puppet language declares typed resources grouped into parameterized classes and reusable defined
types, uses variables and conditionals (if/case/selector) to adapt on facts, and orders work with
relationships — require/before for ordering and notify/subscribe for ordering plus refresh — rendering
dynamic files with EPP/ERB templates, all in idiomatic Style-Guide form.

- [ ] I can declare resources with relationships and notifications.
- [ ] I can write a parameterized class.
- [ ] I can use a defined type.
- [ ] I can branch on a fact with a conditional.
- [ ] I completed Labs 3.1–3.4 including each negative test.
