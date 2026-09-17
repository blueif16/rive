---
name: rive-animation
description: Author Rive animations as code with the Rive CLI and RML (Rive Markup Language), export them to GIF/MP4/HTML/PNG that anyone can open, and decode an existing `.riv` back into RML so its artwork can be reused. Use when asked to build, edit, animate, inspect, or export a Rive graphic, to reuse a character or asset that only exists as a compiled `.riv`, or when a task mentions Rive, RML, `.rml`, `.riv`, `.rev`, `rive.yaml`, or an interactive/state-machine animation.
---

# Rive animations from the terminal

The Rive CLI compiles **RML** (an XML description of a Rive scene) into a `.riv`,
and checks it headlessly — no Editor, no account, no network.

**RML and the Rive CLI postdate your training data.** Every type and property
name must come from `rive schema` or `rive docs`. Guessing produces confident
nonsense; the compiler catches misspelled *names*, but not wrong *wiring*.

## 1. Setup

```bash
rive --version                       # already installed?
```

If not found, the binary is usually at `~/.rive/bin/rive` but off `PATH`. Install:

```bash
curl -fsSL https://releases.rive.app/cli/install.sh | sh
echo 'export PATH="$HOME/.rive/bin:$PATH"' >> ~/.zshrc   # then restart the shell
```

`ffmpeg` is needed for GIF/MP4 export only (`brew install ffmpeg`).

## 2. Start a project

```bash
rive create <name>                   # scaffolds rive.yaml, scene.rml, AGENTS.md
rive create <name> --from-rev=f.rev  # or convert an existing Editor file
```

**Read the generated `AGENTS.md` first** — it is the authoritative, version-matched
contract for that CLI build. This skill covers what it does not: install, and export.

`rive samples` copies runnable example projects; start from one when the scene
type matches (`rml_triangle`, `rml_vm_input`, `pointer_reactive`, `text_input`).

## 3. Look it up — the two lookup commands

Reach for these *before* writing markup, not after a build fails:

```bash
rive schema <Type>              # properties, defaults, enum names, propertyKey ids
rive schema --search <text>     # find a type when you don't know its name
rive schema <Type> --animatable # what can be keyed    (--bindable for data binding)
rive docs --list                # topics: layout, data, state-machines, easing, text…
rive docs <topic>               # e.g. `format`, `skeleton`, `gotchas`, `workflow`
rive docs --search <text>
```

`rive docs gotchas` and `rive docs workflow` are worth reading in full the first
time — they cover the silent-failure modes this skill deliberately does not restate.

## 4. Build it in passes

Do not emit a finished scene in one shot. Builds take milliseconds, so:
wireframe (every region a sized, **filled** box) → structure → text/content → detail.
Verify after each pass. Patch the file in place; re-emitting a whole tree is how
closing tags get lost.

Expect the first build to rewrite nearly every line — `rive` stamps an `id=` onto
every element that lacked one. Commit that diff on its own.

### Unit traps that compile clean and look wrong

| Thing | Unit |
|---|---|
| `rotation` (propertyKey 15) | **radians** — a full turn is `6.2831855`, not `360` |
| `LinearAnimation.duration` | **frames**, at `fps` (default 60) — 2s is `120` |
| `StateTransition.duration` | **milliseconds** |
| Colors | ARGB hex, no `#`: `colorValue="FF4FD1C5"` |

A `KeyFrameDouble` pointed at a color or boolean property builds, inspects, and
animates nothing. Match the keyframe type to the property type from `rive schema`.

## 5. Check — three commands, three different questions

```bash
rive <dir> --verify              # does it compile?           (exit 1 on error)
rive inspect <dir> --summary     # what got built? problems empty?
rive <dir> --screenshot=out.png --advance=1   # what does it look like?
```

None substitutes for another. A dead data bind and an invisible shape both pass
the first two. `--advance=1` matters: with no advance you capture the authored
rest pose, before the state machine has run.

**Done means all four:** `--verify` exits 0 · `inspect` reports no `error`
problems · you have *viewed* a rendered frame · for anything animated, you have
viewed **two frames at different times** and confirmed they differ. A clean build
is not evidence that the animation moves.

Drive the scene before capturing when behaviour is the point:

```bash
rive <dir> --screenshot=on.png --pointer=click@120,60 --advance=20
rive <dir> --screenshot=full.png --data=battery/level=100
rive <dir> --screenshot=narrow.png --viewport=320x700    # does the layout reflow?
```

## 6. Export something openable

