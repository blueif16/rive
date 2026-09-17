#!/usr/bin/env node
// One headless-browser pass over a .riv, driving @rive-app/canvas-advanced by a
// fixed timestep and writing PNG frames to stdout as an image2pipe stream.
//
// The alternative — `rive --screenshot` once per frame — rebuilds the .riv every
// time, which costs minutes for a minute of video. Here the file is loaded once
// and the state machine is stepped, so the cost per frame is a draw plus a PNG
// encode.
//
//   node render.mjs --riv=scene.riv --fps=30 --duration=52.5 > frames.pipe
//   node render.mjs --riv=scene.riv --info
//   node render.mjs --riv=scene.riv --stills=2,11.5,24 --stills-dir=out/
//
// Frames go to stdout; progress and diagnostics go to stderr, so stdout can be
// piped straight into ffmpeg.

import { writeFileSync, existsSync } from "node:fs";
import { join, resolve, basename } from "node:path";
import { open, die as bail } from "./browser.mjs";

const die = (msg) => bail("render", msg);

const pngFromDataUrl = (u) => Buffer.from(u.slice(u.indexOf(",") + 1), "base64");

// ------------------------------------------------------------------- main ---

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const m = a.match(/^--([^=]+)(?:=(.*))?$/);
    return m ? [m[1], m[2] ?? true] : [a, true];
  })
);

const rivPath = resolve(args.riv || die("--riv=<path> is required"));
if (!existsSync(rivPath)) die(`${rivPath} does not exist`);

const { page, close } = await open(rivPath);

try {
  if (args.info) {
    const info = await page.evaluate(() => window.describe());
    process.stdout.write(JSON.stringify(info, null, 2) + "\n");
  } else {
    const bootOpts = {
      width: Number(args.width) || 0, height: Number(args.height) || 0,
      artboard: args.artboard || null, stateMachine: args.sm || null,
      background: args.bg ? (String(args.bg).startsWith("#") ? args.bg : `#${args.bg}`) : null,
    };
    const info = await page.evaluate((o) => window.boot(o), bootOpts);
    if (args.animation) {
      const ok = await page.evaluate((n) => window.useAnimation(n), args.animation === true ? null : args.animation);
      if (!ok) die(`no animation named ${args.animation}`);
    }
    process.stderr.write(
      `  ${basename(rivPath)}${args.artboard ? ` [${args.artboard}]` : ""}: ` +
      `${info.width}x${info.height}, ${args.animation ? "animation " + args.animation : info.driver}\n`);

    for (const pair of String(args.input || "").split(",").filter(Boolean)) {
      const [k, v] = pair.split("=");
      const ok = await page.evaluate((k, v) => window.setInput(k, isNaN(+v) ? v === "true" : +v),
                                     k, v ?? "true");
      if (!ok) process.stderr.write(`  warning: no input named ${k}\n`);
    }

    const fps = Number(args.fps) || 30;
    const dt = 1 / fps;
    const BATCH = 12;   // fewer CDP round trips, bounded response size

    /** Pull `total` frames through the page in batches, handing each to `sink`. */
    async function pump(total, sink) {
      let done = 0;
      while (done < total) {
        const n = Math.min(BATCH, total - done);
        const urls = await page.evaluate((n, d) => window.renderBatch(n, d), n, dt);
        if (urls.length !== n) die(`page returned ${urls.length} of ${n} frames`);
        for (const u of urls) await sink(pngFromDataUrl(u), done++);
        process.stderr.write(`\r  rendering ${done}/${total} frames`);
      }
      process.stderr.write("\n");
    }

    if (args.stills) {
      // One continuous pass, saving only the frames the caller asked for — far
      // cheaper than re-seeking from t=0 for each still.
      const dir = args["stills-dir"] || ".";
      const wanted = new Map();
      for (const sec of String(args.stills).split(",").map(Number)) {
        wanted.set(Math.max(0, Math.round(sec * fps) - 1),
                   join(dir, `t${String(sec).replace(".", "_")}.png`));
      }
      const last = Math.max(...wanted.keys());
      await pump(last + 1, (png, i) => {
        const out = wanted.get(i);
        if (out) { writeFileSync(out, png); process.stderr.write(`\r  still ${out}\n`); }
      });
    } else {
      const total = Math.max(1, Math.round((Number(args.duration) || 2) * fps));
      await pump(total, async (png) => {
        if (!process.stdout.write(png)) {
          await new Promise((r) => process.stdout.once("drain", r));
        }
      });
    }
  }
} finally {
  await close();
}
