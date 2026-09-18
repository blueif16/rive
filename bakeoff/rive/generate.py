#!/usr/bin/env python3
"""Emit scene.rml — "A taxonomy of world models" as two Rive artboards.

Two artboards, one timeline shape:

    Desktop  1200x600   three lanes, label card pinned left of each
    Mobile    360x560   the same three lanes, label card stacked above each

Both run a 13.6 s looping LinearAnimation called "Loop" with identical beat
timing, so the web embed can swap artboards at a breakpoint without the
figure meaning anything different.

The knowledge point is the contrast between three *kinds* of output, so each
lane is given a motion signature that cannot be confused with the others:

    Renderer   pictures    a constant-velocity strip whose content is quantised
                           into frames -- smooth carrier, discrete samples
    Simulator  signal      everything continuous: a swinging pendulum, an
                           unbroken trace, a dot gliding on it
    Planner    choices     nothing continuous: the chip row indexes one slot at
                           a time, hold-snap-hold, through a fixed selection ring

Run:  ./.venv/bin/python generate.py   (writes scene.rml and build/charsets.json)
"""

import json
import math
import pathlib
from collections import OrderedDict

from geom import El, Ids, fmt

HERE = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- palette ----
# House style tokens, ARGB.
PAGE = "FFF7F7FA"
PAGE0 = "00F7F7FA"
CREAM = "FFEDECE1"
INK = "FF3B3730"
MUTED = "FFA3A09D"
WARM_DK = "FF746E63"
WARM_LT = "FF948778"
ACCENT = "FFC5683C"
INDIGO = "FF4B4FDD"
LAVENDER = "FF7C71B5"
EDGE = "FFD9D3C6"

GRID = "33A3A09D"   # gridlines, muted at 20%
DASH = "59A3A09D"   # equilibrium dash, muted at 35%
TILE_EDGE = "59746E63"  # film frame border, warm-dk at 35%
ARC = "38A3A09D"    # pendulum swing guide

# ------------------------------------------------------------------ time ----
FPS = 60
T_LOOP = 13.6                      # seconds; four beats of 3.4 s
DUR_F = round(T_LOOP * FPS)        # 816 frames
BEAT_F = DUR_F // 4                # 204
XFADE_F = 32                       # crossfade length, ~0.53 s

# Cubic beziers
EASE_FADE = (0.42, 0.0, 0.58, 1.0)     # symmetric, for opacity crossfades
EASE_STEP = (0.16, 0.86, 0.26, 1.0)    # decisive index step for the planner
EASE_SNAP = (0.2, 0.0, 0.2, 1.0)

PROP = {"x": 13, "y": 14, "rotation": 15, "scaleX": 16, "scaleY": 17, "opacity": 18}

# --------------------------------------------------------------- content ----
ACTIONS = ["scan", "grasp", "lift", "rotate", "move", "place",
           "scan", "lift", "move", "grasp", "rotate", "place"]
N_ACTIONS = len(ACTIONS)           # one full plan cycle == one loop

LANES = [
    ("renders", "OBSERVATIONS", "Renderer", "OUTPUTS OBSERVATIONS"),
    ("simulates", "STATE", "Simulator", "OUTPUTS STATE"),
    ("plans", "ACTIONS", "Planner", "OUTPUTS ACTIONS"),
]

FONTS = {"serif": "1:2", "italic": "1:3", "sans": "1:4", "sansmed": "1:5"}
_charsets = {k: set() for k in FONTS}


# ------------------------------------------------------------ the system ----
A0 = 0.45                   # pendulum amplitude envelope peak, radians
W1 = 2 * math.pi / (T_LOOP / 8)    # 8 swings per loop
W2 = 2 * math.pi / (T_LOOP / 2)    # 2 envelope cycles per loop


def theta(t):
    """Pendulum angle. Both periods divide T_LOOP, so the swing is seamless."""
    amp = A0 * (0.6 + 0.4 * math.cos(W2 * t))
    return amp * math.sin(W1 * t)


def state(t):
    """The plotted quantity x(t): horizontal displacement, normalised to +-1."""
    return math.sin(theta(t)) / math.sin(A0)


