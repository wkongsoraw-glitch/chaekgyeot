# -*- coding: utf-8 -*-
"""네 권을 한 장의 아티팩트로 엮는다."""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "_artifact-build.html")   # 클로드 아티팩트용(평소엔 안 씀)

HEAD = r'''<title>AI와 동행하는 방법</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+KR:wght@300;400;500;600&display=swap">

<style>
  /* ═══════════  가을 토큰  ═══════════ */
  :root {
    /* 권마다의 색 — 늦가을에서 하나씩 */
    --h-moss:      #4C6444;   /* 1권 · 마른 이끼 */
    --h-persimmon: #B04A18;   /* 2권 · 감 */
    --h-plum:      #7C3B5E;   /* 3권 · 들국화 */
    --h-dusk:      #35566F;   /* 4권 · 저녁 하늘 */
    --h-series:    #8A6A2F;   /* 시리즈 · 마른 억새 */
    --accent: var(--h-series);

    --ground:    #FAF7F1;
    --surface:   #FFFFFF;
    --surface-2: #F1ECE1;
    --ink:       #211D18;
    --ink-soft:  #574E44;
    --ink-faint: #877C6E;
    --rule:      #E0D8C9;
    --rule-soft: #EDE7DB;
    --code-bg:   #F2EDE2;
    --shadow:    0 1px 2px rgba(33,29,24,.04), 0 12px 30px -24px rgba(33,29,24,.45);

    --measure: 38em;
    --mid:     760px;
    --wide:    900px;

    --f-display: "Gowun Batang", "Apple SD Gothic Neo", serif;
    --f-body: "IBM Plex Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif;
    --f-mono: "IBM Plex Mono", "SFMono-Regular", Menlo, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --h-moss:      #A2C291;
      --h-persimmon: #EC9660;
      --h-plum:      #D79CC1;
      --h-dusk:      #93B9D6;
      --h-series:    #D9B872;
      --ground:    #14120E;
      --surface:   #1C1913;
      --surface-2: #241F18;
      --ink:       #EEE8DC;
      --ink-soft:  #B5AA97;
      --ink-faint: #8B8070;
      --rule:      #322B22;
      --rule-soft: #241F18;
      --code-bg:   #1F1B15;
      --shadow:    0 1px 2px rgba(0,0,0,.5), 0 12px 30px -24px rgba(0,0,0,.9);
    }
  }
  :root[data-theme="dark"] {
    --h-moss:      #A2C291;
    --h-persimmon: #EC9660;
    --h-plum:      #D79CC1;
    --h-dusk:      #93B9D6;
    --h-series:    #D9B872;
    --ground:    #14120E;
    --surface:   #1C1913;
    --surface-2: #241F18;
    --ink:       #EEE8DC;
    --ink-soft:  #B5AA97;
    --ink-faint: #8B8070;
    --rule:      #322B22;
    --rule-soft: #241F18;
    --code-bg:   #1F1B15;
    --shadow:    0 1px 2px rgba(0,0,0,.5), 0 12px 30px -24px rgba(0,0,0,.9);
  }

  /* 지금 펼친 권이 페이지 전체의 색을 정한다 */
  :root[data-hue="moss"]      { --accent: var(--h-moss); }
  :root[data-hue="persimmon"] { --accent: var(--h-persimmon); }
  :root[data-hue="plum"]      { --accent: var(--h-plum); }
  :root[data-hue="dusk"]      { --accent: var(--h-dusk); }

  .c-moss      { --card-hue: var(--h-moss); }
  .c-persimmon { --card-hue: var(--h-persimmon); }
  .c-plum      { --card-hue: var(--h-plum); }
  .c-dusk      { --card-hue: var(--h-dusk); }
  .c-series    { --card-hue: var(--h-series); }

  /* ═══════════  로고  ═══════════ */
  .logo {
    display: block; flex: none;
    background-image: url("data:image/png;base64,__LOGO_B64__");
    background-repeat: no-repeat; background-position: left center; background-size: contain;
    aspect-ratio: 452 / 158;
  }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .logo { filter: invert(1); } }
  :root[data-theme="dark"] .logo { filter: invert(1); }
  .logo-cover { width: 86px; }
  .logo-side  { width: 60px; margin-bottom: 16px; }
  .logo-bar   { width: 51px; }

  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }

  body {
    background: var(--ground);
    color: var(--ink);
    font-family: var(--f-body);
    font-weight: 400;
    font-size: 17px;
    line-height: 1.8;
    margin: 0;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    word-break: keep-all;
    overflow-wrap: break-word;
  }

  .progress { position: fixed; inset: 0 0 auto 0; height: 2px; z-index: 50; pointer-events: none; }
  .progress i { display: block; height: 100%; width: 0; background: var(--accent); }

  /* ═══════════  뼈대  ═══════════ */
  .shell {
    max-width: 1320px; margin: 0 auto; padding: 0 28px 140px;
    display: grid; grid-template-columns: 1fr; gap: 0;
  }
  @media (min-width: 1080px) {
    .shell { grid-template-columns: 260px minmax(0, 1fr); gap: 64px; padding-left: 40px; padding-right: 40px; }
  }

  .side { display: none; }
  @media (min-width: 1080px) {
    .side { display: block; }
    .side-inner {
      position: sticky; top: 0; max-height: 100vh; overflow-y: auto;
      padding: 44px 32px 48px 0; margin-right: -32px;
      border-right: 1px solid var(--rule); scrollbar-width: thin;
    }
  }
  .side-logo { display: block; }
  .side-title {
    display: block; font-family: var(--f-display); font-weight: 700;
    font-size: 19px; color: var(--ink); text-decoration: none; line-height: 1.4;
  }
  .side-sub {
    font-family: var(--f-mono); font-size: 10px; letter-spacing: .14em;
    text-transform: uppercase; color: var(--ink-faint); margin: 6px 0 24px;
  }
  .vol-nav { display: grid; gap: 1px; padding-bottom: 22px; margin-bottom: 22px; border-bottom: 1px solid var(--rule); }
  .vol-nav a {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 10px; margin-left: -10px; border-radius: 3px;
    color: var(--ink-soft); text-decoration: none; font-size: 14px; line-height: 1.4;
    transition: background .15s, color .15s;
  }
  .vol-nav a i { width: 7px; height: 7px; border-radius: 50%; background: var(--card-hue, var(--ink-faint)); flex: none; }
  .vol-nav a:hover { background: var(--surface-2); color: var(--ink); }
  .vol-nav a.on { color: var(--ink); font-weight: 600; background: var(--surface-2); }

  .ch-nav { display: grid; gap: 1px; }
  .ch-nav a {
    display: grid; grid-template-columns: 26px minmax(0,1fr); gap: 10px; align-items: baseline;
    padding: 6px 10px 6px 11px; margin-left: -12px;
    border-left: 2px solid transparent; border-radius: 0 3px 3px 0;
    color: var(--ink-soft); text-decoration: none; font-size: 13.5px; line-height: 1.5;
    transition: color .15s, background .15s;
  }
  .ch-nav a .n { font-family: var(--f-mono); font-size: 10px; color: var(--ink-faint); }
  .ch-nav a:hover { color: var(--ink); background: var(--surface-2); }
  .ch-nav a.on { color: var(--accent); border-left-color: var(--accent); background: var(--surface-2); }
  .ch-nav a.on .n { color: var(--accent); }

  .doc { min-width: 0; }
  .vol { display: block; }
  html.js .vol { display: none; }
  html.js .vol.on { display: block; }

  /* ═══════════  표지  ═══════════ */
  .cover {
    padding: 76px 0 52px; border-bottom: 1px solid var(--rule);
    display: flex; flex-direction: column; gap: 24px; max-width: var(--wide);
  }
  .eyebrow {
    font-family: var(--f-mono); font-size: 11.5px; letter-spacing: .18em;
    text-transform: uppercase; color: var(--accent);
    display: flex; align-items: center; gap: 14px;
  }
  .eyebrow::after { content: ""; flex: 1; height: 1px; background: var(--rule); max-width: 200px; }
  .cover h1 {
    font-family: var(--f-display); font-weight: 700;
    font-size: clamp(36px, 5vw, 56px); line-height: 1.18; letter-spacing: -.015em;
    margin: 0; text-wrap: balance;
  }
  .cover .lede {
    font-family: var(--f-display); font-size: clamp(17.5px, 1.9vw, 21px);
    line-height: 1.8; color: var(--ink-soft); max-width: 33em; margin: 0;
  }
  .cover-meta {
    display: flex; flex-wrap: wrap; gap: 10px 30px;
    font-family: var(--f-mono); font-size: 12px; color: var(--ink-faint); padding-top: 6px;
  }
  .cover-meta b { color: var(--ink-soft); font-weight: 500; }

  /* ═══════════  네 권 카드  ═══════════ */
  .cards {
    display: grid; gap: 16px; max-width: var(--wide); margin: 44px 0 0;
    grid-template-columns: 1fr;
  }
  @media (min-width: 700px) { .cards { grid-template-columns: 1fr 1fr; } }
  .card {
    display: flex; flex-direction: column; gap: 9px;
    background: var(--surface); border: 1px solid var(--rule);
    border-top: 3px solid var(--card-hue);
    border-radius: 4px; padding: 22px 22px 20px;
    text-decoration: none; color: var(--ink);
    box-shadow: var(--shadow);
    transition: transform .18s, box-shadow .18s;
  }
  .card:hover { transform: translateY(-2px); box-shadow: 0 2px 4px rgba(33,29,24,.06), 0 18px 36px -26px rgba(33,29,24,.55); }
  .card .num {
    font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .16em;
    text-transform: uppercase; color: var(--card-hue);
  }
  .card h3 { font-family: var(--f-display); font-weight: 700; font-size: 21px; line-height: 1.35; margin: 0; }
  .card p { font-size: 14.5px; line-height: 1.7; color: var(--ink-soft); margin: 0; max-width: none; }
  .card .meta {
    font-family: var(--f-mono); font-size: 10.5px; color: var(--ink-faint);
    margin-top: 6px; padding-top: 12px; border-top: 1px solid var(--rule-soft);
  }

  /* ═══════════  권 맨 위의 큰 목차  ═══════════ */
  .toc { margin: 46px 0 0; max-width: var(--wide); border-top: 2px solid var(--accent); padding-top: 18px; }
  .toc h2 {
    font-family: var(--f-mono); font-size: 11px; letter-spacing: .18em;
    text-transform: uppercase; color: var(--accent); margin: 0 0 6px; font-weight: 500;
  }
  .toc ol { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr; }
  @media (min-width: 720px) {
    .toc ol { grid-template-columns: 1fr 1fr; grid-template-rows: repeat(6, auto); grid-auto-flow: column; column-gap: 48px; }
  }
  .toc li { display: block; }
  .toc li a {
    display: grid; grid-template-columns: 32px minmax(0,1fr); gap: 12px; align-items: baseline;
    padding: 13px 2px; min-height: 48px;
    border-bottom: 1px solid var(--rule-soft);
    color: var(--ink); text-decoration: none; font-size: 16px; line-height: 1.5;
    transition: color .15s;
  }
  .toc li a .n { font-family: var(--f-mono); font-size: 11px; letter-spacing: .06em; color: var(--ink-faint); }
  .toc li a:hover { color: var(--accent); }
  .toc li a:hover .n { color: var(--accent); }

  /* ═══════════  네 권 전체 차례 (표지)  ═══════════ */
  .allcontents { display: grid; grid-template-columns: 1fr; gap: 34px 48px; max-width: var(--wide); }
  @media (min-width: 720px) { .allcontents { grid-template-columns: 1fr 1fr; } }
  .allvol-h {
    display: flex; align-items: baseline; gap: 10px; text-decoration: none;
    padding-bottom: 10px; border-bottom: 2px solid var(--card-hue); margin-bottom: 4px;
  }
  .allvol-h .num { font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--card-hue); }
  .allvol-h .ttl { font-family: var(--f-display); font-weight: 700; font-size: 19px; color: var(--ink); }
  .allvol ol { list-style: none; margin: 0; padding: 0; display: grid; }
  .allvol li a {
    display: grid; grid-template-columns: 30px minmax(0,1fr); gap: 10px; align-items: baseline;
    padding: 10px 2px; min-height: 42px; border-bottom: 1px solid var(--rule-soft);
    color: var(--ink-soft); text-decoration: none; font-size: 14.5px; line-height: 1.5;
  }
  .allvol li a .n { font-family: var(--f-mono); font-size: 10px; color: var(--ink-faint); }
  .allvol li a:hover { color: var(--card-hue); }

  /* ═══════════  휴대폰 상단 바  ═══════════ */
  .topbar { display: none; }
  @media (max-width: 1079px) {
    /* 스크롤을 내려도 목차 바가 끝까지 따라온다 */
    .topbar {
      display: block; position: sticky; top: 0; z-index: 40;
      background: var(--ground); border-bottom: 1px solid var(--rule);
    }
    .topbar-row {
      display: flex; align-items: center; justify-content: space-between; gap: 12px;
      padding: 9px 20px 7px;
    }
    .topbar-title {
      display: flex; align-items: center; gap: 11px; min-width: 0;
      color: var(--ink); text-decoration: none;
    }
    .topbar-name {
      font-family: var(--f-display); font-weight: 700; font-size: 15px;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    @media (max-width: 344px) { .topbar-name { display: none; } }
    .toc-btn {
      flex: none; display: flex; align-items: center; gap: 8px; cursor: pointer;
      font-family: var(--f-body); font-size: 13px; font-weight: 500; color: var(--ink);
      background: var(--surface); border: 1px solid var(--rule); border-radius: 999px; padding: 8px 15px;
    }
    .toc-btn span.bars { display: block; width: 13px; height: 9px; border-top: 1.5px solid currentColor; border-bottom: 1.5px solid currentColor; position: relative; }
    .toc-btn span.bars::after { content: ""; position: absolute; left: 0; top: 3px; width: 100%; height: 1.5px; background: currentColor; }
    .chips { display: flex; gap: 7px; overflow-x: auto; padding: 0 20px 9px; scrollbar-width: none; }
    /* 화면이 낮을 때(가로로 눕혔을 때)는 제목 줄만 남긴다 */
    @media (max-height: 500px) { .chips { display: none; } }
    .chips::-webkit-scrollbar { display: none; }
    .chips a {
      flex: none; display: flex; align-items: center; gap: 7px; white-space: nowrap;
      font-size: 13px; text-decoration: none; color: var(--ink-soft);
      background: var(--surface); border: 1px solid var(--rule); border-radius: 999px; padding: 7px 14px;
    }
    .chips a i { width: 6px; height: 6px; border-radius: 50%; background: var(--card-hue); flex: none; }
    .chips a.on { color: var(--ink); font-weight: 600; border-color: var(--card-hue); background: var(--surface-2); }
  }

  /* ═══════════  차례 시트  ═══════════ */
  .sheet { display: none; position: fixed; inset: 0; z-index: 60; background: var(--ground); overflow-y: auto; }
  @media (max-width: 1079px) { .sheet.open { display: block; } }
  .sheet-bar {
    position: sticky; top: 0; display: flex; align-items: center; justify-content: space-between;
    padding: 13px 20px; background: var(--ground); border-bottom: 1px solid var(--rule);
  }
  .sheet-bar b { font-family: var(--f-display); font-size: 17px; font-weight: 700; }
  .sheet-close {
    cursor: pointer; font-family: var(--f-body); font-size: 13px; color: var(--ink);
    background: var(--surface); border: 1px solid var(--rule); border-radius: 999px; padding: 8px 16px;
  }
  .sheet-body { padding: 24px 20px 60px; }
  .sheet-label {
    font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase;
    color: var(--ink-faint); margin: 0 0 10px;
  }
  .sheet-vols { display: grid; gap: 8px; margin-bottom: 34px; }
  .sheet-vols a {
    display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink);
    border: 1px solid var(--rule); border-radius: 4px; padding: 14px 16px; background: var(--surface); font-size: 15px;
  }
  .sheet-vols a i { width: 7px; height: 7px; border-radius: 50%; background: var(--card-hue); flex: none; }
  .sheet-vols a.on { border-color: var(--card-hue); background: var(--surface-2); font-weight: 600; }
  .sheet-chs { display: grid; border-top: 1px solid var(--rule); }
  .sheet-chs a {
    display: grid; grid-template-columns: 32px minmax(0,1fr); gap: 12px; align-items: baseline;
    padding: 14px 2px; min-height: 50px; border-bottom: 1px solid var(--rule-soft);
    color: var(--ink); text-decoration: none; font-size: 15.5px; line-height: 1.5;
  }
  .sheet-chs a .n { font-family: var(--f-mono); font-size: 10.5px; color: var(--ink-faint); }

  /* ═══════════  장  ═══════════ */
  .chapter { padding-top: 88px; scroll-margin-top: 24px; }
  /* 상단 고정 바가 제목을 가리지 않도록 */
  @media (max-width: 1079px) { .chapter { scroll-margin-top: 112px; } }
  @media (max-width: 1079px) and (max-height: 500px) { .chapter { scroll-margin-top: 62px; } }
  .chapter-body { max-width: var(--wide); min-width: 0; }
  .chapter-eyebrow {
    font-family: var(--f-mono); font-size: 11px; letter-spacing: .18em;
    text-transform: uppercase; color: var(--accent); margin-bottom: 12px;
  }
  .chapter h2 {
    font-family: var(--f-display); font-weight: 700;
    font-size: clamp(25px, 2.9vw, 33px); line-height: 1.34; letter-spacing: -.01em;
    margin: 0 0 26px; padding-bottom: 16px; border-bottom: 1px solid var(--rule);
    max-width: var(--wide); text-wrap: balance;
  }
  .chapter h3 {
    font-family: var(--f-body); font-weight: 600; font-size: 16.5px; letter-spacing: -.005em;
    margin: 46px 0 14px; color: var(--ink);
    display: flex; align-items: baseline; gap: 11px; max-width: var(--measure);
  }
  .chapter h3::before { content: ""; width: 6px; height: 6px; flex: none; background: var(--accent); transform: translateY(-3px); }

  p { margin: 0 0 20px; max-width: var(--measure); }
  .chapter-body > p:last-child { margin-bottom: 0; }
  a { color: var(--accent); text-underline-offset: .18em; }
  strong { font-weight: 600; color: var(--ink); }
  em { font-style: normal; font-family: var(--f-display); }
  u { text-decoration-color: var(--accent); text-underline-offset: .22em; }

  ul.plain, ol.steps {
    padding-left: 0; list-style: none; margin: 0 0 22px;
    display: grid; gap: 11px; max-width: var(--measure);
  }
  ul.plain li { padding-left: 19px; position: relative; }
  ul.plain li::before { content: "—"; position: absolute; left: 0; color: var(--ink-faint); font-family: var(--f-mono); font-size: 13px; }
  ol.steps { counter-reset: s; gap: 15px; }
  ol.steps li { counter-increment: s; padding-left: 40px; position: relative; }
  ol.steps li::before {
    content: counter(s); position: absolute; left: 0; top: 4px;
    width: 24px; height: 24px; display: grid; place-items: center;
    border: 1px solid var(--accent); color: var(--accent); border-radius: 50%;
    font-family: var(--f-mono); font-size: 11.5px;
  }

  code {
    font-family: var(--f-mono); font-size: .855em; background: var(--code-bg);
    padding: .14em .4em; border-radius: 3px; color: var(--ink);
  }
  pre {
    font-family: var(--f-mono); font-size: 13.5px; line-height: 1.85;
    background: var(--code-bg); border: 1px solid var(--rule-soft); border-radius: 4px;
    padding: 20px 22px; margin: 0 0 24px; max-width: var(--mid);
    overflow-x: auto; color: var(--ink); tab-size: 2;
  }
  pre code { background: none; padding: 0; font-size: inherit; }
  .cm { color: var(--ink-faint); }

  /* ═══════════  나란히 두기  ═══════════ */
  .demo { margin: 0 0 30px; display: grid; gap: 16px; max-width: var(--wide); }
  @media (min-width: 1000px) { .demo.split { grid-template-columns: 1fr 1fr; gap: 22px; align-items: start; } }
  .demo-label {
    font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .14em;
    text-transform: uppercase; color: var(--ink-faint); margin-bottom: 9px;
  }
  .demo pre { margin: 0; max-width: none; }
  .demo-why { font-size: 14px; line-height: 1.7; color: var(--ink-soft); margin: 10px 0 0; max-width: none; }

  .say {
    font-family: var(--f-display); font-size: 17px; line-height: 1.75;
    padding: 16px 18px; border-radius: 4px;
    border: 1px solid var(--rule); background: var(--surface);
  }
  .say-dim { color: var(--ink-faint); border-style: dashed; background: transparent; }
  .say-lit { border-left: 2px solid var(--accent); }

  .browser { border: 1px solid var(--rule); border-radius: 5px; overflow: hidden; box-shadow: var(--shadow); background: #FCFCFD; }
  .browser-bar {
    background: var(--surface-2); border-bottom: 1px solid var(--rule);
    padding: 8px 13px; font-family: var(--f-mono); font-size: 10.5px;
    color: var(--ink-faint); display: flex; align-items: center; gap: 6px;
  }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--rule); flex: none; }
  .browser-bar span { margin-left: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

  .preview {
    background: #FCFCFD; color: #16181C; padding: 22px 24px;
    font-family: "Times New Roman", "Apple SD Gothic Neo", serif;
    font-size: 15px; line-height: 1.55; font-weight: 400;
  }
  .preview h1 { font-size: 1.9em; margin: .5em 0; font-weight: 700; font-family: inherit; line-height: 1.25; max-width: none; }
  .preview h2 { font-size: 1.4em; margin: .7em 0 .4em; font-weight: 700; font-family: inherit; border: 0; padding: 0; max-width: none; }
  .preview p { margin: 0 0 .9em; max-width: none; }
  .preview ul { margin: 0 0 .9em; padding-left: 1.6em; }
  .preview a { color: #1A46C8; }
  .preview.styled { font-family: var(--f-body); background: #FBF9F5; color: #23262B; font-weight: 400; }
  .preview.styled h1 { font-family: var(--f-display); font-size: 1.7em; letter-spacing: -.01em; margin: 0 0 .2em; font-weight: 700; }
  .preview.styled .sub { color: #7C8291; font-size: .85em; margin-bottom: 1.4em; }
  .preview.styled ul { list-style: none; padding: 0; }
  .preview.styled li { padding: 9px 0; border-bottom: 1px solid #E7E2D9; }

  /* ═══════════  안내 상자  ═══════════ */
  .note {
    border-left: 2px solid var(--accent); background: var(--surface);
    padding: 18px 22px; margin: 0 0 26px; border-radius: 0 4px 4px 0;
    font-size: 15.5px; line-height: 1.75; max-width: var(--mid); box-shadow: var(--shadow);
  }
  .note p { margin-bottom: 0; max-width: none; }
  .note .tag {
    font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .14em;
    text-transform: uppercase; color: var(--accent); display: block; margin-bottom: 8px;
  }
  .note.quiet { border-left-color: var(--ink-faint); }
  .note.quiet .tag { color: var(--ink-faint); }

  /* ═══════════  표  ═══════════ */
  .table-wrap {
    overflow-x: auto; margin: 0 0 28px; max-width: var(--wide);
    border-top: 1px solid var(--rule);
    /* 가로로 더 있을 때만 가장자리에 그늘이 진다 */
    background:
      linear-gradient(to right, var(--ground), transparent) 0 0 / 20px 100% no-repeat local,
      linear-gradient(to left, var(--ground), transparent) 100% 0 / 20px 100% no-repeat local,
      radial-gradient(farthest-side at 0 50%, rgba(33,29,24,.14), transparent) 0 0 / 11px 100% no-repeat scroll,
      radial-gradient(farthest-side at 100% 50%, rgba(33,29,24,.14), transparent) 100% 0 / 11px 100% no-repeat scroll;
  }
  table { width: 100%; border-collapse: collapse; font-size: 14.5px; line-height: 1.7; min-width: 420px; }
  th, td { text-align: left; padding: 13px 20px 13px 0; border-bottom: 1px solid var(--rule-soft); vertical-align: top; }
  th {
    font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .14em;
    text-transform: uppercase; color: var(--ink-faint); font-weight: 500;
    padding-top: 12px; padding-bottom: 10px;
  }
  td:first-child { color: var(--ink); }
  td code { white-space: nowrap; }

  /* ═══════════  용어  ═══════════ */
  dl.glossary { margin: 0; display: grid; max-width: var(--mid); border-top: 1px solid var(--rule); }
  dl.glossary > div { display: grid; grid-template-columns: 1fr; gap: 3px; padding: 15px 0; border-bottom: 1px solid var(--rule-soft); }
  @media (min-width: 660px) { dl.glossary > div { grid-template-columns: 158px minmax(0,1fr); gap: 24px; align-items: baseline; } }
  dl.glossary dt { font-weight: 600; font-size: 15px; }
  dl.glossary dt small { display: block; font-family: var(--f-mono); font-size: 10px; color: var(--ink-faint); letter-spacing: .06em; font-weight: 400; margin-top: 2px; }
  dl.glossary dd { margin: 0; color: var(--ink-soft); font-size: 15px; line-height: 1.72; }

  /* ═══════════  계획표  ═══════════ */
  .plan { display: grid; margin: 0 0 26px; max-width: var(--mid); border-top: 1px solid var(--rule); }
  .plan-row { display: grid; grid-template-columns: 96px minmax(0,1fr); gap: 20px; padding: 16px 0; border-bottom: 1px solid var(--rule-soft); align-items: baseline; }
  .plan-row .day { font-family: var(--f-mono); font-size: 11.5px; color: var(--accent); letter-spacing: .06em; }
  .plan-row.rest .day { color: var(--ink-faint); }
  .plan-row .what { font-size: 15.5px; line-height: 1.7; }
  .plan-row .what small { display: block; color: var(--ink-soft); font-size: 13.5px; line-height: 1.7; margin-top: 3px; }

  /* ═══════════  그대로 쓰는 문장  ═══════════ */
  .script { display: grid; margin: 0 0 26px; max-width: var(--mid); border-top: 1px solid var(--rule); }
  .script-item { padding: 20px 0; border-bottom: 1px solid var(--rule-soft); }
  .script-when { font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-faint); margin-bottom: 10px; }
  .script-say { font-family: var(--f-display); font-size: 18px; line-height: 1.75; color: var(--ink); padding: 2px 0 2px 18px; border-left: 2px solid var(--accent); }
  .script-why { margin-top: 10px; font-size: 14.5px; line-height: 1.72; color: var(--ink-soft); max-width: 46em; }
  .script-why b { font-weight: 600; color: var(--ink); }

  .closing { margin-top: 88px; padding-top: 36px; border-top: 1px solid var(--rule); max-width: var(--measure); }
  .closing p { font-family: var(--f-display); font-size: 18px; line-height: 1.9; color: var(--ink-soft); max-width: none; }
  .closing p:first-child { color: var(--ink); }

  .next {
    display: flex; flex-wrap: wrap; gap: 14px; align-items: center;
    margin-top: 40px; padding-top: 26px; border-top: 1px solid var(--rule-soft); max-width: var(--wide);
  }
  .next-label { font-family: var(--f-mono); font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-faint); }
  .next a {
    text-decoration: none; font-size: 15px; padding: 8px 16px;
    border: 1px solid var(--rule); border-radius: 3px; background: var(--surface);
    color: var(--ink); transition: border-color .15s, color .15s;
  }
  .next a:hover { border-color: var(--card-hue, var(--accent)); color: var(--card-hue, var(--accent)); }

  a:focus-visible, .card:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }
  ::selection { background: var(--surface-2); }

  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    * { animation: none !important; transition: none !important; }
  }
  @media (max-width: 640px) {
    body { font-size: 16.5px; }
    .shell { padding: 0 20px 100px; }
    .cover { padding-top: 56px; }
    .chapter { padding-top: 64px; }
    .plan-row { grid-template-columns: 78px minmax(0,1fr); gap: 14px; }
  }
</style>

<script>document.documentElement.classList.add("js");</script>

<div class="progress" aria-hidden="true"><i></i></div>

<header class="topbar">
  <div class="topbar-row">
    <a class="topbar-title" href="#cover"><span class="logo logo-bar" role="img" aria-label="최수빈"></span><span class="topbar-name">AI와 동행하는 방법</span></a>
    <button class="toc-btn" type="button" aria-expanded="false" aria-controls="sheet"><span class="bars"></span>차례</button>
  </div>
  <nav class="chips" aria-label="권">
    <a href="#cover" data-vol="v0" class="c-series"><i></i>표지</a>
    <a href="#v1" data-vol="v1" class="c-moss"><i></i>1권</a>
    <a href="#v2" data-vol="v2" class="c-persimmon"><i></i>2권</a>
    <a href="#v3" data-vol="v3" class="c-plum"><i></i>3권</a>
    <a href="#v4" data-vol="v4" class="c-dusk"><i></i>4권</a>
  </nav>
</header>

<div class="sheet" id="sheet">
  <div class="sheet-bar">
    <b>차례</b>
    <button class="sheet-close" type="button">닫기</button>
  </div>
  <div class="sheet-body">
    <div class="sheet-label">권 고르기</div>
    <nav class="sheet-vols">
      <a href="#cover" data-vol="v0" class="c-series"><i></i>표지</a>
      <a href="#v1" data-vol="v1" class="c-moss"><i></i>1권 · AI에게 질문하는 법</a>
      <a href="#v2" data-vol="v2" class="c-persimmon"><i></i>2권 · 아이디어 꺼내는 법</a>
      <a href="#v3" data-vol="v3" class="c-plum"><i></i>3권 · 웹사이트 만들기</a>
      <a href="#v4" data-vol="v4" class="c-dusk"><i></i>4권 · 앱 만들기</a>
    </nav>
    <div class="sheet-label sheet-chs-label">이 권의 차례</div>
    <nav class="sheet-chs"></nav>
  </div>
</div>

<div class="shell">

<aside class="side">
  <div class="side-inner">
    <a class="side-logo" href="#cover" aria-label="표지로"><span class="logo logo-side" role="img" aria-label="최수빈"></span></a>
    <a class="side-title" href="#cover">AI와 동행하는 방법</a>
    <div class="side-sub">비전공자를 위한 실용 시리즈</div>
    <nav class="vol-nav" aria-label="권">
      <a href="#cover" data-vol="v0" class="c-series"><i></i><span>표지</span></a>
      <a href="#v1" data-vol="v1" class="c-moss"><i></i><span>1권 · AI에게 질문하는 법</span></a>
      <a href="#v2" data-vol="v2" class="c-persimmon"><i></i><span>2권 · 아이디어 꺼내는 법</span></a>
      <a href="#v3" data-vol="v3" class="c-plum"><i></i><span>3권 · 웹사이트 만들기</span></a>
      <a href="#v4" data-vol="v4" class="c-dusk"><i></i><span>4권 · 앱 만들기</span></a>
    </nav>
    <nav class="ch-nav" aria-label="이 권의 차례"></nav>
  </div>
</aside>

<main class="doc">
'''

