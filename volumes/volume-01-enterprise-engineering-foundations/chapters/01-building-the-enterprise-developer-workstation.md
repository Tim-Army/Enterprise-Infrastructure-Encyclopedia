# Chapter 01: Building the Enterprise Developer Workstation

![Lab flow for this chapter: a lab-only ed25519 key is generated on the developer workstation and registered with GitHub as a signing key; a commit made with that key verifies as a Good signature locally and Verified on GitHub, while a commit signed with an unregistered key still signs locally but shows as Unverified on GitHub.](../../../diagrams/volume-01-enterprise-engineering-foundations/chapter-01-signed-commit-workstation-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: generating and registering an SSH signing key, then verifying signed commits, including the unregistered-key negative test.*

## Learning Objectives

- Explain why a reproducible, version-controlled workstation configuration
  reduces onboarding time and "works on my machine" defects.
- Select and justify a package manager, shell, and version-manager strategy
  for a multi-project enterprise engineering role.
- Configure Git identity, commit signing, and SSH authentication that meet
  common enterprise source-control policies.
- Install and validate a container runtime, an editor with a reproducible
  extension set, and a secrets-handling workflow.
- Build a bootstrap script that provisions a new workstation from a clean
  operating system install and verify it idempotently.

## Theory and Architecture

An enterprise developer workstation is not a personal device that happens to
run work software — it is a managed endpoint that must satisfy three
competing requirements at once: engineer productivity, organizational
security policy, and reproducibility across a team. Treat the workstation as
an artifact with a declared, versioned configuration, the same way you would
treat a server. The practice of describing a machine's desired state in
source-controlled files — sometimes called "dotfiles as code" — is the
workstation-scale application of infrastructure as code (IaC), a concept
this volume returns to in [Chapter 03](03-automation-architecture.md) and formalizes in [Volume IX](../../volume-09-infrastructure-automation/README.md).

Three architectural layers make up a modern engineering workstation:

1. **Host layer.** The operating system, its package manager, and baseline
   security controls (disk encryption, screen lock, endpoint protection).
   Most enterprises standardize on macOS (via MDM such as Jamf or Kandji),
   Windows with WSL2, or a Linux distribution with a corporate image.
2. **Toolchain layer.** Shell, Git, language runtimes, version managers,
   container runtime, and editor/IDE. This layer changes far more often than
   the host layer and benefits most from declarative, replayable setup.
3. **Identity and secrets layer.** SSH keys, GPG/Sigstore commit signing,
   credential helpers, and short-lived cloud credentials. This layer is
   where workstation compromise translates directly into infrastructure
   compromise, so it receives dedicated security treatment later in this
   chapter.

### Reproducibility models

There are three common patterns for making a workstation reproducible, and
most enterprise engineers end up combining two of them:

| Model | Mechanism | Strength | Weakness |
| --- | --- | --- | --- |
| Dotfiles repository | Git repo of shell/editor/tool config, symlinked into `$HOME` | Fast, transparent, works on bare metal | Does not capture installed packages by itself |
| Bootstrap script | Idempotent shell script that installs packages and links dotfiles | Reproduces a machine from zero | Script drifts from reality if not run regularly |
| Declarative package manifest | A manifest (Homebrew `Brewfile`, `mise` config, a Nix flake) that a tool reconciles against | Auditable diff of installed state | Steeper learning curve, ecosystem-specific |

A dotfiles repository plus an idempotent bootstrap script that consumes a
declarative package manifest is the most common enterprise pattern: it is
simple enough for every engineer to read, and it gives platform engineering
teams a single artifact to review for compliance.

### Version management

Enterprise engineers routinely work across multiple repositories that pin
different language and tool versions. A per-project version manager (such as
`mise`, the modern replacement for `asdf`) reads a version file committed to
each repository and activates the correct interpreter/runtime automatically
on `cd`. This removes an entire class of "wrong Node version" or "wrong
Terraform version" defects and is the workstation-side counterpart to the
dated version baselines this encyclopedia maintains in
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).

## Design Considerations

- **Managed vs. unmanaged endpoints.** If the organization enrolls laptops in
  an MDM, workstation setup must coexist with policy-pushed configuration
  profiles (disk encryption enforcement, firewall rules, restricted admin
  rights). Confirm which layer — MDM or the engineer's own bootstrap script —
  owns each control before scripting around it.