# ================================================================ animation ==
class Anim:
    """Keyframe registry for one artboard."""

    def __init__(self):
        self.tracks = OrderedDict()

    def key(self, obj_id, prop, frames):
        """frames: list of (frame, value, ease) -- ease None == linear."""
        self.tracks.setdefault((obj_id, PROP[prop]), []).extend(frames)

    def hold_fade(self, obj_id, spans):
        """spans: list of (frame, opacity) -- crossfade with a shared ease."""
        self.key(obj_id, "opacity", [(f, v, EASE_FADE) for f, v in spans])

    def xml(self, anim_id):
        a = El("LinearAnimation", reverse=False, loopValue="loop", duration=DUR_F,
               fps=FPS, name="Loop", id=anim_id)
        by_obj = OrderedDict()
        for (obj, key), kfs in self.tracks.items():
            by_obj.setdefault(obj, []).append((key, kfs))
        for obj, props in by_obj.items():
            ko = El("KeyedObject", reverse=False, objectId=obj)
            for key, kfs in props:
                kp = El("KeyedProperty", reverse=False, propertyKey=key)
                for frame, value, ease in sorted(kfs, key=lambda k: k[0]):
                    if ease == "hold":
                        kf = El("KeyFrameDouble", reverse=False, value=value,
                                frame=frame, interpolationType="hold")
                    elif ease:
                        kf = El("KeyFrameDouble", reverse=False, value=value,
                                frame=frame, interpolationType="cubic")
                        kf.add(El("CubicEaseInterpolator", x1=ease[0], y1=ease[1],
                                  x2=ease[2], y2=ease[3]))
                    else:
                        kf = El("KeyFrameDouble", reverse=False, value=value,
                                frame=frame, interpolationType="linear")
                    kp.add(kf)
                ko.add(kp)
            a.add(ko)
        return a


# =================================================================== paint ==
def solid(color, name="C"):
    return El("SolidColor", reverse=False, colorValue=color, name=name)


def fill(color, rule=None):
    return El("Fill", reverse=False, name="F", fillRule=rule).add(solid(color))


def stroke(color, thickness, cap="butt", join="miter", dash=None):
    s = El("Stroke", reverse=False, thickness=thickness, cap=cap, join=join, name="S")
    s.add(solid(color))
    if dash:
        d = El("DashPath", reverse=False, name="D")
        d.add(El("Dash", length=dash[0], name="on"))
        d.add(El("Dash", length=dash[1], name="off"))
        s.add(d)
    return s


def rect(x, y, w, h, *, r=0, fill_=None, stroke_=None, name="R", id=None, opacity=None):
    sh = El("Shape", reverse=False, x=x, y=y, name=name, id=id, opacity=opacity)
    sh.add(El("Rectangle", originX=0, originY=0, width=w, height=h,
              cornerRadiusTL=r or None, name="P"))
    if fill_ is not None:
        sh.add(fill(fill_))
    if stroke_ is not None:
        sh.add(stroke(*stroke_))
    return sh


def ellipse(cx, cy, r, *, fill_=None, stroke_=None, name="E", id=None, opacity=None):
    sh = El("Shape", reverse=False, x=cx, y=cy, name=name, id=id, opacity=opacity)
    sh.add(El("Ellipse", originX=0.5, originY=0.5, width=r * 2, height=r * 2, name="P"))
    if fill_ is not None:
        sh.add(fill(fill_))
    if stroke_ is not None:
        sh.add(stroke(*stroke_))
    return sh


def line(x1, y1, x2, y2, color, thickness, *, cap="butt", dash=None, name="L"):
    sh = El("Shape", reverse=False, x=0, y=0, name=name)
    p = El("PointsPath", reverse=False, name="P")
    p.add(El("StraightVertex", x=x1, y=y1))
    p.add(El("StraightVertex", x=x2, y=y2))
    sh.add(p)
    sh.add(stroke(color, thickness, cap=cap, dash=dash))
    return sh


def poly(points, color, *, name="Poly"):
    sh = El("Shape", reverse=False, x=0, y=0, name=name)
    p = El("PointsPath", reverse=False, isClosed=True, name="P")
    for px, py in points:
        p.add(El("StraightVertex", x=round(px, 2), y=round(py, 2)))
    sh.add(p)
    sh.add(fill(color))
    return sh


def fade(x, y, w, h, *, opaque_at):
    """A page-coloured wash so scrolling content fades out instead of clipping.

    opaque_at is "left" or "right": the edge the content disappears into.
    """
    sh = El("Shape", reverse=False, x=x, y=y, name="Fade")
    sh.add(El("Rectangle", originX=0, originY=0, width=w, height=h, name="P"))
    f = El("Fill", reverse=False, name="F")
    g = El("LinearGradient", reverse=False, startX=0, startY=0, endX=w, endY=0, name="G")
    ramp = [(0.0, "FF"), (0.30, "D8"), (0.62, "70"), (1.0, "00")]
    if opaque_at == "right":
        ramp = [(1 - p, a) for p, a in ramp][::-1]
    for pos, alpha in ramp:
        g.add(El("GradientStop", colorValue=alpha + PAGE[2:], position=round(pos, 4)))
    f.add(g)
    sh.add(f)
    return sh


