<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>README — Sports or Politics Classifier</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg:        #0a0c10;
    --surface:   #0f1219;
    --card:      #141820;
    --border:    #1e2535;
    --accent1:   #00d9a3;   /* teal  — sports */
    --accent2:   #e85d4a;   /* coral — politics */
    --accent3:   #f5c842;   /* gold  — highlight */
    --text:      #dce5f0;
    --muted:     #6b7a99;
    --code-bg:   #0d111a;
    --glow1: rgba(0,217,163,.18);
    --glow2: rgba(232,93,74,.18);
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Lora', Georgia, serif;
    font-size: 15.5px;
    line-height: 1.75;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 28px 80px;
  }

  /* ── HERO ─────────────────────────────────────────────────────── */
  .hero {
    position: relative;
    text-align: center;
    padding: 64px 0 56px;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 60% 55% at 25% 40%, var(--glow1), transparent),
      radial-gradient(ellipse 60% 55% at 75% 60%, var(--glow2), transparent);
    z-index: 0;
    animation: pulse 8s ease-in-out infinite alternate;
  }
  @keyframes pulse {
    from { opacity: .6; }
    to   { opacity: 1;  }
  }
  .hero > * { position: relative; z-index: 1; }

  .hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--accent1);
    margin-bottom: 16px;
    opacity: 0;
    animation: fadeUp .6s .1s forwards;
  }
  .hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 7vw, 68px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -.02em;
    margin-bottom: 18px;
    opacity: 0;
    animation: fadeUp .7s .2s forwards;
  }
  .hero h1 span.s { color: var(--accent1); }
  .hero h1 span.p { color: var(--accent2); }
  .hero h1 span.q { color: var(--accent3); }

  .hero-sub {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 17px;
    color: var(--muted);
    max-width: 540px;
    margin: 0 auto 32px;
    opacity: 0;
    animation: fadeUp .7s .35s forwards;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 32px;
    opacity: 0;
    animation: fadeUp .7s .45s forwards;
  }
  .badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .06em;
    padding: 5px 13px;
    border-radius: 4px;
    border: 1px solid;
    text-transform: uppercase;
  }
  .badge.teal  { color: var(--accent1); border-color: var(--accent1); background: rgba(0,217,163,.08); }
  .badge.coral { color: var(--accent2); border-color: var(--accent2); background: rgba(232,93,74,.08); }
  .badge.gold  { color: var(--accent3); border-color: var(--accent3); background: rgba(245,200,66,.08); }
  .badge.grey  { color: var(--muted);   border-color: var(--border);  background: var(--surface); }

  .cta-row {
    display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;
    opacity: 0; animation: fadeUp .7s .55s forwards;
  }
  .cta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .07em;
    text-transform: uppercase;
    padding: 10px 22px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    text-decoration: none;
  }
  .cta-primary   { background: var(--accent1); color: #000; }
  .cta-secondary { background: transparent; color: var(--accent2); border: 1px solid var(--accent2); }
  .cta-tertiary  { background: transparent; color: var(--muted);   border: 1px solid var(--border); }

  @keyframes fadeUp {
    from { opacity:0; transform: translateY(18px); }
    to   { opacity:1; transform: translateY(0); }
  }

  /* ── DIVIDER ──────────────────────────────────────────────────── */
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 48px 0;
  }

  /* ── SECTION ──────────────────────────────────────────────────── */
  .section { margin-bottom: 56px; }

  h2 {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  h2::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }
  h2 .icon { font-size: 18px; }

  h3 {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--accent1);
    letter-spacing: .05em;
    text-transform: uppercase;
    margin: 28px 0 12px;
  }

  p { margin-bottom: 14px; color: var(--text); }

  /* ── RESULT MATRIX ────────────────────────────────────────────── */
  .matrix-wrap {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    background: var(--card);
  }
  .matrix-header {
    background: var(--surface);
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
  }
  .matrix-header span {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .matrix-header .dot { width:8px;height:8px;border-radius:50%; display:inline-block; margin-left:6px; }
  .matrix {
    width: 100%;
    border-collapse: collapse;
  }
  .matrix th {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    padding: 12px 18px;
    text-align: center;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
  }
  .matrix th:first-child { text-align: left; }
  .matrix td {
    font-size: 14px;
    padding: 13px 18px;
    text-align: center;
    border-bottom: 1px solid var(--border);
    transition: background .15s;
  }
  .matrix tr:last-child td { border-bottom: none; }
  .matrix td:first-child {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 13px;
    text-align: left;
    color: var(--text);
  }
  .matrix tr:hover td { background: rgba(255,255,255,.025); }

  .cell-top {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 14px;
    color: var(--accent1);
    background: rgba(0,217,163,.07);
  }
  .cell-mid {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--accent3);
  }
  .cell-low {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--accent2);
  }
  .feat-label {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 3px;
    margin-left: 8px;
    font-weight: 500;
  }
  .feat-bow   { background: rgba(0,217,163,.12); color: var(--accent1); }
  .feat-tfidf { background: rgba(245,200,66,.12); color: var(--accent3); }
  .feat-ngram { background: rgba(232,93,74,.12);  color: var(--accent2); }

  /* ── PIPELINE ─────────────────────────────────────────────────── */
  .pipeline {
    display: flex;
    flex-direction: column;
    gap: 0;
    position: relative;
  }
  .pipeline::before {
    content: '';
    position: absolute;
    left: 27px;
    top: 24px;
    bottom: 24px;
    width: 2px;
    background: linear-gradient(to bottom, var(--accent1), var(--accent2));
    border-radius: 2px;
  }
  .pipe-step {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 14px 0;
    position: relative;
    opacity: 0;
    animation: fadeUp .5s forwards;
  }
  .pipe-step:nth-child(1) { animation-delay: .05s; }
  .pipe-step:nth-child(2) { animation-delay: .12s; }
  .pipe-step:nth-child(3) { animation-delay: .19s; }
  .pipe-step:nth-child(4) { animation-delay: .26s; }
  .pipe-step:nth-child(5) { animation-delay: .33s; }
  .pipe-step:nth-child(6) { animation-delay: .40s; }

  .pipe-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
    z-index: 1;
    border: 2px solid;
    background: var(--bg);
    margin-top: 2px;
  }
  .pipe-num.c1 { color: var(--accent1); border-color: var(--accent1); }
  .pipe-num.c2 { color: var(--accent3); border-color: var(--accent3); }
  .pipe-num.c3 { color: var(--accent2); border-color: var(--accent2); }

  .pipe-body { flex: 1; }
  .pipe-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: var(--text);
    margin-bottom: 4px;
  }
  .pipe-desc {
    font-size: 13.5px;
    color: var(--muted);
    line-height: 1.6;
    font-family: 'Lora', serif;
  }
  .pipe-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 2px 7px;
    border-radius: 3px;
    margin-left: 6px;
  }

  /* ── FEATURE CARDS ────────────────────────────────────────────── */
  .feat-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  @media(max-width: 640px) { .feat-cards { grid-template-columns: 1fr; } }

  .feat-card {
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    background: var(--card);
    position: relative;
    overflow: hidden;
    transition: transform .2s, border-color .2s;
  }
  .feat-card:hover {
    transform: translateY(-3px);
    border-color: var(--accent1);
  }
  .feat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .feat-card.bow::before   { background: var(--accent1); }
  .feat-card.tfidf::before { background: var(--accent3); }
  .feat-card.ngram::before { background: var(--accent2); }

  .feat-card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 10px;
  }
  .feat-card.bow .feat-card-label   { color: var(--accent1); }
  .feat-card.tfidf .feat-card-label { color: var(--accent3); }
  .feat-card.ngram .feat-card-label { color: var(--accent2); }

  .feat-card-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 8px;
  }
  .feat-card-vocab {
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 6px;
  }
  .feat-card.bow .feat-card-vocab   { color: var(--accent1); }
  .feat-card.tfidf .feat-card-vocab { color: var(--accent3); }
  .feat-card.ngram .feat-card-vocab { color: var(--accent2); }

  .feat-card-desc {
    font-size: 12.5px;
    color: var(--muted);
    line-height: 1.55;
  }

  /* ── CODE BLOCK ───────────────────────────────────────────────── */
  .code-wrap {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    background: var(--code-bg);
  }
  .code-header {
    background: var(--surface);
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid var(--border);
  }
  .code-dot { width:11px;height:11px;border-radius:50%; }
  .code-dot.r { background:#ff5f57; }
  .code-dot.y { background:#ffbd2e; }
  .code-dot.g { background:#28ca42; }
  .code-lang {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-left: auto;
  }
  pre {
    padding: 20px 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px;
    line-height: 1.65;
    overflow-x: auto;
    margin: 0;
    color: #b8c9e8;
  }
  .kw   { color: #7eb8f7; }
  .fn   { color: var(--accent1); }
  .str  { color: #c3e88d; }
  .cmt  { color: #4e5f7c; font-style: italic; }
  .num  { color: var(--accent3); }
  .var  { color: #f8c8a0; }

  /* ── FINDINGS ─────────────────────────────────────────────────── */
  .findings { display: flex; flex-direction: column; gap: 14px; }
  .finding {
    display: flex;
    gap: 16px;
    padding: 18px 20px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    border-left: 3px solid;
    transition: transform .15s;
  }
  .finding:hover { transform: translateX(4px); }
  .finding.f1 { border-left-color: var(--accent1); }
  .finding.f2 { border-left-color: var(--accent3); }
  .finding.f3 { border-left-color: var(--accent2); }
  .finding.f4 { border-left-color: var(--muted); }
  .finding-icon { font-size: 22px; flex-shrink: 0; line-height: 1; margin-top: 2px; }
  .finding-body { flex: 1; }
  .finding-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 5px;
  }
  .finding-desc { font-size: 13.5px; color: var(--muted); line-height: 1.6; }
  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: .85em;
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 1px 5px;
    border-radius: 3px;
    color: var(--accent1);
  }

  /* ── LIMITATIONS ──────────────────────────────────────────────── */
  .lim-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  @media(max-width: 580px) { .lim-grid { grid-template-columns: 1fr; } }
  .lim {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 15px 17px;
  }
  .lim-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--accent2);
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-bottom: 5px;
  }
  .lim-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 13.5px;
    margin-bottom: 5px;
  }
  .lim-desc { font-size: 12.5px; color: var(--muted); line-height: 1.55; }

  /* ── STATS ROW ────────────────────────────────────────────────── */
  .stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 40px;
  }
  @media(max-width: 560px) { .stats-row { grid-template-columns: repeat(2,1fr); } }
  .stat {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 16px;
    text-align: center;
  }
  .stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 5px;
  }
  .stat-val.teal  { color: var(--accent1); }
  .stat-val.coral { color: var(--accent2); }
  .stat-val.gold  { color: var(--accent3); }
  .stat-val.grey  { color: var(--muted);   }
  .stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
  }

  /* ── FOOTER ───────────────────────────────────────────────────── */
  .footer {
    border-top: 1px solid var(--border);
    padding-top: 32px;
    text-align: center;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: .08em;
  }
  .footer .roll {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    display: block;
    margin-bottom: 6px;
  }
