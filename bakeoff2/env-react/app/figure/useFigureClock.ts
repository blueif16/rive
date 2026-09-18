import { useEffect, useRef, useState } from 'react';

/**
 * The clock every figure runs on.
 *
 * Returns loop-normalised time in [0, 1) plus elapsed seconds, and handles the
 * three things the embed contract requires of every figure:
 *
 *   - pauses when the figure scrolls out of the viewport
 *   - freezes at `staticAt` when the reader prefers reduced motion
 *   - keeps running across beat changes, so nothing restarts mid-loop
 *
 * Drive every animated value from `t`. Do NOT use CSS animations for anything
 * that must stay in phase across a beat change — a CSS animation restarts when
 * its element remounts or its `animation` shorthand changes, which is exactly
 * the "motion restarted when it faded back in" defect.
 */
export interface FigureClock {
  /** Loop position, 0 <= t < 1. */
  t: number;
  /** Seconds since mount, unpaused. */
  elapsed: number;
  /** True when reduced motion is requested — render the still composition. */
  reduced: boolean;
  /** Attach to the figure's outermost element. */
  ref: React.RefObject<HTMLDivElement>;
  /** False while scrolled out of view. */
  running: boolean;
}

export function useFigureClock(loopSeconds: number, staticAt = 0.08): FigureClock {
  const ref = useRef<HTMLDivElement>(null);
  const [reduced, setReduced] = useState(false);
  const [inView, setInView] = useState(false);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const sync = () => setReduced(mq.matches);
    sync();
    mq.addEventListener('change', sync);
    return () => mq.removeEventListener('change', sync);
  }, []);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([e]) => setInView(e.isIntersecting),
      { rootMargin: '10% 0px' },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const running = inView && !reduced;

  useEffect(() => {
    if (!running) return;
    let raf = 0;
    let last = performance.now();
    const tick = (now: number) => {
      const dt = Math.min((now - last) / 1000, 0.1); // clamp tab-switch jumps
      last = now;
      setElapsed((e) => e + dt);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [running]);

  const t = reduced ? staticAt : (elapsed % loopSeconds) / loopSeconds;
  return { t, elapsed, reduced, ref, running };
}

/** Linear interpolation. */
export const lerp = (a: number, b: number, u: number) => a + (b - a) * u;

/** Clamp to [0, 1]. */
export const sat = (u: number) => (u < 0 ? 0 : u > 1 ? 1 : u);

/** Symmetric ease, matching the house crossfade feel. */
export const easeInOut = (u: number) =>
  u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;

/**
 * Opacity of beat `i` at loop position `t`, given `n` beats and a crossfade
 * that is `fade` of a beat long. Use this for every beat-gated element so all
 * of them cross-fade on exactly the same curve.
 */
export function beatOpacity(t: number, i: number, n: number, fade = 0.14) {
  const pos = t * n;
  const d = Math.min(
    Math.abs(pos - i),
    Math.abs(pos - i - n),
    Math.abs(pos - i + n),
  );
  if (d <= 0.5 - fade) return 1;
  if (d >= 0.5 + fade) return 0;
  return easeInOut(1 - (d - (0.5 - fade)) / (2 * fade));
}
