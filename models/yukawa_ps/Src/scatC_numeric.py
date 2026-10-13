# %% [markdown]
# # Step (12): one-loop psi psibar -> psi psibar and the completed one-loop partial-wave bound (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (12), Eq. (MC1), App. scatC.  psi(p1) psibar(p2) -> psi(p3) psibar(p4), m = 1, M = 0.7
# (pole masses), y (MS-bar).  Tree: M0 = y^2 [S/(s - m^2) - T/(t - m^2)], S = (vbar2 g5 u1)(ubar3 g5 v4), T = (ubar3 g5 u1)(vbar2 g5 v4).
# One-loop S-matrix element (pole masses, LSZ residues, MS-bar coupling), the hand formula of the note:
#   M1 = y^2 sum_{x = s, t} sigma_x X_x/(x - m^2) [2 dR_psi - 2 y^2 G(x)/(4pi)^2 + Sigma^(x)/(x - m^2)] + boxes,
#   (sigma_s, X_s) = (+1, S), (sigma_t, X_t) = (-1, T);  G(x) = B0(M^2; M^2, m^2) + 2 M^2 [C0 + C2](x) + x C1(x),
#   C_i(x) = C_i(x, M^2, M^2; M^2, M^2, m^2) (the pseudoscalar form factor of the vertex V_y of Eq. (VR) between on-shell spinors),
#   Sigma^(x) = -(2 y^2/(4pi)^2) [x B0(x; M^2, M^2) - m^2 B0(m^2; M^2, M^2)] (phi self-energy minus its value at the pole),
#   (4pi)^2 dR_psi = y^2 [B1 + 2 M^2 (B0' + B1')](M^2; M^2, m^2)  (four external fermions: R_psi^2 = 1 + 2 dR_psi);
#   boxes (rank-2 tensor integrals, two phi and two psi propagators; the Dirac equation removes everything but l l):
#   (4pi)^2 M_box = - [ubar3 g_mu u1][vbar2 g_nu v4] (D_td - D_tx)^{mu nu} + [vbar2 g_mu u1][ubar3 g_nu v4] (D_sd - D_sx)^{mu nu},
#   D^{mu nu} = int l^mu l^nu/(D_phi(l) D_psi(l + k1) D_phi(l + k2) D_psi(l + k3)) with offsets (k1, k2, k3) = td: (-p1, p3-p1, p2),
#   tx: (-p1, p3-p1, -p4), sd: (-p1, -p1-p2, -p3), sx: (-p1, -p1-p2, -p4)  (COLLIER, work/scatC_collier).
# Checks: (1) the tree spin sum against Eq. (11); (2) the vertex from its integrand (explicit Dirac matrices and rank-2 C tensors,
# plus the rational term (D - 4) x the UV pole of C00) against G(x); (3) the mu-dependence d M1/d ln mu = -10 y^2 M0/(4pi)^2;
# (4) the FeynCalc projections of each class on four spinor structures (results/scatC_feyncalc.csv); (5) MadLoop (work/ml_<OS|
# MSbar>_C) at several points and mu_R; (6) partial-wave unitarity Abs a^(1) = a^(0) a^(0)+ for J = 0 (with the phi phi state)
# and J = 1 (four psi psibar helicity states).
# Then the full J = 0 one-loop matrix (phi phi, psi psibar(++), psi psibar(--); the elements with phi phi as in step (8),
# pw_numeric.py) and the bound (C): the eigenvalues of Re a^0 = Re(a^(0) + a^(1)) satisfy |.| <= 1/2 for 2M < sqrt(s) <= 4m, mu = m
# (band mu = m/2, 2m with the one-loop running), against step (8)'s elementwise criterion and the tree in the same range.
# Writes results/scatC.csv and ../figs/scatC_d4.pdf.  Usage (from Src/): ~/miniforge3/envs/qft/bin/python scatC_numeric.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import csv
import math
import os
import re
import subprocess
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
MPHI, MPSI = 1.0, 0.7
M2, BM2 = MPHI ** 2, MPSI ** 2
K = (4 * math.pi) ** 2
mp.mp.dps = 30
H = (0.5, -0.5)
HEL = [(a, b, c, d) for a in H for b in H for c in H for d in H]
NQ = 48

# %% [markdown]
# ## Dirac matrices and helicity spinors (chiral basis, as in pw_numeric.py)

# %%
I2, Z2 = np.eye(2), np.zeros((2, 2))
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]])
SZ = np.array([[1, 0], [0, -1]], complex)
G0 = np.block([[Z2, I2], [I2, Z2]]).astype(complex)
GI = [np.block([[Z2, s], [-s, Z2]]) for s in (SX, SY, SZ)]
G5 = np.block([[-I2, Z2], [Z2, I2]]).astype(complex)
GLOW = [G0, -GI[0], -GI[1], -GI[2]]                 # gamma_mu
GINV = np.diag([1.0, -1.0, -1.0, -1.0])             # g^{mu nu}
SIGMA_Y = np.block([[SY, Z2], [Z2, SY]])
ONE = np.eye(4)
UP, DN = np.array([1, 0], complex), np.array([0, 1], complex)


def slash(p):
    return sum(p[i] * GLOW[i] for i in range(4))


def mdot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def bar(w):
    return w.conj() @ G0


def sqrt_psigma(e, pz, sign):
    return np.diag([math.sqrt(e - sign * pz), math.sqrt(e + sign * pz)]).astype(complex)


def u_z(e, pz, lam):
    xi = UP if (lam > 0) == (pz >= 0) else DN
    return np.concatenate([sqrt_psigma(e, pz, 1) @ xi, sqrt_psigma(e, pz, -1) @ xi])