def text(x, y, w, h, runs, size, color, *, align="center", ls=0, font="sans",
         name="T", vmid=True, ids=None, line_height=None):
    """runs: str, or list of (text, color) for a mixed-colour line."""
    if isinstance(runs, str):
        runs = [(runs, color)]
    t = El("Text", reverse=False, x=x, y=y, width=w, height=h, sizingValue="fixed",
           overflowValue="visible", wrapValue="noWrap", alignValue=align,
           verticalAlignValue="middle" if vmid else "top", name=name)
    styles = []
    for i, (s, c) in enumerate(runs):
        sid = ids()
        styles.append(sid)
        sp = El("TextStylePaint", reverse=False, fontSize=size, fontAssetId=FONTS[font],
                letterSpacing=ls or None, lineHeight=line_height,
                name=f"st{i}", id=sid)
        sp.add(fill(c))
        t.add(sp)
        _charsets[font].update(s)
    for (s, _), sid in zip(runs, styles):
        t.add(El("TextValueRun", styleId=sid, text=s, name="run"))
    return t


def grp(name, x=0, y=0, id=None, opacity=None):
    return El("Node", x=x, y=y, name=name, id=id, opacity=opacity)


# ============================================================ lane pieces ==
def film_tile(w, h, phase, sun_r):
    """One frame of the strip: a still picture of a world whose sun has moved on.

    The sun runs an ellipse that stays wholly inside the frame, so the picture
    sequence is continuous across the loop seam instead of snapping back — the
    strip reads as one shot sampled, which is the point of the lane.
    """
    g = grp("Tile")
    yb = h * 0.80                                    # horizon
    ang = 2 * math.pi * phase
    sx = w * 0.5 + w * 0.34 * math.sin(ang)
    sy = h * 0.375 - h * 0.245 * math.cos(ang)

    g.add(rect(0, 0, w, h, fill_=CREAM, name="Sky"))
    g.add(ellipse(sx, sy, sun_r, fill_=ACCENT, name="Sun"))
    g.add(poly([(-2, yb), (w * 0.32, h * 0.54), (w * 0.62, yb)], WARM_LT, name="Far"))
    g.add(poly([(-2, yb), (w * 0.18, h * 0.72), (w * 0.38, h * 0.60),
                (w * 0.56, h * 0.70), (w * 0.78, h * 0.56), (w + 2, yb)],
               WARM_DK, name="Near"))
    g.add(rect(0, yb, w, h - yb, fill_=PAGE, name="Ground"))

    # Perforations: page-on-cream along the top, cream-on-page along the base.
    # Drawn as one dashed stroke per row rather than N rectangles — a 22-tile
    # strip of individual perf shapes cost ~1200 objects on its own.
    s = max(3.6, h * 0.068)
    inset = 3.0
    g.add(line(inset, s * 1.05, w - inset, s * 1.05, PAGE, s,
               dash=(s, s * 1.15), name="perfTop"))
    g.add(line(inset, h - s * 1.05, w - inset, h - s * 1.05, CREAM, s,
               dash=(s, s * 1.15), name="perfBot"))
    g.add(rect(0, 0, w, h, stroke_=(TILE_EDGE, 1), name="Border"))
    return g


def trace_path(pl, pr, pm, amp, v, step=20):
    """The scrolling x(t) curve, in the trace node's local space.

    Local u maps to time tau = u / v, so u = 0 is always "now" at the plot's
    right edge. The node translates from pr to pr - v*T_LOOP across the loop;
    because the path is generated from a T_LOOP-periodic function, the wrap is
    invisible and the trace never restarts.
    """
    u0 = -(pr - pl) - step * 2
    u1 = v * T_LOOP + step * 2
    n = int((u1 - u0) / step) + 1
    pts = []
    for i in range(n):
        u = u0 + i * step
        pts.append((u, pm - state((u / v) % T_LOOP) * amp))

    sh = El("Shape", reverse=False, x=0, y=0, name="TraceShape")
    p = El("PointsPath", reverse=False, name="P")
    for i, (px, py) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        p.add(El("CubicMirroredVertex", x=round(px, 2), y=round(py, 2),
                 rotation=round(math.atan2(dy, dx), 5),
                 distance=round(math.hypot(dx, dy) / 6, 3)))
    sh.add(p)
    sh.add(stroke(INDIGO, 2.6, cap="round", join="round"))
    return sh


