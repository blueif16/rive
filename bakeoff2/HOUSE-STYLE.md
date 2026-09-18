# House style — animated essay figures

Shared by every figure. Each figure spec references it.

## Visual system

| Token | Hex | Use |
|---|---|---|
| `page` | `#F7F7FA` | Background |
| `cream` | `#EDECE1` | Cards, chips, panels |
| `ink` | `#3B3730` | Primary text, structural strokes |
| `muted` | `#A3A09D` | Secondary text, gridlines, ticks |
| `warm-dk` | `#746E63` | Illustration fill, dark |
| `warm-lt` | `#948778` | Illustration fill, light |
| `accent` | `#C5683C` | Warm accent, used sparingly |
| `indigo` | `#4B4FDD` | Cool accent — data, signal, the live element |
| `lavender` | `#7C71B5` | Sub-labels, highlighted state |
| `edge` | `#D9D3C6` | Hairline borders |

Type roles: **serif italic** for object names · **serif regular** for titles ·
**sans uppercase, letterspaced ~0.15em** for labels and subtitles · **sans
regular** for in-figure content text. Editorial, restrained, generous whitespace.

## Motion grammar

- Loops seamlessly; motion runs continuously.
- Beat transitions are **opacity crossfades in place**. Nothing slides,
  re-centres, or resizes between beats.
- Continuous motion never restarts when an element fades back in.
- Scrolling content dissolves at its trailing edge rather than hard-clipping.

## Embed contract

The figure ships inside a long-form essay page. All required:

1. **Responsive** — legible from 390px to 1440px+.
2. **Plays only when in viewport**, pauses when out.
3. **Honours `prefers-reduced-motion`** with a static, still-informative composition.
4. **Accessible** — a screen-reader user gets the figure's point.
5. **Self-contained** — drops into an existing page without restructuring it.
6. **Weight reported** — total bytes downloaded, including runtime and fonts.

## Quality bar

**1. Does the motion carry the idea?** The figure must teach, not decorate. The
distinguishing property of the concept has to be legible in how things move. A
viewer who watches once, without narration, should be able to state the point.

**2. Is it crafted?** Considered spacing and hierarchy, confident palette use,
motion that eases rather than lurches, no overlap or clipping at any width.
