# %% [markdown]
# # Step (1) of the NLO note: LO widths with MS-bar couplings and pole kinematics
#
# Eq. (lo) of the note: Gamma_0(Z -> f fbar), Gamma_0(W+ -> f fbar'), Gamma_0(t -> d_j W+), Gamma_0(H -> f fbar) with the
# MS-bar couplings at mu (nlo_inputs.py: the SM note's step (7) values run with the CKM note's one-loop equations) and the
# pole masses of nlo_inputs.POLE.  The default scale is the mass of the decaying particle; mu = M/2 and 2M show the
# scale dependence of the LO widths.
#   --cards: MadGraph param cards with the same couplings and kinematics (the UFO derives the couplings from aEWM1, MZ, MW):
#            Z card  MZ = pole, MW = MZ c(M_Z), 1/aEWM1 = alpha(M_Z);   W card  MW = pole, MZ = MW/c(M_W);
#            t card  MW = pole, MZ = MW/c(m_t), alpha(m_t);   H card (a check of the formula only: the UFO's Yukawa coupling
#            is sqrt(2) m/v with the kinematic mass) MZ = pole, MW = MZ c(M_H);  the CKM block of V(mu)
#   default: the widths, and MadGraph's compute_widths (work/widths_*.dat; the partial widths that it sets to zero below its
#            "QCD scale", t -> d W+ and t -> s W+, from work/lo_mg5.log) against Eq. (lo) with the card values.
# Writes results/lo_widths.csv, results/lo_mg5_comparison.csv.  Usage (from Src/): python3 lo_widths.py [--cards]

# %%
import csv
import math
import re
import sys
from pathlib import Path

import numpy as np

from nlo_inputs import POLE, at, std_params

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
WORK = HERE / "work"
RES.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

# fermions: (name, pdg, N_c, T3, Q, pole-mass key)
FERM = {"ve": (12, 1, 0.5, 0, None), "vm": (14, 1, 0.5, 0, None), "vt": (16, 1, 0.5, 0, None),
        "e": (11, 1, -0.5, -1, "Me"), "mu": (13, 1, -0.5, -1, "MMU"), "ta": (15, 1, -0.5, -1, "MTA"),
        "u": (2, 3, 0.5, 2 / 3, "MU"), "c": (4, 3, 0.5, 2 / 3, "MC"), "d": (1, 3, -0.5, -1 / 3, "MD"),
        "s": (3, 3, -0.5, -1 / 3, "MS"), "b": (5, 3, -0.5, -1 / 3, "MB")}
UP, DN = ("u", "c", "t"), ("d", "s", "b")


def mass(name, masses):
    k = FERM[name][4] if name in FERM else {"t": "MT"}[name]
    return 0.0 if k is None else masses[k]


def lam_k(a, b, c):
    return a * a + b * b + c * c - 2 * a * b - 2 * b * c - 2 * c * a


# %% [markdown]
# ## Eq. (lo)

# %%
def gamma_Z(f, gZ, s2, MZ, masses):
    _, nc, t3, q, _ = FERM[f]
    m = mass(f, masses)
    if 2 * m >= MZ:
        return 0.0
    b = math.sqrt(1 - 4 * m**2 / MZ**2)
    v, a = t3 - 2 * q * s2, t3
    return nc * gZ**2 * MZ / (48 * math.pi) * b * ((3 - b**2) / 2 * v**2 + b**2 * a**2)


def gamma_W(f1, f2, g, V2, MW, masses):
    """W+ -> f1 fbar2 with |V|^2 (1 for leptons)"""
    nc = 3 if f1 in UP else 1
    x1, x2 = mass(f1, masses)**2 / MW**2, mass(f2, masses)**2 / MW**2
    if math.sqrt(x1) + math.sqrt(x2) >= 1:
        return 0.0
    return nc * V2 * g**2 * MW / (48 * math.pi) * math.sqrt(lam_k(1, x1, x2)) * (1 - (x1 + x2) / 2 - (x1 - x2)**2 / 2)


def gamma_t(fd, g, V2, MW, mt, masses):
    xb, xw = mass(fd, masses)**2 / mt**2, MW**2 / mt**2
    return V2 * g**2 * mt**3 / (64 * math.pi * MW**2) * math.sqrt(lam_k(1, xb, xw)) * ((1 - xb)**2 + xw * (1 + xb) - 2 * xw**2)


def gamma_H(f, y, MH, masses):
    _, nc, _, _, _ = FERM[f]
    m = mass(f, masses)
    b = math.sqrt(1 - 4 * m**2 / MH**2)
    return nc * y**2 * MH / (16 * math.pi) * b**3


