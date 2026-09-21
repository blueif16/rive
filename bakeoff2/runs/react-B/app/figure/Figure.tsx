import { useEffect, useMemo, useRef, useState } from 'react';
import { useFigureClock, beatOpacity, easeInOut, lerp, sat } from './useFigureClock';
import './figure.css';

/**
 * Figure B — Gradient descent finds a minimum.
 *
 * The whole figure is a single 1-D loss landscape. A marble is released onto it
 * and integrates plain gradient descent, dx/dτ = -η f'(x): fast where the
 * ground is steep, slow where it flattens, settling exponentially rather than
 * stopping. Its vertical position is never keyframed — it is always
 * loss(currentShape, x), offset along the surface normal — so it stays glued to
 * the curve even while the curve is morphing underneath it.
 *
 * Every animated value is a pure function of the clock's `t`. The trajectories
 * are integrated once at mount and then *sampled* by t, so nothing restarts
 * when a beat fades back in and the loop is seamless.
 */

const LOOP_SECONDS = 16;
const BEATS = 4;
/** Reduced-motion still: beat 3 settled, trace and both markers visible. */
const STATIC_AT = 0.589;

const VIEW_W = 1000;
const PAD_L = 62;
const PAD_R = 46;
const PLOT_W = VIEW_W - PAD_L - PAD_R;

/** Fixed loss -> y mapping, shared by every shape so a morph never rescales. */
const LOSS_MIN = -0.1;
const LOSS_MAX = 0.84;

const R = 13; // marble radius, view units

// ---------------------------------------------------------------- landscape

interface Shape {
  b: number;
  k: number;
  c1: number;
  w1: number;
  a1: number;
  c2: number;
  w2: number;
  a2: number;
}

/** Canonical landscape: deep valley left, shallow valley right, ridge between. */
const SHAPE_A: Shape = { b: 0.55, k: 0.9, c1: 0.3, w1: 0.16, a1: 0.62, c2: 0.76, w2: 0.13, a2: 0.34 };
/** The same landscape, breathing — slightly different depths, widths, centres. */
const SHAPE_B: Shape = { b: 0.565, k: 0.85, c1: 0.318, w1: 0.172, a1: 0.575, c2: 0.748, w2: 0.139, a2: 0.372 };
/** After the ground shifts: the right-hand valley is gone, the basin moved. */
const SHAPE_C: Shape = { b: 0.56, k: 1.0, c1: 0.42, w1: 0.2, a1: 0.64, c2: 0.88, w2: 0.1, a2: 0 };

const mixShape = (p: Shape, q: Shape, u: number): Shape => ({
  b: lerp(p.b, q.b, u),
  k: lerp(p.k, q.k, u),
  c1: lerp(p.c1, q.c1, u),
  w1: lerp(p.w1, q.w1, u),
  a1: lerp(p.a1, q.a1, u),
  c2: lerp(p.c2, q.c2, u),
  w2: lerp(p.w2, q.w2, u),
  a2: lerp(p.a2, q.a2, u),
});

const loss = (s: Shape, x: number) =>
  s.b +
  s.k * (x - 0.5) * (x - 0.5) -
  s.a1 * Math.exp(-(((x - s.c1) / s.w1) ** 2)) -
  s.a2 * Math.exp(-(((x - s.c2) / s.w2) ** 2));

/** df/dx — the only thing the marble is ever allowed to know. */
const slope = (s: Shape, x: number) =>
  2 * s.k * (x - 0.5) +
  ((s.a1 * 2 * (x - s.c1)) / (s.w1 * s.w1)) * Math.exp(-(((x - s.c1) / s.w1) ** 2)) +
  ((s.a2 * 2 * (x - s.c2)) / (s.w2 * s.w2)) * Math.exp(-(((x - s.c2) / s.w2) ** 2));

// ----------------------------------------------------------------- descent

interface Run {
  xs: number[];
  /** Signed arc length in reference view units — drives the rolling spin. */
  arc: number[];
  /** Index at which the marble has effectively settled. */
  n: number;
}

const SAMPLES = 400;
const REF_H = 430;

