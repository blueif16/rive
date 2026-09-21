#!/usr/bin/env python3
"""Figure A — What a context window holds.

A fixed-width budget bar. Turns push in from the right; the counter climbs; at
capacity the oldest turns collapse into one summary and the reclaimed space is
taken immediately. The bar's width never changes.

Run:  ./.venv/bin/python generate.py       -> writes scene.rml + build/charsets.json
Then: rive . --once                         -> writes build/figure.riv
"""
import json
import pathlib

from geom import El, Ids
import rivelib as R

HERE = pathlib.Path(__file__).parent

# ==================================================================== config ==
# Colours are 8-digit ARGB strings. "FF" prefix == fully opaque.
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

CREAM_70 = "B3EDECE1"          # block token counts — cream, held back
INK_55   = "8C3B3730"

W, H = 1200, 600
FPS = 60
T_LOOP = 12.0
DUR_F = round(T_LOOP * FPS)    # 720

# Font asset ids are fixed by the document preamble below.
FONTS = {"serif": "1:2", "italic": "1:3", "sans": "1:4", "sansmed": "1:5"}
TTF = {
    "serif":   str(HERE / "fonts/serif.ttf"),
    "italic":  str(HERE / "fonts/serif-italic.ttf"),
    "sans":    str(HERE / "fonts/sans.ttf"),
    "sansmed": str(HERE / "fonts/sans-medium.ttf"),
}

# --- layout -------------------------------------------------------------------
M_L, M_R = 96, 1104            # left / right content edges

BAR_X, BAR_Y = M_L, 264
BAR_W, BAR_H = M_R - M_L, 116  # 1008 x 116 — this never changes, ever
PAD = 6
IN_X, IN_Y = BAR_X + PAD, BAR_Y + PAD
IN_W, BLK_H = BAR_W - 2 * PAD, BAR_H - 2 * PAD   # 996 x 104

TOTAL = 128000
PX = IN_W / TOTAL              # px per token
GAP = 3.0                      # hairline gutter between blocks
OFF = IN_W + 40                # staging x for a block that has not entered yet

# Letterspacing: Rive's unit is ambiguous (em vs px). 0.15 is the house value if
# em, and negligible if px — but boxes are measured at the em width so that the
# wider of the two readings still fits.
LS = 0.15

# --- beat timing (4 beats x 3s, 26-frame crossfades landing on each boundary) --
BEAT = 180
XF = 26


def beat_fade(i):
    """Opacity track for beat i: opaque in its window, crossfading on the seams."""
    a, b = i * BEAT, (i + 1) * BEAT
    if i == 0:
        return [(0, 1.0), (b - XF, 1.0), (b, 0.0), (DUR_F - XF, 0.0), (DUR_F, 1.0)]
    return [(0, 0.0), (a - XF, 0.0), (a, 1.0), (b - XF, 1.0), (b, 0.0), (DUR_F, 0.0)]


RESET = {0: 400, 1: 500, 2: 620, 3: DUR_F}   # frame each beat rewinds, unseen

# ===================================================================== blocks ==
KIND = {                       # fill, label colour
    "system":      (INK,      CREAM),
    "user":        (WARM_LT,  CREAM),
    "tool result": (WARM_DK,  CREAM),
    "assistant":   (LAVENDER, CREAM),
    "summary":     (ACCENT,   CREAM),
}
# Real words of differing lengths. Longest form that measures into the block wins.
FORMS = {
    "system":      ["SYSTEM", "SYS", "S"],
    "user":        ["USER", "USR", "U"],
    "tool result": ["TOOL RESULT", "TOOL", "T"],
    "assistant":   ["ASSISTANT", "ASST", "A"],
    "summary":     ["SUMMARY", "SUM", "S"],
}
LFS, CFS = 10, 11              # label / count font sizes


def toks(n):
    return f"{n / 1000:.1f}k"


def blk(kind, n, x, ids, *, gid=None, live=False):
    """One conversation turn. Width is strictly proportional to its token count."""
    w = n * PX - GAP
    g = R.grp(f"b_{kind.replace(' ', '_')}_{n}", x=x, y=0, id=gid)
    fill_c, text_c = KIND[kind]
    g.add(R.rect(0, 0, w, BLK_H, r=7, fill_=fill_c,
                 stroke_=(INDIGO, 2.5) if live else None))

    avail = w - 14
    for form in FORMS[kind]:
        lw = R.measure(form, LFS, TTF["sansmed"], letter_spacing=LFS * LS)
        if lw <= avail:
            bw = lw + 6
            g.add(R.text((w - bw) / 2, 30, bw, 20, form, LFS, text_c, FONTS,
                         align="center", ls=LS, font="sansmed", ids=ids))
            break

    cnt = toks(n)
    cw = R.measure(cnt, CFS, TTF["sans"])
    if cw <= avail:
        g.add(R.text((w - cw - 6) / 2, 54, cw + 6, 22, cnt, CFS, CREAM_70, FONTS,
                     align="center", font="sans", ids=ids))
    return g