HUB = r'''<section class="vol" id="v0" data-hue="series">

  <header class="cover">
    <span class="logo logo-cover" role="img" aria-label="최수빈"></span>
    <div class="eyebrow">네 권으로 된 실용 시리즈</div>
    <h1>AI와 동행하는 방법</h1>
    <p class="lede">코딩도 기획도 배운 적 없는 사람이 AI와 함께 무언가를 만들어 내보내기까지, 실제로 필요한 것만 네 권에 나눠 담았습니다. 이론은 최소한만 두고, 오늘 그대로 써먹을 수 있는 문장과 절차 위주로 썼습니다.</p>
    <div class="cover-meta">
      <div><b>읽는 사람</b> 비전공자 · 처음 만드는 사람</div>
      <div><b>전제 지식</b> 없음</div>
      <div><b>전체</b> 네 권 · 약 두 시간</div>
    </div>
  </header>

  <div class="cards">
    <a class="card c-moss" href="#v1" data-vol="v1">
      <div class="num">제1권</div>
      <h3>AI에게 질문하는 법</h3>
      <p>무엇을 시킬 수 있는지, 어떻게 말해야 하는지. 그대로 복사해 쓰는 요청 틀 여덟 개.</p>
      <div class="meta">11장 · 25분</div>
    </a>
    <a class="card c-persimmon" href="#v2" data-vol="v2">
      <div class="num">제2권</div>
      <h3>아이디어 꺼내는 법</h3>
      <p>AI는 무엇을 만들지 정해 주지 않습니다. 모으고 · 쏟고 · 고르고 · 키우는 네 단계.</p>
      <div class="meta">11장 · 25분</div>
    </a>
    <a class="card c-plum" href="#v3" data-vol="v3">
      <div class="num">제3권</div>
      <h3>웹사이트 만들기</h3>
      <p>웹사이트는 결국 폴더 하나다. HTML·CSS의 최소 문법에서 주소를 갖기까지.</p>
      <div class="meta">11장 · 40분</div>
    </a>
    <a class="card c-dusk" href="#v4" data-vol="v4">
      <div class="num">제4권</div>
      <h3>앱 만들기</h3>
      <p>'앱'이라는 말의 세 가지 뜻을 가르는 데서 시작해, 가장 빠른 길로 첫 앱까지.</p>
      <div class="meta">11장 · 30분</div>
    </a>
  </div>

  <section class="chapter" id="v0toc">
    <div class="chapter-body">
      <div class="chapter-eyebrow">전체 차례</div>
      <h2>네 권의 모든 장</h2>
      <p>어느 장이든 눌러 바로 펴실 수 있습니다.</p>
      <div class="allcontents"><!--ALLTOC--></div>
    </div>
  </section>

  <section class="chapter" id="v0c0">
    <div class="chapter-body">
      <div class="chapter-eyebrow">읽는 법</div>
      <h2>어디부터 읽어도 됩니다</h2>
      <p>네 권은 이어져 있지만 묶여 있지는 않습니다. <strong>지금 하려는 일이 있는 자리에서 펴시면 됩니다.</strong> 만들 것이 이미 정해져 있다면 3권이나 4권부터 시작하셔도 괜찮습니다.</p>

      <div class="table-wrap">
        <table>
          <tr><th>지금 이런 자리라면</th><th>여기부터</th></tr>
          <tr><td>AI를 어떻게 써야 할지 감이 없다</td><td>1권</td></tr>
          <tr><td>만들고 싶은데 무엇을 만들지 모르겠다</td><td>2권</td></tr>
          <tr><td>내 이름의 사이트를 갖고 싶다</td><td>3권</td></tr>
          <tr><td>기록하거나 계산하는 것을 만들고 싶다</td><td>4권 (3권을 먼저 훑으면 수월합니다)</td></tr>
        </table>
      </div>

      <p>다만 순서대로 읽으실 거라면 1권이 가장 도움이 됩니다. 나머지 세 권은 전부 <strong>AI와 함께 만드는 것</strong>을 전제로 쓰였고, 그 대화법이 1권에 있기 때문입니다.</p>

      <h3>네 권을 관통하는 한 문장</h3>
      <p><em>작게 만들어 일찍 내보내고, 반응을 보고 다시 만든다.</em> 이 문장은 네 권 어디에서도 다시 나옵니다. 글도 그렇게 쓰이고, 아이디어도 그렇게 자라고, 앱도 그렇게 만들어집니다.</p>

      <div class="note quiet">
        <span class="tag">이 시리즈의 약속</span>
        <p>배경 지식과 이론은 최소한만 둡니다. 대신 <strong>그대로 복사해 쓸 수 있는 문장</strong>, <strong>순서가 정해진 절차</strong>, <strong>고를 수 있게 정리한 표</strong>를 중심에 둡니다. 읽고 나서 무엇을 해야 할지 모르겠는 장이 있다면, 그건 이 시리즈의 잘못입니다.</p>
      </div>
    </div>
  </section>

</section>
'''

