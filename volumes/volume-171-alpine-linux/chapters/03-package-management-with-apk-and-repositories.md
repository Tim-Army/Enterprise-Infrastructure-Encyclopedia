# Chapter 03: Package Management with apk and Repositories

## Learning Objectives

- Use the core `apk` verbs to install, remove, search, and inspect packages.
- Explain the `world` file and why Alpine tracks *what you asked for* rather than
  the full dependency closure.
- Configure repositories — main, community, and edge/testing — and the mirror.
- Pin a package to a specific repository with a tagged source.
- Manage the package cache for containers and for persistent hosts.

## Theory and Architecture

`apk` (Alpine Package Keeper) is Alpine's package manager. It is fast because its
repository indexes are compact and cryptographically signed, and because it plans
the whole transaction before touching the filesystem. Two ideas make `apk`
different from `apt`/`dnf`:

- **The `world` file (`/etc/apk/world`) is the source of truth.** It lists only the
  packages *you explicitly asked for* — your "world" — not their dependencies.
  `apk add X` adds `X` to the world and pulls in whatever `X` needs; `apk del X`
  removes `X` from the world and garbage-collects dependencies nothing else needs.
  The installed system is always the dependency closure of the world file, which
  makes the machine's intent legible in a single short file.
- **Repositories are plain URLs in `/etc/apk/repositories`.** Each line is a
  mirror path to a repository:

  ```text
  https://dl-cdn.alpinelinux.org/alpine/v3.24/main
  https://dl-cdn.alpinelinux.org/alpine/v3.24/community
  #https://dl-cdn.alpinelinux.org/alpine/edge/testing
  ```

Alpine splits packages into repositories with different support promises:

| Repository | Contents | Support |
| --- | --- | --- |
| **main** | Core packages the Alpine team maintains and supports for the release's life | Two years |
| **community** | Community-maintained packages for the stable release | Best-effort, for the release |
| **testing** | New/unreviewed packages; only exists under **edge** | None |
| **edge** | The rolling development branch (main + community + testing at `edge`) | None — development only |

A stable host uses **main + community** at a pinned release (`v3.24`). **edge** and
**testing** are for development and for pulling a single newer package, never for a
production base.

### Versions, upgrades, and virtual packages

`apk upgrade` moves every world package to the newest version available in the
configured repositories; `apk version` reports which installed packages are behind.
A **virtual package** (created with `-t`/`--virtual`) groups several packages under
one name so you can remove them together — invaluable for build dependencies:

```sh
apk add --virtual .build-deps gcc make musl-dev
# ...build something...
apk del .build-deps          # removes exactly that group, nothing else
```

### The cache

By default `apk` downloads packages, installs them, and does not keep the archives.
A persistent host can enable a **cache** (`/etc/apk/cache`) so re-installs and
rollbacks are local; a container image should instead use **`--no-cache`** so no
index is written into the image layer.

## Design Considerations

- **Pin to a stable release for anything you operate.** Point
  `/etc/apk/repositories` at `v3.24` (or the current stable), not `edge`, unless
  you are deliberately testing.
- **Enable community deliberately.** Many useful packages (including `tftp-hpa`,
  Chapter 05) live in **community**; enable it, but know it is best-effort.
- **Reach for edge surgically, not wholesale.** When you need one package newer
  than stable ships, add a *tagged* edge source and pin only that package, rather
  than moving the whole system to edge.
- **Choose the cache model to match the target.** `--no-cache` for images;
  `apk cache` for hosts that reinstall or roll back.

## Implementation and Automation

Core verbs:

```sh
apk update                     # refresh repository indexes
apk add tftp-hpa tcpdump       # install (adds to /etc/apk/world)
apk del tcpdump                # remove (drops from world, GC deps)
apk info                       # list installed packages
apk info -a tftp-hpa           # everything about one package
apk search -v tftp             # search available packages
apk policy tftp-hpa            # which repo/version would be used
apk version -l '<'             # installed packages older than the repo
apk upgrade                    # upgrade the world to the newest available
apk fix                        # repair a partially-installed package
```

Enable the **community** repository (uncomment its line) and refresh:

```sh
sed -i '/\/community/s/^#//' /etc/apk/repositories
apk update
```

Pin a single package from **edge** with a repository **tag** (`@edge`), leaving the
rest of the system on stable:

```sh
echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories
apk update
apk add somepkg@edge           # only this package comes from edge
```

Container-friendly install (writes nothing to the cache/index in the layer):

```sh
apk add --no-cache curl
```

## Validation and Troubleshooting

```sh
cat /etc/apk/world             # exactly what you asked for
cat /etc/apk/repositories      # which repos/mirror are active
apk policy <pkg>               # the source and version apk will choose
apk version                    # installed vs available
```

