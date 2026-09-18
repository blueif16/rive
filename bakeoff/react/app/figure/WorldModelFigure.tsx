import {
  useEffect,
  useInsertionEffect,
  useMemo,
  useRef,
  useState,
  type ComponentType,
  type CSSProperties,
} from 'react';
import {
  CHIP_COUNT,
  FILM_COUNT,
  PLOT_GRID,
  canBeChosen,
  chipLabel,
  filmPhase,
  motionCSS,
  staticCSS,
  tracePath,
} from './motion';
import './figure.css';

/* --------------------------------------------------------------- content */

const BEAT_MS = 3400;
const BEATS = 4;

type LaneId = 'renderer' | 'simulator' | 'planner';

interface LaneDef {
  id: LaneId;
  verb: string;
  output: string;
  title: string;
  subtitle: string;
  /** Which lane band the title card occupies when this lane is solo. */
  slot: 0 | 1;
}

const LANES: LaneDef[] = [
  {
    id: 'renderer',
    verb: 'renders',
    output: 'observations',
    title: 'Renderer',
    subtitle: 'outputs observations',
    slot: 1,
  },
  {
    id: 'simulator',
    verb: 'simulates',
    output: 'state',
    title: 'Simulator',
    subtitle: 'outputs state',
    slot: 0,
  },
  {
    id: 'planner',
    verb: 'plans',
    output: 'actions',
    title: 'Planner',
    subtitle: 'outputs actions',
    slot: 1,
  },
];

const ARIA_LABEL =
  'Animated diagram of three world-model functions, each emitting a different kind of output. ' +
  'The renderer lane is a film strip: framed pictures of one landscape glide past, the sun a little ' +
  'further along its arc in each frame, so the strip reads as a continuous shot sampled into images — ' +
  'its output is observations. The simulator lane is a swinging pendulum beside a live plot of x of t: ' +
  'an unbroken curve scrolls leftward with a dot riding its right-hand edge — its output is state, a ' +
  'continuous signal. The planner lane is a row of labelled action chips — scan, grasp, lift, rotate, ' +
  'move, place — that advance one discrete step at a time, each chip highlighted as it becomes the ' +
  'chosen action — its output is actions, discrete choices from a finite set. The figure loops through ' +
  'four beats: all three lanes together, then the renderer, the simulator and the planner alone.';

/* ------------------------------------------------------------ primitives */

function FilmCell({ phase }: { phase: number }) {
  // Sun arc across one "day" per 12 cells: the whole point of the lane is that
  // each picture is a later sample of one continuous shot.
  const sx = 10 + 90 * phase;
  const sy = 58 - 42 * Math.sin(Math.PI * phase);
  return (
    <svg className="wmf-cell-svg" viewBox="0 0 112 96" aria-hidden="true" focusable="false">
      <rect
        className="wmf-cell-base"
        x="0.6"
        y="0.6"
        width="110.8"
        height="94.8"
        rx="1.2"
      />
      <g className="wmf-cell-perf">
        {[0, 1, 2, 3, 4, 5].map((j) => (
          <g key={j}>
            <rect x={3.5 + j * 19} y="2.6" width="10" height="5.8" rx="1.1" />
            <rect x={3.5 + j * 19} y="87.6" width="10" height="5.8" rx="1.1" />
          </g>
        ))}
      </g>
      <svg x="1" y="10" width="110" height="72" viewBox="0 0 110 72">
        <path className="wmf-cell-far" d="M-6 66 L24 42 L56 66 Z" />
        <circle className="wmf-cell-sun" cx={sx} cy={sy} r="5" />
        <path className="wmf-cell-near" d="M-8 66 L32 46 L48 54 L70 34 L118 66 Z" />
      </svg>
      <path className="wmf-cell-ground" d="M1 76 H111" />
    </svg>
  );
}

