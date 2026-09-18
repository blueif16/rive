#!/usr/bin/env python3
"""The teacher character: renumber, recolour, dock.

`teacher.rml` is a complete 1000x1000 `<Artboard name="Teacher">` decoded out of
a compiled `.riv` — its own paths, bones, blink and head-sway state machine, and
no background fill. It goes into the lesson unchanged in shape: emitted as a
SIBLING artboard, then placed with a `<NestedArtboard>` in the lesson artboard.

Three things have to happen on the way in, and all three fail silently:

  * ids collide. teacher.rml numbers everything `1:N`, and so does generate.py
    (fonts at 1:1/1:2, the machine at 1:50..1:55, content from 1:101 up). Ids
    share ONE namespace across the whole document, so every teacher id moves to
    client 2 — `1:N` -> `2:N`. `renumber()` asserts nothing `1:` survives.
  * the drawing is black-on-white and the stage is FF080B11. `recolour()`
    inverts it, by STRUCTURE rather than by id, so the mapping survives a
    re-extraction of teacher.rml.
  * hair and eyes are the same FF000000 in the source. Left equal, the hair —
    a large mass — becomes the brightest thing in a frame whose subject is the
    grid. Hair is held at HAIR, the two 17px eye dots go to full INK.

Nothing here knows about the lesson's layout; it takes the band it is docked in
as four numbers and works the placement out from the character's own bounds.
"""

import pathlib
import re
import xml.etree.ElementTree as ET

SRC = pathlib.Path(__file__).with_name("teacher.rml")

# --------------------------------------------------------------- palette ---
INK    = "FFF2F6FB"   # every outline, and the eyes
FACE   = "FF121823"   # face / ear / nose fills, one notch off the background
HAIR   = "FFC9D4E3"   # dimmed, so the hair mass never outshines the diagram
SHADOW = "26F2F6FB"   # the black-on-white shadows, inverted to low-alpha white

CLIENT = 2            # the id client the teacher's objects move to

# ---------------------------------------------------------------- bounds ---
# Measured off a render of teacher.rml on its own at 1000x1000 (the union over
# t = 0.2 .. 8.0s, so the head sway and the blink are both inside it), NOT
# derived from the path data — the rig's bones move the artwork off its
# authored coordinates.
SRC_X0, SRC_X1 = 325.0, 671.0
SRC_Y0, SRC_Y1 = 204.0, 694.0
SRC_W, SRC_H = SRC_X1 - SRC_X0, SRC_Y1 - SRC_Y0

# ------------------------------------------------------------- placement ---
TARGET_H = 165.0      # how tall the character stands in the lesson
MARGIN   = 56.0       # air between the character and the frame edge
FEET_Y   = 664.0      # where it stands — 11px under it, band ends at 675
HOP      = 44.0       # how high the arc lifts it when crossing between docks

# where the teacher artboard sits on the editor's stage, clear of the lesson's
STAGE_X, STAGE_Y = 1300, 0


def scale():
    return TARGET_H / SRC_H


def width():
    return SRC_W * scale()


# The rig Node's origin is the character's FEET CENTRE, not its top-left, so
# that moving it is one x, leaning it is one rotation, and mirroring it is
# scaleX=-1 without the character sliding sideways as it flips.
def nested_origin():
    """NestedArtboard x/y inside the rig node."""
    s = scale()
    return (-(SRC_X0 + SRC_X1) / 2 * s, -SRC_Y1 * s)


def dock(side, frame_w=1200.0):
    """Feet-centre of the left or right dock, in lesson coordinates."""
    half = width() / 2
    return (MARGIN + half) if side == "L" else (frame_w - MARGIN - half)


def bounds(side="L"):
    """Where the character lands, for a layout check."""
    cx, half = dock(side), width() / 2
    return (cx - half, cx + half, FEET_Y - TARGET_H, FEET_Y)


def apex_top():
    """Highest the head reaches, at the top of a dock-to-dock arc.

    The crossing is the only time the character leaves its band, so this is the
    number that has to be checked against the diagram — and the one thing no
    layout box can constrain, since a transform is by definition an excursion
    out of the flow."""
    return FEET_Y - HOP - TARGET_H


# ---------------------------------------------------------------- colour ---
EYE_MAX = 24.0        # a 4-vertex path no bigger than this is an eye dot


def _vbox(points_path):
    xs = [float(v.get("x", 0)) for v in points_path]
    ys = [float(v.get("y", 0)) for v in points_path]
    if not xs:
        return 0.0, 0.0
    return max(xs) - min(xs), max(ys) - min(ys)