def v_z(e, pz, lam):
    eta = DN if (lam > 0) == (pz >= 0) else UP
    return np.concatenate([sqrt_psigma(e, pz, 1) @ eta, -sqrt_psigma(e, pz, -1) @ eta])


def rot(theta):
    """exp(-i theta Sigma_y/2) = cos(theta/2) - i sin(theta/2) Sigma_y (Sigma_y^2 = 1; = scipy.linalg.expm, checked below)"""
    return math.cos(theta / 2) * ONE - 1j * math.sin(theta / 2) * SIGMA_Y


def rot4(v, theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([v[0], c * v[1] + s * v[3], v[2], -s * v[1] + c * v[3]])


def energies(rs, ma, mb):
    ea = (rs * rs + ma * ma - mb * mb) / (2 * rs)
    return ea, rs - ea, math.sqrt(max(ea * ea - ma * ma, 0.0))


def state(kind, hel, rs, theta):
    R = rot(theta)
    if kind == "phiphi":
        e, _, k = energies(rs, MPHI, MPHI)
        return {"k": [rot4(np.array([e, 0, 0, k]), theta), rot4(np.array([e, 0, 0, -k]), theta)]}
    e, _, p = energies(rs, MPSI, MPSI)
    return {"p": rot4(np.array([e, 0, 0, p]), theta), "pb": rot4(np.array([e, 0, 0, -p]), theta),
            "u": R @ u_z(e, p, hel[0]), "v": R @ v_z(e, -p, hel[1])}

assert np.abs(rot(0.83) - expm(-0.5j * 0.83 * SIGMA_Y)).max() < 1e-15

# %% [markdown]
# ## Inspect: the diagrams MadLoop evaluates (2 Born, 12 loops), drawn when MadGraph wrote the standalone code

# %%
if INTERACTIVE:
    import shutil
    import tempfile
    from IPython.display import Image, display
    GS = shutil.which("gs") or "/opt/homebrew/bin/gs"
    base = os.path.join(HERE, "work", "ml_OS_C", "SubProcesses")
    dML = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    tmpML = tempfile.mkdtemp()
    for ps in ("born_matrix.ps", "loop_matrix.ps"):
        subprocess.run([GS, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                        "-sOutputFile=" + os.path.join(tmpML, ps[:-3] + "_%02d.png"), os.path.join(dML, ps)], check=True)
        for png in sorted(f for f in os.listdir(tmpML) if f.startswith(ps[:-3] + "_")):
            display(Image(filename=os.path.join(tmpML, png)))

# %% [markdown]
# ## Loop integrals (COLLIER) and two-point functions at the special points

# %%
def collier(points):
    """run work/scatC_collier on (sqrts, cos, mu) points; returns a list of dicts of complex loop functions"""
    with open(os.path.join(HERE, "work", "scatC_nodes.txt"), "w") as fh:
        for rs, c, mu in points:
            fh.write("%.17e %.17e %.17e\n" % (rs, c, mu))
    subprocess.run([os.path.join(HERE, "work", "scatC_collier"), "scatC_nodes.txt", "scatC_amp.csv"], cwd=os.path.join(HERE, "work"),
                   check=True, capture_output=True)
    out = []
    with open(os.path.join(HERE, "work", "scatC_amp.csv")) as fh:
        for r in csv.DictReader(fh):
            d = {k[3:]: complex(float(r[k]), float(r["im_" + k[3:]])) for k in r if k.startswith("re_")}
            d.update({k: float(r[k]) for k in ("sqrts", "costheta", "mu", "s", "t", "u")})
            out.append(d)
    return out


def dx(x, p2, ma2, mb2):
    return x * mb2 + (1 - x) * ma2 - x * (1 - x) * p2


SP = {"B0phi": float(-mp.quad(lambda x: mp.log(dx(x, 1.0, 0.49, 0.49)), [0, 1])),
      "B0pphi": float(mp.quad(lambda x: x * (1 - x) / dx(x, 1.0, 0.49, 0.49), [0, 1])),
      "B0psi": float(-mp.quad(lambda x: mp.log(dx(x, 0.49, 0.49, 1.0)), [0, 1])),
      "B1psi": float(mp.quad(lambda x: x * mp.log(dx(x, 0.49, 0.49, 1.0)), [0, 1])),
      "B0ppsi": float(mp.quad(lambda x: x * (1 - x) / dx(x, 0.49, 0.49, 1.0), [0, 1])),
      "B1ppsi": float(-mp.quad(lambda x: x * x * (1 - x) / dx(x, 0.49, 0.49, 1.0), [0, 1]))}


def dR_psi(mu):
    """(4 pi)^2 (R_psi - 1)/y^2 = B1 + 2 M^2 (B0' + B1') at p^2 = M^2 (Eq. (Mpole)); B1 carries -ln(mu)"""
    return SP["B1psi"] - math.log(mu) + 2 * BM2 * (SP["B0ppsi"] + SP["B1ppsi"])


def a0(m2_, mu):
    return m2_ * (1 - math.log(m2_ / mu ** 2))

# %% [markdown]
# ## The amplitude classes (coupling factors removed: tree / y^2, loops / y^4, the quartic tadpole / (lambda y^2))

# %%
def tensor2(L, pre, ks, names):
    T = L[pre + "_" + names[0]] * GINV
    for i in range(len(ks)):
        for j in range(len(ks)):
            T = T + L[pre + "_" + names[1][(min(i, j), max(i, j))]] * np.outer(ks[i], ks[j])
    return T


DN_ = ("d00", {(0, 0): "d11", (0, 1): "d12", (0, 2): "d13", (1, 1): "d22", (1, 2): "d23", (2, 2): "d33"})
CN_ = ("c00", {(0, 0): "c11", (0, 1): "c12", (1, 1): "c22"})


def lowvec(xb, y_):
    return np.array([xb @ GLOW[m] @ y_ for m in range(4)])


def vertex_explicit(xb, y_, p, pp, L, pre):
    """(4pi)^2/y^3 x the one-loop vertex between spinors: int xb g5 (pp - l + M) g5 (p - l + M) g5 y_ / (D_phi(l) D_psi(l - p)
    D_psi(l - pp)) from the rank-2 C tensors (offsets -p, -pp) with 4-dimensional Dirac matrices, plus the rational term
    -(D - 4) x (UV pole of C00 = 1/(4 eps)) x (g_mu g^mu -> D) = +1/2 xb g5 y_"""
    k1, k2 = -p, -pp
    T1 = L[pre + "_c1"] * k1 + L[pre + "_c2"] * k2
    T2 = tensor2(L, pre, (k1, k2), CN_)
    Pp, P = slash(pp) + MPSI * ONE, slash(p) + MPSI * ONE
    val = L[pre + "_c0"] * (xb @ G5 @ Pp @ G5 @ P @ G5 @ y_)
    for m in range(4):
        val -= T1[m] * (xb @ (G5 @ GLOW[m] @ G5 @ P @ G5 + G5 @ Pp @ G5 @ GLOW[m] @ G5) @ y_)
        for n in range(4):
            val += T2[m, n] * (xb @ G5 @ GLOW[m] @ G5 @ GLOW[n] @ G5 @ y_)
    return val + 0.5 * (xb @ G5 @ y_)


def G_ff(L, x, pre):
    """pseudoscalar form factor of V_y between on-shell spinors: (4pi)^2 Gamma^(1) = -y^3 G(x) g5"""
    return L["b0v"] + 2 * BM2 * (L[pre + "_c0"] + L[pre + "_c2"]) + x * L[pre + "_c1"]


def sigma_ms(L, x, b0x, mu):
    """(4pi)^2 Sigma_phi(x) (MS-bar, Eq. (VR)): y^2 part and lambda part"""
    return -2 * (x * b0x - 2 * a0(BM2, mu)), -0.5 * a0(M2, mu)


def classes(L, h, explicit=False):
    """amplitude classes for initial (h1 h2) along z, final (h3 h4) at theta, couplings removed"""
    rs, c, mu, s, t = L["sqrts"], L["costheta"], L["mu"], L["s"], L["t"]
    i, f = state("psipsibar", h[:2], rs, 0.0), state("psipsibar", h[2:], rs, math.acos(c))
    p1, p2, p3, p4 = i["p"], i["pb"], f["p"], f["pb"]
    u1, v2, u3, v4 = i["u"], i["v"], f["u"], f["v"]
    bu3, bv2 = bar(u3), bar(v2)
    a_s1, a_s2, a_t1, a_t2 = bv2 @ G5 @ u1, bu3 @ G5 @ v4, bu3 @ G5 @ u1, bv2 @ G5 @ v4
    S, T = a_s1 * a_s2, a_t1 * a_t2
    out = {"S": S, "T": T, "tree": S / (s - M2) - T / (t - M2)}
    Gs, Gt = G_ff(L, s, "ns"), G_ff(L, t, "nt")
    out["vertex"] = -2 * (Gs * S / (s - M2) - Gt * T / (t - M2)) / K
    if explicit:
        out["vertex_explicit"] = ((vertex_explicit(bv2, u1, p1, -p2, L, "vs") * a_s2 + a_s1 * vertex_explicit(bu3, v4, -p4, p3, L, "vs"))
                                  / (s - M2) - (vertex_explicit(bu3, u1, p1, p3, L, "vt") * a_t2
                                                + a_t1 * vertex_explicit(bv2, v4, -p4, -p2, L, "vt")) / (t - M2)) / K
    sh = lambda x, b0x: -2 * (x * b0x - M2 * L["b0m"])
    out["se"] = (S * sh(s, L["b0s"]) / (s - M2) ** 2 - T * sh(t, L["b0t"]) / (t - M2) ** 2) / K
    sms, tms = sigma_ms(L, s, L["b0s"], mu), sigma_ms(L, t, L["b0t"], mu)
    out["se_ms_y"] = (S * sms[0] / (s - M2) ** 2 - T * tms[0] / (t - M2) ** 2) / K
    out["se_ms_l"] = (S * sms[1] / (s - M2) ** 2 - T * tms[1] / (t - M2) ** 2) / K
    out["res"] = 2 * dR_psi(mu) * out["tree"] / K
    P = p1 + p2
    At, Bt, As, Bs = lowvec(bu3, u1), lowvec(bv2, v4), lowvec(bv2, u1), lowvec(bu3, v4)
    con = lambda A, B, T2: np.einsum("m,n,mn->", A, B, T2)
    out["boxT"] = (-con(At, Bt, tensor2(L, "td", (-p1, p3 - p1, p2), DN_)) + con(At, Bt, tensor2(L, "tx", (-p1, p3 - p1, -p4), DN_))) / K
    out["boxS"] = (con(As, Bs, tensor2(L, "sd", (-p1, -P, -p3), DN_)) - con(As, Bs, tensor2(L, "sx", (-p1, -P, -p4), DN_))) / K
    out["os"] = out["res"] + out["vertex"] + out["se"] + out["boxT"] + out["boxS"]           # M1_phys / y^4
    out["struct"] = {"S55": S, "T55": T, "S11": (bv2 @ u1) * (bu3 @ v4), "T11": (bu3 @ u1) * (bv2 @ v4)}
    return out

# %% [markdown]
# ## Checks (1)-(3): tree spin sum, the vertex from its integrand, the mu-dependence

# %%
PTS = [(5.0, 0.3), (2.5, -0.6), (10.0, 0.9), (1.6, 0.0), (3.0, 0.99)]
LC = {(round(L["sqrts"], 9), round(L["costheta"], 9), round(L["mu"], 9)): L for L in collier([(rs, c, mu) for rs, c in PTS for mu in (0.5, 1.0, 2.0)])}
dev1 = dev2 = dev3 = 0.0
for rs, c in PTS:
    L1 = LC[(rs, c, 1.0)]
    s, t = L1["s"], L1["t"]
    cl = {h: classes(L1, h, explicit=True) for h in HEL}
    ssum = sum(abs(cl[h]["tree"]) ** 2 for h in HEL)
    ref = 4 * (s * s / (s - M2) ** 2 + t * t / (t - M2) ** 2 + s * t / ((s - M2) * (t - M2)))
    dev1 = max(dev1, abs(ssum / ref - 1))
    dev2 = max(dev2, max(abs(cl[h]["vertex_explicit"] - cl[h]["vertex"]) for h in HEL) / max(abs(cl[h]["vertex"]) for h in HEL))
    for mu in (0.5, 2.0):
        Lm = LC[(rs, c, mu)]
        for h in HEL:
            a, b = classes(Lm, h)["os"], cl[h]["os"]
            pred = -10 * math.log(mu) * cl[h]["tree"] / K
            dev3 = max(dev3, abs((a - b) - pred) / max(abs(cl[h]["os"]), 1e-30))
print(f"check 1: tree spin sum against Eq. (11) at {len(PTS)} points: max rel. dev. {dev1:.1e}")
print(f"check 2: vertex from its integrand (rank-2 C tensors + rational term) against the form factor G(x): max rel. dev. {dev2:.1e}")
print(f"check 3: M1(mu) - M1(m) = -10 ln(mu) M0/(4pi)^2 (fixed couplings, mu = m/2, 2m): max dev. {dev3:.1e} (relative to |M1|)")
# the size of the classes at sqrt(s) = 5, cos = 0.3, (++ -> ++)
c0_ = classes(LC[(5.0, 0.3, 1.0)], (0.5, 0.5, 0.5, 0.5))
{k: complex(np.round(v, 6)) for k, v in c0_.items() if k in ("tree", "res", "vertex", "se", "boxT", "boxS", "os")}   # inspect

# %% [markdown]
# ## Check (4): FeynCalc projections; check (5): MadLoop

# %%
fcpath = os.path.join(HERE, "results", "scatC_feyncalc.csv")
dev4 = None
if os.path.exists(fcpath):
    with open(fcpath) as fh:
        fc_rows = list(csv.DictReader(fh))
    vals = []
    for r in fc_rows:
        rs, c = float(r["sqrts"]), float(r["costheta"])
        L1 = LC[(round(rs, 9), round(c, 9), 1.0)]
        cl = {h: classes(L1, h) for h in HEL}
        key = {"se": "se_ms", "vertex": "vertex", "boxT": "boxT", "boxS": "boxS", "tree": "tree"}[r["class"]]
        if key == "se_ms":
            val = sum((cl[h]["se_ms_y"] + cl[h]["se_ms_l"]) * np.conj(cl[h]["struct"][r["structure"]]) for h in HEL)
        else:
            val = sum(cl[h][key] * np.conj(cl[h]["struct"][r["structure"]]) for h in HEL)
        fac = 1.0 if key == "tree" else K                         # FeynCalc rows: (4pi)^2 x projection (loops), projection (tree)
        vals.append((r, fac * val, complex(float(r["re"]), float(r["im"]))))
    # FeynArts fixes the overall sign of a four-fermion amplitude by its own convention: take it from the tree rows
    signs = [(got / mine).real for r, mine, got in vals if r["class"] == "tree"]
    sgn = round(signs[0])
    assert all(abs(x - sgn) < 1e-12 for x in signs), signs
    dev4 = 0.0
    for r, mine, got in vals:
        scale = max(abs(g) for rr, _, g in vals if (rr["sqrts"], rr["costheta"], rr["class"]) == (r["sqrts"], r["costheta"], r["class"]))
        d = abs(sgn * mine - got) / scale
        dev4 = max(dev4, d)
        if d > 1e-9:
            print("  FeynCalc mismatch:", r["sqrts"], r["costheta"], r["class"], r["structure"], sgn * mine, got)
    print(f"check 4: projections of the classes (se, vertex, boxT, boxS) on S55, T55, S11, T11 against FeynCalc + LoopTools (2 points):"
          f" max dev. {dev4:.1e} (relative to the largest projection of the class; overall sign of the FeynArts amplitude {sgn:+d})")
else:
    print("check 4: results/scatC_feyncalc.csv not found (run scatC_feyncalc.wl)")


def run_madloop(scheme, rs, ct, mu):
    base = os.path.join(HERE, "work", f"ml_{scheme}_C", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    e = rs / 2
    p = math.sqrt(e * e - BM2)
    st = math.sqrt(1 - ct * ct)
    mom = [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * ct), (e, -p * st, 0, -p * ct)]
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in mom)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps", "2eps")}


