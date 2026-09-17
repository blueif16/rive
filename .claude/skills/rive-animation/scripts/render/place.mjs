#!/usr/bin/env node
// Placement measurement for a .riv — numbers and a bitmask instead of a picture.
//
// Why pixels: the runtime exposes worldTransform() for a named node but no
// width/height, and `rive inspect --json`'s computedWorld*/computedWidth are
// always 0 (they are runtime-derived, and inspect is a static resolve). The
// painted frame is the only source of truth for where something actually is.
//
// So: extents come from the frame buffer, NAMES come from worldTransform — a
// named node's world origin picks out which painted blob is which.
//
//   node place.mjs --riv=x.riv --at=17.7
//   node place.mjs --riv=x.riv --at=2,17.7,43.3 --cols=80
//   node place.mjs --riv=x.riv --at=17.7 --nodes=TeacherArt,Bubble
//   node place.mjs --riv=x.riv --at=17.7 --regions=layout.json --json
//   node place.mjs --riv=x.riv --sweep=0:52.5:0.25 --regions=layout.json --rules=rules.json
//
// Exits 1 if any rule fails, so it works as a build gate.

import { readFileSync, existsSync } from "node:fs";
import { resolve, basename } from "node:path";
import { open, die as bail } from "./browser.mjs";

const die = (msg) => bail("place", msg);

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const m = a.match(/^--([^=]+)(?:=(.*))?$/);
    return m ? [m[1], m[2] ?? true] : [a, true];
  })
);

const rivPath = resolve(args.riv || die("--riv=<path> is required"));
if (!existsSync(rivPath)) die(`${rivPath} does not exist`);

const fps = Number(args.fps) || 60;          // measurement timebase
const cols = Number(args.cols) || 60;
const threshold = Number(args.threshold) || 24;
const minPx = Number(args.minPx) || 120;
const nodeNames = String(args.nodes || "").split(",").map((s) => s.trim()).filter(Boolean);
const regions = args.regions ? JSON.parse(readFileSync(args.regions, "utf8")) : null;
const rules = args.rules ? JSON.parse(readFileSync(args.rules, "utf8")) : null;

/** Timestamps to measure: an explicit list, or a start:end:step sweep. */
function timestamps() {
  if (args.sweep) {
    const [a, b, s] = String(args.sweep).split(":").map(Number);
    if (![a, b, s].every(Number.isFinite) || s <= 0) die("--sweep=start:end:step");
    const out = [];
    for (let t = a; t <= b + 1e-9; t += s) out.push(Math.round(t * 1e4) / 1e4);
    return out;
  }
  const list = String(args.at ?? "1").split(",").map(Number);
  if (list.some((n) => !Number.isFinite(n))) die("--at takes seconds, comma separated");
  return list;
}

// ------------------------------------------------------------------ boxes ---

const overlap = (a, b) => {
  const x = Math.min(a[2], b[2]) - Math.max(a[0], b[0]);
  const y = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
  return x > 0 && y > 0 ? x * y : 0;
};
const boxOf = (c) => [c.x0, c.y0, c.x1, c.y1];
const area = (b) => Math.max(0, b[2] - b[0]) * Math.max(0, b[3] - b[1]);

/** Every named box available at a timestamp: probed nodes first, then regions. */
function namedBoxes(shot) {
  const out = new Map();
  if (shot.nodes) {
    for (const [n, v] of Object.entries(shot.nodes)) {
      if (!v || v.component === null) continue;
      const c = shot.components.find((k) => k.id === v.component);
      if (c) out.set(n, boxOf(c));
    }
  }
  if (shot.regions) {
    for (const [n, r] of Object.entries(shot.regions)) {
      if (r.inkBox) out.set(n, r.inkBox);
      else if (!out.has(n)) out.set(n, null);      // named, but nothing painted
    }
  }
  return out;
}

/**
 * Names whose ink landed in the same connected blob. Two drawables sharing a
 * component are touching or overlapping — this is the sharpest overlap signal
 * the pixels give, and it needs no threshold.
 */
function sharedComponents(shot) {
  const byComp = new Map();
  for (const [n, v] of Object.entries(shot.nodes ?? {})) {
    if (!v || v.component === null) continue;
    byComp.set(v.component, [...(byComp.get(v.component) ?? []), n]);
  }
  return [...byComp.entries()].filter(([, ns]) => ns.length > 1);
}

