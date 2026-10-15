# %% [markdown]
# # Step (4): the loop functions of the on-shell counterterms -- LoopTools against mpmath (Standard Model)
#
# Research note models/sm, step (4).  The note's counterterms (ct_feyncalc.wl, section (c)) need B0 and its derivative
# DB0 = dB0/dp^2 at p^2 = 0, M_W^2, M_Z^2, M_H^2.  ct_formcalc.wl evaluates them with LoopTools (Delta = 0, mu = M_Z) and
# writes results/ct_functions.csv; here they are recomputed independently:
#   B0(p^2; m1^2, m2^2) = -int_0^1 dx ln[(x m2^2 + (1-x) m1^2 - x(1-x) p^2 - i0)/mu^2]   (mpmath, 30 digits),
#   DB0 = the numerical derivative of that integral in p^2 (mpmath.diff), except the IR-divergent DB0(m^2; 0, m^2)
#   (the photon in the W self-energy), which LoopTools regularizes with the photon mass lambda: its value
#   -[1 + ln(lambda^2/m^2)/2]/m^2 is compared with the closed form.
# Batch: `~/miniforge3/envs/qft/bin/python ct_numeric.py` (from Src/).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import os

import mpmath as mp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
MU2 = mp.mpf("91.1880") ** 2
LAMBDA2 = mp.mpf(1)


def log_m_i0(x):
    return mp.log(x) if x > 0 else mp.log(-x) - 1j * mp.pi


def b0_ref(p2, m1, m2):
    p2, m1, m2 = mp.mpf(p2), mp.mpf(m1), mp.mpf(m2)
    delta = lambda x: x * m2 + (1 - x) * m1 - x * (1 - x) * p2
    pts = [mp.mpf(0)]
    if p2 != 0:
        a, b, c = p2, m2 - m1 - p2, m1
        disc = b * b - 4 * a * c
        if disc > 0:
            pts += sorted(r for r in ((-b - mp.sqrt(disc)) / (2 * a), (-b + mp.sqrt(disc)) / (2 * a)) if 0 < r < 1)
    pts.append(mp.mpf(1))
    return -mp.quad(lambda x: log_m_i0(delta(x) / MU2) if delta(x) != 0 else 0, pts)


# %%
rows = list(csv.DictReader(open(os.path.join(HERE, "results", "ct_functions.csv"))))
worst = {"B0": 0.0, "DB0": 0.0}
for r in rows:
    p2, m1, m2 = mp.mpf(r["p2"]), mp.mpf(r["m1sq"]), mp.mpf(r["m2sq"])
    lt = complex(float(r["re_lt"]), float(r["im_lt"]))
    if r["func"] == "B0":
        ref = complex(b0_ref(p2, m1, m2))
    elif (m1 == 0 and m2 == p2) or (m2 == 0 and m1 == p2):
        m = m1 if m1 != 0 else m2
        ref = complex(-(1 + mp.log(LAMBDA2 / m) / 2) / m)
        print(f"IR-divergent DB0({float(p2):.6g}; 0, {float(m):.6g}) with lambda^2 = 1: LoopTools {lt.real:.15e}, "
              f"closed form {ref.real:.15e}, rel. diff. {abs(lt / ref - 1):.1e}")
    else:
        h = mp.mpf(10) ** -8 * max(abs(p2), mp.mpf(1))
        ref = complex(mp.diff(lambda x: b0_ref(x, m1, m2).real, p2, h=h)) + 1j * float(mp.diff(lambda x: b0_ref(x, m1, m2).imag, p2, h=h))
    dev = abs(lt - ref) / max(abs(ref), 1e-300)
    worst[r["func"]] = max(worst[r["func"]], dev)
print(f"{len(rows)} loop functions of the counterterms; max relative deviation LoopTools - mpmath: "
      f"B0 {worst['B0']:.1e}, DB0 {worst['DB0']:.1e}")