function Renderer() {
  const cells = useMemo(
    () => Array.from({ length: FILM_COUNT }, (_, i) => filmPhase(i)),
    [],
  );
  return (
    <div className="wmf-film">
      <div className="wmf-film-track wmf-anim">
        {cells.map((phase, i) => (
          <div className="wmf-cell" key={i}>
            <FilmCell phase={phase} />
          </div>
        ))}
      </div>
    </div>
  );
}

function Pendulum() {
  return (
    <div className="wmf-system">
      <span className="wmf-micro">System</span>
      <svg className="wmf-pendulum" viewBox="0 0 92 104" aria-hidden="true" focusable="false">
        <path className="wmf-pend-arc" d="M19.8 72.2 A62 62 0 0 1 72.2 72.2" />
        <path className="wmf-pend-plumb" d="M46 16 V86" />
        <g className="wmf-pendulum-arm wmf-anim">
          <path className="wmf-pend-rod" d="M46 16 V78" />
          <circle className="wmf-pend-halo" cx="46" cy="78" r="14.4" />
          <circle className="wmf-pend-bob" cx="46" cy="78" r="9.4" />
        </g>
        <circle className="wmf-pend-pivot" cx="46" cy="16" r="3.4" />
      </svg>
    </div>
  );
}

function Plot() {
  const d = useMemo(tracePath, []);
  return (
    <div className="wmf-plot">
      <span className="wmf-plot-y">x(t)</span>
      <div className="wmf-plot-axis" aria-hidden="true">
        <span /> <span /> <span />
      </div>
      <div className="wmf-plot-body">
        <svg
          className="wmf-plot-static"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          aria-hidden="true"
          focusable="false"
        >
          <path className="wmf-plot-zero" d="M0 50 H100" vectorEffect="non-scaling-stroke" />
        </svg>
        <svg
          className="wmf-plot-live"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          aria-hidden="true"
          focusable="false"
        >
          <g className="wmf-trace wmf-anim">
            {PLOT_GRID.map((x) => (
              <path
                key={x}
                className="wmf-plot-grid"
                d={`M${x} 6 V94`}
                vectorEffect="non-scaling-stroke"
              />
            ))}
            <path className="wmf-plot-trace" d={d} vectorEffect="non-scaling-stroke" />
          </g>
        </svg>
      </div>
      <div className="wmf-dot wmf-anim" aria-hidden="true">
        <span className="wmf-dot-halo" />
        <span className="wmf-dot-core" />
      </div>
      <span className="wmf-plot-x">t →</span>
    </div>
  );
}

function Simulator() {
  return (
    <div className="wmf-sim">
      <Pendulum />
      <Plot />
    </div>
  );
}