- **macOS vs. Linux vs. WSL2.** macOS and Linux offer POSIX-compatible
  shells and the widest tooling compatibility with production Linux targets.
  WSL2 lets Windows-standardized enterprises give engineers a real Linux
  kernel without dual-booting, at the cost of an extra virtualization layer
  to reason about for file-system performance and container networking.
- **Container runtime choice.** Docker Desktop requires a paid license above
  a headcount/revenue threshold at many organizations; Podman and
  Rancher Desktop are common license-free alternatives with mostly
  Docker-CLI-compatible interfaces. Decide this before writing bootstrap
  automation, since Compose file compatibility and rootless-mode defaults
  differ.
- **Local admin rights.** Some security policies remove local administrator
  rights from engineers, which changes how package managers, container
  runtimes, and VPN clients must be installed (often through an internal
  self-service catalog rather than `sudo`). Bootstrap scripts must degrade
  gracefully when they cannot escalate privileges.
- **Golden image vs. self-service bootstrap.** A golden image (a pre-built
  OS image with the toolchain baked in) minimizes first-day setup time but
  goes stale and requires image-pipeline investment. A self-service
  bootstrap script is slower on day one but stays current automatically
  because it installs from source-of-truth manifests on every run.
- **Secrets on a laptop.** Decide early whether long-lived cloud credentials
  are permitted on developer machines at all, or whether all cloud access
  must go through short-lived, broker-issued credentials (see Security and
  Best Practices below). This decision shapes the entire toolchain layer.

## Implementation and Automation

The following bootstrap approach targets macOS and Debian/RHEL-family Linux,
the two most common enterprise engineering platforms, using Homebrew as the
package manager (Homebrew now supports Linux as well as macOS).

### 1. Base package manager

```bash
# macOS and Linux — install Homebrew if not already present
if ! command -v brew >/dev/null 2>&1; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
brew update
```

### 2. Declarative package manifest

Commit a `Brewfile` to the dotfiles repository so the toolchain is
auditable and diffable in pull requests:

```ruby
# Brewfile
brew "git"
brew "gh"
brew "mise"
brew "direnv"
brew "shellcheck"
brew "jq"
brew "gnupg"
brew "podman"
cask "visual-studio-code"
```

Apply it with:

```bash
brew bundle --file=./Brewfile
```

### 3. Shell and version manager

```bash
# ~/.zshrc — activate mise for automatic per-project runtime versions
eval "$(mise activate zsh)"
eval "$(direnv hook zsh)"
```

Per-project version pinning then lives in each repository, not on the
workstation:

```toml
# .mise.toml in a project repository
[tools]
node = "22"
terraform = "1.9"
```

### 4. Git identity and commit signing

Enterprises increasingly require signed commits to satisfy supply-chain and
audit requirements. SSH-based signing (supported natively by Git since 2.34)
is simpler to operate than GPG for teams that already distribute SSH keys:

```bash
git config --global user.name "Jordan Lee"
git config --global user.email "jordan.lee@example.com"
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Generate a modern SSH key and register it with the Git host:

```bash
ssh-keygen -t ed25519 -C "jordan.lee@example.com" -f ~/.ssh/id_ed25519
gh ssh-key add ~/.ssh/id_ed25519.pub --title "workstation-2026" --type authentication
gh ssh-key add ~/.ssh/id_ed25519.pub --title "workstation-2026" --type signing
```

### 5. Container runtime

```bash
brew install podman
podman machine init --cpus 4 --memory 8192 --disk-size 60
podman machine start
podman run --rm hello-world
```

### 6. Editor and reproducible extensions

Commit an extensions manifest alongside the dotfiles so any engineer can
replay the editor setup:

```json
{
  "recommendations": [
    "editorconfig.editorconfig",
    "davidanson.vscode-markdownlint",
    "streetsidesoftware.code-spell-checker",
    "hashicorp.terraform",
    "redhat.ansible"
  ]
}
```

```bash
# Install every recommended extension from a workspace manifest
jq -r '.recommendations[]' .vscode/extensions.json | xargs -I{} code --install-extension {}
```

### 7. A single bootstrap entry point

Tie the previous steps together in one idempotent script so a new
workstation — or a re-imaged one — can be provisioned with one command:

```bash
#!/usr/bin/env bash
# bootstrap.sh — idempotent workstation setup
set -euo pipefail

