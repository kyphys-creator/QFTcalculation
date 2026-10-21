"""Step 4 of the stable-lepton workflow (run_workflow.sh, README.md): each step against own calculations.

  (a) sigma(p p > lv+ lv-) of MG5 against own integral of q qbar -> gamma*/Z* -> lv+ lv- (q = u, d, s, c) over the same
      LHAPDF set at mu_F = sqrt(shat):  sigma_hat = (1/N_c) shat/(48 pi) sum_{h = L, R} 2 |A_h|^2 beta (3 - beta^2)/2,
      A_h = e^2 Q_q Q_lv/shat + g_Z^2 g_h^q g^lv/(shat - M_Z^2 + i M_Z Gamma_Z),  g_Z = e/(sw cw),  g_L = T3 - Q sw^2,
      g_R = -Q sw^2,  Q_lv = -1,  g^lv = sw^2 (lv couples to the photon and the Z as e_R, in both chiralities:
      generate_vll.wl);  SM.fr's inputs aEWM1, Gf, MZ and the param_card's Z width;
  (b) Pythia: every event keeps one lv+ and one lv- (status 1), with the param_card's mass;
  (c) HepMC -> Geant4: the primaries of each event (the status-1 particles less the neutrinos), and the lv momenta;
  (d) the energy deposited in the 0.3 mm silicon layers by lv+- (and by the charged hadrons with pT > 5 GeV, beta gamma
      > 10) against the most probable energy loss of Landau-Vavilov-Bichsel,
        Delta_p = xi [ln(2 m_e c^2 beta^2 gamma^2/I) + ln(xi/I) + j - beta^2 - delta(beta gamma)],  j = 0.200,
        xi = (K/2) <Z/A> rho x/beta^2  (PDG, Passage of particles through matter, eq. 34.12),
      with Sternheimer's density effect for Si, per crossing (its path length x and beta gamma from Geant4): the most
      probable value of deposit/Delta_p in bins of beta gamma;
  (e) the curvature of lv in the tracker (its 12 crossings smeared by 20 um in r phi and 50 um in z; a parabola fitted
      in the frame of the chord) against the true one, with own expected error from the hits and from multiple
      scattering (Highland in the beam pipe and in each layer, correlated along the track);
  (f) the mean momentum lost by lv between production and the first muon station (beam pipe, tracker, ECAL, HCAL, coil;
      |eta| < 0.8, beta < 0.8) against own continuous-slowing-down integral of the Bethe-Bloch mean loss on a straight
      line (I values of ICRU 37, Bragg's rule for brass and the gas, no density effect: delta/2 < 1.3% of the logarithm
      for beta < 0.8, beta gamma < 1.33);
  (g) the time of flight to the muon stations (smeared by 1 ns): 1/beta of the fit t_i = L_i/(beta c) against the one of
      own arrival times of the slowed-down lv of (f) (from the true momentum and the model's mass), with own expected
      error; the mass from the measured momentum (e) and 1/beta: the m for which own slowed-down lv arrives as measured,
      against the model's (and m = p sqrt(1/beta^2 - 1), which neglects the slowing down, for comparison).
Run with ~/hep/opt/lhc/bin/python.  Uses LHAPDF from MG5's HEPTools.  Figure: figs/checks.png.
"""
import gzip
import math
import re
import sys
from pathlib import Path

import numpy as np
import uproot
from scipy.stats import gaussian_kde

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
RUN = OUT / "vll_proc" / "Events" / "run_01"
sys.path.insert(0, str(Path.home() / "hep" / "MG5_aMC_v3_8_1" / "HEPTools" / "lhapdf6_py3" / "lib" / "python3.12" / "site-packages"))
import lhapdf  # noqa: E402

LV = 9000011
GEV_PB = 0.3893793721e9   # GeV^-2 -> pb
ME = 0.51099895           # MeV
K_BB = 0.307075           # MeV cm^2/mol
C_MM_NS = 299.792458
B_T = 3.8
LAYERS = np.array([30, 70, 110, 160, 250, 340, 430, 520, 610, 750, 900, 1050], float)   # mm (Detector.cc)
SIG_RPHI, SIG_Z, SIG_T = 0.020, 0.050, 1.0   # mm, mm, ns
RNG = np.random.default_rng(1)
results = []   # (check, verdict) lines for the summary


def verdict(name, ok, text):
    results.append((name, ok))
    print(f"  [{'ok' if ok else 'FAIL'}] {text}")


