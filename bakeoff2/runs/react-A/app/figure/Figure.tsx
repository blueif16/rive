import { useFigureClock, beatOpacity, easeInOut, sat, lerp } from './useFigureClock';
import './figure.css';

/**
 * Figure A — what a context window holds.
 *
 * A single budget bar of fixed width. Turns arrive at its leading edge and take
 * space in proportion to their size. When the budget is full the oldest turns
 * dim and collapse into one small `summary`, and the reclaimed space is taken
 * at once by new arrivals. Below the bar, a history rail shows every turn ever
 * said, at the same scale — so the rail grows past the figure's edge while the
 * bar above it never does. That contrast is the whole point.
 *
 * Every animated value is a pure function of the clock's `t`. Nothing here uses
 * a CSS animation or transition.
 */

const LOOP_SECONDS = 12;
const BEATS = 4;
/** Representative still for prefers-reduced-motion: deep in beat 4. */
const STATIC_AT = 11.15 / LOOP_SECONDS;
/** Crossfade, in seconds, that carries the last beat back into the first. */
const XFADE = 0.7;

const CAPACITY = 32000;

/** Arrival ramp, seconds. A block grows in from the leading edge as it lands. */
const ENTER = 0.55;
/** Compaction: blocks dim over DIM_DUR, geometry collapses GEO_DELAY later. */
const DIM_DUR = 1.0;
const GEO_DELAY = 0.22;
const GEO_DUR = 0.9;

/** The two moments the window runs out of room. */
const COMPACT_1 = 7.2;
const COMPACT_2 = 9.9;

type Kind = 'system' | 'user' | 'assistant' | 'tool result' | 'summary';

const COLOR: Record<Kind, string> = {
  system: 'var(--warm-dk)',
  user: 'var(--indigo)',
  assistant: 'var(--lavender)',
  'tool result': 'var(--warm-lt)',
  summary: 'var(--accent)',
};

interface Item {
  id: string;
  kind: Kind;
  tokens: number;
  /** Sim time at which this item starts taking space. */
  enter: number;
  inDur: number;
  /** Sim time at which it is folded into a summary, if it ever is. */
  remove?: number;
  /** Position in the conversation. Summaries have none — they are not turns. */
  chrono?: number;
}

/**
 * Display order, oldest on the left. Summaries are listed at the slot they
 * occupy once they exist (directly after the pinned system prompt), which is
 * ahead of the turns they replace — so a summary grows rightward exactly as
 * that group shrinks away.
 */
const ITEMS: Item[] = [
  { id: 'sys', kind: 'system', tokens: 2400, enter: -3.2, inDur: ENTER, chrono: 0 },

  { id: 'sum2', kind: 'summary', tokens: 3000, enter: COMPACT_2 + GEO_DELAY, inDur: GEO_DUR },
  { id: 'sum1', kind: 'summary', tokens: 2200, enter: COMPACT_1 + GEO_DELAY, inDur: GEO_DUR, remove: COMPACT_2 },

  { id: 't1', kind: 'user', tokens: 1100, enter: -2.2, inDur: ENTER, remove: COMPACT_1, chrono: 1 },
  { id: 't2', kind: 'assistant', tokens: 2800, enter: -1.2, inDur: ENTER, remove: COMPACT_1, chrono: 2 },
  { id: 't3', kind: 'user', tokens: 900, enter: 1.4, inDur: ENTER, remove: COMPACT_1, chrono: 3 },
  { id: 't4', kind: 'assistant', tokens: 3400, enter: 2.4, inDur: ENTER, remove: COMPACT_1, chrono: 4 },
  { id: 't5', kind: 'tool result', tokens: 6800, enter: 3.3, inDur: ENTER, remove: COMPACT_1, chrono: 5 },

  { id: 't6', kind: 'user', tokens: 1200, enter: 4.1, inDur: ENTER, remove: COMPACT_2, chrono: 6 },
  { id: 't7', kind: 'assistant', tokens: 3900, enter: 4.8, inDur: ENTER, remove: COMPACT_2, chrono: 7 },
  { id: 't8', kind: 'tool result', tokens: 5900, enter: 5.6, inDur: ENTER, remove: COMPACT_2, chrono: 8 },

  { id: 't9', kind: 'user', tokens: 1000, enter: 6.3, inDur: ENTER, chrono: 9 },
  { id: 't10', kind: 'assistant', tokens: 2300, enter: 6.9, inDur: ENTER, chrono: 10 },
  { id: 't11', kind: 'tool result', tokens: 7100, enter: 7.9, inDur: ENTER, chrono: 11 },
  { id: 't12', kind: 'user', tokens: 1300, enter: 8.6, inDur: ENTER, chrono: 12 },
  { id: 't13', kind: 'assistant', tokens: 3600, enter: 9.2, inDur: ENTER, chrono: 13 },
  { id: 't14', kind: 'tool result', tokens: 6800, enter: 10.5, inDur: ENTER, chrono: 14 },
  { id: 't15', kind: 'user', tokens: 1100, enter: 11.0, inDur: ENTER, chrono: 15 },
  { id: 't16', kind: 'assistant', tokens: 2900, enter: 11.5, inDur: ENTER, chrono: 16 },
];

