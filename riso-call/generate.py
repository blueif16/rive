#!/usr/bin/env python3
"""riso-call — a risograph-style opening, generated as RML.

    python3 generate.py && rive . --once
    node ../.claude/skills/rive-animation/scripts/render/render.mjs \
        --riv=build/riso-call.riv --stills=0.3,1.8,3.0 --stills-dir=/tmp/rc

Everything visible is emitted here from seeded PRNGs (one per element), so a
rebuild is byte-identical and textures never swim. Keyframes live in the Anim
class at the bottom; layout and scene content in the functions above it.

RML rules this file respects (all fail silently):
  * draw order is front-to-back — the FIRST sibling paints on top
  * rotation is radians; animation durations are frames at 60fps
  * an ease belongs on the keyframe that STARTS the segment
"""
import math
import random
import sys

FPS = 60
W = H = 720
CX = CY = 360.0
DIAG = math.hypot(CX, CY)            # 509 — a ripple must pass this
TAU = math.tau

# riso inks, ARGB without '#'
BLUE, PINK, YELLOW, GREEN = "FF0078BF", "FFFF48B0", "FFFFE800", "FF00A95C"
ORANGE, VIOLET, INDIGO, PAPER = "FFFF6C2F", "FF765BA7", "FF2E3192", "FFF2EDE3"

DOT_D = 0.022 * W                   # the dot: 2.2 % of frame width
DISC_D = 0.55 * W                   # a disc: 55 % of frame width
DISC_R = DISC_D / 2


def s(sec):
    return int(round(sec * FPS))


def rng_for(tag):
    return random.Random(f"riso-call/{tag}")


# ------------------------------------------------------------ RML helpers ---
_next = [100]


def nid():
    _next[0] += 1
    return f"0:{_next[0]}"


def f(v):
    if isinstance(v, float):
        t = f"{v:.3f}".rstrip("0").rstrip(".")
        return t if t not in ("", "-0") else "0"
    return str(v)


def el(tag, attrs=None, children=()):
    a = "".join(f' {k}="{v}"' for k, v in (attrs or {}).items() if v is not None)
    kids = "".join(children)
    return f"<{tag}{a}>{kids}</{tag}>" if kids else f"<{tag}{a}/>"


def alpha(hex6, a):
    return "%02X%s" % (max(0, min(255, round(a * 255))), hex6[-6:])


def solid(color):
    return el("SolidColor", {"colorValue": color, "name": "C"})


def fill(color, rule=None):
    return el("Fill", {"name": "F", "fillRule": rule}, [solid(color)])


def stroke(color, thick, cap="round", join="round", sid=None, children=()):
    return el("Stroke", {"thickness": f(thick), "cap": cap, "join": join,
                         "name": "S", "id": sid}, [solid(color), *children])


def shape(x, y, geom, paints, name, sid=None, blend=None, opacity=None, **kw):
    attrs = {"x": f(x), "y": f(y), "name": name, "id": sid,
             "blendModeValue": blend,
             "opacity": None if opacity is None else f(opacity)}
    attrs.update({k: f(v) for k, v in kw.items()})
    return el("Shape", attrs, [*geom, *paints])


def node(x, y, children, name, sid=None, opacity=None, **kw):
    attrs = {"x": f(x), "y": f(y), "name": name, "id": sid,
             "opacity": None if opacity is None else f(opacity)}
    attrs.update({k: f(v) for k, v in kw.items()})
    return el("Node", attrs, children)


def ellipse(w, h=None, x=0, y=0, pid=None):
    h = w if h is None else h
    return el("Ellipse", {"width": f(w), "height": f(h), "x": f(x), "y": f(y),
                          "name": "P", "id": pid})


def rect(w, h, x=0, y=0, ox=0.5, oy=0.5):
    return el("Rectangle", {"width": f(w), "height": f(h), "x": f(x), "y": f(y),
                            "originX": f(ox), "originY": f(oy), "name": "P"})


def smooth(points, closed, tension=1.0):
    """Catmull-Rom tangents -> CubicDetachedVertex list. Hand-drawn feel comes
    from the jitter the caller already put into `points`."""
    n = len(points)
    out = []
    for i, (x, y) in enumerate(points):
        if closed:
            px, py = points[(i - 1) % n]
            nx, ny = points[(i + 1) % n]
        else:
            px, py = points[max(i - 1, 0)]
            nx, ny = points[min(i + 1, n - 1)]
        tx, ty = (nx - px) / 2 * tension, (ny - py) / 2 * tension
        d = math.hypot(tx, ty) / 3
        if d < 1e-6:
            out.append(el("StraightVertex", {"x": f(x), "y": f(y)}))
            continue
        a = math.atan2(ty, tx)
        out.append(el("CubicDetachedVertex", {
            "x": f(x), "y": f(y),
            "inRotation": f(a + math.pi), "inDistance": f(d),
            "outRotation": f(a), "outDistance": f(d)}))
    return out


def poly(points):
    return [el("StraightVertex", {"x": f(x), "y": f(y)}) for x, y in points]