def colour_map(path=SRC):
    """{SolidColor id -> new ARGB}, classified by structure.

    The eyes are found the only way that survives re-extraction: they are the
    Fill'd Shapes whose PointsPath has exactly four vertices spanning under
    EYE_MAX in both directions (17x17). Every other 4-vertex path in the file
    is a hair puff, 100px across or more.
    """
    artboard = ET.parse(str(path)).getroot().find("Artboard")
    out, eyes = {}, []
    for shape in artboard.iter("Shape"):
        pts = shape.find("PointsPath")
        w, h = _vbox(pts) if pts is not None else (0.0, 0.0)
        dot = (pts is not None and len(list(pts)) == 4
               and w <= EYE_MAX and h <= EYE_MAX)
        for paint in shape:
            if paint.tag not in ("Fill", "Stroke"):
                continue
            for sc in paint.iter("SolidColor"):
                cid, col = sc.get("id"), sc.get("colorValue", "")
                if col[:2] != "FF":                     # a shadow: invert it
                    out[cid] = SHADOW
                elif paint.tag == "Stroke" and col == "FF000000":
                    out[cid] = INK
                elif col == "FFFFFFFF":
                    out[cid] = FACE
                elif col == "FF000000":
                    out[cid] = INK if dot else HAIR
                    if dot:
                        eyes.append(cid)
                else:
                    raise SystemExit(f"mascot: unclassified {col} on {cid}")
    if len(eyes) != 2:
        raise SystemExit(f"mascot: expected 2 eye dots, found {eyes}")
    return out, eyes


_ID_ATTR = re.compile(r'\b(\w*[Ii]d)="1:(\d+)"')
_SOLID = re.compile(r'<SolidColor colorValue="([0-9A-Fa-f]{8})" id="1:(\d+)"\s*/>')


def artboard_rml(path=SRC):
    """The Teacher artboard, recoloured and renumbered, ready to splice in."""
    raw = pathlib.Path(path).read_text()
    cmap, _ = colour_map(path)

    def repaint(m):
        cid = "1:" + m.group(2)
        return f'<SolidColor colorValue="{cmap[cid]}" id="{cid}"/>'

    raw, n = _SOLID.subn(repaint, raw)
    if n != len(cmap):
        raise SystemExit(f"mascot: repainted {n} of {len(cmap)} SolidColors")

    start = raw.index("<Artboard ")
    end = raw.rindex("</Artboard>") + len("</Artboard>")
    frag = _ID_ATTR.sub(rf'\1="{CLIENT}:\2"', raw[start:end])
    if '"1:' in frag:
        raise SystemExit("mascot: an id still in client 1 after renumbering")
    # isComponent is what makes an artboard nestable at all; x/y only keep it
    # from stacking on the lesson when the file is opened in the editor
    head = f'<Artboard isComponent="true" x="{STAGE_X}" y="{STAGE_Y}" '
    return frag.replace("<Artboard ", head, 1)


_AB_ID = re.compile(r'<Artboard\b[^>]*\bid="1:(\d+)"')
_AB_SM = re.compile(r'<Artboard\b[^>]*\bdefaultStateMachineId="1:(\d+)"')


def _ab_attr(pattern, path):
    raw = pathlib.Path(path).read_text()
    return "%d:%s" % (CLIENT, pattern.search(raw).group(1))


def artboard_id(path=SRC):
    """The renumbered id of the Teacher artboard, for artboardId to point at."""
    return _ab_attr(_AB_ID, path)


def state_machine_id(path=SRC):
    """The renumbered id of the teacher's own blink + head-sway machine."""
    return _ab_attr(_AB_SM, path)


def component_asset_rml(asset_id, name="Teacher"):
    """Lists the Teacher artboard as a component. Editor-side only — without it
    `inspect` warns that an isComponent artboard no asset names is invisible in
    the component picker. The .riv renders the same either way."""
    return (f'<ComponentAsset artboardId="{artboard_id()}" '
            f'name="{name}" id="{asset_id}"/>')


def rig_rml(rig_id, nested_id, sm_id, name="Teacher"):
    """The character, wrapped in a rig Node the timeline can drive.

    Returns (rig_node_id, xml). Animate the RIG, never the NestedArtboard: the
    nested one carries the scale that fits the character to the band, and keying
    scaleX on it would fight that. The rig's own scaleX is free to run 1 -> -1,
    which is how the character turns to face the other dock.

    The <NestedStateMachine> child is not optional dressing. `defaultStateMachineId`
    only starts a machine on the artboard the runtime plays at the top; a nested
    artboard runs exactly what its NestedAnimation children name. Without one it
    compiles, inspects and draws — in its UNPOSED rest pose, which for this rig
    puts an ear across the cheek and loses an eye.
    """
    x, y = nested_origin()
    s = scale()
    inner = (f'<NestedArtboard artboardId="{artboard_id()}" x="{x:.2f}" '
             f'y="{y:.2f}" scaleX="{s:.4f}" scaleY="{s:.4f}" '
             f'name="{name}Art" id="{nested_id}">'
             f'<NestedStateMachine animationId="{sm_id}" name="Idle"/>'
             f'</NestedArtboard>')
    return (f'<Node x="{dock("L"):.2f}" y="{FEET_Y:.2f}" name="{name}Rig" '
            f'id="{rig_id}">{inner}</Node>')


if __name__ == "__main__":
    cmap, eyes = colour_map()
    print(f"teacher artboard {artboard_id()}  scale {scale():.4f}  "
          f"width {width():.1f}  nested origin "
          f"{nested_origin()[0]:.2f},{nested_origin()[1]:.2f}")
    for side in ("L", "R"):
        x0, x1, y0, y1 = bounds(side)
        print(f"  dock {side}: centre {dock(side):7.1f}  "
              f"x {x0:.0f}..{x1:.0f}  y {y0:.0f}..{y1:.0f}")
    print(f"{len(cmap)} SolidColors recoloured, eyes {eyes}")
