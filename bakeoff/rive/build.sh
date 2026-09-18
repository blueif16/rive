#!/usr/bin/env bash
# Full build: RML -> fonts -> .riv -> the files the page actually serves.
set -euo pipefail
cd "$(dirname "$0")"

PY=./.venv/bin/python
RIV=build/world-model-taxonomy.riv

$PY generate.py                 # scene.rml + build/charsets.json
$PY subset_fonts.py             # fonts/*.ttf, cut to the glyphs the scene uses
rive . --once                   # compile; exits 1 on error

mkdir -p figure
cp "$RIV" figure/world-models.riv

# file:// pages cannot fetch a sibling .riv (opaque origin), so a base64 copy
# rides along for the double-click case. Nothing requests it over http.
$PY - <<'PY'
import base64, pathlib
b = pathlib.Path("figure/world-models.riv").read_bytes()
pathlib.Path("figure/world-models-inline.js").write_text(
    "window.WM_FIGURE_RIV=\"%s\";\n" % base64.b64encode(b).decode())
PY

printf '\n%-28s %8s\n' "file" "bytes"
for f in figure/rive-runtime.js figure/rive.wasm figure/world-models.riv \
         figure/wm-figure.js index.html; do
  printf '%-28s %8d\n' "$f" "$(stat -f%z "$f")"
done
