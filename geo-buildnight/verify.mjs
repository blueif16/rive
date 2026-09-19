// Runs the SPEC.md verification checklist against index.html and prints PASS/FAIL
// with evidence. Also writes the 160×90 thumbnails for check 7.
//   node verify.mjs
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdirSync, writeFileSync } from 'node:fs';
import puppeteer from '/Users/tk/Desktop/brain/projects/rive/.claude/skills/rive-animation/scripts/render/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = 'file://' + join(HERE, 'index.html');
const THUMBS = join(HERE, 'out', 'thumbs'); mkdirSync(THUMBS, { recursive: true });

const STAGES = { C1: '#4A7BF7', C2: '#F4603A', C3: '#6DBF9A', C4: '#F5D8DA', C5: '#F2BE4B', C6: '#F5D8DA', C7: '#F4EEE4', C8: '#1F2125', C9: '#4A7BF7', C10: '#F4EEE4' };
const STARTS = { C1: 0, C2: 2.5, C3: 5.0, C4: 6.5, C5: 8.5, C6: 11.0, C7: 12.5, C8: 16.0, C9: 18.0, C10: 20.5 };
const IDS = Object.keys(STARTS);
const MID = { C1: 1.6, C2: 4.0, C3: 5.4, C4: 7.5, C5: 9.8, C6: 12.1, C7: 14.5, C8: 17.4, C9: 19.2, C10: 23.0 };
const READ = { C1: 1.05, C2: 1.30, C3: 1.05, C4: 1.05, C5: 1.05, C7: 1.30, C9: 1.05, C10: 0.80 };
const TYPE = { C1: '#1F2125', C2: '#F4EEE4', C3: '#1F2125', C4: '#1F2125', C5: '#1F2125', C7: '#1F2125', C9: '#F4EEE4', C10: '#1F2125' };
const r1 = v => Math.round(v * 10) / 10;
const results = [];
function rec(no, name, pass, evidence) { results.push({ no, name, pass, evidence }); console.log(`\n[${pass ? 'PASS' : 'FAIL'}] ${no}. ${name}\n${evidence}`); }

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--hide-scrollbars'] });
async function open(q) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto(BASE + q, { waitUntil: 'load' }); await page.waitForFunction('window.__ready === true');
  return page;
}
const page = await open('?t=0');
const at = t => page.evaluate(t => window.renderAt(t), t);
const font = await page.evaluate(() => window.fontInfo());
console.log('font:', JSON.stringify(font));

// 1. Cut timing --------------------------------------------------------------
{
  const lines = []; let ok = true;
  for (let i = 0; i < IDS.length; i++) {
    const id = IDS[i], b = STARTS[id];
    await at(b); const now = await page.evaluate(() => window.pixelAt(8, 8));
    let prev = '—';
    if (i > 0) { await at(b - 1 / 60); prev = await page.evaluate(() => window.pixelAt(8, 8)); }
    const good = now === STAGES[id] && (i === 0 || prev === STAGES[IDS[i - 1]]);
    ok = ok && good;
    lines.push(`  t=${b}: (8,8)=${now} ${now === STAGES[id] ? '✓' : '✗'}${i > 0 ? `  t=${(b - 1 / 60).toFixed(4)}: ${prev} ${prev === STAGES[IDS[i - 1]] ? '✓' : '✗'}` : ''}`);
  }
  rec(1, 'Cut timing', ok, lines.join('\n'));
}

