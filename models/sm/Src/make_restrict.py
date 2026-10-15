"""make_restrict.py -- write MadGraph's restriction card restrict_massless.dat for the SM UFO (models/sm, step (1)).

Usage:  python make_restrict.py <UFO directory>

The card is the default parameter card of the UFO (external parameters of parameters.py) with
  cabi = 0 (CKM = 1) and the masses and Yukawa couplings of e, mu, u, d, s, c set to 0,
so that MadGraph removes the corresponding couplings, as in its own sm model (restrict_default.dat).
Parameters are read from parameters.py with regular expressions (the FeynRules UFO is Python 2 code).
"""
import os
import re
import sys

ufo = sys.argv[1]
text = open(os.path.join(ufo, "parameters.py")).read()
pattern = re.compile(r"(\w+) = Parameter\(name = '(\w+)',\s*nature = 'external',\s*type = '\w+',\s*value = ([^,]+),"
                     r".*?lhablock = '(\w+)',\s*lhacode = \[ ([\d, ]+) \]\)", re.S)
zero = {"cabi", "Me", "MMU", "MU", "MD", "MS", "MC", "yme", "ymm", "ymup", "ymdo", "yms", "ymc"}
blocks = {}
for _, name, value, block, code in pattern.findall(text):
    val = 0.0 if name in zero else float(value)
    blocks.setdefault(block, []).append(([int(c) for c in code.split(",")], val, name))
found = {n for entries in blocks.values() for _, _, n in entries}
missing = zero - found
if missing:
    sys.exit("parameters not found: %s" % sorted(missing))
lines = ["# restrict_massless.dat -- written by make_restrict.py (models/sm, step (1))"]
for block in sorted(b for b in blocks if b != "DECAY"):
    lines.append("BLOCK %s" % block)
    for code, val, name in sorted(blocks[block]):
        lines.append("    %s %.10e # %s" % (" ".join(str(c) for c in code), val, name))
for code, val, name in sorted(blocks.get("DECAY", [])):
    lines.append("DECAY %d %.10e # %s" % (code[0], val, name))
open(os.path.join(ufo, "restrict_massless.dat"), "w").write("\n".join(lines) + "\n")
print("wrote %s: %d blocks, %d parameters, set to 0: %s"
      % (os.path.join(ufo, "restrict_massless.dat"), len(blocks), len(found), ", ".join(sorted(zero))))