# ============================================================== the lanes ==
def build_renderer(cfg, ids, anim, lane):
    """Lane 1 -- a filmstrip: smooth carrier, quantised content."""
    g = grp("RendererContent")
    w, h, pitch = cfg["tile_w"], cfg["tile_h"], cfg["tile_pitch"]
    k = cfg["tile_cycle"]
    span = cfg["mask_r1"] - cfg["strip_x0"] + cfg["scroll_tiles"] * pitch
    n = int(span / pitch) + 3
    top = lane["cy"] - h / 2

    strip_id = ids()
    strip = grp("FilmStrip", x=cfg["strip_x0"], y=top, id=strip_id)
    for j in range(n):
        t = film_tile(w, h, (j % k) / k, cfg["sun_r"])
        t.attrs["x"] = j * pitch
        strip.add(t)
    g.add(strip)

    # One constant-velocity pass; content repeats every `tile_cycle` tiles so
    # the wrap is exact.
    dist = cfg["scroll_tiles"] * pitch
    anim.key(strip_id, "x", [(0, cfg["strip_x0"], None),
                             (DUR_F, cfg["strip_x0"] - dist, None)])
    return g, []


def build_simulator(cfg, ids, anim, lane):
    """Lane 2 -- a pendulum and its live x(t): continuous everywhere."""
    back = grp("SimulatorContent")
    front = grp("SimulatorFront")

    pl, pr = cfg["plot_l"], cfg["plot_r"]
    pm = lane["cy"] + cfg["plot_dy"]
    amp = cfg["plot_amp"]
    v = cfg["plot_v"]
    top, bot = pm - cfg["plot_h"] / 2, pm + cfg["plot_h"] / 2

    # --- behind the fades: gridlines then the trace
    grid = grp("Grid")
    for i in (-1, 1):
        grid.add(line(pl, pm + i * cfg["plot_h"] * 0.31, pr, pm + i * cfg["plot_h"] * 0.31,
                      GRID, 1, name="g"))
    for i in range(1, 5):
        gx = pl + (pr - pl) * i / 5
        grid.add(line(gx, top, gx, bot, GRID, 1, name="gv"))
    grid.add(line(pl, pm, pr + 6, pm, DASH, 1, dash=(5, 6), name="eq"))
    back.add(grid)

    trace_id = ids()
    tn = grp("Trace", x=pr, y=0, id=trace_id)
    tn.add(trace_path(pl, pr, pm, amp, v, step=cfg["trace_step"]))
    back.add(tn)
    anim.key(trace_id, "x", [(0, pr, None), (DUR_F, pr - v * T_LOOP, None)])

    # --- above the fades: axis, labels, the system, the live dot
    axis = grp("Axis")
    axis.add(line(pl, top, pl, bot, EDGE, 1.2, name="ax"))
    axis.add(line(pl + cfg["lab_dx"], top + cfg["lab_dy"],
                  pl + cfg["lab_dx"] + cfg["swatch"], top + cfg["lab_dy"],
                  INDIGO, 2.6, cap="round", name="key"))
    axis.add(text(pl + cfg["lab_dx"] + cfg["swatch"] + 8, top + cfg["lab_dy"] - 10,
                  70, 20, "x(t)", cfg["fs_plot"], INK, align="left", font="sans",
                  ids=ids, name="xt"))
    axis.add(text(pr - 90, bot + 2, 90, 18, "t →", cfg["fs_tick"], MUTED,
                  align="right", ls=1.0, font="sans", ids=ids, name="t"))
    front.add(axis)

    # The system itself. Its rod is one keyed rotation -- nothing quantised.
    px, py = cfg["piv_x"], lane["cy"] + cfg["piv_dy"]
    L, br = cfg["rod_len"], cfg["bob_r"]
    sysg = grp("System")
    arc = El("Shape", reverse=False, x=px, y=py, name="SwingArc")
    ap = El("PointsPath", reverse=False, name="P")
    steps = 14
    for i in range(steps + 1):
        a = -A0 + 2 * A0 * i / steps
        ap.add(El("StraightVertex", x=round(math.sin(a) * L, 2),
                  y=round(math.cos(a) * L, 2)))
    arc.add(ap)
    arc.add(stroke(ARC, 1, cap="round"))
    sysg.add(arc)

    arm_id = ids()
    arm = grp("Arm", x=px, y=py, id=arm_id)
    arm.add(line(0, 0, 0, L, INK, 1.8, cap="round", name="rod"))
    arm.add(ellipse(0, L, br + 5.5, stroke_=("33" + INDIGO[2:], 3), name="halo"))
    arm.add(ellipse(0, L, br, fill_=INDIGO, name="bob"))
    sysg.add(arm)
    sysg.add(ellipse(px, py, cfg["piv_r"], fill_=INK, name="pivot"))
    sysg.add(text(px - 70, py - cfg["sys_dy"], 140, 16, "SYSTEM", cfg["fs_sys"],
                  MUTED, ls=cfg["ls_sys"], font="sansmed", ids=ids, name="sys"))
    front.add(sysg)

    samples = [(f, round(theta(f / FPS), 5), None)
               for f in range(0, DUR_F + 1, cfg["sample_f"])]
    anim.key(arm_id, "rotation", samples)

    dot_id = ids()
    dot = grp("Dot", x=pr, y=pm, id=dot_id)
    dot.add(ellipse(0, 0, br + 6.5, fill_=PAGE, stroke_=("40" + INDIGO[2:], 2),
                    name="dotring"))
    dot.add(ellipse(0, 0, br - 1, fill_=INDIGO, name="dot"))
    front.add(dot)
    anim.key(dot_id, "y", [(f, round(pm - state(f / FPS) * amp, 3), None)
                           for f in range(0, DUR_F + 1, cfg["sample_f"])])
    return back, [front]


