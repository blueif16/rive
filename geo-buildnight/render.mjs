// Render geo-buildnight/index.html to a 24 fps H.264 MP4.
// Loads the page once in headless Chrome (puppeteer-core), calls window.renderAt(t)
// for each of the 576 frames, grabs canvas.toDataURL and pipes PNGs into ffmpeg.
//   node render.mjs [out.mp4]
import { spawn } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdirSync } from 'node:fs';
import puppeteer from '/Users/tk/Desktop/brain/projects/rive/.claude/skills/rive-animation/scripts/render/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PAGE = 'file://' + join(HERE, 'index.html') + '?t=0';
const OUT = process.argv[2] || join(HERE, 'out', 'buildnight.mp4');
const FPS = 24, DUR = 24, FRAMES = FPS * DUR;
mkdirSync(dirname(OUT), { recursive: true });

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
page.on('pageerror', e => process.stderr.write(`page error: ${e.message}\n`));
await page.goto(PAGE, { waitUntil: 'load' });
await page.waitForFunction('window.__ready === true');

const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'png', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
const write = buf => new Promise(res => { if (!ff.stdin.write(buf)) ff.stdin.once('drain', res); else res(); });

const t0 = Date.now();
for (let f = 0; f < FRAMES; f++) {
  const url = await page.evaluate(t => { window.renderAt(t); return window.dataURL(); }, f / FPS);
  await write(Buffer.from(url.slice(url.indexOf(',') + 1), 'base64'));
  if (f % 48 === 0) process.stderr.write(`frame ${f}/${FRAMES}\n`);
}
ff.stdin.end();
await new Promise((res, rej) => ff.on('close', code => code === 0 ? res() : rej(new Error('ffmpeg exit ' + code))));
await browser.close();
process.stderr.write(`wrote ${OUT} (${FRAMES} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s)\n`);
