#!/usr/bin/env python3
"""Generate scene.rml for the CNN convolution lesson.

Layout + content here, keyframes in timeline.py. The scene is ~700 objects of
grid with computed convolution values and colour ramps, so it is emitted rather
than typed.

    python3 generate.py && rive . --verify && rive . --screenshot --advance=1

Two RML rules this file exists to respect, both of which fail silently:
  * draw order is front-to-back — the FIRST element declared paints on top,
    so every cell's number is emitted before the rectangle behind it.
  * FontAsset is a root element, a sibling of <Artboard>, never a child.

SHOW_ALL=1 reveals every hidden group at once, to check placement. Captions and
sums deliberately overlap in that mode; it is a layout tool, not a preview.
"""

import os
import pathlib
import sys

import timeline

SHOW_ALL = os.environ.get("SHOW_ALL") == "1"

# ---------------------------------------------------------------- content ---
IMG = [[1, 1, 1, 1, 1],
       [1, 8, 8, 8, 1],
       [1, 8, 8, 8, 1],
       [1, 8, 8, 8, 1],
       [1, 1, 1, 1, 1]]

FILTERS = [
    ("Vertical edge",   [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
    ("Horizontal edge", [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
    ("Blur",            [[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
]

N_IN, N_K, N_OUT = 5, 3, 3
POSITIONS = [(r, c) for r in range(N_OUT) for c in range(N_OUT)]


def convolve(k):
    return [[sum(IMG[r + i][c + j] * k[i][j] for i in range(3) for j in range(3))
             for c in range(N_OUT)] for r in range(N_OUT)]


def products(k, r, c):
    return [[IMG[r + i][c + j] * k[i][j] for j in range(3)] for i in range(3)]


OUTS = {name: convolve(k) for name, k in FILTERS}

# ----------------------------------------------------------------- colour ---
BG        = "FF080B11"
INK       = "FFF2F6FB"
INK_MUTED = "FF8A99AD"
INK_DIM   = "FF515F73"
ACCENT    = "FF22D3EE"          # cyan — the live edge: kernel, travelling value
POS_COLOR = (245, 158, 11)      # amber  — positive response
NEG_COLOR = (99, 102, 241)      # indigo — negative response
ZERO_COLOR = (25, 31, 43)
IMG_DARK, IMG_LIGHT = (18, 24, 34), (238, 243, 249)


def hexc(rgb):
    return "FF%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in rgb)


def lerp(a, b, t):
    return [a[i] + (b[i] - a[i]) * t for i in range(3)]


def img_color(v):
    return hexc(lerp(IMG_DARK, IMG_LIGHT, v / 9.0))


def signed_color(v, m):
    if not m:
        return hexc(ZERO_COLOR)
    t = max(-1.0, min(1.0, v / m))
    return hexc(lerp(ZERO_COLOR, POS_COLOR if t > 0 else NEG_COLOR, abs(t)))


def readable_on(c):
    r, g, b = (int(c[i:i + 2], 16) for i in (2, 4, 6))
    return "FF080B11" if (0.299 * r + 0.587 * g + 0.114 * b) > 140 else INK


# ----------------------------------------------------------------- layout ---
W, H = 1200, 675

IN_CELL, IN_GAP = 68, 6
IN_PITCH = IN_CELL + IN_GAP
IN_X, IN_Y = 64, 200
IN_W = N_IN * IN_CELL + (N_IN - 1) * IN_GAP          # 364

SM_CELL, SM_GAP = 50, 5
SM_PITCH = SM_CELL + SM_GAP
SM_W = N_K * SM_CELL + (N_K - 1) * SM_GAP            # 160

K_X, K_Y = 496, 302
P_X, P_Y = 704, 302

OUT_CELL, OUT_GAP = 68, 6
OUT_PITCH = OUT_CELL + OUT_GAP
OUT_W = N_OUT * OUT_CELL + (N_OUT - 1) * OUT_GAP     # 216
OUT_X, OUT_Y = 928, 274

KERNEL_W = N_K * IN_CELL + (N_K - 1) * IN_GAP        # 216

FONT_UI, FONT_MONO = "1:1", "1:2"


def kernel_xy(r, c):
    return (IN_X + c * IN_PITCH, IN_Y + r * IN_PITCH)


in_xy = kernel_xy


def out_xy(r, c):
    return (OUT_X + c * OUT_PITCH, OUT_Y + r * OUT_PITCH)


def out_center(r, c):
    x, y = out_xy(r, c)
    return (x + OUT_CELL / 2, y + OUT_CELL / 2)


def sum_anchor():
    return (P_X + SM_W / 2, P_Y + SM_W + 30)


# ------------------------------------------------------------- emit utils ---
_id = [100]


def nid():
    _id[0] += 1
    return "1:%d" % _id[0]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _op(o):
    if o is None or (SHOW_ALL and o == 0):
        return ""
    return f' opacity="{o}"'


def rect(x, y, w, h, color, radius=8, name="Cell", opacity=None):
    i = nid()
    return i, (f'<Shape x="{x}" y="{y}" name="{esc(name)}" id="{i}"{_op(opacity)}>'
               f'<Rectangle originX="0" originY="0" width="{w}" height="{h}" '
               f'cornerRadiusTL="{radius}" name="P"/>'
               f'<Fill name="F"><SolidColor colorValue="{color}" name="C"/></Fill>'
               f'</Shape>')


def outline(x, y, w, h, color, thickness=3, radius=10, name="Frame", opacity=None):
    i = nid()
    return i, (f'<Shape x="{x}" y="{y}" name="{esc(name)}" id="{i}"{_op(opacity)}>'
               f'<Rectangle originX="0" originY="0" width="{w}" height="{h}" '
               f'cornerRadiusTL="{radius}" name="P"/>'
               f'<Stroke thickness="{thickness}" name="S">'
               f'<SolidColor colorValue="{color}" name="C"/></Stroke></Shape>')


def text(x, y, w, h, body, size, color, font=FONT_MONO, align="center",
         valign="middle", name="T", opacity=None):
    i, sid = nid(), nid()
    return i, (f'<Text x="{x}" y="{y}" width="{w}" height="{h}" sizingValue="fixed" '
               f'overflowValue="visible" alignValue="{align}" '
               f'verticalAlignValue="{valign}" name="{esc(name)}" id="{i}"'
               f'{_op(opacity)}>'
               f'<TextStylePaint fontSize="{size}" fontAssetId="{font}" name="S" '
               f'id="{sid}"><Fill name="F">'
               f'<SolidColor colorValue="{color}" name="C"/></Fill></TextStylePaint>'
               f'<TextValueRun styleId="{sid}" text="{esc(body)}" name="R"/></Text>')


def group(x, y, name, children, opacity=None):
    i = nid()
    return i, (f'<Node x="{x}" y="{y}" name="{esc(name)}" id="{i}"{_op(opacity)}>'
               + "".join(children) + '</Node>')


CAPTIONS = [
    "An image is just a grid of numbers - bright pixels are high, dark are low.",
    "A filter is a small grid of numbers too. This one has only nine.",
    "Lay it on the image. Multiply each pair, then add all nine results together.",
    "That one number says how strongly this patch matches the filter.",
    "Now slide one step and repeat - reusing the very same nine numbers.",
    "Read it backwards: every output cell came from the 3x3 patch beneath it.",
    "And forwards: one pixel feeds every output whose patch covered it.",
    "Change the nine numbers, and the filter looks for something else entirely.",
    "Only nine positions fit, so the map comes out 3x3 - smaller than the image.",
]


# ------------------------------------------------------------------ build ---
def build():
    body, overlay, ids = [], [], {}

    _, t = text(64, 38, 900, 40, "How a filter turns an image into a feature map",
                27, INK, FONT_UI, align="left", name="Title")
    body.append(t)

    ids["caption"] = []
    for n, cap in enumerate(CAPTIONS):
        i, t = text(64, 84, 1080, 30, cap, 17, INK_MUTED, FONT_UI,
                    align="left", name=f"Cap{n}", opacity=0)
        ids["caption"].append(i)
        body.append(t)

    for key, x, w, y, label in (
            ("lblIn",  IN_X,  IN_W,  IN_Y,  "INPUT   5 x 5"),
            ("lblK",   K_X,   SM_W,  K_Y,   "FILTER   3 x 3"),
            ("lblP",   P_X,   SM_W,  P_Y,   "MULTIPLY"),
            ("lblOut", OUT_X, OUT_W, OUT_Y, "FEATURE MAP   3 x 3")):
        i, t = text(x - 50, y - 36, w + 100, 22, label, 12, INK_DIM, FONT_UI,
                    name=key, opacity=0)
        ids[key] = i
        body.append(t)

    for key, x, w in (("opMul", IN_X + IN_W, K_X - IN_X - IN_W),
                      ("opEq",  K_X + SM_W,  P_X - K_X - SM_W)):
        i, t = text(x, K_Y + SM_W / 2 - 24, w, 48, "x" if key == "opMul" else "=",
                    28, INK_DIM, FONT_UI, name=key, opacity=0)
        ids[key] = i
        body.append(t)

    # ---- input: numbers declared before cells so they paint on top --------
    cells, nums, ids["inNums"] = [], [], []
    for r in range(N_IN):
        for c in range(N_IN):
            v = IMG[r][c]
            col = img_color(v)
            x, y = in_xy(r, c)
            _, sh = rect(x, y, IN_CELL, IN_CELL, col, 8, f"in{r}{c}")
            cells.append(sh)
            i, t = text(x, y, IN_CELL, IN_CELL, str(v), 26, readable_on(col),
                        name=f"inv{r}{c}", opacity=0)
            ids["inNums"].append(i)
            nums.append(t)
    _, g = group(0, 0, "InputNums", nums)
    body.append(g)
    ids["inputGrid"], g = group(0, 0, "InputGrid", cells, opacity=0)
    body.append(g)

    # ---- filters ----------------------------------------------------------
    ids["filterGroups"] = []
    for fi, (fname, k) in enumerate(FILTERS):
        kids = []
        m = max(abs(v) for row in k for v in row)
        for r in range(N_K):
            for c in range(N_K):
                v = k[r][c]
                col = signed_color(v, m)
                x, y = K_X + c * SM_PITCH, K_Y + r * SM_PITCH
                _, sh = rect(x, y, SM_CELL, SM_CELL, col, 6, f"k{r}{c}")
                _, t = text(x, y, SM_CELL, SM_CELL, str(v), 20, readable_on(col),
                            name=f"kv{r}{c}")
                kids += [t, sh]
        _, t = text(K_X - 50, K_Y + SM_W + 16, SM_W + 100, 24, fname, 15,
                    ACCENT, FONT_UI, name="kname")
        kids.insert(0, t)
        i, g = group(0, 0, f"Filter{fi}", kids, opacity=0)
        ids["filterGroups"].append(i)
        body.append(g)

    # ---- products: one group per kernel position, per-cell subgroups ------
    k0 = FILTERS[0][1]
    ids["prodGroups"], ids["prodCells"], ids["prodSums"] = [], [], []
    for pi, (pr, pc) in enumerate(POSITIONS):
        pv = products(k0, pr, pc)
        m = max(abs(v) for row in pv for v in row) or 1
        kids, per = [], []
        for r in range(N_K):
            for c in range(N_K):
                v = pv[r][c]
                col = signed_color(v, m)
                x, y = P_X + c * SM_PITCH, P_Y + r * SM_PITCH
                h = -SM_CELL / 2
                _, sh = rect(h, h, SM_CELL, SM_CELL, col, 6, "bg")
                _, t = text(h, h, SM_CELL, SM_CELL, str(v), 20, readable_on(col),
                            name="v")
                # position 0's cells pop in one at a time (the teaching beat);
                # every later position rides its parent group's fade
                cid, g = group(x + SM_CELL / 2, y + SM_CELL / 2, f"p{r}{c}",
                               [t, sh], opacity=0 if pi == 0 else None)
                per.append(cid)
                kids.append(g)
        ids["prodCells"].append(per)
        i, g = group(0, 0, f"Prod{pi}", kids, opacity=0)
        ids["prodGroups"].append(i)
        body.append(g)

        total = sum(v for row in pv for v in row)
        i, t = text(P_X - 70, P_Y + SM_W + 12, SM_W + 140, 36,
                    f"sum  =  {total}", 21, INK, name=f"psum{pi}", opacity=0)
        ids["prodSums"].append(i)
        body.append(t)

    # ---- feature maps -----------------------------------------------------
    ids["outCells"], ids["outGroups"] = [], []
    for fi, (fname, k) in enumerate(FILTERS):
        out = OUTS[fname]
        m = max(abs(v) for row in out for v in row) or 1
        kids, per = [], []
        for r, c in POSITIONS:
            v = out[r][c]
            col = signed_color(v, m)
            x, y = out_xy(r, c)
            h = -OUT_CELL / 2
            _, sh = rect(h, h, OUT_CELL, OUT_CELL, col, 8, "bg")
            _, t = text(h, h, OUT_CELL, OUT_CELL, str(v), 24, readable_on(col),
                        name="v")
            # filter 0's cells pop in one by one; the others ride their group
            cid, g = group(x + OUT_CELL / 2, y + OUT_CELL / 2, f"o{r}{c}",
                           [t, sh], opacity=0 if fi == 0 else None)
            per.append(cid)
            kids.append(g)
        ids["outCells"].append(per)
        i, g = group(0, 0, f"Out{fi}", kids, opacity=None if fi == 0 else 0)
        ids["outGroups"].append(i)
        body.append(g)

    slots = []
    for r, c in POSITIONS:
        x, y = out_xy(r, c)
        _, sh = outline(x, y, OUT_CELL, OUT_CELL, "FF1C2432", 2, 8, f"slot{r}{c}")
        slots.append(sh)
    ids["slots"], g = group(0, 0, "Slots", slots, opacity=0)
    body.append(g)

    # ---- overlays (declared first => painted on top) ----------------------
    ids["travel"] = []
    for pi, (r, c) in enumerate(POSITIONS):
        v = OUTS["Vertical edge"][r][c]
        _, bgs = rect(-34, -23, 68, 46, "FF0B1018", 12, "chip")
        _, rng = outline(-34, -23, 68, 46, ACCENT, 2, 12, "chipring")
        _, num = text(-46, -23, 92, 46, str(v), 24, ACCENT, name="n")
        i, g = group(0, 0, f"Travel{pi}", [num, rng, bgs], opacity=0)
        ids["travel"].append(i)
        overlay.append(g)

    # arrow that takes the products column's place once the maths is understood
    ay = K_Y + SM_W / 2
    _, shaft = rect(P_X + 34, ay - 2, 62, 4, INK_DIM, 2, "shaft")
    hid = nid()
    head = (f'<Shape x="{P_X + 108}" y="{ay}" rotation="1.5707963" name="head" '
            f'id="{hid}"><Triangle originX="0.5" originY="0.5" width="18" '
            f'height="16" name="P"/><Fill name="F">'
            f'<SolidColor colorValue="{INK_DIM}" name="C"/></Fill></Shape>')
    ids["arrow"], g = group(0, 0, "Arrow", [shaft, head], opacity=0)
    overlay.append(g)

    ids["outRing"], sh = outline(0, 0, OUT_CELL, OUT_CELL, ACCENT, 3, 8,
                                 "OutRing", opacity=0)
    overlay.append(sh)
    ids["inputRing"], sh = outline(0, 0, IN_CELL, IN_CELL, ACCENT, 3, 8,
                                   "InRing", opacity=0)
    overlay.append(sh)

    _, rng = outline(0, 0, KERNEL_W, KERNEL_W, ACCENT, 3, 10, "ring")
    _, tnt = rect(0, 0, KERNEL_W, KERNEL_W, "2622D3EE", 10, "tint")
    ids["kernelFrame"], g = group(IN_X, IN_Y, "KernelFrame", [rng, tnt], opacity=0)
    overlay.append(g)

    return overlay + body, ids


if __name__ == "__main__":
    body, ids = build()
    anim, end = timeline.compose(ids, sys.modules[__name__])
    duration = int(end + 90)
    doc = (
        '<Rive version="1" kind="fragment">\n'
        f'    <Artboard defaultStateMachineId="1:50" styleId="1:51" width="{W}" '
        f'height="{H}" name="Artboard" id="1:52">\n'
        '        <LayoutComponentStyle name="Artboard Style" id="1:51"/>\n'
        f'        <Fill name="Background"><SolidColor colorValue="{BG}" '
        'name="C"/></Fill>\n'
        + "".join("        " + b + "\n" for b in body)
        + "        " + anim.emit("Lesson", "1:53", duration) + "\n"
        '        <StateMachine name="State Machine 1" id="1:50">\n'
        '            <StateMachineLayer name="Layer 1" id="1:54">\n'
        '                <AnyState x="200" y="-120"/><ExitState x="400" y="-120"/>\n'
        '                <EntryState><StateTransition stateToId="1:55"/></EntryState>\n'
        '                <AnimationState x="200" animationId="1:53" id="1:55"/>\n'
        '            </StateMachineLayer>\n'
        '        </StateMachine>\n'
        '    </Artboard>\n'
        f'    <FontAsset file="Inter.ttf" name="Inter" id="{FONT_UI}"/>\n'
        f'    <FontAsset file="JetBrainsMono-Regular.ttf" name="Mono" '
        f'id="{FONT_MONO}"/>\n'
        '</Rive>\n')
    pathlib.Path("scene.rml").write_text(doc)
    print(f"scene.rml  {len(doc):,} bytes | {_id[0] - 100} ids | "
          f"{duration} frames ({duration / 60:.1f}s)")