Common issues:

- **`ERROR: unable to select packages ... (no such package)`.** The package lives
  in **community** or **edge** and that repository is not enabled — enable it and
  `apk update`.
- **`apk update` fails with a bad signature or 404.** The mirror line points at a
  release that does not exist (a typo like `v3.42`) or an unreachable mirror; fix
  the URL.
- **An `@edge` pin dragged in newer dependencies.** A tagged package can pull edge
  dependencies; check `apk policy` and prefer the stable version unless the newer
  one is required.

## Security and Best Practices

- Keep the system on a **supported stable release** and run `apk upgrade` on a
  schedule (Chapter 07); indexes are signed, so upgrades are authenticated.
- Do not run a production host on **edge/testing** — those packages are unreviewed
  and unsupported.
- Use `--virtual` for build dependencies so a build box does not accumulate
  toolchain packages it no longer needs.
- Use `--no-cache` in images to avoid leaking an index and to keep layers small.

## References and Knowledge Checks

- Alpine wiki — [Alpine Package Keeper (apk)](https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper)
  and [Repositories](https://wiki.alpinelinux.org/wiki/Repositories).
- Alpine wiki — [Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository).

**Knowledge checks:**

1. What does `/etc/apk/world` contain, and how does it differ from the full list of
   installed packages?
2. Which repository is supported for two years, and which has no support at all?
3. How do you install one newer package from edge without moving the whole system
   to edge?

## Hands-On Lab

**Objective:** Drive `apk` end to end — install, inspect, enable community, pin from
edge, and manage the cache.

**Shared prerequisites** — an Alpine host with a working resolver and `apk update`
succeeding (Chapter 02). **Cost:** none.

### Lab 3.1 — Install, inspect, and remove

**Objective:** See the `world` file change as you add and remove a package.

```sh
cp /etc/apk/world /tmp/world.before
apk add tcpdump
diff /tmp/world.before /etc/apk/world     # tcpdump added
apk info -a tcpdump | head
apk del tcpdump
diff /tmp/world.before /etc/apk/world     # back to the original set
```

**Expected result:** `tcpdump` appears in `world` after `add` and disappears after
`del`, and its dependencies are garbage-collected — the world file mirrors your
intent exactly.

**Negative test:** `apk del` a package another package depends on; `apk` refuses or
warns rather than breaking the closure — dependencies are protected.

**Rollback:** none (returned to the original set).

### Lab 3.2 — Enable community and install from it

**Objective:** Install a package that lives in community (the TFTP server used in
Chapter 05).

```sh
apk add tftp-hpa || echo "not found until community is enabled"
sed -i '/\/community/s/^#//' /etc/apk/repositories
apk update
apk policy tftp-hpa            # now resolvable from community
apk add tftp-hpa
```

**Expected result:** `tftp-hpa` is unresolvable until community is enabled, then
`apk policy` shows it coming from the community repository and it installs.

**Negative test:** search for `tftp-hpa` with only `main` enabled; it is not found —
the package is in community, which must be enabled first.

**Rollback:** `apk del tftp-hpa` (Chapter 05 reinstalls it).

### Lab 3.3 — Pin one package from edge

**Objective:** Pull a single package from edge with a tag, leaving the base stable.

```sh
cp /etc/apk/repositories /tmp/repos.before
echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories
apk update
apk policy htop               # stable and @edge candidates both listed
apk add htop@edge
apk info -a htop | grep -i version
```

**Expected result:** `apk policy` lists both a stable and an `@edge` candidate, and
the `@edge` version installs while the rest of the system stays on stable.

**Negative test:** point the whole `/etc/apk/repositories` at edge and `apk
upgrade`; the entire system moves to an unsupported rolling branch — pin instead.

**Rollback:** `cp /tmp/repos.before /etc/apk/repositories && apk update` to restore
stable-only sources.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

`apk` manages Alpine packages around the `world` file — the short, declarative list
of what you asked for — with the installed system always its dependency closure.
Repositories are plain URLs split into supported **main**, best-effort
**community**, and unsupported **edge/testing**; a stable host runs main + community
at a pinned release and reaches for edge only with a tagged, per-package pin.
Virtual packages group build dependencies for clean removal, and the cache model
(`--no-cache` vs `apk cache`) follows whether the target is an image or a host.

- [ ] Can install, remove, search, and inspect packages with `apk`.
- [ ] Can explain the `world` file and dependency garbage collection.
- [ ] Can enable community and pin a single package from edge.
- [ ] Can choose the right cache model for a container vs a host.
- [ ] Completed Labs 3.1–3.3 including each negative test.
