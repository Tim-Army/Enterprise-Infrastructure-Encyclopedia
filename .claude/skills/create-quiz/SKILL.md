---
name: create-quiz
description: Turn a folder of training screenshots and/or screen-recording videos into an interactive, self-grading multiple-choice quiz (HTML + markdown question bank), with each answer checked against its source frame. Use when the user runs /create-quiz or asks to build a study quiz from course media.
argument-hint: <media folder inside the repo>
---

# /create-quiz

Build a multi-lesson study quiz from course media. Everything happens inside this repo
(`D:\Documents\claude\Enterprise-Infrastructure-Encyclopedia`): read, write and scratch only there.

Paths used below:
- `REPO` = `D:\Documents\claude\Enterprise-Infrastructure-Encyclopedia`
- `GEN` = `REPO\.claude\skills\create-quiz\gen_quiz.py` (HTML + markdown generator)
- `WORK` = `REPO\temp\create-quiz-work\<quiz-slug>` (gitignored scratch: frames, lesson JSON, verdicts)
- `ffmpeg` / `ffprobe`: `D:\ffmpeg\bin\`

## 1. Inputs

- **Source folder**: the argument. Default `REPO\imports`. It must be inside the repo; if not, stop and say so.
- **Output folder**: ALWAYS ask with AskUserQuestion before doing any work. Offer:
  - `<source folder>\quiz` (next to the media; gitignored if the source is under `imports/`)
  - `REPO\exports\<quiz-slug>` (tracked in git, for publishing)
  - `REPO\publishing\interactive` (where published quizzes live; the files are renamed `<quiz-slug>.html` / `<quiz-slug>-question-bank.md`)
  The user may type any other folder, but it must be inside the repo.
- **Maximum questions**: 1000 for the whole quiz unless the user gives another number.
- **Title / subject**: infer from the file names (e.g. "FortiGate 7.6 Administrator (NSE 4)"); ask in the same AskUserQuestion call only if they can't be inferred.
- Run the rest without further questions.

## 2. Discover lessons

List media in the source folder (non-recursive): images (`.png/.jpg/.jpeg`) and videos (`.mp4/.mov/.m4v/.webm`).

- **Videos**: one lesson each, ordered by file name. Get durations with `ffprobe`. Extract one frame every 25 s from keyframes (fast), in parallel, into `WORK\frames\L<NN>\`, named `<slug>-L<NN>_t<seconds>s.png`:
  `ffmpeg -loglevel error -skip_frame nokey -i <video> -vf fps=1/25 -fps_mode vfr tmp_%04d.png`, then rename frame *i* to `t=(i-1)*25`.
- **Screenshots**: split into lessons wherever capture time jumps by more than 15 minutes (parse the timestamp in the file name, else use LastWriteTime, else treat them as one lesson ordered by name). Screenshot lessons come before video lessons.
- Name each lesson from its file name, or read its first frame.
- Read one frame to confirm it's legible before continuing.

## 3. Draft (one background agent per lesson)

Launch one `general-purpose` agent per lesson, all in one message, `run_in_background: true`. Each prompt must be self-contained:

- Lesson id, name, frames folder, frame count, output file `WORK\lessons\L<NN>.json`.
- Only read and write inside REPO.
- Read EVERY frame in numeric time order; read slide text AND any speaker-notes panel; ignore repeats, title and black frames.
- Questions: exactly 4 options, one correct; plausible, topical distractors; grounded strictly in the frames (no outside knowledge); self-contained wording; mixed difficulty; favour concepts, behaviours, defaults, order of operations, CLI/GUI paths and troubleshooting over trivia.
- Write as many high-quality questions as the frames genuinely support, up to the lesson's cap: the quiz-wide maximum (default **1000**, or whatever the user sets) split across lessons in proportion to their frame counts. Never pad to reach the cap. No duplicates.
- 3–6 sections, answer key balanced across A–D, 3–6 objectives, `source` = absolute path of the best supporting frame.
- Output shape:
  `{"id":N,"name":"...","objectives":[...],"sections":[...],"questions":[{"num":1,"section":"...","topic":"...","question":"...","options":[4],"correct_index":0,"rationale":"...","source":"<abs path>","difficulty":"easy|medium|hard"}]}`
- Validate the JSON parses; reply with only the count, sections and unreadable frames.

## 4. Verify (one background agent per lesson, after its draft lands)

As each draft finishes, launch a separate `general-purpose` agent to check it adversarially. For every question it reads the `source` frame (and neighbouring frames if needed) and decides:
- `confirmed`: the marked answer is clearly supported and no distractor is also true.
- `refuted`: the marked answer is wrong or unsupported, or a distractor is also correct. It gives a fix.
- `unclear`: the frames don't show enough to tell.

It writes `WORK\verify\L<NN>.json` as `{"verdicts":[{"n":1,"verdict":"...","observed":"...","issue":"...","suggested_fix":"..."}]}` and fixes the lesson file in place: it applies fixes for `refuted` items where the frame supports a correct version, and drops the question otherwise. `unclear` items are dropped or rewritten to what the frame does show. It renumbers the questions and re-balances A–D afterwards. It replies with confirmed / fixed / dropped counts.

## 5. Build

With all lessons verified, run a short Python script (in WORK) that:
1. Loads `WORK\lessons\L*.json` in id order.
2. Builds `dataset.json` in the output folder:
   - top level: `title`, `subject`, `source_desc`, `brand` = title, `brand_tag` = "Quiz", `hero` = title, `eyebrow` = "Self-Check", `out_html`, `out_md`, `lessons`, `questions`.
   - `lessons[]`: `{id, name, short, objectives, sections}`, where `short` is the name if ≤ 20 chars, otherwise its first two words.
   - `questions[]`: ordered by lesson, then section order, with a running global `n` and per-lesson `ln`: `{n, ln, lesson, section, topic, q, opts, a, rat, src, diff}`. `src` is `"Video · m:ss"` from the `_t<sec>s` frame name, `"Slide · hh:mm:ss"` for timestamped screenshots, else the file name.
3. Runs `python GEN` with the output folder as the working directory.

Confirm `quiz.html` and `quiz-question-bank.md` exist (or the renamed files) and report their sizes.

## 6. Report

Tell the user the lesson list with question counts, the total, verification results (confirmed / fixed / dropped), and links to the output files. Mention whether the output folder is tracked or gitignored. Leave `WORK` in place (it's gitignored) unless the user asks to clean it up.
