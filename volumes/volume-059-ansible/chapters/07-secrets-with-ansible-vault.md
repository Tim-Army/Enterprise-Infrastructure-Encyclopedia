# Chapter 07: Secrets with Ansible Vault

## Learning Objectives

- Explain how Ansible Vault protects secrets.
- Encrypt variables and files.
- Reference encrypted data in playbooks.
- Manage vault credentials and multiple vaults.
- Complete a walkthrough for each Vault skill.

## Theory and Architecture

Automation needs **secrets** (passwords, API tokens, certificates), but they must never sit
in plaintext in version control. **Ansible Vault** encrypts variables and files with a
**password/secret**, so encrypted content is safe to commit; at runtime Ansible **decrypts**
it using the supplied vault password (prompted, from a file, or a script). You can encrypt a
whole file (`ansible-vault encrypt`) or a single variable inline (`ansible-vault
encrypt_string`), and use **vault IDs** to manage multiple vaults (e.g., dev vs prod). The
password itself lives outside the repo (a secret store / CI secret).

## Design Considerations

Encrypt **secret vars** (ideally a separate `vault.yml` in group_vars), keep the **vault
password out of the repo** (CI secret / password file with restrictive perms), and use
**vault IDs** to separate environments. Reference decrypted values like any variable.

## Implementation and Automation

The labs encrypt a variable and a file, and run a playbook that decrypts them.

## Validation and Troubleshooting

Confirm the model:

```text
ansible-vault encrypt/decrypt/edit/view <file>; encrypt_string for inline vars.
Run with --ask-vault-pass or --vault-password-file. Vault IDs for multiple vaults.
```

Common pitfalls: committing the **vault password**; and encrypting non-secret data
(needless friction).

## Security and Best Practices

Encrypt **only secrets**, keep the **password out of version control** (secret store/CI),
restrict password-file perms, use **vault IDs** per environment, and rotate secrets. Never
`--ask-vault-pass` with the password on the command line.

## Hands-On Lab

Vault walkthroughs. **Shared prerequisites** — ansible-core. **Cost:** none.

### Lab 7.1 — Encrypt a variable inline

**Objective:** Encrypt a single secret value.

```bash
echo "s3cr3t" | ansible-vault encrypt_string --stdin-name "db_password" \
  --vault-password-file <(echo "vaultpw") 2>/dev/null | head -3
```

**Expected result:** an **`!vault |`** encrypted block for `db_password` — a committable
secret.

**Negative test:** commit the password in plaintext vars; **encrypt it** so the repo holds
no secrets.

**Cleanup:** none.

### Lab 7.2 — Encrypt a file

**Objective:** Encrypt a whole vars file.

```bash
echo "api_token: abc123" > secrets.yml
ansible-vault encrypt secrets.yml --vault-password-file <(echo "vaultpw")
head -1 secrets.yml   # $ANSIBLE_VAULT;1.1;AES256
```

**Expected result:** the file header shows **`$ANSIBLE_VAULT;1.1;AES256`** — an encrypted
file.

**Negative test:** store `secrets.yml` in plaintext in Git; **encrypt** it first.

**Cleanup:** `rm -f secrets.yml`.

### Lab 7.3 — View/edit encrypted content

**Objective:** Read an encrypted file without decrypting on disk.

```bash
ansible-vault view secrets.yml --vault-password-file <(echo "vaultpw") 2>/dev/null || echo "(recreate secrets.yml first)"
```

**Expected result:** the decrypted content shown **in memory** — safe inspection.

**Negative test:** `ansible-vault decrypt` to read then forget to re-encrypt; use **`view`/
`edit`** so it never sits decrypted on disk.

**Cleanup:** none.

### Lab 7.4 — Use vault in a playbook

**Objective:** Consume decrypted vars at runtime.

```bash
# playbook referencing api_token from the encrypted vars:
# ansible-playbook site.yml -e @secrets.yml --vault-password-file <(echo "vaultpw")
echo "run: ansible-playbook ... --vault-password-file <file>  (password NOT in the repo)"
```

**Expected result:** the playbook runs with secrets **decrypted at runtime** from the
password file — secrets stay encrypted at rest.

**Negative test:** pass the password on the command line (`--ask-vault-pass` typed in a
script); use a **password file / CI secret** kept out of the repo.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ansible Vault encrypts secret variables/files so they're safe to commit, decrypting at
runtime with a password kept out of the repo, with vault IDs for multiple environments.
This chapter encrypted a variable and a file, viewed content, and used it in a run.

- [ ] I can encrypt a variable inline.
- [ ] I can encrypt a vars file.
- [ ] I can view/edit encrypted content safely.
- [ ] I can consume vault secrets in a playbook.
- [ ] I completed Labs 7.1–7.4 including each negative test.
