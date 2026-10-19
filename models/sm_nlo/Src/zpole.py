"""Step (5) of the NLO note: sin^2 theta_eff and the Z-pole asymmetries from the effective couplings (results/zeff.csv, zeff.wl).

With x_f = Re V_f/A_f = 1 - 4 |Q_f| sin^2 theta_eff^f:
  A_f = 2 x_f/(1 + x_f^2),   A_FB^{0,f} = (3/4) A_e A_f
(the pole asymmetries of the LEP definition: the photon exchange, the photonic and gluonic final-state corrections and the
quark masses taken out).  At the tree level s^2(M_Z) (MS-bar, the full SM; no top decoupling) in place of sin^2 theta_eff.
Two sets of inputs: the note's (the SM note's M_W scheme; results/zeff.csv) and the SM note's alpha scheme (alpha(0) in place of M_W;
results/zeff_alpha.csv): one-loop determinations of g, g' that differ at higher order.  The measured values (LEP and SLD,
Phys. Rept. 427, 257 (2006): sin^2 theta_eff^lept from all asymmetries, A_l from SLD's A_LR and the lepton asymmetries) are references.  Writes results/zpole.csv.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
MZ = 91.1876
Q = {"e": -1, "mu": -1, "tau": -1, "u": 2 / 3, "c": 2 / 3, "d": -1 / 3, "s": -1 / 3, "b": -1 / 3}
NAME = {"l1": "e", "l2": "mu", "l3": "tau", "u1": "u", "u2": "c", "d1": "d", "d2": "s", "d3": "b"}   # zeff.wl's names
rows = [dict(r, fermion=NAME[r["fermion"]]) for r in csv.DictReader(open(HERE / "results" / "zeff.csv"))]
rows_a = [dict(r, fermion=NAME[r["fermion"]]) for r in csv.DictReader(open(HERE / "results" / "zeff_alpha.csv"))]
names = sorted({r["fermion"] for r in rows}, key=list(Q).index) if all(r["fermion"] in Q for r in rows) else None
if names is None:
    raise SystemExit("unexpected fermion names in zeff.csv: %s" % sorted({r["fermion"] for r in rows}))
s2eff = {(r["fermion"], round(float(r["mu"]), 3)): float(r["s2eff"]) for r in rows}
s2full = {(r["fermion"], round(float(r["mu"]), 3)): float(r["s2eff_full_ratio"]) for r in rows}
s2ms = {round(float(r["mu"]), 3): float(r["s2_msbar"]) for r in rows}
s2eff_a = {(r["fermion"], round(float(r["mu"]), 3)): float(r["s2eff"]) for r in rows_a}
s2ms_a = {round(float(r["mu"]), 3): float(r["s2_msbar"]) for r in rows_a}
spread = {r["fermion"]: float(r["xi_spread"]) for r in rows if r["xi_spread"]}
MUS = [round(MZ, 3), round(MZ / 2, 3), round(2 * MZ, 3)]


def asym(s2, f):
    x = 1 - 4 * abs(Q[f]) * s2
    return 2 * x / (1 + x * x)


def obs(s2of):
    a = {f: asym(s2of(f), f) for f in ("e", "b", "c")}
    return {"s2eff_lept": s2of("e"), "A_l": a["e"], "A_b": a["b"], "A_c": a["c"], "AFB0_l": 0.75 * a["e"]**2,
            "AFB0_b": 0.75 * a["e"] * a["b"], "AFB0_c": 0.75 * a["e"] * a["c"]}


MEAS = {"s2eff_lept": (0.23153, 0.00016), "A_l": (0.1513, 0.0021), "A_b": (0.923, 0.020), "A_c": (0.670, 0.027),
        "AFB0_l": (0.0171, 0.0010), "AFB0_b": (0.0992, 0.0016), "AFB0_c": (0.0707, 0.0035)}
print("sin^2 theta_eff^f at mu = M_Z (O(alpha); the gauge spread; the full ratio minus O(alpha)):")
for f in names:
    print("  %-4s %.8f  (s^2(M_Z) %.8f, kappa %.6f;  spread %.0e;  %+.1e)" % (
        f, s2eff[(f, MUS[0])], s2ms[MUS[0]], s2eff[(f, MUS[0])] / s2ms[MUS[0]], spread[f], s2full[(f, MUS[0])] - s2eff[(f, MUS[0])]))
print("mu = M_Z/2, M_Z, 2 M_Z:  s^2(mu) " + ", ".join("%.6f" % s2ms[m] for m in MUS[1:2] + MUS[:1] + MUS[2:]) +
      ";  sin^2 theta_eff^lept " + ", ".join("%.6f" % s2eff[("e", m)] for m in MUS[1:2] + MUS[:1] + MUS[2:]))
print("alpha scheme: s^2(M_Z) %.6f, sin^2 theta_eff^lept %.6f (mu = M_Z/2, 2 M_Z: %.6f, %.6f);  minus the note's: %+.2e"
      % (s2ms_a[MUS[0]], s2eff_a[("e", MUS[0])], s2eff_a[("e", MUS[1])], s2eff_a[("e", MUS[2])], s2eff_a[("e", MUS[0])] - s2eff[("e", MUS[0])]))
tree = obs(lambda f: s2ms[MUS[0]])
nlo = [obs(lambda f, m=m: s2eff[(f, m)]) for m in MUS]
nlo_a = obs(lambda f: s2eff_a[(f, MUS[0])])
out = []
print("%-11s %-10s %-10s %-10s %-18s %-14s  %s" % ("quantity", "tree", "NLO", "NLO alpha", "measured", "pulls", "NLO at mu = M_Z/2, 2 M_Z"))
for k, (m, e) in MEAS.items():
    print("%-11s %.6f   %.6f   %.6f   %.5f +- %.5f   %+5.2f %+5.2f    %.6f, %.6f" % (k, tree[k], nlo[0][k], nlo_a[k], m, e,
          (nlo[0][k] - m) / e, (nlo_a[k] - m) / e, nlo[1][k], nlo[2][k]))
    out.append([k, "%.8f" % tree[k], "%.8f" % nlo[0][k], "%.8f" % nlo[1][k], "%.8f" % nlo[2][k], "%.8f" % nlo_a[k], m, e,
                "%.3f" % ((nlo[0][k] - m) / e), "%.3f" % ((nlo_a[k] - m) / e)])
with open(HERE / "results" / "zpole.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "tree", "nlo", "nlo_mu_half", "nlo_mu_2", "nlo_alpha_scheme", "measured", "error", "pull", "pull_alpha_scheme"])
    w.writerows(out)
print("wrote results/zpole.csv")