def points_path(verts, closed=False, pid=None, x=0, y=0):
    return el("PointsPath", {"isClosed": "true" if closed else None,
                             "x": f(x), "y": f(y), "name": "P", "id": pid}, verts)


# ------------------------------------------------------------- primitives ---
def ring_points(rng, r=100.0, n=40, wobble=0.03):
    """A circle that is never a perfect circle: low-frequency radius noise."""
    ph = [rng.uniform(0, TAU) for _ in range(3)]
    pts = []
    for i in range(n):
        a = TAU * i / n
        w = (math.sin(2 * a + ph[0]) + 0.6 * math.sin(3 * a + ph[1])
             + 0.35 * math.sin(5 * a + ph[2])) / 1.95
        rr = r * (1 + wobble * w)
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def ripple(name, ink, seed, thick=6.0, cx=CX, cy=CY):
    """Ring at rest radius 100; the timeline scales the PATH (not the shape) so
    stroke thickness stays in screen pixels and is keyed separately."""
    rng = rng_for(seed)
    pid, sid, oid = nid(), nid(), nid()
    xml = shape(cx, cy, [points_path(smooth(ring_points(rng), True), True, pid)],
                [stroke(ink, thick, sid=sid)], name, sid=oid, opacity=0)
    return xml, {"shape": oid, "path": pid, "stroke": sid, "thick": thick}


def ticks(name, ink, seed, radius=300.0):
    """2-3 short parallel arcs near the rim, flicked on by the timeline."""
    rng = rng_for(seed)
    ang = rng.uniform(0, TAU)
    n = rng.choice((2, 3, 3))
    arcs = []
    for k in range(n):
        r = radius + k * 9
        span = rng.uniform(0.07, 0.11)
        pts = []
        for j in range(5):
            a = ang - span + 2 * span * j / 4
            jit = rng.uniform(-0.8, 0.8)
            pts.append(((r + jit) * math.cos(a), (r + jit) * math.sin(a)))
        arcs.append(points_path(smooth(pts, False)))
    oid = nid()
    xml = shape(CX, CY, arcs, [stroke(ink, 2.2)], name, sid=oid, opacity=0)
    return xml, {"shape": oid}


def halftone(seed, ink, coverage, region, bounds, pitch=6.5, angle=15.0,
             name="tone", blend="multiply", dx=0.0, dy=0.0, max_r=None):
    """One Shape holding a dot screen: grid at `angle`, dot radius from the
    coverage function (0..1). Gradients are dot-size ramps; solids are 100 %."""
    rng = rng_for(seed)
    x0, y0, x1, y1 = bounds
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    max_r = max_r or pitch * 0.62
    ext = max(x1 - x0, y1 - y0) * 0.75
    dots = []
    u = -ext
    while u <= ext:
        v = -ext
        while v <= ext:
            x = (x0 + x1) / 2 + u * ca - v * sa
            y = (y0 + y1) / 2 + u * sa + v * ca
            if x0 <= x <= x1 and y0 <= y <= y1 and region(x, y):
                c = coverage(x, y)
                c = max(0.0, min(1.0, c + rng.uniform(-0.04, 0.04)))
                r = math.sqrt(c) * max_r
                if r > 0.45:
                    jx, jy = rng.uniform(-0.35, 0.35), rng.uniform(-0.35, 0.35)
                    dots.append(ellipse(2 * r, 2 * r, x + jx, y + jy))
            v += pitch
        u += pitch
    return shape(dx, dy, dots, [fill(ink)], name, blend=blend)


def in_disc(x, y, r=DISC_R):
    return x * x + y * y <= r * r


def disc_paper():
    """Every disc is its own sheet: opaque cream behind the inks, so a disc
    opening over the previous scene covers it."""
    return shape(0, 0, [ellipse(DISC_D + 8)], [fill(PAPER)], "discPaper")


# ------------------------------------------------------------------ paper ---
def paper():
    """Static grain: speckle, short fibres, faint mottling. Never animated."""
    rng = rng_for("paper")
    speck = [ellipse(rng.uniform(0.8, 2.2), None, rng.uniform(0, W), rng.uniform(0, H))
             for _ in range(650)]
    fibres = []
    for _ in range(170):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a, L = rng.uniform(0, TAU), rng.uniform(5, 14)
        fibres.append(points_path(poly([(x, y), (x + L * math.cos(a), y + L * math.sin(a))])))
    mottle = [ellipse(rng.uniform(140, 300), rng.uniform(120, 260),
                      rng.uniform(0, W), rng.uniform(0, H)) for _ in range(14)]
    return [
        shape(0, 0, speck, [fill(alpha("9C8B6E", 0.30))], "speckle"),
        shape(0, 0, fibres, [stroke(alpha("9C8B6E", 0.16), 0.8, cap="butt")], "fibres"),
        shape(0, 0, mottle, [fill(alpha("D8CDB5", 0.035))], "mottle"),
    ]


