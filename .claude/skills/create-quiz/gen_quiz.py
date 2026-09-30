import json, re, sys

# Generalized interactive-quiz generator (asset for the "create-quiz" workflow).
# Reads dataset.json in the CWD and writes an interactive HTML quiz + a markdown bank.
# dataset.json shape:
#   { "title": "...", "brand": "...", "brand_tag": "...", "eyebrow": "...",
#     "hero": "...", "subject": "...", "source_desc": "...",
#     "out_html": "quiz.html", "out_md": "quiz-question-bank.md",
#     "lessons": [ {id,name,short,objectives:[...],sections:[...]} ],
#     "questions": [ {n,ln,lesson,section,topic,q,opts:[4],a,rat,src,diff} ] }

ds = json.load(open('dataset.json', encoding='utf-8'))
lessons = ds['lessons']
combined = ds['questions']

TITLE       = ds.get('title', 'Study Quiz')
BRAND       = ds.get('brand', TITLE)
BRAND_TAG   = ds.get('brand_tag', 'Quiz')
EYEBROW     = ds.get('eyebrow', 'Self-Check')
HERO        = ds.get('hero', TITLE)
SUBJECT     = ds.get('subject', '')          # e.g. "FortiGate Operator"
SOURCE_DESC = ds.get('source_desc', 'the source material')
OUT_HTML    = ds.get('out_html', 'quiz.html')
OUT_MD      = ds.get('out_md', 'quiz-question-bank.md')
SUBJ_SP     = (' ' + SUBJECT + ' ') if SUBJECT else ' '

def lesson_color(i):
    return {1:'var(--accent)', 2:'#2E7DE9', 3:'#12A594', 4:'#D08018', 5:'#8B5CF6',
            6:'#0EA5E9', 7:'#DB2777', 8:'#65A30D'}.get(i, '#6B7280')

lesson_css=[]
for L in lessons:
    i=L['id']; c=lesson_color(i)
    lesson_css.append(f".lesson-card.l{i} .lnum{{color:{c}}}")
    lesson_css.append(f".lesson-card.l{i} li::before{{background:{c}}}")
    lesson_css.append(f".qhead .eyebrow .lt.l{i}{{color:{c}}}")
    lesson_css.append(f".lesson-banner.l{i} .lb-tag{{color:{c}}}")
    lesson_css.append(f".sq.l{i} .sqq .n{{color:{c}}}")
LESSONCSS="\n".join(lesson_css)

QJSON=json.dumps(combined, ensure_ascii=False)
LJSON=json.dumps(lessons, ensure_ascii=False)
NQ=len(combined); NL=len(lessons)