ml_rows, dev5 = [], {}
ml_runs = [(rs, c, 1.0) for rs, c in PTS] + [(5.0, 0.3, 0.5), (5.0, 0.3, 2.0)]
if os.path.isdir(os.path.join(HERE, "work", "ml_OS_C")):
    for scheme in ("OS", "MSbar"):
        for rs, c, mu in ml_runs:
            L1 = LC[(round(rs, 9), round(c, 9), round(mu, 9))]
            cl = {h: classes(L1, h) for h in HEL}
            born = 0.25 * sum(abs(cl[h]["tree"]) ** 2 for h in HEL)
            if scheme == "OS":
                m1 = {h: cl[h]["os"] for h in HEL}
            else:                                                 # MS-bar masses = the same numbers, no residues
                m1 = {h: cl[h]["vertex"] + cl[h]["se_ms_y"] + cl[h]["se_ms_l"] + cl[h]["boxT"] + cl[h]["boxS"] for h in HEL}
            fin = 0.25 * sum(2 * (np.conj(cl[h]["tree"]) * m1[h]).real for h in HEL)
            v = run_madloop(scheme, rs, c, mu)
            d = abs(v["finite"] / fin - 1)
            dev5[scheme] = max(dev5.get(scheme, 0.0), d, abs(v["born"] / born - 1))
            ml_rows.append([scheme, rs, c, mu, v["born"], born, v["finite"], fin, v["1eps"], d])
            print(f"  MadLoop {scheme:5} sqrt(s) = {rs:4.1f} cos = {c:5.2f} mu = {mu:3.1f}: born {v['born']:.12e} ({born:.12e}),"
                  f" finite {v['finite']:+.12e} ({fin:+.12e}), rel. dev. {d:.1e}, 1/eps {v['1eps']:+.1e}")
    print("check 5: MadLoop against the hand formula, max rel. dev. (born and finite):", {k: f"{x:.1e}" for k, x in dev5.items()})