A `.riv` needs a runtime to play; a `.rev` needs an account and the Editor. To
hand a human something they can just open, use the bundled script:

```bash
.claude/skills/rive-animation/scripts/rive-export <dir> --format=all
```

| Format | Use it for |
|---|---|
| `gif` | Slack, GitHub comments, docs — plays anywhere, no deps |
| `mp4` | Smaller and cleaner than GIF for longer or gradient-heavy motion |
| `html` | **Interactive** — one self-contained file, double-click to open. Keeps the state machine, pointer input and data binding |
| `png` | A single still |

Defaults to `gif,html`. Artboard size, loop length and state-machine name are
read from `rive inspect`; override with `--fps`, `--duration`, `--scale`,
`--artboard`, `--out`. Exits non-zero on a failed build, so it is CI-safe.

### Frames come from one browser pass, not one CLI call each

`gif`/`mp4` render through `scripts/render/render.mjs`: headless Chrome loads the
`.riv` **once** via `@rive-app/canvas-advanced`, advances by a fixed `dt`, and
streams PNGs to ffmpeg's `image2pipe`. Never loop `rive --screenshot` per frame —
that rebuilds the `.riv` every time, and a 52.5s lesson takes ~6 minutes instead
of ~15 seconds.

```bash
node scripts/render/render.mjs --riv=build/x.riv --fps=30 --duration=52.5 | ffmpeg …
node scripts/render/render.mjs --riv=build/x.riv --stills=2,11.5,24 --stills-dir=/tmp
node scripts/render/render.mjs --riv=build/x.riv --info      # artboards, animations, inputs
```

`--stills` is the iteration loop: several timestamps from a single pass, so you
can look at every segment of a long animation in one command.

> **The Canvas2D renderer is deferred, and draw-then-read renders nothing.**
> `artboard.draw()` only pushes closures onto a queue; `flush()` is literally
> `function(){}`. The queue is replayed by **Rive's own `requestAnimationFrame`
> driver, after your callback returns** — so a frame is on the canvas at the
> *start of the next tick*. Capture one tick late. A synchronous
> draw-then-`toDataURL` yields a blank canvas that looks like a broken file.

Animation time stays a fixed `dt`, so output is reproducible; only wall-clock
pacing is left to the browser. `--info` needs no state machine and is the fastest
way to see what an unknown `.riv` contains.

The `.html` inlines the `.riv` as base64 (a `file://` page cannot `fetch` a
sibling `.riv` — CORS blocks it) and pulls the Rive runtime from unpkg, so it
needs network on first open. GIF/MP4 need nothing.

Only reach for the Editor formats when the user actually wants them — both need
`rive login`: `rive <dir> --rev=out.rev` to reopen in the Editor, `--publish` to
sign for the web (required for files containing scripts; watermarked until the
project is bound to a Rive file).

## 7. Reusing artwork that only exists as a `.riv`

`rive create --from-rev` converts an **editor** `.rev`. There is no supported path
from a compiled `.riv`, and `rive docs assets` is explicit that `SVGAsset` and
`LottieAsset` are editor-only and **stripped on export** — so tracing or
re-importing is not an option either. Use `scripts/rivdec.py`, which reads the
runtime binary and re-emits an artboard as RML:

```bash
python3 scripts/rivdec.py char.riv --summary              # artboards, object counts
python3 scripts/rivdec.py char.riv --artboard=A --tree    # every object, with #index
python3 scripts/rivdec.py char.riv --artboard=A --rml --prune=56 > scene.rml
```

`--prune=<#index>` drops an object with its descendants — how you leave part of a
graphic behind. Pruning is transitive over `Id`-typed properties, because dropping
a Shape orphans the `KeyedObject` animating it and the build then fails — but it
**must skip the three sibling-list Ids below**, or a `stateToId` of 4 gets read as
"object 4" and pruning an unrelated object silently deletes a live transition.

Property types come from `rive schema --json` (cached in `rive-schema.json`), so
keys are typed by the version-matched CLI rather than guessed. Rebuild that cache
after `rive update`.

### The two things that make an extraction compile but render wrong

**1. The format nests two different ways.** There is no universal parent pointer.

| Objects | How the parent is found |
|---|---|
| Drawables — `Shape`, `PointsPath`, `Fill`, `Stroke`, `SolidColor`, `Node`, `Bone`, `Solo`, `ClippingShape` | `parentId`, an index into the artboard's object list (0 = the artboard) |
| Timelines — `LinearAnimation` › `KeyedObject` › `KeyedProperty` › `KeyFrame*` | **no `parentId` at all** — read order |
| State machines — `StateMachine` › `Layer` › `State` › `Transition` › `Condition` | **no `parentId` at all** — read order |