template = r'''<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
:root{
  --bg:#E9ECEF; --surface:#FFFFFF; --surface-2:#F3F5F7; --surface-3:#EAEEF2;
  --ink:#14181D; --muted:#59636E; --faint:#8A939D; --border:#D8DDE3;
  --accent:#E4002B; --accent-2:#B00722;
  --ok:#0B8A54; --ok-tint:#E6F4EC; --ok-border:#9BD3B4;
  --bad:#C8102E; --bad-tint:#FBE9EC; --bad-border:#E9A9B4;
  --btn-bg:#14181D; --btn-fg:#FFFFFF; --btn-bg-hover:#000000;
  --focus:#1668E3; --chip:#EDF0F3;
  --shadow:0 1px 2px rgba(20,24,29,.06), 0 8px 24px rgba(20,24,29,.07);
  --shadow-sm:0 1px 2px rgba(20,24,29,.08);
}
:root:not([data-theme="light"]){
  @media (prefers-color-scheme: dark){
    --bg:#0F1317; --surface:#171C22; --surface-2:#1E252C; --surface-3:#252E37;
    --ink:#E7ECF1; --muted:#93A0AD; --faint:#6B7783; --border:#2A333C;
    --accent:#FF3B4E; --accent-2:#FF6472;
    --ok:#35D08A; --ok-tint:#12251C; --ok-border:#1F6B47;
    --bad:#FF6472; --bad-tint:#2A1519; --bad-border:#7A2733;
    --btn-bg:#EAEEF2; --btn-fg:#14181D; --btn-bg-hover:#FFFFFF;
    --focus:#5AA0FF; --chip:#222A32;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 12px 32px rgba(0,0,0,.45);
    --shadow-sm:0 1px 2px rgba(0,0,0,.4);
  }
}
:root[data-theme="dark"]{
  --bg:#0F1317; --surface:#171C22; --surface-2:#1E252C; --surface-3:#252E37;
  --ink:#E7ECF1; --muted:#93A0AD; --faint:#6B7783; --border:#2A333C;
  --accent:#FF3B4E; --accent-2:#FF6472;
  --ok:#35D08A; --ok-tint:#12251C; --ok-border:#1F6B47;
  --bad:#FF6472; --bad-tint:#2A1519; --bad-border:#7A2733;
  --btn-bg:#EAEEF2; --btn-fg:#14181D; --btn-bg-hover:#FFFFFF;
  --focus:#5AA0FF; --chip:#222A32;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 12px 32px rgba(0,0,0,.45);
  --shadow-sm:0 1px 2px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0; background:var(--bg); color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased}
.mono{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace}
h1,h2,h3{font-family:"Archivo",system-ui,sans-serif; margin:0; line-height:1.15; text-wrap:balance}
a{color:var(--accent)}
button{font-family:inherit}

.bar{position:sticky; top:0; z-index:20; background:var(--surface); border-bottom:2px solid var(--accent); box-shadow:var(--shadow-sm)}
.bar-in{max-width:900px; margin:0 auto; padding:11px 20px; display:flex; align-items:center; gap:14px}
.brand{display:flex; align-items:center; gap:10px; min-width:0}
.mark{width:20px; height:20px; border-radius:4px; background:var(--accent); flex:none; box-shadow:inset 0 0 0 3px rgba(255,255,255,.35)}
.brand b{font-family:"Archivo"; font-weight:800; font-size:15px; letter-spacing:-.01em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
.brand span{color:var(--faint); font-size:11px; letter-spacing:.12em; text-transform:uppercase}
.bar-spacer{flex:1}
.readout{font-size:12px; color:var(--muted); display:flex; gap:14px; align-items:center}
.readout b{color:var(--ink); font-weight:600}
.iconbtn{background:transparent; border:1px solid var(--border); color:var(--muted); width:34px; height:34px; border-radius:8px; cursor:pointer; font-size:15px; display:grid; place-items:center; transition:.15s}
.iconbtn:hover{color:var(--ink); border-color:var(--faint)}

main{max-width:900px; margin:0 auto; padding:28px 20px 80px}
.eyebrow{font-family:"IBM Plex Mono"; font-size:11.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); font-weight:600}
.card{background:var(--surface); border:1px solid var(--border); border-radius:16px; box-shadow:var(--shadow)}

.hero{padding:40px 34px 34px}
.hero h1{font-size:clamp(30px,5vw,44px); font-weight:800; letter-spacing:-.02em; margin-top:14px}
.hero .lede{color:var(--muted); font-size:17px; max-width:62ch; margin:16px 0 0}
.pillrow{display:flex; flex-wrap:wrap; gap:8px; margin-top:22px}
.pill{font-family:"IBM Plex Mono"; font-size:12px; padding:6px 11px; border-radius:999px; background:var(--chip); color:var(--muted); border:1px solid var(--border)}
.pill b{color:var(--ink)}

.lessons{display:grid; grid-template-columns:repeat(auto-fit,minmax(288px,1fr)); gap:16px; margin-top:26px}
.lesson-card{border:1px solid var(--border); border-radius:14px; background:var(--surface-2); padding:20px 20px 22px; display:flex; flex-direction:column}
.lesson-card .lnum{font-family:"IBM Plex Mono"; font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--faint); font-weight:600}
.lesson-card h3{font-size:18px; font-weight:700; margin:7px 0 0; letter-spacing:-.01em}
.lesson-card .lc-count{font-family:"IBM Plex Mono"; font-size:12px; color:var(--muted); margin-top:4px}
.lesson-card ul{margin:14px 0 0; padding:0; list-style:none; display:grid; gap:7px}
.lesson-card li{position:relative; padding-left:20px; font-size:12.5px; color:var(--ink); line-height:1.4}
.lesson-card li::before{content:""; position:absolute; left:2px; top:7px; width:7px; height:7px; border-radius:2px}
.lesson-card .lc-btn{margin-top:auto; padding-top:18px}
.lesson-card button{width:100%; appearance:none; border:1px solid var(--border); background:var(--surface); color:var(--ink); border-radius:10px; padding:11px 16px; font-size:14px; font-weight:600; cursor:pointer; transition:.15s}
.lesson-card button:hover{border-color:var(--faint); background:var(--surface-3)}
.lesson-card button:focus-visible{outline:2px solid var(--focus); outline-offset:2px}

.toggles{display:flex; flex-wrap:wrap; gap:10px 22px; margin-top:26px; padding-top:22px; border-top:1px solid var(--border)}
.tog{display:flex; align-items:center; gap:9px; font-size:14px; color:var(--muted); cursor:pointer; user-select:none}
.tog input{position:absolute; opacity:0; width:0; height:0}
.sw{width:38px; height:22px; border-radius:999px; background:var(--surface-3); border:1px solid var(--border); position:relative; transition:.18s; flex:none}
.sw::after{content:""; position:absolute; top:2px; left:2px; width:16px; height:16px; border-radius:50%; background:#fff; box-shadow:0 1px 2px rgba(0,0,0,.3); transition:.18s}
.tog input:checked + .sw{background:var(--accent); border-color:var(--accent)}
.tog input:checked + .sw::after{transform:translateX(16px)}
.tog input:focus-visible + .sw{outline:2px solid var(--focus); outline-offset:2px}
.actions{display:flex; flex-wrap:wrap; gap:12px; margin-top:26px}

.btn{appearance:none; border:1px solid transparent; border-radius:10px; padding:12px 22px; font-size:15px; font-weight:600; cursor:pointer; transition:.15s}
.btn-primary{background:var(--btn-bg); color:var(--btn-fg)}
.btn-primary:hover{background:var(--btn-bg-hover)}
.btn-ghost{background:transparent; color:var(--ink); border-color:var(--border)}
.btn-ghost:hover{border-color:var(--faint); background:var(--surface-2)}
.btn:focus-visible{outline:2px solid var(--focus); outline-offset:2px}
.btn:disabled{opacity:.45; cursor:default}

.qhead{display:flex; align-items:flex-start; justify-content:space-between; gap:16px; padding:22px 30px 0}
.qhead .eyebrow .lt{color:var(--faint)}
.diff{font-family:"IBM Plex Mono"; font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; padding:4px 9px; border-radius:6px; font-weight:600; white-space:nowrap; border:1px solid var(--border); color:var(--muted); background:var(--surface-2)}
.diff.easy{color:var(--ok); border-color:var(--ok-border); background:var(--ok-tint)}
.diff.hard{color:var(--accent); border-color:var(--border)}
.qtext{padding:14px 30px 4px; font-size:20px; font-weight:600; font-family:"Archivo"; letter-spacing:-.01em; line-height:1.32}
.opts{display:grid; gap:10px; padding:18px 30px 6px}
.opt{display:flex; align-items:flex-start; gap:13px; width:100%; text-align:left; background:var(--surface-2); border:1.5px solid var(--border); border-radius:11px; padding:13px 15px; cursor:pointer; transition:.13s; color:var(--ink); font-size:15.5px; line-height:1.45}
.opt:hover:not(:disabled){border-color:var(--faint); background:var(--surface-3)}
.opt:focus-visible{outline:2px solid var(--focus); outline-offset:2px}
.opt .lz{font-family:"IBM Plex Mono"; font-weight:600; font-size:13px; width:24px; height:24px; border-radius:6px; background:var(--surface); border:1px solid var(--border); display:grid; place-items:center; flex:none; color:var(--muted); margin-top:1px; transition:.13s}
.opt.sel{border-color:var(--ink); background:var(--surface-3)}
.opt.sel .lz{background:var(--ink); color:var(--surface); border-color:var(--ink)}
.opt.correct{border-color:var(--ok-border); background:var(--ok-tint)}
.opt.correct .lz{background:var(--ok); color:#fff; border-color:var(--ok)}
.opt.wrong{border-color:var(--bad-border); background:var(--bad-tint)}
.opt.wrong .lz{background:var(--bad); color:#fff; border-color:var(--bad)}
.opt:disabled{cursor:default}
.opt .otext{flex:1; min-width:0}
.opt .fmark{font-weight:700; font-size:15px; flex:none; margin-top:1px}
.opt.correct .fmark{color:var(--ok)}
.opt.wrong .fmark{color:var(--bad)}

.feedback{margin:8px 30px 0; border-radius:12px; padding:0; max-height:0; overflow:hidden; transition:max-height .28s ease, margin .28s ease}
.feedback.show{max-height:460px; margin:16px 30px 0}
.fb-in{padding:16px 18px; border-radius:12px; border:1px solid var(--border); background:var(--surface-2)}
.fb-in.ok{border-color:var(--ok-border); background:var(--ok-tint)}
.fb-in.no{border-color:var(--bad-border); background:var(--bad-tint)}
.fb-verdict{font-family:"Archivo"; font-weight:700; font-size:14px; display:flex; align-items:center; gap:8px; margin-bottom:6px}
.fb-in.ok .fb-verdict{color:var(--ok)}
.fb-in.no .fb-verdict{color:var(--bad)}
.fb-rat{font-size:14.5px; color:var(--ink)}
.fb-src{margin-top:10px; font-family:"IBM Plex Mono"; font-size:11.5px; color:var(--muted); display:flex; align-items:center; gap:7px; flex-wrap:wrap}
.fb-src .tag{border:1px solid var(--border); border-radius:5px; padding:2px 7px; background:var(--surface)}

.qfoot{display:flex; align-items:center; gap:16px; padding:20px 30px 24px; margin-top:8px}
.progress{flex:1; height:7px; border-radius:999px; background:var(--surface-3); overflow:hidden}
.progress > i{display:block; height:100%; width:0; background:var(--accent); border-radius:999px; transition:width .35s ease}
.foot-btns{display:flex; gap:10px}
.btn-sm{padding:10px 18px; font-size:14px}
.hint{font-family:"IBM Plex Mono"; font-size:11px; color:var(--faint); text-align:center; margin-top:16px}
.hint kbd{background:var(--surface); border:1px solid var(--border); border-bottom-width:2px; border-radius:5px; padding:1px 6px; font-size:11px; color:var(--muted)}

.score-wrap{padding:38px 34px 30px; text-align:center}
.score-ring{width:150px; height:150px; margin:6px auto 0; position:relative}
.score-ring svg{transform:rotate(-90deg)}
.score-ring .pct{position:absolute; inset:0; display:grid; place-items:center}
.score-ring .pct b{font-family:"Archivo"; font-weight:800; font-size:38px; letter-spacing:-.02em; display:block; line-height:1}
.score-ring .pct small{color:var(--muted); font-size:12px; font-family:"IBM Plex Mono"}
.verdict-line{font-family:"Archivo"; font-weight:700; font-size:22px; margin-top:18px}
.score-sub{color:var(--muted); margin-top:6px}
.tally{display:grid; gap:9px; padding:26px 34px; border-top:1px solid var(--border)}
.tally h3, .review h3{font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--faint); font-family:"IBM Plex Mono"; font-weight:600; margin-bottom:4px}
.tally .lesson-head{font-family:"Archivo"; font-weight:700; font-size:14px; color:var(--ink); margin-top:10px}
.trow{display:grid; grid-template-columns:1fr auto; gap:6px 12px; align-items:center}
.trow .tn{font-size:13.5px; color:var(--ink)}
.trow .tv{font-family:"IBM Plex Mono"; font-size:12.5px; color:var(--muted); font-variant-numeric:tabular-nums}
.tbar{grid-column:1/-1; height:6px; border-radius:999px; background:var(--surface-3); overflow:hidden}
.tbar > i{display:block; height:100%; border-radius:999px}
.review{padding:8px 34px 30px}
.miss{border:1px solid var(--border); border-radius:11px; padding:14px 16px; margin-top:12px; background:var(--surface-2)}
.miss .mq{font-weight:600; font-size:14.5px; margin-bottom:9px}
.miss .ml{font-size:13.5px; display:flex; gap:8px; align-items:baseline; margin-top:3px}
.miss .ml .k{font-family:"IBM Plex Mono"; font-size:11px; font-weight:600; padding:1px 6px; border-radius:4px; flex:none}
.miss .k.ok{background:var(--ok-tint); color:var(--ok); border:1px solid var(--ok-border)}
.miss .k.no{background:var(--bad-tint); color:var(--bad); border:1px solid var(--bad-border)}
.miss .msrc{font-family:"IBM Plex Mono"; font-size:11px; color:var(--faint); margin-top:9px}
.end-actions{display:flex; gap:12px; justify-content:center; padding:6px 34px 4px; flex-wrap:wrap}

.filters{display:flex; flex-wrap:wrap; gap:8px; margin-bottom:22px}
.fchip{font-family:"IBM Plex Mono"; font-size:12px; padding:7px 13px; border-radius:999px; border:1px solid var(--border); background:var(--surface); color:var(--muted); cursor:pointer; transition:.13s}
.fchip:hover{border-color:var(--faint); color:var(--ink)}
.fchip.on{background:var(--ink); color:var(--surface); border-color:var(--ink)}
.fchip:focus-visible{outline:2px solid var(--focus); outline-offset:2px}
.lesson-banner{display:flex; align-items:baseline; gap:12px; margin:26px 0 14px; padding-bottom:10px; border-bottom:2px solid var(--border)}
.lesson-banner .lb-tag{font-family:"IBM Plex Mono"; font-size:11px; font-weight:600; letter-spacing:.1em; text-transform:uppercase}
.lesson-banner h2{font-family:"Archivo"; font-size:20px; font-weight:700}
.sgroup{margin-bottom:12px}
.sgroup > summary{cursor:pointer; list-style:none; padding:15px 20px; background:var(--surface); border:1px solid var(--border); border-radius:12px; display:flex; align-items:center; gap:12px; font-family:"Archivo"; font-weight:700; font-size:15.5px}
.sgroup > summary::-webkit-details-marker{display:none}
.sgroup > summary .cnt{margin-left:auto; font-family:"IBM Plex Mono"; font-size:12px; color:var(--muted); font-weight:400}
.sgroup > summary .caret{color:var(--faint); transition:.2s; font-size:13px}
.sgroup[open] > summary .caret{transform:rotate(90deg)}
.sgroup[open] > summary{border-radius:12px 12px 0 0; border-bottom-color:transparent}
.sbody{border:1px solid var(--border); border-top:none; border-radius:0 0 12px 12px; padding:6px 20px 8px}
.sq{padding:18px 0; border-bottom:1px solid var(--border)}
.sq:last-child{border-bottom:none}
.sq .sqq{font-weight:600; font-size:15.5px; display:flex; gap:10px}
.sq .sqq .n{font-family:"IBM Plex Mono"; color:var(--accent); font-weight:600; flex:none}
.sopts{display:grid; gap:6px; margin:12px 0 0}
.sopt{display:flex; gap:11px; align-items:flex-start; padding:9px 12px; border-radius:9px; font-size:14.5px; border:1px solid transparent}
.sopt .sl{font-family:"IBM Plex Mono"; font-size:12px; color:var(--muted); flex:none; width:18px}
.sopt.ok{background:var(--ok-tint); border-color:var(--ok-border)}
.sopt.ok .sl{color:var(--ok); font-weight:600}
.sopt.ok .ck{color:var(--ok); margin-left:auto; font-weight:700}
.srat{margin-top:12px; font-size:14px; color:var(--muted); border-left:2px solid var(--border); padding-left:12px}
.ssrc{margin-top:9px; font-family:"IBM Plex Mono"; font-size:11px; color:var(--faint)}
.foot-note{text-align:center; color:var(--faint); font-size:12px; margin-top:40px; font-family:"IBM Plex Mono"; line-height:1.7}
__LESSONCSS__

@media (max-width:640px){
  .hero{padding:30px 22px 26px}
  .qhead,.qtext,.opts,.qfoot,.feedback.show{padding-left:20px; padding-right:20px}
  .feedback.show{margin-left:20px; margin-right:20px}
  .score-wrap,.tally,.review,.end-actions{padding-left:22px; padding-right:22px}
  .brand span{display:none}
  .readout .rd-sec{display:none}
}
@media (prefers-reduced-motion:reduce){*{transition:none !important; animation:none !important}}
.fade{animation:fade .3s ease}
@keyframes fade{from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none}}
</style>

<div class="bar">
  <div class="bar-in">
    <div class="brand"><div class="mark"></div><div style="min-width:0"><b>__BRAND__</b></div><span>__BRAND_TAG__</span></div>
    <div class="bar-spacer"></div>
    <div class="readout" id="readout"></div>
    <button class="iconbtn" id="themeBtn" title="Toggle theme" aria-label="Toggle light/dark theme">◐</button>
  </div>
</div>
<main id="app"></main>
<div class="foot-note">__FOOT__</div>

<script>
const LESSONS = __LESSONS__;
const QUESTIONS = __QUESTIONS__;
const LETTERS = ["A","B","C","D"];
const lessonById = id => LESSONS.find(l=>l.id===id);

const root = document.documentElement;
document.getElementById("themeBtn").addEventListener("click", ()=>{
  const t=root.getAttribute("data-theme");
  const dark = t==="dark" || (!t && window.matchMedia("(prefers-color-scheme: dark)").matches);
  root.setAttribute("data-theme", dark ? "light" : "dark");
});

let S = { mode:"start", scope:"all", shuffleQ:true, shuffleOpts:true, order:[], optMap:{}, ptr:0, picked:null, checked:false, answers:{}, studyFilter:"all" };
const app = document.getElementById("app");
const readout = document.getElementById("readout");
function shuffle(a){ a=a.slice(); for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]];} return a; }
function esc(s){ return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function scopeIdx(scope){ return QUESTIONS.map((q,i)=>i).filter(i => scope==="all" || QUESTIONS[i].lesson===scope); }

function renderStart(){
  S.mode="start";
  const diffs={easy:0,medium:0,hard:0}; QUESTIONS.forEach(q=>diffs[q.diff]++);
  app.innerHTML = `
  <div class="card hero fade">
    <div class="eyebrow">__EYEBROW__</div>
    <h1>__HERO__</h1>
    <p class="lede">${QUESTIONS.length} multiple-choice questions across ${LESSONS.length}__SUBJ_SP__lessons, pulled straight from __SOURCE_DESC__. Drill any single lesson, or take the full exam.</p>
    <div class="pillrow">
      <span class="pill"><b>${QUESTIONS.length}</b> questions</span>
      <span class="pill"><b>${LESSONS.length}</b> lessons</span>
      <span class="pill"><b>${diffs.easy}</b> easy · <b>${diffs.medium}</b> medium · <b>${diffs.hard}</b> hard</span>
      <span class="pill">4 options each</span>
    </div>
    <div class="lessons">
      ${LESSONS.map(L=>{
        const c=QUESTIONS.filter(q=>q.lesson===L.id).length;
        return `<div class="lesson-card l${L.id}">
          <div class="lnum">Lesson ${L.id}</div>
          <h3>${esc(L.name)}</h3>
          <div class="lc-count">${c} questions · ${L.sections.length} sections</div>
          <ul>${L.objectives.map(o=>`<li>${esc(o)}</li>`).join("")}</ul>
          <div class="lc-btn"><button data-scope="${L.id}">Quiz this lesson →</button></div>
        </div>`;
      }).join("")}
    </div>
    <div class="toggles">
      <label class="tog"><input type="checkbox" id="tqo" ${S.shuffleQ?"checked":""}><span class="sw"></span>Shuffle question order</label>
      <label class="tog"><input type="checkbox" id="too" ${S.shuffleOpts?"checked":""}><span class="sw"></span>Shuffle answer choices</label>
    </div>
    <div class="actions">
      <button class="btn btn-primary" id="startAll">Take the full exam (${QUESTIONS.length}) →</button>
      <button class="btn btn-ghost" id="startStudy">Study mode — read all answers</button>
    </div>
  </div>`;
  document.getElementById("tqo").addEventListener("change",e=>S.shuffleQ=e.target.checked);
  document.getElementById("too").addEventListener("change",e=>S.shuffleOpts=e.target.checked);
  document.getElementById("startAll").addEventListener("click", ()=>beginQuiz("all"));
  document.getElementById("startStudy").addEventListener("click", ()=>renderStudy());
  [...document.querySelectorAll(".lesson-card button")].forEach(b=>b.addEventListener("click",()=>beginQuiz(+b.dataset.scope)));
  readout.innerHTML="";
}

function beginQuiz(scope){
  S.scope=scope;
  const pool=scopeIdx(scope);
  S.order = S.shuffleQ ? shuffle(pool) : pool;
  S.optMap={};
  S.order.forEach(i=>{ const q=QUESTIONS[i]; const slots=q.opts.map((_,k)=>k); S.optMap[q.n]=S.shuffleOpts?shuffle(slots):slots; });
  S.ptr=0; S.answers={}; S.picked=null; S.checked=false; S.mode="quiz";
  renderQuiz();
}

function renderQuiz(){
  const q=QUESTIONS[S.order[S.ptr]]; const L=lessonById(q.lesson); const map=S.optMap[q.n]; const answered=S.answers[q.n];
  S.checked=!!answered; S.picked=answered?map.indexOf(answered.pickOrig):null;
  app.innerHTML=`
  <div class="card fade">
    <div class="qhead">
      <div class="eyebrow"><span class="lt l${q.lesson}">L${q.lesson} ${esc(L.short)}</span> · ${esc(q.section)}</div>
      <div class="diff ${q.diff}">${q.diff}</div>
    </div>
    <div class="qtext">${esc(q.q)}</div>
    <div class="opts">
      ${map.map((orig,slot)=>`<button class="opt" data-slot="${slot}" data-orig="${orig}"><span class="lz">${LETTERS[slot]}</span><span class="otext">${esc(q.opts[orig])}</span><span class="fmark" aria-hidden="true"></span></button>`).join("")}
    </div>
    <div class="feedback" id="fb"></div>
    <div class="qfoot"><div class="progress"><i style="width:${(S.ptr/S.order.length)*100}%"></i></div><div class="foot-btns" id="footBtns"></div></div>
  </div>
  <div class="hint">Keys: <kbd>A</kbd><kbd>B</kbd><kbd>C</kbd><kbd>D</kbd> or <kbd>1</kbd>–<kbd>4</kbd> to choose · <kbd>Enter</kbd> to ${answered?"continue":"check"}</div>`;
  const optEls=[...app.querySelectorAll(".opt")];
  optEls.forEach(el=>el.addEventListener("click",()=>{ if(S.checked) return; S.picked=+el.dataset.slot; optEls.forEach(o=>o.classList.toggle("sel",o===el)); updateFootBtns(); }));
  if(answered) revealAnswer(q,map);
  updateReadout(); updateFootBtns();
}
function updateFootBtns(){
  const fb=document.getElementById("footBtns"); if(!fb) return;
  const last=S.ptr===S.order.length-1;
  if(S.checked){ fb.innerHTML=`<button class="btn btn-primary btn-sm" id="nextBtn">${last?"See results":"Next"} →</button>`; document.getElementById("nextBtn").addEventListener("click", nextQ); }
  else { fb.innerHTML=`<button class="btn btn-ghost btn-sm" id="skipBtn">Skip</button><button class="btn btn-primary btn-sm" id="checkBtn" ${S.picked===null?"disabled":""}>Check answer</button>`;
    document.getElementById("skipBtn").addEventListener("click",()=>{recordSkip();nextQ();}); const cb=document.getElementById("checkBtn"); if(cb) cb.addEventListener("click", checkAnswer); }
}
function checkAnswer(){ if(S.picked===null||S.checked) return; const q=QUESTIONS[S.order[S.ptr]]; const map=S.optMap[q.n]; const pickOrig=map[S.picked]; S.answers[q.n]={correct:pickOrig===q.a, pickOrig}; S.checked=true; revealAnswer(q,map); updateReadout(); updateFootBtns(); }
function recordSkip(){ const q=QUESTIONS[S.order[S.ptr]]; if(!S.answers[q.n]) S.answers[q.n]={correct:false,pickOrig:null,skipped:true}; }
function revealAnswer(q,map){
  const optEls=[...app.querySelectorAll(".opt")]; const ans=S.answers[q.n];
  optEls.forEach(el=>{ el.disabled=true; el.classList.remove("sel"); const orig=+el.dataset.orig; const fm=el.querySelector(".fmark");
    if(orig===q.a){el.classList.add("correct"); fm.textContent="✓";} else if(ans&&orig===ans.pickOrig){el.classList.add("wrong"); fm.textContent="✗";} });
  const good=ans&&ans.correct; const fb=document.getElementById("fb"); const verdict=ans&&ans.skipped?"Skipped":(good?"Correct":"Not quite");
  fb.innerHTML=`<div class="fb-in ${good?"ok":"no"}"><div class="fb-verdict">${good?"✓":"✗"} ${verdict}${good?"":" — answer "+LETTERS[map.indexOf(q.a)]}</div><div class="fb-rat">${esc(q.rat)}</div><div class="fb-src"><span class="tag">Source</span> ${esc(q.src)} · <span>${esc(q.topic)}</span></div></div>`;
  requestAnimationFrame(()=>fb.classList.add("show"));
}
function nextQ(){ if(S.ptr===S.order.length-1){renderEnd();return;} S.ptr++; S.picked=null; S.checked=false; renderQuiz(); }
function updateReadout(){ const done=Object.keys(S.answers).length; const correct=Object.values(S.answers).filter(a=>a.correct).length; readout.innerHTML=`<span class="rd-sec">Question <b>${S.ptr+1}</b>/${S.order.length}</span><span>Score <b>${correct}</b>/${done}</span>`; }

function renderEnd(){
  S.mode="end";
  const scoped=S.order.map(i=>QUESTIONS[i]); const total=scoped.length;
  const correct=scoped.filter(q=>S.answers[q.n]&&S.answers[q.n].correct).length; const pct=Math.round(correct/total*100);
  const circ=2*Math.PI*66; const dash=circ*(pct/100); const col=pct>=80?"var(--ok)":pct>=60?"var(--accent)":"var(--bad)";
  const verdict=pct>=90?"Outstanding":pct>=80?"Strong pass":pct>=60?"Getting there":"Keep studying";
  const scopeLabel=S.scope==="all"?"Full exam":("Lesson "+S.scope+" · "+lessonById(S.scope).short);
  const lessonsInScope=S.scope==="all"?LESSONS:[lessonById(S.scope)];
  let tallyHtml="";
  lessonsInScope.forEach(L=>{
    const rows=L.sections.map(s=>{ const items=scoped.filter(q=>q.lesson===L.id&&q.section===s); if(!items.length) return "";
      const c=items.filter(q=>S.answers[q.n]&&S.answers[q.n].correct).length; const p=Math.round(c/items.length*100);
      const bc=p>=80?"var(--ok)":p>=50?"var(--accent)":"var(--bad)";
      return `<div class="trow"><span class="tn">${esc(s)}</span><span class="tv">${c}/${items.length}</span><span class="tbar"><i style="width:${p}%; background:${bc}"></i></span></div>`; }).join("");
    if(rows) tallyHtml+=`<div class="lesson-head">Lesson ${L.id} · ${esc(L.name)}</div>${rows}`;
  });
  const missed=scoped.filter(q=>!(S.answers[q.n]&&S.answers[q.n].correct));
  app.innerHTML=`
  <div class="card fade">
    <div class="score-wrap"><div class="eyebrow">${esc(scopeLabel)} · complete</div>
      <div class="score-ring"><svg width="150" height="150" viewBox="0 0 150 150"><circle cx="75" cy="75" r="66" fill="none" stroke="var(--surface-3)" stroke-width="11"></circle><circle cx="75" cy="75" r="66" fill="none" stroke="${col}" stroke-width="11" stroke-linecap="round" stroke-dasharray="${dash} ${circ}"></circle></svg><div class="pct"><div><b>${pct}%</b><small>${correct}/${total}</small></div></div></div>
      <div class="verdict-line">${verdict}</div><div class="score-sub">You answered ${correct} of ${total} correctly.</div></div>
    <div class="tally"><h3>By section</h3>${tallyHtml}</div>
    ${missed.length?`<div class="review"><h3>Review — ${missed.length} to revisit</h3>${missed.map(q=>{ const ans=S.answers[q.n];
      const yours=ans&&ans.pickOrig!=null?`<div class="ml"><span class="k no">Your pick</span><span>${esc(q.opts[ans.pickOrig])}</span></div>`:`<div class="ml"><span class="k no">Skipped</span><span>no answer given</span></div>`;
      return `<div class="miss"><div class="mq">${esc(q.q)}</div><div class="ml"><span class="k ok">Correct</span><span>${esc(q.opts[q.a])}</span></div>${yours}<div class="msrc">${esc(q.rat)}<br>Source: ${esc(q.src)}</div></div>`; }).join("")}</div>`:`<div class="review"><h3>Perfect run</h3><p style="color:var(--muted)">Every question correct — nothing to review.</p></div>`}
    <div class="end-actions"><button class="btn btn-primary" id="again">Retake</button><button class="btn btn-ghost" id="toStudy">Study mode</button><button class="btn btn-ghost" id="home">Home</button></div>
    <div style="height:26px"></div>
  </div>`;
  document.getElementById("again").addEventListener("click",()=>beginQuiz(S.scope));
  document.getElementById("toStudy").addEventListener("click",()=>renderStudy());
  document.getElementById("home").addEventListener("click", renderStart);
  readout.innerHTML=`<span>Final <b>${pct}%</b></span>`; window.scrollTo({top:0,behavior:"smooth"});
}

function renderStudy(){
  S.mode="study";
  const shown=S.studyFilter==="all"?LESSONS:LESSONS.filter(l=>l.id===S.studyFilter);
  app.innerHTML=`
    <div class="card hero fade" style="padding:30px 30px 26px; margin-bottom:22px">
      <div class="eyebrow">Study mode</div><h1 style="font-size:26px; margin-top:10px">Every question, answered</h1>
      <p class="lede" style="font-size:15px">All ${QUESTIONS.length} questions with the correct choice marked, the reasoning, and the exact source it came from.</p>
    </div>
    <div class="filters" id="filters">
      <button class="fchip ${S.studyFilter==="all"?"on":""}" data-f="all">All lessons (${QUESTIONS.length})</button>
      ${LESSONS.map(L=>`<button class="fchip ${S.studyFilter===L.id?"on":""}" data-f="${L.id}">L${L.id} · ${esc(L.short)} (${QUESTIONS.filter(q=>q.lesson===L.id).length})</button>`).join("")}
    </div>
    <div id="studyList"></div>
    <div class="actions" style="margin-top:24px"><button class="btn btn-primary" id="toQuiz">Take the full exam →</button><button class="btn btn-ghost" id="home2">Home</button></div>`;
  document.getElementById("studyList").innerHTML=shown.map(L=>{
    const secBlocks=L.sections.map(s=>{ const items=QUESTIONS.filter(q=>q.lesson===L.id&&q.section===s); if(!items.length) return "";
      return `<details class="sgroup" open><summary><span class="caret">▶</span>${esc(s)}<span class="cnt">${items.length} question${items.length>1?"s":""}</span></summary>
        <div class="sbody">${items.map(q=>`<div class="sq l${q.lesson}"><div class="sqq"><span class="n">${q.ln}</span><span>${esc(q.q)}</span></div>
          <div class="sopts">${q.opts.map((o,i)=>`<div class="sopt ${i===q.a?"ok":""}"><span class="sl">${LETTERS[i]}</span><span>${esc(o)}</span>${i===q.a?'<span class="ck">✓</span>':""}</div>`).join("")}</div>
          <div class="srat">${esc(q.rat)}</div><div class="ssrc">Source: ${esc(q.src)} · ${esc(q.topic)} · ${q.diff}</div></div>`).join("")}</div></details>`;
    }).join("");
    return `<div class="lesson-banner l${L.id}"><span class="lb-tag">Lesson ${L.id}</span><h2>${esc(L.name)}</h2></div>${secBlocks}`;
  }).join("");
  [...document.querySelectorAll("#filters .fchip")].forEach(c=>c.addEventListener("click",()=>{ S.studyFilter=c.dataset.f==="all"?"all":+c.dataset.f; renderStudy(); window.scrollTo({top:0,behavior:"smooth"}); }));
  document.getElementById("toQuiz").addEventListener("click",()=>beginQuiz("all"));
  document.getElementById("home2").addEventListener("click", renderStart);
  readout.innerHTML=`<span>Study · <b>${QUESTIONS.length}</b> Q</span>`;
}

document.addEventListener("keydown",e=>{
  if(S.mode!=="quiz") return;
  const k=e.key.toLowerCase(); const q=QUESTIONS[S.order[S.ptr]]; const n=S.optMap[q.n].length; let slot=-1;
  if(["a","b","c","d"].includes(k)) slot="abcd".indexOf(k); else if(["1","2","3","4"].includes(k)) slot=+k-1;
  if(slot>=0&&slot<n&&!S.checked){ S.picked=slot; [...app.querySelectorAll(".opt")].forEach(o=>o.classList.toggle("sel",+o.dataset.slot===slot)); updateFootBtns(); e.preventDefault(); return; }
  if(e.key==="Enter"){ if(!S.checked&&S.picked!==null) checkAnswer(); else if(S.checked) nextQ(); e.preventDefault(); }
});
renderStart();
</script>'''