# ---------------------------------------------------------------- (a)
def card():
    banner = next(RUN.glob("*banner.txt"))
    txt = banner.read_text()
    pc = txt[txt.index("<slha>"):txt.index("</slha>")]
    vals = {}
    for line in pc.splitlines():
        mm = re.match(r"\s*\d+\s+([-+0-9.eE]+)\s+#\s*(\w+)", line)
        if mm:
            vals[mm.group(2).lower()] = float(mm.group(1))
    vals["wz"] = float(re.search(r"^DECAY\s+23\s+([-+0-9.eE]+)", pc, re.M).group(1))
    log = (OUT / "vll_run.log").read_text(errors="replace")
    xs, err = map(float, re.findall(r"Cross-section :\s*([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb", log)[-1])
    lhaid = int(re.search(r"^\s*(\d+)\s*=\s*lhaid", txt, re.M).group(1))
    scale = int(re.search(r"^\s*(-?\d+)\s*=\s*dynamical_scale_choice", txt, re.M).group(1))
    return vals, xs, err, lhaid, scale


def ew(vals):
    """SM.fr's internal parameters from aEWM1, Gf, MZ: e^2, sw^2"""
    aew = 1 / vals["aewm1"]
    mz, gf = vals["mz"], vals["gf"]
    mw = math.sqrt(mz ** 2 / 2 + math.sqrt(mz ** 4 / 4 - aew * math.pi * mz ** 2 / (gf * math.sqrt(2))))
    return 4 * math.pi * aew, 1 - mw ** 2 / mz ** 2


def own_sigma(vals, pdf, n_m=400, n_y=96):
    e2, sw2 = ew(vals)
    gz2 = e2 / (sw2 * (1 - sw2))
    mz, wz, M = vals["mz"], vals["wz"], vals["mlv"]
    S = 13000.0 ** 2
    quarks = {1: (-0.5, -1 / 3), 2: (0.5, 2 / 3), 3: (-0.5, -1 / 3), 4: (0.5, 2 / 3)}   # PDG id: T3, Q
    # m = 2M + (13 TeV - 2M) t^2: the threshold's beta ~ t is smooth in t
    xt, wt = np.polynomial.legendre.leggauss(n_m)
    t = 0.5 * (xt + 1)
    m = 2 * M + (13000.0 - 2 * M) * t ** 2
    dm = (13000.0 - 2 * M) * 2 * t * 0.5 * wt
    xy, wy = np.polynomial.legendre.leggauss(n_y)
    total = 0.0
    for mi, dmi in zip(m, dm):
        shat = mi * mi
        beta = math.sqrt(max(0.0, 1 - 4 * M * M / shat))
        tau = shat / S
        ymax = -0.5 * math.log(tau)
        x1, x2 = np.sqrt(tau) * np.exp(ymax * xy), np.sqrt(tau) * np.exp(-ymax * xy)
        prop = 1 / complex(shat - mz * mz, mz * wz)
        sig = 0.0
        for pid, (t3, q) in quarks.items():
            fq1 = np.array([pdf.xfxQ2(pid, a, shat) for a in x1]) / x1
            fa1 = np.array([pdf.xfxQ2(-pid, a, shat) for a in x1]) / x1
            fq2 = np.array([pdf.xfxQ2(pid, a, shat) for a in x2]) / x2
            fa2 = np.array([pdf.xfxQ2(-pid, a, shat) for a in x2]) / x2
            lum = ymax * np.sum(wy * (fq1 * fa2 + fa1 * fq2))
            amp2 = sum(abs(e2 * q * (-1) / shat + gz2 * g * sw2 * prop) ** 2 for g in (t3 - q * sw2, -q * sw2))
            sig += lum * (1 / 3) * shat / (48 * math.pi) * 2 * amp2 * beta * (3 - beta ** 2) / 2
        total += dmi * 2 * mi / S * sig
    return total * GEV_PB


def part_a():
    print("(a) the cross section")
    vals, xs, err, lhaid, scale = card()
    pdf = lhapdf.mkPDF(lhaid)
    own = own_sigma(vals, pdf)
    own2 = own_sigma(vals, pdf, 800, 160)
    print(f"  MLV = {vals['mlv']:.1f} GeV, lhaid {lhaid}, dynamical_scale_choice {scale} (4: sqrt(shat))")
    print(f"  MG5 {xs * 1e3:.4f} +- {err * 1e3:.4f} fb;  own {own * 1e3:.4f} fb (with twice the nodes {own2 * 1e3:.4f} fb);"
          f"  MG5/own - 1 = {xs / own - 1:+.4f} ({(xs - own) / err:+.1f} sigma)")
    verdict("a", scale == 4 and abs(xs - own) < 3 * err, "MG5 within 3 sigma of own integral")
    return vals


