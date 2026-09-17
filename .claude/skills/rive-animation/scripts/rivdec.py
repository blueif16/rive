#!/usr/bin/env python3
"""Decode a compiled .riv back into a typed object tree.

The Rive CLI converts .rev (editor) into RML, but there is no path back from a
.riv -- and `SVGAsset`/`LottieAsset` are stripped on export, so an imported
graphic cannot be round-tripped either. This reads the runtime format directly,
so artwork that only exists as a .riv can be lifted into an RML project.

The format, per rive-runtime's `runtime_header.hpp` and `binary_reader`:

    "RIVE"                     4-byte fingerprint
    varuint majorVersion
    varuint minorVersion
    varuint fileId
    varuint propertyKey ...    the table of contents, terminated by 0
    uint32 ...                 2 bits of field type per ToC key, 16 per word
    <objects to EOF>           varuint typeKey, then
                               (varuint propertyKey, value) ... terminated by 0

Field types are 0=uint(varuint) 1=string 2=double(float32) 3=color(uint32).
The ToC only exists so an old runtime can *skip* properties it does not know;
every key this tool knows is typed from `rive schema --json` instead, which is
version-matched to the CLI.

    python3 rivdec.py file.riv --summary
    python3 rivdec.py file.riv --artboard=Artboard --tree
    python3 rivdec.py file.riv --artboard=Artboard --json
"""

import argparse
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_CACHE = os.path.join(HERE, "rive-schema.json")

UINT, STRING, DOUBLE, COLOR = 0, 1, 2, 3

# schema type name -> how the byte stream encodes it
FIELD_OF_TYPE = {
    "uint": UINT, "int": UINT, "int16": UINT, "uint8": UINT, "uint16": UINT,
    "uint64": UINT, "bool": UINT, "Id": UINT, "List<Id>": UINT,
    "String": STRING, "Bytes": STRING,
    "double": DOUBLE,
    "Color": COLOR,
}


# ----------------------------------------------------------------- schema ---

