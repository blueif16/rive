# Authoring an essay figure in React

The environment is prepared. Dependencies are installed, the build is
configured, the palette tokens exist, and the clock hook already implements the
embed contract. Replace `app/figure/Figure.tsx`, leave the plumbing alone.

## The loop

```bash
npm run build          # -> index.html at the package root, single-file, opens over file://
npm run build:embed    # -> dist-embed/figure.js + style.css, the per-figure weight
npm run typecheck      # tsc --noEmit
```

`npm run build` inlines everything into one `index.html`, so it opens by
double-click with no server. That is also how you screenshot it.

## Drive everything from the clock

```tsx
const { t, reduced, ref } = useFigureClock(LOOP_SECONDS);
```

`t` is loop position in `[0, 1)`. The hook already handles all three of the
things the embed contract requires: it pauses when the figure scrolls out of
view, freezes at a representative still under `prefers-reduced-motion`, and
keeps running across beat changes.

**Do not use CSS animations or transitions for anything beat-phased.** A CSS
animation restarts when its element remounts or when its `animation` shorthand
changes — which is precisely the "motion restarted when it faded back in"
defect. Compute the value from `t` and write it to a `transform` instead.

CSS animation is still the right tool for a purely decorative loop that no beat
ever interrupts. If a beat can touch it, it belongs on the clock.

## Beat gating

```tsx
opacity: beatOpacity(t, beatIndex, BEAT_COUNT)
```

Use it for every beat-gated element so they all cross-fade on one curve.
Elements fade **in place** — never animate layout position between beats. If you
find yourself changing `top`, `height`, `grid-template`, or `flex` as a function
of `t`, you are about to ship a reflow, not a crossfade.

## Palette

Tokens live in `figure.css` as CSS custom properties on `.figure`. Use
`var(--indigo)`, never a literal hex. Type roles are the `.name` / `.title` /
`.label` classes.

## Animate only transform and opacity

Those two are the compositor's; everything else costs layout or paint every
frame. A marquee is `transform: translate3d(...)` driven from `t`, not a
changing `left`. Add `will-change: transform` only on elements that actually
move continuously.

## Structure

- **SVG** for anything drawn — curves, shapes, plots, illustrations. Use a
  `viewBox` and let it scale; do not compute pixel coordinates from the
  container width.
- **DOM elements** for anything with text — labels, chips, cards. This is the
  approach's main advantage: text sizes itself, so a box can never be too narrow
  for its label. Do not reintroduce the problem by putting fixed `width` on a
  text container.

## Edge fades

`.fade-left` / `.fade-right` in `figure.css` are mask-image gradients. Put them
on the scrolling track so content dissolves rather than hard-clipping. Masks
composite correctly here, so nesting is fine.

## Responsive

One component, one layout that adapts — not separate desktop and mobile trees.
Reach for, in order: `clamp()` on font sizes and gaps, `aspect-ratio` on the
figure frame, a `viewBox` that scales, container queries or a single media query
to restack lanes vertically when the width no longer supports them side by side.

Check 390px specifically. The common failure is a composition that merely scales
down until its labels are unreadable.

## Accessibility

The outer element is `<figure role="img" aria-label="...">`. Write a sentence
that conveys what the figure *means*, not what it looks like — that label is the
entire figure for a screen-reader user.

## Verify by screenshotting

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --hide-scrollbars --screenshot=shot.png \
  --window-size=1440,1200 --virtual-time-budget=6000 "file://$PWD/index.html"
```

Then open the PNG. A clean typecheck says nothing about whether the figure looks
right.