# ---------------------------------------------------------------- (b), (c)
def read_hepmc(path):
    """per event: the number of status-1 non-neutrino particles, and the lv's (pdg, p4, m)"""
    counts, lvs = [], []
    k = n_orph = 0
    with gzip.open(path, "rt") as f:
        for line in f:
            c = line[0]
            if c == "P":
                w = line.split()
                if k >= n_orph and w[8] == "1" and abs(int(w[2])) not in (12, 14, 16):
                    counts[-1] += 1
                if abs(int(w[2])) == LV and w[8] == "1":
                    lvs[-1].append((int(w[2]), float(w[3]), float(w[4]), float(w[5]), float(w[6]), float(w[7])))
                k += 1
            elif c == "V":
                w = line.split()
                n_orph, k = int(w[7]), 0
            elif c == "E":
                counts.append(0)
                lvs.append([])
    return counts, lvs


def part_bc(vals, f):
    print("(b) Pythia's events, (c) the primaries in Geant4")
    counts, lvs = read_hepmc(RUN / "tag_1_pythia8_events.hepmc.gz")
    nev = len(counts)
    pairs = sum(1 for l in lvs if sorted(p[0] for p in l) == [-LV, LV])
    masses = np.array([p[5] for l in lvs for p in l])
    print(f"  {nev} events; with one lv+ and one lv- of status 1: {pairs}; their masses {masses.min():.4f} to"
          f" {masses.max():.4f} GeV (MLV = {vals['mlv']:.4f})")
    verdict("b", pairs == nev and np.allclose(masses, vals["mlv"], rtol=1e-6), "every event has lv+ lv- with the model's mass")
    ev = f["event"].arrays(library="np")
    nprim = dict(zip(ev["evt"], ev["nprim"]))
    same = sum(1 for i in range(nev) if nprim.get(i) == counts[i])
    pr = f["prim"].arrays(library="np")
    sel = np.abs(pr["pdg"]) == LV
    g4 = {(e, p): np.array([x, y, z, en]) for e, p, x, y, z, en in
          zip(pr["evt"][sel], pr["pdg"][sel], pr["px"][sel], pr["py"][sel], pr["pz"][sel], pr["e"][sel])}
    dev = max(np.max(np.abs(g4[(i, p[0])] - np.array(p[1:5])) / p[4]) for i, l in enumerate(lvs) for p in l)
    print(f"  Geant4 events {len(nprim)}; with as many primaries as the HepMC event's status-1 non-neutrinos: {same};"
          f" largest relative difference of the lv four-momenta {dev:.1e}")
    verdict("c", len(nprim) == nev and same == nev and dev < 1e-9, "Geant4 got every event's particles and the lv momenta")
    return nev


# ---------------------------------------------------------------- (d)
SI = dict(za=14 / 28.0855, rho=2.33, I=173.0e-6, C=4.4355, x0=0.2015, x1=2.8716, a=0.14921, k=3.2546, d0=0.14)


def delta_sternheimer(bg, m):
    X = np.log10(bg)
    return np.where(X >= m["x1"], 2 * math.log(10) * X - m["C"],
                    np.where(X >= m["x0"], 2 * math.log(10) * X - m["C"] + m["a"] * np.clip(m["x1"] - X, 0, None) ** m["k"],
                             m["d0"] * 10 ** (2 * (X - m["x0"]))))


def delta_p(bg, x_cm):
    """Landau-Vavilov-Bichsel most probable energy loss in silicon, MeV"""
    b2 = bg ** 2 / (1 + bg ** 2)
    xi = 0.5 * K_BB * SI["za"] * SI["rho"] * x_cm / b2
    return xi * (np.log(2 * ME * bg ** 2 / SI["I"]) + np.log(xi / SI["I"]) + 0.200 - b2 - delta_sternheimer(bg, SI))


def mode(r):
    grid = np.linspace(0.5, 1.8, 1301)
    kde = gaussian_kde(r, bw_method=0.025 / np.std(r))
    return grid[np.argmax(kde(grid))]


