"""Step (1) of the Higgs note: the LO widths of H -> f fbar, H -> V V* and H -> 4 f.

(a) H -> f fbar, Eq. (lo): Gamma_0 = N_c y^2 M_H beta^3/(16 pi), the pole masses in beta, with the MS-bar Yukawa coupling at
    mu = M_H, M_H/2, 2 M_H (the NLO note's inputs, models/sm_nlo/Src/nlo_inputs.py) and with the pole Yukawa coupling
    sqrt(2) m/v_G, v_G = (sqrt(2) G_F)^(-1/2).  b, c, tau, mu.
(b) H -> V f fbar' (one V on shell, the other off shell, no width in its propagator), massless fermions: the hand sum|M|^2
    of Appendix A (equal to FeynCalc's, lo_feyncalc.wl) integrated over the Dalitz plot, summed over the fermions (three
    lepton and two quark doublets for W*, all but the top for Z*) and the two charge assignments of W W*, against Eq. (vv)
    (Keung-Marciano).  Two sets of couplings, the pole masses in both:
      G_F:    g_V^2 = 4 sqrt(2) G_F M_V^2, g_HVV = g_V M_V, s^2 = 1 - M_W^2/M_Z^2;
      MS-bar: g(M_H), g'(M_H), s^2(M_H), g_HVV = g_V^2 v_FJ/2 with v_FJ of the inputs (at M_t; the inputs do not run it).
    The fermion masses: the Feynman-gauge sum|M|^2 with masses (work/me_hvff.txt, lo_feyncalc.wl; y = sqrt(2) m/v) integrated
    for H -> W+ tau- nubar, W+ b cbar, Z tau+ tau-, Z b bbar in the G_F set, against the massless value.
(c) H -> 4 f with fixed-width Breit-Wigner propagators, massless fermions, in the factorised form (exact for V V -> 4 f with
    massless fermions; the q^mu q^nu parts of the propagators drop out on the currents)
       Gamma = int dq1^2/pi dq2^2/pi  sqrt(q1^2) G1(q1^2)/|D1|^2  sqrt(q2^2) G2(q2^2)/|D2|^2  Gamma(H -> V(q1) V(q2)),
       G(q^2) = N_c (cL^2 + cR^2) sqrt(q^2)/(24 pi),  Gamma(H -> V1 V2) = g_HVV^2 [2 + (k1.k2)^2/(q1^2 q2^2)] |p|/(8 pi M_H^2),
    for H -> nu_e e+ mu- nubar_mu, H -> e- e+ mu- mu+, and summed over all the pairs (W W; Z Z with 1/2 for the identical Z,
    without the interference of identical fermions or of W W with Z Z) with Gamma_V the LO width in the same couplings, so
    that the narrow-width limit is Eq. (vv): the ratio to Eq. (vv) is the effect of the widths.
Writes results/lo_hff.csv, results/lo_hvv.csv.
"""
import csv
import math
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.integrate import IntegrationWarning, quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "sm_nlo" / "Src"))
from nlo_inputs import POLE, VFJ, at  # noqa: E402

RES = HERE / "results"
RES.mkdir(exist_ok=True)
GF = 1.1663788e-5
VG = (math.sqrt(2) * GF)**-0.5
MH, MW, MZ = POLE["MH"], POLE["MW"], POLE["MZ"]


# %% (a) H -> f fbar
def gamma_ff(nc, y, m):
    return nc * y**2 * MH / (16 * math.pi) * (1 - 4 * m**2 / MH**2)**1.5


FF = [("b", 3, "MB", lambda p: p["yd"][2]), ("c", 3, "MC", lambda p: p["yu"][1]), ("tau", 1, "MTA", lambda p: p["ye"][2]),
      ("mu", 1, "MMU", lambda p: p["ye"][1])]
# %% (b) H -> V V*: couplings
def couplings(kind):
    """g_HWW, g_HZZ, g, gZ, s^2"""
    if kind == "G_F":
        g, gz = math.sqrt(4 * math.sqrt(2) * GF) * MW, math.sqrt(4 * math.sqrt(2) * GF) * MZ
        return g * MW, gz * MZ, g, gz, 1 - MW**2 / MZ**2
    p = at(MH)
    return p["g"]**2 * VFJ / 2, p["gZ"]**2 * VFJ / 2, p["g"], p["gZ"], p["s2"]


# (N_c, T3, Q) of the fermions of Z*, all but the top
ZF = [(1, 0.5, 0)] * 3 + [(1, -0.5, -1)] * 3 + [(3, 0.5, 2 / 3)] * 2 + [(3, -0.5, -1 / 3)] * 3
NWD = 9   # W* doublets with colours: 3 leptons + 2 x 3 quarks


def cz2(gz, s2, t3, q):   # cL^2 + cR^2 of the Z
    return gz**2 * ((t3 - q * s2)**2 + (q * s2)**2)