def chain(turns, ids, x0=0.0, live_last=False):
    """Lay `turns` [(kind, tokens), ...] end to end from token offset 0."""
    out, cur = [], x0
    for i, (kind, n) in enumerate(turns):
        out.append(blk(kind, n, cur * PX, ids,
                       live=live_last and i == len(turns) - 1))
        cur += n
    return out, cur


def arrive(anim, gid, x_end, f0, f1, reset):
    """Stage off the right edge, glide to the frontier, rewind while unseen."""
    anim.key(gid, "x", [(0, OFF, "hold"), (f0, OFF, R.EASE_OUT),
                        (f1, x_end, "hold"), (reset, OFF, "hold")])


# ====================================================================== type ==
def ltext(x, cy, s, fs, color, ids, *, font="sans", ls=0.0, h=None):
    w = R.measure(s, fs, TTF[font], letter_spacing=fs * ls) + 4
    h = h or fs * 1.7
    return R.text(x, cy - h / 2, w, h, s, fs, color, FONTS,
                  align="left", ls=ls or 0, font=font, ids=ids)


def rtext(right, cy, s, fs, color, ids, *, font="sans", ls=0.0, h=None):
    w = R.measure(s, fs, TTF[font], letter_spacing=fs * ls) + 4
    h = h or fs * 1.7
    return R.text(right - w, cy - h / 2, w, h, s, fs, color, FONTS,
                  align="right", ls=ls or 0, font=font, ids=ids)


# ==================================================================== counter ==
# (frame, used, colour). Each value is its own box, right-aligned to a shared
# edge and stepped with hold keys — a real readout, climbing and dropping.
COUNTER = [
    (0,   "21,000",  INDIGO),
    (86,  "45,800",  INDIGO),
    (220, "61,000",  INDIGO),
    (252, "67,400",  INDIGO),
    (296, "99,000",  INDIGO),
    (330, "117,700", ACCENT),
    (400, "126,900", ACCENT),
    (458, "75,700",  INDIGO),
    (482, "81,100",  INDIGO),
    (508, "103,900", INDIGO),
    (592, "111,700", INDIGO),
    (640, "125,900", ACCENT),
]

CAPTIONS = [
    ("01 — EMPTY",        "A fixed budget. New turns push in from the right."),
    ("02 — FILLING",      "The history grows. The budget does not."),
    ("03 — PRESSURE",     "Full. The oldest turns collapse into one summary."),
    ("04 — STEADY STATE", "A long compacted history, only recent turns in full."),
]


