"""Step (9) of the CKM note: split the UV counterterm couplings of the UFO by coupling order.

FeynRules' WriteUFO puts the electroweak and the QCD parts of a UV counterterm (the CT parameters FJ...re/im of order QED 2,
and FJ...qcdre/qcdim, FJdlngsre of order QCD 2) into one coupling with one order, that of the QCD part (the tree order plus
QCD 2).  MadLoop then counts the electroweak part as a QCD counterterm: [virt=QED] misses it and [virt=QCD] includes it.
This script splits every such coupling of CT_couplings.py into its QCD terms (the name and order kept) and its electroweak
terms (name + "_ew", the order with QCD 2 replaced by QED 2), and lists both in CT_vertices.py (MadGraph accepts a list of
couplings for one colour and Lorentz structure and splits the interaction by order).  The couplings with one kind of CT
parameter (the names of CT_parameters.py) are checked to carry an order that contains it.
Usage: python3 nlo_ckm_ufo_split.py <UFO directory>   (called by nlo_ckm_ufo.wl; a second run finds nothing to split)
"""
import ast
import os
import re
import sys

ufo = sys.argv[1]
QCD_PAR = re.compile(r"^FJ\w*qcd(re|im)$|^FJdlngsre$")
CT_PAR = set(re.findall(r"^(\w+) = CTParameter\(", open(os.path.join(ufo, "CT_parameters.py")).read(), re.M))
src = open(os.path.join(ufo, "CT_couplings.py")).read()
pat = re.compile(r"(\w+) = Coupling\(name = '(\w+)',\s*value = '([^']*)',\s*order = (\{[^}]*\})\)")


def terms(expr):
    """the signed terms of a sum, as (sign, ast node)"""
    out = []

    def walk(n, sign):
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub)):
            walk(n.left, sign)
            walk(n.right, sign if isinstance(n.op, ast.Add) else -sign)
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            walk(n.operand, -sign)
        else:
            out.append((sign, n))
    walk(ast.parse(expr, mode="eval").body, 1)
    return out


def kind(node):
    names = {x.id for x in ast.walk(node) if isinstance(x, ast.Name) and x.id in CT_PAR}
    q, e = any(QCD_PAR.match(x) for x in names), any(not QCD_PAR.match(x) for x in names)
    assert not (q and e), "a term with both kinds of CT parameter: " + ast.unparse(node)
    return "QCD" if q else "EW" if e else None


def join(ts):
    s = ""
    for sign, n in ts:
        t = ast.unparse(n)
        s += (" - " if sign < 0 else (" + " if s else "")) + ("(" + t + ")" if s or sign < 0 else t)
    return s.lstrip(" +")


split, bad = [], []


def fix(m):
    var, name, val, order = m.groups()
    o = ast.literal_eval(order)
    ts = terms(val)
    kinds = {kind(n) for _, n in ts} - {None}
    if kinds == {"QCD", "EW"}:
        assert o.get("QCD", 0) >= 2, (name, o)
        qcd = [t for t in ts if kind(t[1]) == "QCD"]
        ew = [t for t in ts if kind(t[1]) != "QCD"]
        oew = dict(o)
        oew["QCD"] -= 2
        oew["QED"] = oew.get("QED", 0) + 2
        oew = {k: v for k, v in oew.items() if v}
        split.append(name)
        fmt = lambda d: "{" + ",".join("'%s':%d" % kv for kv in sorted(d.items())) + "}"
        return ("%s = Coupling(name = '%s',\n%svalue = '%s',\n%sorder = %s)\n\n%s_ew = Coupling(name = '%s_ew',\n%svalue = '%s',\n"
                "%sorder = %s)" % (var, name, " " * (len(var) + 15), join(qcd), " " * (len(var) + 15), fmt(o),
                                   var, name, " " * (len(var) + 18), join(ew), " " * (len(var) + 18), fmt(oew)))
    if kinds == {"QCD"} and o.get("QCD", 0) < 2 or kinds == {"EW"} and o.get("QED", 0) < 1:
        bad.append((name, order))
    return m.group(0)


new = pat.sub(fix, src)
if bad:
    print("couplings whose order does not contain their CT parameters:", bad)
    sys.exit(1)
open(os.path.join(ufo, "CT_couplings.py"), "w").write(new)
vsrc = open(os.path.join(ufo, "CT_vertices.py")).read()
n_rep = 0
for name in split:
    vsrc, k = re.subn(r"\bC\.%s(?=[,}])" % name, "[C.%s,C.%s_ew]" % (name, name), vsrc)
    n_rep += k
open(os.path.join(ufo, "CT_vertices.py"), "w").write(vsrc)
print("split %d CT couplings into QCD and electroweak parts (%d entries in CT_vertices.py)" % (len(split), n_rep))