def widths(mus=None):
    """the LO widths at the scale factors xi (mu = xi M)"""
    rows = []
    for xi in (1.0, 0.5, 2.0):
        pz, pw, pt, ph = at(xi * POLE["MZ"]), at(xi * POLE["MW"]), at(xi * POLE["MT"]), at(xi * POLE["MH"])
        out = {}
        for f in ("ve", "e", "mu", "ta", "u", "c", "d", "s", "b"):
            out["Z_" + f] = gamma_Z(f, pz["gZ"], pz["s2"], POLE["MZ"], POLE)
        out["Z_total"] = 3 * out["Z_ve"] + out["Z_e"] + out["Z_mu"] + out["Z_ta"] + sum(out["Z_" + q] for q in "ucdsb")
        V2 = np.abs(pw["V"])**2
        for i, u in enumerate(UP[:2]):
            for j, d in enumerate(DN):
                out["W_%s%s" % (u, d)] = gamma_W(u, d, pw["g"], V2[i, j], POLE["MW"], POLE)
        for nu, l in (("ve", "e"), ("vm", "mu"), ("vt", "ta")):
            out["W_" + l] = gamma_W(nu, l, pw["g"], 1.0, POLE["MW"], POLE)
        out["W_total"] = sum(v for k, v in out.items() if k.startswith("W_"))
        V2t = np.abs(pt["V"])**2
        for j, d in enumerate(DN):
            out["t_" + d] = gamma_t(d, pt["g"], V2t[2, j], POLE["MW"], POLE["MT"], POLE)
        out["t_total"] = out["t_d"] + out["t_s"] + out["t_b"]
        out["H_b"] = gamma_H("b", ph["yd"][2], POLE["MH"], POLE)
        out["H_c"] = gamma_H("c", ph["yu"][1], POLE["MH"], POLE)
        out["H_ta"] = gamma_H("ta", ph["ye"][2], POLE["MH"], POLE)
        out["H_mu"] = gamma_H("mu", ph["ye"][1], POLE["MH"], POLE)
        rows.append((xi, out))
    return rows


# %% [markdown]
# ## MadGraph param cards with the same couplings and kinematics

# %%
def card_values(kind):
    if kind == "Z":
        p = at(POLE["MZ"]); MZ = POLE["MZ"]; MW = MZ * math.sqrt(1 - p["s2"])
    elif kind == "W":
        p = at(POLE["MW"]); MW = POLE["MW"]; MZ = MW / math.sqrt(1 - p["s2"])
    elif kind == "t":
        p = at(POLE["MT"]); MW = POLE["MW"]; MZ = MW / math.sqrt(1 - p["s2"])
    else:
        p = at(POLE["MH"]); MZ = POLE["MZ"]; MW = MZ * math.sqrt(1 - p["s2"])
    vals = {"aEWM1": 1 / p["alpha"], "aS": p["alphas"], "MZ": MZ, "MW": MW, "MH": POLE["MH"], "MT": POLE["MT"],
            "MB": POLE["MB"], "MC": POLE["MC"], "MS": POLE["MS"], "MD": POLE["MD"], "MU": POLE["MU"], "MTA": POLE["MTA"],
            "MMU": POLE["MMU"], "Me": POLE["Me"]}
    s12, s23, s13, dl = std_params(p["V"])
    vals.update({"s12": s12, "s23": s23, "s13": s13, "dCKM": dl})
    return p, vals


def write_card(path, vals):
    blocks = [("CKMBLOCK", [(1, "s12"), (2, "s23"), (3, "s13"), (4, "dCKM")]),
              ("GAUGE", [(1, "xiA"), (2, "xiZ"), (3, "xiW"), (4, "xiG")]),
              ("MASS", [(1, "MD"), (2, "MU"), (3, "MS"), (4, "MC"), (5, "MB"), (6, "MT"), (11, "Me"), (13, "MMU"), (15, "MTA"),
                        (23, "MZ"), (24, "MW"), (25, "MH")]),
              ("SMINPUTS", [(1, "aEWM1"), (3, "aS")])]
    v = dict(vals, xiA=1.0, xiZ=1.0, xiW=1.0, xiG=1.0)
    with open(path, "w") as fh:
        for name, entries in blocks:
            fh.write("BLOCK %s\n" % name)
            for code, key in entries:
                fh.write("    %d %.16e # %s\n" % (code, v[key], key))
        for pdg in (6, 23, 24, 25):
            fh.write("DECAY %d 0.000000e+00\n" % pdg)


def read_widths(path):
    out, parent = {}, None
    for line in open(path):
        m = re.match(r"DECAY\s+(\d+)\s+(\S+)", line)
        if m:
            parent = int(m.group(1)); out[(parent, "total")] = float(m.group(2)); continue
        m = re.match(r"\s+(\S+)\s+2\s+(-?\d+)\s+(-?\d+)\s+#\s+(\S+)", line)
        if m and parent is not None:
            out[(parent, tuple(sorted((int(m.group(2)), int(m.group(3))))))] = float(m.group(4))
    return out