else:
    print("check 5: work/ml_OS_C not found (run run_scatC_check.sh)")

# %% [markdown]
# ## Partial waves of psi psibar -> psi psibar (tree and one loop) and check (6): unitarity for J = 0 and J = 1

# %%
def wigner_d(j, mp_, m, theta):
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    f = math.factorial
    tot = 0.0
    for k in range(0, int(round(2 * j)) + 1):
        a, b, cc, d = j + m - k, k, j - k - mp_, k - m + mp_
        if min(a, b, cc, d) < -1e-9:
            continue
        a, b, cc, d = (int(round(x)) for x in (a, b, cc, d))
        tot += (-1) ** (k - m + mp_) * c ** (2 * j + m - mp_ - 2 * k) * s ** (2 * k - m + mp_) / (f(a) * f(b) * f(cc) * f(d))
    jm = lambda x: math.factorial(int(round(x)))
    return math.sqrt(jm(j + mp_) * jm(j - mp_) * jm(j + m) * jm(j - m)) * tot


def nodes(A, n):
    xg, wg = np.polynomial.legendre.leggauss(n)
    ua, ub = math.log(A - 1), math.log(A)
    u = ua + (ub - ua) * (xg + 1) / 2
    c, w = A - np.exp(u), np.exp(u) * (ub - ua) / 2 * wg
    return np.concatenate([c, -c]), np.concatenate([w, w])