def part_d(trk, pdg_of):
    print("(d) the energy deposits in silicon against Landau-Vavilov-Bichsel")
    pdg = np.array([pdg_of[(e, i)] for e, i in zip(trk["evt"], trk["id"])])
    ratio = trk["edep"] / 1e3 / delta_p(trk["bg"], trk["path"] / 10)
    is_lv = np.abs(pdg) == LV
    had = np.isin(np.abs(pdg), (211, 321, 2212)) & (trk["bg"] > 10)
    bins = [(is_lv, 0.4, 0.6), (is_lv, 0.6, 0.8), (is_lv, 0.8, 1.0), (is_lv, 1.0, 1.3), (is_lv, 1.3, 1.7), (is_lv, 1.7, 2.3),
            (is_lv, 2.3, 4.0), (had, 10, 1e4)]
    rows = []
    print("   particles   beta gamma   crossings   <x> (mm)   Delta_p (keV)   kappa   MPV(deposit/Delta_p)")
    for sel0, lo, hi in bins:
        sel = sel0 & (trk["bg"] >= lo) & (trk["bg"] < hi)
        r = ratio[sel]
        if len(r) < 200:
            continue
        mpv = mode(r)
        boot = [mode(RNG.choice(r, len(r))) for _ in range(20)]
        bg = np.median(trk["bg"][sel])
        x = np.median(trk["path"][sel])
        b2 = bg ** 2 / (1 + bg ** 2)
        kappa = 0.5 * K_BB * SI["za"] * SI["rho"] * x / 10 / b2 / (2 * ME * bg ** 2)
        rows.append((bg, mpv, np.std(boot), "lv" if sel0 is is_lv else "hadrons", kappa))
        print(f"   {rows[-1][3]:9s}   {lo:4.1f}-{hi:<6.4g}  {len(r):9d}   {x:8.3f}   {1e3 * delta_p(bg, x / 10):11.1f}"
              f"   {kappa:6.3f}   {mpv:.3f} +- {np.std(boot):.3f}")
    good = [abs(m - 1) < 0.05 for bg, m, s, who, kap in rows if kap < 0.05]
    verdict("d", all(good) and len(good) >= 4, "most probable deposits within 5% of Delta_p where kappa = xi/T_max < 0.05")
    return rows


# ---------------------------------------------------------------- (e)
def highland(p, beta, x_x0):
    return 0.0136 / (beta * p) * np.sqrt(x_x0) * (1 + 0.038 * np.log(x_x0 / beta ** 2))


def fit_track(h, q, pt_true, p_true, beta):
    """h: the 12 crossings (x, y, z in mm, ordered by layer).  Returns the fitted and true curvature (1/m), the expected
    error of the fitted one, and the fitted cot theta"""
    r = np.hypot(h[:, 0], h[:, 1])
    phi = np.arctan2(h[:, 1], h[:, 0]) + RNG.normal(0, SIG_RPHI, len(r)) / r
    xy = np.c_[r * np.cos(phi), r * np.sin(phi)] / 1e3
    z = (h[:, 2] + RNG.normal(0, SIG_Z, len(r))) / 1e3
    u = (xy[-1] - xy[0]) / np.linalg.norm(xy[-1] - xy[0])
    n = np.array([-u[1], u[0]])   # z x u
    xp, yp = (xy - xy[0]) @ u, (xy - xy[0]) @ n
    A = np.c_[np.ones_like(xp), xp, xp ** 2]
    coef, *_ = np.linalg.lstsq(A, yp, rcond=None)
    kappa = 2 * coef[2] / (1 + coef[1] ** 2) ** 1.5
    s = np.r_[0, np.cumsum(np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1])))] + r[0] / 1e3
    cot = np.polyfit(s, z, 1)[0]
    kappa_true = -q * 0.299792458 * B_T / pt_true
    # expected covariance: hits, and multiple scattering in the beam pipe (r = 23 mm, 0.8 mm Be) and layers 0-10
    sin_t = 1 / math.sqrt(1 + cot ** 2)
    sc_r = np.r_[22.9, LAYERS[:-1]]
    sc_x0 = np.r_[0.8 / 352.8, np.full(11, 0.3 / 93.7)] / sin_t
    theta = highland(p_true, beta, sc_x0) / sin_t   # projected on the bending plane
    xs = (sc_r - LAYERS[0]) / 1e3
    d = np.clip(xp[:, None] - xs[None, :], 0, None)
    V = (d * theta) @ (d * theta).T + np.eye(len(xp)) * (SIG_RPHI / 1e3) ** 2
    Ainv = np.linalg.pinv(A)
    cov = Ainv @ V @ Ainv.T
    return kappa, kappa_true, 2 * math.sqrt(cov[2, 2]), cot, 2 * math.sqrt((Ainv @ Ainv.T)[2, 2]) * SIG_RPHI / 1e3


