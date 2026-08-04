# Chapter 02: The Entry Tier — LPI Essentials and LFCA

## Learning Objectives

- Map the four LPI Essentials credentials (010/020/030/050) and the Linux Foundation's LFCA.
- Know what each entry credential tests and who it serves.
- Complete a walkthrough lab per credential.

## The entry tier

| Credential | Exam | Tests |
|:---|:---|:---|
| Linux Essentials | 010 | Linux basics: FOSS, command line, files, users, simple scripts |
| Security Essentials | 020 | Security literacy: threats, encryption, identity, network/device hygiene |
| Web Development Essentials | 030 | HTML/CSS/JavaScript/Node.js and SQL basics |
| Open Source Essentials | 050 | Open source licensing, communities, business models |
| LFCA | 60 MCQ | IT breadth: Linux fundamentals, sysadmin basics, cloud, security, DevOps |

All four Essentials are 40 questions / 60 minutes, no prerequisites, **lifetime validity** — teaching-friendly credentials. LFCA is the Linux Foundation's pre-professional equivalent with more cloud/DevOps breadth.

## Hands-On Lab

Any Linux machine or VM. **Cost:** none.

### Lab 2.1 — Linux Essentials core loop (010)

**Objective:** Drill the file/user/permission basics 010 tests.

```bash
mkdir -p ~/lab && cd ~/lab
echo "hello" > notes.txt
ls -l notes.txt
chmod 640 notes.txt
ls -l notes.txt | awk '{print $1}'
```

**Expected result:** The file created, listed, and its mode changed to `-rw-r-----` — files, listing, and the permission triplet (user/group/other) are 010's backbone, alongside knowing what a distribution, a shell, and free software licensing are.

**Negative test:** `chmod 999 notes.txt` — invalid mode; octal digits stop at 7 because each is three bits (rwx). The error teaches the encoding.

**Cleanup:** Keep `~/lab` for the chapter.

### Lab 2.2 — Security Essentials literacy (020)

**Objective:** Exercise the encryption/identity vocabulary 020 tests.

```bash
echo "secret" > s.txt
gpg --symmetric --cipher-algo AES256 --batch --passphrase lab123 s.txt
file s.txt.gpg
gpg --decrypt --batch --passphrase lab123 s.txt.gpg 2>/dev/null
```

**Expected result:** `s.txt.gpg` reported as GPG encrypted data and the decrypt returning `secret` — symmetric encryption in one loop. 020 tests literacy: symmetric vs public-key, hashing vs encryption, MFA, updates, backups — concepts this loop makes tangible.

**Negative test:** Decrypt with the wrong passphrase — `decryption failed`; keys, not obscurity, hold the secret.

**Cleanup:** `rm s.txt s.txt.gpg`.

### Lab 2.3 — Web Development Essentials stack (030)

**Objective:** Touch each layer 030 names.

```bash
node -e 'const items=["html","css","js"]; console.log(items.map(x=>x.toUpperCase()).join(","))'
python3 -c "import sqlite3; c=sqlite3.connect(':memory:'); c.execute('CREATE TABLE t(x)'); c.execute('INSERT INTO t VALUES (42)'); print(c.execute('SELECT x FROM t').fetchone())"
```

**Expected result:** `HTML,CSS,JS` from Node and `(42,)` from SQL — JavaScript on the server and a SQL round trip; with HTML/CSS structure-and-style knowledge, that is 030's stack in miniature.

**Negative test:** `SELECT y FROM t` — `no such column`; SQL errors name the schema, the debugging habit 030 expects.

**Cleanup:** None.

### Lab 2.4 — Open Source Essentials licensing (050)

**Objective:** Apply the license distinctions 050 tests.

```bash
cat <<'EOF'
scenario: you modify GPLv3 code and distribute binaries       -> must offer source (copyleft)
scenario: you modify MIT code and distribute binaries          -> attribution suffices (permissive)
scenario: you run modified AGPL code as a network service      -> must offer source to users (network copyleft)
EOF
```

**Expected result:** The three scenarios answered correctly — copyleft vs permissive vs network copyleft is 050's core, alongside community roles and open-source business models.

**Negative test:** Treating "open source" as "no obligations" — the GPL scenario shows why that fails legal review.

**Cleanup:** None.

### Lab 2.5 — LFCA breadth check

**Objective:** Sample LFCA's six-domain breadth in one pass.

```bash
uname -r                          # Linux fundamentals
systemctl is-system-running       # system administration
ip -brief addr | head -3          # networking
id                                # security: who am I, what groups
df -h / | tail -1                 # resources/troubleshooting
echo "cloud/devops: images, containers, CI - see Volumes VIII, XLI, XCII"
```

**Expected result:** Kernel version, system state, addresses, identity, and disk usage — one command per LFCA domain area. LFCA is breadth, not depth; if each output makes sense to you, you're near ready.

**Negative test:** Any line you cannot explain is your study pointer — the lab as diagnostic.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] All four Essentials mapped and sampled with a lab each.
- [ ] LFCA breadth sampled as a diagnostic.
- [ ] Entry credential chosen (lifetime Essentials vs LFCA's cloud breadth).
