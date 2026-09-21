"""Primitives for authoring a Rive scene as RML from Python.

Import this, build a tree of El() nodes, and write out scene.rml. The `rive`
CLI compiles it. See SKILL.md for the loop and the pitfalls.

Everything here is figure-agnostic — no palette, no layout, no timing baked in.
"""
import math
from collections import OrderedDict, defaultdict
from geom import El, Ids, fmt

# Animatable property keys, as Rive numbers them.
PROP = {"x": 13, "y": 14, "rotation": 15, "scaleX": 16, "scaleY": 17, "opacity": 18}

# Cubic bezier easings. Reach for these before inventing your own.
EASE_FADE = (0.42, 0.00, 0.58, 1.00)   # symmetric — opacity crossfades
EASE_OUT  = (0.16, 0.86, 0.26, 1.00)   # decisive arrival — steps, snaps
EASE_SNAP = (0.20, 0.00, 0.20, 1.00)   # fast in, fast out
EASE_IN_OUT = (0.65, 0.00, 0.35, 1.00)  # pronounced ease both ends

_charsets = defaultdict(set)


def charsets():
    """Glyphs actually used, per font key — feed to subset_fonts.py."""
    return {k: "".join(sorted(v)) for k, v in _charsets.items()}


# ================================================================= animation ==
class Anim:
    """Keyframe registry for one artboard. One instance per artboard."""

    def __init__(self, duration_frames, fps=60):
        self.tracks = OrderedDict()
        self.duration = duration_frames
        self.fps = fps

    def key(self, obj_id, prop, frames):
        """frames: list of (frame, value, ease). ease None == linear,
        "hold" == step, or a 4-tuple cubic."""
        self.tracks.setdefault((obj_id, PROP[prop]), []).extend(frames)

    def fade(self, obj_id, spans):
        """spans: list of (frame, opacity). Applies the standard crossfade ease."""
        self.key(obj_id, "opacity", [(f, v, EASE_FADE) for f, v in spans])

    def linear(self, obj_id, prop, spans):
        """spans: list of (frame, value). Constant velocity — use for marquees."""
        self.key(obj_id, prop, [(f, v, None) for f, v in spans])

    def xml(self, anim_id, name="Loop"):
        a = El("LinearAnimation", reverse=False, loopValue="loop",
               duration=self.duration, fps=self.fps, name=name, id=anim_id)
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


# ===================================================================== paint ==
def solid(color, name="C"):
    return El("SolidColor", reverse=False, colorValue=color, name=name)


def fill(color, rule=None):
    return El("Fill", reverse=False, name="F", fillRule=rule).add(solid(color))


def stroke(color, thickness, cap="butt", join="miter", dash=None):
    """dash: (on_len, off_len) or None."""
    s = El("Stroke", reverse=False, thickness=thickness, cap=cap, join=join, name="S")
    s.add(solid(color))
    if dash:
        d = El("DashPath", reverse=False, name="D")
        d.add(El("Dash", length=dash[0], name="on"))
        d.add(El("Dash", length=dash[1], name="off"))
        s.add(d)
    return s


# ==================================================================== shapes ==
def rect(x, y, w, h, *, r=0, fill_=None, stroke_=None, name="R", id=None, opacity=None):
    """Top-left anchored. stroke_ is a tuple of stroke() args."""
    sh = El("Shape", reverse=False, x=x, y=y, name=name, id=id, opacity=opacity)
    sh.add(El("Rectangle", originX=0, originY=0, width=w, height=h,
              cornerRadiusTL=r or None, name="P"))
    if fill_ is not None:
        sh.add(fill(fill_))
    if stroke_ is not None:
        sh.add(stroke(*stroke_))
    return sh


def ellipse(cx, cy, r, *, fill_=None, stroke_=None, name="E", id=None, opacity=None):
    """Centre anchored."""
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


def poly(points, color, *, name="Poly", closed=True):
    sh = El("Shape", reverse=False, x=0, y=0, name=name)
    p = El("PointsPath", reverse=False, isClosed=closed, name="P")
    for px, py in points:
        p.add(El("StraightVertex", x=round(px, 2), y=round(py, 2)))
    sh.add(p)
    sh.add(fill(color))
    return sh


def curve(points, color, thickness, *, name="Curve", cap="round", smooth=0.35):
    """A smooth open stroke through `points` [(x,y), ...].

    Uses cubic vertices with mirrored tangents, so the result reads as one
    continuous hand-drawn curve rather than a polyline. `smooth` scales the
    control-point reach (0 == polyline, ~0.35 == natural).
    """
    sh = El("Shape", reverse=False, x=0, y=0, name=name)
    p = El("PointsPath", reverse=False, isClosed=False, name="P")
    n = len(points)
    for i, (px, py) in enumerate(points):
        prev = points[max(i - 1, 0)]
        nxt = points[min(i + 1, n - 1)]
        dx, dy = (nxt[0] - prev[0]) * smooth, (nxt[1] - prev[1]) * smooth
        rot = math.atan2(dy, dx)
        dist = math.hypot(dx, dy)
        p.add(El("CubicMirroredVertex", x=round(px, 2), y=round(py, 2),
                 rotation=round(rot, 4), distance=round(dist, 2)))
    sh.add(p)
    sh.add(stroke(color, thickness, cap=cap, join="round"))
    return sh


