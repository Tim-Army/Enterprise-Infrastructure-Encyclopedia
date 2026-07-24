# Vendor Certification Pipeline

How a vendor's certification program gets added to this encyclopedia, end
to end: the one-line request that starts it, the seven steps it runs, the
build and ship commands, and the traps that have actually caused errors.

This is the process used to add Cisco, Juniper, Dell, Palo Alto Networks,
Fortinet, VMware/Broadcom, and AWS. It complements
[CERTIFICATION_BLUEPRINTS.md](CERTIFICATION_BLUEPRINTS.md) (what is
mapped), [RELEASE_PROCESS.md](RELEASE_PROCESS.md) (how a release is cut),
and [EDITORIAL_STANDARDS.md](EDITORIAL_STANDARDS.md) (how chapters are
written).

## Starting the pipeline

One message naming the vendor is enough:

```text
Do the same for <vendor>
```

That authorizes the whole pipeline — all seven steps below, through push
and deploy verification, without pausing for confirmation between them.

### Optional qualifiers

| Qualifier | Effect |
| --- | --- |
| *(none)* | **Extend** the vendor's existing volume if it has one; create one if not. This is the default and the recent precedent — VMware extended Volume V, Palo Alto extended XVI, AWS extended XVII, and Fortinet was consolidated *into* Volume XIX. |
| `, new volume` | Create a separate volume instead of extending. This is a **minor** version bump, not a patch. |
| `, just the content — don't ship` | Stop after step 4. No archive, no tag, no release. |
| `, and check <specific thing>` | Verify a named track or exam you suspect has changed. |

### What runs without being asked

A Tracks row in the root README, a course-catalog appendix in Master
Appendices (Volume XCVII) carrying **exam** and **exam end date** columns,
United States English spelling, and the full ship-and-verify sequence.

### What still interrupts

Pre-approval covers the pipeline, not judgment. Stop and surface: a
verification that fails or contradicts what the repository already states,
a conflicting or unresolvable exam code, and any destructive step outside
this pipeline.

## The seven steps

1. **Primary-source verification.** Verify every code, name, format, and
   transition date against the vendor's own pages or exam-topics documents.
   Third-party summaries are not acceptable sources — several have been
   found wrong during these checks.
2. **Supersession handling.** Never delete retired exam content. Annotate
   it `retired on <date>` and add the successor alongside.
3. **Content.** Chapters following the house template
   ([templates/chapter.md](templates/chapter.md)), one diagram per chapter,
   blueprint mapping, and study plans derived from published domain
   weights. Naming paid courseware is fine; reproducing it is not.

   **Labs must cover every topic on every blueprint.** Coverage is
   measured against each certification's published exam guide, topic by
   topic — *not* against the chapter count. Where a vendor publishes an
   exam **guide** with sections and topics rather than a formal weighted
   blueprint, **that guide's topic list is the blueprint** and is treated
   identically — so vendors with no exam codes or no published domain
   weights (Google Cloud, Palo Alto Networks) are covered on the same
   terms. Harvest the topic list from the vendor's page rather than
   recalling it; it is cert data and falls under the same primary-source
   rule as exam codes. The template's single
   `## Hands-On Lab` section is a floor, not a target: where one lab
   cannot carry a chapter's topics, add further labs under that heading
   (`### Lab 2 — …`) or split the chapter. More chapters is acceptable;
   uncovered topics is not. Every lab records a blueprint-topic-to-lab
   mapping in the volume README so coverage is auditable.

   **Every lab must be a walkthrough.** A lab is a guided path that shows
   the work being done, not a set of tasks assigned to the reader. Each
   step carries the **actual runnable command** (full invocation, not
   "create a VM"), the **expected output or observable result** stated
   concretely enough to check against — a sample line, a status value, a
   count, a specific error string — and, where not obvious, why the step
   exists. Keep the house furniture around that: objective,
   prerequisites, cost implications where the platform bills, a
   **negative test** that proves the control actually works (shown as a
   walkthrough too, with the failing command and the exact error), and
   cleanup.
4. **Integration.** `book.yml`, volume README/INDEX/GLOSSARY,
   [SUMMARY.md](SUMMARY.md), [MASTER_TOC.md](MASTER_TOC.md), root README
   counts and Tracks row, [PROJECT_STATUS.md](PROJECT_STATUS.md),
   [CERTIFICATION_BLUEPRINTS.md](CERTIFICATION_BLUEPRINTS.md) row plus a
   dated note, and the `cspell.json` dictionary (alphabetized).
5. **Validate, build, ship.** The commands below.
6. **Verify the deploy.** Workflows green, zero annotations, and proof the
   live site serves the change.
7. **Currency rotation.** The vendor joins the recurring certification
   currency check.

## Commands

