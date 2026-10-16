# %% [markdown]
# # Step (9): hadronic t tbar cross sections from f0, f1, fbar1 against aMC@NLO
#
# Research note models/qcd, step (9).  sigma = sum_ij int_{tau0}^1 dtau L_ij(tau) sigma_ij(tau S), tau0 = 4 m^2/S, with
#   sigma_ij = alpha_s^2/m^2 [f0 + 4 pi alpha_s (f1 + fbar1 ln(mu^2/m^2))]  (mu_R = mu_F = mu, alpha_s = alpha_s^(5), pole mass m = 172.5),
# f1 from results/hq_f1_<chan>.csv (this work; spline in beta of f1 minus the Coulomb and logarithmic threshold terms above rho = 0.64,
# spline in ln rho below; with the switch at rho = 0.19 the error was 5e-4 of sigma at 13 TeV, checked with the exact f1 of hq_cm.wl), fbar1 and f0 from hq_lib.py, alpha_s at two loops from alpha_s(M_Z) = 0.119 (the value of the PDF; exact
# implicit solution, Eq. (run2)), luminosities from the NNPDF2.3 NLO grid of MadGraph (hq_lumi.f).  Compared with aMC@NLO (hq_mg5.sh) at
# 13 TeV (p p; mu = m/2, m, 2m) and 1.96 TeV (p pbar; mu = m): the second line after 'Total ABS and Total:' of the last res_<k>.txt.
# Also the LO, the channel decomposition, sigma with the MS-bar mass m(m) (App. L), and the p pbar runs of the patched MG5 (hq_mg5_fix.sh,
# work/hq/amc_fix, if present).  -> results/hq_hadronic.csv
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python hq_hadronic.py

# %%
import csv, glob, os, re, subprocess, sys
import numpy as np
from fractions import Fraction
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
sys.path.insert(0, HERE)
import hq_lib as H
WORK = os.path.join(HERE, "work", "hq")
GEV2PB = 0.3893793721e9
MT, MZ, ASMZ = 172.5, 91.188, 0.119
b0 = float(H.B0)/(4*np.pi); b1 = (102 - 38*5/3)/(16*np.pi**2)

def alphas(mu):
    F = lambda a: 1/(b0*a) + b1/b0**2*np.log(b0*a/(1 + b1*a/b0))
    rhs = F(ASMZ) + np.log(mu**2/MZ**2)
    return brentq(lambda a: F(a) - rhs, 1e-4, 0.5, xtol=1e-16, rtol=1e-15)

def load_f1(c):
    pts = []
    for r in csv.DictReader(open(os.path.join(HERE, "results", f"hq_f1_{c}.csv"))):
        pts.append((4/float(Fraction(r["s"])), float(r["f1"])))
    return sorted(pts)

def thr_sing(c, b):
    """Coulomb and logarithmic threshold terms (Eq. (hqthr) without the constant)"""
    L = np.log(8*b*b)
    if c == "qq":
        return float(H.f0_qq(1 - b*b))/(4*np.pi**2)*((4/3 - 1.5)*np.pi**2/(2*b) + 2*4/3*L**2 - (8*4/3 + 3)*L)
    if c == "gg":
        return float(H.f0_gg(1 - b*b))/(4*np.pi**2)*((4/3 - 15/14)*np.pi**2/(2*b) + 2*3*L**2 - 61*3/7*L)
    return 0.0

RSW, NOV = 0.64, 2   # switch between the two splines at rho = RSW (beta = 0.6); each spline also uses NOV points beyond it
class F1:
    def __init__(self, c, pts):
        self.c = c
        rho = np.array([p[0] for p in pts]); f = np.array([p[1] for p in pts]); o = np.argsort(rho); rho, f = rho[o], f[o]
        ia = np.arange(max(np.where(rho >= RSW - 1e-12)[0][0] - NOV, 0), len(rho))
        b = np.sqrt(1 - rho[ia]); g = f[ia] - np.array([thr_sing(c, x) for x in b]); o = np.argsort(b)
        self.sA = CubicSpline(np.concatenate([[0.0], b[o]]), np.concatenate([[0.0], g[o]]))
        ib = np.arange(0, min(np.where(rho <= RSW + 1e-12)[0][-1] + 1 + NOV, len(rho)))
        self.sB = CubicSpline(np.log(rho[ib]), f[ib])
    def __call__(self, rho):
        if rho >= RSW:
            b = np.sqrt(1 - rho); return float(self.sA(b)) + thr_sing(self.c, b)
        return float(self.sB(np.log(rho)))

# %% [markdown]
# ## Luminosities