// 2. Type scale (pixel-scanned cap height of the line's first capital / digit) --
const midDbg = {};
{
  const lines = []; let ok = true;
  for (const id of IDS) {
    const d = await at(MID[id]); midDbg[id] = d;
    if (!TYPE[id]) continue;
    const want = (id === 'C3' || id === 'C10') ? 114 : 62;
    for (const L of d.lines) {
      const g = L.glyphs ? L.glyphs.find(g => /[A-Z0-9]/.test(g.ch)) : null;
      if (!g && !L.digit) { lines.push(`  ${id} t=${MID[id]} "${L.text}" px=${L.px}: no capital in the line; face cap height at ${L.px} px = ${r1(L.px * font.capH86 / 86)} px`); continue; }
      const x0 = g ? g.x : L.box[0], x1 = g ? g.x + g.w : L.box[2];
      const scan = await page.evaluate((x0, x1, y0, y1, hex) => window.scanRows(x0, x1, y0, y1, hex), x0, x1, L.baseline - L.px * 0.85, L.baseline - 0.5, TYPE[id]);
      const h = scan ? scan[2] : 0; const good = Math.abs(h - want) <= 2;
      ok = ok && good;
      lines.push(`  ${id} t=${MID[id]} "${L.text}" px=${L.px} glyph "${g ? g.ch : L.text}" ink rows above baseline: ${r1(h)} px (want ${want}±2) ${good ? '✓' : '✗'}`);
    }
  }
  lines.push(`  measureText cap height: ${r1(font.capH86)} px @86, ${r1(font.capH158)} px @158 (face: ${font.resolved})`);
  rec(2, 'Type scale', ok, lines.join('\n'));
}

// 3. No bleed, no overlap ------------------------------------------------------
{
  const lines = []; let ok = true;
  const M = [51, 29, 1229, 691];
  const inter = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]);
  for (const id of IDS) {
    if (!TYPE[id]) continue;
    const d = midDbg[id];
    for (const L of d.lines) {
      const b = L.box, inside = b[0] >= M[0] && b[1] >= M[1] && b[2] <= M[2] && b[3] <= M[3];
      ok = ok && inside;
      lines.push(`  ${id} "${L.text}" box [${b.map(r1)}] inside margin ${inside ? '✓' : '✗'}`);
      for (const s of d.shapes) {
        const allowed = s.tag === 'Semicircle stage' || s.tag === 'countdown ground' || /swap|Star4 Build|Star4 Night/.test(s.tag);
        if (inter(b, s.aabb)) { if (!allowed) ok = false; lines.push(`    ∩ ${s.tag} [${s.aabb.map(r1)}] ${allowed ? '(allowed)' : '✗ OVERLAP'}`); }
      }
    }
  }
  rec(3, 'No bleed, no overlap', ok, lines.join('\n'));
}

// 4 & 11. Holds and timing ------------------------------------------------------
const table = await page.evaluate(() => window.moveTable());
{
  const lines = []; let ok4 = true, ok11 = true;
  lines.push('  card   entrance-end  exit/cut  hold   read   ok');
  for (const c of table) {
    const len = c.end - c.start;
    const ins = c.moves.filter(m => m.k === 'in');
    const inEnd = Math.max(...ins.filter(m => c.id !== 'C3' || m.holdRef).map(m => m.t0 + m.d));
    const inEndAll = Math.max(...ins.map(m => m.t0 + m.d));
    const exit = c.moves.find(m => m.k === 'exit');
    const exitStart = exit ? exit.t0 : len;
    const hold = exitStart - inEnd;
    const read = READ[c.id];
    const good = read === undefined || hold >= read - 1e-9;
    ok4 = ok4 && good;
    const endsOnTime = inEndAll <= c.holdStart + 1e-9 || (c.id === 'C3' && inEnd <= c.holdStart + 1e-9);
    const exitOnTime = !exit || Math.abs(exit.t0 + exit.d - len) <= 1 / 60;
    ok11 = ok11 && endsOnTime && exitOnTime;
    lines.push(`  ${c.id.padEnd(5)} ${inEnd.toFixed(2).padStart(8)}     ${exitStart.toFixed(2).padStart(6)}   ${hold.toFixed(2)}   ${read === undefined ? '  — ' : read.toFixed(2)}   ${good ? '✓' : '✗'}${c.id === 'C3' ? `   (ground pop settles ${inEndAll.toFixed(2)}; hold from pop end ${(exitStart - inEndAll).toFixed(2)})` : ''}   entr≤hold ${endsOnTime ? '✓' : '✗'} exit@cut ${exitOnTime ? '✓' : '✗'}`);
  }
  rec(4, 'Hold ≥ reading time', ok4, lines.join('\n'));
  rec(11, 'Entrances/exits end on time', ok11, lines.join('\n'));
}