# ===================================================================== scene ==
def build_scene(ab, anim, ids):
    # ------------------------------------------------------------- header --
    hd = R.grp("Header")
    hd.add(ltext(M_L, 40, "FIGURE A — CONTEXT WINDOW", 11, MUTED, ids,
                 font="sansmed", ls=LS))
    hd.add(ltext(M_L, 83, "What a context window holds", 38, INK, ids,
                 font="serif"))
    hd.add(rtext(M_R, 42, "TOKENS IN WINDOW", 11, MUTED, ids,
                 font="sansmed", ls=LS))
    hd.add(R.line(M_L, 146, M_R, 146, EDGE, 1))
    ab.add(hd)

    # ---------------------------------------------- bar track (fill only) --
    ab.add(R.rect(BAR_X, BAR_Y, BAR_W, BAR_H, r=10, fill_=CREAM))

    # --------------------------------------------------------- beat 1: empty
    b1 = ids()
    g1 = R.grp("Beat1", id=b1)
    c1 = R.grp("C1", x=IN_X, y=IN_Y)
    base1 = [("system", 12400), ("user", 8600)]
    kids, cur = chain(base1, ids)
    c1.add(*kids)
    a1 = ids()
    c1.add(blk("tool result", 24800, 0, ids, gid=a1, live=True))
    arrive(anim, a1, cur * PX, 34, 86, RESET[0])
    g1.add(c1)
    ab.add(g1)

    # ------------------------------------------------------- beat 2: filling
    b2 = ids()
    g2 = R.grp("Beat2", id=b2)
    c2 = R.grp("C2", x=IN_X, y=IN_Y)
    kids, cur = chain(base1 + [("tool result", 24800)], ids)
    c2.add(*kids)
    incoming = [("assistant", 15200, 186, 220), ("user", 6400, 224, 252),
                ("tool result", 31600, 256, 296), ("assistant", 18700, 298, 330)]
    for i, (kind, n, f0, f1) in enumerate(incoming):
        gid = ids()
        c2.add(blk(kind, n, 0, ids, gid=gid, live=(i == len(incoming) - 1)))
        arrive(anim, gid, cur * PX, f0, f1, RESET[1])
        cur += n
    g2.add(c2)
    ab.add(g2)

    # ------------------------------------------------------ beat 3: pressure
    # The oldest four (61,000 tokens) dim, collapse leftward and are replaced by
    # a single 9,800-token summary; everyone behind slides into the reclaimed
    # space, which new arrivals take immediately.
    OLD = [("system", 12400), ("user", 8600), ("tool result", 24800),
           ("assistant", 15200)]
    old_tok = sum(n for _, n in OLD)          # 61,000
    SUM_TOK = 9800
    SHIFT = (old_tok - SUM_TOK) * PX

    b3 = ids()
    g3 = R.grp("Beat3", id=b3)
    c3 = R.grp("C3", x=IN_X, y=IN_Y)

    g_old_id = ids()
    g_old = R.grp("Oldest", x=0, y=0, id=g_old_id)
    kids, _ = chain(OLD, ids)
    g_old.add(*kids)
    c3.add(g_old)
    anim.key(g_old_id, "opacity", [(0, 1.0, "hold"), (404, 1.0, R.EASE_FADE),
                                   (444, 0.0, "hold"), (RESET[2], 1.0, "hold")])
    anim.key(g_old_id, "scaleX", [(0, 1.0, "hold"), (408, 1.0, R.EASE_IN_OUT),
                                  (448, 0.04, "hold"), (RESET[2], 1.0, "hold")])

    g_sum_id = ids()
    g_sum = R.grp("Summary", x=0, y=0, id=g_sum_id)
    g_sum.add(blk("summary", SUM_TOK, 0, ids))
    c3.add(g_sum)
    anim.key(g_sum_id, "opacity", [(0, 0.0, "hold"), (428, 0.0, R.EASE_FADE),
                                   (462, 1.0, "hold"), (RESET[2], 0.0, "hold")])

    g_sv_id = ids()
    g_sv = R.grp("Survivors", x=0, y=0, id=g_sv_id)
    SURV = [("user", 6400), ("tool result", 31600), ("assistant", 18700)]
    kids, cur = chain(SURV, ids, x0=old_tok)
    g_sv.add(*kids)
    a3 = ids()                                 # last turn before the squeeze
    g_sv.add(blk("tool result", 9200, 0, ids, gid=a3, live=True))
    arrive(anim, a3, cur * PX, 368, 400, RESET[2])
    cur += 9200
    c3.add(g_sv)
    anim.key(g_sv_id, "x", [(0, 0.0, "hold"), (414, 0.0, R.EASE_IN_OUT),
                            (456, -SHIFT, "hold"), (RESET[2], 0.0, "hold")])

    cur = SUM_TOK + (cur - old_tok)            # token frontier after compaction
    for kind, n, f0, f1 in [("user", 5400, 452, 482),
                            ("tool result", 22800, 474, 508)]:
        gid = ids()
        c3.add(blk(kind, n, 0, ids, gid=gid, live=(n == 22800)))
        arrive(anim, gid, cur * PX, f0, f1, RESET[2])
        cur += n

    cap_id = ids()                             # capacity wall, struck twice
    cap = R.grp("CapFlash", x=IN_W - 5, y=0, id=cap_id)
    cap.add(R.rect(0, 0, 5, BLK_H, r=2, fill_=ACCENT))
    c3.add(cap)
    anim.key(cap_id, "opacity", [(0, 0.0, "hold"), (372, 0.0, R.EASE_FADE),
                                 (386, 0.9, R.EASE_FADE), (398, 0.15, R.EASE_FADE),
                                 (408, 0.9, R.EASE_FADE), (424, 0.0, "hold"),
                                 (DUR_F, 0.0, "hold")])
    g3.add(c3)
    ab.add(g3)

    # -------------------------------------------------- beat 4: steady state
    B4_SUM = 23600                             # the summary itself has grown
    b4 = ids()
    g4 = R.grp("Beat4", id=b4)
    c4 = R.grp("C4", x=IN_X, y=IN_Y)
    kids, cur = chain([("summary", B4_SUM), ("assistant", 18700),
                       ("tool result", 9200), ("user", 5400),
                       ("tool result", 22800), ("assistant", 16900),
                       ("user", 7300)], ids)
    c4.add(*kids)
    for kind, n, f0, f1 in [("user", 7800, 560, 592),
                            ("tool result", 14200, 600, 640)]:
        gid = ids()
        c4.add(blk(kind, n, 0, ids, gid=gid, live=(n == 14200)))
        arrive(anim, gid, cur * PX, f0, f1, RESET[3])
        cur += n
    g4.add(c4)

    # what fell out of the window, squeezed under the summary it became
    sum_w = B4_SUM * PX - GAP
    hist = R.grp("History", x=IN_X, y=396)
    hx = sum_w
    for cw in [28, 16, 34, 22, 44, 14, 30, 20, 38, 24, 16, 32, 26, 18, 40]:
        hx -= cw
        hist.add(R.rect(hx, 0, cw - 4, 14, r=3, fill_=EDGE))
        hx -= 0
    g4.add(hist)
    brk = R.grp("Bracket", x=IN_X, y=0)
    brk.add(R.line(0, 422, sum_w, 422, MUTED, 1))
    brk.add(R.line(0, 417, 0, 427, MUTED, 1))
    brk.add(R.line(sum_w, 417, sum_w, 427, MUTED, 1))
    g4.add(brk)
    g4.add(ltext(IN_X, 442, "412,000 TOKENS COMPACTED INTO 23,600", 11, MUTED,
                 ids, font="sansmed", ls=LS))
    ab.add(g4)

    for gid, i in ((b1, 0), (b2, 1), (b3, 2), (b4, 3)):
        anim.fade(gid, beat_fade(i))

    # ------------------------- masks — own layer, never faded (see SKILL.md) --
    msk = R.grp("Masks")
    msk.add(R.rect(M_R + 1, BAR_Y - 10, W - M_R, BAR_H + 20, fill_=PAGE))
    msk.add(R.edge_fade(-20, 390, 172, 28, PAGE, opaque_at="left"))
    ab.add(msk)

    # ------------------------------------- bar frame + capacity (never fades) --
    fr = R.grp("Frame")
    fr.add(R.rect(BAR_X, BAR_Y, BAR_W, BAR_H, r=10, stroke_=(INK, 2)))
    fr.add(R.line(M_R, BAR_Y + BAR_H, M_R, BAR_Y + BAR_H + 12, INK, 2))
    fr.add(rtext(M_R, 404, "CAPACITY 128,000", 11, MUTED, ids,
                 font="sansmed", ls=LS))
    ab.add(fr)

    # -------------------------------------------------- captions (per beat) --
    for i, (label, line) in enumerate(CAPTIONS):
        cid = ids()
        cg = R.grp(f"Cap{i}", id=cid)
        cg.add(ltext(M_L, 180, label, 12, LAVENDER, ids, font="sansmed", ls=LS))
        cg.add(ltext(M_L, 212, line, 17, INK, ids))
        ab.add(cg)
        anim.fade(cid, beat_fade(i))

    # ------------------------------------------------ counter (stepped digits) --
    slash = "/ 128,000"
    w_slash = R.measure(slash, 22, TTF["sans"]) + 4
    x_div = M_R - w_slash - 14
    w_used = max(R.measure(v, 40, TTF["sansmed"]) for _, v, _ in COUNTER) + 6

    for i, (f, val, col) in enumerate(COUNTER):
        nxt = COUNTER[i + 1][0] if i + 1 < len(COUNTER) else DUR_F
        nid = ids()
        ng = R.grp(f"N{i}", id=nid)
        ng.add(R.text(x_div - w_used, 64, w_used, 52, val, 40, col, FONTS,
                      align="right", font="sansmed", ids=ids))
        ab.add(ng)
        if i == 0:
            anim.key(nid, "opacity", [(0, 1.0, "hold"), (nxt, 0.0, "hold"),
                                      (DUR_F, 1.0, "hold")])
        else:
            anim.key(nid, "opacity", [(0, 0.0, "hold"), (f, 1.0, "hold"),
                                      (nxt, 0.0, "hold")])

    ab.add(R.text(M_R - w_slash, 82, w_slash, 32, slash, 22, MUTED, FONTS,
                  align="right", font="sans", ids=ids))


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
