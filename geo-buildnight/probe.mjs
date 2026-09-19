// Quick layout probe: loads the page once, dumps font info and layout boxes.
import puppeteer from '/Users/tk/Desktop/brain/projects/rive/.claude/skills/rive-animation/scripts/render/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const URL = 'file:///Users/tk/Desktop/brain/projects/rive/geo-buildnight/index.html';
const times = process.argv.slice(2).map(Number);
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
page.on('pageerror', e => console.log('PAGE ERROR', e.message));
page.on('console', m => console.log('console:', m.text()));
await page.goto(URL + '?t=0', { waitUntil: 'load' });
console.log('font', JSON.stringify(await page.evaluate(() => window.fontInfo())));
console.log('peaks', JSON.stringify(await page.evaluate(() => window.curvePeaks())));
for (const t of times) {
  const d = await page.evaluate(t => window.renderAt(t), t);
  console.log(`\n== t=${t} ${d.card}`);
  for (const L of d.lines) console.log('  line', JSON.stringify(L.text), 'box', L.box.map(v => +v.toFixed(1)), 'ink', L.ink.map(v => +v.toFixed(1)));
  for (const s of d.shapes) console.log('  shape', s.tag, s.aabb.map(v => +v.toFixed(1)), 'scale', +s.scale.toFixed(3));
  for (const s of d.swaps) console.log('  swap', s.tag, +s.cx.toFixed(1), +s.cy.toFixed(1), 'scale', +s.scale.toFixed(3));
  for (const a of d.accents) console.log('  accent', a.tag, a.bbox.map(v => +v.toFixed(1)), 'reveal', +a.reveal.toFixed(2));
}
await browser.close();