TAIL = r'''</main>
</div>

<script>
(function () {
  var root = document.documentElement;
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  var vols = Array.prototype.slice.call(document.querySelectorAll(".vol"));
  var volLinks = Array.prototype.slice.call(document.querySelectorAll(".vol-nav a, .chips a, .sheet-vols a"));
  var sheet = document.getElementById("sheet");
  var sheetChs = document.querySelector(".sheet-chs");
  var tocBtn = document.querySelector(".toc-btn");
  var chNav = document.querySelector(".ch-nav");
  var bar = document.querySelector(".progress i");
  var chLinks = [], chSecs = [], ticking = false, current = null;

  function buildChapterNav(vol) {
    chNav.innerHTML = "";
    sheetChs.innerHTML = "";
    chLinks = []; chSecs = [];
    Array.prototype.forEach.call(vol.querySelectorAll(".chapter"), function (sec) {
      var eyebrow = sec.querySelector(".chapter-eyebrow");
      var h2 = sec.querySelector("h2");
      if (!h2) return;
      var a = document.createElement("a");
      a.href = "#" + sec.id;
      a.innerHTML = '<span class="n"></span><span class="t"></span>';
      a.querySelector(".n").textContent = eyebrow ? eyebrow.textContent.trim() : "";
      a.querySelector(".t").textContent = h2.textContent.trim();
      chNav.appendChild(a);
      chLinks.push(a); chSecs.push(sec);

      var b = a.cloneNode(true);
      sheetChs.appendChild(b);
    });
  }

  function show(id, keepScroll) {
    var vol = document.getElementById(id) || document.getElementById("v0");
    if (current === vol) return;
    current = vol;
    vols.forEach(function (v) { v.classList.toggle("on", v === vol); });
    root.setAttribute("data-hue", vol.getAttribute("data-hue") || "series");
    volLinks.forEach(function (a) { a.classList.toggle("on", a.getAttribute("data-vol") === vol.id); });
    buildChapterNav(vol);
    var lbl = document.querySelector(".sheet-chs-label");
    if (lbl) lbl.style.display = vol.id === "v0" ? "none" : "";
    if (!keepScroll) jumpTop();
    paint();
  }

  function jumpTop() {
    var prev = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
    requestAnimationFrame(function () {
      window.scrollTo(0, 0);
      root.style.scrollBehavior = prev;
    });
  }

  function paint() {
    ticking = false;
    var h = document.scrollingElement || document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    var here = -1;
    for (var i = 0; i < chSecs.length; i++) {
      if (chSecs[i].getBoundingClientRect().top <= 140) here = i;
    }
    for (var j = 0; j < chLinks.length; j++) {
      var on = j === here;
      chLinks[j].classList.toggle("on", on);
      if (on) chLinks[j].setAttribute("aria-current", "true");
      else chLinks[j].removeAttribute("aria-current");
    }
  }

  function fromHash() {
    var hash = (location.hash || "").replace("#", "");
    if (!hash || hash === "cover") { show("v0"); return; }
    var m = hash.match(/^(v\d+)/);
    var volId = m ? m[1] : "v0";
    var wasSame = current && current.id === volId;
    show(volId, wasSame);
    var target = document.getElementById(hash);
    if (target && hash !== volId) {
      requestAnimationFrame(function () {
        target.scrollIntoView({ behavior: wasSame ? "smooth" : "auto", block: "start" });
      });
    } else if (!wasSame) {
      jumpTop();
    }
  }

  /* 해시 변경이 막힌 환경(내장 뷰어 등)에서도 권 이동이 되도록 직접 처리한다 */
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href^='#']") : null;
    if (!a) return;
    var hash = a.getAttribute("href").slice(1);
    var volId = hash === "cover" || !hash ? "v0" : (hash.match(/^(v\d+)/) || [])[1];
    if (!volId) return;
    e.preventDefault();
    closeSheet();
    var wasSame = current && current.id === volId;
    show(volId, wasSame);
    var target = document.getElementById(hash);
    if (target && hash !== volId) {
      target.scrollIntoView({ behavior: wasSame ? "smooth" : "auto", block: "start" });
    } else if (!wasSame) {
      jumpTop();
    }
    try { history.replaceState(null, "", "#" + hash); } catch (err) {}
    paint();
  });

  function openSheet() {
    sheet.classList.add("open");
    if (tocBtn) tocBtn.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    sheet.scrollTop = 0;
  }
  function closeSheet() {
    if (!sheet.classList.contains("open")) return;
    sheet.classList.remove("open");
    if (tocBtn) tocBtn.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }
  if (tocBtn) tocBtn.addEventListener("click", openSheet);
  var closeBtn = document.querySelector(".sheet-close");
  if (closeBtn) closeBtn.addEventListener("click", closeSheet);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeSheet(); });

  window.addEventListener("hashchange", fromHash);
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(paint); }
  }, { passive: true });
  window.addEventListener("resize", paint);

  fromHash();
})();
</script>
'''

