#!/usr/bin/env python3
"""Move one Fortinet product's STIG and SRG chapters from Volume CLXXII into a
volume of its own in the 200 to 299 block. Run from the repository root.

Usage:
  python .claude/skills/stig-volume-for/move_product.py <product>           dry run: print the plan, change nothing
  python .claude/skills/stig-volume-for/move_product.py <product> --apply   make the move
  python .claude/skills/stig-volume-for/move_product.py <product> --check   check a finished move

Options:
  --volume N         volume number (default: one more than the highest volume-2NN)
  --chapters A,B     chapter numbers of Volume CLXXII to move, the map chapter first
                     (default: the product's map chapter, then the crosswalks that name it)
  --date YYYY-MM-DD  the date of the move (default: today)

The dry run and --apply make the same plan. --apply then:

- moves the chapters and their data files with git mv and renumbers them from 01;
- leaves a pointer page at each old chapter number;
- rewrites the chapter references and links inside the moved chapters;
- updates Volume CLXXII's README, index, and Chapter 90;
- registers the volume in book.yml, the root README.md, PROJECT_STATUS.md,
  cspell.json, and scripts/python/export_srg_tables.py, and runs that script;
- writes the new volume's README, index, glossary, and Chapter 90, with a
  comment that starts "TODO stig-volume-for" wherever a person or Claude has
  to write prose.

It does not commit. --check fails while a TODO comment or a chapter reference
that was not rewritten remains. Every edit to an existing file is worked out
before the first file is written, so a plan that cannot be carried out stops
with nothing changed.
"""
import argparse
import contextlib
import datetime
import importlib.util
import io
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile

V172 = "volumes/volume-172-disa-srgs-and-stigs"
EXPORT = "scripts/python/export_srg_tables.py"
SKILL = ".claude/skills/stig-volume-for"
MARK = "TODO stig-volume-for"
AS_BUILT = "90-as-built-how-this-volume-was-built.md"
OTHERS = "- **Other Fortinet STIG volumes:**"
POINTER_RE = re.compile(
    r"This chapter moved to Volume ([A-Z]+),.*?\[Chapter (\d+): [^\]]*\]"
    r"\(\.\./\.\./(volume-\d+-[a-z0-9-]+)/chapters/([^)]+\.md)\)", re.S)
LINK_RE = re.compile(r"\[([^\]\n]*)\]\(([^)\s#]+)(#[^)\s]*)?\)")
REF_RE = re.compile(r"\b(Chapters?)(\s+)(\d+)((?:(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:to|and|or|through)\s+)\d+)*)")
WORDS = "zero one two three four five six seven eight nine ten eleven twelve".split()


def die(message):
    sys.exit("move_product.py: " + message)


def read(path):
    return io.open(path, encoding="utf-8", newline="").read()


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="").write(text)