</style>
</head>
<body>

<!-- ═══════════════════════════ HERO ═══════════════════════════════ -->
<div class="hero">
  <p class="hero-eyebrow">NLP Assignment · Problem 4 · B23CM1053</p>
  <h1>
    <span class="s">Sports</span>
    <span class="q"> or </span>
    <span class="p">Politics</span>
    <span class="q">?</span>
  </h1>
  <p class="hero-sub">A binary text classifier trained on live Wikinews articles.<br/>Features built from scratch — no sklearn vectorisers.</p>
  <div class="badges">
    <span class="badge teal">Python 3.9+</span>
    <span class="badge teal">NumPy · from scratch</span>
    <span class="badge gold">scikit-learn</span>
    <span class="badge gold">BeautifulSoup</span>
    <span class="badge coral">Wikinews API</span>
    <span class="badge grey">Standard Library Only (features)</span>
  </div>
  <div class="cta-row">
    <a class="cta cta-primary" href="./B23CM1053_prob4_report.pdf">📄 Full Report (PDF)</a>
    <a class="cta cta-secondary" href="./B23CM1053_prob4.py">🐍 Source Code</a>
    <a class="cta cta-tertiary" href="./outputs/results_summary_wikinews.csv">📊 Results CSV</a>
  </div>
</div>

