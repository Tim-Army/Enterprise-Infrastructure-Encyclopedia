# Chapter 09: Maintenance and Keeping Current

## Learning Objectives

- Keep LibreNMS updated on its rolling release.
- Validate the install after changes.
- Back up the database and RRD data.
- Track the project and community.
- Complete a walkthrough for each maintenance task.

## Theory and Architecture

LibreNMS ships a **rolling (CalVer) release** — frequent updates applied with the
built-in updater (`daily.sh` / `lnms` update path), which pulls code, updates
dependencies, and runs database migrations. **`validate.php`** checks health after any
change. Durable state to protect is the **MariaDB** database (config, alerts, history)
and the **RRD** files (time-series); back up both. The current release is **26.7.0**;
track releases and release notes on GitHub.

## Design Considerations

Stay on the **rolling release** (don't drift far behind — migrations assume
incremental updates), run **`validate.php`** after every change, and back up **DB +
RRD** before updating. Watch the release notes for breaking changes and new OS/device
support.

## Implementation and Automation

The labs update, validate, back up, and check the current release.

## Validation and Troubleshooting

Confirm the maintenance model:

```text
Update: daily.sh / lnms update -> pull code + composer + DB migrations.
validate.php: health check. Backups: mysqldump (DB) + rrd/ directory.
Releases: github.com/librenms/librenms/releases (CalVer, e.g. 26.7.0).
```

Common pitfalls: skipping updates until far behind (migration pain); and backing up the
DB but not **RRD** (lose history).

## Security and Best Practices

Update on a **cadence**, run **`validate.php`** each time, back up **both** the database
and RRD data, and read release notes before updating. Keep PHP/MariaDB within supported
versions.

## Hands-On Lab

Maintenance walkthroughs. **Shared prerequisites** — a running LibreNMS (`daily.sh`
available); `curl`, `python3`. **Cost:** none.

### Lab 9.1 — Update LibreNMS

**Objective:** Run the built-in updater.

```bash
docker compose exec librenms ./daily.sh 2>&1 | tail -15
# (bare-metal: sudo -u librenms ./daily.sh)
```

**Expected result:** update output showing code pull + **migrations** applied — the
rolling-update path.

**Negative test:** patch files by hand; the **updater** runs dependency + DB migrations
too — use it.

**Cleanup:** none.

### Lab 9.2 — Validate after change

**Objective:** Confirm health post-update.

```bash
docker compose exec librenms php validate.php | tail -20
```

**Expected result:** validation ending **OK** (or clear warnings) — a healthy install.

**Negative test:** assume the update worked; **validate** — it catches migration/permission
issues.

**Cleanup:** none.

### Lab 9.3 — Back up DB and RRD

**Objective:** Protect durable state.

```bash
docker compose exec -T db mysqldump -u librenms -p"$DBPASS" librenms > librenms-db.sql
docker compose exec librenms sh -c 'tar czf - rrd 2>/dev/null' > librenms-rrd.tgz
ls -lh librenms-db.sql librenms-rrd.tgz | awk '{print $5,$9}'
```

**Expected result:** a non-empty **DB dump and RRD archive** — a full restore point.

**Negative test:** back up only the database; without **RRD** you lose all historical
graphs — back up both.

**Cleanup:** store or remove the backups per policy.

### Lab 9.4 — Check the current release

**Objective:** Read the latest LibreNMS release.

```bash
curl -sS "https://api.github.com/repos/librenms/librenms/releases/latest" \
  | python3 -c "import sys,json;print('latest:',json.load(sys.stdin)['tag_name'])"
```

**Expected result:** the latest tag (a **CalVer** release like 26.7.0) — what to track.

**Negative test:** run a months-old release; the **rolling** model expects incremental
updates — stay current.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

LibreNMS is maintained on a rolling CalVer release via the built-in updater, validated
with `validate.php`, and protected by backing up both the database and RRD data. This
chapter updated, validated, backed up, and checked the current release.

- [ ] I can update LibreNMS with the built-in updater.
- [ ] I can validate the install after changes.
- [ ] I can back up both the database and RRD data.
- [ ] I can find the current release to plan updates.
- [ ] I completed Labs 9.1–9.4 including each negative test.