def part_e(trk, prims):
    print("(e) the curvature from the tracker")
    by = {}
    for e, i, l, x, y, z in zip(trk["evt"], trk["id"], trk["layer"], trk["x"], trk["y"], trk["z"]):
        if (e, i) in prims:
            by.setdefault((e, i), {})[l] = (x, y, z)
    fits = {}
    for key, hits in by.items():
        if len(hits) < 12:
            continue
        pdg, px, py, pz, en = prims[key]
        q = -1 if pdg > 0 else 1
        pt, p = math.hypot(px, py), math.sqrt(px * px + py * py + pz * pz)
        h = np.array([hits[l] for l in range(12)])
        fits[key] = fit_track(h, q, pt, p, p / en) + (pt, p, en)
    k = np.array([v[0] for v in fits.values()])
    kt = np.array([v[1] for v in fits.values()])
    sk = np.array([v[2] for v in fits.values()])
    sk_hits = np.array([v[4] for v in fits.values()])
    pull = (k - kt) / sk
    half68 = 0.5 * (np.percentile(pull, 84.135) - np.percentile(pull, 15.865))
    pt = np.array([v[5] for v in fits.values()])
    print(f"  {len(fits)} lv with all 12 layers; median pT {np.median(pt):.0f} GeV; expected sigma(pT)/pT at the median"
          f" {np.median(sk / np.abs(kt)):.3f} ({np.median(sk_hits / np.abs(kt)):.3f} from the hits alone)")
    print(f"  pull (kappa - kappa_true)/sigma_expected: mean {pull.mean():+.3f} +- {pull.std() / math.sqrt(len(pull)):.3f},"
          f" rms {pull.std():.3f}, half-width of the central 68% {half68:.3f}; charge right for"
          f" {np.mean(np.sign(k) == np.sign(kt)):.4f}")
    verdict("e", abs(pull.mean()) < 0.1 and abs(half68 - 1) < 0.07, "curvature unbiased, its spread as expected (within 7%)")
    return fits, pull


# ---------------------------------------------------------------- (f), (g): own slowing down
def _bragg(parts):
    """Z/A and I (eV) of a mixture by Bragg's rule (ln I weighted by the electrons); parts: (mass fraction, Z/A, I)"""
    za = sum(w * z for w, z, _ in parts)
    return za, math.exp(sum(w * z * math.log(i) for w, z, i in parts) / za)


_BRASS = _bragg([(0.7, 29 / 63.546, 322.0), (0.3, 30 / 65.38, 330.0)])
_W_AR = 0.8 * 1.784 / (0.8 * 1.784 + 0.2 * 1.977)
_GAS = _bragg([(_W_AR, 18 / 39.948, 188.0), (1 - _W_AR, 22 / 44.0095, 85.0)])
# Z/A, rho (g/cm^3), I (eV) of ICRU 37
MAT = {"Be": (4 / 9.0122, 1.848, 63.7), "Si": (14 / 28.0855, 2.33, 173.0),
       "PbWO4": ((82 + 74 + 4 * 8) / (207.2 + 183.84 + 4 * 15.999), 8.28, 600.7),
       "brass": (_BRASS[0], 8.53, _BRASS[1]), "PVT": (0.54141, 1.032, 64.7), "Al": (13 / 26.9815, 2.699, 166.0),
       "gas": (_GAS[0], 1.82e-3, _GAS[1]), "Fe": (26 / 55.845, 7.874, 286.0)}
STATIONS = np.array([4000.0, 4800.0, 5930.0, 7060.0])   # inner radii of the muon stations, mm
BETA_STOP = 0.05


def segments():
    """(material, r_in, r_out) in mm, radially from the beam to the last muon station (Detector.cc)"""
    seg = [("Be", 22.5, 23.3)] + [("Si", r, r + 0.3) for r in LAYERS] + [("PbWO4", 1290, 1520)]
    for i in range(20):
        r = 1770 + 59 * i
        seg += [("brass", r, r + 55), ("PVT", r + 55, r + 59)]
    return seg + [("Al", 3000, 3300), ("gas", 4000, 4100), ("Fe", 4300, 4600), ("gas", 4800, 4900), ("Fe", 5100, 5730),
                  ("gas", 5930, 6030), ("Fe", 6230, 6860)]


