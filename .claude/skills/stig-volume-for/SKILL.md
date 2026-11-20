---
name: stig-volume-for
description: Move one Fortinet product's STIG and SRG chapters out of Volume CLXXII (DISA SRGs and STIGs) into a volume of its own in the 200 to 299 block — its feature map chapter and the crosswalks built on it, with their CSV files — and leave pointer pages behind. Use when the user runs /stig-volume-for <product>, asks for a volume for a Fortinet product's STIG or SRG mapping, or asks to "do the same workflow" for another product.
argument-hint: <Fortinet product, for example "FortiGate" or "FortiClient and EMS">
---

# /stig-volume-for

Move one Fortinet product from Volume CLXXII to a volume of its own, the way
Volume CCI (FortiSwitch), Volume CCII (FortiAnalyzer), and Volume CCIII
(FortiManager) were made. Volume numbers 200 to 299 are reserved for this work
(`Structure.md`). Everything happens inside this repository.

Paths used below:

- `VOL172` = `volumes/volume-172-disa-srgs-and-stigs`
- `SKILL` = `.claude/skills/stig-volume-for`
- `MOVE` = `python SKILL/move_product.py`, run from the repository root

The argument is the product name as the chapter titles write it, for example
`FortiGate` or `"FortiClient and EMS"`. If it is missing, ask for it.

## What the workflow produces

1. **A new volume**, `volumes/volume-2NN-<product>-stig-and-srg-mapping`,
   titled "<Product> STIG and SRG Mapping". Chapter 01 is the product's map
   chapter. The crosswalk chapters that name the product follow as Chapters
   02, 03, and so on. Chapter 90 is the as-built record. The volume also has a
   README, an index, a glossary, and a `data/` folder with the CSV files.
2. **A pointer page** at each old chapter number of Volume CLXXII, so old
   links keep working.
3. **Updated records**: Volume CLXXII's README, index, and Chapter 90,
   `book.yml`, the root `README.md`, `PROJECT_STATUS.md`, `cspell.json`,
   `scripts/python/export_srg_tables.py`, and the "Other Fortinet STIG
   volumes" line in the README of every volume of the block.

## Rules

- **The script does the mechanical work.** Do not move, renumber, or register
  by hand what `move_product.py` does. If the script is wrong, fix the script.
- **Do not change a table row or a command.** In a moved chapter only chapter
  numbers, links, and the CSV download links change.
- **Do not download anything.** Every fact comes from the moved chapters, the
  repository history, and Volume CLXXII's Chapter 90.
- **Do not invent a count, a date, or a source.** If a fact is not in those
  places, leave it out.
- **Do not commit or push** as part of this workflow. Stop after the checks
  and report. See *Commit* below for what to do when the user asks.
- Write no `.md` files under `temp/` (the link checker scans it).

## Steps

### 1. Dry run

```bash
python .claude/skills/stig-volume-for/move_product.py "<product>"
```

The script prints the plan and changes nothing. Give the user a short summary
of it: the volume number and title, each chapter with its old and new number,
the number of data files, the chapter references that need a person, and the
files that will change. Ask for a go-ahead before step 2, unless the user has
already told you to run the move.

Look at these lines of the plan before you go on:

- **Chapters.** The default is the product's map chapter, then every
  crosswalk whose file name holds the product's name. If the user wants
  another set, pass `--chapters` with the Volume CLXXII chapter numbers, the
  map chapter first.
- **Volume number.** The default is one more than the highest volume of the
  block. Pass `--volume` for another number.
- **CSV export.** The line must say the scratch export has the same content
  as today's files. If it does not, run
  `python scripts/python/export_srg_tables.py` first and look at what it
  changes.
- **Data files left in Volume CLXXII.** A file such as a workbook, whose name
  starts with the chapter number but not with the chapter's file name, is not
  moved. Decide with the user where it belongs.

### 2. Apply

```bash
python .claude/skills/stig-volume-for/move_product.py "<product>" --apply
```

