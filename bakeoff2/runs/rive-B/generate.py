#!/usr/bin/env python3
"""Starter scene generator. Copy this, replace build_scene(), keep the rest.

Run:  ./.venv/bin/python generate.py       -> writes scene.rml + build/charsets.json
Then: rive build .                          -> writes build/<name>.riv
"""
import json
import pathlib

from geom import El, Ids
import rivelib as R

HERE = pathlib.Path(__file__).parent

# ==================================================================== config ==
# Colours are 8-digit ARGB strings. "FF" prefix == fully opaque.
PAGE   = "FFF7F7FA"
CREAM  = "FFEDECE1"
INK    = "FF3B3730"
MUTED  = "FFA3A09D"
ACCENT = "FFC5683C"
INDIGO = "FF4B4FDD"
EDGE   = "FFD9D3C6"

W, H = 1200, 600
FPS = 60
T_LOOP = 12.0
DUR_F = round(T_LOOP * FPS)

# Font asset ids are fixed by the document preamble below. Keys match the
# `font=` argument of R.text(). TTF paths are for R.measure().
FONTS = {"serif": "1:2", "italic": "1:3", "sans": "1:4", "sansmed": "1:5"}
TTF = {
    "serif":   str(HERE / "fonts/serif.ttf"),
    "italic":  str(HERE / "fonts/serif-italic.ttf"),
    "sans":    str(HERE / "fonts/sans.ttf"),
    "sansmed": str(HERE / "fonts/sans-medium.ttf"),
}


# ===================================================================== scene ==
def build_scene(ab, anim, ids):
    """Add your drawables to `ab` and your keyframes to `anim`.

    Painter order is document order: the FIRST child drawn is the BACKMOST.
    Group anything you want to move or fade as a unit with R.grp(), give the
    group an id from ids(), and key that id.
    """
    # --- a box that drifts right and back, to prove the pipeline runs ---
    box_id = ids()
    box = R.grp("Box", id=box_id)
    box.add(R.rect(0, 0, 160, 96, r=14, fill_=CREAM, stroke_=(EDGE, 1.5)))
    label = "hello"
    fs = 20
    box.add(R.text(0, 24, R.fit_box(label, fs, TTF["sans"], pad=12), 48,
                   label, fs, INK, FONTS, font="sans", ids=ids))
    ab.add(R.grp("Stage", x=140, y=250).add(box))

    anim.key(box_id, "x", [(0, 0, None), (DUR_F // 2, 760, R.EASE_IN_OUT),
                           (DUR_F, 0, R.EASE_IN_OUT)])
    anim.fade(box_id, [(0, 1.0), (DUR_F // 2, 0.35), (DUR_F, 1.0)])


# ================================================================== assembly ==
def document():
    ids = Ids(start=20)                 # 1:2 .. 1:19 reserved for the preamble
    anim = R.Anim(DUR_F, fps=FPS)

    ab = El("Artboard", reverse=False, name="Main", id="1:8", x=0, y=0,
            width=W, height=H, defaultStateMachineId="1:10", styleId="1:6",
            clip=True)
    ab.add(El("LayoutComponentStyle", name="Main Style", id="1:6"))
    ab.add(El("Fill", reverse=False, name="Background").add(R.solid(PAGE)))

    build_scene(ab, anim, ids)

    # State machine: one layer that enters straight into the looping timeline.
    sm = El("StateMachine", reverse=False, name="Main", id="1:10")
    layer = El("StateMachineLayer", reverse=False, name="Layer 1", id=ids())
    st = ids()
    layer.add(El("AnyState", x=400, y=0))
    layer.add(El("ExitState", x=560, y=0))
    layer.add(El("EntryState", x=0, y=16).add(El("StateTransition", stateToId=st)))
    layer.add(El("AnimationState", x=200, y=0, animationId="1:9", id=st))
    sm.add(layer)
    ab.add(sm)
    ab.add(anim.xml("1:9"))

    root = El("Rive", version=1, kind="fragment")
    root.add(El("FontAsset", file="fonts/serif.ttf", name="serif", id="1:2"))
    root.add(El("FontAsset", file="fonts/serif-italic.ttf", name="serifItalic", id="1:3"))
    root.add(El("FontAsset", file="fonts/sans.ttf", name="sans", id="1:4"))
    root.add(El("FontAsset", file="fonts/sans-medium.ttf", name="sansMedium", id="1:5"))
    root.add(ab)
    return root


if __name__ == "__main__":
    (HERE / "scene.rml").write_text(document().xml())
    (HERE / "build").mkdir(exist_ok=True)
    (HERE / "build/charsets.json").write_text(json.dumps(R.charsets(), indent=2))
    print(f"wrote scene.rml ({(HERE / 'scene.rml').stat().st_size:,} bytes)")
