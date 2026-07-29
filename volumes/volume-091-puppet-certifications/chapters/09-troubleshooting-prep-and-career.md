# Chapter 09: Troubleshooting, Prep, and Career

## Learning Objectives

- Validate and debug Puppet code.
- Troubleshoot platform components (agent, server, PuppetDB).
- Plan preparation for the Puppet Certified Professional exam.
- Map a Puppet automation career.
- Complete a walkthrough for each troubleshooting-and-career topic.

## Theory and Architecture

The **Troubleshooting** domain — and closing the volume — covers finding and fixing problems in **code**
and the **platform**. For **code**: **`puppet parser validate`** catches syntax errors, **`puppet apply
--noop`** previews changes without applying, and **`--debug`/`--trace`** show detailed compilation and
application. Common code problems are dependency cycles, missing relationships, and wrong data lookups
(check with **`puppet lookup`**). For the **platform**: verify the **agent** run (`puppet agent -t`),
the **server** (Puppet Server logs, catalog compilation errors), **certificates** (unsigned/expired), and
**PuppetDB** connectivity; **`facter`** confirms the data a catalog is built from. For **certification**,
prepare across all eight domains with Puppet's official training and the free open-source Puppet for
hands-on practice, then sit the **$200 Questionmark** exam. A Puppet career ladders from configuration
management into DevOps, platform engineering, and SRE roles. This chapter closes with troubleshooting,
prep, and career walkthroughs.

## Design Considerations

**Validate** before applying (`parser validate`, `--noop`), and use **`--debug`** to trace failures.
Reproduce issues with the node's **facts**. Check the **agent → server → PuppetDB** path for platform
issues, and **certificates** for enrollment failures. For the exam, practice on **open-source Puppet 8**
(same language as PE) and study all domains. Keep skills current with Puppet/PE releases.

## Implementation and Automation

The labs validate and debug code, reason about platform troubleshooting, and plan exam prep and career —
the troubleshooting and progression the domain and program support.

## Validation and Troubleshooting

Confirm troubleshooting and progression:

```text
Code: puppet parser validate (syntax) | puppet apply --noop (preview) | --debug/--trace (detail)
      puppet lookup (data) ; watch for dependency cycles + missing relationships
Platform: puppet agent -t (run) | Puppet Server logs (compile) | certs (sign/expiry) | PuppetDB | facter
Exam: 8 domains; practice on open-source Puppet 8; $200 Questionmark exam
Career: config management -> DevOps / platform engineering / SRE
```

Common pitfalls: applying code that never passed **`parser validate`**; and blaming code when a **cert**
or **PuppetDB** issue is the real cause — check the platform path.

## Security and Best Practices

Validate and `--noop` before changing production, keep certificates healthy, and practice on your own
systems. Careful troubleshooting protects your infrastructure. All work is authorized administration.

## Hands-On Lab

Troubleshooting-and-career walkthroughs. **Shared prerequisites** — open-source Puppet 8 and `python3`.
**Cost:** none.

### Lab 9.1 — Validate and debug code

**Objective:** Catch a syntax error before applying.

```bash
cat > /tmp/broken.pp <<'PP'
file { '/tmp/x'
  ensure => file,
}
PP
puppet parser validate /tmp/broken.pp; echo "exit=$?"
```

```text
Error: Could not parse for environment production: Syntax error at 'ensure' (line: 2, column: 3)
exit=1
```

**Expected result:** `parser validate` catching the missing colon before any apply — fast feedback.

**Negative test:** `puppet apply` the broken manifest in production; **validate** first to catch syntax
errors.

**Cleanup:**

```bash
rm -f /tmp/broken.pp
```

### Lab 9.2 — Reason about platform troubleshooting

**Objective:** Follow the agent→server→PuppetDB path.

```python
python3 - <<'PY'
checks = {
  "agent run":  "puppet agent -t --debug  (does it get a catalog? error?)",
  "certificate":"unsigned/expired cert -> agent cannot authenticate to server",
  "server":     "Puppet Server logs: catalog compilation errors (bad code/Hiera)",
  "PuppetDB":   "down -> facts/reports/exported resources fail",
  "facts":      "facter -> confirm the data the catalog is built from",
}
for k, v in checks.items(): print(f"{k:12}: {v}")
print("Isolate: is it CODE (compile) or PLATFORM (cert/server/PuppetDB)?")
PY
```

**Expected result:** a checklist isolating code versus platform faults along the run path.

**Negative test:** assume every failed run is a code bug; check **certs/server/PuppetDB** too.

**Cleanup:** none.

### Lab 9.3 — Plan exam prep and career

**Objective:** Sequence preparation and progression.

```python
python3 - <<'PY'
prep = [
  "Practice on free open-source Puppet 8 (same language as PE)",
  "Study all 8 domains (concepts/language/modules/Hiera/classification/environments/admin/orchestration)",
  "Follow the Puppet Language Style Guide; lint + rspec-puppet",
  "Register + sit PPT-PCP-24 ($200, Questionmark, 60 Q / 90 min)",
]
for p in prep: print("-", p)
career = "Config management -> DevOps engineer -> platform engineer / SRE"
print("Career:", career)
PY
```

**Expected result:** a free-practice, all-domains prep plan and a career path from config management to
platform/SRE roles.

**Negative test:** cram only the language and skip administration/orchestration; the exam spans **eight**
domains.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Troubleshooting Puppet means validating and previewing code (`parser validate`, `--noop`, `--debug`) and
isolating platform faults along the agent → server → PuppetDB → certificate path with facter, while
certification prep spans all eight domains practiced on free open-source Puppet 8 before the $200
Questionmark exam — laddering a career from configuration management into DevOps, platform engineering,
and SRE.

- [ ] I can validate and debug Puppet code.
- [ ] I can reason about platform troubleshooting.
- [ ] I can plan exam preparation across all domains.
- [ ] I can map a Puppet automation career.
- [ ] I completed Labs 9.1–9.3 including each negative test.