def load_schema(rive_bin="rive"):
    """{typeKey: {name, props:{key:{n,t}}}} plus a flat key -> type map.

    Built by walking `rive schema --list` once and cached next to this file;
    the CLI is the authority for which keys exist in this version.
    """
    if os.path.exists(SCHEMA_CACHE):
        with open(SCHEMA_CACHE) as f:
            return json.load(f)

    names = subprocess.run([rive_bin, "schema", "--list"],
                           capture_output=True, text=True).stdout.split()
    types, keytype = {}, {}
    for name in names:
        r = subprocess.run([rive_bin, "schema", name, "--json"],
                           capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            continue
        d = json.loads(r.stdout)
        types[str(d["typeKey"])] = {
            "name": d["type"],
            "props": {str(p["key"]): {"n": p["name"], "t": p["type"]}
                      for p in d["properties"]},
        }
        for p in d["properties"]:
            keytype[str(p["key"])] = p["type"]
    schema = {"types": types, "keytype": keytype}
    with open(SCHEMA_CACHE, "w") as f:
        json.dump(schema, f)
    return schema


# ------------------------------------------------------------------ bytes ---

class Reader:
    def __init__(self, data):
        self.d, self.i = data, 0

    def byte(self):
        b = self.d[self.i]
        self.i += 1
        return b

    def varuint(self):
        """LEB128, low 7 bits per byte, high bit = continue."""
        value, shift = 0, 0
        while True:
            b = self.d[self.i]
            self.i += 1
            value |= (b & 0x7F) << shift
            if not (b & 0x80):
                return value
            shift += 7

    def float32(self):
        v = struct.unpack_from("<f", self.d, self.i)[0]
        self.i += 4
        return v

    def uint32(self):
        v = struct.unpack_from("<I", self.d, self.i)[0]
        self.i += 4
        return v

    def string(self):
        n = self.varuint()
        s = self.d[self.i:self.i + n].decode("utf-8", "replace")
        self.i += n
        return s

    @property
    def eof(self):
        return self.i >= len(self.d)


def read_value(r, field):
    if field == UINT:
        return r.varuint()
    if field == STRING:
        return r.string()
    if field == DOUBLE:
        return r.float32()
    if field == COLOR:
        return r.uint32()
    raise ValueError(f"unknown field type {field}")


# ------------------------------------------------------------------ parse ---

def parse(path, schema):
    with open(path, "rb") as f:
        data = f.read()
    r = Reader(data)

    if data[:4] != b"RIVE":
        raise SystemExit(f"{path}: not a .riv (no RIVE fingerprint)")
    r.i = 4
    major, minor, file_id = r.varuint(), r.varuint(), r.varuint()

    toc = []
    while True:
        k = r.varuint()
        if k == 0:
            break
        toc.append(k)
    # 2 bits per key, packed 16 to a 32-bit word
    toc_field = {}
    word, bit = 0, 32
    for k in toc:
        if bit == 32:
            word, bit = r.uint32(), 0
        toc_field[k] = (word >> bit) & 3
        bit += 2

    keytype = schema["keytype"]
    types = schema["types"]

    objects = []
    while not r.eof:
        type_key = r.varuint()
        props = {}
        while True:
            pk = r.varuint()
            if pk == 0:
                break
            t = keytype.get(str(pk))
            field = FIELD_OF_TYPE.get(t) if t else toc_field.get(pk)
            if field is None:
                raise SystemExit(
                    f"property {pk} is neither in the schema nor the ToC; "
                    f"the file is newer than this CLI")
            props[pk] = read_value(r, field)
        td = types.get(str(type_key))
        objects.append({
            "typeKey": type_key,
            "type": td["name"] if td else f"Unknown{type_key}",
            "props": props,
        })

    return {"version": f"{major}.{minor}", "fileId": file_id, "objects": objects}


def named(obj, schema):
    """Property dict keyed by schema name rather than number."""
    td = schema["types"].get(str(obj["typeKey"]))
    out = {}
    for k, v in obj["props"].items():
        p = td["props"].get(str(k)) if td else None
        out[p["n"] if p else f"key{k}"] = v
    return out


def artboards(doc, schema):
    """Split the flat object stream into artboards.

    Objects belong to the most recent Artboard (typeKey 1); within one, a
    component's parentId indexes that artboard's own list, where 0 is the
    artboard itself.
    """
    groups, cur = [], None
    for obj in doc["objects"]:
        if obj["type"] == "Artboard":
            cur = {"artboard": obj, "objects": [obj]}
            groups.append(cur)
        elif cur is not None:
            cur["objects"].append(obj)
    for g in groups:
        g["name"] = named(g["artboard"], schema).get("name", "(unnamed)")
        g["props"] = named(g["artboard"], schema)
    return groups


def build_tree(group, schema):
    """Attach each object to its parent, returning the artboard's children."""
    objs = group["objects"]
    for i, o in enumerate(objs):
        o["_named"] = named(o, schema)
        o["_children"] = []
        o["_index"] = i
    for i, o in enumerate(objs):
        if i == 0:
            continue
        pid = o["_named"].get("parentId")
        parent = objs[pid] if pid is not None and pid < len(objs) else objs[0]
        parent["_children"].append(o)
    return objs[0]


def print_tree(node, schema, depth=0, out=sys.stdout):
    n = node["_named"]
    bits = [f"#{node['_index']}"]
    for k in ("name", "width", "height", "x", "y", "colorValue", "thickness",
              "radius", "rotation", "opacity", "text"):
        if k in n:
            v = n[k]
            if k == "colorValue":
                v = f"#{v:08X}"
            elif isinstance(v, float):
                v = round(v, 2)
            bits.append(f"{k}={v}")
    print("  " * depth + f"{node['type']}  " + " ".join(bits), file=out)
    for c in node["_children"]:
        print_tree(c, schema, depth + 1, out)


# -------------------------------------------------------------------- rml ---

# Properties whose value indexes the artboard's object list are found by TYPE,
# not by name: the schema marks them `Id`. Hand-listing names misses the ones
# that are not called `somethingId` at all -- `KeyFrameId.value` is an Id, and
# so are `yId`, `handleSourceId` and `activeComponentId`.
#
# Runtime-only bookkeeping that is either derived, implied by nesting, or
# rejected by the compiler.
SKIP_PROPS = {"parentId", "flags"}


def fmt_num(v):
    if v == int(v):
        return str(int(v))
    return repr(round(v, 4))


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def to_rml(group, schema, artboard_name=None, indent="    ", prune=(), keep_animations=True):
    """Emit one decoded artboard as RML, ids renumbered, parents implied.

    `prune` drops objects by index along with their descendants -- how a part
    of the source graphic (a pair of glasses, say) gets left behind.
    """
    objs = group["objects"]
    types = schema["types"]

    # A state machine's states are grouped by stream order, not parentId, so
    # nesting them by parent produces objects the importer rejects. Animations
    # are safe; the consumer re-authors the state machine anyway.
    ANIM_ONLY = {"StateMachine", "StateMachineLayer", "AnimationState", "AnyState",
                 "EntryState", "ExitState", "StateTransition", "BlendState1D",
                 "BlendStateDirect", "StateMachineListenerSingle", "ListenerBoolChange",
                 "ListenerAlignTarget", "ListenerNumberChange", "ListenerTriggerChange",
                 "StateMachineBool", "StateMachineNumber", "StateMachineTrigger",
                 "StateMachineListener", "TransitionBoolCondition",
                 "TransitionNumberCondition", "TransitionTriggerCondition"}
    TIMELINE = {"LinearAnimation", "KeyedObject", "KeyedProperty", "KeyFrameDouble",
                "KeyFrameColor", "KeyFrameId", "KeyFrameBool", "KeyFrameString",
                "KeyFrameUint", "CubicValueInterpolator", "CubicEaseInterpolator",
                "CubicInterpolator", "ElasticInterpolator"}

    dropped = set()

    def mark(o):
        dropped.add(o["_index"])
        for c in o["_children"]:
            mark(c)

    for o in objs:
        if o["_index"] in prune or o["type"] in ANIM_ONLY:
            mark(o)
        elif not keep_animations and o["type"] in TIMELINE:
            mark(o)

    # Anything still POINTING at a dropped object has to go too, or the compiler
    # rejects the dangling reference -- pruning a shape orphans the KeyedObject
    # that animates it. Repeat until it settles, since those cascade.
    while True:
        grew = False
        for o in objs:
            if o["_index"] in dropped:
                continue
            td = types.get(str(o["typeKey"]), {})
            for key, val in o["props"].items():
                spec = td.get("props", {}).get(str(key))
                if spec and spec["t"] in ("Id", "List<Id>") and int(val) in dropped:
                    mark(o)
                    grew = True
                    break
        if not grew:
            break

    # Only objects that actually hang off the artboard get an id; a stray
    # parentId would otherwise silently drop a whole subtree.
    ids = {i: f"1:{i + 1}" for i in range(len(objs))}

    def attrs(obj, index):
        td = types.get(str(obj["typeKey"]), {})
        props = td.get("props", {})
        out = []
        for key, val in obj["props"].items():
            spec = props.get(str(key))
            if not spec:
                continue
            name = spec["n"]
            if name in SKIP_PROPS or spec.get("derived"):
                continue
            t = spec["t"]
            if t == "Id":
                out.append(f'{name}="{ids.get(int(val), "")}"')
            elif t == "List<Id>":
                out.append(f'{name}="{ids.get(int(val), "")}"')
            elif "accepts" in spec:
                opts = spec["accepts"]
                out.append(f'{name}="{opts[int(val)] if int(val) < len(opts) else int(val)}"')
            elif t == "Color":
                out.append(f'{name}="{int(val):08X}"')
            elif t == "bool":
                out.append(f'{name}="{"true" if val else "false"}"')
            elif t == "double":
                out.append(f'{name}="{fmt_num(val)}"')
            elif t == "String":
                out.append(f'{name}="{esc(val)}"')
            else:
                out.append(f'{name}="{int(val)}"')
        out.append(f'id="{ids[index]}"')
        return " ".join(out)

    lines = []

    def emit(obj, depth):
        i = obj["_index"]
        if i in dropped:
            return
        tag = obj["type"]
        a = attrs(obj, i)
        pad = indent * depth
        kids = obj["_children"]
        if kids:
            lines.append(f"{pad}<{tag} {a}>")
            for c in kids:
                emit(c, depth + 1)
            lines.append(f"{pad}</{tag}>")
        else:
            lines.append(f"{pad}<{tag} {a}/>")

    root = objs[0]
    name = artboard_name or group["name"]
    p = group["props"]
    head = (f'{indent}<Artboard name="{esc(name)}" '
            f'width="{fmt_num(p.get("width", 0))}" '
            f'height="{fmt_num(p.get("height", 0))}" id="{ids[0]}">')
    lines.append(head)
    for c in root["_children"]:
        emit(c, 2)
    lines.append(f"{indent}</Artboard>")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("riv")
    ap.add_argument("--artboard", default=None)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--tree", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rml", action="store_true",
                    help="emit the artboard as RML on stdout")
    ap.add_argument("--prune", default="",
                    help="comma separated object indices to drop, with their children")
    ap.add_argument("--no-animations", action="store_true",
                    help="artwork only: leave the source timelines behind")
    ap.add_argument("--name", default=None, help="rename the emitted artboard")
    ap.add_argument("--rive", default=os.path.expanduser("~/.rive/bin/rive"))
    args = ap.parse_args()

    schema = load_schema(args.rive if os.path.exists(args.rive) else "rive")
    doc = parse(args.riv, schema)
    groups = artboards(doc, schema)

    if args.summary or not (args.tree or args.json or args.rml):
        print(f"{os.path.basename(args.riv)}  format {doc['version']}  "
              f"{len(doc['objects'])} objects  {len(groups)} artboards")
        counts = {}
        for o in doc["objects"]:
            counts[o["type"]] = counts.get(o["type"], 0) + 1
        for g in groups:
            p = g["props"]
            print(f"  [{g['name']}]  {p.get('width')}x{p.get('height')}  "
                  f"{len(g['objects'])} objects")
        print("  by type: " + ", ".join(
            f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])[:18]))
        if not (args.tree or args.json or args.rml):
            return

    picked = [g for g in groups if args.artboard in (None, g["name"])]
    if args.artboard and not picked:
        raise SystemExit(f"no artboard named {args.artboard!r}")

    for g in picked:
        root = build_tree(g, schema)
        if args.tree:
            print(f"\n=== {g['name']} ===")
            print_tree(root, schema)
        if args.json:
            def strip(n):
                return {"type": n["type"], "props": n["_named"],
                        "children": [strip(c) for c in n["_children"]]}
            print(json.dumps(strip(root), indent=1))
        if args.rml:
            prune = {int(x) for x in args.prune.split(",") if x.strip()}
            print('<Rive version="1" kind="fragment">')
            print(to_rml(g, schema, artboard_name=args.name, prune=prune,
                         keep_animations=not args.no_animations))
            print("</Rive>")


if __name__ == "__main__":
    main()