<!-- ═══════════════════════════ STATS ══════════════════════════════ -->
<div class="stats-row">
  <div class="stat">
    <div class="stat-val teal">98.75%</div>
    <div class="stat-label">Best Accuracy</div>
  </div>
  <div class="stat">
    <div class="stat-val gold">396</div>
    <div class="stat-label">Articles Total</div>
  </div>
  <div class="stat">
    <div class="stat-val coral">9</div>
    <div class="stat-label">Experiments</div>
  </div>
  <div class="stat">
    <div class="stat-val grey">177K</div>
    <div class="stat-label">Max Features</div>
  </div>
</div>

<!-- ═══════════════════════════ RESULTS ════════════════════════════ -->
<div class="section">
  <h2><span class="icon">🏆</span> Results</h2>

  <div class="matrix-wrap">
    <div class="matrix-header">
      <span>Test Accuracy — 80-article stratified held-out set</span>
      <span><span class="dot" style="background:var(--accent1)"></span><span class="dot" style="background:var(--accent3)"></span><span class="dot" style="background:var(--accent2)"></span></span>
    </div>
    <table class="matrix">
      <thead>
        <tr>
          <th>Feature Representation</th>
          <th>Logistic Regression</th>
          <th>Linear SVC</th>
          <th>Random Forest</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Bag-of-Words Unigram <span class="feat-label feat-bow">BOW</span></td>
          <td class="cell-top">98.75%</td>
          <td class="cell-top">98.75%</td>
          <td class="cell-top">98.75%</td>
        </tr>
        <tr>
          <td>TF-IDF Unigram <span class="feat-label feat-tfidf">TF-IDF</span></td>
          <td class="cell-mid">95.00%</td>
          <td class="cell-top">98.75%</td>
          <td class="cell-top">98.75%</td>
        </tr>
        <tr>
          <td>TF-IDF 1–3-gram <span class="feat-label feat-ngram">N-GRAM</span></td>
          <td class="cell-mid">95.00%</td>
          <td class="cell-low">93.75%</td>
          <td class="cell-top">98.75%</td>
        </tr>
      </tbody>
    </table>
  </div>
  <p style="font-size:12px;color:var(--muted);margin-top:8px;font-family:'JetBrains Mono',monospace;">
    🟢 ≥ 98%  · 🟡 ≥ 95%  · 🔴 &lt; 95%  &nbsp;|&nbsp; Macro F1 mirrors accuracy in all cases
  </p>