def rt(x):
    return (3 * (1 - 8 * x + 20 * x**2) / math.sqrt(4 * x - 1) * math.acos((3 * x - 1) / (2 * x**1.5))
            - (1 - x) * (2 - 13 * x + 47 * x**2) / (2 * x) - 1.5 * (1 - 6 * x + 4 * x**2) * math.log(x))


def km(ghvv, gv, mv, dprime):
    return 3 * ghvv**2 * gv**2 * MH * dprime * rt(mv**2 / MH**2) / (512 * math.pi**3 * mv**2)


def dalitz(f, m1, m2, m3, epsrel=1e-12):
    """int ds23 int ds12 f(s12, s13) / (256 pi^3 M_H^3): V = 1, f = 2, fbar' = 3"""
    def inner(s23):
        r = math.sqrt(s23)
        e2, e1 = (s23 - m3**2 + m2**2) / (2 * r), (MH**2 - s23 - m1**2) / (2 * r)
        a, b = math.sqrt(max(e1**2 - m1**2, 0.0)), math.sqrt(max(e2**2 - m2**2, 0.0))
        lo, hi = (e1 + e2)**2 - (a + b)**2, (e1 + e2)**2 - (a - b)**2
        return quad(lambda s12: f(s12, MH**2 + m1**2 + m2**2 + m3**2 - s12 - s23), lo, hi, epsabs=0.0, epsrel=epsrel, limit=200)[0]
    return quad(inner, (m2 + m3)**2, (MH - m1)**2, epsabs=0.0, epsrel=epsrel, limit=200)[0] / (256 * math.pi**3 * MH**3)


def hand3(nc, ghvv, c2, mv):
    def f(s12, s13):
        s23 = MH**2 + mv**2 - s12 - s13
        return nc * ghvv**2 * c2 * (s23 + (s12 - mv**2) * (s13 - mv**2) / mv**2) / (s23 - mv**2)**2
    return f


# %% (c) H -> 4 f with Breit-Wigner propagators
def gv_of(c2, nc=1):
    return lambda q2: nc * c2 * math.sqrt(q2) / (24 * math.pi)


def h_vv(ghvv, q1, q2):
    lam = (MH**2 - q1 - q2)**2 - 4 * q1 * q2
    if lam <= 0:
        return 0.0
    k12 = (MH**2 - q1 - q2) / 2
    return ghvv**2 * (2 + k12**2 / (q1 * q2)) * math.sqrt(lam) / (2 * MH) / (8 * math.pi * MH**2)


def four_f(ghvv, mv, gam, g1, g2, epsrel=1e-10):
    """the factorised H -> V V -> 4 f with BW propagators; tan mapping of both q^2"""
    def jac(th):    # q^2 and dq^2/|D|^2 for q^2 = M^2 + M Gamma tan(theta)
        return mv**2 + mv * gam * math.tan(th), 1 / (mv * gam)

    def inner(t1):
        q1, j1 = jac(t1)
        if q1 <= 0:
            return 0.0
        top = (MH - math.sqrt(q1))**2
        th0, th1 = math.atan(-mv / gam), math.atan((top - mv**2) / (mv * gam))
        def f2(t2):
            q2, j2 = jac(t2)
            return 0.0 if q2 <= 0 else j2 * math.sqrt(q2) * g2(q2) / math.pi * h_vv(ghvv, q1, q2)
        return j1 * math.sqrt(q1) * g1(q1) / math.pi * quad(f2, th0, th1, epsabs=0.0, epsrel=epsrel, limit=200)[0]
    # split where the q2 range stops containing the q2 peak, q1 = (M_H - M)^2: the region below is thin in theta1
    cut = math.atan(((MH - mv)**2 - mv**2) / (mv * gam))
    return sum(quad(inner, lo, hi, epsabs=0.0, epsrel=epsrel, limit=200)[0]
               for lo, hi in ((math.atan(-mv / gam), cut), (cut, math.atan((MH**2 - mv**2) / (mv * gam)))))