def the_dot():
    """Indigo, pinned to the centre, thin pink fringe on the right."""
    oid = nid()
    return [node(CX, CY, [
        shape(0, 0, [ellipse(DOT_D)], [fill(INDIGO)], "dot"),
        shape(1.8, 0.6, [ellipse(DOT_D)], [fill(PINK)], "dotFringe", blend="multiply"),
    ], "theDot", sid=oid)], {"node": oid}


# ------------------------------------------------------------------ discs ---
def disc(name, content, misreg=(0, 0)):
    """A circular window on the dot. Returns (node xml, clipper xml, ids).
    The clipper is a paint-less sibling; its transform is what the timeline keys."""
    nid_, cid = nid(), nid()
    clip = el("ClippingShape", {"sourceId": cid, "name": "clip"})
    body = node(CX, CY, [clip, *content], name, sid=nid_, opacity=0)
    clipper = shape(CX, CY, [ellipse(DISC_D)], [], name + "Clip", sid=cid)
    return body, clipper, {"node": nid_, "clip": cid}


def scene_koi():
    """Koi pond: blue water tint, green lily pads, orange koi, water rings
    spreading from the dot. Inks: blue, green, orange."""
    rng = rng_for("koi")
    R = DISC_R
    water = halftone("koi/water", BLUE,
                     lambda x, y: 0.30 + 0.45 * (math.hypot(x, y) / R) ** 1.5,
                     in_disc, (-R, -R, R, R), pitch=6.5, angle=15, name="water")
    # concentric water rings from the centre: unprinted paper (cream strokes)
    rings = []
    for k, r in enumerate((34, 66, 100, 138)):
        rr = rng_for(f"koi/ring{k}")
        rings.append(points_path(smooth(ring_points(rr, r, 36, 0.02), True), True))
    ring_shape = shape(0, 0, rings, [stroke(alpha("F2EDE3", 0.9), 3.0)], "rings")
    pads = []
    for k, (px, py, pr, rot) in enumerate(((-118, -96, 52, 0.4), (96, -128, 40, 2.4),
                                            (128, 78, 58, 4.0), (-96, 122, 44, 1.6))):
        rr = rng_for(f"koi/pad{k}")
        pts = [(0, 0)]
        for j in range(22):
            a = rot + 0.45 + (TAU - 0.9) * j / 21
            rad = pr * (1 + rr.uniform(-0.03, 0.03))
            pts.append((rad * math.cos(a), rad * math.sin(a)))
        pads.append(points_path(smooth(pts, True, 0.8), True, x=px, y=py))
    pad_shape = shape(-1.5, 2, pads, [fill(GREEN)], "pads", blend="multiply")
    fish, spots = [], []
    for k, (fx, fy, fa, fl) in enumerate(((-44, 66, 2.3, 74), (74, -26, -0.7, 66),
                                          (-34, -146, 1.0, 50))):
        rr = rng_for(f"koi/fish{k}")
        top, bot = [], []
        for j in range(13):
            t = j / 12
            w = 0.23 * fl * math.sqrt(math.sin(math.pi * t) + 1e-6) * (1.15 - 0.55 * t)
            top.append((fl * (t - 0.5), -w))
            bot.append((fl * (t - 0.5), w))
        tail = [(fl * 0.62, -fl * 0.2), (fl * 0.53, 0), (fl * 0.62, fl * 0.2)]
        outline = top + tail + bot[::-1]
        ca, sa = math.cos(fa), math.sin(fa)
        rot = lambda p: (fx + p[0] * ca - p[1] * sa + rr.uniform(-0.5, 0.5),
                         fy + p[0] * sa + p[1] * ca + rr.uniform(-0.5, 0.5))
        fish.append(points_path(smooth([rot(p) for p in outline], True, 0.85), True))
        sx, sy = rot((-fl * 0.1, 0))
        spots.append(ellipse(fl * 0.16, fl * 0.11, sx, sy))
    spot_shape = shape(2, 1, spots, [fill(PAPER)], "koiSpots")
    fish_shape = shape(2, 1, fish, [fill(ORANGE)], "koi", blend="multiply")
    return [spot_shape, fish_shape, pad_shape, ring_shape, water, disc_paper()]