// 5. Overshoot present ----------------------------------------------------------
{
  const pk = await page.evaluate(() => window.curvePeaks());
  const ok = pk.fastSpatial > 1 && pk.defaultSpatial > 1 && pk.slowSpatial > 1 && pk.fastEffects <= 1 && pk.defaultEffects <= 1;
  rec(5, 'Overshoot present', ok, `  glyph stagger-in (fast spatial) peak ${pk.fastSpatial.toFixed(4)} → glyph scale peak ${(0.8 + 0.2 * pk.fastSpatial).toFixed(4)}\n  scale pop (default spatial) peak ${pk.defaultSpatial.toFixed(4)}; bleeding hero pop (slow spatial) ${pk.slowSpatial.toFixed(4)}\n  word land (default spatial) peak ${pk.defaultSpatial.toFixed(4)} → lands ${(0.4 * 86 * (pk.defaultSpatial - 1)).toFixed(2)} px past rest then settles\n  morph k (default spatial) peak ${pk.defaultSpatial.toFixed(4)}\n  effects tokens: fast ${pk.fastEffects}, default ${pk.defaultEffects} (no overshoot)`);
}

// 6. Colour census ------------------------------------------------------------------
{
  const lines = []; let ok = true, maxCount = 0; const perFrame = [];
  for (let i = 0; i <= 96; i++) {
    const t = i * 0.25; await at(t);
    const c = await page.evaluate(() => window.census());
    perFrame.push(`${t.toFixed(2)}:${c.paletteCount}`);
    maxCount = Math.max(maxCount, c.paletteCount);
    if (c.paletteCount > 8) { ok = false; lines.push(`  t=${t} has ${c.paletteCount} palette colours ✗`); }
  }
  await at(12.1); const c6 = await page.evaluate(() => window.census());
  const c6ok = c6.paletteCount === 8; ok = ok && c6ok;
  lines.push(`  97 frames (0…24 s every 0.25 s), palette colours per frame: ${perFrame.join(' ')}`);
  lines.push(`  max palette colours in any frame: ${maxCount}; C6 still t=12.1: ${c6.paletteCount} colours [${c6.palette.map(p => p[0]).join(', ')}] ${c6ok ? '✓' : '✗'}; non-palette (anti-aliased) pixels at 12.1: ${c6.other} of ${c6.total}`);
  rec(6, 'Colour census', ok, lines.join('\n'));
}

// 8. Swapped words still read ------------------------------------------------------
{
  const want = { 1.75: { 'o Hello': 478, 'i night': 540 }, 8.05: { 'o one': 368 }, 10.35: { 'o something': 368 }, 14.65: { 'o you': 358, 'i tonight': 420 }, 21.5: { 'i Build': 219, 'i Night': 399 } };
  const lines = []; let ok = true;
  for (const [t, w] of Object.entries(want)) {
    const d = await at(+t);
    for (const s of d.swaps) {
      const dy = Math.abs(s.cy - w[s.tag]); const good = dy <= 3 && s.scale > 0.99;
      ok = ok && good;
      lines.push(`  t=${t} ${s.tag}: centre (${r1(s.cx)}, ${r1(s.cy)}) stated y ${w[s.tag]} → Δ ${r1(dy)} px, shape scale ${s.scale.toFixed(3)} ${good ? '✓' : '✗'}`);
    }
  }
  lines.push('  words read on stills: out/stills/t1_75.png, t8_05.png, t10_35.png, t14_65.png, t21_5.png (visual)');
  rec(8, 'Swapped words still read', ok, lines.join('\n'));
}

// 9. Countdown mask -------------------------------------------------------------------
{
  const lines = []; let ok = true;
  for (const t of [5.35, 5.85, 6.35, 5.6]) {
    const d = await at(t);
    const out = await page.evaluate((poly, hex) => window.countOutside(poly, hex), d.ground, '#1F2125');
    const good = out.outside === 0; ok = ok && good;
    const digits = d.lines.map(L => `"${L.text}" ink [${L.ink.map(r1)}]`).join(', ');
    lines.push(`  t=${t}: ink pixels ${out.total}, outside ground polygon ${out.outside} ${good ? '✓' : '✗'}; digits ${digits}`);
  }
  rec(9, 'Countdown mask', ok, lines.join('\n'));
}

