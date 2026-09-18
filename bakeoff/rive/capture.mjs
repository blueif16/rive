// Capture harness: real-time screenshots of the running page, plus the exact
// transfer size of every request the browser makes.
//
// Headless Chrome's --virtual-time-budget clamps requestAnimationFrame deltas,
// so the animation only creeps forward and a chosen beat is unreachable that
// way. This drives a real browser instead and seeks the Rive instance the
// embed exposes on the <figure>.
//
//   node capture.mjs http://localhost:8099/
import { chromium } from "playwright-core";
import fs from "node:fs";

const URL_ = process.argv[2] || "http://localhost:8099/";
const OUT = "build/shots";
fs.mkdirSync(OUT, { recursive: true });

// Beat boundaries of the 13.6 s loop, in seconds, taken mid-beat.
const BEATS = { all: 1.6, renderer: 5.0, simulator: 8.4, planner: 11.8 };

const VIEWS = [
  { name: "desktop", width: 1440, height: 1560 },
  { name: "mobile", width: 390, height: 1560 }
];

const browser = await chromium.launch({ channel: "chrome" });

async function shoot(view, { beat = "all", reduce = false, suffix = "" } = {}) {
  const ctx = await browser.newContext({
    viewport: { width: view.width, height: view.height },
    deviceScaleFactor: 2,
    reducedMotion: reduce ? "reduce" : "no-preference"
  });
  const page = await ctx.newPage();

  const wire = [];
  page.on("response", async (res) => {
    try {
      const h = await res.allHeaders();
      wire.push({
        url: new URL(res.url()).pathname,
        status: res.status(),
        encoding: h["content-encoding"] || "identity",
        sent: Number(h["content-length"] || 0)
      });
    } catch { /* redirects and data: urls */ }
  });

  await page.goto(URL_, { waitUntil: "networkidle" });
  await page.waitForFunction(() => {
    const f = document.querySelector("figure.wmf");
    return f && f.rive;
  }, null, { timeout: 20000 });

  const artboard = await page.evaluate(() => {
    const f = document.querySelector("figure.wmf");
    return f.rive.activeArtboard;
  });

  if (!reduce) {
    // Pause, then seek: a screenshot of a playing loop lands wherever it lands.
    await page.evaluate((t) => {
      const r = document.querySelector("figure.wmf").rive;
      r.pause();
      r.scrub("Loop", t);
    }, BEATS[beat]);
    await page.waitForTimeout(250);
  }

  const fig = page.locator("figure.wmf");
  await fig.scrollIntoViewIfNeeded();
  await page.waitForTimeout(150);

  const file = `${OUT}/${view.name}${suffix}.png`;
  await page.screenshot({ path: file });
  await ctx.close();
  return { file, artboard, wire };
}

const report = {};
for (const view of VIEWS) {
  const r = await shoot(view, { beat: "all" });
  report[view.name] = { artboard: r.artboard, wire: r.wire };
  console.log(`${view.name.padEnd(8)} artboard=${r.artboard.padEnd(8)} -> ${r.file}`);
  for (const beat of ["renderer", "simulator", "planner"]) {
    await shoot(view, { beat, suffix: `-${beat}` });
  }
  await shoot(view, { reduce: true, suffix: "-reduced" });
}

fs.writeFileSync("build/wire.json", JSON.stringify(report, null, 1));

const w = report.desktop.wire.filter((x) => x.status === 200);
const total = w.reduce((a, b) => a + b.sent, 0);
console.log("\nbytes on the wire (desktop, brotli where offered):");
for (const x of w) console.log(`  ${String(x.sent).padStart(8)}  ${x.encoding.padEnd(9)} ${x.url}`);
console.log(`  ${String(total).padStart(8)}  TOTAL`);

await browser.close();
