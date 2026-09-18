"""Timeline for the CNN convolution lesson.

Keyframes only — layout and content live in generate.py. Frames are at 60fps.

The arc, built so it assumes no prior knowledge and never skips a step:

  S1  an image is a grid of numbers
  S2  a filter is a grid of numbers too
  S3  ONE position, fully worked: 9 products appear one at a time, then sum
  S4  slide and repeat — the same 9 weights, every position
  S5  back and forth — output -> its input patch, and input -> its outputs
  S6  change the 9 numbers, the filter looks for something else
"""

FPS = 60


def s(seconds):
    return int(round(seconds * FPS))


# ------------------------------------------------------------- key tracks ---
class Anim:
    """Collects (object, property) -> keyframes, then emits RML."""

    OPACITY, X, Y, SCALE_X, SCALE_Y = 18, 13, 14, 16, 17
    ROTATION = 15                      # radians, not degrees

    def __init__(self):
        self.tracks = {}

    def key(self, oid, prop, frame, value, interp="cubic"):
        self.tracks.setdefault((oid, prop), []).append((int(frame), value, interp))

    def fade(self, oid, f0, f1, v0, v1, interp="cubic"):
        self.key(oid, self.OPACITY, f0, v0, interp)
        self.key(oid, self.OPACITY, f1, v1, interp)

    def show(self, oid, f_in, f_out=None, rise=12, fall=12):
        """Fade in at f_in; if f_out given, fade back out there."""
        self.fade(oid, f_in, f_in + rise, 0, 1)
        if f_out is not None:
            self.fade(oid, f_out, f_out + fall, 1, 0)

    def move(self, oid, f0, f1, xy0, xy1, interp="cubic"):
        self.key(oid, self.X, f0, xy0[0], interp)
        self.key(oid, self.X, f1, xy1[0], interp)
        self.key(oid, self.Y, f0, xy0[1], interp)
        self.key(oid, self.Y, f1, xy1[1], interp)

    def pop(self, oid, f0, dur=14, from_scale=0.55):
        """Scale + fade a node in from small."""
        self.key(oid, self.SCALE_X, f0, from_scale)
        self.key(oid, self.SCALE_X, f0 + dur, 1)
        self.key(oid, self.SCALE_Y, f0, from_scale)
        self.key(oid, self.SCALE_Y, f0 + dur, 1)
        self.fade(oid, f0, f0 + dur, 0, 1)

    def pulse(self, oid, f0, dur=20, peak=1.14):
        h = dur // 2
        for p, v in ((0, 1), (h, peak), (dur, 1)):
            self.key(oid, self.SCALE_X, f0 + p, v)
            self.key(oid, self.SCALE_Y, f0 + p, v)

    def emit(self, name, anim_id, duration):
        by_obj = {}
        for (oid, prop), keys in self.tracks.items():
            by_obj.setdefault(oid, {})[prop] = sorted(keys, key=lambda k: k[0])
        out = [f'<LinearAnimation loopValue="loop" duration="{int(duration)}" '
               f'fps="{FPS}" name="{name}" id="{anim_id}">']
        for oid, props in by_obj.items():
            out.append(f'<KeyedObject objectId="{oid}">')
            for prop, keys in props.items():
                out.append(f'<KeyedProperty propertyKey="{prop}">')
                seen = set()
                for frame, value, interp in keys:
                    if frame in seen:          # last write wins per frame
                        continue
                    seen.add(frame)
                    out.append(f'<KeyFrameDouble value="{round(value, 4)}" '
                               f'interpolationType="{interp}" frame="{frame}"/>')
                out.append('</KeyedProperty>')
            out.append('</KeyedObject>')
        out.append('</LinearAnimation>')
        return "".join(out)


# ---------------------------------------------------------------- the arc ---
# Which dock each line is spoken from. The teacher stands next to whatever it is
# talking about: the image and the single pixel are on the left, the feature map
# and the filter swap are on the right. Three crossings in 52s — enough for the
# move to mean something, few enough that it never reads as pacing.
DOCK = {0: "L", 1: "L", 2: "L", 3: "R", 4: "R", 5: "R", 6: "L", 7: "R", 8: "R"}