const RULES = {
  not_overlapping: (a, b) => [overlap(a, b) === 0, `overlap ${overlap(a, b)}px²`],
  above: (a, b) => [a[3] <= b[1], `a.y1=${a[3]} vs b.y0=${b[1]}`],
  below: (a, b) => [a[1] >= b[3], `a.y0=${a[1]} vs b.y1=${b[3]}`],
  left_of: (a, b) => [a[2] <= b[0], `a.x1=${a[2]} vs b.x0=${b[0]}`],
  right_of: (a, b) => [a[0] >= b[2], `a.x0=${a[0]} vs b.x2=${b[2]}`],
  contains: (a, b) => [a[0] <= b[0] && a[1] <= b[1] && a[2] >= b[2] && a[3] >= b[3],
                       `b escapes a`],
  // Same box => the two names resolved to one connected blob: they touch.
  disconnected: (a, b) => [!(a[0] === b[0] && a[1] === b[1] && a[2] === b[2] && a[3] === b[3])
                           && overlap(a, b) === 0,
                           `ink is connected / overlapping`],
};

/** Evaluate every rule against one measured frame. */
function check(shot) {
  if (!rules) return [];
  const boxes = namedBoxes(shot);
  const fails = [];
  for (const r of rules) {
    const type = r.type ?? r.rule;
    const fn = RULES[type];
    if (!fn) { fails.push({ ...r, why: `unknown rule "${type}"` }); continue; }
    const a = boxes.get(r.a), b = boxes.get(r.b);
    if (!a || !b) {
      // A missing box is only a failure if the rule needed it to be there.
      if (r.requirePresent !== false) {
        fails.push({ ...r, why: `no ink for ${!a ? r.a : r.b}` });
      }
      continue;
    }
    const gap = Number(r.gap) || 0;
    const pad = gap ? [a[0] - gap, a[1] - gap, a[2] + gap, a[3] + gap] : a;
    const [ok, detail] = fn(pad, b);
    if (!ok) fails.push({ ...r, why: detail });
  }
  return fails;
}

// ----------------------------------------------------------------- render ---

const RAMP = " .:+#@";
const cellChar = (f) =>
  f <= 0 ? RAMP[0] : f < 0.12 ? RAMP[1] : f < 0.37 ? RAMP[2]
  : f < 0.62 ? RAMP[3] : f < 0.87 ? RAMP[4] : RAMP[5];

function drawGrid(shot) {
  const w = String(shot.rows - 1).length;
  const lines = [];
  // Column ruler: tens on the first line, units on the second.
  let tens = "", ones = "";
  for (let x = 0; x < shot.cols; x++) {
    tens += x % 10 === 0 ? String((x / 10) % 10) : " ";
    ones += String(x % 10);
  }
  lines.push(" ".repeat(w + 1) + tens);
  lines.push(" ".repeat(w + 1) + ones);
  shot.grid.forEach((row, y) => {
    lines.push(String(y).padStart(w) + "|" + row.map(cellChar).join("") + "|");
  });
  return lines.join("\n");
}

function report(t, shot, fails) {
  const L = [];
  const px = (n) => String(Math.round(n)).padStart(5);
  L.push(`t=${t.toFixed(2)}s  ink ${(shot.inkFraction * 100).toFixed(1)}%  ` +
         `grid ${shot.cols}x${shot.rows} cell ${shot.cellW.toFixed(1)}x${shot.cellH.toFixed(1)}px`);
  if (!args.nogrid) L.push(drawGrid(shot));

  L.push(`components  ${shot.components.length} shown of ${shot.componentsTotal} (>=${minPx}px)`);
  L.push("  id     x0    y0    x1    y1      w     h       px  name");
  for (const c of shot.components) {
    L.push(`  ${String(c.id).padStart(2)} ${px(c.x0)} ${px(c.y0)} ${px(c.x1)} ${px(c.y1)}` +
           ` ${px(c.w)} ${px(c.h)} ${String(c.px).padStart(8)}  ${c.name ?? ""}`);
  }

  if (shot.nodes) {
    L.push("nodes  (world origin from worldTransform — an ORIGIN, not an extent)");
    for (const [n, v] of Object.entries(shot.nodes)) {
      L.push(v ? `  ${n.padEnd(20)} ${v.x.toFixed(1)},${v.y.toFixed(1)}  ` +
                 `${v.component === null ? "(origin outside every blob)"
                    : `component ${v.component}${v.approx ? " ~nearest" : ""}`}`
                : `  ${n.padEnd(20)} not found`);
    }
    for (const [id, names] of sharedComponents(shot)) {
      L.push(`  TOUCHING: ${names.join(" + ")} share component ${id} — one blob of ink`);
    }
  }

  if (shot.regions) {
    L.push("regions");
    L.push("  name                 cover    inkPx  inkbox x0,y0,x1,y1");
    for (const [n, r] of Object.entries(shot.regions)) {
      L.push(`  ${n.padEnd(20)} ${(r.coverage * 100).toFixed(1).padStart(5)}% ` +
             `${String(r.inkPx).padStart(8)}  ${r.inkBox ? r.inkBox.join(",") : "(empty)"}`);
    }
    const names = Object.keys(shot.regions);
    const hits = [];
    for (let i = 0; i < names.length; i++)
      for (let j = i + 1; j < names.length; j++) {
        const a = shot.regions[names[i]].inkBox, b = shot.regions[names[j]].inkBox;
        if (a && b) { const o = overlap(a, b);
          if (o > 0) hits.push(`  ${names[i]} x ${names[j]}  ${o}px²  ` +
                               `(${(o / Math.min(area(a), area(b)) * 100).toFixed(1)}% of smaller)`); }
      }
    L.push(`collisions: ${hits.length ? "" : "none"}`);
    L.push(...hits);
  }

  if (rules) {
    L.push(`rules: ${fails.length ? `${fails.length} FAILED` : "all pass"}`);
    for (const f of fails) L.push(`  FAIL ${f.type ?? f.rule}(${f.a}, ${f.b})  ${f.why}`);
  }
  return L.join("\n");
}

