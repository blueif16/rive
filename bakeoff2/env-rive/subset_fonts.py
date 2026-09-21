#!/usr/bin/env python3
"""Instance + subset the embedded fonts to exactly the glyphs the scene uses.

Sources in fonts/src/ are never modified; the four embedded faces are
regenerated from them on every build, driven by build/charsets.json, which
generate.py writes from the strings actually passed to R.text().

Run order:  generate.py  ->  subset_fonts.py  ->  rive . --once

Keeping sources separate is the point: if the embedded faces were their own
input, each build would narrow them further, and the first string using a new
character would silently render as nothing while the compile still said OK.
"""
import json
import pathlib
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

HERE = pathlib.Path(__file__).parent
SRC = HERE / "fonts/src"
OUT = HERE / "fonts"

FACES = [
    # (source, embedded name, axis location, charsets.json key)
    ("EBGaramond-var.ttf",        "serif.ttf",        {"wght": 400}, "serif"),
    ("EBGaramond-Italic-var.ttf", "serif-italic.ttf", {"wght": 500}, "italic"),
    ("Inter-src.ttf",             "sans.ttf",         {"opsz": 14, "wght": 400}, "sans"),
    ("Inter-src.ttf",             "sans-medium.ttf",  {"opsz": 14, "wght": 500}, "sansmed"),
]


def build(src_name, out_name, location, charset):
    src = SRC / src_name
    if not src.exists():
        sys.exit(f"missing source font {src}")
    font = TTFont(src)
    if "fvar" in font:
        font = instancer.instantiateVariableFont(font, location, inplace=True)

    options = subset.Options()
    # An explicit feature list, never "*": Inter's feature table references
    # variant glyphs that are not in the subset and the subsetter dies on them.
    options.layout_features = ["kern", "liga", "calt", "ccmp", "locl"]
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.notdef_outline = True
    options.recalc_bounds = True
    options.drop_tables += ["DSIG"]
    options.glyph_names = False

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=charset or " ")
    subsetter.subset(font)

    out = OUT / out_name
    font.flavor = None
    font.save(out)
    print(f"  {out_name:18s} {len(set(charset or ' ')):4d} glyphs  "
          f"{out.stat().st_size / 1024:7.1f} KB  (from {src.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    charsets = json.loads((HERE / "build/charsets.json").read_text())
    for src, out, loc, key in FACES:
        build(src, out, loc, charsets.get(key, ""))