def build_planner(cfg, ids, anim, lane):
    """Lane 3 -- a plan: nothing moves continuously, it indexes."""
    back = grp("PlannerContent")
    front = grp("PlannerFront")

    w, h, pitch = cfg["chip_w"], cfg["chip_h"], cfg["chip_pitch"]
    sel_cx = cfg["sel_cx"]
    top = lane["cy"] - h / 2

    # Slot 0 is the selection; chips are laid out to its right and left so the
    # row's resting positions land exactly on it.
    left_slots = int((sel_cx - cfg["mask_l0"]) / pitch) + 1
    x0 = sel_cx - left_slots * pitch
    n = left_slots + N_ACTIONS + 3

    row_id = ids()
    row = grp("ChipRow", x=0, y=top, id=row_id)
    for j in range(n):
        cx = x0 + j * pitch
        word = ACTIONS[(j - left_slots) % N_ACTIONS]
        c = grp("Chip", x=cx - w / 2, y=0)
        c.add(rect(0, 0, w, h, r=cfg["chip_r"], fill_=CREAM,
                   stroke_=(EDGE, 1.2), name="chip"))
        c.add(text(0, 0, w, h, word, cfg["fs_chip"], WARM_DK, font="sans",
                   ids=ids, name="w"))
        row.add(c)
    back.add(row)

    # Index one slot per beat-twelfth: hold, then a short eased step.
    steps = N_ACTIONS
    per = DUR_F / steps
    hold = per - cfg["step_f"]
    kfs = []
    for s in range(steps + 1):
        v = -s * pitch
        t0 = s * per
        kfs.append((round(t0), v, None))
        if s < steps:
            kfs.append((round(t0 + hold), v, EASE_STEP))
    anim.key(row_id, "x", kfs)

    # The selection ring never moves; choices step into it and snap.
    ring_id = ids()
    ring = grp("Ring", x=sel_cx, y=lane["cy"], id=ring_id)
    pad = cfg["sel_pad"]
    ring.add(rect(-(w / 2 + pad), -(h / 2 + pad), w + pad * 2, h + pad * 2,
                  r=cfg["chip_r"] + pad, stroke_=(INDIGO, 1.6), name="ring"))
    ring.add(rect(-cfg["tick_w"] / 2, h / 2 + pad + cfg["tick_gap"],
                  cfg["tick_w"], 2.4, r=1.2, fill_=INDIGO, name="tick"))
    front.add(ring)

    # The ring pops on the landing frame, not across the slide, so the arrival
    # reads as a click rather than a swell.
    snap = []
    for s in range(steps + 1):
        land = s * per
        snap.append((round(land - 4), 1.0, EASE_SNAP))
        snap.append((round(land), cfg["snap"], EASE_SNAP))
        snap.append((round(land + cfg["snap_f"]), 1.0, EASE_FADE))
    snap = [k for k in snap if 0 <= k[0] <= DUR_F]
    anim.key(ring_id, "scaleX", snap)
    anim.key(ring_id, "scaleY", list(snap))
    return back, [front]


