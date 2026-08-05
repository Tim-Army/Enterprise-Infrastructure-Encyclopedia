# Chapter 04: Confluence Administration

## Learning Objectives

- Explain Confluence's structure — spaces, pages, and the page tree.
- Administer space permissions and understand the inheritance model.
- Use templates and macros to make knowledge maintainable rather than sprawling.
- Recognize the knowledge-rot failure mode Confluence admins fight.

*Cert relevance: the **Confluence Administration** certification (ACP) — spaces, permissions, templates, and the content lifecycle.*

## What Confluence is

Confluence is Atlassian's **team knowledge and documentation** platform — where organizations write down decisions, processes, project plans, and reference material. Where Jira tracks *work*, Confluence holds *knowledge*, and the pair is the point: a Jira ticket links to the Confluence page explaining the decision behind it.

The administrator's job is not writing the content — it is keeping the *structure* navigable and the *permissions* correct as thousands of pages accumulate, which is a harder problem than it sounds.

## Spaces and the page tree

Confluence's structure is two levels:

| Level | Is |
|:---|:---|
| **Space** | A container for related content — a team, a project, a department |
| **Page** | A document within a space, arranged in a **page tree** (pages have child pages) |

The **space** is the unit of organization and permission, the way a Jira project is. The design question every Confluence admin faces is **how to carve the organization into spaces** — one per team? per project? per product? — and there is no universal answer, only the trade: too few spaces and everything piles into a few unnavigable giants; too many and knowledge fragments across spaces nobody can find.

The **page tree** within a space is where knowledge either stays findable or rots. A shallow, well-organized tree is navigable; a deep, ad-hoc one becomes the place documents go to be lost. This is Confluence's version of the scheme-sprawl problem — structure decays unless someone tends it.

## Permissions and inheritance

Confluence permissions operate at two levels, and confusing them is the classic admin error:

- **Space permissions** — who can view, add, or administer content in a space. The primary control.
- **Page restrictions** — additional limits on *individual pages*, which can *further restrict* (never broaden) beyond the space permissions.

The inheritance rule that trips people up: **page restrictions can only narrow, not widen.** A page in an open space can be restricted to a few people; a page in a restricted space *cannot* be opened to more people than the space allows. Access is the intersection of space permission and page restriction, and an admin who thinks a page restriction can grant access has the model backwards — the lab makes this concrete, because it is a real source of "why can't they see this page?" tickets.

## Templates and macros: maintainability

Two features separate a healthy Confluence from a chaotic one:

- **Templates** standardize recurring page types (meeting notes, decision records, project charters). A template is to a page what a scheme is to a Jira project — configure the structure once, and every instance is consistent and complete.
- **Macros** embed dynamic content: a Jira issue list on a Confluence page, a table of contents, a status. Used well, they keep a page current automatically; overused, they make pages slow and fragile.

The through-line, again, is **structure as maintainability**: templates keep new content consistent, a tended page tree keeps it findable, and the alternative — let everyone create freely with no structure — produces the knowledge base everyone has and nobody trusts.

## Hands-On Lab

Python models Confluence administration. **Cost:** none.

### Lab 4.1 — Permission inheritance: narrow, never widen

**Objective:** Compute effective access from space + page.

```bash
python3 - <<'EOF'
SPACES = {
  "Engineering (open)":     {"view": {"all-staff"}},
  "HR (restricted)":        {"view": {"hr-team", "managers"}},
  "Board (locked)":         {"view": {"board-members"}},
}
PAGES = [
  # page,                     space,                 page_restriction (further limit)
  ("Onboarding guide",        "Engineering (open)",  None),
  ("Salary bands",            "Engineering (open)",  {"hr-team", "managers"}),   # narrowed
  ("Team offsite notes",      "HR (restricted)",     None),
  ("Attempt to 'open' a page","HR (restricted)",     {"all-staff"}),            # tries to WIDEN
  ("Board minutes",           "Board (locked)",      {"board-chair"}),           # narrowed further
]
def effective(space, restriction):
    space_view = SPACES[space]["view"]
    if restriction is None:
        return space_view
    # page restriction can only NARROW: intersection with space permission
    return space_view & restriction
for page, space, restr_set in PAGES:
    eff = effective(space, restr_set)
    note = ""
    if restr_set and not (restr_set <= SPACES[space]["view"]):
        note = "  <-- page tried to WIDEN; extra groups IGNORED (intersection only)"
    print(f"{page:28} space={space:22}")
    print(f"{'':28} restriction={restr_set}")
    print(f"{'':28} EFFECTIVE VIEW = {eff or 'nobody'}{note}\n")
print("The rule made concrete: effective access = space permission INTERSECT page")
print("restriction. Restrictions can only NARROW.")
print("\n'Attempt to open a page': HR space allows {hr-team, managers}; a page")
print("restriction listing 'all-staff' does NOT grant all-staff access — the")
print("intersection with the space's {hr-team, managers} is still just those two.")
print("The extra group is silently ignored. This is the #1 'why can't they see it?'")
print("ticket: someone added a group to a PAGE expecting it to grant access, not")
print("realizing the SPACE permission is the ceiling.")
print("\nTo grant broader access, change the SPACE permission — the page restriction")
print("is a narrowing tool only.")
EOF
```

**Expected result:** Effective access computed as space-permission intersected with page-restriction, with the widening attempt silently ignored. The narrow-never-widen rule is the admin lesson — the space permission is the ceiling, page restrictions only lower it, and the reversed mental model is the source of the most common access ticket.