/** The same turns in the order they were said — the history rail's content. */
const CHRONO: Item[] = ITEMS.filter((it) => it.chrono !== undefined).sort(
  (a, b) => (a.chrono as number) - (b.chrono as number),
);

/** A block wide enough to carry its own label without the fade eating it. */
const LABELLED = 0.058;

const BEAT_TEXT: Array<{ title: string; sub: string }> = [
  {
    title: 'A fixed budget',
    sub: 'A context window is not a memory — it is a width. Three turns in, most of it is free, and that width is all there will ever be.',
  },
  {
    title: 'The history grows',
    sub: 'Every turn takes room in proportion to its size, and a single tool result can take more than the whole conversation before it. The bar does not grow with it.',
  },
  {
    title: 'Something has to give',
    sub: 'Full. The oldest turns dim and collapse into one small summary, and the space they give back is taken by new arrivals almost immediately.',
  },
  {
    title: 'Steady state',
    sub: 'A long conversation, compacted to a sliver. Only the most recent turns are still held in full — the rest the model knows only as a summary.',
  },
];

interface Piece {
  id: string;
  kind: Kind;
  /** Left edge as a fraction of the bar's width. */
  x: number;
  /** Width as a fraction of the bar's width, already scaled by occupancy. */
  w: number;
  opacity: number;
  tokens: number;
}

interface Sim {
  blocks: Piece[];
  rail: Piece[];
  used: number;
  usedFrac: number;
  turns: number;
  everTokens: number;
  pressure: number;
  compacted: number;
}

/** The whole figure's state at sim time `u` seconds. Pure; `u` may be negative. */
function simulate(u: number): Sim {
  const blocks: Piece[] = [];
  let x = 0;
  let used = 0;
  let compacted = 0;

  for (const it of ITEMS) {
    const pin = easeInOut(sat((u - it.enter) / it.inDur));
    const geo = it.remove === undefined ? 0 : easeInOut(sat((u - it.remove - GEO_DELAY) / GEO_DUR));
    const dim = it.remove === undefined ? 0 : easeInOut(sat((u - it.remove) / DIM_DUR));
    const occ = pin * (1 - geo);
    const opacity = pin * (1 - dim);
    const w = (it.tokens / CAPACITY) * occ;

    used += it.tokens * occ;
    if (it.kind === 'summary' && opacity > compacted) compacted = opacity;
    if (w > 0.0002) blocks.push({ id: it.id, kind: it.kind, x, w, opacity, tokens: it.tokens });
    x += w;
  }

  const usedFrac = used / CAPACITY;

  // The rail carries every turn at the bar's own scale, right-aligned to the
  // leading edge — so its recent tail registers exactly with the bar above and
  // the rest runs off the left of the frame.
  const spans: Array<Piece & { before: number }> = [];
  let ever = 0;
  let turns = 0;
  for (const it of CHRONO) {
    const pin = easeInOut(sat((u - it.enter) / it.inDur));
    const dim = it.remove === undefined ? 0 : easeInOut(sat((u - it.remove) / DIM_DUR));
    const w = (it.tokens / CAPACITY) * pin;
    if (pin > 0.5) turns += 1;
    spans.push({
      id: it.id,
      kind: it.kind,
      x: 0,
      before: ever,
      w,
      opacity: lerp(0.92, 0.24, dim),
      tokens: it.tokens,
    });
    ever += w;
  }
  const rail = spans
    .filter((s) => s.w > 0.0002)
    .map((s) => ({ id: s.id, kind: s.kind, x: usedFrac - ever + s.before, w: s.w, opacity: s.opacity, tokens: s.tokens }));

  return {
    blocks,
    rail,
    used,
    usedFrac,
    turns,
    everTokens: ever * CAPACITY,
    pressure: sat((usedFrac - 0.9) / 0.07),
    compacted,
  };
}

const num = (n: number) => Math.round(n / 100) * 100;
const fmt = (n: number) => num(n).toLocaleString('en-US');

/** Positions a child at a fraction of the track using transform alone. */
function frac(x: number): string {
  return `translate3d(${(x * 100).toFixed(3)}%, 0, 0)`;
}

function width(w: number, gap: number): string {
  return `max(0px, calc(${(w * 100).toFixed(3)}% - ${gap}px))`;
}

function Block({ p }: { p: Piece }) {
  const color = COLOR[p.kind];
  return (
    <div className="cw-pos" style={{ transform: frac(p.x), opacity: p.opacity }}>
      <div
        className={p.kind === 'summary' ? 'cw-blk cw-blk--sum' : 'cw-blk'}
        style={{ width: width(p.w, 2) }}
      >
        <div className="cw-tint" style={{ background: color }} />
        <div className="cw-cap" style={{ background: color }} />
        {p.tokens / CAPACITY >= LABELLED && (
          <div className="cw-txt fade-right">
            <span className="cw-kind">{p.kind}</span>
            <span className="cw-tok">{p.tokens.toLocaleString('en-US')}</span>
          </div>
        )}
      </div>
    </div>
  );
}