</div>

<div class="divider"></div>

<!-- ═══════════════════════════ PIPELINE ═══════════════════════════ -->
<div class="section">
  <h2><span class="icon">⚙️</span> Pipeline</h2>
  <div class="pipeline">
    <div class="pipe-step">
      <div class="pipe-num c1">1</div>
      <div class="pipe-body">
        <div class="pipe-title">Fetch Article Titles <span class="pipe-tag">MediaWiki API</span></div>
        <div class="pipe-desc"><code>categorymembers</code> for Sports (200 titles ✓) and Politics (0 titles — fell back to <code>search("politics")</code>, 200 titles ✓)</div>
      </div>
    </div>
    <div class="pipe-step">
      <div class="pipe-num c1">2</div>
      <div class="pipe-body">
        <div class="pipe-title">Scrape Full Article Text <span class="pipe-tag">BeautifulSoup</span></div>
        <div class="pipe-desc">GET <code>/wiki/&lt;title&gt;</code> → parse <code>.mw-parser-output</code> → strip tables, scripts, asides → join all <code>&lt;p&gt;</code> longer than 30 chars. Discard if &lt; 50 words. Result: 198 Sports + 199 Politics → balanced to <strong>198 each</strong>.</div>
      </div>
    </div>
    <div class="pipe-step">
      <div class="pipe-num c2">3</div>
      <div class="pipe-body">
        <div class="pipe-title">Preprocess Text</div>
        <div class="pipe-desc">Lowercase → strip URLs → remove <code>[N]</code> citations → keep <code>[a-z0-9 ]</code> only → collapse whitespace</div>
      </div>
    </div>
    <div class="pipe-step">
      <div class="pipe-num c2">4</div>
      <div class="pipe-body">
        <div class="pipe-title">Build Features from Scratch <span class="pipe-tag">Pure NumPy</span></div>
        <div class="pipe-desc">Custom <code>build_vocabulary_and_df()</code>, <code>build_bow_matrix()</code>, <code>compute_idf()</code>, <code>build_tfidf_matrix()</code>, <code>make_ngrams()</code> — no sklearn vectorisers</div>
      </div>
    </div>
    <div class="pipe-step">
      <div class="pipe-num c3">5</div>
      <div class="pipe-body">
        <div class="pipe-title">Train & Evaluate <span class="pipe-tag">sklearn</span></div>
        <div class="pipe-desc">Stratified 80/20 split · <code>random_state=42</code> · 3 features × 3 classifiers = 9 experiments · Metrics: Accuracy, Precision, Recall, F1 (macro)</div>
      </div>
    </div>
    <div class="pipe-step">
      <div class="pipe-num c3">6</div>
      <div class="pipe-body">
        <div class="pipe-title">Export Results</div>
        <div class="pipe-desc">All results saved to <code>outputs/results_summary_wikinews.csv</code></div>
      </div>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- ═══════════════════════════ QUICK START ════════════════════════ -->
