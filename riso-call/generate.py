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


def fill(color):
    return el("Fill", {"name": "F"}, [solid(color)])


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
        shape(0, 0, mottle, [fill(alpha("D8CDB5", 0.10))], "mottle"),
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
    fish = []
    for k, (fx, fy, fa, fl) in enumerate(((-40, 60, 2.2, 70), (70, -20, -0.6, 62),
                                          (-30, -150, 0.9, 48))):
        rr = rng_for(f"koi/fish{k}")
        body = []
        for j in range(16):
            t = j / 15
            a = TAU * t
            # teardrop: wide head, tapering tail
            w = 0.34 * (1 - t * 0.0) * math.sin(math.pi * (0.5 + 0.5 * math.cos(a)) ** 0.9)
            u = 0.5 * math.cos(a) * fl
            v = (0.30 * math.sin(a) * (0.55 + 0.45 * (1 + math.cos(a)) / 2)) * fl
            body.append((u, v))
        tail = [(fl * 0.5, 0), (fl * 0.72, -fl * 0.22), (fl * 0.62, 0), (fl * 0.72, fl * 0.22)]
        ca, sa = math.cos(fa), math.sin(fa)
        rot = lambda p: (fx + p[0] * ca - p[1] * sa + rr.uniform(-0.6, 0.6),
                         fy + p[0] * sa + p[1] * ca + rr.uniform(-0.6, 0.6))
        fish.append(points_path(smooth([rot(p) for p in body], True), True))
        fish.append(points_path(poly([rot(p) for p in tail]), True))
    fish_shape = shape(2, 1, fish, [fill(ORANGE)], "koi", blend="multiply")
    return [fish_shape, pad_shape, ring_shape, water]


# --------------------------------------------------------------- timeline ---
OUT_CUBIC = (0.215, 0.61, 0.355, 1)
IN_OUT_CUBIC = (0.645, 0.045, 0.355, 1)
IN_QUAD = (0.55, 0.085, 0.68, 0.53)
EASE_OUT = (0, 0, 0.58, 1)


class Anim:
    X, Y, ROT, SX, SY, OPACITY, THICK = 13, 14, 15, 16, 17, 18, 47

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
def build():
    A = Anim()
    layers = []            # front-to-back

    # --- the dot (always on top)
    dot_xml, dot_ids = the_dot()
    layers += dot_xml

    # --- ripples & ticks (Act I: 0.0 and 0.75; then one per disc beat)
    RIPPLES = [(0.0, BLUE), (0.75, BLUE), (1.5, BLUE), (2.25, BLUE),
               (3.25, BLUE), (4.25, BLUE)]
    for k, (t, ink) in enumerate(RIPPLES):
        rx, rids = ripple(f"ripple{k}", ink, f"ripple{k}", thick=6.5)
        layers.append(rx)
        A.ripple(rids, s(t))
        if t < 1.0:
            tx, tids = ticks(f"ticks{k}", ink, f"ticks{k}")
            layers.append(tx)
            A.flick(tids, s(t) + 14)

    # --- disc 1: koi pond, 1.5 -> 2.25, grows with overshoot
    d1, c1, ids1 = disc("koi", scene_koi())
    layers += [d1]
    clippers = [c1]
    f0, f1 = s(1.5), s(2.25)
    A.hold(ids1["node"], A.OPACITY, 0, 0)
    A.hold(ids1["node"], A.OPACITY, f0, 1)
    A.hold(ids1["node"], A.OPACITY, f1, 0)
    for p in (A.SX, A.SY):
        A.key(ids1["clip"], p, 0, 0.02)
        A.tween(ids1["clip"], p, f0, f0 + 16, 0.02, 1.08, OUT_CUBIC)
        A.tween(ids1["clip"], p, f0 + 16, f0 + 26, 1.08, 1.0, IN_OUT_CUBIC)

    # --- paper grain, behind everything (the cream itself is the artboard fill)
    layers += paper()
    layers += clippers

    duration = s(3.5)
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