def peak_A(rs):
    e = rs / 2
    p, k = math.sqrt(e * e - BM2), math.sqrt(max(e * e - M2, 1e-30))
    cands = [1 + M2 / (2 * p * p)]
    if rs > 2 * MPHI:
        cands.append((2 * e * e - M2) / (2 * p * k))
    return min(cands)


def beta(kind, rs):
    if kind == "phiphi":
        return math.sqrt(1 - 4 * M2 / rs ** 2) if rs > 2 * MPHI else 0.0
    return math.sqrt(1 - 4 * BM2 / rs ** 2)


ST0 = [(0.5, 0.5), (-0.5, -0.5)]                                        # J = 0 psi psibar states (l = 0)
ST1 = [(0.5, 0.5, 0), (-0.5, -0.5, 0), (0.5, -0.5, 1), (-0.5, 0.5, -1)]  # J = 1: (h1, h2, l = h1 - h2)
RSP = np.unique(np.concatenate([2 * MPSI + np.geomspace(2e-3, 2 * MPHI - 2 * MPSI - 1e-3, 14),
                                2 * MPHI + np.geomspace(1e-3, 2.0, 30), [5.0, 10.0]]))
MUS = (0.5, 1.0, 2.0)
NODES = {rs: nodes(peak_A(rs), NQ) for rs in RSP}
LP = {}
for L in collier([(rs, c, mu) for rs in RSP for c in NODES[rs][0] for mu in MUS]):
    LP.setdefault((round(L["sqrts"], 9), round(L["mu"], 9)), []).append(L)


def pw_psi(rs, mu, J):
    """psi psibar block of a^J: tree / y^2 and one loop (S-matrix element) / y^4, index [final, initial]"""
    sts = ST0 if J == 0 else ST1
    n = len(sts)
    tr, lo = np.zeros((n, n), complex), np.zeros((n, n), complex)
    c, w = NODES[rs]
    norm = beta("psipsibar", rs) / (32 * math.pi)
    for L, ci, wi in zip(LP[(round(rs, 9), round(mu, 9))], c, w):
        th = math.acos(ci)
        for a, si in enumerate(sts):
            for b, sf in enumerate(sts):
                li, lf = (0, 0) if J == 0 else (si[2], sf[2])
                d = wigner_d(J, li, lf, th)
                cl = classes(L, (si[0], si[1], sf[0], sf[1]))
                tr[b, a] += wi * norm * d * cl["tree"]
                lo[b, a] += wi * norm * d * cl["os"]
    return tr, lo


PW = {(rs, mu, 0): pw_psi(rs, mu, 0) for rs in RSP for mu in MUS}
PW.update({(rs, 1.0, 1): pw_psi(rs, 1.0, 1) for rs in RSP})
# tree partial waves of psi psibar <-> phi phi (J = 0) for the unitarity sum (as in pw_numeric.py)


