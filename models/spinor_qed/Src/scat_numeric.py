# %% [markdown]
# # Step (4): one-loop e+ e- -> mu+ mu- -- FeynCalc, COLLIER and FormCalc against each other, the IR poles, unitarity
#
# Research note models/spinor_qed, step (4), Eqs. (15)-(17).  The quantity is K W/e^6 at e = 1 (K = (4 pi)^2,
# W = sum_spins M0^* M1), m_e = mu = 1, m_mu = 1.7, Feynman gauge, per class VP, Le, Lmu, box and their sum (the classes
# of scat_feyncalc.wl: VP with -delta3, the vertices with R_f - 1), split into the 1/eps coefficient and the MS-bar finite
# part, at the nine physical points of scat_feyncalc.wl (f).
#
# 1. CDR: FeynCalc + LoopTools (the FeynArts diagrams, results/scat_mathematica.csv) against the note's formulas with
#    COLLIER (scat_collier.f90, results/scat_collier.csv).
# 2. FormCalc + LoopTools (scat_formcalc.wl, results/scat_formcalc.csv; four-dimensional spin sums): the UV pole of each
#    class vanishes, the IR pole equals the CDR one, and the finite parts obey Eq. (17),
#    K W(FormCalc) = K W(CDR) + 8 e^4 (IR pole of K W)/B(4).
# 3. The IR poles against the eikonal formula, Eq. (16), with mpmath (independent of the three tools):
#    Le: 2 B(4) f_IR(s; m),  Lmu: 2 B(4) f_IR(s; M),  box: 2 B(4) [G(t) - G(u)].
# 4. Unitarity: the imaginary part of the boxes is the gamma gamma cut,
#    Im W_box = sum_spins M0^* (1/2) (1/2) (1/(32 pi^2)) int dOmega sum_pol M(e+e- -> gg) M(mu+mu- -> gg)^*
#    (the first 1/2 from 2 Abs T = T^dagger T, the second for the identical photons), with explicit spinors and
#    polarization vectors and Gauss-Legendre quadrature over the photon direction.
# Writes results/scat_comparison.csv.
# Batch: `~/miniforge3/envs/qft/bin/python scat_numeric.py` (from Src/).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import itertools
import math
import os
import sys

import mpmath as mp
import numpy as np

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
ME, MMU = 1.0, 1.7
CLASSES = ("VP", "Le", "Lmu", "box", "total")


def born4(s, t):
    u = 2 * ME ** 2 + 2 * MMU ** 2 - s - t
    sig = ME ** 2 + MMU ** 2
    return 8 / s ** 2 * ((t - sig) ** 2 + (u - sig) ** 2 + 2 * s * sig)


def read(name):
    """{(class, s, t): row with complex 'pole' (or 'uv', 'ir') and 'fin'}"""
    out = {}
    with open(os.path.join(HERE, "results", name)) as fh:
        for r in csv.DictReader(fh):
            z = lambda k: complex(float(r["re_" + k]), float(r["im_" + k]))
            row = {"rs": float(r["rs"]), "cos": float(r["cos"]), "fin": z("fin")}
            if "re_pole" in r:
                row["pole"] = z("pole")
            else:
                row["uv"], row["ir"] = z("uv"), z("ir")
                row["pole"] = row["uv"] + row["ir"]
            out[(r["class"].strip(), round(float(r["s"]), 8), round(float(r["t"]), 8))] = row
    return out


fc_cdr = read("scat_mathematica.csv")
col = read("scat_collier.csv")
form = read("scat_formcalc.csv")
POINTS = sorted({(k[1], k[2]) for k in fc_cdr}, key=lambda p: (p[0], p[1]))
POINTS

# %% [markdown]
# ## 1, 2: the three tools
#
# Relative deviations |x - y|/max(|y|, 1) of the poles and of the finite parts; for FormCalc the CDR value is first
# shifted by Eq. (17).

# %%
def rdev(x, y):
    return abs(x - y) / max(abs(y), 1.0)


worst = {}
rows = []
for s, t in POINTS:
    b4 = born4(s, t)
    for c in CLASSES:
        a, b, f = fc_cdr[(c, s, t)], col[(c, s, t)], form[(c, s, t)]
        shift = 8 * a["pole"] / b4
        d = {"collier_pole": rdev(b["pole"], a["pole"]), "collier_fin": rdev(b["fin"], a["fin"]),
             "formcalc_uv": abs(f["uv"]), "formcalc_ir": rdev(f["ir"], a["pole"]),
             "formcalc_fin_eq17": rdev(f["fin"], a["fin"] + shift), "formcalc_fin_raw": rdev(f["fin"], a["fin"])}
        for k, v in d.items():
            worst[k] = max(worst.get(k, 0.0), v)
        rows.append({"class": c, "rs": a["rs"], "cos": a["cos"], "s": s, "t": t, "B4": b4, "pole": a["pole"], "fin": a["fin"],
                     "fin_formcalc": f["fin"], "eq17_shift": shift, **d})
