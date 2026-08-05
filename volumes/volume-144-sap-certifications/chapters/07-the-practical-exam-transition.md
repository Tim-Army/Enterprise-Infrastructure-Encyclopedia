# Chapter 07: The Practical Exam Transition

## Learning Objectives

- Explain what changed in SAP's 2026 move to practical, performance-based exams.
- Understand the open-book, AI-allowed, unproctored format and its rationale.
- Prepare for a practical exam — a genuinely different study problem.
- Know the transition rules: who is affected, scoring, and timing.

*This chapter is the defining feature of the current SAP program. Every certification is affected, and the format is unlike the multiple-choice exams most SAP study material still assumes.*

## What changed, exactly

Through the first quarter of 2026, SAP replaced its certification exams' format:

> **"SAP Certification is transitioning to practical certification exams in planned phases. Most exams will be available by mid-January 2026 with all practical exams transitioned by end-March."**

The old format was **multiple-choice**: 80 questions, pick the right answers, pass at a threshold, proctored. The new format, in SAP's own four points:

1. **System-based tasks or roleplay scenarios tailored to each certification** — you perform the work, or handle a realistic scenario, rather than answer questions about it.
2. **Timeboxed challenges designed around real project expectations** — structured like the job, under a clock.
3. **Open-book approach allowing use of relevant resources and AI-supported tools** — you may consult documentation *and AI assistants during the exam*.
4. **No live proctoring** — a self-managed exam experience.

Each of these inverts an assumption of the old exam, and the third one — **open-book with AI tools allowed** — is the radical one.

## Why: the AI-era rationale

SAP's stated reasoning is worth engaging with rather than dismissing as marketing, because it is the argument the whole industry will have to answer:

> When AI can instantly recall any fact, transaction code, or configuration path, **memorizing those facts is no longer a skill worth certifying.** What remains scarce and valuable is the ability to *apply* knowledge — to solve a real problem, in a real system, using whatever tools are at hand, exactly as the job actually works.

The old multiple-choice exam tested whether you had memorized what the AI now knows. The new exam hands you the AI and asks whether you can *direct it to an outcome*. This is honest: it aligns the exam with the real working conditions, where no consultant works without documentation and, increasingly, without an AI assistant. **"Prove what you can do, not just what you know."**

The uncomfortable corollary for exam-takers: **you cannot cram a practical exam.** Memorizing a question bank — the traditional SAP-certification study method, which spawned an entire dumps industry — is worthless when the exam is a task in a live system with the documentation open. The only preparation is *doing the work*, which is why the two-attempt bundle now includes 10 hours of practice-system access (Chapter 01).

## The transition rules

| Rule | Detail |
|:---|:---|
| **Who must take the practical format** | **First-time exam takers only** |
| **Already certified?** | No immediate re-certification; continue renewal cycle, take the standard "stay-certified assessment" at expiration |
| **Scoring** | Auto-scored or AI-reviewed; **video submissions scored by experts within 20 business days** |
| **Languages** | Scenario-based in multiple languages; system-based English-first, others planned |
| **Recognition** | Still a **Credly badge** showing type and level; description highlights the applied validation |

The 20-business-day expert scoring for video submissions is a real planning fact: **a practical exam is not always instant-result.** For a video-scored component, the certification is not confirmed on exam day — budget the four weeks.

## Hands-On Lab

Python models practical-exam preparation. **Cost:** none.

### Lab 7.1 — Why you cannot cram a practical exam

**Objective:** Contrast question-bank study with practice-system study.

```bash
python3 - <<'EOF'
import random
random.seed(44)
# A candidate's readiness under two study methods, tested two ways
def old_exam_score(memorized_fraction):
    return memorized_fraction                       # multiple choice rewards recall
def practical_exam_score(hands_on_hours):
    return min(0.98, 1 - 0.9 ** (hands_on_hours/3)) # rewards accumulated DOING

CANDIDATES = [
  ("crammed the dump, 0 hrs hands-on",   0.92, 0),
  ("studied notes, 5 hrs hands-on",      0.70, 5),
  ("light study, 25 hrs hands-on",       0.55, 25),
  ("experienced consultant, 200+ hrs",   0.60, 60),
]
print(f"{'candidate':38}{'OLD (MC)':>10}{'NEW (practical)':>17}")
for name, mem, hrs in CANDIDATES:
    old = old_exam_score(mem)
    new = practical_exam_score(hrs)
    print(f"{name:38}{old*100:>9.0f}%{new*100:>16.0f}%")
print("\nThe dump-crammer ACES the old exam (92%) and FAILS the new one (0 hands-on")
print("hours -> ~0%). The experienced consultant is mediocre at trivia recall but")
print("excellent at the practical exam — because it tests what they actually do.")
print("\nThis is the transition's whole point, made numeric: the two exams reward")
print("OPPOSITE preparation. Every 'SAP certification dump' still sold online is")
print("preparing people for an exam that no longer exists.")
print("\nThe new study plan: HOURS IN THE SYSTEM. There is no shortcut, which is")
print("exactly what SAP intended — a certification you cannot fake by memorizing.")
EOF
```

