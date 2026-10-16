#!/usr/bin/env python3
"""Write MadGraph restriction cards for the UFO of SM.fr (step (1) of the SM note).

FeynRules' parameters.py is read with regular expressions (it is written for Python 2 and is not imported here).
Every external parameter keeps its benchmark value except the ones listed below, which are set to 0; MadGraph then
drops the vanishing couplings.  The gauge parameters xiA, xiZ, xiW, xiG have the value 1 (Feynman gauge) and are
fixed to 1 by the restriction, as MadGraph does with every parameter equal to 1.

  restrict_massless.dat : all fermions massless except the top quark (Yukawa coupling only for the top)

Usage:  python3 make_restrict.py generated/SM_UFO     (writes the cards into that folder)
"""
import re
import sys
from pathlib import Path

ZERO = {"massless": {"Me", "MMU", "MTA", "MU", "MC", "MD", "MS", "MB"}}

def externals(ufo):
    text = (Path(ufo) / "parameters.py").read_text()
    pat = re.compile(r"(\w+)\s*=\s*Parameter\(name\s*=\s*'(\w+)',\s*nature\s*=\s*'external',.*?value\s*=\s*([^,]+),"
                     r".*?lhablock\s*=\s*'(\w+)',\s*lhacode\s*=\s*\[\s*([\d,\s]+)\]", re.S)
    out = []
    for m in pat.finditer(text):
        name, value, block, code = m.group(2), float(m.group(3)), m.group(4), m.group(5)
        out.append((block, [int(c) for c in code.split(",")], name, value))
    return out

def write_card(ufo, tag, zero):
    pars = externals(ufo)
    lines = ["# restriction card written by make_restrict.py (" + tag + ")"]
    blocks = {}
    for block, code, name, value in pars:
        blocks.setdefault(block, []).append((code, name, 0.0 if name in zero else value))
    for block in sorted(blocks):
        if block == "DECAY":
            continue
        lines.append("Block " + block)
        for code, name, value in sorted(blocks[block]):
            lines.append("  " + " ".join(str(c) for c in code) + "  %.10e  # %s" % (value, name))
    for code, name, value in sorted(blocks.get("DECAY", [])):
        lines.append("DECAY  %d  %.10e  # %s" % (code[0], value, name))
    path = Path(ufo) / ("restrict_" + tag + ".dat")
    path.write_text("\n".join(lines) + "\n")
    missing = zero - {p[2] for p in pars}
    print("wrote", path, "with", len(pars), "external parameters; set to 0:", sorted(zero & {p[2] for p in pars}),
          "; not found:", sorted(missing))

if __name__ == "__main__":
    ufo = sys.argv[1] if len(sys.argv) > 1 else "generated/SM_UFO"
    for tag, zero in ZERO.items():
        write_card(ufo, tag, zero)
