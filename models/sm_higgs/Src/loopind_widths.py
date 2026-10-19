"""Step (2) of the Higgs note: the LO widths of H -> gamma gamma, Z gamma, g g and their dependence on the inputs.

Eq. (loop) and the Z gamma form (checked against the note's one-loop amplitudes in loopind.wl to 1e-18, and their normalization
against MadLoop's in loopind_madloop.py):
  Gamma(gamma gamma) = alpha^2 M_H^3/(256 pi^3 v^2) |sum_f N_c Q_f^2 A_1/2(tau_f) + A_1(tau_W)|^2,
  Gamma(Z gamma)     = G_F^2 M_W^2 alpha M_H^3/(64 pi^4) (1 - M_Z^2/M_H^2)^3 |sum_f N_c Q_f vhat_f/c_W A^Zg_1/2 + A^Zg_1|^2,
  Gamma(g g)         = alpha_s^2 M_H^3/(72 pi^3 v^2) |(3/4) sum_q A_1/2(tau_q)|^2,
with tau = M_H^2/(4 m^2) (Djouadi's tau = 4 m^2/M_H^2, lambda = 4 m^2/M_Z^2 in the Z gamma functions), the pole masses in the loop
functions (u, d, s massless: no contribution), 1/v^2 = sqrt(2) G_F, s_W^2 = 1 - M_W^2/M_Z^2.  The inputs that LO leaves open:
  (a) alpha(0) = 1/137.035999084 (the Thomson limit) for the on-shell photons, G_F, the pole masses: the reference;
  (b) the note's MS-bar alpha(M_H) = e^2(M_H)/(4 pi) in place of alpha(0);
  (c) the MS-bar Yukawa couplings y_t(M_H), y_b(M_H), y_c(M_H), y_tau(M_H) in place of sqrt(2) m/v_G in the H coupling of the
      fermion loops (the pole masses kept in the loop functions);
  (d) for g g, alpha_s at mu = M_H/2, 2 M_H.
Writes results/loopind_widths.csv.
"""
import cmath
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "sm_nlo" / "Src"))
from nlo_inputs import POLE, at  # noqa: E402

GF = 1.1663788e-5
ALPHA0 = 1 / 137.035999084
MH, MW, MZ = POLE["MH"], POLE["MW"], POLE["MZ"]
VG = (math.sqrt(2) * GF)**-0.5
S2 = 1 - MW**2 / MZ**2
CW = math.sqrt(1 - S2)
# name, N_c, T3, Q, pole-mass key, MS-bar Yukawa at mu
FERM = [("t", 3, 0.5, 2 / 3, "MT", lambda p: p["yu"][2]), ("b", 3, -0.5, -1 / 3, "MB", lambda p: p["yd"][2]),
        ("c", 3, 0.5, 2 / 3, "MC", lambda p: p["yu"][1]), ("tau", 1, -0.5, -1, "MTA", lambda p: p["ye"][2]),
        ("mu", 1, -0.5, -1, "MMU", lambda p: p["ye"][1]), ("e", 1, -0.5, -1, "Me", lambda p: p["ye"][0])]


def f(t):
    if t <= 1:
        return math.asin(math.sqrt(t))**2
    r = math.sqrt(1 - 1 / t)
    return -0.25 * (math.log((1 + r) / (1 - r)) - 1j * math.pi)**2


def g(t):
    if t <= 1:
        return math.sqrt(1 / t - 1) * math.asin(math.sqrt(t))
    r = math.sqrt(1 - 1 / t)
    return r / 2 * (math.log((1 + r) / (1 - r)) - 1j * math.pi)


def a_half(t):
    return 2 * (t + (t - 1) * f(t)) / t**2


def a_one(t):
    return -(2 * t**2 + 3 * t + 3 * (2 * t - 1) * f(t)) / t**2


def i1(ta, la):
    return (ta * la / (2 * (ta - la)) + ta**2 * la**2 / (2 * (ta - la)**2) * (f(1 / ta) - f(1 / la))
            + ta**2 * la / (ta - la)**2 * (g(1 / ta) - g(1 / la)))


def i2(ta, la):
    return -ta * la / (2 * (ta - la)) * (f(1 / ta) - f(1 / la))


def azg_half(ta, la):
    return i1(ta, la) - i2(ta, la)


