"""Tiny XML tree helper for emitting RML.

Draw order in Rive is the reverse of HTML: the *first* sibling declared paints
on top. Authoring back-to-front is far easier to reason about, so `Node.kids`
is written back-to-front and `xml()` reverses it on the way out. Every builder
in generate.py therefore appends background first, foreground last.
"""

from xml.sax.saxutils import quoteattr


def fmt(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        return f"{v:.4f}".rstrip("0").rstrip(".")
    return str(v)


class El:
    __slots__ = ("tag", "attrs", "kids", "reverse")

    def __init__(self, tag, reverse=True, **attrs):
        self.tag = tag
        self.attrs = {k: v for k, v in attrs.items() if v is not None}
        self.kids = []
        # Paint children *inside* one shape stack last-on-top, the opposite of
        # sibling shapes, so Fill/Stroke lists must not be flipped.
        self.reverse = reverse

    def add(self, *kids):
        for k in kids:
            if k is not None:
                self.kids.append(k)
        return self

    def xml(self, indent=0):
        pad = "  " * indent
        attr = "".join(
            f" {k.rstrip('_')}={quoteattr(fmt(v))}" for k, v in self.attrs.items()
        )
        if not self.kids:
            return f"{pad}<{self.tag}{attr}/>"
        kids = self.kids[::-1] if self.reverse else self.kids
        inner = "\n".join(k.xml(indent + 1) for k in kids)
        return f"{pad}<{self.tag}{attr}>\n{inner}\n{pad}</{self.tag}>"


class Ids:
    """Document-wide id allocator. Ids share one namespace across every file."""

    def __init__(self, client=1, start=10):
        self.client = client
        self.n = start

    def __call__(self):
        self.n += 1
        return f"{self.client}:{self.n}"