// ------------------------------------------------------------------- main ---

const { page, close } = await open(rivPath);
let failed = 0;

try {
  const info = await page.evaluate((o) => window.boot(o), {
    width: Number(args.width) || 0, height: Number(args.height) || 0,
    artboard: args.artboard || null, stateMachine: args.sm || null,
    background: args.bg ? (String(args.bg).startsWith("#") ? args.bg : `#${args.bg}`) : null,
  });
  process.stderr.write(`  ${basename(rivPath)}: ${info.width}x${info.height}, ${info.driver}\n`);

  const times = timestamps();
  const shots = [];
  let frame = 0;                       // frames already advanced — one pass, no re-seek

  for (const t of times) {
    const want = Math.max(1, Math.round(t * fps));
    if (want > frame) { await page.evaluate((n, d) => window.advanceFrames(n, d), want - frame, 1 / fps); frame = want; }
    const shot = await page.evaluate((o) => window.analyze(o),
                                     { cols, threshold, minPx, regions,
                                       rows: Number(args.rows) || 0 });

    // Name a blob by the world origin of a named node that falls inside it.
    for (const name of nodeNames) {
      const n = await page.evaluate((nm) => window.probeNode(nm), name);
      if (!n) { (shot.nodes ??= {})[name] = null; continue; }
      // A node's origin often sits exactly on its own edge (a rect's top-left),
      // so an exact containment test misses by a fraction of a pixel.
      const pad = Number(args.anchorPad) || 2;
      let hit = shot.components.find(
        (c) => n.tx >= c.x0 - pad && n.tx <= c.x1 + pad &&
               n.ty >= c.y0 - pad && n.ty <= c.y1 + pad);
      // A rig's origin is often a floor/pivot point that sits off its own
      // artwork entirely (a docked character). Fall back to the nearest blob,
      // but only within a stated radius, and flag it so it is never silently
      // wrong — a mis-attributed name would make the whole gate lie.
      let approx = false;
      if (!hit) {
        // Deliberately TIGHT. This exists to rescue a pivot sitting a couple of
        // pixels off its own artwork, nothing more. Widen it and a node that is
        // not painted at all adopts whatever blob happens to be nearby — which
        // reads as a collision that is not there.
        const reach = Number(args.anchorReach) || 8;
        let best = null, bestD = Infinity;
        for (const c of shot.components) {
          const dx = Math.max(c.x0 - n.tx, 0, n.tx - c.x1);
          const dy = Math.max(c.y0 - n.ty, 0, n.ty - c.y1);
          const d = Math.hypot(dx, dy);
          if (d < bestD) { bestD = d; best = c; }
        }
        if (best && bestD <= reach) { hit = best; approx = true; }
      }
      if (hit) hit.name = hit.name ? `${hit.name},${name}` : name;
      (shot.nodes ??= {})[name] =
        { x: n.tx, y: n.ty, component: hit ? hit.id : null, approx };
    }

    const fails = check(shot);
    if (fails.length) failed++;
    shots.push({ t, shot, fails });
  }

  if (args.json) {
    process.stdout.write(JSON.stringify(
      shots.map(({ t, shot, fails }) => ({ t, ...shot, failures: fails })), null, 2) + "\n");
  } else if (args.sweep) {
    // A sweep is a gate: print only the frames that broke a rule.
    process.stdout.write(
      `swept ${shots.length} frames ${times[0]}..${times[times.length - 1]}s\n`);
    for (const { t, shot, fails } of shots) {
      if (!fails.length) continue;
      process.stdout.write(`\nt=${t.toFixed(2)}s\n`);
      for (const f of fails) process.stdout.write(`  FAIL ${f.type ?? f.rule}(${f.a}, ${f.b})  ${f.why}\n`);
    }
    process.stdout.write(failed ? `\n${failed}/${shots.length} frames failed\n`
                                : `all ${shots.length} frames pass\n`);
  } else {
    process.stdout.write(shots.map(({ t, shot, fails }) => report(t, shot, fails)).join("\n\n") + "\n");
  }
} finally {
  await close();
}

process.exit(failed ? 1 : 0);