def edge_fade(x, y, w, h, page_color, *, opaque_at="left"):
    """A page-coloured wash so scrolling content dissolves instead of clipping.

    page_color: the 8-digit ARGB of the background, e.g. "FFF7F7FA".
    opaque_at: the edge content disappears into — "left" or "right".
    """
    sh = El("Shape", reverse=False, x=x, y=y, name="Fade")
    sh.add(El("Rectangle", originX=0, originY=0, width=w, height=h, name="P"))
    f = El("Fill", reverse=False, name="F")
    g = El("LinearGradient", reverse=False, startX=0, startY=0, endX=w, endY=0, name="G")
    ramp = [(0.0, "FF"), (0.30, "D8"), (0.62, "70"), (1.0, "00")]
    if opaque_at == "right":
        ramp = [(1 - p, a) for p, a in ramp][::-1]
    for pos, alpha in ramp:
        g.add(El("GradientStop", colorValue=alpha + page_color[2:], position=round(pos, 4)))
    f.add(g)
    sh.add(f)
    return sh


def grp(name, x=0, y=0, id=None, opacity=None):
    """A Node — the container you translate/rotate/fade as a unit."""
    return El("Node", x=x, y=y, name=name, id=id, opacity=opacity)


# ====================================================================== text ==
def text(x, y, w, h, runs, size, color, font_assets, *, align="center", ls=0,
         font="sans", name="T", vmid=True, ids=None, line_height=None):
    """A text box. runs: str, or [(text, color), ...] for mixed colour.

    IMPORTANT: w/h are a FIXED box with visible overflow — text wider than w
    spills over its neighbours and nothing warns you. Size the box from the
    string with measure() before calling this. See SKILL.md.
    """
    if isinstance(runs, str):
        runs = [(runs, color)]
    t = El("Text", reverse=False, x=x, y=y, width=w, height=h, sizingValue="fixed",
           overflowValue="visible", wrapValue="noWrap", alignValue=align,
           verticalAlignValue="middle" if vmid else "top", name=name)
    styles = []
    for i, (s, c) in enumerate(runs):
        sid = ids()
        styles.append(sid)
        sp = El("TextStylePaint", reverse=False, fontSize=size,
                fontAssetId=font_assets[font], letterSpacing=ls or None,
                lineHeight=line_height, name=f"st{i}", id=sid)
        sp.add(fill(c))
        t.add(sp)
        _charsets[font].update(s)
    for (s, _), sid in zip(runs, styles):
        t.add(El("TextValueRun", styleId=sid, text=s, name="run"))
    return t


_metrics_cache = {}


def measure(s, size, ttf_path, *, letter_spacing=0.0):
    """Advance width of `s` at `size` px in the font at `ttf_path`.

    Call this before text() and size the box from it. This is the single
    highest-value habit in this library: Rive text boxes are fixed-size with
    visible overflow, so an unmeasured string silently overlaps its neighbours
    and the compiler reports zero errors.

    Returns a float in the same units as `size`.
    """
    from fontTools.ttLib import TTFont
    if ttf_path not in _metrics_cache:
        f = TTFont(ttf_path, fontNumber=0, lazy=True)
        cmap = f.getBestCmap()
        hmtx = f["hmtx"]
        upem = f["head"].unitsPerEm
        _metrics_cache[ttf_path] = (cmap, hmtx, upem, f.getGlyphOrder())
    cmap, hmtx, upem, order = _metrics_cache[ttf_path]
    total = 0.0
    for ch in s:
        gname = cmap.get(ord(ch))
        if gname is None:
            gname = order[0]
        try:
            total += hmtx[gname][0]
        except KeyError:
            total += upem * 0.5
    return total / upem * size + letter_spacing * max(len(s) - 1, 0)


def fit_box(s, size, ttf_path, *, letter_spacing=0.0, pad=0.0):
    """Width for a text box that will not clip `s`. Adds `pad` on each side."""
    return measure(s, size, ttf_path, letter_spacing=letter_spacing) + 2 * pad


def verify_glyphs(ttf_map):
    """Assert every character used by text() exists in the font it was set in.

    A missing glyph does NOT fail the Rive compile — `problems.log` says OK and
    the character renders as nothing, so a counter or a label silently vanishes.
    Call this at the end of generation. ttf_map is the {font_key: ttf_path} dict.

    Raises ValueError listing exactly what is missing.
    """
    from fontTools.ttLib import TTFont
    missing = {}
    for key, used in _charsets.items():
        path = ttf_map.get(key)
        if not path:
            missing[key] = f"no TTF path registered for font key {key!r}"
            continue
        cmap = TTFont(path, lazy=True).getBestCmap()
        gone = sorted(c for c in used if ord(c) not in cmap)
        if gone:
            missing[key] = "".join(gone)
    if missing:
        lines = [f"  {k}: {v!r}" for k, v in missing.items()]
        raise ValueError(
            "font is missing glyphs that the scene uses — these would render as "
            "nothing and the Rive compile would still report 0 errors:\n"
            + "\n".join(lines)
        )
