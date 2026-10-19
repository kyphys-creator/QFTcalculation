"""Step (8) of the Higgs note: the total width and the branching ratios, with the mu and scheme dependence.

The partial widths of steps (2)-(7) (results/*.csv), at mu = M_H and at M_H/2, 2 M_H (the same xi for all channels):
  b, c, tau, mu:   NLO with QCD, QED and the weak correction, MS-bar y(mu) (hff_widths.csv, step (5));
  s, d, u, e:      the massless NLO of Eq. (hqq) with QCD and QED, MS-bar y(mu), no weak correction (here);
  g g:             NLO in the heavy-top effective theory on the exact LO (hgg_widths.csv, step (6));
  gamma gamma, Z gamma: LO with alpha(0), G_F, the pole masses (loopind_widths.csv, step (2)), no mu;
  W W*, Z Z*:      the G_mu four-fermion widths with the QCD factors of the V decays, alpha_s at xi M_V (hvv_widths.csv, step (7)).
The scheme dependence, one shift per channel, taken as +-|shift| and added in quadrature (independent):
  W W*, Z Z*:      the tadpole-free part of the MS-bar against the G_F tree (hvv_scheme.csv: -3.98%, -0.57%), the size of the
                   electroweak NLO that this note does not compute;
  gamma gamma, Z gamma, g g: the MS-bar y_f(M_H) in place of sqrt(2) m/v_G in the H coupling of the loops (loopind_widths.csv
                   row (c)), the size of the missing NLO of the loops.
The mu envelope and the scheme part are added in quadrature, up and down.  For reference only (not computed here): the LHC Higgs
Cross Section Working Group's YR4 branching ratios at M_H = 125.20 GeV (de Florian et al., arXiv:1610.07922; the WG's BR table) and
the PDG 2024 Gamma_H.  Writes results/total_width.csv.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "sm_nlo" / "Src"))
from nlo_inputs import POLE, at  # noqa: E402

MH = POLE["MH"]
CF = 4 / 3
XIS = (1.0, 0.5, 2.0)
RES = HERE / "results"
# reference only: YR4 (LHC HXSWG) BR at M_H = 125.20 GeV and Gamma_H; PDG 2024 Gamma_H (equal on- and off-shell couplings)
YR4 = {"bb": 5.792e-1, "tautau": 6.240e-2, "mumu": 2.165e-4, "cc": 2.876e-2, "gg": 8.172e-2, "gamgam": 2.270e-3,
       "Zgam": 1.550e-3, "WW": 2.170e-1, "ZZ": 2.667e-2}
YR4_GAMMA = 4.115e-3
PDG_GAMMA = (3.7e-3, 1.9e-3, 1.4e-3)


def rows(name):
    return list(csv.DictReader(open(RES / name)))


def light(nc, q, yf):
    """the massless NLO of Eq. (hqq) with QCD (quarks) and QED, MS-bar y(mu)"""
    out = []
    for xi in XIS:
        p = at(xi * MH)
        c = (CF * p["alphas"] if nc == 3 else 0.0) + q**2 * p["alpha"]
        out.append(nc * yf(p)**2 * MH / (16 * math.pi) * (1 + c / math.pi * (17 / 4 + 1.5 * math.log(xi**2))))
    return out


gam = {}      # channel -> partial widths [GeV] at xi = 1, 1/2, 2
hff = {r["fermion"]: r for r in rows("hff_widths.csv")}
for ch, f in (("bb", "b"), ("cc", "c"), ("tautau", "tau"), ("mumu", "mu")):
    gam[ch] = [float(hff[f][k]) for k in ("nlo_full", "nlo_full_half", "nlo_full_2")]
gam["ss"] = light(3, -1 / 3, lambda p: p["yd"][1])
gam["dd + uu + ee"] = [sum(x) for x in zip(light(3, -1 / 3, lambda p: p["yd"][0]), light(3, 2 / 3, lambda p: p["yu"][0]),
                                          light(1, -1, lambda p: p["ye"][0]))]
hgg = {round(float(r["mu"]) / MH, 2): float(r["nlo_GeV"]) for r in rows("hgg_widths.csv")}
gam["gg"] = [hgg[xi] for xi in XIS]
li = {r["inputs"][:3]: r for r in rows("loopind_widths.csv")}
gam["gamgam"] = [float(li["(a)"]["gamma_gamma_GeV"])] * 3
gam["Zgam"] = [float(li["(a)"]["Z_gamma_GeV"])] * 3
hv = {r["case"]: r for r in rows("hvv_widths.csv")}
for ch, k in (("WW", "Gamma_HWW_GeV"), ("ZZ", "Gamma_HZZ_GeV")):
    gam[ch] = [float(hv[c][k]) for c in ("LO + QCD", "LO + QCD, mu = M_V/2", "LO + QCD, mu = 2 M_V")]
sch = {r["quantity"]: float(r["value"]) for r in rows("hvv_scheme.csv")}
shift = {"WW": sch["nontadpole_W"], "ZZ": sch["nontadpole_Z"],
         "gamgam": float(li["(c)"]["gamma_gamma_GeV"]) / float(li["(a)"]["gamma_gamma_GeV"]) - 1,
         "Zgam": float(li["(c)"]["Z_gamma_GeV"]) / float(li["(a)"]["Z_gamma_GeV"]) - 1,
         "gg": float(li["(c)"]["g_g_GeV"]) / float(li["(a)"]["g_g_GeV"]) - 1}
order = ["bb", "WW", "gg", "tautau", "cc", "ZZ", "gamgam", "Zgam", "mumu", "ss", "dd + uu + ee"]


def total(i, mod=None):
    g = {c: gam[c][i] for c in order}
    if mod:
        g[mod[0]] *= 1 + mod[1]
    t = sum(g.values())
    return t, {c: g[c] / t for c in order}


def band(f):
    """f(i, mod) -> value: the mu envelope (up, down) and the scheme part, relative to the central value"""
    c = f(0, None)
    mu = [f(i, None) for i in (1, 2)]
    up, dn = max(0.0, *(m - c for m in mu)), min(0.0, *(m - c for m in mu))
    s = math.sqrt(sum((f(0, (j, abs(shift[j]))) - c)**2 for j in shift))
    return c, up / c, dn / c, s / c, math.hypot(up, s) / c, -math.hypot(dn, s) / c


gt, br = total(0)
print("partial widths at mu = M_H [MeV], branching ratios with the mu envelope (M_H/2, 2 M_H; all channels together), the scheme"
      " part, the total;  YR4 at M_H = 125.20 GeV for reference")
out = []
for c in order:
    b = band(lambda i, m, c=c: total(i, m)[1][c])
    ref = ("  YR4 %.4e: BR ratio %.4f, Gamma ratio %.4f" % (YR4[c], br[c] / YR4[c], gam[c][0] / (YR4[c] * YR4_GAMMA))
           if c in YR4 else "")
    print("  %-12s %.6e  BR %.4e  mu %+.2f%% %+.2f%%  scheme +-%.2f%%  total %+.2f%% %+.2f%%%s"
          % (c, 1e3 * gam[c][0], br[c], 100 * b[1], 100 * b[2], 100 * b[3], 100 * b[4], 100 * b[5], ref))
    out.append([c, "%.10e" % gam[c][0], "%.10e" % gam[c][1], "%.10e" % gam[c][2], "%.8e" % br[c]]
               + ["%.6f" % x for x in b[1:]] + ["%.4e" % YR4[c] if c in YR4 else ""])
bt = band(lambda i, m: total(i, m)[0])
print("  sum of BR - 1: %.1e" % (sum(br.values()) - 1))
print("  Gamma_H = %.4f MeV  mu %+.2f%% %+.2f%%  scheme +-%.2f%%  total %+.2f%% %+.2f%%  (mu = M_H/2: %.4f, 2 M_H: %.4f MeV)"
      % (1e3 * gt, 100 * bt[1], 100 * bt[2], 100 * bt[3], 100 * bt[4], 100 * bt[5], 1e3 * total(1)[0], 1e3 * total(2)[0]))
print("  reference: YR4 Gamma_H = %.3f MeV (ratio %.4f);  PDG 2024 Gamma_H = %.1f +%.1f -%.1f MeV (ours at %+.2f sigma)"
      % (1e3 * YR4_GAMMA, gt / YR4_GAMMA, 1e3 * PDG_GAMMA[0], 1e3 * PDG_GAMMA[1], 1e3 * PDG_GAMMA[2],
         (gt - PDG_GAMMA[0]) / (PDG_GAMMA[1] if gt > PDG_GAMMA[0] else PDG_GAMMA[2])))
print("  the scheme shifts: " + ", ".join("%s %+.2f%%" % (j, 100 * shift[j]) for j in shift))
out.append(["total", "%.10e" % gt, "%.10e" % total(1)[0], "%.10e" % total(2)[0], "1"] + ["%.6f" % x for x in bt[1:]]
           + ["%.4e" % YR4_GAMMA])
with open(RES / "total_width.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["channel", "gamma_GeV", "gamma_half_GeV", "gamma_2_GeV", "br", "mu_up", "mu_down", "scheme", "total_up", "total_down",
                "yr4_br"])
    w.writerows(out)
print("wrote results/total_width.csv")
