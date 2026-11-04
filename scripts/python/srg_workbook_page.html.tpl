<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FortiSwitch SRG Crosswalk — 2048F and 648F-FPOE on FortiSwitchOS 7.6.7</title>
<style>
  :root{
    --bg:#f6f8fa; --panel:#ffffff; --ink:#152230; --muted:#5b6b7a;
    --line:#e2e8ee; --line-strong:#cdd8e2;
    --accent:#0b7a86; --accent-ink:#075a63; --accent-bg:#e3f2f4;
    --ok:#2f855a; --ok-bg:#e8f4ec; --warn:#9a6a12; --warn-bg:#f6efdf; --bad:#b0392f; --bad-bg:#f8e9e7;
    --shadow:0 1px 2px rgba(21,34,48,.06),0 6px 18px rgba(21,34,48,.05);
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0e161e; --panel:#152230; --ink:#e7eef4; --muted:#95a7b6;
      --line:#24333f; --line-strong:#32444f;
      --accent:#3cc6d4; --accent-ink:#7fe0ea; --accent-bg:#10303a;
      --ok:#5bc98b; --ok-bg:#123023; --warn:#e0b25a; --warn-bg:#33280f; --bad:#f08a80; --bad-bg:#3a1c19;
      --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.28);
    }
  }
  :root[data-theme="light"]{
    --bg:#f6f8fa; --panel:#ffffff; --ink:#152230; --muted:#5b6b7a;
    --line:#e2e8ee; --line-strong:#cdd8e2;
    --accent:#0b7a86; --accent-ink:#075a63; --accent-bg:#e3f2f4;
    --ok:#2f855a; --ok-bg:#e8f4ec; --warn:#9a6a12; --warn-bg:#f6efdf; --bad:#b0392f; --bad-bg:#f8e9e7;
    --shadow:0 1px 2px rgba(21,34,48,.06),0 6px 18px rgba(21,34,48,.05);
  }
  :root[data-theme="dark"]{
    --bg:#0e161e; --panel:#152230; --ink:#e7eef4; --muted:#95a7b6;
    --line:#24333f; --line-strong:#32444f;
    --accent:#3cc6d4; --accent-ink:#7fe0ea; --accent-bg:#10303a;
    --ok:#5bc98b; --ok-bg:#123023; --warn:#e0b25a; --warn-bg:#33280f; --bad:#f08a80; --bad-bg:#3a1c19;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.28);
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1500px;margin:0 auto;padding:36px 24px 72px}
  header.hd{display:flex;flex-direction:column;gap:6px;margin-bottom:22px;position:relative}
  .eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-ink);font-weight:700}
  h1{font-size:clamp(24px,3.6vw,36px);line-height:1.12;margin:2px 0 0;font-weight:800;letter-spacing:-.02em;text-wrap:balance}
  .sub{color:var(--muted);font-size:15px;max-width:90ch}
  .sub a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}
  .sub a:hover{border-bottom-color:var(--accent)}
  #themeBtn{position:absolute;top:0;right:0;border:1px solid var(--line-strong);background:var(--panel);color:var(--ink);border-radius:8px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}

  .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 22px}
  @media(max-width:720px){.stats{grid-template-columns:repeat(2,1fr)}}
  .stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px;box-shadow:var(--shadow)}
  .stat .n{font-size:26px;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
  .stat .l{font-size:12.5px;color:var(--muted);margin-top:2px}

  .tabs{display:flex;gap:6px;border-bottom:1px solid var(--line-strong);margin-bottom:16px;flex-wrap:wrap}
  .tabs button{border:1px solid transparent;border-bottom:0;background:transparent;color:var(--muted);font:inherit;font-size:14px;font-weight:600;padding:9px 16px;cursor:pointer;border-radius:10px 10px 0 0}
  .tabs button[aria-selected="true"]{background:var(--panel);color:var(--accent-ink);border-color:var(--line-strong);margin-bottom:-1px}
  .tabs button:focus-visible,.btn:focus-visible,select:focus-visible,input:focus-visible,.tg:focus-visible,th button:focus-visible{outline:2px solid var(--accent);outline-offset:1px}

  .controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px}
  .search{flex:1 1 280px;min-width:220px}
  .search input,.controls select{border:1px solid var(--line-strong);border-radius:10px;background:var(--panel);color:var(--ink);font:inherit;font-size:14px;padding:9px 12px;box-shadow:var(--shadow)}
  .search input{width:100%}
  .controls label.chk{font-size:13.5px;color:var(--muted);display:inline-flex;gap:6px;align-items:center}
  .btn{border:1px solid var(--line-strong);background:var(--panel);color:var(--ink);font:inherit;font-size:13.5px;font-weight:600;padding:8px 13px;border-radius:10px;cursor:pointer;box-shadow:var(--shadow);text-decoration:none;display:inline-block}
  .btn:hover{border-color:var(--accent);color:var(--accent-ink)}
  details.cols{position:relative}
  details.cols summary{list-style:none}
  details.cols summary::-webkit-details-marker{display:none}
  details.cols .menu{position:absolute;z-index:5;top:110%;left:0;background:var(--panel);border:1px solid var(--line-strong);border-radius:10px;box-shadow:var(--shadow);padding:10px 14px;display:grid;gap:4px;max-height:360px;overflow:auto;min-width:230px}
  details.cols .menu label{font-size:13.5px;display:flex;gap:8px;align-items:center;white-space:nowrap}
  .count{font-size:13.5px;color:var(--muted);margin:6px 0 10px}

  .tablewrap{background:var(--panel);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);overflow:auto;max-height:78vh}
  table{border-collapse:separate;border-spacing:0;width:100%;font-size:13.5px}
  th,td{padding:8px 11px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
  thead th{position:sticky;top:0;z-index:2;background:var(--panel);border-bottom:1px solid var(--line-strong);white-space:nowrap;font-size:12.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
  th button{all:unset;cursor:pointer;display:inline-flex;gap:6px;align-items:center;font:inherit;color:inherit;text-transform:inherit;letter-spacing:inherit}
  th button .ar{font-size:10px;opacity:.5}
  th[aria-sort="ascending"] button .ar,th[aria-sort="descending"] button .ar{opacity:1;color:var(--accent)}
  tbody tr.data:hover td{background:var(--accent-bg)}
  td.tgc{width:34px;padding-right:0}
  .tg{all:unset;cursor:pointer;width:22px;height:22px;display:inline-grid;place-items:center;border:1px solid var(--line-strong);border-radius:6px;font-size:12px;color:var(--muted);background:var(--panel)}
  .tg[aria-expanded="true"]{color:var(--accent-ink);border-color:var(--accent)}
  td.wide{min-width:260px;max-width:460px}
  td.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;min-width:220px;max-width:420px;word-break:break-word}
  .pill{display:inline-block;border-radius:999px;padding:1px 9px;font-size:12px;font-weight:700;white-space:nowrap}
  .p1{background:var(--bad-bg);color:var(--bad)} .p2{background:var(--warn-bg);color:var(--warn)} .p3{background:var(--accent-bg);color:var(--accent-ink)}
  .ok{background:var(--ok-bg);color:var(--ok)} .no{background:var(--bad-bg);color:var(--bad)} .na{background:var(--warn-bg);color:var(--warn)}
  tr.detail td{background:var(--bg);padding:14px 18px 18px}
  dl.dt{display:grid;grid-template-columns:minmax(150px,220px) 1fr;gap:6px 18px;margin:0;font-size:13.5px}
  dl.dt dt{color:var(--muted);font-weight:600}
  dl.dt dd{margin:0;white-space:pre-wrap;word-break:break-word}
  .empty{padding:36px;text-align:center;color:var(--muted)}
  footer.ft{margin-top:26px;font-size:13px;color:var(--muted);max-width:110ch}
  footer.ft code{font-size:12px}
  [hidden]{display:none !important}
</style>
</head>
<body>
<div class="wrap">
  <header class="hd">
    <button id="themeBtn" type="button">Toggle theme</button>
    <div class="eyebrow">Volume CCI · FortiSwitch STIG and SRG Mapping</div>
    <h1>FortiSwitch SRG Crosswalk</h1>
    <p class="sub">FortiSwitch 2048F and 648F-FPOE on FortiSwitchOS 7.6.7, mapped to the Layer 2 Switch, Network Device Management and Router SRGs.
      Search, filter and sort the crosswalk, its prerequisites and the per-model support check; open a row for every column.
      Companion to <a href="../html/volume-201-fortiswitch-stig-and-srg-mapping/Enterprise-Infrastructure-Encyclopedia.html">Volume CCI</a>.
      Download the data as CSV with the buttons below or from the <a href="../data/volume-201-fortiswitch-stig-and-srg-mapping/">data folder</a>.</p>
  </header>

  <div class="stats" id="stats"></div>

  <div class="tabs" role="tablist" aria-label="Workbook sheets">
    <button role="tab" id="tab-crosswalk" aria-selected="true" data-tab="crosswalk">Crosswalk</button>
    <button role="tab" id="tab-prerequisites" aria-selected="false" data-tab="prerequisites">Prerequisites</button>
    <button role="tab" id="tab-model" aria-selected="false" data-tab="model">Model support</button>
  </div>

  <section id="panel-crosswalk" role="tabpanel" aria-labelledby="tab-crosswalk"></section>
  <section id="panel-prerequisites" role="tabpanel" aria-labelledby="tab-prerequisites" hidden></section>
  <section id="panel-model" role="tabpanel" aria-labelledby="tab-model" hidden></section>

  <footer class="ft">
    <strong>Source and method.</strong> Built from the workbook <code>__SOURCE__</code> (saved beside the CSV files in this volume's data folder) on __GENERATED__.
    The <strong>Crosswalk</strong> tab holds the Cisco-derived rows (those with a Cisco rule) and the FortiSwitch features migrated in from the feature list, one row per feature and SRG ID.
    <strong>CLI Verified by</strong> and <strong>GUI Verified by</strong> record who checked the command syntax on a switch; “Nobody” means not yet verified, and a check of the syntax does not show that a feature is supported on a model.
    <strong>Reference</strong> and <strong>Page</strong> point into the FortiSwitchOS 7.6.7 CLI Reference, the FortiOS 7.6.7 CLI Reference, the FortiSwitchOS 7.6.7 Administration Guide or the FortiSwitch 7.6.7 Feature Matrix.
    The <strong>Model support</strong> tab comes from the 7.6.7 feature matrix columns for the 6xxF series (648F-FPOE) and the 2048F.
    SRG versions and requirement IDs were checked against a third-party mirror of the DISA files only and still require DISA verification. Names are first names only.
  </footer>
</div>

<script>
const DATA = __DATA__;

const $ = (s, r = document) => r.querySelector(s);
const el = (tag, attrs = {}, kids = []) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v; else if (k === 'text') n.textContent = v; else n.setAttribute(k, v);
  }
  for (const c of [].concat(kids)) if (c != null) n.append(c);
  return n;
};
const collator = new Intl.Collator(undefined, {numeric: true, sensitivity: 'base'});