# %%
def build_lumi():
    d = os.path.join(WORK, "lumi"); os.makedirs(d, exist_ok=True)
    mg = os.path.expanduser("~/hep/MG5_aMC_v3_8_1")
    for f in ("Template/Common/Source/PDF/NNPDFDriver.f", "Template/NLO/lib/Pdfdata/NNPDF23nlo_as_0119_qed_mem0.grid"):
        src = os.path.join(mg, f); dst = os.path.join(d, os.path.basename(f))
        if not os.path.exists(dst):
            open(dst, "wb").write(open(src, "rb").read())
    env = dict(os.environ)
    env.setdefault("SDKROOT", subprocess.run(["xcrun", "--show-sdk-path"], capture_output=True, text=True).stdout.strip())
    subprocess.run(["gfortran", "-O2", "-o", "lumi", os.path.join(HERE, "hq_lumi.f"), "NNPDFDriver.f"], cwd=d, env=env, check=True,
                   stderr=subprocess.DEVNULL)
    return d

LUMIDIR = build_lumi()
def lumis(ipbar, mu, taus):
    inp = f"{ipbar}\n{mu}\n{len(taus)}\n" + "".join(f"{t:.17e}\n" for t in taus)
    out = subprocess.run(["./lumi"], cwd=LUMIDIR, input=inp, capture_output=True, text=True, check=True).stdout
    rows = [l.split() for l in out.splitlines() if len(l.split()) == 4 and "E" in l]
    return np.array([[float(x) for x in r] for r in rows])

def sigma(Ecm, ipbar, mu, f1s, n=240, m=MT, shift=None):
    """per channel (LO, NLO) in pb; shift: m is the MS-bar mass m(m) -> f1 gets the shift of Eq. (hqmsbar), fbar1 does not (its shift
    belongs to m(mu) and cancels against the running of m(mu) = m(m) [1 - 3 C_F alpha_s/(4 pi) ln(mu^2/m^2)] at this order)"""
    tau0 = 4*m**2/Ecm**2; a = alphas(mu); L = np.log(mu**2/m**2)
    x, w = np.polynomial.legendre.leggauss(n)
    y = np.log(tau0)*(1 - x)/2; wy = w*(-np.log(tau0))/2; rho = np.exp(y)
    lu = lumis(ipbar, mu, tau0/rho); jac = wy*tau0/rho
    res = {}
    for c, col in (("gg", 1), ("qq", 2), ("qg", 3)):
        f0f = {"gg": H.f0_gg, "qq": H.f0_qq}.get(c)
        f0 = np.array([float(f0f(r)) if f0f else 0.0 for r in rho])
        fb = np.array([float({"gg": H.fbar_gg, "qq": H.fbar_qq, "qg": H.fbar_qg}[c](r)) for r in rho])
        f1 = np.array([f1s[c](r) for r in rho])
        if shift and f0f:
            f1 = f1 + np.array([float(H.msbar_shift(f0f, r)[0]) for r in rho])
        lo = np.sum(jac*lu[:, col]*a**2/m**2*f0)*GEV2PB
        nlo = np.sum(jac*lu[:, col]*a**2/m**2*(f0 + 4*np.pi*a*(f1 + fb*L)))*GEV2PB
        res[c] = (lo, nlo)
    return a, res

# %% [markdown]
# ## aMC@NLO

# %%
def amc(run, base="amc_had"):
    """sigma, error (pb) of <base>/Events/run_<run>[_LO]: the second line after 'Total ABS and Total:' of the last res_<k>.txt"""
    files = glob.glob(os.path.join(WORK, base, "Events", f"run_{run:02d}*", "res_*.txt"))
    last = max(files, key=lambda f: int(re.search(r"res_(\d+)\.txt", f).group(1)))
    m = re.search(r"Total:\s*\n\s*[0-9.eE+-]+\s*\+-\s*[0-9.eE+-]+[^\n]*\n\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)", open(last).read())
    return float(m.group(1)), float(m.group(2))

def amc_mean(runs):
    v = [amc(r) for r in runs]; w = [1/e**2 for _, e in v]
    return sum(x*wi for (x, _), wi in zip(v, w))/sum(w), sum(w)**-0.5

f1s = {c: F1(c, load_f1(c)) for c in ("qq", "gg", "qg")}
# error of the interpolation of f1: spline vs the exact f1 (hq_cm.wl) at the 80 Gauss-Legendre nodes, mu = m (pb)
def interp_error(Ecm, ipbar, n=80):
    ex = {}
    for r in csv.DictReader(open(os.path.join(HERE, "results", "hq_cm_nodes.csv"))):
        if float(r["sqrtS"]) == Ecm:
            ex.setdefault(r["chan"], []).append((float(r["rho"]), float(r["f1_cm"])))
    tau0 = 4*MT**2/Ecm**2; a = alphas(MT)
    x, w = np.polynomial.legendre.leggauss(n)
    y = np.log(tau0)*(1 - x)/2; wy = w*(-np.log(tau0))/2; rho = np.exp(y)
    lu = lumis(ipbar, MT, tau0/rho); jac = wy*tau0/rho; out = {}
    for c, col in (("gg", 1), ("qq", 2), ("qg", 3)):
        e = np.array(sorted(ex[c])); o = np.argsort(rho); assert np.allclose(e[:, 0], rho[o], rtol=1e-12)
        d = np.empty(n); d[o] = np.array([f1s[c](r) for r in rho[o]]) - e[:, 1]
        out[c] = np.sum(jac*lu[:, col]*a**2/MT**2*4*np.pi*a*d)*GEV2PB
    return out
