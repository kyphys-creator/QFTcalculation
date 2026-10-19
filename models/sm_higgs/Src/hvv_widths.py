"""Step (7) of the Higgs note: Gamma(H -> W W*) and Gamma(H -> Z Z*) with the G_mu couplings, the V widths and the QCD factors.

The G_mu tree couplings (g0^2 = 4 sqrt2 G_F M_W^2, G0^2 = 4 sqrt2 G_F M_Z^2, s0^2 = 1 - M_W^2/M_Z^2), in which the FJ tadpoles do
not enter (hvv_scheme.wl: the MS-bar tree with v_FJ needs the H H V V tadpole vertex of the NLO amplitude to come close), with
the pole masses M_V = M_BW/sqrt(1 + Gamma^2/M^2) (the SM note's fit: Gamma_W = 2.085, Gamma_Z = 2.4955 GeV) and the fixed-width
Breit-Wigner propagators, the factorised four-fermion form of step (1) (lo_widths.four_f; massless fermions, W W: all 81 pairs,
Z Z: 1/2 for the identical Z, no interference of identical fermions or of W W with Z Z):
  (a) LO: the partial widths of V(q) -> f fbar' at LO, Gamma_V their sum at q^2 = M_V^2;
  (b) + QCD: the hadronic partial widths times (1 + alpha_s/pi) (massless quarks, alpha_s(M_V) of the inputs; the NLO note's
      factor), Gamma_V the sum again (so that the branching ratios add to 1): only the off-shell V* gains, on the on-shell V the
      factor cancels in the branching ratio;
  and Eq. (vv) (the narrow on-shell V) for reference.  The narrow-width limit (all widths, total and partial, times 0.1 at
  fixed branching ratios, as in step (1)): the QCD gain then is Gamma_V's, sum_f N_c c_f^2 K_f over sum_f N_c c_f^2 (the off-shell
  V* to all f fbar' with the on-shell V's branching ratios adding to 1); the rest of the gain at the physical widths comes from
  the region where both V are off the peak.  For step (8), LO + QCD also with alpha_s at M_V/2 and 2 M_V.
Writes results/hvv_widths.csv.
"""
import csv
import math
import sys
import warnings
from pathlib import Path

from scipy.integrate import IntegrationWarning

import lo_widths as lw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "sm_nlo" / "Src"))
from nlo_inputs import POLE, at  # noqa: E402

GF = 1.1663788e-5
MH = POLE["MH"]
MW = 80.3692 / math.sqrt(1 + (2.085 / 80.3692)**2)
MZ = 91.188 / math.sqrt(1 + (2.4955 / 91.188)**2)
S2 = 1 - MW**2 / MZ**2
G2 = 4 * math.sqrt(2) * GF * MW**2
GZ2 = 4 * math.sqrt(2) * GF * MZ**2
# the doublets of W*: (N_c, quark); the fermions of Z*: (N_c, T3, Q)
WD = [(1, False)] * 3 + [(3, True)] * 2
ZF = lw.ZF


def widths(qcd, xi=1.0):
    aw, az = at(xi * MW)["alphas"], at(xi * MZ)["alphas"]
    cw = sum(nc * (1 + (aw / math.pi if (qcd and q) else 0)) for nc, q in WD) * G2 / 2       # sum of N_c (cL^2 + cR^2) for W
    cz = sum(nc * lw.cz2(math.sqrt(GZ2), S2, t3, q) * (1 + (az / math.pi if (qcd and nc == 3) else 0)) for nc, t3, q in ZF)
    return cw, cz, cw * MW / (24 * math.pi), cz * MZ / (24 * math.pi)


def km(ghvv, gv2, mv, dprime):
    return 3 * ghvv**2 * gv2 * MH * dprime * lw.rt(mv**2 / MH**2) / (512 * math.pi**3 * mv**2)


