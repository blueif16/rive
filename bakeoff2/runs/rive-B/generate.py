#!/usr/bin/env python3
"""Figure B — Gradient descent finds a minimum.

A loss landscape with two valleys. A marble is released onto it and rolls
downhill under a simulated gravity+damping law, so its vertical position comes
from the curve and its speed comes from the local slope. Four beats, looping.

Run:  ./.venv/bin/python generate.py       -> writes scene.rml + build/charsets.json
Then: rive . --once                         -> writes build/<name>.riv
"""
import json
import math
import pathlib

from geom import El, Ids
import rivelib as R

HERE = pathlib.Path(__file__).parent

# ==================================================================== config ==
PAGE     = "FFF7F7FA"
CREAM    = "FFEDECE1"
INK      = "FF3B3730"
MUTED    = "FFA3A09D"
WARM_DK  = "FF746E63"
WARM_LT  = "FF948778"
ACCENT   = "FFC5683C"
INDIGO   = "FF4B4FDD"
LAVENDER = "FF7C71B5"
EDGE     = "FFD9D3C6"

# palette tokens carrying alpha (same hexes, reduced opacity)
CREAM_SOFT = "FFEDECE1"
HILITE     = "B3EDECE1"   # cream at ~70% — marble specular

W, H = 1200, 600
FPS = 60
T_LOOP = 12.0
DUR_F = round(T_LOOP * FPS)

FONTS = {"serif": "1:2", "italic": "1:3", "sans": "1:4", "sansmed": "1:5"}
TTF = {
    "serif":   str(HERE / "fonts/serif.ttf"),
    "italic":  str(HERE / "fonts/serif-italic.ttf"),
    "sans":    str(HERE / "fonts/sans.ttf"),
    "sansmed": str(HERE / "fonts/sans-medium.ttf"),
}

# vertex y is animatable (StraightVertex > Vertex, key 25) — that is what lets
# the landscape deform continuously instead of cutting between two drawings.
R.PROP["vy"] = 25

# ------------------------------------------------------------------ geometry --
PLOT_L, PLOT_R = 130.0, 1090.0
PLOT_W = PLOT_R - PLOT_L
Y_BASE = 484.0          # loss == 0
Y_SCALE = 300.0         # loss == 1  ->  y = 184
GROUND_Y = 508.0        # where the ground fill is cut off
NV = 81                 # landscape vertices (12px pitch — reads as smooth)

# ------------------------------------------------------------------- timeline --
B1_A, B1_B, B1_END = 0, 78, 160          # breathe A -> B -> A
R2_IN, R2_GO, R2_STOP = 158, 172, 332    # beat 2: released on the right
K2_IN = 316                              # its marker settles
R2_OUT0, R2_OUT1 = 352, 384              # marble + trace dissolve, marker stays
R3_IN, R3_GO, R3_STOP = 348, 360, 514    # beat 3: released on the left
K3_IN = 498
CMP_IN0, CMP_IN1 = 396, 424              # the "well above the minimum" guide
CMP_OUT0, CMP_OUT1 = 520, 548
B3_OUT0, B3_OUT1 = 540, 578              # everything from beats 2-3 clears
M_AC0, M_AC1 = 540, 586                  # beat 4: landscape A -> C
R4_IN, R4_GO, R4_STOP = 582, 594, 660
K4_IN = 646
R4_OUT0, R4_OUT1 = 668, 700
M_CA0, M_CA1 = 676, DUR_F                # landscape C -> A, closing the loop

BEATS = [
    ("A LOSS LANDSCAPE",           0,   B1_END),
    ("RELEASED ON THE RIGHT — STUCK", B1_END, 348),
    ("RELEASED ON THE LEFT — FOUND",  348,    540),
    ("NEW LANDSCAPE — SAME START",    540,    DUR_F),
]

# ================================================================== landscape ==
# Control points are (u, loss). Loss 1 is the top of the frame, 0 the bottom.
# A: deep valley left (0.30), ridge (0.52), shallow valley right (0.75).
CTRL_A = [(0.00, 0.95), (0.10, 0.66), (0.20, 0.34), (0.30, 0.12), (0.41, 0.35),
          (0.52, 0.60), (0.63, 0.44), (0.75, 0.32), (0.87, 0.56), (1.00, 0.92)]
# B: the same landscape breathing — same topology, every extremum nudged.
CTRL_B = [(0.00, 0.91), (0.10, 0.63), (0.20, 0.38), (0.30, 0.16), (0.41, 0.32),
          (0.52, 0.565), (0.63, 0.47), (0.75, 0.295), (0.87, 0.59), (1.00, 0.96)]
