# Build Night — opening bumper (expressive geometry)

**Fit:**

| question | score | note |
|---|---|---|
| Whole piece as cards of ≤ 7 words or one number? | 2 | ten lines, longest four words |
| Register bright, welcoming, playful, celebratory? | 2 | warm, encouraging, a little cheeky |
| Every visual a flat named shape, badge, line accent or type? | 2 | no place, creature, face or texture needed |
| Static camera on a coloured stage enough? | 2 | holding-screen format |
| Audience reads rather than watches? | 2 | six short messages to a room |
| Legibility at thumbnail and on a stream overlay important? | 2 | projected in a room and streamed |
| **Sum** | **12** | proceed, no fit adjustments |

**Format:** 1280×720, 24 s, time-based, 120 BPM grid (beat = 0.5 s; every cut lands on a beat), Canvas 2D — one self-contained `index.html`, no libraries, no assets, system fonts only
**Defaults assumed:** none (duration, frame, grid and renderer were all given). House palette, house type stack, no brand substitutions.

Coordinates below are pixels in the 1280×720 frame with the percentage of frame width or height in parentheses. Sizes of shapes are the outer radius R unless a diameter is stated. Type sizes are the font size (em) as a percentage of frame height; cap height is taken as 0.72 em, x-height as 0.52 em. Card-local time is written `t+s`.

## The idea

A friendly voice counts a room of first-time builders into an all-nighter. It says hello to the night owls, welcomes them to Build Night, counts three-two-one on a ground shape that gets spikier with every beat, hands down the only rule with a wink ("Ship something small", the word "small" ringed by hand), asks the one question that matters, lets a night-sky constellation of shapes think for a moment, then pushes everyone out the door with an arrow and holds on the plain title. The feeling it leaves: you are expected, the bar is low on purpose, and it is time to start.

## The deck

**Copy deck** (every line the piece says, in order; each ≤ 7 words, sentence case, one idea)

1. "Hello, night owls!"
2. "Welcome to Build Night"
3. "3"
4. "2"
5. "1"
6. "Just one rule"
7. "Ship something small"
8. "What'll you make tonight?"
9. "Off you go!"
10. "Build Night"

Reading times (0.3 s + 0.25 s per word): 1 → 1.05 s · 2 → 1.30 s · 3, 4, 5 → 0.55 s each · 6 → 1.05 s · 7 → 1.05 s · 8 → 1.30 s · 9 → 1.05 s · 10 → 0.80 s.

**Palette** (house, eight roles)

| role | hex |
|---|---|
| stage blue | `#4A7BF7` |
| stage orange | `#F4603A` |
| stage yellow | `#F2BE4B` |
| stage green | `#6DBF9A` |
| cream | `#F4EEE4` |
| ink | `#1F2125` |
| blush | `#F5D8DA` |
| grey | `#9AA1A8` |

Stage colour per card: C1 blue · C2 orange · C3 green · C4 blush · C5 yellow · C6 blush · C7 cream · C8 ink · C9 blue · C10 cream. No two consecutive cards share a stage.

**Cast** (six shapes; no card uses any other)

- **Sunny** = hero shape (countdown ground for "3", bleeding shape on C2, the "o" swap on C4, C5, C7, hub of the constellation)
- **Burst** = hero morph target (countdown ground for "2", bleeding shape on C2 and C9)
- **VerySunny** = hero morph target (countdown ground for "1", badge inset)
- **Star4** = accent shape ("i"-dot swap on C1, C7, C10; constellation stars; badge inset)
- **Circle** = badge ground, the "o" swap on C1 (a yellow moon), constellation nodes
- **Semicircle** = greeting stage on C1, badge inset on C6
- Morph pair: Sunny ↔ Burst ↔ VerySunny (one family; the countdown ground morphs Sunny → Burst → VerySunny). Nothing morphs across families.

**Glyph-swap map** (at most two per line; never a first consonant or a silhouette letter)

| line | letter | shape | colour | note |
|---|---|---|---|---|
| "Hello, night owls!" | o in "Hello" | Circle | yellow | a moon for the night owls |
| "Hello, night owls!" | dot of i in "night" | Star4 | orange | stem stays as dotless ı |
| "Welcome to Build Night" | none | — | — | the title stays clean |
| "Just one rule" | o in "one" | Sunny | orange | the one rule shines; rotates 8°/s while held |
| "Ship something small" | o in "something" | Sunny | blue | rotates 8°/s while held |
| "What'll you make tonight?" | o in "you" | Sunny | orange | |
| "What'll you make tonight?" | dot of i in "tonight" | Star4 | blue | |
| "Off you go!" | none | — | — | the arrow is this card's event |
| "Build Night" | dot of i in "Build" | Star4 | orange | arrives swapped, resolves to the dot |
| "Build Night" | dot of i in "Night" | Star4 | blue | arrives swapped, resolves to the dot |