/** Integrate gradient descent once; the render only ever samples this. */
function buildRun(s: Shape, x0: number): Run {
  const SUB = 4;
  const DT = 0.01;
  const ETA = 0.055;
  const yScale = REF_H / (LOSS_MAX - LOSS_MIN);
  const xs = [x0];
  const arc = [0];
  let x = x0;
  let len = 0;
  for (let i = 1; i < SAMPLES; i++) {
    const prev = x;
    for (let j = 0; j < SUB; j++) x -= ETA * slope(s, x) * DT;
    x = Math.max(-0.03, Math.min(1.03, x));
    const dx = (x - prev) * PLOT_W;
    const dy = (loss(s, x) - loss(s, prev)) * yScale;
    len += Math.hypot(dx, dy) * (dx < 0 ? -1 : 1);
    xs.push(x);
    arc.push(len);
  }
  const end = xs[SAMPLES - 1];
  let n = SAMPLES - 1;
  for (let i = SAMPLES - 1; i >= 0; i--) {
    if (Math.abs(xs[i] - end) > 0.0012) {
      n = Math.min(SAMPLES - 1, i + Math.round(SAMPLES * 0.07));
      break;
    }
  }
  return { xs, arc, n };
}

/** Mild ease-in on simulated time so release is a roll, not a jerk. */
const releaseEase = (d: number) => d * (0.35 + 0.65 * d);

function sampleRun(run: Run, d: number) {
  const f = releaseEase(sat(d)) * run.n;
  const i = Math.min(run.n, Math.floor(f));
  const j = Math.min(run.n, i + 1);
  const g = f - i;
  return { x: lerp(run.xs[i], run.xs[j], g), arc: lerp(run.arc[i], run.arc[j], g), idx: f };
}

// -------------------------------------------------------------- loop phase

const mod1 = (v: number) => ((v % 1) + 1) % 1;

/** 0 -> 1 across beat `i`'s full crossfade window; frozen at the edges. */
const beatPhase = (t: number, i: number) => Math.min(mod1(t - (i / BEATS - 0.16)) / 0.32, 1);

/** One slow breath across beat 1's window, exactly zero everywhere else. */
function breatheAt(t: number) {
  const r = mod1(t - 0.84);
  if (r > 0.32) return 0;
  return 0.5 - 0.5 * Math.cos((2 * Math.PI * r) / 0.32);
}

/** Rises through beat 4's opening, holds, relaxes back before the loop seam. */
function morphAt(t: number) {
  const r = mod1(t - 0.59);
  if (r > 0.41) return 0;
  const up = easeInOut(sat((r - 0.01) / 0.06));
  const down = easeInOut(sat((r - 0.31) / 0.1));
  return up * (1 - down);
}

function shapeAt(t: number): Shape {
  const base = mixShape(SHAPE_A, SHAPE_B, breatheAt(t));
  const m = morphAt(t);
  return m > 0 ? mixShape(base, SHAPE_C, m) : base;
}

// ------------------------------------------------------------- projection

const px = (x: number) => PAD_L + x * PLOT_W;
const topOf = (h: number) => h * 0.085;
const baseOf = (h: number) => h * 0.855;
const py = (v: number, h: number) =>
  topOf(h) + ((LOSS_MAX - v) / (LOSS_MAX - LOSS_MIN)) * (baseOf(h) - topOf(h));

const r1 = (v: number) => Math.round(v * 10) / 10;

function curvePath(s: Shape, h: number) {
  let d = '';
  for (let i = 0; i <= 220; i++) {
    const x = i / 220;
    d += `${i ? 'L' : 'M'}${r1(px(x))} ${r1(py(loss(s, x), h))}`;
  }
  return d;
}

/** Contact point plus the outward surface normal, so the marble sits ON it. */
function contact(s: Shape, x: number, h: number) {
  const xc = Math.max(0, Math.min(1, x));
  const e = 0.003;
  const cx = px(xc);
  const cy = py(loss(s, xc), h);
  const dx = px(xc + e) - px(xc - e);
  const dy = py(loss(s, Math.min(1, xc + e)), h) - py(loss(s, Math.max(0, xc - e)), h);
  const m = Math.hypot(dx, dy) || 1;
  return { cx, cy, nx: dy / m, ny: -dx / m, tilt: (Math.atan2(dy, dx) * 180) / Math.PI };
}

// ------------------------------------------------------------------ pieces

