"""Register a new Volume CLXXII chapter. Run from the repository root.

Usage: python .claude/skills/srg-mapping-for/register.py <spec.json>

Spec (JSON):
  nn            chapter number (int)
  file          chapter file name, for example "33-juniper-products-stigs-and-srg-mapping.md"
  title         title without the "Chapter NN: " prefix
  readme_line   the volume README chapter-list line, "NN. [Title](chapters/file.md) — summary."
  index         [[topic, extra_links_or_empty], ...]  -> INDEX.md lines, link to this chapter appended
  glossary      [[term, definition], ...]             -> GLOSSARY.md lines
  overview_file optional: chapter file of the vendor overview (for example "10-fortinet-...md")
  overview_old  optional: exact text in that chapter to replace (for example the product's table row ending)
  overview_new  optional: replacement text
  words         space-separated words to add to cspell.json

Chapter 90 is the volume's as-built chapter and stays last: a new chapter goes
before it in book.yml and the volume README, and chapter_count is the number of
chapter entries, not nn.

It updates book.yml (entry and chapter_count), the root README.md and
PROJECT_STATUS.md counts, the volume README chapter list and index count,
INDEX.md and GLOSSARY.md (alphabetically), the overview chapter row, and
cspell.json. It does NOT write the volume README's overview prose; edit that by
hand. Every edit is checked; if one fails, the script stops before writing any
file, so it is safe to fix the spec and run it again.
"""
import json
import re
import sys

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen " \
       "fifteen sixteen seventeen eighteen nineteen".split()
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def words(n):
    if n < 20:
        return ONES[n]
    t, o = divmod(n, 10)
    return TENS[t] + ("" if o == 0 else "-" + ONES[o])


spec = json.load(open(sys.argv[1], encoding="utf-8"))
V = "volumes/volume-172-disa-srgs-and-stigs/"
nn, f = spec["nn"], spec["file"]
link = f"[Chapter {nn}](chapters/{f})"
pending = {}


def load(p):
    return pending.get(p) or open(p, encoding="utf-8").read()


def edit(p, fn):
    s = load(p)
    t = fn(s)
    if t == s:
        sys.exit(f"register.py: no change made to {p}; check the spec")
    pending[p] = t


def bump(s, pat):
    m = re.search(pat, s)
    if not m:
        sys.exit(f"register.py: pattern not found: {pat}")
    a, b = m.span(1)
    return s[:a] + str(int(m.group(1)) + 1) + s[b:]


def book(s):
    if f"chapters/{f}" in s:
        sys.exit("register.py: chapter already in book.yml")
    i = s.index("slug: volume-172-disa-srgs-and-stigs")
    j = s.index("\n  - id: volume-", i)
    blk = s[i:j].rstrip("\n")
    new = (f'\n      - id: {nn}\n        title: "Chapter {nn}: {spec["title"]}"'
           f"\n        path: {V}chapters/{f}")
    k = blk.find("\n      - id: 90\n")  # the as-built chapter stays last
    blk = blk + new if k < 0 else blk[:k] + new + blk[k:]
    count = len(re.findall(r"\n      - id: ", blk))
    blk = re.sub(r"chapter_count: \d+", f"chapter_count: {count}", blk)
    return s[:i] + blk + s[j:]


edit("book.yml", book)
edit("README.md", lambda s: bump(bump(s, r"\d+ volumes, (\d+) chapters\."),
     r"\| CLXXII \| \[DISA SRGs and STIGs\]\(volumes/volume-172-disa-srgs-and-stigs/README\.md\) \| (\d+) \|"))
edit("PROJECT_STATUS.md", lambda s: bump(bump(bump(
    s, r"\| CLXXII — DISA SRGs and STIGs \| (\d+) \| Drafted \|"),
    r"\*\*Total declared chapters:\*\* (\d+) of \d+"),
    r"\*\*Total declared chapters:\*\* \d+ of (\d+)"))


def vreadme(s):
    k = s.find("\n90. [")  # the as-built chapter stays last
    if k < 0:
        k = s.index("\n## Volume resources")
        s = s[:k].rstrip("\n") + "\n" + spec["readme_line"] + "\n" + s[k:]
    else:
        s = s[:k] + "\n" + spec["readme_line"] + s[k:]
    listed = s[s.index("\n## Chapters"):s.index("\n## Volume resources")]
    count = len(re.findall(r"^\d+\. \[", listed, re.M))
    return s.replace(f"across all {words(count - 1)} chapters", f"across all {words(count)} chapters")


edit(V + "README.md", vreadme)


def alpha(entries):
    def fn(s):
        lines = s.split("\n")
        for term, rest in entries:
            idx = [i for i, l in enumerate(lines) if l.startswith("- **")]
            pos = next((i for i in idx
                        if re.match(r"- \*\*(.*?)\*\*", lines[i]).group(1).lower() > term.lower()),
                       idx[-1] + 1)
            lines.insert(pos, f"- **{term}** — {rest}")
        return "\n".join(lines)
    return fn


if spec.get("index"):
    edit(V + "INDEX.md", alpha([(t, (e + ", " if e else "") + link) for t, e in spec["index"]]))
if spec.get("glossary"):
    edit(V + "GLOSSARY.md", alpha(spec["glossary"]))
if spec.get("overview_old"):
    edit(V + "chapters/" + spec["overview_file"],
         lambda s: s.replace(spec["overview_old"], spec["overview_new"], 1))

d = json.loads(load("cspell.json"))
low = {w.lower() for w in d["words"]}
for w in spec.get("words", "").split():
    if w.lower() not in low:
        d["words"].append(w)
        low.add(w.lower())
pending["cspell.json"] = json.dumps(d, indent=2, ensure_ascii=False) + "\n"

for p, t in pending.items():
    open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"registered chapter {nn}: {', '.join(pending)}")