The script moves the chapters and data files with `git mv`, writes the
pointer pages, rewrites the references and links in the moved chapters,
updates the records listed above, runs the CSV export, and writes the new
volume's README, index, glossary, and Chapter 90. It works out every edit to
an existing file before it writes the first one, so a plan that cannot be
carried out stops with nothing changed.

### 3. Rewrite the references the script leaves

The script rewrites a reference to one chapter, and a reference to a group of
chapters that all stay or all move together. It leaves a group that mixes
them, such as "Chapters 33 to 37", and lists it under "Chapter references
that need a person". Read each sentence and name every volume, for example
"the other crosswalks (Volume CCI Chapters 02 and 03, and Volume CLXXII
Chapters 34 to 36)". Do not add a volume name without reading the sentence.

### 4. Write the prose the script marks

The new volume's files hold a comment that starts `TODO stig-volume-for`
wherever a person or Claude has to write: the README's summary, one bullet for
each chapter, and the software baseline; the glossary terms; and, in Chapter
90, the sources of each chapter, the design considerations, how the chapters
were built, the references, the knowledge checks, and the summary. Each
comment says what to write. Replace the comment with the text and leave none.

- Models: the README, glossary, and Chapter 90 of Volume CCII (two chapters)
  and Volume CCIII (one chapter).
- Sources: the moved chapters, their commit messages
  (`git log --follow -- <chapter file>`), and Volume CLXXII's Chapter 90.
- Read the generated text around each comment once. It comes from a template,
  and a product may need a sentence changed.
- Add index entries for topics that only this volume covers.

### 5. Do the steps the script lists as yours

"Steps the script cannot do" names an edit whose place the script did not
find, for example a row of a table in Volume CLXXII's Chapter 90. Make each
edit by hand, in the wording the earlier moves used.

### 6. Check

```bash
python .claude/skills/stig-volume-for/move_product.py "<product>" --check
```

```bash
bash scripts/bash/validate.sh
```

The check fails while a TODO comment remains, a chapter reference in a moved
chapter names no volume, a link of the new volume does not resolve, a CSV
link still uses the Volume CLXXII address, or the CSV export changes a file.
`validate.sh` then checks `book.yml`, every relative link in the book,
markdownlint, and CSpell. Fix every failure. Also confirm that the CSV row
counts in the script's output are the ones the chapters had before the move.

### 7. Keep the records current

- The new volume's Chapter 90 is its as-built record.
- Volume CLXXII's Chapter 90 describes this workflow under *Moving a product
  to a volume of its own*, with the list of products moved so far. Add the
  product to that list. When this skill or the script changes, update that
  section in the same commit.

### 8. Report

Tell the user what moved, what the checks showed, and what is not verified.
The site build rewrites links between chapters and volumes, and only the
Deploy Pages run after a push checks that. Say that nothing is committed.

## Commit

Commit and push only when the user asks. Use one commit for each volume, with
a subject in the style of the first move:

`Vol <ROMAN>: new <Product> STIG and SRG Mapping volume; move <Product> chapters from Vol CLXXII`

The body lists what moved and what was checked, and ends with the attribution
line. After a push, watch the Validate and Deploy Pages runs, then open the
new volume's page on the site and follow one link into Volume CLXXII and one
link back.

## How the script decides

- **Which chapters.** `NN-<product>-feature-version-and-srg-map.md` or
  `...-and-stig-map.md` is the map chapter. A crosswalk belongs to the product
  when its file name holds the product's name between hyphens.
- **Which chapters moved earlier.** A chapter of Volume CLXXII whose text says
  "This chapter moved to Volume" is a pointer page. The script reads the
  volume and the new chapter from it, so a reference to that chapter names
  the volume it moved to.
- **What a reference becomes.** A chapter that moves in this run keeps the
  word "Chapter" and takes its new number. A chapter that stays becomes
  "Volume CLXXII Chapter NN". A chapter that moved earlier becomes
  "Volume <ROMAN> Chapter NN". A reference that already names a volume is
  left alone.
- **What it does not touch.** Chapters that stay in Volume CLXXII keep their
  links to the old chapter numbers, which the pointer pages resolve. The
  scratch folders under `temp/` are local and untracked; the new Chapter 90
  names the ones whose scripts still hold the old paths.