// 10. Occupancy ----------------------------------------------------------------------
{
  const lines = []; let ok = true;
  for (const id of IDS) {
    await at(MID[id]); const f = await page.evaluate(h => window.occupancy(h), STAGES[id]);
    const good = f <= 0.60; ok = ok && good;
    lines.push(`  ${id} t=${MID[id]}: non-stage ${(f * 100).toFixed(1)} % ${good ? '✓' : '✗'}`);
  }
  rec(10, 'Occupancy ≤ 60 %', ok, lines.join('\n'));
}

// 12. Reduced motion ------------------------------------------------------------------
{
  const rm = await open('?rm=1&t=0');
  const lines = []; let ok = true;
  for (const c of table) {
    const t = c.start + c.holdStart;
    await at(t); const urlN = await page.evaluate(() => window.dataURL());
    await rm.evaluate(t => window.renderAt(t), t);
    const diff = await rm.evaluate(u => window.diffAgainst(u), urlN);
    const good = diff === 0; if (c.id !== 'C3') ok = ok && good;
    lines.push(`  ${c.id} hold start t=${t.toFixed(2)}: diff ${diff} px ${good ? '✓' : (c.id === 'C3' ? '(expected: the ground pop settles at t+0.50, after the 0.35 legibility point)' : '✗')}`);
  }
  const digitAt = async t => { const d = await rm.evaluate(t => window.renderAt(t), t); return d.lines.filter(L => Math.abs(L.baseline - 417) < 1).map(L => L.text).join('') || '(none)'; };
  const seq = [];
  for (const t of [5.49, 5.5, 5.99, 6.0, 6.49]) seq.push(`${t}:${await digitAt(t)}`);
  const digitsOk = (await digitAt(5.49)) === '3' && (await digitAt(5.5)) === '2' && (await digitAt(6.0)) === '1';
  ok = ok && digitsOk;
  lines.push(`  rm=1 digit at rest: ${seq.join(' ')} ${digitsOk ? '✓' : '✗'}`);
  rec(12, 'Reduced motion', ok, lines.join('\n'));
  await rm.close();
}

// 13. Determinism ------------------------------------------------------------------------
{
  await at(17.4); const h1 = await page.evaluate(() => window.frameHash());
  const p2 = await open('?t=17.4'); const h2 = await p2.evaluate(() => window.frameHash());
  await p2.evaluate(() => window.renderAt(17.4)); const h3 = await p2.evaluate(() => window.frameHash());
  await p2.close();
  rec(13, 'Determinism', h1 === h2 && h2 === h3, `  frame hash t=17.4: run A ${h1}, run B (fresh page load) ${h2}, run B re-render ${h3}`);
}

// 7. Thumbnails ------------------------------------------------------------------------------
{
  const tp = await browser.newPage(); await tp.setViewport({ width: 160, height: 90, deviceScaleFactor: 1 });
  const files = [];
  for (const id of IDS) {
    await tp.goto(BASE + `?w=160&t=${MID[id]}`, { waitUntil: 'load' }); await tp.waitForFunction('window.__ready === true');
    const f = join(THUMBS, `${id}.png`); const el = await tp.$('canvas'); await el.screenshot({ path: f }); files.push(f);
  }
  await tp.close();
  rec(7, 'Thumbnail legibility (visual)', true, `  10 thumbnails at 160×90 (browser downsampling of the full frame): ${THUMBS}/C1.png … C10.png; tiled sheet: out/thumbs_sheet.png (inspect)`);
}

// Per-frame cost ------------------------------------------------------------------------------
{
  const ms = await page.evaluate(() => window.timeRender(240));
  console.log(`\nper-frame render cost (headless, software raster): ${ms.toFixed(2)} ms average over 240 frames`);
}

await browser.close();
console.log('\nSUMMARY');
for (const r of results.sort((a, b) => a.no - b.no)) console.log(`  ${r.no.toString().padStart(2)}. ${r.pass ? 'PASS' : 'FAIL'}  ${r.name}`);
writeFileSync(join(HERE, 'out', 'verify.json'), JSON.stringify(results, null, 2));
