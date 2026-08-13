# Chapter 02: Essential Tools, Shell Scripting, and Software Management

![Lab flow for this chapter: an administrative audit script prints disk usage, recent dnf transactions, and largest /var directories cleanly; installing a small test package creates a new transaction that the script's next run picks up automatically. As a negative test, a copy of the script replaces a quoted path with an unquoted multi-word variable; running it word-splits the value into two separate arguments, and du reports it cannot access a directory literally named audit in the current working directory — exactly the class of bug quoting prevents. Separately, dnf history undo cleanly reverses the test package installation.](../../../diagrams/volume-014-red-hat-enterprise-linux-10/chapter-02-dnf-audit-quoting-rollback-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: an administrative audit script exercised against a real package transaction, then deliberately broken to demonstrate a quoting bug.*

## Learning Objectives

- Navigate, inspect, and manipulate the filesystem efficiently using
  core command-line utilities and I/O redirection.
- Use `grep`, `sed`, `awk`, and `find` to search, filter, and transform
  text and file sets at production scale.
- Write portable Bash scripts with variables, conditionals, loops,
  functions, and correct exit-status handling.
- Query, install, update, and audit software with `dnf` and `rpm`,
  including package group, history, and dependency operations.
- Diagnose and recover from a broken or partial package transaction.

## Theory and Architecture

Every higher-level administrative task in this volume — SELinux
troubleshooting, systemd unit authoring, Ansible playbook design — rests
on fluency with the same small set of composable command-line tools.
RHEL 10 ships GNU coreutils, Bash 5.x, and the standard text-processing
trio (`grep`, `sed`, `awk`) as the baseline shell environment; treating
these as a coherent toolkit rather than isolated commands is what makes
an administrator fast under incident pressure.

### The Unix pipeline model

RHEL's shell tools follow the Unix philosophy: each utility does one
thing, reads from standard input or a file argument, and writes to
standard output, so tools compose through pipes (`|`) into pipelines
that no single tool could express alone. Redirection operators
(`>`, `>>`, `<`, `2>`, `&>`) route those streams to and from files
independently of the pipeline itself, which is why a command's stdout
can be captured to a file while its stderr is still visible on the
terminal (`command 2>error.log | tee output.log`).

### Text processing tools

| Tool | Role | Typical use |
| --- | --- | --- |
| `grep` | Pattern matching (POSIX/extended regex) | Filter lines matching or excluding a pattern |
| `sed` | Stream editing | In-place, scripted, line-oriented text transformation |
| `awk` | Field-oriented text processing | Column extraction, arithmetic, report generation from structured text |
| `find` | Filesystem traversal | Locate files by name, type, age, size, permission, or owner, optionally acting on matches |
| `xargs` | Argument construction | Convert a stream of names into arguments for another command, with parallelism control |

`grep`, `sed`, and `awk` all understand regular expressions, but with
different defaults: `grep` uses basic regular expressions (BRE) unless
called as `grep -E` (or `egrep`), while `awk` always uses extended
regular expressions (ERE). Knowing which dialect a tool speaks avoids a
large class of "my pattern doesn't match" debugging sessions.

### Shell scripting fundamentals

A Bash script is a sequence of the same commands used interactively,
made repeatable through variables, control flow, and functions. Three
concepts define a production-quality script:

1. **Exit status.** Every command returns a numeric exit status (`$?`);
   `0` means success, anything else is tool-specific failure. Scripts
   should check exit status explicitly or rely on `set -e` to abort on
   the first failing command.
2. **Quoting and word-splitting.** Unquoted variable expansion
   (`$var` instead of `"$var"`) is subject to word-splitting and glob
   expansion, a frequent source of scripts that break on filenames with
   spaces. Default to double-quoting variable expansions.
3. **Idempotency.** A well-written administrative script produces the
   same end state whether run once or run five times — the same
   principle this encyclopedia applies to Kickstart, Ansible, and
   Terraform automation elsewhere.

### Software management architecture

RHEL 10 uses `dnf` (DNF5) as the primary package manager, itself built
on `libdnf5` and ultimately manipulating the RPM database
(`/var/lib/rpm`). Every `dnf` operation is one of:

- **Query/inspect** (`dnf list`, `dnf info`, `dnf repoquery`) — reads
  repository metadata without changing system state.
- **Transaction** (`dnf install`, `dnf remove`, `dnf upgrade`) — computes
  a dependency-resolved set of RPM operations, then applies them
  atomically and records the transaction in `dnf history`.
- **Group/module** (`dnf group`, `dnf module`) — operates on curated
  sets of packages (environment groups) or versioned application
  stacks (modules), described in [Chapter 01](01-installation-subscriptions-repositories-and-cockpit.md).

`rpm` itself remains available for lower-level queries and for
inspecting packages outside of a repository context (a downloaded
`.rpm` file, or a package already installed but whose repo is no
longer configured), but `rpm -i`/`rpm -U` should not be used for
routine installation because it does not resolve dependencies the way
`dnf` does.

## Design Considerations

- **Script location and packaging.** Ad hoc one-off scripts belong in
  an administrator's own tooling repository; anything that runs on a
  schedule or is invoked by another system belongs under
  `/usr/local/sbin` (root-only tools) with a version-controlled source,
  not hand-edited in place on production hosts.
- **grep/sed/awk vs. a general-purpose language.** These tools are
  ideal for single-pass, line-oriented transformation of text a human
  can reason about; once a task needs structured data (JSON, complex
  state, error handling beyond exit codes), moving to Python or a
  proper Ansible module is usually less fragile than a longer `awk`
  script.
- **`dnf` transaction discipline.** Decide, per environment, whether
  `dnf upgrade` runs unattended (`dnf-automatic`) or only through a
  change-controlled window; unattended patching reduces exposure time
  to known CVEs but removes the human checkpoint before a kernel or
  service-affecting update lands.
- **Versionlock and module stream pinning.** Environments with strict
  compatibility requirements (a vendor application certified against a
  specific PostgreSQL minor version) should use `dnf versionlock` or a
  pinned module stream rather than relying on staff discipline to avoid
  an unwanted upgrade.
- **Exit-code contracts in automation.** Any script invoked by
  systemd, cron, or Ansible must return accurate exit codes; a script
  that always exits `0` regardless of internal failure silently breaks
  monitoring and automation built on top of it.

## Implementation and Automation

### 1. Filesystem navigation and inspection

```bash
# Long listing with human-readable sizes, including hidden files
ls -lah /var/log

# Disk usage summary, one level deep, human-readable
du -h --max-depth=1 /var

# Filesystem-level free space
df -hT

# Find files modified in the last 24 hours under /etc
find /etc -type f -mtime -1

# Find and remove files older than 30 days in a scratch directory
find /var/tmp/reports -type f -mtime +30 -exec rm -f {} \;

# Find world-writable files (a common hardening audit)
find / -xdev -type f -perm -0002 -exec ls -l {} \;
```

### 2. Text processing with grep, sed, and awk

```bash
# Show lines matching a pattern, with line numbers, case-insensitive
grep -in "failed password" /var/log/secure

# Extended regex: match either "error" or "critical"
grep -E "error|critical" /var/log/messages

# In-place substitution across a config file, with a backup
sed -i.bak 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

# Print the third column (username) of /etc/passwd-style colon data
awk -F: '{ print $1, $3 }' /etc/passwd

# Sum the second column of a report and print the total
awk '{ sum += $2 } END { print "Total:", sum }' disk-report.txt
```

### 3. A production-style Bash script

```bash
#!/usr/bin/env bash
# package-audit.sh — report installed packages not from an enabled repo
set -euo pipefail

LOGFILE="/var/log/package-audit.log"
THRESHOLD_DAYS=90

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" | tee -a "$LOGFILE"
}

log "Starting package audit"

# Packages not associated with any currently configured repository
orphaned=$(dnf list extras 2>/dev/null | tail -n +2 || true)

if [[ -n "${orphaned}" ]]; then
  log "WARNING: packages installed outside configured repositories:"
  echo "${orphaned}" | tee -a "$LOGFILE"
  exit_code=1
else
  log "OK: no orphaned packages found"
  exit_code=0
fi

log "Audit complete"
exit "${exit_code}"
```

Key patterns worth calling out: `set -euo pipefail` turns unset
variables and mid-pipeline failures into hard errors instead of silent
continuations; the `log()` function centralizes timestamped output to
both console and file; and the script's final `exit` code reflects
whether a finding occurred, so it composes correctly with cron, systemd
`OnFailure=`, or an Ansible `command` task's `failed_when`.

### 4. Software management with dnf and rpm

```bash
# Search for a package by name or description
dnf search httpd

# Show detailed package metadata before installing
dnf info httpd

# Install with automatic dependency resolution
dnf install -y httpd mod_ssl

# Update everything, or a single package
dnf upgrade -y
dnf upgrade -y httpd

# Remove a package and any dependencies no longer needed
dnf remove -y httpd

# List transaction history and inspect one transaction
dnf history list
dnf history info 42

# Undo the most recent transaction
dnf history undo last

# Pin a package to its current version
dnf install -y python3-dnf-plugin-versionlock
dnf versionlock add httpd

# Query the RPM database directly
rpm -qa | grep httpd
rpm -qi httpd
rpm -ql httpd            # list files owned by the package
rpm -qf /etc/httpd/conf/httpd.conf   # which package owns this file
rpm -V httpd              # verify installed files against the package manifest
```

### 5. Working with package groups

```bash
dnf group list
dnf group install -y "Development Tools"
dnf group remove -y "Development Tools"
```

## Validation and Troubleshooting

- **Confirm a script's logic without side effects.** Run with `bash -x
  script.sh` to trace execution, or `bash -n script.sh` to check syntax
  only, before running against production data.
- **Diagnose "command not found" in a script vs. shell.** A script
  invoked with a different shebang or via `sh script.sh` may not have
  the same `PATH` or built-ins as an interactive Bash session; always
  invoke with `./script.sh` (respecting the shebang) or explicitly
  `bash script.sh`.
- **Diagnose a stuck or failed dnf transaction.** `dnf history list`
  shows whether the last transaction completed; a killed transaction
  can leave an RPM database lock. Confirm with:

  ```bash
  rpm --quiet -q kernel && echo "rpm db readable"
  ls /var/lib/rpm/.rpm.lock 2>/dev/null && echo "lock file present"
  ```

  If no `dnf`/`rpm` process is actually running (`ps aux | grep -E
  'dnf|rpm'`), a stale lock can be cleared, but treat this as a last
  resort after confirming no other process holds it.
- **Diagnose unmet dependencies.** `dnf install` failing with a
  dependency error benefits from `dnf repoquery --deplist <package>` to
  see the full dependency chain, and `dnf repoquery --whatprovides
  '<capability>'` to find which package satisfies a missing capability.
- **Verify installed-file integrity.** `rpm -V <package>` flags any
  file that differs from the package manifest (size, checksum, mode,
  owner); a leading `5` in the output means the file's checksum
  changed, which is either expected local configuration (for a config
  file) or worth investigating (for a binary).
- **Common failure: sed in-place edits without a backup.** `sed -i`
  without a suffix argument overwrites the file with no recovery path
  if the expression was wrong. Always use `sed -i.bak` (or test with
  `sed` alone, no `-i`, first) against configuration files.

## Security and Best Practices

- Never pipe an untrusted, unreviewed script directly into `bash`
  (`curl ... | bash`); download, inspect, and then execute, or verify a
  checksum/signature first.
- Quote every variable expansion in scripts that touch filenames
  (`"$file"`, not `$file`) to prevent word-splitting and glob-expansion
  bugs from becoming path-traversal or unintended-deletion incidents.
- Use `set -euo pipefail` in administrative scripts so a failed command
  in the middle of a pipeline does not silently allow the script to
  continue as if nothing happened.
- Verify GPG signatures on packages (`gpgcheck=1` in repo definitions,
  the default for Red Hat repositories) and never disable `gpgcheck`
  permanently to work around a signing issue — fix the key import
  instead.
- Keep `find -exec` and `xargs`-driven deletions behind a dry-run pass
  (`find ... -print` before adding `-delete`/`-exec rm`) when the
  pattern is new or broad.
- Use `dnf versionlock` and module stream pinning deliberately and
  document why a package is pinned, so a pin does not silently block
  a future security update.
- Review `dnf history` after any unattended patch window as part of
  routine change verification, not only when something looks wrong.

## References and Knowledge Checks

**References**

- [`bash(1)`, `grep(1)`, `sed(1)`, `gawk(1)`, `find(1)` man pages.](https://man7.org/linux/man-pages/man1/bash.1.html)
- [DNF5 documentation](https://dnf5.readthedocs.io/) — command reference and plugin list, Red Hat
  Customer Portal.
- [`rpm(8)` and `rpm --verify` documentation.](https://rpm.org/documentation.html)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — RHEL 10
  baseline referenced throughout this chapter.

**Knowledge checks**

1. Why does an unquoted `$variable` expansion in a Bash script risk
   incorrect behavior on filenames containing spaces?
2. What is the practical difference between `grep -E` and default
   `grep` pattern matching?
3. What does `dnf history undo last` do, and what precondition must be
   true for it to succeed cleanly?
4. Why is `rpm -i` discouraged for routine package installation in
   favor of `dnf install`?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each skill under RHCSA objectives 1
(essential tools) and 3 (create simple shell scripts)** — files and links, text processing
and redirection, archiving, and scripting. Every step is a runnable RHEL 10 command. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 2.1–2.4** — a RHEL 10 shell as a normal user with `sudo`
where noted, and a scratch directory (`mkdir -p ~/lab && cd ~/lab`). **Cost:** none.

### Lab 2.1 — Files, directories, and links (Topic: Essential tools)

**Objective:** Manage files and create hard and symbolic links.

```bash
cd ~/lab
echo "data" > file.txt
ln file.txt hard.txt          # hard link (same inode)
ln -s file.txt soft.txt       # symbolic link (points to name)
ls -li file.txt hard.txt soft.txt
```

**Expected result:** `file.txt` and `hard.txt` share one inode number and a link count of 2;
`soft.txt` is a separate inode pointing to the name — a hard link is another name for the
same data (survives deleting the original name), a symlink is a pointer (breaks if the target
is removed).

**Negative test:** `rm file.txt`, then `cat hard.txt` (still works — data persists) vs
`cat soft.txt` (fails — dangling symlink) — this proves the inode-vs-name distinction the
exam expects you to know.

**Rollback:** `rm -f ~/lab/file.txt ~/lab/hard.txt ~/lab/soft.txt`.

### Lab 2.2 — Text processing and I/O redirection (Topic: Essential tools)

**Objective:** Filter and transform text with pipes and redirection.

```bash
cd ~/lab
getent passwd > users.txt
grep -c bash users.txt                          # count bash users
awk -F: '$3 >= 1000 {print $1}' users.txt        # regular (UID>=1000) accounts
sed -n '1,3p' users.txt > firstthree.txt          # redirect first 3 lines to a file
```

**Expected result:** a count of bash-shell accounts, the list of regular-user names, and a
three-line file — `grep`/`sed`/`awk` with pipes (`|`) and redirection (`>`, `>>`, `2>`) are
the core text-processing tools RHCSA tasks lean on for extracting and transforming data.

**Negative test:** use `>` where you meant `>>` and overwrite a file you meant to append to;
the prior content is gone — redirection operators are exact, and choosing the wrong one loses
data.

**Rollback:** `rm -f ~/lab/users.txt ~/lab/firstthree.txt`.

### Lab 2.3 — Archiving and compression (Topic: Essential tools)

**Objective:** Create and extract a compressed archive.

```bash
cd ~/lab
mkdir -p src && echo hi > src/a && echo yo > src/b
tar -czvf backup.tar.gz src/
rm -rf src
tar -xzvf backup.tar.gz
ls src/
```

**Expected result:** `backup.tar.gz` is created, and extraction restores `src/a` and
`src/b` — `tar` with `-z` (gzip), `-j` (bzip2), or `-J` (xz) bundles and compresses
directories, the standard RHCSA backup/transfer mechanism.

**Negative test:** extract a `.tar.gz` with `tar -xf` but without matching the compression
in a pipeline that needs it; modern `tar` autodetects, but a raw `gzip -d` on a `.tar` (not
`.tar.gz`) fails — the tool must match the file's actual format.

**Rollback:** `rm -rf ~/lab/src ~/lab/backup.tar.gz`.

### Lab 2.4 — A simple shell script (Topic: Create shell scripts)

**Objective:** Write a script with a conditional, a loop, and exit status.

```bash
cd ~/lab
cat > report.sh <<'EOF'
#!/bin/bash
# usage: report.sh <dir>
dir="${1:-.}"
if [ ! -d "$dir" ]; then
    echo "Not a directory: $dir" >&2
    exit 1
fi
for f in "$dir"/*; do
    [ -f "$f" ] && echo "file: $f"
done
exit 0
EOF
chmod +x report.sh
./report.sh /etc; echo "exit=$?"
./report.sh /nope; echo "exit=$?"
```

**Expected result:** the script lists files in `/etc` and exits 0, then reports the bad
directory to stderr and exits 1 — RHCSA scripting expects positional parameters (`$1`),
conditionals (`if [ ]`), loops (`for`), input/output, and meaningful exit codes.

**Negative test:** omit the `#!/bin/bash` shebang and run `./report.sh`; it may run under the
wrong interpreter or fail — the shebang declares the interpreter, and `chmod +x` makes it
executable; both are required.

**Rollback:** `rm -f ~/lab/report.sh`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Command-line fluency with coreutils, `grep`/`sed`/`awk`, `find`, and
disciplined Bash scripting underpins every later chapter's automation.
`dnf` and `rpm` form a two-layer software management model: `dnf`
resolves dependencies and records reversible transactions, while `rpm`
provides low-level query and verification against the installed package
database. Scripts intended for production or automation use should be
idempotent, correctly quoted, and honest about their exit status.

- [ ] Can compose `grep`, `sed`, `awk`, and `find` into working text-
      processing pipelines.
- [ ] Can write a Bash script using `set -euo pipefail`, functions, and
      correct variable quoting.
- [ ] Can install, query, verify, and roll back software using `dnf`
      and `rpm`.
- [ ] Can diagnose a broken script and a failed or partial `dnf`
      transaction.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