if os.path.exists(os.path.join(HERE, "results", "hq_cm_nodes.csv")):
    for E, ip in ((13000.0, 0), (1960.0, 1)):
        ie = interp_error(E, ip)
        print(f"interpolation error of f1 at {E/1000} TeV (ipbar = {ip}), mu = m: " + ", ".join(f"{c} {v:+.4f}" for c, v in ie.items())
              + f" pb, total {sum(ie.values()):+.4f} pb")
# (label, sqrt(S), ipbar of beam 2, mu, NLO runs, LO run, run of the patched MG5 (hq_mg5_fix.sh))
cases = (("LHC 13 TeV p p", 13000.0, 0, MT/2, (2,), None, None), ("LHC 13 TeV p p", 13000.0, 0, MT, (1, 10), 6, None),
         ("LHC 13 TeV p p", 13000.0, 0, 2*MT, (3,), None, None),
         ("1.96 TeV p pbar", 1960.0, 1, MT/2, (7,), None, 3), ("1.96 TeV p pbar", 1960.0, 1, MT, (4, 9, 12), 5, 1), ("1.96 TeV p pbar", 1960.0, 1, 2*MT, (8,), None, None),
         ("1.96 TeV p p", 1960.0, 0, MT, (11,), None, None), ("13 TeV p pbar", 13000.0, 1, MT, (13,), None, 2))
HAVE_FIX = os.path.isdir(os.path.join(WORK, "amc_fix", "Events"))
rows = []
for name, E, ip, mu, runs, lorun, fixrun in cases:
    a, r = sigma(E, ip, mu, f1s)
    lo = sum(v[0] for v in r.values()); nlo = sum(v[1] for v in r.values())
    m5, e5 = amc_mean(runs)
    l5, le5 = amc(lorun) if lorun else (float("nan"), float("nan"))
    print(f"{name}, mu = {mu}: alpha_s = {a:.6f};  LO {lo:.4f} (aMC {l5:.4f} +- {le5:.4f});  NLO {nlo:.4f} [gg {r['gg'][1]:.4f}, qq {r['qq'][1]:.4f}, "
          f"qg {r['qg'][1]:.4f}];  aMC@NLO {m5:.4f} +- {e5:.4f};  (ours - aMC)/error = {(nlo - m5)/e5:+.2f}, relative {(nlo - m5)/m5:+.2e}")
    f5, fe5 = amc(fixrun, "amc_fix") if (fixrun and HAVE_FIX) else (float("nan"), float("nan"))
    if fixrun and HAVE_FIX:
        print(f"    patched MG5 (use_evpr for p pbar): {f5:.4f} +- {fe5:.4f};  (ours - patched)/error = {(nlo - f5)/fe5:+.2f}, relative {(nlo - f5)/f5:+.2e}")
    rows.append([name, mu, a, lo, l5, le5, r["gg"][1], r["qq"][1], r["qg"][1], nlo, m5, e5, f5, fe5])
# the MS-bar mass m(m) that corresponds to m_p = 172.5 at one loop: m_p = m (1 + 4 alpha_s(m)/(3 pi))
mbar = brentq(lambda x: x*(1 + 4*alphas(x)/(3*np.pi)) - MT, 150, 172.5, xtol=1e-12)
for name, E, ip in (("LHC 13 TeV", 13000.0, 0), ("Tevatron 1.96 TeV", 1960.0, 1)):
    for k in (0.5, 1.0, 2.0):
        a, r = sigma(E, ip, k*mbar, f1s, m=mbar, shift=True)
        nlo = sum(v[1] for v in r.values()); lo = sum(v[0] for v in r.values())
        print(f"{name}, MS-bar mass m(m) = {mbar:.3f}, mu = {k} m(m): LO {lo:.3f}, NLO {nlo:.3f} pb")
        rows.append([name + " MSbar", k*mbar, a, lo, float("nan"), float("nan"), r["gg"][1], r["qq"][1], r["qg"][1], nlo, float("nan"), float("nan"),
                     float("nan"), float("nan")])
with open(os.path.join(HERE, "results", "hq_hadronic.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["collider", "mu", "alpha_s", "LO", "amc_LO", "amc_LO_err", "NLO_gg", "NLO_qq", "NLO_qg", "NLO", "amc", "amc_err", "amc_fixed", "amc_fixed_err"])
    w.writerows(rows)
print("wrote results/hq_hadronic.csv")
