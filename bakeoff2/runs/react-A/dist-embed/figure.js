import { jsxs as i, jsx as n } from "react/jsx-runtime";
import { useRef as B, useState as T, useEffect as E } from "react";
function P(t, o = 0.08) {
  const c = B(null), [r, m] = T(!1), [l, u] = T(!1), [h, w] = T(0);
  E(() => {
    const s = window.matchMedia("(prefers-reduced-motion: reduce)"), d = () => m(s.matches);
    return d(), s.addEventListener("change", d), () => s.removeEventListener("change", d);
  }, []), E(() => {
    const s = c.current;
    if (!s) return;
    const d = new IntersectionObserver(
      ([k]) => u(k.isIntersecting),
      { rootMargin: "10% 0px" }
    );
    return d.observe(s), () => d.disconnect();
  }, []);
  const p = l && !r;
  return E(() => {
    if (!p) return;
    let s = 0, d = performance.now();
    const k = (N) => {
      const g = Math.min((N - d) / 1e3, 0.1);
      d = N, w((D) => D + g), s = requestAnimationFrame(k);
    };
    return s = requestAnimationFrame(k), () => cancelAnimationFrame(s);
  }, [p]), { t: r ? o : h % t / t, elapsed: h, reduced: r, ref: c, running: p };
}
const $ = (t, o, c) => t + (o - t) * c, v = (t) => t < 0 ? 0 : t > 1 ? 1 : t, y = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
function q(t, o, c, r = 0.14) {
  const m = t * c, l = Math.min(
    Math.abs(m - o),
    Math.abs(m - o - c),
    Math.abs(m - o + c)
  );
  return l <= 0.5 - r ? 1 : l >= 0.5 + r ? 0 : y(1 - (l - (0.5 - r)) / (2 * r));
}
const A = 12, j = 4, z = 11.15 / A, L = 0.7, f = 32e3, a = 0.55, F = 1, S = 0.22, O = 0.9, b = 7.2, x = 9.9, C = {
  system: "var(--warm-dk)",
  user: "var(--indigo)",
  assistant: "var(--lavender)",
  "tool result": "var(--warm-lt)",
  summary: "var(--accent)"
}, R = [
  { id: "sys", kind: "system", tokens: 2400, enter: -3.2, inDur: a, chrono: 0 },
  { id: "sum2", kind: "summary", tokens: 3e3, enter: x + S, inDur: O },
  { id: "sum1", kind: "summary", tokens: 2200, enter: b + S, inDur: O, remove: x },
  { id: "t1", kind: "user", tokens: 1100, enter: -2.2, inDur: a, remove: b, chrono: 1 },
  { id: "t2", kind: "assistant", tokens: 2800, enter: -1.2, inDur: a, remove: b, chrono: 2 },
  { id: "t3", kind: "user", tokens: 900, enter: 1.4, inDur: a, remove: b, chrono: 3 },
  { id: "t4", kind: "assistant", tokens: 3400, enter: 2.4, inDur: a, remove: b, chrono: 4 },
  { id: "t5", kind: "tool result", tokens: 6800, enter: 3.3, inDur: a, remove: b, chrono: 5 },
  { id: "t6", kind: "user", tokens: 1200, enter: 4.1, inDur: a, remove: x, chrono: 6 },
  { id: "t7", kind: "assistant", tokens: 3900, enter: 4.8, inDur: a, remove: x, chrono: 7 },
  { id: "t8", kind: "tool result", tokens: 5900, enter: 5.6, inDur: a, remove: x, chrono: 8 },
  { id: "t9", kind: "user", tokens: 1e3, enter: 6.3, inDur: a, chrono: 9 },
  { id: "t10", kind: "assistant", tokens: 2300, enter: 6.9, inDur: a, chrono: 10 },
  { id: "t11", kind: "tool result", tokens: 7100, enter: 7.9, inDur: a, chrono: 11 },
  { id: "t12", kind: "user", tokens: 1300, enter: 8.6, inDur: a, chrono: 12 },
  { id: "t13", kind: "assistant", tokens: 3600, enter: 9.2, inDur: a, chrono: 13 },
  { id: "t14", kind: "tool result", tokens: 6800, enter: 10.5, inDur: a, chrono: 14 },
  { id: "t15", kind: "user", tokens: 1100, enter: 11, inDur: a, chrono: 15 },
  { id: "t16", kind: "assistant", tokens: 2900, enter: 11.5, inDur: a, chrono: 16 }
], G = R.filter((t) => t.chrono !== void 0).sort(
  (t, o) => t.chrono - o.chrono
), H = 0.058, V = [
  {
    title: "A fixed budget",
    sub: "A context window is not a memory — it is a width. Three turns in, most of it is free, and that width is all there will ever be."
  },
  {
    title: "The history grows",
    sub: "Every turn takes room in proportion to its size, and a single tool result can take more than the whole conversation before it. The bar does not grow with it."
  },
  {
    title: "Something has to give",
    sub: "Full. The oldest turns dim and collapse into one small summary, and the space they give back is taken by new arrivals almost immediately."
  },
  {
    title: "Steady state",
    sub: "A long conversation, compacted to a sliver. Only the most recent turns are still held in full — the rest the model knows only as a summary."
  }
];
function I(t) {
  const o = [];
  let c = 0, r = 0, m = 0;
  for (const e of R) {
    const s = y(v((t - e.enter) / e.inDur)), d = e.remove === void 0 ? 0 : y(v((t - e.remove - S) / O)), k = e.remove === void 0 ? 0 : y(v((t - e.remove) / F)), N = s * (1 - d), g = s * (1 - k), D = e.tokens / f * N;
    r += e.tokens * N, e.kind === "summary" && g > m && (m = g), D > 2e-4 && o.push({ id: e.id, kind: e.kind, x: c, w: D, opacity: g, tokens: e.tokens }), c += D;
  }
  const l = r / f, u = [];
  let h = 0, w = 0;
  for (const e of G) {
    const s = y(v((t - e.enter) / e.inDur)), d = e.remove === void 0 ? 0 : y(v((t - e.remove) / F)), k = e.tokens / f * s;
    s > 0.5 && (w += 1), u.push({
      id: e.id,
      kind: e.kind,
      x: 0,
      before: h,
      w: k,
      opacity: $(0.92, 0.24, d),
      tokens: e.tokens
    }), h += k;
  }
  const p = u.filter((e) => e.w > 2e-4).map((e) => ({ id: e.id, kind: e.kind, x: l - h + e.before, w: e.w, opacity: e.opacity, tokens: e.tokens }));
  return {
    blocks: o,
    rail: p,
    used: r,
    usedFrac: l,
    turns: w,
    everTokens: h * f,
    pressure: v((l - 0.9) / 0.07),
    compacted: m
  };
}
const X = (t) => Math.round(t / 100) * 100, _ = (t) => X(t).toLocaleString("en-US");
function M(t) {
  return `translate3d(${(t * 100).toFixed(3)}%, 0, 0)`;
}
function U(t, o) {
  return `max(0px, calc(${(t * 100).toFixed(3)}% - ${o}px))`;
}
function Y({ p: t }) {
  const o = C[t.kind];
  return /* @__PURE__ */ n("div", { className: "cw-pos", style: { transform: M(t.x), opacity: t.opacity }, children: /* @__PURE__ */ i(
    "div",
    {
      className: t.kind === "summary" ? "cw-blk cw-blk--sum" : "cw-blk",
      style: { width: U(t.w, 2) },
      children: [
        /* @__PURE__ */ n("div", { className: "cw-tint", style: { background: o } }),
        /* @__PURE__ */ n("div", { className: "cw-cap", style: { background: o } }),
        t.tokens / f >= H && /* @__PURE__ */ i("div", { className: "cw-txt fade-right", children: [
          /* @__PURE__ */ n("span", { className: "cw-kind", children: t.kind }),
          /* @__PURE__ */ n("span", { className: "cw-tok", children: t.tokens.toLocaleString("en-US") })
        ] })
      ]
    }
  ) });
}
function W({ p: t }) {
  return /* @__PURE__ */ n("div", { className: "cw-pos", style: { transform: M(t.x), opacity: t.opacity }, children: /* @__PURE__ */ n("div", { className: "cw-seg", style: { width: U(t.w, 1.5), background: C[t.kind] } }) });
}
function Q() {
  const { t, ref: o } = P(A, z), c = t * A, r = y(v((c - (A - L)) / L)), m = I(c), l = r > 1e-3 ? I(c - A) : null, u = [{ k: "a", s: m, o: 1 - r }];
  l && u.push({ k: "b", s: l, o: r });
  const h = (e) => e(m) * (1 - r) + (l ? e(l) * r : 0), w = h((e) => e.pressure), p = h((e) => e.compacted);
  return /* @__PURE__ */ i(
    "figure",
    {
      ref: o,
      className: "figure figure-cw",
      role: "img",
      "aria-label": "A context window is a fixed budget, not a memory. A bar of unchanging width fills with conversation turns sized in proportion to their token count — system prompt, user turns, assistant replies and large tool results. A counter climbs toward the 32,000-token limit; when the bar is full the oldest turns dim and collapse into a single small summary block, the counter drops, and new turns immediately take the reclaimed space. A rail beneath the bar shows the whole conversation at the same scale, running off the left edge of the frame: the history keeps growing while the window never does.",
      children: [
        /* @__PURE__ */ i("div", { className: "cw-hdr", children: [
          /* @__PURE__ */ n("span", { className: "label", children: "What a context window holds" }),
          /* @__PURE__ */ n("div", { className: "cw-beats", children: V.map((e, s) => /* @__PURE__ */ i("div", { className: "cw-beat", style: { opacity: q(t, s, j) }, children: [
            /* @__PURE__ */ n("span", { className: "title", children: e.title }),
            /* @__PURE__ */ n("p", { className: "cw-sub", children: e.sub })
          ] }, e.title)) })
        ] }),
        /* @__PURE__ */ i("div", { children: [
          /* @__PURE__ */ i("div", { className: "cw-meter", children: [
            /* @__PURE__ */ i("div", { className: "cw-meter-l", children: [
              /* @__PURE__ */ i("span", { className: "label", children: [
                "Context window · capacity ",
                f.toLocaleString("en-US"),
                " tokens"
              ] }),
              /* @__PURE__ */ n("span", { className: "label cw-atcap", style: { opacity: w }, children: "At capacity" })
            ] }),
            /* @__PURE__ */ n("div", { className: "cw-count", children: u.map((e) => /* @__PURE__ */ i("div", { className: "cw-count-in", style: { opacity: e.o }, children: [
              /* @__PURE__ */ n("span", { className: "label", children: "Used" }),
              /* @__PURE__ */ n("span", { className: "cw-num", children: _(e.s.used) }),
              /* @__PURE__ */ i("span", { className: "cw-tot", children: [
                "/ ",
                f.toLocaleString("en-US")
              ] })
            ] }, e.k)) })
          ] }),
          /* @__PURE__ */ i("div", { className: "cw-bar", style: { marginTop: "clamp(9px, 1.3vw, 14px)" }, children: [
            [0.25, 0.5, 0.75].map((e) => /* @__PURE__ */ n("div", { className: "cw-tick", style: { left: `${e * 100}%` } }, e)),
            u.map((e) => /* @__PURE__ */ i("div", { className: "cw-layer", style: { opacity: e.o }, children: [
              e.s.blocks.map((s) => /* @__PURE__ */ n(Y, { p: s }, s.id)),
              /* @__PURE__ */ i("div", { className: "cw-pos", style: { transform: M(e.s.usedFrac), opacity: 0.85 }, children: [
                /* @__PURE__ */ n("div", { className: "cw-edge" }),
                /* @__PURE__ */ n("div", { className: "cw-edge-dot" })
              ] })
            ] }, e.k)),
            /* @__PURE__ */ n("div", { className: "cw-full", style: { opacity: w } })
          ] })
        ] }),
        /* @__PURE__ */ i("div", { className: "cw-railwrap", children: [
          /* @__PURE__ */ n("div", { className: "cw-row", children: /* @__PURE__ */ n("div", { className: "cw-stack", children: u.map((e) => /* @__PURE__ */ i("span", { className: "label", style: { opacity: e.o }, children: [
            "The conversation so far · ",
            e.s.turns,
            " turns · ",
            _(e.s.everTokens),
            " tokens"
          ] }, e.k)) }) }),
          /* @__PURE__ */ n("div", { className: "cw-rail fade-left", children: u.map((e) => /* @__PURE__ */ n("div", { className: "cw-layer", style: { opacity: e.o }, children: e.s.rail.map((s) => /* @__PURE__ */ n(W, { p: s }, s.id)) }, e.k)) }),
          /* @__PURE__ */ i("div", { className: "cw-row", children: [
            /* @__PURE__ */ n("span", { className: "label", style: { opacity: p }, children: "Compacted" }),
            /* @__PURE__ */ n("span", { className: "label", children: "Held in full" })
          ] })
        ] }),
        /* @__PURE__ */ n("div", { className: "cw-legend", children: ["system", "user", "assistant", "tool result", "summary"].map((e) => /* @__PURE__ */ i("span", { className: "cw-leg", children: [
          /* @__PURE__ */ n("span", { className: "cw-sw", style: { background: C[e] } }),
          /* @__PURE__ */ n("span", { className: "name", children: e })
        ] }, e)) })
      ]
    }
  );
}
export {
  Q as Figure
};
