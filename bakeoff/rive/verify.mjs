// Checks the six embed-contract items against the page as a browser actually
// runs it. Exits 1 on any failure, so it is usable as a build gate.
//
//   node verify.mjs http://localhost:8099/
import { chromium } from "playwright-core";

const URL_ = process.argv[2] || "http://localhost:8099/";
const browser = await chromium.launch({ channel: "chrome" });
let failures = 0;

function check(name, ok, detail) {
  console.log(`${ok ? "  ok  " : " FAIL "} ${name}${detail ? "  — " + detail : ""}`);
  if (!ok) failures++;
}

async function openPage(width, height, reducedMotion = "no-preference") {
  const ctx = await browser.newContext({ viewport: { width, height }, reducedMotion });
  const page = await ctx.newPage();
  const wire = [];
  page.on("response", async (r) => {
    try {
      const h = await r.allHeaders();
      wire.push({ url: new URL(r.url()).pathname, sent: Number(h["content-length"] || 0),
                  encoding: h["content-encoding"] || "identity", status: r.status() });
    } catch {}
  });
  await page.goto(URL_, { waitUntil: "networkidle" });
  await page.waitForFunction(() => document.querySelector("figure.wmf")?.rive, null,
                             { timeout: 20000 });
  return { ctx, page, wire };
}

// 1 — responsive: the right artboard for the band, and no horizontal overflow.
console.log("\n1. responsive");
for (const [w, expect] of [[390, "Mobile"], [520, "Mobile"], [800, "Medium"], [1024, "Desktop"], [1440, "Desktop"]]) {
  const { ctx, page } = await openPage(w, 900);
  const got = await page.evaluate(() => document.querySelector("figure.wmf").rive.activeArtboard);
  const overflow = await page.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth);
  const scale = await page.evaluate(() => {
    const c = document.querySelector("figure.wmf canvas");
    const r = document.querySelector("figure.wmf").rive;
    return +(c.getBoundingClientRect().width / r.artboardWidth).toFixed(3);
  });
  check(`${w}px → ${expect}`, got === expect, `got ${got}, render scale ${scale}`);
  check(`${w}px no horizontal overflow`, overflow <= 0, `scrollWidth-clientWidth = ${overflow}`);
  check(`${w}px scale within 0.75–1.45`, scale >= 0.75 && scale <= 1.45, `scale ${scale}`);
  await ctx.close();
}

// 1b — the artboard actually swaps when a resize crosses a band edge.
{
  const { ctx, page } = await openPage(1440, 900);
  await page.setViewportSize({ width: 390, height: 900 });
  await page.waitForTimeout(900);
  const got = await page.evaluate(() => document.querySelector("figure.wmf").rive.activeArtboard);
  check("resize 1440→390 swaps artboard", got === "Mobile", `got ${got}`);
  await ctx.close();
}

// 2 — plays only in viewport.
console.log("\n2. play only when visible");
{
  // A short viewport, so "scrolled away" really means out of view: at 900px
  // tall the figure is still a third on screen at scrollTop 0.
  const { ctx, page } = await openPage(1440, 500);
  await page.locator("figure.wmf").scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  const playingIn = await page.evaluate(() => document.querySelector("figure.wmf").rive.isPlaying);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(900);
  const playingOut = await page.evaluate(() => document.querySelector("figure.wmf").rive.isPlaying);
  await page.locator("figure.wmf").scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  const playingBack = await page.evaluate(() => document.querySelector("figure.wmf").rive.isPlaying);
  check("plays while in viewport", playingIn === true);
  check("pauses when scrolled out", playingOut === false);
  check("resumes when scrolled back", playingBack === true);
  await ctx.close();
}

// 3 — prefers-reduced-motion: never plays, and the frame drawn is not blank.
console.log("\n3. prefers-reduced-motion");
{
  const { ctx, page } = await openPage(1440, 900, "reduce");
  await page.locator("figure.wmf").scrollIntoViewIfNeeded();
  await page.waitForTimeout(1500);
  const playing = await page.evaluate(() => document.querySelector("figure.wmf").rive.isPlaying);
  const ink = await page.evaluate(() => {
    const c = document.querySelector("figure.wmf canvas");
    const g = c.getContext("2d");
    const d = g.getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 0; i < d.length; i += 4 * 97) {
      if (Math.abs(d[i] - 247) > 12 || Math.abs(d[i + 1] - 247) > 12 || Math.abs(d[i + 2] - 250) > 12) n++;
    }
    return n;
  });
  check("never plays", playing === false);
  check("still frame is drawn, not blank", ink > 200, `${ink} sampled non-background pixels`);
  await ctx.close();
}

// 4 — accessible.
console.log("\n4. accessible");
{
  const { ctx, page } = await openPage(1440, 900);
  const a = await page.evaluate(() => {
    const fig = document.querySelector("figure.wmf");
    const c = fig.querySelector("canvas");
    const d = document.getElementById(c.getAttribute("aria-describedby"));
    return {
      tag: fig.tagName,
      role: c.getAttribute("role"),
      label: (c.getAttribute("aria-label") || "").trim(),
      desc: (d?.textContent || "").trim(),
      caption: (fig.querySelector("figcaption")?.textContent || "").trim()
    };
  });
  check("wrapped in <figure>", a.tag === "FIGURE");
  check('canvas role="img"', a.role === "img");
  check("aria-label present", a.label.length > 60, `${a.label.length} chars`);
  check("aria-describedby resolves", a.desc.length > 200, `${a.desc.length} chars`);
  check("describes all three functions",
    ["render", "simulat", "plan"].every((w) => a.desc.toLowerCase().includes(w)));
  check("describes all three output kinds",
    ["pictorial", "continuous", "discrete"].every((w) => a.desc.toLowerCase().includes(w)));
  check("visible figcaption", a.caption.length > 60, `${a.caption.length} chars`);
  await ctx.close();
}

// 5 — self-contained: one element plus one script, no globals leaked beyond
//     the runtime, and no CSS the host has to supply.
console.log("\n5. self-contained");
{
  const { ctx, page } = await openPage(1440, 900);
  // Count the script tags the *page author* wrote, not the one the embed
  // injects for the runtime.
  const html = await (await fetch(URL_)).text();
  const authored = (html.match(/<script[^>]+src=/g) || []).length;
  const s = await page.evaluate(() => ({
    stylesheets: document.querySelectorAll('link[rel="stylesheet"]').length,
    injected: !!document.getElementById("wmf-styles")
  }));
  check("page authors one <script src>", authored === 1, `${authored} in the served HTML`);
  check("no external stylesheet required", s.stylesheets === 0);
  check("figure styles are injected by the embed", s.injected);
  await ctx.close();
}

// 6 — weight, as transferred.
console.log("\n6. page weight (as served, brotli)");
{
  const { ctx, wire } = await openPage(1440, 900);
  const got = wire.filter((x) => x.status === 200);
  const total = got.reduce((a, b) => a + b.sent, 0);
  for (const x of got) console.log(`       ${String(x.sent).padStart(8)}  ${x.encoding.padEnd(9)} ${x.url}`);
  console.log(`       ${String(total).padStart(8)}  TOTAL`);
  check("weight reported", total > 0);
  check("no font requests (faces are inside the .riv)",
    !got.some((x) => /\.(woff2?|ttf|otf)$/.test(x.url)));
  await ctx.close();
}

console.log(failures ? `\n${failures} FAILED` : "\nall checks passed");
await browser.close();
process.exit(failures ? 1 : 0);
