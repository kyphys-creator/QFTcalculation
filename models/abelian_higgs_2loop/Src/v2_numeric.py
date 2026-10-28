# %% [markdown]
# # Step (1): numbers of the two-loop effective potential in Landau gauge (TSIL against AMFlow)
#
# Research note models/abelian_higgs_2loop, step (1).  Benchmark couplings e = 1/2, lam = 25/32, m2 = 25/8 (v = 2,
# MA = 1, MH = 5/2), Q = 1, background fields phi = 2 (tree minimum, xg = 0) and phi = 3.
#   (a) the vacuum sunrise I(x,y,z) for the 11 mass triples of V2: TSIL 1.46 (work/v2_tsil, analytic) against AMFlow 2.0
#       (results/v2_amflow.csv, auxiliary mass flow, 30 digits);
#   (b) V0, V1/K and V2/K^2 (K = 16 pi^2, Landau gauge, Eq. (V2) of the note) at the two points, with either set of I.
# Writes results/v2_numeric.csv.  Usage (from Src/, after v2_amflow.wl and building work/v2_tsil):
#     ~/miniforge3/envs/qft/bin/python v2_numeric.py

# %%
import csv
import math
import os
import subprocess

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
E, LAM, M2 = 0.5, 25 / 32, 25 / 8
K = 16 * math.pi ** 2


def masses(phi):
    return -M2 + 3 * LAM * phi ** 2, -M2 + LAM * phi ** 2, E ** 2 * phi ** 2


def A(x):
    return 0.0 if x == 0 else x * (math.log(x) - 1)


# %% [markdown]
# ## (a) I(x,y,z): TSIL against AMFlow

# %%
with open(os.path.join(HERE, "results", "v2_amflow.csv")) as fh:
    am = [(float(r["x"]), float(r["y"]), float(r["z"]), float(r["I"])) for r in csv.DictReader(fh)]
inp = "".join("%.17g,%.17g,%.17g\n" % t[:3] for t in am)
out = subprocess.run([os.path.join(HERE, "work", "v2_tsil")], input=inp, capture_output=True, text=True, check=True).stdout
ts = {(float(r["x"]), float(r["y"]), float(r["z"])): float(r["I"]) for r in csv.DictReader(out.splitlines())}
Itab = {}
worst = 0.0
for x, y, z, ia in am:
    it = ts[(x, y, z)]
    worst = max(worst, abs(it / ia - 1))
    Itab[(x, y, z)] = (it, ia)
    print("(a) I(%.6g, %.6g, %.6g): TSIL %.15f, AMFlow %.15f, relative difference %.1e" % (x, y, z, it, ia, it / ia - 1))
print("(a) largest relative difference over the %d sunrises: %.1e" % (len(am), worst))


# %% [markdown]
# ## (b) V0, V1 and V2 at phi = 2 and 3

# %%
def I(x, y, z, k):
    return Itab[tuple(sorted((x, y, z)))][k]


def fSSV(x, y, z, k):
    lk = -x * x - y * y - z * z + 2 * x * y + 2 * x * z + 2 * y * z
    return (lk * I(x, y, z, k) + (x - y) ** 2 * I(0, x, y, k) + (y - x - z) * A(x) * A(z) + (x - y - z) * A(y) * A(z)
            + z * A(x) * A(y)) / z + 2 * (x + y - z / 3) * A(z)


def fVS(x, y):
    return 3 * A(x) * A(y) + 2 * x * A(y)


def fVVS(x, y, z, k):
    c = -x * x - y * y - z * z - 10 * x * y + 2 * x * z + 2 * y * z
    return ((c * I(x, y, z, k) + (x - z) ** 2 * I(0, x, z, k) + (y - z) ** 2 * I(0, y, z, k) - z * z * I(0, 0, z, k)
             + (z - x - y) * A(x) * A(y) + y * A(x) * A(z) + x * A(y) * A(z)) / (4 * x * y)
            + A(x) / 2 + A(y) / 2 + 2 * A(z) - x - y - z)


def V2(phi, k):
    xh, xg, xa = masses(phi)
    return (-3 * LAM ** 2 * phi ** 2 * I(xh, xh, xh, k) - LAM ** 2 * phi ** 2 * I(xh, xg, xg, k)
            + 0.75 * LAM * (A(xh) ** 2 + A(xg) ** 2) + 0.5 * LAM * A(xh) * A(xg)
            + E ** 2 / 2 * fSSV(xh, xg, xa, k) + E ** 2 / 2 * (fVS(xa, xh) + fVS(xa, xg)) + E ** 4 * phi ** 2 * fVVS(xa, xa, xh, k))


def V1(phi):
    xh, xg, xa = masses(phi)
    f = lambda x, c: 0.0 if x == 0 else x * x * (math.log(x) - c)
    return (f(xh, 1.5) + f(xg, 1.5) + 3 * f(xa, 5 / 6)) / 4


rows = []
for phi in (2.0, 3.0):
    v0 = -M2 * phi ** 2 / 2 + LAM * phi ** 4 / 4
    v1, v2t, v2a = V1(phi) / K, V2(phi, 0) / K ** 2, V2(phi, 1) / K ** 2
    print("(b) phi = %g: V0 = %.10f, V1/K = %.10f, V2/K^2 = %.12e (TSIL), %.12e (AMFlow), relative difference %.1e"
          % (phi, v0, v1, v2t, v2a, v2t / v2a - 1))
    rows.append([phi, v0, v1, v2t, v2a])
with open(os.path.join(HERE, "results", "v2_numeric.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["phi", "V0", "V1_over_K", "V2_over_K2_TSIL", "V2_over_K2_AMFlow"])
    for r in rows:
        w.writerow(["%.17g" % x for x in r])
print("written results/v2_numeric.csv")
