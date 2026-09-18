# House style — animated essay figures

Shared by every figure on a page. Written once; each figure spec references it.

## Visual system

| Token | Hex | Use |
|---|---|---|
| `page` | `#F7F7FA` | Background |
| `cream` | `#EDECE1` | Cards, chips, panels |
| `ink` | `#3B3730` | Primary text, structural strokes |
| `muted` | `#A3A09D` | Secondary text, gridlines, ticks |
| `warm-dk` | `#746E63` | Illustration fill, dark |
| `warm-lt` | `#948778` | Illustration fill, light |
| `accent` | `#C5683C` | Warm accent — one per figure, used sparingly |
| `indigo` | `#4B4FDD` | Cool accent — data, signal, the "live" element |
| `lavender` | `#7C71B5` | Sub-labels, highlighted state |
| `edge` | `#D9D3C6` | Hairline borders |

Type roles: **serif italic** for object names · **serif regular** for titles ·
**sans uppercase, letterspaced ~0.15em** for labels and subtitles · **sans
regular** for in-figure content text. Editorial, restrained, lots of whitespace.

## Motion grammar

- Everything loops seamlessly and runs continuously.
- Transitions between beats are **opacity crossfades in place**. Elements do not
  slide, re-centre, or resize between beats — they fade. Continuous motion never
  restarts when an element fades back in.
- Scrolling content fades out toward its trailing edge rather than hard-clipping.

## Embed contract

Each figure ships inside a long-form essay page (reference context:
worldlabs.ai/blog). A page carries 3–4 of these. All required:

1. **Responsive** — legible from 390px to 1440px+. Reflow, restack, or rescale as
   you judge best; a shrunken illegible strip fails.
2. **Plays only when in viewport**, pauses when out.
3. **Honours `prefers-reduced-motion`** with a static, still-informative composition.
4. **Accessible** — a screen-reader user gets the figure's point.
5. **Self-contained** — drops into an existing page without restructuring it.
6. **Reports page weight** — total bytes downloaded, including runtime and fonts.

Because a page carries several figures, per-figure cost matters: state whether
your approach's fixed cost amortises across figures or repeats per figure.

## Quality bar

Judged on two things, in this order:

**1. Does the motion carry the idea?** The animation must *teach*, not decorate.
The distinguishing property of each concept should be legible in how it moves —
if two concepts differ in kind, their motion must differ in kind. A viewer who
watches once, without narration, should be able to state the point.

**2. Is it crafted?** Considered spacing and hierarchy, confident use of the
palette, motion that eases rather than lurches, no overlap or misplacement at any
viewport width, no element that exists without a reason.

A figure that is visually pretty but whose motion is arbitrary decoration fails
the first test and therefore fails.