def scene_moon():
    """Cricket silhouetted on a big yellow moon. Inks: violet night, yellow moon,
    orange halftone shading, indigo cricket. The dot lands on the cricket's body."""
    R = DISC_R
    mx, my, mr = 8.0, -6.0, 150.0
    moon_pts = ring_points(rng_for("moon/edge"), mr, 44, 0.012)
    night = shape(0, 0, [ellipse(DISC_D + 4), points_path(smooth(moon_pts, True), True, x=mx, y=my)],
                  [fill(VIOLET, "evenOdd")], "night", blend="multiply")
    rng = rng_for("moon/stars")
    stars = [ellipse(rng.uniform(2, 4), None, *(lambda a, d: (d * math.cos(a), d * math.sin(a)))(
        rng.uniform(0, TAU), rng.uniform(165, 192))) for _ in range(14)]
    star_shape = shape(0, 0, stars, [fill(YELLOW)], "stars")
    moon = shape(2, 1, [points_path(smooth(moon_pts, True), True, x=mx, y=my)],
                 [fill(YELLOW)], "moon", blend="multiply")
    shade = halftone("moon/shade", ORANGE,
                     lambda x, y: ((x - mx) * 0.6 + (y - my) * 0.8) / mr * 0.9 + 0.05,
                     lambda x, y: (x - mx) ** 2 + (y - my) ** 2 <= (mr - 2) ** 2,
                     (mx - mr, my - mr, mx + mr, my + mr), pitch=6.0, angle=45, name="moonShade",
                     dx=-1, dy=2)
    # cricket, facing left, perched at the centre
    rr = rng_for("moon/cricket")
    jit = lambda pts: [(x + rr.uniform(-0.7, 0.7), y + rr.uniform(-0.7, 0.7)) for x, y in pts]
    body = points_path(smooth(jit([(-30, -14), (-4, -20), (24, -14), (44, -2), (40, 10),
                                   (18, 14), (-10, 12), (-32, 2)]), True, 0.9), True)
    head = ellipse(30, 26, -42, -8)
    eye = ellipse(7, 7, -50, -13)
    legs = [
        points_path(smooth(jit([(14, -8), (34, -44), (46, -46), (58, 8), (66, 16)]), False, 0.8)),
        points_path(smooth(jit([(-2, 8), (-8, 30), (-24, 36)]), False)),
        points_path(smooth(jit([(-22, 4), (-36, 26), (-46, 28)]), False)),
        points_path(smooth(jit([(30, 8), (38, 30), (52, 34)]), False)),
    ]
    antennae = [
        points_path(smooth(jit([(-52, -16), (-80, -50), (-104, -86)]), False)),
        points_path(smooth(jit([(-54, -12), (-92, -34), (-124, -44)]), False)),
    ]
    wing = points_path(smooth(jit([(-8, -12), (16, -12), (36, -4)]), False))
    cricket = [
        shape(0, 0, [body, head], [fill(INDIGO)], "cricketBody"),
        shape(0, 0, [eye], [fill(PAPER)], "cricketEye"),
        shape(0, 0, legs, [stroke(INDIGO, 4.5)], "cricketLegs"),
        shape(0, 0, antennae, [stroke(INDIGO, 2.2)], "cricketAntennae"),
        shape(0, 0, [wing], [stroke(PAPER, 2.0)], "cricketWing"),
    ]
    return [*cricket, shade, moon, star_shape, night, disc_paper()]


def scene_jelly():
    """Jellyfish in a deep green-blue sea: blue + green overprint, pink bell,
    trailing tentacles. The dot sits in the bell."""
    R = DISC_R
    rr = rng_for("jelly")
    under_bell = lambda x, y: (x / 86) ** 2 + ((y + 28) / 60) ** 2 < 1
    weed = halftone("jelly/green", GREEN,
                    lambda x, y: 0.12 + 0.8 * (1 - (y + R) / (2 * R)) ** 1.3,
                    lambda x, y: in_disc(x, y) and not under_bell(x, y),
                    (-R, -R, R, R), pitch=6.5, angle=75, name="seaTone", dx=1, dy=-2)
    jit = lambda pts, a=0.8: [(x + rr.uniform(-a, a), y + rr.uniform(-a, a)) for x, y in pts]
    dome = [(-78, 14), (-80, -20), (-58, -62), (-20, -84), (20, -84), (58, -62), (80, -20), (78, 14)]
    scallop = []
    for k in range(5):
        x0 = 78 - k * 39
        scallop += [(x0 - 10, 24), (x0 - 20, 18), (x0 - 30, 24)]
    bell_pts = jit(dome + scallop[:-1])
    bell = points_path(smooth(bell_pts, True, 0.9), True)
    bell_shape = shape(0, 0, [bell], [fill(PINK)], "bell", blend="multiply")
    sea = shape(0, 0, [ellipse(DISC_D + 4), points_path(smooth(bell_pts, True, 0.9), True, x=-2, y=-1)],
                [fill(BLUE, "evenOdd")], "sea", blend="multiply")
    gleam = points_path(smooth(jit([(-56, -30), (-40, -58), (-12, -70)]), False))
    gleam_shape = shape(0, 0, [gleam], [stroke(alpha("F2EDE3", 0.85), 4)], "gleam")
    tents = []
    for k in range(9):
        x0 = -64 + k * 16
        L = rr.uniform(90, 160)
        ph = rr.uniform(0, TAU)
        pts = [(x0 + 9 * math.sin(ph + t * 4.2) * t + rr.uniform(-1, 1), 20 + L * t) for t in
               [j / 7 for j in range(8)]]
        tents.append(points_path(smooth(pts, False)))
    tent_shape = shape(0, 0, tents, [stroke(PINK, 2.6)], "tentacles")
    arms = []
    for x0, L in ((-22, 120), (18, 135)):
        pts = [(x0 + 14 * math.sin(t * 5.5) * t, 22 + L * t) for t in [j / 8 for j in range(9)]]
        arms.append(points_path(smooth(jit(pts), False)))
    arm_shape = shape(0, 0, arms, [stroke(PINK, 6.5)], "oralArms")
    bubbles = [ellipse(rr.uniform(3, 8), None, rr.uniform(-150, 150), rr.uniform(-180, 180))
               for _ in range(11)]
    bub_shape = shape(0, 0, bubbles, [stroke(alpha("F2EDE3", 0.6), 1.5)], "bubbles")
    return [gleam_shape, bell_shape, arm_shape, tent_shape, bub_shape, weed, sea, disc_paper()]


