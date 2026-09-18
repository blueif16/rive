# Motion vocabulary — springs, morphs, cuts

The motion is Material 3 Expressive's physics scheme: spatial properties (position,
size, rotation, shape) overshoot and settle on a spring; effects (colour, opacity) never
overshoot. The camera is static. Cards change on hard cuts.

## 1. Spring tokens and their curve equivalents

Material publishes these curves for web use when a real spring is not available.
Use the token name in every move; the builder picks spring or curve.

| token | curve (cubic-bezier) | duration | use for |
|---|---|---|---|
| expressive fast spatial | 0.42, 1.67, 0.21, 0.90 | 350 ms | small elements, glyphs, accents |
| expressive default spatial | 0.38, 1.21, 0.22, 1.00 | 500 ms | shapes, badges, words |
| expressive slow spatial | 0.39, 1.29, 0.35, 0.98 | 650 ms | hero shapes, big morphs, clusters |
| expressive fast effects | 0.31, 0.94, 0.34, 1.00 | 150 ms | opacity of accents |
| expressive default effects | 0.34, 0.80, 0.34, 1.00 | 200 ms | colour and opacity |
| standard default spatial | 0.27, 1.06, 0.18, 1.00 | 500 ms | when a move must not bounce |

Spring form (for a real integrator): expressive default spatial ≈ stiffness 380,
damping ratio 0.8; fast ≈ 800, 0.6; slow ≈ 200, 0.8; effects ≈ 1600, 1.0. Values in
the y-axis above 1.0 are the overshoot; that overshoot is the signature, keep it.

## 2. Timing

- 120 BPM grid. Cards hold 1.0–1.5 s for a line, 0.5 s per number in a countdown,
  up to 2.5 s for a question or a closer.
- Hold ≥ reading time: 0.3 s + 0.25 s per word.
- Stagger: glyphs 40–60 ms apart, badges 80–120 ms, cluster members 120–160 ms.
- Entrances finish before the hold begins; exits finish before the cut.

## 3. The moves

| move | what happens | token | notes |
|---|---|---|---|
| Glyph stagger-in | letters spring in one by one from +0.2 em tracking and 0.8 scale | fast spatial | left to right, or centre-out for a hero word |
| Word land | a whole word drops or slides into its line position | default spatial | for sentences that assemble word by word on stepped lines |
| Tracking breathe | letters spread to make room, then a shape fills the gap | fast spatial | precedes every glyph swap |
| Glyph swap pop | the letter scales to zero as the shape springs to full size | fast spatial | shape may keep a slow rotation while the card holds |
| Shape morph | outline interpolates within its family | slow spatial | the countdown ground morphs Burst → Sunny → Clover8 as numbers change |
| Number slide | numbers move vertically inside a shape mask, next one entering as the last leaves | default spatial | mask = the hero shape |
| Badge roll-in | badges enter from one side with slight rotation, settle into a row | default spatial, 100 ms stagger | last badge may bleed off-frame |
| Cluster settle | four badges arrive from four directions and overlap at centre | slow spatial, 140 ms stagger | on an ink stage |
| Scale pop | a shape appears from 0 to 1 with overshoot | default spatial | the default entrance for any shape |
| Hero rotate | the hero shape rotates 5–15°/s during the hold | linear | only the hero, only while it is the subject |
| Accent draw-on | arrow, loop or squiggle reveals along its length | fast effects on reveal, then hold | one per card |
| Accent pop-off | the accent scales to zero or retracts | fast spatial | before the cut |
| Constellation drift | small shapes joined by curved lines drift 1–2 % of frame | slow spatial, looped as ping-pong | for a reflective card |
| Capsule fill | small shapes drop into a Pill and settle | fast spatial with 60 ms stagger | playful pause |
| Exit slide | the card's contents slide off one edge together | default spatial | when the next card enters from the opposite edge |
| Exit shrink | contents scale to zero at their own centres | fast spatial | the default exit |
| Hard cut | stage colour changes instantly | none | every card boundary |

## 4. Rules

- Spatial properties spring; colour and opacity use effects tokens and never overshoot.
- A shape morphs only on a state change (a number changes, a word lands). No idle
  morphing.
- The camera never moves. Depth is overlap only.
- Every card has exactly one focal event during its hold: a swap, a morph, an accent,
  or a rotation. Not several.
- Loops must reset invisibly on the grid.
- Reduced motion: every move has a snap-to-end equivalent; the spec notes this once.