function Descent({ run, shape, h, d, tone }: { run: Run; shape: Shape; h: number; d: number; tone: string }) {
  const at = sampleRun(run, d);
  const settled = sat((d - 0.7) / 0.3);

  let path = `M${r1(px(run.xs[0]))} ${r1(py(loss(shape, run.xs[0]), h))}`;
  const step = Math.max(1, Math.round(run.n / 90));
  for (let i = step; i < at.idx; i += step) {
    path += `L${r1(px(run.xs[i]))} ${r1(py(loss(shape, run.xs[i]), h))}`;
  }
  path += `L${r1(px(at.x))} ${r1(py(loss(shape, at.x), h))}`;

  // Stroboscopic beads, one per equal slice of simulated time: far apart where
  // the ground is steep, crowded where it flattens out.
  const stride = Math.max(2, Math.round(run.n / 15));
  const beads: number[] = [];
  for (let i = stride; i <= at.idx; i += stride) beads.push(run.xs[i]);

  const c = contact(shape, at.x, h);
  const roll = ((at.arc / R) * 180) / Math.PI;

  return (
    <g>
      <path d={path} fill="none" stroke={tone} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" opacity={0.5} />
      {beads.map((bx, i) => {
        const b = contact(shape, bx, h);
        return <circle key={i} cx={r1(b.cx)} cy={r1(b.cy)} r={2.6} fill={tone} opacity={0.75} />;
      })}
      <line
        x1={r1(c.cx)}
        y1={r1(c.cy)}
        x2={r1(c.cx)}
        y2={r1(baseOf(h))}
        stroke={tone}
        strokeWidth={1.4}
        strokeDasharray="2 5"
        opacity={settled * 0.55}
      />
      <ellipse
        cx={r1(c.cx)}
        cy={r1(c.cy)}
        rx={R * 1.05}
        ry={R * 0.32}
        fill="var(--ink)"
        opacity={0.13}
        transform={`rotate(${r1(c.tilt)} ${r1(c.cx)} ${r1(c.cy)})`}
      />
      <g transform={`translate(${r1(c.cx + R * c.nx)} ${r1(c.cy + R * c.ny)})`}>
        <circle r={R} fill="var(--ink)" />
        <path
          d={`M${-R * 0.6} 0A${R * 0.6} ${R * 0.6} 0 0 1 ${R * 0.6} 0`}
          fill="none"
          stroke="var(--cream)"
          strokeWidth={2.4}
          strokeLinecap="round"
          opacity={0.5}
          transform={`rotate(${r1(roll)})`}
        />
        <circle cx={-R * 0.33} cy={-R * 0.36} r={R * 0.22} fill="var(--cream)" opacity={0.8} />
      </g>
    </g>
  );
}

function Marker({ shape, x, h, tone }: { shape: Shape; x: number; h: number; tone: string }) {
  const c = contact(shape, x, h);
  return (
    <g>
      <line
        x1={r1(c.cx)}
        y1={r1(c.cy)}
        x2={r1(c.cx)}
        y2={r1(baseOf(h))}
        stroke={tone}
        strokeWidth={1.4}
        strokeDasharray="2 5"
        opacity={0.5}
      />
      <circle
        cx={r1(c.cx + R * c.nx)}
        cy={r1(c.cy + R * c.ny)}
        r={R * 0.72}
        fill="var(--page)"
        stroke={tone}
        strokeWidth={2.4}
      />
    </g>
  );
}

// -------------------------------------------------------------------- text

const CAPTIONS: Array<[string, string]> = [
  ['The landscape', 'A loss surface. Only the ground underfoot is ever visible.'],
  ['Stuck', 'Released on the right, it stops in the nearer valley — short of the true minimum.'],
  ['Found', 'The same rule from a different start reaches the deepest point.'],
  ['The ground shifts', 'Same start as before. The landscape decides where it lands.'],
];

const plotLabel = (extra: React.CSSProperties): React.CSSProperties => ({
  position: 'absolute',
  margin: 0,
  whiteSpace: 'nowrap',
  fontSize: 'clamp(8.5px, 1.25cqw, 11px)',
  background: 'var(--page)',
  padding: '1px 5px',
  pointerEvents: 'none',
  ...extra,
});

