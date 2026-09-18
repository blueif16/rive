# Language rules — the fixed vocabulary of expressive geometry

Derived from Google's Material 3 Expressive system (35-shape library with built-in
morphing, spring motion physics, expressive type) and from frame analysis of a Google
event holding-screen package (hello / welcome / countdown / grab a snack / question /
see you soon / beautiful). Nothing here is decoration to be sprinkled; it is the cast.

## 1. Shapes: a named library, drawn procedurally

All shapes are filled polygons built from a circle of radius R with n features. No
outlines. A builder needs only these recipes:

| name | recipe | reads as |
|---|---|---|
| Circle | plain | badge ground, dot |
| Pill | rect with full-radius ends, ratio 2.4:1 | capsule, button |
| Semicircle | half disc, flat edge down or up | stage, bowl, sunrise |
| Star4 | 4 points, inner radius 0.42 R, sharp | sparkle, "i" dot, highlight |
| Sunny | 8 rays, inner 0.72 R, rounded tips | sun, "o" swap, warmth |
| VerySunny | 16 rays, inner 0.78 R, sharp | glow, burst of attention |
| Burst | 12 spikes, inner 0.62 R, sharp | ta-da, countdown ground |
| Boom | 10–14 spikes of two alternating lengths, inner 0.5 R | loud accent |
| Clover8 | 8 lobes, inner 0.7 R, fully rounded | soft flower, "o" swap |
| Cookie6 / Cookie9 | 6 or 9 shallow notches, inner 0.9 R, rounded | badge ground with character |
| Flower | 8 petals, inner 0.6 R, rounded | "o" swap, celebration |
| Diamond | rotated rounded square | gem, marker |

Rules:
- A piece uses a **cast of 4–6** of these. The same cast recurs on every card.
- Shapes are solid, one colour each. Two shapes may overlap; the overlap is opaque.
- **Morphing** is between shapes of the same family: Star4 ↔ Burst ↔ Sunny ↔ VerySunny;
  Circle ↔ Cookie ↔ Clover8 ↔ Flower; Circle ↔ Pill ↔ Semicircle. Morph by resampling
  both outlines to the same point count (64 or 128) and interpolating with a spatial
  spring. Never morph across families (a Burst into a Pill).
- Shapes rotate slowly (5–15° per second) only while they are the card's hero; they
  never spin continuously as decoration.

## 2. Palette: eight colours, four of them stages

| role | hex | use |
|---|---|---|
| stage blue | `#4A7BF7` | full-bleed background; cream shapes and type on it |
| stage orange | `#F4603A` | background; cream shapes and type |
| stage yellow | `#F2BE4B` | background; cream and ink shapes |
| stage green | `#6DBF9A` | background; cream and ink shapes |
| cream | `#F4EEE4` | the neutral stage and the shape colour on stages |
| ink | `#1F2125` | type, arrows, squiggles, the dark stage |
| blush | `#F5D8DA` | soft stage and soft shape |
| grey | `#9AA1A8` | one supporting shape colour on ink |

Rules:
- Every card has exactly one stage colour, full bleed, flat. Stage changes are hard cuts.
- Type is ink on cream, blush and yellow; cream on blue, orange, green and ink.
- A brand may substitute its own colours, mapped onto the same eight roles. Keep four
  saturated stages, one neutral, one ink, one soft, one grey.
- No gradients, no tints, no transparency, no texture, no shadow.

## 3. Type: the subject

- Face: a geometric grotesque with round terminals (Google Sans class). In an
  asset-free build use a system stack such as `"Google Sans", "Product Sans",
  "Avenir Next", "Helvetica Neue", Arial, sans-serif` and say so in the appendix.
- Sentence case. Weight medium to semibold. One size per card, from a three-step
  scale: hero 22 % of frame height (single words, numbers), statement 12 % (lines up to
  four words), sentence 8 % (five to seven words, wrapped to at most three lines).
- Centred, or left-stepped for a sentence that lands word by word on staggered lines.
- Tracking breathes: letters arrive with +0.2 em spacing and settle to normal, or a
  word opens up to make room for a swap.
- Lines wrap by meaning ("See you / Soon!"), never mid-phrase.

## 4. Glyph swaps

- Only round or dotted letters are swapped: **o** → Sunny, Clover8, Flower, Circle;
  **i**'s dot → Star4; **u** → Semicircle bowl; **a** or **e** counter → small Circle.
- At most two swaps per line. The swapped shape sits on the baseline at x-height, in
  a stage colour that contrasts with the ink.
- Never swap the first consonant or any letter that carries the word's silhouette.
  "hello" → "hell●!" reads; "welcome" with the w swapped does not.
- A swap is an event: the letter is present, then pops out as the shape springs in.

## 5. Line accents

- Thin ink strokes, 0.3 % of frame height, round caps: arrows, loops, squiggles, a
  circle drawn around a word, an underline.
- They draw on with a stroke reveal over 0.3–0.5 s, hold, then pop off by scaling to
  zero or retracting along their length.
- One accent per card, placed to point at or frame the line's meaning.

## 6. Badges

- A Circle of 26–34 % of frame height holding one cast shape at 55 % of its diameter,
  in a contrasting colour. Badge rows of five to six roll in from one side; badge
  clusters of four overlap on an ink stage.
- A badge may carry a number or a single short word instead of a shape.

## 7. Composition

- Centred by default. Generous empty stage: shapes and type occupy at most 60 % of the
  frame area.
- Layouts: single hero (one shape or word); stacked shapes above and below a line;
  badge row; badge cluster; constellation (6–10 small shapes joined by thin curved
  lines); number in shape; capsule (a Pill holding small shapes like a jar).
- Big shapes may bleed off the frame edge; type never does.

## 8. Forbidden

Gradients, textures, grain, outlines, drop shadows, 3D, photographic or illustrated
subjects, characters, faces, more than eight colours, paragraphs, small text under 4 %
of frame height, decorative motion with no state change.
