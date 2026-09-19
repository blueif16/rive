// Contact sheet: one frame every 0.5 s (49 frames) tiled 7×7 into out/sheet.png.
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import puppeteer from '/Users/tk/Desktop/brain/projects/rive/.claude/skills/rive-animation/scripts/render/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
const HERE = '/Users/tk/Desktop/brain/projects/rive/geo-buildnight';
mkdirSync(HERE + '/out/sheet', { recursive: true });
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--hide-scrollbars'] });
const page = await browser.newPage(); await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
await page.goto('file://' + HERE + '/index.html?t=0', { waitUntil: 'load' });
for (let i = 0; i <= 48; i++) {
  const url = await page.evaluate(t => { window.renderAt(t); return window.dataURL(); }, i * 0.5);
  writeFileSync(`${HERE}/out/sheet/f${String(i).padStart(2, '0')}.png`, Buffer.from(url.slice(url.indexOf(',') + 1), 'base64'));
}
await browser.close();
const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '1', '-i', HERE + '/out/sheet/f%02d.png', '-vf', 'scale=320:180,tile=7x7:padding=4:margin=4:color=0x1F2125', '-frames:v', '1', HERE + '/out/sheet.png'], { stdio: 'inherit' });
console.log('sheet exit', r.status);
