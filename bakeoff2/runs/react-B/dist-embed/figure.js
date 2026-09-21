import { jsxs as M, jsx as s } from "react/jsx-runtime";
import { useRef as K, useState as N, useEffect as C, useMemo as H } from "react";
function rt(t, e = 0.08) {
  const o = K(null), [c, a] = N(!1), [r, f] = N(!1), [x, l] = N(0);
  C(() => {
    const i = window.matchMedia("(prefers-reduced-motion: reduce)"), h = () => a(i.matches);
    return h(), i.addEventListener("change", h), () => i.removeEventListener("change", h);
  }, []), C(() => {
    const i = o.current;
    if (!i) return;
    const h = new IntersectionObserver(
      ([p]) => f(p.isIntersecting),
      { rootMargin: "10% 0px" }
    );
    return h.observe(i), () => h.disconnect();
  }, []);
  const d = r && !c;
  return C(() => {
    if (!d) return;
    let i = 0, h = performance.now();
    const p = (u) => {
      const g = Math.min((u - h) / 1e3, 0.1);
      h = u, l((y) => y + g), i = requestAnimationFrame(p);
    };
    return i = requestAnimationFrame(p), () => cancelAnimationFrame(i);
  }, [d]), { t: c ? e : x % t / t, elapsed: x, reduced: c, ref: o, running: d };
}
const w = (t, e, o) => t + (e - t) * o, $ = (t) => t < 0 ? 0 : t > 1 ? 1 : t, V = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
function ct(t, e, o, c = 0.14) {
  const a = t * o, r = Math.min(
    Math.abs(a - e),
    Math.abs(a - e - o),
    Math.abs(a - e + o)
  );
  return r <= 0.5 - c ? 1 : r >= 0.5 + c ? 0 : V(1 - (r - (0.5 - c)) / (2 * c));
}
const st = 16, Q = 4, at = 0.589, A = 1e3, X = 62, G = 46, tt = A - X - G, et = -0.1, U = 0.84, m = 13, z = { b: 0.55, k: 0.9, c1: 0.3, w1: 0.16, a1: 0.62, c2: 0.76, w2: 0.13, a2: 0.34 }, it = { b: 0.565, k: 0.85, c1: 0.318, w1: 0.172, a1: 0.575, c2: 0.748, w2: 0.139, a2: 0.372 }, nt = { b: 0.56, k: 1, c1: 0.42, w1: 0.2, a1: 0.64, c2: 0.88, w2: 0.1, a2: 0 }, Z = (t, e, o) => ({
  b: w(t.b, e.b, o),
  k: w(t.k, e.k, o),
  c1: w(t.c1, e.c1, o),
  w1: w(t.w1, e.w1, o),
  a1: w(t.a1, e.a1, o),
  c2: w(t.c2, e.c2, o),
  w2: w(t.w2, e.w2, o),
  a2: w(t.a2, e.a2, o)
}), b = (t, e) => t.b + t.k * (e - 0.5) * (e - 0.5) - t.a1 * Math.exp(-(((e - t.c1) / t.w1) ** 2)) - t.a2 * Math.exp(-(((e - t.c2) / t.w2) ** 2)), lt = (t, e) => 2 * t.k * (e - 0.5) + t.a1 * 2 * (e - t.c1) / (t.w1 * t.w1) * Math.exp(-(((e - t.c1) / t.w1) ** 2)) + t.a2 * 2 * (e - t.c2) / (t.w2 * t.w2) * Math.exp(-(((e - t.c2) / t.w2) ** 2)), P = 400, dt = 430;
function j(t, e) {
  const r = dt / (U - et), f = [e], x = [0];
  let l = e, d = 0;
  for (let h = 1; h < P; h++) {
    const p = l;
    for (let y = 0; y < 4; y++) l -= 0.055 * lt(t, l) * 0.01;
    l = Math.max(-0.03, Math.min(1.03, l));
    const u = (l - p) * tt, g = (b(t, l) - b(t, p)) * r;
    d += Math.hypot(u, g) * (u < 0 ? -1 : 1), f.push(l), x.push(d);
  }
  const T = f[P - 1];
  let i = P - 1;
  for (let h = P - 1; h >= 0; h--)
    if (Math.abs(f[h] - T) > 12e-4) {
      i = Math.min(P - 1, h + Math.round(P * 0.07));
      break;
    }
  return { xs: f, arc: x, n: i };
}
const ht = (t) => t * (0.35 + 0.65 * t);
function pt(t, e) {
  const o = ht($(e)) * t.n, c = Math.min(t.n, Math.floor(o)), a = Math.min(t.n, c + 1), r = o - c;
  return { x: w(t.xs[c], t.xs[a], r), arc: w(t.arc[c], t.arc[a], r), idx: o };
}
const Y = (t) => (t % 1 + 1) % 1, _ = (t, e) => Math.min(Y(t - (e / Q - 0.16)) / 0.32, 1);
function ft(t) {
  const e = Y(t - 0.84);
  return e > 0.32 ? 0 : 0.5 - 0.5 * Math.cos(2 * Math.PI * e / 0.32);
}
function mt(t) {
  const e = Y(t - 0.59);
  if (e > 0.41) return 0;
  const o = V($((e - 0.01) / 0.06)), c = V($((e - 0.31) / 0.1));
  return o * (1 - c);
}
function xt(t) {
  const e = Z(z, it, ft(t)), o = mt(t);
  return o > 0 ? Z(e, nt, o) : e;
}
const k = (t) => X + t * tt, F = (t) => t * 0.085, O = (t) => t * 0.855, L = (t, e) => F(e) + (U - t) / (U - et) * (O(e) - F(e)), n = (t) => Math.round(t * 10) / 10;
function J(t, e) {
  let o = "";
  for (let c = 0; c <= 220; c++) {
    const a = c / 220;
    o += `${c ? "L" : "M"}${n(k(a))} ${n(L(b(t, a), e))}`;
  }
  return o;
}
function R(t, e, o) {
  const c = Math.max(0, Math.min(1, e)), a = 3e-3, r = k(c), f = L(b(t, c), o), x = k(c + a) - k(c - a), l = L(b(t, Math.min(1, c + a)), o) - L(b(t, Math.max(0, c - a)), o), d = Math.hypot(x, l) || 1;
  return { cx: r, cy: f, nx: l / d, ny: -x / d, tilt: Math.atan2(l, x) * 180 / Math.PI };
}
function B({ run: t, shape: e, h: o, d: c, tone: a }) {
  const r = pt(t, c), f = $((c - 0.7) / 0.3);
  let x = `M${n(k(t.xs[0]))} ${n(L(b(e, t.xs[0]), o))}`;
  const l = Math.max(1, Math.round(t.n / 90));
  for (let p = l; p < r.idx; p += l)
    x += `L${n(k(t.xs[p]))} ${n(L(b(e, t.xs[p]), o))}`;
  x += `L${n(k(r.x))} ${n(L(b(e, r.x), o))}`;
  const d = Math.max(2, Math.round(t.n / 15)), T = [];
  for (let p = d; p <= r.idx; p += d) T.push(t.xs[p]);
  const i = R(e, r.x, o), h = r.arc / m * 180 / Math.PI;
  return /* @__PURE__ */ M("g", { children: [
    /* @__PURE__ */ s("path", { d: x, fill: "none", stroke: a, strokeWidth: 4, strokeLinecap: "round", strokeLinejoin: "round", opacity: 0.5 }),
    T.map((p, u) => {
      const g = R(e, p, o);
      return /* @__PURE__ */ s("circle", { cx: n(g.cx), cy: n(g.cy), r: 2.6, fill: a, opacity: 0.75 }, u);
    }),
    /* @__PURE__ */ s(
      "line",
      {
        x1: n(i.cx),
        y1: n(i.cy),
        x2: n(i.cx),
        y2: n(O(o)),
        stroke: a,
        strokeWidth: 1.4,
        strokeDasharray: "2 5",
        opacity: f * 0.55
      }
    ),
    /* @__PURE__ */ s(
      "ellipse",
      {
        cx: n(i.cx),
        cy: n(i.cy),
        rx: m * 1.05,
        ry: m * 0.32,
        fill: "var(--ink)",
        opacity: 0.13,
        transform: `rotate(${n(i.tilt)} ${n(i.cx)} ${n(i.cy)})`
      }
    ),
    /* @__PURE__ */ M("g", { transform: `translate(${n(i.cx + m * i.nx)} ${n(i.cy + m * i.ny)})`, children: [
      /* @__PURE__ */ s("circle", { r: m, fill: "var(--ink)" }),
      /* @__PURE__ */ s(
        "path",
        {
          d: `M${-m * 0.6} 0A${m * 0.6} ${m * 0.6} 0 0 1 ${m * 0.6} 0`,
          fill: "none",
          stroke: "var(--cream)",
          strokeWidth: 2.4,
          strokeLinecap: "round",
          opacity: 0.5,
          transform: `rotate(${n(h)})`
        }
      ),
      /* @__PURE__ */ s("circle", { cx: -m * 0.33, cy: -m * 0.36, r: m * 0.22, fill: "var(--cream)", opacity: 0.8 })
    ] })
  ] });
}
function ut({ shape: t, x: e, h: o, tone: c }) {
  const a = R(t, e, o);
  return /* @__PURE__ */ M("g", { children: [
    /* @__PURE__ */ s(
      "line",
      {
        x1: n(a.cx),
        y1: n(a.cy),
        x2: n(a.cx),
        y2: n(O(o)),
        stroke: c,
        strokeWidth: 1.4,
        strokeDasharray: "2 5",
        opacity: 0.5
      }
    ),
    /* @__PURE__ */ s(
      "circle",
      {
        cx: n(a.cx + m * a.nx),
        cy: n(a.cy + m * a.ny),
        r: m * 0.72,
        fill: "var(--page)",
        stroke: c,
        strokeWidth: 2.4
      }
    )
  ] });
}
const yt = [
  ["The landscape", "A loss surface. Only the ground underfoot is ever visible."],
  ["Stuck", "Released on the right, it stops in the nearer valley — short of the true minimum."],
  ["Found", "The same rule from a different start reaches the deepest point."],
  ["The ground shifts", "Same start as before. The landscape decides where it lands."]
], D = (t) => ({
  position: "absolute",
  margin: 0,
  whiteSpace: "nowrap",
  fontSize: "clamp(8.5px, 1.25cqw, 11px)",
  background: "var(--page)",
  padding: "1px 5px",
  pointerEvents: "none",
  ...t
});
function Mt() {
  const { t, ref: e } = rt(st, at), o = K(null), [c, a] = N(880);
  C(() => {
    const v = o.current;
    if (!v || typeof ResizeObserver > "u") return;
    const S = new ResizeObserver((W) => {
      const E = W[0]?.contentRect.width ?? 0;
      E > 0 && a((q) => Math.abs(q - E) > 4 ? E : q);
    });
    return S.observe(v), () => S.disconnect();
  }, []);
  const r = H(() => {
    const v = 520 + 260 * $((760 - c) / 340);
    return Math.round(Math.max(380, Math.min(v, 520 / Math.max(c, 1) * 1e3)) / 10) * 10;
  }, [c]), f = H(
    () => ({
      stuck: j(z, 0.945),
      found: j(z, 0.052),
      shift: j(nt, 0.945)
    }),
    []
  ), x = H(() => {
    let v = { x: 0, v: 1 / 0 };
    for (let S = 0; S <= 1e3; S++) {
      const W = S / 1e3, E = b(z, W);
      E < v.v && (v = { x: W, v: E });
    }
    return v;
  }, []), l = xt(t), d = [0, 1, 2, 3].map((v) => ct(t, v, Q)), T = $((_(t, 1) - 0.2) / 0.52), i = $((_(t, 2) - 0.2) / 0.52), h = $((_(t, 3) - 0.26) / 0.46), p = Math.min(1, d[1] + d[2]), u = L(x.v, r), g = f.stuck.xs[f.stuck.n], y = R(l, g, r), I = R(l, 0.945, r), ot = $((_(t, 1) - 0.62) / 0.12) * d[1];
  return /* @__PURE__ */ M(
    "figure",
    {
      ref: e,
      className: "figure",
      role: "img",
      "aria-label": "A loss curve with two valleys, one deeper than the other, separated by a ridge. A marble released on the right rolls downhill and settles in the shallower valley, short of the true minimum; the same marble released on the left settles in the deeper one. When the landscape itself changes shape, a marble from that same right-hand start ends up somewhere else entirely. Gradient descent only ever follows the slope under its feet, so the starting point and the shape of the landscape decide where it stops.",
      style: {
        containerType: "inline-size",
        display: "flex",
        flexDirection: "column",
        padding: "clamp(16px, 3vw, 30px)",
        border: "1px solid var(--edge)",
        borderRadius: 3,
        boxSizing: "border-box"
      },
      children: [
        /* @__PURE__ */ s("header", { style: { position: "relative", minHeight: "clamp(92px, 13cqw, 112px)" }, children: yt.map(([v, S], W) => /* @__PURE__ */ M("div", { style: { position: "absolute", inset: 0, opacity: d[W] }, children: [
          /* @__PURE__ */ s("div", { className: "label", style: { fontSize: "clamp(8.5px, 1.25cqw, 11px)", color: "var(--lavender)" }, children: `0${W + 1} / 04` }),
          /* @__PURE__ */ s(
            "div",
            {
              className: "title",
              style: { fontSize: "clamp(20px, 3.4cqw, 30px)", lineHeight: 1.15, marginTop: 6 },
              children: v
            }
          ),
          /* @__PURE__ */ s(
            "div",
            {
              style: {
                fontSize: "clamp(12.5px, 1.65cqw, 15px)",
                lineHeight: 1.45,
                color: "var(--warm-dk)",
                marginTop: 4,
                maxWidth: "46em"
              },
              children: S
            }
          )
        ] }, v)) }),
        /* @__PURE__ */ M("div", { ref: o, style: { position: "relative", width: "100%", aspectRatio: `${A} / ${r}` }, children: [
          /* @__PURE__ */ M(
            "svg",
            {
              viewBox: `0 0 ${A} ${r}`,
              preserveAspectRatio: "xMidYMid meet",
              style: { display: "block", width: "100%", height: "100%", overflow: "visible" },
              "aria-hidden": "true",
              children: [
                /* @__PURE__ */ s("defs", { children: /* @__PURE__ */ M("linearGradient", { id: "fig-b-ground", x1: "0", y1: "0", x2: "0", y2: "1", children: [
                  /* @__PURE__ */ s("stop", { offset: "0%", stopColor: "var(--cream)", stopOpacity: 0.95 }),
                  /* @__PURE__ */ s("stop", { offset: "100%", stopColor: "var(--cream)", stopOpacity: 0.35 })
                ] }) }),
                /* @__PURE__ */ s("path", { d: `${J(l, r)}L${k(1)} ${n(O(r))}L${k(0)} ${n(O(r))}Z`, fill: "url(#fig-b-ground)" }),
                /* @__PURE__ */ s(
                  "line",
                  {
                    x1: X - 22,
                    y1: n(O(r)),
                    x2: A - G + 16,
                    y2: n(O(r)),
                    stroke: "var(--edge)",
                    strokeWidth: 1.2
                  }
                ),
                /* @__PURE__ */ s(
                  "line",
                  {
                    x1: k(0.01),
                    y1: n(u),
                    x2: k(0.99),
                    y2: n(u),
                    stroke: "var(--muted)",
                    strokeWidth: 1.2,
                    strokeDasharray: "5 6",
                    opacity: p * 0.85
                  }
                ),
                /* @__PURE__ */ s("path", { d: J(l, r), fill: "none", stroke: "var(--ink)", strokeWidth: 2.6, strokeLinecap: "round" }),
                /* @__PURE__ */ s("g", { opacity: d[1], children: /* @__PURE__ */ s(B, { run: f.stuck, shape: l, h: r, d: T, tone: "var(--indigo)" }) }),
                /* @__PURE__ */ M("g", { opacity: ot, children: [
                  /* @__PURE__ */ s(
                    "line",
                    {
                      x1: n(y.cx),
                      y1: n(y.cy),
                      x2: n(y.cx),
                      y2: n(u),
                      stroke: "var(--accent)",
                      strokeWidth: 1.8
                    }
                  ),
                  /* @__PURE__ */ s("line", { x1: n(y.cx - 7), y1: n(u), x2: n(y.cx + 7), y2: n(u), stroke: "var(--accent)", strokeWidth: 1.8 }),
                  /* @__PURE__ */ s(
                    "line",
                    {
                      x1: n(y.cx - 7),
                      y1: n(y.cy),
                      x2: n(y.cx + 7),
                      y2: n(y.cy),
                      stroke: "var(--accent)",
                      strokeWidth: 1.8
                    }
                  )
                ] }),
                /* @__PURE__ */ M("g", { opacity: d[2], children: [
                  /* @__PURE__ */ s("g", { opacity: 0.45, children: /* @__PURE__ */ s(ut, { shape: l, x: g, h: r, tone: "var(--muted)" }) }),
                  /* @__PURE__ */ s(B, { run: f.found, shape: l, h: r, d: i, tone: "var(--indigo)" })
                ] }),
                /* @__PURE__ */ M("g", { opacity: d[3], children: [
                  /* @__PURE__ */ s(
                    "line",
                    {
                      x1: n(I.cx),
                      y1: n(F(r) * 1.25),
                      x2: n(I.cx),
                      y2: n(I.cy),
                      stroke: "var(--lavender)",
                      strokeWidth: 1.4,
                      strokeDasharray: "2 5",
                      opacity: 0.75
                    }
                  ),
                  /* @__PURE__ */ s(B, { run: f.shift, shape: l, h: r, d: h, tone: "var(--lavender)" })
                ] })
              ]
            }
          ),
          /* @__PURE__ */ s("span", { className: "label", style: D({ left: "1.6%", top: "44%", transform: "translate(-50%, -50%) rotate(-90deg)" }), children: "Loss" }),
          /* @__PURE__ */ s(
            "span",
            {
              className: "label",
              style: D({ left: `${(A - G) / A * 100}%`, top: "94%", transform: "translate(-100%, -50%)" }),
              children: "Parameter"
            }
          ),
          /* @__PURE__ */ s(
            "span",
            {
              className: "label",
              style: D({
                left: `${k(0.02) / A * 100}%`,
                top: `${u / r * 100}%`,
                transform: "translate(0, -128%)",
                opacity: p
              }),
              children: "True minimum"
            }
          ),
          /* @__PURE__ */ s(
            "span",
            {
              className: "label",
              style: D({
                left: `${I.cx / A * 100}%`,
                top: `${F(r) * 1.25 / r * 100}%`,
                transform: "translate(-100%, -118%)",
                color: "var(--lavender)",
                opacity: d[3]
              }),
              children: "Same start"
            }
          )
        ] })
      ]
    }
  );
}
export {
  Mt as Figure
};