echo "==> Installing Homebrew packages"
brew bundle --file=./Brewfile

echo "==> Linking dotfiles"
for f in zshrc gitconfig; do
  ln -sf "$(pwd)/dotfiles/${f}" "${HOME}/.${f}"
done

echo "==> Configuring Git signing"
git config --global gpg.format ssh
git config --global commit.gpgsign true

echo "==> Verifying container runtime"
podman run --rm hello-world >/dev/null && echo "Podman OK"

echo "Bootstrap complete."
```

Running this script twice in a row must produce no errors and no unwanted
duplicate state — that idempotency is what allows it to double as a drift
check.

## Validation and Troubleshooting

- **Verify signed commits.** Run `git log --show-signature -1` after a test
  commit; the output must show `Good "git" signature`. If it instead reports
  `No signature`, confirm `commit.gpgsign` is `true` and that
  `user.signingkey` points at a key registered with the Git host as a
  signing key, not only an authentication key.
- **Verify SSH authentication.** `ssh -T git@github.com` should return a
  greeting with your username. A `Permission denied (publickey)` error
  usually means the key was never added to the agent (`ssh-add
  ~/.ssh/id_ed25519`) or was registered as the wrong key type on the host.
- **Verify version manager activation.** `cd` into a project with a
  `.mise.toml` and run `mise current`; it must show the pinned versions, not
  a global fallback. If it falls back, confirm the shell hook (`mise
  activate`) is sourced in an interactive shell, not only a login shell.
- **Verify container runtime networking.** `podman run --rm curlimages/curl
  -sI https://example.com` should return HTTP headers. Failures here are
  frequently corporate TLS-inspection proxies that require the proxy's root
  certificate to be trusted inside the VM/container context, not just on the
  host.
- **Bootstrap idempotency check.** Re-run `bootstrap.sh` and diff `brew
  list` output before and after; a properly idempotent script produces an
  empty diff on the second run.
- **Common failure: PATH ordering.** Multiple version managers (a language's
  native installer plus `mise`) fighting over `PATH` precedence is the most
  common source of "wrong version" reports. Run `which -a node` (or the
  relevant binary) and confirm only the expected manager's shim appears
  first.

## Security and Best Practices

- Enable full-disk encryption (FileVault on macOS, LUKS on Linux) before any
  other setup step; an unencrypted laptop is a full infrastructure-access
  breach the moment it is lost.
- Prefer SSH- or hardware-token-based (FIDO2/`sk-ecdsa`) commit signing over
  long-lived GPG keys with no expiration; hardware-backed keys cannot be
  exfiltrated by copying a file.
- Do not store long-lived cloud provider credentials (static AWS access
  keys, service-account JSON keys) on the workstation. Use short-lived,
  identity-federated credentials (AWS IAM Identity Center, `aws sso login`,
  cloud CLI OIDC device flows) that expire in hours, not years.
