"""One-loop phi phi -> phi phi in d = 4: comparison and unitarity check (research note, step (5)).

The MS-bar truncated one-loop amplitude M1 (note, Eq. (17) (eq:M1); m = g = mu = 1) from
  FeynCalc + Package-X, FeynCalc + LoopTools   (results/scat4_feyncalc.csv),
  FormCalc + LoopTools                         (results/scat4_formcalc.csv),
  COLLIER                                      (results/scat4_collier.csv, scan: scat4_collier_scan.csv)
is compared point by point.  Reference values:
  Re M1: COLLIER (no tool-independent value is available for the box in the physical region);
  Im M1: the s-channel unitarity relation with two tree amplitudes (note, App. I, eq:unit = Eq. (18)),
      Im M1(s, t) = (1/4) (p / (16 pi^2 sqrt(s))) int dOmega_k M0(s, t1) M0(s, t2),
      M0(s, t') = -g^2 [1/(s - m^2) + 1/(t' - m^2) + 1/(u' - m^2)],  u' = 4 m^2 - s - t',
      t1 = (p1 - k)^2, t2 = (p3 - k)^2; the factor 1/4 = (1/2 from 2 Im M = sum |M|^2) x (1/2 identical
      particles).  In the forward direction it becomes the optical theorem Im M1(s, 0) = 2 p sqrt(s) sigma.
Writes results/scat4_comparison.csv and ../figs/scat4_d4.pdf.
Usage (from Src/):  ~/miniforge3/envs/qft/bin/python scat4_numeric.py
"""
import csv
import os

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 1e-10
M2 = 1


def tree(s, t):
    u = 4 * M2 - s - t
    return -(1 / (s - M2) + 1 / (t - M2) + 1 / (u - M2))


def im_unitarity(s, cth, dps=20):
    """(1/4) p/(16 pi^2 sqrt s) int dOmega_k M0(s,t1) M0(s,t2), p3 at angle theta to p1 in the x-z plane."""
    with mp.workdps(dps):
        s, cth = mp.mpf(s), mp.mpf(cth)
        p2 = s / 4 - M2
        sth = mp.sqrt(1 - cth ** 2)

        def f(a, phi):
            ca, sa = mp.cos(a), mp.sin(a)
            t1 = -2 * p2 * (1 - ca)
            t2 = -2 * p2 * (1 - (sth * sa * mp.cos(phi) + cth * ca))
            return sa * tree(s, t1) * tree(s, t2)

        integral = mp.quad(f, [0, mp.pi], [0, mp.pi, 2 * mp.pi])
        return mp.sqrt(p2) / (16 * mp.pi ** 2 * mp.sqrt(s)) * integral / 4


def sigma_tree(s, dps=20):
    """Eq. (19) (eq:sigma) of the note: sigma = (1/2) int dOmega |M0|^2/(64 pi^2 s)."""
    with mp.workdps(dps):
        s = mp.mpf(s)
        p2 = s / 4 - M2
        g = lambda c: tree(s, -2 * p2 * (1 - c)) ** 2
        return mp.mpf(1) / 2 * 2 * mp.pi * mp.quad(g, [-1, 1]) / (64 * mp.pi ** 2 * s)


def read(path, cols):
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6))
            out[key] = dict(s=float(r["s"]), t=float(r["t"]),
                            **{c: complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols})
    return out


fc = read(os.path.join(HERE, "results", "scat4_feyncalc.csv"), ["packagex", "looptools"])
fo = read(os.path.join(HERE, "results", "scat4_formcalc.csv"), ["formcalc"])
co = read(os.path.join(HERE, "results", "scat4_collier.csv"), ["collier"])
tools = ("packagex", "looptools", "formcalc", "collier")

# the unitarity code reproduces the optical theorem in the forward direction
for rs in (2.5, 5, 10):
    lhs, rhs = im_unitarity(rs ** 2, 1), 2 * mp.sqrt(rs ** 2 / 4 - M2) * rs * sigma_tree(rs ** 2)
    assert abs(lhs / rhs - 1) < 1e-15, (rs, lhs, rhs)
print("unitarity integral at cos(theta) = 1 equals 2 p sqrt(s) sigma_tree (optical theorem): ok")