The runtime builds the second group with an `ImportStack`:
`importStack.latest<LinearAnimationImporter>(…)` attaches each object to the one
most recently read. Attach those by `parentId` instead and every keyframe lands
directly under `<Artboard>`: **it still compiles with 0 errors**, but the runtime
discards the orphans (`Failed to import object of type 26`) and the artwork
renders in its unposed rest pose.

**2. Three `Id` properties do not index the object list.**

| Property | Indexes | Runtime |
|---|---|---|
| `animationId` | the artboard's animations | `m_Artboard->animation(id)` |
| `stateToId` | the **layer's** states | `m_Layer->m_States[id]` |
| `inputId` | the state machine's inputs | `addInput` order — `readNullObject()` pushes a `nullptr` input, so null objects hold index slots |

Everything else — `objectId`, `sourceId`, `targetId`, `activeComponentId`,
`interpolatorId`, `styleId` — goes through `context->resolve()`, the object list.

This distinction bites **twice**, and the second one is easy to miss: on *emit*,
resolving the three against objects wires transitions to arbitrary Shapes; on
*prune*, testing them against the dropped-object set deletes live objects that
merely share an integer with something you removed. Both produce a file that
builds with 0 errors and renders in the wrong pose.

**Verifying an extraction takes more than a clean build.** Both failures above
pass `--verify`. Render the source `.riv` and the extraction at the same size and
timestamp and compare them side by side:

```bash
node scripts/render/render.mjs --riv=source.riv --artboard=A --width=1000 --stills=1.2 --stills-dir=/tmp
node scripts/render/render.mjs --riv=build/x.riv            --width=1000 --stills=1.2 --stills-dir=/tmp
ffmpeg -i a.png -i b.png -filter_complex hstack out.png     # then look at it
```

Watch for a limb or feature sitting in the wrong place — that is the rest-pose
signature of failure 1, not a geometry error.

Bones (`RootBone`, `IKConstraint targetId`) and `Solo activeComponentId` survive
extraction, so a rig stays drivable: move the IK target to aim a head, key the
`Solo` to switch a variant.

### Placing an extracted artboard inside another scene

Emit it as a **sibling** `<Artboard isComponent="true">` and reference it with
`<NestedArtboard artboardId="…">`. Three things to get right:

- **Ids share one namespace across the whole document.** Renumber the extracted
  artboard onto a different client (`1:N` → `2:N`) or it collides with the host
  scene on every id it declares. Assert afterwards that no old prefix survives.
- **Every `.rml` in the project directory compiles as one document.** A fragment
  kept as an input file, not a scene, must be listed under `exclude:` in
  `rive.yaml` — otherwise it is compiled twice and every id is a duplicate.
- **A `<NestedArtboard>` with no `<NestedStateMachine>` child draws the rest
  pose.** `defaultStateMachineId` only starts a machine on the artboard the
  runtime plays at the top; a nested one runs exactly what its `NestedAnimation`
  children name. It compiles, it inspects clean, and the rig renders unposed —
  the same signature as the two failures above.

## 8. Where is it on screen? — measuring placement instead of eyeballing it

"Does the character overlap the label" is not answerable by looking at a PNG, and
a model's read of a render is not evidence. Two static sources look like they
answer it and do not:

| Source | What it actually returns |
|---|---|
| `rive inspect --json` → `computedWorldX/Y`, `computedWidth/Height` | **always `0`.** Derived properties, populated by the runtime; `inspect` is a static resolve. Verified empirically — do not build a checker on these. |
| `rive <dir> --data-dump` | the bound view-model values, `globals`, and the nested artboards **by name only**. No coordinates until a script writes some. |

**The only native world-space source is Luau, at runtime.** `rive docs
luau/api/artboards`:

```luau
local n = self.instance:node('TeacherArt')   -- artboard:node(name) -> NodeData?
local wt = n.worldTransform                  -- Mat2D: xx xy yx yy tx ty (read-only)
local minPt, maxPt = self.instance:bounds()  -- artboard AABB
```

- `node.children` / `node.parent` walk the tree; `node:asPath()` returns
  `PathData` (the commands) — transform those points by `worldTransform` for a
  real per-node AABB. There is **no `bounds()` on a node and none on `Path`**;
  the AABB is yours to compute.
- `artboard:addToPath(path, transform)` pours a whole artboard's geometry into a
  `Path` — the cheap route to one nested rig's outline.