foot = ds.get('foot', f"{NQ} questions across {NL} lessons · Self-check study aid · answers grounded in {SOURCE_DESC}")
html = (template
    .replace("__LESSONCSS__", LESSONCSS)
    .replace("__TITLE__", TITLE).replace("__BRAND__", BRAND).replace("__BRAND_TAG__", BRAND_TAG)
    .replace("__EYEBROW__", EYEBROW).replace("__HERO__", HERO)
    .replace("__SUBJ_SP__", SUBJ_SP).replace("__SOURCE_DESC__", SOURCE_DESC)
    .replace("__FOOT__", foot)
    .replace("__LESSONS__", LJSON).replace("__QUESTIONS__", QJSON))
open(OUT_HTML,"w",encoding="utf-8",newline="\n").write(html)
print("wrote HTML", OUT_HTML, len(html), "bytes;", NQ, "questions,", NL, "lessons")

# markdown bank
L=['A','B','C','D']; md=[]
md.append(f"# {TITLE}"); md.append("")
md.append(f"**{NQ} multiple-choice questions (four options each) across {NL} lessons.**  ")
md.append(f"Built from {SOURCE_DESC}. Each answer cites its exact source."); md.append("")
for Lz in lessons:
    qs=[q for q in combined if q['lesson']==Lz['id']]
    md.append(f"- **Lesson {Lz['id']} — {Lz['name']}** ({len(qs)} questions)")
md.append("")
for Lz in lessons:
    md.append("---"); md.append(""); md.append(f"# Lesson {Lz['id']} — {Lz['name']}"); md.append("")
    md.append("**Objectives:** " + "; ".join(Lz['objectives']) + "."); md.append("")
    qs=[q for q in combined if q['lesson']==Lz['id']]
    md.append("## Questions"); md.append("")
    for s in Lz['sections']:
        items=[q for q in qs if q['section']==s]
        if not items: continue
        md.append(f"### {s}"); md.append("")
        for q in items:
            md.append(f"**{q['ln']}. {q['q']}**"); md.append("")
            for i,o in enumerate(q['opts']): md.append(f"- {L[i]}. {o}")
            md.append("")
    md.append("## Answer key"); md.append("")
    for q in qs:
        md.append(f"**{q['ln']}. {L[q['a']]}** — {q['opts'][q['a']]}  ")
        md.append(f"{q['rat']}  ")
        md.append(f"*(Topic: {q['topic']} · Difficulty: {q['diff'].capitalize()} · Source: {q['src']})*"); md.append("")
open(OUT_MD,"w",encoding="utf-8",newline="\n").write("\n".join(md))
print("wrote markdown", OUT_MD, len(md), "lines")
