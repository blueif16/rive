// Render keeper to a 24 fps MP4: load index.html once in headless Chrome,
// call window.renderAt(t) for each of the 480 frames, pipe PNGs to ffmpeg.
//   node render.mjs [out.mp4]
import { spawn } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdirSync } from 'node:fs';

const HERE = dirname(fileURLToPath(import.meta.url));
const RENDER = join(HERE, '..', '.claude', 'skills', 'rive-animation', 'scripts', 'render');
const puppeteer = (await import(join(RENDER, 'node_modules', 'puppeteer-core', 'lib', 'puppeteer', 'puppeteer-core.js'))).default;
const { findChrome } = await import(join(RENDER, 'browser.mjs'));

const FPS = 24, DUR = 20, FRAMES = FPS * DUR;
const out = process.argv[2] || join(HERE, 'out', 'riso-keeper.mp4');
mkdirSync(dirname(out), { recursive: true });

const browser = await puppeteer.launch({
  executablePath: findChrome(), headless: true,
  // --disable-gpu pins Skia's software canvas: headless Chrome otherwise promotes the
  // canvases to SwiftShader GL after a few frames, where filter+multiply compositing breaks.
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars', '--disable-gpu'],
});
const page = await browser.newPage();
await page.setViewport({ width: 720, height: 720, deviceScaleFactor: 1 });
page.on('pageerror', e => process.stderr.write(`page error: ${e.message}\n`));
await page.goto(`file://${join(HERE, 'index.html')}?render=1`, { waitUntil: 'load' });
await page.waitForFunction('window.__ready === true', { timeout: 120000 });

const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'png', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let f = 0; f < FRAMES; f++) {
  const b64 = await page.evaluate(t => { window.renderAt(t); return window.frameCanvas.toDataURL('image/png').split(',')[1]; }, f / FPS);
  const ok = ff.stdin.write(Buffer.from(b64, 'base64'));
  if (!ok) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 48 === 0) process.stderr.write(`frame ${f}/${FRAMES}\n`);
}
ff.stdin.end();
const code = await new Promise(r => ff.on('close', r));
await browser.close();
process.stderr.write(`${out} (${FRAMES} frames, ffmpeg exit ${code}, ${((Date.now() - t0) / 1000).toFixed(1)} s)\n`);
process.exit(code);
