# ufo_digits.py -- keep the full double precision of the numbers in a UFO's CT_couplings.py through MadGraph.
#
# Research note models/sm, step (6).  MadGraph's UFO-to-Fortran converter writes every number with '%e', i.e. with 7
# significant digits.  nlo_ufo.wl writes the counterterm couplings as numbers (17 significant digits); this script
# rewrites each number with more than 7 significant digits as a sum of three 7-digit integers times powers of ten,
#   0.012345678901234567 -> (1234567*1e-08+8901234*1e-15+5670000*1e-22),
# which MadGraph converts exactly (small integers and powers of ten).  Usage: python ufo_digits.py <UFO directory> ...
import re
import sys
from decimal import Decimal, getcontext

getcontext().prec = 40
NUM = re.compile(r"(?<![\w.])(\d+\.\d*(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+|\.\d+(?:[eE][-+]?\d+)?)")


def split(lit):
    d = Decimal(lit)
    digits = len(d.normalize().as_tuple().digits)
    if d == 0 or digits <= 7:
        return lit
    e = d.adjusted()                       # d = 0.d1d2... x 10^(e+1)
    n = int((d.scaleb(20 - e)).to_integral_value())   # 21 significant digits
    parts = [(n // 10 ** 14, e - 6), ((n // 10 ** 7) % 10 ** 7, e - 13), (n % 10 ** 7, e - 20)]
    terms = [f"{m}*1e{p}" for m, p in parts if m != 0]
    return "(" + "+".join(terms) + ")"


for ufo in sys.argv[1:]:
    path = f"{ufo}/CT_couplings.py"
    txt = open(path).read()
    count = [0]

    def repl(m):
        new = split(m.group(1))
        if new != m.group(1):
            count[0] += 1
        return new

    open(path, "w").write(NUM.sub(repl, txt))
    print(f"{path}: {count[0]} numbers split into 7-digit pieces")