for s, t in POINTS:
    tot = fc_cdr[("total", s, t)]
    print(f"sqrt(s) = {math.sqrt(s):4.1f}, t = {t:6.1f}:  K W pole {tot['pole'].real:+.10f} {tot['pole'].imag:+.10f}i, "
          f"finite {tot['fin'].real:+.10f} {tot['fin'].imag:+.10f}i  (CDR, MS-bar, mu = 1)")
print("max deviation over the classes and points:")
for k, v in worst.items():
    print(f"  {k:18s} {v:.1e}")
print("(formcalc_fin_raw: FormCalc against CDR without Eq. (17), i.e. the size of the scheme difference)")

# %% [markdown]
# ## 3: the IR poles against Eq. (16)

# %%
def f_ir(s, m):
    """above threshold: ((s - 2m^2)/(s beta)) [ln((1+beta)/(1-beta)) - i pi] - 1"""
    s, m = mp.mpf(s), mp.mpf(m)
    b = mp.sqrt(1 - 4 * m * m / s)
    return (s - 2 * m * m) / (s * b) * (mp.log((1 + b) / (1 - b)) - 1j * mp.pi) - 1


def g_ir(x):
    m2, mm2, x = mp.mpf(ME) ** 2, mp.mpf(MMU) ** 2, mp.mpf(x)
    return (m2 + mm2 - x) * mp.quad(lambda w: 1 / (w * m2 + (1 - w) * mm2 - x * w * (1 - w)), [0, 1])


ir_worst = {}
for s, t in POINTS:
    u = 2 * ME ** 2 + 2 * MMU ** 2 - s - t
    b4 = mp.mpf(born4(s, t))
    pred = {"Le": 2 * b4 * f_ir(s, ME), "Lmu": 2 * b4 * f_ir(s, MMU), "box": 2 * b4 * (g_ir(t) - g_ir(u)), "VP": mp.mpf(0)}
    pred["total"] = sum(pred.values())
    for c in CLASSES:
        v = complex(pred[c])
        ir_worst[c] = max(ir_worst.get(c, 0.0), rdev(fc_cdr[(c, s, t)]["pole"], v))
        next(r for r in rows if r["class"] == c and r["s"] == s and r["t"] == t)["eq16_dev"] = rdev(fc_cdr[(c, s, t)]["pole"], v)
print("IR pole (CDR) against Eq. (16), max relative deviation per class:",
      ", ".join(f"{c} {v:.1e}" for c, v in ir_worst.items()))

# %% [markdown]
# ## 4: unitarity of the boxes (the gamma gamma cut)
#
# Dirac representation and spinors as in tree_sigma.py.  M0 = (e^2/s) [vbar(p2) g^mu u(p1)] [ubar(k1) g_mu v(k2)];
# M(f fbar -> g(q1, e1) g(q2, e2)) = -e^2 vbar [e2slash (p - q1slash + m) e1slash/(t1 - m^2) + (1 <-> 2)] u.
# The spin sum factorizes: sum_spins M0^* A_ee A_mumu^* = (e^2/s) sum_pol X(pol).Y(pol), with
# X^mu = sum_{e spins} J_e^mu* A_ee and Y^mu = sum_{mu spins} J_mu^mu* A_mumu^*.

# %%
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
G0 = np.block([[I2, Z2], [Z2, -I2]])
GAM = [G0] + [np.block([[Z2, sg], [-sg, Z2]]) for sg in SIG]
METRIC = np.array([1.0, -1.0, -1.0, -1.0])
ONE = np.eye(4, dtype=complex)
CHI = [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]


def slash(p):
    return sum(METRIC[n] * p[n] * GAM[n] for n in range(4))


def mdot(p, q):
    return float(p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3])


def u_spinor(p, mass, chi):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + mass)
    return np.concatenate([n * chi, sp @ chi / n])


def v_spinor(p, mass, eta):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + mass)
    return np.concatenate([sp @ eta / n, n * eta])


def bar(w):
    return w.conj() @ G0


def current(wl, wr):
    return np.array([wl @ GAM[n] @ wr for n in range(4)])


def pol_vectors(n):
    """two real polarization vectors transverse to the unit vector n"""
    th, ph = math.acos(max(-1.0, min(1.0, n[2]))), math.atan2(n[1], n[0])
    return (np.array([0.0, math.cos(th) * math.cos(ph), math.cos(th) * math.sin(ph), -math.sin(th)]),
            np.array([0.0, -math.sin(ph), math.cos(ph), 0.0]))


def kinematics(s, t):
    e = math.sqrt(s) / 2
    p, k = math.sqrt(e * e - ME ** 2), math.sqrt(e * e - MMU ** 2)
    cth = (t - ME ** 2 - MMU ** 2 + 2 * e * e) / (2 * p * k)
    sth = math.sqrt(1 - cth * cth)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    k1 = np.array([e, k * sth, 0, k * cth])
    k2 = np.array([e, -k * sth, 0, -k * cth])
    return p1, p2, k1, k2