if len(sys.argv) > 1 and sys.argv[1] == "--cards":
    for kind in "ZWtH":
        _, vals = card_values(kind)
        write_card(WORK / ("card_%s.dat" % kind), vals)
    with open(WORK / "lo_mg5.mg5", "w") as fh:
        fh.write("set automatic_html_opening False\nimport model ./work/SM_CKM_UFO\n")
        for kind, part in (("Z", "z"), ("W", "w+"), ("t", "t"), ("H", "h")):
            fh.write("compute_widths %s --body_decay=2 --min_br=0 --path=./work/card_%s.dat --output=./work/widths_%s.dat\n" % (part, kind, kind))
    print("wrote work/card_[ZWtH].dat and work/lo_mg5.mg5")
    sys.exit(0)

# %% [markdown]
# ## The widths and the comparison with MadGraph

# %%
rows = widths()
with open(RES / "lo_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    keys = list(rows[0][1])
    w.writerow(["quantity", "mu=M", "mu=M/2", "mu=2M"])
    for k in keys:
        w.writerow([k] + ["%.10e" % r[1][k] for r in rows])
lo = rows[0][1]
print("LO widths [GeV] at mu = M (mu = M/2, 2M):")
for k in ("Z_ve", "Z_e", "Z_ta", "Z_u", "Z_d", "Z_c", "Z_b", "Z_total", "W_e", "W_ud", "W_cs", "W_total", "t_b", "t_total",
          "H_b", "H_ta"):
    print("  %-8s %.6e   (%+.2f%%, %+.2f%%)" % (k, lo[k], 100 * (rows[1][1][k] / lo[k] - 1), 100 * (rows[2][1][k] / lo[k] - 1)))

# MadGraph against Eq. (lo) with the card values
cmp_rows = []
worst = 0.0
for kind, pdg in (("Z", 23), ("W", 24), ("t", 6), ("H", 25)):
    f = WORK / ("widths_%s.dat" % kind)
    if not f.exists():
        print("no", f); continue
    mg = read_widths(f)
    # MadGraph sets partial widths below its "QCD scale" to zero and prints them in the log
    if kind == "t":
        for m in re.finditer(r"partial width of particle t lower than QCD scale:(\S+)\. Set it to zero\. \(\[(\d+), (\d+)\]\)",
                             open(WORK / "lo_mg5.log").read()):
            mg[(6, tuple(sorted((int(m.group(2)), int(m.group(3))))))] = float(m.group(1))
    p, vals = card_values(kind)
    ee = math.sqrt(4 * math.pi / vals["aEWM1"]); cw = vals["MW"] / vals["MZ"]; sw2 = 1 - cw**2
    g, gZ = ee / math.sqrt(sw2), ee / math.sqrt(sw2) / cw
    V2 = np.abs(p["V"])**2
    vcard = 2 * vals["MW"] * math.sqrt(sw2) / ee
    mine = {}
    if kind == "Z":
        for f_ in ("ve", "vm", "vt", "e", "mu", "ta", "u", "c", "d", "s", "b"):
            pid = FERM[f_][0]
            mine[(pdg, (-pid, pid))] = (f_, gamma_Z(f_, gZ, sw2, vals["MZ"], vals))
    if kind == "W":
        for i, u in enumerate(UP[:2]):
            for j, d in enumerate(DN):
                mine[(pdg, tuple(sorted((FERM[u][0], -FERM[d][0]))))] = (u + d, gamma_W(u, d, g, V2[i, j], vals["MW"], vals))
        for nu, l in (("ve", "e"), ("vm", "mu"), ("vt", "ta")):
            mine[(pdg, tuple(sorted((FERM[nu][0], -FERM[l][0]))))] = (l + nu, gamma_W(nu, l, g, 1.0, vals["MW"], vals))
    if kind == "t":
        for j, d in enumerate(DN):
            mine[(pdg, tuple(sorted((FERM[d][0], 24))))] = (d + "W", gamma_t(d, g, V2[2, j], vals["MW"], vals["MT"], vals))
    if kind == "H":
        for f_ in ("b", "c", "ta", "mu"):
            pid = FERM[f_][0]
            mine[(pdg, (-pid, pid))] = (f_, gamma_H(f_, math.sqrt(2) * mass(f_, vals) / vcard, vals["MH"], vals))
    for key, (lab, val) in mine.items():
        if val == 0:
            continue
        m = mg.get(key)
        rel = (m / val - 1) if m else float("nan")
        worst = max(worst, abs(rel)) if m else worst
        cmp_rows.append([kind, lab, val, m if m else "", rel])
        print("  MadGraph %s -> %-5s %.12e vs Eq. (lo) %.12e (rel %+.1e)" % (kind, lab, m if m else float("nan"), val, rel))
print("MadGraph against Eq. (lo), largest relative difference: %.1e" % worst)
with open(RES / "lo_mg5_comparison.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["parent", "channel", "eq_lo", "madgraph", "rel"])
    w.writerows(cmp_rows)
print("wrote results/lo_widths.csv, results/lo_mg5_comparison.csv")