def tree_psiphi(rs):
    """a^0_{phiphi, psipsibar(hh)} / y^2 for h = +, - (tree)"""
    if rs <= 2 * MPHI:
        return np.zeros(2)
    c, w = nodes(peak_A(rs), NQ)
    norm = math.sqrt(beta("phiphi", rs) * beta("psipsibar", rs)) / math.sqrt(2) / (32 * math.pi)
    out = np.zeros(2, complex)
    for j, hh in enumerate(ST0):
        i = state("psipsibar", hh, rs, 0.0)
        for ci, wi in zip(c, w):
            f = state("phiphi", None, rs, math.acos(ci))
            out[j] += wi * norm * sum(bar(i["v"]) @ (MPSI * ONE - slash(i["p"] - k)) @ i["u"] / (mdot(i["p"] - k, i["p"] - k) - BM2)
                                      for k in f["k"])
    return out


TPP = {rs: tree_psiphi(rs) for rs in RSP}
dev6, dev6j1, dev6j1far = 0.0, 0.0, 0.0
for rs in RSP:
    tr0, lo0 = PW[(rs, 1.0, 0)]
    x = TPP[rs]
    pred = tr0 @ tr0.conj().T + np.outer(x.conj(), x)                   # sum over psi psibar(++, --) and phi phi
    dev6 = max(dev6, np.abs((lo0 - lo0.conj().T) / 2j - pred).max() / np.abs(pred).max())
    tr1, lo1 = PW[(rs, 1.0, 1)]
    pred1 = tr1 @ tr1.conj().T
    d1 = np.abs((lo1 - lo1.conj().T) / 2j - pred1).max() / np.abs(pred1).max()
    dev6j1 = max(dev6j1, d1)
    if math.sqrt(rs ** 2 / 4 - BM2) >= 0.1 * MPSI:
        dev6j1far = max(dev6j1far, d1)
print(f"check 6: partial-wave unitarity Abs a^(1) = a^(0) a^(0)+ of psi psibar -> psi psibar ({len(RSP)} energies, 2M < sqrt(s) <= 10m):"
      f" J = 0 (with phi phi): {dev6:.1e}, J = 1: {dev6j1far:.1e} for p >= 0.1 M ({dev6j1:.1e} at the threshold, where both sides"
      f" are ~ p^6 ~ 1e-12; relative to the largest element)")
print("  tree psi psibar -> phi phi: max |Im| =", f"{max(np.abs(TPP[rs].imag).max() for rs in RSP):.1e}",
      "; one-loop psi psibar block symmetric:", f"{max(np.abs(PW[(rs, 1.0, 0)][1] - PW[(rs, 1.0, 0)][1].T).max() for rs in RSP):.1e}")
print("  J = 0 tree x 16 pi (sqrt(s) = 10): ", np.round(16 * math.pi * PW[(10.0, 1.0, 0)][0].real, 5).tolist(),
      " hermiticity of the tree:", f"{max(np.abs(PW[(rs, 1.0, 0)][0] - PW[(rs, 1.0, 0)][0].conj().T).max() for rs in RSP):.1e}")

# %% [markdown]
# ## The elements with phi phi at one loop (as in step (8), pw_numeric.py: work/pw_collier, Eqs. (16), (20))

# %%
RS1 = [rs for rs in RSP if rs > 2 * MPHI]
nodes1 = {rs: nodes(peak_A(rs), NQ) for rs in RS1}
with open(os.path.join(HERE, "work", "scatC_pw_nodes.txt"), "w") as fh:
    for rs in RS1:
        for c in nodes1[rs][0]:
            for mu in MUS:
                fh.write("%.17e %.17e %.17e\n" % (rs, c, mu))
subprocess.run([os.path.join(HERE, "work", "pw_collier"), "scatC_pw_nodes.txt", "scatC_pw_amp.csv"], cwd=os.path.join(HERE, "work"),
               check=True, capture_output=True)
loop = {}
with open(os.path.join(HERE, "work", "scatC_pw_amp.csv")) as fh:
    for r in csv.DictReader(fh):
        key = (round(float(r["sqrts"]), 9), round(float(r["mu"]), 9))
        loop.setdefault(key, []).append({k: complex(float(r["re_" + k]), float(r["im_" + k])) for k in ("ay", "al", "b", "mAl", "mAy")})


def loop_structures(rs, mu):
    """J = 0 one-loop a_{phiphi,phiphi} = lambda^2 A_ll + y^4 A_yy + lambda y^2 A_ly, a_{phiphi,psipsibar(hh)} = y^4 B_yy[h]
    + lambda y^2 B_ly[h] (S-matrix elements, pole masses), complex (copied from pw_numeric.py)"""
    L = math.log(mu ** 2)
    c, w = nodes1[rs]
    rows = loop[(round(rs, 9), round(mu, 9))]
    res = 4 * (SP["B0phi"] + L + SP["B0pphi"])
    dmp = SP["B0psi"] + SP["B1psi"] + L / 2
    drs = (SP["B1psi"] - L / 2 + 2 * 0.49 * (SP["B0ppsi"] + SP["B1ppsi"])) - 2 * (SP["B0phi"] + L + SP["B0pphi"])
    bphi, bpsi = beta("phiphi", rs), beta("psipsibar", rs)
    nA, nB = 0.5 * bphi / (32 * math.pi * K), math.sqrt(bphi * bpsi) / math.sqrt(2) / (32 * math.pi * K)
    out = {"A_ll": 0j, "A_yy": 0j, "A_ly": 0j, "B_yy": np.zeros(2, complex), "B_ly": np.zeros(2, complex)}
    ist = [state("psipsibar", hh, rs, 0.0) for hh in ST0]
    for ci, wi, r in zip(c, w, rows):
        k1 = state("phiphi", None, rs, math.acos(ci))["k"][0]
        out["A_ll"] += wi * nA * r["mAl"]
        out["A_yy"] += wi * nA * r["mAy"]
        out["A_ly"] += wi * nA * res
        for j, st in enumerate(ist):
            vu, vku = bar(st["v"]) @ st["u"], bar(st["v"]) @ slash(k1) @ st["u"]
            t = mdot(st["p"] - k1, st["p"] - k1)
            X, W = t - 0.49, 2 * 0.49 + 2 - rs * rs - t - 0.49
            b0 = 1 / X - 1 / W
            conv_a = -MPSI * dmp * (1 / X + 1 / W)
            conv_b = drs * b0 - 2 * 0.49 * dmp * (1 / X ** 2 - 1 / W ** 2)
            out["B_yy"][j] += wi * nB * ((r["ay"] + conv_a) * vu + (r["b"] + conv_b) * vku)
            out["B_ly"][j] += wi * nB * r["al"] * vu
    return out