<div class="section">
  <h2><span class="icon">🚀</span> Quick Start</h2>

  <h3>Install</h3>
  <div class="code-wrap">
    <div class="code-header">
      <span class="code-dot r"></span><span class="code-dot y"></span><span class="code-dot g"></span>
      <span class="code-lang">bash</span>
    </div>
    <pre>pip install requests beautifulsoup4 numpy pandas scikit-learn tqdm</pre>
  </div>

  <h3>Run</h3>
  <div class="code-wrap">
    <div class="code-header">
      <span class="code-dot r"></span><span class="code-dot y"></span><span class="code-dot g"></span>
      <span class="code-lang">bash</span>
    </div>
    <pre>python B23CM1053_prob4.py --articles-per-class 200</pre>
  </div>

  <h3>All Arguments</h3>
  <div class="code-wrap">
    <div class="code-header">
      <span class="code-dot r"></span><span class="code-dot y"></span><span class="code-dot g"></span>
      <span class="code-lang">bash</span>
    </div>
<pre>python B23CM1053_prob4.py \
  <span class="var">--articles-per-class</span>  <span class="num">200</span>   <span class="cmt"># articles to fetch per class   (default: 200)</span>
  <span class="var">--min-words</span>           <span class="num">50</span>    <span class="cmt"># discard shorter articles      (default: 50)</span>
  <span class="var">--test-size</span>           <span class="num">0.2</span>   <span class="cmt"># fraction held out for test    (default: 0.2)</span>
  <span class="var">--delay</span>               <span class="num">0.3</span>   <span class="cmt"># seconds between API requests  (default: 0.3)</span></pre>
  </div>

  <h3>Expected Terminal Output</h3>
  <div class="code-wrap">
    <div class="code-header">
      <span class="code-dot r"></span><span class="code-dot y"></span><span class="code-dot g"></span>
      <span class="code-lang">terminal</span>
    </div>
<pre><span class="cmt">Step 1: fetch category titles for Sports and Politics (API).</span>
Listing Category:Sports: 100%|████████████| 200/200 [00:01&lt;00:00, 186.22titles/s]
Listing Category:Politics:   0%|          |   0/200 [00:00&lt;?, ?titles/s]
Found titles -&gt; Sports: 200, Politics: <span class="num">0</span>
<span class="str">No category members found for Politics — falling back to search('politics').</span>
Search 'politics': 100%|████████████████| 200/200 [00:01&lt;00:00, 120.86titles/s]
Final counts -&gt; Sports: <span class="num">200</span>, Politics: <span class="num">200</span>
Downloading Sports:   100%|████████████| 200/200 [02:22&lt;00:00,  1.40it/s]
Downloading Politics: 100%|████████████| 200/200 [03:59&lt;00:00,  1.20s/it]
Downloaded articles -&gt; Sports: <span class="num">198</span>, Politics: <span class="num">199</span>
Using <span class="num">198</span> articles per class (balanced).
Building unigram vocabulary and feature matrices (from scratch)...
Building ngram (1-3) vocabulary and TF-IDF...

