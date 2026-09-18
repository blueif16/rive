# Motion vocabulary — moves that come from the printing process

A riso film is a stack of sheets. Every move below is either something a sheet can do
(turn, slide, be punched, be printed plate by plate) or something ink can do (spread,
drain, dissolve). Anything that is neither is suspect. Riso animators who print every
frame (Hiromu Oka, Kelli Anderson's workshops) work exactly this way; digital fakes that
ignore it read as filters.

## 1. Timing grid

- 120 BPM default: 0.25 s and 0.5 s units; act boundaries on whole beats.
- Montage cuts are hard cuts on the grid, accelerating from 0.5 s to 0.25 s per scene.
- "Breathe" every 2 s or so in a montage: one beat of blank paper with a single motif
  event before the next scene irises open.
- Character and creature motion runs on twos or threes (12 or 8 drawings per second
  equivalent). Camera moves, ripples and blooms stay smooth. Mixing the two is the point.

## 2. The moves

| move | print origin | easing | duration | parameters |
|---|---|---|---|---|
| Ripple / ring | a stencil circle growing | easeOutCubic | 0.5–0.7 s | radius to beyond the corner; stroke thins 6→1 px; opacity fades from 35 %; radius wobble 2–3 %; 2–3 tick arcs flick at the rim for 0.15 s |
| Iris / disc reveal | a punched hole | easeOutBack as two keys (1.08 then 1.0) | 0.35–0.45 s | disc 55 % of frame; opaque paper backing inside the disc |
| Coin flip | a sheet turning edge-on | easeOutCubic | 0.35 s | scaleX 0→1.06→1; rim in the line ink, offset −12 px during the flip |
| Sheet slide | a sheet sliding under the lens | easeOutCubic | 0.45 s | from +1.1 frame widths; rotation 0.5→0 rad |
| Dive | the lens pushing through the hole | easeInOutCubic | 0.35 s | scene scale 0.55→1.0 while the mask grows past the corners; anchor fixed |
| Hard cut | next sheet | none | 0 | on the grid; new misregistration vector |
| Plate-by-plate reveal | printing light to dark | hold keys | 0.1–0.15 s per plate | yellow, then pink/orange, then blue/violet, then line |
| Lens ring | the registration target | linear | per shot | pale double outline around the anchor, tightening 4–6 px per shot |
| Archive pull-back | contact sheet of prints | easeInOutCubic | 1.5–2 s | current scene shrinks to a medallion; ~40 medallions on 4 orbits, orbits alternate direction |
| Ink drain | reprinting in one ink | linear crossfade | 0.6 s | the only allowed crossfade: each medallion re-rendered as one blue plate from luminance |
| Scatter | sheets blown off the table | easeInQuad | 0.8 s | outward while shrinking to zero |
| Bloom | petals printed one by one | easeOutBack with 40 ms stagger | 0.6 s then slow spin | halftone petals, orange-yellow heart |
| Stroke reveal | the pen writing | linear along length | 0.2–0.3 s per glyph, 2-frame lag on the pink plate | single-line glyphs; misregistered copy behind |
| Halftone dissolve | ink starving | easeInQuad, noise-staggered | 0.5 s | lettering becomes dots that shrink to zero |
| Registration drift as a cut | re-registering the sheet | hold | 0 | plate offsets jump to new vectors on the beat |

## 3. Camera

- Only pans and zooms about the anchor, critically damped, no overshoot, no jitter.
- No 3D, no parallax deeper than two planes, no motion blur.
- The anchor never drifts for the whole first two thirds of a piece; a pan that moves it
  is a story event and must be written as one.

## 4. Texture in motion

- Paper grain is static for the whole film. It never boils, never scrolls.
- Every object's texture (dots, voids, speckle) is seeded from the object and moves with
  it. Texture that stays fixed to the frame while the object moves reads as a filter.
- Misregistration vectors change only at cuts.
- Line boil is allowed only as a deliberate choice for a living subject: a 3–8 frame loop
  at 8–12 fps, amplitude 1–2 px, never on the motif.

## 5. Limited animation

- Move what matters: arcs, wings, water rings, flames, beams, a striker, a tail. Hold the
  rest as printed plates.
- Cycles are fine; a loop should reset invisibly on the grid.
- One live element per scene in a montage; two or three in a held scene.

## 6. Determinism

- Every frame is a pure function of time. Seeded randomness per scene and per element,
  never a random call inside the render loop.
- The timeline is data: cues with start, duration, kind, scene, transition, parameters.
