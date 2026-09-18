/**
 * Motion maths for the world-model taxonomy figure.
 *
 * Everything that moves is a CSS animation driven off constants declared here,
 * so the SVG geometry and the keyframes can never drift apart. The generated
 * keyframes are written in terms of CSS custom properties (`--wmf-amp`,
 * `--wmf-swing`, `--chip-pitch`) which means one set of keyframes serves every
 * breakpoint — only the variables change.
 */

/* ------------------------------------------------------------------ wave */

/** Harmonics of the simulated state signal: [multiple, amplitude, phase]. */
const HARMONICS: ReadonlyArray<readonly [number, number, number]> = [
  [1, 0.7, 0],
  [2, 0.22, 0.9],
  [3, 0.08, 2.35],
];

const rawWave = (u: number): number =>
  HARMONICS.reduce((sum, [k, a, p]) => sum + a * Math.sin(2 * Math.PI * k * u + p), 0);

const PEAK = (() => {
  let m = 0;
  for (let i = 0; i < 4000; i += 1) m = Math.max(m, Math.abs(rawWave(i / 4000)));
  return m;
})();

/** Normalised state signal, period 1, range [-1, 1]. */
export const wave = (u: number): number => rawWave(u) / PEAK;

/** Resting value used for the reduced-motion still frame. */
export const WAVE_REST = wave(0);

/* ----------------------------------------------------------------- plot */

export const PLOT_W = 100; // viewBox width = the visible window
export const PLOT_CYCLE = 50; // one period of the signal, in viewBox units
export const PLOT_SPAN = PLOT_W + PLOT_CYCLE; // drawn length, so one period can scroll off
export const PLOT_MID = 50;
export const PLOT_AMP = 30; // viewBox units; --wmf-amp must stay 0.30 * plot height

/** Trace path long enough to scroll exactly one period and repeat seamlessly. */
export function tracePath(): string {
  const pts: string[] = [];
  for (let x = 0; x <= PLOT_SPAN; x += 1) {
    const y = PLOT_MID - PLOT_AMP * wave(x / PLOT_CYCLE);
    pts.push(`${x} ${y.toFixed(2)}`);
  }
  return `M${pts.join('L')}`;
}

/** Vertical gridlines, spaced so they scroll with the trace and tile. */
export const PLOT_GRID = Array.from({ length: PLOT_SPAN / 25 + 1 }, (_, i) => i * 25);

/* ---------------------------------------------------------------- chips */

export const ACTIONS = ['scan', 'grasp', 'lift', 'rotate', 'move', 'place'] as const;
export const CHIP_CYCLE = ACTIONS.length; // chips per repeat
export const CHIP_COUNT = 18; // enough to cover the widest lane plus one cycle
export const CHIP_MOVE_FRAC = 0.26; // share of a step spent moving; rest is held
/** Which chip slot (in pitches from the right edge) counts as "now". */
export const CHIP_SLOT = 1;
/** Index of the chip resting in the slot when the timeline is frozen at 0. */
export const CHIP_REST_INDEX = CHIP_SLOT + CHIP_CYCLE;

/**
 * Only these chips ever pass through the decision slot. Every other chip in the
 * track is a duplicate six pitches away, and animating its highlight too would
 * light a second chip off-screen — which becomes visible if the figure is
 * dropped into a very wide column.
 */
export const canBeChosen = (i: number): boolean =>
  i >= CHIP_SLOT && i < CHIP_SLOT + CHIP_CYCLE;

/** Rightmost chip is index 0, so left-to-right reads past -> future. */
export const chipLabel = (i: number): string =>
  ACTIONS[(CHIP_CYCLE - (i % CHIP_CYCLE)) % CHIP_CYCLE];

/* ---------------------------------------------------------------- film */

export const FILM_CYCLE = 12; // frames per sun arc
export const FILM_COUNT = 24;

/** 0 = sunrise, approaching 1 = sunset. Rightmost frame is the newest. */
export const filmPhase = (i: number): number =>
  ((FILM_CYCLE - (i % FILM_CYCLE)) % FILM_CYCLE) / FILM_CYCLE;