def main():
    pars = {xi: at(xi * MH) for xi in (1.0, 0.5, 2.0)}
    rows_ff = []
    print("(a) H -> f fbar at LO [MeV]: MS-bar y(mu) at mu = M_H (M_H/2, 2 M_H);  the pole y = sqrt(2) m/v_G;  the ratio at M_H")
    for f, nc, mk, yf in FF:
        m = POLE[mk]
        ms = [gamma_ff(nc, yf(pars[xi]), m) for xi in (1.0, 0.5, 2.0)]
        pole = gamma_ff(nc, math.sqrt(2) * m / VG, m)
        print("  %-4s %.6f (%.6f, %.6f)   pole %.6f   ratio %.4f   [m(mu = M_H) = y v_G/sqrt2 = %.4f GeV]"
              % (f, 1e3 * ms[0], 1e3 * ms[1], 1e3 * ms[2], 1e3 * pole, ms[0] / pole, yf(pars[1.0]) * VG / math.sqrt(2)))
        rows_ff.append([f, "%.10e" % ms[0], "%.10e" % ms[1], "%.10e" % ms[2], "%.10e" % pole, "%.6f" % (ms[0] / pole),
                        "%.6f" % (yf(pars[1.0]) * VG / math.sqrt(2))])
    with open(RES / "lo_hff.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fermion", "msbar_mu_MH", "msbar_mu_MH_half", "msbar_mu_2MH", "pole_yukawa", "msbar_over_pole", "m_msbar_MH"])
        w.writerows(rows_ff)


    rows_vv = []
    print("(b) H -> V V* at LO, massless fermions [MeV]: the Dalitz integral of the hand sum|M|^2 against Eq. (vv)")
    res_b = {}
    for kind in ("G_F", "MS-bar"):
        ghww, ghzz, g, gz, s2 = couplings(kind)
        gw_ch = dalitz(hand3(1, ghww, g**2 / 2, MW), MW, 0, 0)          # H -> W+ (one massless doublet, one colour)
        num_w = 2 * NWD * gw_ch
        num_z = sum(dalitz(hand3(nc, ghzz, cz2(gz, s2, t3, q), MZ), MZ, 0, 0) for nc, t3, q in ZF)
        dz = 7 / 12 - 10 / 9 * s2 + 40 / 27 * s2**2
        kw, kz = km(ghww, g, MW, 1.0), km(ghzz, gz, MZ, dz)
        res_b[kind] = (num_w, num_z, kw, kz, gw_ch)
        print("  %-6s WW*: Dalitz %.10f, Eq. (vv) %.10f (rel %+.1e);  ZZ*: Dalitz %.10f, Eq. (vv) %.10f (rel %+.1e)"
              % (kind, 1e3 * num_w, 1e3 * kw, num_w / kw - 1, 1e3 * num_z, 1e3 * kz, num_z / kz - 1))
        rows_vv += [["WW*", kind, "dalitz_massless", "%.10e" % num_w], ["WW*", kind, "eq_vv", "%.10e" % kw],
                    ["ZZ*", kind, "dalitz_massless", "%.10e" % num_z], ["ZZ*", kind, "eq_vv", "%.10e" % kz]]
    print("  MS-bar (g(M_H), v_FJ) over G_F: WW* %.5f, ZZ* %.5f;  (v_FJ/v_G)^2 = %.5f"
          % (res_b["MS-bar"][2] / res_b["G_F"][2], res_b["MS-bar"][3] / res_b["G_F"][3], (VFJ / VG)**2))

    # the fermion masses, with FeynCalc's sum|M|^2 (Feynman gauge, |V| = 1, y = sqrt(2) m/v)
    me = dict(line.strip().split("|", 1) for line in open(HERE / "work" / "me_hvff.txt") if "|" in line)
    ghww, ghzz, g, gz, s2 = couplings("G_F")
    ee = g * math.sqrt(s2)
    ns = {"Power": pow, "Sqrt": math.sqrt}
    base = {"MH": MH, "MW": MW, "MZ": MZ, "ee": ee, "Me": POLE["Me"], "MTA": POLE["MTA"], "MB": POLE["MB"], "MC": POLE["MC"]}
    print("  fermion masses (G_F set; Feynman-gauge sum|M|^2 of lo_feyncalc.wl; |V| = 1):")
    MASSIVE = [("W+ tau- nutaubar", MW, "MTA", None, 1, g**2 / 2), ("W+ b cbar", MW, "MB", "MC", 3, g**2 / 2),
               ("Z tau- tau+", MZ, "MTA", "MTA", 1, cz2(gz, s2, -0.5, -1)), ("Z b bbar", MZ, "MB", "MB", 3, cz2(gz, s2, -0.5, -1 / 3))]
    for lab, mv, k2, k3, nc, c2 in MASSIVE:
        code = compile(me[lab], lab, "eval")
        m2, m3 = POLE[k2], POLE[k3] if k3 else 0.0
        f = lambda s12, s13: eval(code, ns, dict(base, s12=s12, s13=s13))
        massive = dalitz(f, mv, m2, m3, epsrel=1e-10)
        massless = dalitz(hand3(nc, ghww if mv == MW else ghzz, c2, mv), mv, 0, 0)
        # the massive expression at tiny masses against the hand form (a check of the export)
        tiny = dict(base, MTA=1e-6, MB=1e-6, MC=1e-6)
        s12t, s13t = 0.3 * MH**2, 0.2 * MH**2 + mv**2 / 2
        chk = eval(code, ns, dict(tiny, s12=s12t, s13=s13t)) / hand3(nc, ghww if mv == MW else ghzz, c2, mv)(s12t, s13t) - 1
        print("    H -> %-17s massive %.8e MeV, massless %.8e MeV, ratio - 1 = %+.5f   (export at m = 1e-6 GeV vs hand: %+.1e)"
              % (lab, 1e3 * massive, 1e3 * massless, massive / massless - 1, chk))
        rows_vv += [[lab, "G_F", "massive", "%.10e" % massive], [lab, "G_F", "massless", "%.10e" % massless]]


    print("(c) H -> 4 f with Breit-Wigner propagators (G_F set, massless fermions; Gamma_V = LO width in the same couplings)")
    ghww, ghzz, g, gz, s2 = couplings("G_F")
    gw_lo = NWD * g**2 * MW / (48 * math.pi)
    gz_lo = sum(nc * cz2(gz, s2, t3, q) for nc, t3, q in ZF) * MZ / (24 * math.pi)
    w_tot = four_f(ghww, MW, gw_lo, gv_of(NWD * g**2 / 2), gv_of(NWD * g**2 / 2))
    zsum = sum(nc * cz2(gz, s2, t3, q) for nc, t3, q in ZF)
    z_tot = 0.5 * four_f(ghzz, MZ, gz_lo, gv_of(zsum), gv_of(zsum))
    w_1 = four_f(ghww, MW, gw_lo, gv_of(g**2 / 2), gv_of(g**2 / 2))
    z_1 = four_f(ghzz, MZ, gz_lo, gv_of(cz2(gz, s2, -0.5, -1)), gv_of(cz2(gz, s2, -0.5, -1)))
    kw, kz, gch = res_b["G_F"][2], res_b["G_F"][3], res_b["G_F"][4]
    print("  Gamma_W^LO = %.6f GeV, Gamma_Z^LO = %.6f GeV" % (gw_lo, gz_lo))
    print("  H -> W W -> 4 f (all pairs): %.8f MeV;  Eq. (vv) %.8f MeV;  ratio - 1 = %+.4f" % (1e3 * w_tot, 1e3 * kw, w_tot / kw - 1))
    print("  H -> Z Z -> 4 f (all pairs, 1/2): %.8f MeV;  Eq. (vv) %.8f MeV;  ratio - 1 = %+.4f" % (1e3 * z_tot, 1e3 * kz, z_tot / kz - 1))
    nw_1 = 2 * gch * (g**2 * MW / (48 * math.pi)) / gw_lo
    print("  H -> nu_e e+ mu- nubar_mu: %.8e MeV (narrow on-shell W x 2 x BR: %.8e MeV, ratio - 1 = %+.4f)"
          % (1e3 * w_1, 1e3 * nw_1, w_1 / nw_1 - 1))
    print("  H -> e- e+ mu- mu+: %.8e MeV" % (1e3 * z_1))
    # the narrow-width limit: all widths (total and partial) times 0.1 at a fixed branching ratio
    w_s = four_f(ghww, MW, 0.1 * gw_lo, gv_of(0.1 * NWD * g**2 / 2), gv_of(NWD * g**2 / 2))
    with warnings.catch_warnings():   # quad warns on the narrow Z peak; the value agrees to 1e-13 at epsrel 1e-8 and 1e-10
        warnings.simplefilter("ignore", IntegrationWarning)
        z_s = 0.5 * four_f(ghzz, MZ, 0.1 * gz_lo, gv_of(0.1 * zsum), gv_of(zsum))
    print("  the widths x 0.1 (the same branching ratios): WW %+.5f, ZZ %+.5f relative to Eq. (vv)  (x 1: %+.5f, %+.5f)"
          % (w_s / kw - 1, z_s / kz - 1, w_tot / kw - 1, z_tot / kz - 1))
    rows_vv += [["WW->4f", "G_F", "bw_width_x0.1", "%.10e" % w_s], ["ZZ->4f", "G_F", "bw_width_x0.1", "%.10e" % z_s]]
    rows_vv += [["WW->4f", "G_F", "bw_lo_width", "%.10e" % w_tot], ["ZZ->4f", "G_F", "bw_lo_width", "%.10e" % z_tot],
                ["nue e+ mu- numubar", "G_F", "bw_lo_width", "%.10e" % w_1], ["e- e+ mu- mu+", "G_F", "bw_lo_width", "%.10e" % z_1],
                ["Gamma_W", "G_F", "lo", "%.10e" % gw_lo], ["Gamma_Z", "G_F", "lo", "%.10e" % gz_lo]]
    with open(RES / "lo_hvv.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["channel", "couplings", "quantity", "width_GeV"])
        w.writerows(rows_vv)
    print("wrote results/lo_hff.csv, results/lo_hvv.csv")


if __name__ == "__main__":
    main()