LS = {(rs, mu): loop_structures(rs, mu) for rs in RS1 for mu in MUS}


def a0_matrix(rs, y2, lam, mu, loop_=True):
    """the J = 0 matrix in (phi phi, psi psibar(++), psi psibar(--)) (only psi psibar below 2m): tree + one loop, index [final, initial]"""
    tr, lo = PW[(rs, mu, 0)]
    if rs <= 2 * MPHI:
        return y2 * tr + (y2 ** 2 * lo if loop_ else 0)
    a = np.zeros((3, 3), complex)
    a[1:, 1:] = y2 * tr + (y2 ** 2 * lo if loop_ else 0)
    a[0, 0] = -lam / (32 * math.pi) * beta("phiphi", rs)                 # tree phi phi: -lambda x beta/(32 pi) x (1/sqrt 2)^2 x 2
    x = y2 * TPP[rs]
    if loop_:
        o = LS[(rs, mu)]
        a[0, 0] += lam ** 2 * o["A_ll"] + y2 ** 2 * o["A_yy"] + lam * y2 * o["A_ly"]
        x = x + y2 ** 2 * o["B_yy"] + lam * y2 * o["B_ly"]
    a[0, 1:] = x
    a[1:, 0] = x
    return a


# full unitarity check of the J = 0 matrix at y = lambda = 1, mu = m (all entries)
dev7 = 0.0
for rs in RS1:
    a0t = a0_matrix(rs, 1.0, 1.0, 1.0, loop_=False)
    a1 = a0_matrix(rs, 1.0, 1.0, 1.0) - a0t
    pred = a0t @ a0t.conj().T
    dev7 = max(dev7, np.abs((a1 - a1.conj().T) / 2j - pred).max() / np.abs(pred).max())
print(f"check 7: unitarity of the full J = 0 one-loop matrix (phi phi and psi psibar, y = lambda = 1, {len(RS1)} energies): {dev7:.1e}")
print("  tree phi phi element against step (8) (-lambda beta/(32 pi)):", f"{a0_matrix(5.0, 0.0, 1.0, 1.0, False)[0, 0].real:.10f}",
      f"{-beta('phiphi', 5.0) / (32 * math.pi):.10f}")

# %% [markdown]
# ## The bound (C): eigenvalues of Re a^0 of the full J = 0 matrix, 2M < sqrt(s) <= 4m

# %%
K2 = K


def rhs(t, v):
    y2, lam = v
    return [10 * y2 ** 2 / K2, (3 * lam ** 2 + 8 * lam * y2 - 48 * y2 ** 2) / K2]


def run_to(y0, lam0, mu):
    if mu == 1.0:
        return y0 ** 2, lam0
    sol = solve_ivp(rhs, [0, math.log(mu)], [y0 ** 2, lam0], rtol=1e-11, atol=1e-13)
    return sol.y[0, -1], sol.y[1, -1]


RS_C = [rs for rs in RSP if rs <= 4.0 + 1e-9]


def metric(y0, lam0, mu, kind):
    """max over 2M < sqrt(s) <= 4m of the largest |eigenvalue| of Re a^0, over 1/2 (allowed if <= 1).  kind: 'full' (one loop,
    full matrix), 'tree' (tree, same range), 'old' (step (8): |Re a_phiphi,phiphi| and |a_phiphi,psipsibar| at one loop, sqrt(s) > 2m)"""
    y2, lam = run_to(y0, lam0, mu)
    worst = 0.0
    for rs in RS_C:
        if kind == "old":
            if rs <= 2 * MPHI:
                continue
            a = a0_matrix(rs, y2, lam, mu)
            worst = max(worst, abs(a[0, 0].real), abs(a[0, 1]), abs(a[0, 2]))
            continue
        a = a0_matrix(rs, y2, lam, mu, loop_=(kind == "full"))
        ev = np.linalg.eigvalsh((a + a.conj().T).real / 2)
        worst = max(worst, np.max(np.abs(ev)))
    return worst / 0.5


def bisect(f, lo, hi, n=40):
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) else (lo, mid)
    return lo


res_C = {}
for mu in MUS:
    for kind in ("full", "tree", "old"):
        if kind != "full" and mu != 1.0:
            continue
        ym0 = bisect(lambda y: metric(y, 0.0, mu, kind) <= 1, 0.0, 8.0)
        ym1 = bisect(lambda y: metric(y, 1.0, mu, kind) <= 1, 0.0, 8.0)
        lp = bisect(lambda l: metric(1.0, l, mu, kind) <= 1, 0.0, 200.0)
        lm = -bisect(lambda l: metric(1.0, -l, mu, kind) <= 1, 0.0, 200.0)
        res_C[(kind, mu)] = (ym0, ym1, lm, lp)
        print(f"(C) {kind:4} mu = {mu}: lambda = 0: y <= {ym0:.4f};  lambda = 1: y <= {ym1:.4f};  y = 1: {lm:.2f} <= lambda <= {lp:.2f}")