# C: a different landscape — one broad basin, its floor far to the left.
CTRL_C = [(0.00, 0.78), (0.12, 0.50), (0.24, 0.30), (0.34, 0.18), (0.45, 0.10),
          (0.58, 0.32), (0.70, 0.50), (0.82, 0.64), (0.91, 0.70), (1.00, 0.76)]

NF = 1601          # fine sampling grid for the field


def _piecewise(ctrl, u):
    if u <= ctrl[0][0]:
        return ctrl[0][1]
    for (u0, l0), (u1, l1) in zip(ctrl, ctrl[1:]):
        if u <= u1:
            t = (u - u0) / (u1 - u0)
            return l0 + (l1 - l0) * t
    return ctrl[-1][1]


def field(ctrl, sigma_u=0.026):
    """Control points -> a smooth loss field sampled on a uniform u grid.

    Linear interpolation followed by a gaussian blur: C-infinity smooth, and it
    keeps the designed ordering of the valley depths, which a spline would not
    guarantee.
    """
    raw = [_piecewise(ctrl, i / (NF - 1)) for i in range(NF)]
    sig = sigma_u * (NF - 1)
    rad = int(3 * sig)
    ker = [math.exp(-0.5 * (k / sig) ** 2) for k in range(-rad, rad + 1)]
    tot = sum(ker)
    ker = [k / tot for k in ker]
    out = []
    for i in range(NF):
        acc = 0.0
        for j, kw in enumerate(ker):
            idx = min(max(i + j - rad, 0), NF - 1)
            acc += raw[idx] * kw
        out.append(acc)
    return out


def loss_at(fld, u):
    u = min(max(u, 0.0), 1.0)
    t = u * (NF - 1)
    i = min(int(t), NF - 2)
    f = t - i
    return fld[i] + (fld[i + 1] - fld[i]) * f


def y_at(fld, x):
    return Y_BASE - loss_at(fld, (x - PLOT_L) / PLOT_W) * Y_SCALE


def dydx(fld, x):
    h = 3.0
    return (y_at(fld, x + h) - y_at(fld, x - h)) / (2 * h)


def verts(fld):
    return [(PLOT_L + PLOT_W * i / (NV - 1), y_at(fld, PLOT_L + PLOT_W * i / (NV - 1)))
            for i in range(NV)]


# ==================================================================== physics ==
G = 2100.0      # px/s^2
DAMP = 3.6      # 1/s
SUB = 6


def simulate(fld, u0, n_frames):
    """Roll a marble from u0 and return its per-frame (x, y) on the surface.

    Acceleration is g*Y'/(1+Y'^2) — the tangential component of gravity mapped
    back onto x — so the marble is fast where the ground is steep and slow where
    it flattens, and the damping term gives it a settle rather than a stop.
    """
    x = PLOT_L + u0 * PLOT_W
    v = 0.0
    dt = 1.0 / (FPS * SUB)
    out = [(x, y_at(fld, x))]
    for _ in range(n_frames):
        for _ in range(SUB):
            g = dydx(fld, x)
            v += (G * g / (1 + g * g) - DAMP * v) * dt
            x += v * dt
            if x < PLOT_L + 6:
                x, v = PLOT_L + 6, 0.0
            if x > PLOT_R - 6:
                x, v = PLOT_R - 6, 0.0
        out.append((x, y_at(fld, x)))
    return out


# ===================================================================== pieces ==
MARBLE_R = 9.5
SIT = MARBLE_R + 1.4        # marble centre sits this far above the surface


def seg_shape(fld, xa, xb, color, thick, sid):
    """One short piece of the traced path, lying exactly on the surface."""
    pts = [(xa + (xb - xa) * k / 6.0, 0.0) for k in range(7)]
    pts = [(px, y_at(fld, px)) for px, _ in pts]
    sh = R.curve(pts, color, thick, name="Tr")
    sh.attrs["id"] = sid
    sh.attrs["opacity"] = 0
    return sh