function csvText(cols, rows) {
  const q = v => /[",\r\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  return '﻿' + [cols, ...rows].map(r => r.map(q).join(',')).join('\r\n') + '\r\n';
}
function download(name, text) {
  const a = el('a', {href: URL.createObjectURL(new Blob([text], {type: 'text/csv;charset=utf-8'})), download: name});
  document.body.append(a); a.click(); a.remove();
}

// One searchable, sortable, filterable table.
function Grid(root, cfg) {
  const cols = cfg.columns, rows = cfg.rows;
  const hay = rows.map(r => r.join(' ').toLowerCase());
  let visible = new Set(cfg.visible);
  let sortCol = -1, sortDir = 1;
  const filterState = {};
  let checks = {};
  const open = new Set();

  const q = el('input', {type: 'search', placeholder: cfg.placeholder, 'aria-label': 'Search'});
  const controls = el('div', {class: 'controls'}, [el('div', {class: 'search'}, q)]);
  const selects = {};
  for (const f of cfg.filters) {
    const s = el('select', {'aria-label': f.label}, f.options.map(o => el('option', {value: o, text: o === '' ? f.label + ': all' : o})));
    s.addEventListener('change', () => { filterState[f.id] = s.value; render(); });
    filterState[f.id] = ''; selects[f.id] = s; controls.append(s);
  }
  for (const c of cfg.checks || []) {
    const cb = el('input', {type: 'checkbox'}); checks[c.id] = false;
    cb.addEventListener('change', () => { checks[c.id] = cb.checked; render(); });
    controls.append(el('label', {class: 'chk'}, [cb, c.label]));
  }
  const menu = el('div', {class: 'menu'}, cols.map((c, i) => {
    const cb = el('input', {type: 'checkbox'}); cb.checked = visible.has(i);
    cb.addEventListener('change', () => { cb.checked ? visible.add(i) : visible.delete(i); render(); });
    return el('label', {}, [cb, c]);
  }));
  controls.append(el('details', {class: 'cols'}, [el('summary', {class: 'btn', text: 'Columns'}), menu]));
  const dl = el('button', {class: 'btn', type: 'button', text: 'Download filtered rows (CSV)'});
  controls.append(dl);
  controls.append(el('a', {class: 'btn', href: cfg.csvHref, download: '', text: 'Download all (CSV)'}));
  const reset = el('button', {class: 'btn', type: 'button', text: 'Reset'});
  controls.append(reset);

  const count = el('p', {class: 'count', 'aria-live': 'polite'});
  const thead = el('thead'), tbody = el('tbody'), empty = el('div', {class: 'empty', text: 'No rows match.', hidden: ''});
  const table = el('table', {}, [thead, tbody]);
  root.append(controls, count, el('div', {class: 'tablewrap'}, [table, empty]));

  let current = [];
  function filtered() {
    const terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    const out = [];
    rows.forEach((r, i) => {
      if (!terms.every(t => hay[i].includes(t))) return;
      for (const f of cfg.filters) if (filterState[f.id] && !f.test(r, filterState[f.id])) return;
      for (const c of cfg.checks || []) if (checks[c.id] && !c.test(r)) return;
      out.push(i);
    });
    if (sortCol >= 0) out.sort((a, b) => sortDir * collator.compare(rows[a][sortCol], rows[b][sortCol]));
    return out;
  }
  function cell(i, r) {
    const v = r[i], name = cols[i];
    const td = el('td');
    if (cfg.pill && cfg.pill[name]) {
      const cls = cfg.pill[name](v);
      if (v && cls) { td.append(el('span', {class: 'pill ' + cls, text: v})); return td; }
    }
    if (cfg.mono && cfg.mono.includes(name)) td.className = 'mono';
    else if (cfg.wide && cfg.wide.includes(name)) td.className = 'wide';
    td.textContent = v;
    return td;
  }
  function render() {
    const vis = cols.map((_, i) => i).filter(i => visible.has(i));
    thead.replaceChildren(el('tr', {}, [el('th', {scope: 'col', 'aria-label': 'Details'}), ...vis.map(i => {
      const th = el('th', {scope: 'col', 'aria-sort': i === sortCol ? (sortDir > 0 ? 'ascending' : 'descending') : 'none'});
      const b = el('button', {type: 'button'}, [cols[i], el('span', {class: 'ar', text: i === sortCol ? (sortDir > 0 ? '▲' : '▼') : '▲▼'})]);
      b.addEventListener('click', () => { if (sortCol === i) sortDir *= -1; else { sortCol = i; sortDir = 1; } render(); });
      th.append(b); return th;
    })]));
    current = filtered();
    const frag = document.createDocumentFragment();
    for (const idx of current) {
      const r = rows[idx], isOpen = open.has(idx);
      const tg = el('button', {class: 'tg', type: 'button', 'aria-expanded': String(isOpen), 'aria-label': 'Show all columns for this row', text: isOpen ? '−' : '+'});
      tg.addEventListener('click', () => { open.has(idx) ? open.delete(idx) : open.add(idx); render(); });
      const tr = el('tr', {class: 'data'}, [el('td', {class: 'tgc'}, tg), ...vis.map(i => cell(i, r))]);
      frag.append(tr);
      if (isOpen) {
        const d = el('dl', {class: 'dt'});
        cols.forEach((c, i) => { if (r[i] !== '') d.append(el('dt', {text: c}), el('dd', {text: r[i]})); });
        frag.append(el('tr', {class: 'detail'}, el('td', {colspan: String(vis.length + 1)}, d)));
      }
    }
    tbody.replaceChildren(frag);
    empty.hidden = current.length > 0;
    count.textContent = current.length === rows.length ? rows.length + ' rows' : current.length + ' of ' + rows.length + ' rows';
  }
  q.addEventListener('input', render);
  dl.addEventListener('click', () => download(cfg.csvName, csvText(cols, current.map(i => rows[i]))));
  reset.addEventListener('click', () => {
    q.value = ''; sortCol = -1; sortDir = 1; open.clear();
    for (const f of cfg.filters) { filterState[f.id] = ''; selects[f.id].value = ''; }
    root.querySelectorAll('.controls input[type=checkbox]').forEach(cb => { if (!cb.closest('.menu')) cb.checked = false; });
    for (const c of cfg.checks || []) checks[c.id] = false;
    render();
  });
  render();
}

const col = (d, name) => d.columns.indexOf(name);
const unique = (d, i) => [...new Set(d.rows.map(r => r[i]).filter(Boolean))].sort(collator.compare);
const BASE = '../data/volume-201-fortiswitch-stig-and-srg-mapping/';

// ---- Crosswalk ----
const X = DATA.crosswalk;
const xi = {sev: col(X, 'Severity'), id: col(X, 'SRG ID'), cisco: col(X, 'Cisco rule'), cli: col(X, 'CLI Verified by'), gui: col(X, 'GUI Verified by'), ai: col(X, 'AI-comments')};
const family = r => (r[xi.id].match(/-(NDM|L2S|RTR|AAA)-/) || [])[1] || '';
const isVerified = v => v !== '' && v !== 'Nobody' && v !== 'Future';
const pillSev = v => ({'CAT I': 'p1', 'CAT II': 'p2', 'CAT III': 'p3'})[v] || '';
const pillWho = v => isVerified(v) ? 'ok' : 'na';
Grid($('#panel-crosswalk'), {
  columns: X.columns, rows: X.rows,
  visible: ['Severity', 'SRG ID', 'Requirement', 'FortiSwitch setting', 'FortiSwitchOS command', 'FortiSwitchOS version', 'Reference', 'Page', 'CLI Verified by', 'GUI Verified by'].map(n => col(X, n)),
  placeholder: 'Search the crosswalk: SRG ID, requirement, command, feature, reference…',
  filters: [
    {id: 'sev', label: 'Severity', options: ['', 'CAT I', 'CAT II', 'CAT III'], test: (r, v) => r[xi.sev] === v},
    {id: 'fam', label: 'SRG', options: ['', 'NDM', 'L2S', 'RTR', 'AAA'], test: (r, v) => family(r) === v},
    {id: 'org', label: 'Origin', options: ['', 'Cisco crosswalk', 'Migrated feature'], test: (r, v) => (r[xi.cisco] !== '') === (v === 'Cisco crosswalk')},
    {id: 'cli', label: 'CLI verified', options: ['', 'Verified', 'Not verified'], test: (r, v) => isVerified(r[xi.cli]) === (v === 'Verified')},
  ],
  checks: [{id: 'def', label: 'Deferred notes only', test: r => r[xi.ai].includes('DEFERRED')}],
  pill: {'Severity': pillSev, 'CLI Verified by': pillWho, 'GUI Verified by': pillWho},
  mono: ['FortiSwitchOS command', 'Cisco IOS XE command'], wide: ['Requirement', 'FortiSwitch setting', 'Comments', 'AI-comments'],
  csvHref: BASE + '__CSV_CROSSWALK__', csvName: '__CSV_CROSSWALK__',
});

// ---- Prerequisites ----
const P = DATA.prerequisites;
Grid($('#panel-prerequisites'), {
  columns: P.columns, rows: P.rows, visible: P.columns.map((_, i) => i),
  placeholder: 'Search the prerequisites…', filters: [],
  mono: ['How to put it in place'], wide: ['Prerequisite', 'What it enables', 'Source'],
  csvHref: BASE + '__CSV_PREREQ__', csvName: '__CSV_PREREQ__',
});

// ---- Model support ----
const M = DATA.model;
const status = v => /^Supported/.test(v) ? 'ok' : v === 'Not supported' ? 'no' : v ? 'na' : '';
const sg = (v, want) => want === 'Supported' ? /^Supported/.test(v) : want === 'Not supported' ? v === 'Not supported' : !/^Supported/.test(v) && v !== 'Not supported';
const m6 = col(M, '648F-FPOE (6xxF)'), m2 = col(M, '2048F');
Grid($('#panel-model'), {
  columns: M.columns, rows: M.rows, visible: M.columns.map((_, i) => i),
  placeholder: 'Search the features…',
  filters: [
    {id: 'cat', label: 'Category', options: ['', ...unique(M, col(M, 'Category'))], test: (r, v) => r[col(M, 'Category')] === v},
    {id: 's6', label: '648F-FPOE', options: ['', 'Supported', 'Not supported', 'Other'], test: (r, v) => sg(r[m6], v)},
    {id: 's2', label: '2048F', options: ['', 'Supported', 'Not supported', 'Other'], test: (r, v) => sg(r[m2], v)},
  ],
  pill: {'648F-FPOE (6xxF)': status, '2048F': status}, wide: ['Feature', '7.6.7 matrix row', 'First listed'],
  csvHref: BASE + '__CSV_MODEL__', csvName: '__CSV_MODEL__',
});

// ---- stats ----
const sevCount = s => X.rows.filter(r => r[xi.sev] === s).length;
const stats = [
  [X.rows.length, 'crosswalk rows'],
  [sevCount('CAT I'), 'CAT I requirements'],
  [X.rows.filter(r => isVerified(r[xi.cli])).length, 'rows with the command checked on a switch'],
  [X.rows.filter(r => r[xi.cisco] === '').length, 'rows migrated from the feature list'],
];
$('#stats').append(...stats.map(([n, l]) => el('div', {class: 'stat'}, [el('div', {class: 'n', text: String(n)}), el('div', {class: 'l', text: l})])));

// ---- tabs and theme ----
const tabs = [...document.querySelectorAll('.tabs [data-tab]')];
function showTab(name) {
  if (!['crosswalk', 'prerequisites', 'model'].includes(name)) name = 'crosswalk';
  tabs.forEach(t => t.setAttribute('aria-selected', String(t.dataset.tab === name)));
  for (const n of ['crosswalk', 'prerequisites', 'model']) $('#panel-' + n).hidden = n !== name;
  history.replaceState(null, '', '#' + name);
}
tabs.forEach(t => t.addEventListener('click', () => showTab(t.dataset.tab)));
showTab(location.hash.slice(1));
$('#themeBtn').addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  const dark = cur ? cur === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
});
</script>
</body>
</html>
