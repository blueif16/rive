# Renderer appendix — what changes per build target

The vocabulary never changes. What changes is how shapes are generated, how springs are
integrated, and how type is measured for glyph swaps.

## Canvas 2D (single self-contained HTML)

- **Shapes are generators**: `shape(name, R)` returns a polygon of N points (64 or 128)
  from the recipes in language-rules §1; round the tips with a small corner radius
  where the recipe says rounded. Draw with `fill()` only.
- **Morph by resampling**: both outlines to the same N points starting at angle 0; lerp
  point-wise with a spatial spring value.
- **Springs**: either integrate a damped spring per property each frame with fixed dt,
  or map the token to its cubic-bezier curve and duration from motion-vocabulary §1.
  Curves are deterministic and seekable; springs need a fixed-step integrator to stay
  deterministic. State the choice.
- **Type**: `ctx.font` with the system stack from language-rules §3; measure with
  `measureText` to place each glyph for stagger and swaps. A swapped glyph's shape sits
  at the glyph's advance box, centred at x-height.
- **Accents**: paths sampled to polylines; draw-on is a prefix of the polyline by length.
- **Cards**: a scheduler picks the card for time t; all card content is a pure function
  of local time. Seeded randomness only for constellation scatter.
- **Verify**: `?t=` stills in headless Chrome at 1280×720 and scaled to 160 px for the
  legibility check; count colours used per frame in a script to enforce the eight.
- Controls: space play/pause, scrubber with card markers, arrow keys to step, record via
  `captureStream` + `MediaRecorder`.

## Rive (RML compiled by the Rive CLI)

- Shapes as `PointsPath` with `CubicMirroredVertex` or `StraightVertex` children;
  vertex x/y are animatable, so a morph is a keyed vertex set (same vertex count).
- Springs: `elastic` interpolation with small amplitude, or `cubicValue` curves that
  overshoot past the target; the Material curves with y > 1 need `cubicValue`, not
  `cubic`.
- Type needs a `FontAsset` (a `.ttf` in the project). Geometric sans files are fine
  if provided; otherwise letter the copy as single-line paths and say so.
- Glyph swaps: a `Solo` keyed between the glyph run and the shape.
- Stage colour change: keyed `KeyFrameColor` with hold interpolation on the background
  fill.
- Verify with `render.mjs --stills=` and `place.mjs` for shape positions.

## After Effects

- One shape layer per cast member; morph via path keyframes between resampled paths.
- Springs via expressions implementing stiffness/damping, or the curve table as
  keyframe eases.
- Text layers with per-character animators for stagger and tracking; swaps as a shape
  layer parented to the text's character position.
