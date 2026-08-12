# Volume CLXXI Glossary

Definitions for terms introduced in **Volume CLXXI — Alpine Linux**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **apk (Alpine Package Keeper)** — Alpine's package manager; installs, removes, and upgrades signed packages and tracks the `world` file.
- **BusyBox** — a single multi-call binary providing the shell (`ash`) and coreutils-equivalent applets that make up Alpine's base userland.
- **doas** — OpenBSD's small privilege-escalation tool, Alpine's preferred alternative to `sudo`, configured in `/etc/doas.conf`.
- **edge** — Alpine's rolling development branch (main + community + testing at `edge`); unsupported, for testing only.
- **gcompat** — a glibc-compatibility shim that lets some glibc-linked binaries run on musl.
- **in.tftpd** — the TFTP server binary from the `tftp-hpa` package.
- **local.d** — the OpenRC `local` service's directory of `*.start`/`*.stop` scripts run at boot/shutdown; Alpine's simplest durable boot hook.
- **musl libc** — Alpine's lightweight C standard library, used instead of glibc; smaller and static-linking friendly, with some glibc compatibility differences.
- **OpenRC** — Alpine's dependency-based init and service manager; services live in `/etc/init.d` and are managed with `rc-service` and `rc-update`.
- **resize2fs** — the ext filesystem-growth tool used to extend `/` after enlarging a disk (`/dev/sda` on a whole-disk cloud layout).
- **setup-alpine** — the interactive installer script that configures keymap, hostname, network, timezone, mirror, SSH, and disk, then installs Alpine.
- **sys / data / diskless** — Alpine's three install modes: a normal disk install, a RAM system with `/var` on disk, and a fully RAM-resident system persisted with `lbu`.
- **tftp-hpa** — the community-repository package providing the `in.tftpd` server and `tftp` client.
- **TFTP (Trivial File Transfer Protocol)** — a minimal, unauthenticated UDP (port 69) file-transfer protocol used to stage firmware, boot files, and device configurations.
- **virtual package** — an `apk` group created with `--virtual` (for example `.build-deps`) so several packages can be removed together.
- **world file (`/etc/apk/world`)** — the plain-text list of explicitly-requested packages; the installed system is always its dependency closure.