# ============================================================== artboard ==
def build_artboard(name, cfg, ab_id, sm_id, anim_id, ids):
    anim = Anim()
    ab = El("Artboard", reverse=False, name=name, id=ab_id, x=cfg["stage_x"], y=0,
            width=cfg["W"], height=cfg["H"], defaultStateMachineId=sm_id,
            styleId=cfg["style_id"], clip=True)
    ab.add(El("LayoutComponentStyle", name=f"{name} Style", id=cfg["style_id"]))
    ab.add(El("Fill", reverse=False, name="Background").add(solid(PAGE)))

    body = []          # painter order, back to front; reversed at the end
    builders = [build_renderer, build_simulator, build_planner]

    # Rive multiplies a group's opacity into each drawable rather than
    # compositing the group as one layer, so a page-coloured mask nested inside
    # a fading lane goes translucent exactly when it is needed and the
    # scrolling content leaks past it. The masks therefore sit in their own
    # never-faded layer between each lane's streaming content and its
    # foreground. They are page-on-page wherever their lane is dark, so they
    # cost nothing visually when the lane is out.
    masks = grp("Masks")
    fronts = []

    for i, (fn, (obj, out, title, sub)) in enumerate(zip(builders, LANES)):
        lane = cfg["lanes"][i]
        content, above = fn(cfg, ids, anim, lane)

        back_id, front_id = ids(), ids()
        bg = grp(f"Lane{i + 1}Stream", id=back_id).add(content)
        fg = grp(f"Lane{i + 1}Front", id=front_id)
        for a in above:
            fg.add(a)
        fg.add(lane_card(cfg, lane, obj, out, ids))

        ly, lh = lane["cy"] - cfg["lane_h"] / 2 - 12, cfg["lane_h"] + 24
        m = cfg["sim_masks"] if i == 1 else cfg["masks"]
        masks.add(rect(-8, ly, m["l0"] + 8, lh, fill_=PAGE, name="MaskL"))
        masks.add(fade(m["l0"], ly, m["l1"] - m["l0"], lh, opaque_at="left"))
        if m.get("r0") is not None:
            masks.add(fade(m["r0"], ly, m["r1"] - m["r0"], lh, opaque_at="right"))
        masks.add(rect(m["r1"], ly, cfg["W"] - m["r1"] + 8, lh, fill_=PAGE,
                       name="MaskR"))

        body.append(bg)
        fronts.append(fg)

        # Beat choreography: lane i is lit in beat 1 and in its own solo beat.
        on = {0, i + 1}
        spans = []
        for b in range(4):
            lit = 1.0 if b in on else 0.0
            nxt = 1.0 if ((b + 1) % 4) in on else 0.0
            start, end = b * BEAT_F, (b + 1) * BEAT_F
            spans.append((start, lit))
            if lit != nxt:
                spans.append((end - XFADE_F, lit))
                spans.append((end, nxt))
        spans.append((DUR_F, 1.0 if 0 in on else 0.0))
        for node_id in (back_id, front_id):
            anim.hold_fade(node_id, dedupe(spans))

    body.append(masks)
    body.extend(fronts)

    for i, (_, _, title, sub) in enumerate(LANES):
        t_id = ids()
        # The title takes the middle row, except when the middle lane is the
        # subject -- then it takes the top row. Nothing else ever moves.
        row = cfg["lanes"][0 if i == 1 else 1]
        tg = grp(f"Title{i + 1}", id=t_id, opacity=0)
        tg.add(text(cfg["W"] / 2 - 300, row["cy"] + cfg["title_dy"], 600,
                    cfg["fs_title"] * 1.5, title, cfg["fs_title"], INK,
                    font="serif", ids=ids, name="title"))
        tg.add(text(cfg["W"] / 2 - 300, row["cy"] + cfg["sub_dy"], 600, 22, sub,
                    cfg["fs_sub"], INDIGO, ls=cfg["ls_sub"], font="sansmed",
                    ids=ids, name="sub"))
        body.append(tg)
        b = i + 1
        anim.hold_fade(t_id, [(0, 0.0), (b * BEAT_F - XFADE_F, 0.0), (b * BEAT_F, 1.0),
                              ((b + 1) * BEAT_F - XFADE_F, 1.0),
                              ((b + 1) * BEAT_F, 0.0), (DUR_F, 0.0)])

    for el in body[::-1]:
        ab.add(el)

    sm = El("StateMachine", reverse=False, name="Main", id=sm_id)
    layer = El("StateMachineLayer", reverse=False, name="Layer 1", id=ids())
    st_id = ids()
    layer.add(El("AnyState", x=400, y=0))
    layer.add(El("ExitState", x=560, y=0))
    layer.add(El("EntryState", x=0, y=16).add(
        El("StateTransition", stateToId=st_id)))
    layer.add(El("AnimationState", x=200, y=0, animationId=anim_id, id=st_id))
    sm.add(layer)
    ab.add(sm)
    ab.add(anim.xml(anim_id))
    return ab