def dedx(ek, M, mat):
    """Bethe-Bloch mean loss, MeV/cm, for charge 1, mass M and kinetic energy ek in MeV, no density effect"""
    za, rho, I = mat
    g = 1 + ek / M
    b2 = 1 - 1 / g ** 2
    wmax = 2 * ME * b2 * g * g / (1 + 2 * g * ME / M + (ME / M) ** 2)
    return K_BB * za * rho / b2 * (0.5 * np.log(2 * ME * b2 * g * g * wmax / (I * 1e-6) ** 2) - b2)


def slow_down(p, M, sin_t):
    """own continuous slowing down of lv (momentum p and mass M in GeV, arrays) on straight lines from the origin at
    polar angle theta, in radial steps of at most 5 mm: the momentum (GeV) at the first muon station, and the times (ns)
    at the four stations' inner radii, shape (4, n) (inf for a station it does not reach)"""
    p, M, sin_t = (np.asarray(a, float) for a in np.broadcast_arrays(p, M, sin_t))
    Mm = M * 1e3
    ek = (np.sqrt(p * p + M * M) - M) * 1e3
    t = np.zeros_like(ek)
    times = np.full((len(STATIONS),) + ek.shape, np.inf)
    p1 = None

    def beta(e):
        return np.sqrt(np.clip(1 - 1 / (1 + e / Mm) ** 2, 0, None))

    def drift(dl, b):   # time over the path dl (mm, per lv) at speed b
        with np.errstate(divide="ignore"):
            return np.where(b > BETA_STOP, dl / (np.maximum(b, BETA_STOP) * C_MM_NS), np.inf)

    r, k = 0.0, 0
    for name, r0, r1 in segments() + [(None, 1e9, 1e9)]:
        while k < len(STATIONS) and STATIONS[k] <= r0:
            t = t + drift((STATIONS[k] - r) / sin_t, beta(ek))
            r = STATIONS[k]
            times[k] = t
            if k == 0:
                p1 = np.sqrt((ek / 1e3 + M) ** 2 - M * M)
            k += 1
        if name is None:
            break
        t = t + drift((r0 - r) / sin_t, beta(ek))
        n = max(1, math.ceil((r1 - r0) / 5.0))
        dl = (r1 - r0) / n / sin_t
        for _ in range(n):
            b0 = beta(ek)
            alive = b0 > BETA_STOP
            with np.errstate(all="ignore"):
                loss = np.where(alive, dedx(np.where(alive, ek, Mm), Mm, MAT[name]) * dl / 10, ek)
            ek = np.maximum(ek - loss, 0)
            t = t + drift(dl, 0.5 * (b0 + beta(ek)))
        r = r1
    return p1, times


def part_f(muon, prims, M):
    print("(f) the mean momentum lost up to the first muon station against own Bethe-Bloch")
    rows = []
    for e, i, st, p1 in zip(muon["evt"], muon["id"], muon["station"], muon["p"]):
        if st != 0 or (e, i) not in prims:
            continue
        pdg, px, py, pz, en = prims[(e, i)]
        p = math.sqrt(px * px + py * py + pz * pz)
        if abs(math.asinh(pz / math.hypot(px, py))) > 0.8:
            continue
        rows.append((p / en, p, p1, math.hypot(px, py) / p))
    rows = np.array(rows)
    p1_own, _ = slow_down(rows[:, 1], M, rows[:, 3])
    rows = np.c_[rows[:, 0], rows[:, 1] - rows[:, 2], rows[:, 1] - p1_own]
    print("   beta at production   lv   <loss> Geant4 (GeV)   <loss> own (GeV)   Geant4/own")
    ok = True
    for lo, hi in [(0.3, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8)]:
        s = (rows[:, 0] >= lo) & (rows[:, 0] < hi)
        if s.sum() < 20:
            continue
        g4, own = rows[s, 1].mean(), rows[s, 2].mean()
        err = rows[s, 1].std() / math.sqrt(s.sum())
        print(f"   {lo:.1f}-{hi:.1f}             {s.sum():5d}   {g4:8.3f} +- {err:.3f}       {own:8.3f}       {g4 / own:.4f}")
        ok &= abs(g4 / own - 1) < 0.03 + 3 * err / own
    verdict("f", ok, "mean loss within 3% (plus 3 sigma) of own Bethe-Bloch in every bin")
    return rows


def own_inv_beta(p, M, sin_t, L, hit):
    """1/beta of the fit t_i = L_i/(beta c) to own arrival times at the stations hit (L, hit: shape (n, 4))"""
    _, times = slow_down(p, M, sin_t)
    with np.errstate(invalid="ignore"):
        num = np.sum(np.where(hit, times.T * L, 0), axis=1)
    return C_MM_NS * num / np.sum(np.where(hit, L * L, 0), axis=1)


