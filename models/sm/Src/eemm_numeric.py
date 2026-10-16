# %% [markdown]
# # Step (6): the one-loop e- e+ -> mu- mu+ virtual correction -- MadLoop (NLOCT model) against FormCalc (SM.mod)
#
# Research note models/sm, step (6).  On-shell renormalization with alpha(0) (the note's scheme), all fermion masses kept,
# Feynman gauge, widths zero, mu_R = MZ, the soft poles dimensionally regularized (photon massless).
#   python eemm_numeric.py --points          writes work/eemm_points.csv (sqrt(s), cos(theta), s, t) and the MadLoop
#                                            momenta work/eemm_ps_<n>.txt
#   python eemm_numeric.py --collier-input   writes work/eemm_collier_in.txt from results/eemm_functions.csv
#   python eemm_numeric.py                   compares (needs results/eemm_coeffs.csv, eemm_functions.csv, eemm_collier.csv
#                                            and the MadLoop standalone program work/ml_eemm)
# FormCalc (eemm_formcalc.wl) gives W = sum over spins of M0^* M1 = c_0 + sum_i c_i f_i (f_i the loop functions; the
# marker Finite of FormCalc's rational terms is 1) and B = sum over spins |M0|^2.  MadLoop returns the spin-averaged
# born = B/4 and finite = Re W/2, 1eps = Re(IR pole of W)/2 (the UV poles cancel against the counterterms).
# The loop functions: LoopTools (all; its C0 is wrong below threshold in this build), COLLIER (all).
# Writes results/eemm_comparison.csv.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%).

# %%
import csv
import math
import os
import re
import subprocess
import sys

import mpmath as mp

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
mp.mp.dps = 40
# --heavy: the cross-check with heavier leptons (m_e = 2, m_mu = 3 GeV; files *_heavy, MadLoop work/ml_eemm_heavy)
HEAVY = "--heavy" in sys.argv
TAG = "_heavy" if HEAVY else ""
MASSES = {"": (mp.mpf("0.00051099895"), mp.mpf("0.1056583755")), "_heavy": (mp.mpf(2), mp.mpf(3))}
ME, MMU = MASSES[TAG]
MZ = mp.mpf("91.1880")
POINTS = [(30, "0.5"), (200, "0.3"), (500, "-0.6")]       # sqrt(s) in GeV, cos(theta) of the mu- against the e-


def momenta(rs, c, me=None, mmu=None):
    """e-(p1) along +z, e+(p2), mu-(p3) at angle theta, mu+(p4); returns the four momenta and t = (p1 - p3)^2"""
    ME, MMU = (me, mmu) if me is not None else (globals()["ME"], globals()["MMU"])
    rs, c = mp.mpf(rs), mp.mpf(c)
    e = rs / 2
    p, k = mp.sqrt(e * e - ME ** 2), mp.sqrt(e * e - MMU ** 2)
    st = mp.sqrt(1 - c * c)
    moms = [(e, 0, 0, p), (e, 0, 0, -p), (e, k * st, 0, k * c), (e, -k * st, 0, -k * c)]
    t = ME ** 2 + MMU ** 2 - 2 * (e * e - p * k * c)
    return moms, t


def write_points():
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    for tag, (me, mmu) in MASSES.items():
        with open(os.path.join(HERE, "work", f"eemm_points{tag}.csv"), "w") as f:
            f.write("rs,cos,s,t\n")
            for rs, c in POINTS:
                moms, t = momenta(rs, c, me, mmu)
                f.write(f"{rs},{c},{mp.nstr(mp.mpf(rs) ** 2, 25)},{mp.nstr(t, 25)}\n")
        print(f"wrote work/eemm_points{tag}.csv")


KINDS = {"A0": "A0", "aa0": "A0", "bb0": "B0", "bb1": "B1", "bb00": "B00", "bb11": "B11", "dbb0": "DB0", "dbb1": "DB1",
         "dbb00": "DB00", "dbb11": "DB11", "cc0": "C0", "dd0": "D0"}


def parse_key(key):
    """'B0i[bb0, 1.*^4, 0, 8315.25]' -> ('B0', [1e4, 0, 8315.25]); 'A0[m2]' -> ('A0', [m2])"""
    head, body = re.match(r"(\w+)\[(.*)\]$", key).groups()
    args = [a.strip().replace("*^", "e") for a in body.split(",")]
    if head == "A0":
        return "A0", args
    return KINDS[args[0]], args[1:]


def read_functions():
    """key, kind, args and the LoopTools values (the last six columns: re/im of finite part, UV and IR coefficient)"""
    out = []
    with open(os.path.join(HERE, "results", f"eemm_functions{TAG}.csv")) as f:
        rows = list(csv.reader(f))[1:]
    for r in rows:
        kind, args = parse_key(r[0])
        v = [float(x) for x in r[-6:]]
        out.append({"key": r[0], "kind": kind, "args": args,
                    "lt": {"fin": complex(v[0], v[1]), "uv": complex(v[2], v[3]), "ir": complex(v[4], v[5])}})
    return out


def write_collier_input():
    rows = read_functions()
    with open(os.path.join(HERE, "work", f"eemm_collier_in{TAG}.txt"), "w") as f:
        for i, r in enumerate(rows, 1):
            f.write(f"{i} {r['kind']} {len(r['args'])} " + " ".join(r["args"]) + "\n")
    print(f"wrote {len(rows)} functions to work/eemm_collier_in{TAG}.txt")


if __name__ == "__main__" and "--points" in sys.argv:
    write_points()
    sys.exit(0)