rows = []
ghww, ghzz = math.sqrt(G2) * MW, math.sqrt(GZ2) * MZ
dz = 7 / 12 - 10 / 9 * S2 + 40 / 27 * S2**2
print("pole masses M_W = %.5f, M_Z = %.5f GeV;  s0^2 = %.6f" % (MW, MZ, S2))
kmw, kmz = km(ghww, G2, MW, 1.0), km(ghzz, GZ2, MZ, dz)
print("Eq. (vv) (narrow on-shell V, G_mu, pole masses): WW* %.6f MeV, ZZ* %.6f MeV" % (1e3 * kmw, 1e3 * kmz))
res, narrow, gam = {}, {}, {}
for label, qcd in (("LO", False), ("LO + QCD", True)):
    cw, cz, gw, gz = widths(qcd)
    ww = lw.four_f(ghww, MW, gw, lw.gv_of(cw), lw.gv_of(cw))
    zz = 0.5 * lw.four_f(ghzz, MZ, gz, lw.gv_of(cz), lw.gv_of(cz))
    with warnings.catch_warnings():   # quad warns on the narrow Z peak (step (1): the value agrees to 1e-13 at epsrel 1e-8, 1e-10)
        warnings.simplefilter("ignore", IntegrationWarning)
        narrow[label] = (lw.four_f(ghww, MW, 0.1 * gw, lw.gv_of(0.1 * cw), lw.gv_of(cw)),
                         0.5 * lw.four_f(ghzz, MZ, 0.1 * gz, lw.gv_of(0.1 * cz), lw.gv_of(cz)))
    res[label], gam[label] = (ww, zz), (gw, gz)
    print("  %-9s Gamma_W = %.5f, Gamma_Z = %.5f GeV;  Gamma(H -> W W* -> 4 f) = %.6f MeV (%+.2f%% of Eq. (vv)), "
          "Gamma(H -> Z Z* -> 4 f) = %.6f MeV (%+.2f%%)" % (label, gw, gz, 1e3 * ww, 100 * (ww / kmw - 1), 1e3 * zz, 100 * (zz / kmz - 1)))
    rows.append([label, "%.8f" % gw, "%.8f" % gz, "%.10e" % ww, "%.10e" % zz])
print("  the QCD factors raise W W* by %+.2f%% and Z Z* by %+.2f%%" % (100 * (res["LO + QCD"][0] / res["LO"][0] - 1),
                                                                      100 * (res["LO + QCD"][1] / res["LO"][1] - 1)))
gain = [res["LO + QCD"][i] / res["LO"][i] - 1 for i in (0, 1)]
gain_n = [narrow["LO + QCD"][i] / narrow["LO"][i] - 1 for i in (0, 1)]
gain_v = [gam["LO + QCD"][i] / gam["LO"][i] - 1 for i in (0, 1)]
print("  the QCD gain of Gamma_V (BR_had alpha_s/pi): W %+.3f%%, Z %+.3f%%;  of H -> V V* -> 4 f with the widths x 0.1 (fixed BR): "
      "WW %+.3f%%, ZZ %+.3f%%;  at the widths: WW %+.3f%%, ZZ %+.3f%%" % (*(100 * x for x in gain_v), *(100 * x for x in gain_n),
                                                                     *(100 * x for x in gain)))
for label in ("LO", "LO + QCD"):
    rows.append([label + ", widths x 0.1", "", "", "%.10e" % narrow[label][0], "%.10e" % narrow[label][1]])
for label, xi in (("LO + QCD, mu = M_V/2", 0.5), ("LO + QCD, mu = 2 M_V", 2.0)):
    cw, cz, gw, gz = widths(True, xi)
    ww = lw.four_f(ghww, MW, gw, lw.gv_of(cw), lw.gv_of(cw))
    zz = 0.5 * lw.four_f(ghzz, MZ, gz, lw.gv_of(cz), lw.gv_of(cz))
    print("  %-21s Gamma(H -> W W* -> 4 f) = %.6f MeV (%+.3f%%), Gamma(H -> Z Z* -> 4 f) = %.6f MeV (%+.3f%%)"
          % (label, 1e3 * ww, 100 * (ww / res["LO + QCD"][0] - 1), 1e3 * zz, 100 * (zz / res["LO + QCD"][1] - 1)))
    rows.append([label, "%.8f" % gw, "%.8f" % gz, "%.10e" % ww, "%.10e" % zz])
rows.append(["Eq. (vv)", "", "", "%.10e" % kmw, "%.10e" % kmz])
with open(HERE / "results" / "hvv_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["case", "Gamma_W_GeV", "Gamma_Z_GeV", "Gamma_HWW_GeV", "Gamma_HZZ_GeV"])
    w.writerows(rows)
print("wrote results/hvv_widths.csv")