def part_g(muon, fits, M):
    print("(g) the time of flight and the mass")
    st = {}
    for e, i, s, x, y, z, t in zip(muon["evt"], muon["id"], muon["station"], muon["x"], muon["y"], muon["z"], muon["t"]):
        st.setdefault((e, i), {})[s] = (math.sqrt(x * x + y * y + z * z), t + RNG.normal(0, SIG_T))
    rows, L, T, hit = [], [], [], []
    for key, v in fits.items():
        s = st.get(key, {})
        if len(s) < 3:
            continue
        kappa, kappa_true, s_k, cot, _, pt, p, en = v
        rows.append((p / en, p, pt / p, 0.299792458 * B_T / abs(kappa) * math.sqrt(1 + cot ** 2),
                     1 / math.sqrt(1 + cot ** 2), s_k / abs(kappa)))
        L.append([s[k][0] if k in s else 0 for k in range(4)])
        T.append([s[k][1] if k in s else 0 for k in range(4)])
        hit.append([k in s for k in range(4)])
    rows, L, T, hit = map(np.array, (rows, L, T, hit))
    beta0, p, sin_t, p_reco, sin_reco, s_p = rows.T
    inv = C_MM_NS * np.sum(T * L, axis=1) / np.sum(L * L, axis=1)
    s_inv = C_MM_NS * SIG_T / np.sqrt(np.sum(L * L, axis=1))
    inv_own = own_inv_beta(p, M, sin_t, L, hit)   # expected from the true momentum and the model's mass
    pull_prod, pull_own = (inv - 1 / beta0) / s_inv, (inv - inv_own) / s_inv
    print(f"  {len(inv)} lv with the tracker fit and at least 3 stations; sigma(1/beta) {np.median(s_inv):.4f}")
    print("   beta at production   lv   mean pull of 1/beta against: beta at production   own slowed-down lv  (rms)")
    ok = True
    for lo, hi in [(0.3, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]:
        s = (beta0 >= lo) & (beta0 < hi)
        if s.sum() < 20:
            continue
        f = s & np.isfinite(pull_own)   # own lv may stop before a station Geant4's reached
        stop = f" ({(s & ~f).sum()} stop earlier in own)" if (s & ~f).any() else ""
        print(f"   {lo:.1f}-{hi:.1f}             {s.sum():5d}   {pull_prod[s].mean():+7.3f}"
              f"                      {pull_own[f].mean():+.3f} +- {1 / math.sqrt(f.sum()):.3f}  ({pull_own[f].std():.3f})"
              + stop)
        if lo >= 0.5:
            ok &= f.sum() == s.sum() and abs(pull_own[s].mean()) < 0.15 and abs(pull_own[s].std() - 1) < 0.1
    # the mass: m such that own slowed-down lv of the measured momentum and direction gives the measured 1/beta
    # (bisection in log m), and without the slowing down, m = p sqrt(1/beta^2 - 1)
    lo, hi = np.full(len(inv), 1.0), np.full(len(inv), 3000.0)
    valid = (own_inv_beta(p_reco, lo, sin_reco, L, hit) < inv) & (own_inv_beta(p_reco, hi, sin_reco, L, hit) > inv)
    for _ in range(40):
        mid = np.sqrt(lo * hi)
        up = own_inv_beta(p_reco, mid, sin_reco, L, hit) > inv
        hi, lo = np.where(up, mid, hi), np.where(up, lo, mid)
    m = np.where(valid, np.sqrt(lo * hi), np.nan)
    with np.errstate(invalid="ignore"):
        m_naive = p_reco * np.sqrt(inv ** 2 - 1)
        s_m = m * np.hypot(s_p, inv * s_inv / (inv ** 2 - 1))
    pm = (m - M) / s_m
    good = np.isfinite(pm)
    half68 = 0.5 * (np.percentile(pm[good], 84.135) - np.percentile(pm[good], 15.865))
    print(f"  mass with own slowing down ({good.sum()} lv): median {np.median(m[good]):.1f} GeV (model {M:.1f});"
          f" expected resolution at the median {np.median(s_m[good] / m[good]):.3f}; pull median"
          f" {np.median(pm[good]):+.3f}, half-width of the central 68% {half68:.3f}")
    for lo_b, hi_b in [(0.3, 0.5), (0.5, 0.7), (0.7, 1.0)]:
        s = good & (beta0 >= lo_b) & (beta0 < hi_b)
        print(f"    beta {lo_b:.1f}-{hi_b:.1f}: {s.sum():5d} lv, median {np.median(m[s]):.1f} GeV"
              f" (without the slowing down {np.nanmedian(m_naive[s]):.1f} GeV)")
    ok &= abs(np.median(pm[good])) < 0.1 and abs(half68 - 1) < 0.1
    verdict("g", ok, "1/beta as own slowed-down lv (beta > 0.5); the mass at the model's within its expected error")
    return np.c_[beta0, m, m_naive]


def figure(d_rows, pull_k, f_rows, g_out, M):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    a = ax[0, 0]
    for who, mk in [("lv", "o"), ("hadrons", "s")]:
        r = [x for x in d_rows if x[3] == who]
        if r:
            a.errorbar([x[0] for x in r], [x[1] for x in r], [x[2] for x in r], fmt=mk, label=who)
    a.axhline(1, color="k", lw=0.8)
    a.set(xscale="log", xlabel=r"$\beta\gamma$", ylabel=r"MPV(deposit) / $\Delta_p$", title="(d) silicon, 0.3 mm",
          ylim=(0.85, 1.15))
    a.legend()
    a = ax[0, 1]
    a.hist(np.clip(pull_k, -5, 5), bins=60, range=(-5, 5), density=True, histtype="step", label="Geant4 + fit")
    xx = np.linspace(-5, 5, 200)
    a.plot(xx, np.exp(-xx ** 2 / 2) / math.sqrt(2 * math.pi), "k", lw=0.8, label="N(0, 1)")
    a.set(xlabel=r"$(\kappa - \kappa_{\rm true})/\sigma_{\rm expected}$", title="(e) tracker curvature")
    a.legend()
    a = ax[1, 0]
    f_rows = f_rows[f_rows[:, 0] < 0.8]
    a.scatter(f_rows[:, 0], f_rows[:, 1] / f_rows[:, 2], s=2, alpha=0.3, label="each lv")
    edges = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    idx = np.digitize(f_rows[:, 0], edges) - 1
    means = [f_rows[idx == k, 1].mean() / f_rows[idx == k, 2].mean() for k in range(len(edges) - 1)]
    a.plot(0.5 * (edges[1:] + edges[:-1]), means, "ko", label="mean loss ratio")
    a.axhline(1, color="k", lw=0.8)
    a.set(xlabel=r"$\beta$ at production", ylabel="loss up to muon station 1: Geant4 / own",
          title=r"(f) $|\eta| < 0.8$", ylim=(0.5, 1.5))
    a.legend()
    a = ax[1, 1]
    a.hist(g_out[np.isfinite(g_out[:, 1]), 1], bins=60, range=(250, 850), histtype="step", label="with own slowing down")
    a.hist(g_out[np.isfinite(g_out[:, 2]), 2], bins=60, range=(250, 850), histtype="step",
           label=r"$p\sqrt{1/\beta^2 - 1}$")
    a.axvline(M, color="k", lw=0.8)
    a.set(xlabel="mass from the tracker and the time of flight (GeV)", title="(g) all lv with 3 or more stations")
    a.legend()
    fig.tight_layout()
    (HERE / "figs").mkdir(exist_ok=True)
    fig.savefig(HERE / "figs" / "checks.png", dpi=120)


def main():
    vals = part_a()
    f = uproot.open(OUT / "detector" / "vll.root")
    part_bc(vals, f)
    pr = f["prim"].arrays(library="np")
    pdg_of = {(e, i): p for e, i, p in zip(pr["evt"], pr["id"], pr["pdg"])}
    prims = {(e, i): (p, px, py, pz, en) for e, i, p, px, py, pz, en in
             zip(pr["evt"], pr["id"], pr["pdg"], pr["px"], pr["py"], pr["pz"], pr["e"]) if abs(p) == LV}
    trk = f["trk"].arrays(library="np")
    muon = f["muon"].arrays(library="np")
    d_rows = part_d(trk, pdg_of)
    fits, pull_k = part_e(trk, prims)
    f_rows = part_f(muon, prims, vals["mlv"])
    g_out = part_g(muon, fits, vals["mlv"])
    stopped = int(np.sum((np.abs(pr["pdg"]) == LV) & (pr["endekin"] == 0)))
    print(f"lv stopped in the detector: {stopped} of {len(prims)}")
    figure(d_rows, pull_k, f_rows, g_out, vals["mlv"])
    print("summary: " + ", ".join(f"({n}) {'ok' if ok else 'FAIL'}" for n, ok in results))
    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    sys.exit(main())
