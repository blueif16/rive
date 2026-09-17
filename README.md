# rive

Authoring Rive animations as code — RML text in, `.riv` plus openable previews out.

Rive shipped a CLI and **RML** (Rive Markup Language, an XML description of a Rive
scene) in 2026. Together they let an agent write an animation as text, compile it,
and check it headlessly — no Editor, no account, no network.

## Start

```bash
rive --version || curl -fsSL https://releases.rive.app/cli/install.sh | sh
rive create myproject
rive myproject            # live preview window, rebuilds on save
```

Then open the folder in Claude Code and describe what you want. The
`rive-animation` skill in `.claude/skills/` loads automatically and covers the
author → verify → export loop.

## Export

The CLI only emits `.riv` (needs a runtime) and `.rev` (needs the Editor). To get
something a person can just open:

```bash
.claude/skills/rive-animation/scripts/rive-export myproject --format=all
```

Writes `.gif`, `.mp4`, `.png`, and a self-contained `.html` that keeps the
animation interactive and opens with a double-click.

## Reference

The CLI carries its own docs, which are version-matched and authoritative:
`rive docs --list`, `rive docs <topic>`, `rive schema <Type>`.
Online: <https://rive.app/docs/cli/overview> · <https://rive.app/docs/runtimes/advanced-topic/rml>