def trace(fld, samples, f0, color, thick, ids, anim, fade_out_f):
    """Path segments that reveal, in order, as the marble first reaches them."""
    xs = [p[0] for p in samples]
    x_lo, x_hi = min(xs), max(xs)
    span = x_hi - x_lo
    k = max(6, min(46, int(span / 22.0)))
    node = R.grp("Trace")
    rightward = samples[-1][0] > samples[0][0]
    edges = [x_lo + span * i / k for i in range(k + 1)]
    for i in range(k):
        xa, xb = edges[i], edges[i + 1]
        over = (xb - xa) * 0.22
        xc = 0.5 * (xa + xb)
        tp = f0
        for j, (sx, _) in enumerate(samples):
            if (sx >= xc) if rightward else (sx <= xc):
                tp = f0 + j
                break
        sid = ids()
        node.add(seg_shape(fld, max(x_lo, xa - over), min(x_hi, xb + over),
                           color, thick, sid))
        anim.key(sid, "opacity", [(0, 0.0, "hold"), (tp, 0.0, R.EASE_FADE),
                                  (min(tp + 9, fade_out_f - 1), 1.0, "hold"),
                                  (fade_out_f, 0.0, "hold")])
    return node


def marble(ids):
    mid = ids()
    g = R.grp("Marble", id=mid)
    g.add(R.ellipse(0, 0, MARBLE_R, fill_=INDIGO, stroke_=(PAGE, 2.6)))
    g.add(R.ellipse(-3.2, -3.4, 2.6, fill_=HILITE))
    return g, mid


def marker(x, y, color, ids):
    kid = ids()
    g = R.grp("Marker", id=kid, opacity=0)
    g.add(R.line(x, y - 2, x, GROUND_Y - 2, color, 1.1, dash=(4, 5)))
    g.add(R.ellipse(x, y - SIT, 10.5, stroke_=(color, 2.0)))
    g.add(R.ellipse(x, y - SIT, 2.6, fill_=color))
    return g, kid


def label(txt, cx_left, cy, size, color, ids, *, font="sans", ls=0.0,
          right_edge=None):
    w = R.fit_box(txt, size, TTF[font], letter_spacing=ls, pad=8)
    h = size * 1.9
    x = (right_edge - w) if right_edge is not None else cx_left
    return R.text(x, cy - h / 2, w, h, txt, size, color, FONTS,
                  font=font, ls=ls or 0, ids=ids)


def key_frames(anim, obj, samples, f0, step, dy):
    """Sample the simulated path onto keyframes. Linear between samples, so the
    speed profile the physics produced survives into the timeline intact."""
    kx, ky = [], []
    n = len(samples)
    for i in range(0, n, step):
        f = f0 + i
        kx.append((f, round(samples[i][0], 2), None))
        ky.append((f, round(samples[i][1] + dy, 2), None))
    f = f0 + n - 1
    if kx[-1][0] != f:
        kx.append((f, round(samples[-1][0], 2), None))
        ky.append((f, round(samples[-1][1] + dy, 2), None))
    # the last sample holds: the marble must sit still while it dissolves, not
    # drift back toward its release point ahead of the reset keyframe.
    kx[-1] = (kx[-1][0], kx[-1][1], "hold")
    ky[-1] = (ky[-1][0], ky[-1][1], "hold")
    anim.key(obj, "x", kx)
    anim.key(obj, "y", ky)
    return samples[-1]


