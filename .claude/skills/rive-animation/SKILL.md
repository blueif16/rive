---
name: rive-animation
description: Author Rive animations as code with the Rive CLI and RML (Rive Markup Language), then export them to GIF/MP4/HTML/PNG that anyone can open. Use when asked to build, edit, animate, inspect, or export a Rive graphic — or when a task mentions Rive, RML, `.rml`, `.riv`, `.rev`, `rive.yaml`, or an interactive/state-machine animation.
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

The `.html` inlines the `.riv` as base64 (a `file://` page cannot `fetch` a
sibling `.riv` — CORS blocks it) and pulls the Rive runtime from unpkg, so it
needs network on first open. GIF/MP4 need nothing.

Only reach for the Editor formats when the user actually wants them — both need
`rive login`: `rive <dir> --rev=out.rev` to reopen in the Editor, `--publish` to
sign for the web (required for files containing scripts; watermarked until the
project is bound to a Rive file).
