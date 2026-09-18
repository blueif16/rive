# Spec template and canonical exemplar

The spec is one Markdown document. Copy the section skeleton exactly; fill every slot.
The exemplar at the bottom is the piece that defined this style's contract.

## Skeleton

```
# <Title>

**Fit:** <table from Step 0, with the sum>
**Format:** <W×H>, <duration> s, time-based, <BPM> grid (0.25 s / 0.5 s units), <renderer>
**Defaults assumed:** <list, or "none">

## The idea
<one paragraph: the story in the medium's terms>

## The spine
- Motif: <figure> — <what it means>
- Anchor: <frame position> — never drifts during acts <…>
- House inks: <3–4 inks with roles>; paper <hex>; misregistration budget <px>

## Timeline
| time (s) | act | what happens |
|---|---|---|
<every cut on the grid; act boundaries explicit; breathe beats marked>

## Scene library (in timeline order)
### <n>. <name>   t = <start–end>, <transition in>
- Silhouette: …
- Anchor: …
- Inks: <ink> = line · <ink> = base · <ink> = overprint (<mix result>) · <ink> = accent; misregistration per ink
- Knockouts: …
- Tone: <where dots, pitch, angle> · <where grain> · <where solid>
- Motif rhyme: …
- Live element: <what moves, how, timing on the grid>
- Don't: …

## Composition rules for every scene
<the seven rules from subjects-and-composition.md, adapted to this piece>

## Visual system
- Paper: …
- Inks: <name hex role> …
- Screening: pitch <px>; angles <ink: deg …>; grain zones <…>
- Coverage: large solids <75–85 %>; voids; roller band <on/off>
- Misregistration: <1–3 px>, fixed per scene, motif fringe on <side>
- Print texture: speckle, voids, paper hatching
- Line quality: wobble, width variation, tapered ends, rings never perfect
- The motif: <size as % of frame width>, <ink>

## Motion vocabulary
<each move used: print origin, easing, duration, parameters — from motion-vocabulary.md>

## Architecture
<render(t) pure, seeded PRNG per element, cue array, scene registry, plate compositor, caching, controls>

## Process
<staged build with stop points: engine first with stills at t=…; scenes in batches with screenshots; transitions and late acts; boundary inspection at 0.25 s steps>

## Verification checklist
<≥ 6 measurable checks; one measures the anchor at every act boundary>

## Don'ts
<the style's must-nots plus this piece's own>

## Renderer appendix: <renderer>
<from renderer-notes.md>

## Self-check
| bar item | PASS/FAIL | evidence |
```

## Canonical exemplar (abridged)

The idea. A lone ink dot calls out into the world with ripples, and everything that
resonates answers back: bells, wolves, whales, radios, fireworks. It collects them as
memories, but alone they fade to blue. A second dot, pink, answers from off-screen. Where
their ripples meet, a flower blooms, the world is reprinted in their two inks, and we pull
back to a universe of pairs. It ends on a hand-lettered signature.

The spine. A small indigo dot pinned to the exact centre, and concentric ripple rings
coming out of it. Every scene, transition and camera move is organised around that dot.
It never drifts during Acts I–III.

Timeline (720×720, 28 s, 120 BPM).

| time | act | what happens |
|---|---|---|
| 0.0–1.5 | I The call | Blank cream paper, dot at centre. Two blue ripples expand past the edges; tick arcs flick at the rim. |
| 1.5–4.5 | | Each ripple leaves a disc (55 % of frame) holding a tiny world, with blank paper and one ripple between: koi pond → cricket on a yellow moon (coin flip, rim visible) → jellyfish in a green-blue sea (slides in from the right, rotating). |
| 4.5–6.0 | | A disc opens on the dot and the camera dives through to full bleed: owl → temple bell with sound arcs → lighthouse. Each next scene opens as a disc over the previous one. |
| 6.0–13.9 | II Everything resonates | Montage of full-bleed scenes, hard cuts on the beat, 0.5 s → 0.25 s. Breathe at 6.0, 8.0, 10.0: blank paper for one ripple, then iris open. |
| 13.9–15.9 | | Rewind: earlier scenes flash back in reverse in swapped inks, a pale double lens ring tightening each time. |
| 15.9–17.8 | III Archive | Pull back: ~40 medallions on 4 counter-rotating orbits on pale yellow paper. They drain to one blue ink, shrink, scatter. Lone dot. One beat of stillness. |
| 17.8–22.0 | IV The answer | Pink halftone glow from bottom-left; pink ripple arcs roll in. The dot answers with a blue ring. Camera eases back to reveal the pink dot. Alternating blue and pink ripples, bolder, drifting closer. |
| 22.0–23.0 | | Rings touch: yellow sparks, the pink dot gets a yellow core, a pink lotus with an orange-yellow heart blooms between them, framed by one blue and one pink ring. |
| 23.0–24.0 | V Together | Duotone reprise in pink + blue only: waterfall, whale, rocket, ringed planet, both dots in every frame. |
| 24.0–26.0 | | Indigo night with star grain. The two dots with yellow halos orbit inside their rings. Zoom out to hundreds of pairs. |
| 26.0–28.0 | VI Signature | Cream paper. The title hand-lettered stroke by stroke in indigo with pink misregistration; the two dots as a "••" mark; the pink dot sends one ring; a second line writes itself; hold; lettering dissolves into shrinking halftone dots. |

Scene library for Act II (order): howling wolf on a snowy ridge under aurora · rotary
telephone on a pink sunburst (dot = dial) · turntable (dot = spindle) · frogs under a full
moon among reeds · bats out of a cave at sunset · breaking wave · cat from behind at a
rainy window · sunflower with a bee (dot = heart) · valve radio with sound arcs ·
fireworks over a harbour · hummingbird among morning glories · whistling kettle on tiles ·
Ferris wheel at dusk · jungle waterfall · bicycle under bougainvillea · whale in light
shafts · piano strings with sound arcs · rocket launch from a gantry · apartment windows at
night · ringed planet · hot-air balloons over hills · volcano with lightning · radio
telescope and a spiral galaxy · campfire in a dark forest · sunflower field · layered
ridges at sunrise · umbrella pine over furrowed fields · raindrops on a night pond.

Visual system. Paper `#F2EDE3` with static fibre grain. Inks: blue `#0078BF`, fluorescent
pink `#FF48B0`, yellow `#FFE800`, green `#00A95C`, orange `#FF6C2F`, violet `#765BA7`,
indigo `#2E3192` for the dot and lettering. No black. Halftone per ink, 4–6 px pitch,
angles 15°/45°/75°/0°, gradients as dot-size ramps, solids at 100 %. Misregistration 1–3
px per ink in a fixed direction per scene; the dot always shows a thin pink fringe on one
side. Speckle, ink-starved voids, paper hatching for highlights. Hand-drawn wobble; ripples
never perfect circles. The dot is 2.2 % of frame width.

Quality bar. Fewer excellent scenes beat many mediocre ones. If short on budget, cut Act
II scenes, never the transitions or Acts III–VI.

Why this exemplar passes the bar: motif and anchor are defined before any scene; every
transition is a print move with a duration; every scene has a stated anchor landing; the
system section carries pitch, angles, coverage and misregistration as numbers; the process
section stops for stills at fixed times; the don'ts forbid gradients, black, crossfades and
extra text. What the abridged form omits and a full spec must include: the per-scene ink
plan with knockouts for all 28 scenes, and the verification checklist.
