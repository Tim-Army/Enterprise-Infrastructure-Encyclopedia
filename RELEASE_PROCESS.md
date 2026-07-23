# Release Process

Version tags matching `v*` publish the verified complete-encyclopedia EPUB
to a GitHub release. (The single-page complete-encyclopedia HTML edition was
retired; the portal serves per-volume and per-chapter HTML, and the EPUB is
the one-file edition.)

**Naming.** The release is titled `Enterprise-Infrastructure-Encyclopedia
<tag>` and the EPUB is attached as
`Enterprise-Infrastructure-Encyclopedia-<tag>.epub`, so the release name and
its asset both lead with the project name and carry the version — matching
the offline archive (`Enterprise-Infrastructure-Encyclopedia-v<tag>.zip`)
and the EPUB filename convention.

## Steps

1. Confirm every volume in [book.yml](book.yml) is `build_eligible: true`
   and [PROJECT_STATUS.md](PROJECT_STATUS.md) shows no volume blocked on
   technical review.
2. Run `scripts/bash/validate.sh` and `scripts/bash/check-external-links.sh`
   locally and resolve any failures.
3. Update [SOFTWARE_VERSIONS.md](SOFTWARE_VERSIONS.md) if any baseline
   changed since the last release.
4. Tag the release commit on `main`:

   ```bash
   git tag -a vX.Y.Z -m "Enterprise Infrastructure Encyclopedia vX.Y.Z"
   git push origin vX.Y.Z
   ```

5. The [release workflow](.github/workflows/release.yml) builds the
   complete-encyclopedia EPUB 3 edition and attaches it to the
   GitHub release automatically.
6. Verify the attached artifacts and the published
   [Pages portal](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/)
   before announcing the release.

## Versioning

Use semantic versioning against the curriculum, not the tooling. **Every
build is a release:** each content change to the published site bumps the
**patch** and is tagged, so a matching GitHub release and offline archive
(`Enterprise-Infrastructure-Encyclopedia-v<tag>.zip`) always exist. Minor
and major bumps are made deliberately.

- **Major** — a volume's scope or structure changes in a way that breaks
  existing chapter links.
- **Minor** — a new volume or chapter set is added.
- **Patch** — any other content change; cut per build, tagged as part of
  shipping the offline archive.

**Retention.** Patch releases accumulate quickly (one per build), so the
release workflow keeps **three releases total, milestones excluded** — the
three most recent `vX.Y.Z` (Z>0) releases survive and older ones are deleted
(release and tag). Milestone releases (`vX.Y.0` — the first release and
deliberate minor/major bumps) are excluded from pruning and do not count
toward the three. The offline archive in `zip/` follows the same
three-most-recent rule.

Because milestones are never pruned, they grow without bound. **Revisit this
retention policy once there are ten milestone releases** — the release
workflow prints the current milestone count on every run and raises a notice
at ten.