def dedupe(spans):
    out = []
    for f, v in sorted(spans, key=lambda s: s[0]):
        if out and out[-1][0] == f:
            out[-1] = (f, v)
        else:
            out.append((f, v))
    return out


def lane_card(cfg, lane, obj, out, ids):
    """The pinned label card: serif italic object name over a tracked caption."""
    c = grp("Card")
    if cfg["card_fill"]:
        c.add(rect(lane["card_x"], lane["card_y"], cfg["card_w"], cfg["card_h"],
                   fill_=CREAM, name="CardBg"))
    cx = lane["card_x"]
    c.add(text(cx, lane["card_y"] + cfg["name_dy"], cfg["card_w"],
               cfg["fs_name"] * 1.4, obj, cfg["fs_name"], INK, font="italic",
               ids=ids, name="name"))
    c.add(text(cx, lane["card_y"] + cfg["out_dy"], cfg["card_w"], 18,
               [("→ ", MUTED), (out, LAVENDER)], cfg["fs_out"], MUTED,
               ls=cfg["ls_out"], font="sansmed", ids=ids, name="out"))
    return c


# ================================================================= layouts ==
def desktop():
    W, H = 1200, 600
    lane_h, card_w, card_h = 148, 186, 148
    cys = [138, 300, 462]
    cfg = {
        "W": W, "H": H, "stage_x": 0, "style_id": "1:6", "lane_h": lane_h,
        "card_w": card_w, "card_h": card_h, "card_fill": True,
        "lanes": [{"cy": cy, "card_x": 56, "card_y": cy - card_h / 2} for cy in cys],
        "masks": {"l0": 242, "l1": 424, "r0": 1030, "r1": 1140},
        "sim_masks": {"l0": 470, "l1": 566, "r0": None, "r1": 1141},
        # type
        "fs_name": 34, "name_dy": 40, "fs_out": 11, "ls_out": 1.7, "out_dy": 86,
        "fs_title": 46, "title_dy": -40, "fs_sub": 13, "ls_sub": 2.3, "sub_dy": 22,
        "fs_chip": 17, "fs_plot": 12, "fs_tick": 10, "fs_sys": 10, "ls_sys": 1.5,
        # renderer
        "tile_w": 118, "tile_h": 98, "tile_pitch": 136, "tile_cycle": 12,
        "sun_r": 8, "strip_x0": 180, "scroll_tiles": 12, "mask_r1": 1140,
        # simulator
        "piv_x": 340, "piv_dy": -52, "piv_r": 3.6, "rod_len": 78, "bob_r": 13,
        "sys_dy": 22, "plot_l": 470, "plot_r": 1140, "plot_dy": 2, "plot_h": 112,
        "plot_amp": 44, "plot_v": 140, "trace_step": 20, "sample_f": 4,
        "lab_dx": 16, "lab_dy": 12, "swatch": 15,
        # planner
        "chip_w": 112, "chip_h": 74, "chip_pitch": 128, "chip_r": 14,
        "sel_cx": 968, "sel_pad": 7, "tick_w": 26, "tick_gap": 9,
        "mask_l0": 242, "step_f": 18, "snap": 1.05, "snap_f": 11,
    }
    return cfg


def medium():
    """Tablet / narrow-desktop band. Same lane grammar as Desktop, smaller."""
    W, H = 700, 440
    lane_h, card_w, card_h = 108, 142, 108
    cys = [100, 220, 340]
    return {
        "W": W, "H": H, "stage_x": 1320, "style_id": "1:7", "lane_h": lane_h,
        "card_w": card_w, "card_h": card_h, "card_fill": True,
        "lanes": [{"cy": cy, "card_x": 32, "card_y": cy - card_h / 2} for cy in cys],
        "masks": {"l0": 174, "l1": 282, "r0": 592, "r1": 668},
        "sim_masks": {"l0": 306, "l1": 366, "r0": None, "r1": 669},
        "fs_name": 25, "name_dy": 26, "fs_out": 10, "ls_out": 1.5, "out_dy": 69,
        "fs_title": 36, "title_dy": -32, "fs_sub": 11.5, "ls_sub": 1.9, "sub_dy": 17,
        "fs_chip": 15, "fs_plot": 11, "fs_tick": 9, "fs_sys": 9, "ls_sys": 1.3,
        "tile_w": 84, "tile_h": 70, "tile_pitch": 97, "tile_cycle": 12,
        "sun_r": 6, "strip_x0": 100, "scroll_tiles": 12, "mask_r1": 668,
        "piv_x": 222, "piv_dy": -38, "piv_r": 3, "rod_len": 56, "bob_r": 10,
        "sys_dy": 17, "plot_l": 306, "plot_r": 668, "plot_dy": 2, "plot_h": 84,
        "plot_amp": 32, "plot_v": 105, "trace_step": 18, "sample_f": 4,
        "lab_dx": 12, "lab_dy": 10, "swatch": 13,
        "chip_w": 82, "chip_h": 54, "chip_pitch": 94, "chip_r": 11,
        "sel_cx": 540, "sel_pad": 6, "tick_w": 20, "tick_gap": 7,
        "mask_l0": 174, "step_f": 18, "snap": 1.05, "snap_f": 11,
    }


