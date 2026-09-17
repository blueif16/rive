# Rive projects

## Placement is measured, never eyeballed

A rendered PNG read by a model is not evidence about layout — the last lesson
shipped a collision that existed for 0.2s at an animation apex and passed every
check. NEVER conclude "it clears" / "they don't overlap" from looking at a frame.

- **NEVER trust `rive inspect --json` for position.** `computedWorldX/Y` and
  `computedWidth/Height` are **always `0`** — derived properties populated by the
  runtime, and `inspect` is a static resolve.
- **ALWAYS get world-space numbers from Luau at runtime**: `artboard:node(name)`
  → `node.worldTransform` (`Mat2D`: `xx xy yx yy tx ty`), `node:asPath()` for the
  geometry, `artboard:bounds()`. There is no `bounds()` on a node — compute the
  AABB by transforming path points.
- **ALWAYS assert over the animation's extremes, not one frame.** Bounds are
  time-varying; an arc apex is where collisions live. Artboards expose `advance`,
  and `--data-dump-every` dumps a time series:
  `rive . --data-dump=- --data-dump-every=1 --advance=52.5s`
- **`--verify` exiting 0 is not a correct picture.** A dead bind, an unposed rig
  and an overlap all pass it.

## Look it up in the CLI, not on the web

`rive docs <topic>` / `rive schema <Type>` are version-matched to the installed
binary. The **published rive.app docs are wrong** about the Tests protocol
(they show `function setup(test: Tester)`; the CLI requires the double wrapper
and silently skips the file otherwise, reporting "no Tests scripts found").
Context7 mirrors the website, so it inherits that error — use it for orientation,
then confirm against `rive docs`.

## Rendering

`scripts/rive-export` shells one `rive --screenshot` per frame and takes ~6 min
for a 52.5s scene — it looks like a hang. Drive `render.mjs` directly; ffmpeg
needs `-c:v png` on the input or it opens no encoder and writes a 0-byte file.
See `.claude/skills/rive-animation/SKILL.md` §8.
