"""Research note models/sm_pp, step (4d): the SSM Z' mass limit of stage 6 of the LHC tools redone with the note's NLO.

Stage 6 (environment.pdf; tests/lhc/test_zprime.py, used here without change through its functions) set 95% CL limits on
sigma x B(Z' -> l l) from the ATLAS 139 fb^-1 dilepton spectra (HEPData; the published background function fitted, binned Poisson
likelihood, qtilde, asymptotic CLs) with signal templates from its Delphes samples (8000 events per mass, ATLAS card) and divided
them by its LO SSM cross section (MG5, no cuts; observed limit 5.04 TeV, expected 4.99 TeV).  Here each event is weighted by
  K(m) = (dsigma/dm)_NLO/(dsigma/dm)_LO   (zp_hadronic.py, results/zp_kfactor.csv; mu_R = mu_F = M as the samples),
m = the mass of the Z' (status 22) when it is in the event record, else the invariant mass of the two hard-process leptons
(status 23: MG5 does not write the Z' to the LHE far off shell; with the Z' in the record, its decay leptons are kept only as
final particles), so that the template shape and the normalisation follow the NLO m_ll distribution:
  template = L x sum_{selected in the bin} K / sum_{channel} K,   sigma_SSM,NLO = sigma_SSM,LO x <K> (<K> over all the events).
The lepton acceptance at NLO (the recoil against the extra parton) is not changed: the events keep their LO kinematics.
Checks: the LO limits (all K = 1) against stage 6; <K> of the events against the own K of the whole m_ll range.
Writes results/zp_limit.csv and the data of the note's figure (ResearchNote/figs/zp_k.dat: the own K of zp_hadronic.py;
zp_kmg5.dat: aMC@NLO's NLO/LO of zp_compare.csv; zp_ratio.dat: observed limit / sigma_SSM at LO and NLO, the expected at NLO,
and ATLAS's (NNLO, a reference)).  Run with ~/hep/opt/lhc/bin/python (from Src/); about 1.8 GB, about 1 minute.
"""
import csv
import math
import sys
from pathlib import Path

import awkward as ak
import numpy as np

SRC = Path(__file__).resolve().parent
LHC = SRC.parents[2] / "environment" / "tests" / "lhc"
sys.path.insert(0, str(LHC))
import test_zprime as tz  # noqa: E402

RES = SRC / "results"
FIGS = SRC.parent / "ResearchNote" / "figs"


def k_tables():
    tab = {}
    for row in csv.DictReader(open(RES / "zp_kfactor.csv")):
        tab.setdefault(int(row["M_GeV"]), []).append((float(row["m_ll_GeV"]), float(row["K"])))
    return {M: np.array(sorted(v)) for M, v in tab.items()}


def hard_mass(a):
    """the invariant mass of the two hard-process leptons (status 23, |pid| = 11 or 13)"""
    pid, st = a["Particle.PID"], a["Particle.Status"]
    hard = (st == 23) & ((abs(pid) == 11) | (abs(pid) == 13))
    e = ak.to_numpy(ak.sum(a["Particle.E"][hard], axis=1))
    px = ak.to_numpy(ak.sum(a["Particle.Px"][hard], axis=1))
    py = ak.to_numpy(ak.sum(a["Particle.Py"][hard], axis=1))
    pz = ak.to_numpy(ak.sum(a["Particle.Pz"][hard], axis=1))
    nhard = ak.to_numpy(ak.num(a["Particle.E"][hard]))
    return np.sqrt(np.maximum(e * e - px * px - py * py - pz * pz, 0.0)), nhard


def mass_limit(v, k):
    """the mass where log(limit/sigma) crosses 0, interpolated linearly between the masses (as stage 6)"""
    lr = np.log(v[:, k])
    i = np.where(np.diff(np.sign(lr)) != 0)[0]
    if not len(i):
        return float("nan")
    i = i[0]
    return v[i, 0] + (v[i + 1, 0] - v[i, 0]) * (0 - lr[i]) / (lr[i + 1] - lr[i])


