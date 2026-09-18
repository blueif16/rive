---
name: style-expressive-geometry
description: >-
  Turn short copy, a brief or a story into a complete PRODUCTION SPEC for a short
  animation in the EXPRESSIVE GEOMETRY style: full-bleed flat colour cards, a small
  library of named geometric shapes (sunny, burst, clover, cookie, 4-point star,
  semicircle, pill) that morph and spring, kinetic sentence-case type where single
  glyphs are swapped for shapes, thin hand-drawn arrow and squiggle accents, hard cuts
  between cards, a static camera. The language of Google's Material 3 Expressive event
  packages. The output is the detailed prompt a build agent executes; this skill never
  builds. Second of a family of art-style skills a router picks by topic. ROUTE HERE
  when the content is copy-first: event and broadcast packaging (openers, countdowns,
  breaks, "back soon", end cards, stream bumpers); product, feature and platform
  launches; developer, design and community conferences, hackathons, meetups;
  onboarding, welcome, celebration and milestone moments; greetings, questions,
  slogans, single statistics, dates; brand idents and logo stings for tech, education,
  productivity and creative tools; kinetic typography for lyrics, quotes and social
  captions; loops and stickers. Expressions it carries: joy, welcome, anticipation,
  progress, playfulness, clarity, momentum before a reveal. ROUTE ELSEWHERE when the
  content needs a place or a creature in a scene, characters with faces or a story arc
  longer than a card, texture or nostalgia or anything printed (use style-risograph),
  gravity (grief, danger, luxury, finance, health, legal), dense information, realism or
  dark moody lighting. Triggers: "expressive", "Material 3", "shape morph", "kinetic
  type", "event package", "countdown", "bumper", "sting", "badge", "geometric shapes",
  "Google style", or any request for a bright flat-shape typographic animation.
---

# Expressive geometry — copy to production spec

You produce the **production spec**, not the animation. A build agent reads your spec and
makes every pixel from it. In this style the words are the subject, the frame is the
stage, and a handful of named shapes are the cast. Read
`references/language-rules.md` first: the shapes, the palette, the type rules and the
glyph-swap rules are fixed vocabulary, not suggestions.

## Inputs

- **copy or story**: the lines to say, or a brief to turn into lines. Required.
- **duration** in seconds, **frame** (default 1280×720), **beat grid** (default 120 BPM,
  0.25 s and 0.5 s units), **renderer** (Canvas 2D | Rive | AE | unspecified).
- Optional: a brand palette to substitute for the house palette, a typeface, a logo
  described in words, a closing line.

If duration or frame is missing, state the default you chose in the spec header. If
there is neither copy nor a brief, HALT and ask. Never invent the message.

## Step 0 — fit check (also used by the router)

Score 0–2 per row, sum, print the table at the top of the spec.

| question | 2 | 0 |
|---|---|---|
| Can the whole piece be told as a sequence of cards each carrying ≤ 7 words or one number? | yes | needs paragraphs or a scene |
| Is the register bright, welcoming, playful or celebratory? | yes | grave, gritty, luxurious |
| Can every visual be a flat named shape, a badge, a line accent or type? | yes | needs a place, creature, face, texture |
| Is a static camera on a coloured stage enough? | yes | needs camera travel through a world |
| Does the audience need to read rather than watch? | read | watch a story |
| Is legibility at thumbnail size and on a stream overlay important? | yes | irrelevant |

Sum ≥ 8: proceed. 5–7: proceed and write a "Fit adjustments" paragraph naming what you
changed. ≤ 4: stop and emit `STYLE_MISMATCH` with the failing rows and the traits a
better style needs. Do not force it.

## Step 1 — copy deck, palette, cast, before any card

Write these at the top of the spec, in this order:

1. **Copy deck**: every line the piece says, in order, each ≤ 7 words, sentence case,
   one idea per line. Numbers and single words are lines too. Cut anything that cannot
   be read in the card's hold time.
2. **Palette**: the eight house colours from language-rules §2, or the brand's
   substitutes mapped onto the same eight roles (stage colours ×4, cream, ink, blush,
   grey). Every card names its stage colour.
3. **Cast**: 4–6 shapes from the library, named, with their roles (hero shape, badge
   shape, accent shape, morph pair). The same cast appears across the whole piece.
4. **Glyph-swap map**: which letters in which lines become which shapes, in which
   colour. At most two swaps per line, never on a consonant that carries the word's
   silhouette.
5. **Rhythm**: hold time per card, where the cuts land on the grid, where the tempo
   rises (countdown, montage) and where it rests (question, closer).

## Step 2 — enumerate, then write everything in full

First list every card the duration needs at the stated hold times, then write each
card in the fixed entry shape from `references/spec-template.md`. Pick card types from
`references/card-grammar.md` and moves from `references/motion-vocabulary.md`.

A **minimal** spec lists lines and says "animate in" — that FAILS. A **good** spec
gives every card its type, its stage colour, its exact composition, its cast members
with sizes, its glyph swaps, its line accent, its entrance and exit moves with spring
tokens, and its hold.

## Output shape

One Markdown document with exactly these sections, in this order:

1. Header: title, fit table, duration, frame, beat grid, renderer, defaults assumed
2. The idea (one paragraph) and the deck: copy deck, palette, cast, glyph-swap map
3. Timeline table: time range · card id · stage colour · line · entrance · exit
4. Card library: one entry per card in the fixed entry shape
5. Composition rules for every card
6. Visual system: palette with hex, shape recipes used, type (face, weight, size scale,
   tracking), line-accent rules, badge rules, no-texture rule
7. Motion vocabulary: each move used, with its spring token or curve and duration
8. Architecture: pure time function, seeded randomness for scatter only, shape
   generators, morph by resampling, spring integration or curve table, card scheduler
9. Process: staged build with stop points and what to inspect at each
10. Verification checklist: measurable checks the builder must run
11. Don'ts
12. Renderer appendix (only for the named renderer; see `references/renderer-notes.md`)

## The bar

Required. If any Required item fails, revise before returning.

- The copy deck exists before the first card, and every card's line is in it verbatim.
- Every card entry names its type, stage colour, cast members with sizes as % of frame
  height, glyph swaps, line accent (or "none"), entrance move, exit move, and hold.
- Every move carries a spring token from motion-vocabulary §1 or its curve equivalent,
  and a duration.
- Every card's hold time is ≥ the reading time of its line (0.3 s + 0.25 s per word).
- The cast is 4–6 shapes and no card introduces a shape outside it.
- No card has more than two glyph swaps, and swapped words remain readable as words.
- Text contrast: ink on cream or stage colours, cream on stage colours or ink; never
  text over another shape's interior except inside a badge or a semicircle stage.
- Section 10 has at least six checks answerable by a measurement or a still, including
  a thumbnail legibility check at 160 px wide for every card.

Must not: gradients, textures, outlines, drop shadows, 3D, camera moves, crossfades
between cards, more than eight colours, paragraphs, decorative shapes that animate
continuously without a state change, springs on colour or opacity.

## Self-check (mandatory, printed at the end of the spec)

Audit against every Required line above. Print a table: item · PASS/FAIL · one line of
evidence (a card id, a count, a section name). Revise every FAIL and re-audit. Then read
three random card entries as the builder would: if any cannot be drawn without asking a
question, add the missing number.

## Scope fence

Do NOT write code, RML or After Effects setups. Do NOT render. Do NOT choose a renderer
the inputs did not name; if unspecified, write the appendix for Canvas 2D and say so.
If the fit check fails, emit `STYLE_MISMATCH` rather than a weak spec.