BELL_PROFILE = [(0, -246), (16, -240), (24, -224), (48, -212), (74, -194), (86, -156),
                (90, -96), (96, -28), (110, 44), (126, 96), (142, 122), (146, 134)]


def bell_halfwidth(y):
    for (x0, y0), (x1, y1) in zip(BELL_PROFILE, BELL_PROFILE[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return 0.0


def scene_bell():
    """Temple bell, full-bleed (local coords +-360). Violet bell hung from an
    orange beam; a striker log; blue sound arcs rhyme with the ripples.
    The dot sits on the bell body."""
    rr = rng_for("bell")
    jit = lambda pts, a=1.0: [(x + rr.uniform(-a, a), y + rr.uniform(-a, a)) for x, y in pts]
    glow = halftone("bell/glow", YELLOW,
                    lambda x, y: max(0.0, 1 - math.hypot(x, y) / 330) ** 1.4 * 0.95,
                    lambda x, y: math.hypot(x, y) < 330, (-360, -360, 360, 360),
                    pitch=9.0, angle=0, name="glow", dx=2, dy=2)
    beam = shape(0, -326, [rect(760, 66)], [fill(ORANGE)], "beam", blend="multiply")
    beam_grain = shape(0, -326, [points_path(poly([(-360, y), (360, y + rr.uniform(-3, 3))]))
                                 for y in (-18, -4, 12)], [stroke(alpha("2E3192", 0.55), 1.6, cap="butt")], "beamGrain")
    ropes = shape(0, 0, [points_path(poly(jit([(-22, -294), (-14, -244)]))),
                         points_path(poly(jit([(22, -294), (14, -244)])))],
                  [stroke(INDIGO, 5)], "ropes")
    right = BELL_PROFILE + [(0, 138)]
    outline = right + [(-x, y) for x, y in BELL_PROFILE[::-1][:-1]]
    bell = shape(0, 0, [points_path(smooth(jit(outline, 1.2), True, 0.7), True)],
                 [fill(VIOLET)], "bell", blend="multiply")
    # shading: blue dots down the right side, darkening the violet by overprint
    shade = halftone("bell/shade", BLUE,
                     lambda x, y: max(0.0, x / max(bell_halfwidth(y), 1) - 0.15) * 0.85,
                     lambda x, y: abs(x) < bell_halfwidth(y) - 3 and -244 < y < 134,
                     (-150, -246, 150, 138), pitch=6.5, angle=15, name="bellShade", dx=-2, dy=1)
    bands = shape(0, 0, [points_path(smooth(jit([(-bell_halfwidth(y) + 4, y + 3), (0, y), (bell_halfwidth(y) - 4, y + 3)]), False))
                         for y in (-150, -52, 60)], [stroke(BLUE, 4.5)], "bands", blend="multiply")
    bosses = []
    for row, y in enumerate((-190, -170)):
        for k in range(-3, 4):
            x = k * 18 + (9 if row else 0)
            if abs(x) < bell_halfwidth(y) - 8:
                bosses.append(ellipse(7, 7, x, y))
    boss_shape = shape(0, 0, bosses, [fill(INDIGO)], "bosses")
    lip = shape(0, 0, [points_path(smooth(jit([(-140, 128), (-70, 132), (0, 130), (70, 132), (140, 128)]), False))],
                [stroke(alpha("F2EDE3", 0.7), 3)], "lipGleam")
    striker_id = nid()
    striker = node(0, 0, [
        shape(0, 0, [rect(196, 36, 250, 18)], [fill(ORANGE)], "log", blend="multiply", rotation=-0.04),
        shape(0, 0, [points_path(poly([(206, 2), (206, -294)])), points_path(poly([(294, 6), (294, -294)]))],
              [stroke(INDIGO, 4)], "logRopes"),
        shape(0, 0, [ellipse(28, 28, 158, 20)], [fill(INDIGO)], "logEnd"),
    ], "striker", sid=striker_id)
    arcs_id = nid()
    arcs = []
    for side in (0.0, math.pi):
        for r in (196, 240, 286):
            pts = [((r + rr.uniform(-1.5, 1.5)) * math.cos(side + a), (r + rr.uniform(-1.5, 1.5)) * math.sin(side + a))
                   for a in [-0.44 + 0.88 * j / 8 for j in range(9)]]
            arcs.append(points_path(smooth(pts, False)))
    arc_shape = node(0, 0, [shape(0, 0, arcs, [stroke(BLUE, 5)], "arcs", blend="multiply")], "soundArcs", sid=arcs_id, opacity=0)
    content = [arc_shape, striker, lip, boss_shape, bands, shade, bell, ropes, beam_grain, beam, glow,
               shape(0, 0, [rect(W + 8, H + 8)], [fill(PAPER)], "paperBacking")]
    return content, {"striker": striker_id, "arcs": arcs_id}


# ------------------------------------------------------------- lettering ---
GLYPHS = {
    "f": ([[(40, -88), (30, -96), (20, -88), (17, -60), (17, -20), (18, 14), (24, 28)],
           [(2, -44), (38, -46)]], 44),
    "a": ([[(44, -40), (30, -52), (12, -46), (4, -26), (10, -6), (28, -1), (42, -14),
            (45, -46), (44, -12), (52, 0)]], 56),
    "b": ([[(8, -92), (8, -40), (8, 0), (9, -10), (20, -42), (36, -49), (46, -32),
            (43, -10), (28, 2), (10, -4)]], 54),
    "l": ([[(9, -94), (12, -50), (9, -8), (16, 4), (26, 0)]], 28),
    "e": ([[(6, -26), (40, -26), (38, -44), (20, -53), (4, -36), (4, -16), (18, 0), (40, -5)]], 50),
    "c": ([[(42, -40), (26, -52), (8, -42), (4, -20), (14, -3), (30, 0), (42, -8)]], 48),
    "u": ([[(6, -50), (4, -16), (14, -1), (32, -9), (42, -50), (42, -12), (50, 0)]], 56),
    "d": ([[(44, -40), (28, -52), (8, -44), (4, -22), (14, -4), (34, -8), (44, -38),
            (44, -92), (44, -8), (52, 0)]], 56),
}


def lettering(word, cx, baseline, scale, thick, seed):
    """Single-line glyph strokes revealed by TrimPath. Returns (xml list, trim ids
    in writing order): each glyph is an indigo stroke over a pink misregistered copy."""
    rng = rng_for(seed)
    width = sum(GLYPHS[ch][1] for ch in word) * scale
    x = cx - width / 2
    out, trims = [], []
    for ch in word:
        strokes, adv = GLYPHS[ch]
        jit = [[(px + rng.uniform(-1.4, 1.4), py + rng.uniform(-1.4, 1.4)) for px, py in st] for st in strokes]
        rot = rng.uniform(-0.03, 0.03)
        by = baseline + rng.uniform(-2, 2)
        pair = []
        for ink, dx, dy in ((INDIGO, 0, 0), (PINK, 2.2, 1.4)):
            tid = nid()
            geom = [points_path(smooth(st, False, 0.9)) for st in jit]
            trim = el("TrimPath", {"start": "0", "end": "0", "modeValue": "sequential", "name": "trim", "id": tid})
            out.append(shape(x + dx, by + dy, geom, [stroke(ink, thick, children=[trim])], f"glyph_{ch}",
                             blend="multiply", scaleX=scale, scaleY=scale, rotation=rot))
            pair.append(tid)
        trims.append(pair)
        x += adv * scale
    return out, trims


# --------------------------------------------------------------- timeline ---
OUT_CUBIC = (0.215, 0.61, 0.355, 1)
IN_OUT_CUBIC = (0.645, 0.045, 0.355, 1)
IN_QUAD = (0.55, 0.085, 0.68, 0.53)
EASE_OUT = (0, 0, 0.58, 1)


class Anim:
    X, Y, ROT, SX, SY, OPACITY, THICK, TRIM_END = 13, 14, 15, 16, 17, 18, 47, 115

    def __init__(self):
        self.tracks = {}

    def key(self, oid, prop, frame, value, interp="hold", ease=None):
        self.tracks.setdefault((oid, prop), {})[int(frame)] = (value, interp, ease)

    def tween(self, oid, prop, f0, f1, v0, v1, ease=OUT_CUBIC):
        self.key(oid, prop, f0, v0, "cubic", ease)
        self.key(oid, prop, f1, v1)

    def tween_xy(self, oid, props, f0, f1, v0, v1, ease=OUT_CUBIC):
        for p in props:
            self.tween(oid, p, f0, f1, v0, v1, ease)

    def hold(self, oid, prop, frame, value):
        self.key(oid, prop, frame, value)

    def ripple(self, ids, f0, dur=s(0.6), r_to=5.3):
        p, sh, st = ids["path"], ids["shape"], ids["stroke"]
        self.hold(sh, self.OPACITY, 0, 0)
        self.hold(sh, self.OPACITY, f0, 1)
        self.tween(sh, self.OPACITY, f0 + dur * 0.35, f0 + dur, 1, 0, IN_QUAD)
        self.tween_xy(p, (self.SX, self.SY), f0, f0 + dur, 0.06, r_to, OUT_CUBIC)
        self.tween(st, self.THICK, f0, f0 + dur, ids["thick"], 1.2, OUT_CUBIC)

    def flick(self, ids, f0, dur=9):
        sh = ids["shape"]
        self.hold(sh, self.OPACITY, 0, 0)
        self.hold(sh, self.OPACITY, f0, 1)
        self.hold(sh, self.OPACITY, f0 + dur, 0)

    def emit(self, name, anim_id, duration):
        by_obj = {}
        for (oid, prop), keys in self.tracks.items():
            by_obj.setdefault(oid, {})[prop] = sorted(keys.items())
        out = [el("LinearAnimation", {"duration": duration, "fps": FPS,
                                      "loopValue": "oneShot", "name": name, "id": anim_id})[:-2] + ">"]
        for oid, props in by_obj.items():
            out.append(f'<KeyedObject objectId="{oid}">')
            for prop, keys in props.items():
                out.append(f'<KeyedProperty propertyKey="{prop}">')
                for frame, (value, interp, ease) in keys:
                    kids = []
                    if interp == "cubic":
                        x1, y1, x2, y2 = ease or IN_OUT_CUBIC
                        kids = [el("CubicEaseInterpolator",
                                   {"x1": f(x1), "y1": f(y1), "x2": f(x2), "y2": f(y2)})]
                    out.append(el("KeyFrameDouble", {"value": f(round(value, 4)),
                                                      "interpolationType": interp,
                                                      "frame": frame}, kids))
                out.append("</KeyedProperty>")
            out.append("</KeyedObject>")
        out.append("</LinearAnimation>")
        return "\n".join(out)


# ------------------------------------------------------------------ build ---
def reveal(A, ids, f0, f1, grow=16, settle=10, scale=1.0):
    """Disc opens on the dot with a little overshoot (easeOutBack, as two keys)."""
    A.hold(ids["node"], A.OPACITY, 0, 0)
    A.hold(ids["node"], A.OPACITY, f0, 1)
    A.hold(ids["node"], A.OPACITY, f1, 0)
    for p in (A.SX, A.SY):
        A.key(ids["clip"], p, 0, 0.02)
        A.tween(ids["clip"], p, f0, f0 + grow, 0.02, 1.08, OUT_CUBIC)
        A.tween(ids["clip"], p, f0 + grow, f0 + grow + settle, 1.08, 1.0, IN_OUT_CUBIC)
        A.hold(ids["node"], p, 0, scale)


def build():
    A = Anim()
    layers = []            # front-to-back

    # --- the dot (always on top)
    dot_xml, dot_ids = the_dot()
    layers += dot_xml

    # --- signature (Act VI), on paper, above the discs
    sig_id = nid()
    fable, fable_trims = lettering("fable", CX, 322, 1.35, 6.6, "sig/fable")
    claude, claude_trims = lettering("claude", CX, 466, 0.78, 6.2, "sig/claude")
    pink_dot_id = nid()
    pink_dot = node(CX + 13, CY + 2, [shape(0, 0, [ellipse(DOT_D)], [fill(PINK)], "pinkDot", blend="multiply"),
                                      shape(-1.6, 0.8, [ellipse(DOT_D)], [fill(INDIGO)], "pinkDotFringe", blend="multiply")],
                    "thePinkDot", sid=pink_dot_id, scaleX=0, scaleY=0)
    layers.append(node(0, 0, [*fable, *claude], "signature", sid=sig_id))
    layers.append(pink_dot)

    # --- ripples & ticks: Act I at 0.0 / 0.75, then one per beat, one at the cut
    RIPPLES = [0.0, 0.75, 1.5, 2.25, 3.25, 4.25, 6.0]
    for k, t in enumerate(RIPPLES):
        rx, rids = ripple(f"ripple{k}", BLUE, f"ripple{k}", thick=6.5)
        layers.append(rx)
        A.ripple(rids, s(t))
        if t < 1.0:
            tx, tids = ticks(f"ticks{k}", BLUE, f"ticks{k}")
            layers.append(tx)
            A.flick(tids, s(t) + 14)
    # the pink dot's one small answer
    px, pids = ripple("pinkRing", PINK, "pinkRing", thick=4.0, cx=CX + 13, cy=CY + 2)
    layers.append(px)
    A.ripple(pids, s(7.65), dur=s(0.5), r_to=0.7)

    clippers = []

    # --- disc 4: temple bell, opens on the dot at 4.5 over the jellyfish, dives to full bleed
    bell_content, bell_ids = scene_bell()
    d4, c4, ids4 = disc("bell", bell_content)
    layers.append(d4); clippers.append(c4)
    f0, f1 = s(4.5), s(6.0)
    reveal(A, ids4, f0, f1, scale=0.55)
    dive0, dive1 = s(4.9), s(5.25)
    for p in (A.SX, A.SY):
        A.tween(ids4["node"], p, dive0, dive1, 0.55, 1.0, IN_OUT_CUBIC)
        A.tween(ids4["clip"], p, dive0, dive1, 1.0, 2.9, IN_OUT_CUBIC)
    # strikes: the log swings in, the arcs pulse out
    for k, fs in enumerate((s(4.75), s(5.3), s(5.7))):
        A.tween(bell_ids["striker"], A.X, fs - 8, fs, 0, -34, IN_QUAD)
        A.tween(bell_ids["striker"], A.X, fs, fs + 14, -34, 0, OUT_CUBIC)
        A.hold(bell_ids["arcs"], A.OPACITY, 0, 0)
        A.hold(bell_ids["arcs"], A.OPACITY, fs, 1)
        A.tween(bell_ids["arcs"], A.OPACITY, fs + 6, fs + 26, 1, 0, IN_QUAD)
        A.tween_xy(bell_ids["arcs"], (A.SX, A.SY), fs, fs + 26, 0.9, 1.14, OUT_CUBIC)

    # --- disc 3: jellyfish slides in from the right with a little rotation, 3.5 -> 4.85
    d3, c3, ids3 = disc("jelly", scene_jelly())
    layers.append(d3); clippers.append(c3)
    f0, f1 = s(3.5), s(4.85)
    A.hold(ids3["node"], A.OPACITY, 0, 0)
    A.hold(ids3["node"], A.OPACITY, f0, 1)
    A.hold(ids3["node"], A.OPACITY, f1, 0)
    for oid in (ids3["node"], ids3["clip"]):
        A.tween(oid, A.X, f0, f0 + 27, CX + 820, CX, OUT_CUBIC)
    A.tween(ids3["node"], A.ROT, f0, f0 + 27, 0.5, 0, OUT_CUBIC)

    # --- disc 2: cricket on the moon, flips in like a coin, 2.5 -> 3.25
    d2, c2, ids2 = disc("moon", scene_moon())
    rim_id = nid()
    rim = shape(CX, CY, [ellipse(DISC_D + 6)], [fill(INDIGO)], "moonRim", sid=rim_id, opacity=0)
    layers += [d2, rim]; clippers.append(c2)
    f0, f1 = s(2.5), s(3.25)
    flip = 22
    for oid in (ids2["node"], rim_id):
        A.hold(oid, A.OPACITY, 0, 0)
        A.hold(oid, A.OPACITY, f0, 1)
        A.hold(oid, A.OPACITY, f1, 0)
    for oid in (ids2["node"], ids2["clip"], rim_id):
        A.key(oid, A.SX, 0, 0.02)
        A.tween(oid, A.SX, f0, f0 + flip, 0.02, 1.06, OUT_CUBIC)
        A.tween(oid, A.SX, f0 + flip, f0 + flip + 8, 1.06, 1.0, IN_OUT_CUBIC)
    A.tween(rim_id, A.X, f0, f0 + flip, CX - 14, CX, OUT_CUBIC)

    # --- disc 1: koi pond, 1.5 -> 2.25, grows with overshoot
    d1, c1, ids1 = disc("koi", scene_koi())
    layers.append(d1); clippers.append(c1)
    reveal(A, ids1, s(1.5), s(2.25))

    # --- Act VI: the signature writes itself
    def write(trims, f0, stride, dur):
        for k, (ind, pnk) in enumerate(trims):
            fs = f0 + k * stride
            A.tween(ind, A.TRIM_END, fs, fs + dur, 0, 1, IN_OUT_CUBIC)
            A.tween(pnk, A.TRIM_END, fs + 2, fs + dur + 2, 0, 1, IN_OUT_CUBIC)
    write(fable_trims, s(6.25), 11, 17)
    fd = s(7.4)
    A.tween(dot_ids["node"], A.X, fd, fd + 14, CX, CX - 13, OUT_CUBIC)
    A.tween(dot_ids["node"], A.Y, fd, fd + 14, CY, CY + 2, OUT_CUBIC)
    for p in (A.SX, A.SY):
        A.tween(pink_dot_id, p, fd + 6, fd + 16, 0, 1.15, OUT_CUBIC)
        A.tween(pink_dot_id, p, fd + 16, fd + 24, 1.15, 1.0, IN_OUT_CUBIC)
    write(claude_trims, s(7.9), 8, 13)
    A.tween(sig_id, A.OPACITY, s(9.5), s(9.95), 1, 0, IN_QUAD)
    A.hold(sig_id, A.OPACITY, 0, 1)

    # --- paper grain, behind everything (the cream itself is the artboard fill)
    layers += paper()
    layers += clippers

    duration = s(10.0)
    anim = A.emit("main", "0:6", duration)
    art = "\n".join([
        '<Rive version="1" kind="fragment">',
        f'<Artboard defaultStateMachineId="0:7" width="{W}" height="{H}" name="Artboard" id="0:2">',
        f'<Fill name="Background"><SolidColor colorValue="{PAPER}" name="Color"/></Fill>',
        *layers,
        anim,
        '<StateMachine name="Main" id="0:7"><StateMachineLayer name="Layer 1" id="0:8">',
        '<AnyState x="200" y="-120"/><ExitState x="400" y="-120"/>',
        '<EntryState><StateTransition stateToId="0:12"/></EntryState>',
        '<AnimationState x="200" animationId="0:6" id="0:12"/>',
        '</StateMachineLayer></StateMachine>',
        '</Artboard>',
        '</Rive>'])
    return art


if __name__ == "__main__":
    out = build()
    with open("scene.rml", "w") as fh:
        fh.write(out)
    print(f"scene.rml: {len(out)//1024} KB, {out.count('<Ellipse')} ellipses", file=sys.stderr)