import re as _re

VOLMETA = [
    ("v1", "제1권", "AI에게 질문하는 법", "c-moss"),
    ("v2", "제2권", "아이디어 꺼내는 법", "c-persimmon"),
    ("v3", "제3권", "웹사이트 만들기", "c-plum"),
    ("v4", "제4권", "앱 만들기", "c-dusk"),
]

def rebuild_toc_items(frag):
    """<li><span class="n">00</span><a href="#x">제목</a></li>  →  행 전체가 링크"""
    return _re.sub(
        r'<li><span class="n">(.*?)</span><a href="(.*?)">(.*?)</a></li>',
        lambda m: '<li><a href="%s"><span class="n">%s</span><span class="t">%s</span></a></li>'
                  % (m.group(2), m.group(1), m.group(3)),
        frag)

def toc_items(frag):
    return _re.findall(r'<li><a href="(.*?)"><span class="n">(.*?)</span><span class="t">(.*?)</span></a></li>', frag)

NEXT = {
    "v1.html": ('v2', 'c-persimmon', '제2권 · 아이디어 꺼내는 법'),
    "v2.html": ('v3', 'c-plum', '제3권 · 웹사이트 만들기'),
    "v3.html": ('v4', 'c-dusk', '제4권 · 앱 만들기'),
    "v4.html": ('cover', 'c-series', '표지로 돌아가기'),
}

