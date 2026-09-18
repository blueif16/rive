import { jsxs as h, jsx as u } from "react/jsx-runtime";
import { useRef as E, useState as d, useEffect as m } from "react";
function F(e, i = 0.08) {
  const s = E(null), [r, c] = d(!1), [a, y] = d(!1), [f, w] = d(0);
  m(() => {
    const t = window.matchMedia("(prefers-reduced-motion: reduce)"), n = () => c(t.matches);
    return n(), t.addEventListener("change", n), () => t.removeEventListener("change", n);
  }, []), m(() => {
    const t = s.current;
    if (!t) return;
    const n = new IntersectionObserver(
      ([o]) => y(o.isIntersecting),
      { rootMargin: "10% 0px" }
    );
    return n.observe(t), () => n.disconnect();
  }, []);
  const l = a && !r;
  return m(() => {
    if (!l) return;
    let t = 0, n = performance.now();
    const o = (p) => {
      const v = Math.min((p - n) / 1e3, 0.1);
      n = p, w((M) => M + v), t = requestAnimationFrame(o);
    };
    return t = requestAnimationFrame(o), () => cancelAnimationFrame(t);
  }, [l]), { t: r ? i : f % e / e, elapsed: f, reduced: r, ref: s, running: l };
}
const I = (e) => e < 0.5 ? 2 * e * e : 1 - Math.pow(-2 * e + 2, 2) / 2;
function g(e, i, s, r = 0.14) {
  const c = e * s, a = Math.min(
    Math.abs(c - i),
    Math.abs(c - i - s),
    Math.abs(c - i + s)
  );
  return a <= 0.5 - r ? 1 : a >= 0.5 + r ? 0 : I(1 - (a - (0.5 - r)) / (2 * r));
}
const O = 12, b = 4;
function R() {
  const { t: e, reduced: i, ref: s } = F(O);
  return /* @__PURE__ */ h(
    "figure",
    {
      ref: s,
      className: "figure",
      role: "img",
      "aria-label": "Replace with a sentence describing what this figure conveys.",
      style: { aspectRatio: "2 / 1", minHeight: 260 },
      children: [
        /* @__PURE__ */ u(
          "div",
          {
            style: {
              position: "absolute",
              inset: 0,
              display: "grid",
              placeItems: "center",
              opacity: g(e, 0, b)
            },
            children: /* @__PURE__ */ u("span", { className: "title", style: { fontSize: 42 }, children: "Figure scaffold" })
          }
        ),
        /* @__PURE__ */ u(
          "div",
          {
            style: {
              position: "absolute",
              inset: 0,
              display: "grid",
              placeItems: "center",
              opacity: g(e, 1, b)
            },
            children: /* @__PURE__ */ h("span", { className: "label", children: [
              "beat two",
              i ? " · reduced motion" : ""
            ] })
          }
        )
      ]
    }
  );
}
export {
  R as Figure
};