**Expected result:** The dump-crammer acing the old multiple-choice exam and failing the practical one, while the experienced consultant shows the reverse. The opposite-preparation framing is the chapter's core — the format change makes the entire question-bank study industry obsolete, and the only preparation for a practical exam is accumulated hands-on time.

**Negative test:** Preparing for a 2026 SAP practical exam with a question dump. It targets a format that was retired by March 2026; the exam is a live-system task with the docs open.

**Cleanup:** None.

### Lab 7.2 — Open-book with AI changes what to practice

**Objective:** Reallocate study time to what the format actually tests.

```bash
python3 - <<'EOF'
STUDY_ACTIVITIES = [
  # activity,                              old_exam_value, new_exam_value
  ("memorize transaction codes",                5,  1),   # AI/docs supply these now
  ("memorize config menu paths",                5,  1),
  ("memorize field-level details",              5,  1),
  ("practice completing tasks in the system",   2,  5),   # THE exam now
  ("learn to find answers in docs FAST",        1,  5),   # open-book skill
  ("learn to direct the AI assistant well",     0,  5),   # AI-allowed skill
  ("understand WHY a process works",            3,  5),   # judgment, not recall
  ("time-management under a clock",             2,  5),   # timeboxed
]
print(f"{'study activity':44}{'OLD value':>10}{'NEW value':>10}   shift")
for act, old, new in STUDY_ACTIVITIES:
    arrow = "UP" if new > old else ("DOWN" if new < old else "=")
    print(f"{act:44}{old:>10}{new:>10}   {arrow}")
print("\nThe reallocation is stark: everything MEMORIZATION drops to near-zero value")
print("(the AI and the docs supply it during the exam); everything APPLICATION and")
print("SPEED rises. Two brand-new high-value skills appear that the old exam never")
print("tested at all:")
print("  - finding answers in documentation FAST (open-book is only an advantage")
print("    if you can navigate the docs quicker than the clock)")
print("  - directing the AI assistant effectively (it is in the room; using it well")
print("    is now part of the assessed skill, exactly as in the real job)")
print("\nStudy plan inversion: STOP memorizing, START doing — in the system, against")
print("the clock, with the docs and AI open, practicing the exact conditions of the exam.")
EOF
```

**Expected result:** Memorization activities collapsing to near-zero study value while application, doc-navigation speed, and AI-direction rise — including two skills the old exam never tested. The reallocation is the actionable content — open-book-with-AI is only an advantage if you have practiced navigating docs and directing AI faster than the timebox allows.

**Negative test:** Studying for the practical exam by memorizing more thoroughly. You are optimizing the one dimension the open-book format explicitly neutralizes.

**Cleanup:** None.

### Lab 7.3 — Plan around the 20-day scoring window

**Objective:** Schedule a certification with a video-scored component.

```bash
python3 - <<'EOF'
from datetime import date, timedelta
def add_business_days(start, n):
    d, added = start, 0
    while added < n:
        d += timedelta(days=1)
        if d.weekday() < 5: added += 1
    return d

exam_day = date(2026, 9, 14)   # a Monday
COMPONENTS = [
  ("system-based tasks",  "auto/AI-scored",   "same day"),
  ("scenario roleplay",   "AI-reviewed",      "same day / days"),
  ("video submission",    "expert-scored",    "20 business days"),
]
print(f"Exam taken: {exam_day} ({exam_day.strftime('%A')})\n")
print(f"{'component':22}{'scoring':>18}   result available")
for comp, scoring, when in COMPONENTS:
    if "20 business" in when:
        result = add_business_days(exam_day, 20)
        when = f"{result} ({result.strftime('%A')})"
    print(f"{comp:22}{scoring:>18}   {when}")
result = add_business_days(exam_day, 20)
print(f"\nA video-scored certification taken {exam_day} is not CONFIRMED until {result} —")
print(f"nearly a MONTH later. That is not a delay, it is the published process:")
print("expert humans score video within 20 business days.")
print("\nPlanning consequences:")
print("  - do NOT schedule an exam the week you need the badge (a job start, an RFP")
print("    deadline, a partner-status requirement) — build in the 4-week window")
print("  - a FAILED video component is also learned ~4 weeks later; the retake")
print("    clock starts then, so a tight timeline can slip two months on one retry")
print("  - the auto-scored components ARE instant; the window applies only where")
print("    video is part of the exam — check which your target certification uses")
EOF
```

**Expected result:** A video-scored certification taken September 14 confirming around October 12 — nearly a month later. The planning consequences are the practical payoff — the 20-business-day expert scoring means a practical exam is not always instant-result, so certification timing must account for the window, especially where a badge gates a job or partner status.

**Negative test:** Scheduling a video-scored SAP exam the week before a deadline that requires the certification. The result lands ~20 business days later; the deadline passes uncertified.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The 2026 practical-exam transition and its four format changes understood.
- [ ] The AI-era rationale engaged: recall is delegated to AI, application is what remains scarce.
- [ ] Preparation reallocated from memorization to hands-on practice, doc-speed, and AI-direction.
- [ ] The transition rules known: first-timers only, and the 20-business-day video-scoring window.