frags = {}
for name in ("v1.html", "v2.html", "v3.html", "v4.html"):
    frags[name] = rebuild_toc_items(io.open(os.path.join(HERE, name), encoding="utf-8").read())

blocks = []
for (vid, num, title, cls), name in zip(VOLMETA, ("v1.html", "v2.html", "v3.html", "v4.html")):
    rows = "".join(
        '\n        <li><a href="%s"><span class="n">%s</span><span class="t">%s</span></a></li>'
        % (href, n, t) for href, n, t in toc_items(frags[name]))
    blocks.append(
        '\n    <div class="allvol %s">'
        '\n      <a class="allvol-h" href="#%s"><span class="num">%s</span><span class="ttl">%s</span></a>'
        '\n      <ol>%s\n      </ol>'
        '\n    </div>' % (cls, vid, num, title, rows))

LOGO_B64 = io.open(os.path.join(HERE, "logo.b64"), encoding="utf-8").read().strip()
HEAD = HEAD.replace("__LOGO_B64__", LOGO_B64)

parts = [HEAD, HUB.replace("<!--ALLTOC-->", "".join(blocks) + "\n  ")]
for name in ("v1.html", "v2.html", "v3.html", "v4.html"):
    frag = frags[name]
    href, cls, label = NEXT[name]
    link = ('\n  <div class="next %s">\n'
            '    <span class="next-label">다음 권</span>\n'
            '    <a href="#%s">%s &rarr;</a>\n'
            '  </div>\n') % (cls, href, label)
    tail = frag.rstrip()
    assert tail.endswith("</section>")
    frag = tail[: tail.rfind("</section>")] + link + "</section>\n"
    parts.append(frag)
parts.append(TAIL)

html = "\n".join(parts)
io.open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, len(html), "bytes")

# ── 깃헙 등 어디에나 올릴 수 있는 판본 ──
TITLE = "AI와 동행하는 방법"
DESC = "코딩도 기획도 배운 적 없는 사람이 AI와 함께 무언가를 만들어 내보내기까지. 네 권으로 나눈 실용 시리즈."
cut = html.index("</style>") + len("</style>")
doc = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%s">
<meta name="author" content="최수빈">

<!-- 메신저에 링크를 붙였을 때 보이는 미리보기 -->
<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary">

%s
</head>
<body>
%s
</body>
</html>
""" % (DESC, TITLE, DESC, html[:cut], html[cut:].strip())

SITE = os.path.expanduser("~/Documents/chaekgyeot/index.html")
if os.path.isdir(os.path.dirname(SITE)):
    io.open(SITE, "w", encoding="utf-8").write(doc)
    print("wrote", SITE, len(doc), "bytes")
print("volumes:", html.count('class="vol"'), " chapters:", html.count('class="chapter"'))