All commands run from the repository root, after
[SETUP.md](SETUP.md).

### Validate first

```bash
scripts/bash/validate.sh
```

Runs before building because it is fast and catches the two recurring
classes: markdownlint spacing (MD012 multiple blanks, MD022 blanks around
headings) and `cspell`. The spell dictionary is US English, which is also
what catches British spellings that slip into prose.

### Build all formats

```bash
scripts/bash/build-book.sh --format all
```

Takes several minutes across the full series; run it in the background.
Scoped variants are much faster while drafting:

```bash
scripts/bash/build-book.sh --format all --volume volume-17-aws-architecture-security
```

```bash
scripts/bash/build-book.sh --format all --chapter volumes/volume-17-aws-architecture-security/chapters/10-the-aws-certification-program-structure-foundational-tier-and-recertification.md
```

### Build the portal

```bash
scripts/bash/build-download-site.sh --output _site
```

Requires `build-book.sh` to have populated `output/` first. On macOS,
remove any `output/epub 2` or `output/html 2` sandbox artifacts before this
step, or they are copied into the archive.

### Package the release archive

Every build is a patch release. Compute the next version, then stage, strip
`.DS_Store`, and zip so the archive expands into one directory named for
its version:

```bash
V=$(git tag --sort=-v:refname | head -1 | sed 's/^v//' | awk -F. '{print $1"."$2"."$3+1}'); D="Enterprise-Infrastructure-Encyclopedia-v$V"; S=$(mktemp -d); mkdir -p "$S/$D" && cp -R _site/. "$S/$D/" && find "$S" -name .DS_Store -delete && (cd "$S" && zip -rq "$D.zip" "$D") && mv "$S/$D.zip" zip/ && echo "built zip/$D.zip"
```

Then prune `zip/` to the three most recent archives and add a row to the
version-log table in [zip/README.md](zip/README.md): version, created (the
zip's mtime, to the minute), deleted (`*current*`). Fill in the deleted
time of whatever was pruned.

### Commit and push

Stage the paths the task touched — never `git add -A`, which sweeps in
concurrent sessions' work:

```bash
git add book.yml README.md SUMMARY.md MASTER_TOC.md PROJECT_STATUS.md CERTIFICATION_BLUEPRINTS.md cspell.json volumes/volume-NN-vendor volumes/volume-97-master-appendices diagrams/volume-NN-vendor zip/
```

```bash
git push origin main
```

### Tag the release

```bash
git tag -a v1.0.3 -m "Enterprise Infrastructure Encyclopedia v1.0.3" && git push origin v1.0.3
```

Pushing the tag is what triggers `release.yml` to build the EPUB and create
the GitHub release. Without the tag there is no release, and the archive in
`zip/` will not match any published version.

## Verifying the deploy

Green workflows are not sufficient evidence. Check all three.

```bash
gh run list --limit 10 --json name,status,conclusion,headSha --jq '.[] | select(.headSha|startswith("<sha>")) | "\(.name): \(.status)/\(.conclusion)"'
```

```bash
gh release view v1.0.3 --json tagName,assets --jq '"\(.tagName): \(.assets[].name)"'
```

Then confirm zero annotations per run, and `curl` the live URLs — an HTTP
200 plus a `grep -c` for a fact that only the new content contains, so a
cached or stale page cannot pass.

## Traps that have caused real errors

- **Never state certification data from model memory.** A wireless track
  was once flagged as fabricated when it was real and simply newer than the
  model's knowledge. Verify against the vendor, and never "correct"
  repository cert data from recollection.
- **Codes are often not in the page text.** Broadcom injects them through a
  `getjson` education-program API; AWS puts them in the Skill Builder
  exam-prep link on each certification page. Fetching the rendered HTML and
  grepping finds nothing in both cases.
- **Read which noun a retirement notice attaches to.** AWS's Cloud
  Practitioner page carries a retirement notice for its *Indonesian
  language version*, not for the exam. Exam retirement, language-version
  retirement, and a blueprint version bump all read alike.
- **Check the current ship scheme before shipping.** It has changed —
  four-digit `v00xx` archives gave way to semver patch releases with
  matching tags. Confirm against [zip/README.md](zip/README.md) and the
  existing tags rather than repeating the last remembered scheme.
- **Derive counts from the files.** The root README, `PROJECT_STATUS.md`,
  and `book.yml` each track volume and chapter counts separately and drift
  silently.
- **US English throughout.** `cspell` catches the repository; nothing
  catches prose written elsewhere.

## When a change does not need a release

Only ship when the **published site** changed. Changes confined to CI
workflows or to root documents that are never rendered get no archive and
no release — `_site` is byte-identical. The root
[README.md](README.md) *is* rendered into the EPUB, so a change to it does
count as a published-site change.
