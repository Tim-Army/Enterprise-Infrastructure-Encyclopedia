---
name: srg-mapping-for
description: Build DISA STIG and SRG mapping chapters for a vendor's products in Volume CLXXII (DISA SRGs and STIGs) — a vendor overview chapter plus one feature, version, and requirement map chapter per product, each committed and pushed when done. Use when the user runs /srg-mapping-for <vendor> or asks for "SRG mapping for <vendor>".
argument-hint: <vendor name, for example "Juniper" or "Palo Alto Networks">
---

# /srg-mapping-for

Build the SRG and STIG mapping for one vendor, the way Volume CLXXII already
does it for Fortinet (Chapters 10–30) and Cisco (Chapters 31–32). Everything
happens inside this repo (`D:\Documents\claude\Enterprise-Infrastructure-Encyclopedia`):
read, write, and scratch only there.

Paths used below:

- `VOL` = `volumes/volume-172-disa-srgs-and-stigs`
- `SKILL` = `.claude/skills/srg-mapping-for`
- `LIB` = the newest dated folder under `imports/` that holds the DISA STIG
  library download (for example `imports/2026-10-06`). If none exists, or it is
  older than the current quarter, ask the user before downloading a new one.
- Scratch work goes in `temp/<vendor-slug>/` and `temp/<product-slug>/`
  (gitignored). Never write `.md` files under `temp/`.

The argument is the vendor name. If it is missing, ask for it.

## What the workflow produces

1. **A vendor overview chapter** (model: Chapter 10 for a vendor with few
   STIGs, Chapter 31 for a vendor with many). Title:
   `Chapter NN: <Vendor> Products — STIGs and SRG Mapping`. It inventories the
   vendor's STIGs in `LIB`, explains what they require and how to meet the main
   rules, and maps every product without a STIG to the SRGs that apply.
2. **One map chapter per product** (models: Chapters 11–30 and 32). Each maps
   every feature to the release that introduced it, the STIG rule or SRG
   requirement it relates to, and the verified command or setting that meets
   it, with a requirement reference table and documented product limitations.
   Products with a STIG are mapped to the STIG rules (file suffix
   `-feature-version-and-stig-map.md`, title "... Feature, Version, and STIG
   Map"); products without one are mapped to SRGs (suffix
   `-feature-version-and-srg-map.md`, title "... Feature, Version, and SRG Map").
3. **CSV downloads** before both tables of every map chapter, from
   `scripts/python/export_srg_tables.py`.
4. **An updated overview chapter and volume README** at the end, with a
   "What the product maps found" table (model: Chapter 10's section of that
   name).

## Steps

### 1. Inventory the vendor

- Find the vendor's STIG packages in `LIB` (match the vendor name and its
  common abbreviations, for example `FN_` for Fortinet or `PAN_` for Palo Alto
  Networks). Also search the library compilation ZIP's listing, as some content
  only appears there.
- Unzip them into `temp/<vendor-slug>/` (including nested ZIPs) and run
  `python SKILL/stigs.py temp/<vendor-slug>` to get each STIG's title,
  release, benchmark date, rule counts by severity, rule-ID prefixes, and every
  rule with its fix text (written to `temp/<vendor-slug>/stigs.json`).
- Read each package's overview PDF for its scope statement.
- List the vendor's products: the STIG-covered ones, plus the main products
  without a STIG (from the vendor's documentation site and the encyclopedia's
  own vendor volumes under `volumes/`).

### 2. Confirm scope with the user

Show the planned chapter list (overview chapter number, then one chapter per
product, with STIG or SRGs for each) and ask the user to confirm or trim it
before building. This is the one question the workflow asks up front.

### 3. Write the overview chapter

Write it yourself (not an agent), following the standard chapter template and
the model chapter. Every figure (releases, dates, rule counts, CAT I lists)
comes from `stigs.json`; every claim about scope comes from the overview PDFs.
Check summaries of rule content against the actual rule titles before
finishing; quote fix-text commands only after checking them, and say where
DISA's fix text will not parse as written. Register it (step 5) and commit it
before starting the product chapters.

### 4. Build the product chapters, one agent at a time

For each product, launch **one** background agent (`general-purpose`) and wait
for it to finish before starting the next. Never run product agents in
parallel. The agent prompt gives:

- the product, its chapter number, file name, title, and scratch folder;
- the STIG (with its unzipped path in `temp/<vendor-slug>/`) or the SRGs to
  use, the abbreviation for each, and the non-essential-capabilities rule or
  requirement to use for "no direct requirement" rows;
- the likely version and command sources;
- an instruction to follow `SKILL/PLAYBOOK.txt` exactly and to send its final
  report in the format the playbook defines.

If an agent stops on a usage limit, resume the same agent with `SendMessage`
once the limit resets, telling it where it stopped. Do not start a fresh agent
for the same product.

When an agent reports back:

1. Spot-check the chapter: the standard sections are present, sample rows are
   sensible, and for a STIG chapter every rule ID appears (count the distinct
   rule IDs in the chapter against `stigs.json`).
2. Re-run the agent's verifier yourself (`temp/<product-slug>/verify.py`) and
   confirm 0 failures.
3. Question anything odd in the report (for example a requirement ID format
   you have not seen, or a row with no requirement that plainly needs one), and
   check it against the source before accepting it.

### 5. Register, check, commit, push, watch

For each finished chapter:

1. Write a spec JSON in `temp/<vendor-slug>/specNN.json` and run
   `python SKILL/register.py temp/<vendor-slug>/specNN.json`. It updates
   `book.yml`, the root `README.md` and `PROJECT_STATUS.md` counts, the volume
   README chapter list and index count, `INDEX.md`, `GLOSSARY.md`, an optional
   row in the overview chapter, and `cspell.json`. The spec format is in the
   script's docstring.
2. Update the volume README's overview prose by hand so it describes the new
   chapter in context (the script only appends the chapter-list line).
3. Run `bash SKILL/check.sh <chapter-file>`. It regenerates the CSV downloads
   and runs markdownlint, cspell, the internal link check, and the `book.yml`
   check. Fix every failure.
4. Commit with a message in the style of the existing chapter commits (subject
   `Vol CLXXII Ch NN: <Product> feature, version, and STIG|SRG map`, a body
   giving counts, sources, and requirements, and the attribution line), push
   to `main` (retry on GitHub server errors), and watch the Pages build in the
   background until it succeeds. Do not push while an earlier Pages build is
   still running if that build carries something the user is waiting to see:
   the workflow cancels in-progress runs.

Invoking this workflow authorizes committing and pushing each finished chapter
to `main`, as the Fortinet and Cisco runs did. If the user says otherwise,
stop before committing and ask.

### 6. Finish

After the last product chapter:

- Add a "The product map chapters" and a "What the product maps found" section
  to the overview chapter (model: Chapter 10), summarizing each product's
  requirements, command source, and main gaps from the agents' reports, and the
  gaps that recur across the vendor's products. Check each claim against the
  map chapters before writing it.
- Update the volume README for the new chapters.
- Run the checks, then commit, push, and watch as above.
- Report to the user: chapters added, anything left out and why, and any
  follow-ups (for example fix text that no longer matches the vendor's CLI).
