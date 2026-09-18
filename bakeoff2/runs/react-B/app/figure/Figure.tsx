import { useFigureClock, beatOpacity } from './useFigureClock';
import './figure.css';

const LOOP_SECONDS = 12;
const BEATS = 4;

/**
 * Replace this with the figure the spec describes.
 *
 * Drive every animated value from `t` (loop position, 0..1). Use beatOpacity()
 * for anything that fades in and out with a beat. Keep continuous motion as a
 * function of t so it never restarts when an element fades back in.
 */
export default function Figure() {
  const { t, reduced, ref } = useFigureClock(LOOP_SECONDS);

  return (
    <figure
      ref={ref}
      className="figure"
      role="img"
      aria-label="Replace with a sentence describing what this figure conveys."
      style={{ aspectRatio: '2 / 1', minHeight: 260 }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'grid',
          placeItems: 'center',
          opacity: beatOpacity(t, 0, BEATS),
        }}
      >
        <span className="title" style={{ fontSize: 42 }}>
          Figure scaffold
        </span>
      </div>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'grid',
          placeItems: 'center',
          opacity: beatOpacity(t, 1, BEATS),
        }}
      >
        <span className="label">beat two{reduced ? ' · reduced motion' : ''}</span>
      </div>
    </figure>
  );
}
