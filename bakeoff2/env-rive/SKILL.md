# Authoring an essay figure in Rive

The environment is prepared. Fonts are placed, the venv has fontTools, the
primitive library is written, and `generate.py` already compiles. Copy the
starter, replace `build_scene()`, leave the assembly alone.

## The loop

```bash
./.venv/bin/python generate.py && rive . --once
```

Sub-second. Run it after every meaningful edit.

**NEVER run `rive .` without `--once` or `--verify`.** The bare form opens a
blocking preview window and hangs until killed. `--once` writes the `.riv` and
exits 1 on errors; `--verify` checks without writing.

Errors land in `build/problems.log`. `rive docs <topic>` and `rive schema <Type>`
are version-matched and authoritative — prefer them over recall, since RML is
recent and easy to misremember.

## Measure text before you place it

This is the highest-value habit here, and the one that silently ruins figures.

Rive text boxes are **fixed size with visible overflow**. A string wider than its
box spills across its neighbours, and the compiler reports **zero errors**. There
is no reflow and no warning — `problems.log` will say `OK` while the figure is
visibly broken.

```python
w = R.fit_box(label, fs, TTF["sans"], pad=12)     # never guess this number
box.add(R.text(x, y, w, h, label, fs, INK, FONTS, font="sans", ids=ids))
```

Size every box from `R.measure()` or `R.fit_box()`. If you find yourself typing a
literal width next to a string, you have introduced the bug.

## Painter order is reversed

`El` emits children back-to-front: the **first** thing you `.add()` is the
**backmost**. Build background first, foreground last — the natural reading
order. Only `Fill`/`Stroke` inside one shape are not flipped.

## Group opacity does not composite as a layer

Rive multiplies a group's opacity into each drawable individually rather than
compositing the group once. Consequence: a page-coloured mask nested inside a
fading group goes translucent exactly when it is doing its job, and whatever it
was hiding leaks through.

Keep masks and edge fades in **their own never-faded layer**, between the
content they hide and the foreground. Do not nest them inside anything you
animate the opacity of.

## What the library gives you

`rivelib` as `R`: `rect` `ellipse` `line` `poly` `curve` `text` `grp` `solid`
`fill` `stroke` `edge_fade` `measure` `fit_box`, plus `Anim` and the `EASE_*`
constants.

- `R.curve(points, colour, thickness)` — a smooth continuous stroke through a
  point list, not a polyline. Use it for any traced path or plotted signal.
- `R.edge_fade(...)` — a page-coloured gradient wash so scrolling content
  dissolves instead of hard-clipping.
- `anim.fade(id, [(frame, opacity), ...])` — standard crossfade ease.
- `anim.linear(id, "x", [(frame, value), ...])` — constant velocity, for marquees.
- `anim.key(id, prop, [(frame, value, ease), ...])` — everything else. `ease` is
  `None` for linear, `"hold"` for a step, or a 4-tuple cubic.

Group anything you move or fade with `R.grp(name, id=ids())` and key the group's
id — never key each child.

## Seamless loops

The timeline loops on `DUR_F`. Every animated value must return to its frame-0
value by `DUR_F`, and any periodic motion needs a period that divides `T_LOOP`
exactly, or the seam will visibly jump.

For a marquee: translate by exactly one item pitch over `DUR_F / n` frames with
linear easing, and lay down enough items to cover the viewport plus one pitch.

## Responsive

Rive has no reflow. The way to serve multiple widths is **one artboard per
breakpoint**, laid out side by side in the same document at different `x`
offsets, each with its own complete set of coordinates. Budget for this: a
second artboard duplicates every tuned number in the layout.

If the spec's width range can be served by scaling one artboard with
`Fit.Contain`, prefer that — it is far cheaper. Only add artboards when scaling
would make text illegible.

## Verify by rendering

```bash
../../.claude/skills/rive-animation/scripts/rive-export . --format=png --fps=1
```

Then open the PNGs. The compiler proves the file is structurally valid; it says
nothing about whether the figure looks right. Overlap, misalignment, and a
broken loop are all invisible to it.

## Export

```bash
../../.claude/skills/rive-animation/scripts/rive-export . --format=mp4,html
```

Produces a shareable MP4 and a self-contained double-clickable HTML from the
compiled `.riv`, in one command.