def mobile():
    W, H = 360, 560
    lane_h, card_w, card_h = 88, 158, 58
    tops = [20, 202, 384]
    cfg = {
        "W": W, "H": H, "stage_x": 2160, "style_id": "1:14", "lane_h": lane_h,
        "card_w": card_w, "card_h": card_h, "card_fill": True,
        "lanes": [{"cy": t + 70 + lane_h / 2, "card_x": 20, "card_y": t}
                  for t in tops],
        "masks": {"l0": 20, "l1": 80, "r0": 282, "r1": 340},
        "sim_masks": {"l0": 104, "l1": 162, "r0": None, "r1": 333},
        "fs_name": 24, "name_dy": 6, "fs_out": 10, "ls_out": 1.25, "out_dy": 34,
        "fs_title": 32, "title_dy": -64, "fs_sub": 11, "ls_sub": 1.8, "sub_dy": -20,
        "fs_chip": 14, "fs_plot": 10, "fs_tick": 9, "fs_sys": 8.5, "ls_sys": 1.1,
        "tile_w": 78, "tile_h": 66, "tile_pitch": 90, "tile_cycle": 12,
        "sun_r": 5.5, "strip_x0": 40, "scroll_tiles": 12, "mask_r1": 340,
        "piv_x": 54, "piv_dy": -26, "piv_r": 2.8, "rod_len": 42, "bob_r": 8.5,
        "sys_dy": 16, "plot_l": 104, "plot_r": 332, "plot_dy": 2, "plot_h": 76,
        "plot_amp": 29, "plot_v": 76, "trace_step": 16, "sample_f": 4,
        "lab_dx": 10, "lab_dy": 9, "swatch": 11,
        "chip_w": 70, "chip_h": 48, "chip_pitch": 80, "chip_r": 10,
        "sel_cx": 220, "sel_pad": 5, "tick_w": 18, "tick_gap": 6,
        "mask_l0": 20, "step_f": 18, "snap": 1.06, "snap_f": 11,
    }
    return cfg


# ==================================================================== main ==
def main():
    ids = Ids(client=1, start=20)
    root = El("Rive", reverse=False, version="1", kind="fragment")
    root.add(El("FontAsset", file="fonts/serif.ttf", name="serif", id=FONTS["serif"]))
    root.add(El("FontAsset", file="fonts/serif-italic.ttf", name="serifItalic",
                id=FONTS["italic"]))
    root.add(El("FontAsset", file="fonts/sans.ttf", name="sans", id=FONTS["sans"]))
    root.add(El("FontAsset", file="fonts/sans-medium.ttf", name="sansMedium",
                id=FONTS["sansmed"]))
    root.add(build_artboard("Desktop", desktop(), "1:8", "1:10", "1:12", ids))
    root.add(build_artboard("Medium", medium(), "1:9", "1:11", "1:13", ids))
    root.add(build_artboard("Mobile", mobile(), "1:15", "1:16", "1:17", ids))

    (HERE / "scene.rml").write_text(root.xml() + "\n")
    (HERE / "build").mkdir(exist_ok=True)
    (HERE / "build" / "charsets.json").write_text(
        json.dumps({k: "".join(sorted(v)) for k, v in _charsets.items()},
                   ensure_ascii=False, indent=1))
    n = (HERE / "scene.rml").read_text().count("<")
    print(f"scene.rml  {len(root.xml()) / 1024:.0f} KB  ~{n} elements  "
          f"{DUR_F} frames @ {FPS}fps")
    for k, v in _charsets.items():
        print(f"  {k:9s} {len(v):3d} glyphs")


if __name__ == "__main__":
    main()