// ------------------------------------------------------------------ figure

export default function Figure() {
  const { t, ref } = useFigureClock(LOOP_SECONDS, STATIC_AT);
  const plotRef = useRef<HTMLDivElement>(null);
  const [w, setW] = useState(880);

  useEffect(() => {
    const el = plotRef.current;
    if (!el || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver((entries) => {
      const cw = entries[0]?.contentRect.width ?? 0;
      if (cw > 0) setW((prev) => (Math.abs(prev - cw) > 4 ? cw : prev));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // The viewBox height tracks the box, so the SVG always fills it exactly and
  // percent-positioned DOM labels land on view coordinates with no letterbox.
  const h = useMemo(() => {
    const tall = 520 + 260 * sat((760 - w) / 340);
    return Math.round(Math.max(380, Math.min(tall, (520 / Math.max(w, 1)) * 1000)) / 10) * 10;
  }, [w]);

  const runs = useMemo(
    () => ({
      stuck: buildRun(SHAPE_A, 0.945),
      found: buildRun(SHAPE_A, 0.052),
      shift: buildRun(SHAPE_C, 0.945),
    }),
    [],
  );

  const trueMin = useMemo(() => {
    let best = { x: 0, v: Infinity };
    for (let i = 0; i <= 1000; i++) {
      const x = i / 1000;
      const v = loss(SHAPE_A, x);
      if (v < best.v) best = { x, v };
    }
    return best;
  }, []);

  const shape = shapeAt(t);
  const o = [0, 1, 2, 3].map((i) => beatOpacity(t, i, BEATS));
  const dStuck = sat((beatPhase(t, 1) - 0.2) / 0.52);
  const dFound = sat((beatPhase(t, 2) - 0.2) / 0.52);
  const dShift = sat((beatPhase(t, 3) - 0.26) / 0.46);

  const refLine = Math.min(1, o[1] + o[2]);
  const minY = py(trueMin.v, h);
  const stuckX = runs.stuck.xs[runs.stuck.n];
  const stuckC = contact(shape, stuckX, h);
  const startC = contact(shape, 0.945, h);
  const gapShow = sat((beatPhase(t, 1) - 0.62) / 0.12) * o[1];

  return (
    <figure
      ref={ref}
      className="figure"
      role="img"
      aria-label="A loss curve with two valleys, one deeper than the other, separated by a ridge. A marble released on the right rolls downhill and settles in the shallower valley, short of the true minimum; the same marble released on the left settles in the deeper one. When the landscape itself changes shape, a marble from that same right-hand start ends up somewhere else entirely. Gradient descent only ever follows the slope under its feet, so the starting point and the shape of the landscape decide where it stops."
      style={{
        containerType: 'inline-size',
        display: 'flex',
        flexDirection: 'column',
        padding: 'clamp(16px, 3vw, 30px)',
        border: '1px solid var(--edge)',
        borderRadius: 3,
        boxSizing: 'border-box',
      }}
    >
      <header style={{ position: 'relative', minHeight: 'clamp(92px, 13cqw, 112px)' }}>
        {CAPTIONS.map(([title, body], i) => (
          <div key={title} style={{ position: 'absolute', inset: 0, opacity: o[i] }}>
            <div className="label" style={{ fontSize: 'clamp(8.5px, 1.25cqw, 11px)', color: 'var(--lavender)' }}>
              {`0${i + 1} / 04`}
            </div>
            <div
              className="title"
              style={{ fontSize: 'clamp(20px, 3.4cqw, 30px)', lineHeight: 1.15, marginTop: 6 }}
            >
              {title}
            </div>
            <div
              style={{
                fontSize: 'clamp(12.5px, 1.65cqw, 15px)',
                lineHeight: 1.45,
                color: 'var(--warm-dk)',
                marginTop: 4,
                maxWidth: '46em',
              }}
            >
              {body}
            </div>
          </div>
        ))}
      </header>

      <div ref={plotRef} style={{ position: 'relative', width: '100%', aspectRatio: `${VIEW_W} / ${h}` }}>
        <svg
          viewBox={`0 0 ${VIEW_W} ${h}`}
          preserveAspectRatio="xMidYMid meet"
          style={{ display: 'block', width: '100%', height: '100%', overflow: 'visible' }}
          aria-hidden="true"
        >
          <defs>
            <linearGradient id="fig-b-ground" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--cream)" stopOpacity={0.95} />
              <stop offset="100%" stopColor="var(--cream)" stopOpacity={0.35} />
            </linearGradient>
          </defs>

          {/* the surface itself — never fades, it is the one continuous thing */}
          <path d={`${curvePath(shape, h)}L${px(1)} ${r1(baseOf(h))}L${px(0)} ${r1(baseOf(h))}Z`} fill="url(#fig-b-ground)" />
          <line
            x1={PAD_L - 22}
            y1={r1(baseOf(h))}
            x2={VIEW_W - PAD_R + 16}
            y2={r1(baseOf(h))}
            stroke="var(--edge)"
            strokeWidth={1.2}
          />

          {/* the depth every run is measured against */}
          <line
            x1={px(0.01)}
            y1={r1(minY)}
            x2={px(0.99)}
            y2={r1(minY)}
            stroke="var(--muted)"
            strokeWidth={1.2}
            strokeDasharray="5 6"
            opacity={refLine * 0.85}
          />

          <path d={curvePath(shape, h)} fill="none" stroke="var(--ink)" strokeWidth={2.6} strokeLinecap="round" />

          {/* beat 2 — stuck in the shallow valley */}
          <g opacity={o[1]}>
            <Descent run={runs.stuck} shape={shape} h={h} d={dStuck} tone="var(--indigo)" />
          </g>
          <g opacity={gapShow}>
            <line
              x1={r1(stuckC.cx)}
              y1={r1(stuckC.cy)}
              x2={r1(stuckC.cx)}
              y2={r1(minY)}
              stroke="var(--accent)"
              strokeWidth={1.8}
            />
            <line x1={r1(stuckC.cx - 7)} y1={r1(minY)} x2={r1(stuckC.cx + 7)} y2={r1(minY)} stroke="var(--accent)" strokeWidth={1.8} />
            <line
              x1={r1(stuckC.cx - 7)}
              y1={r1(stuckC.cy)}
              x2={r1(stuckC.cx + 7)}
              y2={r1(stuckC.cy)}
              stroke="var(--accent)"
              strokeWidth={1.8}
            />
          </g>

          {/* beat 3 — same rule, a different start, the deep valley */}
          <g opacity={o[2]}>
            <g opacity={0.45}>
              <Marker shape={shape} x={stuckX} h={h} tone="var(--muted)" />
            </g>
            <Descent run={runs.found} shape={shape} h={h} d={dFound} tone="var(--indigo)" />
          </g>

          {/* beat 4 — the ground shifts under the same starting point */}
          <g opacity={o[3]}>
            <line
              x1={r1(startC.cx)}
              y1={r1(topOf(h) * 1.25)}
              x2={r1(startC.cx)}
              y2={r1(startC.cy)}
              stroke="var(--lavender)"
              strokeWidth={1.4}
              strokeDasharray="2 5"
              opacity={0.75}
            />
            <Descent run={runs.shift} shape={shape} h={h} d={dShift} tone="var(--lavender)" />
          </g>
        </svg>

        <span className="label" style={plotLabel({ left: '1.6%', top: '44%', transform: 'translate(-50%, -50%) rotate(-90deg)' })}>
          Loss
        </span>
        <span
          className="label"
          style={plotLabel({ left: `${((VIEW_W - PAD_R) / VIEW_W) * 100}%`, top: '94%', transform: 'translate(-100%, -50%)' })}
        >
          Parameter
        </span>
        <span
          className="label"
          style={plotLabel({
            left: `${(px(0.02) / VIEW_W) * 100}%`,
            top: `${(minY / h) * 100}%`,
            transform: 'translate(0, -128%)',
            opacity: refLine,
          })}
        >
          True minimum
        </span>
        <span
          className="label"
          style={plotLabel({
            left: `${(startC.cx / VIEW_W) * 100}%`,
            top: `${((topOf(h) * 1.25) / h) * 100}%`,
            transform: 'translate(-100%, -118%)',
            color: 'var(--lavender)',
            opacity: o[3],
          })}
        >
          Same start
        </span>
      </div>
    </figure>
  );
}
