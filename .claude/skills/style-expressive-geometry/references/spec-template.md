# Spec template and canonical exemplar

## Skeleton

```
# <Title>

**Fit:** <table from Step 0, with the sum>
**Format:** <W×H>, <duration> s, time-based, <BPM> grid, <renderer>
**Defaults assumed:** <list, or "none">

## The idea
<one paragraph: what the piece says and the feeling it leaves>

## The deck
- Copy deck: 1. "<line>" 2. "<line>" … (numbers count as lines)
- Palette: <role: hex> ×8 (house or brand-mapped)
- Cast: <Shape> = hero · <Shape> = badge · <Shape> = accent · <Shape ↔ Shape> = morph pair …
- Glyph-swap map: "<word>" <letter> → <Shape> in <colour>; …
- Rhythm: holds, tempo peak, emotional peak, closer

## Timeline
| time (s) | card | stage | line | entrance | exit |
|---|---|---|---|---|---|

## Card library (in timeline order)
### <id>. <type> — "<line>"   t = <start–end>
- Stage: <colour hex>
- Composition: <layout name>; <positions as % of frame width/height>
- Cast on card: <Shape> <size % of frame height> <colour> at <x,y>; …
- Type: <scale step>, <colour>, <alignment>, wrap "<line / break>"
- Glyph swaps: <letter> → <Shape> <colour>, or none
- Accent: <kind> from <x,y> to <x,y>, or none
- Entrance: <move> (<token>, <ms>), stagger <ms>
- Focal event: <one of swap | morph | accent | rotate | drift>, at t+<s>
- Exit: <move> (<token>, <ms>)
- Hold: <s>  (reading time <s>)
- Don't: <card-specific trap>

## Composition rules for every card
## Visual system
## Motion vocabulary
## Architecture
## Process
## Verification checklist
## Don'ts
## Renderer appendix: <renderer>
## Self-check
| bar item | PASS/FAIL | evidence |
```

## Canonical exemplar: a Google event holding-screen package (transcribed, 31 s, 1280×720)

The deck. "hello!" · "welcome to" · 10 · 9 · 8 · "Grab a snack, we'll be back soon" ·
"How will today change tomorrow?" · "We'll be back soon" · "See you soon!" · "beautiful".
Cast: Sunny, VerySunny, Burst, Clover8, Star4, Semicircle, plus Circle badges. Stages
cycle blue → orange → blush → green → ink → cream → yellow.

| time | card | stage | line | focal event |
|---|---|---|---|---|
| 0.0–1.5 | Greeting | blue, cream Semicircle stage | "hello!" | the o pops out as a green Sunny; a loop accent above |
| 1.5–3.5 | Welcome | orange, cream Sunny bleeding top and bottom | "welcome to" | letters stagger in with breathing tracking; "to" lands late; arrow accent |
| 3.5–7.0 | Countdown | blush → green → ink | 10, 9, 8 | the ground morphs Burst → Semicircle → plain; numbers slide vertically; hand-drawn arrows |
| 7.0–9.0 | Announcement | blush, orange Burst behind "a" | "Grab a snack, we'll be back soon" | words breathe apart around the burst |
| 9.0–11.0 | Badge cluster | blue | none | ink Circle, blush Circle and Sunny badge overlap and settle |
| 11.0–13.0 | Badge row | blush | none | six badges roll in: blue Star4, orange Clover8, cream VerySunny-lines, ink Sunny, cream Boom |
| 13.0–17.0 | Question | cream then blue | "How will today change tomorrow?" | words land stepped over four lines; o → blue Circle, o → orange Sunny, o → green Flower; squiggle accent |
| 17.0–19.0 | Constellation | cream | none | eight small shapes on two crossing curves drift |
| 19.0–21.0 | Badge field | green | none | cream Circles with ink and blue shapes scale-pop |
| 21.0–23.0 | Badge cluster | ink | none | four badges (orange, grey, yellow, cream) overlap; arrows float |
| 23.0–24.0 | Thought | blush | none | scalloped cloud with an orange Sunny, trailing circles |
| 24.0–26.0 | Capsule | yellow | none | a cream Pill fills with a blue Clover8, green Semicircle, ink dot |
| 26.0–27.0 | Break | blush | "We'll be back soon" | cream Clover8 shapes behind; loop accent |
| 27.0–29.0 | Return | orange → blue | "See you soon!" | blush Clover8 top, cream Burst bottom; arrow draws on |
| 29.0–31.0 | Closer | cream | "beautiful" | letters arrive with swaps (Semicircle, Sunny, Star4, VerySunny), then resolve to the plain word |

Why it passes the bar: a copy deck of ten short lines; one stage colour per card; a
recurring cast of six shapes; at most two swaps per line; one focal event per card;
every entrance a spring with visible overshoot; every third card wordless; the closer
resolves swaps back to letters. What a full spec adds: the numbers on every card entry
and the verification checklist.