# ===================================================================== scene ==
def build_scene(ab, anim, ids):
    fa, fb, fc = field(CTRL_A), field(CTRL_B), field(CTRL_C)
    va, vb, vc = verts(fa), verts(fb), verts(fc)

    # --- runs, simulated up front: the layout below depends on where they land
    s2 = simulate(fa, 0.855, R2_STOP - R2_GO)     # right start -> shallow valley
    s3 = simulate(fa, 0.125, R3_STOP - R3_GO)     # left start  -> deep valley
    s4 = simulate(fc, 0.855, R4_STOP - R4_GO)     # same start, new landscape
    end2, end3, end4 = s2[-1], s3[-1], s4[-1]
    print(f"  run2 ends u={(end2[0]-PLOT_L)/PLOT_W:.3f} y={end2[1]:.1f}")
    print(f"  run3 ends u={(end3[0]-PLOT_L)/PLOT_W:.3f} y={end3[1]:.1f}")
    print(f"  run4 ends u={(end4[0]-PLOT_L)/PLOT_W:.3f} y={end4[1]:.1f}")

    # Everything lives in one Stage node. The Artboard is reverse=False (its
    # children paint front-to-back), but R.grp is reverse=True, so inside Stage
    # the first thing added is the backmost — the natural authoring order.
    stage = R.grp("Stage")
    ab.add(stage)
    ab = stage

    # -------------------------------------------------- 1. axes (backmost) --
    axes = R.grp("Axes")
    axes.add(R.line(112, 170, 112, GROUND_Y, MUTED, 1.2))
    axes.add(R.line(112, GROUND_Y, 1098, GROUND_Y, MUTED, 1.2))
    ab.add(axes)

    # ---------------------------------------------- 2. ground fill (cream) --
    gp = El("PointsPath", reverse=False, isClosed=True, name="P")
    gp.add(El("StraightVertex", x=PLOT_L, y=GROUND_Y))
    ground_vids = []
    for (vx, vy) in va:
        vid = ids()
        ground_vids.append(vid)
        gp.add(El("StraightVertex", x=round(vx, 2), y=round(vy, 2), id=vid))
    gp.add(El("StraightVertex", x=PLOT_R, y=GROUND_Y))
    ground = El("Shape", reverse=False, x=0, y=0, name="Ground")
    ground.add(gp)
    ground.add(R.fill(CREAM))
    ab.add(ground)

    # ------------------------------------------------ 3. landscape surface --
    lp = El("PointsPath", reverse=False, isClosed=False, name="P")
    line_vids = []
    for (vx, vy) in va:
        vid = ids()
        line_vids.append(vid)
        lp.add(El("StraightVertex", x=round(vx, 2), y=round(vy, 2), id=vid))
    surf = El("Shape", reverse=False, x=0, y=0, name="Surface")
    surf.add(lp)
    surf.add(R.stroke(INK, 2.6, cap="round", join="round"))
    ab.add(surf)

    # the morph: every vertex of both paths keyed to the same y programme
    for vids in (ground_vids, line_vids):
        for i, vid in enumerate(vids):
            ya, yb, yc = round(va[i][1], 2), round(vb[i][1], 2), round(vc[i][1], 2)
            anim.key(vid, "vy", [
                (B1_A,  ya, R.EASE_IN_OUT),
                (B1_B,  yb, R.EASE_IN_OUT),
                (B1_END, ya, None),
                (M_AC0, ya, R.EASE_IN_OUT),
                (M_AC1, yc, None),
                (M_CA0, yc, R.EASE_IN_OUT),
                (M_CA1, ya, None),
            ])

    # --------------------------------------------------- 4. run 2 — stuck --
    r2 = ids()
    run2 = R.grp("Run2", id=r2, opacity=0)
    run2.add(trace(fa, s2, R2_GO, INDIGO, 3.4, ids, anim, R2_OUT1))
    m2, m2id = marble(ids)
    run2.add(m2)
    ab.add(run2)
    key_frames(anim, m2id, s2, R2_GO, 2, -SIT)
    anim.key(m2id, "x", [(0, round(s2[0][0], 2), "hold"),
                         (R2_OUT1, round(s2[0][0], 2), "hold")])
    anim.key(m2id, "y", [(0, round(s2[0][1] - SIT, 2), "hold"),
                         (R2_OUT1, round(s2[0][1] - SIT, 2), "hold")])
    anim.fade(r2, [(0, 0.0), (R2_IN, 0.0), (R2_IN + 16, 1.0),
                   (R2_OUT0, 1.0), (R2_OUT1, 0.0), (DUR_F, 0.0)])

    k2g, k2 = marker(end2[0], end2[1], LAVENDER, ids)
    ab.add(k2g)
    anim.fade(k2, [(0, 0.0), (K2_IN, 0.0), (K2_IN + 22, 1.0),
                   (R2_OUT0, 1.0), (R2_OUT1, 0.40), (B3_OUT0, 0.40),
                   (B3_OUT1, 0.0), (DUR_F, 0.0)])

    # ------------------------- 5. the comparison guide (beat 3 teaching aid) --
    cmp_id = ids()
    cmpg = R.grp("Compare", id=cmp_id, opacity=0)
    cmpg.add(R.line(end3[0] - 6, end2[1] - SIT, end2[0] - 12, end2[1] - SIT,
                    MUTED, 1.2, dash=(7, 6)))
    cmpg.add(R.line(end3[0], end2[1] - SIT + 3, end3[0], end3[1] - SIT - 11,
                    LAVENDER, 1.2, dash=(4, 5)))
    ab.add(cmpg)
    anim.fade(cmp_id, [(0, 0.0), (CMP_IN0, 0.0), (CMP_IN1, 1.0),
                       (CMP_OUT0, 1.0), (CMP_OUT1, 0.0), (DUR_F, 0.0)])

    # --------------------------------------------------- 6. run 3 — found --
    r3 = ids()
    run3 = R.grp("Run3", id=r3, opacity=0)
    run3.add(trace(fa, s3, R3_GO, INDIGO, 3.4, ids, anim, B3_OUT1))
    m3, m3id = marble(ids)
    run3.add(m3)
    ab.add(run3)
    key_frames(anim, m3id, s3, R3_GO, 2, -SIT)
    anim.key(m3id, "x", [(0, round(s3[0][0], 2), "hold"),
                         (B3_OUT1, round(s3[0][0], 2), "hold")])
    anim.key(m3id, "y", [(0, round(s3[0][1] - SIT, 2), "hold"),
                         (B3_OUT1, round(s3[0][1] - SIT, 2), "hold")])
    anim.fade(r3, [(0, 0.0), (R3_IN, 0.0), (R3_IN + 16, 1.0),
                   (B3_OUT0, 1.0), (B3_OUT1, 0.0), (DUR_F, 0.0)])

    k3g, k3 = marker(end3[0], end3[1], INDIGO, ids)
    ab.add(k3g)
    anim.fade(k3, [(0, 0.0), (K3_IN, 0.0), (K3_IN + 22, 1.0),
                   (B3_OUT0, 1.0), (B3_OUT1, 0.0), (DUR_F, 0.0)])

    # ------------------------------------------ 7. run 4 — new landscape --
    r4 = ids()
    run4 = R.grp("Run4", id=r4, opacity=0)
    run4.add(trace(fc, s4, R4_GO, INDIGO, 3.4, ids, anim, R4_OUT1))
    m4, m4id = marble(ids)
    run4.add(m4)
    ab.add(run4)
    key_frames(anim, m4id, s4, R4_GO, 2, -SIT)
    anim.key(m4id, "x", [(0, round(s4[0][0], 2), "hold"),
                         (R4_OUT1, round(s4[0][0], 2), "hold")])
    anim.key(m4id, "y", [(0, round(s4[0][1] - SIT, 2), "hold"),
                         (R4_OUT1, round(s4[0][1] - SIT, 2), "hold")])
    anim.fade(r4, [(0, 0.0), (R4_IN, 0.0), (R4_IN + 16, 1.0),
                   (R4_OUT0, 1.0), (R4_OUT1, 0.0), (DUR_F, 0.0)])

    k4g, k4 = marker(end4[0], end4[1], INDIGO, ids)
    ab.add(k4g)
    anim.fade(k4, [(0, 0.0), (K4_IN, 0.0), (K4_IN + 20, 1.0),
                   (R4_OUT0, 1.0), (R4_OUT1, 0.0), (DUR_F, 0.0)])

    # ----------------------------------------- 8. the ghost of run 2's start --
    # a hairline tick at the shared release point, so beat 4's "same start"
    # reads as the same place beat 2 started from.
    g_id = ids()
    ghost = R.grp("StartTick", id=g_id, opacity=0)
    ghost.add(R.line(s4[0][0], 172, s4[0][0], GROUND_Y - 2, EDGE, 1.2, dash=(3, 6)))
    ab.add(ghost)
    anim.fade(g_id, [(0, 0.0), (R2_IN, 0.0), (R2_IN + 16, 0.9), (R2_OUT1, 0.9),
                     (B3_OUT0, 0.9), (B3_OUT1, 0.55), (R4_IN, 0.55),
                     (R4_IN + 16, 0.9), (R4_OUT0, 0.9), (R4_OUT1, 0.0),
                     (DUR_F, 0.0)])

    # ------------------------------------------------------------ 9. text --
    ab.add(label("Gradient descent", 130, 58, 27, INK, ids, font="serif"))
    ab.add(label("LOSS", 118, 152, 10, MUTED, ids, font="sansmed", ls=1.7))
    ab.add(label("PARAMETER", 0, 532, 10, MUTED, ids, font="sansmed", ls=1.7,
                 right_edge=1098))

    for i, (txt, f0, f1) in enumerate(BEATS):
        lid = ids()
        g = R.grp(f"Beat{i+1}", id=lid, opacity=0)
        g.add(label(txt, 130, 92, 11.5, LAVENDER, ids, font="sansmed", ls=1.7))
        ab.add(g)
        if i == 0:
            # beat 1 owns frame 0, so it crossfades in over the loop seam
            anim.fade(lid, [(0, 1.0), (f1 - 20, 1.0), (f1, 0.0),
                            (DUR_F - 22, 0.0), (DUR_F, 1.0)])
        else:
            anim.fade(lid, [(0, 0.0), (f0, 0.0), (f0 + 22, 1.0),
                            (f1 - 22, 1.0), (f1 if i < 3 else DUR_F - 4, 0.0),
                            (DUR_F, 0.0)])


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
