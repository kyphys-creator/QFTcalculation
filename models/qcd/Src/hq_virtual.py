# %% [markdown]
# # Step (9): the one-loop virtual correction from MadLoop on a grid of scattering angles
#
# Research note models/qcd, step (9).  Uses the MadLoop standalone programs of step (5) (work/ml_A: u u~ > t t~, work/ml_B: g g > t t~,
# NLOCT UFO, alpha_s^(n_l), pole mass m = 1, aS = 1/(4 pi), check_sa.f reading PS.input and MU_R.input; built by run_madloop_check.sh)
# with mu_R = m, at Gauss-Legendre nodes in v = ln((1 + b c)/(1 - b c)) (dc = (1 - b^2 c^2)/(2 b) dv flattens the t- and u-channel peaks).
# Stores K W^(4)_fin, K W^(4)_{-1}, K W^(4)_{-2} (sums over 4-dimensional external states, MS-bar e^(-eps gamma) normalization:
# MadLoop's finite part is ours + (pi^2/12) x double pole) and the weights of (1/2) int dc.  -> work/hq/ml_scan.json
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python hq_virtual.py s1,s2,... [n]   (n = 64 nodes; about 1 minute for 20 values of s)

# %%
import numpy as np, subprocess, os, re, sys, json
from fractions import Fraction
try:
    SRC = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SRC = os.getcwd()
KK = (4*np.pi)**2; AVG = {"A": 36, "B": 256}
svals = [Fraction(x) for x in sys.argv[1].split(",")]
skey = lambda f: str(f).replace('/', 'o')
NGL = int(sys.argv[2]) if len(sys.argv) > 2 else 40
xg, wg = np.polynomial.legendre.leggauss(NGL)
def pdir(proc):
    base = os.path.join(SRC, "work", f"ml_{proc}", "SubProcesses")
    return os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
for proc in "AB":
    with open(os.path.join(pdir(proc), "MU_R.input"), "w") as fh: fh.write("%.17e\n" % 1.0)
out = {}
for sf in svals:
    s = float(sf); b = np.sqrt(1 - 4/s); E = np.sqrt(s)/2; k = b*E
    # rapidity-like variable v = ln((1+b c)/(1-b c)) flattens the t- and u-channel peaks: dc = (1 - b^2 c^2)/(2 b) dv
    Lv = np.log((1+b)/(1-b)); cs = np.tanh(xg*Lv/2)/b; ws = 0.5*wg*Lv*(1 - b*b*cs*cs)/(2*b)   # 1/2 int dc f = sum ws f
    for proc in "AB":
        rows = []
        for c in cs:
            st = np.sqrt(1-c*c)
            P = [(E,0,0,E),(E,0,0,-E),(E,k*st,0,k*c),(E,-k*st,0,-k*c)]
            with open(os.path.join(pdir(proc), "PS.input"), "w") as fh:
                fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in P)
            o = subprocess.run(["./check"], cwd=pdir(proc), capture_output=True, text=True, check=True).stdout
            v = {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, o).group(1)) for key in ("born","finite","1eps","2eps")}
            a = AVG[proc]
            rows.append({"c": c, "t": 1-s/2*(1-b*c), "born4": v["born"]*a, "KW4m2": KK*a/2*v["2eps"], "KW4m1": KK*a/2*v["1eps"],
                         "KW4fin": KK*a/2*(v["finite"]-np.pi**2/12*v["2eps"])})
        out[f"{proc}_{skey(sf)}"] = {"s": s, "beta": b, "w": list(ws), "rows": rows}
        print(proc, sf, "done", flush=True)
os.makedirs(os.path.join(SRC, "work", "hq"), exist_ok=True)
json.dump(out, open(os.path.join(SRC, "work", "hq", "ml_scan.json"), "w"), indent=1)