rows = []
print(f"\n{'sqrt(s)':>7} {'cos':>4} {'Re M1 (COLLIER)':>22} {'Im M1 (unitarity)':>22} | "
      "rel. dev. Re: PX LT FormCalc | Im: PX LT FormCalc COLLIER")
for key in sorted(fc):
    rs, cth = key
    v = {**fc[key], **fo[key], **co[key]}   # s and t are the same in all three files
    re_ref = v["collier"].real
    im_ref = float(im_unitarity(v["s"], cth))
    dre = {k: abs(v[k].real - re_ref) / abs(re_ref) for k in tools}
    dim = {k: abs(v[k].imag - im_ref) / abs(im_ref) for k in tools}
    bad = [k for k in tools if dre[k] > TOL or dim[k] > TOL]
    print(f"{rs:7.1f} {cth:4.1f} {re_ref:+22.15e} {im_ref:+22.15e} | "
          f"{dre['packagex']:7.1e} {dre['looptools']:7.1e} {dre['formcalc']:7.1e} | "
          f"{dim['packagex']:7.1e} {dim['looptools']:7.1e} {dim['formcalc']:7.1e} {dim['collier']:7.1e}"
          + (("   <- disagrees: " + ",".join(bad)) if bad else ""))
    rows.append([rs, cth, v["s"], v["t"], re_ref, im_ref, tree(v["s"], v["t"]),
                 *(x for k in tools for x in (v[k].real, v[k].imag, dre[k], dim[k]))])

with open(os.path.join(HERE, "results", "scat4_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sqrts", "costheta", "s", "t", "re_ref_collier", "im_ref_unitarity", "tree",
                *(f"{c}_{k}" for k in tools for c in ("re", "im", "reldev_re", "reldev_im"))])
    w.writerows(rows)

# ---------------- figure: Re and Im of M1 at sqrt(s) = 5 versus cos(theta) ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

scan = read(os.path.join(HERE, "results", "scat4_collier_scan.csv"), ["collier"])
cs = np.array(sorted(k[1] for k in scan))
col = np.array([scan[(5.0, round(c, 6))]["collier"] for c in cs])
cu = np.linspace(0, 1, 26)
imu = np.array([float(im_unitarity(25, c, dps=15)) for c in cu])
sig = 2 * mp.sqrt(25 / 4 - M2) * 5 * sigma_tree(25)
pts = sorted(k for k in fc if k[0] == 5.0)

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 3.6), sharex=True)
ax1.plot(cs, 1e3 * col.real, color="k", lw=0.9, label="COLLIER")
ax2.plot(cs, 1e3 * col.imag, color="k", lw=0.9, label="COLLIER")
ax2.plot(cu, 1e3 * imu, color="#eb6235", lw=0.8, ls="--", label="unitarity")
ax2.plot([1], [1e3 * float(sig)], "*", ms=7, color="#eb6235", label=r"$2p\sqrt{s}\,\sigma_{\rm tree}$")
for ax, part in ((ax1, np.real), (ax2, np.imag)):
    ax.plot([k[1] for k in pts], [1e3 * part(fc[k]["packagex"]) for k in pts], "o", ms=4.5, mfc="none",
            mec="#5d81b4", label="Package-X")
    ax.plot([k[1] for k in pts], [1e3 * part(fc[k]["looptools"]) for k in pts], "x", ms=4, color="#e09b24",
            label="LoopTools")
    ax.plot([k[1] for k in pts], [1e3 * part(fo[k]["formcalc"]) for k in pts], "+", ms=6, color="#8eb031",
            label="FormCalc")
ax1.set_ylabel(r"$10^3\,\mathrm{Re}\,\mathcal{M}^{(1)}$")
ax2.set_ylabel(r"$10^3\,\mathrm{Im}\,\mathcal{M}^{(1)}$")
ax2.set_xlabel(r"$\cos\theta$")
ax1.legend(loc="upper left")
ax2.legend(loc="upper left", ncol=2)
ax1.set_title(r"$\sqrt{s}=5m$", fontsize=8)
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)
fig.savefig(os.path.join(figdir, "scat4_d4.pdf"))
print("\nwrote results/scat4_comparison.csv and figs/scat4_d4.pdf")