Evaluating feature: <span class="fn">bow_unigram</span>   shape=(<span class="num">396</span>, <span class="num">11665</span>)
 LogisticRegression → acc=<span class="num">0.9875</span>  f1=<span class="num">0.9875</span>
 LinearSVC          → acc=<span class="num">0.9875</span>  f1=<span class="num">0.9875</span>
 RandomForest       → acc=<span class="num">0.9875</span>  f1=<span class="num">0.9875</span>
...
Saved results to outputs/results_summary_wikinews.csv</pre>
  </div>
  <p style="font-size:13px;color:var(--muted);margin-top:10px;">⏱️ Total runtime: ~7–8 minutes (network-bound)</p>
</div>

<div class="divider"></div>

<!-- ═══════════════════════════ FEATURES ═══════════════════════════ -->
<div class="section">
  <h2><span class="icon">🧮</span> Feature Representations</h2>
  <p>All three representations are built <strong>entirely from scratch</strong> in pure NumPy — no <code>CountVectorizer</code> or <code>TfidfVectorizer</code>.</p>

  <div class="feat-cards">
    <div class="feat-card bow">
      <div class="feat-card-label">Feature 01</div>
      <div class="feat-card-name">Bag-of-Words</div>
      <div class="feat-card-vocab">11,665</div>
      <div class="feat-card-desc">Raw token counts. <code>X[i][j] = count(vⱼ, dᵢ)</code>. No normalisation. Simplest baseline — but performs on par with TF-IDF for LogReg and RF.</div>
    </div>
    <div class="feat-card tfidf">
      <div class="feat-card-label">Feature 02</div>
      <div class="feat-card-name">TF-IDF Unigram</div>
      <div class="feat-card-vocab">11,665</div>
      <div class="feat-card-desc">TF × smooth IDF. Weights discriminative words higher, suppresses common noise. Same vocab as BoW — different weighting scheme.</div>
    </div>
    <div class="feat-card ngram">
      <div class="feat-card-label">Feature 03</div>
      <div class="feat-card-name">TF-IDF 1–3-gram</div>
      <div class="feat-card-vocab">177,913</div>
      <div class="feat-card-desc">Unigrams + bigrams + trigrams. Captures "won the match", "prime minister of". ~15× larger vocabulary than unigram alone.</div>
    </div>
  </div>

  <h3>IDF Formula (implemented from scratch)</h3>
  <div class="code-wrap">
    <div class="code-header">
      <span class="code-dot r"></span><span class="code-dot y"></span><span class="code-dot g"></span>
      <span class="code-lang">python</span>
    </div>
<pre><span class="cmt"># compute_idf() — pure Python/NumPy, no sklearn</span>
<span class="kw">def</span> <span class="fn">compute_idf</span>(vocab, docs_tokens):
    N = <span class="fn">len</span>(docs_tokens)
    df = <span class="fn">defaultdict</span>(<span class="fn">int</span>)
    <span class="kw">for</span> tokens <span class="kw">in</span> docs_tokens:
        <span class="kw">for</span> t <span class="kw">in</span> <span class="fn">set</span>(tokens):
            df[t] += <span class="num">1</span>
    <span class="kw">return</span> {t: math.<span class="fn">log</span>((N+<span class="num">1</span>) / (df.<span class="fn">get</span>(t,<span class="num">0</span>)+<span class="num">1</span>)) + <span class="num">1.0</span>
            <span class="kw">for</span> t <span class="kw">in</span> vocab}    <span class="cmt"># smooth IDF: ln((N+1)/(df+1)) + 1</span></pre>
  </div>
</div>

<div class="divider"></div>