if __name__ == "__main__" and "--collier-input" in sys.argv:
    write_collier_input()
    sys.exit(0)

# %% [markdown]
# ## FormCalc's coefficients and the loop functions from LoopTools and COLLIER

# %%
funcs = read_functions()
lt = {r["key"]: r["lt"] for r in funcs}
coll = {}
with open(os.path.join(HERE, "results", f"eemm_collier{TAG}.csv")) as f:
    for r in csv.DictReader(f):
        key = funcs[int(r["index"]) - 1]["key"]
        coll[key] = {k: complex(float(r[f"re_{k}"]), float(r[f"im_{k}"])) for k in ("fin", "uv", "ir")}
coeffs = {}
with open(os.path.join(HERE, "results", f"eemm_coeffs{TAG}.csv")) as f:
    for r in csv.DictReader(f):
        pt = (float(r["rs"]), float(r["cos"]))
        coeffs.setdefault(pt, {})[r["key"]] = complex(float(r["re"]), float(r["im"]))


def assemble(pt, lib):
    """W per part: fin (Finite = 1), uv and ir pole coefficients, with the loop functions of lib"""
    c = coeffs[pt]
    out = {"fin": c["const"] + c.get("Finite", 0), "uv": 0j, "ir": 0j}
    for key, ci in c.items():
        if key in ("born", "const", "Finite"):
            continue
        # FormCalc's renormalization constants are real parts of self-energies: "Re:"/"Im:" take the real or imaginary part
        # of each part (finite, UV and IR coefficients) of the function
        if key.startswith("Re:"):
            f = {part: complex(v.real) for part, v in lib[key[3:]].items()}
        elif key.startswith("Im:"):
            f = {part: complex(v.imag) for part, v in lib[key[3:]].items()}
        else:
            f = lib[key]
        for part in out:
            out[part] += ci * f[part]
    return out


# where LoopTools and COLLIER differ (relative 1e-8 on the finite part)
diff = sorted(((abs(lt[k]["fin"] - coll[k]["fin"]) / max(abs(coll[k]["fin"]), 1e-300), k) for k in lt), reverse=True)
print(f"{len(lt)} loop functions; LoopTools against COLLIER (finite part), largest relative differences:")
for d, k in diff[:6]:
    print(f"   {d:9.2e}  {k}   LoopTools {lt[k]['fin']:.12g}   COLLIER {coll[k]['fin']:.12g}")
print(f"   functions differing by more than 1e-8: {sum(1 for d, _ in diff if d > 1e-8)}")

# the FormCalc values alone (UV pole, IR pole, finite part of W) with both libraries
for rs, cs in POINTS:
    pt = (float(rs), float(cs))
    for name, lib in (("COLLIER", coll), ("LoopTools", lt)):
        w = assemble(pt, lib)
        print(f"FormCalc with {name:9}: sqrt(s) = {rs:3}, cos = {cs:>4}:  B/4 = {coeffs[pt]['born'].real / 4:.12e}  "
              f"Re W/2: finite {w['fin'].real / 2:+.12e}, IR pole {w['ir'].real / 2:+.12e}, UV pole {abs(w['uv']):.1e}")
if not os.path.isdir(os.path.join(HERE, "work", f"ml_eemm{TAG}")):
    sys.exit(0)

# %% [markdown]
# ## MadLoop

# %%
def run_madloop(rs, c, mu):
    base = os.path.join(HERE, "work", f"ml_eemm{TAG}", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    moms, _ = momenta(rs, c)
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines(" ".join(mp.nstr(x, 20, min_fixed=-30, max_fixed=30) for x in m) + "\n" for m in moms)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write(f"{mp.nstr(mu, 20)}\n")
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1).replace("D", "E"))
            for key in ("born", "finite", "1eps", "2eps")}


rows = []
print(f"\n{'sqrt(s)':>7} {'cos':>5} {'':10} {'MadLoop':>24} {'FormCalc (COLLIER)':>24} {'rel. diff.':>10} {'FormCalc (LoopTools)':>24}")
for rs, cs in POINTS:
    pt = (float(rs), float(cs))
    ml = run_madloop(rs, cs, MZ)
    b4 = coeffs[pt]["born"].real / 4
    wc, wl = assemble(pt, coll), assemble(pt, lt)
    comp = {"born": (ml["born"], b4, b4), "finite": (ml["finite"], wc["fin"].real / 2, wl["fin"].real / 2),
            "1eps": (ml["1eps"], wc["ir"].real / 2, wl["ir"].real / 2), "2eps": (ml["2eps"], 0.0, 0.0)}
    for key, (m, fc, fl) in comp.items():
        rel = abs(m / fc - 1) if fc != 0 else abs(m)
        print(f"{rs:7} {cs:>5} {key:10} {m:24.15e} {fc:24.15e} {rel:10.1e} {fl:24.15e}")
        rows.append([rs, cs, key, m, fc, fl, rel])
    print(f"{'':14} UV pole of W with the counterterms (expect 0): COLLIER {abs(wc['uv']):.1e}, LoopTools {abs(wl['uv']):.1e};"
          f"  virtual/born = {ml['finite'] / ml['born']:.10f}")

with open(os.path.join(HERE, "results", f"eemm_comparison{TAG}.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rs", "cos", "quantity", "madloop", "formcalc_collier", "formcalc_looptools", "rel_diff"])
    for r in rows:
        w.writerow(r[:3] + [repr(x) for x in r[3:]])
print(f"wrote results/eemm_comparison{TAG}.csv")