def azg_one(ta, la):
    return CW * (4 * (3 - S2 / CW**2) * i2(ta, la) + ((1 + 2 / ta) * S2 / CW**2 - (5 + 2 / ta)) * i1(ta, la))


def amplitudes(yscale):
    """the sums of Eq. (loop) and of Z gamma, and the loops one by one; yscale[f]: the H coupling over sqrt(2) m/v_G"""
    aa, zg, gg, parts = a_one(MH**2 / (4 * MW**2)), azg_one(4 * MW**2 / MH**2, 4 * MW**2 / MZ**2), 0, {"W": a_one(MH**2 / (4 * MW**2))}
    for name, nc, t3, q, mk, _ in FERM:
        m = POLE[mk]
        k = yscale.get(name, 1.0)
        ah = a_half(MH**2 / (4 * m**2))
        parts[name] = k * nc * q**2 * ah
        aa += k * nc * q**2 * ah
        zg += k * nc * q * (2 * t3 - 4 * q * S2) / CW * azg_half(4 * m**2 / MH**2, 4 * m**2 / MZ**2)
        if nc == 3:
            gg += k * 0.75 * ah
    return aa, zg, gg, parts


def widths(alpha, alphas, yscale):
    aa, zg, gg, _ = amplitudes(yscale)
    w_aa = alpha**2 * MH**3 / (256 * math.pi**3 * VG**2) * abs(aa)**2
    w_zg = GF**2 * MW**2 * alpha * MH**3 / (64 * math.pi**4) * (1 - MZ**2 / MH**2)**3 * abs(zg)**2
    w_gg = alphas**2 * MH**3 / (72 * math.pi**3 * VG**2) * abs(gg)**2
    return w_aa, w_zg, w_gg


p = {xi: at(xi * MH) for xi in (1.0, 0.5, 2.0)}
amsbar = p[1.0]["alpha"]
ysc = {name: yf(p[1.0]) / (math.sqrt(2) * POLE[mk] / VG) for name, nc, t3, q, mk, yf in FERM}
_, _, _, parts = amplitudes({})
print("the loops of H -> gamma gamma (alpha(0), G_F, pole masses): " + ", ".join(
    "%s %s" % (k, ("%.5f" % v.real) if abs(v.imag) < 1e-12 else "%.5f%+.5fi" % (v.real, v.imag)) for k, v in parts.items()))
aa, zg, gg, _ = amplitudes({})
print("  sums: gamma gamma %.5f%+.5fi, Z gamma %.5f%+.5fi, g g %.5f%+.5fi" % (aa.real, aa.imag, zg.real, zg.imag, gg.real, gg.imag))
cases = [("(a) alpha(0), G_F, pole", ALPHA0, p[1.0]["alphas"], {}),
         ("(b) MS-bar alpha(M_H)", amsbar, p[1.0]["alphas"], {}),
         ("(c) MS-bar y_f(M_H)", ALPHA0, p[1.0]["alphas"], ysc),
         ("(d) alpha_s(M_H/2)", ALPHA0, p[0.5]["alphas"], {}),
         ("(d) alpha_s(2 M_H)", ALPHA0, p[2.0]["alphas"], {})]
ref = widths(*cases[0][1:])
rows = []
print("LO widths [MeV] (relative to (a)); 1/alpha(M_H) = %.4f, alpha_s(M_H) = %.5f, y_f(M_H)/(sqrt2 m/v_G): %s"
      % (1 / amsbar, p[1.0]["alphas"], ", ".join("%s %.4f" % (k, v) for k, v in ysc.items() if k in ("t", "b", "c", "tau"))))
for label, a, als, ys in cases:
    w = widths(a, als, ys)
    print("  %-26s gamma gamma %.6e (%+.2f%%)   Z gamma %.6e (%+.2f%%)   g g %.6e (%+.2f%%)"
          % (label, 1e3 * w[0], 100 * (w[0] / ref[0] - 1), 1e3 * w[1], 100 * (w[1] / ref[1] - 1), 1e3 * w[2], 100 * (w[2] / ref[2] - 1)))
    rows.append([label] + ["%.10e" % x for x in w])
with open(HERE / "results" / "loopind_widths.csv", "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["inputs", "gamma_gamma_GeV", "Z_gamma_GeV", "g_g_GeV"])
    wr.writerows(rows)
print("wrote results/loopind_widths.csv")