Swap geometry (in em of the card's font size): an "o" swap has R = 0.32 em, centred on the o's advance box at baseline − 0.26 em; an "i"-dot swap has R = 0.16 em, centred on the stem at baseline − 0.70 em, and the letter is drawn as dotless ı (U+0131). The swapped letter's slot widens by 0.16 em during the tracking breathe and stays widened while the shape is present.

**Rhythm**

- Holds: greeting 1.15 s · welcome 1.53 s · countdown 0.5 s per number · rule 1.10 s · punchline 1.30 s · badge row 0.5 s settled · question 1.80 s · constellation 0.66 s settled · send-off 1.10 s · closer 2.85 s (plain title for the last 1.15 s).
- Every cut lands on a beat (multiple of 0.5 s): 2.5 · 5.0 · 6.5 · 8.5 · 11.0 · 12.5 · 16.0 · 18.0 · 20.5 · 24.0.
- Tempo peak: the countdown, 5.0–6.5 s, one number per beat, cut into the rule on the fourth beat (3, 2, 1, go).
- Emotional peak: the question, 12.5–16.0 s, the longest word card, on cream.
- Release: the closer, 20.5–24.0 s, swaps resolve to plain letters and the title holds.
- Wordless cards: C6 (badge row) and C8 (constellation). Two of ten; the brief carries six messages in 24 s, so "every third card wordless" is met at the ratio the time allows (see self-check note).

## Timeline

| time (s) | card | stage | line | entrance | exit |
|---|---|---|---|---|---|
| 0.0–2.5 | C1 Greeting | blue | "Hello, night owls!" | Semicircle scale pop + glyph stagger-in, loop draw-on | exit shrink |
| 2.5–5.0 | C2 Welcome | orange | "Welcome to Build Night" | shapes scale pop, glyph stagger-in, word land | hard cut |
| 5.0–6.5 | C3 Countdown | green | "3" · "2" · "1" | ground scale pop + number slide | hard cut |
| 6.5–8.5 | C4 Announcement | blush | "Just one rule" | glyph stagger-in, underline draw-on | hard cut |
| 8.5–11.0 | C5 Announcement | yellow | "Ship something small" | word land, loop draw-on | hard cut |
| 11.0–12.5 | C6 Badge row | blush | — | badge roll-in from the left | hard cut |
| 12.5–16.0 | C7 Question | cream | "What'll you make tonight?" | word land on stepped lines, squiggle draw-on | exit shrink |
| 16.0–18.0 | C8 Constellation | ink | — | node scale pops, lines draw-on | hard cut |
| 18.0–20.5 | C9 Return | blue | "Off you go!" | shapes scale pop, word land | exit slide right |
| 20.5–24.0 | C10 Closer | cream | "Build Night" | glyph stagger-in with swaps in place | none — holds to the end |

## Card library (in timeline order)

### C1. Greeting — "Hello, night owls!"   t = 0.0–2.5 s
- Stage: blue `#4A7BF7`
- Composition: single hero on a Semicircle stage; the half-disc rises from the bottom edge and holds both lines of type inside its chord.
- Cast on card: Semicircle 62 % H (R 446 px) cream, flat edge down, centre (640, 720) = (50 %, 100 %), top of the arc at y = 274 (38 %) · Circle 3.9 % H (R 28 px) yellow as the "o" swap · Star4 1.9 % H (R 14 px) orange as the "i"-dot swap
- Type: statement 12 % H (86 px), ink, centred at x = 640, wrap "Hello, / night owls!", baselines y = 500 (69 %) and 600 (83 %). Chord widths inside the Semicircle at those baselines are 776 px and 859 px; the lines measure about 285 px and 525 px.
- Glyph swaps: o in "Hello" → Circle yellow, centre (o advance centre, 478) · dot of i in "night" → Star4 orange, centre (stem centre, 540); the i is drawn as ı
- Accent: ink lasso loop above "Hello,": a shallow arch from (500, 418) up to (640, 372) and down to (780, 418) with one 18 px-radius loop drawn clockwise at the apex; stroke 2.2 px (0.3 % H), round caps. Its lowest point sits 20 px above the caps of "Hello," (cap top y = 438).
- Entrance: Semicircle scale pop from its centre (expressive default spatial, 500 ms) at t+0.00 · glyph stagger-in of both lines concurrently, left to right, from t+0.10 (expressive fast spatial, 350 ms), stagger 40 ms; line 1 ends t+0.65, line 2 ends t+0.81 · accent draw-on t+0.60–1.00 (expressive fast effects 150 ms on opacity, reveal by length over 400 ms)
- Focal event: glyph swap pop. Tracking breathe t+1.10–1.25 (fast spatial 350 ms, slot widens 0.16 em), then o → Circle pops t+1.25–1.60 and i-dot → Star4 pops t+1.35–1.70 (fast spatial, 350 ms each; letter scales to 0 as the shape scales to 1)
- Exit: exit shrink (expressive fast spatial, 350 ms) t+2.15–2.50 — type, swap shapes, accent and the Semicircle all scale to zero at their own centres (the Semicircle sinks into the bottom edge)
- Hold: 1.15 s, t+1.00–2.15 (reading time 1.05 s)
- Don't: never let the Semicircle's arc top rise above y = 274 at rest (its overshoot peak may briefly reach y ≈ 230, before any type exists); never swap the H or the w.

### C2. Welcome — "Welcome to Build Night"   t = 2.5–5.0 s
- Stage: orange `#F4603A`
- Composition: stacked shapes bleeding top-left and bottom-right around a centred two-line statement.
- Cast on card: Sunny 30 % H (R 216 px) cream, centre (180, −30) = (14 %, −4 %), bleeding off the top-left; its AABB is x −36…396, y −246…186 · Burst 28 % H (R 202 px) cream, centre (1130, 750) = (88 %, 104 %), bleeding off the bottom-right; its AABB is x 928…1332, y 548…952
- Type: statement 12 % H (86 px), cream, centred at x = 640, wrap "Welcome to / Build Night", baselines y = 330 (46 %) and 430 (60 %). Line boxes: about x 402…878 (line 1) and x 380…900 (line 2); cap top of line 1 at y = 268, descender bottom of line 2 at y = 447. Both shapes clear the type by ≥ 80 px.
- Glyph swaps: none
- Accent: cream arrow, an S-curve from (1010, 250) to its tip at (925, 398) with an open chevron head 22 px long, pointing at the end of "Night"; stroke 2.2 px, round caps
- Entrance: Sunny and Burst scale pop (expressive slow spatial, 650 ms) at t+0.00 · "Welcome to" glyph stagger-in from t+0.10, left to right, 45 ms stagger (fast spatial 350 ms; 9 glyphs, ends t+0.81) · "Build Night" word land: each word drops 0.4 em from above into its position (expressive default spatial, 500 ms), "Build" t+0.35–0.85, "Night" t+0.47–0.97
- Focal event: accent draw-on, t+1.00–1.40 (fast effects 150 ms on opacity, reveal by length 400 ms); the arrow then holds
- Exit: hard cut at t+2.50 (the count-in slams in)
- Hold: 1.53 s, t+0.97–2.50 (reading time 1.30 s)
- Don't: never move the Burst's centre above y = 750 — its tips must stay below y = 548, under the descenders of "Build Night"; no swap on this card.

### C3. Countdown — "3" · "2" · "1"   t = 5.0–6.5 s
- Stage: green `#6DBF9A`
- Composition: number in shape; one cream hero ground centred at (640, 360) = (50 %, 50 %), the digit masked to the ground's outline.
- Cast on card: Sunny 25 % H (R 180 px) cream for "3" → morphs to Burst 28 % H (R 202 px) cream for "2" → morphs to VerySunny 32 % H (R 230 px) cream for "1"; all centred (640, 360)
- Type: hero 22 % H (158 px), ink, centred at x = 640, baseline y = 417 so the digit's cap box (114 px tall) is centred on y = 360. Digits are clipped to the ground shape (the mask is the current morphed outline).
- Glyph swaps: none
- Accent: none
- Entrance: ground scale pop as Sunny (expressive default spatial, 500 ms) t+0.00–0.50 · "3" number slide from y+180 (below centre) to rest (expressive fast spatial, 350 ms) t+0.00–0.35
- Focal event: shape morph + number slide on each beat. t+0.50: Sunny → Burst morph by resampling (expressive default spatial, 500 ms, R 180 → 202) while "3" slides up and out and "2" slides in from below (fast spatial, 350 ms, t+0.50–0.85). t+1.00: Burst → VerySunny (default spatial, 500 ms, R 202 → 230) while "2" exits upward and "1" enters (fast spatial, 350 ms, t+1.00–1.35).
- Exit: hard cut at t+1.50 into C4 (the fourth beat is "go")
- Hold: one number per beat, 0.5 s each; a digit is at hero size and inside the mask for the whole slot (at rest for the last 0.15 s of it). Card-level: a digit is legible from t+0.35 to t+1.50 = 1.15 s (the card's three numbers read in 1.05 s).
- Don't: never rotate the ground; never crossfade digits (they slide inside the mask); never use the slow spatial token here — 650 ms overruns the beat.

### C4. Announcement — "Just one rule"   t = 6.5–8.5 s
- Stage: blush `#F5D8DA`
- Composition: single centred statement, one swap, one underline; nothing else on the stage.
- Cast on card: Sunny 3.9 % H (R 28 px) orange as the "o" swap, rotating 8°/s clockwise while the card holds
- Type: statement 12 % H (86 px), ink, centred at x = 640, one line, baseline y = 390 (54 %); line box about x 332…948, cap top y = 328, descender bottom y = 407
- Glyph swaps: o in "one" → Sunny orange, centre (o advance centre, 368)
- Accent: ink underline beneath "rule", from (x of "rule" start, 404) to (x of "rule" end, 404); stroke 2.2 px, round caps; drawn left to right
- Entrance: glyph stagger-in from t+0.10, left to right, 40 ms stagger (fast spatial 350 ms; 11 glyphs, ends t+0.85) · underline draw-on t+0.60–0.90 (fast effects 150 ms on opacity, reveal by length 300 ms)
- Focal event: tracking breathe t+1.00–1.15 (fast spatial, slot widens 0.16 em) then glyph swap pop t+1.15–1.50 (fast spatial, 350 ms)
- Exit: hard cut at t+2.00 (the punchline slams in)
- Hold: 1.10 s, t+0.90–2.00 (reading time 1.05 s)
- Don't: never swap the J or the r; never add a second shape — the Sunny is the only one.

### C5. Announcement — "Ship something small"   t = 8.5–11.0 s
- Stage: yellow `#F2BE4B`
- Composition: single centred statement, one swap, a hand loop ringing the last word.
- Cast on card: Sunny 3.9 % H (R 28 px) blue as the "o" swap, rotating 8°/s clockwise while the card holds
- Type: statement 12 % H (86 px), ink, centred at x = 640, one line, baseline y = 390 (54 %); line box about x 150…1130 (measure it: the widest line in the piece, it must stay inside a 4 % margin, x ≥ 51 and x ≤ 1229), cap top y = 328, descender bottom y = 407
- Glyph swaps: o in "something" → Sunny blue, centre (o advance centre, 368)
- Accent: ink loop drawn around "small": an ellipse centred on the word's advance centre at (cx, 372), radii 138 × 62 px, drawn clockwise from its leftmost point over 400 ms and overshooting its start by 15°; stroke 2.2 px, round caps. The ellipse's top (y = 310) and bottom (y = 434) clear the caps and descenders; its left edge stays ≥ 20 px from the g of "something".
- Entrance: word land of three words 150 ms apart from t+0.00, each dropping 0.4 em from above (expressive default spatial, 500 ms): "Ship" t+0.00–0.50, "something" t+0.15–0.65, "small" t+0.30–0.80 · loop draw-on t+0.80–1.20 (fast effects 150 ms on opacity, reveal by length 400 ms)
- Focal event: tracking breathe t+1.30–1.45 then glyph swap pop t+1.45–1.80 (fast spatial, 350 ms)
- Exit: hard cut at t+2.50
- Hold: 1.30 s, t+1.20–2.50 (reading time 1.05 s)
- Don't: never shrink the word "small" — one size per card, the loop carries the joke; never let the loop cross a letter of "something".

### C6. Badge row — (no line)   t = 11.0–12.5 s
- Stage: blush `#F5D8DA`
- Composition: badge row; six Circle badges on the horizontal centre line, the sixth bleeding off the right edge.
- Cast on card (badges are Circles 26 % H = 187 px diameter, centres at y = 360 (50 %); inset shapes are 55 % of the badge diameter = 103 px across, R 51 px, centred in the badge):
  1. cream Circle at x = 160 (12.5 %) holding an orange Sunny
  2. ink Circle at x = 380 (30 %) holding a yellow Star4
  3. blue Circle at x = 600 (47 %) holding a cream Burst
  4. cream Circle at x = 820 (64 %) holding a green Semicircle, flat edge down, its bounding box centred in the badge
  5. orange Circle at x = 1040 (81 %) holding a cream VerySunny
  6. ink Circle at x = 1260 (98 %) holding a grey Circle; this badge spans x 1166…1353 and bleeds off the right edge
- Type: none
- Glyph swaps: none
- Accent: none
- Entrance: badge roll-in from the left: each badge starts 400 px left of its rest position rotated −15° and settles to rest at 0° (expressive default spatial, 500 ms), 100 ms stagger in order 1→6 (starts t+0.00 … t+0.50; last settles t+1.00); the inset rides with its badge
- Focal event: the roll-in settle (t+1.00); nothing moves after it
- Exit: hard cut at t+1.50
- Hold: 0.5 s settled, t+1.00–1.50 (wordless, no reading time)
- Don't: never rotate a badge after it settles; never bring badge 1 closer than 66 px to the left edge; this frame uses all eight colours — add nothing.

### C7. Question — "What'll you make tonight?"   t = 12.5–16.0 s
- Stage: cream `#F4EEE4`
- Composition: left-stepped three-line statement, each line indented 80 px further than the last; a squiggle under the last line. The block sits slightly left of centre; the generous right side is empty on purpose.
- Cast on card: Sunny 3.9 % H (R 28 px) orange as the "o" swap · Star4 1.9 % H (R 14 px) blue as the "i"-dot swap
- Type: statement 12 % H (86 px), ink, left-aligned per line, wrap "What'll / you make / tonight?": "What'll" starts x = 250 (19.5 %), baseline y = 280 (39 %); "you make" starts x = 330 (26 %), baseline y = 380 (53 %); "tonight?" starts x = 410 (32 %), baseline y = 480 (67 %). Line boxes about x 250…550, x 330…708, x 410…754.
- Glyph swaps: o in "you" → Sunny orange, centre (o advance centre, 358) · dot of i in "tonight" → Star4 blue, centre (stem centre, 420); the i is drawn as ı
- Accent: ink squiggle under "tonight?": a four-hump wave from (410, 496) to (754, 496), amplitude 8 px, stroke 2.2 px, round caps, drawn left to right
- Entrance: word land, four words 150 ms apart from t+0.00, each dropping 0.4 em from above (expressive default spatial, 500 ms): "What'll" t+0.00–0.50, "you" t+0.15–0.65, "make" t+0.30–0.80, "tonight?" t+0.45–0.95 · squiggle draw-on t+0.95–1.35 (fast effects 150 ms on opacity, reveal by length 400 ms)
- Focal event: tracking breathe t+1.50–1.65 (both swap slots), then o → Sunny pops t+1.65–2.00 and i-dot → Star4 pops t+1.75–2.10 (fast spatial, 350 ms each)
- Exit: exit shrink (fast spatial, 350 ms) t+3.15–3.50
- Hold: 1.80 s, t+1.35–3.15 (reading time 1.30 s)
- Don't: never centre the lines — the step is the layout; never swap the W; never add a shape that is not a swap.

### C8. Constellation — (no line)   t = 16.0–18.0 s
- Stage: ink `#1F2125` (the night sky)
- Composition: constellation; eight small shapes joined by thin cream curves in two arcs plus one link, spread across the middle 70 % of the frame.
- Cast on card (nodes):
  - n1 Circle 3 % H (R 22 px) cream at (230, 216) = (18 %, 30 %)
  - n2 Star4 5 % H (R 36 px) yellow at (410, 418) = (32 %, 58 %)
  - n3 Circle 4 % H (R 29 px) cream at (576, 187) = (45 %, 26 %)
  - n4 Sunny 7 % H (R 50 px) grey at (704, 360) = (55 %, 50 %), the hub
  - n5 Star4 4 % H (R 29 px) yellow at (870, 518) = (68 %, 72 %)
  - n6 Circle 5 % H (R 36 px) cream at (998, 245) = (78 %, 34 %)
  - n7 Star4 3 % H (R 22 px) yellow at (1100, 446) = (86 %, 62 %)
  - n8 Circle 4 % H (R 29 px) blue at (512, 562) = (40 %, 78 %)
- Lines: cream, 2.2 px (0.3 % H), round caps; each segment a quadratic curve whose control point is offset 30 px perpendicular to the chord, sides alternating along the arc. Arc A: n1 → n2 → n8 → n5 → n7. Arc B: n3 → n4 → n6. Link: n4 → n8. Seven segments; lines end at node edges, not centres.
- Type: none
- Glyph swaps: none
- Accent: none (the curves are layout, not an accent)
- Entrance: node scale pop (expressive default spatial, 500 ms), 120 ms stagger in order n1 → n8 (starts t+0.00 … t+0.84, last settles t+1.34) · lines draw-on along their length t+0.90–1.30 (fast effects 150 ms on opacity, reveal by length 400 ms, all seven together)
- Focal event: constellation drift: from t+1.35 every node moves along its own seeded vector of magnitude 8–11 px (1.1–1.5 % H) on expressive slow spatial (650 ms), lines following their nodes; the card cuts before the return leg. Seed 20260918.
- Exit: hard cut at t+2.00
- Hold: 0.66 s settled, t+1.34–2.00 (wordless)
- Don't: never draw ink strokes on the ink stage (lines are cream); no node larger than 7 % H; no continuous drift beyond the one 650 ms leg.

### C9. Return — "Off you go!"   t = 18.0–20.5 s
- Stage: blue `#4A7BF7`
- Composition: statement centred, shapes bleeding bottom-left and top-right, an arrow sweeping right toward the exit.
- Cast on card: Burst 28 % H (R 202 px) cream, centre (150, 760) = (12 %, 106 %), bleeding off the bottom-left; AABB x −52…352, y 558…962 · Sunny 24 % H (R 173 px) yellow, centre (1140, −20) = (89 %, −3 %), bleeding off the top-right; AABB x 967…1313, y −193…153
- Type: statement 12 % H (86 px), cream, centred at x = 640, one line, baseline y = 390 (54 %); line box about x 380…900, cap top y = 328, descender bottom y = 407. Both shapes clear the type by ≥ 150 px.
- Glyph swaps: none
- Accent: cream arrow beneath the line sweeping to the right: a quadratic curve from (520, 480) with control point (760, 560) to its tip at (1010, 470), open chevron head 24 px long; stroke 2.2 px, round caps
- Entrance: Burst and Sunny scale pop (expressive slow spatial, 650 ms) at t+0.00 · word land, three words 150 ms apart, each dropping 0.4 em from above (expressive default spatial, 500 ms): "Off" t+0.10–0.60, "you" t+0.25–0.75, "go!" t+0.40–0.90
- Focal event: accent draw-on t+1.00–1.40 (fast effects 150 ms on opacity, reveal by length 400 ms); the arrow then holds
- Exit: exit slide right (expressive default spatial, 500 ms) t+2.00–2.50: type, arrow, Burst and Sunny move together by +1400 px in x, off the right edge
- Hold: 1.10 s, t+0.90–2.00 (reading time 1.05 s)
- Don't: never swap the o in "go" — the arrow is this card's one event; never let the Sunny's rays reach below y = 153.

### C10. Closer — "Build Night"   t = 20.5–24.0 s
- Stage: cream `#F4EEE4`
- Composition: single hero, two stacked words centred; two swaps that arrive in place and resolve back to letters; nothing else.
- Cast on card: Star4 3.5 % H (R 25 px) orange as the "i"-dot swap in "Build" · Star4 3.5 % H (R 25 px) blue as the "i"-dot swap in "Night"
- Type: hero 22 % H (158 px), ink, centred at x = 640, wrap "Build / Night", baselines y = 330 (46 %) and 510 (71 %); line boxes about x 423…857 and x 411…869; cap top of line 1 y = 216, descender bottom of line 2 y = 542
- Glyph swaps: dot of i in "Build" → Star4 orange, centre (stem centre, 219) · dot of i in "Night" → Star4 blue, centre (stem centre, 399); both i's are drawn as ı while swapped
- Accent: none
- Entrance: glyph stagger-in, both lines concurrently, left to right, 50 ms stagger (fast spatial, 350 ms; 5 glyphs per line, done t+0.65); the two Star4s arrive already in place of the dots, popping in with their stem's glyph (the slot is not widened — an i-dot swap needs no breathe)
- Focal event: swaps resolve: at t+1.90 the orange Star4 scales to zero as the plain dot of "Build" appears (fast spatial, 350 ms, t+1.90–2.25); at t+2.00 the blue Star4 resolves the same way for "Night" (t+2.00–2.35). The plain title then holds.
- Exit: none — the plain title holds to t+3.50 (24.0 s) and the piece ends on it
- Hold: 2.85 s, t+0.65–3.50 (reading time 0.80 s); plain-title hold t+2.35–3.50 = 1.15 s
- Don't: never add a logo, a third shape or an accent; never crossfade a star into its dot — it is a scale swap.

## Composition rules for every card

- One stage colour per card, full bleed, flat, changed only by a hard cut on a beat.
- Centred by default. The type block's centre sits on x = 640 unless the card entry says left-stepped (C7 only).
- Type never bleeds: every line box stays inside a 4 % margin (x 51…1229, y 29…691). Big shapes may bleed; the bleed is set by the centre given in the entry, never by scaling.
- Occupancy: type plus shapes cover at most 60 % of the frame area on every still (C1, the densest card, sits near 35 %: the Semicircle stage alone covers 34 % of the frame).
- Text contrast: ink on cream, blush and yellow (C1's Semicircle, C4, C5, C7, C10); cream on blue, orange and green (C2, C3's ground is cream so its digit is ink, C9). Text never sits over a shape's interior except inside C1's Semicircle stage and C3's countdown ground (a number-in-shape).
- Swap shapes are stage colours that contrast with the type colour and differ from the card's stage colour. Accent strokes are the card's type colour (ink on light stages, cream on blue/orange; the constellation lines on ink are cream).
- z-order per card, back to front: stage → bleeding shapes → Semicircle stage → badges/nodes → lines → type → swap shapes → accent.
- One focal event per hold. Accents draw on as the tail of the entrance on swap cards (C1, C4, C5, C7); the accent is the focal event on C2 and C9; the morph is on C3; the roll-in settle on C6; the drift on C8; the resolve on C10.
- Two shapes may overlap; overlap is opaque. No shape touches a line of type: the AABBs in each entry give the clearance to verify.
- Exits finish before the cut; entrances finish before the hold begins. Hard cuts carry the contents out with the stage.

## Visual system

**Palette** — the eight house colours only: stage blue `#4A7BF7`, stage orange `#F4603A`, stage yellow `#F2BE4B`, stage green `#6DBF9A`, cream `#F4EEE4`, ink `#1F2125`, blush `#F5D8DA`, grey `#9AA1A8`. Grey appears only on the ink stage (C6 badge 6 inset, C8 hub). No tints, no transparency, no gradients.

**Shape recipes used** (filled polygons from a circle of radius R, N = 128 points, no outlines):

| shape | recipe |
|---|---|
| Circle | plain |
| Semicircle | half disc; flat edge down (C1 stage) or as an inset with flat edge down (C6 badge 4); the polygon is the 64-point arc plus the flat edge |
| Star4 | 4 points, inner radius 0.42 R, sharp tips; drawn with points at 0°, 90°, 180°, 270° |
| Sunny | 8 rays, inner radius 0.72 R, rounded tips (corner radius 0.06 R) |
| Burst | 12 spikes, inner radius 0.62 R, sharp |
| VerySunny | 16 rays, inner radius 0.78 R, sharp |

Sizes are given in every card entry as % of frame height (R). Morphs happen only inside the Sunny ↔ Burst ↔ VerySunny family (C3), by resampling both outlines to 128 points starting at angle 0 and interpolating point-wise.

**Type**

- Face: `"Google Sans", "Product Sans", "Avenir Next", "Helvetica Neue", Arial, sans-serif`, weight 600 (semibold). No asset is loaded; whichever system face resolves first is used, and the appendix says how to measure it.
- Sentence case. One size per card from the three-step scale: hero 22 % H = 158 px (C3 digits, C10), statement 12 % H = 86 px (C1, C2, C4, C5, C7, C9). The sentence step (8 % H = 58 px) is not used because no line exceeds four words. Nothing smaller than 4 % H appears anywhere.
- Line pitch 1.15 em for two-line statements (100 px at 86 px), 1.14 em for the hero pair (180 px at 158 px).
- Tracking breathes: glyphs arrive from +0.2 em letter-spacing and settle to 0; before a swap the swapped letter's slot widens by 0.16 em (neighbours shift ±0.08 em) and stays widened while the shape is present.
- Wrap by meaning only: "Hello, / night owls!", "Welcome to / Build Night", "What'll / you make / tonight?", "Build / Night".
- Centred, except C7 which is left-stepped 80 px per line.

**Line accents**

- Stroke 2.2 px (0.3 % H), round caps and joins, colour = the card's type colour. One per card (C1 loop, C2 arrow, C4 underline, C5 ellipse loop, C7 squiggle, C9 arrow). Arrowheads are open chevrons, 22–24 px long, 50° between the arms.
- Draw-on = a prefix of the path by arc length over 300–400 ms with opacity on the fast effects token; then hold; then leave with the card's exit (shrink, slide, or hard cut).

**Badges** (C6 only)

- Circle 26 % H (187 px diameter) holding one cast shape at 55 % of the diameter in a contrasting colour, or nothing else; a row of six, centres 220 px apart, last one bleeding off the right edge.

**No texture** — no gradients, grain, outlines, shadows, blur or transparency anywhere; every pixel is one of the eight colours (anti-aliased edges excepted).

## Motion vocabulary

Every spatial move uses one of these tokens; colour and opacity use only the effects tokens and never overshoot. The builder implements the tokens as cubic-bezier curves (see Architecture); the y-values above 1.0 are the overshoot and must be kept.

| token | curve | duration |
|---|---|---|
| expressive fast spatial | cubic-bezier(0.42, 1.67, 0.21, 0.90) | 350 ms |
| expressive default spatial | cubic-bezier(0.38, 1.21, 0.22, 1.00) | 500 ms |
| expressive slow spatial | cubic-bezier(0.39, 1.29, 0.35, 0.98) | 650 ms |
| expressive fast effects | cubic-bezier(0.31, 0.94, 0.34, 1.00) | 150 ms |
| expressive default effects | cubic-bezier(0.34, 0.80, 0.34, 1.00) | 200 ms |

Moves used in this piece:

| move | what happens | token · duration | where |
|---|---|---|---|
| Glyph stagger-in | each glyph springs from 0.8 scale and +0.2 em tracking to 1.0 / 0, opacity 0→1 on fast effects (150 ms) at the same start | fast spatial · 350 ms, stagger 40–50 ms | C1, C2 line 1, C4, C10 |
| Word land | a whole word drops 0.4 em from above into its position, opacity 0→1 on fast effects | default spatial · 500 ms, stagger 120–150 ms | C2 line 2, C5, C7, C9 |
| Tracking breathe | the swapped letter's slot widens by 0.16 em (neighbours shift ±0.08 em) | fast spatial · 350 ms (its first 150 ms precede the pop) | C1, C4, C5, C7 |
| Glyph swap pop | letter scales 1→0 at its centre while the shape scales 0→1 at the swap centre | fast spatial · 350 ms | C1, C4, C5, C7 |
| Swap resolve | the reverse: shape 1→0 while the letter (or dot) 0→1 | fast spatial · 350 ms | C10 |
| Shape morph | resampled outline interpolates Sunny → Burst → VerySunny with R growing | default spatial · 500 ms (fits the 0.5 s beat; the slow token would overrun it) | C3 |
| Number slide | the digit moves vertically inside the ground mask; the next enters from below as the last leaves upward | fast spatial · 350 ms | C3 |
| Scale pop | a shape appears from 0 to 1 with overshoot at its own centre | default spatial · 500 ms (small/medium shapes), slow spatial · 650 ms (bleeding hero shapes on C2, C9) | C1, C2, C3, C8, C9 |
| Badge roll-in | badges enter from 400 px left with −15° rotation and settle | default spatial · 500 ms, stagger 100 ms | C6 |
| Hero rotate | the swapped Sunny turns 8°/s clockwise during the hold | linear | C4, C5, C7 |
| Accent draw-on | prefix-by-length reveal over 300–400 ms, opacity 0→1 on fast effects (150 ms) at the start | fast effects + linear reveal | C1, C2, C4, C5, C7, C9 |
| Constellation drift | nodes move 8–11 px along seeded vectors, lines follow | slow spatial · 650 ms, one leg | C8 |
| Exit shrink | all contents scale to 0 at their own centres | fast spatial · 350 ms | C1, C7 |
| Exit slide | all contents move +1400 px in x together | default spatial · 500 ms | C9 |
| Hard cut | stage and contents change instantly on the beat | none | every card boundary |

Rules: staggers are glyphs 40–50 ms, words 120–150 ms, badges 100 ms, nodes 120 ms. Loops: none. Reduced motion (`?rm=1`): every move snaps to its end state at its start time, so each card shows its hold composition for the card's whole duration; stage cuts and the countdown's number changes stay on the beat. This note applies once to every move above.

## Architecture

- **Pure time function.** `render(t)` draws the frame for absolute time `t` seconds from a blank canvas: clear to the card's stage colour, then draw the card's contents as a function of local time `t − start`. No state carries between frames; seeking to any `t` gives the same pixels.
- **Card scheduler.** A table of `{id, start, end, stage, draw(local)}` in timeline order; `render` picks the card with `start ≤ t < end`. At t = 24.0 the last card's final state is held.
- **Curves, not springs.** Each token is a cubic-bezier solved numerically (Newton or bisection on the x-parameter, 1e-4 tolerance). A move is `value = from + (to − from) × curve(clamp((local − t0) / duration, 0, 1))`; overshoot comes from the curve's y > 1. This choice is stated here because it is deterministic and seekable; a fixed-step spring integrator would also be allowed but was not chosen.
- **Shape generators.** `shape(name, R)` returns 128 points `[x, y]` for Circle, Semicircle, Star4, Sunny, Burst, VerySunny per the recipes; rounded tips are made by replacing each tip vertex with a short arc of corner radius 0.06 R. Draw with `beginPath / lineTo / closePath / fill` only; no `stroke` on shapes.
- **Morph by resampling.** `morph(a, b, k)` lerps two 128-point outlines point-wise (both start at angle 0, both wind the same way); `k` is the curve value and may exceed 1.0. R interpolates alongside.
- **Type engine.** One `ctx.font` per card; each line is laid out glyph by glyph with `measureText` for advances so every glyph has a known box for stagger, breathe and swap placement. A swapped "o" is skipped in drawing and its shape drawn at the box's centre; a swapped "i" is drawn as ı and its Star4 placed on the stem's centre.
- **Accents.** Paths are sampled to polylines (≥ 64 segments); draw-on strokes the prefix of the polyline whose cumulative length ≤ reveal × total length.
- **Seeded randomness** (mulberry32, seed 20260918) is used only for the eight constellation drift vectors on C8. Nothing else is random.
- **Masking.** C3's digit is drawn inside `ctx.clip()` of the current morphed ground polygon.
- **Rendering.** A 1280×720 canvas scaled by `devicePixelRatio`; the frame is redrawn on `requestAnimationFrame` with `t` from a play clock, or once for `?t=`.

## Process

Build in stages; stop at each stop point and inspect the named stills before continuing.

1. **Stage and scheduler.** Canvas, card table, hard cuts, `?t=` parameter. Stop: stills at t = 0.0, 2.5, 5.0, 6.5, 8.5, 11.0, 12.5, 16.0, 18.0, 20.5 each show only the new card's stage colour; a still at each boundary minus one frame (1/60 s) shows the previous stage.
2. **Type, static.** Every line at its final size, position and wrap, no motion. Stop: mid-hold stills for every word card (t = 1.6, 4.0, 5.4, 7.5, 9.8, 14.5, 19.2, 23.0); measure cap heights (114 px hero, 62 px statement, ±2 px) and check every line box is inside the 4 % margin.
3. **Shapes, static.** Cast generators; every shape at its rest position and size. Stop: the same stills; check each shape's AABB against the numbers in its card entry and against the type boxes (no intersection except C1's Semicircle stage and C3's ground). Check tips are rounded on Sunny and sharp on Burst, VerySunny, Star4.
4. **Entrances and exits.** Curves, stagger, scale pops, word lands, hard cuts. Stop: log the peak scale of one glyph, one shape pop and one word land — each must exceed 1.0 (overshoot present); confirm every entrance ends before the hold start given in the card entry and every exit ends at the cut.
5. **Swaps and accents.** Breathe, pop, resolve, draw-on. Stop: stills at t = 1.75 (C1 both swaps done), 8.05 (C4), 10.35 (C5), 14.65 (C7), 22.9 (C10 resolved) and at each accent's draw-on end; the swapped word must still read as the word.
6. **Countdown.** Morph, mask, number slides. Stop: stills at t = 5.35, 5.85, 6.35 (digit at rest on Sunny, Burst, VerySunny) and 5.6 (mid-morph, mid-slide); the digit must be fully inside the ground at rest.
7. **Wordless cards.** Badge roll-in, constellation pops, lines, drift. Stop: stills at t = 12.1 and 17.4; count colours on the C6 still (exactly eight).
8. **Verification.** Run the checklist below in full; produce the thumbnail sheet and the colour census. Fix, re-run, then stop.

## Verification checklist

Each check is answered by a measurement or a named still. All must pass.

1. **Cut timing.** For every boundary b in {2.5, 5.0, 6.5, 8.5, 11.0, 12.5, 16.0, 18.0, 20.5}: the still at `?t=b` shows the new stage colour at pixel (8, 8), and the still at `?t=b−0.0167` shows the previous one. Ten stage colours match the timeline table.
2. **Type scale.** On the mid-hold stills (t = 1.6, 4.0, 5.4, 7.5, 9.8, 14.5, 19.2, 23.0) the cap height of the line is 62 ± 2 px for statement cards and 114 ± 2 px for C3 and C10; one size per card.
3. **No bleed, no overlap.** For every word card, the measured line boxes lie inside x 51…1229, y 29…691, and no line box intersects any non-stage shape's AABB except the C1 Semicircle and the C3 ground.
4. **Hold ≥ reading time.** From the scheduler's move table, compute per card: hold = (exit start or cut) − (entrance end). Assert C1 ≥ 1.05, C2 ≥ 1.30, C3 ≥ 1.05 (card-level), C4 ≥ 1.05, C5 ≥ 1.05, C7 ≥ 1.30, C9 ≥ 1.05, C10 ≥ 0.80. Print the table.
5. **Overshoot present.** Log the maximum of the curve value for one glyph stagger-in, one scale pop, one word land and one morph; each maximum must be > 1.0 (fast spatial peaks near 1.12, default near 1.05).
6. **Colour census.** For stills every 0.25 s (97 frames), count distinct colours after excluding pixels whose colour is not one of the eight (anti-aliasing); every remaining pixel must be one of the eight hexes and no frame may contain more than eight. The C6 still (t = 12.1) contains exactly eight.
7. **Thumbnail legibility, every card.** Render the mid-hold still of each of the ten cards (t = 1.6, 4.0, 5.4, 7.5, 9.8, 12.1, 14.5, 17.4, 19.2, 23.0) scaled to 160 × 90 px with the browser's default downsampling and tile them on one sheet. On each tile: the stage colour is identifiable, the line's word silhouettes are distinguishable from one another (for word cards), the swap shape or hero shape is a recognisable blob ≥ 3 px, and no card looks like another card's tile.
8. **Swapped words still read.** On the full-size stills at t = 1.75, 8.05, 10.35, 14.65 and 21.5, read the swapped words aloud: "Hello,", "night", "one", "something", "you", "tonight?", "Build", "Night". Each still keeps every non-swapped letter in place; the shape sits inside the widened slot at the stated centre ± 3 px.
9. **Countdown mask.** At t = 5.35, 5.85 and 6.35 the digit's ink bounding box lies entirely inside the ground shape's polygon; at t = 5.6 the departing and arriving digits are both clipped at the ground's outline (no ink outside it).
10. **Occupancy.** On every mid-hold still, non-stage pixels ≤ 60 % of the frame.
11. **Entrances/exits end on time.** For every card the last entrance move's end ≤ the hold start in its entry, and every exit's end == the card's end time (±1 frame).
12. **Reduced motion.** With `?rm=1&t=` at each card's hold start, the still is pixel-identical to the normal `?t=` still at the same time (diff = 0), and the countdown digits still change at 5.5 and 6.0.
13. **Determinism.** Two runs of `?t=17.4` (C8 drift active) produce identical pixels.

## Don'ts

- No gradients, textures, grain, outlines, drop shadows, blur, transparency or 3D anywhere.
- No camera moves; no crossfade between cards — every boundary is a hard cut on a beat.
- No ninth colour; no tint of a palette colour; grey only on the ink stage.
- No shape outside the cast of six (Sunny, Burst, VerySunny, Star4, Circle, Semicircle).
- No morph across families; nothing morphs except C3's ground.
- No continuous decorative motion: nothing rotates except the swapped Sunny on C4, C5, C7 while held; nothing drifts except C8's one leg.
- No springs or overshoot on colour or opacity.
- No text smaller than 4 % H, no second type size on a card, no wrap mid-phrase, no paragraphs.
- No text over a shape's interior except C1's Semicircle stage and C3's ground.
- No swap on a first consonant or a silhouette letter; never more than two swaps on a line.
- Never shrink "small" on C5; never add a logo or mark to C10; never swap the o in "go" on C9.
- Never move a card's cut off the 0.5 s beat grid.

## Renderer appendix: Canvas 2D

- **File.** One `index.html`, inline `<style>` and `<script>`, no `fetch`, no fonts, no images. A 1280×720 `<canvas>` sized by `devicePixelRatio`, letterboxed to the window.
- **Fonts.** `ctx.font = "600 86px 'Google Sans', 'Product Sans', 'Avenir Next', 'Helvetica Neue', Arial, sans-serif"` (158px for hero cards). Because the resolved face varies by system, all horizontal positions of glyphs come from `measureText(glyph).width` at run time; the line boxes in the card entries are estimates to verify against, not constants to hard-code. `ctx.textBaseline = "alphabetic"`; vertical positions use the baselines given.
- **Glyph layout.** Lay out each line glyph by glyph: x advances from `measureText`, plus the current letter-spacing (tracking breathe / arrival offset), plus the 0.16 em slot widening on a swapped glyph. Draw each glyph with its own scale and opacity about its box centre. A swapped o is skipped; a swapped i is drawn as "ı" (if the face lacks U+0131, draw the "i" with a clip rect from the baseline up to 0.55 em to remove the dot).
- **Shapes.** `shape(name, R)` per Architecture; draw with `fill()` only. Rounded tips on Sunny via short arcs of radius 0.06 R at each tip vertex.
- **Morph.** `morph(a, b, k)` point-wise on 128 points; `k` from the default spatial curve; R interpolated the same way. C3 draws `morph(shape("sunny",180), shape("burst",202), k)` and then `morph(shape("burst",202), shape("verysunny",230), k)`.
- **Curves.** `bezier(x1,y1,x2,y2)` returning `f(u)` via Newton iteration on x; the five tokens from Motion vocabulary. Deterministic; `?t=` seeks exactly.
- **Accents.** Each accent is a function returning a polyline in frame px; draw-on strokes the prefix by cumulative length; `lineWidth 2.2`, `lineCap "round"`, `lineJoin "round"`. Arrowheads are two extra polyline segments drawn at the end of the reveal.
- **Mask.** C3: `ctx.save(); path(groundPolygon); ctx.clip(); drawDigits(); ctx.restore()`.
- **Scheduler.** `CARDS = [{id:"C1", start:0, end:2.5, stage:"#4A7BF7", draw}, …]`; `render(t)` finds the card, fills the stage, calls `draw(t − start)`. All content is a pure function of local time.
- **Seeded randomness.** mulberry32(20260918) called exactly eight times for C8's drift angles; nothing else consumes it.
- **Controls.** Space = play/pause; a scrubber under the canvas with a tick at every card start; ← → step one frame (1/60 s), Shift+← → step 0.25 s; `R` records the full 24 s via `canvas.captureStream(60)` + `MediaRecorder` to a WebM download.
- **URL parameters.** `?t=<s>` renders one frame and stops; `?w=160` renders that frame scaled to 160 × 90 for the thumbnail check; `?rm=1` selects reduced motion; `?census=1` logs the distinct palette colours in the current frame to the console (used by checks 6 and 7).
- **Verification.** Headless Chrome screenshots at `?t=` for every still named in the checklist; the thumbnail sheet is assembled from `?w=160` captures; the colour census runs from `?census=1` on 97 frames.

## Self-check

| bar item | PASS/FAIL | evidence |
|---|---|---|
| Copy deck exists before the first card; every card's line is in it verbatim | PASS | The deck lists ten lines; C1…C10 quote lines 1, 2, 3–5, 6, 7, 8, 9, 10 verbatim; C6 and C8 carry no line |
| Every card entry names type, stage colour, cast members with sizes as % of frame height, glyph swaps, accent (or "none"), entrance, exit, hold | PASS | ten entries, each with the eleven fixed fields; sizes given as % H with R in px (e.g. C2 Sunny 30 % H R 216) |
| Every move carries a token from motion-vocabulary §1 or its curve, and a duration | PASS | Motion vocabulary table lists 15 moves with token and ms; every card entry names token and ms per move |
| Every card's hold ≥ reading time (0.3 s + 0.25 s per word) | PASS | C1 1.15 ≥ 1.05 · C2 1.53 ≥ 1.30 · C4 1.10 ≥ 1.05 · C5 1.30 ≥ 1.05 · C7 1.80 ≥ 1.30 · C9 1.10 ≥ 1.05 · C10 2.85 ≥ 0.80 · C3 card-level 1.15 ≥ 1.05 for its three numbers; each number's own slot is the 0.5 s card-grammar allows (0.55 s per lone number would not fit a beat) |
| Cast is 4–6 shapes; no card introduces a shape outside it | PASS | six shapes named in The deck; every "Cast on card" line uses only Sunny, Burst, VerySunny, Star4, Circle, Semicircle |
| No card has more than two swaps; swapped words remain readable | PASS | C1 two, C4 one, C5 one, C7 two, C10 two, others none; no first consonant or silhouette letter is swapped (glyph-swap map) |
| Text contrast rule | PASS | ink on cream (C1 Semicircle, C7, C10), blush (C4), yellow (C5); cream on blue (C9), orange (C2); ink digit on cream ground (C3); text over a shape only inside the C1 Semicircle stage and the C3 number-in-shape |
| Section 10 has ≥ 6 measurable checks incl. a 160 px thumbnail check for every card | PASS | 13 checks; check 7 renders all ten cards at 160 × 90 on one sheet |
| Must not: gradients, textures, outlines, shadows, 3D | PASS | Visual system "No texture"; Don'ts line 1 |
| Must not: camera moves, crossfades between cards | PASS | every boundary is a hard cut on a beat (Timeline); Don'ts line 2 |
| Must not: more than eight colours | PASS | palette of eight; C6 is the densest at exactly eight; check 6 enforces it per frame |
| Must not: paragraphs | PASS | longest line is four words |
| Must not: decorative shapes animating continuously without a state change | PASS | only the swapped Sunny rotates while it is the card's hero; C8 drifts one 650 ms leg; nothing idles |
| Must not: springs on colour or opacity | PASS | opacity uses fast effects (150 ms) only; colour changes are hard switches |

Builder read-through of three entries picked at random (C9, C3, C6): C9 could be drawn but the arrow's head length was missing — added "open chevron head 24 px long". C3 needed the digit's baseline to centre the cap box — added "baseline y = 417". C6 needed the inset Semicircle's placement — added "flat edge down, bounding box centred in the badge". Re-audited after the additions: all items PASS.

Note on card-grammar guidance (not a bar item): "every third card wordless" gives two wordless cards in ten here (C6, C8); with six messages plus a count-in in 24 s, a third wordless card would push a word card's hold under its reading time. The Question card uses the statement size (four words) rather than the sentence size because the line was written to four words on purpose.