**Negative test:** Adding a group to a page's restrictions to grant them access in a restricted space. The intersection with the space permission ignores the addition; access is unchanged and the ticket reopens.

**Cleanup:** None.

### Lab 4.2 — Space design: too few, too many, or right

**Objective:** Carve an organization into spaces sensibly.

```bash
python3 - <<'EOF'
STRATEGIES = {
  "one giant space":        {"spaces": 1,   "avg_pages": 8000, "findability": 1, "consistency": 2},
  "space per project":      {"spaces": 340, "avg_pages": 24,   "findability": 2, "consistency": 2},
  "space per team + shared":{"spaces": 45,  "avg_pages": 180,  "findability": 4, "consistency": 4},
}
print(f"{'strategy':28}{'spaces':>8}{'pages/space':>13}{'findable':>10}{'consistent':>12}")
for name, s in STRATEGIES.items():
    print(f"{name:28}{s['spaces']:>8}{s['avg_pages']:>13}{s['findability']*'#':>10}{s['consistency']*'#':>12}")
print("\nThe two failure modes bracket the good answer:")
print("  ONE GIANT SPACE: 8000 pages in one tree — nobody finds anything, the search")
print("     box IS the navigation, and permissions are all-or-nothing.")
print("  SPACE PER PROJECT: 340 spaces — knowledge FRAGMENTS. 'Where's the deploy")
print("     runbook?' could be any of 340 places; cross-project knowledge has no home.")
print("  SPACE PER TEAM (+ shared spaces for cross-cutting docs): ~45 spaces, each")
print("     navigable, permissions align to teams, and shared spaces hold the")
print("     org-wide references. This is usually the healthy middle.")
print("\nNo universal answer — it depends on org size and how work is structured —")
print("but the SHAPE of the trade is universal: too few spaces = unnavigable giants,")
print("too many = fragmentation. Carve along how PEOPLE actually look for knowledge.")
print("\n(This is the company-managed-vs-team-managed decision from Chapter 02 in")
print("Confluence clothing: centralize for findability, decentralize for autonomy,")
print("and the answer is almost never either extreme.)")
EOF
```

**Expected result:** The space-per-team strategy scoring best on both findability and consistency, bracketed by the unnavigable giant and the fragmented per-project sprawl. The parallel to Chapter 02's project-type decision is the unifying lesson — centralize-versus-decentralize, and the answer is almost never an extreme.

**Negative test:** One space per project for an org with heavy cross-project knowledge. The deploy runbook that ten teams need has no natural home and gets duplicated (and then the copies diverge).

**Cleanup:** None.

### Lab 4.3 — Knowledge rot and the tended tree

**Objective:** Model why documentation decays without maintenance.

```bash
python3 - <<'EOF'
import random
random.seed(31)
# 500 pages created over 2 years. Without curation, most pages are written once
# and never revisited — the realistic pattern, not uniform re-editing.
pages = []
for i in range(500):
    age_days = random.randint(1, 730)
    # ~70% of pages are never meaningfully edited after creation (write-once);
    # the rest get a follow-up edit at some point in their life.
    if random.random() < 0.70:
        last_edit = age_days                       # never re-edited since creation
    else:
        last_edit = random.randint(0, age_days)    # edited again at some point
    pages.append({"age": age_days, "since_edit": last_edit})
STALE_THRESHOLD = 365
stale = [p for p in pages if p["since_edit"] > STALE_THRESHOLD]
very_stale = [p for p in pages if p["since_edit"] > 540]
print(f"500 pages, no curation process:\n")
print(f"   stale (>1yr since edit):     {len(stale)} ({len(stale)/len(pages)*100:.0f}%)")
print(f"   very stale (>18mo):          {len(very_stale)} ({len(very_stale)/len(pages)*100:.0f}%)")
print("\nThe knowledge-rot problem: pages do not announce when they go wrong. A")
print("runbook edited 18 months ago LOOKS as authoritative as one edited yesterday,")
print("and a reader cannot tell the current process from the abandoned one. Stale")
print("docs are worse than missing docs — missing docs send you to ask a human;")
print("stale docs send you confidently in the wrong direction.")
print("\nWhat a Confluence admin does about it (the curation the cert expects):")
print("  - TEMPLATES with owners + review dates baked in (a 'last reviewed' field)")
print("  - periodic REVIEW of pages past the staleness threshold (archive or update)")
print("  - ARCHIVE spaces for retired content — remove it from search, don't delete")
print("  - macros that SURFACE staleness ('pages not edited in 12 months in this space')")
print("\nThe admin does not write the docs, but OWNS the process that keeps the")
print("knowledge base trustworthy. Without it, Confluence becomes the wiki everyone")
print("has and nobody believes — structure without curation still rots.")
EOF
```

**Expected result:** Nearly 40% of pages going stale (and 17% very stale) in a two-year uncurated instance, with the insight that stale documentation is worse than missing documentation. The curation process — templates with review dates, periodic review, archiving, staleness-surfacing macros — is the admin's actual job, since the content authorship belongs to the teams but the trustworthiness process belongs to the admin.

**Negative test:** Treating Confluence as write-once storage. Within two years roughly 40% of the content is stale, indistinguishable from current, and actively misleading readers.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Confluence's space/page/page-tree structure understood as the organization and permission model.
- [ ] Effective access computed as space-permission intersected with page-restriction — narrow, never widen.
- [ ] Space design carved along how people look for knowledge, avoiding both giants and fragmentation.
- [ ] Knowledge rot addressed with templates, review cycles, and archiving — curation as the admin's job.