function Planner() {
  const chips = useMemo(
    () => Array.from({ length: CHIP_COUNT }, (_, i) => chipLabel(i)),
    [],
  );
  return (
    <div className="wmf-chips">
      <div className="wmf-chip-track wmf-anim">
        {chips.map((label, i) => (
          <div
            className="wmf-chip wmf-anim"
            key={i}
            data-i={i}
            data-pick={canBeChosen(i)}
            style={{ '--i': i } as CSSProperties}
          >
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}

const LANE_BODY: Record<LaneId, ComponentType> = {
  renderer: Renderer,
  simulator: Simulator,
  planner: Planner,
};

/* ----------------------------------------------------------------- hooks */

function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(() =>
    typeof window !== 'undefined' && typeof window.matchMedia === 'function'
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false,
  );
  useEffect(() => {
    if (typeof window.matchMedia !== 'function') return;
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const on = () => setReduced(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  return reduced;
}

/**
 * Injected once per document and shared by every instance of the figure —
 * a second figure on the page adds no extra CSS. useInsertionEffect runs
 * before paint, so the animations start on the first frame rather than
 * appearing frozen for a beat.
 */
function useMotionStyles() {
  useInsertionEffect(() => {
    const id = 'wmf-generated-motion';
    if (document.getElementById(id)) return;
    const el = document.createElement('style');
    el.id = id;
    el.textContent = motionCSS() + staticCSS();
    document.head.appendChild(el);
  }, []);
}

/* ------------------------------------------------------------- component */

export default function WorldModelFigure({ className = '' }: { className?: string }) {
  useMotionStyles();
  const reduced = usePrefersReducedMotion();
  const rootRef = useRef<HTMLElement | null>(null);
  const [inView, setInView] = useState(false);
  const [wants, setWants] = useState<boolean | null>(null); // explicit user choice
  const [beat, setBeat] = useState(0);

  const motionWanted = wants ?? !reduced;
  const mode = !motionWanted ? 'static' : inView ? 'running' : 'paused';
  const running = mode === 'running';

  // Play only while on screen.
  useEffect(() => {
    const node = rootRef.current;
    if (!node || typeof IntersectionObserver === 'undefined') {
      setInView(true);
      return;
    }
    const io = new IntersectionObserver(
      ([entry]) => setInView(entry.isIntersecting),
      { rootMargin: '96px 0px', threshold: 0 },
    );
    io.observe(node);
    return () => io.disconnect();
  }, []);

  // Beat clock. Elapsed time is banked on pause so the loop resumes in place,
  // exactly like the CSS animations it sits alongside.
  const bankedRef = useRef(0);
  useEffect(() => {
    if (!running) return;
    const started = performance.now();
    let timer = 0;
    const step = () => {
      const total = bankedRef.current + (performance.now() - started);
      setBeat(Math.floor(total / BEAT_MS) % BEATS);
      timer = window.setTimeout(step, BEAT_MS - (total % BEAT_MS) + 6);
    };
    step();
    return () => {
      window.clearTimeout(timer);
      bankedRef.current += performance.now() - started;
    };
  }, [running]);

  useEffect(() => {
    if (mode === 'static') setBeat(0);
  }, [mode]);

  const solo = beat === 0 ? null : LANES[beat - 1].id;

  return (
    <figure ref={rootRef} className={`wmf ${className}`} data-mode={mode} data-beat={beat}>
      <div className="wmf-stage">
        <div className="wmf-plate" role="img" aria-label={ARIA_LABEL}>
          <div className="wmf-lanes">
            {LANES.map((lane) => {
              const Body = LANE_BODY[lane.id];
              return (
                <div
                  className="wmf-lane"
                  key={lane.id}
                  data-lane={lane.id}
                  data-dim={solo !== null && solo !== lane.id}
                >
                  <div className="wmf-media">
                    <Body />
                  </div>
                  <div className="wmf-card">
                    <span className="wmf-card-verb">{lane.verb}</span>
                    <span className="wmf-card-out">
                      <i className="wmf-card-arrow">→</i>
                      {lane.output}
                    </span>
                  </div>
                </div>
              );
            })}

            {LANES.map((lane) => (
              <div
                className="wmf-title"
                key={`t-${lane.id}`}
                data-lane={lane.id}
                data-on={solo === lane.id}
                style={{ '--slot': lane.slot } as CSSProperties}
              >
                <span className="wmf-title-name">{lane.title}</span>
                <span className="wmf-title-sub">{lane.subtitle}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      <figcaption className="wmf-caption">
        <p className="wmf-caption-text">
          <b>Three functions, three kinds of output.</b> The same world model can{' '}
          <i>render</i> observations — a stream of pictures; <i>simulate</i> state — one
          continuous signal; or <i>plan</i> actions — discrete choices from a finite set.
        </p>
        <button
          type="button"
          className="wmf-toggle"
          onClick={() => setWants(!motionWanted)}
          aria-pressed={motionWanted}
          title={motionWanted ? 'Pause animation' : 'Play animation'}
        >
          <span className="wmf-sr">
            {motionWanted ? 'Pause animation' : 'Play animation'}
          </span>
          <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">
            {motionWanted ? (
              <g>
                <rect x="4.6" y="3.4" width="2.3" height="9.2" rx="0.6" />
                <rect x="9.1" y="3.4" width="2.3" height="9.2" rx="0.6" />
              </g>
            ) : (
              <path d="M5.2 3.3 L12.6 8 L5.2 12.7 Z" />
            )}
          </svg>
        </button>
      </figcaption>
    </figure>
  );
}