- Use a credential manager (`git-credential-manager`, the platform keychain,
  or a password manager's CLI/SSH-agent integration) instead of storing
  tokens in plaintext files such as `.netrc` unless the file is itself
  encrypted at rest.
- Pin and checksum-verify any installer script fetched from the network
  (`curl | bash` patterns) rather than trusting an unpinned URL; prefer
  package manager repositories with signed packages where available.
- Rotate SSH signing/authentication keys on a defined schedule (for example,
  annually or on role change) and immediately on suspected compromise or
  device loss; deregister the old key from the Git host in the same change.
- Keep the bootstrap script and dotfiles repository itself under code
  review — a compromised bootstrap script is a supply-chain attack vector
  against every engineer who runs it.

## References and Knowledge Checks

**References**

- [Git documentation, *Signing Your Work*](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work) — SSH and GPG commit signing.
- [GitHub CLI (`gh`) manual](https://cli.github.com/manual/) — `gh ssh-key`, `gh auth login`.
- [`mise` documentation](https://mise.jdx.dev/) — per-project runtime version management.
- [Podman documentation](https://docs.podman.io/) — `podman machine` for macOS/Windows container hosts.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated baseline for
  Node.js and pnpm referenced throughout this volume.

**Knowledge checks**

1. Why is a dotfiles repository alone insufficient to make a workstation
   fully reproducible, and what artifact closes the gap?
2. What is the operational difference between an SSH authentication key and
   an SSH signing key registered with a Git host?
3. Name two reasons a security team might prohibit long-lived static cloud
   credentials on developer laptops.
4. Why does re-running a bootstrap script twice serve as a validation step,
   not just a convenience?

## Hands-On Lab

**Objective:** Build and validate a minimal, idempotent workstation
bootstrap that installs Git, configures SSH-based commit signing, and
verifies the configuration — safely, in a disposable environment.

**Prerequisites**

- A macOS or Linux machine (or a disposable VM/container you are willing to
  modify) with `bash`, `curl`, and `git` available.
- A GitHub account and the GitHub CLI (`gh`) installed and authenticated
  (`gh auth login`).

**Steps**

1. Create a working directory and a minimal manifest:

   ```bash
   mkdir -p ~/lab-workstation/dotfiles && cd ~/lab-workstation
   cat > Brewfile <<'EOF'
   brew "git"
   brew "gh"
   EOF
   ```

2. Generate a lab-only SSH key (do not reuse a production key):

   ```bash
   ssh-keygen -t ed25519 -C "lab-workstation" -f ~/.ssh/id_ed25519_lab -N ""
   ```

3. Register the key as a signing key on your GitHub account:

   ```bash
   gh ssh-key add ~/.ssh/id_ed25519_lab.pub --title "lab-workstation-signing" --type signing
   ```

4. Configure a scoped Git identity for this lab only, using
   `--local` inside a throwaway repository so global settings are untouched:

   ```bash
   git init ~/lab-workstation/repo && cd ~/lab-workstation/repo
   git config --local user.name "Lab Engineer"
   git config --local user.email "lab@example.com"
   git config --local gpg.format ssh
   git config --local user.signingkey ~/.ssh/id_ed25519_lab.pub
   git config --local commit.gpgsign true
   ```

5. Make and sign a commit:

   ```bash
   echo "# Lab" > README.md
   git add README.md
   git commit -m "Initial commit"
   ```

6. **Expected result:** Validate the signature:

   ```bash
   git log --show-signature -1
   ```

   The output must include `Good "git" signature for ... using ED25519 key`.

7. **Negative test:** Temporarily point `user.signingkey` at a key that was
   never registered with GitHub, and commit again:

   ```bash
   ssh-keygen -t ed25519 -f /tmp/unregistered_key -N ""
   git config --local user.signingkey /tmp/unregistered_key.pub
   echo "change" >> README.md
   git add README.md
   git commit -m "Unregistered key test"
   git log --show-signature -1
   ```

   **Expected result:** Git still creates a local cryptographic signature
   (local signing does not require host registration), but `gh` and GitHub's
   web UI will show the commit as **Unverified** because the key is not
   registered to your account — confirm this by pushing to a scratch
   repository and checking the commit's badge in the GitHub UI. This
   demonstrates why key registration, not just local signing, is the control
   that matters for supply-chain trust.

8. **Cleanup:**

   ```bash
   cd ~ && rm -rf ~/lab-workstation
   rm -f ~/.ssh/id_ed25519_lab ~/.ssh/id_ed25519_lab.pub /tmp/unregistered_key /tmp/unregistered_key.pub
   gh ssh-key list   # confirm the lab key's ID, then:
   gh ssh-key delete <key-id>
   ```

## Summary and Completion Checklist

A reproducible enterprise workstation treats configuration as versioned,
reviewable code across three layers — host, toolchain, and identity/secrets
— rather than as manual, undocumented setup. Declarative package manifests,
per-project version managers, and SSH-based commit signing reduce onboarding
time and close common supply-chain and credential-hygiene gaps. Bootstrap
automation should be idempotent so it doubles as its own drift check.

- [ ] Can explain the three architectural layers of a managed workstation.
- [ ] Can justify a reproducibility model (dotfiles, bootstrap script, or
      declarative manifest) for a given team's constraints.
- [ ] Can configure and verify SSH-based Git commit signing.
- [ ] Can install and smoke-test a container runtime.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