def pair_to_gg(pa, pb, mass, q1, q2, e1, e2):
    """the 2x2 (spin of the fermion, spin of the antifermion) matrix of M(f(pa) fbar(pb) -> g(q1, e1) g(q2, e2)), e = 1"""
    t1, u1 = mdot(pa - q1, pa - q1), mdot(pa - q2, pa - q2)
    gam = (slash(e2) @ (slash(pa - q1) + mass * ONE) @ slash(e1) / (t1 - mass ** 2)
           + slash(e1) @ (slash(pa - q2) + mass * ONE) @ slash(e2) / (u1 - mass ** 2))
    return np.array([[-(bar(v_spinor(pb, mass, b)) @ gam @ u_spinor(pa, mass, a)) for b in CHI] for a in CHI])


def im_box_unitarity(s, t, nodes=48):
    p1, p2, k1, k2 = kinematics(s, t)
    je = np.array([[current(bar(v_spinor(p2, ME, b)), u_spinor(p1, ME, a)) for b in CHI] for a in CHI])    # [a, b, mu]
    jm = np.array([[current(bar(u_spinor(k1, MMU, c)), v_spinor(k2, MMU, d)) for d in CHI] for c in CHI])  # [c, d, mu]
    xs, ws = np.polynomial.legendre.leggauss(nodes)
    total = 0.0
    for x, wx in zip(xs, ws):                         # cos of the photon polar angle
        sx = math.sqrt(1 - x * x)
        for y, wy in zip(xs, ws):                     # azimuth phi = pi (y + 1)
            ph = math.pi * (y + 1)
            n = np.array([sx * math.cos(ph), sx * math.sin(ph), x])
            q1 = math.sqrt(s) / 2 * np.concatenate([[1.0], n])
            q2 = math.sqrt(s) / 2 * np.concatenate([[1.0], -n])
            pols1, pols2 = pol_vectors(n), pol_vectors(-n)
            acc = 0.0
            for e1, e2 in itertools.product(pols1, pols2):
                aee = pair_to_gg(p1, p2, ME, q1, q2, e1, e2)          # [a, b]
                amm = pair_to_gg(k1, k2, MMU, q1, q2, e1, e2)         # [c, d]
                xv = np.einsum("abm,ab->m", je.conj(), aee)
                yv = np.einsum("cdm,cd->m", jm.conj(), amm.conj())
                acc += np.sum(METRIC * xv * yv)
            total += wx * wy * math.pi * acc          # dOmega = dx dphi, dphi = pi dy
    return (1 / s) * 0.25 / (32 * math.pi ** 2) * total


KK = (4 * math.pi) ** 2
uni = []
for s, t in POINTS:
    # the integrand peaks where a photon is collinear with a fermion (width ~ m/E): more nodes at sqrt(s) = 10
    n1, n2 = (48, 64) if s < 50 else (96, 128)
    va, vb = KK * im_box_unitarity(s, t, n1), KK * im_box_unitarity(s, t, n2)
    ref = fc_cdr[("box", s, t)]["fin"].imag
    uni.append((s, t, ref, vb, abs(vb - va)))
    next(r for r in rows if r["class"] == "box" and r["s"] == s and r["t"] == t)["unitarity_im"] = vb
    print(f"sqrt(s) = {math.sqrt(s):4.1f}, t = {t:6.1f}:  K Im W_box: loop {ref:+.12f}, gamma gamma cut {vb.real:+.12f} "
          f"(imag. part of the cut {abs(vb.imag):.0e}, quadrature {n1} vs {n2} nodes {abs(vb - va):.0e}), rel. dev. {abs(vb - ref) / abs(ref):.1e}")

# %%
with open(os.path.join(HERE, "results", "scat_comparison.csv"), "w", newline="") as fh:
    keys = ["class", "rs", "cos", "s", "t", "B4", "pole", "fin", "fin_formcalc", "eq17_shift", "collier_pole", "collier_fin",
            "formcalc_uv", "formcalc_ir", "formcalc_fin_eq17", "formcalc_fin_raw", "eq16_dev", "unitarity_im"]
    w = csv.writer(fh)
    head = []
    for k in keys:
        head += [f"re_{k}", f"im_{k}"] if k in ("pole", "fin", "fin_formcalc", "eq17_shift") else [k]
    w.writerow(head)
    for r in rows:
        line = []
        for k in keys:
            v = r.get(k, "")
            if k in ("pole", "fin", "fin_formcalc", "eq17_shift"):
                line += [f"{v.real:.16e}", f"{v.imag:.16e}"]
            elif isinstance(v, complex):
                line.append(f"{v.real:.16e}")
            elif isinstance(v, float):
                line.append(f"{v:.16e}")
            else:
                line.append(v)
        w.writerow(line)
print("wrote results/scat_comparison.csv")