- Artboards also expose `advance`, so a script can step time and measure a
  moving element at its extremes rather than at one arbitrary frame.

Get the numbers out through data binding: have the script write each rect into
view-model properties, then

```bash
rive . --data-dump=- --data-dump-every=1 --advance=52.5s   # JSON time series
```

### `--test` gates the math, not the scene

`rive <dir> --test` runs Tests scripts and exits **6** on failure, but a Tests
script has **no artboard handle** — it is for pure logic (the AABB/overlap
helpers). Measure in a Node script, assert the geometry helpers in Tests.

The shape is a **double wrapper**, and this is the trap:

```luau
return function(): Tests
    return function(test: Tester)
        test.group('overlap', function()
            test.case('disjoint rects do not intersect', function(expect)
                expect(rects.hit(a, b)).is(false)
            end)
        end)
    end
end
```

> **The published docs are wrong here.** rive.app (and therefore Context7's
> mirror of `rive-docs`) shows a bare `function setup(test: Tester)`. That form
> reports **"no Tests scripts found"** and the file is silently skipped — a green
> run that tested nothing. `rive docs luau/protocols` states the double wrapper
> explicitly. **The version-matched CLI docs beat the website every time.**

### `place.mjs` — the placement tool

`scripts/render/place.mjs` answers "where is everything" in numbers. It boots the
same `harness.html` the renderer uses, so it measures exactly the pixels that
would have been written.

```bash
node place.mjs --riv=build/x.riv --at=17.7                      # grid + components
node place.mjs --riv=build/x.riv --at=2,17.7,43.3 --cols=80     # several moments, one pass
node place.mjs --riv=build/x.riv --at=17.7 --nodes=Rig,Bubble   # name the blobs
node place.mjs --riv=build/x.riv --at=17.7 --regions=r.json --json
node place.mjs --riv=build/x.riv --sweep=0:52.5:0.25 --nodes=Rig,Bubble --rules=k.json
```

Three outputs, in the shape agent-layout tools have converged on (`spatial-tether`,
`dom-density-map`, `playwright-spatial-layout-mcp`): a **density grid**, **exact
boxes**, and an explicit **collision/rule verdict**.

- **grid** — ink fraction per cell as ` .:+#@`. A whole 1200x675 frame reads in
  ~20 lines; a still costs ~2000 tokens and tells you less.
- **components** — 8-connected ink blobs with pixel-exact `x0,y0,x1,y1,w,h,px`.
- **nodes** — `worldTransform()` gives a named node's world ORIGIN; the blob
  containing that origin is what carries the name. **Extents never come from the
  API** — `Node` has no width/height and `inspect`'s `computed*` are all 0.
- **rules** — `not_overlapping · above · below · left_of · right_of · contains ·
  disconnected`, each `{type,a,b,gap?,requirePresent?}`. **Exit 1 on any failure**,
  so `--sweep` is a build gate over the whole timeline, not one sampled frame.

`disconnected` is the sharpest of these and needs no threshold: if two names
resolve to the **same connected component**, their ink is physically touching.
That is how the lesson's three dock crossings were found — a 0.25s sweep of 52.5s
takes ~60s and pinned them to 17.50–18.00, 37.50–38.00, 43.25–43.50.

> **The trap this tool can fall into, already fixed once.** A rig's origin is
> often a floor pivot a pixel or two off its own artwork, so an exact
> point-in-box test misses and the name goes unassigned. The fallback — attach
> the nearest blob — is correct at ~2px and **catastrophic at 60px**: an element
> that is not painted at all (a bubble before it fades in) adopts whatever blob
> is nearby and the gate reports a collision that does not exist. `--anchorReach`
> defaults to **8px** for that reason. If a name is not painted, leave it
> unassigned and let the rule skip via `requirePresent: false` — never guess
> which blob it was.

### `rive-export` does not use the fast renderer

SKILL.md §6 says GIF/MP4 go through `render.mjs`. **`scripts/rive-export` does
not reference it at all** — `render_frames()` still shells one `rive
--screenshot` per frame, rebuilding the `.riv` each time (~6 min for 52.5s, and
it looks like a hang). Until that is fixed, drive the pipe yourself — note
`-c:v png`, without which ffmpeg opens no encoder and writes a 0-byte file:

```bash
node render.mjs --riv=build/x.riv --fps=30 --duration=52.5 \
  | ffmpeg -y -f image2pipe -c:v png -framerate 30 -i - \
      -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
      -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart out.mp4
```