/* ------------------------------------------------------- CSS generation */

const pct = (n: number) => `${+n.toFixed(4)}%`;

function waveKeyframes(stops = 72): string {
  const dot: string[] = [];
  const pend: string[] = [];
  for (let i = 0; i <= stops; i += 1) {
    const p = i / stops;
    const v = +wave(p).toFixed(4);
    // Screen y grows downward, and a clockwise rotation swings a hanging bob
    // to the left — so both signs are flipped to keep "positive x(t)" meaning
    // "bob to the right, dot above the zero line".
    dot.push(`${pct(p * 100)}{transform:translate3d(0,calc(var(--wmf-amp) * ${-v}),0)}`);
    pend.push(`${pct(p * 100)}{transform:rotate(calc(var(--wmf-swing) * ${-v}))}`);
  }
  return `@keyframes wmf-dot{${dot.join('')}}@keyframes wmf-pend{${pend.join('')}}`;
}

function chipKeyframes(): string {
  const stepPct = 100 / CHIP_CYCLE;
  // Snap, then hold: the row jumps one pitch at the head of each step and sits
  // perfectly still for the rest of it. That stillness is what makes the
  // planner's output read as discrete rather than as a stream.
  const at = (k: number) => `transform:translate3d(calc(var(--chip-pitch) * ${-k}),0,0)`;
  const march: string[] = [`0%{${at(0)}}`];
  for (let k = 0; k < CHIP_CYCLE; k += 1) {
    march.push(`${pct((k + CHIP_MOVE_FRAC) * stepPct)}{${at(k + 1)}}`);
    march.push(`${pct((k + 1) * stepPct)}{${at(k + 1)}}`);
  }
  // A chip's own timeline is zeroed on the instant it lands in the decision
  // slot; it stays chosen for exactly the hold, then releases as the row moves.
  const hold = (1 - CHIP_MOVE_FRAC) * stepPct;
  const idle = `background:var(--cream);border-color:var(--edge);color:var(--warm-dk)`;
  const live = `background:var(--lav-wash);border-color:var(--lavender);color:var(--ink)`;
  const pick =
    `@keyframes wmf-pick{` +
    `0%,${pct(hold - 0.6)}{${live}}` +
    `${pct(hold + 0.5)},100%{${idle}}}`;
  return `@keyframes wmf-march{${march.join('')}}${pick}`;
}

/**
 * Chip `i` reaches the decision slot at t = (SLOT + 5 - i + MOVE) * step, so
 * giving it that value as its animation-delay zeroes its own timeline on the
 * instant it lands. The highlight is therefore locked to a fixed screen
 * position at any container width, which is what lets the whole lane stay in
 * pure CSS.
 */
export const CHIP_DELAY_OFFSET = CHIP_SLOT + 5 + CHIP_MOVE_FRAC;

export function motionCSS(): string {
  return (
    waveKeyframes() +
    chipKeyframes() +
    // Derived from the march geometry, so the highlight can never drift out of
    // step with the row. Kept here rather than in figure.css for that reason.
    `.wmf .wmf-chip[data-pick="true"]{` +
    `animation-delay:calc((${CHIP_DELAY_OFFSET} - var(--i)) * var(--chip-step))}`
  );
}

/** Resting transforms used when prefers-reduced-motion freezes the figure. */
export function staticCSS(root = '.wmf[data-mode="static"]'): string {
  const v = +WAVE_REST.toFixed(4);
  return (
    `${root} .wmf-anim{animation:none !important}` +
    `${root} .wmf-dot{transform:translate3d(0,calc(var(--wmf-amp) * ${-v}),0) !important}` +
    `${root} .wmf-pendulum-arm{transform:rotate(calc(var(--wmf-swing) * ${-v})) !important}` +
    `${root} .wmf-chip[data-i="${CHIP_REST_INDEX}"]{` +
    `background:var(--lav-wash) !important;border-color:var(--lavender) !important;` +
    `color:var(--ink) !important}`
  );
}
