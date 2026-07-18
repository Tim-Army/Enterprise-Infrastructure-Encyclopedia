# Release Process

Version tags matching `v*` publish verified complete-encyclopedia artifacts
to a GitHub release.

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

5. The [release workflow](.github/workflows/release.yml) builds DOCX, HTML,
   PDF/UA-1, EPUB 3, and website-ZIP editions and attaches them to the
   GitHub release automatically.
6. Verify the attached artifacts and the published
   [Pages portal](https://derg20.github.io/Enterprise-Infrastructure-Encyclopedia-v2/)
   before announcing the release.

## Versioning

Use semantic versioning against the curriculum, not the tooling:

- **Major** — a volume's scope or structure changes in a way that breaks
  existing chapter links.
- **Minor** — a new volume or chapter set is added.
- **Patch** — content corrections within existing chapters.