def main():
    ktab = k_tables()
    own = {int(r["M_GeV"]): float(r["K"]) for r in csv.DictReader(open(RES / "zp_hadronic.csv"))}
    chans = {f: tz.Channel(f) for f in ("e", "mu")}
    for c in chans.values():
        c.bkg_fit()
    rows, ratios = [], {"LO": [], "NLO": []}
    for M in tz.MASSES:
        a = tz.events(M, "")
        ch, _, mt = tz.truth(a)
        mh, nhard = hard_mass(a)
        m = np.where(np.isfinite(mt), mt, mh)
        nmiss = int((~np.isfinite(mt) & (nhard != 2)).sum())
        mk, kk = ktab[M][:, 0], ktab[M][:, 1]
        w = np.interp(np.log(np.clip(m, mk[0], mk[-1])), np.log(mk), kk)
        kbar = float(w.mean())
        tm = {"LO": [], "NLO": []}
        for f, code in (("e", 11), ("mu", 13)):
            sel, mll = tz.select(a, f)
            inch = ch == code
            edges = np.append(chans[f].lo, chans[f].hi[-1])
            h_lo, _ = np.histogram(mll[sel & inch], bins=edges)
            h_nlo, _ = np.histogram(mll[sel & inch], bins=edges, weights=w[sel & inch])
            tm["LO"].append(tz.LUMI * h_lo / inch.sum())
            tm["NLO"].append(tz.LUMI * h_nlo / w[inch].sum())
        del a
        sig_lo = tz.card(M)[2] / 2 * 1e3      # fb per flavour: stage 6's MG5 LO (e and mu together), halved
        sig = {"LO": sig_lo, "NLO": sig_lo * kbar}
        line = []
        for order in ("LO", "NLO"):
            obs, exp = tz.cls_limit([chans["e"], chans["mu"]], tm[order], mu_hi=1.0)
            ratios[order].append((M, obs / sig[order], exp / sig[order]))
            rows.append([M, order, "%.6e" % sig[order], "%.6e" % obs, "%.6e" % exp, "%.6e" % (obs / sig[order]), "%.6e" % (exp / sig[order])])
            line.append("%s: limit obs %.4g, exp %.4g fb, SSM %.4g fb, obs/SSM %.4g" % (order, obs, exp, sig[order], obs / sig[order]))
        print("    M = %4d GeV: <K> of the events %.4f (own whole range %.4f; Z' in the record %d, two hard leptons %d, neither %d);"
              "  %s;  %s" % (M, kbar, own[M], int(np.isfinite(mt).sum()), int((~np.isfinite(mt) & (nhard == 2)).sum()), nmiss,
                             line[0], line[1]))
    res = {}
    for order in ("LO", "NLO"):
        v = np.array(ratios[order])
        res[order] = (mass_limit(v, 1), mass_limit(v, 2))
        print("(4d) SSM mass limit, %-3s cross section: observed %.0f GeV, expected %.0f GeV" % (order, *res[order]))
    print("    stage 6 (LO): observed 5040 GeV, expected 4990 GeV;  ATLAS (NNLO): 5100 GeV (references)")
    with open(RES / "zp_limit.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["M_GeV", "order", "sigma_SSM_fb", "limit_obs_fb", "limit_exp_fb", "obs_over_SSM", "exp_over_SSM"])
        wr.writerows(rows)
        for order in ("LO", "NLO"):
            wr.writerow(["mass_limit", order, "", "%.1f" % res[order][0], "%.1f" % res[order][1], "", ""])
    # the figure data
    FIGS.mkdir(exist_ok=True)
    with open(FIGS / "zp_k.dat", "w") as f:
        f.write("M K Kcut Kpeak\n")
        for r in csv.DictReader(open(RES / "zp_hadronic.csv")):
            f.write("%s %s %s %s\n" % (r["M_GeV"], r["K"], r["K_mll_gt_225"], r["K_peak_2Gamma"]))
    cmp = {}
    for r in csv.DictReader(open(RES / "zp_compare.csv")):
        if r["xiR,xiF"] == "1,1":
            cmp[(int(r["M_GeV"]), r["order"], r["quantity"].split()[0])] = (float(r["mg5_pb"]), float(r["mg5_err_pb"]))
    with open(FIGS / "zp_kmg5.dat", "w") as f:
        f.write("M Kcut Kcuterr Kpeak Kpeakerr\n")
        for M in (1000, 3000, 5000):
            nlo = "NLO_p" if M == 3000 else "NLO"
            vals = []
            for q in ("total", "window"):
                (n, en), (l, el) = cmp[(M, nlo, q)], cmp[(M, "LO", q)]
                vals += [n / l, n / l * math.hypot(en / n, el / l)]
            f.write("%d %.6f %.6f %.6f %.6f\n" % (M, *vals))
    with open(FIGS / "zp_ratio.dat", "w") as f:
        f.write("M lo nlo nloexp atlas\n")
        for (M, rlo, _), (_, rnlo, enlo) in zip(ratios["LO"], ratios["NLO"]):
            f.write("%d %.6e %.6e %.6e %.6e\n" % (M, rlo, rnlo, enlo, tz.atlas_ratio(M)))
    print("written: results/zp_limit.csv, figs/zp_k.dat, zp_kmg5.dat, zp_ratio.dat")


if __name__ == "__main__":
    main()
