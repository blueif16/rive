// Headless-browser plumbing shared by render.mjs (frames out) and place.mjs
// (measurements out). Both load the same harness.html, so a measurement is
// taken from exactly the pixels the renderer would have written.

import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { existsSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

export const HERE = dirname(fileURLToPath(import.meta.url));
const PKG = join(HERE, "node_modules", "@rive-app", "canvas-advanced");

export function die(tool, msg) {
  process.stderr.write(`${tool}: ${msg}\n`);
  process.exit(1);
}

/** Chrome for Testing from a puppeteer cache, or the installed Chrome. */
export function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const cache = join(process.env.HOME, ".cache", "puppeteer");
  for (const kind of ["chrome-headless-shell", "chrome"]) {
    const dir = join(cache, kind);
    if (!existsSync(dir)) continue;
    const builds = readdirSync(dir)
      .filter((d) => d.startsWith("mac") || d.startsWith("linux") || d.startsWith("win"))
      .sort()
      .reverse();
    for (const b of builds) {
      for (const rel of [
        "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chrome-headless-shell-mac-arm64/chrome-headless-shell",
        "chrome-headless-shell-mac-x64/chrome-headless-shell",
        "chrome-linux64/chrome",
        "chrome-headless-shell-linux64/chrome-headless-shell",
      ]) {
        const p = join(dir, b, rel);
        if (existsSync(p)) return p;
      }
    }
  }
  for (const p of [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
  ]) {
    if (existsSync(p)) return p;
  }
  die("browser", "no Chrome found. Set CHROME_PATH, or `npx puppeteer browsers install chrome`.");
}

/** Serve the harness, the wasm and the .riv — fetch() needs http, not file://. */
async function serve(rivPath) {
  const routes = {
    "/": [join(HERE, "harness.html"), "text/html"],
    "/canvas_advanced.mjs": [join(PKG, "canvas_advanced.mjs"), "text/javascript"],
    "/rive.wasm": [join(PKG, "rive.wasm"), "application/wasm"],
    "/scene.riv": [rivPath, "application/octet-stream"],
  };
  const server = createServer(async (req, res) => {
    const hit = routes[req.url.split("?")[0]];
    if (!hit) return res.writeHead(404).end();
    try {
      const body = await readFile(hit[0]);
      res.writeHead(200, { "content-type": hit[1], "content-length": body.length });
      res.end(body);
    } catch (e) {
      res.writeHead(500).end(String(e));
    }
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  return { server, port: server.address().port };
}

export async function open(rivPath) {
  const { server, port } = await serve(rivPath);
  const browser = await puppeteer.launch({
    executablePath: findChrome(),
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage",
           "--enable-unsafe-swiftshader", "--hide-scrollbars"],
  });
  const page = await browser.newPage();
  page.on("pageerror", (e) => process.stderr.write(`  page error: ${e.message}\n`));
  await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "load" });
  await page.waitForFunction("window.__ready === true", { timeout: 30000 });
  const close = async () => { await browser.close(); server.close(); };
  return { page, close };
}