<!-- ═══════════════════════════ FINDINGS ═══════════════════════════ -->
<div class="section">
  <h2><span class="icon">💡</span> Key Findings</h2>
  <div class="findings">
    <div class="finding f1">
      <div class="finding-icon">🌲</div>
      <div class="finding-body">
        <div class="finding-title">Random Forest wins every feature configuration</div>
        <div class="finding-desc">All three feature sets → 98.75%. Its 200-tree ensemble handles both the 11K sparse unigram and the 177K n-gram space without degradation — no tuning required.</div>
      </div>
    </div>
    <div class="finding f2">
      <div class="finding-icon">📦</div>
      <div class="finding-body">
        <div class="finding-title">Raw counts (BoW) ≥ TF-IDF for Logistic Regression</div>
        <div class="finding-desc">LogReg drops 98.75% → 95.00% switching from BoW to TF-IDF. For this task, <em>absolute frequency</em> is more discriminative — "football" appearing 20× is a strong signal that TF-IDF normalisation dilutes.</div>
      </div>
    </div>
    <div class="finding f3">
      <div class="finding-icon">📉</div>
      <div class="finding-body">
        <div class="finding-title">More n-grams ≠ better for LinearSVC</div>
        <div class="finding-desc">LinearSVC falls 98.75% → 93.75% on the 177K n-gram space. The explosion of correlated bigram/trigram features makes max-margin harder to optimise within the fixed <code>max_iter=5000</code> budget.</div>
      </div>
    </div>
    <div class="finding f4">
      <div class="finding-icon">🎯</div>
      <div class="finding-body">
        <div class="finding-title">Task is inherently easy — even the worst config achieves 93.75%</div>
        <div class="finding-desc">Sports and Politics have extremely distinct vocabularies (team names, scores vs. government terminology, party names). The ceiling effect limits differences between configurations to a few percentage points.</div>
      </div>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- ═══════════════════════════ LIMITATIONS ════════════════════════ -->
<div class="section">
  <h2><span class="icon">⚠️</span> Limitations</h2>
  <div class="lim-grid">
    <div class="lim">
      <div class="lim-num">01 · Label Noise</div>
      <div class="lim-title">Search-API Politics labels</div>
      <div class="lim-desc"><code>Category:Politics</code> was empty. Search-based titles may include articles that only mention politics tangentially.</div>
    </div>
    <div class="lim">
      <div class="lim-num">02 · Scale</div>
      <div class="lim-title">Small test set (80 articles)</div>
      <div class="lim-desc">One misclassification = 1.25% accuracy change. High variance — cross-validation would give more reliable estimates.</div>
    </div>
    <div class="lim">
      <div class="lim-num">03 · Preprocessing</div>
      <div class="lim-title">No stop-word removal or stemming</div>
      <div class="lim-desc">Function words inflate vocabulary without discriminative signal. Porter stemming would reduce sparsity.</div>
    </div>
    <div class="lim">
      <div class="lim-num">04 · Memory</div>
      <div class="lim-title">Dense 177K-feature matrix ≈ 563 MB</div>
      <div class="lim-desc">Dense NumPy arrays don't scale. <code>scipy.sparse.csr_matrix</code> would be needed for larger corpora.</div>
    </div>
    <div class="lim">
      <div class="lim-num">05 · Vocabulary</div>
      <div class="lim-title">No min-df threshold</div>
      <div class="lim-desc">Single-occurrence tokens (hapax legomena) add noise to the vocabulary without generalisation benefit.</div>
    </div>
    <div class="lim">
      <div class="lim-num">06 · Domain</div>
      <div class="lim-title">Wikinews prose style only</div>
      <div class="lim-desc">Short, neutral encyclopaedic articles. Likely degrades on social media, blogs, or other writing styles.</div>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- ═══════════════════════════ STRUCTURE ══════════════════════════ -->
<div class="section">
  <h2><span class="icon">📁</span> Project Structure</h2>
  <div class="code-wrap">
    <div class="code-header">
      <span class="code-dot r"></span><span class="code-dot y"></span><span class="code-dot g"></span>
      <span class="code-lang">tree</span>
    </div>
<pre>sports-politics-classifier/
│
├── <span class="fn">B23CM1053_prob4.py</span>               <span class="cmt">← main pipeline</span>
│
├── outputs/
│   └── <span class="str">results_summary_wikinews.csv</span>  <span class="cmt">← all 9 experiment results</span>
│
├── <span class="str">B23CM1053_prob4_report.pdf</span>        <span class="cmt">← full 12-page LaTeX report</span>
│
└── <span class="var">README.md</span>                         <span class="cmt">← you are here</span></pre>
  </div>
</div>

<!-- ═══════════════════════════ FOOTER ═════════════════════════════ -->
<div class="footer">
  <span class="roll">B23CM1053</span>
  NLP Assignment · Problem 4 · Binary Text Classification on Wikinews
</div>

</body>
</html>
