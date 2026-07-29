# Chapter 01: The Puppet Certification Program

## Learning Objectives

- Describe the Puppet Certified Professional credential and its eight exam domains.
- Explain the exam format, delivery, and product versions.
- Explain the declarative, idempotent Puppet model.
- Reason about where Puppet fits (versus imperative tools).
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

**Puppet** is a declarative **configuration-management** platform — now a **Perforce** company — that
defines the **desired state** of systems as code and continuously enforces it. Its certification program
centers on one credential, the **Puppet Certified Professional (PPT-PCP-24)** (also called "Puppet 206").
The exam validates administering system infrastructure with Puppet and developing basic modules, and
spans **eight domains**: **Concepts**, **Language**, **Module Authoring**, **Hiera/data separation**
(within Language), **Classification**, **Environments**, **Administration**, **Orchestration & Tasks**,
and **Troubleshooting**. The exam is **60 multiple-choice questions in 90 minutes**, **$200 USD**,
delivered **online-proctored through Questionmark** (Perforce's certification portal), in English. It is
based on **Open Source Puppet 8.9.0+** and **Puppet Enterprise 2023.8.0+**, with no formal prerequisites
(though familiarity with Puppet automation, module development, and the Puppet Language **Style Guide**
is expected). The defining idea is **declarative, idempotent** management: you describe *what* the system
should look like, and Puppet makes it so — applying repeatedly with the same result. This chapter orients
you on a local open-source Puppet install so the domains map to real commands.

## Design Considerations

Prepare across **all eight domains** — the exam is broad. Practice on **open-source Puppet 8** locally
(the language and `puppet apply` are the same as Puppet Enterprise's). Internalize the **declarative,
idempotent** model — it separates Puppet from imperative scripting. Follow the **Style Guide** (the exam
expects idiomatic code). Budget for the **$200** Questionmark exam.

## Implementation and Automation

The labs confirm the Puppet version, apply a first idempotent resource, and map the certification domains
— the orientation every PCP candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Credential: Puppet Certified Professional (PPT-PCP-24 / "Puppet 206")
Exam: 60 multiple-choice / 90 min / $200 / Questionmark online-proctored / English
Based on: Open Source Puppet 8.9+ and Puppet Enterprise 2023.8+; no formal prereqs
Domains: Concepts | Language | Module Authoring | Classification | Environments | Administration |
         Orchestration & Tasks | Troubleshooting
Model: declarative + idempotent (describe desired state; apply repeatedly = same result)
```

Common pitfalls: studying only the language and skipping **administration/orchestration/troubleshooting**;
and thinking imperatively (scripting steps) instead of **declaratively** (desired state).

## Security and Best Practices

Puppet enforces a consistent, idempotent **desired state** and corrects drift — defensive standardization
of your own infrastructure. Protect the primary server and certificates (Chapter 07). All work in this
volume is authorized administration.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a system with **open-source Puppet 8**
installed (`puppet` on PATH), sudo for `puppet apply`, and `python3`. **Cost:** none (open-source Puppet
is free).

### Lab 1.1 — Confirm the Puppet version

**Objective:** Verify the platform the exam assumes.

```bash
puppet --version
facter os.family
```

```text
8.9.0
Debian
```

**Expected result:** Puppet **8.9+** and a working `facter` — the platform the PCP exam is based on.

**Negative test:** study against Puppet 5/6 syntax and modules; the exam is **Puppet 8** — use a current
version.

**Cleanup:** none (read-only).

### Lab 1.2 — Apply a first idempotent resource

**Objective:** See declarative, idempotent management.

```bash
cat > /tmp/first.pp <<'PP'
file { '/tmp/hello.txt':
  ensure  => file,
  content => "Managed by Puppet\n",
}
PP
sudo puppet apply /tmp/first.pp
sudo puppet apply /tmp/first.pp   # run again
```

```text
Notice: /Stage[main]/Main/File[/tmp/hello.txt]/ensure: defined content as '{sha256}...'
Applied catalog in 0.02 seconds
# second run:
Applied catalog in 0.01 seconds        # no change -> idempotent
```

**Expected result:** the file created on the first run and **unchanged** on the second — idempotence.

**Negative test:** write a shell script that appends the line every run; it is not **idempotent** —
Puppet converges to the declared state.

**Cleanup:**

```bash
sudo rm -f /tmp/hello.txt /tmp/first.pp
```

### Lab 1.3 — Map the exam domains

**Objective:** Reason about what the PCP covers.

```python
python3 - <<'PY'
domains = ["Concepts", "Language", "Module Authoring", "Classification",
           "Environments", "Administration", "Orchestration & Tasks", "Troubleshooting"]
for i, d in enumerate(domains, 1): print(f"Domain {i}: {d}")
print("60 MC / 90 min / $200 (Questionmark); based on Puppet 8 + PE 2023.8")
PY
```

**Expected result:** the eight domains listed — the breadth to prepare across.

**Negative test:** prepare only the Puppet **language**; the exam also tests administration, orchestration,
and troubleshooting — study all eight.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Puppet Certified Professional (PPT-PCP-24) is a 60-question, 90-minute, $200 Questionmark-proctored
exam based on Puppet 8 and Puppet Enterprise 2023.8, spanning eight domains from concepts and the
language to module authoring, classification, environments, administration, orchestration, and
troubleshooting — all grounded in Puppet's declarative, idempotent desired-state model.

- [ ] I can describe the PCP credential and its eight domains.
- [ ] I can explain the exam format and product versions.
- [ ] I can explain the declarative, idempotent model.
- [ ] I completed Labs 1.1–1.3 including each negative test.