function Segment({ p }: { p: Piece }) {
  return (
    <div className="cw-pos" style={{ transform: frac(p.x), opacity: p.opacity }}>
      <div className="cw-seg" style={{ width: width(p.w, 1.5), background: COLOR[p.kind] }} />
    </div>
  );
}

export default function Figure() {
  const { t, ref } = useFigureClock(LOOP_SECONDS, STATIC_AT);

  const u = t * LOOP_SECONDS;
  // The loop's seam is a crossfade in place: the outgoing cycle's bar dissolves
  // into the incoming one's, both drawn in the same position at the same scale.
  const xf = easeInOut(sat((u - (LOOP_SECONDS - XFADE)) / XFADE));
  const a = simulate(u);
  const b = xf > 0.001 ? simulate(u - LOOP_SECONDS) : null;

  const layers: Array<{ k: string; s: Sim; o: number }> = [{ k: 'a', s: a, o: 1 - xf }];
  if (b) layers.push({ k: 'b', s: b, o: xf });

  const blend = (pick: (s: Sim) => number) => pick(a) * (1 - xf) + (b ? pick(b) * xf : 0);
  const pressure = blend((s) => s.pressure);
  const compacted = blend((s) => s.compacted);

  return (
    <figure
      ref={ref}
      className="figure figure-cw"
      role="img"
      aria-label={
        'A context window is a fixed budget, not a memory. A bar of unchanging width fills with ' +
        'conversation turns sized in proportion to their token count — system prompt, user turns, ' +
        'assistant replies and large tool results. A counter climbs toward the 32,000-token limit; ' +
        'when the bar is full the oldest turns dim and collapse into a single small summary block, ' +
        'the counter drops, and new turns immediately take the reclaimed space. A rail beneath the ' +
        'bar shows the whole conversation at the same scale, running off the left edge of the frame: ' +
        'the history keeps growing while the window never does.'
      }
    >
      <div className="cw-hdr">
        <span className="label">What a context window holds</span>
        <div className="cw-beats">
          {BEAT_TEXT.map((beat, i) => (
            <div key={beat.title} className="cw-beat" style={{ opacity: beatOpacity(t, i, BEATS) }}>
              <span className="title">{beat.title}</span>
              <p className="cw-sub">{beat.sub}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="cw-meter">
          <div className="cw-meter-l">
            <span className="label">Context window · capacity {CAPACITY.toLocaleString('en-US')} tokens</span>
            <span className="label cw-atcap" style={{ opacity: pressure }}>
              At capacity
            </span>
          </div>
          <div className="cw-count">
            {layers.map((l) => (
              <div key={l.k} className="cw-count-in" style={{ opacity: l.o }}>
                <span className="label">Used</span>
                <span className="cw-num">{fmt(l.s.used)}</span>
                <span className="cw-tot">/ {CAPACITY.toLocaleString('en-US')}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="cw-bar" style={{ marginTop: 'clamp(9px, 1.3vw, 14px)' }}>
          {[0.25, 0.5, 0.75].map((p) => (
            <div key={p} className="cw-tick" style={{ left: `${p * 100}%` }} />
          ))}
          {layers.map((l) => (
            <div key={l.k} className="cw-layer" style={{ opacity: l.o }}>
              {l.s.blocks.map((p) => (
                <Block key={p.id} p={p} />
              ))}
              <div className="cw-pos" style={{ transform: frac(l.s.usedFrac), opacity: 0.85 }}>
                <div className="cw-edge" />
                <div className="cw-edge-dot" />
              </div>
            </div>
          ))}
          <div className="cw-full" style={{ opacity: pressure }} />
        </div>
      </div>

      <div className="cw-railwrap">
        <div className="cw-row">
          <div className="cw-stack">
            {layers.map((l) => (
              <span key={l.k} className="label" style={{ opacity: l.o }}>
                The conversation so far · {l.s.turns} turns · {fmt(l.s.everTokens)} tokens
              </span>
            ))}
          </div>
        </div>
        <div className="cw-rail fade-left">
          {layers.map((l) => (
            <div key={l.k} className="cw-layer" style={{ opacity: l.o }}>
              {l.s.rail.map((p) => (
                <Segment key={p.id} p={p} />
              ))}
            </div>
          ))}
        </div>
        <div className="cw-row">
          <span className="label" style={{ opacity: compacted }}>
            Compacted
          </span>
          <span className="label">Held in full</span>
        </div>
      </div>

      <div className="cw-legend">
        {(['system', 'user', 'assistant', 'tool result', 'summary'] as Kind[]).map((k) => (
          <span key={k} className="cw-leg">
            <span className="cw-sw" style={{ background: COLOR[k] }} />
            <span className="name">{k}</span>
          </span>
        ))}
      </div>
    </figure>
  );
}