def compose(ids, L):
    """L is the layout namespace from generate.py (constants + helpers)."""
    A = Anim()
    cap = ids["caption"]
    rig, art, bub = ids["rig"], ids["rigArt"], ids["bubble"]
    M = L.mascot
    NEST_Y = M.nested_origin()[1]
    here = {"side": "L", "last_out": 0}

    def bubble_x(side):
        return L.BUB_X_L if side == "L" else L.BUB_X_R

    # rest pose: left dock, facing the diagram, left-hand tail on the bubble
    A.key(rig, A.X, 0, M.dock("L"))
    A.key(rig, A.Y, 0, M.FEET_Y)
    A.key(rig, A.SCALE_X, 0, 1)
    A.key(rig, A.ROTATION, 0, 0)
    A.key(bub, A.X, 0, bubble_x("L"))
    A.key(ids["tailL"], A.OPACITY, 0, 1)
    A.key(ids["tailR"], A.OPACITY, 0, 0)

    def walk(side, f0, dur=s(0.6)):
        """Cross to the other dock: a hop and a lean into the direction.

        Deliberately NOT mirrored. Flipping scaleX to face the other way has to
        pass through zero, and for one frame mid-stride the character is a
        vertical sliver — it reads as a glitch, not as turning round. The rig
        does not need it either: the character's own state machine sways its
        head both ways, so it never looks stuck facing one edge.

        The path crosses the middle of the band, where the bubble is. The rig is
        declared BEFORE the bubble in generate.py, so the character passes in
        FRONT of it — which costs nothing, because the crossing is timed to the
        gap when the bubble is empty, and it keeps the face visible throughout.
        The arc height is mascot.HOP, held low enough to stay clear of the
        diagram; generate.py asserts that.
        """
        if here["side"] == side:
            return
        x0, x1 = M.dock(here["side"]), M.dock(side)
        mid, endf = f0 + dur // 2, f0 + dur
        A.key(rig, A.X, f0, x0)
        A.key(rig, A.X, endf, x1)
        # The arc has to clear the bubble, not just look springy: at the top of
        # it the head must be ABOVE the bubble's top edge, or the character
        # crosses with its face hidden and only its hair showing over the box.
        A.key(rig, A.Y, f0, M.FEET_Y)
        A.key(rig, A.Y, mid, M.FEET_Y - M.HOP)
        A.key(rig, A.Y, endf, M.FEET_Y)
        lean = 0.07 if x1 > x0 else -0.07
        for f, v in ((f0, 0), (f0 + s(0.18), lean), (endf - s(0.14), lean), (endf, 0)):
            A.key(rig, A.ROTATION, f, v)
        # a little weight on the landing — the rig's origin is the feet, so
        # scaleY compresses it downward the way a body settles
        for f, v in ((endf, 1.0), (endf + s(0.10), 0.94), (endf + s(0.26), 1.0)):
            A.key(rig, A.SCALE_Y, f, v)
        # the bubble travels with it and changes which side its tail is on
        A.key(bub, A.X, f0, bubble_x(here["side"]))
        A.key(bub, A.X, endf, bubble_x(side))
        old, new = ("tailL", "tailR") if side == "R" else ("tailR", "tailL")
        A.fade(ids[old], f0, f0 + s(0.16), 1, 0)
        A.fade(ids[new], endf - s(0.16), endf, 0, 1)
        here["side"] = side

    def caption(n, f_in, f_out):
        """One spoken line: cross to its dock if needed, then say it.

        The crossing starts the instant the PREVIOUS line begins to fade, so the
        whole traverse happens while the bubble is empty. Timed off the incoming
        line instead, the teacher would walk across live text.
        """
        walk(DOCK[n], max(here["last_out"], f_in - s(1.4)))
        here["last_out"] = f_out if f_out is not None else f_in
        A.show(cap[n], f_in, f_out)
        # a small nod as the line lands — the gesture that ties voice to speaker
        for f, v in ((f_in, 0), (f_in + s(0.13), 0.035), (f_in + s(0.30), 0)):
            A.key(rig, A.ROTATION, f, v)

    # The bubble arrives once, with the first line, and then stays — it only
    # ever sits empty for the 0.4-0.8s between two lines, and popping it in and
    # out nine times would strobe the corner of the frame.
    A.fade(bub, s(1.0), s(1.35), 0, 1)
    for f, v in ((s(1.0), 0.90), (s(1.30), 1.02), (s(1.45), 1.0)):
        A.key(bub, A.SCALE_X, f, v)
        A.key(bub, A.SCALE_Y, f, v)

    # ============================================================= S1 ======
    # An image is a grid of numbers.
    A.show(ids["lblIn"], s(0.3))
    A.show(ids["inputGrid"], s(0.5))
    caption(0, s(1.2), s(5.0))
    for n, tid in enumerate(ids["inNums"]):          # 25 numbers, staggered
        A.show(tid, s(2.0) + n * 4)

    # ============================================================= S2 ======
    # A filter is a grid of numbers too.
    caption(1, s(5.4), s(9.2))
    A.show(ids["lblK"], s(6.0))
    A.show(ids["filterGroups"][0], s(6.2))
    A.show(ids["opMul"], s(6.8))

    # ============================================================= S3 ======
    # One position, worked in full.
    caption(2, s(9.6), s(17.4))
    A.show(ids["kernelFrame"], s(10.0))
    A.key(ids["kernelFrame"], A.X, s(10.0), L.IN_X)
    A.key(ids["kernelFrame"], A.Y, s(10.0), L.IN_Y)
    A.show(ids["slots"], s(10.4))
    A.show(ids["lblOut"], s(10.4))
    A.show(ids["lblP"], s(11.0))
    A.show(ids["opEq"], s(11.0))

    # the nine products, one at a time — this is the beat the lesson exists for
    P0 = ids["prodCells"][0]
    for n in range(9):
        A.pop(P0[n], s(11.6) + n * 26, dur=12)
    A.show(ids["prodSums"][0], s(15.6))

    # the sum travels into the feature map
    A.show(ids["travel"][0], s(16.2), s(17.2), rise=8, fall=8)
    A.move(ids["travel"][0], s(16.4), s(17.2), L.sum_anchor(), L.out_center(0, 0))
    A.pop(ids["outCells"][0][0], s(17.1), dur=14)
    caption(3, s(17.8), s(20.4))

    # ============================================================= S4 ======
    # Slide and repeat, with the very same nine numbers.
    caption(4, s(20.8), s(29.2))     # must clear before caption 8 lands
    STEP = s(1.35)
    base = s(21.6)
    for p in range(1, 9):
        t = base + (p - 1) * STEP
        r, c = L.POSITIONS[p]
        pr, pc = L.POSITIONS[p - 1]
        A.move(ids["kernelFrame"], t, t + s(0.42),
               L.kernel_xy(pr, pc), L.kernel_xy(r, c))
        A.fade(ids["prodGroups"][p - 1], t, t + s(0.18), 1, 0)
        A.fade(ids["prodSums"][p - 1], t, t + s(0.18), 1, 0)   # or they stack up
        A.fade(ids["prodGroups"][p], t + s(0.30), t + s(0.48), 0, 1)
        A.fade(ids["prodSums"][p], t + s(0.30), t + s(0.48), 0, 1)
        A.show(ids["travel"][p], t + s(0.62), t + s(1.02), rise=7, fall=7)
        A.move(ids["travel"][p], t + s(0.66), t + s(1.02),
               L.sum_anchor(), L.out_center(r, c))
        A.pop(ids["outCells"][0][p], t + s(0.98), dur=12)
    # products group 0 is the one visible going in; make that explicit
    A.fade(ids["prodGroups"][0], s(11.5), s(11.6), 1, 1)

    end_sweep = base + 8 * STEP
    # answer the question the shrinking map raises, before moving on
    caption(8, end_sweep - s(2.6), end_sweep - s(0.2))

    # ============================================================= S5 ======
    # Back and forth: output -> patch, and input -> outputs.
    t = end_sweep + s(0.6)
    caption(5, t, t + s(4.4))
    # forward: this output cell came from this patch.
    # Swap the products to position 4 as the frame moves, or the column would
    # still be showing position 8's arithmetic next to a highlighted cell (1,1).
    A.move(ids["kernelFrame"], t + s(0.4), t + s(1.0),
           L.kernel_xy(*L.POSITIONS[8]), L.kernel_xy(1, 1))
    A.fade(ids["prodGroups"][8], t + s(0.4), t + s(0.7), 1, 0)
    A.fade(ids["prodSums"][8], t + s(0.4), t + s(0.7), 1, 0)
    A.fade(ids["prodGroups"][4], t + s(0.9), t + s(1.2), 0, 1)
    A.fade(ids["prodSums"][4], t + s(0.9), t + s(1.2), 0, 1)
    A.show(ids["outRing"], t + s(0.9), t + s(4.2))
    A.key(ids["outRing"], A.X, t + s(0.9), L.out_xy(1, 1)[0])
    A.key(ids["outRing"], A.Y, t + s(0.9), L.out_xy(1, 1)[1])
    A.pulse(ids["outCells"][0][4], t + s(1.2), dur=26)

    # reverse: this input cell fed all of these outputs
    t2 = t + s(5.0)
    caption(6, t2, t2 + s(5.0))
    A.fade(ids["kernelFrame"], t2, t2 + s(0.3), 1, 0)
    # no single kernel position applies here, so retire the arithmetic column
    for oid in (ids["prodGroups"][4], ids["prodSums"][4],
                ids["lblP"], ids["opEq"]):
        A.fade(oid, t2, t2 + s(0.3), 1, 0)
    A.show(ids["arrow"], t2 + s(0.4))      # takes over the vacated column
    A.show(ids["inputRing"], t2 + s(0.4), t2 + s(4.6))
    A.key(ids["inputRing"], A.X, t2 + s(0.4), L.in_xy(2, 2)[0])
    A.key(ids["inputRing"], A.Y, t2 + s(0.4), L.in_xy(2, 2)[1])
    for n in range(9):                    # centre pixel feeds every output
        A.pulse(ids["outCells"][0][n], t2 + s(1.0) + n * 5, dur=22)
    # ...whereas the corner pixel feeds exactly one
    A.move(ids["inputRing"], t2 + s(2.6), t2 + s(3.1), L.in_xy(2, 2), L.in_xy(0, 0))
    A.pulse(ids["outCells"][0][0], t2 + s(3.3), dur=26)

    # ============================================================= S6 ======
    # Change the nine numbers and it looks for something else.
    t3 = t2 + s(5.6)
    caption(7, t3, None)
    # the products column and its arrow are already handled in S5 — re-fading
    # them from 1 here would key them back ON at t3 before fading out again

    for fi in (1, 2):
        ft = t3 + s(0.8) + (fi - 1) * s(3.2)
        A.fade(ids["filterGroups"][fi - 1], ft, ft + s(0.35), 1, 0)
        A.fade(ids["filterGroups"][fi], ft + s(0.35), ft + s(0.7), 0, 1)
        A.fade(ids["outGroups"][fi - 1], ft, ft + s(0.35), 1, 0)
        A.fade(ids["outGroups"][fi], ft + s(0.35), ft + s(0.7), 0, 1)

    end = t3 + s(0.8) + s(3.2) + s(3.4)

    # A slow breath on the nested artboard's own y, for the whole lesson. It is
    # keyed HERE and not on the rig because the rig's y is the hop in walk() —
    # two tracks writing one property would fight, and the last key at a frame
    # would silently win.
    breath = s(1.35)                      # half a cycle
    f, down = 0, False
    while f <= end + breath:
        A.key(art, A.Y, f, NEST_Y - (0 if down else 3.0))
        down = not down
        f += breath

    return A, end
