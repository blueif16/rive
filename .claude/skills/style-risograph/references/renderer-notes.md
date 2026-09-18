# Renderer appendix — what changes per build target

The medium rules never change. What changes is where tone comes from, how plates
composite, how time is expressed, and how the builder verifies. Write only the appendix
for the renderer named in the inputs.

## Canvas 2D (single self-contained HTML)

- **Plates are offscreen canvases.** Draw each ink's coverage as greyscale, threshold it
  against a precomputed screen tile for that ink's angle, tint, then multiply onto the
  paper with the plate's misregistration offset. This is a true print simulation: dot
  ramps, rosettes and dot gain come for free.
- **Knockouts** are `destination-out` draws on the darker plate. Cheap; list them anyway.
- **Pre-render static plates** to bitmaps once per scene, with a loading bar. Animate only
  transforms and the one live element. Target 60 fps on a laptop.
- **Time** is `render(t)`, a pure function. Easings are inline functions of normalised
  progress. The cue array drives which scenes and transitions are active.
- **Stroke reveal** needs arc-length sampling of each glyph path; budget it.
- **Verify** with `?t=` stills in headless Chrome, and by asserting the anchor's pixel
  position in code at every act boundary.
- Controls: space play/pause, scrubber with act markers, arrow keys to step 1/24 s,
  record via `captureStream` + `MediaRecorder`. Optional muted WebAudio at the BPM.

## Rive (RML compiled by the Rive CLI, rendered by the Rive runtime)

Lessons from the `riso-call` build in this repo (`riso-call/generate.py`).

- **Tone is geometry.** A dot screen is one `Shape` holding thousands of `Ellipse` children;
  about 12,000 dots for four scenes was the practical ceiling. Use screens for ramps and
  glows only; solids elsewhere. For many scenes, switch to grain plates or fewer dots.
- **Knockouts are evenOdd holes.** A light shape on a dark plate must be cut out of the dark
  shape with a second geometry child and `fillRule="evenOdd"`, or multiply prints it black.
- **Every sheet needs an opaque cream backing** as its last child, or a disc opening over
  the previous scene shows the old scene through it.
- **Overprint** is `blendModeValue="multiply"` on the shape. Misregistration is a translated
  group per ink.
- **Ripples**: key the `PointsPath` scale, not the `Shape` scale, so the stroke stays in
  screen pixels; key stroke thickness separately.
- **Reveals** are `ClippingShape` masks whose scale is keyed; overshoot is two keys, not a
  bezier past 1. Coin flip keys scaleX with a rim shape behind. Hard cuts are hold keys on
  opacity or a keyed `Solo`.
- **Lettering** is a `TrimPath` inside the stroke, `end` keyed 0→1. Rive beats Canvas here.
- **No scripts** unless the file will be `--publish`ed; unsigned Luau is rejected by web
  runtimes. Keep everything as keyframes so the piece stays seekable.
- **Verify** with `render.mjs --stills=` at each boundary and `place.mjs --nodes=<anchor>`
  to measure the anchor's world origin; never eyeball it (see project CLAUDE.md).
- Deliverable is a `.riv` plus MP4/GIF renders; the HTML viewer needs the runtime.

## After Effects

- One precomp per ink plate in greyscale; a halftone or stochastic effect per plate at its
  own angle; tint; multiply onto a paper layer; per-plate position offset changed by
  hold keyframes at cuts. Posterize time to 12 or 8 fps on character layers only.
- Paper grain is a single still layer, never a looping noise.
- Export frames per plate if the piece will be printed for real (the Hiromu Oka workflow).
