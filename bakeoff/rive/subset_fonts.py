#!/usr/bin/env python3
"""Instance + subset the source fonts down to the glyphs this figure actually draws.

Full EB Garamond is ~850 KB and full Inter ~876 KB; embedded whole they would
dwarf everything else in the .riv. Each face here ends up at a few KB.

Run with the project venv:  ./.venv/bin/python subset_fonts.py
"""
import json
import pathlib
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"

# generate.py records the exact characters each face draws, so the subset can
# never drift from the copy. Fallback below is only for a cold checkout.
FALLBACK = {
    "serif": "PRSadeilmnortu",
    "italic": "adeilmnprstu",
    "sans": " ()afcegilmnoprstvx→",
    "sansmed": " ABCEIMNOPRSTUVY→",
}

FACES = [
    # (source, output, axis location, charset key)
    ("EBGaramond-var.ttf", "serif.ttf", {"wght": 400}, "serif"),
    ("EBGaramond-Italic-var.ttf", "serif-italic.ttf", {"wght": 500}, "italic"),
    ("Inter-src.ttf", "sans.ttf", {"opsz": 14, "wght": 400}, "sans"),
    ("Inter-src.ttf", "sans-medium.ttf", {"opsz": 14, "wght": 500}, "sansmed"),
]


def build(src_name, out_name, location, charset):
    src = FONTS / src_name
    if not src.exists():
        sys.exit(f"missing source font {src}")
    font = TTFont(src)
    if "fvar" in font:
        font = instancer.instantiateVariableFont(font, location, inplace=True)

    options = subset.Options()
    options.layout_features = ["kern", "liga", "calt", "ccmp", "locl"]
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.notdef_outline = True
    options.recalc_bounds = True
    options.drop_tables += ["DSIG"]
    options.glyph_names = False

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=charset)
    subsetter.subset(font)

    out = FONTS / out_name
    font.flavor = None
    font.save(out)
    print(f"{out_name:20s} {out.stat().st_size / 1024:7.1f} KB   (from {src.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    cs = HERE / "build" / "charsets.json"
    charsets = json.loads(cs.read_text()) if cs.exists() else FALLBACK
    for src, out, loc, key in FACES:
        build(src, out, loc, charsets.get(key) or FALLBACK[key])