# the same with the range extended to sqrt(s) <= 10 m (mu = m)
RS_C4 = RS_C
RS_C = [rs for rs in RSP if rs <= 10.0 + 1e-9]
for kind in ("full", "tree"):
    print(f"(C) {kind:4} mu = 1.0, sqrt(s) <= 10m: lambda = 0: y <= {bisect(lambda y: metric(y, 0.0, 1.0, kind) <= 1, 0.0, 8.0):.4f}")
RS_C = RS_C4
# where the y-bound is set (lambda = 0, mu = m): sqrt(s) and the eigenvector
y_b = res_C[("full", 1.0)][0]
best = max(((rs, np.linalg.eigh((a0_matrix(rs, y_b ** 2, 0.0, 1.0) + a0_matrix(rs, y_b ** 2, 0.0, 1.0).conj().T).real / 2))
            for rs in RS_C), key=lambda z: np.max(np.abs(z[1][0])))
k_ = int(np.argmax(np.abs(best[1][0])))
print(f"  the y-bound (lambda = 0, mu = m) is set at sqrt(s) = {best[0]:.3f} by the eigenvalue {best[1][0][k_]:+.4f} with eigenvector"
      f" {np.round(best[1][1][:, k_], 3).tolist()}")

# %% [markdown]
# ## Grid of the (y, lambda) plane, CSV and figure

# %%
YG, LG = np.linspace(0, 4.5, 46), np.linspace(-84, 70, 78)
grid = {(kind, mu): np.array([[metric(yv, lv, mu, kind) for yv in YG] for lv in LG]) for kind, mu in
        (("full", 0.5), ("full", 1.0), ("full", 2.0), ("tree", 1.0), ("old", 1.0))}
with open(os.path.join(HERE, "results", "scatC.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["# MadLoop: scheme", "sqrts", "costheta", "mu_R", "born_madloop", "born_hand", "finite_madloop", "finite_hand", "eps1", "reldev"])
    w.writerows(ml_rows)
    w.writerow([])
    w.writerow(["y_m", "lambda_m", "metric_full_mu1", "metric_full_mu0.5", "metric_full_mu2", "metric_tree_4m", "metric_old_C"])
    for i, lv in enumerate(LG):
        for j, yv in enumerate(YG):
            w.writerow([yv, lv, grid[("full", 1.0)][i, j], grid[("full", 0.5)][i, j], grid[("full", 2.0)][i, j], grid[("tree", 1.0)][i, j],
                        grid[("old", 1.0)][i, j]])
print("wrote results/scatC.csv")

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
pax = [math.sqrt(rs ** 2 / 4 - BM2) / MPSI for rs in RSP]
for (b, a), col, lab in (((0, 0), "C0", r"$(++)\to(++)$"), ((1, 0), "C1", r"$(++)\to(--)$")):
    got, ref = [], []
    for rs in RSP:
        tr0, lo0 = PW[(rs, 1.0, 0)]
        x = TPP[rs]
        pred = tr0 @ tr0.conj().T + np.outer(x.conj(), x)
        got.append(lo0[b, a].imag)
        ref.append(pred[b, a].real)
    ax.plot(pax, got, color=col, label=lab)
    ax.plot(pax, ref, color=col, ls="none", marker="o", mfc="none", ms=3)
ax.axvline(math.sqrt(1 - BM2) / MPSI, color="0.6", lw=0.5, zorder=0)
ax.set_xscale("log")
ax.set_xlabel(r"$p/M$ ($\psi$ momentum)")
ax.set_ylabel(r"$\mathrm{Abs}\,a^{0(1)}_{\psi\bar\psi}$ ($y=1$)")
ax.legend(fontsize=7)
ya = math.sqrt(8 * math.pi / 3)
ax2.plot([0, ya, ya, 0], [16 * math.pi, 16 * math.pi, -16 * math.pi, -16 * math.pi], color="k", lw=0.8)
ax2.contour(YG, LG, grid[("tree", 1.0)], levels=[1.0], colors="0.5", linestyles="-", linewidths=0.8)
ax2.contour(YG, LG, grid[("old", 1.0)], levels=[1.0], colors="C1", linestyles="-.", linewidths=0.8)
ax2.contour(YG, LG, grid[("full", 1.0)], levels=[1.0], colors="C0", linestyles="-", linewidths=1.2)
for mu in (0.5, 2.0):
    ax2.contour(YG, LG, grid[("full", mu)], levels=[1.0], colors="C0", linestyles="--", linewidths=0.6)
ax2.plot([1.0], [1.0], marker="*", color="C3", ms=7, ls="none")
hd = [plt.Line2D([], [], color="k", lw=0.8), plt.Line2D([], [], color="0.5", lw=0.8), plt.Line2D([], [], color="C1", ls="-.", lw=0.8),
      plt.Line2D([], [], color="C0", lw=1.2), plt.Line2D([], [], color="C0", ls="--", lw=0.6)]
ax2.legend(hd, [r"(A) tree, $s\to\infty$", r"tree, $\sqrt{s}\leq 4m$", r"(C) step 8 ($\phi\phi$ elements)", r"(C) full $J=0$, $\mu=m$",
                r"(C), $\mu=m/2,\ 2m$"], fontsize=5.8, loc="center left", bbox_to_anchor=(0.0, 0.42))
ax2.set_xlim(0, 4.5)
ax2.set_ylim(-84, 70)
ax2.set_xlabel(r"$y$ ($\mu=m$)")
ax2.set_ylabel(r"$\lambda$ ($\mu=m$)")
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "scatC_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