def git(*args):
    done = subprocess.run(["git"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True, encoding="utf-8")
    if done.returncode:
        die("git %s failed: %s" % (" ".join(args), done.stderr.strip()))
    return done.stdout


def roman(number):
    out = ""
    for value, digits in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                          (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while number >= value:
            out += digits
            number -= value
    return out


def unroman(text):
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, digit in enumerate(text):
        value = values[digit]
        total += -value if i + 1 < len(text) and values[text[i + 1]] > value else value
    return total


def join_and(items):
    items = list(items)
    if len(items) < 3:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def number_range(numbers):
    """'01', '01 and 02', or '01 to 03' for a run of chapter numbers."""
    numbers = list(numbers)
    if len(numbers) > 2 and [int(n) for n in numbers] == list(range(int(numbers[0]), int(numbers[0]) + len(numbers))):
        return "%s to %s" % (numbers[0], numbers[-1])
    return join_and(numbers)


def sentence_case(title):
    """'FortiManager Feature, Version, and SRG Map' -> 'FortiManager feature, version, and SRG map'."""
    out = []
    for word in title.split(" "):
        core = word.strip(",.()")
        keep = core.isupper() or any(c.isupper() for c in core[1:]) or core in ("Cisco", "Catalyst", "Nexus")
        out.append(word if keep else word.lower())
    return " ".join(out)


class Rewriter:
    """Rewrites links and 'Chapter NN' references of Volume CLXXII for a file in the new volume."""

    def __init__(self, names, now, before, slug):
        self.names = dict((n.split("-", 1)[0], n) for n in names)   # number -> file name in Volume CLXXII
        self.now = now          # old number -> new file name (moved by this run)
        self.before = before    # old number -> (roman, slug, new number, new file), moved earlier
        self.slug = slug

    def where(self, number):
        """('prefix ', 'new number') for a chapter number of Volume CLXXII."""
        if number in self.now:
            return "", self.now[number].split("-", 1)[0]
        if number in self.before:
            return "Volume %s " % self.before[number][0], self.before[number][2]
        return "Volume CLXXII ", number

    def path(self, source):
        """The repository path a link target leads to after the move."""
        folder, name = posixpath.split(source)
        if folder == V172 + "/chapters":
            number = name.split("-", 1)[0]
            if self.names.get(number) == name:
                if number in self.now:
                    return "volumes/%s/chapters/%s" % (self.slug, self.now[number])
                if number in self.before:
                    return "volumes/%s/chapters/%s" % (self.before[number][1], self.before[number][3])
        return source

    def run(self, text, source_dir, target_dir):
        def link(match):
            label, target, anchor = match.group(1), match.group(2), match.group(3) or ""
            if "://" in target or target.startswith("mailto:"):
                return "\x00" + match.group(0) + "\x01"
            source = posixpath.normpath(posixpath.join(source_dir, target))
            folder, name = posixpath.split(source)
            number = name.split("-", 1)[0]
            if folder == V172 + "/chapters" and self.names.get(number) == name:
                prefix, new = self.where(number)
                label = re.sub(r"\bChapter %s\b" % number, "%sChapter %s" % (prefix, new), label)
            new_target = posixpath.relpath(self.path(source), target_dir)
            return "\x00[%s](%s%s)\x01" % (label, new_target, anchor)

        def reference(match, segment):
            if re.search(r"Volume\s+[A-Z]+\s+$", segment[max(0, match.start() - 40):match.start()]):
                return match.group(0)
            word, gap, first, rest = match.groups()
            numbers = [first] + re.findall(r"\d+", rest)
            if any(len(n) != 2 or n not in self.names for n in numbers):
                return match.group(0)
            if not rest:
                prefix, new = self.where(first)
                return prefix + word + gap + new
            if len(numbers) == 2 and re.search(r"\b(to|through)\b", rest):
                span = [n for n in sorted(self.names) if int(first) <= int(n) <= int(numbers[1])]
                places = [self.where(n) for n in span]
                run = [int(new) for _, new in places]
                if len(set(p for p, _ in places)) == 1 and run == list(range(run[0], run[0] + len(run))):
                    return places[0][0] + word + gap + places[0][1] + re.sub(r"\d+$", places[-1][1], rest)
                return match.group(0)
            places = [self.where(n) for n in numbers]
            if len(set(p for p, _ in places)) == 1:
                rest_numbers = iter(places[1:])
                return places[0][0] + word + gap + places[0][1] + re.sub(r"\d+", lambda _: next(rest_numbers)[1], rest)
            return match.group(0)

        parts = re.split(r"(\x00.*?\x01)", LINK_RE.sub(link, text), flags=re.S)
        for i in range(0, len(parts), 2):
            parts[i] = REF_RE.sub(lambda m, seg=parts[i]: reference(m, seg), parts[i])
        return "".join(parts).replace("\x00", "").replace("\x01", "")


def unrewritten(text, own):
    """(line, phrase) for each chapter reference that names no volume and is not one of this volume's chapters."""
    found = []
    for match in REF_RE.finditer(text):
        if re.search(r"Volume\s+[A-Z]+\s+$", text[max(0, match.start() - 40):match.start()]):
            continue
        numbers = [match.group(3)] + re.findall(r"\d+", match.group(4))
        if any(n not in own for n in numbers):
            found.append((text.count("\n", 0, match.start()) + 1, " ".join(match.group(0).split())))
    return found


def block_volumes():
    """[(number, slug, 'Volume CCI — FortiSwitch STIG and SRG Mapping')] for the volumes of the 200 to 299 block."""
    out = []
    for name in sorted(os.listdir("volumes")):
        readme = "volumes/%s/README.md" % name
        if re.match(r"volume-2\d\d-", name) and os.path.exists(readme):
            out.append((int(name[7:10]), name, read(readme).split("\n", 1)[0][2:].strip()))
    return out


def others_bullet(slug, volumes):
    links = ["[%s](../%s/README.md)" % (title, s) for _, s, title in sorted(volumes) if s != slug]
    return OTHERS + " " + ", ".join(links) + "." if links else ""


def set_others(text, bullet):
    """Put the 'other Fortinet STIG volumes' bullet into a volume README; None if it has no place for it."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith(OTHERS):
            lines[i] = bullet
            return "\n".join(lines)
    for i, line in enumerate(lines):
        if line.strip() == "## Related volumes":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            lines.insert(j, bullet)
            return "\n".join(lines)
    return None


def make_plan(args):
    product = args.product.strip()
    pslug = re.sub(r"[^a-z0-9]+", "-", product.lower()).strip("-")
    if not os.path.isdir(V172 + "/chapters") or not os.path.exists("book.yml"):
        die("run this from the repository root")
    names = sorted(n for n in os.listdir(V172 + "/chapters") if n.endswith(".md"))
    before = {}
    for name in names:
        hit = POINTER_RE.search(read(V172 + "/chapters/" + name))
        if hit:
            before[name.split("-", 1)[0]] = (hit.group(1), hit.group(3), hit.group(2), hit.group(4))
    existing = [d for d in os.listdir("volumes") if re.match(r"volume-2\d\d-%s-stig-and-srg-mapping$" % re.escape(pslug), d)]
    if args.check:
        if not existing:
            die("no volume-2NN-%s-stig-and-srg-mapping folder to check" % pslug)
        slug = existing[0]
        number = int(slug[7:10])
        chosen = sorted(n for n, place in before.items() if place[1] == slug)
        if not chosen:
            die("Volume CLXXII has no pointer page that leads to %s" % slug)
        moves = [(next(x for x in names if x.startswith(n + "-")), before[n][3]) for n in chosen]
        moves.sort(key=lambda pair: pair[1])
        before = dict((n, place) for n, place in before.items() if place[1] != slug)
    else:
        if existing:
            die("%s already has a volume: %s" % (product, existing[0]))
        if args.chapters:
            chosen = []
            for number in [c.strip().zfill(2) for c in args.chapters.split(",")]:
                hits = [n for n in names if n.startswith(number + "-")]
                if len(hits) != 1:
                    die("Volume CLXXII has no Chapter %s" % number)
                chosen.append(hits[0])
        else:
            maps = [n for n in names if re.match(r"\d+-%s-feature-version-and-s[a-z]+-map\.md$" % re.escape(pslug), n)]
            crosswalks = [n for n in names if n.endswith("-crosswalk.md")
                          and "-%s-" % pslug in "-%s-" % n.split("-", 1)[1][:-3]]
            chosen = maps + crosswalks
        if not chosen:
            die("Volume CLXXII has no chapter for %s (looked for <NN>-%s-feature-version-and-...-map.md)" % (product, pslug))
        for name in chosen:
            if name.split("-", 1)[0] in before:
                die("Chapter %s has already moved to Volume %s" % (name.split("-", 1)[0], before[name.split("-", 1)[0]][0]))
        moves = [(old, "%02d-%s" % (i, old.split("-", 1)[1])) for i, old in enumerate(chosen, 1)]
        block = sorted(int(d[7:10]) for d in os.listdir("volumes") if re.match(r"volume-2\d\d-", d))
        number = args.volume or (block[-1] + 1 if block else 201)
        if not 200 <= number <= 299:
            die("volume %d is outside the 200 to 299 block" % number)
        if any(d.startswith("volume-%d-" % number) for d in os.listdir("volumes")):
            die("volume %d is taken" % number)
        slug = "volume-%d-%s-stig-and-srg-mapping" % (number, pslug)
    data_names = sorted(os.listdir(V172 + "/data")) if os.path.isdir(V172 + "/data") else []
    data = []
    for old, new in moves:
        for name in data_names:
            if name.startswith(old[:-3] + "-"):
                data.append((name, new[:-3] + name[len(old) - 3:]))
    stray = [n for n in data_names if any(n.startswith(old.split("-", 1)[0] + "-") for old, _ in moves)
             and n not in [d[0] for d in data]]
    plan = argparse.Namespace(
        product=product, pslug=pslug, number=number, roman=roman(number), slug=slug,
        title="%s STIG and SRG Mapping" % product, folder="volumes/" + slug, moves=moves, data=data, stray=stray,
        names=names, before=before, date=args.date or datetime.date.today().isoformat())
    plan.now = dict((old.split("-", 1)[0], new) for old, new in moves)
    plan.own = set(new.split("-", 1)[0] for _, new in moves) | {"90"}
    plan.rewriter = Rewriter(names, plan.now, before, slug)
    return plan


def chapter_title(text):
    """'FortiManager Feature, Version, and SRG Map' from '# Chapter 13: FortiManager Feature, ...'."""
    hit = re.match(r"# Chapter \d+: (.+)", text)
    if not hit:
        die("a chapter does not start with '# Chapter NN: Title'")
    return hit.group(1).strip()


def history(path):
    """[(date, subject)] for a file, oldest first."""
    lines = git("log", "--follow", "--date=short", "--format=%ad|%s", "--", path).strip().split("\n")
    return [tuple(line.split("|", 1)) for line in reversed(lines) if "|" in line]


def csv_tables(text):
    """[(heading, rows, file name)] for the CSV download links of a chapter."""
    out, heading = [], ""
    for line in text.split("\n"):
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        hit = re.match(r"\[Download [^\]]+ as CSV\]\([^)]*/([^/)]+\.csv)\) \((\d+) rows\)", line)
        if hit:
            out.append((heading, int(hit.group(2)), hit.group(1)))
    return out


def edits_for_existing_files(plan):
    """({path: new text}, [manual steps]) for the files outside the new volume. Dies on an edit that must work."""
    pending, manual = {}, []
    volume_link = "[Volume %s](../%s/README.md)" % (plan.roman, plan.slug)

    # Volume CLXXII README: the chapter list, and a sentence in the overview.
    text = read(V172 + "/README.md")
    plan.descriptions = {}
    for old, new in plan.moves:
        old_number, new_number = old.split("-", 1)[0], new.split("-", 1)[0]
        hit = re.search(r"(?m)^(%d\. \[[^\]]+\]\(chapters/%s\)) — (.*)$" % (int(old_number), re.escape(old)), text)
        if not hit:
            die("Volume CLXXII's README has no chapter list line for Chapter %s" % old_number)
        plan.descriptions[new] = hit.group(2)
        text = text[:hit.start()] + "%s — moved to Volume %s, [Chapter %s](../%s/chapters/%s)." % (
            hit.group(1), plan.roman, new_number, plan.slug, new) + text[hit.end():]
        lines = text.split("\n")
        is_map = old.endswith("-map.md")
        start = next((i for i, line in enumerate(lines)
                      if (line.startswith("- **Chapters 11 to 30**") if is_map
                          else line.startswith("- **Chapter %s** " % old_number))), None)
        if start is None:
            manual.append("Volume CLXXII README, Overview: say that Chapter %s moved to Volume %s." % (old_number, plan.roman))
        else:
            end = start
            while end + 1 < len(lines) and lines[end + 1].startswith("  "):
                end += 1
            lines[end] += (" The %s map (Chapter %s) moved to %s, where it is Chapter %s." % (
                plan.product, old_number, volume_link, new_number) if is_map
                else " It moved to %s, where it is Chapter %s." % (volume_link, new_number))
            text = "\n".join(lines)
    pending[V172 + "/README.md"] = text

    # Volume CLXXII index.
    text = read(V172 + "/INDEX.md")
    plan.index_lines = [line for line in text.split("\n") if any("](chapters/%s)" % old in line for old, _ in plan.moves)]
    for old, new in plan.moves:
        text = text.replace("[Chapter %s](chapters/%s)" % (old.split("-", 1)[0], old),
                            "[Volume %s Chapter %s](../%s/chapters/%s)" % (plan.roman, new.split("-", 1)[0], plan.slug, new))
    pending[V172 + "/INDEX.md"] = text

    # Volume CLXXII Chapter 90: a paragraph and a note in the table of how each part was built.
    path = V172 + "/chapters/" + AS_BUILT
    text = read(path)
    link90 = "[Volume %s](../../%s/README.md)" % (plan.roman, plan.slug)
    olds, news = [o.split("-", 1)[0] for o, _ in plan.moves], [n.split("-", 1)[0] for _, n in plan.moves]
    one = len(olds) == 1
    paragraph = ("The %s chapter%s (%s) moved on %s to\n%s, where %s; the pointer page%s\nat %s remain%s here, and %s build "
                 "record is in that volume's\nChapter 90.") % (
        plan.product, "" if one else "s", join_and(olds), plan.date, link90,
        "it is Chapter 01" if one else "they are Chapters " + number_range(news), "" if one else "s",
        "its old number" if one else "their old numbers", "s" if one else "", "its" if one else "their")
    paragraphs = text.split("\n\n")
    spots = [i for i, p in enumerate(paragraphs) if p.startswith("The ") and " moved on " in p and "[Volume " in p]
    if spots:
        paragraphs.insert(spots[-1] + 1, paragraph)
        text = "\n\n".join(paragraphs)
    else:
        manual.append("Volume CLXXII Chapter 90: add a paragraph that says the %s chapters moved." % plan.product)
    for old, new in plan.moves:
        row_start = "| [11 to 30](" if old.endswith("-map.md") else "| [33 to 38]("
        lines = text.split("\n")
        row = next((i for i, line in enumerate(lines) if line.startswith(row_start) and line.endswith(" |")), None)
        if row is None:
            manual.append("Volume CLXXII Chapter 90: note the move of Chapter %s in the table of how each part was built."
                          % old.split("-", 1)[0])
        else:
            lines[row] = lines[row][:-2] + ". Chapter %s moved to %s as Chapter %s on %s |" % (
                old.split("-", 1)[0], link90, new.split("-", 1)[0], plan.date)
            text = "\n".join(lines)
    pending[path] = text

    # book.yml.
    chapters = [(new.split("-", 1)[0], "Chapter %s: %s" % (new.split("-", 1)[0], plan.titles[new]),
                 "%s/chapters/%s" % (plan.folder, new)) for _, new in plan.moves]
    chapters.append(("90", "Chapter 90: As-Built — How This Volume Was Built", "%s/chapters/%s" % (plan.folder, AS_BUILT)))
    if any('"' in title for _, title, _ in chapters):
        die("a chapter title holds a double quote, which book.yml cannot take as written")
    block = ["  - id: volume-%d" % plan.number, '    number: "%s"' % plan.roman, "    slug: " + plan.slug,
             '    title: "%s"' % plan.title, "    chapter_count: %d" % len(chapters), "    build_eligible: true",
             "    chapters:"]
    for number, title, path in chapters:
        block += ["      - id: " + number, '        title: "%s"' % title, "        path: " + path]
    lines = read("book.yml").split("\n")
    spot = next((i for i, line in enumerate(lines)
                 if re.match(r"  - id: volume-(\d+)$", line) and int(line.rsplit("-", 1)[1]) > plan.number), None)
    if spot is None:
        die("book.yml has no volume after %d to insert before" % plan.number)
    pending["book.yml"] = "\n".join(lines[:spot] + block + lines[spot:])

    # Root README.md and PROJECT_STATUS.md.
    text = read("README.md")
    hit = re.search(r"(\d+) volumes, (\d+) chapters\. Each volume has a dedicated", text)
    if not hit:
        die("README.md has no 'N volumes, N chapters' line")
    text = text[:hit.start()] + "%d volumes, %d chapters. Each volume has a dedicated" % (
        int(hit.group(1)) + 1, int(hit.group(2)) + len(chapters)) + text[hit.end():]
    lines = text.split("\n")
    spot = next((i for i, line in enumerate(lines)
                 if re.match(r"\| [A-Z]+ \| \[[^\]]+\]\(volumes/volume-(\d+)-[^)]*\) \| \d+ \|$", line)
                 and int(re.search(r"volumes/volume-(\d+)-", line).group(1)) > plan.number), None)
    if spot is None:
        die("README.md has no volume row after %d to insert before" % plan.number)
    lines.insert(spot, "| %s | [%s](%s/README.md) | %d |" % (plan.roman, plan.title, plan.folder, len(chapters)))
    pending["README.md"] = "\n".join(lines)

    text = read("PROJECT_STATUS.md")
    hit = re.search(r"\*\*Total declared chapters:\*\* (\d+) of (\d+) drafted", text)
    if not hit:
        die("PROJECT_STATUS.md has no 'Total declared chapters' line")
    text = text[:hit.start()] + "**Total declared chapters:** %d of %d drafted" % (
        int(hit.group(1)) + len(chapters), int(hit.group(2)) + len(chapters)) + text[hit.end():]
    lines = text.split("\n")
    spot = next((i for i, line in enumerate(lines)
                 if re.match(r"\| ([IVXLCDM]+) — .* \| \d+ \| Drafted \|$", line)
                 and unroman(line.split(" ")[1]) > plan.number), None)
    if spot is None:
        die("PROJECT_STATUS.md has no volume row after %d to insert before" % plan.number)
    lines.insert(spot, "| %s — %s | %d | Drafted |" % (plan.roman, plan.title, len(chapters)))
    pending["PROJECT_STATUS.md"] = "\n".join(lines)

    # cspell.json: the Roman numeral.
    text = read("cspell.json")
    if '"%s"' % plan.roman not in text:
        # The list is alphabetical apart from a few words at its head, so the word goes
        # between the two neighbors that share the most leading letters with it.
        lines = text.split("\n")
        start = next(i for i, line in enumerate(lines) if '"words": [' in line)
        word, best = plan.roman.lower(), None
        for i in range(start + 2, len(lines)):
            before = re.match(r'\s+"([^"]+)",?$', lines[i - 1])
            after = re.match(r'\s+"([^"]+)",?$', lines[i])
            if not before or not after:
                break
            if before.group(1).lower() <= word < after.group(1).lower():
                shared = max(len(os.path.commonprefix([word, w.group(1).lower()])) for w in (before, after))
                if best is None or shared > best[0]:
                    best = (shared, i)
        if best is None:
            die("cspell.json has no place for the word %s" % plan.roman)
        lines.insert(best[1], '    "%s",' % plan.roman)
        pending["cspell.json"] = "\n".join(lines)

    # The CSV export script.
    text = read(EXPORT)
    if '"%s"' % plan.slug not in text:
        hit = re.search(r'VOLUMES = \[\n((?:    "[^"]+",\n)+)\]', text)
        if not hit:
            die("%s has no VOLUMES list in the expected form" % EXPORT)
        pending[EXPORT] = text[:hit.end(1)] + '    "%s",\n' % plan.slug + text[hit.end(1):]

    # The other volumes of the block name the new one.
    plan.volumes = block_volumes() + [(plan.number, plan.slug, "Volume %s — %s" % (plan.roman, plan.title))]
    for _, slug, _ in plan.volumes:
        if slug == plan.slug:
            continue
        new_text = set_others(read("volumes/%s/README.md" % slug), others_bullet(slug, plan.volumes))
        if new_text is None:
            manual.append("volumes/%s/README.md: name Volume %s under Related volumes." % (slug, plan.roman))
        else:
            pending["volumes/%s/README.md" % slug] = new_text
    return pending, manual


def scratch_folders(plan):
    """Local, untracked scratch folders under temp/ whose scripts name the old chapter files."""
    found = set()
    if os.path.isdir("temp"):
        for folder in sorted(os.listdir("temp")):
            path = os.path.join("temp", folder)
            if not os.path.isdir(path):
                continue
            for name in os.listdir(path):
                if name.endswith(".py"):
                    try:
                        body = io.open(os.path.join(path, name), encoding="utf-8", errors="replace").read()
                    except OSError:
                        continue
                    if any(old in body for old, _ in plan.moves):
                        found.add("`temp/%s/`" % folder)
    return sorted(found)


def new_volume_files(plan):
    """{path: text} for the README, index, glossary, and Chapter 90 of the new volume."""
    todo = lambda words: "<!-- %s: %s -->" % (MARK, words)   # noqa: E731
    olds = [o.split("-", 1)[0] for o, _ in plan.moves]
    news = [n.split("-", 1)[0] for _, n in plan.moves]
    one = len(news) == 1
    content = ("Chapter " if one else "Chapters ") + number_range(news)
    count = WORDS[len(news) + 1]
    tables = dict((new, csv_tables(read("%s/chapters/%s" % (plan.folder, new)))) for _, new in plan.moves)
    v172 = "../volume-172-disa-srgs-and-stigs"
    build = dict((new, history("%s/chapters/%s" % (V172, old))) for old, new in plan.moves)
    scratch = scratch_folders(plan)

    readme = ["# Volume %s — %s" % (plan.roman, plan.title), "",
              todo("replace this comment with the volume's summary as a block quote, three to six lines that each "
                   "start with '> ': what the product is, which STIG or SRGs it is assessed against, and what the "
                   "chapters give for each feature. Model: the README of Volume CCII."), "",
              "## Overview", "",
              "Volume %s is the **%s volume of the Fortinet STIG work**. Volume" % (plan.roman, plan.product),
              "numbers 200 to 299 are reserved for that work (see",
              "[Structure.md](../../Structure.md)). The vendor-neutral material this volume",
              "builds on, the framework, the SRG catalog, the Fortinet overview, and the",
              "Cisco overview, stays in [Volume CLXXII — DISA SRGs and STIGs](%s/README.md)." % v172,
              ("The content chapter here was Chapter %s of that volume and" % olds[0]) if one
              else ("The %s content chapters here were Chapters %s of that volume and" % (WORDS[len(news)], join_and(olds))),
              "moved on %s. Volume CLXXII keeps a short pointer page at %s old" % (plan.date, "the" if one else "each"),
              "chapter number, so earlier links still work.", "",
              "The volume has %s chapters:" % count, ""]
    for _, new in plan.moves:
        readme += ["- **Chapter %s** is the **%s**:" % (new.split("-", 1)[0], sentence_case(plan.titles[new])),
                   "  " + todo("say in two to five lines what the chapter holds, with its counts.")]
    readme += ["- **Chapter 90**, the as-built chapter, records how %s %s built, when, and" % (content, "was" if one else "were"),
               "  from which sources, what changed after the first build, and the move from",
               "  Volume CLXXII.", "",
               "## CSV downloads", "",
               "Each table in %s has a CSV copy in this volume's `data/` folder and a" % content,
               "download link on the line above the table. `%s`" % EXPORT,
               "writes the files from the chapter tables, so a file always has the same rows",
               "as its table.", "",
               "| Chapter | Table | Rows | File in `data/` |", "| --- | --- | ---: | --- |"]
    for _, new in plan.moves:
        readme += ["| %s | %s | %d | `%s` |" % (new.split("-", 1)[0], heading, rows, name) for heading, rows, name in tables[new]]
    readme += ["", "The files moved with the chapter%s, so the download addresses changed. The" % ("" if one else "s"),
               "addresses under `data/volume-172-disa-srgs-and-stigs/` that began with %s" % join_and("`%s-`" % o for o in olds),
               "no longer exist.", "", "## Chapters", ""]
    for _, new in plan.moves:
        description = plan.rewriter.run(plan.descriptions[new], V172, plan.folder)
        readme.append("%d. [%s](chapters/%s) — %s" % (int(new.split("-", 1)[0]), plan.titles[new], new, description))
    readme += ["90. [As-Built — How This Volume Was Built](chapters/%s) — how and when %s %s built, from which sources, "
               "and what changed after the first build, including the move from Volume CLXXII."
               % (AS_BUILT, content, "was" if one else "were"), "",
               "## Volume resources", "",
               "- [Index](INDEX.md) — alphabetized topical index across all %s chapters." % count,
               "- [Glossary](GLOSSARY.md) — definitions for terms used in this volume.", "",
               "## Related volumes", ""]
    if others_bullet(plan.slug, plan.volumes):
        readme.append(others_bullet(plan.slug, plan.volumes))
    readme += ["- [Volume CLXXII — DISA SRGs and STIGs](%s/README.md)" % v172,
               "  for the framework (Chapters 01 to 09), the Fortinet overview (Chapter 10), the",
               "  product maps and crosswalks that have not moved, and the Cisco chapters.",
               "- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md).", "",
               "## Lab coverage", "",
               "This volume has **no hands-on labs**, by design. It is a reference. Each",
               "chapter keeps its implementation examples (commands and configuration",
               "snippets) and its knowledge checks, but omits the Hands-On Lab and Lab",
               "Verification sections of the standard chapter template.", "",
               "## Software and platform baseline", "",
               "DISA content is the quarterly release recorded in",
               "[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md).",
               todo("name the SRGs or STIGs and their releases, the documents the version data comes from, and the "
                    "command reference the commands were checked against, from the References section of each chapter."),
               "Confirm the current release of any STIG or SRG on the DoD Cyber Exchange",
               "before assessing against it.", "",
               "## Building and validating this volume", "",
               "From the repository root, after completing [SETUP.md](../../SETUP.md):", "",
               "```bash", "scripts/bash/validate.sh", "```", "",
               "```bash", "scripts/bash/build-book.sh --format all --volume %s" % plan.slug, "```", "",
               "After changing a table in %s, regenerate the CSV downloads" % content,
               "(written to this volume's `data/` folder) and refresh the download links:", "",
               "```bash", "python %s" % EXPORT, "```", "",
               "See the root [README.md](../../README.md#validation) for the complete",
               "validation and multi-format build reference.", ""]

    index = [plan.rewriter.run(line, V172, plan.folder) for line in plan.index_lines]
    index += ["- **CSV downloads of the chapter tables** — [Chapter 90](chapters/%s)" % AS_BUILT,
              "- **Move of the %s chapter%s from Volume CLXXII** — [Chapter 90](chapters/%s)"
              % (plan.product, "" if one else "s", AS_BUILT)]
    index = ["# Volume %s Index" % plan.roman, "",
             "Alphabetized topical index for **Volume %s — %s**." % (plan.roman, plan.title),
             "See also the [volume glossary](GLOSSARY.md) for term definitions and the",
             "[master index](../../INDEX.md) for cross-volume topics.", ""] + sorted(set(index), key=str.lower) + [""]

    terms = [line for line in read(V172 + "/GLOSSARY.md").split("\n")
             if line.startswith("- **") and plan.product.lower() in line.split("**")[1].lower()]
    glossary = ["# Volume %s Glossary" % plan.roman, "",
                "Definitions for terms used in **Volume %s — %s**." % (plan.roman, plan.title),
                "See the [master glossary](../../GLOSSARY.md) for cross-volume terms and the",
                "[Volume CLXXII glossary](%s/GLOSSARY.md) for" % v172,
                "the SRG and STIG terms this volume builds on.", ""] + terms + [
        todo("add the terms the chapters use, one line each in the form '- **Term** — definition.', in alphabetical "
             "order with the lines above, then delete this comment. Model: the glossary of Volume CCII."), ""]

    link172 = "../../volume-172-disa-srgs-and-stigs"
    chapter90 = [
        "# Chapter 90: As-Built — How This Volume Was Built", "", "## Learning Objectives", "",
        "- Trace how %s %s built, when, and from which sources." % (content, "was" if one else "were"),
        "- Explain why the %s chapter%s moved here from Volume CLXXII, and what" % (plan.product, "" if one else "s"),
        "  Volume CLXXII keeps.",
        "- Say what changed in the chapter%s after the first build." % ("" if one else "s"),
        "- Regenerate the CSV downloads and check their row counts.",
        "- Name what the move changed, and what it left where it was.", "",
        "## Theory and Architecture", "",
        "This is the volume's **as-built chapter**. Like an as-built drawing, it",
        "records how the volume was actually made rather than how it was planned: which",
        "parts were generated by a repeatable workflow, which sources each part rests",
        "on, and which changes came later. It is numbered 90 so that it stays last if",
        "chapters are added, and so that as-built chapters have the same number in every",
        "volume that has one.", "",
        "The content chapter%s not written here. %s built inside" % (" was" if one else "s were", "It was" if one else "They were"),
        "[Volume CLXXII — DISA SRGs and STIGs](%s/README.md)" % link172,
        "as Chapter%s %s, by the `/srg-mapping-for` workflow that" % ("" if one else "s", join_and(olds)),
        "[Volume CLXXII's own as-built chapter](%s/chapters/%s)" % (link172, AS_BUILT),
        "describes step by step. On %s %s moved here, together with %s CSV" % (
            plan.date, "it" if one else "they", "its" if one else "their"),
        "files, because volume numbers 200 to 299 are reserved for Fortinet STIG work",
        "(see [Structure.md](../../../Structure.md)). This chapter records only what is",
        "specific to the %s material. For the workflow itself (inventory," % plan.product,
        "agents, playbooks, registration), read the Volume CLXXII chapter.", "",
        "### How each part of the volume was built", "",
        "| Part | Built | How | Later changes |", "| --- | --- | --- | --- |"]
    for old, new in plan.moves:
        later = "; ".join("%s (%s)" % (re.sub(r"^Vol CLXXII( Ch \d+)?: ", "", subject), date)
                          for date, subject in build[new][1:]) or "None"
        chapter90.append("| [Chapter %s](%s), %s | %s | One agent, as Chapter %s of Volume CLXXII %s | %s |" % (
            new.split("-", 1)[0], new, sentence_case(plan.titles[new]), build[new][0][0] if build[new] else plan.date,
            old.split("-", 1)[0], todo("add the sources and the method in one or two sentences."), later))
    chapter90 += [
        "| CSV files | With the chapter%s | Generated from the chapter tables by `%s` | Regenerate whenever a table changes |"
        % ("" if one else "s", EXPORT),
        "| Move to Volume %s | %s | Chapter%s and `data/` files moved with `git mv` by the `/stig-volume-for` workflow; "
        "cross-references rewritten; pointer page%s left at Chapter%s %s of Volume CLXXII | None |"
        % (plan.roman, plan.date, "" if one else "s", "" if one else "s", "" if one else "s", join_and(olds)),
        "| 90, this chapter | %s | Started by the `/stig-volume-for` workflow, then completed from Volume CLXXII's "
        "Chapter 90, the chapter%s, and the repository history | Updated whenever the volume changes |"
        % (plan.date, "" if one else "s"), "",
        "Each chapter commit names its chapter in the subject (`Vol CLXXII Ch NN: ...`),",
        "so `git log --follow` on a chapter file in this volume shows its full history,",
        "including the time before the move.", "",
        "### What Volume CLXXII keeps", "",
        "Volume CLXXII keeps the vendor-neutral framework (Chapters 01 to 09), the",
        "Fortinet overview (Chapter 10), the Cisco overview and Catalyst map (Chapters",
        "31 and 32), and the Fortinet product maps and crosswalks that have not moved",
        "to a volume of their own. At the old number%s of the moved chapter%s (%s)" % ("" if one else "s", "" if one else "s", join_and(olds)),
        "it keeps %s that link%s here, so links from other" % ("a one-page pointer" if one else "one-page pointers", "s" if one else ""),
        "chapters, indexes, and outside pages still resolve. Chapters in this volume",
        "link back to Volume CLXXII by relative path and say \"Volume CLXXII\" in the",
        "text, because their own numbers overlap with that volume's.", "",
        "## Design Considerations", "",
        todo("write four to seven bullets on the design choices of the chapter%s, each with a bold lead: the version "
             "source, the SRGs or STIGs that apply, how the commands were checked, what the product does not meet "
             "exactly, and, for a crosswalk, how the rows are matched. Take every fact from the chapter%s. Model: "
             "Chapter 90 of Volume CCII." % ("" if one else "s", "" if one else "s")), "",
        "## Implementation and Automation", "",
        "### How the chapter%s built" % (" was" if one else "s were"), "",
        todo("describe the method of each chapter in a short numbered list, and name each later pass, such as the "
             "prerequisites pass, with its date and what it changed. Take the dates from the table above and the facts "
             "from the commit messages (git log --follow on each chapter)."), "",
        "### The CSV files", "", "One script writes the downloads:", "",
        "```bash", "python %s" % EXPORT, "```", "",
        "It finds each table in %s by its heading, writes it to" % content,
        "`data/<chapter>-<suffix>.csv`, and inserts or refreshes the download link on",
        "the line before the table. The CSV files use UTF-8 with a byte-order mark, so",
        "spreadsheet programs show dashes and quotes correctly.",
        "`scripts/bash/build-download-site.sh` copies them to the portal at",
        "`data/%s/`." % plan.slug, "", "| File | Rows |", "| --- | ---: |"]
    for _, new in plan.moves:
        chapter90 += ["| `%s` | %d |" % (name, rows) for _, rows, name in tables[new]]
    chapter90 += [
        "", "### The move from Volume CLXXII", "",
        "The `/stig-volume-for` workflow made the move on %s. Its script is" % plan.date,
        "`%s/move_product.py`, and" % SKILL,
        "[Volume CLXXII's Chapter 90](%s/chapters/%s)" % (link172, AS_BUILT),
        "describes it. The move changed these things:", "",
        "- Chapter%s %s of Volume CLXXII became Chapter%s %s here, with %s `data/`" % (
            "" if one else "s", join_and(olds), "" if one else "s", number_range(news), "its" if one else "their"),
        "  files renamed to match.",
        "- Cross-references inside the chapter%s were rewritten. A reference to a moved" % ("" if one else "s"),
        "  chapter uses its new number. A reference to a chapter that stays in Volume",
        "  CLXXII names the volume and links across by relative path. A reference to a",
        "  chapter that moved to another volume earlier names that volume.",
        "- `%s` covers this volume." % EXPORT,
        "- Volume CLXXII's README and index point to the new location%s, and its" % ("" if one else "s"),
        "  Chapter 90 records the move.",
        "- The portal URLs of the moved CSV files changed from",
        "  `data/volume-172-disa-srgs-and-stigs/` to",
        "  `data/%s/`, with new file names." % plan.slug, ""]
    if scratch:
        chapter90 += [
            "The move left one thing where it was. The scratch folder%s that built the" % ("" if len(scratch) == 1 else "s"),
            "chapter%s (%s)" % ("" if one else "s", join_and(scratch)),
            "%s not tracked, and %s scripts still name the Volume CLXXII paths. Change" % (
                "is" if len(scratch) == 1 else "are", "its" if len(scratch) == 1 else "their"),
            "those paths before you run one of them again, or it reads a pointer page or",
            "writes over one.", ""]
    counts = []
    for _, new in plan.moves:
        counts.append("Chapter %s has %s." % (new.split("-", 1)[0], join_and(
            "%d rows in *%s*" % (rows, heading) for heading, rows, _ in tables[new])))
    chapter90 += [
        "## Validation and Troubleshooting", "", "To check this volume:", "",
        "- **Row counts.** %s The CSV files must match: run" % " ".join(counts),
        "  `python %s` and confirm a clean `git status`" % EXPORT,
        "  afterward.",
        "- **The move.** `python %s/move_product.py \"%s\" --check`" % (SKILL, plan.product),
        "  looks for chapter references that were not rewritten, links of this volume",
        "  that do not resolve, and an export that changes a file.",
        "- **Repository checks.** `scripts/bash/validate.sh` checks `book.yml`, internal",
        "  links, markdownlint, and cspell.", "", "Common problems:", "",
        "| Symptom | Cause | Fix |", "| --- | --- | --- |",
        "| A link to a CSV file returns 404 on the portal | The link uses the Volume CLXXII path or an old file name | "
        "Run `export_srg_tables.py` to refresh the link |",
        "| A reader lands on a short page at Chapter%s %s of Volume CLXXII | They followed an old link | "
        "The page links to the new chapter; nothing to fix |" % ("" if one else "s", join_and(olds) if one else " or ".join(olds))]
    if scratch:
        chapter90.append("| A scratch script writes a full chapter into Volume CLXXII | The script still names the old "
                         "path | Restore the pointer page with `git checkout`, then change the path in the script |")
    chapter90 += [
        "", "## Security and Best Practices", "",
        "- **Treat the map as a starting point, not a ruling.** Confirm each mapping",
        "  with your assessor, especially where a requirement is organization-defined.",
        "- **Confirm SRG and STIG releases with DISA.** Download the current files from",
        "  DoD Cyber Exchange before citing an ID in an authorization package.",
        "- **Confirm prerequisites for your exact model and release.** Licenses and",
        "  hardware support differ by model and release.",
        "- **Do not commit the downloaded documents.** The scratch folders under",
        "  `temp/` hold vendor documents and are not tracked.",
        "- **Keep this chapter current.** When a chapter, a table, or the export script",
        "  changes, update this chapter in the same commit.", "",
        "## References and Knowledge Checks", "", "**References:**", "",
        "- [Volume CLXXII, Chapter 90](%s/chapters/%s)" % (link172, AS_BUILT),
        "  for the `/srg-mapping-for` workflow that built the chapter%s and the" % ("" if one else "s"),
        "  `/stig-volume-for` workflow that moved %s." % ("it" if one else "them"),
        "- `%s` and `%s/` in this repository." % (EXPORT, SKILL),
        "- " + todo("list the vendor and DISA documents the chapters cite, from their References sections."),
        "- DISA STIG and SRG library, DoD Cyber Exchange (`public.cyber.mil/stigs`).",
        "- The repository's commit history (`git log --follow` on each chapter file).", "",
        "**Knowledge checks:**", "",
        "1. Which chapter%s of Volume CLXXII did %s come from, and what does" % ("" if one else "s", content),
        "   Volume CLXXII keep at %s?" % ("that number" if one else "those numbers"),
        "2. What does the export script write, and how do you check its output?",
        "3. " + todo("add two to four checks on the design of the chapters, then renumber the list."), "",
        "## Summary and Completion Checklist", "",
        "%s %s built inside Volume CLXXII by the `/srg-mapping-for` workflow and" % (content, "was" if one else "were"),
        "moved here on %s with %s CSV files." % (plan.date, WORDS[sum(len(t) for t in tables.values())] if sum(
            len(t) for t in tables.values()) < len(WORDS) else str(sum(len(t) for t in tables.values()))),
        todo("add two or three sentences on what the chapters map, with their counts."),
        "Volume CLXXII keeps a pointer page at Chapter%s %s." % ("" if one else "s", join_and(olds)), "",
        "- [ ] Can say how each part of the volume was built, and when.",
        "- [ ] Can explain why the chapter%s moved and what Volume CLXXII keeps." % ("" if one else "s"),
        "- [ ] Can run the export script and check the row counts.",
        "- [ ] Knows that SRG and STIG releases need confirmation with DISA.", ""]
    return {plan.folder + "/README.md": "\n".join(readme), plan.folder + "/INDEX.md": "\n".join(index),
            plan.folder + "/GLOSSARY.md": "\n".join(glossary),
            "%s/chapters/%s" % (plan.folder, AS_BUILT): "\n".join(chapter90)}


def pointer_page(plan, old, new, title):
    old_number, new_number = old.split("-", 1)[0], new.split("-", 1)[0]
    return "\n".join([
        "# Chapter %s: %s" % (old_number, title), "",
        "This chapter moved to Volume %s, %s, where it" % (plan.roman, plan.title),
        "is now [Chapter %s: %s](../../%s/chapters/%s)." % (new_number, title, plan.slug, new),
        "This page stays so that links to Chapter %s keep working." % old_number, "",
        "See the [Volume %s README](../../%s/README.md)" % (plan.roman, plan.slug),
        "for the rest of the %s material: the other chapters of that volume, the" % plan.product,
        "CSV downloads of the tables, and the record of how the chapters were built.", ""])


def export_matches(plan):
    """Run the CSV export on a scratch copy of the chapters under their new names; True if the files are unchanged."""
    scratch = tempfile.mkdtemp(prefix="stig-volume-for-")
    here = os.getcwd()
    try:
        for old, new in plan.moves:
            target = os.path.join(scratch, "volumes", plan.slug, "chapters", new)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(os.path.join(V172, "chapters", old), target)
        spec = importlib.util.spec_from_file_location("export_srg_tables", os.path.join(here, EXPORT))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.VOLUMES = [plan.slug]
        os.chdir(scratch)
        with contextlib.redirect_stdout(io.StringIO()):
            module.main()
        os.chdir(here)
        same = True
        for old_name, new_name in plan.data:
            made = os.path.join(scratch, "volumes", plan.slug, "data", new_name)
            if new_name.endswith(".csv") and not (os.path.exists(made) and io.open(made, "rb").read()
                                                  == io.open(os.path.join(V172, "data", old_name), "rb").read()):
                same = False
        return same
    finally:
        os.chdir(here)
        shutil.rmtree(scratch, ignore_errors=True)


def report(plan, texts, pending, manual, applied):
    print("%s: Volume %s (%d), %s" % ("Applied" if applied else "Plan", plan.roman, plan.number, plan.title))
    print("  folder: %s" % plan.folder)
    print("  date of the move: %s" % plan.date)
    print("Chapters:")
    for old, new in plan.moves:
        print("  Volume CLXXII Chapter %s -> Chapter %s   %s" % (old.split("-", 1)[0], new.split("-", 1)[0], new))
    print("Data files: %d" % len(plan.data))
    for old, new in plan.data:
        print("  %s -> %s" % (old, new))
    for name in plan.stray:
        print("  left in Volume CLXXII, check it: %s" % name)
    left = [(new, line, phrase) for _, new in plan.moves for line, phrase in unrewritten(texts[new], plan.own)]
    print("Chapter references that need a person: %d" % len(left))
    for new, line, phrase in left:
        print("  %s line %d: %s" % (new, line, phrase))
    print("Existing files %s: %d" % ("changed" if applied else "to change", len(pending)))
    for path in sorted(pending):
        print("  %s" % path)
    print("Steps the script cannot do: %d" % len(manual))
    for step in manual:
        print("  %s" % step)


def check(plan):
    problems = []
    for name in ("README.md", "INDEX.md", "GLOSSARY.md", "chapters/" + AS_BUILT):
        path = "%s/%s" % (plan.folder, name)
        if not os.path.exists(path):
            problems.append("%s is missing" % path)
        else:
            for i, line in enumerate(read(path).split("\n"), 1):
                if MARK in line:
                    problems.append("%s line %d: a TODO comment is left" % (path, i))
    for folder, _, files in os.walk(plan.folder):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = posixpath.join(folder.replace(os.sep, "/"), name)
            text = read(path)
            if posixpath.dirname(path).endswith("/chapters") and name != AS_BUILT:
                for line, phrase in unrewritten(text, plan.own):
                    problems.append("%s line %d: '%s' names no volume" % (path, line, phrase))
            for match in LINK_RE.finditer(text):
                target = match.group(2)
                if "://" not in target and not target.startswith("mailto:") and not os.path.exists(
                        posixpath.normpath(posixpath.join(posixpath.dirname(path), target))):
                    problems.append("%s: the link to %s does not resolve" % (path, target))
            for old, _ in plan.moves:
                if "data/volume-172-disa-srgs-and-stigs/%s-" % old.split("-", 1)[0] in text:
                    problems.append("%s: a CSV link still uses the Volume CLXXII address" % path)
    before = git("status", "--porcelain") + git("diff")
    done = subprocess.run([sys.executable, EXPORT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if done.returncode:
        problems.append("%s failed" % EXPORT)
    elif before != git("status", "--porcelain") + git("diff"):
        problems.append("%s changed a file: a table and its CSV file or link did not match" % EXPORT)
    if "volume-%d" % plan.number not in read("book.yml"):
        problems.append("book.yml does not list volume-%d" % plan.number)
    print("Check of Volume %s (%s): %s" % (plan.roman, plan.slug, "OK" if not problems else "%d problem(s)" % len(problems)))
    for problem in problems:
        print("  " + problem)
    if not problems:
        print("  Now run scripts/bash/validate.sh.")
    return 1 if problems else 0


def main():
    parser = argparse.ArgumentParser(description="Move a Fortinet product's chapters from Volume CLXXII to its own volume.")
    parser.add_argument("product", help='the product name as the chapter titles write it, for example "FortiManager"')
    parser.add_argument("--apply", action="store_true", help="make the move (the default is a dry run)")
    parser.add_argument("--check", action="store_true", help="check a finished move")
    parser.add_argument("--volume", type=int, help="volume number, 200 to 299")
    parser.add_argument("--chapters", help="chapter numbers of Volume CLXXII to move, the map chapter first")
    parser.add_argument("--date", help="date of the move, YYYY-MM-DD")
    args = parser.parse_args()
    plan = make_plan(args)
    if args.check:
        sys.exit(check(plan))

    sources = dict((new, read("%s/chapters/%s" % (V172, old))) for old, new in plan.moves)
    old_titles = dict((new, chapter_title(sources[new])) for _, new in plan.moves)
    texts = dict((new, plan.rewriter.run(sources[new], V172 + "/chapters", plan.folder + "/chapters"))
                 for _, new in plan.moves)
    plan.titles = dict((new, chapter_title(texts[new])) for _, new in plan.moves)
    pending, manual = edits_for_existing_files(plan)
    for old, new in plan.moves:
        pending["%s/chapters/%s" % (V172, old)] = pointer_page(plan, old, new, old_titles[new])

    if not args.apply:
        report(plan, texts, pending, manual, False)
        print("CSV export on a scratch copy under the new names: %s"
              % ("same content as today's files" if export_matches(plan) else "DIFFERENT from today's files, look before you apply"))
        print("New files: README.md, INDEX.md, GLOSSARY.md, and chapters/%s in %s" % (AS_BUILT, plan.folder))
        print("Dry run: nothing was changed. Run again with --apply to make the move.")
        return

    os.makedirs(plan.folder + "/chapters")
    if plan.data:
        os.makedirs(plan.folder + "/data")
    for old, new in plan.moves:
        git("mv", "%s/chapters/%s" % (V172, old), "%s/chapters/%s" % (plan.folder, new))
        write("%s/chapters/%s" % (plan.folder, new), texts[new])
    for old, new in plan.data:
        git("mv", "%s/data/%s" % (V172, old), "%s/data/%s" % (plan.folder, new))
    for path, text in pending.items():
        write(path, text)
    done = subprocess.run([sys.executable, EXPORT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if done.returncode:
        die("%s failed after the move:\n%s" % (EXPORT, done.stdout.decode("utf-8", "replace")))
    for path, text in new_volume_files(plan).items():
        write(path, text)
    texts = dict((new, read("%s/chapters/%s" % (plan.folder, new))) for _, new in plan.moves)
    report(plan, texts, pending, manual, True)
    marks = sum(read(path).count(MARK) for path in new_volume_files_paths(plan))
    print("TODO comments to replace with prose in the new volume: %d" % marks)
    print("Nothing was committed. Next: rewrite the references listed above, replace the TODO comments,")
    print("do the listed steps, then run this script with --check and scripts/bash/validate.sh.")


def new_volume_files_paths(plan):
    return [plan.folder + "/README.md", plan.folder + "/INDEX.md", plan.folder + "/GLOSSARY.md",
            "%s/chapters/%s" % (plan.folder, AS_BUILT)]


if __name__ == "__main__":
    main()
